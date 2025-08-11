#!/bin/bash

# JIRA Task Display Script for mypromptflow project
# Reads from symlinked .jira cache to display current sprint and backlog tasks

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
JIRA_DIR="$PROJECT_ROOT/.jira"

# Colors for output formatting
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to display usage
show_usage() {
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  sprint     Show current sprint tasks (default)"
    echo "  backlog    Show backlog items"
    echo "  all        Show both sprint and backlog"
    echo "  status     Show JIRA system status"
    echo "  help       Show this help message"
}

# Function to check if JIRA system is available
check_jira_system() {
    if [[ ! -L "$JIRA_DIR" ]]; then
        echo -e "${RED}Error: JIRA system not found at $JIRA_DIR${NC}"
        echo "Expected symlink to vanguardAI project's .jira directory"
        return 1
    fi
    
    local target_dir
    target_dir=$(readlink -f "$JIRA_DIR" 2>/dev/null) || {
        echo -e "${RED}Error: Cannot resolve JIRA symlink target${NC}"
        return 1
    }
    
    if [[ ! -d "$target_dir" ]]; then
        echo -e "${RED}Error: JIRA target directory not found: $target_dir${NC}"
        return 1
    fi
    
    return 0
}

# Function to display system status
show_status() {
    echo -e "${BLUE}=== JIRA System Status ===${NC}"
    echo ""
    
    if check_jira_system; then
        local target_dir
        target_dir=$(readlink -f "$JIRA_DIR")
        echo -e "✅ JIRA System: ${GREEN}Available${NC}"
        echo -e "📂 Symlink Target: $target_dir"
        
        # Check cache files
        local sprint_cache="$target_dir/cache/stories/current-sprint.json"
        local backlog_cache="$target_dir/cache/stories/backlog.json"
        
        if [[ -f "$sprint_cache" ]]; then
            local last_updated
            last_updated=$(jq -r '.last_updated // "Unknown"' "$sprint_cache" 2>/dev/null || echo "Unknown")
            echo -e "📋 Sprint Cache: ${GREEN}Available${NC} (Updated: $last_updated)"
        else
            echo -e "📋 Sprint Cache: ${RED}Missing${NC}"
        fi
        
        if [[ -f "$backlog_cache" ]]; then
            local last_updated
            last_updated=$(jq -r '.last_updated // "Unknown"' "$backlog_cache" 2>/dev/null || echo "Unknown")
            echo -e "📋 Backlog Cache: ${GREEN}Available${NC} (Updated: $last_updated)"
        else
            echo -e "📋 Backlog Cache: ${RED}Missing${NC}"
        fi
    else
        echo -e "❌ JIRA System: ${RED}Not Available${NC}"
    fi
    echo ""
}

# Function to display current sprint tasks
show_sprint_tasks() {
    local target_dir
    target_dir=$(readlink -f "$JIRA_DIR")
    local sprint_cache="$target_dir/cache/stories/current-sprint.json"
    
    if [[ ! -f "$sprint_cache" ]]; then
        echo -e "${RED}Error: Sprint cache file not found: $sprint_cache${NC}"
        return 1
    fi
    
    echo -e "${BLUE}=== Current Sprint Tasks ===${NC}"
    echo ""
    
    # Extract basic info using jq if available, fallback to grep
    if command -v jq >/dev/null 2>&1; then
        local sprint_name total_stories
        sprint_name=$(jq -r '.sprint_name // "Unknown Sprint"' "$sprint_cache")
        total_stories=$(jq -r '.total_stories // 0' "$sprint_cache")
        
        echo -e "${CYAN}Sprint:${NC} $sprint_name"
        echo -e "${CYAN}Total Stories:${NC} $total_stories"
        echo ""
        
        # Group and display tasks by status
        jq -r '.active_stories[] | "\(.status)|\(.key)|\(.title)"' "$sprint_cache" | \
        sort | \
        while IFS='|' read -r status key title; do
            case "$status" in
                "To Do")
                    status_color="${NC}"
                    ;;
                "In Progress")
                    status_color="${YELLOW}"
                    ;;
                "In Review")
                    status_color="${CYAN}"
                    ;;
                "Done")
                    status_color="${GREEN}"
                    ;;
                *)
                    status_color="${NC}"
                    ;;
            esac
            
            # Truncate long titles
            if [[ ${#title} -gt 70 ]]; then
                title="${title:0:67}..."
            fi
            
            echo -e "${status_color}● $status${NC}: $key - $title"
        done
    else
        # Fallback without jq
        echo -e "${YELLOW}Note: Install 'jq' for better formatting${NC}"
        echo ""
        grep -o '"key": "[^"]*"' "$sprint_cache" | head -10 | cut -d'"' -f4 | while read -r key; do
            echo "• $key"
        done
    fi
}

# Function to display backlog items
show_backlog_items() {
    local target_dir
    target_dir=$(readlink -f "$JIRA_DIR")
    local backlog_cache="$target_dir/cache/stories/backlog.json"
    
    if [[ ! -f "$backlog_cache" ]]; then
        echo -e "${RED}Error: Backlog cache file not found: $backlog_cache${NC}"
        return 1
    fi
    
    echo -e "${BLUE}=== Backlog Items ===${NC}"
    echo ""
    
    if command -v jq >/dev/null 2>&1; then
        local total_stories total_points
        total_stories=$(jq -r '.total_stories // 0' "$backlog_cache")
        total_points=$(jq -r '.total_points // 0' "$backlog_cache")
        
        echo -e "${CYAN}Total Stories:${NC} $total_stories"
        echo -e "${CYAN}Total Story Points:${NC} $total_points"
        echo ""
        
        jq -r '.backlog_stories[] | "\(.key)|\(.title)|\(.story_points)|\(.assignee)"' "$backlog_cache" | \
        while IFS='|' read -r key title points assignee; do
            # Truncate long titles
            if [[ ${#title} -gt 60 ]]; then
                title="${title:0:57}..."
            fi
            
            # Format assignee
            if [[ "$assignee" == "Unassigned" ]]; then
                assignee_display="${YELLOW}Unassigned${NC}"
            else
                assignee_display="${GREEN}$assignee${NC}"
            fi
            
            echo -e "${YELLOW}●${NC} $key (${points} pts)"
            echo -e "  $title"
            echo -e "  Assignee: $assignee_display"
            echo ""
        done
    else
        # Fallback without jq
        echo -e "${YELLOW}Note: Install 'jq' for better formatting${NC}"
        echo ""
        grep -o '"key": "[^"]*"' "$backlog_cache" | cut -d'"' -f4 | while read -r key; do
            echo "• $key"
        done
    fi
}

# Main function
main() {
    local command="${1:-sprint}"
    
    case "$command" in
        "help"|"-h"|"--help")
            show_usage
            ;;
        "status")
            show_status
            ;;
        "sprint")
            if ! check_jira_system; then
                exit 1
            fi
            show_sprint_tasks
            ;;
        "backlog")
            if ! check_jira_system; then
                exit 1
            fi
            show_backlog_items
            ;;
        "all")
            if ! check_jira_system; then
                exit 1
            fi
            show_sprint_tasks
            echo ""
            show_backlog_items
            ;;
        *)
            echo -e "${RED}Error: Unknown command '$command'${NC}"
            echo ""
            show_usage
            exit 1
            ;;
    esac
}

# Execute main function with all arguments
main "$@"