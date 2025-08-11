#!/usr/bin/env python3
"""
Claude Intelligence Implementation
Advanced quality scoring for Claude AI and Claude Code content discovery
Implements the enhanced universal quality framework with Claude-specific patterns
"""

import re
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

@dataclass
class ContentItem:
    title: str
    description: str
    content: str
    source: str
    url: str
    author: str
    platform: str
    engagement_metrics: Dict
    metadata: Dict

class TopicCategory(Enum):
    CLAUDE_AI = "claude_ai_content"
    CLAUDE_CODE = "claude_code_development"
    META_PROMPTING = "meta_prompting_techniques"
    AI_WORKFLOWS = "ai_development_workflows"
    GENERAL = "general_content"

class ClaudeIntelligenceScorer:
    """Enhanced quality scorer with Claude-specific intelligence patterns"""
    
    def __init__(self):
        self.topic_patterns = {
            TopicCategory.CLAUDE_AI: {
                'primary': [
                    r'\bclaude\b', r'\banthropic\b', r'\bconstitutional ai\b', 
                    r'\bclaude api\b', r'\bclaude\.ai\b'
                ],
                'secondary': [
                    r'\bai assistant\b', r'\bconversational ai\b', r'\bai safety\b',
                    r'\bhelpful ai\b', r'\bharmless ai\b', r'\bhonest ai\b'
                ],
                'advanced': [
                    r'\bmeta-prompting\b', r'\bprompt engineering\b', 
                    r'\bai coordination\b', r'\bclaude workflows\b'
                ],
                'weight_multiplier': 1.3
            },
            TopicCategory.CLAUDE_CODE: {
                'primary': [
                    r'\bclaude code\b', r'\bclaude\.ai/code\b', r'\bai coding\b',
                    r'\bautomated development\b', r'\bclaude ide\b'
                ],
                'secondary': [
                    r'\bai-assisted development\b', r'\bcode generation\b',
                    r'\bautomated workflow\b', r'\bai productivity\b'
                ],
                'advanced': [
                    r'\bai-assisted architecture\b', r'\bteam collaboration\b',
                    r'\bcode review automation\b', r'\bworkflow optimization\b'
                ],
                'weight_multiplier': 1.4
            },
            TopicCategory.META_PROMPTING: {
                'primary': [
                    r'\bmeta-prompting\b', r'\bprompt engineering\b',
                    r'\bchain of thought\b', r'\bfew shot\b'
                ],
                'secondary': [
                    r'\bprompt optimization\b', r'\bai prompting\b',
                    r'\bprompt design\b', r'\bconstitutional prompting\b'
                ],
                'advanced': [
                    r'\bworkflow automation\b', r'\bmulti-step reasoning\b',
                    r'\bdomain expertise\b', r'\berror handling\b'
                ],
                'weight_multiplier': 1.25
            }
        }
        
        self.authority_sources = {
            'anthropic_official': [
                'anthropic.com', 'claude.ai', 'docs.anthropic.com'
            ],
            'claude_team_verified': [
                'anthropic team', 'claude team', 'anthropic researcher'
            ],
            'claude_community_leaders': [
                # This would be populated with known community leaders
            ]
        }
        
        self.quality_bonuses = {
            'anthropic_official': 0.4,
            'claude_team_verified': 0.3,
            'claude_community_leaders': 0.2,
            'anthropic_research_papers': 0.3,
            'constitutional_ai_principles': 0.2,
            'claude_api_examples': 0.15,
            'anthropic_best_practices': 0.15,
            'safety_considerations': 0.1,
            'meta_prompting_examples': 0.2,
            'claude_code_workflows': 0.25,
            'working_claude_examples': 0.3,
            'end_to_end_workflows': 0.2,
            'ai_assisted_architecture': 0.3
        }

    def detect_topic_category(self, content_item: ContentItem) -> Tuple[TopicCategory, float]:
        """Detect the primary topic category and confidence score"""
        
        text = f"{content_item.title} {content_item.description} {content_item.content}".lower()
        
        category_scores = {}
        
        for category, patterns in self.topic_patterns.items():
            score = 0.0
            
            # Primary pattern matches (highest weight)
            for pattern in patterns['primary']:
                matches = len(re.findall(pattern, text, re.IGNORECASE))
                score += matches * 1.0
            
            # Secondary pattern matches (medium weight)
            for pattern in patterns['secondary']:
                matches = len(re.findall(pattern, text, re.IGNORECASE))
                score += matches * 0.6
            
            # Advanced pattern matches (bonus weight)
            for pattern in patterns['advanced']:
                matches = len(re.findall(pattern, text, re.IGNORECASE))
                score += matches * 0.8
            
            category_scores[category] = score
        
        # Find the category with the highest score
        if not category_scores or max(category_scores.values()) == 0:
            return TopicCategory.GENERAL, 0.0
        
        best_category = max(category_scores.items(), key=lambda x: x[1])
        confidence = min(best_category[1] / 5.0, 1.0)  # Normalize to [0, 1]
        
        return best_category[0], confidence

    def calculate_authority_bonus(self, content_item: ContentItem, topic_category: TopicCategory) -> float:
        """Calculate authority bonus based on source credibility and topic relevance"""
        
        bonus = 0.0
        source_lower = content_item.source.lower()
        author_lower = content_item.author.lower()
        url_lower = content_item.url.lower()
        
        # Check for official Anthropic sources
        if any(domain in url_lower for domain in self.authority_sources['anthropic_official']):
            bonus += self.quality_bonuses['anthropic_official']
        
        # Check for verified team members
        if any(identifier in author_lower for identifier in self.authority_sources['claude_team_verified']):
            bonus += self.quality_bonuses['claude_team_verified']
        
        # Platform-specific authority indicators
        if content_item.platform == 'github':
            stars = content_item.engagement_metrics.get('stars', 0)
            if stars > 10000:
                bonus += 0.15
            elif stars > 1000:
                bonus += 0.1
        
        elif content_item.platform == 'youtube':
            subscribers = content_item.engagement_metrics.get('subscribers', 0)
            if subscribers > 100000:
                bonus += 0.1
            elif subscribers > 10000:
                bonus += 0.05
        
        return min(bonus, 0.4)  # Cap maximum authority bonus

    def calculate_accuracy_bonus(self, content_item: ContentItem, topic_category: TopicCategory) -> float:
        """Calculate accuracy bonus based on content quality indicators"""
        
        bonus = 0.0
        text = f"{content_item.title} {content_item.description} {content_item.content}".lower()
        
        # Constitutional AI principles demonstration
        constitutional_indicators = [
            r'\bconstitutional ai\b', r'\bai safety\b', r'\bharmful\b.*\bavoid\b',
            r'\bresponsible\b.*\bai\b', r'\bethical\b.*\bai\b'
        ]
        
        for pattern in constitutional_indicators:
            if re.search(pattern, text, re.IGNORECASE):
                bonus += self.quality_bonuses['constitutional_ai_principles']
                break
        
        # Working code examples
        code_indicators = [
            r'```[\s\S]*?```',  # Code blocks
            r'\bapi\s+example\b', r'\bworking\s+example\b',
            r'\bimplementation\b', r'\bcode\s+sample\b'
        ]
        
        code_found = any(re.search(pattern, content_item.content, re.IGNORECASE) 
                        for pattern in code_indicators)
        
        if code_found and topic_category == TopicCategory.CLAUDE_CODE:
            bonus += self.quality_bonuses['working_claude_examples']
        elif code_found:
            bonus += self.quality_bonuses['claude_api_examples']
        
        # Safety considerations
        safety_indicators = [
            r'\bsafety\s+consideration\b', r'\bbest\s+practice\b',
            r'\bresponsible\s+use\b', r'\bguideline\b'
        ]
        
        if any(re.search(pattern, text, re.IGNORECASE) for pattern in safety_indicators):
            bonus += self.quality_bonuses['safety_considerations']
        
        return min(bonus, 0.4)  # Cap maximum accuracy bonus

    def calculate_completeness_bonus(self, content_item: ContentItem, topic_category: TopicCategory) -> float:
        """Calculate completeness bonus based on content depth and breadth"""
        
        bonus = 0.0
        text = f"{content_item.title} {content_item.description} {content_item.content}".lower()
        
        # End-to-end workflow coverage
        workflow_indicators = [
            r'\bend-to-end\b', r'\bcomplete\s+workflow\b', r'\bfull\s+example\b',
            r'\bstep-by-step\b', r'\bcomprehensive\s+guide\b'
        ]
        
        if any(re.search(pattern, text, re.IGNORECASE) for pattern in workflow_indicators):
            bonus += self.quality_bonuses['end_to_end_workflows']
        
        # Troubleshooting and best practices
        troubleshooting_indicators = [
            r'\btroubleshooting\b', r'\bcommon\s+issues\b', r'\berror\s+handling\b',
            r'\bbest\s+practices\b', r'\boptimization\b'
        ]
        
        if any(re.search(pattern, text, re.IGNORECASE) for pattern in troubleshooting_indicators):
            bonus += 0.15
        
        # Content length as completeness indicator
        content_length = len(content_item.content)
        if content_length > 5000:  # Substantial content
            bonus += 0.1
        elif content_length > 2000:  # Adequate content
            bonus += 0.05
        
        return min(bonus, 0.3)  # Cap maximum completeness bonus

    def calculate_enhanced_quality_score(self, content_item: ContentItem) -> Dict:
        """Calculate enhanced quality score with Claude-specific intelligence"""
        
        # Step 1: Detect topic category and confidence
        topic_category, topic_confidence = self.detect_topic_category(content_item)
        
        # Step 2: Calculate base quality score (simplified for demonstration)
        base_score = self._calculate_base_quality_score(content_item)
        
        # Step 3: Apply topic-specific weight multiplier
        if topic_category in self.topic_patterns:
            weight_multiplier = self.topic_patterns[topic_category]['weight_multiplier']
            base_score *= weight_multiplier
        
        # Step 4: Calculate topic-specific bonuses
        authority_bonus = self.calculate_authority_bonus(content_item, topic_category)
        accuracy_bonus = self.calculate_accuracy_bonus(content_item, topic_category)
        completeness_bonus = self.calculate_completeness_bonus(content_item, topic_category)
        
        # Step 5: Apply bonuses
        enhanced_score = base_score + authority_bonus + accuracy_bonus + completeness_bonus
        
        # Step 6: Apply topic-specific threshold adjustments
        quality_tier = self._determine_quality_tier(enhanced_score, topic_category)
        
        # Step 7: Clamp to valid range
        final_score = min(max(enhanced_score, 0.0), 1.0)
        
        return {
            'final_score': final_score,
            'base_score': base_score,
            'topic_category': topic_category.value,
            'topic_confidence': topic_confidence,
            'bonuses': {
                'authority': authority_bonus,
                'accuracy': accuracy_bonus,
                'completeness': completeness_bonus,
                'total_bonus': authority_bonus + accuracy_bonus + completeness_bonus
            },
            'quality_tier': quality_tier,
            'recommendations': self._generate_recommendations(content_item, topic_category, final_score)
        }

    def _calculate_base_quality_score(self, content_item: ContentItem) -> float:
        """Calculate base quality score using traditional 5-dimension framework"""
        # Simplified implementation - in practice, this would use the full framework
        
        # Source authority (0.25 weight)
        authority_score = 0.7  # Default moderate authority
        
        # Content accuracy (0.30 weight)  
        accuracy_score = 0.8  # Default good accuracy
        
        # Relevance alignment (0.20 weight)
        relevance_score = 0.75  # Default good relevance
        
        # Completeness depth (0.15 weight) 
        completeness_score = 0.7  # Default moderate completeness
        
        # Constitutional compliance (0.10 weight)
        constitutional_score = 0.9  # Default high compliance
        
        base_score = (
            authority_score * 0.25 +
            accuracy_score * 0.30 +
            relevance_score * 0.20 +
            completeness_score * 0.15 +
            constitutional_score * 0.10
        )
        
        return base_score

    def _determine_quality_tier(self, score: float, topic_category: TopicCategory) -> str:
        """Determine quality tier with topic-specific threshold adjustments"""
        
        # Apply topic-specific threshold adjustments
        if topic_category == TopicCategory.CLAUDE_CODE:
            if score >= 0.80:
                return "auto_approve"
            elif score >= 0.70:
                return "high_quality"
        elif topic_category == TopicCategory.CLAUDE_AI:
            if score >= 0.85:
                return "auto_approve"
            elif score >= 0.75:
                return "high_quality"
        elif topic_category == TopicCategory.META_PROMPTING:
            if score >= 0.85:
                return "auto_approve"
            elif score >= 0.75:
                return "high_quality"
        
        # Standard thresholds
        if score >= 0.90:
            return "auto_approve"
        elif score >= 0.80:
            return "high_quality"
        elif score >= 0.60:
            return "medium_quality"
        elif score >= 0.40:
            return "review_required"
        else:
            return "auto_reject"

    def _generate_recommendations(self, content_item: ContentItem, topic_category: TopicCategory, score: float) -> List[str]:
        """Generate actionable recommendations for content improvement"""
        
        recommendations = []
        
        if score < 0.6:
            recommendations.append("Consider seeking more authoritative sources")
            
        if topic_category in [TopicCategory.CLAUDE_AI, TopicCategory.CLAUDE_CODE]:
            if score < 0.8:
                recommendations.append("Add working code examples or practical demonstrations")
                recommendations.append("Include references to official Anthropic documentation")
            
            if "constitutional ai" not in content_item.content.lower():
                recommendations.append("Consider adding discussion of AI safety and responsible use")
        
        if topic_category == TopicCategory.META_PROMPTING:
            if "example" not in content_item.content.lower():
                recommendations.append("Add practical meta-prompting examples")
        
        if len(content_item.content) < 1000:
            recommendations.append("Expand content depth with more comprehensive coverage")
        
        return recommendations

# Example usage and testing
def test_claude_intelligence_scorer():
    """Test the Claude Intelligence Scorer with sample content"""
    
    scorer = ClaudeIntelligenceScorer()
    
    # Test content: Claude Code workflow example
    test_content = ContentItem(
        title="Advanced Claude Code Workflows for AI-Assisted Development",
        description="Learn how to use Claude Code for automated development workflows with meta-prompting techniques",
        content="""
        # Claude Code Development Workflow
        
        This guide demonstrates end-to-end Claude Code workflows for AI-assisted development.
        
        ## Constitutional AI Principles
        Claude Code follows Constitutional AI principles to ensure responsible AI assistance.
        
        ```python
        # Example Claude Code automation
        def automated_development_workflow():
            # Working code example for Claude integration
            claude_response = claude_api.complete(
                prompt="Generate optimal React component structure",
                context="Following best practices and safety considerations"
            )
            return claude_response
        ```
        
        ## Best Practices and Troubleshooting
        - Always validate AI-generated code
        - Follow Anthropic's recommended practices
        - Implement proper error handling
        
        This comprehensive guide covers complete workflow implementation.
        """,
        source="claude.ai",
        url="https://claude.ai/docs/workflows",
        author="Anthropic Team",
        platform="documentation",
        engagement_metrics={"views": 5000, "upvotes": 250},
        metadata={"official": True, "verified": True}
    )
    
    # Calculate enhanced quality score
    result = scorer.calculate_enhanced_quality_score(test_content)
    
    print("Claude Intelligence Scoring Results:")
    print("=" * 50)
    print(f"Final Score: {result['final_score']:.3f}")
    print(f"Base Score: {result['base_score']:.3f}")
    print(f"Topic Category: {result['topic_category']}")
    print(f"Topic Confidence: {result['topic_confidence']:.3f}")
    print(f"Quality Tier: {result['quality_tier']}")
    print(f"Total Bonus: +{result['bonuses']['total_bonus']:.3f}")
    print(f"Bonuses Breakdown:")
    for bonus_type, value in result['bonuses'].items():
        if bonus_type != 'total_bonus':
            print(f"  {bonus_type.title()}: +{value:.3f}")
    
    if result['recommendations']:
        print(f"Recommendations:")
        for rec in result['recommendations']:
            print(f"  • {rec}")

if __name__ == "__main__":
    test_claude_intelligence_scorer()