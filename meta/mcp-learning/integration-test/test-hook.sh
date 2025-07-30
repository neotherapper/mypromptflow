#!/bin/bash
# Simple test hook that logs when called by Claude Code

TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
TEST_OUTPUT_FILE="$(dirname "$0")/hook-call-evidence.log"

echo "[$TIMESTAMP] ✅ PreToolUse hook called by Claude Code!" >> "$TEST_OUTPUT_FILE"
echo "[$TIMESTAMP] Arguments received: $*" >> "$TEST_OUTPUT_FILE"
echo "[$TIMESTAMP] Environment variables:" >> "$TEST_OUTPUT_FILE"
echo "[$TIMESTAMP]   CLAUDE_SESSION_ID: $CLAUDE_SESSION_ID" >> "$TEST_OUTPUT_FILE"
echo "[$TIMESTAMP]   CLAUDE_TOOL_NAME: $CLAUDE_TOOL_NAME" >> "$TEST_OUTPUT_FILE"
echo "[$TIMESTAMP]   CLAUDE_TOOL_INPUT: $CLAUDE_TOOL_INPUT" >> "$TEST_OUTPUT_FILE"
echo "[$TIMESTAMP] Working directory: $(pwd)" >> "$TEST_OUTPUT_FILE"
echo "" >> "$TEST_OUTPUT_FILE"

# Return allow - don't block any tools during testing
echo '{"action": "allow", "reason": "Integration test - allowing all tools"}'
