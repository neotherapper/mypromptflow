#!/usr/bin/env python3
"""
Automated Monitoring Scheduler
Periodically refreshes content from all configured sources
"""

import asyncio
import logging
import signal
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any
import json

# Import our monitoring components
from agents.queen_agent import QueenAgent
from sources.rss_monitor import RSSSourceMonitor
from sources.claude_focused_monitor import CLAUDE_FOCUSED_SOURCES
from core import SourceMetadata, SourceType
from storage.database import StorageManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("AutoMonitor")

class AutoMonitor:
    """Automated monitoring scheduler for continuous intelligence gathering"""
    
    def __init__(self, interval_minutes: int = 30):
        """
        Initialize auto monitor
        
        Args:
            interval_minutes: How often to refresh content (default: 30 minutes)
        """
        self.interval = interval_minutes * 60  # Convert to seconds
        self.running = False
        self.queen = QueenAgent()
        self.storage = StorageManager()
        self.stats = {
            "total_runs": 0,
            "successful_runs": 0,
            "failed_runs": 0,
            "total_items_collected": 0,
            "last_run": None,
            "next_run": None
        }
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info("🛑 Received shutdown signal, stopping monitor...")
        self.running = False
        sys.exit(0)
    
    async def monitor_once(self) -> Dict[str, Any]:
        """
        Run a single monitoring cycle
        
        Returns:
            Results of the monitoring run
        """
        logger.info("🔄 Starting monitoring cycle...")
        start_time = datetime.now()
        
        try:
            # Monitor all Claude-focused sources
            total_items = 0
            successful_sources = 0
            failed_sources = 0
            
            for source_config in CLAUDE_FOCUSED_SOURCES:
                try:
                    # Create source metadata
                    metadata = SourceMetadata(
                        source_id=source_config["source_id"],
                        source_name=source_config["source_name"],
                        source_url=source_config["source_url"],
                        source_type=SourceType.RSS,
                        authority_score=source_config["authority_score"],
                        update_frequency="hourly",
                        topics=source_config["topics"]
                    )
                    
                    # Create monitor
                    monitor = RSSSourceMonitor(metadata, {
                        "timeout": 30,
                        "max_items": 20,
                        "enable_language_filtering": True
                    })
                    
                    # Run monitoring
                    result = await monitor.monitor()
                    
                    if result.success:
                        successful_sources += 1
                        total_items += len(result.new_items)
                        
                        # Store new items
                        for item in result.new_items:
                            await self.storage.store_content(item)
                        
                        logger.info(f"✅ {source_config['source_name']}: {len(result.new_items)} new items")
                    else:
                        failed_sources += 1
                        logger.warning(f"⚠️ {source_config['source_name']}: Failed - {result.errors}")
                        
                except Exception as e:
                    failed_sources += 1
                    logger.error(f"❌ Error monitoring {source_config['source_name']}: {e}")
            
            # Update stats
            self.stats["total_runs"] += 1
            self.stats["successful_runs"] += 1
            self.stats["total_items_collected"] += total_items
            self.stats["last_run"] = start_time.isoformat()
            
            duration = (datetime.now() - start_time).total_seconds()
            
            result = {
                "success": True,
                "duration_seconds": duration,
                "sources_monitored": successful_sources + failed_sources,
                "successful_sources": successful_sources,
                "failed_sources": failed_sources,
                "new_items": total_items,
                "timestamp": start_time.isoformat()
            }
            
            logger.info(f"📊 Monitoring complete: {total_items} new items from {successful_sources} sources in {duration:.1f}s")
            
            # Save stats
            self._save_stats()
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Monitoring cycle failed: {e}")
            self.stats["failed_runs"] += 1
            self.stats["last_run"] = start_time.isoformat()
            
            return {
                "success": False,
                "error": str(e),
                "timestamp": start_time.isoformat()
            }
    
    async def run_continuous(self):
        """Run continuous monitoring with scheduled intervals"""
        self.running = True
        logger.info(f"🚀 Starting auto-monitor with {self.interval/60:.0f} minute intervals")
        
        while self.running:
            # Calculate next run time
            next_run = datetime.now() + timedelta(seconds=self.interval)
            self.stats["next_run"] = next_run.isoformat()
            
            # Run monitoring
            await self.monitor_once()
            
            # Wait for next cycle
            if self.running:
                logger.info(f"💤 Next run at {next_run.strftime('%H:%M:%S')}")
                await asyncio.sleep(self.interval)
    
    def _save_stats(self):
        """Save monitoring statistics to file"""
        stats_file = Path("monitoring_stats.json")
        try:
            with open(stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save stats: {e}")
    
    def load_stats(self):
        """Load previous monitoring statistics"""
        stats_file = Path("monitoring_stats.json")
        if stats_file.exists():
            try:
                with open(stats_file, 'r') as f:
                    self.stats = json.load(f)
                logger.info(f"📈 Loaded stats: {self.stats['total_runs']} previous runs")
            except Exception as e:
                logger.error(f"Failed to load stats: {e}")

async def main():
    """Main entry point for auto-monitor"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Automated Topic Intelligence Monitor")
    parser.add_argument(
        "--interval",
        type=int,
        default=30,
        help="Monitoring interval in minutes (default: 30)"
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="Run once and exit"
    )
    
    args = parser.parse_args()
    
    # Create monitor
    monitor = AutoMonitor(interval_minutes=args.interval)
    monitor.load_stats()
    
    print("🤖 Universal Topic Intelligence Auto-Monitor")
    print("=" * 50)
    print(f"📍 Monitoring {len(CLAUDE_FOCUSED_SOURCES)} Claude-focused sources")
    print(f"⏱️  Interval: Every {args.interval} minutes")
    print(f"📊 Previous runs: {monitor.stats.get('total_runs', 0)}")
    print(f"📈 Total items collected: {monitor.stats.get('total_items_collected', 0)}")
    
    if monitor.stats.get('last_run'):
        print(f"⏰ Last run: {monitor.stats['last_run']}")
    
    print("=" * 50)
    print("Press Ctrl+C to stop\n")
    
    if args.once:
        # Run once and exit
        result = await monitor.monitor_once()
        if result["success"]:
            print(f"\n✅ Monitoring complete: {result['new_items']} new items")
        else:
            print(f"\n❌ Monitoring failed: {result.get('error', 'Unknown error')}")
    else:
        # Run continuously
        await monitor.run_continuous()

if __name__ == "__main__":
    asyncio.run(main())