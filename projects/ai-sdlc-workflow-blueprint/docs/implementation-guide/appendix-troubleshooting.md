# Appendix: Comprehensive Troubleshooting Guide

## Overview

This guide provides solutions for common issues encountered while implementing the AI-assisted SDLC workflow for the maritime insurance application. Each section includes symptoms, root causes, solutions, and prevention strategies.

---

## 1. Common Setup Issues

### 1.1 Tool Installation and Configuration Problems

#### 1.1.1 Claude Code Max Connection Issues

**Symptoms:**
- "Failed to connect to MCP server" error
- Claude Code Max not recognizing JIRA or GitHub integration
- Timeout errors when accessing repositories

**Root Causes:**
- Incorrect API credentials
- Network firewall blocking MCP connections
- Expired authentication tokens

**Solutions:**
1. Verify MCP server configuration:
   ```bash
   claude-code-max --check-config
   ```
2. Regenerate API tokens in GitHub Settings → Developer Settings → Personal Access Tokens
3. Update firewall rules to allow outbound connections on ports 443 and 8080
4. Clear Claude Code Max cache: `~/.claude/cache/`

**Prevention:**
- Document all API endpoints and required ports
- Set up token rotation reminders (90-day cycle)
- Test connections during off-peak hours

#### 1.1.2 GitPod Environment Startup Failures

**Symptoms:**
- "Workspace failed to start" error
- Stuck at "Initializing workspace" for >5 minutes
- Missing dependencies after workspace starts

**Root Causes:**
- Incorrect `.gitpod.yml` configuration
- Docker image build failures
- Insufficient GitPod resource allocation

**Solutions:**
1. Validate `.gitpod.yml` syntax:
   ```yaml
   # Correct format
   image: gitpod/workspace-full:latest
   tasks:
     - init: |
         pnpm install
         pnpm run setup
   ```
2. Check GitPod status page: https://www.gitpodstatus.com/
3. Increase workspace resources in GitPod settings (minimum 4 cores, 8GB RAM)

**Prevention:**
- Test `.gitpod.yml` changes in a separate branch
- Pin Docker image versions instead of using `latest`
- Monitor GitPod usage dashboard for resource constraints

### 1.2 Environment Setup Failures

#### 1.2.1 Neon Database Connection Errors

**Symptoms:**
- "FATAL: password authentication failed" error
- "Connection to server lost" during queries
- Slow query performance on cold starts

**Root Causes:**
- Incorrect connection string format
- Database branch not activated
- Serverless timeout on idle connections

**Solutions:**
1. Verify connection string format:
   ```
   postgresql://[user]:[password]@[endpoint]/[database]?sslmode=require
   ```
2. Activate database branch via Neon CLI:
   ```bash
   neon branches activate feature-branch
   ```
3. Implement connection pooling with proper retry logic

**Prevention:**
- Use environment variables for all connection strings
- Configure connection pool with minimum 5 connections
- Set appropriate timeout values (30s for serverless)

#### 1.2.2 pnpm Installation Issues

**Symptoms:**
- "pnpm: command not found" error
- Package installation hanging indefinitely
- Workspace conflicts with npm/yarn

**Root Causes:**
- pnpm not installed globally
- Conflicting package manager lock files
- Corrupted pnpm store

**Solutions:**
1. Install pnpm globally:
   ```bash
   npm install -g pnpm
   ```
2. Remove conflicting lock files:
   ```bash
   rm -f package-lock.json yarn.lock
   ```
3. Clear pnpm store and reinstall:
   ```bash
   pnpm store prune
   pnpm install --force
   ```

**Prevention:**
- Include pnpm installation in GitPod configuration
- Add npm/yarn lock files to `.gitignore`
- Document pnpm version requirements

### 1.3 Authentication and Access Issues

#### 1.3.1 GitHub Team Access Problems

**Symptoms:**
- "Permission denied" when pushing to repository
- Unable to trigger GitHub Actions workflows
- Missing access to team repositories

**Root Causes:**
- User not added to GitHub organization
- Incorrect repository permissions
- SSH key not configured

**Solutions:**
1. Verify organization membership:
   ```bash
   gh api /orgs/{org}/memberships/{username}
   ```
2. Configure SSH key:
   ```bash
   ssh-keygen -t ed25519 -C "email@example.com"
   gh ssh-key add ~/.ssh/id_ed25519.pub
   ```
3. Request admin to update repository permissions

**Prevention:**
- Document onboarding checklist with access requirements
- Use GitHub team sync for automatic access management
- Regular access audits (quarterly)

#### 1.3.2 Microsoft Teams Integration Failures

**Symptoms:**
- GitHub notifications not appearing in Teams
- Unable to access Teams channels from IDE
- Authentication loops when connecting services

**Root Causes:**
- Expired OAuth tokens
- Incorrect webhook URLs
- Azure AD permission restrictions

**Solutions:**
1. Regenerate Teams webhook URL
2. Update Azure AD app permissions:
   - Navigate to Azure Portal → App registrations
   - Add required Graph API permissions
3. Clear Teams cache: `%appdata%\Microsoft\Teams\`

**Prevention:**
- Document all integration endpoints
- Set up monitoring for webhook failures
- Regular token refresh (30-day cycle)

### 1.4 Infrastructure Deployment Problems

#### 1.4.1 Railway Deployment Failures

**Symptoms:**
- "Build failed" errors during deployment
- Application crashes after successful deployment
- Environment variables not loading

**Root Causes:**
- Missing buildpack configuration
- Incorrect Procfile syntax
- Environment variable naming conflicts

**Solutions:**
1. Verify Procfile format:
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
2. Check Railway build logs for specific errors
3. Ensure all environment variables are set in Railway dashboard

**Prevention:**
- Test deployments in staging environment first
- Use Railway templates for initial setup
- Version control all configuration files

#### 1.4.2 Vercel Build Errors

**Symptoms:**
- "Module not found" errors during build
- Build timeout after 45 minutes
- Deployment succeeds but site shows 404

**Root Causes:**
- Incorrect build command configuration
- Missing environment variables
- Output directory misconfiguration

**Solutions:**
1. Update `vercel.json`:
   ```json
   {
     "buildCommand": "pnpm run build",
     "outputDirectory": ".next",
     "framework": "nextjs"
   }
   ```
2. Set all required environment variables in Vercel dashboard
3. Clear build cache and redeploy

**Prevention:**
- Use Vercel CLI for local testing
- Document all required environment variables
- Monitor build performance metrics

---

## 2. Development Issues

### 2.1 IDE and Editor Configuration Problems

#### 2.1.1 Cursor IDE AI Features Not Working

**Symptoms:**
- No AI suggestions appearing
- "Rate limit exceeded" errors
- Cursor crashing when opening large files

**Root Causes:**
- Free plan API limits reached
- Incorrect API key configuration
- Memory limitations with large codebases

**Solutions:**
1. Check API usage: Settings → AI → Usage Statistics
2. Reduce context window size for large files
3. Disable unnecessary AI features to conserve API calls

**Prevention:**
- Monitor daily API usage
- Configure file size limits for AI analysis
- Use Gemini CLI for large file analysis

#### 2.1.2 VS Code Extension Conflicts

**Symptoms:**
- ESLint not highlighting errors
- Prettier not formatting on save
- Git integration showing incorrect status

**Root Causes:**
- Conflicting formatter extensions
- Outdated extension versions
- Workspace settings overriding user settings

**Solutions:**
1. Disable conflicting extensions
2. Update workspace settings:
   ```json
   {
     "editor.defaultFormatter": "esbenp.prettier-vscode",
     "editor.formatOnSave": true,
     "eslint.validate": ["javascript", "typescript", "typescriptreact"]
   }
   ```
3. Clear VS Code extension cache

**Prevention:**
- Maintain approved extension list
- Use workspace recommended extensions
- Regular extension updates (monthly)

### 2.2 Build and Compilation Errors

#### 2.2.1 TypeScript Compilation Failures

**Symptoms:**
- "Cannot find module" errors
- Type definition conflicts
- Build succeeds locally but fails in CI

**Root Causes:**
- Missing type definitions
- Incorrect tsconfig.json paths
- Version mismatches between local and CI

**Solutions:**
1. Install missing types:
   ```bash
   pnpm add -D @types/node @types/react
   ```
2. Verify tsconfig.json paths:
   ```json
   {
     "compilerOptions": {
       "baseUrl": ".",
       "paths": {
         "@/*": ["src/*"]
       }
     }
   }
   ```
3. Lock TypeScript version in package.json

**Prevention:**
- Use strict TypeScript configuration
- Regular dependency updates
- Consistent Node.js versions across environments

#### 2.2.2 Next.js Build Optimization Issues

**Symptoms:**
- Build times exceeding 10 minutes
- "JavaScript heap out of memory" errors
- Large bundle sizes (>1MB)

**Root Causes:**
- Unoptimized imports
- Missing dynamic imports
- Incorrect webpack configuration

**Solutions:**
1. Implement code splitting:
   ```javascript
   const HeavyComponent = dynamic(() => import('./HeavyComponent'), {
     loading: () => <p>Loading...</p>,
   });
   ```
2. Analyze bundle size:
   ```bash
   pnpm run build && pnpm run analyze
   ```
3. Increase Node.js memory limit:
   ```bash
   NODE_OPTIONS="--max-old-space-size=4096" pnpm run build
   ```

**Prevention:**
- Regular bundle size monitoring
- Implement performance budgets
- Use Lighthouse CI for automated checks

### 2.3 Testing Framework Issues

#### 2.3.1 Vitest Test Failures

**Symptoms:**
- Tests passing locally but failing in CI
- "Cannot find module" in test files
- Timeout errors on async tests

**Root Causes:**
- Different timezone settings
- Missing test environment setup
- Incorrect async test patterns

**Solutions:**
1. Set consistent timezone:
   ```javascript
   // vitest.config.ts
   export default {
     test: {
       env: {
         TZ: 'UTC'
       }
     }
   }
   ```
2. Configure module aliases for tests
3. Increase test timeout for async operations

**Prevention:**
- Use consistent test data
- Mock external dependencies
- Document test environment requirements

#### 2.3.2 Playwright E2E Test Instability

**Symptoms:**
- Flaky tests with intermittent failures
- "Element not found" errors
- Different results across browsers

**Root Causes:**
- Race conditions in UI interactions
- Hardcoded wait times
- Browser-specific implementations

**Solutions:**
1. Use proper wait strategies:
   ```javascript
   await page.waitForSelector('.loading', { state: 'hidden' });
   await expect(page.locator('.result')).toBeVisible();
   ```
2. Implement retry logic for flaky operations
3. Use browser-specific test conditions when necessary

**Prevention:**
- Avoid hardcoded waits
- Use data-testid attributes
- Regular test maintenance

### 2.4 CI/CD Pipeline Failures

#### 2.4.1 GitHub Actions Workflow Errors

**Symptoms:**
- "Resource not accessible by integration" errors
- Workflows not triggering on events
- Artifact upload failures

**Root Causes:**
- Insufficient repository permissions
- Incorrect workflow syntax
- GitHub API rate limits

**Solutions:**
1. Verify GITHUB_TOKEN permissions:
   ```yaml
   permissions:
     contents: read
     pull-requests: write
     actions: read
   ```
2. Validate workflow syntax using GitHub's online validator
3. Implement exponential backoff for API calls

**Prevention:**
- Use workflow templates
- Test workflows in separate branch
- Monitor GitHub Actions usage

#### 2.4.2 Deployment Pipeline Failures

**Symptoms:**
- Deployments stuck in pending state
- Health checks failing after deployment
- Rollback failures

**Root Causes:**
- Insufficient startup time allowance
- Missing health check endpoints
- Database migration failures

**Solutions:**
1. Implement proper health checks:
   ```python
   @app.get("/health")
   async def health_check():
       return {"status": "healthy", "timestamp": datetime.now()}
   ```
2. Increase deployment timeout settings
3. Separate migration jobs from deployment

**Prevention:**
- Implement comprehensive health checks
- Use blue-green deployment strategy
- Test rollback procedures regularly

---

## 3. Production Issues

### 3.1 Deployment Failures

#### 3.1.1 Zero-Downtime Deployment Issues

**Symptoms:**
- Users experiencing 502/503 errors during deployment
- Database connection drops during migration
- Session data loss after deployment

**Root Causes:**
- Improper load balancer configuration
- Long-running database migrations
- Incompatible session storage

**Solutions:**
1. Configure Railway for zero-downtime deployments:
   ```toml
   [deploy]
   healthcheckPath = "/health"
   healthcheckTimeout = 30
   ```
2. Run migrations separately from deployment
3. Use Redis for session storage

**Prevention:**
- Implement database migration testing
- Use feature flags for gradual rollouts
- Monitor deployment metrics

#### 3.1.2 Environment Variable Misconfigurations

**Symptoms:**
- "undefined is not a function" errors
- API calls failing with 401 errors
- Features working in staging but not production

**Root Causes:**
- Missing production environment variables
- Incorrect variable naming
- Build-time vs runtime variables confusion

**Solutions:**
1. Audit all environment variables:
   ```bash
   # List all required variables
   grep -r "process.env" src/ | grep -o "process.env.[A-Z_]*" | sort | uniq
   ```
2. Use environment variable validation
3. Document all required variables with examples

**Prevention:**
- Use .env.example files
- Implement startup validation
- Regular environment audits

### 3.2 Performance Degradation

#### 3.2.1 Slow API Response Times

**Symptoms:**
- API latency >2 seconds
- Database query timeouts
- Memory usage steadily increasing

**Root Causes:**
- N+1 query problems
- Missing database indexes
- Memory leaks in long-running processes

**Solutions:**
1. Enable query logging to identify slow queries
2. Add appropriate indexes:
   ```sql
   CREATE INDEX idx_quotes_vessel_id ON quotes(vessel_id);
   CREATE INDEX idx_quotes_created_at ON quotes(created_at DESC);
   ```
3. Implement connection pooling with proper limits

**Prevention:**
- Regular performance profiling
- Automated performance testing
- Database query analysis in code reviews

#### 3.2.2 Frontend Performance Issues

**Symptoms:**
- High First Contentful Paint (>2.5s)
- Large bundle sizes
- Janky scrolling or animations

**Root Causes:**
- Unoptimized images
- Blocking JavaScript execution
- Excessive re-renders

**Solutions:**
1. Implement image optimization:
   ```javascript
   import Image from 'next/image';
   <Image src="/hero.jpg" alt="Hero" width={1200} height={600} priority />
   ```
2. Use React.memo and useMemo appropriately
3. Lazy load non-critical components

**Prevention:**
- Lighthouse CI performance budgets
- Regular bundle analysis
- Performance monitoring in production

### 3.3 Error Tracking and Monitoring Issues

#### 3.3.1 Sentry Integration Problems

**Symptoms:**
- Errors not appearing in Sentry dashboard
- Source maps not working
- Performance data missing

**Root Causes:**
- Incorrect DSN configuration
- Source map upload failures
- Sampling rate too low

**Solutions:**
1. Verify Sentry initialization:
   ```javascript
   Sentry.init({
     dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
     environment: process.env.NODE_ENV,
     tracesSampleRate: 0.1,
   });
   ```
2. Configure source map upload in build process
3. Increase sampling rate for critical transactions

**Prevention:**
- Test Sentry integration in staging
- Monitor Sentry quota usage
- Regular error report reviews

#### 3.3.2 Missing Error Context

**Symptoms:**
- Errors without user context
- Unable to reproduce reported issues
- Generic error messages

**Root Causes:**
- Insufficient error boundaries
- Missing user context in errors
- Poor error messages

**Solutions:**
1. Implement comprehensive error boundaries:
   ```javascript
   <ErrorBoundary
     fallback={<ErrorFallback />}
     onError={(error, errorInfo) => {
       Sentry.captureException(error, {
         contexts: { react: { componentStack: errorInfo.componentStack } }
       });
     }}
   >
   ```
2. Add user context to all errors
3. Include request IDs in error responses

**Prevention:**
- Standardize error handling patterns
- Include error scenarios in testing
- Regular error dashboard reviews

### 3.4 Security and Compliance Problems

#### 3.4.1 Security Vulnerability Alerts

**Symptoms:**
- Dependabot security alerts
- Failed security scans
- Penetration test findings

**Root Causes:**
- Outdated dependencies
- Insecure coding practices
- Missing security headers

**Solutions:**
1. Update vulnerable dependencies:
   ```bash
   pnpm audit
   pnpm update --interactive
   ```
2. Implement security headers:
   ```javascript
   // next.config.js
   async headers() {
     return [{
       source: '/(.*)',
       headers: securityHeaders,
     }];
   }
   ```
3. Regular security training for team

**Prevention:**
- Automated dependency updates
- Security-focused code reviews
- Regular penetration testing

#### 3.4.2 Compliance Audit Failures

**Symptoms:**
- Failed GDPR compliance checks
- Missing audit logs
- Data retention policy violations

**Root Causes:**
- Insufficient logging
- Missing data lifecycle management
- Unclear data processing documentation

**Solutions:**
1. Implement comprehensive audit logging
2. Create data retention policies
3. Document all data processing activities

**Prevention:**
- Regular compliance reviews
- Automated compliance checks
- Privacy by design principles

---

## 4. Team Collaboration Issues

### 4.1 Communication Tool Problems

#### 4.1.1 Microsoft Teams Notification Overload

**Symptoms:**
- Important messages missed
- Constant interruptions
- Channel chaos

**Root Causes:**
- Poor channel organization
- Lack of notification rules
- Missing communication protocols

**Solutions:**
1. Implement channel naming conventions:
   - `#dev-frontend` - Frontend development
   - `#dev-backend` - Backend development
   - `#alerts-production` - Production alerts only
2. Configure smart notifications
3. Create communication guidelines

**Prevention:**
- Regular channel audits
- Clear communication protocols
- Team notification preferences

#### 4.1.2 Documentation Sync Issues

**Symptoms:**
- Outdated documentation
- Conflicting information sources
- Missing critical documentation

**Root Causes:**
- No single source of truth
- Manual documentation processes
- Lack of documentation ownership

**Solutions:**
1. Implement Notion as single source of truth
2. Automate documentation generation:
   ```javascript
   // Use Claude MCP for automated docs
   await claude.generateDocs({
     source: './src',
     output: './docs'
   });
   ```
3. Assign documentation owners

**Prevention:**
- Documentation in Definition of Done
- Regular documentation reviews
- Automated documentation checks

### 4.2 Version Control Conflicts

#### 4.2.1 Merge Conflicts

**Symptoms:**
- Frequent merge conflicts
- Lost code changes
- Broken builds after merges

**Root Causes:**
- Long-lived feature branches
- Poor branch naming
- Lack of communication

**Solutions:**
1. Implement branch protection rules
2. Use conventional commits:
   ```bash
   feat(quote): add vessel type validation
   fix(api): correct rate calculation error
   ```
3. Regular branch synchronization

**Prevention:**
- Small, frequent commits
- Feature flags for long features
- Daily branch updates

#### 4.2.2 Code Review Bottlenecks

**Symptoms:**
- PRs waiting days for review
- Superficial reviews
- Review fatigue

**Root Causes:**
- Large PR sizes
- Unclear review responsibilities
- Missing review guidelines

**Solutions:**
1. Implement PR size limits (max 400 lines)
2. Create review checklist:
   - [ ] Tests pass
   - [ ] Documentation updated
   - [ ] Performance impact considered
   - [ ] Security reviewed
3. Rotate review responsibilities

**Prevention:**
- Automated PR checks
- Review SLAs (24 hours)
- Pair programming for complex changes

### 4.3 Review Process Bottlenecks

#### 4.3.1 Slow PR Approvals

**Symptoms:**
- PRs open for >48 hours
- Multiple review rounds
- Blocked development

**Root Causes:**
- Unclear requirements
- Missing context in PRs
- Reviewer availability

**Solutions:**
1. Implement PR templates:
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   
   ## Testing
   - [ ] Unit tests pass
   - [ ] E2E tests pass
   
   ## Screenshots (if applicable)
   ```
2. Use draft PRs for early feedback
3. Implement review time slots

**Prevention:**
- Clear acceptance criteria
- Automated checks before review
- Review time allocation

### 4.4 Training and Onboarding Challenges

#### 4.4.1 New Developer Onboarding

**Symptoms:**
- Long time to first commit (>1 week)
- Repeated basic questions
- Inconsistent setup across team

**Root Causes:**
- Missing onboarding documentation
- Complex local setup
- Information overload

**Solutions:**
1. Create onboarding checklist:
   - [ ] GitHub access granted
   - [ ] GitPod workspace created
   - [ ] Claude Code Max configured
   - [ ] First PR submitted
2. Record setup videos
3. Assign onboarding buddy

**Prevention:**
- Automated environment setup
- Regular onboarding updates
- Feedback collection

#### 4.4.2 Tool Adoption Resistance

**Symptoms:**
- Low tool usage rates
- Reverting to old workflows
- Productivity not improving

**Root Causes:**
- Insufficient training
- Unclear benefits
- Change fatigue

**Solutions:**
1. Demonstrate clear wins:
   - Show 10x test generation speed
   - Highlight automated documentation
   - Share success metrics
2. Provide hands-on workshops
3. Create tool champions

**Prevention:**
- Gradual tool introduction
- Success story sharing
- Regular training sessions

---

## Escalation Procedures

### Severity Levels

#### SEV1 - Critical (Production Down)
- **Response Time**: 15 minutes
- **Escalation**: Head of Engineering → Product Owner → External Support
- **Communication**: Immediate Teams alert + Status page update

#### SEV2 - High (Major Feature Broken)
- **Response Time**: 2 hours
- **Escalation**: Lead Developer → Head of Engineering
- **Communication**: Teams channel update + JIRA ticket

#### SEV3 - Medium (Minor Feature Issue)
- **Response Time**: 24 hours
- **Escalation**: Developer → Lead Developer
- **Communication**: JIRA ticket + Teams thread

#### SEV4 - Low (Cosmetic/Minor)
- **Response Time**: 1 week
- **Escalation**: Normal development flow
- **Communication**: JIRA ticket

### External Support Contacts

#### Critical Infrastructure
- **GitHub Support**: https://support.github.com (Enterprise SLA: 4 hours)
- **Railway Support**: support@railway.app (Pro SLA: 24 hours)
- **Vercel Support**: https://vercel.com/support (Pro SLA: 24 hours)
- **Neon Support**: support@neon.tech (Business hours)

#### Tool Support
- **Claude/Anthropic**: https://support.anthropic.com
- **Sentry**: https://sentry.io/support/
- **Microsoft Teams**: Via organizational IT support

### Incident Response Process

1. **Identify**: Determine severity and impact
2. **Communicate**: Alert appropriate channels
3. **Mitigate**: Implement temporary fixes if needed
4. **Resolve**: Fix root cause
5. **Document**: Create incident report
6. **Review**: Post-mortem within 48 hours

### Post-Mortem Template

```markdown
## Incident Post-Mortem

**Date**: [YYYY-MM-DD]
**Duration**: [X hours Y minutes]
**Severity**: [SEV1-4]
**Impact**: [Users/features affected]

### Timeline
- HH:MM - Issue detected
- HH:MM - Investigation started
- HH:MM - Root cause identified
- HH:MM - Fix deployed
- HH:MM - Issue resolved

### Root Cause
[Technical explanation]

### Resolution
[Steps taken to resolve]

### Action Items
- [ ] [Preventive measure 1]
- [ ] [Preventive measure 2]

### Lessons Learned
[Key takeaways]
```

---

## Quick Reference Checklists

### Daily Health Checks
- [ ] All GitHub Actions passing
- [ ] No Sentry errors in last 24h
- [ ] Lighthouse scores within budget
- [ ] Database performance normal
- [ ] No security alerts

### Weekly Maintenance
- [ ] Review and merge Dependabot PRs
- [ ] Clear old GitPod workspaces
- [ ] Review error trends in Sentry
- [ ] Update team on any issues
- [ ] Check infrastructure costs

### Monthly Reviews
- [ ] Full security audit
- [ ] Performance benchmarking
- [ ] Tool usage analysis
- [ ] Documentation updates
- [ ] Team feedback collection

---

## Conclusion

This troubleshooting guide covers the most common issues encountered with the AI-assisted SDLC workflow stack. Regular maintenance, proactive monitoring, and clear escalation procedures will minimize the impact of these issues on team productivity.

For issues not covered in this guide:
1. Check tool-specific documentation
2. Search GitHub issues for similar problems
3. Contact tool support with detailed information
4. Document new solutions for future reference

Remember: Prevention is always better than cure. Invest time in proper setup, monitoring, and maintenance to avoid most issues before they impact development.