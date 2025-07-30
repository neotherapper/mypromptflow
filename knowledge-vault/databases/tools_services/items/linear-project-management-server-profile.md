---
description: 'Modern issue tracking and project management platform with streamlined workflows. Strategic development server for agile teams providing high-performance issue tracking, project planning, and team collaboration with minimalist design principles.'
id: 7e30e977-7c74-493d-b713-d49cca08538b
installation_priority: 3
item_type: mcp_server
migration_date: '2025-07-27'
name: Linear Project Management MCP Server
<<<<<<< HEAD
original_file: projects/universal-topic-intelligence-system/mcp-registry/detailed-profiles/tier-2/linear-project-management-server-profile.md
=======
original_file: projects/ai-knowledge-intelligence-orchestrator/mcp-registry/detailed-profiles/tier-2/linear-project-management-server-profile.md
>>>>>>> origin/master
priority: 2nd_priority
production_readiness: 92
quality_score: 8.4
source_database: tools_services
status: active
tags:
- MCP Server
- Tier 2
- Project Management
- Issue Tracking
- Agile Development
- Modern Workflow
- API Service
- Team Collaboration
- High Performance
- Developer Tools
mcp_profile_reference: "@mcp_profile/linear-project-management"
information_capabilities:
  access_methods:
    - method: "Linear GraphQL API"
      protocol: "GraphQL over HTTPS"
      authentication: "API Key / OAuth 2.0"
      rate_limits: "5,000 requests/hour"
      data_format: "JSON"
    - method: "Webhook integration"
      protocol: "HTTP POST"
      authentication: "Secret-based verification"
      rate_limits: "Event-driven"
      data_format: "JSON events"
  information_types:
    - type: "Issue Data"
      scope: "Issues, projects, teams, cycles with complete metadata"
      update_frequency: "Real-time"
      quality_score: 98
      validation_method: "GraphQL schema validation"
    - type: "Project Analytics"
      scope: "Velocity metrics, burndown charts, team performance"
      update_frequency: "Real-time"
      quality_score: 95
      validation_method: "Analytics engine validation"
    - type: "Workflow States"
      scope: "Issue states, transitions, assignments, priorities"
      update_frequency: "Real-time"
      quality_score: 97
      validation_method: "State machine validation"
  decision_support:
    use_for_fact_checking: false
    use_for_research: false
    use_for_analysis: true
    reliability_score: 96
    coverage_assessment: "Comprehensive for modern project management"
    bias_considerations: "Team workflow and process dependent"
  integration_complexity: 5
  setup_requirements:
    - "Linear workspace access"
    - "API key or OAuth application setup"
    - "Team and project permissions"
    - "Webhook endpoint configuration (optional)"
---

## Header Classification
**Tier**: 2 (Strategic Priority - Modern Project Management Platform)
**Server Type**: Issue Tracking & Agile Project Management Platform
**Business Category**: Development & Team Productivity Tools
**Implementation Priority**: Medium-High (Strategic Value for Modern Development Teams)

## Technical Specifications

### Core Capabilities
- **Issue Management**: Streamlined issue creation, tracking, and resolution with intelligent automation
- **Project Planning**: Roadmap visualization, milestone tracking, and release planning with timeline views
- **Team Collaboration**: Real-time updates, notifications, and team communication with status visibility
- **Workflow Automation**: Custom workflows, smart assignments, and automated state transitions
- **Analytics & Insights**: Velocity tracking, burndown charts, and team performance analytics
- **Integration Ecosystem**: Seamless integrations with GitHub, Slack, Figma, and development tools

### API Interface Standards
- **Protocol**: GraphQL API with comprehensive query and mutation support
- **Authentication**: API key-based or OAuth 2.0 with team-level permissions
- **Rate Limits**: 5,000 requests/hour with generous burst allowances
- **Data Format**: JSON with strongly-typed GraphQL schema
- **Real-time Updates**: WebSocket subscriptions for live data synchronization

### System Requirements
- **Linear Workspace**: Active Linear workspace with appropriate team access
- **Authentication**: Valid API key or OAuth application credentials
- **Network**: HTTPS connectivity to Linear API endpoints
- **Permissions**: Team member or admin permissions for full functionality
- **Storage**: Minimal local storage for authentication and configuration

## Business Value & Strategic Implementation

The Linear Project Management MCP Server provides exceptional value for modern development teams requiring high-performance issue tracking and streamlined project management. With its GraphQL API and real-time capabilities, it enables sophisticated automation and integration workflows while maintaining simplicity and speed.