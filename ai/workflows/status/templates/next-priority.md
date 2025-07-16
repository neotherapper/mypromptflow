# Next Priority Template

## AI Instructions
Use this template to generate Option 6: Next Priority reports.

## Data Sources
- Primary: `cache_summary.next_priority_action` from knowledge-status-cache.yaml
- Secondary: `dependency_analysis` and `completion_metrics` for analysis

## Report Structure

### Header
```
🎯 Next Priority Action Report
Analysis Date: [current_timestamp]
```

### Top Priority Recommendation
```
## 🎯 **TOP PRIORITY**

### Create: [priority_document_name]

**Why This Document?**
[priority_reasoning]

**Impact:**
- Will unblock: [count_unblocked] documents
- Affects tiers: [affected_tiers]
- Critical path: [is_critical_path]

**Effort:** [estimated_effort]
**Command:** `/create-document [priority_document_name]`
```

### Detailed Analysis
```
## 🔍 Priority Analysis

**Selection Criteria:**
- Impact Score: [impact_score]/100
- Effort Required: [effort_rating]
- Dependencies: [dependency_status]
- Urgency: [urgency_level]
- Strategic Value: [strategic_value]

**Comparison with Alternatives:**
[for each alternative considered:]
- **[alternative_name]**: [comparison_reason]
  - Impact: [alternative_impact]
  - Effort: [alternative_effort]
  - Why not chosen: [rejection_reason]
```

### Expected Outcomes
```
## 🌟 Expected Outcomes

**Immediate Benefits:**
- [immediate_benefit_1]
- [immediate_benefit_2]
- [immediate_benefit_3]

**Documents This Will Unblock:**
[for each unblocked document:]
- **[document_name]** ([tier])
  - Why unblocked: [unblock_reason]
  - Next in sequence: [next_in_sequence]

**Workflow Improvements:**
- [workflow_improvement_1]
- [workflow_improvement_2]
- [workflow_improvement_3]
```

### Implementation Strategy
```
## 🚀 Implementation Strategy

**Preparation (5 minutes):**
1. Review [reference_document_1]
2. Gather [required_information]
3. Set up [required_tools]

**Execution (Estimated: [execution_time]):**
1. **Phase 1** ([phase1_time]): [phase1_description]
2. **Phase 2** ([phase2_time]): [phase2_description]
3. **Phase 3** ([phase3_time]): [phase3_description]

**Completion Criteria:**
- ✅ [completion_criteria_1]
- ✅ [completion_criteria_2]
- ✅ [completion_criteria_3]
```

### Success Metrics
```
## 📊 Success Metrics

**Quality Targets:**
- Completeness: [completeness_target]%
- Accuracy: [accuracy_target]%
- Usefulness: [usefulness_target]%

**Progress Indicators:**
- Document structure complete
- Content sections filled
- Dependencies satisfied
- Quality review passed

**Next Steps After Completion:**
1. Update cache: `/update-knowledge-cache`
2. Check status: `/knowledge-status`
3. Create next document: `[next_document_command]`
```

### Alternative Paths
```
## 🔀 Alternative Paths (If Blocked)

**If [priority_document_name] is blocked:**

**Option A:** [alternative_a_name]
- Why: [alternative_a_reason]
- Impact: [alternative_a_impact]
- Command: `/create-document [alternative_a_name]`

**Option B:** [alternative_b_name]
- Why: [alternative_b_reason]
- Impact: [alternative_b_impact]
- Command: `/create-document [alternative_b_name]`

**Option C:** [alternative_c_name]
- Why: [alternative_c_reason]
- Impact: [alternative_c_impact]
- Command: `/create-document [alternative_c_name]`
```

### Time-Based Recommendations
```
## ⏰ Time-Based Recommendations

**If you have 30 minutes:**
- Start with [quick_section] section
- Complete [completable_part]
- Make progress on [progress_opportunity]

**If you have 2 hours:**
- Complete full document
- Review and refine
- Plan next document

**If you have 4+ hours:**
- Complete [priority_document_name]
- Start [next_document_name]
- Update all dependencies
```

### Context and Background
```
## 📚 Context and Background

**Why This Matters:**
[context_explanation]

**Business Impact:**
[business_impact_description]

**Technical Impact:**
[technical_impact_description]

**User Impact:**
[user_impact_description]
```

### Dependencies and Prerequisites
```
## 🔗 Dependencies and Prerequisites

**Required Information:**
[for each required info:]
- [info_item]: [source_location]

**Recommended Reading:**
[for each recommended document:]
- [document_name]: [reading_reason]

**Tools Needed:**
[for each tool:]
- [tool_name]: [tool_purpose]
```

### Risk Mitigation
```
## ⚠️ Risk Mitigation

**Potential Issues:**
[for each potential issue:]
- **Risk:** [risk_description]
- **Mitigation:** [mitigation_strategy]
- **Contingency:** [contingency_plan]

**Quality Assurance:**
- Review checklist available
- Validation criteria defined
- Feedback mechanism ready
```

### Motivation and Encouragement
```
## 💪 Motivation

**Progress Impact:**
Creating [priority_document_name] will bring your knowledge base to [new_completion_percentage]% completion!

**Milestone Achievement:**
This completes [milestone_name] milestone and unlocks [unlocked_opportunities].

**Team Benefit:**
[team_benefit_description]
```

## Data Processing Instructions

### Priority Scoring Algorithm
```yaml
priority_calculation:
  impact_weight: 40
  effort_weight: 30
  dependency_weight: 20
  strategic_weight: 10
```

### Impact Assessment
```yaml
impact_factors:
  documents_unblocked: "High weight"
  tier_affected: "Medium weight"
  workflow_enabled: "Medium weight"
  strategic_value: "Low weight"
```

### Effort Estimation
```yaml
effort_categories:
  quick: "< 2 hours"
  medium: "2-8 hours"
  large: "8+ hours"
```

## Response Guidelines
- Be decisive and clear
- Provide concrete next steps
- Show impact and value
- Include alternatives for flexibility
- Motivate action

## Success Criteria
- ✅ Single clear next action identified
- ✅ Compelling reasoning provided
- ✅ Implementation path clear
- ✅ Alternatives available if needed
- ✅ User motivated to take action