# Intent vs Implementation Validator

**Revolutionary Innovation**: First-ever PR validation system that checks if PRs actually do what they claim to do.

**Location**: meta/validation/validators/ai-instruction/intent-implementation-validator.md  
**Purpose**: Validate semantic alignment between PR description and actual implementation  
**Authority Level**: Specialist Agent (Level 3)  
**Production Threshold**: ≥85% semantic alignment for approval  
**Timeout Configuration**: ≤240s execution time with error handling  

## Validator Purpose

This groundbreaking validator addresses a critical gap in PR validation: ensuring PRs actually implement what they claim in their descriptions. It prevents scope creep, identifies missing implementations, and flags unrelated changes.

### Revolutionary Scenarios This Catches:
- **Scope Creep**: PR says "Fix login validation bug" but also includes unrelated UI redesign
- **Incomplete Implementation**: PR says "Add user authentication system" but missing test files and security validations  
- **Mislabeled Changes**: PR says "Update API documentation" but includes breaking API changes
- **Hidden Dependencies**: PR says "Refactor database layer" but changes frontend components too

## Intent Analysis Framework

### Phase 1: PR Metadata Extraction (≤60s)

**Data Sources** (with fallback hierarchy):
```yaml
pr_metadata_sources:
  primary: "gh pr view [pr] --json title,body,labels,author,baseRefName"
  fallback: "git log --oneline | head -5 for commit messages"
  timeout: 30s
  retry_attempts: 2
```

**Extracted Elements**:
```yaml
intent_extraction:
  pr_title: "Main change description"
  pr_description: "Detailed explanation of changes"
  pr_labels: "Categorization hints (feature/bug/enhancement)"
  change_scope: "Expected areas of impact"
  success_criteria: "How to verify the change works"
```

### Phase 2: Intent Parsing and Categorization (≤60s)

**Change Type Classification**:
```yaml
change_types:
  fix:
    indicators: ["fix", "bug", "error", "issue", "problem", "resolve"]
    expected_scope: "Minimal, targeted changes"
    unrelated_threshold: 5  # percent
    
  feature:
    indicators: ["add", "new", "implement", "create", "feature"]
    expected_scope: "Multiple files, tests, documentation"
    unrelated_threshold: 10  # percent
    
  refactor:
    indicators: ["refactor", "restructure", "reorganize", "clean up"]
    expected_scope: "Code structure changes, no functionality changes"
    unrelated_threshold: 15  # percent
    
  documentation:
    indicators: ["docs", "documentation", "readme", "comments"]
    expected_scope: "Documentation files only"
    unrelated_threshold: 5  # percent
    
  testing:
    indicators: ["test", "spec", "coverage", "testing"]
    expected_scope: "Test files and test-related code"
    unrelated_threshold: 10  # percent
```

**Scope Definition Extraction**:
```yaml
scope_analysis:
  explicit_mentions:
    method: "Parse description for specific file/directory mentions"
    examples: ["update src/auth/", "modify database schema", "add tests for login"]
    
  implicit_scope:
    method: "Infer scope from change type and magnitude"
    factors: ["change_type", "component_mentions", "integration_points"]
    
  expected_file_types:
    method: "Map intended changes to expected file extensions"
    mapping: {
      "frontend": [".tsx", ".ts", ".css", ".scss"],
      "backend": [".py", ".js", ".yaml", ".sql"],
      "tests": [".test.ts", ".spec.py", ".test.js"],
      "docs": [".md", ".rst", ".txt"]
    }
```

### Phase 3: Implementation Analysis (≤60s)

**File Change Detection**:
```yaml
file_analysis:
  changed_files: "List from gh pr diff --name-only [pr]"
  change_stats: "Addition/deletion counts per file"
  change_magnitude: "Lines changed relative to total file size"
  
  file_categorization:
    core_changes: "Files directly related to stated intent"
    supporting_changes: "Tests, docs, config related to core changes"
    unrelated_changes: "Files not mentioned or implied in description"
```

**Change Content Analysis**:
```yaml
content_analysis:
  diff_analysis:
    method: "Parse actual code changes for semantic meaning"
    focus: ["function additions", "interface changes", "logic modifications"]
    
  integration_points:
    method: "Identify how changes interact with existing code"
    validation: "Check if integration matches stated goals"
    
  breaking_changes:
    method: "Detect API/interface changes not mentioned in description"
    severity: "Critical if undisclosed breaking changes found"
```

## Semantic Alignment Validation

### Alignment Scoring Algorithm (0-100 scale)

```yaml
semantic_alignment_calculation:
  stated_vs_actual_scope:
    weight: 40  # percent of total score
    measurement: "Percentage of expected changes actually implemented"
    scoring: |
      if actual_changes ⊆ expected_changes: +40 points
      if actual_changes ⊃ expected_changes: +(40 * overlap_percentage)
      if significant_unrelated_changes: -(unrelated_percentage * 40)
      
  completeness_assessment:
    weight: 35  # percent of total score  
    measurement: "Goals stated vs goals implemented"
    scoring: |
      implemented_goals / stated_goals * 35
      
  consistency_validation:
    weight: 25  # percent of total score
    measurement: "Consistency between title, description, labels, commits"
    factors: ["title_description_alignment", "label_content_match", "commit_message_consistency"]
```

### Critical Issue Detection

**Scope Creep Detection**:
```yaml
scope_creep_thresholds:
  minor_creep: 
    threshold: "5-15% unrelated changes"
    action: "WARNING - Review additional changes"
    
  moderate_creep:
    threshold: "15-30% unrelated changes"  
    action: "CONCERN - Significant scope expansion"
    
  major_creep:
    threshold: ">30% unrelated changes"
    action: "BLOCK - Major scope creep detected"
```

**Incomplete Implementation Detection**:
```yaml
completeness_validation:
  missing_tests:
    condition: "Feature/fix PR without corresponding test changes"
    severity: "HIGH for features, MEDIUM for fixes"
    
  missing_documentation:
    condition: "Public API changes without documentation updates"
    severity: "HIGH for breaking changes, MEDIUM for additions"
    
  missing_migrations:
    condition: "Database schema changes without migration files"
    severity: "CRITICAL - deployment blocker"
    
  missing_security:
    condition: "Authentication/authorization changes without security review"
    severity: "CRITICAL - security concern"
```

## Error Handling and Recovery

### Timeout and Failure Management

```yaml
error_recovery_strategy:
  intent_parsing_failure:
    timeout: 60s
    fallback: "Basic file type classification"
    partial_mode: "Flag as 'Intent analysis incomplete'"
    
  github_api_failure:
    timeout: 30s
    retry_attempts: 2
    fallback: "Use git log and diff for basic analysis"
    
  semantic_analysis_failure:
    timeout: 60s
    fallback: "File extension and directory-based analysis"
    minimum_output: "Basic scope validation"
    
  network_timeout:
    overall_timeout: 240s
    graceful_degradation: "Return partial results with confidence scores"
    report_limitations: "Clearly state analysis limitations"
```

### Confidence Scoring

```yaml
confidence_calculation:
  high_confidence: "≥90% - Complete data, successful analysis"
  medium_confidence: "70-89% - Partial data or minor failures"
  low_confidence: "50-69% - Significant limitations or failures"
  unreliable: "<50% - Major failures, results questionable"
  
confidence_factors:
  data_completeness: "40% - PR metadata and file change data quality"
  analysis_success: "35% - Semantic analysis completion rate"  
  consistency_checks: "25% - Cross-validation between different data sources"
```

## Validation Output Format

### Structured Results

```yaml
intent_implementation_assessment:
  overall_alignment_score: 0  # 0-100
  confidence_level: "high|medium|low|unreliable"
  assessment_duration: "120s"
  
  intent_analysis:
    change_type: "fix|feature|refactor|documentation|testing"
    stated_scope: "Expected areas of change"
    expected_files: ["list of file patterns"]
    success_criteria: ["extracted goals"]
    
  implementation_analysis:
    files_changed: 15
    lines_added: 150
    lines_removed: 45
    file_categories:
      core_changes: 8
      supporting_changes: 5
      unrelated_changes: 2
      
  alignment_validation:
    semantic_alignment: 87  # 0-100
    scope_consistency: 92   # 0-100  
    completeness: 78        # 0-100
    
  critical_issues:
    scope_creep:
      severity: "minor|moderate|major|none"
      unrelated_changes_percentage: 13
      flagged_files: ["src/unrelated-component.tsx"]
      
    missing_implementations:
      - type: "missing_tests"
        severity: "medium"
        description: "Feature PR lacks test coverage for new authentication flow"
        
    undisclosed_changes:
      - type: "breaking_change"
        severity: "high"
        description: "API signature changed without mention in description"
        
  recommendations:
    - priority: "high"
      action: "Add test coverage for new authentication functionality"
      justification: "Feature changes require corresponding test validation"
      
    - priority: "medium"  
      action: "Update PR description to mention API signature changes"
      justification: "Breaking changes must be explicitly documented"
```

### Human-Readable Summary

```yaml
summary_report_template: |
  ## 🎯 Intent vs Implementation Analysis
  
  **Overall Alignment**: {alignment_score}/100 ({alignment_status})
  **Confidence**: {confidence_level} ({confidence_percentage}%)
  **Analysis Time**: {duration}
  
  ### 📋 Stated Intent
  **Change Type**: {change_type}
  **Scope**: {stated_scope}
  **Goals**: {extracted_goals}
  
  ### 🔍 Actual Implementation  
  **Files Changed**: {files_changed} ({core_changes} core, {supporting_changes} supporting, {unrelated_changes} unrelated)
  **Change Magnitude**: {lines_added} additions, {lines_removed} deletions
  
  ### ⚠️ Issues Found
  {critical_issues_summary}
  
  ### ✅ Recommendations
  {actionable_recommendations}
  
  ### 📊 Detailed Scores
  - Semantic Alignment: {semantic_alignment}/100
  - Scope Consistency: {scope_consistency}/100  
  - Implementation Completeness: {completeness}/100
```

## Integration with PR Validation System

### Spawning Pattern

```yaml
conditional_spawning:
  trigger_condition: "Any PR with title and description available"
  spawn_pattern: "Task tool with intent-implementation-validator specialist"
  parallel_safe: true
  dependencies: ["gh CLI or git access for PR metadata"]
  
execution_context:
  input_data:
    - pr_number: "Target PR identifier"
    - pr_metadata: "Title, description, labels from gh CLI"
    - file_changes: "Changed files list from gh pr diff"
    
  output_location: "meta/validation/reports/pr-{number}/intent-implementation-alignment.yaml"
  
coordination:
  with_other_validators: "Runs in parallel with file-type validators"
  reporting_integration: "Results included in comprehensive PR validation report"
  quality_gates: "≥85% alignment required for approval recommendation"
```

### Constitutional AI Compliance

**Ethical Validation Principles**:
```yaml
constitutional_principles:
  accuracy_principle:
    description: "Provide truthful assessment of PR alignment without bias"
    validation: "Cross-reference multiple data sources for consistency"
    threshold: 95  # percent compliance required
    
  transparency_principle:
    description: "Clearly explain analysis methodology and limitations"
    validation: "Include confidence scores and analysis scope"
    threshold: 95  # percent compliance required
    
  completeness_principle:
    description: "Comprehensive analysis within timeout constraints"
    validation: "Cover all stated goals and major implementation areas"
    threshold: 85  # percent compliance required
    
  responsibility_principle:
    description: "Consider impact of validation results on development workflow"
    validation: "Provide actionable recommendations, not just criticism"
    threshold: 90  # percent compliance required
    
  integrity_principle:
    description: "Acknowledge analysis limitations and uncertainty"
    validation: "Use confidence scoring and clearly state when analysis is incomplete"
    threshold: 95  # percent compliance required
```

## Success Criteria and Deployment

**Production Readiness Thresholds**:
- **Overall Alignment Detection**: ≥85% accuracy in identifying intent-implementation mismatches
- **Execution Time**: ≤240s total processing time with error handling
- **False Positive Rate**: ≤10% incorrect scope creep or missing implementation flags
- **Constitutional Compliance**: ≥95% across all 5 principles
- **Confidence Reliability**: ≥90% correlation between confidence scores and actual accuracy

**Validation Effectiveness Metrics**:
- **Scope Creep Detection**: Successfully identify unrelated changes in ≥90% of cases
- **Completeness Assessment**: Identify missing implementations in ≥85% of incomplete PRs  
- **Consistency Validation**: Flag title/description mismatches in ≥95% of cases
- **Critical Issue Detection**: Zero false negatives for security or deployment blockers

This revolutionary intent-implementation-validator represents a breakthrough in PR validation technology, ensuring PRs actually deliver what they promise and maintaining development workflow integrity through semantic alignment verification.