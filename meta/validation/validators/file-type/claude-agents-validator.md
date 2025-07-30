# Claude Agents Sub-Agent Configuration Validator

## Validator Purpose

Specialized validation for .claude/agents sub-agent configuration files, ensuring compliance with Claude Code sub-agents architecture. Integrates meta/validation framework standards with Claude-specific requirements for optimal sub-agent performance.

## File Type Coverage

**Primary Files**: `.claude/agents/*.md`
**Configuration Format**: Markdown files with YAML frontmatter
**Architecture**: Claude Code sub-agents with independent 200k-token contexts

## Validation Framework Integration

### Best Practices Compliance Assessment
**Primary Reference**: `@meta/validation/validators/file-type/claude-subagents-compliance-validator.md`

This validator integrates comprehensive best practices assessment through the specialized compliance validator, ensuring:
- **Single Responsibility Principle**: 25-point assessment of domain coherence
- **Tool Minimalism**: 20-point evaluation of optimal tool selection  
- **Context Isolation**: 20-point verification of independent contexts
- **Anti-Pattern Prevention**: 20-point detection of micro-specialization or excessive breadth
- **Configuration Quality**: 15-point assessment of YAML structure and documentation

### Constitutional AI Compliance (5-Principle Assessment)
1. **Helpfulness**: Agent provides clear, actionable assistance within defined scope
2. **Harmlessness**: No potential for misuse or harmful coordination patterns
3. **Honesty**: Accurate capability descriptions without fabricated metrics
4. **Autonomy Respect**: Preserves user decision-making authority
5. **Privacy Protection**: Proper context isolation and data handling

### Anti-Fiction Validation
- **Evidence-Based Claims**: All capability assertions must be verifiable
- **Realistic Performance**: No fabricated efficiency or accuracy metrics
- **Honest Limitations**: Clear scope boundaries and capability constraints
- **Verifiable Integration**: Documented coordination patterns and tool usage

### Vagueness Detection
- **Clear Invocation Criteria**: Specific, unambiguous usage conditions
- **Concrete Specializations**: Detailed, actionable domain expertise
- **Measurable Outcomes**: Specific deliverables and success criteria
- **Actionable Instructions**: Direct, implementable system prompts

### Framework Coherence Analysis
- **Cross-Agent Consistency**: Naming conventions and format standardization
- **Tool Assignment Logic**: Appropriate tool selections for agent purposes
- **Context Isolation Compliance**: Proper independent context configuration
- **Integration Pattern Alignment**: Consistent coordination mechanisms

## Claude-Specific Validation Criteria

### YAML Frontmatter Requirements
```yaml
required_fields:
  - name: "Unique, descriptive agent identifier"
  - description: "Clear purpose and invocation criteria"

optional_fields:
  - tools: "Minimal necessary tool set (comma-separated)"
  - priority: "Delegation preference (high/medium/low)"
  - team: "Team or functional domain assignment"
  - domain: "Specialization area"
  - context_isolation: "true (recommended for sub-agents)"
```

### System Prompt Quality Assessment
- **Clarity Score**: ≥85/100 for comprehension and actionability
- **Specificity Rating**: Detailed task definition and scope boundaries
- **Context Optimization**: Efficient use of 200k-token context window
- **Integration Guidelines**: Clear coordination with main session

### Architecture Compliance Validation
- **Independent Context**: Verification of context isolation configuration
- **Parallel Execution Safety**: Validation of concurrent operation compatibility
- **Tool Efficiency**: Minimal necessary tool sets for performance optimization
- **Coordination Patterns**: Clean result delivery without context pollution

## Quality Scoring Framework

### Primary Scores (0-100 Scale)
- **Configuration Completeness**: Required fields presence and validity
- **System Prompt Quality**: Clarity, specificity, and actionability assessment
- **Constitutional AI Compliance**: 5-principle framework adherence
- **Architecture Adherence**: Claude sub-agents specification compliance

### Meta-Framework Scores (0-100 Scale)
- **Anti-Fiction Compliance**: Evidence-based claims verification
- **Vagueness Elimination**: Clear, actionable language assessment
- **Framework Coherence**: Cross-agent consistency validation
- **Integration Quality**: Coordination pattern effectiveness

## Specialized Agent Category Validation

### Research Agent Validation
- **Method Integration**: Compatibility with 15-method research orchestrator
- **Source Tool Configuration**: Proper WebSearch/WebFetch/Grep tool assignments
- **Quality Standards**: Research validation and compliance frameworks
- **Registry Integration**: Proper research registry coordination patterns

### Development Agent Validation
- **Code Generation Capabilities**: Tool configuration for code development
- **Quality Assurance Integration**: Testing and validation tool assignments
- **Framework Compliance**: Development standard adherence validation
- **Version Control Integration**: Git and repository coordination patterns

### Management Agent Validation
- **Task Coordination Tools**: TodoWrite and project management integration
- **Cross-Project Capabilities**: Multi-project coordination validation
- **Documentation Standards**: Progress tracking and reporting validation
- **Performance Metrics**: Measurable outcome and quality assessment

## Advanced Validation Features

### Context Isolation Verification
- **Independence Testing**: Verification of true context isolation
- **Pollution Prevention**: Assessment of contamination risk mitigation
- **Clean Communication**: Result delivery pattern validation
- **Parallel Safety**: Concurrent execution safety verification

### Performance Optimization Assessment
- **Token Efficiency**: Context window usage optimization
- **Tool Minimization**: Unnecessary tool elimination validation
- **Execution Speed**: Configuration for optimal performance
- **Resource Utilization**: Efficient resource usage patterns

### Integration Quality Assessment
- **Coordination Patterns**: Sub-agent coordination mechanism validation
- **Result Aggregation**: Clean result collection and delivery
- **Error Handling**: Error management and recovery pattern validation
- **Quality Reporting**: Metrics and feedback delivery assessment

## Validation Output Structure

### Comprehensive Assessment Report
```yaml
agent_validation_report:
  agent_name: "Validated agent identifier"
  overall_score: "Weighted average of all validation scores"
  
  best_practices_compliance:
    reference: "@meta/validation/validators/file-type/claude-subagents-compliance-validator.md"
    total_score: "0-100 best practices compliance score"
    single_responsibility: "Score/25 with domain coherence assessment"
    tool_minimalism: "Score/20 with optimization recommendations"
    context_isolation: "Score/20 with independence verification"
    anti_pattern_prevention: "Score/20 with consolidation suggestions"
    configuration_quality: "Score/15 with structure assessment"
  
  configuration_assessment:
    completeness_score: "0-100 (required fields validation)"
    format_compliance: "YAML frontmatter format validation"
    naming_convention: "Consistency with repository standards"
    
  system_prompt_quality:
    clarity_score: "0-100 (comprehension and actionability)"
    specificity_rating: "Task definition and scope assessment"
    context_optimization: "200k-token window usage efficiency"
    
  meta_framework_compliance:
    constitutional_ai_score: "5-principle framework adherence"
    anti_fiction_score: "Evidence-based claims verification"
    vagueness_elimination: "Clear, actionable language assessment"
    framework_coherence: "Cross-agent consistency validation"
    
  claude_architecture_compliance:
    context_isolation: "Independent context verification"
    parallel_safety: "Concurrent execution compatibility"
    tool_efficiency: "Minimal necessary tool validation"
    integration_quality: "Coordination pattern assessment"
    
  recommendations:
    high_priority: "Critical improvements for production readiness"
    medium_priority: "Quality enhancements for optimization"
    low_priority: "Minor refinements for excellence"
    best_practices_specific: "Recommendations from compliance validator"
    
  production_readiness: "Overall assessment for deployment approval (≥85/100 threshold)"
```

### Quality Improvement Recommendations
- **Specific Enhancements**: Targeted improvements with implementation guidance
- **Framework Alignment**: Adjustments for meta/validation compliance
- **Performance Optimizations**: Efficiency improvements and best practices
- **Integration Enhancements**: Coordination pattern improvements

## Success Criteria and Thresholds

### Production Readiness Requirements
- **Overall Score**: ≥85/100 for production deployment approval
- **Constitutional AI**: ≥90/100 for ethical compliance validation
- **Anti-Fiction**: ≥95/100 for evidence-based accuracy
- **Vagueness Elimination**: ≥90/100 for actionable clarity
- **Architecture Compliance**: ≥90/100 for Claude sub-agents specification

### Quality Excellence Targets
- **Context Optimization**: ≥85/100 for efficient token usage
- **Tool Configuration**: ≥90/100 for appropriate tool selection
- **Integration Quality**: ≥85/100 for clean coordination patterns
- **Framework Coherence**: ≥90/100 for cross-agent consistency

This validator ensures comprehensive quality assessment of Claude sub-agent configurations while integrating all meta/validation framework standards for complete validation coverage and production readiness verification.