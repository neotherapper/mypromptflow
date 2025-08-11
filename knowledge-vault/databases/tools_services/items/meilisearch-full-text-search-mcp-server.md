---
description: "Lightning-fast full-text search engine server with typo tolerance, faceted search, and instant results for AI-powered search applications"
id: meilisearch-001-2024
installation_priority: 2
item_type: mcp_server
name: Meilisearch Full-Text Search MCP Server
priority: 1st_priority
production_readiness: 94
quality_score: 9.0
repository_url: https://github.com/meilisearch/meilisearch-mcp
source_database: tools_services
status: active
tags:
- Tier 1
- MCP Server
- Search Engine
- Database Service
- Full-Text Search
- Developer Tool
- API Service
---

## 📋 Basic Information

**Meilisearch Full-Text Search MCP Server** - Ultra-fast, typo-tolerant search engine providing instant search results with built-in relevance and filtering capabilities for AI applications.

## Quality & Scoring Metrics

### Business-Aligned Scoring Analysis

**Business Domain Relevance**: 9/10 - Critical for search-powered applications
**Technical Development Value**: 9/10 - Essential for user-facing search features  
**Production Readiness**: 9/10 - Production-ready with cloud offerings
**Setup Complexity**: 8/10 - Simple deployment with instant results
**Maintenance Status**: 10/10 - Very active development
**Documentation Quality**: 9/10 - Excellent documentation with SDKs

**Composite Score: 9.0/10** - Tier 1 Implementation Priority

## Technical Specifications

### Core Capabilities
- **Typo Tolerance**: Handles misspellings and typos automatically
- **Instant Search**: Sub-50ms search responses
- **Faceted Search**: Dynamic filtering and categorization
- **Multi-Language**: Supports all languages including CJK
- **Synonyms**: Configure custom synonyms for better results
- **Geo Search**: Location-based search capabilities

### Advanced Features
- **AI Semantic Search**: Vector search with embedding support
- **Multi-Tenancy**: Isolated indexes for different tenants
- **Stop Words**: Automatic language-specific stop word handling
- **Ranking Rules**: Customizable relevance algorithms
- **Snapshots**: Backup and restore capabilities

## Setup & Configuration

### Installation Methods

#### Method 1: Docker MCP Toolkit (Recommended)
```bash
# Pull and run the MCP server
docker pull getmeili/meilisearch:latest
docker run -d --name meilisearch-mcp \
  -e MEILI_MASTER_KEY=${MEILI_MASTER_KEY} \
  -p 7700:7700 \
  -v $(pwd)/meili_data:/meili_data \
  getmeili/meilisearch:latest
```

#### Method 2: Direct Installation
```bash
# Install via pnpm
pnpm install -g @meilisearch/mcp-server

# Configure master key
export MEILI_MASTER_KEY="your_master_key_here"

# Start the server
meilisearch-mcp-server --db-path ./data.ms
```

### Configuration
```json
{
  "meilisearch": {
    "host": "http://localhost:7700",
    "api_key": "${MEILI_MASTER_KEY}",
    "indexes": {
      "products": {
        "primary_key": "id",
        "searchable_attributes": ["title", "description", "category"],
        "filterable_attributes": ["price", "brand", "in_stock"],
        "sortable_attributes": ["price", "rating"],
        "ranking_rules": [
          "words",
          "typo",
          "proximity",
          "attribute",
          "sort",
          "exactness"
        ]
      }
    }
  }
}
```

## Use Cases

### Primary Applications
- **E-commerce Search**: Product search with filters and facets
- **Documentation Search**: Instant documentation and knowledge base search
- **User Search**: Fast user and profile searching
- **Content Discovery**: Media and content recommendation
- **Autocomplete**: Real-time search suggestions

### Integration Example
```javascript
// Example: Intelligent search with AI
const searchResults = await meilisearchMCP.search({
  index: 'products',
  query: 'blue running shoes',
  filter: 'price < 100 AND in_stock = true',
  facets: ['brand', 'size', 'color'],
  limit: 20
});

// Semantic search with embeddings
const embedding = await generateEmbedding('comfortable shoes');
const semanticResults = await meilisearchMCP.vectorSearch({
  index: 'products',
  vector: embedding,
  hybrid: {
    query: 'running shoes',
    semanticRatio: 0.7
  }
});

// Update search analytics
await meilisearchMCP.updateAnalytics({
  query: searchResults.query,
  position: clickedPosition,
  conversion: true
});
```

## Business Value

### Key Benefits
- 10x faster than Elasticsearch for most use cases
- Zero configuration instant search
- 95% smaller resource footprint
- Built-in typo tolerance improves user experience
- Real-time indexing with immediate availability

### ROI Metrics
- 300ms → 30ms search latency improvement
- 80% reduction in infrastructure costs
- 40% increase in search conversion rates
- 90% reduction in search implementation time