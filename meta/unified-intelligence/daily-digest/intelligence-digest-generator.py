#!/usr/bin/env python3
"""
Intelligence Digest Generator for Unified Intelligence System
Generates personalized daily intelligence digests across all platforms
"""

import json
import os
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
import sys
import importlib.util

# Add parent paths for imports
sys.path.append(str(Path(__file__).parent.parent))

# Import the topic scoring engine
try:
    # Import with proper file name (hyphenated)
    import importlib.util
    spec = importlib.util.spec_from_file_location("topic_scoring_engine", 
                                                str(Path(__file__).parent.parent / "topic-scoring-engine.py"))
    topic_scoring_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(topic_scoring_module)
    TopicScoringEngine = topic_scoring_module.TopicScoringEngine
    TOPIC_SCORING_AVAILABLE = True
    print("✅ Topic scoring engine imported successfully")
except Exception as e:
    print(f"⚠️  Topic scoring engine not available - using fallback scoring: {e}")
    TOPIC_SCORING_AVAILABLE = False
    TopicScoringEngine = None

class IntelligenceDigestGenerator:
    """Generates personalized intelligence digests"""
    
    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = base_path or Path(__file__).parent.parent
        # Updated paths to use main knowledge-vault structure
        self.knowledge_vault = Path(__file__).parent.parent.parent.parent / "knowledge-vault" / "databases" / "knowledge_vault" / "content-intelligence"
        self.preferences_file = Path(__file__).parent.parent.parent.parent / "knowledge-vault" / "databases" / "knowledge_vault" / "content-intelligence" / "user-preferences.json"
        
        # Load user preferences
        self.user_preferences = self._load_user_preferences()
        
        # Initialize priority topic scoring engine
        if TOPIC_SCORING_AVAILABLE:
            priority_config_path = self.base_path / "priority-topics.json"
            self.topic_scorer = TopicScoringEngine(str(priority_config_path))
            print("✅ Priority topic scoring engine initialized")
        else:
            self.topic_scorer = None
        
    def _load_user_preferences(self) -> Dict[str, Any]:
        """Load user preferences for personalization"""
        if self.preferences_file.exists():
            with open(self.preferences_file, 'r') as f:
                return json.load(f)
        return {}
    
    def generate_daily_digest(self, digest_type: str = "system_wide", date_range: str = "today") -> Dict[str, Any]:
        """Generate daily intelligence digest with flexible date range"""
        
        print(f"📰 Generating {digest_type} intelligence digest for {date_range}...")
        
        # Collect content from all platforms with date filtering
        content_items = self._collect_recent_content(date_range=date_range)
        
        # Score and rank content
        scored_content = self._score_and_rank_content(content_items)
        
        # Generate digest sections
        digest = {
            "metadata": {
                "digest_type": digest_type,
                "date_range": date_range,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "framework_version": "1.0.0",
                "total_items_considered": len(content_items),
                "items_included": len(scored_content[:20])  # Top 20 items
            },
            "sections": self._create_digest_sections(scored_content[:20]),
            "summary": self._create_digest_summary(scored_content[:20]),
            "recommendations": self._create_recommendations(scored_content)
        }
        
        # Save digest with date range in filename
        self._save_digest(digest, f"{digest_type}_{date_range}")
        
        return digest
    
    def _collect_recent_content(self, date_range: str = "today") -> List[Dict[str, Any]]:
        """Collect recent content from all platforms with date filtering"""
        
        content_items = []
        
        # Collect YouTube content with date range
        youtube_content = self._collect_youtube_content(date_range=date_range)
        content_items.extend(youtube_content)
        
        # Collect GitHub content (placeholder for now)
        github_content = self._collect_github_content()
        content_items.extend(github_content)
        
        # Additional platforms would be added here
        
        print(f"   📊 Collected {len(content_items)} items from all platforms ({date_range})")
        
        return content_items
    
    def _collect_youtube_content(self, date_range: str = "today") -> List[Dict[str, Any]]:
        """Collect recent YouTube content with flexible date range logic"""
        
        youtube_content = []
        
        # Look for YouTube intelligence in knowledge vault
        youtube_vault = self.knowledge_vault / "youtube-intelligence"
        
        if not youtube_vault.exists():
            return youtube_content
        
        # Parse date range and determine date window
        target_dates = self._parse_date_range(date_range)
        
        print(f"   📅 Collecting content from date range: {target_dates[0]} to {target_dates[-1]} ({len(target_dates)} days)")
        
        # Get content from various channels across date range
        for channel_dir in youtube_vault.iterdir():
            if channel_dir.is_dir():
                for date_str in target_dates:
                    date_dir = channel_dir / date_str
                    
                    if date_dir.exists():
                        for content_file in date_dir.glob("*_unified_*.json"):
                            try:
                                with open(content_file, 'r') as f:
                                    content = json.load(f)
                                    content['platform'] = 'youtube'
                                    content['content_file'] = str(content_file)
                                    
                                    # Add content age calculation
                                    content['content_age_days'] = self._calculate_content_age(content)
                                    
                                    youtube_content.append(content)
                            except Exception as e:
                                print(f"   ❌ Error reading {content_file}: {e}")
        
        return youtube_content
    
    def _parse_date_range(self, date_range: str) -> List[str]:
        """Parse date range string and return list of date strings"""
        
        now = datetime.now()
        
        if date_range == "today":
            return [now.strftime('%Y-%m-%d')]
        elif date_range == "yesterday":
            yesterday = now - timedelta(days=1)
            return [yesterday.strftime('%Y-%m-%d')]
        elif date_range == "last_3_days":
            dates = []
            for i in range(3):
                date_str = (now - timedelta(days=i)).strftime('%Y-%m-%d')
                dates.append(date_str)
            return dates
        elif date_range == "last_week" or date_range == "week":
            dates = []
            for i in range(7):
                date_str = (now - timedelta(days=i)).strftime('%Y-%m-%d')
                dates.append(date_str)
            return dates
        elif date_range == "last_2_weeks":
            dates = []
            for i in range(14):
                date_str = (now - timedelta(days=i)).strftime('%Y-%m-%d')
                dates.append(date_str)
            return dates
        else:
            # Default to last 7 days for any unrecognized range
            dates = []
            for i in range(7):
                date_str = (now - timedelta(days=i)).strftime('%Y-%m-%d')
                dates.append(date_str)
            return dates
    
    def _calculate_content_age(self, content: Dict[str, Any]) -> float:
        """Calculate content age in days from published date"""
        
        # Try to get published date from different possible fields
        published_date_str = content.get('published_date') or content.get('published') or content.get('queued_at')
        
        if not published_date_str:
            # If no date available, assume very old (low priority)
            return 999.0
        
        try:
            # Parse the date string (handle various formats)
            if published_date_str.endswith('Z'):
                published_date = datetime.fromisoformat(published_date_str.replace('Z', '+00:00'))
            elif '+' in published_date_str or published_date_str.endswith('00:00'):
                published_date = datetime.fromisoformat(published_date_str)
            else:
                # Fallback: assume UTC if no timezone info
                published_date = datetime.fromisoformat(published_date_str).replace(tzinfo=timezone.utc)
            
            # Calculate age in days
            now = datetime.now(timezone.utc)
            age_delta = now - published_date.replace(tzinfo=timezone.utc)
            age_days = age_delta.total_seconds() / (24 * 3600)  # Convert to days
            
            return max(0.0, age_days)  # Ensure non-negative
            
        except (ValueError, AttributeError) as e:
            print(f"   ⚠️ Error parsing date '{published_date_str}': {e}")
            return 999.0  # Treat as very old if parsing fails
    
    def _collect_github_content(self) -> List[Dict[str, Any]]:
        """Collect recent GitHub content (placeholder)"""
        
        # This would collect from GitHub discovery results
        # For now, return empty list as placeholder
        return []
    
    def _score_and_rank_content(self, content_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Score and rank content based on priority topics and quality"""
        
        if self.topic_scorer and TOPIC_SCORING_AVAILABLE:
            print("🎯 Using priority topic scoring engine")
            
            # Use the advanced topic scoring engine
            scored_objects = self.topic_scorer.score_content_batch(content_items)
            
            # Convert back to dict format with enhanced scoring
            scored_items = []
            for scored_obj in scored_objects:
                # Find original item
                original_item = None
                for item in content_items:
                    if (item.get('title', '') == scored_obj.title and 
                        item.get('url', '') == scored_obj.url):
                        original_item = item
                        break
                
                if original_item:
                    # Add priority scoring data to original item
                    original_item['intelligence_score'] = scored_obj.final_score
                    original_item['priority_score'] = scored_obj.priority_score
                    original_item['detected_priority_topics'] = scored_obj.detected_priority_topics
                    original_item['score_breakdown'] = scored_obj.score_breakdown
                    scored_items.append(original_item)
            
            print(f"   📊 Scored {len(scored_items)} items with priority topic weighting")
            return scored_items
        else:
            print("⚠️  Using fallback scoring (no priority topics)")
            
            # Fallback to original scoring
            scored_items = []
            for item in content_items:
                score = self._calculate_content_score(item)
                item['intelligence_score'] = score
                scored_items.append(item)
            
            return sorted(scored_items, key=lambda x: x.get('intelligence_score', 0), reverse=True)
    
    def _calculate_content_score(self, item: Dict[str, Any]) -> float:
        """Calculate intelligence score for content item"""
        
        base_score = 0.5  # Default base score
        
        # Platform-specific scoring
        if item.get('platform') == 'youtube':
            base_score = self._score_youtube_content(item)
        elif item.get('platform') == 'github':
            base_score = self._score_github_content(item)
        
        # Apply user preference multipliers
        preference_multiplier = self._get_preference_multiplier(item)
        
        # Apply recency bonus (newer content gets slight boost)
        recency_bonus = self._calculate_recency_bonus(item)
        
        final_score = (base_score * preference_multiplier) + recency_bonus
        
        return min(final_score, 1.0)  # Cap at 1.0
    
    def _score_youtube_content(self, item: Dict[str, Any]) -> float:
        """Score YouTube content"""
        
        # Use unified score if available
        if 'unified_score' in item:
            return item['unified_score']
        
        # Fallback scoring
        channel_rating = item.get('channel_rating', 3.0) / 5.0
        priority_bonus = 0.2 if item.get('priority') == 'high' else 0.0
        
        return min(channel_rating + priority_bonus, 1.0)
    
    def _score_github_content(self, item: Dict[str, Any]) -> float:
        """Score GitHub content"""
        
        # Placeholder scoring for GitHub content
        stars = item.get('stars', 0)
        if stars > 10000:
            return 0.9
        elif stars > 1000:
            return 0.7
        else:
            return 0.5
    
    def _get_preference_multiplier(self, item: Dict[str, Any]) -> float:
        """Get user preference multiplier for item"""
        
        multiplier = 1.0
        
        # Channel/source preference
        source_name = item.get('channel') or item.get('source_name', '')
        if source_name:
            channel_key = f"{source_name.lower().replace(' ', '_')}_channel"
            stated_prefs = self.user_preferences.get('stated_preferences', {})
            
            if channel_key in stated_prefs:
                pref_score = stated_prefs[channel_key].get('preference_score', 3.0)
                multiplier *= (pref_score / 3.0)  # Normalize around 1.0
        
        # Topic preference
        topics = item.get('topics', [])
        if topics:
            topic_prefs = self.user_preferences.get('topic_preferences', {})
            topic_scores = []
            
            for topic in topics:
                topic_key = topic.replace('-', '_')
                if topic_key in topic_prefs:
                    topic_scores.append(topic_prefs[topic_key].get('interest_level', 0.6))
                else:
                    topic_scores.append(0.6)
            
            if topic_scores:
                avg_topic_score = sum(topic_scores) / len(topic_scores)
                multiplier *= (avg_topic_score * 1.2 + 0.4)  # Scale to reasonable range
        
        return max(0.5, min(2.0, multiplier))  # Clamp to reasonable range
    
    def _calculate_recency_bonus(self, item: Dict[str, Any]) -> float:
        """Calculate recency bonus based on content age"""
        
        content_age = item.get('content_age_days', 999.0)
        
        # Fresh content (≤1 day) gets maximum bonus
        if content_age <= 1.0:
            return 0.2
        # Recent content (≤3 days) gets good bonus  
        elif content_age <= 3.0:
            return 0.1
        # Week-old content (≤7 days) gets small bonus
        elif content_age <= 7.0:
            return 0.05
        # Older content gets no bonus
        else:
            return 0.0
    
    def _create_digest_sections(self, scored_content: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create structured digest sections with priority topic highlighting"""
        
        sections = {
            "top_priority": [],
            "priority_topics": {},
            "by_platform": {},
            "by_topic": {},
            "recommended_actions": []
        }
        
        # Top priority items (score > 0.8)
        sections["top_priority"] = [
            {
                "title": item.get('title', 'Unknown Title'),
                "source": item.get('channel') or item.get('source_name', 'Unknown'),
                "platform": item.get('platform', 'unknown'),
                "score": item.get('intelligence_score', 0),
                "priority_score": item.get('priority_score', 0),
                "detected_priority_topics": item.get('detected_priority_topics', []),
                "url": item.get('video_url') or item.get('url', ''),
                "topics": item.get('topics', []),
                "content_age_days": item.get('content_age_days', 999.0)
            }
            for item in scored_content if item.get('intelligence_score', 0) > 0.8
        ]
        
        # Group by detected priority topics
        if self.topic_scorer and TOPIC_SCORING_AVAILABLE:
            priority_topic_groups = {}
            for item in scored_content:
                detected_topics = item.get('detected_priority_topics', [])
                for topic in detected_topics:
                    if topic not in priority_topic_groups:
                        priority_topic_groups[topic] = []
                    priority_topic_groups[topic].append(item)
            
            # Create priority topic sections
            for topic, items in priority_topic_groups.items():
                # Sort by priority score
                items_sorted = sorted(items, key=lambda x: x.get('priority_score', 0), reverse=True)
                sections["priority_topics"][topic] = {
                    "count": len(items),
                    "avg_priority_score": sum(item.get('priority_score', 0) for item in items) / len(items),
                    "top_items": [
                        {
                            "title": item.get('title', 'Unknown Title')[:60] + "...",
                            "source": item.get('channel') or item.get('source_name', 'Unknown'),
                            "platform": item.get('platform', 'unknown'),
                            "priority_score": item.get('priority_score', 0),
                            "url": item.get('video_url') or item.get('url', ''),
                            "content_age_days": item.get('content_age_days', 999.0)
                        }
                        for item in items_sorted[:5]  # Top 5 per priority topic
                    ]
                }
        
        # Group by platform
        for item in scored_content:
            platform = item.get('platform', 'unknown')
            if platform not in sections["by_platform"]:
                sections["by_platform"][platform] = []
            
            sections["by_platform"][platform].append({
                "title": item.get('title', 'Unknown Title')[:60] + "...",
                "source": item.get('channel') or item.get('source_name', 'Unknown'),
                "score": item.get('intelligence_score', 0),
                "priority_score": item.get('priority_score', 0),
                "detected_priority_topics": item.get('detected_priority_topics', [])
            })
        
        # Group by topic (general topics, not priority topics)
        topic_counts = {}
        for item in scored_content:
            topics = item.get('topics', [])
            for topic in topics:
                if topic not in topic_counts:
                    topic_counts[topic] = []
                topic_counts[topic].append(item)
        
        # Get top topics by content count
        top_topics = sorted(topic_counts.items(), key=lambda x: len(x[1]), reverse=True)[:5]
        
        for topic, items in top_topics:
            sections["by_topic"][topic] = {
                "count": len(items),
                "avg_score": sum(item.get('intelligence_score', 0) for item in items) / len(items),
                "priority_items_count": len([item for item in items if item.get('detected_priority_topics', [])]),
                "top_items": [
                    {
                        "title": item.get('title', 'Unknown Title')[:50] + "...",
                        "source": item.get('channel') or item.get('source_name', 'Unknown'),
                        "detected_priority_topics": item.get('detected_priority_topics', [])
                    }
                    for item in sorted(items, key=lambda x: x.get('intelligence_score', 0), reverse=True)[:3]
                ]
            }
        
        return sections
    
    def _create_digest_summary(self, scored_content: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create digest summary"""
        
        if not scored_content:
            return {"message": "No content available for today's digest"}
        
        # Calculate summary statistics
        high_quality_count = len([item for item in scored_content if item.get('intelligence_score', 0) > 0.8])
        avg_score = sum(item.get('intelligence_score', 0) for item in scored_content) / len(scored_content)
        
        # Get top sources
        source_counts = {}
        for item in scored_content:
            source = item.get('channel') or item.get('source_name', 'Unknown')
            source_counts[source] = source_counts.get(source, 0) + 1
        
        top_sources = sorted(source_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            "total_items": len(scored_content),
            "high_quality_items": high_quality_count,
            "average_quality_score": round(avg_score, 3),
            "top_sources": [{"source": source, "items": count} for source, count in top_sources],
            "recommendation": self._get_summary_recommendation(high_quality_count, avg_score)
        }
    
    def _get_summary_recommendation(self, high_quality_count: int, avg_score: float) -> str:
        """Get summary recommendation based on content quality"""
        
        if high_quality_count >= 5 and avg_score > 0.8:
            return "Excellent day for learning! Multiple high-quality items available."
        elif high_quality_count >= 3 and avg_score > 0.7:
            return "Good selection of quality content today."
        elif high_quality_count >= 1:
            return "Some quality content available, focus on top-rated items."
        else:
            return "Light day for new content, consider exploring discovery algorithms."
    
    def _create_recommendations(self, scored_content: List[Dict[str, Any]]) -> List[str]:
        """Create actionable recommendations"""
        
        recommendations = []
        
        if not scored_content:
            recommendations.append("Run discovery algorithms to find new content sources")
            return recommendations
        
        # Top item recommendation
        if scored_content:
            top_item = scored_content[0]
            recommendations.append(
                f"🌟 Priority: '{top_item.get('title', 'Unknown')[:50]}...' from {top_item.get('channel', 'Unknown')}"
            )
        
        # High-quality items
        high_quality = [item for item in scored_content if item.get('intelligence_score', 0) > 0.8]
        if len(high_quality) > 1:
            recommendations.append(f"📚 {len(high_quality)} high-quality items available for deep learning")
        
        # Topic focus recommendation
        topic_counts = {}
        for item in scored_content[:10]:  # Top 10 items
            for topic in item.get('topics', []):
                topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
        if topic_counts:
            top_topic = max(topic_counts.items(), key=lambda x: x[1])
            if top_topic[1] >= 3:
                recommendations.append(f"🎯 Strong focus on {top_topic[0]} today ({top_topic[1]} items)")
        
        return recommendations
    
    def _save_digest(self, digest: Dict[str, Any], digest_type: str) -> None:
        """Save digest to file with history tracking"""
        
        # Create digest directory
        digest_dir = self.base_path / "daily-digest" / "generated"
        digest_dir.mkdir(parents=True, exist_ok=True)
        
        # Create history directory
        history_dir = digest_dir / "history"
        history_dir.mkdir(parents=True, exist_ok=True)
        
        # Save with timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        digest_file = digest_dir / f"{digest_type}_{timestamp}.json"
        
        with open(digest_file, 'w') as f:
            json.dump(digest, f, indent=2)
        
        # Also save as "latest" for easy access
        latest_file = digest_dir / f"{digest_type}_latest.json"
        with open(latest_file, 'w') as f:
            json.dump(digest, f, indent=2)
        
        # Update digest history index
        self._update_digest_history(digest, digest_type, timestamp)
        
        print(f"💾 Digest saved to: {digest_file}")
    
    def _update_digest_history(self, digest: Dict[str, Any], digest_type: str, timestamp: str) -> None:
        """Update digest history index for day-over-day comparisons"""
        
        history_dir = self.base_path / "daily-digest" / "generated" / "history"
        history_index_file = history_dir / "digest_history.json"
        
        # Load existing history
        if history_index_file.exists():
            with open(history_index_file, 'r') as f:
                history_index = json.load(f)
        else:
            history_index = {"digests": []}
        
        # Extract key metrics for history tracking
        metadata = digest.get('metadata', {})
        summary = digest.get('summary', {})
        
        history_entry = {
            "timestamp": timestamp,
            "digest_type": digest_type,
            "date_range": metadata.get('date_range', 'unknown'),
            "generated_at": metadata.get('generated_at'),
            "total_items": summary.get('total_items', 0),
            "high_quality_items": summary.get('high_quality_items', 0),
            "average_score": summary.get('average_quality_score', 0),
            "recommendation": summary.get('recommendation', ''),
            "top_sources": summary.get('top_sources', []),
            "file_path": f"{digest_type}_{timestamp}.json"
        }
        
        # Add to history (keep last 90 days)
        history_index["digests"].append(history_entry)
        
        # Sort by timestamp and keep last 90 entries
        history_index["digests"].sort(key=lambda x: x["timestamp"], reverse=True)
        history_index["digests"] = history_index["digests"][:90]
        
        # Update metadata
        history_index["last_updated"] = datetime.now(timezone.utc).isoformat()
        history_index["total_digests"] = len(history_index["digests"])
        
        # Save updated history
        with open(history_index_file, 'w') as f:
            json.dump(history_index, f, indent=2)
        
        print(f"📈 History updated: {len(history_index['digests'])} digests tracked")
    
    def get_digest_history(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get digest history for the last N days"""
        
        history_dir = self.base_path / "daily-digest" / "generated" / "history"
        history_index_file = history_dir / "digest_history.json"
        
        if not history_index_file.exists():
            return []
        
        with open(history_index_file, 'r') as f:
            history_index = json.load(f)
        
        # Filter to last N days
        cutoff_date = datetime.now() - timedelta(days=days)
        cutoff_timestamp = cutoff_date.strftime('%Y-%m-%d')
        
        recent_digests = [
            entry for entry in history_index.get("digests", [])
            if entry["timestamp"] >= cutoff_timestamp
        ]
        
        return recent_digests
    
    def compare_with_yesterday(self) -> Dict[str, Any]:
        """Compare today's digest with yesterday's for trends"""
        
        history = self.get_digest_history(days=2)
        
        if len(history) < 2:
            return {"comparison": "insufficient_data", "message": "Need at least 2 days of data for comparison"}
        
        # Get today's and yesterday's digests (system_wide, today)
        today_digests = [d for d in history if d["date_range"] == "today" and d["digest_type"] == "system_wide"]
        
        if len(today_digests) < 2:
            return {"comparison": "insufficient_data", "message": "Need today and yesterday system_wide digests"}
        
        today = today_digests[0]  # Most recent
        yesterday = today_digests[1]  # Previous
        
        # Calculate trends
        item_trend = today["total_items"] - yesterday["total_items"]
        quality_trend = today["high_quality_items"] - yesterday["high_quality_items"]
        score_trend = today["average_score"] - yesterday["average_score"]
        
        comparison = {
            "comparison": "success",
            "today": {
                "total_items": today["total_items"],
                "high_quality_items": today["high_quality_items"],
                "average_score": today["average_score"]
            },
            "yesterday": {
                "total_items": yesterday["total_items"],
                "high_quality_items": yesterday["high_quality_items"],
                "average_score": yesterday["average_score"]
            },
            "trends": {
                "item_change": item_trend,
                "quality_change": quality_trend,
                "score_change": round(score_trend, 3),
                "trend_summary": self._generate_trend_summary(item_trend, quality_trend, score_trend)
            },
            "generated_at": datetime.now(timezone.utc).isoformat()
        }
        
        return comparison
    
    def _generate_trend_summary(self, item_trend: int, quality_trend: int, score_trend: float) -> str:
        """Generate human-readable trend summary"""
        
        trends = []
        
        if item_trend > 0:
            trends.append(f"+{item_trend} more items")
        elif item_trend < 0:
            trends.append(f"{item_trend} fewer items")
        
        if quality_trend > 0:
            trends.append(f"+{quality_trend} more high-quality")
        elif quality_trend < 0:
            trends.append(f"{quality_trend} fewer high-quality")
        
        if score_trend > 0.05:
            trends.append(f"quality up {score_trend:.2f}")
        elif score_trend < -0.05:
            trends.append(f"quality down {abs(score_trend):.2f}")
        
        if not trends:
            return "Similar to yesterday"
        
        return "; ".join(trends)
    
    def generate_markdown_digest(self, digest: Dict[str, Any]) -> str:
        """Generate markdown version of digest"""
        
        metadata = digest.get('metadata', {})
        sections = digest.get('sections', {})
        summary = digest.get('summary', {})
        recommendations = digest.get('recommendations', [])
        
        md_content = f"""# Daily Intelligence Digest
*Generated: {metadata.get('generated_at', 'Unknown')}*
*Framework: {metadata.get('framework_version', 'Unknown')}*

## Summary
- **Total Items**: {summary.get('total_items', 0)}
- **High Quality**: {summary.get('high_quality_items', 0)}
- **Average Score**: {summary.get('average_quality_score', 0):.3f}
- **Recommendation**: {summary.get('recommendation', 'No recommendation')}

## 🌟 Top Priority Items
"""
        
        top_priority = sections.get('top_priority', [])
        if top_priority:
            for item in top_priority[:5]:
                md_content += f"""
**{item['title']}**
- Source: {item['source']} ({item['platform']})
- Score: {item['score']:.3f}
- Topics: {', '.join(item['topics'])}
- [Link]({item['url']})
"""
        else:
            md_content += "\nNo high-priority items today.\n"
        
        # Platform breakdown
        md_content += "\n## 📊 By Platform\n"
        by_platform = sections.get('by_platform', {})
        for platform, items in by_platform.items():
            md_content += f"\n### {platform.title()}\n"
            for item in items[:3]:  # Top 3 per platform
                md_content += f"- **{item['title']}** ({item['source']}) - Score: {item['score']:.3f}\n"
        
        # Recommendations
        if recommendations:
            md_content += "\n## 💡 Recommendations\n"
            for rec in recommendations:
                md_content += f"- {rec}\n"
        
        return md_content

def main():
    """Generate and display daily digest with flexible date ranges and history tracking"""
    generator = IntelligenceDigestGenerator()
    
    print("📰 Enhanced Daily Intelligence Digest Generator v2.0")
    print("=" * 60)
    
    # Test multiple date ranges to demonstrate new functionality
    test_ranges = ["today", "yesterday", "last_3_days"]
    
    for date_range in test_ranges:
        print(f"\n🔍 Testing {date_range} digest...")
        
        # Generate digest for this date range
        digest = generator.generate_daily_digest("system_wide", date_range=date_range)
        
        # Display summary
        summary = digest.get('summary', {})
        sections = digest.get('sections', {})
        metadata = digest.get('metadata', {})
        
        print(f"\n📊 {date_range.title()} Digest Summary:")
        print(f"   Date range: {metadata.get('date_range', 'unknown')}")
        print(f"   Total items: {summary.get('total_items', 0)}")
        print(f"   High quality: {summary.get('high_quality_items', 0)}")
        print(f"   Average score: {summary.get('average_quality_score', 0):.3f}")
        print(f"   {summary.get('recommendation', 'No recommendation')}")
        
        # Show top priority with content age
        top_priority = sections.get('top_priority', [])
        if top_priority:
            print(f"\n🌟 Top Priority Items ({date_range}):")
            for item in top_priority[:2]:  # Show top 2 for brevity
                age = item.get('content_age_days', 'unknown')
                if isinstance(age, (int, float)):
                    age_str = f"{age:.1f}d"
                else:
                    age_str = str(age)
                print(f"   • {item['title'][:40]}... ({item['source']}) - Score: {item['score']:.3f}, Age: {age_str}")
        
        print("-" * 60)
    
    # Test history tracking
    print(f"\n📈 Testing History Tracking:")
    history = generator.get_digest_history(days=7)
    print(f"   Found {len(history)} digest entries in last 7 days")
    
    # Test day-over-day comparison
    comparison = generator.compare_with_yesterday()
    if comparison.get("comparison") == "success":
        print(f"\n📊 Day-over-Day Comparison:")
        trends = comparison["trends"]
        print(f"   Today: {comparison['today']['total_items']} items, {comparison['today']['high_quality_items']} high-quality")
        print(f"   Yesterday: {comparison['yesterday']['total_items']} items, {comparison['yesterday']['high_quality_items']} high-quality") 
        print(f"   Trend: {trends['trend_summary']}")
    else:
        print(f"\n📊 Day-over-Day Comparison: {comparison.get('message', 'No comparison available')}")
    
    # Generate latest digest (today's) for markdown
    latest_digest = generator.generate_daily_digest("system_wide", date_range="today")
    markdown = generator.generate_markdown_digest(latest_digest)
    
    # Save markdown
    md_file = Path(__file__).parent / "generated" / "latest_digest.md"
    md_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(md_file, 'w') as f:
        f.write(markdown)
    
    print(f"\n📝 Latest digest markdown saved to: {md_file}")
    print(f"\n✅ Enhanced daily digest generation complete!")
    print(f"\n💡 New capabilities:")
    print(f"   • Flexible date ranges (today, yesterday, last_3_days, week)")
    print(f"   • Content age scoring and prioritization") 
    print(f"   • Published date extraction from RSS feeds")
    print(f"   • Historical digest access and comparison")
    print(f"   • Digest history tracking (90-day retention)")
    print(f"   • Day-over-day trend analysis")

if __name__ == "__main__":
    main()