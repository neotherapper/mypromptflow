# Sub-Agent Usage Patterns: Coordination and Orchestration

## Overview

This guide documents advanced usage patterns for coordinating Claude Code sub-agents, including sequential processing, parallel execution, and adaptive coordination. These patterns enable sophisticated multi-agent workflows while respecting architectural constraints and maintaining context isolation.

## Architectural Foundation

### Core Coordination Principles

**Main Session Orchestration** (Required):
- All sub-agent coordination must go through main Claude session
- Sub-agents CANNOT spawn other sub-agents (critical constraint)
- Maximum 10 concurrent sub-agents with automatic queuing
- Each sub-agent operates in independent 200k-token context

**Context Isolation Benefits**:
- Main conversation focus preserved during complex sub-agent work
- Implementation details contained within specialist contexts
- Clean results integration without pollution
- Parallel processing without context interference

## Sequential Processing Patterns

### Linear Workflow Pattern

**Use Case**: Dependent tasks requiring ordered execution

```yaml
development_lifecycle:
  phase_1:
    agent: "requirements-analyst"
    input: "Business requirements and user stories"
    output: "Structured technical specifications"
    
  phase_2:
    agent: "system-architect"
    input: "Technical specifications from phase 1"
    output: "System architecture and implementation plans"
    
  phase_3:
    agent: "implementation-lead"
    input: "Architecture plans from phase 2"
    output: "Development coordination and code quality guidelines"
    
  phase_4:
    agent: "qa-specialist"
    input: "Implementation results from phase 3"
    output: "Testing strategy and quality validation"
    
  coordination: "Main session passes results between phases"
  context_isolation: "Each specialist maintains independent context"
```

**Implementation Example**:
```
User: "Help me build a user authentication system"

Main Session Orchestration:
1. Invokes requirements-analyst → Analyzes business requirements
2. Takes analyst results → Invokes system-architect → Creates technical design
3. Takes architecture → Invokes implementation-lead → Coordinates development
4. Takes implementation → Invokes qa-specialist → Validates quality
5. Integrates all findings → Presents comprehensive development plan
```

### Multi-Stage Analysis Pattern

**Use Case**: Complex analysis requiring progressive refinement

```yaml
security_assessment_workflow:
  stage_1_discovery:
    agent: "information-access-specialist"
    purpose: "Source discovery and vulnerability research"
    framework: "information-access"
    output: "Comprehensive security source compilation"
    
  stage_2_analysis:
    agent: "security-code-reviewer"
    purpose: "Detailed security analysis using discovered sources"
    input: "Sources from stage 1"
    output: "Vulnerability assessment and risk analysis"
    
  stage_3_validation:
    agent: "framework-compliance-validator"
    purpose: "Compliance validation and quality assurance"
    input: "Security analysis from stage 2"
    output: "Compliance report and remediation recommendations"
    
  integration_pattern: "Sequential with context preservation"
  quality_assurance: "Constitutional AI validation at each stage"
```

## Parallel Processing Patterns

### Independent Analysis Pattern

**Use Case**: Multiple perspectives on same problem

```yaml
comprehensive_feature_analysis:
  parallel_specialists:
    frontend_perspective:
      agent: "react-specialist"
      focus: "UI/UX implementation and user experience"
      framework: "information-access (React sources)"
      
    backend_perspective:
      agent: "database-expert"
      focus: "Data modeling and API architecture"
      framework: "information-access (Database sources)"
      
    security_perspective:
      agent: "security-code-reviewer"
      focus: "Security implications and vulnerability assessment"
      framework: "information-access (Security sources)"
      
    performance_perspective:
      agent: "performance-optimizer"
      focus: "Performance bottlenecks and optimization opportunities"
      framework: "information-access (Performance sources)"
  
  coordination: "Main session launches all agents simultaneously"
  token_usage: "4x parallel agents = ~4x token consumption"
  completion_time: "Dramatically faster than sequential analysis"
  results_integration: "Main session consolidates all perspectives"
```

**Implementation Example**:
```
User: "Analyze this e-commerce checkout feature for production readiness"

Parallel Orchestration:
├── react-specialist → UI/UX analysis (independent context)
├── database-expert → Data architecture review (independent context)  
├── security-code-reviewer → Security assessment (independent context)
└── performance-optimizer → Performance analysis (independent context)

Main Session: Receives 4 independent analyses, integrates findings into comprehensive production readiness assessment
```

### Multi-Domain Investigation Pattern

**Use Case**: Complex problems requiring diverse expertise

```yaml
production_incident_analysis:
  parallel_investigation_teams:
    infrastructure_team:
      agent: "deployment-coordinator"
      domain: "Infrastructure and deployment analysis"
      tools: "Read, Grep, Glob, Bash"
      
    application_team:
      agent: "implementation-lead"
      domain: "Application code and logic analysis"
      tools: "Read, Grep, Glob, Bash"
      
    data_team:
      agent: "database-expert"
      domain: "Database performance and integrity analysis"
      tools: "Read, Grep, Glob, Bash"
      
    security_team:
      agent: "security-code-reviewer"
      domain: "Security incident and vulnerability analysis"
      tools: "Read, Grep, Glob, Bash, WebSearch"
  
  coordination_pattern: "Parallel investigation with independent findings"
  context_isolation: "Each team maintains separate investigation context"
  results_consolidation: "Main session creates unified incident report"
```

## Adaptive Coordination Patterns

### Context-Aware Routing Pattern

**Use Case**: Dynamic specialist selection based on content analysis

```yaml
intelligent_file_analysis:
  routing_logic:
    file_type_detection:
      "*.tsx, *.jsx, *.js": "react-specialist"
      "*.py, *.sql": "database-expert" 
      "*.yml, *.yaml, Dockerfile": "deployment-coordinator"
      "security-sensitive files": "security-code-reviewer"
      "test files": "qa-specialist"
      
    complexity_assessment:
      simple_changes: "Single appropriate specialist"
      moderate_changes: "2-3 coordinated specialists"
      complex_changes: "5-10 parallel specialists"
      
    framework_integration:
      research_needed: "information-access-specialist + research-specialist"
      validation_required: "appropriate validator + framework-compliance-validator"
      quality_critical: "multiple specialists + constitutional AI validation"
```

**Dynamic Selection Example**:
```
User: "Review this pull request with 15 files across frontend, backend, and infrastructure"

Adaptive Orchestration:
1. Main session analyzes file types and complexity
2. Routes files to appropriate specialists:
   ├── Frontend files → react-specialist
   ├── Backend files → database-expert
   ├── Infrastructure files → deployment-coordinator
   ├── Security-sensitive files → security-code-reviewer
3. Coordinates parallel analysis across 4 specialists
4. Integrates findings into comprehensive PR review
```

### Load-Balanced Processing Pattern

**Use Case**: Optimizing resource usage across multiple tasks

```yaml
concurrent_task_optimization:
  task_distribution:
    high_priority_queue: "Up to 6 specialists for critical tasks"
    medium_priority_queue: "Up to 3 specialists for important tasks"  
    low_priority_queue: "1 specialist for routine tasks"
    
  resource_allocation:
    token_budget_management: "Monitor cumulative token usage"
    performance_optimization: "Balance speed vs cost"
    queue_management: "Automatic queuing when exceeding 10 concurrent"
    
  adaptive_scheduling:
    peak_usage: "Prioritize high-impact specialists"
    normal_usage: "Balanced distribution across all specialists"
    low_usage: "Opportunistic processing of queued tasks"
```

## Framework-Enhanced Coordination

### Information Access Coordination

**Pattern**: Multiple specialists leveraging unified source discovery

```yaml
research_coordination_pattern:
  primary_coordinator:
    agent: "information-access-specialist"
    role: "Source discovery and coordination using unified framework"
    framework: "information-access"
    output: "Technology-specific source mappings and MCP coordination"
    
  specialized_consumers:
    react_research:
      agent: "react-specialist"
      sources: "React-specific mappings from information-access framework"
      
    security_research:
      agent: "security-code-reviewer"  
      sources: "Security-specific sources and vulnerability databases"
      
    performance_research:
      agent: "performance-optimizer"
      sources: "Performance optimization sources and benchmarking data"
  
  coordination_benefit: "Unified source discovery with specialized application"
  quality_enhancement: "Cross-validated information across multiple specialists"
```

### Research Orchestrator Integration

**Pattern**: Research specialist coordinating with domain experts

```yaml
comprehensive_research_pattern:
  research_coordinator:
    agent: "research-specialist"
    framework: "research-orchestrator (15 methods)"
    role: "Method selection and research execution"
    context: "Independent 200k context for research isolation"
    
  domain_validation:
    technology_expert: "Validates technical accuracy within domain"
    security_expert: "Validates security implications and compliance"
    performance_expert: "Validates performance claims and recommendations"
    
  quality_assurance:
    constitutional_ai: "95%+ compliance across all research outputs"
    cross_specialist_validation: "Domain expert verification of findings"
    framework_compliance: "Research method adherence and quality metrics"
```

## Quality Assurance Patterns

### Multi-Level Validation Pattern

**Use Case**: Ensuring quality across complex multi-agent workflows

```yaml
quality_assurance_stack:
  agent_level_validation:
    constitutional_ai: "95%+ compliance for each individual agent"
    framework_integration: "Proper leverage of relevant frameworks"
    context_isolation: "Clean separation without pollution"
    
  coordination_level_validation:
    results_consistency: "Cross-agent validation and verification"
    integration_quality: "Clean consolidation without conflicts"
    completeness_assessment: "Comprehensive coverage of requirements"
    
  system_level_validation:
    overall_quality: "Integrated results meet quality standards"
    performance_optimization: "Efficient resource usage and token management"
    continuous_improvement: "Meta-prompting integration for enhancement"
```

### Error Handling and Recovery Patterns

**Resilient Coordination**:

```yaml
error_recovery_patterns:
  agent_failure_handling:
    detection: "Agent timeout or error response"
    isolation: "Failure contained within agent context"
    recovery: "Fallback to alternative specialist or simplified approach"
    
  coordination_failure_handling:
    partial_results: "Integration of available results with gap identification"
    retry_strategies: "Re-attempt with different coordination pattern"
    graceful_degradation: "Simplified analysis when parallel processing fails"
    
  quality_failure_handling:
    constitutional_violation: "Automatic rejection and re-processing"
    consistency_conflicts: "Cross-agent validation and resolution"
    incomplete_coverage: "Additional specialist invocation for gaps"
```

## Performance Optimization Strategies

### Token Usage Optimization

```yaml
efficiency_patterns:
  sequential_optimization:
    benefit: "Lower token usage"
    tradeoff: "Longer execution time"
    use_case: "Cost-sensitive or simple workflows"
    
  parallel_optimization:
    benefit: "Faster completion"
    tradeoff: "Higher token usage (linear multiplication)"
    use_case: "Time-critical or complex analysis"
    
  adaptive_optimization:
    logic: "Dynamic selection based on task complexity and resource availability"
    simple_tasks: "Single specialist, minimal coordination"
    complex_tasks: "Parallel processing with comprehensive integration"
```

### Context Loading Efficiency

```yaml
context_optimization_patterns:
  progressive_loading:
    approach: "Load specialist context only when needed"
    benefit: "Reduced initial overhead"
    implementation: "Just-in-time specialist invocation"
    
  intelligent_caching:
    approach: "Cache frequently used specialist configurations"
    benefit: "Faster specialist initialization"
    implementation: "Framework-level configuration caching"
    
  context_compression:
    approach: "Optimize context representation for efficiency"
    benefit: "Reduced token usage per specialist"
    implementation: "Symbol-based state management"
```

## Success Metrics and Validation

### Coordination Effectiveness Metrics

```yaml
performance_indicators:
  task_completion_rate: "95%+ successful completion across all patterns"
  context_isolation_success: "100% main conversation focus preservation"
  quality_consistency: "95%+ constitutional AI compliance across all agents"
  resource_efficiency: "Optimal token usage for complexity level"
  integration_quality: "Clean consolidation without conflicts or gaps"
```

### Pattern Selection Criteria

```yaml
decision_framework:
  sequential_patterns:
    use_when: "Tasks have clear dependencies"
    benefits: "Lower token usage, logical progression"
    limitations: "Longer execution time"
    
  parallel_patterns:
    use_when: "Independent analysis required"
    benefits: "Faster completion, diverse perspectives"
    limitations: "Higher token usage"
    
  adaptive_patterns:
    use_when: "Complex or variable requirements"
    benefits: "Optimal resource allocation"
    limitations: "Higher coordination complexity"
```

---

**Pattern Categories**: Sequential, Parallel, Adaptive coordination  
**Maximum Concurrency**: 10 specialists with automatic queuing  
**Context Isolation**: Independent 200k contexts per specialist  
**Framework Integration**: Information-access, Research-orchestrator, Validation-systems

These usage patterns enable sophisticated multi-agent coordination while maintaining architectural constraints, context isolation, and quality standards for next-generation AI-assisted development workflows.