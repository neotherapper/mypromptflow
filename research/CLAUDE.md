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

**Read**: `@research/orchestrator/integration/claude-orchestrator-integration.yaml`

This Claude-specific integration file contains complete instructions for using the research framework, including:

- CLI workflow patterns
- Orchestrator usage instructions
- Method selection guidance
- Quality assurance procedures
- Logging and evaluation requirements

## 🚨 MANDATORY RESEARCH COMPLETION REQUIREMENTS

**ALL AI AGENTS MUST FOLLOW ENHANCED FILE STRUCTURE AND VALIDATION:**

### Enhanced File Structure (Required)

All research must use the enhanced folder structure:

```
research/findings/[topic]/
├── research/                    # All research content
│   ├── comprehensive-analysis.md  # Main combined analysis
│   ├── perspective-1-quantitative.md  # Individual outputs (multi-perspective)
│   ├── perspective-2-qualitative.md   # Individual outputs (multi-perspective)
│   ├── phase-1-discovery.md          # Individual outputs (step-by-step)
│   └── [other method-specific files]  # Based on method used
└── .meta/                       # All metadata and tracking (hidden folder)
    ├── research-execution-log.yaml
    ├── research-metadata.yaml
    ├── method-compliance.yaml      # NEW: Method validation
    ├── research-plan.md
    └── research-sources.md
```

### 🚨 CRITICAL PATH ENFORCEMENT 🚨

**RESEARCH FINDINGS MUST GO IN /research/findings/ - NEVER /docs/ OR ANY OTHER LOCATION**

**BEFORE CREATING ANY FILES:**
1. **VERIFY** the path starts with `research/findings/`
2. **DOUBLE-CHECK** you are not using `docs/`, `projects/`, `ai/`, or any other base path
3. **CONFIRM** the folder structure follows the exact pattern: `research/findings/[topic]/research/` and `research/findings/[topic]/.meta/`

**FORBIDDEN PATHS:**
- ❌ `docs/research-findings/` 
- ❌ `docs/`
- ❌ `projects/*/docs/`
- ❌ `ai/`
- ❌ Any path other than `research/findings/`

**REQUIRED PATHS:**
- ✅ `research/findings/[topic]/research/comprehensive-analysis.md`
- ✅ `research/findings/[topic]/.meta/research-plan.md`
- ✅ `research/findings/[topic]/.meta/research-sources.md`

### Required Files (Non-Negotiable)

**Research Content Files:**

1. **comprehensive-analysis.md** - Main research output
2. **Individual method outputs** - All sub-agent research (perspectives, phases, modules)

**Meta Documentation Files:** 3. **research-plan.md** - Research approach and method selection 4. **research-sources.md** - Complete source tracking with timestamps 5. **method-compliance.yaml** - Method validation and compliance tracking 6. **research-execution-log.yaml** - Complete execution tracking

### Method Compliance Validation (NEW)

**AI agents must validate that sub-agents properly follow research method prompts:**

- **Multi-Perspective Method**: Must generate 4 distinct perspective files with unique expert personas
- **Step-by-Step Method**: Must complete all 5 phases with documented deliverables
- **Constitutional AI**: Must complete all 6 phases including self-evaluation and correction
- **Complex Research**: Must create all planned modules with clear boundaries
- **All Methods**: Must follow the specific structure and requirements of the chosen method

### Templates Available

- `research/templates/research-plan-template.md`
- `research/templates/research-sources-template.md`
- `research/templates/method-compliance-template.yaml` (NEW)
- `research/templates/research-execution-log-template.yaml`

### Enforcement

- **INCOMPLETE RESEARCH** = Missing required files OR failing method compliance
- Use Write tool to create ALL required files before ending research
- Validate method compliance using the compliance template
- Track ALL sources: WebFetch, WebSearch, Read, file access
- Include timestamps and relevance for each source
- **No research is considered complete without method compliance validation**

## 🔍 How to Use Method Compliance Validation

### Step 1: During Research Execution

1. **Follow Method Prompts**: Use the exact structure from `research/orchestrator/methods/[method].md`
2. **Create Individual Outputs**: Save each sub-agent research as separate files
3. **Document Method Steps**: Track completion of each method component

### Step 2: After Research Completion

1. **Create Compliance File**: Use `research/templates/method-compliance-template.yaml`
2. **Validate Method Adherence**: Check if all method requirements were met
3. **Score Compliance**: Rate how well the method was followed (0-1 scale)
4. **Document Issues**: Record any deviations from method requirements

### Step 3: Quality Verification

1. **Check File Structure**: Ensure all files are in correct research/ and meta/ folders
2. **Verify Individual Outputs**: Confirm all method components have corresponding files
3. **Validate Integration**: Ensure individual outputs are properly combined in main analysis
4. **Update Execution Log**: Include compliance results in research-execution-log.yaml

### Example: Multi-Perspective Method Validation

```yaml
method_validation:
  multi_perspective_approach:
    required_perspectives: 4
    expected_outputs:
      - "perspective-1-quantitative.md" ✓
      - "perspective-2-qualitative.md" ✓
      - "perspective-3-industry-practice.md" ✓
      - "perspective-4-future-trends.md" ✓
    compliance_checks:
      perspective_count: 4
      distinct_personas: true
      methodology_variance: true
      source_diversity: true
      integration_quality: 0.92
```

**This validation system ensures no research work is lost and method prompts are properly followed.**
