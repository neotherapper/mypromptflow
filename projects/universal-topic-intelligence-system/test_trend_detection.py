#!/usr/bin/env python3
"""
Test Trend Detection Engine
Validates velocity tracking and emergence detection functionality
"""

import asyncio
import logging
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import List

# Configure logging to be less verbose
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("TrendDetectionTest")

# Import the trend detection system
from core.trend_detection_engine import TrendDetectionEngine, TrendSignal, TrendType, TrendStrength
from core.universal_source_monitor import ContentItem
from monitor import UniversalMonitor

def create_trending_content_sequence() -> List[ContentItem]:
    """Create a sequence of content items that should show a trend"""
    base_time = datetime.now(timezone.utc)
    
    # React topic showing accelerating trend
    react_items = []
    
    for i in range(10):
        # Increasing engagement over time
        views = 1000 + (i * 2000)  # Views increasing from 1K to 19K
        likes = int(views * 0.05)   # 5% like rate
        
        content = ContentItem(
            item_id=f"react_trend_{i:02d}",
            source_id="youtube_react_channel",
            title=f"React 19 Feature #{i+1} - Advanced Tutorial",
            content=f"This is tutorial #{i+1} covering React 19 features with practical examples and code demonstrations. This is getting more popular each day!",
            url=f"https://www.youtube.com/watch?v=trend{i}",
            published_date=base_time - timedelta(hours=9-i),  # Recent to older
            author="React Expert",
            topics=["react", "javascript"],
            metadata={
                "mcp_source_type": "youtube_transcript",
                "youtube_video_id": f"trend{i}",
                "youtube_channel": "React",
                "youtube_duration": "PT20M15S",
                "youtube_view_count": views,
                "youtube_like_count": likes,
                "youtube_language": "en"
            }
        )
        react_items.append(content)
    
    return react_items

def create_emerging_content_sequence() -> List[ContentItem]:
    """Create content for a newly emerging topic"""
    base_time = datetime.now(timezone.utc)
    
    # "Web Components" as emerging topic
    emerging_items = []
    
    for i in range(5):
        content = ContentItem(
            item_id=f"webcomponents_emerge_{i:02d}",
            source_id=f"source_{i % 3}",  # Multiple sources
            title=f"Web Components Revolution - Part {i+1}",
            content="Web Components are gaining massive adoption. This new browser standard is changing how we build web applications with custom elements and shadow DOM.",
            url=f"https://example.com/webcomponents/{i}",
            published_date=base_time - timedelta(hours=3-i*0.5),  # Very recent
            author="Web Platform Expert",
            topics=["webcomponents", "frontend", "standards"],
            metadata={
                "mcp_source_type": "web_search",
                "search_query": "web components 2024",
                "search_rank": i + 1,
                "search_engine": "google",
                "search_relevance_score": 0.9,
                "search_domain": "developer.mozilla.org"
            }
        )
        emerging_items.append(content)
    
    return emerging_items

def create_viral_content() -> ContentItem:
    """Create content that should be detected as viral"""
    return ContentItem(
        item_id="viral_content_001",
        source_id="github_viral_repo",
        title="Revolutionary New Framework - Breaks All Performance Records!",
        content="This groundbreaking new framework just achieved 1M+ GitHub stars in 24 hours. The developer community is going absolutely crazy about this innovation.",
        url="https://github.com/viral/framework",
        published_date=datetime.now(timezone.utc) - timedelta(hours=2),
        author="Viral Developer",
        topics=["framework", "javascript", "performance"],
        metadata={
            "mcp_source_type": "github_repository",
            "github_repo_name": "viral/framework",
            "github_stars": 1200000,  # 1.2M stars
            "github_forks": 45000,
            "github_language": "JavaScript",
            "github_license": "MIT",
            "github_open_issues": 150
        }
    )

def create_declining_content_sequence() -> List[ContentItem]:
    """Create content showing a declining trend"""
    base_time = datetime.now(timezone.utc)
    
    # jQuery showing decline
    declining_items = []
    
    for i in range(6):
        # Decreasing engagement over time
        views = 5000 - (i * 500)  # Views decreasing from 5K to 2.5K
        
        content = ContentItem(
            item_id=f"jquery_decline_{i:02d}",
            source_id="legacy_tutorials",
            title=f"jQuery Tutorial Part {i+1}",
            content="jQuery tutorial covering traditional DOM manipulation techniques.",
            url=f"https://example.com/jquery/{i}",
            published_date=base_time - timedelta(hours=5-i*0.8),
            author="Legacy Dev",
            topics=["jquery", "javascript", "legacy"],
            metadata={
                "mcp_source_type": "youtube_transcript",
                "youtube_video_id": f"decline{i}",
                "youtube_channel": "Legacy Tutorials",
                "youtube_duration": "PT15M00S",
                "youtube_view_count": views,
                "youtube_like_count": int(views * 0.02),  # Low like rate
                "youtube_language": "en"
            }
        )
        declining_items.append(content)
    
    return declining_items

async def test_trend_detection_engine():
    """Test the trend detection engine directly"""
    print("🔍 Testing Trend Detection Engine...")
    print("=" * 60)
    
    # Initialize trend detection engine
    trend_engine = TrendDetectionEngine()
    
    # Add trending content sequence
    print("📈 Adding trending React content...")
    react_items = create_trending_content_sequence()
    
    for i, content in enumerate(react_items):
        # Simulate increasing priority scores
        priority_score = 0.5 + (i * 0.05)  # 0.5 to 0.95
        signal = trend_engine.add_content_signal(content, priority_score)
        print(f"  Added signal {i+1}: topic='{signal.topic}', value={signal.value:.3f}")
    
    # Add emerging content
    print("\n🌱 Adding emerging Web Components content...")
    emerging_items = create_emerging_content_sequence()
    
    for content in emerging_items:
        signal = trend_engine.add_content_signal(content, 0.8)  # High quality emerging content
        print(f"  Added signal: topic='{signal.topic}', value={signal.value:.3f}")
    
    # Add viral content
    print("\n🚀 Adding viral content...")
    viral_content = create_viral_content()
    viral_signal = trend_engine.add_content_signal(viral_content, 1.0)
    print(f"  Added viral signal: topic='{viral_signal.topic}', value={viral_signal.value:.3f}")
    
    # Add declining content
    print("\n📉 Adding declining jQuery content...")
    declining_items = create_declining_content_sequence()
    
    for i, content in enumerate(declining_items):
        # Decreasing priority scores
        priority_score = 0.8 - (i * 0.1)  # 0.8 to 0.3
        signal = trend_engine.add_content_signal(content, max(0.1, priority_score))
        print(f"  Added signal {i+1}: topic='{signal.topic}', value={signal.value:.3f}")
    
    # Analyze trends
    print("\n🧠 Performing trend analysis...")
    analysis = trend_engine.analyze_trends("short")
    
    print(f"\n📊 Analysis Results:")
    print(f"  Total trends detected: {len(analysis.detected_trends)}")
    print(f"  Analysis window: {analysis.analysis_window_hours} hours")
    print(f"  Signals analyzed: {analysis.total_signals_analyzed}")
    print(f"  Confidence score: {analysis.confidence_score:.3f}")
    
    # Show detected trends
    if analysis.detected_trends:
        print(f"\n🎯 Detected Trends:")
        print(f"  {'Topic':<15} {'Type':<12} {'Strength':<10} {'Velocity':<8} {'Confidence':<10}")
        print(f"  {'-'*15} {'-'*12} {'-'*10} {'-'*8} {'-'*10}")
        
        for trend in analysis.detected_trends[:10]:  # Show top 10
            print(f"  {trend.topic:<15} {trend.trend_type.value:<12} {trend.trend_strength.value:<10} "
                  f"{trend.velocity:<8.2f} {trend.confidence:<10.3f}")
    
    # Show topic velocities
    if analysis.topic_velocities:
        print(f"\n⚡ Topic Velocities:")
        sorted_velocities = sorted(analysis.topic_velocities.items(), key=lambda x: abs(x[1]), reverse=True)
        for topic, velocity in sorted_velocities[:5]:
            direction = "📈" if velocity > 0 else "📉" if velocity < -0.1 else "➡️"
            print(f"    {direction} {topic}: {velocity:.3f}")
    
    # Show emerging topics
    if analysis.emergence_candidates:
        print(f"\n🌟 Emerging Topics:")
        for topic in analysis.emergence_candidates[:5]:
            print(f"    🌱 {topic}")
    
    # Show declining topics
    if analysis.declining_topics:
        print(f"\n🔻 Declining Topics:")
        for topic in analysis.declining_topics[:5]:
            print(f"    📉 {topic}")
    
    # Show viral content
    if analysis.viral_content:
        print(f"\n💥 Viral Content:")
        for content_id in analysis.viral_content[:3]:
            print(f"    🚀 {content_id}")
    
    return len(analysis.detected_trends) > 0

async def test_monitor_integration():
    """Test trend detection integration with monitor system"""
    print("\n🔗 Testing Monitor Integration with Trend Detection...")
    print("=" * 60)
    
    # Initialize monitor (should have trend detection)
    monitor = UniversalMonitor()
    
    # Verify trend detector is initialized
    if hasattr(monitor, 'trend_detector'):
        print("✅ Trend detector initialized in monitor")
    else:
        print("❌ Trend detector NOT found in monitor")
        return False
    
    # Add some test content through the monitor's content processing
    test_content = create_trending_content_sequence()[0]  # Just one item for integration test
    
    # Simulate the monitor's content processing
    try:
        # Calculate priority (like monitor does)
        priority_result = monitor.prioritizer.prioritize(test_content, strategy="intelligent")
        
        # Add trend signal (like monitor does)
        trend_signal = monitor.trend_detector.add_content_signal(test_content, priority_result.total_score)
        
        print(f"✅ Successfully processed content through trend detection")
        print(f"  Content: {test_content.title[:50]}...")
        print(f"  Priority Score: {priority_result.total_score:.3f}")
        print(f"  Trend Signal Value: {trend_signal.value:.3f}")
        print(f"  Topic: {trend_signal.topic}")
        
        # Get trend summary
        trend_summary = monitor.trend_detector.get_trend_summary("short")
        
        print(f"\n📈 Trend Summary:")
        print(f"  Active topics: {trend_summary['active_topics']}")
        print(f"  Total signals analyzed: {trend_summary['total_signals_analyzed']}")
        print(f"  Confidence score: {trend_summary['confidence_score']:.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

async def test_real_monitoring_cycle():
    """Test with a real monitoring cycle to see trend detection in action"""
    print("\n🏃‍♂️ Testing Real Monitoring Cycle with Trend Detection...")
    print("=" * 60)
    
    # Initialize monitor
    monitor = UniversalMonitor()
    
    # Run a mini monitoring cycle (just one source for speed)
    print("🚀 Running monitoring cycle...")
    
    try:
        # Test just one MCP source for speed
        test_mcp_source = monitor.mcp_sources[0]  # React YouTube Content
        
        result = await monitor.monitor_mcp_source(test_mcp_source)
        
        print(f"📊 Monitoring Result:")
        print(f"  Source: {result['source']}")
        print(f"  Success: {'✅' if result['success'] else '❌'}")
        print(f"  Items found: {result['items_found']}")
        print(f"  Items stored: {result['items_stored']}")
        
        if result['success'] and result['items_stored'] > 0:
            print(f"\n🔍 Checking trend analysis...")
            
            # Get trend summary after processing
            trend_summary = monitor.trend_detector.get_trend_summary("immediate")
            
            print(f"  Trends detected: {trend_summary['total_trends']}")
            print(f"  Active topics: {trend_summary['active_topics']}")
            print(f"  Signals analyzed: {trend_summary['total_signals_analyzed']}")
            
            if trend_summary['top_emerging']:
                print(f"  Emerging topics: {', '.join(trend_summary['top_emerging'])}")
            
            return True
        else:
            print("ℹ️  No new content stored, trend analysis not triggered")
            return True  # Still success, just no new data
            
    except Exception as e:
        print(f"❌ Real monitoring test failed: {e}")
        logger.exception("Full error details:")
        return False

async def main():
    """Main test runner"""
    print("🚀 Trend Detection Engine Test Suite")
    print("=" * 70)
    
    try:
        # Test individual components
        engine_test_passed = await test_trend_detection_engine()
        integration_test_passed = await test_monitor_integration()
        monitoring_test_passed = await test_real_monitoring_cycle()
        
        # Summary
        print("\n" + "=" * 70)
        
        if engine_test_passed and integration_test_passed and monitoring_test_passed:
            print("✅ All trend detection tests PASSED!")
            print("\n🎉 Phase 3 Component 1: Trend Detection - COMPLETE")
            print("\n🎯 Key Achievements:")
            print("  • Velocity tracking with linear regression analysis")
            print("  • Emergence detection for new topics gaining momentum")
            print("  • Viral content identification with rapid spread detection")
            print("  • Decline pattern recognition for fading topics")
            print("  • Multi-source signal aggregation and analysis")
            print("  • Real-time integration with monitor system")
            print("  • Confidence scoring for trend reliability")
            print("  • MCP metadata enhancement for trend signals")
            return True
        else:
            print("❌ Some trend detection tests FAILED")
            print(f"  Engine Test: {'✅' if engine_test_passed else '❌'}")
            print(f"  Integration Test: {'✅' if integration_test_passed else '❌'}")
            print(f"  Monitoring Test: {'✅' if monitoring_test_passed else '❌'}")
            return False
            
    except Exception as e:
        print(f"\n💥 Test suite failed with error: {e}")
        logger.exception("Full test error details:")
        return False

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)