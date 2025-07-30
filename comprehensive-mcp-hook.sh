#!/bin/bash

# Comprehensive MCP Hook for Claude Code
# Combines debugging with parameter validation

DEBUG_LOG="/Users/georgiospilitsoglou/Developer/projects/mypromptflow/hook-debug.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] 📋 COMPREHENSIVE HOOK CALLED!" >> "$DEBUG_LOG"
echo "[$TIMESTAMP] Tool: $CLAUDE_TOOL_NAME" >> "$DEBUG_LOG"
echo "[$TIMESTAMP] Session: $CLAUDE_SESSION_ID" >> "$DEBUG_LOG"
echo "[$TIMESTAMP] Args: $*" >> "$DEBUG_LOG"
echo "[$TIMESTAMP] Working Dir: $(pwd)" >> "$DEBUG_LOG"

# Check if this is a JIRA tool that needs validation
case "$CLAUDE_TOOL_NAME" in
    mcp__MCP_DOCKER__jira_*)
        echo "[$TIMESTAMP] 🔍 JIRA tool detected - applying validation" >> "$DEBUG_LOG"
        
        # Call MCP parameter validator
        VALIDATOR_PATH="/Users/georgiospilitsoglou/Developer/projects/mypromptflow/meta/mcp-learning/scripts/mcp-parameter-validator.sh"
        if [ -f "$VALIDATOR_PATH" ]; then
            echo "[$TIMESTAMP] 🚀 Running validation..." >> "$DEBUG_LOG"
            bash "$VALIDATOR_PATH" "$CLAUDE_SESSION_ID" "$CLAUDE_TRANSCRIPT_PATH" "$CLAUDE_TOOL_NAME" "$CLAUDE_TOOL_INPUT" 2>> "$DEBUG_LOG"
            VALIDATION_RESULT=$?
            echo "[$TIMESTAMP] ✅ Validation completed with code: $VALIDATION_RESULT" >> "$DEBUG_LOG"
        else
            echo "[$TIMESTAMP] ⚠️  Validator not found at $VALIDATOR_PATH" >> "$DEBUG_LOG"
            echo '{"action": "allow", "reason": "Validator not available"}'
        fi
        ;;
    *)
        echo "[$TIMESTAMP] ℹ️  Non-JIRA tool - allowing without validation" >> "$DEBUG_LOG"
        echo '{"action": "allow", "reason": "Non-JIRA tool"}'
        ;;
esac

echo "[$TIMESTAMP] ====================" >> "$DEBUG_LOG"
exit 0