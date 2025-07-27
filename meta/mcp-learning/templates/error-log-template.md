# [MCP Server Name] Error Log

## Error Log Format

### Error Entry Template
```markdown
## Error #[number] - [Date YYYY-MM-DD HH:MM]

### Context & Intent
**What I was trying to do:** [Describe the goal/task]
**User request:** [Original user request if applicable]
**Expected outcome:** [What should have happened]

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

### Error Information
**Error Message:** 
```
[Full error message/response]
```

**Error Type:** [Authentication, Parameter Validation, API Limit, Network, etc.]
**Severity:** [High/Medium/Low]

### Analysis
**Root Cause:** [What actually caused the error]
**Missing Information:** [What parameter or context was missing]
**Parameter Issues:** [Specific parameter format problems]

### Resolution Attempts
1. **Attempt 1:** [What I tried] → [Result]
2. **Attempt 2:** [What I tried] → [Result]
3. **Final Resolution:** [What worked, if anything]

### Lessons Learned
**For Future Use:**
- [ ] [Specific lesson 1]
- [ ] [Specific lesson 2]
- [ ] [Parameter format requirement]
- [ ] [Authentication requirement]

**Prevention:**
- [ ] Check [specific requirement] before using
- [ ] Validate [parameter] format
- [ ] Ensure [context] is available

### Frequency Tracking
**First Occurrence:** [Date]
**Frequency:** [How many times this error occurred]
**Last Occurrence:** [Date]
**Status:** [Unresolved/Resolved/Pattern Identified]
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