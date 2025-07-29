# Commands: Slash Command System Documentation

## Overview

This section provides comprehensive documentation for Claude Code slash commands, which are expanded prompts saved as Markdown files that enable complex AI workflow automation. Commands integrate multiple frameworks and coordinate sub-agents for sophisticated development and research tasks.

## Architecture & Purpose

### Slash Command System
- **Custom Prompts**: Commands starting with `/` that execute expanded prompt templates
- **Workflow Automation**: Complex multi-step processes automated through single command invocation
- **Framework Integration**: Commands coordinate multiple AI systems (research, validation, development)
- **Context Preservation**: Commands maintain main conversation focus while orchestrating complex workflows

### Command Execution Pattern
```bash
# Command invocation
/research "React performance optimization techniques"

# Expanded execution
- Loads research.md command template
- Integrates with research orchestrator framework
- Coordinates with information-access-specialist sub-agent
- Executes 15-method research system
- Returns clean results to main conversation
```

## Current Command Categories

### Research & Analysis Commands (4 commands)
- **research.md**: Comprehensive research using 15-method orchestrator system
- **analyse-dependencies.md**: Dependency analysis and optimization recommendations
- **knowledge-status.md**: Knowledge base status and quality assessment
- **validate-knowledge-base.md**: Comprehensive knowledge validation workflows

### Development Workflow Commands (6 commands)
- **create-feature.md**: End-to-end feature development coordination
- **create-project.md**: Project scaffolding and setup automation
- **create-document.md**: Documentation generation with quality standards
- **fix-github-issue.md**: Automated issue analysis and resolution workflows
- **improve-claude.md**: AI system improvement and optimization workflows
- **orchestrate-agents.md**: Multi-agent coordination for complex tasks

### SDLC Integration Commands (3 commands)
- **sdlc-orchestrate.md**: Software Development Lifecycle orchestration
- **sdlc-validate-pr.md**: Pull request validation with multi-role analysis
- **ai-sdlc-assistant.md**: AI-assisted SDLC coordination and optimization

### Validation & Quality Assurance Commands (4 commands)
- **validate-pr.md**: Pull request validation with framework compliance
- **validation-framework.md**: Comprehensive validation system coordination
- **generate-tier-documents.md**: Tier-based documentation generation
- **gh-issue.md**: GitHub issue analysis and coordination workflows

## Command Design Principles

### Framework Integration
```markdown
# Example: research.md command structure
Execute research workflow using context-aware method selection from @research/orchestrator/config/selection-rules.yaml

## Research Workflow:
1. **Extract Research Context** using claude-orchestrator-integration.yaml
2. **Analyze Complexity** using context-analyzer.yaml scoring algorithm
3. **Select Primary Methods** with confidence threshold validation
4. **Execute Research** using multi-agent approach
5. **Generate Findings** following research-execution-log-template.yaml
6. **Save Research** according to enhanced file structure requirements
```

### Quality Standards Integration
- **Constitutional AI Compliance**: ≥95% compliance across all workflows
- **Framework Coordination**: Seamless integration with information-access, research, validation systems
- **Error Handling**: Comprehensive fallback procedures and timeout management
- **Documentation Requirements**: Mandatory file creation and quality metrics

### Multi-Agent Coordination
- **Sub-Agent Integration**: Commands can coordinate multiple specialized sub-agents
- **Context Isolation**: Sub-agent work isolated from main command execution
- **Parallel Processing**: Commands can orchestrate up to 10 concurrent sub-agents
- **Results Consolidation**: Clean integration of multi-agent outputs

## Command Categories Deep Dive

### Research Commands
**Purpose**: Automate comprehensive research workflows with quality validation
- **Primary Framework**: Research orchestrator with 15-method system
- **Sub-Agent Integration**: Research-specialist and information-access-specialist
- **Quality Standards**: Constitutional AI validation, cross-source verification
- **Output Standards**: Enhanced file structure, comprehensive documentation

### Development Commands
**Purpose**: Automate development workflows from ideation to deployment
- **Framework Integration**: SDLC orchestration, validation systems, quality gates
- **Multi-Agent Coordination**: System-architect, implementation-lead, qa-specialist
- **Quality Assurance**: Multi-role validation, framework compliance checking
- **Documentation**: Automated documentation generation and maintenance

### Validation Commands
**Purpose**: Ensure quality, compliance, and framework adherence
- **Validation Framework**: Constitutional AI, multi-level validation systems
- **Specialist Integration**: Multiple validation specialists (ai-instruction, framework-compliance, file-type)
- **Quality Metrics**: Comprehensive scoring and compliance measurement
- **Continuous Improvement**: Feedback loops and optimization recommendations

## Usage Patterns

### Simple Command Invocation
```bash
# Direct command usage
/research "Database design patterns for microservices"
```

### Command with Arguments
```bash
# Command with specific parameters
/create-feature "User authentication system" --security-focus --testing-required
```

### Workflow Integration
```bash
# Commands as part of larger workflows
/sdlc-orchestrate "Payment processing feature"
# Automatically coordinates: requirements → design → implementation → testing → deployment
```

## Quality Assurance

### Command Validation Requirements
- [ ] **Framework Integration**: Proper coordination with relevant AI systems
- [ ] **Sub-Agent Coordination**: Appropriate specialist delegation patterns
- [ ] **Error Handling**: Comprehensive fallback and timeout procedures
- [ ] **Documentation Standards**: Required file creation and quality metrics
- [ ] **Quality Compliance**: Constitutional AI and framework compliance validation

### Performance Standards
- [ ] **Execution Efficiency**: Optimized token usage and processing time
- [ ] **Context Preservation**: Main conversation focus maintained
- [ ] **Results Quality**: Actionable, comprehensive outputs
- [ ] **Integration Quality**: Seamless framework and sub-agent coordination

## Integration with AI Systems

### Framework Coordination
- **Information Access**: Commands leverage unified source discovery framework
- **Research Orchestrator**: Research commands integrate 15-method system
- **Validation Systems**: Quality assurance and compliance automation
- **Meta-Prompting**: Self-improving command execution and optimization

### Sub-Agent Integration
- **Specialist Coordination**: Commands can delegate to appropriate specialist sub-agents
- **Parallel Processing**: Multi-agent coordination for complex workflows
- **Context Isolation**: Sub-agent work doesn't contaminate command execution
- **Quality Enhancement**: Cross-specialist validation and quality assurance

---

**Current Command Count**: 17 specialized workflow commands  
**Framework Integration**: 4+ major AI systems coordinated  
**Sub-Agent Coordination**: Up to 10 parallel specialists  
**Quality Standards**: Constitutional AI compliance + framework validation

This documentation enables optimal command usage and development while maintaining integration with advanced AI coordination systems.