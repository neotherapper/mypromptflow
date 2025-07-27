#!/usr/bin/env python3
"""
Intelligence Coordinator
Main coordination class for AI agent intelligence system
Integrates content categorization, relationship discovery, and predictive optimization
Achieves comprehensive intelligence with real-time analysis and adaptive learning
"""

import os
import sys
import yaml
import time
import logging
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

# Add the operations directory to Python path for imports
operations_path = Path(__file__).parent.parent
sys.path.insert(0, str(operations_path))

# Import intelligence components
from intelligence.content_categorization import IntelligentContentCategorizer, CategorizationResult
from intelligence.relationship_discovery import IntelligentRelationshipDiscovery, RelationshipResult
from intelligence.predictive_optimization import PredictiveOptimizationEngine, OptimizationRecommendation

# Import database registry manager
from scripts.database_id_registry_manager import DatabaseIDRegistryManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class IntelligenceResult:
    """Comprehensive intelligence analysis result"""
    item_id: str
    database_id: str
    categorization_result: Optional[CategorizationResult]
    relationships: List[RelationshipResult]
    optimization_impact: Dict[str, float]
    intelligence_score: float
    processing_time_ms: float
    recommendations: List[str]
    confidence_level: float

@dataclass
class SystemIntelligenceMetrics:
    """System-wide intelligence performance metrics"""
    total_items_analyzed: int
    categorization_accuracy: float
    relationships_discovered: int
    optimization_improvements: Dict[str, float]
    average_intelligence_score: float
    processing_efficiency: float
    adaptive_learning_rate: float

class IntelligenceCoordinator:
    """
    Main coordination class for AI agent intelligence system
    Orchestrates content categorization, relationship discovery, and predictive optimization
    """
    
    def __init__(self, config_path: str = None):
        """Initialize the intelligence coordination system"""
        self.base_path = Path(__file__).parent.parent.parent
        self.config_path = config_path or self.base_path / "operations/intelligence/schemas/optimization_schema.yaml"
        
        # Initialize intelligence components
        self.categorizer = IntelligentContentCategorizer()
        self.relationship_engine = IntelligentRelationshipDiscovery()
        self.optimization_engine = PredictiveOptimizationEngine()
        self.registry_manager = DatabaseIDRegistryManager()
        
        # Load configuration
        self.config = self._load_config()
        
        # System state and caching
        self.intelligence_cache = {}
        self.system_metrics = SystemIntelligenceMetrics(
            total_items_analyzed=0,
            categorization_accuracy=0.0,
            relationships_discovered=0,
            optimization_improvements={},
            average_intelligence_score=0.0,
            processing_efficiency=0.0,
            adaptive_learning_rate=0.0
        )
        
        # Real-time intelligence processing
        self.real_time_active = False
        self.processing_queue = asyncio.Queue() if hasattr(asyncio, 'Queue') else None
        self.intelligence_history = []
        
        # Thread pool for parallel processing
        self.thread_pool = ThreadPoolExecutor(max_workers=4)
        
        logger.info("Intelligence Coordinator initialized with all AI agent components")
    
    def analyze_item_intelligence(self, item_data: Dict[str, Any], database_id: str, 
                                 include_relationships: bool = True,
                                 target_databases: List[str] = None) -> IntelligenceResult:
        """
        Perform comprehensive intelligence analysis on a single item
        
        Args:
            item_data: Item data dictionary
            database_id: Source database identifier
            include_relationships: Whether to include relationship discovery
            target_databases: List of databases to search for relationships
            
        Returns:
            IntelligenceResult with comprehensive analysis
        """
        start_time = time.time()
        item_id = item_data.get('id', 'unknown')
        
        logger.debug(f"Starting intelligence analysis for {item_id} in {database_id}")
        
        try:
            # Step 1: Content categorization
            categorization_result = self.categorizer.categorize_content(item_data, database_id)
            
            # Step 2: Relationship discovery (if enabled)
            relationships = []
            if include_relationships and target_databases:
                target_items = self._get_target_items_for_relationships(target_databases)
                relationships = self.relationship_engine.discover_relationships(
                    item_data, database_id, target_items, target_databases
                )
            
            # Step 3: Calculate optimization impact
            optimization_impact = self._calculate_optimization_impact(
                item_data, categorization_result, relationships
            )
            
            # Step 4: Calculate intelligence score
            intelligence_score = self._calculate_intelligence_score(
                categorization_result, relationships, optimization_impact
            )
            
            # Step 5: Generate recommendations
            recommendations = self._generate_intelligence_recommendations(
                categorization_result, relationships, optimization_impact
            )
            
            # Step 6: Calculate confidence level
            confidence_level = self._calculate_overall_confidence(
                categorization_result, relationships
            )
            
            processing_time = (time.time() - start_time) * 1000
            
            # Create comprehensive result
            result = IntelligenceResult(
                item_id=item_id,
                database_id=database_id,
                categorization_result=categorization_result,
                relationships=relationships,
                optimization_impact=optimization_impact,
                intelligence_score=intelligence_score,
                processing_time_ms=processing_time,
                recommendations=recommendations,
                confidence_level=confidence_level
            )
            
            # Cache and record result
            self._cache_intelligence_result(result)
            self._record_intelligence_analysis(result)
            
            logger.debug(f"Intelligence analysis completed for {item_id}: "
                        f"score={intelligence_score:.2f}, confidence={confidence_level:.2f} "
                        f"({processing_time:.1f}ms)")
            
            return result
            
        except Exception as e:
            processing_time = (time.time() - start_time) * 1000
            logger.error(f"Error in intelligence analysis for {item_id}: {e}")
            
            # Return minimal result on error
            return IntelligenceResult(
                item_id=item_id,
                database_id=database_id,
                categorization_result=None,
                relationships=[],
                optimization_impact={},
                intelligence_score=0.0,
                processing_time_ms=processing_time,
                recommendations=[f"Analysis failed: {str(e)}"],
                confidence_level=0.0
            )
    
    def analyze_database_intelligence(self, database_id: str, 
                                    max_items: int = 100,
                                    parallel_processing: bool = True) -> Dict[str, Any]:
        """
        Perform comprehensive intelligence analysis on an entire database
        
        Args:
            database_id: Database identifier to analyze
            max_items: Maximum number of items to analyze
            parallel_processing: Whether to use parallel processing
            
        Returns:
            Comprehensive database intelligence analysis
        """
        logger.info(f"Starting database intelligence analysis for {database_id} (max {max_items} items)")
        start_time = time.time()
        
        try:
            # Get database items
            database_items = self._get_database_items(database_id, max_items)
            if not database_items:
                logger.warning(f"No items found in database {database_id}")
                return {'error': f'No items found in database {database_id}'}
            
            # Get all other databases for relationship analysis
            all_databases = self._get_all_database_ids()
            target_databases = [db for db in all_databases if db != database_id]
            
            # Analyze items
            if parallel_processing:
                results = self._analyze_items_parallel(database_items, database_id, target_databases)
            else:
                results = self._analyze_items_sequential(database_items, database_id, target_databases)
            
            # Generate comprehensive database analysis
            database_analysis = self._generate_database_analysis(results, database_id)
            
            processing_time = (time.time() - start_time) * 1000
            database_analysis['processing_time_ms'] = processing_time
            
            logger.info(f"Database intelligence analysis completed for {database_id}: "
                       f"{len(results)} items analyzed ({processing_time:.1f}ms)")
            
            return database_analysis
            
        except Exception as e:
            logger.error(f"Error in database intelligence analysis for {database_id}: {e}")
            return {'error': str(e)}
    
    def analyze_cross_database_intelligence(self, database_ids: List[str] = None,
                                          max_items_per_db: int = 50) -> Dict[str, Any]:
        """
        Perform comprehensive cross-database intelligence analysis
        
        Args:
            database_ids: List of database IDs to analyze (None for all)
            max_items_per_db: Maximum items per database
            
        Returns:
            Cross-database intelligence analysis results
        """
        if not database_ids:
            database_ids = self._get_all_database_ids()
        
        logger.info(f"Starting cross-database intelligence analysis across {len(database_ids)} databases")
        start_time = time.time()
        
        try:
            # Collect items from all databases
            all_database_items = {}
            for db_id in database_ids:
                items = self._get_database_items(db_id, max_items_per_db)
                if items:
                    all_database_items[db_id] = items
            
            # Perform cross-database relationship analysis
            relationship_analysis = self.relationship_engine.analyze_cross_database_relationships(
                all_database_items
            )
            
            # Analyze categorization patterns across databases
            categorization_analysis = self._analyze_cross_database_categorization(all_database_items)
            
            # Generate optimization recommendations for entire system
            system_recommendations = self._generate_system_optimization_recommendations(
                all_database_items, relationship_analysis
            )
            
            # Calculate system intelligence metrics
            system_intelligence = self._calculate_system_intelligence_metrics(
                all_database_items, relationship_analysis, categorization_analysis
            )
            
            processing_time = (time.time() - start_time) * 1000
            
            cross_db_analysis = {
                'analysis_summary': {
                    'databases_analyzed': len(all_database_items),
                    'total_items_analyzed': sum(len(items) for items in all_database_items.values()),
                    'processing_time_ms': processing_time
                },
                'relationship_analysis': relationship_analysis,
                'categorization_analysis': categorization_analysis,
                'system_recommendations': system_recommendations,
                'system_intelligence_metrics': system_intelligence,
                'cross_database_insights': self._generate_cross_database_insights(
                    all_database_items, relationship_analysis, categorization_analysis
                )
            }
            
            logger.info(f"Cross-database intelligence analysis completed: "
                       f"{len(all_database_items)} databases, "
                       f"{sum(len(items) for items in all_database_items.values())} items "
                       f"({processing_time:.1f}ms)")
            
            return cross_db_analysis
            
        except Exception as e:
            logger.error(f"Error in cross-database intelligence analysis: {e}")
            return {'error': str(e)}
    
    def start_real_time_intelligence(self, monitoring_interval_seconds: int = 60):
        """
        Start real-time intelligence monitoring and adaptive learning
        
        Args:
            monitoring_interval_seconds: Interval for intelligence analysis
        """
        if self.real_time_active:
            logger.warning("Real-time intelligence is already active")
            return
        
        logger.info(f"Starting real-time intelligence monitoring (interval: {monitoring_interval_seconds}s)")
        
        self.real_time_active = True
        
        # Start real-time monitoring for optimization engine
        self.optimization_engine.start_real_time_monitoring(monitoring_interval_seconds)
        
        # Start intelligence coordination loop
        intelligence_thread = threading.Thread(
            target=self._real_time_intelligence_loop,
            args=(monitoring_interval_seconds,),
            daemon=True
        )
        intelligence_thread.start()
    
    def stop_real_time_intelligence(self):
        """Stop real-time intelligence monitoring"""
        if not self.real_time_active:
            return
        
        logger.info("Stopping real-time intelligence monitoring")
        self.real_time_active = False
        
        # Stop optimization engine monitoring
        self.optimization_engine.stop_real_time_monitoring()
    
    def get_intelligence_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive intelligence system performance statistics
        
        Returns:
            Dictionary with detailed system metrics and performance data
        """
        # Get component statistics
        categorization_stats = self.categorizer.get_categorization_statistics()
        relationship_stats = self.relationship_engine.get_discovery_statistics()
        optimization_stats = self.optimization_engine.get_optimization_statistics()
        
        # Calculate overall system statistics
        total_analyses = len(self.intelligence_history)
        successful_analyses = [r for r in self.intelligence_history if r.intelligence_score > 0.5]
        
        avg_intelligence_score = (
            sum(r.intelligence_score for r in self.intelligence_history) / max(total_analyses, 1)
            if self.intelligence_history else 0.0
        )
        
        avg_processing_time = (
            sum(r.processing_time_ms for r in self.intelligence_history) / max(total_analyses, 1)
            if self.intelligence_history else 0.0
        )
        
        return {
            "system_summary": {
                "total_intelligence_analyses": total_analyses,
                "successful_analyses": len(successful_analyses),
                "success_rate_percentage": (len(successful_analyses) / max(total_analyses, 1)) * 100,
                "average_intelligence_score": avg_intelligence_score,
                "average_processing_time_ms": avg_processing_time,
                "real_time_monitoring_active": self.real_time_active
            },
            "component_statistics": {
                "categorization": categorization_stats,
                "relationship_discovery": relationship_stats,
                "predictive_optimization": optimization_stats
            },
            "system_metrics": asdict(self.system_metrics),
            "cache_performance": {
                "cached_results": len(self.intelligence_cache),
                "cache_hit_rate": self._calculate_cache_hit_rate()
            },
            "adaptive_learning": {
                "learning_rate": self.system_metrics.adaptive_learning_rate,
                "pattern_evolution": self._calculate_pattern_evolution_rate(),
                "accuracy_improvement": self._calculate_accuracy_improvement_trend()
            }
        }
    
    def update_intelligence_feedback(self, feedback_data: List[Dict[str, Any]]) -> bool:
        """
        Update intelligence system based on user feedback
        
        Args:
            feedback_data: List of feedback items for system improvement
            
        Returns:
            True if feedback was processed successfully
        """
        logger.info(f"Processing intelligence feedback from {len(feedback_data)} items")
        
        try:
            # Process categorization feedback
            categorization_feedback = [
                fb for fb in feedback_data 
                if fb.get('feedback_type') == 'categorization'
            ]
            if categorization_feedback:
                self.categorizer.update_category_patterns(categorization_feedback)
            
            # Process relationship feedback
            relationship_feedback = [
                fb for fb in feedback_data 
                if fb.get('feedback_type') == 'relationship'
            ]
            if relationship_feedback:
                self._process_relationship_feedback(relationship_feedback)
            
            # Update adaptive learning rate
            self.system_metrics.adaptive_learning_rate = min(
                self.system_metrics.adaptive_learning_rate + 0.01, 1.0
            )
            
            logger.info("Intelligence feedback processed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error processing intelligence feedback: {e}")
            return False
    
    # Private helper methods
    
    def _load_config(self) -> Dict[str, Any]:
        """Load intelligence coordinator configuration"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Error loading intelligence config: {e}")
            return {}
    
    def _get_target_items_for_relationships(self, target_databases: List[str], 
                                          max_items_per_db: int = 50) -> List[Dict[str, Any]]:
        """Get target items for relationship discovery"""
        target_items = []
        
        for db_id in target_databases:
            db_items = self._get_database_items(db_id, max_items_per_db)
            if db_items:
                # Add database_id to each item for identification
                for item in db_items:
                    item['database_id'] = db_id
                target_items.extend(db_items)
        
        return target_items
    
    def _get_database_items(self, database_id: str, max_items: int = 100) -> List[Dict[str, Any]]:
        """Get items from a specific database"""
        try:
            # In a real implementation, this would query the actual database
            # For now, return mock data based on database_id
            mock_items = []
            
            for i in range(min(max_items, 20)):  # Limit to 20 for testing
                mock_items.append({
                    'id': f'{database_id}_item_{i:03d}',
                    'name': f'Sample Item {i} from {database_id}',
                    'description': f'This is a sample description for item {i} in {database_id} database',
                    'tags': [database_id.replace('_', '-'), 'sample', 'test'],
                    'category': 'sample',
                    'url': f'https://example.com/{database_id}/item_{i}',
                    'created_date': datetime.now().isoformat()
                })
            
            return mock_items
            
        except Exception as e:
            logger.error(f"Error getting items from database {database_id}: {e}")
            return []
    
    def _get_all_database_ids(self) -> List[str]:
        """Get list of all available database IDs"""
        return [
            'knowledge_vault',
            'tools_services',
            'business_ideas',
            'training_vault',
            'platforms_sites',
            'notes_ideas'
        ]
    
    def _calculate_optimization_impact(self, item_data: Dict[str, Any],
                                     categorization_result: Optional[CategorizationResult],
                                     relationships: List[RelationshipResult]) -> Dict[str, float]:
        """Calculate optimization impact for the item"""
        impact = {
            'cache_priority': 0.5,
            'batch_processing_priority': 0.5,
            'relationship_value': 0.0,
            'categorization_value': 0.0
        }
        
        # Calculate relationship value
        if relationships:
            avg_strength = sum(r.strength_score for r in relationships) / len(relationships)
            impact['relationship_value'] = avg_strength
            impact['cache_priority'] += avg_strength * 0.3
        
        # Calculate categorization value
        if categorization_result and categorization_result.validation_passed:
            impact['categorization_value'] = categorization_result.quality_score
            impact['cache_priority'] += categorization_result.quality_score * 0.2
        
        # Normalize values
        for key in impact:
            impact[key] = min(impact[key], 1.0)
        
        return impact
    
    def _calculate_intelligence_score(self, categorization_result: Optional[CategorizationResult],
                                    relationships: List[RelationshipResult],
                                    optimization_impact: Dict[str, float]) -> float:
        """Calculate overall intelligence score for the item"""
        score_components = []
        
        # Categorization score (30% weight)
        if categorization_result and categorization_result.validation_passed:
            cat_score = categorization_result.quality_score * 0.3
            score_components.append(cat_score)
        
        # Relationship score (40% weight)
        if relationships:
            rel_score = min(len(relationships) / 10, 1.0) * 0.4  # Normalize to max 10 relationships
            avg_strength = sum(r.strength_score for r in relationships) / len(relationships)
            rel_score *= avg_strength
            score_components.append(rel_score)
        
        # Optimization impact score (30% weight)
        if optimization_impact:
            opt_score = sum(optimization_impact.values()) / len(optimization_impact) * 0.3
            score_components.append(opt_score)
        
        # Overall intelligence score
        return sum(score_components) if score_components else 0.0
    
    def _generate_intelligence_recommendations(self, categorization_result: Optional[CategorizationResult],
                                             relationships: List[RelationshipResult],
                                             optimization_impact: Dict[str, float]) -> List[str]:
        """Generate intelligence-based recommendations"""
        recommendations = []
        
        # Categorization recommendations
        if categorization_result:
            if categorization_result.quality_score < 0.7:
                recommendations.append("Consider improving item description for better categorization")
            if len(categorization_result.assigned_categories) < 2:
                recommendations.append("Add more relevant tags to improve categorization")
        
        # Relationship recommendations
        if len(relationships) > 5:
            recommendations.append("High relationship count - consider as hub item for improved caching")
        elif len(relationships) == 0:
            recommendations.append("No relationships found - consider adding tags or improving description")
        
        # Optimization recommendations
        if optimization_impact.get('cache_priority', 0) > 0.8:
            recommendations.append("High cache priority - include in hot cache tier")
        if optimization_impact.get('relationship_value', 0) > 0.8:
            recommendations.append("High relationship value - use for recommendation systems")
        
        return recommendations
    
    def _calculate_overall_confidence(self, categorization_result: Optional[CategorizationResult],
                                    relationships: List[RelationshipResult]) -> float:
        """Calculate overall confidence level for the analysis"""
        confidence_factors = []
        
        # Categorization confidence
        if categorization_result:
            avg_cat_confidence = (
                sum(categorization_result.confidence_scores.values()) / 
                max(len(categorization_result.confidence_scores), 1)
            )
            confidence_factors.append(avg_cat_confidence)
        
        # Relationship confidence
        if relationships:
            avg_rel_confidence = sum(r.confidence_level for r in relationships) / len(relationships)
            confidence_factors.append(avg_rel_confidence)
        
        # Overall confidence
        return sum(confidence_factors) / max(len(confidence_factors), 1) if confidence_factors else 0.0
    
    def _cache_intelligence_result(self, result: IntelligenceResult):
        """Cache intelligence result for future reference"""
        cache_key = f"{result.database_id}:{result.item_id}"
        self.intelligence_cache[cache_key] = {
            'result': result,
            'timestamp': datetime.now().isoformat(),
            'access_count': 0
        }
        
        # Limit cache size
        if len(self.intelligence_cache) > 1000:
            # Remove oldest entries
            sorted_items = sorted(
                self.intelligence_cache.items(),
                key=lambda x: x[1]['timestamp']
            )
            for key, _ in sorted_items[:100]:  # Remove oldest 100
                del self.intelligence_cache[key]
    
    def _record_intelligence_analysis(self, result: IntelligenceResult):
        """Record intelligence analysis for metrics and learning"""
        self.intelligence_history.append(result)
        
        # Update system metrics
        self.system_metrics.total_items_analyzed += 1
        
        # Update categorization accuracy
        if result.categorization_result and result.categorization_result.validation_passed:
            current_accuracy = self.system_metrics.categorization_accuracy
            total_analyzed = self.system_metrics.total_items_analyzed
            new_accuracy = (current_accuracy * (total_analyzed - 1) + 
                          result.categorization_result.quality_score) / total_analyzed
            self.system_metrics.categorization_accuracy = new_accuracy
        
        # Update relationships discovered
        self.system_metrics.relationships_discovered += len(result.relationships)
        
        # Update average intelligence score
        current_avg = self.system_metrics.average_intelligence_score
        total_analyzed = self.system_metrics.total_items_analyzed
        new_avg = (current_avg * (total_analyzed - 1) + result.intelligence_score) / total_analyzed
        self.system_metrics.average_intelligence_score = new_avg
        
        # Keep history manageable
        if len(self.intelligence_history) > 10000:
            self.intelligence_history = self.intelligence_history[-5000:]  # Keep last 5000
    
    def _analyze_items_parallel(self, items: List[Dict[str, Any]], database_id: str,
                              target_databases: List[str]) -> List[IntelligenceResult]:
        """Analyze items using parallel processing"""
        results = []
        
        # Submit tasks to thread pool
        future_to_item = {}
        for item in items:
            future = self.thread_pool.submit(
                self.analyze_item_intelligence,
                item, database_id, True, target_databases
            )
            future_to_item[future] = item
        
        # Collect results
        for future in as_completed(future_to_item):
            try:
                result = future.result(timeout=30)  # 30 second timeout per item
                results.append(result)
            except Exception as e:
                item = future_to_item[future]
                logger.error(f"Error analyzing item {item.get('id', 'unknown')}: {e}")
        
        return results
    
    def _analyze_items_sequential(self, items: List[Dict[str, Any]], database_id: str,
                                target_databases: List[str]) -> List[IntelligenceResult]:
        """Analyze items sequentially"""
        results = []
        
        for item in items:
            try:
                result = self.analyze_item_intelligence(item, database_id, True, target_databases)
                results.append(result)
            except Exception as e:
                logger.error(f"Error analyzing item {item.get('id', 'unknown')}: {e}")
        
        return results
    
    def _generate_database_analysis(self, results: List[IntelligenceResult], 
                                  database_id: str) -> Dict[str, Any]:
        """Generate comprehensive database analysis from individual results"""
        successful_results = [r for r in results if r.intelligence_score > 0.0]
        
        analysis = {
            'database_summary': {
                'database_id': database_id,
                'total_items_analyzed': len(results),
                'successful_analyses': len(successful_results),
                'success_rate': len(successful_results) / max(len(results), 1) * 100,
                'average_intelligence_score': (
                    sum(r.intelligence_score for r in successful_results) / 
                    max(len(successful_results), 1)
                ),
                'average_processing_time_ms': (
                    sum(r.processing_time_ms for r in results) / max(len(results), 1)
                )
            },
            'categorization_analysis': self._analyze_database_categorization(successful_results),
            'relationship_analysis': self._analyze_database_relationships(successful_results),
            'optimization_insights': self._analyze_database_optimization(successful_results),
            'top_items': self._get_top_intelligent_items(successful_results, 10),
            'recommendations': self._generate_database_recommendations(successful_results, database_id)
        }
        
        return analysis
    
    def _analyze_database_categorization(self, results: List[IntelligenceResult]) -> Dict[str, Any]:
        """Analyze categorization patterns in database results"""
        categorization_data = [r.categorization_result for r in results 
                             if r.categorization_result and r.categorization_result.validation_passed]
        
        if not categorization_data:
            return {'message': 'No valid categorization data'}
        
        # Category distribution
        all_categories = []
        for cat_result in categorization_data:
            all_categories.extend(cat_result.assigned_categories)
        
        from collections import Counter
        category_counts = Counter(all_categories)
        
        # Quality metrics
        quality_scores = [cat.quality_score for cat in categorization_data]
        
        return {
            'total_categorized_items': len(categorization_data),
            'average_quality_score': sum(quality_scores) / len(quality_scores),
            'category_distribution': dict(category_counts.most_common(10)),
            'average_categories_per_item': len(all_categories) / len(categorization_data),
            'quality_distribution': {
                'high_quality': len([q for q in quality_scores if q >= 0.8]),
                'medium_quality': len([q for q in quality_scores if 0.6 <= q < 0.8]),
                'low_quality': len([q for q in quality_scores if q < 0.6])
            }
        }
    
    def _analyze_database_relationships(self, results: List[IntelligenceResult]) -> Dict[str, Any]:
        """Analyze relationship patterns in database results"""
        all_relationships = []
        for result in results:
            all_relationships.extend(result.relationships)
        
        if not all_relationships:
            return {'message': 'No relationships discovered'}
        
        from collections import Counter
        relationship_types = Counter(r.relationship_type for r in all_relationships)
        
        # Strength distribution
        strength_scores = [r.strength_score for r in all_relationships]
        
        return {
            'total_relationships': len(all_relationships),
            'relationship_type_distribution': dict(relationship_types),
            'average_strength_score': sum(strength_scores) / len(strength_scores),
            'strength_distribution': {
                'strong': len([s for s in strength_scores if s >= 0.8]),
                'moderate': len([s for s in strength_scores if 0.6 <= s < 0.8]),
                'weak': len([s for s in strength_scores if s < 0.6])
            },
            'top_connected_items': self._get_most_connected_items(results, 5)
        }
    
    def _analyze_database_optimization(self, results: List[IntelligenceResult]) -> Dict[str, Any]:
        """Analyze optimization insights from database results"""
        optimization_data = [r.optimization_impact for r in results if r.optimization_impact]
        
        if not optimization_data:
            return {'message': 'No optimization data available'}
        
        # Aggregate optimization metrics
        aggregated_metrics = {}
        for impact_data in optimization_data:
            for metric, value in impact_data.items():
                if metric not in aggregated_metrics:
                    aggregated_metrics[metric] = []
                aggregated_metrics[metric].append(value)
        
        # Calculate averages
        avg_metrics = {}
        for metric, values in aggregated_metrics.items():
            avg_metrics[f'average_{metric}'] = sum(values) / len(values)
        
        # High-value items
        high_cache_priority = [r for r in results 
                             if r.optimization_impact.get('cache_priority', 0) > 0.8]
        
        return {
            'optimization_metrics': avg_metrics,
            'high_cache_priority_items': len(high_cache_priority),
            'optimization_recommendations': [
                f"{len(high_cache_priority)} items identified for high-priority caching",
                f"Average relationship value: {avg_metrics.get('average_relationship_value', 0):.2f}",
                f"Average categorization value: {avg_metrics.get('average_categorization_value', 0):.2f}"
            ]
        }
    
    def _get_top_intelligent_items(self, results: List[IntelligenceResult], count: int) -> List[Dict[str, Any]]:
        """Get top items by intelligence score"""
        sorted_results = sorted(results, key=lambda x: x.intelligence_score, reverse=True)
        
        return [
            {
                'item_id': r.item_id,
                'intelligence_score': r.intelligence_score,
                'confidence_level': r.confidence_level,
                'relationships_count': len(r.relationships),
                'categories_count': len(r.categorization_result.assigned_categories) 
                                  if r.categorization_result else 0,
                'recommendations': r.recommendations[:3]  # Top 3 recommendations
            }
            for r in sorted_results[:count]
        ]
    
    def _generate_database_recommendations(self, results: List[IntelligenceResult], 
                                         database_id: str) -> List[str]:
        """Generate database-specific recommendations"""
        recommendations = []
        
        # Analyze overall performance
        avg_intelligence = sum(r.intelligence_score for r in results) / max(len(results), 1)
        
        if avg_intelligence < 0.6:
            recommendations.append(f"Database {database_id} has low intelligence scores - consider improving item descriptions and tags")
        
        # Analyze categorization
        categorized_items = [r for r in results 
                           if r.categorization_result and r.categorization_result.validation_passed]
        
        if len(categorized_items) / max(len(results), 1) < 0.8:
            recommendations.append(f"Only {len(categorized_items)}/{len(results)} items successfully categorized - review categorization criteria")
        
        # Analyze relationships
        items_with_relationships = [r for r in results if r.relationships]
        
        if len(items_with_relationships) / max(len(results), 1) < 0.5:
            recommendations.append(f"Low relationship discovery rate - consider adding more descriptive content or tags")
        
        return recommendations
    
    def _get_most_connected_items(self, results: List[IntelligenceResult], count: int) -> List[Dict[str, Any]]:
        """Get items with most relationships"""
        sorted_results = sorted(results, key=lambda x: len(x.relationships), reverse=True)
        
        return [
            {
                'item_id': r.item_id,
                'relationships_count': len(r.relationships),
                'intelligence_score': r.intelligence_score,
                'relationship_types': list(set(rel.relationship_type for rel in r.relationships))
            }
            for r in sorted_results[:count]
        ]
    
    def _analyze_cross_database_categorization(self, all_database_items: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """Analyze categorization patterns across databases"""
        cross_db_analysis = {}
        
        # Analyze each database's categorization characteristics
        for db_id, items in all_database_items.items():
            # Sample items for analysis
            sample_items = items[:20] if len(items) > 20 else items
            
            categorization_results = []
            for item in sample_items:
                result = self.categorizer.categorize_content(item, db_id)
                if result.validation_passed:
                    categorization_results.append(result)
            
            if categorization_results:
                avg_quality = sum(r.quality_score for r in categorization_results) / len(categorization_results)
                all_categories = []
                for r in categorization_results:
                    all_categories.extend(r.assigned_categories)
                
                from collections import Counter
                category_counts = Counter(all_categories)
                
                cross_db_analysis[db_id] = {
                    'average_quality': avg_quality,
                    'top_categories': dict(category_counts.most_common(5)),
                    'categorization_rate': len(categorization_results) / len(sample_items)
                }
        
        return cross_db_analysis
    
    def _generate_system_optimization_recommendations(self, all_database_items: Dict[str, List[Dict[str, Any]]],
                                                    relationship_analysis: Dict[str, Any]) -> List[OptimizationRecommendation]:
        """Generate system-wide optimization recommendations"""
        recommendations = []
        
        # Get system metrics
        total_items = sum(len(items) for items in all_database_items.values())
        total_relationships = relationship_analysis.get('analysis_summary', {}).get('total_relationships_discovered', 0)
        
        # System-level cache optimization
        if total_relationships > 100:
            recommendations.append(OptimizationRecommendation(
                recommendation_id="system_cache_001",
                category="performance_improvements",
                priority="high",
                impact_score=0.85,
                implementation_effort="medium",
                description="Implement cross-database intelligent caching based on relationship patterns",
                expected_improvement={
                    'cross_database_query_time': 0.40,
                    'relationship_traversal_speed': 0.35
                },
                implementation_steps=[
                    "Analyze relationship patterns across databases",
                    "Implement predictive caching for highly connected items",
                    "Configure cache warming based on cross-database relationships"
                ],
                risk_level="low"
            ))
        
        # Database balancing recommendation
        db_sizes = [(db_id, len(items)) for db_id, items in all_database_items.items()]
        db_sizes.sort(key=lambda x: x[1], reverse=True)
        
        if db_sizes[0][1] > db_sizes[-1][1] * 3:  # If largest DB is 3x larger than smallest
            recommendations.append(OptimizationRecommendation(
                recommendation_id="system_balance_001",
                category="operational_efficiency",
                priority="medium",
                impact_score=0.6,
                implementation_effort="high",
                description="Rebalance database sizes for optimal performance",
                expected_improvement={
                    'query_distribution': 0.25,
                    'system_load_balance': 0.30
                },
                implementation_steps=[
                    f"Consider redistributing items from {db_sizes[0][0]} to smaller databases",
                    "Implement automatic load balancing for new items",
                    "Monitor database growth patterns"
                ],
                risk_level="medium"
            ))
        
        return recommendations
    
    def _calculate_system_intelligence_metrics(self, all_database_items: Dict[str, List[Dict[str, Any]]],
                                             relationship_analysis: Dict[str, Any],
                                             categorization_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate system-wide intelligence metrics"""
        total_items = sum(len(items) for items in all_database_items.values())
        total_relationships = relationship_analysis.get('analysis_summary', {}).get('total_relationships_discovered', 0)
        
        # Calculate connectivity score
        connectivity_score = min(total_relationships / max(total_items, 1), 1.0)
        
        # Calculate categorization coverage
        categorization_scores = []
        for db_analysis in categorization_analysis.values():
            if isinstance(db_analysis, dict) and 'average_quality' in db_analysis:
                categorization_scores.append(db_analysis['average_quality'])
        
        avg_categorization_quality = (
            sum(categorization_scores) / max(len(categorization_scores), 1)
            if categorization_scores else 0.0
        )
        
        return {
            'system_connectivity_score': connectivity_score,
            'average_categorization_quality': avg_categorization_quality,
            'cross_database_relationship_density': total_relationships / max(total_items * (total_items - 1) / 2, 1),
            'system_intelligence_index': (connectivity_score + avg_categorization_quality) / 2,
            'databases_analyzed': len(all_database_items),
            'total_items_in_system': total_items
        }
    
    def _generate_cross_database_insights(self, all_database_items: Dict[str, List[Dict[str, Any]]],
                                        relationship_analysis: Dict[str, Any],
                                        categorization_analysis: Dict[str, Any]) -> List[str]:
        """Generate cross-database insights"""
        insights = []
        
        # Database connectivity insights
        connectivity_matrix = relationship_analysis.get('connectivity_matrix', {})
        
        if connectivity_matrix:
            # Find most connected database pairs
            max_connections = 0
            best_pair = None
            
            for source_db, targets in connectivity_matrix.items():
                for target_db, connection_count in targets.items():
                    if connection_count > max_connections:
                        max_connections = connection_count
                        best_pair = (source_db, target_db)
            
            if best_pair:
                insights.append(f"Highest connectivity: {best_pair[0]} <-> {best_pair[1]} ({max_connections} relationships)")
        
        # Categorization insights
        if categorization_analysis:
            db_qualities = [(db_id, analysis.get('average_quality', 0)) 
                          for db_id, analysis in categorization_analysis.items()
                          if isinstance(analysis, dict)]
            
            if db_qualities:
                db_qualities.sort(key=lambda x: x[1], reverse=True)
                insights.append(f"Best categorization quality: {db_qualities[0][0]} ({db_qualities[0][1]:.2f})")
                
                if len(db_qualities) > 1:
                    insights.append(f"Lowest categorization quality: {db_qualities[-1][0]} ({db_qualities[-1][1]:.2f})")
        
        # System size insights
        db_sizes = sorted([(db_id, len(items)) for db_id, items in all_database_items.items()], 
                         key=lambda x: x[1], reverse=True)
        
        if db_sizes:
            insights.append(f"Largest database: {db_sizes[0][0]} ({db_sizes[0][1]} items)")
            insights.append(f"Total system size: {sum(size for _, size in db_sizes)} items across {len(db_sizes)} databases")
        
        return insights
    
    def _calculate_cache_hit_rate(self) -> float:
        """Calculate cache hit rate for intelligence results"""
        if not self.intelligence_cache:
            return 0.0
        
        total_accesses = sum(entry['access_count'] for entry in self.intelligence_cache.values())
        cache_hits = len([entry for entry in self.intelligence_cache.values() if entry['access_count'] > 0])
        
        return cache_hits / max(len(self.intelligence_cache), 1)
    
    def _calculate_pattern_evolution_rate(self) -> float:
        """Calculate how quickly patterns are evolving"""
        # Simplified calculation - in practice would analyze pattern changes over time
        return self.system_metrics.adaptive_learning_rate * 0.5
    
    def _calculate_accuracy_improvement_trend(self) -> float:
        """Calculate accuracy improvement trend"""
        if len(self.intelligence_history) < 10:
            return 0.0
        
        # Compare recent accuracy vs historical accuracy
        recent_scores = [r.intelligence_score for r in self.intelligence_history[-10:]]
        historical_scores = [r.intelligence_score for r in self.intelligence_history[-50:-10]] if len(self.intelligence_history) >= 50 else []
        
        if not historical_scores:
            return 0.0
        
        recent_avg = sum(recent_scores) / len(recent_scores)
        historical_avg = sum(historical_scores) / len(historical_scores)
        
        return (recent_avg - historical_avg) / max(historical_avg, 0.01)
    
    def _process_relationship_feedback(self, feedback_data: List[Dict[str, Any]]):
        """Process relationship feedback for learning"""
        for feedback in feedback_data:
            source_item = feedback.get('source_item_id')
            target_item = feedback.get('target_item_id')
            source_db = feedback.get('source_database')
            target_db = feedback.get('target_database')
            new_strength = feedback.get('corrected_strength')
            
            if all([source_item, target_item, source_db, target_db, new_strength is not None]):
                self.relationship_engine.update_relationship_strength(
                    source_item, source_db, target_item, target_db, 
                    new_strength, "user_feedback"
                )
    
    def _real_time_intelligence_loop(self, interval_seconds: int):
        """Real-time intelligence monitoring and adaptive learning loop"""
        logger.info("Real-time intelligence loop started")
        
        while self.real_time_active:
            try:
                # Perform periodic intelligence analysis on random samples
                all_db_ids = self._get_all_database_ids()
                
                for db_id in all_db_ids:
                    # Sample a few items for continuous analysis
                    sample_items = self._get_database_items(db_id, 5)  # Small sample
                    
                    if sample_items:
                        for item in sample_items[:2]:  # Analyze 2 items per database
                            # Quick intelligence analysis
                            result = self.analyze_item_intelligence(
                                item, db_id, include_relationships=False
                            )
                            
                            # Update learning patterns if needed
                            if result.intelligence_score > 0.8:
                                self._update_high_performance_patterns(result)
                
                # Perform system optimization analysis
                self._perform_system_optimization_cycle()
                
                time.sleep(interval_seconds)
                
            except Exception as e:
                logger.error(f"Error in real-time intelligence loop: {e}")
                time.sleep(interval_seconds)
        
        logger.info("Real-time intelligence loop stopped")
    
    def _update_high_performance_patterns(self, result: IntelligenceResult):
        """Update patterns based on high-performance results"""
        # Extract patterns from high-performing items
        if result.categorization_result and result.categorization_result.quality_score > 0.8:
            # This is a high-quality categorization - learn from it
            self.system_metrics.adaptive_learning_rate = min(
                self.system_metrics.adaptive_learning_rate + 0.001, 1.0
            )
    
    def _perform_system_optimization_cycle(self):
        """Perform a system optimization cycle"""
        try:
            # Generate system metrics
            current_metrics = {
                'avg_response_time': 150,  # Mock data
                'cache_hit_rate': self._calculate_cache_hit_rate(),
                'total_analyses': len(self.intelligence_history),
                'system_intelligence_score': self.system_metrics.average_intelligence_score
            }
            
            # Generate optimization recommendations
            recommendations = self.optimization_engine.generate_optimization_recommendations(current_metrics)
            
            # Apply automatic optimizations if any
            if recommendations:
                logger.debug(f"Generated {len(recommendations)} optimization recommendations during real-time cycle")
            
        except Exception as e:
            logger.error(f"Error in system optimization cycle: {e}")

def main():
    """Main function for testing and CLI operations"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Intelligence Coordinator - AI Agent Intelligence System')
    parser.add_argument('--test', action='store_true', help='Run comprehensive intelligence test')
    parser.add_argument('--analyze-item', help='Analyze intelligence for specific item ID')
    parser.add_argument('--analyze-database', help='Analyze intelligence for entire database')
    parser.add_argument('--cross-database', action='store_true', help='Perform cross-database analysis')
    parser.add_argument('--stats', action='store_true', help='Show intelligence statistics')
    parser.add_argument('--monitor', type=int, help='Start real-time monitoring (interval in seconds)')
    
    args = parser.parse_args()
    
    # Initialize intelligence coordinator
    coordinator = IntelligenceCoordinator()
    
    if args.test:
        print("🧠 Running Comprehensive Intelligence System Test")
        
        # Test single item analysis
        test_item = {
            'id': 'test-intelligence-001',
            'name': 'Advanced AI-Powered Maritime Insurance Analytics Platform',
            'description': 'Comprehensive analytics platform using machine learning for maritime insurance risk assessment, claims processing, and fraud detection',
            'tags': ['ai', 'maritime-insurance', 'analytics', 'machine-learning', 'risk-assessment'],
            'category': 'platform',
            'url': 'https://maritime-ai-analytics.com'
        }
        
        result = coordinator.analyze_item_intelligence(
            test_item, 'tools_services', include_relationships=True,
            target_databases=['knowledge_vault', 'business_ideas']
        )
        
        print(f"\\n📊 Intelligence Analysis Result:")
        print(f"   Item: {result.item_id}")
        print(f"   Intelligence Score: {result.intelligence_score:.2f}")
        print(f"   Confidence Level: {result.confidence_level:.2f}")
        print(f"   Relationships Found: {len(result.relationships)}")
        print(f"   Processing Time: {result.processing_time_ms:.1f}ms")
        
        if result.categorization_result:
            print(f"   Categories: {', '.join(result.categorization_result.assigned_categories)}")
            print(f"   Categorization Quality: {result.categorization_result.quality_score:.2f}")
        
        print(f"   Recommendations: {len(result.recommendations)}")
        for i, rec in enumerate(result.recommendations[:3], 1):
            print(f"     {i}. {rec}")
    
    elif args.analyze_item:
        print(f"🔍 Analyzing Intelligence for Item: {args.analyze_item}")
        # In a real implementation, would load actual item data
        print("Item analysis requires actual item data loading")
    
    elif args.analyze_database:
        print(f"📊 Analyzing Database Intelligence: {args.analyze_database}")
        
        analysis = coordinator.analyze_database_intelligence(args.analyze_database, max_items=20)
        
        if 'error' in analysis:
            print(f"❌ Error: {analysis['error']}")
        else:
            summary = analysis['database_summary']
            print(f"\\n📈 Database Analysis Results:")
            print(f"   Database: {summary['database_id']}")
            print(f"   Items Analyzed: {summary['total_items_analyzed']}")
            print(f"   Success Rate: {summary['success_rate']:.1f}%")
            print(f"   Average Intelligence Score: {summary['average_intelligence_score']:.2f}")
            print(f"   Processing Time: {summary['average_processing_time_ms']:.1f}ms avg")
            
            if 'top_items' in analysis:
                print(f"\\n🏆 Top Intelligent Items:")
                for item in analysis['top_items'][:3]:
                    print(f"     {item['item_id']}: {item['intelligence_score']:.2f}")
    
    elif args.cross_database:
        print("🌐 Performing Cross-Database Intelligence Analysis")
        
        analysis = coordinator.analyze_cross_database_intelligence(max_items_per_db=10)
        
        if 'error' in analysis:
            print(f"❌ Error: {analysis['error']}")
        else:
            summary = analysis['analysis_summary']
            print(f"\\n📊 Cross-Database Analysis Results:")
            print(f"   Databases Analyzed: {summary['databases_analyzed']}")
            print(f"   Total Items: {summary['total_items_analyzed']}")
            print(f"   Processing Time: {summary['processing_time_ms']:.1f}ms")
            
            if 'cross_database_insights' in analysis:
                print(f"\\n💡 Key Insights:")
                for insight in analysis['cross_database_insights'][:3]:
                    print(f"     • {insight}")
    
    elif args.stats:
        stats = coordinator.get_intelligence_statistics()
        print("📈 Intelligence System Statistics")
        print("=" * 50)
        
        system = stats["system_summary"]
        print(f"Total Analyses: {system['total_intelligence_analyses']}")
        print(f"Success Rate: {system['success_rate_percentage']:.1f}%")
        print(f"Average Intelligence Score: {system['average_intelligence_score']:.2f}")
        print(f"Average Processing Time: {system['average_processing_time_ms']:.1f}ms")
        print(f"Real-time Monitoring: {'Active' if system['real_time_monitoring_active'] else 'Inactive'}")
        
        # Component statistics
        cat_stats = stats["component_statistics"]["categorization"]
        if "performance_summary" in cat_stats:
            cat_perf = cat_stats["performance_summary"]
            print(f"\\n🏷️  Categorization Performance:")
            print(f"   Success Rate: {cat_perf['success_rate_percentage']:.1f}%")
            print(f"   Avg Quality: {cat_perf['average_quality_score']:.2f}")
        
        rel_stats = stats["component_statistics"]["relationship_discovery"]
        if "discovery_summary" in rel_stats:
            rel_disc = rel_stats["discovery_summary"]
            print(f"\\n🔗 Relationship Discovery:")
            print(f"   Total Relationships: {rel_disc['total_relationships']}")
            print(f"   Discovery Rate: {rel_disc['discovery_rate']:.1f}%")
        
        opt_stats = stats["component_statistics"]["predictive_optimization"]
        if "optimization_summary" in opt_stats:
            opt_sum = opt_stats["optimization_summary"]
            print(f"\\n⚡ Optimization Performance:")
            print(f"   Patterns Discovered: {opt_sum['total_patterns_discovered']}")
            print(f"   Recommendations: {opt_sum['total_recommendations_generated']}")
    
    elif args.monitor:
        print(f"📡 Starting Real-time Intelligence Monitoring (interval: {args.monitor}s)")
        print("Press Ctrl+C to stop monitoring")
        
        try:
            coordinator.start_real_time_intelligence(args.monitor)
            
            # Keep running and display periodic stats
            import time
            while True:
                time.sleep(30)  # Show stats every 30 seconds
                stats = coordinator.get_intelligence_statistics()
                system = stats["system_summary"]
                print(f"\\r🔄 Active | Analyses: {system['total_intelligence_analyses']} | "
                      f"Avg Score: {system['average_intelligence_score']:.2f} | "
                      f"Success: {system['success_rate_percentage']:.1f}%", end="", flush=True)
                
        except KeyboardInterrupt:
            print("\\n\\n🛑 Stopping real-time intelligence monitoring")
            coordinator.stop_real_time_intelligence()
    
    else:
        print("🧠 Intelligence Coordinator - AI Agent Intelligence System")
        print("Integrates content categorization, relationship discovery, and predictive optimization")
        print("Use --help for available options")
        
        # Show basic system info
        stats = coordinator.get_intelligence_statistics()
        system = stats["system_summary"]
        print(f"\\nSystem Status:")
        print(f"  Real-time Monitoring: {'Active' if system['real_time_monitoring_active'] else 'Ready'}")
        print(f"  Components: Categorization + Relationships + Optimization")
        print(f"  Analysis History: {system['total_intelligence_analyses']} items")

if __name__ == "__main__":
    main()