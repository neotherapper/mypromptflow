#!/bin/bash

# Continuous Size Monitoring System for CLAUDE.md Files
# Monitors all CLAUDE.md files and alerts when size limits are approached
# Usage: ./continuous-size-monitor.sh [--watch] [--alert-threshold]

set -e

# Configuration
TIER_1_LIMIT=800    # Main routing files (CLAUDE.md)
TIER_2_LIMIT=1500   # Domain-specific files
TIER_3_LIMIT=2500   # Complex domain files  
ABSOLUTE_MAX=3000   # Never exceed threshold

WARNING_PERCENT=80  # Warning at 80% of limit
ALERT_PERCENT=90    # Alert at 90% of limit

PROJECT_ROOT="$(pwd)"
LOG_FILE="${PROJECT_ROOT}/meta/validation/size-monitor.log"
ALERT_FILE="${PROJECT_ROOT}/meta/validation/size-alerts.log"

WATCH_MODE=false
ALERT_THRESHOLD=${WARNING_PERCENT}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --watch)
            WATCH_MODE=true
            shift
            ;;
        --alert-threshold)
            ALERT_THRESHOLD="$2"
            shift 2
            ;;
        *)
            echo "Usage: $0 [--watch] [--alert-threshold PERCENT]"
            echo "  --watch              Run in continuous monitoring mode"
            echo "  --alert-threshold    Set alert threshold percentage (default: ${WARNING_PERCENT})"
            exit 1
            ;;
    esac
done

# Logging functions
log_message() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $1" | tee -a "$LOG_FILE"
}

log_alert() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local message="[$timestamp] ALERT: $1"
    echo "$message" | tee -a "$LOG_FILE" | tee -a "$ALERT_FILE"
}

# Function to get tier classification (same as validator)
get_tier_limit() {
    local file_path="$1"
    local filename=$(basename "$file_path")
    local dirname=$(dirname "$file_path")
    
    # Tier 1: Main project CLAUDE.md files
    if [[ "$filename" == "CLAUDE.md" && $(basename "$dirname") != "projects" && $(basename "$(dirname "$dirname")") != "projects" ]]; then
        echo "$TIER_1_LIMIT"
    # Tier 3: Complex domain files (instruction design, research orchestration)  
    elif [[ "$dirname" == *"ai-agent-instruction-design-excellence"* || "$dirname" == *"orchestrator"* ]]; then
        echo "$TIER_3_LIMIT"
    # Tier 2: Everything else
    else
        echo "$TIER_2_LIMIT"  
    fi
}

# Function to check single file and generate alerts
check_file_size() {
    local file_path="$1"
    local word_count=$(wc -w < "$file_path")
    local limit=$(get_tier_limit "$file_path")
    local tier=""
    
    # Determine tier for display
    case "$limit" in
        "$TIER_1_LIMIT") tier="1 (Routing)" ;;
        "$TIER_2_LIMIT") tier="2 (Specialized)" ;;
        "$TIER_3_LIMIT") tier="3 (Complex)" ;;
    esac
    
    local warning_threshold=$((limit * WARNING_PERCENT / 100))
    local alert_threshold=$((limit * ALERT_THRESHOLD / 100))
    local critical_threshold=$((limit * 95 / 100))
    local usage_percent=$((word_count * 100 / limit))
    
    local relative_path=${file_path#$PROJECT_ROOT/}
    
    # Generate alerts based on thresholds
    if [[ $word_count -gt $ABSOLUTE_MAX ]]; then
        log_alert "CRITICAL: $relative_path exceeds absolute maximum ($word_count > $ABSOLUTE_MAX words)"
        return 3
    elif [[ $word_count -gt $critical_threshold ]]; then
        log_alert "CRITICAL: $relative_path approaching limit ($word_count/$limit words, ${usage_percent}%)"
        return 2
    elif [[ $word_count -gt $alert_threshold ]]; then
        log_alert "WARNING: $relative_path reaching threshold ($word_count/$limit words, ${usage_percent}%)"
        return 1
    else
        log_message "OK: $relative_path - $word_count/$limit words (${usage_percent}%)"
        return 0
    fi
}

# Function to scan all CLAUDE.md files
scan_all_files() {
    local total_alerts=0
    local total_files=0
    
    log_message "Starting size monitoring scan..."
    
    while IFS= read -r -d '' file; do
        ((total_files++))
        check_file_size "$file"
        local exit_code=$?
        if [[ $exit_code -gt 0 ]]; then
            ((total_alerts++))
        fi
    done < <(find "$PROJECT_ROOT" -name "CLAUDE.md" -type f -print0 | sort -z)
    
    log_message "Scan complete: $total_files files checked, $total_alerts alerts generated"
    return $total_alerts
}

# Function to generate recommendations for oversized files
generate_recommendations() {
    local file_path="$1"
    local word_count="$2"
    local limit="$3"
    
    echo "📋 RECOMMENDATIONS for $file_path:"
    echo "   Current: $word_count words, Limit: $limit words"
    echo "   Suggested actions:"
    echo "   1. Extract large sections to specialized CLAUDE.md files"
    echo "   2. Replace detailed content with @file_path routing references"
    echo "   3. Move implementation details to dedicated files"
    echo "   4. Use meta/validation/claude-file-size-validator.sh for detailed analysis"
    echo ""
}

# Function to create monitoring report
create_monitoring_report() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    local report_file="${PROJECT_ROOT}/meta/validation/size-monitoring-report.md"
    
    cat > "$report_file" << EOF
# CLAUDE.md Size Monitoring Report

**Generated**: $timestamp
**Monitoring Script**: continuous-size-monitor.sh
**Alert Threshold**: ${ALERT_THRESHOLD}%

## Current Status

EOF
    
    # Run validator and append results
    if [[ -f "${PROJECT_ROOT}/meta/validation/claude-file-size-validator.sh" ]]; then
        echo "### File Size Analysis" >> "$report_file"
        echo '```' >> "$report_file"
        "${PROJECT_ROOT}/meta/validation/claude-file-size-validator.sh" 2>&1 >> "$report_file" || true
        echo '```' >> "$report_file"
    fi
    
    # Add recent alerts if any
    if [[ -f "$ALERT_FILE" && -s "$ALERT_FILE" ]]; then
        echo "" >> "$report_file"
        echo "## Recent Alerts" >> "$report_file"
        echo '```' >> "$report_file"
        tail -20 "$ALERT_FILE" >> "$report_file"
        echo '```' >> "$report_file"
    fi
    
    # Add recommendations
    cat >> "$report_file" << EOF

## Monitoring Guidelines

### Size Limits by Tier
- **Tier 1 (Routing)**: ≤800 words - Main CLAUDE.md files should be lightweight routing hubs
- **Tier 2 (Specialized)**: ≤1500 words - Domain-specific instruction files
- **Tier 3 (Complex)**: ≤2500 words - Complex domain files with detailed procedures

### Alert Thresholds
- **Warning**: ≥80% of limit - Consider optimization
- **Alert**: ≥90% of limit - Requires immediate attention
- **Critical**: ≥95% of limit - Must decompose before further changes
- **Maximum**: >3000 words - Absolute limit, immediate action required

### Recommended Actions for Oversized Files
1. **Content Decomposition**: Extract large sections to specialized files
2. **Routing References**: Replace detailed content with @file_path references
3. **Progressive Disclosure**: Move implementation details to dedicated files
4. **Regular Monitoring**: Use continuous monitoring to prevent size bloat

### Commands
\`\`\`bash
# Run size validation
./meta/validation/claude-file-size-validator.sh

# Start continuous monitoring
./meta/validation/continuous-size-monitor.sh --watch

# Generate monitoring report
./meta/validation/continuous-size-monitor.sh --report
\`\`\`
EOF
    
    log_message "Monitoring report generated: $report_file"
}

# Watch mode function
run_watch_mode() {
    log_message "Starting continuous monitoring (watch mode)..."
    log_message "Monitoring interval: 60 seconds"
    log_message "Alert threshold: ${ALERT_THRESHOLD}%"
    
    while true; do
        scan_all_files
        local alerts=$?
        
        if [[ $alerts -gt 0 ]]; then
            log_message "Found $alerts files requiring attention"
            create_monitoring_report
        fi
        
        # Wait 60 seconds before next scan
        sleep 60
    done
}

# Main execution
main() {
    # Ensure log directory exists
    mkdir -p "$(dirname "$LOG_FILE")"
    
    log_message "CLAUDE.md Continuous Size Monitor started"
    log_message "Project: $(basename "$PROJECT_ROOT")"
    log_message "Alert threshold: ${ALERT_THRESHOLD}%"
    
    if [[ "$WATCH_MODE" == "true" ]]; then
        run_watch_mode
    else
        # Single scan mode
        scan_all_files
        local alerts=$?
        
        create_monitoring_report
        
        if [[ $alerts -gt 0 ]]; then
            echo ""
            echo "⚠️  MONITORING ALERT: $alerts files require attention"
            echo "📊 View detailed report: meta/validation/size-monitoring-report.md"
            echo "🔧 Run validator: ./meta/validation/claude-file-size-validator.sh"
            exit 1
        else
            echo ""
            echo "✅ MONITORING OK: All CLAUDE.md files within size limits"
            echo "📊 Report generated: meta/validation/size-monitoring-report.md"
            exit 0
        fi
    fi
}

# Handle script termination gracefully
trap 'log_message "Continuous monitoring stopped"; exit 0' SIGINT SIGTERM

# Run main function
main "$@"