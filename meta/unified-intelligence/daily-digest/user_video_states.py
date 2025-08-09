#!/usr/bin/env python3
"""
User Video States Management System
Handles personal video tracking, watch progress, queues, and analytics
"""

import json
import os
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
import shutil

class WatchStatus(Enum):
    """Video watch status enumeration"""
    UNWATCHED = "unwatched"
    WATCHING = "watching"
    COMPLETED = "completed"
    SKIPPED = "skipped"

class QueueType(Enum):
    """Queue type enumeration"""
    PERSONAL = "personal"
    SHARED = "shared"
    SYSTEM = "system"

@dataclass
class WatchSession:
    """Individual watch session data"""
    started_at: str
    ended_at: str
    duration_minutes: float
    progress_start: float
    progress_end: float

@dataclass
class VideoContext:
    """Context information for why user wants to watch video"""
    added_from: str = "daily_digest"
    learning_goal: str = ""
    project_context: str = ""
    difficulty_perception: Optional[int] = None

@dataclass
class VideoState:
    """Individual video state tracking"""
    video_id: str
    video_title: str
    channel_name: str
    watch_status: WatchStatus = WatchStatus.UNWATCHED
    watch_progress: float = 0.0
    personal_rating: Optional[int] = None
    personal_notes: str = ""
    tags: List[str] = None
    added_to_states_at: str = None
    last_watched_at: Optional[str] = None
    completed_at: Optional[str] = None
    estimated_watch_time_minutes: Optional[float] = None
    actual_watch_time_minutes: float = 0.0
    watch_sessions: List[WatchSession] = None
    context: VideoContext = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.watch_sessions is None:
            self.watch_sessions = []
        if self.context is None:
            self.context = VideoContext()
        if self.added_to_states_at is None:
            self.added_to_states_at = datetime.now(timezone.utc).isoformat()

@dataclass
class QueueVideo:
    """Video in a queue with position and metadata"""
    video_id: str
    position: int
    priority: int = 5  # 1-10
    added_at: str = None
    added_by: str = "user"
    notes: str = ""
    target_watch_date: Optional[str] = None

    def __post_init__(self):
        if self.added_at is None:
            self.added_at = datetime.now(timezone.utc).isoformat()

@dataclass
class UserQueue:
    """User's video queue"""
    queue_id: str
    name: str
    description: str = ""
    queue_type: QueueType = QueueType.PERSONAL
    created_at: str = None
    last_accessed_at: str = None
    is_active: bool = True
    settings: Dict[str, Any] = None
    videos: List[QueueVideo] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc).isoformat()
        if self.last_accessed_at is None:
            self.last_accessed_at = self.created_at
        if self.settings is None:
            self.settings = {
                "auto_sort": False,
                "max_videos": 100,
                "estimated_total_time_minutes": 0
            }
        if self.videos is None:
            self.videos = []

class UserVideoStateManager:
    """Manages all user video states, queues, and analytics"""
    
    def __init__(self, base_path: Optional[Path] = None, user_id: str = "default_user"):
        self.base_path = base_path or Path(__file__).parent
        self.user_id = user_id
        self.user_data_path = self.base_path / "data" / "users" / user_id
        
        # Ensure user directory exists
        self.user_data_path.mkdir(parents=True, exist_ok=True)
        
        # File paths
        self.profile_file = self.user_data_path / "profile.json"
        self.video_states_file = self.user_data_path / "video_states.json"
        self.queues_file = self.user_data_path / "queues.json"
        self.analytics_file = self.user_data_path / "analytics.json"
        self.sessions_file = self.user_data_path / "sessions.json"
        
        # Initialize default files if they don't exist
        self._initialize_user_files()
        
        print(f"📱 User Video State Manager initialized for user: {user_id}")
        print(f"   📁 User data path: {self.user_data_path}")

    def _initialize_user_files(self):
        """Initialize default user files if they don't exist"""
        
        # Initialize profile
        if not self.profile_file.exists():
            default_profile = {
                "user_id": self.user_id,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "last_active_at": datetime.now(timezone.utc).isoformat(),
                "preferences": {
                    "default_playback_speed": 1.0,
                    "auto_mark_completed_threshold": 0.90,
                    "daily_learning_goal_minutes": 30,
                    "priority_topics": ["claude", "react", "typescript"],
                    "time_zone": "UTC",
                    "notifications_enabled": True
                },
                "stats": {
                    "total_videos_watched": 0,
                    "total_watch_time_minutes": 0,
                    "learning_streak_days": 0,
                    "favorite_channels": [],
                    "most_watched_topics": []
                }
            }
            self._write_json_file(self.profile_file, default_profile)

        # Initialize video states
        if not self.video_states_file.exists():
            default_video_states = {
                "metadata": {
                    "user_id": self.user_id,
                    "last_updated": datetime.now(timezone.utc).isoformat(),
                    "total_videos_tracked": 0
                },
                "video_states": {}
            }
            self._write_json_file(self.video_states_file, default_video_states)

        # Initialize queues with default watch later queue
        if not self.queues_file.exists():
            default_queues = {
                "metadata": {
                    "user_id": self.user_id,
                    "last_updated": datetime.now(timezone.utc).isoformat(),
                    "total_queues": 2
                },
                "queues": {
                    "watch_later": asdict(UserQueue(
                        queue_id="watch_later",
                        name="Watch Later",
                        description="Default watch later queue",
                        queue_type=QueueType.PERSONAL
                    )),
                    "daily_learning": asdict(UserQueue(
                        queue_id="daily_learning", 
                        name="Today's Learning",
                        description="AI-curated daily learning queue",
                        queue_type=QueueType.SYSTEM,
                        settings={
                            "auto_sort": True,
                            "max_videos": 10,
                            "target_duration_minutes": 30,
                            "auto_refresh_daily": True
                        }
                    ))
                }
            }
            # Convert enum values to strings for JSON serialization
            for queue_data in default_queues["queues"].values():
                queue_data["queue_type"] = queue_data["queue_type"].value
            self._write_json_file(self.queues_file, default_queues)

        # Initialize analytics
        if not self.analytics_file.exists():
            today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
            default_analytics = {
                "metadata": {
                    "user_id": self.user_id,
                    "last_updated": datetime.now(timezone.utc).isoformat(),
                    "analytics_start_date": datetime.now(timezone.utc).isoformat()
                },
                "daily_stats": {},
                "weekly_stats": {},
                "monthly_stats": {},
                "all_time_stats": {
                    "total_videos_discovered": 0,
                    "total_videos_watched": 0,
                    "total_videos_completed": 0,
                    "total_watch_time_minutes": 0,
                    "completion_rate": 0.0,
                    "average_session_minutes": 0,
                    "longest_learning_streak": 0,
                    "favorite_watch_times": [],
                    "skill_competencies": {}
                }
            }
            self._write_json_file(self.analytics_file, default_analytics)

        # Initialize sessions
        if not self.sessions_file.exists():
            session_id = f"sess_{int(time.time() * 1000)}"
            default_sessions = {
                "metadata": {
                    "user_id": self.user_id,
                    "last_updated": datetime.now(timezone.utc).isoformat()
                },
                "current_session": {
                    "session_id": session_id,
                    "started_at": datetime.now(timezone.utc).isoformat(),
                    "last_activity_at": datetime.now(timezone.utc).isoformat(),
                    "videos_viewed": [],
                    "actions_performed": []
                },
                "recent_sessions": [],
                "last_visit_timestamp": datetime.now(timezone.utc).isoformat()
            }
            self._write_json_file(self.sessions_file, default_sessions)

    def _read_json_file(self, file_path: Path) -> Dict[str, Any]:
        """Safely read JSON file with error handling"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"⚠️  File not found: {file_path}")
            return {}
        except json.JSONDecodeError as e:
            print(f"❌ JSON decode error in {file_path}: {e}")
            return {}
        except Exception as e:
            print(f"❌ Error reading {file_path}: {e}")
            return {}

    def _write_json_file(self, file_path: Path, data: Dict[str, Any]):
        """Safely write JSON file with atomic operation"""
        try:
            # Write to temporary file first
            temp_file = file_path.with_suffix('.tmp')
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            # Backup existing file if it exists
            if file_path.exists():
                backup_file = file_path.with_suffix('.bak')
                shutil.copy2(file_path, backup_file)
            
            # Atomically replace the original file
            temp_file.replace(file_path)
            
        except Exception as e:
            print(f"❌ Error writing {file_path}: {e}")
            if temp_file.exists():
                temp_file.unlink()
            raise

    # Video State Management Methods
    
    def get_video_state(self, video_id: str) -> Optional[VideoState]:
        """Get video state for a specific video"""
        video_states_data = self._read_json_file(self.video_states_file)
        state_data = video_states_data.get("video_states", {}).get(video_id)
        
        if not state_data:
            return None
            
        # Convert back from JSON to VideoState object
        state_data["watch_status"] = WatchStatus(state_data["watch_status"])
        
        # Convert watch sessions
        if "watch_sessions" in state_data:
            state_data["watch_sessions"] = [
                WatchSession(**session) for session in state_data["watch_sessions"]
            ]
        
        # Convert context
        if "context" in state_data:
            state_data["context"] = VideoContext(**state_data["context"])
            
        return VideoState(**state_data)

    def set_video_state(self, video_state: VideoState) -> bool:
        """Set or update video state"""
        try:
            video_states_data = self._read_json_file(self.video_states_file)
            
            # Convert VideoState to dict for JSON storage
            state_dict = asdict(video_state)
            state_dict["watch_status"] = video_state.watch_status.value
            
            # Update the video states
            video_states_data["video_states"][video_state.video_id] = state_dict
            video_states_data["metadata"]["last_updated"] = datetime.now(timezone.utc).isoformat()
            video_states_data["metadata"]["total_videos_tracked"] = len(video_states_data["video_states"])
            
            self._write_json_file(self.video_states_file, video_states_data)
            return True
            
        except Exception as e:
            print(f"❌ Error setting video state for {video_state.video_id}: {e}")
            return False

    def update_watch_progress(self, video_id: str, progress: float, session_duration_minutes: float = 0) -> bool:
        """Update watch progress for a video"""
        video_state = self.get_video_state(video_id)
        if not video_state:
            return False
            
        old_progress = video_state.watch_progress
        video_state.watch_progress = min(1.0, max(0.0, progress))
        video_state.last_watched_at = datetime.now(timezone.utc).isoformat()
        video_state.actual_watch_time_minutes += session_duration_minutes
        
        # Add watch session if there was actual watching time
        if session_duration_minutes > 0:
            session = WatchSession(
                started_at=(datetime.now(timezone.utc) - timedelta(minutes=session_duration_minutes)).isoformat(),
                ended_at=datetime.now(timezone.utc).isoformat(),
                duration_minutes=session_duration_minutes,
                progress_start=old_progress,
                progress_end=video_state.watch_progress
            )
            video_state.watch_sessions.append(session)
        
        # Update watch status based on progress
        if video_state.watch_progress >= 0.90:  # 90% threshold for completion
            video_state.watch_status = WatchStatus.COMPLETED
            if not video_state.completed_at:
                video_state.completed_at = datetime.now(timezone.utc).isoformat()
        elif video_state.watch_progress > 0:
            video_state.watch_status = WatchStatus.WATCHING
            
        return self.set_video_state(video_state)

    def get_videos_by_status(self, status: WatchStatus) -> List[VideoState]:
        """Get all videos with a specific watch status"""
        video_states_data = self._read_json_file(self.video_states_file)
        matching_videos = []
        
        for video_id, state_data in video_states_data.get("video_states", {}).items():
            if state_data.get("watch_status") == status.value:
                video_state = self.get_video_state(video_id)
                if video_state:
                    matching_videos.append(video_state)
                    
        return matching_videos

    def get_recently_watched(self, limit: int = 10) -> List[VideoState]:
        """Get recently watched videos"""
        video_states_data = self._read_json_file(self.video_states_file)
        recent_videos = []
        
        for video_id, state_data in video_states_data.get("video_states", {}).items():
            if state_data.get("last_watched_at"):
                video_state = self.get_video_state(video_id)
                if video_state:
                    recent_videos.append((video_state, state_data["last_watched_at"]))
        
        # Sort by last watched time (most recent first)
        recent_videos.sort(key=lambda x: x[1], reverse=True)
        return [video for video, _ in recent_videos[:limit]]

    # Queue Management Methods
    
    def get_queue(self, queue_id: str) -> Optional[UserQueue]:
        """Get a specific queue"""
        queues_data = self._read_json_file(self.queues_file)
        queue_data = queues_data.get("queues", {}).get(queue_id)
        
        if not queue_data:
            return None
            
        # Convert back from JSON
        queue_data["queue_type"] = QueueType(queue_data["queue_type"])
        
        # Convert videos
        if "videos" in queue_data:
            queue_data["videos"] = [
                QueueVideo(**video_data) for video_data in queue_data["videos"]
            ]
            
        return UserQueue(**queue_data)

    def add_to_queue(self, queue_id: str, video_id: str, priority: int = 5, notes: str = "") -> bool:
        """Add a video to a queue"""
        try:
            queue = self.get_queue(queue_id)
            if not queue:
                return False
            
            # Check if video already in queue
            for video in queue.videos:
                if video.video_id == video_id:
                    return False  # Already in queue
            
            # Add video to queue
            queue_video = QueueVideo(
                video_id=video_id,
                position=len(queue.videos) + 1,
                priority=priority,
                notes=notes
            )
            queue.videos.append(queue_video)
            queue.last_accessed_at = datetime.now(timezone.utc).isoformat()
            
            # Update queue in file
            queues_data = self._read_json_file(self.queues_file)
            queue_dict = asdict(queue)
            queue_dict["queue_type"] = queue.queue_type.value
            queues_data["queues"][queue_id] = queue_dict
            queues_data["metadata"]["last_updated"] = datetime.now(timezone.utc).isoformat()
            
            self._write_json_file(self.queues_file, queues_data)
            return True
            
        except Exception as e:
            print(f"❌ Error adding video {video_id} to queue {queue_id}: {e}")
            return False

    def remove_from_queue(self, queue_id: str, video_id: str) -> bool:
        """Remove a video from a queue"""
        try:
            queue = self.get_queue(queue_id)
            if not queue:
                return False
            
            # Remove video from queue
            queue.videos = [v for v in queue.videos if v.video_id != video_id]
            
            # Reorder positions
            for i, video in enumerate(queue.videos, 1):
                video.position = i
            
            queue.last_accessed_at = datetime.now(timezone.utc).isoformat()
            
            # Update queue in file
            queues_data = self._read_json_file(self.queues_file)
            queue_dict = asdict(queue)
            queue_dict["queue_type"] = queue.queue_type.value
            queues_data["queues"][queue_id] = queue_dict
            queues_data["metadata"]["last_updated"] = datetime.now(timezone.utc).isoformat()
            
            self._write_json_file(self.queues_file, queues_data)
            return True
            
        except Exception as e:
            print(f"❌ Error removing video {video_id} from queue {queue_id}: {e}")
            return False

    def get_all_queues(self) -> Dict[str, UserQueue]:
        """Get all user queues"""
        queues_data = self._read_json_file(self.queues_file)
        queues = {}
        
        for queue_id in queues_data.get("queues", {}):
            queue = self.get_queue(queue_id)
            if queue:
                queues[queue_id] = queue
                
        return queues

    # Session Management Methods
    
    def start_new_session(self) -> str:
        """Start a new user session"""
        session_id = f"sess_{int(time.time() * 1000)}"
        
        sessions_data = self._read_json_file(self.sessions_file)
        
        # Archive current session to recent sessions
        if "current_session" in sessions_data:
            current_session = sessions_data["current_session"]
            current_session["ended_at"] = datetime.now(timezone.utc).isoformat()
            
            # Calculate duration
            try:
                started = datetime.fromisoformat(current_session["started_at"].replace('Z', '+00:00'))
                ended = datetime.now(timezone.utc)
                current_session["duration_minutes"] = (ended - started).total_seconds() / 60
            except:
                current_session["duration_minutes"] = 0
            
            # Add to recent sessions
            if "recent_sessions" not in sessions_data:
                sessions_data["recent_sessions"] = []
            sessions_data["recent_sessions"].insert(0, current_session)
            
            # Keep only last 10 sessions
            sessions_data["recent_sessions"] = sessions_data["recent_sessions"][:10]
        
        # Create new current session
        sessions_data["current_session"] = {
            "session_id": session_id,
            "started_at": datetime.now(timezone.utc).isoformat(),
            "last_activity_at": datetime.now(timezone.utc).isoformat(),
            "videos_viewed": [],
            "actions_performed": []
        }
        
        sessions_data["last_visit_timestamp"] = datetime.now(timezone.utc).isoformat()
        sessions_data["metadata"]["last_updated"] = datetime.now(timezone.utc).isoformat()
        
        self._write_json_file(self.sessions_file, sessions_data)
        return session_id

    def get_new_videos_since_last_visit(self, all_videos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Get videos that are new since the last visit"""
        sessions_data = self._read_json_file(self.sessions_file)
        last_visit = sessions_data.get("last_visit_timestamp")
        
        if not last_visit:
            return all_videos  # First visit, all videos are new
        
        try:
            last_visit_dt = datetime.fromisoformat(last_visit.replace('Z', '+00:00'))
            new_videos = []
            
            for video in all_videos:
                # Check if video was published after last visit
                if "published_at" in video:
                    try:
                        published_dt = datetime.fromisoformat(video["published_at"].replace('Z', '+00:00'))
                        if published_dt > last_visit_dt:
                            new_videos.append(video)
                    except:
                        continue
                        
            return new_videos
            
        except Exception as e:
            print(f"❌ Error getting new videos since last visit: {e}")
            return []

    def update_user_activity(self, action: str, video_id: str = None):
        """Update user activity in current session"""
        try:
            sessions_data = self._read_json_file(self.sessions_file)
            
            if "current_session" not in sessions_data:
                self.start_new_session()
                sessions_data = self._read_json_file(self.sessions_file)
            
            current_session = sessions_data["current_session"]
            current_session["last_activity_at"] = datetime.now(timezone.utc).isoformat()
            
            # Add action
            action_data = {
                "action": action,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            if video_id:
                action_data["video_id"] = video_id
                
            current_session["actions_performed"].append(action_data)
            
            # Add to viewed videos if it's a view action
            if video_id and action in ["view_video", "start_watching", "complete_video"]:
                if video_id not in current_session["videos_viewed"]:
                    current_session["videos_viewed"].append(video_id)
            
            sessions_data["metadata"]["last_updated"] = datetime.now(timezone.utc).isoformat()
            self._write_json_file(self.sessions_file, sessions_data)
            
        except Exception as e:
            print(f"❌ Error updating user activity: {e}")

def main():
    """Test the UserVideoStateManager"""
    print("🧪 Testing User Video State Manager")
    print("=" * 50)
    
    # Initialize manager
    manager = UserVideoStateManager()
    
    # Test video state management
    print("\n📹 Testing Video State Management")
    video_state = VideoState(
        video_id="test123",
        video_title="Test Video",
        channel_name="Test Channel"
    )
    
    # Set video state
    success = manager.set_video_state(video_state)
    print(f"Set video state: {'✅' if success else '❌'}")
    
    # Get video state
    retrieved_state = manager.get_video_state("test123")
    print(f"Retrieved video state: {'✅' if retrieved_state else '❌'}")
    if retrieved_state:
        print(f"   Status: {retrieved_state.watch_status.value}")
        print(f"   Progress: {retrieved_state.watch_progress:.1%}")
    
    # Update progress
    success = manager.update_watch_progress("test123", 0.5, 15)
    print(f"Updated progress to 50%: {'✅' if success else '❌'}")
    
    # Test queue management
    print("\n📋 Testing Queue Management")
    success = manager.add_to_queue("watch_later", "test123", priority=8, notes="Important video")
    print(f"Added to watch later queue: {'✅' if success else '❌'}")
    
    watch_later = manager.get_queue("watch_later")
    if watch_later:
        print(f"Watch later queue has {len(watch_later.videos)} videos")
    
    # Test session management
    print("\n🔄 Testing Session Management")
    session_id = manager.start_new_session()
    print(f"Started new session: {session_id}")
    
    manager.update_user_activity("view_video", "test123")
    print("Updated user activity ✅")
    
    print("\n✅ User Video State Manager testing completed!")

if __name__ == "__main__":
    main()