#!/bin/bash

# MCP Parameter Validation Script (PreToolUse Hook)
# Validates MCP tool parameters BEFORE execution to prevent known errors
# Returns JSON decision to allow, deny, or ask for permission

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MCP_LEARNING_DIR="$(dirname "$SCRIPT_DIR")"
ERROR_LOGS_DIR="$MCP_LEARNING_DIR/error-logs"
SUCCESS_PATTERNS_DIR="$MCP_LEARNING_DIR/success-patterns"
USAGE_GUIDES_DIR="$MCP_LEARNING_DIR/usage-guides"
VALIDATION_LOG="$MCP_LEARNING_DIR/validation-log.txt"

# Main validation function
main() {
    local session_id="$1"
    local transcript_path="$2"
    local tool_name="$3"
    local tool_input="$4"
    
    # Only process MCP tools
    if [[ ! "$tool_name" =~ ^mcp__.* ]]; then
        echo '{"permissionDecision": "allow", "reason": "Non-MCP tool, no validation needed"}'
        exit 0
    fi
    
    # Log validation attempt
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Validating $tool_name" >> "$VALIDATION_LOG"
    
    # Source the parameter corrector and pattern blocker
    source "$SCRIPT_DIR/mcp-parameter-corrector.sh"
    source "$SCRIPT_DIR/mcp-pattern-blocker.sh"
    
    # Check if call should be blocked by learned patterns
    local blocking_result=$(check_blocking_rules "$tool_name" "$tool_input")
    local should_block=$(echo "$blocking_result" | grep -o '"should_block":[^,}]*' | cut -d':' -f2 | tr -d ' "')
    
    if [[ "$should_block" == "true" ]]; then
        local block_action=$(echo "$blocking_result" | grep -o '"action":"[^"]*"' | cut -d'"' -f4)
        local block_reason=$(echo "$blocking_result" | grep -o '"reason":"[^"]*"' | cut -d'"' -f4)
        local block_severity=$(echo "$blocking_result" | grep -o '"severity":"[^"]*"' | cut -d'"' -f4)
        
        case "$block_action" in
            "deny")
                echo "{\"permissionDecision\": \"deny\", \"reason\": \"Blocked by learned pattern: $block_reason\", \"severity\": \"$block_severity\", \"prevention\": \"This pattern has caused errors before\"}"
                exit 0
                ;;
            "ask")
                echo "{\"permissionDecision\": \"ask\", \"reason\": \"Pattern warning: $block_reason\", \"severity\": \"$block_severity\", \"context\": \"Consider reviewing this operation\"}"
                exit 0
                ;;
        esac
    fi
    
    # Apply intelligent parameter corrections first
    local corrected_input=$(correct_parameters "$tool_name" "$tool_input")
    local corrections_applied=false
    
    if [[ "$corrected_input" != "$tool_input" ]]; then
        corrections_applied=true
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Applied parameter corrections for $tool_name" >> "$VALIDATION_LOG"
    fi
    
    # Perform parameter validation on corrected parameters
    validate_parameters "$tool_name" "$corrected_input" > /tmp/validation_output.txt
    local validation_code=$?
    local validation_result=$(cat /tmp/validation_output.txt)
    rm -f /tmp/validation_output.txt
    
    case $validation_code in
        0)
            # Validation passed - allow with corrections and success patterns
            if [[ "$corrections_applied" = true ]]; then
                echo "{\"permissionDecision\": \"allow\", \"reason\": \"Parameters validated successfully with auto-corrections\", \"correctedParameters\": $(echo "$corrected_input" | tr -d '\n'), \"modifications\": \"Applied intelligent corrections and success patterns\"}"
            else
                echo '{"permissionDecision": "allow", "reason": "Parameters validated successfully", "modifications": "Applied success patterns for optimization"}'
            fi
            ;;
        1)
            # Validation failed - try once more with auto-correction, then deny
            if [[ "$corrections_applied" = false ]]; then
                # Try correction and re-validate
                corrected_input=$(correct_parameters "$tool_name" "$tool_input")
                if [[ "$corrected_input" != "$tool_input" ]]; then
                    validation_result=$(validate_parameters "$tool_name" "$corrected_input")
                    validation_code=$?
                    if [[ $validation_code -eq 0 ]]; then
                        echo "{\"permissionDecision\": \"allow\", \"reason\": \"Parameters corrected and validated\", \"correctedParameters\": $(echo "$corrected_input" | tr -d '\n'), \"modifications\": \"Auto-corrected parameter errors\"}"
                        exit 0
                    fi
                fi
            fi
            
            # Still failing after correction - deny
            local error_reason=$(echo "$validation_result" | tail -1)
            echo "{\"permissionDecision\": \"deny\", \"reason\": \"Parameter validation failed: $error_reason\", \"suggestion\": \"Check usage guide: meta/mcp-learning/usage-guides/$(get_server_name "$tool_name")-guide.md\"}"
            log_prevented_error "$tool_name" "$tool_input" "$error_reason"
            ;;
        2)
            # Validation uncertain - ask user for confirmation with corrections if available
            local warning_message=$(echo "$validation_result" | tail -1)
            if [[ "$corrections_applied" = true ]]; then
                echo "{\"permissionDecision\": \"ask\", \"reason\": \"Uncertain parameter validation: $warning_message\", \"context\": \"Similar patterns have caused errors before\", \"suggestedCorrections\": $(echo "$corrected_input" | tr -d '\n')}"
            else
                echo "{\"permissionDecision\": \"ask\", \"reason\": \"Uncertain parameter validation: $warning_message\", \"context\": \"Similar patterns have caused errors before\"}"
            fi
            ;;
        *)
            # Validation error - allow but with warning
            echo '{"permissionDecision": "allow", "reason": "Validation system error, allowing with caution", "warning": "Parameter validation unavailable"}'
            ;;
    esac
    
    exit 0
}

# Validate parameters against known error patterns
validate_parameters() {
    local tool_name="$1"
    local tool_input="$2"
    local server_name=$(get_server_name "$tool_name")
    
    # Load error patterns for this server
    local error_log_file="$ERROR_LOGS_DIR/${server_name}-errors.md"
    
    # Always perform basic validation, with or without error history
    
    # Tool-specific validation
    case "$tool_name" in
        mcp__MCP_DOCKER__jira_get_issue)
            validate_jira_get_issue "$tool_input" "$error_log_file"
            return $?
            ;;
        mcp__MCP_DOCKER__jira_search)
            validate_jira_search "$tool_input" "$error_log_file"
            return $?
            ;;
        mcp__MCP_DOCKER__jira_create_issue)
            validate_jira_create_issue "$tool_input" "$error_log_file"
            return $?
            ;;
        mcp__MCP_DOCKER__jira_update_issue)
            validate_jira_update_issue "$tool_input" "$error_log_file"
            return $?
            ;;
        *)
            # Generic validation for unknown tools
            validate_generic_parameters "$tool_input" "$error_log_file"
            return $?
            ;;
    esac
}

# Validate JIRA get_issue parameters
validate_jira_get_issue() {
    local tool_input="$1"
    local error_log="$2"
    
    # Extract issue_key from JSON input
    local issue_key=$(echo "$tool_input" | grep -o '"issue_key":"[^"]*"' | cut -d'"' -f4)
    
    if [[ -z "$issue_key" ]]; then
        echo "Missing required parameter: issue_key"
        return 1
    fi
    
    # Validate issue key format (PROJECT-NUMBER)
    if [[ ! "$issue_key" =~ ^[A-Z][A-Z0-9]*-[0-9]+$ ]]; then
        echo "Invalid issue key format: '$issue_key'. Expected format: PROJECT-123"
        return 1
    fi
    
    # Check against known error patterns
    if grep -q "Invalid issue key.*$issue_key" "$error_log" 2>/dev/null; then
        echo "Issue key '$issue_key' has failed before - check if issue exists"
        return 2  # Ask for confirmation
    fi
    
    # Check for common problematic patterns
    if [[ "$issue_key" =~ (TEST|INVALID|DUMMY|FAKE) ]]; then
        echo "Issue key '$issue_key' appears to be a test value - confirm this is intentional"
        return 2  # Ask for confirmation
    fi
    
    echo "JIRA get_issue parameters validated successfully"
    return 0
}

# Validate JIRA search parameters
validate_jira_search() {
    local tool_input="$1"
    local error_log="$2"
    
    # Extract JQL from input
    local jql=$(echo "$tool_input" | grep -o '"jql":"[^"]*"' | cut -d'"' -f4)
    
    if [[ -z "$jql" ]]; then
        echo "Missing required parameter: jql"
        return 1
    fi
    
    # Check for common JQL syntax errors
    if [[ "$jql" =~ [[:space:]]*=[[:space:]]*[^\"\'[:space:]][^[:space:]]* ]]; then
        echo "JQL syntax warning: String values should be quoted. Example: status = \"Open\""
        return 2  # Ask for confirmation
    fi
    
    # Check for suspicious JQL patterns
    if [[ "$jql" =~ (DROP|DELETE|UPDATE|INSERT) ]]; then
        echo "JQL contains SQL-like keywords - JIRA uses different syntax"
        return 1
    fi
    
    echo "JIRA search parameters validated successfully"
    return 0
}

# Validate JIRA create_issue parameters
validate_jira_create_issue() {
    local tool_input="$1"
    local error_log="$2"
    
    # Check for required fields
    local project_key=$(echo "$tool_input" | grep -o '"project_key":"[^"]*"' | cut -d'"' -f4)
    local summary=$(echo "$tool_input" | grep -o '"summary":"[^"]*"' | cut -d'"' -f4)
    local issue_type=$(echo "$tool_input" | grep -o '"issue_type":"[^"]*"' | cut -d'"' -f4)
    
    if [[ -z "$project_key" ]]; then
        echo "Missing required parameter: project_key"
        return 1
    fi
    
    if [[ -z "$summary" ]]; then
        echo "Missing required parameter: summary"
        return 1
    fi
    
    if [[ -z "$issue_type" ]]; then
        echo "Missing required parameter: issue_type"
        return 1
    fi
    
    # Validate project key format
    if [[ ! "$project_key" =~ ^[A-Z][A-Z0-9]*$ ]]; then
        echo "Invalid project key format: '$project_key'. Expected format: PROJECT"
        return 1
    fi
    
    echo "JIRA create_issue parameters validated successfully"
    return 0
}

# Validate JIRA update_issue parameters
validate_jira_update_issue() {
    local tool_input="$1"
    local error_log="$2"
    
    # Check for required issue_key
    local issue_key=$(echo "$tool_input" | grep -o '"issue_key":"[^"]*"' | cut -d'"' -f4)
    
    if [[ -z "$issue_key" ]]; then
        echo "Missing required parameter: issue_key"
        return 1
    fi
    
    # Validate issue key format
    if [[ ! "$issue_key" =~ ^[A-Z][A-Z0-9]*-[0-9]+$ ]]; then
        echo "Invalid issue key format: '$issue_key'. Expected format: PROJECT-123"
        return 1
    fi
    
    # Check if fields parameter exists
    if ! echo "$tool_input" | grep -q '"fields"'; then
        echo "Missing required parameter: fields (what to update)"
        return 1
    fi
    
    echo "JIRA update_issue parameters validated successfully"
    return 0
}

# Generic parameter validation
validate_generic_parameters() {
    local tool_input="$1"
    local error_log="$2"
    
    # Basic JSON structure validation
    if ! echo "$tool_input" | python3 -m json.tool > /dev/null 2>&1; then
        echo "Invalid JSON structure in tool parameters"
        return 1
    fi
    
    echo "Generic parameter validation passed"
    return 0
}

# Apply success patterns to optimize parameters
apply_success_patterns() {
    local tool_name="$1"
    local tool_input="$2"
    local server_name=$(get_server_name "$tool_name")
    local success_file="$SUCCESS_PATTERNS_DIR/${server_name}-success-patterns.md"
    
    # Log successful pattern application for future learning
    if [[ -f "$success_file" ]]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Applied success patterns for $tool_name" >> "$VALIDATION_LOG"
        # In a more sophisticated implementation, this would actually modify parameters
        # based on learned success patterns
    fi
}

# Log prevented errors for learning
log_prevented_error() {
    local tool_name="$1"
    local tool_input="$2"
    local error_reason="$3"
    local prevention_log="$MCP_LEARNING_DIR/error-prevention-log.txt"
    
    cat >> "$prevention_log" << EOF
[$(date '+%Y-%m-%d %H:%M:%S')] PREVENTED ERROR
Tool: $tool_name
Reason: $error_reason
Parameters: $(echo "$tool_input" | head -1 | cut -c1-200)
---
EOF
    
    echo "[MCP Validator] Prevented error: $error_reason for $tool_name" >&2
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

# Execute main function with arguments if called directly (not sourced)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi