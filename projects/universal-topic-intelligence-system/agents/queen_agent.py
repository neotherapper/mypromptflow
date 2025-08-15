#!/usr/bin/env python3
"""
Queen Agent - Level 1 Orchestrator
Universal topic orchestrator managing all monitored topics
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)

class ResourcePriority(Enum):
    """Priority levels for resource allocation"""
    CRITICAL = "critical"  # Breaking news, major releases
    HIGH = "high"          # Important updates, trending topics
    MEDIUM = "medium"      # Regular monitoring
    LOW = "low"            # Background monitoring

@dataclass
class TopicStatus:
    """Status tracking for each monitored topic"""
    topic_id: str
    name: str
    last_update: datetime
    items_collected: int
    priority: ResourcePriority
    health_score: float  # 0.0 to 1.0
    active_architects: List[str] = field(default_factory=list)
    
class QueenAgent:
    """
    Level 1 - Queen Agent
    Universal orchestrator managing all topics and resource allocation
    """
    
    def __init__(self):
        self.topic_registry: Dict[str, TopicStatus] = {}
        self.architect_pool: Dict[str, Any] = {}  # Architect agents
        self.resource_budget = {
            "max_concurrent_monitors": 20,
            "max_api_calls_per_minute": 100,
            "max_storage_mb_per_hour": 500
        }
        self.performance_metrics = {
            "topics_monitored": 0,
            "total_items_collected": 0,
            "cross_topic_insights": 0,
            "resource_efficiency": 0.0
        }
        
    async def orchestrate(self) -> Dict[str, Any]:
        """Main orchestration loop"""
        logger.info("👑 Queen Agent: Starting orchestration cycle")
        
        # 1. Assess topic priorities
        priorities = await self.assess_topic_priorities()
        
        # 2. Allocate resources
        allocations = await self.allocate_resources(priorities)
        
        # 3. Deploy architects
        deployments = await self.deploy_architects(allocations)
        
        # 4. Monitor performance
        performance = await self.monitor_performance()
        
        # 5. Detect cross-topic patterns
        patterns = await self.detect_cross_topic_patterns()
        
        # 6. Adjust strategies
        adjustments = await self.adjust_strategies(performance, patterns)
        
        return {
            "timestamp": datetime.now().isoformat(),
            "topics_active": len(self.topic_registry),
            "priorities": priorities,
            "allocations": allocations,
            "deployments": deployments,
            "performance": performance,
            "cross_topic_patterns": patterns,
            "adjustments": adjustments
        }
    
    async def assess_topic_priorities(self) -> Dict[str, ResourcePriority]:
        """Assess priority levels for all topics"""
        priorities = {}
        
        for topic_id, status in self.topic_registry.items():
            # Calculate priority based on multiple factors
            time_since_update = (datetime.now() - status.last_update).total_seconds()
            
            if time_since_update < 300:  # Updated in last 5 minutes
                priority = ResourcePriority.LOW
            elif time_since_update < 1800:  # Updated in last 30 minutes
                priority = ResourcePriority.MEDIUM
            elif time_since_update < 3600:  # Updated in last hour
                priority = ResourcePriority.HIGH
            else:  # Over an hour old
                priority = ResourcePriority.CRITICAL
                
            # Adjust based on topic importance
            if "claude" in status.name.lower() or "react" in status.name.lower():
                if priority == ResourcePriority.LOW:
                    priority = ResourcePriority.MEDIUM
                elif priority == ResourcePriority.MEDIUM:
                    priority = ResourcePriority.HIGH
                    
            priorities[topic_id] = priority
            status.priority = priority
            
        logger.info(f"Queen: Assessed priorities for {len(priorities)} topics")
        return priorities
    
    async def allocate_resources(self, priorities: Dict[str, ResourcePriority]) -> Dict[str, Dict]:
        """Allocate resources based on priorities"""
        allocations = {}
        
        # Count topics by priority
        priority_counts = {p: 0 for p in ResourcePriority}
        for priority in priorities.values():
            priority_counts[priority] += 1
            
        # Allocate monitoring slots
        total_slots = self.resource_budget["max_concurrent_monitors"]
        
        # Allocation strategy: 40% critical, 30% high, 20% medium, 10% low
        slot_distribution = {
            ResourcePriority.CRITICAL: int(total_slots * 0.4),
            ResourcePriority.HIGH: int(total_slots * 0.3),
            ResourcePriority.MEDIUM: int(total_slots * 0.2),
            ResourcePriority.LOW: int(total_slots * 0.1)
        }
        
        for topic_id, priority in priorities.items():
            allocations[topic_id] = {
                "monitoring_slots": max(1, slot_distribution[priority] // max(1, priority_counts[priority])),
                "api_calls_per_minute": 20 if priority == ResourcePriority.CRITICAL else 10,
                "storage_mb": 50 if priority in [ResourcePriority.CRITICAL, ResourcePriority.HIGH] else 25,
                "priority": priority.value
            }
            
        logger.info(f"Queen: Allocated resources for {len(allocations)} topics")
        return allocations
    
    async def deploy_architects(self, allocations: Dict[str, Dict]) -> List[Dict]:
        """Deploy architect agents based on allocations"""
        deployments = []
        
        for topic_id, allocation in allocations.items():
            if topic_id in self.topic_registry:
                status = self.topic_registry[topic_id]
                
                # Deploy architects based on priority
                if allocation["priority"] == ResourcePriority.CRITICAL.value:
                    architects = ["official_source", "community", "aggregator"]
                elif allocation["priority"] == ResourcePriority.HIGH.value:
                    architects = ["official_source", "community"]
                else:
                    architects = ["aggregator"]
                    
                deployment = {
                    "topic_id": topic_id,
                    "topic_name": status.name,
                    "architects_deployed": architects,
                    "resources": allocation,
                    "timestamp": datetime.now().isoformat()
                }
                
                deployments.append(deployment)
                status.active_architects = architects
                
        logger.info(f"Queen: Deployed architects for {len(deployments)} topics")
        return deployments
    
    async def monitor_performance(self) -> Dict[str, Any]:
        """Monitor system performance"""
        total_items = sum(status.items_collected for status in self.topic_registry.values())
        active_topics = len([s for s in self.topic_registry.values() if s.active_architects])
        
        performance = {
            "total_items_collected": total_items,
            "active_topics": active_topics,
            "average_health_score": sum(s.health_score for s in self.topic_registry.values()) / max(1, len(self.topic_registry)),
            "resource_utilization": {
                "monitoring_slots_used": active_topics,
                "monitoring_slots_total": self.resource_budget["max_concurrent_monitors"],
                "efficiency": active_topics / max(1, self.resource_budget["max_concurrent_monitors"])
            }
        }
        
        self.performance_metrics.update(performance)
        logger.info(f"Queen: Performance - {active_topics} active topics, {total_items} items collected")
        
        return performance
    
    async def detect_cross_topic_patterns(self) -> List[Dict]:
        """Detect patterns across multiple topics"""
        patterns = []
        
        # Simple pattern detection - would be more sophisticated in real implementation
        topics = list(self.topic_registry.values())
        
        for i, topic1 in enumerate(topics):
            for topic2 in topics[i+1:]:
                # Check for correlated activity
                if abs(topic1.items_collected - topic2.items_collected) < 5:
                    patterns.append({
                        "type": "correlated_activity",
                        "topics": [topic1.name, topic2.name],
                        "confidence": 0.7,
                        "insight": f"Similar activity levels between {topic1.name} and {topic2.name}"
                    })
                    
        self.performance_metrics["cross_topic_insights"] = len(patterns)
        logger.info(f"Queen: Detected {len(patterns)} cross-topic patterns")
        
        return patterns
    
    async def adjust_strategies(self, performance: Dict, patterns: List[Dict]) -> Dict[str, Any]:
        """Adjust strategies based on performance and patterns"""
        adjustments = {
            "resource_reallocations": [],
            "priority_changes": [],
            "new_monitoring_targets": []
        }
        
        # Adjust based on efficiency
        if performance["resource_utilization"]["efficiency"] < 0.5:
            adjustments["resource_reallocations"].append({
                "action": "increase_monitoring",
                "reason": "Low resource utilization",
                "target_efficiency": 0.75
            })
            
        # Adjust based on patterns
        for pattern in patterns:
            if pattern["type"] == "correlated_activity":
                adjustments["new_monitoring_targets"].append({
                    "action": "create_joint_monitor",
                    "topics": pattern["topics"],
                    "reason": pattern["insight"]
                })
                
        logger.info(f"Queen: Made {len(adjustments['resource_reallocations'])} resource adjustments")
        
        return adjustments
    
    def register_topic(self, topic_id: str, name: str):
        """Register a new topic for monitoring"""
        self.topic_registry[topic_id] = TopicStatus(
            topic_id=topic_id,
            name=name,
            last_update=datetime.now(),
            items_collected=0,
            priority=ResourcePriority.MEDIUM,
            health_score=1.0
        )
        logger.info(f"Queen: Registered new topic '{name}' with ID {topic_id}")
        
    def update_topic_status(self, topic_id: str, items_collected: int):
        """Update topic status after monitoring"""
        if topic_id in self.topic_registry:
            status = self.topic_registry[topic_id]
            status.last_update = datetime.now()
            status.items_collected += items_collected
            status.health_score = min(1.0, items_collected / 10.0)  # Simple health calculation
            logger.info(f"Queen: Updated topic '{status.name}' - {items_collected} new items")