#!/usr/bin/env python3
"""
Integration Example for Intelligent Batching System
Demonstrates how all components work together in a production scenario.
"""

import asyncio
import time
import logging
from typing import Dict, List, Any
import json
from pathlib import Path

from adaptive_batching import create_adaptive_batching_engine, OperationType, PerformanceMetrics
from resource_monitor import create_resource_monitor
from performance_optimizer import create_performance_optimizer, OptimizationTarget
from batch_coordinator import create_batch_coordinator
from load_testing import create_load_testing_framework, LoadTestConfiguration

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IntelligentBatchingSystem:
    """
    Complete intelligent batching system integration example.
    Demonstrates production-ready usage of all components.
    """
    
    def __init__(self, config_dir: str = "schemas/"):
        """Initialize the complete system"""
        self.config_dir = Path(config_dir)
        
        # Initialize all components
        self.coordinator = create_batch_coordinator(str(self.config_dir / "batching_config.yaml"))
        self.load_tester = create_load_testing_framework(self.coordinator)
        
        # Performance tracking
        self.performance_history: List[Dict[str, Any]] = []
        self.optimization_results: List[Dict[str, Any]] = []
        
    async def run_production_example(self):
        """Run a complete production example"""
        logger.info("🚀 Starting Intelligent Batching System Production Example")
        
        try:
            # Step 1: Start the system
            await self._start_system()
            
            # Step 2: Run baseline performance test
            baseline_results = await self._run_baseline_test()
            
            # Step 3: Submit various workloads
            workload_results = await self._submit_production_workloads()
            
            # Step 4: Run optimization cycle
            optimization_results = await self._run_optimization_cycle()
            
            # Step 5: Validate improvements
            validation_results = await self._validate_improvements()
            
            # Step 6: Generate comprehensive report
            report = await self._generate_performance_report(
                baseline_results, workload_results, optimization_results, validation_results
            )
            
            # Step 7: Save results
            await self._save_results(report)
            
            logger.info("✅ Production example completed successfully")
            
        except Exception as e:
            logger.error(f"❌ Production example failed: {e}")
            raise
        finally:
            await self._cleanup_system()
    
    async def _start_system(self):
        """Start all system components"""
        logger.info("🔧 Starting system components...")
        
        # Start coordinator (which starts resource monitoring)
        self.coordinator.start()
        
        # Wait for system stabilization
        await asyncio.sleep(10)
        
        logger.info("✅ All components started successfully")
    
    async def _run_baseline_test(self) -> Dict[str, Any]:
        """Run baseline performance test"""
        logger.info("📊 Running baseline performance test...")
        
        # Create baseline test configuration
        baseline_config = LoadTestConfiguration(
            name="Production Baseline",
            description="Baseline performance measurement for production workload",
            duration_seconds=300,  # 5 minutes
            concurrent_users=10,
            operations_per_user=100,
            operation_types=[OperationType.READ, OperationType.WRITE],
            batch_sizes=[25, 50, 100]
        )
        
        # Run baseline test
        baseline_result = await self.load_tester.run_load_test(baseline_config)
        
        logger.info(f"📈 Baseline throughput: {baseline_result.operations_per_second:.2f} ops/sec")
        logger.info(f"⏱️  Baseline response time: {baseline_result.average_response_time:.2f}ms")
        logger.info(f"🎯 Baseline success rate: {(1 - baseline_result.error_rate):.1%}")
        
        return {
            'test_name': baseline_result.test_name,
            'throughput': baseline_result.operations_per_second,
            'response_time': baseline_result.average_response_time,
            'error_rate': baseline_result.error_rate,
            'resource_usage': baseline_result.resource_usage
        }
    
    async def _submit_production_workloads(self) -> List[Dict[str, Any]]:
        """Submit various production workloads to test adaptability"""
        logger.info("🏭 Submitting production workloads...")
        
        workload_results = []
        
        # Workload 1: High-priority read operations
        logger.info("📖 Testing high-priority read workload...")
        read_operations = [
            {'id': f'read_{i}', 'type': 'database_query', 'data': f'select * from table where id = {i}'}
            for i in range(500)
        ]
        
        read_job_id = self.coordinator.submit_job(
            read_operations, OperationType.READ, priority="high"
        )
        
        # Workload 2: Bulk write operations
        logger.info("✍️  Testing bulk write workload...")
        write_operations = [
            {'id': f'write_{i}', 'type': 'database_insert', 'data': {'user_id': i, 'timestamp': time.time()}}
            for i in range(200)
        ]
        
        write_job_id = self.coordinator.submit_job(
            write_operations, OperationType.BULK_CREATE, priority="normal"
        )
        
        # Workload 3: Mixed priority operations
        logger.info("🔀 Testing mixed priority workload...")
        mixed_operations = []
        for i in range(300):
            priority = "critical" if i % 10 == 0 else "normal" if i % 3 == 0 else "low"
            mixed_operations.append({
                'id': f'mixed_{i}',
                'type': 'update_operation',
                'data': {'record_id': i, 'priority': priority},
                'priority': priority
            })
        
        mixed_job_id = self.coordinator.submit_job(
            mixed_operations, OperationType.UPDATE, priority="normal"
        )
        
        # Monitor job completion
        jobs_to_monitor = [read_job_id, write_job_id, mixed_job_id]
        completed_jobs = []
        
        while len(completed_jobs) < len(jobs_to_monitor):
            await asyncio.sleep(5)
            
            for job_id in jobs_to_monitor:
                if job_id not in completed_jobs:
                    status = self.coordinator.get_job_status(job_id)
                    if status and status['status'] in ['completed', 'failed']:
                        completed_jobs.append(job_id)
                        workload_results.append(status)
                        logger.info(f"✅ Job {job_id} completed: {status['status']}")
        
        logger.info(f"🎯 Completed {len(workload_results)} production workloads")
        return workload_results
    
    async def _run_optimization_cycle(self) -> Dict[str, Any]:
        """Run optimization cycle to improve performance"""
        logger.info("🔧 Running optimization cycle...")
        
        # Get current performance metrics
        dashboard = self.coordinator.get_performance_dashboard()
        current_performance = dashboard.get('performance_metrics', {})
        
        logger.info("📊 Current Performance:")
        logger.info(f"  Throughput: {current_performance.get('average_throughput', 0):.2f} ops/sec")
        logger.info(f"  Response Time: {current_performance.get('average_execution_time', 0) * 1000:.2f}ms")
        logger.info(f"  CPU Usage: {current_performance.get('system_cpu_usage', 0):.1f}%")
        logger.info(f"  Memory Usage: {current_performance.get('system_memory_usage', 0):.1f}%")
        
        # Run A/B test for batch size optimization
        logger.info("🧪 Starting A/B test for batch size optimization...")
        
        optimizer = self.coordinator.performance_optimizer
        ab_test_id = optimizer.start_ab_test(
            test_name="batch_size_optimization",
            control_strategy="current_adaptive",
            test_strategy="ml_optimized",
            duration_hours=1
        )
        
        # Simulate A/B test results (in real scenario, this would happen naturally)
        await self._simulate_ab_test_results(optimizer, ab_test_id)
        
        # Analyze A/B test results
        ab_results = optimizer.analyze_ab_test(ab_test_id)
        
        logger.info("🔬 A/B Test Results:")
        logger.info(f"  Control Performance: {ab_results.get('control_mean', 0):.2f}")
        logger.info(f"  Test Performance: {ab_results.get('test_mean', 0):.2f}")
        logger.info(f"  Improvement: {ab_results.get('improvement_percent', 0):.1f}%")
        logger.info(f"  Recommendation: {ab_results.get('recommendation', 'unknown')}")
        
        return ab_results
    
    async def _simulate_ab_test_results(self, optimizer, test_id: str):
        """Simulate A/B test results for demonstration"""
        import random
        
        # Simulate control group results (current performance)
        for _ in range(50):
            control_score = random.gauss(75, 10)  # Mean 75, std 10
            optimizer.record_ab_test_result(test_id, False, control_score)
        
        # Simulate test group results (improved performance)
        for _ in range(50):
            test_score = random.gauss(85, 8)  # Mean 85, std 8 (better performance)
            optimizer.record_ab_test_result(test_id, True, test_score)
    
    async def _validate_improvements(self) -> Dict[str, Any]:
        """Validate performance improvements after optimization"""
        logger.info("✅ Validating performance improvements...")
        
        # Run validation test
        validation_config = LoadTestConfiguration(
            name="Post-Optimization Validation",
            description="Validate performance improvements after optimization",
            duration_seconds=300,
            concurrent_users=15,  # Slightly higher load
            operations_per_user=120,
            operation_types=[OperationType.READ, OperationType.WRITE, OperationType.UPDATE],
            batch_sizes=[50, 100]  # Focus on optimal sizes
        )
        
        validation_result = await self.load_tester.run_load_test(validation_config)
        
        logger.info("📈 Validation Results:")
        logger.info(f"  Throughput: {validation_result.operations_per_second:.2f} ops/sec")
        logger.info(f"  Response Time: {validation_result.average_response_time:.2f}ms")
        logger.info(f"  P95 Response Time: {validation_result.p95_response_time:.2f}ms")
        logger.info(f"  Error Rate: {validation_result.error_rate:.2%}")
        logger.info(f"  Resource Efficiency: CPU {validation_result.resource_usage.get('average_cpu', 0):.1f}%, Memory {validation_result.resource_usage.get('average_memory', 0):.1f}%")
        
        return {
            'test_name': validation_result.test_name,
            'throughput': validation_result.operations_per_second,
            'response_time': validation_result.average_response_time,
            'p95_response_time': validation_result.p95_response_time,
            'error_rate': validation_result.error_rate,
            'resource_usage': validation_result.resource_usage
        }
    
    async def _generate_performance_report(self, 
                                         baseline: Dict[str, Any],
                                         workloads: List[Dict[str, Any]],
                                         optimization: Dict[str, Any],
                                         validation: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        logger.info("📋 Generating comprehensive performance report...")
        
        # Calculate improvements
        throughput_improvement = ((validation['throughput'] - baseline['throughput']) / 
                                baseline['throughput'] * 100)
        response_time_improvement = ((baseline['response_time'] - validation['response_time']) / 
                                   baseline['response_time'] * 100)
        
        # Resource efficiency calculation
        baseline_resource_score = (baseline['resource_usage'].get('average_cpu', 0) + 
                                 baseline['resource_usage'].get('average_memory', 0)) / 2
        validation_resource_score = (validation['resource_usage'].get('average_cpu', 0) + 
                                   validation['resource_usage'].get('average_memory', 0)) / 2
        resource_efficiency_improvement = ((baseline_resource_score - validation_resource_score) / 
                                         baseline_resource_score * 100)
        
        report = {
            'timestamp': time.time(),
            'test_duration_minutes': 30,  # Approximate total test time
            'summary': {
                'throughput_improvement_percent': throughput_improvement,
                'response_time_improvement_percent': response_time_improvement,
                'resource_efficiency_improvement_percent': resource_efficiency_improvement,
                'error_rate_change': validation['error_rate'] - baseline['error_rate']
            },
            'baseline_performance': baseline,
            'validation_performance': validation,
            'workload_results': workloads,
            'optimization_results': optimization,
            'achievements': self._calculate_achievements(baseline, validation),
            'recommendations': self._generate_recommendations(baseline, validation, optimization)
        }
        
        # Log summary
        logger.info("🎯 Performance Report Summary:")
        logger.info(f"  📈 Throughput Improvement: {throughput_improvement:+.1f}%")
        logger.info(f"  ⚡ Response Time Improvement: {response_time_improvement:+.1f}%")
        logger.info(f"  🔋 Resource Efficiency Improvement: {resource_efficiency_improvement:+.1f}%")
        logger.info(f"  🎪 Error Rate Change: {report['summary']['error_rate_change']:+.3f}")
        
        return report
    
    def _calculate_achievements(self, baseline: Dict[str, Any], validation: Dict[str, Any]) -> List[str]:
        """Calculate and list achievements"""
        achievements = []
        
        # Throughput achievements
        throughput_improvement = ((validation['throughput'] - baseline['throughput']) / 
                                baseline['throughput'] * 100)
        if throughput_improvement >= 40:
            achievements.append(f"🚀 Exceptional throughput improvement: +{throughput_improvement:.1f}%")
        elif throughput_improvement >= 20:
            achievements.append(f"📈 Significant throughput improvement: +{throughput_improvement:.1f}%")
        elif throughput_improvement >= 10:
            achievements.append(f"📊 Good throughput improvement: +{throughput_improvement:.1f}%")
        
        # Response time achievements
        response_time_improvement = ((baseline['response_time'] - validation['response_time']) / 
                                   baseline['response_time'] * 100)
        if response_time_improvement >= 30:
            achievements.append(f"⚡ Outstanding response time improvement: +{response_time_improvement:.1f}%")
        elif response_time_improvement >= 15:
            achievements.append(f"🎯 Great response time improvement: +{response_time_improvement:.1f}%")
        
        # Error rate achievements
        if validation['error_rate'] < baseline['error_rate']:
            error_improvement = ((baseline['error_rate'] - validation['error_rate']) / 
                               baseline['error_rate'] * 100)
            achievements.append(f"🛡️ Improved reliability: -{error_improvement:.1f}% error rate reduction")
        
        # Resource efficiency achievements
        baseline_cpu = baseline['resource_usage'].get('average_cpu', 0)
        validation_cpu = validation['resource_usage'].get('average_memory', 0)
        if validation_cpu < baseline_cpu * 0.8:
            achievements.append("🔋 Significant resource efficiency improvement")
        
        return achievements
    
    def _generate_recommendations(self, 
                                baseline: Dict[str, Any], 
                                validation: Dict[str, Any],
                                optimization: Dict[str, Any]) -> List[str]:
        """Generate optimization recommendations"""
        recommendations = []
        
        # Performance recommendations
        if validation['throughput'] < baseline['throughput'] * 1.1:
            recommendations.append(
                "Consider implementing more aggressive batch sizing strategies for higher throughput"
            )
        
        if validation['response_time'] > 500:  # milliseconds
            recommendations.append(
                "Response times above target - implement response time-focused optimization"
            )
        
        # Resource recommendations
        cpu_usage = validation['resource_usage'].get('average_cpu', 0)
        memory_usage = validation['resource_usage'].get('average_memory', 0)
        
        if cpu_usage > 80:
            recommendations.append(
                "High CPU usage detected - consider horizontal scaling or CPU optimization"
            )
        
        if memory_usage > 85:
            recommendations.append(
                "High memory usage detected - implement memory-efficient batching strategies"
            )
        
        # A/B test recommendations
        if optimization.get('recommendation') == 'adopt_test':
            recommendations.append(
                "A/B test shows positive results - consider adopting test strategy in production"
            )
        
        return recommendations
    
    async def _save_results(self, report: Dict[str, Any]):
        """Save results to files"""
        logger.info("💾 Saving results...")
        
        # Create results directory
        results_dir = Path("results")
        results_dir.mkdir(exist_ok=True)
        
        # Save comprehensive report
        report_file = results_dir / f"performance_report_{int(time.time())}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        # Save human-readable summary
        summary_file = results_dir / f"performance_summary_{int(time.time())}.txt"
        with open(summary_file, 'w') as f:
            f.write("# Intelligent Batching System Performance Report\n\n")
            f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Summary\n")
            f.write(f"Throughput Improvement: {report['summary']['throughput_improvement_percent']:+.1f}%\n")
            f.write(f"Response Time Improvement: {report['summary']['response_time_improvement_percent']:+.1f}%\n")
            f.write(f"Resource Efficiency Improvement: {report['summary']['resource_efficiency_improvement_percent']:+.1f}%\n\n")
            
            f.write("## Achievements\n")
            for achievement in report['achievements']:
                f.write(f"- {achievement}\n")
            f.write("\n")
            
            f.write("## Recommendations\n")
            for recommendation in report['recommendations']:
                f.write(f"- {recommendation}\n")
        
        logger.info(f"📄 Report saved to: {report_file}")
        logger.info(f"📄 Summary saved to: {summary_file}")
    
    async def _cleanup_system(self):
        """Clean up system resources"""
        logger.info("🧹 Cleaning up system resources...")
        
        # Stop coordinator
        self.coordinator.stop()
        
        logger.info("✅ Cleanup completed")

# Advanced usage examples
class AdvancedUsageExamples:
    """Advanced usage examples for specific scenarios"""
    
    @staticmethod
    async def maritime_insurance_scenario():
        """Example for maritime insurance specific workload"""
        logger.info("🚢 Running Maritime Insurance Scenario")
        
        system = IntelligentBatchingSystem()
        
        try:
            system.coordinator.start()
            await asyncio.sleep(5)
            
            # Maritime insurance specific operations
            policy_operations = [
                {'id': f'policy_{i}', 'type': 'policy_validation', 'vessel_id': f'V{i:06d}'}
                for i in range(100)
            ]
            
            claim_operations = [
                {'id': f'claim_{i}', 'type': 'claim_processing', 'claim_amount': i * 1000}
                for i in range(50)
            ]
            
            risk_operations = [
                {'id': f'risk_{i}', 'type': 'risk_assessment', 'route': f'Route_{i}'}
                for i in range(75)
            ]
            
            # Submit jobs with maritime insurance priorities
            policy_job = system.coordinator.submit_job(policy_operations, OperationType.READ, "high")
            claim_job = system.coordinator.submit_job(claim_operations, OperationType.WRITE, "critical")
            risk_job = system.coordinator.submit_job(risk_operations, OperationType.QUERY, "normal")
            
            logger.info(f"📋 Submitted maritime insurance jobs: {policy_job}, {claim_job}, {risk_job}")
            
            # Monitor performance for maritime insurance workload
            await asyncio.sleep(30)
            
            dashboard = system.coordinator.get_performance_dashboard()
            logger.info("🎯 Maritime Insurance Performance:")
            logger.info(f"  Active Jobs: {dashboard.get('coordinator_status', {}).get('active_jobs', 0)}")
            logger.info(f"  Average Throughput: {dashboard.get('performance_metrics', {}).get('average_throughput', 0):.2f}")
            
        finally:
            system.coordinator.stop()
    
    @staticmethod
    async def high_volume_scenario():
        """Example for high-volume data processing"""
        logger.info("📊 Running High-Volume Data Processing Scenario")
        
        system = IntelligentBatchingSystem()
        
        try:
            system.coordinator.start()
            await asyncio.sleep(5)
            
            # High-volume test configuration
            high_volume_config = LoadTestConfiguration(
                name="High Volume Processing",
                description="Test system under high-volume load",
                duration_seconds=600,  # 10 minutes
                concurrent_users=50,
                operations_per_user=500,
                operation_types=[OperationType.BULK_CREATE, OperationType.READ],
                batch_sizes=[100, 250, 500]
            )
            
            result = await system.load_tester.run_load_test(high_volume_config)
            
            logger.info("📈 High-Volume Results:")
            logger.info(f"  Total Operations: {result.total_operations:,}")
            logger.info(f"  Throughput: {result.operations_per_second:.2f} ops/sec")
            logger.info(f"  P99 Response Time: {result.p99_response_time:.2f}ms")
            logger.info(f"  Success Rate: {(1 - result.error_rate):.1%}")
            
        finally:
            system.coordinator.stop()

# Main execution
async def main():
    """Main execution function"""
    print("🎯 Intelligent Batching System - Production Integration Example")
    print("=" * 70)
    
    # Run complete production example
    system = IntelligentBatchingSystem()
    await system.run_production_example()
    
    print("\n" + "=" * 70)
    print("🚢 Running Advanced Maritime Insurance Scenario")
    await AdvancedUsageExamples.maritime_insurance_scenario()
    
    print("\n" + "=" * 70)
    print("📊 Running High-Volume Processing Scenario")
    await AdvancedUsageExamples.high_volume_scenario()
    
    print("\n" + "=" * 70)
    print("✅ All examples completed successfully!")

if __name__ == "__main__":
    asyncio.run(main())