#!/usr/bin/env python3
"""
Tests for the FastAPI dashboard
"""

import pytest
import sqlite3
import tempfile
from datetime import datetime
from pathlib import Path
import sys
from fastapi.testclient import TestClient

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dashboard import app, get_db
from contextlib import contextmanager

@pytest.fixture
def temp_db():
    """Create temporary database with test data"""
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.close()
    
    # Initialize database with schema and test data
    with sqlite3.connect(temp_file.name) as conn:
        cursor = conn.cursor()
        
        # Create schema
        cursor.execute('''
            CREATE TABLE content_items (
                item_id TEXT PRIMARY KEY,
                source_id TEXT,
                title TEXT,
                content TEXT,
                url TEXT,
                published_date TIMESTAMP,
                collected_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                priority_level TEXT,
                priority_score REAL,
                topics TEXT,
                is_english INTEGER DEFAULT 1
            )
        ''')
        
        # Insert test data
        test_items = [
            ('test1', 'react_blog', 'React 19 Released', 'React 19 introduces new features', 'https://react.dev/blog/react-19', datetime.now(), datetime.now(), 'critical', 0.9, 'react,javascript', 1),
            ('test2', 'claude_reddit', 'Claude AI Discussion', 'Community discussion about Claude', 'https://reddit.com/r/claude', datetime.now(), datetime.now(), 'high', 0.7, 'claude,ai', 1),
            ('test3', 'crypto_news', 'Bitcoin Update', 'Bitcoin price movement', 'https://crypto.com/bitcoin', datetime.now(), datetime.now(), 'medium', 0.5, 'crypto,bitcoin', 1),
            ('test4', 'spam_source', 'Low Quality Content', 'This is low quality content', 'https://spam.com/content', datetime.now(), datetime.now(), 'low', 0.2, 'spam', 1)
        ]
        
        cursor.executemany('''
            INSERT INTO content_items 
            (item_id, source_id, title, content, url, published_date, collected_date, priority_level, priority_score, topics, is_english)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', test_items)
        
        conn.commit()
    
    return temp_file.name

@pytest.fixture
def client(temp_db):
    """Create test client with temporary database"""
    
    @contextmanager
    def get_test_db():
        conn = sqlite3.connect(temp_db)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    # Override the database dependency
    app.dependency_overrides[get_db] = get_test_db
    
    with TestClient(app) as client:
        yield client
    
    # Clean up override
    app.dependency_overrides.clear()

def test_dashboard_home(client):
    """Test dashboard home page loads"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Universal Topic Intelligence Dashboard" in response.text
    assert "text/html" in response.headers["content-type"]

def test_stats_api(client):
    """Test statistics API endpoint"""
    response = client.get("/api/stats")
    assert response.status_code == 200
    
    data = response.json()
    assert "total_items" in data
    assert "critical_items" in data
    assert "high_priority_items" in data
    assert "sources_count" in data
    assert "last_update" in data
    
    # Verify counts match test data
    assert data["total_items"] == 4  # All test items
    assert data["critical_items"] == 1  # React 19 item
    assert data["high_priority_items"] == 1  # Claude AI item
    assert data["sources_count"] == 3  # 3 unique sources

def test_content_api_all(client):
    """Test content API returns all items"""
    response = client.get("/api/content")
    assert response.status_code == 200
    
    items = response.json()
    assert len(items) == 4
    
    # Check first item structure
    first_item = items[0]
    assert "item_id" in first_item
    assert "title" in first_item
    assert "priority" in first_item
    assert "priority_score" in first_item
    assert "topics" in first_item
    assert "is_bookmarked" in first_item
    assert "is_read" in first_item

def test_content_api_priority_filter(client):
    """Test content API with priority filter"""
    # Test critical priority filter
    response = client.get("/api/content?priority=critical")
    assert response.status_code == 200
    
    items = response.json()
    assert len(items) == 1
    assert items[0]["title"] == "React 19 Released"
    assert items[0]["priority"] == "critical"

def test_content_api_search(client):
    """Test content API with search"""
    # Search for React
    response = client.get("/api/content?search=React")
    assert response.status_code == 200
    
    items = response.json()
    assert len(items) == 1
    assert "React" in items[0]["title"]
    
    # Search for AI  
    response = client.get("/api/content?search=AI")
    assert response.status_code == 200
    
    items = response.json()
    assert len(items) == 1
    assert "Claude AI" in items[0]["title"]

def test_content_api_pagination(client):
    """Test content API pagination"""
    # Get first 2 items
    response = client.get("/api/content?limit=2&offset=0")
    assert response.status_code == 200
    
    items = response.json()
    assert len(items) == 2
    
    # Get next 2 items
    response = client.get("/api/content?limit=2&offset=2")
    assert response.status_code == 200
    
    items = response.json()
    assert len(items) == 2

def test_bookmark_api(client):
    """Test bookmark functionality"""
    # Add bookmark
    response = client.post("/api/bookmark?item_id=test1")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "added"
    assert data["item_id"] == "test1"
    
    # Remove bookmark
    response = client.post("/api/bookmark?item_id=test1")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "removed"
    assert data["item_id"] == "test1"

def test_mark_read_api(client):
    """Test mark as read functionality"""
    response = client.post("/api/mark-read?item_id=test2")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "marked_read"
    assert data["item_id"] == "test2"

def test_api_validation(client):
    """Test API parameter validation"""
    # Test invalid priority filter
    response = client.get("/api/content?priority=invalid")
    assert response.status_code == 200  # Should still work, just return no results
    items = response.json()
    assert len(items) == 0
    
    # Test limit validation  
    response = client.get("/api/content?limit=250")  # Over max limit
    assert response.status_code == 422  # Validation error
    
    # Test negative offset
    response = client.get("/api/content?offset=-1") 
    assert response.status_code == 422  # Validation error

def test_content_ordering(client):
    """Test that content is ordered by priority score desc"""
    response = client.get("/api/content")
    assert response.status_code == 200
    
    items = response.json()
    assert len(items) == 4
    
    # Should be ordered by priority score (descending)
    scores = [item["priority_score"] for item in items]
    assert scores == sorted(scores, reverse=True)
    
    # First item should be highest priority
    assert items[0]["priority"] == "critical"
    assert items[0]["priority_score"] == 0.9

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])