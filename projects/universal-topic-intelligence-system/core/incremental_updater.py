#!/usr/bin/env python3
"""
Incremental Update Manager for Universal Topic Intelligence System
Implements timestamp-based incremental updates to avoid reprocessing old content
"""

import sqlite3
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from pathlib import Path

from core import ContentItem, SourceMetadata


class IncrementalUpdateManager:
    """
    Manages incremental updates for the intelligence system
    Tracks last fetch timestamps and filters content accordingly
    """
    
    def __init__(self, db_path: str = "topic_intelligence.db"):
        """
        Initialize incremental update manager
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.logger = logging.getLogger("IncrementalUpdater")
        self._ensure_schema_updates()
        
    def _ensure_schema_updates(self):
        """Add last_fetched column to sources table if it doesn't exist"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if last_fetched column exists
                cursor.execute("PRAGMA table_info(sources)")
                columns = [row[1] for row in cursor.fetchall()]
                
                if 'last_fetched' not in columns:
                    cursor.execute("""
                        ALTER TABLE sources 
                        ADD COLUMN last_fetched TIMESTAMP
                    """)
                    conn.commit()
                    self.logger.info("Added last_fetched column to sources table")
                    
                # Add index for better performance
                cursor.execute("""
                    CREATE INDEX IF NOT EXISTS idx_sources_last_fetched 
                    ON sources(last_fetched)
                """)
                conn.commit()
                
        except Exception as e:
            self.logger.error(f"Error updating database schema: {e}")
            raise
    
    def get_last_fetch_time(self, source_id: str) -> Optional[datetime]:
        """
        Get the last successful fetch time for a source
        
        Args:
            source_id: ID of the source to check
            
        Returns:
            Last fetch datetime or None if never fetched
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT last_fetched FROM sources WHERE source_id = ?
                """, (source_id,))
                
                result = cursor.fetchone()
                if result and result[0]:
                    return datetime.fromisoformat(result[0])
                return None
                
        except Exception as e:
            self.logger.error(f"Error getting last fetch time for {source_id}: {e}")
            return None
    
    def update_last_fetch_time(self, source_id: str, fetch_time: Optional[datetime] = None):
        """
        Update the last successful fetch time for a source
        
        Args:
            source_id: ID of the source
            fetch_time: Fetch time to record (defaults to now)
        """
        if fetch_time is None:
            fetch_time = datetime.now()
            
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    UPDATE sources 
                    SET last_fetched = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE source_id = ?
                """, (fetch_time.isoformat(), source_id))
                
                conn.commit()
                
                if cursor.rowcount > 0:
                    self.logger.debug(f"Updated last fetch time for {source_id}: {fetch_time}")
                else:
                    self.logger.warning(f"No source found with ID {source_id} for timestamp update")
                    
        except Exception as e:
            self.logger.error(f"Error updating last fetch time for {source_id}: {e}")
            raise
    
    def filter_new_items(self, source_id: str, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter items to only include those newer than the last fetch
        
        Args:
            source_id: ID of the source
            items: List of raw items with 'published' timestamps
            
        Returns:
            Filtered list of new items only
        """
        last_fetch = self.get_last_fetch_time(source_id)
        
        # If no previous fetch, return all items
        if last_fetch is None:
            self.logger.info(f"First fetch for {source_id}, processing all {len(items)} items")
            return items
        
        # Add small buffer (5 minutes) to avoid missing items due to timestamp precision
        cutoff_time = last_fetch - timedelta(minutes=5)
        
        new_items = []
        for item in items:
            published_str = item.get('published', '')
            if not published_str:
                # If no published date, include the item to be safe
                new_items.append(item)
                continue
                
            try:
                # Parse published date
                if isinstance(published_str, datetime):
                    published_date = published_str
                else:
                    # Try parsing various formats
                    published_date = self._parse_date_flexible(published_str)
                
                if published_date and published_date > cutoff_time:
                    new_items.append(item)
                else:
                    self.logger.debug(f"Skipping old item: {item.get('title', 'Unknown')[:50]}...")
                    
            except Exception as e:
                self.logger.warning(f"Error parsing date for item {item.get('title', 'Unknown')}: {e}")
                # Include items with unparseable dates to be safe
                new_items.append(item)
        
        reduction = len(items) - len(new_items)
        if reduction > 0:
            self.logger.info(f"Filtered out {reduction} old items for {source_id}, processing {len(new_items)} new items")
        else:
            self.logger.info(f"All {len(new_items)} items are new for {source_id}")
            
        return new_items
    
    def _parse_date_flexible(self, date_str: str) -> Optional[datetime]:
        """
        Parse date string with multiple format attempts
        
        Args:
            date_str: Date string to parse
            
        Returns:
            Parsed datetime or None if unparseable
        """
        from email.utils import parsedate_to_datetime
        
        formats_to_try = [
            # ISO formats
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%dT%H:%M:%SZ", 
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d",
            
            # RSS/Atom formats
            "%a, %d %b %Y %H:%M:%S %z",
            "%a, %d %b %Y %H:%M:%S GMT",
            "%a, %d %b %Y %H:%M:%S",
        ]
        
        # First try email.utils parser (handles RFC 2822 format)
        try:
            return parsedate_to_datetime(date_str)
        except:
            pass
        
        # Try manual parsing
        for format_str in formats_to_try:
            try:
                return datetime.strptime(date_str, format_str)
            except ValueError:
                continue
        
        # Try to parse just the date part if full datetime fails
        try:
            date_part = date_str.split('T')[0]  # Get date part from ISO format
            return datetime.strptime(date_part, "%Y-%m-%d")
        except:
            pass
            
        return None
    
    def get_sources_needing_update(self, max_age_hours: int = 24) -> List[Dict[str, Any]]:
        """
        Get sources that need updating based on their last fetch time
        
        Args:
            max_age_hours: Maximum age in hours before source needs updating
            
        Returns:
            List of source dictionaries that need updating
        """
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT source_id, source_name, source_url, last_fetched, update_frequency
                    FROM sources 
                    WHERE last_fetched IS NULL OR last_fetched < ?
                    ORDER BY last_fetched ASC NULLS FIRST
                """, (cutoff_time.isoformat(),))
                
                results = cursor.fetchall()
                sources = []
                
                for row in results:
                    sources.append({
                        'source_id': row[0],
                        'source_name': row[1], 
                        'source_url': row[2],
                        'last_fetched': row[3],
                        'update_frequency': row[4]
                    })
                
                self.logger.info(f"Found {len(sources)} sources needing updates (older than {max_age_hours}h)")
                return sources
                
        except Exception as e:
            self.logger.error(f"Error getting sources needing update: {e}")
            return []
    
    def register_source_if_missing(self, metadata: SourceMetadata):
        """
        Register a source in the database if it doesn't exist
        
        Args:
            metadata: Source metadata to register
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if source exists
                cursor.execute("SELECT 1 FROM sources WHERE source_id = ?", (metadata.source_id,))
                if cursor.fetchone():
                    return  # Source already exists
                
                # Insert new source
                cursor.execute("""
                    INSERT INTO sources (
                        source_id, source_name, source_type, source_url,
                        authority_score, update_frequency, topics, metadata
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    metadata.source_id,
                    metadata.source_name,
                    metadata.source_type.value,
                    metadata.source_url,
                    metadata.authority_score,
                    metadata.update_frequency,
                    str(metadata.topics),  # Convert list to string
                    "{}"  # Empty metadata JSON
                ))
                
                conn.commit()
                self.logger.info(f"Registered new source: {metadata.source_name}")
                
        except Exception as e:
            self.logger.error(f"Error registering source {metadata.source_id}: {e}")
    
    def get_incremental_stats(self) -> Dict[str, Any]:
        """
        Get statistics about incremental update performance
        
        Returns:
            Dictionary with update statistics
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get total sources
                cursor.execute("SELECT COUNT(*) FROM sources")
                total_sources = cursor.fetchone()[0]
                
                # Get sources with last_fetched
                cursor.execute("SELECT COUNT(*) FROM sources WHERE last_fetched IS NOT NULL")
                fetched_sources = cursor.fetchone()[0]
                
                # Get sources updated in last 24 hours
                cutoff = datetime.now() - timedelta(hours=24)
                cursor.execute("""
                    SELECT COUNT(*) FROM sources 
                    WHERE last_fetched > ?
                """, (cutoff.isoformat(),))
                recent_updates = cursor.fetchone()[0]
                
                # Get oldest and newest fetch times
                cursor.execute("""
                    SELECT MIN(last_fetched), MAX(last_fetched) 
                    FROM sources WHERE last_fetched IS NOT NULL
                """)
                oldest, newest = cursor.fetchone()
                
                return {
                    'total_sources': total_sources,
                    'sources_ever_fetched': fetched_sources,
                    'sources_updated_24h': recent_updates,
                    'oldest_fetch': oldest,
                    'newest_fetch': newest,
                    'never_fetched': total_sources - fetched_sources
                }
                
        except Exception as e:
            self.logger.error(f"Error getting incremental stats: {e}")
            return {}