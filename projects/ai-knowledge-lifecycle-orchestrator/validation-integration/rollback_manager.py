#!/usr/bin/env python3
"""
Rollback Manager
AI Knowledge Lifecycle Orchestrator - Quality-based rollback system

This module provides intelligent rollback capabilities based on quality thresholds,
framework compliance, and validation failures to ensure instruction quality is preserved.
"""

import asyncio
import logging
import shutil
import hashlib
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RollbackReason(Enum):
    """Reasons for triggering rollback"""
    QUALITY_DECLINE = "quality_decline"
    CRITICAL_ISSUES = "critical_issues"
    FRAMEWORK_FAILURE = "framework_failure"
    VALIDATION_TIMEOUT = "validation_timeout"
    USER_REQUESTED = "user_requested"
    AUTOMATIC_TRIGGER = "automatic_trigger"
    BATCH_FAILURE = "batch_failure"


class RollbackStatus(Enum):
    """Rollback execution status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class RollbackDecision:
    """Decision about whether to perform rollback"""
    file_path: str
    should_rollback: bool
    reason: RollbackReason
    confidence: float  # 0.0 to 1.0
    quality_impact: float  # Negative = quality decline
    critical_issues_count: int
    recommendations: List[str]
    decision_time: datetime
    backup_available: bool
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['reason'] = self.reason.value
        data['decision_time'] = self.decision_time.isoformat()
        return data


@dataclass
class RollbackExecution:
    """Information about rollback execution"""
    execution_id: str
    file_path: str
    status: RollbackStatus
    reason: RollbackReason
    backup_path: str
    original_hash: str
    execution_start: datetime
    execution_end: Optional[datetime]
    success: bool
    error_details: Optional[str]
    validation_after_rollback: Optional[Dict[str, Any]]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['status'] = self.status.value
        data['reason'] = self.reason.value
        data['execution_start'] = self.execution_start.isoformat()
        if self.execution_end:
            data['execution_end'] = self.execution_end.isoformat()
        return data


class RollbackManager:
    """
    Intelligent rollback management system
    Provides quality-based rollback decisions and reliable execution
    """
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the rollback manager"""
        self.config = config
        
        # Rollback thresholds
        self.quality_decline_threshold = config.get('quality_decline_threshold', 10.0)
        self.critical_issues_threshold = config.get('critical_issues_threshold', 1)
        self.confidence_threshold = config.get('confidence_threshold', 0.7)
        
        # Detection timeouts
        self.rollback_detection_timeout = config.get('rollback_detection_timeout', 10)  # seconds
        self.rollback_execution_timeout = config.get('rollback_execution_timeout', 30)  # seconds
        
        # Backup management
        self.backup_directory = Path(config.get('backup_directory', 
            '/Users/georgiospilitsoglou/Developer/projects/mypromptflow/.backups'))
        self.backup_directory.mkdir(parents=True, exist_ok=True)
        self.backup_retention_days = config.get('backup_retention_days', 30)
        
        # Rollback state
        self.rollback_history: List[RollbackExecution] = []
        self.pending_rollbacks: Dict[str, RollbackDecision] = {}
        
        # Performance metrics
        self.rollback_metrics = {
            'total_decisions': 0,
            'rollbacks_recommended': 0,
            'rollbacks_executed': 0,
            'successful_rollbacks': 0,
            'failed_rollbacks': 0,
            'average_decision_time': 0.0,
            'average_execution_time': 0.0,
            'quality_recoveries': 0
        }
        
        logger.info("Rollback Manager initialized successfully")
    
    async def assess_rollback_need(self, file_path: str, framework_result, 
                                 quality_impact: Optional[Dict[str, Any]], 
                                 alerts: List) -> RollbackDecision:
        """Assess whether rollback is needed based on validation results"""
        start_time = datetime.utcnow()
        
        try:
            logger.debug(f"Assessing rollback need for {file_path}")
            
            # Initialize decision parameters
            should_rollback = False
            reason = None
            confidence = 0.0
            quality_impact_value = 0.0
            critical_issues_count = 0
            recommendations = []
            
            # Check framework validation results
            if framework_result:
                critical_issues_count = len([i for i in framework_result.issues if i.severity.value == 'critical'])
                
                # Critical issues trigger rollback
                if critical_issues_count >= self.critical_issues_threshold:
                    should_rollback = True
                    reason = RollbackReason.CRITICAL_ISSUES
                    confidence = 0.9
                    recommendations.append(f"Rollback due to {critical_issues_count} critical issues")
                
                # Framework failure
                if framework_result.overall_score == 0.0 or framework_result.approval_status == "FAILED":
                    should_rollback = True
                    reason = RollbackReason.FRAMEWORK_FAILURE
                    confidence = 0.95
                    recommendations.append("Rollback due to framework validation failure")
            
            # Check quality impact
            if quality_impact and not should_rollback:
                quality_impact_value = quality_impact.get('quality_change', 0.0)
                
                # Significant quality decline
                if quality_impact_value < -self.quality_decline_threshold:
                    should_rollback = True
                    reason = RollbackReason.QUALITY_DECLINE
                    confidence = min(0.9, abs(quality_impact_value) / 20.0)  # Higher decline = higher confidence
                    recommendations.append(f"Rollback due to quality decline: {quality_impact_value:.1f} points")
                
                # Check quality impact analysis
                impact_analysis = quality_impact.get('impact_analysis', {})
                if impact_analysis.get('significant_decline', False):
                    should_rollback = True
                    reason = RollbackReason.QUALITY_DECLINE
                    confidence = 0.85
                    recommendations.append("Rollback due to significant quality decline")
                
                if impact_analysis.get('new_critical_issues', False):
                    should_rollback = True
                    reason = RollbackReason.CRITICAL_ISSUES
                    confidence = 0.9
                    recommendations.append("Rollback due to new critical issues introduced")
            
            # Check alerts
            if alerts and not should_rollback:
                critical_alerts = [a for a in alerts if a.severity == 'CRITICAL']
                if critical_alerts:
                    should_rollback = True
                    reason = RollbackReason.AUTOMATIC_TRIGGER
                    confidence = 0.8
                    recommendations.append(f"Rollback due to {len(critical_alerts)} critical alerts")
            
            # Check backup availability
            backup_available = await self._check_backup_availability(file_path)
            
            # Override rollback decision if no backup available
            if should_rollback and not backup_available:
                logger.warning(f"Rollback recommended but no backup available for {file_path}")
                should_rollback = False
                confidence = 0.0
                reason = None
                recommendations = ["Cannot rollback: No backup available"]
            
            # Create rollback decision
            decision = RollbackDecision(
                file_path=file_path,
                should_rollback=should_rollback,
                reason=reason or RollbackReason.QUALITY_DECLINE,
                confidence=confidence,
                quality_impact=quality_impact_value,
                critical_issues_count=critical_issues_count,
                recommendations=recommendations,
                decision_time=start_time,
                backup_available=backup_available
            )
            
            # Update metrics
            self.rollback_metrics['total_decisions'] += 1
            if should_rollback:
                self.rollback_metrics['rollbacks_recommended'] += 1
                # Store pending rollback
                self.pending_rollbacks[file_path] = decision
            
            # Update average decision time
            decision_time = (datetime.utcnow() - start_time).total_seconds()
            total_decisions = self.rollback_metrics['total_decisions']
            current_avg = self.rollback_metrics['average_decision_time']
            self.rollback_metrics['average_decision_time'] = (
                (current_avg * (total_decisions - 1) + decision_time) / total_decisions
            )
            
            logger.debug(f"Rollback assessment completed: {should_rollback} (confidence: {confidence:.2f})")
            return decision
            
        except Exception as e:
            logger.error(f"Error assessing rollback need for {file_path}: {e}")
            # Return safe decision
            return RollbackDecision(
                file_path=file_path,
                should_rollback=False,
                reason=RollbackReason.FRAMEWORK_FAILURE,
                confidence=0.0,
                quality_impact=0.0,
                critical_issues_count=0,
                recommendations=[f"Assessment error: {str(e)}"],
                decision_time=start_time,
                backup_available=False
            )
    
    async def execute_rollback(self, decision: RollbackDecision) -> Dict[str, Any]:
        """Execute rollback based on decision"""
        if not decision.should_rollback:
            return {'success': False, 'error': 'Rollback not recommended'}
        
        execution_id = f"{Path(decision.file_path).name}_{int(datetime.utcnow().timestamp())}"
        start_time = datetime.utcnow()
        
        logger.info(f"Executing rollback for {decision.file_path} (reason: {decision.reason.value})")
        
        try:
            # Find backup file
            backup_path = await self._find_latest_backup(decision.file_path)
            if not backup_path:
                error_msg = f"No backup found for {decision.file_path}"
                logger.error(error_msg)
                return {'success': False, 'error': error_msg}
            
            # Verify backup integrity
            if not await self._verify_backup_integrity(backup_path):
                error_msg = f"Backup integrity check failed for {backup_path}"
                logger.error(error_msg)
                return {'success': False, 'error': error_msg}
            
            # Calculate original file hash
            original_hash = ""
            if Path(decision.file_path).exists():
                with open(decision.file_path, 'rb') as f:
                    original_hash = hashlib.sha256(f.read()).hexdigest()
            
            # Create rollback execution record
            execution = RollbackExecution(
                execution_id=execution_id,
                file_path=decision.file_path,
                status=RollbackStatus.IN_PROGRESS,
                reason=decision.reason,
                backup_path=str(backup_path),
                original_hash=original_hash,
                execution_start=start_time,
                execution_end=None,
                success=False,
                error_details=None,
                validation_after_rollback=None
            )
            
            # Execute the rollback
            try:
                # Copy backup to original location
                shutil.copy2(backup_path, decision.file_path)
                
                # Verify rollback
                rollback_success = await self._verify_rollback_success(decision.file_path, backup_path)
                
                if rollback_success:
                    execution.status = RollbackStatus.COMPLETED
                    execution.success = True
                    execution.execution_end = datetime.utcnow()
                    
                    # Update metrics
                    self.rollback_metrics['rollbacks_executed'] += 1
                    self.rollback_metrics['successful_rollbacks'] += 1
                    
                    logger.info(f"Rollback completed successfully for {decision.file_path}")
                    
                    # Optional: Validate quality after rollback
                    validation_result = await self._validate_after_rollback(decision.file_path)
                    execution.validation_after_rollback = validation_result
                    
                    if validation_result and validation_result.get('quality_improved', False):
                        self.rollback_metrics['quality_recoveries'] += 1
                    
                else:
                    execution.status = RollbackStatus.FAILED
                    execution.error_details = "Rollback verification failed"
                    execution.execution_end = datetime.utcnow()
                    self.rollback_metrics['failed_rollbacks'] += 1
                
            except Exception as e:
                execution.status = RollbackStatus.FAILED
                execution.error_details = str(e)
                execution.execution_end = datetime.utcnow()
                self.rollback_metrics['failed_rollbacks'] += 1
                logger.error(f"Rollback execution failed: {e}")
            
            # Store rollback execution
            self.rollback_history.append(execution)
            
            # Remove from pending rollbacks
            if decision.file_path in self.pending_rollbacks:
                del self.pending_rollbacks[decision.file_path]
            
            # Update average execution time
            if execution.execution_end:
                execution_time = (execution.execution_end - execution.execution_start).total_seconds()
                total_executions = self.rollback_metrics['rollbacks_executed']
                current_avg = self.rollback_metrics['average_execution_time']
                
                if total_executions > 0:
                    self.rollback_metrics['average_execution_time'] = (
                        (current_avg * (total_executions - 1) + execution_time) / total_executions
                    )
            
            return {
                'success': execution.success,
                'execution_id': execution_id,
                'execution_time': (execution.execution_end - execution.execution_start).total_seconds() if execution.execution_end else 0,
                'backup_used': str(backup_path),
                'validation_after_rollback': execution.validation_after_rollback,
                'error': execution.error_details
            }
            
        except Exception as e:
            logger.error(f"Error executing rollback for {decision.file_path}: {e}")
            self.rollback_metrics['failed_rollbacks'] += 1
            return {'success': False, 'error': str(e)}
    
    async def _check_backup_availability(self, file_path: str) -> bool:
        """Check if backup is available for the file"""
        try:
            backup_path = await self._find_latest_backup(file_path)
            return backup_path is not None and backup_path.exists()
        except Exception as e:
            logger.error(f"Error checking backup availability for {file_path}: {e}")
            return False
    
    async def _find_latest_backup(self, file_path: str) -> Optional[Path]:
        """Find the latest backup for a file"""
        try:
            file_name = Path(file_path).name
            backup_pattern = f"{file_name}_*.backup"
            
            # Find all backups for this file
            backup_files = list(self.backup_directory.glob(backup_pattern))
            
            if not backup_files:
                return None
            
            # Sort by modification time (most recent first)
            backup_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            return backup_files[0]
            
        except Exception as e:
            logger.error(f"Error finding backup for {file_path}: {e}")
            return None
    
    async def _verify_backup_integrity(self, backup_path: Path) -> bool:
        """Verify backup file integrity"""
        try:
            # Check if file exists and is readable
            if not backup_path.exists():
                return False
            
            # Check file size (must be > 0)
            if backup_path.stat().st_size == 0:
                return False
            
            # Try to read the file
            with open(backup_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if not content.strip():
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error verifying backup integrity for {backup_path}: {e}")
            return False
    
    async def _verify_rollback_success(self, file_path: str, backup_path: Path) -> bool:
        """Verify that rollback was successful"""
        try:
            # Compare file contents
            with open(file_path, 'rb') as f1, open(backup_path, 'rb') as f2:
                file_hash = hashlib.sha256(f1.read()).hexdigest()
                backup_hash = hashlib.sha256(f2.read()).hexdigest()
                
                return file_hash == backup_hash
                
        except Exception as e:
            logger.error(f"Error verifying rollback success: {e}")
            return False
    
    async def _validate_after_rollback(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Validate file quality after rollback"""
        try:
            # This would integrate with the framework connector for validation
            # For now, simulate basic validation
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic quality checks
            has_content = len(content.strip()) > 0
            has_structure = any(marker in content for marker in ['#', '-', '*', '1.'])
            has_reasonable_length = 50 < len(content) < 10000
            
            quality_score = 0
            if has_content:
                quality_score += 30
            if has_structure:
                quality_score += 40
            if has_reasonable_length:
                quality_score += 30
            
            return {
                'quality_score': quality_score,
                'quality_improved': quality_score > 70,
                'has_content': has_content,
                'has_structure': has_structure,
                'content_length': len(content)
            }
            
        except Exception as e:
            logger.error(f"Error validating after rollback: {e}")
            return None
    
    async def batch_rollback(self, decisions: List[RollbackDecision]) -> List[Dict[str, Any]]:
        """Execute rollback for multiple files"""
        logger.info(f"Executing batch rollback for {len(decisions)} files")
        
        # Filter decisions that require rollback
        rollback_decisions = [d for d in decisions if d.should_rollback]
        
        if not rollback_decisions:
            return [{'success': True, 'message': 'No rollbacks required'}]
        
        # Execute rollbacks in parallel
        rollback_tasks = []
        for decision in rollback_decisions:
            task = self.execute_rollback(decision)
            rollback_tasks.append(task)
        
        results = await asyncio.gather(*rollback_tasks, return_exceptions=True)
        
        # Process results
        rollback_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Batch rollback failed for {rollback_decisions[i].file_path}: {result}")
                rollback_results.append({
                    'success': False,
                    'file_path': rollback_decisions[i].file_path,
                    'error': str(result)
                })
            else:
                result['file_path'] = rollback_decisions[i].file_path
                rollback_results.append(result)
        
        successful_rollbacks = len([r for r in rollback_results if r.get('success', False)])
        logger.info(f"Batch rollback completed: {successful_rollbacks}/{len(rollback_results)} successful")
        
        return rollback_results
    
    async def get_rollback_metrics(self) -> Dict[str, Any]:
        """Get rollback performance metrics"""
        return {
            'total_decisions': self.rollback_metrics['total_decisions'],
            'rollbacks_recommended': self.rollback_metrics['rollbacks_recommended'],
            'rollbacks_executed': self.rollback_metrics['rollbacks_executed'],
            'successful_rollbacks': self.rollback_metrics['successful_rollbacks'],
            'failed_rollbacks': self.rollback_metrics['failed_rollbacks'],
            'quality_recoveries': self.rollback_metrics['quality_recoveries'],
            'success_rate': self.rollback_metrics['successful_rollbacks'] / max(self.rollback_metrics['rollbacks_executed'], 1),
            'recommendation_rate': self.rollback_metrics['rollbacks_recommended'] / max(self.rollback_metrics['total_decisions'], 1),
            'average_decision_time': self.rollback_metrics['average_decision_time'],
            'average_execution_time': self.rollback_metrics['average_execution_time'],
            'pending_rollbacks': len(self.pending_rollbacks),
            'rollback_history_count': len(self.rollback_history),
            'backup_directory': str(self.backup_directory),
            'backup_count': len(list(self.backup_directory.glob('*.backup'))),
            'configuration': {
                'quality_decline_threshold': self.quality_decline_threshold,
                'critical_issues_threshold': self.critical_issues_threshold,
                'confidence_threshold': self.confidence_threshold
            },
            'timestamp': datetime.utcnow().isoformat()
        }
    
    async def get_rollback_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent rollback history"""
        recent_history = sorted(
            self.rollback_history, 
            key=lambda x: x.execution_start, 
            reverse=True
        )[:limit]
        
        return [execution.to_dict() for execution in recent_history]
    
    async def cleanup_old_backups(self, days_to_keep: Optional[int] = None):
        """Clean up old backup files"""
        try:
            days_to_keep = days_to_keep or self.backup_retention_days
            cutoff_time = datetime.utcnow() - timedelta(days=days_to_keep)
            cutoff_timestamp = cutoff_time.timestamp()
            
            cleaned_count = 0
            for backup_file in self.backup_directory.glob('*.backup'):
                if backup_file.stat().st_mtime < cutoff_timestamp:
                    backup_file.unlink()
                    cleaned_count += 1
            
            logger.info(f"Cleaned up {cleaned_count} old backup files (older than {days_to_keep} days)")
            
        except Exception as e:
            logger.error(f"Error cleaning up old backups: {e}")


async def main():
    """Main function for testing"""
    try:
        # Initialize rollback manager
        config = {
            'quality_decline_threshold': 10.0,
            'critical_issues_threshold': 1,
            'backup_directory': '/tmp/test_rollback_backups'
        }
        
        rollback_manager = RollbackManager(config)
        
        # Create a test backup directory and file
        os.makedirs('/tmp/test_rollback_backups', exist_ok=True)
        
        # Test file
        test_file = '/tmp/test_instruction.md'
        test_content = "# Test Instruction\n\nThis is a test instruction file."
        
        with open(test_file, 'w') as f:
            f.write(test_content)
        
        # Create a backup
        backup_file = Path('/tmp/test_rollback_backups/test_instruction.md_20250725_120000.backup')
        shutil.copy2(test_file, backup_file)
        
        # Simulate framework result and quality impact
        class MockValidationResult:
            def __init__(self):
                self.overall_score = 40.0  # Low score to trigger rollback
                self.approval_status = "NEEDS_IMPROVEMENT"
                self.issues = [MockIssue()]
        
        class MockIssue:
            def __init__(self):
                self.severity = MockSeverity()
        
        class MockSeverity:
            def __init__(self):
                self.value = 'critical'
        
        framework_result = MockValidationResult()
        quality_impact = {
            'quality_change': -15.0,  # Significant decline
            'impact_analysis': {
                'significant_decline': True,
                'new_critical_issues': True
            }
        }
        
        # Test rollback assessment
        decision = await rollback_manager.assess_rollback_need(
            test_file, framework_result, quality_impact, []
        )
        
        print("Rollback Decision:")
        print(json.dumps(decision.to_dict(), indent=2, default=str))
        
        if decision.should_rollback:
            # Test rollback execution
            result = await rollback_manager.execute_rollback(decision)
            print("\nRollback Execution:")
            print(json.dumps(result, indent=2, default=str))
        
        # Get metrics
        metrics = await rollback_manager.get_rollback_metrics()
        print("\nRollback Metrics:")
        print(json.dumps(metrics, indent=2, default=str))
        
        # Cleanup
        if os.path.exists(test_file):
            os.unlink(test_file)
        if backup_file.exists():
            backup_file.unlink()
        
        print("\nRollback Manager test completed successfully!")
        
    except Exception as e:
        print(f"Error testing rollback manager: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(asyncio.run(main()))