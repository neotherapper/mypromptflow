# Analysis Templates

## Overview

This guide provides comprehensive analysis templates for AI agent instruction design, enabling systematic analysis, structured reporting, and consistent evaluation methodologies. These templates ensure thorough analysis and actionable insights.

## Key Characteristics

- **Systematic Analysis**: Structured approach to analysis tasks
- **Comprehensive Coverage**: Templates for all analysis types
- **Actionable Insights**: Analysis that leads to concrete recommendations
- **Quality Assurance**: Built-in validation and quality checks

## Template 1: Comparative Analysis Template

### When to Use
- Technology comparison tasks
- Option evaluation requirements
- Benchmark analysis needs
- Decision support analysis

### Template Structure

```yaml
comparative_analysis_template:
  header:
    analysis_id: "unique_identifier"
    analysis_type: "comparative_analysis"
    comparison_subjects: "list_of_items_being_compared"
    analysis_purpose: "specific_analysis_objective"
    
  analysis_framework:
    evaluation_criteria:
      criterion_1:
        name: "specific_criterion_name"
        weight: "importance_weight_0_to_1"
        measurement_method: "objective_measurement_approach"
        
      criterion_2:
        name: "specific_criterion_name"
        weight: "importance_weight_0_to_1"
        measurement_method: "objective_measurement_approach"
        
    comparison_matrix:
      subject_1:
        criterion_1_score: "numerical_score_0_to_10"
        criterion_2_score: "numerical_score_0_to_10"
        overall_score: "weighted_average_score"
        
      subject_2:
        criterion_1_score: "numerical_score_0_to_10"
        criterion_2_score: "numerical_score_0_to_10"
        overall_score: "weighted_average_score"
        
  analysis_results:
    ranking: "ordered_list_of_subjects_by_score"
    recommendation: "specific_recommendation_with_rationale"
    confidence_level: "recommendation_confidence_percentage"
    
  validation:
    methodology_validation: "analysis_methodology_verification"
    data_validation: "analysis_data_verification"
    conclusion_validation: "analysis_conclusion_verification"
```

### Example Implementation

```yaml
comparative_analysis_example:
  header:
    analysis_id: "frontend_framework_comparison_001"
    analysis_type: "comparative_analysis"
    comparison_subjects: ["React", "Vue", "Angular"]
    analysis_purpose: "enterprise_application_framework_selection"
    
  analysis_framework:
    evaluation_criteria:
      performance:
        name: "runtime_performance_efficiency"
        weight: 0.25
        measurement_method: "benchmark_testing_metrics"
        
      developer_experience:
        name: "development_productivity_learning_curve"
        weight: 0.20
        measurement_method: "developer_survey_productivity_metrics"
        
      ecosystem_maturity:
        name: "library_ecosystem_community_support"
        weight: 0.20
        measurement_method: "npm_downloads_github_activity_stackoverflow"
        
      maintenance_overhead:
        name: "long_term_maintenance_requirements"
        weight: 0.15
        measurement_method: "technical_debt_update_frequency"
        
      enterprise_readiness:
        name: "enterprise_feature_support"
        weight: 0.20
        measurement_method: "feature_checklist_enterprise_adoption"
        
    comparison_matrix:
      react:
        performance: 8.5
        developer_experience: 8.0
        ecosystem_maturity: 9.0
        maintenance_overhead: 7.0
        enterprise_readiness: 8.5
        overall_score: 8.2
        
      vue:
        performance: 8.0
        developer_experience: 9.0
        ecosystem_maturity: 7.5
        maintenance_overhead: 8.5
        enterprise_readiness: 7.0
        overall_score: 7.9
        
      angular:
        performance: 7.5
        developer_experience: 6.5
        ecosystem_maturity: 8.0
        maintenance_overhead: 8.0
        enterprise_readiness: 9.0
        overall_score: 7.7
        
  analysis_results:
    ranking: ["React (8.2)", "Vue (7.9)", "Angular (7.7)"]
    recommendation: "React_recommended_for_enterprise_applications_due_to_superior_performance_and_ecosystem_maturity"
    confidence_level: "85%"
    
  validation:
    methodology_validation: "comparative_analysis_methodology_peer_reviewed"
    data_validation: "benchmark_data_verified_from_multiple_sources"
    conclusion_validation: "recommendation_validated_against_enterprise_requirements"
```

## Template 2: Performance Analysis Template

### When to Use
- System performance evaluation
- Optimization analysis
- Bottleneck identification
- Capacity planning analysis

### Template Structure

```yaml
performance_analysis_template:
  header:
    analysis_id: "unique_identifier"
    analysis_type: "performance_analysis"
    system_under_analysis: "specific_system_component"
    analysis_scope: "performance_analysis_boundaries"
    
  performance_metrics:
    baseline_measurements:
      throughput: "current_throughput_measurement"
      latency: "current_latency_measurement"
      resource_utilization: "current_resource_usage"
      error_rate: "current_error_rate"
      
    target_measurements:
      throughput: "target_throughput_requirement"
      latency: "target_latency_requirement"
      resource_utilization: "target_resource_usage"
      error_rate: "target_error_rate"
      
  analysis_methodology:
    measurement_approach: "performance_measurement_methodology"
    testing_environment: "performance_testing_setup"
    test_scenarios: "performance_test_scenarios"
    validation_criteria: "performance_validation_standards"
    
  bottleneck_analysis:
    identified_bottlenecks: "performance_constraint_identification"
    impact_assessment: "bottleneck_impact_quantification"
    optimization_opportunities: "performance_improvement_potential"
    
  recommendations:
    optimization_recommendations: "specific_optimization_actions"
    implementation_priority: "optimization_priority_ranking"
    expected_improvements: "quantified_improvement_expectations"
    
  validation:
    measurement_validation: "performance_measurement_accuracy_verification"
    analysis_validation: "performance_analysis_methodology_verification"
    recommendation_validation: "optimization_recommendation_feasibility_verification"
```

### Decision Criteria

- **Performance Gap**: >20% gap between current and target triggers analysis
- **Bottleneck Severity**: >30% performance impact requires detailed analysis
- **Resource Utilization**: >80% utilization triggers capacity analysis
- **Error Rate**: >5% error rate requires performance investigation

## Template 3: Risk Analysis Template

### When to Use
- Risk assessment requirements
- Security analysis needs
- Compliance evaluation
- Impact analysis tasks

### Template Structure

```yaml
risk_analysis_template:
  header:
    analysis_id: "unique_identifier"
    analysis_type: "risk_analysis"
    risk_domain: "specific_risk_area"
    analysis_scope: "risk_analysis_boundaries"
    
  risk_identification:
    risk_categories:
      technical_risks: "technology_related_risks"
      operational_risks: "operational_process_risks"
      security_risks: "security_vulnerability_risks"
      compliance_risks: "regulatory_compliance_risks"
      
    risk_inventory:
      risk_1:
        risk_name: "specific_risk_name"
        risk_description: "detailed_risk_description"
        risk_category: "risk_classification"
        
      risk_2:
        risk_name: "specific_risk_name"
        risk_description: "detailed_risk_description"
        risk_category: "risk_classification"
        
  risk_assessment:
    risk_evaluation:
      risk_1:
        probability: "occurrence_probability_0_to_1"
        impact: "impact_severity_0_to_10"
        risk_score: "probability_×_impact"
        
      risk_2:
        probability: "occurrence_probability_0_to_1"
        impact: "impact_severity_0_to_10"
        risk_score: "probability_×_impact"
        
    risk_prioritization:
      high_priority_risks: "risks_requiring_immediate_attention"
      medium_priority_risks: "risks_requiring_monitoring"
      low_priority_risks: "risks_requiring_periodic_review"
      
  mitigation_strategies:
    risk_mitigation:
      risk_1:
        mitigation_strategy: "specific_risk_mitigation_approach"
        implementation_effort: "mitigation_implementation_requirements"
        effectiveness: "mitigation_effectiveness_assessment"
        
      risk_2:
        mitigation_strategy: "specific_risk_mitigation_approach"
        implementation_effort: "mitigation_implementation_requirements"
        effectiveness: "mitigation_effectiveness_assessment"
        
  validation:
    risk_identification_validation: "risk_identification_completeness_verification"
    risk_assessment_validation: "risk_assessment_accuracy_verification"
    mitigation_validation: "mitigation_strategy_effectiveness_verification"
```

## Template 4: Requirements Analysis Template

### When to Use
- Requirements gathering
- Stakeholder analysis
- Functional analysis
- System specification

### Template Structure

```yaml
requirements_analysis_template:
  header:
    analysis_id: "unique_identifier"
    analysis_type: "requirements_analysis"
    project_scope: "requirements_analysis_scope"
    stakeholder_context: "stakeholder_environment"
    
  stakeholder_analysis:
    stakeholder_identification:
      primary_stakeholders: "direct_system_users"
      secondary_stakeholders: "indirect_system_beneficiaries"
      key_stakeholders: "decision_makers_influencers"
      
    stakeholder_requirements:
      stakeholder_1:
        needs: "specific_stakeholder_needs"
        expectations: "stakeholder_expectations"
        constraints: "stakeholder_constraints"
        
      stakeholder_2:
        needs: "specific_stakeholder_needs"
        expectations: "stakeholder_expectations"
        constraints: "stakeholder_constraints"
        
  functional_requirements:
    core_functions:
      function_1:
        description: "specific_function_description"
        priority: "high|medium|low"
        acceptance_criteria: "measurable_acceptance_criteria"
        
      function_2:
        description: "specific_function_description"
        priority: "high|medium|low"
        acceptance_criteria: "measurable_acceptance_criteria"
        
    supporting_functions:
      function_1:
        description: "specific_supporting_function"
        priority: "high|medium|low"
        acceptance_criteria: "measurable_acceptance_criteria"
        
  non_functional_requirements:
    performance_requirements:
      throughput: "specific_throughput_requirements"
      response_time: "specific_response_time_requirements"
      scalability: "specific_scalability_requirements"
      
    quality_requirements:
      reliability: "specific_reliability_requirements"
      availability: "specific_availability_requirements"
      maintainability: "specific_maintainability_requirements"
      
  validation:
    requirements_validation: "requirements_completeness_accuracy_verification"
    stakeholder_validation: "stakeholder_requirement_satisfaction_verification"
    feasibility_validation: "requirements_technical_feasibility_verification"
```

## Template 5: Technical Analysis Template

### When to Use
- Technical assessment tasks
- Architecture analysis
- Technology evaluation
- Implementation analysis

### Template Structure

```yaml
technical_analysis_template:
  header:
    analysis_id: "unique_identifier"
    analysis_type: "technical_analysis"
    technical_domain: "specific_technical_area"
    analysis_depth: "surface|detailed|comprehensive"
    
  technical_assessment:
    technology_evaluation:
      technology_1:
        technical_merit: "technology_technical_assessment"
        maturity_level: "technology_maturity_evaluation"
        adoption_risk: "technology_adoption_risk_assessment"
        
      technology_2:
        technical_merit: "technology_technical_assessment"
        maturity_level: "technology_maturity_evaluation"
        adoption_risk: "technology_adoption_risk_assessment"
        
    architecture_analysis:
      system_architecture:
        scalability: "architecture_scalability_assessment"
        maintainability: "architecture_maintainability_evaluation"
        security: "architecture_security_assessment"
        
      integration_architecture:
        compatibility: "integration_compatibility_assessment"
        complexity: "integration_complexity_evaluation"
        risk: "integration_risk_assessment"
        
  technical_recommendations:
    technology_recommendations:
      recommended_technologies: "specific_technology_recommendations"
      implementation_approach: "recommended_implementation_strategy"
      risk_mitigation: "technical_risk_mitigation_strategies"
      
    architecture_recommendations:
      recommended_architecture: "specific_architecture_recommendations"
      design_patterns: "recommended_design_patterns"
      implementation_guidelines: "architecture_implementation_guidelines"
      
  validation:
    technical_validation: "technical_analysis_accuracy_verification"
    feasibility_validation: "technical_recommendation_feasibility_verification"
    quality_validation: "technical_analysis_quality_verification"
```

## Template 6: Business Analysis Template

### When to Use
- Business impact analysis
- Value proposition analysis
- ROI analysis
- Strategic analysis

### Template Structure

```yaml
business_analysis_template:
  header:
    analysis_id: "unique_identifier"
    analysis_type: "business_analysis"
    business_context: "specific_business_environment"
    analysis_timeline: "analysis_time_horizon"
    
  business_context_analysis:
    market_analysis:
      market_conditions: "current_market_environment"
      competitive_landscape: "competitive_analysis"
      market_trends: "relevant_market_trends"
      
    organizational_analysis:
      organizational_readiness: "change_readiness_assessment"
      resource_availability: "available_resources_assessment"
      capability_gaps: "capability_gap_analysis"
      
  value_proposition_analysis:
    business_benefits:
      quantifiable_benefits: "measurable_business_benefits"
      qualitative_benefits: "non_quantifiable_business_benefits"
      benefit_timeline: "benefit_realization_timeline"
      
    cost_analysis:
      implementation_costs: "total_implementation_investment"
      operational_costs: "ongoing_operational_expenses"
      opportunity_costs: "opportunity_cost_assessment"
      
  roi_analysis:
    financial_projections:
      revenue_impact: "projected_revenue_impact"
      cost_savings: "projected_cost_savings"
      investment_recovery: "investment_recovery_timeline"
      
    risk_adjusted_roi:
      base_case_roi: "expected_roi_calculation"
      best_case_roi: "optimistic_roi_scenario"
      worst_case_roi: "pessimistic_roi_scenario"
      
  validation:
    business_validation: "business_analysis_accuracy_verification"
    financial_validation: "financial_projection_accuracy_verification"
    stakeholder_validation: "business_stakeholder_analysis_validation"
```

## Analysis Template Quality Metrics

### Template Effectiveness Metrics

```yaml
template_effectiveness:
  analysis_quality:
    - accuracy_rate: "analysis_accuracy_measurement"
    - completeness_score: "analysis_completeness_assessment"
    - consistency_rating: "analysis_consistency_evaluation"
    - actionability_index: "analysis_actionability_measurement"
    
  template_usability:
    - ease_of_use: "template_usability_assessment"
    - learning_curve: "template_learning_requirements"
    - customization_flexibility: "template_customization_capability"
    - documentation_quality: "template_documentation_effectiveness"
    
  analysis_efficiency:
    - time_to_completion: "analysis_completion_time"
    - resource_utilization: "analysis_resource_efficiency"
    - automation_potential: "analysis_automation_capability"
    - reusability_factor: "template_reusability_assessment"
```

### Quality Assurance Metrics

```yaml
quality_assurance_metrics:
  validation_effectiveness:
    - validation_coverage: "analysis_validation_completeness"
    - validation_accuracy: "validation_procedure_accuracy"
    - error_detection_rate: "analysis_error_detection_capability"
    - quality_improvement: "analysis_quality_improvement_measurement"
    
  continuous_improvement:
    - template_evolution: "template_improvement_over_time"
    - user_feedback_integration: "user_feedback_incorporation_rate"
    - best_practice_adoption: "best_practice_integration_rate"
    - innovation_integration: "new_technique_adoption_rate"
```

## Template Automation

### Automated Analysis Support

```yaml
analysis_automation:
  data_collection_automation:
    - automated_data_gathering: "automatic_data_collection_procedures"
    - data_validation_automation: "automated_data_quality_verification"
    - source_integration: "automated_data_source_integration"
    - real_time_data_updates: "automated_data_refresh_procedures"
    
  analysis_processing_automation:
    - automated_calculations: "automatic_metric_calculation"
    - pattern_recognition: "automated_pattern_identification"
    - trend_analysis: "automated_trend_detection"
    - comparative_analysis: "automated_comparison_procedures"
    
  reporting_automation:
    - automated_report_generation: "automatic_analysis_report_creation"
    - visualization_automation: "automated_chart_graph_generation"
    - insight_extraction: "automated_insight_identification"
    - recommendation_generation: "automated_recommendation_synthesis"
```

## Cross-References

- **Research Methods**: See `knowledge/research/analysis-methods.md` for analysis methodologies
- **Validation Templates**: See `knowledge/templates/validation-templates.md` for validation procedures
- **Instruction Templates**: See `knowledge/templates/instruction-templates.md` for instruction formats
- **Quality Frameworks**: See `knowledge/research/quality-frameworks.md` for quality analysis

## Performance Benchmarks

- **Analysis Accuracy**: Target >90%, Excellence >95%
- **Analysis Completeness**: Target >85%, Excellence >90%
- **Template Usability**: Target >80%, Excellence >85%
- **Analysis Efficiency**: Target >75%, Excellence >80%

## Troubleshooting

**Common Issues:**
- **Incomplete Analysis**: Enhance template completeness, improve validation
- **Low Accuracy**: Strengthen analysis methodology, improve validation
- **Template Complexity**: Simplify template structure, improve documentation
- **Poor Actionability**: Enhance recommendation sections, improve specificity

**Analysis Recovery:**
- **Analysis Failures**: Implement robust validation, enhance methodology
- **Quality Issues**: Strengthen quality assurance, improve validation
- **Usability Problems**: Enhance template design, improve documentation
- **Efficiency Issues**: Optimize template structure, increase automation

## Implementation Guidelines

1. **Select appropriate analysis template** based on analysis type and scope
2. **Customize template parameters** for specific analysis requirements
3. **Apply systematic analysis methodology** throughout the process
4. **Validate analysis results** using built-in validation procedures
5. **Generate actionable recommendations** based on analysis findings
6. **Document analysis process** for reproducibility and improvement