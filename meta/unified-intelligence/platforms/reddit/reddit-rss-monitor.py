#!/usr/bin/env python3
"""
Reddit RSS Monitoring System
Universal Topic Intelligence System - Reddit Feed Monitoring

This script monitors programming-related subreddits via RSS feeds to discover
trending discussions, high-quality technical content, and emerging technologies.
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
class RedditPost:
    """Reddit post entry from RSS feed"""
    post_id: str
    title: str
    url: str
    permalink: str
    published: str
    subreddit: str
    author: str
    score: Optional[int] = None
    num_comments: Optional[int] = None
    description: str = ""

@dataclass
class SubredditConfig:
    """Subreddit configuration"""
    name: str
    rss_url: str
    topics: List[str]
    priority: str = "medium"
    quality_threshold: int = 10  # Minimum score for inclusion
    last_checked: Optional[str] = None
    last_post_id: Optional[str] = None

class RedditRSSMonitor:
    """Reddit RSS feed monitoring for programming content"""
    
    def __init__(self, config_path: str = None):
        self.logger = self._setup_logging()
        self.config_path = config_path or "reddit-subreddits-config.json"
        self.state_file = "reddit-monitor-state.json"
        self.subreddits = self._load_subreddit_config()
        self.state = self._load_state()
        
        # User agents for rotation
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'RSS Reader 1.0 (compatible; Educational Content Aggregator)'
        ]
        
        # Rate limiting for Reddit
        self.request_delay = (3, 6)  # Conservative delays for Reddit
        self.max_retries = 3
        self.retry_delay = 15
    
    def _setup_logging(self) -> logging.Logger:
        """Set up logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('reddit-rss-monitor.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def _load_subreddit_config(self) -> List[SubredditConfig]:
        """Load Reddit subreddit configuration"""
        # High-quality programming subreddits
        default_subreddits = [
            {
                "name": "programming",
                "rss_url": "https://www.reddit.com/r/programming/.rss",
                "topics": ["programming", "software-development", "computer-science", "algorithms"],
                "priority": "high",
                "quality_threshold": 20
            },
            {
                "name": "javascript",
                "rss_url": "https://www.reddit.com/r/javascript/.rss",
                "topics": ["javascript", "web-development", "frontend", "node.js"],
                "priority": "high",
                "quality_threshold": 15
            },
            {
                "name": "reactjs",
                "rss_url": "https://www.reddit.com/r/reactjs/.rss",
                "topics": ["react", "frontend", "javascript", "web-development"],
                "priority": "high",
                "quality_threshold": 15
            },
            {
                "name": "Python",
                "rss_url": "https://www.reddit.com/r/Python/.rss",
                "topics": ["python", "programming", "data-science", "machine-learning"],
                "priority": "high",
                "quality_threshold": 20
            },
            {
                "name": "webdev",
                "rss_url": "https://www.reddit.com/r/webdev/.rss",
                "topics": ["web-development", "frontend", "backend", "full-stack"],
                "priority": "high",
                "quality_threshold": 15
            },
            {
                "name": "MachineLearning",
                "rss_url": "https://www.reddit.com/r/MachineLearning/.rss",
                "topics": ["machine-learning", "artificial-intelligence", "data-science", "deep-learning"],
                "priority": "medium",
                "quality_threshold": 25
            },
            {
                "name": "devops",
                "rss_url": "https://www.reddit.com/r/devops/.rss",
                "topics": ["devops", "infrastructure", "deployment", "automation"],
                "priority": "medium",
                "quality_threshold": 10
            },
            {
                "name": "selfhosted",
                "rss_url": "https://www.reddit.com/r/selfhosted/.rss",
                "topics": ["self-hosting", "homelab", "servers", "infrastructure"],
                "priority": "medium",
                "quality_threshold": 15
            }
        ]
        
        if Path(self.config_path).exists():
            with open(self.config_path, 'r') as f:
                data = json.load(f)
                return [SubredditConfig(**sub) for sub in data]
        else:
            # Create default config file
            with open(self.config_path, 'w') as f:
                json.dump(default_subreddits, f, indent=2)
            return [SubredditConfig(**sub) for sub in default_subreddits]
    
    def _load_state(self) -> Dict[str, Any]:
        """Load monitoring state"""
        if Path(self.state_file).exists():
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {"last_run": None, "subreddit_states": {}, "processed_posts": set()}
    
    def _save_state(self):
        """Save monitoring state"""
        # Convert set to list for JSON serialization 
        state_copy = self.state.copy()
        if "processed_posts" in state_copy and isinstance(state_copy["processed_posts"], set):
            state_copy["processed_posts"] = list(state_copy["processed_posts"])
        
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
                
                # Conservative delay for Reddit
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
        """Fetch RSS feed from Reddit"""
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
    
    def _extract_score_from_description(self, description: str) -> Optional[int]:
        """Extract score from Reddit RSS description"""
        # Reddit RSS includes score in HTML description
        score_match = re.search(r'(\d+) points?', description)
        if score_match:
            return int(score_match.group(1))
        return None
    
    def _extract_comments_from_description(self, description: str) -> Optional[int]:
        """Extract comment count from Reddit RSS description"""
        # Reddit RSS includes comment count in HTML description
        comment_match = re.search(r'(\d+) comments?', description)
        if comment_match:
            return int(comment_match.group(1))
        return None
    
    def _parse_reddit_entry(self, entry, subreddit_name: str) -> RedditPost:
        """Parse RSS entry into RedditPost object"""
        # Extract post ID from permalink
        post_id = entry.link.split('/')[-2] if '/comments/' in entry.link else entry.id
        
        # Extract metadata from description
        description = getattr(entry, 'summary', '')
        score = self._extract_score_from_description(description)
        num_comments = self._extract_comments_from_description(description)
        
        return RedditPost(
            post_id=post_id,
            title=entry.title,
            url=entry.link,
            permalink=entry.link,
            published=entry.published,
            subreddit=subreddit_name,
            author=getattr(entry, 'author', 'unknown'),
            score=score,
            num_comments=num_comments,
            description=description
        )
    
    def _is_new_post(self, post: RedditPost, subreddit_name: str) -> bool:
        """Check if post is new since last check"""
        # Check if we've processed this post before
        if "processed_posts" not in self.state:
            self.state["processed_posts"] = set()
        
        processed_posts = set(self.state["processed_posts"]) if isinstance(self.state["processed_posts"], list) else self.state["processed_posts"]
        
        return post.post_id not in processed_posts
    
    def _is_quality_content(self, post: RedditPost, subreddit_config: SubredditConfig) -> bool:
        """Check if post meets quality thresholds"""
        # Score threshold
        if post.score is not None and post.score < subreddit_config.quality_threshold:
            return False
        
        # Title length and quality
        if len(post.title) < 15:  # Too short, likely not substantial
            return False
        
        # Skip common low-quality patterns
        title_lower = post.title.lower()
        skip_patterns = [
            'eli5', 'help', 'how do i', 'newbie', 'beginner question',
            'simple question', 'stupid question', 'quick question'
        ]
        
        if any(pattern in title_lower for pattern in skip_patterns):
            return False
        
        # Programming relevance keywords
        programming_keywords = [
            'api', 'framework', 'library', 'algorithm', 'database', 'performance',
            'architecture', 'design pattern', 'best practice', 'tutorial', 'guide',
            'open source', 'deployment', 'testing', 'debugging', 'optimization'
        ]
        
        # Check for programming relevance
        text_content = f"{title_lower} {post.description.lower()}"
        keyword_matches = sum(1 for keyword in programming_keywords if keyword in text_content)
        
        # Topic relevance
        topic_matches = sum(1 for topic in subreddit_config.topics if topic.replace('-', ' ') in text_content)
        
        # Calculate relevance score
        relevance_score = (keyword_matches * 0.3 + topic_matches * 0.4) / max(len(post.title.split()), 1)
        
        # Lower threshold for high-priority subreddits
        threshold = 0.05 if subreddit_config.priority == "high" else 0.1
        
        return relevance_score >= threshold or keyword_matches > 0
    
    def monitor_subreddit(self, subreddit: SubredditConfig) -> List[RedditPost]:
        """Monitor a single subreddit for new posts"""
        self.logger.info(f"Monitoring subreddit: r/{subreddit.name}")
        
        feed = self._fetch_rss_feed(subreddit.rss_url)
        if not feed:
            return []
        
        new_posts = []
        
        for entry in feed.entries:
            post = self._parse_reddit_entry(entry, subreddit.name)
            
            if self._is_new_post(post, subreddit.name) and self._is_quality_content(post, subreddit):
                new_posts.append(post)
                self.logger.info(f"New quality post found: {post.title} (Score: {post.score})")
        
        # Update subreddit state
        if feed.entries:
            latest_post = self._parse_reddit_entry(feed.entries[0], subreddit.name)
            self.state["subreddit_states"][subreddit.name] = {
                "last_checked": datetime.now().isoformat(),
                "last_post_id": latest_post.post_id
            }
        
        return new_posts
    
    def monitor_all_subreddits(self) -> Dict[str, List[RedditPost]]:
        """Monitor all configured subreddits"""
        self.logger.info("Starting Reddit subreddit monitoring cycle")
        
        all_new_posts = {}
        
        # Sort subreddits by priority
        sorted_subreddits = sorted(
            self.subreddits,
            key=lambda x: {"high": 0, "medium": 1, "low": 2}.get(x.priority, 1)
        )
        
        for subreddit in sorted_subreddits:
            try:
                new_posts = self.monitor_subreddit(subreddit)
                if new_posts:
                    all_new_posts[subreddit.name] = new_posts
                    
                    # Mark posts as processed
                    if "processed_posts" not in self.state:
                        self.state["processed_posts"] = set()
                    
                    for post in new_posts:
                        if isinstance(self.state["processed_posts"], list):
                            self.state["processed_posts"] = set(self.state["processed_posts"])
                        self.state["processed_posts"].add(post.post_id)
                
            except Exception as e:
                self.logger.error(f"Error monitoring subreddit r/{subreddit.name}: {e}")
                continue
        
        # Update global state
        self.state["last_run"] = datetime.now().isoformat()
        self._save_state()
        
        return all_new_posts
    
    def queue_for_content_processing(self, posts: Dict[str, List[RedditPost]]) -> List[Dict[str, Any]]:
        """Queue new posts for content processing"""
        processing_queue = []
        
        for subreddit_name, subreddit_posts in posts.items():
            subreddit_config = next((s for s in self.subreddits if s.name == subreddit_name), None)
            
            for post in subreddit_posts:
                queue_entry = {
                    "post_url": post.url,
                    "post_id": post.post_id,
                    "title": post.title,
                    "subreddit": subreddit_name,
                    "author": post.author,
                    "score": post.score,
                    "comments": post.num_comments,
                    "topics": subreddit_config.topics if subreddit_config else [],
                    "priority": subreddit_config.priority if subreddit_config else "medium",
                    "published_date": post.published,  # Include published date
                    "queued_at": datetime.now().isoformat(),
                    "status": "pending"
                }
                processing_queue.append(queue_entry)
        
        # Save processing queue
        queue_file = "reddit-content-processing-queue.json"
        if Path(queue_file).exists():
            with open(queue_file, 'r') as f:
                existing_queue = json.load(f)
        else:
            existing_queue = []
        
        existing_queue.extend(processing_queue)
        
        with open(queue_file, 'w') as f:
            json.dump(existing_queue, f, indent=2)
        
        self.logger.info(f"Queued {len(processing_queue)} Reddit posts for content processing")
        return processing_queue
    
    def generate_update_report(self, new_posts: Dict[str, List[RedditPost]]) -> str:
        """Generate summary report of new posts found"""
        if not new_posts:
            return "No new relevant Reddit posts found in this monitoring cycle."
        
        report = [
            "=== Reddit Subreddit Monitoring Report ===",
            f"Monitoring run completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Subreddits monitored: {len(self.subreddits)}",
            f"New posts found: {sum(len(posts) for posts in new_posts.values())}",
            ""
        ]
        
        for subreddit_name, posts in new_posts.items():
            subreddit_config = next((s for s in self.subreddits if s.name == subreddit_name), None)
            priority = subreddit_config.priority if subreddit_config else "unknown"
            threshold = subreddit_config.quality_threshold if subreddit_config else 0
            
            report.extend([
                f"📰 r/{subreddit_name} ({priority} priority, min {threshold} score):",
                f"   Found {len(posts)} new posts:"
            ])
            
            for post in posts:
                score_str = f"{post.score} pts" if post.score else "? pts"
                comments_str = f"{post.num_comments} comments" if post.num_comments else "? comments"
                report.append(f"   • {post.title} ({score_str}, {comments_str})")
                report.append(f"     {post.url}")
            report.append("")
        
        return "\n".join(report)
    
    def run_monitoring_cycle(self) -> Dict[str, Any]:
        """Run complete monitoring cycle"""
        try:
            # Monitor all subreddits
            new_posts = self.monitor_all_subreddits()
            
            # Queue for content processing
            processing_queue = self.queue_for_content_processing(new_posts)
            
            # Generate report
            report = self.generate_update_report(new_posts)
            
            # Log results
            self.logger.info(f"Monitoring cycle completed. Found {len(processing_queue)} posts to process.")
            print(report)
            
            return {
                "success": True,
                "new_posts": new_posts,
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
    monitor = RedditRSSMonitor()
    
    print("Reddit RSS Monitoring System")
    print("=" * 40)
    print(f"Configured subreddits: {len(monitor.subreddits)}")
    print(f"High priority subreddits: {len([s for s in monitor.subreddits if s.priority == 'high'])}")
    print()
    
    # Run monitoring cycle
    result = monitor.run_monitoring_cycle()
    
    if result["success"]:
        print("✅ Monitoring cycle completed successfully")
        if result["processing_queue"]:
            print(f"📋 {len(result['processing_queue'])} posts queued for content processing")
            print("\nNext steps:")
            print("1. Analyze Reddit post content and discussions")
            print("2. Extract key insights and trending topics")
            print("3. Update knowledge vault with Reddit intelligence")
    else:
        print(f"❌ Monitoring cycle failed: {result['error']}")

if __name__ == "__main__":
    main()