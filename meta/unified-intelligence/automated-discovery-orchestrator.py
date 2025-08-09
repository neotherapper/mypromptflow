#!/usr/bin/env python3
"""
Comprehensive Automated Discovery Algorithm Execution System
Orchestrates all intelligence discovery systems with intelligent coordination

Features:
- Integrates YouTube dynamic search, Reddit discovery, MCP YouTube processor, content digests
- Intelligent scheduling with configurable intervals
- Resource management and rate limiting
- Duplicate prevention and priority-based execution
- Error handling with retry logic and fallback systems
- Performance monitoring and reporting
- Configuration management and system health checks
"""

import os
import sys
import json
import time
import logging
import asyncio
import schedule
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import hashlib
import pickle
from enum import Enum
import traceback
import subprocess
import psutil
import signal

# Set up comprehensive logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automated-discovery-orchestrator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SystemStatus(Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    CRITICAL = "critical"
    OFFLINE = "offline"

class TaskPriority(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"
    SKIPPED = "skipped"

@dataclass
class DiscoveryTask:
    """Individual discovery task configuration"""
    task_id: str
    name: str
    module_path: str
    function_name: str
    priority: TaskPriority
    schedule_pattern: str  # cron-like or interval
    max_runtime_minutes: int
    retry_count: int = 0
    max_retries: int = 3
    retry_delay_minutes: int = 5
    dependencies: List[str] = None
    resource_requirements: Dict[str, Any] = None
    enabled: bool = True
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    status: TaskStatus = TaskStatus.PENDING
    error_message: Optional[str] = None
    execution_stats: Dict[str, Any] = None

@dataclass
class SystemMetrics:
    """System performance and health metrics"""
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    active_tasks: int
    completed_tasks_today: int
    failed_tasks_today: int
    error_rate: float
    average_task_duration: float
    system_uptime: float
    last_health_check: datetime

@dataclass
class OrchestrationConfig:
    """Master configuration for the orchestration system"""
    max_concurrent_tasks: int = 3
    resource_limits: Dict[str, Any] = None
    scheduling_intervals: Dict[str, str] = None
    quality_thresholds: Dict[str, Any] = None
    retry_policies: Dict[str, Any] = None
    monitoring_settings: Dict[str, Any] = None
    output_organization: Dict[str, Any] = None

class AutomatedDiscoveryOrchestrator:
    """Main orchestration system for all intelligence discovery operations"""
    
    def __init__(self, config_path: Optional[Path] = None):
        self.base_path = Path(__file__).parent
        self.config_path = config_path or self.base_path / "orchestrator-config.json"
        self.state_file = self.base_path / "orchestrator-state.json"
        self.metrics_file = self.base_path / "orchestrator-metrics.json"
        self.lock_file = self.base_path / "orchestrator.lock"
        
        # Load configuration
        self.config = self._load_configuration()
        
        # Initialize task registry
        self.tasks: Dict[str, DiscoveryTask] = {}
        self.task_history: List[Dict[str, Any]] = []
        self.active_processes: Dict[str, subprocess.Popen] = {}
        
        # Resource management
        self.executor = ThreadPoolExecutor(max_workers=self.config.max_concurrent_tasks)
        self.resource_locks = threading.RLock()
        
        # State management
        self.system_metrics = SystemMetrics(
            cpu_usage=0.0, memory_usage=0.0, disk_usage=0.0,
            active_tasks=0, completed_tasks_today=0, failed_tasks_today=0,
            error_rate=0.0, average_task_duration=0.0, system_uptime=0.0,
            last_health_check=datetime.now(timezone.utc)
        )
        
        # Initialize discovery systems
        self._initialize_discovery_systems()
        
        # Load previous state
        self._load_state()
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        logger.info("🚀 Automated Discovery Orchestrator initialized successfully")

    def _load_configuration(self) -> OrchestrationConfig:
        """Load or create orchestration configuration"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    config_data = json.load(f)
                return OrchestrationConfig(**config_data)
            except Exception as e:
                logger.warning(f"Failed to load config, using defaults: {e}")
        
        # Create default configuration
        default_config = OrchestrationConfig(
            max_concurrent_tasks=3,
            resource_limits={
                "max_cpu_percent": 80,
                "max_memory_mb": 2048,
                "max_disk_io_mb": 100
            },
            scheduling_intervals={
                "youtube_search": "daily",
                "reddit_discovery": "weekly", 
                "mcp_youtube_processing": "daily",
                "content_digest": "daily",
                "system_health": "hourly"
            },
            quality_thresholds={
                "min_content_score": 0.7,
                "max_duplicate_percentage": 0.1,
                "min_source_credibility": 0.8
            },
            retry_policies={
                "max_retries": 3,
                "retry_delay_minutes": 5,
                "exponential_backoff": True
            },
            monitoring_settings={
                "health_check_interval": 300,  # 5 minutes
                "metrics_retention_days": 30,
                "alert_thresholds": {
                    "error_rate": 0.2,
                    "cpu_usage": 90,
                    "memory_usage": 90
                }
            },
            output_organization={
                "base_storage_path": str(self.base_path / "orchestrator-outputs"),
                "organize_by_date": True,
                "compress_old_data": True,
                "retention_days": 90
            }
        )
        
        # Save default configuration
        self._save_configuration(default_config)
        return default_config

    def _save_configuration(self, config: OrchestrationConfig):
        """Save configuration to file"""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(asdict(config), f, indent=2, default=str)
            logger.info("📝 Configuration saved successfully")
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")

    def _initialize_discovery_systems(self):
        """Initialize all discovery system tasks"""
        
        # YouTube Dynamic Search System
        youtube_search_task = DiscoveryTask(
            task_id="youtube_search",
            name="YouTube Dynamic Search",
            module_path=str(self.base_path / "youtube-dynamic-search.py"),
            function_name="run_search_discovery",
            priority=TaskPriority.HIGH,
            schedule_pattern="daily",
            max_runtime_minutes=30,
            max_retries=3,
            resource_requirements={
                "network": True,
                "api_quota": "youtube",
                "memory_mb": 512
            }
        )
        
        # Reddit Dynamic Discovery System
        reddit_discovery_task = DiscoveryTask(
            task_id="reddit_discovery",
            name="Reddit Dynamic Discovery",
            module_path=str(self.base_path / "reddit-dynamic-discovery.py"),
            function_name="run_discovery_sweep",
            priority=TaskPriority.MEDIUM,
            schedule_pattern="weekly",
            max_runtime_minutes=45,
            max_retries=2,
            resource_requirements={
                "network": True,
                "api_quota": "reddit",
                "memory_mb": 768
            }
        )
        
        # MCP YouTube Processor
        mcp_youtube_task = DiscoveryTask(
            task_id="mcp_youtube_processing",
            name="MCP YouTube Content Processing",
            module_path=str(self.base_path / "mcp-youtube-processor.py"),
            function_name="process_priority_content",
            priority=TaskPriority.HIGH,
            schedule_pattern="daily",
            max_runtime_minutes=60,
            max_retries=3,
            dependencies=["youtube_search"],
            resource_requirements={
                "network": True,
                "mcp_server": "youtube",
                "memory_mb": 1024
            }
        )
        
        # Content Digest Generation
        digest_generation_task = DiscoveryTask(
            task_id="content_digest",
            name="Daily Intelligence Digest Generation",
            module_path=str(self.base_path / "daily-digest" / "intelligence-digest-generator.py"),
            function_name="generate_comprehensive_digest",
            priority=TaskPriority.CRITICAL,
            schedule_pattern="daily",
            max_runtime_minutes=20,
            max_retries=2,
            dependencies=["youtube_search", "reddit_discovery", "mcp_youtube_processing"],
            resource_requirements={
                "memory_mb": 512,
                "disk_mb": 100
            }
        )
        
        # System Health Monitoring
        health_monitoring_task = DiscoveryTask(
            task_id="system_health",
            name="System Health Monitoring",
            module_path=str(self.base_path / "automation" / "system-health-monitor.py"),
            function_name="run_health_check",
            priority=TaskPriority.LOW,
            schedule_pattern="hourly",
            max_runtime_minutes=5,
            max_retries=1,
            resource_requirements={
                "memory_mb": 128
            }
        )
        
        # Register all tasks
        for task in [youtube_search_task, reddit_discovery_task, mcp_youtube_task, 
                    digest_generation_task, health_monitoring_task]:
            self.tasks[task.task_id] = task
        
        logger.info(f"✅ Initialized {len(self.tasks)} discovery systems")

    def _load_state(self):
        """Load previous orchestrator state"""
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    state_data = json.load(f)
                
                # Restore task states
                for task_id, task_state in state_data.get("tasks", {}).items():
                    if task_id in self.tasks:
                        self.tasks[task_id].last_run = datetime.fromisoformat(task_state["last_run"]) if task_state.get("last_run") else None
                        self.tasks[task_id].next_run = datetime.fromisoformat(task_state["next_run"]) if task_state.get("next_run") else None
                        self.tasks[task_id].retry_count = task_state.get("retry_count", 0)
                        self.tasks[task_id].status = TaskStatus(task_state.get("status", "pending"))
                
                # Restore metrics
                if "metrics" in state_data:
                    self.system_metrics = SystemMetrics(**state_data["metrics"])
                
                logger.info("📊 Previous state restored successfully")
                
            except Exception as e:
                logger.warning(f"Failed to load previous state: {e}")

    def _save_state(self):
        """Save current orchestrator state"""
        try:
            state_data = {
                "tasks": {
                    task_id: {
                        "last_run": task.last_run.isoformat() if task.last_run else None,
                        "next_run": task.next_run.isoformat() if task.next_run else None,
                        "retry_count": task.retry_count,
                        "status": task.status.value,
                        "error_message": task.error_message
                    }
                    for task_id, task in self.tasks.items()
                },
                "metrics": asdict(self.system_metrics),
                "last_saved": datetime.now(timezone.utc).isoformat()
            }
            
            with open(self.state_file, 'w') as f:
                json.dump(state_data, f, indent=2, default=str)
                
            logger.debug("💾 State saved successfully")
            
        except Exception as e:
            logger.error(f"Failed to save state: {e}")

    def _check_system_resources(self) -> Tuple[bool, Dict[str, Any]]:
        """Check if system has sufficient resources for task execution"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            resource_status = {
                "cpu_usage": cpu_percent,
                "memory_usage": memory.percent,
                "disk_usage": disk.percent,
                "available_memory_mb": memory.available / (1024 * 1024),
                "available_disk_gb": disk.free / (1024 * 1024 * 1024)
            }
            
            # Check against limits
            limits = self.config.resource_limits
            resources_available = (
                cpu_percent < limits["max_cpu_percent"] and
                memory.percent < limits.get("max_memory_percent", 85) and
                disk.percent < limits.get("max_disk_percent", 90)
            )
            
            # Update system metrics
            self.system_metrics.cpu_usage = cpu_percent
            self.system_metrics.memory_usage = memory.percent
            self.system_metrics.disk_usage = disk.percent
            self.system_metrics.last_health_check = datetime.now(timezone.utc)
            
            return resources_available, resource_status
            
        except Exception as e:
            logger.error(f"Resource check failed: {e}")
            return False, {"error": str(e)}

    def _calculate_next_run_time(self, task: DiscoveryTask) -> datetime:
        """Calculate next run time based on schedule pattern"""
        now = datetime.now(timezone.utc)
        
        if task.schedule_pattern == "hourly":
            return now + timedelta(hours=1)
        elif task.schedule_pattern == "daily":
            # Run at 6 AM UTC daily
            next_run = now.replace(hour=6, minute=0, second=0, microsecond=0)
            if next_run <= now:
                next_run += timedelta(days=1)
            return next_run
        elif task.schedule_pattern == "weekly":
            # Run on Sundays at 8 AM UTC
            days_ahead = 6 - now.weekday()  # Sunday is 6
            if days_ahead <= 0:
                days_ahead += 7
            next_run = now.replace(hour=8, minute=0, second=0, microsecond=0)
            next_run += timedelta(days=days_ahead)
            return next_run
        elif task.schedule_pattern == "bi-weekly":
            # Run every 14 days
            last_run = task.last_run or now
            return last_run + timedelta(days=14)
        else:
            # Default to daily
            return now + timedelta(days=1)

    def _check_task_dependencies(self, task: DiscoveryTask) -> bool:
        """Check if task dependencies are satisfied"""
        if not task.dependencies:
            return True
        
        for dep_id in task.dependencies:
            if dep_id not in self.tasks:
                logger.warning(f"Dependency {dep_id} not found for task {task.task_id}")
                continue
            
            dep_task = self.tasks[dep_id]
            
            # Check if dependency completed successfully within last 24 hours
            if (dep_task.status != TaskStatus.COMPLETED or 
                not dep_task.last_run or
                (datetime.now(timezone.utc) - dep_task.last_run) > timedelta(hours=24)):
                logger.info(f"Dependency {dep_id} not satisfied for task {task.task_id}")
                return False
        
        return True

    def _execute_discovery_task(self, task: DiscoveryTask) -> Tuple[bool, Dict[str, Any]]:
        """Execute a single discovery task"""
        logger.info(f"🔄 Starting task: {task.name} ({task.task_id})")
        
        start_time = datetime.now(timezone.utc)
        task.status = TaskStatus.RUNNING
        
        try:
            # Import and execute the task module
            if task.module_path.endswith('.py'):
                # Execute Python script
                result = subprocess.run([
                    sys.executable, task.module_path
                ], capture_output=True, text=True, timeout=task.max_runtime_minutes * 60)
                
                success = result.returncode == 0
                output = {
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "returncode": result.returncode
                }
                
                if not success:
                    logger.error(f"Task {task.task_id} failed with return code {result.returncode}")
                    logger.error(f"Error output: {result.stderr}")
                
            else:
                # Direct function execution (for future extensibility)
                success = False
                output = {"error": "Direct function execution not implemented yet"}
            
            # Update task statistics
            execution_time = (datetime.now(timezone.utc) - start_time).total_seconds()
            task.execution_stats = {
                "execution_time_seconds": execution_time,
                "start_time": start_time.isoformat(),
                "end_time": datetime.now(timezone.utc).isoformat(),
                "success": success
            }
            
            if success:
                task.status = TaskStatus.COMPLETED
                task.retry_count = 0
                task.error_message = None
                self.system_metrics.completed_tasks_today += 1
                logger.info(f"✅ Task {task.name} completed successfully in {execution_time:.2f}s")
            else:
                task.status = TaskStatus.FAILED
                task.error_message = output.get("stderr", "Unknown error")
                self.system_metrics.failed_tasks_today += 1
                logger.error(f"❌ Task {task.name} failed after {execution_time:.2f}s")
            
            task.last_run = datetime.now(timezone.utc)
            task.next_run = self._calculate_next_run_time(task)
            
            return success, output
            
        except subprocess.TimeoutExpired:
            task.status = TaskStatus.FAILED
            task.error_message = f"Task timed out after {task.max_runtime_minutes} minutes"
            logger.error(f"⏱️ Task {task.name} timed out")
            return False, {"error": "Timeout"}
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error_message = str(e)
            logger.error(f"💥 Task {task.name} crashed: {e}")
            logger.error(traceback.format_exc())
            return False, {"error": str(e), "traceback": traceback.format_exc()}

    def _should_retry_task(self, task: DiscoveryTask) -> bool:
        """Determine if a failed task should be retried"""
        if task.retry_count >= task.max_retries:
            return False
        
        if task.status != TaskStatus.FAILED:
            return False
        
        # Don't retry if error indicates permanent failure
        if task.error_message and any(term in task.error_message.lower() for term in 
                                    ["authentication", "permission", "not found", "invalid"]):
            return False
        
        return True

    def _execute_with_retry(self, task: DiscoveryTask) -> Tuple[bool, Dict[str, Any]]:
        """Execute task with retry logic"""
        max_attempts = task.max_retries + 1
        
        for attempt in range(max_attempts):
            if attempt > 0:
                task.status = TaskStatus.RETRYING
                retry_delay = task.retry_delay_minutes * (2 ** (attempt - 1))  # Exponential backoff
                logger.info(f"🔄 Retrying task {task.name} (attempt {attempt + 1}/{max_attempts}) after {retry_delay}min delay")
                time.sleep(retry_delay * 60)
            
            success, result = self._execute_discovery_task(task)
            
            if success:
                return True, result
            
            task.retry_count = attempt + 1
            
            if not self._should_retry_task(task):
                break
        
        logger.error(f"🚫 Task {task.name} failed after {max_attempts} attempts")
        return False, result

    def _process_task_queue(self):
        """Process all eligible tasks in priority order"""
        logger.info("🎯 Processing task queue...")
        
        # Check system resources
        resources_available, resource_status = self._check_system_resources()
        if not resources_available:
            logger.warning(f"⚠️ Insufficient system resources: {resource_status}")
            return
        
        # Get eligible tasks (enabled, due for execution, dependencies satisfied)
        now = datetime.now(timezone.utc)
        eligible_tasks = []
        
        for task in self.tasks.values():
            if not task.enabled:
                continue
            
            if task.status == TaskStatus.RUNNING:
                continue
            
            if task.next_run and task.next_run > now:
                continue
            
            if not self._check_task_dependencies(task):
                continue
            
            eligible_tasks.append(task)
        
        # Sort by priority
        eligible_tasks.sort(key=lambda t: t.priority.value)
        
        if not eligible_tasks:
            logger.info("No eligible tasks found")
            return
        
        logger.info(f"Found {len(eligible_tasks)} eligible tasks")
        
        # Execute tasks within resource limits
        futures = []
        active_tasks = 0
        
        for task in eligible_tasks:
            if active_tasks >= self.config.max_concurrent_tasks:
                break
            
            logger.info(f"🚀 Submitting task: {task.name}")
            future = self.executor.submit(self._execute_with_retry, task)
            futures.append((future, task))
            active_tasks += 1
            
            self.system_metrics.active_tasks += 1
        
        # Wait for completion and collect results
        for future, task in futures:
            try:
                success, result = future.result()
                
                # Log task completion
                self.task_history.append({
                    "task_id": task.task_id,
                    "name": task.name,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "success": success,
                    "execution_time": task.execution_stats.get("execution_time_seconds", 0) if task.execution_stats else 0,
                    "error_message": task.error_message
                })
                
            except Exception as e:
                logger.error(f"Task execution error: {e}")
            
            finally:
                self.system_metrics.active_tasks -= 1
        
        # Clean up completed futures
        for future, _ in futures:
            if not future.done():
                future.cancel()

    def _generate_system_report(self) -> Dict[str, Any]:
        """Generate comprehensive system status report"""
        now = datetime.now(timezone.utc)
        
        # Calculate statistics
        today_tasks = [h for h in self.task_history 
                      if datetime.fromisoformat(h["timestamp"]).date() == now.date()]
        
        total_today = len(today_tasks)
        successful_today = sum(1 for h in today_tasks if h["success"])
        error_rate = (total_today - successful_today) / total_today if total_today > 0 else 0
        
        # Average execution time
        execution_times = [h["execution_time"] for h in today_tasks if h["execution_time"] > 0]
        avg_execution_time = sum(execution_times) / len(execution_times) if execution_times else 0
        
        # Update metrics
        self.system_metrics.completed_tasks_today = successful_today
        self.system_metrics.failed_tasks_today = total_today - successful_today
        self.system_metrics.error_rate = error_rate
        self.system_metrics.average_task_duration = avg_execution_time
        
        # Task status summary
        task_status_summary = {}
        for status in TaskStatus:
            task_status_summary[status.value] = sum(1 for t in self.tasks.values() if t.status == status)
        
        # Next scheduled tasks
        next_tasks = []
        for task in self.tasks.values():
            if task.enabled and task.next_run:
                next_tasks.append({
                    "task_id": task.task_id,
                    "name": task.name,
                    "next_run": task.next_run.isoformat(),
                    "priority": task.priority.value
                })
        
        next_tasks.sort(key=lambda t: t["next_run"])
        
        report = {
            "system_status": SystemStatus.HEALTHY.value,
            "timestamp": now.isoformat(),
            "metrics": asdict(self.system_metrics),
            "task_status_summary": task_status_summary,
            "tasks_today": {
                "total": total_today,
                "successful": successful_today,
                "failed": total_today - successful_today,
                "error_rate": error_rate
            },
            "next_scheduled_tasks": next_tasks[:10],  # Next 10 tasks
            "resource_status": self._check_system_resources()[1],
            "configuration": asdict(self.config)
        }
        
        return report

    def _cleanup_old_data(self):
        """Clean up old logs, states, and outputs based on retention policy"""
        try:
            retention_days = self.config.output_organization.get("retention_days", 90)
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=retention_days)
            
            # Clean up task history
            self.task_history = [
                h for h in self.task_history 
                if datetime.fromisoformat(h["timestamp"]) > cutoff_date
            ]
            
            # Clean up old output files (implementation depends on output structure)
            output_base = Path(self.config.output_organization["base_storage_path"])
            if output_base.exists():
                for item in output_base.rglob("*"):
                    if item.is_file() and item.stat().st_mtime < cutoff_date.timestamp():
                        try:
                            item.unlink()
                            logger.debug(f"Cleaned up old file: {item}")
                        except Exception as e:
                            logger.warning(f"Failed to clean up {item}: {e}")
            
            logger.info(f"🧹 Cleanup completed - removed data older than {retention_days} days")
            
        except Exception as e:
            logger.error(f"Cleanup failed: {e}")

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info(f"📡 Received signal {signum}, initiating graceful shutdown...")
        
        # Cancel running tasks
        for task_id, task in self.tasks.items():
            if task.status == TaskStatus.RUNNING:
                logger.info(f"🛑 Stopping task: {task.name}")
                task.status = TaskStatus.PENDING
        
        # Save final state
        self._save_state()
        
        # Cleanup
        if hasattr(self, 'executor'):
            self.executor.shutdown(wait=True)
        
        # Remove lock file
        if self.lock_file.exists():
            self.lock_file.unlink()
        
        logger.info("👋 Graceful shutdown completed")
        sys.exit(0)

    def run_single_cycle(self):
        """Run a single orchestration cycle"""
        logger.info("🔄 Starting orchestration cycle")
        
        try:
            # Create lock file
            with open(self.lock_file, 'w') as f:
                f.write(str(os.getpid()))
            
            # Process task queue
            self._process_task_queue()
            
            # Save state
            self._save_state()
            
            # Generate and save system report
            report = self._generate_system_report()
            report_file = self.base_path / f"system-report-{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2, default=str)
            
            # Periodic cleanup
            if datetime.now().hour == 2:  # Run cleanup at 2 AM
                self._cleanup_old_data()
            
            logger.info("✅ Orchestration cycle completed successfully")
            
        except Exception as e:
            logger.error(f"💥 Orchestration cycle failed: {e}")
            logger.error(traceback.format_exc())
        
        finally:
            # Remove lock file
            if self.lock_file.exists():
                self.lock_file.unlink()

    def run_continuous(self):
        """Run orchestrator continuously with scheduling"""
        logger.info("🚀 Starting continuous orchestration mode")
        
        # Schedule regular cycles
        schedule.every(30).minutes.do(self.run_single_cycle)
        schedule.every().day.at("06:00").do(self.run_single_cycle)
        schedule.every().sunday.at("08:00").do(self.run_single_cycle)
        
        # Initial run
        self.run_single_cycle()
        
        # Continuous scheduling loop
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
            except KeyboardInterrupt:
                logger.info("🛑 Received interrupt signal, shutting down...")
                break
            except Exception as e:
                logger.error(f"Scheduling error: {e}")
                time.sleep(300)  # Wait 5 minutes before retrying

    def get_status(self) -> Dict[str, Any]:
        """Get current orchestrator status"""
        return self._generate_system_report()

    def enable_task(self, task_id: str) -> bool:
        """Enable a specific task"""
        if task_id in self.tasks:
            self.tasks[task_id].enabled = True
            logger.info(f"✅ Enabled task: {task_id}")
            return True
        return False

    def disable_task(self, task_id: str) -> bool:
        """Disable a specific task"""
        if task_id in self.tasks:
            self.tasks[task_id].enabled = False
            logger.info(f"⏸️ Disabled task: {task_id}")
            return True
        return False

    def force_run_task(self, task_id: str) -> Tuple[bool, Dict[str, Any]]:
        """Force run a specific task immediately"""
        if task_id not in self.tasks:
            return False, {"error": f"Task {task_id} not found"}
        
        task = self.tasks[task_id]
        logger.info(f"🚀 Force running task: {task.name}")
        
        return self._execute_with_retry(task)

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Automated Discovery Orchestrator")
    parser.add_argument("--mode", choices=["single", "continuous", "status"], 
                       default="continuous", help="Execution mode")
    parser.add_argument("--config", type=Path, help="Configuration file path")
    parser.add_argument("--task", help="Force run specific task (requires --mode single)")
    parser.add_argument("--enable", help="Enable specific task")
    parser.add_argument("--disable", help="Disable specific task")
    
    args = parser.parse_args()
    
    # Initialize orchestrator
    orchestrator = AutomatedDiscoveryOrchestrator(config_path=args.config)
    
    try:
        if args.enable:
            success = orchestrator.enable_task(args.enable)
            print(f"Task {args.enable} {'enabled' if success else 'not found'}")
            return
        
        if args.disable:
            success = orchestrator.disable_task(args.disable)
            print(f"Task {args.disable} {'disabled' if success else 'not found'}")
            return
        
        if args.mode == "status":
            status = orchestrator.get_status()
            print(json.dumps(status, indent=2, default=str))
        
        elif args.mode == "single":
            if args.task:
                success, result = orchestrator.force_run_task(args.task)
                print(f"Task execution {'successful' if success else 'failed'}")
                print(json.dumps(result, indent=2))
            else:
                orchestrator.run_single_cycle()
        
        else:  # continuous
            orchestrator.run_continuous()
    
    except KeyboardInterrupt:
        logger.info("👋 Orchestrator stopped by user")
    except Exception as e:
        logger.error(f"💥 Orchestrator crashed: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main()