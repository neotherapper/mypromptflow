Validate Claude Code .claude/agents/*.md files against established best practices framework ensuring single responsibility, tool optimization, context isolation, and anti-pattern prevention.

## Validation Framework

**Reference Integration**: Use `@knowledge-vault/knowledge/techniques/claude-subagents-best-practices.md` for comprehensive assessment criteria and `@knowledge-vault/knowledge/technologies/*/` for technology-specific patterns.

**Compliance Scoring**: 0-100 scale targeting ≥85/100 for production deployment with detailed breakdown across 5 validation dimensions.

## Assessment Methodology

### 1. Single Responsibility Principle (25 points)
Verify agent scope represents single coherent domain without scope creep or excessive breadth.

**Assessment Criteria**:
- **Domain Coherence** (10 points): Agent scope forms logical, coherent domain boundary
- **Scope Boundaries** (8 points): Clear boundaries without overlap with other specialists  
- **Anti-Pattern Detection** (7 points): No micro-specialization or overly broad coverage

**Scoring Algorithm**:
```yaml
single_responsibility_scoring:
  excellent (23-25): "Clear single domain, no scope creep detected"
  good (20-22): "Mostly coherent with minor boundary optimization opportunities"
  needs_review (15-19): "Some scope creep or unclear domain boundaries"
  non_compliant (0-14): "Multiple domains or excessive scope violations"
```

**Validation Process**:
1. Parse agent description and system prompt for domain indicators
2. Check for multiple unrelated responsibilities or excessive granularity
3. Compare against technology-specific patterns from knowledge vault
4. Assess coherence of assigned tools with domain scope
5. Identify scope creep or consolidation opportunities

### 2. Tool Minimalism (20 points)
Validate optimal tool selection following standard Read/Grep/Glob pattern with minimal necessary additions.

**Assessment Criteria**:
- **Standard Pattern Adherence** (8 points): Uses Read, Grep, Glob as foundation
- **Necessary Additions Logic** (7 points): Additional tools justified by domain requirements
- **Anti-Pattern Prevention** (5 points): No tool bloat or unnecessary complexity

**Tool Classification Standards**:
```yaml
tool_patterns:
  standard_foundation: ["Read", "Grep", "Glob"]
  research_enhancement: "+WebSearch, +WebFetch (for research domains)"
  development_enhancement: "+Bash (for development execution)"
  management_enhancement: "+Write, +Edit, +TodoWrite (for coordination)"
  
anti_patterns:
  tool_bloat: "More than 6 tools without clear justification"
  missing_foundation: "Lacks standard Read/Grep/Glob foundation"
  domain_mismatch: "Tools don't align with agent domain responsibility"
```

**Validation Process**:
1. Extract tools list from YAML frontmatter
2. Verify standard foundation (Read, Grep, Glob) presence
3. Assess necessity of additional tools based on domain requirements
4. Check against technology-specific tool patterns in knowledge vault
5. Identify tool optimization opportunities or excessive complexity

### 3. Context Isolation (20 points)
Verify independent 200k-token contexts with domain-specific expertise and contamination prevention.

**Assessment Criteria**:
- **Independence Validation** (8 points): Agent can operate with isolated context
- **Domain Specificity** (7 points): Context focused on specialist expertise area
- **Contamination Prevention** (5 points): No cross-domain context pollution

**Context Analysis Framework**:
```yaml
context_isolation_patterns:
  excellent_isolation:
    - "Clear domain boundaries in system prompt"
    - "Specialist expertise without other domain knowledge"
    - "Independent operation capability documented"
    
  contamination_indicators:
    - "References to multiple unrelated domains"
    - "Generic responsibilities crossing domain boundaries"
    - "Dependencies on other agent contexts for basic operation"
```

**Validation Process**:
1. Analyze system prompt for domain focus and boundary clarity
2. Check for cross-domain knowledge requirements or references
3. Assess independence of operation within 200k-token context
4. Identify contamination risks or unclear domain boundaries
5. Verify domain-specific expertise depth and coherence

### 4. Anti-Pattern Prevention (20 points)
Detect and prevent micro-specialization, overly broad agents, and other configuration anti-patterns.

**Assessment Criteria**:
- **Micro-Specialization Detection** (8 points): Identify overly granular scopes
- **Excessive Breadth Prevention** (7 points): Detect agents covering too many domains
- **Consolidation Assessment** (5 points): Suggest appropriate domain consolidation

**Anti-Pattern Detection Framework**:
```yaml
anti_patterns:
  micro_specialization:
    indicators: ["Single function focus", "Extremely narrow scope", "Should be part of larger domain"]
    examples: ["css-validator vs frontend-specialist", "error-logger vs monitoring-specialist"]
    
  excessive_breadth:
    indicators: ["Multiple unrelated domains", "Jack-of-all-trades scope", "Context overload risk"]
    examples: ["frontend-backend-database-specialist", "everything-validator"]
    
  consolidation_opportunities:
    patterns: ["Related micro-agents", "Overlapping domains", "Coordination overhead"]
```

**Validation Process**:
1. Assess agent scope granularity against best practices framework
2. Identify micro-specialization patterns requiring consolidation
3. Detect overly broad agents needing domain separation
4. Compare against technology-specific patterns for optimal scope
5. Recommend consolidation or separation based on best practices

### 5. Configuration Quality (15 points)
Validate YAML frontmatter structure, system prompt clarity, and documentation completeness.

**Assessment Criteria**:
- **YAML Structure** (6 points): Required fields (name, description, tools, team, priority)
- **System Prompt Quality** (5 points): Clear, actionable, domain expertise demonstration
- **Documentation Completeness** (4 points): Adequate context for agent operation

**Configuration Standards**:
```yaml
required_yaml_fields:
  mandatory: ["name", "description", "tools"]
  recommended: ["team", "priority", "specialization", "context_scope"]
  
system_prompt_quality:
  clarity: "Unambiguous instructions and responsibilities"
  actionability: "Specific, executable guidance for agent operation"
  expertise: "Demonstrates deep domain knowledge and specialist focus"
  
documentation_requirements:
  context_sufficiency: "Complete operational context within agent file"
  independence: "No external dependencies for basic understanding"
  maintainability: "Clear structure enabling future updates and improvements"
```

**Validation Process**:
1. Parse and validate YAML frontmatter structure and completeness
2. Assess system prompt for clarity, actionability, and expertise demonstration
3. Check documentation adequacy for independent agent operation
4. Verify configuration follows established structural patterns
5. Identify improvement opportunities for clarity and completeness

## Comprehensive Scoring Algorithm

### Scoring Aggregation
```yaml
total_score_calculation:
  single_responsibility: "25 points maximum"
  tool_minimalism: "20 points maximum"
  context_isolation: "20 points maximum"
  anti_pattern_prevention: "20 points maximum"
  configuration_quality: "15 points maximum"
  total_maximum: "100 points"
```

### Compliance Interpretation
```yaml
compliance_levels:
  excellent (90-100):
    status: "Production ready - exemplary best practices implementation"
    action: "Deploy immediately, use as reference pattern"
    
  good (80-89):
    status: "Production ready with minor optimizations available"
    action: "Deploy with optional improvements during next review cycle"
    
  needs_review (70-79):
    status: "Requires improvements before production deployment"
    action: "Address identified issues, re-validate before deployment"
    
  non_compliant (0-69):
    status: "Major revisions required - not suitable for production"
    action: "Comprehensive redesign following best practices framework"
```

## Validation Output Format

### Compliance Report Structure
```yaml
agent_compliance_report:
  agent_file: "Path to validated agent file"
  total_score: "0-100 compliance score"
  compliance_level: "excellent|good|needs_review|non_compliant"
  
  dimension_scores:
    single_responsibility: "Score/25 with specific findings"
    tool_minimalism: "Score/20 with tool analysis"
    context_isolation: "Score/20 with domain assessment"
    anti_pattern_prevention: "Score/20 with pattern analysis"
    configuration_quality: "Score/15 with structure review"
    
  recommendations:
    priority_high: ["Critical improvements required for compliance"]
    priority_medium: ["Important optimizations for best practices"]
    priority_low: ["Minor enhancements for excellence"]
    
  best_practices_reference:
    patterns_followed: ["Successfully implemented patterns"]
    patterns_missing: ["Best practices not yet applied"]
    framework_alignment: "Alignment with knowledge vault patterns"
```

### Actionable Improvement Suggestions
```yaml
improvement_framework:
  single_responsibility_improvements:
    - "Narrow scope to focus on [specific domain]"
    - "Separate [unrelated functionality] into dedicated specialist"
    - "Consolidate with [related agent] to reduce coordination overhead"
    
  tool_optimization_suggestions:
    - "Remove unnecessary [specific tools] not required for domain"
    - "Add [missing tools] essential for domain operation"
    - "Consider consolidation pattern from knowledge vault"
    
  context_isolation_enhancements:
    - "Remove cross-domain references to [specific areas]"
    - "Strengthen domain-specific expertise in [specialist area]"
    - "Clarify independence boundaries for operational clarity"
    
  anti_pattern_prevention_actions:
    - "Consolidate micro-specialized scope into comprehensive domain"
    - "Separate overly broad responsibilities into focused specialists"
    - "Apply [technology-specific] patterns from knowledge vault"
    
  configuration_quality_improvements:
    - "Add missing YAML fields: [specific fields]"
    - "Enhance system prompt clarity in [specific areas]"
    - "Improve documentation completeness for [specific aspects]"
```

## Integration Requirements

### Meta Framework Integration
- **File Pattern**: `.claude/agents/*.md`
- **Validation Trigger**: Automatic on file creation/modification
- **Registry Integration**: Listed in `meta/validation/validators/registry.yaml`
- **Command Integration**: Available through `.claude/commands/validate-agents.md`

### Knowledge Vault Integration
- **Best Practices Reference**: `knowledge-vault/knowledge/techniques/claude-subagents-best-practices.md`
- **Technology Patterns**: `knowledge-vault/knowledge/technologies/*/` for domain-specific validation
- **Continuous Updates**: Framework evolves with knowledge vault enhancements

### Quality Assurance Integration
- **Constitutional AI Compliance**: Ethical validation principles applied to all assessments
- **Self-Consistency Verification**: Multiple validation passes for accuracy confirmation
- **Framework Validation**: Regular assessment of validator effectiveness and accuracy

This validator ensures systematic application of Claude sub-agents best practices, maintaining high quality standards and preventing configuration anti-patterns across all agent deployments.