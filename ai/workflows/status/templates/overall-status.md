# Overall Status Template

## AI Instructions
Use this template to generate Option 1: Overall Status reports.

## Data Sources
- Primary: `cache_summary` from knowledge-status-cache.yaml
- Secondary: `completion_metrics` from knowledge-status-cache.yaml

## Report Structure

### Header
```
📊 AI Knowledge Base - Overall Status Report
Generated: [current_timestamp]
```

### Summary Section
```
🎯 **Health Status**: [cache_summary.knowledge_base_health]
📈 **Overall Progress**: [cache_summary.completion_rate]
📚 **Total Documents**: [cache_summary.total_documents]
🔄 **Current Phase**: [cache_summary.status]
```

### Key Metrics
```
## 📊 Progress Breakdown

**By Completion Status:**
- ✅ Completed: [count_completed] documents
- ⏳ In Progress: [count_in_progress] documents  
- ❌ Missing: [count_missing] documents

**By Priority Tier:**
- 🔴 Tier 1 (Critical): [tier1_completion_rate]
- 🟡 Tier 2 (Important): [tier2_completion_rate]
- 🟢 Tier 3 (Standard): [tier3_completion_rate]
- ⚪ Tier 4 (Optional): [tier4_completion_rate]
```

### Recent Activity
```
## 📅 Recent Progress

**Last Document Created**: [cache_summary.last_document_created]
**Last Updated**: [cache_summary.last_updated]
**Recent Milestones**: [list_recent_completions]
```

### Health Indicators
```
## 🏥 Knowledge Base Health

**Overall Health**: [health_status_with_emoji]
**Completion Velocity**: [documents_per_week]
**Dependency Status**: [dependency_health]
**Next Milestone**: [next_milestone_name]
```

### Priority Actions
```
## 🎯 Priority Actions

**Immediate Next Step**: [cache_summary.next_priority_action]
**Recommended Focus**: [current_focus_area]
**Estimated Completion**: [estimated_completion_timeline]
```

## Data Mapping Instructions

### Health Status Mapping
```yaml
health_status_mapping:
  empty: "🔴 Empty - Bootstrap needed"
  critical: "🔴 Critical - Immediate attention required"
  needs_attention: "🟡 Needs Attention - Several gaps exist"
  healthy: "🟢 Healthy - Good progress"
  excellent: "🟢 Excellent - Nearly complete"
```

### Completion Rate Visualization
```yaml
completion_visualization:
  0-20: "▱▱▱▱▱ (Starting)"
  21-40: "▰▱▱▱▱ (Early Progress)"
  41-60: "▰▰▱▱▱ (Developing)"
  61-80: "▰▰▰▱▱ (Maturing)"
  81-100: "▰▰▰▰▰ (Excellent)"
```

### Trend Analysis
```yaml
trend_indicators:
  improving: "📈 Trending Up"
  stable: "📊 Stable Progress"
  declining: "📉 Needs Attention"
  stagnant: "⏸️ Stagnant"
```

## Response Formatting
- Use emojis for visual clarity
- Include specific numbers and percentages
- Provide actionable next steps
- Keep total length under 500 words
- End with clear command suggestions

## Success Criteria
- ✅ User understands overall health at a glance
- ✅ Key metrics clearly communicated
- ✅ Next actions are obvious
- ✅ Progress trends are visible