# User Experience Workflow for Blocked/Corrected MCP Calls

## Overview

This document defines the user experience workflow when the MCP Learning System blocks or corrects tool calls to prevent errors. The goal is to provide clear, actionable feedback that helps users understand what happened and how to proceed.

## User Experience Principles

### 1. Transparency
Users should always understand:
- **What was blocked/corrected** - Specific tool and parameters
- **Why the action was taken** - Clear reasoning based on learned patterns
- **What they can do next** - Actionable next steps

### 2. Efficiency
- **Minimal disruption** - Quick feedback without breaking workflow
- **Intelligent defaults** - Auto-correct when safe, ask when uncertain
- **Learning from interaction** - User choices improve future decisions

### 3. Control
- **User override capability** - Users can bypass blocks when needed
- **Preference learning** - System learns from user override patterns
- **Customizable sensitivity** - Adjust blocking/correction thresholds

## Workflow Scenarios

### Scenario 1: Automatic Parameter Correction

**Trigger**: System detects correctable parameter error (e.g., missing dash in PROJ123)

**User Experience Flow**:

```
1. Tool call intercepted
2. Parameters automatically corrected
3. Corrected call executed
4. User notification with summary
```

**User Notification Format**:
```
✅ Parameter Auto-Corrected
Tool: mcp__MCP_DOCKER__jira_get_issue
Original: {"issue_key": "PROJ123"}
Corrected: {"issue_key": "PROJ-123"}
Reason: Missing dash in issue key (learned from 3 previous errors)
Action: Call executed with corrected parameters
```

**User Actions Available**:
- **Continue** (default) - Accept correction and proceed
- **Revert** - Use original parameters anyway
- **Learn** - View correction details and patterns

### Scenario 2: High-Risk Call Blocking

**Trigger**: System detects high-risk pattern that typically causes errors

**User Experience Flow**:

```
1. Tool call intercepted
2. Call blocked with explanation
3. User presented with options
4. User choice recorded for learning
```

**User Notification Format**:
```
🚫 Call Blocked - High Error Risk
Tool: mcp__MCP_DOCKER__jira_create_issue
Parameters: {"project_key": "INVALID-PROJECT", ...}
Risk: 89% error probability based on 12 previous failures
Reason: Project key "INVALID-PROJECT" not found in system
Suggested: Check available projects with jira_get_projects

Options:
[Proceed Anyway] [Fix Parameters] [Cancel] [Learn More]
```

**User Actions Available**:
- **Proceed Anyway** - Override block and execute original call
- **Fix Parameters** - Open parameter correction assistant
- **Cancel** - Abort the operation entirely
- **Learn More** - View detailed error history and patterns

### Scenario 3: Medium-Risk Warning

**Trigger**: System detects potential issue but not certain enough to block

**User Experience Flow**:

```
1. Tool call intercepted
2. Warning presented with recommendation
3. User can proceed or modify
4. Choice feeds back to learning system
```

**User Notification Format**:
```
⚠️ Potential Issue Detected
Tool: mcp__MCP_DOCKER__jira_update_issue
Warning: Field "priority" value "Critical" might not exist
Confidence: 67% based on 5 similar cases
Suggestion: Use "High" instead (confirmed working)

Options:
[Proceed] [Use Suggestion] [Modify] [Cancel]
```

**User Actions Available**:
- **Proceed** - Continue with original parameters
- **Use Suggestion** - Apply system recommendation
- **Modify** - Open parameter editor
- **Cancel** - Abort operation

## User Interface Design

### Notification Styles

#### Success Notification (Auto-Correction)
```
┌─────────────────────────────────────────────────────────┐
│ ✅ Auto-Corrected: PROJ123 → PROJ-123                  │
│ Call executed successfully with learned correction      │
│ [View Details] [Disable for this tool]                 │
└─────────────────────────────────────────────────────────┘
```

#### Warning Notification (Medium Risk)
```
┌─────────────────────────────────────────────────────────┐
│ ⚠️  Potential Issue: Priority "Critical" might fail    │
│ Suggestion: Use "High" instead (89% success rate)      │
│ [Proceed] [Use Suggestion] [Modify] [Details]          │
└─────────────────────────────────────────────────────────┘
```

#### Block Notification (High Risk)
```
┌─────────────────────────────────────────────────────────┐
│ 🚫 Call Blocked: High error probability (89%)          │
│ Issue: Project "INVALID-PROJECT" not found             │
│ Based on 12 previous failures with this pattern        │
│ [Override] [Fix Parameters] [Cancel] [Details]         │
└─────────────────────────────────────────────────────────┘
```

### Interactive Parameter Editor

When user selects "Fix Parameters" or "Modify":

```
┌─────────────────────────────────────────────────────────┐
│ Parameter Editor - mcp__MCP_DOCKER__jira_create_issue  │
├─────────────────────────────────────────────────────────┤
│ project_key: [INVALID-PROJECT] ⚠️ Not found            │
│              Suggestions: [PROJ] [TEST] [DEV]          │
│                                                         │
│ summary: [Test Issue] ✅ Valid                          │
│                                                         │
│ issue_type: [Task] ✅ Valid                             │
│                                                         │
│ [Preview Call] [Execute] [Cancel]                       │
└─────────────────────────────────────────────────────────┘
```

### Learning Feedback Interface

When user selects "Learn More" or "Details":

```
┌─────────────────────────────────────────────────────────┐
│ Error Pattern Analysis                                  │
├─────────────────────────────────────────────────────────┤
│ Pattern: Invalid project key                           │
│ Occurrences: 12 times in last 30 days                  │
│ Success Rate: 11% (1 success, 11 failures)            │
│ Common Corrections:                                     │
│   • INVALID-PROJECT → PROJ (5 times)                   │
│   • TEST-PROJ → TEST (3 times)                         │
│   • DEV-PROJECT → DEV (2 times)                        │
│                                                         │
│ Recent Failures:                                        │
│   • 2025-07-29: "project does not exist"               │
│   • 2025-07-28: "permission denied for project"        │
│   • 2025-07-27: "invalid project key format"           │
│                                                         │
│ [Close] [Report Issue] [Adjust Sensitivity]            │
└─────────────────────────────────────────────────────────┘
```

## User Preference Management

### Sensitivity Settings

Users can customize the system behavior:

```
MCP Learning System Preferences
├── Blocking Sensitivity
│   ├── Conservative (block >60% error probability)
│   ├── Balanced (block >80% error probability) [Default]
│   └── Aggressive (block >95% error probability)
│
├── Auto-Correction
│   ├── Always auto-correct safe parameters ✅
│   ├── Ask before auto-correction
│   └── Never auto-correct
│
├── Notification Level
│   ├── Detailed (show all corrections and warnings)
│   ├── Summary (show blocks and major corrections) [Default]
│   └── Minimal (show only blocks)
│
└── Tool-Specific Overrides
    ├── jira_*: Balanced sensitivity
    ├── browser_*: Conservative (web interactions are risky)
    └── notion_*: Aggressive (Notion calls are usually safe)
```

### Learning from User Choices

The system learns from user decisions:

**Override Patterns**:
- If user consistently overrides blocks for specific patterns → Reduce blocking sensitivity
- If user's overrides frequently fail → Increase blocking sensitivity
- If user accepts most corrections → Continue auto-correcting similar patterns

**Success Tracking**:
- Track success/failure of user overrides
- Adjust confidence scores based on actual outcomes
- Build user-specific preference models

## Implementation Architecture

### User Experience Layer

```
┌─────────────────────────────────────────────────────────┐
│ User Experience Controller                              │
├─────────────────────────────────────────────────────────┤
│ • Notification Dispatcher                               │
│ • User Choice Handler                                   │
│ • Preference Manager                                    │
│ • Learning Feedback Collector                          │
└─────────────────────────────────────────────────────────┘
                              │
┌─────────────────────────────────────────────────────────┐
│ MCP Parameter Validator (Hook)                          │
├─────────────────────────────────────────────────────────┤
│ • Decision Engine                                       │
│ • Risk Assessment                                       │
│ • Correction Engine                                     │
│ • Pattern Matcher                                       │
└─────────────────────────────────────────────────────────┘
```

### User Choice Response Handler

```bash
# Handle user choice from notification
handle_user_choice() {
    local choice="$1"
    local tool_name="$2"
    local original_params="$3"
    local context="$4"
    
    case "$choice" in
        "proceed")
            execute_original_call "$tool_name" "$original_params"
            log_user_override "$tool_name" "$original_params" "proceed"
            ;;
        "use_suggestion")
            execute_corrected_call "$tool_name" "$corrected_params"
            log_user_acceptance "$tool_name" "$correction_type"
            ;;
        "modify")
            launch_parameter_editor "$tool_name" "$original_params"
            ;;
        "cancel")
            log_user_cancellation "$tool_name" "$original_params"
            ;;
        "learn_more")
            show_pattern_analysis "$tool_name" "$pattern_id"
            ;;
    esac
}
```

### Notification System Integration

```bash
# Send notification to user interface
send_user_notification() {
    local notification_type="$1"  # success|warning|block
    local tool_name="$2"
    local message="$3"
    local options="$4"
    
    # Format notification based on type
    local formatted_message=$(format_notification "$notification_type" "$tool_name" "$message" "$options")
    
    # Send to Claude Code interface
    echo "$formatted_message"
    
    # Wait for user response if interactive
    if [[ "$notification_type" != "success" ]]; then
        read -r user_choice
        handle_user_choice "$user_choice" "$tool_name" "$original_params" "$context"
    fi
}
```

## Success Metrics

### User Experience Quality
- **Decision Time**: Average time for user to respond to notifications (target: <30 seconds)
- **Override Success Rate**: Success rate of user overrides (target: >70%)
- **User Satisfaction**: Survey scores for workflow interruption acceptability (target: >4/5)
- **Learning Effectiveness**: Reduction in repeated user corrections (target: >50% in 2 weeks)

### System Effectiveness
- **False Positive Rate**: Unnecessary blocks/corrections (target: <20%)
- **False Negative Rate**: Missed error prevention opportunities (target: <10%)
- **Auto-Correction Accuracy**: Success rate of automatic corrections (target: >90%)
- **User Preference Adaptation**: Accuracy of learned user preferences (target: >80%)

## Future Enhancements

### Advanced Features
1. **Predictive Assistance**: Suggest parameters before user enters them
2. **Context-Aware Blocking**: Consider current task context in decisions
3. **Collaborative Learning**: Share anonymized patterns across users
4. **Integration with IDEs**: Native IDE plugins for seamless experience

### Machine Learning Integration
1. **User Behavior Modeling**: Personalized risk tolerance learning
2. **Pattern Evolution**: Automatically detect new error patterns
3. **Success Prediction**: Predict call success probability in real-time
4. **Optimal Timing**: Learn best times to show notifications

This workflow ensures users maintain control while benefiting from the system's learned intelligence, creating a balance between automation and transparency that improves over time through user interaction.