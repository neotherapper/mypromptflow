#!/usr/bin/env python3
"""
YouTube RSS Monitoring Workflow Runner
Automated workflow for monitoring YouTube channels and processing new videos
"""

import json
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
import time
import logging
import schedule

class YouTubeMonitoringWorkflow:
    """Complete YouTube monitoring workflow automation"""
    
    def __init__(self):
        self.logger = self._setup_logging()
        self.base_path = Path(__file__).parent
        self.queue_file = self.base_path / "transcript-processing-queue.json"
        self.state_file = self.base_path / "youtube-monitor-state.json"
        self.config_file = self.base_path / "youtube-channels-config.json"
        
    def _setup_logging(self):
        """Configure logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('monitoring-workflow.log'),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def check_system_status(self):
        """Check system components status"""
        self.logger.info("🔍 Checking system status...")
        
        status = {
            "timestamp": datetime.now().isoformat(),
            "components": {}
        }
        
        # Check RSS monitoring script
        rss_script = self.base_path / "scripts" / "rss-youtube-monitor.py"
        if rss_script.exists():
            status["components"]["rss_monitor"] = "ready"
            self.logger.info("✅ RSS monitor script found")
        else:
            status["components"]["rss_monitor"] = "missing"
            self.logger.warning("❌ RSS monitor script missing")
        
        # Check YouTube integration manager
        integration_script = self.base_path / "youtube-integration-manager.py"
        if integration_script.exists():
            status["components"]["integration_manager"] = "ready"
            self.logger.info("✅ Integration manager found")
        else:
            status["components"]["integration_manager"] = "missing"
            self.logger.warning("❌ Integration manager missing")
        
        # Check processing queue
        if self.queue_file.exists():
            with open(self.queue_file, 'r') as f:
                queue = json.load(f)
                pending = len([v for v in queue if v.get('status') == 'pending'])
                status["components"]["queue"] = {
                    "status": "ready",
                    "pending_videos": pending,
                    "total_videos": len(queue)
                }
                self.logger.info(f"✅ Processing queue: {pending} pending, {len(queue)} total")
        else:
            status["components"]["queue"] = {"status": "empty"}
            self.logger.info("📋 Processing queue is empty")
        
        # Check knowledge vault
        vault_path = self.base_path.parent.parent.parent.parent / "knowledge-vault" / "databases" / "knowledge_vault" / "content-intelligence" / "youtube-intelligence"
        if vault_path.exists():
            channel_dirs = list(vault_path.glob("*/"))
            status["components"]["knowledge_vault"] = {
                "status": "ready",
                "channels": len(channel_dirs)
            }
            self.logger.info(f"✅ Knowledge vault: {len(channel_dirs)} channels")
        else:
            status["components"]["knowledge_vault"] = {"status": "not_initialized"}
            self.logger.warning("❌ Knowledge vault not initialized")
        
        return status
    
    def run_rss_monitoring(self):
        """Run RSS monitoring to check for new videos"""
        self.logger.info("📺 Starting RSS monitoring...")
        
        try:
            # Run the RSS monitor script
            result = subprocess.run(
                ["python3", "scripts/rss-youtube-monitor.py"],
                cwd=self.base_path,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                self.logger.info("✅ RSS monitoring completed successfully")
                
                # Parse output for new videos
                if "new videos found" in result.stdout.lower():
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if "new videos" in line.lower():
                            self.logger.info(f"📹 {line.strip()}")
                
                return {"status": "success", "output": result.stdout}
            else:
                self.logger.error(f"❌ RSS monitoring failed: {result.stderr}")
                return {"status": "error", "error": result.stderr}
                
        except subprocess.TimeoutExpired:
            self.logger.error("⏱️ RSS monitoring timed out")
            return {"status": "timeout"}
        except Exception as e:
            self.logger.error(f"❌ Error running RSS monitoring: {str(e)}")
            return {"status": "error", "error": str(e)}
    
    def process_pending_videos(self, limit=5):
        """Process pending videos in the queue"""
        self.logger.info(f"🎬 Processing pending videos (limit: {limit})...")
        
        if not self.queue_file.exists():
            self.logger.info("📋 No processing queue found")
            return {"status": "no_queue"}
        
        with open(self.queue_file, 'r') as f:
            queue = json.load(f)
        
        pending_videos = [v for v in queue if v.get('status') == 'pending'][:limit]
        
        if not pending_videos:
            self.logger.info("✅ No pending videos to process")
            return {"status": "no_pending", "processed": 0}
        
        processed_count = 0
        
        for video in pending_videos:
            self.logger.info(f"📹 Processing: {video['title'][:50]}...")
            
            try:
                # Simulate processing (in real workflow, this would call MCP tools)
                # For now, we'll mark as processed_simulation
                video['status'] = 'processed_simulation'
                video['processed_at'] = datetime.now().isoformat()
                processed_count += 1
                
                # Small delay between videos
                time.sleep(2)
                
            except Exception as e:
                self.logger.error(f"❌ Error processing video: {str(e)}")
                video['status'] = 'error'
                video['error'] = str(e)
        
        # Save updated queue
        with open(self.queue_file, 'w') as f:
            json.dump(queue, f, indent=2)
        
        self.logger.info(f"✅ Processed {processed_count} videos")
        return {"status": "success", "processed": processed_count}
    
    def generate_daily_report(self):
        """Generate daily monitoring report"""
        self.logger.info("📊 Generating daily report...")
        
        report = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "timestamp": datetime.now().isoformat(),
            "channels_monitored": 0,
            "new_videos_found": 0,
            "videos_processed": 0,
            "storage_used": 0
        }
        
        # Analyze processing queue
        if self.queue_file.exists():
            with open(self.queue_file, 'r') as f:
                queue = json.load(f)
                
            # Count videos by status
            today = datetime.now().date()
            today_videos = []
            
            for video in queue:
                if 'queued_at' in video:
                    try:
                        video_date = datetime.fromisoformat(video['queued_at'].replace('Z', '+00:00')).date()
                        if video_date == today:
                            today_videos.append(video)
                    except:
                        pass
            
            report["new_videos_found"] = len(today_videos)
            report["videos_processed"] = len([v for v in today_videos if v.get('status') in ['completed', 'processed_simulation']])
        
        # Count monitored channels
        if self.state_file.exists():
            with open(self.state_file, 'r') as f:
                state = json.load(f)
                report["channels_monitored"] = len(state)
        
        # Save report
        report_file = self.base_path / f"daily_report_{datetime.now().strftime('%Y-%m-%d')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.logger.info(f"📊 Report saved: {report_file.name}")
        self.logger.info(f"  • Channels monitored: {report['channels_monitored']}")
        self.logger.info(f"  • New videos found: {report['new_videos_found']}")
        self.logger.info(f"  • Videos processed: {report['videos_processed']}")
        
        return report
    
    def run_complete_workflow(self):
        """Run the complete monitoring workflow"""
        self.logger.info("🚀 Starting complete monitoring workflow")
        self.logger.info("=" * 50)
        
        # Step 1: Check system status
        status = self.check_system_status()
        
        # Step 2: Run RSS monitoring
        rss_result = self.run_rss_monitoring()
        
        # Step 3: Process pending videos
        process_result = self.process_pending_videos(limit=3)
        
        # Step 4: Generate report
        report = self.generate_daily_report()
        
        self.logger.info("=" * 50)
        self.logger.info("✅ Workflow completed!")
        
        return {
            "timestamp": datetime.now().isoformat(),
            "system_status": status,
            "rss_monitoring": rss_result,
            "processing": process_result,
            "report": report
        }
    
    def setup_automated_schedule(self):
        """Setup automated monitoring schedule"""
        self.logger.info("⏰ Setting up automated schedule...")
        
        # Schedule RSS monitoring every 2 hours
        schedule.every(2).hours.do(self.run_rss_monitoring)
        
        # Schedule video processing every 4 hours
        schedule.every(4).hours.do(lambda: self.process_pending_videos(limit=5))
        
        # Schedule daily report at 23:00
        schedule.every().day.at("23:00").do(self.generate_daily_report)
        
        self.logger.info("✅ Schedule configured:")
        self.logger.info("  • RSS monitoring: Every 2 hours")
        self.logger.info("  • Video processing: Every 4 hours")
        self.logger.info("  • Daily report: 23:00")
        
        return schedule.get_jobs()

def main():
    """Main entry point"""
    workflow = YouTubeMonitoringWorkflow()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "monitor":
            # Run RSS monitoring only
            workflow.run_rss_monitoring()
        elif command == "process":
            # Process pending videos
            limit = int(sys.argv[2]) if len(sys.argv) > 2 else 5
            workflow.process_pending_videos(limit=limit)
        elif command == "report":
            # Generate report
            workflow.generate_daily_report()
        elif command == "schedule":
            # Run with automated schedule
            workflow.setup_automated_schedule()
            print("⏰ Scheduler running... Press Ctrl+C to stop")
            try:
                while True:
                    schedule.run_pending()
                    time.sleep(60)
            except KeyboardInterrupt:
                print("\n🛑 Scheduler stopped")
        else:
            print(f"Unknown command: {command}")
            print("Usage: python run_monitoring_workflow.py [monitor|process|report|schedule]")
    else:
        # Run complete workflow once
        result = workflow.run_complete_workflow()
        
        # Save workflow result
        result_file = workflow.base_path / f"workflow_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(result_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"💾 Workflow result saved to: {result_file.name}")

if __name__ == "__main__":
    main()