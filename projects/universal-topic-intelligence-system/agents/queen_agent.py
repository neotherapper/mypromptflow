#!/usr/bin/env python3
"""
Queen Agent - Level 1 Universal Topic Orchestrator
Manages all monitored topics with resource allocation and cross-topic intelligence
"""

import asyncio
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import logging
import yaml
from pathlib import Path
import heapq

from core import (
    ContentItem,
    ContentPriority,
    UniversalContentPrioritizer,
    SourceMonitorFactory,
    SourceMetadata,
    SourceType
)
from storage import StorageManager


class ResourceAllocationStrategy(Enum):
    """Resource allocation strategies"""
    PRIORITY_BASED = "priority_based"      # Allocate based on topic priority
    ACTIVITY_BASED = "activity_based"      # Allocate based on recent activity
    BALANCED = "balanced"                  # Equal distribution
    ADAPTIVE = "adaptive"                  # Learn from patterns


class CrossTopicRelationship(Enum):
    """Types of relationships between topics"""
    COMPETITIVE = "competitive"      # Topics compete for same audience
    COMPLEMENTARY = "complementary"  # Topics enhance each other
    DEPENDENT = "dependent"          # One topic depends on another
    CONVERGENT = "convergent"        # Topics merging over time
    INFLUENTIAL = "influential"      # One topic influences another
    APPLICATION = "application"      # One topic applies to another
    TOOL = "tool"                   # One topic uses another as a tool
    BUSINESS = "business"           # Business relationship


@dataclass
class TopicState:
    """State tracking for a monitored topic"""
    topic_slug: str
    topic_name: str
    priority_level: str
    last_monitored: Optional[datetime] = None
    items_collected: int = 0
    critical_items: int = 0
    monitoring_frequency: str = "hourly"
    active_sources: Set[str] = field(default_factory=set)
    error_count: int = 0
    resource_allocation: float = 1.0  # Resource weight
    
    def needs_monitoring(self) -> bool:
        """Check if topic needs monitoring based on frequency"""
        if not self.last_monitored:
            return True
            
        now = datetime.now()
        
        if self.monitoring_frequency == "continuous":
            return (now - self.last_monitored).seconds > 300  # 5 minutes
        elif self.monitoring_frequency == "hourly":
            return (now - self.last_monitored).seconds > 3600
        elif self.monitoring_frequency == "daily":
            return (now - self.last_monitored).days >= 1
        elif self.monitoring_frequency == "weekly":
            return (now - self.last_monitored).days >= 7
            
        return True


@dataclass
class TopicOrchestrationResult:
    """Result of topic orchestration"""
    topics_monitored: List[str]
    total_items_collected: int
    critical_items: List[ContentItem]
    cross_topic_insights: List[Dict[str, Any]]
    resource_usage: Dict[str, float]
    performance_metrics: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)


class QueenAgent:
    """
    Queen Agent - Universal topic orchestrator
    Manages resource allocation, cross-topic intelligence, and emergency response
    """
    
    def __init__(self, config_dir: str = "configs/topics", db_path: str = "topic_intelligence.db"):
        """
        Initialize Queen Agent
        
        Args:
            config_dir: Directory containing topic configurations
            db_path: Path to database file for persistence
        """
        self.config_dir = Path(config_dir)
        self.logger = logging.getLogger("QueenAgent")
        
        # Topic management
        self.topics: Dict[str, TopicState] = {}
        self.topic_configs: Dict[str, Dict] = {}
        self.topic_relationships: Dict[Tuple[str, str], CrossTopicRelationship] = {}
        
        # Resource management
        self.resource_pool = 100.0  # Total resource units
        self.allocation_strategy = ResourceAllocationStrategy.ADAPTIVE
        
        # Cross-topic intelligence
        self.shared_sources: Dict[str, Set[str]] = {}  # source_id -> topic_slugs
        self.topic_patterns: Dict[str, List[Dict]] = {}  # Learned patterns
        
        # Prioritizer for cross-topic analysis
        self.prioritizer = UniversalContentPrioritizer()
        
        # Storage manager for persistence
        self.storage = StorageManager(db_path)
        
        # Performance tracking
        self.orchestration_count = 0
        self.total_items_processed = 0
        
        # Load configurations
        self._load_topic_configurations()
        self._initialize_relationships()
    
    def _load_topic_configurations(self):
        """Load all topic configurations from config directory"""
        if not self.config_dir.exists():
            self.logger.warning(f"Config directory {self.config_dir} not found")
            return
            
        for config_file in self.config_dir.glob("*.yaml"):
            try:
                with open(config_file, 'r') as f:
                    config = yaml.safe_load(f)
                    
                topic_slug = config['topic_metadata']['slug']
                self.topic_configs[topic_slug] = config
                
                # Create topic state
                self.topics[topic_slug] = TopicState(
                    topic_slug=topic_slug,
                    topic_name=config['topic_metadata']['name'],
                    priority_level=config['topic_metadata']['priority_level'],
                    monitoring_frequency=config['topic_metadata']['monitoring_frequency']
                )
                
                self.logger.info(f"Loaded configuration for topic: {topic_slug}")
                
                # Track shared sources
                self._track_shared_sources(topic_slug, config)
                
            except Exception as e:
                self.logger.error(f"Failed to load config {config_file}: {str(e)}")
    
    def _track_shared_sources(self, topic_slug: str, config: Dict):
        """Track sources shared across topics"""
        for tier in ['tier_1_official', 'tier_2_community', 'tier_3_aggregators']:
            if tier in config.get('source_mapping', {}):
                for source in config['source_mapping'][tier].get('sources', []):
                    source_id = source.get('url', source.get('name', ''))
                    if source_id not in self.shared_sources:
                        self.shared_sources[source_id] = set()
                    self.shared_sources[source_id].add(topic_slug)
    
    def _initialize_relationships(self):
        """Initialize cross-topic relationships from configurations"""
        for topic_slug, config in self.topic_configs.items():
            cross_topic = config.get('cross_topic_integration', {})
            
            for related in cross_topic.get('related_topics', []):
                related_slug = related['topic_slug']
                relationship = CrossTopicRelationship(related['relationship'])
                
                # Store bidirectional relationship
                self.topic_relationships[(topic_slug, related_slug)] = relationship
                
                # Infer reverse relationship
                if relationship == CrossTopicRelationship.COMPLEMENTARY:
                    self.topic_relationships[(related_slug, topic_slug)] = relationship
                elif relationship == CrossTopicRelationship.COMPETITIVE:
                    self.topic_relationships[(related_slug, topic_slug)] = relationship
    
    async def orchestrate(self, 
                          force_topics: Optional[List[str]] = None,
                          emergency_mode: bool = False) -> TopicOrchestrationResult:
        """
        Main orchestration method - coordinate monitoring across all topics
        
        Args:
            force_topics: Specific topics to monitor (overrides scheduling)
            emergency_mode: Process critical updates immediately
            
        Returns:
            Orchestration result with cross-topic insights
        """
        self.orchestration_count += 1
        self.logger.info(f"Starting orchestration #{self.orchestration_count}")
        
        start_time = datetime.now()
        
        # Determine which topics to monitor
        topics_to_monitor = self._select_topics_for_monitoring(force_topics, emergency_mode)
        
        # Allocate resources
        resource_allocation = self._allocate_resources(topics_to_monitor)
        
        # Monitor topics concurrently with resource limits
        monitoring_tasks = []
        for topic_slug in topics_to_monitor:
            resources = resource_allocation.get(topic_slug, 1.0)
            task = self._monitor_topic_with_resources(topic_slug, resources)
            monitoring_tasks.append(task)
        
        # Execute monitoring
        results = await asyncio.gather(*monitoring_tasks, return_exceptions=True)
        
        # Process results
        all_items = []
        critical_items = []
        topics_monitored = []
        
        for topic_slug, result in zip(topics_to_monitor, results):
            if isinstance(result, Exception):
                self.logger.error(f"Error monitoring {topic_slug}: {str(result)}")
                self.topics[topic_slug].error_count += 1
            else:
                topics_monitored.append(topic_slug)
                all_items.extend(result.get('items', []))
                critical_items.extend(result.get('critical', []))
                
                # Update topic state
                state = self.topics[topic_slug]
                state.last_monitored = datetime.now()
                state.items_collected += len(result.get('items', []))
                state.critical_items += len(result.get('critical', []))
        
        # Save collected items to database
        if all_items:
            items_to_save = []
            for item in all_items:
                # Prioritize each item
                priority_result = self.prioritizer.prioritize(item)
                items_to_save.append((
                    item,
                    priority_result.total_score,
                    priority_result.priority_level.value
                ))
            
            # Batch save to database
            saved_count = self.storage.save_content_items_batch(items_to_save)
            self.logger.info(f"Saved {saved_count} new items to database")
            
            # Update topic statistics in database
            for topic_slug in topics_monitored:
                state = self.topics[topic_slug]
                topic_items = [i for i in all_items if topic_slug in i.topics]
                topic_critical = [i for i in critical_items if topic_slug in i.topics]
                self.storage.update_topic_stats(
                    topic_slug,
                    items_collected=len(topic_items),
                    critical_items=len(topic_critical)
                )
        
        # Perform cross-topic analysis
        cross_topic_insights = self._analyze_cross_topic_patterns(all_items)
        
        # Detect emerging relationships
        new_relationships = self._detect_emerging_relationships(all_items)
        if new_relationships:
            cross_topic_insights.append({
                "type": "emerging_relationships",
                "relationships": new_relationships
            })
        
        # Learn from this orchestration
        self._update_learning(topics_monitored, all_items, critical_items)
        
        # Calculate performance metrics
        duration = (datetime.now() - start_time).total_seconds()
        performance_metrics = {
            "orchestration_duration": duration,
            "topics_monitored": len(topics_monitored),
            "items_per_second": len(all_items) / duration if duration > 0 else 0,
            "resource_efficiency": self._calculate_resource_efficiency(resource_allocation),
            "shared_source_optimization": len([s for s in self.shared_sources if len(self.shared_sources[s]) > 1])
        }
        
        self.total_items_processed += len(all_items)
        
        return TopicOrchestrationResult(
            topics_monitored=topics_monitored,
            total_items_collected=len(all_items),
            critical_items=critical_items[:10],  # Top 10 critical
            cross_topic_insights=cross_topic_insights,
            resource_usage=resource_allocation,
            performance_metrics=performance_metrics
        )
    
    def _select_topics_for_monitoring(self, 
                                      force_topics: Optional[List[str]],
                                      emergency_mode: bool) -> List[str]:
        """Select which topics need monitoring"""
        if force_topics:
            return [t for t in force_topics if t in self.topics]
        
        topics_to_monitor = []
        
        for topic_slug, state in self.topics.items():
            if emergency_mode and state.priority_level != "high":
                continue  # Only high priority in emergency
                
            if state.needs_monitoring():
                topics_to_monitor.append(topic_slug)
        
        # Sort by priority and last monitored time
        priority_order = {"high": 0, "medium": 1, "low": 2}
        topics_to_monitor.sort(
            key=lambda t: (
                priority_order.get(self.topics[t].priority_level, 3),
                self.topics[t].last_monitored or datetime.min
            )
        )
        
        return topics_to_monitor
    
    def _allocate_resources(self, topics: List[str]) -> Dict[str, float]:
        """
        Allocate resources to topics based on strategy
        
        Returns:
            Dictionary of topic_slug -> resource_units
        """
        if not topics:
            return {}
        
        allocation = {}
        
        if self.allocation_strategy == ResourceAllocationStrategy.BALANCED:
            # Equal distribution
            units_per_topic = self.resource_pool / len(topics)
            for topic in topics:
                allocation[topic] = units_per_topic
                
        elif self.allocation_strategy == ResourceAllocationStrategy.PRIORITY_BASED:
            # Weighted by priority
            weights = {"high": 3, "medium": 2, "low": 1}
            total_weight = sum(weights.get(self.topics[t].priority_level, 1) for t in topics)
            
            for topic in topics:
                weight = weights.get(self.topics[topic].priority_level, 1)
                allocation[topic] = (weight / total_weight) * self.resource_pool
                
        elif self.allocation_strategy == ResourceAllocationStrategy.ACTIVITY_BASED:
            # Based on recent activity
            total_recent_items = sum(self.topics[t].items_collected for t in topics)
            
            if total_recent_items > 0:
                for topic in topics:
                    activity_ratio = self.topics[topic].items_collected / total_recent_items
                    # Blend with minimum allocation
                    allocation[topic] = max(10, activity_ratio * self.resource_pool)
            else:
                # Fallback to balanced
                units_per_topic = self.resource_pool / len(topics)
                for topic in topics:
                    allocation[topic] = units_per_topic
                    
        elif self.allocation_strategy == ResourceAllocationStrategy.ADAPTIVE:
            # Learn from patterns and adapt
            allocation = self._adaptive_resource_allocation(topics)
        
        return allocation
    
    def _adaptive_resource_allocation(self, topics: List[str]) -> Dict[str, float]:
        """Adaptive resource allocation based on learned patterns"""
        allocation = {}
        
        # Start with priority-based allocation
        weights = {"high": 3, "medium": 2, "low": 1}
        
        for topic in topics:
            state = self.topics[topic]
            base_weight = weights.get(state.priority_level, 1)
            
            # Adjust based on recent critical items
            if state.critical_items > 0:
                critical_boost = min(2.0, 1.0 + (state.critical_items / 10))
                base_weight *= critical_boost
            
            # Adjust based on error rate
            if state.error_count > 5:
                base_weight *= 0.7  # Reduce resources for problematic topics
            
            # Adjust based on relationships
            for (t1, t2), rel in self.topic_relationships.items():
                if t1 == topic and t2 in topics:
                    if rel == CrossTopicRelationship.DEPENDENT:
                        base_weight *= 1.2  # Boost dependent topics
                    elif rel == CrossTopicRelationship.COMPETITIVE:
                        base_weight *= 0.9  # Slightly reduce competitive topics
            
            allocation[topic] = base_weight
        
        # Normalize to resource pool
        total_weight = sum(allocation.values())
        if total_weight > 0:
            for topic in allocation:
                allocation[topic] = (allocation[topic] / total_weight) * self.resource_pool
        
        return allocation
    
    async def _monitor_topic_with_resources(self, 
                                           topic_slug: str,
                                           resources: float) -> Dict[str, Any]:
        """Monitor a specific topic with allocated resources"""
        config = self.topic_configs.get(topic_slug)
        if not config:
            return {"items": [], "critical": []}
        
        # Check if this topic uses a specialized monitor
        if config.get('topic_metadata', {}).get('use_specialized_monitor'):
            # Use the ClaudeFocusedMonitor for this topic
            from sources.claude_focused_monitor import ClaudeFocusedMonitor
            claude_monitor = ClaudeFocusedMonitor()
            
            self.logger.info(f"Using ClaudeFocusedMonitor for topic {topic_slug}")
            
            # Get results from the specialized monitor
            results = await claude_monitor.monitor_all()
            all_items = []
            critical_items = []
            
            for source_id, result in results.items():
                if result.success:
                    all_items.extend(result.new_items)
                    # Identify critical items
                    for item in result.new_items:
                        priority_result = self.prioritizer.prioritize(item)
                        if priority_result.priority_level in [ContentPriority.CRITICAL, ContentPriority.HIGH]:
                            critical_items.append(item)
                    self.logger.info(
                        f"ClaudeFocusedMonitor collected {len(result.new_items)} items from {source_id}"
                    )
            
            return {
                "items": all_items,
                "critical": critical_items
            }
        
        # Determine how many sources to monitor based on resources
        max_sources = int(resources / 10)  # 10 resource units per source
        
        all_items = []
        critical_items = []
        
        # Monitor sources based on tier priority
        sources_monitored = 0
        
        for tier in ['tier_1_official', 'tier_2_community', 'tier_3_aggregators']:
            if sources_monitored >= max_sources:
                break
                
            tier_config = config.get('source_mapping', {}).get(tier, {})
            
            for source_config in tier_config.get('sources', []):
                if sources_monitored >= max_sources:
                    break
                    
                # Monitor this source
                items = await self._monitor_single_source(source_config, topic_slug)
                all_items.extend(items)
                
                # Identify critical items
                for item in items:
                    priority_result = self.prioritizer.prioritize(item)
                    if priority_result.priority_level in [ContentPriority.CRITICAL, ContentPriority.HIGH]:
                        critical_items.append(item)
                
                sources_monitored += 1
        
        return {
            "items": all_items,
            "critical": critical_items
        }
    
    async def _monitor_single_source(self, 
                                    source_config: Dict,
                                    topic_slug: str) -> List[ContentItem]:
        """Monitor a single source for a topic"""
        try:
            # Create source metadata from config
            from sources.rss_monitor import RSSSourceMonitor
            
            metadata = SourceMetadata(
                source_id=source_config.get('name', 'unknown'),
                source_name=source_config.get('name', 'Unknown'),
                source_type=SourceType.RSS if source_config.get('type') == 'rss' else SourceType.API,
                source_url=source_config.get('url', ''),
                authority_score=source_config.get('authority_score', 0.7),
                update_frequency=source_config.get('update_frequency', 'hourly'),
                topics=source_config.get('topics_focus', [topic_slug])
            )
            
            # Create appropriate monitor based on source type
            if source_config.get('type') == 'rss' and source_config.get('url'):
                # Use RSS monitor for RSS feeds
                monitor = RSSSourceMonitor(
                    metadata,
                    config={
                        'timeout': source_config.get('config', {}).get('timeout', 15),
                        'max_items': source_config.get('config', {}).get('max_items', 20)
                    }
                )
                
                # Actually monitor the source
                result = await monitor.monitor()
                
                if result.success:
                    self.logger.info(
                        f"Collected {len(result.new_items)} items from {source_config.get('name')} for {topic_slug}"
                    )
                    return result.new_items
                else:
                    self.logger.warning(
                        f"Failed to monitor {source_config.get('name')}: {', '.join(result.errors)}"
                    )
                    return []
            else:
                # For non-RSS sources, log and return empty for now
                self.logger.debug(
                    f"Skipping non-RSS source {source_config.get('name')} (type: {source_config.get('type')})"
                )
                return []
                
        except Exception as e:
            self.logger.error(f"Error monitoring source {source_config.get('name')}: {str(e)}")
            return []
    
    def _analyze_cross_topic_patterns(self, items: List[ContentItem]) -> List[Dict[str, Any]]:
        """Analyze patterns across topics"""
        insights = []
        
        # Topic overlap analysis
        topic_overlap = {}
        for item in items:
            topics = set(item.topics)
            for t1 in topics:
                for t2 in topics:
                    if t1 != t2:
                        key = tuple(sorted([t1, t2]))
                        topic_overlap[key] = topic_overlap.get(key, 0) + 1
        
        if topic_overlap:
            top_overlaps = sorted(topic_overlap.items(), key=lambda x: x[1], reverse=True)[:5]
            insights.append({
                "type": "topic_overlap",
                "description": "Topics frequently appearing together",
                "data": [{"topics": list(k), "count": v} for k, v in top_overlaps]
            })
        
        # Temporal patterns
        time_buckets = {}
        for item in items:
            hour = item.published_date.hour if item.published_date else 0
            time_buckets[hour] = time_buckets.get(hour, 0) + 1
        
        if time_buckets:
            peak_hours = sorted(time_buckets.items(), key=lambda x: x[1], reverse=True)[:3]
            insights.append({
                "type": "temporal_pattern",
                "description": "Peak activity hours",
                "data": [{"hour": h, "items": c} for h, c in peak_hours]
            })
        
        return insights
    
    def _detect_emerging_relationships(self, items: List[ContentItem]) -> List[Dict[str, Any]]:
        """Detect emerging relationships between topics"""
        relationships = []
        
        # Analyze co-occurrence patterns
        co_occurrence = {}
        for item in items:
            source_topics = [t for t in item.topics if t in self.topics]
            for i, t1 in enumerate(source_topics):
                for t2 in source_topics[i+1:]:
                    key = tuple(sorted([t1, t2]))
                    co_occurrence[key] = co_occurrence.get(key, 0) + 1
        
        # Identify strong co-occurrences not yet in relationships
        for (t1, t2), count in co_occurrence.items():
            if count > 5 and (t1, t2) not in self.topic_relationships:
                # Determine relationship type based on context
                rel_type = self._infer_relationship_type(t1, t2, items)
                relationships.append({
                    "topic1": t1,
                    "topic2": t2,
                    "relationship": rel_type.value,
                    "strength": count
                })
        
        return relationships
    
    def _infer_relationship_type(self, 
                                 topic1: str,
                                 topic2: str,
                                 items: List[ContentItem]) -> CrossTopicRelationship:
        """Infer relationship type between two topics"""
        # Simple heuristic - can be made more sophisticated
        
        # Check if topics share many sources
        shared = len(self.shared_sources.get(topic1, set()) & 
                    self.shared_sources.get(topic2, set()))
        
        if shared > 3:
            return CrossTopicRelationship.COMPETITIVE
        
        # Check content overlap
        topic1_items = [i for i in items if topic1 in i.topics]
        topic2_items = [i for i in items if topic2 in i.topics]
        both_items = [i for i in items if topic1 in i.topics and topic2 in i.topics]
        
        overlap_ratio = len(both_items) / min(len(topic1_items), len(topic2_items)) if min(len(topic1_items), len(topic2_items)) > 0 else 0
        
        if overlap_ratio > 0.5:
            return CrossTopicRelationship.CONVERGENT
        elif overlap_ratio > 0.2:
            return CrossTopicRelationship.COMPLEMENTARY
        else:
            return CrossTopicRelationship.INFLUENTIAL
    
    def _update_learning(self, 
                        topics_monitored: List[str],
                        all_items: List[ContentItem],
                        critical_items: List[ContentItem]):
        """Update learned patterns from this orchestration"""
        
        # Update topic patterns
        for topic in topics_monitored:
            if topic not in self.topic_patterns:
                self.topic_patterns[topic] = []
            
            # Record pattern
            pattern = {
                "timestamp": datetime.now(),
                "items_collected": len([i for i in all_items if topic in i.topics]),
                "critical_ratio": len([i for i in critical_items if topic in i.topics]) / len(all_items) if all_items else 0,
                "hour": datetime.now().hour,
                "day_of_week": datetime.now().weekday()
            }
            
            self.topic_patterns[topic].append(pattern)
            
            # Keep only recent patterns (last 100)
            if len(self.topic_patterns[topic]) > 100:
                self.topic_patterns[topic] = self.topic_patterns[topic][-100:]
    
    def _calculate_resource_efficiency(self, allocation: Dict[str, float]) -> float:
        """Calculate how efficiently resources were used"""
        if not allocation:
            return 0.0
        
        # Calculate efficiency based on items collected per resource unit
        efficiency_scores = []
        
        for topic, resources in allocation.items():
            state = self.topics.get(topic)
            if state and resources > 0:
                items_per_resource = state.items_collected / resources
                efficiency_scores.append(items_per_resource)
        
        return sum(efficiency_scores) / len(efficiency_scores) if efficiency_scores else 0.0
    
    def get_status(self) -> Dict[str, Any]:
        """Get current Queen Agent status"""
        return {
            "orchestration_count": self.orchestration_count,
            "total_items_processed": self.total_items_processed,
            "topics_managed": len(self.topics),
            "active_topics": [t for t, s in self.topics.items() if s.items_collected > 0],
            "resource_pool": self.resource_pool,
            "allocation_strategy": self.allocation_strategy.value,
            "shared_sources": len(self.shared_sources),
            "known_relationships": len(self.topic_relationships),
            "learned_patterns": {t: len(p) for t, p in self.topic_patterns.items()}
        }
    
    def emergency_response(self, trigger: str) -> asyncio.Task:
        """
        Trigger emergency response for critical events
        
        Args:
            trigger: Description of emergency trigger
            
        Returns:
            Async task for emergency orchestration
        """
        self.logger.warning(f"EMERGENCY RESPONSE TRIGGERED: {trigger}")
        
        # Run emergency orchestration for high-priority topics only
        return asyncio.create_task(
            self.orchestrate(emergency_mode=True)
        )