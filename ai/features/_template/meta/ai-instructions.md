---
document_type: ai-instructions
feature_name: { FEATURE_NAME }
version: 1.0
created_date: { DATE }
---

# AI Implementation Instructions: {FEATURE_NAME}

## Quick Start

To implement this feature, start with:

1. Read feature-spec.md for context
2. Review user-stories.md for requirements
3. Check api-contracts.md for endpoints
4. Reference data-models.md for database schema

## Implementation Order

1. **Backend API**

   - Create data models
   - Implement service layer
   - Add API endpoints
   - Write unit tests

2. **Frontend Components**

   - Create UI components
   - Connect to API
   - Implement state management
   - Add component tests

3. **Integration**
   - Wire up full flow
   - Add E2E tests
   - Performance optimization
   - Security review

## Code Structure

### Backend Structure

src/
features/
{feature-name}/
controllers/
{feature}.controller.ts
services/
{feature}.service.ts
models/
{feature}.model.ts
dto/
create-{feature}.dto.ts
update-{feature}.dto.ts
tests/
{feature}.controller.spec.ts
{feature}.service.spec.ts

### Frontend Structure

src/
features/
{feature-name}/
components/
{Feature}List.tsx
{Feature}Detail.tsx
{Feature}Form.tsx
hooks/
use{Feature}.ts
services/
{feature}.service.ts
types/
{feature}.types.ts
tests/
{Feature}.test.tsx

## Key Patterns to Follow

### API Pattern

```typescript
// Controller
@Controller('{feature}')
export class {Feature}Controller {
  constructor(private readonly {feature}Service: {Feature}Service) {}

  @Post()
  create(@Body() dto: Create{Feature}DTO) {
    return this.{feature}Service.create(dto);
  }
}

// Service
@Injectable()
export class {Feature}Service {
  async create(dto: Create{Feature}DTO): Promise<{Feature}> {
    // Business logic here
  }
}
```

### React Component Pattern

```typescript
export const {Feature}List: React.FC = () => {
  const { data, loading, error } = use{Feature}();

  if (loading) return <Loading />;
  if (error) return <Error error={error} />;

  return (
    <div>
      {data.map(item => (
        <{Feature}Item key={item.id} item={item} />
      ))}
    </div>
  );
};
```

### Testing Pattern

```typescript
describe("{Feature}", () => {
  beforeEach(() => {
    // Setup
  });

  it("should create a new {feature}", async () => {
    // Test implementation
  });
});
```

### Common Pitfalls to Avoid

1. Don't skip input validation
2. Always handle error cases
3. Don't hardcode values
4. Remember to update documentation
5. Don't forget accessibility

### Integration Points

- Authentication: Use existing auth middleware
- Logging: Use application logger
- Error handling: Use global error handler
- Database: Use existing connection pool

### Performance Considerations

- Implement pagination for lists
- Use database indexes effectively
- Cache frequently accessed data
- Optimize bundle size

### Security Checklist

- [ ] Input validation implemented
- [ ] Authentication required
- [ ] Authorization checks in place
- [ ] SQL injection prevented
- [ ] XSS prevention implemented
- [ ] CSRF protection enabled

### Questions for Clarification

If you need clarification:

1. Check existing similar features
2. Review architecture decisions
3. Ask about business rules
4. Confirm with test scenarios

## 8. Example Documents

### `ai/knowledge/strategic/statement-of-purpose.md`

```markdown
---
document_type: statement-of-purpose
version: 1.0
created_date: 2024-01-15
dependencies: []
status: approved
ai_context:
  primary_purpose: Define business vision and core values
  key_insights:
    - Target audience definition
    - Core value propositions
    - Business objectives
---

# Statement of Purpose

## Vision

To create a platform that revolutionizes how small businesses manage their operations through intelligent automation and intuitive design.

## Mission

We empower small business owners by providing an all-in-one solution that simplifies complex business processes, enabling them to focus on growth rather than administration.

## Core Values

1. **Simplicity**: Complex problems, simple solutions
2. **Reliability**: Trust through consistent performance
3. **Innovation**: Continuous improvement and adaptation
4. **Accessibility**: Available to businesses of all sizes

## Target Audience

### Primary Users

- Small business owners (1-50 employees)
- Startups and entrepreneurs
- Freelancers and consultants

### User Characteristics

- Time-constrained
- Not necessarily tech-savvy
- Need integrated solutions
- Value efficiency and cost-effectiveness

## Business Objectives

1. Reduce operational overhead by 40%
2. Increase user productivity by 60%
3. Achieve 95% user satisfaction rating
4. Reach 10,000 active users in year one

## Success Metrics

- User activation rate > 80%
- Monthly active users growth > 20%
- Churn rate < 5%
- NPS score > 50

## AI Agent Instructions

When using this document:

1. Reference target audience for all feature decisions
2. Ensure solutions align with core values
3. Validate features against business objectives
4. Use success metrics for prioritization
```
