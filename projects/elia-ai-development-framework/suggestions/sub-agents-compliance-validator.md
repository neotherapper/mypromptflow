# Claude Sub-Agents Compliance Validator

## Core Functionality

Specialized validator for assessing Claude Code .claude/agents/*.md files against established best practices framework. Validates configuration structure, domain coherence, tool optimization, and anti-pattern prevention.

## Validation Framework

### Best Practices Reference Integration
**Primary Reference**: `knowledge-vault/knowledge/techniques/claude-subagents-best-practices.md`
**Technology Patterns**: React, TypeScript, Python sub-agents patterns from knowledge vault
**Compliance Scoring**: 0-100 scale with ≥85/100 target for production deployment

## Validation Criteria

### 1. Single Responsibility Principle (25 points)
**Validates**: Each agent has coherent single domain without scope creep
**Assessment Pattern**:
```yaml
single_responsibility_check:
  domain_coherence: "Verify agent scope represents single coherent domain"
  scope_boundaries: "Validate clear boundaries without overlap with other specialists"
  anti_pattern_detection: "Identify overly broad agents or micro-specialization"
  scoring_criteria:
    - excellent (23-25): "Clear single domain, no scope creep"
    - good (20-22): "Mostly coherent with minor boundary issues"
    - needs_review (15-19): "Some scope creep or unclear boundaries"
    - non_compliant (0-14): "Multiple domains or excessive scope"
```

### 2. Tool Minimalism (20 points)
**Validates**: Standard Read/Grep/Glob pattern with minimal necessary additions
**Assessment Pattern**:
```yaml
tool_optimization_check:
  standard_pattern: ["Read", "Grep", "Glob"]
  necessary_additions:
    research_agents: "+WebSearch, +WebFetch"
    development_agents: "+Bash"
    management_agents: "+Write, +Edit, +TodoWrite"
  anti_pattern_detection: "Excessive tool assignment or unnecessary complexity"
  scoring_criteria:
    - excellent (18-20): "Optimal tool selection for domain"
    - good (15-17): "Mostly optimized with 1-2 unnecessary tools"
    - needs_review (10-14): "Some tool bloat or missing essential tools"
    - non_compliant (0-9): "Excessive tools or inadequate tool selection"
```

### 3. Context Isolation (20 points)
**Validates**: Independent 200k-token contexts with domain-specific expertise
**Assessment Pattern**:
```yaml
context_isolation_check:
  independence_validation: "Verify agent can operate with isolated context"
  domain_specificity: "Confirm context focused on specialist domain"
  contamination_prevention: "Check for cross-domain context pollution"
  scoring_criteria:
    - excellent (18-20): "Perfect domain isolation and independence"
    - good (15-17): "Strong isolation with minor cross-domain elements"
    - needs_review (10-14): "Some context contamination or unclear boundaries"
    - non_compliant (0-9): "Significant context pollution or poor isolation"
```

### 4. Anti-Pattern Prevention (20 points)
**Validates**: Avoidance of micro-specialization and overly broad agents
**Assessment Pattern**:
```yaml
anti_pattern_check:
  micro_specialization: "Detect overly granular agent scopes (avoided pattern)"
  excessive_breadth: "Identify agents attempting to cover too many domains"
  consolidation_opportunities: "Suggest appropriate domain consolidation"
  scoring_criteria:
    - excellent (18-20): "Perfect balance, no anti-patterns detected"
    - good (15-17): "Good balance with minor optimization opportunities"
    - needs_review (10-14): "Some anti-pattern tendencies requiring attention"
    - non_compliant (0-9): "Clear anti-pattern violations requiring major revision"
```

### 5. Configuration Quality (15 points)
**Validates**: YAML frontmatter structure and system prompt clarity
**Assessment Pattern**:
```yaml
configuration_quality_check:
  yaml_structure: "Validate required fields (name, description, tools, team, priority)"
  system_prompt: "Assess clarity, actionability, and domain expertise"
  documentation: "Verify adequate context for agent operation"
  scoring_criteria:
    - excellent (14-15): "Complete, clear, and actionable configuration"
    - good (12-13): "Mostly complete with minor gaps"
    - needs_review (8-11): "Some missing elements or unclear documentation"
    - non_compliant (0-7): "Incomplete or poorly structured configuration"
```

## Validation Methodology

### Comprehensive Assessment Process
1. **Parse Agent Configuration**: Extract YAML frontmatter and system prompt content
2. **Domain Analysis**: Assess scope coherence and single responsibility compliance
3. **Tool Evaluation**: Validate tool selection against minimalism principles
4. **Context Assessment**: Verify independence and domain specificity
5. **Anti-Pattern Detection**: Check for micro-specialization or excessive breadth
6. **Configuration Review**: Validate structural completeness and clarity
7. **Scoring Aggregation**: Calculate total compliance score (0-100 scale)
8. **Recommendations**: Provide actionable improvement suggestions

### Scoring Interpretation
```yaml
compliance_levels:
  excellent: "90-100 points - Production ready, exemplary best practices"
  good: "80-89 points - Production ready with minor optimizations"
  needs_review: "70-79 points - Requires improvements before production"
  non_compliant: "0-69 points - Major revisions required"
```

## Integration with Meta Framework

### Validator Registry Integration
**Location**: `meta/validation/validators/file-type/claude-subagents-compliance-validator.md`
**Registry Entry**: Update `meta/validation/validators/registry.yaml` with:
```yaml
claude-subagents-compliance-validator:
  file_pattern: ".claude/agents/*.md"
  purpose: "Validate Claude sub-agents configurations against best practices"
  compliance_framework: "claude-subagents-best-practices"
  scoring_scale: "0-100 with ≥85 production threshold"
  last_updated: "2025-07-28"
  status: "production-ready"
```

### Usage Integration
**Validation Command**: `.claude/commands/validate-agents.md`
**Batch Assessment**: Validate all agents in `.claude/agents/` directory
**Continuous Monitoring**: Regular compliance assessment for configuration drift

## Expected Outcomes

### Immediate Benefits
1. **Quality Assurance**: Systematic validation of all agent configurations
2. **Best Practices Enforcement**: Automated compliance checking against documented standards
3. **Anti-Pattern Prevention**: Early detection of configuration issues
4. **Production Readiness**: Clear criteria for agent deployment validation

### Long-term Impact
1. **Consistent Quality**: Standardized approach to agent configuration validation
2. **Continuous Improvement**: Framework for ongoing best practices evolution
3. **Knowledge Base Integration**: Systematic application of documented patterns
4. **Scalable Validation**: Automated assessment supporting growth and expansion

## Implementation Strategy

### Phase 1: Core Validator Creation
1. **Framework Integration**: Implement validator using meta framework patterns
2. **Scoring Algorithm**: Develop comprehensive assessment methodology
3. **Registry Integration**: Add to validator registry with appropriate metadata
4. **Testing**: Validate against existing agents for effectiveness verification

### Phase 2: Integration Enhancement
1. **Command Integration**: Create validation command for easy usage
2. **Batch Processing**: Support for directory-level agent assessment
3. **Reporting**: Comprehensive compliance reports with improvement recommendations
4. **Continuous Monitoring**: Regular validation for configuration drift detection

This validator ensures systematic application of Claude sub-agents best practices across all agent configurations, maintaining high quality standards and preventing common anti-patterns.