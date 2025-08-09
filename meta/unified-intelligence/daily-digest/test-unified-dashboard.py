#!/usr/bin/env python3
"""
Test script for the Unified Command Center
"""

import json
import time
from pathlib import Path

# Import from the unified command center module
import sys
sys.path.append(str(Path(__file__).parent))

try:
    from unified_command_center import SystemStatusMonitor, IntelligenceAssistant
except ImportError:
    # If that fails, try importing from the file directly
    import importlib.util
    spec = importlib.util.spec_from_file_location("unified_command_center", "unified-command-center.py")
    ucc_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ucc_module)
    SystemStatusMonitor = ucc_module.SystemStatusMonitor
    IntelligenceAssistant = ucc_module.IntelligenceAssistant

def test_system_monitor():
    """Test the system status monitoring"""
    print("🧪 Testing System Status Monitor...")
    
    base_path = Path(__file__).parent
    monitor = SystemStatusMonitor(base_path)
    
    systems = monitor.get_system_status()
    
    print(f"   Found {len(systems)} systems:")
    for name, status in systems.items():
        print(f"   • {name}: {status.status} (health: {status.health_score:.1%})")
        print(f"     Description: {status.description}")
        print(f"     Last update: {status.last_update}")
        print(f"     Quick actions: {status.quick_actions}")
        print()
    
    return systems

def test_ai_assistant():
    """Test the AI assistant"""
    print("🤖 Testing AI Assistant...")
    
    base_path = Path(__file__).parent
    assistant = IntelligenceAssistant(base_path)
    
    test_messages = [
        "show system status",
        "add youtube channel",
        "generate intelligence report",
        "help me with something"
    ]
    
    for message in test_messages:
        print(f"   User: {message}")
        response = assistant.handle_request(message)
        print(f"   Assistant: {response['message'][:100]}...")
        print(f"   Success: {response['success']}")
        print()

def test_file_detection():
    """Test file detection for existing reports and dashboards"""
    print("📁 Testing File Detection...")
    
    base_path = Path(__file__).parent
    
    # Check for existing files
    files_to_check = [
        ("reports", "latest_intelligence_report.html"),
        ("reports", "latest_intelligence_report.json"),
        ("dashboard", "latest_dashboard.html"),
        ("trends", "latest_trend_analysis.json"),
        ("generated/content", "daily-digest.html"),
        ("config", "youtube-rss-channels.json")
    ]
    
    for directory, filename in files_to_check:
        file_path = base_path / directory / filename
        exists = file_path.exists()
        size = file_path.stat().st_size if exists else 0
        print(f"   {'✅' if exists else '❌'} {directory}/{filename} ({size:,} bytes)")

def main():
    """Run all tests"""
    
    print("🚀 Unified Command Center Test Suite")
    print("=" * 60)
    
    try:
        # Test system monitoring
        systems = test_system_monitor()
        
        # Test AI assistant
        test_ai_assistant()
        
        # Test file detection
        test_file_detection()
        
        # Summary
        print("📊 Test Summary:")
        active_systems = [name for name, status in systems.items() if status.status == "active"]
        inactive_systems = [name for name, status in systems.items() if status.status == "inactive"]
        error_systems = [name for name, status in systems.items() if status.status == "error"]
        
        print(f"   ✅ Active systems: {len(active_systems)}")
        if active_systems:
            print(f"      {', '.join(active_systems)}")
        
        print(f"   ⚠️  Inactive systems: {len(inactive_systems)}")
        if inactive_systems:
            print(f"      {', '.join(inactive_systems)}")
        
        print(f"   ❌ Error systems: {len(error_systems)}")
        if error_systems:
            print(f"      {', '.join(error_systems)}")
        
        print(f"\n✅ Test completed successfully!")
        print(f"💡 Start the dashboard with: python3 unified-command-center.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()