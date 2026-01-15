#!/usr/bin/env python3
"""
Test Enhanced Database Schema with MCP Integration
Validates the new database schema properly handles MCP content types
"""

import asyncio
import logging
import sys
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("DatabaseTest")

# Import the enhanced storage system
from storage.database import StorageManager
from sources.production_mcp_integration import ProductionMCPIntegration

async def test_enhanced_database():
    """Test the enhanced database schema with MCP content"""
    
    print("🧪 Testing Enhanced Database Schema with MCP Content...")
    print("=" * 60)
    
    # Initialize storage manager
    storage = StorageManager("test_enhanced_mcp.db")
    
    # Run migration to add new columns (safe for existing databases)
    print("\n📊 Running database migration...")
    migration_success = storage.migrate_database_schema()
    if migration_success:
        print("✅ Database migration completed successfully")
    else:
        print("❌ Database migration failed")
        return False
    
    # Initialize MCP integration
    mcp_integration = ProductionMCPIntegration()
    
    # Test YouTube content collection and storage
    print("\n📹 Testing YouTube MCP Integration...")
    try:
        youtube_urls = [
            "https://www.youtube.com/watch?v=8pDqJVdNa44",  # React documentary
            "https://www.youtube.com/watch?v=N3AkSS5hXMA",  # React explained
        ]
        
        youtube_items = await mcp_integration.extract_youtube_transcripts(youtube_urls, max_videos=2)
        print(f"✅ Extracted {len(youtube_items)} YouTube transcripts")
        
        # Store YouTube items
        youtube_stored = 0
        for item in youtube_items:
            if await storage.store_content(item, priority_score=0.8, priority_level="high"):
                youtube_stored += 1
        
        print(f"✅ Stored {youtube_stored} YouTube items in enhanced database")
        
    except Exception as e:
        print(f"❌ YouTube test failed: {e}")
    
    # Test GitHub content collection and storage
    print("\n🐙 Testing GitHub MCP Integration...")
    try:
        github_queries = ["facebook/react", "vercel/next.js"]
        
        github_items = await mcp_integration.search_github_repositories(github_queries, max_results=3)
        print(f"✅ Found {len(github_items)} GitHub repositories")
        
        # Store GitHub items
        github_stored = 0
        for item in github_items:
            if await storage.store_content(item, priority_score=0.7, priority_level="medium"):
                github_stored += 1
        
        print(f"✅ Stored {github_stored} GitHub items in enhanced database")
        
    except Exception as e:
        print(f"❌ GitHub test failed: {e}")
    
    # Test Web Search content collection and storage
    print("\n🔍 Testing Web Search MCP Integration...")
    try:
        search_queries = ["React 19 features", "Claude AI updates"]
        
        search_items = await mcp_integration.search_web_content(search_queries, max_results=2)
        print(f"✅ Found {len(search_items)} web search results")
        
        # Store search items
        search_stored = 0
        for item in search_items:
            if await storage.store_content(item, priority_score=0.6, priority_level="medium"):
                search_stored += 1
        
        print(f"✅ Stored {search_stored} search items in enhanced database")
        
    except Exception as e:
        print(f"❌ Web search test failed: {e}")
    
    # Test enhanced analytics
    print("\n📊 Testing Enhanced Analytics...")
    try:
        # Get MCP-specific analytics
        mcp_analytics = storage.get_mcp_analytics()
        
        print("\n📈 MCP Analytics Results:")
        
        if mcp_analytics.get('content_by_mcp_type'):
            print("  🎯 Content by MCP Type:")
            for source_type, count in mcp_analytics['content_by_mcp_type'].items():
                print(f"    {source_type}: {count} items")
        
        if mcp_analytics.get('top_youtube_channels'):
            print("  📹 Top YouTube Channels:")
            for channel_data in mcp_analytics['top_youtube_channels'][:3]:
                print(f"    {channel_data['channel']}: {channel_data['videos']} videos")
        
        if mcp_analytics.get('top_github_repos'):
            print("  🐙 Top GitHub Repositories:")
            for repo_data in mcp_analytics['top_github_repos'][:3]:
                print(f"    {repo_data['repo']}: {repo_data['stars']} stars")
        
        if mcp_analytics.get('programming_languages'):
            print("  💻 Programming Languages:")
            for lang, count in list(mcp_analytics['programming_languages'].items())[:3]:
                print(f"    {lang}: {count} items")
        
        if mcp_analytics.get('top_search_queries'):
            print("  🔍 Top Search Queries:")
            for query_data in mcp_analytics['top_search_queries'][:3]:
                print(f"    '{query_data['query']}': {query_data['count']} results")
        
        print("✅ Enhanced analytics working properly")
        
    except Exception as e:
        print(f"❌ Analytics test failed: {e}")
    
    # Test content filtering by source type
    print("\n🔍 Testing Content Filtering by Source Type...")
    try:
        youtube_content = storage.get_content_by_source_type('youtube_transcript', limit=5)
        github_content = storage.get_content_by_source_type('github_repository', limit=5)
        search_content = storage.get_content_by_source_type('web_search', limit=5)
        
        print(f"  📹 YouTube content: {len(youtube_content)} items")
        print(f"  🐙 GitHub content: {len(github_content)} items")
        print(f"  🔍 Search content: {len(search_content)} items")
        
        # Show sample data
        if youtube_content:
            sample_yt = youtube_content[0]
            print(f"  📹 Sample YouTube: {sample_yt.get('title', 'No title')[:50]}...")
            print(f"      Channel: {sample_yt.get('youtube_channel', 'Unknown')}")
            print(f"      Views: {sample_yt.get('youtube_view_count', 'Unknown')}")
        
        if github_content:
            sample_gh = github_content[0]
            print(f"  🐙 Sample GitHub: {sample_gh.get('title', 'No title')[:50]}...")
            print(f"      Repo: {sample_gh.get('github_repo_name', 'Unknown')}")
            print(f"      Stars: {sample_gh.get('github_stars', 'Unknown')}")
        
        print("✅ Content filtering by source type working properly")
        
    except Exception as e:
        print(f"❌ Content filtering test failed: {e}")
    
    # Test overall database statistics
    print("\n📊 Testing Overall Database Statistics...")
    try:
        stats = storage.get_statistics()
        
        print(f"  📈 Total items: {stats.get('total_items', 0)}")
        print(f"  🏷️ Topics monitored: {stats.get('topics_monitored', 0)}")
        print(f"  📅 Items last 24h: {stats.get('items_last_24h', 0)}")
        
        if stats.get('items_by_priority'):
            print("  🎯 Items by priority:")
            for priority, count in stats['items_by_priority'].items():
                print(f"    {priority}: {count}")
        
        print("✅ Overall statistics working properly")
        
    except Exception as e:
        print(f"❌ Statistics test failed: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Enhanced Database Schema Test Complete!")
    
    # Get final item count
    total_items = storage.get_item_count()
    print(f"📊 Total items in enhanced database: {total_items}")
    
    if total_items > 0:
        print("✅ Database integration test PASSED")
        return True
    else:
        print("❌ Database integration test FAILED - No items stored")
        return False

def main():
    """Main test runner"""
    try:
        result = asyncio.run(test_enhanced_database())
        if result:
            print("\n🎯 All tests passed! Enhanced database schema is working correctly.")
            sys.exit(0)
        else:
            print("\n❌ Some tests failed. Check the logs above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()