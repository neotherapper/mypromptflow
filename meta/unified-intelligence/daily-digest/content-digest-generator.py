#!/usr/bin/env python3
"""
Content-Only Daily Digest Generator
Pure content focus - NO system information mixing
Beautiful HTML output with duplicate detection
"""

import json
import os
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
import sys
from concurrent.futures import ThreadPoolExecutor
import time
import webbrowser

# Add parent paths for imports
sys.path.append(str(Path(__file__).parent.parent))

# Import the topic scoring engine
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("topic_scoring_engine", 
                                                str(Path(__file__).parent.parent / "topic-scoring-engine.py"))
    topic_scoring_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(topic_scoring_module)
    TopicScoringEngine = topic_scoring_module.TopicScoringEngine
    TOPIC_SCORING_AVAILABLE = True
    print("✅ Priority topic scoring engine imported successfully")
except Exception as e:
    print(f"⚠️  Topic scoring engine not available - using fallback scoring: {e}")
    TOPIC_SCORING_AVAILABLE = False
    TopicScoringEngine = None

# Import the RSS feed collector
try:
    spec = importlib.util.spec_from_file_location("rss_feed_collector", 
                                                str(Path(__file__).parent / "rss-feed-collector.py"))
    rss_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rss_module)
    RSSFeedCollector = rss_module.RSSFeedCollector
    RSS_COLLECTOR_AVAILABLE = True
    print("✅ RSS feed collector imported successfully")
except Exception as e:
    print(f"⚠️  RSS feed collector not available: {e}")
    RSS_COLLECTOR_AVAILABLE = False
    RSSFeedCollector = None

class ContentDigestGenerator:
    """Pure content digest generator - NO system information"""
    
    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = base_path or Path(__file__).parent.parent
        self.knowledge_vault = Path(__file__).parent.parent.parent.parent / "knowledge-vault" / "databases" / "knowledge_vault" / "content-intelligence"
        self.templates_dir = Path(__file__).parent / "templates"
        self.output_dir = Path(__file__).parent / "generated" / "content"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "history").mkdir(parents=True, exist_ok=True)
        
        # Initialize priority topic scoring engine
        if TOPIC_SCORING_AVAILABLE:
            priority_config_path = self.base_path / "priority-topics.json"
            self.topic_scorer = TopicScoringEngine(str(priority_config_path))
            print("✅ Priority topic scoring engine initialized")
        else:
            self.topic_scorer = None
        
        # Initialize RSS feed collector
        if RSS_COLLECTOR_AVAILABLE:
            self.rss_collector = RSSFeedCollector()
            print("✅ RSS feed collector initialized")
        else:
            self.rss_collector = None
    
    def check_existing_digest(self, date_str: str) -> Optional[Path]:
        """Check if digest already exists for the given date"""
        latest_file = self.output_dir / "daily-digest.html"
        history_file = self.output_dir / "history" / f"{date_str}-content-digest.html"
        
        if latest_file.exists():
            # Check if it's from today
            try:
                with open(latest_file, 'r') as f:
                    content = f.read()
                    if date_str in content:
                        return latest_file
            except:
                pass
        
        if history_file.exists():
            return history_file
            
        return None
    
    def generate_content_digest(self, date_range: str = "today", force_regenerate: bool = False) -> Dict[str, Any]:
        """Generate pure content digest - NO system information"""
        
        start_time = time.time()
        today_str = datetime.now().strftime('%Y-%m-%d')
        
        # Check for existing digest
        if not force_regenerate:
            existing_file = self.check_existing_digest(today_str)
            if existing_file:
                print(f"📄 Existing digest found: {existing_file}")
                print(f"   Use force_regenerate=True to create new digest")
                return {
                    "status": "existing_found",
                    "file_path": str(existing_file),
                    "message": f"Content digest already exists for {today_str}",
                    "generation_time": 0
                }
        
        print(f"📰 Generating pure content digest for {date_range}...")
        
        # Progress indicator: Step 1 of 5
        print(f"   [1/5] 📁 Collecting content from knowledge vault...")
        collection_start = time.time()
        content_items = self._collect_content_only(date_range=date_range)
        collection_time = time.time() - collection_start
        print(f"         ✅ Found {len(content_items)} items ({collection_time:.2f}s)")
        
        # Progress indicator: Step 2 of 5
        print(f"   [2/5] 🎯 Applying priority topic scoring...")
        scoring_start = time.time()
        scored_content = self._score_and_rank_content(content_items)
        scoring_time = time.time() - scoring_start
        print(f"         ✅ Scored and ranked content ({scoring_time:.2f}s)")
        
        # Progress indicator: Step 3 of 5
        print(f"   [3/5] 📈 Analyzing content quality and priorities...")
        # Calculate source breakdown
        source_breakdown = {}
        for item in scored_content:
            source_type = item.get('source_type', 'unknown')
            platform = item.get('platform', 'unknown')
            key = f"{platform}_{source_type}"
            source_breakdown[key] = source_breakdown.get(key, 0) + 1

        digest_data = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "date_range": date_range,
            "total_items": len(content_items),
            "high_quality_items": len([item for item in scored_content if item.get('intelligence_score', 0) > 0.8]),
            "average_score": round(sum(item.get('intelligence_score', 0) for item in scored_content) / len(scored_content), 3) if scored_content else 0,
            "priority_items": len([item for item in scored_content if item.get('detected_priority_topics', [])]),
            "subscribed_items": len([item for item in scored_content if item.get('source_type') == 'subscribed']),
            "discovered_items": len([item for item in scored_content if item.get('source_type') == 'discovered']),
            "content": scored_content[:20],  # Top 20 items
            "priority_topics": self._extract_priority_topics_data(scored_content),
            "source_breakdown": source_breakdown
        }
        print(f"         ✅ Quality analysis complete (top {len(digest_data['content'])} items selected)")
        
        # Progress indicator: Step 4 of 5
        print(f"   [4/5] 🎨 Generating beautiful HTML dashboard...")
        html_start = time.time()
        html_content = self._generate_html_digest(digest_data)
        html_time = time.time() - html_start
        print(f"         ✅ Dashboard created ({html_time:.2f}s)")
        
        # Progress indicator: Step 5 of 5
        print(f"   [5/5] 💾 Saving digest files...")
        save_start = time.time()
        self._save_content_digest(html_content, digest_data, today_str)
        save_time = time.time() - save_start
        print(f"         ✅ Files saved ({save_time:.2f}s)")
        
        # Calculate total generation time
        total_time = time.time() - start_time
        print(f"   🎯 Total generation time: {total_time:.2f}s")
        
        return {
            "status": "generated",
            "digest_data": digest_data,
            "file_path": str(self.output_dir / "daily-digest.html"),
            "generation_time": total_time
        }
    
    def _collect_content_only(self, date_range: str = "today") -> List[Dict[str, Any]]:
        """Collect ONLY content items - NO system information"""
        
        content_items = []
        
        # Collect subscribed YouTube content
        youtube_content = self._collect_youtube_content(date_range=date_range)
        content_items.extend(youtube_content)
        
        # Collect dynamic YouTube search results
        youtube_dynamic_content = self._collect_youtube_dynamic_search(date_range=date_range)
        content_items.extend(youtube_dynamic_content)
        
        # Collect Reddit discovery results
        reddit_content = self._collect_reddit_discovery(date_range=date_range)
        content_items.extend(reddit_content)
        
        # Collect RSS feeds content
        rss_content = self._collect_rss_feeds(date_range=date_range)
        content_items.extend(rss_content)
        
        # Collect YouTube Intelligence historical content
        youtube_intelligence_content = self._collect_youtube_intelligence(date_range=date_range)
        content_items.extend(youtube_intelligence_content)
        
        print(f"   📊 Collected {len(content_items)} pure content items ({date_range})")
        print(f"       🎯 YouTube subscribed: {len(youtube_content)} items")
        print(f"       🔍 YouTube dynamic: {len(youtube_dynamic_content)} items")
        print(f"       🔗 Reddit discovery: {len(reddit_content)} items")
        print(f"       📡 RSS feeds: {len(rss_content)} items")
        print(f"       🧠 YouTube intelligence: {len(youtube_intelligence_content)} items")
        
        return content_items
    
    def _collect_youtube_content(self, date_range: str = "today") -> List[Dict[str, Any]]:
        """Collect YouTube content only"""
        
        youtube_content = []
        youtube_vault = self.knowledge_vault / "youtube-intelligence"
        
        if not youtube_vault.exists():
            return youtube_content
        
        # Parse date range
        target_dates = self._parse_date_range(date_range)
        
        # Collect all content files first for parallel processing
        content_files = []
        for channel_dir in youtube_vault.iterdir():
            if channel_dir.is_dir():
                for date_str in target_dates:
                    date_dir = channel_dir / date_str
                    if date_dir.exists():
                        content_files.extend(date_dir.glob("*_unified_*.json"))
        
        print(f"   📁 Found {len(content_files)} content files to process")
        
        # Process files in parallel for better performance
        def load_content_file(content_file):
            try:
                with open(content_file, 'r') as f:
                    content = json.load(f)
                    content['platform'] = 'youtube'
                    content['content_source'] = 'subscribed_channel'
                    content['source_type'] = 'subscribed'
                    content['content_file'] = str(content_file)
                    content['content_age_days'] = self._calculate_content_age(content)
                    return content
            except Exception as e:
                print(f"   ❌ Error reading {content_file}: {e}")
                return None
        
        # Use thread pool for parallel file loading (I/O bound)
        with ThreadPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(load_content_file, content_files))
            youtube_content = [content for content in results if content is not None]
        
        return youtube_content
    
    def _collect_youtube_dynamic_search(self, date_range: str = "today") -> List[Dict[str, Any]]:
        """Collect YouTube dynamic search results"""
        
        dynamic_content = []
        dynamic_search_vault = self.knowledge_vault / "youtube-intelligence" / "dynamic-search"
        
        if not dynamic_search_vault.exists():
            return dynamic_content
        
        # Check for latest dynamic search results
        latest_search_file = dynamic_search_vault / "latest_dynamic_search.json"
        if latest_search_file.exists():
            try:
                with open(latest_search_file, 'r') as f:
                    search_data = json.load(f)
                    
                    # Filter results based on date range if needed
                    target_dates = self._parse_date_range(date_range)
                    
                    for video in search_data.get('top_videos', []):
                        # Add source attribution
                        video['platform'] = 'youtube'
                        video['content_source'] = 'dynamic_search'
                        video['source_type'] = 'discovered'
                        
                        # Map fields to match existing structure
                        content_item = {
                            'title': video.get('title', ''),
                            'url': f"https://www.youtube.com/watch?v={video.get('video_id', '')}",
                            'video_url': f"https://www.youtube.com/watch?v={video.get('video_id', '')}",
                            'channel': video.get('channel_name', ''),
                            'channel_id': video.get('channel_id', ''),
                            'published_date': video.get('published_at', ''),
                            'description': video.get('description', ''),
                            'platform': 'youtube',
                            'content_source': 'dynamic_search',
                            'source_type': 'discovered',
                            'priority_topic': video.get('priority_topic', ''),
                            'search_term': video.get('search_term', ''),
                            'unified_score': video.get('unified_score', 0),
                            'relevance_score': video.get('relevance_score', 0),
                            'engagement_score': video.get('engagement_score', 0),
                            'freshness_score': video.get('freshness_score', 0),
                            'view_count': video.get('view_count', 0),
                            'duration': video.get('duration', ''),
                            'thumbnail_url': video.get('thumbnail_url', ''),
                            'content_age_days': self._calculate_content_age_from_iso(video.get('published_at', ''))
                        }
                        
                        dynamic_content.append(content_item)
                        
            except Exception as e:
                print(f"   ❌ Error reading dynamic search results: {e}")
        
        # Check daily dynamic search results
        daily_dir = dynamic_search_vault / "daily"
        if daily_dir.exists():
            target_dates = self._parse_date_range(date_range)
            for date_str in target_dates:
                daily_file = daily_dir / f"{date_str}_dynamic_search.json"
                if daily_file.exists():
                    try:
                        with open(daily_file, 'r') as f:
                            daily_data = json.load(f)
                            for video in daily_data.get('top_videos', []):
                                # Similar processing as above
                                content_item = {
                                    'title': video.get('title', ''),
                                    'url': f"https://www.youtube.com/watch?v={video.get('video_id', '')}",
                                    'video_url': f"https://www.youtube.com/watch?v={video.get('video_id', '')}",
                                    'channel': video.get('channel_name', ''),
                                    'channel_id': video.get('channel_id', ''),
                                    'published_date': video.get('published_at', ''),
                                    'description': video.get('description', ''),
                                    'platform': 'youtube',
                                    'content_source': 'dynamic_search',
                                    'source_type': 'discovered',
                                    'priority_topic': video.get('priority_topic', ''),
                                    'search_term': video.get('search_term', ''),
                                    'unified_score': video.get('unified_score', 0),
                                    'relevance_score': video.get('relevance_score', 0),
                                    'engagement_score': video.get('engagement_score', 0),
                                    'freshness_score': video.get('freshness_score', 0),
                                    'view_count': video.get('view_count', 0),
                                    'duration': video.get('duration', ''),
                                    'thumbnail_url': video.get('thumbnail_url', ''),
                                    'content_age_days': self._calculate_content_age_from_iso(video.get('published_at', ''))
                                }
                                dynamic_content.append(content_item)
                    except Exception as e:
                        print(f"   ❌ Error reading daily dynamic search {daily_file}: {e}")
        
        return dynamic_content
    
    def _collect_reddit_discovery(self, date_range: str = "today") -> List[Dict[str, Any]]:
        """Collect Reddit discovery results"""
        
        reddit_content = []
        reddit_vault = self.knowledge_vault / "reddit-intelligence" / "dynamic-discovery"
        
        if not reddit_vault.exists():
            return reddit_content
        
        # Parse date range for file matching
        target_dates = self._parse_date_range(date_range)
        
        # Look for Reddit discovery files
        for date_str in target_dates:
            date_file = reddit_vault / f"{date_str}_reddit_discovery.json"
            if date_file.exists():
                try:
                    with open(date_file, 'r') as f:
                        discovery_data = json.load(f)
                        
                        for post in discovery_data.get('top_posts', []):
                            # Add source attribution
                            content_item = {
                                'title': post.get('title', ''),
                                'url': post.get('url', ''),
                                'reddit_url': post.get('reddit_url', ''),
                                'subreddit': post.get('subreddit', ''),
                                'author': post.get('author', ''),
                                'created_utc': post.get('created_utc', ''),
                                'score': post.get('score', 0),
                                'num_comments': post.get('num_comments', 0),
                                'description': post.get('selftext', ''),
                                'platform': 'reddit',
                                'content_source': 'dynamic_discovery',
                                'source_type': 'discovered',
                                'priority_topic': post.get('priority_topic', ''),
                                'search_term': post.get('search_term', ''),
                                'unified_score': post.get('unified_score', 0),
                                'relevance_score': post.get('relevance_score', 0),
                                'engagement_score': post.get('engagement_score', 0),
                                'content_age_days': self._calculate_content_age_from_unix(post.get('created_utc', 0))
                            }
                            
                            reddit_content.append(content_item)
                            
                except Exception as e:
                    print(f"   ❌ Error reading Reddit discovery {date_file}: {e}")
        
        # Check for latest discovery file
        latest_discovery_file = reddit_vault / "latest_reddit_discovery.json"
        if latest_discovery_file.exists():
            try:
                with open(latest_discovery_file, 'r') as f:
                    discovery_data = json.load(f)
                    
                    for post in discovery_data.get('top_posts', []):
                        content_item = {
                            'title': post.get('title', ''),
                            'url': post.get('url', ''),
                            'reddit_url': post.get('reddit_url', ''),
                            'subreddit': post.get('subreddit', ''),
                            'author': post.get('author', ''),
                            'created_utc': post.get('created_utc', ''),
                            'score': post.get('score', 0),
                            'num_comments': post.get('num_comments', 0),
                            'description': post.get('selftext', ''),
                            'platform': 'reddit',
                            'content_source': 'dynamic_discovery',
                            'source_type': 'discovered',
                            'priority_topic': post.get('priority_topic', ''),
                            'search_term': post.get('search_term', ''),
                            'unified_score': post.get('unified_score', 0),
                            'relevance_score': post.get('relevance_score', 0),
                            'engagement_score': post.get('engagement_score', 0),
                            'content_age_days': self._calculate_content_age_from_unix(post.get('created_utc', 0))
                        }
                        
                        reddit_content.append(content_item)
                        
            except Exception as e:
                print(f"   ❌ Error reading latest Reddit discovery: {e}")
        
        return reddit_content
    
    def _collect_rss_feeds(self, date_range: str = "today") -> List[Dict[str, Any]]:
        """Collect content from RSS feeds"""
        
        rss_content = []
        
        if not self.rss_collector:
            return rss_content
        
        try:
            # Get RSS items based on date range
            if date_range == "today":
                # Get items collected in the last 24 hours
                recent_items = self.rss_collector.get_recent_items(hours=24)
            elif date_range == "yesterday":
                # Get items from 24-48 hours ago
                # This is a simplified approach - could be improved for more precise date handling
                recent_items = self.rss_collector.get_recent_items(hours=48)
                # Filter to get only yesterday's items (24-48 hours ago)
                cutoff_start = datetime.now(timezone.utc) - timedelta(hours=48)
                cutoff_end = datetime.now(timezone.utc) - timedelta(hours=24)
                filtered_items = []
                for item in recent_items:
                    collected_at_str = item.get('collected_at')
                    if collected_at_str:
                        try:
                            collected_at = datetime.fromisoformat(collected_at_str.replace('Z', '+00:00'))
                            if cutoff_start <= collected_at < cutoff_end:
                                filtered_items.append(item)
                        except:
                            continue
                recent_items = filtered_items
            else:
                # For other date ranges, collect items from last week
                hours = 24 * 7  # Default to 1 week
                if "3_days" in date_range:
                    hours = 24 * 3
                elif "week" in date_range:
                    hours = 24 * 7
                elif "2_weeks" in date_range:
                    hours = 24 * 14
                
                recent_items = self.rss_collector.get_recent_items(hours=hours)
            
            # Convert RSS feed items to content format
            for item in recent_items:
                content_item = {
                    'title': item.get('title', 'Unknown Title'),
                    'url': item.get('url', ''),
                    'video_url': item.get('url', ''),  # For compatibility with YouTube format
                    'channel': item.get('channel_name', 'Unknown Channel'),
                    'channel_name': item.get('channel_name', 'Unknown Channel'),
                    'source_name': item.get('channel_name', 'Unknown Channel'),
                    'description': item.get('description', ''),
                    'published_date': item.get('published_date', ''),
                    'platform': item.get('platform', 'rss'),
                    'content_source': 'rss_feed',
                    'source_type': 'subscribed',  # RSS feeds are subscribed channels
                    'source_channel': item.get('source_channel', ''),
                    'priority_score': item.get('priority_score', 3.0),
                    'quality_rating': item.get('quality_rating', 4.0) / 5.0,  # Normalize to 0-1
                    'priority_topics': item.get('priority_topics', []),
                    'categories': item.get('categories', []),
                    'content_age_days': item.get('content_age_days', 999.0),
                    'content_hash': item.get('content_hash', ''),
                    'collected_at': item.get('collected_at', ''),
                    'unified_score': item.get('quality_rating', 4.0) / 5.0  # Use quality rating as unified score
                }
                
                rss_content.append(content_item)
            
        except Exception as e:
            print(f"   ❌ Error collecting RSS feeds: {e}")
        
        return rss_content
    
    def _collect_youtube_intelligence(self, date_range: str = "today") -> List[Dict[str, Any]]:
        """Collect high-value historical content from YouTube Intelligence System"""
        
        intelligence_content = []
        
        try:
            # Import YouTube Intelligence hook
            spec = __import__('importlib.util').util.spec_from_file_location(
                "youtube_intelligence_hook", 
                str(Path(__file__).parent / "youtube-intelligence-hook.py")
            )
            hook_module = __import__('importlib.util').util.module_from_spec(spec)
            spec.loader.exec_module(hook_module)
            
            # Determine max videos based on date range
            max_videos = 5  # Default for today
            if date_range == "yesterday":
                max_videos = 3
            elif "3_days" in date_range:
                max_videos = 8
            elif "week" in date_range:
                max_videos = 15
            elif "2_weeks" in date_range:
                max_videos = 20
            
            # Get high-value content from YouTube Intelligence
            intelligence_data = hook_module.get_youtube_intelligence_content(
                max_videos=max_videos, 
                min_score=0.75
            )
            
            if intelligence_data.get('status') == 'success':
                # Convert intelligence items to content format
                for item in intelligence_data.get('content', []):
                    content_item = {
                        'title': item.get('title', 'Unknown Title'),
                        'url': item.get('url', ''),
                        'video_url': item.get('url', ''),
                        'channel': item.get('channel', 'Unknown Channel'),
                        'published_date': item.get('published_at', ''),
                        'description': item.get('description', ''),
                        'platform': 'youtube',
                        'content_source': 'intelligence_analysis',
                        'source_type': 'intelligent',
                        'content_age_days': self._calculate_content_age_from_iso(item.get('published_at', '')),
                        'intelligence_metadata': {
                            'importance_score': item.get('importance_score', 0.0),
                            'priority_topic_score': item.get('priority_topic_score', 0.0),
                            'has_transcript': item.get('has_transcript', False),
                            'transcript_extracted': item.get('transcript_extracted', False),
                            'discovery_method': item.get('discovery_method', 'intelligence_analysis'),
                            'metadata': item.get('metadata', {})
                        },
                        # Use importance score as initial intelligence score
                        'intelligence_score': item.get('importance_score', 0.0),
                        'relevance_score': item.get('relevance_score', 0.0),
                        'source': f"YouTube Intelligence ({item.get('channel', 'Unknown')})",
                    }
                    
                    intelligence_content.append(content_item)
                
                print(f"   🧠 YouTube Intelligence: {len(intelligence_content)} high-value videos collected (min_score=0.75)")
                
                # Log intelligence system status
                metadata = intelligence_data.get('metadata', {})
                if metadata:
                    print(f"       📊 System stats: {metadata.get('videos_selected', 0)}/{metadata.get('total_high_value_videos', 0)} videos selected")
                    print(f"       📡 Channels: {metadata.get('channels_analyzed', 0)} analyzed")
                    if metadata.get('transcript_processing', {}).get('enabled'):
                        processed_count = metadata.get('transcript_processing', {}).get('processed_count', 0)
                        print(f"       📜 Transcripts: {processed_count} processed")
            else:
                status = intelligence_data.get('status', 'unknown')
                message = intelligence_data.get('message', 'No message')
                print(f"   ⚠️  YouTube Intelligence unavailable: {status} - {message}")
        
        except Exception as e:
            print(f"   ❌ Error collecting YouTube Intelligence content: {e}")
        
        return intelligence_content
    
    def _calculate_content_age_from_iso(self, iso_date_str: str) -> float:
        """Calculate content age from ISO format date"""
        if not iso_date_str:
            return 999.0
        
        try:
            if iso_date_str.endswith('Z'):
                published_date = datetime.fromisoformat(iso_date_str.replace('Z', '+00:00'))
            elif '+' in iso_date_str or iso_date_str.endswith('00:00'):
                published_date = datetime.fromisoformat(iso_date_str)
            else:
                published_date = datetime.fromisoformat(iso_date_str).replace(tzinfo=timezone.utc)
            
            now = datetime.now(timezone.utc)
            age_delta = now - published_date.replace(tzinfo=timezone.utc)
            age_days = age_delta.total_seconds() / (24 * 3600)
            
            return max(0.0, age_days)
            
        except (ValueError, AttributeError) as e:
            print(f"   ⚠️ Error parsing ISO date '{iso_date_str}': {e}")
            return 999.0
    
    def _calculate_content_age_from_unix(self, unix_timestamp: int) -> float:
        """Calculate content age from Unix timestamp"""
        if not unix_timestamp or unix_timestamp == 0:
            return 999.0
        
        try:
            published_date = datetime.fromtimestamp(unix_timestamp, tz=timezone.utc)
            now = datetime.now(timezone.utc)
            age_delta = now - published_date
            age_days = age_delta.total_seconds() / (24 * 3600)
            
            return max(0.0, age_days)
            
        except (ValueError, TypeError) as e:
            print(f"   ⚠️ Error parsing Unix timestamp '{unix_timestamp}': {e}")
            return 999.0
    
    def _parse_date_range(self, date_range: str) -> List[str]:
        """Parse date range string and return list of date strings"""
        
        now = datetime.now()
        
        if date_range == "today":
            return [now.strftime('%Y-%m-%d')]
        elif date_range == "yesterday":
            yesterday = now - timedelta(days=1)
            return [yesterday.strftime('%Y-%m-%d')]
        elif date_range == "last_3_days":
            return [(now - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(3)]
        elif date_range == "last_week" or date_range == "week":
            return [(now - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(7)]
        else:
            # Default to today
            return [now.strftime('%Y-%m-%d')]
    
    def _calculate_content_age(self, content: Dict[str, Any]) -> float:
        """Calculate content age in days from published date"""
        
        published_date_str = content.get('published_date') or content.get('published') or content.get('queued_at')
        
        if not published_date_str:
            return 999.0
        
        try:
            if published_date_str.endswith('Z'):
                published_date = datetime.fromisoformat(published_date_str.replace('Z', '+00:00'))
            elif '+' in published_date_str or published_date_str.endswith('00:00'):
                published_date = datetime.fromisoformat(published_date_str)
            else:
                published_date = datetime.fromisoformat(published_date_str).replace(tzinfo=timezone.utc)
            
            now = datetime.now(timezone.utc)
            age_delta = now - published_date.replace(tzinfo=timezone.utc)
            age_days = age_delta.total_seconds() / (24 * 3600)
            
            return max(0.0, age_days)
            
        except (ValueError, AttributeError) as e:
            print(f"   ⚠️ Error parsing date '{published_date_str}': {e}")
            return 999.0
    
    def _score_and_rank_content(self, content_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Score and rank content with priority topics and apply filtering"""
        
        if self.topic_scorer and TOPIC_SCORING_AVAILABLE:
            print("🎯 Using priority topic scoring engine")
            
            scored_objects = self.topic_scorer.score_content_batch(content_items)
            
            # Create lookup dictionary for O(1) matching instead of O(n²)
            content_lookup = {}
            for item in content_items:
                key = f"{item.get('title', '')}|{item.get('url', '')}"
                content_lookup[key] = item
            
            scored_items = []
            for scored_obj in scored_objects:
                # Fast lookup using dictionary
                key = f"{scored_obj.title}|{scored_obj.url}"
                original_item = content_lookup.get(key)
                
                if original_item:
                    # Add priority scoring data
                    original_item['intelligence_score'] = scored_obj.final_score
                    original_item['priority_score'] = scored_obj.priority_score
                    original_item['detected_priority_topics'] = scored_obj.detected_priority_topics
                    original_item['score_breakdown'] = scored_obj.score_breakdown
                    scored_items.append(original_item)
            
            print(f"   📊 Scored {len(scored_items)} items with priority topic weighting")
            # Apply content filtering
            filtered_items = self._filter_relevant_content(scored_items)
            return filtered_items
        else:
            print("⚠️  Using fallback scoring (no priority topics)")
            
            scored_items = []
            for item in content_items:
                score = self._calculate_fallback_score(item)
                item['intelligence_score'] = score
                scored_items.append(item)
            
            sorted_items = sorted(scored_items, key=lambda x: x.get('intelligence_score', 0), reverse=True)
            # Apply content filtering
            filtered_items = self._filter_relevant_content(sorted_items)
            return filtered_items
    
    def _filter_relevant_content(self, scored_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter out content with low relevance scores"""
        
        initial_count = len(scored_items)
        
        # Define minimum thresholds for content inclusion
        MIN_INTELLIGENCE_SCORE = 0.01  # Must have at least 1% intelligence score
        MIN_PRIORITY_SCORE = 0.001     # Or some priority score
        
        filtered_items = []
        
        for item in scored_items:
            intelligence_score = item.get('intelligence_score', 0)
            priority_score = item.get('priority_score', 0)
            priority_topics = item.get('detected_priority_topics', [])
            
            # Keep items that meet any of these criteria:
            # 1. Intelligence score above minimum threshold
            # 2. Has priority topics detected (even with low score)
            # 3. Priority score above minimum threshold
            should_include = (
                intelligence_score >= MIN_INTELLIGENCE_SCORE or
                len(priority_topics) > 0 or
                priority_score >= MIN_PRIORITY_SCORE
            )
            
            if should_include:
                filtered_items.append(item)
            else:
                # Log filtered items for debugging
                title = item.get('title', 'Unknown')[:50]
                print(f"   🚫 Filtered: '{title}...' (score: {intelligence_score:.3f}, priority: {priority_score:.3f})")
        
        filtered_count = len(filtered_items)
        removed_count = initial_count - filtered_count
        
        if removed_count > 0:
            print(f"   🔍 Content filtering: {removed_count} low-relevance items removed ({initial_count} → {filtered_count})")
        else:
            print(f"   ✅ Content filtering: All {initial_count} items meet relevance criteria")
        
        # Sort by intelligence score descending
        return sorted(filtered_items, key=lambda x: x.get('intelligence_score', 0), reverse=True)
    
    def _calculate_fallback_score(self, item: Dict[str, Any]) -> float:
        """Fallback scoring when priority topics not available"""
        
        # Use unified score if available
        if 'unified_score' in item:
            return item['unified_score']
        
        # Basic engagement scoring
        channel_rating = item.get('channel_rating', 3.0) / 5.0
        priority_bonus = 0.2 if item.get('priority') == 'high' else 0.0
        
        return min(channel_rating + priority_bonus, 1.0)
    
    def _format_time_age(self, age_days: float) -> str:
        """Convert age in days to human-friendly format"""
        
        if age_days < 0.041667:  # Less than 1 hour (1/24 days)
            minutes = int(age_days * 24 * 60)
            if minutes < 1:
                return "Just now"
            return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
        elif age_days < 1:  # Less than 1 day
            hours = int(age_days * 24)
            return f"{hours} hour{'s' if hours != 1 else ''} ago"
        else:  # 1+ days
            days = int(age_days)
            return f"{days} day{'s' if days != 1 else ''} ago"
    
    def _format_score_display(self, score: float, score_type: str = "intelligence") -> str:
        """Convert scores to user-friendly format"""
        
        if score <= 0:
            return "No score"
        elif score < 0.01:  # Less than 1%
            if score_type == "priority":
                return "Low priority" 
            else:
                return "Low relevance"
        else:
            # Convert to percentage
            percentage = score * 100
            if percentage >= 10:
                return f"{percentage:.0f}%"
            else:
                return f"{percentage:.1f}%"

    def _extract_priority_topics_data(self, scored_content: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extract priority topics data for HTML template"""
        
        priority_topics = {}
        
        for item in scored_content:
            detected_topics = item.get('detected_priority_topics', [])
            for topic in detected_topics:
                if topic not in priority_topics:
                    priority_topics[topic] = {
                        'count': 0,
                        'items': [],
                        'avg_score': 0
                    }
                
                priority_topics[topic]['count'] += 1
                priority_topics[topic]['items'].append(item)
        
        # Calculate average scores
        for topic, data in priority_topics.items():
            if data['items']:
                data['avg_score'] = round(
                    sum(item.get('priority_score', 0) for item in data['items']) / len(data['items']), 3
                )
                # Keep only top 3 items per topic
                data['items'] = sorted(data['items'], key=lambda x: x.get('priority_score', 0), reverse=True)[:3]
        
        return priority_topics
    
    def _generate_html_digest(self, digest_data: Dict[str, Any]) -> str:
        """Generate HTML digest using blueprint template"""
        
        template_file = self.templates_dir / "content-digest-blueprint.html"
        
        try:
            with open(template_file, 'r') as f:
                template = f.read()
        except Exception as e:
            print(f"❌ Error reading template: {e}")
            return self._generate_fallback_html(digest_data)
        
        # Generate priority topics content
        priority_topics_html = ""
        for topic, data in digest_data['priority_topics'].items():
            topic_items_html = ""
            for item in data['items']:
                age_str = self._format_time_age(item.get('content_age_days', 0))
                score_str = self._format_score_display(item.get('priority_score', 0), "priority")
                topic_items_html += f"""
                <div class="content-item">
                    <div class="content-title">
                        <a href="{item.get('video_url') or item.get('url', '')}" target="_blank">
                            {item.get('title', 'Unknown Title')[:80]}...
                        </a>
                    </div>
                    <div class="content-meta">
                        <span class="content-source">{item.get('channel') or item.get('source_name', 'Unknown')}</span>
                        <span class="content-score">{score_str}</span>
                        <span class="content-age">{age_str}</span>
                    </div>
                </div>
                """
            
            priority_topics_html += f"""
            <div class="topic-card">
                <div class="topic-header">
                    <div class="topic-name">{topic}</div>
                    <div class="topic-count">{data['count']} items</div>
                </div>
                {topic_items_html}
            </div>
            """
        
        if not priority_topics_html:
            priority_topics_html = '<div class="no-content">No priority topics detected in recent content.</div>'
        
        # Generate platform content
        platform_content_html = ""
        platforms = {}
        for item in digest_data['content']:
            platform = item.get('platform', 'unknown')
            if platform not in platforms:
                platforms[platform] = []
            platforms[platform].append(item)
        
        for platform, items in platforms.items():
            platform_items_html = ""
            for item in items[:5]:  # Top 5 per platform
                age_str = self._format_time_age(item.get('content_age_days', 0))
                score_str = self._format_score_display(item.get('intelligence_score', 0), "intelligence")
                priority_badge = ""
                if item.get('detected_priority_topics'):
                    priority_badge = f'<span class="priority-badge">Priority</span>'
                
                # Add source type badge
                source_badge = ""
                source_type = item.get('source_type', 'unknown')
                if source_type == 'discovered':
                    source_badge = f'<span class="source-badge discovered">🔍 Discovered</span>'
                elif source_type == 'subscribed':
                    source_badge = f'<span class="source-badge subscribed">📺 Subscribed</span>'
                
                # Get source name with fallback
                source_name = item.get('channel') or item.get('subreddit') or item.get('source_name', 'Unknown')
                if item.get('platform') == 'reddit' and item.get('subreddit'):
                    source_name = f"r/{item.get('subreddit')}"
                
                platform_items_html += f"""
                <div class="content-item">
                    <div class="content-title">
                        <a href="{item.get('video_url') or item.get('reddit_url') or item.get('url', '')}" target="_blank">
                            {item.get('title', 'Unknown Title')[:70]}...
                        </a>
                        {priority_badge}
                        {source_badge}
                    </div>
                    <div class="content-meta">
                        <span class="content-source">{source_name}</span>
                        <span class="content-score">{score_str}</span>
                        <span class="content-age">{age_str}</span>
                    </div>
                </div>
                """
            
            platform_icons = {
                "youtube": "📺",
                "reddit": "🔗", 
                "hackernews": "📰"
            }
            platform_icon = platform_icons.get(platform, "🌐")
            platform_content_html += f"""
            <div class="platform-section">
                <h3 class="platform-title">
                    <span class="platform-icon">{platform_icon}</span>
                    {platform.title()} ({len(items)} items)
                </h3>
                {platform_items_html}
            </div>
            """
        
        # Generate recommendations
        recommendations_html = ""
        if digest_data['content']:
            top_item = digest_data['content'][0]
            recommendations_html += f'<li>🌟 Priority: "{top_item.get("title", "Unknown")[:50]}..." from {top_item.get("channel", "Unknown")}</li>'
            
            if digest_data['high_quality_items'] > 1:
                recommendations_html += f'<li>📚 {digest_data["high_quality_items"]} high-quality items available for deep learning</li>'
            
            priority_count = digest_data['priority_items']
            if priority_count > 0:
                recommendations_html += f'<li>🎯 {priority_count} items match your priority topics - focus on these first</li>'
            
            discovered_count = digest_data['discovered_items']
            if discovered_count > 0:
                recommendations_html += f'<li>🔍 {discovered_count} new discoveries found through dynamic search - explore fresh content sources</li>'
        else:
            recommendations_html = '<li>🔍 Light content day - consider running discovery algorithms to find more sources</li>'
        
        # Replace template variables using string replacement to avoid CSS brace conflicts
        html_content = template.replace("{date}", datetime.now().strftime('%Y-%m-%d'))
        html_content = html_content.replace("{generated_at}", digest_data['generated_at'])
        html_content = html_content.replace("{total_items}", str(digest_data['total_items']))
        html_content = html_content.replace("{high_quality_items}", str(digest_data['high_quality_items']))
        html_content = html_content.replace("{average_score}", str(digest_data['average_score']))
        html_content = html_content.replace("{priority_items}", str(digest_data['priority_items']))
        html_content = html_content.replace("{subscribed_items}", str(digest_data['subscribed_items']))
        html_content = html_content.replace("{discovered_items}", str(digest_data['discovered_items']))
        html_content = html_content.replace("{priority_topics_content}", priority_topics_html)
        html_content = html_content.replace("{platform_content}", platform_content_html)
        html_content = html_content.replace("{recommendations_list}", recommendations_html)
        
        return html_content
    
    def _generate_fallback_html(self, digest_data: Dict[str, Any]) -> str:
        """Generate fallback HTML if template fails"""
        
        return f"""
        <!DOCTYPE html>
        <html>
        <head><title>Daily Content Digest - {datetime.now().strftime('%Y-%m-%d')}</title></head>
        <body>
            <h1>📰 Daily Content Digest</h1>
            <p>Generated: {digest_data['generated_at']}</p>
            <p>Total Items: {digest_data['total_items']}</p>
            <p>High Quality Items: {digest_data['high_quality_items']}</p>
            <p>Average Score: {digest_data['average_score']}</p>
            
            <h2>Content Items</h2>
            {''.join([f'<p>• {item.get("title", "Unknown")} - {item.get("channel", "Unknown")}</p>' for item in digest_data['content'][:10]])}
        </body>
        </html>
        """
    
    def _save_content_digest(self, html_content: str, digest_data: Dict[str, Any], date_str: str):
        """Save content digest files and auto-open in browser"""
        
        # Save latest HTML
        latest_html = self.output_dir / "daily-digest.html"
        with open(latest_html, 'w') as f:
            f.write(html_content)
        
        # Save latest JSON data
        latest_json = self.output_dir / "daily-digest.json"
        with open(latest_json, 'w') as f:
            json.dump(digest_data, f, indent=2)
        
        # Save historical copy
        history_html = self.output_dir / "history" / f"{date_str}-content-digest.html"
        with open(history_html, 'w') as f:
            f.write(html_content)
        
        history_json = self.output_dir / "history" / f"{date_str}-content-digest.json"
        with open(history_json, 'w') as f:
            json.dump(digest_data, f, indent=2)
        
        print(f"💾 Content digest saved:")
        print(f"   📄 HTML: {latest_html}")
        print(f"   📊 JSON: {latest_json}")
        print(f"   📚 History: {history_html}")
        
        # Auto-open in browser
        try:
            # Get absolute path to HTML file
            html_file_path = latest_html.resolve()
            html_url = f"file://{html_file_path}"
            
            # Open in default browser
            webbrowser.open(html_url)
            print(f"🌐 Browser opened successfully: {html_file_path}")
            
        except Exception as e:
            print(f"⚠️  Could not auto-open browser: {e}")
            print(f"   📄 Manual access: file://{latest_html.resolve()}")
            print(f"   💡 Tip: Copy the file path above and open it manually in your browser")

def main():
    """Generate content-only daily digest"""
    generator = ContentDigestGenerator()
    
    print("📰 Content-Only Daily Digest Generator")
    print("=" * 50)
    
    # Generate today's digest
    result = generator.generate_content_digest("today")
    
    if result['status'] == 'existing_found':
        print(f"\n✅ {result['message']}")
        print(f"📄 File: {result['file_path']}")
        
        # Auto-open existing file in browser
        try:
            existing_file = Path(result['file_path'])
            html_file_path = existing_file.resolve()
            html_url = f"file://{html_file_path}"
            
            webbrowser.open(html_url)
            print(f"🌐 Browser opened successfully: {html_file_path}")
            
        except Exception as e:
            print(f"⚠️  Could not auto-open browser: {e}")
            print(f"   📄 Manual access: file://{Path(result['file_path']).resolve()}")
            print(f"   💡 Tip: Copy the file path above and open it manually in your browser")
        
        # Ask if user wants to regenerate
        try:
            response = input("\n🔄 Regenerate digest? (y/n): ")
            if response.lower() == 'y':
                result = generator.generate_content_digest("today", force_regenerate=True)
        except EOFError:
            # Auto-regenerate when running non-interactively
            print("\n🔄 Auto-regenerating digest...")
            result = generator.generate_content_digest("today", force_regenerate=True)
    
    if result['status'] == 'generated':
        digest_data = result['digest_data']
        generation_time = result.get('generation_time', 0)
        
        print(f"\n✅ Content digest generated successfully!")
        print(f"📄 File: {result['file_path']}")
        print(f"⏱️ Generation Time: {generation_time:.2f}s")
        
        # Performance assessment
        if generation_time < 15:
            print(f"🚀 Performance: EXCELLENT (target: <15s)")
        elif generation_time < 30:
            print(f"⚠️ Performance: ACCEPTABLE (target: <15s)")
        else:
            print(f"❌ Performance: NEEDS IMPROVEMENT (target: <15s)")
        
        print(f"\n📊 Summary:")
        print(f"   Total Items: {digest_data['total_items']}")
        print(f"   High Quality: {digest_data['high_quality_items']}")
        print(f"   Average Score: {digest_data['average_score']}")
        print(f"   Priority Topics: {digest_data['priority_items']}")
        
        if digest_data['priority_topics']:
            print(f"\n🎯 Priority Topics Detected:")
            for topic, data in digest_data['priority_topics'].items():
                print(f"   • {topic}: {data['count']} items (avg score: {data['avg_score']})")

if __name__ == "__main__":
    main()