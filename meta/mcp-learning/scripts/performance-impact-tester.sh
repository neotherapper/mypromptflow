#!/bin/bash

# MCP Learning System Performance Impact Tester
# Measures the performance overhead of PreToolUse hooks compared to direct execution
# Tests both valid and invalid parameter scenarios to measure different code paths

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MCP_LEARNING_DIR="$(dirname "$SCRIPT_DIR")"
PERFORMANCE_LOG="$MCP_LEARNING_DIR/performance-impact-results.md"
TEMP_DIR="/tmp/mcp-performance-test"

# Ensure temp directory exists
mkdir -p "$TEMP_DIR"

# Initialize performance log
cat > "$PERFORMANCE_LOG" << EOF
# MCP Learning System Performance Impact Analysis

**Test Date:** $(date '+%Y-%m-%d %H:%M:%S')
**Test Environment:** $(uname -s) $(uname -r)
**System:** $(uname -m)

## Test Methodology

This analysis measures the performance overhead introduced by PreToolUse hooks 
compared to direct MCP tool execution. Tests include:

1. **Direct Execution Baseline** - Raw tool validation without hooks
2. **Hook Execution** - Full PreToolUse hook validation pipeline  
3. **Different Scenarios** - Valid parameters, invalid parameters, corrections needed
4. **Scaling Tests** - Performance under different load patterns

## Test Results

EOF

# Test scenarios
declare -a TEST_SCENARIOS=(
    "valid_params:{\"issue_key\":\"PROJ-123\",\"fields\":\"summary\"}"
    "invalid_params:{\"issue_key\":\"invalid-test\",\"fields\":\"summary\"}"
    "missing_dash::{\"issue_key\":\"PROJ123\",\"fields\":\"summary\"}"
    "empty_json:{}"
    "complex_nested:{\"project_key\":\"PROJ\",\"summary\":\"Test\",\"issue_type\":\"Task\",\"additional_fields\":{\"priority\":{\"name\":\"High\"}}}"
)

# Performance measurement function
measure_performance() {
    local test_name="$1"
    local command="$2"
    local iterations=10
    local total_time=0
    local min_time=999999
    local max_time=0
    
    echo "### $test_name" >> "$PERFORMANCE_LOG"
    echo "" >> "$PERFORMANCE_LOG"
    
    for ((i=1; i<=iterations; i++)); do
        local start_time=$(perl -MTime::HiRes=time -e 'print time')
        eval "$command" >/dev/null 2>&1
        local end_time=$(perl -MTime::HiRes=time -e 'print time')
        
        local duration=$(echo "scale=6; $end_time - $start_time" | bc -l)
        total_time=$(echo "scale=6; $total_time + $duration" | bc -l)
        
        # Track min/max
        if (( $(echo "$duration < $min_time" | bc -l) )); then
            min_time=$duration
        fi
        if (( $(echo "$duration > $max_time" | bc -l) )); then
            max_time=$duration
        fi
        
        echo "  Iteration $i: ${duration}s" >> "$PERFORMANCE_LOG"
    done
    
    local avg_time=$(echo "scale=6; $total_time / $iterations" | bc -l)
    
    echo "" >> "$PERFORMANCE_LOG"
    echo "**Performance Summary:**" >> "$PERFORMANCE_LOG"
    echo "- **Average:** ${avg_time}s" >> "$PERFORMANCE_LOG"
    echo "- **Minimum:** ${min_time}s" >> "$PERFORMANCE_LOG"
    echo "- **Maximum:** ${max_time}s" >> "$PERFORMANCE_LOG"
    echo "- **Total:** ${total_time}s over $iterations iterations" >> "$PERFORMANCE_LOG"
    echo "" >> "$PERFORMANCE_LOG"
    
    # Return average time for comparison
    echo "$avg_time"
}

# Test direct validation (baseline)
echo "## Baseline Performance (Direct Validation)" >> "$PERFORMANCE_LOG"
echo "" >> "$PERFORMANCE_LOG"

baseline_times=()
for scenario in "${TEST_SCENARIOS[@]}"; do
    scenario_name=$(echo "$scenario" | cut -d':' -f1)
    scenario_data=$(echo "$scenario" | cut -d':' -f2-)
    
    echo "Testing baseline for $scenario_name..."
    
    # Direct validation command (bypassing hooks)
    direct_cmd="bash -c 'source $SCRIPT_DIR/mcp-parameter-validator.sh; validate_parameters \"mcp__MCP_DOCKER__jira_get_issue\" \"$scenario_data\"'"
    
    avg_time=$(measure_performance "Baseline: $scenario_name" "$direct_cmd")
    baseline_times+=("$scenario_name:$avg_time")
done

# Test hook performance
echo "## Hook Performance (PreToolUse Pipeline)" >> "$PERFORMANCE_LOG"
echo "" >> "$PERFORMANCE_LOG"

hook_times=()
for scenario in "${TEST_SCENARIOS[@]}"; do
    scenario_name=$(echo "$scenario" | cut -d':' -f1)
    scenario_data=$(echo "$scenario" | cut -d':' -f2-)
    
    echo "Testing hook performance for $scenario_name..."
    
    # Full hook pipeline command
    hook_cmd="bash '$SCRIPT_DIR/mcp-parameter-validator.sh' 'test-session' '/tmp/transcript' 'mcp__MCP_DOCKER__jira_get_issue' '$scenario_data'"
    
    avg_time=$(measure_performance "Hook: $scenario_name" "$hook_cmd")
    hook_times+=("$scenario_name:$avg_time")
done

# Performance comparison analysis
echo "## Performance Impact Analysis" >> "$PERFORMANCE_LOG"
echo "" >> "$PERFORMANCE_LOG"

echo "| Scenario | Baseline (s) | Hook (s) | Overhead (s) | Overhead (%) |" >> "$PERFORMANCE_LOG"
echo "|----------|--------------|----------|--------------|--------------|" >> "$PERFORMANCE_LOG"

total_baseline=0
total_hook=0
scenario_count=0

for i in "${!baseline_times[@]}"; do
    baseline_entry="${baseline_times[$i]}"
    hook_entry="${hook_times[$i]}"
    
    scenario_name=$(echo "$baseline_entry" | cut -d':' -f1)
    baseline_time=$(echo "$baseline_entry" | cut -d':' -f2)
    hook_time=$(echo "$hook_entry" | cut -d':' -f2)
    
    # Handle empty values for bc calculations
    if [[ -z "$baseline_time" || -z "$hook_time" ]]; then
        overhead="0.000000"
        overhead_percent="0.00"
    else
        overhead=$(echo "scale=6; $hook_time - $baseline_time" | bc -l)
        overhead_percent=$(echo "scale=2; ($overhead / $baseline_time) * 100" | bc -l)
    fi
    
    echo "| $scenario_name | $baseline_time | $hook_time | $overhead | ${overhead_percent}% |" >> "$PERFORMANCE_LOG"
    
    total_baseline=$(echo "scale=6; $total_baseline + $baseline_time" | bc -l)
    total_hook=$(echo "scale=6; $total_hook + $hook_time" | bc -l)
    scenario_count=$((scenario_count + 1))
done

# Calculate overall averages
avg_baseline=$(echo "scale=6; $total_baseline / $scenario_count" | bc -l)
avg_hook=$(echo "scale=6; $total_hook / $scenario_count" | bc -l)
avg_overhead=$(echo "scale=6; $avg_hook - $avg_baseline" | bc -l)
avg_overhead_percent=$(echo "scale=2; ($avg_overhead / $avg_baseline) * 100" | bc -l)

echo "|----------|--------------|----------|--------------|--------------|" >> "$PERFORMANCE_LOG"
echo "| **AVERAGE** | **$avg_baseline** | **$avg_hook** | **$avg_overhead** | **${avg_overhead_percent}%** |" >> "$PERFORMANCE_LOG"

# Performance recommendations
echo "" >> "$PERFORMANCE_LOG"
echo "## Performance Recommendations" >> "$PERFORMANCE_LOG"
echo "" >> "$PERFORMANCE_LOG"

# Generate recommendations based on overhead
overhead_threshold=0.100  # 100ms threshold

if (( $(echo "$avg_overhead > $overhead_threshold" | bc -l) )); then
    cat >> "$PERFORMANCE_LOG" << EOF
**⚠️  High Overhead Detected (${avg_overhead}s average)**

Recommendations for optimization:

1. **Script Optimization:**
   - Cache frequently used functions to avoid repeated sourcing
   - Optimize regex patterns in parameter validation
   - Reduce file I/O operations in validation pipeline

2. **Selective Hook Application:**
   - Apply hooks only to high-risk tool categories
   - Skip validation for tools with perfect success history
   - Use lightweight validation for low-risk parameters

3. **Async Processing:**
   - Move non-critical logging to background processes
   - Cache validation results for repeated parameter patterns
   - Implement validation result memoization

4. **Performance Monitoring:**
   - Set up automated performance regression detection
   - Monitor hook execution time in production
   - Alert on performance degradation > 50ms average
EOF
else
    cat >> "$PERFORMANCE_LOG" << EOF
**✅ Acceptable Performance Impact (${avg_overhead}s average)**

The current performance overhead is within acceptable limits. Consider:

1. **Monitoring:**
   - Regular performance measurement during system evolution
   - Track performance trends over time
   - Alert on degradation > ${overhead_threshold}s

2. **Optimization Opportunities:**
   - Profile individual validation functions for micro-optimizations
   - Consider batch processing for multiple similar validations
   - Cache validation results for frequently used parameters

3. **Scaling Considerations:**
   - Test performance under high-frequency MCP tool usage
   - Validate performance with larger validation rule sets
   - Monitor memory usage during extended operation
EOF
fi

# Add detailed profiling section
echo "" >> "$PERFORMANCE_LOG"
echo "## Detailed Performance Profiling" >> "$PERFORMANCE_LOG"
echo "" >> "$PERFORMANCE_LOG"

# Test component-level performance
echo "### Component Performance Breakdown" >> "$PERFORMANCE_LOG"
echo "" >> "$PERFORMANCE_LOG"

# Test individual components
component_tests=(
    "Parameter Correction:bash -c 'source $SCRIPT_DIR/mcp-parameter-corrector.sh; correct_parameters \"mcp__MCP_DOCKER__jira_get_issue\" \"{\\\"issue_key\\\":\\\"proj123\\\",\\\"fields\\\":\\\"summary\\\"}\"'"
    "Pattern Blocking:bash '$SCRIPT_DIR/mcp-pattern-blocker.sh' 'mcp__MCP_DOCKER__jira_get_issue' '{\"issue_key\":\"TEST-123\",\"fields\":\"summary\"}'"
    "Parameter Validation:bash -c 'source $SCRIPT_DIR/mcp-parameter-validator.sh; validate_parameters \"mcp__MCP_DOCKER__jira_get_issue\" \"{\\\"issue_key\\\":\\\"PROJ-123\\\",\\\"fields\\\":\\\"summary\\\"}\"'"
)

for component_test in "${component_tests[@]}"; do
    component_name=$(echo "$component_test" | cut -d':' -f1)
    component_cmd=$(echo "$component_test" | cut -d':' -f2-)
    
    echo "Testing $component_name performance..."
    component_avg=$(measure_performance "$component_name" "$component_cmd")
done

echo "" >> "$PERFORMANCE_LOG"
echo "## Test Completion" >> "$PERFORMANCE_LOG"
echo "" >> "$PERFORMANCE_LOG"
echo "Performance impact analysis completed at $(date '+%Y-%m-%d %H:%M:%S')" >> "$PERFORMANCE_LOG"
echo "" >> "$PERFORMANCE_LOG"
echo "**Next Steps:**" >> "$PERFORMANCE_LOG"
echo "1. Review performance results above" >> "$PERFORMANCE_LOG"
echo "2. Implement recommended optimizations if overhead > ${overhead_threshold}s" >> "$PERFORMANCE_LOG"
echo "3. Set up regular performance monitoring" >> "$PERFORMANCE_LOG"
echo "4. Track performance trends over time" >> "$PERFORMANCE_LOG"

# Clean up
rm -rf "$TEMP_DIR"

echo "Performance impact analysis complete. Results saved to: $PERFORMANCE_LOG"
echo ""
echo "Summary:"
echo "- Average baseline performance: ${avg_baseline}s"
echo "- Average hook performance: ${avg_hook}s"
echo "- Average overhead: ${avg_overhead}s (${avg_overhead_percent}%)"

if (( $(echo "$avg_overhead > $overhead_threshold" | bc -l) )); then
    echo "⚠️  Optimization recommended - overhead exceeds ${overhead_threshold}s threshold"
    exit 1
else
    echo "✅ Performance within acceptable limits"
    exit 0
fi