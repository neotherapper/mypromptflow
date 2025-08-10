#!/usr/bin/env python3
"""
Test YouTube RSS Monitoring System
Tests RSS feed fetching, new video detection, and metadata extraction
"""

import json
import feedparser
import requests
from datetime import datetime, timedelta
from pathlib import Path
import time

def test_rss_feed_fetch():
    """Test RSS feed fetching for a sample channel"""
    print("🧪 Testing RSS Feed Fetching")
    print("=" * 50)
    
    # Test with Fireship channel (high activity, reliable)
    test_channels = [
        {
            "name": "Fireship",
            "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCsBjURrPoezykLs9EqgamOA",
            "channel_id": "UCsBjURrPoezykLs9EqgamOA"
        },
        {
            "name": "ThePrimeagen",
            "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UC8ENHE5xdFSwx71u3fDH5Xw",
            "channel_id": "UC8ENHE5xdFSwx71u3fDH5Xw"
        }
    ]
    
    results = []
    
    for channel in test_channels:
        print(f"\n📺 Testing channel: {channel['name']}")
        
        try:
            # Set headers to avoid blocking
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            # Fetch RSS feed
            response = requests.get(channel['rss_url'], headers=headers, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ Successfully fetched RSS feed")
                
                # Parse feed
                feed = feedparser.parse(response.content)
                
                if feed.entries:
                    print(f"📊 Found {len(feed.entries)} videos in feed")
                    
                    # Extract latest videos
                    latest_videos = []
                    for entry in feed.entries[:5]:  # Get top 5 latest
                        video_data = {
                            "video_id": entry.yt_videoid if hasattr(entry, 'yt_videoid') else entry.id,
                            "title": entry.title,
                            "url": entry.link,
                            "published": entry.published,
                            "channel": channel['name'],
                            "description": entry.summary[:200] if hasattr(entry, 'summary') else "",
                        }
                        latest_videos.append(video_data)
                        
                        # Parse published date
                        from email.utils import parsedate_to_datetime
                        pub_date = parsedate_to_datetime(entry.published)
                        days_ago = (datetime.now(pub_date.tzinfo) - pub_date).days
                        
                        print(f"  • {entry.title[:50]}... ({days_ago} days ago)")
                    
                    results.append({
                        "channel": channel['name'],
                        "status": "success",
                        "video_count": len(feed.entries),
                        "latest_videos": latest_videos
                    })
                else:
                    print(f"⚠️ Feed parsed but no entries found")
                    results.append({
                        "channel": channel['name'],
                        "status": "empty",
                        "video_count": 0
                    })
            else:
                print(f"❌ Failed to fetch RSS feed: HTTP {response.status_code}")
                results.append({
                    "channel": channel['name'],
                    "status": "failed",
                    "error": f"HTTP {response.status_code}"
                })
                
        except Exception as e:
            print(f"❌ Error fetching RSS feed: {str(e)}")
            results.append({
                "channel": channel['name'],
                "status": "error",
                "error": str(e)
            })
        
        # Small delay between requests
        time.sleep(2)
    
    return results

def test_new_video_detection():
    """Test detection of new videos since last check"""
    print("\n🔍 Testing New Video Detection")
    print("=" * 50)
    
    # Load existing state
    state_file = Path("youtube-monitor-state.json")
    
    if state_file.exists():
        with open(state_file, 'r') as f:
            state = json.load(f)
            print(f"📋 Loaded existing state with {len(state)} channels")
            
            # Check for new videos
            for channel_id, channel_state in state.items():
                if 'last_video_id' in channel_state:
                    last_checked = channel_state.get('last_checked', 'unknown')
                    print(f"  • Channel {channel_id[:20]}... last checked: {last_checked}")
    else:
        print("⚠️ No existing state file found")
        state = {}
    
    return state

def test_metadata_extraction():
    """Test extraction of video metadata from RSS entries"""
    print("\n📝 Testing Metadata Extraction")
    print("=" * 50)
    
    # Use a test RSS URL
    test_url = "https://www.youtube.com/feeds/videos.xml?channel_id=UCsBjURrPoezykLs9EqgamOA"
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(test_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            feed = feedparser.parse(response.content)
            
            if feed.entries:
                # Test metadata extraction on first entry
                entry = feed.entries[0]
                
                print(f"🎬 Testing metadata for: {entry.title}")
                
                # Extract all available metadata
                metadata = {
                    "video_id": getattr(entry, 'yt_videoid', None),
                    "channel_id": getattr(entry, 'yt_channelid', None),
                    "title": entry.title,
                    "link": entry.link,
                    "published": entry.published,
                    "author": getattr(entry, 'author', None),
                    "summary": getattr(entry, 'summary', '')[:200],
                    "media_thumbnail": None,
                    "media_statistics": None
                }
                
                # Check for media namespace elements
                if hasattr(entry, 'media_thumbnail'):
                    metadata['media_thumbnail'] = entry.media_thumbnail[0]['url'] if entry.media_thumbnail else None
                
                if hasattr(entry, 'media_statistics'):
                    metadata['media_statistics'] = {
                        'views': getattr(entry.media_statistics, 'views', None)
                    }
                
                # Print extracted metadata
                for key, value in metadata.items():
                    if value:
                        display_value = str(value)[:100] if len(str(value)) > 100 else value
                        print(f"  • {key}: {display_value}")
                
                return metadata
            else:
                print("❌ No entries in feed")
                return None
        else:
            print(f"❌ Failed to fetch feed: HTTP {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def test_queue_integration():
    """Test integration with processing queue"""
    print("\n🔗 Testing Queue Integration")
    print("=" * 50)
    
    queue_file = Path("transcript-processing-queue.json")
    
    if queue_file.exists():
        with open(queue_file, 'r') as f:
            queue = json.load(f)
            
        # Analyze queue
        total = len(queue)
        pending = len([v for v in queue if v.get('status') == 'pending'])
        completed = len([v for v in queue if v.get('status') in ['completed', 'completed_test']])
        error = len([v for v in queue if v.get('status') == 'error'])
        
        print(f"📊 Queue Statistics:")
        print(f"  • Total videos: {total}")
        print(f"  • Pending: {pending}")
        print(f"  • Completed: {completed}")
        print(f"  • Errors: {error}")
        
        # Check channels in queue
        channels = {}
        for video in queue:
            channel = video.get('channel', 'Unknown')
            channels[channel] = channels.get(channel, 0) + 1
        
        print(f"\n📺 Videos by Channel:")
        for channel, count in sorted(channels.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"  • {channel}: {count} videos")
        
        return {"total": total, "pending": pending, "completed": completed, "error": error}
    else:
        print("⚠️ No processing queue found")
        return None

def main():
    """Run all tests"""
    print("🚀 YouTube RSS Monitoring System Test Suite")
    print("=" * 50)
    
    # Test 1: RSS Feed Fetching
    rss_results = test_rss_feed_fetch()
    
    # Test 2: New Video Detection
    state = test_new_video_detection()
    
    # Test 3: Metadata Extraction
    metadata = test_metadata_extraction()
    
    # Test 4: Queue Integration
    queue_stats = test_queue_integration()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    
    success_count = len([r for r in rss_results if r['status'] == 'success'])
    print(f"✅ RSS Feeds Working: {success_count}/{len(rss_results)}")
    
    if metadata:
        print(f"✅ Metadata Extraction: Working")
    else:
        print(f"❌ Metadata Extraction: Failed")
    
    if queue_stats:
        print(f"✅ Queue Integration: {queue_stats['pending']} videos pending")
    else:
        print(f"⚠️ Queue Integration: No queue found")
    
    # Save test results
    test_results = {
        "timestamp": datetime.now().isoformat(),
        "rss_feeds": rss_results,
        "metadata_test": metadata is not None,
        "queue_stats": queue_stats,
        "state_channels": len(state)
    }
    
    with open("test_results_rss_monitoring.json", 'w') as f:
        json.dump(test_results, f, indent=2)
    
    print(f"\n💾 Test results saved to test_results_rss_monitoring.json")
    print("✅ Testing completed!")

if __name__ == "__main__":
    main()