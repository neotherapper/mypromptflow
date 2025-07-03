#!/bin/bash

# Function to create a file with content only if it doesn't exist
create_file_if_not_exists() {
    local file_path="$1"
    local content="$2"
    if [ ! -f "$file_path" ]; then
        echo "$content" > "$file_path"
    fi
}

# Create .claude files
create_file_if_not_exists ".claude/settings.json" "{}"
create_file_if_not_exists ".claude/tests/document-structure-tests.yaml" ""
create_file_if_not_exists ".claude/tests/dependency-validation-tests.yaml" ""
create_file_if_not_exists ".claude/tests/ai-context-tests.yaml" ""

# Create .claude/commands files
create_file_if_not_exists ".claude/commands/analyse-dependencies.md" "# Analyse Dependencies"
create_file_if_not_exists ".claude/commands/create-document.md" "# Create Document"
create_file_if_not_exists ".claude/commands/create-feature.md" "# Create Feature"
create_file_if_not_exists ".claude/commands/generate-tier-documents.md" "# Generate Tier Documents"
create_file_if_not_exists ".claude/commands/gh-issue.md" "# GH Issue"
create_file_if_not_exists ".claude/commands/orchestrate-agents.md" "# Orchestrate Agents"
create_file_if_not_exists ".claude/commands/validate-knowledge-base.md" "# Validate Knowledge Base"