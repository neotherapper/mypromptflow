#!/bin/bash

# MCP Server Discovery and Analysis Script
# Automated discovery and analysis of knowledge-vault MCP servers for domain mapping

PROJECT_ROOT="/Users/georgiospilitsoglou/Developer/projects/mypromptflow"
KNOWLEDGE_VAULT_ITEMS="$PROJECT_ROOT/knowledge-vault/databases/tools_services/items"
DOMAIN_MAPPINGS="$PROJECT_ROOT/ai/mcp-integration/domain-server-mappings.yaml"
OUTPUT_DIR="$PROJECT_ROOT/ai/mcp-integration/analysis"

# Create output directory
mkdir -p "$OUTPUT_DIR"

echo "🔍 MCP Server Discovery and Analysis"
echo "======================================"

# Count total servers
TOTAL_SERVERS=$(find "$KNOWLEDGE_VAULT_ITEMS" -name "*.md" | wc -l | tr -d ' ')
echo "📊 Total MCP servers in knowledge-vault: $TOTAL_SERVERS"

# Count servers already in domain mappings  
CURRENT_SERVERS=$(grep -c "server_id:" "$DOMAIN_MAPPINGS" || echo "0")
echo "📊 Current servers in domain mappings: $CURRENT_SERVERS"

echo "📊 Coverage gap: $((TOTAL_SERVERS - CURRENT_SERVERS)) servers not yet mapped"
echo ""

# Analyze servers by category
echo "🏷️  Server Analysis by Category"
echo "==============================="

# Extract categories from frontmatter
echo "Top 10 Categories:"
find "$KNOWLEDGE_VAULT_ITEMS" -name "*.md" -exec grep -l "^category:" {} \; | \
while read file; do
    grep "^category:" "$file" | sed 's/category: //' | tr -d '"'
done | sort | uniq -c | sort -nr | head -10

echo ""
echo "🎯 High-Quality Servers (Quality Score >= 8.0)"
echo "=============================================="

# Find high-quality servers not yet in domain mappings
find "$KNOWLEDGE_VAULT_ITEMS" -name "*.md" | while read file; do
    filename=$(basename "$file" .md)
    
    # Check if already in domain mappings
    if ! grep -q "$filename" "$DOMAIN_MAPPINGS" 2>/dev/null; then
        # Extract quality score and name
        quality_score=$(grep "^quality_score:" "$file" 2>/dev/null | sed 's/quality_score: //' | tr -d ' ')
        name=$(grep "^name:" "$file" 2>/dev/null | sed 's/name: //' | tr -d '"')
        category=$(grep "^category:" "$file" 2>/dev/null | sed 's/category: //' | tr -d '"')
        
        # Check if quality score is >= 8.0
        if [[ -n "$quality_score" ]] && (( $(echo "$quality_score >= 8.0" | bc -l 2>/dev/null || echo "0") )); then
            echo "⭐ $name (Score: $quality_score, Category: $category)"
            echo "   File: $filename.md"
            echo ""
        fi
    fi
done > "$OUTPUT_DIR/high_quality_unmapped_servers.txt"

# Display results
if [[ -s "$OUTPUT_DIR/high_quality_unmapped_servers.txt" ]]; then
    head -20 "$OUTPUT_DIR/high_quality_unmapped_servers.txt"
    echo ""
    echo "💾 Full results saved to: $OUTPUT_DIR/high_quality_unmapped_servers.txt"
else
    echo "✅ All high-quality servers appear to be mapped!"
fi

echo ""
echo "🔍 Tier Analysis"
echo "==============="

echo "Tier 1 servers not yet mapped:"
find "$KNOWLEDGE_VAULT_ITEMS" -name "*.md" | while read file; do
    filename=$(basename "$file" .md)
    
    if ! grep -q "$filename" "$DOMAIN_MAPPINGS" 2>/dev/null; then
        tier=$(grep "^tier:" "$file" 2>/dev/null | sed 's/tier: //' | tr -d '"')
        name=$(grep "^name:" "$file" 2>/dev/null | sed 's/name: //' | tr -d '"')
        
        if [[ "$tier" == "Tier 1" ]]; then
            echo "🥇 $name (File: $filename.md)"
        fi
    fi
done | head -10

echo ""
echo "📈 Domain Suggestions"
echo "==================="

# Suggest new domains based on uncategorized servers
echo "Potential new domains based on server categories:"

find "$KNOWLEDGE_VAULT_ITEMS" -name "*.md" -exec grep -l "^category:" {} \; | \
while read file; do
    filename=$(basename "$file" .md)
    if ! grep -q "$filename" "$DOMAIN_MAPPINGS" 2>/dev/null; then
        grep "^category:" "$file" | sed 's/category: //' | tr -d '"'
    fi
done | sort | uniq -c | sort -nr | head -10 | while read count category; do
    echo "📂 $category ($count servers)"
done

echo ""
echo "🎯 Maritime-Specific Recommendations"
echo "==================================="

echo "Servers relevant to maritime insurance platform:"
find "$KNOWLEDGE_VAULT_ITEMS" -name "*.md" | while read file; do
    filename=$(basename "$file" .md)
    name=$(grep "^name:" "$file" 2>/dev/null | sed 's/name: //' | tr -d '"' | tr '[:upper:]' '[:lower:]')
    description=$(grep "^description:" "$file" 2>/dev/null | sed 's/description: //' | tr -d '"' | tr '[:upper:]' '[:lower:]')
    
    # Look for maritime, insurance, financial, or business-related keywords
    if echo "$name $description" | grep -qE "(financial|business|payment|insurance|audit|compliance|security|monitoring|database|api|auth|crm)"; then
        if ! grep -q "$filename" "$DOMAIN_MAPPINGS" 2>/dev/null; then
            server_name=$(grep "^name:" "$file" 2>/dev/null | sed 's/name: //' | tr -d '"')
            category=$(grep "^category:" "$file" 2>/dev/null | sed 's/category: //' | tr -d '"')
            quality_score=$(grep "^quality_score:" "$file" 2>/dev/null | sed 's/quality_score: //' | tr -d ' ')
            
            echo "🚢 $server_name"
            echo "   Category: $category, Quality: $quality_score"
            echo "   File: $filename.md"
            echo ""
        fi
    fi
done | head -20

echo ""
echo "✅ Analysis Complete!"
echo "📊 Results saved in: $OUTPUT_DIR/"
echo ""
echo "🚀 Next Steps:"
echo "1. Review high-quality unmapped servers"
echo "2. Consider new domains for uncategorized servers"
echo "3. Add maritime-specific servers to appropriate domains"
echo "4. Update cross-domain mappings for enhanced workflows"