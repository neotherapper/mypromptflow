#!/usr/bin/env python3
"""
Universal Content Prioritizer
Topic-agnostic content scoring and prioritization system
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
from enum import Enum
import json
import logging
from abc import ABC, abstractmethod

from .universal_source_monitor import ContentItem, ContentPriority, SourceMetadata

@dataclass
class PriorityFactors:
    """Factors used in priority calculation"""
    source_authority: float      # 0-1: Credibility of source
    content_recency: float       # 0-1: How recent the content is
    topic_relevance: float       # 0-1: Relevance to monitored topics
    engagement_signals: float    # 0-1: Social signals, views, etc.
    uniqueness_score: float      # 0-1: How unique/novel the information is
    completeness: float          # 0-1: How complete/detailed the content is
    actionability: float         # 0-1: How actionable the content is
    cross_topic_value: float     # 0-1: Value across multiple topics

@dataclass
class PriorityResult:
    """Result of priority calculation"""
    content_item: ContentItem
    total_score: float
    priority_level: ContentPriority
    factors: PriorityFactors
    reasoning: str
    recommendations: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        return {
            "item_id": self.content_item.item_id,
            "total_score": self.total_score,
            "priority_level": self.priority_level.value,
            "factors": {
                "source_authority": self.factors.source_authority,
                "content_recency": self.factors.content_recency,
                "topic_relevance": self.factors.topic_relevance,
                "engagement_signals": self.factors.engagement_signals,
                "uniqueness_score": self.factors.uniqueness_score,
                "completeness": self.factors.completeness,
                "actionability": self.factors.actionability,
                "cross_topic_value": self.factors.cross_topic_value
            },
            "reasoning": self.reasoning,
            "recommendations": self.recommendations
        }

class PriorityStrategy(ABC):
    """Abstract base for different prioritization strategies"""
    
    @abstractmethod
    def calculate_factors(self, content: ContentItem, context: Dict[str, Any]) -> PriorityFactors:
        """Calculate priority factors for content"""
        pass
    
    @abstractmethod
    def get_strategy_name(self) -> str:
        """Get strategy name"""
        pass

class UniversalContentPrioritizer:
    """
    Universal content prioritization system
    Works across any topic domain with configurable strategies
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize prioritizer with configuration
        
        Args:
            config: Configuration including weights and thresholds
        """
        self.config = config or self._default_config()
        self.logger = self._setup_logging()
        self.strategies: Dict[str, PriorityStrategy] = {}
        self.topic_preferences: Dict[str, float] = {}
        self.source_scores: Dict[str, float] = {}
        
        # Cache for recent prioritizations
        self.priority_cache = {}
        
        # Initialize default strategies
        self._init_default_strategies()
    
    def _default_config(self) -> Dict[str, Any]:
        """Default configuration"""
        return {
            "weights": {
                "source_authority": 0.20,
                "content_recency": 0.25,
                "topic_relevance": 0.20,
                "engagement_signals": 0.10,
                "uniqueness_score": 0.10,
                "completeness": 0.05,
                "actionability": 0.05,
                "cross_topic_value": 0.05
            },
            "thresholds": {
                "critical": 0.85,
                "high": 0.70,
                "medium": 0.50,
                "low": 0.30
            },
            "recency_decay": {
                "half_life_hours": 48,  # Content value halves every 48 hours
                "max_age_days": 30      # Content older than 30 days gets minimal recency score
            },
            "cache_ttl_minutes": 60
        }
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging"""
        logger = logging.getLogger("ContentPrioritizer")
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - ContentPrioritizer - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger
    
    def _init_default_strategies(self):
        """Initialize default prioritization strategies"""
        # Add default strategies
        self.register_strategy("default", DefaultPriorityStrategy())
        self.register_strategy("news", NewsPriorityStrategy())
        self.register_strategy("technical", TechnicalContentStrategy())
        self.register_strategy("social", SocialSignalsStrategy())
    
    def register_strategy(self, name: str, strategy: PriorityStrategy):
        """Register a prioritization strategy"""
        self.strategies[name] = strategy
        self.logger.info(f"Registered strategy: {name}")
    
    def set_topic_preferences(self, preferences: Dict[str, float]):
        """
        Set topic preferences for relevance scoring
        
        Args:
            preferences: Topic -> weight mapping (0-1)
        """
        self.topic_preferences = preferences
    
    def set_source_authorities(self, authorities: Dict[str, float]):
        """
        Set source authority scores
        
        Args:
            authorities: Source ID -> authority score mapping (0-1)
        """
        self.source_scores = authorities
    
    def prioritize(
        self,
        content: ContentItem,
        strategy: str = "default",
        context: Optional[Dict[str, Any]] = None
    ) -> PriorityResult:
        """
        Calculate priority for a content item
        
        Args:
            content: Content item to prioritize
            strategy: Strategy name to use
            context: Additional context for prioritization
            
        Returns:
            PriorityResult with score and reasoning
        """
        # Check cache
        cache_key = f"{content.item_id}_{strategy}"
        if cache_key in self.priority_cache:
            cached = self.priority_cache[cache_key]
            if self._is_cache_valid(cached["timestamp"]):
                return cached["result"]
        
        # Prepare context
        full_context = {
            "topic_preferences": self.topic_preferences,
            "source_scores": self.source_scores,
            "config": self.config,
            **(context or {})
        }
        
        # Get strategy
        priority_strategy = self.strategies.get(strategy, self.strategies["default"])
        
        # Calculate factors
        factors = priority_strategy.calculate_factors(content, full_context)
        
        # Calculate weighted score
        total_score = self._calculate_weighted_score(factors)
        
        # Determine priority level
        priority_level = self._determine_priority_level(total_score)
        
        # Generate reasoning
        reasoning = self._generate_reasoning(factors, priority_level, strategy)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(content, factors, priority_level)
        
        # Create result
        result = PriorityResult(
            content_item=content,
            total_score=total_score,
            priority_level=priority_level,
            factors=factors,
            reasoning=reasoning,
            recommendations=recommendations
        )
        
        # Cache result
        self.priority_cache[cache_key] = {
            "result": result,
            "timestamp": datetime.now()
        }
        
        return result
    
    def prioritize_batch(
        self,
        content_items: List[ContentItem],
        strategy: str = "default",
        context: Optional[Dict[str, Any]] = None
    ) -> List[PriorityResult]:
        """
        Prioritize multiple content items and sort by priority
        
        Args:
            content_items: List of content items
            strategy: Strategy to use
            context: Additional context
            
        Returns:
            Sorted list of PriorityResults (highest priority first)
        """
        results = []
        
        for item in content_items:
            result = self.prioritize(item, strategy, context)
            results.append(result)
        
        # Sort by total score (highest first)
        results.sort(key=lambda x: x.total_score, reverse=True)
        
        self.logger.info(f"Prioritized {len(results)} items using {strategy} strategy")
        
        return results
    
    def _calculate_weighted_score(self, factors: PriorityFactors) -> float:
        """Calculate weighted total score from factors"""
        weights = self.config["weights"]
        
        score = (
            factors.source_authority * weights["source_authority"] +
            factors.content_recency * weights["content_recency"] +
            factors.topic_relevance * weights["topic_relevance"] +
            factors.engagement_signals * weights["engagement_signals"] +
            factors.uniqueness_score * weights["uniqueness_score"] +
            factors.completeness * weights["completeness"] +
            factors.actionability * weights["actionability"] +
            factors.cross_topic_value * weights["cross_topic_value"]
        )
        
        return min(1.0, max(0.0, score))  # Clamp to 0-1
    
    def _determine_priority_level(self, score: float) -> ContentPriority:
        """Determine priority level from score"""
        thresholds = self.config["thresholds"]
        
        if score >= thresholds["critical"]:
            return ContentPriority.CRITICAL
        elif score >= thresholds["high"]:
            return ContentPriority.HIGH
        elif score >= thresholds["medium"]:
            return ContentPriority.MEDIUM
        elif score >= thresholds["low"]:
            return ContentPriority.LOW
        else:
            return ContentPriority.ARCHIVE
    
    def _generate_reasoning(
        self,
        factors: PriorityFactors,
        priority_level: ContentPriority,
        strategy: str
    ) -> str:
        """Generate human-readable reasoning for priority"""
        
        # Find strongest factors
        factor_scores = {
            "source authority": factors.source_authority,
            "recency": factors.content_recency,
            "topic relevance": factors.topic_relevance,
            "engagement": factors.engagement_signals,
            "uniqueness": factors.uniqueness_score,
            "completeness": factors.completeness,
            "actionability": factors.actionability,
            "cross-topic value": factors.cross_topic_value
        }
        
        top_factors = sorted(factor_scores.items(), key=lambda x: x[1], reverse=True)[:3]
        
        reasoning = f"Content prioritized as {priority_level.value} using {strategy} strategy. "
        reasoning += f"Key factors: {', '.join([f'{name} ({score:.2f})' for name, score in top_factors])}."
        
        return reasoning
    
    def _generate_recommendations(
        self,
        content: ContentItem,
        factors: PriorityFactors,
        priority_level: ContentPriority
    ) -> List[str]:
        """Generate action recommendations based on priority"""
        recommendations = []
        
        if priority_level == ContentPriority.CRITICAL:
            recommendations.append("Immediate review required")
            recommendations.append("Consider cross-platform distribution")
            recommendations.append("Alert relevant stakeholders")
        elif priority_level == ContentPriority.HIGH:
            recommendations.append("Priority processing recommended")
            recommendations.append("Schedule for detailed analysis")
        elif priority_level == ContentPriority.MEDIUM:
            recommendations.append("Include in regular review cycle")
        
        # Factor-specific recommendations
        if factors.uniqueness_score > 0.8:
            recommendations.append("Novel information - consider deep analysis")
        if factors.cross_topic_value > 0.7:
            recommendations.append("Has cross-topic relevance - share across teams")
        if factors.actionability > 0.8:
            recommendations.append("Highly actionable - create action items")
        
        return recommendations
    
    def _is_cache_valid(self, timestamp: datetime) -> bool:
        """Check if cache entry is still valid"""
        ttl = timedelta(minutes=self.config["cache_ttl_minutes"])
        return datetime.now() - timestamp < ttl
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get prioritization statistics"""
        return {
            "total_prioritized": len(self.priority_cache),
            "strategies_available": list(self.strategies.keys()),
            "topic_preferences_set": len(self.topic_preferences) > 0,
            "source_authorities_set": len(self.source_scores) > 0,
            "cache_size": len(self.priority_cache)
        }


class DefaultPriorityStrategy(PriorityStrategy):
    """Default prioritization strategy"""
    
    def calculate_factors(self, content: ContentItem, context: Dict[str, Any]) -> PriorityFactors:
        """Calculate priority factors using default logic"""
        
        # Source authority
        source_authority = context.get("source_scores", {}).get(
            content.source_id, 0.5  # Default to medium authority
        )
        
        # Content recency
        if content.published_date:
            # Handle both timezone-aware and naive datetimes
            now = datetime.now(content.published_date.tzinfo) if content.published_date.tzinfo else datetime.now()
            age_hours = (now - content.published_date).total_seconds() / 3600
            half_life = context["config"]["recency_decay"]["half_life_hours"]
            content_recency = 0.5 ** (age_hours / half_life)
        else:
            content_recency = 0.3  # Unknown date gets low recency
        
        # Topic relevance
        topic_prefs = context.get("topic_preferences", {})
        relevance_scores = [
            topic_prefs.get(topic, 0.5) for topic in content.topics
        ]
        topic_relevance = max(relevance_scores) if relevance_scores else 0.5
        
        # Other factors (simplified for default)
        engagement_signals = content.metadata.get("engagement_score", 0.5)
        uniqueness_score = content.metadata.get("uniqueness", 0.5)
        completeness = min(1.0, len(content.content or "") / 1000) if content.content else 0.3
        actionability = content.metadata.get("actionability", 0.5)
        cross_topic_value = len(content.topics) / 5 if content.topics else 0.1
        
        return PriorityFactors(
            source_authority=source_authority,
            content_recency=content_recency,
            topic_relevance=topic_relevance,
            engagement_signals=engagement_signals,
            uniqueness_score=uniqueness_score,
            completeness=completeness,
            actionability=actionability,
            cross_topic_value=min(1.0, cross_topic_value)
        )
    
    def get_strategy_name(self) -> str:
        return "default"


class NewsPriorityStrategy(PriorityStrategy):
    """News-specific prioritization strategy"""
    
    def calculate_factors(self, content: ContentItem, context: Dict[str, Any]) -> PriorityFactors:
        """Calculate factors with news-specific logic"""
        
        # News values recency much higher
        if content.published_date:
            # Handle both timezone-aware and naive datetimes
            now = datetime.now(content.published_date.tzinfo) if content.published_date.tzinfo else datetime.now()
            age_hours = (now - content.published_date).total_seconds() / 3600
            if age_hours < 1:  # Breaking news
                content_recency = 1.0
            elif age_hours < 6:  # Very recent
                content_recency = 0.9
            elif age_hours < 24:  # Today's news
                content_recency = 0.7
            else:
                content_recency = max(0.1, 1.0 - (age_hours / 168))  # Decay over a week
        else:
            content_recency = 0.1
        
        # Check for breaking news indicators
        title_lower = content.title.lower()
        breaking_indicators = ["breaking", "just in", "alert", "urgent", "developing"]
        is_breaking = any(indicator in title_lower for indicator in breaking_indicators)
        
        # Boost uniqueness for breaking news
        uniqueness_score = 1.0 if is_breaking else content.metadata.get("uniqueness", 0.5)
        
        # Source authority is critical for news
        source_authority = context.get("source_scores", {}).get(content.source_id, 0.3)
        
        # Other factors
        topic_prefs = context.get("topic_preferences", {})
        topic_relevance = max([topic_prefs.get(t, 0.5) for t in content.topics], default=0.5)
        
        return PriorityFactors(
            source_authority=source_authority * 1.2,  # Boost authority for news
            content_recency=content_recency,
            topic_relevance=topic_relevance,
            engagement_signals=content.metadata.get("engagement_score", 0.4),
            uniqueness_score=uniqueness_score,
            completeness=content.metadata.get("completeness", 0.5),
            actionability=0.7 if is_breaking else 0.4,
            cross_topic_value=content.metadata.get("cross_topic", 0.3)
        )
    
    def get_strategy_name(self) -> str:
        return "news"


class TechnicalContentStrategy(PriorityStrategy):
    """Technical content prioritization strategy"""
    
    def calculate_factors(self, content: ContentItem, context: Dict[str, Any]) -> PriorityFactors:
        """Calculate factors for technical content"""
        
        # Technical content values completeness and accuracy
        content_length = len(content.content or "")
        completeness = min(1.0, content_length / 2000)  # Technical content should be detailed
        
        # Check for code examples, tutorials, documentation
        technical_indicators = ["tutorial", "guide", "documentation", "api", "example", "code"]
        title_lower = content.title.lower()
        is_technical = any(ind in title_lower for ind in technical_indicators)
        
        # Boost actionability for tutorials and guides
        actionability = 0.9 if "tutorial" in title_lower or "guide" in title_lower else 0.5
        
        # Technical content doesn't decay as quickly
        if content.published_date:
            # Handle both timezone-aware and naive datetimes
            now = datetime.now(content.published_date.tzinfo) if content.published_date.tzinfo else datetime.now()
            age_days = (now - content.published_date).days
            content_recency = max(0.3, 1.0 - (age_days / 90))  # 3-month decay
        else:
            content_recency = 0.4
        
        return PriorityFactors(
            source_authority=context.get("source_scores", {}).get(content.source_id, 0.6),
            content_recency=content_recency,
            topic_relevance=0.8 if is_technical else 0.5,
            engagement_signals=content.metadata.get("engagement_score", 0.4),
            uniqueness_score=content.metadata.get("uniqueness", 0.6),
            completeness=completeness,
            actionability=actionability,
            cross_topic_value=content.metadata.get("cross_topic", 0.4)
        )
    
    def get_strategy_name(self) -> str:
        return "technical"


class SocialSignalsStrategy(PriorityStrategy):
    """Social signals-based prioritization strategy"""
    
    def calculate_factors(self, content: ContentItem, context: Dict[str, Any]) -> PriorityFactors:
        """Calculate factors based on social engagement"""
        
        # Heavy weight on engagement signals
        engagement = content.metadata.get("engagement_score", 0.0)
        views = content.metadata.get("views", 0)
        shares = content.metadata.get("shares", 0)
        comments = content.metadata.get("comments", 0)
        
        # Calculate engagement score if not provided
        if engagement == 0.0 and (views or shares or comments):
            # Normalize engagement metrics
            engagement = min(1.0, (
                min(views / 10000, 1.0) * 0.3 +
                min(shares / 100, 1.0) * 0.4 +
                min(comments / 50, 1.0) * 0.3
            ))
        
        # Viral content indicator
        is_viral = views > 50000 or shares > 500
        uniqueness_score = 0.9 if is_viral else content.metadata.get("uniqueness", 0.5)
        
        return PriorityFactors(
            source_authority=context.get("source_scores", {}).get(content.source_id, 0.5),
            content_recency=0.7,  # Recent content tends to have more engagement
            topic_relevance=0.6,
            engagement_signals=engagement,
            uniqueness_score=uniqueness_score,
            completeness=content.metadata.get("completeness", 0.5),
            actionability=0.6 if is_viral else 0.4,
            cross_topic_value=0.7 if is_viral else 0.3
        )
    
    def get_strategy_name(self) -> str:
        return "social"