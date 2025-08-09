#!/usr/bin/env python3
"""
HackerNews RSS Monitoring System
Universal Topic Intelligence System - HackerNews Feed Monitoring

This script monitors HackerNews RSS feeds to discover trending tech discussions,
startup insights, and emerging technologies with high engagement.
"""

import json
import time
import requests
import feedparser
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
import random
import logging
import re

@dataclass
class HNStory:
    """HackerNews story entry from RSS feed"""
    story_id: str
    title: str
    url: str
    hn_url: str  # HackerNews discussion URL
    published: str
    author: str
    score: Optional[int] = None
    num_comments: Optional[int] = None
    category: str = "general"

@dataclass
class HNFeedConfig:
    """HackerNews feed configuration"""
    name: str
    rss_url: str
    topics: List[str]
    priority: str = "medium"
    min_score: int = 50  # Minimum score for inclusion
    min_comments: int = 10  # Minimum comments for inclusion
    category: str = "general"

class HackerNewsRSSMonitor:
    """HackerNews RSS feed monitoring for tech content"""
    
    def __init__(self, config_path: str = None):
        self.logger = self._setup_logging()
        self.config_path = config_path or "hackernews-feeds-config.json"
        self.state_file = "hackernews-monitor-state.json"
        self.feeds = self._load_feed_config()
        self.state = self._load_state()
        
        # User agents for rotation
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'RSS Reader 1.0 (compatible; Tech News Aggregator)'
        ]
        
        # Conservative rate limiting for HackerNews
        self.request_delay = (2, 4)
        self.max_retries = 3
        self.retry_delay = 10
    
    def _setup_logging(self) -> logging.Logger:
        """Set up logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('hackernews-rss-monitor.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def _load_feed_config(self) -> List[HNFeedConfig]:
        """Load HackerNews feed configuration"""
        # Key HackerNews RSS feeds
        default_feeds = [
            {
                "name": "front_page",
                "rss_url": "https://hnrss.org/frontpage",
                "topics": ["technology", "startups", "programming", "innovation"],
                "priority": "high",
                "min_score": 100,
                "min_comments": 20,
                "category": "front_page"
            },
            {
                "name": "new_stories",
                "rss_url": "https://hnrss.org/newest",
                "topics": ["technology", "programming", "startups"],
                "priority": "medium",
                "min_score": 50,
                "min_comments": 10,
                "category": "new"
            },
            {
                "name": "best_stories",
                "rss_url": "https://hnrss.org/best",
                "topics": ["technology", "innovation", "programming"],
                "priority": "high",
                "min_score": 200,
                "min_comments": 50,
                "category": "best"
            },
            {
                "name": "ask_hn",
                "rss_url": "https://hnrss.org/ask",
                "topics": ["discussion", "advice", "community", "career"],
                "priority": "medium",
                "min_score": 30,
                "min_comments": 15,
                "category": "ask"
            },
            {
                "name": "show_hn", 
                "rss_url": "https://hnrss.org/show",
                "topics": ["projects", "demos", "open-source", "innovation"],
                "priority": "high",
                "min_score": 50,
                "min_comments": 10,
                "category": "show"
            },
            {
                "name": "programming",
                "rss_url": "https://hnrss.org/frontpage?q=programming",
                "topics": ["programming", "software-development", "coding"],
                "priority": "high",
                "min_score": 50,
                "min_comments": 15,
                "category": "programming"
            },
            {
                "name": "ai_ml",
                "rss_url": "https://hnrss.org/frontpage?q=AI+OR+machine+learning+OR+artificial+intelligence",
                "topics": ["artificial-intelligence", "machine-learning", "ai"],
                "priority": "high",
                "min_score": 75,
                "min_comments": 20,
                "category": "ai"
            }
        ]
        
        if Path(self.config_path).exists():
            with open(self.config_path, 'r') as f:
                data = json.load(f)
                return [HNFeedConfig(**feed) for feed in data]
        else:
            # Create default config file
            with open(self.config_path, 'w') as f:
                json.dump(default_feeds, f, indent=2)
            return [HNFeedConfig(**feed) for feed in default_feeds]
    
    def _load_state(self) -> Dict[str, Any]:
        """Load monitoring state"""
        if Path(self.state_file).exists():
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {"last_run": None, "feed_states": {}, "processed_stories": set()}
    
    def _save_state(self):
        """Save monitoring state"""
        # Convert set to list for JSON serialization
        state_copy = self.state.copy()
        if "processed_stories" in state_copy and isinstance(state_copy["processed_stories"], set):
            state_copy["processed_stories"] = list(state_copy["processed_stories"])
        
        with open(self.state_file, 'w') as f:
            json.dump(state_copy, f, indent=2)
    
    def _get_random_user_agent(self) -> str:
        """Get random user agent for request rotation"""
        return random.choice(self.user_agents)
    
    def _make_request_with_retry(self, url: str, max_retries: int = None) -> Optional[requests.Response]:
        """Make HTTP request with retry logic"""
        max_retries = max_retries or self.max_retries
        
        for attempt in range(max_retries):
            try:
                headers = {
                    'User-Agent': self._get_random_user_agent(),
                    'Accept': 'application/rss+xml, application/xml, text/xml',
                    'Accept-Language': 'en-US,en;q=0.9',
                }
                
                # Delay to be respectful to HackerNews
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
        """Fetch RSS feed from HackerNews"""
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
    
    def _extract_hn_metadata(self, entry) -> tuple[Optional[int], Optional[int], str]:
        """Extract score, comments, and HN discussion URL from entry"""
        # hnrss.org includes metadata in the description
        description = getattr(entry, 'summary', '')
        
        # Extract score
        score = None
        score_match = re.search(r'(\d+) points?', description)
        if score_match:
            score = int(score_match.group(1))
        
        # Extract comments count
        comments = None
        comment_match = re.search(r'(\d+) comments?', description)
        if comment_match:
            comments = int(comment_match.group(1))
        
        # HN discussion URL is usually in the entry link or comments link
        hn_url = entry.link
        if 'item?id=' not in hn_url:
            # Try to find HN URL in description
            hn_match = re.search(r'https://news\.ycombinator\.com/item\?id=\d+', description)
            if hn_match:
                hn_url = hn_match.group(0)
        
        return score, comments, hn_url
    
    def _parse_hn_entry(self, entry, feed_config: HNFeedConfig) -> HNStory:
        """Parse RSS entry into HNStory object"""
        # Extract HN story ID from URL
        story_id = re.search(r'id=(\d+)', entry.link)
        story_id = story_id.group(1) if story_id else entry.id
        
        # Extract metadata
        score, comments, hn_url = self._extract_hn_metadata(entry)
        
        # Determine the actual content URL vs HN discussion
        content_url = entry.link
        if 'news.ycombinator.com' in entry.link:
            # This is already the HN discussion, look for content URL in description
            content_match = re.search(r'href="([^"]+)"', getattr(entry, 'summary', ''))
            if content_match and 'ycombinator.com' not in content_match.group(1):
                content_url = content_match.group(1)
        
        return HNStory(
            story_id=story_id,
            title=entry.title,
            url=content_url,
            hn_url=hn_url,
            published=entry.published,
            author=getattr(entry, 'author', 'unknown'),
            score=score,
            num_comments=comments,
            category=feed_config.category
        )
    
    def _is_new_story(self, story: HNStory, feed_name: str) -> bool:
        """Check if story is new since last check"""
        # Check if we've processed this story before
        if "processed_stories" not in self.state:
            self.state["processed_stories"] = set()
        
        processed_stories = set(self.state["processed_stories"]) if isinstance(self.state["processed_stories"], list) else self.state["processed_stories"]
        
        return story.story_id not in processed_stories
    
    def _is_quality_content(self, story: HNStory, feed_config: HNFeedConfig) -> bool:
        """Check if story meets quality thresholds"""
        # Score threshold
        if story.score is not None and story.score < feed_config.min_score:
            return False
        
        # Comments threshold
        if story.num_comments is not None and story.num_comments < feed_config.min_comments:
            return False
        
        # Title quality
        if len(story.title) < 10:
            return False
        
        # Programming/tech relevance keywords
        tech_keywords = [
            'programming', 'software', 'developer', 'code', 'algorithm', 'database',
            'api', 'framework', 'library', 'open source', 'github', 'startup',
            'technology', 'ai', 'machine learning', 'cryptocurrency', 'blockchain',
            'cloud', 'devops', 'security', 'privacy', 'performance', 'scaling'
        ]
        
        title_lower = story.title.lower()
        
        # Check for tech relevance
        keyword_matches = sum(1 for keyword in tech_keywords if keyword in title_lower)
        
        # Topic relevance
        topic_matches = sum(1 for topic in feed_config.topics if topic.replace('-', ' ') in title_lower)
        
        # Special handling for different categories
        if feed_config.category in ['ask', 'show']:
            # Lower threshold for Ask HN and Show HN
            return keyword_matches > 0 or topic_matches > 0 or feed_config.category in title_lower
        
        # Calculate relevance score
        relevance_score = (keyword_matches * 0.4 + topic_matches * 0.6) / max(len(story.title.split()), 1)
        
        # Threshold based on priority
        threshold = 0.1 if feed_config.priority == "high" else 0.2
        
        return relevance_score >= threshold or keyword_matches >= 2
    
    def monitor_feed(self, feed_config: HNFeedConfig) -> List[HNStory]:
        """Monitor a single HackerNews feed"""
        self.logger.info(f"Monitoring HN feed: {feed_config.name}")
        
        feed = self._fetch_rss_feed(feed_config.rss_url)
        if not feed:
            return []
        
        new_stories = []
        
        for entry in feed.entries:
            story = self._parse_hn_entry(entry, feed_config)
            
            if self._is_new_story(story, feed_config.name) and self._is_quality_content(story, feed_config):
                new_stories.append(story)
                self.logger.info(f"New quality story found: {story.title} (Score: {story.score}, Comments: {story.num_comments})")
        
        # Update feed state
        if feed.entries:
            latest_story = self._parse_hn_entry(feed.entries[0], feed_config)
            self.state["feed_states"][feed_config.name] = {
                "last_checked": datetime.now().isoformat(),
                "last_story_id": latest_story.story_id
            }
        
        return new_stories
    
    def monitor_all_feeds(self) -> Dict[str, List[HNStory]]:
        """Monitor all configured HackerNews feeds"""
        self.logger.info("Starting HackerNews feed monitoring cycle")
        
        all_new_stories = {}
        
        # Sort feeds by priority
        sorted_feeds = sorted(
            self.feeds,
            key=lambda x: {"high": 0, "medium": 1, "low": 2}.get(x.priority, 1)
        )
        
        for feed_config in sorted_feeds:
            try:
                new_stories = self.monitor_feed(feed_config)
                if new_stories:
                    all_new_stories[feed_config.name] = new_stories
                    
                    # Mark stories as processed
                    if "processed_stories" not in self.state:
                        self.state["processed_stories"] = set()
                    
                    for story in new_stories:
                        if isinstance(self.state["processed_stories"], list):
                            self.state["processed_stories"] = set(self.state["processed_stories"])
                        self.state["processed_stories"].add(story.story_id)
                
            except Exception as e:
                self.logger.error(f"Error monitoring feed {feed_config.name}: {e}")
                continue
        
        # Update global state
        self.state["last_run"] = datetime.now().isoformat()
        self._save_state()
        
        return all_new_stories
    
    def queue_for_content_processing(self, stories: Dict[str, List[HNStory]]) -> List[Dict[str, Any]]:
        """Queue new stories for content processing"""
        processing_queue = []
        
        for feed_name, feed_stories in stories.items():
            feed_config = next((f for f in self.feeds if f.name == feed_name), None)
            
            for story in feed_stories:
                queue_entry = {
                    "story_url": story.url,
                    "hn_url": story.hn_url,
                    "story_id": story.story_id,
                    "title": story.title,
                    "author": story.author,
                    "score": story.score,
                    "comments": story.num_comments,
                    "category": story.category,
                    "feed": feed_name,
                    "topics": feed_config.topics if feed_config else [],
                    "priority": feed_config.priority if feed_config else "medium",
                    "published_date": story.published,
                    "queued_at": datetime.now().isoformat(),
                    "status": "pending"
                }
                processing_queue.append(queue_entry)
        
        # Save processing queue
        queue_file = "hackernews-content-processing-queue.json"
        if Path(queue_file).exists():
            with open(queue_file, 'r') as f:
                existing_queue = json.load(f)
        else:
            existing_queue = []
        
        existing_queue.extend(processing_queue)
        
        with open(queue_file, 'w') as f:
            json.dump(existing_queue, f, indent=2)
        
        self.logger.info(f"Queued {len(processing_queue)} HackerNews stories for content processing")
        return processing_queue
    
    def generate_update_report(self, new_stories: Dict[str, List[HNStory]]) -> str:
        """Generate summary report of new stories found"""
        if not new_stories:
            return "No new relevant HackerNews stories found in this monitoring cycle."
        
        report = [
            "=== HackerNews Feed Monitoring Report ===",
            f"Monitoring run completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Feeds monitored: {len(self.feeds)}",
            f"New stories found: {sum(len(stories) for stories in new_stories.values())}",
            ""
        ]
        
        for feed_name, stories in new_stories.items():
            feed_config = next((f for f in self.feeds if f.name == feed_name), None)
            priority = feed_config.priority if feed_config else "unknown"
            min_score = feed_config.min_score if feed_config else 0
            category = feed_config.category if feed_config else "unknown"
            
            report.extend([
                f"📰 {feed_name} ({category}, {priority} priority, min {min_score} score):",
                f"   Found {len(stories)} new stories:"
            ])
            
            for story in stories:
                score_str = f"{story.score} pts" if story.score else "? pts"
                comments_str = f"{story.num_comments} comments" if story.num_comments else "? comments"
                report.append(f"   • {story.title} ({score_str}, {comments_str})")
                report.append(f"     Content: {story.url}")
                report.append(f"     Discussion: {story.hn_url}")
            report.append("")
        
        return "\n".join(report)
    
    def run_monitoring_cycle(self) -> Dict[str, Any]:
        """Run complete monitoring cycle"""
        try:
            # Monitor all feeds
            new_stories = self.monitor_all_feeds()
            
            # Queue for content processing
            processing_queue = self.queue_for_content_processing(new_stories)
            
            # Generate report
            report = self.generate_update_report(new_stories)
            
            # Log results
            self.logger.info(f"Monitoring cycle completed. Found {len(processing_queue)} stories to process.")
            print(report)
            
            return {
                "success": True,
                "new_stories": new_stories,
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
    monitor = HackerNewsRSSMonitor()
    
    print("HackerNews RSS Monitoring System")
    print("=" * 40)
    print(f"Configured feeds: {len(monitor.feeds)}")
    print(f"High priority feeds: {len([f for f in monitor.feeds if f.priority == 'high'])}")
    print()
    print("Feed categories:")
    categories = {}
    for feed in monitor.feeds:
        categories[feed.category] = categories.get(feed.category, 0) + 1
    for category, count in categories.items():
        print(f"  • {category}: {count} feeds")
    print()
    
    # Run monitoring cycle
    result = monitor.run_monitoring_cycle()
    
    if result["success"]:
        print("✅ Monitoring cycle completed successfully")
        if result["processing_queue"]:
            print(f"📋 {len(result['processing_queue'])} stories queued for content processing")
            print("\nNext steps:")
            print("1. Analyze HackerNews story content and discussions")
            print("2. Extract trending topics and community insights")
            print("3. Update knowledge vault with HackerNews intelligence")
    else:
        print(f"❌ Monitoring cycle failed: {result['error']}")

if __name__ == "__main__":
    main()