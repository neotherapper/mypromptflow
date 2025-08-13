#!/usr/bin/env python3
"""
Enhanced Source List for Universal Topic Intelligence System
Focused on Claude, AI development tools, React/TypeScript, and practical AI applications
"""

# Enhanced Claude & AI Development focused sources
ENHANCED_CLAUDE_SOURCES = [
    # Official Claude/Anthropic Sources
    {
        "source_id": "anthropic_news",
        "source_name": "Anthropic News",
        "source_url": "https://www.anthropic.com/news/rss.xml",
        "authority_score": 1.0,
        "topics": ["claude", "anthropic", "claude-code", "constitutional-ai"],
        "relevance_keywords": ["claude", "opus", "sonnet", "haiku", "anthropic", "constitutional ai"],
        "exclude_keywords": ["voltage scaling", "hpc", "quantum computing", "blockchain"]
    },
    
    # AI Development Tools & Applications
    {
        "source_id": "langchain_blog",
        "source_name": "LangChain Blog",
        "source_url": "https://blog.langchain.dev/rss/",
        "authority_score": 0.9,
        "topics": ["llm", "ai-development", "claude", "prompting"],
        "relevance_keywords": ["langchain", "claude", "llm", "agents", "rag"],
        "exclude_keywords": ["cryptocurrency", "mining"]
    },
    {
        "source_id": "cursor_blog",
        "source_name": "Cursor Blog",
        "source_url": "https://cursor.sh/blog/rss.xml",
        "authority_score": 0.85,
        "topics": ["ai-coding", "claude", "development-tools"],
        "relevance_keywords": ["cursor", "ai coding", "claude", "copilot"],
        "exclude_keywords": []
    },
    
    # React & Frontend Development
    {
        "source_id": "react_status",
        "source_name": "React Status Newsletter",
        "source_url": "https://react.statuscode.com/rss/",
        "authority_score": 0.85,
        "topics": ["react", "frontend", "typescript"],
        "relevance_keywords": ["react", "hooks", "components", "next.js", "typescript"],
        "exclude_keywords": ["blockchain", "crypto", "web3"]
    },
    {
        "source_id": "typescript_weekly",
        "source_name": "TypeScript Weekly",
        "source_url": "https://typescript-weekly.com/rss.xml",
        "authority_score": 0.85,
        "topics": ["typescript", "javascript", "react"],
        "relevance_keywords": ["typescript", "type safety", "generics", "react"],
        "exclude_keywords": []
    },
    
    # AI Engineering & Best Practices
    {
        "source_id": "ai_engineer_substack",
        "source_name": "AI Engineer Newsletter",
        "source_url": "https://www.aiengineering.substack.com/feed",
        "authority_score": 0.8,
        "topics": ["ai-engineering", "llm", "claude", "best-practices"],
        "relevance_keywords": ["ai engineering", "llm", "claude", "prompt engineering", "rag"],
        "exclude_keywords": ["cryptocurrency", "nft", "blockchain"]
    },
    {
        "source_id": "one_useful_thing",
        "source_name": "One Useful Thing",
        "source_url": "https://www.oneusefulthing.org/feed",
        "authority_score": 0.85,
        "topics": ["ai-applications", "claude", "practical-ai"],
        "relevance_keywords": ["ai", "claude", "gpt", "practical", "business"],
        "exclude_keywords": []
    },
    
    # MCP & Claude Code specific
    {
        "source_id": "github_mcp_releases",
        "source_name": "MCP Releases",
        "source_url": "https://github.com/modelcontextprotocol/servers/releases.atom",
        "authority_score": 0.95,
        "topics": ["mcp", "claude-code", "integrations"],
        "relevance_keywords": ["mcp", "model context protocol", "claude", "integration"],
        "exclude_keywords": []
    },
    
    # Reddit Communities (High Signal)
    {
        "source_id": "reddit_localllama",
        "source_name": "Reddit LocalLLaMA",
        "source_url": "https://www.reddit.com/r/LocalLLaMA/search.rss?q=claude+OR+anthropic&restrict_sr=1&sort=new",
        "authority_score": 0.7,
        "topics": ["llm", "claude", "ai-community"],
        "relevance_keywords": ["claude", "anthropic", "opus", "sonnet"],
        "exclude_keywords": ["mining", "crypto"]
    },
    {
        "source_id": "reddit_claude_ai",
        "source_name": "Reddit Claude AI",
        "source_url": "https://www.reddit.com/r/ClaudeAI/.rss",
        "authority_score": 0.75,
        "topics": ["claude", "claude-code", "prompting"],
        "relevance_keywords": ["claude", "anthropic", "prompting", "claude code"],
        "exclude_keywords": []
    },
    
    # Developer Productivity & AI Tools
    {
        "source_id": "github_blog",
        "source_name": "GitHub Blog",
        "source_url": "https://github.blog/feed/",
        "authority_score": 0.9,
        "topics": ["development", "ai-tools", "copilot"],
        "relevance_keywords": ["copilot", "ai", "development", "productivity"],
        "exclude_keywords": ["security vulnerability", "cve"]
    },
    {
        "source_id": "dev_productivity_weekly",
        "source_name": "Developer Productivity Weekly",
        "source_url": "https://developerproductivity.substack.com/feed",
        "authority_score": 0.75,
        "topics": ["productivity", "ai-tools", "development"],
        "relevance_keywords": ["ai tools", "productivity", "claude", "copilot", "cursor"],
        "exclude_keywords": []
    },
    
    # Prompt Engineering & AI Best Practices
    {
        "source_id": "prompt_engineering_guide",
        "source_name": "Prompt Engineering Daily",
        "source_url": "https://promptengineering.substack.com/feed",
        "authority_score": 0.8,
        "topics": ["prompting", "claude", "best-practices"],
        "relevance_keywords": ["prompt", "claude", "prompting", "few shot", "chain of thought"],
        "exclude_keywords": ["crypto", "nft"]
    },
    
    # Frontend Architecture & Patterns
    {
        "source_id": "frontend_weekly",
        "source_name": "Frontend Weekly",
        "source_url": "https://frontendweekly.co/rss.xml",
        "authority_score": 0.8,
        "topics": ["frontend", "react", "typescript", "patterns"],
        "relevance_keywords": ["react", "typescript", "frontend", "components", "hooks"],
        "exclude_keywords": ["web3", "blockchain"]
    },
    
    # AI Research (Practical Focus)
    {
        "source_id": "papers_with_code",
        "source_name": "Papers with Code - LLM",
        "source_url": "https://paperswithcode.com/rss/area-natural-language-processing",
        "authority_score": 0.85,
        "topics": ["ai-research", "llm", "practical-ai"],
        "relevance_keywords": ["llm", "language model", "claude", "prompting", "rag"],
        "exclude_keywords": ["quantum", "hpc", "distributed computing"]
    }
]

# Content filtering rules
RELEVANCE_RULES = {
    "must_have_keywords": [
        # At least one of these should be present
        "claude", "anthropic", "opus", "sonnet", "haiku",
        "react", "typescript", "next.js", "frontend",
        "ai coding", "claude code", "cursor", "copilot",
        "prompt engineering", "llm", "ai development",
        "mcp", "model context protocol"
    ],
    
    "exclude_if_primary_topic": [
        # Exclude if these are the main topic
        "cryptocurrency", "blockchain", "nft", "web3",
        "quantum computing", "high performance computing", "hpc",
        "voltage scaling", "hardware optimization",
        "mining", "trading", "defi",
        "security vulnerability", "cve", "exploit"
    ],
    
    "boost_if_contains": [
        # Give extra priority to these
        "claude opus", "claude 4", "opus 4.1",
        "anthropic announcement", "claude release",
        "react 19", "next.js 15", "typescript 5",
        "claude code", "mcp server", "cursor ai"
    ]
}

def is_content_relevant(title: str, content: str = "") -> tuple[bool, float]:
    """
    Check if content is relevant to our interests
    
    Returns:
        (is_relevant, relevance_score)
    """
    combined_text = f"{title} {content}".lower()
    
    # Check for excluded topics
    for exclude_term in RELEVANCE_RULES["exclude_if_primary_topic"]:
        if exclude_term in title.lower():
            return False, 0.0
    
    # Check for must-have keywords
    has_relevant_keyword = False
    relevance_score = 0.5
    
    for keyword in RELEVANCE_RULES["must_have_keywords"]:
        if keyword in combined_text:
            has_relevant_keyword = True
            relevance_score = 0.7
            break
    
    # Boost for special content
    for boost_term in RELEVANCE_RULES["boost_if_contains"]:
        if boost_term in combined_text:
            relevance_score = min(1.0, relevance_score + 0.3)
    
    return has_relevant_keyword, relevance_score