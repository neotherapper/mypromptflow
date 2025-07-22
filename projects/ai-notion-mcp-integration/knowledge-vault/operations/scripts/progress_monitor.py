#!/usr/bin/env python3
"""
Progress Monitoring and Logging Script
AI INSTRUCTIONS: This script provides comprehensive progress monitoring and logging for migration operations

Purpose: Real-time progress tracking with detailed metrics and logging
Target: Enterprise-ready monitoring with comprehensive audit trails
"""

import os
import sys
import json
import yaml
import time
import logging
import argparse
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import queue
from contextlib import contextmanager

class OperationStatus(Enum):
    PENDING = "pending"
    STARTING = "starting"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"

@dataclass
class ProgressMetrics:
    """Progress metrics for operations"""
    operation_id: str
    operation_name: str
    total_items: int
    completed_items: int
    failed_items: int
    skipped_items: int
    start_time: datetime
    last_update_time: datetime
    estimated_completion_time: Optional[datetime] = None
    current_phase: str = "initializing"
    status: OperationStatus = OperationStatus.PENDING
    error_count: int = 0
    warning_count: int = 0
    performance_metrics: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.performance_metrics is None:
            self.performance_metrics = {}
    
    @property
    def progress_percentage(self) -> float:
        """Calculate progress percentage"""
        if self.total_items == 0:
            return 0.0
        return (self.completed_items / self.total_items) * 100
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate"""
        processed = self.completed_items + self.failed_items
        if processed == 0:
            return 0.0
        return (self.completed_items / processed) * 100
    
    @property
    def items_per_second(self) -> float:
        """Calculate processing rate"""
        elapsed = (self.last_update_time - self.start_time).total_seconds()
        if elapsed <= 0:
            return 0.0
        return (self.completed_items + self.failed_items) / elapsed
    
    @property
    def estimated_time_remaining(self) -> Optional[timedelta]:
        """Estimate time remaining"""
        if self.items_per_second <= 0:
            return None
        remaining_items = self.total_items - self.completed_items - self.failed_items
        if remaining_items <= 0:
            return timedelta(0)
        return timedelta(seconds=remaining_items / self.items_per_second)

@dataclass
class LogEntry:
    """Single log entry"""
    timestamp: datetime
    level: LogLevel
    operation_id: str
    phase: str
    message: str
    details: Optional[Dict[str, Any]] = None
    exception: Optional[str] = None

class ProgressMonitor:
    """Comprehensive progress monitoring system"""
    
    def __init__(self, log_dir: Path = Path("operations/logs")):
        self.log_dir = log_dir
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Progress tracking
        self.operations = {}
        self.log_entries = queue.Queue()
        
        # Logging setup
        self.logger = self._setup_logger()
        
        # Background thread for log processing
        self.log_thread = threading.Thread(target=self._process_log_entries, daemon=True)
        self.log_thread.start()
        
        # Performance monitoring
        self.performance_history = {}
        
    def _setup_logger(self) -> logging.Logger:
        """Setup comprehensive logging configuration"""
        logger = logging.getLogger('progress_monitor')
        logger.setLevel(logging.DEBUG)
        
        # Remove existing handlers to avoid duplicates
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # Console handler for INFO and above
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)8s | %(message)s',
            datefmt='%H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        # File handler for all levels
        log_file = self.log_dir / "progress_monitor.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s | %(levelname)8s | %(name)s | %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        # JSON handler for structured logging
        json_log_file = self.log_dir / "progress_monitor.json"
        self.json_log_file = json_log_file
        
        return logger
    
    def _process_log_entries(self):
        """Background thread to process log entries"""
        json_logs = []
        last_flush = time.time()
        
        while True:
            try:
                # Get log entry with timeout
                try:
                    entry = self.log_entries.get(timeout=1.0)
                except queue.Empty:
                    # Flush logs every 5 seconds
                    if time.time() - last_flush > 5.0:
                        self._flush_json_logs(json_logs)
                        json_logs = []
                        last_flush = time.time()
                    continue
                
                # Convert to JSON format
                json_entry = {
                    "timestamp": entry.timestamp.isoformat(),
                    "level": entry.level.value,
                    "operation_id": entry.operation_id,
                    "phase": entry.phase,
                    "message": entry.message
                }
                
                if entry.details:
                    json_entry["details"] = entry.details
                if entry.exception:
                    json_entry["exception"] = entry.exception
                    
                json_logs.append(json_entry)
                
                # Flush periodically or when queue is empty
                if len(json_logs) >= 100 or self.log_entries.empty():
                    self._flush_json_logs(json_logs)
                    json_logs = []
                    last_flush = time.time()
                    
            except Exception as e:
                # Log to stderr to avoid infinite loops
                print(f"Error in log processing thread: {e}", file=sys.stderr)
    
    def _flush_json_logs(self, json_logs: List[Dict[str, Any]]):
        """Flush JSON logs to file"""
        if not json_logs:
            return
            
        try:
            # Append to JSON log file
            with open(self.json_log_file, 'a', encoding='utf-8') as f:
                for entry in json_logs:
                    f.write(json.dumps(entry) + '\n')
        except Exception as e:
            print(f"Error writing JSON logs: {e}", file=sys.stderr)
    
    def start_operation(self, 
                       operation_id: str, 
                       operation_name: str, 
                       total_items: int,
                       phases: List[str] = None) -> ProgressMetrics:
        """Start tracking a new operation"""
        
        metrics = ProgressMetrics(
            operation_id=operation_id,
            operation_name=operation_name,
            total_items=total_items,
            completed_items=0,
            failed_items=0,
            skipped_items=0,
            start_time=datetime.now(timezone.utc),
            last_update_time=datetime.now(timezone.utc),
            current_phase="starting",
            status=OperationStatus.STARTING
        )
        
        self.operations[operation_id] = metrics
        
        # Initialize performance history
        self.performance_history[operation_id] = {
            "phases": phases or ["main"],
            "phase_timings": {},
            "item_processing_times": [],
            "error_history": [],
            "checkpoint_history": []
        }
        
        self.log(operation_id, LogLevel.INFO, "starting", 
                f"Started operation '{operation_name}' with {total_items} items")
        
        return metrics
    
    def update_progress(self, 
                       operation_id: str,
                       completed_delta: int = 0,
                       failed_delta: int = 0,
                       skipped_delta: int = 0,
                       current_phase: str = None,
                       details: Dict[str, Any] = None):
        """Update operation progress"""
        
        if operation_id not in self.operations:
            raise ValueError(f"Operation {operation_id} not found")
        
        metrics = self.operations[operation_id]
        
        # Update counters
        metrics.completed_items += completed_delta
        metrics.failed_items += failed_delta
        metrics.skipped_items += skipped_delta
        metrics.last_update_time = datetime.now(timezone.utc)
        
        # Update phase if provided
        if current_phase and current_phase != metrics.current_phase:
            self._record_phase_transition(operation_id, metrics.current_phase, current_phase)
            metrics.current_phase = current_phase
        
        # Update status based on progress
        if metrics.completed_items + metrics.failed_items >= metrics.total_items:
            metrics.status = OperationStatus.COMPLETED
        elif metrics.status == OperationStatus.STARTING:
            metrics.status = OperationStatus.IN_PROGRESS
        
        # Calculate estimated completion time
        if metrics.items_per_second > 0:
            remaining_time = metrics.estimated_time_remaining
            if remaining_time:
                metrics.estimated_completion_time = datetime.now(timezone.utc) + remaining_time
        
        # Update performance metrics
        metrics.performance_metrics.update({
            "items_per_second": metrics.items_per_second,
            "success_rate": metrics.success_rate,
            "progress_percentage": metrics.progress_percentage,
            "estimated_completion": metrics.estimated_completion_time.isoformat() if metrics.estimated_completion_time else None
        })
        
        # Log progress update
        self.log(operation_id, LogLevel.INFO, metrics.current_phase,
                f"Progress: {metrics.progress_percentage:.1f}% ({metrics.completed_items}/{metrics.total_items})",
                details=details)
    
    def _record_phase_transition(self, operation_id: str, from_phase: str, to_phase: str):
        """Record phase transition timing"""
        history = self.performance_history[operation_id]
        current_time = datetime.now(timezone.utc)
        
        # Record end time for previous phase
        if from_phase in history["phase_timings"]:
            history["phase_timings"][from_phase]["end_time"] = current_time
            start_time = history["phase_timings"][from_phase]["start_time"]
            duration = (current_time - start_time).total_seconds()
            history["phase_timings"][from_phase]["duration_seconds"] = duration
        
        # Record start time for new phase
        history["phase_timings"][to_phase] = {
            "start_time": current_time,
            "end_time": None,
            "duration_seconds": None
        }
        
        self.log(operation_id, LogLevel.INFO, "phase_transition",
                f"Phase transition: {from_phase} -> {to_phase}")
    
    def log(self, 
           operation_id: str,
           level: LogLevel, 
           phase: str,
           message: str,
           details: Dict[str, Any] = None,
           exception: Exception = None):
        """Log a message for an operation"""
        
        # Update error/warning counts
        if operation_id in self.operations:
            metrics = self.operations[operation_id]
            if level == LogLevel.ERROR or level == LogLevel.CRITICAL:
                metrics.error_count += 1
            elif level == LogLevel.WARNING:
                metrics.warning_count += 1
        
        # Create log entry
        entry = LogEntry(
            timestamp=datetime.now(timezone.utc),
            level=level,
            operation_id=operation_id,
            phase=phase,
            message=message,
            details=details,
            exception=str(exception) if exception else None
        )
        
        # Add to queue for background processing
        self.log_entries.put(entry)
        
        # Log to Python logger
        log_message = f"[{operation_id}:{phase}] {message}"
        if details:
            log_message += f" | {details}"
            
        if level == LogLevel.DEBUG:
            self.logger.debug(log_message)
        elif level == LogLevel.INFO:
            self.logger.info(log_message)
        elif level == LogLevel.WARNING:
            self.logger.warning(log_message)
        elif level == LogLevel.ERROR:
            self.logger.error(log_message)
        elif level == LogLevel.CRITICAL:
            self.logger.critical(log_message)
    
    def create_checkpoint(self, operation_id: str, checkpoint_name: str, data: Dict[str, Any] = None):
        """Create a progress checkpoint"""
        if operation_id not in self.operations:
            return
        
        metrics = self.operations[operation_id]
        checkpoint = {
            "name": checkpoint_name,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "completed_items": metrics.completed_items,
            "failed_items": metrics.failed_items,
            "current_phase": metrics.current_phase,
            "data": data or {}
        }
        
        # Save checkpoint to history
        self.performance_history[operation_id]["checkpoint_history"].append(checkpoint)
        
        # Save checkpoint to file
        checkpoint_file = self.log_dir / f"checkpoint_{operation_id}_{checkpoint_name}.json"
        with open(checkpoint_file, 'w', encoding='utf-8') as f:
            json.dump(checkpoint, f, indent=2)
        
        self.log(operation_id, LogLevel.INFO, "checkpoint",
                f"Created checkpoint: {checkpoint_name}")
    
    def complete_operation(self, operation_id: str, final_status: OperationStatus = OperationStatus.COMPLETED):
        """Mark operation as completed"""
        if operation_id not in self.operations:
            return
        
        metrics = self.operations[operation_id]
        metrics.status = final_status
        metrics.last_update_time = datetime.now(timezone.utc)
        
        # Record final phase timing
        if metrics.current_phase in self.performance_history[operation_id]["phase_timings"]:
            phase_timing = self.performance_history[operation_id]["phase_timings"][metrics.current_phase]
            if phase_timing["end_time"] is None:
                phase_timing["end_time"] = metrics.last_update_time
                duration = (metrics.last_update_time - phase_timing["start_time"]).total_seconds()
                phase_timing["duration_seconds"] = duration
        
        # Calculate total duration
        total_duration = (metrics.last_update_time - metrics.start_time).total_seconds()
        
        self.log(operation_id, LogLevel.INFO, "completed",
                f"Operation completed with status: {final_status.value} | Duration: {total_duration:.1f}s",
                details={
                    "total_duration_seconds": total_duration,
                    "final_status": final_status.value,
                    "success_rate": metrics.success_rate,
                    "items_per_second": metrics.items_per_second
                })
    
    def get_operation_status(self, operation_id: str) -> Optional[ProgressMetrics]:
        """Get current status of an operation"""
        return self.operations.get(operation_id)
    
    def get_all_operations(self) -> Dict[str, ProgressMetrics]:
        """Get status of all operations"""
        return self.operations.copy()
    
    def generate_progress_report(self, operation_id: str, output_file: Path):
        """Generate comprehensive progress report"""
        if operation_id not in self.operations:
            raise ValueError(f"Operation {operation_id} not found")
        
        metrics = self.operations[operation_id]
        history = self.performance_history[operation_id]
        
        report = {
            "report_metadata": {
                "generation_timestamp": datetime.now(timezone.utc).isoformat(),
                "operation_id": operation_id,
                "report_type": "progress_report"
            },
            "operation_summary": asdict(metrics),
            "performance_analysis": {
                "total_duration_seconds": (metrics.last_update_time - metrics.start_time).total_seconds(),
                "average_processing_rate": metrics.items_per_second,
                "success_rate": metrics.success_rate,
                "error_rate": (metrics.error_count / (metrics.completed_items + metrics.failed_items)) * 100 if (metrics.completed_items + metrics.failed_items) > 0 else 0
            },
            "phase_analysis": history["phase_timings"],
            "checkpoint_history": history["checkpoint_history"],
            "recommendations": self._generate_recommendations(metrics, history)
        }
        
        # Convert datetime objects to ISO strings
        self._serialize_datetimes(report)
        
        # Save report
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        self.log(operation_id, LogLevel.INFO, "reporting",
                f"Progress report generated: {output_file}")
    
    def _serialize_datetimes(self, obj):
        """Convert datetime objects to ISO strings recursively"""
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, datetime):
                    obj[key] = value.isoformat()
                elif isinstance(value, (dict, list)):
                    self._serialize_datetimes(value)
        elif isinstance(obj, list):
            for item in obj:
                if isinstance(item, (dict, list)):
                    self._serialize_datetimes(item)
    
    def _generate_recommendations(self, metrics: ProgressMetrics, history: Dict[str, Any]) -> List[str]:
        """Generate performance recommendations"""
        recommendations = []
        
        # Processing rate recommendations
        if metrics.items_per_second < 1.0:
            recommendations.append("Consider optimizing processing pipeline - current rate is below 1 item/second")
        elif metrics.items_per_second > 10.0:
            recommendations.append("Excellent processing rate - consider this configuration for future operations")
        
        # Error rate recommendations  
        error_rate = (metrics.error_count / (metrics.completed_items + metrics.failed_items)) * 100 if (metrics.completed_items + metrics.failed_items) > 0 else 0
        if error_rate > 5.0:
            recommendations.append(f"High error rate ({error_rate:.1f}%) - investigate common failure patterns")
        
        # Success rate recommendations
        if metrics.success_rate < 90.0:
            recommendations.append(f"Success rate ({metrics.success_rate:.1f}%) below target - review failed items")
        
        return recommendations

@contextmanager
def monitor_operation(monitor: ProgressMonitor, 
                     operation_id: str, 
                     operation_name: str, 
                     total_items: int,
                     auto_complete: bool = True):
    """Context manager for operation monitoring"""
    try:
        # Start monitoring
        metrics = monitor.start_operation(operation_id, operation_name, total_items)
        yield monitor
        
        # Auto-complete if requested
        if auto_complete:
            monitor.complete_operation(operation_id, OperationStatus.COMPLETED)
            
    except Exception as e:
        # Mark as failed and re-raise
        monitor.log(operation_id, LogLevel.CRITICAL, "error", 
                   f"Operation failed with exception: {str(e)}", exception=e)
        if auto_complete:
            monitor.complete_operation(operation_id, OperationStatus.FAILED)
        raise

def main():
    """Main entry point for standalone monitoring"""
    parser = argparse.ArgumentParser(description='Progress monitoring and logging')
    parser.add_argument('--operation-id', type=str, required=True,
                        help='Operation ID to monitor')
    parser.add_argument('--operation-name', type=str, required=True,
                        help='Human-readable operation name')
    parser.add_argument('--total-items', type=int, required=True,
                        help='Total number of items to process')
    parser.add_argument('--log-dir', type=Path, default='operations/logs',
                        help='Directory for log files')
    parser.add_argument('--generate-report', action='store_true',
                        help='Generate progress report at the end')
    
    args = parser.parse_args()
    
    try:
        # Initialize monitor
        monitor = ProgressMonitor(args.log_dir)
        
        # Start monitoring
        with monitor_operation(monitor, args.operation_id, args.operation_name, args.total_items):
            print(f"Monitoring operation: {args.operation_name}")
            print(f"Operation ID: {args.operation_id}")
            print(f"Total items: {args.total_items}")
            print(f"Logs directory: {args.log_dir}")
            print("\nMonitoring started. Use monitor.update_progress() to track progress.")
            
            # Keep monitoring until interrupted
            try:
                while True:
                    time.sleep(1)
                    metrics = monitor.get_operation_status(args.operation_id)
                    if metrics and metrics.status in [OperationStatus.COMPLETED, OperationStatus.FAILED]:
                        break
            except KeyboardInterrupt:
                print("\nMonitoring interrupted by user")
                monitor.complete_operation(args.operation_id, OperationStatus.CANCELLED)
        
        # Generate final report if requested
        if args.generate_report:
            report_file = args.log_dir / f"progress_report_{args.operation_id}.json"
            monitor.generate_progress_report(args.operation_id, report_file)
            print(f"Progress report generated: {report_file}")
        
        print("Monitoring completed successfully")
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()