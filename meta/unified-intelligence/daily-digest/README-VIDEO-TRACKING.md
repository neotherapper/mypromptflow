# Personal Video Intelligence System

A comprehensive video tracking and learning analytics system for developer content consumption.

## Features

- **Video State Tracking**: Track watched, in-progress, completed, and skipped videos
- **Watch Later Queue**: Save videos for later viewing with priority management
- **Personal Analytics**: View learning goals, watch time, and completion rates
- **New Content Detection**: Automatically detect new videos since last visit
- **Continue Watching**: Resume videos with progress tracking
- **Rating System**: Rate videos with 5-star system

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the API Server**:
   ```bash
   python video_states_api.py
   ```
   Server runs on http://localhost:8080

3. **Open the Enhanced Daily Digest**:
   - Open `generated/content/daily-digest.html` in your browser
   - The video tracking features will automatically initialize

## API Endpoints

- `GET /api/user/video/{video_id}/state` - Get video state
- `POST /api/user/video/{video_id}/state` - Set video state
- `PUT /api/user/video/{video_id}/progress` - Update progress
- `GET /api/user/queues` - Get all queues
- `POST /api/user/queues/{queue_id}/videos` - Add to queue
- `GET /api/user/analytics/summary` - Get analytics

## Data Storage

User data is stored in JSON files under `data/users/{user_id}/`:
- `profile.json` - User preferences and settings
- `video_states.json` - All video watch states
- `queues.json` - Watch later and custom queues
- `analytics.json` - Learning analytics data
- `sessions.json` - Session tracking for "last visit"

## How to Use

1. **Track Videos**: Click action buttons on any video to mark as watched, add to queue, or start watching
2. **View Analytics**: Check your personal learning dashboard for progress tracking
3. **Manage Queue**: Use the Watch Later queue to save videos for future viewing
4. **Check New Content**: The "New Since Last Visit" section shows fresh content
5. **Continue Learning**: Resume partially watched videos from the Continue Watching section

## Architecture

- **Frontend**: Enhanced HTML/CSS/JavaScript with video state UI components
- **Backend**: Flask REST API with CORS support
- **Storage**: File-based JSON for user data persistence
- **Video Detection**: Automatic YouTube URL parsing and video ID extraction

This system transforms your daily content digest into a personalized learning platform optimized for developer productivity.