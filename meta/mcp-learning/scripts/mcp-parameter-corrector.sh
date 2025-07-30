#!/bin/bash

# MCP Parameter Auto-Correction Engine
# Automatically fixes common parameter mistakes based on learned patterns
# Works with the parameter validator to provide intelligent corrections

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MCP_LEARNING_DIR="$(dirname "$SCRIPT_DIR")"
SUCCESS_PATTERNS_DIR="$MCP_LEARNING_DIR/success-patterns"
ERROR_LOGS_DIR="$MCP_LEARNING_DIR/error-logs"
CORRECTIONS_LOG="$MCP_LEARNING_DIR/parameter-corrections-log.txt"

# Main correction function
correct_parameters() {
    local tool_name="$1"
    local tool_input="$2"
    local server_name=$(get_server_name "$tool_name")
    
    # Initialize correction tracking
    local corrections_made=false
    local corrected_input="$tool_input"
    local correction_notes=""
    
    # Tool-specific corrections
    case "$tool_name" in
        mcp__MCP_DOCKER__jira_get_issue)
            corrected_input=$(correct_jira_get_issue "$corrected_input")
            if [[ "$corrected_input" != "$tool_input" ]]; then
                corrections_made=true
                correction_notes="$correction_notes\n- Fixed JIRA issue key format"
            fi
            ;;
        mcp__MCP_DOCKER__jira_search)
            corrected_input=$(correct_jira_search "$corrected_input")
            if [[ "$corrected_input" != "$tool_input" ]]; then
                corrections_made=true
                correction_notes="$correction_notes\n- Fixed JQL syntax and formatting"
            fi
            ;;
        mcp__MCP_DOCKER__jira_create_issue)
            corrected_input=$(correct_jira_create_issue "$corrected_input")
            if [[ "$corrected_input" != "$tool_input" ]]; then
                corrections_made=true
                correction_notes="$correction_notes\n- Enhanced issue creation parameters"
            fi
            ;;
        mcp__MCP_DOCKER__jira_update_issue)
            corrected_input=$(correct_jira_update_issue "$corrected_input")
            if [[ "$corrected_input" != "$tool_input" ]]; then
                corrections_made=true
                correction_notes="$correction_notes\n- Optimized update parameters"
            fi
            ;;
    esac
    
    # Apply success patterns as smart defaults
    corrected_input=$(apply_smart_defaults "$tool_name" "$corrected_input")
    if [[ "$corrected_input" != "$([ "$corrections_made" = true ] && echo "$tool_input" || echo "$corrected_input")" ]]; then
        corrections_made=true
        correction_notes="$correction_notes\n- Applied learned success patterns"
    fi
    
    # Log corrections if any were made
    if [[ "$corrections_made" = true ]]; then
        log_correction "$tool_name" "$tool_input" "$corrected_input" "$correction_notes"
    fi
    
    echo "$corrected_input"
}

# Correct JIRA get_issue parameters
correct_jira_get_issue() {
    local input="$1"
    local corrected="$input"
    
    # Extract and fix issue key
    local issue_key=$(echo "$input" | grep -o '"issue_key":"[^"]*"' | cut -d'"' -f4)
    
    if [[ -n "$issue_key" ]]; then
        local fixed_key="$issue_key"
        
        # Convert lowercase to uppercase (common mistake)
        if [[ "$issue_key" =~ ^[a-z] ]]; then
            fixed_key=$(echo "$issue_key" | tr '[:lower:]' '[:upper:]')
        fi
        
        # Fix missing dash (e.g., "PROJ123" -> "PROJ-123")
        if [[ "$fixed_key" =~ ^[A-Z]+[0-9]+$ ]]; then
            fixed_key=$(echo "$fixed_key" | sed 's/\([A-Z]\+\)\([0-9]\+\)/\1-\2/')
        fi
        
        # Apply correction if needed
        if [[ "$fixed_key" != "$issue_key" ]]; then
            corrected=$(echo "$corrected" | sed "s/\"issue_key\":\"$issue_key\"/\"issue_key\":\"$fixed_key\"/")
        fi
    fi
    
    # Add commonly needed fields if missing
    if ! echo "$corrected" | grep -q '"fields"'; then
        # Add default fields based on success patterns
        corrected=$(echo "$corrected" | sed 's/}$/,"fields":"summary,status,assignee,priority,created,updated"}/')
    fi
    
    echo "$corrected"
}

# Correct JIRA search parameters
correct_jira_search() {
    local input="$1"
    local corrected="$input"
    
    # Extract and fix JQL
    local jql=$(echo "$input" | grep -o '"jql":"[^"]*"' | cut -d'"' -f4)
    
    if [[ -n "$jql" ]]; then
        local fixed_jql="$jql"
        
        # Add quotes around unquoted string values
        # Pattern: field = value (without quotes) -> field = "value"
        fixed_jql=$(echo "$fixed_jql" | sed 's/\([[:alpha:]_][[:alnum:]_]*\)[[:space:]]*=[[:space:]]*\([^"'\''[:space:]][^[:space:]]*\)/\1 = "\2"/g')
        
        # Fix common field name mistakes
        fixed_jql=$(echo "$fixed_jql" | sed 's/\bassignee[[:space:]]*=[[:space:]]*currentuser()/assignee = currentUser()/gi')
        fixed_jql=$(echo "$fixed_jql" | sed 's/\bstatus[[:space:]]*=[[:space:]]*open/status = "Open"/gi')
        
        # Apply correction if needed
        if [[ "$fixed_jql" != "$jql" ]]; then
            corrected=$(echo "$corrected" | sed "s|\"jql\":\"$jql\"|\"jql\":\"$fixed_jql\"|")
        fi
    fi
    
    # Add default limit if missing (prevent large result sets)
    if ! echo "$corrected" | grep -q '"limit"'; then
        corrected=$(echo "$corrected" | sed 's/}$/,"limit":20}/')
    fi
    
    # Add essential fields if missing
    if ! echo "$corrected" | grep -q '"fields"'; then
        corrected=$(echo "$corrected" | sed 's/}$/,"fields":"summary,status,assignee,priority,created"}/')
    fi
    
    echo "$corrected"
}

# Correct JIRA create_issue parameters
correct_jira_create_issue() {
    local input="$1"
    local corrected="$input"
    
    # Extract project key and fix case
    local project_key=$(echo "$input" | grep -o '"project_key":"[^"]*"' | cut -d'"' -f4)
    if [[ -n "$project_key" && "$project_key" =~ ^[a-z] ]]; then
        local fixed_project_key=$(echo "$project_key" | tr '[:lower:]' '[:upper:]')
        corrected=$(echo "$corrected" | sed "s/\"project_key\":\"$project_key\"/\"project_key\":\"$fixed_project_key\"/")
    fi
    
    # Add default issue type if missing
    if ! echo "$corrected" | grep -q '"issue_type"'; then
        corrected=$(echo "$corrected" | sed 's/}$/,"issue_type":"Task"}/')
    fi
    
    # Add default priority if missing (learned from success patterns)
    if ! echo "$corrected" | grep -q '"priority"' && ! echo "$corrected" | grep -q '"additional_fields"'; then
        corrected=$(echo "$corrected" | sed 's/}$/,"additional_fields":{"priority":{"name":"Medium"}}}/')
    fi
    
    echo "$corrected"
}

# Correct JIRA update_issue parameters
correct_jira_update_issue() {
    local input="$1"
    local corrected="$input"
    
    # Fix issue key format (same as get_issue)
    local issue_key=$(echo "$input" | grep -o '"issue_key":"[^"]*"' | cut -d'"' -f4)
    
    if [[ -n "$issue_key" ]]; then
        local fixed_key="$issue_key"
        
        # Convert lowercase to uppercase
        if [[ "$issue_key" =~ ^[a-z] ]]; then
            fixed_key=$(echo "$issue_key" | tr '[:lower:]' '[:upper:]')
        fi
        
        # Fix missing dash
        if [[ "$fixed_key" =~ ^[A-Z]+[0-9]+$ ]]; then
            fixed_key=$(echo "$fixed_key" | sed 's/\([A-Z]\+\)\([0-9]\+\)/\1-\2/')
        fi
        
        # Apply correction if needed
        if [[ "$fixed_key" != "$issue_key" ]]; then
            corrected=$(echo "$corrected" | sed "s/\"issue_key\":\"$issue_key\"/\"issue_key\":\"$fixed_key\"/")
        fi
    fi
    
    echo "$corrected"
}

# Apply smart defaults based on success patterns
apply_smart_defaults() {
    local tool_name="$1"
    local input="$2"
    local server_name=$(get_server_name "$tool_name")
    local success_file="$SUCCESS_PATTERNS_DIR/${server_name}-success-patterns.md"
    
    # If no success patterns available, return unchanged
    if [[ ! -f "$success_file" ]]; then
        echo "$input"
        return
    fi
    
    local enhanced_input="$input"
    
    # Apply tool-specific smart defaults based on success patterns
    case "$tool_name" in
        mcp__MCP_DOCKER__jira_get_issue)
            # Add expand parameter for rendered fields if commonly successful
            if grep -q "renderedFields" "$success_file" && ! echo "$enhanced_input" | grep -q '"expand"'; then
                enhanced_input=$(echo "$enhanced_input" | sed 's/}$/,"expand":"renderedFields"}/')
            fi
            ;;
        mcp__MCP_DOCKER__jira_search)
            # Add sorting for consistent results if pattern shows success
            if grep -q "ORDER BY" "$success_file" && ! echo "$enhanced_input" | grep -qi "order by"; then
                local jql=$(echo "$enhanced_input" | grep -o '"jql":"[^"]*"' | cut -d'"' -f4)
                if [[ -n "$jql" && ! "$jql" =~ ORDER[[:space:]]+BY ]]; then
                    local enhanced_jql="$jql ORDER BY created DESC"
                    enhanced_input=$(echo "$enhanced_input" | sed "s|\"jql\":\"$jql\"|\"jql\":\"$enhanced_jql\"|")
                fi
            fi
            ;;
    esac
    
    echo "$enhanced_input"
}

# Log parameter corrections for learning
log_correction() {
    local tool_name="$1"
    local original_input="$2"
    local corrected_input="$3"
    local correction_notes="$4"
    
    cat >> "$CORRECTIONS_LOG" << EOF
[$(date '+%Y-%m-%d %H:%M:%S')] PARAMETER CORRECTION
Tool: $tool_name
Corrections Applied:$(echo -e "$correction_notes")
Original: $(echo "$original_input" | head -1 | cut -c1-150)...
Corrected: $(echo "$corrected_input" | head -1 | cut -c1-150)...
---
EOF
    
    echo "[MCP Corrector] Applied parameter corrections for $tool_name" >&2
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

# Main execution - can be called from validator or standalone
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    # Called directly - expect parameters
    if [[ $# -lt 2 ]]; then
        echo "Usage: $0 <tool_name> <tool_input_json>"
        exit 1
    fi
    
    correct_parameters "$1" "$2"
else
    # Sourced by another script - functions available
    :
fi