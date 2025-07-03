#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: ./create-feature.sh <feature-name>"
    exit 1
fi

FEATURE_NAME=$1
FEATURE_PATH="ai/features/$FEATURE_NAME"

echo "🚀 Creating feature workspace for: $FEATURE_NAME"

# Create directory structure
mkdir -p "$FEATURE_PATH"/{requirements,design,technical,tests,analytics,meta}

# Copy templates
cp -r ai/features/_template/* "$FEATURE_PATH/"

# Replace placeholders
find "$FEATURE_PATH" -type f -name "*.md" -exec sed -i "" "s/{FEATURE_NAME}/$FEATURE_NAME/g" {} \;
find "$FEATURE_PATH" -type f -name "*.md" -exec sed -i "" "s/{DATE}/$(date +%Y-%m-%d)/g" {} \;

echo "✅ Feature workspace created at: $FEATURE_PATH"
echo ""
echo "Next steps:"
echo "1. Review and edit $FEATURE_PATH/feature-spec.md"
echo "2. Run: /create-feature $FEATURE_NAME in Claude Code"
echo "3. Agents will populate remaining documentation"