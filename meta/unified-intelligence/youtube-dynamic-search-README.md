# YouTube Dynamic Search System

## Overview

This system expands content discovery beyond subscribed YouTube channels by dynamically searching for priority topics using configurable search terms and quality thresholds.

## System Components

### Core Files

1. **`youtube-dynamic-search.py`** - Main search engine
   - Configurable search terms for priority topics
   - Rate limiting and error handling
   - Quality scoring and filtering
   - JSON output compatible with digest generator

2. **`youtube-search-integration.py`** - Integration layer
   - Digest generator compatibility
   - Data format standardization
   - Status reporting
   - Sample data generation

3. **`youtube-search-config.json`** - Configuration file
   - Search terms by topic
   - Filtering thresholds
   - Rate limiting settings
   - Output preferences

4. **`daily-digest/youtube-dynamic-search-hook.py`** - Digest integration hook
   - Content retrieval for digest generator
   - Status monitoring
   - Error handling

5. **`youtube-api-implementation-guide.md`** - Implementation guide
   - Real YouTube API integration instructions
   - Multiple API options (YouTube Data API v3, Invidious)
   - Rate limiting and quota management
   - Security considerations

## Directory Structure

```
meta/unified-intelligence/
├── youtube-dynamic-search.py           # Main search engine
├── youtube-search-integration.py       # Integration layer  
├── youtube-search-config.json         # Configuration
├── youtube-api-implementation-guide.md # API implementation guide
├── youtube-dynamic-search-README.md   # This file
└── daily-digest/
    └── youtube-dynamic-search-hook.py  # Digest integration

knowledge-vault/databases/knowledge_vault/content-intelligence/youtube-intelligence/
└── dynamic-search/
    ├── daily/           # Daily search results
    ├── by-topic/        # Results organized by topic
    ├── summaries/       # Search summaries
    └── latest_dynamic_search.json  # Latest results for digest
```

## Features

### Priority Topics

The system searches for these priority topics by default:

- **claude** - Claude AI and Anthropic developments
- **claude-code** - Claude Code IDE and development tools  
- **react** - React framework and ecosystem
- **typescript** - TypeScript language and tooling
- **meta-prompting** - Prompt engineering techniques
- **nextjs** - Next.js React framework

### Search Configuration

Each topic has multiple search terms to maximize discovery:

```json
{
  "search_terms": {
    "claude": [
      "Claude AI tutorial",
      "Claude Code IDE", 
      "Anthropic Claude development",
      "Claude AI programming",
      "Claude Code tutorial",
      "Claude API development"
    ]
  }
}
```

### Quality Filters

- **Recency**: Last 30 days by default
- **View count**: Minimum 100 views
- **Duration**: 2-60 minutes (excludes shorts)
- **Relevance**: Minimum 0.6 relevance score
- **Engagement**: Minimum 0.4 engagement score
- **Unified score**: Minimum 0.5 overall score

### Scoring System

Each video gets multiple scores:

- **Relevance Score** (0-1): Based on title/description matching topic keywords
- **Freshness Score** (0-1): Based on publication date with decay over time
- **Engagement Score** (0-1): Based on views, likes, comments relative to age
- **Unified Score** (0-1): Weighted combination adjusted by topic priority

## Usage

### Basic Usage

```bash
# Run dynamic search with default configuration
python3 youtube-dynamic-search.py

# Run with custom configuration
python3 youtube-dynamic-search.py --config custom-config.json
```

### Integration with Digest Generator

```python
from daily_digest.youtube_dynamic_search_hook import get_youtube_dynamic_content

# Get content for digest
content = get_youtube_dynamic_content(max_videos=15)

if content['status'] == 'success':
    for item in content['content']:
        print(f"{item['title']} - {item['channel']}")
```

### Status Monitoring

```python
from youtube_search_integration import YouTubeSearchIntegration

integration = YouTubeSearchIntegration()
status = integration.get_status()
print(f"System status: {status['status']}")
```

## Configuration

### Search Terms

Add new topics or modify existing ones in `youtube-search-config.json`:

```json
{
  "search_terms": {
    "new_topic": [
      "search term 1",
      "search term 2"
    ]
  }
}
```

### Filters and Thresholds

Adjust quality filters:

```json
{
  "filters": {
    "published_after_days": 30,
    "min_view_count": 100,
    "min_duration_seconds": 120,
    "max_duration_seconds": 3600
  },
  "thresholds": {
    "min_relevance_score": 0.6,
    "min_engagement_score": 0.4,
    "min_unified_score": 0.5,
    "max_results_per_term": 10,
    "max_total_results": 100
  }
}
```

### Rate Limiting

Control API usage:

```json
{
  "rate_limiting": {
    "requests_per_minute": 30,
    "delay_between_requests": 2.0,
    "backoff_multiplier": 1.5,
    "max_retries": 3
  }
}
```

## Output Format

### Individual Video Data

```json
{
  "video_id": "abc123",
  "title": "Video Title",
  "channel_name": "Channel Name",
  "published_at": "2024-07-15T10:00:00Z",
  "view_count": 5000,
  "duration": "PT15M30S",
  "description": "Video description...",
  "thumbnail_url": "https://...",
  "search_term": "Claude AI tutorial",
  "priority_topic": "claude",
  "relevance_score": 0.85,
  "freshness_score": 0.9,
  "engagement_score": 0.75,
  "unified_score": 0.85
}
```

### Search Results Summary

```json
{
  "search_metadata": {
    "timestamp": "2024-07-31T10:00:00Z",
    "topics_searched": ["claude", "react"],
    "total_videos_found": 50,
    "quality_videos_selected": 25
  },
  "top_videos": [...],
  "summary_statistics": {
    "averages": {...},
    "topic_distribution": {...},
    "quality_metrics": {...}
  }
}
```

## Implementation Status

### Current State (Demo Ready)

- ✅ Complete system architecture
- ✅ Configuration management
- ✅ Mock data generation for testing
- ✅ Quality scoring and filtering
- ✅ Integration with digest generator
- ✅ Comprehensive documentation
- ✅ Error handling and rate limiting

### Next Steps (Production Ready)

- 🔄 **Replace mock API calls** with real YouTube API
- 🔄 **Add API key management** and quota monitoring
- 🔄 **Implement caching** for frequently searched terms
- 🔄 **Add automated scheduling** for regular searches
- 🔄 **Enhance error recovery** with exponential backoff

## API Integration

The system currently uses mock data for demonstration. To implement real YouTube search:

1. **Follow the implementation guide**: `youtube-api-implementation-guide.md`
2. **Choose API method**: YouTube Data API v3 (recommended) or Invidious API
3. **Set up credentials**: API keys and environment variables
4. **Replace mock implementation** in `_search_youtube_api()` method
5. **Test with real data** and adjust rate limiting

## Monitoring and Maintenance

### Health Checks

```python
# Check system status
status = integration.get_status()
print(f"Status: {status['status']}")
print(f"Latest results available: {status['latest_results_available']}")
```

### Performance Monitoring

- Monitor API quota usage (YouTube Data API: 10,000 units/day free)
- Track search result quality over time
- Monitor error rates and response times
- Analyze topic distribution and discovery effectiveness

### Regular Maintenance

- Review and update search terms quarterly
- Adjust quality thresholds based on result analysis
- Rotate API keys and update credentials
- Clean up old search result files

## Integration Points

### With Digest Generator

The system integrates seamlessly with the existing digest generator through:

- Standardized content format
- Status reporting API
- Error handling and fallbacks
- Configurable result limits

### With Knowledge Vault

Results are stored in the knowledge vault structure:

- Daily results for historical analysis
- Topic-specific organization for research
- Summary statistics for trend analysis
- Latest results file for real-time access

## Troubleshooting

### Common Issues

**No results found:**
- Check API key and quotas
- Verify search terms are not too specific
- Review quality thresholds (may be too strict)

**Rate limiting errors:**
- Reduce `requests_per_minute` in configuration
- Increase `delay_between_requests`
- Check API provider limits

**Import errors:**
- Ensure all files are in correct directories
- Check Python path configuration
- Verify dependencies are installed

### Debug Mode

Run with verbose logging:

```bash
export LOG_LEVEL=DEBUG
python3 youtube-dynamic-search.py
```

## Contributing

When adding new features:

1. Follow existing code patterns and structure
2. Update configuration schema if needed
3. Add comprehensive error handling
4. Update documentation and examples
5. Test with both mock and real data
6. Consider impact on rate limiting and quotas

## Security Considerations

- Store API keys in environment variables, never in code
- Use HTTPS for all API requests
- Implement proper input validation for search terms
- Monitor for unusual API usage patterns
- Regularly rotate API keys and credentials