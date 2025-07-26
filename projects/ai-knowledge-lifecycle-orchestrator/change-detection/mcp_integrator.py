#!/usr/bin/env python3
"""
MCP Integration Layer
AI Knowledge Lifecycle Orchestrator - MCP server integration with error handling and fallbacks

This module provides a unified interface for interacting with MCP servers for content retrieval
with comprehensive error handling, retry mechanisms, and intelligent fallback strategies.
"""

import asyncio
import logging
import time
import json
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable, Tuple
from enum import Enum
import aiohttp
import subprocess
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MCPServerType(Enum):
    """MCP Server types"""
    FETCH = "mcp__MCP_DOCKER__fetch"
    GITHUB = "mcp__MCP_DOCKER__github_server"
    SEARCH = "mcp__MCP_DOCKER__search"
    BROWSER = "mcp__MCP_DOCKER__browser_automation"
    WIKIPEDIA = "mcp__MCP_DOCKER__extract_key_facts"


class CircuitBreakerState(Enum):
    """Circuit breaker states"""
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


@dataclass
class MCPServerHealth:
    """Track MCP server health metrics"""
    server_name: str
    success_count: int = 0
    failure_count: int = 0
    last_success: Optional[datetime] = None
    last_failure: Optional[datetime] = None
    average_response_time: float = 0.0
    circuit_state: CircuitBreakerState = CircuitBreakerState.CLOSED
    circuit_opened_at: Optional[datetime] = None
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate"""
        total = self.success_count + self.failure_count
        return self.success_count / total if total > 0 else 0.0
    
    @property
    def is_healthy(self) -> bool:
        """Check if server is healthy"""
        return (self.circuit_state == CircuitBreakerState.CLOSED and 
                self.success_rate >= 0.8)


@dataclass
class MCPRequest:
    """Represents an MCP request"""
    server_type: MCPServerType
    method: str
    parameters: Dict[str, Any]
    timeout: float = 30.0
    retry_count: int = 3
    fallback_servers: List[MCPServerType] = None


@dataclass
class MCPResponse:
    """Represents an MCP response"""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    response_time: float = 0.0
    server_used: Optional[MCPServerType] = None
    from_cache: bool = False


class RateLimiter:
    """Rate limiter for MCP server requests"""
    
    def __init__(self, max_requests: int, time_window: int):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
    
    async def acquire(self) -> bool:
        """Acquire rate limit token"""
        current_time = time.time()
        
        # Clean old requests
        self.requests = [req_time for req_time in self.requests 
                        if current_time - req_time < self.time_window]
        
        if len(self.requests) >= self.max_requests:
            return False
        
        self.requests.append(current_time)
        return True
    
    def get_wait_time(self) -> float:
        """Get time to wait before next request is allowed"""
        if len(self.requests) < self.max_requests:
            return 0.0
        
        oldest_request = min(self.requests)
        return max(0.0, self.time_window - (time.time() - oldest_request))


class CircuitBreaker:
    """Circuit breaker for MCP server protection"""
    
    def __init__(self, failure_threshold: int = 5, timeout_duration: int = 300, 
                 success_threshold: int = 2):
        self.failure_threshold = failure_threshold
        self.timeout_duration = timeout_duration
        self.success_threshold = success_threshold
        self.reset()
    
    def reset(self):
        """Reset circuit breaker state"""
        self.failure_count = 0
        self.success_count = 0
        self.state = CircuitBreakerState.CLOSED
        self.opened_at = None
    
    def record_success(self):
        """Record successful operation"""
        if self.state == CircuitBreakerState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.reset()
        elif self.state == CircuitBreakerState.CLOSED:
            self.failure_count = max(0, self.failure_count - 1)
    
    def record_failure(self):
        """Record failed operation"""
        if self.state == CircuitBreakerState.CLOSED:
            self.failure_count += 1
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitBreakerState.OPEN
                self.opened_at = datetime.utcnow()
        elif self.state == CircuitBreakerState.HALF_OPEN:
            self.state = CircuitBreakerState.OPEN
            self.opened_at = datetime.utcnow()
    
    def can_execute(self) -> bool:
        """Check if request can be executed"""
        if self.state == CircuitBreakerState.CLOSED:
            return True
        elif self.state == CircuitBreakerState.OPEN:
            if (datetime.utcnow() - self.opened_at).total_seconds() > self.timeout_duration:
                self.state = CircuitBreakerState.HALF_OPEN
                self.success_count = 0
                return True
            return False
        else:  # HALF_OPEN
            return True


class MCPIntegrator:
    """
    Unified MCP server integration layer with intelligent routing,
    error handling, and performance optimization
    """
    
    def __init__(self, config_manager):
        """Initialize MCP integrator"""
        self.config = config_manager
        self.mcp_config = config_manager.get_mcp_integration_config()
        
        # Initialize server health tracking
        self.server_health = {}
        self.circuit_breakers = {}
        self.rate_limiters = {}
        
        # Initialize performance tracking
        self.performance_stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'average_response_time': 0.0,
            'cache_hits': 0,
            'fallback_uses': 0
        }
        
        # Response cache
        self.response_cache = {}
        self.cache_ttl = 300  # 5 minutes default
        
        self._initialize_server_configs()
        logger.info("MCP Integrator initialized successfully")
    
    def _initialize_server_configs(self):
        """Initialize server-specific configurations"""
        available_servers = self.mcp_config.get('available_mcp_servers', {})
        
        for server_name, server_config in available_servers.items():
            server_type = MCPServerType(server_config.get('server_name', server_name))
            
            # Initialize health tracking
            self.server_health[server_type] = MCPServerHealth(server_name=server_name)
            
            # Initialize circuit breaker
            self.circuit_breakers[server_type] = CircuitBreaker(
                failure_threshold=5,
                timeout_duration=300,
                success_threshold=2
            )
            
            # Initialize rate limiter
            perf_config = server_config.get('performance_characteristics', {})
            rate_limit = self._parse_rate_limit(perf_config.get('rate_limit', '60 requests per minute'))
            self.rate_limiters[server_type] = RateLimiter(
                max_requests=rate_limit[0],
                time_window=rate_limit[1]
            )
    
    def _parse_rate_limit(self, rate_limit_str: str) -> Tuple[int, int]:
        """Parse rate limit string into (requests, seconds)"""
        try:
            # Parse formats like "60 requests per minute", "10 requests per second"
            parts = rate_limit_str.lower().split()
            if len(parts) >= 4:
                requests = int(parts[0])
                time_unit = parts[3]
                
                if 'minute' in time_unit:
                    return requests, 60
                elif 'hour' in time_unit:
                    return requests, 3600
                elif 'second' in time_unit:
                    return requests, 1
                    
        except Exception as e:
            logger.warning(f"Error parsing rate limit '{rate_limit_str}': {e}")
        
        return 60, 60  # Default: 60 requests per minute
    
    async def fetch_content(self, url: str, preferred_server: str = None, 
                           content_type: str = None) -> Optional[str]:
        """
        Fetch content from URL using appropriate MCP server
        
        Args:
            url: URL to fetch content from
            preferred_server: Preferred MCP server to use
            content_type: Type of content (for optimization)
            
        Returns:
            Retrieved content or None if failed
        """
        try:
            # Determine best server for request
            server_type = self._select_server_for_request(url, preferred_server, content_type)
            
            # Create MCP request
            request = MCPRequest(
                server_type=server_type,
                method="fetch_content",
                parameters={"url": url},
                fallback_servers=self._get_fallback_servers(server_type)
            )
            
            # Execute request with fallbacks
            response = await self._execute_request_with_fallback(request)
            
            if response.success:
                return response.data
            else:
                logger.error(f"Failed to fetch content from {url}: {response.error}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching content from {url}: {e}")
            return None
    
    async def get_github_releases(self, owner: str, repo: str) -> Optional[List[Dict[str, Any]]]:
        """
        Get GitHub releases using GitHub MCP server
        
        Args:
            owner: Repository owner
            repo: Repository name
            
        Returns:
            List of releases or None if failed
        """
        try:
            request = MCPRequest(
                server_type=MCPServerType.GITHUB,
                method="get_releases",
                parameters={"owner": owner, "repo": repo},
                fallback_servers=[MCPServerType.FETCH]  # Fallback to web scraping
            )
            
            response = await self._execute_request_with_fallback(request)
            
            if response.success and isinstance(response.data, list):
                return response.data
            else:
                logger.error(f"Failed to get GitHub releases for {owner}/{repo}: {response.error}")
                return None
                
        except Exception as e:
            logger.error(f"Error getting GitHub releases for {owner}/{repo}: {e}")
            return None
    
    async def search_web(self, query: str, max_results: int = 10) -> Optional[List[Dict[str, Any]]]:
        """
        Search web using search MCP server
        
        Args:
            query: Search query
            max_results: Maximum number of results
            
        Returns:
            Search results or None if failed
        """
        try:
            request = MCPRequest(
                server_type=MCPServerType.SEARCH,
                method="search",
                parameters={"query": query, "max_results": max_results}
            )
            
            response = await self._execute_request_with_fallback(request)
            
            if response.success and isinstance(response.data, list):
                return response.data
            else:
                logger.error(f"Failed to search web for '{query}': {response.error}")
                return None
                
        except Exception as e:
            logger.error(f"Error searching web for '{query}': {e}")
            return None
    
    async def automate_browser(self, url: str, actions: List[Dict[str, Any]]) -> Optional[str]:
        """
        Automate browser actions using browser automation MCP server
        
        Args:
            url: URL to navigate to
            actions: List of browser actions to perform
            
        Returns:
            Page content or None if failed
        """
        try:
            request = MCPRequest(
                server_type=MCPServerType.BROWSER,
                method="automate",
                parameters={"url": url, "actions": actions},
                timeout=120.0,  # Longer timeout for browser automation
                retry_count=2   # Fewer retries due to resource intensity
            )
            
            response = await self._execute_request_with_fallback(request)
            
            if response.success:
                return response.data
            else:
                logger.error(f"Failed to automate browser for {url}: {response.error}")
                return None
                
        except Exception as e:
            logger.error(f"Error automating browser for {url}: {e}")
            return None
    
    def _select_server_for_request(self, url: str, preferred_server: str = None, 
                                  content_type: str = None) -> MCPServerType:
        """Select best MCP server for request"""
        # Use preferred server if specified and healthy
        if preferred_server:
            try:
                server_type = MCPServerType(preferred_server)
                if self.server_health[server_type].is_healthy:
                    return server_type
            except (ValueError, KeyError):
                pass
        
        # Select based on URL and content type
        if 'github.com' in url:
            if '/releases' in url or '/tags' in url:
                return MCPServerType.GITHUB
        
        if content_type == 'github_api':
            return MCPServerType.GITHUB
        elif content_type == 'dynamic_content':
            return MCPServerType.BROWSER
        
        # Default to fetch server for web content
        return MCPServerType.FETCH
    
    def _get_fallback_servers(self, primary_server: MCPServerType) -> List[MCPServerType]:
        """Get fallback servers for primary server"""
        fallback_map = {
            MCPServerType.FETCH: [MCPServerType.BROWSER],
            MCPServerType.GITHUB: [MCPServerType.FETCH],
            MCPServerType.SEARCH: [],
            MCPServerType.BROWSER: [MCPServerType.FETCH],
            MCPServerType.WIKIPEDIA: []
        }
        
        return fallback_map.get(primary_server, [])
    
    async def _execute_request_with_fallback(self, request: MCPRequest) -> MCPResponse:
        """Execute MCP request with fallback mechanism"""
        servers_to_try = [request.server_type]
        if request.fallback_servers:
            servers_to_try.extend(request.fallback_servers)
        
        last_error = None
        
        for server_type in servers_to_try:
            try:
                # Check circuit breaker
                if not self.circuit_breakers[server_type].can_execute():
                    logger.warning(f"Circuit breaker open for {server_type.value}")
                    continue
                
                # Check rate limiting
                if not await self.rate_limiters[server_type].acquire():
                    wait_time = self.rate_limiters[server_type].get_wait_time()
                    if wait_time > 0:
                        logger.info(f"Rate limited for {server_type.value}, waiting {wait_time:.1f}s")
                        await asyncio.sleep(min(wait_time, 10))  # Cap wait time
                        continue
                
                # Check cache first
                cache_key = self._get_cache_key(server_type, request)
                cached_response = self._get_cached_response(cache_key)
                if cached_response:
                    self.performance_stats['cache_hits'] += 1
                    return cached_response
                
                # Execute request
                response = await self._execute_single_request(server_type, request)
                
                # Update health metrics
                if response.success:
                    self._record_success(server_type, response.response_time)
                    # Cache successful response
                    self._cache_response(cache_key, response)
                    return response
                else:
                    self._record_failure(server_type, response.error)
                    last_error = response.error
                    
            except Exception as e:
                logger.error(f"Error executing request on {server_type.value}: {e}")
                self._record_failure(server_type, str(e))
                last_error = str(e)
        
        # All servers failed
        self.performance_stats['failed_requests'] += 1
        if len(servers_to_try) > 1:
            self.performance_stats['fallback_uses'] += 1
        
        return MCPResponse(
            success=False,
            error=f"All servers failed. Last error: {last_error}"
        )
    
    async def _execute_single_request(self, server_type: MCPServerType, 
                                    request: MCPRequest) -> MCPResponse:
        """Execute request on single MCP server"""
        start_time = time.time()
        
        try:
            # Execute based on server type and method
            if server_type == MCPServerType.FETCH:
                result = await self._execute_fetch_request(request)
            elif server_type == MCPServerType.GITHUB:
                result = await self._execute_github_request(request)
            elif server_type == MCPServerType.SEARCH:
                result = await self._execute_search_request(request)
            elif server_type == MCPServerType.BROWSER:
                result = await self._execute_browser_request(request)
            else:
                raise ValueError(f"Unsupported server type: {server_type}")
            
            response_time = time.time() - start_time
            
            return MCPResponse(
                success=True,
                data=result,
                response_time=response_time,
                server_used=server_type
            )
            
        except asyncio.TimeoutError:
            response_time = time.time() - start_time
            return MCPResponse(
                success=False,
                error="Request timeout",
                response_time=response_time,
                server_used=server_type
            )
        except Exception as e:
            response_time = time.time() - start_time
            return MCPResponse(
                success=False,
                error=str(e),
                response_time=response_time,
                server_used=server_type
            )
    
    async def _execute_fetch_request(self, request: MCPRequest) -> Any:
        """Execute fetch request using MCP fetch server"""
        if request.method == "fetch_content":
            url = request.parameters.get("url")
            if not url:
                raise ValueError("URL parameter required for fetch_content")
            
            # Simulate MCP server call
            # In production, this would use the actual MCP server
            try:
                proc = await asyncio.create_subprocess_exec(
                    "curl", "-s", "-L", "--max-time", "30", url,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=request.timeout)
                
                if proc.returncode == 0:
                    return stdout.decode('utf-8', errors='ignore')
                else:
                    raise Exception(f"Curl failed: {stderr.decode('utf-8', errors='ignore')}")
                    
            except asyncio.TimeoutError:
                raise asyncio.TimeoutError("Fetch request timed out")
        
        raise ValueError(f"Unsupported fetch method: {request.method}")
    
    async def _execute_github_request(self, request: MCPRequest) -> Any:
        """Execute GitHub request using MCP GitHub server"""
        if request.method == "get_releases":
            owner = request.parameters.get("owner")
            repo = request.parameters.get("repo")
            
            if not owner or not repo:
                raise ValueError("Owner and repo parameters required")
            
            # Simulate GitHub API call
            url = f"https://api.github.com/repos/{owner}/{repo}/releases"
            
            try:
                proc = await asyncio.create_subprocess_exec(
                    "curl", "-s", "-L", "--max-time", "30", url,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=request.timeout)
                
                if proc.returncode == 0:
                    content = stdout.decode('utf-8', errors='ignore')
                    try:
                        return json.loads(content)
                    except json.JSONDecodeError:
                        raise Exception("Invalid JSON response from GitHub API")
                else:
                    raise Exception(f"GitHub API request failed: {stderr.decode('utf-8', errors='ignore')}")
                    
            except asyncio.TimeoutError:
                raise asyncio.TimeoutError("GitHub request timed out")
        
        raise ValueError(f"Unsupported GitHub method: {request.method}")
    
    async def _execute_search_request(self, request: MCPRequest) -> Any:
        """Execute search request using MCP search server"""
        if request.method == "search":
            query = request.parameters.get("query")
            max_results = request.parameters.get("max_results", 10)
            
            if not query:
                raise ValueError("Query parameter required for search")
            
            # Simulate search (in production would use actual search MCP server)
            # Return mock search results for now
            return [
                {
                    "title": f"Search result for: {query}",
                    "url": f"https://example.com/search?q={query}",
                    "snippet": f"Mock search result content for query: {query}",
                    "timestamp": datetime.utcnow().isoformat()
                }
            ]
        
        raise ValueError(f"Unsupported search method: {request.method}")
    
    async def _execute_browser_request(self, request: MCPRequest) -> Any:
        """Execute browser automation request using MCP browser server"""
        if request.method == "automate":
            url = request.parameters.get("url")
            actions = request.parameters.get("actions", [])
            
            if not url:
                raise ValueError("URL parameter required for browser automation")
            
            # Simulate browser automation (in production would use actual browser MCP server)
            # For now, just fetch the page content
            try:
                proc = await asyncio.create_subprocess_exec(
                    "curl", "-s", "-L", "--max-time", "60", url,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=request.timeout)
                
                if proc.returncode == 0:
                    return stdout.decode('utf-8', errors='ignore')
                else:
                    raise Exception(f"Browser automation failed: {stderr.decode('utf-8', errors='ignore')}")
                    
            except asyncio.TimeoutError:
                raise asyncio.TimeoutError("Browser automation timed out")
        
        raise ValueError(f"Unsupported browser method: {request.method}")
    
    def _get_cache_key(self, server_type: MCPServerType, request: MCPRequest) -> str:
        """Generate cache key for request"""
        param_str = json.dumps(request.parameters, sort_keys=True)
        return f"{server_type.value}:{request.method}:{hash(param_str)}"
    
    def _get_cached_response(self, cache_key: str) -> Optional[MCPResponse]:
        """Get cached response if still valid"""
        if cache_key not in self.response_cache:
            return None
        
        cached_data, cached_at = self.response_cache[cache_key]
        
        # Check if cache is still valid
        if (datetime.utcnow() - cached_at).total_seconds() < self.cache_ttl:
            response = MCPResponse(**cached_data)
            response.from_cache = True
            return response
        
        # Remove stale cache entry
        del self.response_cache[cache_key]
        return None
    
    def _cache_response(self, cache_key: str, response: MCPResponse):
        """Cache successful response"""
        if response.success and response.data:
            cache_data = {
                'success': response.success,
                'data': response.data,
                'response_time': response.response_time,
                'server_used': response.server_used
            }
            self.response_cache[cache_key] = (cache_data, datetime.utcnow())
    
    def _record_success(self, server_type: MCPServerType, response_time: float):
        """Record successful operation"""
        health = self.server_health[server_type]
        health.success_count += 1
        health.last_success = datetime.utcnow()
        
        # Update average response time
        if health.average_response_time == 0:
            health.average_response_time = response_time
        else:
            health.average_response_time = (
                (health.average_response_time * (health.success_count - 1) + response_time) /
                health.success_count
            )
        
        # Update circuit breaker
        self.circuit_breakers[server_type].record_success()
        
        # Update performance stats
        self.performance_stats['total_requests'] += 1
        self.performance_stats['successful_requests'] += 1
        
        # Update average response time
        total_requests = self.performance_stats['total_requests']
        current_avg = self.performance_stats['average_response_time']
        self.performance_stats['average_response_time'] = (
            (current_avg * (total_requests - 1) + response_time) / total_requests
        )
    
    def _record_failure(self, server_type: MCPServerType, error: str):
        """Record failed operation"""
        health = self.server_health[server_type]
        health.failure_count += 1
        health.last_failure = datetime.utcnow()
        
        # Update circuit breaker
        self.circuit_breakers[server_type].record_failure()
        
        # Update performance stats
        self.performance_stats['total_requests'] += 1
        self.performance_stats['failed_requests'] += 1
        
        logger.warning(f"Server {server_type.value} failure: {error}")
    
    async def get_server_health(self) -> Dict[str, Dict[str, Any]]:
        """Get health status of all MCP servers"""
        health_status = {}
        
        for server_type, health in self.server_health.items():
            health_status[server_type.value] = {
                'success_count': health.success_count,
                'failure_count': health.failure_count,
                'success_rate': health.success_rate,
                'average_response_time': health.average_response_time,
                'circuit_state': health.circuit_state.value,
                'is_healthy': health.is_healthy,
                'last_success': health.last_success.isoformat() if health.last_success else None,
                'last_failure': health.last_failure.isoformat() if health.last_failure else None
            }
        
        return health_status
    
    async def get_performance_stats(self) -> Dict[str, Any]:
        """Get current performance statistics"""
        stats = self.performance_stats.copy()
        stats['cache_size'] = len(self.response_cache)
        stats['success_rate'] = (
            stats['successful_requests'] / stats['total_requests']
            if stats['total_requests'] > 0 else 0.0
        )
        return stats
    
    async def reset_performance_stats(self):
        """Reset performance statistics"""
        self.performance_stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'average_response_time': 0.0,
            'cache_hits': 0,
            'fallback_uses': 0
        }
        logger.info("MCP Integrator performance statistics reset")
    
    async def clear_cache(self):
        """Clear response cache"""
        cache_size = len(self.response_cache)
        self.response_cache.clear()
        logger.info(f"Cleared {cache_size} cached responses")
    
    async def health_check(self) -> bool:
        """Perform health check on all MCP servers"""
        try:
            # Test basic connectivity to each server type
            test_requests = [
                (MCPServerType.FETCH, "https://httpbin.org/get"),
                (MCPServerType.GITHUB, "microsoft/typescript"),
                (MCPServerType.SEARCH, "test query")
            ]
            
            all_healthy = True
            
            for server_type, test_param in test_requests:
                try:
                    if server_type == MCPServerType.FETCH:
                        result = await self.fetch_content(test_param)
                    elif server_type == MCPServerType.GITHUB:
                        owner, repo = test_param.split('/')
                        result = await self.get_github_releases(owner, repo)
                    elif server_type == MCPServerType.SEARCH:
                        result = await self.search_web(test_param, max_results=1)
                    
                    if not result:
                        all_healthy = False
                        logger.warning(f"Health check failed for {server_type.value}")
                        
                except Exception as e:
                    all_healthy = False
                    logger.error(f"Health check error for {server_type.value}: {e}")
            
            return all_healthy
            
        except Exception as e:
            logger.error(f"Error during health check: {e}")
            return False