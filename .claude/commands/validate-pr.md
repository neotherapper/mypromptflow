# /validate-pr Command

**AI Agent Instruction**: Revolutionary PR validation with intent-implementation alignment and gh CLI integration using progressive loading and multi-tier fallbacks.

## Usage
```bash
/validate-pr [pr-number]
```

## Command Description

**Target AI Agent**: Claude Code with Task, Bash, Read, LS, and Glob tool access  
**Execution Type**: Multi-phase workflow with gh CLI integration and embedded fallbacks  
**Resource Efficiency**: Conditional specialist activation based on file type detection  
**Dependencies**: Self-sufficient with multi-tier fallback strategies for all external dependencies  
**Revolutionary Feature**: Intent vs Implementation semantic alignment validation

This instruction guides AI agents through revolutionary PR validation using GitHub CLI with systematic fallbacks, progressive loading optimization, and the breakthrough intent-implementation-validator for semantic alignment checking.

## Progressive Loading Implementation

When this command is executed, perform the following progressive loading workflow:

### Phase 1: Enhanced Asset Discovery with GitHub Integration

**AI Agent Instructions**: Execute these specific Claude tool operations in sequence:

**Step 1.1: Validator Registry Discovery**  
Use Read tool to check: `meta/validation/validators/registry.yaml`
- **If file exists**: Parse YAML content to extract validator locations and capabilities including the revolutionary intent-implementation-validator
- **If file missing**: Use embedded validator definitions (see Embedded Validators section)
- **Output**: Display validator count, available capabilities, and revolutionary intent validation status

**Step 1.2: Enhanced PR Data Extraction with Multi-Tier Fallbacks**  

**Primary Method - GitHub CLI Integration (≤30s timeout):**
```bash
# Tier 1: GitHub CLI for comprehensive PR data
gh pr view [pr-number] --json title,body,labels,author,baseRefName,url,state
gh pr diff [pr-number] --name-only
```
- **Success case**: Extract PR metadata (title, description, labels) and file changes list
- **Timeout/Error detection**: If gh CLI fails or times out (≤30s), proceed to Tier 2

**Secondary Method - Git Commands with gh Fallback (≤45s timeout):**
```bash  
# Tier 2: Git commands combined with basic gh metadata
gh pr view [pr-number] --json title,body,labels  # metadata only
git diff --name-only origin/master HEAD  # file changes
```
- **Success case**: Parse PR metadata and file list for type classification
- **Error detection**: If file count is 0, check git branch status and report configuration issue
- **Timeout/Error**: If git commands fail, proceed to Tier 3

**Fallback Method - File System Analysis (≤60s timeout):**
```bash
# Tier 3: File system discovery with pattern matching
# Use LS tool to scan current directory recursively
# Use Glob tool with pattern **/*.{md,ts,tsx,py,yaml,yml,js,jsx}
# Filter by recent modification timestamp patterns
```

**Step 1.3: Revolutionary Intent-Implementation Analysis Setup**
**BREAKTHROUGH VALIDATION**: Initialize intent-implementation-validator for semantic alignment checking:
- **Validator Location**: `meta/validation/validators/ai-instruction/intent-implementation-validator.md`
- **Purpose**: Validate PR actually does what it claims to do (industry-first capability)
- **Threshold**: ≥85% semantic alignment required for approval
- **Revolutionary Scenarios**: Scope creep detection, incomplete implementation identification, mislabeled changes flagging

**Step 1.4: Discovery Summary**  
Output structured summary:
```
🔍 Revolutionary PR Validation Discovery Results:
📋 Available validators: [number] ([validator-names])
🚀 Revolutionary intent validation: ACTIVE (≥85% alignment threshold)
📁 Changed files detected: [number] files
🎯 File types detected: [types-list]
📊 Data extraction method: [Tier 1: gh CLI | Tier 2: git+gh | Tier 3: filesystem]
```

**Context Storage**: Store validator registry data, PR metadata, and file list in working memory for Phase 2

### Phase 2: Intelligent File Type Detection and Intent Analysis

**AI Agent Instructions**: Process file list and PR metadata from Phase 1 using enhanced pattern matching:

**Step 2.1: Initialize Enhanced File Type Categories**  
Create working variables for comprehensive file classification:
- `claude_command_files`: Files matching `.claude/commands/*.md` pattern
- `claude_md_files`: Files named `CLAUDE.md` 
- `ai_agent_files`: Files in `ai/agents/` or `ai-agent-instruction-design-excellence/` directories
- `project_documentation_files`: Files matching `*/progress.md`, `*/task-list.md`, `*/project-purpose.md`, `*/research-integration.md`
- `ai_consumable_docs`: Files matching `projects/*/docs/**/*.md` pattern
- `typescript_files`: Files with `.ts` or `.tsx` extensions
- `python_files`: Files with `.py` extension
- `yaml_files`: Files with `.yaml` or `.yml` extensions
- `generic_md_files`: Other `.md` files

**Step 2.2: Enhanced Pattern Matching Classification**  
For each file from Phase 1 file list, apply enhanced pattern matching:
- Check file path contains `.claude/commands/` and ends with `.md` → claude_command_files
- Check filename equals `CLAUDE.md` → claude_md_files
- Check path contains `ai/agents/` or `ai-agent-instruction-design-excellence/` → ai_agent_files
- Check filename matches `progress.md`, `task-list.md`, `project-purpose.md`, `research-integration.md` → project_documentation_files
- Check path matches `projects/*/docs/**/*.md` pattern → ai_consumable_docs
- Check extension `.ts` or `.tsx` → typescript_files
- Check extension `.py` → python_files
- Check extension `.yaml` or `.yml` → yaml_files
- Check extension `.md` (remaining) → generic_md_files

**Step 2.3: Enhanced Priority Classification and Reporting**  
Output comprehensive classification results with priority levels:
```
🎯 Enhanced File Type Detection Results:
  🤖 Claude Commands: [count] files [CRITICAL]
  🧠 CLAUDE.md Files: [count] files [CRITICAL - SPECIALIZED VALIDATOR]  
  👑 AI Agent Instructions: [count] files [HIGH]
  📋 Project Documentation: [count] files [HIGH - NEW CATEGORY]
  🗂️ AI-Consumable Docs: [count] files [HIGH - NEW CATEGORY]
  📘 TypeScript Files: [count] files [HIGH]
  🐍 Python Files: [count] files [HIGH]
  ⚙️ YAML Files: [count] files [MEDIUM]
  📝 Generic Markdown: [count] files [LOW]
```

**Context Storage**: Store categorized file lists for Phase 3 specialist spawning decisions

### Phase 3: Revolutionary Multi-Specialist Validation with Intent Analysis

**AI Agent Instructions**: Based on file type detection results, spawn specialists using Task tool with MANDATORY intent validation:

**Step 3.1: MANDATORY Revolutionary Intent-Implementation Validation**
**BREAKTHROUGH VALIDATION (ALWAYS EXECUTED)**: 
```yaml
intent_implementation_spawning:
  validator: "intent-implementation-validator"
  location: "meta/validation/validators/ai-instruction/intent-implementation-validator.md"
  execution: "MANDATORY for every PR regardless of file types"
  timeout: "≤240s total processing time"
```

Use Task tool with parameters:
- **description**: "Revolutionary intent vs implementation semantic alignment validation"
- **prompt**: "You are an Intent-Implementation Alignment Validator specialist (BREAKTHROUGH TECHNOLOGY). Using the intent-implementation-validator from meta/validation/validators/ai-instruction/intent-implementation-validator.md, validate that this PR actually does what it claims to do. PR metadata: {pr_title}, {pr_description}, {pr_labels}. Changed files: {file_list}. Apply the 3-phase analysis: 1) Intent extraction and categorization, 2) Implementation analysis, 3) Semantic alignment scoring (0-100 scale). Generate detailed alignment assessment with ≥85% threshold for approval. This is the FIRST-EVER PR validation system that checks semantic alignment between stated intent and actual implementation."
- **context**: PR metadata, file changes, intent analysis framework
- **expected_tokens**: 120

**Step 3.2: Initialize Traditional Specialist Spawning Context**  
Set up tracking variables:
- `spawned_specialists`: List of successfully spawned specialists
- `spawned_specialists_count`: Count of successfully activated specialists  
- `spawning_failures`: Track any specialist spawning failures

**Step 3.3: Critical Priority File-Type Specialist Spawning**

**Claude Command Files (CRITICAL Priority)**  
If `claude_command_files` contains files:
1. Check if validator registry contains `claude-command-evaluator` 
2. **If validator exists**: Use Task tool with parameters:
   - **description**: "Validate Claude command files for AI Agent Instruction Design Excellence compliance"
   - **prompt**: "You are a Claude Command Evaluator specialist. Using the claude-command-evaluator from meta/validation/validators/ai-instruction/claude-command-evaluator.md, analyze files: {claude_command_files}. Apply validation criteria focusing on: concrete specificity, external dependency elimination, immediate actionability. Generate compliance report with specific recommendations for improvement."
   - **context**: Embed file list and validation criteria
   - **expected_tokens**: 60
3. **If validator missing**: Use embedded Claude Command validation logic (see Embedded Validators section)

**CLAUDE.md Project Files (CRITICAL Priority)**  
If `claude_md_files` contains files:
1. Check if validator registry contains `claude-project-file-validator`
2. **If validator exists**: Use Task tool with parameters:
   - **description**: "Validate CLAUDE.md project files using specialized Claude integration validator"
   - **prompt**: "You are a Claude Project File Validator specialist. Using the claude-project-file-validator from meta/validation/validators/project/claude-project-file-validator.md, analyze CLAUDE.md files: {claude_md_files}. Apply comprehensive validation focusing on: required elements (9 components), Claude integration excellence, cross-reference accuracy, and AI Agent Instruction Design Excellence compliance. Generate detailed validation report with specific improvement recommendations."
   - **context**: CLAUDE.md files list and Claude project validation requirements
   - **expected_tokens**: 100
3. **If validator missing**: Use embedded CLAUDE.md validation logic based on claude-project-file-validator patterns

**AI Agent Instruction Files (CRITICAL Priority)**  
If `ai_agent_files` contains files:
1. Check if validator registry contains `ai-agent-instruction-evaluator`
2. **If validator exists**: Use Task tool with parameters:
   - **description**: "Validate AI agent instruction files using Design Excellence Framework"
   - **prompt**: "You are an AI Agent Instruction Evaluator specialist. Using the ai-agent-instruction-evaluator from meta/validation/validators/ai-instruction/ai-agent-instruction-evaluator.md, analyze files: {ai_agent_files}. Apply assessment tools from the AI Agent Instruction Design Excellence framework including multi-level validation and constitutional AI compliance. Generate detailed compliance assessment with actionable recommendations."
   - **context**: Embed file list and framework assessment criteria
   - **expected_tokens**: 90
3. **If validator missing**: Use embedded AI instruction validation logic

**Step 3.3: High Priority Specialist Spawning**

**Project Documentation Files (HIGH Priority)**  
If `project_documentation_files` contains files:
1. Check if validator registry contains `project-documentation-validator`
2. **If validator exists**: Use Task tool with parameters:
   - **description**: "Validate project documentation files for AI agent effectiveness"
   - **prompt**: "You are a Project Documentation Validator specialist. Using the project-documentation-validator from meta/validation/validators/project/project-documentation-validator.md, analyze files: {project_documentation_files}. Apply validation criteria focusing on AI agent readability, framework compliance, cross-reference accuracy, and task management effectiveness. Generate detailed compliance assessment with actionable recommendations for project documentation improvement."
   - **context**: Embed project files list and mypromptflow framework requirements
   - **expected_tokens**: 80
3. **If validator missing**: Use embedded project documentation validation logic

**AI-Consumable Documentation Files (HIGH Priority)**  
If `ai_consumable_docs` contains files:
1. Check if validator registry contains `ai-documentation-validator`
2. **If validator exists**: Use Task tool with parameters:
   - **description**: "Validate AI-consumable documentation for effectiveness and actionability"
   - **prompt**: "You are an AI Documentation Validator specialist. Using the ai-documentation-validator from meta/validation/validators/project/ai-documentation-validator.md, analyze AI-consumable documentation files: {ai_consumable_docs}. Focus on technical clarity, implementation guidance, and AI agent actionability. Apply validation criteria for documentation structure, cross-reference integration, and technical quality. Generate comprehensive assessment with specific improvements for AI consumption effectiveness."
   - **context**: Project AI documentation files and technical documentation standards
   - **expected_tokens**: 100
3. **If validator missing**: Use embedded AI documentation validation logic

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
  🔧 Specialists activated: Based on binary file type detection
  ⚡ Resource efficiency: Conditional execution based on detected file types
  ❌ Spawning failures: [count] (fallbacks applied)
```

### Phase 4: Revolutionary Result Aggregation with Intent Analysis

**AI Agent Instructions**: Collect and synthesize results from spawned specialists including MANDATORY intent validation:

**Step 4.1: Wait for Specialist Completion with Intent Priority**  
Monitor Task tool executions until all spawned specialists complete:
- **Priority 1**: Intent-Implementation Validator (MANDATORY - must complete)
- **Priority 2**: Traditional file-type validators (conditional based on detected files)
- Apply timeout handling (maximum 300 seconds per specialist)
- If timeout occurs: Collect partial results and note incomplete specialists
- **Critical**: Intent validation must complete for PR approval determination

**Step 4.2: Revolutionary Intent-Implementation Result Collection**
**BREAKTHROUGH VALIDATION RESULTS**:
Extract critical metrics from intent-implementation-validator:
```yaml
intent_validation_results:
  overall_alignment_score: "[0-100]"
  confidence_level: "[high|medium|low|unreliable]"
  semantic_alignment: "[0-100]"
  scope_consistency: "[0-100]"  
  completeness: "[0-100]"
  critical_issues:
    scope_creep: "[none|minor|moderate|major]"
    missing_implementations: "[count and descriptions]"
    undisclosed_changes: "[count and descriptions]"
  approval_recommendation: "[APPROVE ≥85% | REVIEW <85% | BLOCK critical issues]"
```

**Step 4.3: Traditional Specialist Result Collection**  
For each completed file-type specialist, collect structured results:

**Result Collection Pattern**:
1. **Check Output Files**: Look for specialist result files in expected locations under `meta/validation/reports/pr-[number]/`
2. **Parse Structured Data**: Extract key metrics from specialist outputs:
   - Files processed count
   - Issues found with severity levels
   - Validation coverage percentage  
   - Specific recommendations generated
3. **Aggregate Metrics**: Combine individual specialist results

**Step 4.4: Calculate Enhanced Validation Metrics**  
Compute comprehensive validation effectiveness:
- `intent_alignment_score`: Score from intent-implementation-validator (0-100)
- `total_files_processed`: Sum from all file-type specialists
- `total_issues_found`: Sum of all detected issues across all validators
- `validation_coverage`: (total_files_processed / total_files_in_pr) × 100
- `resource_efficiency`: Based on conditional specialist activation plus mandatory intent validation

**Step 4.5: Generate Revolutionary Comprehensive Report**  
Output final validation results:
```
🚀 REVOLUTIONARY PR VALIDATION RESULTS FOR PR #[number]
══════════════════════════════════════════════════════════

🎯 BREAKTHROUGH INTENT-IMPLEMENTATION ANALYSIS:
  📊 Overall Alignment Score: [score]/100 ([APPROVE ≥85 | REVIEW <85 | BLOCK critical])
  🧠 Intent Analysis: [change_type] with [stated_scope]
  🔍 Implementation Reality: [files_changed] files, [core_changes] core, [unrelated_changes] unrelated
  ⚠️ Critical Issues: [scope_creep_level], [missing_implementations_count], [undisclosed_changes_count]
  💡 Confidence: [high|medium|low] ([percentage]%)

⏳ Traditional Specialist Execution Status:
  ✅ Completed: [count] specialists
  ⚠️ Partial/Timeout: [count] specialists
  ❌ Failed: [count] specialists

📊 File-Type Validation Coverage Analysis:
  📁 Total files in PR: [count]
  🎯 Files validated: [count]
  📈 Validation coverage: [percentage]%
  🔍 Issues found: [count] ([severity_breakdown])

⚡ Resource Efficiency Analysis:
  🚀 Total specialists spawned: [count] (Intent validator + [count] file-type validators)
  🔧 Revolutionary intent validation: ACTIVE (≥85% alignment threshold)
  ⚡ Resource efficiency: Conditional file-type specialist activation + mandatory intent validation
  📊 Data extraction: [Tier 1: gh CLI | Tier 2: git+gh | Tier 3: filesystem]

🎯 Critical Issues Requiring Attention:
  [Intent-implementation misalignments and traditional validator issues]

📋 Recommendations Summary:
  [Consolidated recommendations from intent validator and all file-type specialists]

✅ Revolutionary validation complete - Intent alignment: [score]/100 - Review recommendations for PR approval
```

**Step 4.6: Enhanced Result Persistence with Intent Tracking**  
Store comprehensive validation results for future reference:
- Create `meta/validation/reports/pr-[number]/` directory structure
- Store `intent-implementation-alignment.yaml` with semantic alignment analysis
- Create `comprehensive-analysis.md` with human-readable summary
- Store individual specialist reports in `specialist-reports/` subdirectory
- Update `meta/validation/reports/registry.yaml` with validation history tracking

## Revolutionary Validation Benefits

### Breakthrough Intent-Implementation Validation

**Industry-First Capabilities**:
- **Semantic Alignment Checking**: First-ever PR validation system that verifies PRs actually do what they claim
- **Scope Creep Detection**: Automatically identifies unrelated changes not mentioned in PR description
- **Implementation Completeness**: Validates that stated goals are actually implemented
- **Undisclosed Change Detection**: Flags breaking changes or significant modifications not documented

**Revolutionary Scenarios Detected**:
- PR says "Fix login validation bug" but includes unrelated UI redesign (scope creep detection)
- PR says "Add user authentication system" but missing test files (completeness validation)
- PR says "Update API documentation" but includes breaking API changes (undisclosed changes)
- PR says "Refactor database layer" but changes frontend components (scope consistency)

### Enhanced Resource Efficiency Approach

**Multi-Tier Fallback Strategy**:
- **Tier 1**: GitHub CLI integration for comprehensive PR metadata and diff extraction
- **Tier 2**: Combined git commands with basic gh metadata for fallback scenarios  
- **Tier 3**: File system analysis with pattern matching for offline/disconnected scenarios
- **Progressive Degradation**: Graceful handling of external dependency failures

**Conditional Activation Strategy**:
- **MANDATORY Intent Validation**: Always executes regardless of file types (revolutionary breakthrough)
- **Conditional File-Type Specialists**: Only activates specialists for detected file types
- **Targeted Context Loading**: Loads specific validation tools based on file analysis
- **Resource Benefits**: Optimal resource usage through intelligent specialist selection

### Enhanced Architecture Benefits

1. **Revolutionary Intent Validation**: Industry-first semantic alignment checking for PR intent vs implementation
2. **Multi-Tier Fallback Architecture**: Robust handling of GitHub CLI, git command, and file system access scenarios
3. **Asset Discovery**: Automatic detection of existing validators in reorganized `meta/validation/validators/` structure
4. **Conditional Loading**: Only loads file-type specialists for detected file types plus mandatory intent validation
5. **Scalable Design**: Adding new validators doesn't impact execution efficiency
6. **Production Ready**: Uses reorganized production validators with enhanced locations
7. **Gap Identification**: Clearly identifies missing file-type validators for future creation
8. **Resource Optimization**: Revolutionary intent validation + conditional file-type specialist activation

## Enhanced Validator Integration

### Revolutionary Validator (ALWAYS ACTIVE)
- **Intent-Implementation Validator**: `meta/validation/validators/ai-instruction/intent-implementation-validator.md` (BREAKTHROUGH TECHNOLOGY)

### Production-Ready Validators (Reorganized Locations)
- **Claude Command Evaluator**: `meta/validation/validators/ai-instruction/claude-command-evaluator.md`
- **AI Agent Instruction Evaluator**: `meta/validation/validators/ai-instruction/ai-agent-instruction-evaluator.md`
- **Claude Project File Validator**: `meta/validation/validators/project/claude-project-file-validator.md` (SPECIALIZED CLAUDE.md VALIDATION)

### File-Type Validator Gaps Identified (Ready for Creation)
- **TypeScript Frontend Validator**: `meta/validation/validators/file-type/typescript-frontend-validator.md`
- **Python Backend Validator**: `meta/validation/validators/file-type/python-backend-validator.md`
- **YAML Config Validator**: `meta/validation/validators/file-type/yaml-config-validator.md`
- **Test Validator**: `meta/validation/validators/file-type/test-validator.md`
- **JSON Schema Validator**: `meta/validation/validators/file-type/json-schema-validator.md`

### Enhanced Registry Integration

The command integrates with `meta/validation/validators/registry.yaml` for:
- Revolutionary intent-implementation-validator capability discovery
- Asset discovery for reorganized validator structure
- Capability mapping to file types with enhanced location tracking
- Gap identification for future validator development
- Progressive loading optimization with mandatory intent validation
- Validation reports storage in `meta/validation/reports/` structure

## Execution Instructions

When user runs `/validate-pr 23`, execute this revolutionary enhanced workflow:

1. **Enhanced Asset Discovery**: Read `meta/validation/validators/registry.yaml` for existing capabilities including revolutionary intent-implementation-validator
2. **Multi-Tier PR Data Extraction**: Use gh CLI (Tier 1) → git+gh (Tier 2) → filesystem (Tier 3) fallback strategy
3. **Revolutionary Intent Validation**: MANDATORY execution of intent-implementation-validator for semantic alignment checking (≥85% threshold)
4. **Conditional File-Type Spawning**: Spawn only relevant file-type specialists based on detected files
5. **Progressive Loading**: Load targeted validation components optimized for detected file types
6. **Enhanced Result Aggregation**: Collect results from intent validator (priority 1) and file-type specialists (priority 2)
7. **Revolutionary Reporting**: Document intent alignment score, scope creep detection, and traditional validation coverage
8. **Enhanced Persistence**: Store results in organized `meta/validation/reports/pr-[number]/` structure

## Implementation Notes

This command implements revolutionary PR validation using the **AI Agent Instruction Design Excellence Framework**:

### Revolutionary Enhancements
- **Industry-First Intent Validation**: Breakthrough semantic alignment checking between PR description and actual implementation
- **Multi-Tier Fallback Architecture**: Robust GitHub CLI → git commands → filesystem fallback strategy
- **Scope Creep Detection**: Automatic identification of unrelated changes not mentioned in PR description
- **Implementation Completeness**: Validation that stated goals are actually implemented

### Framework Compliance
- **Concrete Instructions**: Specific Claude tool usage (Task, Bash, Read, LS) with exact command patterns
- **Self-Sufficient**: References reorganized validator locations in `meta/validation/validators/` structure
- **Immediately Actionable**: Clear enhanced 4-phase execution workflow with intent validation priority
- **Resource Efficient**: Revolutionary intent validation + conditional file-type specialist spawning
- **External Dependency Elimination**: Multi-tier fallback strategies eliminate single points of failure

### Validator Integration
- **Reorganized Structure**: Integrates with new `meta/validation/validators/` organization
- **Progressive Loading**: Optimized context loading based on file type detection
- **Gap Identification**: Clear mapping of missing file-type validators for future development
- **Revolutionary Technology**: First-ever PR validation system ensuring PRs do what they claim to do

This enhanced command represents a breakthrough in PR validation technology, combining traditional file-type validation with revolutionary intent-implementation semantic alignment checking.