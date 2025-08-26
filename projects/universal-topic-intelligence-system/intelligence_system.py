#!/usr/bin/env python3
"""
Universal Topic Intelligence System - Core Implementation
Simple, effective, TDD-based solution for monitoring development tool updates
"""

import sqlite3
import hashlib
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
import logging

# Optional imports (will handle gracefully if not available)
try:
    import feedparser
except ImportError:
    feedparser = None
    logging.warning("feedparser not available. RSS collection will be disabled.")


class TopicIntelligence:
    """
    Core intelligence system for monitoring development tool updates
    Uses SQLite with FTS5 for simple, effective full-text search
    """
    
    def __init__(self, db_path: str = "intelligence.db"):
        """
        Initialize the intelligence system
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Enable column access by name
        self._setup_database()
        
        # Configure logging
        self.logger = logging.getLogger("TopicIntelligence")
    
    def _setup_database(self):
        """Create tables with full-text search capabilities"""
        self.conn.executescript("""
            -- Main articles table with deduplication
            CREATE TABLE IF NOT EXISTS articles (
                id TEXT PRIMARY KEY,
                url TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                content TEXT,
                tool TEXT NOT NULL,
                source TEXT NOT NULL,
                published_date DATETIME NOT NULL,
                collected_date DATETIME DEFAULT CURRENT_TIMESTAMP
            );
            
            -- Full-text search virtual table using FTS5
            CREATE VIRTUAL TABLE IF NOT EXISTS articles_fts 
            USING fts5(
                title, 
                content, 
                tool,
                content=articles,
                content_rowid=rowid
            );
            
            -- Triggers to keep FTS table in sync with main table
            CREATE TRIGGER IF NOT EXISTS sync_fts_insert 
            AFTER INSERT ON articles 
            BEGIN
                INSERT INTO articles_fts (rowid, title, content, tool) 
                VALUES (new.rowid, new.title, new.content, new.tool);
            END;
            
            CREATE TRIGGER IF NOT EXISTS sync_fts_delete
            AFTER DELETE ON articles 
            BEGIN
                INSERT INTO articles_fts (articles_fts, rowid, title, content, tool) 
                VALUES ('delete', old.rowid, old.title, old.content, old.tool);
            END;
            
            CREATE TRIGGER IF NOT EXISTS sync_fts_update
            AFTER UPDATE ON articles 
            BEGIN
                INSERT INTO articles_fts (articles_fts, rowid, title, content, tool) 
                VALUES ('delete', old.rowid, old.title, old.content, old.tool);
                INSERT INTO articles_fts (rowid, title, content, tool) 
                VALUES (new.rowid, new.title, new.content, new.tool);
            END;
            
            -- Indexes for performance
            CREATE INDEX IF NOT EXISTS idx_published_date 
            ON articles(published_date DESC);
            
            CREATE INDEX IF NOT EXISTS idx_tool 
            ON articles(tool);
            
            CREATE INDEX IF NOT EXISTS idx_tool_date 
            ON articles(tool, published_date DESC);
        """)
        
        self.conn.commit()
    
    def collect_from_source(self, feed_url: str, tool_name: str) -> int:
        """
        Collect articles from an RSS feed
        
        Args:
            feed_url: RSS feed URL
            tool_name: Name of the development tool
            
        Returns:
            Number of new articles collected
        """
        if feedparser is None:
            raise ImportError("feedparser is required for RSS collection. Install with: pip install feedparser")
        
        try:
            feed = feedparser.parse(feed_url)
            
            if not feed.entries:
                self.logger.warning(f"No entries found in RSS feed: {feed_url}")
                return 0
            
            new_articles = 0
            
            for entry in feed.entries:
                # Generate consistent ID
                article_id = hashlib.md5(entry.link.encode()).hexdigest()[:12]
                
                # Parse published date
                published_date = self._parse_date(entry)
                
                # Extract content (try multiple fields)
                content = (
                    entry.get('summary', '') or 
                    entry.get('description', '') or 
                    entry.get('content', [{}])[0].get('value', '') if entry.get('content') else ''
                )
                
                try:
                    self.conn.execute("""
                        INSERT INTO articles (id, url, title, content, tool, source, published_date)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        article_id,
                        entry.link,
                        entry.title,
                        content,
                        tool_name,
                        feed.feed.get('title', tool_name),
                        published_date
                    ))
                    new_articles += 1
                    
                except sqlite3.IntegrityError:
                    # Article already exists (URL is unique)
                    continue
            
            self.conn.commit()
            self.logger.info(f"Collected {new_articles} new articles for {tool_name}")
            return new_articles
            
        except Exception as e:
            self.logger.error(f"Error collecting from {feed_url}: {e}")
            return 0
    
    def _parse_date(self, entry) -> datetime:
        """Parse date from RSS entry"""
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            import time
            return datetime.fromtimestamp(time.mktime(entry.published_parsed))
        elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
            import time
            return datetime.fromtimestamp(time.mktime(entry.updated_parsed))
        else:
            # Fallback to current time
            return datetime.now()
    
    def query(self, question: str) -> List[Tuple]:
        """
        Answer natural language questions about development tools
        
        Args:
            question: Natural language question
            
        Returns:
            List of matching articles as tuples
        """
        question_lower = question.lower()
        
        # Handle "what's new" style questions
        if any(phrase in question_lower for phrase in ["what's new", "whats new", "new in"]):
            tool = self._extract_tool(question)
            
            # Determine timeframe
            if any(word in question_lower for word in ["week", "weekly"]):
                days = 7
            elif any(word in question_lower for word in ["month", "monthly"]):
                days = 30
            elif any(word in question_lower for word in ["today", "daily"]):
                days = 1
            else:
                days = 7  # Default to week
            
            return self.conn.execute("""
                SELECT title, tool, url, 
                       CAST((julianday('now') - julianday(published_date)) AS INTEGER) as days_ago,
                       published_date
                FROM articles
                WHERE tool = ? AND published_date > datetime('now', '-' || ? || ' days')
                ORDER BY published_date DESC
                LIMIT 20
            """, (tool, days)).fetchall()
        
        # Default to full-text search
        return self.search(question)
    
    def search(self, query: str, limit: int = 20) -> List[Tuple]:
        """
        Full-text search across all articles
        
        Args:
            query: Search query
            limit: Maximum results to return
            
        Returns:
            List of matching articles
        """
        try:
            results = self.conn.execute("""
                SELECT a.title, a.tool, a.url, a.content, a.published_date
                FROM articles_fts fts
                JOIN articles a ON a.rowid = fts.rowid
                WHERE articles_fts MATCH ?
                ORDER BY bm25(articles_fts)
                LIMIT ?
            """, (query, limit)).fetchall()
            
            return results
            
        except sqlite3.OperationalError:
            # Fallback to LIKE search if FTS fails
            return self.conn.execute("""
                SELECT title, tool, url, content, published_date
                FROM articles
                WHERE title LIKE ? OR content LIKE ?
                ORDER BY published_date DESC
                LIMIT ?
            """, (f"%{query}%", f"%{query}%", limit)).fetchall()
    
    def find_security_updates(self, days: int = 90) -> List[Tuple]:
        """
        Find security-related updates across all tools
        
        Args:
            days: Look back this many days (default 90)
            
        Returns:
            List of security-related articles
        """
        security_keywords = [
            'security', 'vulnerability', 'CVE-', 'patch', 'fix',
            'exploit', 'attack', 'breach', 'malware', 'XSS',
            'injection', 'csrf', 'authentication', 'authorization'
        ]
        
        # Build WHERE clause with OR conditions
        conditions = []
        params = []
        
        for keyword in security_keywords:
            conditions.extend([
                "title LIKE ?",
                "content LIKE ?"
            ])
            params.extend([f"%{keyword}%", f"%{keyword}%"])
        
        where_clause = " OR ".join(conditions)
        
        # Add date filter
        where_clause = f"({where_clause}) AND published_date > datetime('now', '-{days} days')"
        
        return self.conn.execute(f"""
            SELECT title, tool, url, published_date, content
            FROM articles
            WHERE {where_clause}
            ORDER BY published_date DESC
            LIMIT 50
        """, params).fetchall()
    
    def generate_digest(self, days: int = 1) -> str:
        """
        Generate a digest of recent activity
        
        Args:
            days: Number of days to include in digest
            
        Returns:
            Formatted digest string
        """
        # Get summary by tool
        results = self.conn.execute("""
            SELECT tool, COUNT(*) as count, 
                   GROUP_CONCAT(title, ' | ') as titles
            FROM articles
            WHERE published_date > datetime('now', '-' || ? || ' days')
            GROUP BY tool
            HAVING count > 0
            ORDER BY count DESC
        """, (days,)).fetchall()
        
        if not results:
            return f"📰 Daily Digest - {datetime.now().strftime('%Y-%m-%d')}\n\nNo new updates found."
        
        # Build digest
        time_period = "today" if days == 1 else f"last {days} days"
        digest = f"📰 Daily Digest - {datetime.now().strftime('%Y-%m-%d')}\n"
        digest += f"Updates from {time_period}\n\n"
        
        total_updates = sum(row[1] for row in results)
        digest += f"📊 Summary: {total_updates} updates across {len(results)} tools\n\n"
        
        for tool, count, titles in results:
            digest += f"**{tool}** ({count} update{'s' if count != 1 else ''})\n"
            
            # Show up to 3 most recent titles
            title_list = titles.split(' | ')
            for i, title in enumerate(title_list[:3]):
                digest += f"  • {title}\n"
            
            if len(title_list) > 3:
                digest += f"  ... and {len(title_list) - 3} more\n"
            
            digest += "\n"
        
        return digest
    
    def _extract_tool(self, question: str) -> str:
        """
        Extract tool name from a natural language question
        
        Args:
            question: Natural language question
            
        Returns:
            Tool name (defaults to 'React' if not found)
        """
        question_lower = question.lower()
        
        # Common development tools (expand this list as needed)
        tools = [
            'react', 'typescript', 'vue', 'angular', 'svelte',
            'next.js', 'nextjs', 'nuxt', 'gatsby',
            'node.js', 'nodejs', 'express', 'fastapi', 'django',
            'webpack', 'vite', 'rollup', 'parcel',
            'eslint', 'prettier', 'jest', 'vitest', 'cypress',
            'docker', 'kubernetes', 'aws', 'gcp', 'azure',
            'postgresql', 'mysql', 'mongodb', 'redis',
            'github', 'gitlab', 'figma', 'notion'
        ]
        
        # Look for exact matches first
        for tool in tools:
            if tool in question_lower:
                # Convert to proper case
                if tool == 'nextjs':
                    return 'Next.js'
                elif tool == 'nodejs':
                    return 'Node.js'
                elif tool == 'vue':
                    return 'Vue.js'
                elif tool == 'typescript':
                    return 'TypeScript'
                else:
                    return tool.capitalize()
        
        # Look for patterns like "React.js", "Vue.js", etc. (but not common words)
        tool_pattern = re.search(r'\b([A-Z][a-z]+(?:\.[a-z]+)?)\b', question)
        if tool_pattern:
            potential_tool = tool_pattern.group(1)
            # Skip common question words
            if potential_tool.lower() not in ['what', 'how', 'when', 'where', 'why', 'which', 'new', 'show', 'give']:
                return potential_tool
        
        # Default fallback
        return 'React'
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get system statistics
        
        Returns:
            Dictionary with system statistics
        """
        stats = {}
        
        # Total articles
        stats['total_articles'] = self.conn.execute(
            "SELECT COUNT(*) FROM articles"
        ).fetchone()[0]
        
        # Articles by tool
        tool_stats = self.conn.execute("""
            SELECT tool, COUNT(*) as count
            FROM articles
            GROUP BY tool
            ORDER BY count DESC
        """).fetchall()
        
        stats['by_tool'] = dict(tool_stats)
        
        # Recent activity (last 7 days)
        stats['recent_articles'] = self.conn.execute("""
            SELECT COUNT(*) FROM articles
            WHERE published_date > datetime('now', '-7 days')
        """).fetchone()[0]
        
        # Date range
        date_range = self.conn.execute("""
            SELECT MIN(published_date), MAX(published_date) FROM articles
        """).fetchone()
        
        stats['date_range'] = {
            'earliest': date_range[0],
            'latest': date_range[1]
        }
        
        return stats
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


if __name__ == "__main__":
    # Simple CLI for testing
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python intelligence_system.py <question>")
        print("Example: python intelligence_system.py 'What's new in React this week?'")
        sys.exit(1)
    
    question = " ".join(sys.argv[1:])
    
    with TopicIntelligence() as system:
        results = system.query(question)
        
        if not results:
            print("No results found.")
        else:
            print(f"\n🔍 Results for: {question}")
            print("=" * 50)
            
            for i, result in enumerate(results, 1):
                title = result[0]
                tool = result[1]
                url = result[2]
                
                print(f"\n{i}. {title}")
                print(f"   Tool: {tool}")
                print(f"   URL: {url}")
                
                if len(result) > 4:  # Has days_ago
                    print(f"   Age: {result[3]} days ago")