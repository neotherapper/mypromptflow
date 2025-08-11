🎯 JIRA Integration - Cross-Project Access

Display this interactive menu to the user:
═══════════════════════════════════════════════════════════════════

┌─────────────────────────────────────────────────────────────────────┐
│ 📋 JIRA INTEGRATION - VanguardAI Project Access │
├─────────────────────────────────────────────────────────────────────┤
│ [1] System Status - Check integration health and setup │
│ [2] Current Sprint - View active sprint tasks │
│ [3] Backlog Items - View product backlog │
│ [4] Project Readiness - Evaluate cross-project setup │
│ [5] Task Details - Get specific issue information │
│ [6] Learning Status - Check MCP integration health │
└─────────────────────────────────────────────────────────────────────┘

💬 **How to Use:**
• **Menu Code Only:** "2" (View current sprint)
• **Menu Code + Query:** "5 SCRUM-87" (Get specific issue details)
• **Natural Language:** "Show me my assigned tasks" or "What's the sprint status?"

**What would you like to check?** Type your choice and I'll provide current JIRA information.

---

## JIRA COMMAND ROUTING INSTRUCTIONS (INTERNAL - DO NOT SHOW TO USER)

### Command Implementation Logic

**Critical: Always read fresh data when option is selected. Never cache or hardcode values.**

### [1] System Status - Integration Health Check

Execute this workflow:

1. **Symlink Validation**:
   ```bash
   # Check if symlink exists and is valid
   ls -la .jira 2>/dev/null
   readlink -f .jira 2>/dev/null
   ```

2. **Cache Health Check** (only if symlink valid):
   - Read `$(readlink -f .jira)/cache/stories/current-sprint.json`
   - Read `$(readlink -f .jira)/cache/stories/backlog.json`
   - Extract actual `last_updated` timestamps
   - Calculate data freshness in real-time

3. **MCP Learning Status**:
   - Check `meta/mcp-learning/usage-guides/jira-guide.md` exists
   - Count recent errors from `meta/mcp-learning/error-logs/jira-errors.md`
   - Verify hook configuration in `.claude/hooks.json`

4. **Display Current Status**:
```
✅ JIRA Integration System Status - Live Check
════════════════════════════════════════════════

🔗 **Symlink Status:**
{if symlink exists:}
✅ Active: .jira → {actual_resolved_path}
{if symlink broken:}
❌ Broken: Symlink target not accessible

📋 **Cache Health:**
{if cache accessible:}
✅ Sprint Cache: {actual_last_updated_time}
✅ Backlog Cache: {actual_last_updated_time}  
📊 Data Age: {calculated_minutes/hours_since_update}
{if cache inaccessible:}
❌ Cache Not Accessible: {specific_error}

🔧 **MCP Integration:**
✅ Learning System: {active/inactive based on file checks}
📊 Recent Errors: {actual_count_from_error_log}
🎯 Hook Status: {active/inactive based on hooks.json}

💡 **Overall Health:** {HEALTHY/DEGRADED/BROKEN based on checks}
```

### [2] Current Sprint - Dynamic Sprint Display

Execute this workflow:

1. **Load Fresh Sprint Data**:
   - Resolve symlink: `readlink -f .jira`
   - Read `{resolved_path}/cache/stories/current-sprint.json`
   - Parse JSON to extract current values

2. **Display Current Sprint Info**:
```
🚀 Current Sprint Status - Live Data
════════════════════════════════════

📊 **Sprint Details:** (from cache: {actual_last_updated})
🎯 Name: {actual_sprint_name}
📅 Duration: {actual_start_date} → {actual_end_date}
🎪 Goal: {actual_sprint_goal}

📈 **Live Task Breakdown:**
📋 Total Stories: {actual_total_count}
{calculate actual status counts from active_stories array:}
🟡 In Progress: {actual_in_progress_count}
🔵 In Review: {actual_in_review_count}  
⚪ To Do: {actual_todo_count}

🔍 **Recent Tasks:** (Top 10 by status priority)
{iterate through actual active_stories, group by status:}
{for each status group:}
**{status}:**
{for story in status group (limit based on space):}
• {actual_key}: {actual_title_truncated}

💡 **Your Focus:** {filter for AI/automation related tasks if any}
🔄 **Data Freshness:** {time_since_cache_update}
```

### [3] Backlog Items - Dynamic Backlog Display

Execute this workflow:

1. **Load Fresh Backlog Data**:
   - Read `{resolved_symlink_path}/cache/stories/backlog.json`
   - Parse to extract current backlog state

2. **Display Current Backlog**:
```
📋 Product Backlog - Live Data  
════════════════════════════════

📊 **Backlog Summary:** (from cache: {actual_last_updated})
🎯 Total Stories: {actual_total_stories_count}
📈 Total Points: {actual_total_points_sum}

📝 **Current Backlog Items:**
{iterate through actual backlog_stories array:}
{for each story:}
🔸 **{actual_key}** ({actual_story_points} pts)
   📋 {actual_title}
   👤 {actual_assignee_status} 
   🏷️ {actual_labels_joined}
   🎯 Epic: {actual_epic_reference}

{if user has assignments:}
💼 **Your Assignments:**
{filter stories where assignee matches user context}

🔄 **Data Freshness:** {calculated_age_of_cache}
```

### [4] Project Readiness - Dynamic Assessment

Execute this comprehensive evaluation:

1. **Real-time Dependency Check**:
   - Symlink accessibility test
   - Cache file availability and age
   - MCP hook configuration validation
   - Error rate analysis from logs

2. **Current Readiness Report**:
```
🔍 Cross-Project Integration Assessment - Live Analysis
═══════════════════════════════════════════════════════

✅ **Infrastructure (Tested Now):**
🔗 Symlink: {actual_test_result}
📂 Cache Access: {actual_read_test_result}
🔧 MCP Tools: {actual_hook_status}

✅ **Data Quality (Current State):**
📊 Sprint Data: {available_age_quality_assessment}
📋 Backlog Data: {available_age_quality_assessment}
🎯 Last Sync: {actual_time_calculation}

✅ **Performance (Real-time):**
⚡ Access Speed: {measure_actual_read_time}
🔄 Data Freshness: {actual_staleness_calculation}
📈 Success Rate: {calculated_from_error_logs}

📋 **Current Issues:** {identify_actual_problems}
💡 **Recommendations:** {specific_to_current_state}

🎯 **Readiness Score:** {calculated_percentage}/100
```

### [5] Task Details - Live Issue Lookup

When user provides issue key, execute:

1. **Dynamic Issue Retrieval**:
   - Use MCP tool: `mcp__MCP_DOCKER__jira_get_issue`
   - Parameters: `{"issue_key": "{extracted_key}", "fields": "summary,status,assignee,description,labels,customfield_10020"}`
   - Handle MCP errors gracefully with fallback to cache search

2. **Current Issue Details**:
```
📋 Issue Details: {actual_issue_key} - Live Data
═══════════════════════════════════════════════

📊 **Current Status:** (Retrieved: {timestamp})
📝 Title: {actual_summary}
🎯 Status: {actual_status}
👤 Assignee: {actual_assignee}
🏷️ Labels: {actual_labels}
📅 Sprint: {actual_sprint_assignment}

📖 **Description:**
{actual_description}

🔗 **Context Analysis:**
{analyze_relevance_to_mypromptflow_project}

{if cache search available:}
🔍 **Related Tasks:** {search_cache_for_related_issues}

💡 **Actions:** Use vanguardAI project for modifications
```

### [6] Learning Status - Live MCP Health

Execute this analysis:

1. **MCP System Health Check**:
   - Count errors from `meta/mcp-learning/error-logs/jira-errors.md`
   - Check recent success patterns
   - Analyze hook performance

2. **Current Learning Dashboard**:
```
🔧 MCP Learning System Status - Live Analysis
═════════════════════════════════════════════

📊 **Current Performance:**
✅ Hook Validation: {check_hooks_json_real_time}
📝 Total Errors Logged: {count_actual_errors}
📈 Recent Operations: {analyze_recent_activity}
🎯 Success Rate: {calculate_current_rate}

🔍 **Recent Activity:** (Last 10 operations)
{parse_actual_recent_entries}

📋 **Error Patterns:** (Current issues)
{categorize_recent_errors}

💡 **System Health:** {EXCELLENT/GOOD/NEEDS_ATTENTION}
🔄 **Recommendations:** {based_on_current_analysis}
```

### Natural Language Processing

Route natural language queries intelligently:

- **Issue key patterns** (SCRUM-XX, PROJ-XX) → Option [5] with extracted key
- **"my tasks"**, **"assigned to me"** → Options [2] or [3] with user filtering
- **"status"**, **"health"**, **"working"** → Option [1]
- **"sprint"**, **"current work"** → Option [2]  
- **"backlog"**, **"upcoming"** → Option [3]
- **"ready"**, **"setup"** → Option [4]
- **"errors"**, **"problems"**, **"learning"** → Option [6]

### Error Handling Strategy

**Integrated Learning System:**
```
🧠 Domain-Specific Error Learning
═══════════════════════════════════

Learning Source: VanguardAI .jira/learning/ system
Error Analysis: AI research context with cross-project coordination
Success Patterns: Documented in jira-usage-patterns.md
Recovery Procedures: Detailed in jira-error-recovery.md

Hooks Integration: Automatic error capture and pattern learning
```

**Symlink Issues:**
```
❌ Symlink Error Detected
═══════════════════════════

Problem: {specific_symlink_issue}
Solution: 
1. Check if vanguardAI project is accessible
2. Recreate symlink: ln -s ../../work/vanguardAI/.jira .jira
3. Verify permissions on target directory

Fallback: Use MCP tools for live data (slower but functional)
Learning: Automatically logged to vanguardAI .jira/learning/jira-error-recovery.md
```

**Cache Issues:**
```
⚠️ Cache Access Issue
════════════════════════

Problem: {specific_cache_issue}  
Impact: {performance_degradation}
Fallback: Using live MCP calls (slower response)

Recommended: Refresh cache from vanguardAI project
```

**MCP Issues:**
- Apply existing error learning system
- Use cache data when MCP calls fail
- Provide degraded but functional responses

### Performance Notes

**Optimization Strategy:**
1. **Cache First**: Always try cache for fast response
2. **MCP Fallback**: Use live calls when cache unavailable  
3. **Error Graceful**: Provide partial information when possible
4. **Fresh Data**: Every interaction reads current state

**Response Time Targets:**
- Cache reads: <1 second
- MCP calls: <5 seconds  
- Error fallbacks: <2 seconds