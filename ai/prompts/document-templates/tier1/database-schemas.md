---
template_type: database-schema
tier: 1
ai_value: 92
---

# Database Schema Template

## Document Structure:

````markdown
---
document_type: database-schema
version: 1.0
created_date: { date }
dependencies:
  - data-requirements
  - domain-models
status: draft
ai_context:
  primary_purpose: Enable automated ORM generation and query building
  key_insights:
    - Complete table definitions
    - Relationship mappings
    - Index strategies
---

# Database Schema Documentation

## Overview

{Database design philosophy and approach}

## Schema Definition

### Table: {table_name}

{Table description}

```sql
CREATE TABLE {table_name} (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    -- fields
);
```

### TypeScript Interface:

```typescript
interface {TableName} {
  id: string;
  createdAt: Date;
  updatedAt: Date;
  // fields
}
```

### Relationships:

Has many: {related_table}
Belongs to: {parent_table}

### Indexes:

```sql
CREATE INDEX idx*{table_name}*{field} ON {table_name}({field});
```

### Migrations

{Migration strategy and versioning}

## AI Agent Instructions

When working with this schema:

1. Use TypeScript interfaces for type safety
2. Include proper foreign key constraints
3. Implement soft deletes where appropriate
4. Generate migration files for changes
````
