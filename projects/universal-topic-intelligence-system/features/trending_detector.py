#!/usr/bin/env python3
"""
Trending Topic Detection for Universal Topic Intelligence System
Identifies emerging topics and trends in collected content
"""

import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
from collections import Counter, defaultdict
import re
import logging

logger = logging.getLogger(__name__)

class TrendingTopicDetector:
    """Detect trending topics in collected content"""
    
    def __init__(self, db_path: str = "topic_intelligence.db"):
        self.db_path = db_path
        self.logger = logging.getLogger("TrendingDetector")
    
    def extract_ngrams(self, text: str, n: int = 2) -> List[str]:
        """
        Extract n-grams from text
        
        Args:
            text: Input text
            n: Size of n-grams (default: 2 for bigrams)
            
        Returns:
            List of n-grams
        """
        # Clean and tokenize
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        words = text.split()
        
        # Filter out stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
                     'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
                     'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
                     'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that'}
        
        words = [w for w in words if w not in stop_words and len(w) > 2]
        
        # Generate n-grams
        ngrams = []
        for i in range(len(words) - n + 1):
            ngram = ' '.join(words[i:i+n])
            ngrams.append(ngram)
        
        return ngrams
    
    def calculate_trend_score(self, 
                            current_count: int, 
                            previous_count: int,
                            total_current: int,
                            total_previous: int) -> float:
        """
        Calculate trend score for a topic
        
        Args:
            current_count: Count in current period
            previous_count: Count in previous period
            total_current: Total items in current period
            total_previous: Total items in previous period
            
        Returns:
            Trend score (higher = more trending)
        """
        # Normalize by total counts
        current_freq = current_count / max(total_current, 1)
        previous_freq = previous_count / max(total_previous, 1)
        
        # Calculate growth rate
        if previous_freq == 0:
            growth_rate = current_freq * 100  # New topic
        else:
            growth_rate = (current_freq - previous_freq) / previous_freq
        
        # Combine frequency and growth
        trend_score = current_freq * (1 + growth_rate)
        
        return trend_score
    
    def detect_trending_topics(self, 
                              period_hours: int = 24,
                              min_mentions: int = 3) -> List[Dict[str, Any]]:
        """
        Detect trending topics over a time period
        
        Args:
            period_hours: Time period to analyze (default: 24 hours)
            min_mentions: Minimum mentions to be considered trending
            
        Returns:
            List of trending topics with scores
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Define time periods
        now = datetime.now()
        current_start = now - timedelta(hours=period_hours)
        previous_start = now - timedelta(hours=period_hours * 2)
        
        # Get current period items
        cursor.execute("""
            SELECT title, content FROM content_items
            WHERE collected_date >= ?
        """, (current_start.isoformat(),))
        
        current_items = cursor.fetchall()
        
        # Get previous period items
        cursor.execute("""
            SELECT title, content FROM content_items
            WHERE collected_date >= ? AND collected_date < ?
        """, (previous_start.isoformat(), current_start.isoformat()))
        
        previous_items = cursor.fetchall()
        
        conn.close()
        
        # Extract topics from current period
        current_topics = Counter()
        for item in current_items:
            text = f"{item['title']} {item['content'] or ''}"
            
            # Extract unigrams and bigrams
            unigrams = self.extract_ngrams(text, 1)
            bigrams = self.extract_ngrams(text, 2)
            
            # Count occurrences
            for term in unigrams + bigrams:
                if len(term) > 3:  # Filter very short terms
                    current_topics[term] += 1
        
        # Extract topics from previous period
        previous_topics = Counter()
        for item in previous_items:
            text = f"{item['title']} {item['content'] or ''}"
            
            unigrams = self.extract_ngrams(text, 1)
            bigrams = self.extract_ngrams(text, 2)
            
            for term in unigrams + bigrams:
                if len(term) > 3:
                    previous_topics[term] += 1
        
        # Calculate trend scores
        trending = []
        total_current = len(current_items)
        total_previous = len(previous_items)
        
        for topic, current_count in current_topics.items():
            if current_count >= min_mentions:
                previous_count = previous_topics.get(topic, 0)
                
                trend_score = self.calculate_trend_score(
                    current_count, previous_count,
                    total_current, total_previous
                )
                
                trending.append({
                    'topic': topic,
                    'current_mentions': current_count,
                    'previous_mentions': previous_count,
                    'trend_score': trend_score,
                    'is_new': previous_count == 0,
                    'growth_rate': ((current_count - previous_count) / max(previous_count, 1)) * 100
                })
        
        # Sort by trend score
        trending.sort(key=lambda x: x['trend_score'], reverse=True)
        
        return trending[:20]  # Top 20 trending topics
    
    def detect_claude_trends(self) -> Dict[str, Any]:
        """
        Detect Claude-specific trending topics
        
        Returns:
            Dictionary with Claude trends
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get Claude-related items from last 7 days
        week_ago = (datetime.now() - timedelta(days=7)).isoformat()
        
        cursor.execute("""
            SELECT title, content, collected_date
            FROM content_items
            WHERE (LOWER(title) LIKE '%claude%' 
                   OR LOWER(title) LIKE '%anthropic%'
                   OR LOWER(title) LIKE '%opus%')
            AND collected_date >= ?
            ORDER BY collected_date DESC
        """, (week_ago,))
        
        items = cursor.fetchall()
        conn.close()
        
        # Track Claude-specific terms
        claude_terms = Counter()
        daily_counts = defaultdict(int)
        
        for item in items:
            text = f"{item['title']} {item['content'] or ''}".lower()
            date = item['collected_date'][:10]  # YYYY-MM-DD
            daily_counts[date] += 1
            
            # Track specific Claude features/versions
            if 'opus 4.1' in text or 'claude 4.1' in text:
                claude_terms['Opus 4.1'] += 1
            if 'claude code' in text:
                claude_terms['Claude Code'] += 1
            if 'constitutional ai' in text:
                claude_terms['Constitutional AI'] += 1
            if 'claude desktop' in text:
                claude_terms['Claude Desktop'] += 1
            if 'sonnet' in text:
                claude_terms['Sonnet'] += 1
            if 'haiku' in text:
                claude_terms['Haiku'] += 1
            if 'claude api' in text:
                claude_terms['Claude API'] += 1
            if 'mcp' in text or 'model context protocol' in text:
                claude_terms['MCP Integration'] += 1
        
        # Calculate trend
        dates = sorted(daily_counts.keys())
        if len(dates) >= 2:
            recent_avg = sum(daily_counts[d] for d in dates[-3:]) / min(3, len(dates))
            older_avg = sum(daily_counts[d] for d in dates[:-3]) / max(len(dates) - 3, 1)
            trend_direction = "📈 Rising" if recent_avg > older_avg else "📉 Declining" if recent_avg < older_avg else "➡️ Stable"
        else:
            trend_direction = "➡️ Stable"
        
        return {
            'total_mentions': len(items),
            'daily_average': len(items) / 7,
            'top_features': dict(claude_terms.most_common(5)),
            'trend_direction': trend_direction,
            'daily_distribution': dict(daily_counts)
        }
    
    def generate_trend_report(self) -> str:
        """
        Generate a comprehensive trend report
        
        Returns:
            Formatted trend report string
        """
        # Get general trending topics
        trending = self.detect_trending_topics(period_hours=24)
        
        # Get Claude-specific trends
        claude_trends = self.detect_claude_trends()
        
        # Format report
        report = f"""
📈 TRENDING TOPICS REPORT
{datetime.now().strftime('%B %d, %Y %I:%M %p')}
{'=' * 50}

🔥 TOP TRENDING TOPICS (24 HOURS)
{'=' * 50}
"""
        
        for i, topic in enumerate(trending[:10], 1):
            emoji = "🆕" if topic['is_new'] else "📈" if topic['growth_rate'] > 50 else "➡️"
            report += f"""
{i}. {emoji} {topic['topic'].title()}
   Current: {topic['current_mentions']} mentions
   Previous: {topic['previous_mentions']} mentions
   Growth: {topic['growth_rate']:.1f}%
   Score: {topic['trend_score']:.3f}
"""
        
        report += f"""

🤖 CLAUDE & ANTHROPIC TRENDS (7 DAYS)
{'=' * 50}
Status: {claude_trends['trend_direction']}
Total Mentions: {claude_trends['total_mentions']}
Daily Average: {claude_trends['daily_average']:.1f}

Top Claude Features:
"""
        
        for feature, count in claude_trends['top_features'].items():
            report += f"  • {feature}: {count} mentions\n"
        
        # Add emerging topics
        new_topics = [t for t in trending if t['is_new']][:5]
        if new_topics:
            report += f"""

🌟 EMERGING TOPICS
{'=' * 50}
"""
            for topic in new_topics:
                report += f"  • {topic['topic'].title()} ({topic['current_mentions']} mentions)\n"
        
        report += f"""

{'=' * 50}
Generated by Universal Topic Intelligence System
View dashboard: http://localhost:5001
"""
        
        return report


def test_trending_detector():
    """Test the trending topic detector"""
    detector = TrendingTopicDetector()
    
    print("🔍 Detecting Trending Topics...")
    print("=" * 50)
    
    # Detect general trends
    trends = detector.detect_trending_topics(period_hours=24)
    
    if trends:
        print("\n📊 Top 5 Trending Topics:")
        for i, topic in enumerate(trends[:5], 1):
            status = "🆕 NEW" if topic['is_new'] else f"📈 +{topic['growth_rate']:.0f}%"
            print(f"{i}. {topic['topic'].title()} - {status}")
            print(f"   Mentions: {topic['current_mentions']} (was {topic['previous_mentions']})")
    else:
        print("No trending topics detected")
    
    # Detect Claude trends
    print("\n🤖 Claude-Specific Trends:")
    claude_trends = detector.detect_claude_trends()
    print(f"Direction: {claude_trends['trend_direction']}")
    print(f"Total mentions (7 days): {claude_trends['total_mentions']}")
    print(f"Top features: {list(claude_trends['top_features'].keys())}")
    
    # Generate full report
    print("\n" + "=" * 50)
    print("Generating Full Trend Report...")
    print("=" * 50)
    
    report = detector.generate_trend_report()
    print(report)
    
    # Save report
    with open("digests/trend_report.txt", "w") as f:
        f.write(report)
    print("\n✅ Trend report saved to digests/trend_report.txt")


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Run test
    test_trending_detector()