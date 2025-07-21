# Instruction Templates

## Overview

This guide provides comprehensive instruction templates for AI agent instruction design, ensuring consistency, clarity, and immediate actionability. These templates are derived from actionable instruction frameworks and proven design patterns.

## Key Characteristics

- **Immediate Actionability**: Templates ensure immediate execution capability
- **Standardized Structure**: Consistent format across all instructions
- **Comprehensive Coverage**: Templates for all instruction types
- **Quality Assurance**: Built-in validation and quality checks

## Template 1: Basic Action Instruction Template

### When to Use
- Simple task execution
- Single-step operations
- Direct commands
- Basic system interactions

### Template Structure

```yaml
basic_action_template:
  header:
    instruction_id: "unique_identifier"
    instruction_type: "basic_action"
    priority: "high|medium|low"
    estimated_duration: "specific_time_in_minutes"
    
  execution:
    action: "specific_executable_action"
    parameters:
      param1: "exact_value"
      param2: "specific_configuration"
    
    success_criteria:
      condition1: "measurable_outcome_1"
      condition2: "measurable_outcome_2"
    
    timeout: "maximum_execution_time"
    
  validation:
    pre_execution_check: "prerequisite_validation"
    post_execution_check: "result_validation"
    quality_threshold: "minimum_quality_standard"
```

### Example Implementation

```yaml
basic_action_example:
  header:
    instruction_id: "deploy_queen_agent_001"
    instruction_type: "basic_action"
    priority: "high"
    estimated_duration: "2_minutes"
    
  execution:
    action: "deploy_queen_agent"
    parameters:
      agent_type: "queen"
      spawning_authority: "unlimited"
      performance_target: "847_tasks_per_second"
      response_time_limit: "4.2ms"
    
    success_criteria:
      agent_deployment: "queen_agent_active_and_responsive"
      performance_achievement: "throughput_≥847_tasks_per_second"
      response_time: "average_response_time_≤4.2ms"
    
    timeout: "120_seconds"
    
  validation:
    pre_execution_check: "system_resources_available_permissions_verified"
    post_execution_check: "agent_functionality_validated_performance_confirmed"
    quality_threshold: "95%_success_rate"
```

## Template 2: Complex Workflow Instruction Template

### When to Use
- Multi-step procedures
- Conditional workflows
- Complex decision trees
- Orchestrated operations

### Template Structure

```yaml
complex_workflow_template:
  header:
    instruction_id: "unique_identifier"
    instruction_type: "complex_workflow"
    priority: "high|medium|low"
    estimated_duration: "total_workflow_time"
    
  workflow_steps:
    step_1:
      action: "specific_action_1"
      parameters: "exact_parameters"
      success_criteria: "measurable_outcomes"
      timeout: "step_timeout"
      
    step_2:
      condition: "IF_condition_from_step_1"
      action: "conditional_action_2"
      parameters: "conditional_parameters"
      success_criteria: "conditional_outcomes"
      timeout: "step_timeout"
      
    step_n:
      action: "final_action"
      parameters: "final_parameters"
      success_criteria: "final_outcomes"
      timeout: "step_timeout"
      
  error_handling:
    step_failure_response: "failure_recovery_procedure"
    workflow_rollback: "rollback_procedures"
    escalation_triggers: "escalation_conditions"
    
  validation:
    checkpoint_validation: "intermediate_validation_points"
    final_validation: "complete_workflow_validation"
    quality_gates: "quality_checkpoints"
```

### Decision Criteria

- **Step Count**: >3 steps requires complex workflow template
- **Conditional Logic**: Decision points require conditional structures
- **Error Handling**: Critical workflows need comprehensive error handling
- **Quality Gates**: High-quality requirements need checkpoint validation

## Template 3: Research Task Instruction Template

### When to Use
- Research and analysis tasks
- Information gathering
- Evidence-based conclusions
- Systematic investigations

### Template Structure

```yaml
research_task_template:
  header:
    instruction_id: "unique_identifier"
    instruction_type: "research_task"
    research_methodology: "universal|complex|domain_adaptive"
    estimated_duration: "research_time_estimate"
    
  research_parameters:
    research_question: "specific_research_question"
    scope_boundaries: "research_scope_definition"
    success_criteria: "research_success_measures"
    quality_requirements: "research_quality_standards"
    
  methodology:
    approach: "systematic_research_approach"
    validation_framework: "research_validation_method"
    quality_assurance: "research_quality_procedures"
    
  progressive_context_loading:
    initial_context: "essential_research_context"
    conditional_context: "methodology_specific_context"
    validation_context: "quality_assurance_context"
    
  deliverables:
    research_output: "expected_research_deliverables"
    documentation: "research_documentation_requirements"
    recommendations: "actionable_recommendations"
```

### Example Implementation

```yaml
research_task_example:
  header:
    instruction_id: "frontend_framework_research_001"
    instruction_type: "research_task"
    research_methodology: "domain_adaptive"
    estimated_duration: "4_hours"
    
  research_parameters:
    research_question: "optimal_frontend_framework_for_enterprise_applications"
    scope_boundaries: "React_Vue_Angular_enterprise_context_2024"
    success_criteria: "actionable_framework_recommendation_with_implementation_plan"
    quality_requirements: "95%_source_credibility_90%_methodology_rigor"
    
  methodology:
    approach: "comparative_analysis_with_case_studies"
    validation_framework: "constitutional_ai_validation_peer_review_simulation"
    quality_assurance: "source_triangulation_consistency_verification"
    
  progressive_context_loading:
    initial_context: "load_knowledge/research/analysis-methods.md"
    conditional_context: "IF_technical_depth_needed_load_knowledge/techniques/performance-optimization.md"
    validation_context: "load_knowledge/research/validation-techniques.md"
    
  deliverables:
    research_output: "comprehensive_framework_comparison_with_metrics"
    documentation: "research_methodology_documentation_source_bibliography"
    recommendations: "specific_implementation_recommendations_with_timeline"
```

## Template 4: Agent Coordination Instruction Template

### When to Use
- Multi-agent orchestration
- Hierarchical coordination
- Distributed task execution
- Performance optimization

### Template Structure

```yaml
agent_coordination_template:
  header:
    instruction_id: "unique_identifier"
    instruction_type: "agent_coordination"
    coordination_pattern: "queen|architect|specialist|worker"
    estimated_duration: "coordination_time_estimate"
    
  agent_hierarchy:
    primary_agent:
      agent_type: "coordination_agent_type"
      authority_level: "spawning_authority"
      responsibilities: "coordination_responsibilities"
      
    secondary_agents:
      agent_type: "subordinate_agent_type"
      count: "number_of_agents"
      responsibilities: "agent_responsibilities"
      
  coordination_parameters:
    performance_targets: "specific_performance_metrics"
    communication_protocols: "agent_communication_specifications"
    synchronization_points: "coordination_checkpoints"
    
  monitoring:
    performance_monitoring: "real_time_performance_tracking"
    quality_monitoring: "coordination_quality_assessment"
    error_monitoring: "coordination_error_detection"
    
  validation:
    coordination_validation: "coordination_effectiveness_verification"
    performance_validation: "performance_target_achievement_verification"
    quality_validation: "coordination_quality_verification"
```

## Template 5: Quality Assurance Instruction Template

### When to Use
- Quality validation tasks
- Compliance verification
- Standard adherence
- Continuous improvement

### Template Structure

```yaml
quality_assurance_template:
  header:
    instruction_id: "unique_identifier"
    instruction_type: "quality_assurance"
    quality_framework: "constitutional_ai|self_consistency|peer_review"
    estimated_duration: "quality_assurance_time"
    
  quality_parameters:
    quality_standards: "specific_quality_criteria"
    validation_methods: "quality_validation_procedures"
    success_thresholds: "quality_success_metrics"
    
  validation_procedures:
    pre_validation: "initial_quality_assessment"
    process_validation: "continuous_quality_monitoring"
    post_validation: "final_quality_verification"
    
  quality_gates:
    gate_1: "initial_quality_checkpoint"
    gate_2: "intermediate_quality_checkpoint"
    gate_3: "final_quality_checkpoint"
    
  continuous_improvement:
    feedback_integration: "quality_feedback_incorporation"
    process_enhancement: "quality_process_improvement"
    standard_evolution: "quality_standard_advancement"
```

## Template 6: Performance Optimization Instruction Template

### When to Use
- System optimization tasks
- Performance enhancement
- Resource optimization
- Efficiency improvement

### Template Structure

```yaml
performance_optimization_template:
  header:
    instruction_id: "unique_identifier"
    instruction_type: "performance_optimization"
    optimization_target: "throughput|latency|efficiency|scalability"
    estimated_duration: "optimization_time_estimate"
    
  performance_parameters:
    baseline_metrics: "current_performance_measurements"
    target_metrics: "desired_performance_targets"
    optimization_techniques: "specific_optimization_methods"
    
  optimization_procedures:
    analysis_phase: "performance_analysis_procedures"
    implementation_phase: "optimization_implementation_procedures"
    validation_phase: "performance_validation_procedures"
    
  monitoring:
    real_time_monitoring: "performance_monitoring_during_optimization"
    comparative_analysis: "before_after_performance_comparison"
    continuous_monitoring: "ongoing_performance_tracking"
    
  validation:
    performance_validation: "optimization_effectiveness_verification"
    stability_validation: "optimized_system_stability_verification"
    scalability_validation: "optimization_scalability_verification"
```

## Template Customization Guidelines

### Template Adaptation Rules

```yaml
adaptation_rules:
  context_adaptation:
    - audience_expertise: "adapt_detail_level_to_user_expertise"
    - domain_specificity: "adapt_terminology_to_domain_requirements"
    - complexity_level: "adapt_structure_to_task_complexity"
    - resource_constraints: "adapt_requirements_to_available_resources"
    
  performance_optimization:
    - token_optimization: "apply_token_compression_techniques"
    - context_loading: "implement_progressive_context_loading"
    - template_reuse: "maximize_template_reusability"
    - validation_efficiency: "optimize_validation_procedures"
    
  quality_assurance:
    - validation_integration: "integrate_quality_validation_procedures"
    - error_handling: "implement_comprehensive_error_handling"
    - success_measurement: "define_measurable_success_criteria"
    - continuous_improvement: "enable_template_improvement_feedback"
```

### Template Quality Metrics

```yaml
template_quality_metrics:
  usability_metrics:
    - clarity_score: "template_clarity_assessment"
    - completeness_score: "template_completeness_evaluation"
    - actionability_score: "template_actionability_measurement"
    - consistency_score: "template_consistency_evaluation"
    
  effectiveness_metrics:
    - success_rate: "template_usage_success_rate"
    - efficiency_gain: "template_efficiency_improvement"
    - error_reduction: "template_error_reduction_rate"
    - time_savings: "template_time_savings_measurement"
    
  adoption_metrics:
    - usage_frequency: "template_usage_frequency"
    - user_satisfaction: "template_user_satisfaction_rating"
    - customization_rate: "template_customization_frequency"
    - improvement_suggestions: "template_improvement_feedback_rate"
```

## Template Validation

### Template Quality Validation

```yaml
template_validation:
  structure_validation:
    - completeness_check: "verify_all_required_sections_present"
    - consistency_check: "verify_template_internal_consistency"
    - format_validation: "verify_template_format_compliance"
    - standard_adherence: "verify_template_standard_compliance"
    
  functionality_validation:
    - actionability_verification: "verify_template_actionability"
    - executability_testing: "test_template_executability"
    - success_criteria_validation: "verify_success_criteria_measurability"
    - error_handling_validation: "verify_error_handling_completeness"
    
  usability_validation:
    - clarity_assessment: "assess_template_clarity"
    - ease_of_use_evaluation: "evaluate_template_usability"
    - learning_curve_assessment: "assess_template_learning_requirements"
    - user_feedback_integration: "integrate_user_usability_feedback"
```

## Template Automation

### Automated Template Generation

```yaml
template_automation:
  intelligent_template_selection:
    - task_analysis: "analyze_task_requirements_for_template_selection"
    - template_recommendation: "recommend_optimal_template_based_on_analysis"
    - customization_suggestions: "suggest_template_customizations"
    - validation_automation: "automate_template_validation_procedures"
    
  dynamic_template_adaptation:
    - context_aware_adaptation: "adapt_template_based_on_context"
    - performance_optimization: "optimize_template_for_performance"
    - quality_enhancement: "enhance_template_quality_automatically"
    - continuous_improvement: "improve_template_based_on_usage_patterns"
```

## Cross-References

- **Actionable Instructions**: See `knowledge/research/actionable-instruction-framework.md` for instruction design
- **Quality Validation**: See `knowledge/quality/validation-procedures.md` for validation templates
- **Research Methods**: See `knowledge/research/analysis-methods.md` for research templates
- **Orchestration Patterns**: See `knowledge/orchestration/` for coordination templates

## Performance Benchmarks

- **Template Clarity**: Target >90%, Excellence >95%
- **Template Completeness**: Target >95%, Excellence >98%
- **Template Actionability**: Target >90%, Excellence >95%
- **User Satisfaction**: Target >85%, Excellence >90%

## Troubleshooting

**Common Issues:**
- **Template Complexity**: Simplify template structure, improve clarity
- **Low Actionability**: Enhance specific parameters, improve success criteria
- **User Confusion**: Improve documentation, provide examples
- **Template Inconsistency**: Standardize format, improve validation

**Template Recovery:**
- **Template Failures**: Implement template validation, enhance error handling
- **Usability Issues**: Improve template design, enhance user experience
- **Performance Problems**: Optimize template efficiency, reduce overhead
- **Quality Issues**: Enhance template quality assurance, improve validation

## Implementation Guidelines

1. **Select appropriate template** based on task type and complexity
2. **Customize template parameters** for specific requirements
3. **Validate template completeness** before execution
4. **Apply progressive context loading** for efficiency
5. **Implement quality validation** throughout template usage
6. **Collect feedback** for continuous template improvement