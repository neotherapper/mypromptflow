#!/bin/bash

# MCP Parameter Format Validator
# Validates parameter formats using learned patterns and common validation rules
# Integrates with pre-flight validator for comprehensive parameter checking

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MCP_LEARNING_DIR="$(dirname "$SCRIPT_DIR")"
PATTERNS_DIR="$MCP_LEARNING_DIR/patterns"
VALIDATION_PATTERNS_FILE="$PATTERNS_DIR/parameter-validation-patterns.yaml"
FORMAT_VALIDATION_LOG="$MCP_LEARNING_DIR/parameter-format-validation.log"

# Validation state
FORMAT_ERRORS=()
FORMAT_WARNINGS=()
FORMAT_CORRECTIONS=()

# Initialize format validation logging
initialize_format_logging() {
    if [[ ! -f "$FORMAT_VALIDATION_LOG" ]]; then
        cat > "$FORMAT_VALIDATION_LOG" << 'EOF'
# MCP Parameter Format Validation Log
# Tracks parameter format validation results and auto-corrections
# Format: [TIMESTAMP] [LEVEL] [SERVER] [PARAMETER] [VALIDATION] - [RESULT]

EOF
    fi
}

# Log format validation result
log_format_validation() {
    local level="$1"
    local server="$2"
    local parameter="$3"
    local validation="$4"
    local result="$5"
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] [$server] [$parameter] [$validation] - $result" >> "$FORMAT_VALIDATION_LOG"
}

# Main parameter format validation
validate_parameter_formats() {
    local server_name="$1"
    local tool_name="$2"
    local parameters="$3"  # JSON string
    
    echo "[Format Validator] Starting parameter format validation..."
    
    # Initialize validation state
    FORMAT_ERRORS=()
    FORMAT_WARNINGS=()
    FORMAT_CORRECTIONS=()
    
    # Parse parameters JSON
    if [[ -z "$parameters" || "$parameters" == "null" || "$parameters" == "{}" ]]; then
        log_format_validation "INFO" "$server_name" "empty" "basic_check" "No parameters to validate"
        return 0
    fi
    
    # Validate JSON format first
    if ! echo "$parameters" | jq . > /dev/null 2>&1; then
        FORMAT_ERRORS+=("Invalid JSON format in parameters")
        log_format_validation "ERROR" "$server_name" "json" "format_check" "Invalid JSON format"
        return 1
    fi
    
    # Run server-specific format validation
    case "$server_name" in
        "jira")
            validate_jira_parameter_formats "$parameters"
            ;;
        "notion-api")
            validate_notion_parameter_formats "$parameters"
            ;;
        "browser")
            validate_browser_parameter_formats "$parameters"
            ;;
        "mcp-docker")
            validate_mcp_docker_parameter_formats "$parameters"
            ;;
    esac
    
    # Run universal format validations
    validate_universal_parameter_formats "$server_name" "$parameters"
    
    # Generate format validation report
    generate_format_validation_report "$server_name" "$tool_name"
    
    # Return validation result
    if [[ ${#FORMAT_ERRORS[@]} -eq 0 ]]; then
        return 0
    else
        return 1
    fi
}

# JIRA parameter format validation
validate_jira_parameter_formats() {
    local parameters="$1"
    
    # Issue Key Format Validation (Critical)
    local issue_key=$(echo "$parameters" | jq -r '.issue_key // empty' 2>/dev/null)
    if [[ -n "$issue_key" ]]; then
        if [[ "$issue_key" =~ ^[A-Z]+-[0-9]+$ ]]; then
            log_format_validation "PASS" "jira" "issue_key" "format_check" "Valid format: $issue_key"
        else
            FORMAT_ERRORS+=("Invalid issue_key format: '$issue_key'. Must be PROJECT-NUMBER (e.g., SCRUM-123)")
            log_format_validation "ERROR" "jira" "issue_key" "format_check" "Invalid format: $issue_key"
            
            # Attempt auto-correction
            if [[ "$issue_key" =~ ^[a-z]+-[0-9]+$ ]]; then
                local corrected=$(echo "$issue_key" | tr '[:lower:]' '[:upper:]')
                FORMAT_CORRECTIONS+=("issue_key: '$issue_key' → '$corrected' (uppercase correction)")
                log_format_validation "CORRECTION" "jira" "issue_key" "auto_fix" "Suggested: $corrected"
            fi
        fi
    fi
    
    # Project Key Format Validation
    local project_key=$(echo "$parameters" | jq -r '.project_key // empty' 2>/dev/null)
    if [[ -n "$project_key" ]]; then
        if [[ "$project_key" =~ ^[A-Z][A-Z0-9]*$ ]]; then
            log_format_validation "PASS" "jira" "project_key" "format_check" "Valid format: $project_key"
        else
            FORMAT_ERRORS+=("Invalid project_key format: '$project_key'. Must be uppercase letters/numbers starting with letter")
            log_format_validation "ERROR" "jira" "project_key" "format_check" "Invalid format: $project_key"
            
            # Attempt auto-correction
            if [[ "$project_key" =~ ^[a-z][a-z0-9]*$ ]]; then
                local corrected=$(echo "$project_key" | tr '[:lower:]' '[:upper:]')
                FORMAT_CORRECTIONS+=("project_key: '$project_key' → '$corrected' (uppercase correction)")
                log_format_validation "CORRECTION" "jira" "project_key" "auto_fix" "Suggested: $corrected"
            fi
        fi
    fi
    
    # JQL Basic Syntax Validation
    local jql=$(echo "$parameters" | jq -r '.jql // empty' 2>/dev/null)
    if [[ -n "$jql" ]]; then
        # Check for common JQL syntax issues
        if [[ "$jql" == *"="* && ! "$jql" == *" = "* ]]; then
            FORMAT_WARNINGS+=("JQL may need spaces around '=' operator: '$jql'")
            log_format_validation "WARN" "jira" "jql" "syntax_check" "Missing spaces around equals"
        fi
        
        if [[ "$jql" =~ [A-Z]+ ]] && [[ ! "$jql" =~ (AND|OR|IN|NOT) ]]; then
            log_format_validation "PASS" "jira" "jql" "basic_syntax" "Basic syntax appears valid"
        fi
    fi
    
    # Fields Parameter Validation
    local fields=$(echo "$parameters" | jq -r '.fields // empty' 2>/dev/null)
    if [[ -n "$fields" ]]; then
        # Check for proper comma separation
        if [[ "$fields" == *","* && "$fields" == *", "* ]]; then
            log_format_validation "PASS" "jira" "fields" "format_check" "Properly formatted field list"
        elif [[ "$fields" == *","* ]]; then
            FORMAT_WARNINGS+=("Fields list should use spaces after commas: '$fields'")
            local corrected=$(echo "$fields" | sed 's/,/, /g')
            FORMAT_CORRECTIONS+=("fields: '$fields' → '$corrected' (space formatting)")
            log_format_validation "CORRECTION" "jira" "fields" "auto_fix" "Suggested: $corrected"
        fi
    fi
    
    # Pagination Parameters
    validate_pagination_parameters "jira" "$parameters"
}

# Notion API parameter format validation
validate_notion_parameter_formats() {
    local parameters="$1"
    
    # Page ID Format Validation
    local page_id=$(echo "$parameters" | jq -r '.page_id // empty' 2>/dev/null)
    if [[ -n "$page_id" ]]; then
        if [[ "$page_id" =~ ^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$ ]] || [[ "$page_id" =~ ^[0-9a-f]{32}$ ]]; then
            log_format_validation "PASS" "notion-api" "page_id" "format_check" "Valid UUID format"
        else
            FORMAT_ERRORS+=("Invalid page_id format: '$page_id'. Must be UUID format")
            log_format_validation "ERROR" "notion-api" "page_id" "format_check" "Invalid UUID format: $page_id"
            
            # Attempt auto-correction for 32-char hex without hyphens
            if [[ "$page_id" =~ ^[0-9a-f]{32}$ ]]; then
                local corrected="${page_id:0:8}-${page_id:8:4}-${page_id:12:4}-${page_id:16:4}-${page_id:20:12}"
                FORMAT_CORRECTIONS+=("page_id: '$page_id' → '$corrected' (UUID formatting)")
                log_format_validation "CORRECTION" "notion-api" "page_id" "auto_fix" "Suggested: $corrected"
            fi
        fi
    fi
    
    # Database ID Format Validation
    local database_id=$(echo "$parameters" | jq -r '.database_id // empty' 2>/dev/null)
    if [[ -n "$database_id" ]]; then
        if [[ "$database_id" =~ ^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$ ]] || [[ "$database_id" =~ ^[0-9a-f]{32}$ ]]; then
            log_format_validation "PASS" "notion-api" "database_id" "format_check" "Valid UUID format"
        else
            FORMAT_ERRORS+=("Invalid database_id format: '$database_id'. Must be UUID format")
            log_format_validation "ERROR" "notion-api" "database_id" "format_check" "Invalid UUID format: $database_id"
        fi
    fi
    
    # Rich Text Structure Validation (Basic)
    if echo "$parameters" | jq -e '.rich_text' > /dev/null 2>&1; then
        local rich_text_valid=$(echo "$parameters" | jq -e '.rich_text | type == "array"' 2>/dev/null)
        if [[ "$rich_text_valid" == "true" ]]; then
            log_format_validation "PASS" "notion-api" "rich_text" "structure_check" "Valid array structure"
        else
            FORMAT_ERRORS+=("rich_text must be an array of rich text objects")
            log_format_validation "ERROR" "notion-api" "rich_text" "structure_check" "Invalid structure: not an array"
        fi
    fi
}

# Browser automation parameter format validation
validate_browser_parameter_formats() {
    local parameters="$1"
    
    # URL Format Validation
    local url=$(echo "$parameters" | jq -r '.url // empty' 2>/dev/null)
    if [[ -n "$url" ]]; then
        if [[ "$url" =~ ^https?://[a-zA-Z0-9._-]+\.[a-zA-Z]{2,}(/.*)?$ ]]; then
            log_format_validation "PASS" "browser" "url" "format_check" "Valid URL format"
        else
            FORMAT_ERRORS+=("Invalid URL format: '$url'. Must be valid HTTP/HTTPS URL")
            log_format_validation "ERROR" "browser" "url" "format_check" "Invalid URL format: $url"
            
            # Attempt auto-correction for missing protocol
            if [[ "$url" =~ ^[a-zA-Z0-9._-]+\.[a-zA-Z]{2,}(/.*)?$ ]]; then
                local corrected="https://$url"
                FORMAT_CORRECTIONS+=("url: '$url' → '$corrected' (added HTTPS protocol)")
                log_format_validation "CORRECTION" "browser" "url" "auto_fix" "Suggested: $corrected"
            fi
        fi
    fi
    
    # Element Reference Validation
    local ref=$(echo "$parameters" | jq -r '.ref // empty' 2>/dev/null)
    if [[ -n "$ref" ]]; then
        if [[ ${#ref} -gt 0 ]]; then
            log_format_validation "PASS" "browser" "ref" "presence_check" "Element reference present"
        else
            FORMAT_ERRORS+=("Element reference (ref) cannot be empty")
            log_format_validation "ERROR" "browser" "ref" "presence_check" "Empty reference"
        fi
    fi
    
    # Element Description Validation
    local element=$(echo "$parameters" | jq -r '.element // empty' 2>/dev/null)
    if [[ -n "$element" ]]; then
        if [[ ${#element} -ge 3 ]]; then
            log_format_validation "PASS" "browser" "element" "length_check" "Adequate description length"
        else
            FORMAT_WARNINGS+=("Element description is very short: '$element'. Consider more descriptive text")
            log_format_validation "WARN" "browser" "element" "length_check" "Short description: $element"
        fi
    fi
    
    # File Paths Validation
    if echo "$parameters" | jq -e '.paths' > /dev/null 2>&1; then
        local paths_valid=$(echo "$parameters" | jq -e '.paths | type == "array"' 2>/dev/null)
        if [[ "$paths_valid" == "true" ]]; then
            # Check each path format
            local paths_array=$(echo "$parameters" | jq -r '.paths[]' 2>/dev/null)
            while IFS= read -r path; do
                if [[ "$path" =~ ^/ ]]; then
                    log_format_validation "PASS" "browser" "paths" "path_format" "Absolute path: $path"
                else
                    FORMAT_WARNINGS+=("Path should be absolute: '$path'")
                    log_format_validation "WARN" "browser" "paths" "path_format" "Relative path: $path"
                fi
            done <<< "$paths_array"
        else
            FORMAT_ERRORS+=("paths must be an array of file path strings")
            log_format_validation "ERROR" "browser" "paths" "structure_check" "Invalid structure: not an array"
        fi
    fi
}

# MCP Docker parameter format validation
validate_mcp_docker_parameter_formats() {
    local parameters="$1"
    
    # GitHub Repository Parameters
    local owner=$(echo "$parameters" | jq -r '.owner // empty' 2>/dev/null)
    local repo=$(echo "$parameters" | jq -r '.repo // empty' 2>/dev/null)
    
    if [[ -n "$owner" ]]; then
        if [[ "$owner" =~ ^[a-zA-Z0-9._-]+$ ]]; then
            log_format_validation "PASS" "mcp-docker" "owner" "format_check" "Valid owner format"
        else
            FORMAT_WARNINGS+=("Owner name contains unusual characters: '$owner'")
            log_format_validation "WARN" "mcp-docker" "owner" "format_check" "Unusual characters: $owner"
        fi
    fi
    
    if [[ -n "$repo" ]]; then
        if [[ "$repo" =~ ^[a-zA-Z0-9._-]+$ ]]; then
            log_format_validation "PASS" "mcp-docker" "repo" "format_check" "Valid repo format"
        else
            FORMAT_WARNINGS+=("Repo name contains unusual characters: '$repo'")
            log_format_validation "WARN" "mcp-docker" "repo" "format_check" "Unusual characters: $repo"
        fi
    fi
    
    # Pull Request Number Validation
    local pullNumber=$(echo "$parameters" | jq -r '.pullNumber // empty' 2>/dev/null)
    if [[ -n "$pullNumber" ]]; then
        if [[ "$pullNumber" =~ ^[0-9]+$ ]]; then
            log_format_validation "PASS" "mcp-docker" "pullNumber" "format_check" "Valid number format"
        else
            FORMAT_ERRORS+=("pullNumber must be a positive integer: '$pullNumber'")
            log_format_validation "ERROR" "mcp-docker" "pullNumber" "format_check" "Invalid number: $pullNumber"
        fi
    fi
    
    # Issue Number Validation
    local issue_number=$(echo "$parameters" | jq -r '.issue_number // empty' 2>/dev/null)
    if [[ -n "$issue_number" ]]; then
        if [[ "$issue_number" =~ ^[0-9]+$ ]]; then
            log_format_validation "PASS" "mcp-docker" "issue_number" "format_check" "Valid number format"
        else
            FORMAT_ERRORS+=("issue_number must be a positive integer: '$issue_number'")
            log_format_validation "ERROR" "mcp-docker" "issue_number" "format_check" "Invalid number: $issue_number"
        fi
    fi
}

# Universal parameter format validation
validate_universal_parameter_formats() {
    local server_name="$1"
    local parameters="$2"
    
    # Pagination Parameters (Universal)
    validate_pagination_parameters "$server_name" "$parameters"
    
    # String Length Validation
    validate_string_lengths "$server_name" "$parameters"
    
    # Common ID Format Validation
    validate_common_id_formats "$server_name" "$parameters"
}

# Pagination parameters validation
validate_pagination_parameters() {
    local server_name="$1"
    local parameters="$2"
    
    local limit=$(echo "$parameters" | jq -r '.limit // empty' 2>/dev/null)
    if [[ -n "$limit" ]]; then
        if [[ "$limit" =~ ^[0-9]+$ ]]; then
            if [[ "$limit" -ge 1 && "$limit" -le 100 ]]; then
                log_format_validation "PASS" "$server_name" "limit" "range_check" "Valid range: $limit"
            else
                FORMAT_WARNINGS+=("Limit value '$limit' may cause issues. Recommended range: 1-100")
                log_format_validation "WARN" "$server_name" "limit" "range_check" "Out of recommended range: $limit"
            fi
        else
            FORMAT_ERRORS+=("Limit must be a positive integer: '$limit'")
            log_format_validation "ERROR" "$server_name" "limit" "format_check" "Invalid number: $limit"
        fi
    fi
    
    local start_at=$(echo "$parameters" | jq -r '.start_at // empty' 2>/dev/null)
    if [[ -n "$start_at" ]]; then
        if [[ "$start_at" =~ ^[0-9]+$ ]]; then
            log_format_validation "PASS" "$server_name" "start_at" "format_check" "Valid number format"
        else
            FORMAT_ERRORS+=("start_at must be a non-negative integer: '$start_at'")
            log_format_validation "ERROR" "$server_name" "start_at" "format_check" "Invalid number: $start_at"
        fi
    fi
}

# String length validation
validate_string_lengths() {
    local server_name="$1"
    local parameters="$2"
    
    # Check common string fields for reasonable lengths
    local title=$(echo "$parameters" | jq -r '.title // empty' 2>/dev/null)
    if [[ -n "$title" && ${#title} -gt 200 ]]; then
        FORMAT_WARNINGS+=("Title is very long (${#title} chars): may be truncated by API")
        log_format_validation "WARN" "$server_name" "title" "length_check" "Long title: ${#title} chars"
    fi
    
    local description=$(echo "$parameters" | jq -r '.description // empty' 2>/dev/null)
    if [[ -n "$description" && ${#description} -gt 2000 ]]; then
        FORMAT_WARNINGS+=("Description is very long (${#description} chars): may hit API limits")
        log_format_validation "WARN" "$server_name" "description" "length_check" "Long description: ${#description} chars"
    fi
}

# Common ID format validation
validate_common_id_formats() {
    local server_name="$1"
    local parameters="$2"
    
    # Look for common ID patterns
    local id_fields=("id" "user_id" "team_id" "workspace_id")
    
    for field in "${id_fields[@]}"; do
        local value=$(echo "$parameters" | jq -r ".$field // empty" 2>/dev/null)
        if [[ -n "$value" ]]; then
            if [[ "$value" =~ ^[a-zA-Z0-9_-]+$ ]]; then
                log_format_validation "PASS" "$server_name" "$field" "id_format" "Valid ID format"
            else
                FORMAT_WARNINGS+=("ID field '$field' contains unusual characters: '$value'")
                log_format_validation "WARN" "$server_name" "$field" "id_format" "Unusual characters: $value"
            fi
        fi
    done
}

# Generate format validation report
generate_format_validation_report() {
    local server_name="$1"
    local tool_name="$2"
    
    echo ""
    echo "=== Parameter Format Validation Report ==="
    echo "Server: $server_name"
    echo "Tool: $tool_name"
    echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    
    if [[ ${#FORMAT_ERRORS[@]} -gt 0 ]]; then
        echo "❌ FORMAT ERRORS (${#FORMAT_ERRORS[@]}):"
        for error in "${FORMAT_ERRORS[@]}"; do
            echo "  - $error"
        done
        echo ""
    fi
    
    if [[ ${#FORMAT_WARNINGS[@]} -gt 0 ]]; then
        echo "⚠️  FORMAT WARNINGS (${#FORMAT_WARNINGS[@]}):"
        for warning in "${FORMAT_WARNINGS[@]}"; do
            echo "  - $warning"
        done
        echo ""
    fi
    
    if [[ ${#FORMAT_CORRECTIONS[@]} -gt 0 ]]; then
        echo "🔧 SUGGESTED CORRECTIONS (${#FORMAT_CORRECTIONS[@]}):"
        for correction in "${FORMAT_CORRECTIONS[@]}"; do
            echo "  - $correction"
        done
        echo ""
    fi
    
    if [[ ${#FORMAT_ERRORS[@]} -eq 0 && ${#FORMAT_WARNINGS[@]} -eq 0 && ${#FORMAT_CORRECTIONS[@]} -eq 0 ]]; then
        echo "✅ All parameter formats are valid"
        echo ""
    fi
    
    echo "=== End Format Validation Report ==="
    echo ""
}

# Apply auto-corrections to parameters
apply_auto_corrections() {
    local parameters="$1"
    local corrected_params="$parameters"
    
    # This would apply the auto-corrections identified during validation
    # For now, just return the original parameters
    echo "$corrected_params"
}

# Quick format validation (for integration)
quick_format_validate() {
    local server_name="$1"
    local tool_name="$2"
    local parameters="$3"
    
    validate_parameter_formats "$server_name" "$tool_name" "$parameters" > /dev/null 2>&1
    return $?
}

# Main execution
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    # Initialize logging
    initialize_format_logging
    
    case "${1:-help}" in
        "validate")
            if [[ $# -lt 3 ]]; then
                echo "Usage: $0 validate <server_name> <tool_name> [parameters_json]"
                echo "Example: $0 validate jira jira_get_issue '{\"issue_key\":\"proj-123\"}'"
                exit 1
            fi
            validate_parameter_formats "$2" "$3" "$4"
            exit $?
            ;;
        "quick")
            if [[ $# -lt 3 ]]; then
                echo "Usage: $0 quick <server_name> <tool_name> [parameters_json]"
                exit 1
            fi
            quick_format_validate "$2" "$3" "$4"
            exit_code=$?
            if [[ $exit_code -eq 0 ]]; then
                echo "✅ FORMAT VALID"
            else
                echo "❌ FORMAT INVALID"
            fi
            exit $exit_code
            ;;
        "correct")
            if [[ $# -lt 4 ]]; then
                echo "Usage: $0 correct <server_name> <tool_name> <parameters_json>"
                exit 1
            fi
            validate_parameter_formats "$2" "$3" "$4" > /dev/null 2>&1
            corrected=$(apply_auto_corrections "$4")
            echo "$corrected"
            ;;
        "help"|*)
            echo "MCP Parameter Format Validator"
            echo "Validates and auto-corrects parameter formats for MCP tool calls"
            echo ""
            echo "Usage:"
            echo "  $0 validate <server> <tool> [params]  - Full format validation with report"
            echo "  $0 quick <server> <tool> [params]     - Quick validation (exit code only)"
            echo "  $0 correct <server> <tool> <params>   - Apply auto-corrections to parameters"
            echo ""
            echo "Examples:"
            echo "  $0 validate jira jira_get_issue '{\"issue_key\":\"proj-123\"}'"
            echo "  $0 quick notion-api retrieve-page '{\"page_id\":\"invalid-id\"}'"
            echo "  $0 correct jira search '{\"jql\":\"project=TEST\"}'"
            echo ""
            echo "Exit codes:"
            echo "  0 - Format validation passed"
            echo "  1 - Format validation failed (errors found)"
            ;;
    esac
else
    # Sourced by another script - functions available
    initialize_format_logging
fi