#!/usr/bin/env python3
"""
AI Summary Generation for Universal Topic Intelligence System
Generates concise summaries of collected content
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import logging
import re

logger = logging.getLogger(__name__)

class ContentSummarizer:
    """Generate AI-powered summaries of content"""
    
    def __init__(self, db_path: str = "topic_intelligence.db"):
        self.db_path = db_path
        self.logger = logging.getLogger("ContentSummarizer")
    
    def generate_summary(self, text: str, max_length: int = 150) -> str:
        """
        Generate a concise summary of text
        Uses extractive summarization (no LLM needed for basic version)
        
        Args:
            text: Text to summarize
            max_length: Maximum summary length in characters
            
        Returns:
            Summary string
        """
        if not text:
            return "No content available"
        
        # Clean the text
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Simple extractive summarization
        # Take first sentence or up to max_length characters
        sentences = text.split('. ')
        
        if sentences:
            summary = sentences[0]
            if len(summary) > max_length:
                summary = summary[:max_length-3] + "..."
            elif not summary.endswith('.'):
                summary += "."
            return summary
        
        return text[:max_length-3] + "..." if len(text) > max_length else text
    
    def extract_key_points(self, title: str, content: str) -> Dict[str, Any]:
        """
        Extract key points from content
        
        Args:
            title: Content title
            content: Content body
            
        Returns:
            Dictionary with key points
        """
        key_points = {
            "title": title,
            "summary": self.generate_summary(content),
            "keywords": [],
            "entities": [],
            "topics": []
        }
        
        # Extract keywords (simple version)
        text_lower = (title + " " + content).lower()
        
        # Claude-related keywords
        claude_keywords = ["claude", "anthropic", "opus", "sonnet", "haiku", "constitutional ai"]
        key_points["keywords"].extend([k for k in claude_keywords if k in text_lower])
        
        # Tech keywords
        tech_keywords = ["react", "typescript", "javascript", "api", "llm", "ai", "machine learning"]
        key_points["keywords"].extend([k for k in tech_keywords if k in text_lower])
        
        # Remove duplicates
        key_points["keywords"] = list(set(key_points["keywords"]))[:10]
        
        # Detect entities (simple pattern matching)
        entities = []
        
        # Company names
        if "anthropic" in text_lower:
            entities.append({"type": "company", "name": "Anthropic"})
        if "openai" in text_lower:
            entities.append({"type": "company", "name": "OpenAI"})
        if "google" in text_lower:
            entities.append({"type": "company", "name": "Google"})
        if "microsoft" in text_lower:
            entities.append({"type": "company", "name": "Microsoft"})
        
        # Product names
        if "claude" in text_lower:
            entities.append({"type": "product", "name": "Claude"})
        if "gpt" in text_lower:
            entities.append({"type": "product", "name": "GPT"})
        if "react" in text_lower:
            entities.append({"type": "framework", "name": "React"})
        
        key_points["entities"] = entities[:5]
        
        # Topic classification
        topics = []
        if any(k in text_lower for k in ["claude", "anthropic", "opus"]):
            topics.append("Claude AI")
        if any(k in text_lower for k in ["react", "component", "hooks"]):
            topics.append("React Development")
        if any(k in text_lower for k in ["typescript", "type", "interface"]):
            topics.append("TypeScript")
        if any(k in text_lower for k in ["llm", "language model", "prompting"]):
            topics.append("LLM Development")
        
        key_points["topics"] = topics[:3]
        
        return key_points
    
    def summarize_batch(self, items: List[Dict]) -> List[Dict]:
        """
        Generate summaries for a batch of items
        
        Args:
            items: List of content items
            
        Returns:
            List of items with summaries
        """
        summarized = []
        
        for item in items:
            title = item.get('title', '')
            content = item.get('content', '')
            
            # Generate summary
            summary = self.generate_summary(content or title)
            
            # Extract key points
            key_points = self.extract_key_points(title, content)
            
            # Add to item
            item['summary'] = summary
            item['key_points'] = key_points
            summarized.append(item)
        
        return summarized
    
    def generate_topic_summary(self, topic: str) -> Dict[str, Any]:
        """
        Generate a summary for a specific topic
        
        Args:
            topic: Topic to summarize (e.g., "claude", "react")
            
        Returns:
            Topic summary dictionary
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get recent items for topic
        query = """
            SELECT * FROM content_items
            WHERE LOWER(title) LIKE ? OR LOWER(content) LIKE ?
            ORDER BY priority_score DESC, published_date DESC
            LIMIT 20
        """
        
        topic_pattern = f"%{topic.lower()}%"
        cursor.execute(query, (topic_pattern, topic_pattern))
        items = [dict(row) for row in cursor.fetchall()]
        
        # Generate summaries
        summarized_items = self.summarize_batch(items)
        
        # Aggregate key points
        all_keywords = []
        all_entities = []
        all_topics = []
        
        for item in summarized_items:
            key_points = item.get('key_points', {})
            all_keywords.extend(key_points.get('keywords', []))
            all_entities.extend(key_points.get('entities', []))
            all_topics.extend(key_points.get('topics', []))
        
        # Count frequencies
        keyword_freq = {}
        for kw in all_keywords:
            keyword_freq[kw] = keyword_freq.get(kw, 0) + 1
        
        # Sort by frequency
        top_keywords = sorted(keyword_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Build topic summary
        topic_summary = {
            "topic": topic,
            "item_count": len(items),
            "top_keywords": [kw for kw, _ in top_keywords],
            "key_items": summarized_items[:5],
            "generated_at": datetime.now().isoformat()
        }
        
        conn.close()
        return topic_summary
    
    def generate_daily_briefing(self) -> str:
        """
        Generate a daily briefing with AI summaries
        
        Returns:
            Formatted briefing text
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get top Claude content
        cursor.execute("""
            SELECT * FROM content_items
            WHERE priority_level IN ('critical', 'high')
            AND (LOWER(title) LIKE '%claude%' OR LOWER(title) LIKE '%anthropic%')
            ORDER BY priority_score DESC
            LIMIT 5
        """)
        claude_items = [dict(row) for row in cursor.fetchall()]
        
        # Get top other content
        cursor.execute("""
            SELECT * FROM content_items
            WHERE priority_level IN ('critical', 'high')
            AND item_id NOT IN (
                SELECT item_id FROM content_items
                WHERE LOWER(title) LIKE '%claude%' OR LOWER(title) LIKE '%anthropic%'
            )
            ORDER BY priority_score DESC
            LIMIT 5
        """)
        other_items = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        # Generate summaries
        claude_summaries = self.summarize_batch(claude_items)
        other_summaries = self.summarize_batch(other_items)
        
        # Format briefing
        briefing = f"""
📰 DAILY AI INTELLIGENCE BRIEFING
{datetime.now().strftime('%B %d, %Y')}
{'=' * 50}

🤖 CLAUDE & ANTHROPIC UPDATES
{'=' * 50}
"""
        
        for i, item in enumerate(claude_summaries, 1):
            briefing += f"""
{i}. {item['title']}
   📝 {item['summary']}
   🏷️ Keywords: {', '.join(item['key_points']['keywords'][:3])}
   🔗 {item.get('url', 'No URL')}
"""
        
        briefing += f"""

📊 OTHER HIGH-PRIORITY CONTENT
{'=' * 50}
"""
        
        for i, item in enumerate(other_summaries, 1):
            briefing += f"""
{i}. {item['title']}
   📝 {item['summary']}
   🏷️ Keywords: {', '.join(item['key_points']['keywords'][:3])}
   🔗 {item.get('url', 'No URL')}
"""
        
        # Add trending topics
        claude_summary = self.generate_topic_summary("claude")
        
        briefing += f"""

🔥 TRENDING TOPICS
{'=' * 50}
Top Keywords: {', '.join(claude_summary['top_keywords'][:5])}

{'=' * 50}
Generated by Universal Topic Intelligence System
View full dashboard at: http://localhost:5001
"""
        
        return briefing


def test_summarizer():
    """Test the content summarizer"""
    summarizer = ContentSummarizer()
    
    # Test single summary
    test_text = """
    Anthropic has released Claude Opus 4.1, a major update to their flagship AI model.
    The new version includes improved reasoning capabilities, better code generation,
    and enhanced safety features through constitutional AI. Early benchmarks show
    significant improvements in complex reasoning tasks and creative writing.
    """
    
    summary = summarizer.generate_summary(test_text)
    print("📝 Test Summary:")
    print(summary)
    print()
    
    # Test key points extraction
    key_points = summarizer.extract_key_points(
        "Claude Opus 4.1 Released with Major Improvements",
        test_text
    )
    print("🔑 Key Points:")
    print(json.dumps(key_points, indent=2))
    print()
    
    # Generate daily briefing
    print("Generating Daily Briefing...")
    print("=" * 50)
    briefing = summarizer.generate_daily_briefing()
    print(briefing)
    
    # Save briefing to file
    with open("digests/daily_briefing.txt", "w") as f:
        f.write(briefing)
    print("\n✅ Briefing saved to digests/daily_briefing.txt")


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Run tests
    test_summarizer()