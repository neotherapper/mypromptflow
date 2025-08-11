#!/usr/bin/env python3
"""
Quality Scorer
Implements quality scoring based on topic configuration rules
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import re
import logging

from .universal_source_monitor import ContentItem


@dataclass
class QualityScore:
    """Quality score result"""
    total_score: float  # 0.0 to 1.0
    category: str  # critical, high, medium, low
    components: Dict[str, float]  # Individual score components
    rules_applied: List[str]  # Rules that were applied
    reasoning: str  # Explanation of scoring


class TopicQualityScorer:
    """
    Scores content quality based on topic-specific configuration
    """
    
    def __init__(self, quality_config: Dict[str, Any]):
        """
        Initialize with quality configuration from topic config
        
        Args:
            quality_config: Quality configuration section from topic YAML
        """
        self.thresholds = quality_config.get("thresholds", {
            "critical": 0.9,
            "high": 0.75,
            "medium": 0.55,
            "low": 0.35
        })
        
        self.weights = quality_config.get("weights", {
            "source_authority": 0.25,
            "content_accuracy": 0.25,
            "relevance_alignment": 0.20,
            "completeness_depth": 0.15,
            "constitutional_compliance": 0.15
        })
        
        self.topic_rules = quality_config.get("topic_specific_rules", [])
        self.logger = logging.getLogger("TopicQualityScorer")
        
    def score_content(self, item: ContentItem) -> QualityScore:
        """
        Score a content item based on quality configuration
        
        Args:
            item: Content item to score
            
        Returns:
            Quality score result
        """
        components = {}
        rules_applied = []
        
        # Calculate base components
        components["source_authority"] = self._score_source_authority(item)
        components["content_accuracy"] = self._score_content_accuracy(item)
        components["relevance_alignment"] = self._score_relevance(item)
        components["completeness_depth"] = self._score_completeness(item)
        components["constitutional_compliance"] = self._score_compliance(item)
        
        # Calculate weighted base score
        base_score = 0.0
        for component, value in components.items():
            weight = self.weights.get(component, 0.0)
            base_score += value * weight
        
        # Apply topic-specific rules
        modified_score = base_score
        for rule in self.topic_rules:
            if self._evaluate_rule_condition(rule, item):
                modified_score = self._apply_rule_action(rule, modified_score)
                rules_applied.append(rule.get("rule", "unnamed_rule"))
        
        # Ensure score is within bounds
        final_score = max(0.0, min(1.0, modified_score))
        
        # Determine category
        category = self._determine_category(final_score)
        
        # Generate reasoning
        reasoning = self._generate_reasoning(components, rules_applied, final_score)
        
        return QualityScore(
            total_score=final_score,
            category=category,
            components=components,
            rules_applied=rules_applied,
            reasoning=reasoning
        )
    
    def _score_source_authority(self, item: ContentItem) -> float:
        """Score based on source authority"""
        # Get from metadata if available
        authority = item.metadata.get("source_authority", 0.5)
        
        # Boost for official sources
        if item.metadata.get("source_type") == "official":
            authority = min(1.0, authority + 0.2)
        
        return authority
    
    def _score_content_accuracy(self, item: ContentItem) -> float:
        """Score content accuracy (simplified heuristic)"""
        score = 0.5  # Base score
        
        content = (item.content or "").lower()
        
        # Positive indicators
        if any(word in content for word in ["verified", "confirmed", "official"]):
            score += 0.2
        
        # Check for citations/references
        if "http://" in content or "https://" in content:
            score += 0.1
        
        # Negative indicators
        if any(word in content for word in ["rumor", "unconfirmed", "allegedly"]):
            score -= 0.3
        
        return max(0.0, min(1.0, score))
    
    def _score_relevance(self, item: ContentItem) -> float:
        """Score relevance to topic"""
        # Check if primary topics are present
        if not item.topics:
            return 0.3
        
        # Higher score for more specific topics
        topic_count = len(item.topics)
        if topic_count == 1:
            return 0.9  # Very focused
        elif topic_count <= 3:
            return 0.7  # Reasonably focused
        else:
            return 0.5  # Broad coverage
    
    def _score_completeness(self, item: ContentItem) -> float:
        """Score content completeness"""
        if not item.content:
            return 0.2
        
        content_length = len(item.content)
        
        # Score based on length
        if content_length > 1500:
            length_score = 1.0
        elif content_length > 800:
            length_score = 0.8
        elif content_length > 400:
            length_score = 0.6
        elif content_length > 200:
            length_score = 0.4
        else:
            length_score = 0.2
        
        # Check for structure
        has_paragraphs = "\n\n" in item.content
        has_sections = any(marker in item.content for marker in ["##", "###", "<h2>", "<h3>"])
        
        structure_score = 0.5
        if has_paragraphs:
            structure_score += 0.25
        if has_sections:
            structure_score += 0.25
        
        return (length_score + structure_score) / 2
    
    def _score_compliance(self, item: ContentItem) -> float:
        """Score constitutional AI compliance"""
        score = 0.8  # Assume good by default
        
        content_lower = (item.title + " " + (item.content or "")).lower()
        
        # Check for harmful content indicators (simplified)
        harmful_indicators = ["fake", "scam", "illegal", "pirated", "leaked"]
        for indicator in harmful_indicators:
            if indicator in content_lower:
                score -= 0.3
        
        # Check for balanced presentation
        if "however" in content_lower or "on the other hand" in content_lower:
            score += 0.1  # Shows balanced perspective
        
        return max(0.0, min(1.0, score))
    
    def _evaluate_rule_condition(self, rule: Dict, item: ContentItem) -> bool:
        """Evaluate if a rule condition matches"""
        condition = rule.get("condition", "")
        
        # Parse simple conditions (this is a simplified parser)
        # Format: "field operator value [AND/OR field operator value]"
        
        # Handle source matching
        if "source =" in condition:
            source_match = re.search(r"source = '([^']+)'", condition)
            if source_match:
                expected_source = source_match.group(1)
                if item.source_id != expected_source:
                    return False
        
        # Handle content contains
        if "content contains" in condition or "title contains" in condition:
            # Extract all quoted strings after "contains"
            contains_patterns = re.findall(r"contains '([^']+)'", condition)
            
            content_to_check = item.title.lower()
            if item.content:
                content_to_check += " " + item.content.lower()
            
            # Check if any pattern matches (OR logic for multiple patterns)
            matches = False
            for pattern in contains_patterns:
                if pattern.lower() in content_to_check:
                    matches = True
                    break
            
            # Handle OR conditions
            if " or " in condition.lower():
                # For OR conditions, we already checked if any pattern matches
                return matches
            elif " and " in condition.lower():
                # For AND conditions, need additional checks
                # This is simplified - would need more complex parsing for full support
                return matches
            else:
                return matches
        
        # Handle priority matching
        if "priority =" in condition:
            priority_match = re.search(r"priority = ([^\s]+)", condition)
            if priority_match:
                expected_priority = priority_match.group(1)
                current_priority = item.metadata.get("priority_level", "medium")
                if current_priority != expected_priority:
                    return False
        
        # If no specific conditions matched, return True for catch-all rules
        if not condition:
            return True
        
        # Default to false if we couldn't parse the condition
        return False
    
    def _apply_rule_action(self, rule: Dict, current_score: float) -> float:
        """Apply a rule action to modify score"""
        action = rule.get("action", "")
        
        # Parse action
        if "multiply_score by" in action:
            multiplier_match = re.search(r"multiply_score by ([\d.]+)", action)
            if multiplier_match:
                multiplier = float(multiplier_match.group(1))
                return current_score * multiplier
        
        elif "add_score" in action:
            addition_match = re.search(r"add_score ([\d.]+)", action)
            if addition_match:
                addition = float(addition_match.group(1))
                return current_score + addition
        
        elif "set_score to" in action:
            score_match = re.search(r"set_score to ([\d.]+)", action)
            if score_match:
                new_score = float(score_match.group(1))
                return new_score
        
        # No action matched, return unchanged
        return current_score
    
    def _determine_category(self, score: float) -> str:
        """Determine quality category based on score"""
        if score >= self.thresholds.get("critical", 0.9):
            return "critical"
        elif score >= self.thresholds.get("high", 0.75):
            return "high"
        elif score >= self.thresholds.get("medium", 0.55):
            return "medium"
        elif score >= self.thresholds.get("low", 0.35):
            return "low"
        else:
            return "noise"
    
    def _generate_reasoning(self, components: Dict[str, float], 
                           rules_applied: List[str], 
                           final_score: float) -> str:
        """Generate explanation for the scoring"""
        reasoning_parts = []
        
        # Describe component scores
        high_components = [k for k, v in components.items() if v > 0.7]
        low_components = [k for k, v in components.items() if v < 0.4]
        
        if high_components:
            reasoning_parts.append(f"Strong in: {', '.join(high_components)}")
        
        if low_components:
            reasoning_parts.append(f"Weak in: {', '.join(low_components)}")
        
        # Mention rules applied
        if rules_applied:
            reasoning_parts.append(f"Rules applied: {', '.join(rules_applied)}")
        
        # Overall assessment
        if final_score > 0.8:
            reasoning_parts.append("High-quality content recommended for priority processing")
        elif final_score > 0.6:
            reasoning_parts.append("Good quality content suitable for standard processing")
        elif final_score > 0.4:
            reasoning_parts.append("Moderate quality, may require verification")
        else:
            reasoning_parts.append("Low quality, consider filtering or manual review")
        
        return ". ".join(reasoning_parts)