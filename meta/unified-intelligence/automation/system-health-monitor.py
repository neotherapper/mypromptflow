#!/usr/bin/env python3
"""
System Health Monitor for Unified Intelligence System
Monitors system health, queue status, and performance metrics
"""

import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List
import subprocess

class SystemHealthMonitor:
    """Monitor the health and status of the Unified Intelligence System"""
    
    def __init__(self, base_path: Path = None):
        self.base_path = base_path or Path(__file__).parent.parent
        self.status_report_file = self.base_path / "automation" / "system-health-report.json"
    
    def check_youtube_queue_health(self) -> Dict[str, Any]:
        """Check YouTube processing queue health"""
        try:
            queue_file = self.base_path / "platforms" / "youtube" / "transcript-processing-queue.json"
            
            if not queue_file.exists():
                return {"status": "error", "message": "Queue file missing"}
            
            with open(queue_file, 'r') as f:
                queue = json.load(f)
            
            # Analyze queue status
            status_counts = {}
            for job in queue:
                status = job['status']
                status_counts[status] = status_counts.get(status, 0) + 1
            
            total_videos = len(queue)
            completed_videos = sum(count for status, count in status_counts.items() 
                                 if 'completed' in status)
            pending_videos = status_counts.get('pending', 0)
            failed_videos = sum(count for status, count in status_counts.items() 
                              if 'failed' in status)
            
            # Calculate health metrics
            completion_rate = (completed_videos / total_videos * 100) if total_videos > 0 else 0
            failure_rate = (failed_videos / total_videos * 100) if total_videos > 0 else 0
            
            # Determine health status
            if completion_rate >= 80:
                health_status = "excellent"
            elif completion_rate >= 60:
                health_status = "good"
            elif completion_rate >= 40:
                health_status = "fair"
            elif completion_rate >= 20:
                health_status = "poor"
            else:
                health_status = "critical"
            
            return {
                "status": "healthy",
                "health_status": health_status,
                "metrics": {
                    "total_videos": total_videos,
                    "completed_videos": completed_videos,
                    "pending_videos": pending_videos,
                    "failed_videos": failed_videos,
                    "completion_rate": round(completion_rate, 1),
                    "failure_rate": round(failure_rate, 1)
                },
                "status_breakdown": status_counts
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def check_knowledge_vault_health(self) -> Dict[str, Any]:
        """Check knowledge vault health and content"""
        try:
            # Updated path to use main knowledge-vault structure
            vault_path = self.base_path.parent.parent / "knowledge-vault" / "databases" / "knowledge_vault" / "content-intelligence" / "youtube-intelligence"
            
            if not vault_path.exists():
                return {"status": "error", "message": "Knowledge vault missing"}
            
            # Count YouTube intelligence files
            youtube_vault = vault_path / "youtube-intelligence"
            youtube_content_count = 0
            
            if youtube_vault.exists():
                for channel_dir in youtube_vault.iterdir():
                    if channel_dir.is_dir():
                        for date_dir in channel_dir.iterdir():
                            if date_dir.is_dir():
                                youtube_content_count += len(list(date_dir.glob("*.json")))
            
            return {
                "status": "healthy",
                "metrics": {
                    "youtube_content_files": youtube_content_count,
                    "vault_exists": vault_path.exists(),
                    "youtube_vault_exists": youtube_vault.exists()
                }
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def check_daily_digest_health(self) -> Dict[str, Any]:
        """Check daily digest generation health"""
        try:
            digest_dir = self.base_path / "daily-digest" / "generated"
            
            if not digest_dir.exists():
                return {"status": "error", "message": "Digest directory missing"}
            
            # Find latest digest files
            json_digests = list(digest_dir.glob("system_wide_*.json"))
            md_digests = list(digest_dir.glob("*.md"))
            
            # Check for latest files
            latest_json = digest_dir / "system_wide_latest.json"
            latest_md = digest_dir / "latest_digest.md"
            
            latest_json_exists = latest_json.exists()
            latest_md_exists = latest_md.exists()
            
            # Get latest digest stats if available
            digest_stats = {}
            if latest_json_exists:
                try:
                    with open(latest_json, 'r') as f:
                        latest_digest = json.load(f)
                    
                    summary = latest_digest.get('summary', {})
                    digest_stats = {
                        "total_items": summary.get('total_items', 0),
                        "high_quality_items": summary.get('high_quality_items', 0),
                        "average_score": summary.get('average_quality_score', 0),
                        "generated_at": latest_digest.get('metadata', {}).get('generated_at', 'Unknown')
                    }
                except:
                    pass
            
            return {
                "status": "healthy",
                "metrics": {
                    "total_json_digests": len(json_digests),
                    "total_md_digests": len(md_digests),
                    "latest_json_exists": latest_json_exists,
                    "latest_md_exists": latest_md_exists,
                    "latest_digest_stats": digest_stats
                }
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def check_user_preferences_health(self) -> Dict[str, Any]:
        """Check user preferences and learning system health"""
        try:
            preferences_file = self.base_path / "user-preferences.json"
            
            if not preferences_file.exists():
                return {"status": "error", "message": "User preferences file missing"}
            
            with open(preferences_file, 'r') as f:
                preferences = json.load(f)
            
            # Analyze preferences structure
            stated_prefs = preferences.get('stated_preferences', {})
            learned_prefs = preferences.get('learned_preferences', {})
            topic_prefs = preferences.get('topic_preferences', {})
            metadata = preferences.get('learning_metadata', {})
            
            return {
                "status": "healthy",
                "metrics": {
                    "stated_preferences_count": len(stated_prefs),
                    "learned_source_patterns": len(learned_prefs.get('source_patterns', {})),
                    "learned_content_patterns": len(learned_prefs.get('content_patterns', {})),
                    "topic_preferences_count": len(topic_prefs),
                    "total_learning_events": metadata.get('total_learning_events', 0),
                    "last_update": metadata.get('last_update', 'Never')
                }
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def check_automation_health(self) -> Dict[str, Any]:
        """Check automation system health"""
        try:
            status_file = self.base_path / "automation" / "automation-status.json"
            log_file = self.base_path / "automation" / "daily-automation.log"
            
            automation_status = "unknown"
            last_run = "never"
            
            if status_file.exists():
                with open(status_file, 'r') as f:
                    status_data = json.load(f)
                
                automation_status = status_data.get('overall_status', 'unknown')
                last_run = status_data.get('run_timestamp', 'unknown')
            
            log_exists = log_file.exists()
            log_size = log_file.stat().st_size if log_exists else 0
            
            return {
                "status": "healthy" if automation_status in ["success", "partial_success"] else "warning",
                "metrics": {
                    "last_automation_status": automation_status,
                    "last_run_timestamp": last_run,
                    "log_file_exists": log_exists,
                    "log_file_size_bytes": log_size,
                    "automation_configured": status_file.exists()
                }
            }
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def generate_health_report(self) -> Dict[str, Any]:
        """Generate comprehensive system health report"""
        print("🏥 Unified Intelligence System Health Monitor")
        print("=" * 50)
        
        report = {
            "report_timestamp": datetime.now(timezone.utc).isoformat(),
            "system_components": {},
            "overall_health": "unknown"
        }
        
        # Check each system component
        components = [
            ("youtube_queue", "YouTube Processing Queue", self.check_youtube_queue_health),
            ("knowledge_vault", "Knowledge Vault", self.check_knowledge_vault_health),
            ("daily_digest", "Daily Digest System", self.check_daily_digest_health),
            ("user_preferences", "User Preferences & Learning", self.check_user_preferences_health),
            ("automation", "Automation System", self.check_automation_health)
        ]
        
        healthy_components = 0
        total_components = len(components)
        
        for component_key, component_name, check_function in components:
            print(f"\n🔍 Checking {component_name}...")
            
            component_health = check_function()
            report["system_components"][component_key] = {
                "name": component_name,
                "health": component_health
            }
            
            status = component_health.get("status", "unknown")
            
            if status == "healthy":
                print(f"   ✅ {component_name}: Healthy")
                healthy_components += 1
            elif status == "warning":
                print(f"   ⚠️ {component_name}: Warning")
            elif status == "error":
                print(f"   ❌ {component_name}: Error - {component_health.get('message', 'Unknown error')}")
            else:
                print(f"   ❓ {component_name}: Unknown status")
        
        # Determine overall system health
        health_percentage = (healthy_components / total_components) * 100
        
        if health_percentage >= 90:
            overall_health = "excellent"
            health_emoji = "🟢"
        elif health_percentage >= 70:
            overall_health = "good"
            health_emoji = "🟡"
        elif health_percentage >= 50:
            overall_health = "fair"
            health_emoji = "🟠"
        else:
            overall_health = "poor"
            health_emoji = "🔴"
        
        report["overall_health"] = overall_health
        report["health_metrics"] = {
            "healthy_components": healthy_components,
            "total_components": total_components,
            "health_percentage": round(health_percentage, 1)
        }
        
        # Display summary
        print(f"\n📊 System Health Summary:")
        print(f"   {health_emoji} Overall Health: {overall_health.title()} ({health_percentage:.1f}%)")
        print(f"   ✅ Healthy Components: {healthy_components}/{total_components}")
        
        # Show key metrics
        youtube_health = report["system_components"]["youtube_queue"]["health"]
        if youtube_health.get("status") == "healthy":
            metrics = youtube_health["metrics"]
            print(f"   🎬 YouTube Queue: {metrics['completed_videos']}/{metrics['total_videos']} videos processed")
            print(f"   📈 Completion Rate: {metrics['completion_rate']}%")
        
        digest_health = report["system_components"]["daily_digest"]["health"]
        if digest_health.get("status") == "healthy":
            latest_stats = digest_health["metrics"].get("latest_digest_stats", {})
            if latest_stats:
                print(f"   📰 Latest Digest: {latest_stats.get('total_items', 0)} items, {latest_stats.get('high_quality_items', 0)} high-quality")
        
        # Save report
        with open(self.status_report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n💾 Health report saved to: {self.status_report_file}")
        
        return report

def main():
    """Generate and display system health report"""
    monitor = SystemHealthMonitor()
    report = monitor.generate_health_report()
    
    # Exit with appropriate status code
    overall_health = report["overall_health"]
    if overall_health in ["excellent", "good"]:
        exit_code = 0
    elif overall_health == "fair":
        exit_code = 1
    else:
        exit_code = 2
    
    return exit_code

if __name__ == "__main__":
    import sys
    sys.exit(main())