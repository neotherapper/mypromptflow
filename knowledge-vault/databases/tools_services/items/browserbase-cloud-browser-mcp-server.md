---
description: "Cloud browser automation platform enabling AI agents to control browsers at scale with session management, anti-detection, and parallel execution capabilities"
id: browserbase-001-2024
installation_priority: 1
item_type: mcp_server
name: Browserbase Cloud Browser MCP Server
priority: 1st_priority
production_readiness: 94
quality_score: 9.4
repository_url: https://github.com/browserbase/mcp-server
source_database: tools_services
status: active
tags:
- Tier 1
- MCP Server
- Browser Automation
- Cloud Service
- Web Scraping
- Testing Tool
- Official Integration
---

## 📋 Basic Information

**Browserbase Cloud Browser MCP Server** - Official Browserbase integration providing cloud-based browser automation with anti-detection, session persistence, and scalable parallel execution for AI agents.

## Quality & Scoring Metrics

### Business-Aligned Scoring Analysis

**Business Domain Relevance**: 9/10 - Essential for scalable web automation
**Technical Development Value**: 10/10 - Cloud browsers eliminate infrastructure complexity  
**Production Readiness**: 9/10 - Production-grade with high availability
**Setup Complexity**: 8/10 - Simple API with powerful features
**Maintenance Status**: 10/10 - Actively maintained by Browserbase team
**Documentation Quality**: 9/10 - Comprehensive documentation

**Composite Score: 9.4/10** - Tier 1 Implementation Priority

## Technical Specifications

### Core Capabilities
- **Cloud Browsers**: Fully managed browser instances
- **Session Persistence**: Maintain browser state across sessions
- **Anti-Detection**: Built-in fingerprinting protection
- **Parallel Execution**: Run thousands of browsers simultaneously
- **Proxy Support**: Integrated proxy rotation
- **Debug Tools**: Live browser viewing and debugging

### Advanced Features
- **Stealth Mode**: Undetectable automation
- **Cookie Management**: Persistent cookie storage
- **Extension Support**: Load browser extensions
- **Geographic Distribution**: Browsers in multiple regions
- **Screenshot & Recording**: Visual debugging capabilities
- **WebSocket Support**: Real-time browser control

## Setup & Configuration

### Installation Methods

#### Method 1: Docker MCP Toolkit (Recommended)
```bash
# Pull and run the MCP server
docker pull browserbase/mcp-server:latest
docker run -d --name browserbase-mcp \
  -e BROWSERBASE_API_KEY=${BROWSERBASE_API_KEY} \
  -e BROWSERBASE_PROJECT_ID=${BROWSERBASE_PROJECT_ID} \
  -p 3000:3000 \
  browserbase/mcp-server:latest
```

#### Method 2: Direct Installation
```bash
# Install via pnpm
pnpm install -g @browserbase/mcp-server

# Configure credentials
export BROWSERBASE_API_KEY="your_api_key_here"
export BROWSERBASE_PROJECT_ID="your_project_id"

# Start the server
browserbase-mcp-server --port 3000
```

### Configuration
```json
{
  "browserbase": {
    "api_key": "${BROWSERBASE_API_KEY}",
    "project_id": "${BROWSERBASE_PROJECT_ID}",
    "default_options": {
      "browser": "chrome",
      "headless": false,
      "stealth": true,
      "proxy": {
        "type": "residential",
        "country": "US"
      },
      "viewport": {
        "width": 1920,
        "height": 1080
      },
      "timeout": 60000,
      "keep_alive": true
    }
  }
}
```

## Use Cases

### Primary Applications
- **Web Scraping at Scale**: Parallel scraping with anti-detection
- **E2E Testing**: Cloud-based test execution
- **Form Automation**: Automated form filling and submission
- **Data Extraction**: Extract data from JavaScript-heavy sites
- **Browser RPA**: Robotic process automation in browsers

### Integration Example
```javascript
// Example: Cloud browser automation
const session = await browserbaseMCP.createSession({
  stealth: true,
  proxy: { country: "US" },
  persist: true
});

// Navigate and interact
await browserbaseMCP.navigate({
  sessionId: session.id,
  url: "https://example.com"
});

await browserbaseMCP.click({
  sessionId: session.id,
  selector: "#login-button"
});

await browserbaseMCP.type({
  sessionId: session.id,
  selector: "#username",
  text: "user@example.com"
});

// Take screenshot
const screenshot = await browserbaseMCP.screenshot({
  sessionId: session.id,
  fullPage: true
});

// Run parallel sessions
const sessions = await browserbaseMCP.createBatch({
  count: 10,
  template: {
    stealth: true,
    proxy: { rotating: true }
  }
});

// Execute JavaScript
const result = await browserbaseMCP.evaluate({
  sessionId: session.id,
  code: "document.title"
});
```

## Business Value

### Key Benefits
- Zero infrastructure management for browsers
- Built-in anti-detection for reliable automation
- Scale to thousands of concurrent browsers
- Geographic distribution for global testing
- Session persistence for complex workflows

### ROI Metrics
- 95% reduction in browser infrastructure costs
- 99.9% uptime for browser availability
- 10x faster parallel execution
- 90% success rate on protected sites