# Phase 3 Workflow Guide - Daily SDLC Procedures

## Overview

This guide provides comprehensive daily procedures and workflows for implementing the 6-stage AI-enhanced SDLC workflow. Each section includes step-by-step procedures, team responsibilities, quality gates, and specific commands to ensure smooth operations.

---

## 1. Daily SDLC Procedures

### Morning Standup Workflow (15 minutes)

**Time**: 9:00 AM Daily  
**Platform**: Microsoft Teams  
**Participants**: Full Team

#### Procedure:
1. **Review Previous Day's Progress** (5 min)
   - Check completed tasks in JIRA via Claude Code Max
   - Review any overnight CI/CD failures
   - Identify blockers from previous day

2. **Current Day Planning** (8 min)
   - Each team member shares:
     - Current task status
     - Today's priorities
     - Any blockers or dependencies
   - Claude Code Max integration check

3. **Quick Metrics Review** (2 min)
   ```bash
   # Check performance metrics
   lighthouse-ci healthcheck
   
   # Review error rates
   sentry stats --period=24h
   ```

### Daily Code Review Sessions

**Time**: 2:00 PM - 3:00 PM  
**Frequency**: Daily  
**Tool**: GitHub + Claude Code Max

#### AI-Assisted Review Process:
1. **Pre-Review with Claude Code Max**
   ```bash
   # Run AI code review
   claude-code review --pr <PR_NUMBER>
   
   # Check for security issues
   claude-code security-scan --branch <BRANCH_NAME>
   ```

2. **Human Review Focus Areas**
   - Business logic correctness
   - Architecture decisions
   - Performance implications
   - User experience impact

3. **Review Checklist**
   - [ ] AI review passed
   - [ ] Tests passing (Vitest/Playwright)
   - [ ] Coverage maintained (>90%)
   - [ ] Performance budget met
   - [ ] Documentation updated

---

## 2. Stage-by-Stage Workflows

### Stage 1: Business Ideation & Requirements (1-2 days)

**Participants**: Product Owner + Head of Engineering + Lead Frontend + Lead Backend  
**Primary Tool**: Claude Code Max with JIRA MCP

#### Day 1: Requirements Gathering

**9:00 AM - Initial Requirements Session**
1. Product Owner presents business need in natural language
2. Team discusses feasibility and clarifications
3. Claude Code Max captures and analyzes requirements

**10:30 AM - AI-Powered Analysis**
```bash
# Analyze requirements completeness
claude-code analyze-requirements --input requirements.md

# Generate technical specifications
claude-code generate-spec --requirements requirements.md --output tech-spec.md

# Create JIRA tickets automatically
claude-code create-tickets --spec tech-spec.md --project MARINE
```

**2:00 PM - Technical Feasibility Review**
1. Review AI-generated technical specifications
2. Identify technical risks and dependencies
3. Estimate development effort

**Quality Gates:**
- [ ] Requirements completeness score >85%
- [ ] All acceptance criteria defined
- [ ] Technical feasibility confirmed
- [ ] Effort estimates approved

#### Day 2: Finalization and Planning

**9:00 AM - Cost and Timeline Estimation**
```bash
# Generate cost estimates
claude-code estimate --spec tech-spec.md --team-velocity 40

# Create implementation roadmap
claude-code roadmap --spec tech-spec.md --sprint-length 2w
```

**11:00 AM - Stakeholder Approval**
- Present estimates and timeline
- Get formal approval to proceed
- Update JIRA with approved scope

**Deliverables:**
- Approved requirements document
- Technical specification
- JIRA epic and stories
- Cost and timeline estimates

### Stage 2: Design & Architecture (2-3 days)

**Participants**: UI/UX Engineer + Lead Frontend + Head of Engineering  
**Primary Tools**: Figma Professional + Gemini CLI

#### Day 1: UI/UX Design Creation

**9:00 AM - Design Kickoff**
1. Review approved requirements
2. Identify key user flows
3. Set design constraints and guidelines

**10:00 AM - Figma Design Work**
```bash
# Initialize design system check
figma-cli check-tokens --design-system maritime-ds

# Export design tokens
figma-cli export-tokens --file <FIGMA_FILE_ID> --output tokens.json
```

**2:00 PM - Component Specification**
1. Document each component's:
   - Props and state
   - Interaction patterns
   - Responsive behavior
   - Accessibility requirements

#### Day 2: Technical Architecture

**9:00 AM - Architecture Planning**
```bash
# Generate architecture diagram
claude-code architect --requirements tech-spec.md --style microservices

# Analyze architecture decisions
claude-code analyze-architecture --input architecture.md
```

**11:00 AM - Design Review Session**
- Walkthrough of Figma designs
- Technical feasibility check
- Performance impact assessment

**Quality Gates:**
- [ ] Design system compliance verified
- [ ] Accessibility score >95
- [ ] Component specifications complete
- [ ] Architecture approved by Head of Engineering

#### Day 3: Design-to-Code Preparation

**9:00 AM - Design Handoff**
```bash
# Generate React components from Figma
gemini generate-components --figma <FILE_ID> --output ./src/components

# Create Storybook stories
claude-code generate-stories --components ./src/components
```

**Deliverables:**
- Completed Figma designs
- Component specification docs
- Technical architecture diagram
- Generated component scaffolds

### Stage 3: Development Planning (0.5-1 day)

**Participants**: Full team  
**Primary Tools**: Claude Code Max + JIRA

#### Sprint Planning Session (4 hours)

**9:00 AM - Capacity Planning**
```bash
# Check team capacity
claude-code capacity --sprint next --team marine-dev

# Analyze velocity trends
claude-code velocity --sprints 6 --format chart
```

**9:30 AM - Story Breakdown**
1. Review design and architecture outputs
2. Break down epics into sprint-sized stories
3. Identify technical tasks

**10:30 AM - Task Assignment**
```bash
# AI-assisted task assignment based on skills
claude-code assign-tasks --sprint next --optimize-for skills

# Check for dependency conflicts
claude-code check-dependencies --sprint next
```

**11:30 AM - Sprint Goal Definition**
- Define clear, measurable sprint goal
- Ensure alignment with release objectives
- Set success criteria

**Quality Gates:**
- [ ] All stories have clear acceptance criteria
- [ ] No blocking dependencies identified
- [ ] Team capacity not exceeded
- [ ] Sprint goal approved

**Deliverables:**
- Sprint backlog in JIRA
- Task assignments completed
- Sprint goal documented
- Dependency map created

### Stage 4: Implementation (1-2 week sprints)

**Participants**: All developers  
**Primary Tools**: Claude Code Max + Cursor IDE + Git

#### Daily Development Workflow

**9:00 AM - Daily Standup** (see Daily Procedures)

**9:15 AM - Development Work Begins**

##### Frontend Development Flow
```bash
# Start new feature branch
git checkout -b feature/MARINE-123-vessel-form

# Open in Cursor IDE with AI assistance
cursor .

# Generate component with Claude Code Max
claude-code generate-component --type form --name VesselRegistration

# Run tests in watch mode
npm run test:watch
```

##### Backend Development Flow
```bash
# Create API endpoint with Claude
claude-code generate-api --spec ./specs/vessel-api.yaml --framework fastapi

# Generate database migrations
claude-code generate-migration --model Vessel --action create

# Run API tests
pytest tests/api/test_vessel.py --cov
```

**Throughout the Day - Continuous Integration**
```bash
# Pre-commit checks
pre-commit run --all-files

# Push changes
git push origin feature/MARINE-123-vessel-form

# Monitor CI/CD pipeline
gh workflow view
```

**4:00 PM - Daily Progress Update**
```bash
# Update JIRA automatically
claude-code update-ticket --ticket MARINE-123 --status "In Progress" --comment "Completed form validation logic"

# Generate daily report
claude-code daily-report --developer @me
```

#### Code Quality Checkpoints

**Before Each Commit:**
1. Run local tests: `npm test`
2. Check linting: `npm run lint`
3. Verify types: `npm run type-check`
4. Review with Claude: `claude-code review --staged`

**Before Pull Request:**
```bash
# Comprehensive quality check
npm run quality:check

# Performance check
lighthouse-ci collect --url http://localhost:3000

# Security scan
claude-code security-scan --deep
```

**Quality Gates:**
- [ ] All tests passing
- [ ] Code coverage >90%
- [ ] No linting errors
- [ ] Performance budget met
- [ ] Security scan passed

### Stage 5: Testing & Quality Assurance (Continuous)

**Participants**: All developers + AI automation  
**Primary Tools**: Claude Code Max + Vitest + Playwright

#### Automated Testing Workflow

**Unit Testing (Continuous)**
```bash
# Generate test cases with AI
claude-code generate-tests --file ./src/components/VesselForm.tsx

# Run tests with coverage
npm run test:coverage

# Update snapshots if needed
npm run test:update
```

**Integration Testing (Daily)**
```bash
# Run API integration tests
npm run test:api

# Test database operations
npm run test:db

# Verify third-party integrations
npm run test:integrations
```

**E2E Testing (Per Feature)**
```bash
# Generate E2E tests
claude-code generate-e2e --user-flow vessel-registration

# Run Playwright tests
npm run test:e2e

# Run cross-browser tests
npm run test:e2e:all-browsers
```

#### Manual Testing Procedures

**Feature Testing Checklist:**
1. **Functional Testing**
   - [ ] All acceptance criteria met
   - [ ] Edge cases handled
   - [ ] Error states properly displayed

2. **Cross-browser Testing**
   - [ ] Chrome/Edge
   - [ ] Firefox
   - [ ] Safari
   - [ ] Mobile browsers

3. **Performance Testing**
   ```bash
   # Run performance audit
   lighthouse http://localhost:3000/vessel-registration --view
   
   # Load testing
   artillery run load-test.yml
   ```

**Quality Gates:**
- [ ] Unit test coverage >90%
- [ ] All E2E tests passing
- [ ] Performance score >90
- [ ] No critical accessibility issues
- [ ] Security vulnerabilities resolved

### Stage 6: Deployment & Monitoring (1-2 hours)

**Participants**: Lead Backend + DevOps automation  
**Primary Tools**: GitHub Actions + Vercel + Sentry

#### Pre-Deployment Checklist

**T-2 hours: Final Checks**
```bash
# Verify all tests passing
gh workflow view test --branch main

# Check dependency vulnerabilities
npm audit

# Review deployment configuration
claude-code review-deployment --env production
```

**T-1 hour: Deployment Preparation**
```bash
# Create release notes
claude-code generate-release-notes --version v1.2.0

# Tag release
git tag -a v1.2.0 -m "Release v1.2.0: Fleet Management Module"
git push origin v1.2.0

# Trigger deployment workflow
gh workflow run deploy.yml --ref v1.2.0
```

#### Deployment Process

**Staged Rollout (Automated)**
1. **Stage 1: Canary (5%)**
   ```bash
   # Monitor canary metrics
   sentry releases --org maritime --project frontend deploys v1.2.0 --environment canary
   ```

2. **Stage 2: Partial (25%)**
   - Monitor for 30 minutes
   - Check error rates
   - Verify performance metrics

3. **Stage 3: Full Deployment**
   ```bash
   # Complete rollout
   vercel promote <DEPLOYMENT_ID> --prod
   ```

#### Post-Deployment Monitoring

**First Hour Monitoring**
```bash
# Real-time error monitoring
sentry monitor v1.2.0 --real-time

# Performance monitoring
lighthouse-ci assert --preset lighthouse:recommended

# User feedback collection
claude-code collect-feedback --version v1.2.0
```

**Quality Gates:**
- [ ] Error rate <0.1%
- [ ] Performance metrics stable
- [ ] No critical user reports
- [ ] All monitoring systems green

---

## 3. Team Collaboration Patterns

### Role-Specific Workflows

#### Head of Engineering

**Daily Responsibilities:**
1. **Morning (9:00 AM - 10:00 AM)**
   - Review overnight alerts
   - Check team capacity
   - Prioritize critical issues

2. **Midday (2:00 PM - 3:00 PM)**
   - Participate in code reviews
   - Architecture decision making
   - Unblock team members

3. **End of Day (5:00 PM - 5:30 PM)**
   - Review daily progress
   - Update stakeholders
   - Plan next day priorities

**Key Commands:**
```bash
# Team performance dashboard
claude-code team-metrics --period week

# Architecture review
claude-code review-architecture --changes last-24h

# Generate executive summary
claude-code executive-summary --date today
```

#### Lead Frontend Developer

**Daily Workflow:**
1. **Development (60% of time)**
   ```bash
   # Component development
   cursor --ai-mode max
   
   # Real-time collaboration
   cursor --live-share <SESSION_ID>
   ```

2. **Code Review (20% of time)**
   - Review React components
   - Verify Figma compliance
   - Performance optimization

3. **Mentoring (20% of time)**
   - Pair programming sessions
   - Knowledge sharing
   - Best practices enforcement

#### Lead Backend Developer

**Daily Focus Areas:**
1. **API Development**
   ```bash
   # Generate API endpoint
   claude-code api --generate endpoint --spec openapi.yaml
   
   # Database optimization
   claude-code db-optimize --analyze slow-queries
   ```

2. **System Integration**
   - Third-party service integration
   - Database performance tuning
   - Security implementation

3. **Infrastructure**
   - Monitor system health
   - Optimize deployments
   - Capacity planning

### Handoff Procedures

#### Design to Development Handoff

**Checklist:**
- [ ] Figma designs finalized and approved
- [ ] Component specifications documented
- [ ] Design tokens exported
- [ ] Interactive prototype available
- [ ] Accessibility requirements defined

**Handoff Meeting Agenda (30 min):**
1. Design walkthrough (10 min)
2. Technical clarifications (10 min)
3. Implementation approach (10 min)

#### Development to QA Handoff

**Automated Handoff Process:**
```bash
# Generate QA package
claude-code qa-package --pr <PR_NUMBER> --output qa-docs/

# Package includes:
# - Feature documentation
# - Test scenarios
# - Known limitations
# - Performance benchmarks
```

#### Sprint to Sprint Handoff

**Sprint Retrospective (1 hour):**
1. What went well (15 min)
2. What could improve (15 min)
3. Action items (15 min)
4. Next sprint preview (15 min)

**Knowledge Transfer:**
```bash
# Generate sprint summary
claude-code sprint-summary --sprint current --format markdown

# Update documentation
claude-code update-docs --changes sprint-23
```

---

## 4. Quality Assurance Procedures

### Continuous Quality Monitoring

#### Automated Quality Gates

**Pre-Commit Hooks:**
```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: eslint
        name: ESLint
        entry: npm run lint:fix
        language: system
        files: \.(js|jsx|ts|tsx)$
        
      - id: prettier
        name: Prettier
        entry: npm run format
        language: system
        files: \.(js|jsx|ts|tsx|css|scss|json|md)$
        
      - id: type-check
        name: TypeScript
        entry: npm run type-check
        language: system
        pass_filenames: false
```

**CI/CD Pipeline Checks:**
```yaml
# GitHub Actions workflow
name: Quality Assurance
on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
        
      - name: Install dependencies
        run: npm ci
        
      - name: Run tests
        run: npm run test:ci
        
      - name: Check coverage
        run: npm run coverage:check
        
      - name: Lighthouse CI
        run: lhci autorun
        
      - name: Security scan
        run: npm audit --production
```

### Testing Workflows

#### Test-Driven Development (TDD) with AI

**Step 1: Write Tests First**
```bash
# Generate test skeleton
claude-code generate-test --component VesselForm --type unit

# Add test cases
claude-code suggest-tests --component VesselForm --coverage edge-cases
```

**Step 2: Implement Feature**
```bash
# Generate implementation
claude-code implement --test vessel-form.test.tsx

# Verify tests pass
npm run test vessel-form.test.tsx
```

**Step 3: Refactor**
```bash
# AI-assisted refactoring
claude-code refactor --file VesselForm.tsx --optimize performance

# Ensure tests still pass
npm run test
```

#### Cross-Browser Testing with Playwright

**Daily Cross-Browser Check:**
```bash
# Morning browser check (9:30 AM)
npm run test:e2e:all

# Specific browser testing
npm run test:e2e -- --project=webkit
npm run test:e2e -- --project=firefox
```

**Visual Regression Testing:**
```bash
# Capture baseline screenshots
npm run test:visual:update

# Run visual regression tests
npm run test:visual

# Review differences
npm run test:visual:report
```

### Performance Monitoring with Lighthouse CI

#### Daily Performance Checks

**Morning Performance Audit (9:15 AM):**
```bash
# Run performance audit
lighthouse-ci collect --numberOfRuns=3

# Check against budgets
lighthouse-ci assert

# View trends
lighthouse-ci open
```

**Performance Optimization Workflow:**
1. **Identify Issues**
   ```bash
   # Generate performance report
   claude-code performance-analyze --url /fleet-management
   ```

2. **Implement Fixes**
   ```bash
   # Optimize bundle size
   npm run build:analyze
   
   # Apply optimizations
   claude-code optimize --target bundle-size
   ```

3. **Verify Improvements**
   ```bash
   # Re-run audit
   lighthouse-ci collect --url http://localhost:3000/fleet-management
   ```

### Error Tracking with Sentry

#### Real-Time Error Monitoring

**Error Response Workflow:**
1. **Alert Received** (via Slack/Email)
   ```bash
   # View error details
   sentry issues <ISSUE_ID>
   
   # Check error frequency
   sentry issues stats <ISSUE_ID> --period 24h
   ```

2. **Investigate Root Cause**
   ```bash
   # View breadcrumbs and stack trace
   sentry events <EVENT_ID> --full
   
   # Check user impact
   sentry issues users <ISSUE_ID>
   ```

3. **Deploy Fix**
   ```bash
   # Create hotfix branch
   git checkout -b hotfix/SENTRY-<ISSUE_ID>
   
   # Deploy fix
   gh workflow run hotfix.yml --ref hotfix/SENTRY-<ISSUE_ID>
   ```

**Daily Error Review (4:30 PM):**
```bash
# Generate daily error report
claude-code error-report --date today --severity high

# Update error tracking dashboard
sentry projects stats maritime-frontend --period 24h
```

---

## 5. Troubleshooting Common Workflow Issues

### Issue: Slow CI/CD Pipeline

**Symptoms:**
- Builds taking >10 minutes
- Frequent timeouts
- Developer frustration

**Resolution:**
```bash
# Analyze pipeline performance
gh workflow view --id <WORKFLOW_ID> --verbose

# Optimize parallelization
# Update .github/workflows/ci.yml
jobs:
  test:
    strategy:
      matrix:
        test-suite: [unit, integration, e2e]
    steps:
      - run: npm run test:${{ matrix.test-suite }}
```

### Issue: Flaky E2E Tests

**Symptoms:**
- Random test failures
- Works locally but fails in CI
- Inconsistent results

**Resolution:**
```javascript
// Add proper wait conditions
await page.waitForLoadState('networkidle');
await expect(page.locator('#vessel-form')).toBeVisible();

// Increase timeout for slow operations
await page.click('#submit', { timeout: 10000 });

// Add retry logic
test.describe('Vessel Registration', () => {
  test.describe.configure({ retries: 2 });
  // tests...
});
```

### Issue: Performance Regression

**Symptoms:**
- Lighthouse score drops
- User complaints about speed
- Increased load times

**Resolution:**
```bash
# Identify regression point
git bisect start
git bisect bad HEAD
git bisect good v1.1.0

# Analyze bundle size
npm run build:analyze

# Find large dependencies
npm ls --depth=0 | grep -E "[0-9]+\.[0-9]+MB"

# Implement code splitting
claude-code optimize --strategy code-splitting --routes /fleet-management
```

### Issue: Merge Conflicts in Concurrent Development

**Symptoms:**
- Frequent merge conflicts
- Delayed pull requests
- Team coordination issues

**Resolution:**
```bash
# Use feature flags for parallel development
claude-code feature-flag --create vessel-redesign

# Implement trunk-based development
git checkout main
git pull origin main
git checkout -b feature/MARINE-456
# Make small, frequent commits

# Use AI to resolve conflicts
claude-code resolve-conflicts --strategy theirs-for-generated
```

### Issue: Claude Code Max Rate Limiting

**Symptoms:**
- "Rate limit exceeded" errors
- Slow AI responses
- Blocked development

**Resolution:**
```bash
# Check current usage
claude-code usage --period today

# Implement request batching
claude-code batch --commands "
  generate-component --name VesselList
  generate-test --component VesselList
  generate-story --component VesselList
"

# Use local caching
claude-code config --enable-cache --cache-ttl 3600
```

---

## 6. Metrics and Success Tracking

### Daily Metrics Collection

**Automated Daily Report (5:00 PM):**
```bash
# Generate comprehensive daily report
claude-code daily-metrics --team marine-dev --output daily-report.md

# Report includes:
# - Completed stories
# - Code coverage
# - Performance scores
# - Error rates
# - Deployment status
```

### Weekly Team Metrics

**Friday Review Meeting (3:00 PM):**
```bash
# Generate weekly dashboard
claude-code weekly-dashboard --format html --open

# Metrics tracked:
# - Velocity trends
# - Quality metrics
# - Performance trends
# - Team satisfaction
```

### Sprint Success Criteria

**End of Sprint Checklist:**
- [ ] Sprint goal achieved
- [ ] All committed stories completed
- [ ] Zero critical bugs
- [ ] Performance budget maintained
- [ ] Documentation updated
- [ ] Retrospective completed

---

## 7. Communication Protocols

### Synchronous Communication

**Microsoft Teams Channels:**
- `#marine-dev-general` - General discussion
- `#marine-dev-standup` - Daily standup notes
- `#marine-dev-pr` - Pull request notifications
- `#marine-dev-alerts` - System alerts and errors
- `#marine-dev-releases` - Release announcements

### Asynchronous Communication

**Notion Documentation (Experimental):**
```bash
# Update project documentation
claude-code update-notion --page "Sprint 23 Progress" --content sprint-summary.md

# Create technical decision record
claude-code create-adr --title "React Query for State Management" --notion
```

**Pull Request Communication:**
```markdown
## PR Description Template
### What does this PR do?
[Brief description]

### How to test
1. [Step 1]
2. [Step 2]

### Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] Performance impact assessed
- [ ] Security review completed
```

---

## 8. Continuous Improvement

### Weekly Retrospectives

**Format:**
1. **Metrics Review** (10 min)
   - Velocity achieved vs. planned
   - Quality metrics
   - Team satisfaction

2. **Discussion** (35 min)
   - What went well?
   - What could improve?
   - Action items

3. **Planning** (15 min)
   - Implement improvements
   - Assign owners
   - Set deadlines

### Monthly Process Review

**First Monday of Month:**
```bash
# Generate process metrics
claude-code process-metrics --period month

# Analyze bottlenecks
claude-code analyze-workflow --identify bottlenecks

# Generate improvement suggestions
claude-code suggest-improvements --based-on metrics
```

---

## Conclusion

This workflow guide provides the foundation for implementing an efficient, AI-enhanced SDLC process. Regular adherence to these procedures, combined with continuous improvement based on metrics and team feedback, will ensure successful project delivery and team satisfaction.

Remember: The workflow should adapt to your team's needs. Use these procedures as a starting point and refine based on your specific context and requirements.