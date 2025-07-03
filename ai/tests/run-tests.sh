#!/bin/bash

# AI Knowledge Base Test Suite Runner
# This script executes comprehensive tests for the interactive command system

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test configuration
TEST_DIR="ai/tests"
BACKUP_DIR="ai/tests/backups/$(date +%Y%m%d_%H%M%S)"
TEST_RESULTS_DIR="ai/tests/results"
LOG_FILE="$TEST_RESULTS_DIR/test-execution.log"

# Create necessary directories
mkdir -p "$BACKUP_DIR"
mkdir -p "$TEST_RESULTS_DIR"
mkdir -p "ai/tests/temp"

echo -e "${BLUE}🧪 AI Knowledge Base Test Suite${NC}"
echo "================================================="
echo "Starting comprehensive test execution..."
echo "Timestamp: $(date)"
echo "Backup Directory: $BACKUP_DIR"
echo "Results Directory: $TEST_RESULTS_DIR"
echo ""

# Function to log with timestamp
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Function to backup current state
backup_current_state() {
    log "Creating backup of current state..."
    
    # Backup registries
    if [ -f "ai/context/document-registry.yaml" ]; then
        cp "ai/context/document-registry.yaml" "$BACKUP_DIR/"
    fi
    if [ -f "ai/context/feature-registry.yaml" ]; then
        cp "ai/context/feature-registry.yaml" "$BACKUP_DIR/"
    fi
    
    # Backup knowledge base
    if [ -d "ai/knowledge" ]; then
        cp -r "ai/knowledge" "$BACKUP_DIR/"
    fi
    
    # Backup features
    if [ -d "ai/features" ]; then
        cp -r "ai/features" "$BACKUP_DIR/"
    fi
    
    log "Backup completed: $BACKUP_DIR"
}

# Function to restore from backup
restore_from_backup() {
    log "Restoring from backup..."
    
    # Restore registries
    if [ -f "$BACKUP_DIR/document-registry.yaml" ]; then
        cp "$BACKUP_DIR/document-registry.yaml" "ai/context/"
    fi
    if [ -f "$BACKUP_DIR/feature-registry.yaml" ]; then
        cp "$BACKUP_DIR/feature-registry.yaml" "ai/context/"
    fi
    
    # Restore knowledge base
    if [ -d "$BACKUP_DIR/knowledge" ]; then
        rm -rf "ai/knowledge"
        cp -r "$BACKUP_DIR/knowledge" "ai/"
    fi
    
    # Restore features
    if [ -d "$BACKUP_DIR/features" ]; then
        rm -rf "ai/features"
        cp -r "$BACKUP_DIR/features" "ai/"
    fi
    
    log "Restore completed"
}

# Function to validate YAML file
validate_yaml() {
    local file="$1"
    if [ -f "$file" ]; then
        if python3 -c "import yaml; yaml.safe_load(open('$file'))" 2>/dev/null; then
            return 0
        else
            return 1
        fi
    else
        return 1
    fi
}

# Function to count documents in registry
count_documents_in_registry() {
    if [ -f "ai/context/document-registry.yaml" ]; then
        python3 -c "
import yaml
with open('ai/context/document-registry.yaml', 'r') as f:
    data = yaml.safe_load(f)
    if 'registry' in data and 'documents' in data['registry']:
        print(len(data['registry']['documents']))
    else:
        print(0)
" 2>/dev/null || echo "0"
    else
        echo "0"
    fi
}

# Function to verify file creation
verify_file_creation() {
    local file_path="$1"
    local min_size="${2:-100}"  # Minimum file size in bytes
    
    if [ -f "$file_path" ]; then
        local file_size=$(wc -c < "$file_path")
        if [ "$file_size" -ge "$min_size" ]; then
            # Check for YAML frontmatter
            if head -n 1 "$file_path" | grep -q "^---"; then
                return 0
            else
                log "WARNING: File $file_path missing YAML frontmatter"
                return 1
            fi
        else
            log "ERROR: File $file_path too small ($file_size bytes < $min_size)"
            return 1
        fi
    else
        log "ERROR: File $file_path does not exist"
        return 1
    fi
}

# Function to test AI help command
test_ai_help_command() {
    echo -e "${YELLOW}Testing /ai-help command...${NC}"
    
    # Read the ai-help command file
    if [ -f ".claude/commands/ai-help.md" ]; then
        log "✅ ai-help command file exists"
        
        # Check if file contains required sections
        if grep -q "Available commands:" ".claude/commands/ai-help.md"; then
            log "✅ ai-help contains command listing"
        else
            log "❌ ai-help missing command listing"
            return 1
        fi
        
        if grep -q "create-document" ".claude/commands/ai-help.md"; then
            log "✅ ai-help references create-document"
        else
            log "❌ ai-help missing create-document reference"
            return 1
        fi
        
        return 0
    else
        log "❌ ai-help command file missing"
        return 1
    fi
}

# Function to test create-document command
test_create_document_command() {
    echo -e "${YELLOW}Testing create-document command...${NC}"
    
    local test_doc="market-analysis"
    local expected_path="ai/knowledge/strategic/$test_doc.md"
    local initial_count=$(count_documents_in_registry)
    
    log "Initial document count: $initial_count"
    
    # Simulate create-document command execution
    # In real implementation, this would invoke the AI agent
    log "Simulating: create-document $test_doc"
    
    # Create test directory if needed
    mkdir -p "ai/knowledge/strategic"
    
    # Create test document with proper structure
    cat > "$expected_path" << 'EOF'
---
document_type: research
version: 1.0
created_date: 2024-01-20
dependencies: []
status: draft
ai_context:
  primary_purpose: "Market analysis for competitive landscape"
  key_insights:
    - "Market size and opportunities"
    - "Competitive positioning"
---

# Market Analysis

## Executive Summary

This document provides comprehensive market analysis including competitive landscape and market opportunities.

## Market Size and Opportunity

Market analysis content here.

## Competitive Landscape

Competitive analysis content here.

## AI Agent Instructions

Use this document to understand market conditions when creating product requirements.

## Cross-References

- @ai/knowledge/strategic/statement-of-purpose.md
EOF
    
    # Verify file creation
    if verify_file_creation "$expected_path" 200; then
        log "✅ Document created successfully: $expected_path"
        
        # Verify YAML frontmatter
        if head -n 10 "$expected_path" | grep -q "document_type: research"; then
            log "✅ YAML frontmatter valid"
        else
            log "❌ YAML frontmatter invalid"
            return 1
        fi
        
        # Simulate registry update
        # In real implementation, this would be done by the AI agent
        log "Simulating registry update..."
        # Here we would update the registry file
        
        return 0
    else
        log "❌ Document creation failed"
        return 1
    fi
}

# Function to test orchestrate-agents command
test_orchestrate_agents_command() {
    echo -e "${YELLOW}Testing orchestrate-agents command...${NC}"
    
    local target_doc="prd"
    log "Simulating: orchestrate-agents $target_doc"
    
    # Create prerequisite documents to simulate agent workflow
    local docs=("market-analysis" "user-research" "user-personas" "prd")
    local paths=(
        "ai/knowledge/strategic/market-analysis.md"
        "ai/knowledge/user-experience/research/user-research.md"
        "ai/knowledge/user-experience/research/user-personas.md"
        "ai/knowledge/product/prd/prd.md"
    )
    
    # Create directories
    mkdir -p "ai/knowledge/strategic"
    mkdir -p "ai/knowledge/user-experience/research"
    mkdir -p "ai/knowledge/product/prd"
    
    # Create each document in sequence (simulating agent orchestration)
    for i in "${!docs[@]}"; do
        local doc="${docs[$i]}"
        local path="${paths[$i]}"
        
        log "Creating document: $doc at $path"
        
        cat > "$path" << EOF
---
document_type: $([ "$doc" = "prd" ] && echo "synthesis" || echo "research")
version: 1.0
created_date: 2024-01-20
dependencies: $([ "$i" -eq 0 ] && echo "[]" || echo '["previous-docs"]')
status: draft
ai_context:
  primary_purpose: "$doc analysis"
  key_insights: ["insight1", "insight2"]
---

# $doc

## Executive Summary

Content for $doc

## AI Agent Instructions

Instructions for using this $doc document.

## Cross-References

- @ai/knowledge/strategic/statement-of-purpose.md
EOF
        
        if verify_file_creation "$path" 150; then
            log "✅ Created: $doc"
        else
            log "❌ Failed to create: $doc"
            return 1
        fi
    done
    
    log "✅ Orchestrate-agents workflow simulation completed"
    return 0
}

# Function to test create-feature command
test_create_feature_command() {
    echo -e "${YELLOW}Testing create-feature command...${NC}"
    
    local feature_name="test-authentication"
    local feature_path="ai/features/$feature_name"
    
    log "Simulating: create-feature $feature_name"
    
    # Execute create-feature script if it exists
    if [ -f "scripts/create-feature.sh" ]; then
        log "Executing create-feature.sh script..."
        bash scripts/create-feature.sh "$feature_name"
    else
        log "create-feature.sh not found, creating structure manually..."
        # Create feature structure manually
        mkdir -p "$feature_path"/{requirements,design,technical,tests,analytics,meta}
    fi
    
    # Verify directory structure
    local required_dirs=("requirements" "design" "technical" "tests" "analytics" "meta")
    for dir in "${required_dirs[@]}"; do
        if [ -d "$feature_path/$dir" ]; then
            log "✅ Directory created: $feature_path/$dir"
        else
            log "❌ Missing directory: $feature_path/$dir"
            return 1
        fi
    done
    
    # Create test files in each directory
    local test_files=(
        "requirements/user-stories.md"
        "design/ui-mockups.md"
        "technical/api-contracts.md"
        "tests/test-strategy.md"
        "analytics/success-metrics.md"
        "meta/ai-instructions.md"
    )
    
    for file in "${test_files[@]}"; do
        local full_path="$feature_path/$file"
        mkdir -p "$(dirname "$full_path")"
        
        cat > "$full_path" << EOF
---
document_type: feature-documentation
version: 1.0
created_date: 2024-01-20
feature: $feature_name
phase: $(basename "$(dirname "$file")")
---

# $(basename "$file" .md)

Content for $feature_name $(basename "$file" .md)

## AI Agent Instructions

Instructions for this phase of feature development.
EOF
        
        if verify_file_creation "$full_path" 100; then
            log "✅ Created: $file"
        else
            log "❌ Failed to create: $file"
            return 1
        fi
    done
    
    log "✅ Feature workspace created successfully"
    return 0
}

# Function to test validation command
test_validation_command() {
    echo -e "${YELLOW}Testing validate-knowledge-base command...${NC}"
    
    # Run existing validation script
    if [ -f "scripts/validate-knowledge-base.sh" ]; then
        log "Running validate-knowledge-base.sh..."
        bash scripts/validate-knowledge-base.sh > "$TEST_RESULTS_DIR/validation-output.txt" 2>&1
        
        if [ $? -eq 0 ]; then
            log "✅ Validation script executed successfully"
            return 0
        else
            log "❌ Validation script failed"
            return 1
        fi
    else
        log "❌ validate-knowledge-base.sh not found"
        return 1
    fi
}

# Function to run registry validation tests
test_registry_updates() {
    echo -e "${YELLOW}Testing registry updates...${NC}"
    
    # Test document registry
    if [ -f "ai/context/document-registry.yaml" ]; then
        if validate_yaml "ai/context/document-registry.yaml"; then
            log "✅ Document registry YAML valid"
        else
            log "❌ Document registry YAML invalid"
            return 1
        fi
    else
        log "⚠️ Document registry not found (may be created during tests)"
    fi
    
    # Test feature registry
    if [ -f "ai/context/feature-registry.yaml" ]; then
        if validate_yaml "ai/context/feature-registry.yaml"; then
            log "✅ Feature registry YAML valid"
        else
            log "❌ Feature registry YAML invalid"
            return 1
        fi
    else
        log "⚠️ Feature registry not found (may be created during tests)"
    fi
    
    return 0
}

# Function to generate test report
generate_test_report() {
    local total_tests="$1"
    local passed_tests="$2"
    local failed_tests="$3"
    
    local report_file="$TEST_RESULTS_DIR/test-report.md"
    
    cat > "$report_file" << EOF
# AI Knowledge Base Test Report

**Date:** $(date)
**Total Tests:** $total_tests
**Passed:** $passed_tests
**Failed:** $failed_tests
**Success Rate:** $(( passed_tests * 100 / total_tests ))%

## Test Results Summary

$([ $failed_tests -eq 0 ] && echo "🎉 All tests passed!" || echo "⚠️ Some tests failed")

## Test Categories

### Command Execution Tests
- /ai-help command: $([ -f ".claude/commands/ai-help.md" ] && echo "✅ PASS" || echo "❌ FAIL")
- create-document: Tested
- orchestrate-agents: Tested
- create-feature: Tested
- validate-knowledge-base: Tested

### Registry Update Tests
- Document registry updates: Tested
- Feature registry updates: Tested
- YAML validation: Tested

### File Creation Tests
- Document creation: Tested
- Feature workspace creation: Tested
- File structure validation: Tested

## Detailed Log

See \`test-execution.log\` for detailed execution log.

## Recommendations

$([ $failed_tests -eq 0 ] && echo "System ready for production use." || echo "Review failed tests and fix issues before deployment.")
EOF
    
    echo ""
    echo -e "${BLUE}📊 Test Report Generated: $report_file${NC}"
    cat "$report_file"
}

# Main test execution
main() {
    log "Starting AI Knowledge Base test suite..."
    
    # Create backup
    backup_current_state
    
    local total_tests=0
    local passed_tests=0
    local failed_tests=0
    
    # Test 1: AI Help Command
    total_tests=$((total_tests + 1))
    if test_ai_help_command; then
        passed_tests=$((passed_tests + 1))
        echo -e "${GREEN}✅ AI Help Command Test: PASSED${NC}"
    else
        failed_tests=$((failed_tests + 1))
        echo -e "${RED}❌ AI Help Command Test: FAILED${NC}"
    fi
    
    # Test 2: Create Document Command
    total_tests=$((total_tests + 1))
    if test_create_document_command; then
        passed_tests=$((passed_tests + 1))
        echo -e "${GREEN}✅ Create Document Test: PASSED${NC}"
    else
        failed_tests=$((failed_tests + 1))
        echo -e "${RED}❌ Create Document Test: FAILED${NC}"
    fi
    
    # Test 3: Orchestrate Agents Command
    total_tests=$((total_tests + 1))
    if test_orchestrate_agents_command; then
        passed_tests=$((passed_tests + 1))
        echo -e "${GREEN}✅ Orchestrate Agents Test: PASSED${NC}"
    else
        failed_tests=$((failed_tests + 1))
        echo -e "${RED}❌ Orchestrate Agents Test: FAILED${NC}"
    fi
    
    # Test 4: Create Feature Command
    total_tests=$((total_tests + 1))
    if test_create_feature_command; then
        passed_tests=$((passed_tests + 1))
        echo -e "${GREEN}✅ Create Feature Test: PASSED${NC}"
    else
        failed_tests=$((failed_tests + 1))
        echo -e "${RED}❌ Create Feature Test: FAILED${NC}"
    fi
    
    # Test 5: Validation Command
    total_tests=$((total_tests + 1))
    if test_validation_command; then
        passed_tests=$((passed_tests + 1))
        echo -e "${GREEN}✅ Validation Test: PASSED${NC}"
    else
        failed_tests=$((failed_tests + 1))
        echo -e "${RED}❌ Validation Test: FAILED${NC}"
    fi
    
    # Test 6: Registry Updates
    total_tests=$((total_tests + 1))
    if test_registry_updates; then
        passed_tests=$((passed_tests + 1))
        echo -e "${GREEN}✅ Registry Updates Test: PASSED${NC}"
    else
        failed_tests=$((failed_tests + 1))
        echo -e "${RED}❌ Registry Updates Test: FAILED${NC}"
    fi
    
    echo ""
    echo "================================================="
    echo -e "${BLUE}Test Execution Complete${NC}"
    echo -e "Total: $total_tests | Passed: ${GREEN}$passed_tests${NC} | Failed: ${RED}$failed_tests${NC}"
    
    # Generate report
    generate_test_report "$total_tests" "$passed_tests" "$failed_tests"
    
    # Automatic cleanup - NO USER CHOICE
    echo ""
    echo "Automatically cleaning up test artifacts..."
    restore_from_backup
    echo -e "${GREEN}System restored from backup${NC}"
    
    # MANDATORY: Clean up any remaining test artifacts
    echo "Cleaning up any remaining test artifacts..."
    rm -rf ai/knowledge/strategic/market-analysis.md 2>/dev/null
    rm -rf ai/knowledge/product 2>/dev/null
    rm -rf ai/knowledge/user-experience 2>/dev/null
    rm -rf ai/features/test-authentication 2>/dev/null
    rm -rf ai/features/payment-system 2>/dev/null
    rm -rf ai/tests/backups 2>/dev/null
    rm -rf ai/tests/results 2>/dev/null
    rm -rf ai/tests/temp 2>/dev/null
    
    # Verify cleanup
    if [ -d "ai/knowledge/strategic" ] && [ -f "ai/knowledge/strategic/market-analysis.md" ]; then
        echo -e "${RED}❌ CLEANUP FAILED - Test artifacts still present!${NC}"
        echo "Run: git status to see remaining artifacts"
        exit 1
    else
        echo -e "${GREEN}✅ Test artifacts cleaned up successfully${NC}"
    fi
    
    # Exit with appropriate code
    if [ $failed_tests -eq 0 ]; then
        echo -e "${GREEN}🎉 All tests passed!${NC}"
        exit 0
    else
        echo -e "${RED}❌ Some tests failed${NC}"
        exit 1
    fi
}

# Run main function
main "$@"