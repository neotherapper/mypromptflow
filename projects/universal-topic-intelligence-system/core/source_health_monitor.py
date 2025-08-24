#!/usr/bin/env python3
"""
Source Health Monitoring System
Tracks source reliability, performance, and health metrics
"""

import sqlite3
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import statistics

class SourceStatus(Enum):
    """Source health status levels"""
    HEALTHY = "healthy"           # 95%+ success rate, normal response times
    WARNING = "warning"           # 80-94% success rate, or slow response times
    DEGRADED = "degraded"         # 50-79% success rate, frequent issues
    CRITICAL = "critical"         # <50% success rate, consistent failures
    UNKNOWN = "unknown"           # Not enough data


@dataclass
class SourceHealthMetrics:
    """Comprehensive health metrics for a source"""
    source_id: str
    source_name: str
    
    # Success/Failure metrics
    total_checks: int
    successful_checks: int
    failed_checks: int
    success_rate: float
    
    # Response time metrics
    avg_response_time: float
    median_response_time: float
    p95_response_time: float
    
    # Error analysis
    error_types: Dict[str, int]  # error_type -> count
    consecutive_failures: int
    last_success_time: Optional[datetime]
    last_failure_time: Optional[datetime]
    
    # Content metrics
    avg_items_per_check: float
    total_items_collected: int
    
    # Health assessment
    status: SourceStatus
    health_score: float  # 0-100 score
    issues: List[str]    # Current issues
    
    # Timestamps
    first_check_time: datetime
    last_check_time: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        # Convert datetime objects to ISO strings
        for key, value in data.items():
            if isinstance(value, datetime):
                data[key] = value.isoformat() if value else None
        data['status'] = self.status.value
        return data


class SourceHealthMonitor:
    """
    Monitors and tracks health metrics for all sources
    """
    
    def __init__(self, db_path: str = "topic_intelligence.db"):
        """
        Initialize source health monitor
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        self.logger = logging.getLogger("SourceHealthMonitor")
        self._ensure_health_tables()
    
    def _ensure_health_tables(self):
        """Create health monitoring tables if they don't exist"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Source health checks table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS source_health_checks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_id TEXT NOT NULL,
                    check_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    success BOOLEAN NOT NULL,
                    response_time_ms INTEGER,
                    error_type TEXT,
                    error_message TEXT,
                    items_found INTEGER DEFAULT 0,
                    items_stored INTEGER DEFAULT 0,
                    metadata TEXT  -- JSON for additional metrics
                )
            """)
            
            # Source health summary table (current status)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS source_health_summary (
                    source_id TEXT PRIMARY KEY,
                    source_name TEXT NOT NULL,
                    status TEXT NOT NULL,
                    health_score REAL DEFAULT 0,
                    success_rate REAL DEFAULT 0,
                    total_checks INTEGER DEFAULT 0,
                    successful_checks INTEGER DEFAULT 0,
                    failed_checks INTEGER DEFAULT 0,
                    consecutive_failures INTEGER DEFAULT 0,
                    avg_response_time REAL DEFAULT 0,
                    avg_items_per_check REAL DEFAULT 0,
                    last_check_time TIMESTAMP,
                    last_success_time TIMESTAMP,
                    last_failure_time TIMESTAMP,
                    error_summary TEXT,  -- JSON of error types
                    issues TEXT,         -- JSON array of current issues
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (source_id) REFERENCES sources(source_id)
                )
            """)
            
            # Create indexes for performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_health_checks_source_time ON source_health_checks(source_id, check_time DESC)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_health_checks_success ON source_health_checks(success, check_time DESC)")
            
            conn.commit()
            self.logger.info("Source health monitoring tables initialized")
    
    def record_check(self, source_id: str, source_name: str, success: bool, 
                    response_time_ms: Optional[int] = None, error_type: str = None, 
                    error_message: str = None, items_found: int = 0, 
                    items_stored: int = 0, **metadata) -> None:
        """
        Record a health check result for a source
        
        Args:
            source_id: Source identifier
            source_name: Human-readable source name
            success: Whether the check was successful
            response_time_ms: Response time in milliseconds
            error_type: Type of error if failed (e.g., '404', 'timeout', 'parse_error')
            error_message: Detailed error message
            items_found: Number of items discovered
            items_stored: Number of items successfully stored
            **metadata: Additional metrics
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Record the health check
                cursor.execute("""
                    INSERT INTO source_health_checks (
                        source_id, success, response_time_ms, error_type, 
                        error_message, items_found, items_stored, metadata
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    source_id, success, response_time_ms, error_type,
                    error_message, items_found, items_stored, 
                    json.dumps(metadata) if metadata else None
                ))
                
                # Update or create health summary
                self._update_health_summary(cursor, source_id, source_name)
                
                conn.commit()
                self.logger.debug(f"Recorded health check for {source_name}: {'SUCCESS' if success else 'FAILED'}")
                
        except Exception as e:
            self.logger.error(f"Error recording health check for {source_id}: {e}")
    
    def _update_health_summary(self, cursor, source_id: str, source_name: str):
        """Update the health summary for a source"""
        
        # Get recent health data (last 30 days)
        cursor.execute("""
            SELECT success, response_time_ms, error_type, items_found, check_time
            FROM source_health_checks 
            WHERE source_id = ? AND check_time > datetime('now', '-30 days')
            ORDER BY check_time DESC
        """, (source_id,))
        
        recent_checks = cursor.fetchall()
        
        if not recent_checks:
            return
        
        # Calculate metrics
        total_checks = len(recent_checks)
        successful_checks = sum(1 for check in recent_checks if check[0])
        failed_checks = total_checks - successful_checks
        success_rate = successful_checks / total_checks if total_checks > 0 else 0
        
        # Response time metrics (only from successful checks)
        response_times = [check[1] for check in recent_checks if check[1] is not None and check[0]]
        avg_response_time = statistics.mean(response_times) if response_times else 0
        
        # Error analysis
        error_types = {}
        for check in recent_checks:
            if not check[0] and check[2]:  # Failed check with error type
                error_types[check[2]] = error_types.get(check[2], 0) + 1
        
        # Calculate consecutive failures
        consecutive_failures = 0
        for check in recent_checks:
            if check[0]:  # Success
                break
            consecutive_failures += 1
        
        # Items per check
        items_counts = [check[3] for check in recent_checks if check[3] is not None]
        avg_items_per_check = statistics.mean(items_counts) if items_counts else 0
        
        # Find last success and failure times
        last_success_time = None
        last_failure_time = None
        
        for check in recent_checks:
            if check[0] and last_success_time is None:  # First success found (most recent)
                last_success_time = check[4]
            elif not check[0] and last_failure_time is None:  # First failure found (most recent)
                last_failure_time = check[4]
            
            if last_success_time and last_failure_time:
                break
        
        # Determine status and health score
        status, health_score, issues = self._calculate_health_status(
            success_rate, consecutive_failures, avg_response_time, error_types
        )
        
        # Update summary
        cursor.execute("""
            INSERT OR REPLACE INTO source_health_summary (
                source_id, source_name, status, health_score, success_rate,
                total_checks, successful_checks, failed_checks, consecutive_failures,
                avg_response_time, avg_items_per_check, last_check_time,
                last_success_time, last_failure_time, error_summary, issues,
                updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (
            source_id, source_name, status.value, health_score, success_rate,
            total_checks, successful_checks, failed_checks, consecutive_failures,
            avg_response_time, avg_items_per_check, recent_checks[0][4],
            last_success_time, last_failure_time, json.dumps(error_types),
            json.dumps(issues)
        ))
    
    def _calculate_health_status(self, success_rate: float, consecutive_failures: int, 
                               avg_response_time: float, error_types: Dict[str, int]) -> Tuple[SourceStatus, float, List[str]]:
        """
        Calculate health status, score, and issues list
        
        Returns:
            Tuple of (status, health_score, issues_list)
        """
        issues = []
        health_score = 100.0
        
        # Success rate assessment
        if success_rate >= 0.95:
            status = SourceStatus.HEALTHY
        elif success_rate >= 0.80:
            status = SourceStatus.WARNING
            issues.append(f"Success rate below 95%: {success_rate:.1%}")
            health_score -= (0.95 - success_rate) * 200  # Reduce score
        elif success_rate >= 0.50:
            status = SourceStatus.DEGRADED
            issues.append(f"Success rate below 80%: {success_rate:.1%}")
            health_score -= (0.95 - success_rate) * 150
        else:
            status = SourceStatus.CRITICAL
            issues.append(f"Critical success rate: {success_rate:.1%}")
            health_score = min(health_score, 25)  # Cap at 25 for critical sources
        
        # Consecutive failures assessment
        if consecutive_failures >= 5:
            status = SourceStatus.CRITICAL
            issues.append(f"{consecutive_failures} consecutive failures")
            health_score = min(health_score, 20)
        elif consecutive_failures >= 3:
            if status not in [SourceStatus.CRITICAL]:
                status = SourceStatus.DEGRADED
            issues.append(f"{consecutive_failures} consecutive failures")
            health_score -= consecutive_failures * 10
        
        # Response time assessment
        if avg_response_time > 30000:  # 30 seconds
            issues.append(f"Slow response times: {avg_response_time/1000:.1f}s average")
            health_score -= 15
        elif avg_response_time > 10000:  # 10 seconds
            issues.append(f"Moderate response times: {avg_response_time/1000:.1f}s average")
            health_score -= 5
        
        # Error type analysis
        critical_errors = ['404', 'forbidden', 'ssl_error']
        if any(error in error_types for error in critical_errors):
            if '404' in error_types:
                issues.append("Feed not found (404 errors)")
            if 'forbidden' in error_types:
                issues.append("Access forbidden (403 errors)")
            if 'ssl_error' in error_types:
                issues.append("SSL/TLS connection issues")
            
            health_score -= 20
        
        # Ensure health score is within bounds
        health_score = max(0, min(100, health_score))
        
        return status, health_score, issues
    
    def get_source_health(self, source_id: str) -> Optional[SourceHealthMetrics]:
        """
        Get comprehensive health metrics for a specific source
        
        Args:
            source_id: Source identifier
            
        Returns:
            SourceHealthMetrics object or None if source not found
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get summary data
                cursor.execute("""
                    SELECT * FROM source_health_summary WHERE source_id = ?
                """, (source_id,))
                
                summary_row = cursor.fetchone()
                if not summary_row:
                    return None
                
                # Get additional metrics from recent checks
                cursor.execute("""
                    SELECT response_time_ms, items_found, check_time
                    FROM source_health_checks 
                    WHERE source_id = ? AND check_time > datetime('now', '-30 days')
                    AND response_time_ms IS NOT NULL
                    ORDER BY response_time_ms
                """, (source_id,))
                
                response_data = cursor.fetchall()
                response_times = [row[0] for row in response_data if row[0] is not None]
                
                # Calculate percentiles
                median_response_time = statistics.median(response_times) if response_times else 0
                p95_response_time = statistics.quantiles(response_times, n=20)[18] if len(response_times) >= 20 else (max(response_times) if response_times else 0)
                
                # Get first check time
                cursor.execute("""
                    SELECT MIN(check_time) FROM source_health_checks WHERE source_id = ?
                """, (source_id,))
                first_check = cursor.fetchone()[0]
                
                # Parse summary data
                (_, source_name, status_str, health_score, success_rate, total_checks,
                 successful_checks, failed_checks, consecutive_failures, avg_response_time,
                 avg_items_per_check, last_check_time, last_success_time, last_failure_time,
                 error_summary, issues, _) = summary_row
                
                return SourceHealthMetrics(
                    source_id=source_id,
                    source_name=source_name,
                    total_checks=total_checks,
                    successful_checks=successful_checks,
                    failed_checks=failed_checks,
                    success_rate=success_rate,
                    avg_response_time=avg_response_time,
                    median_response_time=median_response_time,
                    p95_response_time=p95_response_time,
                    error_types=json.loads(error_summary) if error_summary else {},
                    consecutive_failures=consecutive_failures,
                    last_success_time=datetime.fromisoformat(last_success_time) if last_success_time else None,
                    last_failure_time=datetime.fromisoformat(last_failure_time) if last_failure_time else None,
                    avg_items_per_check=avg_items_per_check,
                    total_items_collected=0,  # Would need separate query for this
                    status=SourceStatus(status_str),
                    health_score=health_score,
                    issues=json.loads(issues) if issues else [],
                    first_check_time=datetime.fromisoformat(first_check) if first_check else datetime.now(),
                    last_check_time=datetime.fromisoformat(last_check_time) if last_check_time else datetime.now()
                )
                
        except Exception as e:
            self.logger.error(f"Error getting source health for {source_id}: {e}")
            return None
    
    def get_health_dashboard(self) -> Dict[str, Any]:
        """
        Generate comprehensive health dashboard data
        
        Returns:
            Dictionary with dashboard metrics and source summaries
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Overall system health
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_sources,
                        SUM(CASE WHEN status = 'healthy' THEN 1 ELSE 0 END) as healthy_count,
                        SUM(CASE WHEN status = 'warning' THEN 1 ELSE 0 END) as warning_count,
                        SUM(CASE WHEN status = 'degraded' THEN 1 ELSE 0 END) as degraded_count,
                        SUM(CASE WHEN status = 'critical' THEN 1 ELSE 0 END) as critical_count,
                        AVG(health_score) as avg_health_score,
                        AVG(success_rate) as avg_success_rate
                    FROM source_health_summary
                """)
                
                system_metrics = cursor.fetchone()
                
                # Source details
                cursor.execute("""
                    SELECT source_id, source_name, status, health_score, success_rate,
                           consecutive_failures, last_check_time, issues
                    FROM source_health_summary
                    ORDER BY 
                        CASE status 
                            WHEN 'critical' THEN 1 
                            WHEN 'degraded' THEN 2 
                            WHEN 'warning' THEN 3 
                            WHEN 'healthy' THEN 4 
                            ELSE 5 
                        END,
                        health_score ASC
                """)
                
                source_details = []
                for row in cursor.fetchall():
                    source_details.append({
                        'source_id': row[0],
                        'source_name': row[1],
                        'status': row[2],
                        'health_score': row[3],
                        'success_rate': row[4],
                        'consecutive_failures': row[5],
                        'last_check_time': row[6],
                        'issues': json.loads(row[7]) if row[7] else []
                    })
                
                # Recent activity (last 24 hours)
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_checks,
                        SUM(CASE WHEN success THEN 1 ELSE 0 END) as successful_checks,
                        COUNT(DISTINCT source_id) as sources_checked,
                        AVG(response_time_ms) as avg_response_time
                    FROM source_health_checks
                    WHERE check_time > datetime('now', '-24 hours')
                """)
                
                recent_activity = cursor.fetchone()
                
                # Top error types (last 7 days)
                cursor.execute("""
                    SELECT error_type, COUNT(*) as count
                    FROM source_health_checks
                    WHERE error_type IS NOT NULL 
                        AND check_time > datetime('now', '-7 days')
                    GROUP BY error_type
                    ORDER BY count DESC
                    LIMIT 5
                """)
                
                top_errors = [{'error_type': row[0], 'count': row[1]} for row in cursor.fetchall()]
                
                return {
                    'timestamp': datetime.now().isoformat(),
                    'system_health': {
                        'total_sources': system_metrics[0] or 0,
                        'healthy_sources': system_metrics[1] or 0,
                        'warning_sources': system_metrics[2] or 0,
                        'degraded_sources': system_metrics[3] or 0,
                        'critical_sources': system_metrics[4] or 0,
                        'avg_health_score': round(system_metrics[5] or 0, 1),
                        'avg_success_rate': round(system_metrics[6] or 0, 3)
                    },
                    'recent_activity': {
                        'total_checks_24h': recent_activity[0] or 0,
                        'successful_checks_24h': recent_activity[1] or 0,
                        'sources_checked_24h': recent_activity[2] or 0,
                        'avg_response_time_24h': round(recent_activity[3] or 0, 1)
                    },
                    'top_errors': top_errors,
                    'sources': source_details
                }
                
        except Exception as e:
            self.logger.error(f"Error generating health dashboard: {e}")
            return {'error': str(e)}
    
    def get_critical_alerts(self) -> List[Dict[str, Any]]:
        """
        Get list of critical health alerts that need immediate attention
        
        Returns:
            List of alert dictionaries
        """
        alerts = []
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Critical sources
                cursor.execute("""
                    SELECT source_id, source_name, consecutive_failures, last_failure_time, issues
                    FROM source_health_summary
                    WHERE status = 'critical' OR consecutive_failures >= 5
                    ORDER BY consecutive_failures DESC
                """)
                
                for row in cursor.fetchall():
                    alerts.append({
                        'type': 'critical_source',
                        'source_id': row[0],
                        'source_name': row[1],
                        'message': f"{row[1]} has {row[2]} consecutive failures",
                        'consecutive_failures': row[2],
                        'last_failure_time': row[3],
                        'issues': json.loads(row[4]) if row[4] else [],
                        'priority': 'high'
                    })
                
                # Recent widespread failures
                cursor.execute("""
                    SELECT COUNT(DISTINCT source_id) as failed_sources
                    FROM source_health_checks
                    WHERE check_time > datetime('now', '-1 hours')
                      AND success = 0
                """)
                
                recent_failures = cursor.fetchone()[0]
                if recent_failures >= 5:
                    alerts.append({
                        'type': 'system_wide_issues',
                        'message': f"{recent_failures} sources failed in the last hour",
                        'failed_sources': recent_failures,
                        'priority': 'medium'
                    })
        
        except Exception as e:
            self.logger.error(f"Error getting critical alerts: {e}")
            alerts.append({
                'type': 'system_error',
                'message': f"Health monitoring system error: {str(e)}",
                'priority': 'high'
            })
        
        return alerts
    
    def cleanup_old_data(self, days_to_keep: int = 90):
        """
        Clean up old health check data
        
        Args:
            days_to_keep: Number of days of data to retain
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cutoff_date = datetime.now() - timedelta(days=days_to_keep)
                
                cursor.execute("""
                    DELETE FROM source_health_checks 
                    WHERE check_time < ?
                """, (cutoff_date.isoformat(),))
                
                deleted_count = cursor.rowcount
                conn.commit()
                
                self.logger.info(f"Cleaned up {deleted_count} old health check records")
                
        except Exception as e:
            self.logger.error(f"Error cleaning up old health data: {e}")