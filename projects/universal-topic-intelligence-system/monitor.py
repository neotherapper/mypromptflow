#!/usr/bin/env python3
"""
Universal Topic Intelligence Monitor - CONSOLIDATED WORKING VERSION
Only includes functional components, no fake implementations
"""

import asyncio
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

from sources.rss_monitor import RSSSourceMonitor
from sources.production_mcp_integration import ProductionMCPIntegration
from sources.real_mcp_monitor import MCP_TEST_CONFIG
from core import SourceMetadata, SourceType
from core.language_filter import LanguageFilter
from core.relevance_filter import RelevanceFilter
from core.incremental_updater import IncrementalUpdateManager
from core.source_health_monitor import SourceHealthMonitor
from storage.database import StorageManager
from core.content_prioritizer import UniversalContentPrioritizer
from core.trend_detection_engine import TrendDetectionEngine
from core.noise_reduction_engine import NoiseReductionEngine
from core.scheduler import UniversalScheduler, ScheduledTask

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("UniversalMonitor")


class UniversalMonitor:
    """
    Consolidated universal monitor - only working functionality
    """
    
    def __init__(self):
        self.storage = StorageManager()
        self.prioritizer = UniversalContentPrioritizer()
        self.language_filter = LanguageFilter(target_languages=['en'], min_confidence=0.7)
        self.relevance_filter = RelevanceFilter()
        self.trend_detector = TrendDetectionEngine()
        self.noise_filter = NoiseReductionEngine()
        self.incremental_updater = IncrementalUpdateManager()
        self.health_monitor = SourceHealthMonitor()
        
        # Initialize scheduler
        self.scheduler = UniversalScheduler("topic_intelligence_scheduler.json")
        self.scheduler.set_task_executor(self._execute_scheduled_monitoring)
        
        # Core verified sources
        self.working_sources = [
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
                "topics": ["llm", "ai"],
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
                "topics": ["crypto"],
                "authority_score": 0.65
            },
            {
                "url": "https://decrypt.co/feed",
                "name": "Decrypt",
                "topics": ["crypto"],
                "authority_score": 0.65
            }
        ]
        
        # Load devtools ecosystem sources from topic configuration
        self.devtools_sources = self._load_devtools_sources()
        
        # Add MCP monitoring configuration
        self.mcp_sources = [
            {
                "name": "React YouTube Content",
                "type": "youtube_mcp",
                "config": MCP_TEST_CONFIG["youtube_react_videos"],
                "topics": ["react", "javascript"]
            },
            {
                "name": "React GitHub Repositories", 
                "type": "github_mcp",
                "config": MCP_TEST_CONFIG["github_react_repos"],
                "topics": ["react", "javascript"]
            },
            {
                "name": "Claude AI News Search",
                "type": "search_mcp", 
                "config": MCP_TEST_CONFIG["search_claude_news"],
                "topics": ["claude", "ai"]
            }
        ]
        
        # Combined sources for monitoring
        all_rss_sources = self.working_sources + self.devtools_sources
        self.all_sources = all_rss_sources
        
        self.stats = {
            "sources_total": len(all_rss_sources) + len(self.mcp_sources),
            "sources_successful": 0,
            "sources_failed": 0,
            "items_found": 0,
            "items_stored": 0,
            "last_run": None
        }
    
    def _load_devtools_sources(self) -> List[Dict]:
        """Load devtools ecosystem sources from topic configuration"""
        import yaml
        from pathlib import Path
        
        try:
            config_path = Path("topics/devtools-ecosystem.yaml")
            if config_path.exists():
                with open(config_path, 'r') as f:
                    config = yaml.safe_load(f)
                
                devtools_sources = []
                for source in config.get('sources', []):
                    if source.get('type') == 'rss' and source.get('rss_url'):
                        devtools_sources.append({
                            "url": source['rss_url'],
                            "name": source['name'],
                            "topics": source.get('categories', ['devtools']),
                            "authority_score": source.get('authority', 0.8)
                        })
                
                logger.info(f"Loaded {len(devtools_sources)} devtools ecosystem RSS sources")
                return devtools_sources
                
        except Exception as e:
            logger.error(f"Error loading devtools sources: {e}")
            
        return []
    
    async def monitor_source(self, source_config: Dict) -> Dict[str, Any]:
        """Monitor a single source"""
        
        # Generate source ID from URL hash
        import hashlib
        source_id = hashlib.md5(source_config['url'].encode()).hexdigest()[:8]
        
        # Track monitoring start time for health metrics
        start_time = datetime.now()
        
        # Create metadata
        metadata = SourceMetadata(
            source_id=source_id,
            source_name=source_config['name'],
            source_type=SourceType.RSS,
            source_url=source_config['url'],
            authority_score=source_config['authority_score'],
            update_frequency='hourly',
            topics=source_config['topics']
        )
        
        # Register source with incremental updater if missing
        self.incremental_updater.register_source_if_missing(metadata)
        
        # Monitor using RSS
        monitor = RSSSourceMonitor(metadata)
        result = await monitor.monitor()
        
        # Calculate response time
        response_time_ms = int((datetime.now() - start_time).total_seconds() * 1000)
        
        items_stored = 0
        items_filtered_out = 0
        if result.success and result.new_items:
            # Apply incremental filtering to avoid reprocessing old content
            raw_items_data = []
            for item in result.new_items:
                # Convert ContentItem back to dict format for incremental filtering
                item_dict = {
                    'id': item.item_id,
                    'title': item.title,
                    'published': item.published_date.isoformat() if item.published_date else None
                }
                raw_items_data.append((item_dict, item))
            
            # Filter for new items only
            if raw_items_data:
                raw_dicts = [item_data[0] for item_data in raw_items_data]
                filtered_dicts = self.incremental_updater.filter_new_items(source_id, raw_dicts)
                filtered_dict_ids = {d['id'] for d in filtered_dicts}
                
                # Get the corresponding ContentItems
                filtered_items = [item_data[1] for item_data in raw_items_data 
                                if item_data[0]['id'] in filtered_dict_ids]
                
                logger.info(f"Incremental filtering: {len(result.new_items)} total items, {len(filtered_items)} new items to process")
            else:
                filtered_items = []
            
            for item in filtered_items:
                try:
                    # Apply language filter
                    should_include, lang_result = self.language_filter.should_include_content(
                        item.title, 
                        item.content or ""
                    )
                    
                    if not should_include:
                        items_filtered_out += 1
                        logger.debug(f"Filtered non-English content: {item.title[:50]}... (detected: {lang_result.language})")
                        continue
                    
                    # Apply noise filter
                    should_filter, noise_result = self.noise_filter.should_filter_content(item)
                    
                    if should_filter:
                        items_filtered_out += 1
                        logger.info(f"Filtered noisy content: {item.title[:50]}... (reason: {noise_result.reasoning})")
                        continue
                    
                    # Calculate priority using intelligent strategy
                    priority_result = self.prioritizer.prioritize(item, strategy="intelligent")
                    
                    # Store in database
                    stored = await self.storage.store_content(
                        item=item,
                        priority_score=priority_result.total_score,
                        priority_level=priority_result.priority_level.value
                    )
                    
                    if stored:
                        items_stored += 1
                        
                        # Add to trend detection engine
                        try:
                            self.trend_detector.add_content_signal(item, priority_result.total_score)
                        except Exception as e:
                            logger.error(f"Error adding trend signal for {item.item_id}: {e}")
                        
                except Exception as e:
                    logger.error(f"Error storing item from {source_config['name']}: {e}")
        
        # Update last fetch timestamp if monitoring was successful
        if result.success:
            try:
                self.incremental_updater.update_last_fetch_time(source_id)
                logger.debug(f"Updated last fetch timestamp for {source_config['name']}")
            except Exception as e:
                logger.error(f"Error updating last fetch timestamp for {source_config['name']}: {e}")
        
        # Record health check results
        error_type = None
        error_message = None
        
        if not result.success and result.errors:
            error_full = result.errors[0]
            # Parse common error types from error messages
            if "404" in error_full or "Not Found" in error_full:
                error_type = "404"
            elif "403" in error_full or "Forbidden" in error_full:
                error_type = "403" 
            elif "timeout" in error_full.lower():
                error_type = "timeout"
            elif "ssl" in error_full.lower() or "certificate" in error_full.lower():
                error_type = "ssl_error"
            elif "connection" in error_full.lower():
                error_type = "connection_error"
            else:
                error_type = "unknown"
            error_message = error_full
        
        try:
            self.health_monitor.record_check(
                source_id=source_id,
                source_name=source_config['name'],
                success=result.success,
                response_time_ms=response_time_ms,
                error_type=error_type,
                error_message=error_message,
                items_found=len(result.new_items) if result.success else 0,
                items_stored=items_stored
            )
        except Exception as e:
            logger.error(f"Error recording health check for {source_config['name']}: {e}")
        
        return {
            "source": source_config['name'],
            "url": source_config['url'][:50] + "...",
            "success": result.success,
            "items_found": len(result.new_items) if result.success else 0,
            "items_filtered": items_filtered_out,
            "items_stored": items_stored,
            "response_time_ms": response_time_ms,
            "error": None if result.success else (result.errors[0] if result.errors else "Unknown error")
        }
    
    async def monitor_mcp_source(self, mcp_config: Dict) -> Dict[str, Any]:
        """Monitor an MCP source"""
        
        # Generate MCP source ID
        import hashlib
        source_id = hashlib.md5(f"mcp_{mcp_config['name']}".encode()).hexdigest()[:8]
        
        # Create metadata for MCP source
        metadata = SourceMetadata(
            source_id=source_id,
            source_name=mcp_config['name'],
            source_type=SourceType.API,
            source_url="https://mcp.example.com",
            authority_score=0.8,
            update_frequency="daily",
            topics=mcp_config['topics']
        )
        
        try:
            # Create production MCP integration
            mcp_integration = ProductionMCPIntegration()
            
            # Run monitoring based on MCP source type
            logger.info(f"Monitoring MCP source: {mcp_config['name']} ({mcp_config['type']})")
            
            collected_items = []
            
            if mcp_config['type'] == 'youtube_mcp':
                video_urls = mcp_config['config'].get('video_urls', [])
                if video_urls:
                    collected_items = await mcp_integration.extract_youtube_transcripts(video_urls[:3])
            
            elif mcp_config['type'] == 'github_mcp':
                repo_queries = mcp_config['config'].get('repo_queries', [])
                if repo_queries:
                    collected_items = await mcp_integration.search_github_repositories(repo_queries[:3])
            
            elif mcp_config['type'] == 'search_mcp':
                search_queries = mcp_config['config'].get('search_queries', [])
                if search_queries:
                    collected_items = await mcp_integration.search_web_content(search_queries[:2])
            
            # Create monitoring result
            monitoring_result = type('MonitoringResult', (), {
                'success': len(collected_items) > 0,
                'new_items': collected_items,
                'items_found': len(collected_items),
                'errors': [] if collected_items else ['No items collected']
            })()
            
            if not monitoring_result.success:
                return {
                    "source": mcp_config['name'],
                    "url": f"MCP:{mcp_config['type']}",
                    "success": False,
                    "items_found": 0,
                    "items_stored": 0,
                    "error": monitoring_result.errors[0] if monitoring_result.errors else "MCP monitoring failed"
                }
            
            # Store items in database
            items_stored = 0
            items_filtered_out = 0
            for item in monitoring_result.new_items:
                try:
                    # Apply language filter
                    should_include, lang_result = self.language_filter.should_include_content(
                        item.title, 
                        item.content or ""
                    )
                    
                    if not should_include:
                        items_filtered_out += 1
                        logger.debug(f"Filtered non-English MCP content: {item.title[:50]}... (detected: {lang_result.language})")
                        continue
                    
                    # Apply noise filter
                    should_filter, noise_result = self.noise_filter.should_filter_content(item)
                    
                    if should_filter:
                        items_filtered_out += 1
                        logger.info(f"Filtered noisy MCP content: {item.title[:50]}... (reason: {noise_result.reasoning})")
                        continue
                    
                    # Apply relevance filter
                    is_relevant, relevance_score, reason = self.relevance_filter.is_relevant(
                        item.title,
                        item.content or "",
                        item.topics
                    )
                    
                    if not is_relevant:
                        items_filtered_out += 1
                        logger.debug(f"Filtered irrelevant MCP content: {item.title[:50]}... ({reason})")
                        continue
                    
                    # Calculate priority using intelligent strategy
                    priority_result = self.prioritizer.prioritize(item, strategy="intelligent")
                    
                    # Store item
                    stored = await self.storage.store_content(
                        item=item,
                        priority_score=priority_result.total_score,
                        priority_level=priority_result.priority_level.value
                    )
                    
                    if stored:
                        items_stored += 1
                        logger.info(f"Stored MCP item: {item.title[:60]}... (Priority: {priority_result.priority_level.value})")
                        
                        # Add to trend detection engine
                        try:
                            self.trend_detector.add_content_signal(item, priority_result.total_score)
                        except Exception as e:
                            logger.error(f"Error adding MCP trend signal for {item.item_id}: {e}")
                    
                except Exception as e:
                    logger.error(f"Error storing MCP item {item.item_id}: {e}")
            
            return {
                "source": mcp_config['name'],
                "url": f"MCP:{mcp_config['type']}",
                "success": True,
                "items_found": monitoring_result.items_found,
                "items_filtered": items_filtered_out,
                "items_stored": items_stored,
                "error": None
            }
            
        except Exception as e:
            logger.error(f"MCP monitoring failed for {mcp_config['name']}: {e}")
            return {
                "source": mcp_config['name'],
                "url": f"MCP:{mcp_config['type']}",
                "success": False,
                "items_found": 0,
                "items_filtered": 0,
                "items_stored": 0,
                "error": str(e)
            }
    
    async def run_monitoring_cycle(self) -> Dict[str, Any]:
        """Run one complete monitoring cycle"""
        
        total_sources = len(self.all_sources) + len(self.mcp_sources)
        logger.info(f"Starting monitoring cycle for {total_sources} sources ({len(self.all_sources)} RSS (including {len(self.devtools_sources)} devtools) + {len(self.mcp_sources)} MCP)")
        self.stats["last_run"] = datetime.now()
        
        # Reset per-cycle stats
        self.stats["sources_successful"] = 0
        self.stats["sources_failed"] = 0
        cycle_items_found = 0
        cycle_items_stored = 0
        cycle_items_filtered = 0
        
        # Monitor all sources concurrently
        tasks = []
        
        # Add RSS source tasks (including devtools)
        for source in self.all_sources:
            task = self.monitor_source(source)
            tasks.append(task)
        
        # Add MCP source tasks
        for mcp_source in self.mcp_sources:
            task = self.monitor_mcp_source(mcp_source)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        source_results = []
        for result in results:
            if isinstance(result, Exception):
                logger.error(f"Source monitoring failed: {result}")
                self.stats["sources_failed"] += 1
            else:
                source_results.append(result)
                if result["success"]:
                    self.stats["sources_successful"] += 1
                    cycle_items_found += result["items_found"]
                    cycle_items_stored += result["items_stored"]
                    cycle_items_filtered += result.get("items_filtered", 0)
                else:
                    self.stats["sources_failed"] += 1
        
        # Update cumulative stats
        self.stats["items_found"] += cycle_items_found
        self.stats["items_stored"] += cycle_items_stored
        if "items_filtered" not in self.stats:
            self.stats["items_filtered"] = 0
        self.stats["items_filtered"] += cycle_items_filtered
        
        # Perform trend analysis if we have new items
        trend_summary = {}
        if cycle_items_stored > 0:
            try:
                trend_summary = self.trend_detector.get_trend_summary("short")
                logger.info(f"Trend analysis: {trend_summary['total_trends']} trends detected, "
                           f"{len(trend_summary['top_emerging'])} emerging topics")
            except Exception as e:
                logger.error(f"Error in trend analysis: {e}")
                trend_summary = {"error": str(e)}
        
        cycle_summary = {
            "timestamp": self.stats["last_run"].isoformat(),
            "sources_checked": total_sources,
            "rss_sources": len(self.all_sources),
            "devtools_sources": len(self.devtools_sources),
            "mcp_sources": len(self.mcp_sources),
            "sources_successful": self.stats["sources_successful"],
            "sources_failed": self.stats["sources_failed"],
            "items_found_this_cycle": cycle_items_found,
            "items_filtered_this_cycle": cycle_items_filtered,
            "items_stored_this_cycle": cycle_items_stored,
            "success_rate": f"{(self.stats['sources_successful'] / total_sources * 100):.1f}%",
            "filter_rate": f"{(cycle_items_filtered / max(1, cycle_items_found) * 100):.1f}%",
            "source_results": source_results,
            "cumulative_stats": self.stats.copy(),
            "trend_analysis": trend_summary
        }
        
        logger.info(f"Cycle complete: {cycle_items_found} found, {cycle_items_filtered} filtered, {cycle_items_stored} stored")
        
        return cycle_summary
    
    async def start_scheduled_monitoring(self, interval_minutes: int = 60):
        """Start continuous monitoring with specified interval"""
        
        logger.info(f"Starting scheduled monitoring every {interval_minutes} minutes")
        
        while True:
            try:
                # Run monitoring cycle
                result = await self.run_monitoring_cycle()
                
                # Log summary
                logger.info(f"Scheduled cycle: {result['items_stored_this_cycle']} items stored, "
                           f"{result['success_rate']} success rate")
                
                # Wait for next interval
                await asyncio.sleep(interval_minutes * 60)
                
            except KeyboardInterrupt:
                logger.info("Scheduled monitoring stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in scheduled monitoring: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retrying
    
    async def _execute_scheduled_monitoring(self, task: ScheduledTask) -> Dict[str, Any]:
        """Execute monitoring cycle for scheduled task"""
        try:
            # Run a monitoring cycle
            result = await self.run_monitoring_cycle()
            
            # Return standardized result for scheduler
            return {
                "items_found": result.get("items_found_this_cycle", 0),
                "items_stored": result.get("items_stored_this_cycle", 0),
                "metadata": {
                    "success_rate": result.get("success_rate", "0%"),
                    "sources_successful": result.get("sources_successful", 0),
                    "sources_failed": result.get("sources_failed", 0),
                    "trend_analysis": result.get("trend_analysis", {}),
                    "filter_rate": result.get("filter_rate", "0%")
                }
            }
        except Exception as e:
            logger.error(f"Scheduled monitoring failed: {e}")
            raise
    
    def setup_default_schedule(self):
        """Set up default monitoring schedule"""
        # Main monitoring cycle - every 30 minutes
        self.scheduler.add_task(
            task_id="main_monitoring",
            name="Main Topic Monitoring",
            interval_minutes=30,
            start_immediately=True,
            metadata={
                "description": "Monitor all RSS and MCP sources for new content",
                "sources_count": len(self.all_sources) + len(self.mcp_sources),
                "devtools_sources": len(self.devtools_sources)
            }
        )
        
        # Intensive monitoring for high-priority sources - every 10 minutes
        self.scheduler.add_task(
            task_id="priority_monitoring", 
            name="Priority Source Monitoring",
            interval_minutes=10,
            metadata={
                "description": "Monitor high-authority sources more frequently",
                "priority_sources": ["React Blog", "Dan Abramov Blog", "Reddit ClaudeAI"]
            }
        )
        
        logger.info("Default monitoring schedule configured")
    
    async def start_scheduled_monitoring(self):
        """Start the automated scheduler"""
        logger.info("Starting automated scheduled monitoring")
        
        # Set up default schedule if no tasks exist
        if not self.scheduler.tasks:
            self.setup_default_schedule()
        
        # Start the scheduler
        await self.scheduler.start()
    
    def get_scheduler_status(self) -> Dict[str, Any]:
        """Get scheduler status information"""
        return self.scheduler.get_task_status()
    
    def add_monitoring_schedule(self, 
                               name: str, 
                               interval_minutes: int,
                               start_immediately: bool = False) -> str:
        """
        Add a new monitoring schedule
        
        Args:
            name: Schedule name
            interval_minutes: How often to monitor
            start_immediately: Whether to start right away
            
        Returns:
            Task ID of the created schedule
        """
        task_id = f"monitor_{name.lower().replace(' ', '_')}"
        
        self.scheduler.add_task(
            task_id=task_id,
            name=f"{name} Monitoring",
            interval_minutes=interval_minutes,
            start_immediately=start_immediately,
            metadata={"custom_schedule": True, "schedule_name": name}
        )
        
        logger.info(f"Added custom monitoring schedule: {name} (every {interval_minutes} min)")
        return task_id
    
    def pause_schedule(self, task_id: str) -> bool:
        """Pause a monitoring schedule"""
        return self.scheduler.pause_task(task_id)
    
    def resume_schedule(self, task_id: str) -> bool:
        """Resume a paused monitoring schedule"""
        return self.scheduler.resume_task(task_id)
    
    def remove_schedule(self, task_id: str) -> bool:
        """Remove a monitoring schedule"""
        return self.scheduler.remove_task(task_id)

    def get_status(self) -> Dict[str, Any]:
        """Get current monitoring status including scheduler"""
        base_status = {
            "active": True,
            "sources": {
                "total": self.stats["sources_total"],
                "working": [s["name"] for s in self.all_sources],
                "devtools_count": len(self.devtools_sources)
            },
            "stats": self.stats,
            "database_ready": True,
            "prioritizer_ready": True
        }
        
        # Add scheduler status
        scheduler_status = self.get_scheduler_status()
        base_status["scheduler"] = scheduler_status
        
        return base_status
    
    def get_health_dashboard(self) -> Dict[str, Any]:
        """Get comprehensive source health dashboard"""
        return self.health_monitor.get_health_dashboard()
    
    def get_critical_health_alerts(self) -> List[Dict[str, Any]]:
        """Get critical health alerts"""
        return self.health_monitor.get_critical_alerts()
    
    def get_source_health_details(self, source_id: str):
        """Get detailed health metrics for a specific source"""
        return self.health_monitor.get_source_health(source_id)


def main():
    """Main CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Universal Topic Intelligence Monitor")
    parser.add_argument("--mode", choices=["single", "scheduled", "scheduler", "status", "health"], 
                       default="single", help="Monitoring mode")
    parser.add_argument("--interval", type=int, default=60, 
                       help="Interval in minutes for scheduled mode")
    parser.add_argument("--verbose", "-v", action="store_true", 
                       help="Verbose logging")
    parser.add_argument("--schedule-name", type=str, 
                       help="Name for custom schedule")
    parser.add_argument("--scheduler-action", choices=["status", "add", "pause", "resume", "remove"],
                       help="Scheduler management action")
    parser.add_argument("--task-id", type=str, 
                       help="Task ID for scheduler actions")
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create monitor
    monitor = UniversalMonitor()
    
    if args.mode == "status":
        # Show status
        status = monitor.get_status()
        print("Universal Topic Intelligence Monitor Status")
        print("=" * 50)
        print(f"Active: {status['active']}")
        print(f"Total Sources: {status['sources']['total']}")
        print(f"Database Ready: {status['database_ready']}")
        print(f"Prioritizer Ready: {status['prioritizer_ready']}")
        
        if status['stats']['last_run']:
            print(f"Last Run: {status['stats']['last_run']}")
            print(f"Total Items Found: {status['stats']['items_found']}")
            print(f"Total Items Stored: {status['stats']['items_stored']}")
        
        print("\nWorking Sources:")
        for source in status['sources']['working']:
            print(f"  ✅ {source}")
        
        return
    
    if args.mode == "health":
        # Show health dashboard
        dashboard = monitor.get_health_dashboard()
        alerts = monitor.get_critical_health_alerts()
        
        print("🏥 Source Health Dashboard")
        print("=" * 50)
        
        # System health overview
        system = dashboard['system_health']
        print(f"📊 System Overview:")
        print(f"  Total Sources: {system['total_sources']}")
        print(f"  🟢 Healthy: {system['healthy_sources']}")
        print(f"  🟡 Warning: {system['warning_sources']}")  
        print(f"  🟠 Degraded: {system['degraded_sources']}")
        print(f"  🔴 Critical: {system['critical_sources']}")
        print(f"  Average Health Score: {system['avg_health_score']}/100")
        print(f"  Average Success Rate: {system['avg_success_rate']:.1%}")
        
        # Recent activity
        recent = dashboard['recent_activity']
        print(f"\n📈 Recent Activity (24h):")
        print(f"  Health Checks: {recent['total_checks_24h']}")
        print(f"  Successful: {recent['successful_checks_24h']}")
        print(f"  Sources Checked: {recent['sources_checked_24h']}")
        print(f"  Avg Response Time: {recent['avg_response_time_24h']:.0f}ms")
        
        # Critical alerts
        if alerts:
            print(f"\n🚨 Critical Alerts ({len(alerts)}):")
            for alert in alerts:
                priority_icon = "🔴" if alert['priority'] == 'high' else "🟡"
                print(f"  {priority_icon} {alert['message']}")
        
        # Top errors
        if dashboard['top_errors']:
            print(f"\n❌ Top Error Types (7 days):")
            for error in dashboard['top_errors']:
                print(f"  {error['error_type']}: {error['count']} occurrences")
        
        # Source details grouped by status
        sources = dashboard['sources']
        status_groups = {
            'critical': [s for s in sources if s['status'] == 'critical'],
            'degraded': [s for s in sources if s['status'] == 'degraded'], 
            'warning': [s for s in sources if s['status'] == 'warning'],
            'healthy': [s for s in sources if s['status'] == 'healthy']
        }
        
        for status_name, sources_list in status_groups.items():
            if sources_list:
                status_icons = {'critical': '🔴', 'degraded': '🟠', 'warning': '🟡', 'healthy': '🟢'}
                print(f"\n{status_icons[status_name]} {status_name.title()} Sources ({len(sources_list)}):")
                for source in sources_list[:10]:  # Show top 10
                    issues_text = f" - {', '.join(source['issues'][:2])}" if source['issues'] else ""
                    consecutive = f" ({source['consecutive_failures']} fails)" if source['consecutive_failures'] > 0 else ""
                    print(f"  {source['source_name']}: {source['health_score']:.0f}/100, {source['success_rate']:.1%}{consecutive}{issues_text}")
                
                if len(sources_list) > 10:
                    print(f"  ... and {len(sources_list) - 10} more")
        
        return
    
    # Run monitoring
    async def run():
        if args.mode == "single":
            print("Running single monitoring cycle...")
            result = await monitor.run_monitoring_cycle()
            
            print(f"\n📊 Monitoring Results:")
            print(f"  Sources Checked: {result['sources_checked']}")
            print(f"  Success Rate: {result['success_rate']}")
            print(f"  Items Found: {result['items_found_this_cycle']}")
            print(f"  Items Stored: {result['items_stored_this_cycle']}")
            
            print(f"\n📋 Source Results:")
            for source_result in result['source_results']:
                status_icon = "✅" if source_result['success'] else "❌"
                error_msg = f" ({source_result['error']})" if source_result.get('error') else ""
                print(f"  {status_icon} {source_result['source']}: "
                      f"{source_result['items_found']} found, "
                      f"{source_result['items_stored']} stored{error_msg}")
        
        elif args.mode == "scheduled":
            print(f"Starting scheduled monitoring (every {args.interval} minutes)")
            print("Press Ctrl+C to stop")
            await monitor.start_scheduled_monitoring(args.interval)
        
        elif args.mode == "scheduler":
            # Use the built-in scheduler system
            print("Starting automated scheduler system...")
            print("Press Ctrl+C to stop")
            await monitor.start_scheduled_monitoring()
        
        elif args.scheduler_action:
            # Handle scheduler management actions
            if args.scheduler_action == "status":
                status = monitor.get_scheduler_status()
                print("Scheduler Status:")
                print("-" * 40)
                print(f"Running: {status['scheduler_running']}")
                print(f"Total tasks: {status['total_tasks']}")
                print(f"Tasks by status: {status['tasks_by_status']}")
                
                if status.get('next_run'):
                    print(f"Next run: {status['next_run']['name']} in {status['next_run']['minutes_until']} minutes")
                
                if status.get('recent_results'):
                    print("\nRecent Results:")
                    for result in status['recent_results'][-3:]:  # Last 3
                        print(f"  {result['task_id']}: {result['status']} ({result['execution_time']})")
                        
            elif args.scheduler_action == "add":
                if not args.schedule_name:
                    print("Error: --schedule-name required for add action")
                    return
                task_id = monitor.add_monitoring_schedule(args.schedule_name, args.interval)
                print(f"Added schedule: {args.schedule_name} (Task ID: {task_id})")
                
            elif args.scheduler_action == "pause":
                if not args.task_id:
                    print("Error: --task-id required for pause action")
                    return
                success = monitor.pause_schedule(args.task_id)
                print(f"{'Paused' if success else 'Failed to pause'} schedule: {args.task_id}")
                
            elif args.scheduler_action == "resume":
                if not args.task_id:
                    print("Error: --task-id required for resume action")
                    return
                success = monitor.resume_schedule(args.task_id)
                print(f"{'Resumed' if success else 'Failed to resume'} schedule: {args.task_id}")
                
            elif args.scheduler_action == "remove":
                if not args.task_id:
                    print("Error: --task-id required for remove action")
                    return
                success = monitor.remove_schedule(args.task_id)
                print(f"{'Removed' if success else 'Failed to remove'} schedule: {args.task_id}")
            
            return
    
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("\nMonitoring stopped")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()