#!/bin/bash

# Universal Topic Intelligence System - Continuous Monitoring Service
# This script starts the automated monitoring in the background

echo "🚀 Starting Universal Topic Intelligence Monitoring Service"
echo "=================================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Check if already running
if [ -f "monitoring.pid" ]; then
    OLD_PID=$(cat monitoring.pid)
    if ps -p $OLD_PID > /dev/null 2>&1; then
        echo "⚠️  Monitoring already running with PID $OLD_PID"
        echo "   Run ./stop_monitoring.sh to stop it first"
        exit 1
    fi
fi

# Start monitoring with specified interval (default 30 minutes)
INTERVAL=${1:-30}

echo "📊 Configuration:"
echo "   - Monitoring interval: $INTERVAL minutes"
echo "   - Log file: monitoring.log"
echo "   - PID file: monitoring.pid"
echo ""

# Start in background and save PID
nohup python auto_monitor.py --interval $INTERVAL > monitoring.log 2>&1 &
MONITOR_PID=$!
echo $MONITOR_PID > monitoring.pid

echo "✅ Monitoring started with PID $MONITOR_PID"
echo "   View logs: tail -f monitoring.log"
echo "   Stop service: ./stop_monitoring.sh"
echo ""
echo "📍 Dashboard available at: http://localhost:5001"

# Also start the dashboard if not running
if ! lsof -ti:5001 > /dev/null 2>&1; then
    echo "🌐 Starting web dashboard..."
    nohup python dashboard_proper.py > dashboard.log 2>&1 &
    DASHBOARD_PID=$!
    echo $DASHBOARD_PID > dashboard.pid
    echo "✅ Dashboard started with PID $DASHBOARD_PID"
else
    echo "📍 Dashboard already running on port 5001"
fi

echo ""
echo "🎯 System is now monitoring Claude and AI news continuously!"