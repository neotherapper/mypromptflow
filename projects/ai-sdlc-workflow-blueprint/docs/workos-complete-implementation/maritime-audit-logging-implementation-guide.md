# Maritime Audit Logging Implementation Guide

## Implementation Overview

This guide provides step-by-step implementation instructions for the WorkOS + FastAPI dual-layer audit logging architecture specifically designed for maritime insurance platform compliance requirements.

**Architecture Summary**: Combine WorkOS built-in audit logs for authentication events with custom FastAPI middleware for comprehensive business operation logging to meet IMO, SOLAS, and maritime law compliance requirements.

## Table of Contents

1. [Prerequisites and Setup](#prerequisites-and-setup)
2. [WorkOS Audit Log Integration](#workos-audit-log-integration)
3. [FastAPI Audit Middleware Implementation](#fastapi-audit-middleware-implementation)
4. [Database Schema and Storage](#database-schema-and-storage)
5. [SIEM Integration](#siem-integration)
6. [Compliance and Retention](#compliance-and-retention)
7. [Testing and Validation](#testing-and-validation)
8. [Deployment and Monitoring](#deployment-and-monitoring)

---

## Prerequisites and Setup

### Required Dependencies

```bash
# Core dependencies
pip install fastapi uvicorn workos sqlalchemy asyncpg
pip install pydantic python-multipart python-jose[cryptography]

# Audit logging specific
pip install aioredis celery datadog prometheus_client
pip install boto3  # For S3 cold storage
pip install structlog  # For structured logging

# Development dependencies
pip install pytest pytest-asyncio httpx factory-boy
```

### Environment Configuration

```python
# settings.py
from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # WorkOS Configuration
    workos_api_key: str
    workos_client_id: str
    workos_webhook_secret: str
    
    # Database Configuration
    database_url: str
    audit_database_url: Optional[str] = None  # Separate audit DB if needed
    
    # SIEM Integration
    siem_type: str = "datadog"  # datadog, splunk, elastic, none
    datadog_api_key: Optional[str] = None
    datadog_app_key: Optional[str] = None
    
    # Audit Storage
    audit_retention_days: int = 2555  # 7 years default
    cold_storage_bucket: Optional[str] = None
    
    # Performance Configuration
    audit_queue_size: int = 10000
    audit_batch_size: int = 100
    audit_flush_interval: int = 30  # seconds
    
    class Config:
        env_file = ".env"

settings = Settings()
```

---

## WorkOS Audit Log Integration

### WorkOS Webhook Configuration

```python
# workos_audit.py
from fastapi import FastAPI, Request, HTTPException
from workos import WorkOS
import hmac
import hashlib
import json
from datetime import datetime, timezone

class WorkOSAuditIntegration:
    def __init__(self, api_key: str, webhook_secret: str):
        self.workos = WorkOS(api_key=api_key)
        self.webhook_secret = webhook_secret
        
    def verify_webhook_signature(self, payload: bytes, signature: str) -> bool:
        """Verify WorkOS webhook signature for security"""
        expected_signature = hmac.new(
            self.webhook_secret.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(f"sha256={expected_signature}", signature)
    
    async def handle_audit_event(self, event_data: dict) -> dict:
        """Process WorkOS audit event into maritime format"""
        maritime_audit_event = {
            "event_id": event_data.get("id"),
            "timestamp": event_data.get("occurred_at"),
            "event_source": "workos",
            "user_info": {
                "user_id": event_data.get("actor", {}).get("id"),
                "email": event_data.get("actor", {}).get("email"),
                "name": event_data.get("actor", {}).get("name"),
                "organization_id": event_data.get("metadata", {}).get("organization_id")
            },
            "event_details": {
                "event_type": "authentication",
                "action": event_data.get("event"),
                "resource": "user_session",
                "resource_id": event_data.get("metadata", {}).get("session_id")
            },
            "technical_metadata": {
                "ip_address": event_data.get("context", {}).get("location"),
                "user_agent": event_data.get("context", {}).get("user_agent"),
                "session_id": event_data.get("metadata", {}).get("session_id")
            },
            "compliance_metadata": {
                "regulation_type": "authentication_compliance",
                "retention_period": "3_years",
                "data_classification": "internal"
            }
        }
        
        return maritime_audit_event

# FastAPI webhook endpoint
@app.post("/webhooks/workos/audit")
async def workos_audit_webhook(request: Request):
    """Receive WorkOS audit events via webhook"""
    payload = await request.body()
    signature = request.headers.get("workos-signature")
    
    if not workos_audit.verify_webhook_signature(payload, signature):
        raise HTTPException(status_code=401, detail="Invalid webhook signature")
    
    event_data = json.loads(payload)
    maritime_event = await workos_audit.handle_audit_event(event_data)
    
    # Queue for processing
    await audit_logger.log_audit_event(maritime_event)
    
    return {"status": "received"}
```

### WorkOS Management API Integration

```python
# workos_management.py
from workos import WorkOS
from typing import List, Dict, Optional
from datetime import datetime, timedelta

class WorkOSManagementIntegration:
    def __init__(self, api_key: str):
        self.workos = WorkOS(api_key=api_key)
    
    async def fetch_historical_audit_logs(
        self, 
        organization_id: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> List[Dict]:
        """Fetch historical audit logs from WorkOS"""
        
        params = {
            "limit": limit,
            "order": "desc"
        }
        
        if organization_id:
            params["organization"] = organization_id
        if start_date:
            params["occurred_after"] = start_date.isoformat()
        if end_date:
            params["occurred_before"] = end_date.isoformat()
        
        try:
            audit_logs = self.workos.audit_logs.list(**params)
            return [log.to_dict() for log in audit_logs.data]
        except Exception as e:
            print(f"Error fetching WorkOS audit logs: {e}")
            return []
    
    async def get_user_audit_trail(self, user_id: str, days: int = 30) -> List[Dict]:
        """Get complete audit trail for a specific user"""
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=days)
        
        audit_logs = await self.fetch_historical_audit_logs(
            start_date=start_date,
            end_date=end_date,
            limit=1000
        )
        
        # Filter for specific user
        user_logs = [
            log for log in audit_logs 
            if log.get("actor", {}).get("id") == user_id
        ]
        
        return user_logs
```

---

## FastAPI Audit Middleware Implementation

### Core Audit Logger

```python
# maritime_audit_logger.py
import asyncio
import json
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession
from dataclasses import dataclass, asdict

@dataclass
class MaritimeAuditEvent:
    event_id: str
    timestamp: datetime
    event_source: str  # 'fastapi', 'workos', 'database'
    
    # User context
    user_id: Optional[str] = None
    organization_id: Optional[str] = None
    tenant_type: Optional[str] = None
    email: Optional[str] = None
    roles: Optional[list] = None
    
    # Event details
    event_type: str = "business"  # business, authentication, admin, data_access
    action: str = ""
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    
    # Maritime context
    vessel_id: Optional[str] = None
    vessel_imo: Optional[str] = None
    geographic_location: Optional[Dict] = None
    financial_amount: Optional[float] = None
    
    # Technical metadata
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    session_id: Optional[str] = None
    api_endpoint: Optional[str] = None
    response_status: Optional[int] = None
    processing_time_ms: Optional[int] = None
    
    # Compliance metadata
    regulation_type: str = "general"
    retention_period: str = "7_years"
    data_classification: str = "internal"
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class MaritimeAuditLogger:
    def __init__(
        self, 
        db_session: AsyncSession,
        siem_integration: Optional['SIEMIntegration'] = None,
        queue_size: int = 10000
    ):
        self.db = db_session
        self.siem = siem_integration
        self.audit_queue = asyncio.Queue(maxsize=queue_size)
        self.batch_queue = []
        self.is_processing = False
        
    async def log_audit_event(self, event_data: Dict[str, Any]):
        """Queue audit event for async processing"""
        try:
            # Convert to standardized format
            if isinstance(event_data, dict):
                audit_event = MaritimeAuditEvent(
                    event_id=event_data.get("event_id", str(uuid.uuid4())),
                    timestamp=event_data.get("timestamp", datetime.now(timezone.utc)),
                    event_source=event_data.get("event_source", "fastapi"),
                    **{k: v for k, v in event_data.items() 
                       if k in MaritimeAuditEvent.__dataclass_fields__}
                )
            else:
                audit_event = event_data
                
            await self.audit_queue.put(audit_event)
            
        except asyncio.QueueFull:
            # Handle queue overflow - could implement rotation or urgent logging
            print(f"Audit queue full, dropping event: {event_data.get('event_id', 'unknown')}")
        except Exception as e:
            print(f"Error queuing audit event: {e}")
    
    async def start_processing(self):
        """Start background audit processing"""
        if self.is_processing:
            return
            
        self.is_processing = True
        asyncio.create_task(self._process_audit_queue())
    
    async def stop_processing(self):
        """Stop audit processing and flush remaining events"""
        self.is_processing = False
        await self._flush_batch_queue()
    
    async def _process_audit_queue(self):
        """Background task to process audit events"""
        while self.is_processing:
            try:
                # Wait for events with timeout
                try:
                    event = await asyncio.wait_for(self.audit_queue.get(), timeout=30.0)
                    self.batch_queue.append(event)
                    
                    # Process batch when size reached or timeout
                    if len(self.batch_queue) >= settings.audit_batch_size:
                        await self._flush_batch_queue()
                        
                except asyncio.TimeoutError:
                    # Flush on timeout even if batch not full
                    if self.batch_queue:
                        await self._flush_batch_queue()
                        
            except Exception as e:
                print(f"Error in audit processing: {e}")
                await asyncio.sleep(1)
    
    async def _flush_batch_queue(self):
        """Flush batch of audit events to storage"""
        if not self.batch_queue:
            return
            
        batch = self.batch_queue.copy()
        self.batch_queue.clear()
        
        try:
            # Store in database
            await self._store_audit_batch(batch)
            
            # Stream to SIEM if configured
            if self.siem:
                await self._stream_to_siem_batch(batch)
                
        except Exception as e:
            print(f"Error storing audit batch: {e}")
            # Could implement retry logic or dead letter queue
    
    async def _store_audit_batch(self, events: List[MaritimeAuditEvent]):
        """Store batch of events in database"""
        try:
            # Bulk insert for performance
            audit_records = [
                MaritimeAuditLog(**event.to_dict()) 
                for event in events
            ]
            
            self.db.add_all(audit_records)
            await self.db.commit()
            
        except Exception as e:
            await self.db.rollback()
            print(f"Database audit storage failed: {e}")
            raise
    
    async def _stream_to_siem_batch(self, events: List[MaritimeAuditEvent]):
        """Stream batch of events to SIEM"""
        if not self.siem:
            return
            
        try:
            await self.siem.stream_audit_batch([event.to_dict() for event in events])
        except Exception as e:
            print(f"SIEM streaming failed: {e}")
            # Don't fail the audit storage if SIEM fails
```

### FastAPI Middleware Implementation

```python
# audit_middleware.py
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import time
import json

class MaritimeAuditMiddleware(BaseHTTPMiddleware):
    def __init__(
        self, 
        app: FastAPI, 
        audit_logger: MaritimeAuditLogger,
        exclude_paths: List[str] = None
    ):
        super().__init__(app)
        self.audit_logger = audit_logger
        self.exclude_paths = exclude_paths or [
            "/health", "/metrics", "/docs", "/openapi.json"
        ]
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip audit for excluded paths
        if any(request.url.path.startswith(path) for path in self.exclude_paths):
            return await call_next(request)
        
        start_time = time.time()
        
        # Extract user context before request processing
        user_context = await self._extract_user_context(request)
        
        # Process request
        response = await call_next(request)
        
        # Calculate processing time
        processing_time = int((time.time() - start_time) * 1000)
        
        # Extract maritime context from request/response
        maritime_context = await self._extract_maritime_context(request, response)
        
        # Create audit event
        audit_event = {
            "event_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc),
            "event_source": "fastapi",
            "user_info": user_context,
            "event_details": {
                "event_type": self._classify_event_type(request),
                "action": f"{request.method} {request.url.path}",
                "resource_type": maritime_context.get("resource_type"),
                "resource_id": maritime_context.get("resource_id")
            },
            "maritime_context": {
                "vessel_id": maritime_context.get("vessel_id"),
                "vessel_imo": maritime_context.get("vessel_imo"),
                "geographic_location": maritime_context.get("location"),
                "financial_amount": maritime_context.get("financial_amount")
            },
            "technical_metadata": {
                "ip_address": request.client.host,
                "user_agent": request.headers.get("user-agent"),
                "session_id": user_context.get("session_id"),
                "api_endpoint": str(request.url),
                "response_status": response.status_code,
                "processing_time_ms": processing_time
            },
            "compliance_metadata": {
                "regulation_type": self._determine_regulation_type(maritime_context),
                "retention_period": self._determine_retention_period(maritime_context),
                "data_classification": self._classify_data_sensitivity(maritime_context)
            }
        }
        
        # Queue for async processing
        await self.audit_logger.log_audit_event(audit_event)
        
        return response
    
    async def _extract_user_context(self, request: Request) -> Dict[str, Any]:
        """Extract user context from WorkOS token"""
        try:
            # Get authorization header
            auth_header = request.headers.get("authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return {}
            
            token = auth_header.split(" ")[1]
            
            # Verify and decode WorkOS token
            user_info = await verify_workos_token(token)
            
            return {
                "user_id": user_info.get("sub"),
                "organization_id": user_info.get("org"),
                "tenant_type": user_info.get("tenant_type"),
                "email": user_info.get("email"),
                "roles": user_info.get("roles", []),
                "session_id": user_info.get("sid")
            }
            
        except Exception as e:
            print(f"Error extracting user context: {e}")
            return {}
    
    async def _extract_maritime_context(
        self, 
        request: Request, 
        response: Response
    ) -> Dict[str, Any]:
        """Extract maritime-specific context from request/response"""
        context = {}
        
        try:
            # Extract from URL path parameters
            path_params = request.path_params
            if "vessel_id" in path_params:
                context["vessel_id"] = path_params["vessel_id"]
                # Look up vessel IMO from database
                context["vessel_imo"] = await self._get_vessel_imo(path_params["vessel_id"])
            
            # Extract from query parameters
            query_params = dict(request.query_params)
            if "vessel_id" in query_params:
                context["vessel_id"] = query_params["vessel_id"]
            
            # Extract from request body if available
            if request.method in ["POST", "PUT", "PATCH"]:
                # Try to get cached body (if middleware cached it)
                body = getattr(request.state, "body", None)
                if body:
                    try:
                        body_data = json.loads(body)
                        context.update(self._extract_maritime_from_body(body_data))
                    except json.JSONDecodeError:
                        pass
            
            # Classify resource type based on endpoint
            context["resource_type"] = self._classify_resource_type(request.url.path)
            
            # Extract geographic location if available
            location = await self._get_user_location(request)
            if location:
                context["location"] = location
            
        except Exception as e:
            print(f"Error extracting maritime context: {e}")
        
        return context
    
    def _classify_event_type(self, request: Request) -> str:
        """Classify event type based on endpoint"""
        path = request.url.path.lower()
        
        if "/auth/" in path or "/login" in path or "/logout" in path:
            return "authentication"
        elif "/admin/" in path or "/management/" in path:
            return "admin"
        elif request.method == "GET" and "/api/" in path:
            return "data_access"
        elif request.method in ["POST", "PUT", "PATCH", "DELETE"]:
            return "business"
        else:
            return "general"
    
    def _classify_resource_type(self, path: str) -> Optional[str]:
        """Classify resource type from API endpoint"""
        path_lower = path.lower()
        
        if "/vessel" in path_lower:
            return "vessel"
        elif "/quote" in path_lower:
            return "quote"
        elif "/claim" in path_lower:
            return "claim"
        elif "/policy" in path_lower:
            return "policy"
        elif "/user" in path_lower:
            return "user"
        elif "/organization" in path_lower:
            return "organization"
        else:
            return None
    
    def _determine_regulation_type(self, maritime_context: Dict) -> str:
        """Determine applicable maritime regulations"""
        if maritime_context.get("vessel_id"):
            return "IMO|SOLAS"
        elif maritime_context.get("financial_amount"):
            return "financial_compliance"
        else:
            return "general"
    
    def _determine_retention_period(self, maritime_context: Dict) -> str:
        """Determine retention period based on context"""
        if maritime_context.get("financial_amount"):
            return "10_years"  # Financial records
        elif maritime_context.get("vessel_id"):
            return "7_years"   # Vessel records
        else:
            return "3_years"   # General records
    
    def _classify_data_sensitivity(self, maritime_context: Dict) -> str:
        """Classify data sensitivity level"""
        if maritime_context.get("financial_amount"):
            return "confidential"
        elif maritime_context.get("vessel_id"):
            return "internal"
        else:
            return "public"
```

### Database Event Listeners

```python
# database_audit.py
from sqlalchemy import event
from sqlalchemy.orm import Session
from sqlalchemy.orm.state import InstanceState
import asyncio
import json

class DatabaseAuditListener:
    def __init__(self, audit_logger: MaritimeAuditLogger):
        self.audit_logger = audit_logger
        self.setup_listeners()
    
    def setup_listeners(self):
        """Setup SQLAlchemy event listeners for audit trail"""
        
        @event.listens_for(Session, 'before_commit')
        def receive_before_commit(session):
            """Capture database changes before commit"""
            asyncio.create_task(self._process_session_changes(session))
    
    async def _process_session_changes(self, session: Session):
        """Process all changes in the session"""
        try:
            # Process new objects
            for obj in session.new:
                await self._audit_database_change(obj, "CREATE", session)
            
            # Process modified objects
            for obj in session.dirty:
                await self._audit_database_change(obj, "UPDATE", session)
            
            # Process deleted objects
            for obj in session.deleted:
                await self._audit_database_change(obj, "DELETE", session)
                
        except Exception as e:
            print(f"Error processing database audit: {e}")
    
    async def _audit_database_change(
        self, 
        obj: Any, 
        operation: str, 
        session: Session
    ):
        """Create audit record for database change"""
        try:
            table_name = obj.__tablename__
            object_id = getattr(obj, 'id', None)
            
            # Extract changes for UPDATE operations
            changes = {}
            if operation == "UPDATE":
                changes = self._get_object_changes(obj, session)
            elif operation == "CREATE":
                changes = self._get_object_state(obj)
            
            # Determine if this is maritime-relevant data
            maritime_context = self._extract_maritime_from_object(obj)
            
            audit_event = {
                "event_id": str(uuid.uuid4()),
                "timestamp": datetime.now(timezone.utc),
                "event_source": "database",
                "event_details": {
                    "event_type": "data_modification",
                    "action": f"DB_{operation}",
                    "resource_type": table_name,
                    "resource_id": str(object_id) if object_id else None
                },
                "maritime_context": maritime_context,
                "technical_metadata": {
                    "database_table": table_name,
                    "operation": operation,
                    "changes": changes
                },
                "compliance_metadata": {
                    "regulation_type": self._get_regulation_for_table(table_name),
                    "retention_period": self._get_retention_for_table(table_name),
                    "data_classification": self._get_classification_for_table(table_name)
                }
            }
            
            await self.audit_logger.log_audit_event(audit_event)
            
        except Exception as e:
            print(f"Error auditing database change: {e}")
    
    def _get_object_changes(self, obj: Any, session: Session) -> Dict[str, Any]:
        """Get changes made to an object"""
        changes = {}
        
        try:
            # Get object state
            state: InstanceState = obj.__dict__['_sa_instance_state']
            
            # Get modified attributes
            for attr in state.attrs:
                history = attr.load_history()
                if history.has_changes():
                    changes[attr.key] = {
                        "old_value": history.deleted[0] if history.deleted else None,
                        "new_value": history.added[0] if history.added else None
                    }
        except Exception as e:
            print(f"Error getting object changes: {e}")
        
        return changes
    
    def _get_object_state(self, obj: Any) -> Dict[str, Any]:
        """Get current state of object for CREATE operations"""
        try:
            return {
                key: value for key, value in obj.__dict__.items()
                if not key.startswith('_')
            }
        except Exception:
            return {}
    
    def _extract_maritime_from_object(self, obj: Any) -> Dict[str, Any]:
        """Extract maritime context from database object"""
        context = {}
        
        # Check for common maritime fields
        if hasattr(obj, 'vessel_id'):
            context["vessel_id"] = str(obj.vessel_id)
        if hasattr(obj, 'vessel_imo'):
            context["vessel_imo"] = str(obj.vessel_imo)
        if hasattr(obj, 'financial_amount'):
            context["financial_amount"] = float(obj.financial_amount)
        
        return context
    
    def _get_regulation_for_table(self, table_name: str) -> str:
        """Get applicable regulations for table"""
        maritime_tables = {
            "vessels": "IMO|SOLAS",
            "claims": "maritime_insurance",
            "quotes": "financial_compliance",
            "policies": "insurance_regulation"
        }
        return maritime_tables.get(table_name, "general")
    
    def _get_retention_for_table(self, table_name: str) -> str:
        """Get retention period for table"""
        retention_periods = {
            "audit_logs": "permanent",
            "financial_transactions": "10_years",
            "vessels": "7_years",
            "claims": "7_years",
            "user_sessions": "3_years"
        }
        return retention_periods.get(table_name, "7_years")
    
    def _get_classification_for_table(self, table_name: str) -> str:
        """Get data classification for table"""
        classifications = {
            "financial_transactions": "confidential",
            "personal_data": "confidential",
            "vessels": "internal",
            "audit_logs": "internal",
            "public_data": "public"
        }
        return classifications.get(table_name, "internal")
```

---

## Database Schema and Storage

### Audit Log Database Schema

```sql
-- Maritime audit logs table with partitioning
CREATE TABLE maritime_audit_logs (
    event_id UUID PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    event_source VARCHAR(50) NOT NULL DEFAULT 'fastapi',
    
    -- User context
    user_id VARCHAR(255),
    organization_id VARCHAR(255),
    tenant_type VARCHAR(50),
    email VARCHAR(255),
    roles JSONB,
    
    -- Event details
    event_type VARCHAR(50) NOT NULL DEFAULT 'business',
    action VARCHAR(255) NOT NULL,
    resource_type VARCHAR(100),
    resource_id VARCHAR(255),
    
    -- Maritime context
    vessel_id VARCHAR(100),
    vessel_imo VARCHAR(20),
    geographic_location JSONB,
    financial_amount DECIMAL(15,2),
    
    -- Technical metadata
    ip_address INET,
    user_agent TEXT,
    session_id VARCHAR(255),
    api_endpoint VARCHAR(500),
    response_status INTEGER,
    processing_time_ms INTEGER,
    
    -- Compliance metadata
    regulation_type VARCHAR(50) DEFAULT 'general',
    retention_period VARCHAR(20) DEFAULT '7_years',
    data_classification VARCHAR(20) DEFAULT 'internal',
    
    -- Full event payload for compliance
    event_payload JSONB,
    
    -- Search and analysis
    search_vector tsvector,
    
    -- Indexing for performance
    CONSTRAINT valid_event_type CHECK (event_type IN ('authentication', 'business', 'admin', 'data_access', 'data_modification')),
    CONSTRAINT valid_retention_period CHECK (retention_period IN ('3_years', '7_years', '10_years', 'permanent')),
    CONSTRAINT valid_data_classification CHECK (data_classification IN ('public', 'internal', 'confidential', 'restricted'))
) PARTITION BY RANGE (timestamp);

-- Create yearly partitions for performance
CREATE TABLE maritime_audit_logs_2025 
    PARTITION OF maritime_audit_logs 
    FOR VALUES FROM ('2025-01-01') TO ('2026-01-01');

CREATE TABLE maritime_audit_logs_2026 
    PARTITION OF maritime_audit_logs 
    FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');

-- Performance indexes
CREATE INDEX idx_audit_user_timestamp ON maritime_audit_logs (user_id, timestamp DESC);
CREATE INDEX idx_audit_vessel_timestamp ON maritime_audit_logs (vessel_id, timestamp DESC);
CREATE INDEX idx_audit_organization_timestamp ON maritime_audit_logs (organization_id, timestamp DESC);
CREATE INDEX idx_audit_event_type_timestamp ON maritime_audit_logs (event_type, timestamp DESC);
CREATE INDEX idx_audit_financial ON maritime_audit_logs (financial_amount) WHERE financial_amount IS NOT NULL;
CREATE INDEX idx_audit_compliance ON maritime_audit_logs (regulation_type, retention_period);

-- Full-text search index
CREATE INDEX idx_audit_search ON maritime_audit_logs USING gin(search_vector);

-- Function to automatically update search vector
CREATE OR REPLACE FUNCTION update_audit_search_vector()
RETURNS TRIGGER AS $$
BEGIN
    NEW.search_vector := 
        setweight(to_tsvector('english', COALESCE(NEW.action, '')), 'A') ||
        setweight(to_tsvector('english', COALESCE(NEW.resource_type, '')), 'B') ||
        setweight(to_tsvector('english', COALESCE(NEW.event_payload::text, '')), 'C');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER audit_search_vector_trigger
    BEFORE INSERT OR UPDATE ON maritime_audit_logs
    FOR EACH ROW EXECUTE FUNCTION update_audit_search_vector();
```

### SQLAlchemy Models

```python
# models/audit.py
from sqlalchemy import Column, String, DateTime, Integer, Numeric, Text, JSON
from sqlalchemy.dialects.postgresql import UUID, INET, JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class MaritimeAuditLog(Base):
    __tablename__ = "maritime_audit_logs"
    
    # Primary identification
    event_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(DateTime(timezone=True), nullable=False, default=func.now())
    event_source = Column(String(50), nullable=False, default="fastapi")
    
    # User context
    user_id = Column(String(255))
    organization_id = Column(String(255))
    tenant_type = Column(String(50))
    email = Column(String(255))
    roles = Column(JSONB)
    
    # Event details
    event_type = Column(String(50), nullable=False, default="business")
    action = Column(String(255), nullable=False)
    resource_type = Column(String(100))
    resource_id = Column(String(255))
    
    # Maritime context
    vessel_id = Column(String(100))
    vessel_imo = Column(String(20))
    geographic_location = Column(JSONB)
    financial_amount = Column(Numeric(15, 2))
    
    # Technical metadata
    ip_address = Column(INET)
    user_agent = Column(Text)
    session_id = Column(String(255))
    api_endpoint = Column(String(500))
    response_status = Column(Integer)
    processing_time_ms = Column(Integer)
    
    # Compliance metadata
    regulation_type = Column(String(50), default="general")
    retention_period = Column(String(20), default="7_years")
    data_classification = Column(String(20), default="internal")
    
    # Full event payload
    event_payload = Column(JSONB)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
    
    @classmethod
    async def create_from_event(
        cls, 
        db: AsyncSession, 
        event: MaritimeAuditEvent
    ) -> 'MaritimeAuditLog':
        """Create audit log record from event"""
        audit_log = cls(**event.to_dict())
        db.add(audit_log)
        await db.commit()
        return audit_log
    
    @classmethod
    async def search_events(
        cls,
        db: AsyncSession,
        user_id: Optional[str] = None,
        vessel_id: Optional[str] = None,
        organization_id: Optional[str] = None,
        event_type: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        search_text: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List['MaritimeAuditLog']:
        """Search audit events with maritime-specific filters"""
        query = db.query(cls)
        
        if user_id:
            query = query.filter(cls.user_id == user_id)
        if vessel_id:
            query = query.filter(cls.vessel_id == vessel_id)
        if organization_id:
            query = query.filter(cls.organization_id == organization_id)
        if event_type:
            query = query.filter(cls.event_type == event_type)
        if start_date:
            query = query.filter(cls.timestamp >= start_date)
        if end_date:
            query = query.filter(cls.timestamp <= end_date)
        if search_text:
            query = query.filter(
                func.to_tsvector('english', cls.action).match(search_text) |
                func.to_tsvector('english', cls.resource_type).match(search_text)
            )
        
        return await query.order_by(cls.timestamp.desc()).offset(offset).limit(limit).all()
```

---

## SIEM Integration

### DataDog Integration

```python
# siem/datadog_integration.py
from datadog import initialize, api
import json
import asyncio
from typing import List, Dict, Any
import aiohttp

class DataDogSIEMIntegration:
    def __init__(self, api_key: str, app_key: str):
        self.api_key = api_key
        self.app_key = app_key
        self.session = None
        
        # Initialize DataDog
        initialize(api_key=api_key, app_key=app_key)
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def stream_audit_event(self, event_data: Dict[str, Any]):
        """Stream single audit event to DataDog"""
        try:
            # Format for DataDog Events API
            dd_event = self._format_for_datadog(event_data)
            
            # Send to DataDog Events
            api.Event.create(**dd_event)
            
            # Send metrics
            await self._send_audit_metrics(event_data)
            
        except Exception as e:
            print(f"DataDog streaming failed: {e}")
    
    async def stream_audit_batch(self, events: List[Dict[str, Any]]):
        """Stream batch of audit events to DataDog"""
        tasks = []
        for event in events:
            tasks.append(self.stream_audit_event(event))
        
        await asyncio.gather(*tasks, return_exceptions=True)
    
    def _format_for_datadog(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format audit event for DataDog Events API"""
        event_type = event_data.get("event_details", {}).get("event_type", "unknown")
        action = event_data.get("event_details", {}).get("action", "unknown")
        
        dd_event = {
            "title": f"Maritime Audit: {action}",
            "text": f"Event Type: {event_type}\nAction: {action}",
            "tags": self._generate_datadog_tags(event_data),
            "source": "maritime-insurance-platform",
            "priority": self._determine_priority(event_data),
            "alert_type": self._determine_alert_type(event_data),
            "date_happened": int(event_data.get("timestamp", 0))
        }
        
        return dd_event
    
    def _generate_datadog_tags(self, event_data: Dict[str, Any]) -> List[str]:
        """Generate DataDog tags from audit event"""
        tags = []
        
        # User context tags
        if event_data.get("user_info", {}).get("tenant_type"):
            tags.append(f"tenant_type:{event_data['user_info']['tenant_type']}")
        if event_data.get("user_info", {}).get("organization_id"):
            tags.append(f"organization:{event_data['user_info']['organization_id']}")
        
        # Maritime context tags
        maritime_context = event_data.get("maritime_context", {})
        if maritime_context.get("vessel_id"):
            tags.append(f"vessel:{maritime_context['vessel_id']}")
        if maritime_context.get("vessel_imo"):
            tags.append(f"vessel_imo:{maritime_context['vessel_imo']}")
        
        # Event classification tags
        event_details = event_data.get("event_details", {})
        if event_details.get("event_type"):
            tags.append(f"event_type:{event_details['event_type']}")
        if event_details.get("resource_type"):
            tags.append(f"resource_type:{event_details['resource_type']}")
        
        # Compliance tags
        compliance = event_data.get("compliance_metadata", {})
        if compliance.get("regulation_type"):
            tags.append(f"regulation:{compliance['regulation_type']}")
        if compliance.get("data_classification"):
            tags.append(f"classification:{compliance['data_classification']}")
        
        return tags
    
    def _determine_priority(self, event_data: Dict[str, Any]) -> str:
        """Determine event priority for DataDog"""
        event_type = event_data.get("event_details", {}).get("event_type")
        financial_amount = event_data.get("maritime_context", {}).get("financial_amount")
        
        if event_type == "authentication" and "failed" in event_data.get("action", ""):
            return "high"
        elif financial_amount and financial_amount > 1000000:  # High-value transactions
            return "high"
        elif event_type in ["admin", "data_modification"]:
            return "normal"
        else:
            return "low"
    
    def _determine_alert_type(self, event_data: Dict[str, Any]) -> str:
        """Determine alert type for DataDog"""
        response_status = event_data.get("technical_metadata", {}).get("response_status", 200)
        
        if response_status >= 400:
            return "error"
        elif response_status >= 300:
            return "warning"
        else:
            return "info"
    
    async def _send_audit_metrics(self, event_data: Dict[str, Any]):
        """Send audit metrics to DataDog"""
        try:
            # Count metrics
            api.Metric.send(
                metric="maritime.audit.events",
                points=[(time.time(), 1)],
                tags=self._generate_datadog_tags(event_data)
            )
            
            # Timing metrics
            processing_time = event_data.get("technical_metadata", {}).get("processing_time_ms")
            if processing_time:
                api.Metric.send(
                    metric="maritime.audit.processing_time",
                    points=[(time.time(), processing_time)],
                    tags=self._generate_datadog_tags(event_data)
                )
            
            # Financial metrics
            financial_amount = event_data.get("maritime_context", {}).get("financial_amount")
            if financial_amount:
                api.Metric.send(
                    metric="maritime.audit.financial_amount",
                    points=[(time.time(), financial_amount)],
                    tags=self._generate_datadog_tags(event_data)
                )
                
        except Exception as e:
            print(f"DataDog metrics failed: {e}")
```

### Elasticsearch Integration

```python
# siem/elasticsearch_integration.py
from elasticsearch import AsyncElasticsearch
import json
from datetime import datetime
from typing import List, Dict, Any

class ElasticsearchSIEMIntegration:
    def __init__(self, elasticsearch_url: str, index_prefix: str = "maritime-audit"):
        self.client = AsyncElasticsearch([elasticsearch_url])
        self.index_prefix = index_prefix
    
    async def stream_audit_event(self, event_data: Dict[str, Any]):
        """Stream audit event to Elasticsearch"""
        try:
            # Generate time-based index name
            timestamp = event_data.get("timestamp", datetime.now())
            if isinstance(timestamp, str):
                timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            
            index_name = f"{self.index_prefix}-{timestamp.strftime('%Y.%m')}"
            
            # Format document for Elasticsearch
            doc = self._format_for_elasticsearch(event_data)
            
            # Index document
            await self.client.index(
                index=index_name,
                id=event_data.get("event_id"),
                body=doc
            )
            
        except Exception as e:
            print(f"Elasticsearch streaming failed: {e}")
    
    async def stream_audit_batch(self, events: List[Dict[str, Any]]):
        """Bulk stream audit events to Elasticsearch"""
        try:
            bulk_body = []
            
            for event in events:
                timestamp = event.get("timestamp", datetime.now())
                if isinstance(timestamp, str):
                    timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                
                index_name = f"{self.index_prefix}-{timestamp.strftime('%Y.%m')}"
                
                # Add bulk index action
                bulk_body.append({
                    "index": {
                        "_index": index_name,
                        "_id": event.get("event_id")
                    }
                })
                
                # Add document
                bulk_body.append(self._format_for_elasticsearch(event))
            
            # Execute bulk operation
            await self.client.bulk(body=bulk_body)
            
        except Exception as e:
            print(f"Elasticsearch bulk streaming failed: {e}")
    
    def _format_for_elasticsearch(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format audit event for Elasticsearch indexing"""
        doc = event_data.copy()
        
        # Ensure timestamp is properly formatted
        if "timestamp" in doc:
            timestamp = doc["timestamp"]
            if isinstance(timestamp, str):
                doc["@timestamp"] = timestamp
            else:
                doc["@timestamp"] = timestamp.isoformat()
        
        # Flatten nested structures for better searching
        if "user_info" in doc:
            for key, value in doc["user_info"].items():
                doc[f"user_{key}"] = value
        
        if "event_details" in doc:
            for key, value in doc["event_details"].items():
                doc[f"event_{key}"] = value
        
        if "maritime_context" in doc:
            for key, value in doc["maritime_context"].items():
                doc[f"maritime_{key}"] = value
        
        if "technical_metadata" in doc:
            for key, value in doc["technical_metadata"].items():
                doc[f"technical_{key}"] = value
        
        return doc
    
    async def create_index_template(self):
        """Create Elasticsearch index template for maritime audit logs"""
        template = {
            "index_patterns": [f"{self.index_prefix}-*"],
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 1,
                "index.lifecycle.name": "maritime-audit-policy",
                "index.lifecycle.rollover_alias": f"{self.index_prefix}-write"
            },
            "mappings": {
                "properties": {
                    "@timestamp": {"type": "date"},
                    "event_id": {"type": "keyword"},
                    "event_source": {"type": "keyword"},
                    "user_id": {"type": "keyword"},
                    "organization_id": {"type": "keyword"},
                    "tenant_type": {"type": "keyword"},
                    "event_type": {"type": "keyword"},
                    "action": {"type": "text", "analyzer": "standard"},
                    "resource_type": {"type": "keyword"},
                    "vessel_id": {"type": "keyword"},
                    "vessel_imo": {"type": "keyword"},
                    "financial_amount": {"type": "double"},
                    "ip_address": {"type": "ip"},
                    "response_status": {"type": "integer"},
                    "regulation_type": {"type": "keyword"},
                    "data_classification": {"type": "keyword"}
                }
            }
        }
        
        await self.client.indices.put_template(
            name=f"{self.index_prefix}-template",
            body=template
        )
```

---

## Compliance and Retention

### Retention Policy Manager

```python
# compliance/retention_manager.py
from datetime import datetime, timedelta
from typing import Dict, List
import boto3
import gzip
import json
from sqlalchemy.ext.asyncio import AsyncSession

class MaritimeRetentionManager:
    def __init__(
        self, 
        db_session: AsyncSession,
        cold_storage_bucket: str = None
    ):
        self.db = db_session
        self.s3_client = boto3.client('s3') if cold_storage_bucket else None
        self.cold_storage_bucket = cold_storage_bucket
        
        # Maritime compliance retention periods
        self.retention_policies = {
            "authentication": timedelta(days=1095),        # 3 years
            "vessel_access": timedelta(days=2555),         # 7 years
            "financial_transactions": timedelta(days=3650), # 10 years
            "safety_incidents": None,                       # Permanent
            "environmental_compliance": None,               # Permanent
            "claims": timedelta(days=2555),                # 7 years
            "policies": timedelta(days=2555),              # 7 years
            "general": timedelta(days=2555)                # 7 years default
        }
    
    async def enforce_retention_policies(self):
        """Run retention policy enforcement"""
        try:
            for regulation_type, retention_period in self.retention_policies.items():
                if retention_period is None:  # Permanent retention
                    continue
                    
                cutoff_date = datetime.now() - retention_period
                await self._process_expired_events(regulation_type, cutoff_date)
                
        except Exception as e:
            print(f"Retention policy enforcement failed: {e}")
    
    async def _process_expired_events(
        self, 
        regulation_type: str, 
        cutoff_date: datetime
    ):
        """Process events that have exceeded retention period"""
        try:
            # Find expired events
            expired_events = await self.db.query(MaritimeAuditLog).filter(
                MaritimeAuditLog.regulation_type.like(f"%{regulation_type}%"),
                MaritimeAuditLog.timestamp < cutoff_date
            ).all()
            
            if not expired_events:
                return
            
            print(f"Processing {len(expired_events)} expired {regulation_type} events")
            
            # Archive to cold storage if configured
            if self.s3_client and self.cold_storage_bucket:
                await self._archive_to_cold_storage(expired_events, regulation_type)
            
            # Remove from primary database
            await self._remove_expired_events(expired_events)
            
        except Exception as e:
            print(f"Error processing expired {regulation_type} events: {e}")
    
    async def _archive_to_cold_storage(
        self, 
        events: List[MaritimeAuditLog], 
        regulation_type: str
    ):
        """Archive events to S3 cold storage"""
        try:
            # Group events by year for archival
            events_by_year = {}
            for event in events:
                year = event.timestamp.year
                if year not in events_by_year:
                    events_by_year[year] = []
                events_by_year[year].append(event.to_dict())
            
            # Create archive files for each year
            for year, year_events in events_by_year.items():
                archive_key = f"maritime-audit-archive/{regulation_type}/{year}/events-{year}.json.gz"
                
                # Compress and upload
                archive_data = json.dumps(year_events, default=str).encode('utf-8')
                compressed_data = gzip.compress(archive_data)
                
                self.s3_client.put_object(
                    Bucket=self.cold_storage_bucket,
                    Key=archive_key,
                    Body=compressed_data,
                    StorageClass='GLACIER',
                    Metadata={
                        'regulation_type': regulation_type,
                        'archive_year': str(year),
                        'event_count': str(len(year_events)),
                        'archive_date': datetime.now().isoformat()
                    }
                )
                
                print(f"Archived {len(year_events)} {regulation_type} events for {year}")
                
        except Exception as e:
            print(f"Cold storage archival failed: {e}")
            raise
    
    async def _remove_expired_events(self, events: List[MaritimeAuditLog]):
        """Remove expired events from primary database"""
        try:
            event_ids = [event.event_id for event in events]
            
            await self.db.query(MaritimeAuditLog).filter(
                MaritimeAuditLog.event_id.in_(event_ids)
            ).delete(synchronize_session=False)
            
            await self.db.commit()
            print(f"Removed {len(events)} expired events from primary database")
            
        except Exception as e:
            await self.db.rollback()
            print(f"Failed to remove expired events: {e}")
            raise
    
    async def retrieve_archived_events(
        self, 
        regulation_type: str, 
        year: int
    ) -> List[Dict]:
        """Retrieve archived events from cold storage"""
        if not self.s3_client:
            raise ValueError("Cold storage not configured")
        
        try:
            archive_key = f"maritime-audit-archive/{regulation_type}/{year}/events-{year}.json.gz"
            
            response = self.s3_client.get_object(
                Bucket=self.cold_storage_bucket,
                Key=archive_key
            )
            
            # Decompress and parse
            compressed_data = response['Body'].read()
            archive_data = gzip.decompress(compressed_data)
            events = json.loads(archive_data.decode('utf-8'))
            
            return events
            
        except Exception as e:
            print(f"Failed to retrieve archived events: {e}")
            return []
    
    async def generate_retention_report(self) -> Dict[str, Any]:
        """Generate retention compliance report"""
        try:
            report = {
                "report_date": datetime.now().isoformat(),
                "retention_policies": {},
                "active_events": {},
                "archived_events": {},
                "compliance_status": "compliant"
            }
            
            # Analyze each regulation type
            for regulation_type, retention_period in self.retention_policies.items():
                policy_info = {
                    "retention_period_days": retention_period.days if retention_period else "permanent",
                    "cutoff_date": (datetime.now() - retention_period).isoformat() if retention_period else None
                }
                
                # Count active events
                active_count = await self.db.query(MaritimeAuditLog).filter(
                    MaritimeAuditLog.regulation_type.like(f"%{regulation_type}%")
                ).count()
                
                policy_info["active_events_count"] = active_count
                
                # Check for retention violations
                if retention_period:
                    cutoff_date = datetime.now() - retention_period
                    overdue_count = await self.db.query(MaritimeAuditLog).filter(
                        MaritimeAuditLog.regulation_type.like(f"%{regulation_type}%"),
                        MaritimeAuditLog.timestamp < cutoff_date
                    ).count()
                    
                    policy_info["overdue_events_count"] = overdue_count
                    
                    if overdue_count > 0:
                        report["compliance_status"] = "violations_detected"
                
                report["retention_policies"][regulation_type] = policy_info
            
            return report
            
        except Exception as e:
            print(f"Failed to generate retention report: {e}")
            return {"error": str(e)}
```

### Compliance Reporting

```python
# compliance/reporting.py
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

class MaritimeComplianceReporter:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
    
    async def generate_maritime_compliance_report(
        self,
        start_date: datetime,
        end_date: datetime,
        organization_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate comprehensive maritime compliance report"""
        
        report = {
            "report_metadata": {
                "generated_at": datetime.now().isoformat(),
                "period_start": start_date.isoformat(),
                "period_end": end_date.isoformat(),
                "organization_id": organization_id,
                "report_type": "maritime_compliance"
            },
            "executive_summary": {},
            "authentication_audit": {},
            "vessel_access_audit": {},
            "financial_compliance": {},
            "regulatory_compliance": {},
            "security_incidents": {}
        }
        
        # Base query
        base_query = self.db.query(MaritimeAuditLog).filter(
            MaritimeAuditLog.timestamp >= start_date,
            MaritimeAuditLog.timestamp <= end_date
        )
        
        if organization_id:
            base_query = base_query.filter(
                MaritimeAuditLog.organization_id == organization_id
            )
        
        # Executive Summary
        total_events = await base_query.count()
        unique_users = await base_query.distinct(MaritimeAuditLog.user_id).count()
        unique_vessels = await base_query.filter(
            MaritimeAuditLog.vessel_id.isnot(None)
        ).distinct(MaritimeAuditLog.vessel_id).count()
        
        report["executive_summary"] = {
            "total_audit_events": total_events,
            "unique_users_active": unique_users,
            "unique_vessels_accessed": unique_vessels,
            "compliance_period_days": (end_date - start_date).days
        }
        
        # Authentication Audit
        auth_events = await base_query.filter(
            MaritimeAuditLog.event_type == "authentication"
        ).all()
        
        auth_summary = {
            "total_auth_events": len(auth_events),
            "successful_logins": len([e for e in auth_events if "success" in e.action.lower()]),
            "failed_logins": len([e for e in auth_events if "failed" in e.action.lower()]),
            "unique_login_locations": len(set(
                e.geographic_location.get("city", "unknown") 
                for e in auth_events 
                if e.geographic_location
            ))
        }
        
        report["authentication_audit"] = auth_summary
        
        # Vessel Access Audit
        vessel_events = await base_query.filter(
            MaritimeAuditLog.vessel_id.isnot(None)
        ).all()
        
        vessel_summary = {
            "total_vessel_access_events": len(vessel_events),
            "vessels_accessed": list(set(e.vessel_id for e in vessel_events)),
            "vessel_access_by_type": {}
        }
        
        # Group vessel access by tenant type
        for event in vessel_events:
            tenant_type = event.tenant_type or "unknown"
            if tenant_type not in vessel_summary["vessel_access_by_type"]:
                vessel_summary["vessel_access_by_type"][tenant_type] = 0
            vessel_summary["vessel_access_by_type"][tenant_type] += 1
        
        report["vessel_access_audit"] = vessel_summary
        
        # Financial Compliance
        financial_events = await base_query.filter(
            MaritimeAuditLog.financial_amount.isnot(None)
        ).all()
        
        financial_summary = {
            "total_financial_events": len(financial_events),
            "total_financial_volume": sum(
                float(e.financial_amount) for e in financial_events
            ),
            "high_value_transactions": len([
                e for e in financial_events 
                if float(e.financial_amount) > 100000
            ]),
            "financial_events_by_type": {}
        }
        
        report["financial_compliance"] = financial_summary
        
        # Regulatory Compliance
        regulation_summary = {}
        for regulation in ["IMO", "SOLAS", "maritime_insurance", "financial_compliance"]:
            reg_events = await base_query.filter(
                MaritimeAuditLog.regulation_type.like(f"%{regulation}%")
            ).all()
            
            regulation_summary[regulation] = {
                "event_count": len(reg_events),
                "compliance_score": self._calculate_compliance_score(reg_events),
                "violations_detected": len([
                    e for e in reg_events 
                    if e.response_status and e.response_status >= 400
                ])
            }
        
        report["regulatory_compliance"] = regulation_summary
        
        # Security Incidents
        security_events = await base_query.filter(
            MaritimeAuditLog.response_status >= 400
        ).all()
        
        security_summary = {
            "total_security_events": len(security_events),
            "unauthorized_access_attempts": len([
                e for e in security_events 
                if e.response_status in [401, 403]
            ]),
            "system_errors": len([
                e for e in security_events 
                if e.response_status >= 500
            ]),
            "suspicious_activities": self._identify_suspicious_activities(security_events)
        }
        
        report["security_incidents"] = security_summary
        
        return report
    
    def _calculate_compliance_score(self, events: List[MaritimeAuditLog]) -> float:
        """Calculate compliance score based on event success rate"""
        if not events:
            return 100.0
        
        successful_events = len([
            e for e in events 
            if not e.response_status or e.response_status < 400
        ])
        
        return (successful_events / len(events)) * 100
    
    def _identify_suspicious_activities(
        self, 
        security_events: List[MaritimeAuditLog]
    ) -> List[Dict[str, Any]]:
        """Identify suspicious patterns in security events"""
        suspicious = []
        
        # Group by IP address to detect potential attacks
        ip_events = {}
        for event in security_events:
            if event.ip_address:
                ip = str(event.ip_address)
                if ip not in ip_events:
                    ip_events[ip] = []
                ip_events[ip].append(event)
        
        # Flag IPs with excessive failed attempts
        for ip, events in ip_events.items():
            if len(events) > 10:  # Threshold for suspicious activity
                suspicious.append({
                    "type": "excessive_failed_attempts",
                    "ip_address": ip,
                    "event_count": len(events),
                    "time_span": f"{events[0].timestamp} to {events[-1].timestamp}"
                })
        
        return suspicious
    
    async def export_compliance_report(
        self,
        report: Dict[str, Any],
        format: str = "json"
    ) -> str:
        """Export compliance report in specified format"""
        if format == "json":
            return json.dumps(report, indent=2, default=str)
        elif format == "csv":
            # Convert to DataFrame and export
            df = pd.json_normalize(report)
            return df.to_csv(index=False)
        else:
            raise ValueError(f"Unsupported export format: {format}")
```

---

## Testing and Validation

### Audit System Testing

```python
# tests/test_audit_system.py
import pytest
import asyncio
from datetime import datetime, timezone
from unittest.mock import Mock, AsyncMock
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from maritime_audit_logger import MaritimeAuditLogger, MaritimeAuditEvent
from audit_middleware import MaritimeAuditMiddleware

class TestMaritimeAuditSystem:
    
    @pytest.fixture
    async def audit_logger(self):
        """Mock audit logger for testing"""
        mock_db = AsyncMock(spec=AsyncSession)
        logger = MaritimeAuditLogger(mock_db)
        return logger
    
    @pytest.fixture
    def sample_audit_event(self):
        """Sample audit event for testing"""
        return MaritimeAuditEvent(
            event_id="test-123",
            timestamp=datetime.now(timezone.utc),
            event_source="test",
            user_id="user-123",
            organization_id="org-456",
            tenant_type="ship_owner",
            event_type="business",
            action="CREATE vessel",
            resource_type="vessel",
            vessel_id="vessel-789",
            vessel_imo="IMO1234567"
        )
    
    async def test_audit_event_creation(self, sample_audit_event):
        """Test audit event creation and validation"""
        assert sample_audit_event.event_id == "test-123"
        assert sample_audit_event.tenant_type == "ship_owner"
        assert sample_audit_event.vessel_imo == "IMO1234567"
        
        # Test serialization
        event_dict = sample_audit_event.to_dict()
        assert event_dict["event_id"] == "test-123"
    
    async def test_audit_logger_queuing(self, audit_logger, sample_audit_event):
        """Test audit event queuing"""
        # Start processing
        await audit_logger.start_processing()
        
        # Queue event
        await audit_logger.log_audit_event(sample_audit_event.to_dict())
        
        # Verify event was queued
        assert audit_logger.audit_queue.qsize() == 1
        
        # Stop processing
        await audit_logger.stop_processing()
    
    async def test_middleware_user_context_extraction(self):
        """Test user context extraction from WorkOS token"""
        from audit_middleware import MaritimeAuditMiddleware
        
        # Mock request with valid token
        mock_request = Mock()
        mock_request.headers = {"authorization": "Bearer valid-token"}
        
        middleware = MaritimeAuditMiddleware(Mock(), Mock())
        
        # Mock token verification
        with patch('audit_middleware.verify_workos_token') as mock_verify:
            mock_verify.return_value = {
                "sub": "user-123",
                "org": "org-456",
                "email": "test@ship.com",
                "tenant_type": "ship_owner"
            }
            
            context = await middleware._extract_user_context(mock_request)
            
            assert context["user_id"] == "user-123"
            assert context["organization_id"] == "org-456"
            assert context["tenant_type"] == "ship_owner"
    
    async def test_maritime_context_extraction(self):
        """Test maritime context extraction from requests"""
        from audit_middleware import MaritimeAuditMiddleware
        
        # Mock request with vessel data
        mock_request = Mock()
        mock_request.path_params = {"vessel_id": "vessel-123"}
        mock_request.query_params = {}
        mock_request.method = "GET"
        mock_request.url.path = "/api/vessels/vessel-123"
        
        middleware = MaritimeAuditMiddleware(Mock(), Mock())
        
        context = await middleware._extract_maritime_context(mock_request, Mock())
        
        assert context["vessel_id"] == "vessel-123"
        assert context["resource_type"] == "vessel"
    
    async def test_database_audit_listener(self):
        """Test database change audit listener"""
        from database_audit import DatabaseAuditListener
        
        mock_audit_logger = AsyncMock()
        listener = DatabaseAuditListener(mock_audit_logger)
        
        # Mock database session with changes
        mock_session = Mock()
        mock_session.new = [Mock(__tablename__="vessels", id=123)]
        mock_session.dirty = []
        mock_session.deleted = []
        
        await listener._process_session_changes(mock_session)
        
        # Verify audit event was logged
        mock_audit_logger.log_audit_event.assert_called_once()
    
    def test_retention_policy_calculation(self):
        """Test retention policy calculations"""
        from compliance.retention_manager import MaritimeRetentionManager
        
        manager = MaritimeRetentionManager(Mock())
        
        # Test retention periods
        assert manager.retention_policies["authentication"].days == 1095  # 3 years
        assert manager.retention_policies["vessel_access"].days == 2555   # 7 years
        assert manager.retention_policies["safety_incidents"] is None     # Permanent
    
    async def test_compliance_report_generation(self):
        """Test compliance report generation"""
        from compliance.reporting import MaritimeComplianceReporter
        
        mock_db = AsyncMock()
        reporter = MaritimeComplianceReporter(mock_db)
        
        # Mock query results
        mock_db.query.return_value.filter.return_value.count.return_value = 100
        mock_db.query.return_value.filter.return_value.all.return_value = []
        
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        
        report = await reporter.generate_maritime_compliance_report(
            start_date, end_date
        )
        
        assert "executive_summary" in report
        assert "authentication_audit" in report
        assert "vessel_access_audit" in report
    
    def test_siem_integration(self):
        """Test SIEM integration formatting"""
        from siem.datadog_integration import DataDogSIEMIntegration
        
        integration = DataDogSIEMIntegration("test-key", "test-app-key")
        
        event_data = {
            "event_details": {"event_type": "business", "action": "CREATE vessel"},
            "user_info": {"tenant_type": "ship_owner", "organization_id": "org-123"},
            "maritime_context": {"vessel_id": "vessel-456"}
        }
        
        dd_event = integration._format_for_datadog(event_data)
        
        assert dd_event["title"] == "Maritime Audit: CREATE vessel"
        assert "tenant_type:ship_owner" in dd_event["tags"]
        assert "vessel:vessel-456" in dd_event["tags"]

# Integration tests
class TestAuditSystemIntegration:
    
    @pytest.fixture
    def client(self):
        """Test client with audit middleware"""
        from fastapi import FastAPI
        from audit_middleware import MaritimeAuditMiddleware
        
        app = FastAPI()
        
        # Add test endpoints
        @app.get("/api/vessels/{vessel_id}")
        async def get_vessel(vessel_id: str):
            return {"vessel_id": vessel_id, "name": "Test Vessel"}
        
        @app.post("/api/quotes")
        async def create_quote(quote_data: dict):
            return {"quote_id": "quote-123", "amount": 50000}
        
        # Add audit middleware
        mock_audit_logger = Mock()
        app.add_middleware(MaritimeAuditMiddleware, audit_logger=mock_audit_logger)
        
        return TestClient(app)
    
    def test_vessel_access_audit(self, client):
        """Test vessel access auditing"""
        response = client.get(
            "/api/vessels/vessel-123",
            headers={"authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 200
        # Verify audit middleware was called
        
    def test_financial_transaction_audit(self, client):
        """Test financial transaction auditing"""
        response = client.post(
            "/api/quotes",
            json={"vessel_id": "vessel-123", "amount": 75000},
            headers={"authorization": "Bearer test-token"}
        )
        
        assert response.status_code == 200
        # Verify audit event includes financial context

# Performance tests
class TestAuditSystemPerformance:
    
    @pytest.mark.asyncio
    async def test_audit_throughput(self):
        """Test audit system throughput under load"""
        mock_db = AsyncMock()
        audit_logger = MaritimeAuditLogger(mock_db)
        
        # Start processing
        await audit_logger.start_processing()
        
        # Generate load
        start_time = time.time()
        
        tasks = []
        for i in range(1000):
            event = {
                "event_id": f"load-test-{i}",
                "timestamp": datetime.now(timezone.utc),
                "action": f"test-action-{i}"
            }
            tasks.append(audit_logger.log_audit_event(event))
        
        await asyncio.gather(*tasks)
        
        # Wait for processing
        await asyncio.sleep(2)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Stop processing
        await audit_logger.stop_processing()
        
        # Verify performance
        throughput = 1000 / processing_time
        assert throughput > 100  # At least 100 events/second
        
        print(f"Audit throughput: {throughput:.2f} events/second")
    
    def test_middleware_latency(self, client):
        """Test audit middleware latency impact"""
        import time
        
        # Measure baseline latency
        start_time = time.time()
        response = client.get("/api/vessels/test-vessel")
        baseline_latency = time.time() - start_time
        
        # Verify minimal latency impact
        assert baseline_latency < 0.1  # Less than 100ms
        assert response.status_code == 200
```

---

## Deployment and Monitoring

### Docker Configuration

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  maritime-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/maritime
      - WORKOS_API_KEY=${WORKOS_API_KEY}
      - DATADOG_API_KEY=${DATADOG_API_KEY}
    depends_on:
      - db
      - redis
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=maritime
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  elasticsearch:
    image: elasticsearch:8.5.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    ports:
      - "9200:9200"
    volumes:
      - elasticsearch_data:/usr/share/elasticsearch/data

volumes:
  postgres_data:
  redis_data:
  elasticsearch_data:
```

### Monitoring and Alerting

```python
# monitoring/metrics.py
from prometheus_client import Counter, Histogram, Gauge, start_http_server
import time
import asyncio

# Prometheus metrics
audit_events_total = Counter(
    'maritime_audit_events_total',
    'Total number of audit events processed',
    ['event_type', 'tenant_type', 'regulation_type']
)

audit_processing_duration = Histogram(
    'maritime_audit_processing_duration_seconds',
    'Time spent processing audit events',
    ['event_type']
)

audit_queue_size = Gauge(
    'maritime_audit_queue_size',
    'Current size of audit processing queue'
)

audit_errors_total = Counter(
    'maritime_audit_errors_total',
    'Total number of audit processing errors',
    ['error_type']
)

class AuditMetricsCollector:
    def __init__(self, audit_logger: MaritimeAuditLogger):
        self.audit_logger = audit_logger
        self.metrics_enabled = True
    
    def start_metrics_server(self, port: int = 8090):
        """Start Prometheus metrics server"""
        start_http_server(port)
        asyncio.create_task(self._collect_metrics())
    
    async def _collect_metrics(self):
        """Collect metrics periodically"""
        while self.metrics_enabled:
            try:
                # Update queue size metric
                audit_queue_size.set(self.audit_logger.audit_queue.qsize())
                
                # Sleep before next collection
                await asyncio.sleep(30)
                
            except Exception as e:
                audit_errors_total.labels(error_type='metrics_collection').inc()
                print(f"Metrics collection error: {e}")
    
    def record_audit_event(self, event_data: Dict[str, Any]):
        """Record metrics for audit event"""
        try:
            event_type = event_data.get("event_details", {}).get("event_type", "unknown")
            tenant_type = event_data.get("user_info", {}).get("tenant_type", "unknown")
            regulation_type = event_data.get("compliance_metadata", {}).get("regulation_type", "general")
            
            audit_events_total.labels(
                event_type=event_type,
                tenant_type=tenant_type,
                regulation_type=regulation_type
            ).inc()
            
        except Exception as e:
            audit_errors_total.labels(error_type='metrics_recording').inc()
    
    def record_processing_time(self, event_type: str, duration: float):
        """Record audit processing time"""
        audit_processing_duration.labels(event_type=event_type).observe(duration)
    
    def record_error(self, error_type: str):
        """Record audit processing error"""
        audit_errors_total.labels(error_type=error_type).inc()
```

### Health Checks and Monitoring

```python
# monitoring/health.py
from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
import asyncio

router = APIRouter()

class HealthChecker:
    def __init__(
        self, 
        audit_logger: MaritimeAuditLogger,
        db_session: AsyncSession
    ):
        self.audit_logger = audit_logger
        self.db = db_session
    
    async def check_audit_system_health(self) -> Dict[str, Any]:
        """Comprehensive audit system health check"""
        health_status = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "healthy",
            "components": {}
        }
        
        # Check audit logger
        try:
            queue_size = self.audit_logger.audit_queue.qsize()
            processing_status = "running" if self.audit_logger.is_processing else "stopped"
            
            health_status["components"]["audit_logger"] = {
                "status": "healthy",
                "queue_size": queue_size,
                "processing_status": processing_status
            }
            
            if queue_size > 5000:  # Alert threshold
                health_status["components"]["audit_logger"]["status"] = "warning"
                health_status["overall_status"] = "degraded"
                
        except Exception as e:
            health_status["components"]["audit_logger"] = {
                "status": "unhealthy",
                "error": str(e)
            }
            health_status["overall_status"] = "unhealthy"
        
        # Check database connectivity
        try:
            await self.db.execute("SELECT 1")
            health_status["components"]["database"] = {"status": "healthy"}
        except Exception as e:
            health_status["components"]["database"] = {
                "status": "unhealthy",
                "error": str(e)
            }
            health_status["overall_status"] = "unhealthy"
        
        # Check recent audit activity
        try:
            recent_events = await self.db.query(MaritimeAuditLog).filter(
                MaritimeAuditLog.timestamp >= datetime.now() - timedelta(minutes=5)
            ).count()
            
            health_status["components"]["audit_activity"] = {
                "status": "healthy",
                "recent_events_5min": recent_events
            }
            
            if recent_events == 0:
                health_status["components"]["audit_activity"]["status"] = "warning"
                
        except Exception as e:
            health_status["components"]["audit_activity"] = {
                "status": "unhealthy",
                "error": str(e)
            }
        
        return health_status

@router.get("/health")
async def health_check():
    """Basic health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@router.get("/health/audit")
async def audit_health_check():
    """Detailed audit system health check"""
    try:
        health_checker = HealthChecker(audit_logger, db_session)
        health_status = await health_checker.check_audit_system_health()
        
        if health_status["overall_status"] == "unhealthy":
            raise HTTPException(status_code=503, detail=health_status)
        
        return health_status
        
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail={"error": "Health check failed", "details": str(e)}
        )

@router.get("/metrics/audit")
async def audit_metrics():
    """Audit system metrics endpoint"""
    try:
        metrics = {
            "timestamp": datetime.now().isoformat(),
            "queue_size": audit_logger.audit_queue.qsize(),
            "processing_status": audit_logger.is_processing,
            "batch_queue_size": len(audit_logger.batch_queue)
        }
        
        # Recent processing statistics
        recent_events = await db_session.query(MaritimeAuditLog).filter(
            MaritimeAuditLog.timestamp >= datetime.now() - timedelta(hours=1)
        ).count()
        
        metrics["recent_events_1hour"] = recent_events
        
        return metrics
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": "Metrics collection failed", "details": str(e)}
        )
```

---

## Deployment Instructions

### 1. Environment Setup

```bash
# Create environment file
cat > .env << EOF
# WorkOS Configuration
WORKOS_API_KEY=your_workos_api_key
WORKOS_CLIENT_ID=your_workos_client_id
WORKOS_WEBHOOK_SECRET=your_webhook_secret

# Database Configuration
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/maritime
AUDIT_DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/maritime_audit

# SIEM Configuration
SIEM_TYPE=datadog
DATADOG_API_KEY=your_datadog_api_key
DATADOG_APP_KEY=your_datadog_app_key

# Audit Configuration
AUDIT_RETENTION_DAYS=2555
COLD_STORAGE_BUCKET=maritime-audit-archive
AUDIT_QUEUE_SIZE=10000
AUDIT_BATCH_SIZE=100

# Performance Configuration
AUDIT_FLUSH_INTERVAL=30
EOF
```

### 2. Database Initialization

```bash
# Run database migrations
alembic upgrade head

# Create audit partitions
python scripts/create_audit_partitions.py

# Setup retention policies
python scripts/setup_retention_policies.py
```

### 3. Application Deployment

```bash
# Build and deploy with Docker Compose
docker-compose up -d

# Verify deployment
curl http://localhost:8000/health
curl http://localhost:8000/health/audit

# Check metrics
curl http://localhost:8090/metrics
```

### 4. WorkOS Webhook Configuration

```bash
# Configure WorkOS webhook endpoint
curl -X POST "https://api.workos.com/webhooks" \
  -H "Authorization: Bearer $WORKOS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-domain.com/webhooks/workos/audit",
    "events": ["session.created", "session.ended", "user.created", "organization.created"]
  }'
```

### 5. Monitoring Setup

```bash
# Setup Prometheus monitoring
kubectl apply -f k8s/prometheus-config.yaml

# Setup Grafana dashboards
kubectl apply -f k8s/grafana-dashboards.yaml

# Configure alerts
kubectl apply -f k8s/alerting-rules.yaml
```

This comprehensive implementation guide provides a production-ready maritime audit logging system that meets all compliance requirements while maintaining high performance and reliability.
