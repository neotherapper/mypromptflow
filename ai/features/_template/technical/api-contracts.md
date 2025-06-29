---
document_type: api-contracts
feature_name: {FEATURE_NAME}
version: 1.0
created_date: {DATE}
dependencies:
  - ../requirements/user-stories.md
  - @ai/knowledge/technical/api/api-documentation.md
---

# API Contracts: {FEATURE_NAME}

## Overview

API specifications for {FEATURE_NAME} endpoints.

## Base Configuration

- Base URL: `/api/v1/{feature}`
- Authentication: Bearer token required
- Content-Type: application/json

## Endpoints

### POST /api/v1/{feature}

Create a new {resource}.

**Request:**

```typescript
interface Create{Resource}Request {
  name: string;
  description?: string;
  // Additional fields
}
```

**Response:**

```typescript
interface Create{Resource}Response {
  id: string;
  name: string;
  description?: string;
  createdAt: string;
  updatedAt: string;
}
```

## Errors:

400 Bad Request - Invalid input
401 Unauthorized - Missing/invalid token
409 Conflict - Resource already exists

## Example:

```bash
curl -X POST https://api.example.com/api/v1/{feature} \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Example",
    "description": "Example description"
  }'
```

### GET /api/v1/{feature}/{id}

Retrieve a specific {resource}.
{Continue pattern for all endpoints}

### Error Responses

```typescript
typescriptinterface ErrorResponse {
  error: {
    code: string;
    message: string;
    details?: Record<string, any>;
  };
  timestamp: string;
  path: string;
}
```

## Rate Limiting

Rate limit: 100 requests per minute
Headers: X-RateLimit-Limit, X-RateLimit-Remaining

## AI Agent Instructions

When implementing these endpoints:

1. Use TypeScript interfaces exactly as defined
2. Implement proper error handling
3. Add request validation
4. Include comprehensive tests
