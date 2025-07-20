# /validate-pr Command

**AI Agent Instruction**: Progressive PR validation using Claude tools with conditional specialist spawning and embedded fallbacks.

## Usage
```bash
/validate-pr [pr-number]
```

## Command Description

**Target AI Agent**: Claude Code with Task, Bash, Read, LS, and Glob tool access  
**Execution Type**: Multi-phase workflow with embedded context and fallback procedures  
**Token Efficiency**: 50-80% savings through conditional loading and embedded validators  
**Dependencies**: Self-sufficient with embedded fallbacks for all external dependencies  

This instruction guides AI agents through progressive PR validation using specific Claude tools, with embedded validator specifications and comprehensive fallback procedures.

## Progressive Loading Implementation

When this command is executed, perform the following progressive loading workflow:

### Phase 1: Mandatory Asset Discovery (30 seconds)

**AI Agent Instructions**: Execute these specific Claude tool operations in sequence:

**Step 1.1: Validator Registry Discovery**  
Use Read tool to check: `meta/validators/registry.yaml`
- **If file exists**: Parse YAML content to extract validator locations and capabilities
- **If file missing**: Use embedded validator definitions (see Embedded Validators section)
- **Output**: Display validator count and available capabilities

**Step 1.2: PR File Change Detection**  
Primary method: Use Bash tool to execute: `git diff --name-only HEAD~1 HEAD`
- **Success case**: Parse returned file list for type classification
- **Failure case**: Execute fallback file detection sequence:
  1. Use LS tool to scan current directory recursively
  2. Use Glob tool with pattern `**/*.{md,ts,tsx,py,yaml,yml,js,jsx}`
  3. Filter by recent modification (if available)

**Step 1.3: Discovery Summary**  
Output structured summary:
```
🔍 Progressive PR Validation Discovery Results:
📋 Available validators: [number] ([validator-names])
📁 Changed files detected: [number] files
🎯 File types detected: [types-list]
```

**Context Storage**: Store validator registry data and file list in working memory for Phase 2

### Phase 2: Intelligent File Type Detection (60 seconds)

**AI Agent Instructions**: Process file list from Phase 1 using pattern matching logic:

**Step 2.1: Initialize File Type Categories**  
Create working variables for file classification:
- `claude_command_files`: Files matching `.claude/commands/*.md` pattern
- `claude_md_files`: Files named `CLAUDE.md` 
- `ai_agent_files`: Files in `ai/agents/` or `ai-agent-instruction-design-excellence/` directories
- `typescript_files`: Files with `.ts` or `.tsx` extensions
- `python_files`: Files with `.py` extension
- `yaml_files`: Files with `.yaml` or `.yml` extensions
- `generic_md_files`: Other `.md` files

**Step 2.2: Pattern Matching Classification**  
For each file from Phase 1 file list, apply pattern matching:
- Check file path contains `.claude/commands/` and ends with `.md` → claude_command_files
- Check filename equals `CLAUDE.md` → claude_md_files
- Check path contains `ai/agents/` or `ai-agent-instruction-design-excellence/` → ai_agent_files
- Check extension `.ts` or `.tsx` → typescript_files
- Check extension `.py` → python_files
- Check extension `.yaml` or `.yml` → yaml_files
- Check extension `.md` (remaining) → generic_md_files

**Step 2.3: Priority Classification and Reporting**  
Output classification results with priority levels:
```
🎯 File Type Detection Results:
  🤖 Claude Commands: [count] files [CRITICAL]
  🧠 CLAUDE.md Files: [count] files [CRITICAL]  
  👑 AI Agent Instructions: [count] files [HIGH]
  📘 TypeScript Files: [count] files [HIGH]
  🐍 Python Files: [count] files [HIGH]
  ⚙️ YAML Files: [count] files [MEDIUM]
  📝 Generic Markdown: [count] files [LOW]
```

**Context Storage**: Store categorized file lists for Phase 3 specialist spawning decisions

### Phase 3: Conditional Specialist Spawning (90 seconds)

**AI Agent Instructions**: Based on file type detection results, spawn specialists using Task tool:

**Step 3.1: Initialize Spawning Context**  
Set up tracking variables:
- `spawned_specialists`: List of successfully spawned specialists
- `total_estimated_tokens`: Running count starting at 50 (base overhead)
- `spawning_failures`: Track any specialist spawning failures

**Step 3.2: Critical Priority Specialist Spawning**

**Claude Command Files (CRITICAL Priority)**  
If `claude_command_files` contains files:
1. Check if validator registry contains `claude-command-evaluator` 
2. **If validator exists**: Use Task tool with parameters:
   - **description**: "Validate Claude command files for AI Agent Instruction Design Excellence compliance"
   - **prompt**: "You are a Claude Command Evaluator specialist. Analyze files: {claude_command_files}. Apply validation criteria from @projects/ai-agent-instruction-design-excellence/docs/assessment-tools/framework-coherence-analyzer.md. Focus on: concrete specificity, external dependency elimination, immediate actionability. Generate compliance report with specific recommendations for improvement."
   - **context**: Embed file list and validation criteria
   - **expected_tokens**: 50
3. **If validator missing**: Use embedded Claude Command validation logic (see Embedded Validators section)

**AI Agent Instruction Files (CRITICAL Priority)**  
If `ai_agent_files` or `claude_md_files` contain files:
1. Check if validator registry contains `ai-agent-instruction-evaluator`
2. **If validator exists**: Use Task tool with parameters:
   - **description**: "Validate AI agent instruction files using Design Excellence Framework"
   - **prompt**: "You are an AI Agent Instruction Evaluator specialist. Analyze files: {combined_file_list}. Apply assessment tools from @projects/ai-agent-instruction-design-excellence/docs/assessment-tools/ including communication-pattern-validator.md and workflow-completeness-inspector.md. Generate detailed compliance assessment with actionable recommendations."
   - **context**: Embed file list and framework assessment criteria
   - **expected_tokens**: 80
3. **If validator missing**: Use embedded AI instruction validation logic

**Step 3.3: High Priority Specialist Spawning**

**TypeScript Files (HIGH Priority)**  
If `typescript_files` contains files:
1. Check registry for `typescript-frontend-validator`
2. **If validator missing** (expected): Output gap identification and apply embedded TypeScript validation patterns
3. Use fallback: Generic code quality assessment focusing on type safety, component patterns, and integration quality

**Python Files (HIGH Priority)**  
If `python_files` contains files:
1. Check registry for `python-backend-validator` 
2. **If validator missing** (expected): Apply embedded Python validation patterns
3. Use fallback: Code quality assessment focusing on PEP compliance, security patterns, and architecture quality

**Step 3.4: Medium/Low Priority Processing**

**YAML Files (MEDIUM Priority)**  
If `yaml_files` contains files: Apply embedded YAML syntax and structure validation

**Generic Markdown (LOW Priority)**  
If `generic_md_files` contains files: Apply lightweight documentation quality assessment

**Step 3.5: Spawning Efficiency Reporting**  
Output spawning results:
```
🚀 Specialist Spawning Results:
  🎯 Specialists spawned: [count]
  💾 Estimated tokens loaded: [total] 
  ⚡ Token efficiency: [percentage]% savings vs monolithic
  ❌ Spawning failures: [count] (fallbacks applied)
```

### Phase 4: Progressive Result Aggregation (60 seconds)

**AI Agent Instructions**: Collect and synthesize results from spawned specialists:

**Step 4.1: Wait for Specialist Completion**  
Monitor Task tool executions until all spawned specialists complete:
- Check completion status of each spawned Task
- Apply timeout handling (maximum 300 seconds per specialist)
- If timeout occurs: Collect partial results and note incomplete specialists

**Step 4.2: Result Collection from Specialists**  
For each completed specialist, collect structured results:

**Result Collection Pattern**:
1. **Check Output Files**: Look for specialist result files in expected locations
2. **Parse Structured Data**: Extract key metrics from specialist outputs:
   - Files processed count
   - Issues found with severity levels
   - Validation coverage percentage  
   - Specific recommendations generated
3. **Aggregate Metrics**: Combine individual specialist results

**Step 4.3: Calculate Validation Metrics**  
Compute validation effectiveness:
- `total_files_processed`: Sum from all specialists
- `total_issues_found`: Sum of all detected issues
- `validation_coverage`: (total_files_processed / total_files_in_pr) × 100
- `token_efficiency`: ((500 - total_estimated_tokens) / 500) × 100

**Step 4.4: Generate Comprehensive Report**  
Output final validation results:
```
📊 PROGRESSIVE PR VALIDATION RESULTS FOR PR #[number]
═══════════════════════════════════════════════════════

⏳ Specialist Execution Status:
  ✅ Completed: [count] specialists
  ⚠️ Partial/Timeout: [count] specialists
  ❌ Failed: [count] specialists

📊 Validation Coverage Analysis:
  📁 Total files in PR: [count]
  🎯 Files validated: [count]
  📈 Validation coverage: [percentage]%
  🔍 Issues found: [count] ([severity_breakdown])

⚡ Progressive Loading Efficiency:
  🚀 Specialists spawned: [count]
  💾 Tokens loaded: [total] (vs 500 monolithic)
  ⚡ Token efficiency: [percentage]% savings
  ⏱️ Total execution time: [duration]

🎯 Critical Issues Requiring Attention:
  [List of high-priority issues from specialists]

📋 Recommendations Summary:
  [Consolidated recommendations from all specialists]

✅ Progressive validation complete - Review recommendations for PR approval
```

**Step 4.5: Result Persistence**  
Store validation results for future reference:
- Create `meta/validation/pr-[number]-results.yaml` with complete results
- Update validation history tracking if available


## Progressive Loading Benefits

### Token Efficiency Comparison

**Traditional Monolithic System (500 lines always loaded)**:
- Simple PR (Claude commands only): 500 lines → 10% utilization = 90% waste
- Medium PR (AI instructions): 500 lines → 30% utilization = 70% waste  
- Complex PR (multiple types): 500 lines → 80% utilization = 20% waste
- **Average waste: 60%**

**Progressive Loading System (50-200 lines based on content)**:
- Simple PR (Claude commands only): 50 + 50 = 100 lines → 100% utilization = **80% savings**
- Medium PR (AI instructions): 50 + 80 = 130 lines → 100% utilization = **74% savings**
- Complex PR (multiple types): 50 + 50 + 80 + 60 = 240 lines → 100% utilization = **52% savings**
- **Average savings: 69%**

### Architecture Benefits

1. **Asset Discovery**: Automatic detection of existing validators prevents duplicate creation
2. **Conditional Loading**: Only loads specialists for detected file types  
3. **Scalable Design**: Adding new specialists doesn't impact simple scenarios
4. **Production Ready**: Uses existing production validators (claude-command-evaluator, ai-agent-instruction-evaluator)
5. **Gap Identification**: Clearly identifies missing validators for future creation
6. **Token Optimization**: Achieves 50-80% token savings while maintaining comprehensive coverage

## Validator Integration

### Production-Ready Validators
- **Claude Command Evaluator**: `@projects/ai-pr-validation-system/ai/agents/claude-command-evaluator.md`
- **AI Agent Instruction Evaluator**: `@projects/ai-pr-validation-system/ai/agents/ai-agent-instruction-evaluator.md`

### Validator Gaps Identified
- **TypeScript Frontend Validator**: Need to create for `.ts/.tsx` files
- **Python Backend Validator**: Need to create for `.py` files  
- **YAML Config Validator**: Need to create for `.yaml/.yml` files
- **Test Validator**: Need to create for test files
- **Docker Validator**: Need to create for Docker files

### Registry Integration

The command integrates with `meta/validators/registry.yaml` for:
- Asset discovery before validation
- Capability mapping to file types
- Gap identification for future development
- Progressive loading optimization

## Execution Instructions

When user runs `/validate-pr 23`, execute this progressive workflow:

1. **Asset Discovery**: Read meta/validators/registry.yaml for existing capabilities
2. **File Detection**: Identify changed files and classify by type
3. **Conditional Spawning**: Spawn only relevant specialists based on detected files
4. **Progressive Loading**: Load 50-200 lines instead of 500 lines monolithic
5. **Result Aggregation**: Collect results from spawned specialists only
6. **Efficiency Reporting**: Document token savings and coverage metrics

## Implementation Notes

This command implements progressive loading using the **AI Agent Instruction Design Excellence Framework**:
- **Concrete Instructions**: Specific Claude tool usage (Task, Bash, Read, LS)
- **Self-Sufficient**: References existing validators and assessment tools
- **Immediately Actionable**: Clear 4-phase execution workflow  
- **Token Efficient**: 50-80% savings through conditional specialist spawning