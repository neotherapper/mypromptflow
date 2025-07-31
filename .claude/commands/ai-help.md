🤖 AI Knowledge Intelligence Meta-Orchestrator

Display this interactive menu to the user:
═══════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────┐
│ 🚀 QUICK TOOLS - Simple & Immediate │
├─────────────────────────────────────────────────────────────────────┤
│ [1] Create Document [5] Analyze Dependencies │
│ [2] Fix GitHub Issue [6] System Status & Navigation │
│ [3] Knowledge Base Validation [7] System Improvement │
│ [4] Generate Tier Documents [8] Browse All Commands │
│ [9] Browse Research History [0] Quick Research Analysis │
│ [J] JIRA Integration - VanguardAI Project Access │
├─────────────────────────────────────────────────────────────────────┤
│ 🧠 ADVANCED FRAMEWORKS - Production-Ready Orchestrators │
├─────────────────────────────────────────────────────────────────────┤
│ [R] Research Orchestrator [P] Project Creation Framework │
│ [V] Validation Framework [S] AI-SDLC Assistant │
│ [F] Feature Development [O] Multi-Agent Orchestration │
├─────────────────────────────────────────────────────────────────────┤
│ ⚡ REVOLUTIONARY CAPABILITIES - Breakthrough Technology │
├─────────────────────────────────────────────────────────────────────┤
│ [PR] PR Validation │
│ [AI] Constitutional AI Compliance Framework │
│ [TOOLS] MCP Servers & Tools Integration Hub │
└─────────────────────────────────────────────────────────────────────┘

💬 **How to Use:**
• **Menu Code + Request:** "R blockchain adoption analysis" or "J 2" (current sprint)
• **Natural Language:** "I want to research blockchain for my company" or "Show me JIRA tasks"
• **Menu Code Only:** "1" (I'll ask for specifics)
• **Full Description:** "Help me validate pull request 23 for scope creep"

**What would you like to work on?** Type your choice and I'll route you to the right tool or orchestrator.

---

## AI AGENT ROUTING INSTRUCTIONS (INTERNAL - DO NOT SHOW TO USER)

## Command Routing Logic

**When user provides input, I will:**

### 🚀 Quick Tools Routing

- **[1] + [type]** → Execute `/create-document [type]` with template selection
- **[2] + [issue]** → Execute `/fix-github-issue [issue]` or `/gh-issue [issue]`
- **[3]** → Execute `/validate-knowledge-base` for comprehensive health check
- **[4] + [tier]** → Execute `/generate-tier-documents [tier]` for bulk generation
- **[5] + [document]** → Execute `/analyse-dependencies [document]` for dependency analysis
- **[6]** → Execute `/knowledge-status` for interactive system navigation
- **[7]** → Execute `/improve-claude` for system improvement suggestions
- **[8]** → Show complete command reference from `.claude/commands/`
- **[9]** → Display research registry with all completed research organized by category and quality scores
- **[0] + [topic]** → Analyze research registry for similarity to proposed topic and provide recommendations
- **[J] + [option]** → Execute `/jira [option]` for VanguardAI project access via symlink

### 🧠 Advanced Frameworks Routing

- **[R] + [topic]** → Execute registry analysis FIRST, then `/research [topic]` using research orchestrator with similarity assessment
- **[P] + [name]** → Execute `/create-project [name]` with comprehensive setup
- **[V] + [file]** → Execute `/validation-framework [file]` with AI Agent Design Standards
- **[S]** → Execute `/ai-sdlc-assistant` for role-based development workflows
- **[F] + [name]** → Execute `/create-feature [name]` with 5-phase development
- **[O] + [target]** → Execute `/orchestrate-agents [target]` for multi-agent coordination

### ⚡ Advanced Capabilities Routing

- **[PR] + [number]** → Execute `/validate-pr [number]` with target alignment score ≥85%
- **[AI]** → Display comprehensive guide to AI Agent Instruction Design Framework with usage examples and assessment tools
- **[TOOLS]** → Display curated catalog of available MCP servers with integration examples and setup instructions

### 💬 Natural Language Processing

**Framework Integration**: Apply intention detection using @meta/shared/intention-detection-framework.md

- **Research Detection**: Apply `research_intention_triggers` → Route to `/research [extracted_topic]`
- **Creation Detection**: Apply `creation_intention_triggers` → Route to appropriate creation command  
- **Validation Detection**: Apply `validation_intention_triggers` → Route to validation framework
- **JIRA Detection**: Apply `jira_intention_triggers` → Route to `/jira [extracted_context]`
- **Context Analysis**: Use `complexity_indicators` and `quality_requirements` for intelligent routing
- **Command Routing**: Apply `command_routing_patterns` with natural language processing backup

## Special Option Implementations

### [AI] - AI Agent Instruction Design Framework Guide

When user selects [AI], display:

```
🧠 AI Agent Instruction Design Excellence Framework
==================================================

📋 **Framework Overview:**
- Constitutional AI compliance validation (accuracy, transparency, completeness, responsibility, integrity)
- Vagueness detection and concrete instruction generation
- Anti-fiction validation for evidence-based reporting
- Framework coherence analysis for structural consistency
- Communication pattern validation for multi-agent systems

⚡ **Available Assessment Tools:**
- /validation-framework [file] - Comprehensive framework validation
- Constitutional AI compliance checking
- Instruction clarity and actionability assessment

📖 **Documentation Location:** @projects/ai-agent-instruction-design-excellence/

🎯 **Usage Examples:**
- "V my-instruction.md" - Validate AI agent instruction file
- "Validate the PR validation command for constitutional compliance"
- "Check my Claude command for vagueness and clarity issues"

Type 'V' followed by a filename to validate an AI instruction, or ask specific questions about the framework.
```

### [TOOLS] - MCP Servers Catalog

When user selects [TOOLS], display:

```
🔧 Available MCP Servers & Integration Tools
===========================================

📡 **Core MCP Servers:**
- **Notion**: Database and page management
- **Browser**: Web automation and testing
- **Jira**: Issue tracking and project management
- **Wikipedia**: Knowledge search and research
- **Fetch**: Web content retrieval and analysis

📊 **AI-Specific Tools:**
- Sequential thinking for complex problem solving
- Library documentation access and integration
- Search and research orchestration
- Automated prompt engineering frameworks

🔗 **Integration Examples:**
- "Research quantum computing using Wikipedia MCP"
- "Create Notion page with research findings"
- "Validate PR using browser automation"

💡 **Setup Instructions:**
MCP servers are pre-configured. Use natural language to request actions:
- "Search Wikipedia for [topic]"
- "Create Notion database for [purpose]"
- "Browse to [URL] and analyze content"

Registry: @knowledge-vault/databases/tools_services/
```

### [9] - Research Registry Browser

When user selects [9], execute:

**Dynamic Research Browser Implementation:**
1. **Load Research Data**: Read `research/findings/research-browser.yaml` using Read tool
2. **Extract Display Data**: Parse research categories, quality dashboard, and recent research
3. **Format for Display**: Apply display templates from research-browser.yaml
4. **Present Organized View**: Show research by category with human-friendly formatting

**Display Format** (loaded dynamically from research-browser.yaml):
```
📚 Research Registry - Completed Research History
===============================================

{quality_dashboard.dashboard_summary}

📊 **Research Categories**:

{for each category in research_categories:}
**{category.category_emoji} {category.category_name}** ({category.research_count} sessions):
{category.description}
Average Quality: {category.average_quality}% | Recent: {category.recent_activity}

{for each research_item in category.research_items:}
- **{research_item.title}** ({research_item.quality_badge}) - {research_item.completion_date}
  Key Outcome: {research_item.one_line_outcome}
  Applications: {research_item.primary_application}
  Location: {research_item.location}

💡 **Usage**:
- Type "0 [your topic]" to check similarity before new research
- Type "R [topic]" to proceed with research (includes automatic similarity check)
- All research locations: research/findings/[topic]/
- Full registry details: @research/findings/research-registry.yaml
```

**Error Handling**: If research-browser.yaml doesn't exist, display message: "Research browser not yet initialized. Complete one research session to generate human-friendly summaries."

### [0] - Quick Research Analysis  

When user provides [0] + [topic], execute:

**Registry Similarity Analysis Implementation:**
1. **Load Registry Data**: Read `research/findings/research-browser.yaml` and `research/findings/research-registry.yaml`
2. **Extract User Topic**: Parse topic from user input after [0]
3. **Perform Similarity Analysis**: Apply similarity calculation logic from research-browser.yaml
4. **Generate Recommendations**: Use decision framework thresholds (≥80% high, 40-79% moderate, <40% low)
5. **Display Results**: Format findings with similarity scores and specific recommendations

**Analysis Output Format**:
```
🔍 Research Registry Analysis for: {extracted_topic}
==========================================

**Step 1: Analyzing existing research...**
✅ Loaded {total_research_sessions} completed research sessions
✅ Performing semantic similarity analysis
✅ Calculating keyword overlap and domain matching

**Step 2: Similarity Assessment**

{if high_similarity_matches found:}
**🔍 High Similarity (≥80%)**:
- **{research_title}** (Quality: {quality_percentage}%, Similarity: {similarity_score}%)
  Key Outcomes: {one_line_outcome}
  📍 Location: {location}
  ✅ **Recommendation**: Reference existing research, avoid duplication
  
{if moderate_similarity_matches found:}
**🔄 Moderate Similarity (40-79%)**:
- **{research_title}** (Quality: {quality_percentage}%, Similarity: {similarity_score}%)
  Key Outcomes: {one_line_outcome} 
  📍 Location: {location}
  🔄 **Recommendation**: Build upon existing findings, cite previous work

{if low_similarity or no_matches:}
**✅ Low Similarity (≤39%)**:
✅ **Recommendation**: Proceed with comprehensive new research
🔗 Will reference any moderately related work where appropriate

**Decision Framework**:
- **High Similarity**: Reference existing research, avoid duplication
- **Moderate Similarity**: Extend existing research, build upon findings
- **Low Similarity**: Proceed with new research, reference related work

**Next Steps**:
- Type "R {topic}" to proceed with research (includes this analysis automatically)
- Type "9" to browse full research registry by category
- Ask specific questions about existing research findings
```

**Error Handling**: If similarity analysis fails, display: "Registry analysis unavailable. Proceeding with standard research workflow."

## Quick Reference

**All Available Commands:**

```
/research [topic]                - Advanced research orchestrator
/create-document [type]          - Document creation with templates
/create-feature [name]           - 5-phase feature development
/create-project [name]           - Full project initialization with templates and configuration
/validate-knowledge-base         - System health validation
/validate-pr [number]            - PR validation system
/validation-framework [file]     - Framework validation
/fix-github-issue [issue]        - GitHub issue resolution
/knowledge-status                - Interactive system navigation
/ai-sdlc-assistant              - Role-based workflows
/analyse-dependencies [document] - Dependency analysis
/orchestrate-agents [target]     - Multi-agent coordination
/generate-tier-documents [tier]  - Bulk document generation
/improve-claude                  - System improvement
/gh-issue [issue]               - GitHub CLI integration
/jira [option]                  - JIRA integration for VanguardAI project access
```

**Repository Knowledge Integration:**

- **AI Instruction Framework** → `@projects/ai-agent-instruction-design-excellence/`
- **Research Framework** → `@research/orchestrator/`
- **Command Templates** → `.claude/commands/`
- **Project Templates** → `projects/_template/`
- **Validation Tools** → `@meta/validation/validators/`

## System Information & Error Handling

**Invalid Input Handling:**

- Unknown menu codes: System will ask for clarification and show valid options
- Missing parameters: System will prompt for required information
- Inaccessible files: System will report error and suggest alternatives

**Resource Considerations:**

- Multi-agent operations may require additional processing time
- Research orchestrator operations involve multiple tool calls
- System performance depends on complexity of requested operations

**Limitations:**

- Validation accuracy may vary based on content complexity and context
- Some advanced features require specific project structure
- MCP server availability depends on system configuration

**Support:**

- Command reference: Type "8" or "Browse Commands"
- System status: Type "6" for health check and navigation
- Issues: Use "2" for GitHub issue resolution

**Ready to help! What would you like to do?**

Note: This system provides target performance thresholds based on framework design. Actual performance may vary based on system context and usage patterns.
