# Implementation Setup Guide - Maritime Insurance Infrastructure

## Overview

This guide provides step-by-step instructions for implementing the complete infrastructure stack for the maritime insurance application development team.

**Target Setup:**
- 4-person development team
- Complete ephemeral environments
- Automated CI/CD pipeline
- Zero DevOps complexity

---

## 🚀 IMPLEMENTATION TIMELINE

### **Week 1: Foundation Setup**
- Day 1-2: Local development environment setup
- Day 3-4: Neon database configuration
- Day 5: Team onboarding and training

### **Week 2: Deployment Pipeline**
- Day 1-2: Railway backend setup
- Day 3-4: Vercel frontend setup
- Day 5: GitHub Actions configuration

### **Week 3: Testing and Optimization**
- Day 1-2: Nx monorepo configuration
- Day 3-4: Automated testing setup
- Day 5: Stakeholder UAT training

### **Week 4: Production Readiness**
- Day 1-2: Production deployment
- Day 3-4: Monitoring and alerts
- Day 5: Documentation and handoff

---

## 📋 PREREQUISITES

### **Required Accounts**
- [ ] GitHub organization account
- [ ] Neon database account (see [Neon documentation](../../tools/neon.md))
- [ ] Railway account (see [Railway documentation](../../tools/railway.md))
- [ ] Vercel account (see [Vercel documentation](../../tools/vercel.md))
- [ ] (Optional Year-2) GitPod Professional account (see [GitPod documentation](../../tools/gitpod.md))

### **Required Information**
- [ ] Team member email addresses
- [ ] Repository URL
- [ ] Domain name for production
- [ ] Microsoft Teams webhook URL

### **Access Requirements**
- [ ] GitHub organization admin access
- [ ] Ability to create webhooks
- [ ] Ability to manage team members
- [ ] Billing access for subscriptions

---

## 🔧 DETAILED SETUP INSTRUCTIONS

### **Step 1: Local Development Environment Setup**

#### **1.1 Create Development Environment Setup Script**
```bash
# Create setup-dev-environment.sh
#!/bin/bash
echo "Setting up local development environment..."

# Install Node.js via nvm
if ! command -v nvm &> /dev/null; then
  curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
  source ~/.bashrc
fi

# Install and use Node.js 20
nvm install 20
nvm use 20

# Install pnpm
npm install -g pnpm

# Install dependencies
pnpm install

# Setup pre-commit hooks
pre-commit install

echo "Development environment setup complete!"
```

#### **1.2 Configure VS Code/Cursor Settings**
```json
# Create .vscode/settings.json
{
  "typescript.preferences.importModuleSpecifier": "relative",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.tabSize": 2,
  "editor.insertSpaces": true
}
```

#### **1.3 Environment Variables Template**
```bash
# Create .env.example
DATABASE_URL="postgresql://user:password@localhost:5432/maritime_dev"
CLAUDE_API_KEY="sk-..."
SENTRY_DSN="https://..."
VITE_API_URL="http://localhost:8000"
NODE_ENV="development"
```

### **Step 2: Neon Database Configuration**

#### **2.1 Create Neon Project**
```bash
# Visit: https://console.neon.tech/
# Click "Create Project"
# Project name: "maritime-insurance-db"
# Region: Select closest to your users
# PostgreSQL version: 15 (latest)
```

#### **2.2 Configure Database Branching**
```bash
# Install Neon CLI
npm install -g neon-cli

# Login to Neon
neon auth login

# Create development branch
neon branches create --name development --parent main

# Create staging branch
neon branches create --name staging --parent main

# Get connection strings
neon connection-string main
neon connection-string development
neon connection-string staging
```

#### **2.3 Environment Variables Setup**
```bash
# Add to GitHub repository secrets
DATABASE_URL_MAIN=postgresql://user:pass@ep-main.neon.tech/main
DATABASE_URL_DEVELOPMENT=postgresql://user:pass@ep-dev.neon.tech/main
DATABASE_URL_STAGING=postgresql://user:pass@ep-staging.neon.tech/main
NEON_API_KEY=your-neon-api-key
```

### **Step 3: Railway Backend Setup**

#### **3.1 Create Railway Project**
```bash
# Visit: https://railway.app/
# Click "New Project"
# Select "Deploy from GitHub repo"
# Connect your repository
# Select "FastAPI" template
```

#### **3.2 Configure Railway Service**
```toml
# Create railway.toml in repository root
[build]
builder = "NIXPACKS"

[deploy]
healthcheckPath = "/health"
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3

[environments.production]
variables = { NODE_ENV = "production" }

[environments.staging]
variables = { NODE_ENV = "staging", DEBUG = "true" }
```

#### **3.3 Railway Environment Variables**
```bash
# Production environment
railway variables set NODE_ENV=production
railway variables set DATABASE_URL=$DATABASE_URL_MAIN
railway variables set CORS_ORIGIN=https://marine-app.vercel.app

# Staging environment
railway variables set NODE_ENV=staging
railway variables set DATABASE_URL=$DATABASE_URL_STAGING
railway variables set CORS_ORIGIN=https://staging-marine-app.vercel.app
```

### **Step 4: Vercel Frontend Setup**

#### **4.1 Create Vercel Project**
```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Connect repository
vercel --prod
```

#### **4.2 Configure Vercel Project**
```json
# Create vercel.json in repository root
{
  "version": 2,
  "builds": [
    {
      "src": "apps/frontend/package.json",
      "use": "@vercel/next"
    }
  ],
  "routes": [
    {
      "handle": "filesystem"
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ],
  "env": {
    "VITE_API_URL": "@api-url"
  }
}
```

#### **4.3 Vercel Environment Variables**
```bash
# Production environment
vercel env add VITE_API_URL production
# Value: https://marine-api.railway.app

# Staging environment
vercel env add VITE_API_URL staging
# Value: https://staging-marine-api.railway.app
```

### **Step 5: GitHub Actions Configuration**

#### **5.1 Create Workflow File**
```yaml
# Create .github/workflows/ephemeral-environments.yml
name: Ephemeral Environments

on:
  pull_request:
    types: [opened, synchronize, reopened, closed]
  workflow_dispatch:

env:
  NEON_API_KEY: ${{ secrets.NEON_API_KEY }}
  RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
  VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
  VERCEL_ORG_ID: ${{ secrets.VERCEL_ORG_ID }}
  VERCEL_PROJECT_ID: ${{ secrets.VERCEL_PROJECT_ID }}

jobs:
  setup:
    runs-on: ubuntu-latest
    outputs:
      should-deploy: ${{ steps.check.outputs.should-deploy }}
      affected-apps: ${{ steps.affected.outputs.apps }}
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install

      - name: Check if should deploy
        id: check
        run: |
          if [ "${{ github.event.action }}" = "closed" ]; then
            echo "should-deploy=false" >> $GITHUB_OUTPUT
          else
            echo "should-deploy=true" >> $GITHUB_OUTPUT
          fi

      - name: Get affected apps
        id: affected
        if: steps.check.outputs.should-deploy == 'true'
        run: |
          AFFECTED=$(pnpm nx affected:apps --plain --base=origin/main --head=HEAD)
          echo "apps=$AFFECTED" >> $GITHUB_OUTPUT

  create-database-branch:
    needs: setup
    if: needs.setup.outputs.should-deploy == 'true'
    runs-on: ubuntu-latest
    steps:
      - name: Create Neon database branch
        run: |
          curl -X POST "https://console.neon.tech/api/v2/projects/$PROJECT_ID/branches" \
            -H "Authorization: Bearer $NEON_API_KEY" \
            -H "Content-Type: application/json" \
            -d "{\"name\": \"pr-${{ github.event.number }}\", \"parent_id\": \"main\"}"

  deploy-backend:
    needs: [setup, create-database-branch]
    if: needs.setup.outputs.should-deploy == 'true' && contains(needs.setup.outputs.affected-apps, 'backend')
    runs-on: ubuntu-latest
    outputs:
      railway-url: ${{ steps.deploy.outputs.url }}
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Deploy to Railway
        id: deploy
        run: |
          railway up --service=api-pr-${{ github.event.number }}
          echo "url=https://api-pr-${{ github.event.number }}.railway.app" >> $GITHUB_OUTPUT
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}

  deploy-frontend:
    needs: [setup, deploy-backend]
    if: needs.setup.outputs.should-deploy == 'true' && contains(needs.setup.outputs.affected-apps, 'frontend')
    runs-on: ubuntu-latest
    outputs:
      vercel-url: ${{ steps.deploy.outputs.url }}
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Deploy to Vercel
        id: deploy
        run: |
          vercel --prod --token=$VERCEL_TOKEN
          echo "url=https://pr-${{ github.event.number }}-marine-app.vercel.app" >> $GITHUB_OUTPUT
        env:
          VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
          VITE_API_URL: ${{ needs.deploy-backend.outputs.railway-url }}

  run-tests:
    needs: [deploy-backend, deploy-frontend]
    if: needs.setup.outputs.should-deploy == 'true'
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
        run: pnpm install

      - name: Run tests
        run: |
          pnpm nx affected:test --parallel=3
          pnpm nx affected:e2e --parallel=2
        env:
          API_URL: ${{ needs.deploy-backend.outputs.railway-url }}
          FRONTEND_URL: ${{ needs.deploy-frontend.outputs.vercel-url }}

  notify-stakeholders:
    needs: [deploy-backend, deploy-frontend, run-tests]
    if: always() && needs.setup.outputs.should-deploy == 'true'
    runs-on: ubuntu-latest
    steps:
      - name: Notify Microsoft Teams
        run: |
          curl -X POST "${{ secrets.TEAMS_WEBHOOK_URL }}" \
            -H "Content-Type: application/json" \
            -d "{
              \"text\": \"🚢 PR #${{ github.event.number }} Environment Ready!\",
              \"sections\": [{
                \"facts\": [
                  {\"name\": \"Frontend\", \"value\": \"${{ needs.deploy-frontend.outputs.vercel-url }}\"},
                  {\"name\": \"Backend\", \"value\": \"${{ needs.deploy-backend.outputs.railway-url }}\"},
                  {\"name\": \"Tests\", \"value\": \"${{ needs.run-tests.result }}\"}
                ]
              }]
            }"

  cleanup:
    if: github.event.action == 'closed'
    runs-on: ubuntu-latest
    steps:
      - name: Cleanup Railway
        run: |
          railway down --service=api-pr-${{ github.event.number }}
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}

      - name: Cleanup Vercel
        run: |
          vercel remove pr-${{ github.event.number }}-marine-app.vercel.app --yes
        env:
          VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}

      - name: Cleanup Neon branch
        run: |
          curl -X DELETE "https://console.neon.tech/api/v2/projects/$PROJECT_ID/branches/pr-${{ github.event.number }}" \
            -H "Authorization: Bearer $NEON_API_KEY"
```

#### **5.2 GitHub Secrets Configuration**
```bash
# Add the following secrets to GitHub repository:
# Settings > Secrets and variables > Actions > New repository secret

NEON_API_KEY=your-neon-api-key
RAILWAY_TOKEN=your-railway-token
VERCEL_TOKEN=your-vercel-token
VERCEL_ORG_ID=your-vercel-org-id
VERCEL_PROJECT_ID=your-vercel-project-id
TEAMS_WEBHOOK_URL=your-teams-webhook-url
```

### **Step 6: Nx Monorepo Configuration**

#### **6.1 Initialize Nx Workspace**
```bash
# If not already initialized
npx create-nx-workspace@latest maritime-insurance --preset=react-monorepo

# Add FastAPI support
pnpm add -D @nxlv/python

# Generate FastAPI application
pnpm nx generate @nxlv/python:poetry-project backend --directory=apps
```

#### **6.2 Configure Nx for Affected Builds**
```json
{
  "version": 2,
  "targetDefaults": {
    "build": {
      "dependsOn": ["^build"],
      "cache": true
    },
    "test": {
      "cache": true
    },
    "e2e": {
      "cache": true
    }
  },
  "affected": {
    "defaultBase": "main"
  },
  "generators": {
    "@nx/react": {
      "application": {
        "bundler": "vite"
      }
    }
  }
}
```

---

## 🧪 TESTING THE SETUP

### **Test 1: Local Development Environment**
```bash
# Clone repository locally
git clone https://github.com/your-org/maritime-insurance
cd maritime-insurance

# Run setup script
./setup-dev-environment.sh

# Verify:
# ✓ Environment sets up in <2 minutes
# ✓ Dependencies installed automatically
# ✓ Development servers start
# ✓ Database connection works
```

### **Test 2: Create Test PR**
```bash
# Create test branch
git checkout -b test/infrastructure-setup

# Make small change
echo "# Test" >> README.md
git add README.md
git commit -m "test: Infrastructure setup verification"
git push origin test/infrastructure-setup

# Create PR via GitHub UI
# Verify:
# ✓ GitHub Actions triggers
# ✓ Environments deployed
# ✓ Tests run successfully
# ✓ Teams notification sent
```

### **Test 3: Stakeholder UAT**
```bash
# Share PR environment URLs with stakeholders
# Verify:
# ✓ Frontend accessible
# ✓ Backend API responding
# ✓ Database connected
# ✓ Features working end-to-end
```

---

## 🎯 SUCCESS METRICS

### **Week 1 Targets**
- [ ] All team members have local development setup
- [ ] Database connections working
- [ ] Development servers running

### **Week 2 Targets**
- [ ] PR creates ephemeral environments
- [ ] Automated deployments working
- [ ] CI/CD pipeline functional

### **Week 3 Targets**
- [ ] Stakeholders can access UAT
- [ ] Testing pipeline complete
- [ ] Nx optimizations active

### **Week 4 Targets**
- [ ] Production deployments working
- [ ] Monitoring and alerts active
- [ ] Team fully trained

---

## 📞 SUPPORT AND TROUBLESHOOTING

### **Common Issues**

#### **Local Development Issues**
- **Node.js version mismatch**: Run nvm install && nvm use
- **Dependencies missing**: Run pnpm install
- **Ports not accessible**: Check if ports 3000/8000 are available

#### **Database Issues**
- **Connection failures**: Verify environment variables
- **Branch creation errors**: Check Neon API permissions
- **Migration failures**: Verify database schema

#### **Deployment Issues**
- **Railway deployment fails**: Check railway.toml configuration
- **Vercel build errors**: Verify build settings
- **GitHub Actions errors**: Check secrets configuration

### **Getting Help**
- **Local Development**: Node.js documentation and community
- **Neon**: Documentation at neon.tech/docs
- **Railway**: Support via Railway dashboard
- **Vercel**: Documentation at vercel.com/docs
- **GitHub Actions**: GitHub community support

---

## 💰 COST TRACKING

### **Monthly Costs**
- **Local Development**: $0 (no ongoing costs)
- **Neon Database**: $25-30 (with branching)
- **Railway**: $20 (backend hosting)
- **Vercel**: $20 (frontend hosting)
- **GitHub Actions**: $0 (included)

**Total**: $65-70/month

### **ROI Calculation**
- **Time saved**: 16 hours/month (vs complex setup)
- **Team hourly rate**: $75/hour average
- **Value created**: $1,200/month
- **Cost savings**: $200/month vs GitPod
- **ROI**: 1,700%+ return on investment

---

## 🚀 NEXT STEPS

1. **Week 1**: Complete foundation setup
2. **Week 2**: Implement CI/CD pipeline
3. **Week 3**: Train team and stakeholders
4. **Week 4**: Go live with production

**After Implementation:**
- Monitor performance and costs
- Optimize based on usage patterns
- Scale as team grows
- Continuous improvement

This setup provides a complete, production-ready infrastructure with minimal ongoing maintenance and maximum developer productivity.

---

**Setup Support**: For implementation questions, refer to the master infrastructure decision document and tool overlap analysis for additional context and reasoning.