Execute research workflow using context-aware method selection from @research/orchestrator/config/selection-rules.yaml for: $ARGUMENTS

## Research Workflow:

**Orchestrator Activation Decision**: Follows @meta/shared/intention-detection-framework.md patterns with 95% confidence threshold using keyword detection: "research", "analyze", "investigate", "study", "explore", "examine"

1. **Extract Research Context** from the request using documented parameter extraction from claude-orchestrator-integration.yaml
2. **Analyze Complexity** using @research/orchestrator/engines/context-analyzer.yaml scoring algorithm (simple/moderate/complex classification)
3. **Select Primary Methods** using documented selection algorithm with complexity_score ≥0.80 confidence threshold from method-registry.yaml
4. **Execute Research** using multi-agent approach with constitutional AI validation ≥95% compliance across 5 principles
5. **Generate Findings** following research-execution-log-template.yaml with quality metrics documentation and evidence-based claims only
6. **Save Research** according to @research/orchestrator/integration/claude-orchestrator-integration.yaml file structure with mandatory completion validation

## Execution Process:

**Research Orchestrator Navigation:**
- Read orchestrator integration: `@research/orchestrator/integration/claude-orchestrator-integration.yaml`
- Use context analyzer: `@research/orchestrator/engines/context-analyzer.yaml`
- Select methods from: `@research/orchestrator/config/method-registry.yaml`
- Follow selection rules: `@research/orchestrator/config/selection-rules.yaml`
- Execute using multi-agent mode with Task tool capability
- Save research to: `research/findings/[topic]/` following documented file structure specifications
- Follow mandatory research completion requirements: research-plan.md and research-sources.md creation

## Error Handling and Fallback Procedures:

**If Research Orchestrator Framework Unavailable** (timeout after 30 seconds):
Execute basic 6-step sequence with specific commands:

1. **Intent Detection**: Apply keyword patterns from intention-detection-framework.md with documented confidence thresholds
2. **Context Extraction**: Parse user request for research_topic, research_scope, quality_requirements, time_constraints using template structure
3. **Complexity Assessment**: Calculate complexity_score using algorithm: emerging_technology(+0.3) + multiple_domains(+0.2) + ethical_implications(+0.2) + technical_depth(+0.1)
4. **Method Selection**: Select from fallback_methods based on complexity_level: simple→step_by_step_research, moderate→domain_adaptive, complex→multi_perspective_approach  
5. **Research Execution**: Execute with constitutional AI validation ≥95% compliance, timeout 300 seconds maximum per research phase
6. **Summary Generation**: Create findings documentation with quality_metrics: accuracy_score, completeness_score, constitutional_compliance_percentage

**Quality Validation Requirements**:
- Constitutional AI compliance ≥95% across accuracy(95%), transparency(95%), completeness(85%), responsibility(80%), integrity(85%)
- Research execution timeout: 300 seconds maximum per phase, 1800 seconds total maximum
- Source credibility assessment using documented criteria from research framework  
- Self-consistency verification for all quantitative claims and assessments
- Mandatory file creation: research-plan.md, research-sources.md, comprehensive-analysis.md
- Success criteria validation: All required files exist AND constitutional compliance achieved