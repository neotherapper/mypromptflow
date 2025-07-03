Orchestrate agent workflow to create: $ARGUMENTS

## Orchestration Process:

1. **Dependency Analysis Phase**

   - Use /analyze-dependencies $ARGUMENTS
   - Identify all missing documents
   - Create execution plan

2. **Agent Spawning Phase**
   For each missing document in parallel_group:

   - Create specialized agent prompt
   - Include relevant context paths
   - Set quality criteria
   - Spawn agent with specific focus

3. **Coordination Phase**

   - Monitor agent progress
   - Share outputs between dependent agents
   - Handle conflicts or clarifications
   - Validate outputs against requirements

4. **Synthesis Phase**
   - Collect all agent outputs
   - Create final document using dependencies
   - Update knowledge base registry
   - Generate summary report

## Example Workflow:

User: /orchestrate-agents prd

System:
🚀 Orchestrating PRD Creation Workflow
════════════════════════════════════════
📊 Dependency Analysis:
Missing: market-analysis, user-research
Existing: statement-of-purpose
🤖 Spawning Parallel Agents:
├── Agent A: Market Analysis Specialist
│ Context: @ai/knowledge/strategic/statement-of-purpose.md
│ Focus: Competitive landscape, market opportunities
│
└── Agent B: User Research Specialist
Context: @ai/knowledge/strategic/statement-of-purpose.md
Focus: User personas, pain points, journey mapping
⏳ Agents working... (2/2 active)
✅ Agent A completed: market-analysis.md
✅ Agent B completed: user-research.md
🤖 Spawning Synthesis Agent:
└── Agent C: PRD Specialist
Context: All prerequisite documents
Focus: Comprehensive product requirements
✅ PRD Creation Complete!
Next Steps:
[1] Review generated PRD
[2] Create priority-feature-list
[3] Begin implementation planning
