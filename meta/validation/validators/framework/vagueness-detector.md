# Vagueness Detection Scanner

**Location**: meta/validators/vagueness-detector.md  
**Purpose**: Automated detection and scoring of vague language in AI agent instructions  
**Input**: Target instruction file (absolute path required)  
**Output**: Vagueness density percentage with line references and concrete replacement suggestions  
**Integration**: Works with self-healing protocol for automatic correction  

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

### Critical Severity Human Documentation Artifacts (Score: 5 points each)
```regex
Pattern Set I: Human Documentation Sections
- ^##\s+(Usage|Command Description|Implementation Notes|How to Use|Overview|Introduction)\b
- ^###\s+(Usage|Command Description|Implementation Notes)\b

Pattern Set J: Meta-Explanatory Content
- \b(this command|this instruction|this tool)\s+(does|performs|executes|provides|allows|enables)\b
- \b(the purpose of|designed to|intended to|meant to)\s+
- \b(allows users to|enables users to|helps users|provides users)\b
- \b(provides the ability to|gives you the ability|you can use this)\b

Pattern Set K: Human-Oriented Language
- \b(you can|you should|you will|you need to|you must)\b
- \b(users can|users should|users will|users need)\b
- \b(for users|for humans|human readable|user friendly)\b
- \b(user experience|user interface|command usage)\b
```

## Severity Calculation Algorithm

### Vagueness Density Formula
```yaml
calculation_method:
  total_words: count(all_words_in_file)
  vague_points: (high_severity_count * 3) + (medium_severity_count * 2) + (low_severity_count * 1)
  human_artifact_points: (critical_human_artifacts * 5)
  total_quality_issues: vague_points + human_artifact_points
  vagueness_density: vague_points / total_words * 100
  human_artifacts: count(critical_human_artifacts)
  
severity_thresholds:
  critical: vagueness_density >= 15.0 OR human_artifacts >= 3    # Blocks production deployment
  high: vagueness_density >= 10.0 OR human_artifacts >= 2        # Requires correction before deployment
  medium: vagueness_density >= 5.0 OR human_artifacts >= 1       # Recommended for improvement
  low: vagueness_density >= 2.0 AND human_artifacts == 0         # Acceptable with minor improvements
  minimal: vagueness_density < 2.0 AND human_artifacts == 0      # Production ready for AI agents
```

### Line-by-Line Analysis Output Format
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
    human_artifacts_found:
      - artifact: "specific human documentation pattern"
        severity: "critical"
        score: 5
        ai_agent_transformation: "transformation to AI agent instruction"
    line_total_score: integer
    
  file_summary:
    total_lines_analyzed: integer
    lines_with_vagueness: integer
    lines_with_human_artifacts: integer
    total_vague_terms: integer
    total_human_artifacts: integer
    severity_breakdown:
      critical_human_artifacts: integer
      high_severity: integer
      medium_severity: integer
      low_severity: integer
    calculated_vagueness_density: float
    human_artifact_density: float
    overall_severity_rating: "critical|high|medium|low|minimal"
    ai_agent_readiness: "ready|needs_improvement|requires_major_revision"
```

## Automated Replacement Suggestions

### High-Priority Replacement Patterns
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
    
  "efficiently":
    concrete_alternatives:
      - "within [time limit]"
      - "using [resource constraint]"
      - "through [optimization method]"
    
  "successfully":
    concrete_alternatives:
      - "achieving [specific outcome]"
      - "meeting [defined criteria]"
      - "completing [measurable goal]"
    
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
    
  "sufficient":
    concrete_alternatives:
      - "meets [requirement threshold]"
      - "achieves [minimum standard]"
      - "satisfies [specific criteria]"
    
  "## Usage":
    ai_agent_transformation:
      - "Remove section - AI agents don't need usage examples"
      - "Integrate parameter information directly into instruction"
      - "Use $ARGUMENTS pattern for parameter handling"
    replacement_note: "Human documentation artifact - not needed for AI agents"
    
  "## Command Description":
    ai_agent_transformation:
      - "Remove section - AI agents don't need meta-explanations"
      - "Start directly with actionable instruction"
      - "Focus on what AI agent should do, not what command does"
    replacement_note: "Meta-explanatory content inappropriate for AI instructions"
    
  "this command does":
    ai_agent_transformation:
      - "Replace with direct instruction: 'Execute [specific steps]'"
      - "Transform to actionable command: 'Perform [specific actions]'"
      - "Convert to AI instruction: '[Direct command without explanation]'"
    replacement_note: "Meta-commentary should be direct actionable instruction"
    
  "you can":
    ai_agent_transformation:
      - "Replace with direct instruction: 'Execute [specific action]'"
      - "Transform to AI command: 'Perform [exact steps]'"
      - "Convert to agent instruction: '[Direct imperative]'"
    replacement_note: "Human-oriented language inappropriate for AI agent instructions"
```

### Context-Aware Replacement Examples
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
    
  git_context:
    vague_term: "handle errors appropriately"
    concrete_replacement: "handle errors using defined recovery procedures: check git branch status with `git branch -v` and report configuration issues"
    
  validation_context:
    vague_term: "process files efficiently"
    concrete_replacement: "process files using pattern matching classification: check file path against `.claude/commands/*.md` pattern"
    
  human_artifact_context:
    human_pattern: "## Usage\n```bash\n/command [args]\n```"
    ai_agent_replacement: "Direct instruction using $ARGUMENTS pattern: 'Execute task for: $ARGUMENTS'"
    transformation_note: "Remove human usage examples, integrate parameters into actionable instruction"
    
  meta_explanation_context:
    human_pattern: "This command allows users to validate PR files"
    ai_agent_replacement: "Validate PR files using the following steps:"
    transformation_note: "Replace meta-explanation with direct actionable instruction for AI agent"
    
  claude_command_context:
    human_pattern: "## Command Description\nThis tool provides..." 
    ai_agent_replacement: "[Direct actionable instruction starting immediately]"
    transformation_note: "Claude commands should start with direct instruction, not description"
```

## Automated Quality Gates

### Vagueness Threshold Gates
```yaml
quality_gates:
  gate_1_critical:
    condition: vagueness_density >= 15.0 OR human_artifacts >= 3
    action: "BLOCK - Major revision required for AI agent instruction readiness"
    message: "Critical issues detected: excessive vagueness or human documentation artifacts. Transform to AI agent instruction format."
    
  gate_2_high:
    condition: vagueness_density >= 10.0 OR human_artifacts >= 2
    action: "WARNING - Significant AI agent instruction issues detected"
    message: "High vagueness or human artifacts detected. Apply AI Agent Instruction Design Excellence framework."
    
  gate_3_human_artifacts:
    condition: human_artifacts >= 1
    action: "WARNING - Human documentation artifacts detected in AI instruction"
    message: "Remove Usage, Description, or Implementation Notes sections. Focus on direct AI agent actionability."
    
  gate_4_medium:
    condition: vagueness_density >= 5.0 AND human_artifacts == 0
    action: "RECOMMEND - Moderate vagueness detected"
    message: "Medium vagueness level. Consider improvement for optimal AI agent clarity."
    
  gate_5_acceptable:
    condition: vagueness_density < 5.0 AND human_artifacts == 0
    action: "PASS - Acceptable for AI agent consumption"
    message: "Instruction meets AI agent effectiveness standards."
```

## Usage Instructions for AI Agents

### Step-by-Step Validation Workflow

```yaml
workflow_steps:
  step_1_preparation:
    action: "Load target instruction file into analysis buffer"
    validation: "Confirm file content visible and readable"
    
  step_2_pattern_application:
    action: "Apply all regex patterns to file content systematically"
    process: "Scan each line for high, medium, and low severity terms"
    validation: "Document each pattern match with line reference"
    
  step_3_scoring_calculation:
    action: "Calculate vagueness density using documented formula"
    process: "Sum severity points and divide by total word count"
    validation: "Show calculation step-by-step with actual numbers"
    
  step_4_severity_assessment:
    action: "Apply severity thresholds and determine overall rating"
    validation: "Reference threshold criteria and justify rating"
    
  step_5_evidence_compilation:
    action: "Compile findings into structured output format"
    validation: "Ensure all findings have line references and concrete suggestions"
```

### Integration with Self-Healing Protocol

**When Vagueness Detected**:
```markdown
## Vagueness Detection Alert
"⚠️ VAGUENESS DETECTED: [density]% vagueness density ([severity] level)
High severity terms: [count] ([specific_terms])
Medium severity terms: [count] ([specific_terms])
Low severity terms: [count] ([specific_terms])

🔧 APPLYING CORRECTIONS:
- Replacing '[vague_term]' with '[concrete_alternative]' (Line [number])
- Updating '[vague_phrase]' to '[specific_implementation]' (Line [number])

✅ VALIDATION: Re-calculating vagueness density post-correction..."
```

### Validation Commands for AI Agents

**Manual Validation Process**:
```bash
# Step 1: Count total words in target file
wc -w [target_file]

# Step 2: Search for critical human documentation artifacts
grep -n -E '^##\s+(Usage|Command Description|Implementation Notes|How to Use|Overview|Introduction)\b' [target_file]
grep -n -i -E '\b(this command|this instruction|this tool)\s+(does|performs|executes|provides|allows|enables)\b' [target_file]
grep -n -i -E '\b(you can|you should|you will|users can|users should|for users|for humans)\b' [target_file]

# Step 3: Search for high severity vague terms
grep -n -i -E '\b(effectively|efficiently|appropriately|properly|optimally|ideally|seamlessly|smoothly|successfully|correctly|accurately|precisely|several|some|many|various|multiple|numerous|plenty|adequate|sufficient|reasonable|appropriate|suitable)\b' [target_file]

# Step 4: Search for medium severity terms  
grep -n -i -E '\b(carefully|thoroughly|comprehensively|diligently|systematically|methodically|regularly|consistently|continuously|frequently|occasionally|periodically|soon|quickly|rapidly|promptly|eventually|ultimately|gradually|relevant|important|significant|critical|necessary|essential|key|main|overall|general|basic|standard)\b' [target_file]

# Step 5: Search for low severity terms
grep -n -i -E '\b(quite|rather|fairly|somewhat|relatively|moderately|reasonably|potentially|possibly|likely|handle|manage|deal\.with|process|coordinate|organize|arrange|setup|implement|develop|create|build)\b' [target_file]

# Step 6: Calculate AI agent instruction quality
# Formula: ((human_artifacts * 5) + (high_count * 3) + (medium_count * 2) + (low_count * 1)) / total_words * 100
```

## Integration Points

### Framework Integration
```yaml
framework_connections:
  self_healing_protocol: "meta/validation/self-healing-protocol.md"
  error_detection_patterns: "meta/validation/self-healing-error-detection-patterns.md"
  anti_fiction_validator: "meta/validators/anti-fiction-validator.md"
  validation_framework_command: "meta/validation/validation-framework-command.md"
```

### Quality Assurance Integration
```yaml
quality_gates:
  command_creation: "Apply vagueness detection before command deployment"
  instruction_writing: "Maintain vagueness density below 5% for production"
  framework_validation: "Include vagueness assessment in comprehensive validation"
  self_healing_activation: "Trigger correction when density exceeds thresholds"
```

### Performance Targets
- **Detection Accuracy**: 95% pattern matching accuracy for vague terms and 100% for human artifacts
- **Assessment Speed**: Complete analysis within 2-3 minutes for standard instruction files
- **Correction Effectiveness**: 80% vagueness reduction and 100% human artifact elimination
- **Quality Improvement**: 90% of corrected instructions meet AI agent production standards
- **AI Agent Readiness**: 100% human documentation artifact detection and transformation

**Success Threshold**: Vagueness density below 5% AND zero human documentation artifacts for AI agent production deployment with clear concrete alternatives and AI agent transformations provided.