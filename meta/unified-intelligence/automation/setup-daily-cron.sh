#!/bin/bash
# Setup Daily Cron Job for Unified Intelligence System
# Configures automated daily execution of the intelligence automation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
AUTOMATION_SCRIPT="$SCRIPT_DIR/run-daily-automation.sh"
LOG_FILE="$SCRIPT_DIR/cron-automation.log"

echo "⚙️ Setting up Daily Intelligence Automation Cron Job"
echo "=================================================="

# Check if the automation script exists
if [ ! -f "$AUTOMATION_SCRIPT" ]; then
    echo "❌ Error: Automation script not found at $AUTOMATION_SCRIPT"
    exit 1
fi

# Make sure the script is executable
chmod +x "$AUTOMATION_SCRIPT"

# Create cron job entry
CRON_ENTRY="0 8 * * * $AUTOMATION_SCRIPT >> $LOG_FILE 2>&1"

echo "📝 Cron job configuration:"
echo "   Script: $AUTOMATION_SCRIPT"
echo "   Schedule: Daily at 8:00 AM"
echo "   Log file: $LOG_FILE"
echo "   Entry: $CRON_ENTRY"

# Check if cron job already exists
existing_cron=$(crontab -l 2>/dev/null | grep -F "$AUTOMATION_SCRIPT")

if [ -n "$existing_cron" ]; then
    echo ""
    echo "⚠️ Existing cron job found:"
    echo "   $existing_cron"
    echo ""
    read -p "Do you want to replace it? (y/N): " -n 1 -r
    echo
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "❌ Cron job setup cancelled"
        exit 1
    fi
    
    # Remove existing cron job
    crontab -l 2>/dev/null | grep -v -F "$AUTOMATION_SCRIPT" | crontab -
    echo "🗑️ Removed existing cron job"
fi

# Add new cron job
(crontab -l 2>/dev/null; echo "$CRON_ENTRY") | crontab -

if [ $? -eq 0 ]; then
    echo "✅ Cron job installed successfully!"
    echo ""
    echo "📅 The Unified Intelligence System will now run daily at 8:00 AM"
    echo "📄 Check logs at: $LOG_FILE"
    echo ""
    echo "🔧 To verify installation, run: crontab -l | grep intelligence"
    echo "🗑️ To remove, run: crontab -l | grep -v '$AUTOMATION_SCRIPT' | crontab -"
else
    echo "❌ Error: Failed to install cron job"
    exit 1
fi

# Create initial log file
touch "$LOG_FILE"
echo "$(date): Cron job installed for Unified Intelligence System" >> "$LOG_FILE"

echo ""
echo "🎉 Daily automation setup complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Monitor logs: tail -f $LOG_FILE"
echo "   2. Check system health: python3 automation/system-health-monitor.py" 
echo "   3. Run manual test: ./automation/run-daily-automation.sh"