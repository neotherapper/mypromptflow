#!/bin/bash

# Stop the Universal Topic Intelligence Monitoring Service

echo "🛑 Stopping Universal Topic Intelligence Monitoring Service"
echo "=================================================="

# Stop monitoring process
if [ -f "monitoring.pid" ]; then
    PID=$(cat monitoring.pid)
    if ps -p $PID > /dev/null 2>&1; then
        kill $PID
        echo "✅ Stopped monitoring process (PID $PID)"
    else
        echo "⚠️  Monitoring process not running (PID $PID)"
    fi
    rm monitoring.pid
else
    echo "⚠️  No monitoring.pid file found"
fi

# Stop dashboard process
if [ -f "dashboard.pid" ]; then
    PID=$(cat dashboard.pid)
    if ps -p $PID > /dev/null 2>&1; then
        kill $PID
        echo "✅ Stopped dashboard process (PID $PID)"
    else
        echo "⚠️  Dashboard process not running (PID $PID)"
    fi
    rm dashboard.pid
else
    echo "⚠️  No dashboard.pid file found"
fi

# Also check for any processes on port 5001
if lsof -ti:5001 > /dev/null 2>&1; then
    echo "🔍 Found process on port 5001, stopping..."
    lsof -ti:5001 | xargs kill -9 2>/dev/null
    echo "✅ Stopped process on port 5001"
fi

echo ""
echo "🎯 All monitoring services stopped"