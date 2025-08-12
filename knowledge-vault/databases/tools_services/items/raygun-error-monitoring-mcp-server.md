---
description: "Application performance monitoring and error tracking platform providing crash reporting, real user monitoring, and deployment tracking for production applications"
id: raygun-001-2024
installation_priority: 2
item_type: mcp_server
name: Raygun Error Monitoring MCP Server
priority: 1st_priority
production_readiness: 95
quality_score: 9.0
repository_url: https://github.com/MindscapeHQ/mcp-server-raygun
source_database: tools_services
status: active
tags:
- Tier 1
- MCP Server
- Monitoring Tool
- Error Tracking
- APM
- DevOps
- Analytics
- Official Integration
---

## 📋 Basic Information

**Raygun Error Monitoring MCP Server** - Official Raygun integration enabling AI agents to interact with crash reporting and real user monitoring data for automated error analysis and resolution.

## Quality & Scoring Metrics

### Business-Aligned Scoring Analysis

**Business Domain Relevance**: 9/10 - Critical for application reliability
**Technical Development Value**: 9/10 - Essential for production monitoring  
**Production Readiness**: 9/10 - Enterprise-grade monitoring platform
**Setup Complexity**: 8/10 - Simple API configuration
**Maintenance Status**: 10/10 - Actively maintained by Raygun
**Documentation Quality**: 9/10 - Comprehensive documentation

**Composite Score: 9.0/10** - Tier 1 Implementation Priority

## Technical Specifications

### Core Capabilities
- **Crash Reporting**: Automatic error capture and grouping
- **Real User Monitoring**: Performance metrics from actual users
- **Deployment Tracking**: Link errors to specific deployments
- **User Tracking**: Associate errors with affected users
- **Alert Management**: Intelligent alerting and notifications
- **Error Diagnostics**: Detailed stack traces and breadcrumbs

### Advanced Features
- **AI Error Analysis**: Automatic error pattern detection
- **Performance Profiling**: Application performance insights
- **Custom Data**: Attach custom data to errors
- **Integration Hub**: Connect with development tools
- **Team Collaboration**: Comments and assignments
- **Trend Analysis**: Error rate and impact trends

## Setup & Configuration

### Installation Methods

#### Method 1: Docker MCP Toolkit (Recommended)
```bash
# Pull and run the MCP server
docker pull raygun/mcp-server:latest
docker run -d --name raygun-mcp \
  -e RAYGUN_API_KEY=${RAYGUN_API_KEY} \
  -e RAYGUN_APP_ID=${RAYGUN_APP_ID} \
  -p 3000:3000 \
  raygun/mcp-server:latest
```

#### Method 2: Direct Installation
```bash
# Install via pnpm
pnpm install -g @raygun.io/mcp-server-raygun

# Configure credentials
export RAYGUN_API_KEY="your_api_key_here"
export RAYGUN_APP_ID="your_app_id_here"

# Start the server
raygun-mcp-server --port 3000
```

### Configuration
```json
{
  "raygun": {
    "api_key": "${RAYGUN_API_KEY}",
    "application_id": "${RAYGUN_APP_ID}",
    "features": {
      "crash_reporting": true,
      "real_user_monitoring": true,
      "deployment_tracking": true
    },
    "alerting": {
      "enabled": true,
      "channels": ["email", "slack"],
      "thresholds": {
        "error_rate": 5,
        "affected_users": 10
      }
    }
  }
}
```

## Use Cases

### Primary Applications
- **Error Resolution**: Automated error analysis and fixes
- **Performance Monitoring**: Track application performance
- **User Impact Analysis**: Understand error impact on users
- **Deployment Validation**: Monitor post-deployment health
- **Proactive Monitoring**: Detect issues before users report

### Integration Example
```javascript
// Example: Error monitoring with Raygun
const errors = await raygunMCP.getErrors({
  status: "active",
  limit: 50,
  timeRange: "24h"
});

// Get error details with diagnostics
const errorDetail = await raygunMCP.getErrorGroup({
  groupId: "error-group-123",
  includeStackTrace: true,
  includeBreadcrumbs: true,
  includeAffectedUsers: true
});

// Real User Monitoring data
const performance = await raygunMCP.getRUM({
  metric: "page_load_time",
  timeRange: "7d",
  groupBy: "page"
});

// Track deployment
await raygunMCP.recordDeployment({
  version: "2.0.1",
  releaseNotes: "Bug fixes and performance improvements",
  email: "deploy@example.com"
});

// Query affected users
const affectedUsers = await raygunMCP.getAffectedUsers({
  errorGroupId: "error-group-123",
  limit: 100
});

// Update error status
await raygunMCP.updateErrorStatus({
  groupId: "error-group-123",
  status: "resolved",
  comment: "Fixed in version 2.0.1"
});
```

## Business Value

### Key Benefits
- Reduce mean time to resolution by 60%
- Proactive error detection before user reports
- Complete visibility into application health
- Prioritize fixes based on user impact
- Link errors directly to code deployments

### ROI Metrics
- 90% faster error diagnosis
- 75% reduction in application downtime
- Track millions of events per day
- Support for all major platforms and languages