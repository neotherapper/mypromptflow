# AI Research Framework

## Project Overview

This is a comprehensive AI Research Framework with intelligent orchestration capabilities. The system provides 15 specialized research methods (11 existing + 4 advanced) with context-aware method selection and quality assurance.

## Key Capabilities

- **Intelligent Orchestration**: Context analysis automatically selects optimal research methods
- **15 Research Methods**: From simple step-by-step to complex multi-perspective approaches
- **Quality Enhancement**: Built-in validation using constitutional AI and self-consistency
- **Dual-Agent System**: Primary research + automatic evaluation and observation
- **Performance Tracking**: Comprehensive logging of decisions, timing, and outcomes

## Quick Start

1. **Request Research**: "Help me research [topic]"
2. **Orchestrator Analyzes**: Context complexity, domain, quality requirements
3. **Method Selection**: Appropriate research methods chosen automatically
4. **Research Execution**: AI agent conducts research using selected methods
5. **Quality Evaluation**: Test agent observes and evaluates process

## Framework Structure

```
research/
├── orchestrator/           # Intelligent method selection system
├── findings/              # Research outputs and execution logs
├── learning/              # Pattern observations and performance data
└── templates/             # Research document templates
```

## 📋 For AI Agents

**Read**: `@research/orchestrator/integration/gemini-orchestrator-integration.yaml`

This Gemini-specific integration file contains complete instructions for using the research framework, including:

- Gemini-optimized workflow patterns
- Multimodal analysis capabilities
- Large context window utilization
- Adaptive reasoning integration
- Real-time method selection
- Quality assurance procedures
- Gemini-enhanced orchestrator usage

## 🚨 MANDATORY RESEARCH COMPLETION REQUIREMENTS

**ALL AI AGENTS MUST CREATE THESE FILES WHEN CONDUCTING RESEARCH:**

### Required Files (Non-Negotiable)

1. **research-plan.md** - Research approach and method selection
2. **research-sources.md** - Complete source tracking with timestamps

### Templates Available

- `research/templates/research-plan-template.md`
- `research/templates/research-sources-template.md`

### Enforcement

- **INCOMPLETE RESEARCH** = Missing these files
- Use Write tool to create both files before ending research
- Track ALL sources: WebFetch, WebSearch, Read, file access
- Include timestamps and relevance for each source
