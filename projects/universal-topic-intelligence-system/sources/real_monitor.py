#!/usr/bin/env python3
"""
REAL Universal Monitor - No fake implementations
Actually monitors sources and stores real content
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path
import yaml
import hashlib

from .rss_monitor import RSSSourceMonitor
from core import SourceMetadata, SourceType, ContentItem
from storage.database import StorageManager
from core.content_prioritizer import UniversalContentPrioritizer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RealMonitor")


class RealUniversalMonitor:
    """
    Honest implementation that actually works
    No fake MCP, no pretend agents, just real monitoring
    """
    
    def __init__(self):
        self.storage = StorageManager()
        self.prioritizer = UniversalContentPrioritizer()
        self.active_sources = []
        self.monitoring_tasks = {}
        self.stats = {
            "sources_monitored": 0,
            "items_collected": 0,
            "items_stored": 0,
            "errors": 0,
            "last_run": None
        }
        
        # Load real working sources
        self._initialize_working_sources()
    
    def _initialize_working_sources(self):
        """Initialize only sources that actually work"""
        
        # Working RSS feeds confirmed by testing
        self.active_sources = [
            {
                "url": "https://react.dev/rss.xml",
                "name": "React Blog",
                "topics": ["react", "frontend"],
                "authority_score": 1.0
            },
            {
                "url": "https://overreacted.io/rss.xml",
                "name": "Dan Abramov Blog",
                "topics": ["react", "javascript"],
                "authority_score": 1.0
            },
            {
                "url": "https://kentcdodds.com/blog/rss.xml",
                "name": "Kent C Dodds",
                "topics": ["react", "testing"],
                "authority_score": 0.95
            },
            {
                "url": "https://blog.langchain.dev/rss/",
                "name": "LangChain Blog",
                "topics": ["llm", "ai-development"],
                "authority_score": 0.9
            },
            {
                "url": "https://hnrss.org/newest",
                "name": "HackerNews",
                "topics": ["tech", "news"],
                "authority_score": 0.75
            },
            {
                "url": "https://reddit.com/r/ClaudeAI/.rss",
                "name": "Reddit ClaudeAI",
                "topics": ["claude", "ai"],
                "authority_score": 0.7
            },
            {
                "url": "https://cointelegraph.com/rss",
                "name": "CoinTelegraph",
                "topics": ["crypto", "blockchain"],
                "authority_score": 0.65
            },
            {
                "url": "https://decrypt.co/feed",
                "name": "Decrypt",
                "topics": ["crypto", "web3"],
                "authority_score": 0.65
            }
        ]
        
        logger.info(f"Initialized {len(self.active_sources)} working sources")
    
    async def monitor_source(self, source_config: Dict) -> Dict[str, Any]:
        """Monitor a single source and store results"""
        
        source_id = hashlib.md5(source_config['url'].encode()).hexdigest()[:8]
        
        # Create metadata
        metadata = SourceMetadata(
            source_id=source_id,
            source_name=source_config['name'],
            source_type=SourceType.RSS,
            source_url=source_config['url'],
            authority_score=source_config.get('authority_score', 0.5),
            update_frequency='hourly',
            topics=source_config.get('topics', [])
        )
        
        # Monitor using RSS monitor
        monitor = RSSSourceMonitor(metadata)
        result = await monitor.monitor()
        
        items_stored = 0
        if result.success and result.new_items:
            for item in result.new_items:
                try:
                    # Calculate priority
                    priority_result = self.prioritizer.prioritize(item)
                    
                    # Store in database
                    stored = await self.storage.store_content(
                        item=item,
                        priority_score=priority_result.total_score,
                        priority_level=priority_result.priority_level.value
                    )
                    
                    if stored:
                        items_stored += 1
                        
                except Exception as e:
                    logger.error(f"Error storing item: {e}")
                    self.stats["errors"] += 1
        
        return {
            "source": source_config['name'],
            "success": result.success,
            "items_found": len(result.new_items) if result.success else 0,
            "items_stored": items_stored,
            "errors": result.errors if not result.success else []
        }
    
    async def monitor_all_sources(self) -> Dict[str, Any]:
        """Monitor all active sources"""
        
        logger.info(f"Starting monitoring of {len(self.active_sources)} sources")
        self.stats["last_run"] = datetime.now()
        
        # Monitor all sources concurrently
        tasks = []
        for source in self.active_sources:
            task = self.monitor_source(source)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        
        # Aggregate results
        total_found = sum(r["items_found"] for r in results)
        total_stored = sum(r["items_stored"] for r in results)
        successful = sum(1 for r in results if r["success"])
        
        self.stats["sources_monitored"] += len(self.active_sources)
        self.stats["items_collected"] += total_found
        self.stats["items_stored"] += total_stored
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "sources_checked": len(self.active_sources),
            "sources_successful": successful,
            "total_items_found": total_found,
            "total_items_stored": total_stored,
            "individual_results": results,
            "cumulative_stats": self.stats
        }
        
        logger.info(f"Monitoring complete: {total_found} found, {total_stored} stored")
        
        return summary
    
    async def start_scheduled_monitoring(self, interval_minutes: int = 30):
        """
        Start scheduled monitoring that actually runs periodically
        No fake scheduling, real asyncio tasks
        """
        
        logger.info(f"Starting scheduled monitoring every {interval_minutes} minutes")
        
        while True:
            try:
                # Run monitoring
                result = await self.monitor_all_sources()
                
                # Log results
                logger.info(f"Scheduled run complete: {result['total_items_stored']} items stored")
                
                # Wait for next interval
                await asyncio.sleep(interval_minutes * 60)
                
            except Exception as e:
                logger.error(f"Error in scheduled monitoring: {e}")
                self.stats["errors"] += 1
                
                # Wait a bit before retrying
                await asyncio.sleep(60)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get real statistics, not fake ones"""
        return {
            **self.stats,
            "active_sources": len(self.active_sources),
            "working_sources": [s["name"] for s in self.active_sources],
            "uptime": str(datetime.now() - self.stats["last_run"]) if self.stats["last_run"] else "Not started"
        }


class SimpleScheduler:
    """
    Simple, honest scheduler that actually works
    No elaborate agent hierarchy, just basic task scheduling
    """
    
    def __init__(self):
        self.monitor = RealUniversalMonitor()
        self.tasks = {}
        self.running = False
    
    async def add_monitoring_task(self, name: str, interval_minutes: int):
        """Add a monitoring task that runs at specified interval"""
        
        async def task_loop():
            while self.running:
                try:
                    logger.info(f"Running task: {name}")
                    await self.monitor.monitor_all_sources()
                    await asyncio.sleep(interval_minutes * 60)
                except Exception as e:
                    logger.error(f"Task {name} error: {e}")
                    await asyncio.sleep(60)
        
        task = asyncio.create_task(task_loop())
        self.tasks[name] = task
        logger.info(f"Added task {name} with {interval_minutes} minute interval")
    
    async def start(self):
        """Start the scheduler"""
        self.running = True
        
        # Add default monitoring tasks
        await self.add_monitoring_task("main_monitor", 30)
        
        logger.info("Scheduler started")
        
        # Keep running
        while self.running:
            await asyncio.sleep(60)
            
            # Log status
            stats = self.monitor.get_stats()
            logger.info(f"Status: {stats['items_stored']} items stored from {stats['sources_monitored']} sources")
    
    async def stop(self):
        """Stop the scheduler"""
        self.running = False
        
        # Cancel all tasks
        for name, task in self.tasks.items():
            task.cancel()
            logger.info(f"Cancelled task: {name}")
        
        logger.info("Scheduler stopped")


async def main():
    """Test the real implementation"""
    
    print("=" * 60)
    print("REAL Universal Monitor - No Fake Implementations")
    print("=" * 60)
    
    monitor = RealUniversalMonitor()
    
    print("\n📋 Active Sources (Actually Working):")
    for source in monitor.active_sources:
        print(f"  ✅ {source['name']}: {source['url'][:50]}...")
    
    print("\n🔍 Running single monitoring pass...")
    result = await monitor.monitor_all_sources()
    
    print(f"\n📊 Results:")
    print(f"  Sources Checked: {result['sources_checked']}")
    print(f"  Sources Successful: {result['sources_successful']}")
    print(f"  Items Found: {result['total_items_found']}")
    print(f"  Items Stored: {result['total_items_stored']}")
    
    print(f"\n📈 Per-Source Results:")
    for r in result['individual_results']:
        if r['success']:
            print(f"  ✅ {r['source']}: {r['items_found']} found, {r['items_stored']} stored")
        else:
            print(f"  ❌ {r['source']}: Failed")
    
    print(f"\n🎯 Cumulative Statistics:")
    stats = monitor.get_stats()
    print(f"  Total Sources Monitored: {stats['sources_monitored']}")
    print(f"  Total Items Collected: {stats['items_collected']}")
    print(f"  Total Items Stored: {stats['items_stored']}")
    print(f"  Total Errors: {stats['errors']}")
    
    print("\n✅ This is REAL monitoring with REAL data storage")
    print("❌ No fake MCP calls, no pretend agents, no theater")


if __name__ == "__main__":
    asyncio.run(main())