# Complete AI-Enhanced SDLC Implementation Guide

## Table of Contents
1. [Overview](#overview)
2. [Stage 1: Business Ideation & Requirements](#stage-1-business-ideation--requirements)
3. [Stage 2: Design & Architecture](#stage-2-design--architecture)
4. [Stage 3: Development Planning](#stage-3-development-planning)
5. [Stage 4: Implementation](#stage-4-implementation)
6. [Stage 5: Testing & Quality Assurance](#stage-5-testing--quality-assurance)
7. [Stage 6: Deployment & Monitoring](#stage-6-deployment--monitoring)

---

## Overview

This guide provides detailed, step-by-step procedures for implementing the 6-stage AI-enhanced SDLC workflow with your 4-person team.

**Team Composition**:
- Head of Engineering (Claude Max $100)
- Lead Frontend Developer (Claude Max $200, Figma $15)
- Lead Backend Developer (Claude Max $100)
- UI/UX Engineer (Figma $15)

**All team members also have**: Cursor IDE (free), Gemini CLI (free)

---

## Stage 1: Business Ideation & Requirements
**Duration**: 1-2 days per feature
**Participants**: Product Owner + Head of Engineering

### Step 1.1: Requirements Submission

**WHO**: Product Owner
**TOOL**: Email/Slack/Meeting
**ACTION**: Submit business requirements in natural language

Example submission:
```
"We need to add a customer portal where clients can view their policies, 
file claims, and track claim status. Should integrate with our existing 
authentication system."
```

### Step 1.2: AI-Powered Requirements Analysis

**WHO**: Head of Engineering
**TOOL**: Claude Code Max ($100)
**ACTION**: Analyze requirements for completeness

Claude prompt template:
```
Analyze these business requirements and identify:
1. Missing specifications
2. Technical dependencies
3. Security considerations
4. Estimated complexity
5. Suggested acceptance criteria

Requirements: [paste requirements here]
```

**OUTPUT**: Gap analysis document with clarification questions

### Step 1.3: Clarification Meeting

**WHO**: Product Owner + Head of Engineering
**TOOL**: Video call + Claude Code Max
**ACTION**: Review gaps and get clarifications

Meeting agenda:
1. Review identified gaps (10 min)
2. Discuss technical feasibility (15 min)
3. Define success metrics (10 min)
4. Agree on priorities (10 min)

### Step 1.4: JIRA Ticket Creation

**WHO**: Head of Engineering
**TOOL**: Claude Code Max with JIRA MCP
**ACTION**: Create structured tickets

Claude command:
```
Create JIRA epic and stories for customer portal with:
- Epic: Customer Self-Service Portal
- Stories for: authentication, policy view, claim filing, status tracking
- Include acceptance criteria from our discussion
- Add story point estimates
```

**OUTPUT**: 
- 1 Epic in JIRA
- 4-6 User Stories with acceptance criteria
- Initial story point estimates

### Success Criteria Stage 1
- [ ] Clear requirements documented
- [ ] All gaps addressed
- [ ] JIRA tickets created
- [ ] Acceptance criteria defined
- [ ] Initial estimates provided

---

## Stage 2: Design & Architecture
**Duration**: 2-3 days per feature
**Participants**: UI/UX Engineer + Lead Frontend + Head of Engineering

### Step 2.1: Design Kickoff

**WHO**: UI/UX Engineer + Lead Frontend
**TOOL**: Figma + Meeting
**ACTION**: Review requirements and plan design approach

Tasks:
1. Review JIRA tickets together (30 min)
2. Identify UI components needed
3. Discuss user flow
4. Plan responsive breakpoints

### Step 2.2: Initial Wireframes

**WHO**: UI/UX Engineer
**TOOL**: Figma Professional ($15)
**ACTION**: Create low-fidelity wireframes

Figma structure:
```
Customer Portal/
├── Wireframes/
│   ├── Dashboard
│   ├── Policy List
│   ├── Policy Details
│   ├── Claim Form
│   └── Claim Status
└── Components/
    ├── Navigation
    ├── Cards
    └── Forms
```

### Step 2.3: Design System Integration

**WHO**: UI/UX Engineer
**TOOL**: Figma + Gemini CLI
**ACTION**: Apply design system and create components

Gemini CLI usage:
```bash
# Analyze existing design system
gemini "analyze our design system in /design-system 
and suggest how to implement customer portal components"

# Generate component specifications
gemini "create component specs for PolicyCard 
based on this Figma design [screenshot]"
```

### Step 2.4: Technical Architecture

**WHO**: Head of Engineering + Lead Backend
**TOOL**: Claude Code Max
**ACTION**: Define technical architecture

Architecture decisions to make:
1. API structure (REST vs GraphQL)
2. State management approach
3. Authentication flow
4. Data caching strategy
5. Security measures

Claude prompt:
```
Design technical architecture for customer portal:
- Existing auth: OAuth2 with JWT
- Backend: Node.js/Express
- Frontend: React/TypeScript
- Database: PostgreSQL
Include API endpoints, data flow, and security considerations
```

### Step 2.5: Design Review & Handoff

**WHO**: Full team
**TOOL**: Figma + Meeting
**ACTION**: Review and approve designs

Review checklist:
- [ ] All user flows covered
- [ ] Responsive designs complete
- [ ] Accessibility requirements met
- [ ] Component specifications clear
- [ ] Technical feasibility confirmed

**OUTPUT**:
- Approved Figma designs
- Component specifications
- API contract documentation
- Architecture decision record

---

## Stage 3: Development Planning
**Duration**: 0.5-1 day (sprint planning)
**Participants**: Full team

### Step 3.1: Sprint Planning Preparation

**WHO**: Head of Engineering
**TOOL**: Claude Code Max + JIRA
**ACTION**: Prepare sprint backlog

Claude prompt:
```
Analyze our team velocity (last 3 sprints: 32, 35, 30 points)
Current capacity: 4 developers, 2-week sprint
Recommend stories for next sprint from customer portal epic
Consider dependencies and parallel work opportunities
```

### Step 3.2: Sprint Planning Meeting

**WHO**: Full team
**TOOL**: JIRA + Video call
**DURATION**: 2 hours

Agenda:
1. **Sprint Goal** (15 min)
   - Define what we'll demo at sprint end
   
2. **Story Review** (45 min)
   - Review each story
   - Clarify requirements
   - Identify dependencies

3. **Task Breakdown** (45 min)
   - Break stories into tasks
   - Assign based on expertise
   - Estimate hours

4. **Commitment** (15 min)
   - Final capacity check
   - Team agreement

### Step 3.3: Task Assignment

**WHO**: Team members
**TOOL**: JIRA
**ACTION**: Self-assign tasks based on expertise

Assignment guidelines:
- **Frontend tasks** → Lead Frontend
- **Backend/API** → Lead Backend  
- **Design updates** → UI/UX Engineer
- **Integration/Review** → Head of Engineering

### Step 3.4: Development Environment Setup

**WHO**: Each developer
**TOOL**: Git + Cursor IDE
**ACTION**: Create feature branches

```bash
# Frontend developer
git checkout -b feature/customer-portal-ui

# Backend developer
git checkout -b feature/customer-portal-api

# Create draft PRs immediately
gh pr create --draft --title "Customer Portal UI" --body "..."
```

---

## Stage 4: Implementation
**Duration**: 1-2 week sprints
**Participants**: All developers

### Step 4.1: Daily Development Workflow

#### Morning Standup (9:00 AM, 15 min)

**WHO**: Full team
**TOOL**: JIRA + Claude Code Max
**FORMAT**: 
```
Each person shares:
1. Yesterday's progress
2. Today's plan
3. Any blockers

Head of Eng: Updates JIRA, removes blockers
```

#### Development Sessions

### Step 4.2: Frontend Implementation

**WHO**: Lead Frontend Developer
**TOOLS**: Claude Max ($200) + Cursor IDE + Figma

Daily workflow:
```
9:15 AM - Review Figma designs
9:30 AM - Claude session for component generation

Claude prompt example:
"Create a React component for PolicyCard based on:
- Props: policyNumber, type, status, premium, expiryDate
- Use our existing Card component from design system
- Include TypeScript types
- Add loading and error states"

10:00 AM - Implementation in Cursor IDE
12:00 PM - Commit progress

Afternoon:
2:00 PM - Integration with API
3:00 PM - Testing
4:00 PM - PR update
```

### Step 4.3: Backend Implementation

**WHO**: Lead Backend Developer
**TOOLS**: Claude Max ($100) + Cursor IDE

Daily workflow:
```
9:15 AM - Review API requirements
9:30 AM - Database schema design

Claude prompt:
"Design PostgreSQL schema for:
- policies table (existing)
- claims table (new)
- claim_status_history table (new)
Include indexes and foreign keys"

10:00 AM - API endpoint development
12:00 PM - Unit test creation

Afternoon:
2:00 PM - Integration testing
3:00 PM - Documentation
4:00 PM - PR update
```

### Step 4.4: Design Support

**WHO**: UI/UX Engineer
**TOOLS**: Figma + Gemini CLI

Daily tasks:
```
Morning:
- Review implementation progress
- Create any missing assets
- Update design specs if needed

Gemini CLI usage:
"Convert this Figma component to React code 
with Tailwind classes"

Afternoon:
- Support developers with design questions
- Validate implementation matches design
- Document any design decisions
```

### Step 4.5: Code Review Process

**WHO**: Head of Engineering + PR Author
**TOOLS**: Claude Code Max + GitHub

Two-stage review:
```
Stage 1: Automated (5-10 min)
- Claude reviews PR for standards
- Security scan
- Test coverage check

Stage 2: Human Review (15-30 min)
- Business logic validation
- Architecture compliance
- Performance considerations
```

Review checklist:
- [ ] Code follows team standards
- [ ] Tests included and passing
- [ ] Documentation updated
- [ ] No security vulnerabilities
- [ ] Performance acceptable

---

## Stage 5: Testing & Quality Assurance
**Duration**: Continuous with development
**Participants**: All developers + AI automation

### Step 5.1: Unit Testing

**WHO**: Developer who wrote the code
**TOOL**: Claude Code Max + Vitest

Test creation workflow:
```
Claude prompt:
"Generate comprehensive unit tests for PolicyService including:
- Happy path scenarios
- Error handling
- Edge cases
- Mock external dependencies"
```

Coverage requirements:
- Minimum 80% code coverage
- All critical paths tested
- Error scenarios covered

### Step 5.2: Integration Testing

**WHO**: Lead Backend + Lead Frontend
**TOOL**: Cypress/Playwright + Claude

Test scenarios:
1. Full user journey tests
2. API integration tests
3. Authentication flow
4. Error handling
5. Performance tests

### Step 5.3: User Acceptance Testing

**WHO**: Product Owner + UI/UX Engineer
**TOOL**: Staging environment
**ACTION**: Validate against requirements

UAT checklist:
- [ ] All acceptance criteria met
- [ ] User flows work as expected
- [ ] Design matches approved mockups
- [ ] Performance acceptable
- [ ] No critical bugs

### Step 5.4: Bug Management

**WHO**: Whoever finds the bug
**TOOL**: JIRA
**ACTION**: Create bug ticket

Bug ticket template:
```
Summary: [Brief description]
Environment: [Dev/Staging/Prod]
Steps to Reproduce:
1. 
2. 
Expected: 
Actual:
Screenshot/Video: 
Severity: [Critical/High/Medium/Low]
```

---

## Stage 6: Deployment & Monitoring
**Duration**: 1-2 hours per release
**Participants**: Lead Backend + DevOps automation

### Step 6.1: Release Preparation

**WHO**: Head of Engineering
**TOOL**: Claude Code Max + Git

Pre-release checklist:
```
Claude prompt:
"Generate release notes for v2.3.0 including:
- New features (customer portal)
- Bug fixes from JIRA
- Breaking changes
- Upgrade instructions"
```

Tasks:
- [ ] All PRs merged
- [ ] Tests passing
- [ ] Release notes ready
- [ ] Rollback plan documented

### Step 6.2: Deployment Process

**WHO**: Lead Backend
**TOOL**: CI/CD Pipeline + Monitoring

Deployment steps:
```bash
# 1. Tag release
git tag -a v2.3.0 -m "Customer Portal Release"
git push origin v2.3.0

# 2. Deploy to staging
./deploy.sh staging

# 3. Smoke tests
npm run test:staging

# 4. Deploy to production (blue-green)
./deploy.sh production

# 5. Verify deployment
curl https://api.example.com/health
```

### Step 6.3: Post-Deployment Monitoring

**WHO**: Lead Backend + Head of Engineering
**TOOL**: Monitoring Dashboard

Monitor for 2 hours:
- Error rates
- Response times  
- CPU/Memory usage
- User activity
- Any anomalies

Alert thresholds:
- Error rate > 1%
- Response time > 2s
- CPU > 80%
- Memory > 85%

### Step 6.4: Success Validation

**WHO**: Full team
**TOOL**: Analytics + User Feedback

Success metrics:
- [ ] No critical issues in 24 hours
- [ ] Performance meets SLAs
- [ ] User adoption tracking started
- [ ] Positive initial feedback

---

## Continuous Improvement

### Weekly Retrospective

**WHO**: Full team
**WHEN**: Friday 4:00 PM
**DURATION**: 1 hour

Format:
1. What went well?
2. What could improve?
3. Action items
4. AI tool learnings

### Monthly Metrics Review

Track and review:
- Velocity trends
- Defect rates
- Cycle time
- AI tool usage
- ROI metrics

---

## Quick Reference Cards

### Daily Checklist
- [ ] Morning standup
- [ ] JIRA updates
- [ ] Development work
- [ ] Code commits
- [ ] PR updates
- [ ] End-of-day status

### Claude Prompts Library
- Requirements analysis
- Code generation
- Test creation
- Documentation
- Code review
- Release notes

### Emergency Procedures
- Production issues → Head of Engineering
- Security concerns → Immediate team alert
- Major bugs → Stop current work
- Rollback needed → Follow rollback plan