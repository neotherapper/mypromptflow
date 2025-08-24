#!/usr/bin/env python3
"""
Universal Topic Intelligence Scheduler
Provides automated background monitoring with configurable intervals
"""

import asyncio
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from pathlib import Path
import signal
import sys
from enum import Enum

class ScheduleStatus(Enum):
    """Status of scheduled tasks"""
    PENDING = "pending"       # Waiting to run
    RUNNING = "running"       # Currently executing
    COMPLETED = "completed"   # Successfully finished
    FAILED = "failed"        # Failed with error
    CANCELLED = "cancelled"  # Manually cancelled
    PAUSED = "paused"       # Temporarily paused

@dataclass
class ScheduledTask:
    """Represents a scheduled monitoring task"""
    task_id: str
    name: str
    interval_minutes: int
    next_run: datetime
    last_run: Optional[datetime] = None
    status: ScheduleStatus = ScheduleStatus.PENDING
    error_count: int = 0
    max_retries: int = 3
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

@dataclass 
class ScheduleResult:
    """Result of a scheduled task execution"""
    task_id: str
    start_time: datetime
    end_time: datetime
    status: ScheduleStatus
    items_found: int = 0
    items_stored: int = 0
    error_message: Optional[str] = None
    execution_time_seconds: float = 0.0
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
        self.execution_time_seconds = (self.end_time - self.start_time).total_seconds()

class UniversalScheduler:
    """
    Universal scheduler for automated topic monitoring
    Supports configurable intervals, retry logic, and background execution
    """
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize scheduler
        
        Args:
            config_file: Optional path to scheduler configuration file
        """
        self.logger = logging.getLogger("UniversalScheduler")
        self.tasks: Dict[str, ScheduledTask] = {}
        self.results_history: List[ScheduleResult] = []
        self.is_running = False
        self.shutdown_requested = False
        
        # Configuration
        self.config_file = config_file or "scheduler_config.json"
        self.max_history_size = 1000  # Keep last 1000 results
        self.default_retry_delay = 60  # 1 minute retry delay
        
        # Task execution callback
        self.task_executor: Optional[Callable] = None
        
        # Statistics
        self.stats = {
            "total_executions": 0,
            "successful_executions": 0,
            "failed_executions": 0,
            "total_runtime_seconds": 0.0,
            "average_execution_time": 0.0,
            "last_cleanup": datetime.now()
        }
        
        # Load configuration if exists
        self._load_config()
        
        # Set up signal handlers for graceful shutdown
        self._setup_signal_handlers()
    
    def _setup_signal_handlers(self):
        """Set up signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            self.logger.info(f"Received signal {signum}, initiating graceful shutdown...")
            self.shutdown_requested = True
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def _load_config(self):
        """Load scheduler configuration from file"""
        config_path = Path(self.config_file)
        if not config_path.exists():
            self.logger.info(f"No config file found at {config_path}, using defaults")
            return
        
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            # Load tasks from config
            for task_data in config.get("tasks", []):
                task = ScheduledTask(
                    task_id=task_data["task_id"],
                    name=task_data["name"],
                    interval_minutes=task_data["interval_minutes"],
                    next_run=datetime.fromisoformat(task_data["next_run"]),
                    last_run=datetime.fromisoformat(task_data["last_run"]) if task_data.get("last_run") else None,
                    status=ScheduleStatus(task_data.get("status", "pending")),
                    error_count=task_data.get("error_count", 0),
                    max_retries=task_data.get("max_retries", 3),
                    metadata=task_data.get("metadata", {})
                )
                self.tasks[task.task_id] = task
                
            self.logger.info(f"Loaded {len(self.tasks)} scheduled tasks from config")
            
        except Exception as e:
            self.logger.error(f"Error loading config from {config_path}: {e}")
    
    def _save_config(self):
        """Save current scheduler configuration to file"""
        try:
            config = {
                "tasks": [],
                "last_saved": datetime.now().isoformat(),
                "stats": self.stats
            }
            
            for task in self.tasks.values():
                task_data = {
                    "task_id": task.task_id,
                    "name": task.name,
                    "interval_minutes": task.interval_minutes,
                    "next_run": task.next_run.isoformat(),
                    "last_run": task.last_run.isoformat() if task.last_run else None,
                    "status": task.status.value,
                    "error_count": task.error_count,
                    "max_retries": task.max_retries,
                    "metadata": task.metadata
                }
                config["tasks"].append(task_data)
            
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2, default=str)
                
            self.logger.debug(f"Saved scheduler config to {self.config_file}")
            
        except Exception as e:
            self.logger.error(f"Error saving config to {self.config_file}: {e}")
    
    def set_task_executor(self, executor: Callable):
        """
        Set the task execution function
        
        Args:
            executor: Async function that takes a task and returns execution results
        """
        self.task_executor = executor
        self.logger.info("Task executor registered")
    
    def add_task(self, 
                 task_id: str, 
                 name: str, 
                 interval_minutes: int,
                 start_immediately: bool = False,
                 metadata: Optional[Dict[str, Any]] = None) -> ScheduledTask:
        """
        Add a new scheduled task
        
        Args:
            task_id: Unique identifier for the task
            name: Human-readable name
            interval_minutes: How often to run the task
            start_immediately: Whether to run immediately or wait for interval
            metadata: Additional task metadata
            
        Returns:
            The created ScheduledTask
        """
        if task_id in self.tasks:
            raise ValueError(f"Task with ID '{task_id}' already exists")
        
        next_run = datetime.now() if start_immediately else datetime.now() + timedelta(minutes=interval_minutes)
        
        task = ScheduledTask(
            task_id=task_id,
            name=name,
            interval_minutes=interval_minutes,
            next_run=next_run,
            metadata=metadata or {}
        )
        
        self.tasks[task_id] = task
        self.logger.info(f"Added scheduled task: {name} (every {interval_minutes}min)")
        
        # Save config after adding task
        self._save_config()
        
        return task
    
    def remove_task(self, task_id: str) -> bool:
        """
        Remove a scheduled task
        
        Args:
            task_id: ID of task to remove
            
        Returns:
            True if task was removed, False if not found
        """
        if task_id in self.tasks:
            task = self.tasks.pop(task_id)
            self.logger.info(f"Removed scheduled task: {task.name}")
            self._save_config()
            return True
        return False
    
    def pause_task(self, task_id: str) -> bool:
        """Pause a scheduled task"""
        if task_id in self.tasks:
            self.tasks[task_id].status = ScheduleStatus.PAUSED
            self.logger.info(f"Paused task: {self.tasks[task_id].name}")
            self._save_config()
            return True
        return False
    
    def resume_task(self, task_id: str) -> bool:
        """Resume a paused task"""
        if task_id in self.tasks:
            task = self.tasks[task_id]
            if task.status == ScheduleStatus.PAUSED:
                task.status = ScheduleStatus.PENDING
                # Reset next run time
                task.next_run = datetime.now() + timedelta(minutes=task.interval_minutes)
                self.logger.info(f"Resumed task: {task.name}")
                self._save_config()
                return True
        return False
    
    def get_task_status(self) -> Dict[str, Any]:
        """Get current status of all scheduled tasks"""
        now = datetime.now()
        
        status = {
            "scheduler_running": self.is_running,
            "total_tasks": len(self.tasks),
            "tasks_by_status": {},
            "next_run": None,
            "recent_results": [],
            "stats": self.stats.copy()
        }
        
        # Count tasks by status
        for task in self.tasks.values():
            status_name = task.status.value
            status["tasks_by_status"][status_name] = status["tasks_by_status"].get(status_name, 0) + 1
        
        # Find next run time
        upcoming_tasks = [t for t in self.tasks.values() 
                         if t.status in [ScheduleStatus.PENDING] and t.next_run > now]
        if upcoming_tasks:
            next_task = min(upcoming_tasks, key=lambda t: t.next_run)
            status["next_run"] = {
                "task_id": next_task.task_id,
                "name": next_task.name,
                "scheduled_time": next_task.next_run.isoformat(),
                "minutes_until": int((next_task.next_run - now).total_seconds() / 60)
            }
        
        # Include recent results (last 5)
        status["recent_results"] = [
            {
                "task_id": r.task_id,
                "status": r.status.value,
                "execution_time": f"{r.execution_time_seconds:.1f}s",
                "items_processed": f"{r.items_found}/{r.items_stored}",
                "timestamp": r.end_time.isoformat()
            }
            for r in self.results_history[-5:]
        ]
        
        return status
    
    def get_task_details(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a specific task"""
        if task_id not in self.tasks:
            return None
        
        task = self.tasks[task_id]
        
        # Get results history for this task
        task_results = [r for r in self.results_history if r.task_id == task_id]
        
        return {
            "task": {
                "task_id": task.task_id,
                "name": task.name,
                "status": task.status.value,
                "interval_minutes": task.interval_minutes,
                "next_run": task.next_run.isoformat(),
                "last_run": task.last_run.isoformat() if task.last_run else None,
                "error_count": task.error_count,
                "max_retries": task.max_retries,
                "metadata": task.metadata
            },
            "execution_history": [
                {
                    "start_time": r.start_time.isoformat(),
                    "end_time": r.end_time.isoformat(),
                    "status": r.status.value,
                    "execution_time_seconds": r.execution_time_seconds,
                    "items_found": r.items_found,
                    "items_stored": r.items_stored,
                    "error_message": r.error_message
                }
                for r in task_results[-10:]  # Last 10 executions
            ]
        }
    
    async def _execute_task(self, task: ScheduledTask) -> ScheduleResult:
        """Execute a single scheduled task"""
        start_time = datetime.now()
        task.status = ScheduleStatus.RUNNING
        
        self.logger.info(f"Executing scheduled task: {task.name}")
        
        try:
            if not self.task_executor:
                raise Exception("No task executor registered")
            
            # Execute the actual task
            execution_result = await self.task_executor(task)
            
            # Create successful result
            result = ScheduleResult(
                task_id=task.task_id,
                start_time=start_time,
                end_time=datetime.now(),
                status=ScheduleStatus.COMPLETED,
                items_found=execution_result.get("items_found", 0),
                items_stored=execution_result.get("items_stored", 0),
                metadata=execution_result.get("metadata", {})
            )
            
            # Update task state
            task.status = ScheduleStatus.COMPLETED
            task.last_run = start_time
            task.error_count = 0  # Reset error count on success
            task.next_run = datetime.now() + timedelta(minutes=task.interval_minutes)
            
            # Update statistics
            self.stats["successful_executions"] += 1
            
            self.logger.info(f"Task '{task.name}' completed successfully in {result.execution_time_seconds:.1f}s")
            
        except Exception as e:
            # Create failed result
            result = ScheduleResult(
                task_id=task.task_id,
                start_time=start_time,
                end_time=datetime.now(),
                status=ScheduleStatus.FAILED,
                error_message=str(e)
            )
            
            # Update task state
            task.error_count += 1
            
            if task.error_count >= task.max_retries:
                task.status = ScheduleStatus.FAILED
                task.next_run = datetime.now() + timedelta(minutes=task.interval_minutes * 2)  # Longer delay after failures
                self.logger.error(f"Task '{task.name}' failed {task.error_count} times, backing off")
            else:
                task.status = ScheduleStatus.PENDING
                task.next_run = datetime.now() + timedelta(minutes=self.default_retry_delay)
                self.logger.warning(f"Task '{task.name}' failed (attempt {task.error_count}/{task.max_retries}), retrying in {self.default_retry_delay} minutes")
            
            # Update statistics
            self.stats["failed_executions"] += 1
            
            self.logger.error(f"Task '{task.name}' failed: {e}")
        
        finally:
            if task.status == ScheduleStatus.RUNNING:
                task.status = ScheduleStatus.PENDING
        
        # Update statistics
        self.stats["total_executions"] += 1
        self.stats["total_runtime_seconds"] += result.execution_time_seconds
        if self.stats["total_executions"] > 0:
            self.stats["average_execution_time"] = self.stats["total_runtime_seconds"] / self.stats["total_executions"]
        
        # Store result in history
        self.results_history.append(result)
        
        # Cleanup old history
        if len(self.results_history) > self.max_history_size:
            self.results_history = self.results_history[-self.max_history_size:]
        
        # Save updated state
        self._save_config()
        
        return result
    
    async def _scheduler_loop(self):
        """Main scheduler loop"""
        self.logger.info("Scheduler loop started")
        
        while not self.shutdown_requested:
            try:
                now = datetime.now()
                
                # Find tasks ready to run
                ready_tasks = [
                    task for task in self.tasks.values()
                    if (task.status in [ScheduleStatus.PENDING] and 
                        task.next_run <= now)
                ]
                
                if ready_tasks:
                    self.logger.info(f"Found {len(ready_tasks)} tasks ready to run")
                    
                    # Execute ready tasks concurrently
                    tasks_to_execute = [self._execute_task(task) for task in ready_tasks]
                    results = await asyncio.gather(*tasks_to_execute, return_exceptions=True)
                    
                    for result in results:
                        if isinstance(result, Exception):
                            self.logger.error(f"Task execution failed with exception: {result}")
                
                # Periodic cleanup
                if (now - self.stats["last_cleanup"]).total_seconds() > 3600:  # Every hour
                    await self._periodic_cleanup()
                    self.stats["last_cleanup"] = now
                
                # Sleep for a short interval before checking again
                await asyncio.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                self.logger.error(f"Error in scheduler loop: {e}")
                await asyncio.sleep(60)  # Wait longer on error
        
        self.logger.info("Scheduler loop stopped")
    
    async def _periodic_cleanup(self):
        """Perform periodic maintenance tasks"""
        self.logger.debug("Performing periodic cleanup")
        
        # Clean up old results
        cutoff_time = datetime.now() - timedelta(days=7)
        original_count = len(self.results_history)
        self.results_history = [r for r in self.results_history if r.end_time > cutoff_time]
        
        if len(self.results_history) < original_count:
            self.logger.debug(f"Cleaned up {original_count - len(self.results_history)} old results")
        
        # Reset error counts for tasks that have been successful recently
        for task in self.tasks.values():
            if (task.last_run and 
                task.error_count > 0 and 
                (datetime.now() - task.last_run).total_seconds() > 3600):  # 1 hour
                recent_results = [r for r in self.results_history 
                                if r.task_id == task.task_id and r.status == ScheduleStatus.COMPLETED]
                if recent_results:
                    task.error_count = max(0, task.error_count - 1)
                    self.logger.debug(f"Reduced error count for task {task.name}")
    
    async def start(self):
        """Start the scheduler"""
        if self.is_running:
            raise RuntimeError("Scheduler is already running")
        
        if not self.task_executor:
            raise RuntimeError("No task executor registered. Call set_task_executor() first.")
        
        self.is_running = True
        self.shutdown_requested = False
        
        self.logger.info(f"Starting Universal Scheduler with {len(self.tasks)} tasks")
        
        # Start the scheduler loop
        await self._scheduler_loop()
        
        self.is_running = False
        self.logger.info("Universal Scheduler stopped")
    
    def stop(self):
        """Request scheduler shutdown"""
        self.shutdown_requested = True
        self.logger.info("Scheduler shutdown requested")
    
    async def run_task_once(self, task_id: str) -> Optional[ScheduleResult]:
        """Run a specific task once, regardless of schedule"""
        if task_id not in self.tasks:
            return None
        
        task = self.tasks[task_id]
        self.logger.info(f"Running task '{task.name}' on-demand")
        
        return await self._execute_task(task)


# CLI interface for scheduler management
def main():
    """CLI interface for scheduler"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Universal Topic Intelligence Scheduler")
    parser.add_argument("--config", default="scheduler_config.json", help="Config file path")
    parser.add_argument("--add-task", nargs=3, metavar=("ID", "NAME", "INTERVAL"), 
                       help="Add a task: ID NAME INTERVAL_MINUTES")
    parser.add_argument("--remove-task", metavar="ID", help="Remove a task by ID")
    parser.add_argument("--list-tasks", action="store_true", help="List all scheduled tasks")
    parser.add_argument("--status", action="store_true", help="Show scheduler status")
    parser.add_argument("--start", action="store_true", help="Start the scheduler daemon")
    
    args = parser.parse_args()
    
    # Initialize scheduler
    scheduler = UniversalScheduler(args.config)
    
    if args.add_task:
        task_id, name, interval = args.add_task
        scheduler.add_task(task_id, name, int(interval))
        print(f"Added task: {name} (every {interval} minutes)")
    
    elif args.remove_task:
        if scheduler.remove_task(args.remove_task):
            print(f"Removed task: {args.remove_task}")
        else:
            print(f"Task not found: {args.remove_task}")
    
    elif args.list_tasks:
        print("Scheduled Tasks:")
        print("-" * 60)
        for task in scheduler.tasks.values():
            print(f"{task.task_id:15} {task.name:25} {task.interval_minutes:4}min {task.status.value:10} {task.next_run}")
    
    elif args.status:
        status = scheduler.get_task_status()
        print("Scheduler Status:")
        print("-" * 40)
        print(f"Running: {status['scheduler_running']}")
        print(f"Total tasks: {status['total_tasks']}")
        print(f"Tasks by status: {status['tasks_by_status']}")
        if status['next_run']:
            print(f"Next run: {status['next_run']['name']} in {status['next_run']['minutes_until']} minutes")
    
    elif args.start:
        print("Starting scheduler daemon...")
        # This would need integration with the actual monitor
        print("Note: Scheduler daemon requires integration with UniversalMonitor")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()