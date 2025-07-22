# AI Knowledge Base Testing Documentation for Claude

## Testing Philosophy

**CRITICAL:** Testing in this AI Knowledge Base system executes real validation protocols with measurable success criteria (accuracy: ≥95%, completeness: ≥90%, execution time: ≤300s per test suite). This means:

- ✅ **Real File Creation**: Tests verify that actual files are created at expected paths
- ✅ **Real Agent Parameter Passing**: Tests validate that AI agents receive correct context and instructions
- ✅ **Real Registry Updates**: Tests check that YAML registries are actually updated
- ✅ **Real Cross-Reference Creation**: Tests verify bidirectional links are actually created
- ❌ **NOT Mocking**: We don't mock or simulate - we execute and validate real outputs

## Testing Framework Overview

### Test Categories

1. **Command Execution Tests** (`command-execution-tests.yaml`)
   - Purpose: Validate that `/ai-help` and all slash commands execute properly
   - Validation: Actual command execution with real file outputs

2. **AI Agent Parameter Tests** (`agent-parameter-tests.yaml`)
   - Purpose: Ensure agents receive correct context documents and instructions
   - Validation: Agent spawning parameters and context accessibility

3. **File Creation Tests** (`file-creation-tests.yaml`)
   - Purpose: Verify actual document and feature workspace creation
   - Validation: File existence, content structure, YAML frontmatter

4. **Registry Update Tests** (`registry-update-tests.yaml`)
   - Purpose: Validate automatic registry updates after operations
   - Validation: YAML file changes, cross-references, dependency tracking

## Key Testing Principles for AI Agents

### 1. Agent Parameter Validation

When testing agent spawning, verify these parameters are correctly passed:

```yaml
# Example: Market Analysis Agent Test
expected_agent_spawn:
  agent_type: "Document Generator"
  specialization: "Market Analysis Specialist"
  required_parameters:
    document_type: "market-analysis"
    tier: 4
    template_path: "@ai/prompts/document-templates/tier4/market-analysis.md"
    output_path: "ai/knowledge/strategic/market-analysis.md"
    context_documents: []  # Tier 4 has no dependencies
```

**Critical Check:** All context documents must be accessible via @file_path references.

### 2. File Creation Validation

Every test must verify actual file creation:

```bash
# Test that file exists and has minimum content
verify_file_creation() {
    local file_path="$1"
    local min_size="${2:-100}"
    
    if [ -f "$file_path" ]; then
        local file_size=$(wc -c < "$file_path")
        if [ "$file_size" -ge "$min_size" ]; then
            # Check for YAML frontmatter
            if head -n 1 "$file_path" | grep -q "^---"; then
                return 0
            fi
        fi
    fi
    return 1
}
```

### 3. Registry Update Verification

Test that registries are actually updated:

```yaml
# Before command execution
initial_document_count: "count_existing_documents"

# After command execution  
expected_registry_changes:
  new_entry_added:
    id: "market-analysis"
    type: "research"
    path: "ai/knowledge/strategic/market-analysis.md"
    version: "1.0"
    status: "draft"
```

## Test Execution Framework

### Running Tests

Execute the full test suite:
```bash
./ai/tests/run-tests.sh
```

The test runner executes systematic validation protocol:
1. **Creates Backup**: Execute state preservation protocol (backup creation: ≤30s, verification: 100% completeness)
2. **Executes Tests**: Run test categories using sequential execution algorithm (category completion: ≤60s each, failure threshold: ≤5% per category)
3. **Validates Results**: Apply validation criteria (file existence: 100%, content structure: ≥95% compliance, YAML validity: 100%)
4. **Generates Report**: Create comprehensive test report (generation time: ≤15s, coverage metrics: accuracy, completeness, consistency scores)
5. **Offers Restore**: Execute restoration protocol (restoration time: ≤45s, integrity verification: 100%)

### Test Environment

- **Isolated**: Tests run in isolated environment with backups
- **Atomic**: Each test can be run independently
- **Cleanup**: Automatic cleanup and restoration options
- **Logging**: Comprehensive logging of all operations

## Agent Testing Protocols

### Context Document Testing

When testing agent context passing:

```yaml
# Verify context documents are provided and accessible
context_documents_provided:
  - "@ai/knowledge/strategic/statement-of-purpose.md"
  - "ai/knowledge/strategic/market-analysis.md"
validation_required:
  - all_context_files_exist: true
  - all_context_files_readable: true
  - context_files_have_valid_yaml: true
  - context_files_have_content: true
```

### Template Reference Testing

Validate template accessibility:

```yaml
# Test template access for different document types
tier_4_document:
  command: "create-document market-analysis"
  expected_template: "@ai/prompts/document-templates/tier4/market-analysis.md"
  validation:
    - template_file_exists: true
    - template_has_yaml_structure: true
    - template_has_content_sections: true
```

### Agent Communication Testing

Test inter-agent parameter handoff:

```yaml
# Sequential agent handoff validation
agent_a_to_agent_b:
  agent_a: "Market Analysis Agent"
  agent_b: "User Personas Agent"
  handoff_parameters:
    - previous_agent_output: "ai/knowledge/strategic/market-analysis.md"
    - context_integration_instructions: "Reference market analysis findings"
    - consistency_requirements: "Maintain competitive landscape insights"
```

## Quality Standards for Test Validation

### Document Structure Validation

Every created document must have:

```yaml
# Required document structure
yaml_frontmatter:
  required_fields:
    document_type: "string matching document category"
    version: "semantic version format"
    created_date: "ISO date format"
    dependencies: "array of dependency IDs"
    status: "enum: [draft, review, approved]"
    ai_context: "object with purpose and insights"

content_structure:
  required_sections:
    - "# Document Title"
    - "## Executive Summary"
    - "## [Content Sections]"
    - "## AI Agent Instructions"
    - "## Cross-References"
```

### Cross-Reference Validation

Test bidirectional linking:

```yaml
# Cross-reference validation
new_document_references:
  - document: "user-personas"
    references:
      - "@ai/knowledge/strategic/statement-of-purpose.md"
      - "@ai/knowledge/strategic/market-analysis.md"

bidirectional_updates:
  - referenced_document: "statement-of-purpose.md"
    should_now_contain:
      - cross_reference_to: "user-personas.md"
      - reference_type: "referenced_by"
```

## Error Handling Testing

### Agent Failure Scenarios

Test agent failure recovery:

```yaml
# Test agent communication failure
agent_communication_failure:
  setup:
    - simulate_agent_failure: "second_agent_in_sequence"
  trigger_command: "orchestrate-agents prd"
  expected_behavior:
    - workflow_pauses_at_failure_point: true
    - partial_results_preserved: true
    - retry_mechanism_available: true
    - user_notified_of_failure_and_options: true
```

### Registry Error Recovery

Test registry update failures:

```yaml
# Test registry update failure recovery
registry_update_failure:
  test_scenarios:
    registry_file_locked:
      - simulate_file_lock: "ai/context/document-registry.yaml"
      - expected_behavior:
          - graceful_error_handling: true
          - retry_mechanism_available: true
          - document_creation_not_blocked: true
```

## Test Success Criteria

### Command Execution Tests
- ✅ All commands execute without errors
- ✅ Files created at expected paths with proper content
- ✅ YAML frontmatter valid and complete
- ✅ Registry updates applied correctly

### Agent Parameter Tests
- ✅ Agents receive complete parameter sets
- ✅ Context documents accessible and valid
- ✅ Templates available and properly formatted
- ✅ Inter-agent communication successful

### File Creation Tests
- ✅ Files created at correct paths
- ✅ Content structure follows standards
- ✅ Cross-references valid and bidirectional
- ✅ TypeScript examples present and valid

### Registry Update Tests
- ✅ Registries updated after every operation
- ✅ YAML syntax remains valid after updates
- ✅ Cross-references bidirectional and valid
- ✅ Dependency satisfaction accurately tracked

## Debugging Failed Tests

### Common Issues and Solutions

1. **File Not Created**
   - Check agent parameters were passed correctly
   - Verify template paths are accessible
   - Check directory permissions

2. **Registry Not Updated**
   - Verify YAML syntax in registry files
   - Check file permissions
   - Validate registry update logic

3. **Agent Parameter Errors**
   - Verify context documents exist and are readable
   - Check template references are valid
   - Validate agent instruction format

4. **Cross-Reference Failures**
   - Check @ai/knowledge/ path format
   - Verify referenced files exist
   - Validate bidirectional linking logic

## Best Practices for AI Agents

### When Writing Tests
1. **Always test actual outputs** - never mock or simulate
2. **Verify agent parameters completely** - context, templates, instructions
3. **Check file system changes** - creation, updates, permissions
4. **Validate registry consistency** - YAML syntax, cross-references
5. **Test error conditions** - agent failures, missing files, corrupted data

### When Implementing Commands
1. **Follow test specifications exactly** - tests define the contract
2. **Ensure atomic operations** - all-or-nothing for complex workflows
3. **Validate inputs thoroughly** - prevent invalid agent spawning
4. **Provide clear error messages** - help users understand and recover
5. **Update registries consistently** - maintain system integrity

This testing framework ensures that the AI Knowledge Base system works reliably in real-world scenarios with actual file creation, agent coordination, and registry management.