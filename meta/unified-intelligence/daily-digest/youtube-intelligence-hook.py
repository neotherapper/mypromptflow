#!/usr/bin/env python3
"""
YouTube Intelligence Hook for Daily Digest Generator
Integration hook to include historical high-value videos in daily digest
"""

import sys
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone

# Add parent directory to path for imports
parent_dir = Path(__file__).parent
sys.path.append(str(parent_dir))

try:
    # Import YouTube Intelligence System
    spec = __import__('importlib.util').util.spec_from_file_location(
        "youtube_intelligence_system", 
        parent_dir / "youtube-intelligence-system.py"
    )
    module = __import__('importlib.util').util.module_from_spec(spec)
    spec.loader.exec_module(module)
    YouTubeChannelAnalyzer = module.YouTubeChannelAnalyzer
    INTELLIGENCE_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import YouTube Intelligence System: {e}")
    YouTubeChannelAnalyzer = None
    INTELLIGENCE_AVAILABLE = False

def get_youtube_intelligence_content(max_videos: int = 10, min_score: float = 0.75) -> Dict[str, Any]:
    """
    Get high-value historical YouTube content for digest generator
    
    Args:
        max_videos: Maximum number of videos to include
        min_score: Minimum importance score for inclusion
    
    Returns:
        Dictionary with high-value content for digest
    """
    
    if not INTELLIGENCE_AVAILABLE:
        return {
            "source": "youtube_intelligence",
            "status": "unavailable", 
            "message": "YouTube Intelligence System not available",
            "content": []
        }
    
    try:
        # Initialize YouTube Intelligence System
        analyzer = YouTubeChannelAnalyzer(transcript_threshold=min_score)
        
        # Get system status first
        system_status = analyzer.get_system_status()
        
        if system_status.get("system_health") != "operational":
            return {
                "source": "youtube_intelligence",
                "status": "system_error",
                "message": "YouTube Intelligence System not operational",
                "content": []
            }
        
        # Collect high-value videos from all channels
        high_value_videos = []
        
        # Get existing video catalogs from all channels
        for channel in analyzer.channels:
            channel_id = channel.get('id')
            channel_path = analyzer.get_channel_data_path(channel_id)
            catalog_file = channel_path / "videos_catalog.json"
            
            if catalog_file.exists():
                try:
                    with open(catalog_file, 'r') as f:
                        catalog_data = json.load(f)
                    
                    # Extract high-value videos
                    for video_data in catalog_data.get('videos', []):
                        if video_data.get('importance_score', 0.0) >= min_score:
                            # Transform to digest format
                            content_item = {
                                "id": video_data['id'],
                                "title": video_data['title'],
                                "url": f"https://www.youtube.com/watch?v={video_data['id']}",
                                "source": "YouTube Intelligence",
                                "channel": video_data['channel_name'],
                                "published_at": video_data['published_at'],
                                "content_type": "video",
                                "discovery_method": "intelligence_analysis",
                                "importance_score": video_data['importance_score'],
                                "priority_topic_score": video_data.get('priority_topic_score', 0.0),
                                "has_transcript": video_data.get('has_transcript', False),
                                "transcript_extracted": video_data.get('transcript_extracted', False),
                                "metadata": {
                                    "view_count": video_data.get('view_count'),
                                    "like_count": video_data.get('like_count'),
                                    "duration": video_data.get('duration'),
                                    "thumbnail_url": video_data.get('thumbnail_url'),
                                    "source_type": video_data.get('source', 'unknown'),
                                    "last_updated": video_data.get('last_updated'),
                                    "discovery_method": "historical_analysis"
                                },
                                "description": (video_data.get('description', '')[:200] + "...") 
                                            if len(video_data.get('description', '')) > 200 
                                            else video_data.get('description', ''),
                                "relevance_score": video_data['importance_score']
                            }
                            high_value_videos.append(content_item)
                            
                except Exception as e:
                    print(f"Error reading catalog for {channel_id}: {e}")
                    continue
        
        # Sort by importance score and limit results
        high_value_videos.sort(key=lambda x: x['importance_score'], reverse=True)
        selected_videos = high_value_videos[:max_videos]
        
        # Get processed transcripts info
        processed_transcripts = []
        if analyzer.transcript_processing_enabled:
            processed_transcripts = analyzer.get_processed_transcripts(limit=5)
        
        return {
            "source": "youtube_intelligence",
            "status": "success",
            "content": selected_videos,
            "metadata": {
                "analysis_timestamp": datetime.now(timezone.utc).isoformat(),
                "total_high_value_videos": len(high_value_videos),
                "videos_selected": len(selected_videos),
                "min_score_threshold": min_score,
                "channels_analyzed": len(analyzer.channels),
                "system_status": system_status,
                "transcript_processing": {
                    "enabled": analyzer.transcript_processing_enabled,
                    "processed_count": len(processed_transcripts),
                    "threshold": analyzer.transcript_threshold
                }
            },
            "summary": {
                "total_items": len(selected_videos),
                "high_relevance_items": len([v for v in selected_videos if v['importance_score'] > 0.85]),
                "channels_represented": len(set(v['channel'] for v in selected_videos)),
                "with_transcripts": len([v for v in selected_videos if v['transcript_extracted']]),
                "description": f"Historical intelligence analysis found {len(selected_videos)} high-value videos from {len(set(v['channel'] for v in selected_videos))} channels"
            }
        }
        
    except Exception as e:
        return {
            "source": "youtube_intelligence",
            "status": "error",
            "message": f"Error retrieving intelligence content: {str(e)}",
            "content": []
        }

def get_intelligence_status() -> Dict[str, Any]:
    """Get status of YouTube Intelligence System"""
    
    if not INTELLIGENCE_AVAILABLE:
        return {
            "system": "youtube_intelligence",
            "status": "unavailable",
            "message": "System not available"
        }
    
    try:
        analyzer = YouTubeChannelAnalyzer()
        system_status = analyzer.get_system_status()
        
        # Add intelligence-specific status info
        intelligence_status = {
            "system": "youtube_intelligence",
            "status": "operational" if system_status.get("system_health") == "operational" else "degraded",
            "last_updated": system_status.get("timestamp"),
            "channels_configured": system_status.get("channel_analysis", {}).get("total_channels", 0),
            "channels_with_data": system_status.get("channel_analysis", {}).get("channels_with_data", 0),
            "total_videos_tracked": system_status.get("channel_analysis", {}).get("total_videos_tracked", 0),
            "high_value_videos": system_status.get("channel_analysis", {}).get("high_value_videos", 0),
            "api_quota": system_status.get("api_quota", {}),
            "transcript_processing": system_status.get("transcript_processing", {}),
            "data_storage": system_status.get("data_storage", {})
        }
        
        return intelligence_status
        
    except Exception as e:
        return {
            "system": "youtube_intelligence",
            "status": "error",
            "message": str(e)
        }

def run_channel_analysis(max_channels: Optional[int] = None, force_refresh: bool = False) -> Dict[str, Any]:
    """
    Trigger YouTube channel analysis (for scheduled execution)
    
    Args:
        max_channels: Maximum number of channels to analyze
        force_refresh: Force refresh of existing data
    
    Returns:
        Analysis results
    """
    
    if not INTELLIGENCE_AVAILABLE:
        return {
            "status": "error",
            "message": "YouTube Intelligence System not available"
        }
    
    try:
        analyzer = YouTubeChannelAnalyzer()
        
        print(f"🔍 Starting YouTube Intelligence analysis...")
        start_time = time.time()
        
        # Run analysis on all channels
        results = analyzer.analyze_all_channels(max_channels=max_channels)
        
        analysis_time = time.time() - start_time
        
        # Process transcript queue if enabled
        transcript_results = None
        if analyzer.transcript_processing_enabled:
            print(f"🎬 Processing transcript queue...")
            transcript_results = analyzer.process_transcript_queue(max_videos=10)
        
        return {
            "status": "success",
            "analysis_results": results,
            "transcript_results": transcript_results,
            "analysis_time": round(analysis_time, 2),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "summary": {
                "channels_analyzed": results.get("channels_analyzed", 0),
                "total_videos": results.get("total_videos_analyzed", 0),
                "high_value_videos": results.get("high_value_videos_found", 0),
                "quota_used": results.get("quota_used", 0)
            }
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Could not run channel analysis: {str(e)}"
        }

def get_channel_insights(channel_id: Optional[str] = None) -> Dict[str, Any]:
    """Get insights for specific channel or all channels"""
    
    if not INTELLIGENCE_AVAILABLE:
        return {
            "status": "error",
            "message": "YouTube Intelligence System not available"
        }
    
    try:
        analyzer = YouTubeChannelAnalyzer()
        
        if channel_id:
            # Get insights for specific channel
            result = analyzer.analyze_channel(channel_id)
            return {
                "status": "success",
                "channel_insights": {channel_id: result},
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        else:
            # Get insights for all channels
            insights = {}
            for channel in analyzer.channels:
                ch_id = channel.get('id')
                insights[ch_id] = analyzer.analyze_channel(ch_id)
            
            return {
                "status": "success",
                "channel_insights": insights,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
    except Exception as e:
        return {
            "status": "error",
            "message": f"Could not get channel insights: {str(e)}"
        }

def main():
    """Test the YouTube Intelligence hook functionality"""
    
    print("🧠 Testing YouTube Intelligence Hook")
    print("=" * 50)
    
    # Test system status
    status = get_intelligence_status()
    print(f"📊 System Status: {status.get('status', 'unknown')}")
    
    if status.get('status') == 'operational':
        print(f"📺 Channels: {status.get('channels_with_data', 0)}/{status.get('channels_configured', 0)}")
        print(f"🎬 Total Videos: {status.get('total_videos_tracked', 0)}")
        print(f"⭐ High-Value Videos: {status.get('high_value_videos', 0)}")
        
        # Test API quota
        api_quota = status.get('api_quota', {})
        if api_quota:
            print(f"🔋 API Quota: {api_quota.get('total_used', 0)}/{api_quota.get('daily_limit', 0)} ({api_quota.get('usage_percentage', 0):.1f}%)")
    
    # Test content retrieval
    print(f"\n🎬 Testing Content Retrieval...")
    content_data = get_youtube_intelligence_content(max_videos=5, min_score=0.75)
    
    print(f"📊 Content Status: {content_data['status']}")
    
    if content_data['status'] == 'success':
        content_items = content_data['content']
        metadata = content_data['metadata']
        summary = content_data['summary']
        
        print(f"📺 Content Items: {len(content_items)}")
        print(f"🏆 High Relevance: {summary['high_relevance_items']}")
        print(f"📡 Channels: {summary['channels_represented']}")
        print(f"📜 With Transcripts: {summary['with_transcripts']}")
        
        print(f"\n🎯 Sample High-Value Content:")
        for i, item in enumerate(content_items[:3], 1):
            print(f"{i}. {item['title'][:60]}...")
            print(f"   Channel: {item['channel']} | Score: {item['importance_score']:.3f}")
            print(f"   Published: {item['published_at'][:10]} | Transcript: {'✓' if item['transcript_extracted'] else '✗'}")
    else:
        print(f"❌ {content_data.get('message', 'Unknown error')}")
    
    print(f"\n✅ Hook test completed!")

if __name__ == "__main__":
    main()