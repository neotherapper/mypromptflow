#!/usr/bin/env python3
"""
Pipeline Orchestrator
AI Knowledge Lifecycle Orchestrator - Main pipeline coordination engine

This module provides the core orchestration engine that coordinates the automated knowledge update
pipeline from change detection through impact analysis, approval workflows, and update execution.
"""

import asyncio
import logging
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Set
from enum import Enum
from dataclasses import dataclass, asdict
from pathlib import Path
import json
import yaml

from .approval_engine import ApprovalEngine, ApprovalRequest, ApprovalStatus
from .impact_analyzer import ImpactAnalyzer, ImpactAssessment
from .update_executor import UpdateExecutor, UpdateResult, UpdateStatus
from ..change_detection.change_detector import TechnologyChange, ChangeType, ImpactLevel, UrgencyLevel
from ..knowledge_vault_integration import KnowledgeVaultIntegration

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PipelineStatus(Enum):
    """Pipeline execution status"""
    IDLE = "idle"
    PROCESSING = "processing"
    ERROR = "error"
    MAINTENANCE = "maintenance"


class PipelineStage(Enum):
    """Pipeline processing stages"""
    CHANGE_DETECTION = "change_detection"
    IMPACT_ANALYSIS = "impact_analysis"
    APPROVAL_PROCESSING = "approval_processing"
    UPDATE_EXECUTION = "update_execution"
    VALIDATION = "validation"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class PipelineExecution:
    """Represents a pipeline execution instance"""
    execution_id: str
    trigger_change: TechnologyChange
    stage: PipelineStage
    status: PipelineStatus
    started_at: datetime
    updated_at: datetime
    error_details: Optional[str] = None
    impact_assessment: Optional[ImpactAssessment] = None
    approval_request: Optional[ApprovalRequest] = None
    update_results: Optional[List[UpdateResult]] = None
    quality_metrics: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['stage'] = self.stage.value
        data['status'] = self.status.value
        data['started_at'] = self.started_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        
        if self.impact_assessment:
            data['impact_assessment'] = self.impact_assessment.to_dict()
        if self.approval_request:
            data['approval_request'] = self.approval_request.to_dict()
        if self.update_results:
            data['update_results'] = [result.to_dict() for result in self.update_results]
            
        return data


class CircuitBreaker:
    """Circuit breaker pattern implementation for reliability"""
    
    def __init__(self, failure_threshold: int = 5, timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.state = "closed"  # closed, open, half-open
    
    def can_execute(self) -> bool:
        """Check if execution is allowed"""
        if self.state == "closed":
            return True
        elif self.state == "open":
            if (datetime.utcnow() - self.last_failure_time).seconds >= self.timeout:
                self.state = "half-open"
                return True
            return False
        elif self.state == "half-open":
            return True
        return False
    
    def record_success(self):
        """Record successful execution"""
        self.failure_count = 0
        self.state = "closed"
    
    def record_failure(self):
        """Record failed execution"""
        self.failure_count += 1
        self.last_failure_time = datetime.utcnow()
        
        if self.failure_count >= self.failure_threshold:
            self.state = "open"


class PipelineOrchestrator:
    """
    Main pipeline orchestration engine that coordinates the automated knowledge update pipeline
    """
    
    def __init__(self, config_path: str, base_path: str = None):
        """Initialize the pipeline orchestrator"""
        self.config_path = Path(config_path)
        self.base_path = Path(base_path or "/Users/georgiospilitsoglou/Developer/projects/mypromptflow")
        
        # Load configuration
        self.config = self._load_config()
        
        # Initialize components
        self.knowledge_vault = KnowledgeVaultIntegration(str(self.base_path))
        self.approval_engine = ApprovalEngine(self.config.get('approval', {}))
        self.impact_analyzer = ImpactAnalyzer(self.knowledge_vault, self.config.get('impact_analysis', {}))
        self.update_executor = UpdateExecutor(self.knowledge_vault, self.config.get('update_execution', {}))
        
        # Pipeline state
        self.status = PipelineStatus.IDLE
        self.active_executions: Dict[str, PipelineExecution] = {}
        self.execution_history: List[PipelineExecution] = []
        
        # Circuit breakers for each stage
        self.circuit_breakers = {
            PipelineStage.IMPACT_ANALYSIS: CircuitBreaker(),
            PipelineStage.APPROVAL_PROCESSING: CircuitBreaker(),
            PipelineStage.UPDATE_EXECUTION: CircuitBreaker(),
            PipelineStage.VALIDATION: CircuitBreaker()
        }
        
        # Performance tracking
        self.performance_metrics = {
            'total_executions': 0,
            'successful_executions': 0,
            'failed_executions': 0,
            'average_processing_time': 0.0,
            'stage_performance': {stage.value: {'count': 0, 'avg_time': 0.0, 'failure_rate': 0.0} 
                                 for stage in PipelineStage}
        }
        
        logger.info("Pipeline Orchestrator initialized successfully")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load pipeline configuration"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    return yaml.safe_load(f)
            else:
                logger.warning(f"Config file not found: {self.config_path}, using defaults")
                return self._get_default_config()
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            'pipeline': {
                'max_concurrent_executions': 5,
                'execution_timeout': 3600,  # 1 hour
                'retry_attempts': 3,
                'retry_delay': 30
            },
            'approval': {
                'auto_approve_low_impact': True,
                'require_approval_threshold': 'medium',
                'approval_timeout': 86400,  # 24 hours
                'emergency_bypass_enabled': True
            },
            'impact_analysis': {
                'analysis_depth': 'comprehensive',
                'dependency_traversal_depth': 3,
                'confidence_threshold': 0.7,
                'parallel_analysis': True
            },
            'update_execution': {
                'batch_size': 10,
                'validation_enabled': True,
                'rollback_on_failure': True,
                'backup_enabled': True
            },
            'monitoring': {
                'metrics_enabled': True,
                'health_check_interval': 300,
                'alert_thresholds': {
                    'failure_rate': 0.2,
                    'processing_time': 1800
                }
            }
        }
    
    async def process_change(self, change: TechnologyChange) -> str:
        """
        Process a detected technology change through the complete pipeline
        
        Args:
            change: Detected technology change to process
            
        Returns:
            Execution ID for tracking
        """
        execution_id = str(uuid.uuid4())
        
        try:
            # Check if pipeline can handle more executions
            if len(self.active_executions) >= self.config['pipeline']['max_concurrent_executions']:
                logger.warning(f"Pipeline at capacity, queuing change: {change.technology_name}")
                # In a production system, this would be queued
                raise Exception("Pipeline at capacity")
            
            # Create pipeline execution
            execution = PipelineExecution(
                execution_id=execution_id,
                trigger_change=change,
                stage=PipelineStage.CHANGE_DETECTION,
                status=PipelineStatus.PROCESSING,
                started_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            self.active_executions[execution_id] = execution
            
            logger.info(f"Starting pipeline execution {execution_id} for {change.technology_name}")
            
            # Execute pipeline stages
            await self._execute_pipeline(execution)
            
            return execution_id
            
        except Exception as e:
            logger.error(f"Error processing change: {e}")
            if execution_id in self.active_executions:
                execution = self.active_executions[execution_id]
                execution.status = PipelineStatus.ERROR
                execution.error_details = str(e)
                execution.updated_at = datetime.utcnow()
            raise
    
    async def _execute_pipeline(self, execution: PipelineExecution):
        """Execute the complete pipeline for a single change"""
        start_time = time.time()
        
        try:
            # Stage 1: Impact Analysis
            await self._execute_impact_analysis(execution)
            
            # Stage 2: Approval Processing
            await self._execute_approval_processing(execution)
            
            # Stage 3: Update Execution (if approved)
            if execution.approval_request and execution.approval_request.status == ApprovalStatus.APPROVED:
                await self._execute_updates(execution)
                
                # Stage 4: Validation
                await self._execute_validation(execution)
            
            # Mark as completed
            execution.stage = PipelineStage.COMPLETED
            execution.status = PipelineStatus.IDLE
            execution.updated_at = datetime.utcnow()
            
            # Update performance metrics
            processing_time = time.time() - start_time
            self._update_performance_metrics(execution, processing_time, success=True)
            
            logger.info(f"Pipeline execution {execution.execution_id} completed successfully in {processing_time:.2f}s")
            
        except Exception as e:
            execution.stage = PipelineStage.FAILED
            execution.status = PipelineStatus.ERROR
            execution.error_details = str(e)
            execution.updated_at = datetime.utcnow()
            
            processing_time = time.time() - start_time
            self._update_performance_metrics(execution, processing_time, success=False)
            
            logger.error(f"Pipeline execution {execution.execution_id} failed: {e}")
            raise
        
        finally:
            # Move to history and cleanup
            self.execution_history.append(execution)
            if execution.execution_id in self.active_executions:
                del self.active_executions[execution.execution_id]
            
            # Limit history size
            if len(self.execution_history) > 1000:
                self.execution_history = self.execution_history[-500:]
    
    async def _execute_impact_analysis(self, execution: PipelineExecution):
        """Execute impact analysis stage"""
        stage = PipelineStage.IMPACT_ANALYSIS
        
        if not self.circuit_breakers[stage].can_execute():
            raise Exception(f"Circuit breaker open for {stage.value}")
        
        execution.stage = stage
        execution.updated_at = datetime.utcnow()
        
        try:
            logger.info(f"Executing impact analysis for {execution.trigger_change.technology_name}")
            
            impact_assessment = await self.impact_analyzer.analyze_change_impact(
                execution.trigger_change
            )
            
            execution.impact_assessment = impact_assessment
            self.circuit_breakers[stage].record_success()
            
            # Store impact assessment in Knowledge Vault
            await self._store_impact_assessment(execution.execution_id, impact_assessment)
            
            logger.info(f"Impact analysis completed: {impact_assessment.affected_files_count} files affected")
            
        except Exception as e:
            self.circuit_breakers[stage].record_failure()
            logger.error(f"Impact analysis failed: {e}")
            raise
    
    async def _execute_approval_processing(self, execution: PipelineExecution):
        """Execute approval processing stage"""
        stage = PipelineStage.APPROVAL_PROCESSING
        
        if not self.circuit_breakers[stage].can_execute():
            raise Exception(f"Circuit breaker open for {stage.value}")
        
        execution.stage = stage
        execution.updated_at = datetime.utcnow()
        
        try:
            logger.info(f"Processing approval for {execution.trigger_change.technology_name}")
            
            approval_request = await self.approval_engine.process_approval_request(
                execution.trigger_change,
                execution.impact_assessment
            )
            
            execution.approval_request = approval_request
            self.circuit_breakers[stage].record_success()
            
            # Store approval request in Knowledge Vault
            await self._store_approval_request(execution.execution_id, approval_request)
            
            logger.info(f"Approval processing completed: {approval_request.status.value}")
            
        except Exception as e:
            self.circuit_breakers[stage].record_failure()
            logger.error(f"Approval processing failed: {e}")
            raise
    
    async def _execute_updates(self, execution: PipelineExecution):
        """Execute update execution stage"""
        stage = PipelineStage.UPDATE_EXECUTION
        
        if not self.circuit_breakers[stage].can_execute():
            raise Exception(f"Circuit breaker open for {stage.value}")
        
        execution.stage = stage
        execution.updated_at = datetime.utcnow()
        
        try:
            logger.info(f"Executing updates for {execution.trigger_change.technology_name}")
            
            update_results = await self.update_executor.execute_updates(
                execution.trigger_change,
                execution.impact_assessment,
                execution.approval_request
            )
            
            execution.update_results = update_results
            self.circuit_breakers[stage].record_success()
            
            # Store update results in Knowledge Vault
            await self._store_update_results(execution.execution_id, update_results)
            
            successful_updates = len([r for r in update_results if r.status == UpdateStatus.SUCCESS])
            logger.info(f"Update execution completed: {successful_updates}/{len(update_results)} successful")
            
        except Exception as e:
            self.circuit_breakers[stage].record_failure()
            logger.error(f"Update execution failed: {e}")
            raise
    
    async def _execute_validation(self, execution: PipelineExecution):
        """Execute validation stage"""
        stage = PipelineStage.VALIDATION
        
        if not self.circuit_breakers[stage].can_execute():
            raise Exception(f"Circuit breaker open for {stage.value}")
        
        execution.stage = stage
        execution.updated_at = datetime.utcnow()
        
        try:
            logger.info(f"Validating updates for {execution.trigger_change.technology_name}")
            
            # Validate update results
            validation_results = await self._validate_updates(execution.update_results)
            
            execution.quality_metrics = validation_results
            self.circuit_breakers[stage].record_success()
            
            # Store validation results
            await self._store_validation_results(execution.execution_id, validation_results)
            
            if validation_results['overall_quality_score'] < self.config['update_execution'].get('min_quality_score', 0.8):
                logger.warning(f"Validation quality below threshold: {validation_results['overall_quality_score']}")
                
                if self.config['update_execution'].get('rollback_on_failure', True):
                    await self._initiate_rollback(execution)
            
            logger.info(f"Validation completed: quality score {validation_results['overall_quality_score']:.2f}")
            
        except Exception as e:
            self.circuit_breakers[stage].record_failure()
            logger.error(f"Validation failed: {e}")
            raise
    
    async def _validate_updates(self, update_results: List[UpdateResult]) -> Dict[str, Any]:
        """Validate update results quality"""
        validation_results = {
            'total_updates': len(update_results),
            'successful_updates': 0,
            'failed_updates': 0,
            'quality_scores': [],
            'overall_quality_score': 0.0,
            'validation_timestamp': datetime.utcnow().isoformat()
        }
        
        for result in update_results:
            if result.status == UpdateStatus.SUCCESS:
                validation_results['successful_updates'] += 1
                if result.quality_score:
                    validation_results['quality_scores'].append(result.quality_score)
            else:
                validation_results['failed_updates'] += 1
        
        # Calculate overall quality score
        if validation_results['quality_scores']:
            validation_results['overall_quality_score'] = sum(validation_results['quality_scores']) / len(validation_results['quality_scores'])
        
        return validation_results
    
    async def _initiate_rollback(self, execution: PipelineExecution):
        """Initiate rollback of failed updates"""
        logger.warning(f"Initiating rollback for execution {execution.execution_id}")
        
        try:
            rollback_results = await self.update_executor.rollback_updates(execution.update_results)
            
            # Update execution with rollback information
            execution.quality_metrics['rollback_initiated'] = True
            execution.quality_metrics['rollback_results'] = [r.to_dict() for r in rollback_results]
            
            successful_rollbacks = len([r for r in rollback_results if r.status == UpdateStatus.SUCCESS])
            logger.info(f"Rollback completed: {successful_rollbacks}/{len(rollback_results)} successful")
            
        except Exception as e:
            logger.error(f"Rollback failed: {e}")
            execution.error_details = f"Original execution and rollback failed: {e}"
    
    async def _store_impact_assessment(self, execution_id: str, assessment: ImpactAssessment):
        """Store impact assessment in Knowledge Vault"""
        try:
            # Create knowledge update entry
            update_data = {
                'update_title': f"Impact assessment for {assessment.technology_name}",
                'trigger_event': 'technology_change',
                'affected_file_path': 'multiple',
                'affected_file_type': 'various',
                'update_description': f"Impact assessment found {assessment.affected_files_count} affected files",
                'update_type': 'impact_analysis',
                'update_scope': assessment.impact_level.value,
                'workflow_status': 'impact_assessed',
                'update_priority': assessment.urgency_level.value,
                'related_technology': assessment.technology_name,
                'execution_id': execution_id
            }
            
            await asyncio.to_thread(self.knowledge_vault.create_knowledge_update, update_data)
            
        except Exception as e:
            logger.error(f"Error storing impact assessment: {e}")
    
    async def _store_approval_request(self, execution_id: str, request: ApprovalRequest):
        """Store approval request in Knowledge Vault"""
        try:
            # Update the knowledge update with approval information
            updates = await asyncio.to_thread(
                self.knowledge_vault.query_updates, 
                {'execution_id': execution_id}
            )
            
            if updates:
                update = updates[0]
                update['workflow_status'] = request.status.value
                update['approval_required'] = request.requires_approval
                update['approval_justification'] = request.justification
                
                await asyncio.to_thread(self.knowledge_vault._save_item, 'knowledge_updates', update)
            
        except Exception as e:
            logger.error(f"Error storing approval request: {e}")
    
    async def _store_update_results(self, execution_id: str, results: List[UpdateResult]):
        """Store update results in Knowledge Vault"""
        try:
            for result in results:
                # Create individual update entries
                update_data = {
                    'update_title': f"Update for {result.file_path}",
                    'trigger_event': 'approved_change',
                    'affected_file_path': result.file_path,
                    'affected_file_type': result.file_type,
                    'update_description': result.changes_made or 'Automated update',
                    'update_type': 'automated_update',
                    'update_scope': 'file',
                    'workflow_status': result.status.value,
                    'update_priority': 'medium',
                    'execution_id': execution_id,
                    'quality_score': result.quality_score
                }
                
                await asyncio.to_thread(self.knowledge_vault.create_knowledge_update, update_data)
            
        except Exception as e:
            logger.error(f"Error storing update results: {e}")
    
    async def _store_validation_results(self, execution_id: str, results: Dict[str, Any]):
        """Store validation results in Knowledge Vault"""
        try:
            # Update the main knowledge update with validation results
            updates = await asyncio.to_thread(
                self.knowledge_vault.query_updates,
                {'execution_id': execution_id, 'update_type': 'impact_analysis'}
            )
            
            if updates:
                update = updates[0]
                update['workflow_status'] = 'completed'
                update['validation_results'] = results
                update['final_quality_score'] = results['overall_quality_score']
                
                await asyncio.to_thread(self.knowledge_vault._save_item, 'knowledge_updates', update)
            
        except Exception as e:
            logger.error(f"Error storing validation results: {e}")
    
    def _update_performance_metrics(self, execution: PipelineExecution, processing_time: float, success: bool):
        """Update performance metrics"""
        self.performance_metrics['total_executions'] += 1
        
        if success:
            self.performance_metrics['successful_executions'] += 1
        else:
            self.performance_metrics['failed_executions'] += 1
        
        # Update average processing time
        total_executions = self.performance_metrics['total_executions']
        current_avg = self.performance_metrics['average_processing_time']
        self.performance_metrics['average_processing_time'] = (
            (current_avg * (total_executions - 1) + processing_time) / total_executions
        )
        
        # Update stage performance
        stage_key = execution.stage.value
        stage_metrics = self.performance_metrics['stage_performance'][stage_key]
        stage_metrics['count'] += 1
        
        # Update stage average time
        stage_avg = stage_metrics['avg_time']
        stage_count = stage_metrics['count']
        stage_metrics['avg_time'] = (stage_avg * (stage_count - 1) + processing_time) / stage_count
        
        # Update failure rate
        if not success:
            failures = stage_metrics.get('failures', 0) + 1
            stage_metrics['failures'] = failures
            stage_metrics['failure_rate'] = failures / stage_count
    
    async def get_pipeline_status(self) -> Dict[str, Any]:
        """Get current pipeline status"""
        return {
            'status': self.status.value,
            'active_executions': len(self.active_executions),
            'execution_history_count': len(self.execution_history),
            'performance_metrics': self.performance_metrics,
            'circuit_breaker_status': {
                stage.value: {
                    'state': breaker.state,
                    'failure_count': breaker.failure_count,
                    'last_failure': breaker.last_failure_time.isoformat() if breaker.last_failure_time else None
                }
                for stage, breaker in self.circuit_breakers.items()
            },
            'timestamp': datetime.utcnow().isoformat()
        }
    
    async def get_execution_status(self, execution_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific execution"""
        # Check active executions
        if execution_id in self.active_executions:
            return self.active_executions[execution_id].to_dict()
        
        # Check history
        for execution in self.execution_history:
            if execution.execution_id == execution_id:
                return execution.to_dict()
        
        return None
    
    async def cancel_execution(self, execution_id: str) -> bool:
        """Cancel an active execution"""
        if execution_id in self.active_executions:
            execution = self.active_executions[execution_id]
            execution.status = PipelineStatus.ERROR
            execution.error_details = "Execution cancelled by user"
            execution.updated_at = datetime.utcnow()
            
            logger.info(f"Execution {execution_id} cancelled")
            return True
        
        return False
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform health check"""
        health_status = {
            'overall_health': 'healthy',
            'pipeline_status': self.status.value,
            'active_executions': len(self.active_executions),
            'circuit_breakers': {},
            'performance_health': {},
            'timestamp': datetime.utcnow().isoformat()
        }
        
        # Check circuit breakers
        unhealthy_breakers = []
        for stage, breaker in self.circuit_breakers.items():
            health_status['circuit_breakers'][stage.value] = breaker.state
            if breaker.state == 'open':
                unhealthy_breakers.append(stage.value)
        
        # Check performance metrics
        failure_rate = (self.performance_metrics['failed_executions'] / 
                       max(self.performance_metrics['total_executions'], 1))
        avg_processing_time = self.performance_metrics['average_processing_time']
        
        health_status['performance_health'] = {
            'failure_rate': failure_rate,
            'average_processing_time': avg_processing_time,
            'failure_rate_healthy': failure_rate < self.config['monitoring']['alert_thresholds']['failure_rate'],
            'processing_time_healthy': avg_processing_time < self.config['monitoring']['alert_thresholds']['processing_time']
        }
        
        # Determine overall health
        if (unhealthy_breakers or 
            failure_rate >= self.config['monitoring']['alert_thresholds']['failure_rate'] or
            avg_processing_time >= self.config['monitoring']['alert_thresholds']['processing_time']):
            health_status['overall_health'] = 'unhealthy'
            health_status['issues'] = {
                'unhealthy_circuit_breakers': unhealthy_breakers,
                'high_failure_rate': failure_rate >= self.config['monitoring']['alert_thresholds']['failure_rate'],
                'slow_processing': avg_processing_time >= self.config['monitoring']['alert_thresholds']['processing_time']
            }
        
        return health_status
    
    async def shutdown(self):
        """Gracefully shutdown the pipeline"""
        logger.info("Shutting down pipeline orchestrator")
        
        self.status = PipelineStatus.MAINTENANCE
        
        # Wait for active executions to complete (with timeout)
        timeout = 300  # 5 minutes
        start_time = time.time()
        
        while self.active_executions and (time.time() - start_time) < timeout:
            logger.info(f"Waiting for {len(self.active_executions)} active executions to complete")
            await asyncio.sleep(5)
        
        # Force cancel remaining executions
        for execution_id in list(self.active_executions.keys()):
            await self.cancel_execution(execution_id)
        
        logger.info("Pipeline orchestrator shutdown complete")


async def main():
    """Main function for testing"""
    try:
        # Initialize orchestrator
        config_path = "/Users/georgiospilitsoglou/Developer/projects/mypromptflow/projects/ai-knowledge-lifecycle-orchestrator/update-pipeline/pipeline_config.yaml"
        orchestrator = PipelineOrchestrator(config_path)
        
        # Health check
        health = await orchestrator.health_check()
        print("Pipeline Health Check:")
        print(json.dumps(health, indent=2))
        
        # Status check
        status = await orchestrator.get_pipeline_status()
        print("\nPipeline Status:")
        print(json.dumps(status, indent=2))
        
    except Exception as e:
        print(f"Error testing pipeline orchestrator: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(asyncio.run(main()))