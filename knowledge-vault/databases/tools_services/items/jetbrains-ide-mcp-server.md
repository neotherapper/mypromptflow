---
description: "Official JetBrains IDE integration enabling AI agents to work directly with IntelliJ IDEA, WebStorm, PyCharm, and other JetBrains IDEs for code editing and project management"
id: jetbrains-001-2024
installation_priority: 1
item_type: mcp_server
name: JetBrains IDE MCP Server
priority: 1st_priority
production_readiness: 96
quality_score: 9.6
repository_url: https://github.com/jetbrains/mcp-server
source_database: tools_services
status: active
tags:
- Tier 1
- MCP Server
- IDE Integration
- Developer Tool
- Code Editor
- JetBrains
- Official Integration
---

## 📋 Basic Information

**JetBrains IDE MCP Server** - Official JetBrains integration allowing AI agents to interact with JetBrains IDEs including IntelliJ IDEA, WebStorm, PyCharm, GoLand, and others for intelligent code editing and project management.

## Quality & Scoring Metrics

### Business-Aligned Scoring Analysis

**Business Domain Relevance**: 10/10 - Essential for professional development workflows
**Technical Development Value**: 10/10 - Deep IDE integration for AI-assisted coding  
**Production Readiness**: 10/10 - Enterprise-grade with JetBrains support
**Setup Complexity**: 7/10 - Requires IDE plugin installation
**Maintenance Status**: 10/10 - Actively maintained by JetBrains
**Documentation Quality**: 10/10 - Professional documentation

**Composite Score: 9.6/10** - Tier 1 Implementation Priority

## Technical Specifications

### Core Capabilities
- **Multi-IDE Support**: Works with all JetBrains IDEs
- **Code Navigation**: Navigate projects, files, and symbols
- **Code Editing**: Direct code modification in IDE
- **Refactoring**: Automated refactoring operations
- **Code Analysis**: Access IDE inspections and analysis
- **Debugging Integration**: Control debugger from AI

### IDE Features
- **Project Management**: Open, create, manage projects
- **Version Control**: Git operations through IDE
- **Build Tools**: Run builds, tests, and tasks
- **Code Completion**: Access IDE's intelligent completion
- **Quick Fixes**: Apply IDE suggested fixes
- **Search**: Project-wide search capabilities

## Setup & Configuration

### Installation Methods

#### Method 1: JetBrains Plugin Installation
```bash
# Install MCP plugin in your JetBrains IDE
# 1. Open IDE Settings/Preferences
# 2. Go to Plugins
# 3. Search for "MCP Server"
# 4. Install and restart IDE

# Start MCP server from IDE
# Tools -> MCP Server -> Start Server
```

#### Method 2: Standalone Installation
```bash
# Install via pnpm
pnpm install -g @jetbrains/mcp-server

# Start server with IDE path
jetbrains-mcp-server \
  --ide-path "/Applications/IntelliJ IDEA.app" \
  --port 3000
```

### Configuration
```json
{
  "jetbrains": {
    "ide_type": "idea",
    "project_path": "${PROJECT_PATH}",
    "features": {
      "code_editing": true,
      "refactoring": true,
      "debugging": true,
      "version_control": true,
      "build_tools": true
    },
    "permissions": {
      "read": true,
      "write": true,
      "execute": true,
      "refactor": true
    },
    "auto_save": true,
    "format_on_save": true
  }
}
```

## Use Cases

### Primary Applications
- **AI Pair Programming**: Real-time code collaboration
- **Automated Refactoring**: Large-scale code improvements
- **Code Review**: AI-assisted code review in IDE
- **Test Generation**: Create tests with IDE context
- **Documentation**: Generate docs with code understanding

### Integration Example
```javascript
// Example: IDE operations via MCP
const project = await jetbrainsMCP.openProject({
  path: "/Users/dev/my-project"
});

// Navigate to file
await jetbrainsMCP.openFile({
  path: "src/main/java/App.java",
  line: 42
});

// Perform refactoring
await jetbrainsMCP.refactor({
  type: "rename",
  element: "oldMethodName",
  newName: "newMethodName",
  scope: "project"
});

// Run inspections
const issues = await jetbrainsMCP.runInspections({
  scope: "project",
  profile: "Project Default"
});

// Execute build
await jetbrainsMCP.runTask({
  task: "build",
  configuration: "Production"
});

// Debug application
await jetbrainsMCP.startDebugger({
  configuration: "Application",
  breakpoints: ["App.java:25", "Service.java:100"]
});
```

## Business Value

### Key Benefits
- Seamless IDE integration for AI workflows
- Leverage full IDE intelligence and features
- Maintain code quality with IDE inspections
- Accelerate development with AI assistance
- Enterprise-ready with JetBrains support

### ROI Metrics
- 60% faster code refactoring
- 80% reduction in context switching
- 90% accuracy in code modifications
- Full IDE feature accessibility