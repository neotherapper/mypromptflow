#!/usr/bin/env python3
"""
Knowledge Vault Progress Monitoring System
Enterprise-grade progress tracking with real-time metrics and comprehensive logging
Production-ready monitoring for migration operations
"""

import os
import sys
import json
import time
import threading
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from contextlib import contextmanager
import psutil
import queue

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
LOGS_PATH = Path(__file__).parent.parent / 'logs'

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class ProgressMetrics:
    """Progress metrics for monitoring"""
    timestamp: str
    total_items: int
    completed_items: int
    failed_items: int
    completion_percentage: float
    items_per_second: float
    estimated_time_remaining: Optional[float]
    current_operation: str
    memory_usage_mb: float
    cpu_usage_percent: float
    errors_count: int
    warnings_count: int
    
@dataclass
class PerformanceSnapshot:
    """Performance snapshot for analysis"""
    timestamp: str
    operation_type: str
    operation_duration: float
    memory_before_mb: float
    memory_after_mb: float
    memory_delta_mb: float
    items_processed: int
    errors_encountered: int
    api_calls_made: int
    api_response_time_avg: float

@dataclass
class MigrationSession:
    """Migration session tracking"""
    session_id: str
    start_time: str
    end_time: Optional[str]
    total_duration: Optional[float]
    status: str  # 'running', 'completed', 'failed', 'cancelled'
    total_items_planned: int
    items_completed: int
    items_failed: int
    databases_processed: List[str]
    performance_metrics: Dict[str, Any]
    error_summary: Dict[str, int]
    checkpoints: List[Dict]

class ProgressMonitor:
    """Comprehensive progress monitoring system"""
    
    def __init__(self, session_id: str = None, log_level: str = 'INFO'):
        self.session_id = session_id or f"migration_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.start_time = datetime.now()
        self.is_monitoring = False
        self.metrics_queue = queue.Queue()
        self.monitor_thread = None
        
        # Progress tracking
        self.total_items = 0
        self.completed_items = 0
        self.failed_items = 0
        self.current_operation = "Initializing"
        self.operation_start_time = None
        
        # Performance tracking
        self.performance_snapshots = []
        self.error_counts = {}
        self.warning_counts = {}
        self.api_call_times = []
        self.checkpoints = []
        
        # Session tracking
        self.session = MigrationSession(
            session_id=self.session_id,
            start_time=self.start_time.isoformat(),
            end_time=None,
            total_duration=None,
            status='running',
            total_items_planned=0,
            items_completed=0,
            items_failed=0,
            databases_processed=[],
            performance_metrics={},
            error_summary={},
            checkpoints=[]
        )
        
        # Create logs directory
        LOGS_PATH.mkdir(exist_ok=True)
        
        # Set up detailed logging
        self._setup_logging(log_level)
        
        logger.info(f"Progress monitor initialized for session: {self.session_id}")
        
    def _setup_logging(self, log_level: str):
        """Set up detailed logging for the session"""
        # Create session-specific log file
        session_log_path = LOGS_PATH / f"session_{self.session_id}.log"
        
        # Create file handler for session logs
        file_handler = logging.FileHandler(session_log_path)
        file_handler.setLevel(getattr(logging, log_level.upper()))
        
        # Create detailed formatter
        detailed_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s'
        )
        file_handler.setFormatter(detailed_formatter)
        
        # Add handler to logger
        logger.addHandler(file_handler)
        
        # Create progress metrics log file
        self.metrics_log_path = LOGS_PATH / f"metrics_{self.session_id}.jsonl"
        
    def start_monitoring(self, total_items: int = 0):
        """Start progress monitoring"""
        self.total_items = total_items
        self.session.total_items_planned = total_items
        self.is_monitoring = True
        
        # Start monitoring thread
        self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitor_thread.start()
        
        logger.info(f"Progress monitoring started for {total_items} items")
        
    def stop_monitoring(self):
        """Stop progress monitoring"""
        self.is_monitoring = False
        self.session.status = 'completed'
        self.session.end_time = datetime.now().isoformat()
        self.session.total_duration = (datetime.now() - self.start_time).total_seconds()
        
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
            
        # Final metrics collection
        self._collect_final_metrics()
        
        # Save session summary
        self._save_session_summary()
        
        logger.info("Progress monitoring stopped")
        
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.is_monitoring:
            try:
                # Collect current metrics
                metrics = self._collect_current_metrics()
                
                # Log metrics to file
                self._log_metrics(metrics)
                
                # Check for alerts
                self._check_performance_alerts(metrics)
                
                # Sleep for monitoring interval
                time.sleep(2)  # Collect metrics every 2 seconds
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                
    def _collect_current_metrics(self) -> ProgressMetrics:
        """Collect current progress metrics"""
        current_time = datetime.now()
        elapsed_time = (current_time - self.start_time).total_seconds()
        
        # Calculate completion percentage
        completion_percentage = (self.completed_items / self.total_items * 100) if self.total_items > 0 else 0
        
        # Calculate items per second
        items_per_second = self.completed_items / elapsed_time if elapsed_time > 0 else 0
        
        # Estimate time remaining
        remaining_items = self.total_items - self.completed_items
        estimated_time_remaining = remaining_items / items_per_second if items_per_second > 0 else None
        
        # Get system metrics
        memory_usage = psutil.virtual_memory().used / (1024 * 1024)  # MB
        cpu_usage = psutil.cpu_percent()
        
        # Count errors and warnings
        total_errors = sum(self.error_counts.values())
        total_warnings = sum(self.warning_counts.values())
        
        metrics = ProgressMetrics(
            timestamp=current_time.isoformat(),
            total_items=self.total_items,
            completed_items=self.completed_items,
            failed_items=self.failed_items,
            completion_percentage=completion_percentage,
            items_per_second=items_per_second,
            estimated_time_remaining=estimated_time_remaining,
            current_operation=self.current_operation,
            memory_usage_mb=memory_usage,
            cpu_usage_percent=cpu_usage,
            errors_count=total_errors,
            warnings_count=total_warnings
        )
        
        return metrics
        
    def _log_metrics(self, metrics: ProgressMetrics):
        """Log metrics to file"""
        try:
            with open(self.metrics_log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(asdict(metrics)) + '\n')
        except Exception as e:
            logger.error(f"Error logging metrics: {e}")
            
    def _check_performance_alerts(self, metrics: ProgressMetrics):
        """Check for performance alerts"""
        # Memory usage alert
        if metrics.memory_usage_mb > 1000:  # 1GB
            logger.warning(f"High memory usage: {metrics.memory_usage_mb:.1f}MB")
            
        # CPU usage alert
        if metrics.cpu_usage_percent > 80:
            logger.warning(f"High CPU usage: {metrics.cpu_usage_percent:.1f}%")
            
        # Error rate alert
        if metrics.errors_count > metrics.completed_items * 0.05:  # 5% error rate
            logger.warning(f"High error rate: {metrics.errors_count} errors out of {metrics.completed_items} items")
            
        # Slow progress alert
        if metrics.items_per_second < 0.1 and metrics.completed_items > 10:  # Less than 1 item per 10 seconds
            logger.warning(f"Slow progress: {metrics.items_per_second:.3f} items per second")
            
    def update_progress(self, operation: str, completed: int = None, failed: int = None):
        """Update progress information"""
        if completed is not None:
            self.completed_items = completed
            self.session.items_completed = completed
            
        if failed is not None:
            self.failed_items = failed
            self.session.items_failed = failed
            
        if operation != self.current_operation:
            if self.operation_start_time:
                # Log operation completion
                operation_duration = (datetime.now() - self.operation_start_time).total_seconds()
                logger.info(f"Operation '{self.current_operation}' completed in {operation_duration:.2f}s")
                
            self.current_operation = operation
            self.operation_start_time = datetime.now()
            logger.info(f"Started operation: {operation}")
            
    def increment_completed(self, count: int = 1):
        """Increment completed items count"""
        self.completed_items += count
        self.session.items_completed = self.completed_items
        
    def increment_failed(self, count: int = 1):
        """Increment failed items count"""
        self.failed_items += count
        self.session.items_failed = self.failed_items
        
    def log_error(self, error_type: str, error_message: str):
        """Log an error occurrence"""
        if error_type not in self.error_counts:
            self.error_counts[error_type] = 0
        self.error_counts[error_type] += 1
        
        logger.error(f"[{error_type}] {error_message}")
        
    def log_warning(self, warning_type: str, warning_message: str):
        """Log a warning occurrence"""
        if warning_type not in self.warning_counts:
            self.warning_counts[warning_type] = 0
        self.warning_counts[warning_type] += 1
        
        logger.warning(f"[{warning_type}] {warning_message}")
        
    def log_api_call(self, duration: float, success: bool = True):
        """Log API call performance"""
        self.api_call_times.append({
            'timestamp': datetime.now().isoformat(),
            'duration': duration,
            'success': success
        })
        
        # Keep only last 100 API calls for memory efficiency
        if len(self.api_call_times) > 100:
            self.api_call_times = self.api_call_times[-100:]
            
    def create_checkpoint(self, name: str, data: Dict = None):
        """Create a progress checkpoint"""
        checkpoint = {
            'timestamp': datetime.now().isoformat(),
            'name': name,
            'completed_items': self.completed_items,
            'failed_items': self.failed_items,
            'current_operation': self.current_operation,
            'data': data or {}
        }
        
        self.checkpoints.append(checkpoint)
        self.session.checkpoints = self.checkpoints
        
        logger.info(f"Checkpoint created: {name}")
        
    @contextmanager
    def operation_timer(self, operation_name: str):
        """Context manager for timing operations"""
        start_time = time.time()
        start_memory = psutil.virtual_memory().used / (1024 * 1024)
        
        self.update_progress(operation_name)
        
        try:
            yield
        except Exception as e:
            self.log_error(f"{operation_name}_error", str(e))
            raise
        finally:
            end_time = time.time()
            end_memory = psutil.virtual_memory().used / (1024 * 1024)
            duration = end_time - start_time
            
            # Create performance snapshot
            snapshot = PerformanceSnapshot(
                timestamp=datetime.now().isoformat(),
                operation_type=operation_name,
                operation_duration=duration,
                memory_before_mb=start_memory,
                memory_after_mb=end_memory,
                memory_delta_mb=end_memory - start_memory,
                items_processed=1,  # Can be overridden
                errors_encountered=0,  # Can be tracked separately
                api_calls_made=0,  # Can be tracked separately
                api_response_time_avg=0  # Can be calculated from recent API calls
            )
            
            self.performance_snapshots.append(snapshot)
            
            logger.debug(f"Operation '{operation_name}' took {duration:.3f}s")
            
    def get_current_status(self) -> Dict:
        """Get current status summary"""
        current_time = datetime.now()
        elapsed_time = (current_time - self.start_time).total_seconds()
        
        completion_percentage = (self.completed_items / self.total_items * 100) if self.total_items > 0 else 0
        items_per_second = self.completed_items / elapsed_time if elapsed_time > 0 else 0
        
        remaining_items = self.total_items - self.completed_items - self.failed_items
        eta_seconds = remaining_items / items_per_second if items_per_second > 0 else None
        eta_human = str(timedelta(seconds=int(eta_seconds))) if eta_seconds else "Unknown"
        
        return {
            'session_id': self.session_id,
            'status': self.session.status,
            'current_operation': self.current_operation,
            'progress': {
                'total_items': self.total_items,
                'completed': self.completed_items,
                'failed': self.failed_items,
                'remaining': remaining_items,
                'completion_percentage': round(completion_percentage, 2),
                'items_per_second': round(items_per_second, 3)
            },
            'timing': {
                'elapsed_time': elapsed_time,
                'elapsed_human': str(timedelta(seconds=int(elapsed_time))),
                'eta_seconds': eta_seconds,
                'eta_human': eta_human
            },
            'performance': {
                'memory_usage_mb': psutil.virtual_memory().used / (1024 * 1024),
                'cpu_usage_percent': psutil.cpu_percent(),
                'total_errors': sum(self.error_counts.values()),
                'total_warnings': sum(self.warning_counts.values())
            },
            'recent_api_performance': self._get_recent_api_performance()
        }
        
    def _get_recent_api_performance(self) -> Dict:
        """Get recent API performance metrics"""
        if not self.api_call_times:
            return {'calls': 0, 'avg_duration': 0, 'success_rate': 0}
            
        recent_calls = [call for call in self.api_call_times 
                       if (datetime.now() - datetime.fromisoformat(call['timestamp'])).total_seconds() < 300]  # Last 5 minutes
        
        if not recent_calls:
            return {'calls': 0, 'avg_duration': 0, 'success_rate': 0}
            
        avg_duration = sum(call['duration'] for call in recent_calls) / len(recent_calls)
        success_count = sum(1 for call in recent_calls if call['success'])
        success_rate = (success_count / len(recent_calls)) * 100
        
        return {
            'calls': len(recent_calls),
            'avg_duration': round(avg_duration, 3),
            'success_rate': round(success_rate, 2)
        }
        
    def _collect_final_metrics(self):
        """Collect final session metrics"""
        final_metrics = self._collect_current_metrics()
        
        # Calculate final performance metrics
        total_duration = (datetime.now() - self.start_time).total_seconds()
        overall_throughput = self.completed_items / total_duration if total_duration > 0 else 0
        
        # API performance summary
        if self.api_call_times:
            avg_api_time = sum(call['duration'] for call in self.api_call_times) / len(self.api_call_times)
            successful_calls = sum(1 for call in self.api_call_times if call['success'])
            api_success_rate = (successful_calls / len(self.api_call_times)) * 100
        else:
            avg_api_time = 0
            api_success_rate = 0
            
        self.session.performance_metrics = {
            'total_duration_seconds': total_duration,
            'overall_throughput_items_per_second': overall_throughput,
            'completion_rate_percent': (self.completed_items / self.total_items * 100) if self.total_items > 0 else 0,
            'failure_rate_percent': (self.failed_items / self.total_items * 100) if self.total_items > 0 else 0,
            'avg_api_response_time_seconds': avg_api_time,
            'api_success_rate_percent': api_success_rate,
            'total_api_calls': len(self.api_call_times),
            'peak_memory_usage_mb': max((snapshot.memory_after_mb for snapshot in self.performance_snapshots), default=0),
            'checkpoints_created': len(self.checkpoints)
        }
        
        self.session.error_summary = dict(self.error_counts)
        
    def _save_session_summary(self):
        """Save complete session summary"""
        session_file = LOGS_PATH / f"session_summary_{self.session_id}.json"
        
        try:
            with open(session_file, 'w', encoding='utf-8') as f:
                session_dict = asdict(self.session)
                # Add performance snapshots
                session_dict['performance_snapshots'] = [asdict(snapshot) for snapshot in self.performance_snapshots]
                # Add API call history
                session_dict['api_call_history'] = self.api_call_times
                
                json.dump(session_dict, f, indent=2, default=str)
                
            logger.info(f"Session summary saved to: {session_file}")
            
        except Exception as e:
            logger.error(f"Error saving session summary: {e}")
            
    def print_progress_report(self):
        """Print a formatted progress report"""
        status = self.get_current_status()
        
        print("\n" + "="*60)
        print(f"MIGRATION PROGRESS REPORT - {status['session_id']}")
        print("="*60)
        print(f"Status: {status['status'].upper()}")
        print(f"Current Operation: {status['current_operation']}")
        print()
        print(f"Progress: {status['progress']['completed']}/{status['progress']['total_items']} items")
        print(f"Completion: {status['progress']['completion_percentage']:.1f}%")
        print(f"Failed: {status['progress']['failed']} items")
        print(f"Speed: {status['progress']['items_per_second']:.2f} items/second")
        print()
        print(f"Elapsed Time: {status['timing']['elapsed_human']}")
        print(f"Estimated Time Remaining: {status['timing']['eta_human']}")
        print()
        print(f"Memory Usage: {status['performance']['memory_usage_mb']:.1f} MB")
        print(f"CPU Usage: {status['performance']['cpu_usage_percent']:.1f}%")
        print(f"Errors: {status['performance']['total_errors']}")
        print(f"Warnings: {status['performance']['total_warnings']}")
        
        if status['recent_api_performance']['calls'] > 0:
            print()
            print(f"API Performance (last 5 min):")
            print(f"  Calls: {status['recent_api_performance']['calls']}")
            print(f"  Avg Response Time: {status['recent_api_performance']['avg_duration']:.3f}s")
            print(f"  Success Rate: {status['recent_api_performance']['success_rate']:.1f}%")
        
        print("="*60)

# Context manager for easy monitoring
@contextmanager
def progress_monitor(session_id: str = None, total_items: int = 0, print_final_report: bool = True):
    """Context manager for progress monitoring"""
    monitor = ProgressMonitor(session_id)
    
    try:
        monitor.start_monitoring(total_items)
        yield monitor
    except Exception as e:
        monitor.log_error("migration_error", str(e))
        monitor.session.status = 'failed'
        raise
    finally:
        monitor.stop_monitoring()
        if print_final_report:
            monitor.print_progress_report()

def main():
    """Demo/test function"""
    import time
    import random
    
    # Demo progress monitoring
    with progress_monitor("demo_session", total_items=50) as monitor:
        
        for i in range(50):
            # Simulate work
            with monitor.operation_timer(f"processing_item_{i+1}"):
                # Simulate API call
                api_start = time.time()
                time.sleep(random.uniform(0.1, 0.5))  # Simulate work
                api_duration = time.time() - api_start
                monitor.log_api_call(api_duration, success=random.random() > 0.1)
                
                # Simulate occasional errors
                if random.random() < 0.05:  # 5% error rate
                    monitor.log_error("processing_error", f"Failed to process item {i+1}")
                    monitor.increment_failed()
                else:
                    monitor.increment_completed()
                
                # Create checkpoints every 10 items
                if (i + 1) % 10 == 0:
                    monitor.create_checkpoint(f"checkpoint_{i+1}", {"items_processed": i+1})
                    
            # Print progress every 10 items
            if (i + 1) % 10 == 0:
                monitor.print_progress_report()

if __name__ == '__main__':
    main()