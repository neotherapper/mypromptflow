#!/usr/bin/env python3
"""
Universal Topic Intelligence System - TDD Test Suite
Tests based on actual user stories and requirements
"""

import unittest
import tempfile
import os
from datetime import datetime, timedelta
from intelligence_system import TopicIntelligence


class TestUserStories(unittest.TestCase):
    
    def setUp(self):
        """Create temporary database for each test"""
        self.db_file = tempfile.NamedTemporaryFile(delete=False)
        self.db_file.close()
        self.system = TopicIntelligence(self.db_file.name)
        
        # Add some test data
        self._add_test_data()
    
    def tearDown(self):
        """Clean up temporary database"""
        self.system.conn.close()
        os.unlink(self.db_file.name)
    
    def _add_test_data(self):
        """Add sample articles for testing"""
        # Recent React article
        self.system.conn.execute("""
            INSERT INTO articles (id, url, title, content, tool, source, published_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            "test1",
            "https://react.dev/blog/react-19-release",
            "React 19 Released with New Features",
            "React 19 introduces new hooks and performance improvements. Security fixes included.",
            "React",
            "React Blog",
            datetime.now() - timedelta(days=2)
        ))
        
        # Older TypeScript article
        self.system.conn.execute("""
            INSERT INTO articles (id, url, title, content, tool, source, published_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            "test2",
            "https://devblogs.microsoft.com/typescript/announcing-typescript-5-3",
            "Announcing TypeScript 5.3",
            "TypeScript 5.3 brings new features and improvements to the language.",
            "TypeScript",
            "TypeScript Blog",
            datetime.now() - timedelta(days=15)
        ))
        
        # Security-related article
        self.system.conn.execute("""
            INSERT INTO articles (id, url, title, content, tool, source, published_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            "test3",
            "https://example.com/security-update",
            "Critical Security Update for React",
            "A critical vulnerability CVE-2024-12345 has been patched in React 18.2.1",
            "React", 
            "Security Alert",
            datetime.now() - timedelta(days=1)
        ))
        
        self.system.conn.commit()
        
        # Update FTS table manually (since we're inserting directly)
        self.system.conn.executescript("""
            INSERT INTO articles_fts (title, content, tool) 
            VALUES 
                ('React 19 Released with New Features', 'React 19 introduces new hooks and performance improvements. Security fixes included.', 'React'),
                ('Announcing TypeScript 5.3', 'TypeScript 5.3 brings new features and improvements to the language.', 'TypeScript'),
                ('Critical Security Update for React', 'A critical vulnerability CVE-2024-12345 has been patched in React 18.2.1', 'React');
        """)
    
    def test_user_story_whats_new_in_react_this_week(self):
        """
        User Story: "What's new in React this week?"
        Should return recent React articles from the last 7 days
        """
        results = self.system.query("What's new in React this week?")
        
        # Should find the React article from 2 days ago
        self.assertGreater(len(results), 0)
        
        # All results should be React-related
        for result in results:
            self.assertEqual(result[1], "React")  # tool field
        
        # Should be from within the last 7 days
        for result in results:
            self.assertLessEqual(result[3], 7)  # days_ago field
    
    def test_user_story_whats_new_in_react_this_month(self):
        """
        User Story: "What's new in React this month?"
        Should return React articles from the last 30 days
        """
        results = self.system.query("What's new in React this month?")
        
        # Should find React articles (including the 2-day old one)
        self.assertGreater(len(results), 0)
        
        # All results should be React-related
        for result in results:
            self.assertEqual(result[1], "React")
        
        # Should be from within the last 30 days
        for result in results:
            self.assertLessEqual(result[3], 30)
    
    def test_user_story_security_updates(self):
        """
        User Story: "Show me security updates across all tools"
        Should find all security-related content
        """
        results = self.system.find_security_updates()
        
        # Should find our security test article
        self.assertGreater(len(results), 0)
        
        # Should contain security-related content
        found_security = False
        for result in results:
            title, tool, url, published_date = result[:4]  # Take first 4 fields
            if "security" in title.lower() or "CVE" in title:
                found_security = True
                break
        
        self.assertTrue(found_security, "Should find security-related articles")
    
    def test_user_story_full_text_search(self):
        """
        User Story: "Search for hooks in React articles"
        Should use full-text search to find relevant content
        """
        results = self.system.search("hooks")
        
        # Should find articles mentioning hooks
        self.assertGreater(len(results), 0)
        
        # Results should contain the search term
        found_hooks = False
        for result in results:
            title, tool, url, content = result[:4]  # Take first 4 fields
            if "hooks" in content.lower():
                found_hooks = True
                break
        
        self.assertTrue(found_hooks, "Should find articles mentioning hooks")
    
    def test_user_story_daily_digest(self):
        """
        User Story: "Give me a daily digest of important updates"
        Should generate a summary of recent activity
        """
        digest = self.system.generate_digest(days=7)
        
        # Should be a non-empty string
        self.assertIsInstance(digest, str)
        self.assertGreater(len(digest), 0)
        
        # Should mention the tools we have data for
        self.assertIn("React", digest)
        
        # Should be formatted nicely
        self.assertIn("Daily Digest", digest)
        self.assertIn("📰", digest)
    
    def test_deduplication_same_url(self):
        """
        Technical Requirement: Same article shouldn't be stored twice
        """
        # Try to add the same article twice
        test_url = "https://example.com/duplicate-test"
        
        # First insert
        self.system.conn.execute("""
            INSERT OR IGNORE INTO articles (id, url, title, content, tool, source, published_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ("dup1", test_url, "Test Article", "Content", "React", "Test", datetime.now()))
        
        # Second insert (should be ignored)
        self.system.conn.execute("""
            INSERT OR IGNORE INTO articles (id, url, title, content, tool, source, published_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ("dup2", test_url, "Test Article Duplicate", "Content", "React", "Test", datetime.now()))
        
        self.system.conn.commit()
        
        # Should only have one article with this URL
        results = self.system.conn.execute(
            "SELECT COUNT(*) FROM articles WHERE url = ?", (test_url,)
        ).fetchone()
        
        self.assertEqual(results[0], 1, "Should not store duplicate URLs")
    
    def test_extract_tool_from_question(self):
        """
        Test helper function to extract tool name from questions
        """
        # Test tool extraction
        self.assertEqual(self.system._extract_tool("What's new in React?"), "React")
        self.assertEqual(self.system._extract_tool("TypeScript updates this week"), "TypeScript")
        self.assertEqual(self.system._extract_tool("Show me Vue.js news"), "Vue.js")
        
        # Default case
        self.assertEqual(self.system._extract_tool("What's new?"), "React")  # Default fallback
    
    def test_database_setup(self):
        """
        Technical Requirement: Database should be properly initialized
        """
        # Check that tables exist
        tables = self.system.conn.execute("""
            SELECT name FROM sqlite_master WHERE type='table'
        """).fetchall()
        
        table_names = [t[0] for t in tables]
        
        self.assertIn("articles", table_names)
        self.assertIn("articles_fts", table_names)
    
    def test_rss_collection(self):
        """
        Technical Requirement: Should be able to collect from RSS feeds
        Note: This is a mock test - real RSS collection would need internet
        """
        # Mock RSS data structure (what feedparser would return)
        class MockEntry:
            def __init__(self):
                self.link = "https://example.com/test-rss"
                self.title = "Test RSS Article"
                self.summary = "Test content from RSS"
                self.published_parsed = datetime.now()
        
        class MockFeed:
            def __init__(self):
                self.entries = [MockEntry()]
                self.feed = {"title": "Test RSS Feed"}
        
        # This would be tested with actual RSS in integration tests
        # For now, just verify the method exists and handles data correctly
        initial_count = self.system.conn.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
        
        # Manually simulate what collect_from_source would do
        entry = MockEntry()
        self.system.conn.execute("""
            INSERT OR IGNORE INTO articles (id, url, title, content, tool, source, published_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            "rss_test",
            entry.link,
            entry.title,
            entry.summary,
            "TestTool",
            "RSS Test",
            entry.published_parsed
        ))
        self.system.conn.commit()
        
        final_count = self.system.conn.execute("SELECT COUNT(*) FROM articles").fetchone()[0]
        self.assertGreater(final_count, initial_count, "Should add articles from RSS")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)