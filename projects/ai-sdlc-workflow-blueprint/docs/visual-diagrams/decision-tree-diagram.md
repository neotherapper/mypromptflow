# Decision Tree Diagram

## Overview
This diagram provides a visual guide for tool selection, process decisions, and implementation choices throughout the AI-SDLC workflow, with clear decision criteria and recommended paths.

---

## Master Decision Tree: AI-SDLC Implementation

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         AI-SDLC IMPLEMENTATION DECISION TREE                    │
└─────────────────────────────────────────────────────────────────────────────────┘

                                START HERE
                                    │
                                    ▼
                        ┌───────────────────────┐
                        │ Team Size & Budget    │
                        │ Assessment            │
                        └───────────┬───────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
            ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
            │ 2-4 People  │ │ 5-8 People  │ │ 9+ People   │
            │ Startup     │ │ Growth      │ │ Enterprise  │
            └─────────────┘ └─────────────┘ └─────────────┘
                    │               │               │
                    ▼               ▼               ▼
            ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
            │ Budget:     │ │ Budget:     │ │ Budget:     │
            │ $500-800/mo │ │ $800-1500/mo│ │ $1500+/mo  │
            │             │ │             │ │             │
            │ → MVP       │ │ → Scale     │ │ → Enterprise│
            │   Approach  │ │   Approach  │ │   Approach  │
            └─────────────┘ └─────────────┘ └─────────────┘
                    │
                    ▼
        ┌─────────────────────────────────────────────────────────────┐
        │                MVP APPROACH (4-Person Team)                  │
        │                                                             │
        │ ✅ Recommended for: Startups, Small Teams, Budget-Conscious │
        │ ✅ Total Cost: $616/month                                   │
        │ ✅ ROI: 420% by Month 12                                    │
        │ ✅ Payback: 3.2 months                                      │
        └─────────────────────────────────────────────────────────────┘
```

---

## Tool Selection Decision Tree

### AI Tool Allocation Decision
```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        AI TOOL ALLOCATION DECISION                              │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│                     Who needs AI assistance?                                   │
│                            │                                                   │
│              ┌─────────────┼─────────────┐                                    │
│              │             │             │                                    │
│              ▼             ▼             ▼                                    │
│    ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                          │
│    │ Lead        │ │ Lead        │ │ Head of     │                          │
│    │ Backend     │ │ Frontend    │ │ Engineering │                          │
│    │ Developer   │ │ Developer   │ │             │                          │
│    └─────────────┘ └─────────────┘ └─────────────┘                          │
│          │               │               │                                    │
│          ▼               ▼               ▼                                    │
│    ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                          │
│    │ Complexity: │ │ Complexity: │ │ Complexity: │                          │
│    │ HIGH        │ │ HIGH        │ │ MEDIUM      │                          │
│    │             │ │             │ │             │                          │
│    │ Tasks:      │ │ Tasks:      │ │ Tasks:      │                          │
│    │ • API Dev   │ │ • React/TS  │ │ • Reviews   │                          │
│    │ • Database  │ │ • UI Logic  │ │ • Architecture│                        │
│    │ • Security  │ │ • State Mgmt│ │ • Coordination│                        │
│    │ • Performance│ │ • Testing   │ │ • Planning  │                          │
│    │             │ │             │ │             │                          │
│    │ → $200/mo   │ │ → $200/mo   │ │ → $100/mo   │                          │
│    │   Claude Max│ │   Claude Max│ │   Claude Max│                          │
│    └─────────────┘ └─────────────┘ └─────────────┘                          │
│                                                                                 │
│ 📊 TOTAL AI INVESTMENT: $500/month                                             │
│ 📊 EXPECTED PRODUCTIVITY GAIN: 320% overall                                    │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Development Environment Decision
```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                    DEVELOPMENT ENVIRONMENT DECISION                             │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│                  What's your team's current setup?                             │
│                                │                                               │
│                 ┌──────────────┼──────────────┐                               │
│                 │              │              │                               │
│                 ▼              ▼              ▼                               │
│        ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                       │
│        │ Experienced │ │ Mixed       │ │ New Team    │                       │
│        │ Local Devs  │ │ Experience  │ │ Members     │                       │
│        └─────────────┘ └─────────────┘ └─────────────┘                       │
│                │              │              │                               │
│                ▼              ▼              ▼                               │
│        ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                       │
│        │ ✅ LOCAL    │ │ ✅ LOCAL    │ │ ⚠️ LOCAL    │                       │
│        │ DEVELOPMENT │ │ DEVELOPMENT │ │ DEVELOPMENT │                       │
│        │             │ │             │ │             │                       │
│        │ Benefits:   │ │ Benefits:   │ │ Benefits:   │                       │
│        │ • Full      │ │ • Cost      │ │ • Learning  │                       │
│        │   Control   │ │   Effective │ │   Opportunity│                       │
│        │ • Offline   │ │ • Skill     │ │ • Ownership │                       │
│        │   Capable   │ │   Building  │ │             │                       │
│        │ • Fast      │ │ • Flexible  │ │ Challenges: │                       │
│        │   Performance│ │             │ │ • Setup Time│                       │
│        │             │ │ Support:    │ │ • Initial   │                       │
│        │ → $0/month  │ │ • Training  │ │   Complexity│                       │
│        │   Added     │ │ • Docs      │ │             │                       │
│        │   Cost      │ │ • Mentoring │ │ → Consider  │                       │
│        │             │ │             │ │   GitPod    │                       │
│        │             │ │ → $0/month  │ │   Year 2    │                       │
│        │             │ │   Added     │ │             │                       │
│        │             │ │   Cost      │ │             │                       │
│        └─────────────┘ └─────────────┘ └─────────────┘                       │
│                                                                                 │
│ 📊 RECOMMENDED: Local Development for MVP                                      │
│ 📊 FUTURE OPTION: GitPod for Year 2 team expansion                            │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Process Decision Trees

### Branch Strategy Decision
```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                       BRANCH STRATEGY DECISION TREE                            │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│                   How complex are your features?                               │
│                                │                                               │
│                 ┌──────────────┼──────────────┐                               │
│                 │              │              │                               │
│                 ▼              ▼              ▼                               │
│        ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                       │
│        │ Simple      │ │ Moderate    │ │ Complex     │                       │
│        │ Features    │ │ Features    │ │ Features    │                       │
│        │             │ │             │ │             │                       │
│        │ • Single    │ │ • Frontend  │ │ • Multiple  │                       │
│        │   Component │ │   + Backend │ │   Systems   │                       │
│        │ • Minor     │ │ • Database  │ │ • Breaking  │                       │
│        │   Changes   │ │   Changes   │ │   Changes   │                       │
│        └─────────────┘ └─────────────┘ └─────────────┘                       │
│                │              │              │                               │
│                ▼              ▼              ▼                               │
│        ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                       │
│        │ ✅ UNIFIED  │ │ ✅ UNIFIED  │ │ ⚠️ UNIFIED  │                       │
│        │ FEATURE     │ │ FEATURE     │ │ FEATURE     │                       │
│        │ BRANCH      │ │ BRANCH      │ │ BRANCH      │                       │
│        │             │ │             │ │             │                       │
│        │ Benefits:   │ │ Benefits:   │ │ Benefits:   │                       │
│        │ • Fast      │ │ • Complete  │ │ • Atomic    │                       │
│        │   Review    │ │   Testing   │ │   Changes   │                       │
│        │ • Quick     │ │ • Stakeholder│ │ • Complete  │                       │
│        │   Deploy    │ │   Validation│ │   Validation│                       │
│        │             │ │ • Reduced   │ │             │                       │
│        │ → Single PR │ │   Integration│ │ Considerations:│                   │
│        │   Workflow  │ │   Issues    │ │ • Large PR  │                       │
│        │             │ │             │ │ • Complex   │                       │
│        │             │ │ → Single PR │ │   Review    │                       │
│        │             │ │   Workflow  │ │ • Longer    │                       │
│        │             │ │             │ │   Cycle     │                       │
│        │             │ │             │ │             │                       │
│        │             │ │             │ │ → Single PR │                       │
│        │             │ │             │ │   Workflow  │                       │
│        │             │ │             │ │   with      │                       │
│        │             │ │             │ │   Enhanced  │                       │
│        │             │ │             │ │   Reviews   │                       │
│        └─────────────┘ └─────────────┘ └─────────────┘                       │
│                                                                                 │
│ 📊 RECOMMENDED: Unified Feature Branch for all scenarios                       │
│ 📊 RATIONALE: Better integration testing and stakeholder validation            │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Testing Strategy Decision
```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                       TESTING STRATEGY DECISION TREE                           │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│                 What's your quality requirement?                               │
│                                │                                               │
│                 ┌──────────────┼──────────────┐                               │
│                 │              │              │                               │
│                 ▼              ▼              ▼                               │
│        ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                       │
│        │ Standard    │ │ High        │ │ Critical    │                       │
│        │ Quality     │ │ Quality     │ │ Mission     │                       │
│        │             │ │             │ │ Critical    │                       │
│        │ • MVP       │ │ • Production│ │ • Enterprise│                       │
│        │ • Prototype │ │ • Customer  │ │ • Regulated │                       │
│        │ • Internal  │ │ • Facing    │ │ • Financial │                       │
│        └─────────────┘ └─────────────┘ └─────────────┘                       │
│                │              │              │                               │
│                ▼              ▼              ▼                               │
│        ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                       │
│        │ ✅ AI-BASIC │ │ ✅ AI-ENHANCED│ │ ✅ AI-COMPREHENSIVE│                │
│        │ TESTING     │ │ TESTING     │ │ TESTING     │                       │
│        │             │ │             │ │             │                       │
│        │ Coverage:   │ │ Coverage:   │ │ Coverage:   │                       │
│        │ • 70% Unit  │ │ • 85% Unit  │ │ • 95% Unit  │                       │
│        │ • 50% Integ │ │ • 70% Integ │ │ • 90% Integ │                       │
│        │ • 30% E2E   │ │ • 60% E2E   │ │ • 80% E2E   │                       │
│        │             │ │             │ │             │                       │
│        │ AI Support: │ │ AI Support: │ │ AI Support: │                       │
│        │ • Test Gen  │ │ • Test Gen  │ │ • Test Gen  │                       │
│        │ • Basic     │ │ • Mock Data │ │ • Mock Data │                       │
│        │   Validation│ │ • Coverage  │ │ • Coverage  │                       │
│        │             │ │ • Performance│ │ • Performance│                      │
│        │ → Claude    │ │             │ │ • Security  │                       │
│        │   Assistance│ │ → Claude    │ │ • Compliance│                       │
│        │   Basic     │ │   Assistance│ │             │                       │
│        │             │ │   Standard  │ │ → Claude    │                       │
│        │             │ │             │ │   Assistance│                       │
│        │             │ │             │ │   Advanced  │                       │
│        └─────────────┘ └─────────────┘ └─────────────┘                       │
│                                                                                 │
│ 📊 RECOMMENDED: AI-Enhanced Testing for Production Applications                 │
│ 📊 SCALABLE: Start with AI-Basic, evolve to AI-Enhanced                       │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Implementation Phase Decision Trees

### Team Onboarding Decision
```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      TEAM ONBOARDING DECISION TREE                             │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│                What's your team's AI experience?                               │
│                                │                                               │
│                 ┌──────────────┼──────────────┐                               │
│                 │              │              │                               │
│                 ▼              ▼              ▼                               │
│        ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                       │
│        │ AI          │ │ Some AI     │ │ No AI       │                       │
│        │ Experienced │ │ Experience  │ │ Experience  │                       │
│        │             │ │             │ │             │                       │
│        │ • Previous  │ │ • Casual    │ │ • New to    │                       │
│        │   AI Tools  │ │   Usage     │ │   AI Tools  │                       │
│        │ • Prompt    │ │ • Basic     │ │ • Traditional│                       │
│        │   Engineer  │ │   Prompting │ │   Development│                       │
│        └─────────────┘ └─────────────┘ └─────────────┘                       │
│                │              │              │                               │
│                ▼              ▼              ▼                               │
│        ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                       │
│        │ ✅ FAST     │ │ ✅ STANDARD │ │ ✅ INTENSIVE│                       │
│        │ TRACK       │ │ TRACK       │ │ TRACK       │                       │
│        │             │ │             │ │             │                       │
│        │ Duration:   │ │ Duration:   │ │ Duration:   │                       │
│        │ • 1 week    │ │ • 2 weeks   │ │ • 3-4 weeks │                       │
│        │             │ │             │ │             │                       │
│        │ Focus:      │ │ Focus:      │ │ Focus:      │                       │
│        │ • Tool      │ │ • Prompt    │ │ • AI Basics │                       │
│        │   Specific  │ │   Engineering│ │ • Prompt    │                       │
│        │ • Advanced  │ │ • Workflow  │ │   Engineering│                       │
│        │   Techniques│ │   Integration│ │ • Workflow  │                       │
│        │ • Custom    │ │ • Best      │ │   Mastery   │                       │
│        │   Prompts   │ │   Practices │ │ • Best      │                       │
│        │             │ │             │ │   Practices │                       │
│        │ → Start     │ │ → Start     │ │ → Start     │                       │
│        │   Week 1    │ │   Week 1    │ │   Week 1    │                       │
│        │             │ │             │ │             │                       │
│        └─────────────┘ └─────────────┘ └─────────────┘                       │
│                                                                                 │
│ 📊 RECOMMENDED: Assess team individually, mix tracks as needed                  │
│ 📊 SUCCESS METRIC: 80% productivity gain by end of training                    │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Scaling Decision Tree
```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         SCALING DECISION TREE                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│                 When should you consider scaling?                              │
│                                │                                               │
│                 ┌──────────────┼──────────────┐                               │
│                 │              │              │                               │
│                 ▼              ▼              ▼                               │
│        ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                       │
│        │ Month 6-8   │ │ Month 9-12  │ │ Month 12+   │                       │
│        │ Early       │ │ Growth      │ │ Scale       │                       │
│        │ Success     │ │ Validation  │ │ Phase       │                       │
│        │             │ │             │ │             │                       │
│        │ Indicators: │ │ Indicators: │ │ Indicators: │                       │
│        │ • 200% ROI  │ │ • 400% ROI  │ │ • 1000% ROI │                       │
│        │ • Team      │ │ • Process   │ │ • Market    │                       │
│        │   Comfort   │ │   Mature    │ │   Demand    │                       │
│        │ • Stable    │ │ • Proven    │ │ • Capacity  │                       │
│        │   Workflow  │ │   Metrics   │ │   Constraints│                       │
│        └─────────────┘ └─────────────┘ └─────────────┘                       │
│                │              │              │                               │
│                ▼              ▼              ▼                               │
│        ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                       │
│        │ ⚠️ WAIT     │ │ ✅ CONSIDER │ │ ✅ SCALE    │                       │
│        │ Continue    │ │ EXPANSION   │ │ AGGRESSIVELY│                       │
│        │ Optimizing  │ │             │ │             │                       │
│        │             │ │ Options:    │ │ Options:    │                       │
│        │ Focus:      │ │ • Add 1-2   │ │ • Add 3-4   │                       │
│        │ • Process   │ │   Developers│ │   Developers│                       │
│        │   Refinement│ │ • Add QA    │ │ • Add QA    │                       │
│        │ • Skill     │ │   Specialist│ │   Team      │                       │
│        │   Building  │ │ • GitPod    │ │ • DevOps    │                       │
│        │ • Metric    │ │   for New   │ │   Specialist│                       │
│        │   Tracking  │ │   Members   │ │ • GitPod    │                       │
│        │             │ │             │ │   Infrastructure│                    │
│        │ → Continue  │ │ → Gradual   │ │ • Advanced  │                       │
│        │   Current   │ │   Expansion │ │   AI Tools  │                       │
│        │   Setup     │ │             │ │             │                       │
│        │             │ │ Cost:       │ │ Cost:       │                       │
│        │             │ │ $800-1200/mo│ │ $1500-2500/mo│                      │
│        └─────────────┘ └─────────────┘ └─────────────┘                       │
│                                                                                 │
│ 📊 RECOMMENDED: Wait for strong ROI validation before scaling                   │
│ 📊 KEY METRIC: 400%+ ROI for 3+ months before major expansion                 │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Risk Assessment Decision Trees

### Risk Mitigation Decision
```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                      RISK MITIGATION DECISION TREE                             │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│                  What's your risk tolerance?                                   │
│                                │                                               │
│                 ┌──────────────┼──────────────┐                               │
│                 │              │              │                               │
│                 ▼              ▼              ▼                               │
│        ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                       │
│        │ Low Risk    │ │ Medium Risk │ │ High Risk   │                       │
│        │ Tolerance   │ │ Tolerance   │ │ Tolerance   │                       │
│        │             │ │             │ │             │                       │
│        │ • Enterprise│ │ • Growing   │ │ • Startup   │                       │
│        │ • Regulated │ │   Company   │ │ • Agile     │                       │
│        │ • Critical  │ │ • Balanced  │ │ • Innovation│                       │
│        │   Systems   │ │   Approach  │ │   Focused   │                       │
│        └─────────────┘ └─────────────┘ └─────────────┘                       │
│                │              │              │                               │
│                ▼              ▼              ▼                               │
│        ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                       │
│        │ ✅ PHASED   │ │ ✅ PARALLEL │ │ ✅ FULL     │                       │
│        │ ROLLOUT     │ │ ROLLOUT     │ │ ROLLOUT     │                       │
│        │             │ │             │ │             │                       │
│        │ Approach:   │ │ Approach:   │ │ Approach:   │                       │
│        │ • Month 1-2:│ │ • Month 1:  │ │ • Month 1:  │                       │
│        │   1 person  │ │   2 people  │ │   All team  │                       │
│        │ • Month 3-4:│ │ • Month 2:  │ │   members   │                       │
│        │   2 people  │ │   Add 1     │ │ • Full      │                       │
│        │ • Month 5-6:│ │ • Month 3:  │ │   workflow  │                       │
│        │   Full team │ │   Full team │ │ • Rapid     │                       │
│        │             │ │             │ │   feedback  │                       │
│        │ Benefits:   │ │ Benefits:   │ │             │                       │
│        │ • Gradual   │ │ • Balanced  │ │ Benefits:   │                       │
│        │   Learning  │ │   Risk      │ │ • Fastest   │                       │
│        │ • Low Risk  │ │ • Faster    │ │   Results   │                       │
│        │ • Validated │ │   than      │ │ • Maximum   │                       │
│        │   Approach  │ │   Phased    │ │   Impact    │                       │
│        │             │ │             │ │ • Early     │                       │
│        │ → 6-month   │ │ → 3-month   │ │   ROI       │                       │
│        │   timeline  │ │   timeline  │ │             │                       │
│        │             │ │             │ │ → 1-month   │                       │
│        │             │ │             │ │   timeline  │                       │
│        └─────────────┘ └─────────────┘ └─────────────┘                       │
│                                                                                 │
│ 📊 RECOMMENDED: Parallel rollout for balanced risk and speed                    │
│ 📊 FALLBACK: Always maintain ability to revert to traditional methods          │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Quick Reference Decision Matrix

### At-a-Glance Decision Guide
```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                        QUICK DECISION REFERENCE                                 │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│ Question: "Should we implement AI-SDLC?"                                       │
│ Answer: ✅ YES - if you have 2+ developers and $500+ budget                   │
│                                                                                 │
│ Question: "Local or Cloud development?"                                        │
│ Answer: ✅ LOCAL - for MVP, GitPod for Year 2                                 │
│                                                                                 │
│ Question: "How much AI budget per developer?"                                  │
│ Answer: ✅ $200 for leads, $100 for head of engineering                       │
│                                                                                 │
│ Question: "Single or separate branches?"                                       │
│ Answer: ✅ UNIFIED - single feature branch for all changes                    │
│                                                                                 │
│ Question: "When to start scaling?"                                             │
│ Answer: ✅ MONTH 9-12 - after 400%+ ROI validation                           │
│                                                                                 │
│ Question: "Risk mitigation strategy?"                                          │
│ Answer: ✅ PARALLEL - balanced risk and speed                                 │
│                                                                                 │
│ Question: "Training approach?"                                                 │
│ Answer: ✅ MIXED - assess team individually                                   │
│                                                                                 │
│ Question: "Testing strategy?"                                                  │
│ Answer: ✅ AI-ENHANCED - 85% unit, 70% integration, 60% E2E                  │
│                                                                                 │
│ Question: "Success metrics?"                                                   │
│ Answer: ✅ 320% productivity gain, 3.2 month payback                          │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Implementation Guidelines

### Using This Decision Tree
1. **Start with Team Assessment**: Determine size, experience, and budget
2. **Follow Sequential Decisions**: Each decision builds on previous choices
3. **Consider Risk Tolerance**: Choose implementation approach based on organizational risk appetite
4. **Plan for Scaling**: Make decisions that support future growth
5. **Monitor and Adjust**: Use feedback loops to refine decisions over time

### Decision Documentation
- **Record Reasoning**: Document why each decision was made
- **Track Outcomes**: Monitor results of decisions for future reference
- **Adjust as Needed**: Be prepared to modify decisions based on new information
- **Share Knowledge**: Ensure team understands decision rationale

---

## Diagram Creation Notes

When creating visual decision trees:

1. **Use Clear Branching**: Show decision points with distinct branches
2. **Include Criteria**: Specify decision criteria at each branch point
3. **Show Outcomes**: Display results/consequences of each decision path
4. **Use Consistent Colors**: Different colors for different decision types
5. **Include Recommendations**: Highlight preferred paths with visual indicators

**Color Coding Suggestions**:
- 🟦 Blue: Decision Points
- 🟩 Green: Recommended Paths
- 🟨 Yellow: Caution/Consider Carefully
- 🟧 Orange: Alternative Options
- 🟥 Red: Not Recommended

This decision tree provides a comprehensive guide for making informed choices throughout the AI-SDLC implementation process, ensuring optimal outcomes based on specific team and organizational contexts.