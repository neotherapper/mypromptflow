#!/usr/bin/env python3
"""
YouTube Intelligence System for Unified Intelligence Platform
Combines RSS feeds with YouTube Data API v3 for comprehensive channel analysis
Features selective transcript extraction based on importance scoring
"""

import json
import os
import requests
import time
import logging
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Tuple
import hashlib
from urllib.parse import parse_qs, urlparse
import xml.etree.ElementTree as ET
from dataclasses import dataclass, asdict

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class QuotaUsage:
    """Track YouTube API quota usage"""
    date: str
    total_used: int = 0
    search_calls: int = 0  # 100 units each
    video_calls: int = 0   # 1 unit each
    playlist_calls: int = 0 # 1 unit each
    daily_limit: int = 10000
    
    @property
    def remaining(self) -> int:
        return max(0, self.daily_limit - self.total_used)
    
    @property
    def usage_percentage(self) -> float:
        return (self.total_used / self.daily_limit) * 100

@dataclass
class VideoMetadata:
    """Comprehensive video metadata structure"""
    id: str
    title: str
    channel_id: str
    channel_name: str
    published_at: str
    duration: Optional[str] = None
    view_count: Optional[int] = None
    like_count: Optional[int] = None
    comment_count: Optional[int] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    category_id: Optional[str] = None
    thumbnail_url: Optional[str] = None
    importance_score: float = 0.0
    priority_topic_score: float = 0.0
    has_transcript: bool = False
    transcript_extracted: bool = False
    last_updated: Optional[str] = None
    source: str = "rss"  # "rss" or "api"

class YouTubeAPIClient:
    """Efficient YouTube Data API v3 client with quota management"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('YOUTUBE_API_KEY')
        self.base_url = "https://www.googleapis.com/youtube/v3"
        self.session = requests.Session()
        self.quota_file = Path(__file__).parent / "data" / "system" / "api_quota_usage.json"
        self.quota_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Load or initialize quota tracking
        self.quota_usage = self._load_quota_usage()
        
        if not self.api_key:
            logger.warning("YouTube API key not provided. API functionality will be limited.")
    
    def _load_quota_usage(self) -> QuotaUsage:
        """Load quota usage from file"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        try:
            if self.quota_file.exists():
                with open(self.quota_file, 'r') as f:
                    data = json.load(f)
                    if data.get('date') == today:
                        return QuotaUsage(**data)
        except Exception as e:
            logger.warning(f"Error loading quota usage: {e}")
        
        # Create new quota tracking for today
        return QuotaUsage(date=today)
    
    def _save_quota_usage(self):
        """Save quota usage to file"""
        try:
            with open(self.quota_file, 'w') as f:
                json.dump(asdict(self.quota_usage), f, indent=2)
        except Exception as e:
            logger.error(f"Error saving quota usage: {e}")
    
    def _track_quota_usage(self, operation: str, cost: int):
        """Track API quota usage"""
        self.quota_usage.total_used += cost
        
        if operation == 'search':
            self.quota_usage.search_calls += 1
        elif operation == 'videos':
            self.quota_usage.video_calls += 1
        elif operation == 'playlist':
            self.quota_usage.playlist_calls += 1
        
        self._save_quota_usage()
        
        if self.quota_usage.remaining < 100:
            logger.warning(f"Low quota remaining: {self.quota_usage.remaining} units")
    
    def can_make_request(self, cost: int) -> bool:
        """Check if we have enough quota for a request"""
        return self.quota_usage.remaining >= cost
    
    def get_channel_uploads_playlist_id(self, channel_id: str) -> Optional[str]:
        """Get the uploads playlist ID for a channel (1 quota unit)"""
        if not self.api_key or not self.can_make_request(1):
            return None
        
        try:
            url = f"{self.base_url}/channels"
            params = {
                'key': self.api_key,
                'part': 'contentDetails',
                'id': channel_id,
                'fields': 'items/contentDetails/relatedPlaylists/uploads'
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            self._track_quota_usage('videos', 1)
            
            data = response.json()
            if data.get('items'):
                return data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            
        except Exception as e:
            logger.error(f"Error getting uploads playlist for {channel_id}: {e}")
        
        return None
    
    def get_playlist_videos(self, playlist_id: str, max_results: int = 500) -> List[str]:
        """Get all video IDs from a playlist (1 quota unit per 50 videos)"""
        if not self.api_key:
            return []
        
        video_ids = []
        next_page_token = None
        
        while len(video_ids) < max_results:
            if not self.can_make_request(1):
                logger.warning("Quota limit reached, stopping playlist fetch")
                break
            
            try:
                url = f"{self.base_url}/playlistItems"
                params = {
                    'key': self.api_key,
                    'part': 'contentDetails',
                    'playlistId': playlist_id,
                    'maxResults': min(50, max_results - len(video_ids)),
                    'fields': 'items/contentDetails/videoId,nextPageToken'
                }
                
                if next_page_token:
                    params['pageToken'] = next_page_token
                
                response = self.session.get(url, params=params)
                response.raise_for_status()
                self._track_quota_usage('playlist', 1)
                
                data = response.json()
                
                # Extract video IDs
                for item in data.get('items', []):
                    video_id = item['contentDetails']['videoId']
                    if video_id not in video_ids:
                        video_ids.append(video_id)
                
                next_page_token = data.get('nextPageToken')
                if not next_page_token:
                    break
                    
            except Exception as e:
                logger.error(f"Error fetching playlist videos: {e}")
                break
        
        logger.info(f"Retrieved {len(video_ids)} video IDs from playlist")
        return video_ids
    
    def get_videos_metadata(self, video_ids: List[str]) -> List[VideoMetadata]:
        """Get metadata for multiple videos (1 quota unit per 50 videos)"""
        if not self.api_key or not video_ids:
            return []
        
        videos_metadata = []
        
        # Process in batches of 50
        for i in range(0, len(video_ids), 50):
            if not self.can_make_request(1):
                logger.warning("Quota limit reached, stopping metadata fetch")
                break
            
            batch = video_ids[i:i+50]
            
            try:
                url = f"{self.base_url}/videos"
                params = {
                    'key': self.api_key,
                    'part': 'snippet,contentDetails,statistics',
                    'id': ','.join(batch),
                    'fields': 'items(id,snippet(title,channelId,channelTitle,publishedAt,description,tags,categoryId,thumbnails),contentDetails(duration),statistics(viewCount,likeCount,commentCount))'
                }
                
                response = self.session.get(url, params=params)
                response.raise_for_status()
                self._track_quota_usage('videos', 1)
                
                data = response.json()
                
                for item in data.get('items', []):
                    video = self._parse_video_metadata(item)
                    if video:
                        videos_metadata.append(video)
                        
            except Exception as e:
                logger.error(f"Error fetching video metadata: {e}")
                continue
        
        logger.info(f"Retrieved metadata for {len(videos_metadata)} videos")
        return videos_metadata
    
    def _parse_video_metadata(self, item: Dict[str, Any]) -> Optional[VideoMetadata]:
        """Parse API response into VideoMetadata object"""
        try:
            snippet = item.get('snippet', {})
            statistics = item.get('statistics', {})
            content_details = item.get('contentDetails', {})
            
            return VideoMetadata(
                id=item['id'],
                title=snippet.get('title', ''),
                channel_id=snippet.get('channelId', ''),
                channel_name=snippet.get('channelTitle', ''),
                published_at=snippet.get('publishedAt', ''),
                duration=content_details.get('duration'),
                view_count=int(statistics.get('viewCount', 0)) if statistics.get('viewCount') else None,
                like_count=int(statistics.get('likeCount', 0)) if statistics.get('likeCount') else None,
                comment_count=int(statistics.get('commentCount', 0)) if statistics.get('commentCount') else None,
                description=snippet.get('description', ''),
                tags=snippet.get('tags', []),
                category_id=snippet.get('categoryId'),
                thumbnail_url=snippet.get('thumbnails', {}).get('medium', {}).get('url'),
                last_updated=datetime.now(timezone.utc).isoformat(),
                source="api"
            )
        except Exception as e:
            logger.error(f"Error parsing video metadata: {e}")
            return None
    
    def get_quota_status(self) -> Dict[str, Any]:
        """Get current quota usage status"""
        return {
            "date": self.quota_usage.date,
            "total_used": self.quota_usage.total_used,
            "remaining": self.quota_usage.remaining,
            "usage_percentage": round(self.quota_usage.usage_percentage, 2),
            "daily_limit": self.quota_usage.daily_limit,
            "api_calls": {
                "search": self.quota_usage.search_calls,
                "videos": self.quota_usage.video_calls,
                "playlist": self.quota_usage.playlist_calls
            }
        }

class YouTubeChannelAnalyzer:
    """Comprehensive YouTube channel analysis system"""
    
    def __init__(self, config_path: Optional[Path] = None, transcript_threshold: float = 0.75):
        self.base_path = Path(__file__).parent
        self.config_path = config_path or (self.base_path / "config" / "youtube-rss-channels.json")
        self.data_path = self.base_path / "data"
        self.transcript_threshold = transcript_threshold
        
        # Initialize components
        self.api_client = YouTubeAPIClient()
        self.rss_session = requests.Session()
        self.rss_session.headers.update({
            'User-Agent': 'Mozilla/5.0 (YouTube Intelligence System)'
        })
        
        # Load configuration
        self.config = self._load_config()
        self.channels = self.config.get('channels', [])
        
        # Create data directories
        self._setup_data_directories()
        
        # Initialize transcript processor
        try:
            from transcript_processor import TranscriptProcessor
            self.transcript_processor = TranscriptProcessor(transcript_threshold=self.transcript_threshold)
            self.transcript_processing_enabled = True
        except ImportError:
            logger.warning("Transcript processor not available - transcript extraction disabled")
            self.transcript_processor = None
            self.transcript_processing_enabled = False
        
        logger.info(f"YouTube Intelligence System initialized with {len(self.channels)} channels")
        logger.info(f"Transcript threshold: {self.transcript_threshold}")
        logger.info(f"Transcript processing enabled: {self.transcript_processing_enabled}")
        logger.info(f"API quota status: {self.api_client.get_quota_status()}")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load channel configuration"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return {"channels": []}
    
    def _setup_data_directories(self):
        """Create necessary data directory structure"""
        directories = [
            self.data_path / "channels",
            self.data_path / "system",
            self.data_path / "processing_queue"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def get_channel_data_path(self, channel_id: str) -> Path:
        """Get data path for a specific channel"""
        return self.data_path / "channels" / channel_id
    
    def analyze_channel(self, channel_id: str, force_refresh: bool = False) -> Dict[str, Any]:
        """Comprehensive channel analysis combining RSS and API data"""
        logger.info(f"🔍 Analyzing channel: {channel_id}")
        
        channel_config = self._get_channel_config(channel_id)
        if not channel_config:
            return {"error": f"Channel {channel_id} not found in configuration"}
        
        channel_path = self.get_channel_data_path(channel_id)
        channel_path.mkdir(parents=True, exist_ok=True)
        
        # Load existing video catalog
        catalog_file = channel_path / "videos_catalog.json"
        existing_catalog = self._load_video_catalog(catalog_file)
        
        # Get videos from RSS (recent)
        rss_videos = self._get_rss_videos(channel_config)
        
        # Get videos from API (historical if needed)
        api_videos = []
        if self._needs_api_refresh(existing_catalog, force_refresh):
            api_videos = self._get_api_videos(channel_config)
        
        # Merge and deduplicate videos
        all_videos = self._merge_video_sources(existing_catalog, rss_videos, api_videos)
        
        # Calculate importance scores
        scored_videos = self._score_videos(all_videos, channel_config)
        
        # Save updated catalog
        catalog_data = {
            "channel_id": channel_id,
            "channel_name": channel_config.get('name'),
            "last_updated": datetime.now(timezone.utc).isoformat(),
            "total_videos": len(scored_videos),
            "api_videos": len([v for v in scored_videos if v.source == 'api']),
            "rss_videos": len([v for v in scored_videos if v.source == 'rss']),
            "high_value_videos": len([v for v in scored_videos if v.importance_score > self.transcript_threshold]),
            "videos": [asdict(video) for video in scored_videos]
        }
        
        with open(catalog_file, 'w') as f:
            json.dump(catalog_data, f, indent=2)
        
        # Identify videos needing transcript extraction
        transcript_candidates = [
            v for v in scored_videos 
            if v.importance_score > self.transcript_threshold and not v.transcript_extracted
        ]
        
        # Queue high-value videos for transcript processing
        queued_for_transcripts = 0
        if self.transcript_processing_enabled and transcript_candidates:
            for video in transcript_candidates[:10]:  # Queue top 10 candidates
                video_data = asdict(video)
                if self.transcript_processor.add_video_to_queue(video_data):
                    queued_for_transcripts += 1
        
        logger.info(f"✅ Channel analysis complete: {len(scored_videos)} total videos, "
                   f"{len(transcript_candidates)} high-value videos for transcript extraction, "
                   f"{queued_for_transcripts} queued for processing")
        
        return {
            "channel_id": channel_id,
            "channel_name": channel_config.get('name'),
            "status": "success",
            "total_videos": len(scored_videos),
            "high_value_videos": len(transcript_candidates),
            "quota_used": self.api_client.quota_usage.total_used,
            "quota_remaining": self.api_client.quota_usage.remaining,
            "transcript_candidates": [asdict(v) for v in transcript_candidates[:10]]  # Top 10
        }
    
    def _get_channel_config(self, channel_id: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific channel"""
        for channel in self.channels:
            if channel.get('id') == channel_id:
                return channel
        return None
    
    def _load_video_catalog(self, catalog_file: Path) -> List[VideoMetadata]:
        """Load existing video catalog"""
        if not catalog_file.exists():
            return []
        
        try:
            with open(catalog_file, 'r') as f:
                data = json.load(f)
                return [VideoMetadata(**video) for video in data.get('videos', [])]
        except Exception as e:
            logger.error(f"Error loading video catalog: {e}")
            return []
    
    def _needs_api_refresh(self, existing_catalog: List[VideoMetadata], force_refresh: bool) -> bool:
        """Determine if we need to refresh via API"""
        if force_refresh:
            return True
        
        # If we have no videos, we need API
        if not existing_catalog:
            return True
        
        # Check if last API refresh was more than 24 hours ago
        api_videos = [v for v in existing_catalog if v.source == 'api']
        if not api_videos:
            return True
        
        try:
            last_api_update = max(datetime.fromisoformat(v.last_updated.replace('Z', '+00:00')) 
                                for v in api_videos if v.last_updated)
            hours_since_update = (datetime.now(timezone.utc) - last_api_update).total_seconds() / 3600
            return hours_since_update > 24
        except:
            return True
    
    def _get_rss_videos(self, channel_config: Dict[str, Any]) -> List[VideoMetadata]:
        """Get recent videos from RSS feed"""
        rss_url = channel_config.get('rss_url')
        if not rss_url:
            return []
        
        try:
            response = self.rss_session.get(rss_url, timeout=30)
            response.raise_for_status()
            
            root = ET.fromstring(response.text)
            videos = []
            
            # Parse Atom feed (YouTube RSS format)
            entries = root.findall('.//{http://www.w3.org/2005/Atom}entry')
            
            for entry in entries:
                video = self._parse_rss_entry(entry, channel_config)
                if video:
                    videos.append(video)
            
            logger.info(f"📡 RSS: Retrieved {len(videos)} recent videos")
            return videos
            
        except Exception as e:
            logger.error(f"Error fetching RSS feed: {e}")
            return []
    
    def _parse_rss_entry(self, entry: ET.Element, channel_config: Dict[str, Any]) -> Optional[VideoMetadata]:
        """Parse RSS entry into VideoMetadata"""
        try:
            video_id_elem = entry.find('.//{http://www.youtube.com/xml/schemas/2015}videoId')
            title_elem = entry.find('.//{http://www.w3.org/2005/Atom}title')
            published_elem = entry.find('.//{http://www.w3.org/2005/Atom}published')
            
            if video_id_elem is None or title_elem is None or published_elem is None:
                return None
            
            return VideoMetadata(
                id=video_id_elem.text,
                title=title_elem.text,
                channel_id=channel_config.get('channel_id', ''),
                channel_name=channel_config.get('name', ''),
                published_at=published_elem.text,
                last_updated=datetime.now(timezone.utc).isoformat(),
                source="rss"
            )
            
        except Exception as e:
            logger.error(f"Error parsing RSS entry: {e}")
            return None
    
    def _get_api_videos(self, channel_config: Dict[str, Any]) -> List[VideoMetadata]:
        """Get all videos from channel via API"""
        channel_id = channel_config.get('channel_id')
        if not channel_id:
            return []
        
        # Get uploads playlist
        playlist_id = self.api_client.get_channel_uploads_playlist_id(channel_id)
        if not playlist_id:
            logger.warning(f"Could not get uploads playlist for channel {channel_id}")
            return []
        
        # Get all video IDs
        video_ids = self.api_client.get_playlist_videos(playlist_id, max_results=1000)
        if not video_ids:
            return []
        
        # Get metadata for all videos
        videos = self.api_client.get_videos_metadata(video_ids)
        
        logger.info(f"🔍 API: Retrieved {len(videos)} historical videos")
        return videos
    
    def _merge_video_sources(self, existing: List[VideoMetadata], 
                           rss_videos: List[VideoMetadata], 
                           api_videos: List[VideoMetadata]) -> List[VideoMetadata]:
        """Merge videos from different sources, avoiding duplicates"""
        video_dict = {}
        
        # Start with existing videos
        for video in existing:
            video_dict[video.id] = video
        
        # Add RSS videos (newer data takes precedence)
        for video in rss_videos:
            if video.id in video_dict:
                # Update existing with RSS data (keep API metadata if available)
                existing_video = video_dict[video.id]
                if existing_video.source == 'api':
                    # Keep API metadata, update timestamps
                    existing_video.last_updated = video.last_updated
                else:
                    video_dict[video.id] = video
            else:
                video_dict[video.id] = video
        
        # Add API videos (only if not already present)
        for video in api_videos:
            if video.id not in video_dict:
                video_dict[video.id] = video
            else:
                # Merge API metadata with existing
                existing_video = video_dict[video.id]
                if existing_video.source == 'rss':
                    # Enhance RSS video with API metadata
                    existing_video.duration = video.duration
                    existing_video.view_count = video.view_count
                    existing_video.like_count = video.like_count
                    existing_video.comment_count = video.comment_count
                    existing_video.description = video.description
                    existing_video.tags = video.tags
                    existing_video.thumbnail_url = video.thumbnail_url
                    existing_video.source = "hybrid"  # Mark as enriched
        
        return list(video_dict.values())
    
    def _score_videos(self, videos: List[VideoMetadata], 
                     channel_config: Dict[str, Any]) -> List[VideoMetadata]:
        """Calculate importance scores for videos"""
        priority_topics = channel_config.get('priority_topics', [])
        priority_weights = self.config.get('priority_weights', {})
        
        for video in videos:
            # Base score from channel priority
            base_score = channel_config.get('priority_score', 3.0) / 5.0
            
            # Content age factor (newer is better, but not too new)
            age_score = self._calculate_age_score(video.published_at)
            
            # Engagement score (if available)
            engagement_score = self._calculate_engagement_score(video)
            
            # Topic relevance score
            topic_score = self._calculate_topic_score(video, priority_topics, priority_weights)
            
            # Combine scores
            video.importance_score = (base_score * 0.2 + 
                                    age_score * 0.3 + 
                                    engagement_score * 0.3 + 
                                    topic_score * 0.2)
            
            video.priority_topic_score = topic_score
        
        # Sort by importance score
        videos.sort(key=lambda x: x.importance_score, reverse=True)
        return videos
    
    def _calculate_age_score(self, published_at: str) -> float:
        """Calculate score based on video age"""
        try:
            pub_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
            days_old = (datetime.now(timezone.utc) - pub_date).days
            
            # Peak relevance at 1-30 days, gradual decline after
            if days_old <= 1:
                return 0.8  # Very new
            elif days_old <= 7:
                return 1.0  # Peak relevance
            elif days_old <= 30:
                return 0.9
            elif days_old <= 90:
                return 0.7
            elif days_old <= 365:
                return 0.5
            else:
                return 0.3  # Old but potentially valuable
        except:
            return 0.5
    
    def _calculate_engagement_score(self, video: VideoMetadata) -> float:
        """Calculate score based on engagement metrics"""
        if not video.view_count:
            return 0.5  # Neutral if no data
        
        try:
            # Basic engagement ratio
            views = video.view_count or 0
            likes = video.like_count or 0
            comments = video.comment_count or 0
            
            if views == 0:
                return 0.5
            
            # Calculate engagement rate
            like_rate = likes / views if views > 0 else 0
            comment_rate = comments / views if views > 0 else 0
            
            # Normalize scores (typical good rates)
            like_score = min(like_rate / 0.02, 1.0)  # 2% is excellent
            comment_score = min(comment_rate / 0.005, 1.0)  # 0.5% is excellent
            
            # View count score (logarithmic)
            import math
            view_score = min(math.log10(views + 1) / 6, 1.0)  # 1M views = 1.0
            
            return (like_score * 0.4 + comment_score * 0.3 + view_score * 0.3)
            
        except:
            return 0.5
    
    def _calculate_topic_score(self, video: VideoMetadata, 
                             priority_topics: List[str], 
                             priority_weights: Dict[str, float]) -> float:
        """Calculate score based on topic relevance"""
        if not priority_topics:
            return 0.5
        
        text_to_check = f"{video.title} {video.description or ''}".lower()
        
        topic_matches = []
        for topic in priority_topics:
            weight = priority_weights.get(topic, 1.0)
            if topic.lower() in text_to_check:
                topic_matches.append(weight)
        
        if not topic_matches:
            return 0.3  # Low relevance if no topic matches
        
        # Average of matched topic weights, normalized
        avg_weight = sum(topic_matches) / len(topic_matches)
        return min(avg_weight / 2.0, 1.0)  # Normalize assuming max weight is 2.0
    
    def analyze_all_channels(self, max_channels: Optional[int] = None) -> Dict[str, Any]:
        """Analyze all configured channels"""
        logger.info(f"🚀 Starting analysis of {len(self.channels)} channels")
        
        results = {
            "started_at": datetime.now(timezone.utc).isoformat(),
            "total_channels": len(self.channels),
            "channels_analyzed": 0,
            "channels_failed": 0,
            "total_videos_analyzed": 0,
            "high_value_videos_found": 0,
            "quota_used": 0,
            "channel_results": {},
            "errors": []
        }
        
        channels_to_analyze = self.channels[:max_channels] if max_channels else self.channels
        
        for channel in channels_to_analyze:
            channel_id = channel.get('id')
            try:
                logger.info(f"📊 Analyzing {channel.get('name', channel_id)}...")
                
                result = self.analyze_channel(channel_id)
                
                if result.get('status') == 'success':
                    results["channels_analyzed"] += 1
                    results["total_videos_analyzed"] += result.get('total_videos', 0)
                    results["high_value_videos_found"] += result.get('high_value_videos', 0)
                else:
                    results["channels_failed"] += 1
                    results["errors"].append(f"{channel_id}: {result.get('error', 'Unknown error')}")
                
                results["channel_results"][channel_id] = result
                
            except Exception as e:
                logger.error(f"Error analyzing channel {channel_id}: {e}")
                results["channels_failed"] += 1
                results["errors"].append(f"{channel_id}: {str(e)}")
        
        # Final statistics
        results["completed_at"] = datetime.now(timezone.utc).isoformat()
        results["quota_used"] = self.api_client.quota_usage.total_used
        results["quota_remaining"] = self.api_client.quota_usage.remaining
        
        # Save results
        results_file = self.data_path / "system" / f"analysis_results_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"✅ Analysis complete: {results['channels_analyzed']}/{results['total_channels']} channels successful")
        logger.info(f"📊 Found {results['high_value_videos_found']} high-value videos across {results['total_videos_analyzed']} total videos")
        logger.info(f"🔋 Quota used: {results['quota_used']}/{self.api_client.quota_usage.daily_limit}")
        
        return results
    
    def process_transcript_queue(self, max_videos: Optional[int] = None) -> Dict[str, Any]:
        """Process the transcript extraction queue"""
        if not self.transcript_processing_enabled:
            return {"status": "error", "message": "Transcript processing not enabled"}
        
        logger.info("🎬 Processing transcript queue...")
        return self.transcript_processor.process_transcript_queue(max_videos=max_videos)
    
    def get_transcript_queue_status(self) -> Dict[str, Any]:
        """Get transcript processing queue status"""
        if not self.transcript_processing_enabled:
            return {"status": "disabled", "message": "Transcript processing not enabled"}
        
        return self.transcript_processor.get_queue_status()
    
    def get_processed_transcripts(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get list of processed transcripts"""
        if not self.transcript_processing_enabled:
            return []
        
        return self.transcript_processor.get_processed_transcripts(limit=limit)
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        
        # API quota status
        quota_status = self.api_client.get_quota_status()
        
        # Channel analysis status
        channel_stats = {
            "total_channels": len(self.channels),
            "channels_with_data": 0,
            "total_videos_tracked": 0,
            "high_value_videos": 0
        }
        
        # Count videos across all channels
        for channel in self.channels:
            channel_path = self.get_channel_data_path(channel['id'])
            catalog_file = channel_path / "videos_catalog.json"
            
            if catalog_file.exists():
                try:
                    with open(catalog_file, 'r') as f:
                        data = json.load(f)
                        channel_stats["channels_with_data"] += 1
                        channel_stats["total_videos_tracked"] += data.get('total_videos', 0)
                        channel_stats["high_value_videos"] += data.get('high_value_videos', 0)
                except:
                    pass
        
        # Transcript processing status
        transcript_status = self.get_transcript_queue_status() if self.transcript_processing_enabled else {"status": "disabled"}
        
        return {
            "system_health": "operational",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "api_quota": quota_status,
            "channel_analysis": channel_stats,
            "transcript_processing": {
                "enabled": self.transcript_processing_enabled,
                "threshold": self.transcript_threshold,
                **transcript_status
            },
            "data_storage": {
                "base_path": str(self.base_path),
                "data_path": str(self.data_path)
            }
        }

def main():
    """Test the YouTube Intelligence System"""
    
    print("🎬 YouTube Intelligence System - Test Mode")
    print("=" * 60)
    
    # Initialize system
    analyzer = YouTubeChannelAnalyzer()
    
    # Show quota status
    quota_status = analyzer.api_client.get_quota_status()
    print(f"📊 API Quota Status:")
    print(f"   Used: {quota_status['total_used']}/{quota_status['daily_limit']} ({quota_status['usage_percentage']}%)")
    print(f"   Remaining: {quota_status['remaining']} units")
    
    # Test single channel analysis
    print(f"\n🔍 Testing Single Channel Analysis...")
    test_channel = "fireship"  # Known working channel
    
    result = analyzer.analyze_channel(test_channel)
    
    print(f"📋 Results for {test_channel}:")
    print(f"   Status: {result.get('status', 'unknown')}")
    if result.get('status') == 'success':
        print(f"   Total videos: {result.get('total_videos', 0)}")
        print(f"   High-value videos: {result.get('high_value_videos', 0)}")
        print(f"   Quota used: {result.get('quota_used', 0)}")
        
        # Show top transcript candidates
        candidates = result.get('transcript_candidates', [])
        if candidates:
            print(f"\n🏆 Top Transcript Candidates:")
            for i, candidate in enumerate(candidates[:3], 1):
                print(f"   {i}. {candidate['title'][:50]}...")
                print(f"      Score: {candidate['importance_score']:.3f} | Views: {candidate.get('view_count', 'N/A')}")
    else:
        print(f"   Error: {result.get('error', 'Unknown error')}")
    
    print(f"\n✅ Test completed!")

if __name__ == "__main__":
    main()