#!/usr/bin/env python3
"""
Universal Topic Intelligence Dashboard - CLEAN VERSION
Only functional components, working with real data
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from contextlib import contextmanager

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

# Initialize FastAPI app
app = FastAPI(
    title="Universal Topic Intelligence System",
    description="Real-time monitoring dashboard for RSS feeds",
    version="1.0.0"
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

def init_user_database():
    """Initialize user data database"""
    USER_DB_PATH.parent.mkdir(exist_ok=True)
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
class Stats(BaseModel):
    total_items: int
    critical_items: int
    high_priority_items: int
    last_update: Optional[str]
    sources_count: int

class ContentItemResponse(BaseModel):
    item_id: str
    source_id: str
    title: str
    content: Optional[str]
    url: Optional[str]
    published_date: str
    priority: str
    priority_score: float
    topics: List[str]
    is_bookmarked: bool = False
    is_read: bool = False

# API endpoints
@app.get("/api/stats", response_model=Stats)
async def get_stats():
    """Get dashboard statistics"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Total items
        cursor.execute("SELECT COUNT(*) FROM content_items WHERE is_english = 1")
        total_items = cursor.fetchone()[0]
        
        # Critical items
        cursor.execute("""
            SELECT COUNT(*) FROM content_items 
            WHERE is_english = 1 AND priority_level = 'critical'
        """)
        critical_items = cursor.fetchone()[0]
        
        # High priority items
        cursor.execute("""
            SELECT COUNT(*) FROM content_items 
            WHERE is_english = 1 AND priority_level = 'high'
        """)
        high_priority_items = cursor.fetchone()[0]
        
        # Sources count
        cursor.execute("SELECT COUNT(DISTINCT source_id) FROM content_items")
        sources_count = cursor.fetchone()[0]
        
        # Last update time
        cursor.execute("SELECT MAX(collected_date) FROM content_items")
        last_update = cursor.fetchone()[0]
        
        return Stats(
            total_items=total_items,
            critical_items=critical_items,
            high_priority_items=high_priority_items,
            last_update=last_update,
            sources_count=sources_count
        )

@app.get("/api/content", response_model=List[ContentItemResponse])
async def get_content(
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
            SELECT 
                c.item_id,
                c.source_id,
                c.title,
                c.content,
                c.url,
                c.published_date,
                c.priority_level,
                c.priority_score,
                c.topics
            FROM content_items c
            WHERE c.is_english = 1
        """
        params = []
        
        # Add priority filter
        if priority:
            query += " AND c.priority_level = ?"
            params.append(priority)
        
        # Add search filter
        if search:
            query += " AND (c.title LIKE ? OR c.content LIKE ?)"
            params.extend([f'%{search}%', f'%{search}%'])
        
        # Order and limit
        query += " ORDER BY c.priority_score DESC, c.collected_date DESC LIMIT ? OFFSET ?"
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
            
            items.append(ContentItemResponse(
                item_id=item_id,
                source_id=row['source_id'],
                title=row['title'],
                content=row['content'],
                url=row['url'],
                published_date=row['published_date'],
                priority=row['priority_level'],
                priority_score=row['priority_score'],
                topics=row['topics'].split(',') if row['topics'] else [],
                is_bookmarked=is_bookmarked,
                is_read=is_read
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

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the dashboard HTML"""
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
            padding: 20px 30px;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        .header h1 {
            font-size: 28px;
            font-weight: 600;
            color: #1d1d1f;
        }
        .controls {
            background: white;
            padding: 20px 30px;
            border-bottom: 1px solid #d2d2d7;
            display: flex;
            gap: 20px;
            align-items: center;
            flex-wrap: wrap;
        }
        .search-box {
            flex: 1;
            max-width: 400px;
        }
        .search-box input {
            width: 100%;
            padding: 10px 15px;
            border: 1px solid #d2d2d7;
            border-radius: 8px;
            font-size: 14px;
        }
        .priority-filter {
            display: flex;
            gap: 10px;
        }
        .filter-btn {
            padding: 8px 16px;
            border: 1px solid #d2d2d7;
            background: white;
            border-radius: 8px;
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
            font-size: 32px;
            font-weight: 600;
            color: #007AFF;
        }
        .stat-label {
            font-size: 12px;
            color: #86868b;
            text-transform: uppercase;
            margin-top: 5px;
        }
        .content-area {
            padding: 30px;
            max-width: 1400px;
            margin: 0 auto;
        }
        .content-item {
            background: white;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            transition: all 0.2s;
        }
        .content-item:hover {
            box-shadow: 0 6px 20px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }
        .content-header {
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 12px;
        }
        .content-title {
            font-size: 18px;
            font-weight: 600;
            color: #1d1d1f;
            text-decoration: none;
            flex: 1;
            line-height: 1.4;
        }
        .content-title:hover {
            color: #007AFF;
        }
        .priority-badge {
            padding: 4px 12px;
            border-radius: 8px;
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
            gap: 20px;
            font-size: 13px;
            color: #86868b;
            margin-bottom: 12px;
        }
        .content-snippet {
            color: #424245;
            line-height: 1.6;
            font-size: 15px;
        }
        .bookmark-btn {
            background: none;
            border: none;
            cursor: pointer;
            font-size: 18px;
            padding: 6px;
            margin-left: 12px;
        }
        .bookmark-btn.bookmarked {
            color: #FF9500;
        }
        .loading {
            text-align: center;
            padding: 60px;
            color: #86868b;
            font-size: 16px;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Universal Topic Intelligence</h1>
    </div>
    
    <div class="controls">
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
            <div class="stat-label">Sources</div>
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
    
    <div class="content-area" id="contentArea">
        <div class="loading">Loading content...</div>
    </div>
    
    <script>
        let currentPriority = 'all';
        let currentSearch = '';
        
        async function loadStats() {
            const response = await fetch('/api/stats');
            const stats = await response.json();
            
            const statsBar = document.getElementById('statsBar');
            statsBar.innerHTML = `
                <div class="stat-item">
                    <div class="stat-number">${stats.total_items}</div>
                    <div class="stat-label">Total Items</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">${stats.sources_count}</div>
                    <div class="stat-label">Sources</div>
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
        }
        
        async function loadContent() {
            const params = new URLSearchParams();
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
                        </a>
                        <div style="display: flex; align-items: center;">
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
                        <span>📊 Score: ${(item.priority_score * 100).toFixed(0)}%</span>
                    </div>
                    ${item.content ? `
                        <div class="content-snippet">
                            ${item.content.substring(0, 300)}...
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
        loadStats();
        loadContent();
        
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

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Universal Topic Intelligence Dashboard")
    print("📍 Open your browser to: http://localhost:8080")
    
    uvicorn.run(app, host="0.0.0.0", port=8080)