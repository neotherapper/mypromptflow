# Agent Usage Guide: Unified Source Discovery Framework

## Quick Start: 5-Step Source Discovery

For immediate implementation, follow this simplified workflow:

### Step 1: Identify Your Topic
Extract the main research topic or validation context from your task.

### Step 2: Check for Specific Technology
- **If React, TypeScript, Python, Database, AI/LLM**: Use technology_mappings
- **If not**: Use category_mappings (frontend, backend, infrastructure, etc.)

### Step 3: Load Framework
Read `meta/information-access/source-discovery-framework.yaml`

### Step 4: Apply Source Selection Algorithm
Use `source_selection_algorithm.step_1_topic_analysis` → `step_2_mapping_selection` → `step_3_source_coordination`

### Step 5: Execute Multi-Source Access
Coordinate primary, supplementary, and validation sources with error handling.

---

## Complete Agent Implementation Guide

### Framework Integration Requirements

**CRITICAL**: Load the unified framework before any source discovery:

```yaml
framework_reference: "meta/information-access/source-discovery-framework.yaml"
integration_level: "mandatory"
applies_to: "ALL research and validation workflows"
```

### Topic Analysis & Technology Detection

#### Algorithm Application
```yaml
step_1_implementation:
  extract_technology_keywords:
    action: "Parse user request/file content for specific technologies"
    specific_technologies: ["react", "typescript", "python", "database", "ai_language_models"]
    example_detection:
      input: "Research React performance optimization"
      output: "technology=react, category=frontend"
      
  classify_domain_categories:
    action: "If no specific technology, identify broader domain"
    categories: ["frontend", "backend", "database", "infrastructure", "testing", "ai_integration"]
    example_classification:
      input: "API security best practices"
      output: "category=backend, domain=security"

  assess_complexity_level:
    simple: "Single technology, basic information needs"
    moderate: "Multiple related technologies, cross-domain analysis"
    complex: "Multiple domains, comprehensive research requirements"
```

#### Decision Logic Implementation
```yaml
technology_detection_patterns:
  react_detection:
    keywords: ["react", "jsx", "hooks", "components", "frontend framework"]
    file_patterns: ["*.tsx", "*.jsx", "component", "react-"]
    framework_mapping: "technology_mappings.react"
    
  typescript_detection:
    keywords: ["typescript", "ts", "type safety", "interfaces"]
    file_patterns: ["*.ts", "*.tsx", "tsconfig.json"]
    framework_mapping: "technology_mappings.typescript"
    
  python_detection:
    keywords: ["python", "django", "flask", "fastapi", "backend", "api"]
    file_patterns: ["*.py", "requirements.txt", "pyproject.toml"]
    framework_mapping: "technology_mappings.python"
    
  database_detection:
    keywords: ["database", "sql", "postgresql", "mysql", "mongodb", "data"]
    file_patterns: ["*.sql", "migration", "model", "schema"]
    framework_mapping: "technology_mappings.database"
    
  category_fallback:
    condition: "No specific technology detected"
    action: "Use category_mappings based on domain patterns"
```

### Mapping Selection & Source Coordination

#### Priority Hierarchy Implementation
```yaml
mapping_selection_logic:
  priority_1_specific_technology:
    condition: "topic matches technology_mappings keys"
    action: "Load technology_mappings[detected_technology]"
    example: "React research → technology_mappings.react"
    benefits: "Authoritative sources, role-aware contexts, comprehensive validation"
    
  priority_2_category_match:
    condition: "topic matches category_mappings.patterns"
    action: "Load best matching category_mappings"
    example: "Frontend optimization → category_mappings.frontend"
    benefits: "Broad coverage, flexible source selection"
    
  priority_3_knowledge_vault_fallback:
    condition: "No specific or category match"
    action: "Query knowledge-vault for available sources"
    implementation: "Use information-sources-by-type view with topic keywords"
    benefits: "Comprehensive fallback, extensible"
```

#### Source Coordination Patterns
```yaml
source_coordination_implementation:
  sequential_access:
    use_case: "Sources with dependencies or authentication requirements"
    pattern: "Primary → Supplementary → Validation"
    example: "MCP server setup → GitHub search → Documentation validation"
    
  parallel_access:
    use_case: "Independent sources for comprehensive coverage"
    pattern: "Simultaneous access to GitHub, Context7, WebFetch"
    example: "React research using GitHub repos + Context7 docs + React.dev simultaneously"
    
  conditional_access:
    use_case: "Sources activated based on intermediate findings"
    pattern: "Base research → conditional deep-dive sources"
    example: "General AI research → specific Claude/OpenAI sources if needed"
```

### Practical Implementation Examples

#### Example 1: React Performance Research
```yaml
user_request: "Research React performance optimization techniques"

step_1_topic_analysis:
  extracted_keywords: ["react", "performance", "optimization"]
  detected_technology: "react"
  domain_classification: "frontend"
  complexity_assessment: "moderate"

step_2_mapping_selection:
  selected_mapping: "technology_mappings.react"
  rationale: "Specific React technology detected"
  
step_3_source_coordination:
  primary_sources:
    - name: "mcp-github"
      access_pattern: "mcp__MCP_DOCKER__search_repositories"
      query: "language:JavaScript,TypeScript stars:>1000 react performance"
      
    - name: "context7-docs"
      access_pattern: "mcp__MCP_DOCKER__get-library-docs"
      library_id: "/vercel/next.js"
      
  supplementary_sources:
    - name: "react-performance-docs"
      access_pattern: "WebFetch"
      url: "https://react.dev/learn/render-and-commit"
      
  validation_sources:
    - name: "knowledge-vault-react"
      access_pattern: "Read"
      file_path: "knowledge-vault/knowledge/technologies/react/react-frontend-dev.md"

agent_implementation:
  # Load framework
  framework_data: "Read meta/information-access/source-discovery-framework.yaml"
  
  # Extract React mapping
  react_mapping: "framework_data.technology_mappings.react"
  
  # Execute coordinated access
  parallel_execution:
    - "Execute mcp__MCP_DOCKER__search_repositories with React performance query"
    - "Execute mcp__MCP_DOCKER__get-library-docs for Next.js documentation"
    - "Execute WebFetch for official React performance docs"
    
  # Apply to research context
  research_integration: "Use sources for step_3_5_discover_information_sources in research orchestrator"
```

#### Example 2: Database Design Analysis
```yaml
user_request: "Analyze database design patterns for microservices"

step_1_topic_analysis:
  extracted_keywords: ["database", "design", "patterns", "microservices"]
  detected_categories: ["database", "backend"]
  complexity_assessment: "moderate"

step_2_mapping_selection:
  selected_mappings: 
    - "category_mappings.database"
    - "category_mappings.backend"
  rationale: "No specific database technology, use categorical approach"

step_3_source_coordination:
  primary_sources:
    - name: "database-mcp-servers"
      access_pattern: "Grep"
      pattern: "database|sql|mongo|redis"
      path: "knowledge-vault/databases/tools_services/"
      
    - name: "database-repositories"
      access_pattern: "mcp__MCP_DOCKER__search_repositories"
      query: "topic:database OR topic:sql microservices"

agent_implementation:
  # Load framework
  framework_data: "Read meta/information-access/source-discovery-framework.yaml"
  
  # Apply category mappings
  database_sources: "framework_data.category_mappings.database.sources"
  backend_sources: "framework_data.category_mappings.backend.sources"
  
  # Coordinate source access
  source_discovery_sequence:
    1. "Grep knowledge-vault for available database MCP servers"
    2. "Search GitHub for database design pattern repositories"
    3. "WebSearch for microservices database design documentation"
    4. "Validate findings against knowledge-vault database expertise"
```

### Research Framework Integration

#### Research Orchestrator Enhancement
```yaml
integration_point: "research/orchestrator/integration/claude-orchestrator-integration.yaml"
step_enhancement: "step_3_5_discover_information_sources"

enhanced_implementation:
  before_orchestrator:
    - "Load meta/information-access/source-discovery-framework.yaml"
    - "Apply source_selection_algorithm to research topic"
    - "Prepare coordinated source access plan"
    
  during_orchestrator:
    - "Replace basic source discovery with unified framework results"
    - "Use technology_mappings for specific technology research"
    - "Apply category_mappings for broader domain research"
    - "Coordinate with knowledge-vault for comprehensive coverage"
    
  method_integration:
    multi_agent_coordination:
      - "Assign specific sources to specialized sub-agents"
      - "Coordinate parallel source access across sub-agents"
      - "Apply source attribution tracking for research-sources.md"
```

#### Research Quality Enhancement
```yaml
quality_improvements:
  source_diversity:
    target: "Minimum 3 different source types per research topic"
    measurement: "Count unique access patterns used"
    enforcement: "Framework ensures primary + supplementary + validation sources"
    
  coverage_completeness:
    target: "Primary + supplementary + validation sources for critical technologies"
    measurement: "Source category coverage percentage"
    enforcement: "Technology_mappings provide comprehensive source categories"
    
  accuracy_validation:
    cross_source_validation: "Information consistency across framework sources"
    credibility_scoring: "Framework provides source authority ratings"
    attribution_tracking: "Complete source documentation with timestamps"
```

### AI-PR Validation Integration

#### Role-Aware Source Selection
```yaml
pr_validation_enhancement:
  role_coordination:
    architect_role:
      sources: "technology_mappings[tech].pr_validation_context.architect_role"
      knowledge: "technology_mappings[tech].pr_validation_context.knowledge_sources[0]"
      
    frontend_dev_role:
      sources: "technology_mappings[tech].pr_validation_context.frontend_dev_role"
      knowledge: "technology_mappings[tech].pr_validation_context.knowledge_sources[1]"
      
    performance_role:
      sources: "technology_mappings[tech].pr_validation_context.performance_role"
      knowledge: "technology_mappings[tech].pr_validation_context.knowledge_sources[2]"
      
    security_role:
      sources: "technology_mappings[tech].pr_validation_context.security_role"
      knowledge: "technology_mappings[tech].pr_validation_context.knowledge_sources[3]"

agent_implementation_pattern:
  file_analysis:
    - "Detect file type using unified framework detection algorithms"
    - "Load appropriate technology_mappings or category_mappings"
    - "Spawn role-specific agents with framework-coordinated sources"
    - "Apply source attribution to validation findings"
```

### Error Handling & Fallback Procedures

#### MCP Server Availability Issues
```yaml
error_handling_implementation:
  mcp_server_unavailable:
    detection: "MCP tool call returns connection error"
    action: "Switch to WebSearch/WebFetch alternatives from same mapping"
    example: "GitHub MCP down → WebSearch for repository information"
    logging: "Record in meta/mcp-learning/error-logs/"
    
  authentication_failure:
    detection: "MCP tool returns authentication error"
    action: "Use non-authenticated sources from same category"
    notification: "Inform user about authentication requirements for full access"
    fallback: "Framework provides alternative source paths"
    
  rate_limiting:
    detection: "Rate limit response from external APIs"
    action: "Coordinate request timing across sources"
    fallback: "Switch to alternative sources in same category"
    prevention: "Use framework rate limiting coordination"
```

#### Mapping Gaps & Unknown Technologies
```yaml
unknown_technology_handling:
  detection: "Topic doesn't match any technology_mappings keys"
  action: "Use closest category_mappings match"
  enhancement: "Create specific mapping for future use"
  example: "Svelte framework → use category_mappings.frontend"
  
no_category_match:
  detection: "No category patterns match the topic"
  action: "Use knowledge-vault fallback query"
  implementation: "Query information-sources-by-type view with topic keywords"
  coverage: "Ensure minimum 3-source diversity"
```

### Decision Trees for Agent Implementation

#### Framework Activation Decision
```yaml
framework_activation_decision:
  always_use_framework:
    conditions:
      - "Research task detected"
      - "PR validation workflow"
      - "Multi-source information needs"
      - "Technology-specific analysis required"
    
  framework_selection_logic:
    if_specific_technology:
      condition: "React, TypeScript, Python, Database, AI detected"
      action: "Use technology_mappings"
      confidence: "high"
      
    if_domain_category:
      condition: "Frontend, backend, infrastructure patterns detected"
      action: "Use category_mappings"
      confidence: "medium"
      
    if_uncertain:
      condition: "Ambiguous topic or mixed domains"
      action: "Use knowledge_vault_fallback"
      confidence: "low"
```

#### Source Coordination Decision
```yaml
coordination_pattern_selection:
  sequential_coordination:
    use_when:
      - "MCP server setup required"
      - "Authentication dependencies exist"
      - "Source results inform subsequent sources"
    
  parallel_coordination:
    use_when:
      - "Independent source types"
      - "Time efficiency required"
      - "Comprehensive coverage needed"
    
  conditional_coordination:
    use_when:
      - "Source selection depends on intermediate findings"
      - "Complex multi-stage research"
      - "Adaptive source requirements"
```

### Quality Metrics & Success Validation

#### Implementation Quality Checks
```yaml
agent_quality_validation:
  framework_integration_completeness:
    check: "Verify framework loaded and mapping selected"
    target: "100% framework usage for research/validation tasks"
    
  source_diversity_achievement:
    check: "Count unique source types accessed"
    target: "≥3 different source types per topic"
    
  error_handling_effectiveness:
    check: "Verify fallback procedures executed on source failures"
    target: "100% graceful degradation on source errors"
    
  attribution_accuracy:
    check: "All sources properly documented with timestamps"
    target: "Complete source tracking for research-sources.md"
```

#### Performance Optimization
```yaml
efficiency_patterns:
  parallel_tool_execution:
    pattern: "Execute independent MCP tools simultaneously"
    example: "GitHub search + Context7 docs + WebFetch in parallel"
    benefit: "50-75% time reduction for multi-source coordination"
    
  smart_caching:
    pattern: "Cache framework mappings for session reuse"
    implementation: "Load framework once, reuse mappings for multiple topics"
    benefit: "Reduced file I/O for repeated source discovery"
    
  early_termination:
    pattern: "Stop source discovery when sufficient coverage achieved"
    trigger: "High-confidence sources provide comprehensive coverage"
    benefit: "Avoid over-engineering source coordination"
```

---

## Agent Implementation Checklist

### Before Using Framework
- [ ] Load `meta/information-access/source-discovery-framework.yaml`
- [ ] Extract topic/technology from user request or file analysis
- [ ] Check MCP server availability using `meta/mcp-learning/usage-guides/`

### During Framework Application
- [ ] Apply `source_selection_algorithm.step_1_topic_analysis`
- [ ] Select appropriate mapping (technology_mappings vs category_mappings)
- [ ] Coordinate source access using selected coordination pattern
- [ ] Implement error handling and fallback procedures

### After Source Discovery
- [ ] Validate source diversity (≥3 different source types)
- [ ] Document all sources for attribution tracking
- [ ] Apply sources to research orchestrator or PR validation workflow
- [ ] Update MCP learning guides with any new patterns or errors

### Integration Validation
- [ ] Verify research orchestrator uses framework sources
- [ ] Confirm PR validation agents use role-aware source selection
- [ ] Check cross-reference accuracy (100% file path accessibility)
- [ ] Validate quality metrics meet framework targets

---

This guide enables AI agents to effectively leverage the unified source discovery framework for consistent, comprehensive, and reliable information access across all research and validation workflows.