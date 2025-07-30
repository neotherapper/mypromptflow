#!/bin/bash

# Knowledge Vault Cleanup Validation Script
# Validates the integrity of the knowledge vault after duplicate cleanup

set -e

echo "🔍 Validating Knowledge Vault Post-Cleanup Integrity..."

BASE_DIR="knowledge-vault/databases/tools_services/items"

# Check if we're in the right directory
if [ ! -d "knowledge-vault" ]; then
    echo "❌ Error: Must run from project root directory"
    exit 1
fi

echo ""
echo "📊 Current Statistics:"
echo "Total files: $(find $BASE_DIR -name "*.md" | wc -l)"
echo "Total lines: $(find $BASE_DIR -name "*.md" -exec wc -l {} + | tail -1 | awk '{print $1}')"

echo ""
echo "🎯 Validating Critical Server Preservation..."

# Critical servers that must exist
critical_servers=(
    "auth0-identity-platform-server-profile.md:Auth0 (Tier 1)"
    "github-mcp-server.md:GitHub (Core Platform)"
    "notion-mcp-server.md:Notion (Original)"
    "postgresql-mcp-server-enhanced.md:PostgreSQL (Enhanced)"
    "datadog-mcp-server.md:Datadog (Core)"
    "stripe-mcp-server-payment-processing-platform.md:Stripe (Platform)"
    "openai-mcp-server.md:OpenAI (Core)"
    "fetch-mcp-server.md:Fetch (Core)"
    "sqlite-mcp-server-database.md:SQLite (Database)"
)

preserved_count=0
for server_info in "${critical_servers[@]}"; do
    filename=$(echo $server_info | cut -d: -f1)  
    description=$(echo $server_info | cut -d: -f2)
    
    if [ -f "$BASE_DIR/$filename" ]; then
        echo "✅ $description preserved"
        preserved_count=$((preserved_count + 1))
    else
        echo "❌ MISSING: $description ($filename)"
    fi
done

echo ""
echo "📈 Preservation Score: $preserved_count/${#critical_servers[@]} critical servers preserved"

echo ""
echo "🚫 Validating Duplicate Removal..."

# Files that should have been deleted
deleted_files=(
    "auth0-identity-mcp-server-comprehensive-profile.md:Auth0 Duplicate (Q:8.6)"
    "auth0-enhanced-mcp-server-comprehensive-enterprise-implementation-profile.md:Auth0 Duplicate (Q:6.2)"
    "tier-1-github-mcp-server-detailed-profile.md:GitHub Backup Duplicate"
    "github-mcp-server-platform.md:GitHub Platform Duplicate"
    "tier-1-postgresql-mcp-server-detailed-profile.md:PostgreSQL Backup Duplicate"
    "datadog-comprehensive-monitoring-mcp-server.md:Datadog Duplicate"
    "notion-server-profile.md:Notion Profile Duplicate"
)

removed_count=0
for file_info in "${deleted_files[@]}"; do
    filename=$(echo $file_info | cut -d: -f1)
    description=$(echo $file_info | cut -d: -f2)
    
    if [ ! -f "$BASE_DIR/$filename" ]; then
        echo "✅ Removed: $description"
        removed_count=$((removed_count + 1))
    else
        echo "⚠️  Still exists: $description ($filename)"
    fi
done

echo ""
echo "🗑️  Removal Score: $removed_count/${#deleted_files[@]} duplicates successfully removed"

echo ""
echo "🔗 Validating Cross-References..."

# Check if master database summary needs updating
if grep -q "auth0-identity-mcp-server-comprehensive-profile" "$BASE_DIR/master-database-summary.md" 2>/dev/null; then
    echo "⚠️  master-database-summary.md contains references to deleted files"
    echo "🔧 Manual update required"
else
    echo "✅ No problematic references found in master-database-summary.md"
fi

echo ""
echo "📋 Schema Compliance Check..."

# Sample a few files for schema compliance
schema_compliant=0
schema_total=5

test_files=(
    "auth0-identity-platform-server-profile.md"
    "github-mcp-server.md" 
    "postgresql-mcp-server-enhanced.md"
    "notion-mcp-server.md"
    "datadog-mcp-server.md"
)

for test_file in "${test_files[@]}"; do
    if [ -f "$BASE_DIR/$test_file" ]; then
        # Check for required YAML frontmatter fields
        if grep -q "^id:" "$BASE_DIR/$test_file" && \
           grep -q "^name:" "$BASE_DIR/$test_file" && \
           grep -q "^item_type:" "$BASE_DIR/$test_file"; then
            echo "✅ Schema compliant: $test_file"
            schema_compliant=$((schema_compliant + 1))
        else
            echo "❌ Schema issues: $test_file"
        fi
    fi
done

echo ""
echo "📊 Schema Compliance: $schema_compliant/$schema_total files checked"

echo ""
echo "🏆 Overall Validation Results:"

# Calculate overall score
total_possible=100
preservation_score=$((preserved_count * 100 / ${#critical_servers[@]}))
removal_score=$((removed_count * 100 / ${#deleted_files[@]}))
schema_score=$((schema_compliant * 100 / schema_total))

overall_score=$(((preservation_score + removal_score + schema_score) / 3))

echo "   🎯 Critical File Preservation: $preservation_score%"
echo "   🗑️  Duplicate Removal: $removal_score%"  
echo "   📋 Schema Compliance: $schema_score%"
echo "   🏆 Overall Success Score: $overall_score%"

if [ $overall_score -ge 90 ]; then
    echo ""
    echo "🎉 EXCELLENT: Cleanup completed successfully with high integrity!"
elif [ $overall_score -ge 75 ]; then
    echo ""
    echo "✅ GOOD: Cleanup completed with minor issues requiring attention"
else
    echo ""
    echo "⚠️  WARNING: Cleanup completed but significant issues detected"
    echo "🔧 Manual review and corrections recommended"
fi

echo ""
echo "🔧 Recommended Next Steps:"
echo "1. Update master-database-summary.md to remove deleted file references"
echo "2. Test tier navigation system functionality"
echo "3. Run full schema validation across all remaining files"
echo "4. Generate updated quality metrics report"
echo "5. Commit changes with descriptive message"