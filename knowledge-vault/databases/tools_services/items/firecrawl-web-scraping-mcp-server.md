---
description: "Advanced web scraping and data extraction server that converts websites into clean, structured data optimized for LLMs with JavaScript rendering support"
id: firecrawl-001-2024
installation_priority: 1
item_type: mcp_server
name: Firecrawl Web Scraping MCP Server
priority: 1st_priority
production_readiness: 94
quality_score: 9.3
repository_url: https://github.com/mendableai/firecrawl-mcp
source_database: tools_services
status: active
tags:
- Tier 1
- MCP Server
- Web Scraping
- Data Extraction
- Content Processing
- API Service
- Developer Tool
- Official Integration
---

## 📋 Basic Information

**Firecrawl Web Scraping MCP Server** - Official Firecrawl integration providing powerful web scraping capabilities with JavaScript rendering, automatic content extraction, and LLM-optimized output formatting.

## Quality & Scoring Metrics

### Business-Aligned Scoring Analysis

**Business Domain Relevance**: 9/10 - Essential for web data extraction and content processing
**Technical Development Value**: 10/10 - Critical for data collection and web automation  
**Production Readiness**: 9/10 - Production-ready with cloud infrastructure
**Setup Complexity**: 7/10 - Simple API setup with advanced configuration options
**Maintenance Status**: 10/10 - Actively maintained by Mendable team
**Documentation Quality**: 9/10 - Comprehensive docs with tutorials

**Composite Score: 9.3/10** - Tier 1 Implementation Priority

## Technical Specifications

### Core Capabilities
- **JavaScript Rendering**: Full browser rendering for dynamic content
- **Automatic Extraction**: Smart content extraction without selectors
- **Markdown Conversion**: Clean markdown output for LLM consumption
- **Batch Crawling**: Crawl entire websites systematically
- **Map Function**: Discover all URLs on a website
- **Screenshot Capture**: Visual page capture capabilities

### Advanced Features
- **Custom Headers**: Support for authentication and custom headers
- **Rate Limiting**: Intelligent rate limiting to avoid blocking
- **Proxy Support**: Built-in proxy rotation capabilities
- **Content Filtering**: Remove ads, popups, and irrelevant content
- **Structured Data**: Extract JSON-LD and microdata

## Setup & Configuration

### Installation Methods

#### Method 1: Docker MCP Toolkit (Recommended)
```bash
# Pull and run the MCP server
docker pull firecrawl/mcp-server:latest
docker run -d --name firecrawl-mcp \
  -e FIRECRAWL_API_KEY=${FIRECRAWL_API_KEY} \
  -p 3000:3000 \
  firecrawl/mcp-server:latest
```

#### Method 2: Direct Installation
```bash
# Install via pnpm
pnpm install -g @firecrawl/mcp-server

# Configure API key
export FIRECRAWL_API_KEY="your_api_key_here"

# Start the server
firecrawl-mcp-server --port 3000
```

### Configuration
```json
{
  "firecrawl": {
    "api_key": "${FIRECRAWL_API_KEY}",
    "default_options": {
      "wait_for_selector": null,
      "screenshot": false,
      "include_html": false,
      "only_main_content": true,
      "remove_scripts": true,
      "wait_time": 0,
      "timeout": 30000
    },
    "crawl_options": {
      "max_depth": 3,
      "limit": 100,
      "allow_backward_links": false,
      "same_domain_only": true
    }
  }
}
```

## Use Cases

### Primary Applications
- **Content Aggregation**: Collect content from multiple sources
- **Market Research**: Extract competitor data and pricing
- **Documentation Scraping**: Convert web docs to structured data
- **News Monitoring**: Real-time news and article extraction
- **E-commerce Data**: Product information and pricing extraction

### Integration Example
```javascript
// Example: Scrape and structure web content
const pageData = await firecrawlMCP.scrape({
  url: "https://example.com/article",
  formats: ["markdown", "html", "screenshot"],
  only_main_content: true,
  wait_for_selector: ".content-loaded"
});

// Crawl entire website
const crawlData = await firecrawlMCP.crawl({
  url: "https://docs.example.com",
  max_depth: 2,
  limit: 50,
  include_paths: ["/api/*", "/guides/*"],
  exclude_paths: ["/blog/*"]
});

// Map all URLs on a site
const siteMap = await firecrawlMCP.map({
  url: "https://example.com",
  search: "pricing",
  limit: 100
});
```

## Business Value

### Key Benefits
- Eliminates complex scraping infrastructure needs
- JavaScript rendering handles modern web apps
- Clean, structured output ready for AI processing
- Automatic handling of anti-scraping measures
- Scale to millions of pages with cloud infrastructure

### ROI Metrics
- 90% reduction in scraping development time
- 95% success rate on JavaScript-heavy sites
- 80% cost reduction vs custom scraping solutions
- Process 100,000+ pages per day