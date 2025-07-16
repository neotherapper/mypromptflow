# Team Collaboration & Communication Flow Diagram

## Overview
This diagram illustrates how the 4-person team collaborates using AI tools throughout the development lifecycle.

---

## Team Structure & Responsibilities

```
┌─────────────────────────────────────────────────────────────┐
│                    TEAM HIERARCHY                            │
│                                                             │
│                 ┌─────────────────────┐                     │
│                 │ Head of Engineering │                     │
│                 │                     │                     │
│                 │ • Tech Leadership   │                     │
│                 │ • Architecture      │                     │
│                 │ • Code Reviews      │                     │
│                 │ • Team Coordination │                     │
│                 └──────────┬──────────┘                     │
│                            │                                │
│        ┌───────────────────┼───────────────────┐           │
│        │                   │                   │           │
│        v                   v                   v           │
│ ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│ │Lead Frontend │  │Lead Backend  │  │UI/UX Engineer│     │
│ │              │  │              │  │              │     │
│ │• React/TS    │  │• APIs        │  │• Design      │     │
│ │• UI Logic    │  │• Database    │  │• UX Research │     │
│ │• Performance │  │• Security    │  │• Prototypes  │     │
│ └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

---

## Daily Collaboration Patterns

### Morning Sync (9:00 AM)

```
┌─────────────────────────────────────────────────────────────┐
│                    DAILY STANDUP                            │
│                                                             │
│  All Team Members → JIRA Board → Claude Summary            │
│                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│  │ Yesterday   │  │   Today     │  │  Blockers   │       │
│  │             │  │             │  │             │       │
│  │ • Completed │  │ • Planned   │  │ • Technical │       │
│  │ • Progress  │  │ • Priority  │  │ • Dependencies│      │
│  └─────────────┘  └─────────────┘  └─────────────┘       │
│                                                             │
│  Head of Eng: Facilitates & removes blockers               │
│  Claude Max: Summarizes and tracks action items            │
└─────────────────────────────────────────────────────────────┘
```

---

## Feature Development Collaboration

### Stage 1-2: Requirements to Design

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Product Owner  │     │ UI/UX Engineer  │     │ Head of Eng     │
│                 │ --> │                 │ --> │                 │
│ Requirements    │     │ Design Process  │     │ Tech Review     │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                        │
         v                       v                        v
    JIRA Story              Figma Design            Architecture
         │                       │                        │
         └───────────────────────┴────────────────────────┘
                                 │
                                 v
                    ┌────────────────────────┐
                    │  Design Review Meeting  │
                    │                        │
                    │ • UI/UX presents       │
                    │ • Frontend feedback    │
                    │ • Technical feasibility│
                    │ • Claude analysis      │
                    └────────────────────────┘
```

---

## Parallel Development Coordination

### Stage 4: Implementation

```
┌─────────────────────────────────────────────────────────────┐
│                 FEATURE BRANCH WORKFLOW                      │
├─────────────────┬─────────────────┬─────────────────────────┤
│   Frontend      │    Backend      │     Integration         │
│                 │                 │                         │
│ Lead Frontend   │  Lead Backend   │   Head of Eng          │
│ Branch: feat/ui │  Branch: feat/api│  Reviews & Merges      │
│                 │                 │                         │
│ Morning:        │  Morning:       │   Continuous:           │
│ • Figma sync    │  • API design   │   • PR reviews          │
│ • Component dev │  • Schema update │   • Conflict resolution │
│                 │                 │   • Integration tests   │
│ Claude: $200    │  Claude: $100   │   Claude: $100          │
└─────────────────┴─────────────────┴─────────────────────────┘
                            │
                            v
                 ┌──────────────────────┐
                 │   API Contract       │
                 │   Coordination       │
                 │                      │
                 │ • Shared interface   │
                 │ • Mock data         │
                 │ • Testing hooks     │
                 └──────────────────────┘
```

---

## Code Review Collaboration

```
┌─────────────────────────────────────────────────────────────┐
│                    PULL REQUEST FLOW                         │
│                                                             │
│  Developer → Git Push → PR Creation → Review Assignment     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                            │
                            v
┌─────────────────────────────────────────────────────────────┐
│                  TWO-STAGE REVIEW                           │
├───────────────────────────┬─────────────────────────────────┤
│   Stage 1: AI Review      │   Stage 2: Human Review        │
│                           │                                 │
│ Claude Max Auto-Review:   │  Senior Developer Review:      │
│ • Code standards          │  • Business logic              │
│ • Security issues         │  • Architecture fit            │
│ • Performance concerns    │  • Domain knowledge            │
│ • Test coverage           │  • Strategic decisions         │
│                           │                                 │
│ Time: 5-10 minutes        │  Time: 15-30 minutes           │
└───────────────────────────┴─────────────────────────────────┘
```

---

## Design Handoff Workflow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  UI/UX Engineer │     │    Handoff      │     │ Lead Frontend   │
│                 │     │    Meeting      │     │   Developer     │
│ Figma Design    │ --> │                 │ --> │                 │
│ Complete        │     │ • Walkthrough   │     │ Implementation  │
└─────────────────┘     │ • Q&A Session   │     └─────────────────┘
                        │ • Specs Review  │
                        └─────────────────┘
                                │
                                v
                    ┌───────────────────────┐
                    │   Shared Resources    │
                    │                       │
                    │ • Figma Dev Mode      │
                    │ • Component Specs     │
                    │ • Design Tokens       │
                    │ • Gemini Analysis     │
                    └───────────────────────┘
```

---

## Knowledge Sharing Sessions

### Weekly AI Discovery Meeting (Fridays 3:00 PM)

```
┌─────────────────────────────────────────────────────────────┐
│                 KNOWLEDGE SHARING SESSION                    │
│                                                             │
│  Facilitator: Rotating team member                         │
│  Duration: 1 hour                                          │
│                                                             │
├─────────────────┬─────────────────┬─────────────────────────┤
│  AI Discoveries │ Tool Tips       │  Process Improvements  │
│                 │                 │                         │
│ • New prompts   │ • Shortcuts     │ • Workflow optimization│
│ • Use cases     │ • Integrations  │ • Automation ideas     │
│ • Productivity  │ • Best practices│ • Team suggestions     │
└─────────────────┴─────────────────┴─────────────────────────┘
                            │
                            v
                 ┌──────────────────────┐
                 │  Documentation       │
                 │                      │
                 │ • Team Wiki         │
                 │ • Prompt Library    │
                 │ • Process Updates   │
                 └──────────────────────┘
```

---

## Cross-Functional Collaboration Points

### Design ↔ Frontend

```
UI/UX Engineer              Lead Frontend Developer
     │                              │
     ├── Figma Comments ────────────┤
     ├── Design Tokens  ────────────┤
     ├── Component Specs ───────────┤
     └── Prototype Review ──────────┘
```

### Frontend ↔ Backend

```
Lead Frontend               Lead Backend
     │                           │
     ├── API Contracts ──────────┤
     ├── Data Models ────────────┤
     ├── Error Handling ─────────┤
     └── Performance Reqs ───────┘
```

### All Team ↔ Head of Engineering

```
Team Members                Head of Engineering
     │                           │
     ├── Architecture Review ────┤
     ├── Technical Decisions ────┤
     ├── Blocker Resolution ─────┤
     └── Code Standards ─────────┘
```

---

## Communication Channels

```
┌─────────────────────────────────────────────────────────────┐
│                   COMMUNICATION MATRIX                       │
├──────────────┬──────────────┬───────────────────────────────┤
│   Sync       │   Async      │   Documentation              │
│              │              │                              │
│ • Standup    │ • Slack/Teams│ • JIRA Comments              │
│ • Planning   │ • PR Reviews │ • Confluence/Wiki            │
│ • Retros     │ • Email      │ • Code Comments              │
│ • 1-on-1s    │ • JIRA       │ • README files               │
└──────────────┴──────────────┴───────────────────────────────┘
```

### Response Time Expectations
- **Blocker Issues**: < 30 minutes
- **PR Reviews**: < 4 hours
- **General Questions**: < 1 day
- **Non-urgent**: < 2 days

---

## Conflict Resolution Flow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ Technical       │     │   Discussion    │     │   Resolution    │
│ Disagreement    │ --> │                 │ --> │                 │
│                 │     │ • Facts/data    │     │ • Decision doc  │
│ • Architecture  │     │ • Pros/cons     │     │ • Action items  │
│ • Implementation│     │ • Claude analysis│    │ • Follow-up     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                │
                                v
                    ┌───────────────────────┐
                    │ Head of Engineering   │
                    │ Final Decision        │
                    └───────────────────────┘
```

---

## Team Metrics Dashboard

```
┌─────────────────────────────────────────────────────────────┐
│                    TEAM PERFORMANCE                          │
├─────────────────┬─────────────────┬─────────────────────────┤
│  Velocity       │  Quality        │  Collaboration          │
│                 │                 │                         │
│ • Story points  │ • Bug rate      │ • PR turnaround         │
│ • Cycle time    │ • Test coverage │ • Meeting efficiency    │
│ • AI usage      │ • Code quality  │ • Knowledge sharing     │
└─────────────────┴─────────────────┴─────────────────────────┘
```

---

## Diagram Implementation Notes

For visual creation:

1. **Use swimlanes** for role-based workflows
2. **Show temporal flow** with arrows and timestamps
3. **Highlight AI touchpoints** with special indicators
4. **Include feedback loops** for iterative processes
5. **Use avatars** for team members for clarity

Color suggestions:
- Team roles: Different colors per role
- AI tools: Consistent purple/blue theme
- Communication: Green for sync, yellow for async
- Decisions: Red for blockers, green for approved