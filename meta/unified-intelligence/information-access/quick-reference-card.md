# Quick Reference: Unified Source Discovery Framework

## 🚀 Instant Implementation

### 1. Load Framework
```yaml
Read: "meta/information-access/source-discovery-framework.yaml"
```

### 2. Technology Detection Decision Tree
```yaml
IF topic contains ["react", "jsx", "hooks", "components"]:
  → USE: technology_mappings.react
  
IF topic contains ["typescript", "ts", "type safety", "interfaces"]:
  → USE: technology_mappings.typescript
  
IF topic contains ["python", "django", "flask", "fastapi", "backend"]:
  → USE: technology_mappings.python
  
IF topic contains ["database", "sql", "postgresql", "mysql", "mongodb"]:
  → USE: technology_mappings.database
  
IF topic contains ["ai", "llm", "gpt", "claude", "openai", "anthropic"]:
  → USE: technology_mappings.ai_language_models
  
ELSE:
  → USE: category_mappings.[frontend|backend|database|infrastructure|testing]
```

### 3. Common Source Coordination Patterns

#### Pattern A: Technology-Specific Research
```yaml
# Example: React Performance Research
sources:
  primary: "mcp__MCP_DOCKER__search_repositories + mcp__MCP_DOCKER__get-library-docs"
  supplementary: "WebFetch(react.dev) + Read(knowledge-vault/react/)"
  validation: "WebFetch(official docs)"
coordination: "parallel"
```

#### Pattern B: Category-Based Analysis  
```yaml
# Example: Backend Security Analysis
sources:
  primary: "mcp__MCP_DOCKER__search_repositories + WebSearch(security patterns)"
  supplementary: "Read(knowledge-vault/backend/) + WebFetch(security guides)"
  validation: "WebSearch(vulnerability databases)"
coordination: "sequential"
```

#### Pattern C: Knowledge Vault Fallback
```yaml
# Example: Unknown Technology
sources:
  primary: "Grep(knowledge-vault/databases/tools_services/) + WebSearch(technology docs)"
  supplementary: "mcp__MCP_DOCKER__search_repositories"
  validation: "WebFetch(official documentation)"
coordination: "conditional"
```

---

## 📋 Agent Implementation Checklist

### Pre-Flight Checks
- [ ] `Read meta/information-access/source-discovery-framework.yaml`
- [ ] Extract technology keywords from topic/request
- [ ] Check `meta/mcp-learning/usage-guides/[server-name]-guide.md` for known issues

### Source Selection
- [ ] Apply technology detection logic
- [ ] Load appropriate mapping (technology_mappings vs category_mappings)
- [ ] Identify primary, supplementary, and validation sources
- [ ] Choose coordination pattern (sequential/parallel/conditional)

### Execution
- [ ] Execute source access with error handling
- [ ] Document all sources for attribution
- [ ] Apply fallback procedures if sources fail
- [ ] Validate source diversity (≥3 source types)

### Integration
- [ ] Feed sources to research orchestrator (step_3_5_discover_information_sources)
- [ ] OR apply to PR validation with role-aware contexts
- [ ] Update research-sources.md with complete attribution
- [ ] Record successful patterns in MCP learning guides

---

## 🔧 Common Error Patterns & Solutions

### Error 1: MCP Server Unavailable
```yaml
Detection: "Connection refused" or "Server not found"
Solution: "Switch to WebSearch/WebFetch alternatives from same mapping"
Example: "GitHub MCP down → WebSearch site:github.com [query]"
```

### Error 2: Authentication Required
```yaml
Detection: "Authentication failed" or "API key required"
Solution: "Use non-authenticated sources from same category"
Notification: "Inform user about authentication requirements"
```

### Error 3: No Technology Match
```yaml
Detection: "Topic doesn't match any technology_mappings"
Solution: "Use closest category_mappings match"
Enhancement: "Consider adding new technology_mapping"
```

### Error 4: Rate Limiting
```yaml
Detection: "Rate limit exceeded" or "Too many requests"
Solution: "Coordinate request timing, switch to alternatives"
Prevention: "Use framework rate limiting coordination"
```

---

## 📊 Quality Validation Quick Checks

### Source Diversity Check
```yaml
Target: "≥3 different source types"
Valid: ["mcp-github", "context7-docs", "web-fetch", "knowledge-vault"]
Invalid: ["mcp-github", "mcp-github", "mcp-github"] # Only 1 type
```

### Coverage Completeness Check
```yaml
Critical Technologies: "Must have primary + supplementary + validation"
General Categories: "Must have primary + supplementary"
Fallback Queries: "Must have minimum 2 sources"
```

### Attribution Accuracy Check
```yaml
Required: "Source name, access pattern, timestamp, query/URL"
Format: "(Source: [name], [timestamp], [url/query])"
Location: "research-sources.md or PR validation report"
```

---

## 🎯 Integration Points

### Research Orchestrator
```yaml
File: "research/orchestrator/integration/claude-orchestrator-integration.yaml"
Step: "step_3_5_discover_information_sources"
Action: "Replace basic source discovery with unified framework results"
```

### AI-PR Validation
```yaml
File: "projects/ai-pr-validation-system/docs/file-type-analysis-templates.md"
Integration: "pr_validation_context mappings"
Action: "Use role-aware source selection for validation agents"
```

### Task Management
```yaml
File: "ai/workflows/task-management/CLAUDE.md"
Integration: "Research task special requirements"
Action: "Apply source attribution for research completion protocol"
```

---

## 🚨 Critical Reminders

1. **ALWAYS** load the framework before source discovery
2. **NEVER** skip error handling and fallback procedures  
3. **ALWAYS** document sources for attribution tracking
4. **VERIFY** source diversity meets minimum requirements
5. **UPDATE** MCP learning guides with new patterns

---

## 📖 Related Documentation

- **Complete Guide**: `meta/information-access/agent-usage-guide.md`
- **Framework Spec**: `meta/information-access/source-discovery-framework.yaml`
- **Error Learning**: `meta/mcp-learning/usage-guides/`
- **Main Instructions**: `CLAUDE.md` (Information Access Framework section)

---

**Last Updated**: 2025-07-28  
**Version**: 2.0.0 (Unified Framework)