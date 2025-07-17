# Quote Generation Workflows - Maritime Insurance Knowledge System

## Document Information

**Title**: Quote Generation Workflows  
**Category**: Operational Processes - Quote Generation  
**Source**: OneDrive File Analysis - Premium Examples & Screenshots  
**Analysis Date**: 2025-01-17  
**Confidence Score**: 90%  
**Status**: Awaiting Validation  

## Executive Summary

This document details the quote generation workflows extracted from the maritime insurance knowledge system analysis. The workflows include multi-step quote creation processes, premium calculation methodologies, coverage selection options, and quote approval procedures for B2C maritime insurance customers.

## Quote Generation Workflow Components

### 1. Multi-Step Quote Creation Process

**Customer-Facing Interface Components**:
- Quote request initiation by customer
- Vessel information collection and validation
- Coverage type selection (war risk, voyage-based, port-specific)
- Route and destination specification
- Quote preview and customer review

**Internal PMSC Interface Components**:
- Quote management dashboard for internal agents
- Risk assessment review and adjustment capabilities
- Premium calculation validation and modification
- Quote approval and finalization workflows
- Customer communication and quote delivery

**Workflow Sequence** (Based on Screenshot Analysis):
1. Customer initiates quote request through customer interface
2. System collects vessel data and voyage information
3. Customer selects coverage options and requirements
4. System performs initial risk assessment and premium calculation
5. Quote transferred to PMSC interface for internal review
6. Internal agent reviews and approves/modifies quote
7. Final quote delivered to customer for acceptance

### 2. Premium Calculation Methodologies

**Base Premium Calculation Structure**:
```
Total Premium = Base Premium + Risk Multipliers + Vessel Factors + Adjustments - Discounts
```

**Risk Multipliers Applied**:
- **Port-specific risk ratings**: Different multipliers for origin and destination ports
- **Vessel-type classifications**: Risk profiles based on vessel type and size
- **Voyage-based factors**: Route risk, duration, seasonal adjustments
- **War risk factors**: Elevated risk regions and conflict zones

**Vessel Factors Considered**:
- **Tonnage factors**: Primary component in war risk calculations
- **Vessel age and condition**: Impact on risk assessment
- **Vessel classification**: Maritime classification society ratings
- **Operational history**: Previous claims and incident history

**Discount Structures Available**:
- **Volume discounts**: Based on fleet size or policy volume
- **Loyalty discounts**: For repeat customers (e.g., 32.5% in OLYMPIC FIGHTER example)
- **Negotiated rates**: Customer-specific pricing agreements
- **Seasonal discounts**: Time-based pricing adjustments

### 3. Coverage Selection Options

**War Risk Coverage**:
- Vessel war risk protection for conflict zones
- Cargo war risk coverage for high-risk shipments
- Port war risk assessments for specific destinations
- Crew war risk coverage for personnel protection

**Voyage-Based Coverage**:
- Single voyage insurance policies
- Multi-voyage coverage for regular routes
- Seasonal coverage for specific time periods
- Route-specific insurance for established shipping lanes

**Port-Specific Coverage**:
- Port entry and exit coverage
- Cargo handling insurance at specific ports
- Port security incident coverage
- Detention and delay coverage for port issues

### 4. Quote Approval Workflows

**Automatic Approval Criteria**:
- Standard risk profiles within acceptable parameters
- Vessel types with established risk classifications
- Routes with standard risk assessments
- Premium calculations within normal ranges

**Manual Review Required**:
- High-risk vessel classifications
- Unusual route or destination requests
- Premium calculations outside normal parameters
- New customer applications requiring enhanced due diligence

**PMSC Agent Review Process**:
- Risk assessment validation against current market conditions
- Premium calculation verification using internal systems
- Compliance screening for sanctions and regulatory requirements
- Customer creditworthiness and payment history review

## Detailed Premium Calculation Examples

### Example 1: OLYMPIC FIGHTER Quote - GOA Route

**Base Calculation Components**:
- Base premium: [Amount to be validated]
- Port risk multiplier (GOA): [Factor to be validated]
- Vessel tonnage factor: [Calculation to be validated]
- War risk adjustment: [Percentage to be validated]
- Loyalty discount applied: 32.5%

**Final Premium Structure**: Base calculation with significant loyalty discount

### Example 2: AQUA LADY - Yuzhny Route (May 2025)

**Voyage-Specific Factors**:
- Seasonal adjustment for May voyage timing
- Yuzhny port risk assessment
- Future voyage pricing (forward-dated coverage)
- Vessel-specific risk profile

### Example 3: CMA CGM CHANCE - Commercial Vessel

**Commercial Vessel Considerations**:
- Commercial vessel type classification
- Higher tonnage factor application
- Route-specific risk assessment
- Corporate customer discount structure

## B2C Platform Considerations

### Customer Self-Service Capabilities

**Quote Initiation**:
- Customer can initiate quote requests independently
- Guided vessel information collection process
- Coverage selection assistance and recommendations
- Real-time premium estimation during quote process

**Quote Management**:
- Customer access to quote history and status
- Ability to modify quote parameters before approval
- Quote comparison tools for different coverage options
- Save and resume quote functionality

### Agent-Assisted Components

**Complex Quote Requirements**:
- Unusual vessel types or routes requiring agent assistance
- High-value vessel coverage requiring additional review
- Multi-vessel fleet quote coordination
- Custom coverage requirements beyond standard options

**Quote Approval Process**:
- Internal agent review for risk assessment validation
- Premium calculation verification and adjustment
- Compliance screening completion
- Final quote approval and delivery to customer

## Vessel Data Collection Requirements

### Essential Vessel Information

**Basic Vessel Details**:
- Vessel name and IMO number
- Vessel type and classification
- Gross tonnage and dimensions
- Year built and current condition
- Flag state and port of registry

**Operational Information**:
- Intended route and destination ports
- Cargo type and value (if applicable)
- Voyage duration and timing
- Crew size and experience level
- Previous insurance history

**Risk Assessment Data**:
- Classification society certification
- Safety and security equipment installed
- Maintenance and inspection records
- Previous claims and incident history
- Current market value and replacement cost

### Data Collection Process

**Customer Input Methods**:
- Online form completion with validation
- Document upload for verification
- Integration with maritime databases for pre-population
- Real-time data validation and error checking

**Verification Procedures**:
- Cross-reference with maritime registration databases
- Validation against classification society records
- Verification of vessel ownership and authority
- Compliance screening for sanctions and restrictions

## Technology Integration Points

### System Dependencies

**Risk Assessment Systems**:
- Integration with risk calculation engines
- Real-time access to port risk databases
- Connection to vessel classification systems
- Link to sanctions screening databases

**Premium Calculation Systems**:
- Automated calculation engine with current rates
- Integration with discount and adjustment systems
- Real-time currency conversion capabilities
- Connection to competitive pricing databases

**Customer Management Systems**:
- Integration with customer profile and history systems
- Connection to payment processing systems
- Link to policy administration systems
- Integration with customer communication systems

## Critical Validation Requirements

### High Priority Validation Items

1. **Multi-Step Process Currency**: Are the customer view and PMSC view interfaces still current and accurate?
2. **Premium Calculation Accuracy**: Are the calculation methodologies (base premium + risk multipliers + vessel factors + discounts) still accurate for B2C customers?
3. **Coverage Selection Options**: How do B2C customers select coverage options during quote generation, and are the interfaces shown still accurate?
4. **Vessel Data Requirements**: What specific vessel data is required during quote generation for B2C customers?

### Medium Priority Validation Items

1. **Quote Approval Workflows**: What are the current quote review and approval workflows for B2C customers?
2. **Discount Structure Applicability**: Are the discount structures shown in premium examples still applicable to B2C pricing?
3. **PMSC Interface Usage**: Do internal agents still use PMSC interfaces for quote management?

## Potential Issues and Conflicts

### B2C vs B2B Process Alignment

**Potential Conflicts**:
- Some quote approval processes may be designed for B2B rather than B2C customers
- Complex vessel data requirements may be excessive for individual customers
- Internal review processes may slow down B2C self-service expectations

**Resolution Required**:
- Validation of B2C-specific quote generation workflows
- Confirmation of simplified vessel data requirements for individual customers
- Clarification of self-service vs. agent-assisted quote processes

### Premium Calculation Complexity

**Complexity Considerations**:
- Multiple discount structures may be confusing for B2C customers
- Complex risk multipliers may not be transparent to individual customers
- Premium calculation variations may affect customer trust and understanding

**Validation Needed**:
- Confirm current premium calculation transparency for B2C customers
- Validate discount structure applicability to individual customers
- Ensure pricing consistency across different quote scenarios

## Next Steps

1. **User Validation**: Present detailed validation questions to users for approval
2. **Process Documentation Updates**: Update workflow documentation based on validation results
3. **Technology Integration Planning**: Plan integration of validated workflows into knowledge base
4. **B2C Optimization**: Identify opportunities to optimize quote generation for B2C customers

---

**Document Status**: Draft - Awaiting User Validation  
**Next Review Date**: Upon completion of validation questions  
**Responsible Party**: Quote Generation Expert Agent  
**Approval Required**: User validation of quote generation workflow knowledge