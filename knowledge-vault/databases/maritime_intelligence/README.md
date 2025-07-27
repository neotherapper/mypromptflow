# Maritime Intelligence Database

## Purpose

This specialized database contains maritime industry-specific intelligence and applications for MCP servers and other tools. It maintains cross-references to the generic profiles in the tools_services database while providing industry-specific context and use cases.

## Architecture

The maritime intelligence system uses a separation approach:
- **Generic Profiles**: Located in `tools_services` database with industry-neutral language
- **Maritime Intelligence**: Located in this database with maritime-specific applications and examples
- **Cross-References**: Bidirectional relationships using `@maritime_intelligence/{uuid}` format

## Database Structure

```
maritime_intelligence/
├── README.md                    # This file
├── indexes/                     # Search and filtering indexes
├── items/                       # Individual maritime intelligence records
├── metadata/                    # Database metadata and configuration
├── relations/                   # Cross-database relationship mappings
├── views/                       # Predefined view configurations
└── schemas/                     # Database schema definitions
```

## Integration Points

- **Tools & Services Database**: Cross-references to generic MCP server profiles
- **Knowledge Vault Hub**: Connected through the central hub architecture
- **Notion Synchronization**: Maintains sync with corresponding Notion database
- **MCP Registry**: Provides maritime-specific context for MCP server selection

## Usage Guidelines

1. **Adding Maritime Intelligence**: Create new records that reference generic tools/services
2. **Cross-Referencing**: Use `@tools_services/{uuid}` to link to generic profiles
3. **Industry Context**: Focus on maritime insurance, claims processing, vessel tracking, regulatory compliance
4. **Relationship Maintenance**: Ensure bidirectional relationships are maintained

## Schema Version

Current schema version: 1.0.0
Last updated: 2025-01-24