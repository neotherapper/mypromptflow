#!/usr/bin/env python3
"""
Performance Optimizer for Intelligent Batching System
Implements machine learning models and optimization algorithms for predictive batch sizing.
"""

import asyncio
import time
import logging
import pickle
from typing import Dict, List, Tuple, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib
from pathlib import Path
import json
import yaml

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PerformancePrediction:
    """Performance prediction results"""
    predicted_batch_size: int
    predicted_throughput: float
    predicted_response_time: float
    predicted_resource_usage: Dict[str, float]
    confidence_score: float
    model_accuracy: float
    timestamp: float = field(default_factory=time.time)

@dataclass
class OptimizationTarget:
    """Optimization targets and constraints"""
    target_throughput: Optional[float] = None
    max_response_time: Optional[float] = None
    max_cpu_usage: Optional[float] = None
    max_memory_usage: Optional[float] = None
    min_success_rate: float = 0.95
    priority: str = "balanced"  # balanced, throughput, latency, resource

class PerformanceOptimizer:
    """
    Advanced performance optimizer using machine learning for predictive
    batch sizing and performance optimization.
    """
    
    def __init__(self, model_save_path: str = "models/"):
        """Initialize the performance optimizer"""
        self.model_save_path = Path(model_save_path)
        self.model_save_path.mkdir(parents=True, exist_ok=True)
        
        # ML Models for different predictions
        self.models = {
            'batch_size': RandomForestRegressor(n_estimators=100, random_state=42),
            'throughput': GradientBoostingRegressor(n_estimators=100, random_state=42),
            'response_time': RandomForestRegressor(n_estimators=100, random_state=42),
            'cpu_usage': LinearRegression(),
            'memory_usage': LinearRegression()
        }
        
        # Feature scalers
        self.scalers = {
            'features': StandardScaler(),
            'targets': StandardScaler()
        }
        
        # Training data storage
        self.training_data: List[Dict[str, Any]] = []
        self.feature_columns = [
            'current_batch_size', 'pending_operations', 'cpu_usage', 'memory_usage',
            'network_latency', 'error_rate', 'rate_limit_hits', 'time_of_day',
            'day_of_week', 'operation_type_encoded', 'historical_avg_throughput',
            'historical_avg_response_time', 'system_load'
        ]
        
        # Model performance tracking
        self.model_performance: Dict[str, Dict[str, float]] = {}
        self.prediction_history: List[PerformancePrediction] = []
        
        # A/B testing framework
        self.ab_tests: Dict[str, Dict[str, Any]] = {}
        self.control_group_performance: List[float] = []
        self.test_group_performance: List[float] = []
        
        # Load existing models if available
        self._load_models()
    
    def add_training_data(self, 
                         features: Dict[str, Any], 
                         performance_results: Dict[str, float]):
        """Add new training data point"""
        data_point = {
            'timestamp': time.time(),
            'features': features.copy(),
            'results': performance_results.copy()
        }
        
        self.training_data.append(data_point)
        
        # Keep only recent data (last 10000 points)
        if len(self.training_data) > 10000:
            self.training_data = self.training_data[-10000:]
        
        logger.debug(f"Added training data point. Total points: {len(self.training_data)}")
    
    def prepare_features(self, raw_features: Dict[str, Any]) -> np.ndarray:
        """Prepare features for model input"""
        # Extract and encode features
        features = []
        
        # Basic metrics
        features.append(raw_features.get('current_batch_size', 50))
        features.append(raw_features.get('pending_operations', 100))
        features.append(raw_features.get('cpu_usage', 50.0))
        features.append(raw_features.get('memory_usage', 60.0))
        features.append(raw_features.get('network_latency', 10.0))
        features.append(raw_features.get('error_rate', 0.01))
        features.append(raw_features.get('rate_limit_hits', 0))
        
        # Time-based features
        current_time = datetime.now()
        features.append(current_time.hour)  # time_of_day
        features.append(current_time.weekday())  # day_of_week
        
        # Operation type encoding (simple numeric encoding)
        operation_type = raw_features.get('operation_type', 'read')
        operation_encoding = {
            'read': 1, 'write': 2, 'delete': 3, 
            'update': 4, 'bulk_create': 5, 'query': 6
        }
        features.append(operation_encoding.get(operation_type, 1))
        
        # Historical metrics
        features.append(raw_features.get('historical_avg_throughput', 50.0))
        features.append(raw_features.get('historical_avg_response_time', 200.0))
        features.append(raw_features.get('system_load', 1.0))
        
        return np.array(features).reshape(1, -1)
    
    def train_models(self, min_data_points: int = 100) -> Dict[str, float]:
        """Train all ML models with available data"""
        if len(self.training_data) < min_data_points:
            logger.warning(f"Insufficient training data: {len(self.training_data)} < {min_data_points}")
            return {}
        
        logger.info(f"Training models with {len(self.training_data)} data points")
        
        # Prepare training data
        X_data = []
        y_data = {target: [] for target in self.models.keys()}
        
        for data_point in self.training_data:
            features = self.prepare_features(data_point['features'])
            X_data.append(features.flatten())
            
            results = data_point['results']
            y_data['batch_size'].append(results.get('optimal_batch_size', 50))
            y_data['throughput'].append(results.get('throughput', 50.0))
            y_data['response_time'].append(results.get('response_time', 200.0))
            y_data['cpu_usage'].append(results.get('cpu_usage', 50.0))
            y_data['memory_usage'].append(results.get('memory_usage', 60.0))
        
        X_data = np.array(X_data)
        
        # Train each model
        model_scores = {}
        
        for target, model in self.models.items():
            try:
                y = np.array(y_data[target])
                
                # Split data
                X_train, X_test, y_train, y_test = train_test_split(
                    X_data, y, test_size=0.2, random_state=42
                )
                
                # Scale features
                X_train_scaled = self.scalers['features'].fit_transform(X_train)
                X_test_scaled = self.scalers['features'].transform(X_test)
                
                # Train model
                model.fit(X_train_scaled, y_train)
                
                # Evaluate model
                y_pred = model.predict(X_test_scaled)
                r2 = r2_score(y_test, y_pred)
                mse = mean_squared_error(y_test, y_pred)
                
                model_scores[target] = {
                    'r2_score': r2,
                    'mse': mse,
                    'accuracy': max(0, r2)  # Use R² as accuracy metric
                }
                
                logger.info(f"Model {target}: R² = {r2:.3f}, MSE = {mse:.3f}")
                
            except Exception as e:
                logger.error(f"Failed to train model {target}: {e}")
                model_scores[target] = {'r2_score': 0, 'mse': float('inf'), 'accuracy': 0}
        
        # Update model performance tracking
        self.model_performance = model_scores
        
        # Save trained models
        self._save_models()
        
        return {target: scores['accuracy'] for target, scores in model_scores.items()}
    
    def predict_optimal_batch_size(self, 
                                  features: Dict[str, Any],
                                  optimization_target: OptimizationTarget) -> PerformancePrediction:
        """Predict optimal batch size using trained ML models"""
        try:
            # Prepare features
            X = self.prepare_features(features)
            X_scaled = self.scalers['features'].transform(X)
            
            # Make predictions
            predictions = {}
            confidences = {}
            
            for target, model in self.models.items():
                try:
                    pred = model.predict(X_scaled)[0]
                    predictions[target] = max(0, pred)  # Ensure non-negative
                    
                    # Calculate confidence based on model accuracy
                    confidence = self.model_performance.get(target, {}).get('accuracy', 0.5)
                    confidences[target] = confidence
                    
                except Exception as e:
                    logger.warning(f"Prediction failed for {target}: {e}")
                    predictions[target] = 0
                    confidences[target] = 0
            
            # Apply optimization constraints
            optimized_batch_size = self._apply_optimization_constraints(
                predictions, optimization_target, features
            )
            
            # Calculate overall confidence
            overall_confidence = np.mean(list(confidences.values()))
            
            # Create prediction result
            prediction = PerformancePrediction(
                predicted_batch_size=int(optimized_batch_size),
                predicted_throughput=predictions.get('throughput', 50.0),
                predicted_response_time=predictions.get('response_time', 200.0),
                predicted_resource_usage={
                    'cpu': predictions.get('cpu_usage', 50.0),
                    'memory': predictions.get('memory_usage', 60.0)
                },
                confidence_score=overall_confidence,
                model_accuracy=np.mean([s.get('accuracy', 0) for s in self.model_performance.values()])
            )
            
            # Store prediction for validation
            self.prediction_history.append(prediction)
            if len(self.prediction_history) > 1000:
                self.prediction_history = self.prediction_history[-1000:]
            
            return prediction
            
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            # Return safe default prediction
            return PerformancePrediction(
                predicted_batch_size=50,
                predicted_throughput=50.0,
                predicted_response_time=200.0,
                predicted_resource_usage={'cpu': 50.0, 'memory': 60.0},
                confidence_score=0.1,
                model_accuracy=0.0
            )
    
    def _apply_optimization_constraints(self,
                                      predictions: Dict[str, float],
                                      target: OptimizationTarget,
                                      features: Dict[str, Any]) -> float:
        """Apply optimization constraints to batch size prediction"""
        base_batch_size = predictions.get('batch_size', 50)
        
        # Apply priority-based optimization
        if target.priority == "throughput":
            # Optimize for maximum throughput
            if predictions.get('throughput', 0) > 0:
                # Increase batch size if throughput allows
                multiplier = min(2.0, (target.target_throughput or 100) / predictions['throughput'])
                base_batch_size *= multiplier
        
        elif target.priority == "latency":
            # Optimize for minimum response time
            if predictions.get('response_time', 0) > target.max_response_time:
                # Reduce batch size to improve response time
                base_batch_size *= 0.7
        
        elif target.priority == "resource":
            # Optimize for resource efficiency
            if predictions.get('cpu_usage', 0) > (target.max_cpu_usage or 80):
                base_batch_size *= 0.8
            if predictions.get('memory_usage', 0) > (target.max_memory_usage or 85):
                base_batch_size *= 0.8
        
        # Apply hard constraints
        current_cpu = features.get('cpu_usage', 50)
        current_memory = features.get('memory_usage', 60)
        
        if current_cpu > 80:
            base_batch_size = min(base_batch_size, base_batch_size * 0.7)
        if current_memory > 85:
            base_batch_size = min(base_batch_size, base_batch_size * 0.7)
        
        # Ensure reasonable bounds
        base_batch_size = max(10, min(500, base_batch_size))
        
        return base_batch_size
    
    def start_ab_test(self, 
                     test_name: str,
                     control_strategy: str,
                     test_strategy: str,
                     split_ratio: float = 0.5,
                     duration_hours: int = 24) -> str:
        """Start A/B test for batch sizing strategies"""
        test_id = f"{test_name}_{int(time.time())}"
        
        self.ab_tests[test_id] = {
            'name': test_name,
            'control_strategy': control_strategy,
            'test_strategy': test_strategy,
            'split_ratio': split_ratio,
            'start_time': time.time(),
            'duration_hours': duration_hours,
            'control_results': [],
            'test_results': [],
            'status': 'active'
        }
        
        logger.info(f"Started A/B test {test_id}: {control_strategy} vs {test_strategy}")
        return test_id
    
    def record_ab_test_result(self, 
                             test_id: str,
                             is_test_group: bool,
                             performance_score: float):
        """Record A/B test result"""
        if test_id not in self.ab_tests:
            logger.warning(f"Unknown A/B test: {test_id}")
            return
        
        test = self.ab_tests[test_id]
        
        if is_test_group:
            test['test_results'].append(performance_score)
        else:
            test['control_results'].append(performance_score)
    
    def analyze_ab_test(self, test_id: str) -> Dict[str, Any]:
        """Analyze A/B test results"""
        if test_id not in self.ab_tests:
            return {'error': 'Test not found'}
        
        test = self.ab_tests[test_id]
        control_results = test['control_results']
        test_results = test['test_results']
        
        if len(control_results) < 10 or len(test_results) < 10:
            return {'error': 'Insufficient data for analysis'}
        
        # Calculate statistics
        control_mean = np.mean(control_results)
        test_mean = np.mean(test_results)
        control_std = np.std(control_results)
        test_std = np.std(test_results)
        
        # Calculate improvement
        improvement = (test_mean - control_mean) / control_mean * 100
        
        # Simple statistical significance test (t-test approximation)
        pooled_std = np.sqrt((control_std**2 + test_std**2) / 2)
        t_stat = abs(test_mean - control_mean) / (pooled_std * np.sqrt(2/min(len(control_results), len(test_results))))
        
        # Rough significance check (simplified)
        is_significant = t_stat > 2.0  # Approximately 95% confidence
        
        analysis = {
            'test_name': test['name'],
            'control_strategy': test['control_strategy'],
            'test_strategy': test['test_strategy'],
            'control_mean': control_mean,
            'test_mean': test_mean,
            'improvement_percent': improvement,
            'is_significant': is_significant,
            'confidence': min(95, t_stat * 30),  # Rough confidence percentage
            'sample_sizes': {
                'control': len(control_results),
                'test': len(test_results)
            },
            'recommendation': 'adopt_test' if improvement > 5 and is_significant else 'keep_control'
        }
        
        return analysis
    
    def optimize_for_scenario(self, 
                             scenario: Dict[str, Any],
                             target: OptimizationTarget) -> Dict[str, Any]:
        """Optimize batch configuration for specific scenario"""
        # Generate multiple batch size candidates
        candidates = [10, 25, 50, 75, 100, 150, 200, 300, 500]
        
        best_candidate = None
        best_score = float('-inf')
        
        for batch_size in candidates:
            # Create scenario with this batch size
            test_scenario = scenario.copy()
            test_scenario['current_batch_size'] = batch_size
            
            # Predict performance
            prediction = self.predict_optimal_batch_size(test_scenario, target)
            
            # Calculate optimization score based on target priority
            score = self._calculate_optimization_score(prediction, target)
            
            if score > best_score:
                best_score = score
                best_candidate = {
                    'batch_size': batch_size,
                    'prediction': prediction,
                    'score': score
                }
        
        return best_candidate or {
            'batch_size': 50,
            'prediction': PerformancePrediction(
                predicted_batch_size=50,
                predicted_throughput=50.0,
                predicted_response_time=200.0,
                predicted_resource_usage={'cpu': 50.0, 'memory': 60.0},
                confidence_score=0.1,
                model_accuracy=0.0
            ),
            'score': 0.0
        }
    
    def _calculate_optimization_score(self,
                                    prediction: PerformancePrediction,
                                    target: OptimizationTarget) -> float:
        """Calculate optimization score for a prediction"""
        score = 0.0
        
        if target.priority == "throughput":
            # Higher throughput is better
            score += prediction.predicted_throughput / 100.0
            # Penalize high response time
            score -= max(0, (prediction.predicted_response_time - 500) / 1000.0)
        
        elif target.priority == "latency":
            # Lower response time is better
            score += max(0, (1000 - prediction.predicted_response_time) / 1000.0)
            # Bonus for reasonable throughput
            score += min(0.5, prediction.predicted_throughput / 200.0)
        
        elif target.priority == "resource":
            # Lower resource usage is better
            cpu_score = max(0, (100 - prediction.predicted_resource_usage.get('cpu', 50)) / 100.0)
            memory_score = max(0, (100 - prediction.predicted_resource_usage.get('memory', 60)) / 100.0)
            score += (cpu_score + memory_score) / 2
        
        else:  # balanced
            # Balance all factors
            throughput_score = prediction.predicted_throughput / 200.0
            latency_score = max(0, (1000 - prediction.predicted_response_time) / 1000.0)
            resource_score = (
                max(0, (100 - prediction.predicted_resource_usage.get('cpu', 50)) / 100.0) +
                max(0, (100 - prediction.predicted_resource_usage.get('memory', 60)) / 100.0)
            ) / 2
            
            score = (throughput_score + latency_score + resource_score) / 3
        
        # Apply confidence weighting
        score *= prediction.confidence_score
        
        return score
    
    def get_optimization_insights(self) -> Dict[str, Any]:
        """Get insights from optimization history"""
        if not self.prediction_history:
            return {'message': 'No optimization history available'}
        
        recent_predictions = self.prediction_history[-100:]
        
        insights = {
            'total_predictions': len(self.prediction_history),
            'recent_predictions': len(recent_predictions),
            'average_confidence': np.mean([p.confidence_score for p in recent_predictions]),
            'batch_size_distribution': self._analyze_batch_size_distribution(recent_predictions),
            'performance_trends': self._analyze_performance_trends(recent_predictions),
            'model_performance': self.model_performance,
            'optimization_opportunities': self._identify_optimization_opportunities()
        }
        
        return insights
    
    def _analyze_batch_size_distribution(self, predictions: List[PerformancePrediction]) -> Dict[str, Any]:
        """Analyze distribution of predicted batch sizes"""
        batch_sizes = [p.predicted_batch_size for p in predictions]
        
        return {
            'mean': np.mean(batch_sizes),
            'median': np.median(batch_sizes),
            'std': np.std(batch_sizes),
            'min': min(batch_sizes),
            'max': max(batch_sizes),
            'percentiles': {
                '25th': np.percentile(batch_sizes, 25),
                '75th': np.percentile(batch_sizes, 75),
                '90th': np.percentile(batch_sizes, 90)
            }
        }
    
    def _analyze_performance_trends(self, predictions: List[PerformancePrediction]) -> Dict[str, Any]:
        """Analyze performance trends from predictions"""
        if len(predictions) < 2:
            return {'message': 'Insufficient data for trend analysis'}
        
        # Calculate trends for key metrics
        throughputs = [p.predicted_throughput for p in predictions]
        response_times = [p.predicted_response_time for p in predictions]
        confidences = [p.confidence_score for p in predictions]
        
        return {
            'throughput_trend': 'increasing' if throughputs[-1] > throughputs[0] else 'decreasing',
            'response_time_trend': 'increasing' if response_times[-1] > response_times[0] else 'decreasing',
            'confidence_trend': 'increasing' if confidences[-1] > confidences[0] else 'decreasing',
            'performance_stability': {
                'throughput_variance': np.var(throughputs),
                'response_time_variance': np.var(response_times)
            }
        }
    
    def _identify_optimization_opportunities(self) -> List[Dict[str, str]]:
        """Identify optimization opportunities"""
        opportunities = []
        
        # Check model performance
        for model_name, performance in self.model_performance.items():
            if performance.get('accuracy', 0) < 0.7:
                opportunities.append({
                    'type': 'model_improvement',
                    'description': f'Model {model_name} has low accuracy ({performance.get("accuracy", 0):.2f})',
                    'suggestion': 'Collect more training data or try different model algorithms'
                })
        
        # Check prediction consistency
        if len(self.prediction_history) >= 10:
            recent_confidences = [p.confidence_score for p in self.prediction_history[-10:]]
            if np.mean(recent_confidences) < 0.6:
                opportunities.append({
                    'type': 'prediction_confidence',
                    'description': 'Low prediction confidence in recent predictions',
                    'suggestion': 'Review feature engineering and model training data quality'
                })
        
        # Check A/B test opportunities
        if not self.ab_tests:
            opportunities.append({
                'type': 'ab_testing',
                'description': 'No A/B tests have been conducted',
                'suggestion': 'Start A/B testing different optimization strategies'
            })
        
        return opportunities
    
    def _save_models(self):
        """Save trained models to disk"""
        try:
            model_data = {
                'models': self.models,
                'scalers': self.scalers,
                'model_performance': self.model_performance,
                'feature_columns': self.feature_columns,
                'timestamp': time.time()
            }
            
            with open(self.model_save_path / 'performance_models.pkl', 'wb') as f:
                pickle.dump(model_data, f)
            
            logger.info("Models saved successfully")
            
        except Exception as e:
            logger.error(f"Failed to save models: {e}")
    
    def _load_models(self):
        """Load trained models from disk"""
        try:
            model_file = self.model_save_path / 'performance_models.pkl'
            if model_file.exists():
                with open(model_file, 'rb') as f:
                    model_data = pickle.load(f)
                
                self.models = model_data.get('models', self.models)
                self.scalers = model_data.get('scalers', self.scalers)
                self.model_performance = model_data.get('model_performance', {})
                self.feature_columns = model_data.get('feature_columns', self.feature_columns)
                
                logger.info("Models loaded successfully")
            
        except Exception as e:
            logger.warning(f"Failed to load models: {e}")

# Factory function
def create_performance_optimizer(model_save_path: str = "models/") -> PerformanceOptimizer:
    """Create and configure a performance optimizer"""
    return PerformanceOptimizer(model_save_path)

if __name__ == "__main__":
    # Example usage
    optimizer = create_performance_optimizer()
    
    # Example training data
    sample_features = {
        'current_batch_size': 50,
        'pending_operations': 200,
        'cpu_usage': 60.0,
        'memory_usage': 70.0,
        'network_latency': 15.0,
        'error_rate': 0.02,
        'rate_limit_hits': 0,
        'operation_type': 'read',
        'historical_avg_throughput': 75.0,
        'historical_avg_response_time': 180.0,
        'system_load': 1.2
    }
    
    sample_results = {
        'optimal_batch_size': 75,
        'throughput': 85.0,
        'response_time': 160.0,
        'cpu_usage': 65.0,
        'memory_usage': 72.0
    }
    
    # Add training data
    optimizer.add_training_data(sample_features, sample_results)
    
    # Create optimization target
    target = OptimizationTarget(
        target_throughput=100.0,
        max_response_time=200.0,
        priority="balanced"
    )
    
    # Generate prediction (with minimal training data, this will be low confidence)
    prediction = optimizer.predict_optimal_batch_size(sample_features, target)
    
    print("Performance Prediction:")
    print(f"  Optimal batch size: {prediction.predicted_batch_size}")
    print(f"  Predicted throughput: {prediction.predicted_throughput:.1f}")
    print(f"  Predicted response time: {prediction.predicted_response_time:.1f}ms")
    print(f"  Confidence: {prediction.confidence_score:.2f}")
    
    # Get optimization insights
    insights = optimizer.get_optimization_insights()
    print("\nOptimization Insights:")
    print(f"  Total predictions: {insights['total_predictions']}")
    print(f"  Optimization opportunities: {len(insights['optimization_opportunities'])}")