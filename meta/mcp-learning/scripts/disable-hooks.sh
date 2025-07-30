#!/bin/bash

# MCP Error Detection Hook Disable Script
# Simple rollback mechanism to disable the hooks if needed

SETTINGS_FILE=".claude/settings.json"
BACKUP_FILE=".claude/settings.json.backup"

if [[ ! -f "$SETTINGS_FILE" ]]; then
    echo "Error: Settings file not found at $SETTINGS_FILE"
    exit 1
fi

# Create backup
cp "$SETTINGS_FILE" "$BACKUP_FILE"
echo "Created backup at $BACKUP_FILE"

# Remove hooks section using jq if available, otherwise use sed
if command -v jq >/dev/null 2>&1; then
    jq 'del(.hooks)' "$SETTINGS_FILE" > "${SETTINGS_FILE}.tmp" && mv "${SETTINGS_FILE}.tmp" "$SETTINGS_FILE"
    echo "Hooks disabled using jq"
else
    # Simple sed-based removal (less robust but works)
    sed -i.bak '/  "hooks": {/,/  }/d' "$SETTINGS_FILE"
    echo "Hooks disabled using sed"
fi

echo "MCP error detection hooks have been disabled."
echo "To restore, run: cp $BACKUP_FILE $SETTINGS_FILE"