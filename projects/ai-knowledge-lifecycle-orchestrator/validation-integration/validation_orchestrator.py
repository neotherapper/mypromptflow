#!/usr/bin/env python3
"""
Validation Orchestrator
AI Knowledge Lifecycle Orchestrator - Validation workflow coordination

This module orchestrates the complete validation workflow, coordinating between
the framework connector, quality monitor, and rollback manager for seamless
integration with the update pipeline.
"""

import asyncio
import logging
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
import json

try:
    from .framework_connector import AIInstructionFrameworkConnector, FrameworkValidationResult, ValidationType
    from .quality_monitor import QualityMonitor, QualityAlert, MonitoringMode
    from .rollback_manager import RollbackManager, RollbackDecision, RollbackReason
except ImportError:
    from framework_connector import AIInstructionFrameworkConnector, FrameworkValidationResult, ValidationType
    from quality_monitor import QualityMonitor, QualityAlert, MonitoringMode
    from rollback_manager import RollbackManager, RollbackDecision, RollbackReason

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ValidationPhase(Enum):
    """Validation workflow phases"""
    PRE_UPDATE = "pre_update"
    DURING_UPDATE = "during_update"
    POST_UPDATE = "post_update"
    QUALITY_VERIFICATION = "quality_verification"
    ROLLBACK_ASSESSMENT = "rollback_assessment"


class ValidationStatus(Enum):
    """Overall validation status"""
    APPROVED = "approved"
    CONDITIONAL_APPROVAL = "conditional_approval"
    REJECTED = "rejected"
    ROLLBACK_REQUIRED = "rollback_required"
    VALIDATION_ERROR = "validation_error"


@dataclass
class ValidationWorkflowResult:
    """Complete validation workflow result"""
    file_path: str
    validation_phase: ValidationPhase
    overall_status: ValidationStatus
    framework_result: Optional[FrameworkValidationResult]
    quality_impact: Optional[Dict[str, Any]]
    rollback_decision: Optional[RollbackDecision]
    workflow_duration: float
    recommendations: List[str]
    alerts_generated: List[QualityAlert]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['validation_phase'] = self.validation_phase.value
        data['overall_status'] = self.overall_status.value
        if self.framework_result:
            data['framework_result'] = self.framework_result.to_dict()
        if self.rollback_decision:
            data['rollback_decision'] = self.rollback_decision.to_dict()
        data['alerts_generated'] = [alert.to_dict() for alert in self.alerts_generated]
        return data


class ValidationOrchestrator:
    """
    Orchestrator for complete validation workflow
    Coordinates framework validation, quality monitoring, and rollback decisions
    """
    
    def __init__(self, framework_connector: AIInstructionFrameworkConnector, 
                 quality_monitor: QualityMonitor, rollback_manager: RollbackManager, 
                 config: Dict[str, Any]):
        """Initialize the validation orchestrator"""
        self.framework_connector = framework_connector
        self.quality_monitor = quality_monitor
        self.rollback_manager = rollback_manager
        self.config = config
        
        # Workflow configuration
        self.enable_quality_monitoring = config.get('enable_quality_monitoring', True)
        self.enable_automatic_rollback = config.get('enable_automatic_rollback', True)
        self.quality_preservation_threshold = config.get('quality_preservation_threshold', 5.0)
        self.validation_timeout = config.get('validation_timeout', 120)  # seconds
        
        # Orchestration state
        self.active_workflows: Dict[str, asyncio.Task] = {}
        self.workflow_history: List[ValidationWorkflowResult] = []
        
        # Performance metrics
        self.orchestration_metrics = {
            'total_workflows': 0,
            'approved_workflows': 0,
            'rejected_workflows': 0,
            'rollbacks_triggered': 0,
            'average_workflow_time': 0.0,
            'quality_improvements': 0,
            'quality_preservations': 0
        }
        
        logger.info("Validation Orchestrator initialized successfully")
    
    async def execute_pre_update_validation(self, file_paths: List[str]) -> List[ValidationWorkflowResult]:
        """Execute pre-update validation workflow"""
        logger.info(f"Executing pre-update validation for {len(file_paths)} files")
        
        # Create workflow tasks
        workflow_tasks = []
        for file_path in file_paths:
            task = self._execute_single_pre_update_workflow(file_path)
            workflow_tasks.append(task)
        
        # Execute workflows in parallel
        results = await asyncio.gather(*workflow_tasks, return_exceptions=True)
        
        # Process results
        validation_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Pre-update validation failed for {file_paths[i]}: {result}")
                validation_results.append(self._create_error_result(
                    file_paths[i], ValidationPhase.PRE_UPDATE, str(result)
                ))
            else:
                validation_results.append(result)
        
        # Update metrics
        self._update_orchestration_metrics(validation_results)
        
        return validation_results
    
    async def execute_post_update_validation(self, file_paths: List[str], 
                                           original_contents: Dict[str, str]) -> List[ValidationWorkflowResult]:
        """Execute post-update validation workflow"""
        logger.info(f"Executing post-update validation for {len(file_paths)} files")
        
        # Create workflow tasks
        workflow_tasks = []
        for file_path in file_paths:
            original_content = original_contents.get(file_path)
            task = self._execute_single_post_update_workflow(file_path, original_content)
            workflow_tasks.append(task)
        
        # Execute workflows in parallel
        results = await asyncio.gather(*workflow_tasks, return_exceptions=True)
        
        # Process results
        validation_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Post-update validation failed for {file_paths[i]}: {result}")
                validation_results.append(self._create_error_result(
                    file_paths[i], ValidationPhase.POST_UPDATE, str(result)
                ))
            else:
                validation_results.append(result)
        
        # Check for rollback requirements
        rollback_required_files = [r for r in validation_results 
                                 if r.overall_status == ValidationStatus.ROLLBACK_REQUIRED]
        
        if rollback_required_files and self.enable_automatic_rollback:
            logger.warning(f"Triggering automatic rollback for {len(rollback_required_files)} files")
            await self._execute_rollback_workflow(rollback_required_files)
        
        # Update metrics
        self._update_orchestration_metrics(validation_results)
        
        return validation_results
    
    async def _execute_single_pre_update_workflow(self, file_path: str) -> ValidationWorkflowResult:
        """Execute pre-update validation workflow for a single file"""
        start_time = time.time()
        alerts_generated = []
        
        try:
            logger.debug(f"Starting pre-update workflow for {file_path}")
            
            # Phase 1: Framework validation
            framework_result = await self.framework_connector.validate_instruction_file(
                file_path, ValidationType.PRE_UPDATE
            )
            
            # Phase 2: Quality monitoring setup
            if self.enable_quality_monitoring:
                # Add alert capture for this workflow
                workflow_alerts = []
                
                async def capture_alerts(alert: QualityAlert):
                    if alert.file_path == file_path:
                        workflow_alerts.append(alert)
                
                self.quality_monitor.add_alert_callback(capture_alerts)
                
                # Start monitoring
                await self.quality_monitor.start_monitoring([file_path], MonitoringMode.ON_DEMAND)
                
                # Capture any immediate alerts
                await asyncio.sleep(1)  # Brief wait to capture immediate alerts
                alerts_generated.extend(workflow_alerts)
            
            # Phase 3: Validation decision
            overall_status = self._determine_pre_update_status(framework_result, alerts_generated)
            
            # Phase 4: Generate recommendations
            recommendations = self._generate_pre_update_recommendations(framework_result, alerts_generated)
            
            workflow_duration = time.time() - start_time
            
            return ValidationWorkflowResult(
                file_path=file_path,
                validation_phase=ValidationPhase.PRE_UPDATE,
                overall_status=overall_status,
                framework_result=framework_result,
                quality_impact=None,
                rollback_decision=None,
                workflow_duration=workflow_duration,
                recommendations=recommendations,
                alerts_generated=alerts_generated
            )
            
        except Exception as e:
            logger.error(f"Error in pre-update workflow for {file_path}: {e}")
            return self._create_error_result(file_path, ValidationPhase.PRE_UPDATE, str(e))
    
    async def _execute_single_post_update_workflow(self, file_path: str, 
                                                 original_content: Optional[str]) -> ValidationWorkflowResult:
        """Execute post-update validation workflow for a single file"""
        start_time = time.time()
        alerts_generated = []
        
        try:
            logger.debug(f"Starting post-update workflow for {file_path}")
            
            # Phase 1: Framework validation
            framework_result = await self.framework_connector.validate_instruction_file(
                file_path, ValidationType.POST_UPDATE, original_content
            )
            
            # Phase 2: Quality impact analysis
            quality_impact = None
            if original_content:
                with open(file_path, 'r', encoding='utf-8') as f:
                    updated_content = f.read()
                
                quality_impact = await self.quality_monitor.validate_update_quality_impact(
                    file_path, original_content, updated_content
                )
            
            # Phase 3: Quality monitoring
            if self.enable_quality_monitoring:
                # Capture alerts
                workflow_alerts = []
                
                async def capture_alerts(alert: QualityAlert):
                    if alert.file_path == file_path:
                        workflow_alerts.append(alert)
                
                self.quality_monitor.add_alert_callback(capture_alerts)
                
                # Create quality snapshot
                await self.quality_monitor._create_quality_snapshot(file_path)
                alerts_generated.extend(workflow_alerts)
            
            # Phase 4: Rollback assessment
            rollback_decision = None
            if self.enable_automatic_rollback:
                rollback_decision = await self.rollback_manager.assess_rollback_need(
                    file_path, framework_result, quality_impact, alerts_generated
                )
            
            # Phase 5: Overall validation decision
            overall_status = self._determine_post_update_status(
                framework_result, quality_impact, rollback_decision, alerts_generated
            )
            
            # Phase 6: Generate recommendations
            recommendations = self._generate_post_update_recommendations(
                framework_result, quality_impact, rollback_decision, alerts_generated
            )
            
            workflow_duration = time.time() - start_time
            
            return ValidationWorkflowResult(
                file_path=file_path,
                validation_phase=ValidationPhase.POST_UPDATE,
                overall_status=overall_status,
                framework_result=framework_result,
                quality_impact=quality_impact,
                rollback_decision=rollback_decision,
                workflow_duration=workflow_duration,
                recommendations=recommendations,
                alerts_generated=alerts_generated
            )
            
        except Exception as e:
            logger.error(f"Error in post-update workflow for {file_path}: {e}")
            return self._create_error_result(file_path, ValidationPhase.POST_UPDATE, str(e))
    
    def _determine_pre_update_status(self, framework_result: FrameworkValidationResult, 
                                   alerts: List[QualityAlert]) -> ValidationStatus:
        """Determine overall pre-update validation status"""
        
        # Check for critical issues
        if framework_result.has_critical_issues():
            return ValidationStatus.REJECTED
        
        # Check for critical alerts
        critical_alerts = [a for a in alerts if a.severity == 'CRITICAL']
        if critical_alerts:
            return ValidationStatus.REJECTED
        
        # Check framework approval
        if framework_result.approval_status != "APPROVED":
            return ValidationStatus.CONDITIONAL_APPROVAL
        
        # Check quality threshold
        if framework_result.overall_score < self.framework_connector.quality_threshold:
            return ValidationStatus.CONDITIONAL_APPROVAL
        
        # All checks passed
        return ValidationStatus.APPROVED
    
    def _determine_post_update_status(self, framework_result: FrameworkValidationResult,
                                    quality_impact: Optional[Dict[str, Any]], 
                                    rollback_decision: Optional[RollbackDecision],
                                    alerts: List[QualityAlert]) -> ValidationStatus:
        """Determine overall post-update validation status"""
        
        # Check rollback decision
        if rollback_decision and rollback_decision.should_rollback:
            return ValidationStatus.ROLLBACK_REQUIRED
        
        # Check for critical issues
        if framework_result.has_critical_issues():
            return ValidationStatus.ROLLBACK_REQUIRED
        
        # Check quality impact
        if quality_impact:
            if quality_impact['recommendation'] == 'REJECT':
                return ValidationStatus.ROLLBACK_REQUIRED
            elif quality_impact['recommendation'] == 'CAUTION':
                return ValidationStatus.CONDITIONAL_APPROVAL
        
        # Check for critical alerts
        critical_alerts = [a for a in alerts if a.severity == 'CRITICAL']
        if critical_alerts:
            return ValidationStatus.ROLLBACK_REQUIRED
        
        # Check framework approval
        if framework_result.approval_status != "APPROVED":
            return ValidationStatus.CONDITIONAL_APPROVAL
        
        # All checks passed
        return ValidationStatus.APPROVED
    
    def _generate_pre_update_recommendations(self, framework_result: FrameworkValidationResult,
                                           alerts: List[QualityAlert]) -> List[str]:
        """Generate pre-update recommendations"""
        recommendations = []
        
        # Framework recommendations
        recommendations.extend(framework_result.recommendations)
        
        # Alert-based recommendations
        for alert in alerts:
            recommendations.append(f"Address {alert.severity.lower()} alert: {alert.recommended_action}")
        
        # Quality improvement suggestions
        if framework_result.overall_score < 90:
            recommendations.append("Consider quality improvements before update to achieve excellence rating")
        
        # Specific issue recommendations
        critical_issues = [i for i in framework_result.issues if i.severity.value == 'critical']
        if critical_issues:
            recommendations.append(f"Resolve {len(critical_issues)} critical issues before proceeding")
        
        return recommendations
    
    def _generate_post_update_recommendations(self, framework_result: FrameworkValidationResult,
                                            quality_impact: Optional[Dict[str, Any]], 
                                            rollback_decision: Optional[RollbackDecision],
                                            alerts: List[QualityAlert]) -> List[str]:
        """Generate post-update recommendations"""
        recommendations = []
        
        # Rollback recommendations
        if rollback_decision and rollback_decision.should_rollback:
            recommendations.append(f"Rollback required: {rollback_decision.reason.value}")
            recommendations.extend(rollback_decision.recommendations)
        
        # Quality impact recommendations
        if quality_impact:
            if quality_impact['quality_change'] < 0:
                recommendations.append(
                    f"Quality declined by {abs(quality_impact['quality_change']):.1f} points - monitor closely"
                )
            elif quality_impact['quality_change'] > 5:
                recommendations.append(
                    f"Quality improved by {quality_impact['quality_change']:.1f} points - excellent outcome"
                )
        
        # Framework recommendations
        recommendations.extend(framework_result.recommendations)
        
        # Alert-based recommendations
        for alert in alerts:
            recommendations.append(f"Monitor {alert.severity.lower()} condition: {alert.recommended_action}")
        
        return recommendations
    
    async def _execute_rollback_workflow(self, rollback_results: List[ValidationWorkflowResult]):
        """Execute rollback workflow for files requiring rollback"""
        logger.info(f"Executing rollback workflow for {len(rollback_results)} files")
        
        rollback_tasks = []
        for result in rollback_results:
            if result.rollback_decision:
                task = self.rollback_manager.execute_rollback(result.rollback_decision)
                rollback_tasks.append(task)
        
        if rollback_tasks:
            rollback_outcomes = await asyncio.gather(*rollback_tasks, return_exceptions=True)
            
            successful_rollbacks = 0
            for i, outcome in enumerate(rollback_outcomes):
                if not isinstance(outcome, Exception) and outcome.get('success', False):
                    successful_rollbacks += 1
                    rollback_results[i].overall_status = ValidationStatus.ROLLBACK_REQUIRED
                else:
                    logger.error(f"Rollback failed: {outcome}")
            
            logger.info(f"Rollback completed: {successful_rollbacks}/{len(rollback_tasks)} successful")
    
    def _create_error_result(self, file_path: str, phase: ValidationPhase, error_message: str) -> ValidationWorkflowResult:
        """Create error result for failed workflows"""
        return ValidationWorkflowResult(
            file_path=file_path,
            validation_phase=phase,
            overall_status=ValidationStatus.VALIDATION_ERROR,
            framework_result=None,
            quality_impact=None,
            rollback_decision=None,
            workflow_duration=0.0,
            recommendations=[f"Resolve validation error: {error_message}"],
            alerts_generated=[]
        )
    
    def _update_orchestration_metrics(self, results: List[ValidationWorkflowResult]):
        """Update orchestration performance metrics"""
        self.orchestration_metrics['total_workflows'] += len(results)
        
        for result in results:
            # Count approvals and rejections
            if result.overall_status == ValidationStatus.APPROVED:
                self.orchestration_metrics['approved_workflows'] += 1
            elif result.overall_status in [ValidationStatus.REJECTED, ValidationStatus.ROLLBACK_REQUIRED]:
                self.orchestration_metrics['rejected_workflows'] += 1
            
            # Count rollbacks
            if result.overall_status == ValidationStatus.ROLLBACK_REQUIRED:
                self.orchestration_metrics['rollbacks_triggered'] += 1
            
            # Count quality changes
            if result.quality_impact:
                if result.quality_impact['quality_change'] > 0:
                    self.orchestration_metrics['quality_improvements'] += 1
                elif abs(result.quality_impact['quality_change']) <= 2.0:
                    self.orchestration_metrics['quality_preservations'] += 1
        
        # Update average workflow time
        total_workflows = self.orchestration_metrics['total_workflows']
        current_avg = self.orchestration_metrics['average_workflow_time']
        
        workflow_times = [r.workflow_duration for r in results if r.workflow_duration > 0]
        if workflow_times:
            new_avg_time = sum(workflow_times) / len(workflow_times)
            self.orchestration_metrics['average_workflow_time'] = (
                (current_avg * (total_workflows - len(results)) + new_avg_time * len(results)) / total_workflows
            )
    
    async def get_orchestration_status(self) -> Dict[str, Any]:
        """Get current orchestration status and metrics"""
        return {
            'active_workflows': len(self.active_workflows),
            'workflow_history_count': len(self.workflow_history),
            'configuration': {
                'enable_quality_monitoring': self.enable_quality_monitoring,
                'enable_automatic_rollback': self.enable_automatic_rollback,
                'quality_preservation_threshold': self.quality_preservation_threshold,
                'validation_timeout': self.validation_timeout
            },
            'metrics': self.orchestration_metrics,
            'component_status': {
                'framework_connector': await self.framework_connector.get_validation_metrics(),
                'quality_monitor': (await self.quality_monitor.get_quality_dashboard())['metrics'],
                'rollback_manager': await self.rollback_manager.get_rollback_metrics()
            },
            'timestamp': datetime.utcnow().isoformat()
        }
    
    async def validate_batch_update_readiness(self, file_paths: List[str]) -> Dict[str, Any]:
        """Validate readiness for batch update operations"""
        logger.info(f"Validating batch update readiness for {len(file_paths)} files")
        
        # Execute pre-update validation
        pre_update_results = await self.execute_pre_update_validation(file_paths)
        
        # Analyze batch readiness
        approved_files = [r for r in pre_update_results if r.overall_status == ValidationStatus.APPROVED]
        conditional_files = [r for r in pre_update_results if r.overall_status == ValidationStatus.CONDITIONAL_APPROVAL]
        rejected_files = [r for r in pre_update_results if r.overall_status == ValidationStatus.REJECTED]
        
        # Calculate readiness score
        total_files = len(file_paths)
        readiness_score = (len(approved_files) + 0.5 * len(conditional_files)) / total_files * 100
        
        # Determine batch recommendation
        if readiness_score >= 80:
            batch_recommendation = "PROCEED"
        elif readiness_score >= 60:
            batch_recommendation = "PROCEED_WITH_CAUTION"
        else:
            batch_recommendation = "DELAY"
        
        return {
            'readiness_score': readiness_score,
            'batch_recommendation': batch_recommendation, 
            'file_analysis': {
                'total_files': total_files,
                'approved_files': len(approved_files),
                'conditional_files': len(conditional_files),
                'rejected_files': len(rejected_files)
            },
            'approved_file_paths': [r.file_path for r in approved_files],
            'conditional_file_paths': [r.file_path for r in conditional_files],
            'rejected_file_paths': [r.file_path for r in rejected_files],
            'recommendations': self._generate_batch_recommendations(pre_update_results),
            'validation_results': [r.to_dict() for r in pre_update_results]
        }
    
    def _generate_batch_recommendations(self, results: List[ValidationWorkflowResult]) -> List[str]:
        """Generate batch update recommendations"""
        recommendations = []
        
        rejected_count = len([r for r in results if r.overall_status == ValidationStatus.REJECTED])
        conditional_count = len([r for r in results if r.overall_status == ValidationStatus.CONDITIONAL_APPROVAL])
        
        if rejected_count > 0:
            recommendations.append(f"Address quality issues in {rejected_count} rejected files before batch update")
        
        if conditional_count > 0:
            recommendations.append(f"Review {conditional_count} files with conditional approval for quality improvements")
        
        # Aggregate common issues
        all_issues = []
        for result in results:
            if result.framework_result:
                all_issues.extend(result.framework_result.issues)
        
        if all_issues:
            issue_categories = {}
            for issue in all_issues:
                category = issue.category
                if category not in issue_categories:
                    issue_categories[category] = 0
                issue_categories[category] += 1
            
            # Recommend addressing most common issues
            most_common = max(issue_categories.items(), key=lambda x: x[1])
            if most_common[1] > 1:
                recommendations.append(f"Common issue detected: {most_common[0]} (affects {most_common[1]} files)")
        
        return recommendations


async def main():
    """Main function for testing"""
    try:
        # Initialize all components
        from .framework_connector import AIInstructionFrameworkConnector
        from .quality_monitor import QualityMonitor
        from .rollback_manager import RollbackManager
        
        # Framework connector
        framework_config = {'quality_threshold': 75.0}
        framework_connector = AIInstructionFrameworkConnector(framework_config)
        
        # Quality monitor
        monitor_config = {'critical_threshold': 50.0, 'warning_threshold': 65.0}
        quality_monitor = QualityMonitor(framework_connector, monitor_config)
        
        # Rollback manager
        rollback_config = {'backup_directory': '/tmp/test_backups'}
        rollback_manager = RollbackManager(rollback_config)
        
        # Validation orchestrator
        orchestrator_config = {
            'enable_quality_monitoring': True,
            'enable_automatic_rollback': True,
            'quality_preservation_threshold': 5.0
        }
        
        orchestrator = ValidationOrchestrator(
            framework_connector, quality_monitor, rollback_manager, orchestrator_config
        )
        
        # Test files
        test_files = [
            '/Users/georgiospilitsoglou/Developer/projects/mypromptflow/.claude/commands/ai-help.md'
        ]
        
        existing_files = [f for f in test_files if Path(f).exists()]
        
        if existing_files:
            # Test batch readiness validation
            readiness = await orchestrator.validate_batch_update_readiness(existing_files)
            print("Batch Update Readiness:")
            print(json.dumps(readiness, indent=2, default=str))
            
            # Get orchestration status
            status = await orchestrator.get_orchestration_status()
            print("\nOrchestration Status:")
            print(json.dumps(status, indent=2, default=str))
        
        print("\nValidation Orchestrator test completed successfully!")
        
    except Exception as e:
        print(f"Error testing validation orchestrator: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(asyncio.run(main()))