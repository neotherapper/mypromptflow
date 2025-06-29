#!/bin/bash

# Function to create a file with content only if it doesn't exist
create_file_if_not_exists() {
    local file_path="$1"
    local content="$2"
    if [ ! -f "$file_path" ]; then
        echo "$content" > "$file_path"
    fi
}

# Create ai/context files
create_file_if_not_exists "ai/context/dependencies.yaml" ""
create_file_if_not_exists "ai/context/document-registry.yaml" ""
create_file_if_not_exists "ai/context/feature-registry.yaml" ""
create_file_if_not_exists "ai/context/tier-configuration.yaml" ""

# Create ai/features/_template files
create_file_if_not_exists "ai/features/_template/feature-spec.md" "# Feature Spec"
create_file_if_not_exists "ai/features/_template/README.md" "# README"
create_file_if_not_exists "ai/features/_template/design/ui-mockups.md" "# UI Mockups"
create_file_if_not_exists "ai/features/_template/meta/ai-instructions.md" "# AI Instructions"
create_file_if_not_exists "ai/features/_template/requirements/acceptance-criteria.md" "# Acceptance Criteria"
create_file_if_not_exists "ai/features/_template/requirements/user-stories.md" "# User Stories"
create_file_if_not_exists "ai/features/_template/technical/api-contracts.md" "# API Contracts"
create_file_if_not_exists "ai/features/_template/technical/data-models.md" "# Data Models"
create_file_if_not_exists "ai/features/_template/tests/test-strategy.md" "# Test Strategy"

# Create ai/features/user-authentication files
create_file_if_not_exists "ai/features/user-authentication/feature-spec.md" "# Feature Spec"

# Create ai/prompts files
create_file_if_not_exists "ai/prompts/1_discover_tools.md" "# Discover Tools"
create_file_if_not_exists "ai/prompts/2_extract_features.md" "# Extract Features"
create_file_if_not_exists "ai/prompts/3_map_features_to_framework.md" "# Map Features to Framework"

# Create ai/prompts/document-templates files
create_file_if_not_exists "ai/prompts/document-templates/tier1/api-documentation.md" "# API Documentation"
create_file_if_not_exists "ai/prompts/document-templates/tier1/database-schemas.md" "# Database Schemas"
create_file_if_not_exists "ai/prompts/document-templates/tier2/prd.md" "# PRD"
create_file_if_not_exists "ai/prompts/document-templates/tier3/user-stories.md" "# User Stories"
create_file_if_not_exists "ai/prompts/document-templates/tier4/user-personas.md" "# User Personas"

# Create ai/prompts/meta-prompts files
create_file_if_not_exists "ai/prompts/meta-prompts/dependency-analyzer.md" "# Dependency Analyzer"
create_file_if_not_exists "ai/prompts/meta-prompts/document-generator.md" "# Document Generator"
create_file_if_not_exists "ai/prompts/meta-prompts/feature-orchestrator.md" "# Feature Orchestrator"
create_file_if_not_exists "ai/prompts/meta-prompts/quality-validator.md" "# Quality Validator"
create_file_if_not_exists "ai/prompts/meta-prompts/tier-orchestrator.md" "# Tier Orchestrator"

# Create ai/prompts/meta files
create_file_if_not_exists "ai/prompts/meta/adaptive_chain_of_thought.md" "# Adaptive Chain of Thought"
create_file_if_not_exists "ai/prompts/meta/complex_research.md" "# Complex Research"
create_file_if_not_exists "ai/prompts/meta/domain_adaptive.md" "# Domain Adaptive"
create_file_if_not_exists "ai/prompts/meta/domain_specific_research.md" "# Domain Specific Research"
create_file_if_not_exists "ai/prompts/meta/iterative_research_refinement.md" "# Iterative Research Refinement"
create_file_if_not_exists "ai/prompts/meta/modular_task_decomposition.md" "# Modular Task Decomposition"
create_file_if_not_exists "ai/prompts/meta/multi_perspective_approach.md" "# Multi Perspective Approach"
create_file_if_not_exists "ai/prompts/meta/primary_research.md" "# Primary Research"
create_file_if_not_exists "ai/prompts/meta/step_by_step_research.md" "# Step by Step Research"
create_file_if_not_exists "ai/prompts/meta/textgrad_iterative.md" "# Textgrad Iterative"
create_file_if_not_exists "ai/prompts/meta/universal_research.md" "# Universal Research"

# Create ai/scratchpads files
create_file_if_not_exists "ai/scratchpads/.gitkeep" ""

# Create ai/tests files
create_file_if_not_exists "ai/tests/ai-context-tests.yaml" ""
create_file_if_not_exists "ai/tests/dependency-validation-tests.yaml" ""
create_file_if_not_exists "ai/tests/document-structure-tests.yaml" ""