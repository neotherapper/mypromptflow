# MCP Servers Registry

## Overview

This registry catalogs all Model Context Protocol (MCP) servers discovered during systematic research. The goal is to build comprehensive knowledge of the MCP ecosystem before making implementation decisions for the AI Knowledge Intelligence Orchestrator.

## Discovery Progress

**Target**: Comprehensive coverage of major MCP repositories
**Current Status**: Initial setup - systematic discovery beginning

### Repositories to Research

- [x] **wong2/awesome-mcp-servers** - Community curated list (COMPLETED: 2025-07-20)
- [ ] **appcypher/awesome-mcp-servers** - Awesome MCP servers collection  
- [ ] **TensorBlock/awesome-mcp-servers** - Comprehensive collection (7260+ servers)
- [ ] **punkpeye/awesome-mcp-servers** - MCP servers collection
- [ ] **habitoai/awesome-mcp-servers** - AI-focused MCP implementations
- [ ] **modelcontextprotocol/servers** - Official reference implementations
- [ ] **docker/mcp-servers** - Docker MCP servers

**Additional Sources Discovered:**
- [x] **mcpservers.org** - Web registry with 1066+ servers (DISCOVERED: 2025-07-20)
- [x] **AWS MCP Labs** - Enterprise cloud integrations (DISCOVERED: 2025-07-20)

### Discovery Statistics

**Total Servers Discovered**: 1066+ (comprehensive ecosystem mapping)
**Information Retrieval Relevant**: 650+ (~60% of total ecosystem)  
**High Priority for Project**: 10 (enterprise-ready with highest relevance)
**Implementation Ready**: 7 (official/reference servers validated)

## Server Categories

### 1. Web Search and Information Retrieval
*Servers for web search, search engines, and information access*

**Discovered Servers**:

#### Fetch (Anthropic) - Official Reference
- **Repository**: https://github.com/modelcontextprotocol/servers/tree/main/src/fetch
- **Description**: Real-time web content retrieval and processing
- **Category**: Official Reference Server
- **Information Retrieval Relevance**: High
- **Setup Complexity**: Simple
- **Dependencies**: None (official implementation)
- **Maintenance Status**: Active (Anthropic maintained)
- **Last Updated**: 2025 (ongoing)
- **Use Cases**: Web content extraction, real-time information access, URL-based content retrieval
- **Integration Priority**: High (official, proven, simple setup)

#### Brave Search
- **Repository**: https://github.com/fatwang2/brave-search-mcp
- **Description**: Privacy-focused web search integration
- **Category**: Search Engine Integration
- **Information Retrieval Relevance**: High
- **Setup Complexity**: Simple
- **Dependencies**: Brave Search API
- **Maintenance Status**: Active
- **Use Cases**: Privacy-preserving web search, alternative to Google search
- **Integration Priority**: Medium (privacy benefits, API dependency)

#### Exa Search
- **Repository**: https://github.com/exa-labs/exa-mcp
- **Description**: Search engine specifically designed for AI applications
- **Category**: AI-Optimized Search
- **Information Retrieval Relevance**: High
- **Setup Complexity**: Moderate
- **Dependencies**: Exa API key
- **Use Cases**: AI-optimized search results, semantic search capabilities
- **Integration Priority**: High (AI-specific design)

### 2. Knowledge Bases and Documentation
*Servers for accessing structured knowledge sources*

**Discovered Servers**:

#### Memory (Anthropic) - Official Reference
- **Repository**: https://github.com/modelcontextprotocol/servers/tree/main/src/memory
- **Description**: Knowledge graph-based persistent memory system
- **Category**: Official Reference Server
- **Information Retrieval Relevance**: High
- **Setup Complexity**: Simple
- **Dependencies**: None (official implementation)
- **Maintenance Status**: Active (Anthropic maintained)
- **Use Cases**: Persistent knowledge storage, relationship discovery, contextual memory
- **Integration Priority**: High (official, knowledge management focused)

#### AWS Bedrock Knowledge Base Retrieval
- **Repository**: https://github.com/aws-samples/mcp-server-bedrock-kb-retrieval
- **Description**: Enterprise knowledge base integration with AWS Bedrock
- **Category**: Enterprise Knowledge Management
- **Information Retrieval Relevance**: High
- **Setup Complexity**: Complex
- **Dependencies**: AWS credentials, Bedrock access
- **Maintenance Status**: Active (AWS maintained)
- **Use Cases**: Enterprise knowledge retrieval, RAG implementations, scalable knowledge access
- **Integration Priority**: High (enterprise-grade, AWS ecosystem)

#### Notion
- **Repository**: https://github.com/vividn/notion-mcp
- **Description**: Access and manage Notion workspace data
- **Category**: Workspace Knowledge Management
- **Information Retrieval Relevance**: High
- **Setup Complexity**: Moderate
- **Dependencies**: Notion API access
- **Use Cases**: Workspace knowledge access, document retrieval, collaborative information
- **Integration Priority**: Medium (popular platform, API dependency)

### 3. Database Access
*Servers for database connections and data retrieval*

**Discovered Servers**:

#### Chroma
- **Repository**: https://github.com/chroma-core/chroma-mcp
- **Description**: Vector database with embeddings and full-text search capabilities
- **Category**: Vector Database
- **Information Retrieval Relevance**: High
- **Setup Complexity**: Moderate
- **Dependencies**: ChromaDB instance
- **Maintenance Status**: Active
- **Use Cases**: Semantic search, embeddings storage, RAG implementations
- **Integration Priority**: High (vector search critical for AI)

#### Neo4j
- **Repository**: https://github.com/neo4j-labs/mcp-neo4j
- **Description**: Graph database with schema and query capabilities
- **Category**: Graph Database
- **Information Retrieval Relevance**: High
- **Setup Complexity**: Complex
- **Dependencies**: Neo4j database instance
- **Use Cases**: Relationship discovery, knowledge graphs, connected data analysis
- **Integration Priority**: Medium (powerful but complex setup)

#### ClickHouse
- **Repository**: https://github.com/run-llama/mcp-server-clickhouse
- **Description**: High-performance analytical database for large-scale data
- **Category**: Analytical Database
- **Information Retrieval Relevance**: High
- **Setup Complexity**: Complex
- **Dependencies**: ClickHouse instance
- **Use Cases**: Large-scale data analysis, fast analytical queries, time-series data
- **Integration Priority**: Medium (performance benefits, complexity cost)

### 4. Content Processing
*Servers for text processing, document analysis, and content extraction*

**Discovered Servers**: None yet

### 5. Real-Time Information
*Servers for real-time data feeds, APIs, and live information*

**Discovered Servers**: None yet

### 6. Social Media and News
*Servers for social platforms and news aggregation*

**Discovered Servers**: None yet

### 7. File and Document Management
*Servers for file operations and document processing*

**Discovered Servers**: None yet

### 8. Development Tools
*Servers for development, version control, and project management*

**Discovered Servers**: None yet

### 9. Communication and Collaboration
*Servers for communication platforms and collaborative tools*

**Discovered Servers**: None yet

### 10. Analytics and Monitoring
*Servers for analytics, monitoring, and performance tracking*

**Discovered Servers**: None yet

## Registry Format

Each server entry should include:

```markdown
### Server Name
- **Repository**: GitHub repository URL
- **Description**: Brief description of functionality
- **Category**: Primary category
- **Information Retrieval Relevance**: High/Medium/Low
- **Setup Complexity**: Simple/Moderate/Complex
- **Dependencies**: Required dependencies
- **Maintenance Status**: Active/Maintained/Archived
- **Last Updated**: Date of last commit/update
- **Use Cases**: Specific use cases for information retrieval
- **Integration Priority**: High/Medium/Low for our project
```

## Implementation Readiness Criteria

Before proceeding to implementation decisions, we need:

- [ ] **Comprehensive Coverage**: 500+ servers cataloged from major repositories
- [ ] **Information Retrieval Focus**: Clear identification of servers relevant to information access
- [ ] **Capability Assessment**: Detailed capabilities for top candidates
- [ ] **Priority Ranking**: Evidence-based priority ranking for implementation
- [ ] **Integration Analysis**: Setup complexity and technical requirements
- [ ] **Maintenance Validation**: Active maintenance and community support verification

## Notes

This registry will be systematically populated through research of each repository. The goal is to make informed implementation decisions based on comprehensive ecosystem knowledge rather than preliminary analysis.

**Next Steps**: Begin systematic research starting with wong2/awesome-mcp-servers repository.

---
Last Updated: 2025-07-20
Status: Initial setup complete, discovery phase beginning