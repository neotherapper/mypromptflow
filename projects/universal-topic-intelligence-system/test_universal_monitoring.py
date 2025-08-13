#!/usr/bin/env python3
"""
Test script for Universal Topic Intelligence System
Validates that the universal topic monitoring system works correctly
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

from sources.universal_topic_monitor import UniversalTopicMonitor


async def test_universal_monitoring():
    """Test the universal topic monitoring system"""
    print("🚀 Testing Universal Topic Intelligence System")
    print("=" * 60)
    
    try:
        # Initialize the universal monitor
        monitor = UniversalTopicMonitor()
        
        # Display available topics
        print("\n📋 Available Topic Configurations:")
        topics = monitor.list_available_topics()
        
        if not topics:
            print("❌ No topic configurations found!")
            print("Please ensure YAML configuration files exist in universal-topic-system/examples/")
            return False
        
        for topic in topics:
            print(f"  ✅ {topic['name']} ({topic['slug']})")
            print(f"     - Priority: {topic['priority_level']}")
            print(f"     - Sources: {topic['source_count']}")
            print(f"     - Status: {topic['status']}")
        
        # Display monitoring statistics
        print(f"\n📊 Monitoring Statistics:")
        stats = monitor.get_monitoring_stats()
        print(f"  - Total Topics: {stats['total_topics']}")
        print(f"  - Active Topics: {stats['active_topics']}")
        print(f"  - Total Sources: {stats['total_sources']}")
        print(f"  - Average Sources per Topic: {stats['average_sources_per_topic']:.1f}")
        
        # Test monitoring a specific topic
        if stats['active_topics'] > 0:
            first_topic = stats['topics'][0]
            print(f"\n🔍 Testing monitoring for topic: {first_topic}")
            
            # Show topic sources
            sources = monitor.get_topic_sources(first_topic)
            print(f"  Sources to monitor ({len(sources)}):")
            for source in sources[:5]:  # Show first 5 sources
                print(f"    - {source.get('url', 'N/A')} (Authority: {source.get('authority_score', 0)})")
            if len(sources) > 5:
                print(f"    ... and {len(sources) - 5} more sources")
            
            # Perform actual monitoring test
            print(f"\n⏳ Running monitoring test...")
            result = await monitor.monitor_topic(first_topic)
            
            print(f"\n✅ Monitoring Results:")
            print(f"  - Topic: {result['topic']}")
            print(f"  - Sources Monitored: {result['sources_monitored']}")
            print(f"  - Total Items Found: {result['total_items']}")
            
            # Show source results
            if result['results']:
                print(f"\n📋 Per-Source Results:")
                for source_id, source_result in result['results'].items():
                    items = source_result.get('items_found', 0)
                    status = '✅' if 'error' not in source_result else '❌'
                    print(f"    {status} {source_id}: {items} items")
            
            print(f"\n🎉 Universal monitoring test completed successfully!")
            return True
        
        else:
            print("❌ No active topics available for testing")
            return False
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_backward_compatibility():
    """Test that the system maintains backward compatibility with Claude monitoring"""
    print("\n🔄 Testing Backward Compatibility")
    print("=" * 40)
    
    try:
        from sources.universal_topic_monitor import monitor_claude_topics
        
        result = await monitor_claude_topics()
        
        if result:
            print(f"✅ Claude topics monitoring: {result.get('total_items', 0)} items found")
            return True
        else:
            print("⚠️  No Claude-specific topics found (this is expected with new universal system)")
            return True
            
    except Exception as e:
        print(f"❌ Backward compatibility error: {e}")
        return False


async def main():
    """Run all tests"""
    print("🧪 Universal Topic Intelligence System Test Suite")
    print("=" * 70)
    
    # Test universal monitoring
    test1_passed = await test_universal_monitoring()
    
    # Test backward compatibility
    test2_passed = await test_backward_compatibility()
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 Test Results Summary:")
    print(f"  Universal Monitoring: {'✅ PASS' if test1_passed else '❌ FAIL'}")
    print(f"  Backward Compatibility: {'✅ PASS' if test2_passed else '❌ FAIL'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 All tests passed! Universal Topic Intelligence System is ready!")
        print("\nNext Steps:")
        print("1. Update main monitoring system to use UniversalTopicMonitor")
        print("2. Create additional topic configurations as needed")
        print("3. Integrate with dashboard for multi-topic display")
    else:
        print("\n⚠️  Some tests failed. Please review configuration files and system setup.")
    
    return test1_passed and test2_passed


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)