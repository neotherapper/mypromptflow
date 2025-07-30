# JIRA Error Log

## Server Information
**Server Name:** JIRA (via MCP Docker)
**Server Tools:** mcp__MCP_DOCKER__jira_* (search, get_issue, create_issue, update_issue, etc.)
**Primary Purpose:** JIRA issue management, project tracking, workflow automation
**Authentication:** JIRA API credentials (username/password or API token)
**Last Updated:** 2025-01-24
**Usage Guide:** @meta/mcp-learning/usage-guides/jira-guide.md

## Error Summary Statistics

**Total Errors Logged:** 0
**Most Common Error Type:** Not yet determined
**Average Resolution Time:** Not yet measured
**Success Rate Improvement:** Baseline being established

## Error Categories

### Authentication Errors (0 errors)
**Common Patterns Expected:**
- Invalid JIRA credentials or API tokens
- Insufficient permissions for project access
- Account lockouts or security restrictions
- OAuth token expiation

### Parameter Errors (0 errors)
**Common Patterns Expected:**
- Invalid issue keys or IDs
- Malformed JQL queries
- Missing required fields for issue creation
- Invalid field values for issue updates
- Project key format errors

### API Errors (0 errors)
**Common Patterns Expected:**
- Rate limiting from JIRA API
- Issue not found errors
- Field validation failures
- Transition permission errors
- Project access restrictions

### Network Errors (0 errors)
**Common Patterns Expected:**
- Connection timeouts to JIRA instance
- VPN or network access issues
- DNS resolution problems
- SSL certificate validation errors

## Error Log Entries

*No errors logged yet. This log will be populated automatically when JIRA tool errors occur.*

## Patterns and Insights

### Common Issues Identified
*To be populated as patterns emerge*

### Parameter Validation Rules
**Expected Requirements:**
- Issue Keys: Must follow PROJECT-NUMBER format (e.g., "SCRUM-123")
- JQL Queries: Must use valid JIRA Query Language syntax
- Project Keys: Must be valid project identifiers
- Field Values: Must match JIRA field type requirements
- User Identifiers: Must be valid usernames or account IDs

### Resolution Strategies
*To be developed based on successful resolutions*

## Known Working Patterns

### Successful Configurations
*To be documented as successful operations are observed*

### Reliable Parameter Sets
**Issue Search Examples:**
```json
{
  "jql": "project = SCRUM AND status = 'In Progress'",
  "fields": "summary,status,assignee,priority",
  "limit": 10
}
```

**Issue Creation Examples:**
```json
{
  "project_key": "SCRUM",
  "summary": "Issue title",
  "issue_type": "Task",
  "description": "Issue description"
}
```

## Prevention Checklist

Based on anticipated JIRA issues:

**Before using JIRA tools:**
- [ ] Verify JIRA credentials are valid and have required permissions
- [ ] Confirm project keys exist and are accessible
- [ ] Validate issue keys follow correct format (PROJECT-NUMBER)
- [ ] Check JQL query syntax before execution
- [ ] Ensure field values match JIRA field type requirements
- [ ] Verify user has permission for requested operations
- [ ] Check rate limit status if making multiple requests

## Integration Notes

**Parent System:** MCP Docker Server
**Related Error Logs:**
- @meta/mcp-learning/error-logs/mcp-docker-errors.md for container-level issues

**Cross-References:**
- Usage Guide: @meta/mcp-learning/usage-guides/jira-guide.md
- Common Patterns: @meta/mcp-learning/patterns/common-error-patterns.yaml
- Parameter Validation: @meta/mcp-learning/patterns/parameter-validation-patterns.yaml

## Maintenance

**Last Review:** 2025-01-24 (Initial creation)
**Next Review:** After first 5 errors logged
**Pattern Analysis:** To be performed bi-weekly once data is available
**Guide Updates:** To be synchronized with usage guide

---

*This error log follows the template at @meta/mcp-learning/templates/error-log-template.md*
*JIRA error entries will be added automatically as tool failures occur*
## Error #1 - 2025-07-30 10:07

### Context & Intent
**What I was trying to do:** MCP tool execution (auto-detected)
**User request:** Claude Code MCP tool operation
**Expected outcome:** Successful MCP tool execution

### Technical Details
**MCP Server:** jira
**Tool Used:** mcp__MCP_DOCKER__jira_get_issue
**Parameters Used:**
```json
{
  "note": "Parameters not captured by hook - requires manual investigation"
}
```

### Error Information
**Error Message:** 
```
Error: Invalid issue key INVALID-999999 not found
```

**Error Type:** Tool Error
**Severity:** Medium (Auto-detected)

### Analysis
**Root Cause:** Auto-detected via pattern matching in tool output
**Missing Information:** Full context and parameters require manual review
**Parameter Issues:** To be investigated through usage guides and patterns

### Resolution Attempts
1. **Automatic Detection:** Error detected and logged by hook → Success
2. **Manual Investigation Required:** Check jira-guide.md for troubleshooting
3. **Final Resolution:** To be updated after manual troubleshooting

### Lessons Learned
**For Future Use:**
- [ ] Review similar patterns in error logs
- [ ] Check usage guide for known solutions
- [ ] Update prevention strategies if pattern emerges

**Prevention:**
- [ ] Check `meta/mcp-learning/usage-guides/jira-guide.md` before using tool
- [ ] Apply known working patterns from previous successes
- [ ] Validate parameters against common error patterns

### Frequency Tracking
**First Occurrence:** 2025-07-30 10:07
**Frequency:** 1 time (auto-detected)
**Last Occurrence:** 2025-07-30 10:07
**Status:** Unresolved - Requires Manual Investigation


## Error #2 - 2025-07-30 10:07

### Context & Intent
**What I was trying to do:** MCP tool execution (auto-detected)
**User request:** Claude Code MCP tool operation
**Expected outcome:** Successful MCP tool execution

### Technical Details
**MCP Server:** jira
**Tool Used:** mcp__MCP_DOCKER__jira_get_issue
**Parameters Used:**
```json
{
  "note": "Parameters not captured by hook - requires manual investigation"
}
```

### Error Information
**Error Message:** 
```
No error - successful operation
```

**Error Type:** Tool Error
**Severity:** Medium (Auto-detected)

### Analysis
**Root Cause:** Auto-detected via pattern matching in tool output
**Missing Information:** Full context and parameters require manual review
**Parameter Issues:** To be investigated through usage guides and patterns

### Resolution Attempts
1. **Automatic Detection:** Error detected and logged by hook → Success
2. **Manual Investigation Required:** Check jira-guide.md for troubleshooting
3. **Final Resolution:** To be updated after manual troubleshooting

### Lessons Learned
**For Future Use:**
- [ ] Review similar patterns in error logs
- [ ] Check usage guide for known solutions
- [ ] Update prevention strategies if pattern emerges

**Prevention:**
- [ ] Check `meta/mcp-learning/usage-guides/jira-guide.md` before using tool
- [ ] Apply known working patterns from previous successes
- [ ] Validate parameters against common error patterns

### Frequency Tracking
**First Occurrence:** 2025-07-30 10:07
**Frequency:** 1 time (auto-detected)
**Last Occurrence:** 2025-07-30 10:07
**Status:** Unresolved - Requires Manual Investigation

