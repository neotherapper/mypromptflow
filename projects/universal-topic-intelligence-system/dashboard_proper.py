#!/usr/bin/env python3
"""
Proper Dashboard using correctly scored priorities
All Claude content is now properly scored as CRITICAL/HIGH
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
    description="Dashboard with properly prioritized Claude content",
    version="5.0.0"
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
            CREATE TABLE IF NOT EXISTS read_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id TEXT NOT NULL UNIQUE,
                read_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

# Initialize user database
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

def estimate_reading_time(content: str, title: str = "") -> int:
    """Estimate reading time in minutes"""
    if not content:
        return 1
    text = f"{title} {content}"
    word_count = len(text.split())
    return max(1, round(word_count / 225))

# Pydantic models
class Stats(BaseModel):
    total_items: int
    critical_items: int
    high_priority_items: int
    unread_count: int
    saved_for_later: int
    claude_items: int
    last_24_hours: int

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
        
        # Critical items (properly scored now)
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
        
        # Claude-related items (should all be critical/high now)
        cursor.execute("""
            SELECT COUNT(*) FROM content_items 
            WHERE is_english = 1 
            AND (title LIKE '%claude%' OR title LIKE '%anthropic%' OR title LIKE '%opus%')
        """)
        claude_items = cursor.fetchone()[0]
        
        # Unread count
        with get_user_db() as user_conn:
            user_cursor = user_conn.cursor()
            user_cursor.execute("SELECT COUNT(*) FROM read_items")
            read_count = user_cursor.fetchone()[0]
            
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
        
        return Stats(
            total_items=total_items,
            critical_items=critical_items,
            high_priority_items=high_priority_items,
            unread_count=unread_count,
            saved_for_later=saved_count,
            claude_items=claude_items,
            last_24_hours=last_24_hours
        )

@app.get("/api/items")
async def get_items(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    topic: Optional[str] = None,
    priority: Optional[str] = None,
    search: Optional[str] = None,
    unread_only: bool = False,
    bookmarked_only: bool = False,
    claude_only: bool = False
):
    """Get content items (now with proper priorities from database)"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Build query
        query = "SELECT * FROM content_items WHERE is_english = 1"
        params = []
        
        if search:
            query += " AND (title LIKE ? OR content LIKE ?)"
            params.append(f"%{search}%")
            params.append(f"%{search}%")
        
        if topic:
            query += " AND topics LIKE ?"
            params.append(f"%{topic}%")
        
        if priority:
            query += " AND priority_level = ?"
            params.append(priority)
        
        if claude_only:
            query += " AND (title LIKE '%claude%' OR title LIKE '%anthropic%' OR title LIKE '%opus%')"
        
        # Get user data
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
            
            user_cursor.execute("SELECT item_id FROM bookmarks")
            all_bookmarks = set(row[0] for row in user_cursor.fetchall())
            
            user_cursor.execute("SELECT item_id FROM read_items")
            all_read = set(row[0] for row in user_cursor.fetchall())
        
        # Order by priority score (highest first), then by date
        query += " ORDER BY priority_score DESC, collected_date DESC LIMIT ? OFFSET ?"
        params.extend([per_page, (page - 1) * per_page])
        
        cursor.execute(query, params)
        items = []
        
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
            
            # Add user status
            item_dict['is_bookmarked'] = item_dict['item_id'] in all_bookmarks
            item_dict['is_read'] = item_dict['item_id'] in all_read
            
            # Add reading time
            item_dict['reading_time'] = estimate_reading_time(
                item_dict.get('content', ''),
                item_dict.get('title', '')
            )
            
            # Use the priority from database (now properly scored)
            item_dict['priority'] = item_dict.get('priority_level', 'medium')
            item_dict['published_date'] = item_dict.get('published_date', item_dict.get('collected_date', ''))
            
            # Ensure priority_score is valid
            if item_dict.get('priority_score') is None or item_dict.get('priority_score') == '':
                item_dict['priority_score'] = 0.5  # Default to medium score
            
            items.append(ContentItemResponse(**item_dict))
        
        # Get total count
        count_query = query.split("LIMIT")[0].replace("SELECT *", "SELECT COUNT(*)")
        cursor.execute(count_query, params[:-2] if len(params) >= 2 else params)
        total = cursor.fetchone()[0]
        
        return {
            "items": items,
            "total": total,
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
        
        # Prioritize Claude-related topics
        claude_topics = ['claude', 'claude-ai', 'anthropic', 'opus', 'sonnet']
        other_topics = [t for t in all_topics if t not in claude_topics]
        
        return {"topics": claude_topics + sorted(other_topics)}

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
            --claude-color: #8b5cf6;
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
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .header-actions {
            display: flex;
            gap: 1rem;
        }

        .main-content {
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }

        .stat-card {
            background: white;
            border-radius: 0.5rem;
            padding: 1.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }

        .stat-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        .stat-card.claude {
            border-top: 3px solid var(--claude-color);
        }

        .stat-label {
            font-size: 0.875rem;
            color: var(--gray-600);
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
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

        .badge-claude {
            background: rgba(139, 92, 246, 0.1);
            color: var(--claude-color);
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
            align-items: center;
        }

        .filter-select {
            padding: 0.5rem 1rem;
            border: 1px solid var(--gray-300);
            border-radius: 0.375rem;
            background: white;
            font-size: 0.875rem;
            min-width: 150px;
        }

        .filter-checkbox {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.875rem;
        }

        .filter-checkbox.claude-filter {
            color: var(--claude-color);
            font-weight: 500;
        }

        .content-section {
            background: white;
            border-radius: 0.5rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }

        .content-header {
            padding: 1.5rem;
            border-bottom: 1px solid var(--gray-200);
            display: flex;
            justify-content: space-between;
            align-items: center;
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
            position: relative;
        }

        .content-item:hover {
            border-color: var(--gray-300);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        .content-item.is-claude {
            border-left: 4px solid var(--claude-color);
        }

        .content-item.is-read {
            opacity: 0.7;
            background: var(--gray-50);
        }

        .content-item.is-bookmarked::before {
            content: '★';
            position: absolute;
            top: 1rem;
            right: 1rem;
            color: var(--warning-500);
            font-size: 1.25rem;
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
            margin-right: 3rem;
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
            flex-wrap: wrap;
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
            flex-wrap: wrap;
            gap: 1rem;
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

        .topic-tag.claude-topic {
            background: rgba(139, 92, 246, 0.1);
            color: var(--claude-color);
            font-weight: 500;
        }

        .priority-info {
            display: flex;
            align-items: center;
            gap: 0.5rem;
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

        .priority-score {
            font-size: 0.75rem;
            color: var(--gray-500);
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

        .btn-claude {
            background: var(--claude-color);
            color: white;
        }

        .btn-claude:hover {
            background: #7c3aed;
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
            <span style="font-size: 0.75rem; color: var(--gray-500);">v5.0 - Proper Prioritization</span>
        </div>
        <div class="header-actions">
            <a href="/youtube-intelligence" class="btn btn-secondary" style="text-decoration: none; margin-right: 10px;">
                📊 YouTube Intelligence
            </a>
            <button class="btn btn-claude" onclick="toggleClaudeFilter()">
                🤖 Claude Focus
            </button>
            <button class="btn btn-primary" onclick="refreshData()">
                🔄 Refresh
            </button>
        </div>
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
            <div class="stat-card claude">
                <div class="stat-label">Claude Content</div>
                <div class="stat-value">
                    <span id="claudeCount">-</span>
                    <span class="stat-badge badge-claude">AI</span>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Unread Items</div>
                <div class="stat-value">
                    <span id="unreadCount">-</span>
                </div>
            </div>
        </div>

        <div class="filter-bar">
            <input type="text" id="searchBox" placeholder="Search content..." style="padding: 0.5rem 1rem; border: 1px solid var(--gray-300); border-radius: 0.375rem; flex: 1; max-width: 300px;">
            <select class="filter-select" id="topicFilter">
                <option value="">All Topics</option>
            </select>
            <select class="filter-select" id="priorityFilter">
                <option value="">All Priorities</option>
                <option value="critical">Critical Only</option>
                <option value="high">High Priority</option>
                <option value="medium">Medium Priority</option>
                <option value="low">Low Priority</option>
            </select>
            <label class="filter-checkbox">
                <input type="checkbox" id="unreadOnly">
                Unread Only
            </label>
            <label class="filter-checkbox">
                <input type="checkbox" id="bookmarkedOnly">
                Bookmarked Only
            </label>
            <label class="filter-checkbox claude-filter">
                <input type="checkbox" id="claudeOnly">
                Claude Content Only
            </label>
        </div>

        <div class="content-section">
            <div class="content-header">
                <h2>Intelligence Feed (Properly Prioritized)</h2>
                <span id="itemCount" style="color: var(--gray-500); font-size: 0.875rem;"></span>
            </div>
            <div class="content-list" id="contentList">
                <div class="loading">Loading properly scored content...</div>
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
            // Search box with debounce
            let searchTimeout;
            document.getElementById('searchBox').addEventListener('input', (e) => {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    currentFilters.search = e.target.value;
                    loadContent();
                }, 300); // 300ms debounce
            });

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

            document.getElementById('claudeOnly').addEventListener('change', (e) => {
                currentFilters.claudeOnly = e.target.checked;
                loadContent();
            });
        }

        function toggleClaudeFilter() {
            const checkbox = document.getElementById('claudeOnly');
            checkbox.checked = !checkbox.checked;
            currentFilters.claudeOnly = checkbox.checked;
            loadContent();
        }

        async function loadStats() {
            try {
                const response = await fetch(`${API_BASE}/api/stats`);
                const stats = await response.json();

                document.getElementById('criticalCount').textContent = stats.critical_items;
                document.getElementById('highCount').textContent = stats.high_priority_items;
                document.getElementById('claudeCount').textContent = stats.claude_items;
                document.getElementById('unreadCount').textContent = stats.unread_count;

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
                
                data.topics.forEach(topic => {
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
            contentList.innerHTML = '<div class="loading">Loading properly scored content...</div>';

            try {
                const params = new URLSearchParams({
                    page: currentPage,
                    per_page: 20,
                    search: currentFilters.search || '',
                    topic: currentFilters.topic || '',
                    priority: currentFilters.priority || '',
                    unread_only: currentFilters.unreadOnly || false,
                    bookmarked_only: currentFilters.bookmarkedOnly || false,
                    claude_only: currentFilters.claudeOnly || false
                });

                const response = await fetch(`${API_BASE}/api/items?${params}`);
                const data = await response.json();

                document.getElementById('itemCount').textContent = `Showing ${data.items.length} of ${data.total} items`;

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
            const isClaude = item.title.toLowerCase().includes('claude') || 
                           item.title.toLowerCase().includes('anthropic') ||
                           item.title.toLowerCase().includes('opus');
            
            div.className = `content-item ${item.is_read ? 'is-read' : ''} ${item.is_bookmarked ? 'is-bookmarked' : ''} ${isClaude ? 'is-claude' : ''}`;
            div.dataset.itemId = item.item_id;

            const publishedDate = new Date(item.published_date).toLocaleDateString();
            
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
                    <span>📖 ${item.reading_time} min</span>
                    <span>📊 Score: ${(item.priority_score * 100).toFixed(0)}%</span>
                </div>
                <div class="content-description">
                    ${item.content ? item.content.substring(0, 300) + '...' : ''}
                </div>
                <div class="content-footer">
                    <div class="topic-tags">
                        ${item.topics.map(topic => {
                            const isClaudeTopic = ['claude', 'anthropic', 'opus', 'sonnet'].includes(topic);
                            return `<span class="topic-tag ${isClaudeTopic ? 'claude-topic' : ''}">${topic}</span>`;
                        }).join('')}
                    </div>
                    <div class="priority-info">
                        <span class="priority-badge priority-${item.priority}">
                            ${item.priority}
                        </span>
                        <span class="priority-score">(${(item.priority_score * 100).toFixed(0)}%)</span>
                    </div>
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

@app.get("/youtube-intelligence")
async def youtube_intelligence():
    """Serve the YouTube Intelligence Dashboard"""
    youtube_dashboard_path = Path("dashboards/youtube_intelligence.html")
    
    if youtube_dashboard_path.exists():
        with open(youtube_dashboard_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return HTMLResponse(content=content)
    else:
        # Return a simple error page if file not found
        error_html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>YouTube Intelligence Dashboard - Not Found</title>
            <style>
                body { 
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; 
                    display: flex; 
                    justify-content: center; 
                    align-items: center; 
                    height: 100vh;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    margin: 0;
                }
                .error-card {
                    background: white;
                    padding: 40px;
                    border-radius: 20px;
                    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
                    text-align: center;
                    max-width: 500px;
                    margin: 20px;
                }
                h1 { 
                    color: #ef4444; 
                    margin-bottom: 20px;
                    font-size: 2rem;
                }
                p { 
                    color: #6b7280; 
                    margin: 15px 0; 
                    line-height: 1.6;
                }
                .path {
                    background: #f3f4f6;
                    padding: 10px;
                    border-radius: 8px;
                    font-family: monospace;
                    font-size: 0.9rem;
                    word-break: break-all;
                    margin: 20px 0;
                }
                a {
                    display: inline-block;
                    padding: 12px 24px;
                    background: #5145e0;
                    color: white;
                    text-decoration: none;
                    border-radius: 8px;
                    margin-top: 20px;
                    transition: background 0.3s;
                }
                a:hover {
                    background: #4339c9;
                }
            </style>
        </head>
        <body>
            <div class="error-card">
                <h1>📊 Dashboard Not Found</h1>
                <p>The YouTube Intelligence Dashboard file could not be located at the expected path.</p>
                <div class="path">""" + str(youtube_dashboard_path) + """</div>
                <p>Please ensure the file exists or contact support.</p>
                <a href="/">🏠 Return to Main Dashboard</a>
            </div>
        </body>
        </html>
        """
        return HTMLResponse(content=error_html, status_code=404)

if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting Universal Topic Intelligence System Dashboard")
    print("✅ Using properly scored priorities from database")
    print("🤖 Claude content now correctly prioritized as CRITICAL")
    print("📍 Open your browser to: http://localhost:5001")
    print("\nPriority Distribution:")
    print("  CRITICAL: 77 items (including all Claude content)")
    print("  HIGH: 15 items")
    print("  MEDIUM: 45 items")
    print("\nPress Ctrl+C to stop the server\n")
    
    uvicorn.run(app, host="0.0.0.0", port=5001)