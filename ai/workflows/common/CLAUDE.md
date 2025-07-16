# Common Workflow Utilities - AI Agent Instructions

## Purpose
This file contains shared utilities and instructions used across all knowledge base workflows (bootstrap, status, and others).

## Cache Reading Utilities

### Standard Cache File Locations
- **Primary Cache**: `ai/context/knowledge-status-cache.yaml`
- **Document Registry**: `ai/context/document-registry.yaml`
- **Dependencies**: `ai/context/dependencies.yaml`
- **Bootstrap Config**: `ai/context/bootstrap-flow.yaml`

### Cache Reading Pattern
```yaml
# Read cache_summary for quick status
cache_summary:
  knowledge_base_health: "empty" | "healthy" | "needs_attention"
  total_documents: number
  completion_rate: "percentage"
  status: "bootstrap_needed" | "active" | "complete"
```

### State Detection Logic
```
IF total_documents == 0:
  → Route to bootstrap workflow
ELSE:
  → Route to status workflow
```

## Error Handling Utilities

### File Not Found Handling
```
IF cache file missing:
  → Create default empty cache
  → Guide user to bootstrap process
  → Suggest cache regeneration
```

### Invalid Data Handling
```
IF cache data malformed:
  → Use fallback defaults
  → Log warning about data quality
  → Suggest manual cache update
```

### User Input Validation
```
IF invalid menu choice:
  → Re-present valid options
  → Provide input format examples
  → Guide to correct selection
```

## Routing Logic

### Workflow Selection
```
function routeWorkflow(cacheData):
  if cacheData.total_documents == 0:
    return "bootstrap"
  else:
    return "status"
```

### Command Routing
```
function routeCommand(userInput):
  if userInput matches "1-9":
    return "status_menu_option"
  else:
    return "invalid_input"
```

## Data Transformation Utilities

### Completion Rate Calculation
```
function calculateCompletionRate(completed, total):
  if total == 0:
    return "0%"
  else:
    return f"{(completed/total)*100:.0f}%"
```

### Health Status Mapping
```
function mapHealthStatus(completionRate):
  if completionRate >= 80:
    return "healthy"
  elif completionRate >= 40:
    return "needs_attention"
  else:
    return "critical"
```

## Standard Response Templates

### Success Response Format
```
✅ [Success Message]
📊 [Key Metrics]
🎯 [Next Steps]
💡 [Helpful Tips]
```

### Error Response Format
```
❌ [Error Description]
🔧 [Suggested Fix]
📝 [Example Usage]
🔄 [Retry Instructions]
```

### Progress Response Format
```
📈 [Progress Summary]
✅ [Completed Items]
⏳ [In Progress Items]
📋 [Next Items]
```

## Integration Patterns

### Cache Update Notification
```
💡 Tip: Cache updates are manual. Run `/update-knowledge-cache` after creating documents.
```

### Command Suggestions
```
Based on your current state, try:
- `/create-document [name]` - Create specific document
- `/orchestrate-agents [type]` - Multi-agent creation
- `/knowledge-status` - Return to status menu
```

## Performance Guidelines

### Cache Loading
- Load cache data once per session
- Cache parsed data in memory
- Reload only when explicitly requested

### Response Speed
- Provide immediate feedback for user actions
- Use progressive disclosure for complex data
- Prioritize most important information first

## Validation Rules

### Data Consistency Checks
- Document counts match between cache and registry
- Dependency references are valid
- Completion percentages are calculated correctly

### User Input Validation
- Menu choices are within valid range (1-9)
- Text responses are non-empty when required
- File paths exist when referenced

## Logging and Debugging

### Log Important Events
- Workflow routing decisions
- Cache read operations
- User menu selections
- Error conditions

### Debug Information
- Cache file timestamps
- Data consistency warnings
- Performance metrics
- User interaction patterns

## Security Considerations

### Safe File Operations
- Always validate file paths
- Use read-only operations when possible
- Handle permission errors gracefully

### Data Privacy
- Don't log sensitive user data
- Sanitize file paths in error messages
- Protect internal system information

## Common UI Elements

### Loading Indicators
```
⏳ Loading knowledge base status...
📊 Analyzing dependencies...
🔍 Checking document registry...
```

### Status Icons
```
✅ Complete
⏳ In Progress
❌ Missing
🔒 Blocked
🚀 Ready
```

### Priority Indicators
```
🔴 High Priority
🟡 Medium Priority
🟢 Low Priority
⚪ No Priority Set
```

These utilities ensure consistency across all knowledge base workflows while providing reliable, reusable components.