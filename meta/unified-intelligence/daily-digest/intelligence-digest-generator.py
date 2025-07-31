#!/usr/bin/env python3
"""
Intelligence Digest Generator for Unified Intelligence System
Generates personalized daily intelligence digests across all platforms
"""

import json
import os
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
import sys

# Add parent paths for imports
sys.path.append(str(Path(__file__).parent.parent))

class IntelligenceDigestGenerator:
    """Generates personalized intelligence digests"""
    
    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = base_path or Path(__file__).parent.parent
        self.knowledge_vault = self.base_path / "knowledge-vault"
        self.preferences_file = self.base_path / "user-preferences.json"
        
        # Load user preferences
        self.user_preferences = self._load_user_preferences()
        
    def _load_user_preferences(self) -> Dict[str, Any]:
        """Load user preferences for personalization"""
        if self.preferences_file.exists():
            with open(self.preferences_file, 'r') as f:
                return json.load(f)
        return {}
    
    def generate_daily_digest(self, digest_type: str = "system_wide") -> Dict[str, Any]:
        """Generate daily intelligence digest"""
        
        print(f"📰 Generating {digest_type} intelligence digest...")
        
        # Collect content from all platforms
        content_items = self._collect_recent_content()
        
        # Score and rank content
        scored_content = self._score_and_rank_content(content_items)
        
        # Generate digest sections
        digest = {
            "metadata": {
                "digest_type": digest_type,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "framework_version": "1.0.0",
                "total_items_considered": len(content_items),
                "items_included": len(scored_content[:20])  # Top 20 items
            },
            "sections": self._create_digest_sections(scored_content[:20]),
            "summary": self._create_digest_summary(scored_content[:20]),
            "recommendations": self._create_recommendations(scored_content)
        }
        
        # Save digest
        self._save_digest(digest, digest_type)
        
        return digest
    
    def _collect_recent_content(self) -> List[Dict[str, Any]]:
        """Collect recent content from all platforms"""
        
        content_items = []
        
        # Collect YouTube content
        youtube_content = self._collect_youtube_content()
        content_items.extend(youtube_content)
        
        # Collect GitHub content (placeholder for now)
        github_content = self._collect_github_content()
        content_items.extend(github_content)
        
        # Additional platforms would be added here
        
        print(f"   📊 Collected {len(content_items)} items from all platforms")
        
        return content_items
    
    def _collect_youtube_content(self) -> List[Dict[str, Any]]:
        """Collect recent YouTube content"""
        
        youtube_content = []
        
        # Look for YouTube intelligence in knowledge vault
        youtube_vault = self.knowledge_vault / "youtube-intelligence"
        
        if not youtube_vault.exists():
            return youtube_content
        
        # Get recent content from various channels
        for channel_dir in youtube_vault.iterdir():
            if channel_dir.is_dir():
                # Get today's content
                today = datetime.now().strftime('%Y-%m-%d')
                today_dir = channel_dir / today
                
                if today_dir.exists():
                    for content_file in today_dir.glob("*_unified_*.json"):
                        try:
                            with open(content_file, 'r') as f:
                                content = json.load(f)
                                content['platform'] = 'youtube'
                                content['content_file'] = str(content_file)
                                youtube_content.append(content)
                        except Exception as e:
                            print(f"   ❌ Error reading {content_file}: {e}")
        
        return youtube_content
    
    def _collect_github_content(self) -> List[Dict[str, Any]]:
        """Collect recent GitHub content (placeholder)"""
        
        # This would collect from GitHub discovery results
        # For now, return empty list as placeholder
        return []
    
    def _score_and_rank_content(self, content_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Score and rank content based on user preferences and quality"""
        
        scored_items = []
        
        for item in content_items:
            score = self._calculate_content_score(item)
            item['intelligence_score'] = score
            scored_items.append(item)
        
        # Sort by score descending
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
        """Calculate recency bonus for content"""
        
        # For now, give small bonus to all items (they're all recent by definition)
        return 0.05
    
    def _create_digest_sections(self, scored_content: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create structured digest sections"""
        
        sections = {
            "top_priority": [],
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
                "url": item.get('video_url') or item.get('url', ''),
                "topics": item.get('topics', [])
            }
            for item in scored_content if item.get('intelligence_score', 0) > 0.8
        ]
        
        # Group by platform
        for item in scored_content:
            platform = item.get('platform', 'unknown')
            if platform not in sections["by_platform"]:
                sections["by_platform"][platform] = []
            
            sections["by_platform"][platform].append({
                "title": item.get('title', 'Unknown Title')[:60] + "...",
                "source": item.get('channel') or item.get('source_name', 'Unknown'),
                "score": item.get('intelligence_score', 0)
            })
        
        # Group by topic
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
                "top_items": [
                    {
                        "title": item.get('title', 'Unknown Title')[:50] + "...",
                        "source": item.get('channel') or item.get('source_name', 'Unknown')
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
        """Save digest to file"""
        
        # Create digest directory
        digest_dir = self.base_path / "daily-digest" / "generated"
        digest_dir.mkdir(parents=True, exist_ok=True)
        
        # Save with timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        digest_file = digest_dir / f"{digest_type}_{timestamp}.json"
        
        with open(digest_file, 'w') as f:
            json.dump(digest, f, indent=2)
        
        # Also save as "latest" for easy access
        latest_file = digest_dir / f"{digest_type}_latest.json"
        with open(latest_file, 'w') as f:
            json.dump(digest, f, indent=2)
        
        print(f"💾 Digest saved to: {digest_file}")
    
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
    """Generate and display daily digest"""
    generator = IntelligenceDigestGenerator()
    
    print("📰 Daily Intelligence Digest Generator")
    print("=" * 50)
    
    # Generate digest
    digest = generator.generate_daily_digest("system_wide")
    
    # Display summary
    summary = digest.get('summary', {})
    sections = digest.get('sections', {})
    
    print(f"\n📊 Digest Summary:")
    print(f"   Total items: {summary.get('total_items', 0)}")
    print(f"   High quality: {summary.get('high_quality_items', 0)}")
    print(f"   Average score: {summary.get('average_quality_score', 0):.3f}")
    print(f"   {summary.get('recommendation', 'No recommendation')}")
    
    # Show top priority
    top_priority = sections.get('top_priority', [])
    if top_priority:
        print(f"\n🌟 Top Priority Items:")
        for item in top_priority[:3]:
            print(f"   • {item['title'][:50]}... ({item['source']}) - {item['score']:.3f}")
    
    # Show platform breakdown
    by_platform = sections.get('by_platform', {})
    if by_platform:
        print(f"\n📊 Platform Breakdown:")
        for platform, items in by_platform.items():
            print(f"   {platform}: {len(items)} items")
    
    # Generate markdown version
    markdown = generator.generate_markdown_digest(digest)
    
    # Save markdown
    md_file = Path(__file__).parent / "generated" / "latest_digest.md"
    md_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(md_file, 'w') as f:
        f.write(markdown)
    
    print(f"\n📝 Markdown digest saved to: {md_file}")
    print(f"\n✅ Daily digest generation complete!")

if __name__ == "__main__":
    main()