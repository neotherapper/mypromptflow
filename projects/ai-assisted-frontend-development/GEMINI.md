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
├── CLAUDE.md               # AI CLAUDE agent instructions and project context
├── GEMINI.md               # AI GEMINI agent instructions and project context
├── README.md               # Human-readable project overview
├── project-purpose.md      # Goals and success criteria
├── task-list.md           # Current tasks with priorities and status
├── progress.md            # What's been accomplished
├── research-integration.md # Research links and identified gaps
└── docs/                  # Project artifacts and documentation
```

## How to Work with Projects

### For AI Agents

1. **Read GEMINI.md first** - This contains all the context you need about the project
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

- AI identifies areas where additional research would benefit the project
- Research tasks are created for knowledge gaps
- New research feeds back into the research framework

## Quality Standards

### Project Documentation

- Clear, concise project purpose and goals
- Specific, actionable tasks with priorities
- Regular progress updates with concrete outcomes
- Integration with relevant research findings

### AI Agent Instructions

- Complete context for understanding the project
- Clear guidance on how to approach tasks
- Specific preferences and constraints
- Quality criteria for deliverables

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

- Provide clear, specific project descriptions
- Identify constraints and preferences upfront
- Link to relevant existing knowledge
- Define concrete success criteria

### For Project Execution

- Work on highest priority tasks first
- Update progress regularly
- Add new tasks as understanding evolves
- Validate work against original goals

### For AI Agents

- Always read GEMINI.md to understand project context
- Check research-integration.md for relevant knowledge
- Update progress and task lists when making changes
- Maintain quality standards defined in project documentation

This framework enables systematic project development while maintaining the flexibility and intelligence that makes AI agents effective collaborators.