# Projects Framework

## Overview

This projects framework provides a structured approach to managing mini-projects where AI agents can understand the complete project context and continue work seamlessly. Each project is self-contained with all necessary context for any AI agent to understand and contribute effectively.

## Key Concepts

- **Self-Documenting Projects**: Each project folder contains complete context in standardized files
- **Research Integration**: Projects automatically link to relevant research findings and identify knowledge gaps
- **AI Agent Continuity**: Any AI agent can read a project folder and understand what to do next
- **Task-Oriented Workflow**: Projects are organized around executable tasks with clear priorities

## Project Structure

Every project follows this standard structure:

```
projects/[project-name]/
├── CLAUDE.md               # AI agent instructions and project context
├── README.md               # Human-readable project overview
├── project-purpose.md      # Goals and success criteria
├── task-list.md           # Current tasks with priorities and status
├── progress.md            # What's been accomplished
├── research-integration.md # Research links and identified gaps
└── docs/                  # Project artifacts and documentation
```

## How to Work with Projects

### For AI Agents

1. **Read CLAUDE.md first** - This contains all the context you need about the project
2. **Check task-list.md** - Find the highest priority uncompleted task
3. **Review research-integration.md** - Understand relevant research context
4. **Update progress.md** - Document what you accomplish
5. **Update task-list.md** - Mark tasks complete and add new ones as needed

### For Users

1. **Use `/create-project` command** - Interactive setup that gathers project context
2. **Review generated files** - AI creates comprehensive project documentation
3. **Add tasks as needed** - Update task-list.md with new requirements
4. **Monitor progress** - Check progress.md for status updates

## Task Management

### Task Categories

- **Research Tasks**: Review existing research or conduct new research
- **Planning Tasks**: Define scope, create roadmaps, analyze requirements
- **Implementation Tasks**: Execute the main project work
- **Validation Tasks**: Review progress and validate outcomes

### Task Format

```markdown
- [ ] Task description [Priority: High/Medium/Low] [Type: Research/Planning/Implementation/Validation]
```

### Task Execution

- AI agents work on highest priority available tasks
- Research tasks can trigger the research orchestrator when needed
- Completed tasks automatically update progress tracking
- New tasks are added based on project evolution

## Research Integration

### Existing Research

- AI automatically scans @research/findings/ for relevant content
- Projects link to applicable research files
- Research insights inform project decisions

### Research Gaps

- Execute gap analysis protocol to identify research needs (complexity scoring: 1-5 scale, benefit assessment: quantified impact estimation)
- Generate research tasks using standardized format (scope definition, success criteria, resource requirements, timeline constraints)
- Integrate research findings through systematic update procedures (relevance scoring, cross-reference validation, knowledge base synchronization)

## Quality Standards

### Project Documentation

- Project purpose and goals with measurable success criteria (completion thresholds: ≥95%, timeline adherence: ≤110% of planned duration)
- Tasks with explicit execution steps, effort estimates (hours), and priority levels (High/Medium/Low)
- Progress updates with completion percentages, quality scores, and milestone tracking (update frequency: ≤48h intervals)
- Integration with relevant research findings

### AI Agent Instructions

- Complete context including project scope, dependencies, success metrics, and failure criteria
- Step-by-step task execution guidance with decision criteria and validation checkpoints
- Explicit preferences (tools, methodologies, formats) and hard constraints (timeframes, resource limits, quality thresholds)
- Measurable quality criteria (accuracy: ≥95%, completeness: ≥90%, consistency: ≥88%) for all deliverables

## Integration with Existing Systems

### Research Framework

- Projects automatically suggest relevant research files
- Research gaps trigger research orchestrator workflows
- Research findings update project context

### AI Knowledge Base

- Projects can reference @ai/knowledge/ documents
- Project outcomes can inform knowledge base updates
- Shared patterns improve future project creation

## Commands

- **`/create-project`**: Interactive project creation with research integration
- AI agents can also reference projects in their work across the system

## Best Practices

### For Project Creation

- Provide project descriptions with scope boundaries, deliverable specifications, and timeline parameters
- Document constraints (budget limits, technical requirements, resource availability) and preferences (tools, methodologies, communication patterns) using structured formats
- Establish cross-references to @research/findings/ and @ai/knowledge/ with relevance scores and dependency mapping
- Define success criteria using measurable metrics (completion rate: ≥95%, quality score: ≥4.0/5.0, timeline adherence: ≤110%)

### For Project Execution

- Execute tasks using priority ordering algorithm (High: ≤24h response, Medium: ≤72h, Low: ≤168h)
- Update progress using standardized tracking format (completion percentage, quality score, time spent, issues encountered) within ≤48h intervals
- Generate new tasks through systematic discovery protocol (dependency analysis, gap identification, risk assessment) with effort estimates and priority classification
- Validate deliverables against defined success criteria using measurement protocols (accuracy verification, completeness checking, consistency validation)

### For AI Agents

- Always read CLAUDE.md to understand project context
- Check research-integration.md for relevant knowledge
- Update progress and task lists when making changes
- Maintain quality standards defined in project documentation

This framework enables systematic project development while maintaining the flexibility and intelligence that makes AI agents effective collaborators.
