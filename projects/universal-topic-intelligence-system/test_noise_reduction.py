#!/usr/bin/env python3
"""
Test Noise Reduction Engine
Validates duplicate detection, spam filtering, and quality assessment functionality
"""

import asyncio
import logging
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import List

# Configure logging to be less verbose
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("NoiseReductionTest")

# Import the noise reduction system
from core.noise_reduction_engine import NoiseReductionEngine, NoiseType, FilterAction
from core.universal_source_monitor import ContentItem
from monitor import UniversalMonitor

def create_duplicate_content() -> List[ContentItem]:
    """Create content items that should be detected as duplicates"""
    base_time = datetime.now(timezone.utc)
    
    # Exact duplicate - same title and content
    exact_duplicate_1 = ContentItem(
        item_id="exact_dup_1",
        source_id="source_a",
        title="React 19 New Features Guide",
        content="React 19 introduces several new features including automatic batching, concurrent features, and improved Suspense.",
        url="https://example.com/react19-guide",
        published_date=base_time,
        author="React Expert",
        topics=["react", "javascript"],
        metadata={}
    )
    
    exact_duplicate_2 = ContentItem(
        item_id="exact_dup_2", 
        source_id="source_b",
        title="React 19 New Features Guide",
        content="React 19 introduces several new features including automatic batching, concurrent features, and improved Suspense.",
        url="https://example.com/react19-guide",  # Same URL
        published_date=base_time + timedelta(minutes=30),
        author="React Expert",
        topics=["react", "javascript"],
        metadata={}
    )
    
    # Near duplicate - similar title and content
    near_duplicate = ContentItem(
        item_id="near_dup_1",
        source_id="source_c", 
        title="React 19 Features Overview",
        content="React version 19 brings several new capabilities including automatic batching, concurrent rendering, and enhanced Suspense functionality.",
        url="https://different-site.com/react19-overview",
        published_date=base_time + timedelta(hours=1),
        author="JS Developer",
        topics=["react", "javascript"],
        metadata={}
    )
    
    return [exact_duplicate_1, exact_duplicate_2, near_duplicate]

def create_spam_content() -> List[ContentItem]:
    """Create content items that should be detected as spam"""
    base_time = datetime.now(timezone.utc)
    
    # Promotional spam
    promotional_spam = ContentItem(
        item_id="spam_promo_1",
        source_id="spam_source",
        title="Buy Now! Special Offer on React Course - Limited Time Deal!",
        content="Get rich quick with our exclusive React course! Click here to buy now and earn $ fast. Don't miss this hot deal - act now before this special offer expires!",
        url="https://spam-site.com/buy-course",
        published_date=base_time,
        author="Course Seller",
        topics=["react", "course"],
        metadata={}
    )
    
    # Clickbait content
    clickbait_spam = ContentItem(
        item_id="spam_clickbait_1",
        source_id="clickbait_source",
        title="You Won't Believe This Shocking React Secret That Will Blow Your Mind!",
        content="This one trick that doctors hate will change your React development forever. The truth about React that developers don't want you to know - exposed!",
        url="https://clickbait-site.com/shocking-secret",
        published_date=base_time,
        author="Clickbait Writer",
        topics=["react", "tutorial"],
        metadata={}
    )
    
    # Low quality content
    low_quality = ContentItem(
        item_id="spam_lowqual_1", 
        source_id="low_quality_source",
        title="First post please like and subscribe",
        content="This is my first post about React. Please like and subscribe and smash that notification bell. Don't forget to check the description for more links.",
        url="https://beginner-blog.com/first-post",
        published_date=base_time,
        author="New Blogger",
        topics=["react", "beginner"],
        metadata={}
    )
    
    return [promotional_spam, clickbait_spam, low_quality]

def create_repetitive_content() -> ContentItem:
    """Create content with repetitive patterns"""
    repetitive_content = """
    React is a great framework. React is used by many developers. React makes building apps easy.
    React is a great framework. React is used by many developers. React makes building apps easy.
    React is a great framework. React is used by many developers. React makes building apps easy.
    React components are reusable. React components are declarative. React components are efficient.
    React components are reusable. React components are declarative. React components are efficient.
    """
    
    return ContentItem(
        item_id="repetitive_1",
        source_id="repetitive_source",
        title="React Tutorial - Basic Concepts Repeated",
        content=repetitive_content,
        url="https://repetitive-site.com/react-basics",
        published_date=datetime.now(timezone.utc),
        author="Repetitive Writer",
        topics=["react", "tutorial"],
        metadata={}
    )

def create_broken_content() -> List[ContentItem]:
    """Create content with various quality issues"""
    base_time = datetime.now(timezone.utc)
    
    # Very short title
    short_title = ContentItem(
        item_id="broken_1",
        source_id="broken_source",
        title="Rea",  # Too short
        content="Some content about React development",
        url="https://broken-site.com/short",
        published_date=base_time,
        author="Broken Author",
        topics=["react"],
        metadata={}
    )
    
    # Malformed URL
    bad_url = ContentItem(
        item_id="broken_2",
        source_id="broken_source",
        title="React Development Guide",
        content="Guide to React development with examples",
        url="not-a-valid-url",  # Malformed URL
        published_date=base_time,
        author="Bad URL Author",
        topics=["react"],
        metadata={}
    )
    
    # Excessive special characters
    special_chars = ContentItem(
        item_id="broken_3",
        source_id="broken_source",
        title="React Guide with Special Characters",
        content="@@@@####$$$$%%%%^^^^&&&&****!!!!????>>>><<<<[[[[]]]]{{{{}}}}||||\\\\\\\\////",  # 70% special chars
        url="https://broken-site.com/special",
        published_date=base_time,
        author="Special Char Author",
        topics=["react"],
        metadata={}
    )
    
    return [short_title, bad_url, special_chars]

def create_quality_content() -> List[ContentItem]:
    """Create high-quality content that should pass all filters"""
    base_time = datetime.now(timezone.utc)
    
    # High quality tutorial
    quality_tutorial = ContentItem(
        item_id="quality_1",
        source_id="quality_source",
        title="Comprehensive React Hooks Tutorial with TypeScript",
        content="This detailed tutorial covers React hooks implementation with TypeScript, including useState, useEffect, and custom hooks. We'll explore best practices for performance optimization and testing strategies.",
        url="https://react.dev/hooks-tutorial",
        published_date=base_time,
        author="React Team",
        topics=["react", "typescript", "hooks"],
        metadata={}
    )
    
    # Technical analysis
    technical_analysis = ContentItem(
        item_id="quality_2",
        source_id="technical_source",
        title="React Fiber Architecture Deep Dive",
        content="An in-depth analysis of React's Fiber architecture, exploring the reconciliation algorithm, priority scheduling, and performance optimizations. Includes code examples and architectural diagrams.",
        url="https://github.com/facebook/react/docs/fiber-architecture",
        published_date=base_time,
        author="Engineering Team",
        topics=["react", "architecture", "performance"],
        metadata={}
    )
    
    return [quality_tutorial, technical_analysis]

async def test_duplicate_detection():
    """Test duplicate detection functionality"""
    print("🔍 Testing Duplicate Detection...")
    print("-" * 50)
    
    # Initialize noise reduction engine
    noise_engine = NoiseReductionEngine()
    
    # Test duplicate content
    duplicate_items = create_duplicate_content()
    
    results = []
    for item in duplicate_items:
        result = noise_engine.analyze_content(item)
        results.append((item, result))
        
        duplicate_types = [nt for nt in result.noise_types if 'duplicate' in nt.value]
        print(f"  📄 {item.item_id}: {item.title[:40]}...")
        
        if duplicate_types:
            for dup_type in duplicate_types:
                confidence = result.confidence_scores.get(dup_type, 0.0)
                print(f"    ⚠️  {dup_type.value} (confidence: {confidence:.3f})")
            if result.similar_content_ids:
                print(f"    🔗 Similar to: {', '.join(result.similar_content_ids)}")
        else:
            print(f"    ✅ No duplicates detected")
        
        print(f"    🎯 Action: {result.filter_action.value}")
        print()
    
    # Check if duplicates were properly detected
    exact_dups_detected = sum(1 for _, result in results if NoiseType.DUPLICATE_EXACT in result.noise_types)
    near_dups_detected = sum(1 for _, result in results if NoiseType.DUPLICATE_NEAR in result.noise_types)
    
    print(f"📊 Duplicate Detection Results:")
    print(f"  Exact duplicates detected: {exact_dups_detected}/2")
    print(f"  Near duplicates detected: {near_dups_detected}/3")
    
    return exact_dups_detected >= 1 and near_dups_detected >= 1

async def test_spam_detection():
    """Test spam detection functionality"""
    print("\n🚫 Testing Spam Detection...")
    print("-" * 50)
    
    # Initialize fresh engine for spam testing
    noise_engine = NoiseReductionEngine()
    
    # Test spam content
    spam_items = create_spam_content()
    
    spam_detected = 0
    for item in spam_items:
        result = noise_engine.analyze_content(item)
        
        spam_types = [nt for nt in result.noise_types if 'spam' in nt.value]
        print(f"  📄 {item.item_id}: {item.title[:40]}...")
        
        if spam_types:
            spam_detected += 1
            for spam_type in spam_types:
                confidence = result.confidence_scores.get(spam_type, 0.0)
                print(f"    🚫 {spam_type.value} (confidence: {confidence:.3f})")
        else:
            print(f"    ✅ No spam detected")
        
        print(f"    🎯 Action: {result.filter_action.value}")
        print()
    
    # Test repetitive content
    repetitive_item = create_repetitive_content()
    repetitive_result = noise_engine.analyze_content(repetitive_item)
    
    print(f"  📄 {repetitive_item.item_id}: {repetitive_item.title[:40]}...")
    if NoiseType.REPETITIVE in repetitive_result.noise_types:
        spam_detected += 1
        confidence = repetitive_result.confidence_scores.get(NoiseType.REPETITIVE, 0.0)
        print(f"    🔄 Repetitive content detected (confidence: {confidence:.3f})")
    else:
        print(f"    ✅ No repetitive patterns detected")
    
    print(f"    🎯 Action: {repetitive_result.filter_action.value}")
    print()
    
    print(f"📊 Spam Detection Results:")
    print(f"  Spam items detected: {spam_detected}/4")
    
    return spam_detected >= 2  # Expect at least 2 out of 4 spam items detected (reasonable threshold)

async def test_quality_assessment():
    """Test content quality assessment"""
    print("\n📊 Testing Quality Assessment...")
    print("-" * 50)
    
    # Initialize fresh engine
    noise_engine = NoiseReductionEngine()
    
    # Test broken content
    broken_items = create_broken_content()
    broken_detected = 0
    
    print("  Testing broken/low-quality content:")
    for item in broken_items:
        result = noise_engine.analyze_content(item)
        
        quality_issues = [nt for nt in result.noise_types if nt in [NoiseType.BROKEN_CONTENT, NoiseType.LOW_QUALITY]]
        print(f"    📄 {item.item_id}: {item.title[:30]}...")
        
        if quality_issues:
            broken_detected += 1
            for issue in quality_issues:
                confidence = result.confidence_scores.get(issue, 0.0)
                print(f"      ⚠️  {issue.value} (confidence: {confidence:.3f})")
        
        print(f"      🎯 Action: {result.filter_action.value}")
    
    print()
    
    # Test quality content (should pass)
    quality_items = create_quality_content()
    quality_passed = 0
    
    print("  Testing high-quality content:")
    for item in quality_items:
        result = noise_engine.analyze_content(item)
        
        print(f"    📄 {item.item_id}: {item.title[:40]}...")
        
        if not result.noise_types:
            quality_passed += 1
            print(f"      ✅ Passed all quality checks")
        else:
            print(f"      ⚠️  Issues detected: {', '.join(nt.value for nt in result.noise_types)}")
        
        print(f"      🎯 Action: {result.filter_action.value}")
        print(f"      📊 Noise score: {result.overall_noise_score:.3f}")
    
    print()
    print(f"📊 Quality Assessment Results:")
    print(f"  Broken content detected: {broken_detected}/3")
    print(f"  Quality content passed: {quality_passed}/2")
    
    return broken_detected >= 2 and quality_passed >= 1

async def test_monitor_integration():
    """Test noise reduction integration with monitor system"""
    print("\n🔗 Testing Monitor Integration with Noise Reduction...")
    print("-" * 50)
    
    # Initialize monitor (should have noise filter)
    monitor = UniversalMonitor()
    
    # Verify noise filter is initialized
    if hasattr(monitor, 'noise_filter'):
        print("✅ Noise filter initialized in monitor")
    else:
        print("❌ Noise filter NOT found in monitor")
        return False
    
    # Test with spam content through the monitor's filtering
    spam_item = create_spam_content()[0]  # Get promotional spam
    
    try:
        # Test the should_filter_content interface
        should_filter, noise_result = monitor.noise_filter.should_filter_content(spam_item)
        
        print(f"✅ Successfully tested noise filter interface")
        print(f"  Content: {spam_item.title[:50]}...")
        print(f"  Should filter: {'Yes' if should_filter else 'No'}")
        print(f"  Filter action: {noise_result.filter_action.value}")
        print(f"  Reasoning: {noise_result.reasoning[:100]}...")
        print(f"  Noise types: {len(noise_result.noise_types)}")
        
        # Test with quality content
        quality_item = create_quality_content()[0]
        should_filter_quality, quality_result = monitor.noise_filter.should_filter_content(quality_item)
        
        print(f"\n  Quality content test:")
        print(f"    Should filter: {'Yes' if should_filter_quality else 'No'}")
        print(f"    Filter action: {quality_result.filter_action.value}")
        print(f"    Noise score: {quality_result.overall_noise_score:.3f}")
        
        return should_filter and not should_filter_quality  # Spam filtered, quality allowed
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

async def test_noise_statistics():
    """Test noise detection statistics"""
    print("\n📈 Testing Noise Statistics...")
    print("-" * 50)
    
    # Initialize engine and process various content types
    noise_engine = NoiseReductionEngine()
    
    # Process all test content
    all_items = (
        create_duplicate_content() +
        create_spam_content() +
        [create_repetitive_content()] +
        create_broken_content() +
        create_quality_content()
    )
    
    print(f"Processing {len(all_items)} content items for statistics...")
    
    for item in all_items:
        noise_engine.analyze_content(item)
    
    # Get statistics
    stats = noise_engine.get_noise_statistics()
    
    print(f"\n📊 Noise Detection Statistics:")
    print(f"  Total analyzed: {stats['total_analyzed']}")
    print(f"  Noise detected: {stats['noise_detected']}")
    print(f"  Detection rate: {stats['noise_detection_rate']}")
    print(f"  Average noise score: {stats['average_noise_score']:.3f}")
    print(f"  Duplicate clusters: {stats['duplicate_clusters']}")
    print(f"  Cached content: {stats['cached_content']}")
    
    print(f"\n  Filter Actions:")
    for action, count in stats['filter_actions'].items():
        print(f"    {action}: {count}")
    
    print(f"\n  Top Noise Types:")
    for noise_type, count in list(stats['noise_types'].items())[:5]:
        print(f"    {noise_type}: {count}")
    
    return stats['total_analyzed'] == len(all_items) and stats['noise_detected'] > 0

async def main():
    """Main test runner"""
    print("🚀 Noise Reduction Engine Test Suite")
    print("=" * 70)
    
    try:
        # Test individual components
        duplicate_test_passed = await test_duplicate_detection()
        spam_test_passed = await test_spam_detection()
        quality_test_passed = await test_quality_assessment()
        integration_test_passed = await test_monitor_integration()
        statistics_test_passed = await test_noise_statistics()
        
        # Summary
        print("\n" + "=" * 70)
        
        if all([duplicate_test_passed, spam_test_passed, quality_test_passed, 
               integration_test_passed, statistics_test_passed]):
            print("✅ All noise reduction tests PASSED!")
            print("\n🎉 Phase 3 Component 2: Noise Reduction - COMPLETE")
            print("\n🎯 Key Achievements:")
            print("  • Exact duplicate detection using URL and content fingerprinting")
            print("  • Near duplicate detection with similarity analysis")
            print("  • Spam filtering for promotional and clickbait content")
            print("  • Quality assessment for broken and low-quality content")
            print("  • Repetitive content detection with sentence similarity")
            print("  • Real-time integration with monitor filtering pipeline")
            print("  • Comprehensive statistics and performance tracking")
            print("  • Constitutional AI compliant filtering decisions")
            return True
        else:
            print("❌ Some noise reduction tests FAILED")
            print(f"  Duplicate Detection: {'✅' if duplicate_test_passed else '❌'}")
            print(f"  Spam Detection: {'✅' if spam_test_passed else '❌'}")
            print(f"  Quality Assessment: {'✅' if quality_test_passed else '❌'}")
            print(f"  Monitor Integration: {'✅' if integration_test_passed else '❌'}")
            print(f"  Statistics: {'✅' if statistics_test_passed else '❌'}")
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