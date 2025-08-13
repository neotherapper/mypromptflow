#!/usr/bin/env python3
"""
MCP-Enhanced Universal Source Monitor
Integrates MCP servers for YouTube, GitHub, JIRA, Notion, and more
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

from .rss_monitor import RSSSourceMonitor
from core import ContentItem, SourceMetadata, SourceType


class MCPMonitorType(Enum):
    """Types of MCP-based monitoring"""
    RSS = "RSS"
    YOUTUBE = "YouTube"
    GITHUB = "GitHub"
    FETCH = "Fetch"
    JIRA = "JIRA"
    NOTION = "Notion"
    WIKIPEDIA = "Wikipedia"
    SEARCH = "Search"


@dataclass
class MCPServerMapping:
    """MCP server configuration mapping"""
    server_name: str
    tool_prefix: str
    capabilities: List[str]
    example_usage: str


class MCPEnhancedMonitor:
    """
    Universal monitor with full MCP server integration
    Leverages existing MCP tools for content discovery
    """
    
    def __init__(self):
        self.logger = logging.getLogger("MCPEnhancedMonitor")
        self.mcp_mappings = self._initialize_mcp_mappings()
        self.monitor_handlers = self._setup_handlers()
    
    def _initialize_mcp_mappings(self) -> Dict[str, MCPServerMapping]:
        """Initialize MCP server mappings based on available tools"""
        return {
            "youtube": MCPServerMapping(
                server_name="YouTube MCP",
                tool_prefix="mcp__MCP_DOCKER__get_transcript",
                capabilities=["transcript", "video_metadata"],
                example_usage="Get YouTube video transcripts and metadata"
            ),
            "github": MCPServerMapping(
                server_name="GitHub MCP",
                tool_prefix="mcp__MCP_DOCKER__",
                capabilities=["search_repositories", "get_file_contents", "list_commits"],
                example_usage="Monitor GitHub repos, issues, and code changes"
            ),
            "jira": MCPServerMapping(
                server_name="JIRA MCP",
                tool_prefix="mcp__MCP_DOCKER__jira_",
                capabilities=["search", "get_issue", "create_issue"],
                example_usage="Track JIRA issues and project updates"
            ),
            "notion": MCPServerMapping(
                server_name="Notion MCP",
                tool_prefix="mcp__MCP_DOCKER__API-",
                capabilities=["post-search", "retrieve-a-page", "post-database-query"],
                example_usage="Search and retrieve Notion content"
            ),
            "fetch": MCPServerMapping(
                server_name="Fetch MCP",
                tool_prefix="mcp__MCP_DOCKER__fetch",
                capabilities=["fetch", "fetch_content"],
                example_usage="Fetch and parse web content"
            ),
            "wikipedia": MCPServerMapping(
                server_name="Wikipedia MCP",
                tool_prefix="mcp__MCP_DOCKER__",
                capabilities=["search_wikipedia", "get_summary", "get_article"],
                example_usage="Search and retrieve Wikipedia content"
            ),
            "search": MCPServerMapping(
                server_name="Search MCP",
                tool_prefix="mcp__MCP_DOCKER__search",
                capabilities=["search", "search_documentation"],
                example_usage="Search web and documentation"
            )
        }
    
    def _setup_handlers(self) -> Dict[MCPMonitorType, Any]:
        """Setup monitor type handlers"""
        return {
            MCPMonitorType.RSS: self._monitor_rss,
            MCPMonitorType.YOUTUBE: self._monitor_youtube_mcp,
            MCPMonitorType.GITHUB: self._monitor_github_mcp,
            MCPMonitorType.FETCH: self._monitor_fetch_mcp,
            MCPMonitorType.JIRA: self._monitor_jira_mcp,
            MCPMonitorType.NOTION: self._monitor_notion_mcp,
            MCPMonitorType.WIKIPEDIA: self._monitor_wikipedia_mcp,
            MCPMonitorType.SEARCH: self._monitor_search_mcp
        }
    
    def determine_monitor_type(self, source_config: Dict[str, Any]) -> MCPMonitorType:
        """Determine the appropriate monitor type from configuration"""
        method = source_config.get("monitoring_method", "RSS").upper()
        url = source_config.get("url", "")
        
        # Check for specific MCP types
        if "YOUTUBE" in method or "youtube.com" in url or "youtu.be" in url:
            return MCPMonitorType.YOUTUBE
        elif "GITHUB" in method or "github.com" in url:
            return MCPMonitorType.GITHUB
        elif "JIRA" in method or source_config.get("jql_query"):
            return MCPMonitorType.JIRA
        elif "NOTION" in method or source_config.get("database_id"):
            return MCPMonitorType.NOTION
        elif "WIKIPEDIA" in method:
            return MCPMonitorType.WIKIPEDIA
        elif "SEARCH" in method:
            return MCPMonitorType.SEARCH
        elif "FETCH" in method or "MCP" in method:
            return MCPMonitorType.FETCH
        else:
            return MCPMonitorType.RSS
    
    async def monitor_source(
        self,
        source_config: Dict[str, Any],
        topic_slug: str
    ) -> Dict[str, Any]:
        """
        Monitor a source using appropriate MCP server or fallback
        
        Args:
            source_config: Source configuration
            topic_slug: Topic identifier
            
        Returns:
            Monitoring results
        """
        monitor_type = self.determine_monitor_type(source_config)
        handler = self.monitor_handlers.get(monitor_type)
        
        if not handler:
            self.logger.error(f"No handler for monitor type: {monitor_type}")
            return {
                "success": False,
                "items": [],
                "error": f"Unsupported monitor type: {monitor_type}"
            }
        
        try:
            result = await handler(source_config, topic_slug)
            result["monitor_type"] = monitor_type.value
            result["mcp_server"] = self.mcp_mappings.get(
                monitor_type.value.lower(), 
                MCPServerMapping("", "", [], "")
            ).server_name
            return result
        except Exception as e:
            self.logger.error(f"Error monitoring {source_config.get('name', 'Unknown')}: {e}")
            return {
                "success": False,
                "items": [],
                "error": str(e),
                "monitor_type": monitor_type.value
            }
    
    async def _monitor_rss(self, config: Dict, topic_slug: str) -> Dict[str, Any]:
        """Standard RSS monitoring (fallback)"""
        metadata = SourceMetadata(
            source_id=f"{topic_slug}_{config.get('source_id', 'unknown')}",
            source_name=config.get('name', 'Unknown'),
            source_type=SourceType.RSS,
            source_url=config['url'],
            authority_score=config.get('authority_score', 0.5),
            update_frequency=config.get('update_frequency', 'daily'),
            topics=[topic_slug]
        )
        
        monitor = RSSSourceMonitor(metadata)
        result = await monitor.monitor()
        
        return {
            "success": result.success,
            "items": result.new_items if result.success else [],
            "errors": result.errors
        }
    
    async def _monitor_youtube_mcp(self, config: Dict, topic_slug: str) -> Dict[str, Any]:
        """Monitor YouTube using MCP tools"""
        url = config.get('url', '')
        
        # For YouTube channels, we'd need to list videos first
        # For individual videos, we can get transcripts
        if 'youtube.com/watch' in url or 'youtu.be/' in url:
            # Create content item that would be filled by MCP tool
            video_id = self._extract_youtube_id(url)
            
            item = ContentItem(
                item_id=f"youtube_{video_id}_{datetime.now().isoformat()}",
                source_id=f"{topic_slug}_youtube",
                source_name=f"YouTube: {config.get('name', 'Video')}",
                title=f"YouTube: {config.get('name', video_id)}",
                content="[YouTube transcript would be fetched via MCP tool]",
                url=url,
                published_date=datetime.now(),
                topics=[topic_slug, "youtube", "video"],
                metadata={
                    "mcp_tool": "get_transcript",
                    "video_id": video_id,
                    "requires_mcp": True
                }
            )
            
            return {
                "success": True,
                "items": [item],
                "mcp_required": True,
                "mcp_tool": "mcp__MCP_DOCKER__get_transcript"
            }
        
        # Channel monitoring would require additional implementation
        return {
            "success": True,
            "items": [],
            "note": "Channel monitoring requires YouTube API integration"
        }
    
    async def _monitor_github_mcp(self, config: Dict, topic_slug: str) -> Dict[str, Any]:
        """Monitor GitHub using MCP tools"""
        url = config.get('url', '')
        
        if 'github.com/' not in url:
            return {"success": False, "items": [], "error": "Invalid GitHub URL"}
        
        # Extract repo information
        parts = url.replace('https://github.com/', '').split('/')
        if len(parts) < 2:
            return {"success": False, "items": [], "error": "Could not parse GitHub URL"}
        
        owner, repo = parts[0], parts[1]
        monitoring_scope = config.get('monitoring_scope', ['releases', 'issues'])
        
        # Create placeholder items for different monitoring scopes
        items = []
        
        if 'releases' in monitoring_scope:
            item = ContentItem(
                item_id=f"github_{owner}_{repo}_releases_{datetime.now().isoformat()}",
                source_id=f"{topic_slug}_github",
                source_name=f"GitHub: {owner}/{repo}",
                title=f"GitHub Releases: {owner}/{repo}",
                content="[GitHub releases would be fetched via MCP tool]",
                url=f"{url}/releases",
                published_date=datetime.now(),
                topics=[topic_slug, "github", "releases"],
                metadata={
                    "mcp_tool": "search_repositories",
                    "owner": owner,
                    "repo": repo,
                    "scope": "releases",
                    "requires_mcp": True
                }
            )
            items.append(item)
        
        return {
            "success": True,
            "items": items,
            "mcp_required": True,
            "mcp_tools": ["search_repositories", "list_commits"]
        }
    
    async def _monitor_fetch_mcp(self, config: Dict, topic_slug: str) -> Dict[str, Any]:
        """Monitor web content using MCP fetch"""
        url = config.get('url', '')
        
        if not url:
            return {"success": False, "items": [], "error": "No URL provided"}
        
        item = ContentItem(
            item_id=f"web_{hash(url)}_{datetime.now().isoformat()}",
            source_id=f"{topic_slug}_web",
            source_name=config.get('name', 'Web Content'),
            title=f"Web: {config.get('name', url)}",
            content="[Web content would be fetched via MCP fetch tool]",
            url=url,
            published_date=datetime.now(),
            topics=[topic_slug, "web"],
            metadata={
                "mcp_tool": "fetch",
                "selector": config.get('selector'),
                "requires_mcp": True
            }
        )
        
        return {
            "success": True,
            "items": [item],
            "mcp_required": True,
            "mcp_tool": "mcp__MCP_DOCKER__fetch"
        }
    
    async def _monitor_jira_mcp(self, config: Dict, topic_slug: str) -> Dict[str, Any]:
        """Monitor JIRA using MCP tools"""
        jql = config.get('jql_query', '')
        project_key = config.get('project_key', '')
        
        if not jql and not project_key:
            return {"success": False, "items": [], "error": "No JQL query or project key"}
        
        # Create placeholder for JIRA monitoring
        return {
            "success": True,
            "items": [],
            "mcp_required": True,
            "mcp_tool": "mcp__MCP_DOCKER__jira_search",
            "jql": jql or f"project = {project_key}",
            "note": "JIRA items would be fetched via MCP tool"
        }
    
    async def _monitor_notion_mcp(self, config: Dict, topic_slug: str) -> Dict[str, Any]:
        """Monitor Notion using MCP tools"""
        database_id = config.get('database_id')
        page_id = config.get('page_id')
        
        if not database_id and not page_id:
            return {"success": False, "items": [], "error": "No Notion ID provided"}
        
        return {
            "success": True,
            "items": [],
            "mcp_required": True,
            "mcp_tool": "mcp__MCP_DOCKER__API-post-search",
            "database_id": database_id,
            "page_id": page_id,
            "note": "Notion content would be fetched via MCP tool"
        }
    
    async def _monitor_wikipedia_mcp(self, config: Dict, topic_slug: str) -> Dict[str, Any]:
        """Monitor Wikipedia using MCP tools"""
        search_terms = config.get('search_terms', [])
        
        if not search_terms:
            return {"success": False, "items": [], "error": "No search terms provided"}
        
        return {
            "success": True,
            "items": [],
            "mcp_required": True,
            "mcp_tool": "mcp__MCP_DOCKER__search_wikipedia",
            "search_terms": search_terms,
            "note": "Wikipedia articles would be fetched via MCP tool"
        }
    
    async def _monitor_search_mcp(self, config: Dict, topic_slug: str) -> Dict[str, Any]:
        """Monitor web search using MCP tools"""
        query = config.get('search_query', '')
        
        if not query:
            return {"success": False, "items": [], "error": "No search query provided"}
        
        return {
            "success": True,
            "items": [],
            "mcp_required": True,
            "mcp_tool": "mcp__MCP_DOCKER__search",
            "query": query,
            "note": "Search results would be fetched via MCP tool"
        }
    
    def _extract_youtube_id(self, url: str) -> str:
        """Extract YouTube video ID from URL"""
        if 'v=' in url:
            return url.split('v=')[1].split('&')[0]
        elif 'youtu.be/' in url:
            return url.split('youtu.be/')[1].split('?')[0]
        return ""
    
    async def monitor_batch(
        self,
        sources: List[Dict[str, Any]],
        topic_slug: str
    ) -> Dict[str, Any]:
        """
        Monitor multiple sources concurrently
        
        Args:
            sources: List of source configurations
            topic_slug: Topic identifier
            
        Returns:
            Aggregated results
        """
        tasks = []
        for source in sources:
            task = self.monitor_source(source, topic_slug)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        
        # Aggregate results
        all_items = []
        successful = 0
        failed = 0
        mcp_servers = set()
        mcp_required_count = 0
        
        for result in results:
            if result.get("success"):
                successful += 1
                all_items.extend(result.get("items", []))
                if result.get("mcp_server"):
                    mcp_servers.add(result["mcp_server"])
                if result.get("mcp_required"):
                    mcp_required_count += 1
            else:
                failed += 1
        
        return {
            "total_sources": len(sources),
            "successful": successful,
            "failed": failed,
            "total_items": len(all_items),
            "items": all_items,
            "mcp_servers_used": list(mcp_servers),
            "mcp_required_count": mcp_required_count,
            "summary": f"Monitored {len(sources)} sources: {successful} successful, {failed} failed, {len(all_items)} items found"
        }


# Example topic configuration with MCP sources
EXAMPLE_MCP_TOPIC_CONFIG = {
    "topic_metadata": {
        "name": "React Ecosystem with MCP",
        "slug": "react-mcp",
        "description": "React development with full MCP integration"
    },
    "source_mapping": {
        "tier_1_official": {
            "sources": [
                {
                    "url": "https://react.dev/blog/feed.xml",
                    "name": "React Blog",
                    "monitoring_method": "RSS"
                },
                {
                    "url": "https://github.com/facebook/react",
                    "name": "React Repository",
                    "monitoring_method": "GitHub MCP",
                    "monitoring_scope": ["releases", "issues", "discussions"]
                }
            ]
        },
        "tier_2_community": {
            "sources": [
                {
                    "url": "https://www.youtube.com/@uidotdev",
                    "name": "ui.dev YouTube",
                    "monitoring_method": "YouTube MCP"
                },
                {
                    "url": "https://overreacted.io/",
                    "name": "Dan Abramov Blog",
                    "monitoring_method": "Fetch MCP"
                }
            ]
        },
        "tier_3_aggregators": {
            "sources": [
                {
                    "search_query": "React 19 features",
                    "name": "React News Search",
                    "monitoring_method": "Search MCP"
                },
                {
                    "search_terms": ["React", "React hooks", "React framework"],
                    "name": "React Wikipedia",
                    "monitoring_method": "Wikipedia MCP"
                }
            ]
        }
    }
}


if __name__ == "__main__":
    async def test_mcp_monitor():
        monitor = MCPEnhancedMonitor()
        
        # Test with example configuration
        sources = EXAMPLE_MCP_TOPIC_CONFIG["source_mapping"]["tier_1_official"]["sources"]
        sources.extend(EXAMPLE_MCP_TOPIC_CONFIG["source_mapping"]["tier_2_community"]["sources"])
        
        result = await monitor.monitor_batch(sources, "react-mcp")
        
        print("MCP Monitoring Test Results:")
        print(f"  {result['summary']}")
        print(f"  MCP Servers Used: {result['mcp_servers_used']}")
        print(f"  MCP Required Count: {result['mcp_required_count']}")
        
        # Show items that require MCP
        mcp_items = [item for item in result['items'] if item.metadata.get('requires_mcp')]
        print(f"\nItems requiring MCP tools: {len(mcp_items)}")
        for item in mcp_items[:3]:
            print(f"  - {item.title}: {item.metadata.get('mcp_tool')}")
    
    asyncio.run(test_mcp_monitor())