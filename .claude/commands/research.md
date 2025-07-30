Execute intelligent research using MCP-aware method selection and simplified coordination for: $ARGUMENTS

## Enhanced Research Workflow:

**Orchestrator Activation**: Follows @meta/shared/intention-detection-framework.md patterns with 95% confidence threshold using keyword detection: "research", "analyze", "investigate", "study", "explore", "examine"

1. **Pre-Research Registry Analysis** (MANDATORY): Execute registry similarity analysis against existing research in research/findings/research-registry.yaml
2. **MCP Intelligence Assessment**: Analyze research domain and select optimal MCP servers using @knowledge-vault/knowledge/ai-systems/frameworks/mcp-research-intelligence.md
3. **Extract Research Context** from the request using documented parameter extraction from claude-orchestrator-integration.yaml  
4. **Analyze Complexity** using @research/orchestrator/engines/context-analyzer.yaml scoring algorithm (simple/moderate/complex classification)
5. **Select Optimal Method** using intelligent selection algorithm based on complexity, domain, and MCP server availability
6. **Execute Research** using selected method (methods spawn their own specialized agents via Task tool)
7. **Generate Findings** following research-execution-log-template.yaml with quality metrics and method compliance validation
8. **Save Research** according to enhanced file structure with mandatory summary generation for research browser

## Intelligent Method Selection Process:

### Method Selection Algorithm:
```yaml
method_selection_logic:
  complex_comprehensive_research:
    triggers: "complexity=complex AND scope=(comprehensive|business|technical)"
    method: "complex_research"  # Spawns 5 specialized agents
    mcp_servers: "Domain-specific server mapping per module"
    
  complex_multi_perspective_research:
    triggers: "complexity=complex AND scope=(analytical|comparative|strategic)"
    method: "multi_perspective_approach"  # Spawns 4 perspective agents
    mcp_servers: "Perspective-specific server coordination"
    
  quality_focused_research:
    triggers: "quality_requirements>=95% OR accuracy_critical=true"
    method: "constitutional_ai"  # Quality-focused with self-correction
    mcp_servers: "Authority-tier server selection for validation"
    
  systematic_discovery_research:
    triggers: "complexity=moderate AND scope=exploratory"
    method: "step_by_step_research"  # 5-phase systematic approach
    mcp_servers: "Progressive server complexity by phase"
    
  general_purpose_research:
    triggers: "complexity=simple OR scope=general"
    method: "universal_research"  # Comprehensive template
    mcp_servers: "Anthropic trio + domain-appropriate servers"
```

### MCP Server Intelligence:
- **Domain Classification**: Analyze research topic for academic/technical/business/infrastructure domains
- **Server Availability**: Check authentication and setup complexity (Tier 1: ≤7, Tier 2: ≤5, Tier 3: avoid)
- **Intelligent Routing**: Select 3-7 servers maximum based on domain mapping and method requirements  
- **Fallback Strategy**: Graceful degradation to public APIs and fetch operations if servers unavailable

## Enhanced Research Execution:

### Registry Analysis & MCP Coordination:
1. **Pre-Research Validation**: Compare against research/findings/research-registry.yaml for similarity (≥95% = recommend existing, 70-94% = extend existing, <70% = proceed)
2. **MCP Server Selection**: Use domain analysis to select optimal servers from @knowledge-vault/knowledge/ai-systems/frameworks/mcp-research-intelligence.md
3. **Method Coordination**: Selected method spawns its own specialized agents - no need for additional orchestration

### Method Execution Patterns:
- **Multi-Agent Methods**: complex_research, multi_perspective_approach spawn specialized agents via Task tool
- **Single-Agent Methods**: constitutional_ai, step_by_step_research, universal_research execute with enhanced prompts
- **Quality Enhancement**: All methods include constitutional AI validation ≥95% compliance
- **MCP Integration**: Methods coordinate with selected servers for domain-appropriate information access

### Mandatory Research Completion:
```yaml
required_deliverables:
  research_content:
    - "research/findings/[topic]/research/comprehensive-analysis.md"
    - "research/findings/[topic]/research/[method-specific-outputs]"
  
  metadata_tracking:
    - "research/findings/[topic]/.meta/research-plan.md"
    - "research/findings/[topic]/.meta/research-sources.md"
    - "research/findings/[topic]/.meta/method-compliance.yaml"
    - "research/findings/[topic]/.meta/research-execution-log.yaml"
  
  human_friendly_summaries:
    - "research/findings/[topic]/summary.yaml"
    - "research/findings/research-browser.yaml" (updated)
```

### Quality Standards:
- **Constitutional AI**: ≥95% compliance across accuracy, transparency, completeness, responsibility, integrity
- **Method Compliance**: Validate that selected method requirements are properly followed
- **Source Diversity**: Multiple server types and authority levels for cross-validation
- **MCP Intelligence**: Domain-appropriate server selection with intelligent fallbacks

## Simplified Error Handling:

**If Core Framework Issues**: Use universal_research method with fetch/memory servers and constitutional AI validation. Still requires complete file structure and registry analysis.