#!/usr/bin/env python3
"""
Tests for Universal Source Monitor
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import (
    UniversalSourceMonitor,
    SourceType,
    ContentPriority,
    SourceMetadata,
    ContentItem,
    MonitoringResult,
    SourceMonitorFactory
)

class MockSourceMonitor(UniversalSourceMonitor):
    """Mock implementation for testing"""
    
    async def fetch_content(self):
        """Return mock content"""
        return [
            {
                "id": "test1",
                "title": "Test Article 1",
                "content": "This is test content about React and TypeScript",
                "url": "https://example.com/test1",
                "published": datetime.now().isoformat(),
                "author": "Test Author"
            },
            {
                "id": "test2",
                "title": "Breaking: Major AI Announcement",
                "content": "Revolutionary AI breakthrough announced today",
                "url": "https://example.com/test2",
                "published": (datetime.now() - timedelta(hours=2)).isoformat(),
                "author": "AI Reporter"
            }
        ]
    
    def parse_content(self, raw_content):
        """Parse mock content"""
        return ContentItem(
            item_id=raw_content["id"],
            source_id=self.source_metadata.source_id,
            title=raw_content["title"],
            content=raw_content["content"],
            url=raw_content["url"],
            published_date=datetime.fromisoformat(raw_content["published"]),
            author=raw_content["author"],
            topics=["technology", "ai"] if "AI" in raw_content["title"] else ["technology"],
            metadata={"raw": raw_content}
        )

@pytest.fixture
def source_metadata():
    """Create test source metadata"""
    return SourceMetadata(
        source_id="test_source",
        source_name="Test Source",
        source_type=SourceType.API,
        source_url="https://example.com/api",
        authority_score=0.8,
        update_frequency="hourly",
        topics=["technology", "ai", "programming"]
    )

@pytest.fixture
def mock_monitor(source_metadata):
    """Create mock monitor instance"""
    return MockSourceMonitor(source_metadata)

@pytest.mark.asyncio
async def test_monitor_initialization(mock_monitor, source_metadata):
    """Test monitor initialization"""
    assert mock_monitor.source_metadata == source_metadata
    assert mock_monitor.error_count == 0
    assert mock_monitor.success_count == 0
    assert mock_monitor.metrics["total_fetches"] == 0

@pytest.mark.asyncio
async def test_fetch_content(mock_monitor):
    """Test content fetching"""
    content = await mock_monitor.fetch_content()
    assert len(content) == 2
    assert content[0]["title"] == "Test Article 1"
    assert "AI" in content[1]["title"]

@pytest.mark.asyncio
async def test_parse_content(mock_monitor):
    """Test content parsing"""
    raw_content = {
        "id": "test_parse",
        "title": "Test Parse Article",
        "content": "Content for parsing test",
        "url": "https://example.com/parse",
        "published": datetime.now().isoformat(),
        "author": "Parser Test"
    }
    
    parsed = mock_monitor.parse_content(raw_content)
    assert isinstance(parsed, ContentItem)
    assert parsed.item_id == "test_parse"
    assert parsed.title == "Test Parse Article"
    assert parsed.source_id == mock_monitor.source_metadata.source_id

@pytest.mark.asyncio
async def test_monitor_operation(mock_monitor):
    """Test complete monitoring operation"""
    result = await mock_monitor.monitor()
    
    assert isinstance(result, MonitoringResult)
    assert result.success == True
    assert result.items_found == 2
    assert len(result.new_items) == 2
    assert result.performance_metrics["fetch_time"] > 0
    
    # Check metrics were updated
    assert mock_monitor.metrics["total_fetches"] == 1
    assert mock_monitor.metrics["total_items"] == 2
    assert mock_monitor.success_count == 1

@pytest.mark.asyncio
async def test_duplicate_detection(mock_monitor):
    """Test duplicate content detection"""
    # First monitor call
    result1 = await mock_monitor.monitor()
    assert len(result1.new_items) == 2
    
    # Second monitor call - should detect duplicates
    result2 = await mock_monitor.monitor()
    assert len(result2.new_items) == 0  # All items should be duplicates

@pytest.mark.asyncio
async def test_date_filtering(mock_monitor):
    """Test filtering by date"""
    cutoff = datetime.now() - timedelta(hours=1)
    result = await mock_monitor.monitor(since=cutoff)
    
    # Should only get items newer than 1 hour
    assert len(result.new_items) == 1
    assert "Test Article 1" in result.new_items[0].title

def test_source_info(mock_monitor):
    """Test source information retrieval"""
    info = mock_monitor.get_source_info()
    
    assert info["source_id"] == "test_source"
    assert info["source_name"] == "Test Source"
    assert info["source_type"] == "api"
    assert info["authority_score"] == 0.8
    assert "metrics" in info

def test_factory_registration():
    """Test factory pattern"""
    # Register mock monitor
    SourceMonitorFactory.register_monitor(SourceType.API, MockSourceMonitor)
    
    # Check registration
    assert SourceType.API in SourceMonitorFactory.list_supported_types()
    
    # Create monitor via factory
    metadata = SourceMetadata(
        source_id="factory_test",
        source_name="Factory Test",
        source_type=SourceType.API,
        source_url="https://example.com",
        authority_score=0.7,
        update_frequency="daily",
        topics=["test"]
    )
    
    monitor = SourceMonitorFactory.create_monitor(metadata)
    assert isinstance(monitor, MockSourceMonitor)
    assert monitor.source_metadata.source_id == "factory_test"

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])