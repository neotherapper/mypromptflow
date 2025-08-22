# MCP Discovery Commands

Execute intelligent MCP server discovery with natural language queries and guided recommendations.

## Command: /mcp-discover

**Purpose**: Find MCP servers based on natural language needs description

**Syntax**: `/mcp-discover [need description]`

**Examples**:
- `/mcp-discover I need to add search to my React app`
- `/mcp-discover monitor production errors`
- `/mcp-discover build AI chatbot`
- `/mcp-discover cache API responses`

**Process**:
1. Parse natural language query using `@knowledge-vault/discovery/query-processor.yaml`
2. Extract intent, technologies, and requirements
3. Search MCP Discovery Index for matches
4. Return ranked results with confidence scores

**Output Format**:
```yaml
Query Understanding:
  Intent: "search functionality"
  Technologies: ["React"]
  Confidence: 85%

Top Recommendations:
1. Algolia Search (Score: 9.2)
   - Setup: 30 minutes
   - Why: React SDK, instant search
   
2. MeiliSearch (Score: 8.5)
   - Setup: 25 minutes
   - Why: Simple, typo-tolerant

Alternative Approaches:
- Elasticsearch (more powerful, complex)
- PostgreSQL Full-Text (if already using)
```

## Command: /mcp-wizard

**Purpose**: Interactive guided questionnaire for MCP server selection

**Syntax**: `/mcp-wizard`

**Process**:
1. Load `@knowledge-vault/discovery/wizards/mcp-selection-wizard.yaml`
2. Ask progressive questions based on answers
3. Build recommendation profile
4. Generate personalized stack

**Interaction Flow**:
```
Q1: What's your primary goal?
> Build a new application

Q2: What type of application?
> Web application

Q3: Primary technology stack?
> React, Python, PostgreSQL

[Generates recommendations...]
```

## Command: /mcp-compare

**Purpose**: Side-by-side comparison of MCP servers

**Syntax**: `/mcp-compare [server1] [server2] [server3?]`

**Examples**:
- `/mcp-compare elasticsearch algolia`
- `/mcp-compare sentry "new relic" datadog`
- `/mcp-compare postgresql mongodb redis`

**Output Format**:
```markdown
| Feature | Elasticsearch | Algolia |
|---------|--------------|---------|
| Setup Time | 2-4 hours | 30 min |
| Complexity | High | Low |
| Cost | Self-hosted/Cloud | SaaS |
| Search Quality | Excellent | Excellent |
| React Support | Client library | Native SDK |
| Score | 7.2 | 8.3 |

Recommendation: Algolia for quick start, Elasticsearch for control
```

## Command: /mcp-stack

**Purpose**: Find servers compatible with your technology stack

**Syntax**: `/mcp-stack [technologies]`

**Examples**:
- `/mcp-stack react typescript postgresql`
- `/mcp-stack python fastapi aws`
- `/mcp-stack nodejs mongodb kubernetes`

**Process**:
1. Load `@knowledge-vault/discovery/views/by-technology-stack.yaml`
2. Calculate alignment scores
3. Filter by technology compatibility
4. Return stack-optimized recommendations

**Output**:
```yaml
Your Stack: React, TypeScript, PostgreSQL

Perfect Alignment (10/10):
- Next.js Framework
- Prisma ORM
- TypeScript

High Alignment (8-9/10):
- Tailwind CSS
- Jest Testing
- Sentry Error Tracking

Good Alignment (6-7/10):
- Redis Cache
- Elasticsearch
```

## Command: /mcp-similar

**Purpose**: Find similar or complementary servers

**Syntax**: `/mcp-similar [server name]`

**Examples**:
- `/mcp-similar postgresql`
- `/mcp-similar sentry`
- `/mcp-similar nextjs`

**Process**:
1. Load `@knowledge-vault/discovery/similarity/similarity-engine.yaml`
2. Find server relationships
3. Calculate similarity scores
4. Return complementary and alternative options

**Output**:
```yaml
Server: PostgreSQL

Works Great With:
- Prisma ORM (95% compatibility)
- Redis Cache (85% synergy)
- SQLAlchemy (90% fit)

Alternatives:
- MySQL (85% similar)
- MongoDB (60% different approach)

Natural Progression:
- Add ORM → Add Caching → Add Search
```

## Command: /mcp-quick

**Purpose**: Get instant recommendations for common scenarios

**Syntax**: `/mcp-quick [scenario]`

**Shortcuts**:
- `/mcp-quick monitoring` → Sentry + Prometheus + Grafana
- `/mcp-quick ai` → Claude API + Redis + PostgreSQL
- `/mcp-quick react` → Next.js + Tailwind + TypeScript
- `/mcp-quick search` → MeiliSearch or Algolia
- `/mcp-quick api` → FastAPI + PostgreSQL + Redis

**Output**:
```yaml
Quick Start: Monitoring Stack

Immediate (15 min):
- Sentry Error Tracking

Next Step (1 hour):
- Prometheus + Grafana

Complete Stack (2 hours):
- Add New Relic APM
- Add LogRocket
```

## Command: /mcp-use-case

**Purpose**: Browse servers by use case

**Syntax**: `/mcp-use-case [use case?]`

**Examples**:
- `/mcp-use-case` (shows all use cases)
- `/mcp-use-case "building web apps"`
- `/mcp-use-case monitoring`

**Process**:
1. Load `@knowledge-vault/discovery/views/by-use-case.yaml`
2. Filter or list use cases
3. Show recommended stacks for each

## Command: /mcp-wins

**Purpose**: Show quick win servers with immediate value

**Syntax**: `/mcp-wins [time budget?]`

**Examples**:
- `/mcp-wins` (all quick wins)
- `/mcp-wins 30min` (setup under 30 minutes)
- `/mcp-wins instant` (< 5 minute setup)

**Process**:
1. Load `@knowledge-vault/discovery/views/quick-wins.yaml`
2. Filter by setup time
3. Sort by ROI score

**Output**:
```yaml
Quick Wins Under 30 Minutes:

1. Filesystem MCP (2 min setup)
   Value: Complete file access
   
2. Sentry (15 min setup)
   Value: Automatic error tracking
   
3. Redis Docker (20 min setup)
   Value: Instant caching
```

## Command: /mcp-expand

**Purpose**: Systematically expand MCP knowledge vault

**Syntax**: `/mcp-expand [source?]`

**Process**:
1. Check `@meta/mcp-system/intelligence/source-tracking.yaml`
2. Identify gaps in coverage
3. Process high-priority sources
4. Create new server profiles

**Output**:
```yaml
Current Coverage: 29.2% (175/600 servers)

Priority Gaps:
- awesome-mcp-servers: 75 servers pending
- docker_hub_mcp: 62 servers pending

Next Batch (10 servers):
[List of servers to profile...]
```

## Advanced Features

### Query Modifiers
- `+require:[feature]` - Must have feature
- `-exclude:[feature]` - Must not have feature
- `tier:1` - Only Tier 1 servers
- `setup:<30min` - Quick setup only
- `free` - Free/open source only

### Examples:
- `/mcp-discover search +require:react -exclude:paid tier:1`
- `/mcp-stack python +require:async setup:<1hour`
- `/mcp-similar postgresql +require:free`

### Batch Operations
- `/mcp-discover --save [name]` - Save discovery session
- `/mcp-wizard --profile [team-size] [experience]` - Pre-configured wizard
- `/mcp-compare --all [category]` - Compare all in category

## Integration with Meta System

Commands automatically integrate with:
- `@meta/mcp-system/intelligence/` - For ecosystem updates
- `@knowledge-vault/databases/tools_services/` - For server profiles
- `@knowledge-vault/discovery/` - For discovery engine

## Implementation Details

**Location**: `@knowledge-vault/discovery/`

**Components Used**:
- `mcp-discovery-index.yaml` - Central search index
- `query-processor.yaml` - Natural language processing
- `views/*.yaml` - Organized server views
- `wizards/*.yaml` - Interactive wizards
- `similarity/*.yaml` - Recommendation engine

**Performance Targets**:
- Query response: < 2 seconds
- Wizard completion: < 7 questions
- Comparison generation: < 3 seconds
- Stack recommendations: < 5 seconds

## Usage Statistics Tracking

Track command usage for continuous improvement:
- Most common queries
- Popular technology stacks
- Frequently compared servers
- Wizard completion rates
- User satisfaction scores