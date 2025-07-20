---
title: "API Documentation (OpenAPI)"
type: "api-documentation-openapi"
category: "technical"
tier: 1
ai_processing_value: 95
dependencies:
  - system-architecture
  - database-design-document
  - technical-specifications-document
outputs:
  - endpoint_definitions
  - request_schemas
  - response_schemas
  - authentication_methods
  - api_contracts
---

# API Documentation (OpenAPI)

## AI Agent Instructions

When creating API Documentation with OpenAPI specifications:

1. **Follow OpenAPI 3.0+ standards** - Use proper schema, components, and structure
2. **Include comprehensive examples** - Request/response examples for all endpoints
3. **Document authentication** - Security schemes and authorization methods
4. **Validate schema accuracy** - Ensure schemas match actual implementation
5. **Generate code-ready specs** - Structure for automatic client generation

## Document Structure

### API Overview
- **API Purpose** - Primary function and business value
- **Base URL** - API endpoint base address
- **Version** - API version and versioning strategy
- **Authentication** - Security and authorization overview

### OpenAPI Specification

```yaml
openapi: 3.0.3
info:
  title: [API Title]
  description: [API Description]
  version: [Version]
  contact:
    name: [Contact Name]
    email: [Contact Email]
servers:
  - url: [Base URL]
    description: [Environment Description]
```

### Authentication & Security

#### Security Schemes
- **API Key** - Header/query parameter authentication
- **Bearer Token** - JWT or OAuth token authentication
- **OAuth 2.0** - OAuth flows and scopes
- **Basic Auth** - Username/password authentication

```yaml
components:
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

### API Endpoints

#### Resource Endpoints
For each resource (e.g., users, orders, products):

##### GET /resource
- **Purpose** - Retrieve resource collection
- **Parameters** - Query parameters for filtering/pagination
- **Response** - Resource list with metadata
- **Examples** - Sample requests and responses

##### GET /resource/{id}
- **Purpose** - Retrieve specific resource
- **Parameters** - Path parameters and optional query params
- **Response** - Single resource object
- **Error Handling** - 404 Not Found scenarios

##### POST /resource
- **Purpose** - Create new resource
- **Request Body** - Resource creation schema
- **Response** - Created resource with ID
- **Validation** - Required fields and constraints

##### PUT /resource/{id}
- **Purpose** - Update existing resource
- **Request Body** - Complete resource update schema
- **Response** - Updated resource object
- **Idempotency** - Ensure idempotent operations

##### DELETE /resource/{id}
- **Purpose** - Remove resource
- **Response** - Confirmation or empty response
- **Cascading** - Related resource cleanup

### Data Models

#### Schema Definitions
```yaml
components:
  schemas:
    User:
      type: object
      required:
        - id
        - email
        - name
      properties:
        id:
          type: integer
          format: int64
          example: 1
        email:
          type: string
          format: email
          example: user@example.com
        name:
          type: string
          example: John Doe
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time
```

#### Validation Rules
- **Required Fields** - Mandatory data elements
- **Data Types** - String, integer, boolean, array, object
- **Format Constraints** - Email, date, UUID, etc.
- **Range Limits** - Min/max values and lengths
- **Pattern Matching** - Regular expressions for validation

### Error Handling

#### Standard Error Response
```yaml
ErrorResponse:
  type: object
  properties:
    error:
      type: string
      example: "Invalid input"
    message:
      type: string
      example: "The provided email address is invalid"
    code:
      type: integer
      example: 400
    details:
      type: object
```

#### HTTP Status Codes
- **200 OK** - Successful GET, PUT
- **201 Created** - Successful POST
- **204 No Content** - Successful DELETE
- **400 Bad Request** - Invalid request data
- **401 Unauthorized** - Missing/invalid authentication
- **403 Forbidden** - Insufficient permissions
- **404 Not Found** - Resource not found
- **409 Conflict** - Resource conflict
- **422 Unprocessable Entity** - Validation errors
- **500 Internal Server Error** - Server errors

### Rate Limiting

#### Rate Limit Headers
- **X-RateLimit-Limit** - Maximum requests per window
- **X-RateLimit-Remaining** - Remaining requests in window
- **X-RateLimit-Reset** - Time when window resets
- **Retry-After** - Seconds to wait when rate limited

### Pagination

#### Pagination Strategy
- **Offset-based** - Using offset and limit parameters
- **Cursor-based** - Using cursor tokens for large datasets
- **Page-based** - Using page and size parameters

```yaml
PaginatedResponse:
  type: object
  properties:
    data:
      type: array
      items:
        $ref: '#/components/schemas/Resource'
    meta:
      type: object
      properties:
        total:
          type: integer
        page:
          type: integer
        per_page:
          type: integer
        total_pages:
          type: integer
```

### Testing & Validation

#### API Testing
- **Unit Tests** - Individual endpoint testing
- **Integration Tests** - End-to-end API workflows
- **Contract Tests** - Schema validation tests
- **Load Tests** - Performance and capacity testing

#### Validation Tools
- **OpenAPI Validators** - Schema validation tools
- **Mock Servers** - API simulation for testing
- **Documentation Tools** - Auto-generated documentation
- **Code Generation** - Client SDK generation

## Dependencies

This document requires:
- **System Architecture** - Overall system design context
- **Database Design** - Data model and schema information
- **Technical Specifications** - Implementation requirements
- **Security Architecture** - Authentication and authorization design

## Outputs

This document produces:
- **Endpoint Definitions** - Complete API endpoint specifications
- **Request Schemas** - Input data validation schemas
- **Response Schemas** - Output data structure definitions
- **Authentication Methods** - Security implementation guides
- **API Contracts** - Client-server interaction agreements

## Cross-References

- Links to @ai/knowledge/technical/system-architecture.md
- References @ai/knowledge/technical/database-design-document.md
- Connects to @ai/knowledge/technical/security-architecture.md
- Supports @ai/knowledge/technical/integration-architecture.md
- Enables @ai/knowledge/quality/test-plans.md