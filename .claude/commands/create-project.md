Create a new project using interactive planning process for: $ARGUMENTS

Conduct focused conversation to gather essential project information, then automatically create complete project structure with populated files.

**Execute interactive planning workflow:**

**Phase 1: Core Project Definition**
Ask: "What is this project and what specific outcome are you trying to achieve?"

Capture:
- Project name
- Project type (tool, framework, research, analysis, experiment)
- Core purpose and goals
- Success criteria

**Phase 2: Approach and Constraints**
Ask: "What's your preferred approach and any key constraints I should know about?"

Capture:
- Methodology preferences
- Technical constraints
- Timeline considerations
- Resource limitations
- Dependencies

**Phase 3: Knowledge Gaps (Optional)**
If project complexity suggests research needs, ask: "Any specific areas where you're unsure and might need research?"

Capture:
- User-identified uncertainty
- Knowledge gaps
- Research priorities

**Phase 4: Automatic Research Analysis**

After gathering user input:

**Scan Existing Research**
- Search @research/findings/ for relevant files
- Match project keywords to research topics
- Identify applicable research insights

**Identify Research Gaps**
- Based on project description, identify missing knowledge areas
- Suggest specific research topics that would benefit the project
- Prioritize research needs (high/medium/low)

**Present Research Integration**
Show user:
- "I found these relevant research files in our knowledge base:"
  - List specific files with brief descriptions
- "I recommend researching these topics to improve project success:"
  - List specific research gaps and why they matter

**Phase 5: Plan Presentation**

Present comprehensive plan including:
- **Project Summary**: Name, type, goals, approach, constraints
- **Research Integration**: Existing research to reference, research gaps to address
- **Proposed Structure**: Project folder and file organization
- **Initial Tasks**: Automatically generated task list based on project type and research needs
- **Next Steps**: Immediate actions for both implementation and research

**Phase 6: Project Creation (After User Approval)**

**Create Project Directory**
```bash
mkdir -p projects/[project-name]/docs
```

**Populate Template Files**
Use the _template/ files and replace placeholders with gathered information:

- **CLAUDE.md**: Complete AI agent instructions with full context
- **README.md**: Human-readable overview
- **project-purpose.md**: Detailed goals, scope, constraints
- **task-list.md**: Prioritized tasks including research tasks
- **progress.md**: Initial status entry
- **research-integration.md**: Research links and identified gaps

**Task Generation Strategy**

**Research Tasks (Always Include)**
- "Review [existing-research-file]" for each relevant research file
- "Research [specific-topic]" for each identified gap

**Planning Tasks (Based on Project Type)**
- "Define detailed project scope and requirements"
- "Create project roadmap with milestones" 
- "Analyze dependencies and constraints"

**Implementation Tasks (Project-Specific)**
- **Framework Projects**: "Design architecture", "Create core components", "Build integration layer"
- **Tool Projects**: "Define user interface", "Implement core functionality", "Create documentation"
- **Research Projects**: "Conduct primary research", "Synthesize findings", "Create analysis report"
- **Analysis Projects**: "Gather data sources", "Perform analysis", "Generate insights report"

**Validation Tasks (Always Include)**
- "Review progress against success criteria"
- "Validate research assumptions and findings"
- "Test deliverables against quality standards"

**Template Population Rules**

**Placeholder Replacement**
Replace template placeholders with actual project information:

- `{PROJECT_NAME}`: User-provided project name
- `{PROJECT_TYPE}`: Determined from conversation
- `{PROJECT_DESCRIPTION}`: User description
- `{PROJECT_GOALS}`: Extracted goals
- `{SUCCESS_CRITERIA}`: User-defined success criteria
- `{PROJECT_APPROACH}`: User preferences and methodology
- `{PROJECT_CONSTRAINTS}`: Identified limitations
- `{RESEARCH_CONTEXT}`: Research integration summary
- `{IMMEDIATE_NEXT_STEPS}`: First 1-3 tasks to begin work

**Dynamic Content Generation**

**Research Integration**
- **Existing Research**: List files with descriptions and relevance
- **Research Gaps**: Specific topics with rationale for why research is needed
- **Research Tasks**: Concrete, actionable research tasks

**Task List**
- **High Priority**: Research review tasks and critical planning tasks
- **Medium Priority**: Implementation tasks and detailed planning
- **Low Priority**: Nice-to-have features and advanced validation

**Example Conversation Flow**

```
User: /create-project

AI: I'll help you create a new project. Let me gather some key information first.

What is this project and what specific outcome are you trying to achieve?

User: I want to create an AI research framework that helps validate research quality

AI: What's your preferred approach and any key constraints I should know about?

User: I prefer modular design, need it to integrate with existing tools, and want it done in the next 2 months

AI: Based on your project description, I found these relevant research files:
- @research/findings/framework-analysis/comprehensive-ai-research-framework-gaps-and-recommendations.md
- @research/findings/orchestration/agent-orchestration-and-workflow-analysis.md

I recommend researching these topics:
- Framework validation methodologies
- Integration architecture patterns

[Present comprehensive plan]

Ready to create the project structure?
```

**Quality Standards**

**Conversation Quality**
- Ask focused, value-extracting questions
- Build on user responses naturally
- Suggest relevant research proactively
- Confirm understanding before proceeding

**Project Structure Quality**
- Complete, actionable task lists
- Clear, specific project documentation
- Meaningful research integration
- AI agent instructions that enable immediate work

**Information Completeness**
- All template placeholders populated with meaningful content
- Research integration includes both existing and needed research
- Tasks are specific, prioritized, and executable
- Project context is complete enough for any AI agent to understand and continue

**Success Criteria**

- User provides minimal input but gets maximum project structure
- Generated projects have complete context for AI agent continuity
- Research integration adds real value to project success
- Task lists enable immediate productive work
- Project documentation serves both human and AI needs effectively