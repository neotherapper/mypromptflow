# Validated KYC Requirements

## Overview
This document contains user-validated information about Know Your Customer (KYC) requirements for the VanguardAI maritime insurance platform.

## Dual KYC Approach

### Comprehensive KYC Framework
- **Validated Fact**: Dual KYC approach: Corporate customers require admin-managed company profiles; B2C customers have two options: 1) Temporary access with dummy data for app trial plus upselling, OR 2) Admin approval after file submission. Both require eventual admin validation.
- **Confidence Level**: 90%
- **Validated By**: User on 2025-01-17
- **Source**: User validation session
- **Validation Response**: C (Need different approach)

### Corporate Customer KYC
**Admin-Managed Company Profiles**
- Corporate customers require admin-created and validated company profiles
- Admin users create company profiles with full verification
- Admin validation required before corporate access granted
- Comprehensive company verification process

### B2C Customer KYC Options

#### Option 1: Trial Access with Upselling
- **Temporary Access**: Customers can access app with dummy data
- **App Trial**: Full app functionality with sample/dummy data
- **Upselling Process**: Convert trial users to full customers
- **Eventual Validation**: Admin validation required for full access

#### Option 2: Admin Approval Flow
- **File Submission**: B2C customers submit required documentation
- **Admin Review**: Admin users review and approve submissions
- **Approval Process**: Standard admin approval workflow
- **Access Granted**: Full access after admin approval

### Universal Requirements
- **Admin Validation**: Both corporate and B2C approaches require eventual admin validation
- **Compliance**: All customers must eventually meet full KYC requirements
- **Documentation**: Proper documentation required for all customer types
- **Audit Trail**: Complete audit trail for all KYC processes

### Implementation Architecture

#### Corporate Flow
1. Admin creates company profile
2. Admin validates company documentation
3. Corporate access granted after validation
4. Ongoing admin management of corporate profiles

#### B2C Flow - Option 1 (Trial)
1. Customer registers for trial access
2. App provides dummy data for trial
3. Upselling process initiated
4. Admin validation required for full access
5. Full access granted after validation

#### B2C Flow - Option 2 (Approval)
1. Customer submits required files
2. Admin reviews documentation
3. Admin approves or requests additional information
4. Full access granted after approval

### Business Logic Considerations
- **Flexibility**: Two B2C options provide customer choice
- **Conversion**: Trial option supports customer conversion
- **Compliance**: All paths lead to proper validation
- **Scalability**: Admin validation ensures quality control

### Technical Implementation
- **Role-Based Access**: Admin users manage validation processes
- **Workflow Management**: Separate workflows for corporate and B2C
- **Document Management**: Secure document storage and review
- **Status Tracking**: Customer status tracking through validation process

### Compliance Framework
- **Regulatory Compliance**: Meets maritime insurance KYC requirements
- **Admin Oversight**: Admin validation ensures compliance
- **Documentation Standards**: Proper documentation for all customer types
- **Audit Requirements**: Complete audit trail for regulatory review

## Validation History
- **Initial Validation**: 2025-01-17
- **Validation Type**: User confirmation requiring different approach
- **Original Source**: KYC documentation analysis
- **Confidence Improvement**: 80% → 90%
- **Validation Status**: Approved with different approach