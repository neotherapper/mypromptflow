#!/bin/bash

# Complete Hook Chain Integration Test
# Tests the full PreToolUse → PostToolUse workflow with enhanced integration

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MCP_LEARNING_DIR="$SCRIPT_DIR"
TEST_RESULTS_DIR="$MCP_LEARNING_DIR/test-results"

# Ensure test results directory exists
mkdir -p "$TEST_RESULTS_DIR"

echo "=== Complete MCP Learning Hook Chain Test ==="
echo "Started: $(date)"
echo

# Test files
TEST_LOG="$TEST_RESULTS_DIR/complete-hook-chain-test.log"
> "$TEST_LOG"  # Clear previous test results

# Test counter
TOTAL_TESTS=0
PASSED_TESTS=0

run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected_pattern="$3"
    local test_description="$4"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    echo "Test $TOTAL_TESTS: $test_name" | tee -a "$TEST_LOG"
    echo "Description: $test_description" | tee -a "$TEST_LOG"
    echo "Command: $test_command" | tee -a "$TEST_LOG"
    echo "Expected: $expected_pattern" | tee -a "$TEST_LOG"
    
    # Run the test
    local output
    local exit_code
    output=$(eval "$test_command" 2>&1) || exit_code=$?
    
    echo "Actual: $output" | tee -a "$TEST_LOG"
    echo "Exit Code: ${exit_code:-0}" | tee -a "$TEST_LOG"
    
    # Check if test passed
    if echo "$output" | grep -q "$expected_pattern"; then
        echo "✅ PASSED" | tee -a "$TEST_LOG"
        PASSED_TESTS=$((PASSED_TESTS + 1))
    else
        echo "❌ FAILED" | tee -a "$TEST_LOG"
    fi
    echo | tee -a "$TEST_LOG"
}

echo "=== Testing PreToolUse Hook Chain ===" | tee -a "$TEST_LOG"

# Test 1: Valid JIRA parameters (should allow with pattern blocker integration)
run_test \
    "PreToolUse - Valid JIRA Issue Key" \
    "bash '$MCP_LEARNING_DIR/scripts/mcp-parameter-validator.sh' 'test-session' '/tmp/transcript' 'mcp__MCP_DOCKER__jira_get_issue' '{\"issue_key\":\"PROJ-123\",\"fields\":\"summary\"}'" \
    "\"action\": \"allow\"" \
    "Valid JIRA issue key should be allowed through complete validation chain"

# Test 2: Invalid JIRA parameters (should be blocked by pattern blocker)
run_test \
    "PreToolUse - Invalid JIRA Issue Key (Pattern Blocked)" \
    "bash '$MCP_LEARNING_DIR/scripts/mcp-parameter-validator.sh' 'test-session' '/tmp/transcript' 'mcp__MCP_DOCKER__jira_get_issue' '{\"issue_key\":\"invalid-test\",\"fields\":\"summary\"}'" \
    "Pattern blocker.*invalid" \
    "Invalid JIRA issue key should be blocked by pattern blocker"

# Test 3: Test pattern that should be asked about
run_test \
    "PreToolUse - Test Pattern (Should Ask)" \
    "bash '$MCP_LEARNING_DIR/scripts/mcp-parameter-validator.sh' 'test-session' '/tmp/transcript' 'mcp__MCP_DOCKER__jira_get_issue' '{\"issue_key\":\"TEST-123\",\"fields\":\"summary\"}'" \
    "\"action\": \"ask\"" \
    "Test patterns should trigger ask action"

# Test 4: Parameter correction integration
run_test \
    "PreToolUse - Parameter Correction" \
    "bash '$MCP_LEARNING_DIR/scripts/mcp-parameter-corrector.sh' 'mcp__MCP_DOCKER__jira_get_issue' '{\"issue_key\":\"PROJ123\",\"fields\":\"summary\"}'" \
    "PROJ-123" \
    "Parameter corrector should fix missing dash in issue key"

echo "=== Testing PostToolUse Hook Chain ===" | tee -a "$TEST_LOG"

# Test 5: Error detection with enhanced patterns
run_test \
    "PostToolUse - Authentication Error Detection" \
    "bash '$MCP_LEARNING_DIR/scripts/mcp-error-detector.sh' 'mcp__MCP_DOCKER__jira_get_issue' 'Error: 401 Unauthorized - Invalid credentials'" \
    "Error detected and logged" \
    "Should detect authentication errors and log them"

# Test 6: Success pattern logging
run_test \
    "PostToolUse - Success Pattern Logging" \
    "bash '$MCP_LEARNING_DIR/scripts/mcp-error-detector.sh' 'mcp__MCP_DOCKER__jira_get_issue' 'Successfully retrieved issue PROJ-123'" \
    "Success logged" \
    "Should log successful operations for pattern learning"

# Test 7: Server-specific error detection
run_test \
    "PostToolUse - JIRA Specific Error Detection" \
    "bash '$MCP_LEARNING_DIR/scripts/mcp-error-detector.sh' 'mcp__MCP_DOCKER__jira_get_issue' 'Issue does not exist or you do not have permission to see it'" \
    "Error detected and logged" \
    "Should detect JIRA-specific errors"

# Test 8: Notion error detection
run_test \
    "PostToolUse - Notion Error Detection" \
    "bash '$MCP_LEARNING_DIR/scripts/mcp-error-detector.sh' 'mcp__MCP_DOCKER__API-retrieve-a-page' 'Page not found or access denied'" \
    "Error detected and logged" \
    "Should detect Notion-specific errors"

echo "=== Testing Integration Flow ===" | tee -a "$TEST_LOG"

# Test 9: End-to-end flow simulation
run_test \
    "Integration - Parameter Validation + Success Logging" \
    "bash '$MCP_LEARNING_DIR/scripts/mcp-parameter-validator.sh' 'test-session' '/tmp/transcript' 'mcp__MCP_DOCKER__jira_get_issue' '{\"issue_key\":\"VALID-456\",\"fields\":\"summary\"}' && echo 'Tool executed successfully' | bash '$MCP_LEARNING_DIR/scripts/mcp-error-detector.sh' 'mcp__MCP_DOCKER__jira_get_issue'" \
    "Success logged" \
    "Complete flow from validation to success logging"

# Test 10: Comprehensive statistics check
run_test \
    "Integration - Statistics Generation" \
    "bash '$MCP_LEARNING_DIR/scripts/mcp-performance-tracker.sh' metrics | head -5" \
    "Total.*Blocked.*Parameters.*Corrected" \
    "Performance tracker should show comprehensive statistics"

echo "=== Test Results Summary ===" | tee -a "$TEST_LOG"
SUCCESS_RATE=$(( (PASSED_TESTS * 100) / TOTAL_TESTS ))
echo "Total Tests: $TOTAL_TESTS" | tee -a "$TEST_LOG"
echo "Passed: $PASSED_TESTS" | tee -a "$TEST_LOG"
echo "Failed: $((TOTAL_TESTS - PASSED_TESTS))" | tee -a "$TEST_LOG"
echo "Success Rate: ${SUCCESS_RATE}%" | tee -a "$TEST_LOG"
echo "Completed: $(date)" | tee -a "$TEST_LOG"

if [ $SUCCESS_RATE -ge 80 ]; then
    echo | tee -a "$TEST_LOG"
    echo "🎉 Hook chain integration successful! Ready for production use." | tee -a "$TEST_LOG"
    exit 0
else
    echo | tee -a "$TEST_LOG"
    echo "⚠️  Some integration issues detected - review and fix before production." | tee -a "$TEST_LOG"
    exit 1
fi