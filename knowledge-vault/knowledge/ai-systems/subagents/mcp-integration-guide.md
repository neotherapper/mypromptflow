# MCP Integration Guide for AI Subagents

## Core Requirement: Use MCP Servers When Available

**MANDATORY**: All AI subagents MUST use MCP servers when they are available and applicable to their domain. This requirement ensures real-time capabilities, enhanced functionality, and optimal performance across all AI operations.

## MCP Server Priority Framework

### Tier 1: Production-Ready Servers (Must Use)
**Integration Priority: HIGH** - Immediate deployment required

- **GitHub** (Score: 8.65/10) - Repository intelligence, security scanning, CI/CD integration
- **JIRA** (Score: 8.0+/10) - Project management, issue tracking, maritime workflow automation
- **Fetch** (Score: 9.65/10) - Web content retrieval, API data fetching, real-time information
- **Memory** (Score: 9.65/10) - Session state management, context preservation
- **Docker** (Score: 8.5/10) - Container management, security scanning, optimization
- **PostgreSQL** (Score: 8.0/10) - Database operations, schema design, query optimization
- **Redis** (Score: 9.18/10) - Caching strategies, session management, performance optimization

### Tier 2: Strategic Implementation Servers
**Integration Priority: MEDIUM** - Implement based on specific use cases

- **AWS** (Score: 6.4/10) - Infrastructure management, cost optimization, security validation
- **Slack** (Score: 8.0/10) - Team communication, workflow notifications
- **Google Analytics** (Score: 8.65/10) - User behavior analysis, performance metrics

### Tier 3: Specialized Use Cases
**Integration Priority: LOW** - Complex setup, niche applications

- **Figma** (Score: 7.2/10) - Design system integration, UI/UX workflows

## Domain-Specific MCP Integration Requirements

### Frontend Development Domain
**Required MCP Servers:**
- GitHub (repository analysis, security scanning)
- Browser automation tools (performance testing, UI validation)
- Fetch (external API testing, documentation retrieval)

**Configuration Pattern:**
```yaml
tools: Read, Grep, Glob, WebSearch, mcp__MCP_DOCKER__get_file_contents, mcp__MCP_DOCKER__search_repositories, mcp__MCP_DOCKER__browser_snapshot, mcp__MCP_DOCKER__browser_take_screenshot
```

### Database Systems Domain
**Required MCP Servers:**
- PostgreSQL (schema operations, query optimization)
- Redis (caching strategy design)
- GitHub (version control for database migrations)

**Configuration Pattern:**
```yaml
tools: Read, Grep, Glob, Edit, Bash, mcp__MCP_DOCKER__search_repositories, mcp__MCP_DOCKER__get_file_contents
```

### Security Systems Domain
**Required MCP Servers:**
- GitHub (security scanning, vulnerability analysis)
- Fetch (vulnerability database access, security documentation)

**Configuration Pattern:**
```yaml
tools: Read, Grep, Glob, WebSearch, mcp__MCP_DOCKER__get_file_contents, mcp__MCP_DOCKER__list_secret_scanning_alerts, mcp__MCP_DOCKER__list_code_scanning_alerts, mcp__MCP_DOCKER__list_dependabot_alerts
```

### API Integration Domain
**Required MCP Servers:**
- JIRA (workflow automation, issue management)
- GitHub (repository integration, CI/CD coordination)
- Fetch (external API testing, integration validation)

**Configuration Pattern:**
```yaml
tools: Read, Write, Bash, WebSearch, mcp__MCP_DOCKER__jira_*, mcp__MCP_DOCKER__fetch, mcp__MCP_DOCKER__get_file_contents, mcp__MCP_DOCKER__search_repositories
```

## Error Handling and Fallback Strategies

### Circuit Breaker Pattern Implementation
All MCP integrations MUST implement circuit breaker patterns:

```python
class MCPIntegrationPattern:
    def __init__(self):
        self.circuit_breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=180)
        self.cache_ttl = 300  # 5 minutes default
        
    async def query_with_fallback(self, mcp_operation, params):
        if self.circuit_breaker.is_open():
            return self.get_cached_knowledge(mcp_operation, params)
            
        try:
            result = await self.circuit_breaker.call(mcp_operation, params)
            self.cache_result(mcp_operation, params, result)
            return result
        except MCPError as e:
            self.log_mcp_error(mcp_operation, e)
            return self.get_cached_knowledge(mcp_operation, params, error=e)
```

### Graceful Degradation Requirements
1. **Always provide fallback**: When MCP server unavailable, use cached knowledge
2. **Log all failures**: Track MCP server availability and performance
3. **User transparency**: Inform users when operating in fallback mode
4. **Recovery monitoring**: Automatically retry failed MCP connections

## Performance Standards and Monitoring

### Response Time Requirements
- **MCP Query Response**: < 3 seconds for standard operations
- **Cache Hit Rate**: > 85% for repeated queries
- **Error Rate**: < 2% for MCP server interactions
- **Fallback Success**: > 96% successful fallback to cached knowledge

### Monitoring Implementation
```yaml
# Required monitoring for all MCP integrations
monitoring:
  response_times: track_all_mcp_calls
  error_rates: alert_on_failure_threshold
  cache_performance: optimize_cache_hit_rates
  fallback_usage: monitor_degraded_operations
```

## Security and Compliance Standards

### Authentication Management
- **Environment Variables**: All MCP server credentials via secure environment variables
- **Token Rotation**: Implement automatic token refresh where supported
- **Least Privilege**: Grant minimal required permissions for each MCP server
- **Audit Logging**: Log all MCP server interactions for security compliance

### Maritime Insurance Compliance
- **Data Protection**: Ensure MCP servers handle maritime data according to GDPR/regulations
- **Audit Trails**: Maintain comprehensive logs for regulatory compliance
- **Access Control**: Implement role-based access for sensitive maritime operations
- **Data Residency**: Ensure MCP operations comply with maritime data locality requirements

## Implementation Checklist

### For New Subagents
- [ ] Identify applicable MCP servers based on domain mapping
- [ ] Configure tools with appropriate MCP server functions
- [ ] Implement circuit breaker and fallback strategies
- [ ] Add error handling and logging
- [ ] Test MCP integration functionality
- [ ] Validate fallback behavior
- [ ] Update documentation with MCP capabilities

### For Existing Subagents
- [ ] Audit current tool configuration for missing MCP integration
- [ ] Update frontmatter with required MCP tools
- [ ] Enhance core responsibilities with MCP integration section
- [ ] Implement error handling patterns
- [ ] Test integration and fallback scenarios
- [ ] Update team collaboration protocols

## Quality Assurance Standards

### Integration Testing Requirements
- **MCP Server Connectivity**: Verify all configured MCP servers are accessible
- **Error Handling**: Test circuit breaker and fallback behavior
- **Performance**: Validate response times meet requirements
- **Security**: Ensure secure authentication and data handling

### Continuous Monitoring
- **Health Checks**: Regular MCP server availability verification
- **Performance Metrics**: Response time and error rate tracking
- **Usage Analytics**: Monitor MCP integration effectiveness
- **Security Audits**: Regular review of MCP server permissions and access patterns

## Migration Strategy for Legacy Subagents

### Phase 1: Critical Tool Configuration (Completed)
- Maritime-specific agents: react-maritime-frontend, postgresql-maritime-specialist, api-integration-specialist, security-code-reviewer, fullstack-performance-optimizer
- Validation agent: claude-agent-validator

### Phase 2: Domain-Specific MCP Integration
- Implement cross-domain patterns for fullstack agents
- Add specialized MCP capabilities for maritime workflows
- Enhance error handling and monitoring

### Phase 3: Advanced Features
- Custom MCP server integration for maritime-specific APIs
- Advanced caching and performance optimization
- Real-time maritime data integration patterns

---

**Remember**: MCP server integration is not optional - it is a core requirement for all AI subagents. When MCP servers are available and applicable to your domain, they MUST be used to provide enhanced real-time capabilities, improved accuracy, and optimal performance.