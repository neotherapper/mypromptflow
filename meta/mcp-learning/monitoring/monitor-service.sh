#!/bin/bash

# MCP Learning System Monitoring Service
# Continuously monitors system health and updates dashboard

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MCP_LEARNING_DIR="$(dirname "$SCRIPT_DIR")"
PID_FILE="$SCRIPT_DIR/monitor.pid"
LOG_FILE="$SCRIPT_DIR/monitor.log"
METRICS_COLLECTOR="$SCRIPT_DIR/metrics-collector.sh"
DASHBOARD_GENERATOR="$SCRIPT_DIR/dashboard-generator.sh"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log_message() {
    local level="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] [$level] $message" >> "$LOG_FILE"
    
    case "$level" in
        "INFO")  echo -e "${GREEN}[$timestamp]${NC} $message" ;;
        "WARN")  echo -e "${YELLOW}[$timestamp]${NC} $message" ;;
        "ERROR") echo -e "${RED}[$timestamp]${NC} $message" ;;
        *)       echo "[$timestamp] $message" ;;
    esac
}

# Check if monitoring service is running
is_running() {
    if [[ -f "$PID_FILE" ]]; then
        local pid=$(cat "$PID_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            return 0
        else
            rm -f "$PID_FILE"
            return 1
        fi
    fi
    return 1
}

# Start monitoring service
start_monitoring() {
    if is_running; then
        log_message "WARN" "Monitoring service is already running (PID: $(cat "$PID_FILE"))"
        return 1
    fi
    
    log_message "INFO" "Starting MCP Learning System monitoring service..."
    
    # Start monitoring in background
    (
        # Save PID
        echo $$ > "$PID_FILE"
        
        log_message "INFO" "Monitoring service started (PID: $$)"
        
        # Monitoring loop
        while true; do
            # Collect metrics every 30 seconds
            if bash "$METRICS_COLLECTOR" >> "$LOG_FILE" 2>&1; then
                log_message "INFO" "Metrics collected successfully"
            else
                log_message "ERROR" "Failed to collect metrics"
            fi
            
            # Check for alerts
            check_system_alerts
            
            # Update dashboard every 2 minutes
            local current_minute=$(date +%M)
            if (( current_minute % 2 == 0 )) && (( $(date +%S) < 30 )); then
                if bash "$DASHBOARD_GENERATOR" >> "$LOG_FILE" 2>&1; then
                    log_message "INFO" "Dashboard updated successfully"
                else
                    log_message "ERROR" "Failed to update dashboard"
                fi
            fi
            
            # Sleep for 30 seconds
            sleep 30
        done
    ) &
    
    local monitor_pid=$!
    echo $monitor_pid > "$PID_FILE"
    
    log_message "INFO" "Monitoring service started successfully (PID: $monitor_pid)"
    echo -e "${GREEN}✅ MCP Learning System monitoring started${NC}"
    echo "Dashboard available at: file://$SCRIPT_DIR/dashboard.html"
    echo "Logs: $LOG_FILE"
    echo "To stop: $0 stop"
}

# Stop monitoring service
stop_monitoring() {
    if ! is_running; then
        log_message "WARN" "Monitoring service is not running"
        return 1
    fi
    
    local pid=$(cat "$PID_FILE")
    log_message "INFO" "Stopping monitoring service (PID: $pid)..."
    
    if kill "$pid" 2>/dev/null; then
        # Wait for process to stop
        local count=0
        while kill -0 "$pid" 2>/dev/null && [ $count -lt 10 ]; do
            sleep 1
            count=$((count + 1))
        done
        
        if kill -0 "$pid" 2>/dev/null; then
            log_message "WARN" "Process still running, force killing..."
            kill -9 "$pid" 2>/dev/null
        fi
        
        rm -f "$PID_FILE"
        log_message "INFO" "Monitoring service stopped successfully"
        echo -e "${GREEN}✅ MCP Learning System monitoring stopped${NC}"
    else
        log_message "ERROR" "Failed to stop monitoring service"
        rm -f "$PID_FILE"
        return 1
    fi
}

# Restart monitoring service
restart_monitoring() {
    log_message "INFO" "Restarting monitoring service..."
    stop_monitoring
    sleep 2
    start_monitoring
}

# Get monitoring service status
get_status() {
    if is_running; then
        local pid=$(cat "$PID_FILE")
        local uptime=$(ps -o etime= -p "$pid" | tr -d ' ')
        echo -e "${GREEN}✅ MCP Learning System monitoring is running${NC}"
        echo "   PID: $pid"
        echo "   Uptime: $uptime"
        echo "   Dashboard: file://$SCRIPT_DIR/dashboard.html"
        echo "   Logs: $LOG_FILE"
    else
        echo -e "${RED}❌ MCP Learning System monitoring is not running${NC}"
        return 1
    fi
}

# Check for system alerts
check_system_alerts() {
    local metrics_file="$SCRIPT_DIR/metrics.json"
    
    if [[ ! -f "$metrics_file" ]]; then
        return 0
    fi
    
    # Read metrics (simplified JSON parsing)
    local error_rate=$(grep -o '"false_positive_rate":[0-9.]*' "$metrics_file" | cut -d':' -f2 || echo "0")
    local response_time=$(grep -o '"hook_response_time":[0-9.]*' "$metrics_file" | cut -d':' -f2 || echo "0")
    local memory_usage=$(grep -o '"memory_usage_mb":[0-9.]*' "$metrics_file" | cut -d':' -f2 || echo "0")
    
    # Check thresholds and generate alerts
    if (( $(echo "$error_rate > 0.20" | bc -l 2>/dev/null || echo "0") )); then
        log_message "ERROR" "CRITICAL: False positive rate above 20%: $error_rate"
    elif (( $(echo "$error_rate > 0.15" | bc -l 2>/dev/null || echo "0") )); then
        log_message "WARN" "WARNING: False positive rate above 15%: $error_rate"
    fi
    
    if (( $(echo "$response_time > 0.150" | bc -l 2>/dev/null || echo "0") )); then
        log_message "ERROR" "CRITICAL: Hook response time above 150ms: ${response_time}s"
    elif (( $(echo "$response_time > 0.100" | bc -l 2>/dev/null || echo "0") )); then
        log_message "WARN" "WARNING: Hook response time above 100ms: ${response_time}s"
    fi
    
    if (( $(echo "$memory_usage > 100" | bc -l 2>/dev/null || echo "0") )); then
        log_message "WARN" "WARNING: Memory usage above 100MB: ${memory_usage}MB"
    fi
}

# View recent logs
view_logs() {
    local lines="${1:-50}"
    if [[ -f "$LOG_FILE" ]]; then
        echo -e "${BLUE}=== Last $lines lines of monitoring logs ===${NC}"
        tail -n "$lines" "$LOG_FILE"
    else
        log_message "WARN" "Log file not found: $LOG_FILE"
    fi
}

# Show help
show_help() {
    echo "MCP Learning System Monitoring Service"
    echo ""
    echo "Usage: $0 {start|stop|restart|status|logs|help}"
    echo ""
    echo "Commands:"
    echo "  start    - Start the monitoring service"
    echo "  stop     - Stop the monitoring service"  
    echo "  restart  - Restart the monitoring service"
    echo "  status   - Show monitoring service status"
    echo "  logs     - Show recent monitoring logs (default: 50 lines)"
    echo "  help     - Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start                    # Start monitoring"
    echo "  $0 status                   # Check if running"
    echo "  $0 logs                     # Show last 50 log lines"
    echo "  $0 logs 100                 # Show last 100 log lines"
    echo "  $0 stop                     # Stop monitoring"
}

# Main command handler
case "${1:-help}" in
    "start")
        start_monitoring
        ;;
    "stop")
        stop_monitoring
        ;;
    "restart")
        restart_monitoring
        ;;
    "status")
        get_status
        ;;
    "logs")
        view_logs "$2"
        ;;
    "help"|"--help"|"-h")
        show_help
        ;;
    *)
        echo -e "${RED}Error: Unknown command '$1'${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac