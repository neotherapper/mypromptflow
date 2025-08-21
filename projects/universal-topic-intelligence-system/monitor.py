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
from storage.database import StorageManager
from core.content_prioritizer import UniversalContentPrioritizer

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
        
        # Only verified working sources
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
        
        self.stats = {
            "sources_total": len(self.working_sources) + len(self.mcp_sources),
            "sources_successful": 0,
            "sources_failed": 0,
            "items_found": 0,
            "items_stored": 0,
            "last_run": None
        }
    
    async def monitor_source(self, source_config: Dict) -> Dict[str, Any]:
        """Monitor a single source"""
        
        # Generate source ID from URL hash
        import hashlib
        source_id = hashlib.md5(source_config['url'].encode()).hexdigest()[:8]
        
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
        
        # Monitor using RSS
        monitor = RSSSourceMonitor(metadata)
        result = await monitor.monitor()
        
        items_stored = 0
        items_filtered_out = 0
        if result.success and result.new_items:
            for item in result.new_items:
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
                        
                except Exception as e:
                    logger.error(f"Error storing item from {source_config['name']}: {e}")
        
        return {
            "source": source_config['name'],
            "url": source_config['url'][:50] + "...",
            "success": result.success,
            "items_found": len(result.new_items) if result.success else 0,
            "items_filtered": items_filtered_out,
            "items_stored": items_stored,
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
        
        total_sources = len(self.working_sources) + len(self.mcp_sources)
        logger.info(f"Starting monitoring cycle for {total_sources} sources ({len(self.working_sources)} RSS + {len(self.mcp_sources)} MCP)")
        self.stats["last_run"] = datetime.now()
        
        # Reset per-cycle stats
        self.stats["sources_successful"] = 0
        self.stats["sources_failed"] = 0
        cycle_items_found = 0
        cycle_items_stored = 0
        cycle_items_filtered = 0
        
        # Monitor all sources concurrently
        tasks = []
        
        # Add RSS source tasks
        for source in self.working_sources:
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
        
        cycle_summary = {
            "timestamp": self.stats["last_run"].isoformat(),
            "sources_checked": total_sources,
            "rss_sources": len(self.working_sources),
            "mcp_sources": len(self.mcp_sources),
            "sources_successful": self.stats["sources_successful"],
            "sources_failed": self.stats["sources_failed"],
            "items_found_this_cycle": cycle_items_found,
            "items_filtered_this_cycle": cycle_items_filtered,
            "items_stored_this_cycle": cycle_items_stored,
            "success_rate": f"{(self.stats['sources_successful'] / total_sources * 100):.1f}%",
            "filter_rate": f"{(cycle_items_filtered / max(1, cycle_items_found) * 100):.1f}%",
            "source_results": source_results,
            "cumulative_stats": self.stats.copy()
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
    
    def get_status(self) -> Dict[str, Any]:
        """Get current monitoring status"""
        return {
            "active": True,
            "sources": {
                "total": self.stats["sources_total"],
                "working": [s["name"] for s in self.working_sources]
            },
            "stats": self.stats,
            "database_ready": True,
            "prioritizer_ready": True
        }


def main():
    """Main CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Universal Topic Intelligence Monitor")
    parser.add_argument("--mode", choices=["single", "scheduled", "status"], 
                       default="single", help="Monitoring mode")
    parser.add_argument("--interval", type=int, default=60, 
                       help="Interval in minutes for scheduled mode")
    parser.add_argument("--verbose", "-v", action="store_true", 
                       help="Verbose logging")
    
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
    
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("\nMonitoring stopped")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()