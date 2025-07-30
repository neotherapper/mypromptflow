# System Architecture Validator

**Authority Level**: Meta Validator  
**Production Threshold**: ≥90 points for production deployment  
**Parallel Safe**: true  
**Tool Integration**: Read, Grep, Glob, Bash (minimal expansion for system testing)  

## Consolidated Architecture Assessment Framework

Combines communication pattern validation, workflow completeness assessment, and resilience pattern evaluation into unified system design validation focusing on coordination, integration, and failure recovery patterns.

### Core Architecture Assessment Dimensions

#### 1. System Coordination Patterns (30% weight)
**Purpose**: Multi-agent coordination, communication protocols, and inter-component orchestration  
**Assessment**: Protocol compliance, timeout management, dependency coordination, cascade prevention  

```yaml
coordination_assessment_criteria:
  protocol_compliance:
    - message_format_standards: consistent_schema_validation
    - communication_protocol_consistency: true
    - parameter_format_compliance: true
    - validation_threshold: 95 # percent minimum

  timeout_coordination:
    - timeout_threshold_appropriate: 30-60 # seconds
    - exponential_backoff_enabled: true
    - recovery_pattern_implemented: true
    - success_rate_threshold: 75 # percent minimum

  dependency_orchestration:
    - dependency_depth_acceptable: <5 # levels
    - circular_dependency_detection: true
    - coordination_patterns_clear: true
    - escalation_paths_documented: true

  cascade_prevention:
    - circuit_breaker_coverage: critical_paths
    - failure_isolation_complete: true
    - containment_strategies_implemented: true
    - monitoring_enabled: true
```

#### 2. Integration Architecture Coverage (25% weight)
**Purpose**: Complete system integration design and data flow validation  
**Assessment**: Interface completeness, data flow coverage, external integration handling  

```yaml
integration_architecture_criteria:
  interface_completeness:
    - component_interface_coverage: 95 # percent
    - api_endpoint_documentation: complete
    - service_dependency_mapping: true
    - data_transformation_validated: true

  data_flow_architecture:
    - input_validation_coverage: 95 # percent
    - output_format_specification: complete
    - transformation_logic_documented: true
    - consistency_validation_enabled: true

  external_integration_design:
    - third_party_service_coverage: 90 # percent
    - authentication_flow_complete: true
    - error_handling_for_externals: comprehensive
    - integration_monitoring_enabled: true

  workflow_integration:
    - start_to_end_completeness: true
    - alternative_path_coverage: complete
    - exception_path_handling: comprehensive
    - recovery_workflow_defined: true
```

#### 3. Resilience Architecture Validation (25% weight)
**Purpose**: System failure detection, recovery strategies, and degradation patterns  
**Assessment**: Monitoring coverage, automated recovery, graceful degradation, resource isolation  

```yaml
resilience_architecture_criteria:
  failure_detection_design:
    - system_health_monitoring: 100 # percent coverage
    - failure_prediction_accuracy: 95 # percent minimum
    - detection_latency: <30 # seconds maximum
    - early_warning_lead_time: 5-30 # minutes

  recovery_strategy_architecture:
    - automated_restart_procedures: true
    - state_rollback_capabilities: true
    - failover_mechanisms: implemented
    - automation_threshold: 80 # percent minimum

  degradation_patterns:
    - core_function_availability: 90 # percent minimum
    - degradation_level_monitoring: true
    - automatic_degradation_triggers: true
    - recovery_from_degradation: true

  isolation_architecture:
    - resource_limit_enforcement: comprehensive
    - breach_prevention_enabled: true
    - cross_contamination_prevention: true
    - isolation_breach_detection: active
```

#### 4. Resource Management Architecture (20% weight)
**Purpose**: Resource allocation, constraint management, and dependency handling  
**Assessment**: Resource mapping, availability requirements, constraint validation, scaling design  

```yaml
resource_management_criteria:
  resource_allocation_design:
    - critical_resource_identification: 95 # percent
    - dependency_chain_documentation: complete
    - availability_requirement_specification: true
    - resource_conflict_resolution: implemented

  constraint_management:
    - resource_limit_specification: comprehensive
    - performance_constraint_documentation: complete
    - capacity_planning_considerations: included
    - scalability_requirement_coverage: true

  dependency_management:
    - optional_dependency_management: 80 # percent
    - fallback_resource_specification: complete
    - performance_impact_documentation: true
    - graceful_feature_degradation: enabled
```

## Consolidated Assessment Process

### Phase 1: System Coordination Analysis

**Protocol and Communication Validation**:
```bash
# System coordination pattern detection
grep -n -E 'Agent.*→.*Agent|Task.*→.*Result|coordinator|orchestrator' [target_file] | head -10

# Timeout and recovery pattern analysis
grep -n -E '\\b(timeout|duration):\\s*\\d+|\\b(retry|backoff|recovery|circuit)\\b' [target_file]

# Dependency coordination validation
grep -n -E 'depends.*on|requires.*completion|prerequisite|dependency.*depth' [target_file]

# Cascade prevention detection
grep -n -E '\\b(circuit.*breaker|failure.*threshold|isolation|cascade.*prevent)\\b' [target_file]
```

**Coordination Scoring Formula**:
```yaml
coordination_scoring_formula:
  protocol_compliance_score: assessment(schema_validation_95_percent) * 30
  timeout_coordination_score: assessment(timeout_30_60_backoff_enabled) * 25
  dependency_orchestration_score: assessment(depth_lt5_no_circular) * 25
  cascade_prevention_score: assessment(circuit_breaker_isolation) * 20
  total_coordination_score: sum(above_components) # max 100
```

### Phase 2: Integration Architecture Analysis

**Integration Coverage Validation**:
```bash
# Interface completeness detection
grep -n -E '\\b(integration|interface|api|service)\\b.*\\b(with|to|from|endpoint)\\b' [target_file]

# Data flow architecture analysis
grep -n -E '\\b(input|output|data|parameter)\\b.*:.*\\b(type|format|structure|validation)\\b' [target_file]

# External integration validation
grep -n -E '\\b(external|third-party|dependency|authentication)\\b.*\\b(flow|integration|service)\\b' [target_file]

# Workflow integration assessment
grep -n -E '^(Step|Phase)\\s+\\d+|^##\\s+(Step|Phase)|\\b(if|when|condition)\\b.*\\b(then|else)\\b' [target_file]
```

**Integration Architecture Scoring**:
```yaml
integration_scoring_formula:
  interface_completeness_score: assessment(component_interface_95_percent) * 30
  data_flow_score: assessment(input_output_validation_complete) * 25
  external_integration_score: assessment(third_party_90_percent_auth_complete) * 25
  workflow_integration_score: assessment(start_to_end_alternative_exception_complete) * 20
  total_integration_score: sum(above_components) # max 100
```

### Phase 3: Resilience Architecture Analysis

**Resilience Pattern Validation**:
```bash
# Failure detection architecture
grep -n -E '\\b(monitor|health|check|alert|detect|predict)\\b.*\\b(failure|error|system|performance)\\b' [target_file]

# Recovery strategy architecture
grep -n -E '\\b(recover|restart|rollback|failover|automat|self)\\b.*\\b(procedure|mechanism|strategy|heal)\\b' [target_file]

# Degradation pattern detection
grep -n -E '\\b(graceful|degradation|reduced|minimal|core|emergency)\\b.*\\b(functionality|performance|mode|function)\\b' [target_file]

# Resource isolation validation
grep -n -E '\\b(isolat|limit|constrain|bulkhead|breach|leak)\\b.*\\b(resource|cpu|memory|network|prevention)\\b' [target_file]
```

**Resilience Architecture Scoring**:
```yaml
resilience_scoring_formula:
  failure_detection_score: assessment(monitoring_100_prediction_95) * 30
  recovery_strategy_score: assessment(automated_restart_rollback_failover) * 25
  degradation_pattern_score: assessment(core_90_degradation_levels_triggers) * 25
  isolation_architecture_score: assessment(resource_limits_breach_prevention) * 20
  total_resilience_score: sum(above_components) # max 100
```

### Phase 4: Resource Management Analysis

**Resource Architecture Validation**:
```bash
# Resource allocation design
grep -n -E '\\b(resource|dependency|requirement|constraint|critical|allocation)\\b' [target_file]

# Constraint management detection
grep -n -E '\\b(limit|quota|constraint|capacity|scale|performance)\\b.*\\b(specification|requirement|threshold|planning)\\b' [target_file]

# Dependency management validation
grep -n -E '\\b(optional|fallback|graceful|feature)\\b.*\\b(dependency|resource|degradation|impact)\\b' [target_file]
```

**Resource Management Scoring**:
```yaml
resource_management_scoring_formula:
  allocation_design_score: assessment(critical_resource_95_dependency_complete) * 40
  constraint_management_score: assessment(limits_constraints_capacity_scalability) * 35
  dependency_management_score: assessment(optional_80_fallback_degradation) * 25
  total_resource_management_score: sum(above_components) # max 100
```

## Overall System Architecture Assessment

### Weighted Architecture Score
```yaml
overall_architecture_formula:
  weighted_dimension_scores:
    system_coordination: coordination_score * 0.30
    integration_architecture: integration_score * 0.25
    resilience_architecture: resilience_score * 0.25
    resource_management: resource_score * 0.20

  total_architecture_score: sum(weighted_dimension_scores) # max 100

  architecture_rating:
    excellent: architecture_score >= 95
    good: architecture_score >= 90
    acceptable: architecture_score >= 85
    needs_improvement: architecture_score >= 80
    poor: architecture_score < 80
```

### System Architecture Quality Gates
```yaml
architecture_quality_gates:
  gate_1_production_ready:
    condition: architecture_score >= 90
    action: "PASS - System architecture meets production standards"
    message: "Architecture score: [score]/100. Ready for production deployment."

  gate_2_improvement_needed:
    condition: architecture_score >= 85
    action: "WARNING - System architecture below optimal threshold"
    message: "Architecture score: [score]/100. Consider improvements for production use."

  gate_3_major_revision:
    condition: architecture_score < 85
    action: "BLOCK - System architecture requires significant improvement"
    message: "Architecture score: [score]/100. Major revision needed before deployment."
```

## Integration with Self-Healing Protocol

### Architecture Gap Detection Alert
```markdown
## 🏗️ SYSTEM ARCHITECTURE GAPS DETECTED

**Overall Architecture Score**: [score]/100 ([rating])
**Threshold**: 90/100 for production deployment
**Gaps Found**: [count] architecture gaps identified

**Dimension Breakdown**:
- System Coordination Patterns: [score]/100 ([status])
- Integration Architecture Coverage: [score]/100 ([status])
- Resilience Architecture Validation: [score]/100 ([status])
- Resource Management Architecture: [score]/100 ([status])

**🔧 APPLYING ARCHITECTURE CORRECTIONS**:
- Coordination: [specific_coordination_fix]
- Integration: [specific_integration_fix]
- Resilience: [specific_resilience_fix]
- Resource Management: [specific_resource_fix]

**✅ VALIDATION**: Re-analyzing system architecture post-correction...
```

## Common Architecture Issues and Corrections

### System Coordination Issues
```yaml
common_coordination_issues:
  protocol_inconsistency:
    problem: "Mixed communication patterns and message formats"
    correction: "Standardize to Agent → Task → Result pattern with schema validation"

  timeout_misconfiguration:
    problem: "Timeout values outside 30-60 second optimal range"
    correction: "Configure 30-60s timeouts with exponential backoff and circuit breaker"

  dependency_complexity:
    problem: "Dependency chains exceed 5 levels or contain circular references"
    correction: "Refactor dependency architecture to <5 levels with clear orchestration"

  cascade_vulnerability:
    problem: "Missing circuit breakers for critical paths"
    correction: "Implement circuit breakers with proper isolation and monitoring"
```

### Integration Architecture Issues
```yaml
common_integration_issues:
  incomplete_interface_coverage:
    problem: "Less than 95% component interface documentation"
    correction: "Complete interface specifications with data flow validation"

  missing_workflow_paths:
    problem: "Incomplete alternative or exception workflow paths"
    correction: "Add comprehensive workflow coverage including error scenarios"

  external_integration_gaps:
    problem: "Third-party integrations lack proper error handling"
    correction: "Implement comprehensive external integration error handling"
```

### Resilience Architecture Issues
```yaml
common_resilience_issues:
  monitoring_gaps:
    problem: "Less than 100% system monitoring coverage"
    correction: "Implement comprehensive monitoring with 95% prediction accuracy"

  recovery_automation_deficit:
    problem: "Less than 80% recovery automation"
    correction: "Automate restart, rollback, and failover procedures"

  degradation_strategy_missing:
    problem: "No graceful degradation patterns defined"
    correction: "Implement 4-level degradation with 90% core function preservation"
```

## Task Tool Spawn Pattern

### Systematic Architecture Validation Command
```bash
# Spawn Task for comprehensive architecture analysis
Task: "Perform complete system architecture validation using consolidated patterns"

# Parameters for Task spawn:
validation_scope: "system_coordination,integration_architecture,resilience_architecture,resource_management"
analysis_depth: "comprehensive"
scoring_method: "weighted_dimensional"
quality_gates: "production_ready_90_threshold"
correction_mode: "automated_with_verification"
```

### Architecture Assessment Automation
```bash
# Complete system architecture analysis
echo "=== System Architecture Validation ==="

# Coordination pattern analysis
echo "Coordination Patterns:"
grep -n -E 'Agent.*→.*Agent|coordinator|orchestrator|timeout.*\\d+|circuit.*breaker' [target_file] | wc -l

# Integration architecture analysis
echo "Integration Architecture:"
grep -n -E '\\b(integration|interface|api)\\b.*\\b(endpoint|service)\\b|^(Step|Phase)\\s+\\d+' [target_file] | wc -l

# Resilience architecture analysis
echo "Resilience Architecture:"
grep -n -E '\\b(monitor|recover|graceful|isolat)\\b.*\\b(health|strategy|degradation|resource)\\b' [target_file] | wc -l

# Resource management analysis
echo "Resource Management:"
grep -n -E '\\b(resource|dependency|constraint|limit)\\b.*\\b(allocation|management|specification)\\b' [target_file] | wc -l

echo "Overall Architecture Score Calculation..."
```

## System Architecture Report Template

```yaml
system_architecture_report:
  assessment_metadata:
    target_file: "[file_path]"
    assessment_date: "[timestamp]"
    analysis_duration: "[actual_time]"
    architecture_validator_version: "1.0.0"

  dimension_scores:
    system_coordination_patterns:
      score: 0  # 0-100
      weight: 30  # percent
      status: "PASS|FAIL"
      issues_found: []
      recommendations: []

    integration_architecture_coverage:
      score: 0  # 0-100
      weight: 25  # percent
      status: "PASS|FAIL"
      issues_found: []
      recommendations: []

    resilience_architecture_validation:
      score: 0  # 0-100
      weight: 25  # percent
      status: "PASS|FAIL"
      issues_found: []
      recommendations: []

    resource_management_architecture:
      score: 0  # 0-100
      weight: 20  # percent
      status: "PASS|FAIL"
      issues_found: []
      recommendations: []

  overall_assessment:
    total_architecture_score: 0  # weighted average
    architecture_rating: "excellent|good|acceptable|needs_improvement|poor"
    production_readiness: "READY|NOT_READY"
    critical_issues: []
    improvement_priority: []

  architecture_certification:
    design_validated: true/false
    architecture_confidence: 0  # 0-100
    assessment_quality: "high|medium|low"
```

## Success Criteria and Integration

**System Architecture Validation Achieved When**:
- ✅ System Coordination: ≥95% protocol compliance, 30-60s timeouts, <5 dependency levels, circuit breaker coverage
- ✅ Integration Architecture: ≥95% interface coverage, complete workflow paths, 90% external integration coverage
- ✅ Resilience Architecture: 100% monitoring, 95% prediction accuracy, 80% automation, 90% core function preservation
- ✅ Resource Management: 95% critical resource identification, comprehensive constraint management, 80% optional dependency handling
- ✅ Overall Architecture: ≥90% weighted score for production deployment

**Integration Points**:
- Vagueness detection: `meta/validation/validators/language/vagueness-detector.md`
- Anti-fiction validation: `meta/validation/validators/accuracy/anti-fiction-validator.md`
- Constitutional AI compliance: `meta/validation/validators/compliance/constitutional-ai-checker.md`
- Framework coherence: `meta/validation/validators/framework/framework-coherence-analyzer.md`
- Self-healing protocol: `meta/validation/protocols/self-healing-error-detection-patterns.md`

**Performance Target**: 95% accuracy in system architecture assessment with 90% effectiveness in identifying design coordination issues and systematic architecture improvement opportunities.