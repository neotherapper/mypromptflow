# Git Workflow Training Guide for Maritime Insurance Development

## Table of Contents
1. [Introduction and Learning Objectives](#introduction-and-learning-objectives)
2. [Git Workflow Overview](#git-workflow-overview)
3. [Maritime Insurance Development Workflow](#maritime-insurance-development-workflow)
4. [GitHub Integration](#github-integration)
5. [Advanced Techniques](#advanced-techniques)
6. [Best Practices](#best-practices)
7. [Hands-On Exercises](#hands-on-exercises)
8. [Competency Assessment](#competency-assessment)

---

## Introduction and Learning Objectives

### Course Overview
This comprehensive training guide provides practical, hands-on experience with Git workflows specifically tailored for maritime insurance software development. The course combines industry-standard Git practices with domain-specific requirements for insurance applications.

### Target Audience
- Junior Developers (New to Git)
- Mid-Level Developers (Familiar with basic Git)
- Senior Developers (Looking to standardize team practices)
- DevOps Engineers (Implementing CI/CD pipelines)

### Learning Objectives
By the end of this training, participants will be able to:
1. **Implement** feature branch workflows with proper protection rules
2. **Execute** maritime insurance-specific development workflows
3. **Configure** GitHub Actions for CI/CD in insurance applications
4. **Resolve** complex merge conflicts and implement hotfix procedures
5. **Apply** security best practices for sensitive insurance data
6. **Collaborate** effectively using pull requests and code reviews

### Prerequisites
- Basic command line familiarity
- Understanding of version control concepts
- Access to a GitHub account
- Local Git installation (2.30+)

---

## Git Workflow Overview

### 1. Branch Protection Rules and Strategy

#### Core Concepts
Branch protection rules ensure code quality and prevent unauthorized changes to critical branches.

#### Protection Strategy for Maritime Insurance Applications

```yaml
# Branch Protection Configuration
main:
  protection_rules:
    - require_pull_request_reviews:
        required_approving_review_count: 2
        dismiss_stale_reviews: true
        require_code_owner_reviews: true
    - require_status_checks:
        strict: true
        contexts:
          - continuous-integration/insurance-compliance
          - security/data-protection-scan
          - test/unit-tests
          - test/integration-tests
    - enforce_admins: false
    - restrictions:
        users: []
        teams: ["insurance-platform-leads"]
    - require_linear_history: true
    - require_conversation_resolution: true

staging:
  protection_rules:
    - require_pull_request_reviews:
        required_approving_review_count: 1
    - require_status_checks:
        contexts:
          - continuous-integration/build
          - test/unit-tests

develop:
  protection_rules:
    - require_status_checks:
        contexts:
          - continuous-integration/build
```

### 2. Feature Branch Workflow

#### Workflow Diagram
```
main
  └── develop
       └── feature/marine-quote-calculator
       └── feature/policy-renewal-engine
       └── feature/claims-processing-api
```

#### Step-by-Step Process

1. **Create Feature Branch**
   ```bash
   # Always branch from develop
   git checkout develop
   git pull origin develop
   git checkout -b feature/marine-cargo-rating-engine
   ```

2. **Development Cycle**
   ```bash
   # Regular commits with meaningful messages
   git add src/rating-engine/cargo-calculator.js
   git commit -m "feat(rating): implement cargo value calculation for marine policies"
   
   # Push to remote regularly
   git push -u origin feature/marine-cargo-rating-engine
   ```

3. **Keep Branch Updated**
   ```bash
   # Daily rebase from develop
   git fetch origin
   git rebase origin/develop
   ```

### 3. Code Review Processes

#### Review Checklist for Maritime Insurance Code

```markdown
## Code Review Checklist

### Business Logic
- [ ] Premium calculations follow underwriting guidelines
- [ ] Policy validation rules are correctly implemented
- [ ] Compliance with maritime insurance regulations
- [ ] Proper handling of currency conversions

### Security
- [ ] No hardcoded API keys or credentials
- [ ] Sensitive data (SSN, policy details) properly encrypted
- [ ] SQL injection prevention measures in place
- [ ] Input validation for all user data

### Performance
- [ ] Database queries optimized for large policy datasets
- [ ] Caching implemented for rate tables
- [ ] Bulk operations properly batched

### Testing
- [ ] Unit tests cover all calculation methods
- [ ] Integration tests verify API endpoints
- [ ] Edge cases tested (null values, extreme amounts)
- [ ] Performance tests for high-volume scenarios

### Documentation
- [ ] API documentation updated
- [ ] Business logic explained in comments
- [ ] README updated with new features
```

### 4. Merge vs Rebase Strategies

#### When to Use Each Strategy

**Merge Strategy** - Use for:
- Feature branches with multiple developers
- Preserving complete development history
- Public branches shared across teams

```bash
# Merge example for feature completion
git checkout develop
git merge --no-ff feature/marine-quote-calculator
```

**Rebase Strategy** - Use for:
- Personal feature branches
- Cleaning up commit history before merge
- Keeping linear history in main branches

```bash
# Rebase example for clean history
git checkout feature/policy-renewal-engine
git rebase -i develop
# Squash related commits, reword messages
```

---

## Maritime Insurance Development Workflow

### 1. Branch Naming Conventions

#### Standard Format
```
<type>/<ticket-number>-<brief-description>

Types:
- feature/   New functionality
- bugfix/    Bug fixes
- hotfix/    Emergency production fixes
- release/   Release preparation
- chore/     Maintenance tasks
```

#### Examples
```bash
feature/INS-234-marine-cargo-premium-calculator
bugfix/INS-567-policy-renewal-date-validation
hotfix/INS-890-critical-quote-generation-error
release/v2.3.0-q4-marine-products
chore/INS-123-update-rate-tables
```

### 2. Commit Message Standards

#### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

#### Types
- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, semicolons)
- **refactor**: Code refactoring
- **perf**: Performance improvements
- **test**: Test additions or corrections
- **chore**: Maintenance tasks

#### Maritime Insurance Examples
```bash
# Feature commit
git commit -m "feat(underwriting): add vessel age factor to marine hull premium calculation

- Implement age depreciation table per IMO guidelines
- Add validation for vessel build year
- Update premium calculation engine

Implements: INS-234"

# Bug fix commit
git commit -m "fix(claims): correct deductible calculation for partial loss claims

- Fix arithmetic error in pro-rata deductible calculation
- Add unit tests for edge cases
- Update claims processing documentation

Fixes: INS-567"

# Performance improvement
git commit -m "perf(quotes): optimize database queries for policy quote generation

- Add composite index on policy_type and effective_date
- Implement query result caching for rate tables
- Reduce average quote generation time by 60%

References: INS-890"
```

### 3. Pull Request Templates

#### Template File: `.github/pull_request_template.md`
```markdown
## Description
Brief description of changes and business impact

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Documentation update

## Insurance Domain Impact
- [ ] Premium Calculation
- [ ] Policy Management
- [ ] Claims Processing
- [ ] Underwriting Rules
- [ ] Regulatory Compliance
- [ ] Reporting

## Testing
- [ ] Unit tests pass locally
- [ ] Integration tests pass
- [ ] Tested with production-like data volumes
- [ ] Compliance tests pass
- [ ] Performance benchmarks met

## Checklist
- [ ] My code follows the style guidelines
- [ ] I have performed self-review
- [ ] I have commented complex business logic
- [ ] I have updated documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests covering my changes
- [ ] All new and existing tests pass
- [ ] Security scan completed

## Related Issues
Closes #INS-XXX

## Screenshots (if applicable)
Add screenshots of UI changes

## Performance Impact
Describe any performance implications

## Deployment Notes
Special instructions for deployment
```

### 4. Code Review Checklists

#### Reviewer Guidelines
```markdown
## Code Review Guidelines for Maritime Insurance

### Priority 1: Business Logic Correctness
1. Verify premium calculations against underwriting guidelines
2. Check policy validation rules match business requirements
3. Ensure compliance with maritime regulations (IMO, local laws)
4. Validate currency handling and conversions

### Priority 2: Data Integrity
1. Check for proper transaction handling
2. Verify audit trail implementation
3. Ensure proper data validation
4. Confirm error handling preserves data consistency

### Priority 3: Security
1. No sensitive data in logs
2. Proper authentication/authorization
3. Encrypted storage of PII
4. SQL injection prevention

### Priority 4: Performance
1. Efficient database queries
2. Proper indexing strategy
3. Caching where appropriate
4. Resource cleanup

### Priority 5: Maintainability
1. Clear naming conventions
2. Proper documentation
3. Testable code structure
4. No code duplication
```

---

## GitHub Integration

### 1. GitHub Actions CI/CD

#### Basic CI Pipeline for Insurance Applications
```yaml
name: Maritime Insurance CI/CD Pipeline

on:
  push:
    branches: [develop, main]
  pull_request:
    branches: [develop, main]

jobs:
  quality-checks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run linting
        run: npm run lint
      
      - name: Run type checking
        run: npm run type-check

  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run security audit
        run: npm audit --production
      
      - name: SAST scan
        uses: github/super-linter@v4
        env:
          DEFAULT_BRANCH: main
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Check for secrets
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}

  test-suite:
    runs-on: ubuntu-latest
    needs: [quality-checks]
    
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: marine_insurance_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup test environment
        run: |
          cp .env.test .env
          npm ci
      
      - name: Run unit tests
        run: npm run test:unit -- --coverage
      
      - name: Run integration tests
        run: npm run test:integration
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/marine_insurance_test
      
      - name: Run compliance tests
        run: npm run test:compliance
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info

  build-and-deploy:
    runs-on: ubuntu-latest
    needs: [test-suite, security-scan]
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Build application
        run: |
          npm ci
          npm run build
      
      - name: Deploy to staging
        if: github.ref == 'refs/heads/develop'
        run: |
          echo "Deploying to staging environment"
          # Add deployment scripts here
      
      - name: Deploy to production
        if: github.ref == 'refs/heads/main'
        run: |
          echo "Deploying to production environment"
          # Add production deployment scripts here
```

### 2. Issue Tracking and Project Management

#### Issue Templates

**Bug Report Template**: `.github/ISSUE_TEMPLATE/bug_report.md`
```markdown
---
name: Bug Report
about: Report a bug in the maritime insurance platform
title: '[BUG] '
labels: bug, triage
assignees: ''
---

## Bug Description
Clear description of the bug

## Steps to Reproduce
1. Go to '...'
2. Click on '....'
3. Enter '....'
4. See error

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Impact
- [ ] Critical - System down/Data loss
- [ ] High - Major feature broken
- [ ] Medium - Feature partially working
- [ ] Low - Minor inconvenience

## Environment
- Environment: [Production/Staging/Development]
- Browser/Version: 
- User Role: [Underwriter/Broker/Admin]
- Policy Type: [Marine Cargo/Hull/Liability]

## Screenshots
If applicable, add screenshots

## Additional Context
Any other relevant information
```

**Feature Request Template**: `.github/ISSUE_TEMPLATE/feature_request.md`
```markdown
---
name: Feature Request
about: Suggest a new feature for the maritime insurance platform
title: '[FEATURE] '
labels: enhancement, triage
assignees: ''
---

## Feature Description
Clear description of the proposed feature

## Business Value
How this feature benefits our maritime insurance operations

## User Story
As a [user type], I want [feature] so that [benefit]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Technical Considerations
Any technical constraints or considerations

## Mockups/Examples
Visual representations if applicable
```

### 3. Security Scanning Integration

#### Security Workflow
```yaml
name: Security Scanning

on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight
  pull_request:
    paths:
      - 'package*.json'
      - 'src/**'

jobs:
  dependency-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run OWASP Dependency Check
        uses: dependency-check/dependency-check-action@main
        with:
          project: 'marine-insurance-platform'
          path: '.'
          format: 'HTML'
          
      - name: Upload OWASP results
        uses: actions/upload-artifact@v3
        with:
          name: dependency-check-report
          path: reports/

  code-scanning:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Initialize CodeQL
        uses: github/codeql-action/init@v2
        with:
          languages: javascript, typescript
          
      - name: Autobuild
        uses: github/codeql-action/autobuild@v2
        
      - name: Perform CodeQL Analysis
        uses: github/codeql-action/analyze@v2

  container-scanning:
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker image
        run: docker build -t marine-insurance:${{ github.sha }} .
        
      - name: Run Trivy scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: marine-insurance:${{ github.sha }}
          format: 'sarif'
          output: 'trivy-results.sarif'
          
      - name: Upload Trivy scan results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
```

### 4. Automated Testing Workflows

#### Comprehensive Test Strategy
```yaml
name: Automated Testing Suite

on:
  pull_request:
    types: [opened, synchronize, reopened]
  push:
    branches: [develop, main]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [16.x, 18.x, 20.x]
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Use Node.js ${{ matrix.node-version }}
        uses: actions/setup-node@v3
        with:
          node-version: ${{ matrix.node-version }}
          
      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: ~/.npm
          key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
          
      - name: Install dependencies
        run: npm ci
        
      - name: Run unit tests
        run: npm run test:unit -- --coverage --maxWorkers=2
        
      - name: Generate coverage report
        run: npm run coverage:report

  integration-tests:
    runs-on: ubuntu-latest
    needs: unit-tests
    
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: testpass
          POSTGRES_DB: marine_test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
          
      redis:
        image: redis:7
        ports:
          - 6379:6379
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          
      - name: Install dependencies
        run: npm ci
        
      - name: Run database migrations
        run: npm run db:migrate:test
        env:
          DATABASE_URL: postgresql://postgres:testpass@localhost:5432/marine_test
          
      - name: Seed test data
        run: npm run db:seed:test
        env:
          DATABASE_URL: postgresql://postgres:testpass@localhost:5432/marine_test
          
      - name: Run integration tests
        run: npm run test:integration
        env:
          DATABASE_URL: postgresql://postgres:testpass@localhost:5432/marine_test
          REDIS_URL: redis://localhost:6379

  e2e-tests:
    runs-on: ubuntu-latest
    needs: integration-tests
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          
      - name: Install dependencies
        run: npm ci
        
      - name: Install Playwright
        run: npx playwright install --with-deps
        
      - name: Run E2E tests
        run: npm run test:e2e
        
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30

  performance-tests:
    runs-on: ubuntu-latest
    needs: integration-tests
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup K6
        run: |
          sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys C5AD17C747E3415A3642D57D77C6C491D6AC1D69
          echo "deb https://dl.k6.io/deb stable main" | sudo tee /etc/apt/sources.list.d/k6.list
          sudo apt-get update
          sudo apt-get install k6
          
      - name: Run performance tests
        run: k6 run tests/performance/load-test.js
        
      - name: Upload performance results
        uses: actions/upload-artifact@v3
        with:
          name: k6-report
          path: k6-report.html
```

---

## Advanced Techniques

### 1. Conflict Resolution Strategies

#### Systematic Conflict Resolution Process

**Step 1: Identify Conflicts**
```bash
# Attempting to merge feature branch
git checkout develop
git merge feature/marine-cargo-rating

# If conflicts occur, Git will show:
# Auto-merging src/rating/cargo-calculator.js
# CONFLICT (content): Merge conflict in src/rating/cargo-calculator.js
# Automatic merge failed; fix conflicts and then commit the result.
```

**Step 2: Analyze Conflicts**
```bash
# View conflict status
git status

# Examine specific conflicts
git diff --name-only --diff-filter=U

# Use mergetool for visual comparison
git mergetool
```

**Step 3: Resolve Conflicts - Maritime Insurance Example**
```javascript
// Original conflict in cargo-calculator.js
<<<<<<< HEAD
    calculatePremium(cargoValue, voyageRisk) {
        const basePremium = cargoValue * 0.002;
        const riskMultiplier = this.getRiskMultiplier(voyageRisk);
        return basePremium * riskMultiplier;
=======
    calculatePremium(cargoValue, voyageRisk, commodityType) {
        const basePremium = cargoValue * 0.0025;
        const riskFactor = this.assessRisk(voyageRisk, commodityType);
        return basePremium * riskFactor;
>>>>>>> feature/marine-cargo-rating
    }

// Resolved version combining both changes
    calculatePremium(cargoValue, voyageRisk, commodityType) {
        // Using updated rate from HEAD and new parameter from feature
        const basePremium = cargoValue * 0.002;
        const riskMultiplier = this.getRiskMultiplier(voyageRisk);
        const commodityFactor = this.getCommodityFactor(commodityType);
        return basePremium * riskMultiplier * commodityFactor;
    }
```

**Step 4: Test and Commit Resolution**
```bash
# After resolving conflicts in editor
git add src/rating/cargo-calculator.js

# Run tests to ensure resolution is correct
npm test -- src/rating/cargo-calculator.test.js

# Commit the resolution
git commit -m "merge: resolve conflicts in cargo premium calculation

- Kept base rate of 0.002 from develop branch
- Added commodity type parameter from feature branch
- Combined both risk assessment approaches"
```

### 2. Hotfix Workflows

#### Emergency Fix Process for Production Issues

**Scenario**: Critical bug in marine policy premium calculation discovered in production

**Step 1: Create Hotfix Branch**
```bash
# Branch from main (production)
git checkout main
git pull origin main
git checkout -b hotfix/INS-999-critical-premium-calculation-error

# Verify you're on the correct branch
git branch --show-current
```

**Step 2: Implement Fix**
```bash
# Make the necessary fix
vim src/premium/marine-calculator.js

# Example fix for critical calculation error
# Before: premium = baseRate * tonnage * 0.01
# After:  premium = baseRate * tonnage * 0.001  # Correct decimal place

# Test the fix thoroughly
npm run test:unit -- src/premium/marine-calculator.test.js
npm run test:integration -- --grep "premium calculation"

# Commit the fix
git add src/premium/marine-calculator.js
git commit -m "hotfix(premium): fix decimal place error in tonnage calculation

- Corrected multiplication factor from 0.01 to 0.001
- This was causing 10x overcharge on all marine cargo policies
- Added additional unit tests to prevent regression

Fixes: INS-999"
```

**Step 3: Deploy Hotfix**
```bash
# Push hotfix branch
git push -u origin hotfix/INS-999-critical-premium-calculation-error

# Create PR directly to main
# Use GitHub CLI or web interface
gh pr create --base main --title "HOTFIX: Critical premium calculation error" \
  --body "## Critical Production Fix

### Issue
Premium calculations for marine cargo policies were 10x higher than intended due to decimal place error.

### Fix
Corrected multiplication factor in tonnage calculation.

### Testing
- All unit tests pass
- Integration tests verified
- Manually tested with production data samples

### Rollback Plan
Revert this commit if any issues arise.

**This requires immediate deployment to production.**"

# After PR approval and merge to main
git checkout main
git pull origin main

# Merge hotfix back to develop
git checkout develop
git pull origin develop
git merge main
git push origin develop
```

### 3. Release Management

#### Structured Release Process

**Phase 1: Release Planning**
```bash
# Create release branch from develop
git checkout develop
git pull origin develop
git checkout -b release/v2.4.0-marine-enhancements

# Update version numbers
npm version minor  # Updates package.json version

# Update CHANGELOG
vim CHANGELOG.md
```

**CHANGELOG.md Example**:
```markdown
# Changelog

## [2.4.0] - 2024-01-15

### Added
- Marine cargo commodity-based rating engine
- Vessel age depreciation calculator
- Multi-currency support for international policies

### Changed
- Improved performance of quote generation by 60%
- Updated premium calculation to include IMO 2024 guidelines

### Fixed
- Decimal place error in tonnage calculations
- Date validation for policy effective dates
- Memory leak in bulk quote processing

### Security
- Updated dependencies to patch CVE-2024-12345
- Implemented additional input validation for API endpoints
```

**Phase 2: Release Testing**
```bash
# Run comprehensive test suite
npm run test:all

# Run performance benchmarks
npm run benchmark

# Security audit
npm audit
npm run security:scan

# Build production bundle
npm run build:production

# Test production build
npm run start:production
```

**Phase 3: Release Deployment**
```bash
# Merge to main
git checkout main
git merge --no-ff release/v2.4.0-marine-enhancements

# Tag the release
git tag -a v2.4.0 -m "Release version 2.4.0: Marine Enhancements

Major features:
- Commodity-based rating
- Vessel age calculator
- Multi-currency support

See CHANGELOG.md for full details"

# Push to remote
git push origin main
git push origin v2.4.0

# Merge back to develop
git checkout develop
git merge main
git push origin develop

# Clean up release branch
git branch -d release/v2.4.0-marine-enhancements
git push origin --delete release/v2.4.0-marine-enhancements
```

### 4. Rollback Procedures

#### Emergency Rollback Process

**Option 1: Quick Revert (Preferred for single commits)**
```bash
# Identify the problematic commit
git log --oneline -10

# Create a revert commit
git revert <commit-hash>

# Example for our premium calculation fix
git revert a1b2c3d

# This creates a new commit that undoes the changes
git push origin main
```

**Option 2: Reset to Previous Release (Nuclear option)**
```bash
# DO NOT do this on shared branches without team coordination!

# Find the last known good release
git tag -l
git checkout v2.3.0

# Create a new branch from the good state
git checkout -b emergency/rollback-from-v2.4.0

# Force update (requires admin permissions)
# This should only be done in extreme circumstances
git push --force-with-lease origin emergency/rollback-from-v2.4.0:main
```

**Option 3: Database Rollback Coordination**
```bash
# For changes involving database migrations
cd database/migrations

# Check migration status
npm run db:migration:status

# Rollback last migration
npm run db:migration:rollback

# Rollback to specific version
npm run db:migration:rollback --to-version 20240114120000
```

**Post-Rollback Actions**:
```bash
# 1. Notify team immediately
echo "EMERGENCY: Production rollback initiated for v2.4.0" | \
  slack-cli send --channel #marine-platform-alerts

# 2. Create incident report
git checkout -b incident/rollback-v2.4.0-analysis
touch docs/incidents/2024-01-15-v2.4.0-rollback.md

# 3. Document root cause
# 4. Plan forward fix
# 5. Update monitoring alerts
```

---

## Best Practices

### 1. Security Considerations

#### Protecting Sensitive Insurance Data

**Git Security Configuration**
```bash
# Global gitignore for sensitive files
cat >> ~/.gitignore_global << EOF
# Insurance-specific sensitive data
*.pem
*.key
*.p12
.env*
!.env.example
config/production.json
config/secrets.yml
data/customer_*.csv
data/policies_*.xlsx
logs/
*.log
.DS_Store
node_modules/
coverage/
EOF

git config --global core.excludesfile ~/.gitignore_global
```

**Pre-commit Hooks for Security**

Create `.githooks/pre-commit`:
```bash
#!/bin/bash

# Check for sensitive data patterns
PATTERNS=(
    "password.*=.*['\"].*['\"]"
    "api[_-]?key.*=.*['\"].*['\"]"
    "secret.*=.*['\"].*['\"]"
    "[0-9]{3}-[0-9]{2}-[0-9]{4}"  # SSN pattern
    "BEGIN (RSA|DSA|EC) PRIVATE KEY"
    "mysql://.*:.*@"
    "postgres://.*:.*@"
)

for pattern in "${PATTERNS[@]}"; do
    if git diff --cached --name-only | xargs grep -E "$pattern" 2>/dev/null; then
        echo "ERROR: Sensitive data pattern detected: $pattern"
        echo "Please remove sensitive data before committing"
        exit 1
    fi
done

# Run security scanner
npm run security:pre-commit || exit 1

exit 0
```

**Secrets Management**
```yaml
# .github/workflows/secrets-scanning.yml
name: Secret Scanning

on: [push, pull_request]

jobs:
  trufflehog:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
          
      - name: TruffleHog scan
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD
          extra_args: --debug --only-verified
```

### 2. Performance Optimization

#### Git Performance for Large Insurance Repositories

**Repository Optimization**
```bash
# Configure Git for large repositories
git config core.preloadindex true
git config core.fscache true
git config gc.auto 256

# Enable partial clone for large repos
git clone --filter=blob:none <url>

# Sparse checkout for specific components
git sparse-checkout init --cone
git sparse-checkout set src/marine-module src/shared
```

**LFS for Large Files**
```bash
# Initialize Git LFS
git lfs install

# Track large insurance data files
git lfs track "*.pdf"  # Policy documents
git lfs track "*.xlsx" # Rate tables
git lfs track "*.zip"  # Batch processing files
git lfs track "test-data/*.json" # Large test datasets

# Add .gitattributes
git add .gitattributes
git commit -m "chore: configure Git LFS for large files"
```

**Performance Monitoring**
```bash
# Create performance tracking script
cat > scripts/git-performance-check.sh << 'EOF'
#!/bin/bash

echo "Git Performance Report"
echo "====================="

# Repository size
echo "Repository size:"
du -sh .git

# Object count
echo -e "\nObject count:"
git count-objects -v

# Large files
echo -e "\nTop 10 largest files:"
git ls-tree -r -l HEAD | sort -k 4 -n -r | head -10

# Fetch time
echo -e "\nFetch time:"
time git fetch --dry-run

# Status time
echo -e "\nStatus check time:"
time git status

# Recommend optimizations
echo -e "\nRecommendations:"
if [ $(git count-objects | cut -d' ' -f1) -gt 10000 ]; then
    echo "- Run 'git gc --aggressive' to optimize repository"
fi
EOF

chmod +x scripts/git-performance-check.sh
```

### 3. Team Collaboration

#### Effective Git Collaboration Patterns

**Team Branching Guidelines**
```markdown
## Team Branching Rules

### Feature Development
1. Always branch from latest develop
2. Prefix with ticket number: feature/INS-XXX-description
3. Keep branches focused on single features
4. Delete branches after merge

### Code Ownership
CODEOWNERS file:
```
```
# Global owners
* @marine-platform-team

# Marine-specific modules
/src/marine/ @marine-underwriting-team
/src/rating/ @actuarial-team
/src/claims/ @claims-processing-team
/src/compliance/ @compliance-team

# Infrastructure
/infrastructure/ @devops-team
/.github/ @devops-team

# Documentation
/docs/ @technical-writing-team
*.md @technical-writing-team
```

**Pull Request Etiquette**
```markdown
## PR Guidelines

### For Authors
1. Keep PRs small and focused (< 400 lines changed)
2. Provide clear description and context
3. Link to relevant tickets/issues
4. Respond to feedback within 24 hours
5. Don't merge your own PRs (except hotfixes)

### For Reviewers
1. Review within 24 hours of assignment
2. Provide constructive feedback
3. Approve only when confident
4. Use suggestions for minor changes
5. Block only for critical issues

### Review Response Examples
```
```markdown
<!-- Constructive feedback -->
**Suggestion**: Consider extracting this premium calculation logic into a separate method for better testability.

<!-- Blocking issue -->
**Must Fix**: This SQL query is vulnerable to injection. Please use parameterized queries.

<!-- Minor improvement -->
**Nit**: Typo in comment: "calcualte" -> "calculate" (not blocking)

<!-- Praise good work -->
**Great work**: Excellent error handling here! This will prevent the issues we saw in production last month.
```

### 4. Documentation Standards

#### Git-Related Documentation

**README.md Template**
```markdown
# Marine Insurance Platform

## Quick Start
```bash
# Clone repository
git clone https://github.com/company/marine-insurance-platform.git

# Install dependencies
npm install

# Setup pre-commit hooks
npm run setup:hooks

# Run tests
npm test
```

## Git Workflow

### Branch Strategy
- `main`: Production-ready code
- `staging`: Pre-production testing
- `develop`: Integration branch
- `feature/*`: New features
- `bugfix/*`: Bug fixes
- `hotfix/*`: Emergency fixes

### Commit Standards
We follow [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation
- `style:` Code style
- `refactor:` Code refactoring
- `test:` Test updates
- `chore:` Maintenance

### Development Process
1. Create feature branch from develop
2. Make changes with clear commits
3. Push branch and create PR
4. Address review feedback
5. Merge after approval

## Contributing
See [CONTRIBUTING.md](./CONTRIBUTING.md) for detailed guidelines.
```

**CONTRIBUTING.md**
```markdown
# Contributing to Marine Insurance Platform

## Code of Conduct
We are committed to providing a welcoming environment. See [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md).

## How to Contribute

### Reporting Bugs
1. Check existing issues
2. Create detailed bug report
3. Include reproduction steps
4. Provide environment details

### Suggesting Features
1. Check roadmap and existing requests
2. Create feature proposal
3. Explain business value
4. Consider implementation approach

### Submitting Changes

#### Setup
```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/marine-insurance-platform.git
cd marine-insurance-platform

# Add upstream
git remote add upstream https://github.com/company/marine-insurance-platform.git

# Create branch
git checkout -b feature/INS-123-your-feature
```

#### Development
1. Write tests first (TDD)
2. Implement feature
3. Update documentation
4. Run full test suite

#### Submission
1. Push to your fork
2. Create pull request
3. Fill out PR template
4. Address review feedback

### Style Guide
- Use ESLint configuration
- Follow TypeScript strict mode
- Write self-documenting code
- Add JSDoc for public APIs

### Testing Requirements
- Unit test coverage > 80%
- Integration tests for APIs
- E2E tests for critical paths
- Performance benchmarks
```

---

## Hands-On Exercises

### Exercise 1: Feature Branch Workflow (Beginner)

**Objective**: Create and merge a feature branch for a new marine cargo calculator.

**Setup**:
```bash
# Clone training repository
git clone https://github.com/training/marine-insurance-exercises.git
cd marine-insurance-exercises

# Checkout develop branch
git checkout develop
```

**Tasks**:
1. Create feature branch: `feature/cargo-value-calculator`
2. Implement calculator function in `src/calculators/cargo.js`
3. Add unit tests in `src/calculators/cargo.test.js`
4. Commit changes with proper message format
5. Push branch and create pull request
6. Address review comments (provided by instructor)
7. Merge to develop after approval

**Success Criteria**:
- Branch follows naming convention
- At least 3 meaningful commits
- All tests pass
- PR description complete
- Code review addressed

### Exercise 2: Conflict Resolution (Intermediate)

**Objective**: Resolve merge conflicts in premium calculation logic.

**Setup**:
```bash
# Two conflicting branches are pre-created
git checkout feature/premium-calculator-a
git merge feature/premium-calculator-b
```

**Conflict to Resolve**:
```javascript
<<<<<<< HEAD
    calculateMarinePremium(value, riskFactor) {
        const base = value * 0.002;
        return base * riskFactor;
=======
    calculateMarinePremium(value, riskFactor, vesselAge) {
        const base = value * 0.0025;
        const ageFactor = this.getAgeFactor(vesselAge);
        return base * riskFactor * ageFactor;
>>>>>>> feature/premium-calculator-b
    }
```

**Tasks**:
1. Analyze both implementations
2. Resolve conflict keeping both features
3. Ensure tests pass after resolution
4. Commit with descriptive message
5. Document resolution decision

**Success Criteria**:
- Conflict resolved correctly
- Both features preserved
- Tests pass
- Clear commit message explaining resolution

### Exercise 3: Hotfix Deployment (Advanced)

**Objective**: Deploy emergency fix for production calculation error.

**Scenario**: Production reports show marine liability premiums are being undercharged by 50% due to a decimal error.

**Tasks**:
1. Create hotfix branch from main
2. Identify and fix the calculation error
3. Add regression test
4. Fast-track through abbreviated review
5. Deploy to production
6. Merge back to develop and main
7. Create incident report

**Provided Code with Bug**:
```javascript
// Current production code with bug
calculateLiabilityPremium(coverageAmount, riskCategory) {
    const baseRate = riskCategory === 'high' ? 0.0002 : 0.0001; // BUG: Should be 0.002 and 0.001
    return coverageAmount * baseRate;
}
```

**Success Criteria**:
- Hotfix branch created from main
- Bug fixed with test
- Proper commit message
- Successfully merged to both main and develop
- Incident report created

### Exercise 4: Release Management (Advanced)

**Objective**: Prepare and deploy quarterly release with multiple features.

**Features to Include**:
1. New vessel classification system
2. Updated premium calculations
3. API rate limiting implementation
4. Performance optimizations

**Tasks**:
1. Create release branch from develop
2. Update version numbers
3. Generate changelog from commits
4. Run full regression suite
5. Create release notes
6. Deploy to staging
7. Get stakeholder approval
8. Merge to main and tag
9. Deploy to production
10. Merge back to develop

**Success Criteria**:
- Clean release branch
- Comprehensive changelog
- All tests pass
- Proper version tagging
- Successful deployment
- Post-release cleanup

### Exercise 5: CI/CD Pipeline Creation (Expert)

**Objective**: Build complete CI/CD pipeline for marine module.

**Requirements**:
- Automated testing on PR
- Security scanning
- Performance benchmarks
- Automated deployment
- Rollback capability

**Tasks**:
1. Create `.github/workflows/marine-ci.yml`
2. Configure test stages
3. Add security scanning
4. Implement performance gates
5. Setup deployment stages
6. Add rollback workflow
7. Document pipeline

**Success Criteria**:
- Pipeline runs on PR creation
- All quality gates enforced
- Deployment automation works
- Rollback tested successfully
- Documentation complete

---

## Competency Assessment

### Assessment Framework

#### Level 1: Git Fundamentals (Junior Developer)

**Knowledge Requirements**:
- Basic Git commands
- Branch creation and switching
- Commit creation
- Push/pull operations
- Basic merge operations

**Practical Assessment**:
1. **Task**: Implement a simple feature
   - Create feature branch
   - Make 3 meaningful commits
   - Push to remote
   - Create PR

2. **Evaluation Criteria**:
   - Correct branch naming (10%)
   - Meaningful commit messages (20%)
   - Clean commit history (20%)
   - PR properly formatted (25%)
   - Code review addressed (25%)

**Passing Score**: 70%

#### Level 2: Collaborative Development (Mid-Level Developer)

**Knowledge Requirements**:
- Conflict resolution
- Code review best practices
- Git flow understanding
- Basic CI/CD concepts
- Security awareness

**Practical Assessment**:
1. **Task**: Complex feature with conflicts
   - Implement feature requiring multiple commits
   - Resolve merge conflicts
   - Perform code review
   - Address security concerns

2. **Evaluation Criteria**:
   - Conflict resolution accuracy (20%)
   - Code review quality (20%)
   - Security practices (20%)
   - Documentation (20%)
   - Collaboration effectiveness (20%)

**Passing Score**: 75%

#### Level 3: Advanced Git Operations (Senior Developer)

**Knowledge Requirements**:
- Release management
- Hotfix procedures
- Advanced Git commands
- CI/CD pipeline design
- Performance optimization

**Practical Assessment**:
1. **Task**: Release preparation and hotfix
   - Prepare release with 5+ features
   - Execute hotfix procedure
   - Optimize repository performance
   - Design CI/CD improvements

2. **Evaluation Criteria**:
   - Release process execution (25%)
   - Hotfix handling (25%)
   - Performance optimization (20%)
   - CI/CD design (20%)
   - Documentation quality (10%)

**Passing Score**: 80%

#### Level 4: Git Architecture (Lead/Architect)

**Knowledge Requirements**:
- Repository strategy design
- Branching model customization
- Security architecture
- Performance at scale
- Team process optimization

**Practical Assessment**:
1. **Task**: Design complete Git workflow
   - Design branching strategy for 50+ developers
   - Create security guidelines
   - Design CI/CD architecture
   - Create team onboarding process

2. **Evaluation Criteria**:
   - Strategy completeness (30%)
   - Security considerations (25%)
   - Scalability design (25%)
   - Team enablement (20%)

**Passing Score**: 85%

### Certification Requirements

#### Git Workflow Certification - Maritime Insurance Platform

**Prerequisites**:
- Complete all training modules
- Pass written exam (80%)
- Complete practical assessment
- Peer review approval

**Certification Levels**:
1. **Certified Practitioner**: Levels 1-2 completed
2. **Certified Professional**: Levels 1-3 completed
3. **Certified Expert**: All levels completed

**Maintenance Requirements**:
- Annual recertification
- Continuous learning credits
- Project contributions
- Knowledge sharing sessions

### Assessment Tools and Resources

#### Self-Assessment Checklist

```markdown
## Git Workflow Self-Assessment

### Basic Skills
- [ ] I can create and switch branches
- [ ] I can write meaningful commit messages
- [ ] I can push and pull from remote
- [ ] I can create pull requests
- [ ] I can resolve simple conflicts

### Intermediate Skills
- [ ] I can rebase branches effectively
- [ ] I can use interactive rebase
- [ ] I can perform code reviews
- [ ] I can setup Git hooks
- [ ] I can troubleshoot Git issues

### Advanced Skills
- [ ] I can design branching strategies
- [ ] I can optimize repository performance
- [ ] I can implement CI/CD pipelines
- [ ] I can handle complex merges
- [ ] I can train others on Git

### Expert Skills
- [ ] I can architect Git workflows for large teams
- [ ] I can implement security best practices
- [ ] I can design disaster recovery procedures
- [ ] I can optimize Git for enterprise scale
- [ ] I can customize Git for specific needs
```

#### Practice Resources

1. **Git Simulator**: Interactive exercises
2. **Sample Repository**: Pre-configured with exercises
3. **Video Tutorials**: Step-by-step walkthroughs
4. **Mentorship Program**: Pairing with experienced developers
5. **Documentation Library**: Comprehensive reference materials

### Continuous Improvement

#### Quarterly Skills Review

**Process**:
1. Self-assessment against framework
2. Peer feedback collection
3. Manager evaluation
4. Skills gap analysis
5. Training plan creation

**Metrics to Track**:
- PR turnaround time
- Merge conflict resolution time
- Code review quality scores
- Pipeline failure rates
- Security incident count

#### Team Maturity Model

**Level 1: Ad-hoc**
- Inconsistent practices
- Manual processes
- Frequent conflicts
- Limited automation

**Level 2: Managed**
- Documented workflows
- Basic automation
- Regular code reviews
- Consistent branching

**Level 3: Defined**
- Standardized processes
- Comprehensive automation
- Proactive reviews
- Measured metrics

**Level 4: Optimized**
- Continuous improvement
- Full automation
- Predictive analytics
- Self-healing processes

**Level 5: Innovative**
- Industry leadership
- Custom tooling
- Research contributions
- Training others

---

## Conclusion

This comprehensive Git workflow training guide provides the foundation for effective version control in maritime insurance software development. Regular practice with the exercises and continuous assessment will build proficiency and confidence in Git operations.

Remember that mastering Git is a journey, not a destination. The maritime insurance industry's unique requirements for security, compliance, and reliability make these skills essential for every developer on the team.

### Next Steps

1. Complete self-assessment
2. Start with exercises matching your level
3. Practice daily with real projects
4. Seek feedback from peers
5. Share knowledge with team members

### Additional Resources

- [Official Git Documentation](https://git-scm.com/doc)
- [GitHub Learning Lab](https://lab.github.com/)
- [Atlassian Git Tutorials](https://www.atlassian.com/git/tutorials)
- Internal Wiki: `wiki/git-best-practices`
- Team Slack Channel: `#git-help`

---

**Document Version**: 1.0  
**Last Updated**: January 2024  
**Maintained By**: Maritime Insurance Platform Team  
**Review Cycle**: Quarterly