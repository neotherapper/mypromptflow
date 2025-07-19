# Vagueness Detection Scanner

**Input**: Target instruction file (absolute path required)
**Output**: Vagueness density percentage with line references
**Calculation**: (total_vague_terms * severity_weights) / total_words * 100

## Automated Vagueness Detection Patterns

### High Severity Vague Terms (Score: 3 points each)
```regex
Pattern Set A: Process Qualifiers
- \b(effectively|efficiently|appropriately|properly)\b
- \b(optimally|ideally|seamlessly|smoothly)\b
- \b(successfully|correctly|accurately|precisely)\b

Pattern Set B: Quality Descriptors
- \b(good|better|best|optimal|superior)\b
- \b(high.quality|excellent|outstanding|robust)\b
- \b(reliable|stable|secure|scalable)\b

Pattern Set C: Quantity Vagueness
- \b(several|some|many|various|multiple)\b
- \b(numerous|plenty|adequate|sufficient)\b
- \b(reasonable|appropriate|suitable)\b
```

### Medium Severity Vague Terms (Score: 2 points each)
```regex
Pattern Set D: Effort Descriptors
- \b(carefully|thoroughly|comprehensively)\b
- \b(diligently|systematically|methodically)\b
- \b(regularly|consistently|continuously)\b

Pattern Set E: Time/Frequency Vagueness
- \b(regularly|frequently|occasionally|periodically)\b
- \b(soon|quickly|rapidly|promptly)\b
- \b(eventually|ultimately|gradually)\b

Pattern Set F: Scope Ambiguity
- \b(relevant|important|significant|critical)\b
- \b(necessary|essential|key|main)\b
- \b(overall|general|basic|standard)\b
```

### Low Severity Vague Terms (Score: 1 point each)
```regex
Pattern Set G: Weak Modifiers
- \b(quite|rather|fairly|somewhat)\b
- \b(relatively|moderately|reasonably)\b
- \b(potentially|possibly|likely)\b

Pattern Set H: Generic Actions
- \b(handle|manage|deal.with|process)\b
- \b(coordinate|organize|arrange|setup)\b
- \b(implement|develop|create|build)\b
```

## Severity Calculation Algorithm

### Vagueness Density Formula
```yaml
calculation_method:
  total_words: count(all_words_in_file)
  vague_points: (high_severity_count * 3) + (medium_severity_count * 2) + (low_severity_count * 1)
  vagueness_density: vague_points / total_words * 100
  
severity_thresholds:
  critical: vagueness_density >= 15.0
  high: vagueness_density >= 10.0
  medium: vagueness_density >= 5.0
  low: vagueness_density >= 2.0
  minimal: vagueness_density < 2.0
```

### Line-by-Line Analysis Automation

```yaml
analysis_output_format:
  line_analysis:
    line_number: integer
    line_content: "exact text from file"
    vague_terms_found:
      - term: "specific vague word/phrase"
        severity: "high|medium|low"
        score: integer
        replacement_suggestion: "concrete alternative"
    line_vagueness_score: integer
    
  file_summary:
    total_lines_analyzed: integer
    lines_with_vagueness: integer
    total_vague_terms: integer
    severity_breakdown:
      high_severity: integer
      medium_severity: integer
      low_severity: integer
    calculated_vagueness_density: float
    overall_severity_rating: "critical|high|medium|low|minimal"
```

## Automated Replacement Suggestions

### High-Priority Replacements
```yaml
replacement_automation:
  "effectively":
    concrete_alternatives:
      - "using [specific method/tool]"
      - "by following [numbered steps]"
      - "through [defined process]"
    context_aware: true
    
  "appropriately":
    concrete_alternatives:
      - "according to [specific criteria]"
      - "based on [defined parameters]"
      - "following [documented standards]"
    
  "good quality":
    concrete_alternatives:
      - "meets [specific metrics/criteria]"
      - "achieves [measurable standards]"
      - "passes [defined quality gates]"
    
  "several":
    concrete_alternatives:
      - "[specific number] items"
      - "3-5 instances"
      - "a minimum of [X] cases"
```

### Context-Aware Suggestions
```yaml
context_patterns:
  coordination_context:
    vague_term: "coordinate effectively"
    concrete_replacement: "coordinate using daily standup meetings, shared task boards, and weekly progress reports"
    
  quality_context:
    vague_term: "high quality output"
    concrete_replacement: "output that passes automated tests, meets documented acceptance criteria, and receives peer review approval"
    
  timing_context:
    vague_term: "regularly monitor"
    concrete_replacement: "monitor every 15 minutes during active operations, hourly during normal operations, and daily during maintenance periods"
```

## Automated Quality Gates

### Vagueness Threshold Gates
```yaml
quality_gates:
  gate_1_critical:
    condition: vagueness_density >= 15.0
    action: "BLOCK - Instruction requires major vagueness reduction before assessment"
    message: "Critical vagueness detected. Reduce vague terms by 70% before proceeding."
    
  gate_2_high:
    condition: vagueness_density >= 10.0
    action: "WARNING - Significant vagueness detected"
    message: "High vagueness level. Consider concreteness framework application."
    
  gate_3_acceptable:
    condition: vagueness_density < 5.0
    action: "PASS - Acceptable vagueness level for assessment"
    message: "Vagueness within acceptable range for quality instruction."
```

### Evidence Collection Automation
```yaml
evidence_automation:
  finding_documentation:
    format: "Line {line_number}: '{exact_text}' contains vague term '{term}' (severity: {severity})"
    example: "Line 47: 'coordinate agents effectively using best practices' contains vague term 'effectively' (severity: high)"
    
  scoring_documentation:
    calculation_shown: true
    formula_displayed: "({high_count} × 3) + ({medium_count} × 2) + ({low_count} × 1) ÷ {total_words} × 100 = {density}%"
    threshold_reference: true
```

## Integration with Anti-Fiction Protocol

### Mandatory Validation Checkpoints
```yaml
validation_checkpoints:
  checkpoint_1_file_analysis:
    verify: "Actual file content analyzed (not estimated)"
    evidence_required:
      - file_path_documented: true
      - line_numbers_referenced: true
      - exact_text_quoted: true
      - regex_patterns_applied: true
    
  checkpoint_2_calculation_verification:
    verify: "Vagueness density calculated using documented formula"
    evidence_required:
      - math_shown: true
      - formula_referenced: true
      - manual_calculation_possible: true
      - threshold_logic_applied: true
    
  checkpoint_3_time_tracking:
    verify: "Realistic assessment time documented"
    evidence_required:
      - start_time_recorded: true
      - end_time_recorded: true
      - actual_time_within_bounds: "1-3 minutes for vagueness scanning"
```

## Usage Instructions for AI Agents

### Step-by-Step Automation Workflow

```yaml
workflow_steps:
  step_1_preparation:
    action: "Load target instruction file into analysis buffer"
    time_estimate: "10-15 seconds"
    validation: "Confirm file content visible and readable"
    
  step_2_pattern_application:
    action: "Apply all regex patterns to file content systematically"
    time_estimate: "30-45 seconds"
    validation: "Document each pattern match with line reference"
    
  step_3_scoring_calculation:
    action: "Calculate vagueness density using documented formula"
    time_estimate: "15-20 seconds"
    validation: "Show calculation step-by-step with actual numbers"
    
  step_4_severity_assessment:
    action: "Apply severity thresholds and determine overall rating"
    time_estimate: "10-15 seconds"
    validation: "Reference threshold criteria and justify rating"
    
  step_5_evidence_compilation:
    action: "Compile findings into structured output format"
    time_estimate: "20-30 seconds"
    validation: "Ensure all findings have line references and examples"
```

### Time Optimization Techniques
```yaml
optimization_methods:
  batch_pattern_processing:
    description: "Apply all regex patterns in single pass through file"
    time_savings: "Reduces analysis time by 40%"
    
  automated_scoring:
    description: "Use pre-calculated point values for immediate scoring"
    time_savings: "Eliminates manual calculation time"
    
  template_output:
    description: "Use structured templates for consistent evidence collection"
    time_savings: "Reduces documentation time by 60%"
```

**Success Threshold**: >95% pattern detection accuracy
**Performance Target**: 75-80% time reduction from manual assessment