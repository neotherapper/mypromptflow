---
description: '## 📋 Basic Information Redis Cache Database MCP Server provides comprehensive integration with Redis in-memory data store through the Model Context Protocol, enabling high-performance caching, session management, and real-time data operations for enterprise applications.'
estimated_setup_time: 10-15 minutes
id: 3b7e9f1c-6d2a-4853-b9e4-1c8f5a3d7b96
installation_priority: 1
item_type: mcp_server
name: Redis Cache Database MCP Server
priority: 1st_priority
quality_score: 8.9
setup_complexity: Simple
source_database: tools_services
status: active
tags:
- Tier 1
- MCP Server
- API Service
- Developer Tools
- Cache
- Database
- Database - Key-Value
- Enterprise
- Performance
- Redis
- Software Development
maturity_level: stable
deployment_model: hybrid
integration_complexity: simple
licensing_model: open_source
technology_type:
- database_key_value
- dev_framework
- caching
url: https://github.com/modelcontextprotocol/servers/tree/main/src/redis
vendor: Redis Ltd.
supported_platforms:
- linux
- windows
- macos
- web
- cross_platform
---

## 📋 Basic Information

The Redis Cache Database MCP Server provides comprehensive integration with Redis in-memory data store through the Model Context Protocol, enabling high-performance caching, session management, pub/sub messaging, and real-time data operations for enterprise applications. With a business value score of 8.9/10, this server represents critical performance infrastructure for modern development workflows.

**Key Value Propositions:**
- Complete Redis ecosystem integration with advanced data structures and operations
- Enterprise-grade caching solution with sub-millisecond response times
- High-performance session management and user state persistence
- Comprehensive pub/sub messaging system for real-time application features
- Advanced data structures including sorted sets, streams, and geospatial indexes
- Real-time analytics and monitoring with Redis modules and clustering support

## Quality & Scoring Metrics

### Business-Aligned Scoring Analysis

**Business Domain Relevance**: 9/10 (Critical performance infrastructure for enterprise applications)
**Technical Development Value**: 9/10 (Essential caching and performance optimization layer)
**Production Readiness**: 9/10 (Industry-leading reliability with mature ecosystem)
**Setup Complexity**: 9/10 (Simple configuration with Docker support)
**Maintenance Status**: 9/10 (Actively maintained by Redis Ltd. and community)
**Documentation Quality**: 9/10 (Excellent documentation with comprehensive examples)

**Composite Score: 8.9/10** - Tier 1 Immediate Implementation Priority

### Production Readiness Assessment
- **Performance Stability**: Sub-millisecond latency with throughput up to 1M+ operations per second
- **Security Compliance**: AUTH authentication, TLS encryption, ACL-based access control
- **Scalability**: Horizontal scaling through Redis Cluster and vertical scaling support
- **Enterprise Features**: Redis Enterprise with multi-tenancy, geo-replication, active-active clustering
- **Support Quality**: Extensive community support and Redis Ltd. enterprise support

### Quality Validation Metrics
- **Integration Testing**: Comprehensive testing across major programming languages and frameworks
- **Performance Benchmarks**: Optimized for high-throughput, low-latency operations
- **Error Handling**: Robust connection management and automatic failover capabilities
- **Monitoring**: Real-time performance metrics, memory usage tracking, and alerting
- **Compliance**: Data persistence options with durability guarantees and backup strategies

## Technical Specifications

### Core Architecture
```yaml
Server Type: In-Memory Data Store & Cache
Protocol: Model Context Protocol (MCP)
Primary Language: Redis commands with multi-language client support
Dependencies: Redis Server 6.0+, appropriate Redis client libraries
Authentication: Password-based, ACL, and TLS certificate authentication
```

### System Requirements
- **Runtime**: Redis Server 6.0+ with appropriate client libraries
- **Memory**: 1GB minimum for development (scales with data requirements)
- **Network**: TCP/IP connectivity on port 6379 (configurable)
- **Storage**: Optional for persistence (RDB snapshots, AOF logging)
- **CPU**: Single-threaded core performance critical, multi-core for modules
- **Additional**: Appropriate Redis client drivers for target programming languages

### API Capabilities
```typescript
interface RedisMCPCapabilities {
  dataStructures: {
    strings: boolean;
    hashes: boolean;
    lists: boolean;
    sets: boolean;
    sortedSets: boolean;
    streams: boolean;
    geospatial: boolean;
    hyperLogLog: boolean;
  };
  cacheOperations: {
    setExpiration: boolean;
    keyManagement: boolean;
    memoryOptimization: boolean;
    evictionPolicies: boolean;
  };
  pubsubMessaging: {
    publishSubscribe: boolean;
    patternMatching: boolean;
    streamProcessing: boolean;
    messageQueues: boolean;
  };
  transactionSupport: {
    multiExec: boolean;
    pipelining: boolean;
    luaScripting: boolean;
    atomicOperations: boolean;
  };
  clusterOperations: {
    sharding: boolean;
    replication: boolean;
    sentinelHA: boolean;
    clusterManagement: boolean;
  };
}
```

### Data Models
- **Key-Value**: Simple string-based key-value storage with TTL support
- **Complex Structures**: Hash tables, lists, sets, and sorted sets for complex data modeling
- **Streams**: Time-series data structures for event sourcing and real-time analytics

## Setup & Configuration

### Installation Methods

#### Method 1: Docker MCP Toolkit (Recommended)
Primary deployment method using Docker MCP server ecosystem
```bash
# Pull and run Redis server
docker run -d --name redis-server \
  -p 6379:6379 \
  redis:7-alpine redis-server --appendonly yes --requirepass your-password

# Run Redis MCP server
docker pull mcp/server-redis:latest

docker run -d --name redis-mcp \
  -e REDIS_HOST=redis-server \
  -e REDIS_PORT=6379 \
  -e REDIS_PASSWORD=your-password \
  -e REDIS_DB=0 \
  -p 3000:3000 \
  --link redis-server:redis \
  mcp/server-redis:latest
```

#### Method 2: Docker Compose Deployment
Multi-service deployment with dependencies
```yaml
# docker-compose.yml
version: '3.8'
services:
  redis-server:
    image: redis:7-alpine
    command: redis-server --appendonly yes --requirepass your-password
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
      - ./redis.conf:/usr/local/etc/redis/redis.conf
    restart: unless-stopped

  redis-mcp:
    image: mcp/server-redis:latest
    environment:
      - REDIS_HOST=redis-server
      - REDIS_PORT=6379
      - REDIS_PASSWORD=your-password
      - REDIS_DB=0
      - LOG_LEVEL=info
    ports:
      - "3000:3000"
    volumes:
      - ./config:/app/config
    depends_on:
      - redis-server
    restart: unless-stopped

volumes:
  redis_data:
```

#### Method 3: Claude Code Integration
Direct integration with Claude Code development environment
```bash
# Install via Claude Code MCP configuration
npm install -g @modelcontextprotocol/server-redis

# Configure in Claude Code settings
{
  "mcpServers": {
    "redis": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-redis"],
      "env": {
        "REDIS_HOST": "localhost",
        "REDIS_PORT": "6379",
        "REDIS_PASSWORD": "your-password",
        "REDIS_DB": "0"
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
    "redis": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-redis"]
    }
  }
}
```

#### Method 5: Alternative Installation Methods
Fallback installation options
- Direct Redis installation with custom MCP server implementation
- Package manager installation (apt, yum, homebrew for Redis Server)
- Cloud Redis services (Amazon ElastiCache, Google Memorystore, Azure Cache)
- Redis Enterprise deployment with advanced clustering and security features

### Authentication Configuration

#### Password Authentication (Recommended)
```bash
# Set environment variables
export REDIS_HOST="localhost"
export REDIS_PORT="6379"
export REDIS_PASSWORD="your-secure-password"
export REDIS_DB="0"

# Or use configuration file
cat > ~/.redis/config.json << EOF
{
  "host": "localhost",
  "port": 6379,
  "password": "your-secure-password",
  "db": 0,
  "retryDelayOnFailover": 100,
  "enableReadyCheck": true,
  "maxRetriesPerRequest": 3
}
EOF
```

#### TLS Configuration
```json
{
  "redis": {
    "host": "your-redis-host",
    "port": 6380,
    "password": "your-password",
    "db": 0,
    "tls": {
      "cert": "/path/to/client-cert.pem",
      "key": "/path/to/client-key.pem",
      "ca": "/path/to/ca-cert.pem",
      "rejectUnauthorized": true
    }
  }
}
```

#### Enterprise Configuration
```json
{
  "redis": {
    "host": "redis-cluster.company.com",
    "port": 6379,
    "password": "enterprise-password",
    "db": 0,
    "connectTimeout": 10000,
    "commandTimeout": 5000,
    "retryDelayOnFailover": 100,
    "enableOfflineQueue": false,
    "lazyConnect": true,
    "keepAlive": 30000,
    "family": 4,
    "maxRetriesPerRequest": 3,
    "retryStrategy": "exponential_backoff"
  }
}
```

### Advanced Configuration Options
```json
{
  "server": {
    "port": 3000,
    "host": "0.0.0.0",
    "timeout": 30000
  },
  "redis": {
    "host": "localhost",
    "port": 6379,
    "password": "your-password",
    "db": 0,
    "keyPrefix": "mcp:",
    "connectTimeout": 10000,
    "commandTimeout": 5000,
    "retryDelayOnFailover": 100,
    "enableReadyCheck": true,
    "maxRetriesPerRequest": 3,
    "lazyConnect": false,
    "keepAlive": 30000,
    "family": 4,
    "enableOfflineQueue": true,
    "readOnly": false,
    "stringNumbers": false,
    "dropBufferSupport": false
  },
  "clustering": {
    "enableCluster": false,
    "clusterRetryDelayOnFailover": 100,
    "clusterRetryDelayOnClusterDown": 300,
    "clusterMaxRedirections": 6,
    "scaleReads": "master"
  },
  "security": {
    "acl_enabled": true,
    "max_memory_policy": "allkeys-lru",
    "protected_mode": true,
    "allowed_operations": ["GET", "SET", "DEL", "EXISTS", "EXPIRE"]
  },
  "logging": {
    "level": "info",
    "format": "json",
    "file": "/var/log/redis-mcp.log",
    "command_logging": false,
    "performance_logging": true
  }
}
```