# 🌐 Universal Topic Intelligence System - Complete Guide

## System Overview

The Universal Topic Intelligence System is a sophisticated AI-powered information monitoring platform that intelligently tracks any topic domain using a 4-level agent hierarchy and multiple data sources.

## ✅ Current Features

### 1. **Automated RSS Monitoring**
- Monitors 12+ Claude-focused RSS feeds
- Automatic language filtering (English only)
- Configurable refresh intervals (default: 30 minutes)
- Status: **FULLY OPERATIONAL**

### 2. **Priority Scoring System**
- Uses existing ContentPrioritizer with topic-specific rules
- Claude content receives special boosting (2x-2.2x multiplier)
- 4 priority levels: Critical, High, Medium, Low
- Status: **FULLY OPERATIONAL**

### 3. **Web Dashboard**
- Modern, intuitive interface at http://localhost:5001
- Real-time search across all content
- Bookmarking and read tracking
- Reading time estimates
- Status: **FULLY OPERATIONAL**

### 4. **Continuous Monitoring Service**
- Background service with configurable intervals
- Automatic error recovery
- Statistics tracking
- Status: **FULLY OPERATIONAL**

### 5. **MCP Server Integration Framework**
- Prepared for GitHub, YouTube, Wikipedia, Web Search integration
- Extensible architecture for new MCP servers
- Status: **FRAMEWORK READY** (awaiting MCP server connections)

## 🚀 Quick Start Guide

### Start the System

```bash
# Start continuous monitoring and dashboard
./start_monitoring.sh

# Or start with custom interval (minutes)
./start_monitoring.sh 60
```

### Access the Dashboard

Open your browser to: **http://localhost:5001**

### Stop the System

```bash
./stop_monitoring.sh
```

### Check System Status

```bash
python system_status.py
```

### Manual Operations

```bash
# Run single monitoring cycle
python auto_monitor.py --once

# Re-score all content
python rescore_content.py

# Start dashboard only
python dashboard_proper.py
```

## 📊 System Architecture

```
Universal Topic Intelligence System
├── Core Components
│   ├── ContentPrioritizer (priority scoring)
│   ├── TopicQualityScorer (quality assessment)
│   ├── LanguageFilter (English-only filtering)
│   └── StorageManager (SQLite persistence)
│
├── Data Sources
│   ├── RSS Feeds (12 active sources)
│   │   ├── Dev.to (Claude, React, TypeScript, AI tags)
│   │   ├── HackerNews (AI and React searches)
│   │   ├── Simon Willison's Blog
│   │   └── OpenAI Blog
│   │
│   └── MCP Integrations (Framework Ready)
│       ├── GitHub (repositories)
│       ├── YouTube (video content)
│       ├── Wikipedia (knowledge articles)
│       └── Web Search (news and updates)
│
├── User Interface
│   ├── Web Dashboard (FastAPI + Modern UI)
│   ├── Search Functionality
│   ├── Bookmarking System
│   └── Read Tracking
│
└── Automation
    ├── Auto Monitor (scheduled refresh)
    ├── Service Scripts (start/stop)
    └── Status Monitoring
```

## 📈 Current Statistics

Based on the latest system run:

- **Total Items Collected**: 171
- **Claude-Specific Content**: 20 items
- **Priority Distribution**:
  - Critical: 77 items (45%)
  - High: 15 items (9%)
  - Medium: 45 items (26%)
  - Low/Archive: 34 items (20%)

## 🔧 Configuration

### RSS Sources Configuration

Edit `sources/claude_focused_monitor.py` to add/modify RSS feeds:

```python
CLAUDE_FOCUSED_SOURCES = [
    {
        "source_id": "your_source",
        "source_name": "Your Source Name",
        "source_url": "https://example.com/rss",
        "authority_score": 0.8,
        "topics": ["claude", "ai"]
    }
]
```

### Priority Scoring Configuration

Edit `rescore_content.py` to adjust scoring weights:

```python
prioritizer_config = {
    "weights": {
        "source_authority": 0.25,
        "content_recency": 0.20,
        "topic_relevance": 0.25,
        # ... adjust as needed
    }
}
```

## 🎯 Claude Content Special Rules

The system applies special boosting for Claude-related content:

1. **Claude Opus** mentions: 2.2x multiplier
2. **Claude releases/announcements**: 2.0x multiplier  
3. **Anthropic content**: 1.5x multiplier
4. **General Claude mentions**: 1.5x multiplier

This ensures Claude content is never below HIGH priority.

## 🛠️ Troubleshooting

### Dashboard Won't Start
```bash
# Kill existing process on port 5001
lsof -ti:5001 | xargs kill -9

# Restart dashboard
python dashboard_proper.py
```

### Monitoring Not Collecting Items
```bash
# Check RSS feed status
python auto_monitor.py --once

# Review logs
tail -f monitoring.log
```

### Database Issues
```bash
# Check database integrity
sqlite3 topic_intelligence.db "SELECT COUNT(*) FROM content_items;"

# Reset and re-score content
python rescore_content.py
```

## 📅 Future Enhancements

### In Development
- [ ] Email digest feature
- [ ] AI summary generation for content
- [ ] Trending topic detection
- [ ] Full MCP server integration

### Planned Features
- [ ] Multi-topic monitoring
- [ ] Custom alert rules
- [ ] Content categorization
- [ ] Export functionality
- [ ] Mobile-responsive dashboard

## 🔒 Security & Privacy

- All data stored locally in SQLite databases
- No external API keys required for current functionality
- English-only filtering for content control
- No telemetry or tracking

## 📝 Files Overview

| File | Purpose |
|------|---------|
| `auto_monitor.py` | Automated monitoring scheduler |
| `dashboard_proper.py` | Web dashboard server |
| `rescore_content.py` | Content re-scoring utility |
| `system_status.py` | System health checker |
| `start_monitoring.sh` | Service starter script |
| `stop_monitoring.sh` | Service stopper script |
| `topic_intelligence.db` | Main content database |
| `user_data.db` | User preferences database |

## 💡 Tips for Best Results

1. **Run monitoring regularly**: Keep the service running for continuous updates
2. **Review Critical items daily**: Check the dashboard for high-priority content
3. **Use search effectively**: Search works across titles and content
4. **Bookmark important items**: Use bookmarking for later review
5. **Monitor system status**: Run `system_status.py` periodically

## 🤝 Contributing

To add new features or sources:

1. Add RSS feeds to `sources/claude_focused_monitor.py`
2. Implement new MCP integrations in `sources/mcp_integrations.py`
3. Extend dashboard features in `dashboard_proper.py`
4. Add new scoring rules in `rescore_content.py`

## 📞 Support

For issues or questions:
- Check the troubleshooting section above
- Review logs in `monitoring.log` and `dashboard.log`
- Run `system_status.py` for diagnostics

---

**System Status**: ✅ OPERATIONAL
**Version**: 1.0.0
**Last Updated**: December 2024