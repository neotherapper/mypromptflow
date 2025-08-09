# Reddit Dynamic Discovery System

A comprehensive system for monitoring priority topics across Reddit's ecosystem, designed to discover high-quality discussions about Claude AI, React, TypeScript, meta-prompting, and other key technologies.

## Features

### 🎯 Priority Topic Monitoring
- **Targeted Subreddits**: Monitors r/Claude-ai, r/typescript, r/PromptEngineering, r/reactjs, r/programming
- **Cross-Subreddit Search**: Searches for priority topics across multiple relevant subreddits
- **Quality Filtering**: Filters posts by upvotes (minimum 50), recency (last 7 days), and quality indicators
- **Topic Scoring**: Advanced scoring system based on priority topics configuration

### 🔍 Discovery Methods
1. **RSS Monitoring**: Monitors priority subrededdits via RSS feeds
2. **API Search**: Uses Reddit API for cross-subreddit search (optional)
3. **Quality Assessment**: Evaluates posts based on engagement and content quality
4. **Deduplication**: Removes duplicate posts across discovery methods

### 📊 Priority Topics
- **Claude AI**: Claude, Anthropic developments, Claude Code
- **React**: React framework, hooks, components, ecosystem
- **TypeScript**: Type safety, configuration, tooling
- **Meta-Prompting**: Prompt engineering, chain of thought, few-shot learning
- **Next.js**: App router, server components, full-stack React

### 🛡️ Quality Standards
- **Minimum 50 upvotes** for inclusion
- **Last 7 days** recency filter
- **Quality keyword detection** (comprehensive, detailed, guide, tutorial)
- **Anti-spam filtering** (excludes help requests, beginner questions)
- **Content length requirements** (minimum 100 characters)

## Installation

```bash
# Run the setup script
chmod +x setup-reddit-dynamic-discovery.sh
./setup-reddit-dynamic-discovery.sh
```

The setup script will:
- Create Python virtual environment
- Install required packages (requests, feedparser, praw)
- Create storage directories
- Set up configuration files
- Create test and environment scripts

## Configuration

### Basic Configuration
The system works out-of-the-box with RSS monitoring. Configuration is stored in `reddit-dynamic-discovery-config.json`:

```json
{
  "priority_subreddits": ["Claude", "AnthropicAI", "typescript", "reactjs", "PromptEngineering"],
  "quality_thresholds": {
    "min_upvotes": 50,
    "min_comments": 5,
    "max_age_days": 7
  }
}
```

### Reddit API Setup (Optional)
For enhanced search capabilities:

1. Create Reddit app at https://www.reddit.com/prefs/apps
2. Copy `.env.template` to `.env`
3. Add your credentials:
```bash
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
```

## Usage

### Basic Usage
```bash
# Activate virtual environment
source venv/bin/activate

# Run discovery system
python reddit-dynamic-discovery.py
```

### Advanced Usage
```python
from reddit_dynamic_discovery import RedditDynamicDiscovery

# Initialize with custom config
discovery = RedditDynamicDiscovery("custom-config.json")

# Run discovery cycle
result = discovery.run_discovery_cycle()

if result["success"]:
    print(f"Discovered {result['posts_discovered']} posts")
    print(f"Results saved to: {result['batch_directory']}")
```

## Output Structure

### Storage Directory
```
knowledge-vault/databases/knowledge_vault/content-intelligence/reddit-intelligence/dynamic-discovery/
├── reddit_discovery_2025-08-01_14-30-15/
│   ├── all_posts.json                 # All discovered posts
│   ├── claude_posts.json             # Claude-specific posts
│   ├── react_posts.json              # React-specific posts
│   ├── typescript_posts.json         # TypeScript-specific posts
│   ├── meta-prompting_posts.json     # Meta-prompting posts
│   └── digest_ready.json             # High-score posts for digest
```

### Post Data Structure
```json
{
  "post_id": "abc123",
  "title": "Comprehensive Guide to React Server Components",
  "url": "https://reddit.com/r/reactjs/comments/abc123/...",
  "subreddit": "reactjs",
  "score": 285,
  "num_comments": 47,
  "priority_topics": ["react", "nextjs"],
  "topic_score": 1.8,
  "quality_score": 2.3,
  "discovery_method": "rss",
  "published": "2025-08-01T10:30:00"
}
```

## Integration

### Daily Digest Integration
The system outputs `digest_ready.json` files compatible with the digest generator:

```bash
# Results are automatically compatible with
python content-digest-generator.py
```

### Priority Topic Scoring
Posts are scored based on:
- **Topic Relevance**: Matches against priority topics configuration
- **Quality Indicators**: Engagement metrics and content quality
- **Combination Bonuses**: Extra scoring for topic combinations (e.g., React + TypeScript)

## Monitoring and Logging

### Logs
- **Main Log**: `reddit-dynamic-discovery.log`
- **State Tracking**: `reddit-dynamic-discovery-state.json`
- **Processing Queue**: Discovery results queue for further processing

### State Management
The system tracks:
- Previously processed posts (deduplication)
- Discovery statistics and history
- Rate limiting and API usage
- Search query performance

## Rate Limiting and Guidelines

### Reddit API Compliance
- **Conservative delays**: 2-4 seconds between RSS requests
- **Search rate limiting**: 3-5 seconds between API searches
- **User agent identification**: Educational research purposes
- **Respect robots.txt**: Follows Reddit's guidelines

### Quality Thresholds
- **Minimum engagement**: 50+ upvotes, 5+ comments
- **Recency filter**: Last 7 days by default
- **Content quality**: Avoids low-quality patterns
- **Topic relevance**: Priority topic keyword matching

## Error Handling

### Robust Error Recovery
- **Network failures**: Retry logic with exponential backoff
- **API rate limits**: Automatic delay and retry
- **Invalid responses**: Graceful degradation to RSS-only mode
- **Missing credentials**: Falls back to RSS monitoring

### Logging and Debugging
```bash
# Check system status
python test_reddit_discovery.py

# View recent logs
tail -f reddit-dynamic-discovery.log

# Check discovery state
cat reddit-dynamic-discovery-state.json
```

## Performance

### Efficiency Features
- **Deduplication**: Avoids processing same posts multiple times
- **Batch processing**: Groups related operations
- **Selective storage**: Only saves high-quality posts
- **Memory management**: Processes posts in streams

### Scalability
- **Configurable limits**: Adjustable search result limits
- **Priority queues**: High-priority subreddits processed first
- **Storage optimization**: JSON files with compression support

## Troubleshooting

### Common Issues

**No posts discovered:**
```bash
# Check configuration
python test_reddit_discovery.py

# Verify network connectivity
curl -I https://www.reddit.com/r/programming/.rss

# Check quality thresholds (may be too strict)
```

**Reddit API errors:**
```bash
# Verify credentials in .env file
cat .env

# Test Reddit connection
python -c "import praw; print('PRAW installed successfully')"
```

**Storage issues:**
```bash
# Check permissions
ls -la knowledge-vault/databases/knowledge_vault/content-intelligence/

# Create directories manually if needed
mkdir -p knowledge-vault/databases/knowledge_vault/content-intelligence/reddit-intelligence/dynamic-discovery/
```

## Development

### Adding New Subreddits
Edit `reddit-dynamic-discovery-config.json`:
```json
{
  "priority_subreddits": [
    "existing_subreddit",
    "new_subreddit"
  ]
}
```

### Custom Search Queries
Add to search_queries array:
```json
{
  "terms": ["your", "search", "terms"],
  "priority_topics": ["your-topic"],
  "subreddits": ["target", "subreddits"],
  "min_score": 50
}
```

### Quality Threshold Tuning
Adjust in configuration:
```json
{
  "quality_thresholds": {
    "min_upvotes": 25,          // Lower for more posts
    "min_comments": 3,          // Lower for broader coverage
    "max_age_days": 14          // Higher for older content
  }
}
```

## Future Enhancements

### Planned Features
- **Sentiment analysis** of post content
- **Author credibility scoring** based on karma and history
- **Thread analysis** for comment quality assessment  
- **Trend detection** across time periods
- **Automated summarization** of key discussions

### Integration Opportunities
- **Knowledge vault updates** with discovered insights
- **Alert system** for breaking discussions
- **Cross-platform correlation** with HackerNews, YouTube
- **ML-based topic classification** improvements

## Support

For issues, questions, or contributions:
1. Check the troubleshooting section above
2. Review logs in `reddit-dynamic-discovery.log`
3. Test configuration with `python test_reddit_discovery.py`
4. Ensure all dependencies are installed via `pip install -r requirements.txt`

The system is designed to be self-sufficient and robust, with comprehensive error handling and logging for debugging any issues that arise.