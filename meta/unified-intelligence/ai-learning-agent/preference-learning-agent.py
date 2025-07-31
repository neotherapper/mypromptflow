#!/usr/bin/env python3
"""
AI Preference Learning Agent for Unified Intelligence System
Learns from user feedback to improve content recommendations and source discovery
"""

import json
import os
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional, Tuple
import math

@dataclass
class LearningEvent:
    """Single learning event from user interaction"""
    timestamp: str
    event_type: str  # 'like', 'dislike', 'save', 'share', 'time_spent', 'source_promotion', 'source_demotion'
    content_id: str
    content_type: str  # 'youtube_video', 'github_repo', 'reddit_post', etc.
    source_name: str
    topics: List[str]
    engagement_value: float  # Normalized engagement score
    context_data: Dict[str, Any]

class PreferenceLearningAgent:
    """AI agent that learns user preferences and adapts the system"""
    
    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = base_path or Path(__file__).parent.parent
        self.preferences_file = self.base_path / "user-preferences.json"
        self.learning_log_file = self.base_path / "ai-learning-agent" / "learning-events.json"
        
        # Learning parameters
        self.adaptation_rate = 0.1
        self.decay_factor = 0.05
        self.minimum_data_points = 3
        self.confidence_threshold = 0.7
        
        # Load current state
        self.preferences = self._load_preferences()
        self.learning_history = self._load_learning_history()
        
    def _load_preferences(self) -> Dict[str, Any]:
        """Load current user preferences"""
        if self.preferences_file.exists():
            with open(self.preferences_file, 'r') as f:
                return json.load(f)
        else:
            return self._initialize_default_preferences()
    
    def _load_learning_history(self) -> List[LearningEvent]:
        """Load learning event history"""
        if self.learning_log_file.exists():
            with open(self.learning_log_file, 'r') as f:
                events_data = json.load(f)
                return [LearningEvent(**event) for event in events_data]
        else:
            return []
    
    def _initialize_default_preferences(self) -> Dict[str, Any]:
        """Initialize default preferences structure"""
        return {
            "stated_preferences": {
                "theprimegen_channel": {"preference_score": 5.0, "topics": ["software-engineering", "vim", "programming"]},
                "theo_t3gg_channel": {"preference_score": 5.0, "topics": ["typescript", "react", "modern-web-dev"]},
                "official_sources": {"preference_score": 1.0, "source_types": ["github_official_repos", "official_documentation"]},
                "github_changelogs": {"preference_score": 1.0, "source_types": ["release_notes", "changelogs"]}
            },
            "learned_preferences": {
                "content_patterns": {},
                "source_patterns": {}
            },
            "topic_preferences": {
                "react": {"interest_level": 0.9},
                "typescript": {"interest_level": 0.9},
                "software_engineering": {"interest_level": 0.8},
                "web_development": {"interest_level": 0.8}
            },
            "learning_metadata": {
                "total_learning_events": 0,
                "last_update": datetime.now(timezone.utc).isoformat(),
                "confidence_scores": {}
            }
        }
    
    def record_learning_event(self, event_type: str, content_id: str, content_type: str, 
                            source_name: str, topics: List[str], engagement_value: float,
                            context_data: Optional[Dict[str, Any]] = None) -> None:
        """Record a new learning event"""
        
        event = LearningEvent(
            timestamp=datetime.now(timezone.utc).isoformat(),
            event_type=event_type,
            content_id=content_id,
            content_type=content_type,
            source_name=source_name,
            topics=topics,
            engagement_value=engagement_value,
            context_data=context_data or {}
        )
        
        self.learning_history.append(event)
        self._save_learning_history()
        
        # Trigger learning update
        self._update_preferences_from_event(event)
        
        print(f"🧠 Recorded learning event: {event_type} for {source_name} (engagement: {engagement_value:.2f})")
    
    def _update_preferences_from_event(self, event: LearningEvent) -> None:
        """Update user preferences based on a learning event"""
        
        # Update source preferences
        self._update_source_preferences(event)
        
        # Update topic preferences
        self._update_topic_preferences(event)
        
        # Update content pattern preferences
        self._update_content_pattern_preferences(event)
        
        # Update learning metadata
        self._update_learning_metadata(event)
        
        # Save updated preferences
        self._save_preferences()
    
    def _update_source_preferences(self, event: LearningEvent) -> None:
        """Update preferences for specific sources"""
        
        learned_patterns = self.preferences.setdefault("learned_preferences", {}).setdefault("source_patterns", {})
        
        source_key = f"{event.source_name.lower().replace(' ', '_')}_source"
        
        if source_key not in learned_patterns:
            learned_patterns[source_key] = {
                "preference_score": 0.6,  # Default neutral
                "confidence": 0.0,
                "learning_events": 0,
                "last_updated": event.timestamp
            }
        
        source_pref = learned_patterns[source_key]
        
        # Calculate adjustment based on event type and engagement
        adjustment = self._calculate_preference_adjustment(event)
        
        # Apply adjustment with learning rate
        old_score = source_pref["preference_score"]
        new_score = old_score + (adjustment * self.adaptation_rate)
        source_pref["preference_score"] = max(0.0, min(1.0, new_score))
        
        # Update confidence and metadata
        source_pref["learning_events"] += 1
        source_pref["confidence"] = min(1.0, source_pref["learning_events"] / 10.0)
        source_pref["last_updated"] = event.timestamp
        
        print(f"   📊 Updated {event.source_name} preference: {old_score:.3f} → {source_pref['preference_score']:.3f}")
    
    def _update_topic_preferences(self, event: LearningEvent) -> None:
        """Update preferences for topics"""
        
        topic_prefs = self.preferences.setdefault("topic_preferences", {})
        
        adjustment = self._calculate_preference_adjustment(event)
        
        for topic in event.topics:
            topic_key = topic.replace('-', '_')
            
            if topic_key not in topic_prefs:
                topic_prefs[topic_key] = {"interest_level": 0.6}
            
            old_level = topic_prefs[topic_key]["interest_level"]
            new_level = old_level + (adjustment * self.adaptation_rate * 0.5)  # Half rate for topics
            topic_prefs[topic_key]["interest_level"] = max(0.0, min(1.0, new_level))
            
            if abs(old_level - topic_prefs[topic_key]["interest_level"]) > 0.01:
                print(f"   📚 Updated {topic} interest: {old_level:.3f} → {topic_prefs[topic_key]['interest_level']:.3f}")
    
    def _update_content_pattern_preferences(self, event: LearningEvent) -> None:
        """Update preferences for content patterns"""
        
        content_patterns = self.preferences.setdefault("learned_preferences", {}).setdefault("content_patterns", {})
        
        # Infer content patterns from context data
        if event.context_data:
            patterns = self._extract_content_patterns(event)
            
            adjustment = self._calculate_preference_adjustment(event)
            
            for pattern, strength in patterns.items():
                if pattern not in content_patterns:
                    content_patterns[pattern] = {"preference_score": 0.6, "confidence": 0.0}
                
                old_score = content_patterns[pattern]["preference_score"]
                pattern_adjustment = adjustment * strength * self.adaptation_rate * 0.3
                new_score = old_score + pattern_adjustment
                content_patterns[pattern]["preference_score"] = max(0.0, min(1.0, new_score))
                content_patterns[pattern]["confidence"] = min(1.0, content_patterns[pattern]["confidence"] + 0.1)
    
    def _extract_content_patterns(self, event: LearningEvent) -> Dict[str, float]:
        """Extract content patterns from event context"""
        patterns = {}
        
        context = event.context_data
        
        # Pattern extraction based on content type
        if event.content_type == "youtube_video":
            if context.get("duration_minutes", 0) > 30:
                patterns["long_form_content"] = 0.8
            elif context.get("duration_minutes", 0) < 5:
                patterns["short_form_content"] = 0.8
            
            if "tutorial" in context.get("title", "").lower():
                patterns["tutorial_format"] = 0.9
            
            if context.get("has_code_examples", False):
                patterns["code_examples"] = 0.9
        
        elif event.content_type == "github_repo":
            if context.get("stars", 0) > 10000:
                patterns["popular_projects"] = 0.8
            
            if context.get("recent_activity", False):
                patterns["active_projects"] = 0.9
        
        return patterns
    
    def _calculate_preference_adjustment(self, event: LearningEvent) -> float:
        """Calculate how much to adjust preferences based on event"""
        
        base_adjustments = {
            "like": 0.3,
            "dislike": -0.3,
            "save": 0.4,
            "share": 0.5,
            "source_promotion": 0.4,
            "source_demotion": -0.4,
            "time_spent": 0.0  # Will be calculated based on engagement_value
        }
        
        if event.event_type == "time_spent":
            # Convert engagement time to preference adjustment
            # engagement_value should be normalized (0-1) where 1 = very high engagement
            return (event.engagement_value - 0.5) * 0.4  # Range: -0.2 to +0.2
        
        return base_adjustments.get(event.event_type, 0.0) * event.engagement_value
    
    def _update_learning_metadata(self, event: LearningEvent) -> None:
        """Update learning metadata"""
        metadata = self.preferences.setdefault("learning_metadata", {})
        
        metadata["total_learning_events"] = metadata.get("total_learning_events", 0) + 1
        metadata["last_update"] = event.timestamp
        
        # Update confidence scores
        confidence_scores = metadata.setdefault("confidence_scores", {})
        
        for topic in event.topics:
            topic_events = len([e for e in self.learning_history if topic in e.topics])
            confidence_scores[topic] = min(1.0, topic_events / 10.0)
    
    def get_personalized_score_multiplier(self, content_type: str, source_name: str, 
                                        topics: List[str], context: Optional[Dict[str, Any]] = None) -> float:
        """Get personalized score multiplier for content"""
        
        multipliers = []
        
        # Source preference multiplier
        source_multiplier = self._get_source_multiplier(source_name)
        multipliers.append(source_multiplier)
        
        # Topic preference multiplier
        topic_multiplier = self._get_topic_multiplier(topics)
        multipliers.append(topic_multiplier)
        
        # Content pattern multiplier
        if context:
            pattern_multiplier = self._get_pattern_multiplier(content_type, context)
            multipliers.append(pattern_multiplier)
        
        # Combine multipliers (geometric mean to avoid extreme values)
        if multipliers:
            combined = math.pow(math.prod(multipliers), 1.0 / len(multipliers))
            return max(0.5, min(2.0, combined))  # Clamp to reasonable range
        
        return 1.0  # Default multiplier
    
    def _get_source_multiplier(self, source_name: str) -> float:
        """Get preference multiplier for source"""
        
        # Check stated preferences first
        stated_prefs = self.preferences.get("stated_preferences", {})
        source_key = f"{source_name.lower().replace(' ', '_')}_channel"
        
        if source_key in stated_prefs:
            score = stated_prefs[source_key].get("preference_score", 3.0)
            return score / 3.0  # Normalize around 1.0
        
        # Check learned preferences
        learned_patterns = self.preferences.get("learned_preferences", {}).get("source_patterns", {})
        source_pattern_key = f"{source_name.lower().replace(' ', '_')}_source"
        
        if source_pattern_key in learned_patterns:
            pattern = learned_patterns[source_pattern_key]
            if pattern.get("confidence", 0) > self.confidence_threshold:
                return pattern.get("preference_score", 0.6) * 1.5  # Boost confident learned preferences
        
        return 1.0  # Default neutral
    
    def _get_topic_multiplier(self, topics: List[str]) -> float:
        """Get preference multiplier for topics"""
        
        if not topics:
            return 1.0
        
        topic_prefs = self.preferences.get("topic_preferences", {})
        
        topic_scores = []
        for topic in topics:
            topic_key = topic.replace('-', '_')
            if topic_key in topic_prefs:
                score = topic_prefs[topic_key].get("interest_level", 0.6)
                topic_scores.append(score)
            else:
                topic_scores.append(0.6)  # Default interest
        
        # Average topic score
        avg_score = sum(topic_scores) / len(topic_scores)
        return avg_score * 1.3 + 0.35  # Scale to reasonable multiplier range
    
    def _get_pattern_multiplier(self, content_type: str, context: Dict[str, Any]) -> float:
        """Get preference multiplier for content patterns"""
        
        patterns = self._extract_content_patterns(
            LearningEvent("", "", "", content_type, "", [], 1.0, context)
        )
        
        content_patterns = self.preferences.get("learned_preferences", {}).get("content_patterns", {})
        
        pattern_scores = []
        for pattern, strength in patterns.items():
            if pattern in content_patterns:
                pattern_pref = content_patterns[pattern]
                if pattern_pref.get("confidence", 0) > self.confidence_threshold:
                    score = pattern_pref.get("preference_score", 0.6)
                    pattern_scores.append(score * strength)
        
        if pattern_scores:
            avg_score = sum(pattern_scores) / len(pattern_scores)
            return avg_score * 1.2 + 0.4  # Scale to multiplier range
        
        return 1.0  # Default if no patterns match
    
    def apply_preference_decay(self) -> None:
        """Apply weekly decay to learned preferences"""
        
        learned_prefs = self.preferences.get("learned_preferences", {})
        
        # Decay source patterns
        source_patterns = learned_prefs.get("source_patterns", {})
        for source_key, pattern in source_patterns.items():
            old_score = pattern["preference_score"]
            # Move toward neutral (0.6) by decay factor
            pattern["preference_score"] = old_score + (0.6 - old_score) * self.decay_factor
        
        # Decay content patterns
        content_patterns = learned_prefs.get("content_patterns", {})
        for pattern_key, pattern in content_patterns.items():
            old_score = pattern["preference_score"]
            pattern["preference_score"] = old_score + (0.6 - old_score) * self.decay_factor
            pattern["confidence"] = max(0.0, pattern["confidence"] - self.decay_factor)
        
        self._save_preferences()
        print("🔄 Applied preference decay")
    
    def _save_preferences(self) -> None:
        """Save updated preferences to file"""
        with open(self.preferences_file, 'w') as f:
            json.dump(self.preferences, f, indent=2)
    
    def _save_learning_history(self) -> None:
        """Save learning history to file"""
        self.learning_log_file.parent.mkdir(parents=True, exist_ok=True)
        
        events_data = [asdict(event) for event in self.learning_history]
        with open(self.learning_log_file, 'w') as f:
            json.dump(events_data, f, indent=2)
    
    def get_learning_summary(self) -> Dict[str, Any]:
        """Get summary of learning progress"""
        
        metadata = self.preferences.get("learning_metadata", {})
        learned_prefs = self.preferences.get("learned_preferences", {})
        
        return {
            "total_events": metadata.get("total_learning_events", 0),
            "last_update": metadata.get("last_update", "Never"),
            "learned_sources": len(learned_prefs.get("source_patterns", {})),
            "learned_patterns": len(learned_prefs.get("content_patterns", {})),
            "confidence_scores": metadata.get("confidence_scores", {}),
            "high_confidence_topics": [
                topic for topic, conf in metadata.get("confidence_scores", {}).items() 
                if conf > self.confidence_threshold
            ]
        }

def main():
    """Test the preference learning agent"""
    agent = PreferenceLearningAgent()
    
    print("🧠 AI Preference Learning Agent")
    print("=" * 40)
    
    # Show current learning summary
    summary = agent.get_learning_summary()
    print(f"📊 Learning Summary:")
    print(f"   Total events: {summary['total_events']}")
    print(f"   Learned sources: {summary['learned_sources']}")
    print(f"   Learned patterns: {summary['learned_patterns']}")
    print(f"   High confidence topics: {summary['high_confidence_topics']}")
    
    # Test preference calculation
    print(f"\n🧪 Testing preference calculations:")
    
    # Test ThePrimeagen video
    multiplier = agent.get_personalized_score_multiplier(
        "youtube_video", 
        "ThePrimeagen", 
        ["software-engineering", "vim"],
        {"title": "Advanced Vim Tutorial", "duration_minutes": 25, "has_code_examples": True}
    )
    print(f"   ThePrimeagen vim tutorial: {multiplier:.3f}x multiplier")
    
    # Test React GitHub repo
    multiplier = agent.get_personalized_score_multiplier(
        "github_repo",
        "facebook/react",
        ["react", "javascript"],
        {"stars": 225000, "recent_activity": True}
    )
    print(f"   React GitHub repo: {multiplier:.3f}x multiplier")
    
    print(f"\n✅ AI Learning Agent is operational!")

if __name__ == "__main__":
    main()