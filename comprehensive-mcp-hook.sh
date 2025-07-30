#!/bin/bash
# Comprehensive MCP hook for learning system

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
DEBUG_LOG="/Users/georgiospilitsoglou/Developer/projects/mypromptflow/mcp-hook-analysis.log"

echo "[$TIMESTAMP] ==================================" >> "$DEBUG_LOG"
echo "[$TIMESTAMP] MCP HOOK TRIGGERED!" >> "$DEBUG_LOG"
echo "[$TIMESTAMP] Tool Name: '$CLAUDE_TOOL_NAME'" >> "$DEBUG_LOG"
echo "[$TIMESTAMP] Tool Input: '$CLAUDE_TOOL_INPUT'" >> "$DEBUG_LOG"
echo "[$TIMESTAMP] Session ID: '$CLAUDE_SESSION_ID'" >> "$DEBUG_LOG"
echo "[$TIMESTAMP] Transcript: '$CLAUDE_TRANSCRIPT_PATH'" >> "$DEBUG_LOG"
echo "[$TIMESTAMP] Working Dir: $(pwd)" >> "$DEBUG_LOG"
echo "[$TIMESTAMP] Arguments: $*" >> "$DEBUG_LOG"

# Try to read any JSON input
if [ ! -t 0 ]; then
    echo "[$TIMESTAMP] JSON Input from stdin:" >> "$DEBUG_LOG"
    json_input=$(cat)
    echo "[$TIMESTAMP] $json_input" >> "$DEBUG_LOG"
else
    echo "[$TIMESTAMP] No stdin input" >> "$DEBUG_LOG"
fi

echo "[$TIMESTAMP] Environment dump:" >> "$DEBUG_LOG"
env | grep -i claude >> "$DEBUG_LOG" 2>/dev/null || echo "[$TIMESTAMP] No Claude env vars" >> "$DEBUG_LOG"

echo "[$TIMESTAMP] ==================================" >> "$DEBUG_LOG"

# Call the original MCP parameter validator if tool name is provided
if [[ -n "$CLAUDE_TOOL_NAME" ]]; then
    echo "[$TIMESTAMP] Calling MCP parameter validator..." >> "$DEBUG_LOG"
    bash /Users/georgiospilitsoglou/Developer/projects/mypromptflow/meta/mcp-learning/scripts/mcp-parameter-validator.sh "$CLAUDE_SESSION_ID" "$CLAUDE_TRANSCRIPT_PATH" "$CLAUDE_TOOL_NAME" "$CLAUDE_TOOL_INPUT" 2>&1 >> "$DEBUG_LOG"
else
    echo "[$TIMESTAMP] No tool name - returning allow" >> "$DEBUG_LOG"
    echo '{"action": "allow", "reason": "No tool name provided"}'
fi