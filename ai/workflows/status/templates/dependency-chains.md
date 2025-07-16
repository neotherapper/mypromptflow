# Dependency Chains Template

## AI Instructions
Use this template to generate Option 7: Dependency Chains reports.

## Data Sources
- Primary: `dependency_analysis` from knowledge-status-cache.yaml
- Secondary: `dependencies.yaml` for full dependency mapping

## Report Structure

### Header
```
🔗 Dependency Chains Analysis
Analysis Date: [current_timestamp]
```

### Summary
```
📊 **Dependency Overview**
Total Documents: [total_documents]
Dependency Relationships: [total_dependencies]
Critical Path Length: [critical_path_length]
Bottleneck Points: [bottleneck_count]
```

### Critical Path Analysis
```
## 🎯 Critical Path (Longest Chain)

**Path Length:** [critical_path_length] dependencies
**Total Impact:** [critical_path_impact] documents

**Critical Path Sequence:**
[for each step in critical path:]
[step_number]. **[document_name]** ([tier])
    ↓ [dependency_relationship]
    Status: [current_status]
    ETA: [estimated_completion]
    Blocks: [blocks_count] documents

**Critical Path Bottlenecks:**
[for each bottleneck in critical path:]
- 🚧 **[bottleneck_document]**: [bottleneck_description]
  - Impact: [bottleneck_impact]
  - Resolution: [resolution_strategy]
```

### Dependency Chains by Tier
```
## 🔴 Tier 1 (Critical) Chains

[for each tier1 chain:]
**[root_document]** → [intermediate_docs] → **[end_document]**
- Chain Length: [chain_length]
- Status: [chain_status]
- Next Action: [next_action]

## 🟡 Tier 2 (Important) Chains

[for each tier2 chain:]
**[root_document]** → [intermediate_docs] → **[end_document]**
- Chain Length: [chain_length]
- Status: [chain_status]
- Next Action: [next_action]

## 🟢 Tier 3 (Standard) Chains

[for each tier3 chain:]
**[root_document]** → [intermediate_docs] → **[end_document]**
- Chain Length: [chain_length]
- Status: [chain_status]
- Next Action: [next_action]
```

### Dependency Network Visualization
```
## 🕸️ Dependency Network

**Foundation Layer** (No dependencies):
[for each foundation document:]
- 🏗️ **[document_name]** ([tier])
  - Status: [status]
  - Enables: [enables_count] documents

**Intermediate Layer** (Depends on foundation):
[for each intermediate document:]
- 🔗 **[document_name]** ([tier])
  - Depends on: [dependencies]
  - Status: [status]
  - Enables: [enables_count] documents

**Advanced Layer** (Depends on intermediate):
[for each advanced document:]
- 🎯 **[document_name]** ([tier])
  - Depends on: [dependencies]
  - Status: [status]
  - Enables: [enables_count] documents
```

### Parallel Processing Opportunities
```
## 🔄 Parallel Processing Opportunities

**Independent Chains** (Can work simultaneously):
[for each independent chain group:]
Group [group_number]:
- Chain A: [chain_a_documents]
- Chain B: [chain_b_documents]
- Chain C: [chain_c_documents]
- Parallel Capacity: [parallel_capacity] documents

**Shared Dependencies** (Coordinate carefully):
[for each shared dependency:]
- **[shared_document]** enables:
  - [dependent_document_1]
  - [dependent_document_2]
  - [dependent_document_3]
- Coordination Strategy: [coordination_strategy]
```

### Blocking Analysis
```
## 🔒 Blocking Analysis

**Most Blocking Documents:**
[for each highly blocking document:]
1. **[document_name]** ([tier])
   - Directly blocks: [direct_blocks_count] documents
   - Indirectly blocks: [indirect_blocks_count] documents
   - Total impact: [total_impact_count] documents
   - Status: [current_status]
   - Priority: [priority_level]

**Bottleneck Resolution Impact:**
[for each bottleneck resolution:]
- Resolving **[bottleneck_document]** would unblock:
  - [unblocked_document_1]
  - [unblocked_document_2]
  - [unblocked_document_3]
- Resolution effort: [resolution_effort]
- Impact score: [impact_score]
```

### Workflow Sequences
```
## 🔄 Recommended Workflow Sequences

**Sequence A: Foundation First**
1. [foundation_doc_1] → [foundation_doc_2] → [foundation_doc_3]
2. [intermediate_doc_1] → [intermediate_doc_2]
3. [advanced_doc_1] → [advanced_doc_2]

**Sequence B: Feature Focused**
1. [feature_foundation] → [feature_requirements] → [feature_implementation]
2. [feature_testing] → [feature_deployment]

**Sequence C: Parallel Streams**
Stream 1: [stream1_docs]
Stream 2: [stream2_docs]
Stream 3: [stream3_docs]
Merge Point: [merge_document]
```

### Dependency Health Check
```
## 🏥 Dependency Health Check

**Healthy Chains** (No issues):
[for each healthy chain:]
- [chain_name]: [chain_description]
  - Status: ✅ All dependencies satisfied
  - Progress: [progress_percentage]%

**At Risk Chains** (Potential issues):
[for each at_risk chain:]
- [chain_name]: [chain_description]
  - Issue: [risk_description]
  - Mitigation: [mitigation_strategy]

**Broken Chains** (Blocked/circular):
[for each broken chain:]
- [chain_name]: [chain_description]
  - Problem: [problem_description]
  - Solution: [solution_strategy]
```

### Optimization Recommendations
```
## 🎯 Optimization Recommendations

**Immediate Optimizations:**
1. **[optimization_1]**
   - Action: [action_description]
   - Impact: [impact_description]
   - Effort: [effort_required]

2. **[optimization_2]**
   - Action: [action_description]
   - Impact: [impact_description]
   - Effort: [effort_required]

**Strategic Optimizations:**
1. **[strategic_optimization_1]**
   - Long-term benefit: [benefit_description]
   - Implementation: [implementation_strategy]

2. **[strategic_optimization_2]**
   - Long-term benefit: [benefit_description]
   - Implementation: [implementation_strategy]
```

### Alternative Dependency Paths
```
## 🛤️ Alternative Dependency Paths

**If [primary_path] is blocked:**

**Alternative Path A:**
[alternative_path_a_sequence]
- Trade-offs: [tradeoff_analysis_a]
- Timeline: [timeline_a]

**Alternative Path B:**
[alternative_path_b_sequence]
- Trade-offs: [tradeoff_analysis_b]
- Timeline: [timeline_b]

**Hybrid Approach:**
[hybrid_approach_description]
- Benefits: [hybrid_benefits]
- Complexity: [hybrid_complexity]
```

### Next Actions
```
## 🎯 Recommended Next Actions

**To Optimize Critical Path:**
1. [critical_path_action_1]
2. [critical_path_action_2]
3. [critical_path_action_3]

**To Enable Parallel Work:**
1. [parallel_work_action_1]
2. [parallel_work_action_2]
3. [parallel_work_action_3]

**To Resolve Bottlenecks:**
1. [bottleneck_action_1]
2. [bottleneck_action_2]
3. [bottleneck_action_3]
```

## Data Processing Instructions

### Chain Analysis
```yaml
chain_metrics:
  length: "Count of dependency levels"
  complexity: "Branching factor"
  health: "Status of all dependencies"
  impact: "Documents affected by chain"
```

### Bottleneck Detection
```yaml
bottleneck_criteria:
  high_fanout: "Blocks many documents"
  critical_path: "On longest chain"
  incomplete: "Not yet completed"
  high_effort: "Requires significant work"
```

### Optimization Scoring
```yaml
optimization_factors:
  impact_reduction: "Weight: 40%"
  effort_required: "Weight: 30%"
  risk_mitigation: "Weight: 20%"
  strategic_value: "Weight: 10%"
```

## Response Guidelines
- Use visual representations where possible
- Show both current state and optimized state
- Provide actionable recommendations
- Highlight parallel opportunities
- Focus on unblocking progress

## Success Criteria
- ✅ Clear visualization of dependencies
- ✅ Bottlenecks identified and prioritized
- ✅ Optimization opportunities shown
- ✅ Parallel work paths identified
- ✅ User understands dependency strategy