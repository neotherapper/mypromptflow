#!/usr/bin/env python3
"""
Reddit Dynamic Discovery System
Priority Topic Monitoring and Cross-Subreddit Search

This system monitors priority topic subreddits and performs cross-subreddit searches
for high-quality discussions about Claude AI, React, TypeScript, and meta-prompting.
"""

import json
import time
import requests
import feedparser
import praw
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, asdict
import random
import logging
import re
import os
from urllib.parse import urlparse
import hashlib

@dataclass
class RedditPost:
    """Enhanced Reddit post with priority topic scoring"""
    post_id: str
    title: str
    url: str
    permalink: str
    published: str
    subreddit: str
    author: str
    score: int = 0
    num_comments: int = 0
    description: str = ""
    priority_topics: List[str] = None
    topic_score: float = 0.0
    quality_score: float = 0.0
    discovery_method: str = "rss"  # rss, search, manual
    raw_content: str = ""
    crosspost_parent: Optional[str] = None
    is_crosspost: bool = False

@dataclass
class SearchQuery:
    """Search query configuration"""
    terms: List[str]
    priority_topics: List[str]
    subreddits: List[str]
    time_filter: str = "week"
    min_score: int = 50
    max_results: int = 25

@dataclass
class DynamicDiscoveryConfig:
    """Dynamic discovery configuration"""
    priority_subreddits: List[str]
    search_queries: List[SearchQuery]
    quality_thresholds: Dict[str, int]
    rate_limits: Dict[str, float]
    storage_path: str
    reddit_api_config: Dict[str, str]

class RedditDynamicDiscovery:
    """Reddit dynamic discovery system for priority topics"""
    
    def __init__(self, config_path: str = None):
        self.logger = self._setup_logging()
        self.config = self._load_config(config_path)
        self.priority_topics = self._load_priority_topics()
        self.state_file = "reddit-dynamic-discovery-state.json"
        self.state = self._load_state()
        
        # Reddit API setup
        self.reddit_client = self._setup_reddit_client()
        
        # Rate limiting and request management
        self.request_delays = {
            "rss": (2, 4),
            "api": (1, 2),
            "search": (3, 5)
        }
        
        # Priority topic search terms
        self.priority_search_terms = {
            "claude": ["claude", "claude ai", "anthropic claude", "claude code", "claude.ai"],
            "react": ["react", "reactjs", "react.js", "react hooks", "react components"],
            "typescript": ["typescript", "ts", "type safety", "typescript config"],
            "meta-prompting": ["meta prompting", "prompt engineering", "chain of thought", "few shot"]
        }
        
        # Quality indicators
        self.quality_keywords = [
            "comprehensive", "detailed", "guide", "tutorial", "best practices",
            "deep dive", "analysis", "comparison", "review", "benchmark",
            "production", "enterprise", "scalable", "performance", "optimization"
        ]
        
        # Storage setup
        self.storage_path = Path(self.config.storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
    def _setup_logging(self) -> logging.Logger:
        """Set up logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('reddit-dynamic-discovery.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def _load_config(self, config_path: str = None) -> DynamicDiscoveryConfig:
        """Load dynamic discovery configuration"""
        default_config = {
            "priority_subreddits": [
                "Claude", "AnthropicAI", "typescript", "reactjs", 
                "PromptEngineering", "programming", "ChatGPTCoding"
            ],
            "search_queries": [
                {
                    "terms": ["claude", "claude ai", "anthropic"],
                    "priority_topics": ["claude", "claude-code"],
                    "subreddits": ["programming", "MachineLearning", "artificial", "ChatGPT", "LocalLLaMA"],
                    "time_filter": "week",
                    "min_score": 50,
                    "max_results": 25
                },
                {
                    "terms": ["react", "reactjs", "react hooks"],
                    "priority_topics": ["react"],
                    "subreddits": ["webdev", "javascript", "Frontend", "webdevelopment"],
                    "time_filter": "week", 
                    "min_score": 50,
                    "max_results": 25
                },
                {
                    "terms": ["typescript", "ts config", "type safety"],
                    "priority_topics": ["typescript"],
                    "subreddits": ["javascript", "webdev", "programming", "Frontend"],
                    "time_filter": "week",
                    "min_score": 50,
                    "max_results": 25
                },
                {
                    "terms": ["meta prompting", "prompt engineering", "chain of thought"],
                    "priority_topics": ["meta-prompting"],
                    "subreddits": ["MachineLearning", "artificial", "ChatGPT", "LocalLLaMA"],
                    "time_filter": "week",
                    "min_score": 50,
                    "max_results": 25
                }
            ],
            "quality_thresholds": {
                "min_upvotes": 50,
                "min_upvote_ratio": 0.7,
                "min_comments": 5,
                "max_age_days": 7,
                "min_content_length": 100
            },
            "rate_limits": {
                "requests_per_minute": 30,
                "burst_limit": 10
            },
            "storage_path": "/Users/georgiospilitsoglou/Developer/projects/mypromptflow/knowledge-vault/databases/knowledge_vault/content-intelligence/reddit-intelligence/dynamic-discovery/",
            "reddit_api_config": {
                "client_id": os.getenv("REDDIT_CLIENT_ID", ""),
                "client_secret": os.getenv("REDDIT_CLIENT_SECRET", ""),
                "user_agent": "Universal Topic Intelligence System 1.0 by Educational Research"
            }
        }
        
        config_file = config_path or "reddit-dynamic-discovery-config.json"
        if Path(config_file).exists():
            with open(config_file, 'r') as f:
                config_data = json.load(f)
        else:
            config_data = default_config
            with open(config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
        
        # Convert to dataclass
        search_queries = [SearchQuery(**q) for q in config_data["search_queries"]]
        config_data["search_queries"] = search_queries
        
        return DynamicDiscoveryConfig(**config_data)
    
    def _load_priority_topics(self) -> Dict[str, Any]:
        """Load priority topics configuration"""
        topics_file = Path("priority-topics.json")
        if topics_file.exists():
            with open(topics_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _load_state(self) -> Dict[str, Any]:
        """Load discovery state"""
        if Path(self.state_file).exists():
            with open(self.state_file, 'r') as f:
                return json.load(f)
        return {
            "last_run": None,
            "processed_posts": [],
            "search_history": {},
            "discovered_posts": {}
        }
    
    def _save_state(self):
        """Save discovery state"""
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def _setup_reddit_client(self) -> Optional[praw.Reddit]:
        """Set up Reddit API client if credentials available"""
        try:
            if (self.config.reddit_api_config["client_id"] and 
                self.config.reddit_api_config["client_secret"]):
                
                return praw.Reddit(
                    client_id=self.config.reddit_api_config["client_id"],
                    client_secret=self.config.reddit_api_config["client_secret"],
                    user_agent=self.config.reddit_api_config["user_agent"],
                    check_for_async=False
                )
            else:
                self.logger.warning("Reddit API credentials not found, using RSS-only mode")
                return None
        except Exception as e:
            self.logger.error(f"Failed to setup Reddit client: {e}")
            return None
    
    def _calculate_topic_score(self, post: RedditPost) -> float:
        """Calculate priority topic relevance score"""
        if not self.priority_topics:
            return 0.0
        
        score = 0.0
        text_content = f"{post.title} {post.description}".lower()
        
        # Check priority topics
        priority_topics_config = self.priority_topics.get("priority_topics", {})
        
        for topic_name, topic_config in priority_topics_config.items():
            topic_weight = topic_config.get("weight", 0.5)
            keywords = topic_config.get("keywords", [])
            aliases = topic_config.get("aliases", [])
            
            # Check keywords and aliases
            all_terms = keywords + aliases + [topic_name]
            matches = sum(1 for term in all_terms if term.lower() in text_content)
            
            if matches > 0:
                topic_score = matches * topic_weight
                score += topic_score
                
                if not post.priority_topics:
                    post.priority_topics = []
                if topic_name not in post.priority_topics:
                    post.priority_topics.append(topic_name)
        
        # Check topic combinations for bonus scoring
        combinations = self.priority_topics.get("topic_combinations", {})
        for combo_name, combo_config in combinations.items():
            required_topics = combo_config.get("required_topics", [])
            if post.priority_topics and all(topic in post.priority_topics for topic in required_topics):
                bonus = combo_config.get("bonus_multiplier", 0.0)
                score *= (1 + bonus)
        
        return min(score, 3.0)  # Cap at 3.0
    
    def _calculate_quality_score(self, post: RedditPost) -> float:
        """Calculate content quality score"""
        score = 0.0
        
        # Engagement metrics
        if post.score > 0:
            score += min(post.score / 100.0, 2.0)  # Up to 2.0 for high scores
        
        if post.num_comments > 0:
            score += min(post.num_comments / 50.0, 1.0)  # Up to 1.0 for engagement
        
        # Content quality indicators
        title_lower = post.title.lower()
        description_lower = post.description.lower()
        
        quality_indicators = sum(1 for keyword in self.quality_keywords 
                               if keyword in title_lower or keyword in description_lower)
        score += quality_indicators * 0.2
        
        # Length and structure
        total_length = len(post.title) + len(post.description)
        if total_length > 200:
            score += 0.5
        if total_length > 500:
            score += 0.5
        
        # Avoid low-quality patterns
        low_quality_patterns = [
            "help", "how do i", "newbie", "eli5", "quick question",
            "beginner", "stupid question", "please help"
        ]
        
        if any(pattern in title_lower for pattern in low_quality_patterns):
            score *= 0.5
        
        # Reward structured content
        if any(indicator in title_lower for indicator in 
               ["guide", "tutorial", "how to", "comprehensive", "detailed"]):
            score *= 1.3
        
        return min(score, 3.0)  # Cap at 3.0
    
    def _fetch_rss_feed(self, rss_url: str) -> Optional[feedparser.FeedParserDict]:
        """Fetch RSS feed with error handling"""
        try:
            # Random delay for rate limiting
            delay = random.uniform(*self.request_delays["rss"])
            time.sleep(delay)
            
            headers = {
                'User-Agent': 'Universal Topic Intelligence System 1.0 (Educational Research)'
            }
            
            response = requests.get(rss_url, headers=headers, timeout=30)
            if response.status_code == 200:
                feed = feedparser.parse(response.content)
                if len(feed.entries) > 0:
                    return feed
            
            self.logger.warning(f"Failed to fetch RSS feed: {rss_url}")
            return None
            
        except Exception as e:
            self.logger.error(f"Error fetching RSS feed {rss_url}: {e}")
            return None
    
    def _parse_reddit_entry(self, entry, subreddit_name: str, method: str = "rss") -> RedditPost:
        """Parse RSS entry or API submission into RedditPost"""
        if hasattr(entry, 'link'):  # RSS entry
            post_id = entry.link.split('/')[-2] if '/comments/' in entry.link else entry.id
            url = entry.link
            title = entry.title
            published = entry.published
            author = getattr(entry, 'author', 'unknown')
            description = getattr(entry, 'summary', '')
            
            # Extract score and comments from description
            score = 0
            num_comments = 0
            score_match = re.search(r'(\d+) points?', description)
            if score_match:
                score = int(score_match.group(1))
            
            comment_match = re.search(r'(\d+) comments?', description)
            if comment_match:
                num_comments = int(comment_match.group(1))
                
        else:  # PRAW submission
            post_id = entry.id
            url = f"https://reddit.com{entry.permalink}"
            title = entry.title
            published = datetime.fromtimestamp(entry.created_utc).isoformat()
            author = str(entry.author) if entry.author else 'unknown'
            description = entry.selftext or ""
            score = entry.score
            num_comments = entry.num_comments
        
        post = RedditPost(
            post_id=post_id,
            title=title,
            url=url,
            permalink=url,
            published=published,
            subreddit=subreddit_name,
            author=author,
            score=score,
            num_comments=num_comments,
            description=description,
            discovery_method=method,
            raw_content=description
        )
        
        # Calculate scores
        post.topic_score = self._calculate_topic_score(post)
        post.quality_score = self._calculate_quality_score(post)
        
        return post
    
    def _is_quality_post(self, post: RedditPost) -> bool:
        """Check if post meets quality thresholds"""
        thresholds = self.config.quality_thresholds
        
        # Score threshold
        if post.score < thresholds["min_upvotes"]:
            return False
        
        # Comments threshold
        if post.num_comments < thresholds["min_comments"]:
            return False
        
        # Age threshold
        try:
            post_date = datetime.fromisoformat(post.published.replace('Z', '+00:00'))
            if (datetime.now() - post_date).days > thresholds["max_age_days"]:
                return False
        except:
            pass  # Skip age check if parsing fails
        
        # Content length
        total_length = len(post.title) + len(post.description)
        if total_length < thresholds["min_content_length"]:
            return False
        
        # Minimum topic or quality score
        if post.topic_score < 0.5 and post.quality_score < 1.0:
            return False
        
        return True
    
    def _is_processed(self, post_id: str) -> bool:
        """Check if post was already processed"""
        return post_id in self.state.get("processed_posts", [])
    
    def _mark_processed(self, post_id: str):
        """Mark post as processed"""
        if "processed_posts" not in self.state:
            self.state["processed_posts"] = []
        if post_id not in self.state["processed_posts"]:
            self.state["processed_posts"].append(post_id)
    
    def monitor_priority_subreddits(self) -> List[RedditPost]:
        """Monitor priority subreddits via RSS"""
        self.logger.info("Monitoring priority subreddits...")
        
        discovered_posts = []
        
        for subreddit_name in self.config.priority_subreddits:
            try:
                rss_url = f"https://www.reddit.com/r/{subreddit_name}/.rss"
                feed = self._fetch_rss_feed(rss_url)
                
                if not feed:
                    continue
                
                subreddit_posts = []
                for entry in feed.entries:
                    post = self._parse_reddit_entry(entry, subreddit_name, "rss")
                    
                    if (not self._is_processed(post.post_id) and 
                        self._is_quality_post(post)):
                        subreddit_posts.append(post)
                        self._mark_processed(post.post_id)
                
                discovered_posts.extend(subreddit_posts)
                self.logger.info(f"r/{subreddit_name}: Found {len(subreddit_posts)} quality posts")
                
            except Exception as e:
                self.logger.error(f"Error monitoring r/{subreddit_name}: {e}")
                continue
        
        return discovered_posts
    
    def cross_subreddit_search(self) -> List[RedditPost]:
        """Perform cross-subreddit searches for priority topics"""
        if not self.reddit_client:
            self.logger.warning("Reddit API not available, skipping cross-subreddit search")
            return []
        
        self.logger.info("Performing cross-subreddit searches...")
        
        discovered_posts = []
        
        for query_config in self.config.search_queries:
            try:
                # Search across specified subreddits
                for subreddit_name in query_config.subreddits:
                    try:
                        subreddit = self.reddit_client.subreddit(subreddit_name)
                        
                        # Search for each term
                        for search_term in query_config.terms:
                            try:
                                # Rate limiting
                                delay = random.uniform(*self.request_delays["search"])
                                time.sleep(delay)
                                
                                # Perform search
                                search_results = subreddit.search(
                                    search_term,
                                    time_filter=query_config.time_filter,
                                    limit=query_config.max_results,
                                    sort="relevance"
                                )
                                
                                for submission in search_results:
                                    if submission.score >= query_config.min_score:
                                        post = self._parse_reddit_entry(
                                            submission, subreddit_name, "search"
                                        )
                                        
                                        if (not self._is_processed(post.post_id) and 
                                            self._is_quality_post(post)):
                                            discovered_posts.append(post)
                                            self._mark_processed(post.post_id)
                                
                            except Exception as e:
                                self.logger.error(f"Search error for '{search_term}' in r/{subreddit_name}: {e}")
                                continue
                        
                    except Exception as e:
                        self.logger.error(f"Error accessing r/{subreddit_name}: {e}")
                        continue
                
            except Exception as e:
                self.logger.error(f"Error in search query {query_config.terms}: {e}")
                continue
        
        self.logger.info(f"Cross-subreddit search found {len(discovered_posts)} posts")
        return discovered_posts
    
    def save_discovered_posts(self, posts: List[RedditPost], batch_name: str = None):
        """Save discovered posts to JSON files"""
        if not posts:
            return
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        batch_name = batch_name or f"reddit_discovery_{timestamp}"
        
        # Create batch directory
        batch_dir = self.storage_path / batch_name
        batch_dir.mkdir(exist_ok=True)
        
        # Sort posts by combined score
        sorted_posts = sorted(posts, 
                            key=lambda p: p.topic_score + p.quality_score, 
                            reverse=True)
        
        # Save all posts
        all_posts_data = {
            "discovery_timestamp": timestamp,
            "total_posts": len(posts),
            "batch_name": batch_name,
            "posts": [asdict(post) for post in sorted_posts]
        }
        
        with open(batch_dir / "all_posts.json", 'w') as f:
            json.dump(all_posts_data, f, indent=2)
        
        # Save by priority topic
        posts_by_topic = {}
        for post in sorted_posts:
            if post.priority_topics:
                for topic in post.priority_topics:
                    if topic not in posts_by_topic:
                        posts_by_topic[topic] = []
                    posts_by_topic[topic].append(post)
        
        for topic, topic_posts in posts_by_topic.items():
            topic_data = {
                "topic": topic,
                "discovery_timestamp": timestamp,
                "post_count": len(topic_posts),
                "posts": [asdict(post) for post in topic_posts]
            }
            
            with open(batch_dir / f"{topic}_posts.json", 'w') as f:
                json.dump(topic_data, f, indent=2)
        
        # Save high-score posts (digest compatible)
        high_score_posts = [p for p in sorted_posts 
                           if p.topic_score + p.quality_score >= 2.0]
        
        if high_score_posts:
            digest_data = {
                "source": "reddit",
                "discovery_timestamp": timestamp,
                "high_quality_posts": len(high_score_posts),
                "posts": [
                    {
                        "title": post.title,
                        "url": post.url,
                        "subreddit": post.subreddit,
                        "score": post.score,
                        "comments": post.num_comments,
                        "priority_topics": post.priority_topics or [],
                        "topic_score": post.topic_score,
                        "quality_score": post.quality_score,
                        "published": post.published,
                        "discovery_method": post.discovery_method
                    }
                    for post in high_score_posts
                ]
            }
            
            with open(batch_dir / "digest_ready.json", 'w') as f:
                json.dump(digest_data, f, indent=2)
        
        self.logger.info(f"Saved {len(posts)} posts to {batch_dir}")
        return batch_dir
    
    def generate_discovery_report(self, posts: List[RedditPost]) -> str:
        """Generate discovery summary report"""
        if not posts:
            return "No posts discovered in this cycle."
        
        # Statistics
        total_posts = len(posts)
        avg_score = sum(p.score for p in posts) / total_posts
        avg_comments = sum(p.num_comments for p in posts) / total_posts
        
        # Group by subreddit
        by_subreddit = {}
        for post in posts:
            if post.subreddit not in by_subreddit:
                by_subreddit[post.subreddit] = []
            by_subreddit[post.subreddit].append(post)
        
        # Group by priority topic
        by_topic = {}
        for post in posts:
            if post.priority_topics:
                for topic in post.priority_topics:
                    if topic not in by_topic:
                        by_topic[topic] = []
                    by_topic[topic].append(post)
        
        # Top scoring posts
        top_posts = sorted(posts, 
                         key=lambda p: p.topic_score + p.quality_score, 
                         reverse=True)[:10]
        
        report = [
            "=== Reddit Dynamic Discovery Report ===",
            f"Discovery completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total posts discovered: {total_posts}",
            f"Average score: {avg_score:.1f}",
            f"Average comments: {avg_comments:.1f}",
            "",
            "Discovery by subreddit:",
        ]
        
        for subreddit, subreddit_posts in sorted(by_subreddit.items()):
            avg_subreddit_score = sum(p.score for p in subreddit_posts) / len(subreddit_posts)
            report.append(f"  r/{subreddit}: {len(subreddit_posts)} posts (avg score: {avg_subreddit_score:.1f})")
        
        if by_topic:
            report.extend(["", "Discovery by priority topic:"])
            for topic, topic_posts in sorted(by_topic.items()):
                avg_topic_score = sum(p.topic_score for p in topic_posts) / len(topic_posts)
                report.append(f"  {topic}: {len(topic_posts)} posts (avg topic score: {avg_topic_score:.2f})")
        
        report.extend(["", "Top 10 posts by combined score:"])
        for i, post in enumerate(top_posts, 1):
            combined_score = post.topic_score + post.quality_score
            topics_str = ", ".join(post.priority_topics) if post.priority_topics else "none"
            report.append(f"  {i}. [{combined_score:.2f}] {post.title}")
            report.append(f"     r/{post.subreddit} • {post.score} pts • {post.num_comments} comments")
            report.append(f"     Topics: {topics_str}")
            report.append(f"     {post.url}")
            report.append("")
        
        return "\n".join(report)
    
    def run_discovery_cycle(self) -> Dict[str, Any]:
        """Run complete discovery cycle"""
        try:
            self.logger.info("Starting Reddit dynamic discovery cycle")
            
            # Monitor priority subreddits
            rss_posts = self.monitor_priority_subreddits()
            
            # Cross-subreddit search
            search_posts = self.cross_subreddit_search()
            
            # Combine and deduplicate
            all_posts = rss_posts + search_posts
            unique_posts = []
            seen_ids = set()
            
            for post in all_posts:
                if post.post_id not in seen_ids:
                    unique_posts.append(post)
                    seen_ids.add(post.post_id)
            
            # Save results
            batch_dir = self.save_discovered_posts(unique_posts)
            
            # Generate report
            report = self.generate_discovery_report(unique_posts)
            
            # Update state
            self.state["last_run"] = datetime.now().isoformat()
            self.state["discovered_posts"][datetime.now().strftime("%Y-%m-%d")] = len(unique_posts)
            self._save_state()
            
            # Log results
            self.logger.info(f"Discovery cycle completed. Found {len(unique_posts)} unique posts")
            print(report)
            
            return {
                "success": True,
                "posts_discovered": len(unique_posts),
                "rss_posts": len(rss_posts),
                "search_posts": len(search_posts),
                "batch_directory": str(batch_dir) if batch_dir else None,
                "report": report
            }
            
        except Exception as e:
            self.logger.error(f"Discovery cycle failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

def main():
    """Main execution function"""
    discovery = RedditDynamicDiscovery()
    
    print("Reddit Dynamic Discovery System")
    print("=" * 50)
    print(f"Priority subreddits: {len(discovery.config.priority_subreddits)}")
    print(f"Search queries: {len(discovery.config.search_queries)}")
    print(f"Reddit API available: {'Yes' if discovery.reddit_client else 'No'}")
    print(f"Storage path: {discovery.storage_path}")
    print()
    
    # Show priority topics
    if discovery.priority_topics:
        priority_topics = discovery.priority_topics.get("priority_topics", {})
        print(f"Priority topics configured: {', '.join(priority_topics.keys())}")
        print()
    
    # Run discovery cycle
    result = discovery.run_discovery_cycle()
    
    if result["success"]:
        print("✅ Discovery cycle completed successfully")
        print(f"📊 Posts discovered: {result['posts_discovered']}")
        print(f"📡 RSS posts: {result['rss_posts']}")
        print(f"🔍 Search posts: {result['search_posts']}")
        if result["batch_directory"]:
            print(f"💾 Results saved to: {result['batch_directory']}")
        print("\nNext steps:")
        print("1. Process discovered posts for content analysis")
        print("2. Extract key insights and discussions")
        print("3. Update knowledge vault with Reddit intelligence")
        print("4. Integrate with daily digest generator")
    else:
        print(f"❌ Discovery cycle failed: {result['error']}")

if __name__ == "__main__":
    main()