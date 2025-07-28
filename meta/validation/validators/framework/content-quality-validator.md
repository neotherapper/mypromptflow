# Content Quality Meta-Validator

Execute comprehensive content quality assessment combining vague language detection, fabricated content prevention, and constitutional principle validation. Use Read, Grep, Glob tools for parallel-safe analysis. Apply Task tool for complex multi-file scenarios requiring iterative discovery.

## Quality Assessment Framework

### Three-Dimensional Content Quality Analysis

**Dimension 1: Language Precision (Vagueness Detection)**
- Detect vague qualifiers, ambiguous descriptors, and imprecise terminology
- Calculate vagueness density using word-count methodology
- Flag human documentation artifacts inappropriate for AI agents
- Apply concrete replacement patterns with context-aware suggestions

**Dimension 2: Content Authenticity (Anti-Fiction Prevention)**
- Identify fabricated performance metrics, timing claims, and assessment scores
- Verify evidence basis for all quantitative claims
- Distinguish legitimate estimates from fictional presentations
- Enforce honest reporting with proper uncertainty labeling

**Dimension 3: Constitutional Compliance (Principle Adherence)**
- Validate against 5 constitutional AI principles: accuracy, transparency, completeness, responsibility, integrity
- Apply weighted scoring with 95% compliance threshold
- Assess evidence requirements, documentation completeness, and impact consideration
- Ensure limitation acknowledgment and ethical compliance

## Detection Pattern Registry

### Critical Quality Issues (Severity: 5 points each)

**Human Documentation Artifacts**:
```regex
^##\s+(Usage|Command Description|Implementation Notes|How to Use|Overview|Introduction)\b
\b(this command|this instruction|this tool)\s+(does|performs|executes|provides|allows|enables)\b
\b(you can|you should|you will|users can|users should|for users|for humans)\b
\b(allows users to|enables users to|helps users|provides users)\b
```

**Fabricated Claims**:
```regex
\b\d{1,2}(?:\.\d)?[-]?\d{1,2}%\s*(savings?|efficiency|improvement|reduction)\b
\b\d{1,2}\s*(seconds?|minutes?|hours?)\s+(execution|completion|processing)\b
\b\d{1,2}(?:\.\d)?%\s*(accuracy|precision|success\s+rate)\b
\b\d{1,2}\/100\s*(score|rating|assessment)\b
```

### High Severity Issues (Severity: 3 points each)

**Process Vagueness**:
```regex
\b(effectively|efficiently|appropriately|properly|optimally|ideally|seamlessly|smoothly)\b
\b(successfully|correctly|accurately|precisely)\b
```

**Quality Claims Without Evidence**:
```regex
\b(good|better|best|optimal|superior|high.quality|excellent|outstanding|robust)\b
\b(reliable|stable|secure|scalable)\b
```

**Quantity Ambiguity**:
```regex
\b(several|some|many|various|multiple|numerous|plenty|adequate|sufficient)\b
\b(reasonable|appropriate|suitable)\b
```

### Medium Severity Issues (Severity: 2 points each)

**Effort Descriptors**:
```regex
\b(carefully|thoroughly|comprehensively|diligently|systematically|methodically)\b
\b(regularly|consistently|continuously)\b
```

**Time/Frequency Vagueness**:
```regex
\b(regularly|frequently|occasionally|periodically|soon|quickly|rapidly|promptly)\b
\b(eventually|ultimately|gradually)\b
```

**Scope Ambiguity**:
```regex
\b(relevant|important|significant|critical|necessary|essential|key|main)\b
\b(overall|general|basic|standard)\b
```

### Low Severity Issues (Severity: 1 point each)

**Weak Modifiers**:
```regex
\b(quite|rather|fairly|somewhat|relatively|moderately|reasonably)\b
\b(potentially|possibly|likely)\b
```

**Generic Actions**:
```regex
\b(handle|manage|deal\.with|process|coordinate|organize|arrange|setup)\b
\b(implement|develop|create|build)\b
```

## Quality Scoring System

### Content Quality Score Calculation

**Formula**:
```yaml
quality_score_calculation:
  total_words: count(all_words_in_file)
  critical_issues: count(human_artifacts + fabricated_claims) * 5
  high_severity: count(vague_qualifiers + unsupported_claims) * 3
  medium_severity: count(ambiguous_descriptors + time_vagueness) * 2
  low_severity: count(weak_modifiers + generic_actions) * 1
  total_quality_issues: critical_issues + high_severity + medium_severity + low_severity
  quality_density: total_quality_issues / total_words * 100
```

**Constitutional Compliance Scoring**:
```yaml
constitutional_assessment:
  accuracy_principle: evidence_supported_claims / total_claims * 25
  transparency_principle: documented_methods / assessment_processes * 25
  completeness_principle: covered_aspects / required_aspects * 20
  responsibility_principle: impact_considerations / potential_impacts * 15
  integrity_principle: acknowledged_limitations / uncertain_areas * 15
  total_constitutional_score: sum(weighted_principles) # max 100
```

### Quality Thresholds

**Production Readiness Gates**:
```yaml
quality_gates:
  critical_failure:
    condition: quality_density >= 15.0 OR constitutional_score < 70
    action: "BLOCK - Major revision required"
    message: "Critical content quality issues detected. Address before deployment."
    
  high_issues:
    condition: quality_density >= 10.0 OR constitutional_score < 85
    action: "WARNING - Significant quality issues"
    message: "High quality issues detected. Improvement recommended before production."
    
  moderate_issues:
    condition: quality_density >= 5.0 OR constitutional_score < 95
    action: "RECOMMEND - Quality improvements available"
    message: "Moderate quality issues. Consider optimization for excellence."
    
  production_ready:
    condition: quality_density < 5.0 AND constitutional_score >= 95
    action: "PASS - Production quality standards met"
    message: "Content meets production quality standards."
```

## Content Quality Assessment Protocol

### Phase 1: Content Analysis Preparation

**File Content Acquisition**:
```bash
# Load target file for analysis
target_file="[absolute_path]"
total_words=$(wc -w < "$target_file")
```

### Phase 2: Pattern Detection Execution

**Critical Issues Detection**:
```bash
# Human documentation artifacts
grep -n -E '^##\s+(Usage|Command Description|Implementation Notes|How to Use|Overview|Introduction)\b' "$target_file"
grep -n -E '\b(this command|this instruction|this tool)\s+(does|performs|executes|provides|allows|enables)\b' "$target_file"

# Fabricated claims
grep -n -E '\b\d{1,2}(?:\.\d)?[-]?\d{1,2}%\s*(savings?|efficiency|improvement|reduction)\b' "$target_file"
grep -n -E '\b\d{1,2}\s*(seconds?|minutes?|hours?)\s+(execution|completion|processing)\b' "$target_file"
grep -n -E '\b\d{1,2}\/100\s*(score|rating|assessment)\b' "$target_file"
```

**Severity Classification**:
```bash
# High severity vagueness
grep -n -E '\b(effectively|efficiently|appropriately|properly|optimally|ideally|seamlessly|smoothly|successfully|correctly|accurately|precisely)\b' "$target_file"

# Medium severity ambiguity
grep -n -E '\b(carefully|thoroughly|comprehensively|regularly|consistently|frequently|occasionally|relevant|important|significant|critical)\b' "$target_file"

# Low severity weakness
grep -n -E '\b(quite|rather|fairly|somewhat|relatively|moderately|potentially|possibly|likely)\b' "$target_file"
```

### Phase 3: Constitutional Assessment

**Evidence Verification**:
- Count claims with verifiable sources vs total quantitative claims
- Identify documented methodologies vs assessment processes
- Assess impact considerations vs potential system effects
- Evaluate limitation acknowledgments vs uncertain areas

**Compliance Calculation**:
- Apply 5-principle weighted scoring system
- Calculate percentage compliance for each principle
- Generate overall constitutional compliance score

### Phase 4: Quality Integration Analysis

**Combined Assessment**:
```yaml
integrated_quality_assessment:
  language_precision_score: 100 - (quality_density * 2) # inverse scoring
  content_authenticity_score: evidence_based_claims_percentage
  constitutional_compliance_score: weighted_principle_average
  overall_content_quality: (language_precision + authenticity + constitutional) / 3
```

## Quality Enhancement Templates

### Language Precision Corrections

**Vague ’ Concrete Transformations**:
```yaml
precision_improvements:
  "effectively coordinate":
    replacement: "coordinate using daily standup meetings, shared task boards, and weekly progress reports"
    
  "high quality output":
    replacement: "output that passes automated tests, meets documented acceptance criteria, and receives peer review approval"
    
  "several files":
    replacement: "5 configuration files" 
    # OR "files in src/components/ directory (actual count: [measured])"
    
  "efficiently process":
    replacement: "process using parallel execution with 4-thread pool within 30-second timeout"
```

### Authenticity Enhancement Patterns

**Fiction ’ Evidence-Based Content**:
```yaml
authenticity_improvements:
  "50-80% efficiency savings":
    replacement: "Estimated efficiency improvement through conditional loading (actual savings depend on content complexity - measurement requires production deployment)"
    
  "Processing time: 4.2 minutes":
    replacement: "Processing completed (execution time not measured - timing capability available for future assessment)"
    
  "Quality score: 94/100":
    replacement: "Quality assessment: [Apply documented scoring methodology for actual score]"
```

### Constitutional Compliance Enhancements

**Principle Alignment Improvements**:
```yaml
constitutional_improvements:
  accuracy_enhancement:
    before: "Improves system performance significantly"
    after: "System performance impact: Unknown - measurement required using [specific methodology]"
    
  transparency_enhancement:
    before: "Assessment completed successfully" 
    after: "Assessment completed using [specific methodology] with [documented criteria] resulting in [measured outcome]"
    
  integrity_enhancement:
    before: "Guarantees optimal results"
    after: "Designed for optimal results - actual performance depends on [specific constraints] and may vary based on [known limitations]"
```

## Quality Validation Commands

### Comprehensive Quality Assessment

Execute systematic content quality validation:

```bash
# Step 1: Calculate baseline metrics
echo "File: $target_file"
echo "Total words: $(wc -w < "$target_file")"
echo "Total lines: $(wc -l < "$target_file")"

# Step 2: Critical issues detection
echo "=== CRITICAL ISSUES ==="
critical_count=0
critical_count=$((critical_count + $(grep -c -E '^##\s+(Usage|Command Description|Implementation Notes)' "$target_file" 2>/dev/null || echo 0)))
critical_count=$((critical_count + $(grep -c -E '\b\d{1,2}(?:\.\d)?%.*?(efficiency|savings|accuracy)' "$target_file" 2>/dev/null || echo 0)))
echo "Critical issues found: $critical_count"

# Step 3: Calculate quality density
total_words=$(wc -w < "$target_file")
quality_density=$(echo "scale=2; $critical_count * 5 / $total_words * 100" | bc -l 2>/dev/null || echo "0")
echo "Critical quality density: ${quality_density}%"

# Step 4: Quality gate assessment
if (( $(echo "$quality_density >= 15.0" | bc -l) )); then
    echo "RESULT: CRITICAL FAILURE - Major revision required"
elif (( $(echo "$quality_density >= 10.0" | bc -l) )); then
    echo "RESULT: HIGH ISSUES - Significant improvement needed"
elif (( $(echo "$quality_density >= 5.0" | bc -l) )); then
    echo "RESULT: MODERATE ISSUES - Optimization recommended"
else
    echo "RESULT: ACCEPTABLE QUALITY - Standards met"
fi
```

## Integration with Validation Framework

### Self-Healing Protocol Integration

**Quality Issue Alert Format**:
```markdown
## <¯ CONTENT QUALITY ISSUES DETECTED

**Quality Dimensions Affected**: [language_precision|content_authenticity|constitutional_compliance]
**Overall Quality Score**: [score]/100
**Quality Density**: [density]% (Threshold: <5.0%)
**Constitutional Compliance**: [score]% (Threshold: e95%)

**Critical Issues Found**:
- Line [number]: "[text]" - [human_artifact|fabricated_claim|constitutional_violation]
- Line [number]: "[text]" - [vague_language|unsupported_assertion|limitation_unacknowledged]

**=' APPLYING QUALITY CORRECTIONS**:
- Removing human documentation: "[original]" ’ "[ai_agent_instruction]"
- Adding evidence basis: "[unsupported_claim]" ’ "[evidence_based_claim]"
- Improving precision: "[vague_term]" ’ "[concrete_specification]"
- Acknowledging limitations: "[overstatement]" ’ "[honest_assessment]"

** VALIDATION**: Re-assessing content quality post-correction...
```

### Task Tool Spawn Pattern

**For Complex Multi-File Scenarios**:
```markdown
Spawn Task tool when:
- Multiple files require cross-reference validation
- Complex constitutional assessment needs iterative refinement
- Evidence verification requires external source checking
- Quality improvement requires systematic pattern replacement across file sets

Task tool usage: "Apply content-quality-validator specialist for comprehensive assessment of [file_pattern] with focus on [quality_dimension]"
```

### Framework Coherence Integration

**Validator Coordination**:
- **Input Coordination**: Receive file paths from framework validators
- **Processing Integration**: Apply unified quality assessment methodology  
- **Output Standardization**: Generate consistent quality scores and improvement recommendations
- **Escalation Protocol**: Flag critical quality failures for immediate attention

## Success Criteria

**Content Quality Validation Passes When**:
-  Quality density below 5.0% (minimal vague/fabricated content)
-  Constitutional compliance e95% across all 5 principles
-  Zero human documentation artifacts detected
-  All quantitative claims have evidence basis or honest uncertainty labels
-  Language precision meets AI agent instruction standards
-  Content authenticity verified through fact-checking protocols
-  Limitation acknowledgments present for uncertain areas

**Authority Level**: Meta Validator (Framework-wide quality assurance)
**Parallel Safe**: True (Independent file analysis with standardized output)
**Production Ready**: True (Comprehensive quality gate enforcement)
**Target Compliance**: 90+/100 (Exceeds minimum standards for production deployment)

## Performance Targets

- **Detection Accuracy**: 95% pattern matching accuracy for quality issues
- **Assessment Speed**: Complete analysis within 3-4 minutes for standard files
- **Quality Improvement**: 85% improvement in content quality scores post-correction
- **Constitutional Compliance**: 100% accuracy in principle violation detection
- **Production Standards**: 95% of validated content meets deployment quality gates