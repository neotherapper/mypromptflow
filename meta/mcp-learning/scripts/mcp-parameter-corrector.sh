#!/bin/bash

# MCP Parameter Corrector
# Applies learned corrections to MCP tool parameters

# Handle input - either from stdin or as second argument
TOOL_NAME="$1"
if [ -n "$2" ]; then
    # Input provided as argument
    tool_input="$2"
else
    # Read tool input from stdin
    read -r tool_input
fi

# Apply corrections based on tool type and learned patterns
case "$TOOL_NAME" in
    "mcp__MCP_DOCKER__jira_get_issue"|"mcp__MCP_DOCKER__jira_update_issue")
        # Fix common issue_key format problems
        corrected=$(echo "$tool_input" | sed 's/"issue_key": *"PROJ\([0-9]\+\)"/"issue_key": "PROJ-\1"/g')
        corrected=$(echo "$corrected" | sed 's/"issue_key": *"\([A-Z]*\)\([0-9]*\)"/"issue_key": "\1-\2"/g')
        echo "$corrected"
        ;;
    "mcp__MCP_DOCKER__jira_create_issue")
        # Ensure project_key is uppercase and properly formatted
        corrected=$(echo "$tool_input" | sed 's/"project_key": *"\([a-z]\+\)"/"project_key": "\U\1"/g')
        echo "$corrected"
        ;;
    *)
        # No corrections needed for unknown tools
        echo "$tool_input"
        ;;
esac