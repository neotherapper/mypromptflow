# Infrastructure Training Guide

## Maritime Insurance Application Infrastructure

This comprehensive training guide covers the modern infrastructure stack for the maritime insurance application, focusing on practical implementation and best practices.

---

## Table of Contents

1. [Infrastructure Overview](#infrastructure-overview)
2. [Development Environment Setup](#development-environment-setup)
3. [Maritime Insurance Deployment](#maritime-insurance-deployment)
4. [Advanced Techniques](#advanced-techniques)
5. [Best Practices](#best-practices)
6. [Hands-on Exercises](#hands-on-exercises)
7. [Competency Assessment](#competency-assessment)

---

## Infrastructure Overview

### Learning Objectives
- Understand the complete infrastructure stack
- Learn the benefits of each component
- Master the integration between services
- Implement security best practices

### Infrastructure Stack Components

#### 1. GitPod Professional - Cloud Development Environment
- **Purpose**: Instant, consistent development environments
- **Cost**: $50/month per developer
- **Key Features**:
  - Zero setup time for new developers
  - Pre-configured with all tools and dependencies
  - Browser-based VS Code experience
  - Shared workspaces for collaboration

#### 2. Railway - Backend Hosting Platform
- **Purpose**: Managed backend deployment for FastAPI
- **Cost**: $20/month base + usage
- **Key Features**:
  - Automatic deployments from GitHub
  - Built-in auto-scaling
  - Managed infrastructure with zero DevOps
  - Integrated health monitoring

#### 3. Vercel - Frontend Deployment Platform
- **Purpose**: Optimized React/Next.js hosting
- **Cost**: $20/month Pro plan
- **Key Features**:
  - Global CDN with 100+ edge locations
  - Preview deployments for every PR
  - Automatic optimization and caching
  - <100ms global loading times

#### 4. Neon PostgreSQL - Serverless Database
- **Purpose**: Database with Git-like branching
- **Cost**: $19/month + usage (~$30/month total)
- **Key Features**:
  - Database branching for isolated testing
  - Serverless scaling with auto-sleep
  - Point-in-time recovery
  - Connection pooling built-in

### Architecture Diagram
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    GitPod       │     │     GitHub      │     │   Claude AI     │
│  Development    │────▶│   Repository    │◀────│  Code Review    │
└─────────────────┘     └────────┬────────┘     └─────────────────┘
                                 │
                    ┌────────────┴────────────┐
                    ▼                         ▼
         ┌─────────────────┐         ┌─────────────────┐
         │     Vercel      │         │    Railway      │
         │  Frontend CDN   │         │  Backend API    │
         └─────────────────┘         └─────────────────┘
                    │                         │
                    └─────────┬───────────────┘
                              ▼
                    ┌─────────────────┐
                    │      Neon       │
                    │   PostgreSQL    │
                    └─────────────────┘
```

---

## Development Environment Setup

### Learning Objectives
- Configure GitPod workspace for maritime insurance project
- Set up environment variables securely
- Implement development workflows
- Master debugging and monitoring tools

### GitPod Workspace Configuration

#### Step 1: Create .gitpod.yml Configuration
```yaml
# .gitpod.yml
image: gitpod/workspace-full:latest

tasks:
  - name: Backend Setup
    init: |
      # Install Python dependencies
      cd apps/backend
      pip install -r requirements.txt
      
      # Set up database connection
      export DATABASE_URL=$DATABASE_URL_DEV
      
      # Run database migrations
      alembic upgrade head
    command: |
      # Start FastAPI development server
      uvicorn main:app --reload --host 0.0.0.0 --port 8000
      
  - name: Frontend Setup
    init: |
      # Install Node.js dependencies
      cd apps/frontend
      pnpm install
    command: |
      # Start React development server
      pnpm run dev

ports:
  - port: 3000
    onOpen: open-preview
    description: React Frontend
  - port: 8000
    onOpen: open-preview
    description: FastAPI Backend
  - port: 5173
    onOpen: ignore
    description: Vite HMR

vscode:
  extensions:
    - ms-python.python
    - bradlc.vscode-tailwindcss
    - ms-vscode.vscode-typescript-next
    - dbaeumer.vscode-eslint
    - esbenp.prettier-vscode

github:
  prebuilds:
    master: true
    branches: true
    pullRequests: true
```

#### Step 2: Environment Variables Management
```bash
# GitPod environment variables (secure)
gp env DATABASE_URL_DEV=postgresql://user:pass@dev-branch.neon.tech/maritime
gp env VITE_API_URL=http://localhost:8000
gp env NODE_ENV=development
gp env PYTHONPATH=/workspace/apps/backend/src

# Project-specific variables
gp env MARITIME_INSURANCE_API_KEY=your-api-key
gp env QUOTE_ENGINE_VERSION=v2
gp env RISK_ASSESSMENT_MODEL=maritime-2024
```

#### Step 3: Custom Docker Image for Maritime Insurance
```dockerfile
# .gitpod.Dockerfile
FROM gitpod/workspace-full:latest

# Install maritime insurance specific tools
RUN pip install maritime-risk-calculator==2.1.0
RUN npm install -g @maritime/quote-validator

# Install database tools
RUN brew install postgresql-client
RUN pip install pgcli

# Configure git for the team
RUN git config --global init.defaultBranch main
RUN git config --global pull.rebase true
```

### Development Workflow Implementation

#### Daily Developer Experience
1. **Morning Startup** (30 seconds)
   ```bash
   # Click GitPod button in GitHub repo
   # Environment ready with all services running
   ```

2. **Feature Development**
   ```bash
   # Create feature branch
   git checkout -b feature/marine-cargo-quotes
   
   # Neon automatically creates database branch
   export DATABASE_URL=$(neon connection-string pr-$PR_NUMBER)
   
   # Develop with isolated database
   python manage.py test quotes.test_cargo_quotes
   ```

3. **Testing Integration**
   ```python
   # test_maritime_quotes.py
   import pytest
   from app.services import QuoteCalculator
   
   def test_cargo_insurance_quote():
       calculator = QuoteCalculator()
       quote = calculator.calculate_cargo_quote(
           vessel_type="container_ship",
           cargo_value=1000000,
           route="singapore_rotterdam",
           duration_days=30
       )
       assert quote.premium > 0
       assert quote.coverage_limit == 1000000
   ```

### Debugging and Monitoring

#### Backend Debugging (FastAPI)
```python
# Enable debug mode in development
import logging
from fastapi import FastAPI

app = FastAPI(debug=True)
logging.basicConfig(level=logging.DEBUG)

@app.exception_handler(Exception)
async def debug_exception_handler(request, exc):
    logging.error(f"Unhandled exception: {exc}", exc_info=True)
    return {"error": str(exc), "path": request.url.path}
```

#### Frontend Debugging (React)
```typescript
// Enable React DevTools
if (import.meta.env.DEV) {
  // Enable React Query DevTools
  import('@tanstack/react-query-devtools').then(({ ReactQueryDevtools }) => {
    window.ReactQueryDevtools = ReactQueryDevtools;
  });
}

// Custom error boundary for maritime insurance
class MaritimeErrorBoundary extends React.Component {
  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('Maritime App Error:', error, errorInfo);
    // Send to monitoring service
    if (window.Sentry) {
      window.Sentry.captureException(error);
    }
  }
}
```

---

## Maritime Insurance Deployment

### Learning Objectives
- Design and implement application architecture
- Execute database design and migrations
- Deploy APIs with optimal strategies
- Optimize frontend performance

### Application Architecture

#### Microservices Design
```
┌─────────────────────────────────────────────────────────┐
│                   API Gateway (Railway)                  │
├─────────────┬─────────────┬─────────────┬──────────────┤
│   Quote     │   Policy    │    Risk     │   Claims     │
│  Service    │  Service    │ Assessment  │  Service     │
└─────────────┴─────────────┴─────────────┴──────────────┘
                              │
                    ┌─────────┴─────────┐
                    │   Neon PostgreSQL │
                    │  (Branch per PR)  │
                    └───────────────────┘
```

#### FastAPI Application Structure
```python
# apps/backend/src/main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import get_db
from .routers import quotes, policies, claims
from .middleware import RateLimitMiddleware

app = FastAPI(
    title="Maritime Insurance API",
    description="API for maritime insurance quotes and policies",
    version="2.0.0"
)

# CORS configuration for Vercel frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://maritime-insurance.vercel.app",
        "https://staging-*.vercel.app",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting for API protection
app.add_middleware(RateLimitMiddleware, calls=100, period=60)

# Include routers
app.include_router(quotes.router, prefix="/api/quotes", tags=["quotes"])
app.include_router(policies.router, prefix="/api/policies", tags=["policies"])
app.include_router(claims.router, prefix="/api/claims", tags=["claims"])

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "maritime-insurance-api",
        "version": "2.0.0"
    }
```

### Database Design and Migrations

#### Maritime Insurance Schema
```sql
-- Core tables for maritime insurance
CREATE TABLE vessels (
    id SERIAL PRIMARY KEY,
    imo_number VARCHAR(10) UNIQUE NOT NULL,
    vessel_name VARCHAR(200) NOT NULL,
    vessel_type VARCHAR(50) NOT NULL,
    gross_tonnage INTEGER NOT NULL,
    year_built INTEGER NOT NULL,
    flag_state VARCHAR(3) NOT NULL,
    class_society VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE cargo_types (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    risk_category VARCHAR(20) NOT NULL, -- 'low', 'medium', 'high', 'hazardous'
    base_rate DECIMAL(6,4) NOT NULL,
    special_handling JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE routes (
    id SERIAL PRIMARY KEY,
    origin_port VARCHAR(5) NOT NULL, -- UN/LOCODE
    destination_port VARCHAR(5) NOT NULL,
    distance_nm INTEGER NOT NULL, -- nautical miles
    transit_days INTEGER NOT NULL,
    risk_zones JSONB, -- array of risk zone codes
    seasonal_factors JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE quotes (
    id SERIAL PRIMARY KEY,
    quote_number VARCHAR(20) UNIQUE NOT NULL,
    vessel_id INTEGER REFERENCES vessels(id),
    cargo_type_id INTEGER REFERENCES cargo_types(id),
    route_id INTEGER REFERENCES routes(id),
    cargo_value DECIMAL(15,2) NOT NULL,
    coverage_amount DECIMAL(15,2) NOT NULL,
    deductible DECIMAL(10,2) NOT NULL,
    premium DECIMAL(10,2) NOT NULL,
    validity_days INTEGER DEFAULT 30,
    status VARCHAR(20) DEFAULT 'draft',
    created_by VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP NOT NULL
);

CREATE TABLE policies (
    id SERIAL PRIMARY KEY,
    policy_number VARCHAR(30) UNIQUE NOT NULL,
    quote_id INTEGER REFERENCES quotes(id),
    effective_date DATE NOT NULL,
    expiry_date DATE NOT NULL,
    premium_paid DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(20),
    status VARCHAR(20) DEFAULT 'active',
    terms_conditions JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_vessels_imo ON vessels(imo_number);
CREATE INDEX idx_quotes_status ON quotes(status);
CREATE INDEX idx_quotes_expires ON quotes(expires_at);
CREATE INDEX idx_policies_status ON policies(status);
CREATE INDEX idx_policies_expiry ON policies(expiry_date);
```

#### Database Migration Strategy
```python
# alembic/versions/001_initial_maritime_schema.py
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    # Create enum types
    op.execute("CREATE TYPE vessel_type AS ENUM ('container', 'tanker', 'bulk_carrier', 'general_cargo')")
    op.execute("CREATE TYPE risk_category AS ENUM ('low', 'medium', 'high', 'hazardous')")
    
    # Create vessels table
    op.create_table('vessels',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('imo_number', sa.String(10), nullable=False),
        sa.Column('vessel_name', sa.String(200), nullable=False),
        sa.Column('vessel_type', postgresql.ENUM('container', 'tanker', 'bulk_carrier', 'general_cargo', name='vessel_type'), nullable=False),
        sa.Column('gross_tonnage', sa.Integer(), nullable=False),
        sa.Column('year_built', sa.Integer(), nullable=False),
        sa.Column('flag_state', sa.String(3), nullable=False),
        sa.Column('class_society', sa.String(100), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('imo_number')
    )
    
    # Create indexes
    op.create_index('idx_vessels_imo', 'vessels', ['imo_number'])
    op.create_index('idx_vessels_type', 'vessels', ['vessel_type'])

def downgrade():
    op.drop_table('vessels')
    op.execute("DROP TYPE vessel_type")
    op.execute("DROP TYPE risk_category")
```

### API Deployment Strategies

#### Railway Deployment Configuration
```toml
# railway.toml
[build]
builder = "NIXPACKS"
buildCommand = "pip install -r requirements.txt"

[deploy]
startCommand = "uvicorn src.main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
healthcheckTimeout = 30
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 3

[[services]]
name = "maritime-api"
envVars = { ENVIRONMENT = "production" }

[environments.production]
domains = ["api.maritime-insurance.com"]
region = "us-west"

[environments.staging]
domains = ["staging-api.maritime-insurance.com"]
region = "us-west"
```

#### Auto-scaling Configuration
```python
# src/scaling.py
from fastapi import Request
import time
import psutil

class AutoScalingMiddleware:
    def __init__(self, app):
        self.app = app
        self.request_count = 0
        self.start_time = time.time()
        
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            self.request_count += 1
            
            # Check if scaling is needed
            cpu_percent = psutil.cpu_percent(interval=1)
            memory_percent = psutil.virtual_memory().percent
            
            if cpu_percent > 80 or memory_percent > 85:
                # Trigger Railway scaling via API
                await self.trigger_scaling()
                
        await self.app(scope, receive, send)
    
    async def trigger_scaling(self):
        # Railway auto-scaling API integration
        pass
```

### Frontend Optimization

#### Vercel Deployment Configuration
```json
// vercel.json
{
  "version": 2,
  "builds": [
    {
      "src": "package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "dist"
      }
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "https://api.maritime-insurance.com/$1"
    },
    {
      "handle": "filesystem"
    },
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ],
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "s-maxage=60, stale-while-revalidate" }
      ]
    },
    {
      "source": "/assets/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
      ]
    }
  ]
}
```

#### Performance Optimization Techniques
```typescript
// Lazy loading for maritime insurance modules
const QuoteGenerator = lazy(() => import('./modules/QuoteGenerator'));
const PolicyManager = lazy(() => import('./modules/PolicyManager'));
const ClaimsPortal = lazy(() => import('./modules/ClaimsPortal'));

// Image optimization for vessel photos
import { Image } from '@vercel/image';

export const VesselPhoto: React.FC<{ vessel: Vessel }> = ({ vessel }) => {
  return (
    <Image
      src={vessel.photoUrl}
      alt={`${vessel.name} - ${vessel.type}`}
      width={400}
      height={300}
      loading="lazy"
      placeholder="blur"
      blurDataURL={vessel.thumbnailUrl}
    />
  );
};

// API request caching
import { useQuery } from '@tanstack/react-query';

export const useVesselData = (imoNumber: string) => {
  return useQuery({
    queryKey: ['vessel', imoNumber],
    queryFn: () => fetchVesselData(imoNumber),
    staleTime: 5 * 60 * 1000, // 5 minutes
    cacheTime: 10 * 60 * 1000, // 10 minutes
  });
};
```

---

## Advanced Techniques

### Learning Objectives
- Implement auto-scaling strategies
- Optimize application performance
- Apply security best practices
- Configure monitoring and alerting

### Auto-scaling Configuration

#### Railway Auto-scaling
```python
# railway_scaling.py
import os
import requests
from typing import Dict, Any

class RailwayScaler:
    def __init__(self):
        self.api_token = os.getenv('RAILWAY_API_TOKEN')
        self.project_id = os.getenv('RAILWAY_PROJECT_ID')
        self.service_id = os.getenv('RAILWAY_SERVICE_ID')
        
    def get_current_metrics(self) -> Dict[str, Any]:
        """Fetch current service metrics from Railway"""
        headers = {'Authorization': f'Bearer {self.api_token}'}
        response = requests.get(
            f'https://api.railway.app/v1/projects/{self.project_id}/services/{self.service_id}/metrics',
            headers=headers
        )
        return response.json()
    
    def scale_service(self, replicas: int) -> bool:
        """Scale Railway service to specified number of replicas"""
        headers = {'Authorization': f'Bearer {self.api_token}'}
        data = {
            'replicas': replicas,
            'cpu': '1000m',  # 1 CPU per replica
            'memory': '1Gi'   # 1GB RAM per replica
        }
        response = requests.patch(
            f'https://api.railway.app/v1/projects/{self.project_id}/services/{self.service_id}/scale',
            headers=headers,
            json=data
        )
        return response.status_code == 200
    
    def auto_scale_based_on_load(self):
        """Automatically scale based on current load"""
        metrics = self.get_current_metrics()
        cpu_usage = metrics['cpu']['usage']
        memory_usage = metrics['memory']['usage']
        current_replicas = metrics['replicas']
        
        # Scaling logic for maritime insurance peak times
        if cpu_usage > 80 or memory_usage > 85:
            new_replicas = min(current_replicas + 1, 10)  # Max 10 replicas
            self.scale_service(new_replicas)
        elif cpu_usage < 30 and memory_usage < 40 and current_replicas > 1:
            new_replicas = max(current_replicas - 1, 1)  # Min 1 replica
            self.scale_service(new_replicas)
```

#### Neon Database Auto-scaling
```sql
-- Configure Neon autoscaling parameters
ALTER DATABASE maritime_insurance SET neon.autoscaling_max_cu = 4;
ALTER DATABASE maritime_insurance SET neon.autoscaling_min_cu = 0.25;

-- Create connection pooling configuration
CREATE EXTENSION IF NOT EXISTS pgbouncer;

-- Configure connection limits based on workload
ALTER SYSTEM SET max_connections = 200;
ALTER SYSTEM SET shared_preload_libraries = 'pg_stat_statements';
```

### Performance Optimization

#### Backend Performance Optimization
```python
# Implement caching for frequently accessed data
from functools import lru_cache
from redis import Redis
import json

redis_client = Redis.from_url(os.getenv('REDIS_URL'))

class MaritimeCache:
    @staticmethod
    def cache_key(prefix: str, *args) -> str:
        return f"maritime:{prefix}:{':'.join(map(str, args))}"
    
    @staticmethod
    async def get_or_set(key: str, func, ttl: int = 300):
        """Get from cache or compute and set"""
        cached = redis_client.get(key)
        if cached:
            return json.loads(cached)
        
        result = await func()
        redis_client.setex(key, ttl, json.dumps(result))
        return result

# Use caching for vessel data
@router.get("/vessels/{imo_number}")
async def get_vessel(imo_number: str, db: Session = Depends(get_db)):
    cache_key = MaritimeCache.cache_key("vessel", imo_number)
    
    async def fetch_vessel():
        vessel = db.query(Vessel).filter(Vessel.imo_number == imo_number).first()
        return vessel.dict() if vessel else None
    
    return await MaritimeCache.get_or_set(cache_key, fetch_vessel, ttl=3600)

# Database query optimization
class OptimizedQueries:
    @staticmethod
    def get_active_policies_with_vessels(db: Session):
        """Optimized query with eager loading"""
        return db.query(Policy)\
            .options(joinedload(Policy.quote))\
            .options(joinedload(Policy.quote.vessel))\
            .filter(Policy.status == 'active')\
            .filter(Policy.expiry_date > datetime.now())\
            .all()
```

#### Frontend Performance Optimization
```typescript
// Implement virtual scrolling for large lists
import { VirtualList } from '@tanstack/react-virtual';

export const PolicyList: React.FC<{ policies: Policy[] }> = ({ policies }) => {
  const parentRef = useRef<HTMLDivElement>(null);
  
  const virtualizer = useVirtualizer({
    count: policies.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 80,
    overscan: 5,
  });
  
  return (
    <div ref={parentRef} className="h-[600px] overflow-auto">
      <div style={{ height: `${virtualizer.getTotalSize()}px` }}>
        {virtualizer.getVirtualItems().map((virtualItem) => (
          <div
            key={virtualItem.key}
            style={{
              position: 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: `${virtualItem.size}px`,
              transform: `translateY(${virtualItem.start}px)`,
            }}
          >
            <PolicyCard policy={policies[virtualItem.index]} />
          </div>
        ))}
      </div>
    </div>
  );
};

// Optimize bundle size with code splitting
const routes = [
  {
    path: '/quotes',
    component: lazy(() => import('./pages/Quotes')),
  },
  {
    path: '/policies',
    component: lazy(() => import('./pages/Policies')),
  },
  {
    path: '/claims',
    component: lazy(() => import('./pages/Claims')),
  },
];
```

### Security Best Practices

#### API Security Implementation
```python
# Implement comprehensive security measures
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
import secrets

security = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class SecurityConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_urlsafe(32))
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
class AuthService:
    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=SecurityConfig.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SecurityConfig.SECRET_KEY, algorithm=SecurityConfig.ALGORITHM)
    
    @staticmethod
    async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
        token = credentials.credentials
        try:
            payload = jwt.decode(token, SecurityConfig.SECRET_KEY, algorithms=[SecurityConfig.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=401, detail="Invalid authentication credentials")
            return username
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")

# Rate limiting implementation
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/api/quotes", dependencies=[Depends(verify_token)])
@limiter.limit("10/minute")
async def create_quote(request: Request, quote: QuoteRequest, db: Session = Depends(get_db)):
    # Quote creation logic with security
    pass
```

#### Database Security
```sql
-- Implement row-level security for multi-tenant maritime insurance
CREATE POLICY tenant_isolation ON policies
    FOR ALL
    USING (tenant_id = current_setting('app.current_tenant')::INTEGER);

-- Enable row-level security
ALTER TABLE policies ENABLE ROW LEVEL SECURITY;

-- Create secure views for reporting
CREATE VIEW public_vessel_stats AS
SELECT 
    vessel_type,
    COUNT(*) as vessel_count,
    AVG(gross_tonnage) as avg_tonnage
FROM vessels
WHERE status = 'active'
GROUP BY vessel_type
WITH CHECK OPTION;

-- Audit logging
CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(50),
    action VARCHAR(10),
    user_id INTEGER,
    changed_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION audit_trigger_function()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_log (table_name, action, user_id, changed_data)
    VALUES (TG_TABLE_NAME, TG_OP, current_setting('app.current_user')::INTEGER, row_to_json(NEW));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
```

### Monitoring and Alerting

#### Application Monitoring Setup
```python
# Integrate Sentry for error tracking
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[
        FastApiIntegration(transaction_style='endpoint'),
        SqlalchemyIntegration(),
    ],
    traces_sample_rate=0.1,
    environment=os.getenv('ENVIRONMENT', 'development'),
    release=os.getenv('GIT_COMMIT_SHA', 'unknown'),
)

# Custom metrics collection
from prometheus_client import Counter, Histogram, generate_latest
import time

# Define metrics
quote_requests = Counter('maritime_quote_requests_total', 'Total quote requests')
quote_processing_time = Histogram('maritime_quote_processing_seconds', 'Quote processing time')
policy_conversions = Counter('maritime_policy_conversions_total', 'Total policy conversions')

@app.get("/metrics")
async def metrics():
    return Response(content=generate_latest(), media_type="text/plain")

# Use metrics in endpoints
@app.post("/api/quotes")
async def create_quote(quote: QuoteRequest):
    quote_requests.inc()
    start_time = time.time()
    
    try:
        # Process quote
        result = await process_quote(quote)
        return result
    finally:
        quote_processing_time.observe(time.time() - start_time)
```

#### Infrastructure Monitoring
```yaml
# monitoring/alerts.yml
alerts:
  - name: HighCPUUsage
    condition: cpu_usage > 80
    duration: 5m
    severity: warning
    notification:
      - email: ops@maritime-insurance.com
      - slack: #infrastructure-alerts
      
  - name: DatabaseConnectionPoolExhausted
    condition: connection_pool_usage > 90
    duration: 2m
    severity: critical
    notification:
      - pagerduty: infrastructure-team
      
  - name: HighErrorRate
    condition: error_rate > 5
    duration: 3m
    severity: critical
    notification:
      - email: engineering@maritime-insurance.com
      - slack: #critical-alerts
      
  - name: SlowAPIResponse
    condition: p95_response_time > 2000
    duration: 5m
    severity: warning
    notification:
      - slack: #performance-alerts
```

---

## Best Practices

### Learning Objectives
- Optimize infrastructure costs
- Implement security considerations
- Foster team collaboration
- Troubleshoot common issues effectively

### Cost Optimization

#### Resource Monitoring and Optimization
```python
# Cost tracking automation
import boto3
from datetime import datetime, timedelta

class InfrastructureCostMonitor:
    def __init__(self):
        self.services = {
            'gitpod': {'base_cost': 200, 'per_hour': 0},
            'railway': {'base_cost': 20, 'per_gb_hour': 0.20},
            'vercel': {'base_cost': 20, 'per_gb_bandwidth': 0.40},
            'neon': {'base_cost': 19, 'per_gb_storage': 0.15, 'per_compute_hour': 0.16}
        }
    
    def calculate_monthly_cost(self, usage_data):
        total_cost = 0
        
        # GitPod (fixed cost)
        total_cost += self.services['gitpod']['base_cost']
        
        # Railway (base + compute)
        railway_compute = usage_data['railway_compute_hours'] * self.services['railway']['per_gb_hour']
        total_cost += self.services['railway']['base_cost'] + railway_compute
        
        # Vercel (base + bandwidth)
        vercel_bandwidth = usage_data['vercel_bandwidth_gb'] * self.services['vercel']['per_gb_bandwidth']
        total_cost += self.services['vercel']['base_cost'] + vercel_bandwidth
        
        # Neon (base + storage + compute)
        neon_storage = usage_data['neon_storage_gb'] * self.services['neon']['per_gb_storage']
        neon_compute = usage_data['neon_compute_hours'] * self.services['neon']['per_compute_hour']
        total_cost += self.services['neon']['base_cost'] + neon_storage + neon_compute
        
        return total_cost
    
    def generate_cost_report(self, usage_data):
        return {
            'total_monthly_cost': self.calculate_monthly_cost(usage_data),
            'breakdown': self.get_service_breakdown(usage_data),
            'optimization_suggestions': self.get_optimization_suggestions(usage_data)
        }
    
    def get_optimization_suggestions(self, usage_data):
        suggestions = []
        
        if usage_data['vercel_bandwidth_gb'] > 50:
            suggestions.append("Consider implementing more aggressive caching to reduce bandwidth costs")
        
        if usage_data['neon_compute_hours'] > 500:
            suggestions.append("Review database queries for optimization opportunities")
        
        if usage_data['railway_compute_hours'] > 700:
            suggestions.append("Consider implementing auto-scaling schedules based on traffic patterns")
        
        return suggestions
```

#### Cost-Effective Scaling Strategies
```python
# Implement time-based scaling for predictable patterns
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler()

# Scale down during off-peak hours (maritime insurance typically has business hours patterns)
@scheduler.scheduled_job('cron', hour=20, minute=0)  # 8 PM
async def scale_down_evening():
    scaler = RailwayScaler()
    scaler.scale_service(replicas=1)  # Minimum replicas
    
    # Also scale down database
    await execute_sql("ALTER DATABASE maritime_insurance SET neon.autoscaling_max_cu = 1")

@scheduler.scheduled_job('cron', hour=7, minute=0)  # 7 AM
async def scale_up_morning():
    scaler = RailwayScaler()
    scaler.scale_service(replicas=3)  # Normal business hours capacity
    
    # Scale up database
    await execute_sql("ALTER DATABASE maritime_insurance SET neon.autoscaling_max_cu = 4")

# Start scheduler
scheduler.start()
```

### Security Considerations

#### Comprehensive Security Implementation
```python
# Security middleware stack
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware

# HTTPS enforcement
app.add_middleware(HTTPSRedirectMiddleware)

# Host validation
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["api.maritime-insurance.com", "*.maritime-insurance.com"]
)

# SQL injection prevention with parameterized queries
from sqlalchemy import text

class SecureQueries:
    @staticmethod
    def get_vessel_by_imo(db: Session, imo_number: str):
        # Safe parameterized query
        query = text("""
            SELECT * FROM vessels 
            WHERE imo_number = :imo_number 
            AND status = 'active'
        """)
        result = db.execute(query, {"imo_number": imo_number})
        return result.fetchone()
    
    @staticmethod
    def search_policies(db: Session, search_term: str):
        # Prevent SQL injection with proper escaping
        safe_search = f"%{search_term.replace('%', '\\%').replace('_', '\\_')}%"
        return db.query(Policy).filter(
            Policy.policy_number.ilike(safe_search)
        ).all()

# Input validation
from pydantic import BaseModel, validator, constr

class VesselInput(BaseModel):
    imo_number: constr(regex=r'^IMO\d{7}$')
    vessel_name: constr(min_length=1, max_length=200)
    gross_tonnage: int
    
    @validator('gross_tonnage')
    def validate_tonnage(cls, v):
        if v < 100 or v > 500000:
            raise ValueError('Gross tonnage must be between 100 and 500,000')
        return v
```

#### Data Protection and Compliance
```python
# GDPR compliance for maritime insurance data
from cryptography.fernet import Fernet
import hashlib

class DataProtection:
    def __init__(self):
        self.encryption_key = os.getenv('ENCRYPTION_KEY').encode()
        self.cipher_suite = Fernet(self.encryption_key)
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive information like policy holder details"""
        return self.cipher_suite.encrypt(data.encode()).decode()
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive information"""
        return self.cipher_suite.decrypt(encrypted_data.encode()).decode()
    
    def anonymize_email(self, email: str) -> str:
        """Anonymize email for analytics while maintaining uniqueness"""
        local, domain = email.split('@')
        anonymized_local = hashlib.sha256(local.encode()).hexdigest()[:8]
        return f"{anonymized_local}@{domain}"

# Audit trail for compliance
@app.middleware("http")
async def audit_middleware(request: Request, call_next):
    start_time = time.time()
    
    # Log request
    audit_entry = {
        "timestamp": datetime.utcnow(),
        "method": request.method,
        "path": request.url.path,
        "user_id": request.headers.get("user-id"),
        "ip_address": request.client.host
    }
    
    response = await call_next(request)
    
    # Log response
    audit_entry["status_code"] = response.status_code
    audit_entry["response_time"] = time.time() - start_time
    
    # Store audit log
    await store_audit_log(audit_entry)
    
    return response
```

### Team Collaboration

#### Development Workflow Best Practices
```yaml
# .github/PULL_REQUEST_TEMPLATE.md
## Maritime Insurance PR Checklist

### Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to change)
- [ ] Database migration (schema changes)

### Testing
- [ ] Unit tests pass locally
- [ ] Integration tests pass on GitPod
- [ ] Tested on preview deployment (Vercel URL: )
- [ ] Database migrations tested on Neon branch

### Performance
- [ ] No N+1 queries introduced
- [ ] API response time < 200ms for critical endpoints
- [ ] Frontend bundle size impact documented

### Security
- [ ] Input validation implemented
- [ ] Authentication/authorization checked
- [ ] No sensitive data in logs

### Documentation
- [ ] API documentation updated
- [ ] README updated if needed
- [ ] Inline comments for complex logic

### Deployment
- [ ] Environment variables documented
- [ ] Migration rollback plan documented
- [ ] Feature flags configured if needed

## Preview Links
- Frontend: https://pr-{{PR_NUMBER}}-maritime.vercel.app
- API Docs: https://pr-{{PR_NUMBER}}-api.railway.app/docs
- Database Branch: pr-{{PR_NUMBER}}
```

#### Communication Standards
```typescript
// Standardized error messages for better debugging
export class MaritimeError extends Error {
  constructor(
    public code: string,
    public message: string,
    public details?: any,
    public statusCode: number = 500
  ) {
    super(message);
    this.name = 'MaritimeError';
  }
}

// Error codes enum
export enum ErrorCodes {
  // Quote errors
  QUOTE_INVALID_VESSEL = 'QUOTE_001',
  QUOTE_ROUTE_UNAVAILABLE = 'QUOTE_002',
  QUOTE_CARGO_RESTRICTED = 'QUOTE_003',
  
  // Policy errors
  POLICY_EXPIRED = 'POLICY_001',
  POLICY_DUPLICATE = 'POLICY_002',
  
  // System errors
  DATABASE_CONNECTION = 'SYSTEM_001',
  EXTERNAL_SERVICE = 'SYSTEM_002',
}

// Usage
throw new MaritimeError(
  ErrorCodes.QUOTE_INVALID_VESSEL,
  'Vessel IMO number not found in registry',
  { imo_number: 'IMO1234567' },
  400
);
```

### Troubleshooting Common Issues

#### Issue Resolution Guide
```python
# Common issue detection and resolution
class TroubleshootingGuide:
    @staticmethod
    def diagnose_slow_queries(db: Session):
        """Identify and log slow database queries"""
        slow_queries = db.execute(text("""
            SELECT query, mean_exec_time, calls
            FROM pg_stat_statements
            WHERE mean_exec_time > 100
            ORDER BY mean_exec_time DESC
            LIMIT 10
        """)).fetchall()
        
        for query in slow_queries:
            logger.warning(f"Slow query detected: {query.query[:100]}... "
                         f"Avg time: {query.mean_exec_time}ms, Calls: {query.calls}")
        
        return slow_queries
    
    @staticmethod
    def check_connection_pool_health():
        """Monitor database connection pool status"""
        from sqlalchemy.pool import QueuePool
        
        if isinstance(engine.pool, QueuePool):
            return {
                'size': engine.pool.size(),
                'checked_in': engine.pool.checkedin(),
                'checked_out': engine.pool.checkedout(),
                'overflow': engine.pool.overflow(),
                'total': engine.pool.size() + engine.pool.overflow()
            }
    
    @staticmethod
    def verify_service_connectivity():
        """Check all external service connections"""
        services_status = {}
        
        # Check Neon database
        try:
            db.execute(text("SELECT 1"))
            services_status['neon_database'] = 'healthy'
        except Exception as e:
            services_status['neon_database'] = f'unhealthy: {str(e)}'
        
        # Check Railway API
        try:
            response = requests.get('https://api.railway.app/health', timeout=5)
            services_status['railway_api'] = 'healthy' if response.status_code == 200 else 'unhealthy'
        except Exception as e:
            services_status['railway_api'] = f'unhealthy: {str(e)}'
        
        # Check Vercel deployment
        try:
            response = requests.get('https://maritime-insurance.vercel.app/health', timeout=5)
            services_status['vercel_frontend'] = 'healthy' if response.status_code == 200 else 'unhealthy'
        except Exception as e:
            services_status['vercel_frontend'] = f'unhealthy: {str(e)}'
        
        return services_status
```

#### Common Issues and Solutions
```bash
# Issue: GitPod workspace won't start
# Solution: Check and update .gitpod.yml
gitpod validate  # Validates configuration
gitpod snapshot create  # Create snapshot for debugging

# Issue: Railway deployment failing
# Solution: Check build logs
railway logs --service=maritime-api --filter=error
railway run --service=maritime-api python -m pytest  # Run tests in Railway environment

# Issue: Vercel build errors
# Solution: Test build locally
vercel build --debug
vercel dev  # Test locally with Vercel environment

# Issue: Neon connection issues
# Solution: Verify connection string and SSL
neon connection-string --branch=main --ssl-mode=require
psql $(neon connection-string) -c "SELECT version();"

# Issue: High database latency
# Solution: Analyze query performance
psql $(neon connection-string) -c "
  SELECT query, mean_exec_time, calls 
  FROM pg_stat_statements 
  WHERE mean_exec_time > 100 
  ORDER BY mean_exec_time DESC 
  LIMIT 10;"
```

---

## Hands-on Exercises

### Exercise 1: Complete Infrastructure Setup
**Objective**: Set up the complete infrastructure stack for a new maritime insurance feature

**Tasks**:
1. Create a new GitPod workspace
2. Configure environment variables for all services
3. Deploy a simple quote calculator to Railway
4. Deploy the frontend to Vercel
5. Create a Neon database branch for testing

**Success Criteria**:
- All services accessible and integrated
- Quote calculator returns valid responses
- Frontend successfully calls backend API
- Database migrations run successfully

### Exercise 2: Implement Auto-scaling
**Objective**: Configure auto-scaling for peak maritime insurance periods

**Tasks**:
1. Implement CPU-based auto-scaling for Railway
2. Configure Neon compute scaling
3. Set up scheduled scaling for business hours
4. Create monitoring dashboards
5. Test scaling under load

**Success Criteria**:
- Services scale up under load
- Services scale down during quiet periods
- No service disruptions during scaling
- Cost remains within budget

### Exercise 3: Security Hardening
**Objective**: Implement comprehensive security for the maritime insurance application

**Tasks**:
1. Configure API rate limiting
2. Implement JWT authentication
3. Set up database row-level security
4. Configure HTTPS and security headers
5. Implement audit logging

**Success Criteria**:
- All API endpoints protected
- Authentication working correctly
- Database access properly restricted
- Security scan shows no vulnerabilities

### Exercise 4: Performance Optimization
**Objective**: Optimize application performance for global users

**Tasks**:
1. Implement Redis caching for vessel data
2. Optimize database queries with indexes
3. Configure CDN caching rules
4. Implement lazy loading in frontend
5. Set up performance monitoring

**Success Criteria**:
- API response time < 200ms
- Frontend load time < 2 seconds globally
- Database queries optimized
- Lighthouse score > 90

### Exercise 5: Disaster Recovery
**Objective**: Implement and test disaster recovery procedures

**Tasks**:
1. Create database backup strategy
2. Test point-in-time recovery
3. Implement health checks and failover
4. Document recovery procedures
5. Conduct disaster recovery drill

**Success Criteria**:
- Successful database restoration
- Service recovery < 15 minutes
- No data loss during recovery
- Clear documentation for team

---

## Competency Assessment

### Level 1: Foundation (Junior Developer)
**Required Skills**:
- [ ] Can create and access GitPod workspace
- [ ] Understands environment variables
- [ ] Can deploy simple changes to Railway/Vercel
- [ ] Can run database migrations
- [ ] Understands basic Git workflow

**Assessment Tasks**:
1. Set up development environment in GitPod
2. Make a simple frontend change and deploy
3. Add a new API endpoint
4. Create and run a database migration

### Level 2: Intermediate (Mid-level Developer)
**Required Skills**:
- [ ] Can configure complete infrastructure
- [ ] Implements basic security measures
- [ ] Troubleshoots common issues
- [ ] Optimizes simple performance issues
- [ ] Manages environment configurations

**Assessment Tasks**:
1. Set up new microservice with database
2. Implement authentication system
3. Optimize slow database queries
4. Configure monitoring and alerts

### Level 3: Advanced (Senior Developer)
**Required Skills**:
- [ ] Designs scalable architectures
- [ ] Implements advanced security
- [ ] Optimizes complex performance issues
- [ ] Manages infrastructure costs
- [ ] Mentors other developers

**Assessment Tasks**:
1. Design multi-region deployment strategy
2. Implement zero-downtime deployment
3. Create cost optimization plan
4. Build custom auto-scaling solution

### Level 4: Expert (Lead/Architect)
**Required Skills**:
- [ ] Architects complete solutions
- [ ] Defines infrastructure standards
- [ ] Leads disaster recovery planning
- [ ] Optimizes total cost of ownership
- [ ] Drives technology decisions

**Assessment Tasks**:
1. Create infrastructure roadmap
2. Design enterprise scaling strategy
3. Implement compliance framework
4. Lead architecture review board

### Certification Requirements
To achieve infrastructure certification, complete:
- All exercises for your level
- Pass written assessment (80% minimum)
- Complete practical project
- Demonstrate skills in production environment
- Receive peer review approval

---

## Additional Resources

### Documentation Links
- [GitPod Documentation](https://www.gitpod.io/docs)
- [Railway Documentation](https://docs.railway.app)
- [Vercel Documentation](https://vercel.com/docs)
- [Neon Documentation](https://neon.tech/docs)

### Community Support
- GitPod Discord: https://www.gitpod.io/chat
- Railway Discord: https://discord.gg/railway
- Vercel Discord: https://vercel.com/discord
- Neon Community: https://community.neon.tech

### Training Videos
- Infrastructure Setup Walkthrough
- Security Best Practices Workshop
- Performance Optimization Masterclass
- Disaster Recovery Simulation

### Next Steps
1. Complete hands-on exercises
2. Join infrastructure team meetings
3. Shadow senior developers
4. Contribute to infrastructure improvements
5. Share knowledge with team

---

**Remember**: Infrastructure is the foundation of our maritime insurance application. Master these concepts to build reliable, scalable, and secure systems that serve our global customers effectively.