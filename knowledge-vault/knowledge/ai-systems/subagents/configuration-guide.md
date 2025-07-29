# Sub-Agent Configuration Guide: YAML Frontmatter Standards

## Overview

This guide provides comprehensive standards for configuring Claude Code sub-agents through YAML frontmatter, ensuring optimal performance, proper tool selection, and framework integration. Following these standards ensures consistent, high-quality sub-agent implementations.

## YAML Frontmatter Structure

### Required Fields

```yaml
---
name: "unique-agent-identifier"
description: "Clear purpose and usage criteria"
---
```

### Complete Configuration Template

```yaml
---
# REQUIRED FIELDS
name: "agent-name"                           # Unique identifier (kebab-case)
description: "Detailed usage criteria"       # When to invoke this agent

# OPTIONAL FIELDS  
tools: Tool1, Tool2, Tool3                  # Comma-separated tool list
priority: high                              # high, medium, low
team: backend                               # Team assignment
environment: production                     # Environment context
context_isolation: true                     # Explicit isolation (recommended)

# ENHANCED FIELDS (Recommended)
framework_integration: "framework-name"     # Links to framework documentation
specialization_domain: "domain_name"        # Clear expertise area
quality_standards: "constitutional_ai"      # Quality requirements
coordination_pattern: "parallel"            # parallel, sequential, adaptive
---
```

## Field Specifications

### Name Field Standards

**Format Requirements**:
- Use kebab-case (lowercase with hyphens)
- Be descriptive and specific
- Indicate primary specialization
- Avoid generic terms

**✅ Good Name Examples**:
```yaml
name: "security-code-reviewer"
name: "react-performance-optimizer"
name: "database-architecture-specialist"
name: "information-access-specialist"
name: "ai-instruction-validator"
```

**❌ Poor Name Examples**:
```yaml
name: "helper"                    # Too generic
name: "CodeReviewer"             # Wrong case format
name: "general-purpose-agent"    # Too broad
name: "agent1"                   # Non-descriptive
```

### Description Field Standards

**Content Requirements**:
- Clearly state when to use the agent
- Include specific expertise areas
- Mention framework integrations
- Define scope boundaries

**✅ Good Description Examples**:
```yaml
description: "Expert security code review specialist for identifying vulnerabilities, security anti-patterns, and compliance issues in code changes. Invoke for security-focused code analysis, penetration testing insights, and secure coding recommendations."

description: "Specialized agent for conducting comprehensive research using the 15-method orchestrator system with independent context isolation. Handles complex research workflows requiring multi-perspective analysis and constitutional AI validation."

description: "Expert in unified source discovery and information access coordination using the meta framework's source intelligence system. Specializes in technology-specific source selection and cross-platform information coordination."
```

**❌ Poor Description Examples**:
```yaml
description: "Helps with code"                    # Too vague
description: "Does development tasks"             # No specific scope
description: "General AI assistant"              # Too broad
```

### Tool Selection Standards

**Minimal Necessary Tools Principle**:
```yaml
# ✅ Research specialist - focused tool set
tools: WebSearch, WebFetch, Grep, Glob, Read

# ✅ Code analysis - domain-appropriate tools
tools: Read, Grep, Glob, Bash

# ✅ Information access - MCP integration tools
tools: WebSearch, WebFetch, Grep, Glob, Read, mcp__MCP_DOCKER__search_repositories, mcp__MCP_DOCKER__get-library-docs

# ❌ Kitchen sink approach - too many tools
tools: Read, Write, Edit, MultiEdit, Grep, Glob, Bash, WebSearch, WebFetch, TodoWrite, LS, NotebookRead
```

**Domain-Specific Tool Guidelines**:
```yaml
domain_tool_patterns:
  research_agents:
    tools: "WebSearch, WebFetch, Read, Grep, Glob"
    rationale: "Source discovery and content analysis"
    
  code_analysis_agents:
    tools: "Read, Grep, Glob, Bash"
    rationale: "Code examination and execution testing"
    
  documentation_agents:
    tools: "Read, Write, Edit, MultiEdit"
    rationale: "Document creation and modification"
    
  validation_agents:
    tools: "Read, Grep, Glob"
    rationale: "Read-only analysis for safety"
    
  coordination_agents:
    tools: "TodoWrite, Edit, MultiEdit"
    rationale: "Task and project management"
    
  information_access_agents:
    tools: "WebSearch, WebFetch, Grep, Glob, Read, mcp__MCP_DOCKER__*"
    rationale: "Multi-source coordination with MCP integration"
```

### Priority and Team Assignment

**Priority Levels**:
```yaml
priority_guidelines:
  high: "Critical specialists used frequently (security, research, information-access)"
  medium: "Important but specialized use cases (performance, validation)"
  low: "Utility agents for specific scenarios (documentation, coordination)"
```

**Team Assignment Patterns**:
```yaml
team_categories:
  research: "research-specialist, information-access-specialist"
  security: "security-code-reviewer, ai-instruction-validator"
  backend: "database-expert, api-specialist, system-architect"
  frontend: "react-specialist, ui-ux-specialist"
  devops: "deployment-coordinator, infrastructure-expert"
  quality: "qa-specialist, framework-compliance-validator"
```

## Framework Integration Configuration

### Information Access Framework Integration

```yaml
---
name: "react-specialist"
description: "Comprehensive React development specialist leveraging unified source discovery framework for optimal information access"
tools: Read, Grep, Glob, WebSearch, WebFetch, mcp__MCP_DOCKER__search_repositories, mcp__MCP_DOCKER__get-library-docs
priority: high
team: frontend
framework_integration: "information-access"
specialization_domain: "react_development"
technology_mapping: "react"              # Links to technology_mappings.react
source_coordination: "parallel"          # Parallel source access pattern
---
```

### Research Orchestrator Integration

```yaml
---
name: "research-specialist"
description: "Specialized agent for comprehensive research using the 15-method orchestrator system with independent context isolation"
tools: WebSearch, WebFetch, Grep, Glob, Read
priority: high
team: research
framework_integration: "research-orchestrator"
specialization_domain: "comprehensive_research"
method_capabilities: "15_methods"         # Supports all research methods
quality_validation: "constitutional_ai"  # Built-in quality assurance
context_isolation: true                  # Prevents research pollution
---
```

### Validation Systems Integration

```yaml
---
name: "ai-instruction-validator"
description: "Specialized agent for evaluating AI agent instructions and Claude commands with multi-level validation framework"
tools: Read, Grep, Glob, Edit
priority: high
team: quality
framework_integration: "validation-systems"
specialization_domain: "ai_instruction_validation"
validation_scope: "ai_instructions_only" # Focused validation area
compliance_standards: "constitutional_ai" # Quality requirements
---
```

## Complete Configuration Examples

### Security Specialist Configuration

```yaml
---
name: "security-code-reviewer"
description: "Expert security code review specialist for identifying vulnerabilities, security anti-patterns, and compliance issues. Specializes in OWASP Top 10, secure coding practices, and security testing recommendations."
tools: Read, Grep, Glob, Bash, WebSearch
priority: high
team: security
environment: production
context_isolation: true
framework_integration: "information-access"
specialization_domain: "security_analysis"
technology_mappings: "all"               # Security applies to all technologies
quality_standards: "constitutional_ai"
coordination_pattern: "parallel"         # Can work with other specialists
expertise_areas:
  - "OWASP_top_10"
  - "secure_coding_practices"
  - "penetration_testing"
  - "compliance_validation"
---
```

### Performance Optimization Specialist

```yaml
---
name: "performance-optimizer"
description: "Performance optimization specialist for identifying bottlenecks, analyzing metrics, and implementing performance improvements across frontend, backend, and infrastructure layers."
tools: Read, Grep, Glob, Bash, WebSearch
priority: medium
team: performance
environment: production
context_isolation: true
framework_integration: "information-access"
specialization_domain: "performance_optimization"
technology_mappings: "react,typescript,python,database"
quality_standards: "constitutional_ai"
coordination_pattern: "sequential"       # Often follows analysis phases
optimization_focus:
  - "frontend_performance"
  - "backend_optimization" 
  - "database_tuning"
  - "infrastructure_scaling"
---
```

### Database Architecture Specialist

```yaml
---
name: "database-expert"
description: "Database migration and architecture specialist for schema changes, data migrations, and database optimization. Expert in PostgreSQL, MySQL, and NoSQL migration strategies."
tools: Read, Grep, Glob, Bash
priority: high
team: backend
environment: production
context_isolation: true
framework_integration: "information-access"
specialization_domain: "database_architecture"
technology_mappings: "database"
quality_standards: "constitutional_ai"
coordination_pattern: "sequential"       # Database changes require careful sequencing
database_expertise:
  - "schema_design"
  - "migration_planning"
  - "performance_optimization"
  - "data_modeling"
migration_safety:
  - "zero_downtime_strategies"
  - "rollback_procedures"
  - "data_validation"
---
```

## Validation and Quality Assurance

### Configuration Validation Checklist

**Required Field Validation**:
- [ ] **Name Present**: Agent has unique, descriptive name in kebab-case
- [ ] **Description Complete**: Clear usage criteria and expertise areas defined
- [ ] **YAML Syntax Valid**: Proper YAML formatting without syntax errors

**Optional Field Validation**:
- [ ] **Tools Appropriate**: Minimal necessary tools for domain expertise
- [ ] **Priority Set**: Appropriate priority level based on usage frequency
- [ ] **Team Assignment**: Logical team grouping for organization
- [ ] **Framework Integration**: Proper framework linkage for enhanced capabilities

**Enhanced Field Validation**:
- [ ] **Context Isolation**: Explicit context isolation enabled
- [ ] **Specialization Domain**: Clear expertise area defined
- [ ] **Quality Standards**: Constitutional AI compliance specified
- [ ] **Coordination Pattern**: Appropriate multi-agent coordination specified

### Common Configuration Errors

**❌ YAML Syntax Errors**:
```yaml
# Missing quotes for multi-word description
description: Expert in React development  # Should be quoted

# Missing space after colon
name:"react-specialist"  # Should have space

# Incorrect list format
tools: Read,Grep,Glob  # Should have spaces after commas
```

**✅ Corrected YAML**:
```yaml
name: "react-specialist"
description: "Expert in React development and optimization"
tools: Read, Grep, Glob
```

**❌ Tool Selection Errors**:
```yaml
# Too many unnecessary tools
tools: Read, Write, Edit, MultiEdit, Grep, Glob, Bash, WebSearch, WebFetch, TodoWrite, LS

# Missing essential tools for domain
name: "research-specialist"
tools: Read  # Missing WebSearch, WebFetch for research
```

**✅ Appropriate Tool Selection**:
```yaml
# Research specialist with appropriate tools
name: "research-specialist"
tools: WebSearch, WebFetch, Grep, Glob, Read

# Code analysis with focused tools
name: "code-reviewer"
tools: Read, Grep, Glob, Bash
```

## Testing and Validation Procedures

### Configuration Testing

```bash
# Validate YAML syntax
yamllint .claude/agents/*.md

# Test agent invocation
claude "use the [agent-name] to analyze this code"

# Validate framework integration
# Check if agent properly leverages configured frameworks
```

### Performance Validation

```yaml
performance_checklist:
  response_time: "Reasonable response time for domain complexity"
  token_efficiency: "Appropriate token usage for task scope"
  context_isolation: "Main conversation focus preserved"
  framework_integration: "Proper leverage of configured frameworks"
  quality_compliance: "95%+ constitutional AI compliance"
```

### Quality Metrics

```yaml
quality_validation:
  configuration_completeness: "All required and recommended fields present"
  tool_appropriateness: "Tools match domain requirements"
  framework_integration: "Proper integration with relevant frameworks"
  description_clarity: "Clear usage criteria and boundaries"
  specialization_focus: "Single responsibility principle maintained"
```

## Advanced Configuration Patterns

### Multi-Framework Integration

```yaml
---
name: "comprehensive-analyst"
description: "Advanced analyst leveraging multiple frameworks for comprehensive analysis"
tools: WebSearch, WebFetch, Read, Grep, Glob, mcp__MCP_DOCKER__search_repositories
framework_integration: "information-access,research-orchestrator,validation-systems"
specialization_domain: "multi_framework_analysis"
coordination_complexity: "high"
quality_standards: "constitutional_ai"
integration_patterns:
  information_access: "Source discovery and coordination"
  research_orchestrator: "Method selection and execution"
  validation_systems: "Quality assurance and compliance"
---
```

### Environment-Specific Configuration

```yaml
---
name: "production-deployment-coordinator"
description: "Production deployment specialist with environment-specific safety protocols"
tools: Read, Grep, Glob, Bash
priority: high
team: devops
environment: production
context_isolation: true
framework_integration: "validation-systems"
specialization_domain: "production_deployment"
safety_requirements:
  - "rollback_procedures"
  - "monitoring_integration"
  - "compliance_validation"
deployment_constraints:
  - "zero_downtime_required"
  - "comprehensive_testing"
  - "audit_trail_mandatory"
---
```

---

**Configuration Standards Version**: 2.0.0  
**Framework Integration**: Information-access, Research-orchestrator, Validation-systems  
**Quality Requirements**: 95%+ constitutional AI compliance  
**Validation Procedures**: YAML syntax + performance + quality validation

This comprehensive configuration guide ensures optimal sub-agent setup with proper framework integration, appropriate tool selection, and quality standards compliance for next-generation AI-assisted development capabilities.