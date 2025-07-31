#!/bin/bash

# MCP Parameter Validator - PreToolUse Hook
# Validates and corrects MCP tool parameters before execution
# Returns: {"action": "allow|deny|ask", "reason": "...", "corrected_input": "..."}

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LEARNING_DIR="$(dirname "$SCRIPT_DIR")"

# Parse arguments
SESSION_ID="$1"
TRANSCRIPT_PATH="$2"
TOOL_NAME="$3"
TOOL_INPUT="$4"

# Validation log path
VALIDATION_LOG="$LEARNING_DIR/validation-log.txt"

# Log validation attempt
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Validating $TOOL_NAME" >> "$VALIDATION_LOG"

# Function to validate JIRA tool parameters
validate_parameters() {
    local tool_name="$1"
    local tool_input="$2"
    
    # Basic validation - ensure required fields are present
    case "$tool_name" in
        "mcp__MCP_DOCKER__jira_search")
            # Check for required 'jql' parameter
            if echo "$tool_input" | grep -q '"jql"'; then
                echo "Valid: JQL parameter found"
                return 0
            else
                echo "Invalid: Missing required 'jql' parameter"
                return 1
            fi
            ;;
        "mcp__MCP_DOCKER__jira_get_issue")
            # Check for required 'issue_key' parameter
            if echo "$tool_input" | grep -q '"issue_key"'; then
                echo "Valid: issue_key parameter found"
                return 0
            else
                echo "Invalid: Missing required 'issue_key' parameter"
                return 1
            fi
            ;;
        "mcp__MCP_DOCKER__jira_create_issue")
            # Check for required parameters
            if echo "$tool_input" | grep -q '"project_key"' && echo "$tool_input" | grep -q '"summary"'; then
                echo "Valid: Required parameters found"
                return 0
            else
                echo "Invalid: Missing required 'project_key' or 'summary' parameter"
                return 1
            fi
            ;;
        *)
            echo "Valid: Unknown tool - allowing"
            return 0
            ;;
    esac
}

# Function to apply parameter corrections
correct_parameters() {
    local tool_name="$1"
    local tool_input="$2"
    
    # Apply learned corrections from mcp-parameter-corrector.sh
    if [ -f "$SCRIPT_DIR/mcp-parameter-corrector.sh" ]; then
        # Pass tool_input via stdin to the corrector script
        echo "$tool_input" | bash "$SCRIPT_DIR/mcp-parameter-corrector.sh" "$tool_name"
    else
        echo "$tool_input"
    fi
}

# Main validation logic
main() {
    local corrected_input
    corrected_input=$(correct_parameters "$TOOL_NAME" "$TOOL_INPUT")
    
    # Step 1: Check pattern blocking rules first
    local pattern_blocker_script="$SCRIPT_DIR/mcp-pattern-blocker.sh"
    if [ -f "$pattern_blocker_script" ]; then
        local blocking_result
        blocking_result=$(bash "$pattern_blocker_script" "$TOOL_NAME" "$corrected_input" 2>/dev/null)
        
        # Parse blocking decision
        if echo "$blocking_result" | grep -q '"should_block": true'; then
            local block_action=$(echo "$blocking_result" | grep -o '"action": "[^"]*"' | cut -d'"' -f4)
            local block_reason=$(echo "$blocking_result" | grep -o '"reason": "[^"]*"' | cut -d'"' -f4)
            
            # Return blocking decision
            echo "{\"action\": \"$block_action\", \"reason\": \"Pattern blocker: $block_reason\"}"
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] BLOCKED: $TOOL_NAME - $block_reason" >> "$VALIDATION_LOG"
            return
        fi
    fi
    
    # Step 2: Validate corrected parameters using file-based approach to preserve exit codes
    validate_parameters "$TOOL_NAME" "$corrected_input" > /tmp/validation_output.txt
    local validation_code=$?
    local validation_result=$(cat /tmp/validation_output.txt)
    
    if [ $validation_code -eq 0 ]; then
        # Valid parameters - allow execution
        if [ "$corrected_input" != "$TOOL_INPUT" ]; then
            echo "{\"action\": \"allow\", \"reason\": \"Parameters corrected and validated\", \"corrected_input\": $corrected_input}"
        else
            echo "{\"action\": \"allow\", \"reason\": \"Parameters validated successfully\"}"
        fi
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ALLOWED: $TOOL_NAME - $validation_result" >> "$VALIDATION_LOG"
    else
        # Invalid parameters - deny execution
        echo "{\"action\": \"deny\", \"reason\": \"Parameter validation failed: $validation_result\"}"
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] DENIED: $TOOL_NAME - $validation_result" >> "$VALIDATION_LOG"
    fi
    
    # Clean up temp file
    rm -f /tmp/validation_output.txt
}

# Only run main if script is executed directly (not sourced)
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi