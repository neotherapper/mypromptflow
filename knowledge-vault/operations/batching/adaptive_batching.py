#!/usr/bin/env python3
"""
Adaptive Batching Algorithm for AI Notion MCP Integration
Implements dynamic batch sizing based on performance metrics and system conditions.
"""

import asyncio
import time
import logging
from typing import Dict, List, Tuple, Optional, Any, Callable
from dataclasses import dataclass, field
from enum import Enum
import statistics
import yaml
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OperationType(Enum):
    """Types of operations for different batching strategies"""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    UPDATE = "update"
    BULK_CREATE = "bulk_create"
    QUERY = "query"

class BatchStrategy(Enum):
    """Different batching strategies"""
    CONSERVATIVE = "conservative"  # Small batches, high reliability
    AGGRESSIVE = "aggressive"      # Large batches, high throughput
    ADAPTIVE = "adaptive"          # Dynamic based on performance
    BALANCED = "balanced"          # Middle ground approach

@dataclass
class PerformanceMetrics:
    """Performance metrics for batch operations"""
    success_rate: float = 1.0
    average_response_time: float = 0.0
    throughput: float = 0.0  # operations per second
    error_rate: float = 0.0
    rate_limit_hits: int = 0
    cpu_usage: float = 0.0
    memory_usage: float = 0.0
    network_latency: float = 0.0
    timestamp: float = field(default_factory=time.time)

@dataclass
class BatchConfiguration:
    """Configuration for batch operations"""
    min_batch_size: int = 10
    max_batch_size: int = 500
    target_response_time: float = 500.0  # milliseconds
    max_error_rate: float = 0.05  # 5%
    rate_limit_threshold: int = 3
    cpu_threshold: float = 80.0  # percentage
    memory_threshold: float = 85.0  # percentage
    adaptation_sensitivity: float = 0.2  # How quickly to adapt (0-1)

class AdaptiveBatchingEngine:
    """
    Core adaptive batching engine that dynamically adjusts batch sizes
    based on real-time performance metrics and system conditions.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the adaptive batching engine"""
        self.config = self._load_config(config_path)
        self.performance_history: Dict[OperationType, List[PerformanceMetrics]] = {
            op_type: [] for op_type in OperationType
        }
        self.current_batch_sizes: Dict[OperationType, int] = {
            op_type: self.config.min_batch_size for op_type in OperationType
        }
        self.strategy_performance: Dict[BatchStrategy, Dict[OperationType, float]] = {
            strategy: {op_type: 0.0 for op_type in OperationType} 
            for strategy in BatchStrategy
        }
        self.active_strategies: Dict[OperationType, BatchStrategy] = {
            op_type: BatchStrategy.ADAPTIVE for op_type in OperationType
        }
        self.circuit_breaker_active: Dict[OperationType, bool] = {
            op_type: False for op_type in OperationType
        }
        self.last_adaptation_time: Dict[OperationType, float] = {
            op_type: time.time() for op_type in OperationType
        }
        
    def _load_config(self, config_path: Optional[str]) -> BatchConfiguration:
        """Load configuration from file or use defaults"""
        if config_path and Path(config_path).exists():
            try:
                with open(config_path, 'r') as f:
                    config_data = yaml.safe_load(f)
                return BatchConfiguration(**config_data.get('batching', {}))
            except Exception as e:
                logger.warning(f"Failed to load config from {config_path}: {e}")
        
        return BatchConfiguration()
    
    def calculate_optimal_batch_size(
        self, 
        operation_type: OperationType,
        current_metrics: PerformanceMetrics,
        pending_operations: int = 100
    ) -> int:
        """
        Calculate optimal batch size based on current performance metrics
        and system conditions.
        """
        # Circuit breaker check
        if self.circuit_breaker_active[operation_type]:
            return self._get_circuit_breaker_batch_size(operation_type)
        
        # Get current batch size
        current_size = self.current_batch_sizes[operation_type]
        
        # Calculate performance score
        performance_score = self._calculate_performance_score(
            operation_type, current_metrics
        )
        
        # Apply strategy-specific logic
        strategy = self.active_strategies[operation_type]
        new_size = self._apply_strategy(
            strategy, current_size, performance_score, current_metrics, pending_operations
        )
        
        # Apply constraints and safety checks
        new_size = self._apply_constraints(new_size, current_metrics)
        
        # Update batch size if significant change
        if abs(new_size - current_size) > max(1, current_size * 0.1):
            logger.info(
                f"Adapting batch size for {operation_type.value}: "
                f"{current_size} -> {new_size} (score: {performance_score:.2f})"
            )
            self.current_batch_sizes[operation_type] = new_size
            self.last_adaptation_time[operation_type] = time.time()
        
        return new_size
    
    def _calculate_performance_score(
        self, 
        operation_type: OperationType, 
        metrics: PerformanceMetrics
    ) -> float:
        """Calculate composite performance score (0-1, higher is better)"""
        # Weight factors for different metrics
        weights = {
            'success_rate': 0.30,
            'response_time': 0.25,
            'throughput': 0.20,
            'resource_usage': 0.15,
            'rate_limits': 0.10
        }
        
        # Success rate score (higher is better)
        success_score = metrics.success_rate
        
        # Response time score (lower is better, normalized)
        response_score = max(0, 1 - (metrics.average_response_time / self.config.target_response_time))
        
        # Throughput score (higher is better, normalized against historical max)
        historical_throughput = self._get_historical_throughput(operation_type)
        throughput_score = min(1.0, metrics.throughput / max(1, historical_throughput))
        
        # Resource usage score (lower is better)
        cpu_score = max(0, 1 - (metrics.cpu_usage / 100))
        memory_score = max(0, 1 - (metrics.memory_usage / 100))
        resource_score = (cpu_score + memory_score) / 2
        
        # Rate limit score (fewer hits is better)
        rate_limit_score = max(0, 1 - (metrics.rate_limit_hits / self.config.rate_limit_threshold))
        
        # Calculate weighted score
        total_score = (
            weights['success_rate'] * success_score +
            weights['response_time'] * response_score +
            weights['throughput'] * throughput_score +
            weights['resource_usage'] * resource_score +
            weights['rate_limits'] * rate_limit_score
        )
        
        return total_score
    
    def _apply_strategy(
        self,
        strategy: BatchStrategy,
        current_size: int,
        performance_score: float,
        metrics: PerformanceMetrics,
        pending_operations: int
    ) -> int:
        """Apply specific batching strategy"""
        if strategy == BatchStrategy.CONSERVATIVE:
            return self._conservative_strategy(current_size, performance_score, metrics)
        elif strategy == BatchStrategy.AGGRESSIVE:
            return self._aggressive_strategy(current_size, performance_score, metrics, pending_operations)
        elif strategy == BatchStrategy.ADAPTIVE:
            return self._adaptive_strategy(current_size, performance_score, metrics)
        elif strategy == BatchStrategy.BALANCED:
            return self._balanced_strategy(current_size, performance_score, metrics)
        else:
            return current_size
    
    def _conservative_strategy(self, current_size: int, score: float, metrics: PerformanceMetrics) -> int:
        """Conservative strategy: prioritize reliability over throughput"""
        if score > 0.9 and metrics.error_rate < 0.01:
            return min(current_size + 5, self.config.max_batch_size // 2)
        elif score < 0.7 or metrics.error_rate > 0.03:
            return max(current_size - 10, self.config.min_batch_size)
        return current_size
    
    def _aggressive_strategy(self, current_size: int, score: float, metrics: PerformanceMetrics, pending: int) -> int:
        """Aggressive strategy: maximize throughput"""
        if score > 0.8 and pending > current_size * 2:
            return min(current_size + 20, self.config.max_batch_size)
        elif score < 0.6:
            return max(current_size - 15, self.config.min_batch_size)
        return current_size
    
    def _adaptive_strategy(self, current_size: int, score: float, metrics: PerformanceMetrics) -> int:
        """Adaptive strategy: dynamic adjustment based on performance"""
        # Calculate adjustment based on performance trend
        if score > 0.85:
            # High performance, try to increase
            increase = int(current_size * 0.2)
            return min(current_size + increase, self.config.max_batch_size)
        elif score < 0.6:
            # Poor performance, decrease significantly
            decrease = int(current_size * 0.3)
            return max(current_size - decrease, self.config.min_batch_size)
        elif score < 0.75:
            # Moderate performance, slight decrease
            decrease = int(current_size * 0.1)
            return max(current_size - decrease, self.config.min_batch_size)
        
        return current_size
    
    def _balanced_strategy(self, current_size: int, score: float, metrics: PerformanceMetrics) -> int:
        """Balanced strategy: middle ground between conservative and aggressive"""
        if score > 0.8 and metrics.average_response_time < self.config.target_response_time * 0.8:
            return min(current_size + 10, self.config.max_batch_size * 0.75)
        elif score < 0.65:
            return max(current_size - 8, self.config.min_batch_size)
        return current_size
    
    def _apply_constraints(self, new_size: int, metrics: PerformanceMetrics) -> int:
        """Apply safety constraints and system limits"""
        # Ensure within min/max bounds
        new_size = max(self.config.min_batch_size, min(new_size, self.config.max_batch_size))
        
        # Resource-based constraints
        if metrics.cpu_usage > self.config.cpu_threshold:
            new_size = min(new_size, new_size // 2)
        
        if metrics.memory_usage > self.config.memory_threshold:
            new_size = min(new_size, new_size // 2)
        
        # Rate limiting constraints
        if metrics.rate_limit_hits > 0:
            new_size = min(new_size, new_size * 3 // 4)
        
        return new_size
    
    def _get_circuit_breaker_batch_size(self, operation_type: OperationType) -> int:
        """Get minimal batch size when circuit breaker is active"""
        return self.config.min_batch_size
    
    def _get_historical_throughput(self, operation_type: OperationType) -> float:
        """Get maximum historical throughput for normalization"""
        history = self.performance_history[operation_type]
        if not history:
            return 1.0
        return max(m.throughput for m in history[-50:])  # Last 50 measurements
    
    def update_performance_metrics(
        self, 
        operation_type: OperationType, 
        metrics: PerformanceMetrics
    ):
        """Update performance history with new metrics"""
        # Add to history
        self.performance_history[operation_type].append(metrics)
        
        # Keep only recent history (last 1000 measurements)
        if len(self.performance_history[operation_type]) > 1000:
            self.performance_history[operation_type] = self.performance_history[operation_type][-1000:]
        
        # Update circuit breaker status
        self._update_circuit_breaker(operation_type, metrics)
        
        # Evaluate strategy performance
        self._update_strategy_performance(operation_type, metrics)
    
    def _update_circuit_breaker(self, operation_type: OperationType, metrics: PerformanceMetrics):
        """Update circuit breaker status based on metrics"""
        # Check for circuit breaker activation conditions
        should_activate = (
            metrics.error_rate > self.config.max_error_rate * 2 or
            metrics.rate_limit_hits > self.config.rate_limit_threshold or
            metrics.cpu_usage > 95 or
            metrics.memory_usage > 95
        )
        
        # Check for circuit breaker deactivation conditions
        should_deactivate = (
            metrics.error_rate < self.config.max_error_rate * 0.5 and
            metrics.rate_limit_hits == 0 and
            metrics.cpu_usage < self.config.cpu_threshold and
            metrics.memory_usage < self.config.memory_threshold
        )
        
        if should_activate and not self.circuit_breaker_active[operation_type]:
            logger.warning(f"Activating circuit breaker for {operation_type.value}")
            self.circuit_breaker_active[operation_type] = True
        elif should_deactivate and self.circuit_breaker_active[operation_type]:
            logger.info(f"Deactivating circuit breaker for {operation_type.value}")
            self.circuit_breaker_active[operation_type] = False
    
    def _update_strategy_performance(self, operation_type: OperationType, metrics: PerformanceMetrics):
        """Update strategy performance tracking"""
        current_strategy = self.active_strategies[operation_type]
        performance_score = self._calculate_performance_score(operation_type, metrics)
        
        # Update strategy performance with exponential moving average
        alpha = 0.1  # Learning rate
        current_score = self.strategy_performance[current_strategy][operation_type]
        self.strategy_performance[current_strategy][operation_type] = (
            alpha * performance_score + (1 - alpha) * current_score
        )
    
    def get_batch_recommendation(
        self,
        operation_type: OperationType,
        current_metrics: PerformanceMetrics,
        pending_operations: int = 100,
        priority: str = "normal"
    ) -> Dict[str, Any]:
        """
        Get comprehensive batch recommendation with reasoning
        """
        optimal_size = self.calculate_optimal_batch_size(
            operation_type, current_metrics, pending_operations
        )
        
        # Calculate confidence score
        confidence = self._calculate_confidence_score(operation_type, current_metrics)
        
        # Determine strategy recommendation
        strategy_recommendation = self._recommend_strategy(operation_type, current_metrics)
        
        return {
            'batch_size': optimal_size,
            'confidence': confidence,
            'strategy': strategy_recommendation,
            'reasoning': self._generate_reasoning(operation_type, current_metrics, optimal_size),
            'circuit_breaker_active': self.circuit_breaker_active[operation_type],
            'performance_score': self._calculate_performance_score(operation_type, current_metrics),
            'estimated_completion_time': self._estimate_completion_time(
                optimal_size, pending_operations, current_metrics
            ),
            'resource_impact': self._estimate_resource_impact(optimal_size, current_metrics)
        }
    
    def _calculate_confidence_score(self, operation_type: OperationType, metrics: PerformanceMetrics) -> float:
        """Calculate confidence in the batch size recommendation"""
        history = self.performance_history[operation_type]
        if len(history) < 10:
            return 0.5  # Low confidence with limited data
        
        # Base confidence on recent performance consistency
        recent_scores = [
            self._calculate_performance_score(operation_type, m) 
            for m in history[-10:]
        ]
        
        variance = statistics.variance(recent_scores) if len(recent_scores) > 1 else 0
        consistency_score = max(0, 1 - variance)
        
        return min(1.0, consistency_score + 0.2)
    
    def _recommend_strategy(self, operation_type: OperationType, metrics: PerformanceMetrics) -> BatchStrategy:
        """Recommend optimal strategy based on current conditions"""
        # Analyze recent performance of different strategies
        strategy_scores = {}
        for strategy in BatchStrategy:
            score = self.strategy_performance[strategy][operation_type]
            strategy_scores[strategy] = score
        
        # Factor in current system conditions
        if metrics.cpu_usage > 80 or metrics.memory_usage > 80:
            return BatchStrategy.CONSERVATIVE
        elif metrics.rate_limit_hits > 0:
            return BatchStrategy.CONSERVATIVE
        elif metrics.success_rate > 0.95 and metrics.average_response_time < self.config.target_response_time:
            return BatchStrategy.AGGRESSIVE
        else:
            # Return best performing strategy
            return max(strategy_scores, key=strategy_scores.get)
    
    def _generate_reasoning(
        self, 
        operation_type: OperationType, 
        metrics: PerformanceMetrics, 
        batch_size: int
    ) -> str:
        """Generate human-readable reasoning for the recommendation"""
        reasons = []
        
        if self.circuit_breaker_active[operation_type]:
            reasons.append("Circuit breaker active - using minimal batch size")
        
        if metrics.error_rate > self.config.max_error_rate:
            reasons.append(f"High error rate ({metrics.error_rate:.1%}) - reducing batch size")
        
        if metrics.average_response_time > self.config.target_response_time:
            reasons.append(f"Slow response time ({metrics.average_response_time:.0f}ms) - optimizing batch size")
        
        if metrics.rate_limit_hits > 0:
            reasons.append("Rate limiting detected - using conservative batching")
        
        if metrics.cpu_usage > self.config.cpu_threshold:
            reasons.append(f"High CPU usage ({metrics.cpu_usage:.1f}%) - reducing batch size")
        
        if not reasons:
            performance_score = self._calculate_performance_score(operation_type, metrics)
            if performance_score > 0.8:
                reasons.append("Excellent performance - optimizing for throughput")
            else:
                reasons.append("Balancing performance and reliability")
        
        return " | ".join(reasons)
    
    def _estimate_completion_time(
        self, 
        batch_size: int, 
        pending_operations: int, 
        metrics: PerformanceMetrics
    ) -> float:
        """Estimate completion time for pending operations"""
        if metrics.throughput <= 0:
            return float('inf')
        
        total_batches = (pending_operations + batch_size - 1) // batch_size
        time_per_batch = batch_size / metrics.throughput
        
        return total_batches * time_per_batch
    
    def _estimate_resource_impact(self, batch_size: int, metrics: PerformanceMetrics) -> Dict[str, str]:
        """Estimate resource impact of the recommended batch size"""
        current_size = self.current_batch_sizes.get(OperationType.READ, self.config.min_batch_size)
        size_ratio = batch_size / max(1, current_size)
        
        cpu_impact = "low" if size_ratio < 1.2 else "medium" if size_ratio < 2.0 else "high"
        memory_impact = "low" if size_ratio < 1.5 else "medium" if size_ratio < 2.5 else "high"
        
        return {
            'cpu': cpu_impact,
            'memory': memory_impact,
            'network': "medium" if batch_size > 100 else "low"
        }
    
    async def optimize_batch_sequence(
        self,
        operations: List[Dict[str, Any]],
        operation_type: OperationType
    ) -> List[List[Dict[str, Any]]]:
        """
        Optimize the sequence of operations into batches with intelligent grouping
        """
        if not operations:
            return []
        
        # Get current metrics (would be provided by resource monitor)
        current_metrics = PerformanceMetrics()  # Placeholder
        
        # Get optimal batch size
        batch_size = self.calculate_optimal_batch_size(operation_type, current_metrics, len(operations))
        
        # Group operations with intelligent batching
        batches = []
        current_batch = []
        
        for op in operations:
            current_batch.append(op)
            
            # Check if batch is ready
            if len(current_batch) >= batch_size:
                batches.append(current_batch)
                current_batch = []
        
        # Add remaining operations
        if current_batch:
            batches.append(current_batch)
        
        return batches
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get comprehensive performance summary"""
        summary = {}
        
        for op_type in OperationType:
            history = self.performance_history[op_type]
            if not history:
                continue
            
            recent_metrics = history[-10:] if len(history) >= 10 else history
            
            summary[op_type.value] = {
                'current_batch_size': self.current_batch_sizes[op_type],
                'average_response_time': statistics.mean(m.average_response_time for m in recent_metrics),
                'average_throughput': statistics.mean(m.throughput for m in recent_metrics),
                'success_rate': statistics.mean(m.success_rate for m in recent_metrics),
                'circuit_breaker_active': self.circuit_breaker_active[op_type],
                'active_strategy': self.active_strategies[op_type].value,
                'total_measurements': len(history)
            }
        
        return summary

# Factory function for easy instantiation
def create_adaptive_batching_engine(config_path: Optional[str] = None) -> AdaptiveBatchingEngine:
    """Create and configure an adaptive batching engine"""
    return AdaptiveBatchingEngine(config_path)

if __name__ == "__main__":
    # Example usage and testing
    engine = create_adaptive_batching_engine()
    
    # Simulate some performance metrics
    test_metrics = PerformanceMetrics(
        success_rate=0.95,
        average_response_time=300.0,
        throughput=50.0,
        error_rate=0.02,
        cpu_usage=60.0,
        memory_usage=70.0
    )
    
    # Get batch recommendation
    recommendation = engine.get_batch_recommendation(
        OperationType.READ, test_metrics, pending_operations=500
    )
    
    print("Batch Recommendation:")
    for key, value in recommendation.items():
        print(f"  {key}: {value}")