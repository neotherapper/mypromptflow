#!/usr/bin/env python3
"""
Email Digest Feature for Universal Topic Intelligence System
Generates and sends daily/weekly digests of top content
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

logger = logging.getLogger(__name__)

class EmailDigestGenerator:
    """Generate email digests of collected content"""
    
    def __init__(self, db_path: str = "topic_intelligence.db"):
        self.db_path = db_path
        self.logger = logging.getLogger("EmailDigest")
    
    def generate_digest(self, 
                       period: str = "daily",
                       min_priority: str = "high",
                       max_items: int = 20) -> Dict[str, Any]:
        """
        Generate a digest of top content
        
        Args:
            period: "daily", "weekly", or "hourly"
            min_priority: Minimum priority level to include
            max_items: Maximum number of items to include
            
        Returns:
            Digest data dictionary
        """
        # Calculate time range
        now = datetime.now()
        if period == "hourly":
            since = now - timedelta(hours=1)
            period_label = "Past Hour"
        elif period == "daily":
            since = now - timedelta(days=1)
            period_label = "Today"
        elif period == "weekly":
            since = now - timedelta(days=7)
            period_label = "This Week"
        else:
            since = now - timedelta(days=1)
            period_label = "Today"
        
        # Get content from database
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get Claude-specific content (remove time filter for now)
        query = """
            SELECT * FROM content_items 
            WHERE priority_level IN ('critical', 'high')
            AND (
                LOWER(title) LIKE '%claude%' OR 
                LOWER(title) LIKE '%anthropic%' OR
                LOWER(title) LIKE '%opus%'
            )
            ORDER BY priority_score DESC, published_date DESC
            LIMIT ?
        """
        
        cursor.execute(query, (max_items // 2,))
        claude_items = [dict(row) for row in cursor.fetchall()]
        
        # Get other high-priority content
        query = """
            SELECT * FROM content_items 
            WHERE priority_level IN ('critical', 'high')
            AND item_id NOT IN (
                SELECT item_id FROM content_items 
                WHERE LOWER(title) LIKE '%claude%' 
                OR LOWER(title) LIKE '%anthropic%'
            )
            ORDER BY priority_score DESC, published_date DESC
            LIMIT ?
        """
        
        cursor.execute(query, (max_items // 2,))
        other_items = [dict(row) for row in cursor.fetchall()]
        
        # Get statistics (for all items)
        cursor.execute("""
            SELECT COUNT(*) as total,
                   SUM(CASE WHEN priority_level = 'critical' THEN 1 ELSE 0 END) as critical,
                   SUM(CASE WHEN priority_level = 'high' THEN 1 ELSE 0 END) as high
            FROM content_items
        """)
        
        stats = dict(cursor.fetchone())
        
        # Get top sources
        cursor.execute("""
            SELECT source_id, COUNT(*) as count
            FROM content_items
            GROUP BY source_id
            ORDER BY count DESC
            LIMIT 5
        """)
        
        top_sources = cursor.fetchall()
        
        conn.close()
        
        # Build digest data
        digest = {
            "period": period,
            "period_label": period_label,
            "generated_at": now.isoformat(),
            "stats": {
                "total_items": stats['total'],
                "critical_items": stats['critical'],
                "high_items": stats['high'],
                "included_items": len(claude_items) + len(other_items)
            },
            "claude_content": claude_items,
            "other_content": other_items,
            "top_sources": [{"source": s[0], "count": s[1]} for s in top_sources]
        }
        
        return digest
    
    def format_html_digest(self, digest: Dict[str, Any]) -> str:
        """Format digest as HTML email"""
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #1f2937;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: #f9fafb;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 28px;
        }}
        .header p {{
            margin: 10px 0 0 0;
            opacity: 0.9;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .stat-value {{
            font-size: 32px;
            font-weight: bold;
            color: #5145e0;
        }}
        .stat-label {{
            font-size: 14px;
            color: #6b7280;
            margin-top: 5px;
        }}
        .section {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .section h2 {{
            margin-top: 0;
            color: #1f2937;
            border-bottom: 2px solid #e5e7eb;
            padding-bottom: 10px;
        }}
        .item {{
            padding: 15px;
            border-left: 4px solid #e5e7eb;
            margin-bottom: 15px;
            background: #f9fafb;
            border-radius: 0 8px 8px 0;
            transition: all 0.2s;
        }}
        .item.critical {{
            border-left-color: #ef4444;
        }}
        .item.high {{
            border-left-color: #f59e0b;
        }}
        .item.claude {{
            border-left-color: #8b5cf6;
            background: #faf5ff;
        }}
        .item-title {{
            font-weight: 600;
            color: #1f2937;
            margin-bottom: 5px;
            font-size: 16px;
        }}
        .item-meta {{
            font-size: 13px;
            color: #6b7280;
            margin-bottom: 8px;
        }}
        .item-link {{
            display: inline-block;
            color: #5145e0;
            text-decoration: none;
            font-size: 14px;
            margin-top: 8px;
        }}
        .item-link:hover {{
            text-decoration: underline;
        }}
        .priority-badge {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            margin-left: 8px;
        }}
        .priority-critical {{
            background: #fee2e2;
            color: #dc2626;
        }}
        .priority-high {{
            background: #fed7aa;
            color: #ea580c;
        }}
        .footer {{
            text-align: center;
            color: #6b7280;
            font-size: 14px;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #e5e7eb;
        }}
        .claude-special {{
            background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
            color: white;
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        .claude-special h3 {{
            margin: 0 0 10px 0;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🌐 Universal Topic Intelligence</h1>
        <p>{digest['period_label']} Digest - {datetime.now().strftime('%B %d, %Y')}</p>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <div class="stat-value">{digest['stats']['total_items']}</div>
            <div class="stat-label">Total Items</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{digest['stats']['critical_items']}</div>
            <div class="stat-label">Critical</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{digest['stats']['high_items']}</div>
            <div class="stat-label">High Priority</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{len(digest['claude_content'])}</div>
            <div class="stat-label">Claude Items</div>
        </div>
    </div>
"""
        
        # Add Claude content section if available
        if digest['claude_content']:
            html += """
    <div class="section">
        <h2>🤖 Claude & Anthropic Updates</h2>
        <div class="claude-special">
            <h3>Priority Claude Content</h3>
            <p>Latest updates about Claude, Anthropic, and Opus models</p>
        </div>
"""
            for item in digest['claude_content'][:5]:
                priority = item.get('priority_level', 'medium')
                html += f"""
        <div class="item claude {priority}">
            <div class="item-title">
                {item['title']}
                <span class="priority-badge priority-{priority}">{priority}</span>
            </div>
            <div class="item-meta">
                {item.get('source_id', 'Unknown Source')} • 
                Score: {item.get('priority_score', 0):.2f}
            </div>
            <a href="{item.get('url', '#')}" class="item-link">Read More →</a>
        </div>
"""
            html += "    </div>\n"
        
        # Add other high-priority content
        if digest['other_content']:
            html += """
    <div class="section">
        <h2>📊 High Priority Content</h2>
"""
            for item in digest['other_content'][:10]:
                priority = item.get('priority_level', 'medium')
                html += f"""
        <div class="item {priority}">
            <div class="item-title">
                {item['title']}
                <span class="priority-badge priority-{priority}">{priority}</span>
            </div>
            <div class="item-meta">
                {item.get('source_id', 'Unknown Source')} • 
                Score: {item.get('priority_score', 0):.2f}
            </div>
            <a href="{item.get('url', '#')}" class="item-link">Read More →</a>
        </div>
"""
            html += "    </div>\n"
        
        # Add footer
        html += f"""
    <div class="footer">
        <p>📡 Top Sources: {', '.join([s['source'] for s in digest['top_sources'][:3]])}</p>
        <p>Generated by Universal Topic Intelligence System</p>
        <p><a href="http://localhost:5001" style="color: #5145e0;">View Full Dashboard</a></p>
    </div>
</body>
</html>
"""
        
        return html
    
    def save_digest(self, digest: Dict[str, Any], output_path: str = None):
        """Save digest to file"""
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"digests/digest_{timestamp}.html"
        
        # Create directory if needed
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        
        # Generate and save HTML
        html = self.format_html_digest(digest)
        with open(output_path, 'w') as f:
            f.write(html)
        
        self.logger.info(f"Digest saved to {output_path}")
        return output_path


def generate_daily_digest():
    """Generate and save daily digest"""
    generator = EmailDigestGenerator()
    digest = generator.generate_digest(period="daily")
    
    print("📧 Daily Digest Generated")
    print("=" * 50)
    print(f"Total items: {digest['stats']['total_items']}")
    print(f"Critical items: {digest['stats']['critical_items']}")
    print(f"High priority items: {digest['stats']['high_items']}")
    print(f"Claude content: {len(digest['claude_content'])} items")
    print(f"Other content: {len(digest['other_content'])} items")
    
    # Save to file
    output_path = generator.save_digest(digest)
    print(f"\n✅ Digest saved to: {output_path}")
    
    return digest, output_path


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    # Generate test digest
    digest, path = generate_daily_digest()
    
    print(f"\n🌐 Open digest in browser:")
    print(f"   file://{Path(path).absolute()}")