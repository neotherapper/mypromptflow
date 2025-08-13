#!/bin/bash
export FIGMA_API_KEY="FIGMA_TOKEN_REDACTED"
exec npx figma-developer-mcp --figma-api-key="$FIGMA_API_KEY" --stdio