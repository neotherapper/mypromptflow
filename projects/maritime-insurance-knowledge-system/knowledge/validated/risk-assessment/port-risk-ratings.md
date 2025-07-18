# Port Risk Ratings - Validated Knowledge

## Overview
This document contains user-validated knowledge about port risk ratings in maritime insurance.

## Validated Facts

### Dynamic Port Risk Ratings

**Fact**: Port risk ratings are current but dynamic, changing based on circumstances like war; users must ask underwriters monthly for updated risk ratings

**Validation Details**:
- **Validated by**: User
- **Validation date**: 2025-01-17
- **Confidence level**: 90%
- **User response**: B (Approved with modifications)
- **Source**: User validation session

**Original Knowledge**: "Port risk ratings are current"
**Modified Knowledge**: Added requirement for monthly underwriter updates due to dynamic nature

**Business Logic**:
- Port risk ratings are accurate for current conditions
- Risk ratings change based on geopolitical circumstances (war, political instability)
- Users must actively request updated ratings from underwriters
- Monthly updates recommended for accurate risk assessment
- Risk ratings are not static and require regular refreshing

**Implementation Requirements**:
- System should prompt users to request updated port risk ratings monthly
- Display warning when port risk data is over 30 days old
- Integrate with underwriter communication workflows
- Track last update date for each port's risk rating
- Consider implementing alerts for high-risk port status changes

**Operational Workflow**:
1. User accesses port risk rating for voyage planning
2. System checks last update date
3. If over 30 days old, prompt user to contact underwriters
4. User requests updated ratings from underwriters
5. System updates with new ratings and timestamp
6. New ratings used for risk calculations

**Related Knowledge**:
- Connects to voyage risk models for comprehensive assessment
- Links to war risk calculations for conflict zone ports
- Integrates with vessel type classifications for complete risk profiling

## Quality Assurance

**Validation Process**:
1. Original knowledge indicated static port risk ratings
2. User provided critical modification about dynamic nature
3. User approved with modifications emphasizing monthly updates
4. Knowledge updated to reflect business reality

**Compliance Notes**:
- Reflects real-world maritime insurance practices
- Accounts for rapidly changing geopolitical conditions
- Ensures users maintain current risk assessment data
- Approved for AI agent usage with modification requirements

## Last Updated
2025-01-17 by Risk Assessment Knowledge Builder agent