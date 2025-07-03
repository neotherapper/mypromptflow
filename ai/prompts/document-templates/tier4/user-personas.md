---
template_type: user-personas
tier: 4
ai_value: 65
---

# User Personas Template

## Document Structure:

```markdown
---
document_type: user-personas
version: 1.0
created_date: { date }
dependencies:
  - user-research
  - market-analysis
status: draft
ai_context:
  primary_purpose: Provide user context for feature decisions
  key_insights:
    - User motivations and goals
    - Pain points and frustrations
    - Behavioral patterns
---

# User Personas

## Persona: {Persona Name}

### Demographics

- Age: {range}
- Role: {job title/role}
- Location: {geographic info}
- Tech Savviness: {level}

### Goals & Motivations

- Primary Goal: {main objective}
- Secondary Goals:
  - {goal}
  - {goal}

### Pain Points

- {Current frustration}
- {Workflow inefficiency}
- {Unmet need}

### Behavioral Patterns

- {How they currently solve problems}
- {Tools they use}
- {Frequency of use}

### Quote

> "{Representative quote that captures their perspective}"

### User Journey

{Key touchpoints and interactions with product}

### Design Implications

- {How this persona influences design decisions}
- {Features that would appeal to them}
- {Potential barriers to adoption}

## AI Agent Instructions

When designing for this persona:

1. Prioritize their primary goals
2. Address main pain points
3. Use appropriate language/terminology
4. Consider their tech comfort level
```
