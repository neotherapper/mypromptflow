#!/usr/bin/env python3
"""
Video States API Server
RESTful API for managing user video states, queues, and analytics
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, Optional
import sys

# Import our user video states system
from user_video_states import UserVideoStateManager, VideoState, WatchStatus, VideoContext

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for frontend integration

# Global manager instance
video_state_manager = None

def init_manager():
    """Initialize the video state manager"""
    global video_state_manager
    if video_state_manager is None:
        video_state_manager = UserVideoStateManager()
    return video_state_manager

@app.before_request
def before_request():
    """Initialize manager before each request"""
    init_manager()

# Error handlers
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request", "message": str(error)}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found", "message": str(error)}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error", "message": str(error)}), 500

# Video State API Endpoints

@app.route('/api/user/video/<video_id>/state', methods=['GET'])
def get_video_state(video_id: str):
    """Get video state for a specific video"""
    try:
        video_state = video_state_manager.get_video_state(video_id)
        
        if not video_state:
            return jsonify({"video_id": video_id, "state": None}), 200
        
        # Convert to dict for JSON response
        state_dict = {
            "video_id": video_state.video_id,
            "video_title": video_state.video_title,
            "channel_name": video_state.channel_name,
            "watch_status": video_state.watch_status.value,
            "watch_progress": video_state.watch_progress,
            "personal_rating": video_state.personal_rating,
            "personal_notes": video_state.personal_notes,
            "tags": video_state.tags,
            "added_to_states_at": video_state.added_to_states_at,
            "last_watched_at": video_state.last_watched_at,
            "completed_at": video_state.completed_at,
            "estimated_watch_time_minutes": video_state.estimated_watch_time_minutes,
            "actual_watch_time_minutes": video_state.actual_watch_time_minutes,
            "context": {
                "added_from": video_state.context.added_from,
                "learning_goal": video_state.context.learning_goal,
                "project_context": video_state.context.project_context,
                "difficulty_perception": video_state.context.difficulty_perception
            }
        }
        
        return jsonify({"video_id": video_id, "state": state_dict}), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to get video state: {str(e)}"}), 500

@app.route('/api/user/video/<video_id>/state', methods=['POST', 'PUT'])
def set_video_state(video_id: str):
    """Create or update video state"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Create VideoState object
        video_state = VideoState(
            video_id=video_id,
            video_title=data.get("video_title", "Unknown Title"),
            channel_name=data.get("channel_name", "Unknown Channel"),
            watch_status=WatchStatus(data.get("watch_status", "unwatched")),
            watch_progress=float(data.get("watch_progress", 0.0)),
            personal_rating=data.get("personal_rating"),
            personal_notes=data.get("personal_notes", ""),
            tags=data.get("tags", []),
            estimated_watch_time_minutes=data.get("estimated_watch_time_minutes"),
            context=VideoContext(
                added_from=data.get("context", {}).get("added_from", "api"),
                learning_goal=data.get("context", {}).get("learning_goal", ""),
                project_context=data.get("context", {}).get("project_context", ""),
                difficulty_perception=data.get("context", {}).get("difficulty_perception")
            )
        )
        
        success = video_state_manager.set_video_state(video_state)
        
        if success:
            # Update user activity
            video_state_manager.update_user_activity("update_video_state", video_id)
            return jsonify({"success": True, "video_id": video_id}), 200
        else:
            return jsonify({"error": "Failed to save video state"}), 500
            
    except Exception as e:
        return jsonify({"error": f"Failed to set video state: {str(e)}"}), 500

@app.route('/api/user/video/<video_id>/progress', methods=['PUT'])
def update_video_progress(video_id: str):
    """Update watch progress for a video"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        progress = float(data.get("progress", 0.0))
        session_duration = float(data.get("session_duration_minutes", 0.0))
        
        success = video_state_manager.update_watch_progress(video_id, progress, session_duration)
        
        if success:
            # Update user activity
            activity_action = "complete_video" if progress >= 0.90 else "update_progress"
            video_state_manager.update_user_activity(activity_action, video_id)
            
            return jsonify({
                "success": True, 
                "video_id": video_id, 
                "progress": progress,
                "status": "completed" if progress >= 0.90 else "watching"
            }), 200
        else:
            return jsonify({"error": "Failed to update progress"}), 500
            
    except Exception as e:
        return jsonify({"error": f"Failed to update progress: {str(e)}"}), 500

@app.route('/api/user/videos/by-status/<status>', methods=['GET'])
def get_videos_by_status(status: str):
    """Get all videos with a specific watch status"""
    try:
        watch_status = WatchStatus(status)
        videos = video_state_manager.get_videos_by_status(watch_status)
        
        # Convert to list of dicts
        videos_list = []
        for video in videos:
            videos_list.append({
                "video_id": video.video_id,
                "video_title": video.video_title,
                "channel_name": video.channel_name,
                "watch_status": video.watch_status.value,
                "watch_progress": video.watch_progress,
                "personal_rating": video.personal_rating,
                "last_watched_at": video.last_watched_at,
                "actual_watch_time_minutes": video.actual_watch_time_minutes
            })
        
        return jsonify({
            "status": status,
            "count": len(videos_list),
            "videos": videos_list
        }), 200
        
    except ValueError:
        return jsonify({"error": f"Invalid watch status: {status}"}), 400
    except Exception as e:
        return jsonify({"error": f"Failed to get videos by status: {str(e)}"}), 500

@app.route('/api/user/videos/recently-watched', methods=['GET'])
def get_recently_watched():
    """Get recently watched videos"""
    try:
        limit = int(request.args.get('limit', 10))
        videos = video_state_manager.get_recently_watched(limit)
        
        # Convert to list of dicts
        videos_list = []
        for video in videos:
            videos_list.append({
                "video_id": video.video_id,
                "video_title": video.video_title,
                "channel_name": video.channel_name,
                "watch_status": video.watch_status.value,
                "watch_progress": video.watch_progress,
                "last_watched_at": video.last_watched_at,
                "personal_rating": video.personal_rating
            })
        
        return jsonify({
            "count": len(videos_list),
            "videos": videos_list
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to get recently watched videos: {str(e)}"}), 500

# Queue Management API Endpoints

@app.route('/api/user/queues', methods=['GET'])
def get_all_queues():
    """Get all user queues"""
    try:
        queues = video_state_manager.get_all_queues()
        
        # Convert to dict for JSON response
        queues_dict = {}
        for queue_id, queue in queues.items():
            queues_dict[queue_id] = {
                "queue_id": queue.queue_id,
                "name": queue.name,
                "description": queue.description,
                "queue_type": queue.queue_type.value,
                "created_at": queue.created_at,
                "last_accessed_at": queue.last_accessed_at,
                "is_active": queue.is_active,
                "video_count": len(queue.videos),
                "estimated_total_time": queue.settings.get("estimated_total_time_minutes", 0),
                "videos": [
                    {
                        "video_id": video.video_id,
                        "position": video.position,
                        "priority": video.priority,
                        "added_at": video.added_at,
                        "notes": video.notes
                    }
                    for video in queue.videos
                ]
            }
        
        return jsonify({
            "count": len(queues_dict),
            "queues": queues_dict
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to get queues: {str(e)}"}), 500

@app.route('/api/user/queues/<queue_id>/videos', methods=['POST'])
def add_to_queue(queue_id: str):
    """Add a video to a queue"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        video_id = data.get("video_id")
        if not video_id:
            return jsonify({"error": "video_id is required"}), 400
        
        priority = int(data.get("priority", 5))
        notes = data.get("notes", "")
        
        success = video_state_manager.add_to_queue(queue_id, video_id, priority, notes)
        
        if success:
            # Update user activity
            video_state_manager.update_user_activity("add_to_queue", video_id)
            return jsonify({
                "success": True,
                "queue_id": queue_id,
                "video_id": video_id
            }), 200
        else:
            return jsonify({"error": "Failed to add video to queue"}), 500
            
    except Exception as e:
        return jsonify({"error": f"Failed to add to queue: {str(e)}"}), 500

@app.route('/api/user/queues/<queue_id>/videos/<video_id>', methods=['DELETE'])
def remove_from_queue(queue_id: str, video_id: str):
    """Remove a video from a queue"""
    try:
        success = video_state_manager.remove_from_queue(queue_id, video_id)
        
        if success:
            # Update user activity
            video_state_manager.update_user_activity("remove_from_queue", video_id)
            return jsonify({
                "success": True,
                "queue_id": queue_id,
                "video_id": video_id
            }), 200
        else:
            return jsonify({"error": "Failed to remove video from queue"}), 500
            
    except Exception as e:
        return jsonify({"error": f"Failed to remove from queue: {str(e)}"}), 500

# Session Management API Endpoints

@app.route('/api/user/session/start', methods=['POST'])
def start_session():
    """Start a new user session"""
    try:
        session_id = video_state_manager.start_new_session()
        return jsonify({
            "success": True,
            "session_id": session_id
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to start session: {str(e)}"}), 500

@app.route('/api/user/videos/new-since-last-visit', methods=['POST'])
def get_new_videos_since_last_visit():
    """Get videos that are new since last visit"""
    try:
        data = request.get_json()
        if not data or "videos" not in data:
            return jsonify({"error": "videos array is required"}), 400
        
        all_videos = data["videos"]
        new_videos = video_state_manager.get_new_videos_since_last_visit(all_videos)
        
        return jsonify({
            "count": len(new_videos),
            "new_videos": new_videos
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to get new videos: {str(e)}"}), 500

# Analytics API Endpoints

@app.route('/api/user/analytics/summary', methods=['GET'])
def get_analytics_summary():
    """Get analytics summary for dashboard"""
    try:
        # Get basic stats from video states
        all_videos = video_state_manager.get_videos_by_status(WatchStatus.COMPLETED)
        watching_videos = video_state_manager.get_videos_by_status(WatchStatus.WATCHING)
        
        total_watch_time = sum(video.actual_watch_time_minutes for video in all_videos + watching_videos)
        
        return jsonify({
            "total_videos_completed": len(all_videos),
            "videos_in_progress": len(watching_videos),
            "total_watch_time_minutes": total_watch_time,
            "completion_rate": 0.0 if not (all_videos + watching_videos) else len(all_videos) / len(all_videos + watching_videos),
            "recently_watched": len(video_state_manager.get_recently_watched(7))  # Last 7 days
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to get analytics: {str(e)}"}), 500

# Utility API Endpoints

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "service": "video-states-api"
    }), 200

@app.route('/api/user/activity', methods=['POST'])
def log_user_activity():
    """Log user activity"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        action = data.get("action")
        video_id = data.get("video_id")
        
        if not action:
            return jsonify({"error": "action is required"}), 400
        
        video_state_manager.update_user_activity(action, video_id)
        
        return jsonify({"success": True}), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to log activity: {str(e)}"}), 500

# Static file serving for development
@app.route('/')
def serve_index():
    """Serve main page"""
    return send_from_directory('.', 'generated/content/daily-digest.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

def main():
    """Run the API server"""
    print("🚀 Starting Video States API Server")
    print("=" * 50)
    print("📍 Available endpoints:")
    print("   GET  /api/health")
    print("   GET  /api/user/video/<video_id>/state")
    print("   POST /api/user/video/<video_id>/state")
    print("   PUT  /api/user/video/<video_id>/progress")
    print("   GET  /api/user/videos/by-status/<status>")
    print("   GET  /api/user/videos/recently-watched")
    print("   GET  /api/user/queues")
    print("   POST /api/user/queues/<queue_id>/videos")
    print("   DELETE /api/user/queues/<queue_id>/videos/<video_id>")
    print("   POST /api/user/session/start")
    print("   POST /api/user/videos/new-since-last-visit")
    print("   GET  /api/user/analytics/summary")
    print("   POST /api/user/activity")
    print("=" * 50)
    
    # Initialize manager
    init_manager()
    
    # Run server
    app.run(
        host='0.0.0.0',
        port=8080,
        debug=True,
        threaded=True
    )

if __name__ == "__main__":
    main()