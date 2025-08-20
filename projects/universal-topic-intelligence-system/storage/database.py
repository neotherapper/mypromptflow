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
            
            # Enhanced content items table with MCP-specific columns
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
                    
                    -- MCP Source Type
                    mcp_source_type TEXT,  -- youtube_transcript, github_repository, web_search, web_content
                    
                    -- YouTube specific fields
                    youtube_video_id TEXT,
                    youtube_channel TEXT,
                    youtube_duration TEXT,
                    youtube_view_count INTEGER,
                    youtube_like_count INTEGER,
                    youtube_language TEXT,
                    
                    -- GitHub specific fields
                    github_repo_name TEXT,
                    github_stars INTEGER,
                    github_forks INTEGER,
                    github_language TEXT,
                    github_license TEXT,
                    github_open_issues INTEGER,
                    
                    -- Search specific fields
                    search_query TEXT,
                    search_rank INTEGER,
                    search_engine TEXT,
                    search_relevance_score REAL,
                    
                    -- Web content fields
                    web_domain TEXT,
                    web_content_type TEXT,
                    web_content_length INTEGER,
                    
                    -- Generic metadata for extensibility
                    metadata TEXT,  -- JSON object for additional fields
                    
                    FOREIGN KEY (source_id) REFERENCES sources(source_id)
                )
            """)
            
            # Create indexes for faster lookups
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
            
            # Create MCP-specific indexes only if columns exist
            self._create_mcp_indexes_if_possible(cursor)
            
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
    
    def _create_mcp_indexes_if_possible(self, cursor):
        """
        Create MCP-specific indexes only if the columns exist
        This prevents errors when initializing existing databases
        """
        try:
            # Check if MCP columns exist
            cursor.execute("PRAGMA table_info(content_items)")
            columns = [row[1] for row in cursor.fetchall()]
            
            mcp_indexes = [
                ("idx_items_mcp_type", "mcp_source_type"),
                ("idx_items_youtube_channel", "youtube_channel"),
                ("idx_items_github_stars", "github_stars DESC"),
                ("idx_items_search_query", "search_query"),
                ("idx_items_web_domain", "web_domain")
            ]
            
            for index_name, column_spec in mcp_indexes:
                column_name = column_spec.split()[0]  # Extract column name (remove DESC)
                if column_name in columns:
                    cursor.execute(f"""
                        CREATE INDEX IF NOT EXISTS {index_name}
                        ON content_items({column_spec})
                    """)
                    
        except Exception as e:
            self.logger.warning(f"Could not create MCP indexes: {e}")
    
    def save_content_item(self, item: ContentItem, priority_score: float = 0.5, 
                         priority_level: str = "medium") -> bool:
        """
        Save a content item to the database with MCP-specific field extraction
        
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
                
                # Extract MCP-specific fields from metadata
                mcp_fields = self._extract_mcp_fields(item.metadata)
                
                # Insert new item with MCP fields
                cursor.execute("""
                    INSERT INTO content_items (
                        item_id, source_id, title, content, url, published_date, author, topics, 
                        priority_score, priority_level, 
                        mcp_source_type,
                        youtube_video_id, youtube_channel, youtube_duration, youtube_view_count, 
                        youtube_like_count, youtube_language,
                        github_repo_name, github_stars, github_forks, github_language, 
                        github_license, github_open_issues,
                        search_query, search_rank, search_engine, search_relevance_score,
                        web_domain, web_content_type, web_content_length,
                        metadata
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    item.item_id, item.source_id, item.title, item.content, item.url,
                    item.published_date.isoformat() if item.published_date else None,
                    item.author, json.dumps(item.topics), priority_score, priority_level,
                    mcp_fields['mcp_source_type'],
                    mcp_fields['youtube_video_id'], mcp_fields['youtube_channel'], 
                    mcp_fields['youtube_duration'], mcp_fields['youtube_view_count'], 
                    mcp_fields['youtube_like_count'], mcp_fields['youtube_language'],
                    mcp_fields['github_repo_name'], mcp_fields['github_stars'], 
                    mcp_fields['github_forks'], mcp_fields['github_language'], 
                    mcp_fields['github_license'], mcp_fields['github_open_issues'],
                    mcp_fields['search_query'], mcp_fields['search_rank'], 
                    mcp_fields['search_engine'], mcp_fields['search_relevance_score'],
                    mcp_fields['web_domain'], mcp_fields['web_content_type'], 
                    mcp_fields['web_content_length'],
                    json.dumps(item.metadata)
                ))
                
                conn.commit()
                self.logger.debug(f"Saved item: {item.title[:50]}... (MCP type: {mcp_fields['mcp_source_type']})")
                return True
                
        except Exception as e:
            self.logger.error(f"Error saving content item: {str(e)}")
            return False
    
    async def store_content(self, item: ContentItem, priority_score: float = 0.5, 
                           priority_level: str = "medium") -> bool:
        """
        Async wrapper for saving content (compatible with auto_monitor.py)
        
        Args:
            item: ContentItem to save
            priority_score: Priority score from prioritizer
            priority_level: Priority level (critical/high/medium/low)
            
        Returns:
            True if saved successfully
        """
        return self.save_content_item(item, priority_score, priority_level)
    
    def save_content_items_batch(self, items: List[tuple]) -> int:
        """
        Save multiple content items in a batch with MCP field extraction
        
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
                        # Extract MCP-specific fields
                        mcp_fields = self._extract_mcp_fields(item.metadata)
                        
                        cursor.execute("""
                            INSERT INTO content_items (
                                item_id, source_id, title, content, url, published_date, author, topics,
                                priority_score, priority_level,
                                mcp_source_type,
                                youtube_video_id, youtube_channel, youtube_duration, youtube_view_count,
                                youtube_like_count, youtube_language,
                                github_repo_name, github_stars, github_forks, github_language,
                                github_license, github_open_issues,
                                search_query, search_rank, search_engine, search_relevance_score,
                                web_domain, web_content_type, web_content_length,
                                metadata
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            item.item_id, item.source_id, item.title, item.content, item.url,
                            item.published_date.isoformat() if item.published_date else None,
                            item.author, json.dumps(item.topics), score, level,
                            mcp_fields['mcp_source_type'],
                            mcp_fields['youtube_video_id'], mcp_fields['youtube_channel'],
                            mcp_fields['youtube_duration'], mcp_fields['youtube_view_count'],
                            mcp_fields['youtube_like_count'], mcp_fields['youtube_language'],
                            mcp_fields['github_repo_name'], mcp_fields['github_stars'],
                            mcp_fields['github_forks'], mcp_fields['github_language'],
                            mcp_fields['github_license'], mcp_fields['github_open_issues'],
                            mcp_fields['search_query'], mcp_fields['search_rank'],
                            mcp_fields['search_engine'], mcp_fields['search_relevance_score'],
                            mcp_fields['web_domain'], mcp_fields['web_content_type'],
                            mcp_fields['web_content_length'],
                            json.dumps(item.metadata)
                        ))
                        saved_count += 1
                
                conn.commit()
                self.logger.info(f"Saved {saved_count} new items to database")
                
        except Exception as e:
            self.logger.error(f"Error in batch save: {str(e)}")
        
        return saved_count
    
    def _extract_mcp_fields(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract MCP-specific fields from metadata dictionary
        
        Args:
            metadata: Raw metadata dictionary from ContentItem
            
        Returns:
            Dictionary with extracted MCP fields
        """
        # Initialize all fields with None
        mcp_fields = {
            'mcp_source_type': None,
            # YouTube fields
            'youtube_video_id': None,
            'youtube_channel': None,
            'youtube_duration': None,
            'youtube_view_count': None,
            'youtube_like_count': None,
            'youtube_language': None,
            # GitHub fields
            'github_repo_name': None,
            'github_stars': None,
            'github_forks': None,
            'github_language': None,
            'github_license': None,
            'github_open_issues': None,
            # Search fields
            'search_query': None,
            'search_rank': None,
            'search_engine': None,
            'search_relevance_score': None,
            # Web content fields
            'web_domain': None,
            'web_content_type': None,
            'web_content_length': None
        }
        
        if not metadata:
            return mcp_fields
        
        # Extract source type
        mcp_fields['mcp_source_type'] = metadata.get('source_type')
        
        # Extract YouTube fields
        if 'video_id' in metadata:
            mcp_fields['youtube_video_id'] = metadata.get('video_id')
        if 'channel' in metadata:
            mcp_fields['youtube_channel'] = metadata.get('channel')
        if 'duration' in metadata:
            mcp_fields['youtube_duration'] = metadata.get('duration')
        if 'view_count' in metadata:
            mcp_fields['youtube_view_count'] = metadata.get('view_count')
        if 'like_count' in metadata:
            mcp_fields['youtube_like_count'] = metadata.get('like_count')
        if 'language' in metadata:
            mcp_fields['youtube_language'] = metadata.get('language')
        
        # Extract GitHub fields
        if 'repo_name' in metadata:
            mcp_fields['github_repo_name'] = metadata.get('repo_name')
        if 'stars' in metadata:
            mcp_fields['github_stars'] = metadata.get('stars')
        if 'forks' in metadata:
            mcp_fields['github_forks'] = metadata.get('forks')
        if 'language' in metadata and mcp_fields['mcp_source_type'] == 'github_repository':
            mcp_fields['github_language'] = metadata.get('language')
        if 'license' in metadata:
            mcp_fields['github_license'] = metadata.get('license')
        if 'open_issues' in metadata:
            mcp_fields['github_open_issues'] = metadata.get('open_issues')
        
        # Extract search fields
        if 'search_query' in metadata:
            mcp_fields['search_query'] = metadata.get('search_query')
        if 'search_rank' in metadata:
            mcp_fields['search_rank'] = metadata.get('search_rank')
        if 'search_engine' in metadata:
            mcp_fields['search_engine'] = metadata.get('search_engine')
        if 'relevance_score' in metadata:
            mcp_fields['search_relevance_score'] = metadata.get('relevance_score')
        
        # Extract web content fields
        if 'domain' in metadata:
            mcp_fields['web_domain'] = metadata.get('domain')
        if 'content_type' in metadata:
            mcp_fields['web_content_type'] = metadata.get('content_type')
        if 'content_length' in metadata:
            mcp_fields['web_content_length'] = metadata.get('content_length')
        
        return mcp_fields
    
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
                    
                    # Add computed fields for easier access
                    if item.get('mcp_source_type'):
                        item['is_mcp_content'] = True
                        item['source_category'] = self._categorize_mcp_source(item['mcp_source_type'])
                    else:
                        item['is_mcp_content'] = False
                        item['source_category'] = 'rss'
                    
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
    
    def get_mcp_analytics(self) -> Dict[str, Any]:
        """
        Get analytics specific to MCP content types
        
        Returns:
            Dictionary with MCP analytics
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                analytics = {}
                
                # Content by MCP source type
                cursor.execute("""
                    SELECT mcp_source_type, COUNT(*) as count 
                    FROM content_items 
                    WHERE mcp_source_type IS NOT NULL
                    GROUP BY mcp_source_type
                    ORDER BY count DESC
                """)
                analytics['content_by_mcp_type'] = {
                    row['mcp_source_type']: row['count'] 
                    for row in cursor.fetchall()
                }
                
                # Top YouTube channels
                cursor.execute("""
                    SELECT youtube_channel, COUNT(*) as videos, AVG(youtube_view_count) as avg_views
                    FROM content_items 
                    WHERE youtube_channel IS NOT NULL
                    GROUP BY youtube_channel
                    ORDER BY videos DESC
                    LIMIT 10
                """)
                analytics['top_youtube_channels'] = [
                    {
                        'channel': row['youtube_channel'],
                        'videos': row['videos'],
                        'avg_views': int(row['avg_views']) if row['avg_views'] else 0
                    }
                    for row in cursor.fetchall()
                ]
                
                # Top GitHub repositories by stars
                cursor.execute("""
                    SELECT github_repo_name, github_stars, github_forks, github_language
                    FROM content_items 
                    WHERE github_repo_name IS NOT NULL AND github_stars IS NOT NULL
                    ORDER BY github_stars DESC
                    LIMIT 10
                """)
                analytics['top_github_repos'] = [
                    {
                        'repo': row['github_repo_name'],
                        'stars': row['github_stars'],
                        'forks': row['github_forks'],
                        'language': row['github_language']
                    }
                    for row in cursor.fetchall()
                ]
                
                # Programming languages distribution
                cursor.execute("""
                    SELECT github_language, COUNT(*) as count
                    FROM content_items 
                    WHERE github_language IS NOT NULL
                    GROUP BY github_language
                    ORDER BY count DESC
                    LIMIT 10
                """)
                analytics['programming_languages'] = {
                    row['github_language']: row['count']
                    for row in cursor.fetchall()
                }
                
                # Top search queries
                cursor.execute("""
                    SELECT search_query, COUNT(*) as count, AVG(search_relevance_score) as avg_relevance
                    FROM content_items 
                    WHERE search_query IS NOT NULL
                    GROUP BY search_query
                    ORDER BY count DESC
                    LIMIT 10
                """)
                analytics['top_search_queries'] = [
                    {
                        'query': row['search_query'],
                        'count': row['count'],
                        'avg_relevance': round(row['avg_relevance'], 2) if row['avg_relevance'] else 0
                    }
                    for row in cursor.fetchall()
                ]
                
                # Web domains distribution
                cursor.execute("""
                    SELECT web_domain, COUNT(*) as count
                    FROM content_items 
                    WHERE web_domain IS NOT NULL
                    GROUP BY web_domain
                    ORDER BY count DESC
                    LIMIT 10
                """)
                analytics['top_web_domains'] = {
                    row['web_domain']: row['count']
                    for row in cursor.fetchall()
                }
                
                return analytics
                
        except Exception as e:
            self.logger.error(f"Error getting MCP analytics: {str(e)}")
            return {}
    
    def get_content_by_source_type(self, source_type: str, limit: int = 20) -> List[Dict]:
        """
        Get content items filtered by MCP source type
        
        Args:
            source_type: MCP source type to filter by
            limit: Maximum number of items to return
            
        Returns:
            List of content items
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT * FROM content_items 
                    WHERE mcp_source_type = ?
                    ORDER BY published_date DESC
                    LIMIT ?
                """, (source_type, limit))
                
                items = []
                for row in cursor.fetchall():
                    item = dict(row)
                    item['topics'] = json.loads(item['topics']) if item['topics'] else []
                    item['metadata'] = json.loads(item['metadata']) if item['metadata'] else {}
                    items.append(item)
                
                return items
                
        except Exception as e:
            self.logger.error(f"Error getting content by source type: {str(e)}")
            return []
    
    def migrate_database_schema(self) -> bool:
        """
        Migrate existing database to support MCP fields
        This adds the new columns to existing installations
        
        Returns:
            True if migration successful
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Check if migration is needed
                cursor.execute("PRAGMA table_info(content_items)")
                columns = [row[1] for row in cursor.fetchall()]
                
                mcp_columns = [
                    'mcp_source_type', 'youtube_video_id', 'youtube_channel', 'youtube_duration',
                    'youtube_view_count', 'youtube_like_count', 'youtube_language',
                    'github_repo_name', 'github_stars', 'github_forks', 'github_language',
                    'github_license', 'github_open_issues', 'search_query', 'search_rank',
                    'search_engine', 'search_relevance_score', 'web_domain', 'web_content_type',
                    'web_content_length'
                ]
                
                # Add missing columns
                for column in mcp_columns:
                    if column not in columns:
                        if 'count' in column or 'rank' in column or 'length' in column:
                            cursor.execute(f"ALTER TABLE content_items ADD COLUMN {column} INTEGER")
                        elif 'score' in column:
                            cursor.execute(f"ALTER TABLE content_items ADD COLUMN {column} REAL")
                        else:
                            cursor.execute(f"ALTER TABLE content_items ADD COLUMN {column} TEXT")
                        
                        self.logger.info(f"Added column: {column}")
                
                # Create new indexes if they don't exist
                indexes = [
                    "CREATE INDEX IF NOT EXISTS idx_items_mcp_type ON content_items(mcp_source_type)",
                    "CREATE INDEX IF NOT EXISTS idx_items_youtube_channel ON content_items(youtube_channel)",
                    "CREATE INDEX IF NOT EXISTS idx_items_github_stars ON content_items(github_stars DESC)",
                    "CREATE INDEX IF NOT EXISTS idx_items_search_query ON content_items(search_query)",
                    "CREATE INDEX IF NOT EXISTS idx_items_web_domain ON content_items(web_domain)"
                ]
                
                for index_sql in indexes:
                    cursor.execute(index_sql)
                
                # Create indexes after adding columns
                self._create_mcp_indexes_if_possible(cursor)
                
                conn.commit()
                self.logger.info("Database migration completed successfully")
                return True
                
        except Exception as e:
            self.logger.error(f"Error migrating database schema: {str(e)}")
            return False