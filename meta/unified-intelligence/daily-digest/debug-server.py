#!/usr/bin/env python3
"""
Debug version of the unified command center to identify issues
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
import traceback

# Import the classes we need
import sys
sys.path.append(str(Path(__file__).parent))

try:
    from unified_command_center import SystemStatusMonitor, IntelligenceAssistant, base_path
except ImportError:
    # If that fails, create minimal versions for debugging
    print("⚠️  Could not import main classes, using debug versions")
    
    @dataclass
    class SystemStatus:
        name: str
        status: str
        last_update: str
        health_score: float
        description: str
        quick_actions: List[str]
    
    class SystemStatusMonitor:
        def __init__(self, base_path):
            self.base_path = base_path
        
        def get_system_status(self):
            return {
                "test_system": SystemStatus(
                    name="Test System",
                    status="active",
                    last_update="2025-08-01T12:00:00Z",
                    health_score=0.8,
                    description="Debug test system",
                    quick_actions=["test_action"]
                )
            }
    
    class IntelligenceAssistant:
        def __init__(self, base_path):
            self.base_path = base_path
        
        def handle_request(self, user_input):
            return {
                "success": True,
                "message": f"Debug response to: {user_input}",
                "action": "debug"
            }
    
    base_path = Path(__file__).parent

# Create instances
status_monitor = SystemStatusMonitor(base_path)
ai_assistant = IntelligenceAssistant(base_path)

class DebugDashboardHandler(BaseHTTPRequestHandler):
    """Debug HTTP request handler"""
    
    def do_GET(self):
        """Handle GET requests with detailed logging"""
        print(f"📥 GET request: {self.path}")
        
        try:
            parsed_path = urlparse(self.path)
            path = parsed_path.path
            
            print(f"   Parsed path: {path}")
            
            if path == '/' or path == '/index.html':
                print("   → Serving dashboard")
                self.serve_dashboard()
            elif path == '/api/status':
                print("   → Serving status API")
                self.serve_status_api()
            elif path.startswith('/api/quick-action/'):
                action_id = path.split('/')[-1]
                print(f"   → Quick action: {action_id}")
                self.serve_quick_action(action_id)
            else:
                print(f"   → Path not found: {path}")
                self.send_error(404, f"Path not found: {path}")
                
        except Exception as e:
            print(f"❌ Error in do_GET: {e}")
            traceback.print_exc()
            self.send_error(500, f"Server error: {e}")
    
    def do_POST(self):
        """Handle POST requests with detailed logging"""
        print(f"📤 POST request: {self.path}")
        
        try:
            parsed_path = urlparse(self.path)
            path = parsed_path.path
            
            if path == '/api/assistant':
                print("   → Serving assistant API")
                self.serve_assistant_api()
            else:
                print(f"   → POST path not found: {path}")
                self.send_error(404, f"POST endpoint not found: {path}")
                
        except Exception as e:
            print(f"❌ Error in do_POST: {e}")
            traceback.print_exc()
            self.send_error(500, f"Server error: {e}")
    
    def serve_dashboard(self):
        """Serve the main dashboard HTML with debugging"""
        try:
            dashboard_file = base_path / "templates" / "dashboard.html"
            print(f"   Dashboard file: {dashboard_file}")
            print(f"   File exists: {dashboard_file.exists()}")
            
            if not dashboard_file.exists():
                self.send_error(404, f"Dashboard file not found: {dashboard_file}")
                return
            
            with open(dashboard_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"   Content length: {len(content)} characters")
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
            
            print("   ✅ Dashboard served successfully")
            
        except Exception as e:
            print(f"   ❌ Error serving dashboard: {e}")
            traceback.print_exc()
            self.send_error(500, f"Error serving dashboard: {e}")
    
    def serve_status_api(self):
        """Serve system status API with debugging"""
        try:
            print("   Getting system status...")
            systems = status_monitor.get_system_status()
            print(f"   Found {len(systems)} systems")
            
            response_data = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "systems": {name: asdict(status) for name, status in systems.items()}
            }
            
            json_data = json.dumps(response_data)
            print(f"   Response length: {len(json_data)} characters")
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(json_data.encode('utf-8'))
            
            print("   ✅ Status API served successfully")
            
        except Exception as e:
            print(f"   ❌ Error serving status API: {e}")
            traceback.print_exc()
            self.send_error(500, f"Error getting system status: {e}")
    
    def serve_assistant_api(self):
        """Serve AI assistant API with debugging"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            print(f"   Content length: {content_length}")
            
            if content_length > 0:
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                print(f"   Received data: {data}")
            else:
                data = {}
            
            user_input = data.get('message', '')
            print(f"   User input: {user_input}")
            
            if not user_input:
                response = {
                    "success": False,
                    "message": "No message provided"
                }
            else:
                response = ai_assistant.handle_request(user_input)
            
            json_data = json.dumps(response)
            print(f"   Response: {json_data[:100]}...")
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Cache-Control', 'no-cache')
            self.end_headers()
            self.wfile.write(json_data.encode('utf-8'))
            
            print("   ✅ Assistant API served successfully")
            
        except Exception as e:
            print(f"   ❌ Error serving assistant API: {e}")
            traceback.print_exc()
            self.send_error(500, f"Error processing assistant request: {e}")
    
    def serve_quick_action(self, action_id):
        """Handle quick actions with debugging"""
        try:
            print(f"   Quick action: {action_id}")
            
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
            
            json_data = json.dumps(response)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json_data.encode('utf-8'))
            
            print(f"   ✅ Quick action '{action_id}' handled successfully")
            
        except Exception as e:
            print(f"   ❌ Error handling quick action: {e}")
            traceback.print_exc()
            self.send_error(500, f"Error handling quick action: {e}")
    
    def log_message(self, format, *args):
        """Custom logging"""
        print(f"🌐 {format % args}")

def main():
    """Run the debug server"""
    
    print("🔧 Debug Unified Command Center")
    print("="*50)
    
    # Check if templates directory exists
    templates_dir = base_path / "templates"
    print(f"📁 Templates directory: {templates_dir}")
    print(f"   Exists: {templates_dir.exists()}")
    
    if templates_dir.exists():
        dashboard_file = templates_dir / "dashboard.html"
        print(f"   Dashboard file: {dashboard_file.exists()}")
    
    port = 5001
    print(f"🌐 Starting debug server on port {port}...")
    
    try:
        server = HTTPServer(('localhost', port), DebugDashboardHandler)
        print(f"✅ Debug server started on http://localhost:{port}")
        print("📊 Test in browser or with curl:")
        print(f"   curl http://localhost:{port}/")
        print(f"   curl http://localhost:{port}/api/status")
        print("\nPress Ctrl+C to stop")
        
        server.serve_forever()
        
    except KeyboardInterrupt:
        print("\n🛑 Debug server stopped by user")
        server.shutdown()
    except Exception as e:
        print(f"❌ Debug server error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()