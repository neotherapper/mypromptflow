#!/bin/bash

# Claude Code Hook Integration Test
# Tests if Claude Code actually calls our PreToolUse hooks

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MCP_LEARNING_DIR="$(dirname "$SCRIPT_DIR")"
TEST_OUTPUT_FILE="$SCRIPT_DIR/hook-call-evidence.log"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "🧪 Claude Code Hook Integration Test"
echo "===================================="
echo

# Clear previous test results
> "$TEST_OUTPUT_FILE"

echo "📝 Test Setup:"
echo "- Test Output: $TEST_OUTPUT_FILE"
echo "- MCP Learning Dir: $MCP_LEARNING_DIR"
echo

# Create a simple test hook that logs when called
TEST_HOOK_PATH="$SCRIPT_DIR/test-hook.sh"
cat > "$TEST_HOOK_PATH" << 'EOF'
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
EOF

chmod +x "$TEST_HOOK_PATH"

echo "✅ Created test hook: $TEST_HOOK_PATH"
echo

# Create test Claude Code hooks configuration
CLAUDE_HOOKS_DIR="$SCRIPT_DIR/.claude/hooks"
mkdir -p "$CLAUDE_HOOKS_DIR"

cat > "$CLAUDE_HOOKS_DIR/pre-tool-use.json" << EOF
{
  "name": "Integration Test PreToolUse Hook",
  "matchers": ["*"],
  "command": "$TEST_HOOK_PATH"
}
EOF

echo "✅ Created Claude Code hooks config: $CLAUDE_HOOKS_DIR/pre-tool-use.json"
echo

# Instructions for manual testing
echo "📋 MANUAL TEST INSTRUCTIONS:"
echo "=============================="
echo
echo "1. Copy the hooks configuration to your project:"
echo "   cp -r $CLAUDE_HOOKS_DIR /path/to/your/project/.claude/"
echo
echo "2. Run Claude Code in your project directory"
echo
echo "3. Execute ANY MCP tool call (e.g., use JIRA, Notion, Browser tools)"
echo
echo "4. Check for evidence file: $TEST_OUTPUT_FILE"
echo
echo "5. Run this script again to check results:"
echo "   $0 check"
echo

# Check if this is a results check
if [[ "${1:-}" == "check" ]]; then
    echo "🔍 Checking for hook call evidence..."
    echo
    
    if [[ -f "$TEST_OUTPUT_FILE" ]] && [[ -s "$TEST_OUTPUT_FILE" ]]; then
        echo -e "${GREEN}✅ SUCCESS: Hook was called by Claude Code!${NC}"
        echo
        echo "📋 Evidence found:"
        echo "=================="
        cat "$TEST_OUTPUT_FILE"
        echo
        echo -e "${GREEN}✅ Integration test PASSED${NC}"
        
        # Clean up test files
        echo
        echo "🧹 Cleaning up test files..."
        rm -f "$TEST_HOOK_PATH"
        rm -rf "$CLAUDE_HOOKS_DIR"
        echo "✅ Cleanup complete"
        
    else
        echo -e "${RED}❌ FAILURE: No evidence of hook being called${NC}"
        echo
        echo "Possible reasons:"
        echo "1. Claude Code hooks are not properly configured"
        echo "2. Hook configuration syntax is incorrect"
        echo "3. Claude Code is not using hooks in this project"
        echo "4. No MCP tool calls were made during testing"
        echo
        echo -e "${YELLOW}⚠️  Integration test FAILED${NC}"
        echo
        echo "Troubleshooting:"
        echo "- Verify Claude Code version supports hooks"
        echo "- Check hooks configuration syntax"
        echo "- Ensure hooks directory is in correct location"
        echo "- Try with different MCP tool calls"
    fi
else
    echo "💡 TIP: After testing, run '$0 check' to verify results"
fi

echo
echo "🏁 Test setup complete!"