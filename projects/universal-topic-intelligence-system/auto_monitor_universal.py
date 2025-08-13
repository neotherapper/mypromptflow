#!/usr/bin/env python3
"""
Universal Automated Monitoring Scheduler
Periodically refreshes content from all configured topic sources using Universal Topic Monitor
"""

import asyncio
import logging
import signal
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import json

# Import universal monitoring components
from agents.queen_agent import QueenAgent
from sources.universal_topic_monitor import UniversalTopicMonitor
from storage.database import StorageManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("UniversalAutoMonitor")


class UniversalAutoMonitor:
    """Universal automated monitoring scheduler for multi-topic intelligence gathering"""
    
    def __init__(self, interval_minutes: int = 30, topics_filter: Optional[List[str]] = None):
        """
        Initialize universal auto monitor
        
        Args:
            interval_minutes: How often to refresh content (default: 30 minutes)
            topics_filter: List of topic slugs to monitor (None = monitor all active topics)
        """
        self.interval = interval_minutes * 60  # Convert to seconds
        self.running = False
        self.topics_filter = topics_filter
        
        # Initialize components
        self.queen = QueenAgent()
        self.storage = StorageManager()
        self.topic_monitor = UniversalTopicMonitor()
        
        # Get available topics
        self.available_topics = self.topic_monitor.list_available_topics()
        self.monitored_topics = self._get_monitored_topics()
        
        self.stats = {
            "total_runs": 0,
            "successful_runs": 0,
            "failed_runs": 0,
            "total_items_collected": 0,
            "last_run": None,
            "next_run": None,
            "topics_monitored": len(self.monitored_topics),
            "topic_stats": {},
            "configuration": {
                "interval_minutes": interval_minutes,
                "topics_filter": topics_filter,
                "available_topics": [t['slug'] for t in self.available_topics]
            }
        }
        
        # Initialize topic stats
        for topic in self.monitored_topics:
            self.stats["topic_stats"][topic] = {
                "total_items": 0,
                "successful_runs": 0,
                "failed_runs": 0,
                "last_success": None,
                "avg_items_per_run": 0.0
            }
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        logger.info(f"🎯 Universal Auto Monitor initialized")
        logger.info(f"   Topics: {', '.join(self.monitored_topics)}")
        logger.info(f"   Interval: {interval_minutes} minutes")
    
    def _get_monitored_topics(self) -> List[str]:
        """Get list of topics to monitor based on filter"""
        active_topics = [t['slug'] for t in self.available_topics if t['status'] == 'active']
        
        if self.topics_filter:
            # Filter to specified topics
            monitored = [t for t in active_topics if t in self.topics_filter]
            missing_topics = set(self.topics_filter) - set(active_topics)
            if missing_topics:
                logger.warning(f"⚠️  Filtered topics not available: {', '.join(missing_topics)}")
        else:
            # Monitor all active topics
            monitored = active_topics
        
        return monitored
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info("🛑 Received shutdown signal, stopping universal monitor...")
        self.running = False
        sys.exit(0)
    
    async def monitor_once(self) -> Dict[str, Any]:
        """
        Run a single monitoring cycle across all configured topics
        
        Returns:
            Results of the monitoring run with per-topic breakdown
        """
        logger.info(f"🔄 Starting universal monitoring cycle for {len(self.monitored_topics)} topics...")
        start_time = datetime.now()
        
        try:
            cycle_results = {}
            total_items = 0
            successful_topics = 0
            failed_topics = 0
            
            # Monitor each topic
            for topic_slug in self.monitored_topics:
                try:
                    logger.info(f"📊 Monitoring topic: {topic_slug}")
                    topic_result = await self.topic_monitor.monitor_topic(topic_slug)
                    
                    # Extract items from monitoring results
                    topic_items = 0
                    successful_sources = 0
                    failed_sources = 0
                    
                    for source_id, source_result in topic_result['results'].items():
                        if 'error' in source_result:
                            failed_sources += 1
                        else:
                            successful_sources += 1
                            source_items = source_result.get('items_found', 0)
                            topic_items += source_items
                    
                    # Store results
                    cycle_results[topic_slug] = {
                        "success": True,
                        "sources_monitored": topic_result['sources_monitored'],
                        "successful_sources": successful_sources,
                        "failed_sources": failed_sources,
                        "items_found": topic_items,
                        "raw_results": topic_result
                    }
                    
                    # Update topic stats
                    topic_stats = self.stats["topic_stats"][topic_slug]
                    topic_stats["total_items"] += topic_items
                    topic_stats["successful_runs"] += 1
                    topic_stats["last_success"] = start_time.isoformat()
                    if topic_stats["successful_runs"] > 0:
                        topic_stats["avg_items_per_run"] = topic_stats["total_items"] / topic_stats["successful_runs"]
                    
                    total_items += topic_items
                    successful_topics += 1
                    
                    logger.info(f"✅ {topic_slug}: {topic_items} items from {successful_sources} sources")
                    
                except Exception as e:
                    failed_topics += 1
                    self.stats["topic_stats"][topic_slug]["failed_runs"] += 1
                    
                    cycle_results[topic_slug] = {
                        "success": False,
                        "error": str(e),
                        "items_found": 0
                    }
                    
                    logger.error(f"❌ Error monitoring topic {topic_slug}: {e}")
            
            # Update overall stats
            self.stats["total_runs"] += 1
            self.stats["successful_runs"] += 1
            self.stats["total_items_collected"] += total_items
            self.stats["last_run"] = start_time.isoformat()
            
            duration = (datetime.now() - start_time).total_seconds()
            
            result = {
                "success": True,
                "duration_seconds": duration,
                "topics_monitored": len(self.monitored_topics),
                "successful_topics": successful_topics,
                "failed_topics": failed_topics,
                "total_new_items": total_items,
                "timestamp": start_time.isoformat(),
                "topic_results": cycle_results,
                "summary": {
                    "total_sources": sum(r.get('sources_monitored', 0) for r in cycle_results.values()),
                    "successful_sources": sum(r.get('successful_sources', 0) for r in cycle_results.values()),
                    "failed_sources": sum(r.get('failed_sources', 0) for r in cycle_results.values())
                }
            }
            
            logger.info(f"📊 Universal monitoring complete:")
            logger.info(f"   {total_items} total items from {successful_topics}/{len(self.monitored_topics)} topics")
            logger.info(f"   Duration: {duration:.1f}s")
            
            # Save stats
            self._save_stats()
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Universal monitoring cycle failed: {e}")
            self.stats["failed_runs"] += 1
            self.stats["last_run"] = start_time.isoformat()
            
            return {
                "success": False,
                "error": str(e),
                "timestamp": start_time.isoformat(),
                "topics_monitored": len(self.monitored_topics)
            }
    
    async def run_continuous(self):
        """Run continuous monitoring with scheduled intervals"""
        self.running = True
        logger.info(f"🚀 Starting universal auto-monitor")
        logger.info(f"   Interval: {self.interval/60:.0f} minutes")
        logger.info(f"   Topics: {', '.join(self.monitored_topics)}")
        
        while self.running:
            # Calculate next run time
            next_run = datetime.now() + timedelta(seconds=self.interval)
            self.stats["next_run"] = next_run.isoformat()
            
            # Run monitoring
            await self.monitor_once()
            
            # Wait for next cycle
            if self.running:
                logger.info(f"💤 Next universal run at {next_run.strftime('%H:%M:%S')}")
                await asyncio.sleep(self.interval)
    
    async def monitor_topic(self, topic_slug: str) -> Dict[str, Any]:
        """Monitor a specific topic once"""
        if topic_slug not in self.monitored_topics:
            raise ValueError(f"Topic '{topic_slug}' is not in monitored topics: {self.monitored_topics}")
        
        logger.info(f"🎯 Single-topic monitoring: {topic_slug}")
        return await self.topic_monitor.monitor_topic(topic_slug)
    
    async def monitor_by_keywords(self, keywords: List[str]) -> Dict[str, Any]:
        """Monitor topics that match specific keywords"""
        logger.info(f"🔍 Keyword-based monitoring: {', '.join(keywords)}")
        return await self.topic_monitor.monitor_by_keywords(keywords)
    
    def add_topic_filter(self, topic_slug: str):
        """Add a topic to the monitoring filter"""
        if not self.topics_filter:
            self.topics_filter = []
        
        if topic_slug not in self.topics_filter:
            self.topics_filter.append(topic_slug)
            self.monitored_topics = self._get_monitored_topics()
            
            # Initialize stats for new topic
            if topic_slug not in self.stats["topic_stats"]:
                self.stats["topic_stats"][topic_slug] = {
                    "total_items": 0,
                    "successful_runs": 0,
                    "failed_runs": 0,
                    "last_success": None,
                    "avg_items_per_run": 0.0
                }
            
            logger.info(f"➕ Added topic to filter: {topic_slug}")
    
    def remove_topic_filter(self, topic_slug: str):
        """Remove a topic from the monitoring filter"""
        if self.topics_filter and topic_slug in self.topics_filter:
            self.topics_filter.remove(topic_slug)
            self.monitored_topics = self._get_monitored_topics()
            logger.info(f"➖ Removed topic from filter: {topic_slug}")
    
    def get_topic_info(self, topic_slug: str) -> Optional[Dict]:
        """Get information about a specific topic"""
        return self.topic_monitor.get_topic_info(topic_slug)
    
    def list_available_topics(self) -> List[Dict]:
        """List all available topics"""
        return self.available_topics
    
    def get_monitoring_summary(self) -> Dict[str, Any]:
        """Get comprehensive monitoring statistics"""
        return {
            "configuration": self.stats["configuration"],
            "overall_stats": {
                "total_runs": self.stats["total_runs"],
                "successful_runs": self.stats["successful_runs"],
                "failed_runs": self.stats["failed_runs"],
                "total_items_collected": self.stats["total_items_collected"],
                "last_run": self.stats["last_run"],
                "next_run": self.stats["next_run"]
            },
            "topic_stats": self.stats["topic_stats"],
            "monitored_topics": self.monitored_topics,
            "available_topics": [t['slug'] for t in self.available_topics],
            "system_health": {
                "success_rate": (self.stats["successful_runs"] / max(self.stats["total_runs"], 1)) * 100,
                "avg_items_per_run": self.stats["total_items_collected"] / max(self.stats["total_runs"], 1)
            }
        }
    
    def _save_stats(self):
        """Save monitoring statistics to file"""
        stats_file = Path("universal_monitoring_stats.json")
        try:
            with open(stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except Exception as e:
            logger.error(f"❌ Error saving stats: {e}")


# Convenience functions for backward compatibility and easy usage
async def monitor_all_topics():
    """Monitor all available topics once"""
    monitor = UniversalAutoMonitor()
    return await monitor.monitor_once()


async def monitor_specific_topics(topics: List[str]):
    """Monitor specific topics once"""
    monitor = UniversalAutoMonitor(topics_filter=topics)
    return await monitor.monitor_once()


async def monitor_ai_topics():
    """Monitor AI/ML related topics (backward compatibility with Claude monitoring)"""
    monitor = UniversalAutoMonitor()
    ai_keywords = ["ai", "ml", "claude", "llm", "artificial intelligence"]
    return await monitor.monitor_by_keywords(ai_keywords)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Universal Topic Intelligence Auto Monitor")
    parser.add_argument("--interval", type=int, default=30,
                        help="Monitoring interval in minutes (default: 30)")
    parser.add_argument("--topics", nargs="+", 
                        help="Specific topics to monitor (default: all active topics)")
    parser.add_argument("--once", action="store_true",
                        help="Run monitoring once instead of continuously")
    parser.add_argument("--stats", action="store_true",
                        help="Show monitoring statistics")
    
    args = parser.parse_args()
    
    async def main():
        monitor = UniversalAutoMonitor(
            interval_minutes=args.interval,
            topics_filter=args.topics
        )
        
        if args.stats:
            # Show statistics
            summary = monitor.get_monitoring_summary()
            print(json.dumps(summary, indent=2))
            return
        
        if args.once:
            # Run once
            result = await monitor.monitor_once()
            print(json.dumps(result, indent=2))
        else:
            # Run continuously
            await monitor.run_continuous()
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Universal monitoring stopped by user")
    except Exception as e:
        logger.error(f"❌ Universal monitoring error: {e}")
        sys.exit(1)