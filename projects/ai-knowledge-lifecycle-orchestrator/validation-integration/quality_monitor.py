#!/usr/bin/env python3
"""
Quality Monitor
AI Knowledge Lifecycle Orchestrator - Real-time quality monitoring during instruction updates

This module provides real-time quality scoring and monitoring capabilities to ensure
instruction quality is preserved throughout the update process.
"""

import asyncio
import logging
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
import json

try:
    from .framework_connector import AIInstructionFrameworkConnector, FrameworkValidationResult, ValidationType
except ImportError:
    from framework_connector import AIInstructionFrameworkConnector, FrameworkValidationResult, ValidationType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class QualityTrend(Enum):
    """Quality trend directions"""
    IMPROVING = "improving"
    STABLE = "stable"
    DECLINING = "declining"
    CRITICAL_DECLINE = "critical_decline"


class MonitoringMode(Enum):
    """Quality monitoring modes"""
    CONTINUOUS = "continuous"
    PERIODIC = "periodic"
    ON_DEMAND = "on_demand"
    UPDATE_TRIGGERED = "update_triggered"


@dataclass
class QualitySnapshot:
    """Point-in-time quality measurement"""
    timestamp: datetime
    file_path: str
    overall_score: float
    component_scores: Dict[str, float]
    quality_classification: str
    issues_count: int
    critical_issues_count: int
    validation_time: float
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data


@dataclass
class QualityAlert:
    """Quality monitoring alert"""
    alert_id: str
    timestamp: datetime
    severity: str
    file_path: str
    message: str
    current_score: float
    threshold_violated: str
    recommended_action: str
    auto_action_taken: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data


class QualityMonitor:
    """
    Real-time quality monitoring system for AI instruction files
    Provides continuous quality assessment and alerts during updates
    """
    
    def __init__(self, framework_connector: AIInstructionFrameworkConnector, config: Dict[str, Any]):
        """Initialize the quality monitor"""
        self.framework_connector = framework_connector
        self.config = config
        
        # Quality thresholds
        self.critical_threshold = config.get('critical_threshold', 50.0)
        self.warning_threshold = config.get('warning_threshold', 65.0)
        self.target_threshold = config.get('target_threshold', 75.0)
        self.excellence_threshold = config.get('excellence_threshold', 90.0)
        
        # Monitoring configuration
        self.monitoring_interval = config.get('monitoring_interval', 30)  # seconds
        self.trend_analysis_window = config.get('trend_analysis_window', 5)  # number of snapshots
        self.max_quality_decline = config.get('max_quality_decline', 10.0)  # percentage points
        self.alert_cooldown = config.get('alert_cooldown', 300)  # seconds
        
        # Storage
        self.quality_snapshots: Dict[str, List[QualitySnapshot]] = {}
        self.active_alerts: List[QualityAlert] = []
        self.quality_history: Dict[str, List[Dict[str, Any]]] = {}
        
        # Monitoring state
        self.monitoring_tasks: Dict[str, asyncio.Task] = {}
        self.is_monitoring = False
        self.alert_callbacks: List[Callable] = []
        
        # Metrics
        self.monitoring_metrics = {
            'files_monitored': 0,
            'total_snapshots': 0,
            'alerts_generated': 0,
            'critical_alerts': 0,
            'quality_improvements': 0,
            'quality_declines': 0,
            'average_monitoring_time': 0.0
        }
        
        logger.info("Quality Monitor initialized successfully")
    
    async def start_monitoring(self, file_paths: List[str], mode: MonitoringMode = MonitoringMode.CONTINUOUS):
        """Start monitoring specified files"""
        logger.info(f"Starting {mode.value} monitoring for {len(file_paths)} files")
        
        self.is_monitoring = True
        
        for file_path in file_paths:
            if file_path not in self.monitoring_tasks:
                # Create initial quality snapshot
                await self._create_quality_snapshot(file_path)
                
                # Start monitoring task based on mode
                if mode == MonitoringMode.CONTINUOUS:
                    task = asyncio.create_task(self._continuous_monitoring(file_path))
                    self.monitoring_tasks[file_path] = task
                elif mode == MonitoringMode.PERIODIC:
                    task = asyncio.create_task(self._periodic_monitoring(file_path))
                    self.monitoring_tasks[file_path] = task
                
                self.monitoring_metrics['files_monitored'] += 1
        
        logger.info(f"Monitoring started for {len(self.monitoring_tasks)} files")
    
    async def stop_monitoring(self, file_paths: Optional[List[str]] = None):
        """Stop monitoring specified files or all files"""
        if file_paths is None:
            file_paths = list(self.monitoring_tasks.keys())
        
        logger.info(f"Stopping monitoring for {len(file_paths)} files")
        
        for file_path in file_paths:
            if file_path in self.monitoring_tasks:
                task = self.monitoring_tasks[file_path]
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
                del self.monitoring_tasks[file_path]
        
        if not self.monitoring_tasks:
            self.is_monitoring = False
    
    async def _continuous_monitoring(self, file_path: str):
        """Continuous monitoring loop for a file"""
        logger.debug(f"Starting continuous monitoring for {file_path}")
        
        try:
            while self.is_monitoring:
                await asyncio.sleep(self.monitoring_interval)
                
                # Create quality snapshot
                await self._create_quality_snapshot(file_path)
                
                # Analyze trends and generate alerts
                await self._analyze_quality_trends(file_path)
                
        except asyncio.CancelledError:
            logger.debug(f"Monitoring cancelled for {file_path}")
        except Exception as e:
            logger.error(f"Error in continuous monitoring for {file_path}: {e}")
    
    async def _periodic_monitoring(self, file_path: str):
        """Periodic monitoring with longer intervals"""
        logger.debug(f"Starting periodic monitoring for {file_path}")
        
        try:
            while self.is_monitoring:
                await asyncio.sleep(self.monitoring_interval * 3)  # 3x longer intervals
                
                # Create quality snapshot
                await self._create_quality_snapshot(file_path)
                
                # Analyze trends
                await self._analyze_quality_trends(file_path)
                
        except asyncio.CancelledError:
            logger.debug(f"Periodic monitoring cancelled for {file_path}")
        except Exception as e:
            logger.error(f"Error in periodic monitoring for {file_path}: {e}")
    
    async def _create_quality_snapshot(self, file_path: str) -> QualitySnapshot:
        """Create a quality snapshot for a file"""
        start_time = time.time()
        
        try:
            # Validate file using framework connector
            validation_result = await self.framework_connector.validate_instruction_file(
                file_path, ValidationType.QUALITY_MONITORING
            )
            
            # Create snapshot
            snapshot = QualitySnapshot(
                timestamp=datetime.utcnow(),
                file_path=file_path,
                overall_score=validation_result.overall_score,
                component_scores=validation_result.component_scores,
                quality_classification=validation_result.quality_classification,
                issues_count=len(validation_result.issues),
                critical_issues_count=len([i for i in validation_result.issues if i.severity.value == 'critical']),
                validation_time=validation_result.validation_time
            )
            
            # Store snapshot
            if file_path not in self.quality_snapshots:
                self.quality_snapshots[file_path] = []
            
            self.quality_snapshots[file_path].append(snapshot)
            
            # Keep only recent snapshots (sliding window)
            max_snapshots = self.trend_analysis_window * 3
            if len(self.quality_snapshots[file_path]) > max_snapshots:
                self.quality_snapshots[file_path] = self.quality_snapshots[file_path][-max_snapshots:]
            
            # Update metrics
            self.monitoring_metrics['total_snapshots'] += 1
            
            # Update average monitoring time
            monitoring_time = time.time() - start_time
            total_snapshots = self.monitoring_metrics['total_snapshots']
            current_avg = self.monitoring_metrics['average_monitoring_time']
            self.monitoring_metrics['average_monitoring_time'] = (
                (current_avg * (total_snapshots - 1) + monitoring_time) / total_snapshots
            )
            
            logger.debug(f"Quality snapshot created for {file_path}: {snapshot.overall_score:.1f}/100")
            return snapshot
            
        except Exception as e:
            logger.error(f"Error creating quality snapshot for {file_path}: {e}")
            raise
    
    async def _analyze_quality_trends(self, file_path: str):
        """Analyze quality trends and generate alerts if necessary"""
        snapshots = self.quality_snapshots.get(file_path, [])
        
        if len(snapshots) < 2:
            return  # Need at least 2 snapshots for trend analysis
        
        # Get recent snapshots for trend analysis
        recent_snapshots = snapshots[-self.trend_analysis_window:]
        current_snapshot = recent_snapshots[-1]
        
        # Calculate trend
        trend = self._calculate_quality_trend(recent_snapshots)
        
        # Check for threshold violations
        await self._check_quality_thresholds(current_snapshot, trend)
        
        # Update quality history
        if file_path not in self.quality_history:
            self.quality_history[file_path] = []
        
        self.quality_history[file_path].append({
            'timestamp': current_snapshot.timestamp.isoformat(),
            'score': current_snapshot.overall_score,
            'trend': trend.value,
            'issues_count': current_snapshot.issues_count
        })
        
        # Keep history manageable
        if len(self.quality_history[file_path]) > 100:
            self.quality_history[file_path] = self.quality_history[file_path][-100:]
    
    def _calculate_quality_trend(self, snapshots: List[QualitySnapshot]) -> QualityTrend:
        """Calculate quality trend from snapshots"""
        if len(snapshots) < 2:
            return QualityTrend.STABLE
        
        scores = [s.overall_score for s in snapshots]
        
        # Calculate trend using linear regression slope approximation
        n = len(scores)
        sum_x = sum(range(n))
        sum_y = sum(scores)
        sum_xy = sum(i * score for i, score in enumerate(scores))
        sum_x2 = sum(i * i for i in range(n))
        
        if n * sum_x2 - sum_x * sum_x == 0:
            return QualityTrend.STABLE
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x * sum_x)
        
        # Classify trend based on slope
        if slope > 2.0:
            return QualityTrend.IMPROVING
        elif slope < -2.0:
            # Check if decline is critical
            score_drop = scores[0] - scores[-1]
            if score_drop > self.max_quality_decline:
                return QualityTrend.CRITICAL_DECLINE
            else:
                return QualityTrend.DECLINING
        else:
            return QualityTrend.STABLE
    
    async def _check_quality_thresholds(self, snapshot: QualitySnapshot, trend: QualityTrend):
        """Check quality thresholds and generate alerts"""
        alerts_to_generate = []
        
        # Critical threshold violation
        if snapshot.overall_score < self.critical_threshold:
            alerts_to_generate.append({
                'severity': 'CRITICAL',
                'message': f'Quality score critically low: {snapshot.overall_score:.1f}/100',
                'threshold_violated': f'critical_threshold ({self.critical_threshold})',
                'recommended_action': 'Immediate intervention required - consider rollback'
            })
        
        # Warning threshold violation
        elif snapshot.overall_score < self.warning_threshold:
            alerts_to_generate.append({
                'severity': 'WARNING',
                'message': f'Quality score below warning threshold: {snapshot.overall_score:.1f}/100',
                'threshold_violated': f'warning_threshold ({self.warning_threshold})',
                'recommended_action': 'Review and improve instruction quality'
            })
        
        # Critical decline trend
        if trend == QualityTrend.CRITICAL_DECLINE:
            alerts_to_generate.append({
                'severity': 'HIGH',
                'message': 'Critical quality decline detected',
                'threshold_violated': f'max_decline ({self.max_quality_decline}%)',
                'recommended_action': 'Investigate cause of quality degradation'
            })
        
        # Critical issues present
        if snapshot.critical_issues_count > 0:
            alerts_to_generate.append({
                'severity': 'HIGH', 
                'message': f'{snapshot.critical_issues_count} critical issues detected',
                'threshold_violated': 'critical_issues (0 expected)',
                'recommended_action': 'Address critical issues immediately'
            })
        
        # Generate alerts
        for alert_data in alerts_to_generate:
            await self._generate_alert(snapshot, alert_data)
    
    async def _generate_alert(self, snapshot: QualitySnapshot, alert_data: Dict[str, str]):
        """Generate a quality alert"""
        # Check alert cooldown
        recent_alerts = [a for a in self.active_alerts 
                        if a.file_path == snapshot.file_path 
                        and a.severity == alert_data['severity']
                        and (datetime.utcnow() - a.timestamp).total_seconds() < self.alert_cooldown]
        
        if recent_alerts:
            return  # Skip alert due to cooldown
        
        alert = QualityAlert(
            alert_id=f"{snapshot.file_path}_{alert_data['severity']}_{int(time.time())}",
            timestamp=datetime.utcnow(),
            severity=alert_data['severity'],
            file_path=snapshot.file_path,
            message=alert_data['message'],
            current_score=snapshot.overall_score,
            threshold_violated=alert_data['threshold_violated'],
            recommended_action=alert_data['recommended_action']
        )
        
        self.active_alerts.append(alert)
        self.monitoring_metrics['alerts_generated'] += 1
        
        if alert.severity == 'CRITICAL':
            self.monitoring_metrics['critical_alerts'] += 1
        
        # Execute alert callbacks
        for callback in self.alert_callbacks:
            try:
                await callback(alert)
            except Exception as e:
                logger.error(f"Error executing alert callback: {e}")
        
        logger.warning(f"Quality alert generated: {alert.severity} - {alert.message}")
    
    def add_alert_callback(self, callback: Callable):
        """Add callback function for quality alerts"""
        self.alert_callbacks.append(callback)
        logger.info(f"Alert callback added. Total callbacks: {len(self.alert_callbacks)}")
    
    async def get_quality_report(self, file_path: Optional[str] = None) -> Dict[str, Any]:
        """Get comprehensive quality report"""
        if file_path:
            # Single file report
            snapshots = self.quality_snapshots.get(file_path, [])
            if not snapshots:
                return {'error': f'No quality data available for {file_path}'}
            
            latest = snapshots[-1]
            trend = self._calculate_quality_trend(snapshots[-self.trend_analysis_window:]) if len(snapshots) >= 2 else QualityTrend.STABLE
            
            return {
                'file_path': file_path,
                'current_quality': {
                    'overall_score': latest.overall_score,
                    'classification': latest.quality_classification,
                    'issues_count': latest.issues_count,
                    'critical_issues': latest.critical_issues_count,
                    'last_updated': latest.timestamp.isoformat()
                },
                'trend': {
                    'direction': trend.value,
                    'snapshots_analyzed': len(snapshots[-self.trend_analysis_window:])
                },
                'alerts': [alert.to_dict() for alert in self.active_alerts if alert.file_path == file_path],
                'history': self.quality_history.get(file_path, [])[-20:]  # Last 20 entries
            }
        else:
            # All files report
            all_files_data = {}
            for fp in self.quality_snapshots.keys():
                file_report = await self.get_quality_report(fp)
                all_files_data[fp] = file_report
            
            return {
                'monitoring_summary': {
                    'files_monitored': len(self.quality_snapshots),
                    'active_alerts': len(self.active_alerts),
                    'critical_alerts': self.monitoring_metrics['critical_alerts'],
                    'is_monitoring': self.is_monitoring
                },
                'files': all_files_data,
                'metrics': self.monitoring_metrics
            }
    
    async def get_quality_dashboard(self) -> Dict[str, Any]:
        """Get quality monitoring dashboard data"""
        dashboard_data = {
            'summary': {
                'total_files': len(self.quality_snapshots),
                'active_monitoring': len(self.monitoring_tasks),
                'total_alerts': len(self.active_alerts),
                'critical_alerts': len([a for a in self.active_alerts if a.severity == 'CRITICAL']),
                'average_quality': 0.0,
                'quality_distribution': {
                    'excellent': 0,
                    'good': 0,
                    'acceptable': 0,
                    'needs_improvement': 0,
                    'unacceptable': 0
                }
            },
            'files_status': {},
            'recent_alerts': [],
            'quality_trends': {},
            'metrics': self.monitoring_metrics
        }
        
        # Calculate summary statistics
        all_latest_scores = []
        for file_path, snapshots in self.quality_snapshots.items():
            if snapshots:
                latest = snapshots[-1]
                all_latest_scores.append(latest.overall_score)
                
                # Quality distribution
                classification = latest.quality_classification.lower()
                if classification in dashboard_data['summary']['quality_distribution']:
                    dashboard_data['summary']['quality_distribution'][classification] += 1
                
                # File status
                trend = self._calculate_quality_trend(snapshots[-self.trend_analysis_window:]) if len(snapshots) >= 2 else QualityTrend.STABLE
                dashboard_data['files_status'][file_path] = {
                    'score': latest.overall_score,
                    'classification': latest.quality_classification,
                    'trend': trend.value,
                    'issues': latest.issues_count,
                    'last_check': latest.timestamp.isoformat()
                }
        
        if all_latest_scores:
            dashboard_data['summary']['average_quality'] = sum(all_latest_scores) / len(all_latest_scores)
        
        # Recent alerts (last 10)
        recent_alerts = sorted(self.active_alerts, key=lambda x: x.timestamp, reverse=True)[:10]
        dashboard_data['recent_alerts'] = [alert.to_dict() for alert in recent_alerts]
        
        # Quality trends
        for file_path, history in self.quality_history.items():
            if history:
                dashboard_data['quality_trends'][file_path] = history[-10:]  # Last 10 entries
        
        return dashboard_data
    
    async def clear_resolved_alerts(self, file_path: Optional[str] = None):
        """Clear resolved alerts (where quality has improved)"""
        alerts_to_remove = []
        
        for alert in self.active_alerts:
            if file_path and alert.file_path != file_path:
                continue
            
            # Check if quality has improved
            snapshots = self.quality_snapshots.get(alert.file_path, [])
            if snapshots:
                latest = snapshots[-1]
                
                # Alert resolved if current score is above the threshold that was violated
                if alert.threshold_violated.startswith('critical_threshold') and latest.overall_score >= self.critical_threshold:
                    alerts_to_remove.append(alert)
                elif alert.threshold_violated.startswith('warning_threshold') and latest.overall_score >= self.warning_threshold:
                    alerts_to_remove.append(alert)
                elif alert.threshold_violated.startswith('critical_issues') and latest.critical_issues_count == 0:
                    alerts_to_remove.append(alert)
        
        # Remove resolved alerts
        for alert in alerts_to_remove:
            self.active_alerts.remove(alert)
            logger.info(f"Resolved alert cleared: {alert.alert_id}")
    
    async def validate_update_quality_impact(self, file_path: str, original_content: str, updated_content: str) -> Dict[str, Any]:
        """Validate quality impact of an update before applying"""
        logger.info(f"Validating update quality impact for {file_path}")
        
        # Create temporary file with updated content
        temp_file = None
        try:
            import tempfile
            temp_fd, temp_file = tempfile.mkstemp(suffix='.md', text=True)
            with os.fdopen(temp_fd, 'w') as f:
                f.write(updated_content)
            
            # Get current quality
            current_validation = await self.framework_connector.validate_instruction_file(
                file_path, ValidationType.PRE_UPDATE
            )
            
            # Get updated quality
            updated_validation = await self.framework_connector.validate_instruction_file(
                temp_file, ValidationType.POST_UPDATE
            )
            
            # Calculate impact
            quality_change = updated_validation.overall_score - current_validation.overall_score
            
            # Determine recommendation
            recommendation = "APPROVE"
            if quality_change < -self.max_quality_decline:
                recommendation = "REJECT"
            elif quality_change < -5.0:
                recommendation = "CAUTION"
            
            return {
                'recommendation': recommendation,
                'quality_change': quality_change,
                'current_score': current_validation.overall_score,
                'updated_score': updated_validation.overall_score,
                'current_issues': len(current_validation.issues),
                'updated_issues': len(updated_validation.issues),
                'impact_analysis': {
                    'quality_preserved': quality_change >= -2.0,
                    'significant_decline': quality_change < -self.max_quality_decline,
                    'new_critical_issues': len([i for i in updated_validation.issues if i.severity.value == 'critical']) > 
                                          len([i for i in current_validation.issues if i.severity.value == 'critical']),
                    'approval_status_changed': current_validation.approval_status != updated_validation.approval_status
                }
            }
            
        finally:
            # Cleanup temporary file
            if temp_file and os.path.exists(temp_file):
                os.unlink(temp_file)


async def main():
    """Main function for testing"""
    try:
        # Initialize framework connector and quality monitor
        from .framework_connector import AIInstructionFrameworkConnector
        
        framework_config = {'quality_threshold': 75.0}
        framework_connector = AIInstructionFrameworkConnector(framework_config)
        
        monitor_config = {
            'critical_threshold': 50.0,
            'warning_threshold': 65.0,
            'monitoring_interval': 10
        }
        
        quality_monitor = QualityMonitor(framework_connector, monitor_config)
        
        # Test monitoring
        test_files = [
            '/Users/georgiospilitsoglou/Developer/projects/mypromptflow/.claude/commands/ai-help.md'
        ]
        
        existing_files = [f for f in test_files if Path(f).exists()]
        
        if existing_files:
            # Add alert callback
            async def alert_handler(alert):
                print(f"ALERT: {alert.severity} - {alert.message}")
            
            quality_monitor.add_alert_callback(alert_handler)
            
            # Start monitoring
            await quality_monitor.start_monitoring(existing_files, MonitoringMode.ON_DEMAND)
            
            # Get dashboard
            dashboard = await quality_monitor.get_quality_dashboard()
            print("Quality Monitor Dashboard:")
            print(json.dumps(dashboard, indent=2, default=str))
        
        print("\nQuality Monitor test completed successfully!")
        
    except Exception as e:
        print(f"Error testing quality monitor: {e}")
        return 1
        
    return 0


if __name__ == "__main__":
    import sys
    import os
    sys.exit(asyncio.run(main()))