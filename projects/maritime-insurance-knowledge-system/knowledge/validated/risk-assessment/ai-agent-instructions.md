# AI Agent Instructions - Validated Risk Assessment Knowledge

## Overview
This document provides specific instructions for AI agents using validated risk assessment knowledge in maritime insurance systems.

## Validated Knowledge Usage Rules

### MANDATORY: Use Only Validated Knowledge
- **Requirement**: AI agents MUST use only validated knowledge marked with ✅ status
- **Confidence Threshold**: Only use facts with confidence ≥90%
- **Source Verification**: Confirm knowledge is from user validation sessions
- **Update Tracking**: Check validation dates before using knowledge

### Validated Knowledge Inventory

#### 1. War Risk Calculations
**Knowledge ID**: `risk_assessment.war_risk_factors`
**Status**: ✅ Validated (95% confidence)
**Usage**: 
```
WHEN: Calculating war risk premiums
USE: Vessel tonnage factors as PRIMARY input
ENSURE: Tonnage data is accurate and current
IMPLEMENT: Tonnage-based risk multipliers in algorithms
```

#### 2. Port Risk Ratings
**Knowledge ID**: `risk_assessment.port_risk_ratings`
**Status**: ✅ Validated with Modifications (90% confidence)
**Usage**:
```
WHEN: Assessing port-specific risks
USE: Current port risk ratings
CRITICAL: Prompt user for monthly underwriter updates
WARNING: Display alert if port data >30 days old
IMPLEMENT: Monthly update reminder system
```

#### 3. Voyage Risk Models
**Knowledge ID**: `risk_assessment.voyage_risk_models`
**Status**: ✅ Validated with Modifications (90% confidence)
**Usage**:
```
WHEN: Calculating voyage risks
USE: Seasonal variation factors
CRITICAL: Require users to request updated rates
IMPLEMENT: Rate update prompts and tracking
COMBINE: Seasonal factors + current market rates
```

#### 4. Vessel Type Classifications
**Knowledge ID**: `risk_assessment.vessel_type_classifications`
**Status**: ✅ Validated (95% confidence)
**Usage**:
```
WHEN: Classifying vessels for risk assessment
USE: Current vessel type classifications confidently
IMPLEMENT: Classification-based risk profiles
RELY: System is current and accurate
```

## AI Agent Behavioral Requirements

### 1. Knowledge Validation Checks
Before using any risk assessment knowledge, AI agents MUST:
```
1. Verify knowledge has ✅ validated status
2. Check confidence level is ≥90%
3. Confirm validation date is current
4. Use exact validated fact language
```

### 2. User Interaction Requirements

#### Port Risk Ratings
```python
# Example AI agent behavior
if port_risk_age > 30_days:
    display_warning("Port risk data is over 30 days old")
    prompt_user("Please contact underwriters for updated port risk ratings")
    track_update_request()
```

#### Voyage Risk Models
```python
# Example AI agent behavior
if calculating_voyage_risk:
    apply_seasonal_factors()
    if not has_current_rates():
        prompt_user("Please request updated voyage rates from underwriters")
        wait_for_rate_update()
```

### 3. Error Handling
```python
# AI agent error handling
if knowledge_confidence < 90:
    return "Cannot use unvalidated knowledge"
    
if validation_date > 90_days_ago:
    warn_user("Knowledge may need revalidation")
    
if user_modification_required:
    follow_modification_instructions()
```

## Implementation Patterns

### 1. War Risk Calculation Pattern
```python
def calculate_war_risk(vessel_tonnage, destination_port):
    # VALIDATED: Tonnage is primary factor
    base_risk = vessel_tonnage * WAR_RISK_TONNAGE_MULTIPLIER
    
    # VALIDATED: Port risk affects war risk
    port_risk = get_current_port_risk(destination_port)
    if port_risk.age > 30_days:
        prompt_monthly_update()
    
    return base_risk * port_risk.multiplier
```

### 2. Risk Assessment Workflow Pattern
```python
def assess_maritime_risk(vessel, voyage):
    # Step 1: Vessel Classification (VALIDATED - 95% confidence)
    vessel_class = classify_vessel(vessel.type)
    
    # Step 2: Port Risk Check (VALIDATED - 90% confidence)
    port_risk = get_port_risk(voyage.destination)
    check_monthly_update_needed(port_risk)
    
    # Step 3: Seasonal Voyage Risk (VALIDATED - 90% confidence)
    seasonal_risk = calculate_seasonal_risk(voyage)
    prompt_rate_update_if_needed()
    
    # Step 4: War Risk (VALIDATED - 95% confidence)
    war_risk = calculate_war_risk(vessel.tonnage, voyage.destination)
    
    return combine_risk_factors(vessel_class, port_risk, seasonal_risk, war_risk)
```

### 3. Update Prompt Pattern
```python
def handle_dynamic_risk_data():
    # Port risk ratings - monthly updates required
    if port_data_age > 30_days:
        send_update_prompt("port_risk_ratings")
    
    # Voyage rates - regular updates required
    if voyage_rates_stale():
        send_update_prompt("voyage_rates")
    
    # Track update requests
    log_update_request(timestamp=now(), type="risk_data")
```

## Quality Assurance Rules

### 1. Confidence Level Requirements
- **High Priority Operations**: Use only 95% confidence knowledge
- **Standard Operations**: Use 90%+ confidence knowledge
- **Advisory Functions**: Use 85%+ confidence knowledge
- **Never Use**: Knowledge below 85% confidence

### 2. Validation Date Checks
```python
def validate_knowledge_currency(knowledge_item):
    if knowledge_item.validation_date < 90_days_ago:
        flag_for_revalidation()
    
    if knowledge_item.validation_date < 180_days_ago:
        disable_usage_until_revalidated()
```

### 3. Modification Compliance
For knowledge marked "Approved with Modifications":
- **MUST**: Implement all user-specified modifications
- **MUST**: Follow additional requirements (monthly updates, rate requests)
- **MUST**: Include modification logic in implementation
- **MUST**: Track compliance with modification requirements

## Compliance and Audit

### 1. Usage Tracking
AI agents MUST log:
- Which validated knowledge was used
- When it was used
- Confidence level at time of use
- Any user prompts generated
- Update requests made

### 2. Audit Trail Format
```yaml
knowledge_usage:
  timestamp: "2025-01-17T12:30:00Z"
  agent_id: "risk_assessment_agent"
  knowledge_id: "risk_assessment.war_risk_factors"
  confidence_level: 95
  validation_date: "2025-01-17"
  user_prompts_generated: []
  modifications_applied: true
```

### 3. Compliance Verification
```python
def verify_compliance():
    assert all_knowledge_used.confidence >= 90
    assert all_modifications_implemented()
    assert update_prompts_generated_when_required()
    assert audit_trail_complete()
```

## Emergency Procedures

### 1. Knowledge Invalidation
If validated knowledge becomes invalid:
1. Immediately stop using affected knowledge
2. Notify users of knowledge status change
3. Request emergency revalidation
4. Log invalidation event

### 2. System Fallback
If validated knowledge unavailable:
1. Notify user of limitation
2. Request manual override
3. Use only explicitly approved fallback procedures
4. Log fallback usage

## Performance Monitoring

### 1. Knowledge Effectiveness Metrics
- Usage frequency by knowledge item
- User satisfaction with prompts
- Update compliance rates
- Accuracy of risk assessments

### 2. System Performance Metrics
- Knowledge retrieval speed
- Validation check performance
- User prompt response rates
- Update tracking efficiency

## Last Updated
2025-01-17 by Risk Assessment Knowledge Builder agent

---

*These instructions are mandatory for all AI agents using validated risk assessment knowledge in maritime insurance systems.*