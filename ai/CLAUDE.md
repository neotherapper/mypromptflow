# AI Knowledge Base Project - Claude Documentation

## Project Overview

This AI Knowledge Base is a sophisticated system for creating, managing, and orchestrating comprehensive business documentation through AI agent collaboration. It transforms complex documentation workflows into simple interactive commands that work seamlessly with Claude Code.

### Core Purpose

- **Automate Documentation Creation**: AI agents generate structured, high-quality business documents
- **Orchestrate Multi-Agent Workflows**: Coordinate specialized agents for complex document dependencies
- **Interactive Command System**: Simple slash commands (`/ai-help`, `/create-document`) trigger sophisticated workflows
- **Maintain Knowledge Integrity**: Automatic registry updates, cross-references, and dependency tracking

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

## System Architecture

### 1. Dual Interface System

The system serves both human users and AI agents through a unified command interface:

```
User Types: /ai-help
     ↓
Claude Code → .claude/commands/ai-help.md → AI Agent reads instructions
     ↓
AI Agent → Presents options → User selects → Executes command workflow
     ↓
Specialized Agents → Create documents → Update registries → Report results
```

**Key Benefits:**

- ✅ Single source of truth for command definitions
- ✅ Works with both direct user input and programmatic AI execution
- ✅ No complex TypeScript infrastructure needed
- ✅ Maintains Claude Code compatibility

### 2. Command System (`.claude/commands/`)

Interactive commands that work via AI agent orchestration:

- **`/ai-help`** - Interactive guide that presents all available options
- **`/create-document [type]`** - Create single documents with dependency checking
- **`/orchestrate-agents [target]`** - Multi-agent workflows for complex documents
- **`/create-feature [name]`** - Complete feature workspace with 5-phase documentation
- **`/validate-knowledge-base`** - Comprehensive knowledge base health check

### 3. AI Agent Orchestration (`ai/agents/`, `ai/prompts/meta-prompts/`)

Specialized agents for different documentation tasks:

**Document Generation Agents:**

- Market Analysis Specialist
- User Research Specialist
- PRD Specialist
- Technical Architect
- Test Strategist

**Orchestration Agents:**

- Command Executor Agent (`ai/agents/command-executor.md`)
- Feature Orchestrator (`ai/prompts/meta-prompts/feature-orchestrator.md`)
- Dependency Analyzer (`ai/prompts/meta-prompts/dependency-analyzer.md`)

### 4. Knowledge Organization (`ai/knowledge/`)

Structured repository organized by domain:

```
ai/knowledge/
├── strategic/          # Tier 4: Foundational documents
│   ├── statement-of-purpose.md
│   ├── market-analysis.md
│   └── user-research.md
├── product/            # Tier 2-3: Product requirements
│   ├── prd/
│   ├── user-stories/
│   └── epics/
├── technical/          # Tier 1: Implementation docs
│   ├── api/
│   ├── architecture/
│   └── database/
├── user-experience/    # UX research and design
│   ├── research/
│   ├── design/
│   └── journey-maps/
└── business-analysis/  # Business strategy
```

### 5. Dependency Management (`ai/context/`)

Intelligent dependency tracking and workflow orchestration:

- **`dependencies.yaml`** - Document relationships and workflow chains
- **`document-registry.yaml`** - Tracks all documents with metadata
- **`feature-registry.yaml`** - Feature workspace tracking
- **`tier-configuration.yaml`** - Document tier classifications

## Interactive Command Workflows

### `/ai-help` - Main Interface

When user runs `/ai-help`, AI agent presents:

```
🤖 AI Knowledge Base Assistant

Available commands:
┌─────────────────────────────────────────────────────────────┐
│ 📝 Document Management                                      │
├─────────────────────────────────────────────────────────────┤
│ • create-document      - Create single documents           │
│ • orchestrate-agents   - Multi-document workflows          │
│ • validate             - Check knowledge base health       │
├─────────────────────────────────────────────────────────────┤
│ 🚀 Feature Development                                      │
├─────────────────────────────────────────────────────────────┤
│ • create-feature       - Complete feature workspace        │
│ • analyse-dependencies - Document dependency analysis      │
└─────────────────────────────────────────────────────────────┘

What would you like to do?
```

### `/create-document` - Interactive Document Creation

**User Flow:**

1. User: "create-document"
2. AI analyzes missing documents and presents options:

   ```
   📋 Missing Documents Available to Create:

   Strategic Documents (Tier 4):
   • market-analysis     - Competitive landscape and opportunities
   • user-research      - User interviews and behavioral insights

   Which document would you like to create?
   ```

3. User selects → AI executes creation workflow

### `/orchestrate-agents` - Multi-Agent Workflows

**Example: PRD Creation Workflow**

```
User: "orchestrate-agents prd"
↓
AI analyzes dependencies: needs market-analysis, user-research, user-personas
↓
Spawns parallel agents:
├── Market Analysis Specialist (creates market-analysis.md)
└── User Research Specialist (creates user-research.md)
↓
Sequential agent:
└── User Personas Specialist (creates user-personas.md using both inputs)
↓
Final synthesis:
└── PRD Specialist (creates prd.md using all dependencies)
```

### `/create-feature` - Complete Feature Development

**5-Phase Agent Sequence:**

1. **Requirements Analyst** → user-stories.md, acceptance-criteria.md
2. **Design Specialist** → ui-mockups.md, interaction-flow.md
3. **Technical Architect** → api-contracts.md, data-models.md
4. **Test Strategist** → test-strategy.md, test-scenarios.md
5. **Analytics Specialist** → success-metrics.md, tracking-plan.md

## Document Quality Standards

### Required Structure

Every document must include:

````markdown
---
document_type: research|synthesis|technical|feature
version: 1.0
created_date: 2024-01-20
dependencies: [list-of-required-docs]
status: draft|review|approved
ai_context:
  primary_purpose: "Brief description"
  key_insights:
    - "Key insight 1"
    - "Key insight 2"
---

# Document Title

## Executive Summary

Brief overview for AI agents and humans

## [Content Sections]

Structured content with clear hierarchy

## AI Agent Instructions

How other agents should use this document

## Cross-References

- @ai/knowledge/related/document.md

## TypeScript Examples (if applicable)

```typescript
// Relevant code examples
```
````

````

### AI Optimization Features

Documents are optimized for AI processing:
- **Structured Data**: Tables, lists, YAML frontmatter
- **Clear Cross-References**: @ai/knowledge/ path format
- **Explicit Instructions**: AI agent guidance in every document
- **Hierarchical Organization**: Clear H1/H2/H3 structure
- **Code Examples**: TypeScript interfaces and examples

## Development Workflows

### Adding New Commands

1. **Create Command Definition**: Add new `.claude/commands/new-command.md`
2. **Define Workflow**: Specify step-by-step execution instructions
3. **Add to AI Help**: Update `/ai-help` command to include new option
4. **Create Tests**: Add test cases in `ai/tests/`
5. **Document Integration**: Update this CLAUDE.md

### Creating New Document Types

1. **Add to Dependencies**: Define in `ai/context/dependencies.yaml`
2. **Create Template**: Add template in `ai/prompts/document-templates/`
3. **Update Registry Schema**: Modify `document-registry.yaml` structure
4. **Add Validation**: Include in validation tests
5. **Create Specialist Agent**: Add agent prompt for document type

### Agent Development

1. **Define Agent Role**: Create agent prompt in `ai/prompts/meta-prompts/`
2. **Specify Parameters**: Define required context and outputs
3. **Integration Points**: How agent fits in orchestration workflows
4. **Testing**: Add agent parameter tests
5. **Documentation**: Update agent coordination protocols

## Configuration Management

### Dependencies Configuration (`ai/context/dependencies.yaml`)

Defines document relationships and workflow chains:

```yaml
document_dependencies:
  prd:
    type: synthesis
    tier: 2
    dependencies:
      - statement-of-purpose
      - market-analysis
      - user-research
      - user-personas
    outputs:
      - functional_requirements
      - success_metrics

workflow_chains:
  create_prd:
    order:
      - parallel:
          - statement-of-purpose
          - market-analysis
          - user-research
      - sequential:
          - user-personas
          - prd
````

### Registry Management

**Document Registry** tracks all knowledge base documents:

- Document metadata and status
- Dependency satisfaction tracking
- Cross-reference mapping
- AI value scoring (60-95 range)

**Feature Registry** tracks feature workspaces:

- Feature documentation completion
- Implementation status
- Related knowledge base documents

## Testing Framework

### Test Philosophy: Real Execution, Not Simulation

The testing framework validates actual system behavior:

- ✅ **Real File Creation**: Tests verify actual documents are created
- ✅ **Real Agent Parameters**: Validates agents receive correct context
- ✅ **Real Registry Updates**: Checks YAML files are actually updated
- ❌ **No Mocking**: All tests execute real workflows

### Test Categories

1. **Command Execution Tests** - Validate interactive commands work
2. **Agent Parameter Tests** - Ensure agents get correct context/instructions
3. **File Creation Tests** - Verify document and workspace creation
4. **Registry Update Tests** - Validate automatic registry maintenance

### Running Tests

```bash
# Full test suite
./ai/tests/run-tests.sh

# Individual test categories
python3 -c "import yaml; print(yaml.safe_load(open('ai/tests/command-execution-tests.yaml')))"
```

## Integration Points

### Claude Code Integration

Commands work seamlessly with Claude Code:

- Slash command syntax: `/ai-help`, `/create-document market-analysis`
- Progress reporting in terminal
- Error messages formatted for CLI
- Agent spawning via Task tool

### File System Integration

- Automatic directory creation
- Consistent file naming conventions
- Cross-platform path handling
- Permission management

### External Tool Integration

- Bash script execution (`scripts/create-feature.sh`)
- Git integration for version control
- YAML parsing and validation
- Markdown processing

## Troubleshooting

### Common Issues

**Command Not Working:**

1. Check `.claude/commands/[command].md` exists
2. Verify AI agent can read command definition
3. Check dependencies.yaml syntax
4. Validate file permissions

**Agent Spawn Failures:**

1. Verify context documents exist and are readable
2. Check template paths are correct
3. Validate agent instruction format
4. Ensure required parameters provided

**Registry Update Errors:**

1. Check YAML syntax in registry files
2. Verify file write permissions
3. Validate registry structure
4. Check for circular dependencies

**File Creation Issues:**

1. Verify directory structure exists
2. Check template accessibility
3. Validate YAML frontmatter syntax
4. Ensure proper cross-reference format

### Debug Commands

```bash
# Validate YAML files
python3 -c "import yaml; yaml.safe_load(open('ai/context/dependencies.yaml'))"

# Check command definitions
ls -la .claude/commands/

# Validate knowledge base structure
./scripts/validate-knowledge-base.sh

# Run specific tests
./ai/tests/run-tests.sh
```

## Best Practices

### For AI Agents

1. **Always read command definitions** from `.claude/commands/` before execution
2. **Validate context documents** before spawning dependent agents
3. **Update registries atomically** - all-or-nothing operations
4. **Provide clear progress updates** during multi-step workflows
5. **Handle errors gracefully** with recovery options

### For Users

1. **Start with `/ai-help`** to see all available options
2. **Use dependency analysis** before creating complex documents
3. **Validate knowledge base** regularly with `/validate`
4. **Follow interactive prompts** for best results
5. **Check generated files** and provide feedback for refinement

### For Developers

1. **Follow test specifications exactly** - tests define the contract
2. **Maintain YAML syntax** in all configuration files
3. **Use @ai/knowledge/ paths** for cross-references
4. **Include proper frontmatter** in all documents
5. **Document new features** in this CLAUDE.md

## Future Enhancements

### Planned Features

1. **Command Chaining** - Link multiple commands in workflows
2. **Conditional Execution** - Commands that adapt based on context
3. **External Integrations** - GitHub, Slack, project management tools
4. **Advanced Analytics** - Usage tracking and optimization recommendations
5. **Custom Templates** - User-specific document templates

### Extension Points

- **Custom Document Types** - Add domain-specific document categories
- **Specialized Agents** - Create industry-specific agent specialists
- **Integration APIs** - Connect to external systems and data sources
- **Workflow Automation** - Trigger workflows based on events
- **Quality Metrics** - Advanced document quality scoring

This AI Knowledge Base system provides a powerful foundation for automated documentation that scales with your organization's needs while maintaining quality and consistency through AI agent orchestration.
