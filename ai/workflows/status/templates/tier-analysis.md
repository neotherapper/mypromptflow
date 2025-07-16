# Tier Analysis Template

## AI Instructions
Use this template to generate Option 8: Tier Analysis reports.

## Data Sources
- Primary: `completion_metrics.by_tier` from knowledge-status-cache.yaml
- Secondary: `tier-configuration.yaml` for tier definitions

## Report Structure

### Header
```
📊 Tier Analysis Report
Analysis Date: [current_timestamp]
```

### Tier Overview
```
🏗️ **Tier Analysis Summary**
Total Completion: [overall_completion_rate]%
Best Performing Tier: [best_tier]
Needs Attention: [attention_tier]
```

### Tier 1 Analysis (Critical/Technical)
```
## 🔴 Tier 1 - Critical/Technical Documents

**Status:** [tier1_completion_rate]% Complete
**Priority:** Critical - Foundation for all other work
**Health:** [tier1_health_status]

**Progress Summary:**
- ✅ Completed: [tier1_completed_count] documents
- ⏳ In Progress: [tier1_in_progress_count] documents
- ❌ Missing: [tier1_missing_count] documents

**Completed Documents:**
[for each tier1 completed document:]
- ✅ **[document_name]**
  - Type: [document_type]
  - Created: [creation_date]
  - Impact: [impact_description]

**Missing Critical Documents:**
[for each tier1 missing document:]
- ❌ **[document_name]**
  - Type: [document_type]
  - Impact: [impact_description]
  - Blocking: [blocking_count] documents
  - Priority: [priority_level]

**Next Priority Actions:**
[for each tier1 next action:]
- 🎯 [action_description]
  - Command: `/create-document [document_name]`
  - Impact: [action_impact]
```

### Tier 2 Analysis (Important/Product)
```
## 🟡 Tier 2 - Important/Product Documents

**Status:** [tier2_completion_rate]% Complete
**Priority:** Important - Core product definition
**Health:** [tier2_health_status]

**Progress Summary:**
- ✅ Completed: [tier2_completed_count] documents
- ⏳ In Progress: [tier2_in_progress_count] documents
- ❌ Missing: [tier2_missing_count] documents

**Completed Documents:**
[for each tier2 completed document:]
- ✅ **[document_name]**
  - Type: [document_type]
  - Created: [creation_date]
  - Impact: [impact_description]

**Missing Important Documents:**
[for each tier2 missing document:]
- ❌ **[document_name]**
  - Type: [document_type]
  - Impact: [impact_description]
  - Dependencies: [dependency_status]
  - Priority: [priority_level]

**Next Priority Actions:**
[for each tier2 next action:]
- 🎯 [action_description]
  - Command: `/create-document [document_name]`
  - Impact: [action_impact]
```

### Tier 3 Analysis (Standard/Feature)
```
## 🟢 Tier 3 - Standard/Feature Documents

**Status:** [tier3_completion_rate]% Complete
**Priority:** Standard - Feature implementation
**Health:** [tier3_health_status]

**Progress Summary:**
- ✅ Completed: [tier3_completed_count] documents
- ⏳ In Progress: [tier3_in_progress_count] documents
- ❌ Missing: [tier3_missing_count] documents

**Completed Documents:**
[for each tier3 completed document:]
- ✅ **[document_name]**
  - Type: [document_type]
  - Created: [creation_date]
  - Impact: [impact_description]

**Missing Standard Documents:**
[for each tier3 missing document:]
- ❌ **[document_name]**
  - Type: [document_type]
  - Impact: [impact_description]
  - Dependencies: [dependency_status]
  - Priority: [priority_level]

**Next Priority Actions:**
[for each tier3 next action:]
- 🎯 [action_description]
  - Command: `/create-document [document_name]`
  - Impact: [action_impact]
```

### Tier 4 Analysis (Optional/Strategic)
```
## ⚪ Tier 4 - Optional/Strategic Documents

**Status:** [tier4_completion_rate]% Complete
**Priority:** Optional - Strategic enhancement
**Health:** [tier4_health_status]

**Progress Summary:**
- ✅ Completed: [tier4_completed_count] documents
- ⏳ In Progress: [tier4_in_progress_count] documents
- ❌ Missing: [tier4_missing_count] documents

**Completed Documents:**
[for each tier4 completed document:]
- ✅ **[document_name]**
  - Type: [document_type]
  - Created: [creation_date]
  - Impact: [impact_description]

**Missing Optional Documents:**
[for each tier4 missing document:]
- ❌ **[document_name]**
  - Type: [document_type]
  - Impact: [impact_description]
  - Dependencies: [dependency_status]
  - Priority: [priority_level]

**Next Priority Actions:**
[for each tier4 next action:]
- 🎯 [action_description]
  - Command: `/create-document [document_name]`
  - Impact: [action_impact]
```

### Cross-Tier Analysis
```
## 🔄 Cross-Tier Analysis

**Tier Balance:**
- Foundation Strong: [foundation_strength_assessment]
- Product Definition: [product_definition_assessment]
- Feature Coverage: [feature_coverage_assessment]
- Strategic Vision: [strategic_vision_assessment]

**Dependency Flow:**
- Tier 4 → Tier 3: [tier4_to_tier3_flow]
- Tier 3 → Tier 2: [tier3_to_tier2_flow]
- Tier 2 → Tier 1: [tier2_to_tier1_flow]

**Bottleneck Analysis:**
[for each cross_tier bottleneck:]
- **[bottleneck_location]**: [bottleneck_description]
  - Impact: [bottleneck_impact]
  - Resolution: [resolution_strategy]
```

### Tier Health Assessment
```
## 🏥 Tier Health Assessment

**Tier Performance Ranking:**
1. [best_tier]: [performance_score]% - [performance_description]
2. [second_tier]: [performance_score]% - [performance_description]
3. [third_tier]: [performance_score]% - [performance_description]
4. [fourth_tier]: [performance_score]% - [performance_description]

**Health Indicators:**
[for each tier health indicator:]
- **[tier_name]**: [health_status]
  - Strengths: [tier_strengths]
  - Weaknesses: [tier_weaknesses]
  - Trends: [tier_trends]
```

### Tier-Specific Strategies
```
## 🎯 Tier-Specific Strategies

**Tier 1 (Critical) Strategy:**
- **Focus:** [tier1_focus_strategy]
- **Timeline:** [tier1_timeline]
- **Success Metrics:** [tier1_success_metrics]
- **Key Actions:**
  1. [tier1_action_1]
  2. [tier1_action_2]
  3. [tier1_action_3]

**Tier 2 (Important) Strategy:**
- **Focus:** [tier2_focus_strategy]
- **Timeline:** [tier2_timeline]
- **Success Metrics:** [tier2_success_metrics]
- **Key Actions:**
  1. [tier2_action_1]
  2. [tier2_action_2]
  3. [tier2_action_3]

**Tier 3 (Standard) Strategy:**
- **Focus:** [tier3_focus_strategy]
- **Timeline:** [tier3_timeline]
- **Success Metrics:** [tier3_success_metrics]
- **Key Actions:**
  1. [tier3_action_1]
  2. [tier3_action_2]
  3. [tier3_action_3]

**Tier 4 (Optional) Strategy:**
- **Focus:** [tier4_focus_strategy]
- **Timeline:** [tier4_timeline]
- **Success Metrics:** [tier4_success_metrics]
- **Key Actions:**
  1. [tier4_action_1]
  2. [tier4_action_2]
  3. [tier4_action_3]
```

### Completion Roadmap
```
## 🗺️ Tier Completion Roadmap

**Phase 1: Foundation (Tier 1 Focus)**
- Target: [tier1_target]% Tier 1 completion
- Timeline: [phase1_timeline]
- Key Deliverables: [phase1_deliverables]

**Phase 2: Product Core (Tier 2 Focus)**
- Target: [tier2_target]% Tier 2 completion
- Timeline: [phase2_timeline]
- Key Deliverables: [phase2_deliverables]

**Phase 3: Feature Development (Tier 3 Focus)**
- Target: [tier3_target]% Tier 3 completion
- Timeline: [phase3_timeline]
- Key Deliverables: [phase3_deliverables]

**Phase 4: Strategic Enhancement (Tier 4 Focus)**
- Target: [tier4_target]% Tier 4 completion
- Timeline: [phase4_timeline]
- Key Deliverables: [phase4_deliverables]
```

### Recommendations
```
## 💡 Tier-Based Recommendations

**Immediate Actions (Next 24 hours):**
1. [immediate_action_1] - Focus on [target_tier]
2. [immediate_action_2] - Focus on [target_tier]
3. [immediate_action_3] - Focus on [target_tier]

**Short Term (This Week):**
1. [short_term_action_1] - [target_tier] focus
2. [short_term_action_2] - [target_tier] focus
3. [short_term_action_3] - [target_tier] focus

**Medium Term (This Month):**
1. [medium_term_action_1] - [target_tier] focus
2. [medium_term_action_2] - [target_tier] focus
3. [medium_term_action_3] - [target_tier] focus
```

## Data Processing Instructions

### Tier Health Calculation
```yaml
health_factors:
  completion_rate: "Weight: 40%"
  missing_critical: "Weight: 30%"
  progress_velocity: "Weight: 20%"
  dependency_health: "Weight: 10%"
```

### Performance Scoring
```yaml
performance_metrics:
  excellent: "90-100%"
  good: "70-89%"
  acceptable: "50-69%"
  needs_improvement: "< 50%"
```

### Priority Ranking
```yaml
priority_factors:
  tier_level: "Weight: 40%"
  completion_impact: "Weight: 30%"
  dependency_blocking: "Weight: 20%"
  strategic_value: "Weight: 10%"
```

## Response Guidelines
- Show tier-specific focus areas
- Highlight imbalances between tiers
- Provide tier-specific strategies
- Show progression path through tiers
- Emphasize foundation-first approach

## Success Criteria
- ✅ Clear tier-specific status shown
- ✅ Imbalances identified and addressed
- ✅ Tier-specific strategies provided
- ✅ Progression roadmap clear
- ✅ User understands tier priorities