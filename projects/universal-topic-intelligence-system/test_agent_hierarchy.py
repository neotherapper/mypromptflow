#!/usr/bin/env python3
"""
Test and demonstrate the 4-Level Agent Hierarchy
Shows the complete flow from Queen to Workers
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Any

from agents import (
    QueenAgent,
    ArchitectCoordinator,
    SpecialistCoordinator,
    WorkerPool,
    WorkerTask
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class HierarchyDemonstration:
    """
    Demonstrates the complete 4-level agent hierarchy
    """
    
    def __init__(self):
        # Level 1: Queen
        self.queen = QueenAgent()
        
        # Level 2: Architects (will be created per topic)
        self.architect_coordinators = {}
        
        # Level 3: Specialists
        self.specialist_coordinator = SpecialistCoordinator()
        
        # Level 4: Workers
        self.worker_pool = WorkerPool()
        
    async def setup_topics(self):
        """Register topics for monitoring"""
        topics = [
            ("react_ecosystem", "React Ecosystem"),
            ("claude_ai", "Claude AI"),
            ("web3_crypto", "Web3 & Cryptocurrency")
        ]
        
        for topic_id, topic_name in topics:
            # Register with Queen
            self.queen.register_topic(topic_id, topic_name)
            
            # Create Architect Coordinator for each topic
            self.architect_coordinators[topic_id] = ArchitectCoordinator(topic_id, topic_name)
            
        logger.info(f"✅ Registered {len(topics)} topics")
        
    async def run_complete_cycle(self) -> Dict[str, Any]:
        """Run a complete monitoring cycle through all 4 levels"""
        
        print("\n" + "="*60)
        print("🎯 UNIVERSAL TOPIC INTELLIGENCE SYSTEM")
        print("   4-Level Agent Hierarchy Demonstration")
        print("="*60 + "\n")
        
        # Setup topics
        await self.setup_topics()
        
        # LEVEL 1: Queen Orchestration
        print("👑 LEVEL 1: QUEEN AGENT ORCHESTRATION")
        print("-" * 40)
        
        queen_results = await self.queen.orchestrate()
        
        print(f"  Topics Active: {queen_results['topics_active']}")
        print(f"  Resource Allocations: {len(queen_results['allocations'])}")
        print(f"  Deployments: {len(queen_results['deployments'])}")
        print(f"  Cross-Topic Patterns: {len(queen_results['cross_topic_patterns'])}")
        
        # LEVEL 2: Architect Coordination
        print("\n🏛️ LEVEL 2: ARCHITECT AGENTS")
        print("-" * 40)
        
        architect_results = {}
        for deployment in queen_results['deployments']:
            topic_id = deployment['topic_id']
            architects_to_deploy = deployment['architects_deployed']
            
            if topic_id in self.architect_coordinators:
                coordinator = self.architect_coordinators[topic_id]
                result = await coordinator.coordinate_all(architects_to_deploy)
                architect_results[topic_id] = result
                
                print(f"  {deployment['topic_name']}:")
                print(f"    - Architects: {', '.join(architects_to_deploy)}")
                print(f"    - Specialists Deployed: {result['total_specialists']}")
        
        # LEVEL 3: Specialist Processing
        print("\n🔬 LEVEL 3: SPECIALIST AGENTS")
        print("-" * 40)
        
        # Create mock content for specialists to process
        mock_content = [
            {
                "item_id": f"item_{i}",
                "title": f"React 19 Feature #{i}",
                "content": "New React features with performance improvements and breaking changes",
                "source_type": "official",
                "authority_score": 0.9,
                "metadata": {"comments": 50, "upvotes": 200}
            }
            for i in range(1, 6)
        ]
        
        specialist_results = await self.specialist_coordinator.process_content(
            mock_content,
            ["technical", "market", "sentiment", "quality"]
        )
        
        print(f"  Content Processed: {specialist_results['content_processed']}")
        print(f"  Specialists Used: {specialist_results['specialists_used']}")
        print(f"  Total Analyses: {specialist_results['summary']['total_analyses']}")
        print(f"  High Quality: {specialist_results['summary']['high_quality_count']}")
        
        # LEVEL 4: Worker Execution
        print("\n⚙️ LEVEL 4: WORKER AGENTS")
        print("-" * 40)
        
        # Create tasks for workers
        worker_tasks = [
            WorkerTask(
                task_id=f"task_{i}",
                task_type="fetch",
                source_url="https://github.com/facebook/react" if i % 3 == 0 
                          else "https://youtube.com/watch?v=example" if i % 3 == 1
                          else "https://reddit.com/r/reactjs",
                parameters={"topic": "react"},
                priority="high"
            )
            for i in range(1, 11)
        ]
        
        worker_results = await self.worker_pool.execute_tasks(worker_tasks)
        
        print(f"  Tasks Executed: {worker_results['tasks_executed']}")
        print(f"  Successful: {worker_results['successful']}")
        print(f"  Failed: {worker_results['failed']}")
        print(f"  Success Rate: {worker_results['success_rate']:.1%}")
        print(f"  Avg Execution Time: {worker_results['average_execution_time']:.2f}s")
        
        # Worker breakdown
        print("\n  Worker Breakdown:")
        for worker_type, stats in worker_results['worker_stats'].items():
            if stats['completed'] > 0 or stats['failed'] > 0:
                print(f"    - {worker_type}: {stats['completed']} completed, {stats['failed']} failed")
        
        # SUMMARY
        print("\n" + "="*60)
        print("📊 HIERARCHY EXECUTION SUMMARY")
        print("="*60)
        
        # Simulate data flow through levels
        total_flow = {
            "queen_topics": queen_results['topics_active'],
            "architects_deployed": sum(len(d['architects_deployed']) for d in queen_results['deployments']),
            "specialists_activated": specialist_results['specialists_used'],
            "workers_executed": worker_results['tasks_executed'],
            "final_items_processed": worker_results['successful']
        }
        
        print(f"""
  Data Flow Through Hierarchy:
    👑 Queen: {total_flow['queen_topics']} topics orchestrated
       ↓
    🏛️ Architects: {total_flow['architects_deployed']} strategies deployed
       ↓
    🔬 Specialists: {total_flow['specialists_activated']} content processors
       ↓
    ⚙️ Workers: {total_flow['workers_executed']} tasks executed
       ↓
    ✅ Result: {total_flow['final_items_processed']} items successfully processed
        """)
        
        # Performance metrics
        print("  Performance Metrics:")
        print(f"    - Resource Efficiency: {queen_results['performance']['resource_utilization']['efficiency']:.1%}")
        print(f"    - Average Health Score: {queen_results['performance']['average_health_score']:.2f}")
        print(f"    - Cross-Topic Insights: {len(queen_results['cross_topic_patterns'])}")
        
        # Simulate updating Queen with results
        for topic_id in self.queen.topic_registry:
            self.queen.update_topic_status(topic_id, worker_results['successful'])
        
        return {
            "queen_results": queen_results,
            "architect_results": architect_results,
            "specialist_results": specialist_results,
            "worker_results": worker_results,
            "total_flow": total_flow
        }

async def main():
    """Run the demonstration"""
    demo = HierarchyDemonstration()
    results = await demo.run_complete_cycle()
    
    print("\n✨ 4-Level Agent Hierarchy Demonstration Complete!")
    print(f"   Total execution time: {datetime.now().isoformat()}")
    
    return results

if __name__ == "__main__":
    asyncio.run(main())