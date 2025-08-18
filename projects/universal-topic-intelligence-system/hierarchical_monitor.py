#!/usr/bin/env python3
"""
Hierarchical Universal Monitor
Integrates the 4-Level Agent Hierarchy with the actual monitoring system
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional

from agents import (
    QueenAgent,
    ArchitectCoordinator,
    SpecialistCoordinator,
    WorkerPool,
    WorkerTask
)
from core import SourceMetadata, SourceType, ContentItem
from core.language_filter import LanguageFilter
from core.relevance_filter import RelevanceFilter
from storage.database import StorageManager
from core.content_prioritizer import UniversalContentPrioritizer
from sources.rss_monitor import RSSSourceMonitor
from sources.real_mcp_monitor import RealMCPMonitor, MCP_TEST_CONFIG

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class HierarchicalUniversalMonitor:
    """
    Universal monitor that uses the 4-level agent hierarchy
    Combines RSS/MCP monitoring with intelligent agent coordination
    """
    
    def __init__(self):
        # Core components
        self.storage = StorageManager()
        self.prioritizer = UniversalContentPrioritizer()
        self.language_filter = LanguageFilter(target_languages=['en'], min_confidence=0.7)
        self.relevance_filter = RelevanceFilter()
        
        # Agent hierarchy components
        self.queen = QueenAgent()
        self.architect_coordinators = {}  # topic_id -> ArchitectCoordinator
        self.specialist_coordinator = SpecialistCoordinator()
        self.worker_pool = WorkerPool()
        
        # Topic configurations
        self.topics = {
            "react_ecosystem": {
                "name": "React Ecosystem",
                "sources": [
                    {"url": "https://react.dev/rss.xml", "name": "React Blog", "authority_score": 1.0},
                    {"url": "https://overreacted.io/rss.xml", "name": "Dan Abramov Blog", "authority_score": 1.0},
                    {"url": "https://kentcdodds.com/blog/rss.xml", "name": "Kent C Dodds", "authority_score": 0.9},
                ],
                "mcp_sources": [MCP_TEST_CONFIG["youtube_react_videos"], MCP_TEST_CONFIG["github_react_repos"]]
            },
            "claude_ai": {
                "name": "Claude AI", 
                "sources": [
                    {"url": "https://www.reddit.com/r/ClaudeAI.rss", "name": "Reddit ClaudeAI", "authority_score": 0.7},
                ],
                "mcp_sources": [MCP_TEST_CONFIG["search_claude_news"]]
            },
            "crypto_tech": {
                "name": "Crypto Technology",
                "sources": [
                    {"url": "https://cointelegraph.com/rss", "name": "CoinTelegraph", "authority_score": 0.6},
                    {"url": "https://decrypt.co/feed", "name": "Decrypt", "authority_score": 0.65},
                ],
                "mcp_sources": []
            }
        }
        
        # Initialize agent hierarchy
        self._initialize_hierarchy()
        
    def _initialize_hierarchy(self):
        """Initialize the agent hierarchy for all topics"""
        
        # Register topics with Queen
        for topic_id, topic_config in self.topics.items():
            self.queen.register_topic(topic_id, topic_config["name"])
            
            # Create architect coordinator for each topic
            self.architect_coordinators[topic_id] = ArchitectCoordinator(topic_id, topic_config["name"])
            
        logger.info(f"🏗️ Initialized hierarchy for {len(self.topics)} topics")
        
    async def hierarchical_monitoring_cycle(self) -> Dict[str, Any]:
        """Run a complete monitoring cycle using the agent hierarchy"""
        
        logger.info("👑 Starting Hierarchical Monitoring Cycle")
        
        # LEVEL 1: Queen orchestration
        queen_results = await self.queen.orchestrate()
        logger.info(f"Queen orchestrated {queen_results['topics_active']} topics")
        
        # LEVEL 2: Architect coordination based on Queen's decisions
        monitoring_tasks = []
        for deployment in queen_results['deployments']:
            topic_id = deployment['topic_id']
            architects_to_deploy = deployment['architects_deployed']
            
            if topic_id in self.architect_coordinators:
                # Get architect coordination
                coordinator = self.architect_coordinators[topic_id]
                architect_result = await coordinator.coordinate_all(architects_to_deploy)
                
                # Convert architect strategies into monitoring tasks
                tasks = self._create_monitoring_tasks(topic_id, architect_result)
                monitoring_tasks.extend(tasks)
        
        logger.info(f"🏛️ Created {len(monitoring_tasks)} monitoring tasks from architects")
        
        # LEVEL 4: Execute monitoring tasks via worker pool
        worker_results = await self.worker_pool.execute_tasks(monitoring_tasks)
        logger.info(f"⚙️ Workers executed {worker_results['successful']} tasks successfully")
        
        # Convert worker results to content items
        collected_content = await self._process_worker_results(worker_results['results'])
        
        # LEVEL 3: Process content through specialists
        if collected_content:
            specialist_results = await self.specialist_coordinator.process_content(
                collected_content,
                ["technical", "market", "sentiment", "quality"]
            )
            logger.info(f"🔬 Specialists analyzed {specialist_results['summary']['total_analyses']} items")
        
        # Apply filtering and storage
        items_stored = await self._filter_and_store_content(collected_content)
        
        # Update Queen with results
        for topic_id in self.topics:
            self.queen.update_topic_status(topic_id, items_stored)
        
        return {
            "queen_orchestration": queen_results,
            "monitoring_tasks": len(monitoring_tasks),
            "worker_execution": worker_results,
            "content_collected": len(collected_content),
            "specialist_analysis": specialist_results if collected_content else None,
            "items_stored": items_stored,
            "timestamp": datetime.now().isoformat()
        }
    
    def _create_monitoring_tasks(self, topic_id: str, architect_result: Dict) -> List[WorkerTask]:
        """Convert architect coordination results into worker tasks"""
        tasks = []
        
        topic_config = self.topics.get(topic_id, {})
        
        # Create RSS monitoring tasks
        for source in topic_config.get("sources", []):
            task = WorkerTask(
                task_id=f"rss_{topic_id}_{hash(source['url'])}",
                task_type="rss_fetch",
                source_url=source["url"],
                parameters={
                    "topic": topic_id,
                    "source_name": source["name"],
                    "authority_score": source.get("authority_score", 0.5)
                },
                priority="high" if source.get("authority_score", 0) > 0.8 else "medium"
            )
            tasks.append(task)
        
        # Create MCP monitoring tasks  
        for mcp_source in topic_config.get("mcp_sources", []):
            if "video_urls" in mcp_source:
                # YouTube tasks
                for video_url in mcp_source["video_urls"]:
                    task = WorkerTask(
                        task_id=f"youtube_{topic_id}_{hash(video_url)}",
                        task_type="youtube",
                        source_url=video_url,
                        parameters={"topic": topic_id},
                        priority="medium"
                    )
                    tasks.append(task)
            
            elif "repo_queries" in mcp_source:
                # GitHub tasks
                for repo_query in mcp_source["repo_queries"]:
                    task = WorkerTask(
                        task_id=f"github_{topic_id}_{hash(repo_query)}",
                        task_type="github",
                        source_url=f"https://github.com/{repo_query}",
                        parameters={"topic": topic_id, "repo": repo_query},
                        priority="medium"
                    )
                    tasks.append(task)
            
            elif "search_queries" in mcp_source:
                # Search tasks
                for search_query in mcp_source["search_queries"]:
                    task = WorkerTask(
                        task_id=f"search_{topic_id}_{hash(search_query)}",
                        task_type="search",
                        source_url="https://search.example.com",
                        parameters={"topic": topic_id, "query": search_query},
                        priority="low"
                    )
                    tasks.append(task)
        
        logger.info(f"Created {len(tasks)} tasks for topic '{topic_id}'")
        return tasks
        
    async def _process_worker_results(self, worker_results: List) -> List[Dict]:
        """Convert worker results to content items for specialist processing"""
        content_items = []
        
        for result in worker_results:
            if result.success and result.data:
                # Convert worker result to content dict format
                content_item = {
                    "item_id": result.task_id,
                    "title": result.data.get("title", f"Content from {result.worker_type}"),
                    "content": result.data.get("content", result.data.get("description", "")),
                    "url": result.data.get("url", ""),
                    "published_date": datetime.now().isoformat(),
                    "author": result.data.get("author", "Unknown"),
                    "topics": result.data.get("topics", []),
                    "metadata": {
                        "worker_type": result.worker_type,
                        "execution_time": result.execution_time,
                        **result.data
                    }
                }
                content_items.append(content_item)
        
        logger.info(f"Processed {len(content_items)} content items from worker results")
        return content_items
        
    async def _filter_and_store_content(self, content_items: List[Dict]) -> int:
        """Apply filtering and store content items"""
        items_stored = 0
        items_filtered = 0
        
        for item_dict in content_items:
            try:
                # Create ContentItem
                item = ContentItem(
                    item_id=item_dict["item_id"],
                    source_id="hierarchical_monitor",
                    title=item_dict["title"],
                    content=item_dict["content"],
                    url=item_dict["url"],
                    published_date=datetime.fromisoformat(item_dict["published_date"].replace('Z', '+00:00')) if 'Z' in item_dict["published_date"] else datetime.now(),
                    author=item_dict["author"],
                    topics=item_dict["topics"],
                    metadata=item_dict["metadata"]
                )
                
                # Apply language filtering
                should_include, lang_result = self.language_filter.should_include_content(
                    item.title, item.content or ""
                )
                if not should_include:
                    items_filtered += 1
                    continue
                
                # Apply relevance filtering  
                is_relevant, relevance_score, reason = self.relevance_filter.is_relevant(
                    item.title, item.content or "", item.topics
                )
                if not is_relevant:
                    items_filtered += 1
                    continue
                
                # Calculate priority
                priority_result = self.prioritizer.prioritize(item)
                
                # Store item
                stored = await self.storage.store_content(
                    item=item,
                    priority_score=priority_result.total_score,
                    priority_level=priority_result.priority_level.value
                )
                
                if stored:
                    items_stored += 1
                    logger.debug(f"Stored hierarchical item: {item.title[:50]}...")
                
            except Exception as e:
                logger.error(f"Error processing hierarchical item: {e}")
        
        logger.info(f"Hierarchical filtering: {len(content_items)} → {items_filtered} filtered → {items_stored} stored")
        return items_stored
        
    async def traditional_monitoring_cycle(self) -> Dict[str, Any]:
        """Run traditional monitoring (for comparison/fallback)"""
        
        logger.info("📡 Running Traditional Monitoring Cycle")
        
        # Traditional RSS monitoring
        tasks = []
        for topic_id, topic_config in self.topics.items():
            for source in topic_config.get("sources", []):
                # Create metadata
                metadata = SourceMetadata(
                    source_id=f"trad_{hash(source['url'])}",
                    source_name=source["name"],
                    source_type=SourceType.RSS,
                    source_url=source["url"],
                    authority_score=source.get("authority_score", 0.5),
                    update_frequency="daily",
                    topics=[topic_id]
                )
                
                # Create monitor task
                monitor = RSSSourceMonitor(metadata)
                tasks.append(monitor.monitor())
        
        # Execute traditional monitoring
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        total_items = 0
        for result in results:
            if hasattr(result, 'new_items'):
                total_items += len(result.new_items or [])
        
        return {
            "sources_monitored": len(tasks),
            "items_collected": total_items,
            "timestamp": datetime.now().isoformat()
        }

async def main():
    """Run hierarchical monitoring demonstration"""
    
    print("\n" + "="*70)
    print("🎯 HIERARCHICAL UNIVERSAL TOPIC INTELLIGENCE SYSTEM")
    print("   Integrating 4-Level Agent Hierarchy with Real Monitoring")
    print("="*70 + "\n")
    
    monitor = HierarchicalUniversalMonitor()
    
    # Run hierarchical monitoring
    hierarchical_results = await monitor.hierarchical_monitoring_cycle()
    
    print("📊 HIERARCHICAL MONITORING RESULTS:")
    print("-" * 50)
    print(f"  🎯 Topics Orchestrated: {hierarchical_results['queen_orchestration']['topics_active']}")
    print(f"  📋 Monitoring Tasks: {hierarchical_results['monitoring_tasks']}")
    print(f"  ⚙️ Worker Success Rate: {hierarchical_results['worker_execution']['success_rate']:.1%}")
    print(f"  📄 Content Collected: {hierarchical_results['content_collected']}")
    print(f"  💾 Items Stored: {hierarchical_results['items_stored']}")
    
    if hierarchical_results['specialist_analysis']:
        specialist = hierarchical_results['specialist_analysis']
        print(f"  🔬 Specialist Analyses: {specialist['summary']['total_analyses']}")
        print(f"  ⭐ High Quality Items: {specialist['summary']['high_quality_count']}")
    
    print(f"\n✨ Hierarchical monitoring complete!")
    print(f"   Integration successful: Agent Hierarchy + Real Monitoring")
    
    # Compare with traditional monitoring
    print(f"\n📡 Running Traditional Monitoring for Comparison...")
    traditional_results = await monitor.traditional_monitoring_cycle()
    
    print(f"  Traditional Sources: {traditional_results['sources_monitored']}")
    print(f"  Traditional Items: {traditional_results['items_collected']}")
    
    print(f"\n🚀 Integration Complete: Agent Hierarchy is now connected to real monitoring!")

if __name__ == "__main__":
    asyncio.run(main())