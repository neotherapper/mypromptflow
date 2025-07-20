# Framework Selector - Automated Decision Tree

## Quick Framework Selection

**Use this automated analysis to select the optimal framework for your instruction problem.**

## ⚠️ CRITICAL: No Fictional Assessments

**BEFORE USING THIS FRAMEWORK:**
- ✅ **MUST read and analyze the actual target instruction file**
- ✅ **MUST apply these checklists to real file content**  
- ✅ **MUST document findings with specific line references**
- ✅ **MUST calculate scores using documented formulas**
- ❌ **CANNOT estimate, guess, or fabricate assessment results**
- ❌ **CANNOT create fictional scores or placeholder findings**

**Realistic Assessment Time**: 5-8 minutes per instruction (not 30 seconds)

### Instruction Analysis Workflow

#### Step 0: MANDATORY Asset Discovery (30 seconds)

**⚠️ CRITICAL: Always check for existing assets before framework application**

```bash
# MANDATORY FIRST STEP - Asset Discovery Protocol
check_existing_assets() {
    echo "=== MANDATORY ASSET DISCOVERY ==="
    
    # 1. Check for existing validators/specialists
    if [ -f "meta/validators/registry.yaml" ]; then
        echo "✅ Validator registry found - checking for existing coverage"
        existing_coverage=$(cat meta/validators/registry.yaml)
        echo "Existing specialists: $(echo "$existing_coverage" | grep -c "name:")"
    else
        echo "❌ No validator registry found - progressive loading opportunity exists"
        echo "📋 Recommendation: Consider Progressive Loading Framework for token efficiency"
    fi
    
    # 2. Check for progressive loading opportunities
    monolithic_instruction_size=$(wc -l < "$target_instruction_file")
    if [ "$monolithic_instruction_size" -gt 200 ]; then
        echo "🔍 Large instruction detected ($monolithic_instruction_size lines)"
        echo "📋 STRONG RECOMMENDATION: Assess Progressive Loading Framework FIRST"
        echo "   → Expected 50-80% token savings for conditional execution scenarios"
    fi
    
    # 3. Check for domain knowledge patterns
    domain_count=$(count_distinct_expertise_areas "$target_instruction_file")
    if [ "$domain_count" -gt 2 ]; then
        echo "🎯 Multiple domain expertise detected ($domain_count domains)"
        echo "📋 PROGRESSIVE LOADING CANDIDATE: Coordinator-specialist architecture recommended"
    fi
}
```

**Asset Discovery Decision Points:**

1. **✅ Existing Assets Found**: 
   - Review existing capabilities before creating new frameworks
   - Consider extending existing assets instead of new framework application
   - Check coverage gaps that frameworks might address

2. **🔍 Progressive Loading Opportunity**:
   - Instruction >200 lines with multiple domains
   - Conditional execution scenarios present
   - **FIRST assess [Progressive Loading Framework](../design-principles/progressive-loading/overview.md)**
   - Expected 50-80% token efficiency gains

3. **📋 No Existing Assets**: 
   - Proceed with standard framework selection
   - Document new assets for future discovery

#### Step 1: Analyze the Problem Instruction (5-8 minutes realistic)

**After completing mandatory asset discovery, read your instruction and answer these questions:**

1. **Vagueness Detection**:
   - [ ] Contains vague terms ("effectively", "efficiently", "appropriately", "properly")
   - [ ] Missing specific parameters, values, or thresholds
   - [ ] Uses subjective measures ("good", "high quality", "optimal")

2. **Purpose Clarity**:
   - [ ] Unclear what the end goal or success looks like
   - [ ] Missing agent roles or coordination structure
   - [ ] No hierarchy or responsibility definition

3. **Dependency Analysis**:
   - [ ] References external systems, APIs, or documentation
   - [ ] Mentions frameworks without explanation ("SuperClaude", "Claude Flow")
   - [ ] Requires web searches or external knowledge

4. **Executability Assessment**:
   - [ ] Requires interpretation or clarification
   - [ ] Missing step-by-step procedures
   - [ ] No clear success/failure criteria

5. **Progressive Loading Assessment**:
   - [ ] Instruction loads all knowledge regardless of execution path
   - [ ] Multiple domain expertise areas embedded in single instruction (TypeScript, Python, etc.)
   - [ ] Conditional scenarios use different knowledge subsets
   - [ ] Knowledge utilization varies significantly by context (simple vs complex scenarios)
   - [ ] Monolithic instruction with low utilization rates (<60%)

6. **AI Agent Consumption Efficiency**:
   - [ ] Contains academic justification without actionable value ("Research Foundation", "validated studies")
   - [ ] Includes explanatory text that doesn't change AI agent behavior
   - [ ] Has credibility building language ("research-proven", "comprehensive analysis")
   - [ ] Features performance benchmarks without actionable thresholds
   - [ ] Uses cognitive overhead patterns (background, context, justification sections)

7. **🚨 Cognitive Contamination Detection**:
   - [ ] Contains fabricated statistics or performance claims without sources
   - [ ] Uses academic writing style in operational instructions
   - [ ] Includes research-style language ("studies show", "research indicates")
   - [ ] Features unverified effectiveness percentages or metrics
   - [ ] Mixes human knowledge with AI agent execution instructions

#### Step 2: Framework Selection Logic

**Based on your answers above:**

```yaml
selection_logic:
  priority_framework_selection:
    if_progressive_loading_opportunity: "Progressive Loading Framework (ASSESS FIRST)"
    if_vagueness_detected: "Concreteness Framework"
    if_purpose_unclear: "Purpose-Driven Framework"
    if_external_dependencies: "Self-Sufficiency Framework"
    if_not_executable: "Actionable Framework"
    if_cognitive_overhead_detected: "Concreteness Framework + Cognitive Overhead Elimination"
    if_cognitive_contamination_detected: "IMMEDIATE Cognitive Contamination Cleanup + Framework Selection"
  
  multiple_issues_detected:
    progressive_loading_AND_any_issue: "Progressive Loading FIRST → then other frameworks"
    vague_AND_external_deps: "Self-Sufficiency → Concreteness"
    vague_AND_not_executable: "Actionable → Concreteness"
    unclear_purpose_AND_external_deps: "Self-Sufficiency → Purpose-Driven"
    unclear_purpose_AND_not_executable: "Purpose-Driven → Actionable"
    cognitive_overhead_AND_any_issue: "Apply Cognitive Overhead Elimination FIRST, then selected framework"
  
  ai_agent_instruction_assessment:
    mandatory_consumption_efficiency_check: true
    cognitive_overhead_elimination_required: true
    target_consumption_ratio: "≥80% actionable content"
    maximum_academic_justification: "0 lines"
```

### Automated Framework Recommendation

**Use this decision tree for instant framework selection:**

#### Decision Tree A: Single Framework Selection

**If you checked boxes in only ONE category above:**

- **Progressive Loading only** → **[Progressive Loading Framework](../design-principles/progressive-loading/overview.md)** (ASSESS FIRST - 50-80% token savings)
- **Vagueness only** → **[Concreteness Framework](../design-principles/concreteness/overview.md)**
- **Purpose only** → **[Purpose-Driven Framework](../design-principles/purpose-driven/overview.md)**
- **Dependencies only** → **[Self-Sufficiency Framework](../design-principles/self-sufficiency/overview.md)**
- **Executability only** → **[Actionable Framework](../design-principles/actionable/overview.md)**
- **Cognitive Overhead only** → **[Concreteness Framework with Cognitive Overhead Elimination](../design-principles/concreteness/overview.md)** (See Technique 13: Academic Justification Removal)
- **🚨 Cognitive Contamination detected** → **IMMEDIATE contamination cleanup required** (See Decision Tree D below)

#### Decision Tree B: Multiple Framework Selection

**If you checked boxes in multiple categories:**

**2 Categories Checked:**
- **Progressive Loading + Any Other** → Start with [Progressive Loading](../design-principles/progressive-loading/overview.md), then selected framework
- **Vagueness + Dependencies** → Start with [Self-Sufficiency](../design-principles/self-sufficiency/overview.md), then [Concreteness](../design-principles/concreteness/overview.md)
- **Vagueness + Executability** → Start with [Actionable](../design-principles/actionable/overview.md), then [Concreteness](../design-principles/concreteness/overview.md)
- **Purpose + Dependencies** → Start with [Self-Sufficiency](../design-principles/self-sufficiency/overview.md), then [Purpose-Driven](../design-principles/purpose-driven/overview.md)
- **Purpose + Executability** → Start with [Purpose-Driven](../design-principles/purpose-driven/overview.md), then [Actionable](../design-principles/actionable/overview.md)

**3+ Categories Checked:**
- **Comprehensive transformation needed** → Use [Implementation Path Guide](implementation-paths.md) for systematic multi-framework application

#### Decision Tree C: AI Agent Instruction Assessment (Special Case)

**⚠️ MANDATORY when assessing AI agent instructions FOR AI agents:**

**Cognitive Overhead Detection (Always check first):**
1. **Scan for Academic Patterns**:
   - "Research Foundation" sections
   - "Based on validated research findings"
   - "Performance benchmarks" without actionable thresholds
   - "This tool achieves X% effectiveness" (unless it sets usage thresholds)

2. **Apply Elimination Rules**:
   - **Remove**: Any content that doesn't change AI agent behavior
   - **Keep**: Only configuration parameters, usage instructions, error handling
   - **Transform**: Academic justification → actionable thresholds
   - **Target**: ≥80% actionable content ratio

3. **Consumption Efficiency Validation**:
   - Token density: Information per token ratio
   - Actionability score: Executable instructions percentage  
   - Cognitive load: Academic overhead detection
   - AI agent readiness: Can execute within 5-8 minutes without interpretation

**AI Agent Assessment Protocol:**
```bash
# Step 1: Cognitive overhead detection
if [academic_sections_detected]; then
  apply_cognitive_overhead_elimination_first
fi

# Step 2: Standard framework selection
apply_standard_framework_selection_logic

# Step 3: Consumption efficiency validation  
validate_ai_agent_consumption_efficiency
target_actionable_content_ratio: ≥80%
maximum_academic_justification: 0_lines
```

#### Decision Tree D: 🚨 Cognitive Contamination Emergency Protocol

**If cognitive contamination is detected (fabricated statistics, academic writing, research claims):**

```yaml
contamination_cleanup_protocol:
  step_1_immediate_action:
    priority: "CRITICAL - Stop all processing"
    action: "Identify contamination sources"
    time_limit: "30 seconds"
  
  step_2_quarantine:
    priority: "HIGH - Separate content types"
    action: "Quarantine academic content from operational instructions"
    target: "Move academic content to knowledge-vault/"
  
  step_3_cleanup:
    priority: "HIGH - Remove contamination"
    remove_patterns:
      - "Fabricated statistics (X% effectiveness, Y% reduction)"
      - "Academic language (studies show, research indicates)"
      - "Unverified performance claims"
      - "Research justification in operational instructions"
  
  step_4_validation:
    priority: "MEDIUM - Verify cleanup"
    verify: "100% actionable content, 0% academic contamination"
    check: "No fabricated claims, no research-style language"
  
  step_5_framework_selection:
    priority: "LOW - Resume normal processing"
    action: "Apply standard framework selection logic"
    note: "Only after contamination is eliminated"
```

**Contamination Recovery Examples:**

**Before (Contaminated)**:
```markdown
Based on research findings, this approach achieves 85% effectiveness rates across multiple domains...
```

**After (Clean)**:
```markdown
**Configuration**: Timeout thresholds: 30-60 seconds, retry limit: 3 attempts
```

### Common Problem Patterns

#### Pattern 0: Large Multi-Domain Instruction (NEW - ASSESS FIRST)
**Example**: "500-line PR validation instruction with TypeScript, Python, YAML, and security validation all embedded"
**Analysis**: Multiple domains (4+) + conditional scenarios + low utilization for simple PRs (30%)
**Framework Selection**: Progressive Loading Framework (ASSESS FIRST)
**Expected Benefits**: 50-80% token savings through coordinator-specialist architecture
**Expected Load**: 50-250 lines based on detected domains vs 500 lines always

#### Pattern 1: "Coordinate agents effectively using best practices"
**Analysis**: Vague terms ("effectively", "best practices") + unclear execution steps
**Framework Selection**: Actionable → Concreteness
**Expected Load**: 600-800 lines of context

#### Pattern 2: "Use SuperClaude patterns for optimization"
**Analysis**: External dependency ("SuperClaude") + vague outcome ("optimization")
**Framework Selection**: Self-Sufficiency → Concreteness
**Expected Load**: 800-1000 lines of context

#### Pattern 3: "Create a system that works well for users"
**Analysis**: Unclear purpose ("works well") + vague success criteria
**Framework Selection**: Purpose-Driven → Actionable
**Expected Load**: 700-900 lines of context

#### Pattern 4: "Implement quantum-safe encryption using industry standards"
**Analysis**: External dependency ("industry standards") + technical complexity
**Framework Selection**: Self-Sufficiency → Purpose-Driven
**Expected Load**: 900-1200 lines of context

#### Pattern 5: AI Agent Instruction with Cognitive Contamination (UPDATED)
**Example**: "Based on comprehensive research, this framework achieves 85% effectiveness rates across multiple validation scenarios..."
**Analysis**: 🚨 COGNITIVE CONTAMINATION - Fabricated statistics + academic language + no verifiable source
**Framework Selection**: IMMEDIATE Contamination Cleanup → Standard Framework Selection
**Detection Triggers**: Fabricated percentages, "research shows", unverified effectiveness claims, academic justification in operational instructions
**Contamination Cleanup**: Remove fabricated statistics, eliminate academic language, replace with actionable configuration parameters
**Required Action**: Apply Decision Tree D (Cognitive Contamination Emergency Protocol)

### Context Loading Optimization

#### Progressive Loading Strategy

**Single Framework (Simple Problems)**:
1. Load framework overview (300-400 lines)
2. Load specific technique module (400-600 lines)
3. Load examples if needed (300-500 lines)
4. Total: 700-1000 lines (vs 2000+ lines full framework)

**Multiple Frameworks (Complex Problems)**:
1. Load primary framework overview (300-400 lines)
2. Load primary framework techniques (400-600 lines)
3. Load secondary framework overview (300-400 lines)
4. Load secondary framework specific modules as needed (400-600 lines)
5. Total: 1000-1400 lines (vs 4000+ lines all frameworks)

#### Efficiency Calculations

**Context Load Optimization**:
```yaml
optimization_metrics:
  single_framework_problems:
    traditional_load: "2000+ lines (full framework)"
    progressive_load: "700-1000 lines (specific modules)"
    efficiency_gain: "60-65% reduction"
  
  multiple_framework_problems:
    traditional_load: "4000+ lines (all frameworks)"
    progressive_load: "1000-1400 lines (targeted modules)"
    efficiency_gain: "65-75% reduction"
```

### Quick Selection Shortcuts

#### 10-Second Selection Method

**For experienced users, use these shortcuts:**

1. **"interpret" or "clarify" needed** → Actionable Framework
2. **"external" references or undefined terms** → Self-Sufficiency Framework
3. **"vague" or "subjective" language** → Concreteness Framework
4. **"unclear goals" or "no coordination"** → Purpose-Driven Framework

#### Common Instruction Keywords

**Actionable Framework Triggers**:
- "coordinate", "manage", "handle", "optimize", "improve", "enhance"
- "monitor", "track", "supervise", "oversee", "control"
- "regularly", "appropriately", "effectively", "efficiently"

**Concreteness Framework Triggers**:
- "good", "better", "best", "optimal", "high quality"
- "appropriate", "suitable", "reasonable", "acceptable"
- "several", "some", "many", "various", "multiple"

**Self-Sufficiency Framework Triggers**:
- "SuperClaude", "Claude Flow", "industry standards", "best practices"
- "external API", "third-party", "documentation", "research"
- "web search", "latest information", "current data"

**Purpose-Driven Framework Triggers**:
- "system", "solution", "approach", "methodology", "process"
- "coordination", "management", "oversight", "supervision"
- "hierarchy", "organization", "structure", "framework"

### Validation Checklist

**Before proceeding to your selected framework:**

- [ ] **Problem clearly identified** - You understand what makes the instruction problematic
- [ ] **Framework selected** - You've chosen the most appropriate framework(s)
- [ ] **Loading strategy planned** - You know which modules to load first
- [ ] **Context budget estimated** - You understand the expected context load
- [ ] **Success criteria defined** - You know what constitutes successful transformation

### Integration with Assessment Tools

**After framework selection:**
1. **Load framework overview** to understand the approach
2. **Use assessment tools** to score your instruction
3. **Select specific modules** based on assessment results
4. **Apply transformation techniques** systematically
5. **Validate results** using quality gates

### Framework Selection Examples

#### Example 1: E-commerce System Instruction
**Original**: "Create a robust e-commerce platform that handles user transactions efficiently"
**Analysis**: Vague terms ("robust", "efficiently") + unclear success criteria
**Selection**: Actionable → Concreteness
**Context Load**: ~800 lines

#### Example 2: AI Research Instruction
**Original**: "Research the latest developments in AI using SuperClaude methodologies"
**Analysis**: External dependency ("SuperClaude") + vague scope ("latest developments")
**Selection**: Self-Sufficiency → Concreteness
**Context Load**: ~1000 lines

#### Example 3: Team Coordination Instruction
**Original**: "Coordinate the development team to deliver the project on time"
**Analysis**: Unclear coordination approach + vague success criteria
**Selection**: Purpose-Driven → Actionable
**Context Load**: ~900 lines

This framework selector provides automated decision-making for optimal framework selection and context loading efficiency. Continue to [assessment-tools.md](assessment-tools.md) for detailed instruction evaluation or [implementation-paths.md](implementation-paths.md) for step-by-step implementation guidance.