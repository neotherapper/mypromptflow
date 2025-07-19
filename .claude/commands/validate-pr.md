# /validate-pr Command

Validates a Pull Request using intelligent file detection and specialized AI agent evaluation with comprehensive AI agent instruction detection across the entire project.

## Usage
```bash
/validate-pr [pr-number]
```

## Command Description

This command analyzes a PR's changed files and spawns appropriate specialized AI agents to perform comprehensive validation. It uses advanced content-based detection to identify AI agent instructions throughout the project structure.

## Implementation

When this command is executed, perform the following steps:

### 1. PR Analysis Phase
```bash
# Get PR information using GitHub API or git commands
# For testing, we'll analyze the files in the current project that were changed
echo "Analyzing PR #${pr_number}..."

# List changed files (for testing, use recent project changes)
CHANGED_FILES=$(git diff --name-only HEAD~1 HEAD 2>/dev/null || find . -name "*.md" -type f -newer .git/COMMIT_EDITMSG 2>/dev/null || echo "Manual file detection needed")
echo "Changed files detected:"
echo "$CHANGED_FILES"
```

### 2. Comprehensive File Pattern Detection

Apply advanced content-based and location-based detection:

```yaml
File Detection Rules:
  claude_commands:
    location_pattern: ".claude/commands/*.md"
    content_patterns: ["# /", "## Usage", "## Command Description"]
    agent: "claude-command-evaluator"
    description: "Claude command files requiring structure and syntax validation"
    
  claude_md_files:
    location_pattern: "**/CLAUDE.md"
    content_patterns: ["## AI Agent Instructions", "Project Context", "Working Patterns"]
    agent: "claude-md-evaluator"
    special_handling: "Use improve-claude.md methodology"
    description: "CLAUDE.md files requiring framework compliance and Claude integration validation"
    
  ai_agent_instructions:
    location_patterns: 
      - "ai/agents/*.md"
      - "ai/prompts/**/*.md"
      - "ai/prompts/**/*.yaml"
    content_patterns: 
      - "## Agent Purpose"
      - "You are a specialized"
      - "Your task is to"
      - "product manager"
      - "specialist"
      - "orchestrator"
      - "validator"
    agent: "ai-agent-instruction-evaluator"
    description: "AI agent instruction files requiring framework compliance validation"
    
  meta_prompts:
    location_pattern: "ai/prompts/meta-prompts/*.md"
    content_patterns: ["meta-prompt", "orchestrator", "dependency"]
    agent: "meta-prompt-evaluator"
    description: "Meta-prompt files requiring orchestration and coordination validation"
    
  document_templates:
    location_pattern: "ai/prompts/document-templates/**/*.md"
    content_patterns: ["template", "## Template", "specification"]
    agent: "template-evaluator"
    description: "Document template files requiring structure and AI instruction clarity"
    
  project_docs:
    location_patterns:
      - "README.md"
      - "project-purpose.md" 
      - "task-list.md"
      - "progress.md"
      - "research-integration.md"
    agent: "documentation-validator"
    description: "Project documentation requiring consistency and completeness validation"
```

### 3. Advanced Agent Spawning Logic

For each detected file type, spawn the appropriate validation agent:

```bash
# Content-based detection function
detect_ai_instruction_type() {
    local file="$1"
    local content=$(cat "$file" 2>/dev/null || echo "")
    
    # Check for Claude command patterns
    if [[ "$file" == *".claude/commands/"* ]] && [[ "$content" =~ "# /" ]]; then
        echo "claude-command"
        return
    fi
    
    # Check for CLAUDE.md files (special handling)
    if [[ "$file" == *"CLAUDE.md" ]]; then
        echo "claude-md"
        return
    fi
    
    # Check for AI agent instruction patterns
    if [[ "$content" =~ "## Agent Purpose"|"You are a specialized"|"Your task is to" ]]; then
        echo "ai-agent-instruction"
        return
    fi
    
    # Check for meta-prompts
    if [[ "$file" == *"ai/prompts/meta-prompts/"* ]] || [[ "$content" =~ "meta-prompt"|"orchestrator" ]]; then
        echo "meta-prompt"
        return
    fi
    
    # Check for document templates
    if [[ "$file" == *"ai/prompts/document-templates/"* ]]; then
        echo "document-template"
        return
    fi
    
    # Check for project documentation
    if [[ "$file" =~ (README|project-purpose|task-list|progress|research-integration)\.md$ ]]; then
        echo "project-doc"
        return
    fi
    
    echo "unknown"
}

# Spawn appropriate agents based on detection
for file in $CHANGED_FILES; do
    file_type=$(detect_ai_instruction_type "$file")
    
    case "$file_type" in
        "claude-command")
            echo "🤖 Spawning Claude Command Evaluator for: $file"
            spawn_agent "claude-command-evaluator" "$file"
            ;;
        "claude-md")
            echo "🧠 Spawning CLAUDE.md Evaluator for: $file"
            spawn_agent "claude-md-evaluator" "$file"
            ;;
        "ai-agent-instruction")
            echo "🎯 Spawning AI Agent Instruction Evaluator for: $file"
            spawn_agent "ai-agent-instruction-evaluator" "$file"
            ;;
        "meta-prompt")
            echo "🔧 Spawning Meta-Prompt Evaluator for: $file"
            spawn_agent "meta-prompt-evaluator" "$file"
            ;;
        "document-template")
            echo "📋 Spawning Template Evaluator for: $file"
            spawn_agent "template-evaluator" "$file"
            ;;
        "project-doc")
            echo "📚 Spawning Documentation Validator for: $file"
            spawn_agent "documentation-validator" "$file"
            ;;
        *)
            echo "❓ Unknown file type, skipping: $file"
            ;;
    esac
done
```

### 4. Validation Orchestration

Execute validation with proper coordination:

1. **Independent Validations** (can run in parallel):
   - Claude command structure validation
   - AI agent instruction framework compliance
   - Meta-prompt orchestration validation
   - Template structure validation
   - Documentation consistency checks

2. **CLAUDE.md Special Handling** (sequential after other validations):
   - Apply improve-claude.md methodology
   - Framework assessment using AI Agent Instruction Design Excellence framework
   - Claude integration pattern validation

3. **Cross-Reference Validation** (after all individual validations):
   - Verify @file_path references are accurate
   - Check consistency between related files
   - Validate integration points

### 5. Result Aggregation

Collect and present comprehensive results:

```bash
echo "📊 PR Validation Results for PR #${pr_number}"
echo "============================================"
echo "✅ Files Validated: ${validated_count}"
echo "🎯 AI Instructions Found: ${ai_instruction_count}"
echo "🤖 Claude Commands: ${claude_command_count}"
echo "🧠 CLAUDE.md Files: ${claude_md_count}"
echo "⚠️  Warnings: ${warning_count}"
echo "❌ Errors: ${error_count}"
echo ""
echo "📋 Detailed Results:"
# Display results from each agent with file type classification
```

## Agent Instructions Integration

### Claude Command Evaluator
- **File**: `@projects/ai-pr-validation-system/ai/agents/claude-command-evaluator.md`
- **Purpose**: Validate Claude command structure, syntax, and best practices
- **Focus**: Command documentation, parameter validation, execution logic

### CLAUDE.md Evaluator (Special Handling)
- **Methodology**: Apply improve-claude.md workflow patterns
- **Framework**: Use AI Agent Instruction Design Excellence framework assessment
- **Focus**: Claude integration patterns, cross-reference accuracy, framework compliance

### AI Agent Instruction Evaluator
- **File**: `@projects/ai-pr-validation-system/ai/agents/ai-agent-instruction-evaluator.md`
- **Purpose**: Validate AI agent instructions using 93% effective framework
- **Scope**: Comprehensive detection across entire project structure
- **Focus**: Framework compliance, effectiveness scoring, quality assessment

### Meta-Prompt Evaluator (Future)
- **Purpose**: Validate meta-prompts and orchestration patterns
- **Focus**: Coordination logic, dependency management, orchestration effectiveness

### Template Evaluator (Future)
- **Purpose**: Validate document templates and AI instruction clarity
- **Focus**: Template structure, usage instructions, AI integration patterns

### Documentation Validator (Future)
- **Purpose**: Validate project documentation consistency and completeness
- **Focus**: Cross-reference accuracy, formatting consistency, content completeness

## Execution Instructions

When user runs `/validate-pr 23`, execute this comprehensive workflow:

1. **Parse PR Number**: Extract PR number from command arguments
2. **Detect Changed Files**: Identify files that changed in the PR using git or project analysis
3. **Apply Advanced Pattern Matching**: Use both location and content-based detection
4. **Classify File Types**: Determine appropriate validation approach for each file
5. **Spawn Specialized Agents**: Use Task tool to create appropriate validation agents
6. **Handle Special Cases**: Apply improve-claude.md methodology for CLAUDE.md files
7. **Coordinate Validations**: Manage parallel and sequential validation execution
8. **Collect Results**: Aggregate validation results from all agents
9. **Present Comprehensive Summary**: Provide detailed validation report with file type breakdown

## Testing Instructions

To test this command:

1. **Run on Current PR**: Execute `/validate-pr 23` to validate our own changes
2. **Verify Comprehensive Detection**: Ensure it correctly identifies:
   - `.claude/commands/validate-pr.md` as Claude command
   - `projects/ai-pr-validation-system/CLAUDE.md` as CLAUDE.md file requiring special handling
   - `ai/agents/*.md` files as AI agent instructions
   - Any AI instructions in `ai/prompts/` directories
   - Project documentation files
3. **Check Agent Spawning**: Verify appropriate agents are created for each file type
4. **Validate Content Detection**: Ensure content-based patterns work correctly
5. **Test Special Handling**: Verify CLAUDE.md files get improve-claude.md methodology
6. **Validate Results**: Ensure meaningful validation feedback is provided

## Expected Output

```
🔍 Analyzing PR #23...

📁 Changed files detected:
  - .claude/commands/validate-pr.md (Claude Command)
  - projects/ai-pr-validation-system/CLAUDE.md (CLAUDE.md - Special Handling)
  - projects/ai-pr-validation-system/ai/agents/claude-command-evaluator.md (AI Agent Instruction)
  - projects/ai-pr-validation-system/ai/agents/ai-agent-instruction-evaluator.md (AI Agent Instruction)
  - projects/ai-pr-validation-system/project-purpose.md (Project Documentation)
  - projects/ai-pr-validation-system/README.md (Project Documentation)

🤖 Spawning specialized validation agents...
  ✅ Claude Command Evaluator: Processing validate-pr.md
  🧠 CLAUDE.md Evaluator: Processing CLAUDE.md (using improve-claude.md methodology)
  🎯 AI Agent Instruction Evaluator: Processing claude-command-evaluator.md
  🎯 AI Agent Instruction Evaluator: Processing ai-agent-instruction-evaluator.md
  📚 Documentation Validator: Processing project-purpose.md, README.md

📊 PR Validation Results for PR #23
============================================
✅ Files Validated: 6
🎯 AI Instructions Found: 3
🤖 Claude Commands: 1
🧠 CLAUDE.md Files: 1
⚠️  Warnings: 2
❌ Errors: 0

📋 Detailed Results:
✅ validate-pr.md: Command structure valid, comprehensive file detection implemented
✅ CLAUDE.md: Framework compliance 92% (excellent), Claude integration patterns present
⚠️  claude-command-evaluator.md: Framework compliance 85% (needs minor improvements)
✅ ai-agent-instruction-evaluator.md: Framework compliance 89% (good), comprehensive detection scope
✅ Documentation: Consistent formatting and accurate cross-references

🎯 Overall PR Quality: APPROVED - Comprehensive AI instruction validation system ready for testing
```

## Implementation Notes

- **Content-Based Detection**: Advanced pattern matching beyond simple file location
- **Comprehensive Coverage**: Detects AI instructions across entire project structure
- **Special Handling**: CLAUDE.md files get improve-claude.md methodology
- **Real Testing**: Use actual PR data for immediate validation
- **Iterative Improvement**: Fix issues found through actual usage
- **Framework Integration**: Apply AI Agent Instruction Design Excellence framework throughout