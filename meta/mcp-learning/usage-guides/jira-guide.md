# JIRA Usage Guide

## Server Overview
**Server Name:** JIRA (via MCP Docker)
**Primary Purpose:** JIRA issue management, project tracking, workflow automation, and team collaboration
**Authentication Type:** JIRA API credentials (username/password or API token)
**Last Updated:** 2025-01-24
**Error Log:** @meta/mcp-learning/error-logs/jira-errors.md

## Pre-Flight Checklist

Before using any JIRA tools, verify:

- [ ] **Authentication:** Valid JIRA credentials with required permissions
- [ ] **Project Access:** User has access to target projects and issue types
- [ ] **Issue Key Format:** Using correct PROJECT-NUMBER format (e.g., "SCRUM-123")
- [ ] **JQL Syntax:** Query language syntax is valid for search operations
- [ ] **Field Names:** Field names match JIRA instance configuration
- [ ] **Rate Limits:** Not exceeding API usage quotas

## Common Use Cases

### Use Case 1: Issue Search with JQL
**Purpose:** Find issues matching specific criteria using JIRA Query Language
**Tools:** mcp__MCP_DOCKER__jira_search
**Success Pattern:** Use valid JQL syntax with proper field names and operators

**Working Example:**
```
Tool: mcp__MCP_DOCKER__jira_search
Parameters:
{
  "jql": "project = SCRUM AND status = 'In Progress' AND assignee = currentUser()",
  "fields": "summary,status,assignee,priority,created",
  "limit": 20,
  "start_at": 0
}
Expected Result: Issues array with pagination info and requested fields
```

### Use Case 2: Issue Retrieval
**Purpose:** Get detailed information about a specific issue
**Tools:** mcp__MCP_DOCKER__jira_get_issue
**Success Pattern:** Use exact issue key format and specify needed fields

**Working Example:**
```
Tool: mcp__MCP_DOCKER__jira_get_issue
Parameters:
{
  "issue_key": "SCRUM-123",
  "fields": "summary,description,status,assignee,priority,labels,created,updated",
  "expand": "renderedFields,transitions"
}
Expected Result: Complete issue object with requested fields and metadata
```

### Use Case 3: Issue Creation
**Purpose:** Create new issues in JIRA projects
**Tools:** mcp__MCP_DOCKER__jira_create_issue
**Success Pattern:** Include all required fields and use valid project key

**Working Example:**
```
Tool: mcp__MCP_DOCKER__jira_create_issue
Parameters:
{
  "project_key": "SCRUM",
  "summary": "Fix login validation bug",
  "issue_type": "Bug",
  "description": "User authentication fails when password contains special characters",
  "assignee": "john.doe@company.com",
  "priority": {"name": "High"}
}
Expected Result: Created issue object with generated issue key
```

### Use Case 4: Issue Updates
**Purpose:** Modify existing issue fields and properties
**Tools:** mcp__MCP_DOCKER__jira_update_issue
**Success Pattern:** Use valid field names and appropriate value formats

**Working Example:**
```
Tool: mcp__MCP_DOCKER__jira_update_issue
Parameters:
{
  "issue_key": "SCRUM-123",
  "fields": {
    "summary": "Updated issue summary",
    "assignee": {"name": "jane.smith"},
    "priority": {"name": "Medium"},
    "labels": ["frontend", "critical"]
  }
}
Expected Result: Success confirmation with updated issue details
```

## Parameter Reference

### Essential Parameters
| Parameter | Type | Format | Example | Notes |
|-----------|------|---------|---------|--------|
| issue_key | string | PROJECT-NUMBER | "SCRUM-123" | Case sensitive, exact format |
| project_key | string | UPPERCASE | "SCRUM" | Project identifier |
| jql | string | JQL syntax | "project = SCRUM AND status = 'Open'" | JIRA Query Language |
| fields | string | Comma-separated | "summary,status,assignee" | Specific fields to return |
| limit | integer | 1-50 | 20 | Max results per request |

### Common Field Names
| Field | Type | Example Value | Notes |
|-------|------|---------------|--------|
| summary | string | "Issue title" | Required for creation |
| description | string | "Detailed description" | Markdown supported |
| status | object | {"name": "In Progress"} | Must be valid status |
| assignee | object | {"name": "username"} | Must be valid user |
| priority | object | {"name": "High"} | Must be valid priority |
| labels | array | ["frontend", "bug"] | String array |
| issue_type | string | "Bug" | Must be valid type |

### JQL Operators and Functions
| Operator | Usage | Example |
|----------|-------|---------|
| = | Equals | `status = "Open"` |
| != | Not equals | `priority != "Low"` |
| IN | In list | `status IN ("Open", "In Progress")` |
| AND | Logical and | `project = SCRUM AND status = "Open"` |
| OR | Logical or | `priority = "High" OR priority = "Critical"` |
| currentUser() | Current user | `assignee = currentUser()` |
| now() | Current time | `created >= -7d` |

## Known Working Patterns

### Pattern 1: Complex Issue Search
**When to use:** Finding issues with multiple criteria and sorting
**Steps:**
1. Construct JQL with proper syntax and field names
2. Specify fields to reduce response size
3. Use pagination for large result sets
4. Include sorting for consistent results

**Example:**
```json
{
  "jql": "project = SCRUM AND status IN ('Open', 'In Progress') AND priority IN ('High', 'Critical') AND assignee = currentUser() ORDER BY created DESC",
  "fields": "summary,status,assignee,priority,created,labels",
  "limit": 25,
  "start_at": 0
}
```

### Pattern 2: Issue Creation with Complete Data
**When to use:** Creating well-defined issues with all necessary information
**Steps:**
1. Verify project key exists and user has create permissions
2. Include all required fields for the issue type
3. Use valid values for select fields (priority, status, etc.)
4. Provide clear summary and description

**Example:**
```json
{
  "project_key": "SCRUM",
  "summary": "Implement user profile editing feature",
  "issue_type": "Story",
  "description": "As a user, I want to edit my profile information so that I can keep my details up to date.",
  "assignee": "developer@company.com",
  "priority": {"name": "Medium"},
  "labels": ["frontend", "user-management"],
  "components": ["Web App"],
  "additional_fields": {
    "customfield_10001": "Epic-123"
  }
}
```

### Pattern 3: Issue Status Transition
**When to use:** Moving issues through workflow states
**Steps:**
1. Get available transitions for the issue
2. Identify correct transition ID
3. Include any required fields for the transition
4. Execute transition with proper parameters

**Example:**
```
1. Get transitions: jira_get_transitions({"issue_key": "SCRUM-123"})
2. Identify transition: "Start Progress" (ID: "21")
3. Execute transition:
{
  "issue_key": "SCRUM-123",
  "transition_id": "21",
  "fields": {
    "assignee": {"name": "current-user"}
  },
  "comment": "Starting work on this issue"
}
```

## Common Pitfalls & How to Avoid Them

### Pitfall 1: Invalid Issue Key Format
**Error:** "Issue does not exist" or "Invalid issue key"
**Symptom:** 404 Not Found or 400 Bad Request
**Cause:** Incorrect issue key format or non-existent issue
**Prevention:** Always use PROJECT-NUMBER format (e.g., "SCRUM-123")
**Fix:** Verify issue exists and use exact case-sensitive key

### Pitfall 2: JQL Syntax Errors
**Error:** "JQL syntax error" or "Invalid JQL query"
**Symptom:** 400 Bad Request with query parsing error
**Cause:** Typos, invalid operators, or incorrect field names
**Prevention:** Test JQL queries in JIRA web interface first
**Fix:** Use proper syntax: `field = "value"` with quotes around values

### Pitfall 3: Field Name Mismatches
**Error:** "Field does not exist" or "Invalid field"
**Symptom:** Field-related validation errors
**Cause:** Field names don't match JIRA configuration
**Prevention:** Use jira_search_fields to find correct field names
**Fix:** Use exact field names from JIRA schema (case-sensitive)

### Pitfall 4: Permission and Access Issues
**Error:** "Forbidden" or "You do not have permission"
**Symptom:** 403 Forbidden status code
**Cause:** User lacks required permissions for project or operation
**Prevention:** Verify user permissions in JIRA before operations
**Fix:** Request additional permissions or use different credentials

### Pitfall 5: Invalid Field Values
**Error:** "Invalid value for field" or validation errors
**Symptom:** 400 Bad Request with specific field validation error
**Cause:** Using invalid values for select fields or wrong data types
**Prevention:** Check valid values using get_issue or project metadata
**Fix:** Use exact valid values from JIRA configuration

## Troubleshooting Decision Tree

```
JIRA API Error Occurred?
├── Authentication Error (401/403)?
│   ├── Check credentials validity and format
│   ├── Verify user has required project permissions
│   └── Confirm API token hasn't expired
├── Issue Not Found (404)?
│   ├── Verify issue key format: PROJECT-NUMBER
│   ├── Check if issue exists and user has view permission
│   └── Confirm project key is correct
├── JQL Error (400)?
│   ├── Test JQL syntax in JIRA web interface
│   ├── Check field names exist in JIRA instance
│   ├── Verify operators and functions are valid
│   └── Ensure proper quoting of string values
├── Field Validation Error (400)?
│   ├── Check field names match JIRA schema exactly
│   ├── Verify field values are valid for field type
│   ├── Ensure required fields are included
│   └── Check data types match field requirements
└── Rate Limit Error (429)?
    ├── Implement exponential backoff retry
    └── Monitor API usage and adjust frequency
```

## Success Indicators

You know it's working when:
- [ ] **Issue searches** return expected results with proper pagination
- [ ] **Issue retrieval** returns complete issue objects with requested fields
- [ ] **Issue creation** returns new issue with generated key
- [ ] **Issue updates** reflect changes in JIRA interface
- [ ] **No permission errors** occur during authorized operations
- [ ] **JQL queries** execute without syntax errors

## Error Patterns to Watch For

Based on common JIRA API issues:

1. **Case Sensitivity:** Issue keys and field names are case-sensitive → Use exact casing
2. **Project Access:** User permissions change over time → Monitor project access
3. **JQL Complexity:** Complex queries can timeout → Simplify or paginate
4. **Field Changes:** JIRA configuration changes affect field names → Stay updated
5. **Rate Limiting:** Heavy usage can hit API limits → Implement throttling

## Related Resources

- **Error Log:** `@meta/mcp-learning/error-logs/jira-errors.md`
- **MCP Docker Guide:** `@meta/mcp-learning/usage-guides/mcp-docker-guide.md`
- **Parameter Patterns:** `@meta/mcp-learning/patterns/parameter-validation-patterns.yaml`
- **JIRA API Documentation:** https://developer.atlassian.com/cloud/jira/platform/rest/v3/

## Maintenance Notes

**Last Error Analysis:** 2025-01-24 (Initial baseline)
**Pattern Updates Needed:** None identified yet
**Success Rate:** Baseline being established
**Field Validation:** To be enhanced based on specific JIRA instance configuration

## Version History

- **v1.0** (2025-01-24): Initial guide based on JIRA API best practices and common usage patterns
- **Future versions:** Will be updated based on actual error patterns and successful operations

---

*This guide focuses specifically on JIRA operations and will be enhanced based on real usage patterns and error analysis*
## Auto-Generated Insights

### Error Pattern Analysis (Updated 2025-07-30)

**Common Issues Detected:**
- **Total Errors Logged:** 2
- **Authentication Errors:** 1
- **Parameter Errors:** 1
- **Tool Errors:** 2

**Auto-Generated Recommendations:**
- [ ] Review error patterns in `/Users/georgiospilitsoglou/Developer/projects/mypromptflow/meta/mcp-learning/error-logs/jira-errors.md`
- [ ] Focus on preventing most common error type
- [ ] Update pre-flight checklist based on error analysis
- [ ] Consider additional parameter validation

**Last Analysis:** 2025-07-30 11:18

## Validated Working Patterns (Auto-Generated)

### Success Statistics (Updated 2025-07-30)
- **Total Successful Operations:** 2
- **Success Rate:** High (operations completing without errors)
- **Pattern Confidence:** Based on actual successful operations

### Confirmed Working Approaches
*These patterns have been validated through successful operations:*

- **Issue Key Formats:** Validated through successful retrievals

**Success Pattern Details:** See `/Users/georgiospilitsoglou/Developer/projects/mypromptflow/meta/mcp-learning/success-patterns/jira-success-patterns.md` for complete successful operation logs
**Reliability:** These patterns represent actual working operations
**Last Validation:** 2025-07-30 11:18
