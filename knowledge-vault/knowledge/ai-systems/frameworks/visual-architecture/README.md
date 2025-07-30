# Visual Research Architecture Documentation

## Overview

Comprehensive visual documentation of the tree-leaf research framework architecture, showing how research methods adapt to different AI agent capabilities through Mermaid diagrams.

## Quick Navigation

### 🏗️ Reference Architectures
- **[Claude Desktop Research Pattern](reference-architectures/claude-desktop-research-pattern.md)** - Anthropic's proven orchestrator-worker pattern (90.2% performance improvement)
- **[Tree-Leaf Architecture Overview](reference-architectures/tree-leaf-architecture-overview.md)** - Our hybrid approach supporting both subagent-capable and leaf agents
- **[Agent Capability Matrix](reference-architectures/agent-capability-matrix.md)** - Method compatibility across different agent types

### 🔄 Research Execution Flows
- **[Simple Research Flow](research-execution-flows/simple-research-flow.md)** - 1-2 method coordination for basic queries
- **[Moderate Research Flow](research-execution-flows/moderate-research-flow.md)** - 2-4 method coordination for complex analysis
- **[Complex Research Flow](research-execution-flows/complex-research-flow.md)** - 3-7 method coordination for comprehensive research
- **[Research Orchestration Patterns](research-execution-flows/research-orchestration-patterns.md)** - Coordination patterns and sequence diagrams

### 📊 Method-Specific Diagrams

#### Multi-Agent Methods (Tree Capability)
- **[Multi-Perspective Approach](method-diagrams/multi-agent-methods/multi-perspective-approach.md)** - 4 perspective specialists vs enhanced single prompt
- **[Complex Research](method-diagrams/multi-agent-methods/complex-research.md)** - 5 business modules vs comprehensive analysis
- **[Ensemble Methods](method-diagrams/multi-agent-methods/ensemble-methods.md)** - Multiple method coordination vs sequential execution
- **[Tree of Thoughts](method-diagrams/multi-agent-methods/tree-of-thoughts.md)** - Multi-path exploration vs linear reasoning

#### Single-Agent Methods (Leaf Compatible)
- **[Step-by-Step Research](method-diagrams/single-agent-methods/step-by-step-research.md)** - 5-phase systematic progression
- **[Universal Research](method-diagrams/single-agent-methods/universal-research.md)** - Comprehensive template approach
- **[Constitutional AI](method-diagrams/single-agent-methods/constitutional-ai.md)** - Quality validation and self-correction
- **[Self-Consistency](method-diagrams/single-agent-methods/self-consistency.md)** - Consensus building and error reduction

#### Hybrid Methods (Adaptive)
- **[Domain Adaptive](method-diagrams/hybrid-methods/domain-adaptive.md)** - Domain-specific expertise adaptation
- **[Modular Task Decomposition](method-diagrams/hybrid-methods/modular-task-decomposition.md)** - Task breakdown and parallel planning
- **[Iterative Research Refinement](method-diagrams/hybrid-methods/iterative-research-refinement.md)** - Self-improvement and quality progression

## Architecture Principles

### Tree-Leaf Design Pattern
```
Tree Agents (Claude Code): Can spawn subagents → Multi-agent methods
Leaf Agents (Gemini): Cannot spawn subagents → Enhanced single prompts
```

### Universal Research Outcomes
Both tree and leaf execution paths produce equivalent research quality through:
- **Tree Path**: Parallel specialized agents with coordination
- **Leaf Path**: Enhanced prompts with comprehensive analysis templates

### MCP Intelligence Integration
All methods coordinate with domain-specific MCP servers:
- **Academic Research**: arXiv, Semantic Scholar, PubMed
- **Technical Documentation**: GitHub, Git, Filesystem
- **Business Intelligence**: Bright Data, Linear, Atlassian
- **Infrastructure Research**: AWS, Redis, Qdrant, Sentry

## Usage Scenarios

### For Implementers
- **System Architecture**: Reference architectures show proven patterns
- **Method Selection**: Capability matrix guides agent-method pairing
- **Integration Planning**: Execution flows demonstrate coordination patterns

### For Researchers
- **Method Understanding**: Visual breakdown of research approaches
- **Quality Patterns**: See how validation and enhancement work
- **Coordination Models**: Understand orchestration vs direct execution

### For AI Agents
- **Capability Assessment**: Understand tree vs leaf execution modes
- **Method Adaptation**: See how methods adjust to agent capabilities
- **Quality Standards**: Visual representation of validation requirements

## Source References

- **Claude Desktop Research**: Anthropic engineering documentation and performance analysis
- **Multi-Agent Coordination**: Existing multi_perspective_approach and complex_research implementations
- **Method Framework**: 15-method research orchestrator with constitutional AI compliance
- **MCP Intelligence**: 2,200+ server registry with tier-based prioritization

This visual documentation provides comprehensive understanding of how research methods achieve consistent quality outcomes across different AI agent architectures.