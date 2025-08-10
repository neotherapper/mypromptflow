#!/usr/bin/env python3
"""
Test RSS Monitor with Real News Sources
Tests the RSS monitoring system with actual news feeds
"""

import asyncio
from datetime import datetime, timedelta
import json
from pathlib import Path

# Import components
from sources.rss_monitor import RSSSourceMonitor
from core import (
    SourceMetadata,
    SourceType,
    SourceMonitorFactory,
    UniversalContentPrioritizer
)

# Real news source configurations
NEWS_SOURCES = [
    {
        "source_id": "techcrunch_rss",
        "source_name": "TechCrunch",
        "source_url": "https://techcrunch.com/feed/",
        "authority_score": 0.85,
        "topics": ["technology", "startups", "ai", "software"]
    },
    {
        "source_id": "bbc_tech_rss",
        "source_name": "BBC Technology",
        "source_url": "http://feeds.bbci.co.uk/news/technology/rss.xml",
        "authority_score": 0.95,
        "topics": ["technology", "news", "innovation"]
    },
    {
        "source_id": "hackernews_rss",
        "source_name": "Hacker News",
        "source_url": "https://hnrss.org/frontpage",
        "authority_score": 0.75,
        "topics": ["programming", "technology", "startups"]
    },
    {
        "source_id": "verge_rss",
        "source_name": "The Verge",
        "source_url": "https://www.theverge.com/rss/index.xml",
        "authority_score": 0.80,
        "topics": ["technology", "gadgets", "science"]
    },
    {
        "source_id": "wired_rss",
        "source_name": "Wired",
        "source_url": "https://www.wired.com/feed/rss",
        "authority_score": 0.82,
        "topics": ["technology", "culture", "innovation"]
    }
]

async def test_single_source(source_config):
    """Test a single RSS source"""
    print(f"\n📡 Testing {source_config['source_name']}...")
    print("=" * 60)
    
    # Create source metadata
    metadata = SourceMetadata(
        source_id=source_config["source_id"],
        source_name=source_config["source_name"],
        source_type=SourceType.RSS,
        source_url=source_config["source_url"],
        authority_score=source_config["authority_score"],
        update_frequency="hourly",
        topics=source_config["topics"]
    )
    
    # Create RSS monitor
    monitor = RSSSourceMonitor(metadata, config={
        "timeout": 15,
        "max_items": 10
    })
    
    try:
        # Fetch and monitor content
        result = await monitor.monitor()
        
        if result.success:
            print(f"✅ Successfully fetched {source_config['source_name']}")
            print(f"   Items found: {result.items_found}")
            print(f"   New items: {len(result.new_items)}")
            print(f"   Fetch time: {result.performance_metrics.get('fetch_time', 0):.2f}s")
            
            # Show sample content
            if result.new_items:
                print(f"\n📰 Latest headlines:")
                for i, item in enumerate(result.new_items[:3], 1):
                    print(f"   {i}. {item.title[:80]}...")
                    print(f"      Topics: {', '.join(item.topics[:5])}")
                    print(f"      Published: {item.published_date.strftime('%Y-%m-%d %H:%M')}")
            
            return result
        else:
            print(f"❌ Failed to fetch {source_config['source_name']}")
            print(f"   Errors: {', '.join(result.errors)}")
            return None
            
    except Exception as e:
        print(f"❌ Exception for {source_config['source_name']}: {str(e)}")
        return None

async def test_all_sources():
    """Test all configured news sources"""
    print("🚀 Testing RSS Monitor with Real News Sources")
    print("=" * 80)
    
    # Register RSS monitor
    SourceMonitorFactory.register_monitor(SourceType.RSS, RSSSourceMonitor)
    
    results = []
    successful_sources = []
    failed_sources = []
    
    # Test each source
    for source in NEWS_SOURCES:
        result = await test_single_source(source)
        
        if result and result.success:
            successful_sources.append(source)
            results.append({
                "source": source["source_name"],
                "items": len(result.new_items),
                "fetch_time": result.performance_metrics.get('fetch_time', 0)
            })
        else:
            failed_sources.append(source["source_name"])
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    print(f"✅ Successful sources: {len(successful_sources)}/{len(NEWS_SOURCES)}")
    
    if successful_sources:
        print("\nSuccessfully fetched:")
        for source in successful_sources:
            print(f"   • {source['source_name']}")
    
    if failed_sources:
        print(f"\n❌ Failed sources: {len(failed_sources)}")
        for source in failed_sources:
            print(f"   • {source}")
    
    # Aggregate content for prioritization test
    if successful_sources:
        print("\n⚖️ Testing Content Prioritization Across Sources")
        print("-" * 60)
        
        # Collect all items
        all_items = []
        for source in successful_sources:
            metadata = SourceMetadata(
                source_id=source["source_id"],
                source_name=source["source_name"],
                source_type=SourceType.RSS,
                source_url=source["source_url"],
                authority_score=source["authority_score"],
                update_frequency="hourly",
                topics=source["topics"]
            )
            
            monitor = RSSSourceMonitor(metadata, config={"max_items": 5})
            result = await monitor.monitor()
            if result.success:
                all_items.extend(result.new_items)
        
        # Prioritize content
        prioritizer = UniversalContentPrioritizer()
        
        # Set topic preferences
        prioritizer.set_topic_preferences({
            "ai": 0.95,
            "programming": 0.85,
            "technology": 0.75,
            "startups": 0.70,
            "innovation": 0.65
        })
        
        # Set source authorities
        source_authorities = {
            source["source_id"]: source["authority_score"] 
            for source in successful_sources
        }
        prioritizer.set_source_authorities(source_authorities)
        
        # Prioritize
        priority_results = prioritizer.prioritize_batch(
            all_items[:20],  # Top 20 items
            strategy="news"
        )
        
        print(f"\n🏆 Top Priority Content (from {len(all_items)} total items):")
        for i, pr in enumerate(priority_results[:5], 1):
            print(f"\n   {i}. {pr.content_item.title[:70]}...")
            print(f"      Source: {pr.content_item.source_id}")
            print(f"      Score: {pr.total_score:.3f}")
            print(f"      Priority: {pr.priority_level.value}")
            print(f"      Topics: {', '.join(pr.content_item.topics[:3])}")
    
    # Save test report
    report = {
        "timestamp": datetime.now().isoformat(),
        "sources_tested": len(NEWS_SOURCES),
        "successful": len(successful_sources),
        "failed": len(failed_sources),
        "results": results,
        "success_rate": len(successful_sources) / len(NEWS_SOURCES)
    }
    
    report_path = Path("rss_test_report.json")
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Report saved to {report_path}")
    
    return len(successful_sources) > 0

async def test_continuous_monitoring():
    """Test continuous monitoring capabilities"""
    print("\n🔄 Testing Continuous Monitoring (30 seconds)")
    print("=" * 60)
    
    # Use TechCrunch for continuous test
    source = NEWS_SOURCES[0]
    metadata = SourceMetadata(
        source_id=source["source_id"],
        source_name=source["source_name"],
        source_type=SourceType.RSS,
        source_url=source["source_url"],
        authority_score=source["authority_score"],
        update_frequency="continuous",
        topics=source["topics"]
    )
    
    monitor = RSSSourceMonitor(metadata, config={
        "timeout": 10,
        "max_items": 5
    })
    
    # Monitor 3 times with 10-second intervals
    for i in range(3):
        print(f"\n📡 Monitor cycle {i+1}/3...")
        result = await monitor.monitor()
        
        if result.success:
            print(f"   Found {len(result.new_items)} new items")
            if result.new_items:
                print(f"   Latest: {result.new_items[0].title[:60]}...")
        
        if i < 2:
            print("   Waiting 10 seconds...")
            await asyncio.sleep(10)
    
    # Check metrics
    metrics = monitor.get_metrics()
    print(f"\n📈 Monitoring Metrics:")
    print(f"   Total fetches: {metrics['total_fetches']}")
    print(f"   Success rate: {metrics['success_rate']:.1%}")
    print(f"   Average fetch time: {metrics['avg_fetch_time']:.2f}s")
    print(f"   Total items processed: {metrics['total_items']}")

def main():
    """Main test runner"""
    print("🧪 RSS News Monitor - Real Source Testing")
    print("=" * 80)
    print("Testing with real news RSS feeds from major tech publications")
    print("This test will fetch actual content from the internet\n")
    
    loop = asyncio.get_event_loop()
    
    # Run tests
    try:
        # Test 1: All sources
        success = loop.run_until_complete(test_all_sources())
        
        if success:
            # Test 2: Continuous monitoring
            loop.run_until_complete(test_continuous_monitoring())
            
            print("\n" + "=" * 80)
            print("✅ RSS NEWS MONITOR TESTS COMPLETED SUCCESSFULLY")
            print("The system is ready to monitor real news sources!")
        else:
            print("\n⚠️ Some tests failed. Check connectivity and source availability.")
            
    except KeyboardInterrupt:
        print("\n\n⚠️ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        raise

if __name__ == "__main__":
    main()