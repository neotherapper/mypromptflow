#!/usr/bin/env python3
"""
Claude & Frontend Development Focused RSS Monitor
Monitors sources relevant to Claude, React, TypeScript, MCP, and AI development
"""

from typing import List, Dict, Any
from .rss_monitor import RSSSourceMonitor
from core import SourceMetadata, SourceType

# Claude, AI & Frontend Development focused sources
CLAUDE_FOCUSED_SOURCES = [
    {
        "source_id": "anthropic_blog",
        "source_name": "Anthropic Blog",
        "source_url": "https://www.anthropic.com/blog/rss.xml",
        "authority_score": 1.0,
        "topics": ["claude", "ai", "llm", "claude-code", "claude-desktop", "prompting"],
        "description": "Official Anthropic blog with Claude updates and AI research"
    },
    {
        "source_id": "react_blog",
        "source_name": "React Blog",
        "source_url": "https://react.dev/blog.rss",
        "authority_score": 1.0,
        "topics": ["react", "frontend", "javascript", "typescript", "web-development"],
        "description": "Official React blog with framework updates"
    },
    {
        "source_id": "vercel_blog",
        "source_name": "Vercel Blog",
        "source_url": "https://vercel.com/blog/rss.xml",
        "authority_score": 0.9,
        "topics": ["nextjs", "react", "typescript", "frontend", "deployment"],
        "description": "Vercel blog covering Next.js, React, and modern web development"
    },
    {
        "source_id": "dev_to_claude",
        "source_name": "Dev.to Claude Tag",
        "source_url": "https://dev.to/feed/tag/claude",
        "authority_score": 0.7,
        "topics": ["claude", "claude-code", "ai", "prompting", "tutorials"],
        "description": "Community articles about Claude and Claude Code"
    },
    {
        "source_id": "dev_to_react",
        "source_name": "Dev.to React Tag",
        "source_url": "https://dev.to/feed/tag/react",
        "authority_score": 0.75,
        "topics": ["react", "frontend", "typescript", "javascript", "tutorials"],
        "description": "React community tutorials and best practices"
    },
    {
        "source_id": "dev_to_typescript",
        "source_name": "Dev.to TypeScript Tag",
        "source_url": "https://dev.to/feed/tag/typescript",
        "authority_score": 0.75,
        "topics": ["typescript", "javascript", "frontend", "react", "type-safety"],
        "description": "TypeScript tutorials and advanced patterns"
    },
    {
        "source_id": "dev_to_ai",
        "source_name": "Dev.to AI Tag",
        "source_url": "https://dev.to/feed/tag/ai",
        "authority_score": 0.7,
        "topics": ["ai", "llm", "prompting", "ai-applications", "business-ideas"],
        "description": "AI development, prompting techniques, and application ideas"
    },
    {
        "source_id": "hackernews_ai",
        "source_name": "HackerNews AI",
        "source_url": "https://hnrss.org/newest?q=claude+OR+anthropic+OR+%22claude+code%22",
        "authority_score": 0.8,
        "topics": ["claude", "anthropic", "ai", "claude-code", "news"],
        "description": "HackerNews posts about Claude and Anthropic"
    },
    {
        "source_id": "hackernews_react",
        "source_name": "HackerNews React",
        "source_url": "https://hnrss.org/newest?q=react+OR+typescript+OR+nextjs",
        "authority_score": 0.8,
        "topics": ["react", "typescript", "nextjs", "frontend", "news"],
        "description": "HackerNews posts about React and TypeScript"
    },
    {
        "source_id": "simon_willison",
        "source_name": "Simon Willison's Blog",
        "source_url": "https://simonwillison.net/atom/everything/",
        "authority_score": 0.85,
        "topics": ["llm", "ai", "claude", "prompting", "ai-applications"],
        "description": "Expert insights on LLMs, Claude, and AI applications"
    },
    {
        "source_id": "openai_blog",
        "source_name": "OpenAI Blog",
        "source_url": "https://openai.com/blog/rss.xml",
        "authority_score": 0.95,
        "topics": ["ai", "llm", "gpt", "prompting", "ai-applications"],
        "description": "OpenAI updates and AI research"
    },
    {
        "source_id": "github_mcp",
        "source_name": "GitHub MCP Discussions",
        "source_url": "https://github.com/modelcontextprotocol/discussions/discussions.atom",
        "authority_score": 0.9,
        "topics": ["mcp", "mcp-servers", "claude", "ai-integration"],
        "description": "Model Context Protocol discussions and updates"
    }
]

class ClaudeFocusedMonitor:
    """
    Specialized monitor for Claude and frontend development topics
    """
    
    def __init__(self):
        self.sources = CLAUDE_FOCUSED_SOURCES
        self.monitors = {}
        self._initialize_monitors()
    
    def _initialize_monitors(self):
        """Initialize RSS monitors for all sources"""
        for source in self.sources:
            metadata = SourceMetadata(
                source_id=source["source_id"],
                source_name=source["source_name"],
                source_type=SourceType.RSS,
                source_url=source["source_url"],
                authority_score=source["authority_score"],
                update_frequency="hourly",
                topics=source["topics"]
            )
            
            self.monitors[source["source_id"]] = RSSSourceMonitor(
                metadata, 
                config={
                    "timeout": 15,
                    "max_items": 20
                }
            )
    
    async def monitor_all(self):
        """Monitor all Claude-focused sources"""
        results = {}
        for source_id, monitor in self.monitors.items():
            result = await monitor.monitor()
            results[source_id] = result
        return results
    
    async def monitor_by_topic(self, topic: str):
        """Monitor sources related to a specific topic"""
        relevant_sources = [
            s for s in self.sources 
            if topic.lower() in [t.lower() for t in s["topics"]]
        ]
        
        results = {}
        for source in relevant_sources:
            monitor = self.monitors[source["source_id"]]
            result = await monitor.monitor()
            results[source["source_id"]] = result
        
        return results
    
    def get_topic_sources(self, topic: str) -> List[Dict]:
        """Get all sources covering a specific topic"""
        return [
            s for s in self.sources
            if topic.lower() in [t.lower() for t in s["topics"]]
        ]
    
    def get_high_authority_sources(self, min_score: float = 0.85) -> List[Dict]:
        """Get sources with high authority scores"""
        return [
            s for s in self.sources
            if s["authority_score"] >= min_score
        ]


# Topic-specific configurations for Claude interests
TOPIC_CONFIGURATIONS = {
    "claude_development": {
        "name": "Claude & Claude Code Development",
        "keywords": ["claude", "claude code", "claude desktop", "anthropic", "constitutional ai"],
        "priority_sources": ["anthropic_blog", "dev_to_claude", "hackernews_ai", "simon_willison"],
        "quality_threshold": 0.8,
        "update_frequency": "every_30_min"
    },
    "frontend_react": {
        "name": "React & TypeScript Development",
        "keywords": ["react", "typescript", "nextjs", "hooks", "components", "jsx", "tsx"],
        "priority_sources": ["react_blog", "vercel_blog", "dev_to_react", "dev_to_typescript"],
        "quality_threshold": 0.75,
        "update_frequency": "hourly"
    },
    "mcp_servers": {
        "name": "MCP Server Development",
        "keywords": ["mcp", "model context protocol", "mcp server", "claude integration"],
        "priority_sources": ["github_mcp", "anthropic_blog", "dev_to_claude"],
        "quality_threshold": 0.85,
        "update_frequency": "daily"
    },
    "ai_prompting": {
        "name": "AI Prompting & Applications",
        "keywords": ["prompting", "prompt engineering", "llm", "ai applications", "business ideas"],
        "priority_sources": ["simon_willison", "dev_to_ai", "openai_blog", "anthropic_blog"],
        "quality_threshold": 0.7,
        "update_frequency": "hourly"
    }
}