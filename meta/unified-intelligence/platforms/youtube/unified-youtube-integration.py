#!/usr/bin/env python3
"""
Unified YouTube Integration for @meta/unified-intelligence
Adapts existing YouTube monitoring system to work with unified framework
"""

import os
import sys
import json
import yaml
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import dataclass, asdict
from typing import List, Dict, Any, Optional

# Add the original scripts directory to path for imports
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

# Import existing functionality
from youtube_integration_manager import YouTubeIntegrationManager
from youtube_transcript_processor import ProcessedInsights, process_transcript_with_claude

@dataclass
class UnifiedIntelligenceConfig:
    """Configuration for unified intelligence integration"""
    meta_base_path: str
    source_registry_path: str
    user_preferences_path: str
    discovery_framework_path: str
    knowledge_vault_path: str

class UnifiedYouTubeIntegration:
    """Unified YouTube integration with @meta framework"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent.parent
        self.config = self._load_unified_config()
        self.source_registry = self._load_source_registry()
        self.user_preferences = self._load_user_preferences()
        
        # Initialize existing YouTube manager
        self.youtube_manager = YouTubeIntegrationManager()
        
    def _load_unified_config(self) -> UnifiedIntelligenceConfig:
        """Load unified intelligence configuration"""
        return UnifiedIntelligenceConfig(
            meta_base_path=str(self.base_path),
            source_registry_path=str(self.base_path / "source-registry.yaml"),
            user_preferences_path=str(self.base_path / "user-preferences.json"),
            discovery_framework_path=str(self.base_path / "discovery-framework.yaml"),
            knowledge_vault_path=str(self.base_path / "knowledge-vault")
        )
    
    def _load_source_registry(self) -> Dict[str, Any]:
        """Load unified source registry"""
        with open(self.config.source_registry_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _load_user_preferences(self) -> Dict[str, Any]:
        """Load user preferences"""
        with open(self.config.user_preferences_path, 'r') as f:
            return json.load(f)
    
    def get_youtube_sources_from_registry(self) -> List[Dict[str, Any]]:
        """Extract YouTube sources from unified registry"""
        youtube_sources = []
        
        for tier_name, tier_data in self.source_registry['youtube_sources'].items():
            for source in tier_data['sources']:
                # Enhance with unified framework data
                enhanced_source = {
                    **source,
                    'tier': tier_name,
                    'quality_weight': tier_data['quality_weight'],
                    'unified_score': self._calculate_unified_score(source)
                }
                youtube_sources.append(enhanced_source)
        
        return youtube_sources
    
    def _calculate_unified_score(self, source: Dict[str, Any]) -> float:
        """Calculate unified scoring using user preferences and authority"""
        base_authority = source.get('authority_score', 0.8)
        user_pref = source.get('user_preference', 3.0) / 5.0  # Normalize to 0-1
        
        # Apply user preference multiplier
        unified_score = base_authority * (0.5 + user_pref)
        
        return min(unified_score, 1.0)
    
    def process_youtube_backlog_with_unified_framework(self):
        """Process existing YouTube backlog using unified intelligence framework"""
        print(f"🚀 Starting unified YouTube processing at {datetime.now()}")
        
        # Load existing processing queue
        queue_file = current_dir / "transcript-processing-queue.json"
        if not queue_file.exists():
            print("❌ No processing queue found")
            return
        
        with open(queue_file, 'r') as f:
            processing_queue = json.load(f)
        
        print(f"📋 Found {len(processing_queue)} videos in processing queue")
        
        # Process with enhanced scoring
        processed_count = 0
        for video_data in processing_queue:
            if video_data.get('status') == 'pending':
                try:
                    enhanced_result = self._process_video_with_unified_intelligence(video_data)
                    self._store_in_unified_knowledge_vault(enhanced_result)
                    processed_count += 1
                    print(f"✅ Processed: {video_data['title']} (Score: {enhanced_result['unified_score']:.2f})")
                    
                    # Update processing queue
                    video_data['status'] = 'completed'
                    video_data['processed_at'] = datetime.now(timezone.utc).isoformat()
                    video_data['unified_score'] = enhanced_result['unified_score']
                    
                except Exception as e:
                    print(f"❌ Failed to process {video_data['title']}: {str(e)}")
                    video_data['status'] = 'error'
                    video_data['error'] = str(e)
        
        # Save updated queue
        with open(queue_file, 'w') as f:
            json.dump(processing_queue, f, indent=2)
        
        print(f"🎉 Processed {processed_count} videos with unified intelligence framework")
        
        # Generate unified intelligence summary
        self._generate_processing_summary(processing_queue)
    
    def _process_video_with_unified_intelligence(self, video_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process video with enhanced unified intelligence scoring"""
        
        # Get transcript (reuse existing logic)
        video_url = video_data['video_url']
        
        # Use existing transcript processing
        insights = process_transcript_with_claude(video_url, video_data['title'])
        
        # Enhanced scoring with unified framework
        unified_score = self._calculate_enhanced_video_score(video_data, insights)
        
        # Enhanced result with unified framework metadata
        enhanced_result = {
            **video_data,
            'insights': asdict(insights) if insights else None,
            'unified_score': unified_score,
            'processed_with': 'unified-intelligence-framework',
            'framework_version': '1.0.0',
            'processing_timestamp': datetime.now(timezone.utc).isoformat(),
            'user_preference_applied': self._get_user_preference_for_channel(video_data['channel']),
            'cross_platform_potential': self._assess_cross_platform_potential(insights)
        }
        
        return enhanced_result
    
    def _calculate_enhanced_video_score(self, video_data: Dict[str, Any], insights: Optional[ProcessedInsights]) -> float:
        """Calculate enhanced video score using unified framework"""
        
        # Base components
        channel_rating = video_data.get('channel_rating', 3.0) / 5.0  # Normalize to 0-1
        user_preference = self._get_user_preference_for_channel(video_data['channel'])
        
        # Content quality from insights
        content_quality = insights.relevance_score if insights else 0.5
        
        # Topic relevance based on user preferences
        topic_relevance = self._calculate_topic_relevance(video_data.get('topics', []))
        
        # Unified score calculation
        unified_score = (
            channel_rating * 0.3 +
            user_preference * 0.3 +
            content_quality * 0.25 +
            topic_relevance * 0.15
        )
        
        return min(unified_score, 1.0)
    
    def _get_user_preference_for_channel(self, channel_name: str) -> float:
        """Get user preference score for channel"""
        channel_key = f"{channel_name.lower().replace(' ', '_')}_channel"
        
        # Check stated preferences
        stated_prefs = self.user_preferences.get('stated_preferences', {})
        if channel_key in stated_prefs:
            return stated_prefs[channel_key]['preference_score']
        
        # Check for special high-preference channels
        high_pref_channels = ['theprimegen', 'theo', 'fireship']
        if any(pref in channel_name.lower() for pref in high_pref_channels):
            return 0.9
        
        return 0.6  # Default preference
    
    def _calculate_topic_relevance(self, topics: List[str]) -> float:
        """Calculate topic relevance based on user preferences"""
        if not topics:
            return 0.5
        
        topic_prefs = self.user_preferences.get('topic_preferences', {})
        
        relevance_scores = []
        for topic in topics:
            # Direct topic match
            if topic in topic_prefs:
                relevance_scores.append(topic_prefs[topic]['interest_level'])
            # Partial matches
            elif any(topic in pref_topic for pref_topic in topic_prefs.keys()):
                relevance_scores.append(0.7)
            else:
                relevance_scores.append(0.5)
        
        return sum(relevance_scores) / len(relevance_scores) if relevance_scores else 0.5
    
    def _assess_cross_platform_potential(self, insights: Optional[ProcessedInsights]) -> Dict[str, Any]:
        """Assess potential for cross-platform intelligence connections"""
        if not insights:
            return {"potential": "low", "platforms": []}
        
        cross_platform = {"potential": "medium", "platforms": []}
        
        # Check for GitHub repository mentions
        if any("github" in tool.lower() for tool in insights.tools_mentioned):
            cross_platform["platforms"].append("github")
        
        # Check for Reddit-worthy discussions
        if insights.relevance_score > 0.8:
            cross_platform["platforms"].append("reddit")
        
        # Check for official announcements
        if any(keyword in insights.summary.lower() for keyword in ["release", "announcement", "update"]):
            cross_platform["platforms"].append("official_sources")
            cross_platform["potential"] = "high"
        
        return cross_platform
    
    def _store_in_unified_knowledge_vault(self, enhanced_result: Dict[str, Any]):
        """Store processed result in unified knowledge vault"""
        
        # Create knowledge vault directory structure
        vault_base = Path(self.config.knowledge_vault_path)
        
        # Organize by channel and date
        channel_name = enhanced_result['channel'].lower().replace(' ', '-')
        process_date = datetime.now().strftime('%Y-%m-%d')
        
        channel_dir = vault_base / "youtube-intelligence" / channel_name / process_date
        channel_dir.mkdir(parents=True, exist_ok=True)
        
        # Store enhanced result
        video_id = enhanced_result.get('video_id', 'unknown')
        result_file = channel_dir / f"{video_id}_unified_intelligence.json"
        
        with open(result_file, 'w') as f:
            json.dump(enhanced_result, f, indent=2)
        
        # Store insights separately for easy access
        if enhanced_result.get('insights'):
            insights_file = channel_dir / f"{video_id}_insights.json"
            with open(insights_file, 'w') as f:
                json.dump(enhanced_result['insights'], f, indent=2)
    
    def _generate_processing_summary(self, processing_queue: List[Dict[str, Any]]):
        """Generate unified intelligence processing summary"""
        
        completed_videos = [v for v in processing_queue if v.get('status') == 'completed']
        
        if not completed_videos:
            return
        
        # Calculate summary statistics
        avg_score = sum(v.get('unified_score', 0) for v in completed_videos) / len(completed_videos)
        high_value_videos = [v for v in completed_videos if v.get('unified_score', 0) > 0.8]
        
        # Organize by channel
        by_channel = {}
        for video in completed_videos:
            channel = video['channel']
            if channel not in by_channel:
                by_channel[channel] = []
            by_channel[channel].append(video)
        
        # Generate summary
        summary = {
            "processing_summary": {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "framework_version": "1.0.0",
                "videos_processed": len(completed_videos),
                "average_unified_score": round(avg_score, 3),
                "high_value_videos": len(high_value_videos),
                "channels_processed": list(by_channel.keys())
            },
            "top_videos": sorted(
                [{"title": v["title"], "channel": v["channel"], "score": v.get("unified_score", 0)}
                 for v in completed_videos],
                key=lambda x: x["score"],
                reverse=True
            )[:10],
            "channel_performance": {
                channel: {
                    "videos": len(videos),
                    "avg_score": round(sum(v.get('unified_score', 0) for v in videos) / len(videos), 3)
                }
                for channel, videos in by_channel.items()
            }
        }
        
        # Save summary
        summary_file = Path(self.config.knowledge_vault_path) / "youtube-intelligence" / "processing-summary.json"
        summary_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        print(f"📊 Generated processing summary: {len(completed_videos)} videos, avg score: {avg_score:.3f}")
        print(f"🌟 High-value videos (>0.8): {len(high_value_videos)}")
        
    def monitor_youtube_sources_with_unified_framework(self):
        """Monitor YouTube sources using unified framework configuration"""
        print("🔍 Starting unified YouTube monitoring...")
        
        # Get sources from unified registry
        youtube_sources = self.get_youtube_sources_from_registry()
        
        print(f"📺 Monitoring {len(youtube_sources)} YouTube sources from unified registry")
        
        # Use existing monitoring logic but with enhanced sources
        return self.youtube_manager.monitor_channels_from_config(youtube_sources)

def main():
    """Main entry point for unified YouTube integration"""
    integration = UnifiedYouTubeIntegration()
    
    print("🚀 Unified YouTube Intelligence Integration")
    print("=" * 50)
    
    # Process existing backlog with unified framework
    integration.process_youtube_backlog_with_unified_framework()
    
    print("\n" + "=" * 50)
    print("✅ Unified YouTube integration completed!")
    print(f"📁 Results stored in: {integration.config.knowledge_vault_path}")

if __name__ == "__main__":
    main()