# Universal Topic Intelligence System

A working RSS feed monitoring system that collects content from verified sources and provides a web dashboard for browsing.

## 🌟 What Actually Works

### RSS Feed Monitoring
- **8 Verified Sources**: React, Dan Abramov, Kent C. Dodds, LangChain, HackerNews, Reddit ClaudeAI, CoinTelegraph, Decrypt
- **Content Storage**: SQLite database with 380+ items collected
- **Priority Scoring**: Basic content prioritization system
- **Language Filter**: English content detection

### Web Dashboard
- **Real-time Stats**: Total items, sources, priority breakdown
- **Content Browsing**: Filter by priority, search, bookmark items
- **FastAPI Backend**: Clean API with proper error handling
- **Responsive UI**: Modern web interface

## 🚀 Quick Start

### Prerequisites
```bash
# Install dependencies
pip install feedparser aiohttp fastapi uvicorn pyyaml sqlite3
```

### Run the System
```bash
# Single monitoring run
python monitor.py --mode single

# Start continuous monitoring (every 60 minutes)  
python monitor.py --mode scheduled --interval 60

# Check status
python monitor.py --mode status
```

### Start Web Dashboard
```bash
python dashboard.py
# Open: http://localhost:8080
```

## 📊 What You'll See

### Monitor Output
```
📊 Monitoring Results:
  Sources Checked: 8
  Success Rate: 87.5%
  Items Found: 23
  Items Stored: 18

📋 Source Results:
  ✅ React Blog: 3 found, 2 stored
  ✅ Dan Abramov Blog: 1 found, 1 stored  
  ✅ HackerNews: 15 found, 12 stored
  ❌ Some Feed: Failed (403 Forbidden)
```

### Dashboard Features
- **Statistics Bar**: Total items, sources, critical/high priority counts
- **Content Feed**: Browseable list with titles, dates, priority scores
- **Filtering**: All/Critical/High/Medium priority buttons
- **Search**: Text search across titles and content
- **Bookmarking**: Save items for later review

## 🏗️ System Architecture  

### Core Files (What's Actually Used)
- **`monitor.py`**: Main monitoring script with CLI interface
- **`dashboard.py`**: FastAPI web dashboard
- **`sources/rss_monitor.py`**: RSS feed processing
- **`core/content_prioritizer.py`**: Content scoring logic
- **`storage/database.py`**: SQLite database operations
- **`topic_intelligence.db`**: Main content database

### Working Data Flow
1. **RSS Monitor** fetches feeds from 8 verified sources
2. **Content Prioritizer** scores items (0.0-1.0) based on keywords/topics
3. **Storage Manager** saves to SQLite with deduplication
4. **Web Dashboard** serves content via FastAPI

## 📈 Current Performance

- **8 Working Sources** (tested and verified)
- **380+ Items Stored** in database
- **87.5% Success Rate** (7/8 sources typically working)
- **~20 New Items/Day** average collection rate

## 🔧 Configuration

### Adding New RSS Sources
Edit `monitor.py` working_sources list:
```python
{
    "url": "https://example.com/rss.xml",
    "name": "Example Site", 
    "topics": ["topic1", "topic2"],
    "authority_score": 0.8
}
```

### Priority Scoring Rules
Edit `core/content_prioritizer.py` keyword weights:
```python
self.keyword_scores = {
    "react": 0.8,
    "claude": 0.9, 
    "ai": 0.7,
    # Add your keywords
}
```

## 🧪 Testing

```bash
# Check system status
python monitor.py --mode status

# Run single cycle with verbose logging
python monitor.py --mode single --verbose

# Check database contents
sqlite3 topic_intelligence.db "SELECT COUNT(*) FROM content_items;"
```

## ⚠️ Known Limitations

- **RSS Only**: No YouTube, GitHub, or MCP integration (all placeholders removed)
- **Basic Scoring**: Simple keyword-based priority calculation
- **No Agent Hierarchy**: Elaborate AI agent system was theoretical/unused
- **Limited Sources**: Only 8 working feeds (many others return 403/404)
- **No Real-time**: Polling-based, not push notifications

## 📚 Documentation Structure

- **`CLAUDE.md`**: AI agent instructions (aspirational)
- **`universal-topic-system/`**: Elaborate YAML configs (mostly unused)
- **`examples/`**: Topic monitoring examples (templates)
- **`docs/`**: Research and analysis documents

## 🎯 This Is Actually

- **20% working RSS aggregator** with web dashboard
- **80% elaborate planning documents** and unused configurations
- Good foundation for building a real topic intelligence system
- Honest implementation after removing fake/placeholder code

---

**A working RSS monitoring foundation - no revolutionary AI claims, just functional code that actually collects and displays content.**