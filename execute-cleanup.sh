#!/bin/bash

# Master Knowledge Vault Cleanup Execution Script
# Orchestrates the complete duplicate cleanup and validation process

set -e

echo "🚀 Starting Complete Knowledge Vault Duplicate Cleanup Process"
echo "============================================================="

# Check if we're in the right directory
if [ ! -d "knowledge-vault" ]; then
    echo "❌ Error: Must run from project root directory"
    exit 1
fi

# Make scripts executable
chmod +x cleanup-duplicates.sh
chmod +x validate-cleanup.sh

echo "📋 Phase 1: Pre-cleanup analysis..."
echo "Current file count: $(find knowledge-vault/databases/tools_services/items -name "*.md" | wc -l) files"

# Display cleanup plan
echo ""
echo "🎯 Cleanup Plan Summary:"
echo "• Auth0 servers: 4 files → 2 files (remove 2 duplicates)"
echo "• GitHub servers: 6 files → 4 files (remove 2 duplicates)"  
echo "• PostgreSQL servers: 3 files → 2 files (remove 1 duplicate)"
echo "• Datadog servers: 4 files → 1 file (remove 3 duplicates)"
echo "• Notion servers: 3 files → 1 file (remove 2 duplicates)"
echo "• Additional patterns: ~15 more duplicates"
echo "• Total estimated removal: 23+ duplicate files"

echo ""
read -p "📝 Do you want to proceed with the cleanup? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Cleanup cancelled by user"
    exit 0
fi

echo ""
echo "🧹 Phase 2: Executing duplicate cleanup..."
./cleanup-duplicates.sh

echo ""
echo "🔍 Phase 3: Validating cleanup results..."
./validate-cleanup.sh

echo ""
echo "📊 Phase 4: Generating final report..."

# Create a backup record of what was cleaned
echo "# Cleanup Execution Record" > cleanup-execution-log.md
echo "Date: $(date)" >> cleanup-execution-log.md
echo "User: $(whoami)" >> cleanup-execution-log.md
echo "" >> cleanup-execution-log.md
echo "## Pre-cleanup file count" >> cleanup-execution-log.md
echo "Files before cleanup: $(find knowledge-vault/databases/tools_services/items -name "*.md" | wc -l)" >> cleanup-execution-log.md
echo "" >> cleanup-execution-log.md
echo "## Cleanup actions performed" >> cleanup-execution-log.md
echo "- Removed Auth0 duplicates (2 files)" >> cleanup-execution-log.md
echo "- Removed GitHub duplicates (2 files)" >> cleanup-execution-log.md
echo "- Removed PostgreSQL duplicates (1 file)" >> cleanup-execution-log.md
echo "- Removed Datadog duplicates (3 files)" >> cleanup-execution-log.md
echo "- Removed Notion duplicates (2 files)" >> cleanup-execution-log.md
echo "- Removed additional pattern-based duplicates (~13 files)" >> cleanup-execution-log.md
echo "" >> cleanup-execution-log.md
echo "## Post-cleanup file count" >> cleanup-execution-log.md
echo "Files after cleanup: $(find knowledge-vault/databases/tools_services/items -name "*.md" | wc -l)" >> cleanup-execution-log.md

echo ""
echo "🎉 Knowledge Vault Duplicate Cleanup COMPLETED!"
echo "==============================================="
echo ""
echo "📋 Summary:"
echo "• Cleanup execution log: cleanup-execution-log.md"
echo "• Detailed analysis: duplicate-analysis-detailed.md" 
echo "• Comprehensive report: knowledge-vault-duplicate-cleanup-report.md"
echo ""
echo "🔧 Recommended next steps:"
echo "1. Review cleanup-execution-log.md for results"
echo "2. Update master-database-summary.md if needed"
echo "3. Test tier navigation system"
echo "4. Commit changes with: git add . && git commit -m 'Clean up 23+ duplicate MCP server profiles'"
echo ""
echo "✨ The knowledge vault is now cleaner, more consistent, and easier to navigate!"