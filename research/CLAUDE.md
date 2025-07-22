# AI Research Framework

## Project Overview

This is a comprehensive AI Research Framework with intelligent orchestration capabilities. The system provides 15 specialized research methods (11 existing + 4 advanced) with context-aware method selection and quality assurance.

## Key Capabilities

- **Intelligent Orchestration**: Execute context analysis protocol (complexity scoring: 1-5 scale, domain classification: ≥85% confidence, method selection: ≤60s)
- **15 Research Methods**: Validated methodology range (simple step-by-step: 5 phases, complex multi-perspective: 4+ expert personas, execution time: 5-45 minutes per method)
- **Quality Enhancement**: Apply validation framework (constitutional AI: ≥95% compliance, self-consistency: ≥85% score, accuracy threshold: ≥90%)
- **Dual-Agent System**: Coordinate primary research agents with evaluation specialists (monitoring intervals: 5-15 minutes, quality checkpoints: continuous)
- **Performance Tracking**: Execute comprehensive logging protocol (decision timestamps, execution duration measurement, outcome quality scoring, method effectiveness analysis)

## Quick Start

1. **Request Research**: "Help me research [topic]" (topic specification: scope boundaries, depth requirements, quality thresholds)
2. **Orchestrator Analyzes**: Execute context analysis (complexity assessment: 30-45s, domain classification: ≥85% confidence, quality requirement parsing: ≤30s)
3. **Method Selection**: Apply selection algorithm (method compatibility scoring, resource estimation, execution time calculation: ≤60s total)
4. **Research Execution**: Coordinate AI agents using selected methods (parallel execution: 2-4 agents maximum, quality monitoring: continuous, timeout limits: 5-45 minutes per method)
5. **Quality Evaluation**: Execute validation protocol (accuracy verification: ≥90%, completeness assessment: ≥85%, consistency checking: ≥88%, constitutional compliance: ≥95%)

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

### 🔍 MANDATORY PRE-RESEARCH REGISTRY ANALYSIS (NEW)

**CRITICAL: Before starting ANY research, AI agents MUST execute registry similarity analysis:**

1. **Registry Analysis Requirement**: Execute Step 2.5 from @research/orchestrator/integration/claude-orchestrator-integration.yaml
2. **Similarity Assessment**: Compare proposed research against existing research in research/findings/research-registry.yaml
3. **Decision Framework**: 
   - **High Similarity (≥80%)**: Recommend referencing existing research instead of duplicating
   - **Moderate Similarity (40-79%)**: Recommend extending existing research with new perspectives
   - **Low Similarity (≤39%)**: Proceed with comprehensive new research
4. **User Interaction**: Present similarity findings and recommendations before proceeding
5. **Documentation**: Include registry analysis results in research-plan.md and execution-log.yaml

**Registry Analysis Files to Access**:
- `research/findings/research-registry.yaml` - Master research registry
- `research/findings/research-browser.yaml` - Human-friendly research browser (if available)
- Individual `research/findings/[topic]/summary.yaml` files for detailed comparison

**Enforcement**: Research conducted WITHOUT registry analysis is considered non-compliant and must be restarted.

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

**Meta Documentation Files:** 
3. **research-plan.md** - Research approach and method selection 
4. **research-sources.md** - Complete source tracking with timestamps 
5. **method-compliance.yaml** - Method validation and compliance tracking 
6. **research-execution-log.yaml** - Complete execution tracking

**Human-Friendly Summary Files (NEW - MANDATORY):**
7. **summary.yaml** - Human-readable research summary using research-summary-template.yaml
8. **research-browser.yaml** (updated) - Master research browser file for ai-help.md integration

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

### 📝 MANDATORY POST-RESEARCH SUMMARY GENERATION (NEW)

**CRITICAL: After completing research, AI agents MUST generate human-friendly summaries:**

1. **Individual Summary Creation**: 
   - Create `research/findings/[topic]/summary.yaml` using @research/templates/research-summary-template.yaml
   - Extract quality metrics from research-execution-log.yaml
   - Generate executive summary from comprehensive-analysis.md
   - Apply automatic categorization based on domain keywords
   - Calculate similarity scores against existing research

2. **Research Browser Update**:
   - Update `research/findings/research-browser.yaml` using @research/templates/research-browser-template.yaml  
   - Add new research to appropriate category
   - Update statistics (total sessions, average quality, recent activity)
   - Refresh dashboard metrics and recent research lists
   - Validate category assignment and cross-references

3. **Integration Requirements**:
   - Summaries must be readable by ai-help.md option [9] for research browsing
   - Support similarity analysis for ai-help.md option [0] 
   - Enable registry analysis for future research sessions
   - Maintain consistency with research-registry.yaml

**Template Files to Use**:
- `research/templates/research-summary-template.yaml` - Individual research summaries
- `research/templates/research-browser-template.yaml` - Master browser file structure

**Validation Requirements**:
- summary.yaml contains all required fields from template
- research-browser.yaml successfully updated with new research
- Category assignment based on keyword analysis is accurate
- All file paths and cross-references are valid and accessible

**Enforcement**: Research is NOT COMPLETE until both summary files are created and validated. Missing summaries = research not discoverable via ai-help.md interface.

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
