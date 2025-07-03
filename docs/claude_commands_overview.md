# Claude Commands Overview: Interactive CLI for Knowledge Base Management

This document outlines the interactive command-line interface (CLI) commands available through Claude, which serve as the primary user-facing tools for managing and interacting with the AI Knowledge Base. These commands abstract complex workflows, allowing users to trigger AI agent orchestrations, create documents, and validate the knowledge base with simple inputs.

## 1. Role of Claude Commands

The Claude commands, defined in the `.claude/commands/` directory, act as a bridge between the user and the underlying AI-powered documentation system. Each Markdown file in this directory represents a specific command, detailing its purpose, arguments, and the workflow it initiates. They are designed to:

*   **Simplify Complex Workflows**: Abstract multi-step processes into single, easy-to-use commands.
*   **Enable Interactive Management**: Allow users to create, analyze, and validate documents on demand.
*   **Orchestrate AI Agents**: Trigger the execution of specific AI agents and their associated prompts.
*   **Provide User Feedback**: Outline the expected output and interactive options for the user.

## 2. Key Claude Commands

Here's an overview of some of the critical commands and their functionalities:

### 2.1. `create-feature [name]`

This command initiates the comprehensive workflow for creating a new feature workspace, including all associated documentation. It orchestrates multiple AI agents to generate various document types.

**Command Definition: `create-feature.md`**

```markdown
Create a comprehensive feature workspace: $ARGUMENTS

## Feature Creation Workflow:

1. **Initialize Feature Structure**
   Creating feature: $ARGUMENTS
   Location: ai/features/$ARGUMENTS/

2. **Spawn Feature Orchestrator**

   - Load feature templates
   - Identify relevant knowledge base documents
   - Plan agent sequence

3. **Phase 1: Requirements Analysis**
   🔍 Requirements Analyst Agent
   Creating:
   → user-stories.md
   → acceptance-criteria.md
   → dependencies.md

4. **Phase 2: Design Development**
   🎨 Design Specialist Agent
   Creating:
   → ui-mockups.md
   → interaction-flow.md
   → design-decisions.md

5. **Phase 3: Technical Architecture**
   🏗️ Technical Architect Agent
   Creating:
   → api-contracts.md
   → data-models.md
   → implementation-plan.md
   → architecture-decisions.md

6. **Phase 4: Test Strategy**
   🧪 Test Strategist Agent
   Creating:
   → test-strategy.md
   → test-scenarios.md
   → test-data.md

7. **Phase 5: Analytics & Monitoring**
   📊 Analytics Specialist Agent
   Creating:
   → success-metrics.md
   → tracking-plan.md

8. **Final Integration**
   ✅ Feature Workspace Complete

   AI Instructions Generated:
   → meta/ai-instructions.md

   Ready for Implementation:
   [1] Generate implementation tasks
   [2] Create GitHub issues
   [3] Start development
```

### 2.2. `analyse-dependencies [doc]`

This command analyzes the dependency graph for a specified document, identifying existing, missing, or outdated dependencies. It also suggests a creation order and estimates effort for missing documents.

**Command Definition: `analyse-dependencies.md`**

```markdown
Analyze the dependency graph for document: $ARGUMENTS

1. Read @ai/context/dependencies.yaml
2. Check which dependencies exist in @ai/knowledge/
3. Create a visual representation:
   - ✅ Existing documents
   - ❌ Missing documents
   - 🔄 Documents with outdated dependencies
4. Suggest creation order based on dependency graph
5. Estimate effort for completing missing documents

Output format:

Dependency Analysis for: {document}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Required Dependencies:
├── ✅ statement-of-purpose.md (exists)
├── ❌ market-analysis.md (missing)
└── ❌ user-research.md (missing)

Suggested Creation Order:

1. market-analysis.md (parallel with user-research)
2. user-research.md (parallel with market-analysis)
3. {target-document} (after all dependencies)

Interactive Options:
[1] Create all missing documents
[2] Create specific document
[3] View existing document
[4] Update dependency configuration
```

### 2.3. `validate-knowledge-base`

This command runs comprehensive validation tests across the entire knowledge base, checking for structural integrity, dependency consistency, content quality, cross-reference validity, and AI optimization.

**Command Definition: `validate-knowledge-base.md`**

```markdown
Run comprehensive validation tests on knowledge base

## Validation Process:

1. **Structure Validation**

   - Check all required directories exist
   - Verify document paths match configuration
   - Ensure no orphaned documents

2. **Dependency Validation**

   - Build complete dependency graph
   - Check for circular dependencies
   - Verify all references resolve

3. **Content Validation**

   - Verify frontmatter in all documents
   - Check required sections present
   - Validate AI instruction sections

4. **Cross-Reference Validation**

   - Ensure all @file_path references valid
   - Check bidirectional links consistency
   - Verify feature ↔ knowledge base links

5. **AI Optimization Check**
   - Score documents for AI readability
   - Check structured data usage
   - Verify TypeScript examples present

## Output format:

🔍 Knowledge Base Validation Report
═══════════════════════════════════
📁 Structure Check: [status]
🔗 Dependency Check: [status]
📝 Content Check: [status]
🤖 AI Optimization: [score]
📊 Summary:
Health Score: [score]/100
Issues Found: [count]
Recommendations: [list]
```

### 2.4. Other Commands

*   **`create-document [type]`**: Creates a single document interactively, likely guided by document templates.
*   **`fix-github-issue [issue_id]`**: Suggests integration with GitHub for automated issue resolution or documentation generation related to issues.
*   **`generate-tier-documents [tier]`**: Generates all documents belonging to a specific tier, as defined in `tier-configuration.yaml`.
*   **`gh-issue [issue_details]`**: Likely for creating GitHub issues directly from the CLI.
*   **`orchestrate-agents [doc]`**: Initiates a multi-agent creation workflow for a specific document, allowing for complex document generation tasks.
*   **`tasks.md`**: This command likely relates to task management or the generation of task-related documentation.

## 3. Conclusion

The Claude commands provide a powerful and intuitive interface for managing the AI Knowledge Base. By encapsulating complex AI workflows and documentation processes into simple commands, they empower users to efficiently create, analyze, and validate the comprehensive business documentation generated by the system. This CLI is a critical component in making the AI Knowledge Base accessible and actionable for users.