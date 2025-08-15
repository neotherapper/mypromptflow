#!/usr/bin/env python3
"""
Tests for the working RSS monitoring system
"""

import pytest
import asyncio
import sqlite3
from datetime import datetime
from pathlib import Path
import sys
import tempfile

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sources.rss_monitor import RSSSourceMonitor
from core import SourceMetadata, SourceType, ContentItem
from storage.database import StorageManager
from core.content_prioritizer import UniversalContentPrioritizer

@pytest.fixture
def temp_db():
    """Create temporary database for testing"""
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.close()
    return temp_file.name

@pytest.fixture
def source_metadata():
    """Create test RSS source metadata"""
    return SourceMetadata(
        source_id="test_rss",
        source_name="Test RSS Feed",
        source_type=SourceType.RSS,
        source_url="https://overreacted.io/rss.xml",  # Known working feed
        authority_score=0.9,
        update_frequency="hourly",
        topics=["react", "javascript"]
    )

@pytest.fixture
def storage_manager(temp_db):
    """Create storage manager with temp database"""
    return StorageManager(db_path=temp_db)

@pytest.fixture
def prioritizer():
    """Create content prioritizer"""
    return UniversalContentPrioritizer()

@pytest.mark.asyncio
async def test_rss_monitor_initialization(source_metadata):
    """Test RSS monitor initialization"""
    monitor = RSSSourceMonitor(source_metadata)
    assert monitor.metadata == source_metadata
    assert monitor.metadata.source_url == "https://overreacted.io/rss.xml"

@pytest.mark.asyncio
async def test_rss_feed_fetching(source_metadata):
    """Test RSS feed fetching from real feed"""
    monitor = RSSSourceMonitor(source_metadata)
    result = await monitor.monitor()
    
    # Should successfully fetch from Dan Abramov's blog
    assert result.success == True
    assert len(result.new_items) > 0
    
    # Check item structure
    first_item = result.new_items[0]
    assert isinstance(first_item, ContentItem)
    assert first_item.title is not None
    assert first_item.url is not None
    assert first_item.source_id == "test_rss"

@pytest.mark.asyncio 
async def test_content_prioritizer():
    """Test content prioritization"""
    prioritizer = UniversalContentPrioritizer()
    
    # Create test content item
    item = ContentItem(
        item_id="test123",
        source_id="test_source",
        title="React 19 New Features and Performance Improvements",
        content="React 19 introduces new hooks and server components for better performance",
        url="https://example.com/react19",
        published_date=datetime.now(),
        author="React Team",
        topics=["react", "performance"],
        metadata={"source": "test"}
    )
    
    result = prioritizer.prioritize(item, strategy="default")
    
    # Should have high priority due to React keywords
    assert result.total_score > 0.5
    assert result.priority_level.value in ["high", "medium", "critical"]
    
    # Check individual scores
    assert "keyword_score" in result.component_scores
    assert "topic_score" in result.component_scores

@pytest.mark.asyncio
async def test_database_storage(temp_db):
    """Test database storage operations"""
    storage = StorageManager(db_path=temp_db)
    prioritizer = UniversalContentPrioritizer()
    
    # Create test content
    item = ContentItem(
        item_id="storage_test",
        source_id="test_source", 
        title="Test Article for Storage",
        content="This is test content for database storage testing",
        url="https://example.com/storage-test",
        published_date=datetime.now(),
        author="Test Author",
        topics=["test"],
        metadata={"source": "test"}
    )
    
    # Calculate priority
    priority_result = prioritizer.prioritize(item)
    
    # Store in database
    stored = await storage.store_content(
        item=item,
        priority_score=priority_result.total_score,
        priority_level=priority_result.priority_level.value
    )
    
    assert stored == True
    
    # Verify storage by querying database
    with sqlite3.connect(temp_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM content_items WHERE item_id = ?", ("storage_test",))
        count = cursor.fetchone()[0]
        assert count == 1
        
        # Get the stored item
        cursor.execute("SELECT title, content, priority_level FROM content_items WHERE item_id = ?", ("storage_test",))
        row = cursor.fetchone()
        assert row[0] == "Test Article for Storage"
        assert row[1] == "This is test content for database storage testing"
        assert row[2] in ["low", "medium", "high", "critical"]

@pytest.mark.asyncio
async def test_duplicate_prevention(temp_db):
    """Test that duplicate items are not stored"""
    storage = StorageManager(db_path=temp_db)
    prioritizer = UniversalContentPrioritizer()
    
    item = ContentItem(
        item_id="duplicate_test",
        source_id="test_source",
        title="Duplicate Test Article", 
        content="This should not be stored twice",
        url="https://example.com/duplicate",
        published_date=datetime.now(),
        author="Test Author",
        topics=["test"],
        metadata={"source": "test"}
    )
    
    priority_result = prioritizer.prioritize(item)
    
    # Store first time
    stored1 = await storage.store_content(
        item=item,
        priority_score=priority_result.total_score,
        priority_level=priority_result.priority_level.value
    )
    assert stored1 == True
    
    # Try to store same item again  
    stored2 = await storage.store_content(
        item=item,
        priority_score=priority_result.total_score,
        priority_level=priority_result.priority_level.value
    )
    assert stored2 == False  # Should not store duplicate
    
    # Verify only one item in database
    with sqlite3.connect(temp_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM content_items WHERE item_id = ?", ("duplicate_test",))
        count = cursor.fetchone()[0]
        assert count == 1

def test_priority_scoring_keywords():
    """Test keyword-based priority scoring"""
    prioritizer = UniversalContentPrioritizer()
    
    # High priority keywords
    high_priority_item = ContentItem(
        item_id="high_test",
        source_id="test",
        title="Claude AI Breakthrough Announcement",
        content="Major breakthrough in Claude AI capabilities announced",
        url="https://example.com/claude",
        published_date=datetime.now(),
        author="AI News",
        topics=["ai", "claude"],
        metadata={"source": "test"}
    )
    
    # Low priority keywords
    low_priority_item = ContentItem(
        item_id="low_test", 
        source_id="test",
        title="Random Blog Post About Cats",
        content="Just some random content about cats and dogs",
        url="https://example.com/cats",
        published_date=datetime.now(),
        author="Pet Blogger",
        topics=["pets"],
        metadata={"source": "test"}
    )
    
    high_result = prioritizer.prioritize(high_priority_item)
    low_result = prioritizer.prioritize(low_priority_item)
    
    # High priority item should score higher
    assert high_result.total_score > low_result.total_score
    assert high_result.component_scores["keyword_score"] > low_result.component_scores["keyword_score"]

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])