#!/bin/bash

# Claude File Size Validator
# Validates word count limits for all CLAUDE.md files in the project
# Usage: ./claude-file-size-validator.sh [project-root-path]

set -e

# Configuration
TIER_1_LIMIT=800    # Main routing files (CLAUDE.md)
TIER_2_LIMIT=1500   # Domain-specific files
TIER_3_LIMIT=2500   # Complex domain files  
ABSOLUTE_MAX=3000   # Never exceed threshold

WARNING_PERCENT=80  # Warning at 80% of limit
ERROR_PERCENT=100   # Error at 100% of limit

PROJECT_ROOT="${1:-$(pwd)}"
TOTAL_FILES=0
OVERSIZED_FILES=0
WARNINGS=0
ERRORS=0

echo "🔍 Claude File Size Validation Report"
echo "═══════════════════════════════════════"
echo "📁 Project: $(basename "$PROJECT_ROOT")"
echo "📅 Date: $(date)"
echo ""

# Function to get tier classification
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

# Function to validate a single file
validate_file() {
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
    local error_threshold=$((limit * ERROR_PERCENT / 100))
    local usage_percent=$((word_count * 100 / limit))
    
    local relative_path=${file_path#$PROJECT_ROOT/}
    
    # Status determination
    local status="✅ OK"
    local color=""
    
    if [[ $word_count -gt $ABSOLUTE_MAX ]]; then
        status="🚨 CRITICAL"
        color="\033[1;31m"  # Bold red
        ((ERRORS++))
        ((OVERSIZED_FILES++))
    elif [[ $word_count -gt $error_threshold ]]; then
        status="❌ ERROR"  
        color="\033[0;31m"  # Red
        ((ERRORS++))
        ((OVERSIZED_FILES++))
    elif [[ $word_count -gt $warning_threshold ]]; then
        status="⚠️  WARNING"
        color="\033[0;33m"  # Yellow
        ((WARNINGS++))
    else
        color="\033[0;32m"  # Green
    fi
    
    # Output file status
    printf "${color}%-12s${color}" "$status"
    printf "\033[0m %-50s " "$relative_path"
    printf "Tier %-14s " "$tier"
    printf "%4d/%d words " "$word_count" "$limit"
    printf "(%3d%%)\n" "$usage_percent"
    
    # Add detailed recommendations for problematic files
    if [[ $word_count -gt $error_threshold ]]; then
        echo "    📋 RECOMMENDATION: Decompose content into specialized files"
        if [[ "$relative_path" == "CLAUDE.md" ]]; then
            echo "    🎯 ACTION: Convert to routing hub, move content to domain-specific CLAUDE.md files"
        fi
        echo ""
    elif [[ $word_count -gt $warning_threshold ]]; then
        echo "    💡 SUGGESTION: Consider content optimization or specialization"
        echo ""
    fi
    
    ((TOTAL_FILES++))
}

echo "📊 File Analysis:"
echo "Status      File Path                                          Tier            Words     Usage"
echo "─────────────────────────────────────────────────────────────────────────────────────────────"

# Find and validate all CLAUDE.md files
while IFS= read -r -d '' file; do
    validate_file "$file"
done < <(find "$PROJECT_ROOT" -name "CLAUDE.md" -type f -print0 | sort -z)

echo ""
echo "📈 Summary Statistics:"
echo "─────────────────────────────────────────────────────────────────────────────────────────────"
echo "📁 Total files scanned: $TOTAL_FILES"
echo "✅ Compliant files: $((TOTAL_FILES - OVERSIZED_FILES - WARNINGS))"
echo "⚠️  Warning files: $WARNINGS"  
echo "❌ Error/Critical files: $ERRORS"
echo "🚨 Oversized files: $OVERSIZED_FILES"
echo ""

# Overall assessment
if [[ $ERRORS -gt 0 ]]; then
    echo "🎯 OVERALL STATUS: ❌ FAILED - Critical size issues detected"
    echo "🛠️  ACTION REQUIRED: Immediate decomposition needed for error/critical files"
    exit 1
elif [[ $WARNINGS -gt 0 ]]; then
    echo "🎯 OVERALL STATUS: ⚠️  WARNING - Some files approaching limits"  
    echo "💡 RECOMMENDATION: Consider proactive optimization for warning files"
    exit 0
else
    echo "🎯 OVERALL STATUS: ✅ PASSED - All files within size limits"
    exit 0
fi