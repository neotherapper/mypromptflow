#!/bin/bash

echo "🔍 Validating AI Knowledge Base..."

# Check directory structure
echo "Checking directory structure..."
required_dirs=(
    ".claude/commands"
    "ai/context/"
    "ai/features/_template/design"
    "ai/features/_template/meta"
    "ai/features/_template/requirements"
    "ai/features/_template/technical"
    "ai/features/_template/tests"
    "ai/features/_template/user-authentication"
    "ai/knowledge/product/prd"
    "ai/knowledge/product/strategic"
    "ai/knowledge/quality-assurance"
    "ai/knowledge/technical"
    "ai/knowledge/user-experience/design"
    "ai/knowledge/strategic"
    "ai/prompts/document-templates"
    "ai/prompts/meta"
    "ai/prompts/meta-prompts"
    "ai/scratchpads/"
    "ai/tests/"

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
    "ai/context/document-registry.yaml"
    "ai/context/feature-registry.yaml"
    "ai/features/_template/design/ui-mockups.md"
    "ai/features/_template/meta/ai-instructions.md"
    "ai/features/_template/requirements/acceptance-criteria.md"
    "ai/features/_template/requirements/user-stories.md"
    "ai/features/_template/technical/api-contracts.md"
    "ai/features/_template/technical/data-models.md"
    "ai/features/_template/tests/test-strategy.md"
    "ai/features/_template/feature-spec.md"
    "ai/features/_template/README.md"
    "ai/features/user-authentication/feature-spec.md"
    "ai/tests/ai-context-tests.yaml"
    "ai/tests/dependency-validation-tests.yaml"
    "ai/tests/document-structure-tests.yaml"

)

for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file missing"
    fi
done

echo -e "\n✨ Validation complete!"