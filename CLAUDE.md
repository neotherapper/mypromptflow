# AI Knowledge Base System Instructions

## Core Requirements

**ALL AI Agents MUST**:

- Follow task completion protocol when completing tasks: `ai/workflows/task-management/CLAUDE.md`
- Apply development protocols when doing development work: `development/CLAUDE.md`
- Validate using meta framework when validating instructions: `meta/validation/validators/ai-instruction/`

## Essential Constraints

**Never**:

- Commit to master branch (use feature branches)
- Create files without registry similarity analysis for research

**Always**:

- Use MCP JIRA tools (mcp__MCP_DOCKER__jira\_\*)
- Execute parallel tool operations for efficiency
- Mark TodoWrite complete with timestamps
- Validate @file_path cross-references

## Project Architecture

**Project Type**: AI Knowledge Base Development  
**Current Status**: Research Framework Operational  
**Priority Level**: Critical Infrastructure (Tier 1)  
**Success Threshold**: High research quality, fast response time, zero external dependencies

Self-sufficient AI Knowledge Base system using 4-level agent hierarchy (Queen→Architect→Specialist→Worker) with research capabilities and progressive context loading.

### Three-Layer System Architecture

**Layer 1: AI Orchestration** (`ai/`)
- Multi-agent coordination with feature orchestrators
- 67+ document types with template-based generation
- Hub-spoke database architecture with 6 specialized databases
- Interactive Claude Code integration with slash commands

**Layer 2: Knowledge Vault** (`knowledge-vault/`)
- Structured YAML databases for different domains
- Change detection system with automatic updates
- Cross-domain knowledge mapping and relationships
- Structured metadata with hierarchical organization

**Layer 3: Research & Projects** (`research/`, `projects/`)
- Advanced research orchestrator with 15+ methodologies
- Project-specific workspaces with comprehensive documentation
- Research findings integration with knowledge base updates
- Meta-framework patterns for complex coordination

## AI Research System

**Auto-Integration**: Research intentions trigger the research orchestrator automatically. Use `research/orchestrator/integration/claude-orchestrator-integration.yaml` when conducting research tasks.

**Research Framework Access**: Use `research/CLAUDE.md` when conducting comprehensive research, including:

- MANDATORY registry similarity analysis before starting any research (≥95% compliance required)
- 8-step orchestrator workflow with constitutional AI validation (≥95% accuracy threshold)
- Enhanced file structure requirements (research/findings/[topic]/ with .meta/ folder)
- Quality validation protocols and task completion procedures

**Automatic Research Framework Activation**: Execute universal intention detection using `meta/shared/intention-detection-framework.md` when analyzing user requests:

- Apply `research_intention_triggers` and `complexity_indicators` for activation decisions
- High constitutional compliance (≥95%), execution time ≤300 seconds
- **Fallback Protocol** (if research/ unavailable): Basic 6-step sequence → Intent Detection → Context Extraction → Complexity Assessment → Method Selection → Execution → Summary Generation

**Meta Framework Validation**: All intention detection must pass `meta/validation/validators/ai-instruction/command-intent-validator.md` with ≥90% accuracy

## Development Commands

### Setup and Initialization
```bash
# Initial setup
./setup.sh

# Validate knowledge base structure
./scripts/validate-knowledge-base.sh

# Create new feature workspace
./scripts/create-feature.sh [feature-name]
```

### Python Environment Management
```bash
# Knowledge Vault operations (Python-based)
cd knowledge-vault
python -m pip install -r requirements.txt

# Project-specific Python environments
cd projects/ai-knowledge-lifecycle-orchestrator
source venv/bin/activate
python -m pip install -r requirements.txt
```

### Validation and Testing
```bash
# Validate knowledge base health
./scripts/validate-knowledge-base.sh

# Test AI system workflows
cd ai/tests && ./run-tests.sh

# Validate schemas (Knowledge Vault)
cd knowledge-vault/operations/scripts
python validate_schemas.py
```

## Quality Standards

**Validation Requirements**:

- AI instruction files: ≥75/100 validation score
- Task completion: 6-step protocol within ≤180 seconds
- Cross-reference accuracy: 100% file path accessibility
- Anti-fiction compliance: Use `meta/validation/anti-fiction-safeguards.md` when preventing fabricated claims

**Design Excellence**: Use `projects/ai-agent-instruction-design-excellence/CLAUDE.md` when creating AI instructions

- Concrete specificity (≥95% accuracy thresholds)
- External dependency elimination
- Immediate actionability standards
- Progressive context loading (68% token reduction)

## Context Loading Strategy

**Immediate Loading** (@ prefix): Essential context needed for all operations

- Core requirements and constraints (this file)
- Quality standards and anti-fiction safeguards
- Essential cross-references for project coordination

**Conditional Loading** (bare paths): Load specific contexts when needed

- `development/CLAUDE.md` - When doing development work
- `ai/workflows/task-management/CLAUDE.md` - When managing tasks
- `research/orchestrator/integration/claude-orchestrator-integration.yaml` - When conducting research
- `meta/validation/validators/ai-instruction/` - When validation issues arise

**Usage Pattern**: Reference files using conditional format: "Use `file/path.md` when [specific condition]" rather than immediate @ loading to optimize context efficiency.

## Development Workflows

### Creating New Documents
```bash
# Interactive document creation
/create-document [type]

# Multi-agent orchestrated creation
/orchestrate-agents [document-type]

# Feature workspace creation (complete documentation set)
/create-feature [feature-name]
```

### Knowledge Vault Operations
```bash
# Create database items (requires Python environment)
cd knowledge-vault/operations/scripts
python mcp_operations_enhanced.py

# Sync with Notion (requires MCP Docker setup)
python update_notion_sync.py

# Validate system integrity
python validate_mcp_system.py
```

### Research Workflows
```bash
# Access research templates
ls research/templates/

# Review research findings
ls research/findings/

# Check orchestrator configuration
cat research/orchestrator/config/method-registry.yaml
```

## Key Configuration Files

### AI System Configuration
- `ai/context/dependencies.yaml` - Document dependency relationships
- `ai/context/document-registry.yaml` - Registry of all generated documents
- `ai/context/feature-registry.yaml` - Feature workspace tracking
- `ai/context/tier-configuration.yaml` - Document tier organization

### Knowledge Vault Configuration  
- `knowledge-vault/schemas/` - Database schema definitions (6 schemas)
- `knowledge-vault/shared/tags-vocabulary.yaml` - Standardized tag taxonomy
- `knowledge-vault/shared/status-workflows.yaml` - Status transition rules
- `knowledge-vault/operations/notion-integration.yaml` - MCP sync configuration

### Project Configuration
- `projects/*/CLAUDE.md` - Project-specific AI instructions
- `projects/*/task-list.md` - Project task management
- `projects/*/progress.md` - Project progress tracking

## Key Cross-References

**Framework Access** (Load when needed):

- Tasks: `ai/workflows/task-management/CLAUDE.md`
- Development: `development/CLAUDE.md`
- Validation: `meta/validation/validators/ai-instruction/`
- Commands: `.claude/commands/*` - Use for standardized execution workflows

**Project Resources** (Load when working on specific projects):

- Design Excellence: `projects/ai-agent-instruction-design-excellence/CLAUDE.md`
- Claude Capabilities: `projects/ai-knowledge-base-enhancement/docs/claude-comprehensive-capabilities.md`
- MCP Registry: `projects/ai-knowledge-intelligence-orchestrator/docs/mcp-server-registry/`
- Task Lists: `projects/*/task-list.md`
- Progress: `projects/*/progress.md`

**Quality Assurance** (Load when quality issues arise):

- Anti-Fiction: `meta/validation/anti-fiction-safeguards.md`
- Command Guidelines: `meta/docs/claude-command-creation-guidelines.md`
- Intent Detection: `meta/shared/intention-detection-framework.md`
- MCP Learning: `meta/mcp-learning/` (error-logs/, usage-guides/, patterns/, templates/)

## Critical File Locations

### AI Templates and Prompts
- `ai/prompts/document-templates/` - 67+ document generation templates
- `ai/prompts/meta-prompts/` - AI agent coordination prompts
- `ai/orchestration/` - Agent hierarchy and coordination rules

### Knowledge Vault Data
- `knowledge-vault/databases/*/items/` - Database item storage (Markdown files)
- `knowledge-vault/core/` - System configuration and engines
- `knowledge-vault/operations/scripts/` - Automation and sync scripts

### Research and Analysis
- `research/findings/` - Comprehensive research results by topic
- `research/orchestrator/` - Research methodology configuration
- `research/sessions/` - Research session logs and metadata

## Integration Patterns

### MCP (Model Context Protocol) Integration
The system heavily utilizes MCP for:
- **Notion API integration** via `mcp__MCP_DOCKER__*` tools
- **Database operations** with automatic synchronization
- **External service integration** across projects

### Claude Code Command Integration
Commands serve dual purposes:
- **User interface**: Interactive document and feature creation
- **AI agent interface**: Programmatic workflow execution

### Cross-Component Data Flow
1. **Research** findings inform **Project** implementations
2. **Knowledge Vault** provides structured storage for **AI** system outputs
3. **AI** orchestration manages **Project** documentation lifecycles
4. **Projects** contribute patterns back to **AI** templates and **Research** methodologies

## Quality Assurance

### Validation Layers
1. **Schema Validation**: All data structures validated against YAML schemas
2. **Relationship Integrity**: Bidirectional consistency checks
3. **Business Logic**: Workflow and status transition validation
4. **Quality Metrics**: Completeness, consistency, and freshness scoring

### Performance Targets
- **Search Response**: <2 seconds for tag-based queries
- **Sync Performance**: >3 items per minute for Notion integration
- **System Health**: >90% overall health score
- **Validation Success**: >95% automatic validation with <2% false positives

## Development Guidelines

### When Working with AI Components
- Always check `ai/context/dependencies.yaml` before creating new documents
- Use existing templates from `ai/prompts/document-templates/`
- Update registries automatically via command workflows
- Follow agent hierarchy patterns for complex workflows

### When Working with Knowledge Vault
- Use standardized tags from `knowledge-vault/shared/tags-vocabulary.yaml`
- Maintain bidirectional relationships for all cross-references
- Follow database-specific workflows in `knowledge-vault/shared/status-workflows.yaml`
- Validate changes using scripts in `knowledge-vault/operations/scripts/`

### When Working with Projects
- Each project has its own `CLAUDE.md` with specific instructions
- Track progress in project-specific `progress.md` files
- Integrate research findings from `research/findings/`
- Use established patterns from successful project implementations

## Task Management Protocol

**Essential Requirement**: All AI agents MUST follow standardized task completion procedures.

**Core Protocol**: 6-step task completion within ≤180 seconds:

1. Mark TodoWrite complete with timestamps
2. Update projects/\*/docs/task-list.md synchronously
3. Document outcomes in progress.md with scores
4. Create follow-up tasks with priorities
5. Validate @file_path cross-references
6. Verify completion criteria

**Specialized Task Management**: Use `ai/workflows/task-management/CLAUDE.md` for comprehensive procedures, templates, and enforcement protocols.

**Enforcement**: Task completion protocol violations trigger automatic escalation and performance penalties.

## AI Agent Instruction Standards

**Essential Requirement**: All AI agent instruction files MUST follow validated creation protocols.

**Core Standards**:

- Eliminate human documentation artifacts (Purpose, Overview, Usage sections forbidden)
- Start with direct actionable instructions (no titles or explanations)
- Achieve ≥75/100 validation score using meta validation tools
- Ensure 100% @file_path cross-reference accessibility

**Comprehensive Guidelines**: Use `meta/docs/claude-command-creation-guidelines.md` and validation tools at `meta/validation/validators/ai-instruction/`

**Enforcement**: Invalid AI instruction files must be rewritten with compliant patterns before deployment.

## Anti-Fiction and Quality Assurance

**Essential Requirement**: All AI agents MUST prevent academic contamination and fabricated claims.

**Core Safeguards**:

- Verify all numerical claims with sources (file_path:line_number format)
- Label data type clearly: Verified/Estimated/Analysis/Unknown
- Maintain cognitive separation between academic analysis and operational execution
- Restrict knowledge-vault access to explicitly authorized research tasks

**Comprehensive Anti-Fiction Framework**: Use `meta/validation/anti-fiction-safeguards.md` for complete protocols, including:

- Real-time fact validation checkpoints
- Evidence citation requirements
- Academic content quarantine procedures
- Contamination detection and recovery protocols

**Enforcement**: Anti-fiction violations trigger immediate task invalidation and protocol restart.

## MCP Error Learning Protocol

**Essential Requirement**: All AI agents MUST systematically learn from MCP server errors to prevent repetition.

**Core Protocol**:
1. **BEFORE MCP usage**: Check `meta/mcp-learning/usage-guides/[server-name]-guide.md` for known issues
2. **WHEN errors occur**: Log immediately using `meta/mcp-learning/templates/error-log-template.md`
3. **AFTER success**: Update usage guides with working patterns

**System Location**: `meta/mcp-learning/` (error-logs/, usage-guides/, patterns/, templates/)
**Enforcement**: Violations trigger automatic escalation and enhanced error monitoring

## Cursor Rules Integration
The repository includes Cursor-specific rules in `.cursor/rules/` that enforce:
- Consistent file structure and naming conventions
- AI agent instruction patterns
- Development workflow standards
- Code quality and documentation requirements