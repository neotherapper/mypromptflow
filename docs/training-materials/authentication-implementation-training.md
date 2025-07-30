# Authentication Implementation Training: WorkOS Integration

## Module Objectives
Implement secure, enterprise-grade authentication using WorkOS in the maritime insurance platform, covering frontend React/TypeScript components, backend FastAPI services, security protocols, and hands-on practice exercises.

---

## 1. Frontend Implementation (React/TypeScript)

### Core Dependencies Setup

```bash
# Install WorkOS SDK and authentication dependencies
pnpm add @workos-inc/authkit-js @tanstack/react-query zod
pnpm add -D @types/node
```

### Authentication Context Provider

```typescript
// src/contexts/AuthContext.tsx
import { createContext, useContext, ReactNode, useEffect, useState } from 'react';
import { WorkOS } from '@workos-inc/authkit-js';

interface User {
  id: string;
  email: string;
  firstName?: string;
  lastName?: string;
  organizationId?: string;
  role: 'admin' | 'underwriter' | 'agent' | 'client';
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  login: (email: string, password: string) => Promise<void>;
  loginWithSSO: (organizationId: string) => Promise<void>;
  logout: () => Promise<void>;
  refreshToken: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const workos = new WorkOS({
  apiKey: import.meta.env.VITE_WORKOS_API_KEY,
  clientId: import.meta.env.VITE_WORKOS_CLIENT_ID,
});

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    initializeAuth();
  }, []);

  const initializeAuth = async () => {
    try {
      const session = await workos.userManagement.getUser();
      if (session) {
        setUser(transformWorkOSUser(session));
      }
    } catch (error) {
      console.warn('No active session found');
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    setIsLoading(true);
    try {
      const { user: workosUser } = await workos.userManagement.authenticateWithPassword({
        email,
        password,
        clientId: import.meta.env.VITE_WORKOS_CLIENT_ID,
      });
      setUser(transformWorkOSUser(workosUser));
    } catch (error) {
      throw new Error('Authentication failed');
    } finally {
      setIsLoading(false);
    }
  };

  const loginWithSSO = async (organizationId: string) => {
    const authorizationUrl = workos.userManagement.getAuthorizationUrl({
      provider: 'authkit',
      organizationId,
      redirectUri: `${window.location.origin}/auth/callback`,
      clientId: import.meta.env.VITE_WORKOS_CLIENT_ID,
    });
    
    window.location.href = authorizationUrl;
  };

  const logout = async () => {
    await workos.userManagement.signOut();
    setUser(null);
  };

  const refreshToken = async () => {
    try {
      await workos.userManagement.refreshSession();
      const session = await workos.userManagement.getUser();
      if (session) {
        setUser(transformWorkOSUser(session));
      }
    } catch (error) {
      await logout();
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        isAuthenticated: !!user,
        login,
        loginWithSSO,
        logout,
        refreshToken,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

function transformWorkOSUser(workosUser: any): User {
  return {
    id: workosUser.id,
    email: workosUser.email,
    firstName: workosUser.firstName,
    lastName: workosUser.lastName,
    organizationId: workosUser.organizationId,
    role: determineUserRole(workosUser),
  };
}

function determineUserRole(workosUser: any): User['role'] {
  // Maritime insurance role mapping logic
  const orgRole = workosUser.organizationMemberships?.[0]?.role;
  
  switch (orgRole) {
    case 'admin':
      return 'admin';
    case 'underwriter':
      return 'underwriter';
    case 'agent':
      return 'agent';
    default:
      return 'client';
  }
}
```

### Protected Route Component

```typescript
// src/components/auth/ProtectedRoute.tsx
import { Navigate, useLocation } from '@tanstack/react-router';
import { useAuth } from '@/contexts/AuthContext';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';

interface ProtectedRouteProps {
  children: React.ReactNode;
  requiredRole?: 'admin' | 'underwriter' | 'agent' | 'client';
  fallbackPath?: string;
}

export function ProtectedRoute({ 
  children, 
  requiredRole,
  fallbackPath = '/auth/login' 
}: ProtectedRouteProps) {
  const { isAuthenticated, isLoading, user } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (!isAuthenticated) {
    return <Navigate to={fallbackPath} search={{ from: location.pathname }} />;
  }

  if (requiredRole && user?.role !== requiredRole) {
    return <Navigate to="/dashboard" />;
  }

  return <>{children}</>;
}
```

### Login Form Component

```typescript
// src/components/auth/LoginForm.tsx
import { useState } from 'react';
import { useForm } from '@tanstack/react-form';
import { zodValidator } from '@tanstack/zod-form-adapter';
import { z } from 'zod';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Alert } from '@/components/ui/Alert';

const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

export function LoginForm() {
  const { login } = useAuth();
  const [error, setError] = useState<string | null>(null);

  const form = useForm({
    defaultValues: {
      email: '',
      password: '',
    },
    validatorAdapter: zodValidator,
    validators: {
      onChange: loginSchema,
    },
    onSubmit: async ({ value }) => {
      try {
        setError(null);
        await login(value.email, value.password);
      } catch (err) {
        setError('Invalid email or password');
      }
    },
  });

  return (
    <div className="w-full max-w-md mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold text-center mb-6 text-maritime-blue">
        Maritime Insurance Portal
      </h2>
      
      <form
        onSubmit={(e) => {
          e.preventDefault();
          e.stopPropagation();
          form.handleSubmit();
        }}
        className="space-y-4"
      >
        <div>
          <form.Field
            name="email"
            children={(field) => (
              <>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                  Email Address
                </label>
                <Input
                  id="email"
                  type="email"
                  value={field.state.value}
                  onChange={(e) => field.handleChange(e.target.value)}
                  onBlur={field.handleBlur}
                  placeholder="Enter your email"
                  className="mt-1"
                />
                {field.state.meta.errors && (
                  <p className="mt-1 text-sm text-red-600">
                    {field.state.meta.errors[0]}
                  </p>
                )}
              </>
            )}
          />
        </div>

        <div>
          <form.Field
            name="password"
            children={(field) => (
              <>
                <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                  Password
                </label>
                <Input
                  id="password"
                  type="password"
                  value={field.state.value}
                  onChange={(e) => field.handleChange(e.target.value)}
                  onBlur={field.handleBlur}
                  placeholder="Enter your password"
                  className="mt-1"
                />
                {field.state.meta.errors && (
                  <p className="mt-1 text-sm text-red-600">
                    {field.state.meta.errors[0]}
                  </p>
                )}
              </>
            )}
          />
        </div>

        {error && (
          <Alert variant="destructive">
            {error}
          </Alert>
        )}

        <Button
          type="submit"
          disabled={form.state.isSubmitting}
          className="w-full"
        >
          {form.state.isSubmitting ? 'Signing in...' : 'Sign In'}
        </Button>
      </form>

      <div className="mt-6">
        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-gray-300" />
          </div>
          <div className="relative flex justify-center text-sm">
            <span className="px-2 bg-white text-gray-500">Or continue with SSO</span>
          </div>
        </div>

        <Button
          variant="outline"
          onClick={() => {/* Handle SSO login */}}
          className="w-full mt-3"
        >
          Sign in with SSO
        </Button>
      </div>
    </div>
  );
}
```

### Authentication API Client

```typescript
// src/api/auth.ts
import { z } from 'zod';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export const userSchema = z.object({
  id: z.string(),
  email: z.string().email(),
  firstName: z.string().optional(),
  lastName: z.string().optional(),
  organizationId: z.string().optional(),
  role: z.enum(['admin', 'underwriter', 'agent', 'client']),
  permissions: z.array(z.string()),
});

export type User = z.infer<typeof userSchema>;

export const authApi = {
  async getCurrentUser(): Promise<User> {
    const response = await fetch(`${API_BASE_URL}/api/auth/me`, {
      credentials: 'include',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Failed to fetch user profile');
    }

    const data = await response.json();
    return userSchema.parse(data);
  },

  async refreshToken(): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/api/auth/refresh`, {
      method: 'POST',
      credentials: 'include',
    });

    if (!response.ok) {
      throw new Error('Failed to refresh token');
    }
  },

  async logout(): Promise<void> {
    await fetch(`${API_BASE_URL}/api/auth/logout`, {
      method: 'POST',
      credentials: 'include',
    });
  },
};
```

---

## 2. Backend Implementation (FastAPI)

### Dependencies and Configuration

```python
# requirements.txt additions
workos==2.0.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
```

```python
# app/core/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # WorkOS Configuration
    WORKOS_API_KEY: str
    WORKOS_CLIENT_ID: str
    WORKOS_CLIENT_SECRET: str
    WORKOS_WEBHOOK_SECRET: str
    
    # JWT Configuration
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS Origins for maritime platform
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",  # Vite dev server
        "https://maritime-insurance.com",
        "https://staging.maritime-insurance.com"
    ]
    
    # Session Configuration
    SESSION_COOKIE_NAME: str = "maritime_session"
    SESSION_COOKIE_DOMAIN: Optional[str] = None
    SESSION_COOKIE_SECURE: bool = True
    SESSION_COOKIE_SAMESITE: str = "lax"

    class Config:
        env_file = ".env"

settings = Settings()
```

### Authentication Service

```python
# app/features/auth/service.py
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import workos
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.features.auth.schemas import UserCreate, UserResponse, TokenResponse
from app.features.users.repository import UserRepository
from app.features.users.entities import User

# Initialize WorkOS client
workos_client = workos.WorkOSClient(api_key=settings.WORKOS_API_KEY)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthenticationService:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.user_repository = UserRepository(db_session)

    async def authenticate_with_workos(
        self, 
        authorization_code: str,
        client_id: str
    ) -> UserResponse:
        """Authenticate user via WorkOS Authorization Code flow"""
        try:
            # Exchange authorization code for user profile
            profile = workos_client.user_management.authenticate_with_code(
                code=authorization_code,
                client_id=client_id
            )
            
            # Get or create user in local database
            user = await self._get_or_create_user_from_workos(profile)
            
            return UserResponse.model_validate(user)
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"WorkOS authentication failed: {str(e)}"
            )

    async def authenticate_with_password(
        self, 
        email: str, 
        password: str
    ) -> UserResponse:
        """Authenticate user with email/password (for local accounts)"""
        user = await self.user_repository.get_by_email(email)
        
        if not user or not self._verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Account is deactivated"
            )
        
        # Update last login
        user.last_login_at = datetime.utcnow()
        await self.user_repository.update(user)
        
        return UserResponse.model_validate(user)

    async def create_access_token(self, user: User) -> TokenResponse:
        """Create JWT access and refresh tokens"""
        # Access token payload
        access_payload = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role,
            "organization_id": str(user.organization_id) if user.organization_id else None,
            "permissions": await self._get_user_permissions(user),
            "exp": datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES),
            "iat": datetime.utcnow(),
            "type": "access"
        }
        
        # Refresh token payload
        refresh_payload = {
            "sub": str(user.id),
            "exp": datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS),
            "iat": datetime.utcnow(),
            "type": "refresh"
        }
        
        access_token = jwt.encode(
            access_payload, 
            settings.JWT_SECRET_KEY, 
            algorithm=settings.JWT_ALGORITHM
        )
        
        refresh_token = jwt.encode(
            refresh_payload, 
            settings.JWT_SECRET_KEY, 
            algorithm=settings.JWT_ALGORITHM
        )
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )

    async def refresh_access_token(self, refresh_token: str) -> TokenResponse:
        """Refresh access token using refresh token"""
        try:
            payload = jwt.decode(
                refresh_token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            
            if payload.get("type") != "refresh":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token type"
                )
            
            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token payload"
                )
            
            user = await self.user_repository.get_by_id(int(user_id))
            if not user or not user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found or inactive"
                )
            
            return await self.create_access_token(user)
            
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

    async def _get_or_create_user_from_workos(self, profile: Dict[str, Any]) -> User:
        """Get existing user or create new one from WorkOS profile"""
        user = await self.user_repository.get_by_email(profile["email"])
        
        if user:
            # Update user info from WorkOS
            user.first_name = profile.get("first_name")
            user.last_name = profile.get("last_name")
            user.workos_id = profile["id"]
            user.last_login_at = datetime.utcnow()
            
            # Update organization membership
            if profile.get("organization_id"):
                user.organization_id = profile["organization_id"]
                user.role = self._determine_role_from_workos(profile)
            
            await self.user_repository.update(user)
        else:
            # Create new user
            user_data = UserCreate(
                email=profile["email"],
                first_name=profile.get("first_name"),
                last_name=profile.get("last_name"),
                workos_id=profile["id"],
                organization_id=profile.get("organization_id"),
                role=self._determine_role_from_workos(profile),
                is_active=True
            )
            user = await self.user_repository.create(user_data)
        
        return user

    def _determine_role_from_workos(self, profile: Dict[str, Any]) -> str:
        """Determine user role based on WorkOS organization membership"""
        # Default role mapping for maritime insurance
        org_role = profile.get("organization_membership", {}).get("role", "member")
        
        role_mapping = {
            "admin": "admin",
            "underwriter": "underwriter", 
            "agent": "agent",
            "member": "client"
        }
        
        return role_mapping.get(org_role, "client")

    async def _get_user_permissions(self, user: User) -> list[str]:
        """Get user permissions based on role and organization"""
        # Maritime insurance specific permissions
        role_permissions = {
            "admin": [
                "users:read",
                "users:write", 
                "policies:read",
                "policies:write",
                "claims:read",
                "claims:write",
                "quotes:read",
                "quotes:write",
                "reports:read"
            ],
            "underwriter": [
                "policies:read",
                "policies:write",
                "quotes:read", 
                "quotes:write",
                "claims:read",
                "reports:read"
            ],
            "agent": [
                "policies:read",
                "quotes:read",
                "quotes:write",
                "claims:read"
            ],
            "client": [
                "policies:read",
                "quotes:read",
                "claims:read"
            ]
        }
        
        return role_permissions.get(user.role, [])

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return pwd_context.verify(plain_password, hashed_password)

    def _hash_password(self, password: str) -> str:
        """Hash password"""
        return pwd_context.hash(password)
```

### Authentication Router

```python
# app/features/auth/router.py
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.features.auth.service import AuthenticationService
from app.features.auth.schemas import (
    LoginRequest, 
    WorkOSCallbackRequest,
    TokenResponse,
    UserResponse
)
from app.features.auth.dependencies import get_current_user, get_current_active_user

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()

@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db_session)
):
    """Authenticate user with email/password"""
    auth_service = AuthenticationService(db)
    
    # Authenticate user
    user = await auth_service.authenticate_with_password(
        login_data.email, 
        login_data.password
    )
    
    # Create tokens
    token_response = await auth_service.create_access_token(user)
    
    # Set secure HTTP-only cookie for refresh token
    response.set_cookie(
        key="refresh_token",
        value=token_response.refresh_token,
        max_age=timedelta(days=7).total_seconds(),
        httponly=True,
        secure=True,
        samesite="lax"
    )
    
    return token_response

@router.post("/workos/callback", response_model=TokenResponse)
async def workos_callback(
    callback_data: WorkOSCallbackRequest,
    response: Response,
    db: AsyncSession = Depends(get_db_session)
):
    """Handle WorkOS authentication callback"""
    auth_service = AuthenticationService(db)
    
    # Authenticate with WorkOS
    user = await auth_service.authenticate_with_workos(
        callback_data.code,
        callback_data.client_id
    )
    
    # Create tokens
    token_response = await auth_service.create_access_token(user)
    
    # Set secure HTTP-only cookie for refresh token
    response.set_cookie(
        key="refresh_token",
        value=token_response.refresh_token,
        max_age=timedelta(days=7).total_seconds(),
        httponly=True,
        secure=True,
        samesite="lax"
    )
    
    return token_response

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: Request,
    db: AsyncSession = Depends(get_db_session)
):
    """Refresh access token using refresh token from cookie"""
    refresh_token = request.cookies.get("refresh_token")
    
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found"
        )
    
    auth_service = AuthenticationService(db)
    return await auth_service.refresh_access_token(refresh_token)

@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Get current authenticated user profile"""
    return current_user

@router.post("/logout")
async def logout(
    response: Response,
    current_user: UserResponse = Depends(get_current_user)
):
    """Logout user and clear tokens"""
    response.delete_cookie(key="refresh_token")
    return {"message": "Successfully logged out"}

@router.get("/workos/authorization-url")
async def get_workos_authorization_url(
    organization_id: str = None,
    redirect_uri: str = "http://localhost:5173/auth/callback"
):
    """Get WorkOS authorization URL for SSO login"""
    from workos import WorkOSClient
    from app.core.config import settings
    
    client = WorkOSClient(api_key=settings.WORKOS_API_KEY)
    
    authorization_url = client.user_management.get_authorization_url(
        provider="authkit",
        client_id=settings.WORKOS_CLIENT_ID,
        redirect_uri=redirect_uri,
        organization_id=organization_id
    )
    
    return {"authorization_url": authorization_url}
```

### Authentication Dependencies

```python
# app/features/auth/dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db_session
from app.features.users.repository import UserRepository
from app.features.auth.schemas import UserResponse

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db_session)
) -> UserResponse:
    """Get current authenticated user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        if payload.get("type") != "access":
            raise credentials_exception
        
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
            
    except JWTError:
        raise credentials_exception
    
    user_repository = UserRepository(db)
    user = await user_repository.get_by_id(int(user_id))
    
    if user is None:
        raise credentials_exception
    
    return UserResponse.model_validate(user)

async def get_current_active_user(
    current_user: UserResponse = Depends(get_current_user)
) -> UserResponse:
    """Get current active user (must be active)"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive user"
        )
    return current_user

def require_role(required_role: str):
    """Dependency factory for role-based access control"""
    async def role_checker(
        current_user: UserResponse = Depends(get_current_active_user)
    ) -> UserResponse:
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Operation requires {required_role} role"
            )
        return current_user
    
    return role_checker

def require_permissions(required_permissions: list[str]):
    """Dependency factory for permission-based access control"""
    async def permission_checker(
        current_user: UserResponse = Depends(get_current_active_user)
    ) -> UserResponse:
        user_permissions = set(current_user.permissions or [])
        required_permissions_set = set(required_permissions)
        
        if not required_permissions_set.issubset(user_permissions):
            missing_permissions = required_permissions_set - user_permissions
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Missing required permissions: {', '.join(missing_permissions)}"
            )
        return current_user
    
    return permission_checker
```

---

## 3. Security & Compliance

### Security Configuration

```python
# app/core/security.py
from datetime import datetime, timedelta
from typing import Optional
import secrets
import hashlib
from fastapi import HTTPException, status, Request
from fastapi.security.utils import get_authorization_scheme_param
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
import redis
from app.core.config import settings

# Rate limiting using Redis
redis_client = redis.Redis.from_url(settings.REDIS_URL)

class SecurityMiddleware(BaseHTTPMiddleware):
    """Enhanced security middleware for maritime platform"""
    
    async def dispatch(self, request: Request, call_next):
        # Security headers
        response = await call_next(request)
        
        # HSTS Header
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # Content Security Policy for maritime domain
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://js.workosapis.com; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' https://fonts.gstatic.com; "
            "connect-src 'self' https://api.workos.com; "
            "frame-ancestors 'none'"
        )
        response.headers["Content-Security-Policy"] = csp
        
        # Additional security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        return response

class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware with maritime-specific rules"""
    
    RATE_LIMITS = {
        # Authentication endpoints
        "/auth/login": {"requests": 5, "window": 300},  # 5 requests per 5 minutes
        "/auth/refresh": {"requests": 10, "window": 300},
        
        # API endpoints
        "/api/quotes": {"requests": 50, "window": 3600},  # 50 quotes per hour
        "/api/policies": {"requests": 100, "window": 3600},
        "/api/claims": {"requests": 20, "window": 3600},
    }
    
    async def dispatch(self, request: Request, call_next):
        client_ip = self.get_client_ip(request)
        path = request.url.path
        
        # Check rate limit
        if path in self.RATE_LIMITS:
            limit_config = self.RATE_LIMITS[path]
            if not await self.is_request_allowed(client_ip, path, limit_config):
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Rate limit exceeded"
                )
        
        response = await call_next(request)
        return response
    
    def get_client_ip(self, request: Request) -> str:
        """Get client IP considering proxy headers"""
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        return request.client.host
    
    async def is_request_allowed(
        self, 
        client_ip: str, 
        path: str, 
        limit_config: dict
    ) -> bool:
        """Check if request is within rate limit"""
        key = f"rate_limit:{client_ip}:{path}"
        
        try:
            current_requests = redis_client.get(key)
            if current_requests is None:
                redis_client.setex(key, limit_config["window"], 1)
                return True
            
            if int(current_requests) >= limit_config["requests"]:
                return False
            
            redis_client.incr(key)
            return True
            
        except Exception:
            # If Redis is down, allow request but log error
            return True

class SessionManager:
    """Secure session management for maritime platform"""
    
    def __init__(self):
        self.session_store = redis_client
    
    async def create_session(
        self, 
        user_id: str, 
        user_agent: str, 
        ip_address: str
    ) -> str:
        """Create secure session with device fingerprinting"""
        session_id = secrets.token_urlsafe(32)
        
        session_data = {
            "user_id": user_id,
            "created_at": datetime.utcnow().isoformat(),
            "last_activity": datetime.utcnow().isoformat(),
            "user_agent": user_agent,
            "ip_address": ip_address,
            "device_fingerprint": self._generate_device_fingerprint(user_agent, ip_address)
        }
        
        # Store session with TTL
        await self.session_store.hset(
            f"session:{session_id}", 
            mapping=session_data
        )
        await self.session_store.expire(
            f"session:{session_id}", 
            timedelta(days=7).total_seconds()
        )
        
        return session_id
    
    async def validate_session(
        self, 
        session_id: str, 
        user_agent: str, 
        ip_address: str
    ) -> Optional[dict]:
        """Validate session with security checks"""
        session_data = await self.session_store.hgetall(f"session:{session_id}")
        
        if not session_data:
            return None
        
        # Check device fingerprint for session hijacking
        expected_fingerprint = self._generate_device_fingerprint(user_agent, ip_address)
        if session_data.get("device_fingerprint") != expected_fingerprint:
            # Potential session hijacking - invalidate session
            await self.invalidate_session(session_id)
            return None
        
        # Update last activity
        session_data["last_activity"] = datetime.utcnow().isoformat()
        await self.session_store.hset(f"session:{session_id}", "last_activity", session_data["last_activity"])
        
        return session_data
    
    async def invalidate_session(self, session_id: str):
        """Invalidate session"""
        await self.session_store.delete(f"session:{session_id}")
    
    def _generate_device_fingerprint(self, user_agent: str, ip_address: str) -> str:
        """Generate device fingerprint for security"""
        fingerprint_data = f"{user_agent}:{ip_address}:{settings.JWT_SECRET_KEY}"
        return hashlib.sha256(fingerprint_data.encode()).hexdigest()[:16]
```

### Compliance Features

```python
# app/features/audit/service.py
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.features.audit.entities import AuditLog
from app.features.audit.repository import AuditLogRepository

class AuditService:
    """Audit logging for compliance (SOX, GDPR, maritime regulations)"""
    
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        self.audit_repository = AuditLogRepository(db_session)
    
    async def log_authentication_event(
        self,
        user_id: str,
        event_type: str,  # login, logout, failed_login, password_change
        ip_address: str,
        user_agent: str,
        additional_data: dict = None
    ):
        """Log authentication events for security compliance"""
        await self.audit_repository.create({
            "user_id": user_id,
            "event_type": f"auth.{event_type}",
            "event_category": "authentication",
            "ip_address": ip_address,
            "user_agent": user_agent,
            "timestamp": datetime.utcnow(),
            "additional_data": additional_data or {},
            "compliance_category": "security"
        })
    
    async def log_data_access(
        self,
        user_id: str,
        resource_type: str,  # policy, claim, quote, vessel
        resource_id: str,
        action: str,  # read, create, update, delete
        ip_address: str,
        sensitive_data_accessed: bool = False
    ):
        """Log data access for GDPR and maritime compliance"""
        await self.audit_repository.create({
            "user_id": user_id,
            "event_type": f"data.{action}",
            "event_category": "data_access",
            "resource_type": resource_type,
            "resource_id": resource_id,
            "ip_address": ip_address,
            "timestamp": datetime.utcnow(),
            "additional_data": {
                "sensitive_data": sensitive_data_accessed,
                "maritime_regulation_applicable": True
            },
            "compliance_category": "data_protection"
        })
    
    async def log_business_event(
        self,
        user_id: str,
        event_type: str,  # quote_generated, policy_issued, claim_submitted
        resource_id: str,
        financial_impact: float = None,
        regulatory_significance: str = None
    ):
        """Log business events for SOX and maritime regulatory compliance"""
        await self.audit_repository.create({
            "user_id": user_id,
            "event_type": f"business.{event_type}",
            "event_category": "business_operations",
            "resource_id": resource_id,
            "timestamp": datetime.utcnow(),
            "additional_data": {
                "financial_impact": financial_impact,
                "regulatory_significance": regulatory_significance,
                "maritime_compliance": True
            },
            "compliance_category": "business_operations"
        })
```

---

## 4. Hands-on Exercises

### Exercise 1: Frontend Authentication Flow

**Objective**: Implement complete login/logout flow with WorkOS integration

**Tasks**:
1. Set up AuthProvider in your React app
2. Create login form with validation
3. Implement protected routes
4. Add logout functionality
5. Handle authentication errors

**Code Template**:
```typescript
// Exercise: Complete the missing authentication logic
export function App() {
  return (
    <AuthProvider>
      <Router>
        {/* TODO: Add protected routes */}
        <Route path="/login" component={LoginForm} />
        <Route path="/dashboard" component={/* TODO: Wrap with ProtectedRoute */} />
      </Router>
    </AuthProvider>
  );
}
```

**Validation Criteria**:
- [ ] User can log in with email/password
- [ ] Invalid credentials show appropriate error
- [ ] Successful login redirects to dashboard
- [ ] Protected routes redirect unauthenticated users
- [ ] Logout clears authentication state

### Exercise 2: Backend JWT Implementation

**Objective**: Implement secure JWT token management

**Tasks**:
1. Create JWT token generation
2. Implement token validation middleware
3. Add refresh token rotation
4. Implement role-based access control
5. Add session management

**Code Template**:
```python
# Exercise: Complete the JWT service
class JWTService:
    def create_tokens(self, user: User) -> TokenResponse:
        # TODO: Implement token creation with proper expiration
        pass
    
    def validate_token(self, token: str) -> dict:
        # TODO: Implement token validation with error handling
        pass
    
    def refresh_token(self, refresh_token: str) -> TokenResponse:
        # TODO: Implement secure token refresh
        pass
```

**Validation Criteria**:
- [ ] Access tokens expire after 30 minutes
- [ ] Refresh tokens expire after 7 days  
- [ ] Invalid tokens return 401 errors
- [ ] Token refresh works correctly
- [ ] Role-based permissions enforced

### Exercise 3: Security Implementation

**Objective**: Implement comprehensive security measures

**Tasks**:
1. Add rate limiting to authentication endpoints
2. Implement CSRF protection
3. Add security headers
4. Implement session hijacking detection
5. Add audit logging

**Code Template**:
```python
# Exercise: Complete the security middleware
class SecurityMiddleware:
    async def dispatch(self, request: Request, call_next):
        # TODO: Add rate limiting check
        # TODO: Validate CSRF token
        # TODO: Add security headers
        # TODO: Check for suspicious activity
        pass
```

**Validation Criteria**:
- [ ] Rate limiting blocks excessive requests
- [ ] Security headers are properly set
- [ ] CSRF tokens validated on state-changing operations
- [ ] Suspicious sessions are invalidated
- [ ] All authentication events are audited

### Exercise 4: WorkOS Integration

**Objective**: Complete WorkOS SSO integration

**Tasks**:
1. Set up WorkOS organization
2. Configure SSO providers
3. Implement authorization code flow
4. Handle organization membership
5. Test with multiple identity providers

**Code Template**:
```typescript
// Exercise: Complete WorkOS integration
export function SSOLoginButton({ organizationId }: { organizationId: string }) {
  const handleSSOLogin = async () => {
    // TODO: Get WorkOS authorization URL
    // TODO: Redirect user to WorkOS
    // TODO: Handle callback with authorization code
  };
  
  return <Button onClick={handleSSOLogin}>Sign in with SSO</Button>;
}
```

**Validation Criteria**:
- [ ] SSO login redirects to correct provider
- [ ] Authorization code exchange works
- [ ] User profile synced from WorkOS
- [ ] Organization membership handled correctly
- [ ] Multiple providers supported

### Exercise 5: Error Handling & Recovery

**Objective**: Implement robust error handling

**Tasks**:
1. Handle network failures gracefully
2. Implement token refresh on 401 errors
3. Add retry logic for transient failures
4. Show user-friendly error messages
5. Log errors for monitoring

**Code Template**:
```typescript
// Exercise: Complete error handling
export function useAuthenticatedApi() {
  const { refreshToken } = useAuth();
  
  const apiCall = async (url: string, options: RequestInit) => {
    try {
      // TODO: Make API call
      // TODO: Handle 401 with token refresh
      // TODO: Retry on network errors
      // TODO: Show user-friendly errors
    } catch (error) {
      // TODO: Implement error recovery
    }
  };
  
  return { apiCall };
}
```

**Validation Criteria**:
- [ ] 401 errors trigger automatic token refresh
- [ ] Network failures show retry option
- [ ] User sees clear error messages
- [ ] Errors are logged with context
- [ ] App remains stable during errors

### Exercise 6: Compliance & Audit

**Objective**: Implement audit logging for compliance

**Tasks**:
1. Log all authentication events
2. Track data access for GDPR
3. Monitor privileged operations
4. Generate compliance reports
5. Implement data retention policies

**Code Template**:
```python
# Exercise: Complete audit implementation
@router.post("/policies/{policy_id}/update")
async def update_policy(
    policy_id: str,
    policy_data: PolicyUpdate,
    current_user: User = Depends(get_current_user),
    audit_service: AuditService = Depends(get_audit_service)
):
    # TODO: Update policy
    # TODO: Log audit event with proper categorization
    # TODO: Include compliance metadata
    pass
```

**Validation Criteria**:
- [ ] All authentication events logged
- [ ] Data access events include GDPR metadata
- [ ] Privileged operations properly audited
- [ ] Compliance reports can be generated
- [ ] Data retention policies enforced

---

## Assessment Checklist

### Frontend Implementation ✅
- [ ] AuthContext properly configured
- [ ] Login/logout flows working
- [ ] Protected routes implemented
- [ ] Error handling comprehensive
- [ ] TypeScript types properly defined

### Backend Implementation ✅
- [ ] WorkOS integration functional
- [ ] JWT tokens properly managed
- [ ] Role-based access control working
- [ ] Session management secure
- [ ] API endpoints properly protected

### Security & Compliance ✅
- [ ] Rate limiting implemented
- [ ] Security headers configured
- [ ] CSRF protection active
- [ ] Session hijacking detection
- [ ] Audit logging comprehensive

### Integration Testing ✅
- [ ] End-to-end authentication flow
- [ ] SSO integration tested
- [ ] Error scenarios handled
- [ ] Performance under load
- [ ] Security vulnerabilities addressed

---

## Additional Resources

### Documentation Links
- [WorkOS User Management Guide](https://workos.com/docs/user-management)
- [FastAPI Security Tutorial](https://fastapi.tiangolo.com/tutorial/security/)
- [React Authentication Patterns](https://react.dev/learn/escape-hatches)

### Maritime Industry Standards
- IMO MSC Guidelines for Cyber Security
- NIST Cybersecurity Framework for Maritime
- ISO 27001 Information Security Management

### Compliance Requirements
- GDPR Data Protection Regulation
- SOX Financial Reporting Requirements
- Maritime Labour Convention (MLC) 2006

This training module provides comprehensive coverage of authentication implementation for maritime insurance platforms, combining modern web security practices with industry-specific compliance requirements.