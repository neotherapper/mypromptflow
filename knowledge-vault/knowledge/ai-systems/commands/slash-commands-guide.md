# Slash Commands Guide: Workflow Automation System

## Overview

Claude Code slash commands are expanded prompts saved as Markdown files that enable sophisticated workflow automation. Commands integrate multiple AI frameworks, coordinate sub-agents, and execute complex multi-step processes through single invocations, all while maintaining main conversation focus.

## Command Architecture

### Core Concept
- **Expanded Prompts**: Commands starting with `/` execute comprehensive workflow templates
- **Framework Integration**: Commands coordinate Information Access, Research Orchestrator, Validation Systems
- **Sub-Agent Orchestration**: Commands can coordinate up to 10 parallel specialists
- **Context Preservation**: Complex workflows isolated from main conversation

### Execution Flow
```yaml
command_execution_pattern:
  invocation: "/research 'React performance optimization'"
  expansion: "Load research.md command template"
  integration: "Coordinate with research-orchestrator framework"
  sub_agent_coordination: "Launch research-specialist and information-access-specialist"
  framework_execution: "Execute 15-method research system"
  quality_validation: "Constitutional AI compliance checking"
  results_delivery: "Clean findings returned to main conversation"
```

## Command Categories and Capabilities

### Research & Analysis Commands (4 commands)

**research.md** - Comprehensive Research Orchestration
```yaml
primary_capability: "15-method research system with intelligent method selection"
framework_integration: "research-orchestrator + information-access"
sub_agent_coordination: "research-specialist + information-access-specialist"
quality_standards: "Constitutional AI compliance ≥95%"
output_format: "Enhanced file structure with metadata and validation"

usage_pattern: "/research 'Database design patterns for microservices'"
execution_flow:
  1. "Extract research context using claude-orchestrator-integration.yaml"
  2. "Analyze complexity using context-analyzer.yaml scoring"
  3. "Select methods using method-registry.yaml"
  4. "Execute research using multi-agent approach"
  5. "Generate findings with quality metrics"
  6. "Save research with mandatory completion validation"
```

**analyse-dependencies.md** - Dependency Analysis and Optimization
```yaml
primary_capability: "Comprehensive dependency analysis with optimization recommendations"
framework_integration: "information-access + validation-systems"
sub_agent_coordination: "information-access-specialist + framework-compliance-validator"
focus_areas: ["security_vulnerabilities", "performance_impact", "maintenance_burden"]

usage_pattern: "/analyse-dependencies package.json"
typical_outputs:
  - "Vulnerability assessment with severity ratings" 
  - "Performance impact analysis and recommendations"
  - "Upgrade pathway with compatibility validation"
  - "Alternative package suggestions with risk assessment"
```

**knowledge-status.md** - Knowledge Base Assessment
```yaml
primary_capability: "Comprehensive knowledge base status and quality assessment"
framework_integration: "validation-systems + information-access"
assessment_scope: ["completeness", "accuracy", "currency", "accessibility"]
quality_metrics: ["constitutional_compliance", "cross_reference_accuracy", "documentation_quality"]

usage_pattern: "/knowledge-status ai-systems"
assessment_areas:
  - "Documentation completeness and gap analysis"
  - "Cross-reference validation and accuracy"
  - "Framework integration and consistency"
  - "Quality standard compliance and recommendations"
```

**validate-knowledge-base.md** - Comprehensive Knowledge Validation
```yaml
primary_capability: "Full knowledge base validation with compliance checking"
framework_integration: "validation-systems (all validators)"
sub_agent_coordination: "ai-instruction-validator + framework-compliance-validator + file-type-validator"
validation_scope: ["constitutional_compliance", "framework_adherence", "quality_standards"]

execution_approach: "Parallel validation across multiple specialist validators"
quality_threshold: "95%+ compliance across all validation dimensions"
```

### Development Workflow Commands (6 commands)

**create-feature.md** - End-to-End Feature Development
```yaml
primary_capability: "Complete feature development lifecycle coordination"
framework_integration: "information-access + validation-systems"
sdlc_phases: ["requirements", "design", "implementation", "testing", "deployment"]
sub_agent_coordination: "system-architect + implementation-lead + qa-specialist"

workflow_pattern:
  requirements_phase: "requirements-analyst → structured specifications"
  design_phase: "system-architect → technical architecture" 
  implementation_phase: "implementation-lead → development coordination"
  quality_phase: "qa-specialist + security-code-reviewer → validation"
  deployment_phase: "deployment-coordinator → production readiness"
```

**create-project.md** - Project Scaffolding and Setup
```yaml
primary_capability: "Complete project initialization with best practices"
framework_integration: "information-access + validation-systems"
setup_components: ["architecture", "dependencies", "tooling", "documentation", "quality_gates"]
sub_agent_coordination: "system-architect + information-access-specialist"

automation_scope:
  - "Technology stack selection with compatibility validation"
  - "Project structure creation with best practice compliance"
  - "Development environment setup with tool integration"
  - "Quality assurance pipeline configuration"
  - "Documentation framework establishment"
```

**orchestrate-agents.md** - Multi-Agent Coordination
```yaml
primary_capability: "Advanced multi-agent coordination for complex tasks"
coordination_patterns: ["parallel", "sequential", "adaptive"]
maximum_agents: 10  # Respects architectural limits
framework_integration: "All frameworks as needed"

coordination_intelligence:
  - "Dynamic specialist selection based on task analysis"
  - "Optimal coordination pattern selection"
  - "Context isolation maintenance across all agents"
  - "Results integration with quality validation"
  
usage_scenarios:
  - "Complex analysis requiring multiple perspectives"
  - "Large codebase refactoring with quality assurance"
  - "Production incident analysis across multiple domains"
```

### SDLC Integration Commands (3 commands)

**sdlc-orchestrate.md** - Software Development Lifecycle Orchestration
```yaml
primary_capability: "Complete SDLC coordination with quality gates"
lifecycle_phases: ["ideation", "requirements", "design", "implementation", "testing", "deployment", "monitoring"]
framework_integration: "All frameworks for comprehensive coverage"
quality_gates: ["constitutional_ai", "framework_compliance", "security_validation"]

orchestration_approach:
  sequential_phases: "Dependent phases with validation checkpoints"
  parallel_specialization: "Multiple specialists within each phase"
  continuous_quality: "Quality validation throughout lifecycle"
  integration_testing: "Cross-phase validation and consistency"
```

**sdlc-validate-pr.md** - Pull Request Validation with Multi-Role Analysis
```yaml
primary_capability: "Comprehensive PR validation with multiple specialist perspectives"
validation_roles: ["architect", "security", "performance", "quality", "compliance"]
framework_integration: "validation-systems + information-access"
sub_agent_coordination: "Role-specific validators in parallel"

validation_dimensions:
  architectural_compliance: "system-architect → design consistency validation"
  security_assessment: "security-code-reviewer → vulnerability analysis"
  performance_impact: "performance-optimizer → performance regression analysis"
  quality_standards: "qa-specialist → testing and quality validation"
  framework_compliance: "framework-compliance-validator → standard adherence"
```

### Validation & Quality Assurance Commands (4 commands)

**validate-pr.md** - Pull Request Framework Compliance Validation
```yaml
primary_capability: "Framework compliance validation for pull requests"
validation_frameworks: ["ai_instruction_design", "constitutional_ai", "framework_standards"]
sub_agent_coordination: "Parallel validation specialists"
compliance_threshold: "95%+ across all validation dimensions"

validation_approach:
  file_analysis: "Dynamic routing to appropriate specialists based on file types"
  framework_compliance: "Standard adherence and best practice validation"
  quality_assurance: "Constitutional AI and quality standard compliance"  
  integration_testing: "Cross-framework validation and consistency checking"
```

**validation-framework.md** - Comprehensive Validation System Coordination
```yaml
primary_capability: "Complete validation system orchestration"
validation_levels: ["individual", "integration", "system", "compliance"]
framework_integration: "validation-systems (primary) + all supporting frameworks"
validator_coordination: "All available validation specialists"

system_coverage:
  ai_instruction_validation: "AI agent instruction quality and compliance"
  framework_compliance: "Adherence to framework standards and patterns"
  file_type_validation: "Technology-specific validation and best practices"
  constitutional_compliance: "Ethical and quality standards validation"
```

## Command Design Principles

### Framework Integration Standards

**Multi-Framework Coordination**:
```yaml
integration_requirements:
  primary_framework: "Main framework for command functionality"
  supporting_frameworks: "Additional frameworks for enhanced capabilities"
  quality_validation: "Constitutional AI compliance across all integrations"
  
  example_integration:
    primary: "research-orchestrator (for research commands)"
    supporting: "information-access (for source discovery)"
    validation: "validation-systems (for quality assurance)"
    enhancement: "meta-prompting (for continuous improvement)"
```

**Framework Loading Pattern**:
```markdown
# Standard command structure
Execute [workflow] using context-aware method selection from @[framework]/config/[configuration].yaml

## Workflow Steps:
1. **Extract Context** using [framework-specific-integration].yaml
2. **Analyze Complexity** using [framework]/engines/[analyzer].yaml
3. **Select Methods** with confidence threshold validation
4. **Execute Workflow** using multi-agent approach
5. **Generate Results** following [output-template].yaml
6. **Validate Quality** according to constitutional AI standards
```

### Sub-Agent Coordination Standards

**Parallel Coordination Pattern**:
```yaml
multi_agent_coordination:
  specialist_selection: "Dynamic routing based on task requirements"
  parallel_execution: "Up to 10 concurrent specialists"
  context_isolation: "Independent contexts for each specialist"
  results_integration: "Clean consolidation without pollution"
  quality_assurance: "Cross-specialist validation"

  coordination_example:
    trigger: "/sdlc-validate-pr complex-feature-branch"
    orchestration:
      - "system-architect → architectural compliance"
      - "security-code-reviewer → security assessment"
      - "performance-optimizer → performance analysis"
      - "qa-specialist → quality validation"
      - "framework-compliance-validator → standard compliance"
```

### Quality Assurance Integration

**Constitutional AI Compliance**:
```yaml
quality_standards:
  accuracy_requirement: "95%+ factual accuracy across all outputs"
  transparency_standard: "Clear documentation of methods and sources"
  completeness_threshold: "Comprehensive coverage of requirements"
  responsibility_compliance: "Ethical and safe execution patterns"
  integrity_assurance: "Consistent and reliable command behavior"

validation_checkpoints:
  pre_execution: "Command configuration and framework integration validation"
  during_execution: "Real-time quality monitoring and compliance checking"
  post_execution: "Results validation and constitutional compliance verification"
```

## Advanced Command Patterns

### Meta-Prompting Enhanced Commands

**Self-Improving Command Execution**:
```yaml
meta_prompting_integration:
  performance_measurement: "Track command effectiveness and execution quality"
  optimization_cycles: "Iterative improvement of command workflows"
  framework_enhancement: "Dynamic optimization of framework coordination"
  quality_evolution: "Continuous improvement of constitutional compliance"

  enhancement_approach:
    measurement: "Command execution metrics and quality scores"
    analysis: "Identification of optimization opportunities"
    optimization: "Automated improvement of command patterns"
    validation: "Constitutional AI compliance for all improvements"
```

### Adaptive Command Selection

**Intelligent Command Routing**:
```yaml
command_selection_intelligence:
  context_analysis: "Automatic analysis of user request complexity and domain"
  command_matching: "Optimal command selection based on capabilities"
  framework_optimization: "Best framework combination for requirements"
  quality_prediction: "Expected quality outcomes and resource requirements"

  selection_logic:
    simple_requests: "Direct framework usage with minimal coordination"
    moderate_requests: "Single command with framework integration"
    complex_requests: "Multi-command coordination with parallel processing"
```

## Command Creation and Optimization

### Command Development Workflow

**Phase 1: Requirements Analysis**
```yaml
command_planning:
  workflow_identification: "What process needs automation?"
  framework_requirements: "Which frameworks provide necessary capabilities?"
  sub_agent_coordination: "What specialists are needed?"
  quality_standards: "What constitutional AI requirements apply?"
  integration_complexity: "How do frameworks need to coordinate?"
```

**Phase 2: Implementation**
```yaml
command_implementation:
  framework_integration: "Proper loading and coordination of required frameworks"
  sub_agent_orchestration: "Appropriate specialist selection and coordination"
  quality_validation: "Constitutional AI compliance integration"
  error_handling: "Comprehensive fallback procedures and timeout management"
  documentation: "Clear usage patterns and expected outcomes"
```

**Phase 3: Optimization**
```yaml
command_optimization:
  performance_measurement: "Execution time, token usage, quality metrics"
  framework_efficiency: "Optimal framework coordination patterns"
  sub_agent_coordination: "Efficient specialist usage and results integration"
  meta_prompting: "Self-improving command execution patterns"
```

## Usage Guidelines and Best Practices

### Command Invocation Patterns

**Simple Command Usage**:
```bash
# Direct command with clear parameters
/research "React performance optimization techniques"
/validate-pr feature/user-authentication
/create-feature "Payment processing system"
```

**Complex Command Usage**:
```bash
# Commands with specific requirements
/sdlc-orchestrate "E-commerce checkout flow" --security-critical --performance-focused
/orchestrate-agents "Production incident analysis" --parallel-investigation --comprehensive-report
```

### Quality Assurance for Commands

**Command Validation Checklist**:
- [ ] **Framework Integration**: Proper coordination with required frameworks
- [ ] **Sub-Agent Coordination**: Appropriate specialist selection and orchestration
- [ ] **Quality Standards**: Constitutional AI compliance ≥95%
- [ ] **Error Handling**: Comprehensive fallback procedures
- [ ] **Documentation**: Clear usage patterns and expected outcomes
- [ ] **Performance**: Efficient resource usage and token optimization

### Performance Optimization

**Resource Management**:
```yaml
efficiency_optimization:
  framework_loading: "Load only required frameworks for command"
  sub_agent_usage: "Optimal specialist selection for task requirements"
  parallel_processing: "Balance speed vs token usage based on complexity"
  context_management: "Efficient context loading and isolation"
  results_integration: "Clean consolidation without redundancy"
```

---

**Current Command Portfolio**: 17 specialized workflow commands  
**Framework Integration**: 4+ major AI systems coordinated per command  
**Sub-Agent Orchestration**: Up to 10 parallel specialists  
**Quality Standards**: 95%+ constitutional AI compliance with comprehensive validation

This comprehensive guide enables optimal command usage, development, and optimization while maintaining integration with advanced AI coordination systems and quality standards.