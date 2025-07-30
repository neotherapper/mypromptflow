#!/bin/bash

# Test Hook Functionality Validation Script
# Tests the MCP learning system hooks without requiring actual MCP servers
# Simulates tool calls and validates hook execution

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MCP_LEARNING_DIR="$(dirname "$SCRIPT_DIR")"
TEST_RESULTS_DIR="$MCP_LEARNING_DIR/test-results"
TEST_LOG="$TEST_RESULTS_DIR/hook-functionality-test.log"

# Ensure test results directory exists
mkdir -p "$TEST_RESULTS_DIR"

# Initialize test log
echo "=== MCP Learning System Hook Functionality Test ===" > "$TEST_LOG"
echo "Started: $(date '+%Y-%m-%d %H:%M:%S')" >> "$TEST_LOG"
echo "" >> "$TEST_LOG"

# Test counter
test_count=0
passed_tests=0
failed_tests=0

# Test execution function
run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected_result="$3"
    
    test_count=$((test_count + 1))
    echo "Test $test_count: $test_name" | tee -a "$TEST_LOG"
    echo "Command: $test_command" >> "$TEST_LOG"
    echo "Expected: $expected_result" >> "$TEST_LOG"
    
    # Execute test command and capture result
    local actual_result
    actual_result=$(eval "$test_command" 2>&1)
    local exit_code=$?
    
    echo "Actual: $actual_result" >> "$TEST_LOG"
    echo "Exit Code: $exit_code" >> "$TEST_LOG"
    
    # Check if test passed
    if [[ "$actual_result" =~ $expected_result ]]; then
        echo "✅ PASSED" | tee -a "$TEST_LOG"
        passed_tests=$((passed_tests + 1))
    else
        echo "❌ FAILED" | tee -a "$TEST_LOG"
        failed_tests=$((failed_tests + 1))
    fi
    
    echo "" >> "$TEST_LOG"
}

# Test 1: Parameter Validator Script Execution
echo "=== Testing Parameter Validator Script ===" | tee -a "$TEST_LOG"

run_test "Parameter Validator - Valid JIRA Issue Key" \
    "bash '$SCRIPT_DIR/mcp-parameter-validator.sh' 'test-session' '/tmp/transcript' 'mcp__MCP_DOCKER__jira_get_issue' '{\"issue_key\":\"PROJ-123\",\"fields\":\"summary\"}'" \
    "permissionDecision.*allow"

run_test "Parameter Validator - Invalid JIRA Issue Key" \
    "bash '$SCRIPT_DIR/mcp-parameter-validator.sh' 'test-session' '/tmp/transcript' 'mcp__MCP_DOCKER__jira_get_issue' '{\"issue_key\":\"invalid-test\",\"fields\":\"summary\"}'" \
    "permissionDecision.*(deny|ask)"

run_test "Parameter Validator - Non-MCP Tool" \
    "bash '$SCRIPT_DIR/mcp-parameter-validator.sh' 'test-session' '/tmp/transcript' 'regular_tool' '{\"param\":\"value\"}'" \
    "Non-MCP tool"

# Test 2: Parameter Corrector Script Execution
echo "=== Testing Parameter Corrector Script ===" | tee -a "$TEST_LOG"

run_test "Parameter Corrector - Lowercase Issue Key" \
    "bash '$SCRIPT_DIR/mcp-parameter-corrector.sh' 'mcp__MCP_DOCKER__jira_get_issue' '{\"issue_key\":\"proj-123\",\"fields\":\"summary\"}'" \
    "PROJ-123"

run_test "Parameter Corrector - Missing Dash in Issue Key" \
    "bash '$SCRIPT_DIR/mcp-parameter-corrector.sh' 'mcp__MCP_DOCKER__jira_get_issue' '{\"issue_key\":\"PROJ123\",\"fields\":\"summary\"}'" \
    "PROJ-123"

# Test 3: Pattern Blocker Script Execution
echo "=== Testing Pattern Blocker Script ===" | tee -a "$TEST_LOG"

run_test "Pattern Blocker - Test Issue Key" \
    "bash '$SCRIPT_DIR/mcp-pattern-blocker.sh' 'mcp__MCP_DOCKER__jira_get_issue' '{\"issue_key\":\"TEST-123\",\"fields\":\"summary\"}'" \
    "should_block.*true"

run_test "Pattern Blocker - Valid Issue Key" \
    "bash '$SCRIPT_DIR/mcp-pattern-blocker.sh' 'mcp__MCP_DOCKER__jira_get_issue' '{\"issue_key\":\"PROJ-123\",\"fields\":\"summary\"}'" \
    "should_block.*false"

# Test 4: Learning Engine Script Execution
echo "=== Testing Learning Engine Script ===" | tee -a "$TEST_LOG"

# Check if timeout command is available, otherwise skip timeout functionality
if command -v timeout >/dev/null 2>&1; then
    run_test "Learning Engine - Analyze Mode" \
        "timeout 10 bash '$SCRIPT_DIR/mcp-learning-engine.sh' analyze" \
        "Data analysis completed"
else
    run_test "Learning Engine - Analyze Mode (No timeout)" \
        "bash '$SCRIPT_DIR/mcp-learning-engine.sh' analyze" \
        "Data analysis completed"
fi

# Test 5: Performance Tracker Script Execution
echo "=== Testing Performance Tracker Script ===" | tee -a "$TEST_LOG"

run_test "Performance Tracker - Metrics Mode" \
    "bash '$SCRIPT_DIR/mcp-performance-tracker.sh' metrics" \
    "Total.*Prevented.*Blocked.*Corrected"

# Test 6: JSON Parsing Validation
echo "=== Testing JSON Parsing Robustness ===" | tee -a "$TEST_LOG"

run_test "JSON Parsing - Malformed JSON" \
    "bash '$SCRIPT_DIR/mcp-parameter-validator.sh' 'test-session' '/tmp/transcript' 'mcp__MCP_DOCKER__jira_get_issue' '{\"issue_key\":\"PROJ-123\"invalid}'" \
    "(allow|deny|ask)"

run_test "JSON Parsing - Empty JSON" \
    "bash '$SCRIPT_DIR/mcp-parameter-validator.sh' 'test-session' '/tmp/transcript' 'mcp__MCP_DOCKER__jira_get_issue' '{}'" \
    "Missing required parameter"

run_test "JSON Parsing - Complex Nested JSON" \
    "bash '$SCRIPT_DIR/mcp-parameter-validator.sh' 'test-session' '/tmp/transcript' 'mcp__MCP_DOCKER__jira_create_issue' '{\"project_key\":\"PROJ\",\"summary\":\"Test\",\"issue_type\":\"Task\",\"additional_fields\":{\"priority\":{\"name\":\"High\"}}}'" \
    "permissionDecision.*allow"

# Test 7: Hook Integration Simulation
echo "=== Testing Hook Integration Simulation ===" | tee -a "$TEST_LOG"

# Create temporary hook test environment
TEMP_HOOK_TEST="$TEST_RESULTS_DIR/temp-hook-test.sh"
cat > "$TEMP_HOOK_TEST" << EOF
#!/bin/bash
# Simulate PreToolUse hook execution
export CLAUDE_SESSION_ID="test-session-123"
export CLAUDE_TRANSCRIPT_PATH="/tmp/test-transcript"
export CLAUDE_TOOL_NAME="mcp__MCP_DOCKER__jira_get_issue"
export CLAUDE_TOOL_INPUT='{"issue_key":"TEST-456","fields":"summary,status"}'

# Execute the validator as it would be called by Claude Code
bash "$SCRIPT_DIR/mcp-parameter-validator.sh" "\$CLAUDE_SESSION_ID" "\$CLAUDE_TRANSCRIPT_PATH" "\$CLAUDE_TOOL_NAME" "\$CLAUDE_TOOL_INPUT"
EOF

chmod +x "$TEMP_HOOK_TEST"

run_test "Hook Integration - Environment Variable Simulation" \
    "bash '$TEMP_HOOK_TEST'" \
    "permissionDecision"

# Clean up temporary files
rm -f "$TEMP_HOOK_TEST"

# Test Summary
echo "=== Test Summary ===" | tee -a "$TEST_LOG"
echo "Total Tests: $test_count" | tee -a "$TEST_LOG"
echo "Passed: $passed_tests" | tee -a "$TEST_LOG"
echo "Failed: $failed_tests" | tee -a "$TEST_LOG"
echo "Success Rate: $(echo "scale=1; $passed_tests * 100 / $test_count" | bc 2>/dev/null || echo "N/A")%" | tee -a "$TEST_LOG"
echo "Completed: $(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$TEST_LOG"

# Overall result
if [[ $failed_tests -eq 0 ]]; then
    echo "" | tee -a "$TEST_LOG"
    echo "🎉 ALL TESTS PASSED - Hook functionality validation successful!" | tee -a "$TEST_LOG"
    exit 0
else
    echo "" | tee -a "$TEST_LOG"
    echo "⚠️  Some tests failed - review results and fix issues" | tee -a "$TEST_LOG"
    exit 1
fi