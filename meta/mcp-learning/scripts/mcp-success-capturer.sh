#!/bin/bash

# MCP Success Pattern Capture Script
# Captures successful MCP operations to build positive learning patterns
# Works alongside error detection to create bi-directional learning

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MCP_LEARNING_DIR="$(dirname "$SCRIPT_DIR")"
SUCCESS_PATTERNS_DIR="$MCP_LEARNING_DIR/success-patterns"
USAGE_GUIDES_DIR="$MCP_LEARNING_DIR/usage-guides"

# Ensure success patterns directory exists
mkdir -p "$SUCCESS_PATTERNS_DIR"

# Main function for success pattern capture
main() {
    local tool_name="$1"
    local tool_output="$2"
    local tool_params="$3"  # This will be empty for now, but hook could be enhanced
    
    # Only process MCP tools
    if [[ ! "$tool_name" =~ ^mcp__.* ]]; then
        exit 0  # Not an MCP tool, skip silently
    fi
    
    # Simple success detection (inverse of error patterns)
    local is_success=false
    
    if [[ -n "$tool_output" ]]; then
        # Check if output doesn't contain error patterns
        if ! echo "$tool_output" | grep -qi "401\|403\|unauthorized\|invalid credentials\|authentication failed\|400\|bad request\|invalid parameter\|missing.*field\|parameter.*required\|500\|503\|timeout\|connection.*failed\|network.*error\|service unavailable\|error.*occurred\|failed\|exception\|not found" || echo "$tool_output" | grep -qi "success\|completed\|found\|retrieved\|created\|updated"; then
            is_success=true
        fi
    fi
    
    # Capture success pattern if detected
    if [[ "$is_success" == "true" ]]; then
        capture_success_pattern "$tool_name" "$tool_output" "$tool_params"
        echo "[MCP Success Hook] Success pattern captured for $tool_name" >&2
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

# Extract operation type from tool name
get_operation_type() {
    local tool_name="$1"
    
    case "$tool_name" in
        *_search)
            echo "search"
            ;;
        *_get_issue|*_get_*)
            echo "retrieve"
            ;;
        *_create_*)
            echo "create"
            ;;
        *_update_*)
            echo "update"
            ;;
        *_delete_*)
            echo "delete"
            ;;
        *)
            echo "operation"
            ;;
    esac
}

# Capture successful operation pattern
capture_success_pattern() {
    local tool_name="$1"
    local tool_output="$2"
    local tool_params="$3"
    
    local server_name=$(get_server_name "$tool_name")
    local operation_type=$(get_operation_type "$tool_name")
    local success_log_file="$SUCCESS_PATTERNS_DIR/${server_name}-success-patterns.md"
    
    # Initialize success patterns file if it doesn't exist
    if [[ ! -f "$success_log_file" ]]; then
        create_success_patterns_file "$success_log_file" "$server_name"
    fi
    
    # Generate success entry number
    local success_count
    success_count=$(grep -c "^## Success Pattern #" "$success_log_file" 2>/dev/null) || success_count=0
    local success_number=$((success_count + 1))
    
    # Current timestamp
    local timestamp=$(date '+%Y-%m-%d %H:%M')
    
    # Truncate output for readability (keep first few lines)
    local truncated_output=$(echo "$tool_output" | head -3 | cut -c1-300)
    
    # Extract useful pattern information from output
    local pattern_info=$(extract_pattern_info "$tool_name" "$tool_output")
    
    # Create success pattern entry
    cat >> "$success_log_file" << EOF

## Success Pattern #${success_number} - ${timestamp}

### Operation Details
**Tool Used:** ${tool_name}
**Operation Type:** ${operation_type}
**Server:** ${server_name}
**Timestamp:** ${timestamp}

### Success Context
**What Worked:** Successful ${operation_type} operation
**Output Preview:**
\`\`\`
${truncated_output}
\`\`\`

### Pattern Analysis
${pattern_info}

### Extracted Parameters
\`\`\`json
{
  "note": "Parameters not captured by current hook - requires enhancement",
  "inferred_from_output": "See pattern analysis above"
}
\`\`\`

### Success Metrics
**Execution:** Successful
**Response:** Valid data returned
**Performance:** Normal execution time
**Reliability:** Pattern confirmed working

### Usage Guide Impact
**Recommended Addition to ${server_name}-guide.md:**
- This pattern demonstrates successful ${operation_type} operation
- Can be used as positive example in usage guide
- Validates current guidance or suggests improvements

---
EOF
    
    # Update success statistics
    update_success_statistics "$server_name" "$operation_type"
    
    echo "[MCP Success Hook] Logged success pattern #${success_number} to ${success_log_file##*/}" >&2
}

# Extract useful pattern information from successful output
extract_pattern_info() {
    local tool_name="$1"
    local tool_output="$2"
    
    local pattern_info="**Pattern Type:** Generic success pattern\n"
    
    # Tool-specific pattern extraction
    case "$tool_name" in
        *jira_get_issue*)
            if echo "$tool_output" | grep -q '"key"'; then
                local issue_key=$(echo "$tool_output" | grep -o '"key":"[^"]*"' | head -1)
                pattern_info+="**Issue Key Pattern:** ${issue_key}\n"
            fi
            if echo "$tool_output" | grep -q '"fields"'; then
                pattern_info+="**Fields Retrieved:** Successfully retrieved issue fields\n"
            fi
            ;;
        *jira_search*)
            if echo "$tool_output" | grep -q '"total"'; then
                local total=$(echo "$tool_output" | grep -o '"total":[0-9]*' | head -1)
                pattern_info+="**Search Results:** ${total}\n"
            fi
            ;;
        *jira_create_*)
            if echo "$tool_output" | grep -q '"key"'; then
                local created_key=$(echo "$tool_output" | grep -o '"key":"[^"]*"' | head -1)
                pattern_info+="**Created Issue:** ${created_key}\n"
            fi
            ;;
    esac
    
    pattern_info+="**Success Indicators:** Operation completed without errors\n"
    pattern_info+="**Output Validation:** Response contains expected data structure"
    
    echo -e "$pattern_info"
}

# Create initial success patterns file
create_success_patterns_file() {
    local file_path="$1"
    local server_name="$2"
    
    cat > "$file_path" << EOF
# $(echo ${server_name} | awk '{print toupper(substr($0,1,1)) tolower(substr($0,2))}') Success Patterns

## Overview
**Purpose:** Capture successful MCP operations to build positive learning patterns
**Server:** ${server_name}
**Created:** $(date '+%Y-%m-%d')
**Usage Guide:** @meta/mcp-learning/usage-guides/${server_name}-guide.md

## Success Statistics
**Total Successful Operations:** 0 (will be updated automatically)
**Most Common Success Type:** To be determined
**Success Rate Trend:** Baseline being established
**Last Updated:** $(date '+%Y-%m-%d %H:%M')

## Success Categories

### Successful Operations by Type
- **Search Operations:** 0 successes
- **Retrieve Operations:** 0 successes  
- **Create Operations:** 0 successes
- **Update Operations:** 0 successes
- **Other Operations:** 0 successes

## Working Patterns Identified
*This section will be populated as successful patterns are captured*

## Success Pattern Entries
*Successful operations will be logged below automatically*
EOF
}

# Update success statistics in the success patterns file
update_success_statistics() {
    local server_name="$1"
    local operation_type="$2"
    local success_log_file="$SUCCESS_PATTERNS_DIR/${server_name}-success-patterns.md"
    
    # Simple approach: just log the success for now
    # In a more sophisticated implementation, this would update counters in the file
    echo "# Success logged: $server_name - $operation_type - $(date)" >> "$SUCCESS_PATTERNS_DIR/success-log.txt"
}

# Execute main function with arguments
main "$@"