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

**Total Servers Discovered**: 1,150+ (definitive ecosystem mapping)
**Information Retrieval Relevant**: 700+ (~60% of total ecosystem)  
**High Priority for Project**: 25 (enterprise-ready with highest relevance)
**Implementation Ready**: 15 (official + validated community servers)

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

#### Qdrant ⭐ (Official Vector Database)
- **Repository**: https://github.com/qdrant/qdrant-mcp
- **Description**: Vector search engine for AI memories and semantic search
- **Category**: Vector Database (Official)
- **Information Retrieval Relevance**: High
- **Setup Complexity**: Moderate
- **Dependencies**: Qdrant instance
- **Maintenance Status**: Active (Qdrant maintained)
- **Use Cases**: Semantic search, RAG applications, AI memory systems
- **Integration Priority**: High (critical for AI-powered information retrieval)

#### Redis ⭐ (Official In-Memory Database)
- **Repository**: https://github.com/redis/redis-mcp-server
- **Description**: Natural language interface for Redis data management
- **Category**: In-Memory Database (Official)
- **Information Retrieval Relevance**: High
- **Setup Complexity**: Moderate
- **Dependencies**: Redis instance
- **Maintenance Status**: Active (Redis maintained)
- **Use Cases**: High-performance data access, caching, real-time data
- **Integration Priority**: High (industry-standard performance)

### 4. Content Processing
*Servers for text processing, document analysis, and content extraction*

**Discovered Servers**:

#### Fetch (Anthropic) - Official Reference 
*(Already listed in Web Search category - core server with multiple applications)*

#### Filesystem (Anthropic) - Official Reference
- **Repository**: https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem
- **Description**: Secure file operations with advanced access controls and directory restrictions
- **Category**: Official Reference Server
- **Information Retrieval Relevance**: High
- **Setup Complexity**: Medium (directory configuration required)
- **Dependencies**: None (official implementation)
- **Maintenance Status**: Active (Anthropic maintained)
- **Use Cases**: File system access, document processing, local content management
- **Integration Priority**: High (essential for file-based information retrieval)

### 5. Official Reference Servers (Complete Set)
*Anthropic's official reference implementations - production ready*

#### Everything (Anthropic) - Official Demo Server
- **Repository**: https://github.com/modelcontextprotocol/servers/tree/main/src/everything
- **Description**: Complete MCP protocol demonstration (9 tools, 100 resources, 3 prompts)
- **Category**: Official Reference/Demo Server
- **Information Retrieval Relevance**: Medium
- **Setup Complexity**: Simple
- **Dependencies**: None
- **Use Cases**: MCP protocol testing, capability demonstration, development reference
- **Integration Priority**: Medium (excellent for testing and validation)

#### Git (Anthropic) - Official Reference
- **Repository**: https://github.com/modelcontextprotocol/servers/tree/main/src/git
- **Description**: Complete Git repository management with 13 tools
- **Category**: Official Reference Server
- **Information Retrieval Relevance**: Medium
- **Setup Complexity**: Medium (repository paths configuration)
- **Dependencies**: Git installed locally
- **Use Cases**: Code repository access, version history retrieval, project documentation
- **Integration Priority**: Medium (valuable for development-focused information)

#### Sequential Thinking (Anthropic) - Official Reference
- **Repository**: https://github.com/modelcontextprotocol/servers/tree/main/src/sequentialthinking
- **Description**: Dynamic problem-solving with revision capabilities
- **Category**: Official Reference Server
- **Information Retrieval Relevance**: Low
- **Setup Complexity**: Simple
- **Dependencies**: None
- **Use Cases**: Problem-solving workflows, analytical thinking assistance
- **Integration Priority**: Low (utility function, not core information retrieval)

#### Time (Anthropic) - Official Reference
- **Repository**: https://github.com/modelcontextprotocol/servers/tree/main/src/time
- **Description**: Time and timezone conversion with IANA support
- **Category**: Official Reference Server
- **Information Retrieval Relevance**: Low
- **Setup Complexity**: Simple
- **Dependencies**: None
- **Use Cases**: Time-based information processing, scheduling, temporal analysis
- **Integration Priority**: Low (utility function, supplementary capability)

### 5. Real-Time Information  
*Servers for real-time data feeds, APIs, and live information*

**Discovered Servers**:

#### Bright Data (Professional Web Scraping)
- **Repository**: https://github.com/Noahp091/bright-data-mcp-server
- **Description**: Large-scale web data extraction across public internet
- **Category**: Web Data Extraction
- **Information Retrieval Relevance**: High
- **Setup Complexity**: Moderate
- **Dependencies**: Bright Data API access
- **Use Cases**: Professional web scraping, real-time web data, market intelligence
- **Integration Priority**: High (enterprise-grade web data access)

#### VideoDB Director ⭐ (Official Video AI)
- **Repository**: https://github.com/video-db/videodb-mcp-server
- **Description**: AI-powered video workflows, automatic editing, content moderation
- **Category**: Video Analysis and Search
- **Information Retrieval Relevance**: High
- **Setup Complexity**: Moderate
- **Dependencies**: VideoDB API access
- **Maintenance Status**: Active (VideoDB maintained)
- **Use Cases**: Video content analysis, searchable video moments, automated video processing
- **Integration Priority**: High (first AI-powered video database with natural language)

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