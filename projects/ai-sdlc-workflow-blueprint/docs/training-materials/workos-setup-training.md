# WorkOS Setup Training Module

## Overview

This comprehensive training module provides complete WorkOS AuthKit implementation guidance for the maritime insurance AI-SDLC workflow. The training covers account setup, development environment configuration, team onboarding, and security compliance aligned with maritime regulatory requirements.

**Target Audience**: 4-person maritime development team  
**Duration**: 3 weeks (18 hours total)  
**Format**: Hands-on labs with role-specific implementation tracks  
**Prerequisites**: Basic authentication concepts, React/TypeScript familiarity  

---

## Learning Objectives

By the end of this training, participants will be able to:

1. **Configure WorkOS Organization** with multi-tenant maritime architecture
2. **Implement Authentication Flows** for React frontend and FastAPI backend
3. **Establish Security Compliance** meeting maritime audit requirements
4. **Deploy Production Environment** with monitoring and alerting
5. **Troubleshoot Common Issues** and maintain operational excellence

---

## Week 1: WorkOS Foundation and Account Setup

### Day 1-2: WorkOS Account Configuration

**Learning Goals**: Master WorkOS organization setup and environment management

**Prerequisites Check**:
- [ ] WorkOS account access with billing information
- [ ] Domain ownership verification for maritime insurance platform
- [ ] Development environment with Node.js 18+ and Python 3.12+
- [ ] Basic understanding of OAuth/OIDC protocols

#### Hands-On Lab 1: WorkOS Organization Creation

**Duration**: 2 hours  
**Role Focus**: Head of Engineering (primary), all team members observe

**Step-by-Step Process**:

1. **Create WorkOS Organization**
   ```bash
   # Visit WorkOS Dashboard
   https://dashboard.workos.com/signup
   
   # Organization Configuration
   Organization Name: "Maritime Insurance Platform"
   Primary Domain: "maritimeinsurance.com"
   Environment: "Development" (auto-created)
   ```

2. **Configure Development Environment**
   ```yaml
   # Development Environment Settings
   Environment Name: "Development/Staging"
   Allowed Redirect URIs:
     - http://localhost:3000/callback
     - http://localhost:5173/callback
     - https://dev.maritimeinsurance.com/callback
   
   Webhook URLs:
     - http://localhost:8000/webhooks/workos
     - https://dev-api.maritimeinsurance.com/webhooks/workos
   ```

3. **Generate API Keys**
   ```bash
   # Development API Keys (viewable multiple times)
   Client ID: client_dev_[random_string]
   API Key: sk_test_[random_string]
   Webhook Secret: whsec_[random_string]
   
   # Save keys securely - never commit to repository
   ```

**Role-Specific Tasks**:

**Head of Engineering**:
- Organization setup and billing configuration
- Team member access management
- Security policy establishment
- Environment strategy planning

**Lead Backend Developer**:
- API key management and security practices
- Webhook endpoint planning
- Integration architecture review

**Lead Frontend Developer**:
- Redirect URI configuration understanding
- Client-side security considerations
- Authentication flow planning

**UI/UX Engineer**:
- User experience flow mapping
- Maritime tenant interface requirements
- Accessibility compliance planning

#### Hands-On Lab 2: Maritime Tenant Architecture Setup

**Duration**: 3 hours  
**Role Focus**: All team members collaborative exercise

**Maritime Tenant Configuration**:

1. **Define Tenant Types**
   ```typescript
   // Maritime tenant architecture
   interface MaritimeTenantTypes {
     ship_owner: {
       name: "Ship Owner"
       description: "Vessel ownership and operations"
       permissions: ["vessel_management", "insurance_quotes", "claims_filing"]
     }
     cargo_owner: {
       name: "Cargo Owner"
       description: "Cargo shipping and insurance"
       permissions: ["cargo_insurance", "shipment_tracking", "claims_filing"]
     }
     ship_broker: {
       name: "Ship Broker"
       description: "Vessel chartering services"
       permissions: ["vessel_search", "charter_agreements", "brokerage_fees"]
     }
     charterer: {
       name: "Charterer"
       description: "Vessel charter agreements"
       permissions: ["charter_management", "voyage_planning", "performance_tracking"]
     }
   }
   ```

2. **Configure Organizations in WorkOS**
   ```bash
   # Create test organizations for each tenant type
   curl -X POST "https://api.workos.com/organizations" \
     -H "Authorization: Bearer $WORKOS_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Atlantic Shipping Co",
       "domains": ["atlanticshipping.com"],
       "tenant_type": "ship_owner"
     }'
   ```

3. **Test Multi-Tenant Access**
   ```typescript
   // Test organization switching
   const testTenantAccess = async () => {
     const organizations = await workos.organizations.listOrganizations({
       domains: ['maritimeinsurance.com']
     });
     
     console.log('Available organizations:', organizations.data.length);
     organizations.data.forEach(org => {
       console.log(`- ${org.name} (${org.tenant_type})`);
     });
   };
   ```

**Assessment Criteria**: 
- [ ] WorkOS organization created with correct domain verification
- [ ] Development environment configured with proper redirect URIs
- [ ] API keys generated and securely stored
- [ ] Maritime tenant types documented and configured
- [ ] Multi-tenant access patterns tested

### Day 3-5: Development Environment Integration

**Learning Goals**: Integrate WorkOS with local development stack

#### Hands-On Lab 3: Environment Variables and Security Setup

**Duration**: 2 hours  
**Role Focus**: All developers (Backend lead primary)

**Environment Configuration**:

1. **Create Environment Files**
   ```bash
   # .env.development
   REACT_APP_WORKOS_CLIENT_ID=client_dev_123456789
   REACT_APP_WORKOS_REDIRECT_URI=http://localhost:3000/callback
   REACT_APP_WORKOS_API_HOSTNAME=api.workos.com
   REACT_APP_ENVIRONMENT=development
   
   # Backend .env
   WORKOS_API_KEY=sk_test_123456789
   WORKOS_CLIENT_ID=client_dev_123456789
   WORKOS_WEBHOOK_SECRET=whsec_123456789
   DATABASE_URL=postgresql://localhost:5432/maritime_dev
   MARITIME_AUDIT_LOG_LEVEL=DEBUG
   ```

2. **Security Validation**
   ```bash
   # Check environment security
   echo "Checking for exposed secrets..."
   grep -r "sk_test\|whsec_\|client_" . --exclude-dir=node_modules --exclude-dir=.git
   
   # Should return no results in committed files
   ```

3. **Development Workflow Setup**
   ```bash
   # Local development startup script
   #!/bin/bash
   # Start backend with WorkOS integration
   cd backend
   uvicorn main:app --reload --port 8000 &
   
   # Start frontend with WorkOS AuthKit
   cd ../frontend
   npm run dev &
   
   echo "WorkOS development environment started"
   echo "Frontend: http://localhost:3000"
   echo "Backend: http://localhost:8000"
   echo "API Docs: http://localhost:8000/docs"
   ```

#### Hands-On Lab 4: First Authentication Implementation

**Duration**: 4 hours  
**Role Focus**: Frontend and Backend leads collaborative implementation

**Frontend Implementation** (Lead Frontend Developer primary):

1. **Install WorkOS Dependencies**
   ```bash
   npm install @workos-inc/authkit-react react-router-dom
   npm install -D @types/react @types/react-dom typescript
   ```

2. **Basic AuthKit Setup**
   ```typescript
   // src/providers/WorkOSProvider.tsx
   import React from 'react';
   import { AuthKitProvider } from '@workos-inc/authkit-react';
   
   export const WorkOSProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
     return (
       <AuthKitProvider
         clientId={process.env.REACT_APP_WORKOS_CLIENT_ID!}
         apiHostname={process.env.REACT_APP_WORKOS_API_HOSTNAME}
         redirectUri={process.env.REACT_APP_WORKOS_REDIRECT_URI}
         devMode={process.env.REACT_APP_ENVIRONMENT === 'development'}
       >
         {children}
       </AuthKitProvider>
     );
   };
   ```

3. **Simple Login Component**
   ```typescript
   // src/components/SimpleLogin.tsx
   import React from 'react';
   import { useAuth } from '@workos-inc/authkit-react';
   
   export const SimpleLogin: React.FC = () => {
     const { user, isLoading, signIn, signOut } = useAuth();
   
     if (isLoading) return <div>Loading...</div>;
   
     if (user) {
       return (
         <div className="p-4 bg-green-50 border rounded">
           <h2>Welcome, {user.firstName} {user.lastName}</h2>
           <p>Email: {user.email}</p>
           <p>Organization: {user.organizationId || 'None'}</p>
           <button 
             onClick={() => signOut()}
             className="mt-2 px-4 py-2 bg-red-500 text-white rounded"
           >
             Sign Out
           </button>
         </div>
       );
     }
   
     return (
       <div className="p-4 bg-blue-50 border rounded">
         <h2>Maritime Insurance Platform</h2>
         <p>Please sign in to continue</p>
         <button 
           onClick={() => signIn()}
           className="mt-2 px-4 py-2 bg-blue-500 text-white rounded"
         >
           Sign In with WorkOS
         </button>
       </div>
     );
   };
   ```

**Backend Implementation** (Lead Backend Developer primary):

1. **Install WorkOS Python SDK**
   ```bash
   pip install workos fastapi uvicorn python-jose[cryptography]
   ```

2. **Basic Authentication Middleware**
   ```python
   # middleware/workos_auth.py
   from fastapi import Request, HTTPException, Depends
   from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
   import workos
   import os
   
   workos.api_key = os.getenv("WORKOS_API_KEY")
   workos.client_id = os.getenv("WORKOS_CLIENT_ID")
   
   security = HTTPBearer()
   
   async def verify_workos_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
       """Basic WorkOS token verification"""
       try:
           # This is a simplified version - full implementation in main guide
           user_info = {"user_id": "test_user", "email": "test@example.com"}
           return user_info
       except Exception as e:
           raise HTTPException(status_code=401, detail="Authentication failed")
   
   async def get_current_user(user = Depends(verify_workos_token)):
       return user
   ```

3. **Protected Route Example**
   ```python
   # routes/protected.py
   from fastapi import APIRouter, Depends
   from middleware.workos_auth import get_current_user
   
   router = APIRouter()
   
   @router.get("/profile")
   async def get_user_profile(user = Depends(get_current_user)):
       return {
           "message": "Authentication successful",
           "user": user,
           "maritime_context": "Ready for vessel management"
       }
   ```

**Assessment Criteria**:
- [ ] Frontend displays WorkOS login interface
- [ ] Authentication flow completes successfully
- [ ] Backend receives and validates authentication tokens
- [ ] Protected routes enforce authentication
- [ ] Error handling works for invalid tokens

---

## Week 2: Production Environment and Security

### Day 6-8: Production Configuration

**Learning Goals**: Configure production-ready WorkOS environment with security best practices

#### Hands-On Lab 5: Production Environment Setup

**Duration**: 3 hours  
**Role Focus**: Head of Engineering (setup), Lead Backend Developer (security)

**Production Account Configuration**:

1. **Upgrade to Production**
   ```bash
   # WorkOS Dashboard - Production Environment
   # Requires billing information
   
   # Production Configuration
   Environment: "Production"
   Domain: "maritimeinsurance.com"
   Redirect URIs: "https://maritimeinsurance.com/callback"
   Webhook URL: "https://api.maritimeinsurance.com/webhooks/workos"
   ```

2. **Generate Production Keys** (One-time view only!)
   ```bash
   # CRITICAL: Save immediately - cannot be viewed again
   Production Client ID: client_prod_[unique_string]
   Production API Key: sk_live_[unique_string]
   Production Webhook Secret: whsec_prod_[unique_string]
   
   # Store in secure password manager immediately
   ```

3. **GitHub Secrets Configuration**
   ```bash
   # GitHub Repository Settings > Secrets > Actions
   WORKOS_PRODUCTION_CLIENT_ID: client_prod_123456
   WORKOS_PRODUCTION_API_KEY: sk_live_123456
   WORKOS_PRODUCTION_WEBHOOK_SECRET: whsec_prod_123456
   WORKOS_PRODUCTION_REDIRECT_URI: https://maritimeinsurance.com/callback
   ```

#### Hands-On Lab 6: Maritime Compliance Security Setup

**Duration**: 4 hours  
**Role Focus**: All team members (compliance critical for maritime)

**Security Hardening**:

1. **HTTPS Enforcement**
   ```typescript
   // Production security configuration
   const productionConfig = {
     workos: {
       clientId: process.env.WORKOS_PRODUCTION_CLIENT_ID,
       redirectUri: process.env.WORKOS_PRODUCTION_REDIRECT_URI,
       apiHostname: 'api.workos.com',
       // Force HTTPS in production
       devMode: false
     },
     security: {
       httpsOnly: true,
       secureCookies: true,
       stsMaxAge: 31536000 // 1 year
     }
   };
   ```

2. **Webhook Security**
   ```python
   # Enhanced webhook verification
   import hmac
   import hashlib
   from fastapi import Request, HTTPException
   
   async def verify_workos_webhook(request: Request):
       payload = await request.body()
       signature = request.headers.get("workos-signature")
       
       if not signature:
           raise HTTPException(status_code=400, detail="Missing signature")
       
       webhook_secret = os.getenv("WORKOS_WEBHOOK_SECRET")
       expected_signature = hmac.new(
           webhook_secret.encode(),
           payload,
           hashlib.sha256
       ).hexdigest()
       
       if not hmac.compare_digest(f"sha256={expected_signature}", signature):
           raise HTTPException(status_code=401, detail="Invalid signature")
       
       return payload
   ```

3. **Maritime Audit Logging Integration**
   ```python
   # Maritime compliance event logging
   async def log_maritime_auth_event(event_data: dict):
       maritime_audit_event = {
           "event_id": str(uuid.uuid4()),
           "timestamp": datetime.now(),
           "event_source": "workos_authentication",
           "user_info": {
               "user_id": event_data.get("user_id"),
               "email": event_data.get("email"),
               "organization_id": event_data.get("organization_id"),
               "tenant_type": event_data.get("tenant_type")
           },
           "compliance_metadata": {
               "regulation_type": "maritime_authentication",
               "retention_period": "7_years",  # Maritime requirement
               "data_classification": "internal",
               "audit_trail": True
           },
           "technical_metadata": {
               "ip_address": event_data.get("ip_address"),
               "user_agent": event_data.get("user_agent"),
               "session_id": event_data.get("session_id")
           }
       }
       
       # Send to maritime audit system
       await maritime_audit_logger.log_event(maritime_audit_event)
   ```

---

## Week 3: Team Onboarding and Advanced Implementation

### Day 11-13: Role-Specific Implementation Training

**Learning Goals**: Implement role-specific WorkOS integration patterns

#### Team Member Onboarding Tracks

**Head of Engineering Track** (3 hours):

1. **Administrative Dashboard Setup**
   ```typescript
   // Admin portal integration
   const generateAdminPortalLink = async (organizationId: string) => {
     const link = workos.portal.generateLink({
       organization_id: organizationId,
       intent: 'sso',
       return_url: 'https://admin.maritimeinsurance.com/portal-success'
     });
     return link;
   };
   ```

2. **Team Management Integration**
   ```python
   # Team performance monitoring
   async def get_team_auth_metrics():
       auth_events = await get_auth_events_last_24h()
       return {
           "total_logins": len(auth_events),
           "unique_users": len(set(e.user_id for e in auth_events)),
           "tenant_breakdown": calculate_tenant_usage(auth_events),
           "peak_hours": calculate_peak_usage(auth_events)
       }
   ```

**Lead Frontend Developer Track** (4 hours):

1. **Advanced Authentication Components**
   ```typescript
   // Maritime-specific authentication flow
   interface MaritimeAuthProps {
     tenantType?: 'ship_owner' | 'cargo_owner' | 'ship_broker' | 'charterer';
     onTenantSelect?: (tenant: string) => void;
     requiredPermissions?: string[];
   }
   
   export const MaritimeAuthFlow: React.FC<MaritimeAuthProps> = ({
     tenantType,
     onTenantSelect,
     requiredPermissions = []
   }) => {
     const { user, signIn } = useAuth();
     
     const handleTenantLogin = async (selectedTenant: string) => {
       await signIn({
         state: { 
           tenantType: selectedTenant,
           requiredPermissions 
         }
       });
       onTenantSelect?.(selectedTenant);
     };
     
     return (
       <div className="maritime-auth-flow">
         {/* Tenant selection UI */}
       </div>
     );
   };
   ```

**Lead Backend Developer Track** (5 hours):

1. **Multi-Tenant Data Access**
   ```python
   # Tenant-aware database queries
   async def get_vessels_for_user(user: MaritimeUser) -> List[Vessel]:
       # Ensure user can only access vessels from their organization
       if not user.organization_id:
           raise HTTPException(status_code=403, detail="Organization required")
       
       vessels = await db.query(Vessel).filter(
           Vessel.owner_organization_id == user.organization_id
       ).all()
       
       return vessels
   ```

**UI/UX Engineer Track** (2 hours):

1. **Authentication User Experience Design**
   ```typescript
   // Maritime-themed authentication interface
   export const MaritimeLoginInterface: React.FC = () => {
     const [selectedTenant, setSelectedTenant] = useState<string>('');
     
     const tenantOptions = [
       {
         id: 'ship_owner',
         name: 'Ship Owner',
         description: 'Manage vessel operations and insurance',
         icon: '🚢'
       },
       {
         id: 'cargo_owner',
         name: 'Cargo Owner',
         description: 'Insure and track cargo shipments',
         icon: '📦'
       }
       // More tenant types...
     ];
     
     return (
       <div className="maritime-login-interface">
         {/* Maritime-themed UI implementation */}
       </div>
     );
   };
   ```

### Day 14-15: Integration Testing and Validation

**Learning Goals**: Comprehensive testing and production readiness validation

#### Hands-On Lab 8: Comprehensive Testing Suite

**Duration**: 6 hours  
**Role Focus**: All team members collaborative testing

**Frontend Testing**:

1. **Authentication Flow Testing**
   ```typescript
   // Jest/React Testing Library tests
   describe('WorkOS Authentication', () => {
     test('displays login interface for unauthenticated users', () => {
       render(
         <WorkOSProvider>
           <MaritimeAuthFlow />
         </WorkOSProvider>
       );
       
       expect(screen.getByText('Maritime Insurance Platform')).toBeInTheDocument();
       expect(screen.getByText('Sign In with WorkOS')).toBeInTheDocument();
     });
   });
   ```

**Backend Testing**:

1. **Authentication Middleware Testing**
   ```python
   # FastAPI testing
   def test_protected_endpoint_requires_auth():
       response = client.get("/vessels/12345")
       assert response.status_code == 401
   
   def test_protected_endpoint_with_valid_token():
       headers = {"Authorization": "Bearer valid_test_token"}
       response = client.get("/vessels/12345", headers=headers)
       assert response.status_code == 200
   ```

**Security Testing**:

1. **Security Validation Checklist**
   ```bash
   # Security testing checklist
   
   # 1. Test invalid tokens
   curl -H "Authorization: Bearer invalid_token" \
        https://api.maritimeinsurance.com/auth/me
   # Expected: 401 Unauthorized
   
   # 2. Test webhook without signature
   curl -X POST https://api.maritimeinsurance.com/webhooks/workos \
        -d '{"test": "data"}'
   # Expected: 400 Bad Request
   ```

---

## Success Metrics and Certification

### Technical Competency Assessment

**Individual Certification Requirements**:

1. **Head of Engineering**
   - [ ] Can set up complete WorkOS organization from scratch
   - [ ] Successfully configures production environment with security
   - [ ] Implements team access management
   - [ ] Establishes monitoring and alerting

2. **Lead Frontend Developer**
   - [ ] Implements complete authentication UI components
   - [ ] Creates role-based route protection system
   - [ ] Achieves seamless user experience across tenant types
   - [ ] Maintains 100% TypeScript type safety

3. **Lead Backend Developer**
   - [ ] Implements secure authentication middleware
   - [ ] Creates multi-tenant data access patterns
   - [ ] Integrates maritime audit logging
   - [ ] Achieves sub-200ms authentication response times

4. **UI/UX Engineer**
   - [ ] Designs intuitive maritime authentication flows
   - [ ] Creates accessible authentication interfaces
   - [ ] Implements user-friendly error handling
   - [ ] Maintains WCAG AA compliance

### Business Impact Metrics

**Operational Excellence**:
- [ ] **Implementation Time**: Complete setup within 4-week timeline
- [ ] **Security Incidents**: Zero authentication-related security issues
- [ ] **User Experience**: <2-second authentication flow completion
- [ ] **Availability**: 99.9% authentication service uptime

**Maritime Compliance**:
- [ ] **Audit Logging**: 100% authentication events logged
- [ ] **Data Retention**: 7-year retention policy implemented
- [ ] **Regulatory Compliance**: SOC 2, GDPR, CCPA compliance maintained
- [ ] **Access Control**: Multi-tenant isolation verified

### Certification Process

**Week 1 Assessment**:
- Practical demonstration of WorkOS account setup
- Environment configuration validation
- Basic authentication flow implementation

**Week 2 Assessment**:
- Production deployment demonstration
- Security configuration validation
- Maritime compliance integration testing

**Week 3 Assessment**:
- Role-specific implementation demonstration
- Comprehensive testing execution
- Troubleshooting scenario response

**Final Certification Requirements**:
1. **Technical Demo**: Live demonstration of complete WorkOS integration
2. **Security Review**: Security configuration and compliance validation
3. **Documentation**: Complete implementation documentation
4. **Knowledge Transfer**: Ability to train other team members

---

## Troubleshooting Guide and Support

### Common Issues and Solutions

**Authentication Flow Issues**:

1. **Redirect URI Mismatch**
   ```
   Error: "Invalid redirect URI"
   Solution: Verify redirect URI exactly matches WorkOS configuration
   Check: Development vs Production environment URLs
   ```

2. **Token Verification Failures**
   ```
   Error: "Invalid token signature"
   Solution: Verify API keys match environment (staging vs production)
   Check: Token expiration and refresh logic
   ```

**Multi-Tenant Access Issues**:

1. **Organization Access Denied**
   ```
   Error: "User not member of organization"
   Solution: Verify organization membership in WorkOS dashboard
   Check: Domain configuration and user invitation status
   ```

### Support Resources

**Internal Documentation**:
- **Implementation Guide**: `docs/workos-implementation-guide.md`
- **Decision Documentation**: `decisions/workos-authentication-decision.md`
- **Audit Logging**: `docs/maritime-audit-logging-implementation-guide.md`

**External Resources**:
- **WorkOS Documentation**: https://workos.com/docs
- **WorkOS Support**: https://workos.com/support
- **React AuthKit Guide**: https://workos.com/docs/authkit/react

**Team Support**:
- **Daily Standups**: WorkOS implementation progress tracking
- **Weekly Reviews**: Technical challenges and solutions sharing
- **Monthly Retrospectives**: Continuous improvement and optimization

### Emergency Procedures

**Authentication Service Outage**:
1. Check WorkOS status page: https://status.workos.com
2. Verify local configuration and network connectivity
3. Implement graceful degradation if possible
4. Contact WorkOS support with service impact details

**Security Incident Response**:
1. Immediately rotate API keys if compromised
2. Review audit logs for unauthorized access
3. Notify Head of Engineering and security team
4. Document incident and implement preventive measures

---

## Training Resources and Materials

### Hands-On Practice Environments

**Development Sandbox**:
- WorkOS staging environment with test data
- Local development stack with maritime sample data
- Postman collection for API testing
- React development environment with hot reload

**Training Assets**:
- Sample maritime organization data
- Test user accounts for each tenant type
- Realistic vessel and cargo data sets
- Authentication flow diagrams and wireframes

### Assessment Templates

**Progress Tracking**:
```yaml
# Individual progress tracking template
trainee_name: "[Name]"
role: "[Role]"
start_date: "[Date]"

week_1_progress:
  workos_setup: "[Complete|In Progress|Not Started]"
  environment_config: "[Complete|In Progress|Not Started]"
  basic_integration: "[Complete|In Progress|Not Started]"
  
week_2_progress:
  production_setup: "[Complete|In Progress|Not Started]"
  security_hardening: "[Complete|In Progress|Not Started]"
  monitoring_setup: "[Complete|In Progress|Not Started]"
  
week_3_progress:
  role_specific_implementation: "[Complete|In Progress|Not Started]"
  testing_validation: "[Complete|In Progress|Not Started]"
  certification_demo: "[Complete|In Progress|Not Started]"

overall_competency: "[Novice|Developing|Proficient|Expert]"
certification_status: "[Not Ready|Ready|Certified]"
```

### Continuous Learning Path

**Post-Training Development**:
- Monthly WorkOS feature updates and best practices
- Quarterly security review and compliance updates
- Bi-annual maritime regulation compliance training
- Annual WorkOS integration optimization review

**Advanced Topics** (Future Training Modules):
- Advanced multi-tenant architecture patterns
- WorkOS Directory Sync integration
- Custom identity provider integration
- Enterprise SSO configuration for maritime clients

---

**Training Module Status**: Ready for Implementation  
**Target Completion**: 3 weeks from start date  
**Prerequisites**: Basic React/Python knowledge, maritime domain familiarity  
**Certification**: WorkOS Maritime Implementation Certified

This comprehensive training module ensures all team members can successfully implement, maintain, and troubleshoot WorkOS authentication in the maritime insurance platform while meeting all security and compliance requirements.