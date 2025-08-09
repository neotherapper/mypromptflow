#!/usr/bin/env python3
"""
Unified Intelligence Command Center
MVP centralized dashboard for all intelligence systems
"""

import json
import os
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from threading import Thread
import webbrowser
from dataclasses import dataclass, asdict
import mimetypes

@dataclass
class SystemStatus:
    """System component status"""
    name: str
    status: str  # "active", "inactive", "error", "unknown"
    last_update: str  # ISO timestamp - let frontend handle formatting
    health_score: float
    description: str
    quick_actions: List[str]

@dataclass 
class QuickAction:
    """Quick action definition"""
    id: str
    title: str
    description: str
    endpoint: str
    icon: str
    priority: int

class SystemStatusMonitor:
    """Monitor status of all intelligence systems"""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.data_path = base_path / "data"
        self.reports_path = base_path / "reports"
        self.trends_path = base_path / "trends"
        self.generated_path = base_path / "generated"
        self.config_path = base_path / "config"
        
    def get_system_status(self) -> Dict[str, SystemStatus]:
        """Get comprehensive system status"""
        
        systems = {}
        
        # YouTube Intelligence System
        systems["youtube_intelligence"] = self._check_youtube_intelligence()
        
        # YouTube RSS System  
        systems["youtube_rss"] = self._check_youtube_rss()
        
        # Content Digest System
        systems["content_digest"] = self._check_content_digest()
        
        # Trend Analysis System
        systems["trend_analysis"] = self._check_trend_analysis()
        
        # Reddit Discovery System
        systems["reddit_discovery"] = self._check_reddit_discovery()
        
        return systems
    
    def _check_youtube_intelligence(self) -> SystemStatus:
        """Check YouTube Intelligence System status"""
        
        try:
            # Check for recent intelligence reports
            latest_report = self.reports_path / "latest_intelligence_report.json"
            dashboard_path = self.base_path / "dashboard" / "latest_dashboard.html"
            
            if latest_report.exists():
                with open(latest_report, 'r') as f:
                    report_data = json.load(f)
                
                generated_at = report_data.get('generated_at', '')
                channels_analyzed = report_data.get('channels_analyzed', 0)
                total_configured = report_data.get('total_channels_configured', 0)
                
                # Calculate health score
                health_score = min(channels_analyzed / max(total_configured, 1), 1.0)
                
                status = "active" if health_score > 0.5 else "inactive"
                
                return SystemStatus(
                    name="YouTube Intelligence",
                    status=status,
                    last_update=generated_at or datetime.now(timezone.utc).isoformat(),
                    health_score=health_score,
                    description=f"{channels_analyzed}/{total_configured} channels analyzed",
                    quick_actions=["generate_report", "view_dashboard", "view_trends"]
                )
            else:
                return SystemStatus(
                    name="YouTube Intelligence",
                    status="inactive",
                    last_update="never",
                    health_score=0.0,
                    description="No intelligence reports found",
                    quick_actions=["generate_report"]
                )
                
        except Exception as e:
            return SystemStatus(
                name="YouTube Intelligence", 
                status="error",
                last_update="error",
                health_score=0.0,
                description=f"Error: {e}",
                quick_actions=[]
            )
    
    def _check_youtube_rss(self) -> SystemStatus:
        """Check YouTube RSS System status"""
        
        try:
            config_file = self.config_path / "youtube-rss-channels.json"
            rss_data_path = self.data_path / "rss-feeds"
            
            if not config_file.exists():
                return SystemStatus(
                    name="YouTube RSS Feeds",
                    status="inactive",
                    last_update="never",
                    health_score=0.0,
                    description="No RSS configuration found",
                    quick_actions=[]
                )
            
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            total_channels = config.get('metadata', {}).get('total_channels', 0)
            
            # Check for recent RSS data
            active_channels = 0
            latest_update = None
            
            if rss_data_path.exists():
                for channel_dir in rss_data_path.iterdir():
                    if channel_dir.is_dir():
                        latest_file = channel_dir / "latest.json"
                        if latest_file.exists():
                            active_channels += 1
                            mtime = datetime.fromtimestamp(latest_file.stat().st_mtime, tz=timezone.utc)
                            if latest_update is None or mtime > latest_update:
                                latest_update = mtime
            
            if latest_update:
                last_update_str = latest_update.isoformat()
            else:
                last_update_str = "never"
            
            health_score = active_channels / max(total_channels, 1)
            status = "active" if health_score > 0.3 else "inactive"
            
            return SystemStatus(
                name="YouTube RSS Feeds",
                status=status,
                last_update=last_update_str,
                health_score=health_score,
                description=f"{active_channels}/{total_channels} channels active",
                quick_actions=["run_rss_collection", "view_config"]
            )
            
        except Exception as e:
            return SystemStatus(
                name="YouTube RSS Feeds",
                status="error", 
                last_update="error",
                health_score=0.0,
                description=f"Error: {e}",
                quick_actions=[]
            )
    
    def _check_content_digest(self) -> SystemStatus:
        """Check Content Digest System status"""
        
        try:
            digest_path = self.generated_path / "content" 
            latest_digest = digest_path / "daily-digest.json"
            
            if latest_digest.exists():
                with open(latest_digest, 'r') as f:
                    digest_data = json.load(f)
                
                generated_at = digest_data.get('generated_at', '')
                total_content = len(digest_data.get('content_items', []))
                sources_used = digest_data.get('sources_summary', {})
                
                health_score = min(total_content / 10, 1.0)  # Expect at least 10 items
                status = "active" if health_score > 0.3 else "inactive"
                
                source_count = len([s for s in sources_used.values() if s > 0])
                
                return SystemStatus(
                    name="Content Digest",
                    status=status,
                    last_update=generated_at or datetime.now(timezone.utc).isoformat(),
                    health_score=health_score,
                    description=f"{total_content} items from {source_count} sources",
                    quick_actions=["generate_digest", "view_digest"]
                )
            else:
                return SystemStatus(
                    name="Content Digest",
                    status="inactive",
                    last_update="never",
                    health_score=0.0,
                    description="No digest found",
                    quick_actions=["generate_digest"]
                )
                
        except Exception as e:
            return SystemStatus(
                name="Content Digest",
                status="error",
                last_update="error", 
                health_score=0.0,
                description=f"Error: {e}",
                quick_actions=[]
            )
    
    def _check_trend_analysis(self) -> SystemStatus:
        """Check Trend Analysis System status"""
        
        try:
            latest_trend = self.trends_path / "latest_trend_analysis.json"
            
            if latest_trend.exists():
                with open(latest_trend, 'r') as f:
                    trend_data = json.load(f)
                
                generated_at = trend_data.get('generated_at', '')
                reports_analyzed = trend_data.get('reports_analyzed', 0)
                recommendations = len(trend_data.get('strategic_recommendations', []))
                
                health_score = min(reports_analyzed / 5, 1.0)  # Expect at least 5 reports
                status = "active" if health_score > 0.2 else "inactive"
                
                return SystemStatus(
                    name="Trend Analysis",
                    status=status,
                    last_update=generated_at or datetime.now(timezone.utc).isoformat(),
                    health_score=health_score,
                    description=f"{reports_analyzed} reports analyzed, {recommendations} recommendations",
                    quick_actions=["run_trend_analysis", "view_trends"]
                )
            else:
                return SystemStatus(
                    name="Trend Analysis",
                    status="inactive",
                    last_update="never",
                    health_score=0.0,
                    description="No trend analysis found",
                    quick_actions=["run_trend_analysis"]
                )
                
        except Exception as e:
            return SystemStatus(
                name="Trend Analysis",
                status="error",
                last_update="error",
                health_score=0.0,
                description=f"Error: {e}",
                quick_actions=[]
            )
    
    def _check_reddit_discovery(self) -> SystemStatus:
        """Check Reddit Discovery System status"""
        
        # For now, this is part of the content digest
        # In Phase 2, we'll make this a standalone system
        
        try:
            digest_path = self.generated_path / "content" / "daily-digest.json"
            
            if digest_path.exists():
                with open(digest_path, 'r') as f:
                    digest_data = json.load(f)
                
                sources_summary = digest_data.get('sources_summary', {})
                reddit_items = sources_summary.get('reddit_discovery', 0)
                
                if reddit_items > 0:
                    status = "active"
                    health_score = min(reddit_items / 5, 1.0)
                    description = f"{reddit_items} Reddit items discovered"
                else:
                    status = "inactive"
                    health_score = 0.0
                    description = "No Reddit content found"
                
                generated_at = digest_data.get('generated_at', '')
                
                return SystemStatus(
                    name="Reddit Discovery",
                    status=status,
                    last_update=generated_at or datetime.now(timezone.utc).isoformat(),
                    health_score=health_score,
                    description=description,
                    quick_actions=["configure_reddit"] if status == "inactive" else ["view_reddit_config"]
                )
            else:
                return SystemStatus(
                    name="Reddit Discovery",
                    status="inactive",
                    last_update="never",
                    health_score=0.0,
                    description="Reddit discovery not configured",
                    quick_actions=["configure_reddit"]
                )
                
        except Exception as e:
            return SystemStatus(
                name="Reddit Discovery",
                status="error",
                last_update="error",
                health_score=0.0,
                description=f"Error: {e}",
                quick_actions=[]
            )

class IntelligenceAssistant:
    """AI assistant for conversational system management"""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.config_path = base_path / "config"
        
    def handle_request(self, user_input: str) -> Dict[str, Any]:
        """Handle conversational requests"""
        
        user_input = user_input.lower().strip()
        
        # Add YouTube channel
        if "add" in user_input and ("channel" in user_input or "youtube" in user_input):
            return self._handle_add_channel(user_input)
        
        # Remove YouTube channel  
        elif "remove" in user_input and ("channel" in user_input or "youtube" in user_input):
            return self._handle_remove_channel(user_input)
        
        # Show system status
        elif "status" in user_input or "health" in user_input:
            return self._handle_status_request()
        
        # Generate reports
        elif "generate" in user_input and "report" in user_input:
            return self._handle_generate_report()
        
        # Default response
        else:
            return {
                "success": False,
                "message": "I can help you with:\n• Add/remove YouTube channels\n• Check system status\n• Generate intelligence reports\n• Configure system settings",
                "suggestions": [
                    "Add [channel name] to monitoring",
                    "Show system status",
                    "Generate intelligence report"
                ]
            }
    
    def _handle_add_channel(self, user_input: str) -> Dict[str, Any]:
        """Handle add channel request"""
        
        # For MVP, return instructions for manual addition
        # In future versions, this could use YouTube API to search and add
        
        return {
            "success": True,
            "message": "To add a YouTube channel:\n1. Find the channel's URL\n2. Extract the channel ID (after /channel/ or /c/)\n3. I'll help configure priority and categories\n\nExample: 'Add channel UCxxxxxx with high priority for AI topics'",
            "action": "channel_add_instructions",
            "next_steps": [
                "Provide channel URL or ID",
                "Specify priority level (1-5)",
                "Set topic categories"
            ]
        }
    
    def _handle_remove_channel(self, user_input: str) -> Dict[str, Any]:
        """Handle remove channel request"""
        
        try:
            config_file = self.config_path / "youtube-rss-channels.json"
            if config_file.exists():
                with open(config_file, 'r') as f:
                    config = json.load(f)
                
                channels = [ch['name'] for ch in config.get('channels', [])]
                
                return {
                    "success": True,
                    "message": f"Available channels to remove:\n" + "\n".join([f"• {ch}" for ch in channels[:10]]),
                    "action": "channel_remove_options",
                    "channels": channels
                }
            else:
                return {
                    "success": False,
                    "message": "No YouTube channel configuration found",
                    "action": "config_missing"
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Error accessing channel configuration: {e}",
                "action": "error"
            }
    
    def _handle_status_request(self) -> Dict[str, Any]:
        """Handle system status request"""
        
        monitor = SystemStatusMonitor(self.base_path)
        systems = monitor.get_system_status()
        
        active_systems = [name for name, status in systems.items() if status.status == "active"]
        inactive_systems = [name for name, status in systems.items() if status.status == "inactive"]
        error_systems = [name for name, status in systems.items() if status.status == "error"]
        
        message = f"System Status Summary:\n"
        message += f"✅ Active: {len(active_systems)} systems\n"
        message += f"⚠️  Inactive: {len(inactive_systems)} systems\n"
        message += f"❌ Errors: {len(error_systems)} systems\n"
        
        if active_systems:
            message += f"\nActive Systems: {', '.join(active_systems)}"
        
        return {
            "success": True,
            "message": message,
            "action": "status_summary",
            "systems": {name: asdict(status) for name, status in systems.items()}
        }
    
    def _handle_generate_report(self) -> Dict[str, Any]:
        """Handle generate report request"""
        
        return {
            "success": True,
            "message": "I can help generate these reports:\n• YouTube Intelligence Report\n• Trend Analysis Report\n• Content Digest\n\nWhich would you like to generate?",
            "action": "report_options",
            "options": [
                {"id": "intelligence", "name": "YouTube Intelligence Report", "description": "Comprehensive channel analysis"},
                {"id": "trends", "name": "Trend Analysis Report", "description": "Historical performance trends"},
                {"id": "digest", "name": "Content Digest", "description": "Latest content from all sources"}
            ]
        }

# Global instances
base_path = Path(__file__).parent
status_monitor = SystemStatusMonitor(base_path)
ai_assistant = IntelligenceAssistant(base_path)

class UnifiedDashboardHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the unified dashboard"""
    
    def do_GET(self):
        """Handle GET requests"""
        try:
            parsed_path = urlparse(self.path)
            path = parsed_path.path
            
            if path == '/' or path == '/index.html':
                self.serve_dashboard()
            elif path == '/api/status':
                self.serve_status_api()
            elif path.startswith('/api/quick-action/'):
                action_id = path.split('/')[-1]
                self.serve_quick_action(action_id)
            elif path.startswith('/reports/'):
                filename = path.split('/')[-1]
                self.serve_file('reports', filename)
            elif path.startswith('/dashboard/'):
                filename = path.split('/')[-1]
                self.serve_file('dashboard', filename)
            elif path.startswith('/trends/'):
                filename = path.split('/')[-1]
                self.serve_file('trends', filename)
            elif path.startswith('/static/'):
                # Handle static files (CSS, JS)
                file_path = path[1:]  # Remove leading slash
                self.serve_static_file(file_path)
            elif path.startswith('/generated/'):
                # Handle nested paths for generated content
                sub_path = path[11:]  # Remove '/generated/'
                self.serve_generated_file(sub_path)
            else:
                self.send_error(404, "File not found")
        except Exception as e:
            self.send_error(500, f"Server error: {e}")
    
    def do_POST(self):
        """Handle POST requests"""
        try:
            parsed_path = urlparse(self.path)
            path = parsed_path.path
            
            if path == '/api/assistant':
                self.serve_assistant_api()
            else:
                self.send_error(404, "Endpoint not found")
        except Exception as e:
            self.send_error(500, f"Server error: {e}")
    
    def serve_dashboard(self):
        """Serve the main dashboard HTML"""
        try:
            dashboard_file = base_path / "templates" / "dashboard.html"
            with open(dashboard_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except Exception as e:
            self.send_error(500, f"Error serving dashboard: {e}")
    
    def serve_status_api(self):
        """Serve system status API"""
        try:
            systems = status_monitor.get_system_status()
            response_data = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "systems": {name: asdict(status) for name, status in systems.items()}
            }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        except Exception as e:
            self.send_error(500, f"Error getting system status: {e}")
    
    def serve_assistant_api(self):
        """Serve AI assistant API"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            user_input = data.get('message', '')
            if not user_input:
                response = {
                    "success": False,
                    "message": "No message provided"
                }
            else:
                response = ai_assistant.handle_request(user_input)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        except Exception as e:
            self.send_error(500, f"Error processing assistant request: {e}")
    
    def serve_quick_action(self, action_id):
        """Handle quick actions"""
        try:
            if action_id == "generate_report":
                response = {
                    "success": True,
                    "message": "Intelligence report generation initiated",
                    "redirect": "/reports/latest_intelligence_report.html"
                }
            elif action_id == "view_dashboard":
                response = {
                    "success": True,
                    "message": "Opening intelligence dashboard",
                    "redirect": "/dashboard/latest_dashboard.html"
                }
            elif action_id == "view_trends":
                response = {
                    "success": True,
                    "message": "Opening trend analysis",
                    "redirect": "/trends/latest_trend_analysis.json"
                }
            else:
                response = {
                    "success": False,
                    "message": f"Unknown action: {action_id}"
                }
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode('utf-8'))
        except Exception as e:
            self.send_error(500, f"Error handling quick action: {e}")
    
    def serve_file(self, directory, filename):
        """Serve files from specified directory"""
        try:
            file_path = base_path / directory / filename
            if not file_path.exists():
                self.send_error(404, f"File not found: {filename}")
                return
            
            # Determine content type
            content_type, _ = mimetypes.guess_type(str(file_path))
            if content_type is None:
                content_type = 'application/octet-stream'
            
            with open(file_path, 'rb') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, f"Error serving file: {e}")
    
    def serve_static_file(self, file_path):
        """Serve static files (CSS, JS, images)"""
        try:
            full_path = base_path / file_path
            if not full_path.exists():
                self.send_error(404, f"Static file not found: {file_path}")
                return
            
            # Determine content type
            content_type, _ = mimetypes.guess_type(str(full_path))
            if content_type is None:
                if file_path.endswith('.css'):
                    content_type = 'text/css'
                elif file_path.endswith('.js'):
                    content_type = 'application/javascript'
                else:
                    content_type = 'application/octet-stream'
            
            with open(full_path, 'r' if content_type.startswith('text/') or content_type == 'application/javascript' else 'rb') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Cache-Control', 'public, max-age=3600')  # Cache for 1 hour
            self.end_headers()
            
            if isinstance(content, str):
                self.wfile.write(content.encode('utf-8'))
            else:
                self.wfile.write(content)
                
        except Exception as e:
            self.send_error(500, f"Error serving static file: {e}")

    def serve_generated_file(self, sub_path):
        """Serve files from generated directory with nested paths"""
        try:
            file_path = base_path / "generated" / sub_path
            if not file_path.exists():
                self.send_error(404, f"Generated file not found: {sub_path}")
                return
            
            # Determine content type
            content_type, _ = mimetypes.guess_type(str(file_path))
            if content_type is None:
                content_type = 'application/octet-stream'
            
            with open(file_path, 'rb') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            self.send_error(500, f"Error serving generated file: {e}")
    
    def log_message(self, format, *args):
        """Override to reduce logging noise"""
        pass

def main():
    """Run the unified command center"""
    
    print("🚀 Unified Intelligence Command Center")
    print("=" * 60)
    
    # Create necessary directories
    templates_dir = base_path / "templates"
    static_dir = base_path / "static"
    templates_dir.mkdir(exist_ok=True)
    static_dir.mkdir(exist_ok=True)
    
    port = 8080
    print(f"📊 Dashboard will be available at: http://localhost:{port}")
    print(f"🎯 Base path: {base_path}")
    print(f"📈 Monitoring systems...")
    
    # Get initial status
    systems = status_monitor.get_system_status()
    active_count = sum(1 for s in systems.values() if s.status == "active")
    
    print(f"✅ {active_count}/{len(systems)} systems active")
    
    # Auto-open browser after a short delay
    def open_browser():
        time.sleep(3)
        webbrowser.open(f'http://localhost:{port}')
    
    browser_thread = Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Start HTTP server
    try:
        server = HTTPServer(('localhost', port), UnifiedDashboardHandler)
        print(f"🌐 Server started on http://localhost:{port}")
        print("Press Ctrl+C to stop the server")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        server.shutdown()
    except Exception as e:
        print(f"❌ Server error: {e}")

if __name__ == "__main__":
    main()