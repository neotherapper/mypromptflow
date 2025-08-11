#!/usr/bin/env python3
"""
Fixed Universal Topic Intelligence System Dashboard
- Uses correct database
- Smart priority scoring for Claude content
- Simplified to work reliably
"""

import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional
from contextlib import contextmanager

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from enum import Enum

# Initialize FastAPI app
app = FastAPI(
    title="Universal Topic Intelligence System",
    description="Intelligent monitoring with smart Claude prioritization",
    version="4.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Use the correct database path
DB_PATH = Path("topic_intelligence.db")
USER_DB_PATH = Path("storage/user_data.db")

def init_user_database():
    """Initialize user data database for bookmarks, read status, etc."""
    with sqlite3.connect(USER_DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS bookmarks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id TEXT NOT NULL UNIQUE,
                saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                notes TEXT,
                tags TEXT
            )
        ''')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS read_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id TEXT NOT NULL UNIQUE,
                read_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

# Initialize user database on startup
USER_DB_PATH.parent.mkdir(exist_ok=True)
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

@contextmanager
def get_user_db():
    """User database connection context manager"""
    conn = sqlite3.connect(USER_DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# Smart priority recalculation for Claude content
def recalculate_priority(item: Dict[str, Any]) -> str:
    """
    Recalculate priority with smart logic for Claude content
    """
    title = item.get('title', '').lower()
    content = item.get('content', '').lower()
    topics = item.get('topics', [])
    if isinstance(topics, str):
        try:
            topics = json.loads(topics)
        except:
            topics = []
    
    # Check for Claude-related content
    is_claude_related = any([
        'claude' in title,
        'anthropic' in title,
        'claude' in content[:500] if content else False,
        'claude' in topics,
        'claude-ai' in topics
    ])
    
    # Check for major announcements
    major_keywords = ['release', 'launch', 'new', 'update', 'opus', 'sonnet', 'haiku', 
                      'available', 'here', 'announced', 'introducing']
    has_major_announcement = any(keyword in title for keyword in major_keywords)
    
    # Smart priority logic
    if is_claude_related:
        if has_major_announcement:
            return "critical"  # Major Claude announcements are critical
        elif 'opus' in title or '4.1' in title or '4.0' in title:
            return "critical"  # Opus models are critical
        else:
            return "high"  # Other Claude content is high priority
    
    # Check for other important topics
    if 'react' in topics or 'typescript' in topics:
        if has_major_announcement:
            return "high"
        else:
            return "medium"
    
    # Default to original priority or medium
    original = item.get('priority_level', 'medium')
    if original == 'low' and any(keyword in title for keyword in ['important', 'breaking', 'major']):
        return "medium"
    
    return original

def estimate_reading_time(content: str, title: str = "") -> int:
    """Estimate reading time in minutes"""
    if not content:
        return 1
    
    text = f"{title} {content}"
    word_count = len(text.split())
    minutes = max(1, round(word_count / 225))
    return minutes

# Pydantic models
class Stats(BaseModel):
    total_items: int
    unread_count: int
    saved_for_later: int
    critical_items: int
    high_priority_items: int
    last_24_hours: int
    trending_topics: List[Dict[str, Any]]

class ContentItemResponse(BaseModel):
    item_id: str
    source_id: str
    title: str
    content: Optional[str]
    url: Optional[str]
    published_date: str
    author: Optional[str]
    topics: List[str]
    priority: str  # Recalculated smart priority
    original_priority: str  # Original priority from database
    is_bookmarked: bool = False
    is_read: bool = False
    reading_time: int = 0
    metadata: Dict[str, Any] = Field(default_factory=dict)

class BookmarkRequest(BaseModel):
    item_id: str
    notes: Optional[str] = None

class ReadStatusRequest(BaseModel):
    item_id: str
    is_read: bool

# API endpoints
@app.get("/api/stats", response_model=Stats)
async def get_stats():
    """Get dashboard statistics"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Total items
        cursor.execute("SELECT COUNT(*) FROM content_items WHERE is_english = 1")
        total_items = cursor.fetchone()[0]
        
        # Get all items for smart priority recalculation
        cursor.execute("""
            SELECT item_id, title, content, topics, priority_level 
            FROM content_items WHERE is_english = 1
        """)
        all_items = [dict(row) for row in cursor.fetchall()]
        
        # Recalculate priorities
        critical_count = 0
        high_count = 0
        for item in all_items:
            smart_priority = recalculate_priority(item)
            if smart_priority == "critical":
                critical_count += 1
            elif smart_priority == "high":
                high_count += 1
        
        # Unread count
        with get_user_db() as user_conn:
            user_cursor = user_conn.cursor()
            user_cursor.execute("SELECT COUNT(*) FROM read_items")
            read_count = user_cursor.fetchone()[0]
            
            # Saved for later
            user_cursor.execute("SELECT COUNT(*) FROM bookmarks")
            saved_count = user_cursor.fetchone()[0]
        
        unread_count = total_items - read_count
        
        # Last 24 hours
        yesterday = (datetime.now() - timedelta(days=1)).isoformat()
        cursor.execute("""
            SELECT COUNT(*) FROM content_items 
            WHERE datetime(collected_date) > datetime(?)
            AND is_english = 1
        """, (yesterday,))
        last_24_hours = cursor.fetchone()[0]
        
        # Trending topics
        cursor.execute("""
            SELECT topics, COUNT(*) as count 
            FROM content_items 
            WHERE datetime(collected_date) > datetime(?)
            AND is_english = 1
            GROUP BY topics
            ORDER BY count DESC
            LIMIT 5
        """, (yesterday,))
        
        trending = []
        for row in cursor.fetchall():
            if row['topics']:
                try:
                    topics = json.loads(row['topics']) if isinstance(row['topics'], str) else row['topics']
                    for topic in topics[:1]:
                        trending.append({"name": topic, "count": row['count']})
                except:
                    pass
        
        return Stats(
            total_items=total_items,
            unread_count=unread_count,
            saved_for_later=saved_count,
            critical_items=critical_count,
            high_priority_items=high_count,
            last_24_hours=last_24_hours,
            trending_topics=trending[:5]
        )

@app.get("/api/items")
async def get_items(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    topic: Optional[str] = None,
    priority: Optional[str] = None,
    unread_only: bool = False,
    bookmarked_only: bool = False
):
    """Get content items with smart priority recalculation"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Build query
        query = "SELECT * FROM content_items WHERE is_english = 1"
        params = []
        
        if topic:
            query += " AND topics LIKE ?"
            params.append(f"%{topic}%")
        
        # Get read and bookmarked items
        with get_user_db() as user_conn:
            user_cursor = user_conn.cursor()
            
            if unread_only:
                user_cursor.execute("SELECT item_id FROM read_items")
                read_ids = [row[0] for row in user_cursor.fetchall()]
                if read_ids:
                    placeholders = ','.join('?' * len(read_ids))
                    query += f" AND item_id NOT IN ({placeholders})"
                    params.extend(read_ids)
            
            if bookmarked_only:
                user_cursor.execute("SELECT item_id FROM bookmarks")
                bookmark_ids = [row[0] for row in user_cursor.fetchall()]
                if bookmark_ids:
                    placeholders = ','.join('?' * len(bookmark_ids))
                    query += f" AND item_id IN ({placeholders})"
                    params.extend(bookmark_ids)
                else:
                    return {"items": [], "total": 0, "page": page, "per_page": per_page}
            
            # Get all bookmarks and read items
            user_cursor.execute("SELECT item_id FROM bookmarks")
            all_bookmarks = set(row[0] for row in user_cursor.fetchall())
            
            user_cursor.execute("SELECT item_id FROM read_items")
            all_read = set(row[0] for row in user_cursor.fetchall())
        
        # Order by date
        query += " ORDER BY collected_date DESC"
        
        # Get all matching items first for filtering by smart priority
        cursor.execute(query, params)
        all_results = []
        
        for row in cursor.fetchall():
            item_dict = dict(row)
            
            # Parse JSON fields
            if item_dict.get('topics'):
                try:
                    item_dict['topics'] = json.loads(item_dict['topics']) if isinstance(item_dict['topics'], str) else item_dict['topics']
                except:
                    item_dict['topics'] = []
            else:
                item_dict['topics'] = []
            
            if item_dict.get('metadata'):
                try:
                    item_dict['metadata'] = json.loads(item_dict['metadata']) if isinstance(item_dict['metadata'], str) else item_dict['metadata']
                except:
                    item_dict['metadata'] = {}
            else:
                item_dict['metadata'] = {}
            
            # Recalculate priority
            smart_priority = recalculate_priority(item_dict)
            item_dict['original_priority'] = item_dict.get('priority_level', 'medium')
            item_dict['priority'] = smart_priority
            
            # Filter by recalculated priority if specified
            if priority and smart_priority != priority:
                continue
            
            # Add user status
            item_dict['is_bookmarked'] = item_dict['item_id'] in all_bookmarks
            item_dict['is_read'] = item_dict['item_id'] in all_read
            
            # Add reading time
            item_dict['reading_time'] = estimate_reading_time(
                item_dict.get('content', ''),
                item_dict.get('title', '')
            )
            
            all_results.append(item_dict)
        
        # Sort by priority (critical first) then by date
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        all_results.sort(key=lambda x: (priority_order.get(x['priority'], 4), x.get('collected_date', '')), reverse=False)
        
        # Paginate
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_results = all_results[start_idx:end_idx]
        
        # Convert to response model
        items = []
        for item_dict in paginated_results:
            # Ensure required fields
            item_dict['published_date'] = item_dict.get('published_date', item_dict.get('collected_date', ''))
            items.append(ContentItemResponse(**item_dict))
        
        return {
            "items": items,
            "total": len(all_results),
            "page": page,
            "per_page": per_page
        }

@app.post("/api/bookmark")
async def toggle_bookmark(request: BookmarkRequest):
    """Toggle bookmark status"""
    with get_user_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT id FROM bookmarks WHERE item_id = ?", (request.item_id,))
        existing = cursor.fetchone()
        
        if existing:
            cursor.execute("DELETE FROM bookmarks WHERE item_id = ?", (request.item_id,))
            conn.commit()
            return {"status": "removed", "item_id": request.item_id}
        else:
            cursor.execute(
                "INSERT INTO bookmarks (item_id, notes) VALUES (?, ?)",
                (request.item_id, request.notes)
            )
            conn.commit()
            return {"status": "added", "item_id": request.item_id}

@app.post("/api/read-status")
async def update_read_status(request: ReadStatusRequest):
    """Update read status"""
    with get_user_db() as conn:
        cursor = conn.cursor()
        
        if request.is_read:
            cursor.execute(
                "INSERT OR IGNORE INTO read_items (item_id) VALUES (?)",
                (request.item_id,)
            )
        else:
            cursor.execute("DELETE FROM read_items WHERE item_id = ?", (request.item_id,))
        
        conn.commit()
        return {"status": "updated", "item_id": request.item_id, "is_read": request.is_read}

@app.get("/api/topics")
async def get_topics():
    """Get all available topics"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT topics FROM content_items 
            WHERE is_english = 1 AND topics IS NOT NULL
        """)
        
        all_topics = set()
        for row in cursor.fetchall():
            if row['topics']:
                try:
                    topics = json.loads(row['topics']) if isinstance(row['topics'], str) else row['topics']
                    all_topics.update(topics)
                except:
                    pass
        
        return {"topics": sorted(list(all_topics))}

@app.get("/")
async def root():
    """Serve the dashboard HTML"""
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Universal Topic Intelligence System</title>
    <style>
        :root {
            --primary-600: #5145e0;
            --primary-700: #4339c9;
            --success-500: #10b981;
            --warning-500: #f59e0b;
            --danger-500: #ef4444;
            --gray-50: #f9fafb;
            --gray-100: #f3f4f6;
            --gray-200: #e5e7eb;
            --gray-300: #d1d5db;
            --gray-500: #6b7280;
            --gray-600: #4b5563;
            --gray-700: #374151;
            --gray-900: #111827;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--gray-50);
            color: var(--gray-900);
            line-height: 1.5;
        }

        .header {
            background: white;
            border-bottom: 1px solid var(--gray-200);
            padding: 1rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }

        .header-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--gray-900);
        }

        .main-content {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        .stat-card {
            background: white;
            border-radius: 0.5rem;
            padding: 1.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }

        .stat-label {
            font-size: 0.875rem;
            color: var(--gray-600);
            margin-bottom: 0.5rem;
        }

        .stat-value {
            font-size: 2rem;
            font-weight: 700;
            color: var(--gray-900);
        }

        .stat-badge {
            display: inline-block;
            font-size: 0.75rem;
            padding: 0.25rem 0.5rem;
            border-radius: 0.25rem;
            margin-left: 0.5rem;
            font-weight: 500;
        }

        .badge-critical {
            background: rgba(239, 68, 68, 0.1);
            color: var(--danger-500);
        }

        .badge-high {
            background: rgba(245, 158, 11, 0.1);
            color: var(--warning-500);
        }

        .filter-bar {
            background: white;
            border-radius: 0.5rem;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
        }

        .filter-select {
            padding: 0.5rem 1rem;
            border: 1px solid var(--gray-300);
            border-radius: 0.375rem;
            background: white;
            font-size: 0.875rem;
        }

        .filter-checkbox {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .content-section {
            background: white;
            border-radius: 0.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }

        .content-header {
            padding: 1.5rem;
            border-bottom: 1px solid var(--gray-200);
        }

        .content-list {
            padding: 1.5rem;
        }

        .content-item {
            padding: 1.5rem;
            border: 1px solid var(--gray-200);
            border-radius: 0.5rem;
            margin-bottom: 1rem;
            transition: all 0.2s;
        }

        .content-item:hover {
            border-color: var(--gray-300);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        .content-item.is-read {
            opacity: 0.7;
            background: var(--gray-50);
        }

        .content-item.is-bookmarked {
            border-left: 4px solid var(--primary-600);
        }

        .content-header-row {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 0.75rem;
        }

        .content-title-link {
            font-size: 1.125rem;
            font-weight: 600;
            color: var(--gray-900);
            text-decoration: none;
            flex: 1;
        }

        .content-title-link:hover {
            color: var(--primary-600);
        }

        .content-actions-row {
            display: flex;
            gap: 0.5rem;
        }

        .action-btn {
            padding: 0.25rem 0.5rem;
            border: 1px solid var(--gray-300);
            border-radius: 0.25rem;
            background: white;
            cursor: pointer;
            font-size: 0.875rem;
            transition: all 0.2s;
        }

        .action-btn:hover {
            background: var(--gray-50);
        }

        .action-btn.active {
            background: var(--primary-600);
            color: white;
            border-color: var(--primary-600);
        }

        .content-meta {
            display: flex;
            gap: 1rem;
            margin-bottom: 0.75rem;
            font-size: 0.875rem;
            color: var(--gray-600);
        }

        .content-description {
            color: var(--gray-700);
            line-height: 1.6;
            margin-bottom: 1rem;
        }

        .content-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .topic-tags {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }

        .topic-tag {
            padding: 0.25rem 0.5rem;
            background: var(--gray-100);
            color: var(--gray-700);
            border-radius: 0.25rem;
            font-size: 0.75rem;
        }

        .priority-badge {
            padding: 0.25rem 0.5rem;
            border-radius: 0.25rem;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }

        .priority-critical {
            background: rgba(239, 68, 68, 0.1);
            color: var(--danger-500);
        }

        .priority-high {
            background: rgba(245, 158, 11, 0.1);
            color: var(--warning-500);
        }

        .priority-medium {
            background: rgba(59, 130, 246, 0.1);
            color: #3b82f6;
        }

        .priority-low {
            background: var(--gray-100);
            color: var(--gray-600);
        }

        .btn {
            padding: 0.5rem 1rem;
            border: none;
            border-radius: 0.375rem;
            font-size: 0.875rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
        }

        .btn-primary {
            background: var(--primary-600);
            color: white;
        }

        .btn-primary:hover {
            background: var(--primary-700);
        }

        .loading {
            text-align: center;
            padding: 3rem;
            color: var(--gray-500);
        }

        .empty-state {
            text-align: center;
            padding: 3rem;
            color: var(--gray-500);
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="header-title">
            🧠 Universal Topic Intelligence System
        </div>
        <button class="btn btn-primary" onclick="refreshData()">
            🔄 Refresh
        </button>
    </header>

    <main class="main-content">
        <div class="stats-grid" id="statsGrid">
            <div class="stat-card">
                <div class="stat-label">Critical Priority</div>
                <div class="stat-value">
                    <span id="criticalCount">-</span>
                    <span class="stat-badge badge-critical">URGENT</span>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-label">High Priority</div>
                <div class="stat-value">
                    <span id="highCount">-</span>
                    <span class="stat-badge badge-high">Important</span>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Unread Items</div>
                <div class="stat-value">
                    <span id="unreadCount">-</span>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Saved for Later</div>
                <div class="stat-value">
                    <span id="savedCount">-</span>
                </div>
            </div>
        </div>

        <div class="filter-bar">
            <select class="filter-select" id="topicFilter">
                <option value="">All Topics</option>
            </select>
            <select class="filter-select" id="priorityFilter">
                <option value="">All Priorities</option>
                <option value="critical">Critical</option>
                <option value="high">High</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
            </select>
            <label class="filter-checkbox">
                <input type="checkbox" id="unreadOnly">
                Unread Only
            </label>
            <label class="filter-checkbox">
                <input type="checkbox" id="bookmarkedOnly">
                Bookmarked Only
            </label>
        </div>

        <div class="content-section">
            <div class="content-header">
                <h2>Intelligence Feed</h2>
            </div>
            <div class="content-list" id="contentList">
                <div class="loading">Loading...</div>
            </div>
        </div>
    </main>

    <script>
        const API_BASE = '';
        let currentPage = 1;
        let currentFilters = {};

        document.addEventListener('DOMContentLoaded', () => {
            loadStats();
            loadTopics();
            loadContent();
            setupEventListeners();
        });

        function setupEventListeners() {
            document.getElementById('topicFilter').addEventListener('change', (e) => {
                currentFilters.topic = e.target.value;
                loadContent();
            });

            document.getElementById('priorityFilter').addEventListener('change', (e) => {
                currentFilters.priority = e.target.value;
                loadContent();
            });

            document.getElementById('unreadOnly').addEventListener('change', (e) => {
                currentFilters.unreadOnly = e.target.checked;
                loadContent();
            });

            document.getElementById('bookmarkedOnly').addEventListener('change', (e) => {
                currentFilters.bookmarkedOnly = e.target.checked;
                loadContent();
            });
        }

        async function loadStats() {
            try {
                const response = await fetch(`${API_BASE}/api/stats`);
                const stats = await response.json();

                document.getElementById('criticalCount').textContent = stats.critical_items;
                document.getElementById('highCount').textContent = stats.high_priority_items;
                document.getElementById('unreadCount').textContent = stats.unread_count;
                document.getElementById('savedCount').textContent = stats.saved_for_later;

            } catch (error) {
                console.error('Error loading stats:', error);
            }
        }

        async function loadTopics() {
            try {
                const response = await fetch(`${API_BASE}/api/topics`);
                const data = await response.json();

                const topicFilter = document.getElementById('topicFilter');
                topicFilter.innerHTML = '<option value="">All Topics</option>';
                
                // Prioritize Claude-related topics
                const claudeTopics = data.topics.filter(t => t.includes('claude'));
                const otherTopics = data.topics.filter(t => !t.includes('claude'));
                
                [...claudeTopics, ...otherTopics].forEach(topic => {
                    const option = document.createElement('option');
                    option.value = topic;
                    option.textContent = topic.replace(/-/g, ' ').replace(/\\b\\w/g, l => l.toUpperCase());
                    topicFilter.appendChild(option);
                });

            } catch (error) {
                console.error('Error loading topics:', error);
            }
        }

        async function loadContent() {
            const contentList = document.getElementById('contentList');
            contentList.innerHTML = '<div class="loading">Loading...</div>';

            try {
                const params = new URLSearchParams({
                    page: currentPage,
                    per_page: 20,
                    topic: currentFilters.topic || '',
                    priority: currentFilters.priority || '',
                    unread_only: currentFilters.unreadOnly || false,
                    bookmarked_only: currentFilters.bookmarkedOnly || false
                });

                const response = await fetch(`${API_BASE}/api/items?${params}`);
                const data = await response.json();

                if (data.items.length === 0) {
                    contentList.innerHTML = `
                        <div class="empty-state">
                            <h3>No items found</h3>
                            <p>Try adjusting your filters</p>
                        </div>
                    `;
                    return;
                }

                contentList.innerHTML = '';
                data.items.forEach(item => {
                    const itemEl = createContentItem(item);
                    contentList.appendChild(itemEl);
                });

            } catch (error) {
                console.error('Error loading content:', error);
                contentList.innerHTML = `
                    <div class="empty-state">
                        <h3>Error loading content</h3>
                        <p>${error.message}</p>
                    </div>
                `;
            }
        }

        function createContentItem(item) {
            const div = document.createElement('div');
            div.className = `content-item ${item.is_read ? 'is-read' : ''} ${item.is_bookmarked ? 'is-bookmarked' : ''}`;
            div.dataset.itemId = item.item_id;

            const publishedDate = new Date(item.published_date).toLocaleDateString();
            
            // Show if priority was upgraded
            const priorityInfo = item.priority !== item.original_priority ? 
                ` (was: ${item.original_priority})` : '';
            
            div.innerHTML = `
                <div class="content-header-row">
                    <a href="${item.url}" target="_blank" class="content-title-link">
                        ${item.title}
                    </a>
                    <div class="content-actions-row">
                        <button class="action-btn ${item.is_bookmarked ? 'active' : ''}" 
                                onclick="toggleBookmark('${item.item_id}')" 
                                title="Save for later">
                            ${item.is_bookmarked ? '★' : '☆'}
                        </button>
                        <button class="action-btn ${item.is_read ? 'active' : ''}" 
                                onclick="toggleRead('${item.item_id}', ${!item.is_read})" 
                                title="Mark as ${item.is_read ? 'unread' : 'read'}">
                            ${item.is_read ? '✓' : '○'}
                        </button>
                    </div>
                </div>
                <div class="content-meta">
                    <span>📅 ${publishedDate}</span>
                    ${item.author ? `<span>✍️ ${item.author}</span>` : ''}
                    <span>📖 ${item.reading_time} min read</span>
                </div>
                <div class="content-description">
                    ${item.content ? item.content.substring(0, 300) + '...' : ''}
                </div>
                <div class="content-footer">
                    <div class="topic-tags">
                        ${item.topics.map(topic => 
                            `<span class="topic-tag">${topic}</span>`
                        ).join('')}
                    </div>
                    <span class="priority-badge priority-${item.priority}">
                        ${item.priority}${priorityInfo}
                    </span>
                </div>
            `;

            return div;
        }

        async function toggleBookmark(itemId) {
            try {
                const response = await fetch(`${API_BASE}/api/bookmark`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ item_id: itemId })
                });
                
                const result = await response.json();
                
                const item = document.querySelector(`[data-item-id="${itemId}"]`);
                if (item) {
                    const btn = item.querySelector('.action-btn');
                    if (result.status === 'added') {
                        item.classList.add('is-bookmarked');
                        btn.classList.add('active');
                        btn.textContent = '★';
                    } else {
                        item.classList.remove('is-bookmarked');
                        btn.classList.remove('active');
                        btn.textContent = '☆';
                    }
                }
                
                loadStats();
                
            } catch (error) {
                console.error('Error toggling bookmark:', error);
            }
        }

        async function toggleRead(itemId, isRead) {
            try {
                const response = await fetch(`${API_BASE}/api/read-status`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ item_id: itemId, is_read: isRead })
                });
                
                const result = await response.json();
                
                const item = document.querySelector(`[data-item-id="${itemId}"]`);
                if (item) {
                    const btn = item.querySelectorAll('.action-btn')[1];
                    if (isRead) {
                        item.classList.add('is-read');
                        btn.classList.add('active');
                        btn.textContent = '✓';
                        btn.setAttribute('onclick', `toggleRead('${itemId}', false)`);
                    } else {
                        item.classList.remove('is-read');
                        btn.classList.remove('active');
                        btn.textContent = '○';
                        btn.setAttribute('onclick', `toggleRead('${itemId}', true)`);
                    }
                }
                
                loadStats();
                
            } catch (error) {
                console.error('Error toggling read status:', error);
            }
        }

        function refreshData() {
            loadStats();
            loadContent();
        }
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Universal Topic Intelligence System Dashboard (Fixed)")
    print("✨ Smart Claude Priority Detection Active")
    print("📍 Open your browser to: http://localhost:5001")
    print("Press Ctrl+C to stop the server\n")
    
    uvicorn.run(app, host="0.0.0.0", port=5001)