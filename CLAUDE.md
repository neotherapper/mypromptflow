# AI Knowledge Base System Instructions

## Core Requirements

**ALL AI Agents MUST**:

- Follow task completion protocol when completing tasks: `ai/workflows/task-management/CLAUDE.md`
- Apply development protocols when doing development work: `development/CLAUDE.md`
- Validate using meta framework when validating instructions: `meta/validation/validators/ai-instruction/`

## Essential Constraints

**Never**:

- Commit to master branch (use feature branches)
- Create files without registry similarity analysis for research

**Always**:

- Use MCP JIRA tools (mcp**MCP_DOCKER**jira\_\*)
- Execute parallel tool operations for efficiency
- Mark TodoWrite complete with timestamps
- Validate @file_path cross-references
- Apply unified source discovery framework for research and validation tasks

## System Overview

**AI Knowledge Base Development** (Critical Infrastructure, Tier 1)
Self-sufficient system using 4-level agent hierarchy (Queen→Architect→Specialist→Worker) with research capabilities and progressive context loading.

**Three-Layer Architecture**:

- **AI Orchestration** (`ai/`) - Multi-agent coordination, 40+ document templates available, feature orchestrators
- **Knowledge Vault** (`knowledge-vault/`) - Structured YAML databases, change detection, cross-domain mapping
- **Research & Projects** (`research/`, `projects/`) - Advanced orchestrator with 15+ methodologies, meta-framework patterns

## AI Research & Quality Standards

**Auto-Integration**: Research intentions trigger orchestrator automatically using `research/orchestrator/integration/claude-orchestrator-integration.yaml`

**Research Requirements**:

- MANDATORY registry similarity analysis (≥95% compliance)
- 8-step orchestrator workflow with constitutional AI validation (≥95% accuracy)
- Enhanced file structure: research/findings/[topic]/ with .meta/ folder
- Universal intention detection: `meta/shared/intention-detection-framework.md`

**Quality Standards**:

- AI instruction files: ≥75/100 validation score
- Task completion: 6-step protocol within ≤180 seconds
- Cross-reference accuracy: 100% file path accessibility
- Anti-fiction compliance: `meta/validation/anti-fiction-safeguards.md`
- Design excellence: `projects/ai-agent-instruction-design-excellence/CLAUDE.md`

## Context Loading Strategy

**Immediate Loading** (@ prefix): Essential context needed for all operations

- Core requirements and constraints (this file)
- Quality standards and anti-fiction safeguards
- Essential cross-references for project coordination

**Conditional Loading** (bare paths): Load specific contexts when needed

- `development/CLAUDE.md` - When doing development work
- `ai/workflows/task-management/CLAUDE.md` - When managing tasks
- `research/orchestrator/integration/claude-orchestrator-integration.yaml` - When conducting research
- `meta/validation/validators/ai-instruction/` - When validation issues arise

**Usage Pattern**: Reference files using conditional format: "Use `file/path.md` when [specific condition]" rather than immediate @ loading to optimize context efficiency.

## Essential Protocols

### Information Access Framework (Universal)

**Unified Source Discovery**: Use `meta/information-access/source-discovery-framework.yaml` for ALL research and validation tasks

**5-Step Implementation**:
1. **Topic Analysis**: Extract technology (React, TypeScript, Python) or domain (frontend, backend, database)
2. **Mapping Selection**: Use technology_mappings (specific) or category_mappings (general)
3. **Source Coordination**: Apply primary + supplementary + validation sources
4. **Error Handling**: Implement MCP fallbacks and authentication recovery
5. **Attribution**: Document all sources for research-sources.md tracking

**Agent Usage Guide**: `meta/information-access/agent-usage-guide.md` - Complete implementation instructions

**Decision Logic**:
- **Specific Technology Detected** → Use technology_mappings.react/typescript/python/database
- **Domain Category Match** → Use category_mappings.frontend/backend/infrastructure
- **No Clear Match** → Use knowledge-vault fallback with information-sources-by-type view

### Task Management (≤180 seconds)

1. Mark TodoWrite complete with timestamps
2. Update projects/\*/task-list.md synchronously
3. Document outcomes in progress.md with scores
4. Create follow-up tasks with priorities
5. Validate @file_path cross-references
6. Verify completion criteria

### AI Instruction Standards

- Eliminate human documentation artifacts (Purpose, Overview, Usage sections forbidden)
- Start with direct actionable instructions (no titles or explanations)
- Achieve ≥75/100 validation score using meta validation tools
- Ensure 100% @file_path cross-reference accessibility

### Anti-Fiction Safeguards

- Verify all numerical claims with sources (file_path:line_number format)
- Label data type clearly: Verified/Estimated/Analysis/Unknown
- Maintain cognitive separation between academic analysis and operational execution
- Restrict knowledge-vault access to explicitly authorized research tasks

### MCP Error Learning

1. **BEFORE MCP usage**: Check `meta/mcp-learning/usage-guides/[server-name]-guide.md` for known issues
2. **WHEN errors occur**: Log immediately using `meta/mcp-learning/templates/error-log-template.md`
3. **AFTER success**: Update usage guides with working patterns

## Key Resources

**Framework Access** (Load when needed):

- Tasks: `ai/workflows/task-management/CLAUDE.md`
- Development: `development/CLAUDE.md`
- Validation: `meta/validation/validators/ai-instruction/`
- Commands: `.claude/commands/*`
- Information Access: `meta/information-access/agent-usage-guide.md`

**Project Resources** (Load when working on specific projects):

- Design Excellence: `projects/ai-agent-instruction-design-excellence/CLAUDE.md`
- Claude Capabilities: `projects/ai-knowledge-base-enhancement/docs/claude-comprehensive-capabilities.md`
- MCP Registry: `projects/ai-knowledge-intelligence-orchestrator/mcp-registry/`
- Task Lists: `projects/*/task-list.md`
- Progress: `projects/*/progress.md`

**Quality Assurance** (Load when quality issues arise):

- Anti-Fiction: `meta/validation/anti-fiction-safeguards.md`
- Command Guidelines: `meta/docs/claude-command-creation-guidelines.md`
- Intent Detection: `meta/shared/intention-detection-framework.md`
- MCP Learning: `meta/mcp-learning/` (error-logs/, usage-guides/, patterns/, templates/)

**System Configuration** (Reference when needed):

- AI Context: `ai/context/` (dependencies.yaml, document-registry.yaml, feature-registry.yaml, tier-configuration.yaml)
- Knowledge Vault: `knowledge-vault/` (schemas/, shared/, operations/)
- Research: `research/` (findings/, orchestrator/, sessions/)
- Information Access: `meta/information-access/` (source-discovery-framework.yaml, agent-usage-guide.md, topic-mappings/, category-mappings/)

## Command Integration

**Basic Workflows**: Use `development/CLAUDE.md` for complete development commands and workflows
