#!/bin/bash
# Proper hook following Claude Code documentation

LOG_FILE="/Users/georgiospilitsoglou/Developer/projects/mypromptflow/proper-hook.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Log the execution
echo "[$TIMESTAMP] Hook executed!" >> "$LOG_FILE"
echo "[$TIMESTAMP] Args: $*" >> "$LOG_FILE"
echo "[$TIMESTAMP] PWD: $(pwd)" >> "$LOG_FILE"
echo "[$TIMESTAMP] CLAUDE_PROJECT_DIR: ${CLAUDE_PROJECT_DIR}" >> "$LOG_FILE"

# Read JSON input from stdin if available
if [ ! -t 0 ]; then
    echo "[$TIMESTAMP] Reading stdin..." >> "$LOG_FILE"
    input=$(cat)
    echo "[$TIMESTAMP] Input received: $input" >> "$LOG_FILE"
else
    echo "[$TIMESTAMP] No stdin input" >> "$LOG_FILE"
fi

# Return JSON response for PreToolUse hook
echo '{"continue": true, "permissionDecision": "allow"}'

# Exit successfully
exit 0