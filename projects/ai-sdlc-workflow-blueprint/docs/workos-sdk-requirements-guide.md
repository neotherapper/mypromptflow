# WorkOS SDK Requirements Decision Guide

## Executive Summary

**TL;DR**: You **MUST** use both WorkOS SDKs (React and Python) for secure, maintainable authentication. Bypassing the SDKs creates security vulnerabilities, increases complexity, and loses critical features.

## Core Question: SDK vs Direct API Approach

### ❌ Why You Cannot Just Call Python API Profile URL

Your proposed approach: *"Call Python API profile URL to get data with tenant permissions"* **will not work** for these reasons:

#### 1. **No Authentication Mechanism**
```python
# This approach FAILS - no way to verify who is making the request
@app.get("/api/profile")
async def get_profile(): 
    # How do you know who this user is?
    # How do you verify they're authenticated?
    # How do you prevent unauthorized access?
    return {"error": "No authentication provided"}
```

#### 2. **Missing Token Verification**
```python
# Without WorkOS SDK, you'd need to manually implement:
def manually_verify_jwt(token: str):
    # 1. Decode JWT header and payload
    # 2. Fetch WorkOS public keys
    # 3. Verify signature using cryptographic libraries
    # 4. Validate expiration, issuer, audience
    # 5. Handle key rotation
    # 6. Implement proper error handling
    # Result: 200+ lines of complex security code
```

#### 3. **Session Management Complexity**
```typescript
// Without React SDK, you'd need to implement:
const manualSessionManagement = {
  tokenStorage: "Manual localStorage/cookie management",
  tokenRefresh: "Custom refresh logic with race conditions",
  securityHeaders: "Manual CSRF protection",
  oauthFlow: "Full OAuth 2.0 + PKCE implementation",
  errorHandling: "Custom authentication error scenarios"
};
// Result: 500+ lines of authentication plumbing
```

### ✅ Why Both SDKs Are Required

#### Frontend SDK (`@workos-inc/authkit-react`)
**Primary Responsibilities**:
- Handles complete OAuth 2.0 + PKCE flow
- Manages secure token storage (HTTP-only cookies)
- Provides automatic token refresh
- Offers React hooks for authentication state
- Implements security best practices (CSRF, XSS protection)

**Code Example**:
```typescript
import { useAuth } from '@workos-inc/authkit-react';

// This single hook provides:
const { 
  user,           // Current user profile
  isLoading,      // Loading state
  signIn,         // Login function
  signOut,        // Logout function
  isAuthenticated // Auth status
} = useAuth();

// Without SDK: 500+ lines of manual implementation
```

#### Backend SDK (`workos` Python package)
**Primary Responsibilities**:
- Verifies JWT token signatures securely
- Validates token expiration and claims
- Handles WorkOS API communication
- Provides user profile extraction
- Manages webhook signature verification

**Code Example**:
```python
import workos

# This single function provides secure token verification:
user_info = workos.sso.get_profile_and_token(
    access_token=token
)

# Without SDK: 200+ lines of cryptographic verification code
```

## Detailed Implementation Requirements

### 1. Frontend Authentication Flow

#### With WorkOS SDK (Recommended) ✅
```typescript
// App.tsx - Complete authentication setup in ~50 lines
import { AuthKitProvider, useAuth } from '@workos-inc/authkit-react';

function App() {
  return (
    <AuthKitProvider
      clientId={process.env.REACT_APP_WORKOS_CLIENT_ID!}
      redirectUri={process.env.REACT_APP_WORKOS_REDIRECT_URI}
    >
      <MaritimeApp />
    </AuthKitProvider>
  );
}

function MaritimeApp() {
  const { user, signIn } = useAuth();
  
  return user ? (
    <VesselDashboard user={user} />
  ) : (
    <button onClick={() => signIn()}>Login</button>
  );
}
```

#### Without SDK (Not Recommended) ❌
```typescript
// Manual implementation would require ~500+ lines:
class ManualAuthImplementation {
  // OAuth 2.0 flow implementation
  initiateOAuth() { /* 50+ lines */ }
  handleCallback() { /* 100+ lines */ }
  
  // Token management
  storeTokens() { /* 30+ lines with security considerations */ }
  refreshTokens() { /* 80+ lines with race condition handling */ }
  
  // Security implementation
  validateCSRF() { /* 40+ lines */ }
  handleSecureCookies() { /* 60+ lines */ }
  
  // Error handling
  handleAuthErrors() { /* 100+ lines */ }
  
  // Session management
  manageSessions() { /* 150+ lines */ }
}
```

### 2. Backend Token Verification

#### With WorkOS SDK (Recommended) ✅
```python
# Secure token verification in ~20 lines
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
import workos

security = HTTPBearer()

async def verify_token(credentials = Depends(security)):
    try:
        # WorkOS SDK handles all complexity:
        # - Signature verification
        # - Expiration validation  
        # - Issuer/audience checks
        # - Key rotation handling
        user_info = workos.sso.get_profile_and_token(
            access_token=credentials.credentials
        )
        return user_info.profile
    except workos.exceptions.AuthenticationException:
        raise HTTPException(status_code=401, detail="Invalid token")

# Use in routes
@app.get("/api/vessels")
async def get_vessels(user = Depends(verify_token)):
    return await get_vessels_for_user(user['sub'])
```

#### Without SDK (Not Recommended) ❌
```python
# Manual implementation would require ~200+ lines:
import jwt
import requests
from cryptography.hazmat.primitives import serialization
from datetime import datetime

class ManualJWTVerification:
    def __init__(self):
        self.workos_public_keys = None
        self.last_key_fetch = None
    
    async def verify_jwt_manually(self, token: str):
        # 1. Decode token header (20+ lines)
        header = self.decode_header(token)
        
        # 2. Fetch and cache WorkOS public keys (40+ lines)
        public_key = await self.get_public_key(header['kid'])
        
        # 3. Verify signature (30+ lines)
        if not self.verify_signature(token, public_key):
            raise AuthenticationError("Invalid signature")
        
        # 4. Validate claims (50+ lines)
        payload = jwt.decode(token, public_key, algorithms=['RS256'])
        self.validate_claims(payload)
        
        # 5. Handle errors and edge cases (60+ lines)
        return payload
    
    def decode_header(self, token): # 20+ lines
    def get_public_key(self, kid): # 40+ lines  
    def verify_signature(self, token, key): # 30+ lines
    def validate_claims(self, payload): # 50+ lines
```

### 3. API Request Pattern Comparison

#### With SDKs (Recommended) ✅
```typescript
// Frontend - Simple API calls
const api = axios.create({
  baseURL: '/api'
});

// WorkOS AuthKit automatically adds Authorization header
const vessels = await api.get('/vessels');
```

```python
# Backend - Simple verification
@app.get("/vessels")
async def get_vessels(user = Depends(verify_workos_token)):
    return {"vessels": await get_user_vessels(user.organization_id)}
```

#### Without SDKs (Complex) ❌
```typescript
// Frontend - Manual token management
class ManualAPIClient {
  async makeRequest(url: string) {
    // 1. Get token from storage
    const token = this.getStoredToken();
    
    // 2. Check if token is expired
    if (this.isTokenExpired(token)) {
      // 3. Refresh token
      token = await this.refreshToken();
    }
    
    // 4. Make request with proper headers
    return fetch(url, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'X-CSRF-Token': this.getCSRFToken()
      }
    });
  }
  
  // Each method requires 20-50 lines of implementation
  getStoredToken() { /* 20+ lines */ }
  isTokenExpired() { /* 15+ lines */ }
  refreshToken() { /* 50+ lines */ }
  getCSRFToken() { /* 25+ lines */ }
}
```

## Security Comparison

### Security Features Included with SDKs ✅

| Security Feature | WorkOS SDK Implementation | Manual Implementation |
|------------------|---------------------------|----------------------|
| **JWT Signature Verification** | ✅ Automatic with key rotation | ❌ 50+ lines of crypto code |
| **Token Expiration Handling** | ✅ Automatic validation | ❌ Manual timestamp checking |
| **Secure Token Storage** | ✅ HTTP-only cookies with flags | ❌ Manual cookie security |
| **CSRF Protection** | ✅ Built-in protection | ❌ Custom CSRF implementation |
| **XSS Prevention** | ✅ Secure cookie handling | ❌ Manual XSS prevention |
| **Token Refresh** | ✅ Automatic background refresh | ❌ Custom refresh logic with race conditions |
| **OAuth 2.0 + PKCE** | ✅ Complete implementation | ❌ 200+ lines of OAuth code |
| **Error Handling** | ✅ Comprehensive error scenarios | ❌ Manual error handling |
| **Session Management** | ✅ Complete session lifecycle | ❌ Custom session logic |

### Security Vulnerabilities Without SDKs ❌

#### 1. **Token Storage Vulnerabilities**
```typescript
// Common mistake - storing JWT in localStorage
localStorage.setItem('token', jwt_token); // ❌ XSS vulnerable

// Proper secure storage requires complex implementation:
// - HTTP-only cookies
// - Secure and SameSite flags  
// - CSRF token coordination
// - Domain and path restrictions
```

#### 2. **JWT Verification Vulnerabilities**
```python
# Common mistake - trusting JWT without verification
payload = jwt.decode(token, verify=False) # ❌ NEVER DO THIS

# Proper verification requires:
# - Signature validation with WorkOS public keys
# - Expiration time checking
# - Issuer and audience validation
# - Key rotation handling
# - Algorithm specification (prevent "none" attacks)
```

#### 3. **Race Condition in Token Refresh**
```typescript
// Without proper handling, multiple API calls can cause:
// - Multiple simultaneous refresh attempts
// - Token refresh loops
// - Authentication state corruption
// - Session invalidation
```

## Performance and Maintenance Considerations

### Development Time Comparison

| Implementation Aspect | With SDKs | Without SDKs |
|----------------------|-----------|--------------|
| **Initial Setup** | 2-4 hours | 2-3 weeks |
| **Testing** | Basic unit tests | Comprehensive security testing |
| **Maintenance** | SDK updates | Manual security updates |
| **Bug Fixes** | WorkOS handles security bugs | Your responsibility |
| **Feature Updates** | Automatic with SDK updates | Manual implementation |

### Code Maintainability

#### With SDKs ✅
```typescript
// Clean, maintainable code
const { user, signIn, signOut } = useAuth();

if (!user) {
  return <LoginButton onClick={signIn} />;
}

return <Dashboard user={user} onLogout={signOut} />;
```

#### Without SDKs ❌
```typescript
// Complex, hard-to-maintain code
class AuthManager {
  constructor() {
    this.tokenRefreshPromise = null;
    this.refreshInProgress = false;
    this.authCallbacks = [];
    // ... 50+ more lines of initialization
  }
  
  // 500+ lines of authentication logic
  // Complex error handling
  // Race condition prevention
  // Security implementation
  // Session management
}
```

## Maritime-Specific Requirements

### Multi-Tenant Architecture Support

#### With SDKs ✅
```python
# Clean tenant extraction from WorkOS token
async def get_current_user(token = Depends(verify_workos_token)):
    return MaritimeUser(
        id=token['sub'],
        email=token['email'],
        organization_id=token['org'],  # WorkOS provides this
        tenant_type=determine_tenant_type(token['org'])
    )

@app.get("/vessels")
async def get_vessels(user = Depends(get_current_user)):
    # Automatic tenant filtering
    return await vessel_service.get_vessels_for_org(user.organization_id)
```

#### Without SDKs ❌
```python
# Complex tenant context management
class ManualTenantManager:
    async def extract_tenant_context(self, request):
        # 1. Manually verify JWT
        token = await self.verify_jwt_manually(request.headers.get('authorization'))
        
        # 2. Extract organization info
        org_id = token.get('org')  # Hope WorkOS includes this
        
        # 3. Validate organization access
        if not await self.validate_organization_access(org_id):
            raise AuthorizationError()
        
        # 4. Create tenant context
        return TenantContext(org_id)
    
    # Each method requires significant implementation
```

### Compliance and Audit Logging

#### With SDKs ✅
```python
# WorkOS webhooks provide complete audit trail
@app.post("/webhooks/workos")
async def handle_workos_webhook(request: Request):
    # WorkOS provides:
    # - User login/logout events
    # - Organization changes
    # - Security events
    # - Complete audit trail
    
    event = await workos.webhooks.verify_and_construct_event(
        payload=await request.body(),
        signature=request.headers.get('workos-signature'),
        secret=WORKOS_WEBHOOK_SECRET
    )
    
    await maritime_audit_service.log_auth_event(event)
```

#### Without SDKs ❌
```python
# Manual audit logging implementation
class ManualAuditLogger:
    async def log_authentication_events(self):
        # 1. Track login attempts manually
        # 2. Implement session tracking
        # 3. Monitor security events
        # 4. Handle compliance requirements
        # 5. Ensure 7-year data retention
        # Result: Complex audit system
```

## Cost-Benefit Analysis

### Total Cost of Ownership

#### With WorkOS SDKs ✅
- **Development Time**: 2-4 hours setup
- **Maintenance**: Minimal (SDK updates)
- **Security**: Enterprise-grade (managed by WorkOS)
- **Compliance**: Built-in audit trails
- **Testing**: Standard unit tests
- **Total Cost**: Low

#### Manual Implementation ❌
- **Development Time**: 2-3 weeks initial implementation
- **Maintenance**: Ongoing security updates, bug fixes
- **Security**: Your responsibility (vulnerabilities = your problem)
- **Compliance**: Custom audit system required
- **Testing**: Comprehensive security testing needed
- **Total Cost**: Very High

## Decision Matrix

| Criteria | WorkOS SDKs | Manual Implementation |
|----------|-------------|----------------------|
| **Security** | ✅ Enterprise-grade | ❌ Your responsibility |
| **Development Speed** | ✅ 2-4 hours | ❌ 2-3 weeks |
| **Maintenance** | ✅ Minimal | ❌ High ongoing effort |
| **Reliability** | ✅ Battle-tested | ❌ Custom bugs |
| **Compliance** | ✅ Built-in | ❌ Custom implementation |
| **Performance** | ✅ Optimized | ❌ Depends on your implementation |
| **Future-Proofing** | ✅ Automatic updates | ❌ Manual updates required |
| **Team Productivity** | ✅ Focus on business logic | ❌ Focus on auth plumbing |

## Final Recommendation

### ✅ Use Both WorkOS SDKs

**For React Frontend**:
```bash
npm install @workos-inc/authkit-react
```

**For Python Backend**:
```bash
pip install workos
```

### Implementation Strategy
1. **Start with SDKs**: Get authentication working in 2-4 hours
2. **Layer Maritime Logic**: Add vessel permissions on top
3. **Focus on Business Value**: Spend time on maritime features, not auth plumbing
4. **Leverage WorkOS Security**: Trust enterprise-grade authentication

### Why This Decision Makes Business Sense
- **Faster Time to Market**: 2-4 hours vs 2-3 weeks
- **Lower Risk**: Proven security vs custom vulnerabilities  
- **Better ROI**: Team focuses on maritime business logic
- **Scalable**: WorkOS handles growth, you handle vessels
- **Compliant**: Built-in audit trails for maritime regulations

**Bottom Line**: Use the SDKs. They exist for good reasons, and trying to bypass them creates more problems than they solve.