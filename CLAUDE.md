# AI Knowledge Base Project Instructions

## Project Explanation

This project is an AI Knowledge Base system designed to build comprehensive business documentation using an orchestrated agent system.

## AI Research System

**Available to all AI agents:** This project includes a research framework at `research/` that any AI agent can use autonomously.

### Research Intention Detection

**Automatic Research Framework Activation:** Claude should automatically detect research intentions and activate the research orchestrator when users:

**Direct Research Triggers:**

- Use keywords: "research", "analyze", "investigate", "explore", "study", "examine", "assess", "evaluate"
- Ask for "comprehensive analysis", "in-depth look", "detailed examination", "systematic review"
- Request "help me understand", "what are the implications", "thorough investigation"

**Context-Based Triggers:**

- Multi-domain questions (contains "and", "intersection", "impact on", "relationship between")
- Emerging technology topics (AI, quantum, blockchain, etc.)
- Ethical implications or complex scenarios
- Comparative analysis ("compare", "contrast", "versus", "differences between")
- Strategic planning requests ("strategy", "roadmap", "implementation", "approach")

**When Research Framework Should Be Used:**

- Any request explicitly asking for research
- Questions involving multiple domains or perspectives
- Requests requiring structured systematic analysis
- Topics involving emerging or complex technologies
- When comprehensive coverage is needed
- Complex problem-solving that benefits from orchestrated methods

**Integration:** Read `research/orchestrator/integration/claude-orchestrator-integration.yaml` for complete workflow instructions when research intent is detected.

## MANDATORY Research Framework Compliance

**CRITICAL: All AI agents MUST follow these rules when conducting research:**

### 1. Complete 6-Step Orchestrator Workflow

When research intent is detected, you MUST follow ALL 6 steps from `research/orchestrator/integration/claude-orchestrator-integration.yaml`:

1. **step_1_detect_research_intent** - Verify research triggers match patterns
2. **step_2_extract_context** - Parse all required and optional parameters
3. **step_3_run_context_analysis** - Apply complexity assessment and domain analysis
4. **step_4_select_methods** - Use selection rules and method registry
5. **step_5_execute_methods** - Follow execution guidance with quality checkpoints
6. **step_6_orchestrator_summary** - MANDATORY orchestrator analysis summary

### 2. Research Documentation Requirements

After completing research, you MUST:

- **Create research execution log** using `research/templates/research-execution-log-template.yaml`
- **Save findings** in `research/findings/{topic}/` with proper structure:
  - `comprehensive-analysis.md` - Main research output
  - `research-metadata.yaml` - Following `research/metadata-schema.yaml` structure
  - `research-execution-log.yaml` - Complete execution tracking
- **Update research registry** in `research/findings/research-registry.yaml`

### 3. Research Metadata Schema Compliance

All research documents MUST include YAML frontmatter following `research/metadata-schema.yaml`:

```yaml
---
title: "Descriptive title of the research"
research_type: "primary|secondary|comparative|analysis"
subject: "Main subject being researched"
conducted_by: "AI agent identifier"
date_conducted: "ISO date"
date_updated: "ISO date"
version: "semver"
status: "draft|in_progress|completed|archived"
confidence_level: "high|medium|low"
---
```

### 4. Task List Update Requirements

After completing ANY research task, you MUST:

- **Mark task as completed** in relevant project `task-list.md`
- **Update progress.md** with research outcomes
- **Add new tasks** discovered during research
- **Update research-integration.md** with new findings and applications

### 5. Research Registry Integration

Every research session MUST update `research/findings/research-registry.yaml` with:

- Session metadata and quality scores
- Key outcomes and applications
- Research dependencies and relationships
- Integration points with project work

### 6. Quality Validation Requirements

All research MUST include:

- **Constitutional AI validation** for ethical compliance
- **Self-consistency verification** for accuracy
- **Quality checkpoints** during method execution
- **Success metrics** tracking and outcome assessment

**ENFORCEMENT:** Failure to follow these research framework rules will result in incomplete project documentation and poor research quality. These rules are MANDATORY for all AI agents working on this project.

## MANDATORY Task Completion Protocol

**CRITICAL: All AI agents MUST execute this protocol after completing ANY task:**

### Immediate Actions Required After Task Completion

1. **Update TodoWrite Tool**: IMMEDIATELY mark completed tasks in TodoWrite tool
2. **Update Project Task Lists**: Find and update relevant `task-list.md` files
3. **Document Progress**: Update `progress.md` with completion details
4. **Create Follow-up Tasks**: Add newly discovered tasks to TodoWrite and project task lists

### Specific Research Task Completion Protocol

When completing research tasks, AI agents MUST execute this exact sequence:

#### Step 1: Mark Research Complete in TodoWrite

```
Use TodoWrite tool to mark research task as "completed"
```

#### Step 2: Update Project Task List Files

**FIND**: Locate all `projects/*/docs/task-list.md` files
**UPDATE**: Change research task status from `[ ]` to `[x]` with timestamp
**EXAMPLE**: `- [x] **Research AI validation frameworks** (Completed: 2025-01-06)`

#### Step 3: Add Implementation Tasks

Based on research findings, ADD these tasks to project task-list.md:

- `[ ] Plan [research topic] implementation based on findings`
- `[ ] Design [research topic] system architecture`
- `[ ] Implement [research topic] in appropriate @ai/ directory`

#### Step 4: Update Progress Documentation

**FIND**: `projects/*/docs/progress.md`
**ADD**: Detailed completion entry with research outcomes and next steps

### Task Update Template for AI Agents

**When updating task-list.md files, use this exact format:**

```markdown
## Recently Completed (Auto-updated by AI Agent)

- [x] **[Task Name]** (Completed: [YYYY-MM-DD HH:MM])
  - **Findings**: [Key research outcomes]
  - **Next Steps**: [Implementation tasks created]
  - **Files Created**: [List of research documents]

## Next Priority Tasks (Auto-generated)

- [ ] **Plan [topic] implementation** (Priority: High)
- [ ] **Design [topic] system** (Priority: Medium)
```

### Enforcement Through AI Agent Instructions

**AI agents MUST say these exact words after completing research:**

"I have completed the research task. Now executing mandatory task completion protocol:

1. ✅ Updating TodoWrite tool with completion status
2. ✅ Locating and updating project task-list.md files
3. ✅ Adding implementation tasks based on research findings
4. ✅ Updating progress documentation with outcomes"

**If an AI agent does NOT execute this protocol, they have violated project requirements.**

### Cross-Project Task Synchronization

**AI agents MUST check these locations for task updates:**

- `projects/ai-knowledge-base-enhancement/docs/task-list.md`
- Local TodoWrite tool state
- `projects/*/docs/progress.md` files

**Synchronization Rule**: TodoWrite tool is the master task tracker. Project task-list.md files must mirror TodoWrite status.

### Task Discovery and Creation Protocol

**When research reveals new tasks, AI agents MUST:**

1. **Immediately add to TodoWrite** with appropriate priority
2. **Add to project task-list.md** in relevant sections
3. **Update research-integration.md** with task dependencies
4. **Estimate effort** and add priority classification

### Quality Assurance for Task Updates

**Before completing any session, AI agents MUST verify:**

- [ ] All completed tasks marked in TodoWrite tool
- [ ] All relevant task-list.md files updated
- [ ] Progress.md reflects current status
- [ ] New tasks added based on discoveries
- [ ] Research findings properly documented

**ENFORCEMENT:** Any AI agent that fails to execute this task completion protocol has failed to follow project requirements and must restart their task completion process.

## Development Workflow

- **NEVER** commit directly to the `master` branch.
- Always create a new feature branch for your work.

For maximum efficiency, whenever you need to perform multiple independent operations, invoke all relevant tools simultaneously rather than sequentially.
