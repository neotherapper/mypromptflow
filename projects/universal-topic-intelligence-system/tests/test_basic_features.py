#!/usr/bin/env python3
"""
Tests for the basic working features
"""

import pytest
import sqlite3
from datetime import datetime
from pathlib import Path
import sys
import tempfile

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import ContentItem
from storage.database import StorageManager
from core.content_prioritizer import UniversalContentPrioritizer

@pytest.fixture
def temp_db():
    """Create temporary database for testing"""
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.close()
    return temp_file.name

@pytest.fixture
def storage_manager(temp_db):
    """Create storage manager with temp database"""
    return StorageManager(db_path=temp_db)

@pytest.fixture
def prioritizer():
    """Create content prioritizer"""
    return UniversalContentPrioritizer()

@pytest.mark.asyncio
async def test_database_storage_works(temp_db):
    """Test that database storage is working"""
    storage = StorageManager(db_path=temp_db)
    prioritizer = UniversalContentPrioritizer()
    
    # Create test content
    item = ContentItem(
        item_id="test_item",
        source_id="test_source", 
        title="Test Article",
        content="Test content for storage",
        url="https://example.com/test",
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
    
    # Verify storage
    with sqlite3.connect(temp_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM content_items WHERE item_id = ?", ("test_item",))
        count = cursor.fetchone()[0]
        assert count == 1

def test_prioritizer_works():
    """Test that content prioritizer assigns scores"""
    prioritizer = UniversalContentPrioritizer()
    
    # High priority item
    high_priority_item = ContentItem(
        item_id="high_test",
        source_id="test",
        title="React 19 Released - Major Update",
        content="React 19 introduces new features for developers",
        url="https://example.com/react19",
        published_date=datetime.now(),
        author="React Team",
        topics=["react", "development"],
        metadata={}
    )
    
    result = prioritizer.prioritize(high_priority_item)
    
    # Should get a reasonable score
    assert result.total_score > 0.0
    assert result.total_score <= 1.0
    assert result.priority_level.value in ["low", "medium", "high", "critical"]

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])