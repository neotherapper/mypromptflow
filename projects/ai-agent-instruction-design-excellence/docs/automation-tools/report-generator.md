# Report Generation Templates

## Purpose

Standardized assessment report templates with built-in anti-fiction validation checkpoints to accelerate report creation while ensuring comprehensive documentation and preventing fabricated results.

## Anti-Fiction Validation Requirements

**CRITICAL**: This tool requires actual assessment data - no placeholder or estimated results permitted.

- ✅ **MUST use real assessment data from automation tools**
- ✅ **MUST include mandatory evidence sections with file references**
- ✅ **MUST document assessment methodology used**
- ✅ **MUST show actual calculation steps and formulas**
- ❌ **CANNOT generate reports without running assessment tools**
- ❌ **CANNOT use placeholder scores or fictional findings**

## Standardized Report Templates

### Template 1: Comprehensive Framework Assessment Report
```yaml
comprehensive_report_template:
  report_structure:
    header_section:
      - assessment_title: "Framework Assessment Report"
      - target_file_path: "{absolute_file_path}"
      - assessment_date: "{iso_date_time}"
      - assessment_duration: "{actual_minutes_seconds}"
      - assessor_identification: "{ai_agent_name_version}"
      - framework_version: "{framework_version_used}"
      
    executive_summary:
      - overall_quality_score: "{calculated_score}/5.0 ({percentage}%)"
      - quality_classification: "{excellent|good|fair|poor}"
      - primary_strengths: "{top_3_strength_areas}"
      - critical_improvements: "{top_3_improvement_areas}"
      - recommendation_summary: "{go_no_go_decision_with_rationale}"
      
    methodology_section:
      - assessment_tools_used: "{list_of_automation_tools_applied}"
      - checklist_items_evaluated: "{total_checklist_items_count}"
      - evidence_collection_method: "{evidence_documentation_approach}"
      - calculation_methodology: "{scoring_formula_reference}"
      - anti_fiction_validation: "{validation_checkpoints_completed}"
```

### Template 2: Dimensional Analysis Report
```yaml
dimensional_analysis_template:
  dimensional_breakdown:
    clarity_dimension:
      score: "{clarity_score}/5.0"
      percentage: "{clarity_percentage}%"
      checklist_results:
        - item_1: "{passed|failed} - {evidence_or_gap}"
        - item_2: "{passed|failed} - {evidence_or_gap}"
        - item_3: "{passed|failed} - {evidence_or_gap}"
        - item_4: "{passed|failed} - {evidence_or_gap}"
        - item_5: "{passed|failed} - {evidence_or_gap}"
      improvement_priority: "{high|medium|low}"
      
    specificity_dimension:
      score: "{specificity_score}/5.0"
      percentage: "{specificity_percentage}%"
      vagueness_analysis:
        density: "{vagueness_density}%"
        high_severity_terms: "{count} terms found"
        examples: "{specific_vague_terms_with_line_numbers}"
      improvement_priority: "{high|medium|low}"
      
    self_sufficiency_dimension:
      score: "{self_sufficiency_score}/5.0"
      percentage: "{self_sufficiency_percentage}%"
      dependency_analysis:
        dependency_density: "{dependency_density}%"
        external_frameworks: "{count} references found"
        api_dependencies: "{count} dependencies found"
        examples: "{specific_dependencies_with_line_numbers}"
      improvement_priority: "{high|medium|low}"
      
    executability_dimension:
      score: "{executability_score}/5.0"
      percentage: "{executability_percentage}%"
      actionability_analysis:
        immediate_execution: "{yes|no}"
        clarification_required: "{areas_requiring_clarification}"
        missing_procedures: "{missing_step_by_step_elements}"
      improvement_priority: "{high|medium|low}"
      
    purpose_alignment_dimension:
      score: "{purpose_alignment_score}/5.0"
      percentage: "{purpose_alignment_percentage}%"
      alignment_analysis:
        purpose_clarity: "{explicit|implicit|unclear}"
        goal_instruction_match: "{high|medium|low}"
        scope_appropriateness: "{appropriate|too_broad|too_narrow}"
      improvement_priority: "{high|medium|low}"
```

### Template 3: Improvement Action Plan Report
```yaml
improvement_action_plan_template:
  prioritized_improvements:
    critical_actions:
      title: "Critical Improvements (Must Fix Before Deployment)"
      criteria: "Issues preventing successful instruction execution"
      action_items:
        - action_id: "C1"
          description: "{specific_improvement_needed}"
          current_state: "{current_problematic_element}"
          target_state: "{desired_improved_element}"
          implementation_steps:
            - step_1: "{concrete_action_step}"
            - step_2: "{concrete_action_step}"
            - step_3: "{concrete_action_step}"
          estimated_effort: "{hours_or_complexity_rating}"
          validation_criteria: "{how_to_verify_improvement}"
          
    important_actions:
      title: "Important Improvements (Should Fix for Optimal Performance)"
      criteria: "Issues reducing instruction effectiveness"
      action_items:
        - action_id: "I1"
          description: "{specific_improvement_needed}"
          current_state: "{current_suboptimal_element}"
          target_state: "{desired_improved_element}"
          implementation_steps:
            - step_1: "{concrete_action_step}"
            - step_2: "{concrete_action_step}"
          estimated_effort: "{hours_or_complexity_rating}"
          validation_criteria: "{how_to_verify_improvement}"
          
    optional_actions:
      title: "Optional Improvements (Consider for Future Enhancement)"
      criteria: "Nice-to-have improvements with limited impact"
      action_items:
        - action_id: "O1"
          description: "{specific_improvement_needed}"
          current_state: "{current_acceptable_element}"
          target_state: "{desired_enhanced_element}"
          implementation_approach: "{general_improvement_direction}"
          estimated_effort: "{hours_or_complexity_rating}"
```

## Anti-Fiction Validation Checkpoints

### Built-in Validation Sections
```yaml
validation_checkpoint_templates:
  methodology_validation:
    section_title: "Assessment Methodology Validation"
    required_elements:
      - tools_used: "List all automation tools actually applied"
      - time_tracking: "Document actual assessment start and end times"
      - file_analysis: "Confirm target file was read and analyzed"
      - calculation_verification: "Show step-by-step score calculations"
      - evidence_collection: "Document evidence gathering methodology"
      
  evidence_validation:
    section_title: "Evidence Collection Validation"
    required_elements:
      - file_quotes: "Include exact text quotes from target file"
      - line_references: "Provide specific line numbers for all findings"
      - pattern_matches: "Document regex pattern matches where applicable"
      - checklist_results: "Show results for every checklist item evaluated"
      - gap_documentation: "Explain gaps found during assessment"
      
  calculation_validation:
    section_title: "Scoring Calculation Validation"
    required_elements:
      - formula_application: "Show mathematical formulas used"
      - step_by_step_calculation: "Document calculation steps with actual numbers"
      - threshold_application: "Reference quality thresholds applied"
      - weighting_verification: "Confirm dimensional weighting factors used"
      - final_score_derivation: "Show how final score was calculated"
```

### Quality Gate Integration
```yaml
quality_gate_reporting:
  gate_results_section:
    gate_1_minimum_viability:
      condition_checked: "overall_score >= 2.0"
      result: "{passed|failed}"
      implication: "{production_ready|requires_major_revision}"
      
    gate_2_vagueness_threshold:
      condition_checked: "vagueness_density < 10.0%"
      result: "{passed|failed}"
      implication: "{acceptable_specificity|concreteness_improvement_needed}"
      
    gate_3_dependency_threshold:
      condition_checked: "dependency_density < 8.0%"
      result: "{passed|failed}"
      implication: "{sufficient_self_sufficiency|dependency_reduction_needed}"
      
    gate_4_dimensional_balance:
      condition_checked: "no_dimension_score < 1.0"
      result: "{passed|failed}"
      implication: "{balanced_quality|dimensional_failure_detected}"
```

## Automated Report Generation Workflow

### Report Assembly Process
```yaml
report_assembly:
  data_collection_phase:
    vagueness_data: "Import results from vagueness-detector.md tool"
    dependency_data: "Import results from dependency-scanner.md tool"
    assessment_data: "Import results from assessment-calculator.md tool"
    checklist_data: "Import results from checklist-automator.md tool"
    
  template_population_phase:
    header_completion: "Populate report header with actual metadata"
    summary_generation: "Generate executive summary from actual scores"
    detail_compilation: "Compile detailed findings with evidence"
    action_plan_creation: "Generate prioritized improvement plan"
    
  validation_phase:
    completeness_check: "Verify all required sections populated"
    accuracy_verification: "Confirm data matches tool outputs"
    evidence_validation: "Verify all findings have supporting evidence"
    calculation_verification: "Confirm mathematical accuracy"
```

### Time Optimization Features
```yaml
time_optimization:
  automated_data_import:
    description: "Direct import from automation tool outputs"
    time_savings: "Eliminates manual data transcription (2-3 minutes saved)"
    
  template_auto_population:
    description: "Automatic template field completion"
    time_savings: "Reduces manual report writing (3-4 minutes saved)"
    
  validation_automation:
    description: "Automatic validation checkpoint completion"
    time_savings: "Eliminates manual validation checks (1-2 minutes saved)"
    
  formatting_automation:
    description: "Consistent formatting and structure application"
    time_savings: "Reduces formatting effort (30-60 seconds saved)"
```

## Report Types for Different Use Cases

### Quick Assessment Report (2-3 minute assessment)
```yaml
quick_assessment_template:
  purpose: "Rapid quality check for instruction triage"
  sections_included:
    - executive_summary: true
    - dimensional_scores: true
    - top_3_improvements: true
    - go_no_go_recommendation: true
  sections_excluded:
    - detailed_evidence: false
    - step_by_step_calculations: false
    - comprehensive_action_plan: false
  target_completion_time: "30-45 seconds for report generation"
```

### Comprehensive Assessment Report (5-8 minute assessment)
```yaml
comprehensive_assessment_template:
  purpose: "Thorough analysis for instruction optimization"
  sections_included:
    - executive_summary: true
    - methodology_validation: true
    - dimensional_analysis: true
    - evidence_collection: true
    - calculation_validation: true
    - improvement_action_plan: true
    - quality_gate_results: true
  target_completion_time: "60-90 seconds for report generation"
```

### Production Readiness Report (specialized assessment)
```yaml
production_readiness_template:
  purpose: "Final validation before instruction deployment"
  sections_included:
    - quality_certification: true
    - compliance_verification: true
    - risk_assessment: true
    - deployment_recommendations: true
    - monitoring_requirements: true
  specialized_validations:
    - constitutional_ai_compliance: true
    - multi_agent_coordination_readiness: true
    - error_handling_completeness: true
    - scalability_assessment: true
```

## Usage Instructions for AI Agents

### Report Generation Workflow
```yaml
generation_workflow:
  step_1_data_preparation:
    action: "Collect outputs from all applied automation tools"
    time_estimate: "10-15 seconds"
    validation: "Confirm all tool outputs available and complete"
    
  step_2_template_selection:
    action: "Select appropriate report template based on assessment scope"
    time_estimate: "5 seconds"
    validation: "Match template to assessment objectives"
    
  step_3_automated_population:
    action: "Auto-populate template fields with actual assessment data"
    time_estimate: "20-30 seconds"
    validation: "Verify data accuracy and completeness"
    
  step_4_validation_completion:
    action: "Complete all anti-fiction validation checkpoints"
    time_estimate: "15-20 seconds"
    validation: "Ensure all validation requirements satisfied"
    
  step_5_quality_review:
    action: "Final quality check and formatting validation"
    time_estimate: "10-15 seconds"
    validation: "Confirm report ready for delivery"
```

## Success Metrics

### Time Reduction Targets
```yaml
time_metrics:
  traditional_report_generation:
    manual_data_compilation: "2-3 minutes"
    manual_writing: "3-5 minutes"
    manual_formatting: "1-2 minutes"
    manual_validation: "1-2 minutes"
    total_traditional_time: "7-12 minutes"
    
  automated_report_generation:
    automated_data_import: "10-15 seconds"
    automated_template_population: "20-30 seconds"
    automated_validation: "15-20 seconds"
    quality_review: "10-15 seconds"
    total_automated_time: "55-80 seconds"
    
  time_reduction_achieved: "80-90% reduction in report generation time"
```

### Quality Assurance Metrics
```yaml
quality_metrics:
  completeness_accuracy: ">98% of required sections populated correctly"
  data_accuracy: "100% alignment between tool outputs and report data"
  validation_compliance: ">95% of validation checkpoints satisfied"
  evidence_traceability: "100% of findings traceable to source evidence"
```

This report generation system automates the creation of comprehensive assessment reports, reducing generation time by 80-90% while ensuring complete documentation and preventing fictional results through built-in validation checkpoints.