# Change Events Database

## Overview
Technology change detection and classification

## Directory Structure
- `items/` - Individual database items (YAML files)
- `relations/` - Relationship mappings between items
- `metadata/` - Database metadata and configuration
- `indexes/` - Index files for performance optimization
- `views/` - Predefined views and queries

## Schema
Schema definition: `../../schemas/change-event-schema.yaml`

## Integration
This database is part of the AI Knowledge Lifecycle Orchestrator integration.
- Notion integration: Disabled
- Local operations: Enabled
- Orchestrator integration: Enabled

## Operations
Use the Knowledge Vault operations scripts to interact with this database:
- `../scripts/mcp_operations_enhanced.py`
- `../scripts/knowledge-vault-operations-update.py`

Created: 2025-07-25 00:34:04
