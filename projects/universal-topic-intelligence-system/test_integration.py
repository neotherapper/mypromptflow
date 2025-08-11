#!/usr/bin/env python3
"""
Integration Test for Universal Topic Intelligence System
Tests the complete system with Queen Agent, Architects, and monitoring
"""

import asyncio
from datetime import datetime
import json
from pathlib import Path
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

# Import all components
from core import (
    UniversalContentPrioritizer,
    SourceMetadata,
    SourceType,
    SourceMonitorFactory,
    ContentItem,
    ContentPriority
)
from sources.rss_monitor import RSSSourceMonitor
from agents.queen_agent import QueenAgent, ResourceAllocationStrategy
from agents.architect_agents import (
    ArchitectCoordinator,
    OfficialSourceArchitect,
    CommunityIntelligenceArchitect,
    TrendDetectionArchitect
)


async def test_component_initialization():
    """Test that all components initialize correctly"""
    print("\n🔧 Testing Component Initialization")
    print("=" * 60)
    
    try:
        # Test prioritizer
        prioritizer = UniversalContentPrioritizer()
        print("✅ Content Prioritizer initialized")
        
        # Test RSS monitor factory registration
        SourceMonitorFactory.register_monitor(SourceType.RSS, RSSSourceMonitor)
        print("✅ RSS Monitor registered with factory")
        
        # Test Queen Agent
        queen = QueenAgent(config_dir="configs/topics")
        print(f"✅ Queen Agent initialized with {len(queen.topics)} topics")
        
        # Test Architect Coordinator
        coordinator = ArchitectCoordinator()
        print(f"✅ Architect Coordinator initialized with {len(coordinator.architects)} architects")
        
        return True
        
    except Exception as e:
        print(f"❌ Initialization failed: {str(e)}")
        return False


async def test_single_topic_monitoring():
    """Test monitoring a single topic (Claude AI)"""
    print("\n📡 Testing Single Topic Monitoring (Claude AI)")
    print("=" * 60)
    
    try:
        # Initialize Queen Agent
        queen = QueenAgent(config_dir="configs/topics")
        
        # Force monitoring of Claude AI topic
        result = await queen.orchestrate(force_topics=["claude-ai"])
        
        print(f"✅ Monitored {len(result.topics_monitored)} topic(s)")
        print(f"   Total items collected: {result.total_items_collected}")
        print(f"   Critical items: {len(result.critical_items)}")
        print(f"   Cross-topic insights: {len(result.cross_topic_insights)}")
        
        # Display insights
        if result.cross_topic_insights:
            print("\n📊 Cross-Topic Insights:")
            for insight in result.cross_topic_insights[:3]:
                print(f"   • {insight.get('type', 'unknown')}: {insight.get('description', '')}")
        
        # Display resource usage
        print("\n💰 Resource Usage:")
        for topic, resources in result.resource_usage.items():
            print(f"   • {topic}: {resources:.1f} units")
        
        return result.total_items_collected > 0
        
    except Exception as e:
        print(f"❌ Single topic monitoring failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_multi_topic_orchestration():
    """Test orchestrating multiple topics simultaneously"""
    print("\n🌐 Testing Multi-Topic Orchestration")
    print("=" * 60)
    
    try:
        # Initialize Queen Agent
        queen = QueenAgent(config_dir="configs/topics")
        
        # Set adaptive resource allocation
        queen.allocation_strategy = ResourceAllocationStrategy.ADAPTIVE
        
        # Orchestrate all available topics
        result = await queen.orchestrate()
        
        print(f"✅ Orchestrated {len(result.topics_monitored)} topics")
        print(f"   Total items: {result.total_items_collected}")
        print(f"   Performance: {result.performance_metrics.get('items_per_second', 0):.2f} items/sec")
        print(f"   Resource efficiency: {result.performance_metrics.get('resource_efficiency', 0):.2f}")
        
        # Show topics monitored
        print("\n📋 Topics Monitored:")
        for topic in result.topics_monitored:
            state = queen.topics.get(topic)
            if state:
                print(f"   • {state.topic_name} ({state.priority_level} priority)")
                print(f"     Items: {state.items_collected}, Errors: {state.error_count}")
        
        # Show cross-topic patterns
        if result.cross_topic_insights:
            print("\n🔗 Cross-Topic Patterns:")
            for insight in result.cross_topic_insights:
                if insight.get("type") == "topic_overlap":
                    print("   Topic overlaps detected:")
                    for overlap in insight.get("data", [])[:3]:
                        print(f"     • {' & '.join(overlap['topics'])}: {overlap['count']} co-occurrences")
        
        return len(result.topics_monitored) > 0
        
    except Exception as e:
        print(f"❌ Multi-topic orchestration failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_architect_coordination():
    """Test architect agents working together"""
    print("\n👷 Testing Architect Coordination")
    print("=" * 60)
    
    try:
        # Load a topic configuration
        config_path = Path("configs/topics/claude-ai-configuration.yaml")
        if not config_path.exists():
            print("⚠️ Claude AI configuration not found, skipping architect test")
            return True
        
        import yaml
        with open(config_path) as f:
            topic_config = yaml.safe_load(f)
        
        # Initialize coordinator
        coordinator = ArchitectCoordinator()
        
        # Create mock source mapping for testing
        source_mapping = topic_config.get("source_mapping", {})
        
        # Process with architects (this will attempt real monitoring)
        print("🔄 Processing sources with architects...")
        results = await coordinator.coordinate_analysis(topic_config, source_mapping)
        
        print(f"✅ {len(results)} architects completed analysis")
        
        # Display architect results
        for role, result in results.items():
            print(f"\n📊 {role.replace('_', ' ').title()}:")
            print(f"   Items processed: {result.items_processed}")
            print(f"   High-value items: {len(result.high_value_items)}")
            print(f"   Recommendations: {len(result.recommendations)}")
            
            # Show top recommendation
            if result.recommendations:
                print(f"   Top rec: {result.recommendations[0][:80]}...")
        
        # Synthesize insights
        synthesis = coordinator.synthesize_insights(results)
        
        print("\n🎯 Synthesized Insights:")
        print(f"   Total items: {synthesis['total_items_processed']}")
        print(f"   Priority recommendations: {len(synthesis['priority_recommendations'])}")
        
        if synthesis['priority_recommendations']:
            print("\n   Top Priority Actions:")
            for rec in synthesis['priority_recommendations'][:3]:
                print(f"   • {rec[:80]}...")
        
        return len(results) > 0
        
    except Exception as e:
        print(f"❌ Architect coordination failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_emergency_response():
    """Test emergency response capability"""
    print("\n🚨 Testing Emergency Response")
    print("=" * 60)
    
    try:
        # Initialize Queen Agent
        queen = QueenAgent(config_dir="configs/topics")
        
        # Trigger emergency response
        emergency_task = queen.emergency_response("Critical Claude update detected")
        
        print("⏰ Emergency response triggered, processing high-priority topics...")
        
        # Wait for emergency processing
        result = await emergency_task
        
        print(f"✅ Emergency processing complete")
        print(f"   Topics processed: {len(result.topics_monitored)}")
        print(f"   Critical items found: {len(result.critical_items)}")
        
        # Show critical items
        if result.critical_items:
            print("\n🔴 Critical Items:")
            for item in result.critical_items[:3]:
                print(f"   • {item.title[:60]}...")
                print(f"     Priority: {item.metadata.get('priority', 'unknown')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Emergency response failed: {str(e)}")
        return False


async def test_content_prioritization():
    """Test content prioritization with real examples"""
    print("\n⚖️ Testing Content Prioritization")
    print("=" * 60)
    
    try:
        prioritizer = UniversalContentPrioritizer()
        
        # Create test content items
        test_items = [
            ContentItem(
                item_id="test1",
                source_id="anthropic_blog",
                title="Breaking: Claude 3.5 Sonnet Released with Major Improvements",
                content="Anthropic announces Claude 3.5 Sonnet with significant performance improvements...",
                url="https://anthropic.com/claude-3-5",
                published_date=datetime.now(),
                author="Anthropic Team",
                topics=["claude", "ai", "release"],
                metadata={"source_authority": 1.0}
            ),
            ContentItem(
                item_id="test2",
                source_id="dev_blog",
                title="Building a React App with Claude Code",
                content="Tutorial on using Claude Code for React development...",
                url="https://dev.to/react-claude",
                published_date=datetime.now(),
                author="Dev Author",
                topics=["claude", "react", "tutorial"],
                metadata={"engagement_score": 0.8}
            ),
            ContentItem(
                item_id="test3",
                source_id="community",
                title="Common Issues with TypeScript 5.0",
                content="Discussion of TypeScript 5.0 migration problems...",
                url="https://forum.ts/issues",
                published_date=datetime.now(),
                author="Community Member",
                topics=["typescript", "problems"],
                metadata={"engagement_score": 0.6}
            )
        ]
        
        # Set preferences aligned with user interests
        prioritizer.set_topic_preferences({
            "claude": 1.0,
            "react": 0.9,
            "typescript": 0.85,
            "ai": 0.8,
            "tutorial": 0.7
        })
        
        # Prioritize content
        results = prioritizer.prioritize_batch(test_items, strategy="news")
        
        print(f"✅ Prioritized {len(results)} items")
        print("\n📊 Priority Rankings:")
        
        for i, result in enumerate(results, 1):
            print(f"\n   {i}. {result.content_item.title[:60]}...")
            print(f"      Score: {result.total_score:.3f}")
            print(f"      Priority: {result.priority_level.value}")
            print(f"      Topics: {', '.join(result.content_item.topics)}")
            
            # Show factor breakdown
            factors = result.factors
            print(f"      Factors:")
            print(f"        - Authority: {factors.source_authority:.2f}")
            print(f"        - Recency: {factors.content_recency:.2f}")
            print(f"        - Relevance: {factors.topic_relevance:.2f}")
        
        # Verify Claude content is prioritized
        top_item = results[0].content_item
        is_claude_prioritized = "claude" in top_item.topics
        
        if is_claude_prioritized:
            print("\n✅ Claude content correctly prioritized")
        
        return is_claude_prioritized
        
    except Exception as e:
        print(f"❌ Content prioritization failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


async def test_system_performance():
    """Test system performance metrics"""
    print("\n⚡ Testing System Performance")
    print("=" * 60)
    
    try:
        # Initialize components
        queen = QueenAgent(config_dir="configs/topics")
        
        # Measure orchestration time
        start_time = datetime.now()
        
        # Run orchestration
        result = await queen.orchestrate()
        
        duration = (datetime.now() - start_time).total_seconds()
        
        print(f"✅ Performance Metrics:")
        print(f"   Orchestration time: {duration:.2f} seconds")
        print(f"   Topics processed: {len(result.topics_monitored)}")
        print(f"   Items collected: {result.total_items_collected}")
        print(f"   Items per second: {result.total_items_collected / duration:.2f}")
        print(f"   Resource efficiency: {result.performance_metrics.get('resource_efficiency', 0):.2f}")
        
        # Get Queen Agent status
        status = queen.get_status()
        
        print(f"\n📈 System Status:")
        print(f"   Total orchestrations: {status['orchestration_count']}")
        print(f"   Total items processed: {status['total_items_processed']}")
        print(f"   Topics managed: {status['topics_managed']}")
        print(f"   Shared sources: {status['shared_sources']}")
        print(f"   Known relationships: {status['known_relationships']}")
        
        # Performance thresholds
        performance_ok = duration < 30  # Should complete within 30 seconds
        
        if performance_ok:
            print("\n✅ Performance within acceptable limits")
        else:
            print("\n⚠️ Performance slower than expected")
        
        return performance_ok
        
    except Exception as e:
        print(f"❌ Performance test failed: {str(e)}")
        return False


async def run_all_tests():
    """Run all integration tests"""
    print("🧪 Universal Topic Intelligence System - Integration Tests")
    print("=" * 80)
    print("Testing complete system with Queen Agent, Architects, and Monitoring")
    print("Focused on user interests: Claude, React, TypeScript, AI Prompting\n")
    
    tests = [
        ("Component Initialization", test_component_initialization),
        ("Content Prioritization", test_content_prioritization),
        ("Single Topic Monitoring", test_single_topic_monitoring),
        ("Multi-Topic Orchestration", test_multi_topic_orchestration),
        ("Architect Coordination", test_architect_coordination),
        ("Emergency Response", test_emergency_response),
        ("System Performance", test_system_performance)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            print(f"\n{'='*80}")
            result = await test_func()
            results[test_name] = result
            await asyncio.sleep(1)  # Brief pause between tests
        except Exception as e:
            print(f"❌ Test '{test_name}' crashed: {str(e)}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    # Save test report
    report = {
        "timestamp": datetime.now().isoformat(),
        "system_version": "2.0.0",
        "tests_run": total,
        "tests_passed": passed,
        "test_results": {k: "passed" if v else "failed" for k, v in results.items()},
        "focus_topics": ["claude-ai", "react-typescript", "ai-prompting-apps"]
    }
    
    report_path = Path("integration_test_report.json")
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Test report saved to {report_path}")
    
    if passed == total:
        print("\n🎉 ALL INTEGRATION TESTS PASSED!")
        print("The Universal Topic Intelligence System is fully operational.")
        print("Ready to monitor Claude, React, TypeScript, and AI topics!")
    else:
        print(f"\n⚠️ {total - passed} test(s) failed. Review and fix issues.")
    
    return passed == total


def main():
    """Main test runner"""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        success = loop.run_until_complete(run_all_tests())
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️ Tests interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n❌ Test suite failed: {str(e)}")
        exit(1)
    finally:
        loop.close()


if __name__ == "__main__":
    main()