# 🎯 Unified Intelligence System - Usage Guide

## Quick Start Commands

### 📰 Daily Intelligence Digest
```bash
# Generate today's personalized digest with priority topics
@daily-intelligence-digest "Generate today's digest with priority topics focus"

# Or use the Python script directly
cd meta/unified-intelligence/daily-digest
python3 intelligence-digest-generator.py
```

### 🔍 Generate Digest for Different Time Ranges
```bash
@daily-intelligence-digest "Generate digest for yesterday"
@daily-intelligence-digest "Generate digest for last 3 days" 
@daily-intelligence-digest "Generate digest for last week"
```

## 📊 Priority Topics System

The system now prioritizes content about your key interests:

### 🎯 **Priority Topics** (Auto-detected & Boosted):
- **claude** (weight: 1.0) - Claude AI, Anthropic developments
- **claude-code** (weight: 1.0) - Claude Code IDE, development tools  
- **react** (weight: 0.9) - React.js framework and ecosystem
- **typescript** (weight: 0.8) - TypeScript language and tooling
- **meta-prompting** (weight: 0.9) - Prompt engineering techniques

### 🚀 **Topic Combinations** (Extra Boost):
- **React + TypeScript**: 1.3x multiplier
- **Claude + React**: 1.2x multiplier  
- **Meta-prompting + Claude**: 1.7x multiplier

## 🤖 Available Agents

### Core Intelligence Agents
```bash
# Generate daily digest with priority topic scoring
@daily-intelligence-digest

# Comprehensive system analysis and optimization
@system-architect

# Performance monitoring and optimization
@performance-monitoring-agent
```

### Content & Research Agents
```bash
# Advanced research coordination with ensemble methods
@research-specialist

# Multi-perspective research exploration
@multi-path-research-explorer

# Quality assurance and cross-validation
@cross-validation-orchestrator
```

## 📁 System Architecture

### Key Directories
```
meta/unified-intelligence/
├── daily-digest/                    # Daily digest generation
│   ├── intelligence-digest-generator.py  # Main digest generator
│   └── generated/                   # Output location
├── priority-topics.json            # Priority topics configuration
├── topic-scoring-engine.py         # Advanced scoring algorithm
├── platforms/                      # Platform-specific configs
│   ├── reddit/reddit-subreddits-config.json
│   ├── hackernews/hackernews-feeds-config.json
│   └── youtube/ (coming soon)
└── knowledge-vault/databases/knowledge_vault/content-intelligence/
    └── youtube-intelligence/       # Processed content
```

## 🎛️ Priority Topics Configuration

The system uses `priority-topics.json` to define:

```json
{
  "priority_topics": {
    "claude": {
      "weight": 1.0,
      "aliases": ["Claude AI", "Anthropic Claude", "Claude Code"],
      "keywords": ["claude", "anthropic", "constitutional ai"]
    }
  },
  "content_scoring": {
    "freshness_decay": {
      "0-24_hours": 1.0,
      "1-3_days": 0.8,
      "3-7_days": 0.6
    }
  }
}
```

## 🔧 Advanced Usage

### Manual Content Processing
```bash
# Process YouTube backlog
cd meta/unified-intelligence
python3 test-unified-processing.py

# Run discovery algorithms
cd discovery-algorithms
python3 github-discovery.py
```

### System Health Monitoring
```bash
# Check system status
cd automation
python3 system-health-monitor.py

# View automation logs
tail -f daily-automation.log
```

### Customize Priority Topics
Edit `meta/unified-intelligence/priority-topics.json` to:
- Add new priority topics
- Adjust topic weights
- Define new topic combinations
- Configure freshness decay rates

## 📈 Understanding Scores

### Content Scoring Formula
```
Final Score = Base Score × Freshness Score × Relevance Score × Priority Boost

Where:
- Base Score: Engagement metrics (views, comments, upvotes)
- Freshness Score: Content age penalty (1.0 for <24h, decreases over time)  
- Relevance Score: Match to your interests
- Priority Boost: Multiplier for priority topics (0.8x - 1.7x)
```

### Score Interpretation
- **0.8+ (High Priority)**: Must-read content, perfectly aligned
- **0.5-0.8 (Medium)**: Quality content worth reviewing
- **0.2-0.5 (Low)**: Marginally relevant or older content
- **<0.2 (Filter)**: Off-topic or very low engagement

## 🎯 Digest Output Format

### Priority Topics Section
The digest now includes dedicated sections:
```json
{
  "sections": {
    "priority_topics": {
      "claude": {
        "count": 3,
        "avg_priority_score": 0.285,
        "top_items": [/* Claude-related content */]
      }
    }
  }
}
```

## 🚀 Next Phase Features (Coming Soon)

### Phase 2 - Dynamic Discovery
- **YouTube Search**: Automated searches for "Claude released", "React TypeScript", etc.
- **Reddit Cross-Search**: Finding priority topics across all programming subreddits
- **Trend Detection**: Identifying breaking news in your priority areas

### Phase 3 - Intelligence Enhancement  
- **Semantic Analysis**: Understanding content context beyond keywords
- **Learning Adaptation**: System learns from your reading patterns
- **Predictive Recommendations**: Suggesting content before you need it

## 🛠️ Troubleshooting

### Common Issues

**Topic Scoring Engine Not Loading**:
```bash
cd meta/unified-intelligence/daily-digest
# Check if import works
python3 -c "import sys; sys.path.append('..'); exec(open('../topic-scoring-engine.py').read())"
```

**No Priority Topics Detected**:
- Check `priority-topics.json` configuration
- Verify content contains priority keywords
- Review topic detection logs in digest output

**Low Content Scores**:
- Content may be older (freshness decay applied)
- Content may not match priority topics  
- Check engagement metrics (views, comments)

### Debug Commands
```bash
# Test topic scoring directly
cd meta/unified-intelligence
python3 topic-scoring-engine.py

# Check digest generation with verbose output
cd daily-digest  
python3 intelligence-digest-generator.py 2>&1 | tee debug.log
```

## 🎯 Success Metrics

The system tracks:
- **Priority Topic Coverage**: How many of your interests appear daily
- **Score Accuracy**: Whether high-scored content is actually valuable  
- **Discovery Success**: Finding new relevant sources automatically
- **Personalization Effectiveness**: Improved recommendations over time

## 💡 Usage Tips

1. **Daily Routine**: Run digest generation each morning for fresh insights
2. **Topic Monitoring**: Check priority_topics sections for your key interests
3. **Score Thresholds**: Focus on content with scores >0.5 for best value
4. **Feedback Loop**: The more you use it, the better it learns your preferences
5. **Custom Configuration**: Adjust priority topics based on current projects

---

**Ready to use the system!** Start with `@daily-intelligence-digest` to get your personalized, priority-focused daily digest.