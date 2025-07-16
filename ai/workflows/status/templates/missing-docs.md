# Missing Documents Template

## AI Instructions
Use this template to generate Option 3: Missing Documents reports.

## Data Sources
- Primary: Compare `dependencies.yaml` with `document-registry.yaml`
- Secondary: `completion_metrics` from knowledge-status-cache.yaml

## Report Structure

### Header
```
❌ Missing Documents Report
Analysis Date: [current_timestamp]
```

### Summary
```
📊 **Missing Documents Summary**
Total Missing: [count_missing] documents
Percentage Missing: [missing_percentage]%
Critical Missing: [count_critical_missing]
```

### Critical Missing (Tier 1)
```
## 🔴 Critical Missing Documents (Tier 1)

[for each tier1 missing document:]
- ❌ **[document_name]**
  - Type: [document_type]
  - Impact: [impact_description]
  - Blocking: [count_blocked_documents] documents
  - Estimated Effort: [estimated_effort]
  - Dependencies: [dependency_status]
```

### Important Missing (Tier 2)
```
## 🟡 Important Missing Documents (Tier 2)

[for each tier2 missing document:]
- ❌ **[document_name]**
  - Type: [document_type]
  - Impact: [impact_description]
  - Blocking: [count_blocked_documents] documents
  - Estimated Effort: [estimated_effort]
  - Dependencies: [dependency_status]
```

### Standard Missing (Tier 3)
```
## 🟢 Standard Missing Documents (Tier 3)

[for each tier3 missing document:]
- ❌ **[document_name]**
  - Type: [document_type]
  - Impact: [impact_description]
  - Blocking: [count_blocked_documents] documents
  - Estimated Effort: [estimated_effort]
  - Dependencies: [dependency_status]
```

### Optional Missing (Tier 4)
```
## ⚪ Optional Missing Documents (Tier 4)

[for each tier4 missing document:]
- ❌ **[document_name]**
  - Type: [document_type]
  - Impact: [impact_description]
  - Blocking: [count_blocked_documents] documents
  - Estimated Effort: [estimated_effort]
  - Dependencies: [dependency_status]
```

### Impact Analysis
```
## 💥 Impact Analysis

**High Impact Missing**:
[for each high impact missing document:]
- **[document_name]**: Blocking [count_blocked] documents
  - Critical path: [is_critical_path]
  - Affects tiers: [affected_tiers]

**Bottleneck Documents**:
[for each bottleneck document:]
- **[document_name]**: [bottleneck_description]
```

### Dependency Status
```
## 🔗 Dependency Status for Missing Documents

**Ready to Create** (Dependencies satisfied):
[for each ready document:]
- 🚀 **[document_name]** - Ready now
  - Command: `/create-document [document_name]`

**Blocked** (Dependencies not satisfied):
[for each blocked document:]
- 🔒 **[document_name]** - Waiting for:
  - [dependency_1]
  - [dependency_2]
```

### Prioritization Matrix
```
## 📊 Priority Matrix

**High Priority (Create First)**:
1. [highest_priority_document] - [priority_reason]
2. [second_priority_document] - [priority_reason]
3. [third_priority_document] - [priority_reason]

**Medium Priority (Create After Dependencies)**:
[list of medium priority documents]

**Low Priority (Create When Ready)**:
[list of low priority documents]
```

### Effort Estimation
```
## ⏱️ Effort Estimation

**Quick Wins** (< 2 hours):
[for each quick win document:]
- **[document_name]**: [estimated_time]

**Medium Effort** (2-8 hours):
[for each medium effort document:]
- **[document_name]**: [estimated_time]

**Large Effort** (> 8 hours):
[for each large effort document:]
- **[document_name]**: [estimated_time]
```

### Recommended Actions
```
## 🎯 Recommended Actions

**Immediate Actions**:
1. Create [top_priority_document] - `/create-document [name]`
2. Gather requirements for [second_priority_document]
3. Plan [third_priority_document] dependencies

**This Week**:
- Focus on [weekly_focus_area]
- Complete [weekly_target_count] documents
- Unblock [blocked_document_name]

**This Month**:
- Achieve [monthly_completion_target]% completion
- Complete all Tier 1 documents
- Begin Tier 2 document creation
```

## Data Processing Instructions

### Priority Calculation
```yaml
priority_factors:
  blocking_count: "Weight: 40%"
  tier_level: "Weight: 30%"
  effort_required: "Weight: 20%"
  dependency_satisfaction: "Weight: 10%"
```

### Impact Assessment
```yaml
impact_levels:
  critical: "Blocks multiple high-priority documents"
  high: "Blocks important workflow"
  medium: "Affects specific features"
  low: "Nice to have"
```

### Dependency Status
```yaml
dependency_status:
  satisfied: "🚀 Ready to create"
  partial: "⏳ Some dependencies missing"
  blocked: "🔒 Major dependencies missing"
```

## Sorting Instructions
- Sort by priority score (highest first)
- Group by tier within priority levels
- Emphasize ready-to-create documents
- Show effort estimates for planning

## Response Guidelines
- Be solution-focused, not just problem-focused
- Provide clear next steps
- Highlight quick wins
- Show progress path
- Motivate with achievable goals

## Success Criteria
- ✅ Clear picture of what's missing
- ✅ Priorities are obvious
- ✅ Next actions are actionable
- ✅ Effort estimates help planning
- ✅ User knows where to start