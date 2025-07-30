#!/bin/bash
# Simple test hook based on documentation examples

# Log the hook call
echo "$(date): Simple hook called with args: $*" >> /Users/georgiospilitsoglou/Developer/projects/mypromptflow/simple-hook.log

# Check environment variables
echo "$(date): CLAUDE_PROJECT_DIR=${CLAUDE_PROJECT_DIR}" >> /Users/georgiospilitsoglou/Developer/projects/mypromptflow/simple-hook.log
echo "$(date): PWD=$(pwd)" >> /Users/georgiospilitsoglou/Developer/projects/mypromptflow/simple-hook.log

# Read stdin if available
if [ ! -t 0 ]; then
    echo "$(date): Received stdin data:" >> /Users/georgiospilitsoglou/Developer/projects/mypromptflow/simple-hook.log
    cat >> /Users/georgiospilitsoglou/Developer/projects/mypromptflow/simple-hook.log
fi

# Return success (no blocking)
exit 0