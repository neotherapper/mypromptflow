#!/usr/bin/env python3
"""
Trend Detection Engine
Implements velocity tracking and emergence detection for the Universal Topic Intelligence System
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple, Set
from datetime import datetime, timedelta
from enum import Enum
import json
import logging
import math
from collections import defaultdict, Counter
from abc import ABC, abstractmethod

from .universal_source_monitor import ContentItem

class TrendType(Enum):
    """Types of trends that can be detected"""
    EMERGING = "emerging"        # New topic gaining attention
    ACCELERATING = "accelerating"  # Existing topic gaining momentum
    VIRAL = "viral"              # Rapid spread/popularity
    DECLINING = "declining"      # Topic losing interest
    STABLE = "stable"            # Consistent interest level
    SEASONAL = "seasonal"        # Cyclical pattern
    BREAKING = "breaking"        # Sudden spike in activity

class TrendStrength(Enum):
    """Strength levels for detected trends"""
    WEAK = "weak"          # 1.0-2.0x baseline
    MODERATE = "moderate"  # 2.0-4.0x baseline
    STRONG = "strong"      # 4.0-8.0x baseline
    EXTREME = "extreme"    # 8.0x+ baseline

@dataclass
class TrendSignal:
    """Individual trend signal data point"""
    timestamp: datetime
    topic: str
    value: float              # Metric value (views, mentions, etc.)
    source_type: str          # youtube, github, search, rss
    source_id: str
    content_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TrendPattern:
    """Detected trend pattern"""
    topic: str
    trend_type: TrendType
    trend_strength: TrendStrength
    velocity: float           # Rate of change
    acceleration: float       # Rate of velocity change
    baseline: float           # Historical average
    current_value: float      # Latest measurement
    confidence: float         # 0-1 confidence in detection
    duration_hours: float     # How long trend has been active
    peak_value: float         # Highest value in trend
    contributing_sources: List[str]  # Sources driving the trend
    key_content: List[str]    # Most significant content items
    emergence_score: float    # How "new" this trend is (0-1)
    prediction_horizon: float # Hours ahead we can predict
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class TrendAnalysisResult:
    """Complete trend analysis result"""
    analysis_timestamp: datetime
    detected_trends: List[TrendPattern]
    topic_velocities: Dict[str, float]
    emergence_candidates: List[str]
    declining_topics: List[str]
    viral_content: List[str]
    analysis_window_hours: float
    total_signals_analyzed: int
    confidence_score: float

class TrendDetectionEngine:
    """
    Core engine for trend detection and velocity analysis
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize trend detection engine
        
        Args:
            config: Configuration for trend detection parameters
        """
        self.config = config or self._default_config()
        self.logger = logging.getLogger("TrendDetection")
        
        # Signal storage and processing
        self.signal_history: List[TrendSignal] = []
        self.topic_baselines: Dict[str, float] = {}
        self.trend_cache: Dict[str, TrendPattern] = {}
        
        # Analysis windows (in hours)
        self.analysis_windows = {
            "immediate": 1,      # 1 hour - breaking news
            "short": 6,          # 6 hours - daily trends  
            "medium": 24,        # 24 hours - weekly trends
            "long": 168,         # 1 week - longer patterns
            "baseline": 720      # 30 days - baseline calculation
        }
        
        # Initialize trend detection algorithms
        self._init_detectors()
    
    def _default_config(self) -> Dict[str, Any]:
        """Default configuration for trend detection"""
        return {
            "velocity_thresholds": {
                "weak": 1.5,      # 1.5x baseline = weak trend
                "moderate": 2.5,   # 2.5x baseline = moderate trend  
                "strong": 4.0,     # 4.0x baseline = strong trend
                "extreme": 8.0     # 8.0x baseline = extreme trend
            },
            "emergence_thresholds": {
                "min_signals": 2,        # Minimum signals to detect emergence
                "min_sources": 1,        # Minimum different sources (lowered for testing)
                "novelty_threshold": 0.5, # How "new" topic must be (lowered for testing)
                "growth_rate": 1.5       # Minimum growth rate (lowered for testing)
            },
            "viral_thresholds": {
                "min_velocity": 5.0,     # Minimum velocity for viral
                "min_acceleration": 2.0,  # Minimum acceleration
                "time_window": 6         # Hours to achieve viral status
            },
            "confidence_weights": {
                "signal_count": 0.3,     # More signals = higher confidence
                "source_diversity": 0.3,  # More sources = higher confidence
                "pattern_consistency": 0.2, # Consistent pattern = higher confidence
                "historical_accuracy": 0.2  # Past accuracy = higher confidence
            },
            "signal_decay": {
                "half_life_hours": 24,   # Signal value halves every 24 hours
                "max_age_days": 30       # Keep signals for 30 days max
            }
        }
    
    def _init_detectors(self):
        """Initialize trend detection algorithms"""
        self.detectors = {
            "velocity": VelocityDetector(self.config),
            "emergence": EmergenceDetector(self.config),
            "viral": ViralDetector(self.config),
            "seasonal": SeasonalDetector(self.config)
        }
    
    def add_content_signal(self, content: ContentItem, priority_score: float) -> TrendSignal:
        """
        Convert a content item into a trend signal and add to analysis
        
        Args:
            content: Content item to analyze
            priority_score: Priority score from intelligent scoring system
            
        Returns:
            Generated trend signal
        """
        # Extract trend-relevant metrics from content
        signal_value = self._calculate_signal_value(content, priority_score)
        source_type = content.metadata.get("mcp_source_type", "rss")
        
        # Create trend signal - use content published date for more realistic trend analysis
        signal_timestamp = content.published_date if content.published_date else datetime.now()
        
        signal = TrendSignal(
            timestamp=signal_timestamp,
            topic=content.topics[0] if content.topics else "general",
            value=signal_value,
            source_type=source_type,
            source_id=content.source_id,
            content_id=content.item_id,
            metadata={
                "title": content.title,
                "priority_score": priority_score,
                "engagement_data": self._extract_engagement_data(content),
                "author": content.author,
                "url": content.url
            }
        )
        
        # Add to signal history
        self.signal_history.append(signal)
        
        # Maintain signal history size
        self._cleanup_old_signals()
        
        self.logger.debug(f"Added trend signal for topic '{signal.topic}' with value {signal_value:.3f}")
        
        return signal
    
    def _calculate_signal_value(self, content: ContentItem, priority_score: float) -> float:
        """Calculate trend signal value from content metrics"""
        
        base_value = priority_score  # Start with intelligent priority score
        
        # Enhance based on source type and engagement
        source_type = content.metadata.get("mcp_source_type", "rss")
        
        if source_type == "youtube_transcript":
            # YouTube: amplify based on engagement
            views = content.metadata.get("youtube_view_count", 0)
            likes = content.metadata.get("youtube_like_count", 0)
            
            # Normalize view count (log scale)
            view_factor = math.log10(max(1, views)) / 6  # 1M views = 1.0
            engagement_factor = likes / max(1, views) * 100  # Like rate percentage
            
            base_value += view_factor * 0.3 + engagement_factor * 0.2
            
        elif source_type == "github_repository":
            # GitHub: amplify based on stars and activity
            stars = content.metadata.get("github_stars", 0)
            forks = content.metadata.get("github_forks", 0)
            
            # Normalize metrics
            star_factor = math.log10(max(1, stars)) / 5  # 100K stars = 1.0
            fork_factor = math.log10(max(1, forks)) / 4  # 10K forks = 1.0
            
            base_value += star_factor * 0.4 + fork_factor * 0.2
            
        elif source_type == "web_search":
            # Web search: amplify based on ranking and relevance
            rank = content.metadata.get("search_rank", 10)
            relevance = content.metadata.get("search_relevance_score", 0.5)
            
            # Higher ranking and relevance = higher signal
            rank_factor = max(0, (11 - rank) / 10)  # Top 10 results
            base_value += rank_factor * 0.3 + relevance * 0.2
        
        # Recency boost (newer content gets higher signal value)
        if content.published_date:
            now = datetime.now(content.published_date.tzinfo) if content.published_date.tzinfo else datetime.now()
            hours_old = (now - content.published_date).total_seconds() / 3600
            recency_factor = max(0, 1 - (hours_old / 24))  # Decays over 24 hours
            base_value += recency_factor * 0.3
        
        # Ensure bounded result
        return min(2.0, max(0.1, base_value))
    
    def _extract_engagement_data(self, content: ContentItem) -> Dict[str, Any]:
        """Extract engagement metrics for trend analysis"""
        engagement = {}
        
        source_type = content.metadata.get("mcp_source_type", "rss")
        
        if source_type == "youtube_transcript":
            engagement = {
                "views": content.metadata.get("youtube_view_count", 0),
                "likes": content.metadata.get("youtube_like_count", 0),
                "channel": content.metadata.get("youtube_channel", ""),
                "duration": content.metadata.get("youtube_duration", "")
            }
        elif source_type == "github_repository":
            engagement = {
                "stars": content.metadata.get("github_stars", 0),
                "forks": content.metadata.get("github_forks", 0),
                "issues": content.metadata.get("github_open_issues", 0),
                "language": content.metadata.get("github_language", "")
            }
        elif source_type == "web_search":
            engagement = {
                "rank": content.metadata.get("search_rank", 0),
                "relevance": content.metadata.get("search_relevance_score", 0),
                "domain": content.metadata.get("search_domain", "")
            }
        
        return engagement
    
    def _cleanup_old_signals(self):
        """Remove old signals to maintain performance"""
        max_age = timedelta(days=self.config["signal_decay"]["max_age_days"])
        
        # Handle timezone-aware vs naive datetime comparison
        now = datetime.now()
        if self.signal_history and self.signal_history[0].timestamp.tzinfo:
            # If signals have timezone info, make now timezone-aware
            now = datetime.now(self.signal_history[0].timestamp.tzinfo)
        
        cutoff_time = now - max_age
        
        original_count = len(self.signal_history)
        self.signal_history = [s for s in self.signal_history if s.timestamp >= cutoff_time]
        
        removed_count = original_count - len(self.signal_history)
        if removed_count > 0:
            self.logger.debug(f"Removed {removed_count} old signals (older than {max_age.days} days)")
    
    def analyze_trends(self, analysis_window: str = "medium") -> TrendAnalysisResult:
        """
        Perform comprehensive trend analysis
        
        Args:
            analysis_window: Time window for analysis ("immediate", "short", "medium", "long")
            
        Returns:
            Complete trend analysis results
        """
        window_hours = self.analysis_windows.get(analysis_window, 24)
        
        # Handle timezone-aware vs naive datetime comparison
        now = datetime.now()
        if self.signal_history and self.signal_history[0].timestamp.tzinfo:
            # If signals have timezone info, make now timezone-aware
            now = datetime.now(self.signal_history[0].timestamp.tzinfo)
        
        cutoff_time = now - timedelta(hours=window_hours)
        
        # Filter signals to analysis window
        relevant_signals = [s for s in self.signal_history if s.timestamp >= cutoff_time]
        
        if not relevant_signals:
            return TrendAnalysisResult(
                analysis_timestamp=datetime.now(),
                detected_trends=[],
                topic_velocities={},
                emergence_candidates=[],
                declining_topics=[],
                viral_content=[],
                analysis_window_hours=window_hours,
                total_signals_analyzed=0,
                confidence_score=0.0
            )
        
        # Update baselines using longer window
        self._update_baselines()
        
        # Run individual detectors
        detected_trends = []
        
        for detector_name, detector in self.detectors.items():
            try:
                trends = detector.detect_trends(relevant_signals, self.topic_baselines)
                detected_trends.extend(trends)
                self.logger.debug(f"{detector_name} detector found {len(trends)} trends")
            except Exception as e:
                self.logger.error(f"Error in {detector_name} detector: {e}")
        
        # Calculate additional metrics
        topic_velocities = self._calculate_topic_velocities(relevant_signals)
        emergence_candidates = self._identify_emergence_candidates(relevant_signals)
        declining_topics = self._identify_declining_topics(relevant_signals)
        viral_content = self._identify_viral_content(relevant_signals)
        
        # Calculate overall confidence
        confidence_score = self._calculate_analysis_confidence(detected_trends, relevant_signals)
        
        result = TrendAnalysisResult(
            analysis_timestamp=datetime.now(),
            detected_trends=detected_trends,
            topic_velocities=topic_velocities,
            emergence_candidates=emergence_candidates,
            declining_topics=declining_topics,
            viral_content=viral_content,
            analysis_window_hours=window_hours,
            total_signals_analyzed=len(relevant_signals),
            confidence_score=confidence_score
        )
        
        self.logger.info(f"Trend analysis complete: {len(detected_trends)} trends detected from {len(relevant_signals)} signals")
        
        return result
    
    def _update_baselines(self):
        """Update topic baselines using historical data"""
        baseline_window = timedelta(hours=self.analysis_windows["baseline"])
        
        # Handle timezone-aware vs naive datetime comparison
        now = datetime.now()
        if self.signal_history and self.signal_history[0].timestamp.tzinfo:
            # If signals have timezone info, make now timezone-aware
            now = datetime.now(self.signal_history[0].timestamp.tzinfo)
        
        cutoff_time = now - baseline_window
        
        # Get baseline signals
        baseline_signals = [s for s in self.signal_history if s.timestamp >= cutoff_time]
        
        # Calculate average signal value per topic
        topic_signals = defaultdict(list)
        for signal in baseline_signals:
            topic_signals[signal.topic].append(signal.value)
        
        # Update baselines
        for topic, values in topic_signals.items():
            if len(values) >= 5:  # Need minimum signals for reliable baseline
                self.topic_baselines[topic] = sum(values) / len(values)
            else:
                # Use global average if insufficient data
                all_values = [s.value for s in baseline_signals]
                self.topic_baselines[topic] = sum(all_values) / len(all_values) if all_values else 0.5
        
        self.logger.debug(f"Updated baselines for {len(self.topic_baselines)} topics")
    
    def _calculate_topic_velocities(self, signals: List[TrendSignal]) -> Dict[str, float]:
        """Calculate velocity (rate of change) for each topic"""
        topic_velocities = {}
        
        # Group signals by topic
        topic_signals = defaultdict(list)
        for signal in signals:
            topic_signals[signal.topic].append(signal)
        
        # Calculate velocity for each topic
        for topic, topic_signal_list in topic_signals.items():
            if len(topic_signal_list) < 2:
                topic_velocities[topic] = 0.0
                continue
            
            # Sort by timestamp
            topic_signal_list.sort(key=lambda x: x.timestamp)
            
            # Calculate velocity using linear regression or simple slope
            velocity = self._calculate_velocity_slope(topic_signal_list)
            topic_velocities[topic] = velocity
        
        return topic_velocities
    
    def _calculate_velocity_slope(self, signals: List[TrendSignal]) -> float:
        """Calculate velocity slope for a list of signals"""
        if len(signals) < 2:
            return 0.0
        
        # Convert timestamps to hours from first signal
        start_time = signals[0].timestamp
        x_values = [(s.timestamp - start_time).total_seconds() / 3600 for s in signals]
        y_values = [s.value for s in signals]
        
        # Simple linear regression for slope
        n = len(signals)
        sum_x = sum(x_values)
        sum_y = sum(y_values)
        sum_xy = sum(x * y for x, y in zip(x_values, y_values))
        sum_x2 = sum(x * x for x in x_values)
        
        # Avoid division by zero
        denominator = n * sum_x2 - sum_x * sum_x
        if abs(denominator) < 0.001:
            return 0.0
        
        # Calculate slope (velocity)
        slope = (n * sum_xy - sum_x * sum_y) / denominator
        
        return slope
    
    def _identify_emergence_candidates(self, signals: List[TrendSignal]) -> List[str]:
        """Identify topics that are emerging (new and growing)"""
        emergence_config = self.config["emergence_thresholds"]
        candidates = []
        
        # Group by topic
        topic_signals = defaultdict(list)
        for signal in signals:
            topic_signals[signal.topic].append(signal)
        
        for topic, topic_signal_list in topic_signals.items():
            # Check emergence criteria
            signal_count = len(topic_signal_list)
            source_count = len(set(s.source_id for s in topic_signal_list))
            
            if signal_count >= emergence_config["min_signals"] and source_count >= emergence_config["min_sources"]:
                # Check if topic is "new" (low baseline)
                baseline = self.topic_baselines.get(topic, 0.5)
                current_average = sum(s.value for s in topic_signal_list) / len(topic_signal_list)
                
                # Check growth rate
                if current_average / baseline >= emergence_config["growth_rate"]:
                    candidates.append(topic)
        
        return candidates
    
    def _identify_declining_topics(self, signals: List[TrendSignal]) -> List[str]:
        """Identify topics that are declining"""
        declining = []
        
        topic_signals = defaultdict(list)
        for signal in signals:
            topic_signals[signal.topic].append(signal)
        
        for topic, topic_signal_list in topic_signals.items():
            if len(topic_signal_list) < 3:  # Need enough data
                continue
            
            # Sort by timestamp
            topic_signal_list.sort(key=lambda x: x.timestamp)
            
            # Calculate trend slope
            slope = self._calculate_velocity_slope(topic_signal_list)
            
            # Negative slope indicates decline
            if slope < -0.1:  # Threshold for decline
                declining.append(topic)
        
        return declining
    
    def _identify_viral_content(self, signals: List[TrendSignal]) -> List[str]:
        """Identify content that has gone viral"""
        viral_config = self.config["viral_thresholds"]
        viral = []
        
        # Group by content
        content_signals = defaultdict(list)
        for signal in signals:
            content_signals[signal.content_id].append(signal)
        
        for content_id, content_signal_list in content_signals.items():
            if len(content_signal_list) < 2:
                continue
            
            # Sort by timestamp
            content_signal_list.sort(key=lambda x: x.timestamp)
            
            # Check time window
            time_span = (content_signal_list[-1].timestamp - content_signal_list[0].timestamp).total_seconds() / 3600
            
            if time_span <= viral_config["time_window"]:
                # Calculate velocity and acceleration
                velocity = self._calculate_velocity_slope(content_signal_list)
                
                if velocity >= viral_config["min_velocity"]:
                    viral.append(content_id)
        
        return viral
    
    def _calculate_analysis_confidence(self, trends: List[TrendPattern], signals: List[TrendSignal]) -> float:
        """Calculate confidence score for the analysis"""
        if not trends or not signals:
            return 0.0
        
        weights = self.config["confidence_weights"]
        
        # Signal count factor (more signals = higher confidence)
        signal_factor = min(1.0, len(signals) / 100)  # 100 signals = max confidence
        
        # Source diversity factor
        unique_sources = len(set(s.source_id for s in signals))
        diversity_factor = min(1.0, unique_sources / 10)  # 10 sources = max confidence
        
        # Pattern consistency (placeholder - could be enhanced)
        consistency_factor = 0.7  # Fixed for now
        
        # Historical accuracy (placeholder - would need tracking)
        accuracy_factor = 0.8  # Fixed for now
        
        # Weighted average
        confidence = (
            signal_factor * weights["signal_count"] +
            diversity_factor * weights["source_diversity"] +
            consistency_factor * weights["pattern_consistency"] +
            accuracy_factor * weights["historical_accuracy"]
        )
        
        return confidence
    
    def get_trend_summary(self, window: str = "medium") -> Dict[str, Any]:
        """Get a summary of current trends"""
        analysis = self.analyze_trends(window)
        
        return {
            "timestamp": analysis.analysis_timestamp.isoformat(),
            "analysis_window_hours": analysis.analysis_window_hours,
            "total_trends": len(analysis.detected_trends),
            "trends_by_type": Counter(t.trend_type.value for t in analysis.detected_trends),
            "trends_by_strength": Counter(t.trend_strength.value for t in analysis.detected_trends),
            "top_emerging": analysis.emergence_candidates[:5],
            "top_declining": analysis.declining_topics[:5],
            "viral_content_count": len(analysis.viral_content),
            "confidence_score": analysis.confidence_score,
            "total_signals_analyzed": analysis.total_signals_analyzed,
            "active_topics": len(analysis.topic_velocities)
        }


# Individual trend detectors

class TrendDetector(ABC):
    """Abstract base class for trend detectors"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(f"TrendDetector.{self.__class__.__name__}")
    
    @abstractmethod
    def detect_trends(self, signals: List[TrendSignal], baselines: Dict[str, float]) -> List[TrendPattern]:
        """Detect trends in the given signals"""
        pass


class VelocityDetector(TrendDetector):
    """Detects trends based on velocity (rate of change)"""
    
    def detect_trends(self, signals: List[TrendSignal], baselines: Dict[str, float]) -> List[TrendPattern]:
        trends = []
        
        # Group signals by topic
        topic_signals = defaultdict(list)
        for signal in signals:
            topic_signals[signal.topic].append(signal)
        
        for topic, topic_signal_list in topic_signals.items():
            if len(topic_signal_list) < 2:  # Need minimum signals (lowered for testing)
                continue
            
            # Sort by timestamp
            topic_signal_list.sort(key=lambda x: x.timestamp)
            
            # Calculate metrics
            baseline = baselines.get(topic, 0.5)
            current_value = sum(s.value for s in topic_signal_list[-3:]) / 3  # Average of last 3
            velocity = self._calculate_velocity(topic_signal_list)
            acceleration = self._calculate_acceleration(topic_signal_list)
            
            # Determine trend type and strength
            trend_type, trend_strength = self._classify_velocity_trend(velocity, baseline, current_value)
            
            if trend_type != TrendType.STABLE:
                # Calculate additional metrics
                duration = (topic_signal_list[-1].timestamp - topic_signal_list[0].timestamp).total_seconds() / 3600
                confidence = self._calculate_velocity_confidence(topic_signal_list, velocity)
                
                trend = TrendPattern(
                    topic=topic,
                    trend_type=trend_type,
                    trend_strength=trend_strength,
                    velocity=velocity,
                    acceleration=acceleration,
                    baseline=baseline,
                    current_value=current_value,
                    confidence=confidence,
                    duration_hours=duration,
                    peak_value=max(s.value for s in topic_signal_list),
                    contributing_sources=list(set(s.source_id for s in topic_signal_list)),
                    key_content=self._get_key_content(topic_signal_list),
                    emergence_score=self._calculate_emergence_score(baseline, current_value),
                    prediction_horizon=12.0,  # Can predict 12 hours ahead
                    metadata={"detector": "velocity", "signal_count": len(topic_signal_list)}
                )
                
                trends.append(trend)
        
        return trends
    
    def _calculate_velocity(self, signals: List[TrendSignal]) -> float:
        """Calculate velocity using linear regression"""
        if len(signals) < 2:
            return 0.0
        
        start_time = signals[0].timestamp
        x_values = [(s.timestamp - start_time).total_seconds() / 3600 for s in signals]
        y_values = [s.value for s in signals]
        
        # Linear regression
        n = len(signals)
        sum_x = sum(x_values)
        sum_y = sum(y_values)
        sum_xy = sum(x * y for x, y in zip(x_values, y_values))
        sum_x2 = sum(x * x for x in x_values)
        
        denominator = n * sum_x2 - sum_x * sum_x
        if abs(denominator) < 0.001:
            return 0.0
        
        return (n * sum_xy - sum_x * sum_y) / denominator
    
    def _calculate_acceleration(self, signals: List[TrendSignal]) -> float:
        """Calculate acceleration (change in velocity)"""
        if len(signals) < 4:
            return 0.0
        
        # Split into two halves and calculate velocity for each
        mid = len(signals) // 2
        first_half = signals[:mid+1]
        second_half = signals[mid:]
        
        velocity_1 = self._calculate_velocity(first_half)
        velocity_2 = self._calculate_velocity(second_half)
        
        return velocity_2 - velocity_1
    
    def _classify_velocity_trend(self, velocity: float, baseline: float, current_value: float) -> Tuple[TrendType, TrendStrength]:
        """Classify trend type and strength based on velocity"""
        thresholds = self.config["velocity_thresholds"]
        
        # Determine strength
        ratio = current_value / baseline if baseline > 0 else 1.0
        
        if ratio >= thresholds["extreme"]:
            strength = TrendStrength.EXTREME
        elif ratio >= thresholds["strong"]:
            strength = TrendStrength.STRONG
        elif ratio >= thresholds["moderate"]:
            strength = TrendStrength.MODERATE
        elif ratio >= thresholds["weak"]:
            strength = TrendStrength.WEAK
        else:
            strength = TrendStrength.WEAK
        
        # Determine type
        if velocity > 0.2:
            if ratio > 3.0:
                trend_type = TrendType.VIRAL
            elif baseline < 0.3:
                trend_type = TrendType.EMERGING
            else:
                trend_type = TrendType.ACCELERATING
        elif velocity < -0.1:
            trend_type = TrendType.DECLINING
        else:
            trend_type = TrendType.STABLE
        
        return trend_type, strength
    
    def _calculate_velocity_confidence(self, signals: List[TrendSignal], velocity: float) -> float:
        """Calculate confidence in velocity measurement"""
        # More signals = higher confidence
        signal_confidence = min(1.0, len(signals) / 10)
        
        # Consistent trend = higher confidence
        values = [s.value for s in signals]
        variance = sum((v - sum(values)/len(values))**2 for v in values) / len(values)
        consistency_confidence = max(0.0, 1.0 - variance)
        
        # Stronger velocity = higher confidence
        velocity_confidence = min(1.0, abs(velocity))
        
        return (signal_confidence + consistency_confidence + velocity_confidence) / 3
    
    def _get_key_content(self, signals: List[TrendSignal]) -> List[str]:
        """Get most significant content items"""
        # Sort by signal value and return top content IDs
        signals_sorted = sorted(signals, key=lambda x: x.value, reverse=True)
        return [s.content_id for s in signals_sorted[:3]]
    
    def _calculate_emergence_score(self, baseline: float, current_value: float) -> float:
        """Calculate how "emergent" a topic is"""
        if baseline <= 0:
            return 1.0  # Completely new topic
        
        # Low baseline + high current = high emergence
        emergence = (current_value / baseline) * (1 - min(1.0, baseline))
        return min(1.0, emergence / 5)  # Normalize


class EmergenceDetector(TrendDetector):
    """Detects emerging topics and new trends"""
    
    def detect_trends(self, signals: List[TrendSignal], baselines: Dict[str, float]) -> List[TrendPattern]:
        trends = []
        emergence_config = self.config["emergence_thresholds"]
        
        # Group by topic
        topic_signals = defaultdict(list)
        for signal in signals:
            topic_signals[signal.topic].append(signal)
        
        for topic, topic_signal_list in topic_signals.items():
            signal_count = len(topic_signal_list)
            source_count = len(set(s.source_id for s in topic_signal_list))
            
            # Check basic emergence criteria
            if signal_count < emergence_config["min_signals"]:
                continue
            if source_count < emergence_config["min_sources"]:
                continue
            
            baseline = baselines.get(topic, 0.1)  # Low baseline for new topics
            current_average = sum(s.value for s in topic_signal_list) / len(topic_signal_list)
            
            # Calculate novelty and growth
            novelty_score = 1.0 - min(1.0, baseline / 0.5)  # How "new" the topic is
            growth_rate = current_average / baseline if baseline > 0 else float('inf')
            
            # Check emergence thresholds
            if novelty_score >= emergence_config["novelty_threshold"] and growth_rate >= emergence_config["growth_rate"]:
                # Calculate additional metrics
                topic_signal_list.sort(key=lambda x: x.timestamp)
                velocity = self._calculate_simple_velocity(topic_signal_list)
                duration = (topic_signal_list[-1].timestamp - topic_signal_list[0].timestamp).total_seconds() / 3600
                
                trend = TrendPattern(
                    topic=topic,
                    trend_type=TrendType.EMERGING,
                    trend_strength=self._classify_emergence_strength(growth_rate),
                    velocity=velocity,
                    acceleration=0.0,  # Not calculated for emergence
                    baseline=baseline,
                    current_value=current_average,
                    confidence=min(1.0, novelty_score * (signal_count / 10)),
                    duration_hours=duration,
                    peak_value=max(s.value for s in topic_signal_list),
                    contributing_sources=list(set(s.source_id for s in topic_signal_list)),
                    key_content=[s.content_id for s in sorted(topic_signal_list, key=lambda x: x.value, reverse=True)[:3]],
                    emergence_score=novelty_score,
                    prediction_horizon=6.0,  # Shorter prediction for emerging topics
                    metadata={
                        "detector": "emergence", 
                        "novelty_score": novelty_score,
                        "growth_rate": growth_rate,
                        "signal_count": signal_count,
                        "source_count": source_count
                    }
                )
                
                trends.append(trend)
        
        return trends
    
    def _calculate_simple_velocity(self, signals: List[TrendSignal]) -> float:
        """Simple velocity calculation for emergence detection"""
        if len(signals) < 2:
            return 0.0
        
        # Average change per hour
        total_change = signals[-1].value - signals[0].value
        duration_hours = (signals[-1].timestamp - signals[0].timestamp).total_seconds() / 3600
        
        return total_change / max(1, duration_hours)
    
    def _classify_emergence_strength(self, growth_rate: float) -> TrendStrength:
        """Classify strength of emergence"""
        if growth_rate >= 10:
            return TrendStrength.EXTREME
        elif growth_rate >= 5:
            return TrendStrength.STRONG
        elif growth_rate >= 3:
            return TrendStrength.MODERATE
        else:
            return TrendStrength.WEAK


class ViralDetector(TrendDetector):
    """Detects viral content and rapid spread patterns"""
    
    def detect_trends(self, signals: List[TrendSignal], baselines: Dict[str, float]) -> List[TrendPattern]:
        trends = []
        viral_config = self.config["viral_thresholds"]
        
        # Group by content (not topic) for viral detection
        content_signals = defaultdict(list)
        for signal in signals:
            content_signals[signal.content_id].append(signal)
        
        for content_id, content_signal_list in content_signals.items():
            if len(content_signal_list) < 2:
                continue
            
            content_signal_list.sort(key=lambda x: x.timestamp)
            
            # Check time window for viral spread
            duration = (content_signal_list[-1].timestamp - content_signal_list[0].timestamp).total_seconds() / 3600
            if duration > viral_config["time_window"]:
                continue
            
            # Calculate metrics
            velocity = abs(content_signal_list[-1].value - content_signal_list[0].value) / max(1, duration)
            peak_value = max(s.value for s in content_signal_list)
            
            # Check viral thresholds
            if velocity >= viral_config["min_velocity"]:
                topic = content_signal_list[0].topic
                baseline = baselines.get(topic, 0.5)
                
                trend = TrendPattern(
                    topic=topic,
                    trend_type=TrendType.VIRAL,
                    trend_strength=self._classify_viral_strength(velocity, peak_value),
                    velocity=velocity,
                    acceleration=0.0,
                    baseline=baseline,
                    current_value=peak_value,
                    confidence=min(1.0, velocity / 10),  # Higher velocity = higher confidence
                    duration_hours=duration,
                    peak_value=peak_value,
                    contributing_sources=list(set(s.source_id for s in content_signal_list)),
                    key_content=[content_id],
                    emergence_score=0.5,  # Viral content may not be emerging topic
                    prediction_horizon=3.0,  # Short prediction window for viral
                    metadata={
                        "detector": "viral",
                        "content_id": content_id,
                        "viral_velocity": velocity,
                        "spread_duration": duration
                    }
                )
                
                trends.append(trend)
        
        return trends
    
    def _classify_viral_strength(self, velocity: float, peak_value: float) -> TrendStrength:
        """Classify strength of viral trend"""
        if velocity >= 20 or peak_value >= 2.0:
            return TrendStrength.EXTREME
        elif velocity >= 10 or peak_value >= 1.5:
            return TrendStrength.STRONG
        elif velocity >= 5 or peak_value >= 1.2:
            return TrendStrength.MODERATE
        else:
            return TrendStrength.WEAK


class SeasonalDetector(TrendDetector):
    """Detects seasonal and cyclical patterns (placeholder for future enhancement)"""
    
    def detect_trends(self, signals: List[TrendSignal], baselines: Dict[str, float]) -> List[TrendPattern]:
        # Placeholder implementation
        # Would need much more historical data and sophisticated analysis
        return []