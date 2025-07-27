#!/usr/bin/env python3
"""
Load Testing Framework for Intelligent Batching System
Comprehensive load testing and performance benchmarking for batch operations.
"""

import asyncio
import time
import logging
import random
from typing import Dict, List, Tuple, Optional, Any, Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import statistics
import json
import yaml
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from .batch_coordinator import BatchCoordinator, OperationType
from .adaptive_batching import PerformanceMetrics
from .performance_optimizer import OptimizationTarget

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class LoadTestConfiguration:
    """Configuration for load testing scenarios"""
    name: str
    description: str
    duration_seconds: int = 300
    concurrent_users: int = 10
    operations_per_user: int = 100
    operation_types: List[OperationType] = field(default_factory=lambda: [OperationType.READ])
    batch_sizes: List[int] = field(default_factory=lambda: [10, 25, 50, 100])
    ramp_up_seconds: int = 60
    think_time_seconds: float = 1.0
    data_size_bytes: int = 1024
    failure_rate: float = 0.0  # Simulated failure rate
    priority_distribution: Dict[str, float] = field(default_factory=lambda: {"normal": 1.0})

@dataclass
class LoadTestResult:
    """Results from a load test execution"""
    test_name: str
    start_time: float
    end_time: float
    duration: float
    total_operations: int
    successful_operations: int
    failed_operations: int
    operations_per_second: float
    average_response_time: float
    median_response_time: float
    p95_response_time: float
    p99_response_time: float
    min_response_time: float
    max_response_time: float
    error_rate: float
    resource_usage: Dict[str, float]
    batch_performance: Dict[int, Dict[str, float]]
    performance_over_time: List[Dict[str, Any]]

@dataclass
class BenchmarkResult:
    """Results from benchmark comparison"""
    test_configurations: List[LoadTestConfiguration]
    results: List[LoadTestResult]
    comparison_metrics: Dict[str, Any]
    recommendations: List[str]
    best_configuration: Optional[str] = None

class LoadTestingFramework:
    """
    Comprehensive load testing framework for batch operations with
    performance benchmarking and optimization recommendations.
    """
    
    def __init__(self, coordinator: BatchCoordinator, results_dir: str = "load_test_results/"):
        """Initialize the load testing framework"""
        self.coordinator = coordinator
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        # Test execution state
        self.active_tests: Dict[str, Dict[str, Any]] = {}
        self.test_history: List[LoadTestResult] = []
        
        # Performance tracking
        self.performance_collectors: List[Callable] = []
        self.resource_snapshots: List[Dict[str, Any]] = []
        
        # Load test scenarios
        self.predefined_scenarios = self._create_predefined_scenarios()
    
    def _create_predefined_scenarios(self) -> Dict[str, LoadTestConfiguration]:
        """Create predefined load test scenarios"""
        return {
            'baseline': LoadTestConfiguration(
                name="Baseline Performance",
                description="Basic performance baseline with moderate load",
                duration_seconds=300,
                concurrent_users=5,
                operations_per_user=50,
                batch_sizes=[25, 50]
            ),
            'stress_test': LoadTestConfiguration(
                name="Stress Test",
                description="High load stress testing",
                duration_seconds=600,
                concurrent_users=20,
                operations_per_user=200,
                batch_sizes=[10, 50, 100, 200]
            ),
            'endurance_test': LoadTestConfiguration(
                name="Endurance Test",
                description="Long-running endurance testing",
                duration_seconds=3600,  # 1 hour
                concurrent_users=10,
                operations_per_user=500,
                batch_sizes=[50, 100]
            ),
            'spike_test': LoadTestConfiguration(
                name="Spike Test",
                description="Sudden load spike testing",
                duration_seconds=300,
                concurrent_users=50,
                operations_per_user=100,
                ramp_up_seconds=10,  # Very fast ramp-up
                batch_sizes=[25, 75]
            ),
            'batch_size_comparison': LoadTestConfiguration(
                name="Batch Size Comparison",
                description="Compare different batch sizes",
                duration_seconds=600,
                concurrent_users=10,
                operations_per_user=100,
                batch_sizes=[5, 10, 25, 50, 100, 200, 500]
            ),
            'mixed_operations': LoadTestConfiguration(
                name="Mixed Operations",
                description="Test with mixed operation types",
                duration_seconds=450,
                concurrent_users=15,
                operations_per_user=150,
                operation_types=[OperationType.READ, OperationType.WRITE, OperationType.UPDATE],
                batch_sizes=[25, 50, 100]
            ),
            'priority_testing': LoadTestConfiguration(
                name="Priority Testing",
                description="Test with different priority levels",
                duration_seconds=400,
                concurrent_users=12,
                operations_per_user=100,
                batch_sizes=[50],
                priority_distribution={"critical": 0.1, "high": 0.2, "normal": 0.5, "low": 0.2}
            )
        }
    
    async def run_load_test(self, config: LoadTestConfiguration) -> LoadTestResult:
        """Execute a comprehensive load test"""
        logger.info(f"Starting load test: {config.name}")
        start_time = time.time()
        
        # Initialize test tracking
        test_id = f"{config.name}_{int(start_time)}"
        self.active_tests[test_id] = {
            'config': config,
            'start_time': start_time,
            'operations_completed': 0,
            'operations_failed': 0,
            'response_times': [],
            'batch_results': {}
        }
        
        # Start performance monitoring
        monitoring_task = asyncio.create_task(self._monitor_performance(test_id, config.duration_seconds))
        
        try:
            # Execute test with different batch sizes
            all_results = []
            
            for batch_size in config.batch_sizes:
                logger.info(f"Testing batch size: {batch_size}")
                batch_results = await self._execute_batch_size_test(config, batch_size)
                all_results.extend(batch_results)
                
                # Store batch-specific performance
                self.active_tests[test_id]['batch_results'][batch_size] = {
                    'operations': len(batch_results),
                    'avg_response_time': statistics.mean([r['response_time'] for r in batch_results]),
                    'success_rate': sum(1 for r in batch_results if r['success']) / len(batch_results)
                }
            
            # Calculate overall results
            end_time = time.time()
            duration = end_time - start_time
            
            successful_ops = sum(1 for r in all_results if r['success'])
            failed_ops = len(all_results) - successful_ops
            response_times = [r['response_time'] for r in all_results if r['success']]
            
            if response_times:
                avg_response_time = statistics.mean(response_times)
                median_response_time = statistics.median(response_times)
                p95_response_time = np.percentile(response_times, 95)
                p99_response_time = np.percentile(response_times, 99)
                min_response_time = min(response_times)
                max_response_time = max(response_times)
            else:
                avg_response_time = median_response_time = p95_response_time = p99_response_time = 0
                min_response_time = max_response_time = 0
            
            # Get resource usage summary
            resource_usage = await self._calculate_resource_usage()
            
            # Create result
            result = LoadTestResult(
                test_name=config.name,
                start_time=start_time,
                end_time=end_time,
                duration=duration,
                total_operations=len(all_results),
                successful_operations=successful_ops,
                failed_operations=failed_ops,
                operations_per_second=len(all_results) / duration if duration > 0 else 0,
                average_response_time=avg_response_time,
                median_response_time=median_response_time,
                p95_response_time=p95_response_time,
                p99_response_time=p99_response_time,
                min_response_time=min_response_time,
                max_response_time=max_response_time,
                error_rate=failed_ops / len(all_results) if all_results else 0,
                resource_usage=resource_usage,
                batch_performance=self.active_tests[test_id]['batch_results'],
                performance_over_time=self.resource_snapshots.copy()
            )
            
            # Store result
            self.test_history.append(result)
            await self._save_test_result(result)
            
            logger.info(f"Load test completed: {config.name}")
            logger.info(f"  Operations/sec: {result.operations_per_second:.2f}")
            logger.info(f"  Average response time: {result.average_response_time:.2f}ms")
            logger.info(f"  Error rate: {result.error_rate:.2%}")
            
            return result
            
        finally:
            # Cleanup
            monitoring_task.cancel()
            if test_id in self.active_tests:
                del self.active_tests[test_id]
            self.resource_snapshots.clear()
    
    async def _execute_batch_size_test(self, 
                                      config: LoadTestConfiguration, 
                                      batch_size: int) -> List[Dict[str, Any]]:
        """Execute test for a specific batch size"""
        results = []
        
        # Calculate operations per batch size test
        ops_per_batch_test = config.operations_per_user * config.concurrent_users // len(config.batch_sizes)
        
        # Create operation data
        operations = []
        for i in range(ops_per_batch_test):
            op_type = random.choice(config.operation_types)
            priority = self._select_priority(config.priority_distribution)
            
            operations.append({
                'id': f"op_{batch_size}_{i}",
                'type': op_type.value,
                'data': self._generate_test_data(config.data_size_bytes),
                'priority': priority,
                'timestamp': time.time()
            })
        
        # Execute with controlled concurrency
        semaphore = asyncio.Semaphore(config.concurrent_users)
        
        async def execute_operation_batch(batch_ops):
            async with semaphore:
                batch_start = time.time()
                
                try:
                    # Simulate batch execution
                    await asyncio.sleep(random.uniform(0.1, 0.5))  # Simulate processing
                    
                    # Simulate failures based on configured failure rate
                    success = random.random() > config.failure_rate
                    
                    response_time = (time.time() - batch_start) * 1000  # Convert to ms
                    
                    return {
                        'success': success,
                        'response_time': response_time,
                        'batch_size': len(batch_ops),
                        'operation_type': batch_ops[0]['type'] if batch_ops else 'unknown'
                    }
                    
                except Exception as e:
                    return {
                        'success': False,
                        'response_time': (time.time() - batch_start) * 1000,
                        'batch_size': len(batch_ops),
                        'error': str(e)
                    }
        
        # Split operations into batches
        batches = [operations[i:i + batch_size] for i in range(0, len(operations), batch_size)]
        
        # Execute batches with ramp-up
        ramp_up_delay = config.ramp_up_seconds / len(batches) if batches else 0
        
        tasks = []
        for i, batch in enumerate(batches):
            if i > 0:
                await asyncio.sleep(ramp_up_delay)
            
            task = asyncio.create_task(execute_operation_batch(batch))
            tasks.append(task)
            
            # Add think time
            if config.think_time_seconds > 0:
                await asyncio.sleep(config.think_time_seconds)
        
        # Wait for all tasks to complete
        batch_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for result in batch_results:
            if isinstance(result, Exception):
                results.append({
                    'success': False,
                    'response_time': 0,
                    'batch_size': batch_size,
                    'error': str(result)
                })
            else:
                results.append(result)
        
        return results
    
    async def _monitor_performance(self, test_id: str, duration: int):
        """Monitor performance during test execution"""
        start_time = time.time()
        
        while time.time() - start_time < duration:
            try:
                # Get current performance metrics
                dashboard = self.coordinator.get_performance_dashboard()
                current_metrics = self.coordinator.resource_monitor.get_current_metrics()
                
                snapshot = {
                    'timestamp': time.time(),
                    'elapsed_time': time.time() - start_time,
                    'system_cpu': current_metrics['system']['cpu_percent'],
                    'system_memory': current_metrics['system']['memory_percent'],
                    'active_jobs': dashboard.get('coordinator_status', {}).get('active_jobs', 0),
                    'queued_jobs': dashboard.get('coordinator_status', {}).get('queued_jobs', 0),
                    'operations_per_second': dashboard.get('performance_metrics', {}).get('average_throughput', 0)
                }
                
                self.resource_snapshots.append(snapshot)
                
                # Sleep before next snapshot
                await asyncio.sleep(5)
                
            except Exception as e:
                logger.error(f"Performance monitoring error: {e}")
                await asyncio.sleep(5)
    
    def _select_priority(self, distribution: Dict[str, float]) -> str:
        """Select priority based on distribution"""
        rand = random.random()
        cumulative = 0
        
        for priority, weight in distribution.items():
            cumulative += weight
            if rand <= cumulative:
                return priority
        
        return "normal"  # Default fallback
    
    def _generate_test_data(self, size_bytes: int) -> Dict[str, Any]:
        """Generate test data of specified size"""
        # Generate random string data
        import string
        data_str = ''.join(random.choices(string.ascii_letters + string.digits, k=size_bytes // 2))
        
        return {
            'content': data_str,
            'metadata': {
                'created_at': time.time(),
                'test_data': True,
                'size_bytes': size_bytes
            },
            'payload': list(range(min(100, size_bytes // 10)))  # Additional data
        }
    
    async def _calculate_resource_usage(self) -> Dict[str, float]:
        """Calculate average resource usage from snapshots"""
        if not self.resource_snapshots:
            return {'cpu': 0, 'memory': 0}
        
        cpu_values = [s['system_cpu'] for s in self.resource_snapshots]
        memory_values = [s['system_memory'] for s in self.resource_snapshots]
        
        return {
            'average_cpu': statistics.mean(cpu_values),
            'peak_cpu': max(cpu_values),
            'average_memory': statistics.mean(memory_values),
            'peak_memory': max(memory_values)
        }
    
    async def run_benchmark_suite(self, scenarios: Optional[List[str]] = None) -> BenchmarkResult:
        """Run a comprehensive benchmark suite"""
        if scenarios is None:
            scenarios = list(self.predefined_scenarios.keys())
        
        logger.info(f"Running benchmark suite with {len(scenarios)} scenarios")
        
        results = []
        configurations = []
        
        for scenario_name in scenarios:
            if scenario_name not in self.predefined_scenarios:
                logger.warning(f"Unknown scenario: {scenario_name}")
                continue
            
            config = self.predefined_scenarios[scenario_name]
            configurations.append(config)
            
            logger.info(f"Running benchmark: {scenario_name}")
            result = await self.run_load_test(config)
            results.append(result)
            
            # Brief pause between tests
            await asyncio.sleep(30)
        
        # Analyze results and generate recommendations
        comparison_metrics = self._analyze_benchmark_results(results)
        recommendations = self._generate_recommendations(results, comparison_metrics)
        best_config = self._identify_best_configuration(results)
        
        benchmark_result = BenchmarkResult(
            test_configurations=configurations,
            results=results,
            comparison_metrics=comparison_metrics,
            recommendations=recommendations,
            best_configuration=best_config
        )
        
        # Save benchmark results
        await self._save_benchmark_result(benchmark_result)
        
        return benchmark_result
    
    def _analyze_benchmark_results(self, results: List[LoadTestResult]) -> Dict[str, Any]:
        """Analyze benchmark results for comparison"""
        if not results:
            return {}
        
        # Performance comparison metrics
        throughput_scores = [r.operations_per_second for r in results]
        response_time_scores = [r.average_response_time for r in results]
        error_rates = [r.error_rate for r in results]
        resource_efficiency = [r.resource_usage.get('average_cpu', 0) + r.resource_usage.get('average_memory', 0) for r in results]
        
        return {
            'throughput_analysis': {
                'best': max(throughput_scores),
                'worst': min(throughput_scores),
                'average': statistics.mean(throughput_scores),
                'improvement_potential': (max(throughput_scores) - min(throughput_scores)) / min(throughput_scores) * 100
            },
            'response_time_analysis': {
                'best': min(response_time_scores),
                'worst': max(response_time_scores),
                'average': statistics.mean(response_time_scores),
                'consistency': statistics.stdev(response_time_scores) if len(response_time_scores) > 1 else 0
            },
            'reliability_analysis': {
                'best_error_rate': min(error_rates),
                'worst_error_rate': max(error_rates),
                'average_error_rate': statistics.mean(error_rates)
            },
            'resource_efficiency': {
                'most_efficient': min(resource_efficiency),
                'least_efficient': max(resource_efficiency),
                'efficiency_range': max(resource_efficiency) - min(resource_efficiency)
            }
        }
    
    def _generate_recommendations(self, results: List[LoadTestResult], metrics: Dict[str, Any]) -> List[str]:
        """Generate optimization recommendations based on results"""
        recommendations = []
        
        # Throughput recommendations
        throughput_improvement = metrics.get('throughput_analysis', {}).get('improvement_potential', 0)
        if throughput_improvement > 50:
            recommendations.append(
                f"Significant throughput improvement potential: {throughput_improvement:.1f}%. "
                "Consider optimizing batch sizes and resource allocation."
            )
        
        # Response time recommendations
        response_consistency = metrics.get('response_time_analysis', {}).get('consistency', 0)
        if response_consistency > 100:  # High variance in response times
            recommendations.append(
                "High response time variance detected. Consider implementing adaptive batch sizing "
                "to maintain consistent performance under varying loads."
            )
        
        # Error rate recommendations
        avg_error_rate = metrics.get('reliability_analysis', {}).get('average_error_rate', 0)
        if avg_error_rate > 0.05:  # 5% error rate
            recommendations.append(
                f"Average error rate of {avg_error_rate:.1%} is above target. "
                "Implement circuit breaker patterns and retry mechanisms."
            )
        
        # Resource efficiency recommendations
        efficiency_range = metrics.get('resource_efficiency', {}).get('efficiency_range', 0)
        if efficiency_range > 50:
            recommendations.append(
                "Large resource efficiency variations detected. Consider implementing "
                "resource-aware scaling and load balancing strategies."
            )
        
        # Batch size specific recommendations
        best_performing_test = max(results, key=lambda r: r.operations_per_second)
        if hasattr(best_performing_test, 'batch_performance'):
            best_batch_sizes = [
                size for size, perf in best_performing_test.batch_performance.items()
                if perf.get('success_rate', 0) > 0.95
            ]
            if best_batch_sizes:
                recommendations.append(
                    f"Optimal batch sizes for this workload: {best_batch_sizes}. "
                    "Consider using adaptive batching to dynamically select optimal sizes."
                )
        
        return recommendations
    
    def _identify_best_configuration(self, results: List[LoadTestResult]) -> Optional[str]:
        """Identify the best performing configuration"""
        if not results:
            return None
        
        # Calculate composite score for each result
        best_result = None
        best_score = float('-inf')
        
        for result in results:
            # Weighted score: throughput (40%) + response time (30%) + reliability (20%) + efficiency (10%)
            throughput_score = result.operations_per_second / 100  # Normalize
            response_time_score = max(0, (1000 - result.average_response_time) / 1000)  # Lower is better
            reliability_score = 1 - result.error_rate  # Higher is better
            efficiency_score = max(0, (200 - result.resource_usage.get('average_cpu', 100) - 
                                     result.resource_usage.get('average_memory', 100)) / 200)
            
            composite_score = (
                0.4 * throughput_score +
                0.3 * response_time_score +
                0.2 * reliability_score +
                0.1 * efficiency_score
            )
            
            if composite_score > best_score:
                best_score = composite_score
                best_result = result
        
        return best_result.test_name if best_result else None
    
    async def _save_test_result(self, result: LoadTestResult):
        """Save test result to file"""
        try:
            filename = f"load_test_{result.test_name}_{int(result.start_time)}.json"
            filepath = self.results_dir / filename
            
            # Convert result to dict for JSON serialization
            result_dict = {
                'test_name': result.test_name,
                'start_time': result.start_time,
                'end_time': result.end_time,
                'duration': result.duration,
                'total_operations': result.total_operations,
                'successful_operations': result.successful_operations,
                'failed_operations': result.failed_operations,
                'operations_per_second': result.operations_per_second,
                'average_response_time': result.average_response_time,
                'median_response_time': result.median_response_time,
                'p95_response_time': result.p95_response_time,
                'p99_response_time': result.p99_response_time,
                'min_response_time': result.min_response_time,
                'max_response_time': result.max_response_time,
                'error_rate': result.error_rate,
                'resource_usage': result.resource_usage,
                'batch_performance': result.batch_performance,
                'performance_over_time': result.performance_over_time
            }
            
            with open(filepath, 'w') as f:
                json.dump(result_dict, f, indent=2)
            
            logger.info(f"Test result saved to {filepath}")
            
        except Exception as e:
            logger.error(f"Failed to save test result: {e}")
    
    async def _save_benchmark_result(self, benchmark: BenchmarkResult):
        """Save benchmark result to file"""
        try:
            filename = f"benchmark_suite_{int(time.time())}.json"
            filepath = self.results_dir / filename
            
            # Convert benchmark to dict
            benchmark_dict = {
                'test_configurations': [
                    {
                        'name': config.name,
                        'description': config.description,
                        'duration_seconds': config.duration_seconds,
                        'concurrent_users': config.concurrent_users,
                        'operations_per_user': config.operations_per_user,
                        'batch_sizes': config.batch_sizes
                    }
                    for config in benchmark.test_configurations
                ],
                'results_summary': [
                    {
                        'test_name': result.test_name,
                        'operations_per_second': result.operations_per_second,
                        'average_response_time': result.average_response_time,
                        'error_rate': result.error_rate,
                        'resource_usage': result.resource_usage
                    }
                    for result in benchmark.results
                ],
                'comparison_metrics': benchmark.comparison_metrics,
                'recommendations': benchmark.recommendations,
                'best_configuration': benchmark.best_configuration
            }
            
            with open(filepath, 'w') as f:
                json.dump(benchmark_dict, f, indent=2)
            
            logger.info(f"Benchmark result saved to {filepath}")
            
        except Exception as e:
            logger.error(f"Failed to save benchmark result: {e}")
    
    def generate_performance_report(self, results: List[LoadTestResult]) -> str:
        """Generate a comprehensive performance report"""
        if not results:
            return "No test results available for report generation."
        
        report_lines = []
        report_lines.append("# Load Testing Performance Report")
        report_lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        
        # Executive Summary
        report_lines.append("## Executive Summary")
        total_ops = sum(r.total_operations for r in results)
        avg_throughput = statistics.mean([r.operations_per_second for r in results])
        avg_response_time = statistics.mean([r.average_response_time for r in results])
        avg_error_rate = statistics.mean([r.error_rate for r in results])
        
        report_lines.append(f"- Total operations tested: {total_ops:,}")
        report_lines.append(f"- Average throughput: {avg_throughput:.2f} ops/sec")
        report_lines.append(f"- Average response time: {avg_response_time:.2f} ms")
        report_lines.append(f"- Average error rate: {avg_error_rate:.2%}")
        report_lines.append("")
        
        # Individual Test Results
        report_lines.append("## Test Results")
        for result in results:
            report_lines.append(f"### {result.test_name}")
            report_lines.append(f"- Duration: {result.duration:.1f} seconds")
            report_lines.append(f"- Operations/sec: {result.operations_per_second:.2f}")
            report_lines.append(f"- Average response time: {result.average_response_time:.2f} ms")
            report_lines.append(f"- P95 response time: {result.p95_response_time:.2f} ms")
            report_lines.append(f"- Error rate: {result.error_rate:.2%}")
            report_lines.append(f"- Resource usage: CPU {result.resource_usage.get('average_cpu', 0):.1f}%, Memory {result.resource_usage.get('average_memory', 0):.1f}%")
            report_lines.append("")
        
        # Performance Comparison
        if len(results) > 1:
            best_throughput = max(results, key=lambda r: r.operations_per_second)
            best_response_time = min(results, key=lambda r: r.average_response_time)
            best_reliability = min(results, key=lambda r: r.error_rate)
            
            report_lines.append("## Performance Leaders")
            report_lines.append(f"- Best throughput: {best_throughput.test_name} ({best_throughput.operations_per_second:.2f} ops/sec)")
            report_lines.append(f"- Best response time: {best_response_time.test_name} ({best_response_time.average_response_time:.2f} ms)")
            report_lines.append(f"- Best reliability: {best_reliability.test_name} ({best_reliability.error_rate:.2%} error rate)")
            report_lines.append("")
        
        return "\n".join(report_lines)
    
    def get_test_history(self) -> List[LoadTestResult]:
        """Get history of all load tests"""
        return self.test_history.copy()
    
    def get_predefined_scenarios(self) -> Dict[str, LoadTestConfiguration]:
        """Get all predefined test scenarios"""
        return self.predefined_scenarios.copy()

# Factory function
def create_load_testing_framework(coordinator: BatchCoordinator, 
                                 results_dir: str = "load_test_results/") -> LoadTestingFramework:
    """Create and configure a load testing framework"""
    return LoadTestingFramework(coordinator, results_dir)

# CLI interface for running tests
async def main():
    """Main function for running load tests from command line"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Load Testing Framework")
    parser.add_argument('--scenario', choices=list(LoadTestingFramework._create_predefined_scenarios(None).keys()),
                       help="Predefined scenario to run")
    parser.add_argument('--benchmark', action='store_true', help="Run full benchmark suite")
    parser.add_argument('--results-dir', default="load_test_results/", help="Results directory")
    
    args = parser.parse_args()
    
    # Create coordinator and framework (would need proper initialization in real usage)
    from .batch_coordinator import create_batch_coordinator
    coordinator = create_batch_coordinator()
    framework = create_load_testing_framework(coordinator, args.results_dir)
    
    try:
        coordinator.start()
        
        if args.benchmark:
            print("Running full benchmark suite...")
            benchmark_result = await framework.run_benchmark_suite()
            print(f"Benchmark completed. Best configuration: {benchmark_result.best_configuration}")
            
        elif args.scenario:
            print(f"Running scenario: {args.scenario}")
            config = framework.predefined_scenarios[args.scenario]
            result = await framework.run_load_test(config)
            print(f"Test completed: {result.operations_per_second:.2f} ops/sec")
            
        else:
            print("No test specified. Use --scenario or --benchmark")
    
    finally:
        coordinator.stop()

if __name__ == "__main__":
    asyncio.run(main())