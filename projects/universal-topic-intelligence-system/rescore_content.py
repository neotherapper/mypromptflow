#!/usr/bin/env python3
"""
Re-score all content using the proper prioritization system
This applies the existing ContentPrioritizer with topic-specific rules
"""

import sqlite3
import json
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

# Import our existing systems
from core import (
    ContentItem,
    UniversalContentPrioritizer,
    ContentPriority,
    SourceMetadata,
    SourceType
)
from core.quality_scorer import TopicQualityScorer

def load_topic_configuration() -> Dict[str, Any]:
    """Load the AI/ML topic configuration with Claude rules"""
    config_path = Path("universal-topic-system/examples/ai-ml-topic-configuration.yaml")
    
    # Fallback configuration if file doesn't exist
    default_config = {
        "topic_metadata": {
            "name": "AI and Machine Learning",
            "priority_keywords": ["claude", "anthropic", "opus", "sonnet", "gpt", "openai", "gemini", "ai", "llm"]
        },
        "content_analysis": {
            "significance_indicators": {
                "high_significance": [
                    "New model releases (GPT, Claude, Gemini updates)",
                    "Claude Opus", "Claude Sonnet", "Claude Haiku",
                    "Anthropic announcements",
                    "Major AI breakthroughs"
                ]
            },
            "quality_thresholds": {
                "minimum_relevance_score": 0.7,
                "minimum_authority_score": 0.6,
                "minimum_significance_score": 0.5
            }
        },
        "quality_assessment": {
            "thresholds": {
                "critical": 0.85,
                "high": 0.70,
                "medium": 0.50,
                "low": 0.30
            },
            "weights": {
                "source_authority": 0.25,
                "content_accuracy": 0.20,
                "relevance_alignment": 0.25,
                "completeness_depth": 0.15,
                "constitutional_compliance": 0.15
            },
            "topic_specific_rules": [
                {
                    "rule": "boost_claude_opus",
                    "condition": "title contains 'Claude Opus' or title contains 'Opus 4'",
                    "action": "multiply_score by 2.0"
                },
                {
                    "rule": "boost_claude_releases",
                    "condition": "title contains 'Claude' and (title contains 'release' or title contains 'launch' or title contains 'available' or title contains 'here')",
                    "action": "multiply_score by 1.8"
                },
                {
                    "rule": "boost_anthropic",
                    "condition": "title contains 'Anthropic' or content contains 'Anthropic'",
                    "action": "multiply_score by 1.5"
                },
                {
                    "rule": "boost_ai_breakthroughs",
                    "condition": "title contains 'breakthrough' or title contains 'revolution' or title contains 'major'",
                    "action": "multiply_score by 1.3"
                }
            ]
        }
    }
    
    if config_path.exists():
        try:
            with open(config_path, 'r') as f:
                loaded_config = yaml.safe_load(f)
                # Merge with defaults
                for key in default_config:
                    if key not in loaded_config:
                        loaded_config[key] = default_config[key]
                return loaded_config
        except Exception as e:
            print(f"Warning: Could not load config file: {e}")
    
    return default_config

def create_prioritizer_with_claude_rules() -> UniversalContentPrioritizer:
    """Create a prioritizer configured for Claude/AI content"""
    
    config = load_topic_configuration()
    
    # Create prioritizer with custom configuration
    # Use ContentPrioritizer's weight structure, not quality scorer's
    prioritizer_config = {
        "weights": {
            "source_authority": 0.25,      # Boost source authority for Claude
            "content_recency": 0.20,       # Recent content is important
            "topic_relevance": 0.25,       # High relevance weight for Claude topics
            "engagement_signals": 0.10,
            "uniqueness_score": 0.10,
            "completeness": 0.05,
            "actionability": 0.05,
            "cross_topic_value": 0.00      # Focus on Claude, not cross-topic
        },
        "thresholds": config["quality_assessment"]["thresholds"],
        "recency_decay": {
            "half_life_hours": 48,
            "max_age_days": 30
        }
    }
    
    prioritizer = UniversalContentPrioritizer(prioritizer_config)
    
    # Set topic preferences for Claude-related content
    topic_preferences = {
        "claude": 1.0,
        "claude-ai": 1.0,
        "anthropic": 0.95,
        "opus": 0.95,
        "sonnet": 0.9,
        "haiku": 0.9,
        "ai": 0.8,
        "llm": 0.8,
        "react": 0.7,
        "typescript": 0.7,
        "mcp": 0.7
    }
    prioritizer.set_topic_preferences(topic_preferences)
    
    # Set source authority scores
    source_scores = {
        "anthropic_blog": 1.0,
        "openai_blog": 0.95,
        "react_blog": 0.95,
        "vercel_blog": 0.9,
        "simon_willison": 0.85,
        "hackernews_ai": 0.8,
        "dev_to_claude": 0.75,
        "dev_to_react": 0.75,
        "dev_to_typescript": 0.75,
        "dev_to_ai": 0.7
    }
    prioritizer.set_source_authorities(source_scores)
    
    return prioritizer

def create_quality_scorer_with_rules() -> TopicQualityScorer:
    """Create quality scorer with Claude-specific rules"""
    config = load_topic_configuration()
    
    quality_config = config.get("quality_assessment", {})
    
    # Add Claude-specific rules if not present
    if "topic_specific_rules" not in quality_config:
        quality_config["topic_specific_rules"] = []
    
    # Ensure Claude rules are present
    claude_rules = [
        {
            "rule": "claude_opus_critical",
            "condition": "title contains 'Claude Opus' or title contains 'Opus 4'",
            "action": "multiply_score by 2.2"
        },
        {
            "rule": "claude_major_release",
            "condition": "(title contains 'Claude' or title contains 'Anthropic') and (title contains 'release' or title contains 'launch' or title contains 'announces' or title contains 'here')",
            "action": "multiply_score by 2.0"
        },
        {
            "rule": "claude_general_boost",
            "condition": "title contains 'Claude' or content contains 'Claude Code'",
            "action": "multiply_score by 1.5"
        }
    ]
    
    # Add rules if not already present
    existing_rules = {r.get("rule") for r in quality_config["topic_specific_rules"]}
    for rule in claude_rules:
        if rule["rule"] not in existing_rules:
            quality_config["topic_specific_rules"].append(rule)
    
    return TopicQualityScorer(quality_config)

def rescore_all_content():
    """Re-score all content in the database using proper prioritization"""
    
    print("🚀 Starting content re-scoring with proper prioritization...")
    
    # Initialize systems
    prioritizer = create_prioritizer_with_claude_rules()
    quality_scorer = create_quality_scorer_with_rules()
    
    # Connect to database
    conn = sqlite3.connect("topic_intelligence.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get all content items
    cursor.execute("""
        SELECT * FROM content_items 
        WHERE is_english = 1
        ORDER BY collected_date DESC
    """)
    
    items = cursor.fetchall()
    print(f"📊 Found {len(items)} items to re-score")
    
    # Track scoring results
    priority_counts = {
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0,
        "archive": 0
    }
    
    claude_items = []
    
    for row in items:
        item_dict = dict(row)
        
        # Parse JSON fields
        if item_dict.get('topics'):
            try:
                topics = json.loads(item_dict['topics']) if isinstance(item_dict['topics'], str) else item_dict['topics']
            except:
                topics = []
        else:
            topics = []
        
        if item_dict.get('metadata'):
            try:
                metadata = json.loads(item_dict['metadata']) if isinstance(item_dict['metadata'], str) else item_dict['metadata']
            except:
                metadata = {}
        else:
            metadata = {}
        
        # Add source authority to metadata if we know it
        source_scores = prioritizer.source_scores
        if item_dict['source_id'] in source_scores:
            metadata['source_authority'] = source_scores[item_dict['source_id']]
        
        # Create ContentItem
        content_item = ContentItem(
            item_id=item_dict['item_id'],
            source_id=item_dict['source_id'],
            title=item_dict['title'],
            content=item_dict.get('content'),
            url=item_dict.get('url'),
            published_date=datetime.fromisoformat(item_dict['published_date']) if item_dict.get('published_date') else datetime.now(),
            author=item_dict.get('author'),
            topics=topics,
            metadata=metadata
        )
        
        # First apply quality scorer with topic rules
        quality_score = quality_scorer.score_content(content_item)
        
        # Then use prioritizer for final scoring
        priority_result = prioritizer.prioritize(content_item, strategy="technical")
        
        # Determine final priority (use higher of the two systems)
        final_score = max(quality_score.total_score, priority_result.total_score)
        
        # Special boost for Claude content that might have been missed
        title_lower = item_dict['title'].lower()
        if any(keyword in title_lower for keyword in ['claude', 'opus', 'anthropic', 'sonnet']):
            # Ensure Claude content is never below HIGH priority
            final_score = max(final_score, 0.75)
            
            # Claude Opus should always be CRITICAL
            if 'opus' in title_lower or '4.1' in title_lower or '4.0' in title_lower:
                final_score = max(final_score, 0.90)
        
        # Determine priority level
        if final_score >= 0.85:
            priority = "critical"
        elif final_score >= 0.70:
            priority = "high"
        elif final_score >= 0.50:
            priority = "medium"
        elif final_score >= 0.30:
            priority = "low"
        else:
            priority = "archive"
        
        priority_counts[priority] += 1
        
        # Track Claude items
        if 'claude' in title_lower:
            claude_items.append({
                "title": item_dict['title'],
                "old_score": item_dict.get('priority_score', 0),
                "new_score": final_score,
                "old_priority": item_dict.get('priority_level', 'unknown'),
                "new_priority": priority
            })
        
        # Update database
        cursor.execute("""
            UPDATE content_items 
            SET priority_score = ?, priority_level = ?
            WHERE item_id = ?
        """, (final_score, priority, item_dict['item_id']))
    
    # Commit changes
    conn.commit()
    conn.close()
    
    # Report results
    print("\n✅ Re-scoring complete!")
    print("\n📊 Priority Distribution:")
    for level, count in priority_counts.items():
        print(f"  {level.upper()}: {count} items")
    
    if claude_items:
        print(f"\n🤖 Claude Content Re-scored ({len(claude_items)} items):")
        for item in claude_items[:5]:  # Show first 5
            print(f"\n  📄 {item['title'][:60]}...")
            print(f"     Old: {item['old_priority']} ({item['old_score']:.2f})")
            print(f"     New: {item['new_priority']} ({item['new_score']:.2f})")
            if item['new_score'] > item['old_score']:
                print(f"     ⬆️ Boosted by {(item['new_score'] - item['old_score']):.2f}")
    
    print("\n🎯 Claude content now properly prioritized!")
    print("📍 Refresh the dashboard to see the updated priorities")

if __name__ == "__main__":
    rescore_all_content()