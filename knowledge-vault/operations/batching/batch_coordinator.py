#!/usr/bin/env python3
"""
Batch Coordinator for Intelligent Batching System
Main orchestration component that coordinates adaptive batching, resource monitoring, and performance optimization.
"""

import asyncio
import time
import logging
from typing import Dict, List, Tuple, Optional, Any, Callable, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from contextlib import asynccontextmanager
import json
import yaml
from pathlib import Path

from .adaptive_batching import AdaptiveBatchingEngine, OperationType, PerformanceMetrics, BatchStrategy
from .resource_monitor import ResourceMonitor, SystemResources, ApplicationMetrics
from .performance_optimizer import PerformanceOptimizer, OptimizationTarget, PerformancePrediction

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class BatchJob:
    """Represents a batch job to be executed"""
    job_id: str
    operation_type: OperationType
    operations: List[Dict[str, Any]]
    priority: str = "normal"  # low, normal, high, critical
    max_retry_attempts: int = 3
    timeout_seconds: int = 300
    created_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    status: str = "pending"  # pending, running, completed, failed, cancelled
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    metrics: Optional[PerformanceMetrics] = None

@dataclass
class BatchExecutionResult:
    """Result of batch execution"""
    job_id: str
    success: bool
    processed_count: int
    failed_count: int
    execution_time: float
    throughput: float
    error_details: Optional[List[str]] = None
    performance_metrics: Optional[PerformanceMetrics] = None

class BatchCoordinator:
    """
    Main coordinator that orchestrates intelligent batching operations,
    integrating adaptive batching, resource monitoring, and performance optimization.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the batch coordinator"""
        self.config = self._load_config(config_path)
        
        # Initialize core components
        self.batching_engine = AdaptiveBatchingEngine(config_path)
        self.resource_monitor = ResourceMonitor(config_path, monitoring_interval=5.0)
        self.performance_optimizer = PerformanceOptimizer("models/batching/")
        
        # Job management
        self.job_queue: Dict[str, BatchJob] = {}
        self.active_jobs: Dict[str, BatchJob] = {}
        self.completed_jobs: List[BatchJob] = []
        self.job_counter = 0
        
        # Execution state
        self.coordinator_active = False
        self.max_concurrent_jobs = self.config.get('max_concurrent_jobs', 5)
        self.execution_thread: Optional[threading.Thread] = None
        self.executor = ThreadPoolExecutor(max_workers=self.max_concurrent_jobs)
        
        # Performance tracking
        self.execution_history: List[BatchExecutionResult] = []
        self.performance_dashboard: Dict[str, Any] = {}
        
        # Callbacks and hooks
        self.job_callbacks: Dict[str, List[Callable]] = {
            'job_started': [],
            'job_completed': [],
            'job_failed': [],
            'batch_optimized': []
        }
        
        # Circuit breaker state
        self.circuit_breaker_active = False
        self.circuit_breaker_reset_time: Optional[float] = None
        
        # Setup component integration
        self._setup_component_integration()
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load coordinator configuration"""
        default_config = {
            'max_concurrent_jobs': 5,
            'job_timeout_seconds': 300,
            'max_retry_attempts': 3,
            'circuit_breaker_threshold': 5,
            'circuit_breaker_timeout': 300,
            'performance_tracking_enabled': True,
            'auto_optimization_enabled': True,
            'dashboard_update_interval': 30
        }
        
        if config_path and Path(config_path).exists():
            try:
                with open(config_path, 'r') as f:
                    config_data = yaml.safe_load(f)
                default_config.update(config_data.get('coordinator', {}))
            except Exception as e:
                logger.warning(f"Failed to load config from {config_path}: {e}")
        
        return default_config
    
    def _setup_component_integration(self):
        """Setup integration between components"""
        # Resource monitor callbacks
        self.resource_monitor.register_callback(self._on_resource_update)
        self.resource_monitor.register_alert_callback(self._on_resource_alert)
    
    def start(self):
        """Start the batch coordinator"""
        if self.coordinator_active:
            logger.warning("Coordinator is already active")
            return
        
        logger.info("Starting batch coordinator...")
        
        # Start resource monitoring
        self.resource_monitor.start_monitoring()
        
        # Start coordinator execution loop
        self.coordinator_active = True
        self.execution_thread = threading.Thread(target=self._execution_loop, daemon=True)
        self.execution_thread.start()
        
        # Start performance dashboard updates
        if self.config.get('performance_tracking_enabled'):
            self._start_dashboard_updates()
        
        logger.info("Batch coordinator started successfully")
    
    def stop(self):
        """Stop the batch coordinator"""
        logger.info("Stopping batch coordinator...")
        
        self.coordinator_active = False
        
        # Stop resource monitoring
        self.resource_monitor.stop_monitoring()
        
        # Wait for execution thread
        if self.execution_thread:
            self.execution_thread.join(timeout=30)
        
        # Shutdown executor
        self.executor.shutdown(wait=True)
        
        logger.info("Batch coordinator stopped")
    
    def submit_job(self,
                  operations: List[Dict[str, Any]],
                  operation_type: OperationType,
                  priority: str = "normal",
                  job_id: Optional[str] = None) -> str:
        """Submit a new batch job"""
        if not job_id:
            self.job_counter += 1
            job_id = f"batch_job_{self.job_counter}_{int(time.time())}"
        
        # Create batch job
        job = BatchJob(
            job_id=job_id,
            operation_type=operation_type,
            operations=operations,
            priority=priority,
            max_retry_attempts=self.config.get('max_retry_attempts', 3),
            timeout_seconds=self.config.get('job_timeout_seconds', 300)
        )
        
        # Add to queue
        self.job_queue[job_id] = job
        
        logger.info(f"Submitted job {job_id} with {len(operations)} operations")
        return job_id
    
    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific job"""
        # Check active jobs
        if job_id in self.active_jobs:
            job = self.active_jobs[job_id]
        # Check queue
        elif job_id in self.job_queue:
            job = self.job_queue[job_id]
        # Check completed jobs
        else:
            completed_job = next((j for j in self.completed_jobs if j.job_id == job_id), None)
            if not completed_job:
                return None
            job = completed_job
        
        return {
            'job_id': job.job_id,
            'status': job.status,
            'operation_type': job.operation_type.value,
            'operation_count': len(job.operations),
            'priority': job.priority,
            'created_at': job.created_at,
            'started_at': job.started_at,
            'completed_at': job.completed_at,
            'execution_time': (job.completed_at - job.started_at) if job.started_at and job.completed_at else None,
            'result': job.result,
            'error': job.error
        }
    
    def cancel_job(self, job_id: str) -> bool:
        """Cancel a pending or active job"""
        # Cancel from queue
        if job_id in self.job_queue:
            job = self.job_queue.pop(job_id)
            job.status = "cancelled"
            self.completed_jobs.append(job)
            logger.info(f"Cancelled queued job {job_id}")
            return True
        
        # Cancel active job (more complex, would need execution framework support)
        if job_id in self.active_jobs:
            job = self.active_jobs[job_id]
            job.status = "cancelled"
            logger.info(f"Marked active job {job_id} for cancellation")
            return True
        
        return False
    
    def _execution_loop(self):
        """Main execution loop for processing batch jobs"""
        while self.coordinator_active:
            try:
                # Check circuit breaker
                if self._check_circuit_breaker():
                    time.sleep(5)
                    continue
                
                # Process pending jobs if we have capacity
                if len(self.active_jobs) < self.max_concurrent_jobs and self.job_queue:
                    self._start_next_job()
                
                # Check for completed jobs
                self._check_completed_jobs()
                
                # Update performance dashboard
                if self.config.get('performance_tracking_enabled'):
                    self._update_performance_dashboard()
                
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Execution loop error: {e}")
                time.sleep(5)
    
    def _start_next_job(self):
        """Start the next highest priority job"""
        if not self.job_queue:
            return
        
        # Sort jobs by priority and creation time
        priority_order = {'critical': 0, 'high': 1, 'normal': 2, 'low': 3}
        
        sorted_jobs = sorted(
            self.job_queue.values(),
            key=lambda j: (priority_order.get(j.priority, 4), j.created_at)
        )
        
        next_job = sorted_jobs[0]
        
        # Remove from queue and add to active jobs
        del self.job_queue[next_job.job_id]
        self.active_jobs[next_job.job_id] = next_job
        
        # Start job execution
        next_job.status = "running"
        next_job.started_at = time.time()
        
        # Submit to executor
        future = self.executor.submit(self._execute_job, next_job)
        next_job.future = future
        
        # Trigger callbacks
        self._trigger_callbacks('job_started', next_job)
        
        logger.info(f"Started job {next_job.job_id}")
    
    def _execute_job(self, job: BatchJob) -> BatchExecutionResult:
        """Execute a batch job with intelligent batching"""
        start_time = time.time()
        
        try:
            # Get current system metrics
            current_metrics = self._get_current_performance_metrics(job.operation_type)
            
            # Get optimization target based on priority
            optimization_target = self._create_optimization_target(job.priority)
            
            # Get intelligent batch recommendation
            features = self._create_feature_set(job, current_metrics)
            
            if self.config.get('auto_optimization_enabled'):
                prediction = self.performance_optimizer.predict_optimal_batch_size(
                    features, optimization_target
                )
                recommended_batch_size = prediction.predicted_batch_size
            else:
                recommended_batch_size = self.batching_engine.calculate_optimal_batch_size(
                    job.operation_type, current_metrics, len(job.operations)
                )
            
            # Split operations into optimized batches
            batches = await self._create_optimized_batches(
                job.operations, job.operation_type, recommended_batch_size
            )
            
            # Execute batches
            execution_results = await self._execute_batches(batches, job)
            
            # Calculate final metrics
            execution_time = time.time() - start_time
            total_processed = sum(r['processed'] for r in execution_results)
            total_failed = sum(r['failed'] for r in execution_results)
            throughput = total_processed / execution_time if execution_time > 0 else 0
            
            # Create result
            result = BatchExecutionResult(
                job_id=job.job_id,
                success=total_failed == 0,
                processed_count=total_processed,
                failed_count=total_failed,
                execution_time=execution_time,
                throughput=throughput,
                error_details=[r['error'] for r in execution_results if r.get('error')],
                performance_metrics=PerformanceMetrics(
                    success_rate=(total_processed / (total_processed + total_failed)) if (total_processed + total_failed) > 0 else 1.0,
                    average_response_time=execution_time * 1000 / len(batches) if batches else 0,
                    throughput=throughput,
                    error_rate=total_failed / (total_processed + total_failed) if (total_processed + total_failed) > 0 else 0
                )
            )
            
            # Update performance optimizer with results
            if self.config.get('auto_optimization_enabled'):
                self._update_optimizer_with_results(features, result)
            
            return result
            
        except Exception as e:
            logger.error(f"Job execution failed for {job.job_id}: {e}")
            return BatchExecutionResult(
                job_id=job.job_id,
                success=False,
                processed_count=0,
                failed_count=len(job.operations),
                execution_time=time.time() - start_time,
                throughput=0.0,
                error_details=[str(e)]
            )
    
    async def _create_optimized_batches(self,
                                      operations: List[Dict[str, Any]],
                                      operation_type: OperationType,
                                      batch_size: int) -> List[List[Dict[str, Any]]]:
        """Create optimized batches using the batching engine"""
        return await self.batching_engine.optimize_batch_sequence(operations, operation_type)
    
    async def _execute_batches(self,
                             batches: List[List[Dict[str, Any]]],
                             job: BatchJob) -> List[Dict[str, Any]]:
        """Execute batches with performance monitoring"""
        results = []
        
        for i, batch in enumerate(batches):
            batch_start = time.time()
            
            try:
                # Simulate batch execution (replace with actual MCP operations)
                await asyncio.sleep(0.1)  # Simulate processing time
                
                # Record successful batch
                batch_time = time.time() - batch_start
                results.append({
                    'batch_index': i,
                    'processed': len(batch),
                    'failed': 0,
                    'execution_time': batch_time,
                    'throughput': len(batch) / batch_time if batch_time > 0 else 0
                })
                
            except Exception as e:
                # Record failed batch
                batch_time = time.time() - batch_start
                results.append({
                    'batch_index': i,
                    'processed': 0,
                    'failed': len(batch),
                    'execution_time': batch_time,
                    'throughput': 0,
                    'error': str(e)
                })
        
        return results
    
    def _check_completed_jobs(self):
        """Check for completed active jobs and process results"""
        completed_job_ids = []
        
        for job_id, job in self.active_jobs.items():
            if hasattr(job, 'future') and job.future.done():
                try:
                    result = job.future.result()
                    job.status = "completed" if result.success else "failed"
                    job.completed_at = time.time()
                    job.result = result.__dict__
                    job.metrics = result.performance_metrics
                    
                    # Move to completed jobs
                    self.completed_jobs.append(job)
                    completed_job_ids.append(job_id)
                    
                    # Add to execution history
                    self.execution_history.append(result)
                    if len(self.execution_history) > 1000:
                        self.execution_history = self.execution_history[-1000:]
                    
                    # Trigger callbacks
                    if result.success:
                        self._trigger_callbacks('job_completed', job)
                    else:
                        self._trigger_callbacks('job_failed', job)
                    
                    logger.info(f"Job {job_id} completed: {result.success}")
                    
                except Exception as e:
                    job.status = "failed"
                    job.completed_at = time.time()
                    job.error = str(e)
                    self.completed_jobs.append(job)
                    completed_job_ids.append(job_id)
                    
                    self._trigger_callbacks('job_failed', job)
                    logger.error(f"Job {job_id} failed: {e}")
        
        # Remove completed jobs from active jobs
        for job_id in completed_job_ids:
            del self.active_jobs[job_id]
        
        # Cleanup old completed jobs
        if len(self.completed_jobs) > 1000:
            self.completed_jobs = self.completed_jobs[-1000:]
    
    def _get_current_performance_metrics(self, operation_type: OperationType) -> PerformanceMetrics:
        """Get current performance metrics from resource monitor"""
        current_metrics = self.resource_monitor.get_current_metrics()
        
        return PerformanceMetrics(
            success_rate=0.95,  # Default values, would be calculated from actual data
            average_response_time=200.0,
            throughput=50.0,
            error_rate=0.02,
            rate_limit_hits=0,
            cpu_usage=current_metrics['system']['cpu_percent'],
            memory_usage=current_metrics['system']['memory_percent'],
            network_latency=10.0
        )
    
    def _create_optimization_target(self, priority: str) -> OptimizationTarget:
        """Create optimization target based on job priority"""
        if priority == "critical":
            return OptimizationTarget(
                max_response_time=100.0,
                min_success_rate=0.99,
                priority="latency"
            )
        elif priority == "high":
            return OptimizationTarget(
                target_throughput=100.0,
                max_response_time=200.0,
                priority="throughput"
            )
        elif priority == "low":
            return OptimizationTarget(
                max_cpu_usage=60.0,
                max_memory_usage=70.0,
                priority="resource"
            )
        else:  # normal
            return OptimizationTarget(priority="balanced")
    
    def _create_feature_set(self, job: BatchJob, metrics: PerformanceMetrics) -> Dict[str, Any]:
        """Create feature set for performance optimizer"""
        return {
            'current_batch_size': 50,  # Default
            'pending_operations': len(job.operations),
            'cpu_usage': metrics.cpu_usage,
            'memory_usage': metrics.memory_usage,
            'network_latency': metrics.network_latency,
            'error_rate': metrics.error_rate,
            'rate_limit_hits': metrics.rate_limit_hits,
            'operation_type': job.operation_type.value,
            'historical_avg_throughput': metrics.throughput,
            'historical_avg_response_time': metrics.average_response_time,
            'system_load': 1.0  # Would be calculated from system metrics
        }
    
    def _update_optimizer_with_results(self, features: Dict[str, Any], result: BatchExecutionResult):
        """Update performance optimizer with execution results"""
        optimizer_results = {
            'optimal_batch_size': len(result.job_id),  # Would calculate from actual batch sizes used
            'throughput': result.throughput,
            'response_time': result.execution_time * 1000,  # Convert to milliseconds
            'cpu_usage': features['cpu_usage'],
            'memory_usage': features['memory_usage']
        }
        
        self.performance_optimizer.add_training_data(features, optimizer_results)
    
    def _check_circuit_breaker(self) -> bool:
        """Check and manage circuit breaker state"""
        if self.circuit_breaker_active:
            # Check if we should reset the circuit breaker
            if (self.circuit_breaker_reset_time and 
                time.time() >= self.circuit_breaker_reset_time):
                self.circuit_breaker_active = False
                self.circuit_breaker_reset_time = None
                logger.info("Circuit breaker reset")
                return False
            return True
        
        # Check if we should activate circuit breaker
        recent_failures = sum(1 for job in self.completed_jobs[-10:] if job.status == "failed")
        
        if recent_failures >= self.config.get('circuit_breaker_threshold', 5):
            self.circuit_breaker_active = True
            self.circuit_breaker_reset_time = time.time() + self.config.get('circuit_breaker_timeout', 300)
            logger.warning("Circuit breaker activated due to high failure rate")
            return True
        
        return False
    
    def _on_resource_update(self, sys_metrics, app_metrics):
        """Handle resource monitor updates"""
        # Update batching engine with current metrics
        performance_metrics = PerformanceMetrics(
            cpu_usage=sys_metrics.cpu_percent,
            memory_usage=sys_metrics.memory_percent,
            network_latency=10.0  # Would be calculated from network metrics
        )
        
        # Update for each operation type (simplified)
        for op_type in OperationType:
            self.batching_engine.update_performance_metrics(op_type, performance_metrics)
    
    def _on_resource_alert(self, level: str, resource_type: str, details: Dict[str, Any]):
        """Handle resource alerts"""
        logger.warning(f"Resource alert [{level}] {resource_type}: {details['message']}")
        
        # Implement adaptive responses to resource alerts
        if level == "critical":
            # Reduce concurrent job limit
            self.max_concurrent_jobs = max(1, self.max_concurrent_jobs // 2)
            logger.info(f"Reduced concurrent jobs to {self.max_concurrent_jobs}")
    
    def _trigger_callbacks(self, event_type: str, job: BatchJob):
        """Trigger registered callbacks for job events"""
        for callback in self.job_callbacks.get(event_type, []):
            try:
                callback(job)
            except Exception as e:
                logger.error(f"Callback error for {event_type}: {e}")
    
    def _start_dashboard_updates(self):
        """Start performance dashboard updates"""
        def update_dashboard():
            while self.coordinator_active:
                try:
                    self._update_performance_dashboard()
                    time.sleep(self.config.get('dashboard_update_interval', 30))
                except Exception as e:
                    logger.error(f"Dashboard update error: {e}")
                    time.sleep(30)
        
        dashboard_thread = threading.Thread(target=update_dashboard, daemon=True)
        dashboard_thread.start()
    
    def _update_performance_dashboard(self):
        """Update performance dashboard with current metrics"""
        try:
            current_metrics = self.resource_monitor.get_current_metrics()
            batching_summary = self.batching_engine.get_performance_summary()
            
            # Calculate job statistics
            total_jobs = len(self.completed_jobs)
            successful_jobs = sum(1 for job in self.completed_jobs if job.status == "completed")
            failed_jobs = sum(1 for job in self.completed_jobs if job.status == "failed")
            
            # Calculate average metrics from recent executions
            recent_executions = self.execution_history[-50:] if self.execution_history else []
            avg_throughput = sum(r.throughput for r in recent_executions) / len(recent_executions) if recent_executions else 0
            avg_execution_time = sum(r.execution_time for r in recent_executions) / len(recent_executions) if recent_executions else 0
            
            self.performance_dashboard = {
                'timestamp': time.time(),
                'coordinator_status': {
                    'active': self.coordinator_active,
                    'active_jobs': len(self.active_jobs),
                    'queued_jobs': len(self.job_queue),
                    'circuit_breaker_active': self.circuit_breaker_active
                },
                'job_statistics': {
                    'total_jobs': total_jobs,
                    'successful_jobs': successful_jobs,
                    'failed_jobs': failed_jobs,
                    'success_rate': successful_jobs / total_jobs if total_jobs > 0 else 0
                },
                'performance_metrics': {
                    'average_throughput': avg_throughput,
                    'average_execution_time': avg_execution_time,
                    'system_cpu_usage': current_metrics['system']['cpu_percent'],
                    'system_memory_usage': current_metrics['system']['memory_percent']
                },
                'batching_metrics': batching_summary,
                'optimization_insights': self.performance_optimizer.get_optimization_insights() if self.config.get('auto_optimization_enabled') else {}
            }
            
        except Exception as e:
            logger.error(f"Failed to update performance dashboard: {e}")
    
    def get_performance_dashboard(self) -> Dict[str, Any]:
        """Get current performance dashboard"""
        return self.performance_dashboard.copy()
    
    def register_callback(self, event_type: str, callback: Callable):
        """Register callback for job events"""
        if event_type in self.job_callbacks:
            self.job_callbacks[event_type].append(callback)
        else:
            logger.warning(f"Unknown event type: {event_type}")
    
    def get_queue_status(self) -> Dict[str, Any]:
        """Get current queue status"""
        return {
            'queued_jobs': len(self.job_queue),
            'active_jobs': len(self.active_jobs),
            'completed_jobs': len(self.completed_jobs),
            'queue_details': [
                {
                    'job_id': job.job_id,
                    'operation_type': job.operation_type.value,
                    'priority': job.priority,
                    'operation_count': len(job.operations),
                    'created_at': job.created_at,
                    'wait_time': time.time() - job.created_at
                }
                for job in self.job_queue.values()
            ]
        }
    
    async def execute_immediate_batch(self,
                                    operations: List[Dict[str, Any]],
                                    operation_type: OperationType,
                                    optimization_target: OptimizationTarget) -> BatchExecutionResult:
        """Execute a batch immediately without queuing"""
        job_id = f"immediate_{int(time.time())}"
        
        # Create temporary job
        temp_job = BatchJob(
            job_id=job_id,
            operation_type=operation_type,
            operations=operations,
            priority="high"
        )
        
        # Execute directly
        result = await asyncio.create_task(
            asyncio.to_thread(self._execute_job, temp_job)
        )
        
        return result

# Factory function
def create_batch_coordinator(config_path: Optional[str] = None) -> BatchCoordinator:
    """Create and configure a batch coordinator"""
    return BatchCoordinator(config_path)

if __name__ == "__main__":
    # Example usage
    coordinator = create_batch_coordinator()
    
    # Register event callbacks
    def on_job_completed(job):
        print(f"Job {job.job_id} completed successfully!")
    
    def on_job_failed(job):
        print(f"Job {job.job_id} failed: {job.error}")
    
    coordinator.register_callback('job_completed', on_job_completed)
    coordinator.register_callback('job_failed', on_job_failed)
    
    try:
        # Start coordinator
        coordinator.start()
        
        # Submit some test jobs
        operations = [{'data': f'item_{i}'} for i in range(100)]
        job_id = coordinator.submit_job(operations, OperationType.READ, "normal")
        
        print(f"Submitted job: {job_id}")
        
        # Monitor for a while
        time.sleep(30)
        
        # Get status
        status = coordinator.get_job_status(job_id)
        print("Job Status:", json.dumps(status, indent=2))
        
        # Get performance dashboard
        dashboard = coordinator.get_performance_dashboard()
        print("Performance Dashboard:", json.dumps(dashboard, indent=2))
        
    finally:
        coordinator.stop()