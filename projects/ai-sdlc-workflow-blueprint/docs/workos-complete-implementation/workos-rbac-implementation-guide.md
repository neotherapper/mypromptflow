# WorkOS Role-Based Access Control (RBAC) Implementation Guide

## Executive Summary

This guide provides the definitive approach for implementing Role-Based Access Control (RBAC) in the maritime insurance platform using a **hybrid storage strategy** that combines JWT tokens for basic roles with database storage for detailed permissions.

**Recommended Approach**: Store **basic roles** in JWT tokens, **detailed permissions** in database.

## RBAC Storage Strategy

### Overview Architecture

```mermaid
graph TB
    subgraph "JWT Token (Fast Access)"
        JR[Basic Roles]
        JT[Tenant Type]
        JO[Organization ID]
    end
    
    subgraph "Database (Detailed Permissions)"
        VP[Vessel Permissions]
        GP[Geographic Permissions]
        TP[Time-based Permissions]
        AP[Action-specific Permissions]
    end
    
    subgraph "Performance Layer"
        RC[Redis Cache]
        MC[Memory Cache]
    end
    
    subgraph "API Request Flow"
        AR[API Request] --> BC[Basic Check - JWT]
        BC --> DC{Detailed Check Needed?}
        DC -->|No| AA[Allow Access]
        DC -->|Yes| RC
        RC --> DP[Database Permissions]
        DP --> CA[Combined Authorization]
        CA --> AA
    end
    
    JR --> BC
    VP --> DP
    GP --> DP
    TP --> DP
    AP --> DP
```

## 1. JWT Token Storage (Basic Roles) ✅

### What to Store in JWT

```json
{
  "sub": "user_01234567890",
  "email": "captain@maritimecompany.com",
  "given_name": "Captain",
  "family_name": "Smith", 
  "org": "org_maritime_company_001",
  "roles": ["vessel_operator", "tenant_admin"],
  "tenant_type": "ship_owner",
  "iss": "https://api.workos.com",
  "aud": "your-workos-client-id",
  "iat": 1704067200,
  "exp": 1704070800
}
```

### JWT Role Definitions

```python
# JWT Roles Configuration
JWT_ROLES = {
    # Platform-level roles
    "platform_admin": {
        "description": "Platform-wide administration access",
        "scope": "global",
        "permissions": ["manage_all_tenants", "system_configuration"]
    },
    
    # Organization-level roles  
    "tenant_admin": {
        "description": "Organization administration",
        "scope": "organization",
        "permissions": ["manage_users", "configure_organization", "view_audit_logs"]
    },
    "tenant_user": {
        "description": "Standard organization member",
        "scope": "organization", 
        "permissions": ["view_organization_data", "basic_operations"]
    },
    
    # Functional roles
    "vessel_operator": {
        "description": "Can operate vessel systems",
        "scope": "functional",
        "permissions": ["access_vessels", "update_vessel_status", "manage_crew"]
    },
    "cargo_manager": {
        "description": "Can manage cargo operations", 
        "scope": "functional",
        "permissions": ["access_cargo", "update_cargo_status", "manage_loading"]
    },
    "policy_underwriter": {
        "description": "Can create/modify insurance policies",
        "scope": "functional", 
        "permissions": ["create_policies", "assess_risk", "set_premiums"]
    },
    "claims_adjuster": {
        "description": "Can process insurance claims",
        "scope": "functional",
        "permissions": ["process_claims", "investigate_incidents", "approve_payments"]
    },
    "broker": {
        "description": "Can access multiple tenant data",
        "scope": "cross_tenant",
        "permissions": ["access_broker_clients", "create_quotes", "manage_relationships"]
    },
    
    # Compliance roles
    "compliance_officer": {
        "description": "Can access audit trails and compliance data",
        "scope": "compliance",
        "permissions": ["view_audit_logs", "generate_reports", "investigate_violations"]
    },
    "maritime_inspector": {
        "description": "Can perform regulatory inspections",
        "scope": "regulatory",
        "permissions": ["inspect_vessels", "access_safety_records", "issue_violations"]
    }
}
```

### Advantages of JWT Storage
- ✅ **Fast Access**: No database query on every request
- ✅ **Stateless Authentication**: Works without database connectivity
- ✅ **Offline Capability**: Mobile apps can work offline
- ✅ **Reduced Database Load**: Basic role checks don't hit database
- ✅ **Caching Benefits**: Automatically cached by browsers

### Best Use Cases for JWT Roles
- Basic role identification for route protection
- Tenant-level access control
- High-frequency permission checks
- Offline/mobile application scenarios

## 2. Database Storage (Detailed Permissions) ✅

### Database Schema Design

```sql
-- Organizations table (tenant isolation)
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    tenant_type VARCHAR(50) NOT NULL, -- 'ship_owner', 'cargo_owner', 'broker', 'charterer'
    workos_organization_id VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workos_user_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) NOT NULL,
    organization_id UUID REFERENCES organizations(id),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Vessels table
CREATE TABLE vessels (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    imo_number VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    organization_id UUID REFERENCES organizations(id),
    vessel_type VARCHAR(100),
    flag_state VARCHAR(100),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Detailed vessel permissions
CREATE TABLE user_vessel_permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    vessel_id UUID REFERENCES vessels(id),
    organization_id UUID REFERENCES organizations(id),
    permissions TEXT[] DEFAULT '{}', -- Array of permission strings
    geographic_scope JSONB, -- Geographic restrictions
    valid_from TIMESTAMP DEFAULT NOW(),
    valid_until TIMESTAMP, -- NULL = permanent
    granted_by UUID REFERENCES users(id),
    granted_at TIMESTAMP DEFAULT NOW(),
    revoked_at TIMESTAMP,
    revoked_by UUID REFERENCES users(id),
    
    -- Indexes for performance
    INDEX idx_user_vessel_perms_user (user_id),
    INDEX idx_user_vessel_perms_vessel (vessel_id),
    INDEX idx_user_vessel_perms_org (organization_id),
    INDEX idx_user_vessel_perms_active (valid_from, valid_until)
);

-- Fine-grained maritime permissions  
CREATE TABLE maritime_permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    resource_type VARCHAR(50) NOT NULL, -- 'vessel', 'policy', 'claim', 'cargo'
    resource_id UUID, -- Can be vessel_id, policy_id, etc.
    permission_level VARCHAR(50) NOT NULL, -- Specific permission
    conditions JSONB, -- Geographic, time-based, or other conditions
    granted_by UUID REFERENCES users(id),
    granted_at TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT true,
    
    -- Composite index for fast lookups
    INDEX idx_maritime_perms_lookup (user_id, resource_type, resource_id, is_active)
);

-- Audit trail for permission changes
CREATE TABLE permission_audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    permission_type VARCHAR(50), -- 'vessel_permission', 'maritime_permission'
    permission_id UUID, -- ID of the permission record
    action VARCHAR(20), -- 'granted', 'revoked', 'modified'
    old_values JSONB,
    new_values JSONB,
    changed_by UUID REFERENCES users(id),
    changed_at TIMESTAMP DEFAULT NOW(),
    reason TEXT
);
```

### Detailed Permission Types

```python
# Vessel-specific permissions
VESSEL_PERMISSIONS = [
    # Read permissions
    "read_basic_info",        # View vessel name, IMO, basic details
    "read_location",          # View current vessel location
    "read_crew",             # View crew information and certifications
    "read_maintenance",       # View maintenance records and schedules
    "read_cargo",            # View cargo manifests and status
    "read_insurance",        # View insurance policies and coverage
    "read_compliance",       # View compliance documents and certifications
    
    # Write permissions
    "write_crew",            # Modify crew assignments and information
    "write_maintenance",     # Update maintenance records and schedules
    "write_cargo",           # Modify cargo assignments and manifests
    "write_location",        # Update vessel location (for authorized personnel)
    "write_compliance",      # Update compliance documents
    
    # Management permissions
    "manage_insurance",      # Create/modify insurance policies
    "manage_contracts",      # Handle charter agreements and contracts
    "manage_safety",         # Update safety protocols and incident reports
    
    # Emergency permissions
    "emergency_override",    # Emergency access (heavily logged and monitored)
    "distress_response",     # Emergency response coordination
]

# Geographic permissions
GEOGRAPHIC_PERMISSIONS = [
    "territorial_waters_access",      # Access within specific territorial waters
    "international_waters_access",   # Access in international waters
    "port_access",                   # Access to port operations and data
    "restricted_zone_access",        # Access to restricted maritime zones
    "arctic_operations",             # Special permissions for Arctic shipping
    "high_risk_area_access",         # Access to piracy or conflict zones
]

# Time-based permissions
TIME_BASED_PERMISSIONS = [
    "charter_period_access",         # Access during specific charter periods
    "seasonal_access",               # Seasonal shipping route access
    "maintenance_window_access",     # Access during maintenance periods
    "emergency_24_7_access",         # 24/7 emergency access
]

# Financial permissions
FINANCIAL_PERMISSIONS = [
    "view_vessel_costs",             # View operational costs
    "approve_expenses",              # Approve vessel-related expenses
    "access_insurance_claims",       # Process insurance claims
    "manage_charter_payments",       # Handle charter and freight payments
]
```

### Advantages of Database Storage
- ✅ **Fine-grained Control**: Vessel-specific, time-based, geographic permissions
- ✅ **Real-time Updates**: Permission changes effective immediately
- ✅ **Audit Trail**: Complete history of permission changes
- ✅ **Complex Logic**: Support for conditional and contextual permissions
- ✅ **Revocation**: Instant permission revocation capabilities
- ✅ **Regulatory Compliance**: Detailed logging for maritime authorities

## 3. Implementation Architecture

### Hybrid Permission Checking Flow

```mermaid
sequenceDiagram
    participant Client as Frontend
    participant API as FastAPI
    participant JWT as JWT Verification
    participant Cache as Redis Cache
    participant DB as PostgreSQL

    Client->>API: API Request with JWT
    API->>JWT: Verify JWT Token
    JWT-->>API: Basic Roles + User Context
    
    Note over API: Fast Path - Basic Role Check
    API->>API: Check JWT roles for basic access
    
    alt Basic Role Check Sufficient
        API-->>Client: Allow/Deny (Fast Response)
    else Detailed Permission Check Needed
        API->>Cache: Check Permission Cache
        Cache-->>API: Cache Miss/Hit
        
        alt Cache Hit
            API-->>Client: Allow/Deny (Cached Response)
        else Cache Miss
            API->>DB: Query Detailed Permissions
            DB-->>API: Permission Data
            API->>Cache: Store in Cache (5min TTL)
            API->>API: Apply Business Rules
            API-->>Client: Allow/Deny (Database Response)
        end
    end
```

### Core Implementation Classes

#### 1. Maritime User Class

```python
# models/maritime_user.py
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

class MaritimeUser(BaseModel):
    """Enhanced user model with maritime-specific context"""
    
    # Basic user information (from JWT)
    id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    
    # Organization context (from JWT)
    organization_id: Optional[str] = None
    tenant_type: Optional[str] = None  # ship_owner, cargo_owner, broker, charterer
    
    # Roles (from JWT)
    roles: List[str] = []
    
    # Detailed permissions (from database, cached)
    vessel_permissions: Dict[str, List[str]] = {}  # vessel_id -> [permissions]
    geographic_permissions: List[str] = []
    time_based_permissions: List[str] = []
    
    # Permission metadata
    permission_last_updated: Optional[datetime] = None
    cached_until: Optional[datetime] = None
    
    def has_basic_role(self, role: str) -> bool:
        """Check if user has basic role from JWT"""
        return role in self.roles
    
    def has_vessel_permission(self, vessel_id: str, permission: str) -> bool:
        """Check if user has specific vessel permission"""
        vessel_perms = self.vessel_permissions.get(vessel_id, [])
        return permission in vessel_perms
    
    def has_geographic_permission(self, permission: str) -> bool:
        """Check geographic permission"""
        return permission in self.geographic_permissions
    
    def is_tenant_admin(self) -> bool:
        """Check if user is tenant administrator"""
        return "tenant_admin" in self.roles
    
    def can_access_vessel(self, vessel_id: str) -> bool:
        """Check if user can access vessel at all"""
        return (
            self.has_basic_role("vessel_operator") and
            vessel_id in self.vessel_permissions
        )
```

#### 2. Permission Service

```python
# services/permission_service.py
from typing import List, Dict, Optional
import json
from datetime import datetime, timedelta
from sqlalchemy import select, and_, or_
from redis import Redis

class PermissionService:
    """Service for managing maritime permissions"""
    
    def __init__(self, db_session, redis_client: Redis):
        self.db = db_session
        self.redis = redis_client
        self.cache_ttl = 300  # 5 minutes
    
    async def get_user_vessel_permissions(self, user_id: str) -> Dict[str, List[str]]:
        """Get all vessel permissions for a user"""
        cache_key = f"vessel_perms:{user_id}"
        
        # Try cache first
        cached = await self.redis.get(cache_key)
        if cached:
            return json.loads(cached)
        
        # Query database
        query = select(user_vessel_permissions).where(
            and_(
                user_vessel_permissions.c.user_id == user_id,
                user_vessel_permissions.c.is_active == True,
                or_(
                    user_vessel_permissions.c.valid_until.is_(None),
                    user_vessel_permissions.c.valid_until > datetime.utcnow()
                )
            )
        )
        
        result = await self.db.execute(query)
        permissions = {}
        
        for row in result:
            vessel_id = str(row.vessel_id)
            if vessel_id not in permissions:
                permissions[vessel_id] = []
            permissions[vessel_id].extend(row.permissions)
        
        # Cache result
        await self.redis.setex(cache_key, self.cache_ttl, json.dumps(permissions))
        
        return permissions
    
    async def check_vessel_permission(
        self, 
        user_id: str, 
        vessel_id: str, 
        permission: str,
        context: Optional[Dict] = None
    ) -> bool:
        """Check specific vessel permission with context"""
        
        # Get user's vessel permissions
        vessel_permissions = await self.get_user_vessel_permissions(user_id)
        
        # Basic permission check
        user_vessel_perms = vessel_permissions.get(vessel_id, [])
        if permission not in user_vessel_perms:
            return False
        
        # Apply contextual checks if provided
        if context:
            return await self._apply_contextual_checks(
                user_id, vessel_id, permission, context
            )
        
        return True
    
    async def _apply_contextual_checks(
        self, 
        user_id: str, 
        vessel_id: str, 
        permission: str, 
        context: Dict
    ) -> bool:
        """Apply geographic, time-based, and other contextual permission checks"""
        
        # Geographic restrictions
        if "location" in context:
            location = context["location"]
            if not await self._check_geographic_permission(user_id, location):
                return False
        
        # Time-based restrictions
        if "timestamp" in context:
            timestamp = context["timestamp"]
            if not await self._check_time_based_permission(user_id, vessel_id, timestamp):
                return False
        
        # Financial amount restrictions
        if "amount" in context and permission in ["approve_expenses", "manage_charter_payments"]:
            amount = context["amount"]
            if not await self._check_financial_limit(user_id, permission, amount):
                return False
        
        return True
    
    async def grant_vessel_permission(
        self,
        user_id: str,
        vessel_id: str,
        permissions: List[str],
        granted_by: str,
        valid_until: Optional[datetime] = None,
        conditions: Optional[Dict] = None
    ) -> bool:
        """Grant vessel permissions to user"""
        
        # Insert permission record
        insert_query = user_vessel_permissions.insert().values(
            user_id=user_id,
            vessel_id=vessel_id,
            permissions=permissions,
            valid_until=valid_until,
            granted_by=granted_by,
            granted_at=datetime.utcnow(),
            conditions=conditions
        )
        
        await self.db.execute(insert_query)
        await self.db.commit()
        
        # Log audit event
        await self._log_permission_change(
            user_id, "vessel_permission", "granted", 
            {"vessel_id": vessel_id, "permissions": permissions},
            granted_by
        )
        
        # Invalidate cache
        await self._invalidate_user_cache(user_id)
        
        return True
    
    async def revoke_vessel_permission(
        self,
        user_id: str,
        vessel_id: str,
        permissions: List[str],
        revoked_by: str,
        reason: str
    ) -> bool:
        """Revoke specific vessel permissions"""
        
        # Update permission record
        update_query = (
            user_vessel_permissions.update()
            .where(
                and_(
                    user_vessel_permissions.c.user_id == user_id,
                    user_vessel_permissions.c.vessel_id == vessel_id
                )
            )
            .values(
                revoked_at=datetime.utcnow(),
                revoked_by=revoked_by,
                is_active=False
            )
        )
        
        await self.db.execute(update_query)
        await self.db.commit()
        
        # Log audit event
        await self._log_permission_change(
            user_id, "vessel_permission", "revoked",
            {"vessel_id": vessel_id, "permissions": permissions, "reason": reason},
            revoked_by
        )
        
        # Invalidate cache
        await self._invalidate_user_cache(user_id)
        
        return True
    
    async def _invalidate_user_cache(self, user_id: str):
        """Invalidate all cached permissions for user"""
        patterns = [
            f"vessel_perms:{user_id}",
            f"geo_perms:{user_id}",
            f"time_perms:{user_id}",
            f"user_perms:{user_id}:*"
        ]
        
        for pattern in patterns:
            keys = await self.redis.keys(pattern)
            if keys:
                await self.redis.delete(*keys)
```

#### 3. Permission Decorators and Dependencies

```python
# middleware/rbac_middleware.py
from functools import wraps
from typing import List, Optional, Callable
from fastapi import Depends, HTTPException, Request
from .auth_middleware import verify_workos_token, MaritimeUser

class RBACDependencies:
    """FastAPI dependencies for RBAC checks"""
    
    def __init__(self, permission_service: PermissionService):
        self.permission_service = permission_service
    
    def require_basic_role(self, required_role: str):
        """Dependency for basic role checking (JWT only)"""
        async def role_checker(user: MaritimeUser = Depends(verify_workos_token)):
            if required_role not in user.roles:
                raise HTTPException(
                    status_code=403,
                    detail=f"Role '{required_role}' required for this operation"
                )
            return user
        return role_checker
    
    def require_any_role(self, required_roles: List[str]):
        """Dependency for checking any of multiple roles"""
        async def role_checker(user: MaritimeUser = Depends(verify_workos_token)):
            if not any(role in user.roles for role in required_roles):
                raise HTTPException(
                    status_code=403,
                    detail=f"One of roles {required_roles} required"
                )
            return user
        return role_checker
    
    def require_vessel_permission(self, vessel_id_param: str, permission: str):
        """Dependency for vessel-specific permission checking"""
        async def permission_checker(
            request: Request,
            user: MaritimeUser = Depends(verify_workos_token)
        ):
            # Extract vessel_id from path parameters
            vessel_id = request.path_params.get(vessel_id_param)
            if not vessel_id:
                raise HTTPException(
                    status_code=400,
                    detail=f"Vessel ID parameter '{vessel_id_param}' not found"
                )
            
            # Check basic role first (fast check)
            if not user.has_basic_role("vessel_operator"):
                raise HTTPException(
                    status_code=403,
                    detail="Vessel operator role required"
                )
            
            # Check detailed permission (database check)
            has_permission = await self.permission_service.check_vessel_permission(
                user.id, vessel_id, permission
            )
            
            if not has_permission:
                raise HTTPException(
                    status_code=403,
                    detail=f"Permission '{permission}' denied for vessel {vessel_id}"
                )
            
            return user
        return permission_checker
    
    def require_contextual_permission(
        self, 
        resource_type: str, 
        permission: str,
        context_extractor: Callable = None
    ):
        """Dependency for contextual permission checking"""
        async def permission_checker(
            request: Request,
            user: MaritimeUser = Depends(verify_workos_token)
        ):
            # Extract context from request
            context = {}
            if context_extractor:
                context = await context_extractor(request)
            
            # Apply contextual permission check
            has_permission = await self.permission_service.check_contextual_permission(
                user.id, resource_type, permission, context
            )
            
            if not has_permission:
                raise HTTPException(
                    status_code=403,
                    detail=f"Contextual permission check failed for {resource_type}:{permission}"
                )
            
            return user
        return permission_checker

# Initialize RBAC dependencies
rbac = RBACDependencies(permission_service)
```

### 4. API Route Implementation Examples

#### Basic Role Protection

```python
# routes/vessel_routes.py
from fastapi import APIRouter, Depends
from middleware.rbac_middleware import rbac

router = APIRouter(prefix="/vessels", tags=["vessels"])

@router.get("/")
async def list_vessels(
    user: MaritimeUser = Depends(rbac.require_basic_role("vessel_operator"))
):
    """List vessels - basic role check only"""
    return await vessel_service.get_vessels_for_organization(user.organization_id)

@router.get("/{vessel_id}")
async def get_vessel(
    vessel_id: str,
    user: MaritimeUser = Depends(rbac.require_vessel_permission("vessel_id", "read_basic_info"))
):
    """Get vessel details - detailed permission check"""
    vessel = await vessel_service.get_vessel_by_id(vessel_id)
    
    # Log access for compliance
    await audit_service.log_vessel_access(
        user_id=user.id,
        vessel_id=vessel_id,
        action="view_details"
    )
    
    return vessel

@router.put("/{vessel_id}/crew")
async def update_vessel_crew(
    vessel_id: str,
    crew_data: CrewUpdateModel,
    user: MaritimeUser = Depends(rbac.require_vessel_permission("vessel_id", "write_crew"))
):
    """Update vessel crew - write permission required"""
    
    # Additional business logic validation
    if crew_data.captain_change and not user.has_basic_role("senior_vessel_operator"):
        raise HTTPException(
            status_code=403,
            detail="Senior vessel operator role required for captain changes"
        )
    
    result = await vessel_service.update_crew(vessel_id, crew_data)
    
    # Log crew change for compliance
    await audit_service.log_crew_change(
        user_id=user.id,
        vessel_id=vessel_id,
        changes=crew_data.dict(),
        action="crew_update"
    )
    
    return result
```

#### Contextual Permission Checking

```python
# Context extractors for different scenarios
async def extract_geographic_context(request: Request) -> Dict:
    """Extract geographic context from request"""
    context = {}
    
    # Get location from query parameters
    if "lat" in request.query_params and "lng" in request.query_params:
        context["location"] = {
            "latitude": float(request.query_params["lat"]),
            "longitude": float(request.query_params["lng"])
        }
    
    # Get location from request body (for POST/PUT)
    if request.method in ["POST", "PUT", "PATCH"]:
        body = await request.json()
        if "location" in body:
            context["location"] = body["location"]
    
    return context

async def extract_financial_context(request: Request) -> Dict:
    """Extract financial context from request"""
    context = {}
    
    if request.method in ["POST", "PUT", "PATCH"]:
        body = await request.json()
        if "amount" in body:
            context["amount"] = float(body["amount"])
        if "currency" in body:
            context["currency"] = body["currency"]
    
    return context

# Routes with contextual permissions
@router.post("/{vessel_id}/expenses")
async def approve_vessel_expense(
    vessel_id: str,
    expense_data: ExpenseModel,
    user: MaritimeUser = Depends(
        rbac.require_contextual_permission(
            "vessel", 
            "approve_expenses",
            extract_financial_context
        )
    )
):
    """Approve vessel expense with financial limits"""
    return await expense_service.approve_expense(vessel_id, expense_data)

@router.post("/{vessel_id}/location")
async def update_vessel_location(
    vessel_id: str,
    location_data: LocationModel,
    user: MaritimeUser = Depends(
        rbac.require_contextual_permission(
            "vessel",
            "write_location", 
            extract_geographic_context
        )
    )
):
    """Update vessel location with geographic restrictions"""
    return await vessel_service.update_location(vessel_id, location_data)
```

## 5. Performance Optimization

### Multi-Level Caching Strategy

```python
# services/cache_service.py
from typing import Dict, Optional, Any
import json
from datetime import datetime, timedelta
import asyncio

class MultiLevelCache:
    """Multi-level caching for RBAC permissions"""
    
    def __init__(self, redis_client, memory_cache_size: int = 1000):
        self.redis = redis_client
        self.memory_cache = {}  # L1 cache
        self.memory_cache_size = memory_cache_size
        self.cache_access_order = []  # For LRU eviction
    
    async def get_permission_data(self, cache_key: str) -> Optional[Dict]:
        """Get permission data with multi-level caching"""
        
        # L1 Cache: Memory (fastest)
        if cache_key in self.memory_cache:
            self._update_access_order(cache_key)
            return self.memory_cache[cache_key]
        
        # L2 Cache: Redis
        redis_data = await self.redis.get(cache_key)
        if redis_data:
            data = json.loads(redis_data)
            # Promote to L1 cache
            await self._set_memory_cache(cache_key, data)
            return data
        
        return None
    
    async def set_permission_data(
        self, 
        cache_key: str, 
        data: Dict, 
        ttl: int = 300
    ):
        """Set permission data in multi-level cache"""
        
        # Set in both caches
        await self._set_memory_cache(cache_key, data)
        await self.redis.setex(cache_key, ttl, json.dumps(data))
    
    async def _set_memory_cache(self, key: str, data: Dict):
        """Set data in memory cache with LRU eviction"""
        
        # Remove oldest if cache is full
        if len(self.memory_cache) >= self.memory_cache_size:
            oldest_key = self.cache_access_order.pop(0)
            self.memory_cache.pop(oldest_key, None)
        
        self.memory_cache[key] = data
        self._update_access_order(key)
    
    def _update_access_order(self, key: str):
        """Update LRU access order"""
        if key in self.cache_access_order:
            self.cache_access_order.remove(key)
        self.cache_access_order.append(key)
    
    async def invalidate(self, pattern: str):
        """Invalidate cache entries matching pattern"""
        
        # Invalidate memory cache
        keys_to_remove = [k for k in self.memory_cache.keys() if pattern in k]
        for key in keys_to_remove:
            self.memory_cache.pop(key, None)
            if key in self.cache_access_order:
                self.cache_access_order.remove(key)
        
        # Invalidate Redis cache
        redis_keys = await self.redis.keys(f"*{pattern}*")
        if redis_keys:
            await self.redis.delete(*redis_keys)
```

### Database Query Optimization

```sql
-- Optimized indexes for RBAC queries
CREATE INDEX CONCURRENTLY idx_user_vessel_perms_lookup 
ON user_vessel_permissions (user_id, vessel_id, is_active)
WHERE is_active = true;

CREATE INDEX CONCURRENTLY idx_user_vessel_perms_validity
ON user_vessel_permissions (user_id, valid_from, valid_until)
WHERE is_active = true;

CREATE INDEX CONCURRENTLY idx_maritime_perms_resource
ON maritime_permissions (user_id, resource_type, resource_id, is_active)
WHERE is_active = true;

-- Partitioning for audit logs (by month)
CREATE TABLE permission_audit_log_y2024m01 PARTITION OF permission_audit_log
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

-- Materialized view for frequently accessed permissions
CREATE MATERIALIZED VIEW user_active_permissions AS
SELECT 
    u.workos_user_id,
    u.organization_id,
    o.tenant_type,
    array_agg(DISTINCT uvp.vessel_id) as accessible_vessels,
    array_agg(DISTINCT unnest(uvp.permissions)) as vessel_permissions,
    array_agg(DISTINCT mp.permission_level) as maritime_permissions
FROM users u
JOIN organizations o ON u.organization_id = o.id
LEFT JOIN user_vessel_permissions uvp ON u.id = uvp.user_id 
    AND uvp.is_active = true 
    AND (uvp.valid_until IS NULL OR uvp.valid_until > NOW())
LEFT JOIN maritime_permissions mp ON u.id = mp.user_id 
    AND mp.is_active = true
WHERE u.is_active = true
GROUP BY u.workos_user_id, u.organization_id, o.tenant_type;

-- Refresh materialized view every 5 minutes
CREATE OR REPLACE FUNCTION refresh_user_permissions()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY user_active_permissions;
END;
$$ LANGUAGE plpgsql;

-- Scheduled refresh
SELECT cron.schedule('refresh-permissions', '*/5 * * * *', 'SELECT refresh_user_permissions();');
```

## 6. Security Considerations

### JWT Security Implementation

```python
# security/jwt_security.py
import jwt
from typing import Dict, List
from datetime import datetime, timedelta

class JWTSecurityHandler:
    """Enhanced JWT security for RBAC"""
    
    @staticmethod
    def validate_jwt_roles(jwt_payload: Dict) -> List[str]:
        """Validate and sanitize roles from JWT"""
        
        roles = jwt_payload.get('roles', [])
        
        # Ensure roles is a list
        if not isinstance(roles, list):
            return []
        
        # Validate each role against allowed roles
        valid_roles = []
        for role in roles:
            if isinstance(role, str) and role in JWT_ROLES:
                valid_roles.append(role)
        
        return valid_roles
    
    @staticmethod
    def check_jwt_freshness(jwt_payload: Dict, max_age_minutes: int = 30) -> bool:
        """Check if JWT is fresh enough for sensitive operations"""
        
        issued_at = jwt_payload.get('iat')
        if not issued_at:
            return False
        
        issue_time = datetime.fromtimestamp(issued_at)
        max_age = timedelta(minutes=max_age_minutes)
        
        return datetime.utcnow() - issue_time <= max_age
    
    @staticmethod
    def extract_tenant_context(jwt_payload: Dict) -> Dict:
        """Safely extract tenant context from JWT"""
        
        return {
            'organization_id': jwt_payload.get('org'),
            'tenant_type': jwt_payload.get('tenant_type', 'unknown'),
            'user_id': jwt_payload.get('sub'),
            'email': jwt_payload.get('email')
        }
```

### Permission Audit Logging

```python
# services/permission_audit_service.py
from typing import Dict, Any, Optional
import json
from datetime import datetime

class PermissionAuditService:
    """Audit logging for permission operations"""
    
    def __init__(self, db_session):
        self.db = db_session
    
    async def log_permission_check(
        self,
        user_id: str,
        resource_type: str,
        resource_id: str,
        permission: str,
        result: bool,
        context: Optional[Dict] = None
    ):
        """Log permission check for audit trail"""
        
        audit_data = {
            'user_id': user_id,
            'resource_type': resource_type,
            'resource_id': resource_id,
            'permission': permission,
            'result': result,
            'context': context or {},
            'timestamp': datetime.utcnow().isoformat(),
            'ip_address': context.get('ip_address') if context else None,
            'user_agent': context.get('user_agent') if context else None
        }
        
        # Insert audit record
        insert_query = permission_audit_log.insert().values(
            user_id=user_id,
            permission_type='permission_check',
            action='check',
            new_values=audit_data,
            changed_at=datetime.utcnow()
        )
        
        await self.db.execute(insert_query)
        await self.db.commit()
    
    async def log_permission_grant(
        self,
        user_id: str,
        permission_type: str,
        permission_details: Dict,
        granted_by: str,
        reason: str
    ):
        """Log permission grant for compliance"""
        
        audit_data = {
            'action': 'granted',
            'permission_type': permission_type,
            'permission_details': permission_details,
            'granted_by': granted_by,
            'reason': reason,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        insert_query = permission_audit_log.insert().values(
            user_id=user_id,
            permission_type=permission_type,
            action='granted',
            new_values=audit_data,
            changed_by=granted_by,
            changed_at=datetime.utcnow(),
            reason=reason
        )
        
        await self.db.execute(insert_query)
        await self.db.commit()
    
    async def generate_compliance_report(
        self,
        start_date: datetime,
        end_date: datetime,
        user_id: Optional[str] = None
    ) -> Dict:
        """Generate compliance report for maritime authorities"""
        
        # Build query
        query = select(permission_audit_log).where(
            and_(
                permission_audit_log.c.changed_at >= start_date,
                permission_audit_log.c.changed_at <= end_date
            )
        )
        
        if user_id:
            query = query.where(permission_audit_log.c.user_id == user_id)
        
        # Execute query
        result = await self.db.execute(query)
        audit_records = result.fetchall()
        
        # Generate report
        report = {
            'report_period': {
                'start': start_date.isoformat(),
                'end': end_date.isoformat()
            },
            'total_events': len(audit_records),
            'permission_grants': len([r for r in audit_records if r.action == 'granted']),
            'permission_revocations': len([r for r in audit_records if r.action == 'revoked']),
            'permission_checks': len([r for r in audit_records if r.action == 'check']),
            'events_by_user': {},
            'events_by_type': {},
            'compliance_violations': []
        }
        
        # Analyze events
        for record in audit_records:
            # Group by user
            user_id = record.user_id
            if user_id not in report['events_by_user']:
                report['events_by_user'][user_id] = 0
            report['events_by_user'][user_id] += 1
            
            # Group by type
            perm_type = record.permission_type
            if perm_type not in report['events_by_type']:
                report['events_by_type'][perm_type] = 0
            report['events_by_type'][perm_type] += 1
        
        return report
```

## 7. Maritime-Specific Permission Examples

### Vessel Operation Permissions

```python
# Example: Complex vessel permission checking
async def check_vessel_navigation_permission(
    user_id: str,
    vessel_id: str,
    destination: Dict,
    departure_time: datetime
) -> bool:
    """Check if user can authorize vessel navigation"""
    
    # Step 1: Basic role check (JWT)
    user = await get_user_with_roles(user_id)
    if "vessel_operator" not in user.roles:
        return False
    
    # Step 2: Vessel access check
    if not await permission_service.check_vessel_permission(
        user_id, vessel_id, "write_navigation"
    ):
        return False
    
    # Step 3: Geographic permission check
    destination_zone = await determine_maritime_zone(destination)
    if destination_zone == "restricted" and not await permission_service.check_geographic_permission(
        user_id, "restricted_zone_access"
    ):
        return False
    
    # Step 4: Time-based permission check
    if not await check_navigation_time_window(user_id, vessel_id, departure_time):
        return False
    
    # Step 5: Vessel status check
    vessel_status = await get_vessel_status(vessel_id)
    if vessel_status.under_maintenance and not await permission_service.check_vessel_permission(
        user_id, vessel_id, "emergency_override"
    ):
        return False
    
    return True

# Usage in API endpoint
@router.post("/{vessel_id}/navigation")
async def authorize_navigation(
    vessel_id: str,
    navigation_plan: NavigationPlanModel,
    user: MaritimeUser = Depends(verify_workos_token)
):
    """Authorize vessel navigation with complex permission checking"""
    
    # Complex permission check
    can_navigate = await check_vessel_navigation_permission(
        user.id,
        vessel_id,
        navigation_plan.destination,
        navigation_plan.departure_time
    )
    
    if not can_navigate:
        raise HTTPException(
            status_code=403,
            detail="Navigation authorization denied - insufficient permissions"
        )
    
    # Execute navigation authorization
    result = await navigation_service.authorize_navigation(vessel_id, navigation_plan)
    
    # Log for maritime compliance
    await audit_service.log_navigation_authorization(
        user_id=user.id,
        vessel_id=vessel_id,
        navigation_plan=navigation_plan,
        authorization_result=result
    )
    
    return result
```

### Financial Transaction Permissions

```python
# Example: Financial permission with amount limits
async def check_financial_permission(
    user_id: str,
    transaction_type: str,
    amount: float,
    currency: str = "USD"
) -> bool:
    """Check financial transaction permissions with amount limits"""
    
    # Get user's financial permissions
    financial_perms = await permission_service.get_financial_permissions(user_id)
    
    # Check base permission
    if transaction_type not in financial_perms:
        return False
    
    # Check amount limits
    permission_config = financial_perms[transaction_type]
    
    # Convert to USD for limit checking
    usd_amount = await currency_service.convert_to_usd(amount, currency)
    
    # Check daily limit
    daily_spent = await get_daily_spending(user_id, transaction_type)
    if daily_spent + usd_amount > permission_config.daily_limit:
        return False
    
    # Check single transaction limit
    if usd_amount > permission_config.single_transaction_limit:
        return False
    
    # Check approval requirements for large amounts
    if usd_amount > permission_config.approval_threshold:
        if not await check_supervisor_approval(user_id, transaction_type, amount):
            return False
    
    return True

# Financial permission configuration
FINANCIAL_PERMISSIONS = {
    "vessel_operator": {
        "approve_fuel_expenses": {
            "daily_limit": 10000,  # USD
            "single_transaction_limit": 5000,
            "approval_threshold": 2000
        },
        "approve_port_fees": {
            "daily_limit": 5000,
            "single_transaction_limit": 2000,
            "approval_threshold": 1000
        }
    },
    "fleet_manager": {
        "approve_maintenance_expenses": {
            "daily_limit": 50000,
            "single_transaction_limit": 25000,
            "approval_threshold": 10000
        },
        "approve_charter_payments": {
            "daily_limit": 100000,
            "single_transaction_limit": 75000,
            "approval_threshold": 25000
        }
    }
}
```

## 8. Testing Strategy

### Unit Tests for RBAC

```python
# tests/test_rbac_permissions.py
import pytest
from datetime import datetime, timedelta
from services.permission_service import PermissionService
from models.maritime_user import MaritimeUser

@pytest.fixture
async def permission_service():
    # Setup test database and Redis
    db = await setup_test_database()
    redis = await setup_test_redis()
    return PermissionService(db, redis)

@pytest.fixture
def sample_user():
    return MaritimeUser(
        id="user_123",
        email="captain@example.com",
        organization_id="org_456",
        tenant_type="ship_owner",
        roles=["vessel_operator", "tenant_user"]
    )

class TestBasicRBAC:
    """Test basic RBAC functionality"""
    
    async def test_jwt_role_checking(self, sample_user):
        """Test basic role checking from JWT"""
        assert sample_user.has_basic_role("vessel_operator")
        assert sample_user.has_basic_role("tenant_user")
        assert not sample_user.has_basic_role("platform_admin")
    
    async def test_vessel_permission_grant(self, permission_service, sample_user):
        """Test granting vessel permissions"""
        vessel_id = "vessel_789"
        permissions = ["read_basic_info", "write_crew"]
        
        # Grant permissions
        result = await permission_service.grant_vessel_permission(
            sample_user.id,
            vessel_id,
            permissions,
            granted_by="admin_user"
        )
        
        assert result is True
        
        # Verify permissions were granted
        user_perms = await permission_service.get_user_vessel_permissions(sample_user.id)
        assert vessel_id in user_perms
        assert "read_basic_info" in user_perms[vessel_id]
        assert "write_crew" in user_perms[vessel_id]
    
    async def test_permission_caching(self, permission_service, sample_user):
        """Test permission caching functionality"""
        vessel_id = "vessel_789"
        
        # First call - should hit database
        perms1 = await permission_service.get_user_vessel_permissions(sample_user.id)
        
        # Second call - should hit cache
        perms2 = await permission_service.get_user_vessel_permissions(sample_user.id)
        
        assert perms1 == perms2
        
        # Verify cache key exists
        cache_key = f"vessel_perms:{sample_user.id}"
        cached_data = await permission_service.redis.get(cache_key)
        assert cached_data is not None

class TestContextualPermissions:
    """Test contextual permission checking"""
    
    async def test_geographic_restrictions(self, permission_service, sample_user):
        """Test geographic-based permission restrictions"""
        vessel_id = "vessel_789"
        
        # Grant basic permission
        await permission_service.grant_vessel_permission(
            sample_user.id,
            vessel_id,
            ["write_navigation"],
            granted_by="admin_user"
        )
        
        # Test permission in allowed zone
        allowed_context = {
            "location": {"latitude": 40.7128, "longitude": -74.0060}  # New York
        }
        result = await permission_service.check_vessel_permission(
            sample_user.id, vessel_id, "write_navigation", allowed_context
        )
        assert result is True
        
        # Test permission in restricted zone
        restricted_context = {
            "location": {"latitude": 0.0, "longitude": 0.0}  # Restricted zone
        }
        result = await permission_service.check_vessel_permission(
            sample_user.id, vessel_id, "write_navigation", restricted_context
        )
        # Should be False if user doesn't have restricted zone access
        assert result is False
    
    async def test_time_based_permissions(self, permission_service, sample_user):
        """Test time-based permission restrictions"""
        vessel_id = "vessel_789"
        
        # Grant permission with time restriction
        valid_until = datetime.utcnow() + timedelta(hours=1)
        await permission_service.grant_vessel_permission(
            sample_user.id,
            vessel_id,
            ["manage_crew"],
            granted_by="admin_user",
            valid_until=valid_until
        )
        
        # Test within valid time
        result = await permission_service.check_vessel_permission(
            sample_user.id, vessel_id, "manage_crew"
        )
        assert result is True
        
        # Mock time passage (in real test, you'd use time mocking)
        # After expiration, permission should be denied
        # This would require mocking datetime.utcnow()
    
    async def test_financial_amount_limits(self, permission_service, sample_user):
        """Test financial permission amount limits"""
        context = {"amount": 15000, "currency": "USD"}
        
        # Test within limit
        result = await permission_service.check_contextual_permission(
            sample_user.id,
            "vessel",
            "approve_expenses",
            context
        )
        
        # Result depends on user's financial limits configuration
        # This test would verify the limit checking logic

class TestPermissionRevocation:
    """Test permission revocation and audit"""
    
    async def test_permission_revocation(self, permission_service, sample_user):
        """Test revoking permissions"""
        vessel_id = "vessel_789"
        permissions = ["read_basic_info", "write_crew"]
        
        # Grant permissions first
        await permission_service.grant_vessel_permission(
            sample_user.id,
            vessel_id,
            permissions,
            granted_by="admin_user"
        )
        
        # Revoke permissions
        result = await permission_service.revoke_vessel_permission(
            sample_user.id,
            vessel_id,
            permissions,
            revoked_by="admin_user",
            reason="Security policy change"
        )
        
        assert result is True
        
        # Verify permissions were revoked
        user_perms = await permission_service.get_user_vessel_permissions(sample_user.id)
        assert vessel_id not in user_perms or len(user_perms[vessel_id]) == 0
    
    async def test_audit_trail_creation(self, permission_service, sample_user):
        """Test that permission changes create audit trail"""
        vessel_id = "vessel_789"
        
        # Grant permission (should create audit entry)
        await permission_service.grant_vessel_permission(
            sample_user.id,
            vessel_id,
            ["read_basic_info"],
            granted_by="admin_user"
        )
        
        # Verify audit trail exists
        audit_records = await get_audit_records(sample_user.id, "vessel_permission")
        assert len(audit_records) > 0
        assert audit_records[-1].action == "granted"

# Integration tests
class TestRBACIntegration:
    """Test RBAC integration with API endpoints"""
    
    async def test_api_endpoint_protection(self, test_client, sample_user):
        """Test that API endpoints are properly protected"""
        
        # Test endpoint without authentication - should fail
        response = await test_client.get("/vessels/123")
        assert response.status_code == 401
        
        # Test endpoint with authentication but insufficient role - should fail
        token = create_test_jwt(roles=["basic_user"])
        response = await test_client.get(
            "/vessels/123",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 403
        
        # Test endpoint with proper authentication and role - should succeed
        token = create_test_jwt(roles=["vessel_operator"])
        response = await test_client.get(
            "/vessels/123", 
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
```

## 9. Monitoring and Metrics

### RBAC Metrics Collection

```python
# monitoring/rbac_metrics.py
from prometheus_client import Counter, Histogram, Gauge
import time

# Permission check metrics
PERMISSION_CHECKS_TOTAL = Counter(
    'maritime_permission_checks_total',
    'Total permission checks performed',
    ['user_role', 'permission_type', 'result']
)

PERMISSION_CHECK_DURATION = Histogram(
    'maritime_permission_check_duration_seconds',
    'Duration of permission checks',
    ['permission_type', 'cache_hit']
)

# Active permissions metrics
ACTIVE_PERMISSIONS = Gauge(
    'maritime_active_permissions_total',
    'Number of active permissions by type',
    ['permission_type', 'organization']
)

# Cache metrics
CACHE_HITS_TOTAL = Counter(
    'maritime_rbac_cache_hits_total',
    'Total cache hits for RBAC',
    ['cache_level']  # memory, redis, database
)

CACHE_MISSES_TOTAL = Counter(
    'maritime_rbac_cache_misses_total', 
    'Total cache misses for RBAC',
    ['cache_level']
)

class RBACMetrics:
    """Metrics collection for RBAC operations"""
    
    @staticmethod
    def record_permission_check(
        user_role: str,
        permission_type: str,
        result: bool,
        duration: float,
        cache_hit: bool
    ):
        """Record permission check metrics"""
        
        PERMISSION_CHECKS_TOTAL.labels(
            user_role=user_role,
            permission_type=permission_type,
            result=str(result).lower()
        ).inc()
        
        PERMISSION_CHECK_DURATION.labels(
            permission_type=permission_type,
            cache_hit=str(cache_hit).lower()
        ).observe(duration)
    
    @staticmethod
    def record_cache_access(cache_level: str, hit: bool):
        """Record cache access metrics"""
        
        if hit:
            CACHE_HITS_TOTAL.labels(cache_level=cache_level).inc()
        else:
            CACHE_MISSES_TOTAL.labels(cache_level=cache_level).inc()
    
    @staticmethod
    async def update_active_permissions_gauge(permission_service):
        """Update active permissions gauge"""
        
        # Get active permission counts by type and organization
        permission_counts = await permission_service.get_active_permission_counts()
        
        for perm_type, org_counts in permission_counts.items():
            for org_id, count in org_counts.items():
                ACTIVE_PERMISSIONS.labels(
                    permission_type=perm_type,
                    organization=org_id
                ).set(count)

# Decorator for automatic metrics collection
def track_permission_check(permission_type: str):
    """Decorator to automatically track permission check metrics"""
    
    def decorator(func):
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            cache_hit = False
            result = False
            user_role = "unknown"
            
            try:
                # Extract user role if available
                if 'user' in kwargs and hasattr(kwargs['user'], 'roles'):
                    user_role = ','.join(kwargs['user'].roles)
                
                # Call the actual function
                result = await func(*args, **kwargs)
                
                # Check if result came from cache (simplified check)
                duration = time.time() - start_time
                cache_hit = duration < 0.01  # Very fast = likely cached
                
                return result
                
            finally:
                # Record metrics
                duration = time.time() - start_time
                RBACMetrics.record_permission_check(
                    user_role, permission_type, result, duration, cache_hit
                )
        
        return wrapper
    return decorator
```

### Alerting Configuration

```yaml
# prometheus/rbac_alerts.yml
groups:
  - name: maritime_rbac_alerts
    rules:
      - alert: HighPermissionCheckFailureRate
        expr: rate(maritime_permission_checks_total{result="false"}[5m]) > 0.1
        for: 2m
        labels:
          severity: warning
          component: rbac
        annotations:
          summary: "High permission check failure rate"
          description: "Permission check failure rate is {{ $value }} per second"
      
      - alert: RBACCacheHitRateLow
        expr: |
          (
            rate(maritime_rbac_cache_hits_total[5m]) / 
            (rate(maritime_rbac_cache_hits_total[5m]) + rate(maritime_rbac_cache_misses_total[5m]))
          ) < 0.8
        for: 5m
        labels:
          severity: warning
          component: rbac
        annotations:
          summary: "RBAC cache hit rate is low"
          description: "Cache hit rate is {{ $value | humanizePercentage }}"
      
      - alert: UnauthorizedAccessAttempt
        expr: increase(maritime_permission_checks_total{result="false",permission_type="emergency_override"}[1m]) > 0
        for: 0m
        labels:
          severity: critical
          component: security
        annotations:
          summary: "Unauthorized emergency access attempt"
          description: "Someone attempted emergency override without permission"
      
      - alert: RBACDatabaseConnectionFailure
        expr: up{job="maritime-rbac-service"} == 0
        for: 1m
        labels:
          severity: critical
          component: rbac
        annotations:
          summary: "RBAC service is down"
          description: "Maritime RBAC service has been down for more than 1 minute"
```

## 10. Deployment and Operations

### Environment Configuration

```python
# config/rbac_config.py
from pydantic import BaseSettings
from typing import Dict, List

class RBACSettings(BaseSettings):
    """RBAC configuration settings"""
    
    # JWT Configuration
    jwt_roles_validation: bool = True
    jwt_freshness_required_minutes: int = 30
    jwt_audience_validation: bool = True
    
    # Cache Configuration
    redis_url: str = "redis://localhost:6379"
    cache_ttl_seconds: int = 300
    memory_cache_size: int = 1000
    
    # Database Configuration
    database_url: str
    connection_pool_size: int = 20
    permission_query_timeout: int = 5
    
    # Security Configuration
    audit_logging_enabled: bool = True
    sensitive_operation_logging: bool = True
    permission_check_rate_limit: int = 1000  # per minute per user
    
    # Maritime-specific Configuration
    geographic_restrictions_enabled: bool = True
    financial_limits_enabled: bool = True
    time_based_permissions_enabled: bool = True
    
    # Monitoring Configuration
    metrics_enabled: bool = True
    detailed_metrics: bool = False
    alert_webhook_url: str = ""
    
    class Config:
        env_file = ".env"
        env_prefix = "RBAC_"

# Load settings
rbac_settings = RBACSettings()
```

### Docker Configuration

```dockerfile
# Dockerfile for RBAC service
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash rbac
USER rbac

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml for RBAC stack
version: '3.8'

services:
  rbac-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - RBAC_DATABASE_URL=postgresql://user:pass@postgres:5432/maritime_rbac
      - RBAC_REDIS_URL=redis://redis:6379
      - WORKOS_API_KEY=${WORKOS_API_KEY}
    depends_on:
      - postgres
      - redis
    networks:
      - maritime-network
  
  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=maritime_rbac
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - maritime-network
  
  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    networks:
      - maritime-network
  
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
      - ./rbac_alerts.yml:/etc/prometheus/rbac_alerts.yml
    networks:
      - maritime-network

volumes:
  postgres_data:
  redis_data:

networks:
  maritime-network:
    driver: bridge
```

## Summary and Recommendations

### ✅ Final Recommendation: Hybrid RBAC Approach

**Store in JWT Tokens**:
- Basic organizational roles (`vessel_operator`, `tenant_admin`)
- Tenant type and organization ID
- High-level functional roles

**Store in Database**:
- Vessel-specific permissions
- Geographic access restrictions
- Time-based permissions
- Financial transaction limits
- Detailed maritime permissions

### **Key Benefits**:

1. **Performance**: Fast basic checks via JWT, detailed permissions cached
2. **Security**: Sensitive permissions not exposed in JWT tokens
3. **Flexibility**: Complex maritime business rules supported
4. **Compliance**: Complete audit trail for regulatory requirements
5. **Scalability**: Multi-level caching reduces database load
6. **Real-time**: Permission changes effective immediately

### **Implementation Priority**:

1. **Phase 1**: Basic JWT role checking and database schema
2. **Phase 2**: Detailed permission system and caching
3. **Phase 3**: Maritime-specific contextual permissions
4. **Phase 4**: Advanced monitoring and compliance reporting

This hybrid approach provides the optimal balance of performance, security, and functionality for your maritime insurance platform's RBAC requirements.

<function_calls>
<invoke name="TodoWrite">
<parameter name="todos">[{"content": "Structure comprehensive WorkOS documentation plan", "status": "completed", "priority": "high", "id": "workos-assessment-5"}, {"content": "Research WorkOS account setup and environment strategy (dev vs prod)", "status": "completed", "priority": "high", "id": "phase1-research-1"}, {"content": "Research React/TypeScript WorkOS integration patterns", "status": "completed", "priority": "high", "id": "phase1-research-2"}, {"content": "Research WorkOS deployment and operations guide", "status": "completed", "priority": "medium", "id": "phase1-research-3"}, {"content": "Create formal WorkOS selection decision document", "status": "completed", "priority": "high", "id": "phase2-doc-1"}, {"content": "Create comprehensive WorkOS implementation guide", "status": "completed", "priority": "high", "id": "phase2-doc-2"}, {"content": "Update and fix outdated references in existing documentation", "status": "completed", "priority": "medium", "id": "phase2-doc-3"}, {"content": "Create WorkOS setup training module", "status": "completed", "priority": "medium", "id": "phase3-training-1"}, {"content": "Create authentication implementation training module", "status": "completed", "priority": "medium", "id": "phase3-training-2"}, {"content": "Create maritime compliance training module", "status": "completed", "priority": "low", "id": "phase3-training-3"}, {"content": "Organize documentation structure and update project navigation", "status": "completed", "priority": "low", "id": "phase4-organization"}, {"content": "Create WorkOS JWT authentication flow diagram", "status": "completed", "priority": "high", "id": "auth-flow-diagram-1"}, {"content": "Create WorkOS technical architecture diagram", "status": "completed", "priority": "high", "id": "auth-architecture-2"}, {"content": "Create WorkOS SDK requirements decision guide", "status": "completed", "priority": "medium", "id": "auth-sdk-guide-3"}, {"content": "Create RBAC implementation guide for maritime platform", "status": "completed", "priority": "high", "id": "rbac-implementation-guide"}]