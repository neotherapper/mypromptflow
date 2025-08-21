#!/usr/bin/env python3
"""
Noise Reduction Engine
Implements duplicate detection and spam filtering for the Universal Topic Intelligence System
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple, Set
from datetime import datetime, timedelta
import json
import logging
import hashlib
import re
import math
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from enum import Enum

from .universal_source_monitor import ContentItem

class NoiseType(Enum):
    """Types of noise that can be detected"""
    DUPLICATE_EXACT = "duplicate_exact"      # Exact duplicate content
    DUPLICATE_NEAR = "duplicate_near"        # Near-duplicate content
    SPAM_PROMOTIONAL = "spam_promotional"    # Promotional spam content
    SPAM_CLICKBAIT = "spam_clickbait"       # Clickbait content
    LOW_QUALITY = "low_quality"             # Low quality content
    REPETITIVE = "repetitive"               # Repetitive/template content
    OFF_TOPIC = "off_topic"                 # Content not matching topics
    BROKEN_CONTENT = "broken_content"        # Malformed or broken content

class FilterAction(Enum):
    """Actions to take on noisy content"""
    ALLOW = "allow"          # Let content through
    DEMOTE = "demote"        # Lower priority but keep
    QUARANTINE = "quarantine" # Hold for manual review
    REJECT = "reject"        # Block completely

@dataclass
class NoiseDetectionResult:
    """Result of noise detection analysis"""
    content_id: str
    noise_types: List[NoiseType]
    confidence_scores: Dict[NoiseType, float]  # 0-1 confidence for each noise type
    overall_noise_score: float  # 0-1 overall noise level
    filter_action: FilterAction
    similar_content_ids: List[str]  # IDs of similar/duplicate content
    reasoning: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class DuplicateCluster:
    """Cluster of similar/duplicate content items"""
    cluster_id: str
    representative_id: str  # Best item in cluster
    content_ids: List[str]
    similarity_scores: Dict[Tuple[str, str], float]
    cluster_quality_score: float
    creation_time: datetime

class NoiseReductionEngine:
    """
    Core engine for noise reduction and content filtering
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize noise reduction engine
        
        Args:
            config: Configuration for noise reduction parameters
        """
        self.config = config or self._default_config()
        self.logger = logging.getLogger("NoiseReduction")
        
        # Content storage and duplicate tracking
        self.content_cache: Dict[str, ContentItem] = {}
        self.duplicate_clusters: Dict[str, DuplicateCluster] = {}
        self.content_fingerprints: Dict[str, str] = {}  # content_id -> fingerprint
        self.url_seen: Set[str] = set()
        self.title_patterns: Dict[str, List[str]] = defaultdict(list)  # pattern -> content_ids
        
        # Noise detection history
        self.noise_history: List[NoiseDetectionResult] = []
        self.spam_patterns: Set[str] = set()
        
        # Initialize filters
        self._init_spam_patterns()
        self._init_quality_patterns()
    
    def _default_config(self) -> Dict[str, Any]:
        """Default configuration for noise reduction"""
        return {
            "duplicate_thresholds": {
                "exact_similarity": 0.95,      # 95%+ similarity = exact duplicate
                "near_similarity": 0.80,       # 80%+ similarity = near duplicate
                "title_similarity": 0.90,      # 90%+ title similarity
                "content_min_length": 50,      # Minimum content length to check
                "url_similarity": 0.85         # 85%+ URL similarity
            },
            "spam_thresholds": {
                "promotional_keywords": 5,      # Max promotional keywords
                "clickbait_score": 0.3,        # Max clickbait score (lowered for testing)
                "repetitive_threshold": 0.4,   # Max repetitiveness (lowered for testing)
                "quality_min_score": 0.3       # Minimum quality score
            },
            "filter_actions": {
                "duplicate_exact": FilterAction.REJECT,
                "duplicate_near": FilterAction.DEMOTE,
                "spam_promotional": FilterAction.QUARANTINE,
                "spam_clickbait": FilterAction.DEMOTE,
                "low_quality": FilterAction.DEMOTE,
                "repetitive": FilterAction.QUARANTINE,
                "off_topic": FilterAction.DEMOTE,
                "broken_content": FilterAction.REJECT
            },
            "cache_limits": {
                "max_content_cache": 10000,    # Maximum content items to cache
                "max_clusters": 1000,          # Maximum duplicate clusters
                "history_days": 30              # Keep noise history for 30 days
            }
        }
    
    def _init_spam_patterns(self):
        """Initialize spam detection patterns"""
        self.spam_patterns = {
            # Promotional language
            "promotional": {
                "buy now", "limited time", "special offer", "click here", "subscribe now",
                "get rich quick", "make money", "earn $", "free trial", "discount",
                "hot deal", "exclusive", "limited edition", "act now", "hurry"
            },
            # Clickbait indicators
            "clickbait": {
                "you won't believe", "shocking", "amazing secret", "doctors hate",
                "this one trick", "will blow your mind", "the truth about", "exposed",
                "incredible", "unbelievable", "jaw-dropping", "life-changing", "must see"
            },
            # Low quality indicators  
            "low_quality": {
                "first post", "please like", "smash that", "don't forget to subscribe",
                "like and subscribe", "hit the bell", "check description", "link in bio"
            }
        }
    
    def _init_quality_patterns(self):
        """Initialize quality assessment patterns"""
        self.quality_indicators = {
            # High quality indicators
            "high_quality": {
                "tutorial", "guide", "documentation", "analysis", "research",
                "comprehensive", "detailed", "step-by-step", "best practices",
                "performance", "architecture", "implementation", "case study"
            },
            # Technical indicators
            "technical": {
                "algorithm", "optimization", "framework", "library", "api",
                "database", "scalability", "security", "testing", "deployment"
            }
        }
    
    def analyze_content(self, content: ContentItem) -> NoiseDetectionResult:
        """
        Analyze content for noise and determine filtering action
        
        Args:
            content: Content item to analyze
            
        Returns:
            Noise detection result with filtering recommendation
        """
        noise_types = []
        confidence_scores = {}
        similar_content = []
        
        # Store content in cache for future comparison
        self.content_cache[content.item_id] = content
        self._cleanup_cache()
        
        # 1. Check for exact duplicates
        exact_duplicate, exact_similar = self._check_exact_duplicates(content)
        if exact_duplicate:
            noise_types.append(NoiseType.DUPLICATE_EXACT)
            confidence_scores[NoiseType.DUPLICATE_EXACT] = 1.0
            similar_content.extend(exact_similar)
        
        # 2. Check for near duplicates
        near_duplicate, near_similar, near_confidence = self._check_near_duplicates(content)
        if near_duplicate:
            noise_types.append(NoiseType.DUPLICATE_NEAR)
            confidence_scores[NoiseType.DUPLICATE_NEAR] = near_confidence
            similar_content.extend(near_similar)
        
        # 3. Check for spam content
        spam_types = self._check_spam_content(content)
        for spam_type, spam_confidence in spam_types.items():
            noise_types.append(spam_type)
            confidence_scores[spam_type] = spam_confidence
        
        # 4. Check content quality
        quality_issues = self._check_content_quality(content)
        for quality_issue, quality_confidence in quality_issues.items():
            noise_types.append(quality_issue)
            confidence_scores[quality_issue] = quality_confidence
        
        # 5. Calculate overall noise score
        overall_noise_score = self._calculate_overall_noise_score(confidence_scores)
        
        # 6. Determine filter action
        filter_action = self._determine_filter_action(noise_types, overall_noise_score)
        
        # 7. Generate reasoning
        reasoning = self._generate_noise_reasoning(noise_types, confidence_scores, filter_action)
        
        # Create result
        result = NoiseDetectionResult(
            content_id=content.item_id,
            noise_types=noise_types,
            confidence_scores=confidence_scores,
            overall_noise_score=overall_noise_score,
            filter_action=filter_action,
            similar_content_ids=similar_content,
            reasoning=reasoning,
            metadata={
                "analysis_timestamp": datetime.now(),
                "source_type": content.metadata.get("mcp_source_type", "rss"),
                "content_length": len(content.content or ""),
                "title_length": len(content.title),
                "url": content.url
            }
        )
        
        # Store in history
        self.noise_history.append(result)
        self._cleanup_history()
        
        # Update duplicate clusters if needed
        if NoiseType.DUPLICATE_NEAR in noise_types or NoiseType.DUPLICATE_EXACT in noise_types:
            self._update_duplicate_clusters(content, similar_content, overall_noise_score)
        
        self.logger.debug(f"Noise analysis for {content.item_id}: {len(noise_types)} issues, "
                         f"score {overall_noise_score:.3f}, action {filter_action.value}")
        
        return result
    
    def _check_exact_duplicates(self, content: ContentItem) -> Tuple[bool, List[str]]:
        """Check for exact duplicates"""
        similar_items = []
        
        # Check URL duplicates
        if content.url and content.url in self.url_seen:
            # Find items with same URL
            for cached_id, cached_content in self.content_cache.items():
                if cached_content.url == content.url and cached_id != content.item_id:
                    similar_items.append(cached_id)
            
            if similar_items:
                return True, similar_items
        
        # Add URL to seen set
        if content.url:
            self.url_seen.add(content.url)
        
        # Check content fingerprint
        fingerprint = self._generate_content_fingerprint(content)
        
        if fingerprint in self.content_fingerprints.values():
            # Find items with same fingerprint
            for cached_id, cached_fingerprint in self.content_fingerprints.items():
                if cached_fingerprint == fingerprint and cached_id != content.item_id:
                    similar_items.append(cached_id)
        
        # Store fingerprint
        self.content_fingerprints[content.item_id] = fingerprint
        
        return len(similar_items) > 0, similar_items
    
    def _check_near_duplicates(self, content: ContentItem) -> Tuple[bool, List[str], float]:
        """Check for near duplicates using similarity analysis"""
        thresholds = self.config["duplicate_thresholds"]
        similar_items = []
        max_similarity = 0.0
        
        # Skip if content is too short
        content_text = content.content or ""
        if len(content_text) < thresholds["content_min_length"]:
            return False, [], 0.0
        
        # Compare with cached content
        for cached_id, cached_content in self.content_cache.items():
            if cached_id == content.item_id:
                continue
            
            # Calculate similarity scores
            title_similarity = self._calculate_text_similarity(content.title, cached_content.title)
            content_similarity = self._calculate_text_similarity(content_text, cached_content.content or "")
            
            # Check URL similarity (for different URLs pointing to same content)
            url_similarity = 0.0
            if content.url and cached_content.url:
                url_similarity = self._calculate_text_similarity(content.url, cached_content.url)
            
            # Weighted similarity score
            overall_similarity = (
                title_similarity * 0.4 +
                content_similarity * 0.5 +
                url_similarity * 0.1
            )
            
            max_similarity = max(max_similarity, overall_similarity)
            
            # Check thresholds
            if (title_similarity >= thresholds["title_similarity"] or
                content_similarity >= thresholds["near_similarity"] or
                overall_similarity >= thresholds["near_similarity"]):
                similar_items.append(cached_id)
        
        is_duplicate = len(similar_items) > 0
        confidence = max_similarity if is_duplicate else 0.0
        
        return is_duplicate, similar_items, confidence
    
    def _check_spam_content(self, content: ContentItem) -> Dict[NoiseType, float]:
        """Check for various types of spam content"""
        spam_results = {}
        
        # Combine title and content for analysis
        full_text = f"{content.title} {content.content or ''}".lower()
        
        # Check promotional spam
        promotional_score = self._calculate_pattern_score(full_text, self.spam_patterns["promotional"])
        if promotional_score >= self.config["spam_thresholds"]["promotional_keywords"] / 10:
            spam_results[NoiseType.SPAM_PROMOTIONAL] = min(1.0, promotional_score)
        
        # Check clickbait
        clickbait_score = self._calculate_pattern_score(content.title.lower(), self.spam_patterns["clickbait"])
        if clickbait_score >= self.config["spam_thresholds"]["clickbait_score"]:
            spam_results[NoiseType.SPAM_CLICKBAIT] = min(1.0, clickbait_score)
        
        # Check repetitive content
        repetitive_score = self._calculate_repetitiveness(full_text)
        if repetitive_score >= self.config["spam_thresholds"]["repetitive_threshold"]:
            spam_results[NoiseType.REPETITIVE] = repetitive_score
        
        return spam_results
    
    def _check_content_quality(self, content: ContentItem) -> Dict[NoiseType, float]:
        """Check content quality indicators"""
        quality_results = {}
        
        full_text = f"{content.title} {content.content or ''}".lower()
        
        # Check low quality indicators
        low_quality_score = self._calculate_pattern_score(full_text, self.spam_patterns["low_quality"])
        if low_quality_score > 0:
            quality_results[NoiseType.LOW_QUALITY] = min(1.0, low_quality_score * 2)
        
        # Check for broken content
        if self._is_broken_content(content):
            quality_results[NoiseType.BROKEN_CONTENT] = 0.9
        
        # Check topic relevance (basic implementation)
        if content.topics:
            topic_relevance = self._check_topic_relevance(content)
            if topic_relevance < 0.3:
                quality_results[NoiseType.OFF_TOPIC] = 1.0 - topic_relevance
        
        return quality_results
    
    def _generate_content_fingerprint(self, content: ContentItem) -> str:
        """Generate a fingerprint for content deduplication"""
        # Normalize content for fingerprinting
        title = re.sub(r'[^\w\s]', '', content.title.lower())
        content_text = re.sub(r'[^\w\s]', '', (content.content or "").lower())
        
        # Create fingerprint from normalized content
        fingerprint_text = f"{title}|{content_text[:500]}"  # First 500 chars of content
        return hashlib.md5(fingerprint_text.encode()).hexdigest()
    
    def _calculate_text_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two text strings"""
        if not text1 or not text2:
            return 0.0
        
        # Normalize texts
        text1 = re.sub(r'[^\w\s]', '', text1.lower())
        text2 = re.sub(r'[^\w\s]', '', text2.lower())
        
        # Use SequenceMatcher for similarity
        return SequenceMatcher(None, text1, text2).ratio()
    
    def _calculate_pattern_score(self, text: str, patterns: Set[str]) -> float:
        """Calculate how much text matches spam patterns"""
        if not text or not patterns:
            return 0.0
        
        matches = sum(1 for pattern in patterns if pattern in text)
        return matches / len(patterns)
    
    def _calculate_repetitiveness(self, text: str) -> float:
        """Calculate repetitiveness score of text"""
        if not text or len(text) < 100:
            return 0.0
        
        # Split into sentences and check for repetition
        sentences = [s.strip() for s in text.split('.') if len(s.strip()) > 10]
        
        if len(sentences) < 3:
            return 0.0
        
        # Calculate similarity between sentences
        total_similarity = 0.0
        comparisons = 0
        
        for i in range(len(sentences)):
            for j in range(i + 1, len(sentences)):
                similarity = self._calculate_text_similarity(sentences[i], sentences[j])
                total_similarity += similarity
                comparisons += 1
        
        if comparisons == 0:
            return 0.0
        
        return total_similarity / comparisons
    
    def _is_broken_content(self, content: ContentItem) -> bool:
        """Check if content appears broken or malformed"""
        # Check for very short title
        if len(content.title) < 5:
            return True
        
        # Check for malformed URLs
        if content.url and not (content.url.startswith('http') or content.url.startswith('https')):
            return True
        
        # Check for excessive special characters
        if content.content:
            special_char_ratio = len(re.findall(r'[^\w\s]', content.content)) / len(content.content)
            if special_char_ratio > 0.3:  # More than 30% special characters
                return True
        
        # Check for missing essential fields
        if not content.author and not content.source_id:
            return True
        
        return False
    
    def _check_topic_relevance(self, content: ContentItem) -> float:
        """Check how relevant content is to its assigned topics"""
        if not content.topics:
            return 0.5  # Neutral if no topics
        
        # Simple relevance check based on topic keywords in content
        full_text = f"{content.title} {content.content or ''}".lower()
        
        total_relevance = 0.0
        for topic in content.topics:
            topic_words = topic.lower().split()
            topic_matches = sum(1 for word in topic_words if word in full_text)
            topic_relevance = topic_matches / len(topic_words) if topic_words else 0
            total_relevance += topic_relevance
        
        return min(1.0, total_relevance / len(content.topics))
    
    def _calculate_overall_noise_score(self, confidence_scores: Dict[NoiseType, float]) -> float:
        """Calculate overall noise score from individual confidence scores"""
        if not confidence_scores:
            return 0.0
        
        # Weight different noise types
        weights = {
            NoiseType.DUPLICATE_EXACT: 1.0,
            NoiseType.DUPLICATE_NEAR: 0.7,
            NoiseType.SPAM_PROMOTIONAL: 0.9,
            NoiseType.SPAM_CLICKBAIT: 0.6,
            NoiseType.LOW_QUALITY: 0.5,
            NoiseType.REPETITIVE: 0.8,
            NoiseType.OFF_TOPIC: 0.4,
            NoiseType.BROKEN_CONTENT: 1.0
        }
        
        weighted_sum = 0.0
        total_weight = 0.0
        
        for noise_type, confidence in confidence_scores.items():
            weight = weights.get(noise_type, 0.5)
            weighted_sum += confidence * weight
            total_weight += weight
        
        return weighted_sum / total_weight if total_weight > 0 else 0.0
    
    def _determine_filter_action(self, noise_types: List[NoiseType], noise_score: float) -> FilterAction:
        """Determine what action to take based on noise analysis"""
        if not noise_types:
            return FilterAction.ALLOW
        
        # Check for immediate rejection criteria
        if NoiseType.DUPLICATE_EXACT in noise_types or NoiseType.BROKEN_CONTENT in noise_types:
            return FilterAction.REJECT
        
        # Check for quarantine criteria
        if (NoiseType.SPAM_PROMOTIONAL in noise_types or 
            NoiseType.REPETITIVE in noise_types or
            noise_score >= 0.8):
            return FilterAction.QUARANTINE
        
        # Check for demotion criteria
        if noise_score >= 0.4:
            return FilterAction.DEMOTE
        
        return FilterAction.ALLOW
    
    def _generate_noise_reasoning(self, noise_types: List[NoiseType], 
                                confidence_scores: Dict[NoiseType, float], 
                                action: FilterAction) -> str:
        """Generate human-readable reasoning for noise decision"""
        if not noise_types:
            return f"Content passed noise filter - Action: {action.value}"
        
        issues = []
        for noise_type in noise_types:
            confidence = confidence_scores.get(noise_type, 0.0)
            issues.append(f"{noise_type.value} (confidence: {confidence:.2f})")
        
        issues_str = ", ".join(issues)
        return f"Noise detected: {issues_str} - Action: {action.value}"
    
    def _update_duplicate_clusters(self, content: ContentItem, similar_content: List[str], noise_score: float):
        """Update duplicate clusters with new content"""
        if not similar_content:
            return
        
        # Find or create cluster
        cluster_id = None
        for existing_cluster_id, cluster in self.duplicate_clusters.items():
            if any(content_id in cluster.content_ids for content_id in similar_content):
                cluster_id = existing_cluster_id
                break
        
        if cluster_id is None:
            # Create new cluster
            cluster_id = f"cluster_{len(self.duplicate_clusters)}"
            representative_id = similar_content[0]  # Choose first as representative
            
            self.duplicate_clusters[cluster_id] = DuplicateCluster(
                cluster_id=cluster_id,
                representative_id=representative_id,
                content_ids=similar_content + [content.item_id],
                similarity_scores={},
                cluster_quality_score=1.0 - noise_score,
                creation_time=datetime.now()
            )
        else:
            # Add to existing cluster
            cluster = self.duplicate_clusters[cluster_id]
            cluster.content_ids.append(content.item_id)
            cluster.cluster_quality_score = min(cluster.cluster_quality_score, 1.0 - noise_score)
    
    def _cleanup_cache(self):
        """Clean up content cache to maintain performance"""
        max_cache = self.config["cache_limits"]["max_content_cache"]
        
        if len(self.content_cache) > max_cache:
            # Remove oldest entries
            items = list(self.content_cache.items())
            items_to_remove = items[:len(items) - max_cache]
            
            for content_id, _ in items_to_remove:
                del self.content_cache[content_id]
                if content_id in self.content_fingerprints:
                    del self.content_fingerprints[content_id]
    
    def _cleanup_history(self):
        """Clean up noise detection history"""
        max_age = timedelta(days=self.config["cache_limits"]["history_days"])
        cutoff_time = datetime.now() - max_age
        
        self.noise_history = [
            result for result in self.noise_history 
            if result.metadata.get("analysis_timestamp", datetime.now()) >= cutoff_time
        ]
    
    def should_filter_content(self, content: ContentItem) -> Tuple[bool, NoiseDetectionResult]:
        """
        Main interface: determine if content should be filtered
        
        Args:
            content: Content item to evaluate
            
        Returns:
            (should_filter, detection_result) tuple
        """
        result = self.analyze_content(content)
        
        should_filter = result.filter_action in [FilterAction.REJECT, FilterAction.QUARANTINE]
        
        return should_filter, result
    
    def get_noise_statistics(self) -> Dict[str, Any]:
        """Get statistics about noise detection performance"""
        if not self.noise_history:
            return {
                "total_analyzed": 0,
                "noise_detected": 0,
                "filter_actions": {},
                "noise_types": {},
                "average_noise_score": 0.0
            }
        
        total = len(self.noise_history)
        noisy_items = [r for r in self.noise_history if r.noise_types]
        
        # Count filter actions
        filter_actions = Counter(r.filter_action.value for r in self.noise_history)
        
        # Count noise types
        noise_types = Counter()
        for result in self.noise_history:
            for noise_type in result.noise_types:
                noise_types[noise_type.value] += 1
        
        # Calculate average noise score
        avg_noise_score = sum(r.overall_noise_score for r in self.noise_history) / total
        
        return {
            "total_analyzed": total,
            "noise_detected": len(noisy_items),
            "noise_detection_rate": f"{len(noisy_items)/total*100:.1f}%",
            "filter_actions": dict(filter_actions),
            "noise_types": dict(noise_types.most_common()),
            "average_noise_score": avg_noise_score,
            "duplicate_clusters": len(self.duplicate_clusters),
            "cached_content": len(self.content_cache)
        }