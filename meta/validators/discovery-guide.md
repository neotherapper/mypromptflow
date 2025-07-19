# Validator Discovery Guide for AI Agents

## 🎯 Purpose

This guide helps AI agents discover existing validators in the project before creating new ones, preventing duplicate creation and enabling progressive loading efficiency.

## 🔍 Discovery Protocol

### **MANDATORY Step 1: Check Registry**
**Always read first**: `meta/validators/registry.yaml`
- Contains complete inventory of all validators in project
- Shows file type coverage and capabilities
- Identifies production-ready vs. development validators
- Documents progressive loading opportunities

### **Step 2: Verify Validator Exists**
**Before using any validator**, verify the file exists:
```bash
# Check production validators
ls -la projects/ai-pr-validation-system/ai/agents/claude-command-evaluator.md
ls -la projects/ai-pr-validation-system/ai/agents/ai-agent-instruction-evaluator.md

# Check framework templates (development)
ls -la projects/ai-agent-instruction-design-excellence/docs/assessment-tools/
ls -la projects/ai-agent-instruction-design-excellence/docs/template-library/worker-templates/
```

### **Step 3: Capability Mapping**
**Match your needs to existing capabilities:**

| File Types | Existing Validator | Production Ready |
|------------|-------------------|------------------|
| `.claude/commands/*.md` | claude-command-evaluator | ✅ YES |
| `ai/agents/*.md` | ai-agent-instruction-evaluator | ✅ YES |
| `ai/prompts/**/*.md` | ai-agent-instruction-evaluator | ✅ YES |
| `**/CLAUDE.md` | ai-agent-instruction-evaluator | ✅ YES |
| `*.ts, *.tsx` | **MISSING** | ❌ Need to create |
| `*.py` | **MISSING** | ❌ Need to create |
| `*.yaml, *.json` | **MISSING** | ❌ Need to create |

## 🚀 Progressive Loading Strategy

### **Current Problem**
The `validate-pr.md` command loads ALL detection patterns (~500 lines) regardless of which file types are actually in the PR.

### **Solution: Discovery-First Architecture**

**New Validate-PR Architecture:**
```
validate-pr.md (coordinator - 50 lines):
├── Step 1: Read meta/validators/registry.yaml  
├── Step 2: Detect file types in PR
├── Step 3: Map file types to existing validators
├── Step 4: Spawn ONLY relevant validators
└── Step 5: Aggregate results

Token Efficiency Examples:
- PR with only Claude commands: 50 + 50 = 100 lines (80% savings)
- PR with TypeScript + commands: 50 + 50 + 60 = 160 lines (68% savings)  
- Complex PR with 4 types: 50 + 200 = 250 lines (50% savings)
```

## 📋 Validator Selection Decision Tree

### **For AI Instruction Files**
```yaml
if_file_matches:
  ".claude/commands/*.md": 
    use: "claude-command-evaluator"
    spawn: "Task tool with claude-command-evaluator agent"
    location: "projects/ai-pr-validation-system/ai/agents/claude-command-evaluator.md"
    
  "ai/agents/*.md":
    use: "ai-agent-instruction-evaluator"  
    spawn: "Task tool with ai-agent-instruction-evaluator agent"
    location: "projects/ai-pr-validation-system/ai/agents/ai-agent-instruction-evaluator.md"
    
  "ai/prompts/**/*.md":
    use: "ai-agent-instruction-evaluator"
    spawn: "Task tool with ai-agent-instruction-evaluator agent"
    
  "**/CLAUDE.md":
    use: "ai-agent-instruction-evaluator"
    spawn: "Task tool with ai-agent-instruction-evaluator agent"
    special_handling: "Apply improve-claude.md methodology"
```

### **For Programming Language Files** 
```yaml
if_file_matches:
  "*.ts, *.tsx":
    existing_validator: "NONE"
    action: "Create typescript-frontend-validator OR extend existing"
    priority: "HIGH - Large TypeScript codebase"
    
  "*.py":
    existing_validator: "NONE"  
    action: "Create python-backend-validator OR extend existing"
    priority: "HIGH - Python backend validation missing"
    
  "*.test.*, *.spec.*":
    existing_validator: "NONE"
    action: "Create test-validator OR extend existing"
    priority: "MEDIUM - Test quality validation needed"
```

## ⚡ Best Practices

### **Before Creating Any Validator**
1. ✅ **Check Registry**: Read `meta/validators/registry.yaml` completely
2. ✅ **Verify Paths**: Confirm referenced validators actually exist
3. ✅ **Check Coverage**: See if existing validator can be extended
4. ✅ **Consider Progressive Loading**: How will this fit in token optimization?

### **When Extending Existing Validators**
1. **Read Original**: Understand current capabilities and patterns
2. **Enhance Incrementally**: Add new file types without breaking existing functionality  
3. **Update Registry**: Document new capabilities in registry
4. **Test Integration**: Ensure existing spawn patterns still work

### **When Creating New Validators**
1. **Fill Gaps Only**: Create only for truly uncovered file types
2. **Follow Patterns**: Use existing validators as templates
3. **Add to Registry**: Document in `meta/validators/registry.yaml`
4. **Enable Progressive Loading**: Design for conditional spawning

## 🔧 Integration Examples

### **Spawning Existing Validators**
```bash
# For Claude commands
spawn_agent_with_task_tool "claude-command-evaluator" "$claude_command_files"

# For AI instructions  
spawn_agent_with_task_tool "ai-agent-instruction-evaluator" "$ai_instruction_files"

# For workflow validation (development stage)
spawn_agent_with_task_tool "quality-validator" "$workflow_files"
```

### **Progressive Loading Implementation**
```bash
# Read registry to understand available validators
registry=$(cat meta/validators/registry.yaml)

# Detect file types in PR
file_types=$(detect_file_types_in_pr)

# Map to existing validators
for file_type in $file_types; do
    validator=$(lookup_validator_for_type "$file_type" "$registry")
    if [ "$validator" != "NONE" ]; then
        spawn_existing_validator "$validator" "$files_of_type"
    else
        handle_uncovered_file_type "$file_type" "$files_of_type"
    fi
done
```

## 📊 Registry Maintenance

### **Keeping Registry Updated**
- **Automatic Discovery**: Re-run discovery tools when new validators added
- **Manual Updates**: Update capabilities when validators enhanced
- **Version Tracking**: Track production readiness and effectiveness scores
- **Coverage Analysis**: Regular analysis of gaps and recommendations

### **Registry Schema**
```yaml
validator_entry:
  name: "validator-identifier"
  location: "path/to/validator.md"
  file_types: ["*.ext", "pattern/**/*"]
  capabilities: ["capability1", "capability2"]
  spawn_pattern: "how to spawn this validator"
  authority_level: "Level in hierarchy"
  parallel_safe: true/false
  production_ready: true/false
```

This discovery guide ensures AI agents always check for existing solutions before creating new validators, enabling efficient progressive loading and preventing resource duplication.