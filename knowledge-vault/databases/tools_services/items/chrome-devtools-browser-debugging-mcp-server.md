---
api_version: Chrome DevTools Protocol
authentication_types:
- Local Chrome Instance
- Remote Debugging
- WebSocket Connection
category: Development Tools
description: Browser debugging and development platform integration enabling automated performance analysis, network inspection, DOM manipulation, and JavaScript debugging for comprehensive web development workflows
id: b2c3d4e5-6789-abcd-ef01-23456789abcd
installation_priority: 1
item_type: mcp_server
name: Chrome DevTools Browser Debugging MCP Server
priority: 1st_priority
production_readiness: 95
provider: Google Chrome Team (Open Source)
quality_score: 8.7
source_database: tools_services
status: active
tags:
- Tier 1
- MCP Server
- automation
- browser-debugging
- development-tools
- devops
- javascript
- performance-analysis
- testing
- web-development
transport_protocols:
- WebSocket
- HTTP/HTTPS
- Chrome DevTools Protocol
tier: Tier 1
business_domain_relevance: 9
technical_development_value: 10
setup_complexity: 8
maintenance_status: 10
documentation_quality: 9
integration_potential: 10
composite_score: 8.7
---

## 📋 Basic Information

The Chrome DevTools Browser Debugging MCP Server delivers comprehensive browser development and debugging capabilities through the Model Context Protocol, enabling automated performance analysis, network inspection, DOM manipulation, JavaScript debugging, and security testing for modern web development workflows. With a business value score of 8.7/10, this server represents critical debugging infrastructure for contemporary web applications.

**Key Value Propositions:**
- Complete Chrome DevTools integration with automated debugging and performance analysis capabilities
- Enterprise-grade browser automation with headless operation and remote debugging support
- High-performance network inspection and security analysis with automated vulnerability detection
- Comprehensive JavaScript debugging with breakpoint management and runtime manipulation
- Advanced performance monitoring with Core Web Vitals measurement and optimization recommendations
- Production-ready browser testing with cross-device simulation and automated accessibility auditing

## Quality & Scoring Metrics

### Business-Aligned Scoring Analysis

**Business Domain Relevance**: 9/10 (Critical browser debugging infrastructure for web development)
**Technical Development Value**: 10/10 (Essential browser development and debugging capabilities)
**Production Readiness**: 9/10 (Stable Chrome DevTools Protocol with enterprise reliability)
**Setup Complexity**: 8/10 (Straightforward - Chrome installation with protocol access)
**Maintenance Status**: 10/10 (Official Google Chrome support with continuous development)
**Documentation Quality**: 9/10 (Comprehensive Chrome DevTools documentation with extensive API reference)

**Composite Score: 8.7/10** - Tier 1 Immediate Implementation Priority

### Production Readiness Assessment

- **API Stability**: Production Chrome DevTools Protocol with backward compatibility guarantees
- **Security Compliance**: Browser security sandbox with controlled debugging access
- **Scalability**: Multi-target debugging with concurrent session management
- **Enterprise Features**: Remote debugging, headless operation, automated testing integration
- **Support Quality**: Official Google Chrome support with extensive community documentation

### Quality Validation Metrics

- **Integration Testing**: Comprehensive test coverage with browser automation validation
- **Performance Benchmarks**: <50ms protocol response times with optimized WebSocket communication
- **Error Handling**: Robust connection management with automatic reconnection and error recovery
- **Monitoring**: Built-in performance tracking with debugging session analytics
- **Compliance**: Web security standards with Content Security Policy and CORS handling

## Technical Specifications

### Core Architecture

```yaml
Server Type: Browser Debugging Platform
Protocol: Model Context Protocol (MCP) + Chrome DevTools Protocol
Primary Language: TypeScript/Node.js
Dependencies: Chrome/Chromium 90+, WebSocket support, CDP client libraries
Authentication: Local Chrome instance, remote debugging authentication
```

### System Requirements

- **Runtime**: Node.js 16+ with Chrome/Chromium browser installed
- **Memory**: 2GB minimum, 8GB recommended for complex debugging sessions
- **Network**: WebSocket connectivity to Chrome debugging port (default 9222)
- **Storage**: 1GB local storage for debugging artifacts and performance traces
- **CPU**: 4+ cores recommended for parallel debugging and analysis operations
- **Additional**: Chrome browser with --remote-debugging-port flag enabled

### API Capabilities

```typescript
interface ChromeDevToolsMCPCapabilities {
  debuggingOperations: {
    breakpointManagement: boolean;
    variableInspection: boolean;
    stackTraceAnalysis: boolean;
    runtimeEvaluation: boolean;
    sourceMapSupport: boolean;
  };
  performanceAnalysis: {
    coreWebVitals: boolean;
    networkTimeline: boolean;
    memoryProfiling: boolean;
    cpuProfiling: boolean;
    lighthouseIntegration: boolean;
  };
  domManipulation: {
    elementInspection: boolean;
    stylesheetModification: boolean;
    eventListening: boolean;
    accessibilityAuditing: boolean;
    seoAnalysis: boolean;
  };
  networkInspection: {
    requestInterception: boolean;
    responseModification: boolean;
    cookieManagement: boolean;
    cacheInspection: boolean;
    securityAnalysis: boolean;
  };
}
```

### Data Models

- **Debugging Session**: Active debugging context with target tabs, breakpoints, and runtime state
- **Performance Profile**: CPU profiles, memory snapshots, network timelines, and Core Web Vitals data
- **DOM Snapshot**: Complete DOM structure with computed styles, accessibility tree, and element metadata
- **Network Activity**: Request/response data with timing information, headers, and security details

## Setup & Configuration

### Installation Methods

#### Method 1: Docker MCP Toolkit (Recommended)

Primary deployment method using Docker MCP server ecosystem

```bash
# Pull and run the Chrome DevTools MCP server
docker pull mcp/server-chrome-devtools:latest

# Run with environment configuration
docker run -d --name chrome-devtools-mcp \
  -e CHROME_DEBUGGING_PORT=9222 \
  -e HEADLESS_MODE=true \
  -e REMOTE_DEBUGGING=true \
  -p 9222:9222 \
  -p 3003:3003 \
  --security-opt seccomp:unconfined \
  mcp/server-chrome-devtools:latest
```

#### Method 2: Docker Compose Deployment

Multi-service deployment with dependencies

```yaml
# docker-compose.yml
version: '3.8'
services:
  chrome-devtools-mcp:
    image: mcp/server-chrome-devtools:latest
    environment:
      - CHROME_DEBUGGING_PORT=9222
      - HEADLESS_MODE=true
      - PERFORMANCE_MONITORING=true
      - LIGHTHOUSE_ENABLED=true
    ports:
      - "9222:9222"
      - "3003:3003"
    volumes:
      - chrome-data:/app/chrome-data
      - ./debug-sessions:/app/sessions
    security_opt:
      - seccomp:unconfined
    restart: unless-stopped
volumes:
  chrome-data:
```

#### Method 3: Claude Code Integration

Direct integration with Claude Code development environment

```bash
# Install via Claude Code MCP configuration
pnpm install -g @modelcontextprotocol/server-chrome-devtools

# Configure in Claude Code settings
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "mcp-server-chrome-devtools",
      "args": ["--port", "3003", "--chrome-port", "9222"],
      "env": {
        "CHROME_PATH": "/usr/bin/google-chrome",
        "HEADLESS_MODE": "false"
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
    "chrome-devtools": {
      "command": "pnpm dlx",
      "args": ["@modelcontextprotocol/server-chrome-devtools", "--local-chrome"]
    }
  }
}
```

#### Method 5: Alternative Installation Methods

- NPM package installation: `pnpm install -g @modelcontextprotocol/server-chrome-devtools`
- Local Chrome setup: Launch Chrome with `--remote-debugging-port=9222`
- Source compilation from GitHub repository
- CI/CD integration for automated browser testing workflows

### Authentication Configuration

#### Local Chrome Instance (Recommended)

```json
{
  "authentication": {
    "type": "local",
    "chromePath": "/usr/bin/google-chrome",
    "debuggingPort": 9222,
    "headless": false,
    "userDataDir": "./chrome-profile"
  }
}
```

#### Remote Chrome Debugging

```json
{
  "authentication": {
    "type": "remote",
    "host": "remote-chrome-server.com",
    "port": 9222,
    "secure": true,
    "authToken": "remote_debugging_token"
  }
}
```

#### Enterprise Configuration

```json
{
  "enterprise": {
    "multiUserSupport": true,
    "sessionPersistence": true,
    "auditLogging": true,
    "performanceMonitoring": {
      "enabled": true,
      "lighthouseIntegration": true,
      "coreWebVitalsTracking": true
    }
  }
}
```

### Advanced Configuration Options

```json
{
  "server": {
    "port": 3003,
    "host": "0.0.0.0",
    "timeout": 60000
  },
  "chrome": {
    "executablePath": "/usr/bin/google-chrome",
    "args": [
      "--remote-debugging-port=9222",
      "--disable-web-security",
      "--disable-features=TranslateUI",
      "--no-sandbox"
    ],
    "debugging": {
      "port": 9222,
      "host": "0.0.0.0",
      "maxConnections": 10
    }
  },
  "features": {
    "performanceMonitoring": true,
    "networkInterception": true,
    "domManipulation": true,
    "securityAuditing": true,
    "accessibilityTesting": true,
    "lighthouseIntegration": true
  },
  "session": {
    "persistent": true,
    "timeout": 300000,
    "maxSessions": 5,
    "cleanupInterval": 60000
  },
  "logging": {
    "level": "info",
    "format": "json",
    "file": "/var/log/chrome-devtools-mcp.log"
  }
}
```