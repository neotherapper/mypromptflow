#!/usr/bin/env python3
"""
FastAPI Web Dashboard for Universal Topic Intelligence System
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from datetime import datetime, timedelta
import json
from pathlib import Path
import asyncio
from typing import Optional, List, Dict, Any
from pydantic import BaseModel

# Import our system components
from agents.queen_agent import QueenAgent
from storage import StorageManager

app = FastAPI(title="Universal Topic Intelligence System")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models for API responses
class Stats(BaseModel):
    total_items: int
    priority_distribution: Dict[str, int]
    top_sources: List[Dict[str, Any]]
    items_24h: int

class ContentItemResponse(BaseModel):
    items: List[Dict[str, Any]]
    total: int
    page: int
    per_page: int
    total_pages: int

class MonitoringResult(BaseModel):
    success: bool
    items_collected: int
    topics_monitored: List[str]
    error: Optional[str] = None

# Database helper
def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect('topic_intelligence.db')
    conn.row_factory = sqlite3.Row
    return conn

# HTML Dashboard
DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Universal Topic Intelligence System</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container { 
            max-width: 1400px; 
            margin: 0 auto; 
        }
        
        .header {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            text-align: center;
        }
        
        h1 { 
            color: #333; 
            margin-bottom: 10px;
            font-size: 2.5rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .subtitle { 
            color: #666; 
            font-size: 16px; 
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.15);
        }
        
        .stat-label { 
            color: #999; 
            font-size: 14px; 
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }
        
        .stat-value { 
            font-size: 36px; 
            font-weight: bold; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .content-section {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        
        h2 {
            color: #333;
            margin-bottom: 20px;
            font-size: 1.8rem;
        }
        
        .filters {
            display: flex;
            gap: 15px;
            margin-bottom: 25px;
            flex-wrap: wrap;
            align-items: center;
        }
        
        select, button {
            padding: 12px 20px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 14px;
            background: white;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        select:hover, button:hover {
            border-color: #667eea;
            transform: translateY(-2px);
        }
        
        button.primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            font-weight: 600;
        }
        
        button.primary:hover {
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .items-container {
            max-height: 600px;
            overflow-y: auto;
            padding-right: 10px;
        }
        
        .items-container::-webkit-scrollbar {
            width: 8px;
        }
        
        .items-container::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }
        
        .items-container::-webkit-scrollbar-thumb {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 10px;
        }
        
        .item-card {
            background: #f8f9fa;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            transition: all 0.3s;
            border: 2px solid transparent;
        }
        
        .item-card:hover {
            background: white;
            border-color: #667eea;
            box-shadow: 0 5px 20px rgba(102, 126, 234, 0.2);
            transform: translateX(5px);
        }
        
        .item-title {
            font-size: 18px;
            color: #333;
            margin-bottom: 12px;
            font-weight: 600;
            line-height: 1.4;
        }
        
        .item-meta {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
            color: #666;
            font-size: 14px;
            margin-bottom: 12px;
        }
        
        .priority-badge {
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .priority-critical { 
            background: linear-gradient(135deg, #ff4757, #ff6348);
            color: white;
        }
        .priority-high { 
            background: linear-gradient(135deg, #ff9ff3, #feca57);
            color: white;
        }
        .priority-medium { 
            background: linear-gradient(135deg, #54a0ff, #48dbfb);
            color: white;
        }
        .priority-low { 
            background: linear-gradient(135deg, #48dbfb, #00d2d3);
            color: white;
        }
        
        .topic-tag {
            display: inline-block;
            padding: 5px 12px;
            background: linear-gradient(135deg, #f0f0f0, #e0e0e0);
            border-radius: 8px;
            font-size: 12px;
            margin-right: 5px;
            font-weight: 500;
        }
        
        .item-link {
            color: #667eea;
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            display: inline-flex;
            align-items: center;
            gap: 5px;
            transition: all 0.3s;
        }
        
        .item-link:hover {
            color: #764ba2;
            transform: translateX(3px);
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: #999;
            font-size: 18px;
        }
        
        .spinner {
            display: inline-block;
            width: 40px;
            height: 40px;
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .topics-section {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        
        .topic-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .topic-card {
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            border-radius: 15px;
            padding: 25px;
            transition: all 0.3s;
            cursor: pointer;
            position: relative;
            overflow: hidden;
        }
        
        .topic-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        .topic-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        }
        
        .topic-name {
            font-size: 20px;
            font-weight: 600;
            color: #333;
            margin-bottom: 15px;
        }
        
        .topic-stats {
            color: #666;
            font-size: 14px;
            line-height: 1.8;
        }
        
        .topic-stats p {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .monitor-btn {
            margin-top: 15px;
            width: 100%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 10px;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }
        
        .monitor-btn:hover {
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 Universal Topic Intelligence System</h1>
            <p class="subtitle">Real-time monitoring of Claude AI, React, TypeScript, MCP Servers, and AI Applications</p>
        </div>

        <div class="stats-grid" id="statsGrid">
            <div class="stat-card">
                <div class="stat-label">📚 Total Items</div>
                <div class="stat-value" id="totalItems">-</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">⏰ Last 24 Hours</div>
                <div class="stat-value" id="items24h">-</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">🔥 High Priority</div>
                <div class="stat-value" id="highPriority">-</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">🎯 Active Topics</div>
                <div class="stat-value" id="activeTopics">-</div>
            </div>
        </div>

        <div class="topics-section">
            <h2>📊 Monitored Topics</h2>
            <div class="topic-grid" id="topicsGrid">
                <div class="loading">
                    <div class="spinner"></div>
                    <p>Loading topics...</p>
                </div>
            </div>
        </div>

        <div class="content-section">
            <h2>📰 Latest Intelligence Feed</h2>
            <div class="filters">
                <select id="topicFilter">
                    <option value="">All Topics</option>
                    <option value="claude-ai">Claude AI</option>
                    <option value="react">React</option>
                    <option value="typescript">TypeScript</option>
                    <option value="mcp">MCP Servers</option>
                    <option value="ai">AI Applications</option>
                </select>
                <select id="priorityFilter">
                    <option value="">All Priorities</option>
                    <option value="critical">Critical Only</option>
                    <option value="high">High Priority</option>
                    <option value="medium">Medium Priority</option>
                    <option value="low">Low Priority</option>
                </select>
                <button class="primary" onclick="refreshData()">🔄 Refresh</button>
                <button onclick="triggerMonitoring()">🚀 Run Monitoring Now</button>
            </div>
            <div class="items-container" id="itemsList">
                <div class="loading">
                    <div class="spinner"></div>
                    <p>Loading content...</p>
                </div>
            </div>
        </div>
    </div>

    <script>
        let currentPage = 1;
        const API_BASE = 'http://localhost:5001';
        
        async function loadStats() {
            try {
                const response = await fetch(`${API_BASE}/api/stats`);
                const data = await response.json();
                
                document.getElementById('totalItems').textContent = data.total_items.toLocaleString();
                document.getElementById('items24h').textContent = data.items_24h.toLocaleString();
                
                const highPriority = (data.priority_distribution.critical || 0) + 
                                    (data.priority_distribution.high || 0);
                document.getElementById('highPriority').textContent = highPriority.toLocaleString();
            } catch (error) {
                console.error('Error loading stats:', error);
            }
        }
        
        async function loadTopics() {
            try {
                const response = await fetch(`${API_BASE}/api/topics`);
                const topics = await response.json();
                
                document.getElementById('activeTopics').textContent = topics.length;
                
                const topicsGrid = document.getElementById('topicsGrid');
                if (topics.length === 0) {
                    topicsGrid.innerHTML = '<div class="loading">No topics configured yet</div>';
                    return;
                }
                
                topicsGrid.innerHTML = topics.map(topic => `
                    <div class="topic-card" onclick="filterByTopic('${topic.topic_slug}')">
                        <div class="topic-name">${topic.topic_name || topic.topic_slug}</div>
                        <div class="topic-stats">
                            <p>📦 Items collected: <strong>${topic.items_collected || 0}</strong></p>
                            <p>🎯 Priority: <strong>${topic.priority_level || 'medium'}</strong></p>
                            <p>🕒 Last monitored: <strong>${topic.last_monitored ? new Date(topic.last_monitored).toLocaleString() : 'Never'}</strong></p>
                        </div>
                        <button class="monitor-btn" onclick="event.stopPropagation(); monitorTopic('${topic.topic_slug}')">
                            Monitor Now
                        </button>
                    </div>
                `).join('');
            } catch (error) {
                console.error('Error loading topics:', error);
                document.getElementById('topicsGrid').innerHTML = '<div class="loading">Error loading topics</div>';
            }
        }
        
        async function loadItems(page = 1) {
            try {
                const topicFilter = document.getElementById('topicFilter').value;
                const priorityFilter = document.getElementById('priorityFilter').value;
                
                const params = new URLSearchParams({
                    page: page,
                    per_page: 20,
                    topic: topicFilter,
                    priority: priorityFilter
                });
                
                const response = await fetch(`${API_BASE}/api/items?${params}`);
                const data = await response.json();
                
                const itemsList = document.getElementById('itemsList');
                
                if (data.items.length === 0) {
                    itemsList.innerHTML = '<div class="loading">No items found with current filters</div>';
                    return;
                }
                
                itemsList.innerHTML = data.items.map(item => {
                    const date = item.published_date ? new Date(item.published_date).toLocaleString() : 'Unknown';
                    const score = (item.priority_score * 100).toFixed(0);
                    
                    return `
                        <div class="item-card">
                            <div class="item-title">${item.title}</div>
                            <div class="item-meta">
                                <span class="priority-badge priority-${item.priority_level}">
                                    ${item.priority_level}
                                </span>
                                <span>📅 ${date}</span>
                                <span>📡 ${item.source_id}</span>
                                <span>⭐ Score: ${score}%</span>
                            </div>
                            <div class="topics">
                                ${item.topics.map(t => `<span class="topic-tag">${t}</span>`).join('')}
                            </div>
                            ${item.url ? `<a href="${item.url}" target="_blank" class="item-link">🔗 View Source →</a>` : ''}
                        </div>
                    `;
                }).join('');
                
                currentPage = page;
            } catch (error) {
                console.error('Error loading items:', error);
                document.getElementById('itemsList').innerHTML = '<div class="loading">Error loading items</div>';
            }
        }
        
        function filterByTopic(topic) {
            document.getElementById('topicFilter').value = topic;
            loadItems(1);
        }
        
        async function refreshData() {
            await Promise.all([
                loadStats(),
                loadTopics(),
                loadItems(currentPage)
            ]);
        }
        
        async function triggerMonitoring() {
            const button = event.target;
            button.disabled = true;
            button.textContent = '⏳ Monitoring...';
            
            try {
                const response = await fetch(`${API_BASE}/api/monitor/claude-ai`, {
                    method: 'POST'
                });
                const result = await response.json();
                
                if (result.success) {
                    alert(`✅ Monitoring complete!\nCollected ${result.items_collected} new items`);
                    refreshData();
                } else {
                    alert('❌ Monitoring failed: ' + result.error);
                }
            } catch (error) {
                alert('❌ Error: ' + error.message);
            } finally {
                button.disabled = false;
                button.textContent = '🚀 Run Monitoring Now';
            }
        }
        
        async function monitorTopic(topic) {
            if (!confirm(`Start monitoring ${topic}?`)) return;
            
            try {
                const response = await fetch(`${API_BASE}/api/monitor/${topic}`, {
                    method: 'POST'
                });
                const result = await response.json();
                
                if (result.success) {
                    alert(`✅ Monitoring complete!\nCollected ${result.items_collected} new items`);
                    refreshData();
                } else {
                    alert('❌ Monitoring failed: ' + result.error);
                }
            } catch (error) {
                alert('❌ Error: ' + error.message);
            }
        }
        
        // Initial load
        refreshData();
        
        // Auto-refresh every 30 seconds
        setInterval(refreshData, 30000);
        
        // Filter change handlers
        document.getElementById('topicFilter').addEventListener('change', () => loadItems(1));
        document.getElementById('priorityFilter').addEventListener('change', () => loadItems(1));
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """Serve the main dashboard"""
    return DASHBOARD_HTML

@app.get("/api/stats", response_model=Stats)
async def get_stats():
    """Get system statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Total items
        cursor.execute("SELECT COUNT(*) as count FROM content_items")
        total_items = cursor.fetchone()['count']
        
        # Items by priority
        cursor.execute("""
            SELECT priority_level, COUNT(*) as count 
            FROM content_items 
            GROUP BY priority_level
        """)
        priority_dist = {row['priority_level']: row['count'] for row in cursor.fetchall()}
        
        # Top sources
        cursor.execute("""
            SELECT source_id, COUNT(*) as count 
            FROM content_items 
            GROUP BY source_id 
            ORDER BY count DESC 
            LIMIT 5
        """)
        top_sources = [{'source': row['source_id'], 'count': row['count']} for row in cursor.fetchall()]
        
        # Recent activity (last 24 hours)
        cursor.execute("""
            SELECT COUNT(*) as count 
            FROM content_items 
            WHERE collected_date > datetime('now', '-24 hours')
        """)
        recent_count = cursor.fetchone()['count']
        
        return Stats(
            total_items=total_items,
            priority_distribution=priority_dist,
            top_sources=top_sources,
            items_24h=recent_count
        )
    finally:
        conn.close()

@app.get("/api/items", response_model=ContentItemResponse)
async def get_items(
    page: int = 1,
    per_page: int = 20,
    topic: str = "",
    priority: str = ""
):
    """Get content items with pagination"""
    offset = (page - 1) * per_page
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Build query
        query = "SELECT * FROM content_items WHERE 1=1"
        params = []
        
        if topic:
            query += " AND topics LIKE ?"
            params.append(f'%"{topic}"%')
        
        if priority:
            query += " AND priority_level = ?"
            params.append(priority)
        
        # Get total count
        count_query = query.replace("*", "COUNT(*) as count")
        cursor.execute(count_query, params)
        total = cursor.fetchone()['count']
        
        # Get items
        query += " ORDER BY collected_date DESC LIMIT ? OFFSET ?"
        params.extend([per_page, offset])
        
        cursor.execute(query, params)
        items = []
        for row in cursor.fetchall():
            item = dict(row)
            # Parse JSON fields
            item['topics'] = json.loads(item['topics']) if item['topics'] else []
            item['metadata'] = json.loads(item['metadata']) if item['metadata'] else {}
            items.append(item)
        
        return ContentItemResponse(
            items=items,
            total=total,
            page=page,
            per_page=per_page,
            total_pages=(total + per_page - 1) // per_page
        )
    finally:
        conn.close()

@app.get("/api/topics")
async def get_topics():
    """Get monitored topics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT topic_slug, topic_name, priority_level, 
                   items_collected, last_monitored
            FROM topics
            ORDER BY items_collected DESC
        """)
        
        topics = []
        for row in cursor.fetchall():
            topic = dict(row)
            topics.append(topic)
        
        return topics
    finally:
        conn.close()

@app.post("/api/monitor/{topic}", response_model=MonitoringResult)
async def monitor_topic(topic: str):
    """Trigger monitoring for a specific topic"""
    try:
        # Run async monitoring
        queen = QueenAgent()
        result = await queen.orchestrate(force_topics=[topic])
        
        return MonitoringResult(
            success=True,
            items_collected=result.total_items_collected,
            topics_monitored=result.topics_monitored
        )
    except Exception as e:
        return MonitoringResult(
            success=False,
            items_collected=0,
            topics_monitored=[],
            error=str(e)
        )

if __name__ == "__main__":
    import uvicorn
    print("\n🚀 Starting Universal Topic Intelligence System Dashboard")
    print("📍 Open your browser to: http://localhost:5001")
    print("Press Ctrl+C to stop the server\n")
    uvicorn.run(app, host="0.0.0.0", port=5001)