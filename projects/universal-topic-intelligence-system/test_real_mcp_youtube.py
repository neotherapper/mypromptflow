#!/usr/bin/env python3
"""
Test Real MCP YouTube Integration
Test with actual videos from React topic configuration
"""

import asyncio
import logging
from sources.real_mcp_integration import RealMCPIntegration
from core import SourceMetadata, SourceType

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def test_react_youtube_videos():
    """Test YouTube integration with React ecosystem videos"""
    print("🧪 Testing Real YouTube MCP Integration with React Videos...")
    
    # Create MCP integration instance
    mcp_integration = RealMCPIntegration()
    
    # Test videos from React ecosystem configuration
    react_videos = [
        "https://www.youtube.com/watch?v=8pDqJVdNa44",  # React documentary
        "https://www.youtube.com/watch?v=N3AkSS5hXMA",  # React explained
    ]
    
    print(f"\n📹 Testing with {len(react_videos)} React videos...")
    
    try:
        # Extract transcripts using real MCP integration
        youtube_items = await mcp_integration.extract_youtube_transcripts(react_videos, max_videos=2)
        
        print(f"\n✅ YouTube MCP Integration Results:")
        print(f"   📊 Extracted {len(youtube_items)} transcripts")
        
        for item in youtube_items:
            print(f"\n   📹 Video: {item.title}")
            print(f"      🆔 ID: {item.item_id}")
            print(f"      🔗 URL: {item.url}")
            print(f"      👤 Author: {item.author}")
            print(f"      📝 Content Length: {len(item.content)} characters")
            print(f"      🏷️  Topics: {', '.join(item.topics)}")
            print(f"      📊 Metadata: {item.metadata}")
            
            # Show first 200 characters of transcript
            if len(item.content) > 200:
                print(f"      📄 Preview: {item.content[:200]}...")
            else:
                print(f"      📄 Content: {item.content}")
        
        print(f"\n🎉 Real YouTube MCP Integration Test Complete!")
        return youtube_items
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return []

async def test_github_integration():
    """Test GitHub integration with React repositories"""
    print("\n🐙 Testing GitHub MCP Integration with React Repos...")
    
    mcp_integration = RealMCPIntegration()
    
    react_queries = [
        "facebook/react",
        "vercel/next.js",
        "remix-run/remix"
    ]
    
    try:
        github_items = await mcp_integration.search_github_repositories(react_queries, max_results=2)
        
        print(f"\n✅ GitHub MCP Integration Results:")
        print(f"   📊 Found {len(github_items)} repositories")
        
        for item in github_items:
            print(f"\n   🐙 Repository: {item.title}")
            print(f"      🆔 ID: {item.item_id}")
            print(f"      🔗 URL: {item.url}")
            print(f"      ⭐ Stars: {item.metadata.get('stars', 'N/A')}")
            print(f"      🍴 Language: {item.metadata.get('language', 'N/A')}")
            print(f"      📝 Content: {item.content[:150]}...")
        
        print(f"\n🎉 GitHub MCP Integration Test Complete!")
        return github_items
        
    except Exception as e:
        print(f"❌ GitHub test failed: {e}")
        return []

async def main():
    """Run all MCP integration tests"""
    print("🚀 Starting Comprehensive MCP Integration Tests...\n")
    
    # Test YouTube integration
    youtube_results = await test_react_youtube_videos()
    
    # Test GitHub integration
    github_results = await test_github_integration()
    
    # Summary
    print(f"\n📊 Test Summary:")
    print(f"   📹 YouTube Items: {len(youtube_results)}")
    print(f"   🐙 GitHub Items: {len(github_results)}")
    print(f"   📈 Total Items: {len(youtube_results) + len(github_results)}")
    
    if youtube_results and github_results:
        print(f"\n✅ All MCP Integration Tests PASSED!")
        return True
    else:
        print(f"\n❌ Some MCP Integration Tests FAILED!")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)