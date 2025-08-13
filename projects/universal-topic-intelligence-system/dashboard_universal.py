#!/usr/bin/env python3
"""
Universal Topic Intelligence Dashboard
Dynamically displays content from all monitored topics
"""

import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional
from contextlib import contextmanager

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from enum import Enum

# Initialize FastAPI app
app = FastAPI(
    title="Universal Topic Intelligence System",
    description="Multi-topic monitoring dashboard with dynamic topic selection",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database paths
DB_PATH = Path("topic_intelligence.db")
USER_DB_PATH = Path("storage/user_data.db")

# Load topic configurations
from sources.universal_topic_monitor_fixed import UniversalTopicMonitorFixed
topic_monitor = UniversalTopicMonitorFixed()
AVAILABLE_TOPICS = topic_monitor.list_available_topics()

def init_user_database():
    """Initialize user data database"""
    with sqlite3.connect(USER_DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS bookmarks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id TEXT NOT NULL UNIQUE,
                saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS read_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id TEXT NOT NULL UNIQUE,
                read_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

# Initialize databases
init_user_database()

@contextmanager
def get_db():
    """Database connection context manager"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# Pydantic models
class TopicInfo(BaseModel):
    slug: str
    name: str
    description: str
    source_count: int
    priority_level: str
    status: str
    has_quality_scorer: bool

class Stats(BaseModel):
    total_items: int
    total_topics: int
    active_topics: int
    critical_items: int
    high_priority_items: int
    topics_breakdown: Dict[str, Dict[str, int]]
    last_update: Optional[str]

class ContentItemResponse(BaseModel):
    item_id: str
    source_id: str
    title: str
    content: Optional[str]
    url: Optional[str]
    published_date: str
    author: Optional[str]
    topics: List[str]
    priority: str
    priority_score: float
    is_bookmarked: bool = False
    is_read: bool = False
    reading_time: int = 0
    topic_tags: List[str] = []

# API endpoints
@app.get("/api/topics", response_model=List[TopicInfo])
async def get_topics():
    """Get all available topics"""
    return AVAILABLE_TOPICS

@app.get("/api/stats", response_model=Stats)
async def get_stats(topic: Optional[str] = None):
    """Get dashboard statistics, optionally filtered by topic"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Build topic filter
        topic_filter = ""
        if topic:
            topic_filter = f"AND topics LIKE '%topic:{topic}%'"
        
        # Total items
        cursor.execute(f"SELECT COUNT(*) FROM content_items WHERE is_english = 1 {topic_filter}")
        total_items = cursor.fetchone()[0]
        
        # Critical items
        cursor.execute(f"""
            SELECT COUNT(*) FROM content_items 
            WHERE is_english = 1 AND priority_level = 'critical' {topic_filter}
        """)
        critical_items = cursor.fetchone()[0]
        
        # High priority items
        cursor.execute(f"""
            SELECT COUNT(*) FROM content_items 
            WHERE is_english = 1 AND priority_level = 'high' {topic_filter}
        """)
        high_priority_items = cursor.fetchone()[0]
        
        # Get breakdown by topic
        topics_breakdown = {}
        for topic_info in AVAILABLE_TOPICS:
            slug = topic_info['slug']
            cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN priority_level = 'critical' THEN 1 ELSE 0 END) as critical,
                    SUM(CASE WHEN priority_level = 'high' THEN 1 ELSE 0 END) as high,
                    SUM(CASE WHEN priority_level = 'medium' THEN 1 ELSE 0 END) as medium
                FROM content_items 
                WHERE is_english = 1 AND topics LIKE ?
            """, (f'%topic:{slug}%',))
            row = cursor.fetchone()
            topics_breakdown[slug] = {
                'total': row[0] or 0,
                'critical': row[1] or 0,
                'high': row[2] or 0,
                'medium': row[3] or 0
            }
        
        # Last update time
        cursor.execute("SELECT MAX(created_at) FROM content_items")
        last_update = cursor.fetchone()[0]
        
        return Stats(
            total_items=total_items,
            total_topics=len(AVAILABLE_TOPICS),
            active_topics=len([t for t in AVAILABLE_TOPICS if t['status'] == 'active']),
            critical_items=critical_items,
            high_priority_items=high_priority_items,
            topics_breakdown=topics_breakdown,
            last_update=last_update
        )

@app.get("/api/content", response_model=List[ContentItemResponse])
async def get_content(
    topic: Optional[str] = None,
    priority: Optional[str] = None,
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    search: Optional[str] = None
):
    """Get content items with optional filtering"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Build query
        query = """
            SELECT DISTINCT
                c.item_id,
                c.source_id,
                c.title,
                c.content,
                c.url,
                c.published_date,
                c.author,
                c.topics,
                c.priority_level,
                c.priority_score,
                c.quality_score,
                c.created_at
            FROM content_items c
            WHERE c.is_english = 1
        """
        params = []
        
        # Add topic filter
        if topic:
            query += " AND c.topics LIKE ?"
            params.append(f'%topic:{topic}%')
        
        # Add priority filter
        if priority:
            query += " AND c.priority_level = ?"
            params.append(priority)
        
        # Add search filter
        if search:
            query += " AND (c.title LIKE ? OR c.content LIKE ?)"
            params.extend([f'%{search}%', f'%{search}%'])
        
        # Order and limit
        query += " ORDER BY c.priority_score DESC, c.created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        # Get bookmarks and read history
        user_conn = sqlite3.connect(USER_DB_PATH)
        user_cursor = user_conn.cursor()
        
        items = []
        for row in rows:
            item_id = row['item_id']
            
            # Check bookmark status
            user_cursor.execute("SELECT 1 FROM bookmarks WHERE item_id = ?", (item_id,))
            is_bookmarked = user_cursor.fetchone() is not None
            
            # Check read status
            user_cursor.execute("SELECT 1 FROM read_history WHERE item_id = ?", (item_id,))
            is_read = user_cursor.fetchone() is not None
            
            # Extract topic tags
            topic_tags = []
            if row['topics']:
                for t in row['topics'].split(','):
                    if t.startswith('topic:'):
                        topic_tags.append(t.replace('topic:', '').strip())
            
            # Calculate reading time (rough estimate)
            content_length = len(row['content']) if row['content'] else 0
            reading_time = max(1, content_length // 1000)  # ~200 words per minute
            
            items.append(ContentItemResponse(
                item_id=item_id,
                source_id=row['source_id'],
                title=row['title'],
                content=row['content'],
                url=row['url'],
                published_date=row['published_date'],
                author=row['author'],
                topics=row['topics'].split(',') if row['topics'] else [],
                priority=row['priority_level'],
                priority_score=row['priority_score'],
                is_bookmarked=is_bookmarked,
                is_read=is_read,
                reading_time=reading_time,
                topic_tags=topic_tags
            ))
        
        user_conn.close()
        return items

@app.post("/api/bookmark")
async def toggle_bookmark(item_id: str = Query(...)):
    """Toggle bookmark status for an item"""
    with sqlite3.connect(USER_DB_PATH) as conn:
        cursor = conn.cursor()
        
        # Check if already bookmarked
        cursor.execute("SELECT 1 FROM bookmarks WHERE item_id = ?", (item_id,))
        exists = cursor.fetchone()
        
        if exists:
            cursor.execute("DELETE FROM bookmarks WHERE item_id = ?", (item_id,))
            status = "removed"
        else:
            cursor.execute("INSERT INTO bookmarks (item_id) VALUES (?)", (item_id,))
            status = "added"
        
        conn.commit()
        return {"status": status, "item_id": item_id}

@app.post("/api/mark-read")
async def mark_as_read(item_id: str = Query(...)):
    """Mark an item as read"""
    with sqlite3.connect(USER_DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO read_history (item_id) VALUES (?)",
            (item_id,)
        )
        conn.commit()
        return {"status": "marked_read", "item_id": item_id}

@app.get("/api/bookmarks", response_model=List[ContentItemResponse])
async def get_bookmarks():
    """Get all bookmarked items"""
    with sqlite3.connect(USER_DB_PATH) as user_conn:
        user_cursor = user_conn.cursor()
        user_cursor.execute("SELECT item_id FROM bookmarks ORDER BY saved_at DESC")
        bookmarked_ids = [row[0] for row in user_cursor.fetchall()]
    
    if not bookmarked_ids:
        return []
    
    # Get full content for bookmarked items
    with get_db() as conn:
        cursor = conn.cursor()
        placeholders = ','.join('?' * len(bookmarked_ids))
        query = f"""
            SELECT * FROM content_items
            WHERE item_id IN ({placeholders})
            ORDER BY priority_score DESC
        """
        cursor.execute(query, bookmarked_ids)
        rows = cursor.fetchall()
        
        items = []
        for row in rows:
            topic_tags = []
            if row['topics']:
                for t in row['topics'].split(','):
                    if t.startswith('topic:'):
                        topic_tags.append(t.replace('topic:', '').strip())
            
            items.append(ContentItemResponse(
                item_id=row['item_id'],
                source_id=row['source_id'],
                title=row['title'],
                content=row['content'],
                url=row['url'],
                published_date=row['published_date'],
                author=row['author'],
                topics=row['topics'].split(',') if row['topics'] else [],
                priority=row['priority_level'],
                priority_score=row['priority_score'],
                is_bookmarked=True,
                is_read=False,
                reading_time=max(1, len(row['content'] or '') // 1000),
                topic_tags=topic_tags
            ))
        
        return items

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the universal dashboard HTML"""
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Universal Topic Intelligence Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; 
            background: #f5f5f7; 
            color: #1d1d1f;
        }
        .header {
            background: white;
            border-bottom: 1px solid #d2d2d7;
            padding: 15px 30px;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        .header h1 {
            font-size: 24px;
            font-weight: 600;
        }
        .controls {
            background: white;
            padding: 15px 30px;
            border-bottom: 1px solid #d2d2d7;
            display: flex;
            gap: 15px;
            align-items: center;
            flex-wrap: wrap;
        }
        .topic-selector {
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }
        .topic-pill {
            padding: 6px 14px;
            border-radius: 20px;
            background: #f0f0f2;
            color: #1d1d1f;
            cursor: pointer;
            transition: all 0.2s;
            border: 2px solid transparent;
            font-size: 14px;
        }
        .topic-pill:hover {
            background: #e0e0e2;
        }
        .topic-pill.active {
            background: #007AFF;
            color: white;
            border-color: #0051D5;
        }
        .stats-bar {
            background: white;
            padding: 20px 30px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            border-bottom: 1px solid #d2d2d7;
        }
        .stat-item {
            text-align: center;
        }
        .stat-number {
            font-size: 28px;
            font-weight: 600;
            color: #007AFF;
        }
        .stat-label {
            font-size: 12px;
            color: #86868b;
            text-transform: uppercase;
            margin-top: 4px;
        }
        .content-area {
            padding: 20px 30px;
            max-width: 1400px;
            margin: 0 auto;
        }
        .content-item {
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            transition: all 0.2s;
        }
        .content-item:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.12);
            transform: translateY(-2px);
        }
        .content-header {
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 10px;
        }
        .content-title {
            font-size: 18px;
            font-weight: 600;
            color: #1d1d1f;
            text-decoration: none;
            flex: 1;
        }
        .content-title:hover {
            color: #007AFF;
        }
        .priority-badge {
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
        }
        .priority-critical {
            background: #FF3B30;
            color: white;
        }
        .priority-high {
            background: #FF9500;
            color: white;
        }
        .priority-medium {
            background: #34C759;
            color: white;
        }
        .priority-low {
            background: #8E8E93;
            color: white;
        }
        .content-meta {
            display: flex;
            gap: 15px;
            font-size: 13px;
            color: #86868b;
            margin-bottom: 10px;
        }
        .topic-tags {
            display: flex;
            gap: 6px;
            margin-top: 10px;
        }
        .topic-tag {
            padding: 3px 8px;
            background: #F2F2F7;
            border-radius: 4px;
            font-size: 11px;
            color: #48484A;
        }
        .content-snippet {
            color: #424245;
            line-height: 1.5;
            font-size: 14px;
        }
        .search-box {
            flex: 1;
            max-width: 400px;
        }
        .search-box input {
            width: 100%;
            padding: 8px 15px;
            border: 1px solid #d2d2d7;
            border-radius: 8px;
            font-size: 14px;
        }
        .priority-filter {
            display: flex;
            gap: 8px;
        }
        .filter-btn {
            padding: 6px 12px;
            border: 1px solid #d2d2d7;
            background: white;
            border-radius: 6px;
            cursor: pointer;
            font-size: 13px;
            transition: all 0.2s;
        }
        .filter-btn:hover {
            background: #f0f0f2;
        }
        .filter-btn.active {
            background: #007AFF;
            color: white;
            border-color: #007AFF;
        }
        .loading {
            text-align: center;
            padding: 40px;
            color: #86868b;
        }
        .bookmark-btn {
            background: none;
            border: none;
            cursor: pointer;
            font-size: 20px;
            padding: 4px;
        }
        .bookmark-btn.bookmarked {
            color: #FF9500;
        }
        .read-indicator {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #34C759;
            display: inline-block;
            margin-left: 8px;
        }
        .topic-breakdown {
            background: white;
            padding: 20px 30px;
            margin: 20px 30px;
            border-radius: 12px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        }
        .breakdown-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 15px;
        }
        .breakdown-item {
            padding: 15px;
            background: #F2F2F7;
            border-radius: 8px;
        }
        .breakdown-title {
            font-weight: 600;
            margin-bottom: 8px;
        }
        .breakdown-stats {
            font-size: 13px;
            color: #86868b;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🌐 Universal Topic Intelligence Dashboard</h1>
    </div>
    
    <div class="controls">
        <div class="topic-selector" id="topicSelector">
            <div class="topic-pill active" data-topic="all">All Topics</div>
        </div>
        <div class="search-box">
            <input type="text" id="searchInput" placeholder="Search content...">
        </div>
        <div class="priority-filter">
            <button class="filter-btn active" data-priority="all">All</button>
            <button class="filter-btn" data-priority="critical">Critical</button>
            <button class="filter-btn" data-priority="high">High</button>
            <button class="filter-btn" data-priority="medium">Medium</button>
        </div>
    </div>
    
    <div class="stats-bar" id="statsBar">
        <div class="stat-item">
            <div class="stat-number">-</div>
            <div class="stat-label">Total Items</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">-</div>
            <div class="stat-label">Active Topics</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">-</div>
            <div class="stat-label">Critical</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">-</div>
            <div class="stat-label">High Priority</div>
        </div>
    </div>
    
    <div class="topic-breakdown" id="topicBreakdown" style="display: none;">
        <h3>Topic Breakdown</h3>
        <div class="breakdown-grid" id="breakdownGrid"></div>
    </div>
    
    <div class="content-area" id="contentArea">
        <div class="loading">Loading content...</div>
    </div>
    
    <script>
        let currentTopic = 'all';
        let currentPriority = 'all';
        let currentSearch = '';
        let allTopics = [];
        
        async function loadTopics() {
            const response = await fetch('/api/topics');
            allTopics = await response.json();
            
            const selector = document.getElementById('topicSelector');
            allTopics.forEach(topic => {
                const pill = document.createElement('div');
                pill.className = 'topic-pill';
                pill.dataset.topic = topic.slug;
                pill.textContent = topic.name;
                pill.onclick = () => selectTopic(topic.slug);
                selector.appendChild(pill);
            });
        }
        
        async function loadStats() {
            const params = currentTopic !== 'all' ? `?topic=${currentTopic}` : '';
            const response = await fetch(`/api/stats${params}`);
            const stats = await response.json();
            
            const statsBar = document.getElementById('statsBar');
            statsBar.innerHTML = `
                <div class="stat-item">
                    <div class="stat-number">${stats.total_items}</div>
                    <div class="stat-label">Total Items</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">${stats.active_topics}</div>
                    <div class="stat-label">Active Topics</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">${stats.critical_items}</div>
                    <div class="stat-label">Critical</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">${stats.high_priority_items}</div>
                    <div class="stat-label">High Priority</div>
                </div>
            `;
            
            // Show topic breakdown if viewing all topics
            if (currentTopic === 'all' && stats.topics_breakdown) {
                const breakdown = document.getElementById('topicBreakdown');
                const grid = document.getElementById('breakdownGrid');
                breakdown.style.display = 'block';
                
                grid.innerHTML = '';
                for (const [slug, data] of Object.entries(stats.topics_breakdown)) {
                    const topicInfo = allTopics.find(t => t.slug === slug);
                    if (data.total > 0) {
                        grid.innerHTML += `
                            <div class="breakdown-item">
                                <div class="breakdown-title">${topicInfo?.name || slug}</div>
                                <div class="breakdown-stats">
                                    Total: ${data.total} | 
                                    Critical: ${data.critical} | 
                                    High: ${data.high}
                                </div>
                            </div>
                        `;
                    }
                }
            } else {
                document.getElementById('topicBreakdown').style.display = 'none';
            }
        }
        
        async function loadContent() {
            const params = new URLSearchParams();
            if (currentTopic !== 'all') params.append('topic', currentTopic);
            if (currentPriority !== 'all') params.append('priority', currentPriority);
            if (currentSearch) params.append('search', currentSearch);
            params.append('limit', '100');
            
            const response = await fetch(`/api/content?${params}`);
            const items = await response.json();
            
            const contentArea = document.getElementById('contentArea');
            
            if (items.length === 0) {
                contentArea.innerHTML = '<div class="loading">No content found</div>';
                return;
            }
            
            contentArea.innerHTML = items.map(item => `
                <div class="content-item" data-id="${item.item_id}">
                    <div class="content-header">
                        <a href="${item.url}" target="_blank" class="content-title">
                            ${item.title}
                            ${item.is_read ? '<span class="read-indicator" title="Read"></span>' : ''}
                        </a>
                        <div style="display: flex; gap: 10px; align-items: center;">
                            <button class="bookmark-btn ${item.is_bookmarked ? 'bookmarked' : ''}" 
                                    onclick="toggleBookmark('${item.item_id}')">
                                ${item.is_bookmarked ? '⭐' : '☆'}
                            </button>
                            <span class="priority-badge priority-${item.priority}">
                                ${item.priority}
                            </span>
                        </div>
                    </div>
                    <div class="content-meta">
                        <span>📅 ${new Date(item.published_date).toLocaleDateString()}</span>
                        <span>📍 ${item.source_id}</span>
                        <span>⏱️ ${item.reading_time} min read</span>
                        <span>📊 Score: ${(item.priority_score * 100).toFixed(0)}%</span>
                    </div>
                    ${item.topic_tags.length > 0 ? `
                        <div class="topic-tags">
                            ${item.topic_tags.map(tag => `<span class="topic-tag">${tag}</span>`).join('')}
                        </div>
                    ` : ''}
                    ${item.content ? `
                        <div class="content-snippet">
                            ${item.content.substring(0, 200)}...
                        </div>
                    ` : ''}
                </div>
            `).join('');
            
            // Mark items as read on click
            document.querySelectorAll('.content-item').forEach(el => {
                el.addEventListener('click', (e) => {
                    if (!e.target.closest('.bookmark-btn')) {
                        markAsRead(el.dataset.id);
                    }
                });
            });
        }
        
        function selectTopic(topic) {
            currentTopic = topic;
            document.querySelectorAll('.topic-pill').forEach(el => {
                el.classList.toggle('active', el.dataset.topic === topic);
            });
            loadStats();
            loadContent();
        }
        
        function selectPriority(priority) {
            currentPriority = priority;
            document.querySelectorAll('.filter-btn').forEach(el => {
                el.classList.toggle('active', el.dataset.priority === priority);
            });
            loadContent();
        }
        
        async function toggleBookmark(itemId) {
            await fetch(`/api/bookmark?item_id=${itemId}`, { method: 'POST' });
            loadContent();
        }
        
        async function markAsRead(itemId) {
            await fetch(`/api/mark-read?item_id=${itemId}`, { method: 'POST' });
        }
        
        // Event listeners
        document.getElementById('searchInput').addEventListener('input', (e) => {
            currentSearch = e.target.value;
            clearTimeout(window.searchTimeout);
            window.searchTimeout = setTimeout(loadContent, 300);
        });
        
        document.querySelectorAll('.filter-btn').forEach(btn => {
            btn.addEventListener('click', () => selectPriority(btn.dataset.priority));
        });
        
        // Initialize
        loadTopics().then(() => {
            loadStats();
            loadContent();
        });
        
        // Auto-refresh every 5 minutes
        setInterval(() => {
            loadStats();
            loadContent();
        }, 300000);
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html_content)

@app.get("/youtube-intelligence")
async def youtube_intelligence():
    """Serve the YouTube Intelligence dashboard"""
    youtube_dashboard_path = Path("dashboards/youtube_intelligence.html")
    if youtube_dashboard_path.exists():
        with open(youtube_dashboard_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return HTMLResponse(content=content)
    return HTMLResponse(content="<h1>YouTube Dashboard Not Found</h1>")

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Universal Topic Intelligence Dashboard")
    print("📍 Open your browser to: http://localhost:5001")
    print("\nAvailable Topics:")
    for topic in AVAILABLE_TOPICS:
        print(f"  - {topic['name']} ({topic['slug']}): {topic['source_count']} sources")
    
    uvicorn.run(app, host="0.0.0.0", port=5001)