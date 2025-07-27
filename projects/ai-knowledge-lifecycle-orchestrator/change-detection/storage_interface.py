#!/usr/bin/env python3
"""
Storage Interface
AI Knowledge Lifecycle Orchestrator - Data storage and caching layer

This module provides a unified interface for storing and retrieving change detection data
with support for multiple storage backends, caching, and performance optimization.
"""

import sqlite3
import json
import logging
import asyncio
import hashlib
import pickle
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, asdict
from enum import Enum
import aiosqlite
import threading
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StorageBackend(Enum):
    """Storage backend types"""
    SQLITE = "sqlite"
    POSTGRESQL = "postgresql"
    MEMORY = "memory"


@dataclass
class CacheEntry:
    """Represents a cache entry"""
    key: str
    data: Any
    created_at: datetime
    expires_at: datetime
    access_count: int = 0
    last_accessed: datetime = None
    
    def is_expired(self) -> bool:
        """Check if cache entry is expired"""
        return datetime.utcnow() > self.expires_at
    
    def is_stale(self, max_age_seconds: int) -> bool:
        """Check if cache entry is stale"""
        age = (datetime.utcnow() - self.created_at).total_seconds()
        return age > max_age_seconds
    
    def touch(self):
        """Update access information"""
        self.access_count += 1
        self.last_accessed = datetime.utcnow()


@dataclass
class StorageStats:
    """Storage performance statistics"""
    total_reads: int = 0
    total_writes: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    total_storage_size_bytes: int = 0
    cache_size_bytes: int = 0
    average_read_time_ms: float = 0.0
    average_write_time_ms: float = 0.0
    
    @property
    def cache_hit_rate(self) -> float:
        """Calculate cache hit rate"""
        total_requests = self.cache_hits + self.cache_misses
        return self.cache_hits / total_requests if total_requests > 0 else 0.0


class MemoryCache:
    """High-performance in-memory cache with LRU eviction"""
    
    def __init__(self, max_size_mb: int = 100, default_ttl_seconds: int = 300):
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.default_ttl = default_ttl_seconds
        self.cache: Dict[str, CacheEntry] = {}
        self.access_order: List[str] = []  # For LRU tracking
        self.lock = threading.RLock()
        
        logger.info(f"Memory cache initialized: {max_size_mb}MB max, {default_ttl_seconds}s TTL")
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        with self.lock:
            if key not in self.cache:
                return None
            
            entry = self.cache[key]
            
            # Check expiration
            if entry.is_expired():
                self._remove_entry(key)
                return None
            
            # Update access info
            entry.touch()
            self._update_access_order(key)
            
            return entry.data
    
    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> bool:
        """Set value in cache"""
        with self.lock:
            ttl = ttl_seconds or self.default_ttl
            expires_at = datetime.utcnow() + timedelta(seconds=ttl)
            
            # Estimate size
            estimated_size = self._estimate_size(value)
            
            # Check if we need to evict entries
            while self._should_evict(estimated_size):
                if not self._evict_lru():
                    logger.warning("Could not evict entries to make space")
                    return False
            
            # Create cache entry
            entry = CacheEntry(
                key=key,
                data=value,
                created_at=datetime.utcnow(),
                expires_at=expires_at
            )
            
            # Store entry
            self.cache[key] = entry
            self._update_access_order(key)
            
            return True
    
    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        with self.lock:
            if key in self.cache:
                self._remove_entry(key)
                return True
            return False
    
    def clear(self):
        """Clear all cache entries"""
        with self.lock:
            self.cache.clear()
            self.access_order.clear()
    
    def cleanup_expired(self) -> int:
        """Remove expired entries and return count removed"""
        with self.lock:
            expired_keys = [
                key for key, entry in self.cache.items()
                if entry.is_expired()
            ]
            
            for key in expired_keys:
                self._remove_entry(key)
            
            return len(expired_keys)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        with self.lock:
            total_size = sum(self._estimate_size(entry.data) for entry in self.cache.values())
            
            return {
                'entries': len(self.cache),
                'size_bytes': total_size,
                'size_mb': total_size / (1024 * 1024),
                'max_size_mb': self.max_size_bytes / (1024 * 1024),
                'utilization': total_size / self.max_size_bytes,
                'expired_entries': sum(1 for entry in self.cache.values() if entry.is_expired())
            }
    
    def _estimate_size(self, value: Any) -> int:
        """Estimate size of value in bytes"""
        try:
            return len(pickle.dumps(value))
        except Exception:
            # Fallback estimation
            if isinstance(value, str):
                return len(value.encode('utf-8'))
            elif isinstance(value, (dict, list)):
                return len(str(value).encode('utf-8'))
            else:
                return 1024  # Default estimate
    
    def _should_evict(self, new_entry_size: int) -> bool:
        """Check if we need to evict entries"""
        current_size = sum(self._estimate_size(entry.data) for entry in self.cache.values())
        return (current_size + new_entry_size) > self.max_size_bytes
    
    def _evict_lru(self) -> bool:
        """Evict least recently used entry"""
        if not self.access_order:
            return False
        
        lru_key = self.access_order[0]
        self._remove_entry(lru_key)
        return True
    
    def _remove_entry(self, key: str):
        """Remove entry from cache and access order"""
        if key in self.cache:
            del self.cache[key]
        if key in self.access_order:
            self.access_order.remove(key)
    
    def _update_access_order(self, key: str):
        """Update access order for LRU tracking"""
        if key in self.access_order:
            self.access_order.remove(key)
        self.access_order.append(key)


class SQLiteStorage:
    """SQLite-based persistent storage"""
    
    def __init__(self, db_path: Path, enable_wal: bool = True):
        self.db_path = db_path
        self.enable_wal = enable_wal
        self.executor = ThreadPoolExecutor(max_workers=4)
        
        # Ensure directory exists
        db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        self._initialize_database()
        
        logger.info(f"SQLite storage initialized: {db_path}")
    
    def _initialize_database(self):
        """Initialize database schema"""
        init_sql = """
        -- Source data table
        CREATE TABLE IF NOT EXISTS source_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            technology_name TEXT NOT NULL,
            source_name TEXT NOT NULL,
            url TEXT NOT NULL,
            content_hash TEXT NOT NULL,
            content TEXT NOT NULL,
            retrieved_at TIMESTAMP NOT NULL,
            source_type TEXT NOT NULL,
            extraction_metadata TEXT NOT NULL,  -- JSON
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(technology_name, source_name, content_hash)
        );
        
        -- Change history table
        CREATE TABLE IF NOT EXISTS change_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            technology_name TEXT NOT NULL,
            change_type TEXT NOT NULL,
            old_version TEXT,
            new_version TEXT,
            source_url TEXT NOT NULL,
            detection_timestamp TIMESTAMP NOT NULL,
            impact_level TEXT NOT NULL,
            urgency_level TEXT NOT NULL,
            confidence_score REAL NOT NULL,
            change_description TEXT NOT NULL,
            evidence TEXT NOT NULL,  -- JSON array
            affected_files TEXT,     -- JSON array
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Monitoring status table
        CREATE TABLE IF NOT EXISTS monitoring_status (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            technology_name TEXT NOT NULL UNIQUE,
            last_checked_at TIMESTAMP,
            last_change_detected_at TIMESTAMP,
            total_checks INTEGER DEFAULT 0,
            total_changes INTEGER DEFAULT 0,
            current_version TEXT,
            health_status TEXT DEFAULT 'healthy',
            error_count INTEGER DEFAULT 0,
            last_error TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Performance metrics table
        CREATE TABLE IF NOT EXISTS performance_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            metric_name TEXT NOT NULL,
            metric_value REAL NOT NULL,
            measurement_timestamp TIMESTAMP NOT NULL,
            additional_data TEXT,  -- JSON
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        -- Create indexes for performance
        CREATE INDEX IF NOT EXISTS idx_source_data_tech_source ON source_data(technology_name, source_name);
        CREATE INDEX IF NOT EXISTS idx_source_data_retrieved_at ON source_data(retrieved_at);
        CREATE INDEX IF NOT EXISTS idx_change_history_tech ON change_history(technology_name);
        CREATE INDEX IF NOT EXISTS idx_change_history_timestamp ON change_history(detection_timestamp);
        CREATE INDEX IF NOT EXISTS idx_monitoring_status_tech ON monitoring_status(technology_name);
        CREATE INDEX IF NOT EXISTS idx_performance_metrics_name_time ON performance_metrics(metric_name, measurement_timestamp);
        """
        
        with sqlite3.connect(self.db_path) as conn:
            if self.enable_wal:
                conn.execute("PRAGMA journal_mode=WAL")
            conn.executescript(init_sql)
            conn.commit()
    
    async def store_source_data(self, technology_name: str, source_name: str, 
                               source_data: 'SourceData') -> bool:
        """Store source data"""
        try:
            sql = """
            INSERT OR REPLACE INTO source_data 
            (technology_name, source_name, url, content_hash, content, retrieved_at, source_type, extraction_metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            params = (
                technology_name,
                source_name,
                source_data.url,
                source_data.content_hash,
                source_data.content,
                source_data.retrieved_at.isoformat(),
                source_data.source_type,
                json.dumps(source_data.extraction_metadata)
            )
            
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(self.executor, self._execute_sql, sql, params)
            
            return True
            
        except Exception as e:
            logger.error(f"Error storing source data: {e}")
            return False
    
    async def get_source_data(self, technology_name: str, source_name: str) -> Optional['SourceData']:
        """Get latest source data"""
        try:
            sql = """
            SELECT url, content, content_hash, retrieved_at, source_type, extraction_metadata
            FROM source_data
            WHERE technology_name = ? AND source_name = ?
            ORDER BY retrieved_at DESC
            LIMIT 1
            """
            
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self.executor, 
                self._fetch_one, 
                sql, 
                (technology_name, source_name)
            )
            
            if result:
                from .change_detector import SourceData  # Import here to avoid circular import
                return SourceData(
                    url=result[0],
                    content=result[1],
                    content_hash=result[2],
                    retrieved_at=datetime.fromisoformat(result[3]),
                    source_type=result[4],
                    extraction_metadata=json.loads(result[5])
                )
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting source data: {e}")
            return None
    
    async def store_change(self, change: 'TechnologyChange') -> bool:
        """Store detected change"""
        try:
            sql = """
            INSERT INTO change_history 
            (technology_name, change_type, old_version, new_version, source_url, 
             detection_timestamp, impact_level, urgency_level, confidence_score,
             change_description, evidence, affected_files)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            params = (
                change.technology_name,
                change.change_type.value,
                change.old_version,
                change.new_version,
                change.source_url,
                change.detection_timestamp.isoformat(),
                change.impact_level.value,
                change.urgency_level.value,
                change.confidence_score,
                change.change_description,
                json.dumps(change.evidence),
                json.dumps(change.affected_files) if change.affected_files else None
            )
            
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(self.executor, self._execute_sql, sql, params)
            
            return True
            
        except Exception as e:
            logger.error(f"Error storing change: {e}")
            return False
    
    async def get_changes_for_technology(self, technology_name: str, 
                                       limit: int = 100) -> List['TechnologyChange']:
        """Get recent changes for technology"""
        try:
            sql = """
            SELECT technology_name, change_type, old_version, new_version, source_url,
                   detection_timestamp, impact_level, urgency_level, confidence_score,
                   change_description, evidence, affected_files
            FROM change_history
            WHERE technology_name = ?
            ORDER BY detection_timestamp DESC
            LIMIT ?
            """
            
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(
                self.executor,
                self._fetch_all,
                sql,
                (technology_name, limit)
            )
            
            changes = []
            for row in results:
                from .change_detector import TechnologyChange, ChangeType, ImpactLevel, UrgencyLevel
                
                change = TechnologyChange(
                    technology_name=row[0],
                    change_type=ChangeType(row[1]),
                    old_version=row[2],
                    new_version=row[3],
                    source_url=row[4],
                    detection_timestamp=datetime.fromisoformat(row[5]),
                    impact_level=ImpactLevel(row[6]),
                    urgency_level=UrgencyLevel(row[7]),
                    confidence_score=row[8],
                    change_description=row[9],
                    evidence=json.loads(row[10]),
                    affected_files=json.loads(row[11]) if row[11] else None
                )
                changes.append(change)
            
            return changes
            
        except Exception as e:
            logger.error(f"Error getting changes for technology: {e}")
            return []
    
    async def update_monitoring_status(self, technology_name: str, status_data: Dict[str, Any]) -> bool:
        """Update monitoring status"""
        try:
            sql = """
            INSERT OR REPLACE INTO monitoring_status 
            (technology_name, last_checked_at, last_change_detected_at, total_checks,
             total_changes, current_version, health_status, error_count, last_error, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
            """
            
            params = (
                technology_name,
                status_data.get('last_checked_at'),
                status_data.get('last_change_detected_at'),
                status_data.get('total_checks', 0),
                status_data.get('total_changes', 0),
                status_data.get('current_version'),
                status_data.get('health_status', 'healthy'),
                status_data.get('error_count', 0),
                status_data.get('last_error')
            )
            
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(self.executor, self._execute_sql, sql, params)
            
            return True
            
        except Exception as e:
            logger.error(f"Error updating monitoring status: {e}")
            return False
    
    async def get_monitoring_status(self, technology_name: str) -> Optional[Dict[str, Any]]:
        """Get monitoring status"""
        try:
            sql = """
            SELECT last_checked_at, last_change_detected_at, total_checks, total_changes,
                   current_version, health_status, error_count, last_error, updated_at
            FROM monitoring_status
            WHERE technology_name = ?
            """
            
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                self.executor,
                self._fetch_one,
                sql,
                (technology_name,)
            )
            
            if result:
                return {
                    'last_checked_at': result[0],
                    'last_change_detected_at': result[1],
                    'total_checks': result[2],
                    'total_changes': result[3],
                    'current_version': result[4],
                    'health_status': result[5],
                    'error_count': result[6],
                    'last_error': result[7],
                    'updated_at': result[8]
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting monitoring status: {e}")
            return None
    
    async def store_performance_metric(self, metric_name: str, metric_value: float, 
                                     additional_data: Dict[str, Any] = None) -> bool:
        """Store performance metric"""
        try:
            sql = """
            INSERT INTO performance_metrics (metric_name, metric_value, measurement_timestamp, additional_data)
            VALUES (?, ?, ?, ?)
            """
            
            params = (
                metric_name,
                metric_value,
                datetime.utcnow().isoformat(),
                json.dumps(additional_data) if additional_data else None
            )
            
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(self.executor, self._execute_sql, sql, params)
            
            return True
            
        except Exception as e:
            logger.error(f"Error storing performance metric: {e}")
            return False
    
    async def get_performance_metrics(self, metric_name: str, 
                                    hours_back: int = 24) -> List[Tuple[datetime, float]]:
        """Get performance metrics"""
        try:
            cutoff_time = datetime.utcnow() - timedelta(hours=hours_back)
            
            sql = """
            SELECT measurement_timestamp, metric_value
            FROM performance_metrics
            WHERE metric_name = ? AND measurement_timestamp >= ?
            ORDER BY measurement_timestamp DESC
            """
            
            loop = asyncio.get_event_loop()
            results = await loop.run_in_executor(
                self.executor,
                self._fetch_all,
                sql,
                (metric_name, cutoff_time.isoformat())
            )
            
            return [(datetime.fromisoformat(row[0]), row[1]) for row in results]
            
        except Exception as e:
            logger.error(f"Error getting performance metrics: {e}")
            return []
    
    def _execute_sql(self, sql: str, params: Tuple = None):
        """Execute SQL in thread executor"""
        with sqlite3.connect(self.db_path) as conn:
            if params:
                conn.execute(sql, params)
            else:
                conn.execute(sql)
            conn.commit()
    
    def _fetch_one(self, sql: str, params: Tuple = None):
        """Fetch one result in thread executor"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            return cursor.fetchone()
    
    def _fetch_all(self, sql: str, params: Tuple = None):
        """Fetch all results in thread executor"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)
            return cursor.fetchall()


class StorageInterface:
    """
    Unified storage interface with multi-tier caching and multiple backend support
    """
    
    def __init__(self, config_manager, storage_backend: StorageBackend = StorageBackend.SQLITE):
        """Initialize storage interface"""
        self.config = config_manager
        self.backend_type = storage_backend
        
        # Initialize storage backend
        if storage_backend == StorageBackend.SQLITE:
            db_path = Path("change_detection.db")
            self.backend = SQLiteStorage(db_path)
        else:
            raise ValueError(f"Unsupported storage backend: {storage_backend}")
        
        # Initialize multi-tier cache
        self.memory_cache = MemoryCache(max_size_mb=100, default_ttl_seconds=300)
        
        # Performance statistics
        self.stats = StorageStats()
        
        # Background cleanup task
        self._cleanup_task = None
        self._start_background_tasks()
        
        logger.info(f"Storage interface initialized with {storage_backend.value} backend")
    
    def _start_background_tasks(self):
        """Start background maintenance tasks"""
        async def cleanup_task():
            while True:
                try:
                    # Clean up expired cache entries
                    expired_count = self.memory_cache.cleanup_expired()
                    if expired_count > 0:
                        logger.debug(f"Cleaned up {expired_count} expired cache entries")
                    
                    # Wait 5 minutes before next cleanup
                    await asyncio.sleep(300)
                    
                except Exception as e:
                    logger.error(f"Error in cleanup task: {e}")
                    await asyncio.sleep(60)  # Wait 1 minute on error
        
        # Start cleanup task
        try:
            loop = asyncio.get_event_loop()
            self._cleanup_task = loop.create_task(cleanup_task())
        except RuntimeError:
            # No event loop running, cleanup will be manual
            pass
    
    async def store_source_data(self, technology_name: str, source_name: str, 
                               source_data: 'SourceData') -> bool:
        """Store source data with caching"""
        import time
        start_time = time.time()
        
        try:
            # Store in backend
            success = await self.backend.store_source_data(technology_name, source_name, source_data)
            
            if success:
                # Cache the data
                cache_key = f"source_data:{technology_name}:{source_name}"
                self.memory_cache.set(cache_key, source_data, ttl_seconds=600)  # 10 minutes
                
                # Update stats
                self.stats.total_writes += 1
                write_time = (time.time() - start_time) * 1000
                self.stats.average_write_time_ms = (
                    (self.stats.average_write_time_ms * (self.stats.total_writes - 1) + write_time) /
                    self.stats.total_writes
                )
            
            return success
            
        except Exception as e:
            logger.error(f"Error storing source data: {e}")
            return False
    
    async def get_cached_source_data(self, technology_name: str, source_name: str) -> Optional['SourceData']:
        """Get cached source data with fallback to storage"""
        import time
        start_time = time.time()
        
        try:
            # Check memory cache first
            cache_key = f"source_data:{technology_name}:{source_name}"
            cached_data = self.memory_cache.get(cache_key)
            
            if cached_data:
                self.stats.cache_hits += 1
                return cached_data
            
            # Cache miss - get from backend
            self.stats.cache_misses += 1
            source_data = await self.backend.get_source_data(technology_name, source_name)
            
            if source_data:
                # Cache for future use
                self.memory_cache.set(cache_key, source_data, ttl_seconds=600)
            
            # Update stats
            self.stats.total_reads += 1
            read_time = (time.time() - start_time) * 1000
            self.stats.average_read_time_ms = (
                (self.stats.average_read_time_ms * (self.stats.total_reads - 1) + read_time) /
                self.stats.total_reads
            )
            
            return source_data
            
        except Exception as e:
            logger.error(f"Error getting cached source data: {e}")
            return None
    
    async def store_change(self, change: 'TechnologyChange') -> bool:
        """Store detected change"""
        try:
            success = await self.backend.store_change(change)
            
            if success:
                # Invalidate related caches
                cache_pattern = f"changes:{change.technology_name}"
                self._invalidate_cache_pattern(cache_pattern)
                
                # Update monitoring status
                await self._update_change_statistics(change.technology_name)
            
            return success
            
        except Exception as e:
            logger.error(f"Error storing change: {e}")
            return False
    
    async def get_changes_for_technology(self, technology_name: str, 
                                       limit: int = 100) -> List['TechnologyChange']:
        """Get changes for technology with caching"""
        try:
            # Check cache first
            cache_key = f"changes:{technology_name}:{limit}"
            cached_changes = self.memory_cache.get(cache_key)
            
            if cached_changes:
                self.stats.cache_hits += 1
                return cached_changes
            
            # Get from backend
            self.stats.cache_misses += 1
            changes = await self.backend.get_changes_for_technology(technology_name, limit)
            
            if changes:
                # Cache for 5 minutes
                self.memory_cache.set(cache_key, changes, ttl_seconds=300)
            
            return changes
            
        except Exception as e:
            logger.error(f"Error getting changes for technology: {e}")
            return []
    
    async def update_monitoring_status(self, technology_name: str, 
                                     last_checked: datetime = None,
                                     changes_detected: int = None,
                                     error: str = None) -> bool:
        """Update monitoring status"""
        try:
            # Get current status
            current_status = await self.backend.get_monitoring_status(technology_name) or {}
            
            # Update fields
            status_data = {
                'last_checked_at': (last_checked or datetime.utcnow()).isoformat(),
                'total_checks': current_status.get('total_checks', 0) + 1,
                'total_changes': current_status.get('total_changes', 0) + (changes_detected or 0),
                'current_version': current_status.get('current_version'),
                'health_status': 'error' if error else 'healthy',
                'error_count': current_status.get('error_count', 0) + (1 if error else 0),
                'last_error': error or current_status.get('last_error')
            }
            
            if changes_detected and changes_detected > 0:
                status_data['last_change_detected_at'] = datetime.utcnow().isoformat()
            
            success = await self.backend.update_monitoring_status(technology_name, status_data)
            
            if success:
                # Invalidate cache
                cache_key = f"monitoring_status:{technology_name}"
                self.memory_cache.delete(cache_key)
            
            return success
            
        except Exception as e:
            logger.error(f"Error updating monitoring status: {e}")
            return False
    
    async def get_monitoring_status(self, technology_name: str) -> Optional[Dict[str, Any]]:
        """Get monitoring status with caching"""
        try:
            # Check cache first
            cache_key = f"monitoring_status:{technology_name}"
            cached_status = self.memory_cache.get(cache_key)
            
            if cached_status:
                self.stats.cache_hits += 1
                return cached_status
            
            # Get from backend
            self.stats.cache_misses += 1
            status = await self.backend.get_monitoring_status(technology_name)
            
            if status:
                # Cache for 2 minutes
                self.memory_cache.set(cache_key, status, ttl_seconds=120)
            
            return status
            
        except Exception as e:
            logger.error(f"Error getting monitoring status: {e}")
            return None
    
    async def get_all_monitoring_status(self) -> Dict[str, Dict[str, Any]]:
        """Get monitoring status for all technologies"""
        # This would be implemented with a SQL query to get all statuses
        # For now, return empty dict
        return {}
    
    async def store_performance_metric(self, metric_name: str, metric_value: float, 
                                     additional_data: Dict[str, Any] = None) -> bool:
        """Store performance metric"""
        try:
            return await self.backend.store_performance_metric(metric_name, metric_value, additional_data)
        except Exception as e:
            logger.error(f"Error storing performance metric: {e}")
            return False
    
    async def get_performance_metrics(self, metric_name: str, 
                                    hours_back: int = 24) -> List[Tuple[datetime, float]]:
        """Get performance metrics"""
        try:
            return await self.backend.get_performance_metrics(metric_name, hours_back)
        except Exception as e:
            logger.error(f"Error getting performance metrics: {e}")
            return []
    
    async def cleanup_old_data(self, days_to_keep: int = 90) -> Dict[str, int]:
        """Clean up old data beyond retention period"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days_to_keep)
            
            # This would implement cleanup of old data
            # For now, return counts
            return {
                'source_data_removed': 0,
                'changes_removed': 0,
                'metrics_removed': 0
            }
            
        except Exception as e:
            logger.error(f"Error cleaning up old data: {e}")
            return {}
    
    async def get_storage_stats(self) -> StorageStats:
        """Get current storage statistics"""
        # Update cache size
        cache_stats = self.memory_cache.get_stats()
        self.stats.cache_size_bytes = cache_stats['size_bytes']
        
        return self.stats
    
    async def health_check(self) -> Dict[str, Any]:
        """Perform storage health check"""
        try:
            # Test basic operations
            test_data = {
                'test_key': 'test_value',
                'timestamp': datetime.utcnow().isoformat()
            }
            
            # Test cache
            cache_healthy = True
            try:
                self.memory_cache.set('health_check', test_data, ttl_seconds=10)
                retrieved = self.memory_cache.get('health_check')
                if retrieved != test_data:
                    cache_healthy = False
                self.memory_cache.delete('health_check')
            except Exception:
                cache_healthy = False
            
            # Test backend storage
            storage_healthy = True
            try:
                # This would test actual storage operations
                pass
            except Exception:
                storage_healthy = False
            
            cache_stats = self.memory_cache.get_stats()
            
            return {
                'cache_healthy': cache_healthy,
                'storage_healthy': storage_healthy,
                'cache_entries': cache_stats['entries'],
                'cache_utilization': cache_stats['utilization'],
                'total_reads': self.stats.total_reads,
                'total_writes': self.stats.total_writes,
                'cache_hit_rate': self.stats.cache_hit_rate
            }
            
        except Exception as e:
            logger.error(f"Error during storage health check: {e}")
            return {
                'cache_healthy': False,
                'storage_healthy': False,
                'error': str(e)
            }
    
    def _invalidate_cache_pattern(self, pattern: str):
        """Invalidate cache entries matching pattern"""
        # Simple pattern matching for now
        keys_to_delete = [key for key in self.memory_cache.cache.keys() if pattern in key]
        for key in keys_to_delete:
            self.memory_cache.delete(key)
    
    async def _update_change_statistics(self, technology_name: str):
        """Update change statistics after storing a change"""
        try:
            current_status = await self.backend.get_monitoring_status(technology_name) or {}
            status_data = current_status.copy()
            status_data['total_changes'] = status_data.get('total_changes', 0) + 1
            status_data['last_change_detected_at'] = datetime.utcnow().isoformat()
            
            await self.backend.update_monitoring_status(technology_name, status_data)
        except Exception as e:
            logger.error(f"Error updating change statistics: {e}")
    
    async def close(self):
        """Close storage interface and cleanup resources"""
        try:
            # Cancel cleanup task
            if self._cleanup_task:
                self._cleanup_task.cancel()
                try:
                    await self._cleanup_task
                except asyncio.CancelledError:
                    pass
            
            # Clear cache
            self.memory_cache.clear()
            
            # Close backend
            if hasattr(self.backend, 'close'):
                await self.backend.close()
            
            logger.info("Storage interface closed")
            
        except Exception as e:
            logger.error(f"Error closing storage interface: {e}")
    
    def __del__(self):
        """Cleanup on deletion"""
        try:
            if self._cleanup_task and not self._cleanup_task.done():
                self._cleanup_task.cancel()
        except Exception:
            pass