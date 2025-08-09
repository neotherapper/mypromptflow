# Daily Content Digest Command

Generate pure content-focused daily intelligence digest with priority topics scoring - beautiful HTML dashboard format.

The unified intelligence system monitors 50+ sources across YouTube, Reddit, HackerNews, and GitHub, applying sophisticated priority topic scoring to surface content about claude, claude-code, react, typescript, and meta-prompting. **Content ONLY** - no system information mixing.

## Usage Examples

```bash
# Generate today's content digest with priority topics
/daily-digest

# Generate digest for specific time range  
/daily-digest yesterday
/daily-digest last_3_days
/daily-digest week

# Force regenerate existing digest
/daily-digest today force

# Show priority topics configuration
/daily-digest config
```

## What This Command Does

1. **Pure Content Focus**: Generates ONLY content digests - NO system health or monitoring information
2. **Priority Topic Intelligence**: Advanced scoring for claude, claude-code, react, typescript, meta-prompting
3. **Beautiful HTML Dashboard**: Professional dashboard-style output with responsive design
4. **Topic Combination Bonuses**: React+TypeScript (1.3x boost), Claude+Meta-prompting (1.7x boost)
5. **Duplicate Prevention**: Automatically detects existing digests to prevent regeneration

## Priority Topics Intelligence

The system automatically detects and prioritizes:
- **Claude AI & Anthropic**: Latest developments, features, research, updates
- **Claude Code**: IDE features, development tools, coding assistance, integrations
- **React.js**: Framework updates, best practices, ecosystem tools, component patterns
- **TypeScript**: Language features, tooling, type safety patterns, compiler updates
- **Meta-prompting**: Prompt engineering, AI interaction techniques, optimization strategies

## Beautiful HTML Output

### Professional Dashboard Features
- **Purple Gradient Header**: Elegant content-focused design
- **Statistics Cards**: Total items, high quality count, average score, priority items
- **Priority Topics Section**: Cards for each detected topic with item counts and top content
- **Platform Breakdown**: Organized by source (YouTube, Reddit, etc.) with platform icons
- **Responsive Design**: Works perfectly on desktop and mobile devices
- **Interactive Elements**: Hover effects, clickable links, professional styling

## Output Locations

- **Latest HTML**: `meta/unified-intelligence/daily-digest/generated/content/daily-digest.html`
- **Latest JSON**: `meta/unified-intelligence/daily-digest/generated/content/daily-digest.json`
- **Historical Archive**: `meta/unified-intelligence/daily-digest/generated/content/history/{date}-content-digest.html`

## Priority Topic Scoring System

### Multi-Factor Algorithm
- **Base Score**: Content unified score from processing
- **Freshness Factor**: Recent content (0-24h) gets 1.0x, 1-3 days gets 0.8x, 3-7 days gets 0.6x
- **Relevance Score**: Topic detection accuracy and context matching
- **Priority Boost**: Topic-specific weight multipliers (claude: 1.0, react: 0.9, typescript: 0.8)

### Intelligence Features
- **Topic Detection**: Automatic identification of priority topics in content
- **Context Analysis**: Understands topic relevance within content context
- **Quality Filtering**: High-quality items (>0.8 score) get priority placement
- **Age-Based Decay**: Ensures recent content gets appropriate priority

## Separated Architecture

### Content-Only Benefits
- **No System Mixing**: Pure content digests without operational information
- **Clean Organization**: Structured file system with content/ and history/ folders  
- **Professional Presentation**: Content-focused dashboard design
- **Fast Generation**: Optimized for content processing only

### For System Monitoring
Use the separate `/system-status` command for:
- System health monitoring
- Component performance metrics
- Operational status reports
- Infrastructure monitoring

---

**Pro Tip**: This command generates beautiful HTML dashboards perfect for daily content consumption. For system monitoring, use `/system-status` instead.