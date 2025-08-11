---
description: '## 📋 Basic Information MySQL Database MCP Server provides comprehensive integration with MySQL databases through the Model Context Protocol, enabling advanced database operations, query execution, and schema management for enterprise applications.'
estimated_setup_time: 10-15 minutes
id: 7c4f8d2a-1e6b-4927-a3f5-9d8c7b6a5e43
installation_priority: 1
item_type: mcp_server
name: MySQL Database MCP Server
priority: 1st_priority
quality_score: 8.8
setup_complexity: Simple
source_database: tools_services
status: active
tags:
- Tier 1
- MCP Server
- API Service
- Developer Tools
- Database
- Database - SQL
- Enterprise
- MySQL
- Software Development
maturity_level: stable
deployment_model: hybrid
integration_complexity: moderate
licensing_model: open_source
technology_type:
- database_sql
- dev_framework
url: https://github.com/modelcontextprotocol/servers/tree/main/src/mysql
vendor: Oracle Corporation
supported_platforms:
- linux
- windows
- macos
- web
- cross_platform
---

## 📋 Basic Information

The MySQL Database MCP Server provides comprehensive integration with MySQL databases through the Model Context Protocol, enabling sophisticated database operations, query execution, schema management, and data analysis for enterprise applications. With a business value score of 8.8/10, this server represents critical database infrastructure for modern development workflows.

**Key Value Propositions:**
- Complete MySQL ecosystem integration with advanced query capabilities and transaction management
- Enterprise-grade database connectivity with connection pooling and high availability support
- High-performance data operations with optimized query execution and result caching
- Comprehensive schema management including DDL operations and database migration support
- Advanced security features with role-based access control and encryption support
- Real-time monitoring and performance analytics for database optimization

## Quality & Scoring Metrics

### Business-Aligned Scoring Analysis

**Business Domain Relevance**: 9/10 (Critical database infrastructure for enterprise applications)
**Technical Development Value**: 9/10 (Essential data layer functionality for modern applications)
**Production Readiness**: 9/10 (Industry-leading reliability with mature ecosystem)
**Setup Complexity**: 8/10 (Standard database configuration with Docker support)
**Maintenance Status**: 9/10 (Actively maintained by MySQL community and Oracle)
**Documentation Quality**: 8/10 (Comprehensive documentation with extensive examples)

**Composite Score: 8.8/10** - Tier 1 Immediate Implementation Priority

### Production Readiness Assessment
- **Database Stability**: 99.99% uptime capability with clustering and replication
- **Security Compliance**: SSL/TLS encryption, role-based access control, audit logging
- **Scalability**: Horizontal scaling through replication and sharding strategies
- **Enterprise Features**: InnoDB storage engine, backup solutions, monitoring tools
- **Support Quality**: Extensive community support and Oracle enterprise support options

### Quality Validation Metrics
- **Integration Testing**: Comprehensive testing with major programming languages and frameworks
- **Performance Benchmarks**: Optimized for high-throughput OLTP workloads
- **Error Handling**: Robust transaction management and connection recovery
- **Monitoring**: Real-time performance metrics and query optimization tools
- **Compliance**: ACID compliance with enterprise-grade data consistency guarantees

## Technical Specifications

### Core Architecture
```yaml
Server Type: Relational Database Management System
Protocol: Model Context Protocol (MCP)
Primary Language: SQL with multi-language client support
Dependencies: MySQL Server 8.0+, appropriate database drivers
Authentication: Multiple methods (password, certificates, LDAP, PAM)
```

### System Requirements
- **Runtime**: MySQL Server 8.0+ with appropriate client libraries
- **Memory**: 4GB minimum for production workloads (128MB minimum for development)
- **Network**: TCP/IP connectivity on port 3306 (configurable)
- **Storage**: SSD recommended for optimal performance, varies by data size
- **CPU**: Multi-core recommended for concurrent connections
- **Additional**: Appropriate MySQL client drivers for target programming languages

### API Capabilities
```typescript
interface MySQLMCPCapabilities {
  dataDefinition: {
    createTables: boolean;
    alterTables: boolean;
    dropTables: boolean;
    manageIndexes: boolean;
  };
  dataManipulation: {
    insertData: boolean;
    updateData: boolean;
    deleteData: boolean;
    bulkOperations: boolean;
  };
  queryExecution: {
    selectQueries: boolean;
    complexJoins: boolean;
    aggregations: boolean;
    storedProcedures: boolean;
  };
  transactionManagement: {
    commitTransactions: boolean;
    rollbackTransactions: boolean;
    savepoints: boolean;
    isolationLevels: boolean;
  };
  administrationTools: {
    userManagement: boolean;
    permissionControl: boolean;
    backupRestore: boolean;
    performanceMonitoring: boolean;
  };
}
```

### Data Models
- **Tables**: Relational table structures with primary keys, foreign keys, and constraints
- **Views**: Virtual tables for complex query abstraction and security
- **Procedures**: Stored procedures and functions for business logic encapsulation

## Setup & Configuration

### Installation Methods

#### Method 1: Docker MCP Toolkit (Recommended)
Primary deployment method using Docker MCP server ecosystem
```bash
# Pull and run the MySQL MCP server with database
docker run -d --name mysql-db \
  -e MYSQL_ROOT_PASSWORD=your-secure-password \
  -e MYSQL_DATABASE=your-database \
  -e MYSQL_USER=your-user \
  -e MYSQL_PASSWORD=your-password \
  -p 3306:3306 \
  mysql:8.0

# Run MySQL MCP server
docker pull mcp/server-mysql:latest

docker run -d --name mysql-mcp \
  -e MYSQL_HOST=mysql-db \
  -e MYSQL_PORT=3306 \
  -e MYSQL_USER=your-user \
  -e MYSQL_PASSWORD=your-password \
  -e MYSQL_DATABASE=your-database \
  -p 3000:3000 \
  --link mysql-db:mysql \
  mcp/server-mysql:latest
```

#### Method 2: Docker Compose Deployment
Multi-service deployment with dependencies
```yaml
# docker-compose.yml
version: '3.8'
services:
  mysql-db:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=your-secure-root-password
      - MYSQL_DATABASE=your-database
      - MYSQL_USER=your-user
      - MYSQL_PASSWORD=your-password
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./init:/docker-entrypoint-initdb.d
    restart: unless-stopped
    command: --default-authentication-plugin=mysql_native_password

  mysql-mcp:
    image: mcp/server-mysql:latest
    environment:
      - MYSQL_HOST=mysql-db
      - MYSQL_PORT=3306
      - MYSQL_USER=your-user
      - MYSQL_PASSWORD=your-password
      - MYSQL_DATABASE=your-database
      - LOG_LEVEL=info
    ports:
      - "3000:3000"
    volumes:
      - ./config:/app/config
    depends_on:
      - mysql-db
    restart: unless-stopped

volumes:
  mysql_data:
```

#### Method 3: Claude Code Integration
Direct integration with Claude Code development environment
```bash
# Install via Claude Code MCP configuration
npm install -g @modelcontextprotocol/server-mysql

# Configure in Claude Code settings
{
  "mcpServers": {
    "mysql": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-mysql"],
      "env": {
        "MYSQL_HOST": "localhost",
        "MYSQL_PORT": "3306",
        "MYSQL_USER": "your-user",
        "MYSQL_PASSWORD": "your-password",
        "MYSQL_DATABASE": "your-database"
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
    "mysql": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-mysql"]
    }
  }
}
```

#### Method 5: Alternative Installation Methods
Fallback installation options
- Direct MySQL installation with custom MCP server implementation
- Package manager installation (apt, yum, homebrew for MySQL Server)
- Cloud MySQL services (Amazon RDS, Google Cloud SQL, Azure Database)
- Enterprise MySQL deployment with clustering and high availability

### Authentication Configuration

#### Password Authentication (Recommended)
```bash
# Set environment variables
export MYSQL_HOST="localhost"
export MYSQL_PORT="3306"
export MYSQL_USER="your-user"
export MYSQL_PASSWORD="your-password"
export MYSQL_DATABASE="your-database"

# Or use configuration file
cat > ~/.mysql/config.json << EOF
{
  "host": "localhost",
  "port": 3306,
  "user": "your-user",
  "password": "your-password",
  "database": "your-database",
  "ssl": {
    "rejectUnauthorized": false
  }
}
EOF
```

#### SSL Certificate Authentication
```json
{
  "mysql": {
    "host": "your-mysql-host",
    "port": 3306,
    "user": "your-user",
    "password": "your-password",
    "database": "your-database",
    "ssl": {
      "ca": "/path/to/ca-cert.pem",
      "cert": "/path/to/client-cert.pem",
      "key": "/path/to/client-key.pem",
      "rejectUnauthorized": true
    }
  }
}
```

#### Enterprise Configuration
```json
{
  "mysql": {
    "host": "mysql-cluster.company.com",
    "port": 3306,
    "user": "app-user",
    "password": "secure-password",
    "database": "production-db",
    "connectionLimit": 20,
    "acquireTimeout": 60000,
    "timeout": 60000,
    "reconnect": true,
    "ssl": {
      "rejectUnauthorized": true
    },
    "timezone": "UTC"
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
  "mysql": {
    "host": "localhost",
    "port": 3306,
    "user": "your-user",
    "password": "your-password",
    "database": "your-database",
    "connectionLimit": 10,
    "acquireTimeout": 60000,
    "timeout": 60000,
    "reconnect": true,
    "charset": "UTF8_GENERAL_CI",
    "timezone": "UTC",
    "ssl": {
      "rejectUnauthorized": false
    },
    "multipleStatements": false,
    "dateStrings": false,
    "debug": false,
    "trace": true,
    "supportBigNumbers": true,
    "bigNumberStrings": true
  },
  "security": {
    "query_timeout": 30000,
    "max_query_length": 1048576,
    "allowed_operations": ["SELECT", "INSERT", "UPDATE", "DELETE"],
    "restricted_databases": ["information_schema", "performance_schema", "sys"]
  },
  "logging": {
    "level": "info",
    "format": "json",
    "file": "/var/log/mysql-mcp.log",
    "query_logging": true,
    "performance_logging": true
  }
}
```