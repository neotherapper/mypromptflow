#!/usr/bin/env python3
"""
System Integration Test
Verifies the Universal Topic Intelligence System is working correctly
"""

import asyncio
from datetime import datetime, timedelta
import json
from pathlib import Path

# Import core components
from core import (
    UniversalSourceMonitor,
    UniversalContentPrioritizer,
    SourceType,
    SourceMetadata,
    ContentItem,
    SourceMonitorFactory
)

class TestRSSMonitor(UniversalSourceMonitor):
    """Test RSS monitor implementation"""
    
    async def fetch_content(self):
        """Simulate RSS feed fetch"""
        print("📡 Fetching simulated RSS content...")
        return [
            {
                "id": "news_001",
                "title": "Breaking: AI System Achieves Human-Level Performance",
                "description": "Revolutionary breakthrough in artificial intelligence...",
                "link": "https://news.example.com/ai-breakthrough",
                "pubDate": datetime.now().isoformat(),
                "author": "Tech Reporter"
            },
            {
                "id": "news_002", 
                "title": "React 19 Released with Game-Changing Features",
                "description": "The React team announces major performance improvements...",
                "link": "https://react.dev/blog/react-19",
                "pubDate": (datetime.now() - timedelta(hours=2)).isoformat(),
                "author": "React Team"
            },
            {
                "id": "news_003",
                "title": "Cryptocurrency Market Sees Major Shift",
                "description": "Bitcoin and Ethereum experience significant changes...",
                "link": "https://crypto.news/market-shift",
                "pubDate": (datetime.now() - timedelta(hours=5)).isoformat(),
                "author": "Crypto Analyst"
            }
        ]
    
    def parse_content(self, raw_content):
        """Parse RSS content into ContentItem"""
        # Determine topics based on title
        topics = []
        title_lower = raw_content["title"].lower()
        
        if "ai" in title_lower or "artificial" in title_lower:
            topics.extend(["ai", "technology", "innovation"])
        if "react" in title_lower or "javascript" in title_lower:
            topics.extend(["react", "frontend", "webdev"])
        if "crypto" in title_lower or "bitcoin" in title_lower:
            topics.extend(["cryptocurrency", "finance", "blockchain"])
        
        if not topics:
            topics = ["general", "news"]
        
        return ContentItem(
            item_id=raw_content["id"],
            source_id=self.source_metadata.source_id,
            title=raw_content["title"],
            content=raw_content.get("description", ""),
            url=raw_content["link"],
            published_date=datetime.fromisoformat(raw_content["pubDate"]),
            author=raw_content.get("author"),
            topics=topics,
            metadata={
                "source_type": "rss",
                "original": raw_content
            }
        )

async def test_monitoring_system():
    """Test the complete monitoring system"""
    print("🚀 Testing Universal Topic Intelligence System")
    print("=" * 60)
    
    # 1. Create source metadata
    print("\n📋 Step 1: Creating source metadata...")
    news_source = SourceMetadata(
        source_id="test_news_rss",
        source_name="Test News RSS Feed",
        source_type=SourceType.RSS,
        source_url="https://news.example.com/rss",
        authority_score=0.85,
        update_frequency="hourly",
        topics=["technology", "ai", "programming", "cryptocurrency"]
    )
    print(f"✅ Created source: {news_source.source_name}")
    print(f"   Authority: {news_source.authority_score}")
    print(f"   Topics: {', '.join(news_source.topics)}")
    
    # 2. Create and register monitor
    print("\n🔌 Step 2: Setting up source monitor...")
    SourceMonitorFactory.register_monitor(SourceType.RSS, TestRSSMonitor)
    monitor = SourceMonitorFactory.create_monitor(news_source)
    print(f"✅ Monitor registered for {news_source.source_type.value}")
    
    # 3. Run monitoring
    print("\n📡 Step 3: Running content monitoring...")
    result = await monitor.monitor()
    
    if result.success:
        print(f"✅ Monitoring successful!")
        print(f"   Items found: {result.items_found}")
        print(f"   New items: {len(result.new_items)}")
        print(f"   Fetch time: {result.performance_metrics.get('fetch_time', 0):.2f}s")
        
        # Display found items
        print("\n📰 Content discovered:")
        for item in result.new_items:
            print(f"   • {item.title[:60]}...")
            print(f"     Topics: {', '.join(item.topics)}")
            print(f"     Published: {item.published_date.strftime('%Y-%m-%d %H:%M')}")
    else:
        print(f"❌ Monitoring failed: {', '.join(result.errors)}")
        return False
    
    # 4. Test content prioritization
    print("\n⚖️ Step 4: Testing content prioritization...")
    prioritizer = UniversalContentPrioritizer()
    
    # Set topic preferences (simulating user interests)
    prioritizer.set_topic_preferences({
        "ai": 0.9,
        "react": 0.8,
        "cryptocurrency": 0.6,
        "technology": 0.7,
        "frontend": 0.75
    })
    
    # Set source authorities
    prioritizer.set_source_authorities({
        news_source.source_id: news_source.authority_score
    })
    
    # Prioritize content
    priority_results = prioritizer.prioritize_batch(
        result.new_items,
        strategy="news"
    )
    
    print(f"✅ Prioritized {len(priority_results)} items")
    print("\n📊 Priority Rankings:")
    for i, pr in enumerate(priority_results, 1):
        print(f"   {i}. {pr.content_item.title[:50]}...")
        print(f"      Score: {pr.total_score:.3f}")
        print(f"      Priority: {pr.priority_level.value}")
        print(f"      Key factors: {pr.reasoning.split('Key factors: ')[1].split('.')[0]}")
        if pr.recommendations:
            print(f"      Recommendations: {pr.recommendations[0]}")
    
    # 5. Test source validation
    print("\n✔️ Step 5: Validating source accessibility...")
    is_valid = await monitor.validate_source()
    print(f"✅ Source validation: {'Passed' if is_valid else 'Failed'}")
    
    # 6. Check metrics
    print("\n📈 Step 6: System metrics...")
    monitor_metrics = monitor.get_metrics()
    print(f"   Total fetches: {monitor_metrics['total_fetches']}")
    print(f"   Success rate: {monitor_metrics['success_rate']:.1%}")
    print(f"   Average fetch time: {monitor_metrics['avg_fetch_time']:.3f}s")
    
    prioritizer_stats = prioritizer.get_statistics()
    print(f"   Strategies available: {', '.join(prioritizer_stats['strategies_available'])}")
    print(f"   Items prioritized: {prioritizer_stats['total_prioritized']}")
    
    # 7. Test duplicate detection
    print("\n🔍 Step 7: Testing duplicate detection...")
    result2 = await monitor.monitor()
    print(f"✅ Second monitor run: {len(result2.new_items)} new items (should be 0)")
    
    # 8. Generate summary report
    print("\n📄 Step 8: Generating system report...")
    report = {
        "timestamp": datetime.now().isoformat(),
        "system_version": "2.0.0",
        "test_results": {
            "monitoring": "✅ Passed" if result.success else "❌ Failed",
            "prioritization": "✅ Passed" if len(priority_results) > 0 else "❌ Failed",
            "source_validation": "✅ Passed" if is_valid else "❌ Failed",
            "duplicate_detection": "✅ Passed" if len(result2.new_items) == 0 else "❌ Failed"
        },
        "content_summary": {
            "total_items": result.items_found,
            "new_items": len(result.new_items),
            "topics_covered": list(set(topic for item in result.new_items for topic in item.topics)),
            "highest_priority": priority_results[0].priority_level.value if priority_results else None,
            "top_content": priority_results[0].content_item.title if priority_results else None
        },
        "performance": {
            "fetch_time": result.performance_metrics.get('fetch_time', 0),
            "items_per_second": result.performance_metrics.get('items_per_second', 0),
            "success_rate": monitor_metrics['success_rate']
        }
    }
    
    # Save report
    report_path = Path("test_report.json")
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"✅ Report saved to {report_path}")
    
    # Final status
    print("\n" + "=" * 60)
    all_passed = all([
        result.success,
        len(priority_results) > 0,
        is_valid,
        len(result2.new_items) == 0
    ])
    
    if all_passed:
        print("🎉 ALL TESTS PASSED! System is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the report for details.")
    
    return all_passed

async def test_multi_source_monitoring():
    """Test monitoring multiple sources simultaneously"""
    print("\n🌐 Testing Multi-Source Monitoring")
    print("=" * 60)
    
    # Create multiple sources
    sources = [
        SourceMetadata(
            source_id="tech_news",
            source_name="Tech News",
            source_type=SourceType.RSS,
            source_url="https://tech.news/rss",
            authority_score=0.9,
            update_frequency="hourly",
            topics=["technology", "innovation"]
        ),
        SourceMetadata(
            source_id="dev_blog",
            source_name="Developer Blog",
            source_type=SourceType.RSS,
            source_url="https://dev.blog/rss",
            authority_score=0.75,
            update_frequency="daily",
            topics=["programming", "tutorials"]
        ),
        SourceMetadata(
            source_id="ai_research",
            source_name="AI Research",
            source_type=SourceType.RSS,
            source_url="https://ai.research/rss",
            authority_score=0.95,
            update_frequency="weekly",
            topics=["ai", "machine-learning", "research"]
        )
    ]
    
    # Monitor all sources concurrently
    monitors = [SourceMonitorFactory.create_monitor(source) for source in sources]
    results = await asyncio.gather(*[monitor.monitor() for monitor in monitors])
    
    print(f"✅ Monitored {len(sources)} sources simultaneously")
    
    # Aggregate results
    all_items = []
    for source, result in zip(sources, results):
        if result.success:
            print(f"   • {source.source_name}: {len(result.new_items)} items")
            all_items.extend(result.new_items)
    
    print(f"\n📊 Total content collected: {len(all_items)} items")
    
    # Prioritize all content together
    prioritizer = UniversalContentPrioritizer()
    prioritized = prioritizer.prioritize_batch(all_items, strategy="default")
    
    print(f"✅ Cross-source prioritization complete")
    print(f"   Top item: {prioritized[0].content_item.title if prioritized else 'None'}")
    
    return len(all_items) > 0

def main():
    """Main test runner"""
    print("🧪 Universal Topic Intelligence System - Integration Tests")
    print("=" * 60)
    
    # Run tests
    loop = asyncio.get_event_loop()
    
    # Test 1: Basic system test
    test1_passed = loop.run_until_complete(test_monitoring_system())
    
    # Test 2: Multi-source test
    test2_passed = loop.run_until_complete(test_multi_source_monitoring())
    
    # Final summary
    print("\n" + "=" * 60)
    print("📊 FINAL TEST SUMMARY")
    print("=" * 60)
    print(f"Basic System Test: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"Multi-Source Test: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 ALL INTEGRATION TESTS PASSED!")
        print("The Universal Topic Intelligence System is ready for deployment.")
    else:
        print("\n⚠️ Some tests failed. Please review and fix issues.")
    
    return test1_passed and test2_passed

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)