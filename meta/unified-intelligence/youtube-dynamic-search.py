#!/usr/bin/env python3
"""
YouTube Dynamic Search System for Priority Topics
Expands content discovery beyond subscribed channels using search-based content discovery.

Features:
- Dynamic search for priority topics (claude, claude-code, react, typescript, meta-prompting)
- Recency filtering (last 30 days)
- View count and relevance filtering
- Rate limiting and error handling
- JSON output compatible with digest generator
- Configurable search terms and thresholds
"""

import os
import sys
import json
import time
import requests
from pathlib import Path
from datetime import datetime, timezone, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional
import logging
from urllib.parse import quote_plus, urlencode
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class SearchConfig:
    """Configuration for YouTube search parameters"""
    search_terms: Dict[str, List[str]]
    filters: Dict[str, Any]
    thresholds: Dict[str, Any]
    rate_limiting: Dict[str, Any]
    output_settings: Dict[str, Any]

@dataclass
class VideoResult:
    """Structured video result from search"""
    video_id: str
    title: str
    channel_name: str
    channel_id: str
    published_at: datetime
    view_count: int
    duration: str
    description: str
    thumbnail_url: str
    search_term: str
    priority_topic: str
    relevance_score: float
    freshness_score: float
    engagement_score: float
    unified_score: float

class YouTubeDynamicSearcher:
    """Dynamic YouTube search system for priority topics"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.base_path = Path(__file__).parent
        self.config = self._load_config(config_path)
        self.priority_topics = self._load_priority_topics()
        self.results_dir = self._setup_results_directory()
        
        # Rate limiting
        self.last_request_time = 0
        self.requests_count = 0
        self.request_window_start = time.time()
        
    def _load_config(self, config_path: Optional[str] = None) -> SearchConfig:
        """Load or create search configuration"""
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                config_data = json.load(f)
        else:
            # Default configuration
            config_data = {
                "search_terms": {
                    "claude": [
                        "Claude AI tutorial",
                        "Claude Code IDE",
                        "Anthropic Claude development",
                        "Claude AI programming",
                        "Claude Code tutorial",
                        "Claude API development"
                    ],
                    "claude-code": [
                        "Claude Code IDE",
                        "Claude Code tutorial",
                        "Claude Code development",
                        "AI coding assistant",
                        "Claude Code features",
                        "Claude Code workflow"
                    ],
                    "react": [
                        "React TypeScript tutorial",  
                        "React 2024 development",
                        "React hooks advanced",
                        "React best practices",
                        "React performance optimization",
                        "React modern patterns"
                    ],
                    "typescript": [
                        "TypeScript advanced features",
                        "TypeScript React development",
                        "TypeScript 2024 updates",
                        "TypeScript best practices",
                        "TypeScript type safety",
                        "TypeScript modern patterns"
                    ],
                    "meta-prompting": [
                        "prompt engineering techniques",
                        "meta prompting strategies",
                        "AI prompt optimization",
                        "prompt design patterns",
                        "chain of thought prompting",
                        "few shot prompting"
                    ],
                    "nextjs": [
                        "Next.js 14 tutorial",
                        "Next.js App Router",
                        "Next.js TypeScript",
                        "Next.js server components",
                        "Next.js best practices",
                        "Next.js deployment"
                    ]
                },
                "filters": {
                    "published_after_days": 30,
                    "min_view_count": 100,
                    "min_duration_seconds": 120,
                    "max_duration_seconds": 3600,
                    "exclude_shorts": True,
                    "language": "en"
                },
                "thresholds": {
                    "min_relevance_score": 0.6,
                    "min_engagement_score": 0.4,
                    "min_unified_score": 0.5,
                    "max_results_per_term": 10,
                    "max_total_results": 100
                },
                "rate_limiting": {
                    "requests_per_minute": 30,
                    "delay_between_requests": 2.0,
                    "backoff_multiplier": 1.5,
                    "max_retries": 3
                },
                "output_settings": {
                    "include_transcript_preview": False,
                    "include_thumbnail": True,
                    "save_individual_files": True,
                    "generate_summary": True
                }
            }
            
            # Save default config
            config_file = self.base_path / "youtube-search-config.json"
            with open(config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
            logger.info(f"Created default configuration: {config_file}")
        
        return SearchConfig(**config_data)
    
    def _load_priority_topics(self) -> Dict[str, Any]:
        """Load priority topics configuration"""
        topics_file = self.base_path / "priority-topics.json"
        with open(topics_file, 'r') as f:
            return json.load(f)
    
    def _setup_results_directory(self) -> Path:
        """Setup directory structure for search results"""
        # Main knowledge vault path
        main_knowledge_vault = self.base_path.parent.parent / "knowledge-vault" / "databases" / "knowledge_vault" / "content-intelligence"
        results_dir = main_knowledge_vault / "youtube-intelligence" / "dynamic-search"
        results_dir.mkdir(parents=True, exist_ok=True)
        
        # Create subdirectories
        for subdir in ["daily", "by-topic", "summaries"]:
            (results_dir / subdir).mkdir(exist_ok=True)
        
        return results_dir
    
    def _apply_rate_limiting(self):
        """Apply rate limiting between requests"""
        current_time = time.time()
        
        # Reset counter if window expired
        if current_time - self.request_window_start >= 60:
            self.requests_count = 0
            self.request_window_start = current_time
        
        # Check rate limit
        if self.requests_count >= self.config.rate_limiting["requests_per_minute"]:
            sleep_time = 60 - (current_time - self.request_window_start)
            if sleep_time > 0:
                logger.info(f"Rate limit reached, sleeping for {sleep_time:.1f} seconds")
                time.sleep(sleep_time)
                self.requests_count = 0
                self.request_window_start = time.time()
        
        # Delay between requests
        time_since_last = current_time - self.last_request_time
        min_delay = self.config.rate_limiting["delay_between_requests"]
        if time_since_last < min_delay:
            time.sleep(min_delay - time_since_last)
        
        self.last_request_time = time.time()
        self.requests_count += 1
    
    def search_videos_for_topic(self, topic: str, search_terms: List[str]) -> List[VideoResult]:
        """Search for videos for a specific topic"""
        logger.info(f"Searching for topic: {topic} with {len(search_terms)} search terms")
        
        all_results = []
        published_after = datetime.now(timezone.utc) - timedelta(days=self.config.filters["published_after_days"])
        
        for search_term in search_terms:
            try:
                self._apply_rate_limiting()
                results = self._search_youtube_api(search_term, published_after)
                
                # Process and score results
                for result in results:
                    video_result = self._process_search_result(result, search_term, topic)
                    if video_result and self._meets_quality_thresholds(video_result):
                        all_results.append(video_result)
                        
                logger.info(f"Found {len(results)} results for '{search_term}'")
                
            except Exception as e:
                logger.error(f"Error searching for '{search_term}': {str(e)}")
                continue
        
        # Remove duplicates and sort by score
        unique_results = self._deduplicate_results(all_results)
        unique_results.sort(key=lambda x: x.unified_score, reverse=True)
        
        # Limit results per topic
        max_results = self.config.thresholds["max_results_per_term"] * len(search_terms)
        return unique_results[:max_results]
    
    def _search_youtube_api(self, search_term: str, published_after: datetime) -> List[Dict[str, Any]]:
        """Search YouTube API (mock implementation - replace with actual API call)"""
        # This is a mock implementation. In production, you would use:
        # - YouTube Data API v3
        # - Alternative APIs like Invidious
        # - Web scraping (with proper rate limiting)
        
        logger.warning("Using mock YouTube search - replace with actual API implementation")
        
        # Mock results for demonstration
        mock_results = [
            {
                "id": {"videoId": f"mock_{hash(search_term + str(i))}"},
                "snippet": {
                    "title": f"{search_term} - Tutorial {i+1}",
                    "channelTitle": f"Mock Channel {i+1}",
                    "channelId": f"UC{hash(search_term + str(i))}",
                    "publishedAt": (datetime.now(timezone.utc) - timedelta(days=i*5)).isoformat(),
                    "description": f"This is a mock description for {search_term} tutorial {i+1}",
                    "thumbnails": {
                        "medium": {"url": f"https://example.com/thumb_{i}.jpg"}
                    }
                },
                "statistics": {
                    "viewCount": str(1000 + i * 500),
                    "likeCount": str(50 + i * 10),
                    "commentCount": str(10 + i * 2)
                },
                "contentDetails": {
                    "duration": f"PT{5 + i}M{30 + i*10}S"
                }
            }
            for i in range(3)  # Mock 3 results per search term
        ]
        
        return mock_results
    
    def _process_search_result(self, result: Dict[str, Any], search_term: str, topic: str) -> Optional[VideoResult]:
        """Process a single search result into VideoResult"""
        try:
            snippet = result["snippet"]
            video_id = result["id"]["videoId"]
            
            # Parse published date
            published_at = datetime.fromisoformat(snippet["publishedAt"].replace('Z', '+00:00'))
            
            # Extract statistics
            stats = result.get("statistics", {})
            view_count = int(stats.get("viewCount", 0))
            like_count = int(stats.get("likeCount", 0))
            comment_count = int(stats.get("commentCount", 0))
            
            # Parse duration
            duration_str = result.get("contentDetails", {}).get("duration", "PT0S")
            duration_seconds = self._parse_duration(duration_str)
            
            # Apply filters
            if not self._passes_filters(view_count, duration_seconds, published_at):
                return None
            
            # Calculate scores
            relevance_score = self._calculate_relevance_score(snippet["title"], snippet["description"], search_term, topic)
            freshness_score = self._calculate_freshness_score(published_at)
            engagement_score = self._calculate_engagement_score(view_count, like_count, comment_count, published_at)
            
            # Calculate unified score
            topic_weight = self.priority_topics["priority_topics"].get(topic, {}).get("weight", 0.5)
            unified_score = (relevance_score * 0.4 + freshness_score * 0.3 + engagement_score * 0.3) * topic_weight
            
            return VideoResult(
                video_id=video_id,
                title=snippet["title"],
                channel_name=snippet["channelTitle"],
                channel_id=snippet["channelId"],
                published_at=published_at,
                view_count=view_count,
                duration=duration_str,
                description=snippet["description"][:500],  # Truncate description
                thumbnail_url=snippet["thumbnails"]["medium"]["url"],
                search_term=search_term,
                priority_topic=topic,
                relevance_score=relevance_score,
                freshness_score=freshness_score,
                engagement_score=engagement_score,
                unified_score=unified_score
            )
            
        except Exception as e:
            logger.error(f"Error processing search result: {str(e)}")
            return None
    
    def _parse_duration(self, duration_str: str) -> int:
        """Parse ISO 8601 duration to seconds"""
        # Simple parser for YouTube duration format (PT#M#S)
        match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration_str)
        if not match:
            return 0
        
        hours = int(match.group(1) or 0)
        minutes = int(match.group(2) or 0)
        seconds = int(match.group(3) or 0)
        
        return hours * 3600 + minutes * 60 + seconds
    
    def _passes_filters(self, view_count: int, duration_seconds: int, published_at: datetime) -> bool:
        """Check if video passes basic filters"""
        filters = self.config.filters
        
        # View count filter
        if view_count < filters["min_view_count"]:
            return False
        
        # Duration filters
        if duration_seconds < filters["min_duration_seconds"]:
            return False
        if duration_seconds > filters["max_duration_seconds"]:
            return False
        
        # Shorts filter
        if filters["exclude_shorts"] and duration_seconds < 60:
            return False
        
        # Date filter
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=filters["published_after_days"])
        if published_at < cutoff_date:
            return False
        
        return True
    
    def _calculate_relevance_score(self, title: str, description: str, search_term: str, topic: str) -> float:
        """Calculate relevance score based on title and description matching"""
        title_lower = title.lower()
        description_lower = description.lower()
        search_term_lower = search_term.lower()
        
        # Get topic keywords
        topic_data = self.priority_topics["priority_topics"].get(topic, {})
        keywords = topic_data.get("keywords", [])
        aliases = topic_data.get("aliases", [])
        
        score = 0.0
        
        # Search term matching
        if search_term_lower in title_lower:
            score += 0.3
        if search_term_lower in description_lower:
            score += 0.2
        
        # Topic keyword matching
        keyword_matches = sum(1 for keyword in keywords if keyword.lower() in title_lower)
        score += min(keyword_matches * 0.1, 0.3)
        
        # Alias matching
        alias_matches = sum(1 for alias in aliases if alias.lower() in title_lower)
        score += min(alias_matches * 0.1, 0.2)
        
        return min(score, 1.0)
    
    def _calculate_freshness_score(self, published_at: datetime) -> float:
        """Calculate freshness score based on publication date"""
        now = datetime.now(timezone.utc)
        days_old = (now - published_at).days
        
        # Apply freshness decay from priority topics
        freshness_decay = self.priority_topics["content_scoring"]["freshness_decay"]
        
        if days_old <= 1:
            return freshness_decay["0-24_hours"]
        elif days_old <= 3:
            return freshness_decay["1-3_days"]
        elif days_old <= 7:
            return freshness_decay["3-7_days"]
        elif days_old <= 30:
            return freshness_decay["7-30_days"]
        else:
            return freshness_decay["30+_days"]
    
    def _calculate_engagement_score(self, view_count: int, like_count: int, comment_count: int, published_at: datetime) -> float:
        """Calculate engagement score based on views, likes, comments"""
        days_old = max((datetime.now(timezone.utc) - published_at).days, 1)
        
        # Normalize by age
        views_per_day = view_count / days_old
        likes_per_day = like_count / days_old
        comments_per_day = comment_count / days_old
        
        # Calculate engagement metrics
        like_ratio = like_count / max(view_count, 1)
        comment_ratio = comment_count / max(view_count, 1)
        
        # Weighted engagement score
        engagement_score = (
            min(views_per_day / 1000, 1.0) * 0.4 +  # Views component
            min(like_ratio * 100, 1.0) * 0.4 +       # Like ratio component
            min(comment_ratio * 1000, 1.0) * 0.2     # Comment ratio component
        )
        
        return min(engagement_score, 1.0)
    
    def _meets_quality_thresholds(self, video_result: VideoResult) -> bool:
        """Check if video meets quality thresholds"""
        thresholds = self.config.thresholds
        
        return (
            video_result.relevance_score >= thresholds["min_relevance_score"] and
            video_result.engagement_score >= thresholds["min_engagement_score"] and
            video_result.unified_score >= thresholds["min_unified_score"]
        )
    
    def _deduplicate_results(self, results: List[VideoResult]) -> List[VideoResult]:
        """Remove duplicate videos from results"""
        seen_ids = set()
        unique_results = []
        
        for result in results:
            if result.video_id not in seen_ids:
                seen_ids.add(result.video_id)
                unique_results.append(result)
        
        return unique_results
    
    def run_dynamic_search(self) -> Dict[str, Any]:
        """Run dynamic search for all priority topics"""
        logger.info("Starting YouTube dynamic search for priority topics")
        
        search_results = {}
        all_videos = []
        
        # Search for each priority topic
        for topic, search_terms in self.config.search_terms.items():
            logger.info(f"Searching for topic: {topic}")
            
            topic_results = self.search_videos_for_topic(topic, search_terms)
            search_results[topic] = topic_results
            all_videos.extend(topic_results)
            
            logger.info(f"Found {len(topic_results)} quality videos for {topic}")
        
        # Sort all videos by unified score
        all_videos.sort(key=lambda x: x.unified_score, reverse=True)
        
        # Limit total results
        max_total = self.config.thresholds["max_total_results"]
        top_videos = all_videos[:max_total]
        
        # Generate comprehensive results
        results = {
            "search_metadata": {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "framework_version": "1.0.0",
                "search_type": "dynamic_youtube_search",
                "topics_searched": list(self.config.search_terms.keys()),
                "total_search_terms": sum(len(terms) for terms in self.config.search_terms.values()),
                "total_videos_found": len(all_videos),
                "quality_videos_selected": len(top_videos)
            },
            "search_configuration": {
                "filters": asdict(self.config)["filters"],
                "thresholds": asdict(self.config)["thresholds"],
                "rate_limiting": asdict(self.config)["rate_limiting"]
            },
            "results_by_topic": {
                topic: [asdict(video) for video in videos]
                for topic, videos in search_results.items()
            },
            "top_videos": [asdict(video) for video in top_videos],
            "summary_statistics": self._generate_summary_statistics(search_results, top_videos)
        }
        
        # Save results
        self._save_search_results(results)
        
        logger.info(f"Dynamic search completed: {len(top_videos)} quality videos found")
        return results
    
    def _generate_summary_statistics(self, search_results: Dict[str, List[VideoResult]], top_videos: List[VideoResult]) -> Dict[str, Any]:
        """Generate summary statistics for search results"""
        if not top_videos:
            return {}
        
        # Calculate averages
        avg_unified_score = sum(v.unified_score for v in top_videos) / len(top_videos)
        avg_relevance_score = sum(v.relevance_score for v in top_videos) / len(top_videos)
        avg_engagement_score = sum(v.engagement_score for v in top_videos) / len(top_videos)
        avg_freshness_score = sum(v.freshness_score for v in top_videos) / len(top_videos)
        
        # Topic distribution
        topic_distribution = {}
        for topic, videos in search_results.items():
            topic_distribution[topic] = {
                "total_videos": len(videos),
                "avg_score": sum(v.unified_score for v in videos) / len(videos) if videos else 0,
                "top_video": asdict(max(videos, key=lambda x: x.unified_score)) if videos else None
            }
        
        # Channel analysis
        channel_counts = {}
        for video in top_videos:
            channel_counts[video.channel_name] = channel_counts.get(video.channel_name, 0) + 1
        
        top_channels = sorted(channel_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "averages": {
                "unified_score": round(avg_unified_score, 3),
                "relevance_score": round(avg_relevance_score, 3),
                "engagement_score": round(avg_engagement_score, 3),
                "freshness_score": round(avg_freshness_score, 3)
            },
            "topic_distribution": topic_distribution,
            "top_channels": [{"channel": ch, "video_count": count} for ch, count in top_channels],
            "quality_metrics": {
                "high_relevance_videos": len([v for v in top_videos if v.relevance_score > 0.8]),
                "high_engagement_videos": len([v for v in top_videos if v.engagement_score > 0.7]),
                "fresh_videos": len([v for v in top_videos if v.freshness_score > 0.8])
            }
        }
    
    def _save_search_results(self, results: Dict[str, Any]):
        """Save search results to knowledge vault"""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        date_str = datetime.now().strftime("%Y-%m-%d")
        
        # Save daily results
        daily_file = self.results_dir / "daily" / f"dynamic_search_{date_str}.json"
        with open(daily_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        # Save by topic
        for topic, videos in results["results_by_topic"].items():
            if videos:  # Only save if there are results
                topic_file = self.results_dir / "by-topic" / f"{topic}_{date_str}.json"
                topic_data = {
                    "topic": topic,
                    "search_date": date_str,
                    "videos": videos,
                    "summary": {
                        "total_videos": len(videos),
                        "avg_score": sum(v["unified_score"] for v in videos) / len(videos),
                        "top_video": max(videos, key=lambda x: x["unified_score"])
                    }
                }
                with open(topic_file, 'w') as f:
                    json.dump(topic_data, f, indent=2, default=str)
        
        # Save summary
        summary_file = self.results_dir / "summaries" / f"search_summary_{timestamp}.json"
        summary_data = {
            "timestamp": results["search_metadata"]["timestamp"],
            "total_videos": results["search_metadata"]["total_videos_found"],
            "quality_videos": results["search_metadata"]["quality_videos_selected"],
            "summary_statistics": results["summary_statistics"],
            "top_10_videos": results["top_videos"][:10]
        }
        with open(summary_file, 'w') as f:
            json.dump(summary_data, f, indent=2, default=str)
        
        # Update latest results (for digest generator compatibility)
        latest_file = self.results_dir / "latest_dynamic_search.json"
        with open(latest_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        logger.info(f"Results saved to {self.results_dir}")


def main():
    """Main entry point for YouTube dynamic search"""
    try:
        searcher = YouTubeDynamicSearcher()
        results = searcher.run_dynamic_search()
        
        print("\n🚀 YouTube Dynamic Search Completed!")
        print("=" * 50)
        print(f"📊 Total videos found: {results['search_metadata']['total_videos_found']}")
        print(f"⭐ Quality videos selected: {results['search_metadata']['quality_videos_selected']}")
        print(f"🎯 Topics searched: {', '.join(results['search_metadata']['topics_searched'])}")
        
        # Print top results
        print(f"\n🏆 Top 5 Videos:")
        for i, video in enumerate(results['top_videos'][:5], 1):
            print(f"{i}. {video['title']} ({video['channel_name']})")
            print(f"   Score: {video['unified_score']:.3f} | Topic: {video['priority_topic']}")
        
        print(f"\n📁 Results saved to: {searcher.results_dir}")
        
    except Exception as e:
        logger.error(f"Error in dynamic search: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()