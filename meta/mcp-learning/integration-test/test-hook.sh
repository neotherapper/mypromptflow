#!/bin/bash
# Simple test hook that logs when called by Claude Code

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
TEST_OUTPUT_FILE="$(dirname "$0")/hook-call-evidence.log"

echo "[$TIMESTAMP] ✅ PreToolUse hook called by Claude Code!" >> "$TEST_OUTPUT_FILE"
echo "[$TIMESTAMP] Hook received JSON input:" >> "$TEST_OUTPUT_FILE"

# Parse JSON input from stdin (Claude Code sends hook data as JSON)
if [ -t 0 ]; then
    # Interactive mode - no stdin
    echo "[$TIMESTAMP] No JSON input received (running in interactive mode)" >> "$TEST_OUTPUT_FILE"
else
    # Read JSON from stdin
    json_input=$(cat)
    echo "[$TIMESTAMP] JSON Input: $json_input" >> "$TEST_OUTPUT_FILE"
    
    # Extract key fields from JSON (simplified parsing)
    session_id=$(echo "$json_input" | grep -o '"session_id":"[^"]*"' | cut -d'"' -f4)
    tool_name=$(echo "$json_input" | grep -o '"tool_name":"[^"]*"' | cut -d'"' -f4)
    
    echo "[$TIMESTAMP] Session ID: $session_id" >> "$TEST_OUTPUT_FILE"
    echo "[$TIMESTAMP] Tool Name: $tool_name" >> "$TEST_OUTPUT_FILE"
fi

echo "[$TIMESTAMP] Arguments: $*" >> "$TEST_OUTPUT_FILE"
echo "[$TIMESTAMP] Working directory: $(pwd)" >> "$TEST_OUTPUT_FILE"
echo "[$TIMESTAMP] Environment:" >> "$TEST_OUTPUT_FILE"
echo "[$TIMESTAMP]   PATH: $PATH" >> "$TEST_OUTPUT_FILE"
echo "" >> "$TEST_OUTPUT_FILE"

# Return allow - don't block any tools during testing
echo '{"action": "allow", "reason": "Integration test - allowing all tools"}'
exit 0