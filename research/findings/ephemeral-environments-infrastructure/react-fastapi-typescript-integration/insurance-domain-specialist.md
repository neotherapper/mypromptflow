# Insurance Domain Specialist Analysis

## Overview

This analysis focuses on insurance platform-specific patterns for React/FastAPI integration, examining complex domain models, form validation with shared schemas, file upload patterns, and real-time updates for broker competition workflows.

## Key Findings

### 1. Insurance Domain Data Models (2025)

**Core Insurance Entities:**
Based on industry standards including FIB-DM (Financial Institutions Blueprint Data Model) and ACORD Reference Architecture, the insurance domain includes 3,016+ normative entities. Key entities for the VanguardAI platform include:

**Primary Entities:**
- **Policy**: Core insurance contract with coverage details, premiums, and terms
- **Customer**: Policyholder information with KYC/AML compliance requirements
- **Claim**: Individual claims with processing workflows and settlement details
- **Broker**: Intermediary agent information with commission structures
- **Coverage**: Specific insurance coverage types and limits
- **Premium**: Payment structures and billing information

**TypeScript Domain Models:**
```typescript
// libs/shared-types/src/insurance/policy.ts
export interface PolicyEntity {
  id: string;
  customerId: string;
  policyNumber: string;
  coverageType: CoverageType;
  status: PolicyStatus;
  effectiveDate: Date;
  expirationDate: Date;
  premiumAmount: number;
  deductible: number;
  coverageLimit: number;
  documents: PolicyDocument[];
  claims: ClaimEntity[];
  brokerIds: string[];
  createdAt: Date;
  updatedAt: Date;
}

export type CoverageType = 'auto' | 'home' | 'life' | 'health' | 'commercial' | 'umbrella';
export type PolicyStatus = 'active' | 'inactive' | 'pending' | 'cancelled' | 'expired';

export interface ClaimEntity {
  id: string;
  policyId: string;
  claimNumber: string;
  claimType: string;
  status: ClaimStatus;
  reportedDate: Date;
  incidentDate: Date;
  claimAmount: number;
  settlementAmount?: number;
  description: string;
  adjusterId?: string;
  documents: ClaimDocument[];
  timeline: ClaimTimelineEvent[];
}

export type ClaimStatus = 'open' | 'investigating' | 'pending_review' | 'approved' | 'denied' | 'settled';
```

### 2. FastAPI + Pydantic Domain Models

**Backend Domain Models:**
```python
# backend/app/models/insurance.py
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, validator
from enum import Enum

class CoverageType(str, Enum):
    AUTO = "auto"
    HOME = "home"
    LIFE = "life"
    HEALTH = "health"
    COMMERCIAL = "commercial"
    UMBRELLA = "umbrella"

class PolicyStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    CANCELLED = "cancelled"
    EXPIRED = "expired"

class PolicyCreateRequest(BaseModel):
    customer_id: str = Field(..., description="Customer UUID")
    coverage_type: CoverageType
    premium_amount: float = Field(..., gt=0, description="Premium amount must be positive")
    deductible: float = Field(..., ge=0, description="Deductible amount")
    coverage_limit: float = Field(..., gt=0, description="Coverage limit")
    effective_date: datetime
    expiration_date: datetime
    
    @validator('expiration_date')
    def validate_expiration_date(cls, v, values):
        if 'effective_date' in values and v <= values['effective_date']:
            raise ValueError('Expiration date must be after effective date')
        return v
    
    @validator('premium_amount')
    def validate_premium_amount(cls, v, values):
        if 'coverage_type' in values:
            # Insurance-specific business rules
            if values['coverage_type'] == CoverageType.AUTO and v < 100:
                raise ValueError('Auto insurance premium must be at least $100')
            if values['coverage_type'] == CoverageType.HOME and v < 200:
                raise ValueError('Home insurance premium must be at least $200')
        return v

class PolicyResponse(BaseModel):
    id: str
    customer_id: str
    policy_number: str
    coverage_type: CoverageType
    status: PolicyStatus
    effective_date: datetime
    expiration_date: datetime
    premium_amount: float
    deductible: float
    coverage_limit: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True
```

### 3. Form Validation with Shared Schemas

**Pydantic + React Hook Form Integration:**
```typescript
// libs/shared-types/src/validation/insurance-schemas.ts
import { z } from 'zod';

export const PolicyCreateSchema = z.object({
  customerId: z.string().uuid('Invalid customer ID format'),
  coverageType: z.enum(['auto', 'home', 'life', 'health', 'commercial', 'umbrella']),
  premiumAmount: z.number().positive('Premium amount must be positive'),
  deductible: z.number().nonnegative('Deductible cannot be negative'),
  coverageLimit: z.number().positive('Coverage limit must be positive'),
  effectiveDate: z.date(),
  expirationDate: z.date(),
}).refine((data) => data.expirationDate > data.effectiveDate, {
  message: 'Expiration date must be after effective date',
  path: ['expirationDate'],
}).refine((data) => {
  // Insurance-specific business rules
  if (data.coverageType === 'auto' && data.premiumAmount < 100) {
    return false;
  }
  if (data.coverageType === 'home' && data.premiumAmount < 200) {
    return false;
  }
  return true;
}, {
  message: 'Premium amount does not meet minimum requirements for coverage type',
  path: ['premiumAmount'],
});

export type PolicyCreateRequest = z.infer<typeof PolicyCreateSchema>;
```

**React Hook Form Implementation:**
```typescript
// components/PolicyForm.tsx
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { PolicyCreateSchema, PolicyCreateRequest } from '@vanguardai/shared-types';
import { useCreatePolicyMutation } from '../hooks/usePolicy';

interface PolicyFormProps {
  customerId: string;
  onSuccess: (policy: PolicyResponse) => void;
}

export const PolicyForm: React.FC<PolicyFormProps> = ({ customerId, onSuccess }) => {
  const {
    control,
    handleSubmit,
    formState: { errors, isValid },
    watch,
  } = useForm<PolicyCreateRequest>({
    resolver: zodResolver(PolicyCreateSchema),
    defaultValues: {
      customerId,
      coverageType: 'auto',
      premiumAmount: 0,
      deductible: 0,
      coverageLimit: 0,
      effectiveDate: new Date(),
      expirationDate: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000), // 1 year from now
    },
  });

  const createPolicyMutation = useCreatePolicyMutation();
  const coverageType = watch('coverageType');

  const onSubmit = async (data: PolicyCreateRequest) => {
    try {
      const policy = await createPolicyMutation.mutateAsync(data);
      onSuccess(policy);
    } catch (error) {
      // Error handling with insurance-specific error messages
      handleInsuranceError(error);
    }
  };

  // Dynamic form behavior based on coverage type
  const getMinimumPremium = (coverageType: string) => {
    switch (coverageType) {
      case 'auto': return 100;
      case 'home': return 200;
      case 'life': return 50;
      case 'health': return 150;
      case 'commercial': return 500;
      case 'umbrella': return 300;
      default: return 0;
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="policy-form">
      <Controller
        name="coverageType"
        control={control}
        render={({ field }) => (
          <select {...field} className="form-select">
            <option value="auto">Auto Insurance</option>
            <option value="home">Home Insurance</option>
            <option value="life">Life Insurance</option>
            <option value="health">Health Insurance</option>
            <option value="commercial">Commercial Insurance</option>
            <option value="umbrella">Umbrella Insurance</option>
          </select>
        )}
      />
      {errors.coverageType && (
        <span className="error">{errors.coverageType.message}</span>
      )}

      <Controller
        name="premiumAmount"
        control={control}
        render={({ field }) => (
          <input
            type="number"
            {...field}
            placeholder={`Minimum: $${getMinimumPremium(coverageType)}`}
            className="form-input"
            onChange={(e) => field.onChange(parseFloat(e.target.value))}
          />
        )}
      />
      {errors.premiumAmount && (
        <span className="error">{errors.premiumAmount.message}</span>
      )}

      {/* Additional form fields with insurance-specific validation */}
      
      <button type="submit" disabled={!isValid || createPolicyMutation.isLoading}>
        {createPolicyMutation.isLoading ? 'Creating Policy...' : 'Create Policy'}
      </button>
    </form>
  );
};
```

### 4. File Upload Patterns for Insurance Documents

**FastAPI File Upload Handler:**
```python
# backend/app/routes/documents.py
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List
import aiofiles
import os
from pathlib import Path

router = APIRouter()

ALLOWED_EXTENSIONS = {'.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

@router.post("/policies/{policy_id}/documents")
async def upload_policy_document(
    policy_id: str,
    file: UploadFile = File(...),
    document_type: str = "general",  # claim, policy, id, medical_record, etc.
    current_user: User = Depends(get_current_user)
):
    # Validate file type
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Validate file size
    file_size = 0
    content = await file.read()
    file_size = len(content)
    
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File size exceeds maximum allowed size of {MAX_FILE_SIZE / (1024*1024)}MB"
        )
    
    # Generate secure filename
    filename = f"{policy_id}_{document_type}_{int(time.time())}_{file.filename}"
    file_path = Path(f"uploads/policies/{policy_id}/{filename}")
    
    # Ensure directory exists
    file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save file
    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(content)
    
    # Create database record
    document = await create_policy_document(
        policy_id=policy_id,
        filename=filename,
        original_filename=file.filename,
        document_type=document_type,
        file_size=file_size,
        file_path=str(file_path),
        uploaded_by=current_user.id
    )
    
    return {
        "id": document.id,
        "filename": document.filename,
        "document_type": document.document_type,
        "file_size": document.file_size,
        "upload_date": document.created_at
    }
```

**React File Upload Component:**
```typescript
// components/DocumentUpload.tsx
import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { useUploadPolicyDocumentMutation } from '../hooks/useDocuments';

interface DocumentUploadProps {
  policyId: string;
  documentType: string;
  onUploadComplete: (document: DocumentResponse) => void;
}

export const DocumentUpload: React.FC<DocumentUploadProps> = ({
  policyId,
  documentType,
  onUploadComplete,
}) => {
  const [uploadProgress, setUploadProgress] = useState(0);
  const uploadMutation = useUploadPolicyDocumentMutation();

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    for (const file of acceptedFiles) {
      try {
        // Validate file on client side
        if (!validateInsuranceDocument(file, documentType)) {
          return;
        }

        // Create FormData for upload
        const formData = new FormData();
        formData.append('file', file);
        formData.append('document_type', documentType);

        // Upload with progress tracking
        const response = await uploadMutation.mutateAsync({
          policyId,
          formData,
          onUploadProgress: (progressEvent) => {
            const progress = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
            setUploadProgress(progress);
          },
        });

        onUploadComplete(response);
        setUploadProgress(0);
      } catch (error) {
        handleDocumentUploadError(error);
      }
    }
  }, [policyId, documentType, uploadMutation, onUploadComplete]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'image/*': ['.jpg', '.jpeg', '.png'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    },
    maxSize: 10 * 1024 * 1024, // 10MB
    multiple: true,
  });

  return (
    <div className="document-upload">
      <div {...getRootProps()} className={`dropzone ${isDragActive ? 'active' : ''}`}>
        <input {...getInputProps()} />
        {isDragActive ? (
          <p>Drop the documents here...</p>
        ) : (
          <p>Drag and drop insurance documents here, or click to select files</p>
        )}
      </div>
      
      {uploadProgress > 0 && (
        <div className="upload-progress">
          <div className="progress-bar">
            <div 
              className="progress-fill" 
              style={{ width: `${uploadProgress}%` }}
            />
          </div>
          <span>{uploadProgress}% uploaded</span>
        </div>
      )}
    </div>
  );
};

// Insurance document validation
const validateInsuranceDocument = (file: File, documentType: string): boolean => {
  const maxSizes = {
    'policy': 5 * 1024 * 1024, // 5MB for policy documents
    'claim': 10 * 1024 * 1024, // 10MB for claim documents
    'medical_record': 15 * 1024 * 1024, // 15MB for medical records
    'id': 2 * 1024 * 1024, // 2MB for ID documents
  };

  const maxSize = maxSizes[documentType] || 10 * 1024 * 1024;
  
  if (file.size > maxSize) {
    alert(`File size exceeds maximum allowed size for ${documentType}`);
    return false;
  }

  return true;
};
```

### 5. Real-time Updates for Broker Competition Workflows

**WebSocket Handler for Broker Competition:**
```python
# backend/app/websockets/broker_competition.py
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List
import json
import asyncio

class BrokerCompetitionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.competition_data: Dict[str, Dict] = {}

    async def connect(self, websocket: WebSocket, competition_id: str):
        await websocket.accept()
        if competition_id not in self.active_connections:
            self.active_connections[competition_id] = []
        self.active_connections[competition_id].append(websocket)

    def disconnect(self, websocket: WebSocket, competition_id: str):
        if competition_id in self.active_connections:
            self.active_connections[competition_id].remove(websocket)
            if not self.active_connections[competition_id]:
                del self.active_connections[competition_id]

    async def broadcast_competition_update(self, competition_id: str, update_data: dict):
        if competition_id in self.active_connections:
            message = json.dumps({
                "type": "competition_update",
                "competition_id": competition_id,
                "data": update_data,
                "timestamp": datetime.utcnow().isoformat()
            })
            
            disconnected_connections = []
            for connection in self.active_connections[competition_id]:
                try:
                    await connection.send_text(message)
                except WebSocketDisconnect:
                    disconnected_connections.append(connection)
            
            # Remove disconnected connections
            for connection in disconnected_connections:
                self.active_connections[competition_id].remove(connection)

    async def update_broker_quote(self, competition_id: str, broker_id: str, quote_data: dict):
        # Update competition data
        if competition_id not in self.competition_data:
            self.competition_data[competition_id] = {"quotes": {}}
        
        self.competition_data[competition_id]["quotes"][broker_id] = {
            **quote_data,
            "updated_at": datetime.utcnow().isoformat()
        }
        
        # Broadcast update to all connected clients
        await self.broadcast_competition_update(competition_id, {
            "type": "quote_update",
            "broker_id": broker_id,
            "quote": quote_data
        })

manager = BrokerCompetitionManager()

@router.websocket("/ws/competition/{competition_id}")
async def websocket_endpoint(websocket: WebSocket, competition_id: str):
    await manager.connect(websocket, competition_id)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            if message["type"] == "subscribe":
                # Send current competition state
                current_data = manager.competition_data.get(competition_id, {})
                await websocket.send_text(json.dumps({
                    "type": "competition_state",
                    "data": current_data
                }))
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, competition_id)
```

**React WebSocket Integration:**
```typescript
// hooks/useBrokerCompetition.ts
import { useEffect, useState, useCallback } from 'react';
import { BrokerCompetition, BrokerQuote } from '@vanguardai/shared-types';

interface CompetitionUpdate {
  type: 'competition_update' | 'quote_update' | 'competition_state';
  competition_id: string;
  data: any;
  timestamp: string;
}

export const useBrokerCompetition = (competitionId: string) => {
  const [competition, setCompetition] = useState<BrokerCompetition | null>(null);
  const [quotes, setQuotes] = useState<Record<string, BrokerQuote>>({});
  const [isConnected, setIsConnected] = useState(false);

  const handleMessage = useCallback((event: MessageEvent) => {
    const update: CompetitionUpdate = JSON.parse(event.data);
    
    switch (update.type) {
      case 'competition_state':
        setCompetition(update.data);
        setQuotes(update.data.quotes || {});
        break;
      
      case 'quote_update':
        setQuotes(prev => ({
          ...prev,
          [update.data.broker_id]: update.data.quote
        }));
        break;
      
      case 'competition_update':
        // Handle general competition updates
        setCompetition(prev => ({
          ...prev,
          ...update.data
        }));
        break;
    }
  }, []);

  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:8000/ws/competition/${competitionId}`);
    
    ws.onopen = () => {
      setIsConnected(true);
      // Subscribe to competition updates
      ws.send(JSON.stringify({ type: 'subscribe' }));
    };
    
    ws.onmessage = handleMessage;
    
    ws.onclose = () => {
      setIsConnected(false);
    };
    
    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setIsConnected(false);
    };

    return () => {
      ws.close();
    };
  }, [competitionId, handleMessage]);

  return {
    competition,
    quotes,
    isConnected,
  };
};
```

**Broker Competition Component:**
```typescript
// components/BrokerCompetition.tsx
import { useBrokerCompetition } from '../hooks/useBrokerCompetition';
import { BrokerQuote } from '@vanguardai/shared-types';

interface BrokerCompetitionProps {
  competitionId: string;
}

export const BrokerCompetition: React.FC<BrokerCompetitionProps> = ({ competitionId }) => {
  const { competition, quotes, isConnected } = useBrokerCompetition(competitionId);

  const sortedQuotes = Object.entries(quotes).sort(([, a], [, b]) => a.premium - b.premium);

  return (
    <div className="broker-competition">
      <div className="connection-status">
        <span className={`status ${isConnected ? 'connected' : 'disconnected'}`}>
          {isConnected ? 'Live Updates' : 'Disconnected'}
        </span>
      </div>

      <div className="competition-header">
        <h2>Broker Competition</h2>
        {competition && (
          <div className="competition-info">
            <p>Policy Type: {competition.policy_type}</p>
            <p>Customer: {competition.customer_name}</p>
            <p>Status: {competition.status}</p>
          </div>
        )}
      </div>

      <div className="quotes-list">
        <h3>Live Quotes</h3>
        {sortedQuotes.map(([brokerId, quote]) => (
          <div key={brokerId} className="quote-card">
            <div className="broker-info">
              <h4>{quote.broker_name}</h4>
              <span className="broker-rating">Rating: {quote.rating}/5</span>
            </div>
            <div className="quote-details">
              <div className="premium">
                <span className="amount">${quote.premium.toLocaleString()}</span>
                <span className="period">/{quote.billing_period}</span>
              </div>
              <div className="coverage">
                <p>Coverage: ${quote.coverage_limit.toLocaleString()}</p>
                <p>Deductible: ${quote.deductible.toLocaleString()}</p>
              </div>
            </div>
            <div className="quote-actions">
              <button className="btn-primary">Accept Quote</button>
              <button className="btn-secondary">View Details</button>
            </div>
          </div>
        ))}
      </div>

      {Object.keys(quotes).length === 0 && (
        <div className="no-quotes">
          <p>Waiting for broker quotes...</p>
        </div>
      )}
    </div>
  );
};
```

## Recommendations for VanguardAI Insurance Platform

### 1. Domain Model Strategy
- **Standardized Models**: Use industry-standard models (FIB-DM, ACORD) as foundation
- **Type Safety**: Implement comprehensive TypeScript interfaces for all insurance entities
- **Validation**: Use Pydantic for backend validation and Zod for frontend validation

### 2. Form Validation Approach
- **Shared Schemas**: Maintain single source of truth for validation rules
- **Business Rules**: Implement insurance-specific validation logic
- **Real-time Validation**: Provide immediate feedback for form errors

### 3. Document Management
- **Secure Upload**: Implement robust file upload with security validation
- **Type-specific Handling**: Different validation rules for different document types
- **Progress Tracking**: Real-time upload progress for large documents

### 4. Real-time Features
- **WebSocket Integration**: Use WebSockets for broker competition updates
- **Event-driven Architecture**: Implement event-based updates for all real-time features
- **State Management**: Use React Query for caching and state synchronization

## Implementation Timeline

**Phase 1 (Week 1-2):**
- Implement core insurance domain models
- Set up basic form validation with shared schemas
- Create document upload infrastructure

**Phase 2 (Week 3-4):**
- Implement broker competition WebSocket system
- Add real-time quote updates
- Enhance form validation with business rules

**Phase 3 (Week 5-6):**
- Optimize performance for large document uploads
- Add comprehensive error handling
- Implement advanced broker competition features

## Quality Metrics

**Success Criteria:**
- 100% type coverage for insurance domain models
- Sub-second form validation response times
- 99.9% document upload success rate
- Real-time updates with <100ms latency

**Monitoring:**
- Track form validation performance
- Monitor document upload success rates
- Measure WebSocket connection stability
- Collect user feedback on real-time features

## Conclusion

The insurance domain presents unique challenges that require specialized patterns for form validation, document management, and real-time updates. The combination of strong type safety, comprehensive validation, and real-time communication creates a robust foundation for the VanguardAI insurance platform.

The emphasis on industry-standard data models, secure document handling, and real-time broker competition workflows positions the platform to handle complex insurance business processes while maintaining excellent user experience and regulatory compliance.