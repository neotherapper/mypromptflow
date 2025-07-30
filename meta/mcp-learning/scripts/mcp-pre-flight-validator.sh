#!/bin/bash

# MCP Pre-Flight Validator
# Performs validation checks before MCP tool calls to prevent common errors
# Simple, reliable validation based on learned patterns and common requirements

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MCP_LEARNING_DIR="$(dirname "$SCRIPT_DIR")"
USAGE_GUIDES_DIR="$MCP_LEARNING_DIR/usage-guides"
PATTERNS_DIR="$MCP_LEARNING_DIR/patterns"
VALIDATION_LOG="$MCP_LEARNING_DIR/validation-log.txt"

# Validation results
VALIDATION_PASSED=true
VALIDATION_ERRORS=()
VALIDATION_WARNINGS=()

# Initialize validation log
initialize_validation_log() {
    if [[ ! -f "$VALIDATION_LOG" ]]; then
        cat > "$VALIDATION_LOG" << 'EOF'
# MCP Pre-Flight Validation Log
# Tracks validation checks and their outcomes
# Format: [TIMESTAMP] [LEVEL] [SERVER] [TOOL] [CHECK] - [RESULT]

EOF
    fi
}

# Log validation result
log_validation() {
    local level="$1"
    local server="$2"
    local tool="$3"
    local check="$4"
    local result="$5"
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] [$server] [$tool] [$check] - $result" >> "$VALIDATION_LOG"
}

# Main validation function
validate_mcp_call() {
    local server_name="$1"
    local tool_name="$2"
    local parameters="$3"  # JSON string
    
    echo "[Validator] Starting pre-flight validation for $server_name::$tool_name"
    
    # Initialize validation state
    VALIDATION_PASSED=true
    VALIDATION_ERRORS=()
    VALIDATION_WARNINGS=()
    
    # Run server-specific validation
    case "$server_name" in
        "jira")
            validate_jira_call "$tool_name" "$parameters"
            ;;
        "notion-api")
            validate_notion_call "$tool_name" "$parameters"
            ;;
        "browser")
            validate_browser_call "$tool_name" "$parameters"
            ;;
        "mcp-docker")
            validate_mcp_docker_call "$tool_name" "$parameters"
            ;;
        *)
            validate_generic_call "$server_name" "$tool_name" "$parameters"
            ;;
    esac
    
    # Run universal validation checks
    validate_universal_requirements "$server_name" "$tool_name" "$parameters"
    
    # Generate validation report
    generate_validation_report "$server_name" "$tool_name"
    
    # Return validation result
    if [[ "$VALIDATION_PASSED" == "true" ]]; then
        echo "[Validator] ✅ Validation PASSED - Safe to proceed"
        return 0
    else
        echo "[Validator] ❌ Validation FAILED - Review errors before proceeding"
        return 1
    fi
}

# JIRA-specific validation
validate_jira_call() {
    local tool_name="$1"
    local parameters="$2"
    
    echo "[Validator] Running JIRA-specific validation..."
    
    # Check for issue key format (critical pattern from usage guide)
    if echo "$parameters" | grep -q "issue_key"; then
        local issue_key=$(echo "$parameters" | jq -r '.issue_key // empty' 2>/dev/null)
        if [[ -n "$issue_key" ]]; then
            if [[ ! "$issue_key" =~ ^[A-Z]+-[0-9]+$ ]]; then
                VALIDATION_ERRORS+=("Invalid issue key format: '$issue_key'. Must be PROJECT-NUMBER (e.g., SCRUM-123)")
                VALIDATION_PASSED=false
                log_validation "ERROR" "jira" "$tool_name" "issue_key_format" "Invalid format: $issue_key"
            else
                log_validation "INFO" "jira" "$tool_name" "issue_key_format" "Valid format: $issue_key"
            fi
        fi
    fi
    
    # Check for project key format
    if echo "$parameters" | grep -q "project_key"; then
        local project_key=$(echo "$parameters" | jq -r '.project_key // empty' 2>/dev/null)
        if [[ -n "$project_key" ]]; then
            if [[ ! "$project_key" =~ ^[A-Z]+$ ]]; then
                VALIDATION_ERRORS+=("Invalid project key format: '$project_key'. Must be uppercase letters only")
                VALIDATION_PASSED=false
                log_validation "ERROR" "jira" "$tool_name" "project_key_format" "Invalid format: $project_key"
            else
                log_validation "INFO" "jira" "$tool_name" "project_key_format" "Valid format: $project_key"
            fi
        fi
    fi
    
    # Check for JQL syntax basics (common error prevention)
    if echo "$parameters" | grep -q "jql"; then
        local jql=$(echo "$parameters" | jq -r '.jql // empty' 2>/dev/null)
        if [[ -n "$jql" ]]; then
            # Basic JQL validation
            if [[ "$jql" == *"="* && ! "$jql" == *" = "* ]]; then
                VALIDATION_WARNINGS+=("JQL may need spaces around '=' operator: '$jql'")
                log_validation "WARN" "jira" "$tool_name" "jql_syntax" "Missing spaces around operator"
            fi
            
            if [[ "$jql" == *"AND"* && ! "$jql" == *" AND "* ]]; then
                VALIDATION_WARNINGS+=("JQL may need spaces around 'AND' operator: '$jql'")
                log_validation "WARN" "jira" "$tool_name" "jql_syntax" "Missing spaces around AND"
            fi
            
            log_validation "INFO" "jira" "$tool_name" "jql_syntax" "Basic syntax check passed"
        fi
    fi
    
    # Check for critical sprint field (documented error prevention)
    if [[ "$tool_name" == *"issue"* && "$tool_name" == *"get"* ]]; then
        if echo "$parameters" | grep -q "fields"; then
            local fields=$(echo "$parameters" | jq -r '.fields // empty' 2>/dev/null)
            if [[ -n "$fields" && ! "$fields" == *"customfield_10020"* ]]; then
                VALIDATION_WARNINGS+=("Consider including customfield_10020 (sprint field) to prevent sprint misclassification")
                log_validation "WARN" "jira" "$tool_name" "sprint_field" "Missing sprint field in fields parameter"
            fi
        fi
    fi
}

# Notion API validation
validate_notion_call() {
    local tool_name="$1"
    local parameters="$2"
    
    echo "[Validator] Running Notion API validation..."
    
    # Check for page_id format
    if echo "$parameters" | grep -q "page_id"; then
        local page_id=$(echo "$parameters" | jq -r '.page_id // empty' 2>/dev/null)
        if [[ -n "$page_id" ]]; then
            # Basic UUID format check
            if [[ ! "$page_id" =~ ^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$ ]] && [[ ! "$page_id" =~ ^[a-f0-9]{32}$ ]]; then
                VALIDATION_ERRORS+=("Invalid page_id format: '$page_id'. Must be UUID format")
                VALIDATION_PASSED=false
                log_validation "ERROR" "notion-api" "$tool_name" "page_id_format" "Invalid format: $page_id"
            else
                log_validation "INFO" "notion-api" "$tool_name" "page_id_format" "Valid format"
            fi
        fi
    fi
    
    # Check for database_id format
    if echo "$parameters" | grep -q "database_id"; then
        local database_id=$(echo "$parameters" | jq -r '.database_id // empty' 2>/dev/null)
        if [[ -n "$database_id" ]]; then
            if [[ ! "$database_id" =~ ^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$ ]] && [[ ! "$database_id" =~ ^[a-f0-9]{32}$ ]]; then
                VALIDATION_ERRORS+=("Invalid database_id format: '$database_id'. Must be UUID format")
                VALIDATION_PASSED=false
                log_validation "ERROR" "notion-api" "$tool_name" "database_id_format" "Invalid format: $database_id"
            else
                log_validation "INFO" "notion-api" "$tool_name" "database_id_format" "Valid format"
            fi
        fi
    fi
}

# Browser automation validation
validate_browser_call() {
    local tool_name="$1"
    local parameters="$2"
    
    echo "[Validator] Running Browser automation validation..."
    
    # Check for URL format in navigation calls
    if [[ "$tool_name" == *"navigate"* ]] && echo "$parameters" | grep -q "url"; then
        local url=$(echo "$parameters" | jq -r '.url // empty' 2>/dev/null)
        if [[ -n "$url" ]]; then
            if [[ ! "$url" =~ ^https?:// ]]; then
                VALIDATION_ERRORS+=("Invalid URL format: '$url'. Must start with http:// or https://")
                VALIDATION_PASSED=false
                log_validation "ERROR" "browser" "$tool_name" "url_format" "Invalid format: $url"
            else
                log_validation "INFO" "browser" "$tool_name" "url_format" "Valid format"
            fi
        fi
    fi
    
    # Check for element reference requirements
    if [[ "$tool_name" == *"click"* || "$tool_name" == *"type"* ]]; then
        if ! echo "$parameters" | grep -q "ref"; then
            VALIDATION_ERRORS+=("Missing required 'ref' parameter for element interaction")
            VALIDATION_PASSED=false
            log_validation "ERROR" "browser" "$tool_name" "ref_required" "Missing ref parameter"
        else
            log_validation "INFO" "browser" "$tool_name" "ref_required" "Ref parameter present"
        fi
    fi
}

# MCP Docker validation
validate_mcp_docker_call() {
    local tool_name="$1"
    local parameters="$2"
    
    echo "[Validator] Running MCP Docker validation..."
    
    # Check for GitHub repository parameters
    if echo "$parameters" | grep -q "owner" && echo "$parameters" | grep -q "repo"; then
        local owner=$(echo "$parameters" | jq -r '.owner // empty' 2>/dev/null)
        local repo=$(echo "$parameters" | jq -r '.repo // empty' 2>/dev/null)
        
        if [[ -n "$owner" && -n "$repo" ]]; then
            # Basic format validation
            if [[ ! "$owner" =~ ^[a-zA-Z0-9._-]+$ ]]; then
                VALIDATION_WARNINGS+=("Owner name contains unusual characters: '$owner'")
                log_validation "WARN" "mcp-docker" "$tool_name" "owner_format" "Unusual characters in owner"
            fi
            
            if [[ ! "$repo" =~ ^[a-zA-Z0-9._-]+$ ]]; then
                VALIDATION_WARNINGS+=("Repo name contains unusual characters: '$repo'")
                log_validation "WARN" "mcp-docker" "$tool_name" "repo_format" "Unusual characters in repo"
            fi
            
            log_validation "INFO" "mcp-docker" "$tool_name" "repo_params" "Owner and repo parameters valid"
        fi
    fi
}

# Generic validation for all servers
validate_generic_call() {
    local server_name="$1"
    local tool_name="$2"
    local parameters="$3"
    
    echo "[Validator] Running generic validation for $server_name..."
    log_validation "INFO" "$server_name" "$tool_name" "generic_validation" "Basic validation completed"
}

# Universal validation checks
validate_universal_requirements() {
    local server_name="$1"
    local tool_name="$2"
    local parameters="$3"
    
    echo "[Validator] Running universal validation checks..."
    
    # Check for empty parameters
    if [[ -z "$parameters" || "$parameters" == "{}" || "$parameters" == "null" ]]; then
        VALIDATION_WARNINGS+=("Empty parameters - verify if this is expected for $tool_name")
        log_validation "WARN" "universal" "$tool_name" "empty_params" "No parameters provided"
    fi
    
    # Check for valid JSON format
    if [[ -n "$parameters" ]]; then
        if ! echo "$parameters" | jq . > /dev/null 2>&1; then
            VALIDATION_ERRORS+=("Invalid JSON format in parameters")
            VALIDATION_PASSED=false
            log_validation "ERROR" "universal" "$tool_name" "json_format" "Invalid JSON parameters"
        else
            log_validation "INFO" "universal" "$tool_name" "json_format" "Valid JSON parameters"
        fi
    fi
    
    # Check for pagination parameters sanity
    if echo "$parameters" | grep -q "limit"; then
        local limit=$(echo "$parameters" | jq -r '.limit // empty' 2>/dev/null)
        if [[ -n "$limit" && "$limit" =~ ^[0-9]+$ ]]; then
            if [[ "$limit" -gt 100 ]]; then
                VALIDATION_WARNINGS+=("Large limit value ($limit) may cause timeouts or API limits")
                log_validation "WARN" "universal" "$tool_name" "limit_size" "Large limit: $limit"
            fi
        fi
    fi
}

# Generate validation report
generate_validation_report() {
    local server_name="$1"
    local tool_name="$2"
    
    echo ""
    echo "=== MCP Pre-Flight Validation Report ==="
    echo "Server: $server_name"
    echo "Tool: $tool_name"
    echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    
    if [[ ${#VALIDATION_ERRORS[@]} -gt 0 ]]; then
        echo "❌ ERRORS (${#VALIDATION_ERRORS[@]}):"
        for error in "${VALIDATION_ERRORS[@]}"; do
            echo "  - $error"
        done
        echo ""
    fi
    
    if [[ ${#VALIDATION_WARNINGS[@]} -gt 0 ]]; then
        echo "⚠️  WARNINGS (${#VALIDATION_WARNINGS[@]}):"
        for warning in "${VALIDATION_WARNINGS[@]}"; do
            echo "  - $warning"
        done
        echo ""
    fi
    
    if [[ ${#VALIDATION_ERRORS[@]} -eq 0 && ${#VALIDATION_WARNINGS[@]} -eq 0 ]]; then
        echo "✅ No issues found - validation passed cleanly"
        echo ""
    fi
    
    echo "=== End Validation Report ==="
    echo ""
}

# Quick validation check (for integration)
quick_validate() {
    local server_name="$1"
    local tool_name="$2"
    local parameters="$3"
    
    # Run validation silently
    validate_mcp_call "$server_name" "$tool_name" "$parameters" > /dev/null 2>&1
    return $?
}

# Main execution
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    # Initialize logging
    initialize_validation_log
    
    case "${1:-help}" in
        "validate")
            if [[ $# -lt 3 ]]; then
                echo "Usage: $0 validate <server_name> <tool_name> [parameters_json]"
                echo "Example: $0 validate jira jira_get_issue '{\"issue_key\":\"PROJ-123\"}'"
                exit 1
            fi
            validate_mcp_call "$2" "$3" "$4"
            ;;
        "quick")
            if [[ $# -lt 3 ]]; then
                echo "Usage: $0 quick <server_name> <tool_name> [parameters_json]"
                exit 1
            fi
            quick_validate "$2" "$3" "$4"
            exit_code=$?
            if [[ $exit_code -eq 0 ]]; then
                echo "✅ PASS"
            else
                echo "❌ FAIL"
            fi
            exit $exit_code
            ;;
        "help"|*)
            echo "MCP Pre-Flight Validator"
            echo "Validates MCP tool calls before execution to prevent common errors"
            echo ""
            echo "Usage:"
            echo "  $0 validate <server> <tool> [params]  - Full validation with report"
            echo "  $0 quick <server> <tool> [params]     - Quick validation (exit code only)"
            echo ""
            echo "Examples:"
            echo "  $0 validate jira jira_get_issue '{\"issue_key\":\"PROJ-123\"}'"
            echo "  $0 quick notion-api retrieve-page '{\"page_id\":\"12345\"}'"
            echo ""
            echo "Exit codes:"
            echo "  0 - Validation passed"
            echo "  1 - Validation failed (errors found)"
            ;;
    esac
else
    # Sourced by another script - functions available
    initialize_validation_log
fi