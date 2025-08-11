#!/usr/bin/env python3
"""
Specialist Agents - Level 3 Content Processing Experts
Each specialist focuses on specific aspects of content analysis
"""

import asyncio
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging
from abc import ABC, abstractmethod
import re

from core import (
    ContentItem,
    ContentPriority,
    UniversalContentPrioritizer
)


class SpecialistRole(Enum):
    """Types of specialist agents"""
    TECHNICAL_VALIDATOR = "technical_validator"
    MARKET_IMPACT_ANALYZER = "market_impact_analyzer"
    SENTIMENT_TREND_TRACKER = "sentiment_trend_tracker"
    QUALITY_VALIDATOR = "quality_validator"
    CROSS_REFERENCE_SPECIALIST = "cross_reference_specialist"


@dataclass
class SpecialistAnalysis:
    """Result from specialist analysis"""
    role: SpecialistRole
    item_id: str
    confidence_score: float  # 0.0 to 1.0
    findings: Dict[str, Any]
    recommendations: List[str]
    validation_status: str  # "approved", "flagged", "rejected"
    timestamp: datetime = field(default_factory=datetime.now)


class BaseSpecialist(ABC):
    """Base class for all specialist agents"""
    
    def __init__(self, role: SpecialistRole):
        self.role = role
        self.logger = logging.getLogger(f"Specialist.{role.value}")
        self.analysis_count = 0
        self.expertise_patterns = []
        
    @abstractmethod
    async def analyze_item(self, item: ContentItem) -> SpecialistAnalysis:
        """Analyze a single content item"""
        pass
    
    @abstractmethod
    def validate_quality(self, item: ContentItem) -> float:
        """Validate quality of content (0.0 to 1.0)"""
        pass
    
    async def batch_analyze(self, items: List[ContentItem]) -> List[SpecialistAnalysis]:
        """Analyze multiple items in batch"""
        tasks = [self.analyze_item(item) for item in items]
        return await asyncio.gather(*tasks, return_exceptions=True)


class TechnicalValidatorSpecialist(BaseSpecialist):
    """
    Validates technical accuracy and implementation details
    Especially important for code examples, API changes, and technical documentation
    """
    
    def __init__(self):
        super().__init__(SpecialistRole.TECHNICAL_VALIDATOR)
        self.code_patterns = {
            "javascript": r"```(?:javascript|js|jsx|tsx|typescript|ts)(.*?)```",
            "python": r"```(?:python|py)(.*?)```",
            "json": r"```(?:json)(.*?)```",
            "yaml": r"```(?:yaml|yml)(.*?)```",
        }
        self.api_patterns = [
            r"API", r"endpoint", r"REST", r"GraphQL", r"webhook",
            r"authentication", r"authorization", r"OAuth", r"JWT"
        ]
        
    async def analyze_item(self, item: ContentItem) -> SpecialistAnalysis:
        """Analyze technical content"""
        self.analysis_count += 1
        
        findings = {}
        recommendations = []
        
        # Check for code examples
        code_blocks = self._extract_code_blocks(item.content or "")
        if code_blocks:
            findings["code_examples"] = len(code_blocks)
            findings["languages"] = list(code_blocks.keys())
            
            # Validate code quality
            code_quality = self._assess_code_quality(code_blocks)
            findings["code_quality"] = code_quality
            
            if code_quality < 0.5:
                recommendations.append("Code examples may contain errors or be incomplete")
        
        # Check for API references
        api_mentions = self._find_api_references(item.content or "")
        if api_mentions:
            findings["api_references"] = len(api_mentions)
            findings["api_types"] = api_mentions
        
        # Check for version information
        version_info = self._extract_version_info(item.content or "")
        if version_info:
            findings["versions"] = version_info
        
        # Check for breaking changes
        breaking_changes = self._detect_breaking_changes(item)
        if breaking_changes:
            findings["breaking_changes"] = True
            recommendations.append("Contains breaking changes - requires attention")
        
        # Calculate confidence score
        confidence = self.validate_quality(item)
        
        # Determine validation status
        if breaking_changes:
            validation_status = "flagged"
        elif confidence > 0.7:
            validation_status = "approved"
        elif confidence > 0.4:
            validation_status = "flagged"
        else:
            validation_status = "rejected"
        
        return SpecialistAnalysis(
            role=self.role,
            item_id=item.item_id,
            confidence_score=confidence,
            findings=findings,
            recommendations=recommendations,
            validation_status=validation_status
        )
    
    def validate_quality(self, item: ContentItem) -> float:
        """Validate technical content quality"""
        score = 0.5  # Base score
        
        content = (item.content or "").lower()
        
        # Positive indicators
        if "example" in content or "demo" in content:
            score += 0.1
        if "documentation" in content or "docs" in content:
            score += 0.1
        if any(pattern in content for pattern in ["version", "release", "update"]):
            score += 0.1
        
        # Check source authority
        if item.metadata.get("source_authority", 0) > 0.8:
            score += 0.15
        
        # Negative indicators
        if "deprecated" in content or "obsolete" in content:
            score -= 0.2
        if "beta" in content or "experimental" in content:
            score -= 0.1
        if "bug" in content or "issue" in content:
            score -= 0.1
        
        return max(0.0, min(1.0, score))
    
    def _extract_code_blocks(self, content: str) -> Dict[str, List[str]]:
        """Extract code blocks by language"""
        code_blocks = {}
        
        for lang, pattern in self.code_patterns.items():
            matches = re.findall(pattern, content, re.DOTALL)
            if matches:
                code_blocks[lang] = matches
        
        return code_blocks
    
    def _assess_code_quality(self, code_blocks: Dict[str, List[str]]) -> float:
        """Simple code quality assessment"""
        if not code_blocks:
            return 0.0
        
        total_score = 0
        block_count = 0
        
        for lang, blocks in code_blocks.items():
            for block in blocks:
                block_count += 1
                score = 0.5  # Base score
                
                # Check for comments
                if "//" in block or "#" in block or "/*" in block:
                    score += 0.2
                
                # Check for proper structure (very basic)
                if lang in ["javascript", "python"]:
                    if "function" in block or "def " in block or "class " in block:
                        score += 0.2
                
                # Check length (not too short, not too long)
                lines = block.strip().split("\n")
                if 3 <= len(lines) <= 50:
                    score += 0.1
                
                total_score += score
        
        return total_score / block_count if block_count > 0 else 0.5
    
    def _find_api_references(self, content: str) -> List[str]:
        """Find API-related references"""
        found = []
        content_lower = content.lower()
        
        for pattern in self.api_patterns:
            if pattern.lower() in content_lower:
                found.append(pattern)
        
        return found
    
    def _extract_version_info(self, content: str) -> List[str]:
        """Extract version information"""
        version_pattern = r"v?\d+\.\d+(?:\.\d+)?"
        versions = re.findall(version_pattern, content)
        return versions[:5]  # Limit to first 5
    
    def _detect_breaking_changes(self, item: ContentItem) -> bool:
        """Detect if content mentions breaking changes"""
        keywords = ["breaking change", "migration", "deprecat", "incompatible", "major version"]
        content_lower = (item.title + " " + (item.content or "")).lower()
        
        return any(keyword in content_lower for keyword in keywords)


class MarketImpactAnalyzer(BaseSpecialist):
    """
    Analyzes business implications and adoption potential
    """
    
    def __init__(self):
        super().__init__(SpecialistRole.MARKET_IMPACT_ANALYZER)
        self.business_indicators = [
            "revenue", "market", "customer", "business", "enterprise",
            "adoption", "growth", "investment", "partnership", "acquisition"
        ]
        self.impact_levels = {
            "high": ["major", "significant", "breakthrough", "revolutionary", "game-changing"],
            "medium": ["notable", "important", "substantial", "meaningful"],
            "low": ["minor", "small", "incremental", "modest"]
        }
        
    async def analyze_item(self, item: ContentItem) -> SpecialistAnalysis:
        """Analyze market and business impact"""
        self.analysis_count += 1
        
        findings = {}
        recommendations = []
        
        # Assess business relevance
        business_score = self._calculate_business_relevance(item)
        findings["business_relevance"] = business_score
        
        # Detect market signals
        market_signals = self._detect_market_signals(item)
        if market_signals:
            findings["market_signals"] = market_signals
        
        # Assess impact level
        impact_level = self._assess_impact_level(item)
        findings["impact_level"] = impact_level
        
        # Check for competitive implications
        competitive_aspect = self._analyze_competitive_aspect(item)
        if competitive_aspect:
            findings["competitive_implications"] = competitive_aspect
        
        # Generate recommendations
        if business_score > 0.7:
            recommendations.append("High business relevance - prioritize for stakeholder review")
        
        if impact_level == "high":
            recommendations.append("Significant market impact potential - track closely")
        
        # Calculate confidence
        confidence = self.validate_quality(item)
        
        # Determine validation status
        if confidence > 0.6 and business_score > 0.5:
            validation_status = "approved"
        elif confidence > 0.4:
            validation_status = "flagged"
        else:
            validation_status = "rejected"
        
        return SpecialistAnalysis(
            role=self.role,
            item_id=item.item_id,
            confidence_score=confidence,
            findings=findings,
            recommendations=recommendations,
            validation_status=validation_status
        )
    
    def validate_quality(self, item: ContentItem) -> float:
        """Validate market impact content quality"""
        score = 0.5
        
        # Check source credibility for business news
        if item.metadata.get("source_type") in ["official", "news", "research"]:
            score += 0.2
        
        # Check for quantitative data
        content = (item.content or "")
        if any(char.isdigit() for char in content):
            if "%" in content or "$" in content or "€" in content:
                score += 0.15
        
        # Check for specific companies or products mentioned
        if re.search(r"[A-Z][a-z]+(?:Corp|Inc|Ltd|LLC|Company)", content):
            score += 0.1
        
        # Authority boost
        if item.metadata.get("source_authority", 0) > 0.7:
            score += 0.1
        
        return min(1.0, score)
    
    def _calculate_business_relevance(self, item: ContentItem) -> float:
        """Calculate business relevance score"""
        content_lower = (item.title + " " + (item.content or "")).lower()
        
        indicator_count = sum(1 for indicator in self.business_indicators 
                             if indicator in content_lower)
        
        return min(1.0, indicator_count / 5)  # Normalize to 0-1
    
    def _detect_market_signals(self, item: ContentItem) -> List[str]:
        """Detect market-related signals"""
        signals = []
        content_lower = (item.title + " " + (item.content or "")).lower()
        
        signal_patterns = {
            "funding": ["funding", "investment", "series", "raised"],
            "launch": ["launch", "release", "announce", "introduce"],
            "partnership": ["partner", "collaboration", "alliance", "joint"],
            "acquisition": ["acquire", "acquisition", "merger", "buyout"],
            "expansion": ["expand", "growth", "scale", "international"]
        }
        
        for signal_type, keywords in signal_patterns.items():
            if any(keyword in content_lower for keyword in keywords):
                signals.append(signal_type)
        
        return signals
    
    def _assess_impact_level(self, item: ContentItem) -> str:
        """Assess the impact level of the content"""
        content_lower = (item.title + " " + (item.content or "")).lower()
        
        for level, indicators in self.impact_levels.items():
            if any(indicator in content_lower for indicator in indicators):
                return level
        
        return "medium"  # Default
    
    def _analyze_competitive_aspect(self, item: ContentItem) -> Optional[str]:
        """Analyze competitive implications"""
        content_lower = (item.title + " " + (item.content or "")).lower()
        
        competitive_keywords = ["competitor", "rival", "versus", "vs", "compare", "alternative"]
        
        if any(keyword in content_lower for keyword in competitive_keywords):
            return "competitive_analysis_needed"
        
        return None


class SentimentTrendTracker(BaseSpecialist):
    """
    Tracks community sentiment and emerging patterns
    """
    
    def __init__(self):
        super().__init__(SpecialistRole.SENTIMENT_TREND_TRACKER)
        self.sentiment_words = {
            "positive": ["great", "excellent", "amazing", "love", "best", "awesome", 
                        "fantastic", "brilliant", "perfect", "wonderful"],
            "negative": ["bad", "terrible", "awful", "hate", "worst", "horrible",
                        "disappointing", "broken", "frustrating", "poor"],
            "neutral": ["okay", "fine", "average", "normal", "typical", "standard"]
        }
        self.trend_indicators = ["trending", "viral", "popular", "hot", "buzz"]
        
    async def analyze_item(self, item: ContentItem) -> SpecialistAnalysis:
        """Analyze sentiment and trends"""
        self.analysis_count += 1
        
        findings = {}
        recommendations = []
        
        # Analyze sentiment
        sentiment_result = self._analyze_sentiment(item)
        findings["sentiment"] = sentiment_result
        
        # Check for trending signals
        is_trending = self._check_trending_signals(item)
        findings["trending"] = is_trending
        
        # Analyze engagement metrics if available
        engagement = self._analyze_engagement(item)
        if engagement:
            findings["engagement_metrics"] = engagement
        
        # Detect emotional intensity
        emotional_intensity = self._measure_emotional_intensity(item)
        findings["emotional_intensity"] = emotional_intensity
        
        # Generate recommendations
        if sentiment_result["score"] < -0.5:
            recommendations.append("Strong negative sentiment - investigate concerns")
        elif sentiment_result["score"] > 0.5:
            recommendations.append("Strong positive sentiment - amplification opportunity")
        
        if is_trending:
            recommendations.append("Content is trending - monitor for developments")
        
        # Calculate confidence
        confidence = self.validate_quality(item)
        
        # Determine validation status
        validation_status = "approved" if confidence > 0.5 else "flagged"
        
        return SpecialistAnalysis(
            role=self.role,
            item_id=item.item_id,
            confidence_score=confidence,
            findings=findings,
            recommendations=recommendations,
            validation_status=validation_status
        )
    
    def validate_quality(self, item: ContentItem) -> float:
        """Validate sentiment analysis quality"""
        score = 0.5
        
        # Check if we have engagement data
        if item.metadata.get("comments") or item.metadata.get("likes") or item.metadata.get("shares"):
            score += 0.2
        
        # Check content length (more content = better sentiment analysis)
        content_length = len(item.content or "")
        if content_length > 500:
            score += 0.15
        elif content_length > 200:
            score += 0.1
        
        # Check source type
        if item.metadata.get("source_type") in ["social", "forum", "community"]:
            score += 0.15  # Better for sentiment
        
        return min(1.0, score)
    
    def _analyze_sentiment(self, item: ContentItem) -> Dict[str, Any]:
        """Analyze sentiment of content"""
        content_lower = (item.title + " " + (item.content or "")).lower()
        
        positive_count = sum(1 for word in self.sentiment_words["positive"] 
                           if word in content_lower)
        negative_count = sum(1 for word in self.sentiment_words["negative"] 
                           if word in content_lower)
        neutral_count = sum(1 for word in self.sentiment_words["neutral"] 
                          if word in content_lower)
        
        total = positive_count + negative_count + neutral_count
        
        if total == 0:
            return {"label": "neutral", "score": 0.0, "confidence": 0.3}
        
        # Calculate sentiment score (-1 to 1)
        score = (positive_count - negative_count) / total
        
        # Determine label
        if score > 0.3:
            label = "positive"
        elif score < -0.3:
            label = "negative"
        else:
            label = "neutral"
        
        return {
            "label": label,
            "score": score,
            "confidence": min(1.0, total / 10)  # More sentiment words = higher confidence
        }
    
    def _check_trending_signals(self, item: ContentItem) -> bool:
        """Check if content shows trending signals"""
        content_lower = (item.title + " " + (item.content or "")).lower()
        
        # Check for trending keywords
        if any(indicator in content_lower for indicator in self.trend_indicators):
            return True
        
        # Check engagement metrics
        views = item.metadata.get("views", 0)
        if views > 10000:
            return True
        
        comments = item.metadata.get("comments", 0)
        if comments > 100:
            return True
        
        return False
    
    def _analyze_engagement(self, item: ContentItem) -> Optional[Dict[str, Any]]:
        """Analyze engagement metrics if available"""
        engagement = {}
        
        if "views" in item.metadata:
            engagement["views"] = item.metadata["views"]
        if "likes" in item.metadata:
            engagement["likes"] = item.metadata["likes"]
        if "comments" in item.metadata:
            engagement["comments"] = item.metadata["comments"]
        if "shares" in item.metadata:
            engagement["shares"] = item.metadata["shares"]
        
        if engagement:
            # Calculate engagement rate if possible
            if "views" in engagement and engagement["views"] > 0:
                interactions = sum([
                    engagement.get("likes", 0),
                    engagement.get("comments", 0),
                    engagement.get("shares", 0)
                ])
                engagement["engagement_rate"] = interactions / engagement["views"]
            
            return engagement
        
        return None
    
    def _measure_emotional_intensity(self, item: ContentItem) -> str:
        """Measure emotional intensity of content"""
        content_lower = (item.title + " " + (item.content or "")).lower()
        
        # Count exclamation marks and caps
        exclamation_count = content_lower.count("!")
        caps_ratio = sum(1 for c in item.title if c.isupper()) / max(1, len(item.title))
        
        # Strong emotional words
        strong_words = ["absolutely", "completely", "totally", "extremely", "incredibly"]
        strong_word_count = sum(1 for word in strong_words if word in content_lower)
        
        # Calculate intensity
        intensity_score = exclamation_count + (caps_ratio * 5) + strong_word_count
        
        if intensity_score > 5:
            return "high"
        elif intensity_score > 2:
            return "medium"
        else:
            return "low"


class QualityValidator(BaseSpecialist):
    """
    Ensures content quality and source credibility
    """
    
    def __init__(self):
        super().__init__(SpecialistRole.QUALITY_VALIDATOR)
        self.quality_indicators = {
            "positive": ["verified", "official", "confirmed", "authoritative", "peer-reviewed"],
            "negative": ["unverified", "rumor", "speculation", "allegedly", "unconfirmed"]
        }
        
    async def analyze_item(self, item: ContentItem) -> SpecialistAnalysis:
        """Validate content quality"""
        self.analysis_count += 1
        
        findings = {}
        recommendations = []
        
        # Check source credibility
        source_credibility = self._assess_source_credibility(item)
        findings["source_credibility"] = source_credibility
        
        # Check content completeness
        completeness = self._assess_completeness(item)
        findings["completeness"] = completeness
        
        # Check for citations/references
        has_references = self._check_references(item)
        findings["has_references"] = has_references
        
        # Check factual indicators
        factual_score = self._assess_factual_indicators(item)
        findings["factual_score"] = factual_score
        
        # Overall quality score
        quality_score = self.validate_quality(item)
        findings["overall_quality"] = quality_score
        
        # Generate recommendations
        if quality_score < 0.5:
            recommendations.append("Low quality content - verify before using")
        
        if not has_references and factual_score < 0.5:
            recommendations.append("Lacks references - cross-verify claims")
        
        if source_credibility < 0.5:
            recommendations.append("Low source credibility - seek additional sources")
        
        # Determine validation status
        if quality_score > 0.7:
            validation_status = "approved"
        elif quality_score > 0.4:
            validation_status = "flagged"
        else:
            validation_status = "rejected"
        
        return SpecialistAnalysis(
            role=self.role,
            item_id=item.item_id,
            confidence_score=quality_score,
            findings=findings,
            recommendations=recommendations,
            validation_status=validation_status
        )
    
    def validate_quality(self, item: ContentItem) -> float:
        """Comprehensive quality validation"""
        scores = []
        
        # Source credibility (40% weight)
        source_score = self._assess_source_credibility(item)
        scores.append(source_score * 0.4)
        
        # Content completeness (20% weight)
        completeness = self._assess_completeness(item)
        scores.append(completeness * 0.2)
        
        # Factual indicators (20% weight)
        factual = self._assess_factual_indicators(item)
        scores.append(factual * 0.2)
        
        # Freshness (10% weight)
        freshness = self._assess_freshness(item)
        scores.append(freshness * 0.1)
        
        # References (10% weight)
        has_refs = 1.0 if self._check_references(item) else 0.3
        scores.append(has_refs * 0.1)
        
        return sum(scores)
    
    def _assess_source_credibility(self, item: ContentItem) -> float:
        """Assess credibility of the source"""
        # Start with source authority score if available
        score = item.metadata.get("source_authority", 0.5)
        
        # Adjust based on source type
        source_type = item.metadata.get("source_type", "")
        if source_type == "official":
            score += 0.2
        elif source_type == "news":
            score += 0.1
        elif source_type == "social":
            score -= 0.1
        
        return min(1.0, max(0.0, score))
    
    def _assess_completeness(self, item: ContentItem) -> float:
        """Assess content completeness"""
        if not item.content:
            return 0.2
        
        content_length = len(item.content)
        
        # Score based on length
        if content_length > 1000:
            length_score = 1.0
        elif content_length > 500:
            length_score = 0.8
        elif content_length > 200:
            length_score = 0.6
        else:
            length_score = 0.4
        
        # Check for structure (paragraphs, sections)
        paragraph_count = item.content.count("\n\n")
        if paragraph_count > 3:
            structure_score = 1.0
        elif paragraph_count > 1:
            structure_score = 0.7
        else:
            structure_score = 0.4
        
        return (length_score + structure_score) / 2
    
    def _check_references(self, item: ContentItem) -> bool:
        """Check if content has references or citations"""
        if not item.content:
            return False
        
        # Look for URLs
        if "http://" in item.content or "https://" in item.content:
            return True
        
        # Look for citation patterns
        citation_patterns = [r"\[\d+\]", r"\(\d{4}\)", r"Source:", r"Reference:"]
        for pattern in citation_patterns:
            if re.search(pattern, item.content):
                return True
        
        return False
    
    def _assess_factual_indicators(self, item: ContentItem) -> float:
        """Assess factual quality indicators"""
        content_lower = (item.title + " " + (item.content or "")).lower()
        
        positive_count = sum(1 for indicator in self.quality_indicators["positive"]
                            if indicator in content_lower)
        negative_count = sum(1 for indicator in self.quality_indicators["negative"]
                            if indicator in content_lower)
        
        if positive_count + negative_count == 0:
            return 0.5  # Neutral
        
        score = 0.5 + (positive_count * 0.2) - (negative_count * 0.3)
        return min(1.0, max(0.0, score))
    
    def _assess_freshness(self, item: ContentItem) -> float:
        """Assess content freshness"""
        if not item.published_date:
            return 0.5
        
        age = datetime.now() - item.published_date
        
        if age.days == 0:
            return 1.0
        elif age.days <= 1:
            return 0.9
        elif age.days <= 7:
            return 0.7
        elif age.days <= 30:
            return 0.5
        else:
            return 0.3


class SpecialistCoordinator:
    """
    Coordinates multiple specialist agents for comprehensive content analysis
    """
    
    def __init__(self):
        self.specialists = {
            SpecialistRole.TECHNICAL_VALIDATOR: TechnicalValidatorSpecialist(),
            SpecialistRole.MARKET_IMPACT_ANALYZER: MarketImpactAnalyzer(),
            SpecialistRole.SENTIMENT_TREND_TRACKER: SentimentTrendTracker(),
            SpecialistRole.QUALITY_VALIDATOR: QualityValidator()
        }
        self.logger = logging.getLogger("SpecialistCoordinator")
        
    async def analyze_content(self, 
                             items: List[ContentItem],
                             required_specialists: Optional[List[SpecialistRole]] = None) -> Dict[str, List[SpecialistAnalysis]]:
        """
        Coordinate specialist analysis of content items
        
        Args:
            items: Content items to analyze
            required_specialists: Specific specialists to use (None = all)
            
        Returns:
            Dictionary mapping item IDs to list of specialist analyses
        """
        if not items:
            return {}
        
        # Determine which specialists to use
        if required_specialists:
            active_specialists = {role: spec for role, spec in self.specialists.items() 
                                if role in required_specialists}
        else:
            active_specialists = self.specialists
        
        # Run all specialists concurrently on all items
        tasks = []
        for role, specialist in active_specialists.items():
            task = specialist.batch_analyze(items)
            tasks.append((role, task))
        
        # Gather results
        results_by_item = {}
        
        for role, task in tasks:
            try:
                analyses = await task
                for analysis in analyses:
                    if not isinstance(analysis, Exception):
                        item_id = analysis.item_id
                        if item_id not in results_by_item:
                            results_by_item[item_id] = []
                        results_by_item[item_id].append(analysis)
            except Exception as e:
                self.logger.error(f"Specialist {role.value} failed: {str(e)}")
        
        return results_by_item
    
    def synthesize_analyses(self, 
                           analyses: List[SpecialistAnalysis]) -> Dict[str, Any]:
        """
        Synthesize multiple specialist analyses into a consensus
        
        Args:
            analyses: List of analyses for a single item
            
        Returns:
            Synthesized analysis with consensus findings
        """
        if not analyses:
            return {}
        
        synthesis = {
            "consensus_confidence": 0.0,
            "consensus_status": "unknown",
            "key_findings": {},
            "all_recommendations": [],
            "specialist_agreement": 0.0
        }
        
        # Calculate consensus confidence (average)
        confidences = [a.confidence_score for a in analyses]
        synthesis["consensus_confidence"] = sum(confidences) / len(confidences)
        
        # Determine consensus status (majority vote)
        status_votes = {}
        for analysis in analyses:
            status = analysis.validation_status
            status_votes[status] = status_votes.get(status, 0) + 1
        
        synthesis["consensus_status"] = max(status_votes.items(), key=lambda x: x[1])[0]
        
        # Collect all findings
        for analysis in analyses:
            role_name = analysis.role.value
            synthesis["key_findings"][role_name] = analysis.findings
        
        # Collect all recommendations
        for analysis in analyses:
            synthesis["all_recommendations"].extend(analysis.recommendations)
        
        # Remove duplicate recommendations
        synthesis["all_recommendations"] = list(set(synthesis["all_recommendations"]))
        
        # Calculate specialist agreement
        if len(status_votes) == 1:
            synthesis["specialist_agreement"] = 1.0
        else:
            max_votes = max(status_votes.values())
            synthesis["specialist_agreement"] = max_votes / len(analyses)
        
        return synthesis