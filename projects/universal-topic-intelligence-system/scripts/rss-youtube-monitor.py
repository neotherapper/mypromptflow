#!/usr/bin/env python3
"""
YouTube RSS Monitoring System
Universal Topic Intelligence System - RSS Feed Monitoring

This script bypasses YouTube RSS access restrictions and provides automated
monitoring of your 23 curated YouTube channels with intelligent update detection.
"""

import json
import time
import hashlib
import requests
import feedparser
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, asdict
import random
import logging

@dataclass
class VideoEntry:
    """YouTube video entry from RSS feed"""
    video_id: str
    title: str
    url: str
    published: str
    channel_name: str
    channel_url: str
    description: str = ""
    duration: Optional[str] = None

@dataclass
class ChannelConfig:
    """YouTube channel configuration"""
    name: str
    url: str
    rss_url: str
    rating: float
    topics: List[str]
    upload_frequency: str
    priority: str = "medium"
    last_checked: Optional[str] = None
    last_video_id: Optional[str] = None

class YouTubeRSSMonitor:
    """YouTube RSS feed monitoring with bypass techniques"""
    
    def __init__(self, config_path: str = None):
        self.logger = self._setup_logging()
        self.config_path = config_path or "youtube-channels-config.json"
        self.state_file = "youtube-monitor-state.json"
        self.channels = self._load_channel_config()
        self.state = self._load_state()
        
        # User agents for rotation to avoid blocking
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0',
            'RSS Reader 1.0 (compatible; Educational Content Aggregator)',
            'FeedReader 2.0 (compatible; Learning Content Monitor)',
        ]
        
        # Rate limiting configuration
        self.request_delay = (2, 5)  # Random delay between 2-5 seconds
        self.max_retries = 3
        self.retry_delay = 10
    
    def _setup_logging(self) -> logging.Logger:
        """Set up logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('youtube-rss-monitor.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def _load_channel_config(self) -> List[ChannelConfig]:
        """Load YouTube channel configuration"""
        # Your 23 curated channels from Notion analysis
        default_channels = [
            {
                "name": "ThePrimeagen",
                "url": "https://www.youtube.com/@ThePrimeagen",
                "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UC8ENHE5xdFSwx71u3fDH5Xw",
                "rating": 5.0,
                "topics": ["software-engineering", "vim", "programming", "development-workflow"],
                "upload_frequency": "weekly",
                "priority": "high"
            },
            {
                "name": "Fireship",
                "url": "https://www.youtube.com/@Fireship", 
                "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCsBjURrPoezykLs9EqgamOA",
                "rating": 5.0,
                "topics": ["programming", "web-development", "tech-trends", "tutorials"],
                "upload_frequency": "weekly",
                "priority": "high"
            },
            {
                "name": "Theo - t3․gg",
                "url": "https://www.youtube.com/@t3dotgg",
                "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UC7K3iGDFa6OlnshFLrr2_Mw",
                "rating": 5.0,
                "topics": ["typescript", "react", "trpc", "t3-stack", "modern-web-dev"],
                "upload_frequency": "frequent",
                "priority": "high"
            },
            {
                "name": "Learn With Jason",
                "url": "https://www.youtube.com/@learnwithjason",
                "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCnty0z0pNRDgnuoirYXnC5A",
                "rating": 5.0,
                "topics": ["web-development", "live-coding", "javascript", "community"],
                "upload_frequency": "weekly",
                "priority": "high"
            },
            {
                "name": "James Q Quick",
                "url": "https://www.youtube.com/@JamesQQuick",
                "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UC-T8W79DN6PBnzomelvqJYw",
                "rating": 4.0,
                "topics": ["javascript", "react", "career-advice", "web-development"],
                "upload_frequency": "bi-weekly",
                "priority": "medium"
            },
            {
                "name": "UI.dev",
                "url": "https://www.youtube.com/@uidotdev",
                "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCsKsymTY_4BYR-wytLjex7A",
                "rating": 4.0,
                "topics": ["javascript", "frontend", "ecosystem", "tutorials"],
                "upload_frequency": "weekly",
                "priority": "medium"
            }
            # Add remaining 17 channels as needed
        ]
        
        if Path(self.config_path).exists():
            with open(self.config_path, 'r') as f:
                data = json.load(f)
                return [ChannelConfig(**channel) for channel in data]
        else:
            # Create default config file
            with open(self.config_path, 'w') as f:
                json.dump(default_channels, f, indent=2)
            return [ChannelConfig(**channel) for channel in default_channels]
    
    def _load_state(self) -> Dict[str, Any]:
        """Load monitoring state"""
        if Path(self.state_file).exists():
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {"last_run": None, "channel_states": {}, "processed_videos": set()}
    
    def _save_state(self):
        """Save monitoring state"""
        # Convert set to list for JSON serialization
        state_copy = self.state.copy()
        if "processed_videos" in state_copy and isinstance(state_copy["processed_videos"], set):
            state_copy["processed_videos"] = list(state_copy["processed_videos"])
        
        with open(self.state_file, 'w') as f:
            json.dump(state_copy, f, indent=2)
    
    def _get_random_user_agent(self) -> str:
        """Get random user agent for request rotation"""
        return random.choice(self.user_agents)
    
    def _make_request_with_retry(self, url: str, max_retries: int = None) -> Optional[requests.Response]:
        """Make HTTP request with retry logic and user agent rotation"""
        max_retries = max_retries or self.max_retries
        
        for attempt in range(max_retries):
            try:
                headers = {
                    'User-Agent': self._get_random_user_agent(),
                    'Accept': 'application/rss+xml, application/xml, text/xml',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept-Encoding': 'gzip, deflate',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                }
                
                # Random delay to avoid rate limiting
                delay = random.uniform(*self.request_delay)
                time.sleep(delay)
                
                response = requests.get(url, headers=headers, timeout=30)
                
                if response.status_code == 200:
                    return response
                elif response.status_code == 429:  # Rate limited
                    self.logger.warning(f"Rate limited for {url}, attempt {attempt + 1}")
                    time.sleep(self.retry_delay * (attempt + 1))
                else:
                    self.logger.warning(f"HTTP {response.status_code} for {url}, attempt {attempt + 1}")
                    
            except requests.RequestException as e:
                self.logger.error(f"Request failed for {url}, attempt {attempt + 1}: {e}")
                if attempt < max_retries - 1:
                    time.sleep(self.retry_delay)
        
        return None
    
    def _fetch_rss_feed(self, rss_url: str) -> Optional[feedparser.FeedParserDict]:
        """Fetch RSS feed with bypass techniques"""
        try:
            # Method 1: Direct feedparser with user agent
            headers = {'User-Agent': self._get_random_user_agent()}
            feed = feedparser.parse(rss_url, agent=headers['User-Agent'])
            
            if feed.bozo == 0 and len(feed.entries) > 0:
                return feed
            
            # Method 2: Manual request then parse
            response = self._make_request_with_retry(rss_url)
            if response:
                feed = feedparser.parse(response.content)
                if len(feed.entries) > 0:
                    return feed
            
            self.logger.warning(f"Failed to fetch RSS feed: {rss_url}")
            return None
            
        except Exception as e:
            self.logger.error(f"Error fetching RSS feed {rss_url}: {e}")
            return None
    
    def _parse_video_entry(self, entry, channel_name: str) -> VideoEntry:
        """Parse RSS entry into VideoEntry object"""
        # Extract video ID from URL
        video_id = entry.link.split('watch?v=')[-1] if 'watch?v=' in entry.link else entry.id
        
        return VideoEntry(
            video_id=video_id,
            title=entry.title,
            url=entry.link,
            published=entry.published,
            channel_name=channel_name,
            channel_url=entry.author if hasattr(entry, 'author') else "",
            description=entry.summary if hasattr(entry, 'summary') else ""
        )
    
    def _is_new_video(self, video: VideoEntry, channel_name: str) -> bool:
        """Check if video is new since last check"""
        channel_state = self.state["channel_states"].get(channel_name, {})
        last_video_id = channel_state.get("last_video_id")
        
        # Check if we've processed this video before
        if "processed_videos" not in self.state:
            self.state["processed_videos"] = set()
        
        processed_videos = set(self.state["processed_videos"]) if isinstance(self.state["processed_videos"], list) else self.state["processed_videos"]
        
        return video.video_id not in processed_videos
    
    def _is_relevant_content(self, video: VideoEntry, channel_config: ChannelConfig) -> bool:
        """Check if video content is relevant for processing"""
        title_lower = video.title.lower()
        description_lower = video.description.lower()
        
        # Programming keywords
        programming_keywords = [
            'javascript', 'typescript', 'python', 'react', 'node.js', 'css', 'html',
            'programming', 'development', 'code', 'tutorial', 'guide', 'learn',
            'web', 'frontend', 'backend', 'api', 'database', 'framework'
        ]
        
        # Check for programming relevance
        text_content = f"{title_lower} {description_lower}"
        keyword_matches = sum(1 for keyword in programming_keywords if keyword in text_content)
        
        # Channel-specific topic matching
        topic_matches = sum(1 for topic in channel_config.topics if topic.replace('-', ' ') in text_content)
        
        # Quality filters
        if len(video.title) < 10:  # Too short, likely not substantial
            return False
        
        # Skip likely promotional content
        promo_keywords = ['subscribe', 'like and subscribe', 'notification', 'bell icon']
        if any(keyword in title_lower for keyword in promo_keywords):
            return False
        
        # Calculate relevance score
        relevance_score = (keyword_matches * 0.3 + topic_matches * 0.4) / max(len(video.title.split()), 1)
        
        # Higher threshold for lower-rated channels
        threshold = 0.1 if channel_config.rating >= 4.5 else 0.2
        
        return relevance_score >= threshold or topic_matches > 0
    
    def monitor_channel(self, channel: ChannelConfig) -> List[VideoEntry]:
        """Monitor a single channel for new videos"""
        self.logger.info(f"Monitoring channel: {channel.name}")
        
        feed = self._fetch_rss_feed(channel.rss_url)
        if not feed:
            return []
        
        new_videos = []
        
        for entry in feed.entries:
            video = self._parse_video_entry(entry, channel.name)
            
            if self._is_new_video(video, channel.name) and self._is_relevant_content(video, channel):
                new_videos.append(video)
                self.logger.info(f"New relevant video found: {video.title}")
        
        # Update channel state
        if feed.entries:
            latest_video = self._parse_video_entry(feed.entries[0], channel.name)
            self.state["channel_states"][channel.name] = {
                "last_checked": datetime.now().isoformat(),
                "last_video_id": latest_video.video_id
            }
        
        return new_videos
    
    def monitor_all_channels(self) -> Dict[str, List[VideoEntry]]:
        """Monitor all configured channels"""
        self.logger.info("Starting YouTube channel monitoring cycle")
        
        all_new_videos = {}
        
        # Sort channels by priority
        sorted_channels = sorted(
            self.channels, 
            key=lambda x: {"high": 0, "medium": 1, "low": 2}.get(x.priority, 1)
        )
        
        for channel in sorted_channels:
            try:
                new_videos = self.monitor_channel(channel)
                if new_videos:
                    all_new_videos[channel.name] = new_videos
                    
                    # Mark videos as processed
                    if "processed_videos" not in self.state:
                        self.state["processed_videos"] = set()
                    
                    for video in new_videos:
                        if isinstance(self.state["processed_videos"], list):
                            self.state["processed_videos"] = set(self.state["processed_videos"])
                        self.state["processed_videos"].add(video.video_id)
                
            except Exception as e:
                self.logger.error(f"Error monitoring channel {channel.name}: {e}")
                continue
        
        # Update global state
        self.state["last_run"] = datetime.now().isoformat()
        self._save_state()
        
        return all_new_videos
    
    def queue_for_transcript_processing(self, videos: Dict[str, List[VideoEntry]]) -> List[Dict[str, Any]]:
        """Queue new videos for transcript processing"""
        processing_queue = []
        
        for channel_name, channel_videos in videos.items():
            channel_config = next((c for c in self.channels if c.name == channel_name), None)
            
            for video in channel_videos:
                queue_entry = {
                    "video_url": video.url,
                    "video_id": video.video_id,
                    "title": video.title,
                    "channel": channel_name,
                    "channel_rating": channel_config.rating if channel_config else 3.0,
                    "topics": channel_config.topics if channel_config else [],
                    "priority": channel_config.priority if channel_config else "medium",
                    "queued_at": datetime.now().isoformat(),
                    "status": "pending"
                }
                processing_queue.append(queue_entry)
        
        # Save processing queue
        queue_file = "transcript-processing-queue.json"
        if Path(queue_file).exists():
            with open(queue_file, 'r') as f:
                existing_queue = json.load(f)
        else:
            existing_queue = []
        
        existing_queue.extend(processing_queue)
        
        with open(queue_file, 'w') as f:
            json.dump(existing_queue, f, indent=2)
        
        self.logger.info(f"Queued {len(processing_queue)} videos for transcript processing")
        return processing_queue
    
    def generate_update_report(self, new_videos: Dict[str, List[VideoEntry]]) -> str:
        """Generate summary report of new videos found"""
        if not new_videos:
            return "No new relevant videos found in this monitoring cycle."
        
        report = [
            "=== YouTube Channel Monitoring Report ===",
            f"Monitoring run completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Channels monitored: {len(self.channels)}",
            f"New videos found: {sum(len(videos) for videos in new_videos.values())}",
            ""
        ]
        
        for channel_name, videos in new_videos.items():
            channel_config = next((c for c in self.channels if c.name == channel_name), None)
            priority = channel_config.priority if channel_config else "unknown"
            rating = channel_config.rating if channel_config else 0
            
            report.extend([
                f"🎥 {channel_name} ({rating}⭐, {priority} priority):",
                f"   Found {len(videos)} new videos:"
            ])
            
            for video in videos:
                report.append(f"   • {video.title}")
                report.append(f"     {video.url}")
            report.append("")
        
        return "\n".join(report)
    
    def run_monitoring_cycle(self) -> Dict[str, Any]:
        """Run complete monitoring cycle"""
        try:
            # Monitor all channels
            new_videos = self.monitor_all_channels()
            
            # Queue for transcript processing
            processing_queue = self.queue_for_transcript_processing(new_videos)
            
            # Generate report
            report = self.generate_update_report(new_videos)
            
            # Log results
            self.logger.info(f"Monitoring cycle completed. Found {len(processing_queue)} videos to process.")
            print(report)
            
            return {
                "success": True,
                "new_videos": new_videos,
                "processing_queue": processing_queue,
                "report": report
            }
            
        except Exception as e:
            self.logger.error(f"Monitoring cycle failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

def main():
    """Main execution function"""
    monitor = YouTubeRSSMonitor()
    
    print("YouTube RSS Monitoring System")
    print("=" * 40)
    print(f"Configured channels: {len(monitor.channels)}")
    print(f"High priority channels: {len([c for c in monitor.channels if c.priority == 'high'])}")
    print()
    
    # Run monitoring cycle
    result = monitor.run_monitoring_cycle()
    
    if result["success"]:
        print("✅ Monitoring cycle completed successfully")
        if result["processing_queue"]:
            print(f"📋 {len(result['processing_queue'])} videos queued for transcript processing")
            print("\nNext steps:")
            print("1. Run transcript extraction for queued videos")
            print("2. Process content through Universal Topic Intelligence System")
            print("3. Update knowledge vault with new insights")
    else:
        print(f"❌ Monitoring cycle failed: {result['error']}")

if __name__ == "__main__":
    main()