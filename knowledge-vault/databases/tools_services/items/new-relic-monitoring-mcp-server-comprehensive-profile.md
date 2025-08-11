---
description: '## 📋 Basic Information New Relic Monitoring MCP Server provides comprehensive integration with New Relic observability platform through the Model Context Protocol, enabling advanced application performance monitoring, infrastructure monitoring, and real-time analytics for enterprise applications.'
estimated_setup_time: 15-20 minutes
id: 9e4b7f3a-2d8c-4916-b7e2-5f1a8d6c9b47
installation_priority: 1
item_type: mcp_server
name: New Relic Monitoring MCP Server
priority: 1st_priority
quality_score: 8.7
setup_complexity: Moderate
source_database: tools_services
status: active
tags:
- Monitoring
- MCP Server
- API Service
- Tier 2
- DevOps
- Enterprise
- New Relic
- Observability
- Performance Monitoring
- Analytics
maturity_level: stable
deployment_model: cloud_hosted
integration_complexity: moderate
licensing_model: freemium
technology_type:
- monitoring
- analytics
- dev_tool
url: https://docs.newrelic.com/docs/apis/
vendor: New Relic, Inc.
supported_platforms:
- web
- linux
- windows
- macos
- cross_platform
---

## 📋 Basic Information

The New Relic Monitoring MCP Server provides comprehensive integration with New Relic's observability platform through the Model Context Protocol, enabling advanced application performance monitoring (APM), infrastructure monitoring, real-time user monitoring (RUM), and comprehensive analytics for enterprise applications. With a business value score of 8.7/10, this server represents critical observability infrastructure for modern development workflows.

**Key Value Propositions:**
- Complete New Relic ecosystem integration with APM, infrastructure, and digital experience monitoring
- Enterprise-grade observability with AI-powered incident detection and root cause analysis
- High-performance real-time monitoring with sub-second metric collection and alerting
- Comprehensive distributed tracing and service map visualization for microservices architectures
- Advanced query capabilities with NRQL for custom dashboards and business intelligence
- Real-time collaboration features with incident management and team notification systems

## Quality & Scoring Metrics

### Business-Aligned Scoring Analysis

**Business Domain Relevance**: 9/10 (Critical observability infrastructure for enterprise applications)
**Technical Development Value**: 9/10 (Essential monitoring and performance optimization capabilities)
**Production Readiness**: 9/10 (Industry-leading reliability with mature enterprise features)
**Setup Complexity**: 7/10 (Moderate complexity with agent installation and configuration)
**Maintenance Status**: 9/10 (Actively maintained by New Relic with continuous feature updates)
**Documentation Quality**: 8/10 (Comprehensive documentation with extensive integration guides)

**Composite Score: 8.7/10** - Tier 2 Strategic Implementation Priority

### Production Readiness Assessment
- **Monitoring Stability**: 99.9% uptime with global data centers and redundant infrastructure
- **Security Compliance**: SOC 2 Type II, ISO 27001, FedRAMP compliance with enterprise security features
- **Scalability**: Auto-scaling data ingestion supporting millions of metrics and events per minute
- **Enterprise Features**: RBAC, SAML/SSO integration, custom alerting, API governance, dedicated support
- **Support Quality**: 24/7 technical support with dedicated customer success managers

### Quality Validation Metrics
- **Integration Testing**: Comprehensive testing across 70+ programming languages and frameworks
- **Performance Benchmarks**: Sub-second query response times with real-time streaming data
- **Error Handling**: Robust agent recovery and data backup with intelligent sampling
- **Monitoring**: Self-monitoring platform with comprehensive SLA tracking and transparency
- **Compliance**: Continuous compliance monitoring with automated governance reporting

## Technical Specifications

### Core Architecture
```yaml
Server Type: Observability and Monitoring Platform
Protocol: Model Context Protocol (MCP)
Primary Language: REST API with GraphQL support and multi-language agents
Dependencies: New Relic account, appropriate API keys, monitoring agents
Authentication: License key-based with API key authentication and user token access
```

### System Requirements
- **Runtime**: New Relic agents compatible with application runtime (APM) and infrastructure monitoring
- **Memory**: Agent footprint <50MB, varies by monitoring scope and data retention
- **Network**: HTTPS connectivity to New Relic collectors (collector.newrelic.com)
- **Storage**: Local agent configuration and temporary data buffering
- **CPU**: Minimal CPU overhead (<5% impact on monitored applications)
- **Additional**: New Relic account with appropriate license keys and data retention settings

### API Capabilities
```typescript
interface NewRelicMCPCapabilities {
  applicationMonitoring: {
    apmTransactionTracing: boolean;
    errorTracking: boolean;
    databaseMonitoring: boolean;
    externalServices: boolean;
    customMetrics: boolean;
    distributedTracing: boolean;
  };
  infrastructureMonitoring: {
    hostMetrics: boolean;
    containerMonitoring: boolean;
    kubernetesIntegration: boolean;
    cloudIntegrations: boolean;
    networkMonitoring: boolean;
    processMonitoring: boolean;
  };
  digitalExperience: {
    browserMonitoring: boolean;
    mobileMonitoring: boolean;
    syntheticMonitoring: boolean;
    userSessionReplay: boolean;
    webVitalsTracking: boolean;
  };
  alertingAndIncidents: {
    nrqlAlertConditions: boolean;
    anomalyDetection: boolean;
    incidentManagement: boolean;
    notificationChannels: boolean;
    escalationPolicies: boolean;
  };
  dataAnalytics: {
    nrqlQuerying: boolean;
    customDashboards: boolean;
    dataExport: boolean;
    metricsAndEvents: boolean;
    logManagement: boolean;
  };
}
```

### Data Models
- **Applications**: APM applications with transaction traces, errors, and performance metrics
- **Infrastructure**: Host and container metrics with resource utilization and health status
- **Alerts**: Alert policies and conditions with incident management and notification workflows

## Setup & Configuration

### Installation Methods

#### Method 1: Docker MCP Toolkit (Recommended)
Primary deployment method using Docker MCP server ecosystem
```bash
# Pull and run New Relic infrastructure agent
docker run -d --name newrelic-infra \
  --privileged \
  --net=host \
  --pid=host \
  -v "/:/host:ro" \
  -v "/var/run/docker.sock:/var/run/docker.sock" \
  -e NRIA_LICENSE_KEY=your_license_key \
  newrelic/infrastructure:latest

# Run New Relic MCP server
docker pull mcp/server-newrelic:latest

docker run -d --name newrelic-mcp \
  -e NEW_RELIC_API_KEY=your_user_api_key \
  -e NEW_RELIC_ACCOUNT_ID=your_account_id \
  -e NEW_RELIC_LICENSE_KEY=your_license_key \
  -e NEW_RELIC_REGION=US \
  -p 3000:3000 \
  mcp/server-newrelic:latest
```

#### Method 2: Docker Compose Deployment
Multi-service deployment with dependencies
```yaml
# docker-compose.yml
version: '3.8'
services:
  newrelic-infra:
    image: newrelic/infrastructure:latest
    privileged: true
    network_mode: host
    pid: host
    environment:
      - NRIA_LICENSE_KEY=your_license_key
      - NRIA_DISPLAY_NAME=docker-host-$(hostname)
      - NRIA_VERBOSE=1
    volumes:
      - "/:/host:ro"
      - "/var/run/docker.sock:/var/run/docker.sock"
    restart: unless-stopped

  newrelic-mcp:
    image: mcp/server-newrelic:latest
    environment:
      - NEW_RELIC_API_KEY=your_user_api_key
      - NEW_RELIC_ACCOUNT_ID=your_account_id
      - NEW_RELIC_LICENSE_KEY=your_license_key
      - NEW_RELIC_REGION=US
      - LOG_LEVEL=info
    ports:
      - "3000:3000"
    volumes:
      - ./config:/app/config
    restart: unless-stopped

volumes:
  newrelic_data:
```

#### Method 3: Claude Code Integration
Direct integration with Claude Code development environment
```bash
# Install via Claude Code MCP configuration
npm install -g @modelcontextprotocol/server-newrelic

# Configure in Claude Code settings
{
  "mcpServers": {
    "newrelic": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-newrelic"],
      "env": {
        "NEW_RELIC_API_KEY": "your_user_api_key",
        "NEW_RELIC_ACCOUNT_ID": "your_account_id",
        "NEW_RELIC_LICENSE_KEY": "your_license_key"
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
    "newrelic": {
      "command": "npx",
      "args": ["@modelcontextprotocol/server-newrelic"]
    }
  }
}
```

#### Method 5: Alternative Installation Methods
Fallback installation options
- Direct agent installation on target systems (guided installation)
- Kubernetes deployment with Helm charts and operator support
- Cloud marketplace deployments (AWS, Azure, GCP with one-click installation)
- Enterprise deployment with centralized configuration management

### Authentication Configuration

#### API Key Authentication (Recommended)
```bash
# Set environment variables
export NEW_RELIC_API_KEY="NRAK-your_user_api_key"
export NEW_RELIC_ACCOUNT_ID="your_account_id"
export NEW_RELIC_LICENSE_KEY="your_license_key"
export NEW_RELIC_REGION="US"  # or "EU" for EU region

# Or use configuration file
cat > ~/.newrelic/config.json << EOF
{
  "apiKey": "NRAK-your_user_api_key",
  "accountId": "your_account_id",
  "licenseKey": "your_license_key",
  "region": "US",
  "timeout": 30000,
  "retries": 3
}
EOF
```

#### Enterprise SSO Configuration
```json
{
  "newrelic": {
    "authentication": {
      "type": "oauth",
      "clientId": "your_oauth_client_id",
      "clientSecret": "your_oauth_client_secret",
      "redirectUri": "https://your-app.com/auth/newrelic/callback",
      "scopes": ["read", "write", "admin"]
    },
    "saml": {
      "enabled": true,
      "entityId": "your-entity-id",
      "ssoUrl": "https://your-sso.com/saml/newrelic",
      "x509Certificate": "/path/to/certificate.pem"
    }
  }
}
```

#### Regional Configuration
```json
{
  "newrelic": {
    "region": "US",
    "endpoints": {
      "api": "https://api.newrelic.com",
      "collector": "collector.newrelic.com",
      "insights": "https://insights-api.newrelic.com"
    },
    "dataRetention": {
      "metrics": "8_days",
      "events": "8_days",
      "logs": "30_days",
      "traces": "8_days"
    }
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
  "newrelic": {
    "apiKey": "NRAK-your_user_api_key",
    "accountId": "your_account_id",
    "licenseKey": "your_license_key",
    "region": "US",
    "timeout": 30000,
    "retries": 3,
    "rateLimit": {
      "rpm": 3000,
      "burstLimit": 100
    },
    "features": {
      "distributedTracing": true,
      "infiniteTracing": false,
      "customAttributes": true,
      "logForwarding": true,
      "vulnerabilityManagement": true
    },
    "sampling": {
      "transactionSampling": 0.1,
      "errorSampling": 1.0,
      "logSampling": 0.05,
      "traceSampling": 0.1
    },
    "alerting": {
      "defaultNotificationChannel": "email",
      "escalationTimeout": 300,
      "autoResolveTimeout": 1800
    }
  },
  "integrations": {
    "kubernetes": {
      "enabled": true,
      "clusterName": "production-cluster",
      "namespace": "monitoring"
    },
    "aws": {
      "enabled": true,
      "roleArn": "arn:aws:iam::account:role/NewRelicInfrastructure-Integrations",
      "regions": ["us-east-1", "us-west-2"]
    },
    "slack": {
      "enabled": true,
      "webhookUrl": "https://hooks.slack.com/services/...",
      "channel": "#alerts"
    }
  },
  "logging": {
    "level": "info",
    "format": "json",
    "file": "/var/log/newrelic-mcp.log",
    "forwardToNewRelic": true,
    "includeStackTrace": true
  }
}
```