# Integration Examples: Framework Usage in Real Workflows

## Research Orchestrator Integration Examples

### Example 1: React Performance Research with Multi-Agent Method

**User Request**: "Research React performance optimization techniques for large applications"

#### Framework Integration Flow
```yaml
step_3_5_discover_information_sources:
  # 1. Load unified framework
  framework_data: "Read meta/information-access/source-discovery-framework.yaml"
  
  # 2. Apply topic analysis
  topic_analysis:
    extracted_keywords: ["react", "performance", "optimization", "large applications"]
    detected_technology: "react"
    complexity_assessment: "moderate"
    
  # 3. Load React technology mapping
  react_mapping: "framework_data.technology_mappings.react"
  
  # 4. Extract coordinated sources
  coordinated_sources:
    primary:
      - name: "mcp-github"
        access_pattern: "mcp__MCP_DOCKER__search_repositories"
        query: "language:JavaScript,TypeScript stars:>1000 react performance optimization"
        rationale: "Official and community React performance projects"
        
      - name: "context7-docs"
        access_pattern: "mcp__MCP_DOCKER__get-library-docs"
        library_id: "/vercel/next.js"
        rationale: "Comprehensive React framework documentation"
        
    supplementary:
      - name: "react-docs"
        access_pattern: "WebFetch"
        url: "https://react.dev/learn/render-and-commit"
        rationale: "Official React performance documentation"
        
      - name: "knowledge-vault-react"
        access_pattern: "Read"
        file_path: "knowledge-vault/knowledge/technologies/react/react-performance.md"
        rationale: "Internal React performance expertise"
        
    validation:
      - name: "official-react-docs"
        access_pattern: "WebFetch"
        url: "https://react.dev/reference/react"
        rationale: "Official React API documentation for accuracy"

  # 5. Multi-agent source coordination
  sub_agent_coordination:
    performance_specialist:
      assigned_sources:
        - "mcp-github (React performance repositories)"
        - "knowledge-vault-react (performance-specific content)"
      specialization: "Bundle optimization, rendering performance, memory usage"
      
    react_architect:
      assigned_sources:
        - "context7-docs (Next.js architecture patterns)"
        - "official-react-docs (React API patterns)"
      specialization: "Component architecture, state management patterns"
      
    frontend_optimizer:
      assigned_sources:
        - "react-docs (rendering optimization)"
        - "mcp-github (real-world optimization examples)"
      specialization: "User experience optimization, accessibility"
```

#### Practical Agent Implementation
```yaml
# Multi-agent method execution with framework sources
research_execution:
  spawn_sub_agents:
    - name: "React Performance Specialist"
      task_prompt: |
        Research React performance optimization focusing on:
        - Bundle size optimization and code splitting
        - Rendering performance and virtual DOM efficiency
        - Memory usage patterns and optimization
        
        Use these coordinated sources:
        - Execute: mcp__MCP_DOCKER__search_repositories with query "language:JavaScript,TypeScript stars:>1000 react performance optimization"
        - Read: knowledge-vault/knowledge/technologies/react/react-performance.md
        - Document findings in research/findings/react-performance-optimization/research/performance-specialist-analysis.md
        
    - name: "React Architecture Analyst"
      task_prompt: |
        Analyze React architectural patterns for large applications:
        - Component composition and reusability patterns
        - State management architecture (Context, Redux, Zustand)
        - Module organization and dependency management
        
        Use these coordinated sources:
        - Execute: mcp__MCP_DOCKER__get-library-docs with library_id "/vercel/next.js"
        - Execute: WebFetch with url "https://react.dev/reference/react"
        - Document findings in research/findings/react-performance-optimization/research/architecture-analyst-findings.md
        
    - name: "Frontend Experience Optimizer"
      task_prompt: |
        Research user experience optimization for React applications:
        - Accessibility patterns and performance impact
        - Progressive loading and user feedback patterns
        - Error boundary and loading state management
        
        Use these coordinated sources:
        - Execute: WebFetch with url "https://react.dev/learn/render-and-commit"
        - Execute: mcp__MCP_DOCKER__search_repositories with query "react accessibility performance"
        - Document findings in research/findings/react-performance-optimization/research/ux-optimizer-insights.md

  comprehensive_synthesis:
    file: "research/findings/react-performance-optimization/research/comprehensive-analysis.md"
    integration: "Combine all sub-agent findings with cross-validation"
    source_attribution: "Complete source tracking in research-sources.md"
```

### Example 2: Database Architecture Research with Knowledge Vault Fallback

**User Request**: "Research database design patterns for microservices with event sourcing"

#### Framework Integration Flow
```yaml
step_3_5_discover_information_sources:
  # 1. Load framework and analyze topic
  topic_analysis:
    extracted_keywords: ["database", "design", "patterns", "microservices", "event sourcing"]
    detected_categories: ["database", "backend", "infrastructure"]
    complexity_assessment: "complex"
    no_specific_technology: true
    
  # 2. Apply category mappings (no specific database technology)
  selected_mappings:
    - "category_mappings.database"
    - "category_mappings.backend"
    - "category_mappings.infrastructure"
    
  # 3. Coordinate multi-category sources
  coordinated_sources:
    primary:
      - name: "database-mcp-servers"
        access_pattern: "Grep"
        pattern: "database|sql|mongo|redis|event"
        path: "knowledge-vault/databases/tools_services/"
        rationale: "Available database MCP servers for direct access"
        
      - name: "microservices-repositories"
        access_pattern: "mcp__MCP_DOCKER__search_repositories"
        query: "topic:microservices topic:database event-sourcing"
        rationale: "Real-world microservices database patterns"
        
    supplementary:
      - name: "database-design-patterns"
        access_pattern: "WebSearch"
        query: "database design patterns microservices event sourcing CQRS"
        rationale: "Comprehensive pattern documentation"
        
      - name: "infrastructure-best-practices"
        access_pattern: "WebSearch"
        query: "microservices database infrastructure patterns scalability"
        rationale: "Infrastructure scaling considerations"
        
    validation:
      - name: "academic-sources"
        access_pattern: "WebSearch"
        query: "event sourcing database patterns research papers"
        rationale: "Academic validation of patterns"

  # 4. Knowledge vault fallback coordination
  knowledge_vault_fallback:
    trigger: "Complex multi-domain topic requiring comprehensive coverage"
    implementation:
      - query_pattern: "information-sources-by-type view with microservices + database keywords"
      - tag_filtering: "tag:database AND tag:architecture AND complexity_score:<=4"
      - authentication_filtering: "Prioritize non-authenticated sources for rapid access"
```

---

## AI-PR Validation Integration Examples

### Example 3: TypeScript React Component Validation

**PR Context**: TypeScript React component files with performance optimization changes

#### Framework-Enhanced File Type Detection
```yaml
file_analysis:
  detected_files:
    - path: "src/components/DataTable.tsx"
      type: "typescript_react"
      change_type: "modified"
      lines_added: 45
      lines_removed: 12
      
  # Framework integration for role-aware analysis
  framework_integration:
    technology_detected: ["react", "typescript"]
    framework_mappings: 
      - "technology_mappings.react"
      - "technology_mappings.typescript"
    
  # Extract role-aware contexts from framework
  role_contexts:
    architect_context:
      framework_source: "technology_mappings.react.pr_validation_context.architect_role"
      knowledge_sources: 
        - "technology_mappings.react.pr_validation_context.knowledge_sources[0]"
        - "technology_mappings.typescript.pr_validation_context.knowledge_sources[0]"
      information_sources:
        - "technology_mappings.react.sources.primary"
        - "technology_mappings.typescript.sources.primary"
        
    frontend_dev_context:
      framework_source: "technology_mappings.react.pr_validation_context.frontend_dev_role"
      knowledge_sources:
        - "technology_mappings.react.pr_validation_context.knowledge_sources[1]"
      focus_areas: ["Component implementation", "User experience", "React patterns"]
      
    performance_context:
      framework_source: "technology_mappings.react.pr_validation_context.performance_role"
      knowledge_sources:
        - "technology_mappings.react.pr_validation_context.knowledge_sources[2]"
      focus_areas: ["Bundle optimization", "Rendering performance", "Memory usage"]
      
    security_context:
      framework_source: "technology_mappings.react.pr_validation_context.security_role"
      knowledge_sources:
        - "technology_mappings.react.pr_validation_context.knowledge_sources[3]"
      focus_areas: ["XSS prevention", "Secure coding", "Dependency vulnerabilities"]
```

#### Multi-Role Agent Spawning with Framework Sources
```yaml
validation_agents:
  typescript_react_architect:
    context_loading: "REQUEST_CONTEXT(typescript-architect, react-architect)"
    framework_sources:
      # Coordinated information access using framework
      - access_pattern: "mcp__MCP_DOCKER__search_repositories"
        query: "language:TypeScript stars:>1000 react component architecture"
        rationale: "React TypeScript architectural patterns"
        
      - access_pattern: "mcp__MCP_DOCKER__get-library-docs"
        library_id: "/vercel/next.js"
        rationale: "Next.js TypeScript integration patterns"
        
      - access_pattern: "Read"
        file_path: "knowledge-vault/knowledge/technologies/react/react-architect.md"
        rationale: "Internal React architecture expertise"
        
    validation_focus:
      - "TypeScript type architecture and inference patterns"
      - "React component composition and state management"
      - "Module dependency structure and integration patterns"
      
  react_performance_specialist:
    context_loading: "REQUEST_CONTEXT(react-performance, typescript-performance)"
    framework_sources:
      # Framework coordinates performance-specific sources
      - access_pattern: "WebFetch"
        url: "https://react.dev/learn/render-and-commit"
        rationale: "Official React performance documentation"
        
      - access_pattern: "mcp__MCP_DOCKER__search_repositories"
        query: "react performance optimization bundle typescript"
        rationale: "Performance optimization examples"
        
      - access_pattern: "Read"
        file_path: "knowledge-vault/knowledge/technologies/react/react-performance.md"
        rationale: "Internal React performance expertise"
        
    validation_focus:
      - "Component re-render optimization and memoization"
      - "Bundle size impact and code splitting effectiveness"
      - "TypeScript compilation impact on performance"
      
  frontend_security_specialist:
    context_loading: "REQUEST_CONTEXT(react-security, typescript-security)"
    framework_sources:
      # Security-focused source coordination
      - access_pattern: "WebSearch"
        query: "React TypeScript security patterns XSS prevention"
        rationale: "React security best practices"
        
      - access_pattern: "Read"
        file_path: "knowledge-vault/knowledge/technologies/react/react-security.md"
        rationale: "Internal React security patterns"
        
    validation_focus:
      - "XSS prevention and input sanitization"
      - "TypeScript type safety for security"
      - "Dependency vulnerability assessment"
```

### Example 4: Python Backend API Validation

**PR Context**: Python Flask API with authentication and database integration

#### Framework-Enhanced Multi-Role Validation
```yaml
file_analysis:
  detected_files:
    - path: "api/auth/routes.py"
      type: "python_backend"
      patterns: ["flask", "jwt", "authentication"]
      
  framework_integration:
    technology_detected: "python"
    framework_mapping: "technology_mappings.python"
    category_overlap: ["backend", "database"]
    
  coordinated_validation:
    python_backend_architect:
      framework_sources:
        - access_pattern: "mcp__MCP_DOCKER__search_repositories"
          query: "language:Python stars:>1000 flask api architecture"
          rationale: "Flask API architectural patterns"
          
        - access_pattern: "WebSearch"
          query: "Python Flask API design patterns authentication"
          rationale: "API design best practices"
          
        - access_pattern: "Read"
          file_path: "meta/information-access/topic-mappings/python-sources.yaml"
          rationale: "Python-specific information source mappings"
          
      validation_focus:
        - "API endpoint organization and versioning"
        - "Authentication architecture and JWT patterns"
        - "Database integration and ORM usage"
        
    backend_security_specialist:
      framework_sources:
        - access_pattern: "WebSearch"
          query: "Python Flask security best practices authentication vulnerabilities"
          rationale: "Flask security patterns"
          
        - access_pattern: "WebFetch"
          url: "https://flask.palletsprojects.com/en/latest/security/"
          rationale: "Official Flask security documentation"
          
      validation_focus:
        - "SQL injection prevention and input validation"
        - "JWT token security and session management"
        - "CORS configuration and API security headers"
```

---

## Error Handling Integration Examples

### Example 5: MCP Server Failure Recovery

**Scenario**: GitHub MCP server unavailable during React research

#### Framework-Guided Fallback Implementation
```yaml
error_handling_flow:
  initial_attempt:
    action: "mcp__MCP_DOCKER__search_repositories"
    query: "language:JavaScript react performance"
    result: "Connection refused - MCP server unavailable"
    
  framework_fallback:
    # Load framework mapping for alternatives
    react_mapping: "technology_mappings.react.sources"
    fallback_sources: "react_mapping.supplementary + react_mapping.validation"
    
    alternative_execution:
      - access_pattern: "WebSearch"
        query: "site:github.com react performance optimization"
        rationale: "Web-based GitHub search as MCP alternative"
        
      - access_pattern: "WebFetch"
        url: "https://react.dev/learn/render-and-commit"
        rationale: "Official React documentation for performance"
        
      - access_pattern: "Read"
        file_path: "knowledge-vault/knowledge/technologies/react/react-frontend-dev.md"
        rationale: "Internal React knowledge as reliable fallback"
        
  error_logging:
    file: "meta/mcp-learning/error-logs/github-mcp-errors.md"
    entry: |
      **Error**: GitHub MCP server unavailable
      **Date**: 2025-07-28
      **Fallback**: WebSearch + WebFetch + knowledge-vault
      **Success**: Yes - comprehensive information obtained
      **Pattern**: Use framework supplementary sources when primary MCP fails
```

### Example 6: Authentication Recovery for Context7 Docs

**Scenario**: Context7 library documentation requires authentication

#### Framework-Guided Authentication Handling
```yaml
authentication_handling:
  initial_attempt:
    action: "mcp__MCP_DOCKER__get-library-docs"
    library_id: "/vercel/next.js"
    result: "Authentication required"
    
  framework_response:
    # Use framework authentication complexity assessment
    auth_complexity: "technology_mappings.react.sources.primary[1].authentication_complexity"
    fallback_strategy: "Use non-authenticated sources from same category"
    
    alternative_sources:
      - access_pattern: "WebFetch"
        url: "https://nextjs.org/docs"
        rationale: "Official Next.js documentation (public access)"
        
      - access_pattern: "WebSearch"
        query: "Next.js React documentation best practices"
        rationale: "Community documentation and tutorials"
        
      - access_pattern: "Read"
        file_path: "knowledge-vault/knowledge/technologies/react/react-frontend-dev.md"
        rationale: "Internal React knowledge including Next.js patterns"
        
  user_notification:
    message: "Context7 library docs require authentication. Using alternative sources for comprehensive coverage."
    setup_guidance: "For full Context7 access, configure authentication in MCP settings"
```

---

## Task Completion Integration Examples

### Example 7: Research Task Completion with Framework Attribution

**Scenario**: Completing React performance research with full source tracking

#### Framework-Enhanced Task Completion Protocol
```yaml
task_completion_with_framework:
  step_1_todo_update:
    status: "completed"
    framework_metrics:
      source_diversity_achieved: "4 different source types"
      framework_mapping_used: "technology_mappings.react"
      coordination_pattern: "parallel"
      error_recovery_events: "1 (GitHub MCP fallback successful)"
      
  step_6_framework_validation:
    source_attribution_complete:
      research_sources_md: "research/findings/react-performance-optimization/.meta/research-sources.md"
      framework_sources_documented:
        - "GitHub repositories (via mcp__MCP_DOCKER__search_repositories)"
        - "Context7 Next.js docs (via mcp__MCP_DOCKER__get-library-docs)"
        - "Official React docs (via WebFetch)"
        - "Internal knowledge vault (via Read)"
        
    framework_integration_verified:
      orchestrator_integration: "✓ Used unified framework for step_3_5_discover_information_sources"
      quality_metrics: "✓ Achieved ≥3 source types, comprehensive coverage"
      error_handling: "✓ Successfully recovered from MCP server failure"
      cross_validation: "✓ Sources cross-validated for consistency"
```

---

## Quality Metrics Integration

### Comprehensive Quality Validation Example
```yaml
framework_quality_validation:
  source_diversity_metrics:
    target: "≥3 different source types per research topic"
    achieved: 
      - "mcp-servers: 2 (GitHub, Context7)"
      - "web-sources: 2 (WebFetch, WebSearch)"
      - "internal-sources: 1 (knowledge-vault)"
      - "total-diversity: 5 source types ✓"
      
  coverage_completeness_metrics:
    target: "Primary + supplementary + validation sources"
    achieved:
      - "primary: mcp__MCP_DOCKER__search_repositories + mcp__MCP_DOCKER__get-library-docs"
      - "supplementary: WebFetch(official docs) + Read(knowledge-vault)"
      - "validation: WebFetch(reference docs) + WebSearch(community validation)"
      - "completeness: 100% ✓"
      
  integration_success_metrics:
    research_framework: "✓ Seamless orchestrator step_3_5 integration"
    pr_validation: "✓ Role-aware source coordination for validation agents"
    knowledge_vault: "✓ Effective fallback query performance"
    
  accuracy_validation_metrics:
    cross_source_validation: "✓ Information consistency across 5 sources"
    credibility_scoring: "✓ Framework authority ratings applied"
    attribution_tracking: "✓ Complete source documentation with timestamps"
```

---

These integration examples demonstrate how the unified source discovery framework seamlessly enhances both research orchestrator workflows and AI-PR validation systems, providing consistent, comprehensive, and reliable information access across all AI agent operations.