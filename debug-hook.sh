#!/bin/bash
# Minimal debug hook to test if hooks are working

DEBUG_LOG="/Users/georgiospilitsoglou/Developer/projects/mypromptflow/hook-debug.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$TIMESTAMP] 🚀 DEBUG HOOK CALLED!" >> "$DEBUG_LOG"
echo "[$TIMESTAMP] Tool: $CLAUDE_TOOL_NAME" >> "$DEBUG_LOG"
echo "[$TIMESTAMP] Args: $*" >> "$DEBUG_LOG"
echo "[$TIMESTAMP] Working Dir: $(pwd)" >> "$DEBUG_LOG"
echo "[$TIMESTAMP] Input Data:" >> "$DEBUG_LOG"

# Try to read any input data
if [ ! -t 0 ]; then
    cat >> "$DEBUG_LOG" 2>/dev/null || echo "[$TIMESTAMP] No stdin data" >> "$DEBUG_LOG"
fi

echo "[$TIMESTAMP] ===================" >> "$DEBUG_LOG"

# Return allow to not block anything
echo '{"action": "allow", "reason": "Debug hook test"}'
exit 0