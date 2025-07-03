---
document_type: test-strategy
feature_name: {FEATURE_NAME}
version: 1.0
created_date: {DATE}
dependencies:
  - ../requirements/acceptance-criteria.md
  - @ai/knowledge/quality-assurance/qa-plan.md
---

# Test Strategy: {FEATURE_NAME}

## Overview

Comprehensive testing approach for {FEATURE_NAME}.

## Test Levels

### Unit Tests

**Coverage Goal**: > 90%

**Key Areas**:

- Business logic functions
- Data validation
- Utility functions
- Component rendering

**Example**:

```typescript
describe("{FunctionName}", () => {
  it("should {expected behavior}", () => {
    const result = functionName(input);
    expect(result).toBe(expectedOutput);
  });

  it("should handle edge case", () => {
    expect(() => functionName(invalidInput)).toThrow();
  });
});
```

### Integration Tests

Coverage Goal: > 80%
Key Areas:

API endpoint integration
Database operations
External service calls
Authentication flows

### E2E Tests

Coverage Goal: Critical user paths
Test Scenarios:

{Primary user flow}
{Secondary user flow}
{Error handling flow}

### Test Data Strategy

Use factories for consistent test data
Separate test database/environment
Seed data for E2E tests
Mock external services

### Performance Testing

Load testing: {concurrent users}
Response time: < {time}ms
Throughput: > {requests}/second

### Security Testing

Authentication bypass attempts
Authorization checks
Input validation
SQL injection prevention
XSS prevention

### Accessibility Testing

Keyboard navigation
Screen reader compatibility
Color contrast ratios
ARIA labels

## AI Agent Instructions

When implementing tests:

1. Write tests before implementation (TDD)
2. Use descriptive test names
3. Test both happy and error paths
4. Mock external dependencies
5. Keep tests isolated and fast
