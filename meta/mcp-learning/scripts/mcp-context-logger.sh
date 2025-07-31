#!/bin/bash

# MCP Context Logger
# Captures enhanced context for MCP operations including user intent and task context
# Works with enhanced error logging template for comprehensive error analysis

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MCP_LEARNING_DIR="$(dirname "$SCRIPT_DIR")"
CONTEXT_LOG="$MCP_LEARNING_DIR/mcp-context-log.txt"
SESSION_CONTEXT_FILE="$MCP_LEARNING_DIR/current-session-context.json"

# Session context variables
USER_TASK_GOAL=""
WORKFLOW_STAGE=""
USER_EXPERTISE_LEVEL=""
RELATED_OPERATIONS=()
TIME_CONTEXT=""

# Initialize context logging
initialize_context_logging() {
    if [[ ! -f "$CONTEXT_LOG" ]]; then
        cat > "$CONTEXT_LOG" << 'EOF'
# MCP Context Log
# Captures user intent, task context, and system state for MCP operations
# Format: [TIMESTAMP] [LEVEL] [CONTEXT_TYPE] - [DATA]

EOF
    fi
    
    # Initialize session context
    if [[ ! -f "$SESSION_CONTEXT_FILE" ]]; then
        cat > "$SESSION_CONTEXT_FILE" << 'EOF'
{
  "session_id": "",
  "session_start": "",
  "user_task_goal": "",
  "workflow_stage": "beginning",
  "user_expertise_level": "intermediate",
  "related_operations": [],
  "time_context": "normal",
  "system_state": "normal",
  "previous_errors": [],
  "success_history": []
}
EOF
    fi
}

# Log context information
log_context() {
    local level="$1"
    local context_type="$2"
    local data="$3"
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] [$context_type] - $data" >> "$CONTEXT_LOG"
}

# Start new session context
start_session_context() {
    local user_task_goal="$1"
    local user_expertise="$2"
    local time_context="${3:-normal}"
    
    local session_id="session_$(date '+%Y%m%d_%H%M%S')"
    
    # Update session context file
    cat > "$SESSION_CONTEXT_FILE" << EOF
{
  "session_id": "$session_id",
  "session_start": "$(date '+%Y-%m-%d %H:%M:%S')",
  "user_task_goal": "$user_task_goal",
  "workflow_stage": "beginning",
  "user_expertise_level": "$user_expertise",
  "related_operations": [],
  "time_context": "$time_context",
  "system_state": "normal",
  "previous_errors": [],
  "success_history": []
}
EOF
    
    log_context "INFO" "SESSION_START" "New session: $session_id - Goal: $user_task_goal"
    echo "✅ Session context initialized: $session_id"
}

# Update workflow stage
update_workflow_stage() {
    local new_stage="$1"  # beginning/middle/end
    
    # Update session context
    local temp_file=$(mktemp)
    jq --arg stage "$new_stage" '.workflow_stage = $stage' "$SESSION_CONTEXT_FILE" > "$temp_file"
    mv "$temp_file" "$SESSION_CONTEXT_FILE"
    
    log_context "INFO" "WORKFLOW_STAGE" "Updated to: $new_stage"
}

# Record MCP operation context
record_mcp_operation() {
    local server_name="$1"
    local tool_name="$2"
    local immediate_objective="$3"
    local expected_outcome="$4"
    local parameters="$5"
    
    # Add to related operations in session context
    local temp_file=$(mktemp)
    local parameters_summary=""
    if [[ -n "$parameters" && "$parameters" != "null" ]]; then
        parameters_summary=$(echo "$parameters" | jq -c . 2>/dev/null || echo '{}')
    else
        parameters_summary="{}"
    fi
    
    local operation_entry=$(jq -n \
        --arg timestamp "$(date '+%Y-%m-%d %H:%M:%S')" \
        --arg server "$server_name" \
        --arg tool "$tool_name" \
        --arg objective "$immediate_objective" \
        --arg expected "$expected_outcome" \
        --argjson params "$parameters_summary" \
        '{
            timestamp: $timestamp,
            server: $server,
            tool: $tool,
            objective: $objective,
            expected_outcome: $expected,
            parameters_summary: $params
        }')
    
    jq --argjson op "$operation_entry" '.related_operations += [$op]' "$SESSION_CONTEXT_FILE" > "$temp_file"
    mv "$temp_file" "$SESSION_CONTEXT_FILE"
    
    log_context "INFO" "MCP_OPERATION" "$server_name::$tool_name - $immediate_objective"
}

# Record MCP operation success
record_mcp_success() {
    local server_name="$1"
    local tool_name="$2"
    local outcome="$3"
    
    # Add to success history
    local temp_file=$(mktemp)
    local success_entry=$(jq -n \
        --arg timestamp "$(date '+%Y-%m-%d %H:%M:%S')" \
        --arg server "$server_name" \
        --arg tool "$tool_name" \
        --arg outcome "$outcome" \
        '{
            timestamp: $timestamp,
            server: $server,
            tool: $tool,
            outcome: $outcome
        }')
    
    jq --argjson success "$success_entry" '.success_history += [$success]' "$SESSION_CONTEXT_FILE" > "$temp_file"
    mv "$temp_file" "$SESSION_CONTEXT_FILE"
    
    log_context "SUCCESS" "MCP_OPERATION" "$server_name::$tool_name - Success: $outcome"
}

# Record MCP operation error
record_mcp_error() {
    local server_name="$1"
    local tool_name="$2"
    local error_type="$3"
    local error_summary="$4"
    
    # Add to previous errors
    local temp_file=$(mktemp)
    local error_entry=$(jq -n \
        --arg timestamp "$(date '+%Y-%m-%d %H:%M:%S')" \
        --arg server "$server_name" \
        --arg tool "$tool_name" \
        --arg error_type "$error_type" \
        --arg error_summary "$error_summary" \
        '{
            timestamp: $timestamp,
            server: $server,
            tool: $tool,
            error_type: $error_type,
            error_summary: $error_summary
        }')
    
    jq --argjson error "$error_entry" '.previous_errors += [$error]' "$SESSION_CONTEXT_FILE" > "$temp_file"
    mv "$temp_file" "$SESSION_CONTEXT_FILE"
    
    log_context "ERROR" "MCP_OPERATION" "$server_name::$tool_name - Error: $error_type"
}

# Get current session context for error logging
get_session_context_for_error() {
    if [[ -f "$SESSION_CONTEXT_FILE" ]]; then
        echo "=== Current Session Context ==="
        echo "**User Task Goal:** $(jq -r '.user_task_goal' "$SESSION_CONTEXT_FILE")"
        echo "**Workflow Stage:** $(jq -r '.workflow_stage' "$SESSION_CONTEXT_FILE")"
        echo "**User Expertise Level:** $(jq -r '.user_expertise_level' "$SESSION_CONTEXT_FILE")"
        echo "**Time Context:** $(jq -r '.time_context' "$SESSION_CONTEXT_FILE")"
        echo ""
        
        local related_ops_count=$(jq '.related_operations | length' "$SESSION_CONTEXT_FILE")
        if [[ "$related_ops_count" -gt 0 ]]; then
            echo "**Related Operations (Recent):**"
            jq -r '.related_operations[-3:] | .[] | "- " + .timestamp + ": " + .server + "::" + .tool + " - " + .objective' "$SESSION_CONTEXT_FILE"
            echo ""
        fi
        
        local prev_errors_count=$(jq '.previous_errors | length' "$SESSION_CONTEXT_FILE")
        if [[ "$prev_errors_count" -gt 0 ]]; then
            echo "**Previous Errors in Session:**"
            jq -r '.previous_errors[-2:] | .[] | "- " + .timestamp + ": " + .server + "::" + .tool + " - " + .error_type' "$SESSION_CONTEXT_FILE"
            echo ""
        fi
        
        local success_count=$(jq '.success_history | length' "$SESSION_CONTEXT_FILE")
        if [[ "$success_count" -gt 0 ]]; then
            echo "**Recent Successes:**"
            jq -r '.success_history[-2:] | .[] | "- " + .timestamp + ": " + .server + "::" + .tool + " - " + .outcome' "$SESSION_CONTEXT_FILE"
            echo ""
        fi
        
        echo "=== End Session Context ==="
    else
        echo "No session context available"
    fi
}

# Generate enhanced error context for logging
generate_enhanced_error_context() {
    local server_name="$1"
    local tool_name="$2"
    local immediate_objective="$3"
    local error_message="$4"
    local parameters="$5"
    
    echo "=== Enhanced Context for Error Logging ==="
    echo ""
    
    # Get session context
    get_session_context_for_error
    
    echo "**Immediate Objective:** $immediate_objective"
    echo "**Server:** $server_name"
    echo "**Tool:** $tool_name"
    echo "**Timestamp:** $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    
    echo "**Parameters Used:**"
    echo '```json'
    echo "$parameters" | jq . 2>/dev/null || echo "$parameters"
    echo '```'
    echo ""
    
    echo "**Error Message:**"
    echo '```'
    echo "$error_message"
    echo '```'
    echo ""
    
    # Suggest context for enhanced logging
    echo "**Suggested Context Analysis:**"
    echo "- **User Action Analysis:** Was this a reasonable thing to attempt given the current workflow stage?"
    echo "- **Parameter Source Analysis:** Were these parameters user-provided, auto-generated, or from a template?"
    echo "- **Timing Analysis:** Is this error related to system state, API availability, or user workflow timing?"
    echo "- **Pattern Analysis:** Does this error correlate with previous errors or system conditions?"
    echo ""
    
    echo "=== End Enhanced Context ==="
}

# Analyze session patterns for insights
analyze_session_patterns() {
    if [[ ! -f "$SESSION_CONTEXT_FILE" ]]; then
        echo "No session context to analyze"
        return 1
    fi
    
    echo "=== Session Pattern Analysis ==="
    echo ""
    
    local session_id=$(jq -r '.session_id' "$SESSION_CONTEXT_FILE")
    local session_start=$(jq -r '.session_start' "$SESSION_CONTEXT_FILE")
    local task_goal=$(jq -r '.user_task_goal' "$SESSION_CONTEXT_FILE")
    
    echo "**Session:** $session_id"
    echo "**Started:** $session_start"
    echo "**Task Goal:** $task_goal"
    echo ""
    
    local total_operations=$(jq '.related_operations | length' "$SESSION_CONTEXT_FILE")
    local total_errors=$(jq '.previous_errors | length' "$SESSION_CONTEXT_FILE")
    local total_successes=$(jq '.success_history | length' "$SESSION_CONTEXT_FILE")
    
    echo "**Session Statistics:**"
    echo "- Total Operations: $total_operations"
    echo "- Errors: $total_errors"
    echo "- Successes: $total_successes"
    
    if [[ "$total_operations" -gt 0 ]]; then
        local success_rate=$((($total_successes * 100) / $total_operations))
        echo "- Success Rate: $success_rate%"
    fi
    echo ""
    
    # Pattern insights
    if [[ "$total_errors" -gt 0 ]]; then
        echo "**Error Patterns:**"
        jq -r '.previous_errors | group_by(.server) | .[] | "- " + .[0].server + ": " + (length | tostring) + " errors"' "$SESSION_CONTEXT_FILE"
        echo ""
    fi
    
    if [[ "$total_operations" -gt 1 ]]; then
        echo "**Server Usage Pattern:**"
        jq -r '.related_operations | group_by(.server) | .[] | "- " + .[0].server + ": " + (length | tostring) + " operations"' "$SESSION_CONTEXT_FILE"
        echo ""
    fi
    
    echo "=== End Pattern Analysis ==="
}

# Update system state
update_system_state() {
    local new_state="$1"  # normal/degraded/maintenance/high_load
    
    local temp_file=$(mktemp)
    jq --arg state "$new_state" '.system_state = $state' "$SESSION_CONTEXT_FILE" > "$temp_file"
    mv "$temp_file" "$SESSION_CONTEXT_FILE"
    
    log_context "INFO" "SYSTEM_STATE" "Updated to: $new_state"
}

# Main execution
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    initialize_context_logging
    
    case "${1:-help}" in
        "start-session")
            if [[ $# -lt 2 ]]; then
                echo "Usage: $0 start-session <task_goal> [expertise_level] [time_context]"
                echo "Example: $0 start-session 'Create JIRA tickets for project planning' intermediate normal"
                exit 1
            fi
            start_session_context "$2" "${3:-intermediate}" "${4:-normal}"
            ;;
        "record-operation")
            if [[ $# -lt 5 ]]; then
                echo "Usage: $0 record-operation <server> <tool> <objective> <expected_outcome> [parameters]"
                exit 1
            fi
            record_mcp_operation "$2" "$3" "$4" "$5" "$6"
            ;;
        "record-success")
            if [[ $# -lt 4 ]]; then
                echo "Usage: $0 record-success <server> <tool> <outcome>"
                exit 1
            fi
            record_mcp_success "$2" "$3" "$4"
            ;;
        "record-error")
            if [[ $# -lt 5 ]]; then
                echo "Usage: $0 record-error <server> <tool> <error_type> <error_summary>"
                exit 1
            fi
            record_mcp_error "$2" "$3" "$4" "$5"
            ;;
        "generate-error-context")
            if [[ $# -lt 5 ]]; then
                echo "Usage: $0 generate-error-context <server> <tool> <objective> <error_message> [parameters]"
                exit 1
            fi
            generate_enhanced_error_context "$2" "$3" "$4" "$5" "$6"
            ;;
        "update-stage")
            if [[ $# -lt 2 ]]; then
                echo "Usage: $0 update-stage <beginning|middle|end>"
                exit 1
            fi
            update_workflow_stage "$2"
            ;;
        "analyze-patterns")
            analyze_session_patterns
            ;;
        "get-context")
            get_session_context_for_error
            ;;
        "help"|*)
            echo "MCP Context Logger"
            echo "Captures enhanced context for MCP operations and error analysis"
            echo ""
            echo "Usage:"
            echo "  $0 start-session <goal> [expertise] [time]     - Start new session context"
            echo "  $0 record-operation <server> <tool> <obj> <exp> [params] - Record MCP operation"
            echo "  $0 record-success <server> <tool> <outcome>    - Record successful operation"
            echo "  $0 record-error <server> <tool> <type> <summary> - Record error"
            echo "  $0 generate-error-context <server> <tool> <obj> <error> [params] - Generate error context"
            echo "  $0 update-stage <stage>                        - Update workflow stage"
            echo "  $0 analyze-patterns                            - Analyze session patterns"
            echo "  $0 get-context                                 - Get current context"
            echo ""
            echo "Examples:"
            echo "  $0 start-session 'Create JIRA sprint' intermediate normal"
            echo "  $0 record-operation jira jira_search 'Find open issues' 'Get issue list' '{\"jql\":\"status=Open\"}'"
            echo "  $0 record-success jira jira_search 'Found 15 open issues'"
            echo "  $0 record-error jira jira_search 'JQL Error' 'Invalid syntax in query'"
            ;;
    esac
else
    # Sourced by another script - functions available
    initialize_context_logging
fi