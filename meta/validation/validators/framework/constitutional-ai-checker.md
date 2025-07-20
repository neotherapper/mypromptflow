# Constitutional AI Compliance Checker

**Location**: meta/validators/constitutional-ai-checker.md  
**Purpose**: Systematic validation of AI agent instructions against constitutional AI principles  
**Compliance Threshold**: 95% minimum across all 5 constitutional principles  
**Integration**: Core component of validation framework and self-healing protocol  

## Constitutional AI Principles Framework

### Core Principles for AI Agent Instructions

#### 1. Accuracy Principle (95% confidence threshold)
**Requirement**: All claims supported by verifiable evidence  
**Application**: AI agent instructions must not contain fabricated metrics, false claims, or unsupported assertions  

```yaml
accuracy_validation:
  evidence_requirements:
    - verifiable_data_sources
    - documented_calculations  
    - measurement_methodologies
    - confidence_scoring_shown
  
  prohibited_patterns:
    - fabricated_performance_metrics
    - unsupported_timing_claims
    - fake_assessment_scores
    - made_up_statistics
  
  validation_threshold: 95 # percent confidence required
```

#### 2. Transparency Principle (100% auditability)
**Requirement**: Validation methods clearly documented and auditable  
**Application**: All assessment processes, methodologies, and decision criteria must be explicitly documented  

```yaml
transparency_validation:
  documentation_requirements:
    - methodology_explanation
    - decision_reasoning_shown
    - source_attribution_complete
    - audit_trail_maintained
  
  auditability_checklist:
    - assessment_tools_identified
    - scoring_formulas_documented
    - evidence_collection_process_shown
    - quality_gates_defined
  
  auditability_threshold: 100 # percent complete documentation
```

#### 3. Completeness Principle (85% coverage)
**Requirement**: Comprehensive coverage of all required aspects  
**Application**: Instructions must address all necessary components without gaps or omissions  

```yaml
completeness_validation:
  coverage_requirements:
    - stakeholder_consideration
    - implementation_guidance
    - error_handling_procedures
    - quality_validation_steps
  
  assessment_areas:
    - instruction_comprehensiveness
    - scenario_coverage
    - edge_case_handling
    - integration_completeness
  
  coverage_threshold: 85 # percent complete coverage
```

#### 4. Responsibility Principle (80% impact consideration)
**Requirement**: Consider implementation impacts and ethical implications  
**Application**: Instructions must consider broader impacts and responsible usage  

```yaml
responsibility_validation:
  impact_assessment:
    - user_experience_effects
    - system_performance_impacts
    - maintenance_requirements
    - scalability_considerations
  
  ethical_considerations:
    - bias_prevention_measures
    - fairness_in_application
    - inclusive_design_principles
    - harm_prevention_protocols
  
  assessment_threshold: 80 # percent impact consideration
```

#### 5. Integrity Principle (85% limitation acknowledgment)
**Requirement**: Acknowledge limitations, uncertainties, and potential biases  
**Application**: Honest reporting of capabilities, constraints, and measurement limitations  

```yaml
integrity_validation:
  limitation_acknowledgment:
    - measurement_capability_constraints
    - estimation_uncertainty_labeling
    - assumption_documentation
    - boundary_condition_identification
  
  honesty_requirements:
    - no_overstatement_of_capabilities
    - clear_uncertainty_communication
    - realistic_expectation_setting
    - constraint_transparency
  
  integrity_threshold: 85 # percent honest limitation acknowledgment
```

## Compliance Assessment Process

### Phase 1: Accuracy Principle Assessment

**Evidence Verification Checklist**:
- [ ] **Claims Have Sources**: All quantitative claims linked to evidence
- [ ] **Calculations Shown**: Mathematical formulas and processes documented
- [ ] **Measurement Basis**: Clear indication of how metrics were obtained
- [ ] **Confidence Levels**: Uncertainty and confidence explicitly stated
- [ ] **No Fabrication**: No made-up statistics or false performance claims

**Accuracy Scoring Formula**:
```yaml
accuracy_score_calculation:
  evidence_supported_claims: count(claims_with_evidence) / count(total_claims) * 40
  calculation_transparency: count(shown_calculations) / count(quantitative_claims) * 30
  measurement_honesty: count(honest_limitations) / count(measurement_claims) * 20
  confidence_clarity: count(explicit_confidence) / count(uncertain_claims) * 10
  total_accuracy_score: sum(above_components) # max 100
```

### Phase 2: Transparency Principle Assessment

**Documentation Completeness Checklist**:
- [ ] **Methodology Documented**: Assessment processes clearly explained
- [ ] **Decision Criteria**: Quality gates and thresholds explicitly defined
- [ ] **Tool Identification**: Specific assessment tools and frameworks referenced
- [ ] **Process Auditability**: Complete audit trail from input to conclusion
- [ ] **Source Attribution**: All references and influences properly cited

**Transparency Scoring Formula**:
```yaml
transparency_score_calculation:
  methodology_clarity: assessment(documentation_completeness) * 30
  decision_auditability: assessment(reasoning_transparency) * 25
  tool_identification: count(explicit_tools) / count(processes) * 25
  source_attribution: count(attributed_sources) / count(references) * 20
  total_transparency_score: sum(above_components) # max 100
```

### Phase 3: Completeness Principle Assessment

**Coverage Analysis Checklist**:
- [ ] **Stakeholder Consideration**: All affected parties identified and addressed
- [ ] **Scenario Coverage**: Main use cases and edge cases covered
- [ ] **Implementation Guidance**: Clear, actionable implementation steps
- [ ] **Error Handling**: Comprehensive error detection and recovery procedures
- [ ] **Quality Validation**: Systematic quality assurance processes included

**Completeness Scoring Formula**:
```yaml
completeness_score_calculation:
  stakeholder_coverage: assessment(stakeholder_identification) * 25
  scenario_comprehensiveness: assessment(use_case_coverage) * 25
  implementation_clarity: assessment(actionability) * 25
  error_handling_quality: assessment(error_procedures) * 25
  total_completeness_score: sum(above_components) # max 100
```

### Phase 4: Responsibility Principle Assessment  

**Impact Consideration Checklist**:
- [ ] **User Impact**: Effects on user experience and workflow considered
- [ ] **System Impact**: Performance and scalability implications addressed
- [ ] **Maintenance Impact**: Long-term maintenance and support requirements
- [ ] **Ethical Implications**: Bias prevention and fairness considerations
- [ ] **Societal Effects**: Broader implications and responsible usage guidelines

**Responsibility Scoring Formula**:
```yaml
responsibility_score_calculation:
  user_impact_consideration: assessment(user_experience_effects) * 25
  system_impact_analysis: assessment(performance_implications) * 25
  maintenance_planning: assessment(support_requirements) * 25
  ethical_consideration: assessment(bias_and_fairness) * 25
  total_responsibility_score: sum(above_components) # max 100
```

### Phase 5: Integrity Principle Assessment

**Honesty and Limitation Checklist**:
- [ ] **Capability Honesty**: No overstatement of system or process capabilities
- [ ] **Uncertainty Acknowledgment**: Clear labeling of estimates and unknowns
- [ ] **Limitation Documentation**: Explicit identification of constraints and boundaries
- [ ] **Assumption Transparency**: Underlying assumptions clearly stated
- [ ] **Bias Recognition**: Potential biases and limitations acknowledged

**Integrity Scoring Formula**:
```yaml
integrity_score_calculation:
  capability_honesty: assessment(realistic_claims) * 30
  uncertainty_clarity: count(labeled_estimates) / count(uncertain_items) * 25
  limitation_transparency: assessment(constraint_documentation) * 25
  assumption_clarity: assessment(assumption_documentation) * 20
  total_integrity_score: sum(above_components) # max 100
```

## Constitutional Compliance Scoring

### Overall Compliance Calculation
```yaml
overall_compliance_formula:
  weighted_principle_scores:
    accuracy_weight: 25 # percent of total score
    transparency_weight: 25 # percent of total score  
    completeness_weight: 20 # percent of total score
    responsibility_weight: 15 # percent of total score
    integrity_weight: 15 # percent of total score
  
  compliance_calculation:
    total_score: (accuracy * 0.25) + (transparency * 0.25) + (completeness * 0.20) + (responsibility * 0.15) + (integrity * 0.15)
    
  compliance_thresholds:
    production_ready: compliance_score >= 95
    development_acceptable: compliance_score >= 85
    improvement_required: compliance_score >= 75
    major_revision_needed: compliance_score < 75
```

## Integration with Self-Healing Protocol

### Constitutional Violation Detection
```markdown
## ⚖️ CONSTITUTIONAL AI VIOLATION DETECTED

**Principle Violated**: [accuracy|transparency|completeness|responsibility|integrity]
**Violation Severity**: [CRITICAL|HIGH|MEDIUM]
**Current Score**: [score]/100 (Threshold: [threshold])

**Specific Issues**:
- [Principle]: [specific_violation_description] (Line [number])
- [Requirement]: [missing_or_inadequate_element]

**🔧 APPLYING CONSTITUTIONAL CORRECTIONS**:
- Adding evidence basis for claim: "[claim]" → "[evidence_based_version]"
- Improving transparency: "[vague_process]" → "[documented_methodology]"  
- Acknowledging limitation: "[overstatement]" → "[honest_limitation]"

**✅ VALIDATION**: Re-assessing constitutional compliance post-correction...
```

### Quality Gates for Constitutional Compliance
```yaml
constitutional_quality_gates:
  gate_1_critical_violations:
    condition: "Any principle score < 70"
    action: "BLOCK - Critical constitutional violation requires immediate correction"
    message: "Constitutional AI compliance failure. Address critical violations before proceeding."
    
  gate_2_threshold_failures:
    condition: "Overall compliance score < 95"
    action: "WARNING - Constitutional compliance below threshold"
    message: "Constitutional AI compliance: [score]%. Improve to 95% for production deployment."
    
  gate_3_production_ready:
    condition: "Overall compliance score >= 95"
    action: "PASS - Constitutional AI compliance met"
    message: "Constitutional AI compliance: [score]%. Ready for production deployment."
```

## Assessment Automation Commands

### Systematic Constitutional Validation
```bash
# Check for accuracy principle violations (fabricated claims)
grep -n -E '\b\d{1,2}(?:\.\d)?%|\b\d+\/100\b|\b\d+\.\d+\s+minutes?\b' [target_file]

# Check for transparency principle violations (undocumented methodology)
grep -n -E '\b(assessment|evaluation|validation)\b' [target_file] | grep -v -E '\b(using|via|through|by)\b'

# Check for completeness principle violations (missing error handling)
grep -n -E '\b(error|failure|exception)\b' [target_file] | wc -l

# Check for responsibility principle violations (impact not considered)
grep -n -E '\b(user|system|performance|scalability|maintenance)\b' [target_file] | wc -l

# Check for integrity principle violations (overstatement)
grep -n -E '\b(guarantee|always|never|100%|perfect)\b' [target_file]
```

## Constitutional Compliance Report Template

```yaml
constitutional_compliance_report:
  assessment_metadata:
    target_file: "[file_path]"
    assessment_date: "[timestamp]"
    assessor: "[ai_agent_identifier]"
    assessment_duration: "[actual_time]"
  
  principle_scores:
    accuracy_principle:
      score: 0  # 0-100
      threshold: 95
      status: "PASS|FAIL"
      evidence: "[specific_evidence_of_compliance_or_violation]"
    
    transparency_principle:
      score: 0  # 0-100  
      threshold: 95
      status: "PASS|FAIL"
      evidence: "[specific_evidence_of_compliance_or_violation]"
    
    completeness_principle:
      score: 0  # 0-100
      threshold: 85
      status: "PASS|FAIL"
      evidence: "[specific_evidence_of_compliance_or_violation]"
    
    responsibility_principle:
      score: 0  # 0-100
      threshold: 80
      status: "PASS|FAIL"
      evidence: "[specific_evidence_of_compliance_or_violation]"
    
    integrity_principle:
      score: 0  # 0-100
      threshold: 85
      status: "PASS|FAIL"
      evidence: "[specific_evidence_of_compliance_or_violation]"
  
  overall_assessment:
    total_compliance_score: 0  # weighted average
    production_readiness: "READY|NOT_READY"
    critical_violations: []
    improvement_recommendations: []
    
  constitutional_certification:
    constitutional_ai_compliant: true/false
    compliance_confidence: 0  # 0-100
    assessment_quality: "high|medium|low"
```

## Success Criteria and Integration

**Constitutional AI Compliance Achieved When**:
- ✅ Accuracy Principle: ≥95% evidence-based claims
- ✅ Transparency Principle: ≥95% documented methodology
- ✅ Completeness Principle: ≥85% comprehensive coverage
- ✅ Responsibility Principle: ≥80% impact consideration
- ✅ Integrity Principle: ≥85% honest limitation acknowledgment
- ✅ Overall Compliance: ≥95% weighted score

**Integration Points**:
- Anti-fiction validation: `meta/validators/anti-fiction-validator.md`
- Vagueness detection: `meta/validators/vagueness-detector.md`
- Self-healing protocol: `meta/validation/self-healing-protocol.md`
- Validation framework command: `meta/validation/validation-framework-command.md`

**Performance Target**: 100% constitutional principle assessment with 95% accuracy in identifying compliance gaps and violations.