#!/usr/bin/env python3
"""
Topic-Weighted Content Scoring Engine
Universal Topic Intelligence System - Priority Topic Scoring
Enhanced with Claude Intelligence Patterns
"""

import json
import re
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

# Import Claude Intelligence Scorer if available
try:
    from quality_engine.claude_intelligence_implementation import ClaudeIntelligenceScorer, TopicCategory, ContentItem
    CLAUDE_INTELLIGENCE_AVAILABLE = True
    print("✅ Claude Intelligence integration available")
except ImportError:
    CLAUDE_INTELLIGENCE_AVAILABLE = False
    print("⚠️  Claude Intelligence not available - using standard scoring")

@dataclass
class ScoredContent:
    """Content item with priority topic scoring"""
    title: str
    content: str
    source: str
    platform: str
    url: str
    published_date: str
    topics: List[str]
    base_score: float
    priority_score: float
    final_score: float
    detected_priority_topics: List[str]
    score_breakdown: Dict[str, float]

class TopicScoringEngine:
    """Priority topic-aware content scoring engine with Claude intelligence"""
    
    def __init__(self, priority_topics_config_path: Optional[str] = None):
        self.config_path = priority_topics_config_path or "priority-topics.json"
        self.priority_config = self._load_priority_config()
        
        # Initialize Claude Intelligence Scorer if available
        if CLAUDE_INTELLIGENCE_AVAILABLE:
            self.claude_scorer = ClaudeIntelligenceScorer()
            print("✅ Claude Intelligence Scorer initialized")
        else:
            self.claude_scorer = None
        
    def _load_priority_config(self) -> Dict[str, Any]:
        """Load priority topics configuration"""
        config_file = Path(self.config_path)
        if config_file.exists():
            with open(config_file, 'r') as f:
                return json.load(f)
        return {}
    
    def detect_priority_topics(self, content_item: Dict[str, Any]) -> List[str]:
        """Detect priority topics in content using keywords and aliases"""
        detected_topics = []
        
        # Combine title and content for analysis
        text_content = f"{content_item.get('title', '')} {content_item.get('description', '')} {content_item.get('content', '')}".lower()
        
        # Check priority topics
        for topic_name, topic_config in self.priority_config.get('priority_topics', {}).items():
            # Check primary topic name
            if topic_name.lower().replace('-', ' ') in text_content:
                detected_topics.append(topic_name)
                continue
                
            # Check aliases
            for alias in topic_config.get('aliases', []):
                if alias.lower() in text_content:
                    detected_topics.append(topic_name)
                    break
                    
            # Check keywords
            for keyword in topic_config.get('keywords', []):
                if keyword.lower() in text_content:
                    detected_topics.append(topic_name)
                    break
        
        # Remove duplicates while preserving order
        return list(dict.fromkeys(detected_topics))
    
    def _convert_to_claude_content_item(self, content_item: Dict[str, Any]) -> 'ContentItem':
        """Convert content item to Claude Intelligence format"""
        if not CLAUDE_INTELLIGENCE_AVAILABLE:
            return None
            
        return ContentItem(
            title=content_item.get('title', ''),
            description=content_item.get('description', ''),
            content=content_item.get('content', ''),
            source=content_item.get('source', ''),
            url=content_item.get('url', ''),
            author=content_item.get('author', ''),
            platform=content_item.get('platform', ''),
            engagement_metrics={
                'score': content_item.get('score', 0),
                'comments': content_item.get('comments', 0),
                'views': content_item.get('views', 0),
                'upvotes': content_item.get('upvotes', 0),
                'subscribers': content_item.get('subscribers', 0),
                'stars': content_item.get('stars', 0)
            },
            metadata=content_item.get('metadata', {})
        )
    
    def calculate_base_score(self, content_item: Dict[str, Any]) -> float:
        """Calculate base content score from engagement metrics"""
        # Extract engagement metrics
        score = content_item.get('score', 0) or 0
        comments = content_item.get('comments', 0) or content_item.get('num_comments', 0) or 0
        views = content_item.get('views', 0) or 0
        upvotes = content_item.get('upvotes', 0) or 0
        
        # Calculate engagement score
        engagement_score = 0.0
        
        # Score contribution (40% weight)
        if score > 0:
            engagement_score += min(score / 100.0, 1.0) * 0.4
            
        # Comments contribution (30% weight)  
        if comments > 0:
            engagement_score += min(comments / 50.0, 1.0) * 0.3
            
        # Views contribution (20% weight)
        if views > 0:
            engagement_score += min(views / 10000.0, 1.0) * 0.2
            
        # Upvotes contribution (10% weight)
        if upvotes > 0:
            engagement_score += min(upvotes / 100.0, 1.0) * 0.1
        
        # Minimum base score for content without metrics
        return max(engagement_score, 0.1)
    
    def calculate_freshness_score(self, content_item: Dict[str, Any]) -> float:
        """Calculate freshness score based on publication date"""
        published_date_str = content_item.get('published_date') or content_item.get('published')
        if not published_date_str:
            return 0.5  # Default for content without date
            
        try:
            # Parse different date formats
            if 'T' in published_date_str:
                published_date = datetime.fromisoformat(published_date_str.replace('Z', '+00:00'))
            else:
                published_date = datetime.strptime(published_date_str, '%Y-%m-%d')
                published_date = published_date.replace(tzinfo=timezone.utc)
                
            now = datetime.now(timezone.utc)
            age_hours = (now - published_date).total_seconds() / 3600
            
            # Apply freshness decay from config
            freshness_config = self.priority_config.get('content_scoring', {}).get('freshness_decay', {})
            
            if age_hours <= 24:
                return freshness_config.get('0-24_hours', 1.0)
            elif age_hours <= 72:
                return freshness_config.get('1-3_days', 0.8)
            elif age_hours <= 168:  # 7 days
                return freshness_config.get('3-7_days', 0.6)
            elif age_hours <= 720:  # 30 days
                return freshness_config.get('7-30_days', 0.4)
            else:
                return freshness_config.get('30+_days', 0.2)
                
        except (ValueError, TypeError):
            return 0.5  # Default for unparseable dates
    
    def calculate_priority_boost(self, detected_topics: List[str]) -> Tuple[float, Dict[str, float]]:
        """Calculate priority topic boost multiplier"""
        if not detected_topics:
            return 1.0, {}
            
        boost_breakdown = {}
        max_boost = 1.0
        
        # Apply individual topic boosts
        for topic in detected_topics:
            topic_config = self.priority_config.get('priority_topics', {}).get(topic, {})
            topic_weight = topic_config.get('weight', 1.0)
            boost_breakdown[topic] = topic_weight
            max_boost = max(max_boost, topic_weight)
        
        # Check for topic combinations
        combination_config = self.priority_config.get('topic_combinations', {})
        for combo_name, combo_config in combination_config.items():
            required_topics = combo_config.get('required_topics', [])
            if all(topic in detected_topics for topic in required_topics):
                combo_weight = combo_config.get('weight', 1.0)
                combo_bonus = combo_config.get('bonus_multiplier', 0.0)
                total_combo_boost = combo_weight + combo_bonus
                boost_breakdown[f"combo_{combo_name}"] = total_combo_boost
                max_boost = max(max_boost, total_combo_boost)
        
        return max_boost, boost_breakdown
    
    def calculate_relevance_score(self, content_item: Dict[str, Any], detected_topics: List[str]) -> float:
        """Calculate content relevance score"""
        # Base relevance from detected priority topics
        if detected_topics:
            priority_relevance = len(detected_topics) / len(self.priority_config.get('priority_topics', {}))
            return min(priority_relevance, 1.0)
        
        # Secondary relevance from secondary topics
        text_content = f"{content_item.get('title', '')} {content_item.get('description', '')}".lower()
        secondary_matches = 0
        
        for topic_name, topic_config in self.priority_config.get('secondary_topics', {}).items():
            keywords = topic_config.get('keywords', [topic_name])
            if any(keyword.lower() in text_content for keyword in keywords):
                secondary_matches += 1
        
        secondary_relevance = secondary_matches / max(len(self.priority_config.get('secondary_topics', {})), 1)
        return min(secondary_relevance * 0.5, 0.5)  # Max 0.5 for secondary topics
    
    def _apply_claude_intelligence(self, content_item: Dict[str, Any], detected_topics: List[str]) -> Optional[Dict[str, Any]]:
        """Apply Claude Intelligence enhancement if available and applicable"""
        if not self.claude_scorer or not CLAUDE_INTELLIGENCE_AVAILABLE:
            return None
        
        # Check if content is Claude-related
        text_content = f"{content_item.get('title', '')} {content_item.get('description', '')} {content_item.get('content', '')}".lower()
        claude_indicators = ['claude', 'anthropic', 'constitutional ai', 'meta-prompting', 'ai coding', 'ai assistant']
        
        if not any(indicator in text_content for indicator in claude_indicators):
            return None  # Not Claude-related content
        
        try:
            # Convert to Claude content format
            claude_content_item = self._convert_to_claude_content_item(content_item)
            if not claude_content_item:
                return None
            
            # Get Claude intelligence scoring
            claude_result = self.claude_scorer.calculate_enhanced_quality_score(claude_content_item)
            
            # Extract relevant enhancements
            topic_category = claude_result.get('topic_category', 'general_content')
            
            # Map topic categories to multipliers
            topic_multipliers = {
                'claude_code_development': 1.4,
                'claude_ai_content': 1.3,
                'meta_prompting_techniques': 1.25,
                'ai_development_workflows': 1.2,
                'general_content': 1.0
            }
            
            return {
                'topic_category': topic_category,
                'topic_multiplier': topic_multipliers.get(topic_category, 1.0),
                'total_bonus': claude_result.get('bonuses', {}).get('total_bonus', 0.0),
                'bonuses': {
                    'claude_authority': claude_result.get('bonuses', {}).get('authority', 0.0),
                    'claude_accuracy': claude_result.get('bonuses', {}).get('accuracy', 0.0),
                    'claude_completeness': claude_result.get('bonuses', {}).get('completeness', 0.0)
                },
                'quality_tier': claude_result.get('quality_tier', 'medium_quality'),
                'claude_confidence': claude_result.get('topic_confidence', 0.0)
            }
            
        except Exception as e:
            print(f"⚠️  Claude intelligence enhancement failed: {e}")
            return None
    
    def score_content_item(self, content_item: Dict[str, Any]) -> ScoredContent:
        """Score a single content item with priority topic weighting and Claude intelligence"""
        
        # Step 1: Detect priority topics
        detected_topics = self.detect_priority_topics(content_item)
        
        # Step 2: Apply Claude Intelligence Enhancement (if available)
        claude_enhancement = self._apply_claude_intelligence(content_item, detected_topics)
        
        # Step 3: Calculate component scores
        base_score = self.calculate_base_score(content_item)
        freshness_score = self.calculate_freshness_score(content_item)
        relevance_score = self.calculate_relevance_score(content_item, detected_topics)
        priority_boost, boost_breakdown = self.calculate_priority_boost(detected_topics)
        
        # Step 4: Apply Claude intelligence boost
        if claude_enhancement:
            claude_boost = claude_enhancement.get('total_bonus', 0.0)
            claude_multiplier = claude_enhancement.get('topic_multiplier', 1.0)
            priority_boost = max(priority_boost, claude_multiplier)
            boost_breakdown.update(claude_enhancement.get('bonuses', {}))
        else:
            claude_boost = 0.0
            claude_multiplier = 1.0
        
        # Step 5: Calculate priority score with Claude enhancement
        priority_score = base_score * freshness_score * relevance_score * priority_boost + claude_boost
        
        # Step 6: Calculate final score
        final_score = min(priority_score, 1.0)  # Cap at 1.0
        
        # Create enhanced score breakdown
        score_breakdown = {
            'base_score': base_score,
            'freshness_score': freshness_score,
            'relevance_score': relevance_score,
            'priority_boost': priority_boost,
            'priority_boosts': boost_breakdown,
            'claude_boost': claude_boost,
            'claude_multiplier': claude_multiplier,
            'claude_enhancement': claude_enhancement,
            'calculation': f"{base_score:.3f} × {freshness_score:.3f} × {relevance_score:.3f} × {priority_boost:.3f} + {claude_boost:.3f} = {final_score:.3f}"
        }
        
        return ScoredContent(
            title=content_item.get('title', ''),
            content=content_item.get('description', ''),
            source=content_item.get('source', content_item.get('channel', content_item.get('subreddit', 'unknown'))),
            platform=content_item.get('platform', 'unknown'),
            url=content_item.get('url', content_item.get('post_url', content_item.get('story_url', ''))),
            published_date=content_item.get('published_date', content_item.get('published', '')),
            topics=content_item.get('topics', []),
            base_score=base_score,
            priority_score=priority_score,
            final_score=final_score,
            detected_priority_topics=detected_topics,
            score_breakdown=score_breakdown
        )
    
    def score_content_batch(self, content_items: List[Dict[str, Any]]) -> List[ScoredContent]:
        """Score a batch of content items"""
        scored_items = []
        
        for item in content_items:
            try:
                scored_item = self.score_content_item(item)
                scored_items.append(scored_item)
            except Exception as e:
                print(f"Error scoring content item: {e}")
                continue
        
        # Sort by final score (highest first)
        scored_items.sort(key=lambda x: x.final_score, reverse=True)
        
        return scored_items
    
    def generate_scoring_report(self, scored_items: List[ScoredContent], top_n: int = 20) -> Dict[str, Any]:
        """Generate detailed scoring report"""
        
        # Priority topic distribution
        topic_distribution = {}
        for item in scored_items:
            for topic in item.detected_priority_topics:
                topic_distribution[topic] = topic_distribution.get(topic, 0) + 1
        
        # Score statistics
        scores = [item.final_score for item in scored_items]
        
        # Top items by priority topics
        priority_sections = {}
        for topic in self.priority_config.get('priority_topics', {}).keys():
            topic_items = [item for item in scored_items if topic in item.detected_priority_topics]
            if topic_items:
                priority_sections[topic] = topic_items[:5]  # Top 5 per topic
        
        return {
            'metadata': {
                'total_items': len(scored_items),
                'items_with_priority_topics': len([item for item in scored_items if item.detected_priority_topics]),
                'priority_topic_coverage': len(topic_distribution.keys()),
                'generated_at': datetime.now(timezone.utc).isoformat()
            },
            'score_statistics': {
                'max_score': max(scores) if scores else 0,
                'min_score': min(scores) if scores else 0,
                'avg_score': sum(scores) / len(scores) if scores else 0,
                'median_score': sorted(scores)[len(scores) // 2] if scores else 0
            },
            'topic_distribution': topic_distribution,
            'top_items_overall': scored_items[:top_n],
            'top_items_by_priority_topic': priority_sections
        }

def main():
    """Test the topic scoring engine"""
    # Example content items for testing
    test_items = [
        {
            'title': 'New Claude Code Features Released by Anthropic',
            'description': 'Anthropic releases new Claude Code IDE features for better AI-assisted programming',
            'source': 'Anthropic Blog',
            'platform': 'web',
            'url': 'https://example.com/claude-code-features',
            'published_date': '2025-07-31T10:00:00Z',
            'score': 150,
            'comments': 45
        },
        {
            'title': 'React TypeScript Best Practices 2025',
            'description': 'Complete guide to React with TypeScript for modern web development',
            'source': 'React Blog',
            'platform': 'web', 
            'url': 'https://example.com/react-typescript',
            'published_date': '2025-07-31T08:00:00Z',
            'score': 200,
            'comments': 35
        },
        {
            'title': 'Advanced Meta-Prompting Techniques for Claude',
            'description': 'Learn advanced prompt engineering techniques for better Claude interactions',
            'source': 'AI Research',
            'platform': 'web',
            'url': 'https://example.com/meta-prompting',
            'published_date': '2025-07-30T15:00:00Z',
            'score': 75,
            'comments': 20
        },
        {
            'title': 'Generic JavaScript Tutorial',
            'description': 'Basic JavaScript concepts for beginners',
            'source': 'Dev Blog',
            'platform': 'web',
            'url': 'https://example.com/js-tutorial', 
            'published_date': '2025-07-25T12:00:00Z',
            'score': 50,
            'comments': 10
        }
    ]
    
    # Initialize scoring engine
    engine = TopicScoringEngine()
    
    print("🎯 Priority Topic Scoring Engine Test")
    print("=" * 50)
    
    # Score content items
    scored_items = engine.score_content_batch(test_items)
    
    # Display results
    for i, item in enumerate(scored_items, 1):
        print(f"\n{i}. {item.title}")
        print(f"   Source: {item.source} | Platform: {item.platform}")
        print(f"   Priority Topics: {item.detected_priority_topics}")
        print(f"   Score: {item.final_score:.3f} (Base: {item.base_score:.3f})")
        print(f"   Calculation: {item.score_breakdown['calculation']}")
    
    # Generate report
    report = engine.generate_scoring_report(scored_items)
    print(f"\n📊 Scoring Report")
    print(f"   Total Items: {report['metadata']['total_items']}")
    print(f"   Items with Priority Topics: {report['metadata']['items_with_priority_topics']}")
    print(f"   Topic Distribution: {report['topic_distribution']}")
    print(f"   Score Range: {report['score_statistics']['min_score']:.3f} - {report['score_statistics']['max_score']:.3f}")

if __name__ == "__main__":
    main()