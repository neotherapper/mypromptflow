# Knowledge Vault Database - Central Hub

This directory contains the file-based implementation of the Knowledge Vault central hub database.

## Directory Structure

- `items/` - Individual knowledge vault items (YAML files)
- `relations/` - Cross-database relationship mappings
- `indexes/` - Performance indexes for efficient querying
- `views/` - Predefined views and filter configurations
- `metadata/` - Database metadata and usage statistics

## File Naming Conventions

- **Items**: `knowledge_vault_{uuid}.yaml`
- **Relations**: `kv_to_{target_db}_{relation_type}.yaml`
- **Indexes**: `kv_{index_type}_index.yaml`
- **Views**: `kv_{view_name}_view.yaml`
- **Metadata**: `kv_metadata_{timestamp}.yaml`

## Schema Reference

Schema definition: `../../schemas/knowledge-vault-schema.yaml`

## Hub Role

As the central hub, this database:
- Coordinates relationships with all spoke databases
- Maintains global priority and tagging systems
- Provides unified search and discovery
- Tracks system-wide dependencies and connections