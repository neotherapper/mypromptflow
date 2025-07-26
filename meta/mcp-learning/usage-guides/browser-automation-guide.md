# Browser Automation Usage Guide

## Server Overview
**Server Name:** Browser Automation (via MCP Docker)
**Primary Purpose:** Web browser automation, UI testing, web scraping, form filling, and web interaction workflows
**Authentication Type:** Generally none (local browser automation)
**Last Updated:** 2025-01-24
**Error Log:** @meta/mcp-learning/error-logs/browser-errors.md

## Pre-Flight Checklist

Before using any browser automation tools, verify:

- [ ] **Browser Installation:** Target browser is installed and accessible
- [ ] **URL Accessibility:** Target websites are reachable and responsive
- [ ] **Network Connectivity:** Stable internet connection for external sites
- [ ] **Element References:** Current page snapshot available for element interactions
- [ ] **Timeout Settings:** Appropriate timeouts set for page loads and element waits
- [ ] **JavaScript Errors:** Target site doesn't have blocking JavaScript errors

## Common Use Cases

### Use Case 1: Web Navigation and Content Extraction
**Purpose:** Navigate to websites and extract information
**Tools:** mcp__MCP_DOCKER__browser_navigate, mcp__MCP_DOCKER__browser_snapshot
**Success Pattern:** Navigate first, then take snapshot to understand page structure

**Working Example:**
```
Tool: mcp__MCP_DOCKER__browser_navigate
Parameters:
{
  "url": "https://example.com"
}
Expected Result: Navigation success confirmation

Tool: mcp__MCP_DOCKER__browser_snapshot
Parameters: {}
Expected Result: Accessibility tree with element structure and IDs
```

### Use Case 2: Form Filling and Submission
**Purpose:** Automatically fill out and submit web forms
**Tools:** mcp__MCP_DOCKER__browser_type, mcp__MCP_DOCKER__browser_click
**Success Pattern:** Take snapshot, identify elements, interact using references

**Working Example:**
```
1. Take snapshot to identify form elements
2. Fill username field:
Tool: mcp__MCP_DOCKER__browser_type
Parameters:
{
  "element": "Username input field",
  "ref": "input-username-123",
  "text": "user@example.com"
}

3. Click submit button:
Tool: mcp__MCP_DOCKER__browser_click
Parameters:
{
  "element": "Submit button",
  "ref": "button-submit-456"
}
Expected Result: Form submission and page change
```

### Use Case 3: Dynamic Content Interaction
**Purpose:** Wait for and interact with dynamically loaded content
**Tools:** mcp__MCP_DOCKER__browser_wait_for, mcp__MCP_DOCKER__browser_hover
**Success Pattern:** Wait for content to load before attempting interaction

**Working Example:**
```
1. Wait for specific content to appear:
Tool: mcp__MCP_DOCKER__browser_wait_for
Parameters:
{
  "text": "Loading complete",
  "time": 10
}

2. Hover over dropdown menu:
Tool: mcp__MCP_DOCKER__browser_hover
Parameters:
{
  "element": "Settings dropdown",
  "ref": "dropdown-settings-789"
}
Expected Result: Dropdown menu becomes visible
```

### Use Case 4: Screenshot and Visual Verification
**Purpose:** Capture visual state of pages for verification or documentation
**Tools:** mcp__MCP_DOCKER__browser_take_screenshot
**Success Pattern:** Navigate to target state, then capture screenshot

**Working Example:**
```
Tool: mcp__MCP_DOCKER__browser_take_screenshot
Parameters:
{
  "fullPage": true,
  "filename": "homepage-screenshot.png"
}
Expected Result: Screenshot file saved with visual page state
```

## Parameter Reference

### Navigation Parameters
| Parameter | Type | Format | Example | Notes |
|-----------|------|---------|---------|--------|
| url | string | HTTP/HTTPS URL | "https://example.com" | Must be valid and accessible |

### Element Interaction Parameters
| Parameter | Type | Format | Example | Notes |
|-----------|------|---------|---------|--------|
| element | string | Description | "Submit button" | Human-readable element description |
| ref | string | Element ID | "button-submit-123" | From page snapshot |
| text | string | Text content | "Hello World" | For typing operations |
| key | string | Key name | "Enter" | Keyboard key names |

### Screenshot Parameters
| Parameter | Type | Format | Example | Notes |
|-----------|------|---------|---------|--------|
| fullPage | boolean | true/false | true | Capture full scrollable page |
| filename | string | File path | "screenshot.png" | Optional filename |
| raw | boolean | true/false | false | PNG vs JPEG format |

### Wait Parameters
| Parameter | Type | Format | Example | Notes |
|-----------|------|---------|---------|--------|
| text | string | Text content | "Loading complete" | Text to wait for |
| textGone | string | Text content | "Loading..." | Text to wait for removal |
| time | number | Seconds | 10 | Fixed time to wait |

## Known Working Patterns

### Pattern 1: Standard Web Form Automation
**When to use:** Filling out forms with multiple fields
**Steps:**
1. Navigate to form page
2. Take snapshot to identify all form elements
3. Fill fields one by one using element references
4. Submit form and wait for response
5. Verify success with another snapshot

**Example Workflow:**
```
1. browser_navigate({"url": "https://example.com/contact"})
2. browser_snapshot({})
3. browser_type({"element": "Name field", "ref": "input-name", "text": "John Doe"})
4. browser_type({"element": "Email field", "ref": "input-email", "text": "john@example.com"})
5. browser_click({"element": "Submit button", "ref": "button-submit"})
6. browser_wait_for({"text": "Thank you", "time": 5})
```

### Pattern 2: Dynamic Content Interaction
**When to use:** Working with JavaScript-heavy sites with dynamic content
**Steps:**
1. Navigate to page
2. Wait for initial content to load
3. Take snapshot to understand current state
4. Interact with dynamic elements (dropdowns, modals, etc.)
5. Wait for state changes before next interaction

**Example Workflow:**
```
1. browser_navigate({"url": "https://app.example.com/dashboard"})
2. browser_wait_for({"text": "Dashboard loaded", "time": 10})
3. browser_snapshot({})
4. browser_hover({"element": "User menu", "ref": "menu-user"})
5. browser_wait_for({"text": "Profile", "time": 3})
6. browser_click({"element": "Profile option", "ref": "option-profile"})
```

### Pattern 3: Multi-Step Workflow with Verification
**When to use:** Complex workflows requiring verification at each step
**Steps:**
1. Navigate to starting point
2. Perform action and verify result
3. Take screenshot for documentation
4. Continue to next step
5. Handle errors with fallback actions

**Example Workflow:**
```
1. browser_navigate({"url": "https://app.example.com/login"})
2. browser_type({"element": "Username", "ref": "input-user", "text": "username"})
3. browser_type({"element": "Password", "ref": "input-pass", "text": "password"})
4. browser_click({"element": "Login button", "ref": "button-login"})
5. browser_wait_for({"text": "Welcome", "time": 5})
6. browser_take_screenshot({"filename": "login-success.png"})
7. browser_navigate({"url": "https://app.example.com/settings"})
```

## Common Pitfalls & How to Avoid Them

### Pitfall 1: Stale Element References
**Error:** "Element not found" or "Element reference is stale"
**Symptom:** Element interactions fail even though element appears to exist
**Cause:** Page content changed and element references became invalid
**Prevention:** Take fresh snapshot before each interaction sequence
**Fix:** Always take new snapshot after page changes or navigation

### Pitfall 2: Timing Issues with Dynamic Content
**Error:** "Element not interactable" or timeout errors
**Symptom:** Clicks or interactions fail on elements that aren't ready
**Cause:** Attempting to interact before elements are fully loaded or visible
**Prevention:** Use wait_for to ensure content is ready before interaction
**Fix:** Add appropriate waits: `browser_wait_for({"text": "expected content", "time": 10})`

### Pitfall 3: Invalid URL Formats
**Error:** "Invalid URL" or navigation failures
**Symptom:** Navigation fails with URL validation errors
**Cause:** Malformed URLs or missing protocol
**Prevention:** Always use full URLs with http:// or https://
**Fix:** Ensure URLs are complete: "https://example.com" not "example.com"

### Pitfall 4: Element Description Ambiguity
**Error:** "Multiple elements match description" or "Element not found"
**Symptom:** Wrong elements are selected or no elements found
**Cause:** Element descriptions are too vague or not unique
**Prevention:** Use specific, unique descriptions based on snapshot
**Fix:** Be more specific: "Submit button in contact form" vs "Submit button"

### Pitfall 5: Browser State Management
**Error:** "Page not loaded" or unexpected browser state
**Symptom:** Operations fail because browser is in unexpected state
**Cause:** Previous operations left browser in different state than expected
**Prevention:** Always verify current page state with snapshot
**Fix:** Navigate to known starting point or take snapshot to understand current state

## Troubleshooting Decision Tree

```
Browser Automation Error Occurred?
├── Navigation Error?
│   ├── Invalid URL → Check URL format and accessibility
│   ├── Network timeout → Verify internet connection and site availability
│   ├── SSL certificate → Check site security and certificate validity
│   └── DNS resolution → Verify domain exists and is reachable
├── Element Interaction Error?
│   ├── Element not found → Take fresh snapshot and verify element exists
│   ├── Element not clickable → Check if element is visible and enabled
│   ├── Stale reference → Take new snapshot after page changes
│   └── Wrong element → Use more specific element descriptions
├── Timing Error?
│   ├── Page load timeout → Increase timeout or check site performance
│   ├── Element wait timeout → Verify expected content actually appears
│   └── JavaScript error → Check browser console for script errors
└── Browser Setup Error?
    ├── Browser not found → Verify browser installation
    ├── Driver mismatch → Check browser and driver version compatibility
    └── Permissions issue → Verify file system and network permissions
```

## Success Indicators

You know it's working when:
- [ ] **Navigation** completes without timeout errors
- [ ] **Element interactions** successfully perform intended actions
- [ ] **Snapshots** return detailed accessibility trees with element references
- [ ] **Screenshots** capture expected page content
- [ ] **Wait conditions** resolve within reasonable timeframes
- [ ] **Form submissions** complete and show expected results

## Error Patterns to Watch For

Based on common browser automation issues:

1. **Element Staleness:** References become invalid after page changes → Take fresh snapshots
2. **Timing Races:** Interactions happen before elements are ready → Use appropriate waits
3. **URL Accessibility:** Sites become unreachable or slow → Verify connectivity first
4. **JavaScript Errors:** Site scripts interfere with automation → Check browser console
5. **Dynamic Content:** Content loads asynchronously → Wait for specific indicators

## Related Resources

- **Error Log:** `@meta/mcp-learning/error-logs/browser-errors.md`
- **MCP Docker Guide:** `@meta/mcp-learning/usage-guides/mcp-docker-guide.md`
- **Parameter Patterns:** `@meta/mcp-learning/patterns/parameter-validation-patterns.yaml`
- **Browser Automation Best Practices:** Industry standards for web automation

## Maintenance Notes

**Last Error Analysis:** 2025-01-24 (Initial baseline)
**Pattern Updates Needed:** None identified yet
**Success Rate:** Baseline being established
**Browser Compatibility:** To be tested across different browser versions

## Version History

- **v1.0** (2025-01-24): Initial guide based on browser automation best practices and common patterns
- **Future versions:** Will be updated based on actual error patterns and successful automation workflows

---

*This guide focuses specifically on browser automation operations and will be enhanced based on real usage patterns and error analysis*