---
template_type: epic-documentation
tier: 3
ai_value: 77
---

# Epic Documentation Template

## Document Structure:

```markdown
---
document_type: epic-documentation
version: 1.0
created_date: { date }
dependencies:
  - product-requirements-document
  - strategic-roadmap
  - user-stories
status: draft
ai_context:
  primary_purpose: Define large work bodies spanning multiple sprints
  key_insights:
    - High-level feature grouping
    - Cross-team coordination
    - Value delivery tracking
---

# Epic: {Epic Name}

## Epic Overview

### Epic Statement
**As a** {user type}, **I want** {high-level goal} **so that** {business value}.

### Epic Description
{Detailed description of what this epic encompasses}

### Business Value
- **Primary Value**: {Main business benefit}
- **Secondary Values**: {Additional benefits}
- **Success Metrics**: {How we'll measure success}

### Strategic Alignment
- **Company Objective**: {Which company goal this supports}
- **Product Strategy**: {How this fits product strategy}
- **User Need**: {Which user need this addresses}

## Epic Details

### Scope and Boundaries
**In Scope**:
- {Feature/functionality included}
- {Feature/functionality included}
- {Feature/functionality included}

**Out of Scope**:
- {Feature/functionality excluded}
- {Feature/functionality excluded}
- {Feature/functionality excluded}

### User Impact
- **Primary Users**: {Who will use this}
- **Secondary Users**: {Who else might be affected}
- **Use Cases**: {Main scenarios of use}
- **User Benefits**: {What users gain}

### Business Impact
- **Revenue Impact**: {Expected revenue effect}
- **Cost Impact**: {Expected cost effect}
- **Operational Impact**: {Effect on operations}
- **Risk Mitigation**: {Risks this addresses}

## User Stories

### Story Hierarchy
```
Epic: {Epic Name}
├── Story 1: {Story Title}
│   ├── Task 1.1: {Task description}
│   ├── Task 1.2: {Task description}
│   └── Task 1.3: {Task description}
├── Story 2: {Story Title}
│   ├── Task 2.1: {Task description}
│   └── Task 2.2: {Task description}
└── Story 3: {Story Title}
    ├── Task 3.1: {Task description}
    ├── Task 3.2: {Task description}
    └── Task 3.3: {Task description}
```

### High-Priority Stories
1. **{Story Title}**
   - Priority: P0/P1/P2
   - Story Points: {Estimate}
   - Sprint: {Target sprint}
   - Dependencies: {Other stories this depends on}

2. **{Story Title}**
   - Priority: P0/P1/P2
   - Story Points: {Estimate}
   - Sprint: {Target sprint}
   - Dependencies: {Other stories this depends on}

3. **{Story Title}**
   - Priority: P0/P1/P2
   - Story Points: {Estimate}
   - Sprint: {Target sprint}
   - Dependencies: {Other stories this depends on}

### Story Dependencies
- **{Story A}** → **{Story B}**: {Dependency description}
- **{Story C}** → **{Story D}**: {Dependency description}

## Acceptance Criteria

### Epic-Level Acceptance Criteria
- [ ] {High-level criterion}
- [ ] {High-level criterion}
- [ ] {High-level criterion}
- [ ] {High-level criterion}

### Definition of Done
- [ ] All user stories completed
- [ ] All acceptance criteria met
- [ ] Code review completed
- [ ] Testing completed (unit, integration, UAT)
- [ ] Documentation updated
- [ ] Performance requirements met
- [ ] Security requirements met
- [ ] Accessibility requirements met
- [ ] Deployed to production
- [ ] Success metrics baseline established

## Technical Considerations

### Technical Requirements
- **Performance**: {Performance requirements}
- **Scalability**: {Scalability requirements}
- **Security**: {Security requirements}
- **Accessibility**: {Accessibility requirements}

### Technical Dependencies
- **Systems**: {External systems required}
- **APIs**: {API dependencies}
- **Data**: {Data requirements}
- **Infrastructure**: {Infrastructure needs}

### Technical Risks
1. **{Risk}**
   - Impact: {High/Medium/Low}
   - Probability: {High/Medium/Low}
   - Mitigation: {How to address}

2. **{Risk}**
   - Impact: {High/Medium/Low}
   - Probability: {High/Medium/Low}
   - Mitigation: {How to address}

## Design Considerations

### User Experience Requirements
- **Usability**: {Usability requirements}
- **Accessibility**: {Accessibility requirements}
- **Performance**: {UX performance requirements}
- **Mobile**: {Mobile experience requirements}

### Design Dependencies
- **Design System**: {Design system components needed}
- **UI Components**: {New components required}
- **Patterns**: {Design patterns to follow}

### Design Deliverables
- [ ] User flow diagrams
- [ ] Wireframes
- [ ] High-fidelity designs
- [ ] Prototypes
- [ ] Design specifications
- [ ] Design system updates

## Success Metrics

### Key Performance Indicators
- **{KPI}**: {Current baseline} → {Target}
- **{KPI}**: {Current baseline} → {Target}
- **{KPI}**: {Current baseline} → {Target}

### User Metrics
- **Adoption Rate**: {Target percentage}
- **Engagement**: {Target metrics}
- **Satisfaction**: {Target satisfaction score}
- **Task Completion**: {Target completion rate}

### Business Metrics
- **Revenue**: {Expected impact}
- **Cost**: {Expected savings}
- **Efficiency**: {Expected improvement}
- **Risk Reduction**: {Expected risk mitigation}

## Timeline and Milestones

### Epic Timeline
- **Start Date**: {Epic start date}
- **End Date**: {Epic end date}
- **Duration**: {Number of sprints}

### Key Milestones
1. **{Milestone}**
   - Date: {Target date}
   - Deliverables: {What's delivered}
   - Success Criteria: {How we measure success}

2. **{Milestone}**
   - Date: {Target date}
   - Deliverables: {What's delivered}
   - Success Criteria: {How we measure success}

3. **{Milestone}**
   - Date: {Target date}
   - Deliverables: {What's delivered}
   - Success Criteria: {How we measure success}

### Sprint Breakdown
- **Sprint 1**: {Stories and goals}
- **Sprint 2**: {Stories and goals}
- **Sprint 3**: {Stories and goals}
- **Sprint 4**: {Stories and goals}

## Resource Requirements

### Team Requirements
- **Product Manager**: {Time commitment}
- **Engineering**: {Team size and skills}
- **Design**: {Design resources needed}
- **QA**: {Testing resources needed}
- **Other**: {Additional resources}

### Budget Requirements
- **Development**: {Cost estimate}
- **Design**: {Cost estimate}
- **Testing**: {Cost estimate}
- **Infrastructure**: {Cost estimate}
- **Total**: {Total cost estimate}

## Risk Management

### High-Risk Areas
1. **{Risk Category}**
   - Risk: {Specific risk}
   - Impact: {High/Medium/Low}
   - Probability: {High/Medium/Low}
   - Mitigation: {How to address}
   - Owner: {Who's responsible}

2. **{Risk Category}**
   - Risk: {Specific risk}
   - Impact: {High/Medium/Low}
   - Probability: {High/Medium/Low}
   - Mitigation: {How to address}
   - Owner: {Who's responsible}

### Contingency Plans
- **Scenario**: {If this happens}
  - Response: {What we'll do}
  - Timeline: {How quickly we'll respond}
  - Impact: {Effect on epic}

## Stakeholder Communication

### Key Stakeholders
- **Primary**: {Who needs regular updates}
- **Secondary**: {Who needs occasional updates}
- **Approval**: {Who needs to approve deliverables}

### Communication Plan
- **Weekly Updates**: {Format and recipients}
- **Sprint Reviews**: {Who attends}
- **Milestone Reviews**: {Format and participants}
- **Go-Live Communication**: {Launch communication plan}

## Quality Assurance

### Testing Strategy
- **Unit Testing**: {Coverage requirements}
- **Integration Testing**: {Test scenarios}
- **User Acceptance Testing**: {UAT plan}
- **Performance Testing**: {Performance tests}
- **Security Testing**: {Security test plan}

### Quality Gates
- [ ] Code review completed
- [ ] Unit tests passing
- [ ] Integration tests passing
- [ ] Performance tests passing
- [ ] Security scan completed
- [ ] Accessibility audit completed
- [ ] UAT completed

## Launch and Rollout

### Launch Strategy
- **Rollout Type**: {Phased/Full/Feature Flag}
- **Target Audience**: {Who gets it first}
- **Timeline**: {Launch schedule}
- **Rollback Plan**: {How to rollback if needed}

### Post-Launch
- **Monitoring**: {What we'll monitor}
- **Success Criteria**: {How we'll measure success}
- **Iteration Plan**: {How we'll iterate based on feedback}

## AI Agent Instructions

When working with epic documentation:

1. Break down large epics into appropriately sized user stories
2. Identify technical dependencies and integration points
3. Generate acceptance criteria based on user needs
4. Create timeline estimates based on story complexity
5. Suggest risk mitigation strategies
6. Generate testing scenarios and quality gates
7. Create stakeholder communication templates
8. Recommend success metrics and KPIs
9. Generate resource allocation recommendations
10. Create launch and rollout strategies
```