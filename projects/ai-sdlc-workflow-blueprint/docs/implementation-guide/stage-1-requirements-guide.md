# Stage 1: Business Ideation & Requirements - Detailed Guide

## Overview
Transform business ideas into actionable development tickets using AI-powered analysis.

**Duration**: 1-2 days
**Key Participants**: Product Owner, Head of Engineering
**Primary Tool**: Claude Code Max ($100) with JIRA MCP

---

## Pre-Stage Checklist
- [ ] Product Owner has business need identified
- [ ] Head of Engineering available for collaboration
- [ ] Claude Code Max connected to JIRA via MCP
- [ ] Previous sprint velocity data available

---

## Step-by-Step Process

### Step 1: Initial Requirements Gathering (2-3 hours)

**Product Owner Actions**:
1. Document business need in plain language
2. Include context about users and goals
3. Note any constraints or deadlines
4. Gather any existing documentation

**Example Requirements Document**:
```markdown
# Customer Portal Requirements

## Business Need
Our insurance clients need self-service access to:
- View all their policies in one place
- File new claims without calling
- Track claim status in real-time
- Download policy documents

## User Context
- 50,000+ existing customers
- Age range: 25-65
- Varying tech competency
- Mobile usage: 60%

## Constraints
- Must integrate with existing auth system
- Comply with insurance regulations
- Launch before Q3 renewal season
```

### Step 2: AI-Powered Analysis (30-45 minutes)

**Head of Engineering Actions**:

1. **Open Claude Code Max** in terminal
2. **Load requirements** into Claude

**Claude Analysis Prompt**:
```
Analyze these requirements for a customer portal and provide:

1. Missing Technical Specifications:
   - Data requirements
   - Integration points  
   - Security needs
   - Performance targets

2. Clarification Questions:
   - Ambiguous requirements
   - Scope boundaries
   - Priority ordering

3. Technical Recommendations:
   - Architecture approach
   - Technology stack fit
   - Risk factors

4. Initial Estimates:
   - Development effort (story points)
   - Timeline estimate
   - Resource needs

[Paste requirements here]
```

**Expected Claude Output**:
- Structured gap analysis
- 10-15 clarification questions
- Technical consideration list
- Preliminary estimates

### Step 3: Clarification Session (1 hour)

**Meeting Setup**:
- Schedule: Product Owner + Head of Engineering
- Duration: 1 hour
- Tools: Video call + Shared Claude screen

**Meeting Agenda**:
```
1. Review Original Requirements (10 min)
   - Confirm understanding
   - Align on goals

2. Address Claude's Questions (30 min)
   - Go through each clarification
   - Document answers

3. Discuss Technical Aspects (15 min)
   - Integration points
   - Security requirements
   - Performance needs

4. Prioritize Features (5 min)
   - Must-have vs nice-to-have
   - Phasing approach
```

**Documentation During Meeting**:
```markdown
## Clarification Answers

Q: What authentication system exists?
A: OAuth2 with JWT, Azure AD backend

Q: Claims filing complexity?
A: Simple claims only initially (auto, property damage)

Q: Real-time requirements?
A: Status updates within 5 minutes acceptable
```

### Step 4: JIRA Ticket Creation (45 minutes)

**Head of Engineering Actions**:

1. **Prepare Claude for JIRA creation**

```bash
# Ensure MCP JIRA server is running
claude-mcp-server-jira status
```

2. **Create Epic and Stories**

**Claude JIRA Creation Prompt**:
```
Create JIRA tickets for Customer Portal based on our discussion:

Epic Details:
- Title: Customer Self-Service Portal
- Description: Enable customers to manage policies and claims online
- Due date: [Q3 date]

Create these stories:
1. User Authentication Integration
   - Connect to existing OAuth2 system
   - Session management
   - Password reset flow

2. Policy Dashboard
   - List all customer policies
   - Policy detail views
   - Document downloads

3. Claims Filing
   - New claim form
   - Photo upload capability
   - Submission confirmation

4. Claims Tracking
   - Status timeline view
   - Document uploads
   - Communication history

For each story include:
- Acceptance criteria (minimum 5)
- Story point estimate
- Technical notes
- Dependencies
```

3. **Review and Refine Tickets**

Check each ticket for:
- Clear acceptance criteria
- Reasonable estimates
- Proper dependencies
- Complete descriptions

### Step 5: Technical Planning (1 hour)

**Create Technical Specification**:

**Claude Technical Spec Prompt**:
```
Create a technical specification document for Customer Portal:

Include:
1. Architecture Overview
   - System components
   - Data flow diagrams
   - Integration points

2. API Design
   - Endpoint definitions
   - Request/response formats
   - Authentication flow

3. Data Models
   - Database schema
   - Object relationships
   - Migration strategy

4. Security Measures
   - Authentication/Authorization
   - Data encryption
   - Audit logging

5. Performance Requirements
   - Response time targets
   - Concurrent user limits
   - Scalability approach
```

---

## Deliverables Checklist

By end of Stage 1, you should have:

- [ ] **Business Requirements Document**
  - Original requirements
  - Clarification Q&A
  - Prioritized feature list

- [ ] **JIRA Tickets Created**
  - 1 Epic with description
  - 4-8 User stories
  - All with acceptance criteria
  - Story point estimates

- [ ] **Technical Specification**
  - Architecture overview
  - API contracts drafted
  - Security approach defined
  - Performance targets set

- [ ] **Stakeholder Alignment**
  - Product Owner approval
  - Technical feasibility confirmed
  - Timeline expectations set

---

## Common Pitfalls & Solutions

### Pitfall 1: Vague Requirements
**Problem**: "We need a better customer experience"
**Solution**: Use Claude to generate specific questions about user journeys, pain points, and success metrics

### Pitfall 2: Scope Creep
**Problem**: Requirements keep expanding during discussion
**Solution**: Document "Phase 2" items separately, focus on MVP for first release

### Pitfall 3: Missing Non-Functional Requirements
**Problem**: No mention of performance, security, accessibility
**Solution**: Use Claude's analysis to identify these gaps early

### Pitfall 4: Over-Estimation
**Problem**: Team consistently over-estimates story points
**Solution**: Reference historical velocity data in Claude analysis

---

## Success Metrics

Track these metrics for Stage 1:
- Time from idea to JIRA tickets: Target < 2 days
- Number of clarification rounds: Target = 1
- Percentage of stories changed after creation: Target < 20%
- Accuracy of initial estimates: Target ±20%

---

## Templates and Resources

### Requirements Template
```markdown
# [Feature Name] Requirements

## Business Objective
[What business goal does this serve?]

## User Stories
As a [user type], I want to [action] so that [benefit]

## Acceptance Criteria
- [ ] Given [context], when [action], then [result]

## Constraints
- Technical: 
- Business:
- Timeline:

## Success Metrics
- 
```

### Claude Prompts Library
1. **Requirements Analysis**: "Analyze these requirements and identify gaps..."
2. **Story Creation**: "Create user stories with acceptance criteria for..."
3. **Estimation**: "Estimate story points based on complexity of..."
4. **Risk Assessment**: "Identify technical risks in implementing..."

---

## Transition to Stage 2

Stage 1 is complete when:
- All tickets are in JIRA with "Ready for Design" status
- Technical approach is documented
- Team has shared understanding of scope
- UI/UX Engineer is briefed on requirements

Next: UI/UX Engineer begins Stage 2 design work