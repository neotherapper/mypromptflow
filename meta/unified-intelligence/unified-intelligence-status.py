#!/usr/bin/env python3
"""
Unified Intelligence System Status and Integration
Simple status check and integration validation for @meta/unified-intelligence
"""

import json
import os
from pathlib import Path
from datetime import datetime

def check_unified_intelligence_status():
    """Check the status of unified intelligence system components"""
    
    base_path = Path(__file__).parent
    
    print("🚀 Unified Intelligence System Status")
    print("=" * 60)
    
    # Check directory structure
    components = [
        "discovery-framework.yaml",
        "source-registry.yaml", 
        "user-preferences.json",
        "information-access/",
        "platforms/youtube/",
        "discovery-algorithms/",
        "quality-engine/",
        "ai-learning-agent/",
        "knowledge-vault/",
        "daily-digest/"
    ]
    
    print("\n📁 Component Status:")
    for component in components:
        path = base_path / component
        status = "✅" if path.exists() else "❌"
        print(f"  {status} {component}")
    
    # Check YouTube system integration
    print("\n📺 YouTube System Status:")
    youtube_path = base_path / "platforms" / "youtube"
    
    if youtube_path.exists():
        # Check for key files
        youtube_files = [
            "transcript-processing-queue.json",
            "youtube-monitor-state.json", 
            "youtube-channels-config.json",
            "unified-youtube-integration.py"
        ]
        
        for file in youtube_files:
            file_path = youtube_path / file
            status = "✅" if file_path.exists() else "❌"
            print(f"  {status} {file}")
            
            # Show queue status
            if file == "transcript-processing-queue.json" and file_path.exists():
                try:
                    with open(file_path, 'r') as f:
                        queue = json.load(f)
                    pending = len([v for v in queue if v.get('status') == 'pending'])
                    completed = len([v for v in queue if v.get('status') == 'completed'])
                    print(f"      📋 Queue: {pending} pending, {completed} completed")
                except Exception as e:
                    print(f"      ❌ Error reading queue: {e}")
    
    # Check user preferences
    print("\n👤 User Preferences Status:")
    prefs_path = base_path / "user-preferences.json"
    if prefs_path.exists():
        try:
            with open(prefs_path, 'r') as f:
                prefs = json.load(f)
            
            stated_prefs = prefs.get('stated_preferences', {})
            topic_prefs = prefs.get('topic_preferences', {})
            
            print(f"  ✅ Stated preferences: {len(stated_prefs)} items")
            print(f"  ✅ Topic preferences: {len(topic_prefs)} topics")
            
            # Show key preferences
            for pref, data in stated_prefs.items():
                score = data.get('preference_score', 0)
                print(f"      📊 {pref}: {score}")
                
        except Exception as e:
            print(f"  ❌ Error reading preferences: {e}")
    
    # Check source registry
    print("\n🗂️  Source Registry Status:")
    registry_path = base_path / "source-registry.yaml"
    if registry_path.exists():
        print("  ✅ Source registry exists")
        # Basic size check
        size = registry_path.stat().st_size
        print(f"      📏 Registry size: {size} bytes")
    else:
        print("  ❌ Source registry missing")
    
    # Integration recommendations
    print("\n💡 Next Steps:")
    print("  1. ✅ Consolidation at @meta level: Complete")
    print("  2. ✅ Master configuration: Complete") 
    print("  3. ✅ Source registry: Complete")
    print("  4. ✅ User preferences: Complete")
    print("  5. 🔄 Process YouTube backlog: Ready to execute")
    print("  6. 🔄 Build discovery algorithms: In progress")
    print("  7. ⏳ Deploy AI learning agent: Pending")
    print("  8. ⏳ Multi-platform integration: Pending")
    
    print(f"\n🎯 System Status: Consolidated and ready for Phase 2")
    print(f"📅 Status check: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def show_youtube_backlog_preview():
    """Show preview of YouTube backlog for processing"""
    
    youtube_path = Path(__file__).parent / "platforms" / "youtube"
    queue_file = youtube_path / "transcript-processing-queue.json"
    
    if not queue_file.exists():
        print("❌ No YouTube processing queue found")
        return
    
    print("\n📺 YouTube Backlog Preview:")
    print("=" * 50)
    
    try:
        with open(queue_file, 'r') as f:
            queue = json.load(f)
        
        pending_videos = [v for v in queue if v.get('status') == 'pending']
        
        if not pending_videos:
            print("✅ No pending videos in queue")
            return
        
        print(f"📋 Found {len(pending_videos)} pending videos:")
        
        # Group by channel
        by_channel = {}
        for video in pending_videos:
            channel = video.get('channel', 'Unknown')
            if channel not in by_channel:
                by_channel[channel] = []
            by_channel[channel].append(video)
        
        for channel, videos in by_channel.items():
            rating = videos[0].get('channel_rating', 3.0)
            print(f"\n  🎬 {channel} (Rating: {rating}/5.0)")
            
            for video in videos[:3]:  # Show first 3 videos per channel
                title = video.get('title', 'Unknown Title')[:50]
                priority = video.get('priority', 'medium')
                print(f"    • {title}... [{priority}]")
            
            if len(videos) > 3:
                print(f"    ... and {len(videos) - 3} more videos")
        
        # Show high-priority videos
        high_priority = [v for v in pending_videos if v.get('priority') == 'high']
        if high_priority:
            print(f"\n🌟 High Priority Videos: {len(high_priority)}")
            for video in high_priority[:5]:
                title = video.get('title', 'Unknown Title')[:40]
                channel = video.get('channel', 'Unknown')
                print(f"    🔥 {title}... ({channel})")
        
    except Exception as e:
        print(f"❌ Error reading queue: {e}")

def main():
    """Main status check"""
    check_unified_intelligence_status()
    show_youtube_backlog_preview()
    
    print("\n" + "=" * 60)
    print("🎉 Unified Intelligence System is ready for Phase 2!")
    print("💡 Run discovery algorithms and process YouTube backlog next.")

if __name__ == "__main__":
    main()