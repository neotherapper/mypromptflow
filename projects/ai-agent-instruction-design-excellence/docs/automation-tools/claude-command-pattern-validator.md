# Claude Command Pattern Validator

**Purpose**: Automated detection and validation of Claude command patterns for AI agent instruction compliance
**Input**: Target Claude command file (`.claude/commands/*.md`)
**Output**: Pattern compliance score with specific recommendations for AI agent optimization
**Integration**: Works with enhanced claude-command-evaluator and meta/validation/validators/framework/vagueness-detector

## Claude Command Pattern Detection

### Core Pattern Requirements (Critical - 5 points each)

```yaml
claude_command_patterns:
  direct_instruction_start:
    pattern: "Command must start with direct actionable instruction"
    detection: "First line contains actionable verb + $ARGUMENTS if parameterized"
    examples:
      excellent: "Please analyze and fix the GitHub issue: $ARGUMENTS"
      poor: "# /validate-pr Command"
    
  arguments_integration:
    pattern: "$ARGUMENTS pattern for parameterized commands"
    detection: "Commands taking parameters must reference $ARGUMENTS meaningfully"
    examples:
      excellent: "Conduct comprehensive research using the intelligent hybrid orchestrator for: $ARGUMENTS"
      poor: "This command takes a PR number as argument"
    
  human_artifact_elimination:
    pattern: "No human documentation sections"
    detection: "Must not contain ## Usage, ## Command Description, ## Implementation Notes"
    examples:
      excellent: "Direct instruction without explanation sections"
      poor: "## Usage\n```bash\n/command [args]\n```"
```

### AI Agent Instruction Patterns (High Priority - 3 points each)

```yaml
ai_agent_patterns:
  immediate_actionability:
    pattern: "Instructions executable without interpretation"
    detection: "No vague terms, specific commands, exact procedures"
    validation: "AI agent can execute each step without clarification"
    
  concrete_specificity:
    pattern: "Specific steps instead of abstract concepts"
    detection: "Numbered steps, exact commands, measurable criteria"
    validation: "No 'effectively', 'appropriately', 'good quality' terms"
    
  self_sufficiency:
    pattern: "Complete internal context or proper @file_path references"
    detection: "No external dependencies, all context embedded"
    validation: "References are accessible within project structure"
    
  step_clarity:
    pattern: "Clear execution sequence with specific actions"
    detection: "Logical flow, specific commands, clear validation steps"
    validation: "Each step has specific action and success criteria"
```

### Anti-Pattern Detection (Critical Issues - 5 points deduction each)

```yaml
anti_patterns:
  usage_section:
    pattern: "^## Usage"
    issue: "Human documentation artifact - AI agents don't need usage examples"
    recommendation: "Remove section, integrate parameters into instruction with $ARGUMENTS"
    
  command_description:
    pattern: "^## (Command )?Description"
    issue: "Meta-explanatory content inappropriate for AI instructions"
    recommendation: "Start directly with actionable instruction"
    
  implementation_notes:
    pattern: "^## Implementation Notes"
    issue: "Meta-commentary violates immediate actionability principle"
    recommendation: "Integrate necessary context into instruction steps"
    
  meta_explanation:
    pattern: "\\b(this command|this instruction|this tool)\\s+(does|performs|executes|provides)"
    issue: "Explains what command does instead of providing direct instruction"
    recommendation: "Transform to direct actionable command for AI agent"
    
  human_oriented_language:
    pattern: "\\b(you can|you should|users can|for users)"
    issue: "Human-oriented language inappropriate for AI agent instructions"
    recommendation: "Use direct imperative instructions for AI agent execution"
```

## Validation Scoring System

### Scoring Algorithm
```yaml
scoring_method:
  total_possible: 100
  core_patterns: 15 points (3 patterns × 5 points each)
  ai_agent_patterns: 60 points (4 patterns × 15 points each)
  anti_pattern_deductions: -25 points maximum (5 anti-patterns × 5 points each)
  bonus_excellence: 10 points for exceptional AI agent optimization
  
thresholds:
  excellent: 90-100 (AI agent optimized)
  good: 75-89 (Minor improvements needed)
  acceptable: 60-74 (Functional but needs enhancement)
  needs_improvement: 40-59 (Significant issues)
  unacceptable: 0-39 (Major revision required)
```

### Pattern Assessment Matrix
```yaml
assessment_dimensions:
  pattern_compliance:
    weight: 40%
    criteria: "Core Claude command patterns followed"
    
  ai_agent_effectiveness:
    weight: 35%
    criteria: "Immediate actionability for AI agents"
    
  anti_pattern_elimination:
    weight: 25%
    criteria: "Human documentation artifacts removed"
```

## Automated Pattern Analysis

### Detection Workflow
```yaml
validation_steps:
  step_1_file_analysis:
    action: "Load and parse Claude command file"
    validation: "Confirm .claude/commands/*.md file format"
    
  step_2_pattern_detection:
    action: "Apply core pattern detection algorithms"
    process: "Check for direct instruction start, $ARGUMENTS usage, structure"
    
  step_3_anti_pattern_scanning:
    action: "Scan for human documentation artifacts"
    process: "Detect Usage, Description, Implementation Notes sections"
    
  step_4_ai_agent_assessment:
    action: "Evaluate AI agent instruction quality"
    process: "Check actionability, specificity, self-sufficiency"
    
  step_5_scoring_calculation:
    action: "Calculate pattern compliance score"
    process: "Apply scoring algorithm with deductions"
    
  step_6_recommendation_generation:
    action: "Generate specific improvement recommendations"
    process: "Provide actionable steps for AI agent optimization"
```

### Output Format
```yaml
claude_command_analysis:
  file: ".claude/commands/command-name.md"
  pattern_compliance_score: 85/100
  classification: "Good - Minor improvements needed"
  
  core_pattern_analysis:
    direct_instruction_start: 5/5
    arguments_integration: 3/5  # Missing $ARGUMENTS
    human_artifact_elimination: 5/5
    
  ai_agent_pattern_analysis:
    immediate_actionability: 13/15
    concrete_specificity: 14/15
    self_sufficiency: 15/15
    step_clarity: 12/15
    
  anti_pattern_deductions:
    usage_section: -5 points
    command_description: -5 points
    meta_explanation: 0 points
    
  specific_issues:
    - "Line 5: ## Usage section detected (human documentation artifact)"
    - "Line 10: ## Command Description section (meta-explanatory content)"
    - "Missing $ARGUMENTS pattern for parameterized command"
    
  ai_optimization_recommendations:
    - "Remove ## Usage section - integrate parameters with $ARGUMENTS pattern"
    - "Remove ## Command Description - start directly with actionable instruction"
    - "Add $ARGUMENTS reference: 'Execute validation for PR: $ARGUMENTS'"
```

## Integration with Enhanced Validation Framework

### Framework Alignment
```yaml
integration_points:
  claude_command_evaluator: "Primary validator for .claude/commands/*.md files"
  vagueness_detector: "Secondary validation for language quality (meta/validation/validators/framework/vagueness-detector)"
  ai_instruction_evaluator: "Comprehensive AI instruction assessment"
  
coordination_pattern:
  primary_validation: "claude-command-evaluator applies this pattern logic"
  secondary_validation: "meta/validation/validators/framework/vagueness-detector checks for human artifacts"
  comprehensive_assessment: "ai-instruction-evaluator provides framework compliance"
```

### Quality Gate Integration
```yaml
quality_gates:
  gate_1_pattern_compliance:
    condition: pattern_score >= 75
    action: "PASS - Acceptable Claude command pattern"
    
  gate_2_human_artifacts:
    condition: anti_pattern_deductions == 0
    action: "PASS - No human documentation artifacts"
    
  gate_3_ai_agent_readiness:
    condition: ai_agent_score >= 80
    action: "PASS - Ready for AI agent consumption"
    
  gate_4_excellence:
    condition: total_score >= 90
    action: "EXCELLENT - Exemplary AI agent instruction"
```

## Validation Examples

### Excellent Pattern (fix-github-issue.md)
```yaml
analysis_result:
  pattern_compliance: 15/15
  ai_agent_effectiveness: 60/60
  anti_pattern_deductions: 0
  excellence_bonus: 10
  total_score: 95/100
  
strengths:
  - "Perfect $ARGUMENTS integration: 'Please analyze and fix the GitHub issue: $ARGUMENTS'"
  - "Direct actionable instruction start"
  - "No human documentation artifacts"
  - "Specific steps with exact commands"
  - "Complete self-sufficiency"
```

### Poor Pattern (validate-pr.md - before fixes)
```yaml
analysis_result:
  pattern_compliance: 5/15  # Missing $ARGUMENTS, has human artifacts
  ai_agent_effectiveness: 45/60  # Good content but presentation issues
  anti_pattern_deductions: -15  # Usage, Description, Implementation Notes
  total_score: 35/100
  
critical_issues:
  - "## Usage section (human documentation artifact)"
  - "## Command Description (meta-explanatory content)"
  - "## Implementation Notes (meta-commentary)"
  - "Missing $ARGUMENTS pattern for parameterized command"
  - "Meta-explanatory language: 'This instruction guides AI agents'"
```

## Usage Instructions for AI Agents

### Rapid Assessment Protocol
```yaml
quick_validation:
  time_target: "60-90 seconds per command"
  
  step_1_scan: "Check first 5 lines for direct instruction vs title/description"
  step_2_arguments: "Search for $ARGUMENTS if command appears parameterized"
  step_3_sections: "Scan for ## Usage, ## Description, ## Implementation Notes"
  step_4_language: "Check for meta-explanatory vs actionable language"
  step_5_score: "Apply scoring algorithm and generate recommendations"
```

### Integration Commands
```bash
# Apply claude command pattern validation
validate_claude_command ".claude/commands/command-name.md"

# Batch validation for all commands
for file in .claude/commands/*.md; do
  validate_claude_command "$file"
done

# Integration with enhanced framework
apply_ai_instruction_excellence ".claude/commands/command-name.md"
```

## Success Metrics

### Validation Effectiveness
- **Pattern Detection Accuracy**: 100% for core patterns and anti-patterns
- **AI Agent Readiness Assessment**: 95% correlation with manual expert evaluation
- **Improvement Recommendation Quality**: 90% of recommendations lead to measurable improvement
- **Integration Efficiency**: Seamless integration with existing validation framework

### Performance Targets
- **Assessment Speed**: 60-90 seconds per Claude command
- **Pattern Coverage**: 100% detection of human documentation artifacts
- **Recommendation Accuracy**: 95% actionable improvement suggestions
- **Framework Alignment**: 100% compliance with AI Agent Instruction Design Excellence principles

This validator ensures Claude commands serve as effective AI agent instructions, eliminating human documentation artifacts and optimizing for immediate actionability and concrete specificity.