---
template_type: user-stories
tier: 3
ai_value: 75
---

# User Stories Template

## Document Structure:

```markdown
---
document_type: user-stories
version: 1.0
created_date: { date }
dependencies:
  - user-personas
  - prd
status: draft
ai_context:
  primary_purpose: Break down features into implementable units
  key_insights:
    - User-centric requirements
    - Clear acceptance criteria
    - Testable outcomes
---

# User Stories for {Feature/Epic}

## Epic: {Epic Name}

{Epic description}

### Story {ID}: {Story Title}

**As a** {user type}
**I want** {goal/desire}
**So that** {benefit/value}

**Acceptance Criteria:**

- [ ] Given {context}, when {action}, then {outcome}
- [ ] Given {context}, when {action}, then {outcome}

**Technical Notes:**

- {Implementation consideration}
- {API endpoint needed}

**Story Points:** {1|2|3|5|8|13}

**Dependencies:**

- {Other story IDs}
- {External dependencies}

## Story Mapping

{Visual or structured representation of story relationships}

## AI Agent Instructions

When implementing user stories:

1. Complete all acceptance criteria
2. Write tests for each criterion
3. Consider edge cases not explicitly stated
4. Update story status after implementation
```
