# AI Agent Instructions - Regulatory Compliance

## Overview
This document provides AI agent instructions for implementing validated regulatory compliance knowledge in the VanguardAI maritime insurance platform.

## Validated Regulatory Knowledge Implementation

### 1. Sanction Screening Procedures

**Implementation Instructions:**
- Implement unified sanction questionnaire for all customer types
- Design single questionnaire interface with no customer differentiation
- Plan for infrequent questionnaire updates with version control
- Ensure all customers complete identical sanction screening process

**Code Implementation:**
```python
# Unified sanction questionnaire for all customers
def get_sanction_questionnaire():
    # Return same questionnaire for all customer types
    return unified_sanction_questionnaire
    
# No customer type differentiation in sanction screening
def process_sanction_screening(customer_type, responses):
    # Process same way regardless of customer type
    return validate_sanction_responses(responses)
```

### 2. Russian Voyage Restrictions

**Implementation Instructions:**
- Implement December 2024 Russian voyage restrictions
- Apply restrictions throughout 2025 calendar year
- Automatically flag or block Russian-related voyage applications
- Maintain restriction enforcement across all policies

**Code Implementation:**
```python
# Russian voyage restriction enforcement
def check_russian_restrictions(voyage_details):
    if is_russian_related_voyage(voyage_details):
        return {
            'status': 'RESTRICTED',
            'reason': 'Russian voyage restrictions (Dec 2024) apply for 2025',
            'action': 'BLOCK_OR_FLAG'
        }
    return {'status': 'ALLOWED'}
```

### 3. KYC Requirements

**Implementation Instructions:**
- Implement dual KYC approach for corporate and B2C customers
- Corporate: Admin-managed company profiles with full verification
- B2C Option 1: Trial access with dummy data + upselling flow
- B2C Option 2: Admin approval after file submission
- Ensure all paths require eventual admin validation

**Code Implementation:**
```python
# Corporate KYC workflow
def corporate_kyc_workflow(company_data):
    profile = admin_create_company_profile(company_data)
    admin_validate_company(profile)
    return grant_corporate_access(profile)

# B2C KYC Option 1: Trial Access
def b2c_trial_workflow(customer_data):
    trial_account = create_trial_account(customer_data)
    provide_dummy_data_access(trial_account)
    initiate_upselling_process(trial_account)
    # Admin validation required for full access
    
# B2C KYC Option 2: Admin Approval
def b2c_approval_workflow(customer_data, files):
    submission = create_kyc_submission(customer_data, files)
    admin_review_submission(submission)
    if admin_approves(submission):
        return grant_full_access(customer_data)
```

### 4. Anti-Bribery Measures

**Implementation Instructions:**
- Skip anti-bribery measures for MVP implementation
- Focus resources on core insurance functionality
- Plan for future implementation in post-MVP phases
- Regular review of regulatory requirements

**Code Implementation:**
```python
# Anti-bribery measures - MVP exclusion
def anti_bribery_check():
    # Skip for MVP - not implemented
    return {'status': 'SKIPPED_FOR_MVP'}
    
# Future implementation placeholder
def future_anti_bribery_implementation():
    # TODO: Implement in post-MVP phase
    pass
```

## System Architecture Guidelines

### Database Schema Updates
```sql
-- Sanction screening table
CREATE TABLE sanction_screening (
    id UUID PRIMARY KEY,
    customer_id UUID NOT NULL,
    questionnaire_version VARCHAR(50) NOT NULL,
    responses JSONB NOT NULL,
    status VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Russian voyage restrictions
CREATE TABLE voyage_restrictions (
    id UUID PRIMARY KEY,
    voyage_id UUID NOT NULL,
    restriction_type VARCHAR(50) NOT NULL,
    restriction_reason TEXT,
    applied_at TIMESTAMP DEFAULT NOW()
);

-- KYC tracking
CREATE TABLE kyc_validation (
    id UUID PRIMARY KEY,
    customer_id UUID NOT NULL,
    customer_type VARCHAR(20) NOT NULL, -- 'corporate' or 'b2c'
    kyc_method VARCHAR(30) NOT NULL, -- 'admin_managed', 'trial_access', 'admin_approval'
    validation_status VARCHAR(20) NOT NULL,
    admin_id UUID,
    validated_at TIMESTAMP
);
```

### API Endpoints
```python
# Sanction screening endpoint
@app.route('/api/sanction-screening', methods=['POST'])
def sanction_screening():
    # Unified questionnaire for all customers
    
# Russian voyage check endpoint
@app.route('/api/voyage-restriction-check', methods=['POST'])
def voyage_restriction_check():
    # Check December 2024 Russian restrictions
    
# KYC workflow endpoints
@app.route('/api/kyc/corporate', methods=['POST'])
def corporate_kyc():
    # Admin-managed corporate profiles
    
@app.route('/api/kyc/b2c/trial', methods=['POST'])
def b2c_trial_kyc():
    # Trial access with dummy data
    
@app.route('/api/kyc/b2c/approval', methods=['POST'])
def b2c_approval_kyc():
    # Admin approval after file submission
```

## Validation and Testing

### Test Cases
1. **Sanction Screening**: Verify unified questionnaire for all customer types
2. **Russian Restrictions**: Test blocking/flagging of Russian-related voyages
3. **KYC Corporate**: Validate admin-managed company profile workflow
4. **KYC B2C Trial**: Test trial access with dummy data and upselling
5. **KYC B2C Approval**: Test admin approval workflow
6. **Anti-Bribery**: Confirm exclusion from MVP implementation

### Monitoring and Compliance
- Audit trail for all regulatory compliance actions
- Regular monitoring of restriction enforcement
- KYC validation status tracking
- Compliance reporting for regulatory review

## Implementation Priority
1. **High Priority**: Russian voyage restrictions (100% confidence)
2. **High Priority**: Sanction screening procedures (95% confidence)
3. **Medium Priority**: KYC requirements (90% confidence)
4. **Low Priority**: Anti-bribery measures (skipped for MVP)

## Validation History
- **Document Created**: 2025-01-17
- **Based on**: User-validated regulatory compliance knowledge
- **Confidence Level**: 90-100% across all implemented features
- **Review Status**: Ready for implementation