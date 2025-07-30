#!/bin/bash

# MCP Error Pattern Blocking Engine
# Dynamically blocks MCP calls based on learned error patterns
# Evolves blocking rules based on error frequency and context

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MCP_LEARNING_DIR="$(dirname "$SCRIPT_DIR")"
ERROR_LOGS_DIR="$MCP_LEARNING_DIR/error-logs"
PATTERNS_DIR="$MCP_LEARNING_DIR/patterns"
BLOCKED_PATTERNS_FILE="$PATTERNS_DIR/blocked-patterns.yaml"
BLOCKING_LOG="$MCP_LEARNING_DIR/pattern-blocking-log.txt"

# Ensure patterns directory exists
mkdir -p "$PATTERNS_DIR"

# Initialize blocked patterns file if it doesn't exist
initialize_blocked_patterns() {
    if [[ ! -f "$BLOCKED_PATTERNS_FILE" ]]; then
        cat > "$BLOCKED_PATTERNS_FILE" << 'EOF'
# Dynamic Error Pattern Blocking Rules
# Auto-generated from error logs and learning system
# Format: server -> tool -> pattern -> blocking_rule

blocking_rules:
  jira:
    mcp__MCP_DOCKER__jira_get_issue:
      invalid_issue_keys:
        patterns:
          - "TEST-.*"
          - "INVALID-.*"
          - "DUMMY-.*"
          - "FAKE-.*"
        severity: "medium"
        action: "ask"
        reason: "Issue key appears to be a test value"
        frequency_threshold: 2
      malformed_keys:
        patterns:
          - "^[a-z].*"  # lowercase keys
          - ".*[^A-Z0-9-].*"  # invalid characters
          - "^[A-Z]+[0-9]+$"  # missing dash
        severity: "high"
        action: "deny"
        reason: "Issue key format is invalid"
        frequency_threshold: 1
    mcp__MCP_DOCKER__jira_search:
      dangerous_jql:
        patterns:
          - ".*DROP.*"
          - ".*DELETE.*"
          - ".*UPDATE.*"
          - ".*INSERT.*"
        severity: "critical"
        action: "deny"
        reason: "JQL contains SQL-like commands"
        frequency_threshold: 1
      syntax_errors:
        patterns:
          - ".*=[[:space:]]*[^\"'[:space:]][^[:space:]]*[[:space:]]*(AND|OR).*"
        severity: "medium"
        action: "ask"
        reason: "Unquoted JQL values may cause syntax errors"
        frequency_threshold: 2

learning_config:
  auto_update: true
  frequency_analysis: true
  confidence_threshold: 0.7
  max_patterns_per_rule: 10
  
statistics:
  last_updated: "2025-07-30"
  total_patterns: 0
  blocked_calls: 0
  successful_blocks: 0
EOF
    fi
}

# Check if tool call should be blocked based on learned patterns
check_blocking_rules() {
    local tool_name="$1"
    local tool_input="$2"
    local server_name=$(get_server_name "$tool_name")
    
    # Initialize patterns file if needed
    initialize_blocked_patterns
    
    # Load and check blocking rules
    local blocking_decision=$(analyze_blocking_patterns "$server_name" "$tool_name" "$tool_input")
    echo "$blocking_decision"
}

# Analyze tool input against blocking patterns
analyze_blocking_patterns() {
    local server_name="$1"
    local tool_name="$2"
    local tool_input="$3"
    
    # Check server-specific patterns
    case "$server_name" in
        "jira")
            analyze_jira_blocking_patterns "$tool_name" "$tool_input"
            ;;
        *)
            # No specific patterns for this server
            echo '{"should_block": false, "reason": "No blocking patterns defined"}'
            ;;
    esac
}

# Analyze JIRA-specific blocking patterns
analyze_jira_blocking_patterns() {
    local tool_name="$1"
    local tool_input="$2"
    
    case "$tool_name" in
        mcp__MCP_DOCKER__jira_get_issue)
            check_jira_issue_key_patterns "$tool_input"
            ;;
        mcp__MCP_DOCKER__jira_search)
            check_jira_search_patterns "$tool_input"
            ;;
        mcp__MCP_DOCKER__jira_create_issue)
            check_jira_create_patterns "$tool_input"
            ;;
        *)
            echo '{"should_block": false, "reason": "No specific blocking rules for this tool"}'
            ;;
    esac
}

# Check JIRA issue key patterns for blocking
check_jira_issue_key_patterns() {
    local tool_input="$1"
    local issue_key=$(echo "$tool_input" | grep -o '"issue_key":"[^"]*"' | cut -d'"' -f4)
    
    if [[ -z "$issue_key" ]]; then
        echo '{"should_block": false, "reason": "No issue key to validate"}'
        return
    fi
    
    # Critical blocking patterns (always deny)
    local critical_patterns=(
        "^[a-z]"  # lowercase keys
        "[^A-Z0-9-]"  # invalid characters
        "^[A-Z]+[0-9]+$"  # missing dash
    )
    
    for pattern in "${critical_patterns[@]}"; do
        if [[ "$issue_key" =~ $pattern ]]; then
            log_blocked_call "$tool_name" "$tool_input" "Critical: Issue key format violation: $pattern"
            echo '{"should_block": true, "action": "deny", "severity": "critical", "reason": "Issue key format is invalid and will cause API error"}'
            return
        fi
    done
    
    # Warning patterns (ask for confirmation)
    local warning_patterns=(
        "TEST-"
        "INVALID-"
        "DUMMY-"
        "FAKE-"
        "EXAMPLE-"
    )
    
    for pattern in "${warning_patterns[@]}"; do
        if [[ "$issue_key" == *"$pattern"* ]]; then
            log_blocked_call "$tool_name" "$tool_input" "Warning: Suspicious test key: $pattern"
            echo '{"should_block": true, "action": "ask", "severity": "medium", "reason": "Issue key appears to be a test value - confirm this is intentional"}'
            return
        fi
    done
    
    # Check against historically failed keys
    if check_historical_failures "jira" "$issue_key"; then
        echo '{"should_block": true, "action": "ask", "severity": "medium", "reason": "This issue key has failed before - confirm it exists"}'
        return
    fi
    
    echo '{"should_block": false, "reason": "Issue key passes all blocking checks"}'
}

# Check JIRA search patterns for blocking
check_jira_search_patterns() {
    local tool_input="$1"
    local jql=$(echo "$tool_input" | grep -o '"jql":"[^"]*"' | cut -d'"' -f4)
    
    if [[ -z "$jql" ]]; then
        echo '{"should_block": false, "reason": "No JQL to validate"}'
        return
    fi
    
    # Critical blocking patterns (SQL injection-like)
    local dangerous_patterns=(
        "DROP"
        "DELETE"
        "UPDATE"
        "INSERT"
        "ALTER"
        "CREATE"
    )
    
    for pattern in "${dangerous_patterns[@]}"; do
        if [[ "$jql" =~ $pattern ]]; then
            log_blocked_call "$tool_name" "$tool_input" "Critical: Dangerous JQL pattern: $pattern"
            echo '{"should_block": true, "action": "deny", "severity": "critical", "reason": "JQL contains potentially dangerous SQL-like commands"}'
            return
        fi
    done
    
    # Syntax warning patterns
    if [[ "$jql" =~ [[:space:]]*=[[:space:]]*[^\"\'[:space:]][^[:space:]]*[[:space:]]*(AND|OR) ]]; then
        echo '{"should_block": true, "action": "ask", "severity": "medium", "reason": "JQL has unquoted values that may cause syntax errors"}'
        return
    fi
    
    echo '{"should_block": false, "reason": "JQL passes all blocking checks"}'
}

# Check JIRA create patterns for blocking
check_jira_create_patterns() {
    local tool_input="$1"
    local project_key=$(echo "$tool_input" | grep -o '"project_key":"[^"]*"' | cut -d'"' -f4)
    
    # Check for obviously invalid project keys
    if [[ -n "$project_key" ]]; then
        if [[ "$project_key" =~ ^[a-z] ]]; then
            log_blocked_call "$tool_name" "$tool_input" "Critical: Lowercase project key"
            echo '{"should_block": true, "action": "deny", "severity": "critical", "reason": "Project key must be uppercase"}'
            return
        fi
        
        # Check for test project patterns
        local test_patterns=("TEST" "INVALID" "DUMMY" "FAKE" "EXAMPLE")
        for pattern in "${test_patterns[@]}"; do
            if [[ "$project_key" == "$pattern" ]]; then
                echo '{"should_block": true, "action": "ask", "severity": "medium", "reason": "Project key appears to be a test value"}'
                return
            fi
        done
    fi
    
    echo '{"should_block": false, "reason": "Create parameters pass all blocking checks"}'
}

# Check if a parameter has failed historically
check_historical_failures() {
    local server_name="$1"
    local parameter_value="$2"
    local error_log="$ERROR_LOGS_DIR/${server_name}-errors.md"
    
    if [[ -f "$error_log" ]] && grep -q "$parameter_value" "$error_log"; then
        # Parameter found in error log - check frequency
        local failure_count=$(grep -c "$parameter_value" "$error_log")
        if [[ $failure_count -ge 2 ]]; then
            return 0  # Should block (true)
        fi
    fi
    
    return 1  # Don't block (false)
}

# Update blocking patterns based on new error data
update_blocking_patterns() {
    local server_name="$1"
    local error_pattern="$2"
    local frequency="$3"
    
    # For now, log the pattern update
    # In a more sophisticated implementation, this would update the YAML file
    cat >> "$PATTERNS_DIR/pattern-updates.log" << EOF
[$(date '+%Y-%m-%d %H:%M:%S')] PATTERN UPDATE
Server: $server_name
Pattern: $error_pattern
Frequency: $frequency
Action: Added to blocking rules
---
EOF
    
    echo "[Pattern Blocker] Updated blocking patterns for $server_name" >&2
}

# Log blocked calls for analysis
log_blocked_call() {
    local tool_name="$1"
    local tool_input="$2"
    local block_reason="$3"
    
    cat >> "$BLOCKING_LOG" << EOF
[$(date '+%Y-%m-%d %H:%M:%S')] BLOCKED CALL
Tool: $tool_name
Reason: $block_reason
Parameters: $(echo "$tool_input" | head -1 | cut -c1-200)...
Status: Prevented potential error
---
EOF
    
    # Update statistics
    update_blocking_statistics
}

# Update blocking statistics
update_blocking_statistics() {
    local stats_file="$PATTERNS_DIR/blocking-statistics.txt"
    local today=$(date '+%Y-%m-%d')
    
    # Simple statistics tracking
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Blocked call" >> "$stats_file"
    local daily_blocks=$(grep "$today" "$stats_file" 2>/dev/null | wc -l)
    local total_blocks=$(wc -l < "$stats_file" 2>/dev/null || echo 0)
    
    echo "[Pattern Blocker] Daily blocks: $daily_blocks, Total: $total_blocks" >&2
}

# Determine server name from tool name
get_server_name() {
    local tool_name="$1"
    
    case "$tool_name" in
        mcp__MCP_DOCKER__jira_*)
            echo "jira"
            ;;
        mcp__MCP_DOCKER__*notion*|mcp__MCP_DOCKER__API-*)
            echo "notion-api"
            ;;
        mcp__MCP_DOCKER__browser_*)
            echo "browser"
            ;;
        mcp__MCP_DOCKER__*)
            echo "mcp-docker"
            ;;
        *)
            echo "mcp-docker"  # Default fallback
            ;;
    esac
}

# Main execution if called directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    if [[ $# -lt 2 ]]; then
        echo "Usage: $0 <tool_name> <tool_input_json>"
        exit 1
    fi
    
    check_blocking_rules "$1" "$2"
else
    # Sourced by another script - functions available
    initialize_blocked_patterns
fi