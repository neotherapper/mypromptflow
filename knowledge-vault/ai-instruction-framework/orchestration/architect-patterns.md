# Architect Agent Orchestration Patterns

## Overview

Architect Agents provide system design and technical coordination with limited spawning authority (max 5 concurrent specialist agents). This guide provides comprehensive patterns for implementing Architect Agent coordination in technical domains.

## Key Characteristics

- **Authority Level**: Limited spawning (max 5 concurrent specialist agents)
- **Decision Scope**: Technical design and architecture decisions
- **Coordination Span**: Specialist and worker agent levels
- **Performance Targets**: >85% design quality, >90% architectural consistency

## Pattern 1: Technical Design Coordination

### When to Use
- Complex technical system design requirements
- Multi-component architecture development
- Cross-domain technical integration

### Implementation Steps

1. **Requirements Analysis**
   ```yaml
   analyze_technical_requirements:
     - system_complexity_assessment: "technical_difficulty_scoring"
     - component_identification: "modular_architecture_design"
     - integration_mapping: "dependency_analysis"
     - performance_requirements: "scalability_maintainability_criteria"
   ```

2. **Architecture Design**
   ```yaml
   design_system_architecture:
     - component_architecture: "modular_loosely_coupled_design"
     - interface_definitions: "api_specifications"
     - data_architecture: "storage_retrieval_patterns"
     - integration_patterns: "system_connection_protocols"
   ```

3. **Specialist Coordination**
   ```yaml
   coordinate_specialists:
     - spawn_domain_experts: "based_on_technical_requirements"
     - assign_responsibilities: "component_ownership_matrix"
     - establish_communication: "structured_reporting_protocols"
     - monitor_progress: "design_quality_metrics"
   ```

### Example Implementation

```yaml
technical_design_example:
  scenario: "AI Agent Framework Architecture"
  complexity_score: 7.5
  
  actions:
    1. analyze_requirements:
       - components: "orchestration_research_validation_templates"
       - integration_points: "cross_component_communication"
       - performance_targets: "response_time_accuracy_scalability"
    
    2. design_architecture:
       - modular_structure: "independent_loosely_coupled_components"
       - interface_specifications: "standardized_api_definitions"
       - data_flow: "input_processing_output_patterns"
    
    3. coordinate_specialists:
       - orchestration_specialist: "coordination_pattern_development"
       - research_specialist: "research_method_implementation"
       - quality_specialist: "validation_framework_design"
  
  success_criteria:
    - design_quality: ">85%"
    - architectural_consistency: ">90%"
    - integration_success: ">95%"
    - technical_debt: "<10%"
```

## Pattern 2: Cross-Domain Integration

### When to Use
- Systems requiring multiple technical domains
- Integration with existing systems
- Complex dependency management

### Implementation Steps

1. **Domain Analysis**
   ```yaml
   analyze_domains:
     - identify_technical_domains: "frontend_backend_data_integration"
     - map_domain_interactions: "dependency_mapping"
     - assess_integration_complexity: "technical_compatibility_analysis"
   ```

2. **Integration Strategy**
   ```yaml
   integration_strategy:
     - define_integration_points: "api_boundaries_data_flows"
     - establish_communication_protocols: "synchronous_asynchronous_messaging"
     - design_error_handling: "fault_tolerance_recovery_mechanisms"
   ```

3. **Implementation Coordination**
   ```yaml
   coordinate_implementation:
     - parallel_development: "independent_component_development"
     - integration_testing: "component_integration_validation"
     - performance_optimization: "end_to_end_performance_tuning"
   ```

### Decision Criteria

- **Technical Complexity**: >7/10 requires architect-level coordination
- **Integration Points**: >3 systems require structured integration approach
- **Performance Requirements**: Critical performance targets need architecture oversight
- **Quality Standards**: High-quality requirements need architectural validation

## Pattern 3: Scalable System Design

### When to Use
- Systems with growth requirements
- High-performance applications
- Resource-constrained environments

### Implementation Steps

1. **Scalability Assessment**
   ```yaml
   assess_scalability:
     - load_projections: "expected_user_growth_data_volume"
     - performance_requirements: "response_time_throughput_targets"
     - resource_constraints: "hardware_budget_limitations"
   ```

2. **Scalable Architecture Design**
   ```yaml
   design_scalable_architecture:
     - horizontal_scaling: "load_balancing_distribution_strategies"
     - vertical_scaling: "resource_optimization_techniques"
     - caching_strategies: "data_caching_performance_optimization"
     - microservices_architecture: "service_decomposition_patterns"
   ```

3. **Performance Validation**
   ```yaml
   validate_performance:
     - load_testing: "stress_testing_capacity_planning"
     - performance_monitoring: "real_time_metrics_tracking"
     - optimization_cycles: "continuous_performance_improvement"
   ```

## Pattern 4: Quality-Driven Architecture

### When to Use
- High-reliability systems
- Compliance-critical applications
- Long-term maintainability requirements

### Implementation Steps

1. **Quality Framework**
   ```yaml
   establish_quality_framework:
     - code_quality_standards: "coding_conventions_best_practices"
     - testing_strategies: "unit_integration_system_testing"
     - documentation_requirements: "architecture_design_documentation"
   ```

2. **Quality Gates**
   ```yaml
   implement_quality_gates:
     - design_review: "architectural_review_checkpoints"
     - code_review: "peer_review_automated_analysis"
     - testing_gates: "test_coverage_quality_metrics"
   ```

3. **Continuous Quality Monitoring**
   ```yaml
   monitor_quality:
     - quality_metrics: "maintainability_testability_reliability"
     - technical_debt_tracking: "code_quality_degradation_monitoring"
     - improvement_cycles: "continuous_quality_enhancement"
   ```

## Pattern 5: Agile Architecture Coordination

### When to Use
- Iterative development processes
- Changing requirements
- Rapid prototyping needs

### Implementation Steps

1. **Iterative Design**
   ```yaml
   iterative_design_process:
     - minimal_viable_architecture: "core_functionality_focus"
     - incremental_enhancement: "feature_based_architecture_evolution"
     - feedback_integration: "stakeholder_feedback_incorporation"
   ```

2. **Adaptive Planning**
   ```yaml
   adaptive_planning:
     - sprint_planning: "architecture_work_sprint_integration"
     - requirement_evolution: "architecture_adaptation_strategies"
     - risk_management: "architectural_risk_mitigation"
   ```

3. **Continuous Integration**
   ```yaml
   continuous_integration:
     - automated_testing: "continuous_testing_pipeline"
     - deployment_automation: "automated_deployment_strategies"
     - monitoring_integration: "real_time_system_monitoring"
   ```

## Pattern 6: Legacy System Integration

### When to Use
- Modernization projects
- System migration requirements
- Hybrid system architectures

### Implementation Steps

1. **Legacy Analysis**
   ```yaml
   analyze_legacy_systems:
     - system_assessment: "functionality_performance_limitations"
     - integration_points: "api_data_interface_identification"
     - migration_strategy: "gradual_replacement_planning"
   ```

2. **Integration Architecture**
   ```yaml
   design_integration_architecture:
     - adapter_patterns: "legacy_system_interface_adapters"
     - data_synchronization: "data_consistency_strategies"
     - gradual_migration: "phased_replacement_approach"
   ```

3. **Risk Mitigation**
   ```yaml
   mitigate_integration_risks:
     - fallback_strategies: "rollback_procedures"
     - data_integrity: "data_validation_consistency_checks"
     - performance_monitoring: "integration_performance_tracking"
   ```

## Specialist Agent Management

### Spawning Guidelines

```yaml
specialist_spawning_guidelines:
  maximum_concurrent: 5
  
  spawning_criteria:
    - domain_expertise_required: "specialized_knowledge_needed"
    - workload_distribution: "parallel_task_execution"
    - quality_validation: "domain_specific_validation"
    - technical_complexity: "specialized_skill_requirements"
  
  specialist_types:
    - technical_specialist: "programming_frameworks_tools"
    - domain_specialist: "business_domain_knowledge"
    - quality_specialist: "testing_validation_compliance"
    - integration_specialist: "system_integration_expertise"
    - performance_specialist: "optimization_scalability_tuning"
```

### Communication Protocols

```yaml
communication_protocols:
  reporting_frequency:
    - to_queen_agent: "every_15_minutes"
    - from_specialists: "every_10_minutes"
    - emergency_escalation: "immediate_within_30_seconds"
  
  message_format:
    - progress_updates: "completion_percentage_issues_next_actions"
    - quality_metrics: "design_quality_consistency_validation"
    - resource_usage: "specialist_allocation_performance"
    - escalation_requests: "issue_severity_impact_recommendation"
```

## Quality Validation

### Design Quality Metrics

```yaml
design_quality_metrics:
  technical_quality:
    - modularity_score: "component_independence_measurement"
    - maintainability_index: "code_maintainability_assessment"
    - testability_score: "testing_ease_coverage_potential"
    - performance_score: "efficiency_scalability_measurement"
  
  architectural_consistency:
    - pattern_adherence: "design_pattern_compliance"
    - standard_compliance: "architectural_standard_adherence"
    - interface_consistency: "api_design_consistency"
    - documentation_quality: "architecture_documentation_completeness"
```

### Validation Procedures

```yaml
validation_procedures:
  peer_review:
    - architecture_review: "peer_architect_evaluation"
    - design_validation: "technical_design_verification"
    - integration_review: "system_integration_assessment"
  
  automated_validation:
    - design_analysis: "automated_architecture_analysis"
    - dependency_checking: "circular_dependency_detection"
    - performance_modeling: "architecture_performance_prediction"
```

## Cross-References

- **Queen Patterns**: See `knowledge/orchestration/queen-patterns.md` for strategic coordination
- **Specialist Patterns**: See `knowledge/orchestration/specialist-patterns.md` for domain expertise
- **Worker Patterns**: See `knowledge/orchestration/worker-patterns.md` for task execution
- **Coordination Protocols**: See `knowledge/orchestration/coordination-protocols.md` for communication

## Performance Benchmarks

- **Design Quality Score**: Target >85%, Critical <70%
- **Architectural Consistency**: Target >90%, Critical <80%
- **Integration Success Rate**: Target >95%, Critical <85%
- **Technical Debt Ratio**: Target <10%, Critical >25%

## Troubleshooting

**Common Issues:**
- **Design Complexity**: Break down into smaller components, use modular patterns
- **Integration Failures**: Review interface specifications, enhance error handling
- **Performance Issues**: Implement caching, optimize critical paths
- **Quality Problems**: Increase review cycles, enhance validation procedures

**Error Recovery:**
- **Design Failures**: Implement fallback architectures, maintain design alternatives
- **Integration Problems**: Use adapter patterns, implement graceful degradation
- **Performance Degradation**: Implement monitoring, automatic scaling
- **Quality Issues**: Enhance validation, increase review frequency