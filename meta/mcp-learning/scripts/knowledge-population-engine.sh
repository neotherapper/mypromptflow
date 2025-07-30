#!/bin/bash

# MCP Learning Knowledge Population Engine
# Automatically updates learning templates, usage guides, and patterns from captured data
# Transforms static templates into dynamic, self-updating knowledge bases

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MCP_LEARNING_DIR="$(dirname "$SCRIPT_DIR")"
ERROR_LOGS_DIR="$MCP_LEARNING_DIR/error-logs"
SUCCESS_PATTERNS_DIR="$MCP_LEARNING_DIR/success-patterns"
USAGE_GUIDES_DIR="$MCP_LEARNING_DIR/usage-guides"
PATTERNS_DIR="$MCP_LEARNING_DIR/patterns"

# Main population engine
main() {
    local server_name="$1"
    local operation_mode="${2:-both}"  # "errors", "successes", or "both"
    
    if [[ -z "$server_name" ]]; then
        echo "Usage: $0 <server_name> [operation_mode]"
        echo "Example: $0 jira both"
        exit 1
    fi
    
    echo "[Knowledge Engine] Starting knowledge population for $server_name ($operation_mode mode)"
    
    case "$operation_mode" in
        "errors"|"both")
            populate_from_errors "$server_name"
            ;;
    esac
    
    case "$operation_mode" in
        "successes"|"both")
            populate_from_successes "$server_name"
            ;;
    esac
    
    # Update pattern analysis
    update_pattern_analysis "$server_name"
    
    echo "[Knowledge Engine] Knowledge population completed for $server_name"
}

# Populate knowledge from error patterns
populate_from_errors() {
    local server_name="$1"
    local error_log_file="$ERROR_LOGS_DIR/${server_name}-errors.md"
    local usage_guide_file="$USAGE_GUIDES_DIR/${server_name}-guide.md"
    
    if [[ ! -f "$error_log_file" ]]; then
        echo "[Knowledge Engine] No error log found for $server_name"
        return
    fi
    
    echo "[Knowledge Engine] Analyzing error patterns for $server_name..."
    
    # Extract common error patterns
    local common_errors=(
        "Invalid issue key"
        "Authentication failed" 
        "Bad request"
        "Not found"
        "Timeout"
    )
    
    # Analyze error frequency and create prevention rules
    for error_pattern in "${common_errors[@]}"; do
        local error_count=$(grep -c "$error_pattern" "$error_log_file" 2>/dev/null || echo 0)
        if [[ $error_count -gt 0 ]]; then
            generate_prevention_rule "$server_name" "$error_pattern" "$error_count"
        fi
    done
    
    # Update usage guide with error-based insights
    update_usage_guide_from_errors "$server_name"
}

# Populate knowledge from success patterns
populate_from_successes() {
    local server_name="$1"
    local success_patterns_file="$SUCCESS_PATTERNS_DIR/${server_name}-success-patterns.md"
    
    if [[ ! -f "$success_patterns_file" ]]; then
        echo "[Knowledge Engine] No success patterns found for $server_name"
        return
    fi
    
    echo "[Knowledge Engine] Analyzing success patterns for $server_name..."
    
    # Extract successful patterns
    extract_working_patterns "$server_name"
    
    # Update usage guide with success-based insights
    update_usage_guide_from_successes "$server_name"
}

# Generate prevention rules from error patterns
generate_prevention_rule() {
    local server_name="$1"
    local error_pattern="$2"
    local frequency="$3"
    local patterns_file="$PATTERNS_DIR/common-error-patterns.yaml"
    
    # Create prevention rule based on error pattern
    local prevention_rule=""
    case "$error_pattern" in
        "Invalid issue key")
            prevention_rule="Validate issue key format (PROJECT-NUMBER) before API calls"
            ;;
        "Authentication failed")
            prevention_rule="Verify credentials and permissions before operations"
            ;;
        "Bad request")
            prevention_rule="Validate all required parameters and formats"
            ;;
        "Not found")
            prevention_rule="Confirm resource exists before attempting operations"
            ;;
        "Timeout")
            prevention_rule="Implement appropriate timeout settings and retry logic"
            ;;
    esac
    
    if [[ -n "$prevention_rule" ]]; then
        echo "[Knowledge Engine] Generated prevention rule for '$error_pattern' (frequency: $frequency)"
        # In a more sophisticated implementation, this would update the YAML file
        echo "# Auto-generated prevention rule: $server_name - $error_pattern - frequency: $frequency - $(date)" >> "$PATTERNS_DIR/auto-generated-rules.log"
        echo "# Rule: $prevention_rule" >> "$PATTERNS_DIR/auto-generated-rules.log"
    fi
}

# Extract working patterns from successful operations
extract_working_patterns() {
    local server_name="$1"
    local success_file="$SUCCESS_PATTERNS_DIR/${server_name}-success-patterns.md"
    
    # Extract common success patterns
    local search_operations=$(grep -c "Operation Type.*search" "$success_file" 2>/dev/null || echo 0)
    local retrieve_operations=$(grep -c "Operation Type.*retrieve" "$success_file" 2>/dev/null || echo 0)
    local create_operations=$(grep -c "Operation Type.*create" "$success_file" 2>/dev/null || echo 0)
    local update_operations=$(grep -c "Operation Type.*update" "$success_file" 2>/dev/null || echo 0)
    
    echo "[Knowledge Engine] Success patterns found:"
    echo "  - Search operations: $search_operations"
    echo "  - Retrieve operations: $retrieve_operations"
    echo "  - Create operations: $create_operations"
    echo "  - Update operations: $update_operations"
    
    # Log working patterns
    cat >> "$SUCCESS_PATTERNS_DIR/working-patterns-summary.log" << EOF
# Working patterns analysis for $server_name - $(date)
search_operations: $search_operations
retrieve_operations: $retrieve_operations
create_operations: $create_operations
update_operations: $update_operations
EOF
}

# Update usage guide from error analysis
update_usage_guide_from_errors() {
    local server_name="$1"
    local usage_guide_file="$USAGE_GUIDES_DIR/${server_name}-guide.md"
    local error_log_file="$ERROR_LOGS_DIR/${server_name}-errors.md"
    
    if [[ ! -f "$usage_guide_file" ]]; then
        echo "[Knowledge Engine] Usage guide not found for $server_name"
        return
    fi
    
    # Check if we need to add auto-generated section
    if ! grep -q "## Auto-Generated Insights" "$usage_guide_file"; then
        # Add auto-generated insights section
        cat >> "$usage_guide_file" << EOF

## Auto-Generated Insights

### Error Pattern Analysis (Updated $(date '+%Y-%m-%d'))

**Common Issues Detected:**
EOF
        
        # Add specific error patterns found
        local total_errors=$(grep -c "^## Error #" "$error_log_file" 2>/dev/null || echo 0)
        if [[ $total_errors -gt 0 ]]; then
            echo "- **Total Errors Logged:** $total_errors" >> "$usage_guide_file"
            
            # Analyze error types
            local auth_errors=$(grep -c "Authentication Error" "$error_log_file" 2>/dev/null || echo 0)
            local param_errors=$(grep -c "Parameter Error" "$error_log_file" 2>/dev/null || echo 0)
            local tool_errors=$(grep -c "Tool Error" "$error_log_file" 2>/dev/null || echo 0)
            
            echo "- **Authentication Errors:** $auth_errors" >> "$usage_guide_file"
            echo "- **Parameter Errors:** $param_errors" >> "$usage_guide_file"
            echo "- **Tool Errors:** $tool_errors" >> "$usage_guide_file"
            
            # Generate recommendations
            cat >> "$usage_guide_file" << EOF

**Auto-Generated Recommendations:**
- [ ] Review error patterns in \`$error_log_file\`
- [ ] Focus on preventing most common error type
- [ ] Update pre-flight checklist based on error analysis
- [ ] Consider additional parameter validation

**Last Analysis:** $(date '+%Y-%m-%d %H:%M')
EOF
        fi
        
        echo "[Knowledge Engine] Added auto-generated insights to $server_name usage guide"
    else
        echo "[Knowledge Engine] Auto-generated section already exists in $server_name usage guide"
    fi
}

# Update usage guide from success pattern analysis
update_usage_guide_from_successes() {
    local server_name="$1"
    local usage_guide_file="$USAGE_GUIDES_DIR/${server_name}-guide.md"
    local success_file="$SUCCESS_PATTERNS_DIR/${server_name}-success-patterns.md"
    
    if [[ ! -f "$usage_guide_file" ]] || [[ ! -f "$success_file" ]]; then
        echo "[Knowledge Engine] Required files not found for success analysis"
        return
    fi
    
    # Check if we need to add success patterns section
    if ! grep -q "## Validated Working Patterns" "$usage_guide_file"; then
        local total_successes=$(grep -c "^## Success Pattern #" "$success_file" 2>/dev/null || echo 0)
        
        if [[ $total_successes -gt 0 ]]; then
            cat >> "$usage_guide_file" << EOF

## Validated Working Patterns (Auto-Generated)

### Success Statistics (Updated $(date '+%Y-%m-%d'))
- **Total Successful Operations:** $total_successes
- **Success Rate:** High (operations completing without errors)
- **Pattern Confidence:** Based on actual successful operations

### Confirmed Working Approaches
*These patterns have been validated through successful operations:*

EOF
            
            # Extract specific success patterns
            if grep -q "Issue Key Pattern" "$success_file"; then
                echo "- **Issue Key Formats:** Validated through successful retrievals" >> "$usage_guide_file"
            fi
            
            if grep -q "Search Results" "$success_file"; then
                echo "- **Search Operations:** Confirmed working with various queries" >> "$usage_guide_file"
            fi
            
            if grep -q "Created Issue" "$success_file"; then
                echo "- **Issue Creation:** Validated parameter combinations" >> "$usage_guide_file"
            fi
            
            cat >> "$usage_guide_file" << EOF

**Success Pattern Details:** See \`$success_file\` for complete successful operation logs
**Reliability:** These patterns represent actual working operations
**Last Validation:** $(date '+%Y-%m-%d %H:%M')
EOF
            
            echo "[Knowledge Engine] Added validated working patterns to $server_name usage guide"
        fi
    else
        echo "[Knowledge Engine] Working patterns section already exists in $server_name usage guide"
    fi
}

# Update cross-server pattern analysis
update_pattern_analysis() {
    local server_name="$1"
    local common_patterns_file="$PATTERNS_DIR/common-error-patterns.yaml"
    
    # Update server-specific statistics in common patterns file
    if [[ -f "$common_patterns_file" ]]; then
        local error_count=$(grep -c "^## Error #" "$ERROR_LOGS_DIR/${server_name}-errors.md" 2>/dev/null || echo 0)
        local success_count=$(grep -c "^## Success Pattern #" "$SUCCESS_PATTERNS_DIR/${server_name}-success-patterns.md" 2>/dev/null || echo 0)
        
        # Log pattern analysis
        cat >> "$PATTERNS_DIR/pattern-analysis.log" << EOF
# Pattern analysis update for $server_name - $(date)
total_errors: $error_count
total_successes: $success_count
analysis_date: $(date '+%Y-%m-%d %H:%M')
EOF
        
        echo "[Knowledge Engine] Updated pattern analysis for $server_name (errors: $error_count, successes: $success_count)"
    fi
}

# Run for specific server or all servers
if [[ "$1" == "--all" ]]; then
    for server in jira notion-api browser mcp-docker; do
        main "$server" "both"
    done
else
    main "$@"
fi