# MCP Server Recommendation Engine

AI-powered system for analyzing subagent context and automatically recommending relevant MCP servers with tier-based prioritization and integration guidance.

## Core Recommendation Algorithm

### 1. Domain Analysis Engine

**Input Sources:**
- Subagent name and description
- Core responsibilities section content
- Tool configuration and technology stack mentions
- Assessment instructions and deliverable specifications

**Analysis Process:**
```python
class DomainAnalysisEngine:
    def __init__(self, domain_mappings_path="ai/mcp-integration/domain-server-mappings.yaml"):
        self.domain_mappings = self.load_domain_mappings(domain_mappings_path)
        self.keyword_weights = self.initialize_keyword_weights()
        
    def analyze_subagent_domain(self, subagent_config):
        """Analyze subagent configuration to identify relevant domains"""
        
        # Extract text content for analysis
        analysis_text = self.extract_analysis_text(subagent_config)
        
        # Calculate domain relevance scores
        domain_scores = {}
        for domain, config in self.domain_mappings['domain_mappings'].items():
            score = self.calculate_domain_relevance(analysis_text, config['keywords'])
            if score > 0:
                domain_scores[domain] = {
                    'relevance_score': score,
                    'confidence': self.calculate_confidence(score, config['keywords']),
                    'domain_config': config
                }
        
        return self.rank_domains(domain_scores)
    
    def calculate_domain_relevance(self, text, keywords):
        """Calculate relevance score based on keyword matching and context"""
        text_lower = text.lower()
        
        # Direct keyword matches
        direct_matches = sum(1 for keyword in keywords if keyword in text_lower)
        
        # Contextual relevance (nearby related terms)
        contextual_score = self.calculate_contextual_relevance(text_lower, keywords)
        
        # Weighted scoring
        total_score = (direct_matches * 2.0) + (contextual_score * 1.0)
        
        # Normalize by keyword count
        normalized_score = total_score / len(keywords) if keywords else 0
        
        return min(normalized_score * 10, 10)  # Scale to 0-10
```

### 2. MCP Server Matching Engine

**Server Selection Logic:**
```python
class MCPServerMatcher:
    def __init__(self, domain_mappings):
        self.domain_mappings = domain_mappings
        self.tier_priorities = domain_mappings['tier_priorities']
        self.quality_thresholds = domain_mappings['quality_thresholds']
        
    def recommend_mcp_servers(self, domain_analysis, subagent_priority="medium"):
        """Generate prioritized MCP server recommendations"""
        
        recommendations = []
        
        for domain_name, domain_data in domain_analysis.items():
            if domain_data['confidence'] < 0.3:  # Skip low-confidence domains
                continue
                
            domain_config = domain_data['domain_config']
            
            for server in domain_config['primary_servers']:
                # Calculate recommendation score
                recommendation_score = self.calculate_recommendation_score(
                    server, domain_data, subagent_priority
                )
                
                if recommendation_score >= self.get_minimum_threshold(subagent_priority):
                    recommendations.append({
                        'server_id': server['server_id'],
                        'server_name': server['name'],
                        'domain': domain_name,
                        'tier': server['tier'],
                        'composite_score': server['composite_score'],
                        'recommendation_score': recommendation_score,
                        'integration_priority': server['integration_priority'],
                        'setup_complexity': server['setup_complexity'],
                        'use_cases': server['use_cases'],
                        'profile_path': server['profile_path'],
                        'domain_relevance': domain_data['relevance_score'],
                        'confidence': domain_data['confidence']
                    })
        
        return self.prioritize_recommendations(recommendations)
    
    def calculate_recommendation_score(self, server, domain_data, subagent_priority):
        """Calculate overall recommendation score for server"""
        
        # Base score from MCP server composite score
        base_score = server['composite_score']
        
        # Tier priority boost
        tier_boost = self.tier_priorities[f"tier_{server['tier']}"]['priority_score']
        
        # Domain relevance multiplier
        relevance_multiplier = domain_data['relevance_score'] / 10.0
        
        # Priority alignment score
        priority_alignment = self.calculate_priority_alignment(
            server['integration_priority'], subagent_priority
        )
        
        # Setup complexity penalty (higher complexity = lower score for medium/low priority)
        complexity_penalty = self.calculate_complexity_penalty(
            server['setup_complexity'], subagent_priority
        )
        
        # Final calculation
        recommendation_score = (
            (base_score * 0.4) +
            (tier_boost * 0.3) +
            (relevance_multiplier * 10 * 0.2) +
            (priority_alignment * 0.1)
        ) - complexity_penalty
        
        return max(0, min(10, recommendation_score))
```

### 3. Cross-Domain Analysis

**Multi-Technology Subagent Support:**
```python
class CrossDomainAnalyzer:
    def analyze_cross_domain_requirements(self, domain_analysis):
        """Identify patterns requiring multiple MCP servers"""
        
        cross_domain_patterns = []
        
        # Check for known cross-domain combinations
        for pattern_name, pattern_config in self.domain_mappings['cross_domain_mappings'].items():
            pattern_domains = pattern_config['domains']
            
            # Calculate overlap with identified domains
            overlap = set(domain_analysis.keys()).intersection(set(pattern_domains))
            overlap_ratio = len(overlap) / len(pattern_domains)
            
            if overlap_ratio >= 0.5:  # At least 50% domain overlap
                cross_domain_patterns.append({
                    'pattern_name': pattern_name,
                    'domains': pattern_domains,
                    'recommended_servers': pattern_config['recommended_servers'],
                    'overlap_ratio': overlap_ratio,
                    'confidence': self.calculate_pattern_confidence(overlap, domain_analysis)
                })
        
        return sorted(cross_domain_patterns, key=lambda x: x['confidence'], reverse=True)
```

## Integration Template Selection

### Template Matching Logic
```python
class TemplateSelector:
    def __init__(self, templates_path="ai/mcp-integration/subagent-templates/"):
        self.templates_path = templates_path
        self.available_templates = self.discover_templates()
        
    def select_integration_templates(self, recommendations, domain_analysis):
        """Select appropriate integration templates for recommendations"""
        
        template_selections = []
        
        # Primary domain template
        primary_domain = max(domain_analysis.keys(), 
                           key=lambda x: domain_analysis[x]['relevance_score'])
        
        primary_template = self.match_domain_to_template(primary_domain)
        if primary_template:
            template_selections.append({
                'template_type': 'primary_domain',
                'template_path': primary_template,
                'domain': primary_domain,
                'applicable_servers': self.get_servers_for_domain(recommendations, primary_domain)
            })
        
        # Server-specific templates
        for recommendation in recommendations[:3]:  # Top 3 recommendations
            server_template = self.match_server_to_template(recommendation['server_id'])
            if server_template and server_template not in [t['template_path'] for t in template_selections]:
                template_selections.append({
                    'template_type': 'server_specific',
                    'template_path': server_template,
                    'server': recommendation,
                    'integration_guidance': self.generate_server_integration_guidance(recommendation)
                })
        
        # General template as fallback
        if not template_selections:
            template_selections.append({
                'template_type': 'general',
                'template_path': f"{self.templates_path}general-mcp-integration-template.md",
                'applicable_servers': recommendations[:5]
            })
        
        return template_selections
```

## Quality Assessment and Filtering

### Recommendation Quality Filters
```python
class QualityFilter:
    def apply_quality_filters(self, recommendations, quality_requirements=None):
        """Apply quality filters to recommendations"""
        
        if not quality_requirements:
            quality_requirements = self.get_default_quality_requirements()
        
        filtered_recommendations = []
        
        for rec in recommendations:
            quality_score = self.calculate_quality_score(rec)
            
            if self.meets_quality_requirements(rec, quality_requirements, quality_score):
                rec['quality_score'] = quality_score
                rec['quality_assessment'] = self.generate_quality_assessment(rec)
                filtered_recommendations.append(rec)
        
        return self.rank_by_quality(filtered_recommendations)
    
    def calculate_quality_score(self, recommendation):
        """Calculate overall quality score for recommendation"""
        
        # Composite score weight (40%)
        composite_weight = recommendation['composite_score'] * 0.4
        
        # Tier priority weight (30%)
        tier_weight = self.tier_priorities[f"tier_{recommendation['tier']}"]['priority_score'] * 0.3 / 10
        
        # Domain relevance weight (20%)
        relevance_weight = recommendation['domain_relevance'] * 0.2
        
        # Confidence weight (10%)
        confidence_weight = recommendation['confidence'] * 10 * 0.1
        
        return composite_weight + tier_weight + relevance_weight + confidence_weight
```

## Implementation Guidelines

### Usage Example
```python
class MCPRecommendationSystem:
    def __init__(self):
        self.domain_analyzer = DomainAnalysisEngine()
        self.server_matcher = MCPServerMatcher(self.domain_analyzer.domain_mappings)
        self.template_selector = TemplateSelector()
        self.quality_filter = QualityFilter()
        
    def generate_recommendations(self, subagent_config, max_recommendations=5):
        """Generate comprehensive MCP server recommendations"""
        
        # Step 1: Analyze subagent domain
        domain_analysis = self.domain_analyzer.analyze_subagent_domain(subagent_config)
        
        if not domain_analysis:
            return self.generate_fallback_recommendations()
        
        # Step 2: Get MCP server recommendations
        raw_recommendations = self.server_matcher.recommend_mcp_servers(
            domain_analysis, 
            subagent_config.get('priority', 'medium')
        )
        
        # Step 3: Apply quality filters
        quality_filtered = self.quality_filter.apply_quality_filters(raw_recommendations)
        
        # Step 4: Select integration templates
        templates = self.template_selector.select_integration_templates(
            quality_filtered[:max_recommendations], 
            domain_analysis
        )
        
        # Step 5: Generate comprehensive report
        return self.generate_recommendation_report(
            subagent_config,
            domain_analysis,
            quality_filtered[:max_recommendations],
            templates
        )
```

### Integration with Validator
```python
# Usage in claude-agent-validator.md context
def validate_mcp_integration(subagent_config):
    """Validate and recommend MCP integration for subagent"""
    
    recommendation_system = MCPRecommendationSystem()
    recommendations = recommendation_system.generate_recommendations(subagent_config)
    
    validation_report = {
        'domain_analysis': recommendations['domain_analysis'],
        'recommended_servers': recommendations['servers'],
        'integration_templates': recommendations['templates'],
        'quality_assessment': recommendations['quality_metrics'],
        'implementation_guidance': recommendations['implementation_steps'],
        'monitoring_requirements': recommendations['monitoring_setup']
    }
    
    return validation_report
```

## Performance and Caching

### Optimization Strategies
- **Domain Analysis Caching**: Cache keyword analysis results for 1 hour
- **Server Metadata Caching**: Cache MCP server information for 4 hours
- **Template Caching**: Cache template discovery and matching for 24 hours
- **Recommendation Caching**: Cache similar subagent recommendations for 2 hours

### Monitoring and Metrics
- **Recommendation Accuracy**: Track user acceptance rate of recommendations
- **Domain Classification Accuracy**: Monitor domain identification precision
- **Integration Success Rate**: Track successful MCP server integrations
- **Performance Metrics**: Response time and resource usage optimization

This recommendation engine provides intelligent, context-aware MCP server suggestions that enhance AI subagents with relevant real-time capabilities while maintaining quality standards and implementation best practices.