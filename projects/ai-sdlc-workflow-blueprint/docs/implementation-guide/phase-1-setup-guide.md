# Phase 1 Setup Guide - Complete Implementation Roadmap

**Version**: 1.0  
**Last Updated**: 2025-07-15  
**Target Audience**: Head of Engineering  
**Total Implementation Time**: 4-6 weeks  
**Total Monthly Cost**: $748 (including all tools and infrastructure)

---

## Table of Contents

1. [Overview & Prerequisites](#overview--prerequisites)
2. [Phase 1A: Tool Procurement & Accounts (Week 1)](#phase-1a-tool-procurement--accounts-week-1)
3. [Phase 1B: Development Environment Setup (Week 2)](#phase-1b-development-environment-setup-week-2)
4. [Phase 1C: Infrastructure Setup (Week 3-4)](#phase-1c-infrastructure-setup-week-3-4)
5. [Phase 1D: Testing Framework Setup (Week 4-5)](#phase-1d-testing-framework-setup-week-4-5)
6. [Phase 1E: Team Onboarding (Week 5-6)](#phase-1e-team-onboarding-week-5-6)
7. [Verification & Success Criteria](#verification--success-criteria)
8. [Troubleshooting Guide](#troubleshooting-guide)

---

## Overview & Prerequisites

### Prerequisites Checklist

Before starting, ensure you have:

- [ ] GitHub account with administrative privileges
- [ ] Corporate credit card for subscriptions
- [ ] Email addresses for all 4 team members
- [ ] Basic understanding of Git and command line
- [ ] Access to company domain for email verification

### Cost Summary

| Category | Monthly Cost | Details |
|----------|--------------|---------|
| **AI Tools** | $430 | Claude Code Max subscriptions |
| **Communication** | $32 | Notion Team (experimental) |
| **Infrastructure** | $286 | GitPod, GitHub, Neon, Railway, Vercel |
| **Monitoring** | $26 | Sentry Pro |
| **Design** | $30 | Figma Professional (2 seats) |
| **Total** | **$804/month** | All tools and infrastructure |

---

## Phase 1A: Tool Procurement & Accounts (Week 1)

### Day 1-2: AI Tool Subscriptions

#### Claude Code Max Setup

**Time Required**: 2 hours per account

1. **Head of Engineering Account** (Already Active)
   ```bash
   # Verify existing subscription
   https://claude.ai/settings/subscription
   # Should show: $100/month tier
   ```

2. **Lead Frontend Developer Account** (Already Active)
   ```bash
   # Verify existing subscription
   https://claude.ai/settings/subscription
   # Should show: $200/month tier
   ```

3. **Lead Backend Developer Account** (NEW)
   ```bash
   # Navigate to Claude AI
   https://claude.ai/signup
   
   # Select subscription
   Claude Code Max - $100/month tier
   
   # Enable MCP features
   Settings > Advanced > Enable Model Context Protocol
   ```

**Verification Steps**:
- [ ] All three accounts show active Claude Code Max subscriptions
- [ ] MCP (Model Context Protocol) is enabled on all accounts
- [ ] Test JIRA integration with sample prompt

### Day 2-3: Communication Tools

#### Microsoft Teams (Existing)
```bash
# No action required - continue using existing setup
# Verify integrations:
- GitHub notifications configured
- JIRA integration active
```

#### Notion Team Setup (Experimental - 3 months)
```bash
# Create Notion workspace
https://www.notion.so/signup

# Select Team plan
- 4 users × $8/month = $32/month
- Enable trial if available

# Configure workspace
1. Create project structure
2. Set up permissions (all team members as editors)
3. Install Notion API integrations
```

**Notion MCP Integration**:
```bash
# Install Notion MCP server for Claude integration
npm install -g @notionhq/mcp-server-notion

# Configure in Claude settings
{
  "mcpServers": {
    "notion": {
      "command": "notion-mcp-server",
      "apiKey": "YOUR_NOTION_API_KEY"
    }
  }
}
```

### Day 3-4: Design Tools

#### Figma Professional Setup
```bash
# Create Figma organization
https://www.figma.com/signup

# Purchase 2 Professional seats
- UI/UX Engineer: Full seat ($15/month)
- Lead Frontend Developer: Full seat ($15/month)

# Configure organization
1. Set up team workspace
2. Create design system library
3. Enable version history
4. Configure developer handoff settings
```

### Day 4-5: Free Tool Installation

#### Install for All Team Members

1. **Cursor IDE**
   ```bash
   # Download Cursor (free hobby plan)
   https://cursor.sh/download
   
   # Configure AI settings
   Settings > AI > Enable code completion
   Settings > AI > Use free tier
   ```

2. **Gemini CLI**
   ```bash
   # Install Gemini CLI
   npm install -g @google/gemini-cli
   
   # Verify installation
   gemini --version
   
   # Test with sample command
   gemini analyze --context "Show project structure"
   ```

3. **pnpm Package Manager**
   ```bash
   # Install pnpm globally
   npm install -g pnpm
   
   # Verify installation
   pnpm --version
   
   # Set as default package manager
   corepack enable
   corepack prepare pnpm@latest --activate
   ```

---

## Phase 1B: Development Environment Setup (Week 2)

### Day 1-2: GitPod Professional Configuration

**Time Required**: 4 hours

1. **Create GitPod Organization**
   ```bash
   # Navigate to GitPod
   https://gitpod.io/teams
   
   # Create new team
   Team Name: [Your Company Name]
   Plan: Professional ($50/user/month × 4 = $200/month)
   ```

2. **Configure GitPod Workspace**
   ```yaml
   # .gitpod.yml in repository root
   image: gitpod/workspace-full
   
   tasks:
     - name: Install Dependencies
       init: |
         pnpm install
         pnpm build
       command: |
         pnpm dev
   
   vscode:
     extensions:
       - dbaeumer.vscode-eslint
       - esbenp.prettier-vscode
       - bradlc.vscode-tailwindcss
       - prisma.prisma
   
   ports:
     - port: 3000
       onOpen: open-preview
       visibility: public
     - port: 8000
       onOpen: notify
       visibility: private
   ```

3. **Environment Variables Setup**
   ```bash
   # GitPod environment variables
   gp env DATABASE_URL="postgresql://..."
   gp env CLAUDE_API_KEY="sk-..."
   gp env SENTRY_DSN="https://..."
   ```

### Day 2-3: Repository Setup

1. **GitHub Organization Creation**
   ```bash
   # Create GitHub organization
   https://github.com/organizations/new
   
   # Select GitHub Team plan
   $4/user/month × 4 = $16/month
   ```

2. **Repository Structure**
   ```bash
   # Create monorepo structure
   maritime-insurance-app/
   ├── .github/
   │   ├── workflows/
   │   │   ├── ci.yml
   │   │   ├── deploy-frontend.yml
   │   │   └── deploy-backend.yml
   ├── apps/
   │   ├── frontend/         # Next.js/React app
   │   └── backend/          # FastAPI app
   ├── packages/
   │   ├── ui/              # Shared UI components
   │   ├── types/           # Shared TypeScript types
   │   └── utils/           # Shared utilities
   ├── .gitpod.yml
   ├── pnpm-workspace.yaml
   └── turbo.json
   ```

3. **Branch Protection Rules**
   ```bash
   # Settings > Branches > Add rule
   Branch name pattern: main
   
   ✓ Require pull request reviews (1 review)
   ✓ Dismiss stale pull request approvals
   ✓ Require status checks to pass
   ✓ Require branches to be up to date
   ✓ Include administrators
   ```

### Day 3-4: CI/CD Pipeline Setup

1. **GitHub Actions Workflow**
   ```yaml
   # .github/workflows/ci.yml
   name: CI Pipeline
   
   on:
     push:
       branches: [main, develop]
     pull_request:
       branches: [main]
   
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: pnpm/action-setup@v3
           with:
             version: 8
         - uses: actions/setup-node@v4
           with:
             node-version: '20'
             cache: 'pnpm'
         
         - name: Install dependencies
           run: pnpm install --frozen-lockfile
         
         - name: Run tests
           run: pnpm test:ci
         
         - name: Check coverage
           run: pnpm coverage
         
         - name: Run Lighthouse CI
           run: pnpm lhci autorun
   ```

---

## Phase 1C: Infrastructure Setup (Week 3-4)

### Day 1-2: Database Setup (Neon PostgreSQL)

**Time Required**: 3 hours

1. **Create Neon Account**
   ```bash
   # Navigate to Neon
   https://neon.tech/signup
   
   # Create project
   Project Name: maritime-insurance-db
   Region: Select closest to target users
   Plan: Scale ($25-30/month)
   ```

2. **Database Configuration**
   ```sql
   -- Create development branch
   CREATE DATABASE maritime_dev;
   
   -- Create staging branch
   CREATE DATABASE maritime_staging;
   
   -- Production remains on main branch
   ```

3. **Connection String Setup**
   ```bash
   # Development
   DATABASE_URL="postgresql://user:pass@host/maritime_dev?sslmode=require"
   
   # Staging  
   DATABASE_URL_STAGING="postgresql://user:pass@host/maritime_staging?sslmode=require"
   
   # Production
   DATABASE_URL_PROD="postgresql://user:pass@host/maritime_prod?sslmode=require"
   ```

### Day 2-3: Backend Hosting (Railway)

1. **Railway Setup**
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli
   
   # Login to Railway
   railway login
   
   # Create new project
   railway new maritime-insurance-backend
   ```

2. **Deploy FastAPI Backend**
   ```bash
   # railway.toml
   [build]
   builder = "nixpacks"
   
   [deploy]
   startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
   healthcheckPath = "/health"
   healthcheckTimeout = 30
   
   [environment]
   DATABASE_URL = "${{ NEON_DATABASE_URL }}"
   SENTRY_DSN = "${{ SENTRY_DSN }}"
   ```

3. **Environment Configuration**
   ```bash
   # Set Railway environment variables
   railway variables set DATABASE_URL=$NEON_CONNECTION_STRING
   railway variables set SENTRY_DSN=$SENTRY_DSN
   railway variables set ENVIRONMENT=production
   ```

### Day 3-4: Frontend Hosting (Vercel)

1. **Vercel Setup**
   ```bash
   # Install Vercel CLI
   npm install -g vercel
   
   # Login to Vercel
   vercel login
   
   # Link project
   vercel link
   ```

2. **Vercel Configuration**
   ```json
   // vercel.json
   {
     "framework": "nextjs",
     "buildCommand": "pnpm build",
     "devCommand": "pnpm dev",
     "outputDirectory": ".next",
     "env": {
       "NEXT_PUBLIC_API_URL": "@api_url",
       "NEXT_PUBLIC_SENTRY_DSN": "@sentry_dsn"
     }
   }
   ```

3. **Automatic Deployments**
   ```bash
   # Connect GitHub repository
   vercel git connect
   
   # Configure preview deployments
   Settings > Git > Enable preview deployments for all branches
   ```

---

## Phase 1D: Testing Framework Setup (Week 4-5)

### Day 1-2: Frontend Testing Setup

1. **Vitest Configuration**
   ```typescript
   // vitest.config.ts
   import { defineConfig } from 'vitest/config'
   import react from '@vitejs/plugin-react'
   
   export default defineConfig({
     plugins: [react()],
     test: {
       environment: 'jsdom',
       globals: true,
       setupFiles: './src/test/setup.ts',
       coverage: {
         provider: 'v8',
         reporter: ['text', 'json', 'html'],
         thresholds: {
           branches: 90,
           functions: 90,
           lines: 90,
           statements: 90
         }
       }
     }
   })
   ```

2. **React Testing Library Setup**
   ```bash
   # Install testing dependencies
   pnpm add -D vitest @testing-library/react @testing-library/jest-dom
   pnpm add -D @testing-library/user-event @vitejs/plugin-react
   ```

3. **Storybook Installation**
   ```bash
   # Initialize Storybook
   pnpm dlx storybook@latest init
   
   # Configure for Vite
   pnpm add -D @storybook/react-vite
   
   # Start Storybook
   pnpm storybook
   ```

### Day 2-3: E2E Testing Setup

1. **Playwright Installation**
   ```bash
   # Install Playwright
   pnpm add -D @playwright/test
   
   # Install browsers
   pnpm exec playwright install
   ```

2. **Playwright Configuration**
   ```typescript
   // playwright.config.ts
   import { defineConfig, devices } from '@playwright/test';
   
   export default defineConfig({
     testDir: './e2e',
     fullyParallel: true,
     forbidOnly: !!process.env.CI,
     retries: process.env.CI ? 2 : 0,
     workers: process.env.CI ? 1 : undefined,
     reporter: 'html',
     use: {
       baseURL: 'http://localhost:3000',
       trace: 'on-first-retry',
     },
     projects: [
       {
         name: 'chromium',
         use: { ...devices['Desktop Chrome'] },
       },
       {
         name: 'firefox',
         use: { ...devices['Desktop Firefox'] },
       },
       {
         name: 'webkit',
         use: { ...devices['Desktop Safari'] },
       },
     ],
   });
   ```

### Day 3-4: Quality & Monitoring Setup

1. **ESLint & Prettier Configuration**
   ```json
   // .eslintrc.json
   {
     "extends": [
       "next/core-web-vitals",
       "plugin:@typescript-eslint/recommended",
       "prettier"
     ],
     "rules": {
       "@typescript-eslint/no-unused-vars": "error",
       "@typescript-eslint/no-explicit-any": "error"
     }
   }
   ```

2. **Sentry Setup**
   ```bash
   # Create Sentry account
   https://sentry.io/signup/
   
   # Select Pro plan ($26/month)
   
   # Install Sentry SDK
   pnpm add @sentry/nextjs @sentry/node
   ```

3. **Sentry Configuration**
   ```typescript
   // sentry.client.config.ts
   import * as Sentry from '@sentry/nextjs';
   
   Sentry.init({
     dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
     environment: process.env.NODE_ENV,
     integrations: [
       new Sentry.BrowserTracing(),
       new Sentry.Replay(),
     ],
     tracesSampleRate: 1.0,
     replaysSessionSampleRate: 0.1,
     replaysOnErrorSampleRate: 1.0,
   });
   ```

4. **Lighthouse CI Setup**
   ```bash
   # Install Lighthouse CI
   pnpm add -D @lhci/cli
   
   # Configure Lighthouse CI
   module.exports = {
     ci: {
       collect: {
         url: ['http://localhost:3000'],
         numberOfRuns: 3,
       },
       assert: {
         preset: 'lighthouse:recommended',
         assertions: {
           'categories:performance': ['error', { minScore: 0.9 }],
           'categories:accessibility': ['error', { minScore: 0.9 }],
         },
       },
       upload: {
         target: 'temporary-public-storage',
       },
     },
   };
   ```

---

## Phase 1E: Team Onboarding (Week 5-6)

### Day 1-2: Tool Access Setup

**Time Required**: 1 hour per team member

1. **Access Checklist Per Team Member**
   ```markdown
   ## [Team Member Name] Setup Checklist
   
   - [ ] Claude Code Max account activated
   - [ ] GitHub organization access granted
   - [ ] GitPod workspace access configured
   - [ ] Notion team workspace joined
   - [ ] Figma access granted (if applicable)
   - [ ] Railway dashboard access
   - [ ] Vercel team access
   - [ ] Sentry project access
   ```

2. **Environment Setup Script**
   ```bash
   #!/bin/bash
   # setup-dev-environment.sh
   
   echo "Setting up development environment..."
   
   # Install required tools
   npm install -g pnpm @railway/cli vercel @google/gemini-cli
   
   # Clone repository
   git clone https://github.com/[org]/maritime-insurance-app.git
   cd maritime-insurance-app
   
   # Install dependencies
   pnpm install
   
   # Setup git hooks
   pnpm prepare
   
   # Copy environment variables
   cp .env.example .env.local
   
   echo "Setup complete! Edit .env.local with your credentials"
   ```

### Day 3-4: Training Sessions

1. **AI-Assisted Development Training** (2 hours)
   - Claude Code Max workflows
   - MCP integration with JIRA
   - Test generation with AI
   - Code review automation

2. **Infrastructure Training** (1.5 hours)
   - GitPod workspace usage
   - Deployment workflows
   - Database branching with Neon
   - Monitoring with Sentry

3. **Testing Framework Training** (2 hours)
   - TDD approach with Vitest
   - Storybook component development
   - Cross-browser testing with Playwright
   - Performance monitoring

---

## Verification & Success Criteria

### Phase Completion Checklist

#### Tools & Accounts ✓
- [ ] All Claude Code Max subscriptions active
- [ ] Notion workspace configured with MCP
- [ ] Figma seats allocated
- [ ] All free tools installed

#### Development Environment ✓
- [ ] GitPod workspaces functional
- [ ] Repository structure created
- [ ] Branch protection enabled
- [ ] CI/CD pipeline passing

#### Infrastructure ✓
- [ ] Neon database accessible
- [ ] Railway backend deployed
- [ ] Vercel frontend live
- [ ] All environments connected

#### Testing Framework ✓
- [ ] Unit tests running (90% coverage)
- [ ] E2E tests passing (all browsers)
- [ ] Storybook stories created
- [ ] Quality gates enforced

#### Team Readiness ✓
- [ ] All team members have access
- [ ] Training completed
- [ ] First PR successfully merged
- [ ] Monitoring dashboards accessible

### Success Metrics

1. **Development Velocity**
   - First feature deployed: < 1 week
   - PR review time: < 2 hours
   - Test coverage: > 90%

2. **System Performance**
   - Lighthouse score: > 90
   - Build time: < 5 minutes
   - Deploy time: < 2 minutes

3. **Team Productivity**
   - AI tool adoption: 100%
   - Test-first development: 100%
   - Documentation coverage: 100%

---

## Troubleshooting Guide

### Common Issues & Solutions

#### Claude Code Max Issues
```bash
# MCP not connecting to JIRA
Solution: Verify API token and permissions
Settings > Integrations > JIRA > Regenerate token

# Rate limiting errors
Solution: Upgrade to higher tier or distribute usage
Monitor usage at: claude.ai/settings/usage
```

#### GitPod Configuration
```bash
# Workspace not starting
Solution: Check .gitpod.yml syntax
Validate at: gitpod.io/validate

# Environment variables not loading
Solution: Use GitPod dashboard to set variables
https://gitpod.io/variables
```

#### Database Connection
```bash
# Neon connection timeout
Solution: Check firewall rules and SSL mode
Ensure sslmode=require in connection string

# Branch creation failing
Solution: Verify account limits
Upgrade plan if needed
```

#### Deployment Failures
```bash
# Railway deployment stuck
Solution: Check build logs
railway logs --service=backend

# Vercel build errors
Solution: Review build output
vercel logs --follow
```

### Support Resources

1. **Documentation Links**
   - Claude MCP: https://modelcontextprotocol.io/docs
   - GitPod: https://www.gitpod.io/docs
   - Neon: https://neon.tech/docs
   - Railway: https://docs.railway.app
   - Vercel: https://vercel.com/docs

2. **Community Support**
   - Claude Discord: discord.gg/claude
   - GitPod Community: community.gitpod.io
   - Railway Discord: discord.gg/railway

3. **Emergency Contacts**
   - Sentry Support: support@sentry.io
   - GitHub Support: support.github.com
   - Urgent issues: Create support tickets

---

## Next Steps

After completing Phase 1:

1. **Week 7-8**: Begin first sprint with full toolchain
2. **Month 2**: Optimize workflows based on metrics
3. **Month 3**: Evaluate experimental tools (Notion)
4. **Quarterly**: Review and adjust tool stack

This guide provides a complete, actionable roadmap for setting up your AI-enhanced development environment. Follow each phase sequentially, verify success criteria, and your team will be fully operational within 4-6 weeks.