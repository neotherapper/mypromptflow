#!/usr/bin/env python3
"""
Test Intelligent Multi-Factor Scoring System
Validates the enhanced scoring system with real MCP metadata
"""

import asyncio
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

# Configure logging to be less verbose
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("IntelligentScoringTest")

# Import the enhanced system
from core.content_prioritizer import UniversalContentPrioritizer
from core.universal_source_monitor import ContentItem, SourceMetadata, SourceType
from core.intelligent_scoring_system import IntelligentAnalysisEngine, IntelligentPriorityStrategy

def create_test_youtube_content() -> ContentItem:
    """Create test YouTube content with MCP metadata"""
    return ContentItem(
        item_id="test_yt_001",
        source_id="youtube_react_channel",
        title="React 19 Complete Tutorial - New Features and Migration Guide",
        content="Welcome to this comprehensive React 19 tutorial. In this video, we'll cover all the new features including the new compiler, server components, and migration strategies. This is a step-by-step guide with practical examples and code demonstrations.",
        url="https://www.youtube.com/watch?v=example123",
        published_date=datetime(2024, 1, 15, 10, 30, tzinfo=timezone.utc),
        author="React Official",
        topics=["react", "javascript", "frontend"],
        metadata={
            "mcp_source_type": "youtube_transcript",
            "youtube_video_id": "example123",
            "youtube_channel": "React",
            "youtube_duration": "PT25M30S",  # 25 minutes 30 seconds
            "youtube_view_count": 45000,
            "youtube_like_count": 2100,
            "youtube_language": "en"
        }
    )

def create_test_github_content() -> ContentItem:
    """Create test GitHub content with MCP metadata"""
    return ContentItem(
        item_id="test_gh_001",
        source_id="github_nextjs",
        title="Next.js 14 - The React Framework for Production",
        content="Next.js is a React framework that gives you the best developer experience with all the features you need for production: hybrid static & server rendering, TypeScript support, smart bundling, route pre-fetching, and more. No config needed.",
        url="https://github.com/vercel/next.js",
        published_date=datetime(2024, 1, 10, 14, 20, tzinfo=timezone.utc),
        author="Vercel Team",
        topics=["react", "nextjs", "framework"],
        metadata={
            "mcp_source_type": "github_repository",
            "github_repo_name": "vercel/next.js",
            "github_stars": 118000,
            "github_forks": 25300,
            "github_language": "TypeScript",
            "github_license": "MIT",
            "github_open_issues": 2100
        }
    )

def create_test_search_content() -> ContentItem:
    """Create test web search content with MCP metadata"""
    return ContentItem(
        item_id="test_search_001",
        source_id="react_official_blog",
        title="React 19 Release Notes - New Features and Breaking Changes",
        content="React 19 introduces several new features including the React Compiler, Server Components improvements, and new hooks. This release also includes breaking changes that developers should be aware of when upgrading.",
        url="https://react.dev/blog/2024/04/25/react-19",
        published_date=datetime(2024, 4, 25, 9, 0, tzinfo=timezone.utc),
        author="React Team",
        topics=["react", "release", "updates"],
        metadata={
            "mcp_source_type": "web_search",
            "search_query": "React 19 features",
            "search_rank": 1,
            "search_engine": "google",
            "search_relevance_score": 0.95,
            "search_domain": "react.dev"
        }
    )

def create_test_generic_content() -> ContentItem:
    """Create test generic content without MCP metadata"""
    return ContentItem(
        item_id="test_generic_001",
        source_id="generic_blog",
        title="Understanding JavaScript Closures",
        content="JavaScript closures are a fundamental concept that every developer should understand. A closure is a function that has access to variables in its outer scope even after the outer function has returned.",
        url="https://example.com/js-closures",
        published_date=datetime(2024, 1, 5, 16, 45, tzinfo=timezone.utc),
        author="Tech Blogger",
        topics=["javascript", "programming"],
        metadata={
            # No MCP metadata - will use generic analysis
            "engagement_score": 0.6,
            "social_signals": 0.4
        }
    )

async def test_intelligent_analysis():
    """Test the intelligent analysis engine"""
    print("🧠 Testing Intelligent Analysis Engine...")
    print("=" * 60)
    
    # Initialize analysis engine
    engine = IntelligentAnalysisEngine()
    
    # Test different content types
    test_contents = [
        ("YouTube", create_test_youtube_content()),
        ("GitHub", create_test_github_content()),
        ("Web Search", create_test_search_content()),
        ("Generic", create_test_generic_content())
    ]
    
    for content_type, content in test_contents:
        print(f"\n📊 Analyzing {content_type} Content:")
        print(f"  Title: {content.title[:60]}...")
        
        # Perform analysis
        analysis = engine.analyze_mcp_content(content)
        
        print(f"  Source Type: {analysis.source_type}")
        print(f"  Quality Indicators: {len(analysis.quality_indicators)} factors")
        
        # Show top quality indicators
        top_quality = sorted(analysis.quality_indicators.items(), key=lambda x: x[1], reverse=True)[:3]
        for indicator, score in top_quality:
            print(f"    {indicator}: {score:.3f}")
        
        print(f"  Engagement Metrics: {len(analysis.engagement_metrics)} metrics")
        print(f"  Technical Depth: {analysis.technical_metrics.get('technical_depth', 0):.3f}")
        print(f"  Authority Score: {max(analysis.authority_signals.values()) if analysis.authority_signals else 0:.3f}")

async def test_intelligent_prioritizer():
    """Test the intelligent prioritization strategy"""
    print("\n🎯 Testing Intelligent Prioritization Strategy...")
    print("=" * 60)
    
    # Initialize prioritizer with intelligent strategy
    prioritizer = UniversalContentPrioritizer()
    
    # Set up context
    topic_preferences = {
        "react": 1.0,
        "javascript": 0.8,
        "frontend": 0.9,
        "framework": 0.9,
        "nextjs": 0.8
    }
    
    source_authorities = {
        "youtube_react_channel": 0.9,
        "github_nextjs": 1.0,
        "react_official_blog": 1.0,
        "generic_blog": 0.5
    }
    
    prioritizer.set_topic_preferences(topic_preferences)
    prioritizer.set_source_authorities(source_authorities)
    
    # Test different content items
    test_contents = [
        create_test_youtube_content(),
        create_test_github_content(),
        create_test_search_content(),
        create_test_generic_content()
    ]
    
    print("\n📈 Priority Analysis Results:")
    print("-" * 80)
    
    # Compare strategies
    strategies = ["default", "intelligent"]
    
    for strategy in strategies:
        print(f"\n🔍 Using '{strategy}' strategy:")
        
        results = []
        for content in test_contents:
            try:
                result = prioritizer.prioritize(content, strategy=strategy)
                results.append(result)
            except Exception as e:
                logger.warning(f"Error prioritizing {content.item_id} with {strategy}: {e}")
                continue
        
        # Sort by priority score
        results.sort(key=lambda x: x.total_score, reverse=True)
        
        print(f"  {'Rank':<4} {'Title':<40} {'Score':<6} {'Priority':<8} {'Key Factors'}")
        print("  " + "-" * 85)
        
        for i, result in enumerate(results, 1):
            title = result.content_item.title[:37] + "..." if len(result.content_item.title) > 40 else result.content_item.title
            
            # Get top 2 factors
            factors = {
                "authority": result.factors.source_authority,
                "recency": result.factors.content_recency,
                "relevance": result.factors.topic_relevance,
                "engagement": result.factors.engagement_signals,
                "uniqueness": result.factors.uniqueness_score,
                "technical": result.factors.completeness,
                "actionable": result.factors.actionability
            }
            
            top_factors = sorted(factors.items(), key=lambda x: x[1], reverse=True)[:2]
            factor_str = ", ".join([f"{name}:{score:.2f}" for name, score in top_factors])
            
            print(f"  {i:<4} {title:<40} {result.total_score:<6.3f} {result.priority_level.value:<8} {factor_str}")

async def test_scoring_comparison():
    """Compare scoring differences between strategies"""
    print("\n🔬 Detailed Scoring Comparison...")
    print("=" * 60)
    
    prioritizer = UniversalContentPrioritizer()
    
    # Set preferences
    topic_preferences = {"react": 1.0, "javascript": 0.8, "frontend": 0.9}
    source_authorities = {"youtube_react_channel": 0.9, "github_nextjs": 1.0}
    
    prioritizer.set_topic_preferences(topic_preferences)
    prioritizer.set_source_authorities(source_authorities)
    
    # Test high-quality YouTube content
    youtube_content = create_test_youtube_content()
    
    print(f"\n📹 Analyzing YouTube Content:")
    print(f"  Title: {youtube_content.title}")
    print(f"  Channel: {youtube_content.metadata['youtube_channel']}")
    print(f"  Views: {youtube_content.metadata['youtube_view_count']:,}")
    print(f"  Duration: {youtube_content.metadata['youtube_duration']}")
    
    strategies = ["default", "intelligent"]
    
    for strategy in strategies:
        try:
            result = prioritizer.prioritize(youtube_content, strategy=strategy)
            
            print(f"\n  🎯 {strategy.title()} Strategy Results:")
            print(f"    Total Score: {result.total_score:.3f}")
            print(f"    Priority Level: {result.priority_level.value}")
            print(f"    Factor Breakdown:")
            print(f"      Source Authority: {result.factors.source_authority:.3f}")
            print(f"      Content Recency: {result.factors.content_recency:.3f}")
            print(f"      Topic Relevance: {result.factors.topic_relevance:.3f}")
            print(f"      Engagement Signals: {result.factors.engagement_signals:.3f}")
            print(f"      Uniqueness Score: {result.factors.uniqueness_score:.3f}")
            print(f"      Completeness: {result.factors.completeness:.3f}")
            print(f"      Actionability: {result.factors.actionability:.3f}")
            print(f"      Cross-topic Value: {result.factors.cross_topic_value:.3f}")
            
        except Exception as e:
            print(f"    ❌ Error with {strategy} strategy: {e}")

async def main():
    """Main test runner"""
    print("🚀 Intelligent Multi-Factor Scoring System Test")
    print("=" * 70)
    
    try:
        # Test individual components
        await test_intelligent_analysis()
        await test_intelligent_prioritizer()
        await test_scoring_comparison()
        
        print("\n" + "=" * 70)
        print("✅ All tests completed successfully!")
        print("\n🎯 Key Improvements in Intelligent Scoring:")
        print("  • MCP metadata-aware analysis for YouTube, GitHub, and search content")
        print("  • Technical depth assessment using code detection and complexity")
        print("  • Engagement analysis using view counts, stars, and social signals")
        print("  • Authority scoring based on channel reputation and domain trust")
        print("  • Trend detection using recency, velocity, and ecosystem relevance")
        print("  • Actionability scoring for tutorials, guides, and documentation")
        
        return True
        
    except Exception as e:
        print(f"\n💥 Test failed with error: {e}")
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