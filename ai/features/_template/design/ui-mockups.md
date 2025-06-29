---
document_type: ui-mockups
feature_name: {FEATURE_NAME}
version: 1.0
created_date: {DATE}
dependencies:
  - ../requirements/user-stories.md
  - @ai/knowledge/user-experience/design/design-system.md
---

# UI Mockups: {FEATURE_NAME}

## Overview

Visual designs and wireframes for {FEATURE_NAME}.

## Design Principles

- {Key design principle}
- {Accessibility consideration}
- {Mobile-first approach}

## Screen: {SCREEN_NAME}

### Desktop View

┌─────────────────────────────────┐
│ Header │
├─────────────────────────────────┤
│ │
│ Main Content Area │
│ │
│ [Component Description] │
│ │
└─────────────────────────────────┘

### Mobile View

┌─────────────┐
│ Header │
├─────────────┤
│ │
│ Content │
│ │
└─────────────┘

### Component Specifications

- **{Component Name}**
  - Type: {button|input|card|etc}
  - Design System Ref: `{ComponentName}`
  - Props: `{prop1}, {prop2}`
  - States: default, hover, active, disabled

### Interaction Notes

1. On click of {element}: {behavior}
2. On hover: {visual feedback}
3. Loading state: {description}

## Accessibility

- WCAG Level: AA
- Keyboard navigation: {description}
- Screen reader: {considerations}

## AI Agent Instructions

When implementing these designs:

1. Use components from @ai/knowledge/user-experience/design/design-system.md
2. Maintain responsive breakpoints
3. Implement all interaction states
4. Follow accessibility guidelines
