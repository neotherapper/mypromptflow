# AI Knowledge Base System Instructions

## Core Requirements

**ALL AI Agents MUST**:

- Follow task completion protocol at `ai/workflows/task-management/CLAUDE.md` when completing tasks
- Apply development protocols at `development/CLAUDE.md` when doing development work
- Validate using meta framework at `meta/validation/validators/ai-instruction/` when validating instructions

## Essential Constraints

**Never**:

- Commit to master branch (use feature branches)
- Create files without registry similarity analysis for research

**Always**:

- Use MCP JIRA tools (mcp**MCP_DOCKER**jira\_\*)
- Execute parallel tool operations for efficiency
- Mark TodoWrite complete with timestamps
- Validate @file_path cross-references

## Research Framework

**Auto-Integration**: Research intentions trigger the research orchestrator automatically. Use `research/orchestrator/integration/claude-orchestrator-integration.yaml` when conducting research tasks.

## Quality Standards

**Validation Requirements**:

- AI instruction files: ≥75/100 validation score
- Task completion: 6-step protocol within ≤180 seconds
- Cross-reference accuracy: 100% file path accessibility
- Anti-fiction compliance: Use `meta/validation/anti-fiction-safeguards.md` when preventing fabricated claims

**Design Excellence**: Use `projects/ai-agent-instruction-design-excellence/CLAUDE.md` when creating AI instructions

- Concrete specificity (≥95% accuracy thresholds)
- External dependency elimination
- Immediate actionability standards
- Progressive context loading (68% token reduction)

## Key Cross-References

**Framework Access** (Load when needed):

- Tasks: `ai/workflows/task-management/CLAUDE.md`
- Development: `development/CLAUDE.md`
- Validation: `meta/validation/validators/ai-instruction/`
- Commands: `.claude/commands/*` - Use for standardized execution workflows

**Project Resources** (Load when working on specific projects):

- Design Excellence: `projects/ai-agent-instruction-design-excellence/CLAUDE.md`
- Claude Capabilities: `projects/ai-knowledge-base-enhancement/docs/claude-comprehensive-capabilities.md`
- MCP Registry: `projects/ai-knowledge-intelligence-orchestrator/docs/mcp-server-registry/`
- Task Lists: `projects/*/task-list.md`
- Progress: `projects/*/progress.md`

**Quality Assurance** (Load when quality issues arise):

- Anti-Fiction: `meta/validation/anti-fiction-safeguards.md`
- Command Guidelines: `meta/docs/claude-command-creation-guidelines.md`
- Intent Detection: `meta/shared/intention-detection-framework.md`
- MCP Learning: `meta/mcp-learning/` (error-logs/, usage-guides/, patterns/, templates/)

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
