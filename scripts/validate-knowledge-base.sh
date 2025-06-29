#!/bin/bash

echo "🔍 Validating AI Knowledge Base..."

# Check directory structure
echo "Checking directory structure..."
required_dirs=(
    ".claude/commands"
    ".claude/prompts/meta-prompts"
    ".claude/prompts/document-templates/tier1"
    ".claude/prompts/document-templates/tier2"
    ".claude/prompts/document-templates/tier3"
    ".claude/prompts/document-templates/tier4"
    ".claude/tests"
    "ai/context"
    "ai/knowledge/strategic"
    "ai/knowledge/product/prd"
    "ai/knowledge/product/epics"
    "ai/knowledge/product/user-stories"
    "ai/knowledge/product/acceptance-criteria"
    "ai/knowledge/product/release-notes"
    "ai/knowledge/user-experience/research/user-interviews"
    "ai/knowledge/user-experience/research/usability-testing"
    "ai/knowledge/user-experience/research/empathy-maps"
    "ai/knowledge/user-experience/design"
    "ai/knowledge/user-experience/journey-maps"
    "ai/knowledge/technical/api"
    "ai/knowledge/technical/database/schemas"
    "ai/knowledge/technical/architecture/c4-diagrams"
    "ai/knowledge/technical/security"
    "ai/knowledge/business-analysis"
    "ai/knowledge/quality-assurance/test-plans"
    "ai/knowledge/quality-assurance/test-cases"
    "ai/knowledge/quality-assurance/uat-plans"
    "ai/knowledge/compliance/security-docs"
    "ai/features/_template/requirements"
    "ai/features/_template/design"
    "ai/features/_template/technical"
    "ai/features/_template/tests"
    "ai/features/_template/analytics"
    "ai/features/_template/meta"
    "ai/agents/tier-specialists"
    "ai/agents/feature-specialists"
    "ai/agents/orchestrator"
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
    ".claude/settings.json"
    ".claude/tests/document-structure-tests.yaml"
    ".claude/tests/dependency-validation-tests.yaml"
    ".claude/tests/ai-context-tests.yaml"
    "ai/context/dependencies.yaml"
    "ai/context/document-registry.yaml"
    "ai/context/feature-registry.yaml"
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