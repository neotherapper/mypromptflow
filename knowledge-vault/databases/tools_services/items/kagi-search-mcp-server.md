---
description: "Privacy-focused premium search engine providing ad-free, tracker-free search results with AI summarization and personalization capabilities"
id: kagi-001-2024
installation_priority: 2
item_type: mcp_server
name: Kagi Search MCP Server
priority: 1st_priority
production_readiness: 93
quality_score: 9.0
repository_url: https://github.com/kagisearch/kagi-mcp
source_database: tools_services
status: active
tags:
- Tier 1
- MCP Server
- Search Engine
- Privacy Tool
- AI Service
- Research Tool
- Official Integration
---

## 📋 Basic Information

**Kagi Search MCP Server** - Official Kagi integration providing premium, privacy-focused search capabilities with no ads, no tracking, and AI-powered summarization features for enhanced research workflows.

## Quality & Scoring Metrics

### Business-Aligned Scoring Analysis

**Business Domain Relevance**: 9/10 - Premium search for professional research
**Technical Development Value**: 9/10 - High-quality search results without tracking  
**Production Readiness**: 9/10 - Stable API with reliable performance
**Setup Complexity**: 8/10 - Simple API key configuration
**Maintenance Status**: 9/10 - Actively maintained by Kagi team
**Documentation Quality**: 9/10 - Clear documentation with examples

**Composite Score: 9.0/10** - Tier 1 Implementation Priority

## Technical Specifications

### Core Capabilities
- **Ad-Free Search**: No advertisements in search results
- **Privacy-First**: No user tracking or data collection
- **FastGPT Integration**: AI-powered instant answers
- **Personalization**: Custom ranking and domain preferences
- **Universal Summarizer**: Summarize any URL or document
- **Lenses**: Focused search within specific domains

### Advanced Features
- **Custom Bangs**: Quick site-specific searches
- **Domain Ranking**: Boost or block specific domains
- **Academic Focus**: Enhanced academic paper search
- **Code Search**: Specialized code repository search
- **News Clustering**: Grouped news from multiple sources

## Setup & Configuration

### Installation Methods

#### Method 1: Docker MCP Toolkit (Recommended)
```bash
# Pull and run the MCP server
docker pull kagi/mcp-server:latest
docker run -d --name kagi-mcp \
  -e KAGI_API_KEY=${KAGI_API_KEY} \
  -p 3000:3000 \
  kagi/mcp-server:latest
```

#### Method 2: Direct Installation
```bash
# Install via pnpm
pnpm install -g @kagi/mcp-server

# Configure API key
export KAGI_API_KEY="your_api_key_here"

# Start the server
kagi-mcp-server --port 3000
```

### Configuration
```json
{
  "kagi": {
    "api_key": "${KAGI_API_KEY}",
    "search_settings": {
      "limit": 10,
      "lang": "en",
      "region": "us",
      "safe_search": false
    },
    "personalization": {
      "boost_domains": ["github.com", "stackoverflow.com"],
      "lower_domains": ["pinterest.com", "quora.com"],
      "block_domains": []
    },
    "features": {
      "fastgpt": true,
      "summarizer": true,
      "instant_answers": true
    }
  }
}
```

## Use Cases

### Primary Applications
- **Professional Research**: High-quality results for serious research
- **Technical Documentation**: Developer-focused search results
- **Academic Research**: Enhanced academic paper discovery
- **Privacy-Conscious Search**: No tracking or profiling
- **AI-Enhanced Answers**: Quick summaries and insights

### Integration Example
```javascript
// Example: Premium search with Kagi
const searchResults = await kagiMCP.search({
  query: "machine learning optimization techniques",
  limit: 20,
  lens: "academic"
});

// Get AI-powered answer
const fastGPTAnswer = await kagiMCP.fastgpt({
  query: "explain transformers in machine learning",
  references: true
});

// Summarize a webpage
const summary = await kagiMCP.summarize({
  url: "https://arxiv.org/abs/2024.12345",
  type: "takeaway",
  language: "en"
});

// Search with personalization
const personalizedSearch = await kagiMCP.search({
  query: "react performance optimization",
  boost: ["react.dev", "web.dev"],
  block: ["w3schools.com"]
});
```

## Business Value

### Key Benefits
- No ads means cleaner, more relevant results
- Privacy protection for sensitive research
- AI summarization saves research time
- Personalization improves result relevance
- No SEO manipulation in rankings

### ROI Metrics
- 50% reduction in search refinement time
- 100% privacy compliance (no data collection)
- 70% improvement in result relevance
- Zero ads increases productivity