# Actionable Framework Techniques

## Core Transformation Patterns

### Pattern 1: Specificity Amplification

**Technique**: Replace vague terms with exact specifications

**Before/After Examples**:

```yaml
vague: "Monitor system performance regularly"
actionable: "Check CPU usage every 30 seconds, alert if >80% for 5 consecutive readings"
improvement: +0.45 actionability score
```

```yaml
vague: "Coordinate agents effectively"
actionable: "Execute coordination sequence: 1) Spawn Queen Agent with unlimited authority, 2) Set reporting intervals: Queen=master, Architect=15min, Specialist=10min, Worker=5min, 3) Monitor 847 tasks/second target, 4) Escalate failures within 60s"
improvement: +0.60 actionability score
```

**Application Rules**:
- Replace "regularly" with specific time intervals
- Replace "effectively" with measurable criteria
- Replace "appropriately" with exact specifications
- Replace "properly" with step-by-step procedures

### Pattern 2: Measurability Injection

**Technique**: Add quantitative metrics to qualitative statements

**Before/After Examples**:

```yaml
vague: "Ensure high quality output"
actionable: "Validate output meets accuracy ≥ 0.95, completeness ≥ 0.90, consistency ≥ 0.85"
improvement: +0.50 actionability score
```

```yaml
vague: "Optimize for better performance"
actionable: "Execute optimization sequence: 1) Measure baseline (CPU, memory, response time), 2) Apply optimizations (caching, compression, parallel processing), 3) Validate >20% improvement in response time, 4) Confirm resource usage ≤ baseline"
improvement: +0.60 actionability score
```

**Application Rules**:
- Define specific thresholds for success (≥, ≤, =)
- Use decimal format for percentages (0.85 not 85%)
- Include measurement methods and validation criteria
- Specify units for all quantitative measures

### Pattern 3: Execution Path Clarification

**Technique**: Convert abstract goals to concrete steps

**Before/After Examples**:

```yaml
vague: "Improve user experience"
actionable: "Execute UX improvement sequence: 1) Measure baseline (page load time, bounce rate, task completion rate), 2) Apply improvements (optimize images, reduce HTTP requests, streamline navigation), 3) A/B test changes with 1000 users, 4) Validate >15% improvement in task completion rate"
improvement: +0.65 actionability score
```

**Application Rules**:
- Break abstract goals into numbered steps
- Make each step independently executable
- Include validation for each step
- Define completion criteria for the sequence

### Pattern 4: Parameter Specification

**Technique**: Define exact values, thresholds, and criteria

**Parameter Standards**:

```yaml
numerical_parameters:
  percentages: "0.75 (not 75%)"
  thresholds: "0.85 (not 'high')"
  timeouts: "300s (not 'a few minutes')"
  quantities: "5 items (not 'several')"
  ranges: "[0.7, 0.9] (not 'reasonable range')"

string_parameters:
  file_paths: "/full/path/to/file.txt (not 'the file')"
  identifiers: "user_id_12345 (not 'user identifier')"
  status_values: "'completed' (not 'done')"
  formats: "'YYYY-MM-DD' (not 'date format')"
```

## Advanced Transformation Techniques

### Decision Tree Pattern

**Structure**: `IF condition THEN action ELSE alternative`

**Template**:
```yaml
decision_pattern:
  condition: "measurable_variable comparison_operator threshold_value"
  action: "specific_executable_command"
  alternative: "fallback_executable_command"
```

**Example**:
```yaml
instruction: "IF token_usage > 0.75 THEN activate_compression_mode(level=2, symbols=true) ELSE continue_standard_processing()"
```

### Command Execution Pattern

**Structure**: `VERB + OBJECT + PARAMETERS + CRITERIA`

**Template**:
```yaml
command_pattern:
  verb: "execute|create|monitor|validate|configure"
  object: "function_name|file_path|process_id|variable_name"
  parameters: "numerical_values|string_literals|boolean_flags"
  criteria: "measurable_conditions|threshold_values|validation_rules"
```

**Examples**:
```yaml
commands:
  - "Execute analyze_data() with parameters {threshold: 0.85, timeout: 300s} until accuracy ≥ 0.90"
  - "Create file /path/to/output.json with content {data: results} and validate size > 1KB"
  - "Monitor process_id 12345 every 10 seconds for CPU usage < 80% over 5 minutes"
```

### Multi-Agent Coordination Pattern

**Structure**: `COORDINATOR → AGENTS → SYNCHRONIZATION → VALIDATION`

**Template**:
```yaml
coordination_pattern:
  coordinator: "COORDINATOR_AGENT(id=unique_id)"
  agents: "SPAWN_AGENTS(type=count, type=count)"
  synchronization: "SYNCHRONIZATION_POINTS(percentages)"
  validation: "VALIDATION_REQUIREMENTS(metrics)"
```

**Example**:
```yaml
instruction: |
  COORDINATOR_AGENT(id=queen_001):
    SPAWN_AGENTS(architect=2, specialist=5, worker=10)
    CONFIGURE_REPORTING(architect=15min, specialist=10min, worker=5min)
    SET_THRESHOLDS(throughput=847tasks/s, latency=4.2ms)
  
  AGENT_COORDINATION:
    PARALLEL_EXECUTION(max_concurrent=3)
    SYNCHRONIZATION_POINTS(25%, 50%, 75%, 100%)
    CONFLICT_RESOLUTION(method=majority_vote)
  
  VALIDATION_REQUIREMENTS:
    SYSTEM_PERFORMANCE(target_throughput≥847tasks/s)
    QUALITY_METRICS(accuracy≥0.95, consistency≥0.90)
    RESOURCE_EFFICIENCY(cpu_utilization≤0.78, memory_efficiency≥0.94)
```

## Compression Without Ambiguity

### Ultra-Compressed Format

**Structure**: `ACTION(params) → CRITERIA → RESULT`

**Examples**:
```yaml
compressed_format:
  - "SPAWN_AGENT(type=analyst, max=5) → response_time<100ms → agent_id_list"
  - "VALIDATE_OUTPUT(threshold=0.95) → accuracy≥0.95 → validation_passed"
  - "MONITOR_SYSTEM(interval=30s) → CPU<80% → status_report"
```

**Compression Rules**:
- Preserve all parameters (no parameter removal)
- Maintain measurable success criteria
- Keep exact values (no approximation)
- Use standard mathematical operators

### Context-Aware Optimization

**Agent Capability Levels**:

```yaml
high_capability_agents:
  instruction_complexity: "maximum_complexity_allowed"
  parameter_count: "unlimited_parameters"
  nested_structures: "deep_nesting_supported"
  parallel_execution: "multiple_concurrent_tasks"

medium_capability_agents:
  instruction_complexity: "moderate_complexity"
  parameter_count: "max_20_parameters"
  nested_structures: "max_3_levels_deep"
  parallel_execution: "max_3_concurrent_tasks"

basic_capability_agents:
  instruction_complexity: "simple_sequential_only"
  parameter_count: "max_10_parameters"
  nested_structures: "no_nesting"
  parallel_execution: "sequential_only"
```

## Progressive Context Loading Implementation

### User Choice Driven Loading

**Template**:
```yaml
progressive_loading:
  instruction: |
    Based on your selection, I will load specific guidance:
    
    If you choose "Research Analysis":
      - Load procedures from knowledge/research/analysis-methods.md
      - Apply validation from knowledge/quality/research-validation.md
      - Use templates from knowledge/templates/analysis-template.md
    
    If you choose "System Design":
      - Load architecture patterns from knowledge/architecture/design-patterns.md
      - Apply SPARC methodology from knowledge/methodologies/sparc-framework.md
      - Use validation from knowledge/quality/design-validation.md
  
  benefits:
    token_efficiency: "60-70% reduction in initial context load"
    relevance: "100% relevant context for user's actual choice"
    speed: "Faster initial response, targeted context loading"
```

### Analysis Driven Loading

**Template**:
```yaml
analysis_driven:
  instruction: |
    After analyzing the task, I will load appropriate context:
    
    Step 1: Analyze task complexity and requirements
    Step 2: Determine required expertise level
    Step 3: Load context based on analysis:
      - If complexity_score ≤ 3: Load knowledge/basic/simple-procedures.md
      - If complexity_score 4-6: Load knowledge/intermediate/standard-procedures.md
      - If complexity_score ≥ 7: Load knowledge/advanced/complex-procedures.md
    Step 4: Apply loaded procedures with full context
  
  benefits:
    intelligence: "Context selection based on actual requirements"
    efficiency: "Load only necessary complexity level"
    accuracy: "Appropriate context for actual task complexity"
```

## Validation and Testing Procedures

### Pre-Execution Validation Sequence

**Step 1: Syntax Validation (30 seconds)**
- Check command structure for proper syntax
- Validate all required parameters are present
- Verify parameter types match requirements

**Step 2: Semantic Validation (60 seconds)**
- Verify logical consistency of step dependencies
- Validate success criteria are measurable
- Check resource availability and accessibility

**Step 3: Executability Validation (120 seconds)**
- Simulate execution without side effects
- Verify error handling for failure scenarios
- Validate timeout handling and responses

### Execution Readiness Criteria

**Mandatory Conditions**:
```yaml
readiness_criteria:
  completeness: "all_steps_defined=true, parameters_specified=true, success_criteria_measurable=true"
  clarity: "no_ambiguous_terms=true, specific_actions_only=true, objective_criteria=true"
  executability: "no_external_dependencies=true, immediate_execution_possible=true, no_interpretation_required=true"
```

### Automated Testing Framework

**Syntax Testing**:
- Parse instruction structure (YAML/JSON validation)
- Check required fields presence
- Validate parameter type correctness
- Duration: <10 seconds

**Semantic Testing**:
- Logical consistency verification
- Parameter range validation
- Success criteria measurability check
- Duration: <30 seconds

**Executability Testing**:
- Dry run simulation without side effects
- Resource availability verification
- Timeout scenario testing
- Duration: <60 seconds

## Application Examples

### Complex System Optimization

**Before**:
```yaml
vague: "Optimize the system for better performance"
actionability_score: 0.15
```

**After**:
```yaml
actionable: |
  SYSTEM_OPTIMIZATION_SEQUENCE(target_improvement=0.30):
    STEP_1_BASELINE_MEASUREMENT(duration=300s):
      RECORD(cpu_usage, memory_usage, response_time, throughput, error_rate)
      CALCULATE(performance_score = weighted_average(metrics))
    
    STEP_2_OPTIMIZATION_APPLICATION:
      ENABLE_CACHING(type=redis, size=4GB, ttl=3600s)
      ACTIVATE_COMPRESSION(algorithm=gzip, level=6)
      CONFIGURE_LOAD_BALANCING(algorithm=round_robin, health_checks=30s)
      OPTIMIZE_DATABASE(indexes=true, query_optimization=true)
    
    STEP_3_PERFORMANCE_VALIDATION(duration=300s):
      MEASURE(same_metrics_as_baseline)
      CALCULATE(improvement = (new_score - baseline_score) / baseline_score)
      REQUIRE(improvement ≥ 0.30)
    
    STEP_4_STABILITY_VERIFICATION(duration=1800s):
      MONITOR(performance_stability, variance_threshold=0.05)
      VALIDATE(error_rate ≤ baseline_error_rate)
      CONFIRM(resource_usage ≤ baseline_resource_usage)

actionability_score: 0.94
improvements: ["specific_optimizations", "measurable_targets", "validation_procedures"]
```

### Research Task Transformation

**Before**:
```yaml
vague: "Research competitive landscape and provide insights"
actionability_score: 0.25
```

**After**:
```yaml
actionable: |
  RESEARCH_COMPETITIVE_LANDSCAPE(domain=target_domain):
    STEP_1_LOAD_RESEARCH_METHODOLOGY:
      Based on domain complexity, load appropriate research methods:
      - Load base methodology from knowledge/research/competitive-analysis-framework.md
      - Load domain-specific techniques from knowledge/research/domain-analysis.md
      - Load validation procedures from knowledge/quality/research-validation.md
    
    STEP_2_EXECUTE_RESEARCH_SEQUENCE:
      Apply loaded methodology:
      - COLLECT_DATA using procedures from loaded framework
      - ANALYZE_COMPANIES using domain-specific techniques
      - EXTRACT_METRICS using industry-standard metrics
      - SYNTHESIZE_FINDINGS using validation procedures
    
    STEP_3_PROGRESSIVE_VALIDATION:
      - Validate each step using knowledge/quality/research-validation.md
      - Apply quality gates from knowledge/quality/checkpoints.md
      - Generate report using knowledge/templates/competitive-analysis-template.md

actionability_score: 0.94
context_efficiency: "70% reduction compared to full embedding"
```

## Integration with Knowledge Base

**Internal Reference Patterns**:
```yaml
reference_optimization:
  conditional_references:
    structure: "if (condition) load knowledge/path/context.md"
    example: "if (complexity > 7) load knowledge/orchestration/complex-patterns.md"
    benefit: "Context loaded only when needed"
  
  composition_references:
    structure: "load base + load specific based on parameters"
    example: "load knowledge/base/foundations.md + knowledge/specific/[choice].md"
    benefit: "Flexible context composition"
```

**Validation Procedures**:
```yaml
internal_reference_validation:
  accessibility_check: "verify all knowledge/ paths resolve"
  consistency_check: "ensure references are consistent across modules"
  performance_validation: "ensure context loads within 2 seconds"
```

This techniques module provides the core transformation patterns for converting vague instructions into immediately executable commands. Continue to [examples.md](examples.md) for practical applications or [implementation.md](implementation.md) for validation procedures.