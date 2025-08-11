#!/usr/bin/env python3
"""
Test web functionality of the Unified Command Center
Tests actual HTTP endpoints and web interface
"""

import requests
import json
import time
import subprocess
import signal
import sys
import os
from pathlib import Path
from threading import Thread
import webbrowser

class WebFunctionalityTester:
    def __init__(self):
        self.base_url = "http://localhost:5000"
        self.server_process = None
        self.test_results = {}
        
    def start_server(self):
        """Start the unified command center server"""
        print("🚀 Starting server...")
        try:
            # Start server in background
            self.server_process = subprocess.Popen(
                [sys.executable, "unified-command-center.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid if hasattr(os, 'setsid') else None
            )
            
            # Wait for server to start
            time.sleep(4)
            
            # Check if server is running
            try:
                response = requests.get(self.base_url, timeout=5)
                if response.status_code == 200:
                    print("✅ Server started successfully")
                    return True
                else:
                    print(f"❌ Server returned status code: {response.status_code}")
                    return False
            except requests.exceptions.ConnectionError:
                print("❌ Cannot connect to server")
                return False
                
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
            return False
    
    def stop_server(self):
        """Stop the server"""
        if self.server_process:
            try:
                # Kill the process group if possible
                if hasattr(os, 'killpg'):
                    os.killpg(os.getpgid(self.server_process.pid), signal.SIGTERM)
                else:
                    self.server_process.terminate()
                
                self.server_process.wait(timeout=5)
                print("✅ Server stopped")
            except Exception as e:
                print(f"⚠️  Error stopping server: {e}")
    
    def test_main_dashboard(self):
        """Test the main dashboard page"""
        print("\n📊 Testing main dashboard...")
        
        try:
            response = requests.get(self.base_url, timeout=10)
            
            if response.status_code == 200:
                content = response.text
                
                # Check for key elements
                checks = [
                    ("title" in content.lower(), "Page has title"),
                    ("unified intelligence command center" in content.lower(), "Contains main heading"),
                    ("systems-grid" in content, "Has systems grid container"),
                    ("ai-assistant" in content, "Has AI assistant section"),
                    ("api/status" in content, "Contains status API call"),
                    ("api/assistant" in content, "Contains assistant API call")
                ]
                
                passed = 0
                for check, description in checks:
                    status = "✅" if check else "❌"
                    print(f"   {status} {description}")
                    if check:
                        passed += 1
                
                self.test_results['dashboard'] = {
                    'status': 'success' if passed >= 4 else 'partial',
                    'passed': passed,
                    'total': len(checks),
                    'content_length': len(content)
                }
                
                return passed >= 4
            else:
                print(f"   ❌ Dashboard returned status code: {response.status_code}")
                self.test_results['dashboard'] = {'status': 'failed', 'error': f'HTTP {response.status_code}'}
                return False
                
        except Exception as e:
            print(f"   ❌ Error testing dashboard: {e}")
            self.test_results['dashboard'] = {'status': 'error', 'error': str(e)}
            return False
    
    def test_status_api(self):
        """Test the system status API"""
        print("\n📡 Testing status API...")
        
        try:
            response = requests.get(f"{self.base_url}/api/status", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Check API response structure
                checks = [
                    ("timestamp" in data, "Has timestamp"),
                    ("systems" in data, "Has systems data"),
                    (len(data.get("systems", {})) >= 4, "Has multiple systems"),
                    (any("youtube" in name.lower() for name in data.get("systems", {})), "Has YouTube systems"),
                    (any("status" in system for system in data.get("systems", {}).values()), "Systems have status")
                ]
                
                passed = 0
                for check, description in checks:
                    status = "✅" if check else "❌"
                    print(f"   {status} {description}")
                    if check:
                        passed += 1
                
                # Show system status summary
                systems = data.get("systems", {})
                active_count = sum(1 for s in systems.values() if s.get("status") == "active")
                print(f"   📊 Found {len(systems)} systems, {active_count} active")
                
                self.test_results['status_api'] = {
                    'status': 'success' if passed >= 3 else 'partial',
                    'passed': passed,
                    'total': len(checks),
                    'systems_count': len(systems),
                    'active_count': active_count
                }
                
                return passed >= 3
            else:
                print(f"   ❌ Status API returned status code: {response.status_code}")
                self.test_results['status_api'] = {'status': 'failed', 'error': f'HTTP {response.status_code}'}
                return False
                
        except Exception as e:
            print(f"   ❌ Error testing status API: {e}")
            self.test_results['status_api'] = {'status': 'error', 'error': str(e)}
            return False
    
    def test_assistant_api(self):
        """Test the AI assistant API"""
        print("\n🤖 Testing AI assistant API...")
        
        try:
            test_message = "show system status"
            payload = {"message": test_message}
            
            response = requests.post(
                f"{self.base_url}/api/assistant",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check assistant response structure
                checks = [
                    ("success" in data, "Has success field"),
                    ("message" in data, "Has message field"),
                    (len(data.get("message", "")) > 10, "Message has content"),
                    ("system" in data.get("message", "").lower(), "Response mentions systems")
                ]
                
                passed = 0
                for check, description in checks:
                    status = "✅" if check else "❌"
                    print(f"   {status} {description}")
                    if check:
                        passed += 1
                
                print(f"   💬 Assistant response: {data.get('message', '')[:100]}...")
                
                self.test_results['assistant_api'] = {
                    'status': 'success' if passed >= 3 else 'partial',
                    'passed': passed,
                    'total': len(checks),
                    'response_length': len(data.get('message', ''))
                }
                
                return passed >= 3
            else:
                print(f"   ❌ Assistant API returned status code: {response.status_code}")
                self.test_results['assistant_api'] = {'status': 'failed', 'error': f'HTTP {response.status_code}'}
                return False
                
        except Exception as e:
            print(f"   ❌ Error testing assistant API: {e}")
            self.test_results['assistant_api'] = {'status': 'error', 'error': str(e)}
            return False
    
    def test_file_serving(self):
        """Test file serving capabilities"""
        print("\n📁 Testing file serving...")
        
        # Test various file endpoints
        file_tests = [
            ("/reports/latest_intelligence_report.html", "Intelligence report HTML"),
            ("/reports/latest_intelligence_report.json", "Intelligence report JSON"),
            ("/dashboard/latest_dashboard.html", "Live dashboard HTML"),
            ("/trends/latest_trend_analysis.json", "Trend analysis JSON"),
            ("/generated/content/daily-digest.html", "Content digest HTML")
        ]
        
        passed = 0
        total = len(file_tests)
        
        for endpoint, description in file_tests:
            try:
                response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                
                if response.status_code == 200 and len(response.content) > 0:
                    print(f"   ✅ {description} ({len(response.content):,} bytes)")
                    passed += 1
                elif response.status_code == 404:
                    print(f"   ⚠️  {description} - File not found (expected for new systems)")
                else:
                    print(f"   ❌ {description} - HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ {description} - Error: {e}")
        
        self.test_results['file_serving'] = {
            'status': 'success' if passed >= total//2 else 'partial',
            'passed': passed,
            'total': total
        }
        
        return passed >= total//2
    
    def test_quick_actions(self):
        """Test quick action endpoints"""
        print("\n⚡ Testing quick actions...")
        
        actions = ["generate_report", "view_dashboard", "view_trends"]
        passed = 0
        
        for action in actions:
            try:
                response = requests.get(f"{self.base_url}/api/quick-action/{action}", timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("success"):
                        print(f"   ✅ {action}: {data.get('message', '')[:50]}...")
                        passed += 1
                    else:
                        print(f"   ⚠️  {action}: {data.get('message', '')}")
                else:
                    print(f"   ❌ {action} - HTTP {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ {action} - Error: {e}")
        
        self.test_results['quick_actions'] = {
            'status': 'success' if passed == len(actions) else 'partial',
            'passed': passed,
            'total': len(actions)
        }
        
        return passed >= len(actions)//2
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*60)
        print("📊 WEB FUNCTIONALITY TEST RESULTS")
        print("="*60)
        
        total_tests = len(self.test_results)
        successful_tests = sum(1 for result in self.test_results.values() 
                              if result.get('status') == 'success')
        
        print(f"Overall: {successful_tests}/{total_tests} test categories passed")
        print()
        
        for test_name, result in self.test_results.items():
            status_icon = {
                'success': '✅',
                'partial': '⚠️',
                'failed': '❌',
                'error': '❌'
            }.get(result.get('status'), '❓')
            
            print(f"{status_icon} {test_name.replace('_', ' ').title()}: {result.get('status', 'unknown')}")
            
            if 'passed' in result and 'total' in result:
                print(f"   Score: {result['passed']}/{result['total']}")
            
            if 'error' in result:
                print(f"   Error: {result['error']}")
            
            print()
        
        if successful_tests >= total_tests * 0.8:
            print("🎉 WEB FUNCTIONALITY TEST: PASSED")
            print("The unified command center web interface is working correctly!")
        elif successful_tests >= total_tests * 0.5:
            print("⚠️ WEB FUNCTIONALITY TEST: PARTIAL")
            print("Most features work, but some issues need attention.")
        else:
            print("❌ WEB FUNCTIONALITY TEST: FAILED")
            print("Significant issues found with web functionality.")
        
        return successful_tests >= total_tests * 0.8

def main():
    """Run comprehensive web functionality tests"""
    
    print("🌐 Unified Command Center - Web Functionality Test")
    print("="*60)
    
    # os is already imported at the top
    
    tester = WebFunctionalityTester()
    
    try:
        # Start server
        if not tester.start_server():
            print("❌ Cannot start server - aborting tests")
            return False
        
        # Run all tests
        tests = [
            tester.test_main_dashboard,
            tester.test_status_api,
            tester.test_assistant_api,
            tester.test_file_serving,
            tester.test_quick_actions
        ]
        
        results = []
        for test in tests:
            try:
                result = test()
                results.append(result)
            except Exception as e:
                print(f"   ❌ Test error: {e}")
                results.append(False)
        
        # Print summary
        tester.print_summary()
        
        return sum(results) >= len(results) * 0.8
        
    finally:
        # Always stop server
        tester.stop_server()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)