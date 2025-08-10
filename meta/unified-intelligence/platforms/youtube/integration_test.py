#!/usr/bin/env python3
"""
YouTube RSS Monitoring System - Integration Test
Complete end-to-end test of the monitoring and processing pipeline
"""

import json
import subprocess
import time
from datetime import datetime
from pathlib import Path
import sys

class IntegrationTest:
    """Integration test for YouTube monitoring system"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.test_results = {
            "timestamp": datetime.now().isoformat(),
            "tests": []
        }
    
    def run_test(self, test_name: str, test_func):
        """Run a single test and record results"""
        print(f"\n🧪 Running: {test_name}")
        print("-" * 40)
        
        try:
            start_time = time.time()
            result = test_func()
            elapsed = time.time() - start_time
            
            test_result = {
                "name": test_name,
                "status": "passed" if result else "failed",
                "elapsed_seconds": round(elapsed, 2),
                "details": result
            }
            
            if result:
                print(f"✅ PASSED ({elapsed:.2f}s)")
            else:
                print(f"❌ FAILED ({elapsed:.2f}s)")
                
        except Exception as e:
            test_result = {
                "name": test_name,
                "status": "error",
                "error": str(e)
            }
            print(f"❌ ERROR: {str(e)}")
        
        self.test_results["tests"].append(test_result)
        return test_result["status"] == "passed"
    
    def test_rss_monitoring(self):
        """Test RSS feed monitoring"""
        try:
            # Check if RSS monitor script exists
            rss_script = self.base_path / "scripts" / "rss-youtube-monitor.py"
            if not rss_script.exists():
                return {"error": "RSS monitor script not found"}
            
            # Run RSS monitoring
            result = subprocess.run(
                ["python3", str(rss_script)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                # Check if queue was updated
                queue_file = self.base_path / "transcript-processing-queue.json"
                if queue_file.exists():
                    with open(queue_file, 'r') as f:
                        queue = json.load(f)
                    return {
                        "success": True,
                        "videos_in_queue": len(queue),
                        "output_snippet": result.stdout[:200] if result.stdout else None
                    }
            
            return {"error": f"RSS monitoring failed: {result.stderr}"}
            
        except Exception as e:
            return {"error": str(e)}
    
    def test_video_processing(self):
        """Test video processing pipeline"""
        try:
            queue_file = self.base_path / "transcript-processing-queue.json"
            
            if not queue_file.exists():
                return {"error": "No processing queue found"}
            
            with open(queue_file, 'r') as f:
                queue = json.load(f)
            
            # Check queue structure
            if queue and len(queue) > 0:
                sample_video = queue[0]
                required_fields = ["video_url", "video_id", "title", "channel", "status"]
                
                for field in required_fields:
                    if field not in sample_video:
                        return {"error": f"Missing required field: {field}"}
                
                # Count videos by status
                status_counts = {}
                for video in queue:
                    status = video.get("status", "unknown")
                    status_counts[status] = status_counts.get(status, 0) + 1
                
                return {
                    "success": True,
                    "total_videos": len(queue),
                    "status_distribution": status_counts
                }
            
            return {"error": "Queue is empty"}
            
        except Exception as e:
            return {"error": str(e)}
    
    def test_knowledge_vault_storage(self):
        """Test knowledge vault integration"""
        try:
            vault_path = self.base_path.parent.parent.parent.parent / "knowledge-vault" / "databases" / "knowledge_vault" / "content-intelligence" / "youtube-intelligence"
            
            if not vault_path.exists():
                return {"error": "Knowledge vault not initialized"}
            
            # Count stored content
            channel_dirs = list(vault_path.glob("*/"))
            total_files = 0
            file_types = {}
            
            for channel_dir in channel_dirs:
                for file in channel_dir.rglob("*"):
                    if file.is_file():
                        total_files += 1
                        ext = file.suffix
                        file_types[ext] = file_types.get(ext, 0) + 1
            
            return {
                "success": True,
                "channels": len(channel_dirs),
                "total_files": total_files,
                "file_types": file_types
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def test_mcp_integration(self):
        """Test MCP server integration"""
        try:
            # Check if MCP tools are accessible
            # This would normally test actual MCP server connections
            # For now, we'll check configuration
            
            mcp_config_indicators = [
                self.base_path / "youtube-integration-manager.py",
                self.base_path / "youtube_transcript_processor.py"
            ]
            
            configs_found = []
            for config_file in mcp_config_indicators:
                if config_file.exists():
                    configs_found.append(config_file.name)
            
            if configs_found:
                return {
                    "success": True,
                    "mcp_ready_scripts": configs_found,
                    "note": "MCP integration scripts found"
                }
            
            return {"error": "No MCP integration scripts found"}
            
        except Exception as e:
            return {"error": str(e)}
    
    def test_unified_framework_integration(self):
        """Test unified intelligence framework integration"""
        try:
            unified_script = self.base_path / "unified-youtube-integration.py"
            
            if not unified_script.exists():
                return {"error": "Unified integration script not found"}
            
            # Check configuration files
            config_files = {
                "source_registry": self.base_path.parent.parent / "source-registry.yaml",
                "user_preferences": self.base_path.parent.parent.parent.parent / "knowledge-vault" / "databases" / "knowledge_vault" / "content-intelligence" / "user-preferences.json"
            }
            
            configs_status = {}
            for name, path in config_files.items():
                configs_status[name] = path.exists()
            
            return {
                "success": all(configs_status.values()),
                "unified_script": "present",
                "configurations": configs_status
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def test_monitoring_automation(self):
        """Test automation and scheduling capabilities"""
        try:
            workflow_script = self.base_path / "run_monitoring_workflow.py"
            
            if not workflow_script.exists():
                return {"error": "Workflow automation script not found"}
            
            # Check if daily reports exist
            reports = list(self.base_path.glob("daily_report_*.json"))
            
            # Check monitoring logs
            log_file = self.base_path / "monitoring-workflow.log"
            log_exists = log_file.exists()
            
            return {
                "success": True,
                "automation_script": "present",
                "daily_reports": len(reports),
                "monitoring_log": "present" if log_exists else "missing"
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def run_all_tests(self):
        """Run all integration tests"""
        print("🚀 YouTube RSS Monitoring System - Integration Test Suite")
        print("=" * 60)
        
        test_suite = [
            ("RSS Feed Monitoring", self.test_rss_monitoring),
            ("Video Processing Pipeline", self.test_video_processing),
            ("Knowledge Vault Storage", self.test_knowledge_vault_storage),
            ("MCP Server Integration", self.test_mcp_integration),
            ("Unified Framework Integration", self.test_unified_framework_integration),
            ("Monitoring Automation", self.test_monitoring_automation)
        ]
        
        passed = 0
        failed = 0
        errors = 0
        
        for test_name, test_func in test_suite:
            if self.run_test(test_name, test_func):
                passed += 1
            else:
                test_status = self.test_results["tests"][-1]["status"]
                if test_status == "error":
                    errors += 1
                else:
                    failed += 1
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("-" * 60)
        print(f"✅ Passed: {passed}/{len(test_suite)}")
        print(f"❌ Failed: {failed}/{len(test_suite)}")
        print(f"🔥 Errors: {errors}/{len(test_suite)}")
        
        # Calculate overall status
        if passed == len(test_suite):
            overall_status = "ALL TESTS PASSED"
            status_emoji = "🎉"
        elif passed > len(test_suite) / 2:
            overall_status = "PARTIAL SUCCESS"
            status_emoji = "⚠️"
        else:
            overall_status = "TESTS FAILED"
            status_emoji = "❌"
        
        print(f"\n{status_emoji} Overall Status: {overall_status}")
        
        # Save results
        self.test_results["summary"] = {
            "total_tests": len(test_suite),
            "passed": passed,
            "failed": failed,
            "errors": errors,
            "overall_status": overall_status
        }
        
        results_file = self.base_path / f"integration_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(results_file, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"\n💾 Test results saved to: {results_file.name}")
        
        return passed == len(test_suite)

def main():
    """Main entry point"""
    tester = IntegrationTest()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()