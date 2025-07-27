---
api_version: Linear GraphQL API v2023
authentication_types:
- API Token
- Personal Access Token
- OAuth 2.0
category: Project Management
description: Modern project management and issue tracking integration server for
  development teams. High-priority server for agile development workflows, team
  productivity, and automated project coordination through MCP.
estimated_setup_time: 10-15 minutes
id: a8b9c7d6-2e4f-4a91-8c3d-5f7e9b1a3c5d
installation_priority: 1
item_type: mcp_server
migration_date: '2025-07-27'
name: Linear MCP Server
original_file: mcp-registry/detailed-profiles/tier-1/linear-server-profile.md
priority: 1st_priority
production_readiness: 85
provider: Community
quality_score: 8.35
repository_url: https://github.com/jerhadf/linear-mcp-server
setup_complexity: Simple
source_database: tools_services
status: active
tags:
- MCP Server
- Project Management
- Issue Tracking
- Agile Development
- Team Productivity
- Workflow Automation
- Tier 1
- Development Tools
- mcp-server
- tier-1
- linear
tier: Tier 1
transport_protocols:
- Linear GraphQL API
- Webhook Integration
- Real-time Updates
information_capabilities:
  data_types:
  - issue_data
  - project_metadata
  - team_information
  - sprint_data
  - milestone_tracking
  - user_assignments
  - workflow_states
  - comment_threads
  - priority_levels
  - label_systems
  access_methods:
  - real-time
  - batch
  - on-demand
  - webhook
  authentication: required
  rate_limits: medium
  complexity_score: 4
  typical_use_cases:
  - "Create and manage development issues with automated workflow transitions"
  - "Track project progress and sprint planning with team capacity management"
  - "Generate development team performance analytics and velocity reports"
  - "Automate issue creation from various triggers and external systems"
  - "Coordinate team workflows with status updates and assignment management"
  - "Integrate development workflows with GitHub/GitLab for complete visibility"
  - "Monitor team productivity and project delivery timelines"
mcp_profile_reference: "@mcp_profile/linear-server"
---

**Modern project management and issue tracking integration for development teams through MCP**

## 📋 Basic Information

| Field | Value |
|-------|-------|
| **Provider** | Community |
| **Category** | Project Management |
| **Production Readiness** | 85% |
| **Setup Complexity** | Simple (4/10) |
| **Repository** | [Linear MCP Server](https://github.com/jerhadf/linear-mcp-server) |

## 📊 Information Access Capabilities  

### Primary Information Types
- **Issue Management**: Complete issue lifecycle from creation to resolution with automated workflows
- **Project Tracking**: Sprint planning, backlog management, and milestone progress monitoring
- **Team Productivity**: Individual and team performance analytics with velocity tracking
- **Workflow Automation**: Status transitions, assignment rules, and notification systems
- **Integration Data**: GitHub/GitLab integration with commit linking and deployment tracking
- **Reporting Analytics**: Team metrics, burndown charts, and productivity insights

### Access Patterns
- **Real-time Updates**: Live issue status changes and team collaboration events
- **Batch Operations**: Bulk issue management, data imports, and reporting generation
- **Webhook Integration**: Event-driven automation and external system synchronization
- **On-demand Queries**: Specific issue searches, team performance queries, and project analytics

### Authentication & Security
- **Authentication Required**: Linear API token with workspace-level permissions
- **Rate Limits**: Medium (GraphQL-based with query complexity considerations)
- **Permissions**: Team-based access control with role-specific data visibility
- **Security**: OAuth 2.0 support with enterprise SSO integration capabilities

## 🚀 Core Capabilities & Features

### Issue Management
- **Complete Lifecycle**: Create, update, assign, and resolve issues with automated state transitions
- **Advanced Filtering**: Complex queries across projects, teams, and time periods
- **Bulk Operations**: Mass updates, imports, and workflow automation

### Project Coordination
- **Sprint Planning**: Capacity management, story point estimation, and sprint goal tracking
- **Milestone Management**: Project roadmap planning with dependency tracking
- **Team Analytics**: Velocity monitoring, completion rates, and productivity metrics

### Workflow Automation
- **Status Automation**: Automatic issue transitions based on triggers and conditions
- **Assignment Rules**: Intelligent issue routing based on team capacity and expertise
- **Notification Systems**: Custom alerts for project stakeholders and team members

### Development Integration
- **Version Control**: GitHub and GitLab integration with automatic issue linking
- **Deployment Tracking**: Release management with feature delivery monitoring
- **Code Review**: Pull request integration with issue resolution workflows

### Reporting & Analytics
- **Team Performance**: Individual and team productivity metrics with trend analysis
- **Project Insights**: Delivery timelines, scope changes, and quality metrics
- **Custom Dashboards**: Configurable reporting for stakeholders and management

### Typical Use Cases for AI Agents
- **Automated Issue Creation**: "Create issues from customer feedback, bug reports, and feature requests"
- **Sprint Planning**: "Analyze team velocity and recommend sprint capacity allocation"
- **Progress Monitoring**: "Generate daily standup reports and project status updates"
- **Team Coordination**: "Automatically assign issues based on team expertise and workload"
- **Quality Tracking**: "Monitor bug resolution times and feature delivery metrics"
- **Workflow Optimization**: "Identify bottlenecks and recommend process improvements"