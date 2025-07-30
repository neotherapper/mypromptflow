# Topic Deployment Guide

## Overview

This guide provides step-by-step instructions for deploying intelligent monitoring for any topic using the Universal Topic Intelligence System.

## Prerequisites

- Access to MCP server ecosystem via `@meta/mcp-system/`
- Knowledge vault setup for content storage
- AI agent framework with 4-level hierarchy capability

## Deployment Process

### Phase 1: Topic Definition and Planning

#### Step 1: Define Topic Scope
```yaml
# Use this template to define your topic
topic_metadata:
  name: "Your Topic Name"
  slug: "your-topic-slug"
  description: "Clear description of what this topic covers"
  priority_level: "high|medium|low"
  monitoring_frequency: "realtime|hourly|daily|weekly"
  keywords_primary: ["key", "terms", "for", "topic"]
  keywords_secondary: ["related", "context", "terms"]
  keywords_exclusion: ["noise", "terms", "to", "filter"]
```

#### Step 2: Source Discovery
Identify sources across three tiers:

**Tier 1 - Official Sources**:
- Government agencies or regulatory bodies
- Primary company or organization websites
- Official documentation and announcement channels
- Academic institutions and research centers

**Tier 2 - Community Sources**:
- Expert blogs and analysis sites
- Specialized news publications
- Professional YouTube channels
- Industry newsletters and publications

**Tier 3 - Aggregator Sources**:
- Reddit communities and discussion forums
- Social media discussions and hashtags
- News aggregators and curated lists
- Professional networking groups

#### Step 3: MCP Server Mapping
Map appropriate MCP servers for each source type:

```yaml
mcp_server_mapping:
  fetch_server:
    use_cases: ["Official websites", "News sites", "Blog content"]
  github_server:
    use_cases: ["Repository monitoring", "Release tracking", "Issue discussions"]
    repositories: ["owner/repo", "other/repo"]
  youtube_server:
    use_cases: ["Expert channels", "Conference talks", "Educational content"]
    channels: ["channel_id_1", "channel_id_2"]
  playwright_server:
    use_cases: ["Dynamic content", "Social media", "Complex sites"]
```

### Phase 2: Configuration and Quality Setup

#### Step 4: Quality Threshold Configuration
```yaml
content_analysis:
  quality_thresholds:
    minimum_relevance_score: 0.6    # Adjust based on topic noise level
    minimum_authority_score: 0.5    # Adjust based on authority distribution
    minimum_significance_score: 0.4  # Adjust based on topic activity level

  significance_indicators:
    high_significance:
      - "Major announcements and updates"
      - "Regulatory or policy changes"
      - "Breakthrough developments"
    medium_significance:
      - "Expert analysis and opinions"
      - "Community discussions and trends"
    low_significance:
      - "Routine updates and minor news"
      - "Speculation and rumors"
```

#### Step 5: Agent Specialization Setup
Configure agents for topic-specific expertise:

```yaml
agent_specialization:
  content_specialists:
    technical_analyst:
      expertise_areas: ["domain_specific_tech", "implementation_details"]
      validation_criteria: ["technical_accuracy", "feasibility"]
    
    market_impact_specialist:
      expertise_areas: ["business_implications", "adoption_patterns"]
      validation_criteria: ["market_relevance", "economic_impact"]
    
    sentiment_analyst:
      expertise_areas: ["community_sentiment", "expert_opinions"]
      validation_criteria: ["sentiment_accuracy", "trend_identification"]
```

### Phase 3: Integration and Testing

#### Step 6: Knowledge Vault Integration
Set up organized storage for monitored content:

```yaml
file_organization:
  base_path: "knowledge-vault/topics/{topic_slug}/"
  structure:
    config: "config/"           # Topic configuration files
    news: "news/"              # Daily news and updates
    sources: "sources/"        # Source profiles and metadata
    analysis: "analysis/"      # Analysis reports and insights
    relationships: "relationships/"  # Cross-topic connections
    
  naming_conventions:
    daily_files: "YYYY-MM-DD-{source_tier}.md"
    weekly_files: "YYYY-WW-weekly-digest.md"
    analysis_files: "YYYY-MM-DD-{analysis_type}.md"
```

#### Step 7: Cross-Topic Integration
Configure relationships with existing topics:

```yaml
cross_topic_integration:
  relationship_types:
    - type: "complementary"
      targets: ["related_topic_1", "related_topic_2"]
    - type: "competitive"  
      targets: ["competing_topic"]
    - type: "dependent"
      targets: ["dependency_topic"]
      
  shared_sources:
    identification_patterns:
      - "Sources covering multiple related topics"
    resource_optimization: true
```

### Phase 4: Deployment and Monitoring

#### Step 8: Deploy Agent Framework
1. **Queen Agent Setup**: Configure universal orchestration
2. **Architect Agent Deployment**: Deploy topic-specific strategy agents
3. **Specialist Agent Configuration**: Set up content processing experts
4. **Worker Agent Pool**: Deploy task execution specialists

#### Step 9: Performance Monitoring Setup
```yaml
performance_monitoring:
  success_metrics:
    coverage_percentage: 95      # Target coverage of significant developments
    relevance_accuracy: 90       # Target accuracy of content relevance
    false_positive_rate: 10      # Maximum acceptable noise level
    response_time: 600           # Maximum processing time (seconds)
    
  monitoring_intervals:
    real_time_sources: 300       # 5 minutes for critical sources
    high_priority_sources: 1800  # 30 minutes for important sources
    medium_priority_sources: 3600 # 1 hour for regular sources
    low_priority_sources: 21600  # 6 hours for background sources
```

#### Step 10: Quality Assurance Validation
- Test source connectivity and content extraction
- Validate keyword effectiveness for relevance detection
- Confirm agent coordination and task assignment
- Verify quality thresholds produce expected results

## Post-Deployment Operations

### Daily Operations
- Review daily digest files for topic developments
- Monitor agent performance and resource utilization
- Check quality metrics and adjust thresholds if needed
- Identify new sources or changing patterns

### Weekly Optimization
- Analyze weekly digest for trends and patterns
- Review cross-topic relationships and shared resources
- Optimize agent specialization based on content patterns
- Update source authorities and quality assessments

### Monthly Evolution
- Evaluate overall topic monitoring effectiveness
- Update topic configuration based on learned patterns
- Expand or refine source lists based on coverage analysis
- Integrate feedback from usage patterns and outcomes

## Troubleshooting

### Common Issues and Solutions

**Low Coverage (< 90%)**:
- Review source list for gaps in key areas
- Check MCP server connectivity and rate limiting
- Verify keyword effectiveness for content detection
- Consider expanding to additional source tiers

**High False Positive Rate (> 15%)**:
- Tighten relevance scoring criteria
- Add exclusion keywords for common noise patterns
- Improve source quality filtering
- Enhance significance indicator definitions

**Poor Content Quality**:
- Review and adjust quality thresholds
- Validate source authority assessments
- Improve agent specialization criteria
- Check constitutional AI compliance settings

**Resource Optimization Issues**:
- Review cross-topic coordination effectiveness
- Optimize shared source detection and utilization
- Balance resource allocation across topic priorities
- Consider agent pool scaling for high-activity periods

## Success Metrics

### Deployment Success Indicators
- ✅ All configured sources accessible and monitored
- ✅ Agent coordination functioning across all levels
- ✅ Content flowing into knowledge vault with proper organization
- ✅ Quality metrics meeting target thresholds
- ✅ Cross-topic integration operational (if applicable)

### Operational Success Metrics
- **Coverage**: 95% of significant developments captured within target timeframes
- **Accuracy**: 90% relevance accuracy in captured content
- **Efficiency**: Response times under 10 minutes for critical developments
- **Quality**: Constitutional AI compliance at 100%
- **Integration**: Successful coordination with existing systems

This deployment guide ensures systematic, high-quality implementation of topic monitoring that scales across any domain while maintaining constitutional AI compliance and optimal resource utilization.