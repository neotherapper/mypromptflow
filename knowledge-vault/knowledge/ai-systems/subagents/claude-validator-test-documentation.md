# Claude Agent Validator Test Documentation

This document provides comprehensive testing instructions for AI agents to validate the effectiveness of the rewritten claude-agent-validator subagent using AI-generated blueprint patterns.

## Test Overview

**Objective**: Validate that the claude-agent-validator correctly identifies compliance issues, structural problems, and quality improvements using the AI-generated blueprint system.

**Scope**: Test validation of both compliant and non-compliant subagent configurations against blueprint standards.

**Success Criteria**: Validator must achieve >90% accuracy in identifying structural compliance, content quality, and assessment effectiveness issues.

## Test Execution Instructions

### Step 1: Invoke Claude Agent Validator

Use the Task tool to call the claude-agent-validator with this exact format:

```
I need to test the claude-agent-validator subagent. Please use the claude-agent-validator to analyze the [TARGET_SUBAGENT_NAME] subagent configuration and provide a comprehensive validation report.
```

### Step 2: Assess Validation Report Quality

Evaluate the validator's response against these criteria:

**Report Structure Requirements:**

- [ ] Provides numerical scores (0-100 scale) for structural compliance
- [ ] Identifies specific pattern violations with exact corrections
- [ ] Generates prioritized improvement recommendations
- [ ] References AI-generated blueprint standards explicitly
- [ ] Flags fabricated properties (sdlc_stage, context_isolation) if present

**Quality Assessment Depth:**

- [ ] Validates "You are" opening pattern compliance
- [ ] Checks "## Core Responsibilities" section structure
- [ ] Verifies 4-6 categorized technical areas
- [ ] Confirms 4-7 responsibilities per category
- [ ] Evaluates assessment instruction effectiveness

## Test Cases

### Test Case 1: Compliant AI-Generated Pattern

**Target**: security-code-reviewer.md (Known AI-generated compliant agent)

**Expected Results:**

- Structural compliance score: 85-100
- Content quality score: 85-100
- Assessment effectiveness score: 85-100
- Minimal improvement recommendations
- Recognition of AI-generated blueprint compliance

**Validation Commands:**

```
Test the claude-agent-validator against the security-code-reviewer subagent. This should score highly as it follows AI-generated patterns.
```

### Test Case 2: Fabricated Properties Detection

**Target**: Any manual subagent with fabricated properties

**Expected Results:**

- Must flag sdlc_stage as fabricated (doesn't exist in Claude Code)
- Must flag context_isolation as fabricated property
- Must flag framework_integration as non-existent
- Structural compliance score should be reduced for fabricated properties
- Specific recommendations to remove fabricated properties

**Validation Commands:**

```
Use the claude-agent-validator to check the [MANUAL_SUBAGENT_NAME] for fabricated properties that don't exist in Claude Code specifications.
```

### Test Case 3: Structural Pattern Compliance

**Target**: requirements-analyst.md or system-architect.md (Manual agents)

**Expected Results:**

- Must identify missing "You are" opening pattern
- Should flag lack of "## Core Responsibilities" structure
- Must identify category organization issues
- Should recommend AI-generated blueprint structure adoption
- Structural compliance score: 40-70 (medium range for manual agents)

**Validation Commands:**

```
Validate the structural compliance of the requirements-analyst subagent using the claude-agent-validator against AI-generated blueprint patterns.
```

### Test Case 4: Assessment Instruction Effectiveness

**Target**: fullstack-performance-optimizer.md (Has strong assessment instructions)

**Expected Results:**

- High assessment effectiveness score (85-100)
- Recognition of clear behavioral directive pattern
- Acknowledgment of specific deliverable requirements
- Confirmation of business alignment statements
- Validation of coordination protocol clarity

**Validation Commands:**

```
Test the assessment instruction effectiveness in the fullstack-performance-optimizer using the claude-agent-validator.
```

### Test Case 5: Tool Configuration Analysis

**Target**: api-integration-specialist.md

**Expected Results:**

- Validation of tool selection appropriateness
- Assessment of minimal necessary tools principle
- Domain-appropriate tool pattern recognition
- No kitchen sink approach flagging
- Tool efficiency recommendations if applicable

**Validation Commands:**

```
Use the claude-agent-validator to assess the tool configuration appropriateness in the api-integration-specialist subagent.
```

## Validation Criteria for Test Results

### Structural Compliance Validation

**Critical Requirements:**

- [ ] Identifies "You are" pattern presence/absence correctly
- [ ] Validates "## Core Responsibilities" section structure
- [ ] Counts technical categories accurately (expects 4-6)
- [ ] Counts responsibilities per category (expects 4-7)
- [ ] Flags fabricated properties with 100% accuracy

**Scoring Accuracy:**

- Compliant AI-generated agents: 85-100 score expected
- Manual agents with issues: 40-70 score expected
- Severely non-compliant: <40 score expected

### Content Quality Assessment

**Technical Precision Validation:**

- [ ] Identifies vague vs specific technical specifications
- [ ] Recognizes domain context integration quality
- [ ] Validates deliverable specification clarity
- [ ] Assesses collaboration protocol completeness

**Business Alignment Analysis:**

- [ ] Recognizes generic domain references vs specific context
- [ ] Validates business requirement integration
- [ ] Identifies professional workflow alignment

### Assessment Instruction Analysis

**Behavioral Directive Recognition:**

- [ ] Identifies "Always" vs "When" pattern usage
- [ ] Validates deliverable specification completeness
- [ ] Recognizes business alignment statement presence
- [ ] Confirms coordination requirement specification

**Quality Standards Validation:**

- [ ] Identifies production-readiness emphasis
- [ ] Validates code example requirements
- [ ] Confirms measurable outcome specifications

## Expected Validation Outputs

### High-Quality Validation Report Structure

```markdown
## Structural Compliance Score: [85-100]

- ✅ Opens with "You are" pattern
- ✅ Contains "## Core Responsibilities" section
- ✅ Has 5 categorized technical areas (optimal range)
- ✅ Each category has 5-6 responsibilities (optimal range)
- ✅ Ends with behavioral assessment instructions
- ⚠️ Uses only valid Claude Code properties

## Content Quality Score: [80-95]

- ✅ Technical specifications are precise and actionable
- ✅ Domain context integrated throughout
- ✅ Deliverables are specific and measurable
- ⚠️ Minor collaboration protocol clarity improvements needed

## Assessment Effectiveness Score: [90-100]

- ✅ Clear behavioral directive ("Always provide...")
- ✅ Specific deliverable requirements defined
- ✅ Business alignment explicitly stated
- ✅ Coordination requirements specified

## Priority Recommendations:

1. [High] Enhance collaboration protocol specificity
2. [Medium] Add more technical precision examples
3. [Low] Optimize tool selection efficiency
```

### Fabricated Property Detection Example

```markdown
## Critical Issues Identified:

**Fabricated Properties Detected:**

- ❌ `sdlc_stage: "implementation"` - This property does not exist in Claude Code
- ❌ `context_isolation: true` - This is a fabricated property
- ❌ `framework_integration: "research"` - Not a valid Claude Code property

**Required Actions:**

1. Remove all fabricated properties from frontmatter
2. Use only valid properties: name, description, tools, priority, team, environment
3. Restructure content to follow AI-generated blueprint patterns

**Compliance Impact:** Structural score reduced to 45/100 due to fabricated properties
```

## Test Success Indicators

### Validator Performance Benchmarks

**Detection Accuracy:**

- Fabricated properties: 100% detection rate required
- Structural patterns: >90% accuracy in pattern recognition
- Assessment instructions: >85% effectiveness evaluation accuracy
- Tool configuration: >80% appropriateness assessment accuracy

**Report Quality Standards:**

- Provides specific, actionable recommendations
- References AI-generated blueprint standards
- Includes numerical scoring with justification
- Offers concrete examples of improvements
- Maintains professional, constructive tone

### Validation Report Completeness

**Essential Elements:**

- [ ] Numerical scores for all three categories (structural, content, assessment)
- [ ] Specific improvement recommendations with priority levels
- [ ] Blueprint pattern compliance analysis
- [ ] Fabricated property detection results
- [ ] Tool configuration assessment
- [ ] Examples of optimal patterns to follow

## Troubleshooting Common Issues

### Validator Not Detecting Fabricated Properties

**Symptoms:** Validator accepts sdlc_stage or context_isolation as valid
**Resolution:** Validator needs update to explicitly flag these non-existent properties
**Test Command:** Specifically test against agents known to have these properties

### Low Scoring Accuracy

**Symptoms:** AI-generated agents score <80 or manual agents score >70 consistently
**Resolution:** Validator scoring algorithm needs calibration
**Test Command:** Run validation against both fullstack-performance-optimizer (should score high) and requirements-analyst (should score medium)

### Missing Blueprint References

**Symptoms:** Validator doesn't reference AI-generated patterns in recommendations
**Resolution:** Validator needs explicit blueprint template integration
**Test Command:** Check if recommendations include references to AI-generated structural patterns

## Post-Test Assessment

After completing all test cases, evaluate overall validator effectiveness:

**Validation Report Quality:**

- Does the validator consistently provide actionable, specific recommendations?
- Are numerical scores accurate and justified?
- Does it correctly identify AI-generated vs manual pattern differences?

**Blueprint System Integration:**

- Does the validator reference AI-generated blueprint standards?
- Are recommendations aligned with discovered patterns?
- Does it flag fabricated properties with 100% accuracy?

**Production Readiness:**

- Can the validator be used immediately for real subagent validation?
- Are the recommendations implementable and clear?
- Does it maintain consistency across different subagent types?

## Success Criteria Summary

The claude-agent-validator passes testing if it achieves:

1. **>90% accuracy** in structural compliance assessment
2. **100% detection rate** for fabricated properties
3. **>85% accuracy** in assessment instruction evaluation
4. **Consistent scoring** aligned with AI-generated vs manual pattern quality
5. **Actionable recommendations** with specific improvement guidance
6. **Blueprint integration** with explicit references to AI-generated standards

This testing framework ensures the validator meets production quality standards for systematic subagent validation using proven AI-generated blueprint patterns.

Subagents Already validated

- system-architect
