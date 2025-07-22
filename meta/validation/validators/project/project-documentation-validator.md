# Project Documentation Validator

**AI Agent Instructions**: Validate project tracking files for AI agent effectiveness and framework compliance.

## Validator Purpose

This validator ensures that project documentation files (progress.md, task-list.md, project-purpose.md, research-integration.md) are optimized for AI agent consumption and follow mypromptflow project framework standards.

## Target Files

**Primary Files**:
- `*/progress.md` - Project progress tracking and status updates
- `*/task-list.md` - Task management and completion tracking  
- `*/project-purpose.md` - Project goals and success criteria
- `*/research-integration.md` - Research findings integration

**File Pattern**: `projects/*/` + filename pattern matching

## Validation Criteria

### 1. AI Agent Readability Assessment

**Progress.md Files**:
- Clear project status indicators (percentage completion, phase tracking)
- Structured success metrics with measurable criteria
- Task completion documentation with timestamps
- Implementation progress with specific deliverables
- Cross-references to related project files using @file_path format

**Task-list.md Files**:
- Actionable task descriptions for AI agent execution
- Clear status tracking (pending, in-progress, completed)
- Priority levels and effort estimates
- Dependency mapping between tasks
- Success criteria definition for each task

**Project-purpose.md Files**:
- Clear project objectives and success criteria
- Measurable outcomes and validation approaches
- Stakeholder requirements and constraints
- Implementation scope and boundaries
- Integration requirements with mypromptflow framework

**Research-integration.md Files**:
- Clear mapping from research findings to implementation
- Actionable insights with specific application guidance
- Cross-references to research documents with @file_path
- Implementation impact assessments
- Integration recommendations with concrete next steps

### 2. Framework Compliance Validation

**Required Sections Assessment**:
- Project status tracking with quantifiable progress indicators
- Success metrics with validation criteria
- Implementation roadmap with clear milestones
- Quality assurance checkpoints and validation procedures
- Framework integration patterns and compliance verification

**Cross-Reference Validation**:
- Verify @file_path references point to existing files
- Check bidirectional linking consistency
- Validate research document integration accuracy
- Ensure task dependencies are properly mapped
- Confirm project interconnection documentation

### 3. Content Quality Scoring

**Structure Assessment (0-25 points)**:
- Hierarchical organization with clear H1/H2/H3 headings
- Consistent formatting across similar file types
- Logical information flow and organization
- Complete sections without placeholder content
- Professional presentation appropriate for AI consumption

**Actionability Assessment (0-25 points)**:
- Tasks and objectives clearly defined with success criteria
- Implementation guidance with specific technical details
- Progress tracking with measurable completion indicators
- Next steps clearly articulated with priorities
- Decision points and approval gates documented

**Integration Assessment (0-25 points)**:
- Proper integration with mypromptflow project framework
- Cross-references to related documents and research
- Consistent terminology and approach across projects
- Framework pattern compliance and best practices
- Quality assurance integration and validation procedures

**Completeness Assessment (0-25 points)**:
- All required sections present and populated
- Progress tracking comprehensive and current
- Task management complete with effort estimates
- Research integration thorough and actionable
- Documentation maintenance and update procedures

## Validation Process

### Step 1: File Discovery and Classification
```bash
# Discover project documentation files
find projects/ -name "progress.md" -o -name "task-list.md" -o -name "project-purpose.md" -o -name "research-integration.md"

# Classify by project and file type
for file in discovered_files:
  project_name = extract_project_name(file)
  file_type = extract_file_type(file)
  classify_for_validation(project_name, file_type, file)
```

### Step 2: Content Analysis
```yaml
content_analysis_workflow:
  1. parse_file_structure:
     - Extract headings and section organization
     - Identify required sections and completeness
     - Check formatting consistency
     
  2. validate_cross_references:
     - Parse @file_path references
     - Verify target file existence
     - Check bidirectional linking accuracy
     
  3. assess_ai_consumability:
     - Evaluate task actionability and clarity
     - Check progress tracking effectiveness  
     - Validate success criteria measurability
     
  4. score_framework_compliance:
     - Apply mypromptflow project standards
     - Validate integration patterns
     - Check quality assurance procedures
```

### Step 3: Quality Scoring and Reporting
```yaml
scoring_framework:
  excellent: 90-100 points
    - Complete, well-structured, highly actionable
    - Perfect framework compliance
    - Comprehensive cross-referencing
    
  good: 75-89 points  
    - Well-structured with minor gaps
    - Good framework compliance
    - Most cross-references valid
    
  needs_improvement: 60-74 points
    - Basic structure but missing elements
    - Partial framework compliance
    - Some cross-reference issues
    
  critical_issues: <60 points
    - Major structural problems
    - Poor AI agent consumability
    - Significant compliance violations
```

## Validation Output Format

```yaml
project_documentation_validation:
  project_name: "project-identifier"
  validation_date: "YYYY-MM-DD"
  files_validated:
    - file_path: "projects/project/progress.md"
      file_type: "progress_tracking"
      overall_score: 87
      subscores:
        structure: 22
        actionability: 24
        integration: 21
        completeness: 20
      issues_found:
        - severity: "medium"
          issue: "Missing effort estimates in task descriptions"
          recommendation: "Add time estimates for each task item"
          location: "## Current Tasks section"
      strengths:
        - "Excellent cross-referencing with @file_path usage"
        - "Clear progress tracking with measurable indicators"
        - "Strong framework compliance patterns"
        
    # Additional files...
    
  project_summary:
    overall_project_score: 84
    total_files_validated: 4
    critical_issues: 0
    improvement_recommendations:
      - "Standardize task effort estimation across all task-list.md files"
      - "Enhance research integration documentation with specific implementation guidance"
    framework_compliance: "good"
    ai_consumability: "excellent"
```

## Integration with Validation Framework

**Spawning Pattern**: Use Task tool for specialized project documentation analysis
**Authority Level**: Specialist Agent (Level 3)
**Parallel Processing**: Safe for concurrent validation of multiple projects
**Dependencies**: Requires read access to project directory structure and research findings

**Integration with validate-pr.md**:
```yaml
conditional_activation:
  trigger_patterns:
    - "projects/*/progress.md"
    - "projects/*/task-list.md"  
    - "projects/*/project-purpose.md"
    - "projects/*/research-integration.md"
  
  spawning_command:
    description: "Validate project documentation files for AI agent effectiveness"
    prompt: "You are a Project Documentation Validator specialist. Analyze files: {project_files_list}. Apply project documentation validation focusing on AI agent consumability, framework compliance, and cross-reference accuracy. Generate detailed compliance report with actionable recommendations."
    context: "Project files list and mypromptflow framework requirements"
    expected_tokens: 80
```

## Success Criteria

**Validation Effectiveness**:
- Identifies AI consumability issues in project documentation
- Provides actionable recommendations for improvement
- Validates framework compliance accurately
- Ensures cross-reference consistency and accuracy

**Quality Improvements**:
- Project files become more actionable for AI agents
- Framework compliance improves across project portfolio
- Cross-referencing becomes more reliable and comprehensive
- Progress tracking becomes more effective for AI agent coordination

This validator ensures that project documentation files serve their intended purpose of enabling effective AI agent project management and coordination within the mypromptflow framework.