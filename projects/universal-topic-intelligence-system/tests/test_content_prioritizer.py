#!/usr/bin/env python3
"""
Tests for Content Prioritizer
"""

import pytest
from datetime import datetime, timedelta
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core import (
    UniversalContentPrioritizer,
    ContentItem,
    ContentPriority,
    PriorityFactors,
    PriorityResult,
    DefaultPriorityStrategy,
    NewsPriorityStrategy,
    TechnicalContentStrategy,
    SocialSignalsStrategy
)

@pytest.fixture
def prioritizer():
    """Create prioritizer instance"""
    return UniversalContentPrioritizer()

@pytest.fixture
def sample_content():
    """Create sample content items"""
    return [
        ContentItem(
            item_id="news1",
            source_id="cnn",
            title="Breaking: Major Technology Announcement",
            content="A revolutionary new technology has been announced...",
            url="https://example.com/news1",
            published_date=datetime.now() - timedelta(minutes=30),
            author="Tech Reporter",
            topics=["technology", "breaking"],
            metadata={"engagement_score": 0.9, "views": 50000}
        ),
        ContentItem(
            item_id="tutorial1",
            source_id="dev_blog",
            title="Complete Guide to React Performance Optimization",
            content="In this comprehensive tutorial, we'll explore..." * 100,
            url="https://example.com/tutorial1",
            published_date=datetime.now() - timedelta(days=3),
            author="Dev Expert",
            topics=["react", "performance", "tutorial"],
            metadata={"completeness": 0.95}
        ),
        ContentItem(
            item_id="old1",
            source_id="archive",
            title="Historical Technology Overview",
            content="Looking back at technology from last year...",
            url="https://example.com/old1",
            published_date=datetime.now() - timedelta(days=60),
            author="Historian",
            topics=["history", "technology"],
            metadata={}
        )
    ]

def test_prioritizer_initialization(prioritizer):
    """Test prioritizer initialization"""
    assert prioritizer is not None
    assert "default" in prioritizer.strategies
    assert "news" in prioritizer.strategies
    assert "technical" in prioritizer.strategies
    assert "social" in prioritizer.strategies

def test_default_prioritization(prioritizer, sample_content):
    """Test default prioritization strategy"""
    news_item = sample_content[0]
    result = prioritizer.prioritize(news_item, strategy="default")
    
    assert isinstance(result, PriorityResult)
    assert result.content_item == news_item
    assert 0 <= result.total_score <= 1
    assert isinstance(result.priority_level, ContentPriority)
    assert len(result.reasoning) > 0
    assert isinstance(result.recommendations, list)

def test_news_prioritization(prioritizer, sample_content):
    """Test news-specific prioritization"""
    news_item = sample_content[0]
    result = prioritizer.prioritize(news_item, strategy="news")
    
    # Breaking news should get high priority
    assert result.priority_level in [ContentPriority.CRITICAL, ContentPriority.HIGH]
    assert result.factors.content_recency > 0.8  # Very recent
    assert "breaking" in result.reasoning.lower()

def test_technical_prioritization(prioritizer, sample_content):
    """Test technical content prioritization"""
    tutorial = sample_content[1]
    result = prioritizer.prioritize(tutorial, strategy="technical")
    
    # Comprehensive tutorial should score well
    assert result.factors.completeness > 0.8
    assert result.factors.actionability > 0.7
    assert result.priority_level in [ContentPriority.HIGH, ContentPriority.MEDIUM]

def test_social_signals_prioritization(prioritizer, sample_content):
    """Test social signals prioritization"""
    viral_item = sample_content[0]  # Has high views
    result = prioritizer.prioritize(viral_item, strategy="social")
    
    # High engagement should boost score
    assert result.factors.engagement_signals > 0.7
    assert result.priority_level in [ContentPriority.CRITICAL, ContentPriority.HIGH]

def test_batch_prioritization(prioritizer, sample_content):
    """Test batch prioritization"""
    results = prioritizer.prioritize_batch(sample_content, strategy="default")
    
    assert len(results) == len(sample_content)
    # Results should be sorted by score (highest first)
    scores = [r.total_score for r in results]
    assert scores == sorted(scores, reverse=True)
    
    # Recent breaking news should be first
    assert "Breaking" in results[0].content_item.title

def test_topic_preferences(prioritizer, sample_content):
    """Test topic preference influence"""
    # Set high preference for React
    prioritizer.set_topic_preferences({
        "react": 1.0,
        "technology": 0.5,
        "history": 0.1
    })
    
    tutorial = sample_content[1]  # React tutorial
    result = prioritizer.prioritize(tutorial)
    
    # React preference should boost relevance
    assert result.factors.topic_relevance >= 0.8

def test_source_authorities(prioritizer, sample_content):
    """Test source authority influence"""
    prioritizer.set_source_authorities({
        "cnn": 0.95,
        "dev_blog": 0.7,
        "archive": 0.3
    })
    
    news_item = sample_content[0]
    result = prioritizer.prioritize(news_item)
    
    # CNN authority should be reflected
    assert result.factors.source_authority == 0.95

def test_priority_levels(prioritizer):
    """Test priority level determination"""
    # Create content with controlled scores
    test_items = []
    for i, score_target in enumerate([0.9, 0.75, 0.55, 0.35, 0.15]):
        item = ContentItem(
            item_id=f"test{i}",
            source_id="test",
            title=f"Test Item {i}",
            content="Test content",
            url=f"https://example.com/test{i}",
            published_date=datetime.now() if score_target > 0.5 else datetime.now() - timedelta(days=30),
            author="Tester",
            topics=["test"],
            metadata={"engagement_score": score_target}
        )
        test_items.append(item)
    
    results = prioritizer.prioritize_batch(test_items)
    
    # Check that priority levels are assigned correctly
    priority_levels = [r.priority_level for r in results]
    assert ContentPriority.CRITICAL in priority_levels or ContentPriority.HIGH in priority_levels
    assert ContentPriority.MEDIUM in priority_levels
    assert ContentPriority.LOW in priority_levels or ContentPriority.ARCHIVE in priority_levels

def test_caching(prioritizer, sample_content):
    """Test result caching"""
    item = sample_content[0]
    
    # First call
    result1 = prioritizer.prioritize(item)
    
    # Second call should use cache
    result2 = prioritizer.prioritize(item)
    
    assert result1.total_score == result2.total_score
    assert result1.priority_level == result2.priority_level

def test_recommendations(prioritizer, sample_content):
    """Test recommendation generation"""
    # Critical priority item
    news_item = sample_content[0]
    result = prioritizer.prioritize(news_item, strategy="news")
    
    if result.priority_level == ContentPriority.CRITICAL:
        assert any("immediate" in r.lower() for r in result.recommendations)
    
    # Technical content
    tutorial = sample_content[1]
    result = prioritizer.prioritize(tutorial, strategy="technical")
    assert len(result.recommendations) > 0

def test_statistics(prioritizer, sample_content):
    """Test statistics tracking"""
    # Process some items
    for item in sample_content:
        prioritizer.prioritize(item)
    
    stats = prioritizer.get_statistics()
    
    assert stats["total_prioritized"] >= 3
    assert "default" in stats["strategies_available"]
    assert stats["cache_size"] >= 3

if __name__ == "__main__":
    pytest.main([__file__, "-v"])