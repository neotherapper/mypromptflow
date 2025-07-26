# MCP Docker Server Usage Guide

## Server Overview
**Server Name:** MCP Docker Server
**Primary Purpose:** Comprehensive Docker-based tool ecosystem providing Notion API, JIRA integration, browser automation, search capabilities, and specialized tools
**Authentication Type:** Container-based with individual service authentication
**Last Updated:** 2025-01-24
**Error Log:** @meta/mcp-learning/error-logs/mcp-docker-errors.md

## Pre-Flight Checklist

Before using any MCP Docker tools, verify:

- [ ] **Docker Containers:** MCP Docker containers are running and accessible
- [ ] **Service Authentication:** Individual service credentials (Notion, JIRA, etc.) are valid
- [ ] **Parameter Formats:** Input parameters match service-specific requirements
- [ ] **Network Connectivity:** External services are reachable
- [ ] **Rate Limits:** Check usage quotas for external APIs

## Common Use Cases

### Use Case 1: Notion Database Operations
**Purpose:** Create, query, and manage Notion databases and pages
**Tools:** mcp__MCP_DOCKER__API-* (create-a-database, post-database-query, etc.)
**Success Pattern:** Validate UUIDs and rich text format before operations

**Working Example:**
```
Tool: mcp__MCP_DOCKER__API-post-database-query
Parameters:
{
  "database_id": "12345678-1234-1234-1234-123456789abc",
  "page_size": 100,
  "filter": {...},
  "sorts": [...]
}
Expected Result: JSON response with pages array and pagination info
```

### Use Case 2: JIRA Issue Management
**Purpose:** Search, create, and manage JIRA issues and projects
**Tools:** mcp__MCP_DOCKER__jira_* (search, get_issue, create_issue, etc.)
**Success Pattern:** Use proper PROJECT-NUMBER format for issue keys

**Working Example:**
```
Tool: mcp__MCP_DOCKER__jira_get_issue
Parameters:
{
  "issue_key": "SCRUM-123",
  "fields": "summary,status,assignee,priority"
}
Expected Result: Detailed issue object with requested fields
```

### Use Case 3: Browser Automation
**Purpose:** Automate web interactions, form filling, and data extraction
**Tools:** mcp__MCP_DOCKER__browser_* (navigate, click, type, snapshot, etc.)
**Success Pattern:** Always take snapshot before element interactions

**Working Example:**
```
Tool: mcp__MCP_DOCKER__browser_navigate
Parameters:
{
  "url": "https://example.com"
}
Expected Result: Navigation success confirmation
```

## Parameter Reference

### Notion API Parameters
| Parameter | Type | Format | Example | Notes |
|-----------|------|---------|---------|--------|
| database_id | string | UUID | "12345678-1234-1234-1234-123456789abc" | Always required for DB operations |
| page_id | string | UUID/Notion ID | "12345678123412341234123456789abc" | Page identifier |
| rich_text | array | Notion rich text | [{"type": "text", "text": {"content": "Hello"}}] | Must follow Notion format |

### JIRA Parameters
| Parameter | Type | Format | Example | Notes |
|-----------|------|---------|---------|--------|
| issue_key | string | PROJECT-NUMBER | "SCRUM-123" | Case sensitive |
| project_key | string | UPPERCASE | "SCRUM" | Project identifier |
| jql | string | JQL syntax | "project = SCRUM AND status = 'Open'" | Valid JQL required |

### Browser Automation Parameters
| Parameter | Type | Format | Example | Notes |
|-----------|------|---------|---------|--------|
| url | string | HTTP/HTTPS URL | "https://example.com" | Must be accessible |
| element | string | Description | "Submit button" | Human-readable description |
| ref | string | Element ID | "element-123" | From page snapshot |

## Known Working Patterns

### Pattern 1: Notion Database Query Flow
**When to use:** Retrieving data from Notion databases
**Steps:**
1. Validate database_id is proper UUID format
2. Construct filter and sort objects if needed
3. Set appropriate page_size (typically 10-100)
4. Execute query and handle pagination

**Example:**
```json
{
  "database_id": "valid-uuid-here",
  "page_size": 50,
  "filter": {
    "property": "Status",
    "select": {
      "equals": "Active"
    }
  }
}
```

### Pattern 2: JIRA Issue Search with JQL
**When to use:** Finding JIRA issues with specific criteria
**Steps:**
1. Construct valid JQL query
2. Specify fields to return (avoid "*all" for performance)
3. Set reasonable limit (10-50 typically)
4. Handle pagination with start_at

**Example:**
```json
{
  "jql": "project = SCRUM AND assignee = currentUser()",
  "fields": "summary,status,assignee,priority",
  "limit": 20,
  "start_at": 0
}
```

### Pattern 3: Browser Element Interaction Workflow
**When to use:** Interacting with web page elements
**Steps:**
1. Navigate to target URL
2. Take snapshot to understand page structure
3. Identify element from snapshot
4. Perform interaction using element reference
5. Wait for page changes if needed

**Example:**
```
1. browser_navigate: {"url": "https://example.com"}
2. browser_snapshot: {}
3. browser_click: {"element": "Login button", "ref": "button-login-123"}
```

## Common Pitfalls & How to Avoid Them

### Pitfall 1: Invalid UUID Format
**Error:** "Invalid database_id format" or similar UUID errors
**Symptom:** API returns 400 Bad Request with UUID validation error
**Cause:** UUID not in proper format or missing hyphens
**Prevention:** Always validate UUID format: 8-4-4-4-12 character pattern
**Fix:** Use proper UUID format with hyphens: "12345678-1234-1234-1234-123456789abc"

### Pitfall 2: Malformed JQL Queries
**Error:** "JQL syntax error" or query parsing failures
**Symptom:** JIRA search returns syntax error response
**Cause:** Invalid JQL syntax, typos in field names, or improper operators
**Prevention:** Test JQL in JIRA web interface first, use proper quotes around values
**Fix:** Validate JQL syntax: `project = "PROJECT" AND status = "Status Value"`

### Pitfall 3: Element Reference Errors
**Error:** "Element not found" or interaction failures
**Symptom:** Browser automation tools fail to interact with elements
**Cause:** Element reference is stale or incorrect
**Prevention:** Always take fresh snapshot before element interactions
**Fix:** Take new snapshot and use current element references

### Pitfall 4: Authentication Failures
**Error:** "Unauthorized" or "Invalid credentials"
**Symptom:** 401/403 HTTP status codes from APIs
**Cause:** Expired tokens, invalid credentials, or insufficient permissions
**Prevention:** Verify credentials are current and have required scope
**Fix:** Refresh tokens, update credentials, or request additional permissions

## Troubleshooting Decision Tree

```
Error occurred with MCP Docker tool?
├── Authentication Error (401/403)?
│   ├── Yes → Check service-specific credentials
│   │   ├── Notion → Verify API token and workspace access
│   │   ├── JIRA → Check username/password or API token
│   │   └── Browser → Usually no auth required
│   └── No → Continue to Parameter Error
├── Parameter Error (400)?
│   ├── UUID/ID format → Validate UUID format with hyphens
│   ├── JQL syntax → Test query in JIRA web interface
│   ├── Rich text format → Check Notion rich text structure
│   └── Element reference → Take fresh snapshot
└── Service Error (500/503)?
    ├── External service down → Check service status pages
    ├── Rate limiting → Wait and retry with exponential backoff
    └── Network issue → Verify connectivity and DNS resolution
```

## Success Indicators

You know it's working when:
- [ ] **Notion operations** return valid JSON with expected data structure
- [ ] **JIRA operations** return issue objects or successful confirmation
- [ ] **Browser operations** complete without timeout or element errors
- [ ] **No authentication errors** appear in responses
- [ ] **Parameters are accepted** without validation errors

## Error Patterns to Watch For

Based on anticipated issues:

1. **UUID Format Issues:** Missing hyphens or invalid character patterns → Validate before use
2. **JQL Syntax Errors:** Typos or invalid operators → Test queries first
3. **Element Staleness:** Element references become invalid → Take fresh snapshots
4. **Rate Limiting:** Too many requests too quickly → Implement backoff strategies
5. **Authentication Expiry:** Tokens expire over time → Monitor and refresh

## Related Resources

- **Error Log:** `@meta/mcp-learning/error-logs/mcp-docker-errors.md`
- **Parameter Patterns:** `@meta/mcp-learning/patterns/parameter-validation-patterns.yaml`
- **Common Patterns:** `@meta/mcp-learning/patterns/common-error-patterns.yaml`
- **Troubleshooting Template:** `@meta/mcp-learning/templates/troubleshooting-template.md`

## Maintenance Notes

**Last Error Analysis:** 2025-01-24 (Initial baseline)
**Pattern Updates Needed:** None identified yet
**Success Rate:** Baseline being established

## Version History

- **v1.0** (2025-01-24): Initial guide based on anticipated patterns and best practices
- **Future versions:** Will be updated based on actual error patterns and successful resolutions

---

*This guide will be continuously updated based on actual MCP Docker tool usage patterns and error analysis*