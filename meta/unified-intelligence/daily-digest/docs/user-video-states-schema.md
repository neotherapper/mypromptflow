# User Video States Schema Design

## Overview
File-based JSON storage system for tracking personal video states, watch progress, and user preferences.

## Storage Structure

```
data/
├── users/
│   └── {user_id}/
│       ├── profile.json                 # User profile and preferences
│       ├── video_states.json           # All video states for this user
│       ├── queues.json                 # User's custom queues
│       ├── analytics.json              # Watch time analytics
│       └── sessions.json               # Session tracking for "last visit"
```

## Schema Definitions

### 1. User Profile (`profile.json`)
```json
{
  "user_id": "default_user",
  "created_at": "2025-08-01T16:30:00Z",
  "last_active_at": "2025-08-01T16:30:00Z",
  "preferences": {
    "default_playback_speed": 1.0,
    "auto_mark_completed_threshold": 0.90,
    "daily_learning_goal_minutes": 30,
    "priority_topics": ["claude", "react", "typescript"],
    "time_zone": "UTC",
    "notifications_enabled": true
  },
  "stats": {
    "total_videos_watched": 0,
    "total_watch_time_minutes": 0,
    "learning_streak_days": 0,
    "favorite_channels": [],
    "most_watched_topics": []
  }
}
```

### 2. Video States (`video_states.json`)
```json
{
  "metadata": {
    "user_id": "default_user",
    "last_updated": "2025-08-01T16:30:00Z",
    "total_videos_tracked": 0
  },
  "video_states": {
    "{video_id}": {
      "video_id": "miTpJmMt7uo",
      "video_title": "The dating app that doxxed 72,000 women...",
      "channel_name": "Fireship",
      "watch_status": "unwatched",  // "unwatched" | "watching" | "completed" | "skipped"
      "watch_progress": 0.0,        // 0.0 to 1.0 (percentage)
      "personal_rating": null,      // 1-5 stars or null
      "personal_notes": "",
      "tags": [],                   // User-defined tags
      "added_to_states_at": "2025-08-01T16:30:00Z",
      "last_watched_at": null,
      "completed_at": null,
      "estimated_watch_time_minutes": null,
      "actual_watch_time_minutes": 0,
      "watch_sessions": [
        {
          "started_at": "2025-08-01T16:30:00Z",
          "ended_at": "2025-08-01T16:45:00Z",
          "duration_minutes": 15,
          "progress_start": 0.0,
          "progress_end": 0.3
        }
      ],
      "context": {
        "added_from": "daily_digest",     // Where user discovered this video
        "learning_goal": "",              // Why they want to watch this
        "project_context": "",           // Related project/work
        "difficulty_perception": null    // User's perceived difficulty (1-5)
      }
    }
  }
}
```

### 3. User Queues (`queues.json`)
```json
{
  "metadata": {
    "user_id": "default_user",
    "last_updated": "2025-08-01T16:30:00Z",
    "total_queues": 0
  },
  "queues": {
    "watch_later": {
      "queue_id": "watch_later",
      "name": "Watch Later",
      "description": "Default watch later queue",
      "queue_type": "personal",        // "personal" | "shared" | "system"
      "created_at": "2025-08-01T16:30:00Z",
      "last_accessed_at": "2025-08-01T16:30:00Z",
      "is_active": true,
      "settings": {
        "auto_sort": false,
        "max_videos": 100,
        "estimated_total_time_minutes": 0
      },
      "videos": [
        {
          "video_id": "miTpJmMt7uo",
          "position": 1,
          "priority": 5,               // 1-10 priority
          "added_at": "2025-08-01T16:30:00Z",
          "added_by": "user",
          "notes": "Important for security awareness",
          "target_watch_date": null
        }
      ]
    },
    "daily_learning": {
      "queue_id": "daily_learning",
      "name": "Today's Learning",
      "description": "AI-curated daily learning queue",
      "queue_type": "system",
      "created_at": "2025-08-01T16:30:00Z",
      "last_accessed_at": "2025-08-01T16:30:00Z",
      "is_active": true,
      "settings": {
        "auto_sort": true,
        "max_videos": 10,
        "target_duration_minutes": 30,
        "auto_refresh_daily": true
      },
      "videos": []
    }
  }
}
```

### 4. Analytics (`analytics.json`)
```json
{
  "metadata": {
    "user_id": "default_user",
    "last_updated": "2025-08-01T16:30:00Z",
    "analytics_start_date": "2025-08-01T16:30:00Z"
  },
  "daily_stats": {
    "2025-08-01": {
      "date": "2025-08-01",
      "videos_watched": 0,
      "videos_completed": 0,
      "total_watch_time_minutes": 0,
      "learning_goal_met": false,
      "top_topics": [],
      "favorite_channels": [],
      "average_completion_rate": 0.0
    }
  },
  "weekly_stats": {
    "2025-W31": {
      "week": "2025-W31",
      "videos_watched": 0,
      "videos_completed": 0,
      "total_watch_time_minutes": 0,
      "learning_goals_met": 0,
      "learning_streak_days": 0,
      "top_topics": [],
      "skill_progression": {}
    }
  },
  "monthly_stats": {
    "2025-08": {
      "month": "2025-08",
      "videos_watched": 0,
      "videos_completed": 0,
      "total_watch_time_minutes": 0,
      "learning_goals_met": 0,
      "skill_milestones_reached": [],
      "top_learning_paths": []
    }
  },
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
```

### 5. Sessions (`sessions.json`)
```json
{
  "metadata": {
    "user_id": "default_user",
    "last_updated": "2025-08-01T16:30:00Z"
  },
  "current_session": {
    "session_id": "sess_2025080116300001",
    "started_at": "2025-08-01T16:30:00Z",
    "last_activity_at": "2025-08-01T16:30:00Z",
    "videos_viewed": [],
    "actions_performed": []
  },
  "recent_sessions": [
    {
      "session_id": "sess_2025080116300001",
      "started_at": "2025-08-01T16:30:00Z",
      "ended_at": "2025-08-01T17:00:00Z",
      "duration_minutes": 30,
      "videos_viewed": [],
      "videos_watched": [],
      "videos_completed": [],
      "actions_performed": []
    }
  ],
  "last_visit_timestamp": "2025-08-01T16:30:00Z"
}
```

## File Management Strategy

### File Creation
- Files are created lazily when first needed
- Default user profile created on first access
- Empty collections initialized with metadata only

### File Updates
- Atomic writes using temporary files + rename
- Backup previous version before updates
- Graceful handling of concurrent access

### Data Integrity
- JSON schema validation on read/write
- Automatic cleanup of orphaned references
- Data migration support for schema changes

### Performance Considerations
- Lazy loading of user data
- In-memory caching for active sessions
- Batch operations for bulk updates
- Periodic cleanup of old analytics data

## API Interface

### Video State Operations
- `GET /api/user/video/{video_id}/state` - Get video state
- `POST /api/user/video/{video_id}/state` - Create/update video state  
- `PUT /api/user/video/{video_id}/progress` - Update watch progress
- `DELETE /api/user/video/{video_id}/state` - Reset video state

### Queue Operations  
- `GET /api/user/queues` - Get all user queues
- `POST /api/user/queues/{queue_id}/videos` - Add video to queue
- `PUT /api/user/queues/{queue_id}/videos/{video_id}` - Update video in queue
- `DELETE /api/user/queues/{queue_id}/videos/{video_id}` - Remove from queue

### Analytics Operations
- `GET /api/user/analytics/daily` - Get daily analytics
- `GET /api/user/analytics/weekly` - Get weekly analytics  
- `GET /api/user/analytics/dashboard` - Get dashboard summary

This schema provides a solid foundation for tracking personal video states while maintaining the file-based architecture of the existing system.