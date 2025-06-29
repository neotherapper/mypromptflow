#!/bin/bash

# Create ai/context files
touch ai/context/{dependencies.yaml,document-registry.yaml,feature-registry.yaml,tier-configuration.yaml}

# Create ai/features/_template files
echo "# Feature Spec" > ai/features/_template/feature-spec.md
echo "# README" > ai/features/_template/README.md
echo "# UI Mockups" > ai/features/_template/design/ui-mockups.md
echo "# AI Instructions" > ai/features/_template/meta/ai-instructions.md
echo "# Acceptance Criteria" > ai/features/_template/requirements/acceptance-criteria.md
echo "# User Stories" > ai/features/_template/requirements/user-stories.md
echo "# API Contracts" > ai/features/_template/technical/api-contracts.md
echo "# Data Models" > ai/features/_template/technical/data-models.md
echo "# Test Strategy" > ai/features/_template/tests/test-strategy.md

# Create ai/features/user-authentication files
echo "# Feature Spec" > ai/features/user-authentication/feature-spec.md

# Create ai/prompts files
echo "# Discover Tools" > ai/prompts/1_discover_tools.md
echo "# Extract Features" > ai/prompts/2_extract_features.md
echo "# Map Features to Framework" > ai/prompts/3_map_features_to_framework.md

# Create ai/prompts/document-templates files
echo "# API Documentation" > ai/prompts/document-templates/tier1/api-documentation.md
echo "# Database Schemas" > ai/prompts/document-templates/tier1/database-schemas.md
echo "# PRD" > ai/prompts/document-templates/tier2/prd.md
echo "# User Stories" > ai/prompts/document-templates/tier3/user-stories.md
echo "# User Personas" > ai/prompts/document-templates/tier4/user-personas.md

# Create ai/prompts/meta-prompts files
echo "# Dependency Analyzer" > ai/prompts/meta-prompts/dependency-analyzer.md
echo "# Document Generator" > ai/prompts/meta-prompts/document-generator.md
echo "# Feature Orchestrator" > ai/prompts/meta-prompts/feature-orchestrator.md
echo "# Quality Validator" > ai/prompts/meta-prompts/quality-validator.md
echo "# Tier Orchestrator" > ai/prompts/meta-prompts/tier-orchestrator.md

# Create ai/prompts/meta files
echo "# Adaptive Chain of Thought" > ai/prompts/meta/adaptive_chain_of_thought.md
echo "# Complex Research" > ai/prompts/meta/complex_research.md
echo "# Domain Adaptive" > ai/prompts/meta/domain_adaptive.md
echo "# Domain Specific Research" > ai/prompts/meta/domain_specific_research.md
echo "# Iterative Research Refinement" > ai/prompts/meta/iterative_research_refinement.md
echo "# Modular Task Decomposition" > ai/prompts/meta/modular_task_decomposition.md
echo "# Multi Perspective Approach" > ai/prompts/meta/multi_perspective_approach.md
echo "# Primary Research" > ai/prompts/meta/primary_research.md
echo "# Step by Step Research" > ai/prompts/meta/step_by_step_research.md
echo "# Textgrad Iterative" > ai/prompts/meta/textgrad_iterative.md
echo "# Universal Research" > ai/prompts/meta/universal_research.md

# Create ai/scratchpads files
touch ai/scratchpads/.gitkeep

# Create ai/tests files
touch ai/tests/{ai-context-tests.yaml,dependency-validation-tests.yaml,document-structure-tests.yaml}
