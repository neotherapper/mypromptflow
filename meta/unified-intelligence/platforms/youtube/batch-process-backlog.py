#!/usr/bin/env python3
"""
Batch Process YouTube Backlog
Efficiently processes remaining YouTube videos in the queue using the unified intelligence system
"""

import json
import sys
import time
from pathlib import Path
from datetime import datetime, timezone

def load_queue():
    """Load the current processing queue"""
    queue_file = Path(__file__).parent / "transcript-processing-queue.json"
    with open(queue_file, 'r') as f:
        return json.load(f)

def save_queue(queue):
    """Save the updated processing queue"""
    queue_file = Path(__file__).parent / "transcript-processing-queue.json"
    with open(queue_file, 'w') as f:
        json.dump(queue, f, indent=2)

def run_unified_processing(video_job):
    """Run unified processing for a single video"""
    import subprocess
    
    # Create test configuration for this video
    test_config = {
        "video_url": video_job["video_url"],
        "video_id": video_job["video_id"],
        "title": video_job["title"],
        "channel": video_job["channel"],
        "channel_rating": video_job["channel_rating"],
        "topics": video_job["topics"],
        "priority": video_job["priority"]
    }
    
    # Run the unified processing test
    try:
        result = subprocess.run([
            'python3', '../test-unified-processing.py'
        ], 
        capture_output=True, 
        text=True, 
        timeout=120,  # 2 minute timeout per video
        env={**os.environ, 'TEST_VIDEO_CONFIG': json.dumps(test_config)}
        )
        
        if result.returncode == 0:
            print(f"   ✅ Successfully processed: {video_job['title']}")
            return True, None
        else:
            print(f"   ❌ Failed to process: {video_job['title']}")
            print(f"      Error: {result.stderr}")
            return False, result.stderr
            
    except subprocess.TimeoutExpired:
        print(f"   ⏱️ Timeout processing: {video_job['title']}")
        return False, "Processing timeout"
    except Exception as e:
        print(f"   💥 Exception processing: {video_job['title']}")
        print(f"      Error: {str(e)}")
        return False, str(e)

def main():
    """Main batch processing function"""
    print("🚀 YouTube Backlog Batch Processor")
    print("=" * 50)
    
    # Load current queue
    queue = load_queue()
    pending_videos = [job for job in queue if job['status'] == 'pending']
    
    print(f"📊 Queue Status:")
    print(f"   Total videos: {len(queue)}")
    print(f"   Pending videos: {len(pending_videos)}")
    print(f"   Completed videos: {len([job for job in queue if 'completed' in job['status']])}")
    
    if not pending_videos:
        print("\n🎉 No pending videos to process!")
        return
    
    # Process videos in batches
    batch_size = 5  # Process 5 videos at a time
    processed_count = 0
    failed_count = 0
    
    print(f"\n🎬 Starting batch processing ({batch_size} videos per batch)...")
    
    for i in range(0, len(pending_videos), batch_size):
        batch = pending_videos[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        
        print(f"\n📦 Processing Batch {batch_num} ({len(batch)} videos):")
        
        for j, video_job in enumerate(batch):
            print(f"\n   🎥 {j+1}/{len(batch)}: {video_job['title']} ({video_job['channel']})")
            
            # Update status to processing
            for queue_job in queue:
                if queue_job['video_id'] == video_job['video_id']:
                    queue_job['status'] = 'processing'
                    break
            
            # Process the video
            success, error = run_unified_processing(video_job)
            
            # Update status based on result
            for queue_job in queue:
                if queue_job['video_id'] == video_job['video_id']:
                    if success:
                        queue_job['status'] = 'completed_batch'
                        queue_job['processed_at'] = datetime.now(timezone.utc).isoformat()
                        queue_job['unified_score'] = 1.0  # Will be calculated by processor
                        processed_count += 1
                    else:
                        queue_job['status'] = 'failed_batch'
                        queue_job['error'] = error
                        failed_count += 1
                    break
            
            # Save progress after each video
            save_queue(queue)
            
            # Brief pause between videos
            time.sleep(2)
        
        print(f"\n   📊 Batch {batch_num} complete:")
        print(f"      ✅ Processed: {processed_count}")
        print(f"      ❌ Failed: {failed_count}")
        
        # Longer pause between batches
        if i + batch_size < len(pending_videos):
            print(f"\n   ⏸️ Pausing 10 seconds before next batch...")
            time.sleep(10)
    
    # Final summary
    print(f"\n🎯 Batch Processing Complete!")
    print(f"   ✅ Successfully processed: {processed_count} videos")
    print(f"   ❌ Failed: {failed_count} videos")
    print(f"   📊 Success rate: {(processed_count / len(pending_videos) * 100):.1f}%")
    
    # Generate final digest
    print(f"\n📰 Generating updated intelligence digest...")
    try:
        subprocess.run(['python3', '../../daily-digest/intelligence-digest-generator.py'], 
                      timeout=60)
        print("   ✅ Intelligence digest updated!")
    except:
        print("   ⚠️ Could not update intelligence digest")
    
    print(f"\n🎉 All processing complete! Check the daily digest for results.")

if __name__ == "__main__":
    import os
    main()