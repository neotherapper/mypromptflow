#!/usr/bin/env python3
"""
Test the fixed universal monitoring system with database storage
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from sources.universal_topic_monitor_fixed import UniversalTopicMonitorFixed


async def test_universal_with_storage():
    """Test the fixed universal monitoring with database storage"""
    print("🧪 Testing Fixed Universal Topic Intelligence System")
    print("=" * 60)
    
    monitor = UniversalTopicMonitorFixed()
    
    # Display available topics
    print("\n📋 Available Topics:")
    topics = monitor.list_available_topics()
    for topic in topics:
        print(f"  ✅ {topic['name']} ({topic['slug']})")
        print(f"     - Sources: {topic['source_count']}")
        print(f"     - Quality Scorer: {'✅' if topic['has_quality_scorer'] else '❌'}")
    
    # Display stats
    print(f"\n📊 System Statistics:")
    stats = monitor.get_monitoring_stats()
    print(f"  - Total Topics: {stats['total_topics']}")
    print(f"  - Active Topics: {stats['active_topics']}")
    print(f"  - Total Sources: {stats['total_sources']}")
    
    # Test monitoring a single topic
    if stats['active_topics'] > 0:
        first_topic = stats['topics'][0]
        print(f"\n🔍 Testing single topic monitoring: {first_topic}")
        
        result = await monitor.monitor_topic_with_storage(first_topic)
        
        print(f"\n✅ Results for {result['topic_name']}:")
        print(f"  - Sources Monitored: {result['sources_monitored']}")
        print(f"  - Items Found: {result['total_items_found']}")
        print(f"  - Items Stored: {result['total_items_stored']}")
        print(f"  - Success Rate: {result['success_rate']:.1f}%")
        
        # Show per-source results
        if result['results']:
            print(f"\n📋 Source Breakdown:")
            for source_id, source_result in result['results'].items():
                if source_result['success']:
                    print(f"    ✅ {source_id}: {source_result['items_found']} found, {source_result['items_stored']} stored")
                else:
                    error = source_result.get('error', source_result.get('errors', ['Unknown error'])[0] if source_result.get('errors') else 'Unknown error')
                    print(f"    ❌ {source_id}: {error}")
    
    # Test monitoring all topics
    print(f"\n🌐 Testing all topics monitoring with storage...")
    all_results = await monitor.monitor_all_topics_with_storage()
    
    print(f"\n📊 Overall Results:")
    print(f"  - Topics Monitored: {all_results['topics_monitored']}")
    print(f"  - Total Items Found: {all_results['total_items_found']}")
    print(f"  - Total Items Stored: {all_results['total_items_stored']}")
    
    # Per-topic summary
    print(f"\n📈 Per-Topic Summary:")
    for topic_slug, topic_result in all_results['topic_results'].items():
        print(f"  {topic_result['topic_name']}:")
        print(f"    - Found: {topic_result['total_items_found']}")
        print(f"    - Stored: {topic_result['total_items_stored']}")
    
    # Global stats
    print(f"\n🎯 Global Statistics:")
    global_stats = all_results['global_stats']
    print(f"  - Total Items Stored: {global_stats['items_stored']}")
    print(f"  - Sources Success: {global_stats['sources_success']}")
    print(f"  - Sources Failed: {global_stats['sources_failed']}")
    print(f"  - Success Rate: {global_stats.get('success_rate', 0):.1f}%")
    
    return all_results['total_items_stored'] > 0


if __name__ == "__main__":
    success = asyncio.run(test_universal_with_storage())
    
    if success:
        print("\n🎉 SUCCESS! Items were stored in the database.")
        print("You can now run the universal dashboard to see the content.")
    else:
        print("\n⚠️  No items were stored. Check RSS feed configurations.")
    
    sys.exit(0 if success else 1)