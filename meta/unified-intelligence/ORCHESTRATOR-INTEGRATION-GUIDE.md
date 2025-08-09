# Automated Discovery Orchestrator Integration Guide

## Overview

The Automated Discovery Orchestrator is a comprehensive system that coordinates all intelligence discovery operations across multiple platforms, providing intelligent scheduling, resource management, error handling, and performance monitoring.

## System Architecture

### Core Components

1. **Main Orchestrator** (`automated-discovery-orchestrator.py`)
   - Central coordination engine
   - Task scheduling and execution
   - Resource management
   - Error handling and retry logic

2. **Setup Manager** (`setup-orchestrator.py`)
   - Installation and configuration
   - Dependency management
   - Service deployment

3. **Dashboard** (`orchestrator-dashboard.py`)
   - Web-based monitoring interface
   - Real-time status updates
   - Manual control capabilities

4. **Configuration** (`orchestrator-config.json`)
   - Scheduling intervals
   - Resource limits
   - Quality thresholds
   - Integration settings

## Integrated Discovery Systems

### 1. YouTube Dynamic Search
- **File**: `youtube-dynamic-search.py`
- **Schedule**: Daily at 6 AM UTC
- **Function**: Discovers priority topic content through search
- **Integration**: Feeds content to MCP processor

### 2. Reddit Dynamic Discovery
- **File**: `reddit-dynamic-discovery.py`
- **Schedule**: Weekly on Sundays at 8 AM UTC
- **Function**: Cross-subreddit search for high-quality discussions
- **Integration**: Provides social intelligence data

### 3. MCP YouTube Processor
- **File**: `mcp-youtube-processor.py`
- **Schedule**: Daily after YouTube search
- **Function**: Deep transcript analysis using MCP tools
- **Dependencies**: YouTube search results

### 4. Content Digest Generation
- **File**: `daily-digest/intelligence-digest-generator.py`
- **Schedule**: Daily after all discovery tasks
- **Function**: Synthesizes all discovered content into daily reports
- **Dependencies**: All discovery systems

### 5. System Health Monitoring
- **File**: `automation/system-health-monitor.py`
- **Schedule**: Hourly
- **Function**: System performance and health checks
- **Integration**: Feeds into orchestrator metrics

## Installation and Setup

### Quick Setup

```bash
# Navigate to orchestrator directory
cd /Users/georgiospilitsoglou/Developer/projects/mypromptflow/meta/unified-intelligence

# Run full setup
python setup-orchestrator.py setup

# Start orchestrator
./start-orchestrator.sh
```

### Manual Setup

1. **Install Dependencies**
```bash
pip install -r orchestrator-requirements.txt
```

2. **Configure API Keys**
```bash
# Edit configuration files for your API keys
vim orchestrator-config.json
vim reddit-dynamic-discovery-config.json
vim youtube-search-config.json
```

3. **Test Installation**
```bash
python setup-orchestrator.py test
```

4. **Choose Deployment Method**

**Option A: Systemd Service (Linux)**
```bash
sudo cp orchestrator.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable orchestrator.service
sudo systemctl start orchestrator.service
```

**Option B: Cron Jobs**
```bash
crontab orchestrator-cron
```

**Option C: Manual Execution**
```bash
python automated-discovery-orchestrator.py --mode continuous
```

## Configuration Reference

### Core Settings

```json
{
  "max_concurrent_tasks": 3,
  "resource_limits": {
    "max_cpu_percent": 80,
    "max_memory_mb": 2048,
    "max_disk_percent": 90
  },
  "scheduling_intervals": {
    "youtube_search": "daily",
    "reddit_discovery": "weekly", 
    "mcp_youtube_processing": "daily",
    "content_digest": "daily",
    "system_health": "hourly"
  }
}
```

### Quality Thresholds

```json
{
  "quality_thresholds": {
    "min_content_score": 0.7,
    "max_duplicate_percentage": 0.1,
    "min_source_credibility": 0.8,
    "min_engagement_threshold": 100
  }
}
```

### Integration Settings

```json
{
  "integration_settings": {
    "youtube_api": {
      "rate_limit_per_day": 10000,
      "max_results_per_search": 50
    },
    "reddit_api": {
      "rate_limit_per_minute": 60,
      "max_results_per_search": 100
    },
    "mcp_servers": {
      "youtube": {
        "enabled": true,
        "timeout_seconds": 300
      }
    }
  }
}
```

## Usage Patterns

### Daily Operations

The orchestrator automatically handles:
- 6:00 AM UTC: YouTube content discovery
- 6:30 AM UTC: MCP transcript processing
- 7:00 AM UTC: Daily digest generation
- Every hour: System health checks
- Sunday 8:00 AM UTC: Weekly Reddit discovery

### Manual Operations

```bash
# Check status
python automated-discovery-orchestrator.py --mode status

# Run single cycle
python automated-discovery-orchestrator.py --mode single

# Force run specific task
python automated-discovery-orchestrator.py --mode single --task youtube_search

# Enable/disable tasks
python automated-discovery-orchestrator.py --enable reddit_discovery
python automated-discovery-orchestrator.py --disable mcp_youtube_processing
```

### Dashboard Access

```bash
# Start web dashboard
python orchestrator-dashboard.py --host 0.0.0.0 --port 5000

# Access dashboard
open http://localhost:5000
```

## Monitoring and Alerts

### System Metrics

The orchestrator tracks:
- CPU and memory usage
- Task execution times
- Success/failure rates
- Resource utilization
- Content discovery statistics

### Alert Conditions

Automatic alerts for:
- Error rate > 20%
- CPU usage > 90%
- Memory usage > 90%
- 3+ consecutive task failures
- Resource exhaustion

### Log Files

- `orchestrator.log` - Main system log
- `orchestrator-state.json` - Current system state
- `system-report-*.json` - Historical metrics
- `orchestrator-cron.log` - Cron execution log

## Intelligence Flow

### Data Flow Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│ YouTube Search  │───▶│ MCP Processor    │───▶│ Content Digest  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         ▲
┌─────────────────┐    ┌──────────────────┐             │
│ Reddit Discovery│───▶│ Topic Scoring    │─────────────┘
└─────────────────┘    └──────────────────┘
                                                         ▲
┌─────────────────┐    ┌──────────────────┐             │
│ Health Monitor  │───▶│ System Metrics   │─────────────┘
└─────────────────┘    └──────────────────┘
```

### Content Processing Pipeline

1. **Discovery Phase**
   - YouTube search for priority topics
   - Reddit cross-subreddit monitoring
   - Content quality filtering

2. **Analysis Phase**
   - MCP transcript extraction
   - Topic scoring and relevance
   - Duplicate detection

3. **Synthesis Phase**
   - Content aggregation
   - Intelligence digest generation
   - Performance reporting

## Advanced Features

### Adaptive Scheduling

The orchestrator learns from content patterns and adjusts scheduling:
- Increases frequency during high-content periods
- Reduces execution during low-activity times
- Balances resource usage with discovery needs

### Intelligent Prioritization

Dynamic priority adjustment based on:
- Topic scoring results
- Content freshness
- Source credibility
- Historical engagement

### Predictive Resource Management

- Forecasts resource needs based on task patterns
- Preemptively schedules tasks during low-usage periods
- Prevents resource conflicts

## Troubleshooting

### Common Issues

1. **Tasks Not Running**
```bash
# Check system status
python automated-discovery-orchestrator.py --mode status

# Verify configuration
python setup-orchestrator.py validate

# Check logs
tail -f orchestrator.log
```

2. **High Resource Usage**
```bash
# Reduce concurrent tasks
vim orchestrator-config.json
# Set "max_concurrent_tasks": 2

# Check resource limits
python -c "import psutil; print(f'CPU: {psutil.cpu_percent()}%, Memory: {psutil.virtual_memory().percent}%')"
```

3. **API Rate Limits**
```bash
# Check API configurations
vim reddit-dynamic-discovery-config.json
vim youtube-search-config.json

# Review rate limit settings in orchestrator-config.json
```

4. **MCP Integration Issues**
```bash
# Test MCP server connectivity
python mcp-youtube-processor.py --test

# Check MCP server status
python automated-discovery-orchestrator.py --mode status | grep mcp
```

### Performance Optimization

1. **Reduce Discovery Frequency**
   - Adjust scheduling intervals in config
   - Use bi-weekly for less critical tasks

2. **Optimize Resource Usage**
   - Lower max_concurrent_tasks
   - Increase task timeout limits
   - Enable compression for old data

3. **Improve Content Quality**
   - Raise quality thresholds
   - Enable duplicate detection
   - Configure source credibility checks

## Integration with Existing Systems

### Knowledge Vault Integration

The orchestrator automatically:
- Stores discovered content in knowledge vault structure
- Updates content intelligence databases
- Maintains content history and metadata

### MCP Server Coordination

Seamless integration with:
- YouTube transcript extraction
- Content analysis tools
- External API services

### Development Workflow Integration

- Feeds into daily digest system
- Provides intelligence for development decisions
- Supports research and learning workflows

## Maintenance

### Regular Tasks

1. **Weekly Review**
   - Check system performance metrics
   - Review discovery quality
   - Update configuration as needed

2. **Monthly Cleanup**
   - Archive old logs and reports
   - Update API credentials
   - Review and optimize scheduling

3. **Quarterly Updates**
   - Update dependencies
   - Review and enhance discovery algorithms
   - Optimize resource utilization

### Backup and Recovery

The orchestrator includes automatic:
- Configuration backup
- State preservation
- Metric history retention
- Error recovery mechanisms

## Support and Maintenance

For issues or enhancements:
1. Check logs for error details
2. Verify configuration settings
3. Test individual discovery systems
4. Use the dashboard for real-time monitoring
5. Review system metrics for performance insights

This orchestrator provides a robust, scalable foundation for continuous intelligence discovery across all platforms, ensuring high-quality content is automatically discovered, processed, and made available for daily intelligence needs.