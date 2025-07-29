# WorkOS Implementation Guide for Maritime Insurance Platform

## Overview

This comprehensive guide provides step-by-step instructions for implementing WorkOS AuthKit in the AI-SDLC maritime insurance platform. The implementation supports multi-tenant architecture with enterprise-grade security and maritime compliance requirements.

**Implementation Timeline**: 4 weeks  
**Technology Stack**: React/TypeScript frontend, FastAPI backend  
**Security**: SOC 2, GDPR, CCPA compliant with maritime audit logging  

## Table of Contents

1. [Prerequisites and Setup](#prerequisites-and-setup)
2. [WorkOS Account Configuration](#workos-account-configuration)
3. [Frontend Implementation (React/TypeScript)](#frontend-implementation-reacttypescript)
4. [Backend Integration (FastAPI)](#backend-integration-fastapi)
5. [Maritime Audit Logging Integration](#maritime-audit-logging-integration)
6. [Production Deployment](#production-deployment)
7. [Testing and Validation](#testing-and-validation)
8. [Monitoring and Operations](#monitoring-and-operations)

---

## Prerequisites and Setup

### Required Accounts and Services
- WorkOS account with billing information (for production)
- GitHub repository with Actions enabled
- Domain with SSL certificate for production webhooks
- Development environment with Node.js 18+ and Python 3.12+

### Development Environment Setup

```bash
# Frontend dependencies
npm install @workos-inc/authkit-react react-router-dom @tanstack/react-query
npm install -D @types/react @types/react-dom typescript

# Backend dependencies (Python)
pip install workos fastapi uvicorn python-jose[cryptography] python-multipart
```

### Environment Variables Template

```bash
# .env - Development Environment
REACT_APP_WORKOS_CLIENT_ID=your_staging_client_id
REACT_APP_WORKOS_REDIRECT_URI=http://localhost:5173/callback
REACT_APP_WORKOS_API_HOSTNAME=api.workos.com

# Backend Environment
WORKOS_API_KEY=your_staging_api_key
WORKOS_CLIENT_ID=your_staging_client_id
WORKOS_WEBHOOK_SECRET=your_webhook_secret
```

---

## WorkOS Account Configuration

### Step 1: Create WorkOS Organization

1. **Sign up for WorkOS Dashboard**: Visit [WorkOS Dashboard](https://dashboard.workos.com)
2. **Create Organization**: 
   - Organization Name: "Maritime Insurance Platform"
   - Domains: Add your primary domain (e.g., "maritimeinsurance.com")
3. **Environment Setup**:
   - Staging environment is automatically created with viewable API keys
   - Production requires billing information and separate key generation

### Step 2: Configure Authentication Settings

```javascript
// Admin Portal Configuration
const adminPortalLink = workos.portal.generateLink({
  organization_id: 'org_123',
  intent: 'sso',
  return_url: 'https://yourapp.com/admin-portal-success'
});
```

### Step 3: Set Up Webhooks (Development)

**Webhook URL**: `https://yourdevelopmentdomain.com/webhooks/workos`  
**Events to Subscribe**:
- `session.created` - User login events
- `session.ended` - User logout events  
- `user.created` - New user registration
- `organization.created` - New tenant organization

### Step 4: API Key Management

**Staging Keys** (Development):
- Viewable multiple times in dashboard
- HTTP/localhost redirect URIs allowed
- Used for development and testing

**Production Keys** (Production):
- One-time view only - save immediately
- HTTPS-only redirect URIs required
- Requires billing information

---

## Frontend Implementation (React/TypeScript)

### Step 1: Create TypeScript Interfaces

```typescript
// types/auth.ts
export interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  organizationId?: string;
}

export interface AuthState {
  user: User | null;
  isLoading: boolean;
  error: string | null;
}

export interface MaritimeAuthContext {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (options?: { returnTo?: string; organizationId?: string }) => Promise<void>;
  logout: () => Promise<void>;
  switchOrganization: (orgId: string) => Promise<void>;
}
```

### Step 2: Configure AuthKit Provider

```typescript
// providers/AuthProvider.tsx
import React from 'react';
import { AuthKitProvider } from '@workos-inc/authkit-react';

interface AppAuthProviderProps {
  children: React.ReactNode;
}

export const AppAuthProvider: React.FC<AppAuthProviderProps> = ({ children }) => {
  const handleRedirectCallback = ({ state, code }: { state?: any; code?: string }) => {
    // Handle maritime-specific post-authentication flow
    if (state?.returnTo) {
      window.location.href = state.returnTo;
    } else if (state?.organizationId) {
      window.location.href = `/dashboard/${state.organizationId}`;
    } else {
      window.location.href = '/dashboard';
    }
  };

  return (
    <AuthKitProvider
      clientId={process.env.REACT_APP_WORKOS_CLIENT_ID!}
      apiHostname={process.env.REACT_APP_WORKOS_API_HOSTNAME}
      redirectUri={process.env.REACT_APP_WORKOS_REDIRECT_URI}
      devMode={process.env.NODE_ENV === 'development'}
      onRedirectCallback={handleRedirectCallback}
    >
      {children}
    </AuthKitProvider>
  );
};
```

### Step 3: Create Maritime-Specific Auth Context

```typescript
// contexts/MaritimeAuthContext.tsx
import React, { createContext, useContext, useEffect, useState } from 'react';
import { useAuth } from '@workos-inc/authkit-react';
import { MaritimeAuthContext, User } from '../types/auth';

const AuthContext = createContext<MaritimeAuthContext | undefined>(undefined);

export const MaritimeAuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, isLoading, signIn, signOut, switchToOrganization } = useAuth();
  const [authError, setAuthError] = useState<string | null>(null);

  const login = async (options?: { returnTo?: string; organizationId?: string }) => {
    try {
      setAuthError(null);
      const state = {
        returnTo: options?.returnTo,
        organizationId: options?.organizationId
      };
      await signIn({ state, organizationId: options?.organizationId });
    } catch (error) {
      setAuthError(error instanceof Error ? error.message : 'Login failed');
    }
  };

  const logout = async () => {
    try {
      setAuthError(null);
      await signOut();
    } catch (error) {
      setAuthError(error instanceof Error ? error.message : 'Logout failed');
    }
  };

  const switchOrganization = async (orgId: string) => {
    try {
      setAuthError(null);
      await switchToOrganization(orgId);
    } catch (error) {
      setAuthError(error instanceof Error ? error.message : 'Organization switch failed');
    }
  };

  return (
    <AuthContext.Provider value={{
      user,
      isAuthenticated: !!user,
      isLoading,
      error: authError,
      login,
      logout,
      switchOrganization
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useMaritimeAuth = (): MaritimeAuthContext => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useMaritimeAuth must be used within MaritimeAuthProvider');
  }
  return context;
};
```

### Step 4: Protected Route Implementation

```typescript
// components/auth/ProtectedRoute.tsx
import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useMaritimeAuth } from '../../contexts/MaritimeAuthContext';
import { LoadingSpinner } from '../ui/LoadingSpinner';

interface ProtectedRouteProps {
  children: React.ReactNode;
  requiredRole?: string;
  requireAuth?: boolean;
}

export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ 
  children, 
  requiredRole,
  requireAuth = true 
}) => {
  const { user, isLoading, isAuthenticated } = useMaritimeAuth();
  const location = useLocation();

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (requireAuth && !isAuthenticated) {
    return (
      <Navigate 
        to="/login" 
        state={{ returnTo: location.pathname + location.search }}
        replace 
      />
    );
  }

  if (!requireAuth && isAuthenticated) {
    return <Navigate to="/dashboard" replace />;
  }

  // Role-based access control for maritime tenants
  if (requiredRole && user) {
    const userRoles = user.organizationId ? ['tenant_user'] : ['admin'];
    if (!userRoles.includes(requiredRole)) {
      return <Navigate to="/unauthorized" replace />;
    }
  }

  return <>{children}</>;
};
```

### Step 5: Login Component

```typescript
// components/auth/LoginForm.tsx
import React, { useState } from 'react';
import { useLocation } from 'react-router-dom';
import { useMaritimeAuth } from '../../contexts/MaritimeAuthContext';

interface LocationState {
  returnTo?: string;
  organizationId?: string;
}

export const LoginForm: React.FC = () => {
  const { login, isLoading, error } = useMaritimeAuth();
  const [selectedTenantType, setSelectedTenantType] = useState<string>('');
  const location = useLocation();
  
  const state = location.state as LocationState;

  const tenantTypes = [
    { id: 'ship_owner', name: 'Ship Owner', description: 'Vessel ownership and operations' },
    { id: 'cargo_owner', name: 'Cargo Owner', description: 'Cargo shipping and insurance' },
    { id: 'ship_broker', name: 'Ship Broker', description: 'Vessel chartering services' },
    { id: 'charterer', name: 'Charterer', description: 'Vessel charter agreements' }
  ];

  const handleLogin = async () => {
    await login({ 
      returnTo: state?.returnTo || '/dashboard',
      organizationId: selectedTenantType || state?.organizationId
    });
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Maritime Insurance Platform
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Sign in to your account
          </p>
        </div>
        
        <div className="mt-8 space-y-6">
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-md p-4">
              <p className="text-red-600 text-sm">{error}</p>
            </div>
          )}
          
          {/* Tenant Type Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Account Type
            </label>
            <select
              value={selectedTenantType}
              onChange={(e) => setSelectedTenantType(e.target.value)}
              className="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500"
            >
              <option value="">Select your account type</option>
              {tenantTypes.map((type) => (
                <option key={type.id} value={type.id}>
                  {type.name} - {type.description}
                </option>
              ))}
            </select>
          </div>
          
          <button
            onClick={handleLogin}
            disabled={isLoading}
            className="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
          >
            {isLoading ? 'Signing in...' : 'Sign In with WorkOS'}
          </button>
        </div>
      </div>
    </div>
  );
};
```

---

## Backend Integration (FastAPI)

### Step 1: Create FastAPI Authentication Middleware

```python
# middleware/auth_middleware.py
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import workos
from typing import Optional
import json

workos.api_key = os.getenv("WORKOS_API_KEY")
workos.client_id = os.getenv("WORKOS_CLIENT_ID")

security = HTTPBearer()

class MaritimeUser:
    def __init__(self, user_data: dict):
        self.id = user_data.get("sub")
        self.email = user_data.get("email")
        self.first_name = user_data.get("given_name")
        self.last_name = user_data.get("family_name")
        self.organization_id = user_data.get("org")
        self.tenant_type = user_data.get("tenant_type", "unknown")
        self.roles = user_data.get("roles", [])

async def verify_workos_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> MaritimeUser:
    """Verify WorkOS JWT token and return user information"""
    try:
        # Verify the JWT token with WorkOS
        user_info = workos.sso.get_profile_and_token(
            code=None,  # Not needed for token verification
            access_token=credentials.credentials
        )
        
        return MaritimeUser(user_info.profile)
        
    except workos.exceptions.AuthenticationException:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")

async def get_current_user(user: MaritimeUser = Depends(verify_workos_token)) -> MaritimeUser:
    """Get the current authenticated user"""
    return user

async def require_tenant_access(
    vessel_id: str, 
    user: MaritimeUser = Depends(get_current_user)
) -> MaritimeUser:
    """Verify user has access to specific vessel/tenant resources"""
    # Implement vessel-specific access control
    if not user.organization_id:
        raise HTTPException(status_code=403, detail="Organization access required")
    
    # Add vessel ownership verification logic here
    # This would check if user's organization has access to the vessel
    
    return user
```

### Step 2: Create FastAPI Routes with Authentication

```python
# routes/auth_routes.py
from fastapi import APIRouter, Request, HTTPException, Depends
from middleware.auth_middleware import get_current_user, MaritimeUser
import workos

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.get("/me")
async def get_user_profile(user: MaritimeUser = Depends(get_current_user)):
    """Get current user profile information"""
    return {
        "id": user.id,
        "email": user.email,
        "firstName": user.first_name,
        "lastName": user.last_name,
        "organizationId": user.organization_id,
        "tenantType": user.tenant_type,
        "roles": user.roles
    }

@router.post("/organizations/{org_id}/switch")
async def switch_organization(
    org_id: str,
    user: MaritimeUser = Depends(get_current_user)
):
    """Switch user to different organization"""
    try:
        # Implement organization switch logic
        # This might involve updating user session or redirecting
        return {"organizationId": org_id, "switched": True}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Organization switch failed: {str(e)}")

@router.get("/organizations")
async def get_user_organizations(user: MaritimeUser = Depends(get_current_user)):
    """Get organizations user has access to"""
    try:
        # Fetch user's organizations from WorkOS
        organizations = workos.organizations.list_organizations(
            domains=[user.email.split('@')[1]]  # Based on user's domain
        )
        
        return {
            "organizations": [
                {
                    "id": org.id,
                    "name": org.name,
                    "domains": org.domains
                }
                for org in organizations.data
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch organizations: {str(e)}")
```

### Step 3: Webhook Handler Implementation

```python
# routes/webhook_routes.py
from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
import workos
import json
import hmac
import hashlib
from datetime import datetime

router = APIRouter()

@router.post("/webhooks/workos")
async def handle_workos_webhook(
    request: Request, 
    background_tasks: BackgroundTasks
):
    """Handle WorkOS webhook events"""
    payload = await request.body()
    signature = request.headers.get("workos-signature")
    
    if not signature:
        raise HTTPException(status_code=400, detail="Missing webhook signature")
    
    # Verify webhook signature
    webhook_secret = os.getenv("WORKOS_WEBHOOK_SECRET")
    if not verify_webhook_signature(payload, signature, webhook_secret):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")
    
    try:
        event_data = json.loads(payload)
        
        # Process webhook asynchronously
        background_tasks.add_task(process_workos_event, event_data)
        
        return {"status": "received"}
        
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

def verify_webhook_signature(payload: bytes, signature: str, secret: str) -> bool:
    """Verify WorkOS webhook signature"""
    expected_signature = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(f"sha256={expected_signature}", signature)

async def process_workos_event(event_data: dict):
    """Process WorkOS event in background"""
    event_type = event_data.get("event")
    
    # Convert WorkOS event to maritime audit event
    maritime_event = {
        "event_id": event_data.get("id"),
        "timestamp": datetime.now(),
        "event_source": "workos",
        "user_info": {
            "user_id": event_data.get("data", {}).get("id"),
            "email": event_data.get("data", {}).get("email"),
            "organization_id": event_data.get("data", {}).get("organization_id")
        },
        "event_details": {
            "event_type": "authentication",
            "action": event_type,
            "resource": "user_session"
        },
        "compliance_metadata": {
            "regulation_type": "authentication_compliance",
            "retention_period": "3_years"
        }
    }
    
    # Send to maritime audit logging system
    await log_maritime_audit_event(maritime_event)

async def log_maritime_audit_event(event_data: dict):
    """Log event to maritime audit system"""
    # Implementation from maritime-audit-logging-implementation-guide.md
    pass
```

### Step 4: Vessel and Organization Route Protection

```python
# routes/vessel_routes.py
from fastapi import APIRouter, Depends, HTTPException
from middleware.auth_middleware import get_current_user, require_tenant_access, MaritimeUser

router = APIRouter(prefix="/vessels", tags=["vessels"])

@router.get("/{vessel_id}")
async def get_vessel(
    vessel_id: str,
    user: MaritimeUser = Depends(require_tenant_access)
):
    """Get vessel information with tenant access control"""
    # Vessel access is verified by require_tenant_access dependency
    return {
        "vesselId": vessel_id,
        "accessGranted": True,
        "userOrganization": user.organization_id,
        "tenantType": user.tenant_type
    }

@router.post("/{vessel_id}/quotes")
async def create_vessel_quote(
    vessel_id: str,
    quote_data: dict,
    user: MaritimeUser = Depends(require_tenant_access)
):
    """Create insurance quote for vessel"""
    # Implementation with maritime audit logging
    audit_event = {
        "action": f"CREATE quote for vessel {vessel_id}",
        "user_id": user.id,
        "organization_id": user.organization_id,
        "vessel_id": vessel_id,
        "financial_amount": quote_data.get("amount"),
        "tenant_type": user.tenant_type
    }
    
    # Log to maritime audit system
    await log_maritime_audit_event(audit_event)
    
    return {"quoteId": "quote_123", "vesselId": vessel_id}
```

---

## Maritime Audit Logging Integration

### Step 1: Integrate with Existing Audit System

```python
# audit/workos_audit_integration.py
from datetime import datetime
import uuid
from typing import Dict, Any

class WorkOSAuditIntegration:
    def __init__(self, audit_logger):
        self.audit_logger = audit_logger
    
    async def process_workos_event(self, workos_event: Dict[str, Any]) -> Dict[str, Any]:
        """Convert WorkOS event to maritime audit format"""
        maritime_audit_event = {
            "event_id": workos_event.get("id", str(uuid.uuid4())),
            "timestamp": datetime.now(),
            "event_source": "workos",
            
            # User context from WorkOS
            "user_info": {
                "user_id": workos_event.get("data", {}).get("id"),
                "email": workos_event.get("data", {}).get("email"),
                "name": workos_event.get("data", {}).get("name"),
                "organization_id": workos_event.get("data", {}).get("organization_id")
            },
            
            # Event classification
            "event_details": {
                "event_type": "authentication",
                "action": workos_event.get("event"),
                "resource": "user_session",
                "resource_id": workos_event.get("data", {}).get("session_id")
            },
            
            # Maritime compliance metadata
            "compliance_metadata": {
                "regulation_type": "authentication_compliance",
                "retention_period": "3_years",
                "data_classification": "internal"
            },
            
            # Technical details
            "technical_metadata": {
                "ip_address": workos_event.get("ip_address"),
                "user_agent": workos_event.get("user_agent"),
                "session_id": workos_event.get("data", {}).get("session_id")
            }
        }
        
        # Send to maritime audit logging system
        await self.audit_logger.log_audit_event(maritime_audit_event)
        return maritime_audit_event
```

### Step 2: Enhanced FastAPI Middleware with Audit Logging

```python
# middleware/maritime_audit_middleware.py
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
import time
import uuid
from datetime import datetime

class MaritimeAuditMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, audit_logger):
        super().__init__(app)
        self.audit_logger = audit_logger
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Extract user context from WorkOS token
        user_context = await self.extract_user_context(request)
        
        # Process request
        response = await call_next(request)
        
        # Calculate processing time
        processing_time = int((time.time() - start_time) * 1000)
        
        # Create maritime audit event
        audit_event = {
            "event_id": str(uuid.uuid4()),
            "timestamp": datetime.now(),
            "event_source": "fastapi",
            
            "user_info": user_context,
            
            "event_details": {
                "event_type": self.classify_event_type(request),
                "action": f"{request.method} {request.url.path}",
                "resource_type": self.extract_resource_type(request.url.path),
                "resource_id": self.extract_resource_id(request.url.path)
            },
            
            "maritime_context": await self.extract_maritime_context(request),
            
            "technical_metadata": {
                "ip_address": request.client.host,
                "user_agent": request.headers.get("user-agent"),
                "api_endpoint": str(request.url),
                "response_status": response.status_code,
                "processing_time_ms": processing_time
            },
            
            "compliance_metadata": {
                "regulation_type": self.determine_regulation_type(request),
                "retention_period": "7_years",
                "data_classification": "internal"
            }
        }
        
        # Log to maritime audit system
        await self.audit_logger.log_audit_event(audit_event)
        
        return response
    
    async def extract_user_context(self, request: Request) -> Dict[str, Any]:
        """Extract user context from WorkOS authentication"""
        try:
            auth_header = request.headers.get("authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return {}
            
            # This would use the same token verification as the auth middleware
            # user_info = await verify_workos_token(token)
            
            return {
                "user_id": "extracted_from_token",
                "organization_id": "extracted_from_token",
                "tenant_type": "extracted_from_token",
                "email": "extracted_from_token"
            }
            
        except Exception:
            return {}
    
    def classify_event_type(self, request: Request) -> str:
        """Classify request into maritime audit event types"""
        path = request.url.path.lower()
        
        if "/auth/" in path:
            return "authentication"
        elif "/vessels/" in path:
            return "vessel_management"
        elif "/quotes/" in path or "/policies/" in path:
            return "insurance_operations"
        elif request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return "business_operation"
        else:
            return "data_access"
```

---

## Production Deployment

### Step 1: Production Environment Configuration

```yaml
# .github/workflows/deploy-production.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_TO_ASSUME }}
          aws-region: us-east-1
      
      - name: Deploy Frontend
        run: |
          npm install
          npm run build
          aws s3 sync build/ s3://${{ secrets.S3_BUCKET }}
          aws cloudfront create-invalidation --distribution-id ${{ secrets.CLOUDFRONT_DISTRIBUTION }} --paths "/*"
        env:
          REACT_APP_WORKOS_CLIENT_ID: ${{ secrets.WORKOS_PRODUCTION_CLIENT_ID }}
          REACT_APP_WORKOS_REDIRECT_URI: ${{ secrets.WORKOS_PRODUCTION_REDIRECT_URI }}
      
      - name: Deploy Backend
        run: |
          # Deploy FastAPI backend to ECS Fargate
          aws ecs update-service --cluster production --service maritime-api --force-new-deployment
        env:
          WORKOS_API_KEY: ${{ secrets.WORKOS_PRODUCTION_API_KEY }}
          WORKOS_WEBHOOK_SECRET: ${{ secrets.WORKOS_PRODUCTION_WEBHOOK_SECRET }}
```

### Step 2: Production Security Configuration

```python
# config/production.py
import os
from cryptography.fernet import Fernet

class ProductionConfig:
    # WorkOS Production Configuration
    WORKOS_API_KEY = os.getenv("WORKOS_API_KEY")
    WORKOS_CLIENT_ID = os.getenv("WORKOS_CLIENT_ID") 
    WORKOS_WEBHOOK_SECRET = os.getenv("WORKOS_WEBHOOK_SECRET")
    
    # Production Security
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL")
    REDIS_URL = os.getenv("REDIS_URL")
    
    # Maritime Audit Logging
    AUDIT_DATABASE_URL = os.getenv("AUDIT_DATABASE_URL")
    SIEM_API_KEY = os.getenv("DATADOG_API_KEY")
    
    # HTTPS Enforcement
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    @classmethod
    def validate_required_vars(cls):
        required_vars = [
            'WORKOS_API_KEY',
            'WORKOS_CLIENT_ID', 
            'WORKOS_WEBHOOK_SECRET',
            'SECRET_KEY',
            'DATABASE_URL'
        ]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {missing_vars}")
```

### Step 3: Production Webhook Setup

```bash
# Production webhook configuration
curl -X POST "https://api.workos.com/webhooks" \
  -H "Authorization: Bearer $WORKOS_PRODUCTION_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://api.maritimeinsurance.com/webhooks/workos",
    "events": [
      "session.created",
      "session.ended", 
      "user.created",
      "organization.created",
      "directory_sync.user.created",
      "directory_sync.user.updated"
    ]
  }'
```

### Step 4: Health Checks and Monitoring

```python
# routes/health.py
from fastapi import APIRouter, HTTPException
import workos
from datetime import datetime

router = APIRouter()

@router.get("/health")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "maritime-insurance-api"
    }

@router.get("/health/workos")
async def workos_health_check():
    """WorkOS integration health check"""
    try:
        # Test WorkOS API connectivity
        organizations = workos.organizations.list_organizations(limit=1)
        
        return {
            "status": "healthy",
            "workos_api": "connected",
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "workos_api": "disconnected",
                "error": str(e)
            }
        )
```

---

## Testing and Validation

### Step 1: Frontend Testing

```typescript
// tests/auth/LoginForm.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { LoginForm } from '../../components/auth/LoginForm';
import { MaritimeAuthProvider } from '../../contexts/MaritimeAuthContext';
import { AppAuthProvider } from '../../providers/AuthProvider';

const MockAuthProviders: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <BrowserRouter>
    <AppAuthProvider>
      <MaritimeAuthProvider>
        {children}
      </MaritimeAuthProvider>
    </AppAuthProvider>
  </BrowserRouter>
);

describe('LoginForm', () => {
  test('renders login form with tenant selection', () => {
    render(
      <MockAuthProviders>
        <LoginForm />
      </MockAuthProviders>
    );
    
    expect(screen.getByText('Maritime Insurance Platform')).toBeInTheDocument();
    expect(screen.getByText('Account Type')).toBeInTheDocument();
    expect(screen.getByText('Sign In with WorkOS')).toBeInTheDocument();
  });
  
  test('handles tenant type selection', async () => {
    render(
      <MockAuthProviders>
        <LoginForm />
      </MockAuthProviders>
    );
    
    const select = screen.getByDisplayValue('Select your account type');
    fireEvent.change(select, { target: { value: 'ship_owner' } });
    
    expect(select.value).toBe('ship_owner');
  });
});
```

### Step 2: Backend Testing

```python
# tests/test_auth_middleware.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)

@pytest.fixture
def mock_workos_user():
    return {
        "sub": "user_123",
        "email": "test@shipowner.com",
        "given_name": "John",
        "family_name": "Doe",
        "org": "org_456",
        "tenant_type": "ship_owner"
    }

@patch('middleware.auth_middleware.workos.sso.get_profile_and_token')
def test_authenticated_vessel_access(mock_get_profile, mock_workos_user):
    """Test authenticated access to vessel endpoint"""
    mock_get_profile.return_value.profile = mock_workos_user
    
    response = client.get(
        "/vessels/vessel_123",
        headers={"Authorization": "Bearer valid_token"}
    )
    
    assert response.status_code == 200
    assert response.json()["vesselId"] == "vessel_123"
    assert response.json()["userOrganization"] == "org_456"

def test_unauthenticated_vessel_access():
    """Test unauthenticated access is rejected"""
    response = client.get("/vessels/vessel_123")
    
    assert response.status_code == 401

@patch('middleware.auth_middleware.workos.sso.get_profile_and_token')
def test_webhook_signature_validation(mock_get_profile):
    """Test WorkOS webhook signature validation"""
    import hmac
    import hashlib
    
    payload = b'{"event": "session.created", "data": {"id": "user_123"}}'
    secret = "test_webhook_secret"
    signature = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    
    response = client.post(
        "/webhooks/workos",
        data=payload,
        headers={"workos-signature": f"sha256={signature}"}
    )
    
    assert response.status_code == 200
    assert response.json()["status"] == "received"
```

### Step 3: Integration Testing

```python
# tests/test_workos_integration.py
import pytest
import requests
from datetime import datetime

class TestWorkOSIntegration:
    """Integration tests for WorkOS authentication flow"""
    
    def test_workos_api_connectivity(self):
        """Test connectivity to WorkOS API"""
        response = requests.get(
            "https://api.workos.com/organizations",
            headers={"Authorization": f"Bearer {os.getenv('WORKOS_API_KEY')}"}
        )
        assert response.status_code in [200, 401]  # 401 is acceptable (no orgs)
    
    def test_webhook_endpoint_accessibility(self):
        """Test webhook endpoint is accessible"""
        response = requests.post(
            f"{os.getenv('BASE_URL')}/webhooks/workos",
            json={"test": "webhook"},
            timeout=10
        )
        # Should return 400 (bad signature) or 401 (invalid signature)
        assert response.status_code in [400, 401]
    
    def test_frontend_auth_flow(self):
        """Test frontend authentication redirect flow"""
        # This would use Playwright or Selenium for full browser testing
        pass
```

### Step 4: Load Testing

```python
# tests/load_test.py
import asyncio
import aiohttp
import time
from concurrent.futures import ThreadPoolExecutor

async def test_auth_endpoint_load():
    """Load test authentication endpoints"""
    
    async def make_request(session, token):
        async with session.get(
            f"{BASE_URL}/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        ) as response:
            return response.status
    
    async with aiohttp.ClientSession() as session:
        # Simulate 100 concurrent requests
        tasks = [
            make_request(session, "test_token")
            for _ in range(100)
        ]
        
        start_time = time.time()
        results = await asyncio.gather(*tasks, return_exceptions=True)
        end_time = time.time()
        
        success_count = sum(1 for r in results if r == 200)
        avg_response_time = (end_time - start_time) / 100
        
        print(f"Load test results:")
        print(f"Successful requests: {success_count}/100")
        print(f"Average response time: {avg_response_time:.2f}s")
        
        assert avg_response_time < 1.0  # Sub-second response time
```

---

## Monitoring and Operations

### Step 1: Application Monitoring

```python
# monitoring/workos_metrics.py
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time

# Prometheus metrics for WorkOS integration
workos_auth_requests = Counter(
    'workos_auth_requests_total',
    'Total WorkOS authentication requests',
    ['method', 'status']
)

workos_auth_duration = Histogram(
    'workos_auth_duration_seconds',
    'WorkOS authentication request duration',
    ['method']
)

workos_webhook_events = Counter(
    'workos_webhook_events_total',
    'Total WorkOS webhook events received',
    ['event_type']
)

workos_active_sessions = Gauge(
    'workos_active_sessions',
    'Current number of active WorkOS sessions'
)

class WorkOSMetricsCollector:
    def __init__(self):
        self.start_metrics_server()
    
    def start_metrics_server(self, port: int = 8090):
        """Start Prometheus metrics server"""
        start_http_server(port)
    
    def record_auth_request(self, method: str, status: int, duration: float):
        """Record authentication request metrics"""
        workos_auth_requests.labels(method=method, status=status).inc()
        workos_auth_duration.labels(method=method).observe(duration)
    
    def record_webhook_event(self, event_type: str):
        """Record webhook event metrics"""
        workos_webhook_events.labels(event_type=event_type).inc()
    
    def update_active_sessions(self, count: int):
        """Update active sessions gauge"""
        workos_active_sessions.set(count)
```

### Step 2: Error Tracking and Alerting

```python
# monitoring/error_tracking.py
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration

def setup_error_tracking():
    """Configure Sentry error tracking"""
    sentry_sdk.init(
        dsn=os.getenv("SENTRY_DSN"),
        integrations=[
            FastApiIntegration(auto_enabling_integrations=False),
            SqlalchemyIntegration(),
        ],
        traces_sample_rate=0.1,
        environment=os.getenv("ENVIRONMENT", "development"),
        before_send=filter_sensitive_data
    )

def filter_sensitive_data(event, hint):
    """Filter sensitive data from error reports"""
    # Remove authentication tokens and personal data
    if 'request' in event:
        if 'headers' in event['request']:
            event['request']['headers'].pop('authorization', None)
        if 'data' in event['request']:
            # Remove sensitive form data
            pass
    
    return event

# Custom exception classes
class WorkOSAuthenticationError(Exception):
    """WorkOS authentication specific errors"""
    pass

class MaritimeComplianceError(Exception):
    """Maritime compliance specific errors"""
    pass
```

### Step 3: Operational Dashboards

```python
# monitoring/dashboard_data.py
from datetime import datetime, timedelta
from sqlalchemy import func
from database import SessionLocal
from models.audit_log import MaritimeAuditLog

class WorkOSOperationalDashboard:
    def __init__(self):
        self.db = SessionLocal()
    
    async def get_authentication_metrics(self, hours: int = 24):
        """Get authentication metrics for dashboard"""
        since = datetime.now() - timedelta(hours=hours)
        
        # Authentication events from audit log
        auth_events = self.db.query(MaritimeAuditLog).filter(
            MaritimeAuditLog.event_type == "authentication",
            MaritimeAuditLog.timestamp >= since
        ).all()
        
        successful_logins = len([e for e in auth_events if "created" in e.action])
        failed_logins = len([e for e in auth_events if "failed" in e.action])
        
        return {
            "total_auth_events": len(auth_events),
            "successful_logins": successful_logins,
            "failed_logins": failed_logins,
            "success_rate": successful_logins / len(auth_events) if auth_events else 0,
            "unique_users": len(set(e.user_id for e in auth_events if e.user_id)),
            "peak_hour": self.calculate_peak_hour(auth_events)
        }
    
    async def get_tenant_activity_metrics(self, hours: int = 24):
        """Get tenant activity metrics"""
        since = datetime.now() - timedelta(hours=hours)
        
        tenant_events = self.db.query(MaritimeAuditLog).filter(
            MaritimeAuditLog.timestamp >= since,
            MaritimeAuditLog.user_info['tenant_type'].astext.isnot(None)
        ).all()
        
        tenant_activity = {}
        for event in tenant_events:
            tenant_type = event.user_info.get('tenant_type', 'unknown')
            if tenant_type not in tenant_activity:
                tenant_activity[tenant_type] = 0
            tenant_activity[tenant_type] += 1
        
        return {
            "tenant_breakdown": tenant_activity,
            "most_active_tenant": max(tenant_activity, key=tenant_activity.get) if tenant_activity else None,
            "total_tenant_events": len(tenant_events)
        }
    
    def calculate_peak_hour(self, events):
        """Calculate peak activity hour"""
        hour_counts = {}
        for event in events:
            hour = event.timestamp.hour
            hour_counts[hour] = hour_counts.get(hour, 0) + 1
        
        return max(hour_counts, key=hour_counts.get) if hour_counts else None
```

### Step 4: Automated Alerts

```yaml
# monitoring/alerts.yml - Prometheus Alerting Rules
groups:
  - name: workos_authentication
    rules:
      - alert: HighAuthenticationFailureRate
        expr: rate(workos_auth_requests_total{status!="200"}[5m]) > 0.1
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High WorkOS authentication failure rate"
          description: "Authentication failure rate is {{ $value }} per second"
      
      - alert: WorkOSWebhookDeliveryFailure
        expr: increase(workos_webhook_events_total{status="failed"}[5m]) > 5
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "WorkOS webhook delivery failures"
          description: "{{ $value }} webhook deliveries failed in the last 5 minutes"
      
      - alert: SlowAuthenticationResponse
        expr: histogram_quantile(0.95, rate(workos_auth_duration_seconds_bucket[5m])) > 2
        for: 3m
        labels:
          severity: warning
        annotations:
          summary: "Slow WorkOS authentication responses"
          description: "95th percentile authentication time is {{ $value }}s"
```

---

## Implementation Checklist

### Week 1: Foundation Setup
- [ ] WorkOS account creation and staging environment setup
- [ ] Frontend AuthKit provider integration
- [ ] Basic authentication flow implementation
- [ ] Development environment configuration

### Week 2: Backend Integration
- [ ] FastAPI authentication middleware implementation
- [ ] Webhook endpoint creation and testing
- [ ] Maritime user context extraction
- [ ] Basic route protection implementation

### Week 3: Maritime Integration
- [ ] Audit logging system integration
- [ ] Multi-tenant access control implementation
- [ ] Maritime compliance event processing
- [ ] Security validation and testing

### Week 4: Production Deployment
- [ ] Production WorkOS environment setup
- [ ] CI/CD pipeline configuration
- [ ] Production security hardening
- [ ] Monitoring and alerting setup
- [ ] Load testing and performance validation
- [ ] Go-live and operational readiness

---

## Troubleshooting Guide

### Common Issues

**Authentication Token Errors**:
- Verify API keys match environment (staging vs production)
- Check token expiration and refresh logic
- Validate JWT signature verification

**Webhook Delivery Failures**:
- Confirm HTTPS endpoint accessibility
- Verify webhook secret configuration
- Check signature validation logic
- Review firewall and networking rules

**Multi-Tenant Access Issues**:
- Validate organization ID extraction from tokens
- Check tenant-specific access control logic
- Verify organization membership queries

**Performance Issues**:
- Monitor authentication endpoint response times
- Check database query performance for user lookups
- Validate caching strategies for user sessions
- Review webhook processing efficiency

For additional support, refer to:
- WorkOS Documentation: https://workos.com/docs
- Maritime Audit Logging Guide: `docs/maritime-audit-logging-implementation-guide.md`
- Authentication Platform Analysis: `options/authentication-platform-options.md`

---

**Implementation Status**: Ready for immediate deployment  
**Documentation Version**: 1.0  
**Last Updated**: 2025-07-28