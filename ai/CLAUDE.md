# AI Knowledge Base Component

## Component Purpose

Orchestrated document generation through AI agent collaboration with interactive Claude Code commands.

## Usage Instructions

**Command Access**: Use `/ai-help` for interactive command discovery and workflow selection

**Core Commands**:
- `/create-document [type]` - Create single document interactively
- `/create-feature [name]` - Create feature workspace with all documentation
- `/orchestrate-agents [doc]` - Multi-agent creation workflow
- `/validate` - Validate knowledge base health

**Dependencies**: Check `ai/context/dependencies.yaml` when working with document relationships
**Templates**: Access document templates at `ai/prompts/document-templates/`
**Registries**: System automatically updates `ai/context/document-registry.yaml`

## Integration Patterns

**Command System**: Dual interface serving users and AI agents through `.claude/commands/`
**Agent Orchestration**: Specialized agents via Task tool spawning for document types
**Registry Management**: Automatic updates to `ai/context/document-registry.yaml` and `ai/context/feature-registry.yaml`
**Dependency Tracking**: Cross-reference resolution using `ai/context/dependencies.yaml`

**Document Standards**:
- YAML frontmatter with metadata
- AI Agent Instructions section  
- Cross-references using file paths
- TypeScript examples where applicable

**Workflow Integration**: Reference `ai/docs/system-architecture.md` for detailed architecture and agent coordination patterns

## Quick Start

1. **For Users**: Type `/ai-help` to see available commands and select workflow
2. **For AI Agents**: Access command definitions at `.claude/commands/` for execution workflows
3. **For Development**: Check `ai/context/dependencies.yaml` for document relationships before creating new content