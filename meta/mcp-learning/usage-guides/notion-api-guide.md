# Notion API Usage Guide

## Server Overview
**Server Name:** Notion API (via MCP Docker)
**Primary Purpose:** Notion database operations, page creation, content management, and workspace automation
**Authentication Type:** Notion API token with workspace permissions
**Last Updated:** 2025-01-24
**Error Log:** @meta/mcp-learning/error-logs/notion-api-errors.md

## Pre-Flight Checklist

Before using any Notion API tools, verify:

- [ ] **API Token:** Valid Notion integration token with required permissions
- [ ] **Database Access:** Database/page IDs exist and are accessible
- [ ] **Property Schema:** Database properties match expected structure
- [ ] **Rich Text Format:** Content follows Notion rich text object format
- [ ] **Parent Relationships:** Page hierarchies and database relationships are valid

## Common Use Cases

### Use Case 1: Database Querying
**Purpose:** Retrieve filtered and sorted data from Notion databases
**Tools:** mcp__MCP_DOCKER__API-post-database-query
**Success Pattern:** Validate database_id format and construct proper filter objects

**Working Example:**
```
Tool: mcp__MCP_DOCKER__API-post-database-query
Parameters:
{
  "database_id": "12345678-1234-1234-1234-123456789abc",
  "page_size": 50,
  "filter": {
    "property": "Status",
    "select": {
      "equals": "Active"
    }
  },
  "sorts": [
    {
      "property": "Created",
      "direction": "descending"
    }
  ]
}
Expected Result: Pages array with pagination info
```

### Use Case 2: Page Creation
**Purpose:** Create new pages in databases or as child pages
**Tools:** mcp__MCP_DOCKER__API-post-page
**Success Pattern:** Ensure parent exists and properties match database schema

**Working Example:**
```
Tool: mcp__MCP_DOCKER__API-post-page
Parameters:
{
  "parent": {
    "page_id": "parent-page-uuid"
  },
  "properties": {
    "title": [
      {
        "text": {
          "content": "New Page Title"
        }
      }
    ]
  }
}
Expected Result: Created page object with ID and properties
```

### Use Case 3: Database Creation
**Purpose:** Create new databases with defined property schemas
**Tools:** mcp__MCP_DOCKER__API-create-a-database
**Success Pattern:** Define complete property schema before creation

**Working Example:**
```
Tool: mcp__MCP_DOCKER__API-create-a-database
Parameters:
{
  "parent": {
    "type": "page_id",
    "page_id": "parent-page-uuid"
  },
  "title": [
    {
      "type": "text",
      "text": {
        "content": "New Database"
      }
    }
  ],
  "properties": {
    "Name": {
      "title": {}
    },
    "Status": {
      "select": {
        "options": [
          {"name": "Active"},
          {"name": "Inactive"}
        ]
      }
    }
  }
}
Expected Result: Database object with defined schema
```

## Parameter Reference

### Essential Parameters
| Parameter | Type | Format | Example | Notes |
|-----------|------|---------|---------|--------|
| database_id | string | UUID | "12345678-1234-1234-1234-123456789abc" | Must include hyphens |
| page_id | string | UUID/Notion ID | "12345678123412341234123456789abc" | Can be with or without hyphens |
| properties | object | Notion properties | See examples below | Must match database schema |
| rich_text | array | Rich text objects | [{"type": "text", "text": {"content": "Text"}}] | Notion-specific format |

### Property Type Examples
| Property Type | Structure | Example |
|---------------|-----------|---------|
| Title | `[{"text": {"content": "string"}}]` | `[{"text": {"content": "Page Title"}}]` |
| Rich Text | `[{"text": {"content": "string"}}]` | `[{"text": {"content": "Description text"}}]` |
| Select | `{"name": "option_name"}` | `{"name": "In Progress"}` |
| Multi-select | `[{"name": "option1"}, {"name": "option2"}]` | `[{"name": "Tag1"}, {"name": "Tag2"}]` |
| Date | `{"start": "YYYY-MM-DD"}` | `{"start": "2025-01-24"}` |
| Number | `number` | `42` |
| Checkbox | `boolean` | `true` |

## Known Working Patterns

### Pattern 1: Database Query with Complex Filters
**When to use:** Retrieving specific records with multiple conditions
**Steps:**
1. Validate database_id is proper UUID format with hyphens
2. Construct filter object with proper property names
3. Add sorts for consistent ordering
4. Handle pagination for large result sets

**Example:**
```json
{
  "database_id": "12345678-1234-1234-1234-123456789abc",
  "filter": {
    "and": [
      {
        "property": "Status",
        "select": {
          "equals": "Active"
        }
      },
      {
        "property": "Priority",
        "select": {
          "equals": "High"
        }
      }
    ]
  },
  "sorts": [
    {
      "property": "Created",
      "direction": "descending"
    }
  ]
}
```

### Pattern 2: Page Creation with Rich Content
**When to use:** Creating pages with formatted text and properties
**Steps:**
1. Verify parent page/database exists and is accessible
2. Match property structure to database schema
3. Format rich text content properly
4. Include all required properties

**Example:**
```json
{
  "parent": {
    "database_id": "database-uuid-here"
  },
  "properties": {
    "Name": {
      "title": [
        {
          "text": {
            "content": "Task Name"
          }
        }
      ]
    },
    "Status": {
      "select": {
        "name": "In Progress"
      }
    },
    "Description": {
      "rich_text": [
        {
          "text": {
            "content": "Detailed task description with formatting"
          }
        }
      ]
    }
  }
}
```

### Pattern 3: Block Content Manipulation
**When to use:** Adding or updating content within pages
**Steps:**
1. Get page/block ID for target location
2. Structure content as block objects
3. Use appropriate block types (paragraph, heading, etc.)
4. Append or update block children

**Example:**
```json
{
  "block_id": "page-or-block-uuid",
  "children": [
    {
      "type": "paragraph",
      "paragraph": {
        "rich_text": [
          {
            "type": "text",
            "text": {
              "content": "New paragraph content"
            }
          }
        ]
      }
    }
  ]
}
```

## Common Pitfalls & How to Avoid Them

### Pitfall 1: UUID Format Inconsistency
**Error:** "Invalid database_id" or "Page not found"
**Symptom:** 400 Bad Request with UUID validation error
**Cause:** UUID missing hyphens or in wrong format
**Prevention:** Always use UUID with hyphens: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
**Fix:** Convert 32-character IDs to hyphenated format: "12345678-1234-1234-1234-123456789abc"

### Pitfall 2: Property Schema Mismatch
**Error:** "Property does not exist" or "Invalid property value"
**Symptom:** 400 Bad Request with property validation error
**Cause:** Property name doesn't match database schema or wrong value type
**Prevention:** Check database schema first with retrieve-a-database call
**Fix:** Use exact property names and correct value formats from schema

### Pitfall 3: Rich Text Format Errors
**Error:** "Invalid rich text format"
**Symptom:** Content not appearing or formatting errors
**Cause:** Incorrect rich text object structure
**Prevention:** Always use proper rich text array format
**Fix:** Structure as: `[{"type": "text", "text": {"content": "Your text"}}]`

### Pitfall 4: Permission and Access Issues
**Error:** "Unauthorized" or "Forbidden"
**Symptom:** 401/403 HTTP status codes
**Cause:** API token lacks required permissions or access to resource
**Prevention:** Ensure integration has access to target databases/pages
**Fix:** Update integration permissions in Notion or use different API token

## Troubleshooting Decision Tree

```
Notion API Error Occurred?
├── Authentication Error (401/403)?
│   ├── Check API token validity and permissions
│   ├── Verify integration has access to target resources
│   └── Confirm workspace permissions are sufficient
├── Parameter Error (400)?
│   ├── UUID format → Add hyphens to database/page IDs
│   ├── Property name → Check exact schema property names
│   ├── Property value → Validate value type and format
│   └── Rich text format → Use proper array structure
├── Not Found Error (404)?
│   ├── Database/page doesn't exist → Verify ID is correct
│   ├── Resource deleted → Check if resource still exists
│   └── Permission issue → Verify access permissions
└── Rate Limit Error (429)?
    ├── Too many requests → Implement exponential backoff
    └── Check rate limit headers → Adjust request frequency
```

## Success Indicators

You know it's working when:
- [ ] **Database queries** return expected pages array with proper pagination
- [ ] **Page creation** returns new page object with generated ID
- [ ] **Property updates** reflect changes in Notion workspace
- [ ] **Rich text** displays properly formatted in Notion
- [ ] **No authentication errors** occur during operations

## Error Patterns to Watch For

Based on common Notion API issues:

1. **UUID Format Confusion:** Missing hyphens in IDs → Always use hyphenated format
2. **Property Schema Drift:** Database schema changes → Re-check schema before operations
3. **Rich Text Malformation:** Incorrect object structure → Use proper array format
4. **Permission Creep:** Access permissions change → Monitor and update integration permissions
5. **Rate Limiting:** Excessive API calls → Implement request throttling

## Related Resources

- **Error Log:** `@meta/mcp-learning/error-logs/notion-api-errors.md`
- **MCP Docker Guide:** `@meta/mcp-learning/usage-guides/mcp-docker-guide.md`
- **Parameter Patterns:** `@meta/mcp-learning/patterns/parameter-validation-patterns.yaml`
- **Notion API Documentation:** https://developers.notion.com/reference

## Maintenance Notes

**Last Error Analysis:** 2025-01-24 (Initial baseline)
**Pattern Updates Needed:** None identified yet
**Success Rate:** Baseline being established
**Schema Validation:** To be implemented based on error patterns

## Version History

- **v1.0** (2025-01-24): Initial guide based on Notion API best practices and common patterns
- **Future versions:** Will be updated based on actual error patterns and successful operations

---

*This guide focuses specifically on Notion API operations and will be enhanced based on real usage patterns*