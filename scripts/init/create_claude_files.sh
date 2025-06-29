#!/bin/bash

# Create .claude files
touch .claude/settings.json
touch .claude/tests/{document-structure-tests.yaml,dependency-validation-tests.yaml,ai-context-tests.yaml}

# Create .claude/commands files
echo "# Analyse Dependencies" > .claude/commands/analyse-dependencies.md
echo "# Create Document" > .claude/commands/create-document.md
echo "# Create Feature" > .claude/commands/create-feature.md
echo "# Generate Tier Documents" > .claude/commands/generate-tier-documents.md
echo "# GH Issue" > .claude/commands/gh-issue.md
echo "# Orchestrate Agents" > .claude/commands/orchestrate-agents.md
echo "# Validate Knowledge Base" > .claude/commands/validate-knowledge-base.md
