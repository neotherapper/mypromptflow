# General MCP Integration Template for AI Subagents

This template provides standardized patterns for integrating MCP servers into AI subagent configurations. Use this as a foundation and customize for specific domains and server types.

## Template Structure

### 1. MCP Server Integration Section (Add to Core Responsibilities)

```markdown
**MCP Server Integration:**
- Leverage {MCP_SERVER_NAME} ({TIER_LEVEL}) for real-time {DOMAIN_SPECIFIC} information
- Integrate {SPECIFIC_USE_CASES} through MCP server APIs
- Implement fallback strategies when MCP server is unavailable
- Validate recommendations against current {DOMAIN} capabilities and constraints
- Monitor MCP server performance and implement caching strategies
- Handle authentication and rate limiting appropriately
- Provide context-aware error messages when integration fails
```

### 2. MCP Tools Configuration

```yaml
# Add to subagent frontmatter tools section
tools: Read, Grep, Glob, {DOMAIN_SPECIFIC_TOOLS}, {MCP_SERVER_TOOLS}

# Example for AWS integration:
tools: Read, Grep, Glob, WebSearch, mcp__AWS__describe_instances, mcp__AWS__list_s3_buckets
```

### 3. Integration Implementation Pattern

```markdown
## MCP Server Integration Implementation

### Primary MCP Server: {MCP_SERVER_NAME}
- **Tier Level**: {TIER_1/2/3} ({COMPOSITE_SCORE}/10)
- **Setup Complexity**: {MINIMAL/MODERATE/HIGH}
- **Integration Priority**: {HIGH/MEDIUM/LOW}

### Core Integration Capabilities:
{LIST_SPECIFIC_CAPABILITIES}

### Usage Patterns:
1. **Real-time Information Retrieval**:
   - Query {MCP_SERVER_NAME} for current {DOMAIN_SPECIFIC} data
   - Cross-reference with cached knowledge for completeness
   - Provide recommendations based on latest information

2. **Validation and Verification**:
   - Validate architectural/technical recommendations against current capabilities
   - Check compatibility and dependencies in real-time
   - Ensure recommendations align with latest best practices

3. **Error Handling and Fallback**:
   - Implement circuit breaker pattern for server reliability
   - Graceful degradation to cached information when server unavailable
   - Clear error messages explaining integration status

### Implementation Example:
```python
# Example MCP server integration pattern
async def get_current_{DOMAIN}_info(query_context):
    try:
        # Primary: Query MCP server for real-time data
        mcp_result = await {MCP_SERVER_NAME}.query(query_context)
        
        # Enhance with domain expertise
        enhanced_result = apply_domain_expertise(mcp_result)
        
        return {
            "status": "success",
            "source": "mcp_server_real_time",
            "data": enhanced_result,
            "timestamp": datetime.now(),
            "server_health": "operational"
        }
        
    except MCPServerError as e:
        # Fallback to cached knowledge
        fallback_result = get_cached_domain_knowledge(query_context)
        
        return {
            "status": "fallback_mode",
            "source": "cached_knowledge", 
            "data": fallback_result,
            "timestamp": datetime.now(),
            "server_health": "unavailable",
            "error_message": f"MCP server temporarily unavailable: {e}"
        }
```

### Quality Standards:
- Always provide source attribution (MCP server vs cached knowledge)
- Include timestamp information for data freshness
- Implement appropriate caching strategies (TTL: {RECOMMENDED_TTL})
- Monitor and log MCP server performance metrics
- Validate data quality and consistency before providing recommendations
```

## Domain-Specific Customization Guide

### Cloud Infrastructure (AWS/Azure/GCP)
- Focus on real-time service availability and pricing
- Include capacity planning and resource optimization
- Validate against current service limits and quotas
- Monitor costs and provide optimization recommendations

### Development Tools (GitHub/Docker/CI/CD)
- Real-time repository status and branch information
- Current build and deployment pipeline status
- Security vulnerability and dependency updates
- Integration with latest development best practices

### Database Systems (PostgreSQL/Redis/MongoDB)
- Current performance metrics and optimization opportunities
- Schema validation against latest database capabilities
- Real-time connection and resource utilization
- Backup and recovery status validation

### Analytics & Data Science (Google Analytics/Qdrant)
- Real-time data processing and analysis capabilities
- Current model performance and accuracy metrics
- Data pipeline health and processing status
- Integration with latest ML/AI model capabilities

## Implementation Checklist

### Pre-Integration Setup
- [ ] Verify MCP server tier level and composite score meet quality thresholds
- [ ] Confirm setup complexity aligns with team capabilities
- [ ] Review integration priority against project requirements
- [ ] Validate authentication and access requirements

### Integration Implementation
- [ ] Add MCP server tools to subagent configuration
- [ ] Implement primary integration patterns for domain-specific use cases
- [ ] Create comprehensive error handling and fallback strategies
- [ ] Add appropriate caching and performance optimization
- [ ] Include monitoring and health check mechanisms

### Quality Validation
- [ ] Test integration with both successful and failed MCP server responses
- [ ] Validate fallback behavior when server is unavailable
- [ ] Confirm error messages are clear and actionable
- [ ] Verify caching strategies work appropriately
- [ ] Test performance under various load conditions

### Documentation and Maintenance
- [ ] Document all MCP server integration points
- [ ] Create troubleshooting guide for common integration issues
- [ ] Establish monitoring and alerting for integration health
- [ ] Plan regular reviews of integration effectiveness
- [ ] Document upgrade and maintenance procedures

## Best Practices

### Authentication and Security
- Use environment variables for API keys and authentication tokens
- Implement token rotation and refresh mechanisms where supported
- Follow principle of least privilege for MCP server permissions
- Encrypt sensitive configuration data
- Regular security audits of integration points

### Performance and Reliability
- Implement intelligent caching with appropriate TTL values
- Use circuit breaker patterns for unreliable servers
- Batch operations where supported to minimize API calls
- Monitor response times and implement optimization strategies
- Plan for graceful degradation during high load periods

### Monitoring and Observability
- Track MCP server response times and error rates
- Implement health checks for critical integration points
- Log integration usage patterns for optimization insights
- Set up alerting for integration failures and performance degradation
- Regular reporting on integration effectiveness and ROI

### Maintenance and Evolution
- Regular review of MCP server capabilities and new features
- Update integration patterns based on server improvements
- Monitor for deprecated APIs and plan migration strategies
- Keep fallback knowledge current and validated
- Plan for scaling integration as usage grows

This template ensures consistent, reliable, and maintainable MCP server integration across all AI subagents while providing domain-specific value and maintaining high quality standards.