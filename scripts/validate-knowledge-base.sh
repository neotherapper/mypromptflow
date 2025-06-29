#!/bin/bash

echo "🔍 Validating AI Knowledge Base..."

# Check directory structure
echo "Checking directory structure..."
required_dirs=(
    ".claude/commands"
    ".claude/prompts/meta-prompts"
    ".claude/prompts/document-templates"
    "ai/knowledge/strategic"
    "ai/knowledge/product"
    "ai/knowledge/technical"
    "ai/features"
)

for dir in "${required_dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "✅ $dir exists"
    else
        echo "❌ $dir missing"
    fi
done

# Check required files
echo -e "\nChecking configuration files..."
required_files=(
    ".claude/CLAUDE.md"
    "ai/context/dependencies.yaml"
    "ai/context/tier-configuration.yaml"
)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file missing"
    fi
done

echo -e "\n✨ Validation complete!"