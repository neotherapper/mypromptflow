# Framework Coherence Validator

**Authority Level**: Meta Validator  
**Parallel Safe**: true  
**Target Score**: 90+/100 compliance  
**Focus**: Structural consistency and coherence assessment with creation-time validation  

## Validator Purpose

Validates framework coherence through comprehensive structural consistency analysis combined with creation-time anti-fiction validation. Ensures logical organization, semantic alignment, and evidence-based content creation while preventing fabricated metrics during development.

## Detection Patterns

### Location-Based Detection
```yaml
primary_targets:
  - "meta/validation/**/*.md"
  - "ai/agents/**/*.md" 
  - "**/CLAUDE.md"
  - "projects/*/docs/**/*.md"
  - "ai/workflows/**/*.md"
  - "knowledge-vault/**/*.md"

secondary_targets:
  - "research/findings/**/*.md"
  - "meta/information-access/**/*.yaml"
  - ".claude/agents/*.md"
```

### Content-Based Detection
```yaml
framework_indicators:
  - "## Agent Purpose"
  - "## Validation Framework"
  - "## Assessment Dimensions"
  - "constitutional_compliance"
  - "framework_coherence"
  - "validation_criteria"

anti_fiction_triggers:
  - '\d+%' # percentage claims
  - '\d+\.\d+%' # precision percentages  
  - '≥\d+|≤\d+' # performance thresholds
  - 'accuracy of \d+%'
  - 'achieving \d+%'
  - '\d+ms|\d+s' # timing claims
```

## Assessment Framework

### 1. Structural Coherence Analysis (30% weight)

**Hierarchy Consistency Validation**:
```bash
# Check heading structure consistency
grep -n '^#' "$target_file" | head -20

# Validate section organization
grep -n -E '^#{1,4}\s+' "$target_file" | nl

# Check for consistent formatting patterns  
grep -n -E '^\*\*|^-\s|^\d+\.' "$target_file" | head -10
```

**Scoring Criteria**:
```yaml
structural_assessment:
  hierarchy_consistency: # 40% of dimension
    - logical_heading_progression
    - consistent_depth_levels
    - proper_nesting_structure
    
  organization_alignment: # 35% of dimension
    - related_content_grouping
    - logical_section_flow
    - clear_navigation_structure
    
  architecture_validation: # 25% of dimension
    - command_structure_consistency
    - parameter_format_standardization
    - integration_point_organization
```

### 2. Semantic Coherence Analysis (25% weight)

**Concept Consistency Validation**:
```bash
# Check terminology consistency
grep -n -E '\b(validate|validation|validator)\b' "$target_file" | head -10

# Identify semantic conflicts
grep -n -E '\b(should|must|shall|will|can|may)\b' "$target_file" | head -10

# Check definition consistency
grep -n -E '^\*\*.*\*\*:' "$target_file"
```

**Scoring Criteria**:
```yaml
semantic_assessment:
  concept_consistency: # 40% of dimension
    - terminology_usage_uniform
    - definition_alignment_maintained
    - concept_application_consistent
    
  logical_flow_validation: # 35% of dimension
    - cause_effect_relationships_clear
    - prerequisite_dependencies_logical
    - progression_sequence_rational
    
  contradiction_detection: # 25% of dimension
    - conflicting_instructions_identification
    - incompatible_requirements_flagging
    - inconsistent_guidance_detection
```

### 3. Evidence Authenticity Validation (20% weight)

**Creation-Time Anti-Fiction Checking**:
```bash
# Detect numeric claims requiring validation
grep -n -E '\d+%|\d+\.\d+%|≥\d+|≤\d+|\d+ms|\d+s' "$target_file"

# Check for evidence sourcing
grep -n -E 'Source:|file_path:|Measured via|Estimated based on' "$target_file"

# Identify unsupported performance claims
grep -n -E 'accuracy of \d+%|achieving \d+%|providing \d+%' "$target_file"
```

**Evidence Requirements**:
```yaml
evidence_validation:
  source_verification: # 40% of dimension
    - file_path_line_number_format
    - measurement_methodology_specified
    - estimation_basis_documented
    
  claim_substantiation: # 35% of dimension
    - numeric_claims_sourced
    - performance_metrics_measured
    - effectiveness_data_verified
    
  alternative_recommendations: # 25% of dimension
    - qualitative_replacements_suggested
    - evidence_based_alternatives_provided
    - fabricated_metrics_eliminated
```

### 4. Procedural Coherence Analysis (15% weight)

**Workflow Validation**:
```bash
# Check step sequencing
grep -n -E '^(Step|Phase)\s+\d+' "$target_file"

# Validate procedural consistency
grep -n -E '\b(then|next|after|before|following)\b' "$target_file" | head -10

# Check error handling integration
grep -n -E '\b(error|failure|exception|fallback)\b' "$target_file" | wc -l
```

**Scoring Criteria**:
```yaml
procedural_assessment:
  workflow_consistency: # 45% of dimension
    - step_sequence_logical
    - process_flow_unambiguous
    - decision_points_clear
    
  step_alignment: # 35% of dimension
    - prerequisite_completion_verified
    - output_input_matching_validated
    - dependency_satisfaction_confirmed
    
  process_validation: # 20% of dimension
    - error_handling_integration
    - recovery_procedure_alignment
    - completion_criteria_clarity
```

### 5. Terminological Coherence Analysis (10% weight)

**Terminology Consistency Check**:
```bash
# Identify key terms and frequency
grep -o -E '\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b' "$target_file" | sort | uniq -c | sort -nr | head -20

# Check definition patterns
grep -n -E '^\*\*.*\*\*:|^.*:\s*[A-Z]' "$target_file"

# Validate technical term usage
grep -n -E '\b(AI|agent|framework|validation|assessment)\b' "$target_file" | head -10
```

**Scoring Criteria**:
```yaml
terminological_assessment:
  vocabulary_consistency: # 50% of dimension
    - term_usage_standardization
    - definition_uniformity_maintained
    - synonym_management_consistent
    
  concept_mapping: # 30% of dimension
    - term_concept_relationship_clear
    - usage_context_appropriate
    - meaning_boundaries_defined
    
  conflict_resolution: # 20% of dimension
    - inconsistent_usage_resolved
    - ambiguous_references_clarified
    - terminology_scope_defined
```

## Validation Process

### Phase 1: Pre-Validation Setup
```bash
# Set target file and initialize scoring
target_file="$1"
total_score=0
dimension_scores=()

# Verify file accessibility
if [[ \! -f "$target_file" ]]; then
    echo "ERROR: Target file not accessible: $target_file"
    exit 1
fi
```

### Phase 2: Multi-Dimensional Assessment
```bash
# Execute all assessment dimensions in parallel for efficiency
{
    echo "=== Structural Coherence Analysis ==="
    structural_score=$(assess_structural_coherence "$target_file")
    echo "Structural Score: $structural_score/100"
} &

{
    echo "=== Semantic Coherence Analysis ==="
    semantic_score=$(assess_semantic_coherence "$target_file")
    echo "Semantic Score: $semantic_score/100"
} &

{
    echo "=== Evidence Authenticity Validation ==="
    evidence_score=$(validate_evidence_authenticity "$target_file")
    echo "Evidence Score: $evidence_score/100"
} &

{
    echo "=== Procedural Coherence Analysis ==="
    procedural_score=$(assess_procedural_coherence "$target_file")
    echo "Procedural Score: $procedural_score/100"
} &

{
    echo "=== Terminological Coherence Analysis ==="
    terminological_score=$(assess_terminological_coherence "$target_file")
    echo "Terminological Score: $terminological_score/100"
} &

wait # Wait for all parallel assessments to complete
```

### Phase 3: Weighted Score Calculation
```bash
# Calculate weighted coherence score
calculate_overall_coherence() {
    local structural=$1 semantic=$2 evidence=$3 procedural=$4 terminological=$5
    
    local weighted_score=$(echo "scale=2; \
        ($structural * 0.30) + \
        ($semantic * 0.25) + \
        ($evidence * 0.20) + \
        ($procedural * 0.15) + \
        ($terminological * 0.10)" | bc)
    
    echo $weighted_score
}

overall_score=$(calculate_overall_coherence $structural_score $semantic_score $evidence_score $procedural_score $terminological_score)
```

### Phase 4: Quality Gate Assessment
```bash
# Apply quality gates with clear thresholds
assess_quality_gates() {
    local score=$1
    
    if (( $(echo "$score >= 90" | bc -l) )); then
        echo "PASS - Framework coherence exceeds target threshold"
        echo "Status: PRODUCTION_READY"
        return 0
    elif (( $(echo "$score >= 75" | bc -l) )); then
        echo "WARNING - Framework coherence below optimal threshold"  
        echo "Status: IMPROVEMENT_RECOMMENDED"
        return 1
    else
        echo "BLOCK - Framework coherence requires significant improvement"
        echo "Status: MAJOR_REVISION_NEEDED"
        return 2
    fi
}
```

## Anti-Fiction Validation Integration

### Pre-Creation Validation
```yaml
numeric_claim_detection:
  percentage_patterns: '\d+%|\d+\.\d+%'
  performance_patterns: '≤\d+ms|≥\d+%|accuracy of \d+'
  effectiveness_patterns: 'achieving \d+%|providing \d+%'
  precision_patterns: '\d+\.\d+% effectiveness|±\d+\.\d+%'

evidence_requirements:
  source_format: 'Source: file_path:line_number'
  measurement_format: 'Measured via [specific methodology]'
  estimation_format: 'Estimated based on [analysis criteria]'
  assessment_format: 'Assessment based on [evaluation framework]'
```

### Alternative Recommendations
```yaml
qualitative_replacements:
  "93% effectiveness" → "high effectiveness"
  "≤4.2ms response time" → "fast response time"  
  "68% token reduction" → "significant token reduction"
  "99% accuracy" → "high accuracy"
  "achieving 85% coherence" → "achieving strong coherence"
  "providing 90% coverage" → "providing comprehensive coverage"
```

### Creation Gate Implementation
```bash
# Block content creation until evidence requirements met
validate_evidence_before_creation() {
    local content="$1"
    local unsourced_claims=$(echo "$content" | grep -E '\d+%|\d+\.\d+%|≤\d+|≥\d+' | wc -l)
    local evidence_statements=$(echo "$content" | grep -E 'Source:|Measured via|Estimated based on|Assessment based on' | wc -l)
    
    if [[ $unsourced_claims -gt $evidence_statements ]]; then
        echo "CREATION_BLOCKED: $((unsourced_claims - evidence_statements)) unsourced numeric claims detected"
        echo "Evidence required for all quantitative assertions"
        return 1
    fi
    
    return 0
}
```

## Integration with Framework Ecosystem

### Constitutional AI Integration
```yaml
constitutional_compliance:
  principle_1: "Helpfulness without deception - evidence-based claims only"
  principle_2: "Harmlessness through accuracy - no fabricated metrics"
  principle_3: "Honesty in assessment - transparent evaluation criteria"
  principle_4: "Clarity in communication - coherent structural organization"  
  principle_5: "Reliability through validation - systematic quality assurance"
```

### Self-Healing Protocol Integration
```markdown
## 🔧 FRAMEWORK COHERENCE ISSUES DETECTED

**Overall Coherence Score**: [score]/100 ([rating])
**Target Threshold**: 90/100 for production deployment
**Issues Found**: [count] coherence problems identified

**Dimension Breakdown**:
- Structural Coherence: [score]/100 (Weight: 30%)
- Semantic Coherence: [score]/100 (Weight: 25%) 
- Evidence Authenticity: [score]/100 (Weight: 20%)
- Procedural Coherence: [score]/100 (Weight: 15%)
- Terminological Coherence: [score]/100 (Weight: 10%)

**🔧 APPLYING COHERENCE CORRECTIONS**:
- Structural: [specific fixes for hierarchy and organization]
- Semantic: [specific fixes for concept consistency]
- Evidence: [specific fixes for unsourced claims]
- Procedural: [specific fixes for workflow alignment]
- Terminological: [specific fixes for vocabulary consistency]

**✅ VALIDATION**: Re-analyzing framework coherence post-correction...
```

## Task Tool Spawn Pattern

### Specialized Validation Tasks
```yaml
spawn_conditions:
  structural_issues_detected: "Task tool with framework structure analyst"
  semantic_conflicts_found: "Task tool with semantic coherence specialist" 
  evidence_gaps_identified: "Task tool with anti-fiction validation specialist"
  procedural_inconsistencies: "Task tool with workflow coherence analyst"
  terminological_conflicts: "Task tool with vocabulary consistency specialist"

spawn_format: |
  Use Task tool to spawn specialist for detailed [dimension] analysis:
  
  **Specialist Focus**: [structural/semantic/evidence/procedural/terminological] coherence
  **Target File**: [file_path]
  **Issues Found**: [specific issues list]
  **Tools Available**: Read, Grep, Glob
  **Expected Deliverable**: Detailed analysis with specific recommendations
  **Context Isolation**: Complete - no contamination of main validation workflow
```

## Output Format

### Comprehensive Assessment Report
```yaml
framework_coherence_assessment:
  metadata:
    target_file: "[absolute_file_path]"
    assessment_timestamp: "[ISO_timestamp]"
    validator_version: "framework-coherence-validator-1.0"
    execution_duration: "[actual_duration_ms]"
  
  dimension_scores:
    structural_coherence:
      score: 0  # 0-100
      weight: 30
      status: "PASS|FAIL"
      critical_issues: []
      recommendations: []
    
    semantic_coherence:
      score: 0  # 0-100
      weight: 25
      status: "PASS|FAIL" 
      critical_issues: []
      recommendations: []
    
    evidence_authenticity:
      score: 0  # 0-100
      weight: 20
      status: "PASS|FAIL"
      unsourced_claims: []
      evidence_gaps: []
      recommendations: []
    
    procedural_coherence:
      score: 0  # 0-100
      weight: 15
      status: "PASS|FAIL"
      workflow_issues: []
      recommendations: []
    
    terminological_coherence:
      score: 0  # 0-100
      weight: 10
      status: "PASS|FAIL"
      consistency_issues: []
      recommendations: []
  
  overall_assessment:
    weighted_coherence_score: 0  # calculated weighted average
    coherence_rating: "excellent|good|acceptable|needs_improvement|poor"
    production_readiness: "READY|NOT_READY|BLOCKED"
    quality_gate_status: "PASS|WARNING|BLOCK"
    
  validation_certification:
    framework_coherent: true/false
    evidence_based: true/false
    structurally_sound: true/false
    semantically_consistent: true/false
    procedurally_aligned: true/false
    terminologically_unified: true/false
    
  improvement_plan:
    high_priority_fixes: []
    medium_priority_enhancements: []
    low_priority_optimizations: []
    estimated_effort: "low|medium|high"
    
  integration_status:
    constitutional_compliance: "validated|needs_review|non_compliant"
    anti_fiction_compliance: "validated|evidence_gaps|fabricated_content"
    self_healing_ready: true/false
```

## Success Criteria

**Framework Coherence Achieved When**:
- ✅ Structural Coherence: ≥90% consistent architecture and logical organization
- ✅ Semantic Coherence: ≥90% concept consistency and logical flow
- ✅ Evidence Authenticity: ≥90% sourced claims with zero fabricated metrics  
- ✅ Procedural Coherence: ≥90% workflow alignment and step consistency
- ✅ Terminological Coherence: ≥90% unified vocabulary usage
- ✅ Overall Weighted Score: ≥90% for production deployment
- ✅ Creation-Time Validation: Zero fabricated metrics in new content
- ✅ Constitutional Compliance: Full adherence to 5-principle framework

**Performance Targets**:
- Assessment completion: ≤30 seconds for files up to 500 lines
- Issue detection accuracy: ≥95% precision in identifying coherence problems
- False positive rate: ≤5% for well-structured framework content
- Self-healing integration: 100% compatibility with correction protocols
- Evidence validation: 100% detection of unsourced quantitative claims

This validator provides comprehensive framework coherence assessment while preventing fabricated metrics through creation-time validation, ensuring both structural quality and content authenticity.
EOF < /dev/null