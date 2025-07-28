# MCP Integration Patterns - Shared Instructions

**Purpose**: Standardized integration patterns for WorkOS, JIRA, and Sentry MCP servers across AI agents and SDLC workflows.

**Usage**: Referenced by:
- All SDLC stage subagents requiring external tool integration
- Authentication and identity management workflows
- Project management and issue tracking automation
- Error monitoring and performance tracking systems

## Core MCP Integration Framework

### 1. WorkOS B2B Authentication Integration

**WorkOS MCP Server Configuration**:
```yaml
workos_integration:
  server_profile: "workos-b2b-authentication-server-profile.md"
  composite_score: 8.1
  category: "b2b-authentication"
  key_capabilities:
    - Single Sign-On (SSO) implementation
    - Organization-based access control
    - Directory synchronization
    - Multi-factor authentication (MFA)
    - User provisioning and deprovisioning
```

**Authentication Workflow Patterns**:
```yaml
authentication_patterns:
  sso_implementation:
    description: "Implement organization-level SSO authentication"
    use_cases:
      - User login and session management
      - Organization-based access control
      - Administrative user management
      - Team member authentication workflows
    
    integration_steps:
      - Configure WorkOS organization settings
      - Implement SSO callback handling
      - Set up session management with secure tokens
      - Configure organization-based routing
    
    security_considerations:
      - Secure token storage and validation
      - Session timeout and refresh handling
      - Organization isolation and data security
      - Audit logging for authentication events
  
  directory_sync:
    description: "Synchronize user data with organization directories"
    capabilities:
      - Automatic user provisioning
      - Role and permission synchronization
      - Team structure mapping
      - Deactivation workflow automation
    
    implementation_pattern:
      - Set up directory connection (Active Directory, Google Workspace)
      - Configure user attribute mapping
      - Implement real-time synchronization
      - Handle user lifecycle events
```

**WorkOS Integration Code Patterns**:
```yaml
workos_code_patterns:
  authentication_middleware:
    typescript_example: |
      // Secure authentication validation
      export const workosAuth = async (req: Request, res: Response, next: NextFunction) => {
        try {
          const session = await workos.userManagement.loadSealedSession({
            sessionData: req.cookies['wos-session'],
            cookiePassword: process.env.COOKIE_PASSWORD!
          });
          req.user = session.user;
          req.organization = session.organization;
          next();
        } catch (error) {
          res.status(401).json({ error: 'Unauthorized' });
        }
      };
  
  organization_access_control:
    validation_pattern: |
      // Ensure user belongs to correct organization
      const validateOrganizationAccess = (requiredOrgId: string) => {
        return (req: AuthenticatedRequest, res: Response, next: NextFunction) => {
          if (req.organization?.id !== requiredOrgId) {
            return res.status(403).json({ error: 'Organization access denied' });
          }
          next();
        };
      };
```

### 2. JIRA Project Management Integration

**JIRA MCP Server Configuration**:
```yaml
jira_integration:
  server_profile: "jira-server-profile.md"
  category: "project-management"
  key_capabilities:
    - Issue creation and management
    - Sprint planning and tracking
    - Workflow automation
    - Custom field management
    - Reporting and analytics
```

**Project Management Workflow Patterns**:
```yaml
jira_workflow_patterns:
  automated_ticket_creation:
    description: "Create JIRA tickets from requirements analysis"
    triggers:
      - Stage 1: Requirements gathering completion
      - Bug reports from Sentry integration
      - Feature requests from stakeholder input
    
    ticket_creation_pattern:
      - Extract requirement details and acceptance criteria
      - Determine appropriate issue type (Story, Task, Bug, Epic)
      - Assign to appropriate team member based on skill set
      - Set priority based on business impact assessment
      - Link related issues and dependencies
    
    automation_rules:
      - Auto-assign based on component/area expertise
      - Set sprint based on capacity planning
      - Add labels for tracking and categorization
      - Create subtasks for complex stories
  
  sprint_planning_automation:
    description: "AI-assisted sprint planning with capacity management"
    planning_workflow:
      - Analyze team capacity and availability
      - Evaluate story complexity and effort estimation
      - Balance workload across team members
      - Identify and resolve dependency conflicts
      - Generate sprint goals and success criteria
    
    capacity_calculation:
      - Account for team member availability
      - Factor in historical velocity data
      - Consider story complexity and risk factors
      - Include buffer for unforeseen issues
```

**JIRA Integration Code Patterns**:
```yaml
jira_automation_patterns:
  issue_creation:
    python_example: |
      # Automated JIRA issue creation from requirements
      async def create_feature_issues(requirements: RequirementAnalysis) -> List[JiraIssue]:
          issues = []
          
          # Create Epic for major feature
          epic = await jira_client.create_issue({
              'project': {'key': 'VANGUARD'},
              'issuetype': {'name': 'Epic'},
              'summary': requirements.feature_name,
              'description': requirements.business_value,
              'labels': ['ai-generated', requirements.priority]
          })
          
          # Create stories for each requirement
          for req in requirements.user_stories:
              story = await jira_client.create_issue({
                  'project': {'key': 'VANGUARD'},
                  'issuetype': {'name': 'Story'},
                  'summary': req.title,
                  'description': req.acceptance_criteria,
                  'parent': {'key': epic.key},
                  'assignee': {'accountId': req.assigned_developer},
                  'priority': {'name': req.priority}
              })
              issues.append(story)
          
          return issues
  
  workflow_automation:
    status_transitions: |
      # Automated status transitions based on development progress
      async def update_issue_status(issue_key: str, git_event: GitEvent):
          if git_event.type == 'branch_created':
              await transition_issue(issue_key, 'In Progress')
          elif git_event.type == 'pr_opened':
              await transition_issue(issue_key, 'In Review')
          elif git_event.type == 'pr_merged':
              await transition_issue(issue_key, 'Done')
              await add_comment(issue_key, f"Completed in PR #{git_event.pr_number}")
```

### 3. Sentry Error Monitoring Integration

**Sentry MCP Server Configuration**:
```yaml
sentry_integration:
  server_profile: "sentry-official-server-profile.md"
  composite_score: 9.3
  category: "error-monitoring"
  key_capabilities:
    - Real-time error tracking
    - Performance monitoring
    - Release tracking and comparison
    - User feedback collection
    - Alert management and routing
```

**Error Monitoring Workflow Patterns**:
```yaml
sentry_monitoring_patterns:
  automated_error_tracking:
    description: "Comprehensive error monitoring across application layers"
    monitoring_scope:
      - Frontend React application errors
      - Backend FastAPI service errors
      - Database connection and query errors
      - External API integration failures
      - Authentication and authorization errors
    
    error_classification:
      - Critical: Security vulnerabilities, data corruption
      - High: Feature-breaking errors, performance issues
      - Medium: Non-blocking functionality issues
      - Low: UI glitches, minor performance impacts
    
    response_automation:
      - Auto-create JIRA tickets for critical errors
      - Alert relevant team members based on error type
      - Trigger rollback procedures for release issues
      - Generate investigation reports for complex errors
  
  performance_monitoring:
    description: "Track application performance and user experience"
    metrics_tracking:
      - Page load times and Core Web Vitals
      - API response times and database query performance
      - User interaction tracking and conversion funnels
      - Resource usage and memory leak detection
    
    optimization_triggers:
      - Performance regression detection
      - Resource usage threshold alerts
      - User experience impact assessment
      - Automated performance testing integration
```

**Sentry Integration Code Patterns**:
```yaml
sentry_implementation_patterns:
  error_context_enrichment:
    typescript_example: |
      // Enrich error context with user and business data
      Sentry.configureScope((scope) => {
        scope.setUser({
          id: user.id,
          email: user.email,
          organization: user.organization?.name
        });
        
        scope.setContext('business_context', {
          feature: 'policy_calculation',
          maritime_data_source: 'lloyd_registry',
          calculation_type: 'premium_assessment'
        });
        
        scope.setTag('user_role', user.role);
        scope.setTag('organization_tier', user.organization?.tier);
      });
  
  automated_issue_creation:
    integration_pattern: |
      # Sentry webhook to JIRA automation
      async def handle_sentry_issue(sentry_event: SentryWebhookEvent):
          if sentry_event.level in ['error', 'fatal']:
              # Create JIRA ticket for tracking
              jira_issue = await create_jira_issue({
                  'project': 'VANGUARD',
                  'issue_type': 'Bug',
                  'summary': f"Sentry Error: {sentry_event.title}",
                  'description': generate_error_description(sentry_event),
                  'priority': map_sentry_level_to_priority(sentry_event.level),
                  'labels': ['sentry-generated', 'production-error']
              })
              
              # Link Sentry issue to JIRA ticket
              await update_sentry_issue(sentry_event.issue_id, {
                  'external_issue': jira_issue.key
              })
```

## SDLC Stage Integration Patterns

### Stage 1: Business Ideation & Requirements
```yaml
stage1_mcp_integration:
  jira_usage:
    - Create Epic from business requirements
    - Generate user stories with acceptance criteria
    - Set up project structure and components
    - Initialize sprint planning framework
  
  workos_preparation:
    - Define user roles and permissions for new features
    - Plan organization-level access controls
    - Prepare authentication flow requirements
```

### Stage 4: Implementation
```yaml
stage4_mcp_integration:
  development_tracking:
    jira_integration:
      - Auto-transition issues based on git branch activity
      - Update story points and time tracking
      - Link commits and pull requests to issues
      - Generate development progress reports
    
    sentry_setup:
      - Configure error tracking for new features
      - Set up performance monitoring baselines
      - Implement custom error context for new functionality
      - Prepare alert rules for new components
  
  workos_implementation:
    - Implement authentication flows with proper error handling
    - Set up organization-based feature flags
    - Configure user session management
    - Implement audit logging for security events
```

### Stage 5: Testing & Quality Assurance
```yaml
stage5_mcp_integration:
  quality_monitoring:
    sentry_testing:
      - Monitor error rates during testing phases
      - Track performance regressions in test environments
      - Validate error handling and recovery procedures
      - Generate quality assessment reports
    
    jira_test_tracking:
      - Create test execution reports
      - Track defect resolution progress
      - Link test cases to user stories
      - Generate quality metrics dashboards
```

### Stage 6: Deployment & Monitoring
```yaml
stage6_mcp_integration:
  production_monitoring:
    sentry_deployment:
      - Set up release tracking and comparison
      - Configure production alert thresholds
      - Implement user feedback collection
      - Monitor deployment success metrics
    
    jira_release_management:
      - Auto-close completed issues in releases
      - Generate release notes from JIRA tickets
      - Track post-deployment issues and hotfixes
      - Update project velocity and planning metrics
```

## Integration Quality Assurance

### Security Best Practices
```yaml
security_standards:
  credential_management:
    - Store API keys and tokens in secure environment variables
    - Use encrypted storage for sensitive configuration
    - Implement token rotation and refresh procedures
    - Monitor and audit API access patterns
  
  data_privacy:
    - Ensure PII protection in error reports and logs
    - Implement data retention policies across all integrations
    - Configure secure data transmission (HTTPS/TLS)
    - Validate compliance with GDPR and maritime regulations
```

### Performance Optimization
```yaml
performance_patterns:
  api_efficiency:
    - Implement request batching for bulk operations
    - Use caching for frequently accessed data
    - Configure appropriate timeout and retry policies
    - Monitor API rate limits and usage patterns
  
  resource_management:
    - Optimize webhook processing for real-time events
    - Implement efficient data synchronization
    - Use background jobs for heavy integration tasks
    - Monitor integration performance and resource usage
```

## Implementation Guidelines

**Framework Compliance**: Follows AI Agent Instruction Design Excellence:
- **Concrete Integration Patterns**: Specific MCP server usage and code examples
- **Security-First Approach**: Comprehensive security considerations for each integration
- **Performance Optimized**: Efficient integration patterns for production use
- **SDLC-Aware**: Stage-specific integration requirements and workflows

**Quality Standards**:
- All integrations include comprehensive error handling
- Security best practices enforced across all MCP server interactions
- Performance monitoring and optimization built into integration patterns
- Compliance with maritime industry regulations and data privacy requirements

This MCP integration framework ensures consistent, secure, and efficient integration with WorkOS, JIRA, and Sentry across all SDLC stages and AI agent workflows.