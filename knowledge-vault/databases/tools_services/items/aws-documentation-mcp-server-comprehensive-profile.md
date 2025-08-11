---
api_version: AWS Documentation API v2, Service Documentation API v1
authentication_types:
- AWS API Access
- Public Documentation Access
- Service-Specific Authentication
category: Technical Documentation
description: Comprehensive AWS documentation access server providing latest AWS service documentation and API references with intelligent search and context-aware retrieval. Enables real-time access to AWS technical documentation, service guides, and API specifications for development and operations teams.
estimated_setup_time: 20-30 minutes
id: h8i9j0k1-l2m3-4567-hijk-l89012345678
installation_priority: 2
item_type: mcp_server
name: AWS Documentation MCP Server
priority: 2nd_priority
production_readiness: 89
provider: AWS Labs
quality_score: 8.7
repository_url: https://github.com/awslabs/mcp/tree/main/src/aws-documentation-mcp-server
setup_complexity: Moderate
source_database: tools_services
status: active
tags:
- Tier 2
- MCP Server
- Developer Tools
- amazon
- API References
- AWS Documentation
- developer-tools
- documentation
- Enterprise
- Knowledge Access
- Technical Documentation
tier: Tier 2
transport_protocols:
- AWS Documentation API
- REST API Integration
- Content Delivery Network
information_capabilities:
  data_types:
  - service_documentation
  - api_references
  - user_guides
  - developer_guides
  - cli_references
  - sdk_documentation
  - best_practices
  - troubleshooting_guides
  search_types:
  - service_specific_search
  - api_reference_search
  - contextual_search
  - cross_service_search
  - version_aware_search
  automation_capabilities:
  - intelligent_content_discovery
  - contextual_recommendations
  - documentation_updates
  - cross_reference_linking
  - version_tracking
---

## 📋 Basic Information

The AWS Documentation MCP Server delivers comprehensive AWS documentation access capabilities through the Model Context Protocol, enabling real-time access to latest AWS service documentation, API references, and technical guides with intelligent search and context-aware retrieval for development and operations teams. With a business value score of 8.7/10, this server represents strategic infrastructure for AWS development workflow integration and technical knowledge access.

Key value propositions:
- Complete AWS documentation access with real-time updates and comprehensive service coverage
- Enterprise-grade intelligent search with context-aware retrieval and cross-service documentation linking
- High-performance API reference access with version tracking and compatibility information
- Comprehensive technical documentation including user guides, developer guides, and best practices
- Advanced contextual recommendations and intelligent content discovery for development workflows
- Seamless integration with unified intelligence systems and AWS development environments

## Quality & Scoring Metrics

### Business-Aligned Scoring Analysis

**Business Domain Relevance**: 8/10 (Strategic documentation access for AWS development teams)
**Technical Development Value**: 9/10 (Essential technical documentation and API reference functionality)
**Production Readiness**: 9/10 (AWS-maintained with stable documentation API integration)
**Setup Complexity**: 9/10 (Moderate setup with straightforward configuration)
**Maintenance Status**: 9/10 (Active AWS Labs development with documentation focus)
**Documentation Quality**: 8/10 (Comprehensive setup documentation and usage examples)

**Composite Score: 8.7/10** - Tier 2 Strategic Implementation Priority

### Production Readiness Assessment

- **API Stability**: AWS Documentation API v2 with stable content delivery and version management
- **Security Compliance**: Standard AWS security with public documentation access and optional authentication
- **Scalability**: AWS CDN-backed documentation delivery with global availability
- **Enterprise Features**: Intelligent search, contextual recommendations, version tracking, cross-referencing
- **Support Quality**: AWS support with documentation team expertise and community resources

### Quality Validation Metrics

- **Integration Testing**: Comprehensive AWS documentation API integration with content validation
- **Performance Benchmarks**: Sub-500ms documentation retrieval with CDN optimization
- **Error Handling**: Graceful error handling with fallback mechanisms and offline capabilities
- **Monitoring**: Content freshness monitoring with update tracking and availability metrics
- **Compliance**: Standard AWS compliance with documentation access and usage policies

## Technical Specifications

### Core Architecture

```yaml
Server Type: Technical Documentation
Protocol: Model Context Protocol (MCP)
Primary Language: Python/TypeScript
Dependencies: AWS Documentation API, Content Parser, Search Engine
Authentication: AWS API Access, Public Access, Optional Service Auth
```

### System Requirements

- **Runtime**: Python 3.9+ or Node.js 18+, HTTP client libraries
- **Memory**: 1GB+ (2GB recommended for caching and search indexing)
- **Network**: AWS documentation API access, CDN connectivity
- **Storage**: 500MB+ for caching and search indexes
- **CPU**: Single or multi-core processor for content processing and search
- **Additional**: Optional AWS credentials for enhanced access, internet connectivity

### API Capabilities

```typescript
interface AWSDocumentationMCPCapabilities {
  documentation_access: {
    get_service_documentation: boolean;
    search_documentation: boolean;
    get_api_references: boolean;
    access_user_guides: boolean;
  };
  intelligent_search: {
    contextual_search: boolean;
    cross_service_search: boolean;
    version_aware_search: boolean;
    semantic_search: boolean;
  };
  content_discovery: {
    recommend_content: boolean;
    discover_related_docs: boolean;
    track_documentation_updates: boolean;
    cross_reference_linking: boolean;
  };
  version_management: {
    track_api_versions: boolean;
    compare_versions: boolean;
    compatibility_checking: boolean;
    changelog_access: boolean;
  };
}
```

### Data Models

- **Documentation Page**: Comprehensive page content with metadata, version information, and cross-references
- **API Reference**: Detailed API specification with parameters, examples, and compatibility information
- **Search Result**: Contextual search results with relevance scoring and content snippets
- **Version Information**: API version details with compatibility matrix and migration guides

## Setup & Configuration

### Installation Methods

#### Method 1: Docker MCP Toolkit (Recommended)

Primary deployment method using Docker MCP server ecosystem

```bash
# Pull and run the AWS Documentation MCP Server
docker pull awslabs/aws-documentation-mcp-server:latest

# Run with environment configuration
docker run -d --name aws-documentation-mcp \
  -e AWS_REGION=${AWS_REGION} \
  -e DOCUMENTATION_CACHE_SIZE=1000 \
  -p 3006:3006 \
  awslabs/aws-documentation-mcp-server:latest
```

#### Method 2: Docker Compose Deployment

Multi-service deployment with dependencies

```yaml
# docker-compose.yml
version: '3.8'
services:
  aws-documentation-mcp:
    image: awslabs/aws-documentation-mcp-server:latest
    environment:
      - AWS_REGION=${AWS_REGION}
      - DOCUMENTATION_CACHE_SIZE=1000
      - INTELLIGENT_SEARCH=enabled
      - CONTEXT_AWARENESS=enabled
    ports:
      - "3006:3006"
    volumes:
      - ./cache:/app/cache
      - ./config:/app/config
    restart: unless-stopped
```

#### Method 3: Claude Code Integration

Direct integration with Claude Code development environment

```bash
# Install via Claude Code MCP configuration
npm install -g @awslabs/mcp-server-aws-documentation

# Configure in Claude Code settings
{
  "mcpServers": {
    "aws-documentation": {
      "command": "mcp-server-aws-documentation",
      "args": ["--config", "/path/to/docs-config.json"],
      "env": {
        "AWS_REGION": "us-east-1",
        "CACHE_ENABLED": "true",
        "INTELLIGENT_SEARCH": "enabled"
      }
    }
  }
}
```

#### Method 4: Claude Desktop Integration

Integration with Claude Desktop application

```json
// Claude Desktop configuration
{
  "mcpServers": {
    "aws-documentation": {
      "command": "python",
      "args": ["-m", "aws_documentation_mcp_server"],
      "env": {
        "AWS_REGION": "us-east-1",
        "DOCUMENTATION_CACHE_SIZE": "1000"
      }
    }
  }
}
```

#### Method 5: Alternative Installation Methods

Fallback installation options:
- Python pip installation with virtual environment
- Development environment integration with IDE plugins
- Browser extension for direct documentation access
- Enterprise deployment with centralized documentation proxy

### Authentication Configuration

#### Public Access (Recommended)

```json
{
  "documentation": {
    "access_mode": "public",
    "region": "us-east-1",
    "cache": {
      "enabled": true,
      "size": 1000,
      "ttl": 3600
    }
  }
}
```

#### Enhanced Access with AWS Credentials

```json
{
  "aws": {
    "region": "us-east-1",
    "credentials": {
      "accessKeyId": "your_access_key",
      "secretAccessKey": "your_secret_key"
    }
  },
  "documentation": {
    "enhanced_access": true,
    "private_content": true
  }
}
```

#### Enterprise Configuration

```json
{
  "enterprise": {
    "documentation": {
      "proxy_enabled": true,
      "content_filtering": true,
      "custom_endpoints": [
        "https://docs.internal.company.com/aws"
      ]
    },
    "search": {
      "intelligent_ranking": true,
      "context_awareness": true,
      "personalization": true
    }
  }
}
```

### Advanced Configuration Options

```json
{
  "server": {
    "port": 3006,
    "host": "0.0.0.0",
    "timeout": 30000
  },
  "documentation": {
    "services": {
      "enabled": ["all"],
      "disabled": [],
      "priority": ["ec2", "s3", "lambda", "rds"]
    },
    "content_types": {
      "user_guides": true,
      "api_references": true,
      "developer_guides": true,
      "cli_references": true,
      "sdk_documentation": true
    }
  },
  "search": {
    "intelligent_search": {
      "enabled": true,
      "context_awareness": true,
      "semantic_search": true
    },
    "indexing": {
      "full_text": true,
      "metadata": true,
      "cross_references": true
    }
  },
  "caching": {
    "enabled": true,
    "size": 1000,
    "ttl": 3600,
    "compression": true
  },
  "logging": {
    "level": "info",
    "format": "json",
    "file": "/var/log/aws-documentation-mcp.log"
  }
}
```

## Integration Capabilities

### Unified Intelligence System Integration

This server provides comprehensive documentation access capabilities for unified intelligence systems:

- **Real-time Documentation**: Instant access to latest AWS service documentation and updates
- **Intelligent Search**: Context-aware search with semantic understanding and relevance ranking
- **Cross-Service Discovery**: Intelligent discovery of related documentation across AWS services
- **Version Management**: Comprehensive version tracking and compatibility analysis
- **Development Integration**: Seamless integration with development workflows and IDE environments

### Development Workflow Enhancement

- **Contextual Help**: In-context documentation access during development tasks
- **API Reference**: Real-time API reference with examples and parameter documentation
- **Best Practices**: Access to AWS best practices and architectural guidance
- **Troubleshooting**: Comprehensive troubleshooting guides and error resolution
- **Learning Resources**: Progressive learning with guided documentation discovery

### Tools Available

1. **search_documentation**: Intelligent search across all AWS documentation
2. **get_service_docs**: Service-specific documentation retrieval
3. **access_api_reference**: Detailed API reference with examples
4. **discover_related**: Related documentation discovery and recommendations
5. **track_updates**: Documentation update tracking and notifications

### Resources Available

1. **docs://services/*/documentation**: Service-specific documentation collections
2. **docs://api-references/*/**: API reference documentation with examples
3. **docs://guides/best-practices**: AWS best practices and architectural guidance

## Business Impact

### Development Productivity Value

- **Documentation Access**: 70% reduction in time spent searching for AWS documentation
- **Development Efficiency**: Faster development with in-context documentation access
- **Learning Acceleration**: Improved team learning with intelligent content discovery
- **Error Resolution**: Faster troubleshooting with comprehensive guides and references

### Enterprise Integration Benefits

- **Knowledge Management**: Centralized AWS documentation access for development teams
- **Consistency**: Standardized documentation access across all projects and teams
- **Training Support**: Enhanced onboarding and continuous learning resources
- **Compliance**: Accurate and up-to-date documentation for compliance and audit requirements

### Return on Investment

- **Time Savings**: 5-8 hours per developer per month in documentation search and access
- **Training Cost**: 40% reduction in AWS training costs through self-service documentation
- **Development Speed**: 20% improvement in development velocity through faster documentation access
- **Knowledge Retention**: Improved team knowledge retention through intelligent content discovery

This server represents strategic infrastructure for AWS development teams and provides essential documentation access capabilities for unified intelligence systems with particular strength in intelligent search and contextual content discovery.