---
description: "Production-ready RAG platform providing instant search and retrieval from documents with built-in vector search, document processing, and knowledge base management"
id: needle-001-2024
installation_priority: 1
item_type: mcp_server
name: Needle RAG Search MCP Server
priority: 1st_priority
production_readiness: 93
quality_score: 9.1
repository_url: https://github.com/needle-ai/needle-mcp
source_database: tools_services
status: active
tags:
- Tier 1
- MCP Server
- RAG Platform
- Search Engine
- Document Processing
- Vector Search
- Knowledge Management
- Official Integration
---

## 📋 Basic Information

**Needle RAG Search MCP Server** - Official Needle integration providing production-ready RAG capabilities with instant document search, retrieval, and knowledge base management out of the box.

## Quality & Scoring Metrics

### Business-Aligned Scoring Analysis

**Business Domain Relevance**: 9/10 - Essential for knowledge-driven AI applications
**Technical Development Value**: 9/10 - Complete RAG solution without setup  
**Production Readiness**: 9/10 - Production-ready with enterprise features
**Setup Complexity**: 9/10 - Zero configuration required
**Maintenance Status**: 9/10 - Actively maintained by Needle team
**Documentation Quality**: 9/10 - Excellent documentation

**Composite Score: 9.1/10** - Tier 1 Implementation Priority

## Technical Specifications

### Core Capabilities
- **Document Ingestion**: Automatic processing of PDFs, docs, text
- **Vector Search**: Built-in embeddings and similarity search
- **Hybrid Search**: Combine keyword and semantic search
- **Knowledge Bases**: Organize documents into collections
- **Citation Tracking**: Source attribution for retrieved content
- **Real-time Indexing**: Instant document availability

### Advanced Features
- **Multi-Modal Support**: Text, images, tables processing
- **Custom Embeddings**: Support for various embedding models
- **Access Control**: Document-level permissions
- **Version Control**: Track document versions
- **Analytics**: Search and retrieval analytics
- **API Integration**: RESTful API for all operations

## Setup & Configuration

### Installation Methods

#### Method 1: Docker MCP Toolkit (Recommended)
```bash
# Pull and run the MCP server
docker pull needle/mcp-server:latest
docker run -d --name needle-mcp \
  -e NEEDLE_API_KEY=${NEEDLE_API_KEY} \
  -p 3000:3000 \
  -v $(pwd)/documents:/documents \
  needle/mcp-server:latest
```

#### Method 2: Direct Installation
```bash
# Install via pnpm
pnpm install -g @needle-ai/mcp-server

# Configure API key
export NEEDLE_API_KEY="your_api_key_here"

# Start the server
needle-mcp-server --port 3000
```

### Configuration
```json
{
  "needle": {
    "api_key": "${NEEDLE_API_KEY}",
    "collection_id": "${NEEDLE_COLLECTION_ID}",
    "search_options": {
      "hybrid_search": true,
      "rerank": true,
      "max_results": 10,
      "min_relevance": 0.7
    },
    "ingestion": {
      "auto_process": true,
      "chunk_size": 512,
      "chunk_overlap": 128,
      "extract_metadata": true
    },
    "embeddings": {
      "model": "text-embedding-3-small",
      "dimensions": 1536
    }
  }
}
```

## Use Cases

### Primary Applications
- **RAG Applications**: Power AI with document knowledge
- **Knowledge Base Search**: Enterprise document search
- **Customer Support**: Instant answers from documentation
- **Research Assistant**: Academic and research applications
- **Compliance Search**: Find relevant policies and regulations

### Integration Example
```javascript
// Example: RAG operations with Needle
const collection = await needleMCP.createCollection({
  name: "product-docs",
  description: "Product documentation"
});

// Ingest documents
await needleMCP.ingestDocuments({
  collection_id: collection.id,
  documents: [
    { path: "/docs/user-guide.pdf" },
    { path: "/docs/api-reference.md" }
  ]
});

// Search with RAG
const results = await needleMCP.search({
  collection_id: collection.id,
  query: "How to configure authentication?",
  hybrid: true,
  include_citations: true
});

// Get document chunks with context
const context = await needleMCP.getContext({
  query: "authentication setup",
  collection_id: collection.id,
  context_window: 3,
  max_tokens: 2000
});

// Update document
await needleMCP.updateDocument({
  document_id: "doc-123",
  content: "Updated content",
  metadata: { version: "2.0" }
});
```

## Business Value

### Key Benefits
- Zero-setup RAG implementation
- Instant document search and retrieval
- Built-in citation tracking for compliance
- Scale to millions of documents
- Production-ready from day one

### ROI Metrics
- 90% reduction in RAG setup time
- Sub-second search latency
- 95% accuracy in retrieval
- Handle 100GB+ document collections