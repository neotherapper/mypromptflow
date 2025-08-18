#!/usr/bin/env python3
"""
Enhanced Universal Monitor
Integrates hierarchical agents, enhanced sources, and Claude-focused monitoring
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from hierarchical_monitor import HierarchicalUniversalMonitor
from sources.enhanced_sources import ENHANCED_CLAUDE_SOURCES, RELEVANCE_RULES, is_content_relevant
from sources.claude_focused_monitor import ClaudeFocusedMonitor, TOPIC_CONFIGURATIONS
from sources.rss_monitor import RSSSourceMonitor
from core import SourceMetadata, SourceType, ContentItem
from core.language_filter import LanguageFilter
from core.relevance_filter import RelevanceFilter
from storage.database import StorageManager
from core.content_prioritizer import UniversalContentPrioritizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class EnhancedMonitoringConfig:
    """Configuration for enhanced monitoring"""
    enable_hierarchical_agents: bool = True
    enable_enhanced_sources: bool = True
    enable_claude_focused: bool = True
    max_items_per_cycle: int = 500
    quality_threshold: float = 0.7
    update_frequency_minutes: int = 30

class EnhancedUniversalMonitor:
    """
    Unified monitoring system combining:
    - Hierarchical agent coordination
    - Enhanced curated sources
    - Claude-focused monitoring
    - Advanced filtering and quality control
    """
    
    def __init__(self, config: EnhancedMonitoringConfig = None):
        self.config = config or EnhancedMonitoringConfig()
        
        # Core components
        self.storage = StorageManager()
        self.prioritizer = UniversalContentPrioritizer()
        self.language_filter = LanguageFilter(target_languages=['en'], min_confidence=0.7)
        self.relevance_filter = RelevanceFilter()
        
        # Monitoring systems
        self.hierarchical_monitor = None
        self.claude_focused_monitor = None
        
        # Enhanced sources
        self.enhanced_sources = []
        self.enhanced_monitors = {}
        
        # Initialize systems based on configuration
        self._initialize_systems()
        
        # Statistics
        self.stats = {
            "cycles_completed": 0,
            "total_items_processed": 0,
            "total_items_stored": 0,
            "hierarchical_items": 0,
            "enhanced_source_items": 0,
            "claude_focused_items": 0,
            "last_cycle": None
        }
        
    def _initialize_systems(self):
        """Initialize all monitoring systems"""
        
        # Initialize hierarchical agent system
        if self.config.enable_hierarchical_agents:
            self.hierarchical_monitor = HierarchicalUniversalMonitor()
            logger.info("✅ Initialized hierarchical agent monitoring")
        
        # Initialize Claude-focused monitoring
        if self.config.enable_claude_focused:
            self.claude_focused_monitor = ClaudeFocusedMonitor()
            logger.info("✅ Initialized Claude-focused monitoring")
        
        # Initialize enhanced sources
        if self.config.enable_enhanced_sources:
            self._initialize_enhanced_sources()
            logger.info(f"✅ Initialized {len(self.enhanced_sources)} enhanced sources")
        
        logger.info("🚀 Enhanced Universal Monitor initialized successfully")
    
    def _initialize_enhanced_sources(self):
        """Initialize enhanced source monitors"""
        
        self.enhanced_sources = ENHANCED_CLAUDE_SOURCES.copy()
        
        for source in self.enhanced_sources:
            try:
                metadata = SourceMetadata(
                    source_id=source["source_id"],
                    source_name=source["source_name"],
                    source_type=SourceType.RSS,
                    source_url=source["source_url"],
                    authority_score=source["authority_score"],
                    update_frequency="hourly",
                    topics=source["topics"]
                )
                
                monitor = RSSSourceMonitor(metadata, config={
                    "timeout": 15,
                    "max_items": 25,
                    "user_agent": "UniversalTopicIntelligence/1.0"
                })
                
                self.enhanced_monitors[source["source_id"]] = monitor
                
            except Exception as e:
                logger.error(f"Failed to initialize enhanced source {source['source_id']}: {e}")
    
    async def run_comprehensive_cycle(self) -> Dict[str, Any]:
        """Run a comprehensive monitoring cycle using all systems"""
        
        logger.info("🎯 Starting Enhanced Universal Monitoring Cycle")
        cycle_start = datetime.now()
        
        # Initialize cycle results
        cycle_results = {
            "timestamp": cycle_start.isoformat(),
            "hierarchical_results": None,
            "claude_focused_results": None,
            "enhanced_source_results": None,
            "total_items_collected": 0,
            "total_items_stored": 0,
            "system_performance": {}
        }
        
        # 1. Run hierarchical agent monitoring
        if self.hierarchical_monitor:
            try:
                logger.info("🏛️ Running hierarchical agent monitoring...")
                hierarchical_results = await self.hierarchical_monitor.hierarchical_monitoring_cycle()
                cycle_results["hierarchical_results"] = hierarchical_results
                self.stats["hierarchical_items"] += hierarchical_results.get("items_stored", 0)
                logger.info(f"Hierarchical: {hierarchical_results.get('items_stored', 0)} items stored")
            except Exception as e:
                logger.error(f"Hierarchical monitoring failed: {e}")
        
        # 2. Run Claude-focused monitoring
        if self.claude_focused_monitor:
            try:
                logger.info("🤖 Running Claude-focused monitoring...")
                claude_results = await self._run_claude_focused_cycle()
                cycle_results["claude_focused_results"] = claude_results
                self.stats["claude_focused_items"] += claude_results.get("items_stored", 0)
                logger.info(f"Claude-focused: {claude_results.get('items_stored', 0)} items stored")
            except Exception as e:
                logger.error(f"Claude-focused monitoring failed: {e}")
        
        # 3. Run enhanced sources monitoring
        if self.enhanced_monitors:
            try:
                logger.info("⭐ Running enhanced sources monitoring...")
                enhanced_results = await self._run_enhanced_sources_cycle()
                cycle_results["enhanced_source_results"] = enhanced_results
                self.stats["enhanced_source_items"] += enhanced_results.get("items_stored", 0)
                logger.info(f"Enhanced sources: {enhanced_results.get('items_stored', 0)} items stored")
            except Exception as e:
                logger.error(f"Enhanced sources monitoring failed: {e}")
        
        # Calculate totals
        cycle_results["total_items_stored"] = (
            (cycle_results["hierarchical_results"] or {}).get("items_stored", 0) +
            (cycle_results["claude_focused_results"] or {}).get("items_stored", 0) +
            (cycle_results["enhanced_source_results"] or {}).get("items_stored", 0)
        )
        
        cycle_results["total_items_collected"] = (
            (cycle_results["hierarchical_results"] or {}).get("content_collected", 0) +
            (cycle_results["claude_focused_results"] or {}).get("items_collected", 0) +
            (cycle_results["enhanced_source_results"] or {}).get("items_collected", 0)
        )
        
        # Update statistics
        cycle_end = datetime.now()
        cycle_duration = (cycle_end - cycle_start).total_seconds()
        
        self.stats["cycles_completed"] += 1
        self.stats["total_items_processed"] += cycle_results["total_items_collected"]
        self.stats["total_items_stored"] += cycle_results["total_items_stored"]
        self.stats["last_cycle"] = cycle_start
        
        cycle_results["system_performance"] = {
            "cycle_duration_seconds": cycle_duration,
            "items_per_second": cycle_results["total_items_collected"] / max(1, cycle_duration),
            "storage_efficiency": (
                cycle_results["total_items_stored"] / max(1, cycle_results["total_items_collected"]) * 100
            )
        }
        
        # Log comprehensive results
        logger.info("📊 Enhanced Monitoring Cycle Complete!")
        logger.info(f"  Duration: {cycle_duration:.1f}s")
        logger.info(f"  Items Collected: {cycle_results['total_items_collected']}")
        logger.info(f"  Items Stored: {cycle_results['total_items_stored']}")
        logger.info(f"  Storage Efficiency: {cycle_results['system_performance']['storage_efficiency']:.1f}%")
        
        return cycle_results
    
    async def _run_claude_focused_cycle(self) -> Dict[str, Any]:
        """Run Claude-focused monitoring cycle"""
        
        # Monitor high-priority Claude topics
        results = {}
        total_items_stored = 0
        total_items_collected = 0
        
        priority_topics = ["claude_development", "frontend_react", "mcp_servers", "ai_prompting"]
        
        for topic in priority_topics:
            try:
                topic_results = await self.claude_focused_monitor.monitor_by_topic(
                    TOPIC_CONFIGURATIONS[topic]["keywords"][0]  # Use first keyword as topic filter
                )
                
                # Process and store results
                items_stored = await self._process_claude_focused_results(topic_results, topic)
                results[topic] = {
                    "sources_checked": len(topic_results),
                    "items_stored": items_stored
                }
                total_items_stored += items_stored
                total_items_collected += sum(
                    len(result.new_items or []) for result in topic_results.values()
                    if hasattr(result, 'new_items')
                )
                
            except Exception as e:
                logger.error(f"Failed to monitor Claude-focused topic {topic}: {e}")
        
        return {
            "topics_monitored": list(results.keys()),
            "topic_results": results,
            "items_stored": total_items_stored,
            "items_collected": total_items_collected
        }
    
    async def _run_enhanced_sources_cycle(self) -> Dict[str, Any]:
        """Run enhanced sources monitoring cycle"""
        
        # Monitor enhanced sources with advanced relevance filtering
        tasks = []
        for source_id, monitor in self.enhanced_monitors.items():
            task = self._monitor_enhanced_source(source_id, monitor)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        successful_results = [r for r in results if not isinstance(r, Exception)]
        failed_count = len([r for r in results if isinstance(r, Exception)])
        
        total_items_stored = sum(r.get("items_stored", 0) for r in successful_results)
        total_items_collected = sum(r.get("items_found", 0) for r in successful_results)
        
        return {
            "sources_monitored": len(self.enhanced_monitors),
            "sources_successful": len(successful_results),
            "sources_failed": failed_count,
            "items_collected": total_items_collected,
            "items_stored": total_items_stored,
            "source_results": successful_results
        }
    
    async def _monitor_enhanced_source(self, source_id: str, monitor: RSSSourceMonitor) -> Dict[str, Any]:
        """Monitor a single enhanced source"""
        
        try:
            result = await monitor.monitor()
            
            if not result.success or not result.new_items:
                return {
                    "source_id": source_id,
                    "source_name": monitor.metadata.source_name,
                    "success": result.success,
                    "items_found": 0,
                    "items_stored": 0,
                    "error": result.errors[0] if result.errors else None
                }
            
            # Apply enhanced relevance filtering
            items_stored = 0
            items_filtered = 0
            
            for item in result.new_items:
                try:
                    # Apply enhanced relevance rules
                    is_relevant, relevance_score = is_content_relevant(
                        item.title, 
                        item.content or ""
                    )
                    
                    if not is_relevant:
                        items_filtered += 1
                        continue
                    
                    # Apply language filter
                    should_include, lang_result = self.language_filter.should_include_content(
                        item.title, 
                        item.content or ""
                    )
                    
                    if not should_include:
                        items_filtered += 1
                        continue
                    
                    # Apply relevance filter
                    is_relevant_rf, rf_score, rf_reason = self.relevance_filter.is_relevant(
                        item.title,
                        item.content or "",
                        item.topics
                    )
                    
                    if not is_relevant_rf:
                        items_filtered += 1
                        continue
                    
                    # Calculate combined priority
                    priority_result = self.prioritizer.prioritize(item)
                    
                    # Boost priority based on enhanced relevance
                    boosted_score = priority_result.total_score * (1 + relevance_score * 0.5)
                    
                    # Store if above quality threshold
                    if boosted_score >= self.config.quality_threshold:
                        stored = await self.storage.store_content(
                            item=item,
                            priority_score=boosted_score,
                            priority_level=priority_result.priority_level.value
                        )
                        
                        if stored:
                            items_stored += 1
                    else:
                        items_filtered += 1
                        
                except Exception as e:
                    logger.error(f"Error processing enhanced item from {source_id}: {e}")
            
            return {
                "source_id": source_id,
                "source_name": monitor.metadata.source_name,
                "success": True,
                "items_found": len(result.new_items),
                "items_filtered": items_filtered,
                "items_stored": items_stored,
                "error": None
            }
            
        except Exception as e:
            logger.error(f"Enhanced source monitoring failed for {source_id}: {e}")
            return {
                "source_id": source_id,
                "source_name": getattr(monitor, 'metadata', {}).get('source_name', 'Unknown'),
                "success": False,
                "items_found": 0,
                "items_stored": 0,
                "error": str(e)
            }
    
    async def _process_claude_focused_results(self, topic_results: Dict, topic: str) -> int:
        """Process and store Claude-focused monitoring results"""
        
        items_stored = 0
        
        for source_id, result in topic_results.items():
            if not hasattr(result, 'new_items') or not result.new_items:
                continue
            
            for item in result.new_items:
                try:
                    # Apply quality threshold specific to topic
                    topic_config = TOPIC_CONFIGURATIONS.get(topic, {})
                    quality_threshold = topic_config.get("quality_threshold", self.config.quality_threshold)
                    
                    # Calculate priority
                    priority_result = self.prioritizer.prioritize(item)
                    
                    # Store if meets topic-specific quality threshold
                    if priority_result.total_score >= quality_threshold:
                        stored = await self.storage.store_content(
                            item=item,
                            priority_score=priority_result.total_score,
                            priority_level=priority_result.priority_level.value
                        )
                        
                        if stored:
                            items_stored += 1
                            
                except Exception as e:
                    logger.error(f"Error processing Claude-focused item: {e}")
        
        return items_stored
    
    def get_comprehensive_status(self) -> Dict[str, Any]:
        """Get comprehensive status of all monitoring systems"""
        
        return {
            "config": {
                "hierarchical_agents": self.config.enable_hierarchical_agents,
                "enhanced_sources": self.config.enable_enhanced_sources,
                "claude_focused": self.config.enable_claude_focused,
                "quality_threshold": self.config.quality_threshold
            },
            "systems": {
                "hierarchical_monitor": self.hierarchical_monitor is not None,
                "claude_focused_monitor": self.claude_focused_monitor is not None,
                "enhanced_sources_count": len(self.enhanced_monitors)
            },
            "statistics": self.stats.copy(),
            "performance": {
                "avg_items_per_cycle": (
                    self.stats["total_items_processed"] / max(1, self.stats["cycles_completed"])
                ),
                "storage_efficiency": (
                    self.stats["total_items_stored"] / max(1, self.stats["total_items_processed"]) * 100
                )
            }
        }

async def main():
    """Demonstrate enhanced universal monitoring"""
    
    print("\n" + "="*80)
    print("🚀 ENHANCED UNIVERSAL TOPIC INTELLIGENCE SYSTEM")
    print("   Hierarchical Agents + Enhanced Sources + Claude-Focused Monitoring")
    print("="*80 + "\n")
    
    # Initialize enhanced monitor
    config = EnhancedMonitoringConfig(
        enable_hierarchical_agents=True,
        enable_enhanced_sources=True,
        enable_claude_focused=True,
        quality_threshold=0.6,  # Lower threshold for demo
        max_items_per_cycle=200
    )
    
    monitor = EnhancedUniversalMonitor(config)
    
    # Show system status
    status = monitor.get_comprehensive_status()
    print("📊 System Status:")
    print(f"  Hierarchical Agents: {'✅' if status['systems']['hierarchical_monitor'] else '❌'}")
    print(f"  Enhanced Sources: {'✅' if status['systems']['enhanced_sources_count'] > 0 else '❌'} ({status['systems']['enhanced_sources_count']} sources)")
    print(f"  Claude-Focused: {'✅' if status['systems']['claude_focused_monitor'] else '❌'}")
    print(f"  Quality Threshold: {status['config']['quality_threshold']}")
    
    print("\n🎯 Running Comprehensive Monitoring Cycle...")
    
    # Run comprehensive cycle
    results = await monitor.run_comprehensive_cycle()
    
    # Display results
    print("\n📊 COMPREHENSIVE MONITORING RESULTS:")
    print("-" * 60)
    print(f"  ⏱️  Cycle Duration: {results['system_performance']['cycle_duration_seconds']:.1f}s")
    print(f"  📄 Items Collected: {results['total_items_collected']}")
    print(f"  💾 Items Stored: {results['total_items_stored']}")
    print(f"  📈 Storage Efficiency: {results['system_performance']['storage_efficiency']:.1f}%")
    print(f"  🚀 Processing Speed: {results['system_performance']['items_per_second']:.1f} items/sec")
    
    if results["hierarchical_results"]:
        hr = results["hierarchical_results"]
        print(f"\n🏛️ Hierarchical Agents:")
        print(f"     Topics: {hr.get('queen_orchestration', {}).get('topics_active', 0)}")
        print(f"     Tasks: {hr.get('monitoring_tasks', 0)}")
        print(f"     Success Rate: {hr.get('worker_execution', {}).get('success_rate', 0):.1%}")
        print(f"     Items Stored: {hr.get('items_stored', 0)}")
    
    if results["claude_focused_results"]:
        cf = results["claude_focused_results"]
        print(f"\n🤖 Claude-Focused:")
        print(f"     Topics Monitored: {len(cf.get('topics_monitored', []))}")
        print(f"     Items Stored: {cf.get('items_stored', 0)}")
    
    if results["enhanced_source_results"]:
        es = results["enhanced_source_results"]
        print(f"\n⭐ Enhanced Sources:")
        print(f"     Sources Monitored: {es.get('sources_monitored', 0)}")
        print(f"     Success Rate: {es.get('sources_successful', 0)}/{es.get('sources_monitored', 0)}")
        print(f"     Items Stored: {es.get('items_stored', 0)}")
    
    print(f"\n✨ Enhanced Universal Monitoring Complete!")
    print(f"   All systems operational with {results['total_items_stored']} high-quality items stored")

if __name__ == "__main__":
    asyncio.run(main())