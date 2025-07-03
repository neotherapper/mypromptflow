# System Overview: AI Knowledge Base Project

This document provides a comprehensive overview of the AI Knowledge Base project, detailing its purpose, architecture, key components, and workflows.

## 1. Project Purpose

The primary goal of this project is to automate the creation, management, and validation of comprehensive business documentation. It leverages Artificial Intelligence (AI) agents to generate structured and high-quality content, ensuring consistency, accuracy, and easy accessibility across various document types. The system is designed to streamline the documentation process, particularly for software development projects, by integrating with development workflows and tools.

## 2. Architecture and Key Components

The project's architecture is modular, with distinct components working in orchestration to achieve its objectives:

### 2.1. AI Core (`ai/` directory)

This is the heart of the AI Knowledge Base, housing all AI-related configurations, prompts, and generated content.

*   **`ai/context/`**: Contains foundational configuration files that define the structure and relationships within the knowledge base:
    *   `dependencies.yaml`: Defines prerequisites and relationships between documents.
    *   `document-registry.yaml`: A registry of all managed documents and their metadata.
    *   `feature-registry.yaml`: Tracks features and their associated documentation.
    *   `tier-configuration.yaml`: Configures document tiers, potentially for different levels of detail or audience.

*   **`ai/prompts/`**: Stores the instructions and templates that guide the AI agents during content generation. This directory is critical for controlling the AI's output and ensuring adherence to documentation standards.
    *   `document-templates/`: Templates for various document types.
    *   `meta/`: Meta-prompts for advanced AI behaviors (e.g., adaptive chain of thought, complex research).
    *   `meta-prompts/`: Prompts specifically designed for orchestrating other AI agents (e.g., `dependency-analyzer.md`, `document-generator.md`).
    *   Individual prompt files (e.g., `1_discover_tools.md`): Specific prompts for distinct steps in the documentation generation process.

*   **`ai/knowledge/`**: The repository for all generated and managed documentation, organized by subject matter (e.g., `product/`, `strategic/`).

*   **`ai/features/`**: Contains documentation specific to individual features, often generated through a dedicated feature development workflow. Includes a `_template` for new feature documentation.

*   **`ai/scratchpads/`**: A temporary area for AI agents to store intermediate outputs or experimental content.

*   **`ai/tests/`**: Contains tests for validating the AI context and document structure, ensuring the integrity of the knowledge base.

### 2.2. CLI and Command Definitions (`.claude/` directory)

This directory defines the interactive command-line interface (CLI) for interacting with the AI Knowledge Base system.

*   **`.claude/commands/`**: Markdown files that specify the commands available to the Claude CLI (e.g., `/create-document`, `/orchestrate-agents`). These commands trigger the underlying automation scripts and AI workflows.

### 2.3. Automation Scripts (`scripts/` directory)

These shell scripts are the operational backbone of the system, orchestrating the AI agents and managing the documentation lifecycle.

*   `create-feature.sh`: Automates the creation of a new feature workspace, including all necessary documentation stubs.
*   `run_chain.sh`: Executes a sequence of AI agent tasks or documentation generation steps.
*   `setup-mcp.sh`: Script for setting up the Micro-service Communication Protocol.
*   `start_mcp.sh`: Initiates the MCP server.
*   `validate-knowledge-base.sh`: Performs validation checks on the entire knowledge base to ensure consistency and quality.
*   `init/`: Contains initialization scripts for setting up AI and Claude-related files and directories.

### 2.4. Micro-service Communication Protocol (MCP) Servers (`mcp-servers/` directory)

This component facilitates communication with external services and systems.

*   **`mcp-servers/github/`**: A dedicated server for integrating with GitHub. This integration could enable functionalities such as:
    *   Triggering documentation updates based on GitHub events (e.g., pull requests, issue creation).
    *   Automated generation of documentation for new code features or bug fixes.
    *   Synchronization of documentation with code repositories.

## 3. Key Workflows

### 3.1. Feature Development Workflow

This workflow is central to the project, ensuring that new features are comprehensively documented from inception.

1.  **Feature Creation**: Initiated via the `/create-feature [name]` command, which executes `scripts/create-feature.sh`.
2.  **Automated Documentation Generation**: AI agents, guided by prompts in `ai/prompts`, generate various documentation artifacts (e.g., feature specifications, API contracts, user stories) within `ai/features/[feature-name]/`.
3.  **Review and Refinement**: Generated content is reviewed and refined by human users.
4.  **Implementation Guidance**: The generated documentation serves as a guide for developers during the implementation phase.

### 3.2. Document Creation and Management

Individual documents can be created and managed interactively:

1.  **Dependency Analysis**: The `/analyze [doc]` command (likely using `ai/context/dependencies.yaml`) checks for prerequisites.
2.  **Interactive Creation**: The `/create-document [type]` command allows users to create specific document types, with AI assistance.
3.  **Agent Orchestration**: For complex documentation tasks, `/orchestrate-agents [doc]` can be used to coordinate multiple AI agents.

### 3.3. Knowledge Base Validation

Regular validation ensures the quality and integrity of the knowledge base.

1.  **Validation Trigger**: The `/validate` command or `scripts/validate-knowledge-base.sh` initiates the validation process.
2.  **Checks Performed**: Validation includes checking document structure, cross-references, and adherence to quality standards, potentially utilizing tests in `ai/tests/`.

## 4. Document Quality Standards

All documents within the knowledge base adhere to strict quality standards to ensure clarity, consistency, and utility:

*   **Structured Content**: Clear hierarchical structure (H1, H2, H3).
*   **AI Agent Instructions**: Explicit instructions for AI agents embedded within documents.
*   **Cross-references**: Extensive use of `@ai/knowledge/` paths to link related documents.
*   **Versioning and Status Tracking**: Metadata for versioning and status.
*   **Actionable Insights**: Content designed to provide practical guidance for application development.
*   **TypeScript Code Examples**: Inclusion of relevant TypeScript code examples where applicable.

## 5. AI Research Framework

In addition to the core components, the project includes a sophisticated **AI Research Framework** designed to automate and elevate the research process itself. This framework uses a Meta-Prompt Orchestrator and a Cognitive Knowledge Fabric to produce expert-level, validated, and interconnected research.

For a detailed explanation, see the [AI Research Framework Overview](ai_research_framework_overview.md).

## 6. Conclusion

The AI Knowledge Base project is a sophisticated system designed to revolutionize documentation practices. By combining AI-driven content generation, structured data management, and automated workflows, it aims to produce a comprehensive, accurate, and easily maintainable repository of business and technical knowledge.