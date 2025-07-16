# Completed Documents Template

## AI Instructions
Use this template to generate Option 2: Completed Documents reports.

## Data Sources
- Primary: `documents` from document-registry.yaml
- Secondary: `completion_metrics` from knowledge-status-cache.yaml

## Report Structure

### Header
```
✅ Completed Documents Report
Last Updated: [registry.last_updated]
```

### Summary
```
📊 **Completion Summary**
Total Completed: [count_completed] of [total_documents] documents
Completion Rate: [completion_percentage]%
```

### Documents by Tier
```
## 📋 Completed Documents by Tier

### 🔴 Tier 1 (Critical/Technical)
[for each tier1 completed document:]
- ✅ **[document_name]** 
  - Status: [completion_status]
  - Created: [creation_date]
  - Last Updated: [last_updated]
  - Quality Score: [quality_score]

### 🟡 Tier 2 (Important/Product)
[for each tier2 completed document:]
- ✅ **[document_name]**
  - Status: [completion_status]
  - Created: [creation_date]
  - Last Updated: [last_updated]
  - Quality Score: [quality_score]

### 🟢 Tier 3 (Standard/Feature)
[for each tier3 completed document:]
- ✅ **[document_name]**
  - Status: [completion_status]
  - Created: [creation_date]
  - Last Updated: [last_updated]
  - Quality Score: [quality_score]

### ⚪ Tier 4 (Optional/Strategic)
[for each tier4 completed document:]
- ✅ **[document_name]**
  - Status: [completion_status]
  - Created: [creation_date]
  - Last Updated: [last_updated]
  - Quality Score: [quality_score]
```

### Recent Completions
```
## 🆕 Recently Completed (Last 7 Days)

[for each recent completion:]
- ✅ **[document_name]** ([tier])
  - Completed: [completion_date]
  - Impact: [impact_description]
  - Unlocked: [unlocked_dependencies]
```

### Quality Analysis
```
## 📊 Quality Metrics

**Average Quality Score**: [average_quality_score]/100
**High Quality Documents**: [count_high_quality] ([percentage]%)
**Documents Needing Review**: [count_needs_review]

**Quality Distribution:**
- 90-100: [count_excellent] documents
- 80-89: [count_good] documents  
- 70-79: [count_acceptable] documents
- <70: [count_needs_improvement] documents
```

### Document Types Analysis
```
## 📝 Completed by Document Type

**Foundational**: [count_foundational] completed
**Research**: [count_research] completed
**Technical**: [count_technical] completed
**Planning**: [count_planning] completed
**Quality**: [count_quality] completed
```

### Impact Assessment
```
## 💪 Impact Assessment

**High Impact Completions**:
[for each high impact document:]
- **[document_name]**: [impact_description]

**Dependency Chain Progress**:
- Documents that unblocked others: [count_unblocking]
- Critical path completions: [count_critical_path]
```

## Data Processing Instructions

### Status Mapping
```yaml
status_mapping:
  completed: "✅ Complete"
  in_progress: "⏳ In Progress"
  needs_review: "🔍 Needs Review"
  needs_update: "🔄 Needs Update"
```

### Quality Score Interpretation
```yaml
quality_ranges:
  excellent: "90-100 (🌟 Excellent)"
  good: "80-89 (👍 Good)"
  acceptable: "70-79 (✅ Acceptable)"
  needs_improvement: "<70 (⚠️ Needs Improvement)"
```

### Tier Color Coding
```yaml
tier_colors:
  tier1: "🔴"
  tier2: "🟡"
  tier3: "🟢"
  tier4: "⚪"
```

## Sorting Instructions
- Sort by completion date (newest first) within each tier
- Prioritize high-impact documents in summaries
- Group by document type for analysis sections

## Response Guidelines
- Celebrate completed work
- Highlight quality achievements
- Show progress momentum
- Identify maintenance needs
- Keep individual entries concise

## Success Criteria
- ✅ Clear visibility of all completed work
- ✅ Quality assessment provided
- ✅ Recent progress highlighted
- ✅ Maintenance needs identified
- ✅ User feels motivated by progress shown