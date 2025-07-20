# Anti-Fiction Validation Protocol

**Location**: meta/validators/anti-fiction-validator.md  
**Purpose**: Prevent creation of fictional assessment reports and fabricated metrics in AI agent instructions  
**Input**: Target instruction or assessment file  
**Output**: Fiction detection report with evidence-based findings  
**Integration**: Core component of self-healing protocol for systematic correction  

## The Fiction Problem

### Common Fictional Patterns in AI Agent Instructions
1. **Fabricated Performance Metrics**: Creating fake percentages (e.g., "50-80% savings", "95% accuracy") without measurement
2. **Fictional Timing Estimates**: Providing specific timing (e.g., "30 seconds", "4.2 minutes") without actual measurement
3. **Mock Validation Results**: Creating fake assessment scores (e.g., "94/100", "3.5/5") without applying documented checklists
4. **Placeholder Statistics**: Using generic performance claims instead of measured data
5. **Estimated Results Presented as Facts**: Guessing outcomes and presenting them as measured findings

### Why Fiction Occurs in AI Instructions
- **Expectation Pressure**: Belief that instructions should include specific metrics
- **Time Pressure**: Assumption that detailed measurement "takes too long"
- **Result Anticipation**: Creating expected outcomes rather than measuring actual performance
- **Validation Skipping**: Bypassing systematic assessment and creating idealized results

## Fiction Detection Patterns

### 1. Fabricated Performance Metrics Detection

**High-Risk Patterns**:
```regex
Fabricated_Efficiency_Claims:
  - \b\d{1,2}(?:\.\d)?[-–]?\d{1,2}%\s*(savings?|efficiency|improvement|reduction)\b
  - \b(achieves?|provides?|delivers?)\s+\d{1,2}(?:\.\d)?%\b
  - \b(token|memory|resource)\s+(efficiency|optimization):\s*\d{1,2}(?:\.\d)?%\b

Fabricated_Accuracy_Claims:
  - \b\d{1,2}(?:\.\d)?%\s*(accuracy|precision|success\s+rate)\b
  - \b(detection|validation|compliance):\s*\d{1,2}(?:\.\d)?%\b
  - \b\d{1,2}\/100\s*(score|rating|assessment)\b

Fabricated_Time_Claims:
  - \b\d{1,2}\s*(seconds?|minutes?|hours?)\s+(execution|completion|processing)\b
  - \b(phase|step)\s+\d+.*?\(\s*\d{1,2}\s*(seconds?|minutes?)\s*\)\b
  - \btotal.*?time:\s*\d+[\.:]\d+\b
```

**Evidence Requirements for Legitimate Metrics**:
```yaml
legitimate_metrics_must_have:
  measurement_basis:
    - "Source: [specific measurement method]"
    - "Measured using: [tool/process]"
    - "Based on: [actual data collection]"
  
  estimation_labeling:
    - "Estimated based on [methodology]"
    - "Projected using [calculation method]"
    - "Unknown - no measurement available"
  
  evidence_documentation:
    - Specific measurement timestamps
    - Data collection methodology
    - Calculation formulas shown
    - Source data referenced
```

### 2. Fiction vs. Legitimate Content Classification

**FICTION (Must be corrected)**:
```yaml
fabricated_examples:
  timing: "Phase 1: Discovery (30 seconds)"
  efficiency: "Token efficiency: 50-80% savings"
  performance: "Achieves 95% accuracy rate"
  execution: "Total execution time: 4.2 minutes"
  assessment: "Quality score: 94/100"
  
correction_approach: "Remove or replace with honest estimates"
```

**LEGITIMATE (Acceptable)**:
```yaml
honest_examples:
  estimation: "Estimated time: 2-5 minutes depending on complexity"
  measurement: "File count: 300 files (measured using git diff | wc -l)"
  unknown: "Execution time: Not measured (timing capability unavailable)"
  qualified: "Efficiency: Likely improved through conditional loading"
  evidence_based: "Assessment: 87/100 (using documented framework scoring)"
  
acceptance_criteria: "Evidence basis or honest uncertainty acknowledged"
```

## Mandatory Fiction Prevention Protocol

### Phase 1: Pre-Creation Validation
**Before creating any instruction or assessment, verify**:
- [ ] **Measurement Capability Confirmed**: Can actual measurement be performed?
- [ ] **Evidence Sources Identified**: Are data sources available and accessible?
- [ ] **Timing Constraints Realistic**: Is actual timing measurement feasible?
- [ ] **Assessment Tools Ready**: Are documented scoring methods available?

### Phase 2: During Creation Validation
**While writing instructions or assessments, ensure**:
- [ ] **Claims Have Evidence**: Each quantitative claim linked to evidence source
- [ ] **Estimates Clearly Labeled**: All estimates marked as "estimated", "projected", or "unknown"
- [ ] **Timing Claims Verified**: Only include timing if actually measured
- [ ] **No Placeholder Statistics**: Avoid generic performance percentages

### Phase 3: Post-Creation Validation
**Before deploying instructions or assessments, verify**:
- [ ] **Fiction Detection Run**: Apply systematic fiction detection patterns
- [ ] **Evidence Verification**: Confirm all claims have evidence basis
- [ ] **Estimation Labeling**: Verify estimates are clearly marked
- [ ] **Reality Check**: Do claims reflect actual capability rather than idealized targets?

## Fiction Detection Automation

### Automated Fiction Scanning Commands

**For AI Agents to Run Systematic Detection**:
```bash
# Scan for fabricated efficiency claims
grep -n -E '\b\d{1,2}(?:\.\d)?[-–]?\d{1,2}%\s*(savings?|efficiency|improvement|reduction)\b' [target_file]

# Scan for fabricated timing claims  
grep -n -E '\b\d{1,2}\s*(seconds?|minutes?|hours?)\s+(execution|completion|processing)\b' [target_file]

# Scan for fabricated accuracy claims
grep -n -E '\b\d{1,2}(?:\.\d)?%\s*(accuracy|precision|success\s+rate)\b' [target_file]

# Scan for fabricated assessment scores
grep -n -E '\b\d{1,2}\/100\s*(score|rating|assessment)\b' [target_file]

# Scan for specific fabricated patterns from validate-pr issues
grep -n -E '\b(30|60|90)\s+seconds?\b|\b4\.2\s+minutes?\b|\b50-80%\s+savings?\b' [target_file]
```

### Fiction Severity Classification

```yaml
severity_levels:
  critical_fiction:
    - Specific false timing claims (e.g., "4.2 minutes")
    - Exact false efficiency percentages (e.g., "50-80% savings")
    - Fabricated assessment scores without methodology
    - Made-up performance statistics
    action: "Immediate removal required"
    
  high_fiction:
    - Generic efficiency claims without evidence
    - Timing estimates presented as facts
    - Performance claims without measurement basis
    - Success rates without data collection
    action: "Replace with honest estimates or remove"
    
  medium_fiction:
    - Unlabeled estimates presented as facts
    - Generic performance expectations
    - Assumed timing without qualification
    - Implicit accuracy claims
    action: "Add estimation labels or evidence requirements"
```

## Fiction Correction Templates

### Fabricated Metrics Correction
```yaml
correction_patterns:
  before: "Token efficiency: 50-80% savings"
  after: "Token efficiency: Estimated reduction through conditional loading (actual savings depend on content complexity)"
  
  before: "Phase 1: Discovery (30 seconds)"
  after: "Phase 1: Discovery"
  
  before: "Total execution time: 4.2 minutes"
  after: "Total execution time: Process completed (timing not measured)"
  
  before: "Achieves 95% accuracy rate"
  after: "Designed for high accuracy (measurement pending actual deployment)"
  
  before: "Quality score: 94/100"
  after: "Quality assessment: [specific score] using [documented methodology]"
```

### Evidence-Based Alternatives
```yaml
evidence_based_patterns:
  measurement_available:
    pattern: "File count: 300 files (confirmed using: git diff --name-only origin/master HEAD | wc -l)"
    evidence: "Specific command and actual result shown"
    
  calculation_available:
    pattern: "Vagueness density: 2.13% (calculated: 34 points ÷ 1596 words × 100)"
    evidence: "Formula and actual numbers provided"
    
  estimation_honest:
    pattern: "Estimated improvement: 20-40% based on conditional loading analysis"
    evidence: "Clearly labeled as estimate with reasoning provided"
    
  unknown_acknowledged:
    pattern: "Execution time: Unknown (timing measurement not available)"
    evidence: "Limitation honestly acknowledged"
```

## Integration with Self-Healing Protocol

### Fiction Detection Alert Format
```markdown
## 🚨 FICTION DETECTED - ANTI-FICTION PROTOCOL ACTIVATED

**Fiction Type**: [fabricated_metrics|false_timing|fake_assessments]
**Severity**: [CRITICAL|HIGH|MEDIUM]
**Instances Found**: [count] fiction patterns detected

**Specific Issues**:
- Line [number]: "[exact_text]" - [fiction_type] without evidence basis
- Line [number]: "[exact_text]" - [fiction_type] requires measurement or labeling

**🔧 APPLYING CORRECTIONS**:
- Removing fabricated claim: "[original]" → "[corrected]"
- Adding estimation label: "[original]" → "[corrected_with_label]"
- Replacing with evidence: "[original]" → "[evidence_based_alternative]"

**✅ VALIDATION**: Re-scanning for fiction patterns post-correction...
```

### Quality Gates for Fiction Prevention

```yaml
quality_gates:
  gate_1_critical_fiction:
    condition: "Critical fiction patterns detected"
    action: "BLOCK - Immediate correction required before proceeding"
    message: "Critical fiction detected. Remove fabricated metrics before validation."
    
  gate_2_high_fiction:
    condition: "High fiction patterns detected"
    action: "WARNING - Evidence or labeling required"
    message: "High fiction level. Add evidence basis or estimation labels."
    
  gate_3_acceptable:
    condition: "No fiction patterns detected"
    action: "PASS - Fiction prevention standards met"
    message: "Anti-fiction validation passed. Proceeding with assessment."
```

## Validation Checkpoints

### Checkpoint 1: Evidence Verification
```yaml
verification_questions:
  measurement_capability: "Can this metric actually be measured with available tools?"
  evidence_existence: "Is there actual data supporting this claim?"
  calculation_shown: "If calculated, is the formula and process documented?"
  source_identified: "Is the source of this information clearly specified?"

red_flags:
  - Round numbers without measurement (50%, 95%, etc.)
  - Specific timing without actual timing measurement
  - Performance claims without benchmarking
  - Assessment scores without documented methodology
```

### Checkpoint 2: Honest Reporting Verification
```yaml
honesty_requirements:
  estimates_labeled: "All estimates clearly marked as 'estimated', 'projected', or 'unknown'"
  limitations_acknowledged: "Measurement limitations honestly stated"
  uncertainty_expressed: "Uncertainty indicated where appropriate"
  evidence_provided: "Evidence basis documented for all factual claims"

validation_evidence:
  - No fabricated performance percentages
  - No fake timing specifications
  - No made-up assessment scores
  - All claims either evidenced or labeled as estimates
```

## Success Criteria

**Anti-Fiction Validation Passes When**:
- ✅ No fabricated performance metrics detected
- ✅ No false timing claims present
- ✅ No fake assessment scores included
- ✅ All estimates clearly labeled as such
- ✅ Evidence basis provided for factual claims
- ✅ Limitations and uncertainties acknowledged
- ✅ Measurement capabilities honestly represented

**Integration Points**:
- Self-healing error detection patterns: `meta/validation/self-healing-error-detection-patterns.md`
- Vagueness detection: `meta/validators/vagueness-detector.md`
- Constitutional AI compliance: `meta/validators/constitutional-ai-checker.md`
- Framework validation command: `meta/validation/validation-framework-command.md`

**Performance Target**: 100% detection of fabricated metrics with 95% accuracy in distinguishing fiction from legitimate estimates.