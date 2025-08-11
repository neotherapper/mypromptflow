#!/usr/bin/env python3
"""
Enhanced Universal Topic Intelligence System Dashboard v3
- Removed language prominence
- Added Save for Later functionality
- Added Mark as Read tracking
- Added better user features
"""

import asyncio
import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional
from contextlib import contextmanager
import time

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from enum import Enum

# Import our system components
from agents.queen_agent import QueenAgent
from storage.database import StorageManager

# Initialize FastAPI app
app = FastAPI(
    title="Universal Topic Intelligence System",
    description="Intelligent monitoring for any topic domain",
    version="3.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
DB_PATH = Path("storage/universal_topics.db")
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
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS collections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.execute('''
            CREATE TABLE IF NOT EXISTS collection_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                collection_id INTEGER,
                item_id TEXT,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (collection_id) REFERENCES collections(id)
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

# Pydantic models
class ContentPriority(str, Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"

class Stats(BaseModel):
    total_items: int
    unread_count: int
    saved_for_later: int
    high_priority_unread: int
    last_24_hours: int
    trending_topics: List[Dict[str, Any]]
    reading_queue_time: int  # Estimated minutes to read unread items

class ContentItemResponse(BaseModel):
    item_id: str
    source_id: str
    title: str
    content: Optional[str]
    url: Optional[str]
    published_date: str
    author: Optional[str]
    topics: List[str]
    priority: ContentPriority
    quality_score: float
    is_bookmarked: bool = False
    is_read: bool = False
    reading_time: int = 0  # Estimated minutes
    metadata: Dict[str, Any] = Field(default_factory=dict)

class BookmarkRequest(BaseModel):
    item_id: str
    notes: Optional[str] = None
    tags: Optional[List[str]] = None

class ReadStatusRequest(BaseModel):
    item_id: str
    is_read: bool

def estimate_reading_time(content: str, title: str = "") -> int:
    """Estimate reading time in minutes based on word count"""
    if not content:
        return 1
    
    text = f"{title} {content}"
    word_count = len(text.split())
    # Average reading speed: 200-250 words per minute
    minutes = max(1, round(word_count / 225))
    return minutes

# API endpoints
@app.get("/api/stats", response_model=Stats)
async def get_stats():
    """Get dashboard statistics with better metrics"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Total items
        cursor.execute("SELECT COUNT(*) FROM content_items WHERE is_english = 1")
        total_items = cursor.fetchone()[0]
        
        # Unread count
        with get_user_db() as user_conn:
            user_cursor = user_conn.cursor()
            user_cursor.execute("SELECT COUNT(*) FROM read_items")
            read_count = user_cursor.fetchone()[0]
            
            # Saved for later
            user_cursor.execute("SELECT COUNT(*) FROM bookmarks")
            saved_count = user_cursor.fetchone()[0]
        
        unread_count = total_items - read_count
        
        # High priority unread (critical + high that are unread)
        cursor.execute("""
            SELECT COUNT(*) FROM content_items 
            WHERE priority IN ('critical', 'high') 
            AND is_english = 1
            AND item_id NOT IN (SELECT item_id FROM read_items)
        """)
        high_priority_unread = cursor.fetchone()[0] if cursor.fetchone() else 0
        
        # Last 24 hours
        yesterday = (datetime.now() - timedelta(days=1)).isoformat()
        cursor.execute("""
            SELECT COUNT(*) FROM content_items 
            WHERE datetime(collected_at) > datetime(?)
            AND is_english = 1
        """, (yesterday,))
        last_24_hours = cursor.fetchone()[0]
        
        # Trending topics (most common in last 24 hours)
        cursor.execute("""
            SELECT topics, COUNT(*) as count 
            FROM content_items 
            WHERE datetime(collected_at) > datetime(?)
            AND is_english = 1
            GROUP BY topics
            ORDER BY count DESC
            LIMIT 5
        """, (yesterday,))
        
        trending = []
        for row in cursor.fetchall():
            if row['topics']:
                topics = json.loads(row['topics']) if isinstance(row['topics'], str) else row['topics']
                for topic in topics[:1]:  # Take primary topic
                    trending.append({"name": topic, "count": row['count']})
        
        # Estimate total reading time for unread items
        cursor.execute("""
            SELECT content, title FROM content_items 
            WHERE is_english = 1
            AND item_id NOT IN (SELECT item_id FROM read_items)
        """)
        
        total_reading_time = 0
        for row in cursor.fetchall():
            total_reading_time += estimate_reading_time(row['content'] or "", row['title'] or "")
        
        return Stats(
            total_items=total_items,
            unread_count=unread_count,
            saved_for_later=saved_count,
            high_priority_unread=high_priority_unread,
            last_24_hours=last_24_hours,
            trending_topics=trending[:5],
            reading_queue_time=total_reading_time
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
    """Get content items with user status (read/bookmarked)"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Build query
        query = "SELECT * FROM content_items WHERE is_english = 1"
        params = []
        
        if topic:
            query += " AND topics LIKE ?"
            params.append(f"%{topic}%")
        
        if priority:
            query += " AND priority = ?"
            params.append(priority)
        
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
                    # No bookmarks yet
                    return {"items": [], "total": 0, "page": page, "per_page": per_page}
            
            # Get all bookmarks and read items for status
            user_cursor.execute("SELECT item_id FROM bookmarks")
            all_bookmarks = set(row[0] for row in user_cursor.fetchall())
            
            user_cursor.execute("SELECT item_id FROM read_items")
            all_read = set(row[0] for row in user_cursor.fetchall())
        
        # Order and paginate
        query += " ORDER BY collected_at DESC LIMIT ? OFFSET ?"
        params.extend([per_page, (page - 1) * per_page])
        
        cursor.execute(query, params)
        items = []
        
        for row in cursor.fetchall():
            item_dict = dict(row)
            
            # Parse JSON fields
            if item_dict.get('topics'):
                item_dict['topics'] = json.loads(item_dict['topics']) if isinstance(item_dict['topics'], str) else item_dict['topics']
            else:
                item_dict['topics'] = []
            
            if item_dict.get('metadata'):
                item_dict['metadata'] = json.loads(item_dict['metadata']) if isinstance(item_dict['metadata'], str) else item_dict['metadata']
            else:
                item_dict['metadata'] = {}
            
            # Remove language info from metadata since we're English-only
            if 'detected_language' in item_dict['metadata']:
                del item_dict['metadata']['detected_language']
            if 'language_confidence' in item_dict['metadata']:
                del item_dict['metadata']['language_confidence']
            if 'is_english' in item_dict['metadata']:
                del item_dict['metadata']['is_english']
            
            # Add user status
            item_dict['is_bookmarked'] = item_dict['item_id'] in all_bookmarks
            item_dict['is_read'] = item_dict['item_id'] in all_read
            
            # Add reading time estimate
            item_dict['reading_time'] = estimate_reading_time(
                item_dict.get('content', ''),
                item_dict.get('title', '')
            )
            
            items.append(ContentItemResponse(**item_dict))
        
        # Get total count
        count_query = "SELECT COUNT(*) FROM content_items WHERE is_english = 1"
        if topic:
            count_query += " AND topics LIKE ?"
        if priority:
            count_query += " AND priority = ?"
        
        cursor.execute(count_query, params[:-2] if params else [])  # Exclude pagination params
        total = cursor.fetchone()[0]
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "per_page": per_page
        }

@app.post("/api/bookmark")
async def toggle_bookmark(request: BookmarkRequest):
    """Toggle bookmark status for an item"""
    with get_user_db() as conn:
        cursor = conn.cursor()
        
        # Check if already bookmarked
        cursor.execute("SELECT id FROM bookmarks WHERE item_id = ?", (request.item_id,))
        existing = cursor.fetchone()
        
        if existing:
            # Remove bookmark
            cursor.execute("DELETE FROM bookmarks WHERE item_id = ?", (request.item_id,))
            conn.commit()
            return {"status": "removed", "item_id": request.item_id}
        else:
            # Add bookmark
            tags_json = json.dumps(request.tags) if request.tags else None
            cursor.execute(
                "INSERT INTO bookmarks (item_id, notes, tags) VALUES (?, ?, ?)",
                (request.item_id, request.notes, tags_json)
            )
            conn.commit()
            return {"status": "added", "item_id": request.item_id}

@app.post("/api/read-status")
async def update_read_status(request: ReadStatusRequest):
    """Update read status for an item"""
    with get_user_db() as conn:
        cursor = conn.cursor()
        
        if request.is_read:
            # Mark as read
            cursor.execute(
                "INSERT OR IGNORE INTO read_items (item_id) VALUES (?)",
                (request.item_id,)
            )
        else:
            # Mark as unread
            cursor.execute("DELETE FROM read_items WHERE item_id = ?", (request.item_id,))
        
        conn.commit()
        return {"status": "updated", "item_id": request.item_id, "is_read": request.is_read}

@app.get("/api/export")
async def export_items(
    format: str = Query("json", regex="^(json|csv)$"),
    bookmarked_only: bool = False
):
    """Export items in JSON or CSV format"""
    with get_db() as conn:
        cursor = conn.cursor()
        
        query = "SELECT * FROM content_items WHERE is_english = 1"
        params = []
        
        if bookmarked_only:
            with get_user_db() as user_conn:
                user_cursor = user_conn.cursor()
                user_cursor.execute("SELECT item_id FROM bookmarks")
                bookmark_ids = [row[0] for row in user_cursor.fetchall()]
                
                if not bookmark_ids:
                    return JSONResponse(content={"items": []})
                
                placeholders = ','.join('?' * len(bookmark_ids))
                query += f" AND item_id IN ({placeholders})"
                params.extend(bookmark_ids)
        
        cursor.execute(query, params)
        items = []
        
        for row in cursor.fetchall():
            item = dict(row)
            # Clean up for export
            if 'detected_language' in item:
                del item['detected_language']
            if 'language_confidence' in item:
                del item['language_confidence']
            if 'is_english' in item:
                del item['is_english']
            items.append(item)
        
        if format == "csv":
            import csv
            import io
            
            output = io.StringIO()
            if items:
                writer = csv.DictWriter(output, fieldnames=items[0].keys())
                writer.writeheader()
                writer.writerows(items)
            
            return HTMLResponse(
                content=output.getvalue(),
                media_type="text/csv",
                headers={"Content-Disposition": "attachment; filename=export.csv"}
            )
        else:
            return JSONResponse(content={"items": items})

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
                topics = json.loads(row['topics']) if isinstance(row['topics'], str) else row['topics']
                all_topics.update(topics)
        
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
        /* Modern Design System */
        :root {
            /* Colors */
            --primary-600: #5145e0;
            --primary-700: #4339c9;
            --success-500: #10b981;
            --warning-500: #f59e0b;
            --danger-500: #ef4444;
            --gray-50: #f9fafb;
            --gray-100: #f3f4f6;
            --gray-200: #e5e7eb;
            --gray-300: #d1d5db;
            --gray-400: #9ca3af;
            --gray-500: #6b7280;
            --gray-600: #4b5563;
            --gray-700: #374151;
            --gray-800: #1f2937;
            --gray-900: #111827;
            
            /* Spacing */
            --space-xs: 0.25rem;
            --space-sm: 0.5rem;
            --space-md: 1rem;
            --space-lg: 1.5rem;
            --space-xl: 2rem;
            --space-2xl: 3rem;
            
            /* Typography */
            --font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            --text-xs: 0.75rem;
            --text-sm: 0.875rem;
            --text-base: 1rem;
            --text-lg: 1.125rem;
            --text-xl: 1.25rem;
            --text-2xl: 1.5rem;
            --text-3xl: 1.875rem;
            
            /* Shadows */
            --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
            --shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
            --shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
            --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
            
            /* Borders */
            --radius-sm: 0.25rem;
            --radius: 0.375rem;
            --radius-lg: 0.5rem;
            --radius-xl: 0.75rem;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: var(--font-sans);
            background: var(--gray-50);
            color: var(--gray-900);
            line-height: 1.5;
        }

        /* Layout */
        .container {
            display: flex;
            min-height: 100vh;
        }

        /* Header */
        .header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 64px;
            background: white;
            border-bottom: 1px solid var(--gray-200);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 var(--space-xl);
            z-index: 100;
            box-shadow: var(--shadow-sm);
        }

        .header-title {
            font-size: var(--text-xl);
            font-weight: 700;
            color: var(--gray-900);
            display: flex;
            align-items: center;
            gap: var(--space-sm);
        }

        .header-actions {
            display: flex;
            align-items: center;
            gap: var(--space-md);
        }

        /* Search Bar */
        .search-container {
            position: relative;
            width: 400px;
        }

        .search-input {
            width: 100%;
            padding: var(--space-sm) var(--space-md);
            padding-left: 2.5rem;
            border: 1px solid var(--gray-300);
            border-radius: var(--radius-lg);
            font-size: var(--text-sm);
            transition: all 0.2s;
        }

        .search-input:focus {
            outline: none;
            border-color: var(--primary-600);
            box-shadow: 0 0 0 3px rgba(81, 69, 224, 0.1);
        }

        .search-icon {
            position: absolute;
            left: var(--space-md);
            top: 50%;
            transform: translateY(-50%);
            color: var(--gray-400);
        }

        /* Main Content */
        .main-content {
            flex: 1;
            margin-top: 64px;
            padding: var(--space-xl);
        }

        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: var(--space-lg);
            margin-bottom: var(--space-2xl);
        }

        .stat-card {
            background: white;
            border-radius: var(--radius-lg);
            padding: var(--space-lg);
            box-shadow: var(--shadow);
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .stat-card:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }

        .stat-label {
            font-size: var(--text-sm);
            color: var(--gray-600);
            margin-bottom: var(--space-xs);
            font-weight: 500;
        }

        .stat-value {
            font-size: var(--text-2xl);
            font-weight: 700;
            color: var(--gray-900);
            display: flex;
            align-items: baseline;
            gap: var(--space-sm);
        }

        .stat-badge {
            font-size: var(--text-xs);
            padding: 2px 6px;
            border-radius: var(--radius);
            font-weight: 500;
        }

        .stat-badge.success {
            background: rgba(16, 185, 129, 0.1);
            color: var(--success-500);
        }

        .stat-badge.warning {
            background: rgba(245, 158, 11, 0.1);
            color: var(--warning-500);
        }

        .stat-badge.danger {
            background: rgba(239, 68, 68, 0.1);
            color: var(--danger-500);
        }

        /* Filter Bar */
        .filter-bar {
            background: white;
            border-radius: var(--radius-lg);
            padding: var(--space-lg);
            margin-bottom: var(--space-xl);
            box-shadow: var(--shadow);
        }

        .filter-row {
            display: flex;
            gap: var(--space-md);
            flex-wrap: wrap;
            align-items: center;
        }

        .filter-group {
            display: flex;
            flex-direction: column;
            gap: var(--space-xs);
        }

        .filter-label {
            font-size: var(--text-xs);
            color: var(--gray-600);
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .filter-select {
            padding: var(--space-sm) var(--space-md);
            border: 1px solid var(--gray-300);
            border-radius: var(--radius);
            font-size: var(--text-sm);
            background: white;
            cursor: pointer;
            min-width: 150px;
        }

        .filter-checkbox {
            display: flex;
            align-items: center;
            gap: var(--space-sm);
            cursor: pointer;
            user-select: none;
        }

        .filter-checkbox input {
            width: 18px;
            height: 18px;
            cursor: pointer;
        }

        /* Content Section */
        .content-section {
            background: white;
            border-radius: var(--radius-lg);
            box-shadow: var(--shadow);
            overflow: hidden;
        }

        .content-header {
            padding: var(--space-lg);
            border-bottom: 1px solid var(--gray-200);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .content-title {
            font-size: var(--text-lg);
            font-weight: 600;
            color: var(--gray-900);
        }

        .content-actions {
            display: flex;
            gap: var(--space-sm);
        }

        /* Content Items */
        .content-list {
            padding: var(--space-lg);
        }

        .content-item {
            padding: var(--space-lg);
            border: 1px solid var(--gray-200);
            border-radius: var(--radius-lg);
            margin-bottom: var(--space-md);
            transition: all 0.2s;
            position: relative;
        }

        .content-item:hover {
            border-color: var(--gray-300);
            box-shadow: var(--shadow);
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
            margin-bottom: var(--space-sm);
        }

        .content-title-link {
            font-size: var(--text-lg);
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
            gap: var(--space-sm);
        }

        .action-btn {
            padding: var(--space-xs) var(--space-sm);
            border: 1px solid var(--gray-300);
            border-radius: var(--radius);
            background: white;
            cursor: pointer;
            font-size: var(--text-sm);
            color: var(--gray-600);
            transition: all 0.2s;
        }

        .action-btn:hover {
            background: var(--gray-50);
            border-color: var(--gray-400);
        }

        .action-btn.active {
            background: var(--primary-600);
            color: white;
            border-color: var(--primary-600);
        }

        .content-meta {
            display: flex;
            align-items: center;
            gap: var(--space-lg);
            margin-bottom: var(--space-sm);
            font-size: var(--text-sm);
            color: var(--gray-600);
        }

        .meta-item {
            display: flex;
            align-items: center;
            gap: var(--space-xs);
        }

        .content-description {
            color: var(--gray-700);
            line-height: 1.6;
            margin-bottom: var(--space-md);
        }

        .content-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: var(--space-md);
        }

        .topic-tags {
            display: flex;
            gap: var(--space-sm);
            flex-wrap: wrap;
        }

        .topic-tag {
            padding: var(--space-xs) var(--space-sm);
            background: var(--gray-100);
            color: var(--gray-700);
            border-radius: var(--radius);
            font-size: var(--text-xs);
            font-weight: 500;
        }

        .priority-badge {
            padding: var(--space-xs) var(--space-sm);
            border-radius: var(--radius);
            font-size: var(--text-xs);
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

        .reading-time {
            font-size: var(--text-xs);
            color: var(--gray-500);
        }

        /* Trending Topics */
        .trending-list {
            display: flex;
            flex-direction: column;
            gap: var(--space-xs);
            margin-top: var(--space-sm);
        }

        .trending-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: var(--space-xs) 0;
            font-size: var(--text-sm);
        }

        .trending-name {
            color: var(--gray-700);
            text-transform: capitalize;
        }

        .trending-count {
            background: var(--gray-100);
            padding: 2px 8px;
            border-radius: var(--radius);
            font-size: var(--text-xs);
            color: var(--gray-600);
        }

        /* Buttons */
        .btn {
            padding: var(--space-sm) var(--space-lg);
            border: none;
            border-radius: var(--radius);
            font-size: var(--text-sm);
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            gap: var(--space-sm);
        }

        .btn-primary {
            background: var(--primary-600);
            color: white;
        }

        .btn-primary:hover {
            background: var(--primary-700);
        }

        .btn-secondary {
            background: white;
            color: var(--gray-700);
            border: 1px solid var(--gray-300);
        }

        .btn-secondary:hover {
            background: var(--gray-50);
        }

        /* Loading State */
        .loading {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: var(--space-2xl);
            color: var(--gray-500);
        }

        .spinner {
            width: 40px;
            height: 40px;
            border: 3px solid var(--gray-200);
            border-top-color: var(--primary-600);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        /* Empty State */
        .empty-state {
            text-align: center;
            padding: var(--space-2xl);
            color: var(--gray-500);
        }

        .empty-icon {
            font-size: 3rem;
            margin-bottom: var(--space-md);
            opacity: 0.3;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .header {
                padding: 0 var(--space-md);
            }

            .search-container {
                width: 100%;
            }

            .main-content {
                padding: var(--space-md);
            }

            .stats-grid {
                grid-template-columns: 1fr;
            }

            .filter-row {
                flex-direction: column;
                align-items: stretch;
            }

            .filter-select {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <header class="header">
            <div class="header-title">
                <span>🧠</span>
                Universal Topic Intelligence
            </div>
            <div class="header-actions">
                <div class="search-container">
                    <span class="search-icon">🔍</span>
                    <input 
                        type="text" 
                        class="search-input" 
                        placeholder="Search across all content..."
                        id="globalSearch"
                    >
                </div>
                <button class="btn btn-secondary" onclick="exportData()">
                    📥 Export
                </button>
                <button class="btn btn-primary" onclick="refreshData()">
                    🔄 Refresh
                </button>
            </div>
        </header>

        <!-- Main Content -->
        <main class="main-content">
            <!-- Stats Grid -->
            <div class="stats-grid" id="statsGrid">
                <div class="stat-card">
                    <div class="stat-label">Unread Items</div>
                    <div class="stat-value">
                        <span id="unreadCount">-</span>
                        <span class="stat-badge warning" id="unreadBadge">Loading</span>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Saved for Later</div>
                    <div class="stat-value">
                        <span id="savedCount">-</span>
                        <span class="reading-time" id="readingTime">-</span>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Priority Queue</div>
                    <div class="stat-value">
                        <span id="priorityCount">-</span>
                        <span class="stat-badge danger">Urgent</span>
                    </div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Trending Topics</div>
                    <div class="trending-list" id="trendingList">
                        <!-- Populated by JS -->
                    </div>
                </div>
            </div>

            <!-- Filter Bar -->
            <div class="filter-bar">
                <div class="filter-row">
                    <div class="filter-group">
                        <label class="filter-label">Topic</label>
                        <select class="filter-select" id="topicFilter">
                            <option value="">All Topics</option>
                        </select>
                    </div>
                    <div class="filter-group">
                        <label class="filter-label">Priority</label>
                        <select class="filter-select" id="priorityFilter">
                            <option value="">All Priorities</option>
                            <option value="critical">Critical</option>
                            <option value="high">High</option>
                            <option value="medium">Medium</option>
                            <option value="low">Low</option>
                        </select>
                    </div>
                    <div class="filter-checkbox">
                        <input type="checkbox" id="unreadOnly">
                        <label for="unreadOnly">Unread Only</label>
                    </div>
                    <div class="filter-checkbox">
                        <input type="checkbox" id="bookmarkedOnly">
                        <label for="bookmarkedOnly">Bookmarked Only</label>
                    </div>
                </div>
            </div>

            <!-- Content Section -->
            <div class="content-section">
                <div class="content-header">
                    <h2 class="content-title">Intelligence Feed</h2>
                    <div class="content-actions">
                        <button class="btn btn-secondary" onclick="markAllRead()">
                            ✓ Mark All Read
                        </button>
                    </div>
                </div>
                <div class="content-list" id="contentList">
                    <div class="loading">
                        <div class="spinner"></div>
                    </div>
                </div>
            </div>
        </main>
    </div>

    <script>
        const API_BASE = '';
        let currentPage = 1;
        let currentFilters = {};

        // Initialize
        document.addEventListener('DOMContentLoaded', () => {
            loadStats();
            loadTopics();
            loadContent();
            setupEventListeners();
        });

        // Setup event listeners
        function setupEventListeners() {
            // Search
            let searchTimeout;
            document.getElementById('globalSearch').addEventListener('input', (e) => {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    currentFilters.search = e.target.value;
                    loadContent();
                }, 300);
            });

            // Filters
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

        // Load stats
        async function loadStats() {
            try {
                const response = await fetch(`${API_BASE}/api/stats`);
                const stats = await response.json();

                // Update stats display
                document.getElementById('unreadCount').textContent = stats.unread_count;
                document.getElementById('unreadBadge').textContent = 
                    stats.unread_count > 0 ? `${stats.last_24_hours} new` : 'All caught up';
                
                document.getElementById('savedCount').textContent = stats.saved_for_later;
                document.getElementById('readingTime').textContent = 
                    stats.reading_queue_time > 0 ? `~${stats.reading_queue_time} min` : '';
                
                document.getElementById('priorityCount').textContent = stats.high_priority_unread;

                // Update trending topics
                const trendingList = document.getElementById('trendingList');
                trendingList.innerHTML = '';
                
                if (stats.trending_topics && stats.trending_topics.length > 0) {
                    stats.trending_topics.forEach(topic => {
                        const item = document.createElement('div');
                        item.className = 'trending-item';
                        item.innerHTML = `
                            <span class="trending-name">${topic.name}</span>
                            <span class="trending-count">${topic.count}</span>
                        `;
                        trendingList.appendChild(item);
                    });
                } else {
                    trendingList.innerHTML = '<span style="color: var(--gray-400); font-size: var(--text-sm);">No trending topics</span>';
                }

            } catch (error) {
                console.error('Error loading stats:', error);
            }
        }

        // Load topics for filter
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

        // Load content
        async function loadContent() {
            const contentList = document.getElementById('contentList');
            contentList.innerHTML = '<div class="loading"><div class="spinner"></div></div>';

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
                            <div class="empty-icon">📭</div>
                            <h3>No items found</h3>
                            <p>Try adjusting your filters or check back later</p>
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
                        <div class="empty-icon">⚠️</div>
                        <h3>Error loading content</h3>
                        <p>${error.message}</p>
                    </div>
                `;
            }
        }

        // Create content item element
        function createContentItem(item) {
            const div = document.createElement('div');
            div.className = `content-item ${item.is_read ? 'is-read' : ''} ${item.is_bookmarked ? 'is-bookmarked' : ''}`;
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
                    <span class="meta-item">📅 ${publishedDate}</span>
                    ${item.author ? `<span class="meta-item">✍️ ${item.author}</span>` : ''}
                    <span class="meta-item">📖 ${item.reading_time} min read</span>
                    <span class="meta-item">📊 ${(item.quality_score * 100).toFixed(0)}% quality</span>
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
                        ${item.priority}
                    </span>
                </div>
            `;

            return div;
        }

        // Toggle bookmark
        async function toggleBookmark(itemId) {
            try {
                const response = await fetch(`${API_BASE}/api/bookmark`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ item_id: itemId })
                });
                
                const result = await response.json();
                
                // Update UI
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
                
                // Reload stats
                loadStats();
                
            } catch (error) {
                console.error('Error toggling bookmark:', error);
            }
        }

        // Toggle read status
        async function toggleRead(itemId, isRead) {
            try {
                const response = await fetch(`${API_BASE}/api/read-status`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ item_id: itemId, is_read: isRead })
                });
                
                const result = await response.json();
                
                // Update UI
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
                
                // Reload stats
                loadStats();
                
            } catch (error) {
                console.error('Error toggling read status:', error);
            }
        }

        // Mark all as read
        async function markAllRead() {
            if (!confirm('Mark all visible items as read?')) return;
            
            const items = document.querySelectorAll('.content-item:not(.is-read)');
            for (const item of items) {
                await toggleRead(item.dataset.itemId, true);
            }
        }

        // Export data
        async function exportData() {
            const format = prompt('Export format (json or csv):', 'json');
            if (!format) return;
            
            const bookmarkedOnly = confirm('Export only bookmarked items?');
            
            window.location.href = `${API_BASE}/api/export?format=${format}&bookmarked_only=${bookmarkedOnly}`;
        }

        // Refresh data
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
    
    print("🚀 Starting Universal Topic Intelligence System Dashboard v3")
    print("✨ Enhanced with Save for Later, Read Tracking, and Smart Features")
    print("📍 Open your browser to: http://localhost:5001")
    print("Press Ctrl+C to stop the server\n")
    
    uvicorn.run(app, host="0.0.0.0", port=5001)