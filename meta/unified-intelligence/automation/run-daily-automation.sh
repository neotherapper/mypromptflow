#!/bin/bash
# Daily Intelligence Automation Runner
# Runs the daily automation workflow for the Unified Intelligence System

echo "🚀 Starting Daily Intelligence Automation"
echo "=========================================="

# Change to the unified intelligence directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UNIFIED_INTELLIGENCE_DIR="$(dirname "$SCRIPT_DIR")"

cd "$UNIFIED_INTELLIGENCE_DIR" || {
    echo "❌ Error: Could not change to unified intelligence directory"
    exit 1
}

echo "📁 Working directory: $(pwd)"
echo "⏰ Start time: $(date)"

# Check system health first
echo ""
echo "🏥 Running system health check..."
python3 automation/system-health-monitor.py
HEALTH_STATUS=$?

if [ $HEALTH_STATUS -eq 2 ]; then
    echo "🔴 System health is poor - aborting automation"
    exit 1
elif [ $HEALTH_STATUS -eq 1 ]; then
    echo "🟡 System health is fair - proceeding with caution"
else
    echo "🟢 System health is good - proceeding with automation"
fi

# Run the daily automation
echo ""
echo "🤖 Running daily automation workflow..."
python3 automation/daily-intelligence-automation.py
AUTOMATION_STATUS=$?

# Generate final health report
echo ""
echo "📊 Generating final health report..."
python3 automation/system-health-monitor.py > /dev/null 2>&1

echo ""
echo "⏰ End time: $(date)"

if [ $AUTOMATION_STATUS -eq 0 ]; then
    echo "✅ Daily automation completed successfully!"
    exit 0
else
    echo "❌ Daily automation failed!"
    exit 1
fi