---
template_type: product-requirements-document
tier: 2
ai_value: 85
---

# PRD Template

## Document Structure:

```markdown
---
document_type: prd
version: 1.0
created_date: { date }
dependencies:
  - statement-of-purpose
  - market-analysis
  - user-research
status: draft
ai_context:
  primary_purpose: Guide feature development and prioritization
  key_insights:
    - Core functionality requirements
    - Success metrics
    - User value propositions
---

# Product Requirements Document

## Executive Summary

{High-level product vision and goals}

## Problem Statement

{What problem does this solve?}

## Target Users

{Primary and secondary user segments}

## Functional Requirements

### Core Features

1. **{Feature Name}**
   - Description: {description}
   - User Story: As a {user}, I want {goal} so that {benefit}
   - Priority: P0/P1/P2
   - Acceptance Criteria:
     - [ ] {criterion}

### User Flows

{Key user journeys through the product}

## Non-Functional Requirements

### Performance

- {Requirement}: {Target metric}

### Security

- {Security requirement}

### Scalability

- {Scalability requirement}

## Success Metrics

- {Metric}: {Target} by {Timeline}

## MVP Scope

{What's included in the first release}

## Future Considerations

{Features for future releases}

## AI Agent Instructions

When implementing features from this PRD:

1. Start with P0 features
2. Reference user stories for context
3. Validate against acceptance criteria
4. Track success metrics in implementation
```
