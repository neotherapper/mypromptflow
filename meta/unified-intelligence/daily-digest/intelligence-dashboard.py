#!/usr/bin/env python3
"""
Intelligence Dashboard - Interactive Channel Performance Dashboard
Real-time dashboard for YouTube channel intelligence monitoring
"""

import json
import time
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
import webbrowser

class IntelligenceDashboard:
    """Interactive dashboard for channel intelligence monitoring"""
    
    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = base_path or Path(__file__).parent
        self.reports_path = self.base_path / "reports"
        self.dashboard_path = self.base_path / "dashboard"
        self.dashboard_path.mkdir(parents=True, exist_ok=True)
        
        print(f"📊 Intelligence Dashboard initialized")
        print(f"   📋 Reports path: {self.reports_path}")
        print(f"   🖥️  Dashboard path: {self.dashboard_path}")
    
    def load_latest_report(self) -> Optional[Dict[str, Any]]:
        """Load the latest intelligence report"""
        
        latest_json = self.reports_path / "latest_intelligence_report.json"
        
        if not latest_json.exists():
            print(f"⚠️  No intelligence report found. Generate one first with channel-intelligence-reports.py")
            return None
        
        try:
            with open(latest_json, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Error loading report: {e}")
            return None
    
    def generate_dashboard_html(self, report_data: Dict[str, Any]) -> str:
        """Generate interactive dashboard HTML"""
        
        agg_metrics = report_data.get('aggregate_metrics', {})
        rankings = report_data.get('performance_rankings', {})
        insights = report_data.get('aggregate_insights', [])
        recommendations = report_data.get('recommendations', [])
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Intelligence Dashboard</title>
    <link rel="stylesheet" href="/static/css/design-system.css">
    <style>
        /* Intelligence Dashboard specific overrides */
        .metric-icon {{
            font-size: var(--text-5xl);
            margin-bottom: var(--spacing-lg);
            display: block;
        }}
        
        .metric-number {{
            font-size: var(--text-5xl);
            font-weight: var(--font-weight-bold);
            background: var(--primary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: var(--spacing-sm);
        }}
        
        .metric-label {{
            color: var(--text-muted);
            font-size: var(--text-lg);
            font-weight: var(--font-weight-medium);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .insight-card {{
            background: var(--glass-light);
            border-radius: var(--radius-xl);
            padding: var(--spacing-xl);
            border-left: 4px solid var(--primary-gradient);
            backdrop-filter: blur(15px);
            margin-bottom: var(--spacing-lg);
        }}
        
        .insight-card.strength {{
            border-left: 4px solid var(--status-active);
            background: rgba(34, 197, 94, 0.1);
        }}
        
        .insight-card.opportunity {{
            border-left: 4px solid var(--status-inactive);
            background: rgba(245, 158, 11, 0.1);
        }}
        
        .insight-card.trend {{
            border-left: 4px solid #8b5cf6;
            background: rgba(139, 92, 246, 0.1);
        }}
        
        .insight-title {{
            font-size: var(--text-xl);
            font-weight: var(--font-weight-semibold);
            margin-bottom: var(--spacing-sm);
            color: var(--text-primary);
        }}
        
        .insight-description {{
            color: var(--text-secondary);
            margin-bottom: var(--spacing-lg);
            line-height: 1.6;
        }}
        
        .data-points {{
            list-style: none;
            margin-bottom: var(--spacing-lg);
            padding: 0;
        }}
        
        .data-points li {{
            background: var(--glass-lighter);
            padding: var(--spacing-sm) var(--spacing-lg);
            border-radius: var(--radius-lg);
            margin: var(--spacing-xs) 0;
            font-size: var(--text-sm);
            color: var(--text-secondary);
            backdrop-filter: blur(10px);
        }}
        
        .action-items {{
            list-style: none;
            padding: 0;
        }}
        
        .action-items li {{
            background: rgba(59,130,246,0.1);
            padding: var(--spacing-sm) var(--spacing-lg);
            border-radius: var(--radius-lg);
            margin: var(--spacing-xs) 0;
            font-size: var(--text-sm);
            color: var(--text-primary);
            border-left: 3px solid var(--primary-gradient);
            backdrop-filter: blur(10px);
        }}
        
        .ranking-section {{
            background: var(--glass-light);
            border-radius: var(--radius-xl);
            padding: var(--spacing-xl);
            backdrop-filter: blur(15px);
        }}
        .ranking-title {{
            font-size: var(--text-xl);
            font-weight: var(--font-weight-semibold);
            margin-bottom: var(--spacing-lg);
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: var(--spacing-sm);
        }}
        .ranking-list {{
            list-style: none;
        }}
        .ranking-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: var(--spacing-md) var(--spacing-lg);
            background: var(--glass-lighter);
            margin: var(--spacing-sm) 0;
            border-radius: var(--radius-lg);
            backdrop-filter: blur(10px);
            border: 1px solid var(--glass-border);
        }}
        .rank-badge {{
            background: var(--primary-gradient);
            color: var(--text-primary);
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: var(--text-sm);
            font-weight: var(--font-weight-bold);
            box-shadow: var(--shadow-sm);
        }}
        .channel-name {{
            font-weight: var(--font-weight-semibold);
            color: var(--text-primary);
        }}
        .metric-value {{
            font-weight: var(--font-weight-bold);
            color: var(--text-primary);
        }}
        .recommendation {{
            background: var(--glass-light);
            border: 1px solid var(--status-error-border);
            border-radius: var(--radius-xl);
            padding: var(--spacing-xl);
            margin: var(--spacing-lg) 0;
            backdrop-filter: blur(15px);
            border-left: 4px solid var(--status-error);
        }}
        .recommendation.medium {{
            background: rgba(245, 158, 11, 0.1);
            border-color: var(--status-inactive-border);
            border-left: 4px solid var(--status-inactive);
        }}
        .recommendation-title {{
            font-size: var(--text-xl);
            font-weight: var(--font-weight-semibold);
            margin-bottom: var(--spacing-sm);
            color: var(--text-primary);
        }}
        .refresh-btn {{
            position: fixed;
            top: var(--spacing-xl);
            right: var(--spacing-xl);
            background: var(--primary-gradient);
            color: var(--text-primary);
            border: none;
            padding: var(--spacing-md) var(--spacing-lg);
            border-radius: var(--radius-pill);
            font-weight: var(--font-weight-semibold);
            cursor: pointer;
            box-shadow: var(--shadow-lg);
            transition: all var(--transition-normal);
            z-index: 1000;
        }}
        .refresh-btn:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-xl);
        }}
        .status-indicator {{
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            background: var(--status-active);
            margin-right: var(--spacing-sm);
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
            100% {{ opacity: 1; }}
        }}
    </style>
</head>
<body>
    <div class="animated-bg"></div>
    
    <div class="container">
        <button class="refresh-btn" onclick="location.reload()">
            🔄 Refresh Dashboard
        </button>
        
        <!-- Header -->
        <header class="glass-card text-center mb-xl">
            <h1 class="heading-1">📊 YouTube Intelligence Dashboard</h1>
            <p class="text-body"><span class="status-indicator"></span>Real-time Channel Performance Monitoring</p>
        </header>
        
        <!-- Metrics Grid -->
        <div class="grid grid-auto-fit mb-xl">"""
        
        # Add metric cards
        metrics = [
            ("📺", agg_metrics.get('total_videos_tracked', 0), "Videos Tracked"),
            ("⭐", agg_metrics.get('total_high_value_videos', 0), "High-Value Videos"),
            ("📊", f"{agg_metrics.get('high_value_percentage', 0):.1f}%", "High-Value Rate"),
            ("🎯", f"{agg_metrics.get('average_quality_score', 0):.3f}", "Avg Quality Score"),
            ("📈", f"{report_data.get('channels_analyzed', 0)}/{report_data.get('total_channels_configured', 0)}", "Channels Analyzed"),
            ("🚀", f"{agg_metrics.get('average_content_frequency', 0):.1f}", "Avg Videos/Week")
        ]
        
        for icon, value, label in metrics:
            html_content += f"""
            <div class="glass-card text-center">
                <div class="metric-icon">{icon}</div>
                <div class="metric-number">{value}</div>
                <div class="metric-label">{label}</div>
            </div>"""
        
        html_content += """
        </div>
        
        <!-- Key Insights Section -->
        <section class="glass-card mb-xl">
            <h2 class="heading-2 mb-lg">🔍 Key Insights</h2>
            <div class="grid grid-auto-fit">"""
        
        # Add insights
        for insight in insights:
            html_content += f"""
            <div class="insight-card {insight.get('insight_type', 'trend')}">
                <div class="insight-title">{insight.get('title', 'Insight')}</div>
                <div class="insight-description">{insight.get('description', '')}</div>
                <ul class="data-points">"""
            
            for point in insight.get('data_points', []):
                html_content += f"<li>{point}</li>"
            
            html_content += """</ul>
                <ul class="action-items">"""
            
            for action in insight.get('action_items', []):
                html_content += f"<li>{action}</li>"
            
            html_content += "</ul></div>"
        
        html_content += """
            </div>
        </section>
        
        <!-- Performance Rankings Section -->
        <section class="glass-card mb-xl">
            <h2 class="heading-2 mb-lg">🏆 Performance Rankings</h2>
            <div class="grid grid-auto-fit">"""
        
        # Add performance rankings
        ranking_sections = [
            ("top_quality_channels", "📈 Top Quality", "score"),
            ("top_high_value_channels", "⭐ High-Value Leaders", "high_value_videos"),
            ("most_active_channels", "🚀 Most Active", "frequency")
        ]
        
        for key, title, metric in ranking_sections:
            if key in rankings and rankings[key]:
                html_content += f"""
                <div class="ranking-section">
                    <div class="ranking-title">{title}</div>
                    <ol class="ranking-list">"""
                
                for i, item in enumerate(rankings[key][:5], 1):
                    value = item.get(metric, 0)
                    if isinstance(value, float):
                        value = f"{value:.3f}"
                    
                    html_content += f"""
                    <li class="ranking-item">
                        <div style="display: flex; align-items: center; gap: 15px;">
                            <span class="rank-badge">{i}</span>
                            <span class="channel-name">{item.get('name', 'Unknown')}</span>
                        </div>
                        <span class="metric-value">{value}</span>
                    </li>"""
                
                html_content += "</ol></div>"
        
        html_content += """
            </div>
        </section>"""
        
        # Add recommendations if available
        if recommendations:
            html_content += """
        
        <!-- System Recommendations Section -->
        <section class="glass-card mb-xl">
            <h2 class="heading-2 mb-lg">💡 System Recommendations</h2>"""
            
            for rec in recommendations:
                html_content += f"""
                <div class="recommendation {rec.get('priority', 'medium')}">
                    <div class="recommendation-title">{rec.get('title', 'Recommendation')}</div>
                    <p>{rec.get('description', '')}</p>
                    <p><strong>Impact:</strong> {rec.get('impact', '')}</p>
                    <ul>"""
                
                for action in rec.get('action_items', []):
                    html_content += f"<li>{action}</li>"
                
                html_content += "</ul></div>"
            
            html_content += "</section>"
        
        # Add footer
        generated_at = report_data.get('generated_at', '')
        if generated_at:
            try:
                dt = datetime.fromisoformat(generated_at.replace('Z', '+00:00'))
                formatted_time = dt.strftime('%B %d, %Y at %H:%M UTC')
            except:
                formatted_time = generated_at
        else:
            formatted_time = "Unknown"
        
        html_content += f"""
        
        <div class="text-center mt-xl">
            <p class="text-small text-muted">
                📊 Dashboard generated from report created on <span data-timestamp="{report_data.get('generated_at', '')}" data-format="display">{formatted_time}</span><br>
                Analysis completed in {report_data.get('analysis_time_seconds', 0):.2f} seconds | Unified Intelligence System
            </p>
        </div>
    </div>
    
    <script src="/static/js/time-formatter.js"></script>
    <script>
        // Auto-refresh every 5 minutes
        setTimeout(() => {{
            location.reload();
        }}, 300000);
        
        // Add loading animation for refresh button
        document.querySelector('.refresh-btn').addEventListener('click', function() {{
            this.innerHTML = '⏳ Refreshing...';
            this.style.pointerEvents = 'none';
        }});
        
        // Initialize time formatter after page load
        document.addEventListener('DOMContentLoaded', function() {{
            if (window.timeFormatter) {{
                window.timeFormatter.updateAllTimestamps();
            }}
        }});
    </script>
</body>
</html>"""
        
        return html_content
    
    def create_dashboard(self) -> Optional[str]:
        """Create interactive dashboard"""
        
        print(f"🖥️  Creating Intelligence Dashboard...")
        
        # Load latest report
        report_data = self.load_latest_report()
        if not report_data:
            return None
        
        # Generate dashboard HTML
        dashboard_html = self.generate_dashboard_html(report_data)
        
        # Save dashboard
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        dashboard_file = self.dashboard_path / f"intelligence_dashboard_{timestamp}.html"
        
        with open(dashboard_file, 'w') as f:
            f.write(dashboard_html)
        
        # Create latest dashboard symlink
        latest_dashboard = self.dashboard_path / "latest_dashboard.html"
        if latest_dashboard.exists():
            latest_dashboard.unlink()
        
        try:
            latest_dashboard.symlink_to(dashboard_file.name)
        except:
            # Fallback: copy file if symlink fails
            import shutil
            shutil.copy2(dashboard_file, latest_dashboard)
        
        print(f"✅ Dashboard created successfully:")
        print(f"   🖥️  Dashboard: {dashboard_file}")
        print(f"   🔗 Latest: {latest_dashboard}")
        
        return str(latest_dashboard)
    
    def launch_dashboard(self) -> bool:
        """Launch dashboard in browser"""
        
        dashboard_file = self.create_dashboard()
        if not dashboard_file:
            return False
        
        try:
            webbrowser.open(f"file://{Path(dashboard_file).absolute()}")
            print(f"🌐 Dashboard opened in browser")
            return True
        except Exception as e:
            print(f"❌ Could not open browser: {e}")
            print(f"📄 Dashboard available at: {dashboard_file}")
            return False

def main():
    """Launch intelligence dashboard"""
    
    print("🖥️  Intelligence Dashboard")
    print("=" * 50)
    
    # Initialize dashboard
    dashboard = IntelligenceDashboard()
    
    # Launch dashboard
    success = dashboard.launch_dashboard()
    
    if success:
        print(f"\n🎯 Dashboard launched successfully!")
        print(f"   • Real-time channel performance monitoring")
        print(f"   • Interactive insights and recommendations")
        print(f"   • Auto-refresh every 5 minutes")
    else:
        print(f"\n❌ Could not launch dashboard")
        print(f"   • Generate a report first: python3 channel-intelligence-reports.py")
    
    return success

if __name__ == "__main__":
    main()