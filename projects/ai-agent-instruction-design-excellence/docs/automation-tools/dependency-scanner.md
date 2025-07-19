# External Dependency Scanner

## Purpose

Automated detection and classification of external dependencies in instruction files to accelerate framework assessment while maintaining accuracy and preventing fictional assessments.

## Anti-Fiction Validation Requirements

**CRITICAL**: This tool requires actual file analysis - no estimation or guessing permitted.

- ✅ **MUST read and analyze the actual target instruction file**
- ✅ **MUST apply pattern recognition to real file content**  
- ✅ **MUST document findings with specific line references**
- ✅ **MUST classify dependencies using documented criteria**
- ❌ **CANNOT estimate dependency levels without file analysis**
- ❌ **CANNOT create fictional dependency scores**

## Automated Dependency Detection Patterns

### Framework References (Score: 4 points each)
```regex
Pattern Set A: Specific AI Frameworks
- \b(SuperClaude|Claude.Flow|ClaudeFlow)\b
- \b(Gemini.Pro|GPT-4|ChatGPT)\b
- \b(LangChain|LlamaIndex|AutoGPT)\b

Pattern Set B: Generic Framework References
- \b(AI.framework|machine.learning.framework)\b
- \b(natural.language.processing|NLP.framework)\b
- \b(cognitive.architecture|agent.framework)\b

Pattern Set C: Proprietary Systems
- \b(internal.system|company.framework)\b
- \b(proprietary.solution|custom.framework)\b
- \b(enterprise.platform|organization.system)\b
```

### External APIs (Score: 3 points each)
```regex
Pattern Set D: Web APIs
- \b(REST.API|GraphQL.API|web.service)\b
- \b(external.API|third.party.API|remote.service)\b
- \b(API.endpoint|service.endpoint|web.endpoint)\b

Pattern Set E: Cloud Services
- \b(AWS|Azure|Google.Cloud|GCP)\b
- \b(cloud.service|cloud.platform|cloud.API)\b
- \b(serverless|lambda|cloud.function)\b

Pattern Set F: Database/Storage APIs
- \b(database.API|storage.API|data.service)\b
- \b(MongoDB|PostgreSQL|Redis|Elasticsearch)\b
- \b(file.storage|object.storage|data.lake)\b
```

### Documentation Dependencies (Score: 2 points each)
```regex
Pattern Set G: External Documentation
- \b(documentation|manual|guide|handbook)\b
- \b(reference.material|external.docs|online.docs)\b
- \b(specification|standard|protocol)\b

Pattern Set H: Industry Standards
- \b(industry.standard|best.practice|standard.protocol)\b
- \b(ISO.standard|IEEE.standard|W3C.standard)\b
- \b(compliance.standard|regulatory.standard)\b

Pattern Set I: Knowledge Requirements
- \b(domain.knowledge|subject.matter.expert|specialized.knowledge)\b
- \b(prior.experience|background.knowledge|expertise)\b
- \b(training.required|certification.needed)\b
```

### Research Requirements (Score: 1 point each)
```regex
Pattern Set J: Information Gathering
- \b(research|investigate|analyze|study)\b
- \b(web.search|google|search.engine|online.search)\b
- \b(current.information|latest.data|up.to.date)\b

Pattern Set K: External Validation
- \b(verify|validate|confirm|check)\b
- \b(cross.reference|compare.with|benchmark.against)\b
- \b(peer.review|expert.opinion|external.validation)\b
```

## Dependency Classification Algorithm

### Dependency Scoring Formula
```yaml
calculation_method:
  total_words: count(all_words_in_file)
  dependency_points: (framework_refs * 4) + (external_apis * 3) + (documentation_deps * 2) + (research_reqs * 1)
  dependency_density: dependency_points / total_words * 100
  
severity_thresholds:
  critical: dependency_density >= 12.0
  high: dependency_density >= 8.0
  medium: dependency_density >= 4.0
  low: dependency_density >= 1.0
  minimal: dependency_density < 1.0
```

### Dependency Type Analysis
```yaml
dependency_classification:
  framework_dependencies:
    definition: "References to external AI frameworks or systems"
    impact: "Blocks execution without framework access"
    self_sufficiency_impact: "Critical - requires framework inclusion"
    
  api_dependencies:
    definition: "Requirements for external services or APIs"
    impact: "Limits portability and increases failure points"
    self_sufficiency_impact: "High - requires API documentation/mocking"
    
  documentation_dependencies:
    definition: "References to external documentation or standards"
    impact: "Reduces instruction completeness and accessibility"
    self_sufficiency_impact: "Medium - requires context inclusion"
    
  research_dependencies:
    definition: "Requirements for external information gathering"
    impact: "Introduces variability and time delays"
    self_sufficiency_impact: "Low - can be mitigated with specific guidance"
```

## Automated Replacement Suggestions

### Framework Reference Replacements
```yaml
framework_replacements:
  "SuperClaude patterns":
    concrete_alternatives:
      - "token optimization techniques: [specific methods listed]"
      - "hierarchical coordination steps: [numbered procedures]"
      - "quality gates: [defined checkpoints with criteria]"
    replacement_method: "Extract and embed specific techniques"
    
  "Claude Flow methodology":
    concrete_alternatives:
      - "agent spawning procedure: [step-by-step process]"
      - "task distribution algorithm: [specific logic]"
      - "coordination protocol: [defined communication patterns]"
    replacement_method: "Document concrete behaviors"
    
  "industry best practices":
    concrete_alternatives:
      - "established patterns: [specific examples provided]"
      - "proven methods: [documented approaches with references]"
      - "validated techniques: [specific implementations described]"
    replacement_method: "Include specific practice definitions"
```

### API Dependency Replacements
```yaml
api_replacements:
  "external API":
    concrete_alternatives:
      - "mock API responses: [example data structures]"
      - "API interface definition: [complete specification]"
      - "fallback procedures: [offline operation methods]"
    replacement_method: "Provide complete API specifications"
    
  "web service":
    concrete_alternatives:
      - "service interface contract: [detailed specification]"
      - "example request/response: [complete samples]"
      - "error handling procedures: [specific scenarios]"
    replacement_method: "Include service definitions"
    
  "cloud platform":
    concrete_alternatives:
      - "platform-agnostic implementation: [generic approach]"
      - "containerized solution: [Docker-based implementation]"
      - "local development setup: [self-contained environment]"
    replacement_method: "Eliminate platform lock-in"
```

### Documentation Dependency Replacements
```yaml
documentation_replacements:
  "refer to documentation":
    concrete_alternatives:
      - "embedded reference: [relevant content included]"
      - "summary of key points: [essential information extracted]"
      - "quick reference guide: [condensed version provided]"
    replacement_method: "Embed essential content"
    
  "industry standard":
    concrete_alternatives:
      - "standard requirements: [specific criteria listed]"
      - "compliance checklist: [detailed validation steps]"
      - "implementation guidelines: [concrete procedures]"
    replacement_method: "Include standard definitions"
```

## Automated Quality Gates

### Dependency Threshold Gates
```yaml
quality_gates:
  gate_1_critical:
    condition: dependency_density >= 12.0
    action: "BLOCK - Instruction has excessive external dependencies"
    message: "Critical dependency level. Apply self-sufficiency framework before assessment."
    
  gate_2_high:
    condition: dependency_density >= 8.0
    action: "WARNING - Significant external dependencies detected"
    message: "High dependency level. Consider self-sufficiency improvements."
    
  gate_3_acceptable:
    condition: dependency_density < 4.0
    action: "PASS - Acceptable dependency level for assessment"
    message: "Dependencies within acceptable range for self-sufficient instruction."
```

### Self-Sufficiency Analysis
```yaml
self_sufficiency_assessment:
  portability_score:
    calculation: "100 - (dependency_density * 5)"
    interpretation:
      excellent: "> 90 - Highly portable instruction"
      good: "70-90 - Moderately portable with minor dependencies"
      fair: "50-70 - Some portability concerns"
      poor: "< 50 - Significant portability issues"
      
  execution_independence:
    framework_independence: "Can execute without external frameworks"
    api_independence: "Can execute without external services"
    documentation_independence: "Contains all necessary context"
    research_independence: "No external information gathering required"
```

## Integration with Anti-Fiction Protocol

### Mandatory Validation Checkpoints
```yaml
validation_checkpoints:
  checkpoint_1_file_analysis:
    verify: "Actual file content analyzed for dependencies"
    evidence_required:
      - file_path_documented: true
      - line_numbers_referenced: true
      - exact_dependency_text_quoted: true
      - pattern_matches_documented: true
    
  checkpoint_2_classification_verification:
    verify: "Dependencies classified using documented criteria"
    evidence_required:
      - classification_logic_shown: true
      - scoring_calculation_documented: true
      - threshold_application_verified: true
      - replacement_suggestions_provided: true
    
  checkpoint_3_self_sufficiency_analysis:
    verify: "Self-sufficiency impact assessed systematically"
    evidence_required:
      - portability_score_calculated: true
      - independence_factors_evaluated: true
      - improvement_recommendations_specific: true
```

## Usage Instructions for AI Agents

### Step-by-Step Automation Workflow

```yaml
workflow_steps:
  step_1_preparation:
    action: "Load target instruction file and initialize dependency tracking"
    time_estimate: "5-10 seconds"
    validation: "Confirm file content accessible and dependency patterns loaded"
    
  step_2_pattern_scanning:
    action: "Apply all dependency detection patterns systematically"
    time_estimate: "20-30 seconds"
    validation: "Document each pattern match with line reference and type"
    
  step_3_classification:
    action: "Classify dependencies by type and calculate impact scores"
    time_estimate: "15-20 seconds"
    validation: "Show classification logic and scoring calculation"
    
  step_4_self_sufficiency_assessment:
    action: "Calculate portability score and independence factors"
    time_estimate: "10-15 seconds"
    validation: "Document assessment criteria and threshold application"
    
  step_5_replacement_suggestions:
    action: "Generate concrete replacement suggestions for identified dependencies"
    time_estimate: "20-30 seconds"
    validation: "Provide specific alternatives based on dependency type"
```

### Context-Aware Dependency Analysis
```yaml
context_analysis:
  orchestrator_instructions:
    common_dependencies: ["SuperClaude", "Claude Flow", "agent frameworks"]
    replacement_focus: "Embed specific coordination patterns and procedures"
    
  specialist_instructions:
    common_dependencies: ["domain APIs", "external data sources", "specialized tools"]
    replacement_focus: "Include tool specifications and data requirements"
    
  worker_instructions:
    common_dependencies: ["external services", "configuration files", "environment settings"]
    replacement_focus: "Provide complete execution environment definitions"
```

## Success Metrics

### Time Reduction Targets
```yaml
time_metrics:
  traditional_dependency_assessment:
    manual_dependency_identification: "1-2 minutes"
    manual_classification: "30-60 seconds"
    manual_impact_assessment: "1-2 minutes"
    total_traditional_time: "2.5-4.5 minutes"
    
  automated_dependency_assessment:
    automated_pattern_detection: "20-30 seconds"
    automated_classification: "15-20 seconds"
    automated_impact_assessment: "10-15 seconds"
    total_automated_time: "45-65 seconds"
    
  time_reduction_achieved: "70-75% reduction in dependency assessment time"
```

### Accuracy Validation
```yaml
accuracy_requirements:
  dependency_detection_accuracy: ">95% compared to manual identification"
  classification_accuracy: ">90% correct dependency type assignment"
  self_sufficiency_assessment_accuracy: ">85% alignment with expert evaluation"
  replacement_suggestion_relevance: ">80% actionable and appropriate suggestions"
```

## Error Prevention

### Common Assessment Errors Prevented
```yaml
error_prevention:
  missed_dependencies:
    prevention: "Comprehensive pattern coverage across all dependency types"
    validation: "All pattern sets applied systematically with documentation"
    
  incorrect_classification:
    prevention: "Automated classification based on documented criteria"
    validation: "Classification logic transparent and verifiable"
    
  fictional_self_sufficiency_scores:
    prevention: "Mathematical calculation based on actual dependency counts"
    validation: "No scores generated without documented pattern matches"
    
  inadequate_replacement_suggestions:
    prevention: "Type-specific replacement templates with concrete alternatives"
    validation: "Suggestions mapped to specific dependency types and contexts"
```

This external dependency scanner automates the identification and assessment of instruction dependencies, reducing assessment time by 70-75% while maintaining rigorous accuracy standards and preventing fictional results.