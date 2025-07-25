#!/usr/bin/env python3
"""
Change Detection Orchestrator
AI Knowledge Lifecycle Orchestrator - Main orchestration and scheduling component

This module coordinates all change detection components, implements scheduling,
monitoring, alerting, and provides production-ready operations support.
"""

import asyncio
import logging
import signal
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, asdict
from pathlib import Path
from enum import Enum
import schedule
import threading
from concurrent.futures import ThreadPoolExecutor

from .config_manager import ConfigManager
from .mcp_integrator import MCPIntegrator
from .storage_interface import StorageInterface
from .change_detector import ChangeDetectionEngine, ChangeValidator, TechnologyChange

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OrchestrationMode(Enum):
    """Orchestration execution modes"""
    CONTINUOUS = "continuous"
    SCHEDULED = "scheduled"
    ON_DEMAND = "on_demand"
    BATCH = "batch"


class AlertSeverity(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class OrchestrationConfig:
    """Configuration for orchestration behavior"""
    mode: OrchestrationMode = OrchestrationMode.SCHEDULED
    check_interval_minutes: int = 60
    batch_size: int = 5
    max_concurrent_detections: int = 3
    health_check_interval_minutes: int = 10
    alert_cooldown_minutes: int = 30
    retry_failed_after_minutes: int = 120
    max_retries: int = 3


@dataclass
class DetectionTask:
    """Represents a change detection task"""
    technology_name: str
    scheduled_at: datetime
    priority: int = 1
    retry_count: int = 0
    last_attempt: Optional[datetime] = None
    last_error: Optional[str] = None
    status: str = "pending"  # pending, running, completed, failed
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['scheduled_at'] = self.scheduled_at.isoformat()
        if self.last_attempt:
            data['last_attempt'] = self.last_attempt.isoformat()
        return data


@dataclass
class AlertNotification:
    """Represents an alert notification"""
    alert_id: str
    severity: AlertSeverity
    title: str
    message: str
    technology_name: Optional[str]
    created_at: datetime
    metadata: Dict[str, Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['severity'] = self.severity.value
        data['created_at'] = self.created_at.isoformat()
        return data


class ChangeDetectionOrchestrator:
    """
    Main orchestrator that coordinates all change detection components,
    implements scheduling, monitoring, and alerting capabilities.
    """
    
    def __init__(self, config_dir: Optional[Path] = None):
        """Initialize the orchestrator"""
        self.config_dir = config_dir or Path(__file__).parent
        self.running = False
        self.shutdown_event = asyncio.Event()
        
        # Initialize components
        self.config_manager = ConfigManager(config_dir)
        self.mcp_integrator = MCPIntegrator(self.config_manager)
        self.storage = StorageInterface(self.config_manager)
        self.change_detector = ChangeDetectionEngine(
            self.config_manager, self.mcp_integrator, self.storage
        )
        self.change_validator = ChangeValidator(self.config_manager)
        
        # Load orchestration configuration
        self.orchestration_config = self._load_orchestration_config()
        
        # Task management
        self.detection_tasks: Dict[str, DetectionTask] = {}
        self.task_queue = asyncio.Queue()
        self.active_tasks: Dict[str, asyncio.Task] = {}
        
        # Scheduling
        self.scheduler = schedule
        self.scheduler_thread = None
        
        # Alerting and notifications
        self.alert_handlers: List[Callable] = []
        self.alert_history: List[AlertNotification] = []
        self.alert_cooldowns: Dict[str, datetime] = {}
        
        # Performance tracking
        self.orchestration_stats = {
            'total_detections': 0,
            'successful_detections': 0,
            'failed_detections': 0,
            'changes_detected': 0,
            'alerts_sent': 0,
            'average_detection_time': 0.0,
            'uptime_start': datetime.utcnow()
        }
        
        # Health monitoring
        self.last_health_check = None
        self.health_status = {
            'orchestrator_healthy': True,
            'components_healthy': True,
            'last_check': None,
            'issues': []
        }
        
        logger.info("Change Detection Orchestrator initialized successfully")
    
    def _load_orchestration_config(self) -> OrchestrationConfig:
        """Load orchestration configuration from config files or environment"""
        config = OrchestrationConfig()
        
        # Try to load from architecture config
        arch_config = self.config_manager.get_architecture_config()
        orchestration_settings = arch_config.get('orchestration_settings', {})
        
        if orchestration_settings:
            config.mode = OrchestrationMode(orchestration_settings.get('mode', 'scheduled'))
            config.check_interval_minutes = orchestration_settings.get('check_interval_minutes', 60)
            config.batch_size = orchestration_settings.get('batch_size', 5)
            config.max_concurrent_detections = orchestration_settings.get('max_concurrent_detections', 3)
            config.health_check_interval_minutes = orchestration_settings.get('health_check_interval_minutes', 10)
            config.alert_cooldown_minutes = orchestration_settings.get('alert_cooldown_minutes', 30)
            config.retry_failed_after_minutes = orchestration_settings.get('retry_failed_after_minutes', 120)
            config.max_retries = orchestration_settings.get('max_retries', 3)
        
        logger.info(f"Orchestration configured for {config.mode.value} mode")
        return config
    
    async def start(self):
        """Start the orchestrator"""
        if self.running:
            logger.warning("Orchestrator is already running")
            return
        
        self.running = True
        self.orchestration_stats['uptime_start'] = datetime.utcnow()
        
        logger.info("Starting Change Detection Orchestrator")
        
        try:
            # Initialize scheduling based on mode
            if self.orchestration_config.mode in [OrchestrationMode.CONTINUOUS, OrchestrationMode.SCHEDULED]:
                await self._setup_scheduling()
            
            # Start background tasks
            background_tasks = [
                asyncio.create_task(self._task_processor()),
                asyncio.create_task(self._health_monitor()),
                asyncio.create_task(self._performance_monitor())
            ]
            
            # Wait for shutdown signal
            await self.shutdown_event.wait()
            
            # Cleanup
            logger.info("Shutting down orchestrator...")
            for task in background_tasks:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            
            await self._cleanup()
            
        except Exception as e:
            logger.error(f"Error in orchestrator: {e}")
            raise
        finally:
            self.running = False
    
    async def stop(self):
        """Stop the orchestrator"""
        logger.info("Stopping Change Detection Orchestrator")
        self.running = False
        self.shutdown_event.set()
        
        if self.scheduler_thread:
            self.scheduler_thread.join(timeout=5)
    
    async def _setup_scheduling(self):
        """Setup scheduling based on configuration"""
        try:
            # Clear any existing schedules
            self.scheduler.clear()
            
            if self.orchestration_config.mode == OrchestrationMode.CONTINUOUS:
                # Schedule frequent checks for continuous mode
                interval = max(1, self.orchestration_config.check_interval_minutes // 4)
                self.scheduler.every(interval).minutes.do(self._schedule_detection_batch)
                
            elif self.orchestration_config.mode == OrchestrationMode.SCHEDULED:
                # Schedule regular checks
                self.scheduler.every(self.orchestration_config.check_interval_minutes).minutes.do(
                    self._schedule_detection_batch
                )
            
            # Schedule health checks
            self.scheduler.every(self.orchestration_config.health_check_interval_minutes).minutes.do(
                self._schedule_health_check
            )
            
            # Schedule retry of failed tasks
            self.scheduler.every(self.orchestration_config.retry_failed_after_minutes).minutes.do(
                self._schedule_retry_failed
            )
            
            # Start scheduler thread
            self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
            self.scheduler_thread.start()
            
            logger.info("Scheduling setup completed")
            
        except Exception as e:
            logger.error(f"Error setting up scheduling: {e}")
            raise
    
    def _run_scheduler(self):
        """Run the scheduler in a separate thread"""
        while self.running:
            try:
                self.scheduler.run_pending()
                time.sleep(1)
            except Exception as e:
                logger.error(f"Error in scheduler thread: {e}")
                time.sleep(5)
    
    def _schedule_detection_batch(self):
        """Schedule a batch of detection tasks"""
        try:
            # Get all technologies to monitor
            all_technologies = self.config_manager.get_all_technologies()
            
            # Create tasks for technologies that need checking
            current_time = datetime.utcnow()
            
            for tech_name, tech_config in all_technologies.items():
                # Check if technology should be monitored
                monitoring_config = tech_config.get('monitoring_config', {})
                if not monitoring_config.get('enabled', True):
                    continue
                
                # Check if we need to schedule this technology
                if self._should_schedule_technology(tech_name, current_time):
                    priority = self._calculate_task_priority(tech_config)
                    task = DetectionTask(
                        technology_name=tech_name,
                        scheduled_at=current_time,
                        priority=priority
                    )
                    
                    self.detection_tasks[tech_name] = task
                    asyncio.create_task(self.task_queue.put(task))
            
            logger.info(f"Scheduled {len(self.detection_tasks)} detection tasks")
            
        except Exception as e:
            logger.error(f"Error scheduling detection batch: {e}")
    
    def _schedule_health_check(self):
        """Schedule a health check"""
        if self.running:
            asyncio.create_task(self._perform_health_check())
    
    def _schedule_retry_failed(self):
        """Schedule retry of failed tasks"""
        try:
            current_time = datetime.utcnow()
            retry_cutoff = current_time - timedelta(minutes=self.orchestration_config.retry_failed_after_minutes)
            
            for tech_name, task in self.detection_tasks.items():
                if (task.status == "failed" and 
                    task.retry_count < self.orchestration_config.max_retries and
                    task.last_attempt and task.last_attempt < retry_cutoff):
                    
                    # Reset task for retry
                    task.status = "pending"
                    task.scheduled_at = current_time
                    asyncio.create_task(self.task_queue.put(task))
                    
                    logger.info(f"Scheduled retry for failed task: {tech_name}")
            
        except Exception as e:
            logger.error(f"Error scheduling retry of failed tasks: {e}")
    
    def _should_schedule_technology(self, tech_name: str, current_time: datetime) -> bool:
        """Determine if technology should be scheduled for detection"""
        try:
            # Check if task is already running
            if tech_name in self.active_tasks:
                return False
            
            # Check if task was recently completed
            existing_task = self.detection_tasks.get(tech_name)
            if existing_task and existing_task.status == "completed":
                # Get monitoring frequency
                tech_config = self.config_manager.get_technology_by_name(tech_name)
                if tech_config:
                    monitoring_config = tech_config.get('monitoring_config', {})
                    check_frequency = monitoring_config.get('check_frequency', '1h')
                    
                    # Parse frequency and check if enough time has passed
                    frequency_minutes = self._parse_frequency_to_minutes(check_frequency)
                    if existing_task.last_attempt:
                        time_since_last = (current_time - existing_task.last_attempt).total_seconds() / 60
                        if time_since_last < frequency_minutes:
                            return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error checking if technology should be scheduled: {e}")
            return False
    
    def _parse_frequency_to_minutes(self, frequency: str) -> int:
        """Parse frequency string to minutes"""
        try:
            frequency = frequency.lower().strip()
            
            if frequency.endswith('m'):
                return int(frequency[:-1])
            elif frequency.endswith('h'):
                return int(frequency[:-1]) * 60
            elif frequency.endswith('d'):
                return int(frequency[:-1]) * 24 * 60
            else:
                # Default to 60 minutes
                return 60
                
        except Exception:
            return 60
    
    def _calculate_task_priority(self, tech_config: Dict[str, Any]) -> int:
        """Calculate task priority based on technology configuration"""
        base_priority = 1
        
        # Higher priority for critical technologies
        criticality = tech_config.get('criticality', 'low')
        if criticality == 'high':
            base_priority += 3
        elif criticality == 'medium':
            base_priority += 1
        
        # Higher priority based on tier
        tier = tech_config.get('tier', 'tier_3_supplemental_technologies')
        if 'tier_1' in tier:
            base_priority += 3
        elif 'tier_2' in tier:
            base_priority += 2
        
        return base_priority
    
    async def _task_processor(self):
        """Process detection tasks from the queue"""
        logger.info("Starting task processor")
        
        while self.running or not self.task_queue.empty():
            try:
                # Get task from queue with timeout
                try:
                    task = await asyncio.wait_for(self.task_queue.get(), timeout=1.0)
                except asyncio.TimeoutError:
                    continue
                
                # Check if we have capacity to run more tasks
                if len(self.active_tasks) >= self.orchestration_config.max_concurrent_detections:
                    # Put task back in queue and wait
                    await self.task_queue.put(task)
                    await asyncio.sleep(5)
                    continue
                
                # Execute task
                task_coroutine = self._execute_detection_task(task)
                active_task = asyncio.create_task(task_coroutine)
                self.active_tasks[task.technology_name] = active_task
                
                # Don't wait for completion, let it run in background
                
            except Exception as e:
                logger.error(f"Error in task processor: {e}")
                await asyncio.sleep(1)
        
        logger.info("Task processor stopped")
    
    async def _execute_detection_task(self, task: DetectionTask):
        """Execute a single detection task"""
        tech_name = task.technology_name
        start_time = time.time()
        
        try:
            logger.info(f"Starting detection for {tech_name}")
            
            # Update task status
            task.status = "running"
            task.last_attempt = datetime.utcnow()
            
            # Perform change detection
            changes = await self.change_detector.detect_changes_for_technology(tech_name)
            
            # Validate detected changes
            validated_changes = []
            for change in changes:
                is_valid, adjusted_confidence = await self.change_validator.validate_change(change)
                if is_valid:
                    change.confidence_score = adjusted_confidence
                    validated_changes.append(change)
            
            # Store validated changes
            for change in validated_changes:
                success = await self.storage.store_change(change)
                if not success:
                    logger.error(f"Failed to store change for {tech_name}")
            
            # Update monitoring status
            await self.storage.update_monitoring_status(
                tech_name,
                last_checked=datetime.utcnow(),
                changes_detected=len(validated_changes)
            )
            
            # Send alerts for significant changes
            for change in validated_changes:
                await self._process_change_alert(change)
            
            # Update task status
            task.status = "completed"
            
            # Update orchestration stats
            self.orchestration_stats['total_detections'] += 1
            self.orchestration_stats['successful_detections'] += 1
            self.orchestration_stats['changes_detected'] += len(validated_changes)
            
            processing_time = time.time() - start_time
            self.orchestration_stats['average_detection_time'] = (
                (self.orchestration_stats['average_detection_time'] * 
                 (self.orchestration_stats['successful_detections'] - 1) + processing_time) /
                self.orchestration_stats['successful_detections']
            )
            
            logger.info(f"Completed detection for {tech_name}: {len(validated_changes)} changes found")
            
        except Exception as e:
            logger.error(f"Error executing detection task for {tech_name}: {e}")
            
            # Update task status
            task.status = "failed"
            task.retry_count += 1
            task.last_error = str(e)
            
            # Update orchestration stats
            self.orchestration_stats['total_detections'] += 1
            self.orchestration_stats['failed_detections'] += 1
            
            # Send error alert
            await self._send_alert(
                AlertSeverity.ERROR,
                f"Detection Failed: {tech_name}",
                f"Change detection failed for {tech_name}: {e}",
                tech_name
            )
            
        finally:
            # Remove from active tasks
            if tech_name in self.active_tasks:
                del self.active_tasks[tech_name]
    
    async def _process_change_alert(self, change: TechnologyChange):
        """Process alert for a detected change"""
        try:
            # Determine alert severity based on change characteristics
            severity = self._calculate_alert_severity(change)
            
            # Check alert cooldown
            cooldown_key = f"{change.technology_name}:{change.change_type.value}"
            if self._is_alert_on_cooldown(cooldown_key):
                return
            
            # Create alert message
            title = f"Change Detected: {change.technology_name}"
            message = self._format_change_alert_message(change)
            
            await self._send_alert(severity, title, message, change.technology_name, {
                'change_type': change.change_type.value,
                'impact_level': change.impact_level.value,
                'urgency_level': change.urgency_level.value,
                'confidence_score': change.confidence_score,
                'old_version': change.old_version,
                'new_version': change.new_version
            })
            
            # Set alert cooldown
            self.alert_cooldowns[cooldown_key] = datetime.utcnow()
            
        except Exception as e:
            logger.error(f"Error processing change alert: {e}")
    
    def _calculate_alert_severity(self, change: TechnologyChange) -> AlertSeverity:
        """Calculate alert severity based on change characteristics"""
        # Critical alerts
        if (change.impact_level.value == "critical" or 
            change.urgency_level.value == "immediate"):
            return AlertSeverity.CRITICAL
        
        # Error level alerts
        if (change.change_type.value in ["breaking_change", "security_update"] or
            change.impact_level.value == "high"):
            return AlertSeverity.ERROR
        
        # Warning level alerts
        if (change.change_type.value == "deprecation_warning" or
            change.impact_level.value == "medium"):
            return AlertSeverity.WARNING
        
        # Info level for everything else
        return AlertSeverity.INFO
    
    def _format_change_alert_message(self, change: TechnologyChange) -> str:
        """Format alert message for a change"""
        message_parts = [
            f"Technology: {change.technology_name}",
            f"Change Type: {change.change_type.value.replace('_', ' ').title()}",
            f"Impact Level: {change.impact_level.value.title()}",
            f"Urgency: {change.urgency_level.value.title()}",
            f"Confidence: {change.confidence_score:.2f}"
        ]
        
        if change.old_version and change.new_version:
            message_parts.append(f"Version: {change.old_version} → {change.new_version}")
        
        if change.change_description:
            message_parts.append(f"Description: {change.change_description}")
        
        if change.evidence:
            message_parts.append(f"Evidence: {', '.join(change.evidence[:3])}")
        
        return "\n".join(message_parts)
    
    def _is_alert_on_cooldown(self, cooldown_key: str) -> bool:
        """Check if alert is on cooldown"""
        if cooldown_key not in self.alert_cooldowns:
            return False
        
        cooldown_end = (self.alert_cooldowns[cooldown_key] + 
                       timedelta(minutes=self.orchestration_config.alert_cooldown_minutes))
        
        return datetime.utcnow() < cooldown_end
    
    async def _send_alert(self, severity: AlertSeverity, title: str, message: str,
                         technology_name: Optional[str] = None, metadata: Dict[str, Any] = None):
        """Send alert notification"""
        try:
            alert = AlertNotification(
                alert_id=f"{int(time.time())}-{hash(title) % 10000}",
                severity=severity,
                title=title,
                message=message,
                technology_name=technology_name,
                created_at=datetime.utcnow(),
                metadata=metadata or {}
            )
            
            # Add to alert history
            self.alert_history.append(alert)
            
            # Keep only recent alerts (last 1000)
            if len(self.alert_history) > 1000:
                self.alert_history = self.alert_history[-1000:]
            
            # Call alert handlers
            for handler in self.alert_handlers:
                try:
                    await handler(alert)
                except Exception as e:
                    logger.error(f"Error in alert handler: {e}")
            
            # Log alert
            log_level = {
                AlertSeverity.INFO: logging.INFO,
                AlertSeverity.WARNING: logging.WARNING,
                AlertSeverity.ERROR: logging.ERROR,
                AlertSeverity.CRITICAL: logging.CRITICAL
            }.get(severity, logging.INFO)
            
            logger.log(log_level, f"ALERT [{severity.value.upper()}] {title}: {message}")
            
            # Update stats
            self.orchestration_stats['alerts_sent'] += 1
            
        except Exception as e:
            logger.error(f"Error sending alert: {e}")
    
    async def _health_monitor(self):
        """Monitor system health"""
        logger.info("Starting health monitor")
        
        while self.running:
            try:
                await self._perform_health_check()
                await asyncio.sleep(self.orchestration_config.health_check_interval_minutes * 60)
            except Exception as e:
                logger.error(f"Error in health monitor: {e}")
                await asyncio.sleep(60)
        
        logger.info("Health monitor stopped")
    
    async def _perform_health_check(self):
        """Perform comprehensive health check"""
        try:
            logger.debug("Performing health check")
            
            issues = []
            components_healthy = True
            
            # Check storage health
            try:
                storage_health = await self.storage.health_check()
                if not storage_health.get('cache_healthy', False):
                    issues.append("Storage cache unhealthy")
                    components_healthy = False
                if not storage_health.get('storage_healthy', False):
                    issues.append("Storage backend unhealthy")
                    components_healthy = False
            except Exception as e:
                issues.append(f"Storage health check failed: {e}")
                components_healthy = False
            
            # Check MCP integrator health
            try:
                mcp_healthy = await self.mcp_integrator.health_check()
                if not mcp_healthy:
                    issues.append("MCP integrator unhealthy")
                    components_healthy = False
            except Exception as e:
                issues.append(f"MCP health check failed: {e}")
                components_healthy = False
            
            # Check configuration validity
            if not self.config_manager.is_configuration_valid():
                config_errors = self.config_manager.get_validation_errors()
                issues.extend([f"Config error: {error}" for error in config_errors[:3]])
                components_healthy = False
            
            # Check active tasks for stuck processes
            current_time = datetime.utcnow()
            stuck_tasks = []
            for tech_name, task in self.detection_tasks.items():
                if (task.status == "running" and task.last_attempt and 
                    (current_time - task.last_attempt).total_seconds() > 1800):  # 30 minutes
                    stuck_tasks.append(tech_name)
            
            if stuck_tasks:
                issues.append(f"Stuck detection tasks: {', '.join(stuck_tasks)}")
                components_healthy = False
            
            # Update health status
            self.health_status = {
                'orchestrator_healthy': self.running and components_healthy,
                'components_healthy': components_healthy,
                'last_check': current_time.isoformat(),
                'issues': issues
            }
            
            self.last_health_check = current_time
            
            # Send alert if health degraded
            if issues:
                await self._send_alert(
                    AlertSeverity.WARNING if components_healthy else AlertSeverity.ERROR,
                    "Health Check Issues",
                    f"Health check found {len(issues)} issues: {'; '.join(issues[:3])}"
                )
            
        except Exception as e:
            logger.error(f"Error performing health check: {e}")
            self.health_status = {
                'orchestrator_healthy': False,
                'components_healthy': False,
                'last_check': datetime.utcnow().isoformat(),
                'issues': [f"Health check failed: {e}"]
            }
    
    async def _performance_monitor(self):
        """Monitor performance metrics"""
        logger.info("Starting performance monitor")
        
        while self.running:
            try:
                # Store performance metrics
                current_time = datetime.utcnow()
                
                # Orchestrator metrics
                await self.storage.store_performance_metric(
                    "orchestrator_total_detections",
                    float(self.orchestration_stats['total_detections'])
                )
                
                await self.storage.store_performance_metric(
                    "orchestrator_success_rate",
                    (self.orchestration_stats['successful_detections'] / 
                     max(1, self.orchestration_stats['total_detections']))
                )
                
                await self.storage.store_performance_metric(
                    "orchestrator_average_detection_time",
                    self.orchestration_stats['average_detection_time']
                )
                
                await self.storage.store_performance_metric(
                    "orchestrator_active_tasks",
                    float(len(self.active_tasks))
                )
                
                await self.storage.store_performance_metric(
                    "orchestrator_pending_tasks",
                    float(self.task_queue.qsize())
                )
                
                # Component metrics
                mcp_stats = await self.mcp_integrator.get_performance_stats()
                for metric_name, value in mcp_stats.items():
                    if isinstance(value, (int, float)):
                        await self.storage.store_performance_metric(
                            f"mcp_{metric_name}",
                            float(value)
                        )
                
                storage_stats = await self.storage.get_storage_stats()
                await self.storage.store_performance_metric(
                    "storage_cache_hit_rate",
                    storage_stats.cache_hit_rate
                )
                
                # Wait for next monitoring cycle
                await asyncio.sleep(300)  # 5 minutes
                
            except Exception as e:
                logger.error(f"Error in performance monitor: {e}")
                await asyncio.sleep(60)
        
        logger.info("Performance monitor stopped")
    
    async def _cleanup(self):
        """Cleanup resources"""
        try:
            logger.info("Cleaning up orchestrator resources")
            
            # Cancel active tasks
            for tech_name, task in self.active_tasks.items():
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            
            # Close storage
            await self.storage.close()
            
            # Clear caches
            await self.mcp_integrator.clear_cache()
            
            logger.info("Orchestrator cleanup completed")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
    
    # Public API methods
    
    def add_alert_handler(self, handler: Callable[[AlertNotification], None]):
        """Add a custom alert handler"""
        self.alert_handlers.append(handler)
        logger.info("Added custom alert handler")
    
    async def trigger_detection(self, technology_name: str) -> bool:
        """Manually trigger detection for a specific technology"""
        try:
            tech_config = self.config_manager.get_technology_by_name(technology_name)
            if not tech_config:
                logger.error(f"Technology not found: {technology_name}")
                return False
            
            task = DetectionTask(
                technology_name=technology_name,
                scheduled_at=datetime.utcnow(),
                priority=10  # High priority for manual triggers
            )
            
            await self.task_queue.put(task)
            self.detection_tasks[technology_name] = task
            
            logger.info(f"Manually triggered detection for {technology_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error triggering detection for {technology_name}: {e}")
            return False
    
    async def get_orchestration_status(self) -> Dict[str, Any]:
        """Get current orchestration status"""
        try:
            current_time = datetime.utcnow()
            uptime = (current_time - self.orchestration_stats['uptime_start']).total_seconds()
            
            return {
                'running': self.running,
                'mode': self.orchestration_config.mode.value,
                'uptime_seconds': uptime,
                'health_status': self.health_status,
                'statistics': self.orchestration_stats,
                'active_tasks': len(self.active_tasks),
                'pending_tasks': self.task_queue.qsize(),
                'total_tasks': len(self.detection_tasks),
                'recent_alerts': [alert.to_dict() for alert in self.alert_history[-10:]],
                'last_health_check': self.last_health_check.isoformat() if self.last_health_check else None
            }
            
        except Exception as e:
            logger.error(f"Error getting orchestration status: {e}")
            return {'error': str(e)}
    
    async def get_task_status(self, technology_name: str = None) -> Dict[str, Any]:
        """Get status of detection tasks"""
        try:
            if technology_name:
                task = self.detection_tasks.get(technology_name)
                return task.to_dict() if task else {'error': 'Task not found'}
            
            return {
                tech_name: task.to_dict()
                for tech_name, task in self.detection_tasks.items()
            }
            
        except Exception as e:
            logger.error(f"Error getting task status: {e}")
            return {'error': str(e)}


def setup_signal_handlers(orchestrator: ChangeDetectionOrchestrator):
    """Setup signal handlers for graceful shutdown"""
    def signal_handler(signum, frame):
        logger.info(f"Received signal {signum}, initiating graceful shutdown")
        asyncio.create_task(orchestrator.stop())
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


async def main():
    """Main entry point for running the orchestrator"""
    orchestrator = ChangeDetectionOrchestrator()
    
    # Setup signal handlers
    setup_signal_handlers(orchestrator)
    
    try:
        await orchestrator.start()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received")
    except Exception as e:
        logger.error(f"Orchestrator error: {e}")
    finally:
        await orchestrator.stop()


if __name__ == "__main__":
    asyncio.run(main())