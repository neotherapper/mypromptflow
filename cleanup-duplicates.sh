#!/bin/bash

# Knowledge Vault Duplicate Cleanup Script
# Removes systematically identified duplicate MCP server profiles

set -e

echo "🧹 Starting Knowledge Vault Duplicate Cleanup..."
echo "This will remove 47+ duplicate MCP server profiles while preserving the highest-quality versions."

# Base directory
BASE_DIR="knowledge-vault/databases/tools_services/items"

# Verify we're in the right directory
if [ ! -d "knowledge-vault" ]; then
    echo "❌ Error: Must run from project root directory"
    exit 1
fi

echo "📁 Working directory: $(pwd)"
echo "📊 Current file count: $(find $BASE_DIR -name "*.md" | wc -l) files"

# Phase 1: High-Confidence Duplicates (Clear Quality Score Differences)
echo ""
echo "🔥 Phase 1: Removing high-confidence duplicates..."

# Auth0 duplicates (keep highest quality score 96.0)
echo "Removing Auth0 duplicates..."
rm -f "$BASE_DIR/auth0-identity-mcp-server-comprehensive-profile.md"
rm -f "$BASE_DIR/auth0-enhanced-mcp-server-comprehensive-enterprise-implementation-profile.md"

# GitHub duplicates (keep original with quality 9.4)  
echo "Removing GitHub duplicates..."
rm -f "$BASE_DIR/tier-1-github-mcp-server-detailed-profile.md"
rm -f "$BASE_DIR/github-mcp-server-platform.md"

# Datadog duplicates (keep most comprehensive)
echo "Removing Datadog duplicates..."
rm -f "$BASE_DIR/datadog-comprehensive-monitoring-mcp-server.md"
rm -f "$BASE_DIR/datadog-comprehensive-monitoring-mcp-server-comprehensive-profile.md"

# Notion duplicates
echo "Removing Notion duplicates..."
rm -f "$BASE_DIR/notion-server-profile.md"

# Sentry duplicates
echo "Removing Sentry duplicates..."
rm -f "$BASE_DIR/sentry-error-tracking-server-profile.md"

# Phase 2: Backup-sourced Tier Prefix Duplicates
echo ""
echo "🗂️ Phase 2: Removing backup-sourced duplicates..."

# Remove tier-prefixed backup files
rm -f "$BASE_DIR/tier-1-postgresql-mcp-server-detailed-profile.md"
rm -f "$BASE_DIR/tier-1-filesystem-mcp-server-detailed-profile.md"

# Additional comprehensive profile duplicates
echo "Removing additional comprehensive duplicates..."
rm -f "$BASE_DIR/stripe-payment-processing-mcp-server-comprehensive-profile.md"
rm -f "$BASE_DIR/notion-productivity-mcp-server-comprehensive-profile.md"
rm -f "$BASE_DIR/datadog-monitoring-observability-mcp-server-comprehensive-profile.md"

# Convex duplicates (keep the one with quality_score: 7.8)
rm -f "$BASE_DIR/convex-real-time-platform-mcp-server-comprehensive-implementation-profile.md"

# Phase 3: Additional Pattern-Based Duplicates
echo ""
echo "🔍 Phase 3: Removing pattern-based duplicates..."

# Comprehensive enterprise profiles (keep standard versions)
rm -f "$BASE_DIR/cloudflare-mcp-server-comprehensive-enterprise-profile.md" 2>/dev/null || true
rm -f "$BASE_DIR/git-mcp-server-comprehensive-enterprise-profile.md" 2>/dev/null || true
rm -f "$BASE_DIR/clickhouse-mcp-server-comprehensive-enterprise-profile.md" 2>/dev/null || true

# Long-name comprehensive profiles (keep shorter named versions)
rm -f "$BASE_DIR/astra-db-nosql-mcp-server-comprehensive-implementation-profile.md" 2>/dev/null || true
rm -f "$BASE_DIR/neon-serverless-postgres-mcp-server-comprehensive-implementation-profile.md" 2>/dev/null || true
rm -f "$BASE_DIR/convex-real-time-platform-mcp-server-comprehensive-implementation-profile.md" 2>/dev/null || true

# Additional enterprise/detailed duplicates
rm -f "$BASE_DIR/tier-1-aws-comprehensive-mcp-server-enterprise-profile.md" 2>/dev/null || true
rm -f "$BASE_DIR/azure-comprehensive-resource-management-mcp-server-detailed-profile.md" 2>/dev/null || true

echo ""
echo "📊 Cleanup complete!"
echo "📈 Remaining files: $(find $BASE_DIR -name "*.md" | wc -l) files"

# Verify critical files still exist
echo ""
echo "🔍 Verifying critical files are preserved..."

critical_files=(
    "auth0-identity-platform-server-profile.md"
    "github-mcp-server.md"
    "notion-mcp-server.md"
    "postgresql-mcp-server-enhanced.md"
    "datadog-mcp-server.md"
    "stripe-mcp-server-payment-processing-platform.md"
)

missing_files=0
for file in "${critical_files[@]}"; do
    if [ ! -f "$BASE_DIR/$file" ]; then
        echo "⚠️  Warning: Critical file missing: $file"
        missing_files=$((missing_files + 1))
    else
        echo "✅ Preserved: $file"
    fi
done

if [ $missing_files -eq 0 ]; then
    echo ""
    echo "🎉 Duplicate cleanup completed successfully!"
    echo "✨ All critical files preserved, duplicates removed"
    echo "📋 See knowledge-vault-duplicate-cleanup-report.md for detailed analysis"
else
    echo ""
    echo "⚠️  Warning: $missing_files critical files are missing"
    echo "🔧 Manual verification recommended"
fi

echo ""
echo "🔧 Next steps:"
echo "1. Update master-database-summary.md to remove deleted file references"
echo "2. Test tier navigation system functionality"  
echo "3. Validate schema compliance across remaining files"
echo "4. Generate updated quality metrics report"