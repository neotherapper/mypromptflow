---
api_version: Lighthouse CLI 10+
authentication_types:
- Local CLI Execution
- Lighthouse CI Integration
- PSI API Token
category: Performance & Testing Tools
description: Web performance auditing and optimization platform integration enabling automated Core Web Vitals measurement, accessibility testing, SEO analysis, and comprehensive site quality assessment for modern web applications
id: c3d4e5f6-789a-bcde-f012-3456789abcde
installation_priority: 1
item_type: mcp_server
name: Lighthouse Performance Auditing MCP Server
priority: 1st_priority
production_readiness: 96
provider: Google Chrome Team (Open Source)
quality_score: 8.8
source_database: tools_services
status: active
tags:
- Tier 1
- MCP Server
- accessibility
- automation
- optimization
- performance-analysis
- quality-assurance
- seo
- testing
- web-vitals
transport_protocols:
- HTTP/HTTPS
- CLI Process
- PageSpeed Insights API
tier: Tier 1
business_domain_relevance: 10
technical_development_value: 9
setup_complexity: 8
maintenance_status: 10
documentation_quality: 9
integration_potential: 9
composite_score: 8.8
---

## 📋 Basic Information

The Lighthouse Performance Auditing MCP Server delivers comprehensive web performance analysis and optimization capabilities through the Model Context Protocol, enabling automated Core Web Vitals measurement, accessibility testing, SEO auditing, and progressive web app assessment for modern web development workflows. With a business value score of 8.8/10, this server represents critical performance infrastructure for contemporary web applications.

**Key Value Propositions:**
- Complete Lighthouse integration with automated Core Web Vitals measurement and performance optimization
- Enterprise-grade accessibility auditing with WCAG compliance validation and remediation recommendations
- High-performance SEO analysis with technical optimization suggestions and content quality assessment
- Comprehensive progressive web app evaluation with offline capability and installability testing
- Advanced CI/CD integration with performance budgets and automated regression detection
- Production-ready performance monitoring with historical trending and competitive benchmarking

## Quality & Scoring Metrics

### Business-Aligned Scoring Analysis

**Business Domain Relevance**: 10/10 (Critical performance infrastructure directly impacting business metrics)
**Technical Development Value**: 9/10 (Essential web performance and quality assurance capabilities)
**Production Readiness**: 9/10 (Mature Google-maintained tool with enterprise adoption)
**Setup Complexity**: 8/10 (Straightforward - Node.js and Chrome dependencies)
**Maintenance Status**: 10/10 (Official Google Chrome support with active development)
**Documentation Quality**: 9/10 (Comprehensive documentation with detailed configuration guides)

**Composite Score: 8.8/10** - Tier 1 Immediate Implementation Priority

### Production Readiness Assessment

- **API Stability**: Production Lighthouse CLI with stable configuration and reporting APIs
- **Security Compliance**: Secure execution environment with configurable audit parameters
- **Scalability**: Parallel audit execution with resource optimization and queue management
- **Enterprise Features**: CI/CD integration, performance budgets, historical reporting, alerting
- **Support Quality**: Official Google support with extensive community documentation

### Quality Validation Metrics

- **Integration Testing**: Comprehensive test coverage with audit result validation
- **Performance Benchmarks**: <30s audit completion times with optimized Chrome execution
- **Error Handling**: Robust error reporting with retry logic and graceful degradation
- **Monitoring**: Built-in performance tracking with audit success rate monitoring
- **Compliance**: Web standards compliance with accessibility and SEO best practices

## Technical Specifications

### Core Architecture

```yaml
Server Type: Performance Auditing Platform
Protocol: Model Context Protocol (MCP)
Primary Language: TypeScript/Node.js
Dependencies: Lighthouse 10+, Chrome/Chromium, PageSpeed Insights API
Authentication: Local CLI execution, PSI API key for enhanced features
```

### System Requirements

- **Runtime**: Node.js 16+ with Chrome/Chromium browser installed
- **Memory**: 4GB minimum, 8GB recommended for concurrent audit execution
- **Network**: HTTPS connectivity for PageSpeed Insights API and web content access
- **Storage**: 2GB local storage for audit reports, screenshots, and trace files
- **CPU**: 4+ cores recommended for parallel audit processing and Chrome execution
- **Additional**: Chrome browser for headless audit execution and DOM analysis

### API Capabilities

```typescript
interface LighthouseMCPCapabilities {
  performanceAuditing: {
    coreWebVitals: boolean;
    performanceScore: boolean;
    networkOptimization: boolean;
    resourceAnalysis: boolean;
    criticalPathAnalysis: boolean;
  };
  accessibilityTesting: {
    wcagCompliance: boolean;
    colorContrastAnalysis: boolean;
    keyboardNavigation: boolean;
    screenReaderCompatibility: boolean;
    ariaValidation: boolean;
  };
  seoAnalysis: {
    metaTagValidation: boolean;
    structuredDataTesting: boolean;
    mobileFriendliness: boolean;
    crawlabilityAnalysis: boolean;
    contentQualityAssessment: boolean;
  };
  pwaEvaluation: {
    serviceWorkerValidation: boolean;
    manifestValidation: boolean;
    offlineCapability: boolean;
    installabilityTesting: boolean;
    performanceOptimization: boolean;
  };
}
```

### Data Models

- **Audit Report**: Complete Lighthouse audit with scores, metrics, opportunities, and diagnostics
- **Performance Budget**: Configurable thresholds for metrics with pass/fail status tracking
- **Historical Data**: Time-series performance data with trend analysis and regression detection
- **Optimization Recommendations**: Actionable improvement suggestions with impact estimates

## Setup & Configuration

### Installation Methods

#### Method 1: Docker MCP Toolkit (Recommended)

Primary deployment method using Docker MCP server ecosystem

```bash
# Pull and run the Lighthouse Performance Auditing MCP server
docker pull mcp/server-lighthouse:latest

# Run with environment configuration
docker run -d --name lighthouse-mcp \
  -e PSI_API_KEY=${PSI_API_KEY} \
  -e CHROME_PATH=/usr/bin/google-chrome \
  -e OUTPUT_FORMAT=json,html \
  -p 3004:3004 \
  --cap-add=SYS_ADMIN \
  mcp/server-lighthouse:latest
```

#### Method 2: Docker Compose Deployment

Multi-service deployment with dependencies

```yaml
# docker-compose.yml
version: '3.8'
services:
  lighthouse-mcp:
    image: mcp/server-lighthouse:latest
    environment:
      - PSI_API_KEY=${PSI_API_KEY}
      - CHROME_PATH=/usr/bin/google-chrome
      - OUTPUT_FORMAT=json,html
      - PERFORMANCE_BUDGET_ENABLED=true
      - CI_MODE=true
    ports:
      - "3004:3004"
    volumes:
      - lighthouse-reports:/app/reports
      - lighthouse-config:/app/config
    cap_add:
      - SYS_ADMIN
    restart: unless-stopped
volumes:
  lighthouse-reports:
  lighthouse-config:
```

#### Method 3: Claude Code Integration

Direct integration with Claude Code development environment

```bash
# Install via Claude Code MCP configuration
pnpm install -g @modelcontextprotocol/server-lighthouse

# Configure in Claude Code settings
{
  "mcpServers": {
    "lighthouse": {
      "command": "mcp-server-lighthouse",
      "args": ["--port", "3004"],
      "env": {
        "PSI_API_KEY": "your_psi_api_key",
        "CHROME_PATH": "/usr/bin/google-chrome"
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
    "lighthouse": {
      "command": "pnpm dlx",
      "args": ["@modelcontextprotocol/server-lighthouse"]
    }
  }
}
```

#### Method 5: Alternative Installation Methods

- NPM package installation: `pnpm install -g lighthouse @modelcontextprotocol/server-lighthouse`
- Lighthouse CI setup: `pnpm install -g @lhci/cli @modelcontextprotocol/server-lighthouse`
- Source compilation from GitHub repository
- CI/CD pipeline integration with performance budget enforcement

### Authentication Configuration

#### PageSpeed Insights API (Recommended)

```json
{
  "authentication": {
    "type": "psi_api",
    "apiKey": "your_pagespeed_insights_api_key",
    "quotaLimits": {
      "requestsPerDay": 25000,
      "requestsPerMinute": 250
    }
  }
}
```

#### Local CLI Execution

```json
{
  "authentication": {
    "type": "local_cli",
    "chromePath": "/usr/bin/google-chrome",
    "chromeFlags": [
      "--headless",
      "--no-sandbox",
      "--disable-gpu"
    ]
  }
}
```

#### Enterprise Configuration

```json
{
  "enterprise": {
    "lighthouseCI": {
      "enabled": true,
      "serverUrl": "https://lhci.example.com",
      "token": "lhci_server_token"
    },
    "performanceBudgets": {
      "enabled": true,
      "budgetPath": "./lighthouse-budget.json"
    },
    "reporting": {
      "webhooks": [
        "https://slack.com/webhooks/performance-alerts"
      ],
      "historicalStorage": true
    }
  }
}
```

### Advanced Configuration Options

```json
{
  "server": {
    "port": 3004,
    "host": "0.0.0.0",
    "timeout": 120000
  },
  "lighthouse": {
    "configPath": "./lighthouse-config.js",
    "outputFormat": ["json", "html"],
    "chromeFlags": [
      "--headless",
      "--no-sandbox",
      "--disable-gpu",
      "--disable-dev-shm-usage"
    ],
    "onlyCategories": [
      "performance",
      "accessibility",
      "best-practices",
      "seo",
      "pwa"
    ]
  },
  "auditing": {
    "concurrent": 3,
    "retryAttempts": 2,
    "timeout": 60000,
    "throttling": {
      "rttMs": 150,
      "throughputKbps": 1638.4,
      "cpuSlowdownMultiplier": 4
    }
  },
  "budgets": {
    "performanceThreshold": 90,
    "accessibilityThreshold": 95,
    "seoThreshold": 90,
    "bestPracticesThreshold": 90
  },
  "logging": {
    "level": "info",
    "format": "json",
    "file": "/var/log/lighthouse-mcp.log"
  }
}
```