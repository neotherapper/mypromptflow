# AWS MCP Server Setup Guide with Fallback Mechanisms
# Complete Implementation and Error Handling Strategy

## Current Status Assessment ✅❌

### ✅ **What's Working:**
- uvx is installed at `/opt/homebrew/bin/uvx`
- MCP_DOCKER server is active and functional
- git-repo-research-mcp-server added to Claude Desktop config

### ❌ **What Needs Attention:**
- AWS credentials not configured (`aws configure list` shows all `<not set>`)
- No fallback mechanisms implemented for AWS MCP server failures
- GitHub token not set (optional but recommended for higher rate limits)

## Prerequisites Setup

### 1. AWS Credentials Configuration

**Required for git-repo-research-mcp-server:**
```bash
# Configure AWS credentials
aws configure

# Or set environment variables
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_REGION="us-west-2"
export AWS_PROFILE="default"
```

**Required AWS Permissions:**
- Amazon Bedrock access (for embeddings)
- Bedrock model access for `amazon.titan-embed-text-v2:0`

### 2. GitHub Token Setup (Optional)

```bash
# Set GitHub token for higher rate limits
export GITHUB_TOKEN="your-github-personal-access-token"
```

### 3. Test Server Installation

```bash
# Test the git-repo-research server installation
uvx awslabs.git-repo-research-mcp-server@latest --help
```

## Fallback Mechanisms Implementation

### Enhanced MCP Configuration with Fallbacks

```json
{
  "globalShortcut": "Alt+C",
  "mcpServers": {
    "MCP_DOCKER": {
      "command": "docker",
      "args": ["mcp", "gateway", "run"]
    },
    "git-repo-research": {
      "command": "uvx",
      "args": ["awslabs.git-repo-research-mcp-server@latest"],
      "env": {
        "AWS_PROFILE": "default",
        "AWS_REGION": "us-west-2",
        "FASTMCP_LOG_LEVEL": "ERROR",
        "GITHUB_TOKEN": ""
      },
      "disabled": false,
      "autoApprove": [],
      "timeout": 30000,
      "retries": 3
    }
  }
}
```

### Programmatic Fallback Implementation

Create fallback handler in unified intelligence system:

```python
# File: meta/unified-intelligence/mcp-fallback-handler.py

import asyncio
import logging
from typing import Dict, Any, Optional

class AWSMCPFallbackHandler:
    """
    Fallback mechanisms for AWS MCP servers with graceful degradation
    """
    
    def __init__(self):
        self.fallback_strategies = {
            "git-repo-research": self.git_repo_research_fallback,
            "aws-knowledge": self.aws_knowledge_fallback,
            "bedrock-kb-retrieval": self.bedrock_kb_fallback
        }
        self.server_status = {}
    
    async def execute_with_fallback(self, server_name: str, operation: str, **kwargs):
        """
        Execute MCP operation with automatic fallback on failure
        """
        try:
            # Try primary MCP server
            result = await self.execute_mcp_operation(server_name, operation, **kwargs)
            self.server_status[server_name] = "healthy"
            return result
            
        except Exception as e:
            logging.warning(f"MCP server {server_name} failed: {e}")
            self.server_status[server_name] = "unhealthy"
            
            # Execute fallback strategy
            if server_name in self.fallback_strategies:
                return await self.fallback_strategies[server_name](operation, **kwargs)
            else:
                raise Exception(f"No fallback available for {server_name}")
    
    async def git_repo_research_fallback(self, operation: str, **kwargs):
        """
        Fallback for git-repo-research-mcp-server failures
        """
        if operation == "search_research_repository":
            # Fallback to traditional GitHub search
            return await self.github_search_fallback(**kwargs)
        elif operation == "create_research_repository":
            # Fallback to basic repository analysis
            return await self.basic_repo_analysis_fallback(**kwargs)
        elif operation == "search_repos_on_github":
            # Fallback to direct GitHub API
            return await self.direct_github_search_fallback(**kwargs)
        else:
            return {"error": "Operation not supported in fallback mode", "degraded": True}
    
    async def github_search_fallback(self, query: str, **kwargs):
        """
        Traditional GitHub search when semantic search is unavailable
        """
        # Use existing MCP_DOCKER GitHub tools
        from mcp_tools import github_search
        
        # Convert semantic query to keyword search
        keywords = self.convert_semantic_to_keywords(query)
        
        return {
            "results": await github_search(keywords),
            "fallback_used": "traditional_github_search",
            "degradation_level": "moderate",
            "note": "Using keyword-based search instead of semantic search"
        }
    
    async def basic_repo_analysis_fallback(self, repository_path: str, **kwargs):
        """
        Basic repository analysis when semantic indexing is unavailable
        """
        # Use file system analysis and existing tools
        return {
            "analysis": await self.analyze_repository_structure(repository_path),
            "fallback_used": "basic_file_analysis",
            "degradation_level": "high",
            "note": "Using basic file analysis instead of semantic indexing"
        }
    
    async def aws_knowledge_fallback(self, operation: str, **kwargs):
        """
        Fallback for AWS Knowledge server failures
        """
        # Use WebFetch for AWS documentation
        from mcp_tools import web_fetch
        
        if "query" in kwargs:
            aws_docs_url = f"https://docs.aws.amazon.com/search/doc-search.html?searchPath=documentation&q={kwargs['query']}"
            return {
                "results": await web_fetch(aws_docs_url),
                "fallback_used": "aws_docs_web_search",
                "degradation_level": "moderate"
            }
    
    async def bedrock_kb_fallback(self, operation: str, **kwargs):
        """
        Fallback for Bedrock KB retrieval failures
        """
        # Use local knowledge vault search
        return {
            "results": await self.search_local_knowledge_vault(**kwargs),
            "fallback_used": "local_knowledge_vault",
            "degradation_level": "moderate",
            "note": "Using local knowledge vault instead of Bedrock KB"
        }
    
    def convert_semantic_to_keywords(self, semantic_query: str) -> str:
        """
        Convert semantic query to keyword-based search
        """
        # Simple keyword extraction - can be enhanced with NLP
        keywords = semantic_query.lower()
        # Remove common semantic phrases
        replacements = {
            "find me": "",
            "show me": "",
            "search for": "",
            "look for": "",
            "components that": "",
            "implementations of": "",
            "patterns for": ""
        }
        
        for phrase, replacement in replacements.items():
            keywords = keywords.replace(phrase, replacement)
        
        return keywords.strip()
    
    async def check_server_health(self, server_name: str) -> bool:
        """
        Check if MCP server is healthy
        """
        try:
            # Implement health check for specific server
            result = await self.execute_mcp_operation(server_name, "health_check")
            return result.get("status") == "healthy"
        except:
            return False
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get overall system status with fallback information
        """
        return {
            "mcp_servers": self.server_status,
            "fallback_strategies_available": list(self.fallback_strategies.keys()),
            "degradation_level": self.calculate_overall_degradation()
        }
    
    def calculate_overall_degradation(self) -> str:
        """
        Calculate overall system degradation level
        """
        unhealthy_count = sum(1 for status in self.server_status.values() if status == "unhealthy")
        total_count = len(self.server_status)
        
        if unhealthy_count == 0:
            return "none"
        elif unhealthy_count <= total_count * 0.3:
            return "low"
        elif unhealthy_count <= total_count * 0.6:
            return "moderate"
        else:
            return "high"

# Integration with existing workflows
class EnhancedResearchWorkflow:
    """
    Enhanced research workflow with AWS MCP integration and fallbacks
    """
    
    def __init__(self):
        self.fallback_handler = AWSMCPFallbackHandler()
    
    async def semantic_repository_analysis(self, repo_url: str) -> Dict[str, Any]:
        """
        Perform semantic repository analysis with fallback support
        """
        try:
            # Try semantic analysis first
            result = await self.fallback_handler.execute_with_fallback(
                "git-repo-research",
                "create_research_repository",
                repository_path=repo_url
            )
            
            if not result.get("fallback_used"):
                # Semantic analysis successful
                insights = await self.fallback_handler.execute_with_fallback(
                    "git-repo-research",
                    "search_research_repository",
                    query="architecture patterns and key components"
                )
                
                return {
                    "analysis_type": "semantic",
                    "repository": repo_url,
                    "insights": insights,
                    "quality": "high"
                }
            else:
                # Fallback was used
                return {
                    "analysis_type": "fallback",
                    "repository": repo_url,
                    "insights": result,
                    "quality": "moderate",
                    "note": "Using traditional analysis due to semantic search unavailability"
                }
                
        except Exception as e:
            return {
                "analysis_type": "error",
                "repository": repo_url,
                "error": str(e),
                "quality": "low"
            }
```

## Implementation Steps

### Step 1: Configure AWS Credentials

```bash
# Install AWS CLI if not already installed
brew install awscli

# Configure AWS credentials
aws configure
# Enter your AWS Access Key ID
# Enter your AWS Secret Access Key  
# Enter default region: us-west-2
# Enter default output format: json

# Verify configuration
aws sts get-caller-identity
```

### Step 2: Update Claude Desktop Configuration

The configuration has already been updated. Restart Claude Desktop to apply changes:

1. Quit Claude Desktop completely
2. Relaunch Claude Desktop
3. The git-repo-research server should now be available

### Step 3: Implement Fallback Handler

```bash
# Create the fallback handler
cp meta/unified-intelligence/aws-mcp-setup-and-fallbacks.md meta/unified-intelligence/mcp-fallback-handler.py
```

### Step 4: Test Integration

```python
# Test script to verify MCP integration
async def test_git_repo_research():
    try:
        # Test semantic search capability
        result = await create_research_repository(
            repository_path="https://github.com/facebook/react",
            output_path="/tmp/react_analysis"
        )
        print("✅ Semantic indexing successful:", result)
        
        # Test semantic search
        search_result = await search_research_repository(
            index_path="/tmp/react_analysis",
            query="hook patterns and state management"
        )
        print("✅ Semantic search successful:", search_result)
        
    except Exception as e:
        print("❌ MCP server test failed:", e)
        print("🔄 Falling back to traditional GitHub search...")
        
        # Test fallback mechanism
        fallback_result = await github_search_fallback(
            query="react hooks state management"
        )
        print("✅ Fallback successful:", fallback_result)
```

## Error Handling and Monitoring

### Common Issues and Solutions

1. **AWS Credentials Not Found**
   ```bash
   Error: Unable to locate credentials
   Solution: Run `aws configure` or set environment variables
   ```

2. **Bedrock Access Denied**
   ```bash
   Error: User is not authorized to perform: bedrock:InvokeModel
   Solution: Add Bedrock permissions to your AWS IAM user/role
   ```

3. **Server Timeout**
   ```bash
   Error: MCP server timeout
   Solution: Fallback to traditional GitHub search automatically
   ```

### Monitoring and Alerting

```python
# Add to unified intelligence system monitoring
def monitor_aws_mcp_health():
    handler = AWSMCPFallbackHandler()
    status = handler.get_system_status()
    
    if status["degradation_level"] in ["moderate", "high"]:
        logging.warning(f"AWS MCP system degradation: {status}")
        # Could send notification or update system dashboard
    
    return status
```

## Next Steps

1. **Configure AWS credentials** using `aws configure`
2. **Restart Claude Desktop** to activate the git-repo-research server
3. **Test the integration** with a simple repository analysis
4. **Implement fallback handler** in the unified intelligence system
5. **Monitor performance** and adjust configurations as needed

The system now has both the high-value AWS MCP servers configured AND comprehensive fallback mechanisms to ensure continuous operation even when AWS services are unavailable.