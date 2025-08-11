---
api_version: Spotify Web API v1
authentication_types:
- OAuth 2.0 
- Client Credentials
category: Entertainment & Media
description: Spotify MCP server providing comprehensive music streaming data access,
  playlist management, and audio analytics. Essential music platform integration
  enabling Spotify API access, user profile management, and music recommendation
  systems through MCP.
estimated_setup_time: 20-30 minutes
id: 8f2a3b1c-4d5e-6f7g-8h9i-0j1k2l3m4n5o
installation_priority: 3
item_type: service
name: Spotify
priority: 3rd_priority
production_readiness: 88
provider: Community/Third-party
quality_score: 8.6
repository_url: https://github.com/emendir/mcp-server-spotify
setup_complexity: Low-Medium
source_database: tools_services
status: experimental
tags:
- Tier 4
- MCP Server
- API Service
- Consumer Service
- Media Platform
- Entertainment
- music
- Music Streaming
- OAuth
- spotify
tier: Tier 4
transport_protocols:
- Spotify Web API REST
- OAuth 2.0
information_capabilities:
  data_types:
  - user_profiles
  - playlists
  - tracks_metadata
  - audio_features
  - artist_data
  - album_data
  - playback_history
  - recommendations
  - search_results
  access_methods:
  - real-time
  - on-demand
  - batch
  authentication: required
  rate_limits: high
  complexity_score: 3
  typical_use_cases:
  - "Access user's Spotify playlists and music library for analysis"
  - "Retrieve audio features for music recommendation algorithms"
  - "Search and discover music content and artists"
  - "Monitor user listening patterns and preferences"
  - "Integrate music data with other applications and workflows"
  - "Create and manage playlists programmatically"
  - "Analyze music trends and popularity metrics"
---

**Community-maintained Spotify integration server for music streaming data access and playlist management through MCP**

## 📋 Basic Information

| Field | Value |
|-------|-------|
| **Provider** | Community/Third-party |
| **Category** | Entertainment & Media |
| **Production Readiness** | 88% |
| **Setup Complexity** | Low-Medium (3/10) |
| **Repository** | [Spotify MCP Server](https://github.com/emendir/mcp-server-spotify) |

## 📊 Information Access Capabilities  

### Primary Information Types
- **User Music Data**: Complete access to user profiles, listening history, and saved music collections
- **Music Catalog**: Search and browse Spotify's extensive music catalog with metadata
- **Audio Analytics**: Audio features, tempo, key, and acoustic analysis for tracks
- **Playlist Management**: Create, modify, and analyze playlists and user collections
- **Discovery & Recommendations**: Access to Spotify's recommendation algorithms and trending content
- **Artist & Album Data**: Comprehensive metadata for artists, albums, and tracks

### Access Patterns
- **Real-time Access**: Live API calls for current user state and music catalog data
- **OAuth Integration**: Secure user authentication with granular permission scopes
- **Batch Operations**: Bulk data retrieval for analytics and large-scale music processing
- **Search & Discovery**: Advanced search capabilities across Spotify's music catalog

### Authentication & Security
- **Authentication Required**: OAuth 2.0 with user consent and app registration
- **Rate Limits**: High (varies by endpoint, typically 100+ requests per minute)
- **Permissions**: Scope-based access control for user data and playlist modifications
- **Privacy Compliance**: Adheres to user privacy settings and data protection regulations

## 🚀 Core Capabilities & Features

### Music Data Access
- **Track Information**: Detailed metadata including audio features, popularity, and release dates
- **User Library**: Access to saved tracks, albums, and followed artists
- **Listening History**: Recently played tracks and listening patterns (where permitted)

### Playlist Operations
- **Playlist Management**: Create, update, and delete playlists programmatically
- **Collaborative Features**: Manage collaborative playlists and sharing settings
- **Advanced Filtering**: Search and filter playlists by various criteria

### Discovery & Analytics
- **Music Recommendations**: Access Spotify's recommendation engine based on user preferences
- **Audio Analysis**: Detailed audio features for music classification and analysis
- **Market Data**: Track popularity and trending music across different regions

### Search & Browse
- **Comprehensive Search**: Search tracks, albums, artists, and playlists with advanced filters
- **Category Browsing**: Access to Spotify's curated categories and featured playlists
- **New Releases**: Latest music releases and featured content

### Typical Use Cases for AI Agents
- **Music Analysis**: "Analyze audio features of my recently played tracks to identify music preferences"
- **Playlist Creation**: "Create a workout playlist based on high-energy tracks from my library"
- **Discovery Automation**: "Find new music similar to my top artists and add to discovery playlist"
- **Listening Insights**: "Generate reports on my listening habits and favorite genres"
- **Music Matching**: "Find tracks with specific audio characteristics for mood-based playlists"
- **Social Features**: "Share music recommendations based on similar listening patterns"

## 🔧 Setup & Configuration

### Prerequisites
- Spotify Developer Account and registered application
- OAuth 2.0 credentials (Client ID and Client Secret)
- User authentication flow implementation

### Basic Installation
```bash
# Install Spotify MCP Server
npm install @community/spotify-mcp-server

# Configure with Spotify API credentials
export SPOTIFY_CLIENT_ID="your_client_id"
export SPOTIFY_CLIENT_SECRET="your_client_secret"
export SPOTIFY_REDIRECT_URI="http://localhost:3000/callback"
```

### Authentication Setup
```javascript
// OAuth 2.0 Configuration
{
  "spotify": {
    "clientId": "your_spotify_client_id",
    "clientSecret": "your_spotify_client_secret",
    "redirectUri": "http://localhost:3000/callback",
    "scopes": [
      "user-read-private",
      "user-read-email",
      "user-library-read",
      "playlist-read-private",
      "playlist-modify-public",
      "playlist-modify-private",
      "user-read-recently-played",
      "user-top-read"
    ]
  }
}
```

## 📈 Integration Patterns

### Music Recommendation System
- **Preference Analysis**: Analyze user's music preferences and listening patterns
- **Similarity Matching**: Find similar tracks and artists based on audio features
- **Contextual Recommendations**: Create context-specific playlists (workout, focus, relaxation)

### Data Analytics Integration
- **Listening Analytics**: Track and analyze music consumption patterns
- **Trend Analysis**: Monitor music trends and popularity changes
- **Personal Insights**: Generate personalized music statistics and insights

### Content Management
- **Playlist Automation**: Automatically curate and update playlists based on criteria
- **Library Organization**: Organize and categorize music collections efficiently
- **Social Music Sharing**: Share and discover music with friends and communities

## ⚠️ Limitations & Considerations

- **User Consent Required**: All operations require explicit user authentication and consent
- **Regional Restrictions**: Content availability varies by geographic region
- **Rate Limiting**: API calls are subject to Spotify's rate limiting policies
- **Privacy Settings**: Access limited by individual user privacy preferences
- **Experimental Status**: Community-maintained with potential stability concerns

## 🔒 Security & Privacy

- **OAuth 2.0 Compliance**: Secure authentication following industry standards
- **Minimal Data Access**: Request only necessary permissions for intended functionality
- **User Privacy**: Respect user privacy settings and data protection preferences
- **Token Management**: Secure storage and refresh of authentication tokens