# Engineering Practices Guide - AI-Enhanced SDLC

## Overview

This guide covers the essential engineering practices for implementing AI-enhanced software development lifecycle workflows, focusing on automated quality gates, testing procedures, and deployment practices requested by the Head of Engineering.

**Target Audience**: Development Team (All Roles)  
**Implementation Timeline**: Weeks 1-6 (integrated with main setup)  
**Dependencies**: Phase 1 tool setup must be completed first

---

## Table of Contents

1. [Local Pre-Commit Hooks - Fail Fast Strategy](#1-local-pre-commit-hooks---fail-fast-strategy)
2. [Post-Commit Test Execution](#2-post-commit-test-execution)
3. [Pre-Merge Validation Workflows](#3-pre-merge-validation-workflows)
4. [Post-Merge and Ephemeral Environments](#4-post-merge-and-ephemeral-environments)
5. [UAT Environment Fast-Forward](#5-uat-environment-fast-forward)
6. [Production Environment Fast-Forward](#6-production-environment-fast-forward)

---

## 1. Local Pre-Commit Hooks - Fail Fast Strategy

### Philosophy

**Fail Fast Principle**: Catch issues on developer machines before they reach CI/CD or team members. This approach saves time, reduces context switching, and maintains development flow.

**Benefits**:
- Immediate feedback loop (< 30 seconds)
- Prevents broken code from entering shared branches
- Reduces CI/CD pipeline load and costs
- Maintains team velocity by preventing blocking issues

### Implementation

#### 1.1 Husky Setup (Head of Engineering)

```bash
# Install husky for git hooks management
pnpm add -D husky

# Initialize husky
npx husky init

# Add prepare script to package.json
npm pkg set scripts.prepare="husky install"
```

#### 1.2 Pre-Commit Hook Configuration

Create `.husky/pre-commit` with fail-fast checks:

```bash
#!/bin/sh
# .husky/pre-commit

echo "🔍 Running pre-commit checks..."

# Stage 1: Quick syntax and formatting checks (< 10 seconds)
echo "1/4 Checking code formatting..."
pnpm lint-staged || {
  echo "❌ Formatting issues found. Run 'pnpm format' to fix."
  exit 1
}

# Stage 2: Type checking (< 20 seconds)
echo "2/4 Type checking..."
pnpm type-check || {
  echo "❌ Type errors found. Fix TypeScript issues before committing."
  exit 1
}

# Stage 3: Unit tests for changed files (< 30 seconds)
echo "3/4 Running unit tests..."
pnpm test:changed || {
  echo "❌ Unit tests failed. Fix failing tests before committing."
  exit 1
}

# Stage 4: Security scan (< 15 seconds)
echo "4/4 Security scan..."
pnpm audit --audit-level=moderate || {
  echo "❌ Security vulnerabilities found. Review and fix before committing."
  exit 1
}

echo "✅ All pre-commit checks passed!"
```

#### 1.3 Lint-Staged Configuration

Add to `package.json`:

```json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "eslint --fix",
      "prettier --write",
      "vitest related --run"
    ],
    "*.{json,md,yaml,yml}": [
      "prettier --write"
    ],
    "*.{css,scss}": [
      "prettier --write"
    ]
  }
}
```

#### 1.4 Team-Specific Hooks

**Frontend Developer Additional Checks**:
```bash
# Add to pre-commit hook
echo "Frontend: Checking component tests..."
pnpm test:components --changed || exit 1

echo "Frontend: Validating accessibility..."
pnpm a11y:check || exit 1
```

**Backend Developer Additional Checks**:
```bash
# Add to pre-commit hook
echo "Backend: API schema validation..."
pnpm validate:api || exit 1

echo "Backend: Database migration check..."
pnpm migration:validate || exit 1
```

### 1.5 Performance Optimization

**Incremental Checks**: Only run tests for changed files
**Parallel Execution**: Run compatible checks simultaneously
**Caching**: Cache results for unchanged files
**Bypass Option**: Emergency bypass with `--no-verify` (discouraged)

### 1.6 Team Onboarding

**Setup Script** (run during Phase 1E):
```bash
# setup-git-hooks.sh
#!/bin/bash
echo "Setting up pre-commit hooks..."

# Install dependencies
pnpm install

# Setup husky
npx husky install

# Make hooks executable
chmod +x .husky/pre-commit

# Test hooks
echo "Testing pre-commit hooks..."
git add README.md
git commit -m "test: pre-commit hooks" --dry-run

echo "✅ Pre-commit hooks setup complete!"
```

---

## 2. Post-Commit Test Execution

### Execution Location: GitHub Actions

All post-commit tests run in GitHub Actions CI/CD pipeline to ensure consistent environment and resource management.

### 2.1 Post-Commit Workflow

**File**: `.github/workflows/post-commit.yml`

```yaml
name: Post-Commit Tests

on:
  push:
    branches: [main, develop, feature/*]

jobs:
  comprehensive-tests:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'
      
      - name: Install dependencies
        run: pnpm install --frozen-lockfile
      
      # Full test suite (not just changed files)
      - name: Run comprehensive unit tests
        run: |
          pnpm test:unit --coverage
          pnpm test:integration --coverage
      
      # Component and E2E tests
      - name: Run component tests
        run: pnpm test:components --coverage
      
      - name: Run E2E tests
        run: pnpm test:e2e --headless
      
      # Performance and security validation
      - name: Performance testing
        run: pnpm lighthouse:ci
      
      - name: Security audit
        run: pnpm audit --audit-level=high
      
      # AI-assisted code analysis
      - name: AI code review
        run: pnpm ai:review --commit=${{ github.sha }}
      
      # Upload coverage reports
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage/coverage-final.json
```

### 2.2 Test Execution Strategy

**Parallel Execution**: Run test categories in parallel to reduce total time
**Smart Caching**: Cache dependencies and test results between runs
**Fail Fast**: Stop pipeline on first critical failure
**Detailed Reporting**: Generate comprehensive test reports

### 2.3 Notification System

**Success Notifications**: Brief summary to team channel
**Failure Notifications**: Detailed failure report with fix suggestions
**Performance Alerts**: Notify when performance thresholds are exceeded

---

## 3. Pre-Merge Validation Workflows

### Execution Location: GitHub Actions (Pull Request Checks)

All pre-merge validations run as required status checks that must pass before merge is allowed.

### 3.1 Pre-Merge Workflow

**File**: `.github/workflows/pre-merge.yml`

```yaml
name: Pre-Merge Validation

on:
  pull_request:
    types: [opened, synchronize, reopened]
    branches: [main, develop]

jobs:
  validation:
    runs-on: ubuntu-latest
    timeout-minutes: 45
    
    steps:
      - name: Checkout PR
        uses: actions/checkout@v4
        with:
          ref: ${{ github.head_ref }}
          fetch-depth: 0
      
      - name: Setup environment
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'
      
      - name: Install dependencies
        run: pnpm install --frozen-lockfile
      
      # Code quality validation
      - name: Lint and format check
        run: |
          pnpm lint --max-warnings=0
          pnpm format:check
      
      # Comprehensive testing
      - name: Run full test suite
        run: |
          pnpm test:unit --coverage
          pnpm test:integration --coverage
          pnpm test:e2e --coverage
      
      # Architecture and dependency validation
      - name: Validate architecture
        run: pnpm validate:architecture
      
      - name: Check for dependency updates
        run: pnpm audit --audit-level=moderate
      
      # Performance regression testing
      - name: Performance regression test
        run: pnpm lighthouse:ci --assert
      
      # AI-assisted code review
      - name: AI code review
        run: pnpm ai:review --pr=${{ github.event.number }}
      
      # Security validation
      - name: Security scan
        run: |
          pnpm audit --audit-level=high
          pnpm security:scan
      
      # Database migration validation (if applicable)
      - name: Validate migrations
        run: pnpm migration:validate
        if: contains(github.head_ref, 'migration') || contains(github.head_ref, 'database')
```

### 3.2 Branch Protection Rules

**Required Status Checks**:
- Pre-merge validation must pass
- Code coverage must be > 90%
- Performance budgets must be met
- Security scans must pass
- AI code review must approve

**Additional Requirements**:
- At least 1 human reviewer approval
- Up-to-date with base branch
- No merge commits allowed (squash and merge)

### 3.3 AI-Enhanced Validation

**Claude Code Max Integration**:
- Automated code review comments
- Architecture compliance checking
- Security vulnerability analysis
- Performance optimization suggestions
- Test coverage gap identification

---

## 4. Post-Merge and Ephemeral Environments

### Execution Location: Railway + Vercel + Neon

Post-merge deployments create ephemeral environments for each feature branch using our infrastructure stack.

### 4.1 Post-Merge Deployment

**File**: `.github/workflows/post-merge.yml`

```yaml
name: Post-Merge Deployment

on:
  push:
    branches: [main, develop]
  pull_request:
    types: [opened, synchronize]

jobs:
  deploy-ephemeral:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'
      
      - name: Install dependencies
        run: pnpm install --frozen-lockfile
      
      # Create Neon database branch
      - name: Create database branch
        run: |
          neon branches create --name=pr-${{ github.event.number }} \
            --parent=main \
            --project-id=${{ secrets.NEON_PROJECT_ID }}
          echo "DB_BRANCH_URL=$(neon connection-string --branch=pr-${{ github.event.number }})" >> $GITHUB_ENV
      
      # Deploy backend to Railway
      - name: Deploy backend to Railway
        run: |
          railway up --service=api-pr-${{ github.event.number }} \
            --environment=staging \
            --variables DATABASE_URL=${{ env.DB_BRANCH_URL }}
          echo "API_URL=$(railway domain --service=api-pr-${{ github.event.number }})" >> $GITHUB_ENV
      
      # Deploy frontend to Vercel
      - name: Deploy frontend to Vercel
        run: |
          vercel --prod --token=${{ secrets.VERCEL_TOKEN }} \
            --env NEXT_PUBLIC_API_URL=${{ env.API_URL }} \
            --env NEXT_PUBLIC_BRANCH=pr-${{ github.event.number }}
          echo "FRONTEND_URL=$(vercel --prod --token=${{ secrets.VERCEL_TOKEN }} --output url)" >> $GITHUB_ENV
      
      # Run smoke tests on deployed environment
      - name: Smoke tests
        run: |
          pnpm test:smoke --base-url=${{ env.FRONTEND_URL }}
          pnpm test:api --base-url=${{ env.API_URL }}
      
      # Comment on PR with environment URLs
      - name: Comment deployment URLs
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '🚀 **Ephemeral Environment Deployed**\n\n' +
                    `🌐 **Frontend**: ${{ env.FRONTEND_URL }}\n` +
                    `🔗 **API**: ${{ env.API_URL }}\n` +
                    `🗄️ **Database**: Branch pr-${{ github.event.number }}\n\n` +
                    '✅ Smoke tests passed\n' +
                    '⏱️ Environment will be cleaned up when PR is closed'
```

### 4.2 Environment Cleanup

**File**: `.github/workflows/cleanup-ephemeral.yml`

```yaml
name: Cleanup Ephemeral Environments

on:
  pull_request:
    types: [closed]

jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - name: Cleanup Railway deployment
        run: |
          railway down --service=api-pr-${{ github.event.number }} \
            --environment=staging
      
      - name: Cleanup Vercel deployment
        run: |
          vercel rm --yes --token=${{ secrets.VERCEL_TOKEN }} \
            pr-${{ github.event.number }}
      
      - name: Cleanup Neon database branch
        run: |
          neon branches delete --name=pr-${{ github.event.number }} \
            --project-id=${{ secrets.NEON_PROJECT_ID }}
```

### 4.3 Environment Monitoring

**Automated Health Checks**:
- Frontend application loads successfully
- API endpoints respond correctly
- Database connections are functional
- Authentication systems work
- Core user journeys complete

**Performance Validation**:
- Lighthouse CI runs on ephemeral environments
- Performance budgets validated
- Core Web Vitals measured
- API response times monitored

---

## 5. UAT Environment Fast-Forward

### Environment: Dedicated UAT Infrastructure

UAT environment runs on dedicated infrastructure separate from ephemeral environments, providing stable testing environment for stakeholders.

### 5.1 UAT Deployment Strategy

**Fast-Forward Approach**: Direct deployment from develop branch to UAT with comprehensive validation.

**File**: `.github/workflows/uat-deployment.yml`

```yaml
name: UAT Environment Fast-Forward

on:
  push:
    branches: [develop]
  workflow_dispatch:
    inputs:
      branch:
        description: 'Branch to deploy to UAT'
        required: true
        default: 'develop'

jobs:
  deploy-uat:
    runs-on: ubuntu-latest
    environment: uat
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          ref: ${{ github.event.inputs.branch || 'develop' }}
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'
      
      - name: Install dependencies
        run: pnpm install --frozen-lockfile
      
      # Pre-deployment validation
      - name: Run comprehensive test suite
        run: |
          pnpm test:unit --coverage
          pnpm test:integration --coverage
          pnpm test:e2e --coverage
      
      - name: Build applications
        run: pnpm build
      
      # Deploy to UAT infrastructure
      - name: Deploy to UAT Railway
        run: |
          railway up --service=maritime-uat-api \
            --environment=uat \
            --variables DATABASE_URL=${{ secrets.UAT_DATABASE_URL }}
      
      - name: Deploy to UAT Vercel
        run: |
          vercel --prod --token=${{ secrets.VERCEL_TOKEN }} \
            --env NEXT_PUBLIC_API_URL=${{ secrets.UAT_API_URL }} \
            --env NEXT_PUBLIC_ENVIRONMENT=uat
      
      # UAT-specific validation
      - name: UAT smoke tests
        run: |
          pnpm test:uat --base-url=${{ secrets.UAT_FRONTEND_URL }}
          pnpm test:api:uat --base-url=${{ secrets.UAT_API_URL }}
      
      # Data migration and seeding
      - name: Run UAT data migration
        run: |
          pnpm migration:run --environment=uat
          pnpm seed:uat
      
      # Performance validation
      - name: UAT performance test
        run: pnpm lighthouse:ci --url=${{ secrets.UAT_FRONTEND_URL }}
      
      # Notify stakeholders
      - name: Notify UAT deployment
        run: |
          curl -X POST ${{ secrets.TEAMS_WEBHOOK_URL }} \
            -H 'Content-Type: application/json' \
            -d '{
              "title": "UAT Environment Updated",
              "text": "Maritime Insurance App UAT environment has been updated with latest changes from develop branch.",
              "sections": [{
                "facts": [
                  {"name": "Environment", "value": "UAT"},
                  {"name": "Branch", "value": "${{ github.event.inputs.branch || 'develop' }}"},
                  {"name": "URL", "value": "${{ secrets.UAT_FRONTEND_URL }}"},
                  {"name": "Status", "value": "✅ Ready for Testing"}
                ]
              }]
            }'
```

### 5.2 UAT Environment Tests

**Comprehensive Test Suite**:
- All unit and integration tests
- Complete E2E test coverage
- Performance validation
- Security scanning
- Accessibility compliance testing

**UAT-Specific Tests**:
- Stakeholder user journeys
- Business process validation
- Data integrity checks
- Third-party integrations
- Backup and recovery procedures

### 5.3 UAT Validation Checklist

**Pre-Deployment**:
- [ ] All tests passing in develop branch
- [ ] Security scan completed
- [ ] Performance benchmarks met
- [ ] Database migrations validated

**Post-Deployment**:
- [ ] Application loads successfully
- [ ] All core features functional
- [ ] Performance meets requirements
- [ ] Security measures active
- [ ] Monitoring and logging operational

**Stakeholder Notification**:
- [ ] Product Owner notified
- [ ] UAT environment URL shared
- [ ] Test scenarios provided
- [ ] Feedback collection process active

---

## 6. Production Environment Fast-Forward

### Environment: Production Infrastructure

Production deployments follow a carefully orchestrated process with comprehensive validation and rollback capabilities.

### 6.1 Production Deployment Strategy

**Fast-Forward Approach**: Direct deployment from main branch to production with full validation and monitoring.

**File**: `.github/workflows/production-deployment.yml`

```yaml
name: Production Fast-Forward Deployment

on:
  push:
    branches: [main]
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deployment environment'
        required: true
        default: 'production'
        type: choice
        options:
          - production
          - production-hotfix

jobs:
  deploy-production:
    runs-on: ubuntu-latest
    environment: production
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          ref: main
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'
      
      - name: Install dependencies
        run: pnpm install --frozen-lockfile
      
      # Pre-deployment validation
      - name: Production readiness check
        run: |
          pnpm test:unit --coverage
          pnpm test:integration --coverage
          pnpm test:e2e --coverage
          pnpm test:performance
          pnpm security:scan
      
      # Database backup and migration
      - name: Backup production database
        run: |
          neon backup create --project-id=${{ secrets.NEON_PROJECT_ID }} \
            --name="pre-deploy-$(date +%Y%m%d-%H%M%S)"
      
      - name: Run production migrations
        run: |
          pnpm migration:run --environment=production
      
      # Blue-green deployment
      - name: Deploy to production (blue-green)
        run: |
          # Deploy to green environment
          railway up --service=maritime-prod-api-green \
            --environment=production \
            --variables DATABASE_URL=${{ secrets.PROD_DATABASE_URL }}
          
          vercel --prod --token=${{ secrets.VERCEL_TOKEN }} \
            --env NEXT_PUBLIC_API_URL=${{ secrets.PROD_API_URL_GREEN }} \
            --env NEXT_PUBLIC_ENVIRONMENT=production
      
      # Production validation
      - name: Production smoke tests
        run: |
          pnpm test:prod --base-url=${{ secrets.PROD_FRONTEND_URL_GREEN }}
          pnpm test:api:prod --base-url=${{ secrets.PROD_API_URL_GREEN }}
      
      # Switch traffic to green environment
      - name: Switch production traffic
        run: |
          # Update load balancer to point to green environment
          railway environment switch --service=maritime-prod-api \
            --from=blue --to=green
      
      # Post-deployment monitoring
      - name: Monitor production deployment
        run: |
          # Monitor for 10 minutes
          timeout 600 pnpm monitor:production || {
            echo "Production monitoring failed, initiating rollback"
            railway environment switch --service=maritime-prod-api \
              --from=green --to=blue
            exit 1
          }
      
      # Cleanup blue environment
      - name: Cleanup blue environment
        run: |
          railway down --service=maritime-prod-api-blue \
            --environment=production
      
      # Notify team
      - name: Notify production deployment
        run: |
          curl -X POST ${{ secrets.TEAMS_WEBHOOK_URL }} \
            -H 'Content-Type: application/json' \
            -d '{
              "title": "🚀 Production Deployment Successful",
              "text": "Maritime Insurance App has been successfully deployed to production.",
              "sections": [{
                "facts": [
                  {"name": "Environment", "value": "Production"},
                  {"name": "Branch", "value": "main"},
                  {"name": "Deployment", "value": "Blue-Green"},
                  {"name": "Status", "value": "✅ Live"}
                ]
              }]
            }'
```

### 6.2 Production Checks Before Deployment

**Automated Quality Gates**:
- [ ] All CI/CD pipeline checks pass
- [ ] Code coverage > 90%
- [ ] Security scan passes
- [ ] Performance benchmarks met
- [ ] Database migrations validated
- [ ] Backup created successfully

**Manual Approval Gates**:
- [ ] Head of Engineering approval
- [ ] Security team approval (if required)
- [ ] Product Owner sign-off
- [ ] Change management approval

### 6.3 Production Monitoring and Rollback

**Real-Time Monitoring**:
- Application performance metrics
- Error rates and exception tracking
- Database performance and connections
- API response times
- User experience metrics

**Automatic Rollback Triggers**:
- Error rate > 1%
- Response time > 2 seconds
- Database connection failures
- Critical feature failures
- Performance degradation > 20%

**Manual Rollback Process**:
```bash
# Emergency rollback command
railway environment switch --service=maritime-prod-api \
  --from=green --to=blue

# Verify rollback
pnpm test:prod --base-url=${{ secrets.PROD_FRONTEND_URL }}
```

### 6.4 Post-Production Validation

**Immediate Checks** (0-15 minutes):
- [ ] Application loads successfully
- [ ] Critical user journeys work
- [ ] Database connections stable
- [ ] API endpoints responding
- [ ] Error rates within normal limits

**Extended Monitoring** (15 minutes - 24 hours):
- [ ] Performance metrics stable
- [ ] User activity patterns normal
- [ ] No critical errors reported
- [ ] Third-party integrations working
- [ ] Business KPIs maintained

**Success Criteria**:
- Zero critical errors for 24 hours
- Performance metrics within acceptable ranges
- User satisfaction maintained
- All business processes operational

---

## Implementation Timeline

### Week 1: Foundation Setup
- **Day 1-2**: Pre-commit hooks implementation
- **Day 3-4**: Post-commit test workflows
- **Day 5**: Team training on git hooks

### Week 2: CI/CD Integration
- **Day 1-2**: Pre-merge validation workflows
- **Day 3-4**: Ephemeral environment setup
- **Day 5**: UAT environment configuration

### Week 3: Production Readiness
- **Day 1-3**: Production deployment workflows
- **Day 4-5**: Monitoring and rollback procedures

### Week 4: Team Training
- **Day 1-2**: Engineering practices training
- **Day 3-4**: Hands-on practice with workflows
- **Day 5**: Validation and certification

---

## Success Metrics

### Development Velocity
- **Pre-commit feedback**: < 30 seconds
- **CI/CD pipeline duration**: < 15 minutes
- **Deployment frequency**: Multiple per day
- **Lead time**: < 1 day (feature to production)

### Quality Metrics
- **Production defect rate**: < 0.1%
- **Rollback frequency**: < 1% of deployments
- **Test coverage**: > 90%
- **Security scan pass rate**: 100%

### Team Productivity
- **Developer satisfaction**: > 85%
- **Time to onboard new developer**: < 2 days
- **Context switching reduction**: 50%
- **Feedback loop time**: < 5 minutes

---

## Troubleshooting Guide

### Common Issues

**Pre-commit hooks failing**:
```bash
# Check hook permissions
chmod +x .husky/pre-commit

# Reset hooks
npx husky install
```

**CI/CD pipeline failures**:
```bash
# Check GitHub Actions logs
gh run view --log

# Re-run failed jobs
gh run rerun
```

**Deployment failures**:
```bash
# Check Railway logs
railway logs --service=maritime-prod-api

# Check Vercel logs
vercel logs --follow
```

**Database migration issues**:
```bash
# Rollback migration
neon migration rollback --project-id=$PROJECT_ID

# Validate migration
neon migration validate --project-id=$PROJECT_ID
```

This comprehensive engineering practices guide ensures that all critical development workflows are properly implemented with AI-enhanced automation, providing the foundation for efficient and reliable software development.