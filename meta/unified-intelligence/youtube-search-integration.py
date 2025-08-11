#!/usr/bin/env python3
"""
YouTube Dynamic Search Integration
Integration layer for the digest generator to use YouTube dynamic search results
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

class YouTubeSearchIntegration:
    """Integration layer for YouTube dynamic search with digest generator"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.results_dir = self._get_results_directory()
    
    def _get_results_directory(self) -> Path:
        """Get the results directory path"""
        main_knowledge_vault = self.base_path.parent.parent / "knowledge-vault" / "databases" / "knowledge_vault" / "content-intelligence"
        return main_knowledge_vault / "youtube-intelligence" / "dynamic-search"
    
    def get_latest_search_results(self) -> Optional[Dict[str, Any]]:
        """Get the latest dynamic search results"""
        latest_file = self.results_dir / "latest_dynamic_search.json"
        
        if not latest_file.exists():
            return None
        
        try:
            with open(latest_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading latest search results: {e}")
            return None
    
    def get_daily_search_results(self, date: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get search results for a specific date"""
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        daily_file = self.results_dir / "daily" / f"dynamic_search_{date}.json"
        
        if not daily_file.exists():
            return None
        
        try:
            with open(daily_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading daily search results for {date}: {e}")
            return None
    
    def get_topic_results(self, topic: str, date: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get search results for a specific topic"""
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        
        topic_file = self.results_dir / "by-topic" / f"{topic}_{date}.json"
        
        if not topic_file.exists():
            return None
        
        try:
            with open(topic_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading topic results for {topic} on {date}: {e}")
            return None
    
    def get_digest_compatible_data(self, max_videos: int = 20) -> Dict[str, Any]:
        """Get data formatted for digest generator compatibility"""
        latest_results = self.get_latest_search_results()
        
        if not latest_results:
            return {
                "status": "no_data",
                "message": "No dynamic search results available",
                "videos": []
            }
        
        # Extract top videos with digest-compatible format
        top_videos = latest_results.get("top_videos", [])[:max_videos]
        
        digest_videos = []
        for video in top_videos:
            digest_video = {
                "id": video["video_id"],
                "title": video["title"],
                "channel": video["channel_name"],
                "url": f"https://youtube.com/watch?v={video['video_id']}",
                "published_at": video["published_at"],
                "view_count": video["view_count"],
                "duration": video["duration"],
                "description": video["description"],
                "thumbnail": video["thumbnail_url"],
                "topic": video["priority_topic"],
                "search_term": video["search_term"],
                "scores": {
                    "unified_score": video["unified_score"],
                    "relevance_score": video["relevance_score"],
                    "engagement_score": video["engagement_score"],
                    "freshness_score": video["freshness_score"]
                },
                "source_type": "dynamic_search",
                "discovery_method": "search_based"
            }
            digest_videos.append(digest_video)
        
        # Create summary for digest
        summary_stats = latest_results.get("summary_statistics", {})
        
        return {
            "status": "success",
            "search_metadata": latest_results.get("search_metadata", {}),
            "total_videos_found": latest_results.get("search_metadata", {}).get("total_videos_found", 0),
            "quality_videos_selected": len(digest_videos),
            "videos": digest_videos,
            "summary": {
                "averages": summary_stats.get("averages", {}),
                "topic_distribution": summary_stats.get("topic_distribution", {}),
                "top_channels": summary_stats.get("top_channels", [])[:5],
                "quality_metrics": summary_stats.get("quality_metrics", {})
            },
            "last_updated": latest_results.get("search_metadata", {}).get("timestamp")
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get status of dynamic search system"""
        status = {
            "system": "youtube_dynamic_search",
            "status": "operational",
            "results_directory": str(self.results_dir),
            "directory_exists": self.results_dir.exists(),
            "latest_results_available": (self.results_dir / "latest_dynamic_search.json").exists(),
            "subdirectories": {
                "daily": (self.results_dir / "daily").exists(),
                "by-topic": (self.results_dir / "by-topic").exists(), 
                "summaries": (self.results_dir / "summaries").exists()
            }
        }
        
        # Check for recent results
        latest_file = self.results_dir / "latest_dynamic_search.json"
        if latest_file.exists():
            try:
                with open(latest_file, 'r') as f:
                    latest_data = json.load(f)
                    status["last_search"] = latest_data.get("search_metadata", {}).get("timestamp")
                    status["videos_in_latest"] = latest_data.get("search_metadata", {}).get("quality_videos_selected", 0)
            except Exception:
                status["last_search"] = "unknown"
                status["videos_in_latest"] = 0
        
        return status


def create_sample_data():
    """Create sample data for testing the integration"""
    integration = YouTubeSearchIntegration()
    
    # Create sample search results
    sample_results = {
        "search_metadata": {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "framework_version": "1.0.0",
            "search_type": "dynamic_youtube_search",
            "topics_searched": ["claude", "react", "typescript"],
            "total_search_terms": 6,
            "total_videos_found": 15,
            "quality_videos_selected": 10
        },
        "search_configuration": {
            "filters": {
                "published_after_days": 30,
                "min_view_count": 100,
                "min_duration_seconds": 120,
                "max_duration_seconds": 3600
            },
            "thresholds": {
                "min_relevance_score": 0.6,
                "min_engagement_score": 0.4,
                "min_unified_score": 0.5
            }
        },
        "top_videos": [
            {
                "video_id": "sample_video_1",
                "title": "Claude AI Advanced Tutorial 2024",
                "channel_name": "AI Development Channel",
                "channel_id": "UC_sample_channel_1",
                "published_at": "2024-07-15T10:00:00Z",
                "view_count": 5000,
                "duration": "PT15M30S",
                "description": "Learn advanced Claude AI techniques for developers...",
                "thumbnail_url": "https://example.com/thumbnail1.jpg",
                "search_term": "Claude AI tutorial",
                "priority_topic": "claude",
                "relevance_score": 0.85,
                "freshness_score": 0.9,
                "engagement_score": 0.75,
                "unified_score": 0.85
            },
            {
                "video_id": "sample_video_2", 
                "title": "React TypeScript Best Practices",
                "channel_name": "React Experts",
                "channel_id": "UC_sample_channel_2",
                "published_at": "2024-07-20T14:30:00Z",
                "view_count": 3200,
                "duration": "PT12M45S",
                "description": "Modern React with TypeScript patterns and practices...",
                "thumbnail_url": "https://example.com/thumbnail2.jpg",
                "search_term": "React TypeScript tutorial",
                "priority_topic": "react",
                "relevance_score": 0.80,
                "freshness_score": 0.95,
                "engagement_score": 0.70,
                "unified_score": 0.82
            }
        ],
        "summary_statistics": {
            "averages": {
                "unified_score": 0.835,
                "relevance_score": 0.825,
                "engagement_score": 0.725,
                "freshness_score": 0.925
            },
            "topic_distribution": {
                "claude": {"total_videos": 5, "avg_score": 0.82},
                "react": {"total_videos": 3, "avg_score": 0.78},
                "typescript": {"total_videos": 2, "avg_score": 0.75}
            },
            "top_channels": [
                {"channel": "AI Development Channel", "video_count": 3},
                {"channel": "React Experts", "video_count": 2}
            ],
            "quality_metrics": {
                "high_relevance_videos": 8,
                "high_engagement_videos": 6,
                "fresh_videos": 9
            }
        }
    }
    
    # Ensure directory exists
    integration.results_dir.mkdir(parents=True, exist_ok=True)
    
    # Save sample data
    latest_file = integration.results_dir / "latest_dynamic_search.json"
    with open(latest_file, 'w') as f:
        json.dump(sample_results, f, indent=2)
    
    print(f"✅ Created sample data at: {latest_file}")
    return sample_results


def main():
    """Main function for testing the integration"""
    print("🚀 YouTube Dynamic Search Integration Test")
    print("=" * 50)
    
    integration = YouTubeSearchIntegration()
    
    # Check status
    status = integration.get_status()
    print(f"📊 System Status: {status['status']}")
    print(f"📁 Results Directory: {status['results_directory']}")
    print(f"📂 Directory Exists: {status['directory_exists']}")
    
    # If no data exists, create sample data
    if not status['latest_results_available']:
        print("\n📝 No existing data found, creating sample data...")
        create_sample_data()
        status = integration.get_status()
    
    # Test getting digest-compatible data
    print(f"\n🔄 Testing digest compatibility...")
    digest_data = integration.get_digest_compatible_data(max_videos=5)
    
    print(f"📊 Digest Data Status: {digest_data['status']}")
    if digest_data['status'] == 'success':
        print(f"📺 Videos Available: {digest_data['quality_videos_selected']}")
        print(f"🎯 Topics Covered: {list(digest_data['summary']['topic_distribution'].keys())}")
        
        # Show sample videos
        print(f"\n🏆 Sample Videos:")
        for i, video in enumerate(digest_data['videos'][:3], 1):
            print(f"{i}. {video['title']} ({video['channel']})")
            print(f"   Score: {video['scores']['unified_score']:.3f} | Topic: {video['topic']}")
    
    print(f"\n✅ Integration test completed!")


if __name__ == "__main__":
    main()