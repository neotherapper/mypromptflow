# Claude Subagent Configuration Guide: AI-Generated Blueprint Standards

This guide provides comprehensive configuration standards for Claude Code subagents based on empirical analysis of AI-generated patterns, Claude Code specification validation, and official documentation for storage hierarchy, tool permissions, and enterprise integration.

## Valid Claude Code Properties

Based on Claude Code architecture analysis, subagents support ONLY these frontmatter properties:

### Required Fields

```yaml
---
name: "subagent-identifier" # Required: kebab-case unique identifier
description: "Usage criteria..." # Required: When to use with examples
---
```

### Optional Fields

```yaml
---
tools: Read, Grep, Glob # Optional: Minimal necessary tool set
priority: high # Optional: high/medium/low
team: development # Optional: Team assignment
environment: production # Optional: Environment-specific usage
---
```

**CRITICAL**: All Properties besides the above are fabricated and DO NOT exist in Claude Code. Remove these from all configurations.

## Storage Hierarchy and Priority System

### Storage Locations (Priority Order)

**1. Project-Level Subagents** (`.claude/agents/` - Highest Priority):

- **Purpose**: Team-shared subagents with consistent behavior
- **Audience**: All team members working on the project
- **Version Control**: Tracked alongside codebase in Git
- **Automatic Delegation**: First priority for Claude's intelligent routing
- **Use Cases**: Domain-specific expertise, project standards, team workflows

**2. User-Level Subagents** (`~/.claude/agents/` - Fallback):

- **Purpose**: Personal workflow optimizations and preferences
- **Audience**: Individual developer customization
- **Version Control**: Personal configurations, not shared
- **Automatic Delegation**: Used when project subagents don't match context
- **Use Cases**: Individual coding style, experimental configurations, personal productivity tools

### Storage Best Practices

**Project-Level Strategy:**

```bash
# Recommended project subagent structure
.claude/agents/
├── security-code-reviewer.md      # Team security standards and practices
├── performance-optimizer.md       # Project-specific performance criteria
├── api-integration-specialist.md  # External service integration patterns
├── database-architect.md          # Data model and schema management
└── deployment-coordinator.md      # CI/CD and production deployment
```

**User-Level Strategy:**

```bash
# Personal subagent structure
~/.claude/agents/
├── personal-code-reviewer.md      # Individual code review preferences
├── debug-assistant.md             # Personal debugging workflows
├── documentation-writer.md        # Individual documentation style
└── productivity-optimizer.md      # Personal workflow enhancements
```

## AI-Generated Blueprint Structure

### Complete Configuration Template

```yaml
---
name: "domain-specific-specialist"
description: "Use this agent when [specific conditions]. Examples: <example>Context: [scenario] user: '[request]' assistant: '[response]'</example>"
tools: Read, Grep, Glob
priority: high
team: development
environment: production
---

You are a [SPECIFIC ROLE TITLE] with deep expertise in [TECHNICAL STACK + DOMAIN]. Your mission is to [CLEAR OBJECTIVE WITH MEASURABLE OUTCOMES].

## Core Responsibilities

**Technology-Specific Category:**
- Specific responsibility with technical details
- Implementation guidance with measurable outcomes
- Domain context with business alignment
- Coordination requirements with other specialists

**Process-Oriented Category:**
- Assessment methodology with clear criteria
- Implementation patterns with best practices
- Integration approaches with quality standards
- Monitoring strategies with performance metrics

**Domain-Focused Category:**
- Business specialization with operational context
- Compliance requirements with regulatory standards
- Security considerations with threat modeling
- User experience optimization with usability principles

**Collaboration Category:**
- Cross-agent coordination protocols
- Quality assurance integration methods
- Result delivery standards and formats
- Context boundary maintenance procedures

[Behavioral directive starting with "Always" or "When"] [Specific deliverable requirements]. [Business alignment statement]. [Coordination requirements].
```

## Field Configuration Standards

### Name Field Requirements

**Format Standards**:

- Use kebab-case (lowercase with hyphens)
- Be descriptive and domain-specific
- Indicate primary technical specialization
- Avoid generic or overly broad terms

**AI-Generated Pattern Examples**:

```yaml
name: "security-code-reviewer"           # Security domain specialization
name: "fullstack-performance-optimizer"  # Performance domain with tech stack
name: "api-integration-specialist"       # API domain with integration focus
name: "postgresql-database-specialist"   # Database technology specialization
name: "react-frontend-specialist"        # Frontend technology specialization
```

**Anti-Patterns to Avoid**:

```yaml
name: "helper"                    # Too generic, no domain indication
name: "CodeReviewer"             # Wrong case format, lacks specialization
name: "general-purpose-agent"    # Violates single responsibility principle
name: "full-stack-everything"    # Too broad, unclear boundaries
```

### Description Field Standards

**AI-Generated Pattern Requirements**:

- Start with "Use this agent when [specific conditions]"
- Include specific technical expertise areas
- Provide concrete usage examples with context
- Define clear invocation criteria

**Optimal Description Structure**:

```yaml
description: "Use this agent when [specific technical conditions]. This includes [domain expertise areas]. Examples: <example>Context: [scenario] user: '[user request]' assistant: '[response using agent]'</example>"
```

**High-Quality Examples**:

```yaml
description: "Use this agent when conducting security reviews of code changes, validating authentication implementations, or identifying security vulnerabilities. Examples: <example>Context: User has implemented a new API endpoint. user: 'Can you review this for security issues?' assistant: 'I'll use the security-code-reviewer agent to perform comprehensive security assessment.'</example>"

description: "Use this agent when you need comprehensive performance optimization across React frontend, FastAPI backend, and PostgreSQL database stack. Examples: <example>Context: User notices slow page loads. user: 'The app is loading slowly with large datasets' assistant: 'I'll use the fullstack-performance-optimizer agent to analyze and resolve performance bottlenecks.'</example>"
```

### Tool Selection Standards

**Minimal Necessary Tools Principle**:
Only include tools that are essential for the subagent's specific domain expertise.

**Domain-Appropriate Tool Patterns**:

```yaml
# Research specialists
research_tools: "WebSearch, WebFetch, Read, Grep, Glob"

# Code analysis specialists
analysis_tools: "Read, Grep, Glob, Bash"

# Validation specialists
validation_tools: "Read, Grep, Glob"

# Documentation specialists
documentation_tools: "Read, Write, Edit, MultiEdit"

# Coordination specialists
coordination_tools: "TodoWrite, Edit, MultiEdit"
```

**Tool Selection Examples**:

```yaml
# ✅ Focused tool selection for security review
tools: Read, Grep, Glob, WebSearch

# ✅ Performance analysis with execution capability
tools: Read, Grep, Glob, Bash

# ❌ Kitchen sink approach (avoid)
tools: Read, Write, Edit, MultiEdit, Grep, Glob, Bash, WebSearch, WebFetch, TodoWrite
```

### Priority and Team Assignment

**Priority Levels**:

```yaml
priority: high     # Critical specialists used frequently
priority: medium   # Regular specialists for specific domains
priority: low      # Specialized validators or niche tools
```

**Team Assignment Examples**:

```yaml
team: development    # Core development specialists
team: security       # Security-focused specialists
team: research       # Research and analysis specialists
team: validation     # Quality assurance and validation specialists
```

## Tool Permissions and System Configuration

### System-Level Tool Control

**Global Permission Configuration** (`.claude/settings.json`):

```json
{
  "permissions": {
    "allow": [
      "Read",
      "Grep",
      "Glob",
      "Bash(git *)",
      "Bash(npm run lint)",
      "WebSearch"
    ],
    "deny": ["Bash(rm *)", "Bash(curl *)", "Edit(/etc/*)"]
  }
}
```

**Environment-Specific Permissions:**

```json
{
  "permissions": {
    "development": {
      "allow": ["Read", "Write", "Edit", "Bash", "WebSearch", "WebFetch"],
      "deny": ["Bash(rm -rf *)"]
    },
    "production": {
      "allow": ["Read", "Grep", "Glob"],
      "deny": ["Write", "Edit", "Bash"]
    }
  }
}
```

### Dynamic Tool Permission Management

**CLI Flag Override:**

```bash
# Allow specific tools for session
claude --allowedTools "Bash(git log:*)" "Bash(git diff:*)" "Read"

# Deny specific tools for session
claude --disallowedTools "Bash(git push:*)" "Edit"

# Set permission mode
claude --permission-mode plan
```

**Subagent-Specific Tool Restrictions:**

```yaml
# Security-focused subagent - read-only tools
---
name: security-auditor
description: "Security audit specialist with read-only access for safe analysis."
tools: Read, Grep, Glob, WebSearch
priority: high
team: security
---
# Development subagent - broader tool access
---
name: dev-assistant
description: "Development assistant with full tool access for implementation tasks."
tools: Read, Write, Edit, Bash, Grep, Glob
priority: medium
team: development
environment: development
---
```

### Hooks Integration for Subagents

**Subagent Activity Monitoring:**

```json
{
  "hooks": {
    "PreToolUse": {
      "Bash": {
        "command": "echo 'AUDIT: Subagent $SUBAGENT_NAME executing: $TOOL_INPUT' >> .claude/logs/audit.log",
        "timeout": 5000
      }
    },
    "PostToolUse": {
      "*": {
        "command": "echo 'COMPLETED: $TOOL_NAME by $SUBAGENT_NAME at $(date)' >> .claude/logs/activity.log",
        "timeout": 5000
      }
    },
    "UserPromptSubmit": {
      "*": {
        "command": "echo 'CONTEXT: User prompt processed, subagent selection in progress' >> .claude/logs/delegation.log",
        "timeout": 3000
      }
    }
  }
}
```

**Security Validation Hooks:**

```json
{
  "hooks": {
    "PreToolUse": {
      "Bash": {
        "command": "bash .claude/scripts/validate-command.sh '$TOOL_INPUT'",
        "timeout": 10000,
        "blockOnFailure": true
      },
      "Edit": {
        "command": "bash .claude/scripts/validate-file-access.sh '$TOOL_INPUT'",
        "timeout": 5000,
        "blockOnFailure": true
      }
    }
  }
}
```

## Content Structure Standards

### Opening Pattern Requirements

**Universal Structure**:

```
You are a [SPECIFIC ROLE TITLE] with deep expertise in [TECHNICAL STACK + DOMAIN]. Your mission is to [CLEAR OBJECTIVE WITH MEASURABLE OUTCOMES].
```

**Key Elements**:

- Professional title combining technology and specialization
- "deep expertise" phrase for authority establishment
- Technical stack specification for precision
- Mission statement with measurable outcomes

### Responsibility Organization

**Section Header**: Must use `## Core Responsibilities`

**Category Requirements**:

- 4-6 technical categories total
- Each category has 4-7 specific responsibilities
- Use markdown formatting: `**Category Name:**`
- Include bullet points with technical specificity

**Required Category Types**:

1. **Technology-Specific**: Frontend, Backend, Database, Infrastructure
2. **Process-Oriented**: Assessment, Implementation, Integration, Monitoring
3. **Domain-Focused**: Business specialization, Compliance, Security
4. **Collaboration**: Cross-agent coordination, Quality assurance

### Assessment Instructions

**Critical Ending Pattern**:

```
[Behavioral directive starting with "Always" or "When [condition]"] [Specific deliverable requirements]. [Business alignment statement]. [Coordination requirements].
```

**Pattern Examples**:

- "Always provide actionable recommendations with specific code examples, configuration changes, and measurable performance targets."
- "When security issues are identified, always provide both immediate mitigation strategies and long-term architectural improvements."

## Automatic Delegation Optimization

### Description Field Optimization for Intelligent Routing

**Claude Code's Automatic Delegation System** analyzes context, keywords, and usage patterns to intelligently route tasks to appropriate subagents. Optimize descriptions for maximum routing accuracy:

**Intelligent Routing Keywords:**

```yaml
# Technical Keywords - Include specific technologies
technical_keywords:
  ["React", "TypeScript", "FastAPI", "PostgreSQL", "Docker", "JWT", "OAuth"]

# Action Keywords - Match common user intents
action_keywords:
  ["review", "optimize", "debug", "implement", "analyze", "validate", "deploy"]

# Domain Keywords - Business and technical domains
domain_keywords:
  [
    "security",
    "performance",
    "authentication",
    "database",
    "frontend",
    "backend",
  ]

# Context Keywords - Situational triggers
context_keywords:
  [
    "slow loading",
    "security vulnerability",
    "failing tests",
    "production issue",
  ]
```

**Optimal Description Structure for Automatic Selection:**

```yaml
description: "Use this agent when [technical conditions with keywords]. Specializes in [domain expertise with technical terms]. Context triggers: [common scenarios]. Examples: <example>Context: [realistic scenario] user: '[typical request with keywords]' assistant: '[delegation response]'</example>"
```

**Examples Optimized for Claude's Intelligent Routing:**

```yaml
# Security specialist - keyword-rich for security contexts
description: "Use this agent when conducting security reviews, vulnerability assessments, or authentication implementations. Specializes in OWASP Top 10 analysis, JWT security, SQL injection prevention, and secure coding practices. Context triggers: security audit requests, authentication failures, vulnerability reports. Examples: <example>Context: New API endpoint implementation user: 'Can you review this endpoint for security vulnerabilities?' assistant: 'I'll use the security-code-reviewer agent for comprehensive OWASP-based security assessment.'</example>"

# Performance specialist - optimized for performance-related routing
description: "Use this agent when experiencing performance issues, slow page loads, high response times, or memory problems. Specializes in React rendering optimization, database query tuning, API response acceleration, and bundle size reduction. Context triggers: slow loading complaints, timeout errors, resource usage spikes. Examples: <example>Context: Dashboard loading slowly user: 'The dashboard takes 5+ seconds to load with large datasets' assistant: 'I'll use the performance-optimizer agent to analyze and resolve bottlenecks across the full stack.'</example>"
```

**Keyword Strategy for Maximum Routing Accuracy:**

- **Primary Keywords**: Include exact technologies used in the project (React, FastAPI, PostgreSQL)
- **Secondary Keywords**: Add related terms and synonyms (authentication/auth, optimization/performance)
- **Context Triggers**: Include specific problem descriptions users commonly express
- **Example Scenarios**: Provide realistic usage examples that match actual user requests

## Quality Validation Standards

### Structural Compliance Checklist

- [ ] Uses only valid Claude Code properties (name, description, tools, priority, team, environment)
- [ ] Opens with "You are" pattern
- [ ] Contains "## Core Responsibilities" section
- [ ] Has 4-6 categorized technical areas
- [ ] Each category has 4-7 specific responsibilities
- [ ] Ends with behavioral assessment instructions
- [ ] Description optimized for automatic delegation with relevant keywords

### Content Quality Requirements

- [ ] Technical specifications are precise and actionable
- [ ] Domain context integrated throughout content
- [ ] Deliverables are specific and measurable
- [ ] Collaboration protocols clearly defined
- [ ] Quality standards align with production requirements

### Assessment Effectiveness Criteria

- [ ] Ending instructions provide clear behavioral directive
- [ ] Specific deliverable requirements defined
- [ ] Business alignment explicitly stated
- [ ] Coordination requirements specified
- [ ] Implementation guidance is production-ready

## Anti-Patterns and Common Mistakes

### Configuration Problems

**Fabricated Properties**:

```yaml
# ❌ Remove these (don't exist in Claude Code)
context_isolation: true
framework_integration: "research"
specialization_domain: "security"
quality_standards: "constitutional_ai"
coordination_pattern: "parallel"

# ✅ Use only valid properties
priority: high
team: development
environment: production
```

**Overly Broad Scope**:

```yaml
# ❌ Too general
name: "full-stack-helper"
description: "Helps with all development tasks"

# ✅ Specific and focused
name: "react-performance-optimizer"
description: "Use when optimizing React component rendering and bundle size"
```

**Unclear Invocation Criteria**:

```yaml
# ❌ Vague usage conditions
description: "Helps with security when needed"

# ✅ Specific conditions with examples
description: "Use when conducting OWASP Top 10 security assessments or validating authentication flows"
```

## Implementation Workflow

### Phase 1: Blueprint Application

1. Use AI-generated blueprint template as foundation
2. Apply universal opening pattern with role and expertise
3. Structure 4-6 responsibility categories with specific items
4. Include assessment instructions with behavioral directives

### Phase 2: Configuration Validation

1. Verify only valid Claude Code properties used
2. Check structural compliance against blueprint patterns
3. Validate technical precision and domain integration
4. Confirm assessment instruction effectiveness

### Phase 3: Quality Assurance

1. Test subagent in real scenarios
2. Validate deliverable quality and specificity
3. Confirm behavioral directive effectiveness
4. Refine based on performance feedback

## Maintenance Standards

### Regular Validation

1. **Property Compliance**: Ensure no fabricated properties introduced
2. **Structural Integrity**: Maintain AI-generated blueprint patterns
3. **Technical Currency**: Keep technical specifications current
4. **Assessment Effectiveness**: Monitor and improve behavioral outcomes

### Continuous Improvement

1. **Pattern Refinement**: Enhance based on AI-generated pattern discoveries
2. **Technical Precision**: Add specific examples and measurable outcomes
3. **Quality Enhancement**: Strengthen assessment instructions and deliverables
4. **Domain Integration**: Improve business context and professional alignment

## MCP Server Integration Configuration

### Mandatory MCP Integration Standard

**CRITICAL REQUIREMENT**: All AI subagents MUST include MCP server tools when they are available and applicable to their domain. This ensures real-time capabilities, enhanced functionality, and optimal performance.

**Complete MCP Integration Guide**: See [`knowledge-vault/knowledge/ai-systems/subagents/mcp-integration-guide.md`](mcp-integration-guide.md) for comprehensive implementation details.

### Tool Configuration with MCP Integration

**Basic Tools with MCP Enhancement**:

```yaml
# Frontend Development Pattern
tools: Read, Grep, Glob, WebSearch, mcp__MCP_DOCKER__get_file_contents, mcp__MCP_DOCKER__search_repositories, mcp__MCP_DOCKER__browser_snapshot

# Database Systems Pattern  
tools: Read, Grep, Glob, Edit, Bash, mcp__MCP_DOCKER__search_repositories, mcp__MCP_DOCKER__get_file_contents

# Security Systems Pattern
tools: Read, Grep, Glob, WebSearch, mcp__MCP_DOCKER__list_secret_scanning_alerts, mcp__MCP_DOCKER__list_code_scanning_alerts, mcp__MCP_DOCKER__get_file_contents

# API Integration Pattern
tools: Read, Write, Bash, WebSearch, mcp__MCP_DOCKER__jira_get_issue, mcp__MCP_DOCKER__jira_create_issue, mcp__MCP_DOCKER__fetch, mcp__MCP_DOCKER__search_repositories
```

### MCP Tool Selection Guidelines

**Tier 1 MCP Servers (Must Use)**:
- `mcp__MCP_DOCKER__get_file_contents` - Repository file access
- `mcp__MCP_DOCKER__search_repositories` - Repository intelligence
- `mcp__MCP_DOCKER__jira_*` - Project management and workflows
- `mcp__MCP_DOCKER__fetch` - External API and web content access
- `mcp__MCP_DOCKER__browser_*` - Frontend testing and validation

**Tier 2 MCP Servers (Domain-Specific)**:
- `mcp__MCP_DOCKER__list_*_alerts` - Security scanning and analysis
- `mcp__AWS__*` - Infrastructure management and cost optimization

### Configuration Example with MCP Integration

```yaml
---
name: react-maritime-frontend
description: "Use when developing React/TypeScript maritime insurance interfaces with vessel management, policy dashboards, and claims processing forms. Context triggers: frontend component development, UI performance issues, maritime data visualization. Examples: <example>Context: User needs vessel registration form user: 'Create vessel form with IMO validation' assistant: 'Using react-maritime-frontend agent for maritime-specific React component development'</example>"
tools: Read, Grep, Glob, WebSearch, mcp__MCP_DOCKER__get_file_contents, mcp__MCP_DOCKER__search_repositories, mcp__MCP_DOCKER__browser_snapshot, mcp__MCP_DOCKER__browser_take_screenshot
priority: high
team: frontend
---

You are a React/TypeScript Frontend Specialist with deep expertise in maritime insurance interface development. Your mission is to create production-ready maritime components with measurable performance improvements and regulatory compliance.

## Core Responsibilities

**React/TypeScript Excellence:**
- Implement modern React patterns with hooks, context API, and TypeScript strict mode
- Design maritime-specific components (vessel cards, policy forms, risk indicators)
- Utilize MCP GitHub integration for real-time repository analysis and code context
- Apply TanStack Query with MCP fetch integration for optimized maritime data handling

**MCP Integration Capabilities:**
- Leverage repository intelligence through mcp__MCP_DOCKER__search_repositories for code context
- Access file contents via mcp__MCP_DOCKER__get_file_contents for comprehensive analysis
- Utilize browser automation with mcp__MCP_DOCKER__browser_* tools for UI testing
- Implement fallback strategies when MCP servers are unavailable

Always provide production-ready React components with comprehensive TypeScript types, MCP-enhanced development workflows, and maritime-specific accessibility features. Coordinate with ui-ux-specialist for design implementation and system-architect for API integration patterns when components require cross-domain functionality.
```

### MCP Integration Validation Checklist

**Configuration Requirements**:
- [ ] Domain-appropriate MCP servers included in tools configuration
- [ ] Error handling and fallback strategies implemented
- [ ] MCP server usage documented in core responsibilities
- [ ] Performance standards defined for MCP operations

**Quality Standards**:
- [ ] MCP queries complete within 3 seconds
- [ ] Fallback behavior tested and documented
- [ ] Security credentials managed via environment variables
- [ ] Audit logging implemented for MCP server interactions

This configuration guide ensures all Claude subagents follow proven AI-generated patterns for maximum effectiveness while maintaining Claude Code architecture compliance and mandatory MCP server integration for enhanced real-time capabilities.
