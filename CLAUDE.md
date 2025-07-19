# AI Knowledge Base Project Instructions

## Project Explanation

**Project Type**: AI Knowledge Base Development
**Current Status**: Research Framework Operational
**Priority Level**: Critical Infrastructure (Tier 1)
**Success Threshold**: ≥95% research quality score, ≤4.2ms response time, 0 external dependencies

This project creates a self-sufficient AI Knowledge Base system using 4-level agent hierarchy (Queen→Architect→Specialist→Worker) with research capabilities and progressive context loading (60-70% token reduction).

## AI Research System

**Available to all AI agents:** This project includes a research framework at `research/` that any AI agent can use autonomously. Framework provides: 6-step orchestrator workflow, automated execution logging, metadata compliance, and constitutional AI validation (≥95% accuracy).

### Research Intention Detection

**Automatic Research Framework Activation:** Claude MUST automatically detect research intentions and activate the research orchestrator (≤30 seconds) when users:

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

**Integration:** Execute @research/orchestrator/integration/claude-orchestrator-integration.yaml

**Activation Triggers**: "research", "analyze", "investigate", "explore", "study", "examine", "assess", "evaluate"

**Quality Threshold**: ≥95% constitutional compliance, ≤300s total execution time

**Fallback Protocol** (if @research/ unavailable): Basic 6-step sequence → Intent Detection → Context Extraction → Complexity Assessment → Method Selection → Execution → Summary Generation

## MANDATORY Research Framework Compliance

**CRITICAL: All AI agents MUST follow these rules when conducting research:**

### 1. Complete 6-Step Orchestrator Workflow

When research intent is detected, you MUST follow ALL 6 steps using embedded orchestrator workflow (no external dependencies):

**Research Orchestrator Steps** (Full details: @research/orchestrator/integration/claude-orchestrator-integration.yaml):
1. **Intent Detection** (≤15s): Pattern matching, ≥85% confidence threshold
2. **Context Extraction** (≤30s): Parse scope, domain, quality requirements
3. **Complexity Assessment** (≤45s): 1-5 scoring, ≥3.5 = comprehensive research
4. **Method Selection** (≤60s): 12 validated methods, auto-select based on complexity
5. **Execution** (≤300s): Constitutional AI validation (accuracy≥95%, completeness≥90%)
6. **Summary Generation** (≤120s): YAML frontmatter + findings + recommendations

### 2. Research Documentation Requirements

After completing research, execute documentation protocol (≤180s total):

**Templates**: Use @research/templates/research-execution-log-template.yaml
**Schema**: Follow @research/metadata-schema.yaml structure
**Registry**: Update @research/findings/research-registry.yaml

**Required Outputs**:
- Research execution log with quality scores
- Structured findings in `research/findings/{topic}/`
- Registry entry with cross-references
- Validation of all files and metadata

### 3. Research Metadata Schema Compliance

All research documents MUST include YAML frontmatter following @research/metadata-schema.yaml:

**Required Fields**: title, research_type, subject, conducted_by, dates, version, status
**Quality Metrics**: confidence_level, accuracy_score, completeness_score, consistency_score
**Validation**: 100% completion required, enum validation for type/status fields

**Full Schema**: @research/metadata-schema.yaml

### 4. Task List Update Requirements

After completing ANY research task, you MUST execute this 4-step completion protocol (Target: ≤120 seconds total):

**Step 1: Task Status Update** (≤30s): Mark completed in TodoWrite tool + locate and update ALL relevant `projects/*/docs/task-list.md` files with completion timestamp

**Step 2: Progress Documentation** (≤45s): Update `progress.md` with specific outcomes:
- Research quality scores (accuracy, completeness, consistency)
- Key findings summary (3-5 concrete discoveries)
- Implementation impact assessment
- Next action recommendations with priority scores

**Step 3: Task Discovery** (≤30s): Add newly discovered tasks to TodoWrite + project task-list.md with:
- Specific priority level (High/Medium/Low)
- Estimated effort (hours)
- Dependencies identified
- Success criteria defined

**Step 4: Integration Update** (≤15s): Update `research-integration.md` with new findings, applications, and validated cross-references

### 5. Research Registry Integration

Every research session MUST update @research/findings/research-registry.yaml (≤60s):

**Required Data**: Session metadata, quality scores (0.00-1.00 scale), key outcomes, dependencies, integration points
**Registry Format**: @research/findings/research-registry.yaml structure

### 6. Quality Validation Requirements

All research MUST include validation (≤90s total):

**Constitutional AI Validation**: ≥95% score across 5 principles (accuracy, transparency, completeness, responsibility, integrity)
**Self-Consistency Verification**: ≥85% consistency score
**Quality Checkpoints**: Real-time monitoring with threshold alerts
**Success Metrics**: Completion time, quality scores, actionable recommendations

**Full Validation Procedures**: @research/orchestrator/integration/claude-orchestrator-integration.yaml

**ENFORCEMENT PROTOCOL:** Failure to follow research framework rules triggers escalation: quality penalty, research invalidation, agent review. ≥95% compliance required.

These rules are MANDATORY for all AI agents working on this project.

## MANDATORY Task Completion Protocol

**CRITICAL: All AI agents MUST execute this 6-step protocol after completing ANY task (Target: ≤180 seconds total execution time):**

### Immediate Actions Required After Task Completion

1. **TodoWrite Update** (≤15s): IMMEDIATELY mark completed tasks as "completed" status with timestamp
2. **Project Task Lists Update** (≤45s): Locate ALL `projects/*/docs/task-list.md` files and update status from `[ ]` to `[x]` with completion timestamp
3. **Progress Documentation** (≤60s): Update `progress.md` with specific completion details: outcomes achieved, quality scores, time spent, issues encountered
4. **Follow-up Task Creation** (≤45s): Add newly discovered tasks to TodoWrite + project task lists with priority levels (High/Medium/Low) and effort estimates
5. **Cross-Reference Validation** (≤10s): Verify all @file_path references are accessible and accurate
6. **Quality Verification** (≤5s): Confirm completion meets success criteria defined in task description

### Specific Research Task Completion Protocol

When completing research tasks, AI agents MUST execute this exact 4-step sequence (Target: ≤240 seconds total):

#### Step 1: TodoWrite Completion Marking (≤15 seconds)

**Required Action**: Use TodoWrite tool to mark research task status as "completed" with completion timestamp and quality score summary

**Validation**: Verify task marked as completed before proceeding to Step 2

#### Step 2: Project Task List Synchronization (≤60 seconds)

**FIND** (≤20s): Scan all `projects/*/docs/task-list.md` files using pattern matching for task references
**UPDATE** (≤30s): Change research task status from `[ ]` to `[x]` with timestamp and quality score
**VALIDATION** (≤10s): Verify synchronization between TodoWrite and project task lists

**Required Format**: `- [x] **Research Topic** (Completed: YYYY-MM-DD HH:MM, Quality: X.X/5.0, Confidence: XX%)`

#### Step 3: Implementation Task Generation (≤90 seconds)

Based on research findings, ADD these specific tasks to project task-list.md with measurable criteria:

**Required Tasks** (≤60s):
- `[ ] Plan [research topic] implementation (Priority: High, Effort: Xh, Dependencies: [list])`
- `[ ] Design [research topic] system architecture (Target: 95% framework alignment, <48h completion)`
- `[ ] Implement [research topic] in @ai/[specific_directory]/ (Success: functional prototype, test coverage ≥85%)`

**Quality Gates** (≤20s): Each task must include success criteria, time estimates, and dependency validation

**Validation** (≤10s): Verify tasks added to both TodoWrite and project task-list.md with consistent formatting

#### Step 4: Progress Documentation Update (≤75 seconds)

**FIND** (≤15s): Locate all relevant `projects/*/docs/progress.md` files using project scope analysis
**ADD** (≤60s): Detailed completion entry with measurable outcomes:

**Required Content Structure**:
```markdown
## Research Completion: [Topic] (YYYY-MM-DD HH:MM)

**Quality Metrics**:
- Accuracy Score: X.XX/1.00
- Completeness Score: X.XX/1.00
- Constitutional Compliance: XX%
- Execution Time: XXX seconds (Target: ≤300s)

**Key Findings** (3-5 concrete discoveries):
1. [Specific finding with supporting evidence]
2. [Actionable insight with implementation potential]

**Next Steps** (Priority-ranked actions):
- [High Priority Action] (Target completion: within 24h)
- [Medium Priority Action] (Target completion: within 72h)

**Integration Impact**: [How findings affect existing project work]
```

### Task Update Template for AI Agents

**When updating task-list.md files, use this exact format with measurable criteria:**

```markdown
## Recently Completed (Auto-updated by AI Agent - Timestamp: YYYY-MM-DD HH:MM)

- [x] **[Task Name]** (Completed: YYYY-MM-DD HH:MM, Quality: X.X/5.0, Duration: XXXs)
  - **Quality Metrics**: Accuracy X.XX, Completeness X.XX, Consistency X.XX
  - **Key Findings**: [3-5 specific, actionable discoveries]
  - **Implementation Tasks Created**: [List with effort estimates]
  - **Files Generated**: [List with validation status]
  - **Cross-References Updated**: [Count of @file_path references validated]

## Next Priority Tasks (Auto-generated with Success Criteria)

- [ ] **Plan [topic] implementation** (Priority: High, Effort: Xh, Success: 95% framework alignment)
- [ ] **Design [topic] system architecture** (Priority: Medium, Target: <48h, Success: functional specification)
- [ ] **Validate implementation readiness** (Priority: Low, Dependencies: [list], Success: all prerequisites met)
```

### Enforcement Through AI Agent Instructions

**AI agents MUST execute and report this exact protocol after completing research (Target: complete within 240 seconds):**

"Research task completed. Executing mandatory 6-step completion protocol:

1. ✅ TodoWrite tool updated (Status: completed, Quality: X.X/5.0, Duration: XXXs)
2. ✅ Project task-list.md files synchronized (Files updated: X, Cross-references validated: X)
3. ✅ Implementation tasks generated (Tasks created: X, Total effort estimated: Xh)
4. ✅ Progress documentation updated (Findings documented: X, Next steps prioritized: X)
5. ✅ Cross-references validated (Accuracy: 100%, Broken links: 0)
6. ✅ Quality verification complete (Constitutional compliance: XX%, Success criteria: met)

Protocol execution time: XXX seconds (Target: ≤240s)"

**ENFORCEMENT**: AI agents that do NOT execute this protocol within 240 seconds trigger automatic escalation and task re-assignment.**

### Cross-Project Task Synchronization

**AI agents MUST check these specific locations for task updates (Target: ≤60 seconds scan time):**

**Primary Sources** (≤30s):
- `projects/ai-knowledge-base-enhancement/docs/task-list.md` - Master project task list
- Local TodoWrite tool state - Real-time task tracking with timestamps
- `projects/*/docs/progress.md` files - Historical completion records

**Secondary Sources** (≤30s):
- `research/findings/research-registry.yaml` - Research task completion tracking
- `projects/*/docs/research-integration.md` - Cross-project task dependencies

**Synchronization Protocol**: TodoWrite tool = master task tracker. Project task-list.md files MUST mirror TodoWrite status within 15 seconds of updates. Validation: 100% consistency required.

### Task Discovery and Creation Protocol

**When research reveals new tasks, AI agents MUST execute this 4-step protocol (≤120 seconds):**

1. **TodoWrite Addition** (≤30s): Add tasks with specific attributes:
   - Priority: High (research-critical), Medium (implementation), Low (optimization)
   - Effort: Hours estimate based on complexity score
   - Dependencies: List prerequisite tasks/knowledge
   - Success criteria: Measurable completion definition

2. **Project Task-list Integration** (≤45s): Add to relevant `projects/*/docs/task-list.md` sections with consistent formatting and cross-references

3. **Research-Integration Update** (≦30s): Update `research-integration.md` with:
   - Task dependencies mapping
   - Priority impact assessment
   - Cross-project implications
   - Timeline coordination requirements

4. **Effort Estimation & Classification** (≤15s): Apply effort calculation formula: (complexity_score × 1.5) + (dependency_count × 0.5) = estimated_hours

### Quality Assurance for Task Updates

**Before completing any session, AI agents MUST verify this 5-point checklist (≤90 seconds verification):**

**Task Tracking Verification** (≤25s):
- [ ] All completed tasks marked as "completed" in TodoWrite tool with timestamps
- [ ] All relevant `projects/*/docs/task-list.md` files updated with completion status
- [ ] 100% synchronization between TodoWrite and project task lists verified

**Documentation Verification** (≤30s):
- [ ] `progress.md` reflects current status with quality scores and completion metrics
- [ ] New tasks added to both TodoWrite and project task lists with proper formatting

**Quality Verification** (≤35s):
- [ ] Research findings documented with constitutional compliance ≥95%
- [ ] All @file_path cross-references validated and accessible
- [ ] Success criteria met for all marked-complete tasks
- [ ] Quality scores recorded (accuracy, completeness, consistency) for research outputs
- [ ] Next session priorities clearly defined with effort estimates

**ENFORCEMENT PROTOCOL:** Any AI agent that fails to execute this task completion protocol triggers automatic escalation:

**Immediate Actions**:
- Task marked as "incomplete" and flagged for review
- Agent performance score penalty (-0.5 points)
- Automatic notification to session supervisor

**Escalation Thresholds**:
- 1st failure: Warning + protocol re-execution requirement
- 2nd failure: Session supervision requirement
- 3rd failure: Agent retraining and capability assessment

**Recovery Process**: Failed agents must restart task completion protocol within 300 seconds and achieve 100% compliance before proceeding to new tasks.

## Development Workflow

**Git Workflow Protocol** (MANDATORY):
- **NEVER** commit directly to the `master` branch (automated prevention: merge conflicts will result)
- **ALWAYS** create feature branch: `git checkout -b feature/[descriptive-name]` (naming convention: feature/task-description-YYYY-MM-DD)
- **REQUIRED**: All commits must pass pre-commit validation (quality score ≥85%, no external dependencies)

**Efficiency Protocol**:
- **Parallel Tool Execution**: When performing multiple independent operations, invoke ALL relevant tools simultaneously rather than sequentially
- **Target Efficiency**: 60-70% time reduction through parallel processing
- **Quality Maintenance**: Parallel execution must maintain ≥95% accuracy and ≥90% consistency scores

**Claude Integration Optimization**:
- **Automatic Context Loading**: Leverage Claude's recursive file discovery for project understanding
- **Cross-Reference Utilization**: Use @file_path patterns for efficient internal navigation
- **Command System Integration**: Reference .claude/commands/ for automated workflow execution
- **Memory Persistence**: Structure work for Claude's three-tier memory system (project/user/dynamic)

## Claude Integration Optimization

**Claude's Capabilities**: Automatic context loading, three-tier memory (project/user/dynamic), multi-file awareness, cross-reference resolution

**Key Cross-References**:
```
@research/orchestrator/integration/claude-orchestrator-integration.yaml
@research/metadata-schema.yaml
@research/templates/research-execution-log-template.yaml
@projects/*/docs/task-list.md
@projects/*/docs/progress.md
@.claude/commands/* (when available)
```

**Progressive Context Loading**: 60-70% token reduction through hierarchical access and smart loading

**Memory System**: Leverage Claude's session persistence and automatic discovery patterns

**Full Integration Details**: @projects/ai-knowledge-base-enhancement/docs/claude-comprehensive-capabilities.md
