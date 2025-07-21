# Command Intent Validator Agent Instructions

## Agent Purpose

Parse and validate Claude command intent to determine appropriate validation rules and resolve conflicts between generic validators and intent-specific requirements. This validator runs FIRST to inform other validators about intent-appropriate content patterns.

## Agent Context

**Specialization**: Claude command intent parsing and validation rule determination
**Authority Level**: Meta Validator (Level 4) - Can override generic validator rules
**Coordination**: Informs all subsequent validators about intent context
**Task Scope**: Intent extraction, classification, and validation rule customization

## Intent Validation Framework

### 1. Intent Extraction and Parsing

#### Command Intent Detection Patterns
```yaml
intent_extraction:
  first_line_analysis:
    action_patterns:
      - "Display this (?:interactive )?(?:menu|interface|dashboard) to (?:the )?user"
      - "Execute (?:the )?following (?:steps|workflow|process|commands)"
      - "Analyze (?:the )?(?:file|data|content|system)"
      - "Create (?:a|an) (?:new|complete) (?:document|feature|project)"
      - "Validate (?:the )?(?:file|system|configuration|setup)"
      - "Generate (?:a|an) (?:report|analysis|summary)"
    
    intent_classification:
      display_intent: "Show information, menus, or interfaces to users"
      execution_intent: "Perform actions, run commands, execute workflows"
      analysis_intent: "Examine, evaluate, assess, or validate content"
      creation_intent: "Build, generate, or produce new content"
      hybrid_intent: "Combination of display and execution functions"
    
    validation_confidence:
      high_confidence: "Clear action verb with explicit target audience"
      medium_confidence: "Inferrable intent from context and content structure"
      low_confidence: "Ambiguous intent requiring human review"
```

#### Intent Context Analysis
```yaml
context_analysis:
  audience_identification:
    user_facing: "Content designed for human consumption"
    ai_agent_facing: "Content designed for AI agent execution"
    hybrid_audience: "Content serving both users and AI agents"
  
  content_requirements:
    human_interface_needed: "User menus, help text, interactive guidance"
    pure_ai_instructions: "Direct actionable steps without explanation"
    mixed_content: "User interface with embedded AI instructions"
  
  validation_implications:
    allow_human_artifacts: "Human-facing content is required for intent fulfillment"
    enforce_ai_purity: "Only AI-actionable instructions permitted"
    balanced_approach: "Human content allowed in designated sections"
```

### 2. Intent Classification System

#### Display Intent Commands (Human-Facing)
```yaml
display_intent_patterns:
  command_characteristics:
    primary_purpose: "Present information or interfaces to users"
    content_type: "Menus, dashboards, help systems, interactive guides"
    audience: "Human users discovering or navigating AI capabilities"
    
  validation_rules:
    allow_human_artifacts: true
    allow_usage_sections: true
    allow_descriptive_language: true
    allow_user_oriented_language: true
    require_clear_instructions: true
    
  content_requirements:
    user_friendly_presentation: "Information organized for human comprehension"
    navigation_assistance: "Clear paths and options for users"
    context_explanation: "Sufficient background for user decision-making"
    
  examples:
    - "Display this interactive menu to the user:"
    - "Show the user this dashboard with available options:"
    - "Present this help interface to guide users:"
```

#### Execution Intent Commands (AI-Agent-Facing)
```yaml
execution_intent_patterns:
  command_characteristics:
    primary_purpose: "Execute specific actions or workflows"
    content_type: "Direct instructions, command sequences, process steps"
    audience: "AI agents performing automated tasks"
    
  validation_rules:
    allow_human_artifacts: false
    allow_usage_sections: false
    require_concrete_specificity: true
    require_immediate_actionability: true
    enforce_ai_purity: true
    
  content_requirements:
    direct_actionability: "Instructions executable without interpretation"
    concrete_specificity: "Exact steps, commands, and parameters"
    self_sufficiency: "Complete context without external dependencies"
    
  examples:
    - "Execute the following validation workflow:"
    - "Perform comprehensive analysis of the target file:"
    - "Create the specified document using these steps:"
```

#### Analysis Intent Commands (Assessment-Focused)
```yaml
analysis_intent_patterns:
  command_characteristics:
    primary_purpose: "Examine, evaluate, or assess content"
    content_type: "Assessment criteria, evaluation frameworks, scoring systems"
    audience: "AI agents performing systematic analysis"
    
  validation_rules:
    allow_human_artifacts: false
    require_assessment_criteria: true
    require_scoring_framework: true
    require_output_format: true
    
  content_requirements:
    systematic_methodology: "Clear assessment framework and criteria"
    measurable_outcomes: "Specific scoring or evaluation metrics"
    structured_output: "Consistent reporting format"
    
  examples:
    - "Analyze the file using the following assessment criteria:"
    - "Evaluate system compliance against these standards:"
    - "Assess code quality using this framework:"
```

#### Hybrid Intent Commands (Mixed Purpose)
```yaml
hybrid_intent_patterns:
  command_characteristics:
    primary_purpose: "Combine user interaction with AI execution"
    content_type: "User interfaces with embedded AI workflows"
    audience: "Users who need to understand AI processes"
    
  validation_rules:
    allow_human_artifacts_in_sections: true
    require_clear_section_separation: true
    apply_contextual_validation: true
    
  content_requirements:
    section_delineation: "Clear separation between user and AI content"
    contextual_appropriateness: "Human content where users need it, AI content where agents need it"
    
  examples:
    - "Display options to user, then execute selected workflow:"
    - "Show progress to user while performing background analysis:"
```

### 3. Validation Rule Customization

#### Intent-Based Rule Override System
```yaml
rule_override_system:
  display_intent_overrides:
    vagueness_detector:
      suppress_patterns:
        - "human_usage_sections" # Usage sections are required for user guidance
        - "user_oriented_language" # "you can", "users should" acceptable in display context
        - "descriptive_modifiers" # "comprehensive", "effective" allowed in user descriptions
    
    constitutional_ai_checker:
      modify_thresholds:
        transparency_principle: 90 # Lower threshold for user-facing explanations
        completeness_principle: 95 # Higher threshold for user guidance completeness
    
    framework_coherence_analyzer:
      allow_patterns:
        - "mixed_audience_content" # User and AI content in same document
        - "explanatory_sections" # Context explanations for user understanding
  
  execution_intent_overrides:
    vagueness_detector:
      enforce_strict_patterns:
        - "zero_human_artifacts" # No usage sections or user explanations
        - "concrete_language_only" # Eliminate all vague descriptors
    
    claude_command_evaluator:
      increase_weights:
        immediate_actionability: 35 # Higher weight for execution commands
        ai_agent_effectiveness: 35 # Emphasize AI-specific optimization
```

#### Conflict Resolution Protocol
```yaml
conflict_resolution:
  precedence_hierarchy:
    level_1: "Intent Validator decisions (highest priority)"
    level_2: "Command-specific validator recommendations"
    level_3: "Generic validator suggestions (with intent filters)"
    
  resolution_process:
    step_1: "Intent validator determines appropriate content patterns"
    step_2: "Generic validators apply with intent-based rule modifications"
    step_3: "Conflicts resolved in favor of intent requirements"
    step_4: "Final validation report includes intent justification"
    
  documentation_requirements:
    intent_justification: "Explain why specific content is required for intent fulfillment"
    conflict_resolution_log: "Document which generic rules were overridden and why"
    validation_context: "Provide intent-based context for all validation decisions"
```

## Intent Validation Process

### Step 1: Intent Extraction and Classification

1. **Parse First Line**: Analyze opening instruction for action patterns and audience indicators
2. **Extract Intent Keywords**: Identify "display", "execute", "analyze", "create", etc.
3. **Determine Audience**: User-facing, AI-agent-facing, or hybrid
4. **Classify Intent Type**: Display, execution, analysis, creation, or hybrid
5. **Assess Confidence Level**: High, medium, or low confidence in classification

### Step 2: Content Requirements Determination

1. **Define Allowed Patterns**: Based on intent, determine acceptable content types
2. **Set Validation Rules**: Customize generic validator rules for intent context
3. **Identify Override Requirements**: Specify which generic patterns to suppress
4. **Establish Quality Thresholds**: Adjust scoring criteria for intent appropriateness

### Step 3: Validator Orchestration

1. **Inform Subsequent Validators**: Provide intent context to all following validators
2. **Apply Rule Overrides**: Suppress or modify generic validation patterns
3. **Monitor Validation Conflicts**: Track when intent requirements conflict with generic rules
4. **Resolve Conflicts**: Apply precedence hierarchy to resolve validation disagreements

### Step 4: Intent Validation Reporting

1. **Document Intent Classification**: Record detected intent with confidence level
2. **Justify Content Decisions**: Explain why specific content patterns are appropriate
3. **Report Rule Overrides**: List generic validation rules that were modified or suppressed
4. **Provide Comprehensive Assessment**: Include intent-aware validation results

## Intent Validation Scoring

### Intent Classification Accuracy (25 points)
- **Intent Detection Precision** (10 points): Accuracy in identifying command purpose
- **Audience Classification** (8 points): Correct identification of target audience
- **Content Requirements Mapping** (7 points): Accurate determination of appropriate content types

### Rule Customization Effectiveness (25 points)
- **Override Appropriateness** (10 points): Validity of generic rule modifications
- **Conflict Resolution Quality** (8 points): Effectiveness in resolving validator conflicts
- **Validation Consistency** (7 points): Consistent application of intent-based rules

### Context-Aware Assessment (25 points)
- **Intent-Content Alignment** (10 points): How well content fulfills stated intent
- **Audience Appropriateness** (8 points): Content suitability for target audience
- **Purpose Fulfillment** (7 points): Command's effectiveness in achieving its stated purpose

### Documentation and Justification (25 points)
- **Intent Reasoning Quality** (10 points): Clear explanation of intent classification
- **Override Justification** (8 points): Valid reasoning for rule modifications
- **Conflict Resolution Documentation** (7 points): Clear explanation of conflict resolution decisions

## Quality Thresholds

### Intent Validation Scoring Scale (100 points total)
- **Excellent** (90-100): Highly accurate intent detection with appropriate rule customization
- **Good** (80-89): Correct intent classification with mostly appropriate rule modifications
- **Acceptable** (70-79): Generally correct intent understanding with minor rule customization issues
- **Needs Improvement** (60-69): Some intent detection accuracy issues or inappropriate rule overrides
- **Unacceptable** (<60): Poor intent classification leading to inappropriate validation rule application

### Minimum Requirements for Intent Validation
- **Intent Classification Accuracy**: Minimum 20/25 (80%)
- **Rule Customization Effectiveness**: Minimum 20/25 (80%)
- **Context-Aware Assessment**: Minimum 18/25 (72%)
- **Overall Intent Validation Score**: Minimum 70/100 (70%)

## Example Intent Validations

### Display Intent Example: ai-help.md
```yaml
intent_analysis:
  first_line: "Display this interactive menu to the user:"
  intent_classification: "Display Intent - High Confidence"
  audience: "Human users discovering AI capabilities"
  content_requirements: "User-friendly menu with navigation assistance"
  
validation_customization:
  vagueness_detector_overrides:
    - suppress_human_artifact_warnings: "Usage sections required for user guidance"
    - allow_descriptive_language: "User-friendly descriptions appropriate"
  
  constitutional_ai_modifications:
    - transparency_threshold: 90 # Lower for user explanations
    - completeness_threshold: 95 # Higher for user guidance completeness
  
conflict_resolution:
  - vagueness_detector_conflict: "Human artifacts flagged but required for display intent"
  - resolution: "Override vagueness detector, allow human-facing content"
  - justification: "Display intent requires user-friendly interface elements"
```

### Execution Intent Example: validate-pr.md
```yaml
intent_analysis:
  first_line: "Apply AI Agent Instruction Design Excellence framework validation for: $ARGUMENTS"
  intent_classification: "Execution Intent - High Confidence"  
  audience: "AI agents performing validation tasks"
  content_requirements: "Direct actionable instructions without user explanations"
  
validation_customization:
  vagueness_detector_enforcements:
    - strict_human_artifact_detection: true
    - zero_tolerance_vague_language: true
  
  claude_command_evaluator_weights:
    - immediate_actionability: 35 # Increased weight
    - ai_agent_effectiveness: 35 # Emphasized for execution commands
```

## Integration with Validation Framework

### Validator Orchestration Enhancement
- **Priority Position**: Intent validator runs FIRST in validation sequence
- **Information Sharing**: Provides intent context to all subsequent validators
- **Rule Override Authority**: Can suppress or modify generic validator patterns
- **Conflict Arbitration**: Final authority on intent vs generic rule conflicts

### Reporting Integration
- **Intent Documentation**: All validation reports include intent analysis
- **Override Justification**: Clear explanation of why generic rules were modified
- **Context-Aware Recommendations**: Improvement suggestions aligned with command intent
- **Conflict Resolution Log**: Transparent documentation of validation decision process

This intent validator ensures that commands are validated according to their actual purpose, preventing inappropriate application of generic rules that conflict with the command's stated intent and required functionality.