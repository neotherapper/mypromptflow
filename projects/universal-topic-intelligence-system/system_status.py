#!/usr/bin/env python3
"""
System Status Dashboard for Universal Topic Intelligence System
Provides comprehensive system health and statistics
"""

import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any
import os

def get_database_stats() -> Dict[str, Any]:
    """Get statistics from the database"""
    conn = sqlite3.connect("topic_intelligence.db")
    cursor = conn.cursor()
    
    stats = {}
    
    # Total items
    cursor.execute("SELECT COUNT(*) FROM content_items")
    stats['total_items'] = cursor.fetchone()[0]
    
    # Items by priority
    cursor.execute("""
        SELECT priority_level, COUNT(*) 
        FROM content_items 
        WHERE is_english = 1
        GROUP BY priority_level
    """)
    stats['items_by_priority'] = dict(cursor.fetchall())
    
    # Recent items (last 24 hours)
    yesterday = (datetime.now() - timedelta(days=1)).isoformat()
    cursor.execute("""
        SELECT COUNT(*) FROM content_items 
        WHERE collected_date >= ?
    """, (yesterday,))
    stats['items_24h'] = cursor.fetchone()[0]
    
    # Claude-specific items
    cursor.execute("""
        SELECT COUNT(*) FROM content_items 
        WHERE LOWER(title) LIKE '%claude%' 
           OR LOWER(title) LIKE '%anthropic%'
           OR LOWER(title) LIKE '%opus%'
    """)
    stats['claude_items'] = cursor.fetchone()[0]
    
    # Top sources
    cursor.execute("""
        SELECT source_id, COUNT(*) as count
        FROM content_items
        GROUP BY source_id
        ORDER BY count DESC
        LIMIT 5
    """)
    stats['top_sources'] = cursor.fetchall()
    
    # Bookmarked items
    if Path("user_data.db").exists():
        user_conn = sqlite3.connect("user_data.db")
        user_cursor = user_conn.cursor()
        
        user_cursor.execute("SELECT COUNT(*) FROM bookmarks")
        stats['bookmarked_items'] = user_cursor.fetchone()[0]
        
        user_cursor.execute("SELECT COUNT(*) FROM read_items")
        stats['read_items'] = user_cursor.fetchone()[0]
        
        user_conn.close()
    else:
        stats['bookmarked_items'] = 0
        stats['read_items'] = 0
    
    conn.close()
    return stats

def get_monitoring_stats() -> Dict[str, Any]:
    """Get monitoring statistics"""
    stats = {}
    
    # Load monitoring stats if available
    stats_file = Path("monitoring_stats.json")
    if stats_file.exists():
        with open(stats_file, 'r') as f:
            monitoring_stats = json.load(f)
            stats.update(monitoring_stats)
    
    # Check if monitoring is running
    pid_file = Path("monitoring.pid")
    if pid_file.exists():
        pid = int(pid_file.read_text().strip())
        # Check if process is running
        try:
            os.kill(pid, 0)
            stats['monitoring_active'] = True
            stats['monitoring_pid'] = pid
        except OSError:
            stats['monitoring_active'] = False
    else:
        stats['monitoring_active'] = False
    
    # Check if dashboard is running
    dashboard_pid_file = Path("dashboard.pid")
    if dashboard_pid_file.exists():
        pid = int(dashboard_pid_file.read_text().strip())
        try:
            os.kill(pid, 0)
            stats['dashboard_active'] = True
            stats['dashboard_pid'] = pid
        except OSError:
            stats['dashboard_active'] = False
    else:
        stats['dashboard_active'] = False
    
    return stats

def format_time_ago(timestamp_str: str) -> str:
    """Format timestamp as time ago"""
    if not timestamp_str:
        return "Never"
    
    timestamp = datetime.fromisoformat(timestamp_str)
    delta = datetime.now() - timestamp
    
    if delta.days > 0:
        return f"{delta.days} day{'s' if delta.days > 1 else ''} ago"
    elif delta.seconds > 3600:
        hours = delta.seconds // 3600
        return f"{hours} hour{'s' if hours > 1 else ''} ago"
    elif delta.seconds > 60:
        minutes = delta.seconds // 60
        return f"{minutes} minute{'s' if minutes > 1 else ''} ago"
    else:
        return "Just now"

def print_system_status():
    """Print comprehensive system status"""
    print("\n" + "="*60)
    print("🌐 UNIVERSAL TOPIC INTELLIGENCE SYSTEM STATUS")
    print("="*60)
    
    # Get all stats
    db_stats = get_database_stats()
    monitoring_stats = get_monitoring_stats()
    
    # Service Status
    print("\n📊 SERVICE STATUS")
    print("-" * 40)
    
    monitoring_status = "✅ RUNNING" if monitoring_stats.get('monitoring_active') else "🔴 STOPPED"
    dashboard_status = "✅ RUNNING" if monitoring_stats.get('dashboard_active') else "🔴 STOPPED"
    
    print(f"Monitoring Service: {monitoring_status}")
    if monitoring_stats.get('monitoring_pid'):
        print(f"  └─ PID: {monitoring_stats['monitoring_pid']}")
    
    print(f"Web Dashboard:      {dashboard_status}")
    if monitoring_stats.get('dashboard_pid'):
        print(f"  └─ PID: {monitoring_stats['dashboard_pid']}")
        print(f"  └─ URL: http://localhost:5001")
    
    # Database Statistics
    print("\n📈 DATABASE STATISTICS")
    print("-" * 40)
    print(f"Total Items:        {db_stats['total_items']:,}")
    print(f"Items (24h):        {db_stats['items_24h']:,}")
    print(f"Claude Content:     {db_stats['claude_items']:,}")
    print(f"Bookmarked:         {db_stats['bookmarked_items']:,}")
    print(f"Read Items:         {db_stats['read_items']:,}")
    
    # Priority Distribution
    print("\n🎯 PRIORITY DISTRIBUTION")
    print("-" * 40)
    priority_order = ['critical', 'high', 'medium', 'low', 'archive']
    priority_symbols = {
        'critical': '🔴',
        'high': '🟠',
        'medium': '🟡',
        'low': '🟢',
        'archive': '⚫'
    }
    
    for priority in priority_order:
        count = db_stats['items_by_priority'].get(priority, 0)
        if count > 0:
            bar_length = min(30, count // 5)
            bar = '█' * bar_length
            symbol = priority_symbols.get(priority, '⚪')
            print(f"{symbol} {priority.upper():8} {count:4} {bar}")
    
    # Top Sources
    print("\n📡 TOP CONTENT SOURCES")
    print("-" * 40)
    for i, (source, count) in enumerate(db_stats['top_sources'], 1):
        source_name = source.replace('_', ' ').title()
        print(f"{i}. {source_name[:25]:25} {count:4} items")
    
    # Monitoring Statistics
    if monitoring_stats.get('total_runs', 0) > 0:
        print("\n⚙️ MONITORING STATISTICS")
        print("-" * 40)
        print(f"Total Runs:         {monitoring_stats.get('total_runs', 0):,}")
        print(f"Successful:         {monitoring_stats.get('successful_runs', 0):,}")
        print(f"Failed:             {monitoring_stats.get('failed_runs', 0):,}")
        print(f"Items Collected:    {monitoring_stats.get('total_items_collected', 0):,}")
        
        if monitoring_stats.get('last_run'):
            last_run = format_time_ago(monitoring_stats['last_run'])
            print(f"Last Run:           {last_run}")
        
        if monitoring_stats.get('next_run') and monitoring_stats.get('monitoring_active'):
            next_run = datetime.fromisoformat(monitoring_stats['next_run'])
            if next_run > datetime.now():
                delta = next_run - datetime.now()
                minutes = delta.seconds // 60
                print(f"Next Run:           In {minutes} minutes")
    
    # Quick Actions
    print("\n🚀 QUICK ACTIONS")
    print("-" * 40)
    
    if not monitoring_stats.get('monitoring_active'):
        print("Start monitoring:   ./start_monitoring.sh")
    else:
        print("Stop monitoring:    ./stop_monitoring.sh")
        print("View logs:          tail -f monitoring.log")
    
    if not monitoring_stats.get('dashboard_active'):
        print("Start dashboard:    python dashboard_proper.py")
    else:
        print("Open dashboard:     http://localhost:5001")
    
    print("Manual refresh:     python auto_monitor.py --once")
    print("Rescore content:    python rescore_content.py")
    
    print("\n" + "="*60)
    print("System status check complete")
    print("="*60 + "\n")

if __name__ == "__main__":
    print_system_status()