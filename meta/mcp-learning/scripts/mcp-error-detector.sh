#!/bin/bash

# MCP Error Detection Script for Claude Code Hooks
# Simple post-execution error detection that automatically logs MCP tool errors
# Integrates with existing meta/mcp-learning/ infrastructure

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MCP_LEARNING_DIR="$(dirname "$SCRIPT_DIR")"
ERROR_LOGS_DIR="$MCP_LEARNING_DIR/error-logs"

# Main function for PostToolUse hook
main() {
    local tool_name="$1"
    local tool_output="$2"
    
    # Only process MCP tools
    if [[ ! "$tool_name" =~ ^mcp__.* ]]; then
        exit 0  # Not an MCP tool, skip silently
    fi
    
    # Simple error detection patterns
    local has_error=false
    local error_type="Unknown Error"
    local error_message=""
    
    # Check for common error patterns in tool output
    if [[ -n "$tool_output" ]]; then
        # Authentication errors
        if echo "$tool_output" | grep -qi "401\|403\|unauthorized\|invalid credentials\|authentication failed"; then
            has_error=true
            error_type="Authentication Error"
            error_message="Authentication failure detected"
        # Parameter errors
        elif echo "$tool_output" | grep -qi "400\|bad request\|invalid parameter\|missing.*field\|parameter.*required"; then
            has_error=true
            error_type="Parameter Error" 
            error_message="Parameter validation failure detected"
        # API/Network errors
        elif echo "$tool_output" | grep -qi "500\|503\|timeout\|connection.*failed\|network.*error\|service unavailable"; then
            has_error=true
            error_type="API/Network Error"
            error_message="API or network failure detected"
        # Generic error patterns (avoid false positives)
        elif echo "$tool_output" | grep -qi "error.*occurred\|failed\|exception\|not found" && ! echo "$tool_output" | grep -qi "no error\|successful"; then
            has_error=true
            error_type="Tool Error" 
            error_message="Tool execution error detected"
        fi
    fi
    
    # Log error if detected
    if [[ "$has_error" == "true" ]]; then
        log_mcp_error "$tool_name" "$error_type" "$error_message" "$tool_output"
        echo "[MCP Error Hook] Error detected and logged for $tool_name" >&2
    fi
    
    exit 0  # Always exit successfully to not block workflow
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

# Log error using existing template format
log_mcp_error() {
    local tool_name="$1"
    local error_type="$2"
    local error_message="$3"
    local tool_output="$4"
    
    local server_name=$(get_server_name "$tool_name")
    local error_log_file="$ERROR_LOGS_DIR/${server_name}-errors.md"
    
    # Ensure error log file exists
    if [[ ! -f "$error_log_file" ]]; then
        echo "[MCP Error Hook] Error log file not found: $error_log_file" >&2
        return 1
    fi
    
    # Generate error entry number
    local error_count
    error_count=$(grep -c "^## Error #" "$error_log_file" 2>/dev/null) || error_count=0
    local error_number=$((error_count + 1))
    
    # Current timestamp
    local timestamp=$(date '+%Y-%m-%d %H:%M')
    
    # Truncate output for readability
    local truncated_output=$(echo "$tool_output" | head -5 | cut -c1-200)
    
    # Create error log entry
    cat >> "$error_log_file" << EOF

## Error #${error_number} - ${timestamp}

### Context & Intent
**What I was trying to do:** MCP tool execution (auto-detected)
**User request:** Claude Code MCP tool operation
**Expected outcome:** Successful MCP tool execution

### Technical Details
**MCP Server:** ${server_name}
**Tool Used:** ${tool_name}
**Parameters Used:**
\`\`\`json
{
  "note": "Parameters not captured by hook - requires manual investigation"
}
\`\`\`

### Error Information
**Error Message:** 
\`\`\`
${truncated_output}
\`\`\`

**Error Type:** ${error_type}
**Severity:** Medium (Auto-detected)

### Analysis
**Root Cause:** Auto-detected via pattern matching in tool output
**Missing Information:** Full context and parameters require manual review
**Parameter Issues:** To be investigated through usage guides and patterns

### Resolution Attempts
1. **Automatic Detection:** Error detected and logged by hook → Success
2. **Manual Investigation Required:** Check ${server_name}-guide.md for troubleshooting
3. **Final Resolution:** To be updated after manual troubleshooting

### Lessons Learned
**For Future Use:**
- [ ] Review similar patterns in error logs
- [ ] Check usage guide for known solutions
- [ ] Update prevention strategies if pattern emerges

**Prevention:**
- [ ] Check \`meta/mcp-learning/usage-guides/${server_name}-guide.md\` before using tool
- [ ] Apply known working patterns from previous successes
- [ ] Validate parameters against common error patterns

### Frequency Tracking
**First Occurrence:** ${timestamp}
**Frequency:** 1 time (auto-detected)
**Last Occurrence:** ${timestamp}
**Status:** Unresolved - Requires Manual Investigation

EOF
    
    echo "[MCP Error Hook] Logged error #${error_number} to ${error_log_file##*/}" >&2
}

# Execute main function with arguments
main "$@"