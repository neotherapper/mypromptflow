# Task Management Protocols

Apply comprehensive task completion procedures ensuring consistent tracking, documentation, and quality validation across all AI agent operations.

## Core Task Completion Protocol

Execute this 6-step protocol within ≤180 seconds for ALL completed tasks:

### Step 1: TodoWrite Status Update (≤15s)
Mark completed tasks as "completed" status in TodoWrite tool with:
- Completion timestamp (YYYY-MM-DD HH:MM format)
- Quality score summary (if applicable)
- Duration metrics (actual vs. estimated time)

### Step 2: Project Task List Synchronization (≤60s)
**Required Action**: Locate and update ALL relevant `projects/*/docs/task-list.md` files:
- Change task status from `[ ]` to `[x]` 
- Add completion timestamp and quality score
- Required format: `- [x] **Task Name** (Completed: YYYY-MM-DD HH:MM, Quality: X.X/5.0, Duration: XXXs)`
- Verify 100% synchronization between TodoWrite and project task lists

### Step 3: Progress Documentation (≤60s)
Update relevant `projects/*/docs/progress.md` files with:
- **Quality Metrics**: Accuracy, completeness, consistency scores
- **Key Findings**: 3-5 specific, actionable discoveries
- **Implementation Impact**: How completion affects existing project work
- **Next Action Recommendations**: Priority-ranked with effort estimates

### Step 4: Follow-Up Task Creation (≤30s)
Add newly discovered tasks to:
- TodoWrite tool with priority levels (High/Medium/Low) and effort estimates
- Relevant project task-list.md files with success criteria
- Include dependencies, prerequisites, and measurable completion criteria

### Step 5: Cross-Reference Validation (≤10s)
Verify all @file_path references remain accessible and accurate:
- Test referenced file paths exist and contain expected content
- Update any broken or outdated cross-references
- Ensure 100% cross-reference accessibility

### Step 6: Completion Criteria Verification (≤5s)
Confirm completion meets success criteria defined in task description:
- All deliverables produced and validated
- Quality thresholds achieved (accuracy ≥95%, completeness ≥90%)
- No blocking issues or unresolved dependencies

## Task Creation Standards

### Required Task Format
```markdown
- [ ] **Specific Task Description** (Priority: High/Medium/Low, Effort: Xh, Dependencies: [list])
  - **Success Criteria**: Measurable completion definition
  - **Quality Thresholds**: Specific accuracy/completeness requirements
  - **Deliverables**: Expected outputs and formats
  - **Validation**: How completion will be verified
```

### Priority Classification
- **High Priority**: Critical path, blocking other tasks (≤24h response time)
- **Medium Priority**: Important but not blocking (≤72h response time)  
- **Low Priority**: Enhancement or optimization (≤168h response time)

### Effort Estimation Formula
```
estimated_hours = (complexity_score × 1.5) + (dependency_count × 0.5)
```

## Quality Assurance Integration

### Task Quality Validation
Execute quality checks before marking tasks complete:
- **Deliverables Review**: All expected outputs produced
- **Accuracy Verification**: ≥95% accuracy against requirements
- **Completeness Check**: ≥90% of scope requirements met
- **Consistency Validation**: Consistent with project standards

### Cross-Project Synchronization
Maintain consistency across multiple project task lists:
- **Master Tracker**: TodoWrite tool serves as authoritative source
- **Project Integration**: Mirror status across all relevant project task-list.md files
- **Dependency Mapping**: Track inter-project task dependencies
- **Timeline Coordination**: Coordinate timeline conflicts across projects

## Enforcement and Error Recovery

### Compliance Monitoring
- **Execution Time Tracking**: Monitor protocol completion within 180s target
- **Step Completion Verification**: Ensure all 6 steps executed
- **Quality Gate Validation**: Confirm quality thresholds met
- **Cross-Reference Integrity**: Maintain 100% reference accuracy

### Automatic Escalation Triggers
- **Protocol Violation**: Missing any of the 6 required steps
- **Quality Failure**: Below minimum quality thresholds
- **Timeline Breach**: Protocol completion exceeds 180s
- **Synchronization Failure**: Inconsistencies between TodoWrite and project lists

### Recovery Procedures
When task completion protocol failures detected:
1. **Immediate Halt**: Stop current work and address protocol failure
2. **Gap Analysis**: Identify which steps were missed or incomplete
3. **Corrective Action**: Execute missing steps with full documentation
4. **Validation**: Verify protocol compliance before continuing
5. **Prevention**: Update procedures to prevent similar failures

## Integration with Research Framework

### Research Task Special Requirements
When completing research tasks:
- **Registry Analysis**: Include similarity analysis against existing research
- **Quality Scoring**: Use research framework quality metrics
- **File Structure**: Ensure research/findings/[topic]/ structure compliance
- **Summary Generation**: Create human-friendly summaries for ai-help.md integration

### Research Completion Protocol
Additional steps for research tasks:
7. **Research Registry Update**: Add entry to research/findings/research-registry.yaml
8. **Summary Generation**: Create summary.yaml using research-summary-template.yaml
9. **Browser Integration**: Update research-browser.yaml for ai-help.md access
10. **Cross-Reference Mapping**: Identify and document related research connections

**ENFORCEMENT**: Task completion without full protocol execution triggers automatic escalation and performance penalty. Protocol compliance is mandatory for all AI agents working on this project.