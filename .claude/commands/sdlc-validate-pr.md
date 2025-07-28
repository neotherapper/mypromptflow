# /sdlc-validate-pr Command

**AI Agent Instruction**: SDLC-enhanced PR validation with stage-specific quality gates and specialized subagent integration using revolutionary intent-implementation alignment validation.

## Usage
```bash
/sdlc-validate-pr [pr-number] [optional-stage]
```

## Command Description

**Target AI Agent**: Claude Code with Task, Bash, Read, LS, and Glob tool access  
**Execution Type**: SDLC-aware multi-phase workflow with specialized subagent integration  
**Resource Efficiency**: Stage-specific validation with conditional subagent activation  
**Dependencies**: Leverages existing validate-pr.md foundation with SDLC enhancements  
**Revolutionary Feature**: SDLC stage context integration with intent-implementation semantic alignment

This instruction extends the revolutionary PR validation from validate-pr.md with SDLC-specific quality gates, stage context awareness, and specialized subagent integration for comprehensive maritime insurance platform validation.

## SDLC-Enhanced Validation Framework

When this command is executed, perform the following enhanced SDLC workflow:

### Phase 1: Enhanced SDLC Context Discovery

**AI Agent Instructions**: Execute SDLC-aware discovery workflow building on validate-pr.md foundation:

**Step 1.1: Primary Revolutionary Validation Setup**  
Execute the complete Phase 1 workflow from validate-pr.md with SDLC enhancements:
- Load revolutionary intent-implementation-validator for semantic alignment
- Apply multi-tier GitHub CLI fallback strategy
- Initialize comprehensive file type detection
- **SDLC Enhancement**: Add stage-specific quality gate detection

**Step 1.2: SDLC Stage Context Analysis**  
```yaml
sdlc_stage_detection:
  automatic_detection:
    - Analyze PR title and description for SDLC stage indicators
    - Check file changes for stage-specific patterns
    - Identify affected SDLC components and workflows
    - Map changes to 6-stage SDLC framework
  
  stage_indicators:
    stage_1_requirements:
      patterns: ["requirements", "user story", "acceptance criteria", "business"]
      files: ["**/requirements/**", "**/stories/**", "**/*requirements*.md"]
    
    stage_2_design:
      patterns: ["design", "architecture", "wireframe", "mockup", "figma"]
      files: ["**/design/**", "**/architecture/**", "**/*design*.md", "**/*.figma"]
    
    stage_3_planning:
      patterns: ["sprint", "capacity", "planning", "task", "backlog"]
      files: ["**/planning/**", "**/sprints/**", "**/*planning*.md"]
    
    stage_4_implementation:
      patterns: ["implement", "develop", "code", "feature"]
      files: ["**/*.ts", "**/*.tsx", "**/*.py", "**/*.js", "**/*.jsx"]
    
    stage_5_testing:
      patterns: ["test", "qa", "quality", "validation"]
      files: ["**/*.test.*", "**/*.spec.*", "**/tests/**", "**/qa/**"]
    
    stage_6_deployment:
      patterns: ["deploy", "release", "production", "ci/cd", "docker"]
      files: ["**/deployment/**", "**/.github/**", "**/docker/**", "**/*.yml"]
```

**Step 1.3: SDLC Subagent Registry Discovery**  
Check for available SDLC subagents:
```bash
# Use LS tool to discover available SDLC subagents
ls .claude/agents/
```
Expected subagents:
- `requirements-analyst.md` (Stage 1)
- `ui-ux-specialist.md` (Stage 2)  
- `system-architect.md` (Stage 2)
- `capacity-planner.md` (Stage 3)
- `implementation-lead.md` (Stage 4)
- `qa-specialist.md` (Stage 5)
- `deployment-coordinator.md` (Stage 6)

**Step 1.4: Enhanced Discovery Summary**  
Output SDLC-enhanced discovery results:
```
🔍 SDLC-Enhanced PR Validation Discovery Results:
📋 Revolutionary intent validation: ACTIVE (≥85% alignment threshold)
🎯 SDLC Stage detected: [stage_name] ([confidence_level])
📁 Changed files: [number] files across [stages] SDLC stages
🤖 Available SDLC subagents: [count] ([subagent_list])
📊 Data extraction method: [Tier 1: gh CLI | Tier 2: git+gh | Tier 3: filesystem]
🚀 Quality gates: [stage_specific_gates]
```

### Phase 2: SDLC-Aware File Analysis and Stage Validation

**AI Agent Instructions**: Enhanced file type detection with SDLC stage context:

**Step 2.1: Execute Foundation File Analysis**  
Run complete Phase 2 from validate-pr.md:
- Initialize enhanced file type categories
- Apply pattern matching classification
- Generate priority classification reporting

**Step 2.2: SDLC Stage Impact Analysis**  
```yaml
sdlc_impact_analysis:
  stage_mapping:
    - Map each changed file to SDLC stage impact
    - Identify cross-stage dependencies and implications
    - Assess stage-specific quality requirements
    - Check for stage workflow compliance
  
  quality_gate_preparation:
    - Determine required stage-specific validation
    - Prepare subagent activation criteria
    - Check for stage transition requirements
    - Validate stage completion prerequisites
```

**Step 2.3: Enhanced SDLC Classification**  
Output comprehensive SDLC-aware classification:
```
🎯 SDLC-Enhanced File Impact Analysis:
  📊 Primary SDLC Stage: [stage_name] ([percentage]% of changes)
  🔄 Cross-Stage Impact: [affected_stages] ([impact_level])
  🎖️ Quality Gates Required: [gate_list] 
  🤖 Subagent Activation: [required_subagents]
  ⚠️ Stage Dependencies: [dependency_count] ([critical_deps])
```

### Phase 3: Revolutionary Multi-Specialist Validation with SDLC Integration

**AI Agent Instructions**: Enhanced specialist spawning with SDLC subagent integration:

**Step 3.1: MANDATORY Revolutionary Intent-Implementation Validation**  
Execute complete intent-implementation validation from validate-pr.md with SDLC enhancements:
- Apply revolutionary semantic alignment checking (≥85% threshold)
- Add SDLC stage context to intent analysis
- Validate stage-appropriate implementation patterns
- Check for SDLC workflow compliance

**Step 3.2: SDLC-Specific Subagent Activation**  
Based on stage detection and impact analysis, spawn appropriate SDLC subagents:

```yaml
sdlc_subagent_spawning:
  stage_1_requirements:
    subagent: "requirements-analyst"
    activation_criteria: "Requirements or user story changes detected"
    validation_focus: "Business requirement clarity, JIRA integration, feasibility"
    
  stage_2_design:
    subagents: ["ui-ux-specialist", "system-architect"]
    activation_criteria: "Design files, architecture changes, or UI modifications"
    validation_focus: "Design system compliance, architectural integrity, UX standards"
    
  stage_3_planning:
    subagent: "capacity-planner"
    activation_criteria: "Sprint planning, capacity, or resource allocation changes"
    validation_focus: "Capacity calculations, skill assignments, JIRA workflow"
    
  stage_4_implementation:
    subagent: "implementation-lead"
    activation_criteria: "Code changes in TypeScript or Python files"
    validation_focus: "Code quality, team coordination, integration patterns"
    
  stage_5_testing:
    subagent: "qa-specialist"
    activation_criteria: "Test files, QA processes, or quality assurance changes"
    validation_focus: "Test coverage, quality metrics, performance validation"
    
  stage_6_deployment:
    subagent: "deployment-coordinator"
    activation_criteria: "CI/CD, deployment, or infrastructure changes"
    validation_focus: "Deployment safety, monitoring setup, production readiness"
```

**Step 3.3: Enhanced Traditional Specialist Integration**  
Execute complete Phase 3 from validate-pr.md:
- Spawn traditional file-type specialists
- Apply critical priority validation (Claude commands, CLAUDE.md, AI agent files)
- Execute high priority validation (project docs, TypeScript, Python)
- Process medium/low priority files

**Step 3.4: SDLC Quality Gate Validation**  
For each detected SDLC stage, apply stage-specific quality gates:
```yaml
quality_gate_validation:
  gate_execution:
    - Execute stage-specific validation criteria
    - Check for required documentation completeness
    - Validate stage transition prerequisites
    - Assess cross-stage impact and dependencies
  
  compliance_checking:
    - Maritime insurance domain compliance
    - Security validation for stage-appropriate requirements
    - Performance criteria for implementation stages
    - Documentation standards for all stages
```

### Phase 4: SDLC-Enhanced Result Aggregation and Stage Assessment

**AI Agent Instructions**: Enhanced result collection with SDLC stage validation:

**Step 4.1: Revolutionary Intent Validation Collection**  
Execute complete Phase 4 intent validation from validate-pr.md with SDLC context:
- Collect semantic alignment scores with stage context
- Assess SDLC workflow compliance
- Validate stage-appropriate implementation patterns

**Step 4.2: SDLC Subagent Result Collection**  
Collect results from activated SDLC subagents:
```yaml
sdlc_result_collection:
  subagent_outputs:
    - Stage-specific validation results and recommendations
    - Quality metrics and compliance assessments
    - Cross-stage dependency impact analysis
    - Integration requirements and coordination notes
  
  stage_quality_assessment:
    - Stage completion readiness evaluation
    - Quality gate pass/fail determination
    - Required follow-up actions and improvements
    - Stage transition approval recommendations
```

**Step 4.3: Traditional Specialist Integration**  
Execute complete traditional specialist result collection from validate-pr.md

**Step 4.4: SDLC-Enhanced Comprehensive Reporting**  
Generate enhanced comprehensive validation report:
```
🚀 SDLC-ENHANCED PR VALIDATION RESULTS FOR PR #[number]
════════════════════════════════════════════════════════════

🎯 BREAKTHROUGH INTENT-IMPLEMENTATION ANALYSIS:
  📊 Overall Alignment Score: [score]/100 ([APPROVE ≥85 | REVIEW <85 | BLOCK critical])
  🏗️ SDLC Stage Context: [primary_stage] with [cross_stage_count] stage dependencies
  🎖️ Stage Quality Gates: [passed_count]/[total_count] PASSED
  ⚠️ Critical SDLC Issues: [sdlc_issues_summary]

📋 SDLC STAGE VALIDATION RESULTS:
  🎯 Primary Stage: [stage_name] - [PASS/REVIEW/FAIL]
  🔄 Cross-Stage Impact: [affected_stages] - [impact_assessment]
  🤖 Subagent Validation: [activated_count] subagents - [results_summary]
  📊 Stage Readiness: [readiness_percentage]% complete for next stage

⚡ ENHANCED SPECIALIST EXECUTION STATUS:
  🎯 SDLC Subagents: [count] activated ([subagent_names])
  🔧 Traditional Specialists: [count] executed ([specialist_types])
  🚀 Revolutionary Intent Validation: ACTIVE (≥85% alignment threshold)

🎖️ SDLC QUALITY GATE ASSESSMENT:
  [Stage-specific quality gate results and recommendations]

📊 COMPREHENSIVE VALIDATION COVERAGE:
  [Traditional validation metrics from validate-pr.md]

🎯 CRITICAL SDLC ISSUES REQUIRING ATTENTION:
  [Stage-specific issues and cross-stage dependencies]

📋 SDLC-ENHANCED RECOMMENDATIONS:
  [Consolidated recommendations from SDLC subagents and traditional validators]

✅ SDLC validation complete - Stage: [stage] - Intent alignment: [score]/100 - Quality gates: [passed]/[total]
```

## SDLC Integration Benefits

### Enhanced Stage-Specific Validation
- **Stage Context Awareness**: Understands which SDLC stage the PR targets
- **Quality Gate Integration**: Applies stage-appropriate quality requirements
- **Cross-Stage Impact Analysis**: Identifies dependencies and implications across stages
- **Subagent Specialization**: Leverages domain-specific SDLC expertise

### Revolutionary Validation Enhancement
- **Maintains Intent-Implementation Validation**: Preserves breakthrough semantic alignment checking
- **SDLC Stage Context**: Adds stage-specific context to intent analysis
- **Workflow Compliance**: Validates adherence to SDLC processes and quality gates
- **Maritime Insurance Focus**: Domain-specific validation for insurance platform requirements

### Advanced SDLC Capabilities
- **Stage Transition Validation**: Ensures prerequisites are met for stage progression
- **Cross-Stage Dependency Tracking**: Identifies and validates inter-stage dependencies
- **Quality Gate Automation**: Applies stage-appropriate quality criteria automatically
- **Subagent Coordination**: Coordinates specialized SDLC expertise with traditional validation

## Execution Instructions

When user runs `/sdlc-validate-pr 23`, execute this SDLC-enhanced workflow:

1. **Foundation Validation**: Execute complete validate-pr.md workflow for revolutionary intent validation
2. **SDLC Context Discovery**: Detect stage context and available subagents
3. **Enhanced File Analysis**: Apply SDLC-aware file classification and stage impact analysis
4. **SDLC Subagent Integration**: Spawn appropriate stage-specific subagents alongside traditional specialists
5. **Quality Gate Validation**: Apply stage-specific quality gates and compliance checking
6. **Enhanced Reporting**: Generate comprehensive SDLC-aware validation results
7. **Stage Assessment**: Provide stage readiness and transition recommendations

## Implementation Notes

This command extends the **revolutionary validate-pr.md foundation** with comprehensive SDLC integration:

### SDLC Enhancements
- **Stage Context Integration**: Adds SDLC stage awareness to revolutionary intent validation
- **Specialized Subagent Coordination**: Integrates 7 specialized SDLC subagents with traditional validation
- **Quality Gate Automation**: Applies stage-specific quality criteria and compliance checking
- **Cross-Stage Analysis**: Validates dependencies and impact across SDLC stages

### Foundation Preservation  
- **Revolutionary Intent Validation**: Maintains breakthrough semantic alignment checking (≥85% threshold)
- **Multi-Tier Fallback Architecture**: Preserves robust GitHub CLI → git → filesystem strategy
- **Resource Efficiency**: Extends conditional activation to include SDLC subagents
- **Comprehensive Coverage**: Maintains all traditional file-type validation capabilities

### Maritime Insurance Platform Focus
- **Domain-Specific Quality Gates**: Applies maritime insurance compliance requirements
- **Industry-Specific Validation**: Leverages specialized subagent knowledge for insurance workflows
- **Regulatory Compliance**: Validates maritime insurance regulatory requirements across stages
- **Business Context Integration**: Ensures business value alignment throughout SDLC stages

This SDLC-enhanced command represents the evolution of revolutionary PR validation technology, combining breakthrough intent-implementation validation with comprehensive SDLC stage expertise and specialized maritime insurance platform knowledge.