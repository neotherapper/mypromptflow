# Information Access Framework for AI Agents

## Overview

This framework provides AI agents with centralized guidance for accessing information from various sources. It bridges the comprehensive MCP server infrastructure in knowledge-vault with practical decision logic for information retrieval.

## 🎯 Quick Start for AI Agents

### 1. Identify Information Need
Determine what type of information you need:
- **Web Content**: Real-time web data, HTML content, public APIs
- **Version Control**: Repository files, commit history, code analysis  
- **Database Access**: Structured data, SQL queries, real-time database connections
- **File Systems**: Local files, document processing, file operations
- **Real-time Data**: Live feeds, streaming data, event-driven systems
- **Structured Data**: APIs, JSON/XML processing, data transformation

### 2. Query Available Sources
Use knowledge-vault views to find appropriate sources:

```yaml
# Query by information type
@knowledge-vault/tools_services view:information-sources-by-type
filter: information_type:web_content

# Query by complexity requirements  
@knowledge-vault/tools_services view:authentication-required
filter: complexity_score:<=3

# Query for real-time capabilities
@knowledge-vault/tools_services view:real-time-sources
filter: performance_tier:low_latency
```

### 3. Apply Decision Logic
Use the decision framework to select the best source:
- **Priority**: Highest rated sources first
- **Complexity**: Match setup complexity to timeline constraints
- **Authentication**: Consider authentication requirements
- **Rate Limits**: Assess usage restrictions

### 4. Execute Information Retrieval
Implement using selected mechanism:
- **MCP Tools**: Primary method (e.g., `mcp__MCP_DOCKER__get_file_contents`)
- **Direct APIs**: Fallback method (WebFetch with API endpoints)
- **File Operations**: Local access (Read/Write tools)
- **Web Access**: Web scraping (WebFetch/WebSearch tools)

## 📊 Information Source Categories

### Web Content Sources
**Use Cases**: Real-time web monitoring, content extraction, public API access  
**Examples**: Fetch MCP Server, Bright Data, Browser Automation  
**Access Methods**: Real-time, on-demand, streaming  
**Authentication**: Usually none for public content  

### Version Control Sources  
**Use Cases**: Repository analysis, code access, change tracking  
**Examples**: GitHub, GitLab, Git MCP Server  
**Access Methods**: Real-time, batch, webhook  
**Authentication**: Required (tokens, OAuth)  

### Database Access Sources
**Use Cases**: Structured data queries, business data access  
**Examples**: PostgreSQL, MySQL, MongoDB, Redis, Qdrant  
**Access Methods**: Real-time, batch, streaming  
**Authentication**: Required (credentials, connection strings)  

### File System Sources
**Use Cases**: Document processing, local file access  
**Examples**: Filesystem MCP Server, Document processors  
**Access Methods**: On-demand, batch  
**Authentication**: File system permissions  

### Real-time Data Sources
**Use Cases**: Live monitoring, streaming data, event processing  
**Examples**: Redis Streams, Kafka, WebSocket APIs  
**Access Methods**: Streaming, real-time, event-driven  
**Authentication**: Varies by source  

### Structured Data Sources  
**Use Cases**: API integration, data transformation  
**Examples**: REST APIs, GraphQL, JSON processors  
**Access Methods**: Real-time, batch, on-demand  
**Authentication**: API keys, OAuth  

## 🔍 Source Selection Decision Tree

### For GitHub Repository Information:
1. **Query**: `@knowledge-vault/tools_services tag:version-control tag:github`
2. **Primary**: GitHub MCP Server → `mcp__MCP_DOCKER__get_file_contents`
3. **Fallback**: Direct GitHub API → `WebFetch github.com/api`
4. **Local**: Git operations → `Bash git` commands

### For Real-time Web Data:
1. **Query**: `@knowledge-vault/tools_services tag:web-content tag:real-time-data`
2. **Options**: Fetch MCP Server, Bright Data, Browser automation
3. **Selection**: By complexity_score and rate_limits
4. **Implementation**: Start with lowest complexity, highest reliability

### For Database Information:
1. **Query**: `@knowledge-vault/tools_services tag:database-access`
2. **Filter**: By database type (PostgreSQL, MySQL, NoSQL)
3. **Consider**: Authentication requirements, performance needs
4. **Implement**: MCP server if available, direct connection as fallback

### For Document Processing:
1. **Query**: `@knowledge-vault/tools_services tag:file-systems`
2. **Options**: Filesystem MCP Server, document processors
3. **Consider**: File types, processing requirements
4. **Access**: Local files via Read tool, remote via appropriate MCP server

## 🛠️ Available Tools and Mechanisms

### Primary: MCP Tools (Recommended)
- **Advantage**: Standardized interface, comprehensive functionality
- **Access Pattern**: `mcp__MCP_DOCKER__[tool_name]`
- **Examples**: `get_file_contents`, `post_database_query`, `fetch_content`
- **Status**: Active with Docker MCP integration

### Secondary: Direct APIs
- **Use When**: MCP server unavailable or insufficient
- **Access Pattern**: WebFetch with API endpoints
- **Examples**: `WebFetch("https://api.github.com/...", "extract data")`
- **Considerations**: Rate limits, authentication, error handling

### Tertiary: Built-in Tools
- **File Access**: Read, Write tools for local files
- **Web Access**: WebFetch, WebSearch for web content
- **System Access**: Bash tool for system operations
- **Use Cases**: Simple operations, fallback scenarios

### Integration Patterns
- **Single Source**: Direct access to one information source
- **Multi-Source**: Aggregate data from multiple sources
- **Fallback Chain**: Primary → Secondary → Tertiary approaches
- **Parallel Access**: Concurrent queries for speed and redundancy

## 📋 Implementation Checklist

### Before Information Retrieval
- [ ] Identify specific information requirements
- [ ] Query knowledge-vault views for available sources
- [ ] Check authentication and rate limit requirements
- [ ] Plan fallback strategies for source failures
- [ ] Estimate setup complexity vs. timeline

### During Implementation
- [ ] Start with highest-rated, lowest-complexity source
- [ ] Implement proper error handling and retries
- [ ] Respect rate limits and authentication requirements
- [ ] Log access patterns for future optimization
- [ ] Test with representative data samples

### After Implementation
- [ ] Validate information quality and completeness
- [ ] Document successful access patterns
- [ ] Update knowledge-vault with usage experiences
- [ ] Plan maintenance and monitoring procedures
- [ ] Consider caching strategies for frequently accessed data

## 🔗 Related Resources

### Knowledge-Vault Integration
- **Source Catalog**: `@knowledge-vault/tools_services` database
- **Views**: `information-sources-by-type.yaml`, `real-time-sources.yaml`, `authentication-required.yaml`
- **Server Profiles**: Detailed implementation guides in `tools_services/items/`

### Framework Components
- **Decision Framework**: `agent-decision-framework.md` - Logic for source selection
- **Mechanisms Guide**: `retrieval-mechanisms.yaml` - How to access sources
- **Integration Examples**: `integration-examples.md` - Practical usage patterns

### System Integration
- **Research Framework**: Integrated with `@research/orchestrator/integration/`
<<<<<<< HEAD
- **Project Workflows**: Referenced in `@projects/universal-topic-intelligence-system/`
=======
- **Project Workflows**: Referenced in `@projects/ai-knowledge-intelligence-orchestrator/`
>>>>>>> origin/master
- **MCP Learning**: Error patterns and troubleshooting in `@meta/mcp-learning/`

## 🚀 Advanced Usage Patterns

### Technology-Specific Routing (React Example)
When working with React development:
```yaml
detection:
  files: ["src/components/Button.tsx", "package.json with react dependency"]
  confidence: 0.87
  mapping: "meta/information-access/topic-mappings/react-sources.yaml"
source_selection:
  primary: "GitHub MCP Server - React repositories (facebook/react, vercel/next.js)"
  supplementary: "Context7 MCP Server - React documentation (/facebook/react)"
  validation: "npm registry - React ecosystem packages"
integration:
  ai_pr_validation: "typescript-frontend-validator uses React-specific patterns"
  research_framework: "React research automatically uses optimized sources"
  knowledge_context: "REQUEST_CONTEXT(react-frontend-dev)"
```

### Categorical Routing (Database Example)
When database technology is unclear:
```yaml
detection:
  files: ["schema.sql", "migrations/001_create_users.sql"]
  confidence: 0.72
  mapping: "meta/information-access/category-mappings/database-sources.yaml"
source_selection:
  primary: "PostgreSQL MCP Server - default SQL operations"
  supplementary: "Knowledge vault query - database-access tagged items"
  validation: "MongoDB MCP - NoSQL alternative assessment"
integration:
  research_framework: "Step 3.5 source discovery with database category routing"
  validation_framework: "Database source accessibility validation"
  fallback_logic: "Knowledge vault → WebFetch documentation"
```

### Multi-System Coordination
For complex information needs spanning multiple systems:
```yaml
scenario: "React performance optimization research with validation"
detection:
  topic: "React performance optimization"
  complexity: "moderate"
  specific_technology: "React (confidence: 0.89)"
source_coordination:
  react_specific: "GitHub (React repos), Context7 (React docs), npm (performance packages)"
  performance_category: "Knowledge vault performance-tagged MCP servers"
  validation: "WebFetch React official documentation"
system_integration:
  research_orchestrator: "Step 3.5 discovers React-specific sources"
  ai_pr_validation: "Performance validator enhanced with React patterns"
  source_tracking: "research-sources.md includes source selection rationale"
```

## 📊 Performance Optimization

### Source Selection Optimization
- **Cache Frequently Used**: Keep common source configurations
- **Monitor Performance**: Track response times and reliability
- **Update Preferences**: Based on success rates and efficiency
- **Load Balance**: Distribute requests across multiple sources

### Access Pattern Optimization
- **Batch Operations**: Group related information requests
- **Parallel Processing**: Concurrent access when possible
- **Incremental Updates**: Only fetch changed information
- **Smart Caching**: Cache based on data freshness requirements

## 🛡️ Security and Compliance

### Authentication Management
- **Secure Storage**: Use environment variables for credentials
- **Credential Rotation**: Regular token and key updates
- **Access Monitoring**: Log and monitor information access
- **Principle of Least Privilege**: Minimum required permissions

### Data Handling
- **Privacy Compliance**: Respect data privacy requirements
- **Retention Policies**: Appropriate data retention and cleanup
- **Audit Trails**: Comprehensive access logging
- **Error Security**: Fail securely without exposing credentials

---

**Framework Version**: 1.0.0  
<<<<<<< HEAD
**Last Updated**: 2025-07-30  
**Maintained By**: Universal Topic Intelligence System Project
=======
**Last Updated**: 2025-07-27  
**Maintained By**: AI Knowledge Intelligence Orchestrator Project
>>>>>>> origin/master

This framework enables systematic, efficient, and secure information access for AI agents across the comprehensive MCP server infrastructure.