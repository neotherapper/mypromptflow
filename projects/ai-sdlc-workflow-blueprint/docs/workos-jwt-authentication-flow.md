# WorkOS JWT Authentication Flow Diagram

## Overview

This document provides a comprehensive visual representation of how JWT tokens flow through the WorkOS authentication system in the maritime insurance platform, showing the complete OAuth flow, token lifecycle, session management, and multi-tenant access control.

## Visual Flow Diagram

```mermaid
sequenceDiagram
    participant User as 👤 User
    participant Browser as 🌐 Browser
    participant AuthKit as 🔐 WorkOS AuthKit
    participant WorkOS as ☁️ WorkOS Service
    participant Frontend as ⚛️ React App
    participant Backend as 🐍 FastAPI Backend
    participant Database as 🗄️ PostgreSQL

    Note over User, Database: Maritime Insurance Platform Authentication Flow

    %% Initial Access Attempt
    User->>Browser: Access protected route
    Browser->>Frontend: Request /dashboard
    Frontend->>AuthKit: Check authentication status
    AuthKit-->>Frontend: Not authenticated
    Frontend-->>Browser: Redirect to login

    %% OAuth Flow Initiation
    User->>Browser: Click login
    Browser->>AuthKit: Initiate login
    AuthKit->>WorkOS: Start OAuth flow
    WorkOS-->>AuthKit: Return authorization URL
    AuthKit-->>Browser: Redirect to WorkOS login

    %% WorkOS Authentication
    User->>WorkOS: Enter credentials
    WorkOS->>WorkOS: Validate credentials
    WorkOS->>WorkOS: Generate JWT tokens
    Note over WorkOS: Creates access_token (JWT)<br/>Contains: user_id, org_id, roles, exp

    %% OAuth Callback
    WorkOS-->>Browser: Redirect to callback URL with code
    Browser->>AuthKit: Handle callback with auth code
    AuthKit->>WorkOS: Exchange code for tokens
    WorkOS-->>AuthKit: Return JWT access_token & user profile

    %% Session Establishment
    AuthKit->>Browser: Store tokens in secure cookies
    Note over AuthKit, Browser: WorkOS manages token storage<br/>Automatic refresh handling
    AuthKit-->>Frontend: Authentication success
    Frontend-->>Browser: Redirect to dashboard

    %% API Access Flow
    User->>Frontend: Interact with maritime data
    Frontend->>AuthKit: Get current token
    AuthKit-->>Frontend: Return valid JWT token
    Frontend->>Backend: API request with Authorization header
    Note over Frontend, Backend: Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGci...

    %% Backend Token Verification
    Backend->>Backend: Extract JWT from header
    Backend->>WorkOS: Verify token signature/validity
    WorkOS-->>Backend: Token valid + user profile
    Backend->>Backend: Extract maritime context
    Note over Backend: MaritimeUser object created<br/>Contains: user_id, org_id, tenant_type, roles

    %% Tenant-Specific Access Control
    Backend->>Database: Query with tenant context
    Database-->>Backend: Return tenant-filtered data
    Backend-->>Frontend: JSON response with maritime data
    Frontend-->>Browser: Render dashboard

    %% Token Refresh (Automatic)
    AuthKit->>WorkOS: Check token expiration
    WorkOS-->>AuthKit: Token needs refresh
    AuthKit->>WorkOS: Request new token
    WorkOS-->>AuthKit: Return refreshed JWT
    AuthKit->>Browser: Update stored tokens
```

## Detailed Component Breakdown

### 1. Frontend Authentication Layer

#### WorkOS AuthKit React SDK Responsibilities
```typescript
// What WorkOS AuthKit handles automatically:
const authKitFeatures = {
  tokenStorage: "Secure HTTP-only cookies",
  tokenRefresh: "Automatic background refresh",
  sessionManagement: "Complete session lifecycle",
  oauthFlow: "Full OAuth 2.0 + PKCE implementation",
  securityHeaders: "CSRF protection and secure storage"
};

// Your React app integration:
import { useAuth } from '@workos-inc/authkit-react';

const { user, isLoading, signIn, signOut } = useAuth();
```

#### Maritime-Specific Context Wrapper
```typescript
// Your custom wrapper for maritime business logic:
const MaritimeAuthProvider = ({ children }) => {
  const { user } = useAuth();
  
  // Extract maritime-specific context
  const maritimeContext = {
    tenantType: user?.organizationId ? 'tenant_user' : 'admin',
    vesselAccess: user?.roles?.includes('vessel_operator'),
    organizationId: user?.organizationId
  };
  
  return (
    <MaritimeContext.Provider value={maritimeContext}>
      {children}
    </MaritimeContext.Provider>
  );
};
```

### 2. JWT Token Structure

#### Token Content (Decoded)
```json
{
  "header": {
    "alg": "RS256",
    "typ": "JWT",
    "kid": "workos-key-id"
  },
  "payload": {
    "sub": "user_01234567890",
    "email": "captain@maritimecompany.com",
    "given_name": "Captain",
    "family_name": "Smith",
    "org": "org_maritime_company_001",
    "roles": ["vessel_operator", "tenant_user"],
    "tenant_type": "ship_owner",
    "iss": "https://api.workos.com",
    "aud": "your-workos-client-id",
    "iat": 1704067200,
    "exp": 1704070800
  },
  "signature": "WorkOS-generated-signature"
}
```

#### Token Lifecycle Management
```python
# Backend token verification process:
async def verify_workos_token(credentials: HTTPAuthorizationCredentials) -> MaritimeUser:
    try:
        # WorkOS Python SDK handles:
        # 1. Signature verification against WorkOS public keys
        # 2. Expiration time validation
        # 3. Issuer and audience validation
        # 4. Token format validation
        
        user_info = workos.sso.get_profile_and_token(
            access_token=credentials.credentials
        )
        
        # Extract maritime-specific context
        return MaritimeUser({
            'user_id': user_info.profile['sub'],
            'email': user_info.profile['email'],
            'organization_id': user_info.profile.get('org'),
            'tenant_type': user_info.profile.get('tenant_type', 'unknown'),
            'roles': user_info.profile.get('roles', [])
        })
        
    except workos.exceptions.AuthenticationException:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### 3. Session Management Architecture

#### What WorkOS Handles vs. What You Implement

| Component | WorkOS Responsibility | Your Implementation |
|-----------|----------------------|-------------------|
| **Token Generation** | ✅ JWT creation, signing, expiration | ❌ No custom implementation needed |
| **Token Storage** | ✅ Secure cookies, CSRF protection | ❌ No manual storage required |
| **Token Refresh** | ✅ Automatic background refresh | ❌ No refresh logic needed |
| **Session Security** | ✅ HTTP-only cookies, SameSite, Secure flags | ❌ No security headers needed |
| **Token Verification** | ✅ Signature validation, expiration checks | ✅ Call WorkOS SDK for verification |
| **User Context** | ✅ Basic user profile data | ✅ Extract maritime-specific context |
| **Tenant Isolation** | ✅ Organization-based separation | ✅ Implement vessel-specific access control |

#### Session Flow Details
```mermaid
graph TD
    A[User Login] --> B[WorkOS OAuth Flow]
    B --> C[JWT Token Generated]
    C --> D[Stored in Secure Cookies]
    D --> E[Frontend Gets Token via AuthKit]
    E --> F[API Call with Bearer Token]
    F --> G[Backend Verifies with WorkOS]
    G --> H[Extract Maritime Context]
    H --> I[Database Query with Tenant Filter]
    
    J[Token Near Expiry] --> K[AuthKit Auto-Refresh]
    K --> L[New JWT from WorkOS]
    L --> D
    
    M[User Logout] --> N[AuthKit Clear Cookies]
    N --> O[Redirect to Login]
```

### 4. Multi-Tenant Access Control

#### Organization-Based Tenant Isolation
```python
# Tenant context extraction from JWT
def extract_tenant_context(user: MaritimeUser) -> TenantContext:
    return TenantContext(
        organization_id=user.organization_id,
        tenant_type=user.tenant_type,  # ship_owner, cargo_owner, broker, charterer
        access_level=determine_access_level(user.roles),
        geographic_scope=get_geographic_permissions(user.organization_id)
    )

# Database query with tenant filtering
async def get_vessels_for_user(user: MaritimeUser) -> List[Vessel]:
    tenant_context = extract_tenant_context(user)
    
    query = select(Vessel).where(
        Vessel.organization_id == tenant_context.organization_id
    )
    
    # Additional vessel-specific access control
    if tenant_context.tenant_type == "ship_owner":
        query = query.where(Vessel.owner_id == tenant_context.organization_id)
    elif tenant_context.tenant_type == "broker":
        query = query.where(Vessel.broker_id == tenant_context.organization_id)
    
    return await database.fetch_all(query)
```

### 5. API Request Flow

#### Complete Request/Response Cycle
```mermaid
sequenceDiagram
    participant React as React Component
    participant AuthKit as WorkOS AuthKit
    participant API as FastAPI Endpoint
    participant WorkOS as WorkOS Validation
    participant DB as Database

    React->>AuthKit: Get authentication token
    AuthKit-->>React: Return valid JWT token
    
    React->>API: GET /api/vessels
    Note over React, API: Authorization: Bearer eyJ0eXAiOiJKV1Q...
    
    API->>API: Extract Bearer token
    API->>WorkOS: Verify token signature & expiration
    WorkOS-->>API: Token valid + user profile
    
    API->>API: Create MaritimeUser object
    API->>API: Extract tenant context
    
    API->>DB: Query vessels with tenant filter
    Note over API, DB: WHERE organization_id = user.org_id
    
    DB-->>API: Return tenant-filtered vessels
    API-->>React: JSON response with vessels
    
    React->>React: Render vessel dashboard
```

### 6. Error Handling and Edge Cases

#### Authentication Error Scenarios
```typescript
// Frontend error handling
const handleAuthError = (error: AuthError) => {
  switch (error.type) {
    case 'TOKEN_EXPIRED':
      // AuthKit handles this automatically
      break;
      
    case 'INVALID_TOKEN':
      // Force re-authentication
      signOut();
      break;
      
    case 'ORGANIZATION_ACCESS_DENIED':
      // Redirect to tenant selection
      window.location.href = '/select-organization';
      break;
      
    case 'INSUFFICIENT_PERMISSIONS':
      // Show access denied page
      setError('You do not have permission to access this resource');
      break;
  }
};
```

#### Backend Error Responses
```python
# Token validation error handling
try:
    user = await verify_workos_token(credentials)
except workos.exceptions.AuthenticationException as e:
    if "expired" in str(e).lower():
        raise HTTPException(
            status_code=401, 
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"}
        )
    else:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token"
        )
```

## Security Considerations

### 1. Token Security
- **Storage**: WorkOS uses secure HTTP-only cookies (not localStorage)
- **Transport**: All communications over HTTPS with proper SSL/TLS
- **Validation**: Server-side signature verification on every request
- **Expiration**: Short-lived tokens with automatic refresh

### 2. Maritime-Specific Security
- **Tenant Isolation**: Organization-based data separation
- **Vessel Access Control**: Granular permissions per vessel/IMO
- **Geographic Restrictions**: Location-based access controls
- **Audit Trail**: Complete authentication event logging

### 3. Compliance Features
- **GDPR**: Right to deletion, data portability via WorkOS
- **SOC 2**: Security controls and audit trails
- **Maritime Regulations**: 7-year data retention, audit logging

## Implementation Requirements Summary

### ✅ You MUST Use Both SDKs

**React Frontend SDK** (`@workos-inc/authkit-react`):
- Handles OAuth flow, token storage, session management
- Provides React hooks for authentication state
- Manages token refresh automatically
- Required for security and proper integration

**Python Backend SDK** (`workos`):
- Verifies JWT token signatures
- Validates token expiration and claims
- Extracts user profile information
- Required for secure API authentication

### ❌ You Cannot Bypass SDKs

**Direct API Approach Problems**:
- Manual JWT signature verification complexity
- Token refresh logic implementation required
- Security vulnerabilities without proper validation
- Loss of WorkOS security features and updates

**Recommended Architecture**:
- Use WorkOS SDKs as designed
- Layer maritime-specific logic on top
- Leverage WorkOS security and session management
- Focus on business logic, not authentication plumbing

This authentication flow provides enterprise-grade security while maintaining the flexibility needed for maritime insurance platform requirements.