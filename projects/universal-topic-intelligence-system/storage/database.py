#!/usr/bin/env python3
"""
Database Storage Layer for Universal Topic Intelligence System
Provides persistence for collected items, sources, and metrics
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path
import logging
from contextlib import contextmanager

from core import ContentItem, SourceMetadata, SourceType


class StorageManager:
    """Manages persistent storage for the intelligence system"""
    
    def __init__(self, db_path: str = "topic_intelligence.db"):
        """
        Initialize storage manager
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.logger = logging.getLogger("StorageManager")
        self._initialize_database()
    
    def _initialize_database(self):
        """Create database tables if they don't exist"""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            # Sources table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS sources (
                    source_id TEXT PRIMARY KEY,
                    source_name TEXT NOT NULL,
                    source_type TEXT NOT NULL,
                    source_url TEXT,
                    authority_score REAL DEFAULT 0.5,
                    update_frequency TEXT DEFAULT 'daily',
                    topics TEXT,  -- JSON array
                    metadata TEXT,  -- JSON object
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Content items table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS content_items (
                    item_id TEXT PRIMARY KEY,
                    source_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    content TEXT,
                    url TEXT,
                    published_date TIMESTAMP,
                    collected_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    author TEXT,
                    topics TEXT,  -- JSON array
                    priority_score REAL,
                    priority_level TEXT,
                    metadata TEXT,  -- JSON object
                    FOREIGN KEY (source_id) REFERENCES sources(source_id)
                )
            """)
            
            # Create index for faster lookups
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_items_published 
                ON content_items(published_date DESC)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_items_source 
                ON content_items(source_id)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_items_priority 
                ON content_items(priority_level, priority_score DESC)
            """)
            
            # Topics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS topics (
                    topic_slug TEXT PRIMARY KEY,
                    topic_name TEXT NOT NULL,
                    priority_level TEXT DEFAULT 'medium',
                    monitoring_frequency TEXT DEFAULT 'hourly',
                    last_monitored TIMESTAMP,
                    items_collected INTEGER DEFAULT 0,
                    critical_items INTEGER DEFAULT 0,
                    error_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Metrics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    metric_type TEXT NOT NULL,
                    metric_name TEXT NOT NULL,
                    metric_value REAL,
                    topic_slug TEXT,
                    source_id TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT  -- JSON object
                )
            """)
            
            # Cross-topic relationships table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS topic_relationships (
                    topic1 TEXT NOT NULL,
                    topic2 TEXT NOT NULL,
                    relationship_type TEXT NOT NULL,
                    strength REAL DEFAULT 0.5,
                    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (topic1, topic2)
                )
            """)
            
            conn.commit()
            self.logger.info(f"Database initialized at {self.db_path}")
    
    @contextmanager
    def _get_connection(self):
        """Get database connection with proper cleanup"""
        conn = sqlite3.connect(self.db_path, timeout=30)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def save_content_item(self, item: ContentItem, priority_score: float = 0.5, 
                         priority_level: str = "medium") -> bool:
        """
        Save a content item to the database
        
        Args:
            item: ContentItem to save
            priority_score: Priority score from prioritizer
            priority_level: Priority level (critical/high/medium/low)
            
        Returns:
            True if saved successfully
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Check if item already exists
                cursor.execute(
                    "SELECT item_id FROM content_items WHERE item_id = ?",
                    (item.item_id,)
                )
                
                if cursor.fetchone():
                    self.logger.debug(f"Item {item.item_id} already exists, skipping")
                    return False
                
                # Insert new item
                cursor.execute("""
                    INSERT INTO content_items (
                        item_id, source_id, title, content, url,
                        published_date, author, topics, priority_score,
                        priority_level, metadata
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    item.item_id,
                    item.source_id,
                    item.title,
                    item.content,
                    item.url,
                    item.published_date.isoformat() if item.published_date else None,
                    item.author,
                    json.dumps(item.topics),
                    priority_score,
                    priority_level,
                    json.dumps(item.metadata)
                ))
                
                conn.commit()
                self.logger.debug(f"Saved item: {item.title[:50]}...")
                return True
                
        except Exception as e:
            self.logger.error(f"Error saving content item: {str(e)}")
            return False
    
    def save_content_items_batch(self, items: List[tuple]) -> int:
        """
        Save multiple content items in a batch
        
        Args:
            items: List of (ContentItem, priority_score, priority_level) tuples
            
        Returns:
            Number of items saved
        """
        saved_count = 0
        
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                for item, score, level in items:
                    # Check if exists
                    cursor.execute(
                        "SELECT item_id FROM content_items WHERE item_id = ?",
                        (item.item_id,)
                    )
                    
                    if not cursor.fetchone():
                        cursor.execute("""
                            INSERT INTO content_items (
                                item_id, source_id, title, content, url,
                                published_date, author, topics, priority_score,
                                priority_level, metadata
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            item.item_id,
                            item.source_id,
                            item.title,
                            item.content,
                            item.url,
                            item.published_date.isoformat() if item.published_date else None,
                            item.author,
                            json.dumps(item.topics),
                            score,
                            level,
                            json.dumps(item.metadata)
                        ))
                        saved_count += 1
                
                conn.commit()
                self.logger.info(f"Saved {saved_count} new items to database")
                
        except Exception as e:
            self.logger.error(f"Error in batch save: {str(e)}")
        
        return saved_count
    
    def get_recent_items(self, 
                        topic: Optional[str] = None,
                        limit: int = 50,
                        min_priority: Optional[str] = None) -> List[Dict]:
        """
        Get recent content items
        
        Args:
            topic: Filter by topic (searches in topics JSON)
            limit: Maximum number of items
            min_priority: Minimum priority level
            
        Returns:
            List of item dictionaries
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                query = """
                    SELECT * FROM content_items 
                    WHERE 1=1
                """
                params = []
                
                if topic:
                    query += " AND topics LIKE ?"
                    params.append(f'%"{topic}"%')
                
                if min_priority:
                    priority_order = {
                        'critical': 0,
                        'high': 1,
                        'medium': 2,
                        'low': 3
                    }
                    min_order = priority_order.get(min_priority, 3)
                    
                    # Build priority filter
                    valid_priorities = [p for p, o in priority_order.items() if o <= min_order]
                    if valid_priorities:
                        placeholders = ','.join(['?' for _ in valid_priorities])
                        query += f" AND priority_level IN ({placeholders})"
                        params.extend(valid_priorities)
                
                query += " ORDER BY published_date DESC LIMIT ?"
                params.append(limit)
                
                cursor.execute(query, params)
                
                items = []
                for row in cursor.fetchall():
                    item = dict(row)
                    # Parse JSON fields
                    item['topics'] = json.loads(item['topics']) if item['topics'] else []
                    item['metadata'] = json.loads(item['metadata']) if item['metadata'] else {}
                    items.append(item)
                
                return items
                
        except Exception as e:
            self.logger.error(f"Error getting recent items: {str(e)}")
            return []
    
    def update_topic_stats(self, topic_slug: str, items_collected: int = 0, 
                          critical_items: int = 0, error_increment: int = 0):
        """
        Update topic statistics
        
        Args:
            topic_slug: Topic identifier
            items_collected: Number of new items collected
            critical_items: Number of critical items
            error_increment: Increment error count by this amount
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Update or insert topic stats
                cursor.execute("""
                    INSERT INTO topics (
                        topic_slug, topic_name, items_collected, 
                        critical_items, error_count, last_monitored
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    ON CONFLICT(topic_slug) DO UPDATE SET
                        items_collected = items_collected + ?,
                        critical_items = critical_items + ?,
                        error_count = error_count + ?,
                        last_monitored = ?,
                        updated_at = CURRENT_TIMESTAMP
                """, (
                    topic_slug, topic_slug, items_collected, critical_items, 
                    error_increment, datetime.now().isoformat(),
                    items_collected, critical_items, error_increment,
                    datetime.now().isoformat()
                ))
                
                conn.commit()
                
        except Exception as e:
            self.logger.error(f"Error updating topic stats: {str(e)}")
    
    def save_metric(self, metric_type: str, metric_name: str, 
                   metric_value: float, **kwargs):
        """
        Save a metric data point
        
        Args:
            metric_type: Type of metric (performance, quality, etc.)
            metric_name: Name of the metric
            metric_value: Numeric value
            **kwargs: Additional metadata
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO metrics (
                        metric_type, metric_name, metric_value,
                        topic_slug, source_id, metadata
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    metric_type,
                    metric_name,
                    metric_value,
                    kwargs.get('topic_slug'),
                    kwargs.get('source_id'),
                    json.dumps(kwargs.get('metadata', {}))
                ))
                
                conn.commit()
                
        except Exception as e:
            self.logger.error(f"Error saving metric: {str(e)}")
    
    def get_item_count(self, since: Optional[datetime] = None) -> int:
        """
        Get total count of items in database
        
        Args:
            since: Count items collected after this date
            
        Returns:
            Number of items
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                if since:
                    cursor.execute(
                        "SELECT COUNT(*) as count FROM content_items WHERE collected_date > ?",
                        (since.isoformat(),)
                    )
                else:
                    cursor.execute("SELECT COUNT(*) as count FROM content_items")
                
                result = cursor.fetchone()
                return result['count'] if result else 0
                
        except Exception as e:
            self.logger.error(f"Error getting item count: {str(e)}")
            return 0
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get overall system statistics
        
        Returns:
            Dictionary of statistics
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                stats = {}
                
                # Total items
                cursor.execute("SELECT COUNT(*) as count FROM content_items")
                stats['total_items'] = cursor.fetchone()['count']
                
                # Items by priority
                cursor.execute("""
                    SELECT priority_level, COUNT(*) as count 
                    FROM content_items 
                    GROUP BY priority_level
                """)
                stats['items_by_priority'] = {
                    row['priority_level']: row['count'] 
                    for row in cursor.fetchall()
                }
                
                # Topics monitored
                cursor.execute("SELECT COUNT(*) as count FROM topics")
                stats['topics_monitored'] = cursor.fetchone()['count']
                
                # Recent activity (last 24 hours)
                cursor.execute("""
                    SELECT COUNT(*) as count 
                    FROM content_items 
                    WHERE collected_date > datetime('now', '-24 hours')
                """)
                stats['items_last_24h'] = cursor.fetchone()['count']
                
                # Top topics
                cursor.execute("""
                    SELECT topic_slug, items_collected 
                    FROM topics 
                    ORDER BY items_collected DESC 
                    LIMIT 5
                """)
                stats['top_topics'] = [
                    {'topic': row['topic_slug'], 'items': row['items_collected']}
                    for row in cursor.fetchall()
                ]
                
                return stats
                
        except Exception as e:
            self.logger.error(f"Error getting statistics: {str(e)}")
            return {}