# Maritime Compliance Training for WorkOS Authentication

## Training Overview

This specialized training module focuses on maritime compliance requirements for WorkOS authentication implementation in the maritime insurance platform. It builds upon the existing comprehensive audit logging implementation to ensure full regulatory compliance.

**Duration**: 8 hours (2 days, 4 hours each)  
**Prerequisites**: WorkOS Setup Training, Authentication Implementation Training  
**Target Audience**: All team members with focus on compliance responsibilities  

## Learning Objectives

Upon completion, participants will be able to:

1. **Understand Maritime Compliance Requirements**: IMO, SOLAS, and maritime law compliance for authentication systems
2. **Implement Audit Logging**: Configure and maintain maritime-specific audit trails with WorkOS integration
3. **Manage Data Retention**: Execute 7-year data retention policies with automated archival
4. **Monitor Compliance**: Set up monitoring and alerting for compliance violations
5. **Handle Incidents**: Respond to authentication security incidents per maritime regulations

---

## Module 1: Maritime Regulatory Framework (2 hours)

### 1.1 Maritime Compliance Landscape

#### Key Regulations for Authentication Systems
- **IMO Guidelines**: International Maritime Organization security standards
- **SOLAS Requirements**: Safety of Life at Sea authentication protocols
- **Maritime Law**: Authentication data retention and access requirements
- **Insurance Regulations**: NAIC, FIO compliance for authentication events

#### Compliance Requirements Summary
```yaml
# Maritime Authentication Compliance Requirements
data_retention:
  authentication_logs: "3 years minimum"
  vessel_access_logs: "7 years minimum" 
  financial_transaction_logs: "10 years minimum"
  safety_incident_logs: "permanent retention"

audit_requirements:
  real_time_logging: "required"
  tamper_protection: "cryptographic integrity"
  geographic_tracking: "vessel location compliance"
  multi_tenant_isolation: "strict data separation"

regulatory_reporting:
  incident_notification: "24 hours maximum"
  audit_trail_access: "immediate availability"
  data_export: "standard format compliance"
  chain_of_custody: "full audit trail preservation"
```

### 1.2 WorkOS Compliance Features

#### Built-in Compliance Capabilities
- **SOC 2 Type II Certification**: Security and availability controls
- **GDPR Compliance**: Data privacy and user rights management
- **CCPA Compliance**: California consumer privacy requirements
- **NYDFS Compliance**: New York Department of Financial Services requirements

#### Maritime-Specific Enhancements Needed
- **Extended Retention**: Beyond WorkOS standard retention periods
- **Maritime Context**: Vessel ID, IMO numbers, geographic location tracking
- **Regulatory Reporting**: Custom reporting formats for maritime authorities
- **Incident Response**: Maritime-specific incident response procedures

---

## Module 2: Maritime Audit Logging Implementation (3 hours)

### 2.1 Dual-Layer Audit Architecture

#### Architecture Overview
```
WorkOS Built-in Logs → Maritime Audit Middleware → Compliance Database
                   ↓                              ↓
            Authentication Events         Business Operations
            - Login/Logout                - Vessel Access
            - SSO Events                  - Quote Creation
            - MFA Challenges              - Claim Processing
            - Organization Changes        - Policy Management
```

#### Implementation Review
Based on the existing `maritime-audit-logging-implementation-guide.md`, the system implements:

1. **WorkOS Webhook Integration**: Captures all authentication events
2. **FastAPI Middleware**: Captures business operations with maritime context
3. **PostgreSQL Storage**: Partitioned tables with 7+ year retention
4. **SIEM Integration**: Real-time streaming to DataDog/Elasticsearch

### 2.2 Maritime Context Extraction

#### Required Maritime Metadata
```python
# Maritime audit event context
maritime_context = {
    "vessel_id": "IMO1234567",
    "vessel_imo": "1234567", 
    "geographic_location": {
        "latitude": 40.7128,
        "longitude": -74.0060,
        "port": "New York",
        "territorial_waters": "US"
    },
    "financial_amount": 500000.00,
    "insurance_policy": "POL-2024-001",
    "tenant_classification": "ship_owner"
}
```

#### Context Extraction Implementation
```python
async def extract_maritime_context(request: Request) -> Dict[str, Any]:
    """Extract maritime compliance context from API requests"""
    context = {}
    
    # Extract vessel information from request
    if "vessel_id" in request.path_params:
        vessel_id = request.path_params["vessel_id"]
        context["vessel_id"] = vessel_id
        context["vessel_imo"] = await get_vessel_imo(vessel_id)
    
    # Extract geographic context
    if "location" in request.query_params:
        location_data = await resolve_location(request.query_params["location"])
        context["geographic_location"] = location_data
    
    # Extract financial context
    if request.method in ["POST", "PUT", "PATCH"]:
        body = await get_request_body(request)
        if "amount" in body:
            context["financial_amount"] = float(body["amount"])
    
    return context
```

### 2.3 Compliance-Specific Event Processing

#### Event Classification for Maritime Compliance
```python
def determine_compliance_requirements(event_data: Dict) -> Dict[str, str]:
    """Determine compliance requirements based on event context"""
    
    # Base maritime compliance
    compliance = {
        "regulation_type": "maritime_general",
        "retention_period": "7_years",
        "data_classification": "internal"
    }
    
    # Financial transaction compliance
    if event_data.get("financial_amount", 0) > 0:
        compliance.update({
            "regulation_type": "financial_maritime",
            "retention_period": "10_years",
            "data_classification": "confidential"
        })
    
    # Safety-related compliance
    if "safety" in event_data.get("event_type", "").lower():
        compliance.update({
            "regulation_type": "maritime_safety",
            "retention_period": "permanent",
            "data_classification": "restricted"
        })
    
    # International waters compliance
    location = event_data.get("geographic_location", {})
    if location.get("territorial_waters") == "international":
        compliance.update({
            "regulation_type": "international_maritime",
            "retention_period": "15_years"
        })
    
    return compliance
```

---

## Module 3: Data Retention and Archival (2 hours)

### 3.1 Maritime Data Retention Requirements

#### Retention Policy Matrix
| Event Type | Regulation | Retention Period | Storage Tier |
|------------|------------|------------------|--------------|
| Authentication Events | IMO Security | 3 years | Active Database |
| Vessel Access Logs | SOLAS | 7 years | Active → Cold |
| Financial Transactions | Maritime Insurance | 10 years | Active → Cold → Archive |
| Safety Incidents | International Law | Permanent | All Tiers |
| Environmental Events | MARPOL | Permanent | All Tiers |

### 3.2 Automated Retention Management

#### Implementation Using Existing System
The project already includes a comprehensive retention management system:

```python
# From maritime-audit-logging-implementation-guide.md
class MaritimeRetentionManager:
    def __init__(self, db_session, cold_storage_bucket):
        self.retention_policies = {
            "authentication": timedelta(days=1095),     # 3 years
            "vessel_access": timedelta(days=2555),      # 7 years  
            "financial_transactions": timedelta(days=3650), # 10 years
            "safety_incidents": None,                   # Permanent
            "environmental_compliance": None            # Permanent
        }
```

#### Cold Storage Archival Process
1. **Automated Daily Scanning**: Identify records exceeding retention thresholds
2. **Maritime Context Preservation**: Maintain maritime metadata in archive format
3. **Compressed Storage**: GZIP compression with maritime-specific indexing
4. **Retrieval Procedures**: On-demand retrieval for regulatory audits

### 3.3 Compliance Reporting

#### Maritime Audit Report Generation
```python
async def generate_maritime_compliance_report(
    start_date: datetime,
    end_date: datetime,
    vessel_ids: List[str] = None
) -> Dict[str, Any]:
    """Generate comprehensive maritime compliance report"""
    
    report = {
        "report_metadata": {
            "period": f"{start_date} to {end_date}",
            "report_type": "maritime_compliance",
            "regulatory_framework": ["IMO", "SOLAS", "MARPOL"]
        },
        
        "authentication_compliance": {
            "total_auth_events": await count_auth_events(start_date, end_date),
            "failed_auth_attempts": await count_failed_auth(start_date, end_date),
            "compliance_score": await calculate_auth_compliance_score()
        },
        
        "vessel_access_compliance": {
            "vessels_accessed": await get_unique_vessels_accessed(start_date, end_date),
            "unauthorized_access_attempts": await count_unauthorized_access(),
            "geographic_compliance": await validate_territorial_compliance()
        },
        
        "financial_compliance": {
            "total_financial_events": await count_financial_events(),
            "high_value_transactions": await count_high_value_transactions(),
            "regulatory_notifications": await get_required_notifications()
        }
    }
    
    return report
```

---

## Module 4: Monitoring and Incident Response (1 hour)

### 4.1 Compliance Monitoring Setup

#### Key Compliance Metrics
```yaml
# Maritime compliance monitoring metrics
authentication_metrics:
  - failed_login_rate_per_vessel
  - geographic_authentication_anomalies  
  - multi_tenant_access_violations
  - token_expiration_compliance

vessel_access_metrics:
  - unauthorized_vessel_access_attempts
  - cross_tenant_data_access_violations
  - geographic_boundary_violations
  - imo_compliance_validation_failures

financial_metrics:
  - high_value_transaction_authentication
  - financial_data_access_without_authorization
  - currency_transaction_reporting_triggers
  - insurance_policy_access_compliance
```

#### Automated Compliance Alerts
```python
# Compliance alert configuration
COMPLIANCE_ALERTS = {
    "critical": {
        "unauthorized_vessel_access": {
            "threshold": 1,
            "notification": "immediate",
            "escalation": "maritime_security_officer"
        },
        "financial_data_breach": {
            "threshold": 1, 
            "notification": "immediate",
            "escalation": "compliance_officer"
        }
    },
    
    "warning": {
        "authentication_failure_rate": {
            "threshold": "5% per hour",
            "notification": "15_minutes",
            "escalation": "technical_lead"
        },
        "retention_policy_violations": {
            "threshold": 10,
            "notification": "daily",
            "escalation": "data_governance"
        }
    }
}
```

### 4.2 Maritime Incident Response

#### Incident Classification for Maritime Context
1. **Security Incidents**: Unauthorized access to vessel data or financial information
2. **Compliance Violations**: Data retention failures or audit trail corruption
3. **Geographic Violations**: Access from restricted territorial waters
4. **Financial Incidents**: Unauthorized access to high-value transactions

#### Response Procedures
```python
class MaritimeIncidentResponse:
    async def handle_security_incident(self, incident_data: Dict):
        """Handle maritime security incidents"""
        
        # Step 1: Immediate containment
        if incident_data["severity"] == "critical":
            await self.disable_affected_accounts()
            await self.notify_maritime_authorities()
        
        # Step 2: Evidence preservation
        await self.preserve_audit_evidence(incident_data)
        await self.export_compliance_logs(incident_data["time_range"])
        
        # Step 3: Regulatory notification
        if self.requires_regulatory_notification(incident_data):
            await self.notify_regulatory_bodies(incident_data)
        
        # Step 4: Maritime-specific actions
        if incident_data.get("vessel_impact"):
            await self.notify_vessel_operators(incident_data["vessel_ids"])
            await self.update_vessel_access_policies()
```

---

## Hands-On Lab Exercises

### Lab 1: Maritime Audit Event Analysis (1 hour)

**Objective**: Analyze real maritime audit events and classify compliance requirements

**Exercise**: 
1. Review sample audit events from the maritime platform
2. Identify maritime context (vessel, location, financial impact)
3. Determine appropriate retention periods and compliance requirements
4. Generate compliance reports for maritime authorities

**Validation Criteria**:
- Correct event classification (100% accuracy required)
- Proper retention period assignment
- Complete maritime context extraction
- Regulatory report generation

### Lab 2: Compliance Monitoring Setup (1 hour)

**Objective**: Configure maritime-specific compliance monitoring and alerting

**Exercise**:
1. Set up Prometheus metrics for maritime compliance events
2. Configure Grafana dashboards for compliance monitoring
3. Test incident response procedures with simulated events
4. Validate automated reporting functionality

**Validation Criteria**:
- All compliance metrics properly configured
- Alert thresholds set according to maritime regulations
- Incident response procedures tested and validated
- Reports generated in maritime authority format

---

## Assessment and Certification

### Individual Competency Requirements

#### For All Team Members:
- [ ] Understanding of maritime regulatory framework
- [ ] Ability to identify compliance events in audit logs
- [ ] Knowledge of data retention requirements by event type
- [ ] Basic incident response procedures

#### For Technical Roles (Backend/Frontend Leads):
- [ ] Implementation of maritime context extraction
- [ ] Configuration of compliance-specific audit logging
- [ ] Integration with retention management system
- [ ] Performance optimization for compliance queries

#### For Head of Engineering:
- [ ] Maritime compliance strategy and risk assessment
- [ ] Regulatory relationship management
- [ ] Compliance audit coordination
- [ ] Team training and certification oversight

### Certification Requirements

**Written Assessment**: 85% minimum score on maritime compliance principles  
**Practical Demonstration**: Successful implementation of compliance monitoring  
**Incident Simulation**: Proper response to simulated maritime security incident  
**Audit Review**: Successfully assist with mock regulatory audit  

---

## Resources and References

### Maritime Regulatory Resources
- **IMO Security Guidelines**: MSC.1/Circ.1111 - Maritime Security Best Practices
- **SOLAS Chapter XI-2**: Security provisions for ships and port facilities
- **ISPS Code**: International Ship and Port Facility Security Code
- **MARPOL Convention**: Pollution prevention authentication requirements

### Technical Documentation
- **Implementation Guide**: `docs/maritime-audit-logging-implementation-guide.md`
- **WorkOS Documentation**: https://workos.com/docs/audit-logs
- **Compliance Framework**: Project authentication compliance requirements

### Emergency Contacts
- **Maritime Security Officer**: [Contact Information]
- **Compliance Officer**: [Contact Information] 
- **Technical Support**: Internal escalation procedures
- **Regulatory Bodies**: IMO, Coast Guard, relevant maritime authorities

### Continuous Learning
- **Quarterly Compliance Updates**: Maritime regulation changes
- **Annual Certification Renewal**: Updated training requirements
- **Industry Conference Participation**: Maritime security and compliance forums
- **Regulatory Newsletter Subscription**: Updates from maritime authorities

---

**Training Completion**: This completes the maritime compliance training for WorkOS authentication implementation. Team members should maintain awareness of regulatory changes and participate in ongoing compliance education programs.

**Next Steps**: Upon successful completion, proceed to implementation phase with regular compliance reviews and audit preparation procedures.