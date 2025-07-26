#!/usr/bin/env python3
"""
Intelligent Relationship Discovery Engine
Provides AI-powered cross-database relationship detection with semantic similarity analysis
Achieves relationship discovery across 6 Knowledge Vault databases with strength scoring
"""

import os
import re
import yaml
import time
import logging
import hashlib
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass, asdict
from collections import Counter, defaultdict
import math

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class RelationshipResult:
    """Result of relationship discovery analysis"""
    source_item_id: str
    source_database: str
    target_item_id: str
    target_database: str
    relationship_type: str
    strength_score: float
    confidence_level: float
    discovery_reason: str
    bidirectional: bool
    validation_passed: bool
    created_timestamp: str

@dataclass
class SimilarityAnalysis:
    """Detailed similarity analysis between two items"""
    semantic_similarity: float
    tag_overlap_score: float
    content_similarity: float
    structural_similarity: float
    overall_similarity: float
    shared_elements: Dict[str, List[str]]

class IntelligentRelationshipDiscovery:
    """
    AI-powered relationship discovery engine with cross-database intelligence
    Detects relationships between items across different Knowledge Vault databases
    """
    
    def __init__(self, config_path: str = None):
        """Initialize the relationship discovery engine"""
        self.base_path = Path(__file__).parent.parent.parent
        self.config_path = config_path or self.base_path / "operations/intelligence/schemas/relationship_schema.yaml"
        
        # Load configurations
        self.config = self._load_config()
        
        # Initialize relationship components
        self.relationship_types = self._build_relationship_types()
        self.cross_db_rules = self._build_cross_database_rules()
        self.similarity_algorithms = self._initialize_similarity_algorithms()
        
        # Relationship storage and caching
        self.discovered_relationships = {}
        self.similarity_cache = {}
        self.relationship_history = []
        
        # Performance tracking
        self.discovery_metrics = {
            'total_comparisons': 0,
            'relationships_discovered': 0,
            'cache_hits': 0,
            'processing_time_total': 0
        }
        
        logger.info("Intelligent Relationship Discovery Engine initialized successfully")
    
    def discover_relationships(self, item_data: Dict[str, Any], database_id: str, 
                             target_items: List[Dict[str, Any]], 
                             target_databases: List[str]) -> List[RelationshipResult]:
        """
        Discover relationships between source item and target items across databases
        
        Args:
            item_data: Source item data dictionary
            database_id: Source database identifier
            target_items: List of potential target item data
            target_databases: List of target database identifiers
            
        Returns:
            List of RelationshipResult objects with discovered relationships
        """
        start_time = time.time()
        source_item_id = item_data.get('id', 'unknown')
        
        logger.debug(f"Discovering relationships for {source_item_id} against {len(target_items)} targets")
        
        discovered_relationships = []
        
        try:
            # Extract source item features
            source_features = self._extract_item_features(item_data)
            
            # Compare against each target item
            for target_item in target_items:
                target_item_id = target_item.get('id', 'unknown')
                target_db = self._determine_target_database(target_item, target_databases)
                
                if not target_db:
                    continue
                
                # Skip self-comparison
                if source_item_id == target_item_id and database_id == target_db:
                    continue
                
                # Check if relationship analysis is applicable for this database pair
                if not self._is_cross_database_analysis_applicable(database_id, target_db):
                    continue
                
                # Perform relationship analysis
                relationships = self._analyze_item_relationship(
                    item_data, source_features, database_id,
                    target_item, target_db
                )
                
                discovered_relationships.extend(relationships)
                self.discovery_metrics['total_comparisons'] += 1
            
            # Filter and validate relationships
            validated_relationships = self._validate_and_filter_relationships(discovered_relationships)
            
            # Update metrics
            processing_time = (time.time() - start_time) * 1000
            self.discovery_metrics['relationships_discovered'] += len(validated_relationships)
            self.discovery_metrics['processing_time_total'] += processing_time
            
            logger.debug(f"Discovered {len(validated_relationships)} relationships for {source_item_id} "
                        f"({processing_time:.1f}ms)")
            
            return validated_relationships
            
        except Exception as e:
            logger.error(f"Error discovering relationships for {source_item_id}: {e}")
            return []
    
    def analyze_cross_database_relationships(self, database_items: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
        """
        Analyze relationships across all databases comprehensively
        
        Args:
            database_items: Dictionary mapping database_id to list of items
            
        Returns:
            Comprehensive relationship analysis results
        """
        logger.info(f"Analyzing cross-database relationships across {len(database_items)} databases")
        start_time = time.time()
        
        all_relationships = []
        database_pairs_analyzed = 0
        
        # Analyze each database pair
        database_ids = list(database_items.keys())
        for i, source_db in enumerate(database_ids):
            source_items = database_items[source_db]
            
            for j, target_db in enumerate(database_ids):
                if i >= j:  # Skip duplicate pairs and self-comparison
                    continue
                
                target_items = database_items[target_db]
                database_pairs_analyzed += 1
                
                logger.debug(f"Analyzing {source_db} <-> {target_db} ({len(source_items)} x {len(target_items)})")
                
                # Analyze relationships between database pairs
                pair_relationships = self._analyze_database_pair_relationships(
                    source_items, source_db, target_items, target_db
                )
                
                all_relationships.extend(pair_relationships)
        
        # Generate comprehensive analysis
        analysis_results = self._generate_comprehensive_analysis(
            all_relationships, database_items, database_pairs_analyzed
        )
        
        processing_time = (time.time() - start_time) * 1000
        analysis_results['processing_time_ms'] = processing_time
        
        logger.info(f"Cross-database analysis completed: {len(all_relationships)} relationships "
                   f"across {database_pairs_analyzed} database pairs ({processing_time:.1f}ms)")
        
        return analysis_results
    
    def get_item_relationships(self, item_id: str, database_id: str, 
                             relationship_types: List[str] = None) -> List[RelationshipResult]:
        """
        Get all discovered relationships for a specific item
        
        Args:
            item_id: Item identifier
            database_id: Database identifier
            relationship_types: Optional filter for relationship types
            
        Returns:
            List of RelationshipResult objects
        """
        item_key = f"{database_id}:{item_id}"
        relationships = self.discovered_relationships.get(item_key, [])
        
        # Filter by relationship types if specified
        if relationship_types:
            relationships = [r for r in relationships if r.relationship_type in relationship_types]
        
        return relationships
    
    def update_relationship_strength(self, source_item_id: str, source_db: str,
                                   target_item_id: str, target_db: str,
                                   new_strength: float, reason: str = "manual_update") -> bool:
        """
        Update the strength score of an existing relationship
        
        Args:
            source_item_id: Source item identifier
            source_db: Source database identifier
            target_item_id: Target item identifier  
            target_db: Target database identifier
            new_strength: New strength score (0.0 to 1.0)
            reason: Reason for the update
            
        Returns:
            True if relationship was updated successfully
        """
        try:
            # Find and update the relationship
            source_key = f"{source_db}:{source_item_id}"
            if source_key in self.discovered_relationships:
                for relationship in self.discovered_relationships[source_key]:
                    if (relationship.target_item_id == target_item_id and 
                        relationship.target_database == target_db):
                        
                        old_strength = relationship.strength_score
                        relationship.strength_score = new_strength
                        relationship.discovery_reason += f"; Updated: {reason}"
                        
                        logger.info(f"Updated relationship strength {source_item_id}->{target_item_id}: "
                                   f"{old_strength:.2f} -> {new_strength:.2f}")
                        return True
            
            logger.warning(f"Relationship not found for update: {source_item_id}->{target_item_id}")
            return False
            
        except Exception as e:
            logger.error(f"Error updating relationship strength: {e}")
            return False
    
    def get_discovery_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive relationship discovery statistics
        
        Returns:
            Dictionary with detailed performance and discovery metrics
        """
        total_relationships = sum(len(rels) for rels in self.discovered_relationships.values())
        
        # Relationship type distribution
        type_counts = Counter()
        strength_distribution = defaultdict(int)
        database_pair_counts = Counter()
        
        for relationships in self.discovered_relationships.values():
            for rel in relationships:
                type_counts[rel.relationship_type] += 1
                
                # Strength distribution
                if rel.strength_score >= 0.8:
                    strength_distribution['very_strong'] += 1
                elif rel.strength_score >= 0.7:
                    strength_distribution['strong'] += 1
                elif rel.strength_score >= 0.6:
                    strength_distribution['moderate'] += 1
                else:
                    strength_distribution['weak'] += 1
                
                # Database pair distribution
                pair_key = f"{rel.source_database}-{rel.target_database}"
                database_pair_counts[pair_key] += 1
        
        # Calculate performance metrics
        avg_processing_time = (self.discovery_metrics['processing_time_total'] / 
                              max(self.discovery_metrics['total_comparisons'], 1))
        
        return {
            "discovery_summary": {
                "total_relationships": total_relationships,
                "total_comparisons": self.discovery_metrics['total_comparisons'],
                "discovery_rate": (total_relationships / max(self.discovery_metrics['total_comparisons'], 1)) * 100,
                "cache_hit_rate": (self.discovery_metrics['cache_hits'] / 
                                 max(self.discovery_metrics['total_comparisons'], 1)) * 100,
                "average_processing_time_ms": avg_processing_time
            },
            "relationship_type_distribution": dict(type_counts.most_common()),
            "strength_distribution": dict(strength_distribution),
            "database_pair_distribution": dict(database_pair_counts.most_common()),
            "quality_metrics": {
                "high_confidence_relationships": len([r for rels in self.discovered_relationships.values() 
                                                    for r in rels if r.confidence_level >= 0.8]),
                "bidirectional_relationships": len([r for rels in self.discovered_relationships.values() 
                                                   for r in rels if r.bidirectional]),
                "validated_relationships": len([r for rels in self.discovered_relationships.values() 
                                              for r in rels if r.validation_passed])
            }
        }
    
    # Private helper methods
    
    def _load_config(self) -> Dict[str, Any]:
        """Load relationship discovery configuration"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Error loading relationship config: {e}")
            return {}
    
    def _build_relationship_types(self) -> Dict[str, Any]:
        """Build relationship types configuration"""
        return self.config.get('relationship_types', {})
    
    def _build_cross_database_rules(self) -> Dict[str, Any]:
        """Build cross-database relationship rules"""
        return self.config.get('cross_database_rules', {})
    
    def _initialize_similarity_algorithms(self) -> Dict[str, Any]:
        """Initialize similarity analysis algorithms"""
        return self.config.get('semantic_similarity', {})
    
    def _extract_item_features(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract features from item data for relationship analysis"""
        features = {
            'title': item_data.get('name', '').lower(),
            'description': item_data.get('description', '').lower(),
            'tags': [tag.lower() for tag in item_data.get('tags', [])],
            'category': item_data.get('category', '').lower(),
            'url': item_data.get('url', '').lower(),
            
            # Derived features
            'title_words': set(self._tokenize_text(item_data.get('name', ''))),
            'description_words': set(self._tokenize_text(item_data.get('description', ''))),
            'url_domain': self._extract_url_domain(item_data.get('url', '')),
            'content_length': len(item_data.get('description', '')),
            'tag_count': len(item_data.get('tags', [])),
            
            # Semantic vectors (simplified representation)
            'semantic_vector': self._create_semantic_vector(item_data)
        }
        
        return features
    
    def _tokenize_text(self, text: str) -> List[str]:
        """Tokenize text into meaningful words"""
        if not text:
            return []
        
        # Convert to lowercase and extract words
        text = text.lower()
        words = re.findall(r'\\b\\w{3,}\\b', text)  # Words with 3+ characters
        
        # Basic stopword removal
        stopwords = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        words = [w for w in words if w not in stopwords]
        
        return words
    
    def _extract_url_domain(self, url: str) -> str:
        """Extract domain from URL"""
        if not url:
            return ''
        
        # Simple domain extraction
        if '://' in url:
            domain = url.split('://')[1].split('/')[0]
            return domain.replace('www.', '')
        
        return ''
    
    def _create_semantic_vector(self, item_data: Dict[str, Any]) -> List[float]:
        """Create a simple semantic vector representation of the item"""
        # This is a simplified implementation
        # In practice, you might use word embeddings or other NLP techniques
        
        text_content = f"{item_data.get('name', '')} {item_data.get('description', '')}"
        words = self._tokenize_text(text_content)
        
        # Create a simple bag-of-words vector (first 50 dimensions)
        common_words = ['ai', 'data', 'web', 'development', 'business', 'tool', 'service', 
                       'platform', 'software', 'app', 'api', 'database', 'cloud', 
                       'analytics', 'automation', 'integration', 'framework', 'library',
                       'productivity', 'collaboration', 'management', 'optimization',
                       'security', 'design', 'mobile', 'enterprise', 'startup',
                       'marketing', 'sales', 'customer', 'finance', 'insurance',
                       'maritime', 'fintech', 'saas', 'marketplace', 'ecommerce',
                       'education', 'health', 'legal', 'real', 'estate', 'property',
                       'machine', 'learning', 'javascript', 'python', 'react',
                       'node', 'vue', 'angular', 'docker', 'kubernetes']
        
        vector = []
        for word in common_words[:50]:  # Limit to 50 dimensions
            vector.append(1.0 if word in words else 0.0)
        
        return vector
    
    def _determine_target_database(self, target_item: Dict[str, Any], 
                                 target_databases: List[str]) -> Optional[str]:
        """Determine which database the target item belongs to"""
        # This is a simplified implementation
        # In practice, you might have more sophisticated database identification
        item_id = target_item.get('id', '')
        
        # Use simple heuristics or explicit database field
        if 'database_id' in target_item:
            return target_item['database_id']
        
        # Default to first available database
        return target_databases[0] if target_databases else None
    
    def _is_cross_database_analysis_applicable(self, source_db: str, target_db: str) -> bool:
        """Check if cross-database analysis is applicable for database pair"""
        pair_key = f"{source_db}_to_{target_db}"
        reverse_key = f"{target_db}_to_{source_db}"
        
        return (pair_key in self.cross_db_rules or 
                reverse_key in self.cross_db_rules)
    
    def _analyze_item_relationship(self, source_item: Dict[str, Any], source_features: Dict[str, Any],
                                 source_db: str, target_item: Dict[str, Any], 
                                 target_db: str) -> List[RelationshipResult]:
        """Analyze relationship between two specific items"""
        target_features = self._extract_item_features(target_item)
        
        # Perform similarity analysis
        similarity_analysis = self._calculate_similarity(source_features, target_features)
        
        # Determine applicable relationship types for this database pair
        applicable_types = self._get_applicable_relationship_types(source_db, target_db)
        
        discovered_relationships = []
        
        for rel_type in applicable_types:
            # Calculate relationship strength for this type
            strength_score = self._calculate_relationship_strength(
                similarity_analysis, rel_type, source_features, target_features
            )
            
            # Check if strength meets threshold
            rel_config = self.relationship_types.get(rel_type, {})
            threshold = rel_config.get('threshold', 0.7)
            
            if strength_score >= threshold:
                # Calculate confidence level
                confidence = self._calculate_confidence_level(
                    strength_score, similarity_analysis, rel_type
                )
                
                # Generate discovery reason
                reason = self._generate_discovery_reason(
                    similarity_analysis, rel_type, strength_score
                )
                
                # Create relationship result
                relationship = RelationshipResult(
                    source_item_id=source_item.get('id', 'unknown'),
                    source_database=source_db,
                    target_item_id=target_item.get('id', 'unknown'),
                    target_database=target_db,
                    relationship_type=rel_type,
                    strength_score=strength_score,
                    confidence_level=confidence,
                    discovery_reason=reason,
                    bidirectional=rel_config.get('bidirectional', True),
                    validation_passed=True,  # Will be validated later
                    created_timestamp=datetime.now().isoformat()
                )
                
                discovered_relationships.append(relationship)
        
        return discovered_relationships
    
    def _calculate_similarity(self, source_features: Dict[str, Any], 
                            target_features: Dict[str, Any]) -> SimilarityAnalysis:
        """Calculate comprehensive similarity between two items"""
        
        # Semantic similarity (using simple cosine similarity of vectors)
        semantic_sim = self._cosine_similarity(
            source_features['semantic_vector'], 
            target_features['semantic_vector']
        )
        
        # Tag overlap similarity
        source_tags = set(source_features['tags'])
        target_tags = set(target_features['tags'])
        tag_overlap = len(source_tags.intersection(target_tags)) / max(len(source_tags.union(target_tags)), 1)
        
        # Content similarity (Jaccard similarity of words)
        source_words = source_features['title_words'].union(source_features['description_words'])
        target_words = target_features['title_words'].union(target_features['description_words'])
        content_sim = len(source_words.intersection(target_words)) / max(len(source_words.union(target_words)), 1)
        
        # Structural similarity (based on content length, tag count, etc.)
        len_diff = abs(source_features['content_length'] - target_features['content_length'])
        max_len = max(source_features['content_length'], target_features['content_length'], 1)
        len_sim = 1.0 - (len_diff / max_len)
        
        tag_count_diff = abs(source_features['tag_count'] - target_features['tag_count'])
        max_tags = max(source_features['tag_count'], target_features['tag_count'], 1)
        tag_count_sim = 1.0 - (tag_count_diff / max_tags)
        
        structural_sim = (len_sim + tag_count_sim) / 2
        
        # Overall similarity (weighted combination)
        weights = self.similarity_algorithms.get('text_analysis', {})
        title_weight = weights.get('title_weight', 0.4)
        desc_weight = weights.get('description_weight', 0.4)
        tags_weight = weights.get('tags_weight', 0.2)
        
        overall_sim = (semantic_sim * title_weight + 
                      content_sim * desc_weight + 
                      tag_overlap * tags_weight)
        
        # Identify shared elements
        shared_elements = {
            'tags': list(source_tags.intersection(target_tags)),
            'words': list(source_words.intersection(target_words)),
            'url_domain': [source_features['url_domain']] if (
                source_features['url_domain'] and 
                source_features['url_domain'] == target_features['url_domain']
            ) else []
        }
        
        return SimilarityAnalysis(
            semantic_similarity=semantic_sim,
            tag_overlap_score=tag_overlap,
            content_similarity=content_sim,
            structural_similarity=structural_sim,
            overall_similarity=overall_sim,
            shared_elements=shared_elements
        )
    
    def _cosine_similarity(self, vector1: List[float], vector2: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        if not vector1 or not vector2 or len(vector1) != len(vector2):
            return 0.0
        
        # Calculate dot product
        dot_product = sum(a * b for a, b in zip(vector1, vector2))
        
        # Calculate magnitudes
        magnitude1 = math.sqrt(sum(a * a for a in vector1))
        magnitude2 = math.sqrt(sum(b * b for b in vector2))
        
        # Avoid division by zero
        if magnitude1 == 0 or magnitude2 == 0:
            return 0.0
        
        return dot_product / (magnitude1 * magnitude2)
    
    def _get_applicable_relationship_types(self, source_db: str, target_db: str) -> List[str]:
        """Get applicable relationship types for database pair"""
        pair_key = f"{source_db}_to_{target_db}"
        reverse_key = f"{target_db}_to_{source_db}"
        
        # Check both directions
        if pair_key in self.cross_db_rules:
            return self.cross_db_rules[pair_key].get('relationship_types', [])
        elif reverse_key in self.cross_db_rules:
            return self.cross_db_rules[reverse_key].get('relationship_types', [])
        
        # Default relationship types
        return ['semantic_similarity', 'tag_overlap']
    
    def _calculate_relationship_strength(self, similarity: SimilarityAnalysis, 
                                       rel_type: str, source_features: Dict[str, Any],
                                       target_features: Dict[str, Any]) -> float:
        """Calculate relationship strength score for specific type"""
        base_score = 0.0
        
        if rel_type == 'semantic_similarity':
            base_score = similarity.overall_similarity
        elif rel_type == 'tag_overlap':
            base_score = similarity.tag_overlap_score
        elif rel_type == 'complementary':
            # Items are complementary if they're related but not too similar
            base_score = similarity.overall_similarity * (1.0 - similarity.overall_similarity) * 2
        elif rel_type == 'alternative':
            # Items are alternatives if they're very similar
            base_score = similarity.overall_similarity if similarity.overall_similarity > 0.8 else 0.0
        elif rel_type == 'dependency':
            # Simplified dependency detection based on content patterns
            base_score = similarity.content_similarity * 0.8
        else:
            base_score = similarity.overall_similarity
        
        # Apply relationship type weight
        rel_config = self.relationship_types.get(rel_type, {})
        weight = rel_config.get('weight', 1.0)
        
        return min(base_score * weight, 1.0)
    
    def _calculate_confidence_level(self, strength_score: float, 
                                  similarity: SimilarityAnalysis, 
                                  rel_type: str) -> float:
        """Calculate confidence level for relationship"""
        # Base confidence from strength score
        confidence = strength_score
        
        # Adjust based on multiple similarity factors
        if similarity.semantic_similarity > 0.7 and similarity.tag_overlap_score > 0.5:
            confidence += 0.1  # Multiple strong indicators
        
        # Adjust based on shared elements
        shared_count = sum(len(elements) for elements in similarity.shared_elements.values())
        if shared_count > 3:
            confidence += 0.05
        
        return min(confidence, 1.0)
    
    def _generate_discovery_reason(self, similarity: SimilarityAnalysis, 
                                 rel_type: str, strength_score: float) -> str:
        """Generate human-readable reason for relationship discovery"""
        reasons = []
        
        if similarity.semantic_similarity > 0.7:
            reasons.append(f"High semantic similarity ({similarity.semantic_similarity:.2f})")
        
        if similarity.tag_overlap_score > 0.5:
            shared_tags = similarity.shared_elements.get('tags', [])
            reasons.append(f"Shared tags: {', '.join(shared_tags[:3])}")
        
        if similarity.content_similarity > 0.6:
            reasons.append(f"Similar content ({similarity.content_similarity:.2f})")
        
        if not reasons:
            reasons.append(f"Moderate {rel_type} indicators")
        
        return f"{rel_type.replace('_', ' ').title()}: {'; '.join(reasons)} (strength: {strength_score:.2f})"
    
    def _validate_and_filter_relationships(self, relationships: List[RelationshipResult]) -> List[RelationshipResult]:
        """Validate and filter discovered relationships"""
        validated = []
        
        validation_rules = self.config.get('validation_rules', {})
        min_strength = validation_rules.get('minimum_relationship_strength', 0.6)
        max_per_item = validation_rules.get('maximum_relationships_per_item', 20)
        
        # Filter by minimum strength
        strong_relationships = [r for r in relationships if r.strength_score >= min_strength]
        
        # Group by source item and limit count
        source_groups = defaultdict(list)
        for rel in strong_relationships:
            source_key = f"{rel.source_database}:{rel.source_item_id}"
            source_groups[source_key].append(rel)
        
        # Limit relationships per source item
        for source_key, source_rels in source_groups.items():
            # Sort by strength and take top relationships
            source_rels.sort(key=lambda x: x.strength_score, reverse=True)
            validated.extend(source_rels[:max_per_item])
            
            # Store in discovery cache
            self.discovered_relationships[source_key] = source_rels[:max_per_item]
        
        return validated
    
    def _analyze_database_pair_relationships(self, source_items: List[Dict[str, Any]], source_db: str,
                                           target_items: List[Dict[str, Any]], target_db: str) -> List[RelationshipResult]:
        """Analyze relationships between two database collections"""
        pair_relationships = []
        
        # Sample items if collections are too large (for performance)
        max_items_per_db = 100
        if len(source_items) > max_items_per_db:
            source_items = source_items[:max_items_per_db]
        if len(target_items) > max_items_per_db:
            target_items = target_items[:max_items_per_db]
        
        # Analyze each source item against target items
        for source_item in source_items:
            relationships = self.discover_relationships(
                source_item, source_db, target_items, [target_db]
            )
            pair_relationships.extend(relationships)
        
        return pair_relationships
    
    def _generate_comprehensive_analysis(self, all_relationships: List[RelationshipResult],
                                       database_items: Dict[str, List[Dict[str, Any]]],
                                       pairs_analyzed: int) -> Dict[str, Any]:
        """Generate comprehensive analysis results"""
        # Relationship statistics
        total_relationships = len(all_relationships)
        strong_relationships = [r for r in all_relationships if r.strength_score >= 0.8]
        
        # Database connectivity analysis
        connectivity_matrix = defaultdict(lambda: defaultdict(int))
        for rel in all_relationships:
            connectivity_matrix[rel.source_database][rel.target_database] += 1
        
        # Top relationships by strength
        top_relationships = sorted(all_relationships, key=lambda x: x.strength_score, reverse=True)[:10]
        
        return {
            "analysis_summary": {
                "total_relationships_discovered": total_relationships,
                "strong_relationships": len(strong_relationships),
                "database_pairs_analyzed": pairs_analyzed,
                "average_relationships_per_pair": total_relationships / max(pairs_analyzed, 1),
                "total_items_analyzed": sum(len(items) for items in database_items.values())
            },
            "connectivity_matrix": dict(connectivity_matrix),
            "top_relationships": [
                {
                    "source": f"{r.source_database}:{r.source_item_id}",
                    "target": f"{r.target_database}:{r.target_item_id}",
                    "type": r.relationship_type,
                    "strength": r.strength_score,
                    "reason": r.discovery_reason
                }
                for r in top_relationships
            ],
            "relationship_type_distribution": dict(Counter(r.relationship_type for r in all_relationships)),
            "database_coverage": {
                db_id: {
                    "total_items": len(items),
                    "items_with_relationships": len(set(
                        r.source_item_id for r in all_relationships if r.source_database == db_id
                    ))
                }
                for db_id, items in database_items.items()
            }
        }

def main():
    """Main function for testing and CLI operations"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Intelligent Relationship Discovery Engine')
    parser.add_argument('--test', action='store_true', help='Run relationship discovery test')
    parser.add_argument('--stats', action='store_true', help='Show discovery statistics')
    parser.add_argument('--analyze-pair', nargs=2, help='Analyze relationships between two databases')
    
    args = parser.parse_args()
    
    # Initialize relationship discovery engine
    discovery_engine = IntelligentRelationshipDiscovery()
    
    if args.test:
        print("🔗 Running Intelligent Relationship Discovery Test")
        
        # Test items
        source_item = {
            'id': 'react-001',
            'name': 'React Development Framework',
            'description': 'Modern JavaScript library for building user interfaces',
            'tags': ['javascript', 'frontend', 'web-development', 'ui'],
            'url': 'https://reactjs.org'
        }
        
        target_items = [
            {
                'id': 'vue-001',
                'name': 'Vue.js Framework',
                'description': 'Progressive JavaScript framework for building user interfaces',
                'tags': ['javascript', 'frontend', 'web-development', 'vue'],
                'url': 'https://vuejs.org'
            },
            {
                'id': 'nodejs-001',
                'name': 'Node.js Runtime',
                'description': 'JavaScript runtime built on Chrome V8 engine for server-side development',
                'tags': ['javascript', 'backend', 'server', 'runtime'],
                'url': 'https://nodejs.org'
            },
            {
                'id': 'notion-001',
                'name': 'Notion Workspace',
                'description': 'All-in-one workspace for notes and collaboration',
                'tags': ['productivity', 'collaboration', 'notes'],
                'url': 'https://notion.so'
            }
        ]
        
        relationships = discovery_engine.discover_relationships(
            source_item, 'tools_services', target_items, ['tools_services', 'platforms_sites']
        )
        
        print(f"\\n📊 Discovered {len(relationships)} relationships:")
        for rel in relationships:
            print(f"   {rel.source_item_id} -> {rel.target_item_id}")
            print(f"   Type: {rel.relationship_type}, Strength: {rel.strength_score:.2f}")
            print(f"   Reason: {rel.discovery_reason}")
            print()
    
    elif args.stats:
        stats = discovery_engine.get_discovery_statistics()
        print("📈 Relationship Discovery Statistics")
        print("=" * 50)
        
        summary = stats["discovery_summary"]
        print(f"Total Relationships: {summary['total_relationships']}")
        print(f"Total Comparisons: {summary['total_comparisons']}")
        print(f"Discovery Rate: {summary['discovery_rate']:.1f}%")
        print(f"Cache Hit Rate: {summary['cache_hit_rate']:.1f}%")
        print(f"Avg Processing Time: {summary['average_processing_time_ms']:.1f}ms")
        
        print(f"\\n🔗 Relationship Types:")
        for rel_type, count in stats["relationship_type_distribution"].items():
            print(f"  {rel_type}: {count}")
        
        print(f"\\n💪 Strength Distribution:")
        for strength, count in stats["strength_distribution"].items():
            print(f"  {strength}: {count}")
    
    else:
        print("Intelligent Relationship Discovery Engine")
        print("Use --help for available options")

if __name__ == "__main__":
    main()