#!/usr/bin/env python3
"""
YouTube Dynamic Search Hook for Daily Digest Generator
Integration hook to include dynamic search results in daily digest
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any, Optional

# Add parent directory to path for imports
parent_dir = Path(__file__).parent.parent
sys.path.append(str(parent_dir))

try:
    # Try to import the integration module
    integration_file = parent_dir / "youtube-search-integration.py"
    if integration_file.exists():
        spec = __import__('importlib.util').util.spec_from_file_location(
            "youtube_search_integration", integration_file
        )
        module = __import__('importlib.util').util.module_from_spec(spec)
        spec.loader.exec_module(module)
        YouTubeSearchIntegration = module.YouTubeSearchIntegration
    else:
        raise ImportError("Integration file not found")
except ImportError as e:
    print(f"Warning: Could not import YouTube search integration: {e}")
    YouTubeSearchIntegration = None

def get_youtube_dynamic_content(max_videos: int = 15) -> Dict[str, Any]:
    """
    Get YouTube dynamic search content for digest generator
    
    Args:
        max_videos: Maximum number of videos to include
    
    Returns:
        Dictionary with dynamic search content for digest
    """
    
    if not YouTubeSearchIntegration:
        return {
            "source": "youtube_dynamic_search",
            "status": "unavailable", 
            "message": "YouTube dynamic search integration not available",
            "content": []
        }
    
    try:
        integration = YouTubeSearchIntegration()
        digest_data = integration.get_digest_compatible_data(max_videos=max_videos)
        
        if digest_data["status"] != "success":
            return {
                "source": "youtube_dynamic_search",
                "status": "no_data",
                "message": digest_data.get("message", "No dynamic search data available"),
                "content": []
            }
        
        # Transform for digest compatibility
        content_items = []
        for video in digest_data["videos"]:
            content_item = {
                "id": video["id"],
                "title": video["title"],
                "url": video["url"],
                "source": "YouTube Dynamic Search",
                "channel": video["channel"],
                "published_at": video["published_at"],
                "content_type": "video",
                "topic": video["topic"],
                "search_term": video["search_term"],
                "scores": video["scores"],
                "metadata": {
                    "view_count": video["view_count"],
                    "duration": video["duration"],
                    "thumbnail": video["thumbnail"],
                    "discovery_method": "search_based",
                    "priority_topic": video["topic"]
                },
                "description": video["description"][:200] + "..." if len(video["description"]) > 200 else video["description"],
                "relevance_score": video["scores"]["unified_score"]
            }
            content_items.append(content_item)
        
        return {
            "source": "youtube_dynamic_search",
            "status": "success",
            "content": content_items,
            "metadata": {
                "search_timestamp": digest_data.get("last_updated"),
                "total_videos_found": digest_data.get("total_videos_found", 0),
                "quality_videos_selected": digest_data.get("quality_videos_selected", 0),
                "topics_searched": list(digest_data.get("summary", {}).get("topic_distribution", {}).keys()),
                "top_channels": [ch["channel"] for ch in digest_data.get("summary", {}).get("top_channels", [])[:3]],
                "average_scores": digest_data.get("summary", {}).get("averages", {})
            },
            "summary": {
                "total_items": len(content_items),
                "high_relevance_items": len([item for item in content_items if item["relevance_score"] > 0.8]),
                "topics_covered": len(set(item["topic"] for item in content_items)),
                "description": f"Dynamic YouTube search discovered {len(content_items)} high-quality videos across priority topics"
            }
        }
        
    except Exception as e:
        return {
            "source": "youtube_dynamic_search",
            "status": "error",
            "message": f"Error retrieving dynamic search content: {str(e)}",
            "content": []
        }

def get_search_status() -> Dict[str, Any]:
    """Get status of YouTube dynamic search system"""
    
    if not YouTubeSearchIntegration:
        return {
            "system": "youtube_dynamic_search",
            "status": "unavailable",
            "message": "Integration not available"
        }
    
    try:
        integration = YouTubeSearchIntegration()
        return integration.get_status()
    except Exception as e:
        return {
            "system": "youtube_dynamic_search",
            "status": "error",
            "message": str(e)
        }

def run_dynamic_search() -> Dict[str, Any]:
    """
    Trigger a new dynamic search (for scheduled execution)
    Note: This would need the full youtube-dynamic-search.py to work
    """
    
    try:
        # This would import and run the full search system
        # For now, return a placeholder
        return {
            "status": "scheduled",
            "message": "Dynamic search would be triggered here",
            "note": "Replace with actual search execution when YouTube API is implemented"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Could not trigger dynamic search: {str(e)}"
        }

def main():
    """Test the hook functionality"""
    
    print("🔍 Testing YouTube Dynamic Search Hook")
    print("=" * 50)
    
    # Test status
    status = get_search_status()
    print(f"📊 System Status: {status.get('status', 'unknown')}")
    
    if status.get('latest_results_available'):
        print(f"📅 Last Search: {status.get('last_search', 'unknown')}")
        print(f"📺 Videos in Latest: {status.get('videos_in_latest', 0)}")
    
    # Test content retrieval
    print(f"\n🎬 Testing Content Retrieval...")
    content_data = get_youtube_dynamic_content(max_videos=5)
    
    print(f"📊 Content Status: {content_data['status']}")
    
    if content_data['status'] == 'success':
        content_items = content_data['content']
        print(f"📺 Content Items: {len(content_items)}")
        print(f"🎯 Topics Covered: {content_data['summary']['topics_covered']}")
        print(f"⭐ High Relevance Items: {content_data['summary']['high_relevance_items']}")
        
        print(f"\n🏆 Sample Content:")
        for i, item in enumerate(content_items[:3], 1):
            print(f"{i}. {item['title']}")
            print(f"   Channel: {item['channel']} | Topic: {item['topic']}")
            print(f"   Score: {item['relevance_score']:.3f}")
    else:
        print(f"❌ {content_data.get('message', 'Unknown error')}")
    
    print(f"\n✅ Hook test completed!")

if __name__ == "__main__":
    main()