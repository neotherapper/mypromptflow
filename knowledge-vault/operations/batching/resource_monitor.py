#!/usr/bin/env python3
"""
Resource Monitor for Intelligent Batching System
Monitors system resources and provides real-time metrics for adaptive batching decisions.
"""

import asyncio
import time
import psutil
import logging
from typing import Dict, List, Optional, Callable, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import threading
from concurrent.futures import ThreadPoolExecutor
import json
import yaml
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SystemResources:
    """System resource usage metrics"""
    cpu_percent: float = 0.0
    memory_percent: float = 0.0
    memory_available_mb: float = 0.0
    disk_usage_percent: float = 0.0
    network_bytes_sent: int = 0
    network_bytes_received: int = 0
    active_connections: int = 0
    load_average: List[float] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)

@dataclass
class ApplicationMetrics:
    """Application-specific performance metrics"""
    active_requests: int = 0
    request_queue_size: int = 0
    average_response_time: float = 0.0
    error_rate: float = 0.0
    throughput: float = 0.0  # requests per second
    api_rate_limit_remaining: int = 1000
    database_connection_pool_usage: float = 0.0
    cache_hit_rate: float = 0.0
    timestamp: float = field(default_factory=time.time)

@dataclass
class ResourceThresholds:
    """Configurable resource thresholds for scaling decisions"""
    cpu_warning: float = 70.0
    cpu_critical: float = 85.0
    memory_warning: float = 75.0
    memory_critical: float = 90.0
    disk_warning: float = 80.0
    disk_critical: float = 95.0
    network_warning_mbps: float = 100.0
    network_critical_mbps: float = 500.0
    load_average_warning: float = 2.0
    load_average_critical: float = 4.0

class ResourceMonitor:
    """
    Comprehensive resource monitoring system that tracks system and application
    metrics for intelligent batching decisions.
    """
    
    def __init__(self, config_path: Optional[str] = None, monitoring_interval: float = 5.0):
        """Initialize the resource monitor"""
        self.monitoring_interval = monitoring_interval
        self.thresholds = self._load_thresholds(config_path)
        self.system_history: List[SystemResources] = []
        self.app_history: List[ApplicationMetrics] = []
        self.monitoring_active = False
        self.monitoring_thread: Optional[threading.Thread] = None
        self.callbacks: List[Callable[[SystemResources, ApplicationMetrics], None]] = []
        self.alert_callbacks: List[Callable[[str, str, Dict[str, Any]], None]] = []
        
        # Performance tracking
        self.baseline_metrics: Optional[SystemResources] = None
        self.peak_usage_tracking: Dict[str, float] = {}
        self.performance_degradation_alerts: List[Dict[str, Any]] = []
        
        # Network monitoring state
        self.last_network_stats = None
        self.network_speed_history: List[float] = []
        
    def _load_thresholds(self, config_path: Optional[str]) -> ResourceThresholds:
        """Load resource thresholds from configuration file"""
        if config_path and Path(config_path).exists():
            try:
                with open(config_path, 'r') as f:
                    config_data = yaml.safe_load(f)
                thresholds_data = config_data.get('resource_thresholds', {})
                return ResourceThresholds(**thresholds_data)
            except Exception as e:
                logger.warning(f"Failed to load thresholds from {config_path}: {e}")
        
        return ResourceThresholds()
    
    def start_monitoring(self):
        """Start continuous resource monitoring"""
        if self.monitoring_active:
            logger.warning("Monitoring is already active")
            return
        
        self.monitoring_active = True
        self.monitoring_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitoring_thread.start()
        logger.info(f"Resource monitoring started with {self.monitoring_interval}s interval")
    
    def stop_monitoring(self):
        """Stop resource monitoring"""
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=10)
        logger.info("Resource monitoring stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Collect system and application metrics
                system_metrics = self._collect_system_metrics()
                app_metrics = self._collect_application_metrics()
                
                # Store in history
                self._update_history(system_metrics, app_metrics)
                
                # Check thresholds and trigger alerts
                self._check_thresholds(system_metrics, app_metrics)
                
                # Notify callbacks
                for callback in self.callbacks:
                    try:
                        callback(system_metrics, app_metrics)
                    except Exception as e:
                        logger.error(f"Callback error: {e}")
                
                time.sleep(self.monitoring_interval)
                
            except Exception as e:
                logger.error(f"Monitoring loop error: {e}")
                time.sleep(self.monitoring_interval)
    
    def _collect_system_metrics(self) -> SystemResources:
        """Collect comprehensive system resource metrics"""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Memory metrics
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_available_mb = memory.available / (1024 * 1024)
            
            # Disk metrics
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            
            # Network metrics
            network_stats = psutil.net_io_counters()
            network_bytes_sent = network_stats.bytes_sent
            network_bytes_recv = network_stats.bytes_recv
            
            # Connection metrics
            try:
                connections = psutil.net_connections()
                active_connections = len([c for c in connections if c.status == 'ESTABLISHED'])
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                active_connections = 0
            
            # Load average (Unix/Linux systems)
            try:
                load_avg = list(psutil.getloadavg())
            except (AttributeError, OSError):
                load_avg = [0.0, 0.0, 0.0]
            
            return SystemResources(
                cpu_percent=cpu_percent,
                memory_percent=memory_percent,
                memory_available_mb=memory_available_mb,
                disk_usage_percent=disk_percent,
                network_bytes_sent=network_bytes_sent,
                network_bytes_received=network_bytes_recv,
                active_connections=active_connections,
                load_average=load_avg
            )
            
        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")
            return SystemResources()
    
    def _collect_application_metrics(self) -> ApplicationMetrics:
        """Collect application-specific metrics"""
        # This would be implemented based on specific application metrics
        # For now, return placeholder values
        return ApplicationMetrics(
            active_requests=0,
            request_queue_size=0,
            average_response_time=0.0,
            error_rate=0.0,
            throughput=0.0,
            api_rate_limit_remaining=1000,
            database_connection_pool_usage=0.0,
            cache_hit_rate=0.9
        )
    
    def _update_history(self, system_metrics: SystemResources, app_metrics: ApplicationMetrics):
        """Update metrics history with retention limits"""
        # Add new metrics
        self.system_history.append(system_metrics)
        self.app_history.append(app_metrics)
        
        # Keep only recent history (last 1000 measurements)
        if len(self.system_history) > 1000:
            self.system_history = self.system_history[-1000:]
        if len(self.app_history) > 1000:
            self.app_history = self.app_history[-1000:]
        
        # Update baseline if not set
        if self.baseline_metrics is None and len(self.system_history) >= 10:
            self.baseline_metrics = self._calculate_baseline()
        
        # Track peak usage
        self._update_peak_tracking(system_metrics)
        
        # Calculate network speed
        self._calculate_network_speed(system_metrics)
    
    def _check_thresholds(self, system_metrics: SystemResources, app_metrics: ApplicationMetrics):
        """Check resource thresholds and trigger alerts"""
        alerts = []
        
        # CPU threshold checks
        if system_metrics.cpu_percent >= self.thresholds.cpu_critical:
            alerts.append(("critical", "cpu", {
                "current": system_metrics.cpu_percent,
                "threshold": self.thresholds.cpu_critical,
                "message": f"Critical CPU usage: {system_metrics.cpu_percent:.1f}%"
            }))
        elif system_metrics.cpu_percent >= self.thresholds.cpu_warning:
            alerts.append(("warning", "cpu", {
                "current": system_metrics.cpu_percent,
                "threshold": self.thresholds.cpu_warning,
                "message": f"High CPU usage: {system_metrics.cpu_percent:.1f}%"
            }))
        
        # Memory threshold checks
        if system_metrics.memory_percent >= self.thresholds.memory_critical:
            alerts.append(("critical", "memory", {
                "current": system_metrics.memory_percent,
                "threshold": self.thresholds.memory_critical,
                "message": f"Critical memory usage: {system_metrics.memory_percent:.1f}%"
            }))
        elif system_metrics.memory_percent >= self.thresholds.memory_warning:
            alerts.append(("warning", "memory", {
                "current": system_metrics.memory_percent,
                "threshold": self.thresholds.memory_warning,
                "message": f"High memory usage: {system_metrics.memory_percent:.1f}%"
            }))
        
        # Disk threshold checks
        if system_metrics.disk_usage_percent >= self.thresholds.disk_critical:
            alerts.append(("critical", "disk", {
                "current": system_metrics.disk_usage_percent,
                "threshold": self.thresholds.disk_critical,
                "message": f"Critical disk usage: {system_metrics.disk_usage_percent:.1f}%"
            }))
        elif system_metrics.disk_usage_percent >= self.thresholds.disk_warning:
            alerts.append(("warning", "disk", {
                "current": system_metrics.disk_usage_percent,
                "threshold": self.thresholds.disk_warning,
                "message": f"High disk usage: {system_metrics.disk_usage_percent:.1f}%"
            }))
        
        # Load average checks (if available)
        if system_metrics.load_average and len(system_metrics.load_average) > 0:
            load_1min = system_metrics.load_average[0]
            if load_1min >= self.thresholds.load_average_critical:
                alerts.append(("critical", "load", {
                    "current": load_1min,
                    "threshold": self.thresholds.load_average_critical,
                    "message": f"Critical system load: {load_1min:.2f}"
                }))
            elif load_1min >= self.thresholds.load_average_warning:
                alerts.append(("warning", "load", {
                    "current": load_1min,
                    "threshold": self.thresholds.load_average_warning,
                    "message": f"High system load: {load_1min:.2f}"
                }))
        
        # Trigger alert callbacks
        for level, resource_type, details in alerts:
            for callback in self.alert_callbacks:
                try:
                    callback(level, resource_type, details)
                except Exception as e:
                    logger.error(f"Alert callback error: {e}")
    
    def _calculate_baseline(self) -> SystemResources:
        """Calculate baseline metrics from recent history"""
        if len(self.system_history) < 10:
            return SystemResources()
        
        recent_metrics = self.system_history[-10:]
        
        return SystemResources(
            cpu_percent=sum(m.cpu_percent for m in recent_metrics) / len(recent_metrics),
            memory_percent=sum(m.memory_percent for m in recent_metrics) / len(recent_metrics),
            memory_available_mb=sum(m.memory_available_mb for m in recent_metrics) / len(recent_metrics),
            disk_usage_percent=sum(m.disk_usage_percent for m in recent_metrics) / len(recent_metrics),
            active_connections=sum(m.active_connections for m in recent_metrics) / len(recent_metrics)
        )
    
    def _update_peak_tracking(self, metrics: SystemResources):
        """Track peak resource usage"""
        self.peak_usage_tracking['cpu'] = max(
            self.peak_usage_tracking.get('cpu', 0), metrics.cpu_percent
        )
        self.peak_usage_tracking['memory'] = max(
            self.peak_usage_tracking.get('memory', 0), metrics.memory_percent
        )
        self.peak_usage_tracking['disk'] = max(
            self.peak_usage_tracking.get('disk', 0), metrics.disk_usage_percent
        )
    
    def _calculate_network_speed(self, metrics: SystemResources):
        """Calculate network speed from metrics"""
        if self.last_network_stats is None:
            self.last_network_stats = metrics
            return
        
        time_diff = metrics.timestamp - self.last_network_stats.timestamp
        if time_diff <= 0:
            return
        
        bytes_sent_diff = metrics.network_bytes_sent - self.last_network_stats.network_bytes_sent
        bytes_recv_diff = metrics.network_bytes_received - self.last_network_stats.network_bytes_received
        
        # Calculate speed in Mbps
        total_bytes = bytes_sent_diff + bytes_recv_diff
        speed_mbps = (total_bytes * 8) / (time_diff * 1024 * 1024)
        
        self.network_speed_history.append(speed_mbps)
        if len(self.network_speed_history) > 100:
            self.network_speed_history = self.network_speed_history[-100:]
        
        self.last_network_stats = metrics
    
    def get_current_metrics(self) -> Dict[str, Any]:
        """Get current system and application metrics"""
        if not self.system_history or not self.app_history:
            return {
                'system': SystemResources().__dict__,
                'application': ApplicationMetrics().__dict__,
                'network_speed_mbps': 0.0,
                'monitoring_active': self.monitoring_active
            }
        
        latest_system = self.system_history[-1]
        latest_app = self.app_history[-1]
        
        return {
            'system': latest_system.__dict__,
            'application': latest_app.__dict__,
            'network_speed_mbps': self.network_speed_history[-1] if self.network_speed_history else 0.0,
            'monitoring_active': self.monitoring_active,
            'peak_usage': self.peak_usage_tracking.copy(),
            'baseline': self.baseline_metrics.__dict__ if self.baseline_metrics else None
        }
    
    def get_resource_availability(self) -> Dict[str, float]:
        """Calculate available resource capacity (0-1 scale)"""
        if not self.system_history:
            return {'cpu': 1.0, 'memory': 1.0, 'disk': 1.0, 'network': 1.0}
        
        latest = self.system_history[-1]
        
        return {
            'cpu': max(0, (100 - latest.cpu_percent) / 100),
            'memory': max(0, (100 - latest.memory_percent) / 100),
            'disk': max(0, (100 - latest.disk_usage_percent) / 100),
            'network': max(0, 1 - (self.network_speed_history[-1] / self.thresholds.network_critical_mbps 
                                  if self.network_speed_history else 0))
        }
    
    def get_performance_trend(self, window_minutes: int = 5) -> Dict[str, str]:
        """Analyze performance trend over specified time window"""
        if len(self.system_history) < 2:
            return {'cpu': 'stable', 'memory': 'stable', 'disk': 'stable'}
        
        cutoff_time = time.time() - (window_minutes * 60)
        recent_metrics = [m for m in self.system_history if m.timestamp >= cutoff_time]
        
        if len(recent_metrics) < 2:
            return {'cpu': 'stable', 'memory': 'stable', 'disk': 'stable'}
        
        # Calculate trends
        trends = {}
        for metric in ['cpu_percent', 'memory_percent', 'disk_usage_percent']:
            values = [getattr(m, metric) for m in recent_metrics]
            if len(values) < 2:
                trends[metric.replace('_percent', '')] = 'stable'
                continue
            
            # Simple trend analysis
            first_half = values[:len(values)//2]
            second_half = values[len(values)//2:]
            
            first_avg = sum(first_half) / len(first_half)
            second_avg = sum(second_half) / len(second_half)
            
            if second_avg > first_avg + 5:
                trends[metric.replace('_percent', '')] = 'increasing'
            elif second_avg < first_avg - 5:
                trends[metric.replace('_percent', '')] = 'decreasing'
            else:
                trends[metric.replace('_percent', '')] = 'stable'
        
        return trends
    
    def register_callback(self, callback: Callable[[SystemResources, ApplicationMetrics], None]):
        """Register callback for metric updates"""
        self.callbacks.append(callback)
    
    def register_alert_callback(self, callback: Callable[[str, str, Dict[str, Any]], None]):
        """Register callback for resource alerts"""
        self.alert_callbacks.append(callback)
    
    def predict_resource_exhaustion(self) -> Dict[str, Optional[float]]:
        """Predict when resources might be exhausted based on current trends"""
        if len(self.system_history) < 10:
            return {'cpu': None, 'memory': None, 'disk': None}
        
        predictions = {}
        recent_metrics = self.system_history[-10:]
        
        for resource in ['cpu_percent', 'memory_percent', 'disk_usage_percent']:
            values = [getattr(m, resource) for m in recent_metrics]
            timestamps = [m.timestamp for m in recent_metrics]
            
            # Simple linear regression for trend prediction
            if len(values) >= 3:
                # Calculate rate of change
                time_diffs = [timestamps[i] - timestamps[i-1] for i in range(1, len(timestamps))]
                value_diffs = [values[i] - values[i-1] for i in range(1, len(values))]
                
                if time_diffs and all(td > 0 for td in time_diffs):
                    avg_rate = sum(vd / td for vd, td in zip(value_diffs, time_diffs)) / len(value_diffs)
                    
                    current_value = values[-1]
                    critical_threshold = getattr(self.thresholds, 
                                                f"{resource.replace('_percent', '')}_critical")
                    
                    if avg_rate > 0:
                        time_to_critical = (critical_threshold - current_value) / avg_rate
                        predictions[resource.replace('_percent', '')] = time_to_critical if time_to_critical > 0 else None
                    else:
                        predictions[resource.replace('_percent', '')] = None
                else:
                    predictions[resource.replace('_percent', '')] = None
            else:
                predictions[resource.replace('_percent', '')] = None
        
        return predictions
    
    def get_optimization_recommendations(self) -> List[Dict[str, str]]:
        """Get recommendations for resource optimization"""
        recommendations = []
        
        if not self.system_history:
            return recommendations
        
        latest = self.system_history[-1]
        
        # CPU recommendations
        if latest.cpu_percent > self.thresholds.cpu_warning:
            recommendations.append({
                'type': 'cpu',
                'severity': 'high' if latest.cpu_percent > self.thresholds.cpu_critical else 'medium',
                'recommendation': 'Reduce batch sizes and implement request throttling',
                'details': f'Current CPU usage: {latest.cpu_percent:.1f}%'
            })
        
        # Memory recommendations
        if latest.memory_percent > self.thresholds.memory_warning:
            recommendations.append({
                'type': 'memory',
                'severity': 'high' if latest.memory_percent > self.thresholds.memory_critical else 'medium',
                'recommendation': 'Implement memory-efficient batching and increase garbage collection frequency',
                'details': f'Current memory usage: {latest.memory_percent:.1f}%'
            })
        
        # Disk recommendations
        if latest.disk_usage_percent > self.thresholds.disk_warning:
            recommendations.append({
                'type': 'disk',
                'severity': 'high' if latest.disk_usage_percent > self.thresholds.disk_critical else 'medium',
                'recommendation': 'Clean up temporary files and implement log rotation',
                'details': f'Current disk usage: {latest.disk_usage_percent:.1f}%'
            })
        
        # Network recommendations
        if self.network_speed_history:
            avg_speed = sum(self.network_speed_history[-10:]) / len(self.network_speed_history[-10:])
            if avg_speed > self.thresholds.network_warning_mbps:
                recommendations.append({
                    'type': 'network',
                    'severity': 'high' if avg_speed > self.thresholds.network_critical_mbps else 'medium',
                    'recommendation': 'Implement request queuing and optimize data transfer sizes',
                    'details': f'Average network speed: {avg_speed:.1f} Mbps'
                })
        
        return recommendations
    
    def export_metrics(self, filepath: str, format: str = 'json'):
        """Export metrics history to file"""
        try:
            data = {
                'system_metrics': [m.__dict__ for m in self.system_history],
                'application_metrics': [m.__dict__ for m in self.app_history],
                'peak_usage': self.peak_usage_tracking,
                'baseline': self.baseline_metrics.__dict__ if self.baseline_metrics else None,
                'export_timestamp': time.time()
            }
            
            with open(filepath, 'w') as f:
                if format.lower() == 'json':
                    json.dump(data, f, indent=2)
                elif format.lower() == 'yaml':
                    yaml.dump(data, f, default_flow_style=False)
                else:
                    raise ValueError(f"Unsupported format: {format}")
            
            logger.info(f"Metrics exported to {filepath}")
            
        except Exception as e:
            logger.error(f"Failed to export metrics: {e}")

# Factory function
def create_resource_monitor(config_path: Optional[str] = None, 
                           monitoring_interval: float = 5.0) -> ResourceMonitor:
    """Create and configure a resource monitor"""
    return ResourceMonitor(config_path, monitoring_interval)

if __name__ == "__main__":
    # Example usage
    monitor = create_resource_monitor()
    
    def metrics_callback(sys_metrics, app_metrics):
        print(f"CPU: {sys_metrics.cpu_percent:.1f}%, Memory: {sys_metrics.memory_percent:.1f}%")
    
    def alert_callback(level, resource_type, details):
        print(f"ALERT [{level}] {resource_type}: {details['message']}")
    
    monitor.register_callback(metrics_callback)
    monitor.register_alert_callback(alert_callback)
    
    try:
        monitor.start_monitoring()
        time.sleep(30)  # Monitor for 30 seconds
        
        # Get current status
        metrics = monitor.get_current_metrics()
        print("\nCurrent Metrics:", json.dumps(metrics, indent=2))
        
        # Get recommendations
        recommendations = monitor.get_optimization_recommendations()
        print("\nRecommendations:")
        for rec in recommendations:
            print(f"  {rec['type']}: {rec['recommendation']}")
            
    finally:
        monitor.stop_monitoring()