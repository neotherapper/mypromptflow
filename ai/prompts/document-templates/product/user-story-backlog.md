---
template_type: user-story-backlog
tier: 3
ai_value: 75
---

# User Story Backlog Template

## Document Structure:

```markdown
---
document_type: user-story-backlog
version: 1.0
created_date: { date }
dependencies:
  - product-requirements-document
  - epic-documentation
  - user-personas
status: draft
ai_context:
  primary_purpose: Manage and prioritize development work items
  key_insights:
    - Story prioritization framework
    - Sprint planning support
    - Progress tracking
---

# {Product Name} User Story Backlog

## Backlog Overview

### Backlog Health Metrics
- **Total Stories**: {Number}
- **Ready for Development**: {Number}
- **In Progress**: {Number}
- **Completed**: {Number}
- **Backlog Coverage**: {Sprints worth of work}

### Story Distribution
- **P0 (Critical)**: {Number} stories
- **P1 (High)**: {Number} stories
- **P2 (Medium)**: {Number} stories
- **P3 (Low)**: {Number} stories

## Prioritization Framework

### Prioritization Criteria
1. **Business Value** (40%)
   - Revenue impact
   - Cost savings
   - Strategic alignment
   - Customer satisfaction

2. **User Impact** (30%)
   - Number of users affected
   - Frequency of use
   - Pain level addressed
   - User satisfaction improvement

3. **Technical Effort** (20%)
   - Development complexity
   - Testing requirements
   - Integration complexity
   - Technical debt impact

4. **Risk** (10%)
   - Technical risk
   - Business risk
   - Timeline risk
   - Dependencies

### Scoring Method
- **Score Range**: 1-10 for each criterion
- **Weighted Score**: (Business Value × 0.4) + (User Impact × 0.3) + (Effort × 0.2) + (Risk × 0.1)
- **Priority Assignment**: 
  - P0: Score 8.5-10
  - P1: Score 7.0-8.4
  - P2: Score 5.5-6.9
  - P3: Score 1.0-5.4

## Current Sprint Backlog

### Sprint {Number} - {Sprint Name}
**Sprint Goal**: {What we want to achieve this sprint}
**Sprint Dates**: {Start Date} - {End Date}
**Team Capacity**: {Story points available}

#### Committed Stories
1. **{Story ID}**: {Story Title}
   - Priority: P0/P1/P2/P3
   - Story Points: {Estimate}
   - Assignee: {Developer}
   - Status: {Todo/In Progress/Done}
   - Dependencies: {Other stories}

2. **{Story ID}**: {Story Title}
   - Priority: P0/P1/P2/P3
   - Story Points: {Estimate}
   - Assignee: {Developer}
   - Status: {Todo/In Progress/Done}
   - Dependencies: {Other stories}

#### Sprint Risks
- **{Risk}**: {Mitigation plan}
- **{Risk}**: {Mitigation plan}

## Next Sprint Candidates

### Sprint {Number + 1} - Candidate Stories
**Estimated Sprint Goal**: {Potential focus area}

#### High-Priority Candidates
1. **{Story ID}**: {Story Title}
   - Priority Score: {Score}
   - Story Points: {Estimate}
   - Readiness: {Ready/Needs refinement}
   - Blocker: {If any}

2. **{Story ID}**: {Story Title}
   - Priority Score: {Score}
   - Story Points: {Estimate}
   - Readiness: {Ready/Needs refinement}
   - Blocker: {If any}

## Product Backlog

### Epic 1: {Epic Name}
**Epic Priority**: {Priority}
**Epic Status**: {Status}
**Target Timeline**: {Timeline}

#### Stories
1. **{Story ID}**: {Story Title}
   - **User Story**: As a {user type}, I want {functionality} so that {benefit}
   - **Priority**: P0/P1/P2/P3
   - **Story Points**: {Estimate}
   - **Status**: {Backlog/Ready/In Progress/Done}
   - **Acceptance Criteria**:
     - [ ] {Criterion 1}
     - [ ] {Criterion 2}
     - [ ] {Criterion 3}
   - **Dependencies**: {Other stories or external dependencies}
   - **Notes**: {Additional context or considerations}

2. **{Story ID}**: {Story Title}
   - **User Story**: As a {user type}, I want {functionality} so that {benefit}
   - **Priority**: P0/P1/P2/P3
   - **Story Points**: {Estimate}
   - **Status**: {Backlog/Ready/In Progress/Done}
   - **Acceptance Criteria**:
     - [ ] {Criterion 1}
     - [ ] {Criterion 2}
     - [ ] {Criterion 3}
   - **Dependencies**: {Other stories or external dependencies}
   - **Notes**: {Additional context or considerations}

### Epic 2: {Epic Name}
**Epic Priority**: {Priority}
**Epic Status**: {Status}
**Target Timeline**: {Timeline}

#### Stories
1. **{Story ID}**: {Story Title}
   - **User Story**: As a {user type}, I want {functionality} so that {benefit}
   - **Priority**: P0/P1/P2/P3
   - **Story Points**: {Estimate}
   - **Status**: {Backlog/Ready/In Progress/Done}
   - **Acceptance Criteria**:
     - [ ] {Criterion 1}
     - [ ] {Criterion 2}
   - **Dependencies**: {Other stories or external dependencies}
   - **Notes**: {Additional context or considerations}

## Backlog Refinement

### Refinement Schedule
- **Weekly Refinement**: {Day and time}
- **Participants**: {Team members}
- **Duration**: {Time allocation}
- **Agenda**: {Standard agenda items}

### Refinement Criteria
**Story is Ready When**:
- [ ] User story is well-defined
- [ ] Acceptance criteria are clear
- [ ] Story is sized/estimated
- [ ] Dependencies are identified
- [ ] Design requirements are defined
- [ ] Technical approach is understood

### Refinement Process
1. **Story Review**: {Process for reviewing stories}
2. **Criteria Definition**: {Process for defining acceptance criteria}
3. **Estimation**: {Process for story point estimation}
4. **Dependency Mapping**: {Process for identifying dependencies}
5. **Prioritization**: {Process for priority assignment}

## Definition of Ready

### Story-Level Ready Criteria
- [ ] **User Story Format**: Follows "As a... I want... So that..." format
- [ ] **Acceptance Criteria**: Clear, testable criteria defined
- [ ] **Story Points**: Estimated by development team
- [ ] **Dependencies**: Identified and documented
- [ ] **Priority**: Assigned based on prioritization framework
- [ ] **Design Requirements**: UI/UX requirements defined
- [ ] **Technical Requirements**: Technical approach understood
- [ ] **Business Value**: Value proposition clearly articulated

### Epic-Level Ready Criteria
- [ ] **Epic Goal**: Clear objective defined
- [ ] **User Impact**: Target users and impact identified
- [ ] **Success Metrics**: Measurable outcomes defined
- [ ] **Story Breakdown**: High-level story list created
- [ ] **Dependencies**: Cross-epic dependencies identified
- [ ] **Timeline**: Rough timeline estimate provided

## Definition of Done

### Story-Level Done Criteria
- [ ] **Code Complete**: All code written and reviewed
- [ ] **Tests Passing**: Unit, integration, and acceptance tests pass
- [ ] **Documentation**: Code and user documentation updated
- [ ] **Acceptance Criteria**: All criteria met and verified
- [ ] **Code Review**: Peer review completed
- [ ] **Quality Gates**: All quality checks passed
- [ ] **Deployment**: Deployed to appropriate environment
- [ ] **Product Owner Sign-off**: PO accepts the story

### Epic-Level Done Criteria
- [ ] **All Stories Complete**: All epic stories meet DoD
- [ ] **Integration Testing**: Cross-story integration tested
- [ ] **User Acceptance**: UAT completed and passed
- [ ] **Performance Testing**: Performance requirements met
- [ ] **Documentation**: User and technical docs updated
- [ ] **Success Metrics**: Initial metrics captured
- [ ] **Rollout Complete**: Feature fully deployed
- [ ] **Stakeholder Sign-off**: Key stakeholders approve

## Backlog Metrics and KPIs

### Velocity Metrics
- **Current Velocity**: {Story points per sprint}
- **Velocity Trend**: {Improving/Stable/Declining}
- **Capacity Utilization**: {Percentage of capacity used}

### Quality Metrics
- **Story Completion Rate**: {Percentage of stories completed as planned}
- **Defect Rate**: {Defects per story}
- **Rework Rate**: {Percentage of stories requiring rework}

### Cycle Time Metrics
- **Lead Time**: {Time from story creation to completion}
- **Cycle Time**: {Time from story start to completion}
- **Queue Time**: {Time stories wait in backlog}

## Backlog Management

### Backlog Grooming Activities
1. **Story Creation**: {Process for creating new stories}
2. **Story Refinement**: {Process for refining existing stories}
3. **Priority Updates**: {Process for updating priorities}
4. **Dependency Management**: {Process for managing dependencies}
5. **Backlog Pruning**: {Process for removing obsolete stories}

### Stakeholder Involvement
- **Product Owner**: {Role and responsibilities}
- **Development Team**: {Role and responsibilities}
- **Scrum Master**: {Role and responsibilities}
- **Business Stakeholders**: {Role and responsibilities}

### Tools and Processes
- **Backlog Tool**: {Tool used for backlog management}
- **Estimation Process**: {How stories are estimated}
- **Priority Process**: {How priorities are assigned}
- **Review Process**: {How backlog is reviewed}

## Risk Management

### Backlog Risks
1. **{Risk}**: {Description}
   - Impact: {High/Medium/Low}
   - Probability: {High/Medium/Low}
   - Mitigation: {How to address}

2. **{Risk}**: {Description}
   - Impact: {High/Medium/Low}
   - Probability: {High/Medium/Low}
   - Mitigation: {How to address}

### Dependency Risks
- **External Dependencies**: {Dependencies outside team control}
- **Technical Dependencies**: {Technical prerequisites}
- **Resource Dependencies**: {Resource availability issues}

## AI Agent Instructions

When working with user story backlog:

1. Identify story dependencies and potential conflicts
2. Generate story point estimates based on complexity
3. Suggest story prioritization based on business value
4. Create acceptance criteria for user stories
5. Generate backlog health metrics and recommendations
6. Suggest story refinement improvements
7. Create sprint planning recommendations
8. Generate velocity and capacity forecasts
9. Identify backlog optimization opportunities
10. Create stakeholder communication summaries
```