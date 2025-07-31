# [MCP Server Name] Error Log

## Enhanced Error Log Format

### Error Entry Template
```markdown
## Error #[number] - [Date YYYY-MM-DD HH:MM]

### Context & Intent (Enhanced)
**User Task Goal:** [What the user was ultimately trying to accomplish]
**Immediate Objective:** [Specific step/action being attempted]
**User Request (Verbatim):** "[Exact user request if applicable]"
**Expected Outcome:** [What should have happened]
**Task Context:** [Multi-step workflow context, previous steps, dependencies]
**Workflow Stage:** [Beginning/Middle/End of task sequence]

### User & System Context
**User Expertise Level:** [Beginner/Intermediate/Advanced]
**Previous Similar Tasks:** [Success/Failure history with similar operations]
**System State:** [Any relevant system conditions, recent changes, etc.]
**Related Operations:** [Other MCP tools used in this session]
**Time Context:** [Time pressure, urgency, background/foreground task]

### Technical Details
**MCP Server:** [server name]
**Tool Used:** [specific tool name, e.g., mcp__MCP_DOCKER__jira_search]
**Parameters Used:**
```json
{
  "parameter1": "value1",
  "parameter2": "value2"
}
```
**Pre-flight Validation:** [Was validation run? Results?]
**Parameter Source:** [User input/Auto-generated/Template/Previous success]

### Error Information
**Error Message:** 
```
[Full error message/response]
```

**Error Type:** [Authentication, Parameter Validation, API Limit, Network, etc.]
**Severity:** [High/Medium/Low - based on user impact]
**Error Category:** [Format Error/Missing Data/Service Issue/Permission Problem]
**HTTP Status Code:** [If applicable]
**API Response Details:** [Headers, additional context from API]

### Enhanced Analysis
**Root Cause:** [What actually caused the error]
**Contributing Factors:** [System state, timing, dependencies that contributed]
**Missing Information:** [What parameter or context was missing]
**Parameter Issues:** [Specific parameter format problems]
**Authentication Status:** [Valid/Invalid/Expired/Wrong Scope]
**Service Availability:** [API status, rate limits, server health]
**User Action Analysis:** [Was this a reasonable thing to attempt?]

### Resolution Attempts & Learning
1. **Attempt 1:** [What I tried] → [Result] → [What I learned]
2. **Attempt 2:** [What I tried] → [Result] → [What I learned]
3. **Final Resolution:** [What worked, if anything] → [Why it worked]

### Lessons Learned & Patterns
**Immediate Lessons:**
- [ ] [Specific lesson 1 with actionable detail]
- [ ] [Specific lesson 2 with actionable detail]
- [ ] [Parameter format requirement with example]
- [ ] [Authentication requirement with verification steps]

**Pattern Recognition:**
- [ ] Similar error in [context/situation]? 
- [ ] Related to [time of day/system state/user type]?
- [ ] Part of larger workflow failure pattern?
- [ ] Correlation with other MCP server issues?

**Prevention Strategy:**
- [ ] **Pre-flight Check:** [Specific validation to add]
- [ ] **Parameter Validation:** [Format requirement to enforce]
- [ ] **Context Verification:** [Required context to ensure]
- [ ] **User Guidance:** [Warning or tip to provide]

### User Experience Impact
**Frustration Level:** [Low/Medium/High - user's experience]
**Task Blocking:** [Completely blocked/Workaround available/Minor delay]
**Learning Opportunity:** [What user learned vs. what they should learn]
**Follow-up Required:** [Does user need help with workaround/alternative?]

### System Learning Updates
**Usage Guide Updates Needed:** [Specific additions to prevention guides]
**Pattern File Updates:** [New patterns to add to validation]
**Template Improvements:** [Better examples or warnings to add]
**Pre-flight Rule Additions:** [New validation rules to implement]

### Frequency & Trend Tracking
**First Occurrence:** [Date]
**Frequency:** [How many times this error occurred]
**Last Occurrence:** [Date]
**Trend:** [Increasing/Decreasing/Stable/Seasonal]
**User Distribution:** [Single user/Multiple users/Specific user types]
**Status:** [Unresolved/Resolved/Pattern Identified/Prevention Implemented]

### Success Metrics
**Resolution Time:** [How long to fix]
**Repeat Prevention:** [Has this specific error repeated?]
**Pattern Effectiveness:** [How well did learning prevent similar errors?]
**User Satisfaction:** [User feedback on resolution/prevention]
```

## Error Categories

### Authentication Errors
- Missing credentials
- Invalid tokens
- Permission issues
- Configuration problems

### Parameter Errors
- Missing required parameters
- Invalid format
- Wrong data types
- Boundary violations

### API Errors
- Rate limiting
- Service unavailable
- Invalid endpoints
- API version issues

### Network Errors
- Connection timeouts
- DNS resolution
- Proxy issues
- SSL/TLS problems

## Usage Instructions

1. **When an MCP tool fails:** Immediately log the error using this template
2. **Fill all sections:** Complete information aids pattern recognition
3. **Update frequency:** Increase count if error repeats
4. **Cross-reference:** Link to usage guide updates
5. **Review periodically:** Look for patterns to prevent future errors

## Integration with Usage Guides

When errors are resolved, update the corresponding usage guide in:
`@meta/mcp-learning/usage-guides/[server-name]-guide.md`

Include:
- Parameter validation steps
- Pre-flight checklists
- Common pitfall warnings
- Working examples