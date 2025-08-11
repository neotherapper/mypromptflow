#!/usr/bin/env python3
"""
RSS Source Monitor Implementation
Monitors RSS feeds from news outlets, blogs, and other sources
"""

import aiohttp
import feedparser
import asyncio
from datetime import datetime
from typing import List, Dict, Any, Optional
import hashlib
import logging
from urllib.parse import urlparse

from core import (
    UniversalSourceMonitor,
    SourceMetadata,
    ContentItem,
    SourceType,
    SourceMonitorFactory
)
from core.language_filter import LanguageFilter

class RSSSourceMonitor(UniversalSourceMonitor):
    """
    RSS feed monitor implementation
    Handles RSS/Atom feeds with resilient fetching and parsing
    """
    
    def __init__(self, source_metadata: SourceMetadata, config: Optional[Dict] = None):
        """Initialize RSS monitor with enhanced configuration"""
        super().__init__(source_metadata, config)
        
        # RSS-specific configuration
        self.timeout = config.get("timeout", 30) if config else 30
        self.max_items = config.get("max_items", 50) if config else 50
        self.user_agent = config.get("user_agent", self._default_user_agent()) if config else self._default_user_agent()
        
        # Language filtering configuration
        self.language_filter = LanguageFilter(
            target_languages=config.get("target_languages", ["en"]) if config else ["en"],
            min_confidence=config.get("min_language_confidence", 0.7) if config else 0.7
        )
        self.enable_language_filtering = config.get("enable_language_filtering", True) if config else True
        
        # Validate RSS URL
        if not source_metadata.source_url:
            raise ValueError(f"RSS source {source_metadata.source_id} requires a source_url")
    
    def _default_user_agent(self) -> str:
        """Default user agent for RSS fetching"""
        return "UniversalTopicIntelligence/2.0 (RSS Monitor; +https://github.com/yourusername/universal-topic-intelligence)"
    
    async def fetch_content(self) -> List[Dict[str, Any]]:
        """
        Fetch RSS feed content with error handling and retries
        
        Returns:
            List of raw RSS entries
        """
        if not self.source_metadata.source_url:
            self.logger.error(f"No URL configured for source {self.source_metadata.source_id}")
            return []
        
        headers = {
            'User-Agent': self.user_agent,
            'Accept': 'application/rss+xml, application/atom+xml, application/xml, text/xml, */*'
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.source_metadata.source_url,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=self.timeout)
                ) as response:
                    
                    if response.status != 200:
                        self.logger.warning(
                            f"RSS fetch returned status {response.status} for {self.source_metadata.source_name}"
                        )
                        return []
                    
                    content = await response.text()
                    
                    # Parse RSS/Atom feed
                    feed = feedparser.parse(content)
                    
                    if feed.bozo:
                        self.logger.warning(
                            f"RSS feed parse warning for {self.source_metadata.source_name}: {feed.bozo_exception}"
                        )
                    
                    # Extract entries
                    entries = []
                    for entry in feed.entries[:self.max_items]:
                        entries.append(self._normalize_entry(entry, feed))
                    
                    self.logger.info(
                        f"Fetched {len(entries)} entries from {self.source_metadata.source_name}"
                    )
                    
                    return entries
                    
        except asyncio.TimeoutError:
            self.logger.error(f"Timeout fetching RSS feed: {self.source_metadata.source_name}")
            return []
        except Exception as e:
            self.logger.error(f"Error fetching RSS feed {self.source_metadata.source_name}: {str(e)}")
            return []
    
    def _normalize_entry(self, entry: Any, feed: Any) -> Dict[str, Any]:
        """
        Normalize RSS/Atom entry to common format
        
        Args:
            entry: feedparser entry object
            feed: feedparser feed object
            
        Returns:
            Normalized entry dictionary
        """
        # Extract common fields with fallbacks
        normalized = {
            "id": self._get_entry_id(entry),
            "title": getattr(entry, "title", "Untitled"),
            "link": getattr(entry, "link", ""),
            "description": self._get_description(entry),
            "published": self._get_published_date(entry),
            "author": self._get_author(entry, feed),
            "categories": self._get_categories(entry),
            "source_feed_title": getattr(feed.feed, "title", self.source_metadata.source_name),
            "raw_entry": entry
        }
        
        # Add media/enclosures if present
        if hasattr(entry, "enclosures") and entry.enclosures:
            normalized["media"] = [
                {
                    "url": enc.get("href", enc.get("url", "")),
                    "type": enc.get("type", ""),
                    "length": enc.get("length", 0)
                }
                for enc in entry.enclosures
            ]
        
        return normalized
    
    def _get_entry_id(self, entry: Any) -> str:
        """Generate unique ID for entry"""
        # Try various ID fields
        if hasattr(entry, "id"):
            return entry.id
        elif hasattr(entry, "guid"):
            return entry.guid
        elif hasattr(entry, "link"):
            # Generate ID from link
            return hashlib.md5(entry.link.encode()).hexdigest()
        else:
            # Generate from title and date
            title = getattr(entry, "title", "")
            date = self._get_published_date(entry)
            return hashlib.md5(f"{title}{date}".encode()).hexdigest()
    
    def _get_description(self, entry: Any) -> str:
        """Extract description/content from entry"""
        # Try different content fields
        if hasattr(entry, "summary"):
            return entry.summary
        elif hasattr(entry, "description"):
            return entry.description
        elif hasattr(entry, "content") and entry.content:
            # Some feeds have content as list
            if isinstance(entry.content, list) and len(entry.content) > 0:
                return entry.content[0].get("value", "")
            return str(entry.content)
        return ""
    
    def _get_published_date(self, entry: Any) -> str:
        """Extract published date"""
        # Try various date fields
        date_fields = ["published", "updated", "created", "date"]
        
        for field in date_fields:
            if hasattr(entry, field):
                date_value = getattr(entry, field)
                if date_value:
                    return date_value
        
        # Try parsed date
        if hasattr(entry, "published_parsed") and entry.published_parsed:
            from time import mktime
            timestamp = mktime(entry.published_parsed)
            return datetime.fromtimestamp(timestamp).isoformat()
        
        # Default to now
        return datetime.now().isoformat()
    
    def _get_author(self, entry: Any, feed: Any) -> str:
        """Extract author information"""
        # Try entry author
        if hasattr(entry, "author"):
            return entry.author
        elif hasattr(entry, "author_detail") and entry.author_detail:
            return entry.author_detail.get("name", "")
        elif hasattr(entry, "authors") and entry.authors:
            return ", ".join([a.get("name", "") for a in entry.authors if a.get("name")])
        
        # Fallback to feed author
        if hasattr(feed.feed, "author"):
            return feed.feed.author
        elif hasattr(feed.feed, "author_detail") and feed.feed.author_detail:
            return feed.feed.author_detail.get("name", "")
        
        return ""
    
    def _get_categories(self, entry: Any) -> List[str]:
        """Extract categories/tags"""
        categories = []
        
        if hasattr(entry, "tags") and entry.tags:
            for tag in entry.tags:
                if isinstance(tag, dict) and "term" in tag:
                    categories.append(tag["term"])
                elif isinstance(tag, str):
                    categories.append(tag)
        
        if hasattr(entry, "categories") and entry.categories:
            for cat in entry.categories:
                if isinstance(cat, tuple) and len(cat) > 0:
                    categories.append(cat[0])
                elif isinstance(cat, str):
                    categories.append(cat)
        
        return list(set(categories))  # Remove duplicates
    
    def parse_content(self, raw_content: Dict[str, Any]) -> Optional[ContentItem]:
        """
        Parse RSS entry into ContentItem with language filtering
        
        Args:
            raw_content: Normalized RSS entry
            
        Returns:
            Parsed ContentItem or None if filtered out by language detection
        """
        # Apply language filtering first if enabled
        if self.enable_language_filtering:
            title = raw_content.get("title", "")
            description = raw_content.get("description", "")
            
            should_include, lang_result = self.language_filter.should_include_content(title, description)
            
            if not should_include:
                self.logger.debug(
                    f"Filtering out non-English content: '{title[:50]}...' "
                    f"(detected: {lang_result.language}, confidence: {lang_result.confidence:.2f})"
                )
                return None
        
        # Parse published date
        try:
            if raw_content["published"]:
                # Handle various date formats
                from dateutil import parser
                published_date = parser.parse(raw_content["published"])
            else:
                published_date = datetime.now()
        except:
            published_date = datetime.now()
        
        # Determine topics from categories and content
        topics = self._extract_topics(raw_content)
        
        # Create metadata with language information
        metadata = {
            "source_type": "rss",
            "feed_title": raw_content["source_feed_title"],
            "categories": raw_content.get("categories", []),
            "media": raw_content.get("media", []),
            "raw_entry": raw_content.get("raw_entry", {})
        }
        
        # Add language detection results to metadata
        if self.enable_language_filtering:
            metadata.update({
                "detected_language": lang_result.language,
                "language_confidence": lang_result.confidence,
                "is_english": lang_result.is_english
            })
        
        # Create content item
        return ContentItem(
            item_id=raw_content["id"],
            source_id=self.source_metadata.source_id,
            title=raw_content["title"],
            content=raw_content["description"],
            url=raw_content["link"],
            published_date=published_date,
            author=raw_content["author"],
            topics=topics,
            metadata=metadata
        )
    
    def _extract_topics(self, entry: Dict[str, Any]) -> List[str]:
        """
        Extract topics from entry content and metadata
        
        Args:
            entry: Normalized RSS entry
            
        Returns:
            List of extracted topics
        """
        topics = []
        
        # Start with categories
        topics.extend(entry.get("categories", []))
        
        # Add source topics if no categories
        if not topics:
            topics.extend(self.source_metadata.topics)
        
        # Analyze title and content for topic keywords
        text = f"{entry.get('title', '')} {entry.get('description', '')}".lower()
        
        # Technology topics
        tech_keywords = {
            "ai": ["artificial intelligence", "machine learning", "neural network", "deep learning", "ai", "ml"],
            "programming": ["programming", "coding", "developer", "software", "code", "algorithm"],
            "web": ["web", "frontend", "backend", "javascript", "react", "vue", "angular"],
            "cloud": ["cloud", "aws", "azure", "gcp", "kubernetes", "docker"],
            "security": ["security", "cybersecurity", "hack", "vulnerability", "breach"],
            "data": ["data", "database", "analytics", "bigdata", "sql"],
            "mobile": ["mobile", "ios", "android", "app", "swift", "kotlin"],
            "blockchain": ["blockchain", "crypto", "bitcoin", "ethereum", "web3", "defi"]
        }
        
        for topic, keywords in tech_keywords.items():
            if any(keyword in text for keyword in keywords):
                if topic not in topics:
                    topics.append(topic)
        
        # Clean and deduplicate
        topics = [t.lower().replace(" ", "-") for t in topics]
        topics = list(set(topics))
        
        return topics[:10]  # Limit to 10 topics


# Register RSS monitor with factory
SourceMonitorFactory.register_monitor(SourceType.RSS, RSSSourceMonitor)