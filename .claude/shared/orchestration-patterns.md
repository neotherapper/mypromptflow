# Orchestration Patterns - Shared Instructions

**Purpose**: Reusable multi-agent coordination patterns for complex workflow orchestration across SDLC stages.

**Usage**: Referenced by:
- `orchestrate-agents` command for multi-agent workflows
- SDLC stage coordinators for workflow management
- Complex feature development orchestration
- Multi-specialist task coordination

## Core Orchestration Framework

### 1. Agent Spawning Patterns

**Task-Based Agent Spawning**:
```yaml
spawning_patterns:
  parallel_execution:
    description: "Spawn multiple agents simultaneously for independent tasks"
    use_cases:
      - Multi-file validation (security, quality, testing)
      - Feature development (frontend, backend, documentation)
      - Research coordination (market analysis, technical feasibility)
    
    execution_pattern:
      - Analyze dependencies and identify independent tasks
      - Spawn agents with isolated contexts and specific tools
      - Monitor progress with timeout handling
      - Aggregate results when all agents complete
  
  sequential_coordination:
    description: "Chain agent execution where outputs become inputs"
    use_cases:
      - Requirements → Design → Implementation → Testing
      - Research → Analysis → Documentation → Validation
      - Planning → Execution → Review → Deployment
    
    execution_pattern:
      - Execute Agent A with initial context
      - Pass Agent A outputs to Agent B context
      - Continue chain until final deliverable
      - Validate end-to-end workflow completion
  
  conditional_branching:
    description: "Spawn different agents based on analysis results"
    use_cases:
      - File type detection → Appropriate specialist
      - Complexity assessment → Suitable methodology
      - Error detection → Specialized recovery agent
    
    execution_pattern:
      - Analyze input conditions and context
      - Apply decision rules for agent selection
      - Spawn appropriate specialist with targeted context
      - Handle fallback scenarios for edge cases
```

### 2. Context Management Patterns

**Context Isolation & Sharing**:
```yaml
context_management:
  isolated_contexts:
    description: "Each agent operates in independent context"
    benefits:
      - Prevents context pollution between agents
      - Enables parallel processing without interference
      - Maintains focused expertise per agent
    
    implementation:
      - Use Task tool with independent context windows
      - Provide specific context for each agent's role
      - Avoid sharing internal implementation details
  
  selective_context_sharing:
    description: "Share only relevant context between agents"
    patterns:
      - Requirements shared with design and implementation agents
      - Architecture decisions shared with all development agents
      - Test results shared with quality assurance agents
    
    implementation:
      - Extract relevant context from previous agent outputs
      - Create curated context packages for downstream agents
      - Maintain context traceability for debugging
  
  progressive_context_building:
    description: "Build comprehensive context through agent chain"
    use_cases:
      - Feature development lifecycle
      - Research and analysis workflows
      - Complex problem-solving sequences
    
    implementation:
      - Start with minimal context for first agent
      - Accumulate relevant outputs at each stage
      - Build comprehensive context for final deliverable
```

### 3. Result Aggregation Patterns

**Multi-Agent Result Synthesis**:
```yaml
aggregation_strategies:
  comprehensive_synthesis:
    description: "Combine all agent outputs into cohesive deliverable"
    use_cases:
      - Feature documentation from multiple specialists
      - Security + Quality + Performance analysis reports
      - Multi-perspective research findings
    
    process:
      - Collect all agent outputs with metadata
      - Identify overlapping and complementary findings
      - Resolve conflicts through prioritization rules
      - Generate unified deliverable with attribution
  
  prioritized_consolidation:
    description: "Merge results with importance weighting"
    priority_rules:
      - Security findings: Highest priority
      - Critical functionality: High priority
      - Performance optimizations: Medium priority
      - Style improvements: Low priority
    
    process:
      - Categorize findings by priority level
      - Apply consolidation rules per category
      - Generate prioritized action items
      - Create implementation roadmap
  
  consensus_building:
    description: "Resolve conflicting recommendations between agents"
    conflict_resolution:
      - Technical conflicts: Defer to architecture specialist
      - Security conflicts: Defer to security specialist
      - UX conflicts: Defer to design specialist
      - Performance conflicts: Benchmark-based resolution
    
    process:
      - Identify conflicting recommendations
      - Apply domain expertise rules
      - Generate compromise solutions where needed
      - Document decision rationale
```

### 4. SDLC Stage Orchestration

**Stage-Specific Coordination Patterns**:

#### Stage 1: Business Ideation & Requirements
```yaml
requirements_orchestration:
  agent_sequence:
    - requirements_analyst: "Extract and formalize requirements"
    - technical_feasibility_expert: "Assess implementation feasibility"
    - jira_integration_agent: "Create structured tickets"
  
  coordination_pattern: sequential_with_feedback
  deliverables:
    - Formal requirements documentation
    - Technical feasibility assessment
    - JIRA epic and story structure
    - Initial effort estimation
```

#### Stage 2: Design & Architecture
```yaml
design_orchestration:
  agent_coordination:
    - ui_ux_specialist: "Create user interface designs"
    - system_architect: "Define technical architecture"
    - design_validator: "Ensure design system compliance"
  
  coordination_pattern: parallel_then_integration
  deliverables:
    - UI/UX designs and specifications
    - System architecture documentation
    - Component and API specifications
    - Design-to-development handoff materials
```

#### Stage 4: Implementation
```yaml
implementation_orchestration:
  agent_workflow:
    - code_reviewer: "Validate implementation quality"
    - security_auditor: "Ensure security compliance"
    - test_generator: "Create comprehensive test suite"
    - documentation_generator: "Update technical documentation"
  
  coordination_pattern: conditional_parallel
  deliverables:
    - Code quality assessment report
    - Security validation results
    - Test coverage analysis
    - Updated technical documentation
```

#### Stage 5: Testing & Quality Assurance
```yaml
testing_orchestration:
  quality_agents:
    - test_validator: "Validate test coverage and quality"
    - performance_optimizer: "Analyze and improve performance"
    - integration_tester: "Verify system integration"
  
  coordination_pattern: comprehensive_validation
  deliverables:
    - Complete test validation report
    - Performance optimization recommendations
    - Integration test results
    - Quality assurance certification
```

### 5. Error Handling & Recovery

**Orchestration Resilience Patterns**:
```yaml
error_handling:
  agent_failure_recovery:
    timeout_handling:
      - Default timeout: 300 seconds per agent
      - Escalation timeout: 600 seconds for complex tasks
      - Graceful fallback to alternative agents
    
    partial_failure_management:
      - Continue with available agent results
      - Flag incomplete workflows for manual review
      - Provide alternative completion paths
  
  quality_assurance:
    validation_checkpoints:
      - Validate agent outputs against expected formats
      - Check deliverable completeness and quality
      - Ensure all required context is preserved
    
    rollback_procedures:
      - Maintain workflow state at each stage
      - Enable restart from last successful checkpoint
      - Preserve partial results for recovery
```

### 6. Performance Optimization

**Efficient Orchestration Strategies**:
```yaml
performance_patterns:
  resource_optimization:
    parallel_limits:
      - Maximum 10 concurrent agents (Claude limitation)
      - Queue additional agents for sequential execution
      - Priority-based agent scheduling
    
    context_efficiency:
      - Minimize context duplication between agents
      - Use context references for large shared data
      - Implement lazy loading for optional context
  
  execution_optimization:
    intelligent_caching:
      - Cache common analysis results
      - Reuse validation outputs across similar contexts
      - Store frequently used reference materials
    
    adaptive_timeout:
      - Dynamic timeout based on task complexity
      - Historical performance data for estimation
      - Graceful degradation for time-critical workflows
```

## Orchestration Templates

### Feature Development Template
```yaml
feature_orchestration_template:
  name: "Complete Feature Development Workflow"
  stages:
    stage1_requirements:
      agents: [requirements_analyst, technical_feasibility_expert]
      pattern: sequential_coordination
      timeout: 600
    
    stage2_design:
      agents: [ui_ux_specialist, system_architect]
      pattern: parallel_execution
      timeout: 900
      dependencies: [stage1_requirements]
    
    stage4_implementation:
      agents: [code_reviewer, security_auditor, test_generator]
      pattern: conditional_parallel
      timeout: 1200
      dependencies: [stage2_design]
    
    stage5_quality:
      agents: [performance_optimizer, integration_tester]
      pattern: comprehensive_validation
      timeout: 600
      dependencies: [stage4_implementation]
  
  success_criteria:
    - All stages complete successfully
    - Quality thresholds met (≥85% for security, ≥90% for performance)
    - Deliverables generated and validated
```

### PR Validation Template
```yaml
pr_validation_template:
  name: "Comprehensive Pull Request Validation"
  coordination_pattern: parallel_with_aggregation
  
  validation_agents:
    intent_validator:
      priority: critical
      timeout: 240
      description: "Validate PR intent vs implementation"
    
    security_validator:
      priority: critical
      timeout: 300
      description: "Security vulnerability assessment"
      context: "security-validation-core.md"
    
    code_quality_validator:
      priority: high
      timeout: 300
      description: "Code quality and standards assessment"
      context: "code-review-criteria.md"
    
    test_validator:
      priority: high
      timeout: 180
      description: "Test coverage and quality validation"
  
  aggregation_rules:
    approval_threshold: 85
    critical_issue_blocking: true
    comprehensive_reporting: true
```

## Implementation Guidelines

### Command Integration
```yaml
command_orchestration_usage:
  existing_commands:
    validate_pr:
      - Apply parallel validation agents
      - Use security and code review shared libraries
      - Implement comprehensive result aggregation
    
    create_feature:
      - Use sequential stage coordination
      - Apply feature development template
      - Implement progressive context building
    
    orchestrate_agents:
      - Core orchestration engine
      - Apply appropriate coordination patterns
      - Handle complex dependency management
```

### Subagent Coordination
```yaml
subagent_orchestration:
  stage_coordinators:
    - Apply stage-specific orchestration patterns
    - Coordinate multiple specialists per stage
    - Ensure deliverable quality and completeness
  
  cross_stage_coordination:
    - Manage dependencies between SDLC stages
    - Ensure context continuity across stages
    - Validate end-to-end workflow integrity
```

## Quality Assurance

**Framework Compliance**: Follows AI Agent Instruction Design Excellence:
- **Concrete Patterns**: Specific orchestration workflows and templates
- **Self-Sufficient**: Complete coordination framework without external dependencies
- **Immediately Actionable**: Ready-to-use orchestration patterns
- **Resource Efficient**: Optimized for Claude's concurrent agent limitations

**Reliability Standards**:
- Comprehensive error handling and recovery procedures
- Performance optimization for complex workflows
- Quality validation at each orchestration checkpoint
- Consistent deliverable generation across all patterns

This orchestration framework enables sophisticated multi-agent coordination while maintaining efficiency and reliability across all SDLC stages.