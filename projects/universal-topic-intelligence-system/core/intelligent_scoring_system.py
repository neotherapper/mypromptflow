#!/usr/bin/env python3
"""
Intelligent Multi-Factor Scoring System
Leverages MCP metadata for sophisticated content analysis and prioritization
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from enum import Enum
import json
import logging
import re
import math
from abc import ABC, abstractmethod

from .universal_source_monitor import ContentItem, ContentPriority, SourceMetadata
from .content_prioritizer import PriorityFactors, PriorityResult, PriorityStrategy

@dataclass
class MCPAnalysisResult:
    """Results from MCP-specific content analysis"""
    source_type: str
    quality_indicators: Dict[str, float]  # Specific quality metrics
    engagement_metrics: Dict[str, Any]    # Engagement data
    technical_metrics: Dict[str, Any]     # Technical indicators
    trending_signals: Dict[str, float]    # Trend indicators
    authority_signals: Dict[str, float]   # Authority indicators
    
class IntelligentAnalysisEngine:
    """
    Core engine for intelligent content analysis using MCP metadata
    """
    
    def __init__(self):
        self.logger = logging.getLogger("IntelligentAnalysis")
        
        # Quality thresholds for different content types
        self.quality_thresholds = {
            "youtube_transcript": {
                "min_duration_seconds": 300,    # 5 minutes minimum
                "high_engagement_views": 10000,
                "viral_views": 100000,
                "quality_channels": {
                    "Fireship", "The Primeagen", "Coding with Lewis", 
                    "freeCodeCamp.org", "React", "Vercel"
                }
            },
            "github_repository": {
                "high_quality_stars": 1000,
                "viral_stars": 10000,
                "active_threshold_days": 30,
                "quality_languages": {
                    "TypeScript", "JavaScript", "Python", "Go", "Rust"
                }
            },
            "web_search": {
                "high_relevance_score": 0.8,
                "trusted_domains": {
                    "react.dev", "github.com", "stackoverflow.com",
                    "medium.com", "dev.to", "docs.anthropic.com"
                }
            }
        }
    
    def analyze_mcp_content(self, content: ContentItem) -> MCPAnalysisResult:
        """
        Perform intelligent analysis of MCP content using metadata
        """
        mcp_source_type = content.metadata.get("mcp_source_type")
        
        if not mcp_source_type:
            # Fallback for non-MCP content
            return self._analyze_generic_content(content)
        
        if mcp_source_type == "youtube_transcript":
            return self._analyze_youtube_content(content)
        elif mcp_source_type == "github_repository":
            return self._analyze_github_content(content)
        elif mcp_source_type == "web_search":
            return self._analyze_search_content(content)
        else:
            return self._analyze_generic_content(content)
    
    def _analyze_youtube_content(self, content: ContentItem) -> MCPAnalysisResult:
        """Analyze YouTube content using video metadata"""
        metadata = content.metadata
        
        # Extract YouTube-specific data
        view_count = metadata.get("youtube_view_count", 0)
        like_count = metadata.get("youtube_like_count", 0)
        channel = metadata.get("youtube_channel", "")
        duration = metadata.get("youtube_duration", "")
        video_id = metadata.get("youtube_video_id", "")
        language = metadata.get("youtube_language", "")
        
        # Calculate duration in seconds
        duration_seconds = self._parse_youtube_duration(duration)
        
        # Quality indicators
        quality_indicators = {
            "channel_authority": self._calculate_channel_authority(channel),
            "content_length": self._score_video_length(duration_seconds),
            "production_quality": self._estimate_production_quality(view_count, like_count),
            "language_quality": 1.0 if language == "en" else 0.7
        }
        
        # Engagement metrics
        engagement_metrics = {
            "view_count": view_count,
            "like_count": like_count,
            "engagement_rate": self._calculate_youtube_engagement(view_count, like_count),
            "viral_factor": self._calculate_viral_factor(view_count)
        }
        
        # Technical metrics
        technical_metrics = {
            "duration_seconds": duration_seconds,
            "is_tutorial": self._detect_tutorial_content(content.title, content.content),
            "has_code_examples": self._detect_code_content(content.content),
            "technical_depth": self._assess_technical_depth(content.content)
        }
        
        # Trending signals
        trending_signals = {
            "view_velocity": self._estimate_view_velocity(view_count, content.published_date),
            "recency_boost": self._calculate_recency_boost(content.published_date),
            "topic_momentum": self._assess_topic_momentum(content.topics)
        }
        
        # Authority signals
        authority_signals = {
            "channel_reputation": quality_indicators["channel_authority"],
            "view_authority": min(1.0, view_count / 50000),
            "engagement_authority": engagement_metrics["engagement_rate"]
        }
        
        return MCPAnalysisResult(
            source_type="youtube_transcript",
            quality_indicators=quality_indicators,
            engagement_metrics=engagement_metrics,
            technical_metrics=technical_metrics,
            trending_signals=trending_signals,
            authority_signals=authority_signals
        )
    
    def _analyze_github_content(self, content: ContentItem) -> MCPAnalysisResult:
        """Analyze GitHub repository using repository metadata"""
        metadata = content.metadata
        
        # Extract GitHub-specific data
        stars = metadata.get("github_stars", 0)
        forks = metadata.get("github_forks", 0)
        language = metadata.get("github_language", "")
        license = metadata.get("github_license", "")
        open_issues = metadata.get("github_open_issues", 0)
        repo_name = metadata.get("github_repo_name", "")
        
        # Quality indicators
        quality_indicators = {
            "star_quality": self._score_repository_stars(stars),
            "language_relevance": self._score_programming_language(language),
            "maintenance_quality": self._assess_maintenance_quality(open_issues, forks),
            "license_compliance": self._score_license_quality(license)
        }
        
        # Engagement metrics
        engagement_metrics = {
            "stars": stars,
            "forks": forks,
            "fork_ratio": forks / max(1, stars),
            "community_engagement": self._calculate_github_engagement(stars, forks, open_issues)
        }
        
        # Technical metrics
        technical_metrics = {
            "is_framework": self._detect_framework_repo(repo_name, content.title),
            "is_library": self._detect_library_repo(repo_name, content.title),
            "has_documentation": self._detect_documentation_quality(content.content),
            "code_quality_indicators": self._assess_code_quality_signals(metadata)
        }
        
        # Trending signals
        trending_signals = {
            "star_velocity": self._estimate_star_velocity(stars),
            "activity_level": self._assess_repository_activity(content.published_date),
            "ecosystem_relevance": self._assess_ecosystem_relevance(language, content.topics)
        }
        
        # Authority signals
        authority_signals = {
            "community_authority": min(1.0, stars / 5000),
            "technical_authority": quality_indicators["language_relevance"],
            "ecosystem_authority": trending_signals["ecosystem_relevance"]
        }
        
        return MCPAnalysisResult(
            source_type="github_repository",
            quality_indicators=quality_indicators,
            engagement_metrics=engagement_metrics,
            technical_metrics=technical_metrics,
            trending_signals=trending_signals,
            authority_signals=authority_signals
        )
    
    def _analyze_search_content(self, content: ContentItem) -> MCPAnalysisResult:
        """Analyze web search content using search metadata"""
        metadata = content.metadata
        
        # Extract search-specific data
        search_query = metadata.get("search_query", "")
        search_rank = metadata.get("search_rank", 0)
        search_engine = metadata.get("search_engine", "")
        relevance_score = metadata.get("search_relevance_score", 0.0)
        domain = metadata.get("search_domain", "")
        
        # Quality indicators
        quality_indicators = {
            "domain_authority": self._score_domain_authority(domain),
            "search_relevance": relevance_score,
            "rank_quality": self._score_search_rank(search_rank),
            "content_completeness": self._assess_content_completeness(content.content)
        }
        
        # Engagement metrics (limited for search content)
        engagement_metrics = {
            "search_rank": search_rank,
            "query_relevance": self._calculate_query_relevance(search_query, content.title),
            "click_worthiness": self._assess_click_worthiness(content.title, content.url)
        }
        
        # Technical metrics
        technical_metrics = {
            "is_documentation": self._detect_documentation_content(domain, content.title),
            "is_tutorial": self._detect_tutorial_content(content.title, content.content),
            "technical_depth": self._assess_technical_depth(content.content)
        }
        
        # Trending signals
        trending_signals = {
            "query_momentum": self._assess_query_momentum(search_query),
            "domain_freshness": self._assess_domain_freshness(domain),
            "content_recency": self._calculate_recency_boost(content.published_date)
        }
        
        # Authority signals
        authority_signals = {
            "domain_reputation": quality_indicators["domain_authority"],
            "search_authority": quality_indicators["rank_quality"],
            "content_authority": quality_indicators["content_completeness"]
        }
        
        return MCPAnalysisResult(
            source_type="web_search",
            quality_indicators=quality_indicators,
            engagement_metrics=engagement_metrics,
            technical_metrics=technical_metrics,
            trending_signals=trending_signals,
            authority_signals=authority_signals
        )
    
    def _analyze_generic_content(self, content: ContentItem) -> MCPAnalysisResult:
        """Fallback analysis for non-MCP content"""
        
        # Basic quality indicators
        quality_indicators = {
            "content_length": min(1.0, len(content.content or "") / 1000),
            "title_quality": self._assess_title_quality(content.title),
            "source_reliability": 0.5,  # Default
            "language_quality": 0.8    # Assume good
        }
        
        # Basic engagement metrics
        engagement_metrics = {
            "estimated_engagement": content.metadata.get("engagement_score", 0.3),
            "social_signals": content.metadata.get("social_signals", 0.3)
        }
        
        # Basic technical metrics
        technical_metrics = {
            "is_technical": self._detect_technical_content(content.title, content.content),
            "has_examples": self._detect_code_content(content.content),
            "technical_depth": self._assess_technical_depth(content.content)
        }
        
        # Basic trending signals
        trending_signals = {
            "recency_factor": self._calculate_recency_boost(content.published_date),
            "topic_relevance": 0.5
        }
        
        # Basic authority signals
        authority_signals = {
            "source_authority": 0.5,
            "content_authority": quality_indicators["content_length"]
        }
        
        return MCPAnalysisResult(
            source_type="generic",
            quality_indicators=quality_indicators,
            engagement_metrics=engagement_metrics,
            technical_metrics=technical_metrics,
            trending_signals=trending_signals,
            authority_signals=authority_signals
        )
    
    # Helper methods for YouTube analysis
    def _parse_youtube_duration(self, duration_str: str) -> int:
        """Parse YouTube duration string (PT15M33S) to seconds"""
        if not duration_str:
            return 0
        
        # Extract minutes and seconds from PT format
        import re
        match = re.search(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration_str)
        if match:
            hours = int(match.group(1) or 0)
            minutes = int(match.group(2) or 0)
            seconds = int(match.group(3) or 0)
            return hours * 3600 + minutes * 60 + seconds
        return 0
    
    def _calculate_channel_authority(self, channel: str) -> float:
        """Calculate channel authority based on known quality channels"""
        if not channel:
            return 0.3
        
        quality_channels = self.quality_thresholds["youtube_transcript"]["quality_channels"]
        if channel in quality_channels:
            return 1.0
        
        # Check for indicators of quality channels
        quality_indicators = ["official", "react", "google", "microsoft", "meta"]
        channel_lower = channel.lower()
        
        for indicator in quality_indicators:
            if indicator in channel_lower:
                return 0.8
        
        return 0.5  # Default authority
    
    def _score_video_length(self, duration_seconds: int) -> float:
        """Score video based on optimal length for educational content"""
        if duration_seconds == 0:
            return 0.3
        
        # Optimal length for tutorials: 5-30 minutes
        if 300 <= duration_seconds <= 1800:  # 5-30 minutes
            return 1.0
        elif 60 <= duration_seconds <= 300:   # 1-5 minutes
            return 0.7
        elif 1800 < duration_seconds <= 3600: # 30-60 minutes
            return 0.8
        else:
            return 0.4  # Too short or too long
    
    def _estimate_production_quality(self, views: int, likes: int) -> float:
        """Estimate production quality from engagement metrics"""
        if views == 0:
            return 0.3
        
        like_ratio = likes / views if views > 0 else 0
        
        # High like ratio indicates good production quality
        if like_ratio > 0.05:  # 5% like ratio is excellent
            return 1.0
        elif like_ratio > 0.02:  # 2% is good
            return 0.8
        elif like_ratio > 0.01:  # 1% is average
            return 0.6
        else:
            return 0.4
    
    def _calculate_youtube_engagement(self, views: int, likes: int) -> float:
        """Calculate YouTube engagement rate"""
        if views == 0:
            return 0.0
        
        return min(1.0, likes / views * 100)  # Like rate as percentage
    
    def _calculate_viral_factor(self, views: int) -> float:
        """Calculate viral factor based on view count"""
        viral_threshold = self.quality_thresholds["youtube_transcript"]["viral_views"]
        return min(1.0, views / viral_threshold)
    
    # Helper methods for GitHub analysis
    def _score_repository_stars(self, stars: int) -> float:
        """Score repository based on star count"""
        if stars >= 10000:
            return 1.0
        elif stars >= 1000:
            return 0.8
        elif stars >= 100:
            return 0.6
        elif stars >= 10:
            return 0.4
        else:
            return 0.2
    
    def _score_programming_language(self, language: str) -> float:
        """Score based on programming language relevance"""
        if not language:
            return 0.3
        
        quality_languages = self.quality_thresholds["github_repository"]["quality_languages"]
        if language in quality_languages:
            return 1.0
        
        # Common web languages
        web_languages = {"HTML", "CSS", "PHP", "Ruby", "Java", "C++", "C#"}
        if language in web_languages:
            return 0.7
        
        return 0.5  # Other languages
    
    def _assess_maintenance_quality(self, open_issues: int, forks: int) -> float:
        """Assess repository maintenance quality"""
        if forks == 0:
            return 0.3  # No community engagement
        
        # Low issue-to-fork ratio indicates good maintenance
        issue_ratio = open_issues / max(1, forks)
        
        if issue_ratio < 0.1:
            return 1.0  # Excellent maintenance
        elif issue_ratio < 0.3:
            return 0.8  # Good maintenance
        elif issue_ratio < 0.5:
            return 0.6  # Average maintenance
        else:
            return 0.4  # Poor maintenance
    
    def _score_license_quality(self, license: str) -> float:
        """Score license based on openness and adoption"""
        if not license:
            return 0.3
        
        # Popular open source licenses
        good_licenses = {"MIT", "Apache-2.0", "BSD-3-Clause", "ISC", "GPL-3.0"}
        license_upper = license.upper()
        
        for good_license in good_licenses:
            if good_license.upper() in license_upper:
                return 1.0
        
        return 0.6  # Other licenses
    
    # Helper methods for web search analysis
    def _score_domain_authority(self, domain: str) -> float:
        """Score domain based on authority and trustworthiness"""
        if not domain:
            return 0.3
        
        trusted_domains = self.quality_thresholds["web_search"]["trusted_domains"]
        if domain in trusted_domains:
            return 1.0
        
        # Check for other high-authority patterns
        if any(pattern in domain for pattern in [".gov", ".edu", ".org"]):
            return 0.9
        
        # Check for documentation sites
        if "docs." in domain or "documentation" in domain:
            return 0.8
        
        return 0.5  # Default authority
    
    def _score_search_rank(self, rank: int) -> float:
        """Score based on search result ranking"""
        if rank <= 0:
            return 0.5
        
        # Higher ranks (lower numbers) are better
        if rank <= 3:
            return 1.0
        elif rank <= 10:
            return 0.8
        elif rank <= 20:
            return 0.6
        else:
            return 0.4
    
    # Common helper methods
    def _detect_tutorial_content(self, title: str, content: str) -> float:
        """Detect if content is tutorial/educational"""
        tutorial_indicators = [
            "tutorial", "guide", "how to", "step by step", "learn",
            "introduction", "getting started", "walkthrough", "course"
        ]
        
        text = f"{title} {content or ''}".lower()
        matches = sum(1 for indicator in tutorial_indicators if indicator in text)
        
        return min(1.0, matches / 3)  # Normalize to 0-1
    
    def _detect_code_content(self, content: str) -> float:
        """Detect presence of code examples"""
        if not content:
            return 0.0
        
        code_indicators = [
            "```", "function", "const ", "import ", "from ", "class ",
            "def ", "return ", "console.log", "useState", "useEffect"
        ]
        
        matches = sum(1 for indicator in code_indicators if indicator in content)
        return min(1.0, matches / 5)  # Normalize to 0-1
    
    def _assess_technical_depth(self, content: str) -> float:
        """Assess technical depth of content"""
        if not content:
            return 0.0
        
        technical_terms = [
            "api", "algorithm", "architecture", "performance", "optimization",
            "security", "scalability", "database", "backend", "frontend",
            "framework", "library", "component", "interface", "implementation"
        ]
        
        content_lower = content.lower()
        matches = sum(1 for term in technical_terms if term in content_lower)
        
        # Also consider content length as depth indicator
        length_factor = min(1.0, len(content) / 2000)
        
        return min(1.0, (matches / 10) * 0.7 + length_factor * 0.3)
    
    def _calculate_recency_boost(self, published_date: Optional[datetime]) -> float:
        """Calculate recency boost factor"""
        if not published_date:
            return 0.3
        
        now = datetime.now(published_date.tzinfo) if published_date.tzinfo else datetime.now()
        age_hours = (now - published_date).total_seconds() / 3600
        
        # Boost recent content
        if age_hours < 24:
            return 1.0
        elif age_hours < 168:  # 1 week
            return 0.8
        elif age_hours < 720:  # 1 month
            return 0.6
        else:
            return 0.4
    
    def _assess_title_quality(self, title: str) -> float:
        """Assess title quality and descriptiveness"""
        if not title:
            return 0.1
        
        # Good title indicators
        quality_indicators = 0.0
        
        # Reasonable length
        if 20 <= len(title) <= 100:
            quality_indicators += 0.3
        
        # Contains action words
        action_words = ["how", "guide", "tutorial", "learn", "build", "create", "develop"]
        if any(word in title.lower() for word in action_words):
            quality_indicators += 0.3
        
        # Contains technical terms
        if any(char.isupper() for char in title):  # Has capitalization
            quality_indicators += 0.2
        
        # Not clickbait
        clickbait_words = ["you won't believe", "shocking", "amazing", "incredible"]
        if not any(word in title.lower() for word in clickbait_words):
            quality_indicators += 0.2
        
        return min(1.0, quality_indicators)
    
    # Placeholder methods for complex analysis (can be enhanced later)
    def _estimate_view_velocity(self, views: int, published_date: Optional[datetime]) -> float:
        """Estimate view velocity (views per day)"""
        if not published_date or views == 0:
            return 0.0
        
        now = datetime.now(published_date.tzinfo) if published_date.tzinfo else datetime.now()
        age_days = max(1, (now - published_date).days)
        
        velocity = views / age_days
        return min(1.0, velocity / 1000)  # Normalize to daily views
    
    def _assess_topic_momentum(self, topics: List[str]) -> float:
        """Assess momentum of topics (placeholder)"""
        # Could be enhanced with trend data
        return 0.5
    
    def _estimate_star_velocity(self, stars: int) -> float:
        """Estimate star velocity (placeholder)"""
        # Could be enhanced with historical data
        return min(1.0, stars / 5000)
    
    def _assess_repository_activity(self, published_date: Optional[datetime]) -> float:
        """Assess repository activity level"""
        return self._calculate_recency_boost(published_date)
    
    def _assess_ecosystem_relevance(self, language: str, topics: List[str]) -> float:
        """Assess relevance to current ecosystem trends"""
        if not language or not topics:
            return 0.5
        
        # Hot topics and languages
        hot_topics = {"react", "ai", "machine learning", "typescript", "nextjs"}
        hot_languages = {"TypeScript", "Python", "JavaScript", "Rust", "Go"}
        
        relevance = 0.0
        
        if language in hot_languages:
            relevance += 0.5
        
        for topic in topics:
            if any(hot_topic in topic.lower() for hot_topic in hot_topics):
                relevance += 0.3
                break
        
        return min(1.0, relevance)
    
    def _calculate_github_engagement(self, stars: int, forks: int, issues: int) -> float:
        """Calculate GitHub community engagement"""
        if stars == 0:
            return 0.0
        
        # Engagement formula: consider forks and active issues relative to stars
        fork_ratio = forks / stars
        issue_activity = min(1.0, issues / max(1, stars))
        
        engagement = (fork_ratio * 0.6 + issue_activity * 0.4)
        return min(1.0, engagement)
    
    def _calculate_query_relevance(self, query: str, title: str) -> float:
        """Calculate relevance between search query and result title"""
        if not query or not title:
            return 0.3
        
        query_words = set(query.lower().split())
        title_words = set(title.lower().split())
        
        intersection = query_words.intersection(title_words)
        if not query_words:
            return 0.3
        
        return len(intersection) / len(query_words)
    
    def _assess_click_worthiness(self, title: str, url: str) -> float:
        """Assess how click-worthy the content appears"""
        return self._assess_title_quality(title)
    
    def _assess_query_momentum(self, query: str) -> float:
        """Assess momentum of search query (placeholder)"""
        return 0.5
    
    def _assess_domain_freshness(self, domain: str) -> float:
        """Assess how fresh/updated the domain typically is"""
        fresh_domains = {"github.com", "stackoverflow.com", "dev.to"}
        return 0.8 if domain in fresh_domains else 0.5
    
    def _assess_content_completeness(self, content: str) -> float:
        """Assess how complete the content appears"""
        if not content:
            return 0.2
        
        # Simple completeness indicators
        length_score = min(1.0, len(content) / 1500)
        has_structure = any(indicator in content for indicator in ["##", "- ", "1.", "* "])
        structure_score = 0.3 if has_structure else 0.0
        
        return min(1.0, length_score * 0.7 + structure_score)
    
    def _detect_documentation_content(self, domain: str, title: str) -> float:
        """Detect if content is documentation"""
        doc_indicators = ["docs", "documentation", "api", "reference", "guide"]
        text = f"{domain} {title}".lower()
        
        matches = sum(1 for indicator in doc_indicators if indicator in text)
        return min(1.0, matches / 2)
    
    def _detect_technical_content(self, title: str, content: str) -> float:
        """Detect if content is technical"""
        return self._assess_technical_depth(f"{title} {content or ''}")
    
    def _detect_framework_repo(self, repo_name: str, title: str) -> float:
        """Detect if repository is a framework"""
        framework_indicators = ["framework", "react", "vue", "angular", "next", "nuxt"]
        text = f"{repo_name} {title}".lower()
        
        return 1.0 if any(indicator in text for indicator in framework_indicators) else 0.0
    
    def _detect_library_repo(self, repo_name: str, title: str) -> float:
        """Detect if repository is a library"""
        library_indicators = ["library", "lib", "package", "component", "util"]
        text = f"{repo_name} {title}".lower()
        
        return 1.0 if any(indicator in text for indicator in library_indicators) else 0.0
    
    def _detect_documentation_quality(self, content: str) -> float:
        """Detect quality of documentation"""
        if not content:
            return 0.2
        
        doc_quality_indicators = [
            "## ", "### ", "installation", "usage", "example", 
            "api", "getting started", "documentation"
        ]
        
        matches = sum(1 for indicator in doc_quality_indicators if indicator in content.lower())
        return min(1.0, matches / 5)
    
    def _assess_code_quality_signals(self, metadata: Dict[str, Any]) -> float:
        """Assess code quality from repository signals"""
        # Basic assessment from available metadata
        stars = metadata.get("github_stars", 0)
        forks = metadata.get("github_forks", 0)
        
        # High star-to-fork ratio suggests quality
        if forks > 0:
            ratio = stars / forks
            if ratio > 10:
                return 0.9
            elif ratio > 5:
                return 0.7
            else:
                return 0.5
        
        return 0.4


class IntelligentPriorityStrategy(PriorityStrategy):
    """
    Intelligent prioritization strategy using MCP metadata analysis
    """
    
    def __init__(self):
        self.analysis_engine = IntelligentAnalysisEngine()
        self.logger = logging.getLogger("IntelligentPriority")
    
    def calculate_factors(self, content: ContentItem, context: Dict[str, Any]) -> PriorityFactors:
        """Calculate priority factors using intelligent MCP analysis"""
        
        # Perform intelligent analysis
        analysis = self.analysis_engine.analyze_mcp_content(content)
        
        # Extract factors from analysis
        source_authority = self._calculate_source_authority(analysis, context)
        content_recency = self._calculate_content_recency(analysis, content)
        topic_relevance = self._calculate_topic_relevance(analysis, content, context)
        engagement_signals = self._calculate_engagement_signals(analysis)
        uniqueness_score = self._calculate_uniqueness_score(analysis)
        completeness = self._calculate_completeness(analysis)
        actionability = self._calculate_actionability(analysis)
        cross_topic_value = self._calculate_cross_topic_value(analysis, content)
        
        return PriorityFactors(
            source_authority=source_authority,
            content_recency=content_recency,
            topic_relevance=topic_relevance,
            engagement_signals=engagement_signals,
            uniqueness_score=uniqueness_score,
            completeness=completeness,
            actionability=actionability,
            cross_topic_value=cross_topic_value
        )
    
    def _calculate_source_authority(self, analysis: MCPAnalysisResult, context: Dict[str, Any]) -> float:
        """Calculate source authority from analysis"""
        # Combine multiple authority signals
        authority_scores = list(analysis.authority_signals.values())
        
        if not authority_scores:
            return context.get("source_scores", {}).get("default", 0.5)
        
        # Weighted average of authority signals
        return sum(authority_scores) / len(authority_scores)
    
    def _calculate_content_recency(self, analysis: MCPAnalysisResult, content: ContentItem) -> float:
        """Calculate content recency with trending signals"""
        base_recency = analysis.trending_signals.get("recency_factor", 0.5)
        
        # Boost for trending content
        trending_boost = max(analysis.trending_signals.values()) if analysis.trending_signals else 0.0
        
        return min(1.0, base_recency + trending_boost * 0.2)
    
    def _calculate_topic_relevance(self, analysis: MCPAnalysisResult, content: ContentItem, context: Dict[str, Any]) -> float:
        """Calculate topic relevance using intelligent analysis"""
        # Base relevance from topic preferences
        topic_prefs = context.get("topic_preferences", {})
        base_relevance = max([topic_prefs.get(topic, 0.5) for topic in content.topics], default=0.5)
        
        # Boost from technical depth and quality
        technical_boost = analysis.technical_metrics.get("technical_depth", 0.0) * 0.2
        quality_boost = max(analysis.quality_indicators.values()) * 0.1 if analysis.quality_indicators else 0.0
        
        return min(1.0, base_relevance + technical_boost + quality_boost)
    
    def _calculate_engagement_signals(self, analysis: MCPAnalysisResult) -> float:
        """Calculate engagement signals from MCP analysis"""
        engagement_metrics = analysis.engagement_metrics
        
        if not engagement_metrics:
            return 0.5
        
        # Different calculation based on source type
        if analysis.source_type == "youtube_transcript":
            # YouTube: focus on engagement rate and viral factor
            engagement_rate = engagement_metrics.get("engagement_rate", 0.0)
            viral_factor = engagement_metrics.get("viral_factor", 0.0)
            return min(1.0, engagement_rate * 0.7 + viral_factor * 0.3)
        
        elif analysis.source_type == "github_repository":
            # GitHub: focus on community engagement
            return engagement_metrics.get("community_engagement", 0.5)
        
        else:
            # Web search: average of available metrics
            metrics = [v for v in engagement_metrics.values() if isinstance(v, (int, float))]
            return sum(metrics) / len(metrics) if metrics else 0.5
    
    def _calculate_uniqueness_score(self, analysis: MCPAnalysisResult) -> float:
        """Calculate uniqueness score from quality indicators"""
        # Uniqueness comes from high quality and technical depth
        quality_scores = list(analysis.quality_indicators.values())
        
        # Filter technical scores to only include 0-1 normalized values
        technical_scores = []
        for key, value in analysis.technical_metrics.items():
            if isinstance(value, (int, float)) and key != "duration_seconds":
                # Only include normalized metrics
                if 0 <= value <= 1:
                    technical_scores.append(value)
        
        avg_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0.5
        avg_technical = sum(technical_scores) / len(technical_scores) if technical_scores else 0.5
        
        # Ensure result is bounded 0-1
        result = (avg_quality * 0.6 + avg_technical * 0.4)
        return min(1.0, max(0.0, result))
    
    def _calculate_completeness(self, analysis: MCPAnalysisResult) -> float:
        """Calculate completeness from quality indicators"""
        # Look for completeness indicators in quality scores
        completeness_indicators = [
            analysis.quality_indicators.get("content_completeness", 0.0),
            analysis.quality_indicators.get("content_length", 0.0),
            analysis.technical_metrics.get("has_documentation", 0.0)
        ]
        
        valid_indicators = [score for score in completeness_indicators if score > 0]
        return sum(valid_indicators) / len(valid_indicators) if valid_indicators else 0.5
    
    def _calculate_actionability(self, analysis: MCPAnalysisResult) -> float:
        """Calculate actionability from technical metrics"""
        # Actionability comes from tutorials, code examples, and documentation
        actionability_factors = [
            analysis.technical_metrics.get("is_tutorial", 0.0),
            analysis.technical_metrics.get("has_code_examples", 0.0),
            analysis.technical_metrics.get("is_documentation", 0.0)
        ]
        
        valid_factors = [factor for factor in actionability_factors if factor > 0]
        base_actionability = sum(valid_factors) / len(valid_factors) if valid_factors else 0.4
        
        # Boost for technical depth
        technical_boost = analysis.technical_metrics.get("technical_depth", 0.0) * 0.3
        
        return min(1.0, base_actionability + technical_boost)
    
    def _calculate_cross_topic_value(self, analysis: MCPAnalysisResult, content: ContentItem) -> float:
        """Calculate cross-topic value"""
        # Base on number of topics
        base_value = min(1.0, len(content.topics) / 3) if content.topics else 0.1
        
        # Boost for frameworks and libraries (useful across projects)
        if analysis.source_type == "github_repository":
            framework_boost = analysis.technical_metrics.get("is_framework", 0.0) * 0.3
            library_boost = analysis.technical_metrics.get("is_library", 0.0) * 0.2
            base_value += framework_boost + library_boost
        
        # Boost for high authority content
        authority_boost = max(analysis.authority_signals.values()) * 0.2 if analysis.authority_signals else 0.0
        
        return min(1.0, base_value + authority_boost)
    
    def get_strategy_name(self) -> str:
        return "intelligent_mcp"