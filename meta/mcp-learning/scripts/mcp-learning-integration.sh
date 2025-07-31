#!/bin/bash

# MCP Learning Integration Script
# Unified interface for MCP learning system - validation, context logging, and error prevention
# Integrates pre-flight validation, parameter format checking, and context capture

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MCP_LEARNING_DIR="$(dirname "$SCRIPT_DIR")"

# Source component scripts
source "$SCRIPT_DIR/mcp-pre-flight-validator.sh"
source "$SCRIPT_DIR/mcp-parameter-format-validator.sh"
source "$SCRIPT_DIR/mcp-context-logger.sh"

# Integration log
INTEGRATION_LOG="$MCP_LEARNING_DIR/integration-usage.log"

# Initialize integration logging
initialize_integration() {
    if [[ ! -f "$INTEGRATION_LOG" ]]; then
        cat > "$INTEGRATION_LOG" << 'EOF'
# MCP Learning Integration Usage Log
# Tracks unified validation and context capture usage
# Format: [TIMESTAMP] [ACTION] [SERVER] [TOOL] - [RESULT]

EOF
    fi
}

# Log integration action
log_integration() {
    local action="$1"
    local server="$2"
    local tool="$3"
    local result="$4"
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$action] [$server] [$tool] - $result" >> "$INTEGRATION_LOG"
}

# Full MCP validation and context capture
validate_and_prepare_mcp_call() {
    local server_name="$1"
    local tool_name="$2"
    local parameters="$3"
    local immediate_objective="$4"
    local expected_outcome="$5"
    
    echo "🔍 [MCP Learning] Starting comprehensive validation and context capture..."
    echo ""
    
    # Step 1: Record the operation intent
    echo "📝 Step 1: Recording operation context..."
    record_mcp_operation "$server_name" "$tool_name" "$immediate_objective" "$expected_outcome" "$parameters"
    echo "✅ Context recorded"
    echo ""
    
    # Step 2: Parameter format validation
    echo "🔧 Step 2: Validating parameter formats..."
    if validate_parameter_formats "$server_name" "$tool_name" "$parameters"; then
        echo "✅ Parameter format validation passed"
        log_integration "FORMAT_VALIDATION" "$server_name" "$tool_name" "PASSED"
    else
        echo "❌ Parameter format validation failed"
        log_integration "FORMAT_VALIDATION" "$server_name" "$tool_name" "FAILED"
        echo ""
        echo "🛑 Recommendation: Fix parameter format issues before proceeding"
        return 1
    fi
    echo ""
    
    # Step 3: Pre-flight validation
    echo "🚀 Step 3: Running pre-flight validation..."
    if validate_mcp_call "$server_name" "$tool_name" "$parameters"; then
        echo "✅ Pre-flight validation passed"
        log_integration "PREFLIGHT_VALIDATION" "$server_name" "$tool_name" "PASSED"
    else
        echo "❌ Pre-flight validation failed"
        log_integration "PREFLIGHT_VALIDATION" "$server_name" "$tool_name" "FAILED"
        echo ""
        echo "🛑 Recommendation: Address validation issues before proceeding"
        return 1
    fi
    echo ""
    
    # Step 4: Check usage guide for specific warnings
    echo "📚 Step 4: Checking usage guide for known patterns..."
    check_usage_guide_warnings "$server_name" "$tool_name" "$parameters"
    echo ""
    
    echo "✅ [MCP Learning] All validations passed - Safe to proceed with MCP call"
    log_integration "COMPREHENSIVE_VALIDATION" "$server_name" "$tool_name" "ALL_PASSED"
    
    return 0
}

# Check usage guide for specific warnings
check_usage_guide_warnings() {
    local server_name="$1"
    local tool_name="$2"
    local parameters="$3"
    
    local usage_guide="$MCP_LEARNING_DIR/usage-guides/${server_name}-guide.md"
    
    if [[ -f "$usage_guide" ]]; then
        echo "📋 Checking usage guide: ${server_name}-guide.md"
        
        # Look for specific warnings based on the tool
        case "$server_name" in
            "jira")
                check_jira_specific_warnings "$tool_name" "$parameters"
                ;;
            "notion-api")
                check_notion_specific_warnings "$tool_name" "$parameters"
                ;;
            "browser")
                check_browser_specific_warnings "$tool_name" "$parameters"
                ;;
            *)
                echo "ℹ️  Generic usage guide check completed"
                ;;
        esac
    else
        echo "⚠️  No usage guide found for $server_name"
    fi
}

# JIRA-specific usage guide warnings
check_jira_specific_warnings() {
    local tool_name="$1"
    local parameters="$2"
    
    # Check for sprint field warning (documented critical issue)
    if [[ "$tool_name" == *"get_issue"* ]] && echo "$parameters" | jq -e '.fields' > /dev/null 2>&1; then
        local fields=$(echo "$parameters" | jq -r '.fields')
        if [[ ! "$fields" == *"customfield_10020"* ]]; then
            echo "⚠️  JIRA WARNING: Missing sprint field (customfield_10020) - may cause sprint misclassification"
            echo "   Recommendation: Add 'customfield_10020' to fields parameter"
        fi
    fi
    
    # Check for JQL complexity
    if echo "$parameters" | jq -e '.jql' > /dev/null 2>&1; then
        local jql=$(echo "$parameters" | jq -r '.jql')
        local word_count=$(echo "$jql" | wc -w)
        if [[ "$word_count" -gt 20 ]]; then
            echo "⚠️  JIRA WARNING: Complex JQL query ($word_count words) - may timeout"
            echo "   Recommendation: Simplify query or use pagination"
        fi
    fi
}

# Notion-specific usage guide warnings
check_notion_specific_warnings() {
    local tool_name="$1"
    local parameters="$2"
    
    # Check for large rich text arrays
    if echo "$parameters" | jq -e '.rich_text' > /dev/null 2>&1; then
        local rich_text_items=$(echo "$parameters" | jq '.rich_text | length' 2>/dev/null || echo 0)
        if [[ "$rich_text_items" -gt 100 ]]; then
            echo "⚠️  NOTION WARNING: Large rich text array ($rich_text_items items) - may hit API limits"
            echo "   Recommendation: Break into smaller chunks"
        fi
    fi
}

# Browser-specific usage guide warnings
check_browser_specific_warnings() {
    local tool_name="$1"
    local parameters="$2"
    
    # Check for file upload size considerations
    if [[ "$tool_name" == *"file_upload"* ]] && echo "$parameters" | jq -e '.paths' > /dev/null 2>&1; then
        echo "ℹ️  BROWSER INFO: File upload detected - ensure files exist and are accessible"
    fi
    
    # Check for navigation to external sites
    if [[ "$tool_name" == *"navigate"* ]] && echo "$parameters" | jq -e '.url' > /dev/null 2>&1; then
        local url=$(echo "$parameters" | jq -r '.url')
        if [[ ! "$url" == *"localhost"* && ! "$url" == *"127.0.0.1"* ]]; then
            echo "ℹ️  BROWSER INFO: Navigating to external site - ensure it's accessible and safe"
        fi
    fi
}

# Handle MCP operation success
handle_mcp_success() {
    local server_name="$1"
    local tool_name="$2"
    local outcome="$3"
    local response_data="$4"
    
    echo "✅ [MCP Learning] Recording successful operation..."
    
    # Record success in context
    record_mcp_success "$server_name" "$tool_name" "$outcome"
    
    # Log success
    log_integration "OPERATION_SUCCESS" "$server_name" "$tool_name" "$outcome"
    
    # Extract patterns from successful operation
    extract_success_patterns "$server_name" "$tool_name" "$response_data"
    
    echo "📊 Success recorded for learning"
}

# Handle MCP operation error
handle_mcp_error() {
    local server_name="$1"
    local tool_name="$2"
    local error_type="$3"
    local error_message="$4"
    local parameters="$5"
    local immediate_objective="$6"
    
    echo "❌ [MCP Learning] Recording error for analysis and learning..."
    
    # Record error in context
    record_mcp_error "$server_name" "$tool_name" "$error_type" "$error_message"
    
    # Log error
    log_integration "OPERATION_ERROR" "$server_name" "$tool_name" "$error_type"
    
    # Generate enhanced error context for manual logging
    echo ""
    echo "📋 Enhanced error context for logging:"
    generate_enhanced_error_context "$server_name" "$tool_name" "$immediate_objective" "$error_message" "$parameters"
    
    # Suggest immediate fixes if patterns are recognized
    suggest_immediate_fixes "$server_name" "$tool_name" "$error_type" "$error_message"
    
    echo ""
    echo "📝 Please log this error using the enhanced template at:"
    echo "   $MCP_LEARNING_DIR/error-logs/${server_name}-errors.md"
}

# Extract patterns from successful operations
extract_success_patterns() {
    local server_name="$1"
    local tool_name="$2"
    local response_data="$3"
    
    # Simple pattern extraction - more sophisticated analysis can be added later
    local success_file="$MCP_LEARNING_DIR/success-patterns/${server_name}-success-patterns.md"
    
    if [[ ! -f "$success_file" ]]; then
        echo "# $server_name Success Patterns" > "$success_file"
        echo "Auto-generated from successful operations" >> "$success_file"
        echo "" >> "$success_file"
    fi
    
    # Log basic success pattern
    cat >> "$success_file" << EOF
## Success Pattern - $(date '+%Y-%m-%d %H:%M:%S')
**Tool:** $tool_name
**Outcome:** Successful operation
**Response Size:** $(echo "$response_data" | wc -c) characters
**Pattern Confidence:** High (actual success)

EOF
}

# Suggest immediate fixes for recognized error patterns
suggest_immediate_fixes() {
    local server_name="$1"
    local tool_name="$2"
    local error_type="$3"
    local error_message="$4"
    
    echo "🔧 Immediate fix suggestions:"
    
    case "$server_name:$error_type" in
        "jira:Authentication"*)
            echo "  - Check JIRA credentials and permissions"
            echo "  - Verify API token hasn't expired"
            ;;
        "jira:Parameter"*)
            echo "  - Verify issue key format (PROJECT-123)"
            echo "  - Check JQL syntax for spaces around operators"
            ;;
        "notion-api:Authentication"*)
            echo "  - Check Notion integration token"
            echo "  - Verify workspace permissions"
            ;;
        "notion-api:Parameter"*)
            echo "  - Verify UUID formats for page_id/database_id"
            echo "  - Check rich text structure"
            ;;
        "browser:Element"*)
            echo "  - Take new snapshot to get current element references"
            echo "  - Verify element is visible and interactable"
            ;;
        *)
            echo "  - Check parameter formats against usage guide"
            echo "  - Verify API service is available"
            echo "  - Review authentication status"
            ;;
    esac
}

# Generate integration usage report
generate_integration_report() {
    echo "=== MCP Learning Integration Report ==="
    echo "Generated: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    
    if [[ -f "$INTEGRATION_LOG" ]]; then
        local total_validations=$(grep -c "VALIDATION" "$INTEGRATION_LOG" 2>/dev/null || echo 0)
        local passed_validations=$(grep -c "PASSED" "$INTEGRATION_LOG" 2>/dev/null || echo 0)
        local failed_validations=$(grep -c "FAILED" "$INTEGRATION_LOG" 2>/dev/null || echo 0)
        local total_operations=$(grep -c "OPERATION" "$INTEGRATION_LOG" 2>/dev/null || echo 0)
        local successful_operations=$(grep -c "OPERATION_SUCCESS" "$INTEGRATION_LOG" 2>/dev/null || echo 0)
        local error_operations=$(grep -c "OPERATION_ERROR" "$INTEGRATION_LOG" 2>/dev/null || echo 0)
        
        echo "**Validation Statistics:**"
        echo "- Total Validations: $total_validations"
        echo "- Passed: $passed_validations"
        echo "- Failed: $failed_validations"
        
        if [[ "$total_validations" -gt 0 ]]; then
            local pass_rate=$((($passed_validations * 100) / $total_validations))
            echo "- Pass Rate: $pass_rate%"
        fi
        echo ""
        
        echo "**Operation Statistics:**"
        echo "- Total Operations Tracked: $total_operations"
        echo "- Successful: $successful_operations"
        echo "- Errors: $error_operations"
        
        if [[ "$total_operations" -gt 0 ]]; then
            local success_rate=$((($successful_operations * 100) / $total_operations))
            echo "- Success Rate: $success_rate%"
        fi
        echo ""
        
        echo "**Server Usage (Last 24 hours):**"
        grep "$(date '+%Y-%m-%d')" "$INTEGRATION_LOG" | awk '{print $3}' | sort | uniq -c | while read count server; do
            echo "- $server: $count operations"
        done
        echo ""
    else
        echo "No integration data available yet"
    fi
    
    echo "=== End Integration Report ==="
}

# Main execution
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    initialize_integration
    
    case "${1:-help}" in
        "validate-and-prepare")
            if [[ $# -lt 5 ]]; then
                echo "Usage: $0 validate-and-prepare <server> <tool> <parameters> <objective> <expected_outcome>"
                echo "Example: $0 validate-and-prepare jira jira_get_issue '{\"issue_key\":\"PROJ-123\"}' 'Get issue details' 'Issue object returned'"
                exit 1
            fi
            validate_and_prepare_mcp_call "$2" "$3" "$4" "$5" "$6"
            ;;
        "handle-success")
            if [[ $# -lt 4 ]]; then
                echo "Usage: $0 handle-success <server> <tool> <outcome> [response_data]"
                exit 1
            fi
            handle_mcp_success "$2" "$3" "$4" "$5"
            ;;
        "handle-error")
            if [[ $# -lt 6 ]]; then
                echo "Usage: $0 handle-error <server> <tool> <error_type> <error_message> <parameters> <objective>"
                exit 1
            fi
            handle_mcp_error "$2" "$3" "$4" "$5" "$6" "$7"
            ;;
        "report")
            generate_integration_report
            ;;
        "test-validation")
            # Test the validation system with a sample call
            echo "🧪 Testing MCP Learning Integration..."
            echo ""
            validate_and_prepare_mcp_call "jira" "jira_get_issue" '{"issue_key":"TEST-123","fields":"summary,status"}' "Get test issue" "Issue details"
            ;;
        "help"|*)
            echo "MCP Learning Integration"
            echo "Unified interface for MCP validation, context capture, and learning"
            echo ""
            echo "Usage:"
            echo "  $0 validate-and-prepare <server> <tool> <params> <objective> <expected> - Full validation"
            echo "  $0 handle-success <server> <tool> <outcome> [response]                  - Record success"
            echo "  $0 handle-error <server> <tool> <error_type> <error_msg> <params> <obj> - Record error"
            echo "  $0 report                                                               - Generate report"
            echo "  $0 test-validation                                                      - Test system"
            echo ""
            echo "Integration Workflow:"
            echo "  1. Call 'validate-and-prepare' before MCP operation"
            echo "  2. Perform MCP operation"
            echo "  3. Call 'handle-success' or 'handle-error' with results"
            echo ""
            echo "Examples:"
            echo "  # Before MCP call"
            echo "  $0 validate-and-prepare jira jira_search '{\"jql\":\"project=TEST\"}' 'Find issues' 'Issue list'"
            echo ""
            echo "  # After successful MCP call"
            echo "  $0 handle-success jira jira_search 'Found 15 issues' '{\"total\":15}'"
            echo ""
            echo "  # After failed MCP call"
            echo "  $0 handle-error jira jira_search 'JQL Error' 'Invalid syntax' '{\"jql\":\"bad query\"}' 'Find issues'"
            ;;
    esac
else
    # Sourced by another script - all functions available
    initialize_integration
fi