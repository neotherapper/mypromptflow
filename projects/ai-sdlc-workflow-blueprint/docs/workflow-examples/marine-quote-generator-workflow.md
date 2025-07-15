# Marine Quote Generator - Complete Development Workflow

## Scenario Overview

This document provides a detailed walkthrough of how the **Lead Frontend Developer** and **Lead Backend Developer** would collaborate to build a "Marine Quote Generator" feature using the recommended infrastructure stack.

**Feature Requirements:**
- Generate insurance quotes for maritime vessels
- Calculate premiums based on vessel type, cargo, and route
- Provide instant quotes to customers
- Store quote history for follow-up

---

## 👥 TEAM SETUP

### Development Team
- **Sarah** (Lead Frontend Developer) - React/TypeScript specialist
- **Mike** (Lead Backend Developer) - FastAPI/Python specialist
- **John** (Product Owner) - Stakeholder and UAT reviewer
- **Anna** (Head of Engineering) - Technical oversight

### Tools Each Person Uses
- **All Developers**: GitPod Professional workspaces
- **All Team**: Microsoft Teams for communication
- **Product Owner**: Direct access to UAT environments
- **Head of Engineering**: Claude Code Max for oversight

---

## 🌊 COMPLETE DEVELOPMENT WORKFLOW

### **Day 1: Morning - Project Kickoff**

#### **9:00 AM - Product Owner (John) Creates Requirements**

**John opens JIRA and creates user story:**
```
Epic: Marine Quote Generator
Story: As a maritime insurance customer, I want to get instant quotes
  so that I can make informed decisions about my coverage.

Acceptance Criteria:
- User can select vessel type (cargo ship, tanker, container, etc.)
- User can input cargo details and route information
- System calculates premium based on risk factors
- Quote is displayed instantly with breakdown
- Quote can be saved and emailed to customer
```

#### **9:30 AM - Team Planning Meeting (Microsoft Teams)**

**Team discusses:**
- API endpoints needed
- Database schema requirements
- Frontend component structure
- Integration points

**Technical decisions:**
- Backend: FastAPI endpoints for quote calculation
- Frontend: React form with real-time validation
- Database: New tables for quotes, vessel types, and risk factors
- Testing: Unit tests + E2E tests + stakeholder UAT

---

### **Day 1: Development Begins**

#### **10:00 AM - Both Developers Start GitPod**

**Sarah (Frontend Developer):**
```bash
# Opens browser to: https://gitpod.io/#github.com/marine-insurance/app
# GitPod automatically:
# 1. Clones repository
# 2. Installs dependencies: pnpm install
# 3. Sets up Nx workspace
# 4. Starts development server: nx serve frontend
# 5. Opens VS Code in browser
```

**Mike (Backend Developer):**
```bash
# Opens same GitPod workspace
# GitPod automatically:
# 1. Sets up Python environment
# 2. Installs FastAPI dependencies
# 3. Connects to Neon database
# 4. Starts FastAPI server: nx serve backend
# 5. Opens Python debugger
```

#### **10:30 AM - Mike Creates Database Schema**

**Mike works in GitPod terminal:**
```bash
# Create database migration
alembic revision --autogenerate -m "Add marine quote tables"

# GitPod shows the migration file:
# apps/backend/alembic/versions/001_add_marine_quote_tables.py
```

**Generated migration:**
```python
# Migration file content
def upgrade():
    op.create_table('vessel_types',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('base_rate', sa.Decimal(10, 4), nullable=False),
        sa.Column('risk_multiplier', sa.Decimal(5, 2), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('quote_requests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('vessel_type_id', sa.Integer(), nullable=False),
        sa.Column('cargo_value', sa.Decimal(12, 2), nullable=False),
        sa.Column('route', sa.String(200), nullable=False),
        sa.Column('coverage_amount', sa.Decimal(12, 2), nullable=False),
        sa.Column('premium_amount', sa.Decimal(10, 2), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['vessel_type_id'], ['vessel_types.id'])
    )
```

**Mike runs migration:**
```bash
# Apply to local development database
alembic upgrade head

# Neon automatically creates database branch for development
# Connection string: postgresql://user:pass@ep-branch-dev.neon.tech/main
```

#### **11:00 AM - Mike Creates Backend API**

**Mike uses Nx generator (custom):**
```bash
# Generate FastAPI endpoint
nx generate @marine-app/api:endpoint marine-quote

# Creates:
# apps/backend/src/routes/marine_quote.py
# apps/backend/src/models/marine_quote.py
# apps/backend/src/services/marine_quote_service.py
# apps/backend/src/tests/test_marine_quote.py
```

**Generated API endpoint:**
```python
# apps/backend/src/routes/marine_quote.py
from fastapi import APIRouter, HTTPException
from ..models.marine_quote import QuoteRequest, QuoteResponse
from ..services.marine_quote_service import MarineQuoteService

router = APIRouter()

@router.post("/quote", response_model=QuoteResponse)
async def calculate_quote(request: QuoteRequest):
    """Calculate marine insurance quote"""
    try:
        service = MarineQuoteService()
        quote = await service.calculate_quote(request)
        return quote
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/vessel-types")
async def get_vessel_types():
    """Get all available vessel types"""
    service = MarineQuoteService()
    return await service.get_vessel_types()
```

#### **11:30 AM - Sarah Creates Frontend Component**

**Sarah uses Nx generator:**
```bash
# Generate React component
nx generate @nx/react:component marine-quote-generator

# Creates:
# apps/frontend/src/components/marine-quote-generator/
# ├── marine-quote-generator.tsx
# ├── marine-quote-generator.spec.tsx
# ├── marine-quote-generator.stories.tsx
# └── marine-quote-generator.module.css
```

**Generated React component:**
```typescript
// apps/frontend/src/components/marine-quote-generator/marine-quote-generator.tsx
import React, { useState, useEffect } from 'react';
import { QuoteRequest, QuoteResponse, VesselType } from '@marine-app/shared-types';
import { apiClient } from '@marine-app/api-client';

export function MarineQuoteGenerator() {
  const [vesselTypes, setVesselTypes] = useState<VesselType[]>([]);
  const [request, setRequest] = useState<QuoteRequest>({
    vessel_type_id: 0,
    cargo_value: 0,
    route: '',
    coverage_amount: 0
  });
  const [quote, setQuote] = useState<QuoteResponse | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Load vessel types on component mount
    loadVesselTypes();
  }, []);

  const loadVesselTypes = async () => {
    try {
      const types = await apiClient.get('/marine-quote/vessel-types');
      setVesselTypes(types.data);
    } catch (error) {
      console.error('Failed to load vessel types:', error);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const response = await apiClient.post('/marine-quote/quote', request);
      setQuote(response.data);
    } catch (error) {
      console.error('Failed to calculate quote:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="marine-quote-generator">
      <h2>Marine Insurance Quote Generator</h2>
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Vessel Type:</label>
          <select 
            value={request.vessel_type_id} 
            onChange={(e) => setRequest({...request, vessel_type_id: parseInt(e.target.value)})}
            required
          >
            <option value="">Select vessel type</option>
            {vesselTypes.map(type => (
              <option key={type.id} value={type.id}>{type.name}</option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>Cargo Value ($):</label>
          <input 
            type="number" 
            value={request.cargo_value}
            onChange={(e) => setRequest({...request, cargo_value: parseFloat(e.target.value)})}
            required
          />
        </div>

        <div className="form-group">
          <label>Route:</label>
          <input 
            type="text" 
            value={request.route}
            onChange={(e) => setRequest({...request, route: e.target.value})}
            placeholder="e.g., New York to Southampton"
            required
          />
        </div>

        <div className="form-group">
          <label>Coverage Amount ($):</label>
          <input 
            type="number" 
            value={request.coverage_amount}
            onChange={(e) => setRequest({...request, coverage_amount: parseFloat(e.target.value)})}
            required
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Calculating...' : 'Get Quote'}
        </button>
      </form>

      {quote && (
        <div className="quote-result">
          <h3>Your Quote</h3>
          <p><strong>Premium:</strong> ${quote.premium_amount}</p>
          <p><strong>Coverage:</strong> ${quote.coverage_amount}</p>
          <p><strong>Quote ID:</strong> {quote.id}</p>
          <p><strong>Valid Until:</strong> {new Date(quote.valid_until).toLocaleDateString()}</p>
          
          <div className="quote-actions">
            <button onClick={() => window.print()}>Print Quote</button>
            <button onClick={() => emailQuote(quote)}>Email Quote</button>
          </div>
        </div>
      )}
    </div>
  );
}
```

#### **12:00 PM - Shared Types Creation**

**Sarah creates shared TypeScript types:**
```typescript
// libs/shared-types/src/marine-quote.ts
export interface VesselType {
  id: number;
  name: string;
  base_rate: number;
  risk_multiplier: number;
}

export interface QuoteRequest {
  vessel_type_id: number;
  cargo_value: number;
  route: string;
  coverage_amount: number;
}

export interface QuoteResponse {
  id: number;
  premium_amount: number;
  coverage_amount: number;
  vessel_type: VesselType;
  route: string;
  valid_until: string;
  breakdown: {
    base_premium: number;
    risk_adjustment: number;
    route_factor: number;
    total_premium: number;
  };
}
```

---

### **Day 1: Afternoon - Testing and Integration**

#### **1:00 PM - Local Testing in GitPod**

**Both developers test locally:**

**Sarah's terminal:**
```bash
# Start frontend development server
nx serve frontend

# GitPod shows:
# ✓ Frontend running at: https://3000-marine-app-dev.gitpod.io
# ✓ Hot reload enabled
# ✓ Connected to backend API
```

**Mike's terminal:**
```bash
# Start backend development server
nx serve backend

# GitPod shows:
# ✓ Backend running at: https://8000-marine-app-dev.gitpod.io
# ✓ Database connected: postgresql://...neon.tech/main
# ✓ API docs available at: /docs
```

#### **1:30 PM - Unit Testing**

**Sarah writes frontend tests:**
```bash
# Run React component tests
nx test marine-quote-generator

# Test output:
# ✓ should render vessel type dropdown
# ✓ should calculate quote on form submit
# ✓ should display quote result
# ✓ should handle loading states
```

**Mike writes backend tests:**
```bash
# Run FastAPI tests
nx test marine-quote-api

# Test output:
# ✓ should calculate quote correctly
# ✓ should validate input parameters
# ✓ should handle invalid vessel types
# ✓ should return proper error messages
```

#### **2:00 PM - Integration Testing**

**Both developers test integration:**
```bash
# Run E2E tests
nx e2e marine-quote-e2e

# Test flow:
# 1. Open quote generator page
# 2. Select vessel type
# 3. Enter cargo details
# 4. Submit form
# 5. Verify quote calculation
# 6. Test quote actions (print, email)
```

---

### **Day 2: Pull Request and Deployment**

#### **9:00 AM - Create Pull Request**

**Sarah creates PR for frontend changes:**
```bash
# In GitPod terminal:
git checkout -b feature/marine-quote-generator-frontend
git add apps/frontend/src/components/marine-quote-generator/
git add libs/shared-types/src/marine-quote.ts
git commit -m "feat: Add marine quote generator frontend component

- Add vessel type selection dropdown
- Add cargo value and route input fields
- Add real-time quote calculation
- Add quote result display with actions
- Add comprehensive test coverage"

git push origin feature/marine-quote-generator-frontend
```

**Mike creates PR for backend changes:**
```bash
# In GitPod terminal:
git checkout -b feature/marine-quote-generator-backend
git add apps/backend/src/routes/marine_quote.py
git add apps/backend/src/models/marine_quote.py
git add apps/backend/src/services/marine_quote_service.py
git add apps/backend/alembic/versions/001_add_marine_quote_tables.py
git commit -m "feat: Add marine quote generator backend API

- Add vessel types and quote request tables
- Add quote calculation service with risk factors
- Add FastAPI endpoints for quote generation
- Add comprehensive test coverage with pytest"

git push origin feature/marine-quote-generator-backend
```

#### **9:30 AM - Automatic Deployment Triggered**

**GitHub Actions detects PR creation and starts deployment:**

```yaml
# .github/workflows/ephemeral-environments.yml triggered

name: Deploy Ephemeral Environment - Marine Quote Generator

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  detect-changes:
    runs-on: ubuntu-latest
    outputs:
      frontend-changed: ${{ steps.changes.outputs.frontend }}
      backend-changed: ${{ steps.changes.outputs.backend }}
    steps:
      - uses: actions/checkout@v4
      - name: Detect affected projects
        id: changes
        run: |
          if nx affected:apps --base=main | grep -q "frontend"; then
            echo "frontend=true" >> $GITHUB_OUTPUT
          fi
          if nx affected:apps --base=main | grep -q "backend"; then
            echo "backend=true" >> $GITHUB_OUTPUT
          fi

  create-database-branch:
    runs-on: ubuntu-latest
    if: needs.detect-changes.outputs.backend-changed == 'true'
    steps:
      - name: Create Neon database branch
        run: |
          # Create database branch for PR
          curl -X POST "https://console.neon.tech/api/v2/projects/$PROJECT_ID/branches" \
            -H "Authorization: Bearer $NEON_API_KEY" \
            -H "Content-Type: application/json" \
            -d '{
              "name": "pr-${{ github.event.number }}",
              "parent_id": "main"
            }'
          
          # Apply migrations to new branch
          DATABASE_URL="postgresql://...pr-${{ github.event.number }}.neon.tech/main"
          alembic upgrade head

  deploy-backend:
    runs-on: ubuntu-latest
    needs: [detect-changes, create-database-branch]
    if: needs.detect-changes.outputs.backend-changed == 'true'
    steps:
      - name: Deploy FastAPI to Railway
        run: |
          railway up --service=marine-api-pr-${{ github.event.number }}
          
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
          DATABASE_URL: "postgresql://...pr-${{ github.event.number }}.neon.tech/main"
          
      - name: Set environment variables
        run: |
          railway variables set NODE_ENV=staging
          railway variables set CORS_ORIGIN=https://pr-${{ github.event.number }}-marine-app.vercel.app
          railway variables set DATABASE_URL=${{ env.DATABASE_URL }}

  deploy-frontend:
    runs-on: ubuntu-latest
    needs: [detect-changes, deploy-backend]
    if: needs.detect-changes.outputs.frontend-changed == 'true'
    steps:
      - name: Deploy React to Vercel
        run: |
          vercel --prod --token=${{ secrets.VERCEL_TOKEN }}
          
        env:
          VERCEL_TOKEN: ${{ secrets.VERCEL_TOKEN }}
          VITE_API_URL: "https://marine-api-pr-${{ github.event.number }}.railway.app"

  run-tests:
    runs-on: ubuntu-latest
    needs: [deploy-backend, deploy-frontend]
    steps:
      - name: Run E2E tests against ephemeral environment
        run: |
          nx e2e marine-quote-e2e --baseUrl=https://pr-${{ github.event.number }}-marine-app.vercel.app
          
      - name: Run API tests
        run: |
          nx test marine-quote-api --coverage
          
  notify-stakeholders:
    runs-on: ubuntu-latest
    needs: [deploy-backend, deploy-frontend, run-tests]
    if: always()
    steps:
      - name: Send Teams notification
        run: |
          curl -X POST "${{ secrets.TEAMS_WEBHOOK }}" \
            -H "Content-Type: application/json" \
            -d '{
              "text": "🚢 Marine Quote Generator Ready for UAT!",
              "sections": [{
                "facts": [
                  {"name": "Frontend", "value": "https://pr-${{ github.event.number }}-marine-app.vercel.app"},
                  {"name": "Backend API", "value": "https://marine-api-pr-${{ github.event.number }}.railway.app/docs"},
                  {"name": "Database", "value": "Isolated branch with test data"},
                  {"name": "Tests", "value": "${{ needs.run-tests.result }}"}
                ]
              }]
            }'
```

#### **10:00 AM - Deployment Complete**

**GitHub Actions completion notification:**
```
✅ Ephemeral Environment Deployed Successfully!

PR #456 - Marine Quote Generator

🌐 Frontend: https://pr-456-marine-app.vercel.app
🔧 Backend API: https://marine-api-pr-456.railway.app
📊 API Docs: https://marine-api-pr-456.railway.app/docs
🗄️ Database: Isolated branch with test data
✅ Tests: All passing (Unit: 24/24, E2E: 8/8)

Ready for UAT testing!
```

---

### **Day 2: UAT and Stakeholder Review**

#### **10:30 AM - Product Owner (John) Tests Feature**

**John receives Teams notification and opens UAT environment:**

**John's testing process:**
1. **Opens frontend**: https://pr-456-marine-app.vercel.app
2. **Tests quote generator**:
   - Selects "Container Ship" vessel type
   - Enters $2,000,000 cargo value
   - Enters "Rotterdam to New York" route
   - Requests $2,500,000 coverage
   - Clicks "Get Quote"

3. **Verifies results**:
   - Quote appears: $8,450 premium
   - Breakdown shows: Base: $6,000, Risk: $1,200, Route: $1,250
   - Quote ID: QT-456-2024-001
   - Valid until: 30 days from now

4. **Tests actions**:
   - Print functionality works
   - Email functionality works
   - Quote is saved to database

#### **11:00 AM - Stakeholder Feedback**

**John adds PR comment:**
```
✅ UAT Testing Complete - Marine Quote Generator

Tested scenarios:
- Container ship quote: ✅ Working correctly
- Cargo ship quote: ✅ Working correctly  
- Invalid inputs: ✅ Proper error handling
- Quote actions: ✅ Print and email work
- Mobile responsiveness: ✅ Works on tablet/phone

Minor feedback:
- Could we add currency formatting? ($8,450.00 instead of $8450)
- Route dropdown might be better than free text
- Add quote comparison feature in future iteration

Status: ✅ APPROVED FOR PRODUCTION
```

#### **11:30 AM - Head of Engineering (Anna) Review**

**Anna uses Claude Code Max to review the PR:**

**Anna's Claude session:**
```
Anna: "Review the marine quote generator PR for code quality and architecture"

Claude: "I've analyzed the PR changes:

✅ Code Quality:
- Clean TypeScript interfaces in shared-types
- Proper error handling in both frontend and backend
- Comprehensive test coverage (92% frontend, 89% backend)
- Following established patterns

✅ Architecture:
- Proper separation of concerns
- Database migrations are reversible
- API follows RESTful conventions
- Frontend component is reusable

✅ Security:
- Input validation on both frontend and backend
- SQL injection protection with parameterized queries
- CORS properly configured
- No sensitive data in logs

Recommendations:
- Add rate limiting to quote endpoint
- Consider caching vessel types
- Add monitoring for quote calculation performance

Status: ✅ APPROVED"
```

#### **12:00 PM - PR Merge and Production Deployment**

**Sarah merges the PR:**
```bash
# PR is merged via GitHub UI
# Automatic merge triggers production deployment
```

**GitHub Actions production deployment:**
```yaml
# .github/workflows/production-deploy.yml triggered

name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy-production:
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production Railway
        run: |
          railway up --service=marine-api-production
          
      - name: Deploy to production Vercel
        run: |
          vercel --prod --token=${{ secrets.VERCEL_TOKEN }}
          
      - name: Merge database branch to main
        run: |
          # Merge PR database branch to main
          curl -X POST "https://console.neon.tech/api/v2/projects/$PROJECT_ID/branches/main/merge" \
            -H "Authorization: Bearer $NEON_API_KEY" \
            -d '{"source_branch": "pr-456"}'
          
      - name: Cleanup ephemeral environments
        run: |
          # Remove PR environments
          railway down --service=marine-api-pr-456
          vercel remove pr-456-marine-app.vercel.app --yes
          
          # Delete database branch
          curl -X DELETE "https://console.neon.tech/api/v2/projects/$PROJECT_ID/branches/pr-456" \
            -H "Authorization: Bearer $NEON_API_KEY"
```

#### **12:30 PM - Production Verification**

**Automated production tests:**
```bash
# Production smoke tests
nx e2e marine-quote-e2e --baseUrl=https://marine-app.vercel.app

# Results:
# ✅ Marine quote generator loads correctly
# ✅ API endpoints respond correctly
# ✅ Database connection successful
# ✅ All critical paths working

# Production deployment complete!
```

---

## 🎯 SUMMARY: WHAT JUST HAPPENED

### **Complete Workflow Overview**

```
Day 1: Development
├── GitPod Development Environment
│   ├── Sarah: Frontend React component
│   ├── Mike: Backend FastAPI endpoints
│   └── Both: Local testing and integration
├── Neon Database
│   ├── Schema migrations
│   ├── Local development branch
│   └── Test data seeding
└── Local Testing
    ├── Unit tests (Jest + Pytest)
    ├── Integration tests
    └── E2E tests (Cypress)

Day 2: Deployment & UAT
├── Pull Request Creation
│   ├── GitHub Actions triggered
│   ├── Nx detects affected projects
│   └── Automatic deployment begins
├── Ephemeral Environment Creation
│   ├── Railway: Backend API deployment
│   ├── Vercel: Frontend deployment
│   ├── Neon: Database branch creation
│   └── Teams: Stakeholder notification
├── UAT Testing
│   ├── Product Owner testing
│   ├── Stakeholder feedback
│   └── Technical review
└── Production Deployment
    ├── PR merge triggers production
    ├── Database branch merge
    ├── Ephemeral cleanup
    └── Production verification
```

### **Key Benefits Realized**

1. **Zero Setup Time**: Developers productive immediately in GitPod
2. **Isolated Testing**: Each PR has its own database and environment
3. **Stakeholder Involvement**: Immediate UAT access for feedback
4. **Automated Quality**: All tests run automatically
5. **Zero DevOps**: No manual deployment or environment management
6. **Cost Efficiency**: Environments created and destroyed automatically

### **Tools Working Together**

- **GitPod**: Development environment
- **Neon**: Database with branching
- **Railway**: Backend hosting
- **Vercel**: Frontend hosting
- **GitHub Actions**: Automation
- **Nx**: Build optimization
- **Microsoft Teams**: Communication

This workflow demonstrates how all tools work together to create a seamless development experience with minimal DevOps overhead and maximum stakeholder involvement.

---

**Total Development Time**: 1.5 days from idea to production  
**Manual Deployment Steps**: 0  
**Stakeholder Feedback Loop**: Immediate  
**Environment Management**: Fully automated