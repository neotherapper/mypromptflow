---
document_type: data-models
feature_name: {FEATURE_NAME}
version: 1.0
created_date: {DATE}
dependencies:
  - ./api-contracts.md
  - @ai/knowledge/technical/database/schemas/
---

# Data Models: {FEATURE_NAME}

## Overview

Database schemas and data models for {FEATURE_NAME}.

## Entity: {EntityName}

### Table Definition

```sql
CREATE TABLE {table_name} (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

    -- Core fields
    name VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'active',

    -- Foreign keys
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,

    -- Constraints
    CONSTRAINT {table_name}_name_unique UNIQUE (name, user_id)
);

-- Indexes
CREATE INDEX idx_{table_name}_user_id ON {table_name}(user_id);
CREATE INDEX idx_{table_name}_status ON {table_name}(status);
CREATE INDEX idx_{table_name}_created_at ON {table_name}(created_at DESC);
```

### TypeScript Model

```typescript
interface {EntityName} {
  id: string;
  createdAt: Date;
  updatedAt: Date;

  // Core fields
  name: string;
  description?: string;
  status: 'active' | 'inactive' | 'deleted';

  // Relations
  userId: string;
  user?: User;
}

// Create DTO
interface Create{EntityName}DTO {
  name: string;
  description?: string;
}

// Update DTO
interface Update{EntityName}DTO {
  name?: string;
  description?: string;
  status?: 'active' | 'inactive';
}
```

### Relationships

Belongs to: User (many-to-one)
Has many: {RelatedEntity} (one-to-many)

### Business Rules

{Business rule description}
{Validation rule}
{Constraint description}

### Migration Strategy

```sql
-- Migration: create_{table_name}_table
-- Up
{CREATE TABLE statement}

-- Down
DROP TABLE IF EXISTS {table_name};
```

## AI Agent Instructions

When working with these models:

1. Always use UUIDs for primary keys
2. Include timestamps on all tables
3. Implement soft deletes where appropriate
4. Use TypeScript interfaces for type safety
