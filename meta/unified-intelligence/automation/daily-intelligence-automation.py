#!/usr/bin/env python3
"""
Daily Intelligence Automation System
Automated daily processing and monitoring for the Unified Intelligence System
"""

import json
import subprocess
import sys
import time
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Any, List

class DailyIntelligenceAutomation:
    """Automated daily intelligence processing and monitoring"""
    
    def __init__(self, base_path: Path = None):
        self.base_path = base_path or Path(__file__).parent.parent
        self.log_file = self.base_path / "automation" / "daily-automation.log"
        self.status_file = self.base_path / "automation" / "automation-status.json"
        
        # Ensure automation directory exists
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
    
    def log_message(self, message: str, level: str = "INFO"):
        """Log message with timestamp"""
        timestamp = datetime.now(timezone.utc).isoformat()
        log_entry = f"{timestamp} - {level} - {message}"
        
        print(log_entry)
        
        # Write to log file
        with open(self.log_file, 'a') as f:
            f.write(log_entry + "\n")
    
    def run_rss_monitoring(self) -> Dict[str, Any]:
        """Run RSS monitoring for all YouTube channels"""
        self.log_message("Starting RSS monitoring...")
        
        try:
            # Change to YouTube scripts directory
            youtube_scripts = self.base_path / "platforms" / "youtube" / "scripts"
            
            result = subprocess.run([
                'python3', 'rss-youtube-monitor.py'
            ], 
            cwd=youtube_scripts,
            capture_output=True, 
            text=True, 
            timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                self.log_message("RSS monitoring completed successfully")
                return {"status": "success", "output": result.stdout}
            else:
                self.log_message(f"RSS monitoring failed: {result.stderr}", "ERROR")
                return {"status": "failed", "error": result.stderr}
                
        except subprocess.TimeoutExpired:
            self.log_message("RSS monitoring timed out", "ERROR")
            return {"status": "timeout", "error": "RSS monitoring timeout"}
        except Exception as e:
            self.log_message(f"RSS monitoring exception: {str(e)}", "ERROR")
            return {"status": "error", "error": str(e)}
    
    def process_youtube_queue(self, max_videos: int = 5) -> Dict[str, Any]:
        """Process YouTube videos from the queue"""
        self.log_message(f"Processing up to {max_videos} YouTube videos...")
        
        try:
            queue_file = self.base_path / "platforms" / "youtube" / "transcript-processing-queue.json"
            
            # Load current queue
            with open(queue_file, 'r') as f:
                queue = json.load(f)
            
            pending_videos = [job for job in queue if job['status'] == 'pending']
            
            if not pending_videos:
                self.log_message("No pending videos to process")
                return {"status": "success", "processed": 0, "message": "No pending videos"}
            
            # Process up to max_videos
            videos_to_process = pending_videos[:max_videos]
            processed_count = 0
            failed_count = 0
            
            for video in videos_to_process:
                self.log_message(f"Processing: {video['title']} ({video['channel']})")
                
                try:
                    # Run unified processing
                    result = subprocess.run([
                        'python3', 'test-unified-processing.py'
                    ], 
                    cwd=self.base_path,
                    capture_output=True, 
                    text=True, 
                    timeout=120  # 2 minute timeout per video
                    )
                    
                    if result.returncode == 0:
                        processed_count += 1
                        self.log_message(f"Successfully processed: {video['title']}")
                    else:
                        failed_count += 1
                        self.log_message(f"Failed to process: {video['title']} - {result.stderr}", "ERROR")
                    
                    # Brief pause between videos
                    time.sleep(5)
                    
                except subprocess.TimeoutExpired:
                    failed_count += 1
                    self.log_message(f"Timeout processing: {video['title']}", "ERROR")
                except Exception as e:
                    failed_count += 1
                    self.log_message(f"Exception processing: {video['title']} - {str(e)}", "ERROR")
            
            self.log_message(f"YouTube processing complete: {processed_count} success, {failed_count} failed")
            
            return {
                "status": "success",
                "processed": processed_count,
                "failed": failed_count,
                "total_attempted": len(videos_to_process)
            }
            
        except Exception as e:
            self.log_message(f"YouTube queue processing exception: {str(e)}", "ERROR")
            return {"status": "error", "error": str(e)}
    
    def generate_daily_digest(self) -> Dict[str, Any]:
        """Generate daily intelligence digest"""
        self.log_message("Generating daily intelligence digest...")
        
        try:
            result = subprocess.run([
                'python3', 'daily-digest/intelligence-digest-generator.py'
            ], 
            cwd=self.base_path,
            capture_output=True, 
            text=True, 
            timeout=60
            )
            
            if result.returncode == 0:
                self.log_message("Daily digest generated successfully")
                return {"status": "success", "output": result.stdout}
            else:
                self.log_message(f"Daily digest generation failed: {result.stderr}", "ERROR")
                return {"status": "failed", "error": result.stderr}
                
        except Exception as e:
            self.log_message(f"Daily digest generation exception: {str(e)}", "ERROR")
            return {"status": "error", "error": str(e)}
    
    def run_discovery_algorithms(self) -> Dict[str, Any]:
        """Run discovery algorithms for new sources"""
        self.log_message("Running discovery algorithms...")
        
        try:
            # Run GitHub discovery
            result = subprocess.run([
                'python3', 'discovery-algorithms/github-discovery.py'
            ], 
            cwd=self.base_path,
            capture_output=True, 
            text=True, 
            timeout=180  # 3 minute timeout
            )
            
            if result.returncode == 0:
                self.log_message("Discovery algorithms completed successfully")
                return {"status": "success", "output": result.stdout}
            else:
                self.log_message(f"Discovery algorithms failed: {result.stderr}", "ERROR")
                return {"status": "failed", "error": result.stderr}
                
        except Exception as e:
            self.log_message(f"Discovery algorithms exception: {str(e)}", "ERROR")
            return {"status": "error", "error": str(e)}
    
    def update_automation_status(self, status_data: Dict[str, Any]):
        """Update automation status file"""
        with open(self.status_file, 'w') as f:
            json.dump(status_data, f, indent=2)
    
    def run_daily_automation(self) -> Dict[str, Any]:
        """Run complete daily automation workflow"""
        self.log_message("🚀 Starting Daily Intelligence Automation")
        self.log_message("=" * 50)
        
        automation_results = {
            "run_timestamp": datetime.now(timezone.utc).isoformat(),
            "workflow_steps": {},
            "overall_status": "running"
        }
        
        try:
            # Step 1: RSS Monitoring
            self.log_message("📡 Step 1: RSS Monitoring")
            rss_result = self.run_rss_monitoring()
            automation_results["workflow_steps"]["rss_monitoring"] = rss_result
            
            # Step 2: Process YouTube Queue (limited to prevent overload)
            self.log_message("🎬 Step 2: YouTube Processing")
            youtube_result = self.process_youtube_queue(max_videos=3)
            automation_results["workflow_steps"]["youtube_processing"] = youtube_result
            
            # Step 3: Generate Daily Digest
            self.log_message("📰 Step 3: Daily Digest Generation")
            digest_result = self.generate_daily_digest()
            automation_results["workflow_steps"]["daily_digest"] = digest_result
            
            # Step 4: Discovery Algorithms (optional, may skip if other steps failed)
            if (rss_result["status"] == "success" and 
                youtube_result["status"] == "success" and 
                digest_result["status"] == "success"):
                
                self.log_message("🔍 Step 4: Discovery Algorithms")
                discovery_result = self.run_discovery_algorithms()
                automation_results["workflow_steps"]["discovery"] = discovery_result
            else:
                self.log_message("⏭️ Skipping discovery algorithms due to previous failures")
                automation_results["workflow_steps"]["discovery"] = {"status": "skipped", "reason": "Previous step failures"}
            
            # Determine overall status
            successful_steps = sum(1 for step in automation_results["workflow_steps"].values() 
                                 if step["status"] == "success")
            total_steps = len(automation_results["workflow_steps"])
            
            if successful_steps == total_steps:
                automation_results["overall_status"] = "success"
                self.log_message("✅ Daily automation completed successfully!")
            elif successful_steps > 0:
                automation_results["overall_status"] = "partial_success"
                self.log_message(f"⚠️ Daily automation partially successful ({successful_steps}/{total_steps} steps)")
            else:
                automation_results["overall_status"] = "failed"
                self.log_message("❌ Daily automation failed")
            
            # Add summary statistics
            automation_results["summary"] = {
                "successful_steps": successful_steps,
                "total_steps": total_steps,
                "success_rate": f"{(successful_steps / total_steps * 100):.1f}%",
                "youtube_videos_processed": youtube_result.get("processed", 0),
                "completion_time": datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            self.log_message(f"💥 Daily automation exception: {str(e)}", "ERROR")
            automation_results["overall_status"] = "error"
            automation_results["error"] = str(e)
        
        # Update status file
        self.update_automation_status(automation_results)
        
        self.log_message("📊 Daily Automation Summary:")
        self.log_message(f"   Overall Status: {automation_results['overall_status']}")
        if "summary" in automation_results:
            summary = automation_results["summary"]
            self.log_message(f"   Success Rate: {summary['success_rate']}")
            self.log_message(f"   Videos Processed: {summary['youtube_videos_processed']}")
        
        return automation_results

def main():
    """Main automation function"""
    automation = DailyIntelligenceAutomation()
    results = automation.run_daily_automation()
    
    # Exit with appropriate code
    if results["overall_status"] in ["success", "partial_success"]:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()