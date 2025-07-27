# Multi-Role Analysis Patterns - AI Agent Knowledge

## Role Differentiation Matrix Framework

Apply specialized analysis patterns across four core roles for comprehensive code evaluation and validation.

### Core Role Definitions

**Role Specialization Architecture**:
```yaml
role_hierarchy:
  architect:
    primary_focus: "System design, architecture patterns, scalability"
    analysis_weight: "High for structure, Medium for implementation details"
    key_concerns: ["Component architecture", "Integration patterns", "System scalability", "Code organization"]
    
  frontend_dev:
    primary_focus: "User experience, implementation quality, accessibility"
    analysis_weight: "High for UX, High for component implementation"
    key_concerns: ["User experience", "Accessibility", "Component quality", "Browser compatibility"]
    
  performance:
    primary_focus: "Runtime efficiency, optimization, resource usage"
    analysis_weight: "High for performance metrics, Medium for code structure"
    key_concerns: ["Bundle optimization", "Runtime performance", "Memory usage", "Loading efficiency"]
    
  security:
    primary_focus: "Vulnerability detection, security compliance, risk assessment"
    analysis_weight: "High for security risks, High for data protection"
    key_concerns: ["Vulnerability detection", "Authentication security", "Data protection", "Input validation"]
```

### Role-Specific Analysis Dimensions

**Architect Analysis Framework**:
```yaml
architect_analysis:
  component_architecture:
    weight: 35%
    evaluation_criteria:
      - "Component composition and hierarchy"
      - "Props interface design and type safety"
      - "State management patterns and consistency"
      - "Component reusability and modularity"
      
  system_integration:
    weight: 30%
    evaluation_criteria:
      - "Module dependency structure and organization"
      - "API integration patterns and error handling"
      - "Service layer architecture and separation"
      - "Configuration management and environment handling"
      
  scalability_assessment:
    weight: 20%
    evaluation_criteria:
      - "Code organization for team collaboration"
      - "Maintainability and extensibility patterns"
      - "Performance architecture considerations"
      - "Testing architecture and coverage strategy"
      
  technical_quality:
    weight: 15%
    evaluation_criteria:
      - "Type safety and interface definitions"
      - "Error handling and edge case management"
      - "Documentation quality and completeness"
      - "Code consistency and style adherence"
```

**Frontend Developer Analysis Framework**:
```yaml
frontend_dev_analysis:
  user_experience:
    weight: 40%
    evaluation_criteria:
      - "User interface design and interaction patterns"
      - "Accessibility implementation and ARIA compliance"
      - "Responsive design and cross-device compatibility"
      - "User feedback and error state handling"
      
  implementation_quality:
    weight: 30%
    evaluation_criteria:
      - "React patterns and hook usage correctness"
      - "Component lifecycle management"
      - "Event handling and state updates"
      - "Form handling and validation patterns"
      
  browser_compatibility:
    weight: 20%
    evaluation_criteria:
      - "Cross-browser functionality testing"
      - "Progressive enhancement implementation"
      - "Feature detection and fallback strategies"
      - "CSS compatibility and vendor prefixes"
      
  code_maintainability:
    weight: 10%
    evaluation_criteria:
      - "Component testability and isolation"
      - "Code readability and organization"
      - "Naming conventions and documentation"
      - "Refactoring potential and technical debt"
```

**Performance Specialist Analysis Framework**:
```yaml
performance_analysis:
  runtime_efficiency:
    weight: 35%
    evaluation_criteria:
      - "Component rendering optimization"
      - "Memory usage patterns and leak prevention"
      - "Algorithm efficiency and computational complexity"
      - "Event handler performance and optimization"
      
  bundle_optimization:
    weight: 30%
    evaluation_criteria:
      - "Code splitting implementation and effectiveness"
      - "Tree shaking and dead code elimination"
      - "Import optimization and bundle size impact"
      - "Lazy loading and dynamic imports usage"
      
  loading_performance:
    weight: 25%
    evaluation_criteria:
      - "Critical path optimization and resource prioritization"
      - "Asset loading strategies and caching implementation"
      - "Progressive loading and skeleton states"
      - "Third-party dependency impact assessment"
      
  monitoring_integration:
    weight: 10%
    evaluation_criteria:
      - "Performance monitoring setup and metrics"
      - "Error tracking and performance alerting"
      - "User experience metrics collection"
      - "Performance budget compliance"
```

**Security Specialist Analysis Framework**:
```yaml
security_analysis:
  vulnerability_detection:
    weight: 35%
    evaluation_criteria:
      - "Input validation and sanitization patterns"
      - "XSS prevention and output encoding"
      - "SQL injection and NoSQL injection prevention"
      - "Authentication and session management security"
      
  data_protection:
    weight: 30%
    evaluation_criteria:
      - "Sensitive data handling and encryption"
      - "API security and secure communication"
      - "Data exposure prevention and privacy compliance"
      - "Logging security and information disclosure"
      
  access_control:
    weight: 25%
    evaluation_criteria:
      - "Authorization implementation and role management"
      - "Route protection and access validation"
      - "API endpoint security and rate limiting"
      - "Token management and secure storage"
      
  dependency_security:
    weight: 10%
    evaluation_criteria:
      - "Third-party library vulnerability assessment"
      - "Dependency update strategy and security patches"
      - "Supply chain security and package verification"
      - "License compliance and security implications"
```

### Focus Level Indicators

**Focus Level Matrix**:
```yaml
focus_indicators:
  high_focus: "🔥"  # Primary area of expertise and responsibility
  medium_focus: "⚡"  # Secondary area with relevant expertise
  low_focus: "💭"   # Awareness level, limited detailed analysis
  
role_focus_mapping:
  component_architecture:
    architect: "🔥"      # Primary expertise in system design
    frontend_dev: "⚡"   # Secondary focus on component implementation
    performance: "💭"    # Awareness of performance implications
    security: "💭"      # Awareness of security architecture
    
  user_experience:
    architect: "💭"      # Awareness of UX impact on architecture
    frontend_dev: "🔥"   # Primary expertise in UX implementation
    performance: "⚡"    # Secondary focus on UX performance
    security: "💭"      # Awareness of security UX implications
    
  performance_optimization:
    architect: "⚡"      # Secondary focus on performance architecture
    frontend_dev: "⚡"   # Secondary focus on UX performance
    performance: "🔥"    # Primary expertise in optimization
    security: "💭"      # Awareness of security performance trade-offs
    
  security_compliance:
    architect: "💭"      # Awareness of security architecture
    frontend_dev: "💭"   # Awareness of client-side security
    performance: "💭"    # Awareness of security performance impact
    security: "🔥"      # Primary expertise in security assessment
```

### Cross-Role Analysis Coordination

**Consensus Building Framework**:
```yaml
consensus_mechanisms:
  issue_severity_agreement:
    threshold: "≥75% role agreement on critical issues"
    escalation: "Manual review if <75% consensus on high-severity issues"
    
  recommendation_prioritization:
    weight_distribution:
      architect: "25% weight on system design recommendations"
      frontend_dev: "25% weight on UX and implementation recommendations"
      performance: "25% weight on optimization recommendations"
      security: "25% weight on security recommendations"
      
  conflict_resolution:
    security_priority: "Security concerns override other considerations"
    performance_vs_ux: "Balance based on user impact assessment"
    architecture_vs_implementation: "Long-term maintainability prioritized"
```

**Multi-Role Validation Matrix**:
```yaml
validation_matrix:
  cross_role_checks:
    architect_security: "Validate architectural security patterns"
    frontend_performance: "Validate UX performance impact"
    performance_security: "Validate optimization security implications"
    security_frontend: "Validate security UX implementation"
    
  role_handoff_patterns:
    architect_to_specialist: "Design decisions inform implementation analysis"
    specialist_to_architect: "Implementation issues inform design refinement"
    cross_specialist: "Shared concerns require coordinated analysis"
```

### Analysis Outcome Integration

**Role-Specific Verdict Format**:
```yaml
verdict_structure:
  role_assessment:
    verdict: "APPROVED | CONDITIONAL | NEEDS_WORK | CRITICAL"
    confidence: "0-100% confidence in assessment"
    summary: "Concise role-specific evaluation summary"
    
  detailed_findings:
    strengths: ["Positive findings in role domain"]
    concerns: ["Areas requiring attention or improvement"]
    critical_issues: ["Issues requiring immediate attention"]
    recommendations: ["Specific actionable improvements"]
    
  context_information:
    analysis_scope: "Specific areas analyzed by role"
    methodology: "Analysis approach and criteria used"
    limitations: "Constraints or assumptions in analysis"
```

**Integrated Assessment Generation**:
```yaml
assessment_integration:
  weighted_scoring:
    overall_score: "Composite score across all role assessments"
    role_contributions: "Individual role score contributions"
    consensus_indicators: "Agreement levels across roles"
    
  comprehensive_recommendations:
    priority_matrix: "Recommendations ranked by priority and role expertise"
    implementation_guidance: "Step-by-step improvement roadmap"
    timeline_estimates: "Effort estimates for each recommendation"
    
  quality_assurance:
    cross_validation: "Role assessment consistency checks"
    completeness_verification: "Ensure all critical areas covered"
    accuracy_validation: "Validate assessment against known patterns"
```

### Implementation Patterns

**Role Context Loading**:
```yaml
context_loading_strategy:
  role_specific_knowledge:
    architect: "REQUEST_CONTEXT(typescript-architect, react-architect)"
    frontend_dev: "REQUEST_CONTEXT(react-frontend-dev, accessibility-patterns)"
    performance: "REQUEST_CONTEXT(react-performance, optimization-techniques)"
    security: "REQUEST_CONTEXT(react-security, vulnerability-detection)"
    
  adaptive_context:
    technology_detection: "Load relevant technology contexts based on file analysis"
    complexity_scaling: "Adjust context depth based on code complexity"
    domain_specialization: "Include domain-specific patterns when detected"
```

**Analysis Coordination Workflow**:
```yaml
coordination_workflow:
  initialization:
    - "Assign roles based on file type and complexity analysis"
    - "Load appropriate contexts for each role"
    - "Establish communication channels for cross-role coordination"
    
  parallel_analysis:
    - "Execute role-specific analysis in parallel"
    - "Share critical findings across roles in real-time"
    - "Coordinate on overlapping concerns and dependencies"
    
  result_synthesis:
    - "Aggregate role-specific assessments and recommendations"
    - "Resolve conflicts using consensus building mechanisms"
    - "Generate integrated assessment with priority matrix"
    - "Produce actionable recommendations with role attribution"
```

**Quality Validation**:
```yaml
quality_checks:
  role_coverage:
    completeness: "Verify all critical areas covered by appropriate roles"
    expertise_alignment: "Ensure role expertise matches analysis areas"
    gap_detection: "Identify potential analysis gaps or overlaps"
    
  assessment_quality:
    accuracy_validation: "Cross-check assessments against known patterns"
    consistency_verification: "Ensure consistent evaluation criteria application"
    bias_detection: "Identify and mitigate potential assessment biases"
    
  recommendation_quality:
    actionability: "Ensure recommendations are specific and implementable"
    prioritization: "Validate priority assignments and rationale"
    completeness: "Verify comprehensive coverage of identified issues"
```

This knowledge base provides AI agents with comprehensive understanding of multi-role analysis patterns, enabling them to coordinate effectively across specialist roles while maintaining quality and consistency in code evaluation and validation processes.