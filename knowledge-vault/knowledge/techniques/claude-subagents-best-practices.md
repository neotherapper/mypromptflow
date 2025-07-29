# Claude Sub-Agents Best Practices

## Overview

Claude Code sub-agents provide specialized AI assistants with independent 200k-token context windows, enabling parallel processing while preventing context pollution. This guide consolidates best practices from comprehensive research analysis to ensure optimal sub-agent implementation.

**Key Innovation**: Sub-agents solve the fundamental "context pollution" problem by providing complete context isolation while enabling up to 10x performance improvements through parallel processing.

## Architecture Patterns

### Single Responsibility Principle

**✅ RECOMMENDED PATTERN**:

```yaml
# Good: Focused, specific expertise
---
name: "security-code-reviewer"
description: "Expert security code review specialist for identifying vulnerabilities, security anti-patterns, and compliance issues"
tools: Read, Grep, Glob, WebSearch
priority: high
team: security
---
```

**❌ ANTI-PATTERN - Overly Broad Agents**:

```yaml
# Avoid: Too general, unclear responsibilities
---
name: "full-stack-everything-agent"
description: "Handles all development tasks including frontend, backend, database, security, testing, and deployment"
tools: # All possible tools
---
```

### Optimal Granularity Guidelines

**✅ RECOMMENDED APPROACH**:

```bash
# Better: Single comprehensive specialist per domain
.claude/agents/
├── react-specialist.md          # Comprehensive React expertise
├── security-auditor.md          # Complete security analysis
├── performance-optimizer.md     # Full performance assessment
└── database-expert.md           # Complete database operations
```

**❌ ANTI-PATTERN - Over-Specialization**:

```bash
# Avoid: Too many micro-specialists
.claude/agents/
├── react-component-creator.md   # Too narrow
├── react-hook-optimizer.md      # Too narrow
├── react-state-manager.md       # Too narrow
├── react-performance-tuner.md   # Too narrow
└── react-testing-helper.md      # Too narrow
```

**Granularity Decision Framework**:

1. **Single Domain Focus**: Each agent covers one coherent problem domain
2. **Complete Capability**: Agent can handle all aspects within its domain
3. **Clear Boundaries**: Obvious when to use this agent vs others
4. **Manageable Scope**: Can be effectively described in 200k context window

## Configuration Standards

### YAML Frontmatter Requirements

**Essential Fields**:

```yaml
---
name: "unique-agent-identifier" # Required: Unique, descriptive
description: "Clear purpose and usage criteria" # Required: When to invoke
tools: Read, Grep, Glob # Optional: Minimal necessary set
priority: high # Optional: high/medium/low
team: backend # Optional: Team assignment
environment: production # Optional: Environment-specific
---
```

**Configuration Validation Checklist**:

- [ ] Name is unique and descriptive
- [ ] Description clearly states when to use the agent
- [ ] Tools list includes only necessary tools (minimal set principle)
- [ ] Priority reflects actual delegation preference
- [ ] Team/environment tags enable proper organization

### Tool Selection Best Practices

**Minimal Necessary Tools Principle**:

```yaml
# ✅ Good: Only essential tools
tools: Read, Grep, Glob

# ❌ Avoid: Kitchen sink approach
tools: Read, Write, Edit, MultiEdit, Grep, Glob, Bash, WebSearch, WebFetch, TodoWrite
```

**Tool Assignment Guidelines**:

- **Research Agents**: WebSearch, WebFetch, Read, Grep, Glob
- **Code Analysis**: Read, Grep, Glob, Bash (for execution)
- **Documentation**: Read, Write, Edit, MultiEdit
- **Validation**: Read, Grep, Glob (read-only for safety)
- **Coordination**: TodoWrite, Edit, MultiEdit (management tools)

## Performance Optimization

### Concurrency Limits and Token Management

**Performance Characteristics**:

- **Maximum Concurrent Sub-Agents**: 10 simultaneous executions
- **Context Window**: Full 200k tokens per sub-agent
- **Token Usage**: Linear multiplication with parallel execution
- **Queue Management**: Additional tasks automatically queued

**Token Usage Planning**:

```yaml
performance_planning:
  single_agent: "Standard token consumption"
  parallel_3_agents: "~3x token usage, 3x faster completion"
  parallel_5_agents: "~5x token usage, 5x faster completion"
  parallel_10_agents: "~10x token usage, 10x faster completion"

  optimization_strategy:
    - "Use parallel processing for independent tasks"
    - "Sequential execution for dependent workflows"
    - "Monitor token usage vs performance gains"
```

### Context Isolation Validation

**Context Independence Requirements**:

```yaml
context_isolation_checklist:
  - independent_context_window: "Each agent operates in isolated 200k-token space"
  - no_context_sharing: "Agents cannot access each other's conversations"
  - clean_result_delivery: "Results summarized without implementation details"
  - pollution_prevention: "Main conversation preserved from sub-agent work"
```

**Validation Patterns**:

```yaml
# ✅ Good: Context isolation preserved
Main Context: Architecture discussion
├── Sub-Agent: Security review (isolated)
├── Sub-Agent: Performance analysis (isolated)
└── Results: Clean summaries returned to main context

# ❌ Avoid: Context bleeding
Main Context: Architecture + security details + performance logs + implementation specifics
```

## Creation Workflow

### Phase 1: Claude-Generated Foundation

**Recommended Approach**:

```
User: "Generate a sub-agent for React performance optimization"

Claude generates:
├── Proper YAML frontmatter
├── Focused system prompt
├── Relevant tool configuration
├── Best practice compliance
└── Usage examples
```

**Generation Prompts**:

- "Create a sub-agent for [specific domain] with [clear boundaries]"
- "Generate a specialist agent for [problem area] focusing on [key capabilities]"
- "Design a sub-agent that handles [specific tasks] while avoiding [scope creep areas]"

### Phase 2: Iterative Refinement

**Refinement Process**:

```bash
# 1. Initial Generation
claude "create a database performance sub-agent"

# 2. Save and Test
cp generated-agent.md .claude/agents/db-performance.md

# 3. Iterate Based on Results
claude "refine the db-performance sub-agent based on this usage feedback..."

# 4. Validate Against Best Practices
# Use .claude/agents/claude-agent-validator.md for configuration validation
```

**Refinement Focus Areas**:

- **Prompt Clarity**: Ensure system prompt is clear and actionable
- **Tool Optimization**: Remove unnecessary tools, add missing essential ones
- **Scope Boundaries**: Clarify what the agent does and doesn't handle
- **Integration Patterns**: Improve coordination with main session

### Phase 3: Focused Responsibility Design

**Design Principles**:

1. **Single Clear Purpose**: Agent has one primary responsibility
2. **Domain Expertise**: Deep knowledge in specific problem area
3. **Predictable Behavior**: Consistent response patterns
4. **Clear Invocation**: Obvious when to use this agent

**Responsibility Validation Questions**:

- Can this agent's purpose be described in one sentence?
- Are there clear boundaries for when to use vs not use this agent?
- Does this agent duplicate capabilities of existing agents?
- Can this agent handle all reasonable tasks within its domain?

## Strategic Usage Patterns

### Global vs Project-Level Agents

**Global Agents (~/.claude/agents/)**:

```bash
# General-purpose specialists across projects
~/.claude/agents/
├── security-code-reviewer.md    # Universal security expertise
├── performance-optimizer.md     # Cross-language performance analysis
├── api-test-generator.md        # General API testing patterns
├── tech-doc-generator.md        # Documentation specialist
└── infrastructure-architect.md  # Cloud and infrastructure expertise
```

**Project Agents (.claude/agents/)**:

```bash
# Domain-specific and project-specific specialists
.claude/agents/
├── insurance-domain-expert.md      # Industry-specific knowledge
├── legacy-mainframe-specialist.md  # Project-specific technology
├── deployment-coordinator.md       # Environment-specific procedures
└── team-workflow-manager.md        # Team-specific processes
```

**Precedence Rules**:

- Project-level agents take precedence over global agents
- Use project agents for domain-specific expertise
- Use global agents for reusable, cross-project capabilities

### Version Control Integration

**Recommended Practices**:

```bash
# ✅ Version control project-specific agents
git add .claude/agents/
git commit -m "Add project-specific Claude sub-agents"

# ✅ Document agent purposes in project README
echo "## Sub-Agents" >> README.md
echo "- project-reviewer.md: Domain-specific code review" >> README.md

# ⚠️ Consider security for sensitive agents
echo ".claude/agents/secrets-*" >> .gitignore
```

## Advanced Usage Patterns

### Sequential Sub-Agent Chaining

**Workflow Pattern**:

```yaml
sequential_workflow:
  phase_1: "code-analyzer → Identifies optimization opportunities"
  phase_2: "performance-optimizer → Implements performance improvements"
  phase_3: "test-generator → Creates performance validation tests"
  phase_4: "deployment-validator → Confirms production readiness"
```

### Parallel Investigation Pattern

**Multi-Aspect Analysis**:

```yaml
parallel_investigation:
  complex_problem: "Feature development analysis"
  concurrent_agents:
    - frontend_specialist: "UI/UX implementation analysis"
    - backend_specialist: "API and data layer review"
    - infrastructure_expert: "Deployment and scaling evaluation"
    - security_auditor: "Security implications assessment"

  coordination: "Each agent works independently, reports findings"
  integration: "Main session synthesizes all perspectives"
```

### Dynamic Agent Selection

**Context-Aware Routing**:

```yaml
routing_patterns:
  file_type_routing:
    "*.tsx, *.jsx": "frontend-specialist"
    "*.py, *.sql": "backend-specialist"
    "*.yml, *.yaml": "infrastructure-expert"
    "security-sensitive": "security-auditor"

  complexity_routing:
    simple_tasks: "general-purpose agent"
    domain_specific: "specialized domain agent"
    cross_cutting: "multiple parallel agents"
```

## Anti-Patterns and Common Mistakes

### Configuration Anti-Patterns

**❌ Overly Complex Tool Lists**:

```yaml
# Avoid: Kitchen sink tool assignment
tools: Read, Write, Edit, MultiEdit, Grep, Glob, Bash, WebSearch, WebFetch, TodoWrite, LS, NotebookRead, NotebookEdit
```

**❌ Vague Descriptions**:

```yaml
# Avoid: Unclear purpose
description: "Helps with development tasks and other stuff"
```

**❌ Conflicting Agent Purposes**:

```yaml
# Avoid: Multiple agents with overlapping responsibilities
agents:
  - name: "code-reviewer"
  - name: "quality-checker" # Overlaps with code-reviewer
  - name: "ai-instruction-validator" # Better: Focused AI instruction validation
  - name: "framework-compliance-validator" # Better: Focused framework compliance
  - name: "file-type-validator" # Better: Focused file type validation
```

### Usage Anti-Patterns

**❌ Context Pollution Through Poor Design**:

```bash
# Avoid: Agents that leak implementation details
Agent returns: "After reviewing 500 lines of code, examining 15 functions,
checking 8 security patterns, validating 12 performance metrics..."

# Better: Clean result summary
Agent returns: "Security review complete. Found 2 high-priority issues.
Recommendations: Implement input validation and upgrade authentication library."
```

**❌ Micro-Management Through Over-Specialization**:

```bash
# Avoid: Too many narrow agents requiring constant coordination
.claude/agents/
├── button-component-creator.md
├── form-validator.md
├── css-styler.md
├── prop-type-checker.md
└── event-handler-writer.md

# Better: Comprehensive domain coverage
.claude/agents/
├── frontend-component-specialist.md  # Handles all UI component work
└── frontend-integration-specialist.md  # Handles component integration
```

## Quality Assurance

### Validation Checklist

**Agent Configuration Validation**:

- [ ] **Single Responsibility**: Agent has one clear, focused purpose
- [ ] **Complete Coverage**: Agent can handle all tasks within its domain
- [ ] **Minimal Tools**: Only necessary tools assigned
- [ ] **Clear Boundaries**: Obvious when to use vs other agents
- [ ] **Context Isolation**: Agent preserves main conversation focus

**Performance Validation**:

- [ ] **Concurrency Compliance**: Total agents ≤ 10 for parallel execution
- [ ] **Token Efficiency**: Tools and prompts optimized for token usage
- [ ] **Response Quality**: Agent delivers actionable, clear results
- [ ] **Integration Quality**: Clean coordination with main session

### Continuous Improvement

**Monitoring Patterns**:

```yaml
improvement_cycle:
  usage_analysis: "Track which agents are used most frequently"
  effectiveness_review: "Evaluate agent output quality and relevance"
  consolidation_opportunities: "Identify overlapping or underused agents"
  optimization_refinement: "Improve prompts and tool assignments"
```

**Success Metrics**:

- **Agent Utilization**: Balanced usage across agent portfolio
- **Task Completion**: Agents successfully complete delegated tasks
- **Context Preservation**: Main conversations remain focused
- **Performance Gains**: Measurable improvements in development velocity

## Integration with Existing Systems

### MCP Framework Integration

**Server Coordination**:

```yaml
mcp_integration:
  information_access: "Agents coordinate with information-access framework"
  validation_framework: "Agents use meta/validation standards"
  research_orchestrator: "Research agents integrate with 15-method system"
  knowledge_vault: "Agents access structured knowledge effectively"
```

### CI/CD Pipeline Integration

**Automated Validation**:

```yaml
# GitHub Actions example
name: Sub-Agent Validation
on: [push, pull_request]
jobs:
  validate-agents:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Validate Sub-Agent Configurations
        run: |
          # Validate YAML frontmatter
          find .claude/agents -name "*.md" -exec yamllint {} \;
          # Check against best practices
          claude-agent-validator .claude/agents/
```

This comprehensive guide ensures optimal Claude sub-agent implementation while avoiding common pitfalls and maximizing the revolutionary potential of context-isolated, parallel AI assistance.
