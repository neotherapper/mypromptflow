# Blocked Documents Template

## AI Instructions
Use this template to generate Option 5: Blocked Documents reports.

## Data Sources
- Primary: `dependency_analysis.blocking_dependencies` from knowledge-status-cache.yaml
- Secondary: `dependencies.yaml` for full dependency chains

## Report Structure

### Header
```
🔒 Blocked Documents Report
Analysis Date: [current_timestamp]
```

### Summary
```
⚠️ **Blocking Summary**
Total Blocked: [count_blocked] documents
Critical Blocks: [count_critical_blocks]
Average Block Depth: [average_dependency_depth]
```

### Critical Blocks (Tier 1)
```
## 🔴 Critical Blocked Documents (Tier 1)

[for each tier1 blocked document:]
- 🔒 **[document_name]**
  - Blocked By: [blocking_dependencies]
  - Also Blocking: [count_downstream_blocked] documents
  - Impact: [impact_description]
  - Resolution Path: [resolution_steps]
  - Estimated Unblock Time: [estimated_time]
```

### Important Blocks (Tier 2)
```
## 🟡 Important Blocked Documents (Tier 2)

[for each tier2 blocked document:]
- 🔒 **[document_name]**
  - Blocked By: [blocking_dependencies]
  - Also Blocking: [count_downstream_blocked] documents
  - Impact: [impact_description]
  - Resolution Path: [resolution_steps]
  - Estimated Unblock Time: [estimated_time]
```

### Standard Blocks (Tier 3)
```
## 🟢 Standard Blocked Documents (Tier 3)

[for each tier3 blocked document:]
- 🔒 **[document_name]**
  - Blocked By: [blocking_dependencies]
  - Also Blocking: [count_downstream_blocked] documents
  - Impact: [impact_description]
  - Resolution Path: [resolution_steps]
  - Estimated Unblock Time: [estimated_time]
```

### Dependency Chain Analysis
```
## 🔗 Dependency Chain Analysis

**Longest Blocking Chains**:
[for each long chain:]
1. [root_document] → [intermediate_docs] → [final_document]
   - Chain Length: [chain_length] dependencies
   - Total Impact: [total_blocked_count] documents
   - Resolution Strategy: [strategy_description]

**Circular Dependencies** (if any):
[for each circular dependency:]
- 🔄 [document_a] ↔ [document_b]
  - Resolution: [circular_resolution_strategy]
```

### Bottleneck Analysis
```
## 🚧 Bottleneck Analysis

**Major Bottlenecks**:
[for each bottleneck document:]
- 🚧 **[bottleneck_document]**
  - Currently Blocking: [count_blocked] documents
  - Status: [current_status]
  - Progress: [completion_percentage]%
  - ETA: [estimated_completion]
  - Action Needed: [action_required]
```

### Resolution Strategies
```
## 🔧 Resolution Strategies

**Immediate Actions** (Can start today):
1. **[action_1]** - Create [dependency_document]
   - Command: `/create-document [dependency_name]`
   - Will Unblock: [unblocked_documents]
   - Time Required: [time_estimate]

2. **[action_2]** - Complete [in_progress_document]
   - Current Status: [current_status]
   - Remaining Work: [remaining_work]
   - Will Unblock: [unblocked_documents]

**Short Term** (This week):
[for each short term action:]
- [action_description]
  - Target: [target_document]
  - Impact: [impact_description]

**Medium Term** (This month):
[for each medium term action:]
- [action_description]
  - Target: [target_document]
  - Impact: [impact_description]
```

### Parallel Unblocking Opportunities
```
## 🔄 Parallel Unblocking Opportunities

**Independent Chains**:
Chain A: [independent_chain_a]
- Can work on: [workable_documents_a]
- While waiting for: [blocking_documents_a]

Chain B: [independent_chain_b]
- Can work on: [workable_documents_b]
- While waiting for: [blocking_documents_b]

**Partial Progress**:
[for each partial progress opportunity:]
- **[document_name]**: Can complete [completable_sections]
  - Even without: [missing_dependencies]
  - Progress possible: [progress_percentage]%
```

### Workaround Options
```
## 🛠️ Workaround Options

**Temporary Solutions**:
[for each workaround:]
- **For [blocked_document]**:
  - Workaround: [workaround_description]
  - Allows Progress On: [enabled_progress]
  - Temporary Duration: [workaround_duration]
  - Migration Plan: [migration_strategy]

**Alternative Approaches**:
[for each alternative:]
- **Instead of [blocked_document]**:
  - Alternative: [alternative_approach]
  - Trade-offs: [tradeoff_analysis]
  - Recommendation: [recommendation]
```

### Prioritized Unblocking Plan
```
## 📊 Prioritized Unblocking Plan

**Phase 1** (Next 24 hours):
1. Create [phase1_document_1] - Unblocks [count] documents
2. Complete [phase1_document_2] - Unblocks [count] documents
3. Start [phase1_document_3] - Partial unblocking

**Phase 2** (Next week):
1. [phase2_action_1]
2. [phase2_action_2]
3. [phase2_action_3]

**Phase 3** (Next month):
1. [phase3_action_1]
2. [phase3_action_2]
3. [phase3_action_3]
```

### Success Metrics
```
## 📈 Unblocking Success Metrics

**Target Metrics**:
- Reduce blocked documents by [target_reduction]%
- Unblock [target_unblock_count] high-priority documents
- Eliminate [bottleneck_count] major bottlenecks

**Progress Tracking**:
- Weekly blocked document count review
- Dependency chain length monitoring
- Bottleneck resolution progress
```

## Data Processing Instructions

### Block Severity Assessment
```yaml
severity_levels:
  critical: "Blocks multiple tier 1 documents"
  high: "Blocks important workflow"
  medium: "Affects specific features"
  low: "Minor impact"
```

### Chain Analysis
```yaml
chain_metrics:
  depth: "Number of dependency levels"
  breadth: "Number of documents affected"
  criticality: "Tier levels involved"
```

### Resolution Priority
```yaml
priority_factors:
  unblock_count: "Weight: 40%"
  tier_impact: "Weight: 30%"
  effort_required: "Weight: 20%"
  time_sensitivity: "Weight: 10%"
```

## Response Guidelines
- Focus on solutions, not just problems
- Provide concrete unblocking steps
- Show progress opportunities
- Highlight quick wins
- Encourage parallel work

## Success Criteria
- ✅ Clear understanding of blocking issues
- ✅ Concrete unblocking plan provided
- ✅ Priority actions identified
- ✅ Parallel work opportunities shown
- ✅ User knows exactly what to do next