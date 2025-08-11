#!/usr/bin/env python3
"""
Web Dashboard for Universal Topic Intelligence System
"""

from flask import Flask, render_template, jsonify, request
import sqlite3
from datetime import datetime, timedelta
import json
from pathlib import Path
import asyncio
from agents.queen_agent import QueenAgent

app = Flask(__name__)
app.config['SECRET_KEY'] = 'topic-intelligence-system-2024'

def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect('topic_intelligence.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/stats')
def get_stats():
    """Get system statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
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
    
    conn.close()
    
    return jsonify({
        'total_items': total_items,
        'priority_distribution': priority_dist,
        'top_sources': top_sources,
        'items_24h': recent_count
    })

@app.route('/api/items')
def get_items():
    """Get content items with pagination"""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    topic = request.args.get('topic', '')
    priority = request.args.get('priority', '')
    
    offset = (page - 1) * per_page
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
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
        # Format date
        if item['published_date']:
            item['published_date'] = item['published_date'][:19]  # Trim to readable format
        items.append(item)
    
    conn.close()
    
    return jsonify({
        'items': items,
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': (total + per_page - 1) // per_page
    })

@app.route('/api/topics')
def get_topics():
    """Get monitored topics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT topic_slug, topic_name, priority_level, 
               items_collected, last_monitored
        FROM topics
        ORDER BY items_collected DESC
    """)
    
    topics = []
    for row in cursor.fetchall():
        topic = dict(row)
        if topic['last_monitored']:
            topic['last_monitored'] = topic['last_monitored'][:19]
        topics.append(topic)
    
    conn.close()
    
    return jsonify(topics)

@app.route('/api/monitor/<topic>')
def monitor_topic(topic):
    """Trigger monitoring for a specific topic"""
    try:
        # Run async monitoring in sync context
        async def run_monitor():
            queen = QueenAgent()
            result = await queen.orchestrate(force_topics=[topic])
            return {
                'success': True,
                'items_collected': result.total_items_collected,
                'topics_monitored': result.topics_monitored
            }
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(run_monitor())
        loop.close()
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    templates_dir = Path('templates')
    templates_dir.mkdir(exist_ok=True)
    
    # Create the HTML template if it doesn't exist
    dashboard_html = templates_dir / 'dashboard.html'
    if not dashboard_html.exists():
        dashboard_html.write_text('''<!DOCTYPE html>
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
        .container { max-width: 1400px; margin: 0 auto; }
        .header {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }
        h1 { color: #333; margin-bottom: 10px; }
        .subtitle { color: #666; font-size: 16px; }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }
        .stat-label { 
            color: #999; 
            font-size: 14px; 
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }
        .stat-value { 
            font-size: 32px; 
            font-weight: bold; 
            color: #333;
        }
        .content-section {
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }
        .filters {
            display: flex;
            gap: 15px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        select, button {
            padding: 10px 20px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            background: white;
            cursor: pointer;
            transition: all 0.3s;
        }
        select:hover, button:hover {
            border-color: #667eea;
        }
        button.primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
        }
        .items-list {
            max-height: 600px;
            overflow-y: auto;
        }
        .item-card {
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
            transition: all 0.3s;
        }
        .item-card:hover {
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }
        .item-title {
            font-size: 18px;
            color: #333;
            margin-bottom: 10px;
            font-weight: 600;
        }
        .item-meta {
            display: flex;
            gap: 20px;
            color: #666;
            font-size: 14px;
            margin-bottom: 10px;
        }
        .priority-badge {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
        }
        .priority-critical { background: #ff4757; color: white; }
        .priority-high { background: #ff9ff3; color: white; }
        .priority-medium { background: #54a0ff; color: white; }
        .priority-low { background: #48dbfb; color: white; }
        .topic-tag {
            display: inline-block;
            padding: 4px 10px;
            background: #f0f0f0;
            border-radius: 5px;
            font-size: 12px;
            margin-right: 5px;
        }
        .loading {
            text-align: center;
            padding: 40px;
            color: #999;
        }
        .topics-section {
            margin-top: 30px;
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }
        .topic-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .topic-card {
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            padding: 20px;
            transition: all 0.3s;
        }
        .topic-card:hover {
            border-color: #667eea;
            transform: translateY(-2px);
        }
        .topic-name {
            font-size: 18px;
            font-weight: 600;
            color: #333;
            margin-bottom: 10px;
        }
        .topic-stats {
            color: #666;
            font-size: 14px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🧠 Universal Topic Intelligence System</h1>
            <p class="subtitle">Real-time monitoring of Claude AI, React, TypeScript, and more</p>
        </div>

        <div class="stats-grid" id="statsGrid">
            <div class="stat-card">
                <div class="stat-label">Total Items</div>
                <div class="stat-value" id="totalItems">-</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Last 24 Hours</div>
                <div class="stat-value" id="items24h">-</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">High Priority</div>
                <div class="stat-value" id="highPriority">-</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">Active Topics</div>
                <div class="stat-value" id="activeTopics">-</div>
            </div>
        </div>

        <div class="topics-section">
            <h2>📊 Monitored Topics</h2>
            <div class="topic-grid" id="topicsGrid">
                <div class="loading">Loading topics...</div>
            </div>
        </div>

        <div class="content-section">
            <h2>📰 Latest Intelligence</h2>
            <div class="filters">
                <select id="topicFilter">
                    <option value="">All Topics</option>
                    <option value="claude-ai">Claude AI</option>
                    <option value="react">React</option>
                    <option value="typescript">TypeScript</option>
                </select>
                <select id="priorityFilter">
                    <option value="">All Priorities</option>
                    <option value="critical">Critical</option>
                    <option value="high">High</option>
                    <option value="medium">Medium</option>
                    <option value="low">Low</option>
                </select>
                <button class="primary" onclick="refreshData()">🔄 Refresh</button>
                <button onclick="triggerMonitoring()">🚀 Run Monitoring</button>
            </div>
            <div class="items-list" id="itemsList">
                <div class="loading">Loading content...</div>
            </div>
        </div>
    </div>

    <script>
        let currentPage = 1;
        
        async function loadStats() {
            try {
                const response = await fetch('/api/stats');
                const data = await response.json();
                
                document.getElementById('totalItems').textContent = data.total_items;
                document.getElementById('items24h').textContent = data.items_24h;
                
                const highPriority = (data.priority_distribution.critical || 0) + 
                                    (data.priority_distribution.high || 0);
                document.getElementById('highPriority').textContent = highPriority;
            } catch (error) {
                console.error('Error loading stats:', error);
            }
        }
        
        async function loadTopics() {
            try {
                const response = await fetch('/api/topics');
                const topics = await response.json();
                
                document.getElementById('activeTopics').textContent = topics.length;
                
                const topicsGrid = document.getElementById('topicsGrid');
                if (topics.length === 0) {
                    topicsGrid.innerHTML = '<div class="loading">No topics found</div>';
                    return;
                }
                
                topicsGrid.innerHTML = topics.map(topic => `
                    <div class="topic-card">
                        <div class="topic-name">${topic.topic_name || topic.topic_slug}</div>
                        <div class="topic-stats">
                            <p>📦 Items collected: ${topic.items_collected || 0}</p>
                            <p>🎯 Priority: ${topic.priority_level || 'medium'}</p>
                            <p>🕒 Last monitored: ${topic.last_monitored || 'Never'}</p>
                        </div>
                        <button onclick="monitorTopic('${topic.topic_slug}')" style="margin-top: 10px;">
                            Monitor Now
                        </button>
                    </div>
                `).join('');
            } catch (error) {
                console.error('Error loading topics:', error);
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
                
                const response = await fetch(`/api/items?${params}`);
                const data = await response.json();
                
                const itemsList = document.getElementById('itemsList');
                
                if (data.items.length === 0) {
                    itemsList.innerHTML = '<div class="loading">No items found</div>';
                    return;
                }
                
                itemsList.innerHTML = data.items.map(item => `
                    <div class="item-card">
                        <div class="item-title">${item.title}</div>
                        <div class="item-meta">
                            <span class="priority-badge priority-${item.priority_level}">
                                ${item.priority_level}
                            </span>
                            <span>📅 ${item.published_date || 'Unknown'}</span>
                            <span>📡 ${item.source_id}</span>
                            <span>⭐ Score: ${(item.priority_score * 100).toFixed(0)}%</span>
                        </div>
                        <div class="topics">
                            ${item.topics.map(t => `<span class="topic-tag">${t}</span>`).join('')}
                        </div>
                        ${item.url ? `<a href="${item.url}" target="_blank" style="color: #667eea; text-decoration: none; font-size: 14px;">🔗 View Source</a>` : ''}
                    </div>
                `).join('');
                
                currentPage = page;
            } catch (error) {
                console.error('Error loading items:', error);
            }
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
                const response = await fetch('/api/monitor/claude-ai');
                const result = await response.json();
                
                if (result.success) {
                    alert(`Monitoring complete! Collected ${result.items_collected} items`);
                    refreshData();
                } else {
                    alert('Monitoring failed: ' + result.error);
                }
            } catch (error) {
                alert('Error: ' + error.message);
            } finally {
                button.disabled = false;
                button.textContent = '🚀 Run Monitoring';
            }
        }
        
        async function monitorTopic(topic) {
            if (!confirm(`Start monitoring ${topic}?`)) return;
            
            try {
                const response = await fetch(`/api/monitor/${topic}`);
                const result = await response.json();
                
                if (result.success) {
                    alert(`Monitoring complete! Collected ${result.items_collected} items`);
                    refreshData();
                } else {
                    alert('Monitoring failed: ' + result.error);
                }
            } catch (error) {
                alert('Error: ' + error.message);
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
</html>''')
    
    print("\n🚀 Starting Universal Topic Intelligence System Dashboard")
    print("📍 Open your browser to: http://localhost:5000")
    print("Press Ctrl+C to stop the server\n")
    
    app.run(debug=True, port=5000)