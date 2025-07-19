# AI Agent Usage Instructions for Automation Tools

## Purpose

Comprehensive usage instructions for AI agents to effectively utilize the automation tool suite for rapid framework assessments while maintaining accuracy and preventing fictional results.

## Pre-Assessment Preparation

### Essential Prerequisites
```yaml
prerequisites:
  anti_fiction_compliance:
    requirement: "Read and understand anti-fiction validation protocol"
    location: "../validation/anti-fiction-validation-protocol.md"
    critical_points:
      - no_estimation_permitted: "All assessments must be based on actual file analysis"
      - evidence_requirement: "Every finding must include specific line references"
      - calculation_transparency: "All scoring must show step-by-step calculations"
      - time_realism: "Assessment time must be realistic (2-3 minutes minimum)"
    
  tool_familiarity:
    requirement: "Understand each automation tool's purpose and output format"
    tools_to_review:
      - vagueness_detector: "Automated vague term detection and scoring"
      - dependency_scanner: "External dependency identification and classification"
      - checklist_automator: "Framework checklist application with evidence collection"
      - assessment_calculator: "5-dimensional scoring with weighted calculations"
      - report_generator: "Comprehensive report generation with validation checkpoints"
    
  file_access_verification:
    requirement: "Confirm target instruction file is accessible and readable"
    validation_steps:
      - verify_file_path: "Ensure absolute file path is correct and accessible"
      - confirm_file_content: "Verify file contains instruction content to be assessed"
      - check_file_size: "Ensure file is reasonable size for analysis (not empty, not excessively large)"
```

## Step-by-Step Usage Workflow

### Step 1: Assessment Initialization (10-15 seconds)
```yaml
step_1_initialization:
  action_items:
    - record_start_time: "Document assessment start time for tracking"
    - verify_file_access: "Confirm target instruction file is readable"
    - determine_assessment_scope: "Select quick (2-3 min) or comprehensive (5-8 min) assessment"
    - prepare_tool_sequence: "Plan which tools to use based on scope"
    
  validation_checkpoints:
    - file_path_documented: "Record absolute file path for all tools"
    - assessment_scope_clear: "Document whether quick or comprehensive assessment"
    - start_time_logged: "Record timestamp for performance tracking"
    
  common_errors_to_avoid:
    - relative_file_paths: "Always use absolute paths to prevent tool failures"
    - unclear_scope: "Define assessment scope before beginning tool execution"
    - missing_timestamp: "Always document start time for time validation"
```

### Step 2: Concurrent Analysis Phase (45-60 seconds)
```yaml
step_2_concurrent_analysis:
  vagueness_detection_execution:
    tool: "vagueness-detector.md"
    inputs_required:
      - target_file_path: "absolute path to instruction file"
    execution_steps:
      - apply_regex_patterns: "Run all vagueness detection patterns systematically"
      - calculate_density: "Compute vagueness density using documented formula"
      - generate_replacements: "Create concrete replacement suggestions"
      - document_findings: "Record all findings with line references"
    expected_outputs:
      - vagueness_density: "percentage value (e.g., 8.5%)"
      - severity_breakdown: "counts by high/medium/low severity"
      - line_findings: "specific vague terms with line numbers"
      - replacement_suggestions: "concrete alternatives for improvement"
    time_estimate: "30-45 seconds"
    
  dependency_scanning_execution:
    tool: "dependency-scanner.md"
    inputs_required:
      - target_file_path: "absolute path to instruction file"
    execution_steps:
      - apply_dependency_patterns: "Run all dependency detection patterns systematically"
      - classify_dependencies: "Categorize by framework/API/documentation/research"
      - calculate_impact: "Compute dependency density and self-sufficiency score"
      - generate_alternatives: "Create self-sufficient replacement suggestions"
    expected_outputs:
      - dependency_density: "percentage value (e.g., 6.2%)"
      - dependency_breakdown: "counts by dependency type"
      - line_findings: "specific dependencies with line numbers"
      - self_sufficiency_score: "calculated portability rating"
    time_estimate: "30-45 seconds"
    
  concurrent_execution_note: "These tools can run simultaneously to optimize time"
```

### Step 3: Checklist Application Phase (60-90 seconds)
```yaml
step_3_checklist_application:
  framework_selection:
    selection_logic: "Use framework-selector.md logic based on Phase 2 findings"
    decision_criteria:
      - high_vagueness: "Apply concreteness framework (vagueness_density > 10%)"
      - high_dependencies: "Apply self-sufficiency framework (dependency_density > 8%)"
      - execution_issues: "Apply actionable framework (unclear procedures detected)"
      - unclear_purpose: "Apply purpose-driven framework (purpose ambiguity detected)"
      - multiple_issues: "Apply multiple frameworks sequentially"
    
  checklist_execution:
    tool: "checklist-automator.md"
    inputs_required:
      - target_file_path: "absolute path to instruction file"
      - framework_selection: "framework(s) selected based on Phase 2 analysis"
      - vagueness_context: "vagueness analysis from Phase 2"
      - dependency_context: "dependency analysis from Phase 2"
    execution_steps:
      - load_framework_checklist: "Load appropriate framework checklist items"
      - apply_systematic_validation: "Validate each checklist item against file content"
      - collect_evidence: "Document evidence or gaps for every item"
      - calculate_completion: "Compute completion percentages"
      - prioritize_improvements: "Identify and prioritize improvement areas"
    expected_outputs:
      - checklist_results: "pass/fail status for each item with evidence"
      - completion_percentages: "percentages by framework and dimension"
      - gap_analysis: "specific improvement recommendations"
      - evidence_collection: "line-referenced findings for all items"
    time_estimate: "60-90 seconds"
```

### Step 4: Score Calculation Phase (15-25 seconds)
```yaml
step_4_score_calculation:
  assessment_calculation:
    tool: "assessment-calculator.md"
    inputs_required:
      - checklist_results: "from checklist-automator execution"
      - vagueness_density: "from vagueness-detector execution"
      - dependency_density: "from dependency-scanner execution"
      - evidence_collection: "aggregated from all previous tools"
    execution_steps:
      - calculate_dimensional_scores: "Compute scores for all 5 dimensions"
      - apply_weighting_formula: "Use documented weighting (25%, 25%, 20%, 20%, 10%)"
      - integrate_penalties: "Apply vagueness and dependency penalties"
      - determine_classification: "Apply quality thresholds (excellent/good/fair/poor)"
      - validate_calculations: "Verify mathematical accuracy"
    expected_outputs:
      - dimensional_scores: "5 dimension scores (0-5 scale)"
      - overall_quality_score: "weighted final score (0-5 scale)"
      - quality_classification: "excellent/good/fair/poor classification"
      - penalty_adjustments: "documentation of penalty calculations"
      - quality_gates: "pass/fail status for each quality gate"
    time_estimate: "15-25 seconds"
```

### Step 5: Report Generation Phase (30-45 seconds)
```yaml
step_5_report_generation:
  report_creation:
    tool: "report-generator.md"
    inputs_required:
      - all_tool_outputs: "complete dataset from Steps 2-4"
      - assessment_metadata: "timing, methodology, scope information"
      - validation_checkpoints: "anti-fiction compliance documentation"
    execution_steps:
      - select_report_template: "Choose appropriate template based on assessment scope"
      - populate_template_fields: "Auto-populate template with actual assessment data"
      - complete_validation_sections: "Fill all anti-fiction validation checkpoints"
      - generate_improvement_plan: "Create prioritized action items"
      - perform_quality_review: "Final consistency and completeness check"
    expected_outputs:
      - executive_summary: "key findings and overall recommendation"
      - dimensional_analysis: "detailed breakdown by framework dimension"
      - improvement_action_plan: "prioritized improvement recommendations"
      - validation_documentation: "anti-fiction compliance evidence"
      - quality_certification: "assessment methodology and accuracy validation"
    time_estimate: "30-45 seconds"
```

## Critical Usage Guidelines

### Anti-Fiction Compliance Requirements
```yaml
anti_fiction_compliance:
  evidence_requirements:
    all_findings_referenced: "Every finding must include specific file line references"
    exact_quotes_provided: "Use exact text quotes from target file, not paraphrases"
    no_placeholder_data: "Never use placeholder scores or generic findings"
    calculation_transparency: "Show all mathematical calculations step-by-step"
    
  time_tracking_requirements:
    realistic_timing: "Assessment time must be realistic (minimum 2-3 minutes)"
    actual_time_documentation: "Record actual time taken, not estimated time"
    phase_timing_breakdown: "Document time for each phase execution"
    
  methodology_documentation:
    tools_used_listed: "Document which specific tools were applied"
    framework_selection_justified: "Explain framework selection logic"
    validation_checkpoints_completed: "Confirm all validation requirements met"
```

### Common Mistakes to Avoid
```yaml
common_mistakes:
  assessment_shortcuts:
    mistake: "Skipping tool phases to save time"
    consequence: "Incomplete analysis and potential fictional results"
    prevention: "Execute all required tool phases systematically"
    
  evidence_fabrication:
    mistake: "Creating generic findings without specific file references"
    consequence: "Violation of anti-fiction validation protocol"
    prevention: "Always provide exact line numbers and file quotes"
    
  calculation_estimation:
    mistake: "Estimating scores without applying documented formulas"
    consequence: "Mathematical inaccuracy and fictional scoring"
    prevention: "Use automation tools for all calculations"
    
  incomplete_validation:
    mistake: "Skipping validation checkpoints to accelerate completion"
    consequence: "Assessment fails quality assurance requirements"
    prevention: "Complete all validation sections systematically"
```

## Quality Assurance Protocols

### Self-Validation Checklist
```yaml
self_validation_checklist:
  before_starting_assessment:
    - file_accessibility_confirmed: "Target file is readable and contains instruction content"
    - tool_familiarity_verified: "Understanding of each tool's purpose and usage"
    - assessment_scope_defined: "Clear decision on quick vs comprehensive assessment"
    - start_time_documented: "Assessment start timestamp recorded"
    
  during_assessment_execution:
    - phase_completion_verified: "Each tool phase completed successfully"
    - output_quality_checked: "Tool outputs contain required data fields"
    - evidence_collection_confirmed: "All findings include file references"
    - calculation_accuracy_verified: "Mathematical calculations shown step-by-step"
    
  after_assessment_completion:
    - validation_checkpoints_completed: "All anti-fiction validation requirements met"
    - report_completeness_verified: "All required report sections populated"
    - time_tracking_documented: "Actual assessment time recorded"
    - quality_gates_evaluated: "Quality gate pass/fail status determined"
```

### Performance Monitoring
```yaml
performance_monitoring:
  time_tracking_metrics:
    target_completion_time: "2-3 minutes for complete assessment"
    phase_time_breakdown:
      - initialization: "10-15 seconds"
      - concurrent_analysis: "45-60 seconds"
      - checklist_application: "60-90 seconds"
      - score_calculation: "15-25 seconds"
      - report_generation: "30-45 seconds"
    
  accuracy_validation:
    evidence_traceability: "100% of findings traceable to source file"
    calculation_accuracy: "100% mathematical accuracy in scoring"
    consistency_verification: "Repeated assessments produce identical results"
    
  quality_assurance:
    anti_fiction_compliance: "100% validation checkpoint completion"
    methodology_documentation: "Complete tool usage and selection justification"
    improvement_actionability: "All recommendations specific and implementable"
```

## Troubleshooting Guide

### Common Issues and Solutions
```yaml
troubleshooting:
  tool_execution_failures:
    vagueness_detector_issues:
      symptom: "Pattern matching fails or produces no results"
      diagnosis: "File encoding issues or pattern configuration problems"
      solution: "Verify file UTF-8 encoding and pattern regex syntax"
      
    dependency_scanner_issues:
      symptom: "Dependencies not detected or misclassified"
      diagnosis: "Pattern coverage gaps or classification logic errors"
      solution: "Review dependency patterns and update classification criteria"
      
    checklist_automator_issues:
      symptom: "Evidence collection incomplete or inaccurate"
      diagnosis: "Framework selection error or checklist application problems"
      solution: "Verify framework selection logic and checklist item validation"
      
    assessment_calculator_issues:
      symptom: "Score calculations incorrect or inconsistent"
      diagnosis: "Input data format problems or formula application errors"
      solution: "Validate input data structure and formula implementation"
      
    report_generator_issues:
      symptom: "Report generation incomplete or missing sections"
      diagnosis: "Template selection error or data integration problems"
      solution: "Verify template selection and data format compatibility"
  
  integration_problems:
    data_consistency_errors:
      symptom: "Tool outputs don't integrate properly"
      diagnosis: "Data format mismatches or field name inconsistencies"
      solution: "Standardize data formats and validate field mappings"
      
    validation_checkpoint_failures:
      symptom: "Validation requirements not met"
      diagnosis: "Incomplete evidence collection or documentation gaps"
      solution: "Review validation requirements and complete missing documentation"
      
    time_performance_issues:
      symptom: "Assessment takes longer than target time"
      diagnosis: "Tool inefficiencies or sequential execution problems"
      solution: "Optimize tool execution and implement concurrent processing"
```

## Advanced Usage Patterns

### Assessment Scope Optimization
```yaml
scope_optimization:
  quick_assessment_pattern:
    use_case: "Rapid quality triage for instruction prioritization"
    tools_used: ["vagueness-detector", "dependency-scanner", "assessment-calculator", "report-generator(quick)"]
    time_target: "2-3 minutes"
    output_focus: "overall quality score and top 3 improvement recommendations"
    
  comprehensive_assessment_pattern:
    use_case: "Thorough analysis for instruction optimization"
    tools_used: ["all five tools with full checklist application"]
    time_target: "3-4 minutes"
    output_focus: "complete dimensional analysis and detailed improvement action plan"
    
  production_readiness_pattern:
    use_case: "Final validation before instruction deployment"
    tools_used: ["all five tools plus specialized compliance validation"]
    time_target: "4-5 minutes"
    output_focus: "deployment readiness certification and risk assessment"
```

This comprehensive usage guide provides AI agents with the detailed instructions needed to effectively utilize the automation tool suite while maintaining assessment accuracy and preventing fictional results.