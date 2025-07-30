# AI-Generated Subagent Blueprint Template

This template captures the proven structural patterns from AI-generated Claude subagents, providing a systematic framework for creating and validating high-quality subagents optimized for Claude Code's automatic delegation and team collaboration features.

## Frontmatter Structure

```yaml
---
name: [agent-name]
description: Use this agent when [specific conditions and examples]. Examples: <example>Context: [scenario] user: '[user request]' assistant: '[response using agent]'</example>
tools: [minimal-necessary-tools]
priority: [high/medium/low]
team: [team-assignment]
---
```

**Required Properties:**

- `name`: kebab-case agent identifier (used for automatic delegation routing)
- `description`: Comprehensive usage guidance optimized for automatic delegation

**Optional Properties:**

- `tools`: Minimal necessary tool set for domain expertise
- `priority`: Delegation preference (high/medium/low)  
- `team`: Team assignment for project organization

**Storage Locations (Priority Order):**

1. **Project-level**: `.claude/agents/` (highest priority, team-shared)
2. **User-level**: `~/.claude/agents/` (personal fallback)

**Validation:** Frontmatter must contain only valid Claude Code properties: `name`, `description`, `tools`, `priority`, `team`, `environment`

## Universal Opening Pattern

```
You are a [ROLE TITLE] with [EXPERTISE SPECIFICATION]. [MISSION STATEMENT]
```

**Pattern Elements:**

- **Role Title**: Specific, professional title combining technology and domain
- **Expertise Specification**: Technical stack + domain specialization
- **Mission Statement**: Clear objective focusing on measurable outcomes

**Examples:**

- "You are a Full-Stack Performance Optimization Specialist with deep expertise in React/FastAPI/PostgreSQL maritime insurance applications. Your mission is to identify, analyze, and resolve performance bottlenecks across the entire technology stack while providing measurable improvements with specific metrics."
- "You are a Security Code Review Specialist with deep expertise in OWASP Top 10 vulnerabilities, secure coding practices, and maritime insurance compliance requirements."

## Core Responsibilities Structure

### Section Header

```
## Core Responsibilities
[or]
Your core responsibilities include:
```

### Category Organization

**3-6 Technical Categories** with descriptive headers using markdown formatting:

```
**Category Name:**
- Responsibility 1 with specific technical details
- Responsibility 2 with measurable outcomes
- Responsibility 3 with domain context
- Responsibility 4-7 following same pattern
```

**Category Patterns:**

- **Technology-Specific**: Frontend, Backend, Database, Infrastructure
- **Process-Oriented**: Assessment, Implementation, Integration, Monitoring
- **Domain-Focused**: Business Domain Specialization, Compliance, Security
- **Collaboration**: Cross-agent coordination, quality assurance

### Responsibility Specifications

Each responsibility must include:

- **Technical Specificity**: Exact technologies, frameworks, patterns
- **Measurable Outcomes**: Performance targets, compliance standards
- **Domain Context**: business alignment
- **Implementation Guidance**: Specific methodologies or approaches

## Assessment Instructions (Critical)

**Ending Section Pattern:**

```
[Behavioral directive starting with "Always" or "When [condition]"] [Specific deliverable requirements]. [Business alignment statement]. [Coordination requirements].
```

**Essential Elements:**

1. **Action Directive**: Clear behavioral instruction (Always/When pattern)
2. **Deliverable Specification**: Exact outputs expected (code examples, scripts, configurations)
3. **Domain Alignment**: Maritime insurance business requirements connection
4. **Quality Standards**: Production-ready, maintainable, compliant solutions
5. **Collaboration Protocol**: Coordination with other specialists when needed

**Assessment Pattern Examples:**

- "Always provide actionable recommendations with specific code examples, configuration changes, and measurable performance targets."
- "When security issues are identified, always provide both immediate mitigation strategies and long-term architectural improvements."
- "Consider the unique aspects of business domain data and requirements in all recommendations."

## Automatic Delegation Optimization

### Description Field Optimization for Automatic Selection

**Claude Code automatically delegates tasks to specialized subagents based on context analysis**. Optimize descriptions for intelligent routing:

**Optimal Description Structure:**
```yaml
description: "Use this agent when [specific technical conditions with keywords]. This includes [domain expertise areas]. Examples: <example>Context: [realistic scenario] user: '[typical user request]' assistant: '[delegation response]'</example>"
```

**Automatic Delegation Keywords:**
- **Technical Keywords**: Include specific technologies, frameworks, patterns
- **Action Keywords**: Use verbs that match common user intents (review, optimize, debug, implement)
- **Domain Keywords**: Include business domain terminology and concepts
- **Context Keywords**: Add situational triggers (performance issues, security concerns, deployment)

**Examples Optimized for Automatic Delegation:**
```yaml
# Security subagent - optimized for security-related contexts
description: "Use this agent when conducting security reviews, identifying vulnerabilities, or validating authentication implementations. Specializes in OWASP Top 10 analysis, penetration testing insights, and secure coding practices. Examples: <example>Context: User implements new API endpoint user: 'Can you review this endpoint for security issues?' assistant: 'I'll use the security-code-reviewer agent to perform comprehensive security assessment.'</example>"

# Performance subagent - optimized for performance contexts  
description: "Use this agent when experiencing slow performance, optimizing response times, or preparing for production scaling. Handles React rendering optimization, API response acceleration, and database query tuning. Examples: <example>Context: User notices slow page loads user: 'The dashboard is loading slowly with large datasets' assistant: 'I'll use the performance-optimizer agent to analyze and resolve bottlenecks.'</example>"
```

### Team Collaboration Patterns

**Storage Strategy for Teams:**

**Project-Level Subagents** (`.claude/agents/`):
- Shared team subagents with consistent behavior
- Domain-specific specialists for project context
- Version-controlled with codebase
- Highest priority in delegation hierarchy

**User-Level Subagents** (`~/.claude/agents/`):
- Personal workflow optimizations
- Experimental or specialized variants
- Individual productivity enhancements
- Fallback when project subagents unavailable

**Team Consistency Framework:**
```yaml
# Project subagent - consistent team behavior
---
name: project-security-reviewer
description: "Team security specialist for [PROJECT_NAME] codebase. Familiar with project architecture, coding standards, and security requirements."
tools: Read, Grep, Glob, WebSearch
team: security
priority: high
---

# User subagent - personal optimization
---
name: personal-code-reviewer  
description: "Personal code review assistant with individual preferences and custom checks."
tools: Read, Grep, Glob
team: development
priority: medium
---
```

## Quality Standards Framework

### Technical Excellence

- **Code Examples**: Specific, executable implementation guidance
- **Standards Compliance**: Follow coding standards (Black, Ruff, ESLint)
- **Type Safety**: TypeScript strict mode, Pydantic validation, SQLModel entities
- **Testing Integration**: Support for unit, integration, and E2E testing patterns

### Maritime Domain Integration

- **Business Context**: Business domain operational requirements
- **Regulatory Compliance**: if exist -> GDPR, financial regulations
- **Data Specificity**: Business domain data model
- **User Experience**: Business domain used workflows

### Collaboration Protocols

- **Agent Coordination**: Clear integration with other business domain specialists
- **Context Isolation**: Maintain focused responsibility boundaries
- **Parallel Operation**: Support concurrent operation without conflicts
- **Quality Gates**: Integration with validation and testing workflows

## Validation Criteria

### Structural Compliance

- [ ] Frontmatter contains only valid properties
- [ ] Opens with "You are" pattern
- [ ] Contains "## Core Responsibilities" section
- [ ] Has 3-6 categorized technical areas
- [ ] Each category has 4-7 specific responsibilities
- [ ] Ends with behavioral assessment instructions

### Content Quality

- [ ] Technical specifications are precise and actionable
- [ ] Business domain context is integrated throughout
- [ ] Description optimized for automatic delegation with relevant keywords
- [ ] Deliverables are specific and measurable
- [ ] Collaboration protocols are clearly defined
- [ ] Quality standards align with project requirements

### Assessment Effectiveness

- [ ] Ending instructions provide clear behavioral directive
- [ ] Specific deliverable requirements are defined
- [ ] Business alignment is explicitly stated
- [ ] Coordination requirements are specified
- [ ] Implementation guidance is production-ready

## Implementation Notes

**Blueprint Usage:**

1. Start with universal opening pattern
2. Define 3-6 technical responsibility categories
3. Populate each category with 4-7 specific responsibilities
4. Include collaboration protocols and quality standards
5. End with behavioral assessment instructions

**Domain Adaptation:**

- Replace "maritime insurance" with target domain
- Adjust technical stack specifications as needed
- Maintain structural patterns and quality requirements
- Preserve assessment instruction effectiveness

**Validation Integration:**

- Use this template as validation framework
- Check structural compliance systematically
- Verify content quality against criteria
- Validate assessment instruction effectiveness

## Claude Code Ecosystem Integration

### Slash Command Integration

**`/agents` Command Integration:**
- Subagents discoverable via `/agents` slash command
- Proper naming and descriptions enable easy selection
- Team subagents appear with project context

**Custom Command Coordination:**
- Subagents can complement custom commands (`.claude/commands/`)
- Shared tool configurations between subagents and commands
- Coordinated project workflows

### Hooks System Integration

**Pre/Post Tool Execution:**
```yaml
# Example hooks integration for subagents
hooks:
  PreToolUse:
    Read: "echo 'Subagent accessing: $TOOL_INPUT'"
  PostToolUse:
    Bash: "echo 'Command completed by: $SUBAGENT_NAME'"
```

**Subagent Workflow Enhancement:**
- Automated logging of subagent activities
- Security validation for subagent tool usage
- Performance monitoring of subagent executions
- Context injection for enhanced capabilities

### Enterprise and Team Features

**Version Control Integration:**
- Project subagents tracked in Git alongside codebase
- Team consistency through shared configurations
- Deployment coordination with CI/CD pipelines

**Environment-Specific Configurations:**
```yaml
# Development environment subagent
---
name: dev-database-specialist
description: "Development environment database specialist with debug tools and test data access."
tools: Read, Grep, Glob, Bash
environment: development
---

# Production environment subagent  
---
name: prod-database-specialist
description: "Production database specialist with monitoring and safety constraints."
tools: Read, Grep, Glob
environment: production
---
```

**Model Context Protocol (MCP) Integration:**
- Enhanced subagents with external data source access
- Enterprise data integration through MCP servers
- Scalable deployment across AWS/GCP infrastructure

This blueprint template provides comprehensive guidance for creating production-ready Claude subagents that integrate seamlessly with Claude Code's advanced features and team collaboration workflows.
