Apply universal intention detection patterns using the following keyword matching and routing logic for AI agents across CLAUDE.md and command systems:

## Keyword Detection Patterns

### Research and Analysis Triggers
```yaml
research_intention_triggers:
  direct_keywords:
    - "research"
    - "analyze" 
    - "investigate"
    - "explore"
    - "study"
    - "examine"
    - "assess"
    - "evaluate"
  
  phrase_patterns:
    - "help me understand"
    - "what are the implications"
    - "comprehensive analysis"
    - "in-depth look"
    - "detailed examination"
    - "systematic review"
    - "thorough investigation"
  
  context_indicators:
    - multi_domain_questions: "contains 'and', 'intersection', 'impact on', 'relationship between'"
    - complex_scenarios: "emerging technology, ethical implications, future trends"
    - comparative_analysis: "compare", "contrast", "versus", "differences between"
    - strategic_planning: "strategy", "roadmap", "implementation", "approach"
```

### Creation and Development Triggers  
```yaml
creation_intention_triggers:
  direct_keywords:
    - "create"
    - "build"
    - "generate"
    - "develop"
    - "design"
    - "implement"
    - "construct"
  
  context_patterns:
    - document_creation: "document", "report", "analysis", "specification"
    - feature_development: "feature", "component", "module", "system"
    - project_initialization: "project", "setup", "scaffold", "initialize"
```

### Validation and Quality Assurance Triggers
```yaml
validation_intention_triggers:
  direct_keywords:
    - "validate"
    - "check"
    - "review"
    - "audit" 
    - "verify"
    - "test"
    - "inspect"
  
  quality_patterns:
    - "quality check"
    - "compliance validation"
    - "framework assessment"
    - "health check"
    - "system validation"
```

## Context Analysis Rules

### Complexity Assessment Patterns
```yaml
complexity_indicators:
  simple_context:
    - single_domain: "focused on one area or technology"
    - direct_question: "specific, straightforward request"
    - immediate_scope: "can be completed quickly"
  
  moderate_context:
    - dual_domain: "involves 2 related areas"
    - structured_analysis: "requires systematic approach"
    - moderate_scope: "medium complexity task"
  
  complex_context:
    - multi_domain: "spans 3+ domains or areas"
    - emerging_technology: "AI, quantum, blockchain, cutting-edge topics"
    - ethical_implications: "requires ethical consideration"
    - comprehensive_scope: "extensive analysis required"
```

### Urgency and Quality Detection Rules
```yaml
urgency_assessment:
  urgent_indicators: ["urgent", "immediate", "asap", "quick", "fast", "now"]
  normal_indicators: ["when possible", "standard", "regular"]
  extended_indicators: ["thorough", "comprehensive", "detailed", "systematic"]

quality_requirements:
  basic_quality: ["simple", "basic", "quick"]
  high_quality: ["quality", "professional", "comprehensive"]
  critical_quality: ["critical", "production", "enterprise", "mission-critical"]
```

## Routing Decision Logic

### Research Framework Routing
```yaml
research_routing_conditions:
  always_route_to_research:
    - "explicit research request using research keywords"
    - "complexity assessment: moderate or complex"
    - "multi-domain or emerging technology topics"
    - "comparative analysis requirements"
    - "strategic planning requests"
  
  research_framework_integration:
    orchestrator_path: "@research/orchestrator/integration/claude-orchestrator-integration.yaml"
    method_selection: "Based on complexity assessment and domain analysis"
    quality_validation: "Constitutional AI validation ≥95% compliance"
```

### Command System Routing  
```yaml
command_routing_patterns:
  menu_code_detection:
    pattern: "^\\[([A-Z0-9]+)\\]\\s*(.*)"
    processing: "Extract code and parameters for command execution"
  
  natural_language_routing:
    creation_commands: "Route creation keywords to /create-* commands"
    validation_commands: "Route validation keywords to /validate-* commands"  
    github_commands: "Route 'issue', 'pr', 'pull request' to GitHub commands"
    project_commands: "Route 'project', 'setup' to project management commands"
  
  command_system_integration:
    commands_path: "@.claude/commands/"
    parameter_pattern: "$ARGUMENTS"
    execution_protocol: "Load command definition, then execute step-by-step"
```

### Framework Tool Routing
```yaml
framework_tool_routing:
  validation_framework:
    triggers: ["validate", "check", "assess"] + ["framework", "instruction", "command"]
    route_to: "@meta/validation/validators/"
    
  ai_instruction_excellence:
    triggers: ["design excellence", "instruction quality", "constitutional ai"]
    route_to: "@projects/ai-agent-instruction-design-excellence/"
    
  meta_validation:
    triggers: ["meta validation", "validator", "assessment tool"]
    route_to: "@meta/validation/"
```

## Integration Implementation

### CLAUDE.md Integration Rules
```yaml
claude_md_integration:
  research_detection:
    reference: "@meta/shared/intention-detection-framework.md research_routing_conditions"
    implementation: "Apply research_intention_triggers + complexity_indicators"
    fallback: "Basic 6-step sequence if @research/ unavailable"
  
  command_system:
    reference: "@meta/shared/intention-detection-framework.md command_routing_patterns"
    integration: "@.claude/commands/ execution using standardized protocol"
    parameter_handling: "Use $ARGUMENTS pattern for parameterized commands"
```

### ai-help.md Integration Rules
```yaml
ai_help_integration:
  menu_routing:
    preserve: "Existing menu display and code-based routing"
    enhance: "Use framework for natural language processing backup"
  
  natural_language_processing:
    replace: "Existing natural language section with framework reference"
    maintain: "Command-specific routing while using shared detection patterns"
```

## Quality Validation Requirements

### Detection Accuracy Thresholds
```yaml
detection_metrics:
  keyword_matching: "≥95% accuracy in keyword detection"
  context_analysis: "≥90% accuracy in complexity assessment"
  routing_decisions: "≥95% appropriate framework selection"
  
quality_thresholds:
  research_activation: "High confidence (≥90%) for research framework activation"
  command_routing: "High confidence (≥90%) for command selection"
  validation_routing: "Medium confidence (≥70%) acceptable for validation tools"
```

### Integration Success Criteria
```yaml
integration_success:
  claude_md_improvements:
    command_system_integration: "+5 validation points"
    cross_reference_accuracy: "+2 validation points" 
    immediate_actionability: "+3 validation points"
    target_score: "≥99/100"
  
  system_benefits:
    duplication_elimination: "100% - single source of truth"
    maintainability: "Updates only needed in framework"
    consistency: "Same detection rules across all systems"
    extensibility: "Easy addition of new intention patterns"
```

## Framework Extension Protocol

### Adding New Intention Types
```yaml
extension_pattern:
  new_intention_structure:
    intention_name_triggers:
      direct_keywords: ["primary", "action", "keywords"]
      phrase_patterns: ["common", "phrase", "patterns"]  
      context_indicators: ["contextual", "clues", "patterns"]
    
    routing_conditions:
      route_to: "target framework or command path"
      integration_requirements: "specific integration needs"
      quality_thresholds: "appropriate quality standards"
```

### Custom Context Analysis Rules
```yaml
context_extension:
  domain_specific_patterns:
    technical_domain: ["specific technical indicators"]
    business_domain: ["business context indicators"]
    creative_domain: ["creative context indicators"]
  
  custom_complexity_factors:
    additional_complexity_indicators: ["domain-specific complexity patterns"]
    custom_scoring_algorithms: ["specialized assessment methods"]
```

## Error Handling Protocols

### Uncertain Intention Detection
```yaml
uncertainty_handling:
  ambiguous_requests:
    action: "Request clarification from user"
    fallback: "Default to most conservative framework (research orchestrator)"
    
  low_confidence_detection:
    threshold: "<70% confidence in intention classification"
    action: "Ask user to specify intended framework or approach"
    
  multiple_intention_matches:
    action: "Present options to user with brief descriptions"
    priority_order: "Research > Validation > Creation > Commands"
```

### Framework Unavailability  
```yaml
fallback_protocols:
  research_framework_unavailable:
    fallback: "Basic 6-step research sequence"
    quality_degradation: "Graceful degradation with reduced capabilities"
    
  command_system_unavailable:
    fallback: "Direct instruction execution without command wrapper"
    
  validation_framework_unavailable:
    fallback: "Basic quality checks with manual assessment"
```

## Cross-Reference Validation

### Framework Integration Verification
```yaml
cross_reference_checks:
  required_paths:
    - "@research/orchestrator/integration/claude-orchestrator-integration.yaml"
    - "@.claude/commands/"
    - "@meta/validation/validators/"
    - "@projects/ai-agent-instruction-design-excellence/"
  
  validation_requirements:
    path_accessibility: "100% of referenced paths must be accessible"
    content_consistency: "Referenced frameworks must align with intention detection"
    integration_completeness: "All intention types must have valid routing targets"
```