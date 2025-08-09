#!/usr/bin/env python3
"""
Orchestrator Dashboard and Monitoring System
Web-based dashboard for monitoring and controlling the Automated Discovery Orchestrator
"""

import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional
import asyncio
from dataclasses import asdict
import subprocess
import time

# Flask for web dashboard
try:
    from flask import Flask, render_template, jsonify, request, redirect, url_for
    from flask_socketio import SocketIO, emit
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    Flask = None

# Import orchestrator for direct control
from automated_discovery_orchestrator import AutomatedDiscoveryOrchestrator, SystemStatus, TaskStatus, TaskPriority

logger = logging.getLogger(__name__)

class OrchestratorDashboard:
    """Web-based dashboard for orchestrator monitoring and control"""
    
    def __init__(self, orchestrator_path: Optional[Path] = None):
        self.base_path = orchestrator_path or Path(__file__).parent
        self.orchestrator = AutomatedDiscoveryOrchestrator()
        
        if not FLASK_AVAILABLE:
            logger.error("Flask not available - install with: pip install flask flask-socketio")
            sys.exit(1)
        
        # Initialize Flask app
        self.app = Flask(__name__, template_folder='dashboard/templates', static_folder='dashboard/static')
        self.app.config['SECRET_KEY'] = 'orchestrator-dashboard-secret'
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        
        # Setup routes
        self._setup_routes()
        self._setup_socket_events()
        
        # Real-time monitoring
        self.monitoring_active = False
        self.last_metrics = {}
    
    def _setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def dashboard():
            """Main dashboard page"""
            status = self.orchestrator.get_status()
            return render_template('dashboard.html', status=status)
        
        @self.app.route('/api/status')
        def api_status():
            """API endpoint for current status"""
            return jsonify(self.orchestrator.get_status())
        
        @self.app.route('/api/tasks')
        def api_tasks():
            """API endpoint for task information"""
            tasks_info = {}
            for task_id, task in self.orchestrator.tasks.items():
                tasks_info[task_id] = {
                    'task_id': task.task_id,
                    'name': task.name,
                    'status': task.status.value,
                    'priority': task.priority.value,
                    'enabled': task.enabled,
                    'last_run': task.last_run.isoformat() if task.last_run else None,
                    'next_run': task.next_run.isoformat() if task.next_run else None,
                    'retry_count': task.retry_count,
                    'error_message': task.error_message,
                    'execution_stats': task.execution_stats
                }
            return jsonify(tasks_info)
        
        @self.app.route('/api/task/<task_id>/toggle', methods=['POST'])
        def api_toggle_task(task_id):
            """Toggle task enabled/disabled"""
            if task_id not in self.orchestrator.tasks:
                return jsonify({'error': 'Task not found'}), 404
            
            task = self.orchestrator.tasks[task_id]
            if task.enabled:
                success = self.orchestrator.disable_task(task_id)
                action = 'disabled'
            else:
                success = self.orchestrator.enable_task(task_id)
                action = 'enabled'
            
            return jsonify({
                'success': success,
                'action': action,
                'task_id': task_id
            })
        
        @self.app.route('/api/task/<task_id>/run', methods=['POST'])
        def api_run_task(task_id):
            """Force run a specific task"""
            if task_id not in self.orchestrator.tasks:
                return jsonify({'error': 'Task not found'}), 404
            
            success, result = self.orchestrator.force_run_task(task_id)
            return jsonify({
                'success': success,
                'result': result,
                'task_id': task_id
            })
        
        @self.app.route('/api/metrics/history')
        def api_metrics_history():
            """Get historical metrics"""
            # Load historical data from files
            metrics_history = []
            
            # Look for historical metric files
            for file_path in self.base_path.glob("system-report-*.json"):
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        metrics_history.append({
                            'timestamp': data['timestamp'],
                            'metrics': data['metrics'],
                            'resource_status': data.get('resource_status', {}),
                            'tasks_today': data.get('tasks_today', {})
                        })
                except Exception as e:
                    logger.warning(f"Failed to load metrics from {file_path}: {e}")
            
            # Sort by timestamp
            metrics_history.sort(key=lambda x: x['timestamp'])
            
            return jsonify(metrics_history)
        
        @self.app.route('/api/logs')
        def api_logs():
            """Get recent log entries"""
            log_file = self.base_path / "orchestrator.log"
            if not log_file.exists():
                log_file = self.base_path / "automated-discovery-orchestrator.log"
            
            if not log_file.exists():
                return jsonify({'logs': []})
            
            try:
                # Get last 100 lines
                with open(log_file, 'r') as f:
                    lines = f.readlines()
                    recent_lines = lines[-100:] if len(lines) > 100 else lines
                    
                logs = []
                for line in recent_lines:
                    line = line.strip()
                    if line:
                        logs.append(line)
                        
                return jsonify({'logs': logs})
                
            except Exception as e:
                return jsonify({'error': f'Failed to read logs: {e}'})
        
        @self.app.route('/api/control/start', methods=['POST'])
        def api_start_orchestrator():
            """Start orchestrator in continuous mode"""
            try:
                # Check if already running
                if self._is_orchestrator_running():
                    return jsonify({'error': 'Orchestrator is already running'})
                
                # Start orchestrator process
                subprocess.Popen([
                    sys.executable, 
                    str(self.base_path / "automated-discovery-orchestrator.py"),
                    "--mode", "continuous"
                ], cwd=self.base_path)
                
                return jsonify({'success': True, 'message': 'Orchestrator started'})
                
            except Exception as e:
                return jsonify({'error': f'Failed to start orchestrator: {e}'})
        
        @self.app.route('/api/control/stop', methods=['POST'])
        def api_stop_orchestrator():
            """Stop orchestrator"""
            try:
                subprocess.run([
                    "pkill", "-f", "automated-discovery-orchestrator.py"
                ], capture_output=True)
                
                return jsonify({'success': True, 'message': 'Orchestrator stopped'})
                
            except Exception as e:
                return jsonify({'error': f'Failed to stop orchestrator: {e}'})
        
        @self.app.route('/api/control/restart', methods=['POST'])
        def api_restart_orchestrator():
            """Restart orchestrator"""
            try:
                # Stop first
                subprocess.run([
                    "pkill", "-f", "automated-discovery-orchestrator.py"
                ], capture_output=True)
                
                time.sleep(2)  # Wait for process to stop
                
                # Start again
                subprocess.Popen([
                    sys.executable,
                    str(self.base_path / "automated-discovery-orchestrator.py"),
                    "--mode", "continuous"
                ], cwd=self.base_path)
                
                return jsonify({'success': True, 'message': 'Orchestrator restarted'})
                
            except Exception as e:
                return jsonify({'error': f'Failed to restart orchestrator: {e}'})
    
    def _setup_socket_events(self):
        """Setup Socket.IO events for real-time updates"""
        
        @self.socketio.on('connect')
        def handle_connect():
            logger.info("Client connected to dashboard")
            emit('status', self.orchestrator.get_status())
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            logger.info("Client disconnected from dashboard")
        
        @self.socketio.on('request_status')
        def handle_status_request():
            emit('status', self.orchestrator.get_status())
        
        @self.socketio.on('start_monitoring')
        def handle_start_monitoring():
            self.monitoring_active = True
            self._start_real_time_monitoring()
        
        @self.socketio.on('stop_monitoring')
        def handle_stop_monitoring():
            self.monitoring_active = False
    
    def _is_orchestrator_running(self) -> bool:
        """Check if orchestrator is currently running"""
        try:
            result = subprocess.run([
                "pgrep", "-f", "automated-discovery-orchestrator.py"
            ], capture_output=True, text=True)
            
            return result.returncode == 0 and bool(result.stdout.strip())
            
        except Exception:
            return False
    
    def _start_real_time_monitoring(self):
        """Start real-time monitoring and emit updates"""
        def monitor():
            while self.monitoring_active:
                try:
                    current_status = self.orchestrator.get_status()
                    
                    # Check if status changed significantly
                    if self._status_changed(current_status):
                        self.socketio.emit('status_update', current_status)
                        self.last_metrics = current_status
                    
                    time.sleep(10)  # Update every 10 seconds
                    
                except Exception as e:
                    logger.error(f"Monitoring error: {e}")
                    time.sleep(30)  # Wait longer on error
        
        # Run monitoring in background thread
        import threading
        monitor_thread = threading.Thread(target=monitor, daemon=True)
        monitor_thread.start()
    
    def _status_changed(self, current_status: Dict[str, Any]) -> bool:
        """Check if status changed significantly from last update"""
        if not self.last_metrics:
            return True
        
        # Check key metrics for changes
        key_metrics = [
            'active_tasks',
            'completed_tasks_today',
            'failed_tasks_today',
            'cpu_usage',
            'memory_usage'
        ]
        
        current_metrics = current_status.get('metrics', {})
        last_metrics = self.last_metrics.get('metrics', {})
        
        for metric in key_metrics:
            if abs(current_metrics.get(metric, 0) - last_metrics.get(metric, 0)) > 0.1:
                return True
        
        # Check task status changes
        current_tasks = current_status.get('task_status_summary', {})
        last_tasks = self.last_metrics.get('task_status_summary', {})
        
        if current_tasks != last_tasks:
            return True
        
        return False
    
    def create_dashboard_templates(self):
        """Create HTML templates for the dashboard"""
        templates_dir = self.base_path / "dashboard" / "templates"
        static_dir = self.base_path / "dashboard" / "static"
        
        templates_dir.mkdir(parents=True, exist_ok=True)
        static_dir.mkdir(parents=True, exist_ok=True)
        
        # Main dashboard template
        dashboard_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Discovery Orchestrator Dashboard</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .metrics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin-bottom: 20px; }
        .metric-card { background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .metric-value { font-size: 2em; font-weight: bold; color: #3498db; }
        .tasks-section { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .task-item { display: flex; justify-content: between; align-items: center; padding: 10px; border-bottom: 1px solid #eee; }
        .task-status { padding: 4px 8px; border-radius: 4px; color: white; font-size: 0.8em; }
        .status-completed { background: #27ae60; }
        .status-running { background: #f39c12; }
        .status-failed { background: #e74c3c; }
        .status-pending { background: #95a5a6; }
        .controls { background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .btn { padding: 10px 20px; margin: 5px; border: none; border-radius: 4px; cursor: pointer; }
        .btn-primary { background: #3498db; color: white; }
        .btn-success { background: #27ae60; color: white; }
        .btn-danger { background: #e74c3c; color: white; }
        .logs-section { background: white; padding: 20px; border-radius: 8px; }
        .log-entry { font-family: monospace; font-size: 0.9em; padding: 2px 0; }
        .chart-container { width: 100%; height: 300px; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🚀 Discovery Orchestrator Dashboard</h1>
        <div id="system-status">System Status: <span id="status-indicator">Loading...</span></div>
    </div>

    <div class="controls">
        <h3>System Controls</h3>
        <button class="btn btn-success" onclick="startOrchestrator()">Start Orchestrator</button>
        <button class="btn btn-danger" onclick="stopOrchestrator()">Stop Orchestrator</button>
        <button class="btn btn-primary" onclick="restartOrchestrator()">Restart Orchestrator</button>
        <button class="btn btn-primary" onclick="refreshStatus()">Refresh Status</button>
    </div>

    <div class="metrics-grid">
        <div class="metric-card">
            <h3>CPU Usage</h3>
            <div class="metric-value" id="cpu-usage">0%</div>
        </div>
        <div class="metric-card">
            <h3>Memory Usage</h3>
            <div class="metric-value" id="memory-usage">0%</div>
        </div>
        <div class="metric-card">
            <h3>Active Tasks</h3>
            <div class="metric-value" id="active-tasks">0</div>
        </div>
        <div class="metric-card">
            <h3>Completed Today</h3>
            <div class="metric-value" id="completed-tasks">0</div>
        </div>
        <div class="metric-card">
            <h3>Failed Today</h3>
            <div class="metric-value" id="failed-tasks">0</div>
        </div>
        <div class="metric-card">
            <h3>Error Rate</h3>
            <div class="metric-value" id="error-rate">0%</div>
        </div>
    </div>

    <div class="tasks-section">
        <h3>Discovery Tasks</h3>
        <div id="tasks-list">Loading tasks...</div>
    </div>

    <div class="chart-container">
        <canvas id="metrics-chart"></canvas>
    </div>

    <div class="logs-section">
        <h3>Recent Logs</h3>
        <div id="logs-container" style="max-height: 400px; overflow-y: auto;">
            Loading logs...
        </div>
    </div>

    <script>
        const socket = io();
        let metricsChart;

        // Initialize chart
        const ctx = document.getElementById('metrics-chart').getContext('2d');
        metricsChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: [],
                datasets: [{
                    label: 'CPU Usage (%)',
                    data: [],
                    borderColor: 'rgb(255, 99, 132)',
                    tension: 0.1
                }, {
                    label: 'Memory Usage (%)',
                    data: [],
                    borderColor: 'rgb(54, 162, 235)',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: { beginAtZero: true, max: 100 }
                }
            }
        });

        // Socket event handlers
        socket.on('connect', function() {
            console.log('Connected to orchestrator dashboard');
            socket.emit('start_monitoring');
        });

        socket.on('status', function(status) {
            updateStatus(status);
        });

        socket.on('status_update', function(status) {
            updateStatus(status);
        });

        function updateStatus(status) {
            // Update metrics
            const metrics = status.metrics;
            document.getElementById('cpu-usage').textContent = metrics.cpu_usage.toFixed(1) + '%';
            document.getElementById('memory-usage').textContent = metrics.memory_usage.toFixed(1) + '%';
            document.getElementById('active-tasks').textContent = metrics.active_tasks;
            document.getElementById('completed-tasks').textContent = metrics.completed_tasks_today;
            document.getElementById('failed-tasks').textContent = metrics.failed_tasks_today;
            document.getElementById('error-rate').textContent = (metrics.error_rate * 100).toFixed(1) + '%';
            
            // Update system status
            document.getElementById('status-indicator').textContent = status.system_status;
            
            // Update chart
            const now = new Date().toLocaleTimeString();
            metricsChart.data.labels.push(now);
            metricsChart.data.datasets[0].data.push(metrics.cpu_usage);
            metricsChart.data.datasets[1].data.push(metrics.memory_usage);
            
            // Keep only last 20 data points
            if (metricsChart.data.labels.length > 20) {
                metricsChart.data.labels.shift();
                metricsChart.data.datasets[0].data.shift();
                metricsChart.data.datasets[1].data.shift();
            }
            
            metricsChart.update();
        }

        // Control functions
        function startOrchestrator() {
            fetch('/api/control/start', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Orchestrator started successfully');
                    } else {
                        alert('Error: ' + data.error);
                    }
                });
        }

        function stopOrchestrator() {
            fetch('/api/control/stop', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Orchestrator stopped successfully');
                    } else {
                        alert('Error: ' + data.error);
                    }
                });
        }

        function restartOrchestrator() {
            fetch('/api/control/restart', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Orchestrator restarted successfully');
                    } else {
                        alert('Error: ' + data.error);
                    }
                });
        }

        function refreshStatus() {
            socket.emit('request_status');
            loadTasks();
            loadLogs();
        }

        // Load tasks
        function loadTasks() {
            fetch('/api/tasks')
                .then(response => response.json())
                .then(tasks => {
                    const tasksHtml = Object.values(tasks).map(task => `
                        <div class="task-item">
                            <div>
                                <h4>${task.name}</h4>
                                <p>Status: <span class="task-status status-${task.status}">${task.status}</span></p>
                                <p>Last Run: ${task.last_run ? new Date(task.last_run).toLocaleString() : 'Never'}</p>
                                <p>Next Run: ${task.next_run ? new Date(task.next_run).toLocaleString() : 'Not scheduled'}</p>
                            </div>
                            <div>
                                <button class="btn btn-primary" onclick="runTask('${task.task_id}')">Run Now</button>
                                <button class="btn ${task.enabled ? 'btn-danger' : 'btn-success'}" 
                                        onclick="toggleTask('${task.task_id}')">
                                    ${task.enabled ? 'Disable' : 'Enable'}
                                </button>
                            </div>
                        </div>
                    `).join('');
                    document.getElementById('tasks-list').innerHTML = tasksHtml;
                });
        }

        // Load logs
        function loadLogs() {
            fetch('/api/logs')
                .then(response => response.json())
                .then(data => {
                    if (data.logs) {
                        const logsHtml = data.logs.map(log => 
                            `<div class="log-entry">${log}</div>`
                        ).join('');
                        document.getElementById('logs-container').innerHTML = logsHtml;
                        // Scroll to bottom
                        const container = document.getElementById('logs-container');
                        container.scrollTop = container.scrollHeight;
                    }
                });
        }

        function runTask(taskId) {
            fetch(`/api/task/${taskId}/run`, { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert(`Task ${taskId} started successfully`);
                        refreshStatus();
                    } else {
                        alert('Error: ' + JSON.stringify(data.result));
                    }
                });
        }

        function toggleTask(taskId) {
            fetch(`/api/task/${taskId}/toggle`, { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert(`Task ${taskId} ${data.action} successfully`);
                        loadTasks();
                    } else {
                        alert('Error: ' + data.error);
                    }
                });
        }

        // Initial load
        loadTasks();
        loadLogs();
        
        // Refresh data periodically
        setInterval(() => {
            loadTasks();
            loadLogs();
        }, 30000); // Every 30 seconds
    </script>
</body>
</html>"""
        
        with open(templates_dir / "dashboard.html", "w") as f:
            f.write(dashboard_html)
        
        logger.info("✅ Dashboard templates created")
    
    def run(self, host='127.0.0.1', port=5000, debug=False):
        """Run the dashboard server"""
        # Create templates if they don't exist
        self.create_dashboard_templates()
        
        logger.info(f"🌐 Starting dashboard server at http://{host}:{port}")
        self.socketio.run(self.app, host=host, port=port, debug=debug)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Orchestrator Dashboard")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=5000, help="Port to bind to")
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    parser.add_argument("--orchestrator-path", type=Path, help="Path to orchestrator")
    
    args = parser.parse_args()
    
    dashboard = OrchestratorDashboard(orchestrator_path=args.orchestrator_path)
    dashboard.run(host=args.host, port=args.port, debug=args.debug)

if __name__ == "__main__":
    main()