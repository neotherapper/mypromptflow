# Meta-Prompts (Orchestration): Coordinating AI Agents

Meta-prompts focused on orchestration are designed to coordinate the actions of multiple AI agents or define the overarching strategy for complex, multi-step tasks, such as generating a complete document. These prompts act as a conductor, ensuring that different AI components work together seamlessly to achieve a larger goal. They often specify input requirements, generation strategies, and strict output formats to maintain consistency and quality across the entire process.

## Purpose and Functionality

*   **Agent Coordination**: They define how different AI agents should interact and what their respective roles are within a larger workflow.
*   **Workflow Definition**: They outline the sequence of operations, including conditional logic and parallel processing, for complex tasks.
*   **Input/Output Specification**: They clearly define the expected inputs for the orchestration process and the required format of the final output.
*   **Strategy Selection**: They can guide the AI in choosing the most appropriate generation strategy based on the document type or specific requirements.
*   **Quality Control**: By enforcing strict output formats and content requirements, they ensure the consistency and quality of the generated documentation.

## Example: `ai/prompts/meta-prompts/document-generator.md`

This prompt outlines the process for a "Document Generation Agent." It details how the agent should analyze inputs (document type, dependencies, required outputs, context), choose a generation strategy (foundational, research, synthesis), and adhere to a strict output format, including YAML frontmatter and specific sections. This is a prime example of an orchestration meta-prompt because it defines the entire lifecycle of document creation, from input analysis to final output formatting, and implicitly coordinates other potential sub-agents (e.g., a research agent, a synthesis agent).

```markdown
You are a Document Generation Agent specialized in creating business documents for the AI knowledge base.

## Document Creation Process:

### Input Analysis:

1. Document type: {DOCUMENT_TYPE}
2. Available dependencies: {DEPENDENCIES}
3. Required outputs: {REQUIRED_OUTPUTS}
4. Context documents: {CONTEXT_PATHS}

### Generation Strategy:

#### For Foundational Documents (e.g., Statement of Purpose):

- Use first principles thinking
- Gather information through interactive Q&A with user
- Structure content hierarchically
- Include clear sections for each required output

#### For Research Documents (e.g., Market Analysis):

- Synthesize available data
- Use structured analysis frameworks
- Provide quantitative and qualitative insights
- Include actionable recommendations

#### For Synthesis Documents (e.g., PRD):

- Read all dependency documents via @file_path
- Extract relevant information using chain-of-thought
- Cross-reference requirements across documents
- Create comprehensive, coherent output

### Output Format:

All documents must include:

````markdown
---
document_type: { type }
version: 1.0
created_date: { date }
dependencies:
  - { dep1 }
  - { dep2 }
status: draft|review|approved
ai_context:
  primary_purpose: { purpose }
  key_insights:
    - { insight1 }
    - { insight2 }
---

# {Document Title}

## Executive Summary

{Brief overview for AI agents}

## Core Content

{Main document content}

## AI Agent Instructions

{How agents should use this document}

## TypeScript Examples

```typescript
// Relevant code examples
```
````
```

## Key Elements of Orchestration Prompts

*   **Role Definition**: Clearly states the role of the orchestrating agent (e.g., "Document Generation Agent").
*   **Process Flow**: Outlines the step-by-step process the agent should follow.
*   **Conditional Logic**: May include conditions for choosing different strategies (e.g., "For Foundational Documents...").
*   **Sub-Task Delegation**: Implies or explicitly states the need for other agents or sub-processes to handle specific parts of the task (e.g., "Gather information through interactive Q&A with user" might involve a user interaction agent).
*   **Output Constraints**: Defines strict formatting and content requirements for the final output, ensuring consistency across all generated documents.
