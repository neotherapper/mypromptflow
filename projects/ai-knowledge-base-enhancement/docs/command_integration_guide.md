# Command Integration Guide: Dual Interface System

## Overview

The AI Knowledge Base implements a dual interface system where commands can be executed both directly by users through Claude Code and programmatically by AI agents. This creates a seamless bridge between human interaction and automated AI workflows.

## Architecture

### Dual Interface Design

```
User Input: /project:orchestrate-agents prd
     ↓
Claude Code → .claude/commands/orchestrate-agents.md → Execution
     ↓
Command Executor Agent → Reads command definition → Spawns agents
     ↓
Specialized Agents → Create documents → Update registries
```

**Key Components:**

1. **Command Definitions** (`.claude/commands/*.md`): Human-readable command specifications with executable instructions
2. **Command Executor Agent** (`ai/agents/command-executor.md`): AI agent that reads and executes command definitions
3. **Specialized Agents** (`ai/prompts/meta-prompts/`): Domain-specific agents for document creation
4. **Registry System** (`ai/context/*.yaml`): Automatic tracking and cross-referencing

## Command Structure

### Enhanced Command Format

Each command in `.claude/commands/` includes:

```markdown
# Command Title: $ARGUMENTS

## Executable Instructions:

### Step 1: [Description]
```bash
# Bash commands where needed
```

1. Detailed step-by-step instructions
2. File operations and references
3. Agent spawning instructions

### Step 2: [Next Step]
...

## Example Execution:
**Input:** `/project:command-name argument`
**Output:** Expected results and success criteria
```

### Command Categories

1. **Document Management**
   - `/project:create-document [type]` - Create single documents
   - `/project:orchestrate-agents [target]` - Multi-document workflows
   - `/project:validate` - Knowledge base validation

2. **Feature Development**
   - `/project:create-feature [name]` - Complete feature workspace
   - `/project:analyse-dependencies [doc]` - Dependency analysis

3. **Utilities**
   - `/project:generate-tier-documents [tier]` - Bulk document generation

## Execution Flows

### Direct User Execution

1. **User Input**: Types `/project:orchestrate-agents prd` in Claude Code
2. **Claude Code**: Reads `.claude/commands/orchestrate-agents.md`
3. **Execution**: Follows executable instructions step-by-step
4. **Agent Spawning**: Uses Task tool to spawn specialized agents
5. **Coordination**: Manages multi-agent workflows
6. **Results**: Updates registries and reports success

### Programmatic Agent Execution

1. **Agent Call**: AI agent needs to execute a command
2. **Command Reading**: Agent reads command definition from `.claude/commands/`
3. **Instruction Parsing**: Extracts executable instructions
4. **Execution**: Follows instructions programmatically
5. **Integration**: Returns results to calling agent

## Agent Coordination

### Multi-Agent Workflows

**Parallel Execution:**
```
Command Executor Agent
    ↓
┌─────────────────┬─────────────────┐
│   Agent A       │    Agent B      │
│ Market Analysis │ User Research   │
└─────────────────┴─────────────────┘
    ↓                      ↓
    └──────────┬───────────┘
               ↓
        Agent C (Synthesis)
           PRD Creation
```

**Sequential Execution:**
```
Command Executor Agent
    ↓
Agent A (Requirements) → Agent B (Design) → Agent C (Technical) → Agent D (Tests)
```

### Agent Communication Protocol

**Standard Agent Instruction Template:**
```markdown
You are a [Specialist Type] Agent executing [command-name].

Context:
- Command: /project:[command-name] [arguments]
- Previous Outputs: [if applicable]
- Required Documents: [list]

Task:
[Specific instructions for this agent]

Expected Output:
[Deliverables and format requirements]

Integration:
- Update: @ai/context/[registry].yaml
- Cross-reference: [related documents]
- Next Steps: [follow-up actions]
```

## Registry Integration

### Automatic Updates

**Document Registry (`ai/context/document-registry.yaml`):**
```yaml
documents:
  - id: "market-analysis"
    type: "research"
    path: "ai/knowledge/strategic/market-analysis.md"
    version: "1.0"
    status: "draft"
    created_date: "2024-01-20"
    dependencies_satisfied: true
    tier: 4
    ai_value: 85
    created_by_command: "/project:create-document market-analysis"
```

**Feature Registry (`ai/context/feature-registry.yaml`):**
```yaml
features:
  - id: "user-authentication"
    name: "User Authentication"
    path: "ai/features/user-authentication/"
    status: "documented"
    created_date: "2024-01-20"
    documentation_complete: true
    created_by_command: "/project:create-feature user-authentication"
```

### Cross-Reference Management

Commands automatically create bidirectional references:
- Document A references Document B → Document B shows "Referenced by: Document A"
- Feature references Knowledge Base documents → Knowledge Base shows "Used in Features: [list]"

## Command Examples

### Example 1: PRD Creation Workflow

**User Command:**
```
/project:orchestrate-agents prd
```

**Execution Flow:**
1. Read dependencies for 'prd' from `dependencies.yaml`
2. Find missing: market-analysis, user-research, user-personas
3. Spawn parallel agents for market-analysis and user-research
4. After completion, spawn user-personas agent (depends on both)
5. Finally spawn PRD agent with all dependencies
6. Update document registry for all created documents
7. Report completion and next steps

### Example 2: Feature Creation

**User Command:**
```
/project:create-feature payment-system
```

**Execution Flow:**
1. Run `./scripts/create-feature.sh payment-system`
2. Spawn Feature Orchestrator Agent
3. Execute 5-phase agent sequence:
   - Requirements Analyst → user stories, acceptance criteria
   - Design Specialist → UI mockups, interaction flows
   - Technical Architect → API contracts, data models
   - Test Strategist → test strategy, scenarios
   - Analytics Specialist → metrics, tracking
4. Update feature registry
5. Generate AI implementation instructions

### Example 3: Knowledge Base Validation

**User Command:**
```
/project:validate
```

**Execution Flow:**
1. Structure validation (directories, file paths)
2. Dependency validation (graph analysis, circular deps)
3. Content validation (frontmatter, required sections)
4. Cross-reference validation (broken links)
5. AI optimization scoring
6. Generate comprehensive report
7. Suggest action items and commands to fix issues

## Integration Benefits

### For Users
- **Simplified Interface**: Single command triggers complex workflows
- **Consistent Experience**: Same commands work across different contexts
- **Progress Visibility**: Real-time updates during multi-step operations
- **Automatic Documentation**: All actions tracked and documented

### For AI Agents
- **Programmatic Access**: Can execute any command programmatically
- **Standardized Interface**: Consistent command structure and execution
- **Context Awareness**: Access to full knowledge base context
- **Error Handling**: Built-in retry and recovery mechanisms

### For System
- **Single Source of Truth**: Command definitions serve both interfaces
- **Maintainability**: Changes to commands automatically affect both interfaces
- **Extensibility**: Easy to add new commands and capabilities
- **Traceability**: Full audit trail of all command executions

## Testing and Validation

### Command Testing

**Direct Testing:**
```bash
# Test each command directly in Claude Code
/project:validate
/project:create-document market-analysis
/project:orchestrate-agents prd
/project:create-feature test-feature
```

**Programmatic Testing:**
```markdown
Task: Test command executor agent
Prompt: "Execute the command: /project:validate"
Expected: Agent reads validate-knowledge-base.md and executes all validation steps
```

### Validation Criteria

**Command Execution Success:**
- [ ] All executable instructions completed
- [ ] Expected files created in correct locations
- [ ] Registry updates applied successfully
- [ ] Cross-references created properly
- [ ] Progress reporting works correctly

**Agent Coordination Success:**
- [ ] Agents spawn in correct order
- [ ] Context passed between agents correctly
- [ ] Error handling works for failed agents
- [ ] Final integration successful

## Troubleshooting

### Common Issues

1. **Command Not Found**: Check `.claude/commands/[command].md` exists
2. **Agent Spawn Failure**: Verify Task tool availability and agent instructions
3. **Registry Update Failure**: Check YAML syntax in context files
4. **Missing Dependencies**: Use dependency analysis to identify requirements

### Debug Commands

```bash
# Check command definitions
ls -la .claude/commands/

# Validate YAML files
python3 -c "import yaml; yaml.safe_load(open('ai/context/dependencies.yaml'))"

# Check file structure
find ai/ -name "*.md" | head -10
```

## Future Enhancements

### Planned Features

1. **Command Chaining**: Link multiple commands in workflows
2. **Conditional Execution**: Commands that adapt based on context
3. **Parallel Command Execution**: Run multiple commands simultaneously
4. **Command Templates**: User-customizable command templates
5. **Integration APIs**: External system integration via commands

### Extension Points

- **Custom Commands**: Add domain-specific commands for different industries
- **Plugin System**: Extend command functionality with plugins
- **External Integrations**: Connect commands to external tools and services
- **Advanced Analytics**: Track command usage and optimization opportunities

This dual interface system provides a powerful foundation for both human users and AI agents to interact with the knowledge base efficiently and consistently.