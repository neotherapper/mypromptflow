#!/usr/bin/env python3
"""
Test Unified Processing - Process one video to validate integration
"""

import json
import os
from pathlib import Path
from datetime import datetime, timezone
import subprocess

def test_process_one_video():
    """Test processing one video with unified intelligence framework"""
    
    base_path = Path(__file__).parent
    youtube_path = base_path / "platforms" / "youtube"
    queue_file = youtube_path / "transcript-processing-queue.json"
    
    print("🧪 Testing Unified Intelligence Processing")
    print("=" * 50)
    
    # Load the queue
    if not queue_file.exists():
        print("❌ Processing queue not found")
        return
    
    with open(queue_file, 'r') as f:
        queue = json.load(f)
    
    # Find a high-priority pending video
    pending_videos = [v for v in queue if v.get('status') == 'pending']
    high_priority = [v for v in pending_videos if v.get('priority') == 'high']
    
    if not high_priority:
        print("❌ No high-priority videos found for testing")
        return
    
    # Select the first high-priority video
    test_video = high_priority[0]
    
    print(f"🎯 Selected for testing:")
    print(f"   Title: {test_video['title']}")
    print(f"   Channel: {test_video['channel']}")
    print(f"   Priority: {test_video['priority']}")
    print(f"   Rating: {test_video['channel_rating']}")
    
    # Calculate unified score using the preferences
    unified_score = calculate_unified_score(test_video, base_path)
    
    print(f"\n📊 Unified Intelligence Scoring:")
    print(f"   Channel Rating: {test_video['channel_rating']}/5.0")
    print(f"   User Preference: {get_user_preference(test_video['channel'], base_path)}")
    print(f"   Unified Score: {unified_score:.3f}")
    
    # Test transcript extraction
    print(f"\n🎬 Testing transcript extraction...")
    video_url = test_video['video_url']
    
    try:
        # Use Claude Code to extract transcript
        transcript_prompt = f"""
        Extract the transcript from this YouTube video: {video_url}
        
        Process it to identify:
        1. Key programming concepts mentioned
        2. Tools or technologies discussed
        3. Main learning points
        4. Overall content quality and relevance
        
        Provide a summary and relevance score (0-1).
        """
        
        print("   🤖 Calling Claude Code for transcript extraction...")
        
        result = subprocess.run([
            'claude',
            '--print', 
            '--permission-mode', 'bypassPermissions',
            transcript_prompt
        ], capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            transcript_output = result.stdout
            print("   ✅ Transcript extraction successful!")
            
            # Create enhanced result
            enhanced_result = create_enhanced_result(test_video, transcript_output, unified_score)
            
            # Save to knowledge vault
            save_to_knowledge_vault(enhanced_result, base_path)
            
            # Update the queue
            update_processing_queue(test_video['video_id'], queue, queue_file, enhanced_result)
            
            print("   💾 Results saved to unified knowledge vault")
            
        else:
            print(f"   ❌ Transcript extraction failed: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("   ⏰ Transcript extraction timed out (120s limit)")
    except Exception as e:
        print(f"   ❌ Error during processing: {str(e)}")
    
    print(f"\n🎉 Unified processing test completed!")

def calculate_unified_score(video_data, base_path):
    """Calculate unified score based on framework"""
    
    # Load user preferences
    prefs_path = base_path / "user-preferences.json"
    with open(prefs_path, 'r') as f:
        prefs = json.load(f)
    
    # Base components
    channel_rating = video_data.get('channel_rating', 3.0) / 5.0  # Normalize to 0-1
    user_preference = get_user_preference(video_data['channel'], base_path)
    
    # Topic relevance
    topics = video_data.get('topics', [])
    topic_relevance = calculate_topic_relevance(topics, prefs)
    
    # Unified score calculation
    unified_score = (
        channel_rating * 0.4 +
        user_preference * 0.4 + 
        topic_relevance * 0.2
    )
    
    return min(unified_score, 1.0)

def get_user_preference(channel_name, base_path):
    """Get user preference for channel"""
    
    prefs_path = base_path / "user-preferences.json"
    with open(prefs_path, 'r') as f:
        prefs = json.load(f)
    
    stated_prefs = prefs.get('stated_preferences', {})
    
    # Check for exact matches
    channel_key = f"{channel_name.lower().replace(' ', '_')}_channel"
    if channel_key in stated_prefs:
        return stated_prefs[channel_key]['preference_score']
    
    # Check for partial matches
    high_pref_channels = ['theprimegen', 'theo', 'fireship']
    if any(pref in channel_name.lower() for pref in high_pref_channels):
        return 5.0
    
    return 3.0  # Default preference

def calculate_topic_relevance(topics, prefs):
    """Calculate topic relevance score"""
    if not topics:
        return 0.5
    
    topic_prefs = prefs.get('topic_preferences', {})
    
    relevance_scores = []
    for topic in topics:
        topic_key = topic.replace('-', '_')
        if topic_key in topic_prefs:
            relevance_scores.append(topic_prefs[topic_key]['interest_level'])
        else:
            relevance_scores.append(0.6)  # Default relevance
    
    return sum(relevance_scores) / len(relevance_scores)

def create_enhanced_result(video_data, transcript_output, unified_score):
    """Create enhanced result with unified framework metadata"""
    
    return {
        **video_data,
        'transcript_summary': transcript_output[:500] + "..." if len(transcript_output) > 500 else transcript_output,
        'unified_score': unified_score,
        'processed_with': 'unified-intelligence-framework',
        'framework_version': '1.0.0',
        'processing_timestamp': datetime.now(timezone.utc).isoformat(),
        'status': 'completed_test'
    }

def save_to_knowledge_vault(result, base_path):
    """Save result to unified knowledge vault"""
    
    # Create knowledge vault structure
    vault_path = base_path / "knowledge-vault" / "youtube-intelligence"
    channel_name = result['channel'].lower().replace(' ', '-')
    today = datetime.now().strftime('%Y-%m-%d')
    
    channel_dir = vault_path / channel_name / today
    channel_dir.mkdir(parents=True, exist_ok=True)
    
    # Save enhanced result
    video_id = result.get('video_id', 'unknown')
    result_file = channel_dir / f"{video_id}_unified_test.json"
    
    with open(result_file, 'w') as f:
        json.dump(result, f, indent=2)

def update_processing_queue(video_id, queue, queue_file, result):
    """Update processing queue with test result"""
    
    for video in queue:
        if video.get('video_id') == video_id:
            video['status'] = 'completed_test'
            video['unified_score'] = result['unified_score']
            video['processed_at'] = result['processing_timestamp']
            break
    
    # Save updated queue
    with open(queue_file, 'w') as f:
        json.dump(queue, f, indent=2)

if __name__ == "__main__":
    test_process_one_video()