#!/usr/bin/env python3
"""
Universal Source Monitor - Base Framework
Abstracted from YouTube monitoring to support any content source
Part of the Universal Topic Intelligence System
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Set, Callable
from datetime import datetime, timedelta
from pathlib import Path
import json
import logging
import asyncio
from enum import Enum

class SourceType(Enum):
    """Types of content sources"""
    RSS = "rss"
    API = "api"
    WEB_SCRAPING = "web_scraping"
    MCP_SERVER = "mcp_server"
    SOCIAL_MEDIA = "social_media"
    DATABASE = "database"
    FILE_SYSTEM = "file_system"

class ContentPriority(Enum):
    """Universal content priority levels"""
    CRITICAL = "critical"  # Immediate attention required
    HIGH = "high"          # Important content
    MEDIUM = "medium"      # Standard processing
    LOW = "low"            # Background processing
    ARCHIVE = "archive"    # Historical reference only

@dataclass
class SourceMetadata:
    """Universal source metadata"""
    source_id: str
    source_name: str
    source_type: SourceType
    source_url: Optional[str]
    authority_score: float  # 0-1 credibility rating
    update_frequency: str    # "realtime", "hourly", "daily", "weekly"
    topics: List[str]
    authentication: Optional[Dict[str, Any]] = None
    rate_limits: Optional[Dict[str, Any]] = None
    custom_config: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ContentItem:
    """Universal content item structure"""
    item_id: str
    source_id: str
    title: str
    content: Optional[str]
    url: Optional[str]
    published_date: datetime
    author: Optional[str]
    topics: List[str]
    metadata: Dict[str, Any]
    raw_data: Optional[Any] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        return {
            "item_id": self.item_id,
            "source_id": self.source_id,
            "title": self.title,
            "content": self.content,
            "url": self.url,
            "published_date": self.published_date.isoformat() if self.published_date else None,
            "author": self.author,
            "topics": self.topics,
            "metadata": self.metadata
        }

@dataclass
class MonitoringResult:
    """Result of a monitoring operation"""
    success: bool
    items_found: int
    new_items: List[ContentItem]
    errors: List[str]
    performance_metrics: Dict[str, float]
    timestamp: datetime = field(default_factory=datetime.now)

class UniversalSourceMonitor(ABC):
    """
    Abstract base class for all source monitors
    Provides common functionality and enforces interface
    """
    
    def __init__(self, source_metadata: SourceMetadata, config: Optional[Dict] = None):
        """
        Initialize universal source monitor
        
        Args:
            source_metadata: Metadata about the source
            config: Optional configuration overrides
        """
        self.source_metadata = source_metadata
        self.config = config or {}
        self.logger = self._setup_logging()
        self.cache = {}
        self.last_check = None
        self.error_count = 0
        self.success_count = 0
        
        # Performance tracking
        self.metrics = {
            "total_fetches": 0,
            "total_items": 0,
            "avg_fetch_time": 0.0,
            "error_rate": 0.0
        }
        
    def _setup_logging(self) -> logging.Logger:
        """Setup source-specific logging"""
        logger = logging.getLogger(f"UniversalMonitor.{self.source_metadata.source_id}")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                f'%(asctime)s - {self.source_metadata.source_name} - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    @abstractmethod
    async def fetch_content(self) -> List[Dict[str, Any]]:
        """
        Fetch raw content from the source
        Must be implemented by each source type
        
        Returns:
            List of raw content items
        """
        pass
    
    @abstractmethod
    def parse_content(self, raw_content: Any) -> ContentItem:
        """
        Parse raw content into universal ContentItem format
        Must be implemented by each source type
        
        Args:
            raw_content: Raw content from source
            
        Returns:
            Parsed ContentItem
        """
        pass
    
    async def monitor(self, since: Optional[datetime] = None) -> MonitoringResult:
        """
        Main monitoring method - fetches and processes content
        
        Args:
            since: Only fetch content newer than this timestamp
            
        Returns:
            MonitoringResult with items and metrics
        """
        start_time = datetime.now()
        errors = []
        new_items = []
        
        try:
            # Fetch content
            self.logger.info(f"Starting monitor for {self.source_metadata.source_name}")
            raw_content = await self.fetch_content()
            
            # Parse each item
            for raw_item in raw_content:
                try:
                    content_item = self.parse_content(raw_item)
                    
                    # Filter by date if specified
                    if since and content_item.published_date < since:
                        continue
                    
                    # Check if truly new (not in cache)
                    if not self._is_duplicate(content_item):
                        new_items.append(content_item)
                        self._add_to_cache(content_item)
                        
                except Exception as e:
                    errors.append(f"Parse error: {str(e)}")
                    self.logger.error(f"Failed to parse item: {e}")
            
            # Update metrics
            fetch_time = (datetime.now() - start_time).total_seconds()
            self._update_metrics(True, len(new_items), fetch_time)
            
            self.logger.info(f"Monitor complete: {len(new_items)} new items found")
            
            return MonitoringResult(
                success=True,
                items_found=len(raw_content),
                new_items=new_items,
                errors=errors,
                performance_metrics={
                    "fetch_time": fetch_time,
                    "items_per_second": len(raw_content) / fetch_time if fetch_time > 0 else 0
                }
            )
            
        except Exception as e:
            self.logger.error(f"Monitor failed: {e}")
            self._update_metrics(False, 0, 0)
            
            return MonitoringResult(
                success=False,
                items_found=0,
                new_items=[],
                errors=[str(e)],
                performance_metrics={}
            )
    
    def _is_duplicate(self, item: ContentItem) -> bool:
        """Check if item already exists in cache"""
        return item.item_id in self.cache
    
    def _add_to_cache(self, item: ContentItem):
        """Add item to cache with TTL"""
        self.cache[item.item_id] = {
            "item": item,
            "timestamp": datetime.now()
        }
        
        # Clean old cache entries (older than 24 hours)
        self._clean_cache()
    
    def _clean_cache(self):
        """Remove old cache entries"""
        cutoff = datetime.now() - timedelta(hours=24)
        self.cache = {
            k: v for k, v in self.cache.items()
            if v["timestamp"] > cutoff
        }
    
    def _update_metrics(self, success: bool, items_count: int, fetch_time: float):
        """Update performance metrics"""
        self.metrics["total_fetches"] += 1
        self.metrics["total_items"] += items_count
        
        if success:
            self.success_count += 1
        else:
            self.error_count += 1
        
        # Calculate averages
        if fetch_time > 0:
            current_avg = self.metrics["avg_fetch_time"]
            self.metrics["avg_fetch_time"] = (
                (current_avg * (self.metrics["total_fetches"] - 1) + fetch_time) /
                self.metrics["total_fetches"]
            )
        
        self.metrics["error_rate"] = self.error_count / self.metrics["total_fetches"]
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        return {
            **self.metrics,
            "source_id": self.source_metadata.source_id,
            "success_rate": self.success_count / self.metrics["total_fetches"] if self.metrics["total_fetches"] > 0 else 0
        }
    
    async def validate_source(self) -> bool:
        """
        Validate that the source is accessible and configured correctly
        
        Returns:
            True if source is valid and accessible
        """
        try:
            # Try to fetch minimal content
            await self.fetch_content()
            return True
        except Exception as e:
            self.logger.error(f"Source validation failed: {e}")
            return False
    
    def supports_filtering(self) -> bool:
        """Check if source supports advanced filtering"""
        return False  # Override in subclasses that support it
    
    def supports_real_time(self) -> bool:
        """Check if source supports real-time updates"""
        return self.source_metadata.update_frequency == "realtime"
    
    def get_source_info(self) -> Dict[str, Any]:
        """Get source information and status"""
        return {
            "source_id": self.source_metadata.source_id,
            "source_name": self.source_metadata.source_name,
            "source_type": self.source_metadata.source_type.value,
            "authority_score": self.source_metadata.authority_score,
            "update_frequency": self.source_metadata.update_frequency,
            "topics": self.source_metadata.topics,
            "last_check": self.last_check.isoformat() if self.last_check else None,
            "cache_size": len(self.cache),
            "metrics": self.get_metrics()
        }


class SourceMonitorFactory:
    """Factory for creating appropriate source monitors"""
    
    _monitors: Dict[SourceType, type] = {}
    
    @classmethod
    def register_monitor(cls, source_type: SourceType, monitor_class: type):
        """Register a monitor class for a source type"""
        cls._monitors[source_type] = monitor_class
    
    @classmethod
    def create_monitor(cls, source_metadata: SourceMetadata, config: Optional[Dict] = None) -> UniversalSourceMonitor:
        """Create appropriate monitor for source type"""
        monitor_class = cls._monitors.get(source_metadata.source_type)
        if not monitor_class:
            raise ValueError(f"No monitor registered for source type: {source_metadata.source_type}")
        
        return monitor_class(source_metadata, config)
    
    @classmethod
    def list_supported_types(cls) -> List[SourceType]:
        """List all supported source types"""
        return list(cls._monitors.keys())