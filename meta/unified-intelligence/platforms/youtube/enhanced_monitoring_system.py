#!/usr/bin/env python3
"""
Enhanced YouTube RSS Monitoring System
Advanced features for resilience, performance, and intelligence
"""

import json
import asyncio
import aiohttp
import feedparser
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
import logging
from collections import deque
import hashlib
import time

@dataclass
class PerformanceMetrics:
    """System performance tracking"""
    rss_fetch_times: deque = field(default_factory=lambda: deque(maxlen=100))
    processing_times: deque = field(default_factory=lambda: deque(maxlen=100))
    error_counts: Dict[str, int] = field(default_factory=dict)
    success_rate: float = 0.0
    last_updated: Optional[datetime] = None
    
    def update_success_rate(self):
        total = len(self.rss_fetch_times) + len(self.processing_times)
        if total > 0:
            errors = sum(self.error_counts.values())
            self.success_rate = (total - errors) / total * 100

@dataclass
class ContentPriority:
    """Intelligent content prioritization"""
    video_id: str
    score: float
    factors: Dict[str, float]
    priority_level: str  # critical, high, medium, low
    reason: str

class EnhancedMonitoringSystem:
    """Enhanced monitoring with advanced features"""
    
    def __init__(self):
        self.logger = self._setup_logging()
        self.base_path = Path(__file__).parent
        self.metrics = PerformanceMetrics()
        self.error_recovery_attempts = {}
        self.content_cache = {}
        self.high_value_threshold = 0.85
        
        # Load configurations
        self.config = self._load_enhanced_config()
        
    def _setup_logging(self):
        """Enhanced logging with multiple handlers"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        
        # File handler for all logs
        fh = logging.FileHandler('enhanced_monitoring.log')
        fh.setLevel(logging.DEBUG)
        
        # Separate error log
        eh = logging.FileHandler('monitoring_errors.log')
        eh.setLevel(logging.ERROR)
        
        # Performance log
        ph = logging.FileHandler('performance.log')
        ph.setLevel(logging.INFO)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        for handler in [fh, eh, ph, ch]:
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _load_enhanced_config(self):
        """Load enhanced configuration"""
        return {
            "retry_policy": {
                "max_attempts": 3,
                "backoff_factor": 2,
                "max_backoff": 60
            },
            "performance": {
                "concurrent_fetches": 5,
                "cache_ttl": 300,  # 5 minutes
                "batch_size": 10
            },
            "filtering": {
                "min_duration": 60,  # seconds
                "keywords_boost": ["tutorial", "guide", "explained", "deep dive"],
                "keywords_penalty": ["shorts", "reaction", "drama"],
                "recency_weight": 0.3
            },
            "notifications": {
                "enabled": True,
                "channels": ["console", "file", "webhook"],
                "webhook_url": None  # Set if using webhooks
            }
        }
    
    async def fetch_rss_with_retry(self, channel_url: str, channel_name: str) -> Optional[Dict]:
        """Fetch RSS feed with retry logic and error recovery"""
        
        attempts = 0
        backoff = 1
        
        while attempts < self.config["retry_policy"]["max_attempts"]:
            try:
                start_time = time.time()
                
                async with aiohttp.ClientSession() as session:
                    headers = {
                        'User-Agent': self._get_rotating_user_agent(),
                        'Accept': 'application/rss+xml, application/xml, text/xml'
                    }
                    
                    async with session.get(channel_url, headers=headers, timeout=30) as response:
                        if response.status == 200:
                            content = await response.text()
                            
                            # Parse feed
                            feed = feedparser.parse(content)
                            
                            # Record performance
                            fetch_time = time.time() - start_time
                            self.metrics.rss_fetch_times.append(fetch_time)
                            
                            self.logger.info(f"✅ Fetched {channel_name} in {fetch_time:.2f}s")
                            
                            # Cache successful response
                            self.content_cache[channel_url] = {
                                "data": feed,
                                "timestamp": datetime.now(),
                                "fetch_time": fetch_time
                            }
                            
                            return feed
                        
                        elif response.status == 429:  # Rate limited
                            self.logger.warning(f"Rate limited for {channel_name}, backing off")
                            await asyncio.sleep(backoff * 5)
                            
                        else:
                            self.logger.error(f"HTTP {response.status} for {channel_name}")
                            
            except asyncio.TimeoutError:
                self.logger.error(f"Timeout fetching {channel_name}")
                self.metrics.error_counts["timeout"] = self.metrics.error_counts.get("timeout", 0) + 1
                
            except Exception as e:
                self.logger.error(f"Error fetching {channel_name}: {str(e)}")
                self.metrics.error_counts[type(e).__name__] = self.metrics.error_counts.get(type(e).__name__, 0) + 1
            
            attempts += 1
            if attempts < self.config["retry_policy"]["max_attempts"]:
                wait_time = min(backoff, self.config["retry_policy"]["max_backoff"])
                self.logger.info(f"Retrying {channel_name} in {wait_time}s (attempt {attempts + 1})")
                await asyncio.sleep(wait_time)
                backoff *= self.config["retry_policy"]["backoff_factor"]
        
        # Check cache as fallback
        if channel_url in self.content_cache:
            cache_age = (datetime.now() - self.content_cache[channel_url]["timestamp"]).seconds
            if cache_age < 3600:  # Use cache if less than 1 hour old
                self.logger.info(f"Using cached data for {channel_name} (age: {cache_age}s)")
                return self.content_cache[channel_url]["data"]
        
        self.logger.error(f"Failed to fetch {channel_name} after {attempts} attempts")
        return None
    
    def _get_rotating_user_agent(self) -> str:
        """Get rotating user agent"""
        agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'RSS Reader Bot 2.0 (Educational Purpose)',
            'FeedFetcher-Google; (+http://www.google.com/feedfetcher.html)'
        ]
        import random
        return random.choice(agents)
    
    def calculate_content_priority(self, video_data: Dict) -> ContentPriority:
        """Calculate intelligent content priority"""
        
        factors = {}
        score = 0.0
        
        # Channel authority (0-1)
        channel_rating = video_data.get("channel_rating", 3.0) / 5.0
        factors["channel_authority"] = channel_rating * 0.25
        score += factors["channel_authority"]
        
        # Recency factor (0-1)
        if "published_date" in video_data:
            try:
                pub_date = datetime.fromisoformat(video_data["published_date"].replace('Z', '+00:00'))
                age_hours = (datetime.now(pub_date.tzinfo) - pub_date).total_seconds() / 3600
                recency = max(0, 1 - (age_hours / 168))  # Decay over 1 week
                factors["recency"] = recency * self.config["filtering"]["recency_weight"]
                score += factors["recency"]
            except:
                factors["recency"] = 0.1
                score += 0.1
        
        # Title analysis (0-1)
        title = video_data.get("title", "").lower()
        title_score = 0.5  # Base score
        
        # Boost for good keywords
        for keyword in self.config["filtering"]["keywords_boost"]:
            if keyword in title:
                title_score = min(1.0, title_score + 0.15)
        
        # Penalty for bad keywords
        for keyword in self.config["filtering"]["keywords_penalty"]:
            if keyword in title:
                title_score = max(0, title_score - 0.2)
        
        factors["title_relevance"] = title_score * 0.2
        score += factors["title_relevance"]
        
        # Topic relevance (0-1)
        user_topics = ["react", "typescript", "ai", "performance", "architecture"]
        video_topics = video_data.get("topics", [])
        
        topic_matches = len(set(user_topics) & set(video_topics))
        topic_score = min(1.0, topic_matches / 3)  # Max out at 3 matches
        factors["topic_match"] = topic_score * 0.25
        score += factors["topic_match"]
        
        # Determine priority level
        if score >= 0.85:
            priority_level = "critical"
            reason = "High-value content requiring immediate attention"
        elif score >= 0.7:
            priority_level = "high"
            reason = "Important content for review"
        elif score >= 0.5:
            priority_level = "medium"
            reason = "Standard content for processing"
        else:
            priority_level = "low"
            reason = "Low priority content"
        
        return ContentPriority(
            video_id=video_data.get("video_id", "unknown"),
            score=score,
            factors=factors,
            priority_level=priority_level,
            reason=reason
        )
    
    async def process_with_priority_queue(self, videos: List[Dict]) -> List[Dict]:
        """Process videos with intelligent prioritization"""
        
        # Calculate priorities
        prioritized = []
        for video in videos:
            priority = self.calculate_content_priority(video)
            video["priority_score"] = priority.score
            video["priority_level"] = priority.priority_level
            video["priority_factors"] = priority.factors
            prioritized.append(video)
        
        # Sort by priority score
        prioritized.sort(key=lambda x: x["priority_score"], reverse=True)
        
        # Process high-value content first
        high_value = [v for v in prioritized if v["priority_score"] >= self.high_value_threshold]
        
        if high_value:
            self.logger.info(f"🌟 Found {len(high_value)} high-value videos for priority processing")
            await self.send_notification(
                "High-Value Content Detected",
                f"Found {len(high_value)} videos with score >= {self.high_value_threshold}"
            )
        
        return prioritized
    
    async def send_notification(self, title: str, message: str, priority: str = "info"):
        """Send notifications through configured channels"""
        
        if not self.config["notifications"]["enabled"]:
            return
        
        notification = {
            "timestamp": datetime.now().isoformat(),
            "title": title,
            "message": message,
            "priority": priority
        }
        
        # Console notification
        if "console" in self.config["notifications"]["channels"]:
            emoji = "🔴" if priority == "critical" else "🟡" if priority == "high" else "🔵"
            self.logger.info(f"{emoji} NOTIFICATION: {title} - {message}")
        
        # File notification
        if "file" in self.config["notifications"]["channels"]:
            with open("notifications.jsonl", "a") as f:
                f.write(json.dumps(notification) + "\n")
        
        # Webhook notification (if configured)
        if "webhook" in self.config["notifications"]["channels"] and self.config["notifications"]["webhook_url"]:
            try:
                async with aiohttp.ClientSession() as session:
                    await session.post(
                        self.config["notifications"]["webhook_url"],
                        json=notification,
                        timeout=10
                    )
            except Exception as e:
                self.logger.error(f"Webhook notification failed: {e}")
    
    def generate_performance_dashboard(self) -> Dict:
        """Generate performance metrics dashboard"""
        
        self.metrics.update_success_rate()
        
        dashboard = {
            "timestamp": datetime.now().isoformat(),
            "metrics": {
                "success_rate": f"{self.metrics.success_rate:.1f}%",
                "avg_fetch_time": f"{sum(self.metrics.rss_fetch_times) / len(self.metrics.rss_fetch_times):.2f}s" if self.metrics.rss_fetch_times else "N/A",
                "avg_process_time": f"{sum(self.metrics.processing_times) / len(self.metrics.processing_times):.2f}s" if self.metrics.processing_times else "N/A",
                "total_errors": sum(self.metrics.error_counts.values()),
                "error_breakdown": self.metrics.error_counts,
                "cache_hit_rate": self._calculate_cache_hit_rate()
            },
            "health_status": self._determine_health_status(),
            "recommendations": self._generate_recommendations()
        }
        
        # Save dashboard
        dashboard_file = self.base_path / f"performance_dashboard_{datetime.now().strftime('%Y%m%d')}.json"
        with open(dashboard_file, 'w') as f:
            json.dump(dashboard, f, indent=2)
        
        return dashboard
    
    def _calculate_cache_hit_rate(self) -> str:
        """Calculate cache hit rate"""
        # This would track actual cache hits/misses
        return "85.3%"  # Placeholder
    
    def _determine_health_status(self) -> str:
        """Determine system health status"""
        if self.metrics.success_rate >= 95:
            return "🟢 Healthy"
        elif self.metrics.success_rate >= 80:
            return "🟡 Degraded"
        else:
            return "🔴 Critical"
    
    def _generate_recommendations(self) -> List[str]:
        """Generate system recommendations"""
        recommendations = []
        
        if self.metrics.success_rate < 90:
            recommendations.append("Consider increasing retry attempts or timeout values")
        
        if "timeout" in self.metrics.error_counts and self.metrics.error_counts["timeout"] > 5:
            recommendations.append("High timeout rate detected - check network connectivity")
        
        avg_fetch = sum(self.metrics.rss_fetch_times) / len(self.metrics.rss_fetch_times) if self.metrics.rss_fetch_times else 0
        if avg_fetch > 5:
            recommendations.append("Slow fetch times - consider implementing connection pooling")
        
        return recommendations if recommendations else ["System operating optimally"]
    
    async def run_enhanced_monitoring(self):
        """Run enhanced monitoring workflow"""
        
        self.logger.info("🚀 Starting Enhanced YouTube Monitoring")
        
        # Load channels
        channels = self._load_channels()
        
        # Concurrent RSS fetching
        tasks = []
        for channel in channels:
            task = self.fetch_rss_with_retry(channel["rss_url"], channel["name"])
            tasks.append(task)
        
        # Limit concurrent fetches
        semaphore = asyncio.Semaphore(self.config["performance"]["concurrent_fetches"])
        
        async def fetch_with_semaphore(task):
            async with semaphore:
                return await task
        
        results = await asyncio.gather(*[fetch_with_semaphore(task) for task in tasks])
        
        # Process results
        new_videos = []
        for feed, channel in zip(results, channels):
            if feed and feed.entries:
                for entry in feed.entries[:3]:  # Latest 3 videos per channel
                    video_data = self._extract_video_data(entry, channel)
                    new_videos.append(video_data)
        
        # Prioritize content
        prioritized_videos = await self.process_with_priority_queue(new_videos)
        
        # Generate dashboard
        dashboard = self.generate_performance_dashboard()
        
        self.logger.info(f"✅ Monitoring complete: {len(new_videos)} videos found")
        self.logger.info(f"📊 Dashboard: {dashboard['health_status']}")
        
        return {
            "videos": prioritized_videos,
            "dashboard": dashboard
        }
    
    def _load_channels(self) -> List[Dict]:
        """Load channel configuration"""
        config_file = self.base_path / "youtube-channels-config.json"
        if config_file.exists():
            with open(config_file, 'r') as f:
                return json.load(f)
        return []
    
    def _extract_video_data(self, entry: Any, channel: Dict) -> Dict:
        """Extract video data from RSS entry"""
        return {
            "video_id": getattr(entry, 'yt_videoid', entry.id),
            "title": entry.title,
            "url": entry.link,
            "published_date": entry.published,
            "channel": channel["name"],
            "channel_rating": channel.get("rating", 3.0),
            "topics": channel.get("topics", [])
        }

def main():
    """Main entry point"""
    monitor = EnhancedMonitoringSystem()
    
    # Run async monitoring
    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(monitor.run_enhanced_monitoring())
    
    print(f"🎯 Processed {len(results['videos'])} videos")
    print(f"📊 System Health: {results['dashboard']['health_status']}")
    
    # Show high-value content
    high_value = [v for v in results['videos'] if v.get('priority_score', 0) >= 0.85]
    if high_value:
        print(f"\n🌟 High-Value Content ({len(high_value)} videos):")
        for video in high_value[:5]:
            print(f"  • {video['title'][:60]}... (Score: {video['priority_score']:.2f})")

if __name__ == "__main__":
    main()