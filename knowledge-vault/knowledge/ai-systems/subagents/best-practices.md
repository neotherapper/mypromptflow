# Claude Subagent Best Practices: AI-Generated Blueprint System

This guide provides comprehensive best practices for Claude Code subagents based on empirical analysis of AI-generated patterns, proven effectiveness standards, and official Claude Code documentation for automatic delegation, team collaboration, and enterprise integration.

## AI-Generated Blueprint Foundation

Claude Code subagents achieve maximum effectiveness when following AI-generated structural patterns that have been systematically analyzed and validated. This approach prioritizes automatic delegation optimization, team collaboration, and clear behavioral directives for professional development workflows.

### Core Blueprint Principles

**Universal Opening Pattern**: All effective subagents follow "You are a [ROLE] with [EXPERTISE]" structure with clear mission statements focusing on measurable outcomes.

**Structured Responsibilities**: 4-6 technical categories with 4-7 specific, actionable responsibilities each, covering technology-specific, process-oriented, domain-focused, and collaboration aspects.

**Assessment Instructions**: Critical ending section with behavioral directives ("Always" or "When" patterns), specific deliverable requirements, business alignment, and coordination protocols.

### Automatic Delegation Integration

**Claude Code's Intelligent Routing**: Claude automatically delegates tasks to appropriate subagents based on context analysis, description matching, and usage patterns.

**Optimization Strategies**:
- **Keyword-Rich Descriptions**: Include technical terms, action verbs, and domain keywords that match user intents
- **Context Triggers**: Reference common problem scenarios (performance issues, security concerns, deployment challenges)
- **Example-Driven Definitions**: Provide realistic usage examples that demonstrate delegation scenarios

**Team Collaboration Patterns**:
- **Project-Level Priority**: Store team subagents in `.claude/agents/` for shared access and highest delegation priority
- **User-Level Fallbacks**: Personal optimizations in `~/.claude/agents/` for individual workflow enhancement
- **Version Control Integration**: Track project subagents with codebase for team consistency

## Valid Configuration Properties

Based on Claude Code specification analysis, subagents support ONLY these frontmatter properties:

```yaml
---
name: subagent-identifier           # Required: kebab-case identifier
description: "Usage criteria..."    # Required: When to use with examples
tools: Read, Grep, Glob            # Optional: Minimal necessary tools
priority: high                     # Optional: high/medium/low
team: development                  # Optional: Team assignment
environment: production            # Optional: Environment-specific
---
```

**CRITICAL**: Properties like `sdlc_stage`, `context_isolation`, `framework_integration` are fabricated and DO NOT exist in Claude Code. Remove these from all configurations.

## Structural Pattern Requirements

### Opening Structure
```
You are a [SPECIFIC ROLE TITLE] with deep expertise in [TECHNICAL STACK + DOMAIN]. Your mission is to [CLEAR OBJECTIVE WITH MEASURABLE OUTCOMES].
```

**Examples from AI-generated patterns**:
- "You are a Full-Stack Performance Optimization Specialist with deep expertise in React/FastAPI/PostgreSQL applications"
- "You are a Security Code Review Specialist with deep expertise in OWASP Top 10 vulnerabilities, secure coding practices"

### Core Responsibilities Organization

**Section Header**: `## Core Responsibilities`

**Category Structure**:
```
**Category Name:**
- Specific responsibility with technical details
- Implementation guidance with measurable outcomes
- Domain context with business alignment
- Coordination requirements with other specialists
```

**Required Categories** (4-6 total):
1. **Technology-Specific**: Frontend, Backend, Database, Infrastructure
2. **Process-Oriented**: Assessment, Implementation, Integration, Monitoring  
3. **Domain-Focused**: Business specialization, Compliance, Security
4. **Collaboration**: Cross-agent coordination, Quality assurance

### Assessment Instructions (Critical)

**Pattern**: `[Behavioral directive] [Deliverable specification]. [Business alignment]. [Coordination requirements].`

**Examples**:
- "Always provide actionable recommendations with specific code examples, configuration changes, and measurable performance targets."
- "When security issues are identified, always provide both immediate mitigation strategies and long-term architectural improvements."

## Quality Standards Framework

### Technical Excellence Requirements
- **Code Examples**: Specific, executable implementation guidance
- **Standards Compliance**: Follow project coding standards (Black, Ruff, ESLint)
- **Type Safety**: Language-appropriate type safety (TypeScript strict mode, Pydantic validation)
- **Testing Integration**: Support for unit, integration, and E2E testing patterns

### Business Domain Integration  
- **Business Context**: Domain-specific operational requirements
- **Regulatory Compliance**: Industry-specific regulations (GDPR, financial, healthcare)
- **Data Specificity**: Domain data models and processing patterns
- **User Experience**: Professional workflows and user interface requirements

### Collaboration Protocols
- **Agent Coordination**: Clear integration with other domain specialists
- **Context Isolation**: Maintain focused responsibility boundaries (200k-token independent contexts)
- **Parallel Operation**: Support concurrent operation without conflicts
- **Quality Gates**: Integration with validation and testing workflows

## Architecture Constraints

### Fundamental Limitations
- **No Subagent Spawning**: Subagents CANNOT create other subagents (causes system hangs)
- **No Task Tool Usage**: Using Task tool within subagents to spawn others is forbidden
- **Context Isolation**: Each subagent operates in independent 200k-token context
- **Main Session Coordination**: All multi-agent coordination through main session only

### Performance Boundaries
- **Maximum 10 Concurrent**: Additional subagents automatically queued
- **Linear Token Usage**: 3 parallel agents = ~3x token consumption
- **Independent Contexts**: No cross-subagent context sharing or communication

## Tool Selection Guidelines

### Minimal Necessary Tools Principle
```yaml
# ✅ Focused Tool Sets
research_specialist: "WebSearch, WebFetch, Read, Grep, Glob"
code_analyzer: "Read, Grep, Glob, Bash"
validator: "Read, Grep, Glob"

# ❌ Kitchen Sink Approach  
avoid: "All available tools without clear purpose"
```

### Domain-Appropriate Tool Patterns
- **Research Agents**: WebSearch, WebFetch, Read, Grep, Glob
- **Code Analysis**: Read, Grep, Glob, Bash (for execution)
- **Validation**: Read, Grep, Glob (read-only for safety)
- **Documentation**: Read, Write, Edit, MultiEdit
- **Coordination**: TodoWrite, Edit, MultiEdit

## Configuration Quality Assessment

### Structural Compliance Checklist
- [ ] Opens with "You are" pattern
- [ ] Contains "## Core Responsibilities" section  
- [ ] Has 4-6 categorized technical areas
- [ ] Each category has 4-7 specific responsibilities
- [ ] Ends with behavioral assessment instructions
- [ ] Uses only valid Claude Code properties

### Content Quality Criteria
- [ ] Technical specifications are precise and actionable
- [ ] Domain context integrated throughout
- [ ] Deliverables are specific and measurable
- [ ] Collaboration protocols clearly defined
- [ ] Quality standards align with project requirements

### Assessment Effectiveness Validation
- [ ] Ending instructions provide clear behavioral directive
- [ ] Specific deliverable requirements defined
- [ ] Business alignment explicitly stated
- [ ] Coordination requirements specified
- [ ] Implementation guidance is production-ready

## Anti-Patterns to Avoid

### Configuration Problems
**Overly Broad Scope**:
```yaml
# ❌ Problematic
name: "full-stack-helper"
description: "Helps with all development tasks"

# ✅ Better
name: "react-performance-optimizer"  
description: "Optimize React component rendering and bundle size"
```

**Unclear Invocation Criteria**:
```yaml
# ❌ Vague
description: "Helps when needed"

# ✅ Specific
description: "Use when optimizing API response times >200ms or database queries >100ms"
```

**Fabricated Properties**:
```yaml
# ❌ Remove These (Don't Exist)
sdlc_stage: "implementation"
context_isolation: true
framework_integration: "research"

# ✅ Valid Properties Only
priority: high
team: development
environment: production
```

### Architectural Violations
- **Subagent Spawning**: Never attempt to create subagents from within subagents
- **Cross-Agent Communication**: Subagents cannot directly communicate with each other
- **Context Pollution**: Don't return implementation details to main session

## Enterprise and Professional Usage

### Team Collaboration Best Practices

**Storage Strategy for Professional Teams:**

**Project-Specific Subagents** (`.claude/agents/`):
- Shared team knowledge and consistent behavior
- Domain expertise aligned with project architecture
- Version-controlled alongside codebase for deployment consistency
- Highest priority in automatic delegation hierarchy

**Personal Subagents** (`~/.claude/agents/`):
- Individual workflow optimizations and preferences
- Experimental configurations and specialized variants
- Personal productivity enhancements
- Fallback when project subagents don't match context

**Team Consistency Framework:**
```yaml
# Example project team structure
.claude/agents/
├── security-reviewer.md          # Team security standards
├── performance-optimizer.md      # Project-specific performance criteria
├── api-integration-specialist.md # External service coordination
└── database-architect.md         # Data model and schema expertise

~/.claude/agents/
├── personal-code-reviewer.md     # Individual code style preferences
├── debug-assistant.md            # Personal debugging workflows
└── documentation-helper.md       # Individual documentation style
```

### Hooks System Integration

**Automated Workflow Enhancement:**
```yaml
# Project hooks configuration (.claude/settings.json)
{
  "hooks": {
    "PreToolUse": {
      "Read": "echo 'Subagent $SUBAGENT_NAME accessing: $TOOL_INPUT'"
    },
    "PostToolUse": {
      "Bash": "echo 'Command completed by: $SUBAGENT_NAME at $(date)'"
    },
    "UserPromptSubmit": {
      "*": "echo 'Context: $USER_PROMPT' >> .claude/logs/subagent-usage.log"
    }
  }
}
```

**Professional Workflow Patterns:**
- **Security Validation**: Pre-tool hooks validate subagent actions against security policies
- **Audit Logging**: Post-tool hooks track subagent activities for compliance
- **Performance Monitoring**: Measure subagent execution times and resource usage
- **Quality Gates**: Automated validation of subagent outputs before delivery

### Environment-Specific Configurations

**Development vs Production Subagents:**
```yaml
# Development environment - broader tool access
---
name: dev-database-specialist
description: "Development database specialist with debug tools, test data access, and experimental query capabilities."
tools: Read, Grep, Glob, Bash, WebSearch
environment: development
team: database
priority: high
---

# Production environment - restricted and monitored
---
name: prod-database-specialist
description: "Production database specialist with monitoring focus and safety constraints for live system management."
tools: Read, Grep, Glob
environment: production
team: database
priority: high
---
```

**Enterprise Security Integration:**
- **Tool Restrictions**: Production subagents have limited tool access
- **Audit Requirements**: All subagent actions logged for compliance
- **Access Controls**: Environment-specific subagent configurations
- **Monitoring Integration**: Performance and security monitoring for subagent activities

## Implementation Workflow

### Phase 1: Blueprint Application
1. Use AI-generated blueprint template as structural foundation
2. Apply universal opening pattern with role, expertise, and mission
3. Structure 4-6 responsibility categories with 4-7 items each
4. Include assessment instructions with behavioral directives

### Phase 2: Domain Adaptation
1. Replace generic examples with domain-specific context
2. Adjust technical stack specifications as needed
3. Maintain structural patterns and quality requirements
4. Preserve assessment instruction effectiveness

### Phase 3: Validation and Refinement
1. Check structural compliance against blueprint criteria
2. Verify content quality meets technical precision standards
3. Validate assessment instruction effectiveness
4. Test in real scenarios and refine based on performance

## Success Metrics

### Performance Indicators
- **Structural Compliance**: 100% adherence to AI-generated blueprint patterns
- **Content Precision**: Technical specifications are actionable and accurate
- **Assessment Effectiveness**: Clear behavioral outcomes and deliverables
- **Domain Integration**: Relevant business context without generic abstractions
- **Automatic Delegation Success**: Subagents selected appropriately by Claude's intelligent routing
- **Team Collaboration Efficiency**: Project subagents used consistently across team members

### Quality Standards
- **Immediate Usability**: Subagent ready for production use without additional configuration
- **Technical Accuracy**: Current best practices and accurate technical guidance
- **Clear Boundaries**: Well-defined scope without feature creep or overlap
- **Production Readiness**: All recommendations suitable for production deployment
- **Enterprise Integration**: Seamless integration with hooks, MCP, and team workflows

## Maintenance and Evolution

### Continuous Improvement
1. **Pattern Validation**: Regularly verify compliance with AI-generated blueprint standards
2. **Performance Assessment**: Monitor subagent effectiveness and user satisfaction
3. **Technical Updates**: Keep technical specifications current with latest best practices
4. **Quality Enhancement**: Improve assessment instructions based on usage outcomes
5. **Delegation Optimization**: Refine descriptions for better automatic selection accuracy
6. **Team Consistency**: Maintain alignment between project and personal subagent configurations

### Configuration Updates
1. **Remove Fabricated Properties**: Systematically eliminate non-existent configuration options
2. **Enhance Assessment Instructions**: Strengthen behavioral directives and deliverable specifications
3. **Improve Technical Precision**: Add specific code examples and measurable outcomes
4. **Optimize Tool Selection**: Ensure minimal necessary tool sets for maximum effectiveness

## MCP Server Integration Requirements

### Mandatory MCP Usage Standard

**CRITICAL REQUIREMENT**: All AI subagents MUST use MCP servers when they are available and applicable to their domain. This is not optional - MCP integration ensures real-time capabilities, enhanced functionality, and optimal performance across all AI operations.

**Reference**: For comprehensive MCP integration guidance, see [`knowledge-vault/knowledge/ai-systems/subagents/mcp-integration-guide.md`](mcp-integration-guide.md).

### Domain-Specific MCP Integration Patterns

**Frontend Development Domain**:
```yaml
tools: Read, Grep, Glob, WebSearch, mcp__MCP_DOCKER__get_file_contents, mcp__MCP_DOCKER__search_repositories, mcp__MCP_DOCKER__browser_snapshot, mcp__MCP_DOCKER__browser_take_screenshot
```

**Database Systems Domain**:
```yaml
tools: Read, Grep, Glob, Edit, Bash, mcp__MCP_DOCKER__search_repositories, mcp__MCP_DOCKER__get_file_contents
```

**Security Systems Domain**:
```yaml
tools: Read, Grep, Glob, WebSearch, mcp__MCP_DOCKER__get_file_contents, mcp__MCP_DOCKER__list_secret_scanning_alerts, mcp__MCP_DOCKER__list_code_scanning_alerts, mcp__MCP_DOCKER__list_dependabot_alerts
```

**API Integration Domain**:
```yaml
tools: Read, Write, Bash, WebSearch, mcp__MCP_DOCKER__jira_*, mcp__MCP_DOCKER__fetch, mcp__MCP_DOCKER__get_file_contents, mcp__MCP_DOCKER__search_repositories
```

### MCP Integration Quality Standards

**Error Handling Requirements**:
- Implement circuit breaker patterns for MCP server failures
- Provide graceful fallback to cached knowledge when MCP unavailable
- Log all MCP integration errors for monitoring and debugging

**Performance Standards**:
- MCP queries must complete within 3 seconds
- Cache hit rate must exceed 85% for repeated queries
- Error rate must remain below 2% for MCP server interactions

**Security Compliance**:
- Use environment variables for all MCP server credentials
- Implement least-privilege access for MCP operations
- Maintain audit logs for all MCP server interactions

### Implementation Checklist for MCP Integration

**For New Subagents**:
- [ ] Identify applicable MCP servers based on domain mapping
- [ ] Configure tools with appropriate MCP server functions
- [ ] Implement circuit breaker and fallback strategies
- [ ] Add error handling and logging mechanisms
- [ ] Test MCP integration functionality and fallback behavior

**For Existing Subagents**:
- [ ] Audit current tool configuration for missing MCP integration
- [ ] Update frontmatter with required MCP tools
- [ ] Enhance core responsibilities with MCP integration section
- [ ] Implement error handling patterns
- [ ] Test integration and fallback scenarios

This comprehensive approach ensures all subagents follow proven AI-generated patterns while leveraging Claude Code's advanced features for automatic delegation, team collaboration, enterprise integration, and mandatory MCP server integration. The result is production-ready subagents that enhance developer productivity and maintain professional workflow standards with real-time capabilities.