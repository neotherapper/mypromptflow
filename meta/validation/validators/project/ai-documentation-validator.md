# AI Documentation Validator

**AI Agent Instructions**: Validate AI-consumable documentation in project docs/ subfolders for effectiveness, actionability, and technical clarity.

## Validator Purpose

This validator ensures that documentation in `projects/*/docs/` directories is optimized for AI agent consumption, following technical documentation best practices and enabling effective AI-assisted implementation.

## Target Files

**Primary Scope**:
- `projects/*/docs/**/*.md` - All markdown files in project docs directories
- `projects/*/docs/**/*.yaml` - Configuration and specification files
- Focus on AI-consumable technical documentation (not human-oriented knowledge files)

**Documentation Categories**:
- **Architecture**: System design, technical specifications, data flow diagrams
- **Implementation**: Migration procedures, performance optimization, quality protocols  
- **Integration**: Enterprise scaling, security compliance, research findings integration
- **Testing**: Validation protocols, testing frameworks, quality assurance procedures
- **Workflows**: Operational procedures, automation patterns, process documentation

## Validation Criteria

### 1. AI Agent Actionability Assessment

**Technical Clarity (0-25 points)**:
- Clear, unambiguous technical instructions
- Specific implementation steps with executable commands
- Well-defined inputs, outputs, and transformation processes
- Minimal interpretation required for AI agent execution
- Technical precision without unnecessary complexity

**Implementation Guidance (0-25 points)**:
- Step-by-step procedures with validation checkpoints
- Clear success criteria and failure indicators  
- Error handling and recovery procedures documented
- Dependencies and prerequisites clearly specified
- Integration points with existing systems defined

### 2. Documentation Structure and Organization

**Information Architecture (0-20 points)**:
- Logical hierarchical organization (H1/H2/H3 structure)
- Consistent formatting and presentation patterns
- Clear section boundaries and content organization
- Effective use of code blocks, diagrams, and examples
- Appropriate use of tables, lists, and structured data

**Cross-Reference Integration (0-15 points)**:
- Proper @file_path references to related documentation
- Internal linking consistency within project docs
- Integration with project-level files (progress.md, task-list.md)
- Research findings integration with source attribution
- Bidirectional linking where appropriate

### 3. Technical Documentation Quality

**Code and Configuration Examples (0-10 points)**:
- Working code examples with proper syntax highlighting
- Configuration files with complete, valid structure
- Command-line examples with expected outputs
- API specifications with request/response examples
- Database schemas and data structure definitions

**Validation and Testing Procedures (0-5 points)**:
- Quality assurance checkpoints and validation criteria
- Testing procedures with expected outcomes
- Performance benchmarks and measurement approaches
- Security validation and compliance verification
- Integration testing and system validation procedures

## Validation Process

### Step 1: Documentation Discovery and Classification

```bash
# Discover AI-consumable documentation files
find projects/*/docs/ -type f \( -name "*.md" -o -name "*.yaml" \) | grep -v knowledge/

# Classify by documentation type and project
for file in discovered_files:
  project = extract_project_name(file)
  doc_category = classify_documentation_type(file)
  validate_ai_consumption_readiness(project, doc_category, file)
```

### Step 2: Content Analysis Workflow

```yaml
documentation_analysis:
  1. structure_validation:
     - Parse markdown structure and heading hierarchy
     - Validate consistent formatting patterns
     - Check section completeness and organization
     - Assess logical information flow
     
  2. actionability_assessment:
     - Identify executable instructions and procedures
     - Validate technical precision and clarity
     - Check implementation guidance completeness
     - Assess error handling and recovery documentation
     
  3. integration_validation:
     - Parse and validate @file_path references
     - Check cross-project integration patterns
     - Validate research findings integration
     - Assess framework compliance and consistency
     
  4. technical_quality_scoring:
     - Evaluate code examples and configurations
     - Validate API specifications and schemas
     - Check testing and validation procedures
     - Assess performance and security considerations
```

### Step 3: AI Consumption Effectiveness Testing

```yaml
ai_effectiveness_assessment:
  clarity_metrics:
    - Technical instruction ambiguity detection
    - Implementation step completeness validation
    - Prerequisite and dependency clarity assessment
    
  actionability_metrics:
    - Executable command validation and testing
    - Configuration file completeness and validity
    - Integration procedure step-by-step verification
    
  integration_metrics:
    - Cross-reference accuracy and accessibility
    - Framework pattern compliance validation
    - Research integration effectiveness assessment
```

## Validation Output Format

```yaml
ai_documentation_validation:
  project_name: "project-identifier"
  validation_date: "YYYY-MM-DD"
  docs_directory: "projects/project/docs/"
  
  category_analysis:
    architecture:
      files_count: 4
      average_score: 87
      issues_found: 2
      strengths:
        - "Clear system architecture diagrams with AI-parseable structure"
        - "Well-documented API specifications with complete examples"
      improvement_areas:
        - "Add validation checkpoints to data flow procedures"
        - "Include error handling for integration failure scenarios"
    
    implementation:
      files_count: 6
      average_score: 82
      issues_found: 3
      strengths:
        - "Comprehensive step-by-step migration procedures"
        - "Performance optimization with measurable benchmarks"
      improvement_areas:
        - "Add rollback procedures for failed migrations"
        - "Include specific validation criteria for optimization success"
    
    # Additional categories...
  
  file_level_analysis:
    - file_path: "projects/project/docs/architecture/system-architecture.md"
      category: "architecture"
      overall_score: 89
      subscores:
        technical_clarity: 24
        implementation_guidance: 22
        structure_organization: 18
        cross_reference_integration: 14
        technical_quality: 8
        validation_procedures: 3
      
      ai_consumption_assessment:
        actionability: "excellent"
        clarity: "excellent" 
        integration: "good"
        completeness: "good"
      
      specific_findings:
        strengths:
          - "Clear component interaction diagrams"
          - "Well-defined API contracts and data models"
          - "Excellent cross-referencing to implementation files"
        
        issues:
          - severity: "low"
            issue: "Missing error handling documentation for API failures"
            location: "## API Integration section"
            recommendation: "Add error codes and recovery procedures"
          
          - severity: "medium"
            issue: "Integration testing procedures not detailed"
            location: "## Validation section"
            recommendation: "Add specific integration test scenarios and expected outcomes"
    
    # Additional files...
  
  overall_assessment:
    project_ai_documentation_score: 85
    total_files_validated: 27
    critical_issues: 0
    medium_issues: 3
    low_issues: 8
    
    framework_compliance: "excellent"
    ai_consumption_readiness: "excellent"
    technical_documentation_quality: "good"
    
    top_recommendations:
      - "Add comprehensive error handling documentation across all implementation guides"
      - "Include specific validation criteria and success metrics for all procedures"
      - "Enhance integration testing documentation with concrete test scenarios"
      - "Standardize configuration examples across all architecture documents"
```

## Quality Scoring Framework

```yaml
scoring_criteria:
  excellent: 90-100 points
    - Highly actionable for AI agents with minimal interpretation
    - Comprehensive technical documentation with complete examples
    - Perfect cross-referencing and integration patterns
    - Complete validation and testing procedures
    
  good: 75-89 points
    - Generally actionable with minor clarification needed
    - Good technical documentation with most examples complete
    - Solid cross-referencing with minor gaps
    - Basic validation procedures present
    
  needs_improvement: 60-74 points
    - Requires significant interpretation for AI agent execution
    - Technical documentation present but incomplete examples
    - Cross-referencing inconsistent or partially broken
    - Limited validation and testing guidance
    
  critical_issues: <60 points
    - Major gaps in actionability for AI agents
    - Incomplete or incorrect technical documentation
    - Poor integration with project framework
    - Missing critical validation and error handling procedures
```

## Integration with Validation Framework

**Spawning Pattern**: Specialized AI documentation analysis via Task tool
**Authority Level**: Specialist Agent (Level 3)  
**Parallel Processing**: Safe for concurrent project analysis
**Dependencies**: Read access to project docs structure and related project files

**Integration with validate-pr.md**:
```yaml
conditional_activation:
  trigger_patterns:
    - "projects/*/docs/**/*.md"
    - "projects/*/docs/**/*.yaml"
  
  exclude_patterns:
    - "projects/*/knowledge/**/*" # Human-oriented documentation
    - "projects/*/docs/.meta/*"   # Metadata files
  
  spawning_command:
    description: "Validate AI-consumable documentation for effectiveness and actionability"
    prompt: "You are an AI Documentation Validator specialist. Analyze AI-consumable documentation files: {ai_docs_files_list}. Focus on technical clarity, implementation guidance, and AI agent actionability. Apply validation criteria for documentation structure, cross-reference integration, and technical quality. Generate comprehensive assessment with specific improvements for AI consumption effectiveness."
    context: "Project AI documentation files and technical documentation standards"
    expected_tokens: 100
```

## Success Criteria

**Documentation Effectiveness**:
- AI-consumable technical documentation achieves high actionability scores
- Implementation guidance enables successful AI-assisted development
- Cross-referencing provides reliable navigation and integration
- Technical examples and configurations are complete and validated

**Quality Improvements**:
- Consistent technical documentation patterns across projects
- Enhanced AI agent capability to execute implementation procedures
- Improved integration between documentation and project management files
- Reduced interpretation overhead for AI-assisted technical implementation

This validator ensures that AI-consumable technical documentation in project docs/ directories effectively supports AI-assisted development and implementation workflows within the mypromptflow framework.