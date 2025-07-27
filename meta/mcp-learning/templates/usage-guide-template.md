# [MCP Server Name] Usage Guide

## Server Overview
**Server Name:** [Full MCP server name]
**Primary Purpose:** [What this server does]
**Authentication Type:** [API key, OAuth, Basic Auth, etc.]
**Last Updated:** [Date]
**Error Log:** [Link to corresponding error log file]

## Pre-Flight Checklist

Before using any tools from this server, verify:

- [ ] **Authentication:** [Specific auth requirements]
- [ ] **Required Parameters:** [Always needed parameters]
- [ ] **Data Format:** [Expected input formats]
- [ ] **Rate Limits:** [Any known limitations]
- [ ] **Dependencies:** [What must exist first]

## Common Use Cases

### Use Case 1: [Primary Function]
**Purpose:** [What you're trying to accomplish]
**Tools:** [Specific MCP tools to use]
**Success Pattern:** [What works reliably]

**Working Example:**
```
Tool: [mcp_tool_name]
Parameters:
{
  "param1": "working_value",
  "param2": "validated_format"
}
Expected Result: [What you should see]
```

### Use Case 2: [Secondary Function]
[Same format as above]

## Parameter Reference

### Required Parameters
| Parameter | Type | Format | Example | Notes |
|-----------|------|---------|---------|--------|
| param1 | string | specific_format | "example" | Always required |
| param2 | object | {key: value} | {"id": "123"} | Must be valid JSON |

### Optional Parameters
| Parameter | Type | Default | Purpose | Notes |
|-----------|------|---------|---------|--------|
| opt1 | boolean | false | Enable feature | Use with caution |

## Known Working Patterns

### Pattern 1: [Successful Approach]
**When to use:** [Specific scenario]
**Steps:**
1. [First step with specific parameters]
2. [Second step with validation]
3. [Final step with expected outcome]

**Example:**
```
[Full working example with actual parameters]
```

### Pattern 2: [Alternative Approach]
[Same format]

## Common Pitfalls & How to Avoid Them

### Pitfall 1: [Common Error]
**Error:** [What goes wrong]
**Symptom:** [How you recognize it]  
**Cause:** [Why it happens]
**Prevention:** [How to avoid it]
**Fix:** [How to resolve if it occurs]

### Pitfall 2: [Another Common Error]
[Same format]

## Troubleshooting Decision Tree

```
Error occurred?
├── Authentication Error?
│   ├── Yes → Check [specific auth requirement]
│   │   ├── Fixed? → Continue
│   │   └── Still failing? → [Specific resolution steps]
│   └── No → Continue to Parameter Error
├── Parameter Error?
│   ├── Yes → Validate [specific parameters]
│   │   ├── Format issue? → [Fix format]
│   │   └── Missing required? → [Add required parameters]
│   └── No → Continue to API Error
└── API Error?
    ├── Rate limit? → [Wait/retry strategy]
    ├── Service unavailable? → [Check status/alternative]
    └── Unknown? → [Log error and investigate]
```

## Success Indicators

You know it's working when:
- [ ] [Specific success criterion 1]
- [ ] [Specific success criterion 2]
- [ ] [Expected response format received]
- [ ] [No error messages in response]

## Error Patterns to Watch For

Based on error log analysis:

1. **[Pattern Name]:** [Description] → Check [specific thing]
2. **[Pattern Name]:** [Description] → Validate [specific parameter]
3. **[Pattern Name]:** [Description] → Ensure [specific condition]

## Related Resources

- **Error Log:** `@meta/mcp-learning/error-logs/[server-name]-errors.md`
- **Parameter Patterns:** `@meta/mcp-learning/patterns/parameter-validation-patterns.yaml`
- **Server Documentation:** [Official docs if available]

## Maintenance Notes

**Last Error Analysis:** [Date]
**Pattern Updates Needed:** [Any identified improvements]
**Success Rate:** [Track improvement over time]

## Version History

- **v1.0** ([Date]): Initial guide based on error analysis
- **v1.1** ([Date]): Added [specific improvement]