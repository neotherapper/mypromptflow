# Ready to Create Documents Template

## AI Instructions
Use this template to generate Option 4: Ready to Create reports.

## Data Sources
- Primary: `dependency_analysis` from knowledge-status-cache.yaml
- Secondary: `dependencies.yaml` for dependency validation

## Report Structure

### Header
```
🚀 Ready to Create Documents Report
Analysis Date: [current_timestamp]
```

### Summary
```
🎯 **Ready to Create Summary**
Documents Ready: [count_ready] documents
Immediate Opportunities: [count_immediate]
Quick Wins Available: [count_quick_wins]
```

### Immediate Opportunities (No Dependencies)
```
## ⚡ Immediate Opportunities

[for each document with no dependencies:]
- 🚀 **[document_name]** ([tier])
  - Type: [document_type]
  - Estimated Effort: [estimated_effort]
  - Impact: [impact_description]
  - Command: `/create-document [document_name]`
  - Why Ready: No dependencies required
```

### Dependencies Satisfied
```
## ✅ Dependencies Satisfied

[for each document with satisfied dependencies:]
- 🚀 **[document_name]** ([tier])
  - Type: [document_type]
  - Estimated Effort: [estimated_effort]
  - Impact: [impact_description]
  - Command: `/create-document [document_name]`
  - Dependencies: [list_satisfied_dependencies]
  - Why Ready: All dependencies complete
```

### Quick Wins (< 2 hours)
```
## ⚡ Quick Wins (< 2 hours)

[for each quick win document:]
- 🏃 **[document_name]** ([tier])
  - Estimated Time: [estimated_time]
  - Impact: [impact_description]
  - Command: `/create-document [document_name]`
  - Quick Win Factor: [quick_win_reason]
```

### High Impact Ready
```
## 💪 High Impact Ready

[for each high impact ready document:]
- 🎯 **[document_name]** ([tier])
  - Impact: [impact_description]
  - Will Unblock: [count_unblocked] documents
  - Creates Path To: [unlocked_opportunities]
  - Command: `/create-document [document_name]`
```

### Prioritized Creation Order
```
## 📊 Recommended Creation Order

**Priority 1 (Create First)**:
1. **[priority_1_document]** - [priority_reason]
   - Impact: [impact_description]
   - Command: `/create-document [document_name]`

**Priority 2 (Create Next)**:
2. **[priority_2_document]** - [priority_reason]
   - Impact: [impact_description]
   - Command: `/create-document [document_name]`

**Priority 3 (Create After)**:
3. **[priority_3_document]** - [priority_reason]
   - Impact: [impact_description]
   - Command: `/create-document [document_name]`
```

### Parallel Creation Opportunities
```
## 🔄 Parallel Creation Opportunities

**Can Create Simultaneously**:
Group A:
- [document_1] and [document_2] - No shared dependencies
- [document_3] and [document_4] - Independent workflows

Group B:
- [document_5] and [document_6] - Different team members
- [document_7] and [document_8] - Different skill sets
```

### Effort Distribution
```
## ⏱️ Effort Distribution

**Today (< 2 hours total)**:
- [quick_document_1] (30 min)
- [quick_document_2] (1 hour)
- [quick_document_3] (30 min)

**This Week (2-8 hours each)**:
- [medium_document_1] (4 hours)
- [medium_document_2] (6 hours)

**Next Week (> 8 hours)**:
- [large_document_1] (12 hours)
- [large_document_2] (16 hours)
```

### Template Prefill Available
```
## 📝 Template Prefill Available

[for each document with prefill data:]
- 🎯 **[document_name]**
  - Templates will be pre-filled with:
    - [prefill_data_1]
    - [prefill_data_2]
    - [prefill_data_3]
  - Command: `/create-document [document_name]`
```

### Workflow Suggestions
```
## 🔧 Workflow Suggestions

**Batch Creation**:
- Create all [document_type] documents together
- Focus on [tier_level] tier completion
- Complete [workflow_name] workflow

**Orchestrated Creation**:
- Use `/orchestrate-agents [workflow_type]` for:
  - [orchestration_opportunity_1]
  - [orchestration_opportunity_2]

**Team Distribution**:
- [team_member_1]: [assigned_documents]
- [team_member_2]: [assigned_documents]
```

### Next Steps
```
## 🎯 Recommended Next Steps

**Immediate Action** (Next 15 minutes):
1. Run: `/create-document [top_priority_document]`
2. Reason: [immediate_action_reason]

**Short Term** (Today):
1. Complete [short_term_target_1]
2. Start [short_term_target_2]
3. Gather materials for [short_term_target_3]

**Medium Term** (This Week):
1. Focus on [medium_term_focus]
2. Complete [medium_term_target_count] documents
3. Unblock [blocked_document_name]
```

## Data Processing Instructions

### Readiness Validation
```yaml
readiness_criteria:
  all_dependencies_satisfied: "Check against document-registry.yaml"
  no_blocking_issues: "Verify no technical blockers"
  template_available: "Confirm template exists"
  effort_estimated: "Effort assessment complete"
```

### Priority Scoring
```yaml
priority_factors:
  impact_score: "Weight: 40%"
  effort_required: "Weight: 30%"
  dependency_unlock: "Weight: 20%"
  quick_win_factor: "Weight: 10%"
```

### Effort Categories
```yaml
effort_categories:
  quick_win: "< 2 hours"
  medium: "2-8 hours"
  large: "8+ hours"
```

## Sorting Instructions
- Sort by priority score (highest first)
- Group by effort level for planning
- Highlight immediate opportunities
- Show parallel creation options

## Response Guidelines
- Focus on action and momentum
- Provide specific commands
- Show multiple options
- Encourage immediate action
- Highlight quick wins

## Success Criteria
- ✅ Clear immediate next actions
- ✅ Multiple ready options shown
- ✅ Effort estimates for planning
- ✅ Commands ready to execute
- ✅ User motivated to start creating