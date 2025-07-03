---
template_type: api-documentation
tier: 1
ai_value: 95
---

# API Documentation Template

## Document Structure:

````markdown
---
document_type: api-documentation
version: 1.0
created_date: { date }
dependencies:
  - system-architecture
  - database-schemas
status: draft
ai_context:
  primary_purpose: Enable automated API client generation
  key_insights:
    - Complete endpoint coverage
    - TypeScript type definitions
    - Authentication patterns
---

# {Service Name} API Documentation

## Overview

{Brief description of API purpose and capabilities}

## Authentication

{Authentication method details}

## Base URL

{environment}: {base_url}

## Endpoints

### {Resource} Endpoints

#### GET /{resource}

{Description}

**Request:**

```typescript
interface Get{Resource}Request {
  // Query parameters
}
```

**Response:**

```typescript
interface Get{Resource}Response {
  data: {Resource}[];
  pagination: PaginationMeta;
}
```

**Example:**

```bash
curl -X GET "{base_url}/{resource}" \
  -H "Authorization: Bearer {token}"
```

**Error Handling:**

{Common error codes and handling}

**Rate Limiting:**

{Rate limit details}

**AI Agent Instructions:**

When implementing API clients:

1. Use provided TypeScript interfaces
2. Implement proper error handling
3. Include retry logic for rate limits
4. Generate comprehensive tests
````
