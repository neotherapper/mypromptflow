# Nx Monorepo Folder Structure Decision Options

## Decision Required: Choose optimal folder structure organization for VanguardAI Nx monorepo

Based on Nx v20+ documentation, VanguardAI implementation analysis, and maritime domain requirements for our 4-person team, here are the evaluated folder structure options:

## Current VanguardAI Context Analysis

**Team Structure**:
- Head of Engineering (architectural oversight)
- Lead Frontend Developer (React + TypeScript)
- Lead Backend Developer (FastAPI + Python)
- UI/UX Engineer (design + frontend collaboration)

**Maritime Domain Requirements**:
- **Core Entities**: Vessel, Quote, Policy, Coverage, High-Risk Areas (HRA), User Profiles  
- **Area-Specific Logic**: Coverage selection, pricing, and duration per High-Risk Area
- **Complex Workflows**: Area-specific quote wizard, automatic pricing engine, internal KYC workflows
- **Multi-User Platform**: Ship owners, ship brokers, cargo owners + admin users with controlled registration
- **SLA Requirements**: 48-hour standardization across all quotes
- **Internal Operations**: Manual data entry and management by internal team
- **Compliance**: Internal KYC workflows, sanctions screening, audit trails
- **Current VanguardAI Integration**: Existing apps/backend/, apps/frontend/, database/, devops/ structure
- **Nx v20+ Compliance**: Modern plugin system with automatic task inference

---

## Option 1: Domain-Driven Architecture (RECOMMENDED)

**Philosophy**: Organize by business domains first, then by technical concerns within each domain

### Folder Structure
```
vanguardai/                           # Nx workspace root
├── apps/
│   ├── maritime-platform/           # Main React application (TypeScript + Vite)
│   │   ├── src/pages/              # TanStack Router pages
│   │   ├── vite.config.ts          # Vite configuration
│   │   └── project.json            # Nx project config
│   ├── admin-dashboard/             # Admin interface (React + TypeScript)
│   │   └── src/                    # Admin-specific UI components
│   ├── storybook/                   # Separate deployable Storybook app (Nx v20+ pattern)
│   │   ├── .storybook/             # Storybook configuration
│   │   ├── stories/                # Component stories
│   │   ├── project.json            # Nx Storybook project config
│   │   └── package.json            # Storybook dependencies
│   └── api-gateway/                 # FastAPI backend (Python 3.12 + Poetry)
│       ├── app/
│       │   ├── features/           # Domain features (vessels, quotes, etc.)
│       │   ├── shared/             # Shared backend utilities
│       │   ├── infrastructure/     # Database, auth, external services
│       │   └── main.py             # FastAPI app entry point
│       ├── tests/                  # Backend tests
│       ├── pyproject.toml          # Poetry dependencies
│       ├── alembic.ini             # Database migration config
│       └── project.json            # Nx project config (Python integration)
├── libs/
│   ├── maritime/                   # Maritime insurance domain
│   │   ├── vessels/
│   │   │   ├── feature/           # Fleet registration, vessel management
│   │   │   ├── data-access/       # Vessel API clients & Equasis lookup
│   │   │   ├── model/             # Vessel entities & IMO validation
│   │   │   └── ui/                # Vessel-specific UI components
│   │   ├── quotes/
│   │   │   ├── feature/           # Quote wizard with area-specific logic
│   │   │   ├── data-access/       # Quote API & automatic pricing
│   │   │   ├── model/             # Quote entities & area-specific validation
│   │   │   └── ui/                # Quote wizard components
│   │   ├── coverage/
│   │   │   ├── feature/           # Area-specific coverage management
│   │   │   ├── data-access/       # Coverage API & HRA detection
│   │   │   ├── model/             # Coverage types, HRA entities
│   │   │   └── ui/                # Coverage selection components
│   │   ├── policies/
│   │   │   ├── feature/           # Policy management & binding
│   │   │   ├── data-access/       # Policy API & document management
│   │   │   ├── model/             # Policy entities & area-specific rules
│   │   │   └── ui/                # Policy management components
│   │   └── users/
│   │       ├── feature/           # User management for ship owners, brokers, cargo owners
│   │       ├── data-access/       # User API & internal KYC workflows
│   │       ├── model/             # User entities & role management
│   │       └── ui/                # User portal components
│   ├── shared/                     # Cross-domain shared code
│   │   ├── ui/                    # Design system components
│   │   ├── data-access/           # Common API utilities
│   │   ├── utils/                 # Utility functions
│   │   ├── types/                 # Global TypeScript types
│   │   └── validation/            # Shared Zod schemas
│   ├── compliance/                 # Maritime compliance features
│   │   ├── sanctions/
│   │   │   ├── feature/           # Sanctions screening workflows
│   │   │   ├── data-access/       # Sanctions API & screening
│   │   │   └── model/             # Sanctions entities & rules
│   │   ├── kyc/
│   │   │   ├── feature/           # KYC document workflows
│   │   │   ├── data-access/       # KYC API & document processing
│   │   │   └── model/             # KYC entities & validation
│   │   └── audit/
│   │       ├── feature/           # Audit trail management
│   │       ├── data-access/       # Audit logging API
│   │       └── model/             # Audit entities & reporting
│   └── infrastructure/             # Platform concerns (TypeScript)
│       ├── auth/                  # WorkOS authentication utilities
│       ├── notifications/         # System notification management
│       └── monitoring/            # Performance monitoring utilities
├── database/
│   ├── migrations/                # Alembic migration files (.py)
│   └── seeds/                     # Database seed data (.py)
├── devops/                          # AWS CDK Infrastructure (from infrastructure decision)
│   ├── cdk/                        # AWS CDK infrastructure as code
│   │   ├── lib/                    # CDK construct libraries
│   │   │   ├── app-runner-stack.ts # App Runner serverless containers
│   │   │   ├── aurora-stack.ts     # Aurora Serverless v2 database
│   │   │   ├── cloudfront-stack.ts # S3 + CloudFront distribution
│   │   │   └── ephemeral-stack.ts  # PR preview environments ($12/month)
│   │   ├── bin/                    # CDK app entry points
│   │   ├── cdk.json               # CDK configuration
│   │   └── package.json            # CDK dependencies
│   ├── docker/
│   │   ├── Dockerfile.backend      # FastAPI production image
│   │   └── docker-compose.dev.yml  # Development services
│   └── scripts/
│       ├── deploy-ephemeral.sh     # Deploy PR environments
│       └── deploy-production.sh    # Production deployment
├── .github/
│   └── workflows/                  # GitHub Actions CI/CD (from testing decision)
│       ├── ci.yml                  # Main CI pipeline (Nx affected builds)
│       ├── test-backend.yml        # Python backend testing (pytest)
│       ├── test-frontend.yml       # React frontend testing (Vitest + Playwright)
│       ├── test-e2e.yml            # End-to-end testing (Playwright)
│       ├── deploy-staging.yml      # Staging deployment (Aurora Serverless)
│       └── deploy-production.yml   # Production deployment (App Runner + CloudFront)
├── tools/
│   ├── generators/                # Custom Nx generators
│   │   ├── maritime-feature/      # Generate maritime domain features
│   │   └── backend-feature/       # Generate FastAPI features
│   └── scripts/                   # Development and deployment scripts
│       ├── dev-hybrid.sh          # Hybrid development startup
│       ├── manage_db.py           # Database management
│       └── deploy.sh              # Deployment scripts
├── docs/                          # Project documentation
│   ├── architecture/              # Technical architecture docs
│   ├── api/                       # API documentation
│   └── deployment/                # Deployment guides
├── docker-compose.yml             # Local development environment
├── nx.json                        # Nx v20+ workspace configuration
├── package.json                   # Root package.json with workspaces
├── tsconfig.base.json             # Base TypeScript config with path mapping
├── vitest.workspace.ts            # Vitest workspace configuration (from testing decision)
├── .gitignore                     # Git ignore rules
└── README.md                      # Project overview
```

### Benefits
- **Maritime Domain Focus**: Each team member can specialize in specific maritime workflows
- **Business Alignment**: Structure perfectly matches maritime processes and user flows
- **Area-Specific Logic**: Natural organization for High-Risk Area coverage rules
- **Internal Operations**: Clear organization for manual data management and KYC workflows
- **Scalability**: Easy to add new coverage types, areas, or expand maritime products
- **Team Ownership**: Clear ownership boundaries for vessels, quotes, coverage, policies, users
- **Multi-User Optimization**: Structure optimized for ship owners, brokers, cargo owners, and admin users
- **Nx v20+ Integration**: Automatic task inference and modern plugin system
- **VanguardAI Compatibility**: Aligns with existing backend/frontend/database structure

### Drawbacks
- **Learning Curve**: Team needs to understand domain boundaries
- **Initial Complexity**: More folders and structure to navigate initially
- **Cross-Domain Dependencies**: Need careful management of shared concerns

### Cost Analysis
- **Migration Time**: 2-3 weeks to restructure existing code
- **Team Training**: 15 hours total for domain-driven principles
- **Long-term Maintenance**: Lower due to clear boundaries
- **Developer Onboarding**: Faster once structure is learned

### Implementation Strategy
```bash
# Initialize Nx workspace with v20+ preset
npx create-nx-workspace@latest vanguardai --preset=react-monorepo --packageManager=pnpm

# Generate React applications with Vite (auto-detected by Nx plugins)
nx g @nx/react:app maritime-platform --bundler=vite --routing --style=css
nx g @nx/react:app admin-dashboard --bundler=vite --routing --style=css

# Generate Storybook as separate deployable app (Nx v20+ pattern)
nx g @nx/storybook:configuration storybook --project-type=application

# Set up FastAPI backend (manual with Nx integration)
mkdir -p apps/api-gateway
cd apps/api-gateway
poetry init --no-interaction --dependency fastapi --dependency uvicorn
poetry add sqlalchemy alembic asyncpg pydantic-settings
poetry add --group dev pytest pytest-asyncio black ruff mypy

# Generate maritime domain libraries (v20+ approach)
nx g @nx/js:lib maritime-vessels --directory=libs/maritime/vessels --bundler=none
nx g @nx/js:lib maritime-quotes --directory=libs/maritime/quotes --bundler=none
nx g @nx/js:lib shared-ui --directory=libs/shared --bundler=none

# Set up infrastructure aligned with current VanguardAI
mkdir -p database/{migrations,seeds/{dev,test}}
mkdir -p devops/{cdk,docker,scripts}
mkdir -p .github/workflows
mkdir -p tools/{generators,scripts}
```

---

## Option 2: Technical Layer Architecture (ALTERNATIVE)

**Philosophy**: Organize by technical concerns first, then by features within each layer

### Folder Structure
```
vanguardai/
├── apps/
│   ├── web-app/                    # Main React application
│   ├── admin-dashboard/            # Admin interface
│   └── api-gateway/                # FastAPI backend
├── libs/
│   ├── features/                   # Business features
│   │   ├── policy-management/
│   │   ├── claims-processing/
│   │   ├── broker-competition/
│   │   ├── customer-portal/
│   │   └── compliance-dashboard/
│   ├── ui/                         # UI components
│   │   ├── design-system/
│   │   ├── forms/
│   │   ├── charts/
│   │   └── layouts/
│   ├── data-access/                # API clients & state
│   │   ├── api-client/
│   │   ├── websocket-client/
│   │   ├── cache/
│   │   └── state-management/
│   ├── models/                     # Data models & types
│   │   ├── insurance-entities/
│   │   ├── api-contracts/
│   │   └── validation-schemas/
│   ├── utils/                      # Utility functions
│   │   ├── formatters/
│   │   ├── validators/
│   │   └── helpers/
│   └── infrastructure/             # Platform concerns
│       ├── auth/
│       ├── logging/
│       ├── monitoring/
│       └── configuration/
├── tools/
└── docs/
```

### Benefits
- **Technical Clarity**: Clear separation of technical concerns
- **Reusability**: Easy to find and reuse components across features
- **Frontend Team Friendly**: Structure familiar to React developers
- **Simple Navigation**: Straightforward folder hierarchy

### Drawbacks
- **Business Logic Scattered**: Related business logic spread across layers
- **Cross-Feature Dependencies**: Harder to understand feature boundaries
- **Domain Knowledge**: Less alignment with insurance business processes
- **Maintenance Complexity**: Changes often require updates across multiple layers

### Cost Analysis
- **Migration Time**: 1.5-2 weeks (simpler restructuring)
- **Team Training**: 8 hours total for technical architecture
- **Long-term Maintenance**: Higher due to scattered business logic
- **Developer Onboarding**: Easier initial learning curve

---

## Option 3: Hybrid Domain-Technical Architecture (BALANCED)

**Philosophy**: Balance domain organization with technical layer clarity

### Folder Structure
```
vanguardai/
├── apps/
│   ├── web-app/                    # Main React application
│   ├── admin-dashboard/            # Admin interface
│   └── api-gateway/                # FastAPI backend
├── libs/
│   ├── domains/                    # Business domains
│   │   ├── insurance/
│   │   │   ├── policy-feature/
│   │   │   ├── claims-feature/
│   │   │   ├── broker-feature/
│   │   │   └── customer-feature/
│   │   └── compliance/
│   │       ├── audit-feature/
│   │       └── reporting-feature/
│   ├── shared/                     # Shared technical concerns
│   │   ├── ui/                    # Design system & components
│   │   ├── data-access/           # Common API utilities
│   │   ├── models/                # Shared types & entities
│   │   ├── utils/                 # Utility functions
│   │   └── validation/            # Shared validation schemas
│   ├── platform/                   # Platform-wide concerns
│   │   ├── auth/
│   │   ├── logging/
│   │   ├── monitoring/
│   │   └── websockets/
│   └── external/                   # Third-party integrations
│       ├── payment-providers/
│       ├── document-storage/
│       └── notification-services/
├── tools/
└── docs/
```

### Benefits
- **Balanced Approach**: Combines domain focus with technical clarity
- **Gradual Adoption**: Easier migration from current structure
- **Team Flexibility**: Accommodates both domain and technical thinking
- **Clear Separation**: Distinct areas for business and platform concerns

### Drawbacks
- **Compromise Solution**: May not fully optimize for either approach
- **Potential Confusion**: Mixed organizational principles
- **Inconsistent Patterns**: Risk of inconsistent organization over time

---

## Team-Specific Analysis

### Head of Engineering Perspective
- **Option 1 (Domain-Driven)**: ✅ Best for architectural oversight and business alignment
- **Option 2 (Technical)**: ⚠️ Familiar but may complicate business logic management
- **Option 3 (Hybrid)**: ✅ Good balance for team leadership and technical coordination

### Lead Frontend Developer Perspective
- **Option 1 (Domain-Driven)**: ⚠️ Learning curve but better long-term organization
- **Option 2 (Technical)**: ✅ Familiar structure, easy component reuse
- **Option 3 (Hybrid)**: ✅ Good compromise with clear UI separation

### Lead Backend Developer Perspective
- **Option 1 (Domain-Driven)**: ✅ Aligns with DDD patterns already used in FastAPI
- **Option 2 (Technical)**: ⚠️ May scatter business logic across layers
- **Option 3 (Hybrid)**: ✅ Maintains domain focus with technical clarity

### UI/UX Engineer Perspective
- **Option 1 (Domain-Driven)**: ⚠️ May complicate design system management
- **Option 2 (Technical)**: ✅ Clear UI component organization
- **Option 3 (Hybrid)**: ✅ Best of both worlds with dedicated shared/ui

---

## Maritime Domain Considerations

### Regulatory Compliance Requirements
- **Audit Trails**: Need clear organization for compliance features
- **Data Protection**: GDPR/CCPA compliance across all domains
- **Maritime Standards**: IMO compatibility and industry alignment

### Business Process Complexity
- **Area-Specific Quote Wizard**: Complex multi-step workflow with HRA configuration
- **Internal User Management**: KYC workflows with controlled registration
- **Policy Management**: Document management with area-specific rules

### Scalability Requirements
- **New Maritime Coverage**: Easy addition of new coverage types and areas
- **Team Growth**: Structure must support additional developers
- **Feature Expansion**: Accommodation of new maritime business requirements

---

## Migration Strategy Comparison

### Option 1 (Domain-Driven) Migration
**Phase 1 (Week 1)**:
- Analyze existing VanguardAI code for domain boundaries
- Create maritime domain-specific libraries
- Move vessel-related code to maritime/vessels domain

**Phase 2 (Week 2)**:
- Migrate quotes and coverage functionality
- Establish shared libraries for common concerns
- Update import paths and dependencies

**Phase 3 (Week 3)**:
- Implement compliance domain
- Optimize cross-domain communication
- Create custom generators for maritime patterns

### Option 2 (Technical) Migration
**Phase 1 (Week 1)**:
- Create technical layer libraries
- Move React components to ui layer
- Consolidate API clients in data-access

**Phase 2 (Week 2)**:
- Migrate business logic to features layer
- Update import paths and dependencies
- Test cross-layer communication

### Option 3 (Hybrid) Migration
**Phase 1 (Week 1)**:
- Create domain and shared folders
- Move major features to domain organization
- Establish shared technical libraries

**Phase 2 (Week 2)**:
- Refine domain boundaries
- Optimize shared library usage
- Update documentation and patterns

---

## Recommendation Matrix

| Criteria | Domain-Driven | Technical | Hybrid |
|----------|---------------|-----------|---------|
| **Business Alignment** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| **Team Learning Curve** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Long-term Maintainability** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Maritime Domain Fit** | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| **Developer Experience** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Migration Complexity** | ⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Scalability** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Regulatory Compliance** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## Recommendation Summary

**Primary Recommendation**: **Domain-Driven Architecture (Option 1)**

**Reasoning**:
- **Best Maritime Fit**: Structure aligns perfectly with maritime business processes
- **Long-term Value**: Superior maintainability and scalability for complex domain
- **VanguardAI Integration**: Natural evolution from current backend/frontend structure
- **Team Growth**: Structure supports adding domain specialists as team expands
- **Nx v20+ Benefits**: Modern plugin system with automatic task inference and enhanced AI integrations

**Alternative Option**: **Hybrid Domain-Technical (Option 3)** for teams preferring gradual transition

**Implementation Timeline**: 3 weeks with recommended phased approach and team training

---

## Decision Factors Summary

### Choose Domain-Driven Architecture If:
- ✅ Team commits to learning domain-driven principles
- ✅ Long-term maintainability is priority over short-term familiarity
- ✅ Maritime business complexity is primary concern
- ✅ Nx v20+ features and AI integrations are valuable
- ✅ Team size will grow and needs clear ownership boundaries

### Choose Technical Layer Architecture If:
- ✅ Team prefers familiar React/frontend patterns
- ✅ Technical reusability is more important than business alignment
- ✅ Faster migration with minimal learning curve required
- ✅ Simple business domain with limited complexity

### Choose Hybrid Architecture If:
- ✅ Team wants balance between domain focus and technical clarity
- ✅ Gradual transition from current structure preferred
- ✅ Mixed team preferences for organization patterns
- ✅ Flexibility for future architectural evolution desired

---

**Questions for Your Decision:**
1. How important is long-term maintainability vs. short-term migration ease?
2. Is the team willing to invest in learning domain-driven principles?
3. How critical is clear business domain separation for your workflows?
4. What are your preferences for handling regulatory compliance organization?

Please indicate your preferred folder structure option or any modifications you'd like to make to the recommended approach.