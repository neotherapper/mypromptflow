# Sub-Agents: Specialized AI Assistant Documentation

## Overview

This section provides comprehensive documentation for Claude Code sub-agents, including best practices, configuration standards, and detailed guides for all current agents. Sub-agents provide specialized expertise with independent 200k-token context windows, enabling parallel processing while preventing context pollution.

## Key Capabilities

### Context Isolation Revolution
- **Independent Context Windows**: Each sub-agent operates with dedicated 200k-token space
- **Context Pollution Prevention**: Main conversations preserved from sub-agent implementation details
- **Parallel Processing**: Up to 10 concurrent sub-agents for complex multi-faceted tasks
- **Clean Results Delivery**: Summarized findings without contaminating main context

### Architectural Constraints
- **No Sub-Agent Spawning**: Sub-agents CANNOT create other sub-agents (critical limitation)
- **Main Session Orchestration**: Primary Claude session must coordinate all sub-agent delegation
- **Token Multiplication**: Linear token usage increase with parallel execution (3x agents = 3x tokens)
- **Queue Management**: Additional tasks automatically queued when exceeding 10 concurrent limit

## Documentation Structure

### Core Guides
- **best-practices.md**: Comprehensive sub-agent design and usage best practices
- **configuration-guide.md**: YAML frontmatter standards and tool selection
- **usage-patterns.md**: Sequential, parallel, and coordination patterns

### Current Agents Documentation
- **current-agents/**: Complete documentation for all 21 specialized sub-agents
- **Agent Categories**:
  - Validation Specialists (ai-instruction-validator, framework-compliance-validator, etc.)
  - Development Specialists (system-architect, implementation-lead, ui-ux-specialist)
  - Research Specialists (research-specialist, information-access-specialist)
  - Coordination Specialists (project-manager, task-coordinator, capacity-planner)

## Agent Design Principles

### Single Responsibility Principle
```yaml
# ✅ GOOD: Focused expertise
name: "security-code-reviewer"
description: "Expert security code review specialist for vulnerabilities and compliance"
tools: Read, Grep, Glob, WebSearch
```

### Context Isolation Validation
```yaml
# ✅ GOOD: Clean context separation
Main Context: Architecture discussion (preserved)
├── Sub-Agent: Security review (isolated 200k context)
├── Sub-Agent: Performance analysis (isolated 200k context)
└── Results: Clean summaries returned to main context
```

### Tool Minimization
```yaml
# ✅ GOOD: Minimal necessary tools
tools: Read, Grep, Glob

# ❌ AVOID: Kitchen sink approach
tools: Read, Write, Edit, MultiEdit, Grep, Glob, Bash, WebSearch, WebFetch, TodoWrite
```

## Usage Patterns

### Sequential Processing
```yaml
workflow_pattern:
  phase_1: "code-analyzer → Identifies optimization opportunities"
  phase_2: "performance-optimizer → Implements improvements"
  phase_3: "test-generator → Creates validation tests"
  phase_4: "deployment-validator → Confirms production readiness"
```

### Parallel Investigation
```yaml
parallel_pattern:
  complex_problem: "Multi-aspect analysis"
  concurrent_agents:
    - frontend_specialist: "UI/UX analysis"
    - backend_specialist: "API and data layer review"
    - security_auditor: "Security implications"
    - infrastructure_expert: "Deployment considerations"
```

## Quality Standards

### Configuration Validation Checklist
- [ ] **Single Responsibility**: Agent has one clear, focused purpose
- [ ] **Complete Coverage**: Agent handles all tasks within its domain
- [ ] **Minimal Tools**: Only necessary tools assigned
- [ ] **Clear Boundaries**: Obvious when to use vs other agents
- [ ] **Context Isolation**: Agent preserves main conversation focus

### Performance Requirements
- [ ] **Concurrency Compliance**: Total agents ≤ 10 for parallel execution
- [ ] **Token Efficiency**: Tools and prompts optimized for token usage
- [ ] **Response Quality**: Agent delivers actionable, clear results
- [ ] **Integration Quality**: Clean coordination with main session

## Anti-Patterns to Avoid

### Configuration Anti-Patterns
- ❌ **Overly Broad Agents**: "full-stack-everything-agent"
- ❌ **Over-Specialization**: Too many micro-specialists requiring constant coordination
- ❌ **Vague Descriptions**: Unclear purpose and usage criteria
- ❌ **Tool Overload**: Kitchen sink tool assignment

### Usage Anti-Patterns
- ❌ **Context Pollution**: Agents leaking implementation details to main conversation
- ❌ **Micro-Management**: Too many narrow agents requiring constant coordination
- ❌ **Nested Delegation**: Attempting to have sub-agents create other sub-agents

## Integration with Frameworks

### Information Access Framework
- Sub-agents can leverage unified source discovery framework
- Technology-specific source coordination (React, TypeScript, Python, etc.)
- MCP server integration for comprehensive information access

### Research Orchestrator
- Research-specialist sub-agent integrates 15-method research system
- Context isolation prevents research contamination of main conversations
- Quality validation through constitutional AI principles

### Validation Systems
- Multiple validation specialists ensure quality and compliance
- Cross-framework validation and quality assurance
- Constitutional AI integration for continuous improvement

---

**Current Agent Count**: 21 specialized sub-agents  
**Maximum Concurrent**: 10 parallel executions  
**Context Per Agent**: 200k tokens (independent)  
**Token Usage**: Linear multiplication with parallel execution

This documentation enables optimal sub-agent implementation while avoiding common pitfalls and maximizing the revolutionary potential of context-isolated, parallel AI assistance.