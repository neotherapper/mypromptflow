# AI Knowledge Base Project Instructions

## Project Explanation

This project is an AI Knowledge Base system designed to build comprehensive business documentation using an orchestrated agent system.

## Key Concepts

1. **Document Dependencies**: Documents have prerequisites defined in dependencies.yaml
2. **Agent Orchestration**: Specialized agents handle different document types
3. **Interactive Workflows**: Claude suggests and creates missing documents
4. **Context Propagation**: Documents reference each other for coherent knowledge
5. **Structured Documents:** All documents require YAML frontmatter, AI agent instructions, cross-references, and TypeScript examples.
6. **Feature Development:** A dedicated workflow exists for creating features, where agents generate all associated documentation.

## Workflow Commands

- `/analyze [doc]` - Check dependencies for a document
- `/orchestrate-agents [doc]` - Start multi-agent creation workflow
- `/create-document [type]` - Create single document interactively
- `/create-feature [name]` - Create feature workspace with all documentation
- `/generate-tier-documents [tier]` - Generate all documents in a tier
- `/validate` - Validate entire knowledge base

## Document Structure

All documents must include:

- YAML frontmatter with metadata
- AI Agent Instructions section
- Cross-references using @ai/knowledge/ paths
- TypeScript examples where applicable

## When Working on This Project

1. Always check dependencies before creating documents
2. Use @file_path references to existing documents
3. Maintain YAML frontmatter in all documents
4. Update registries after document creation
5. Suggest next logical documents to create

## Document Quality Standards

- Clear hierarchical structure (H1, H2, H3)
- Explicit AI agent instructions
- Cross-references to related documents
- Versioning and status tracking
- Actionable insights for app development
- TypeScript code examples

## Feature Development Workflow

1. Create feature with `/create-feature [name]`
2. Agents will generate complete documentation
3. Review and refine generated content
4. Use for implementation guidance

## AI Research System

**Available to all AI agents:** This project includes a research framework at `research/` that any AI agent can use autonomously.

**MANDATORY:** For all research tasks, you *must* consult and strictly adhere to the guidelines outlined in `research/orchestrator/integration/gemini-orchestrator-integration.yaml`. This file contains the comprehensive instructions for using the research orchestrator and ensuring compliance with research protocols.

## Development Workflow

- **NEVER** commit directly to the `master` branch.
- Always create a new feature branch for your work.
