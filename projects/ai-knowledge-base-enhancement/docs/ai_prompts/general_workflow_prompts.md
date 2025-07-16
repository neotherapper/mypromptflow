# General Workflow Prompts

General workflow prompts are foundational instructions that initiate or guide high-level tasks within the AI Knowledge Base system. They often serve as the starting point for a sequence of operations, helping the AI understand the overall objective and context of a task. These prompts are designed to be broad enough to encompass various sub-tasks, yet specific enough to set the AI on the correct path.

## Purpose and Functionality

*   **Initiation**: They kickstart complex processes, such as analyzing dependencies or extracting key information from a codebase.
*   **Guidance**: They provide the initial direction for AI agents, ensuring that subsequent steps are aligned with the overarching goal.
*   **Context Setting**: They establish the problem space or domain, allowing the AI to focus its efforts and leverage relevant knowledge.

## Example: `ai/prompts/meta-prompts/dependency-analyzer.md`

This prompt defines the role and process for a "Dependency Analysis Agent." It outlines how the agent maps and validates document dependencies, including building a directed graph, detecting circular dependencies, identifying missing ones, and suggesting optimization for parallel processing. This is a prime example of a general workflow prompt because it defines a complete, high-level task that involves multiple sub-steps and outputs a structured report.

```markdown
You are a Dependency Analysis Agent responsible for mapping and validating document dependencies.

## Analysis Process:

1. **Dependency Mapping**

   - Read @ai/context/dependencies.yaml
   - Build directed graph of dependencies
   - Identify dependency chains

2. **Validation Checks**

   - Circular dependency detection
   - Missing dependency identification
   - Version compatibility verification

3. **Optimization**

   - Suggest parallel processing opportunities
   - Identify redundant dependencies
   - Recommend consolidation points

4. **Reporting**
   Create visual dependency graph showing:
   - Document relationships
   - Creation order
   - Parallel vs sequential requirements
   - Critical path analysis

## Output Format:

Dependency Graph for: {document}
════════════════════════════════
Direct Dependencies:
├── {dep1} [status]
├── {dep2} [status]
└── {dep3} [status]
Transitive Dependencies:
└── {dep1}
├── {subdep1}
└── {subdep2}
Suggested Creation Order:

Parallel Group A: [{docs}]
Parallel Group B: [{docs}]
Sequential: {doc1} → {doc2}
```

## Best Practices for General Workflow Prompts

*   **Clear Objective**: Clearly state the main goal of the workflow.
*   **Input/Output Definition**: Define what inputs the AI should expect and what kind of output is required.
*   **High-Level Steps**: Break down the workflow into logical, high-level steps without getting into excessive detail.
*   **Agent Role**: If applicable, define the specific role the AI agent should adopt for this workflow.
*   **Error Handling/Edge Cases**: Briefly mention how the AI should handle common issues or unexpected scenarios.
