# Claude Command: Hybrid Research Orchestrator

Use intelligent hybrid orchestrator for research requests: $ARGUMENTS

## Hybrid Research Orchestration Workflow:

1. **Claude Code Multi-Agent Mode (Default)**
   
   📖 Read: `research/orchestrator/engines/hybrid-orchestrator-controller.yaml`
   
   Claude Code execution mode:
   - Always uses multi-agent mode with Task tool capability
   - Spawns specialized sub-agents for comprehensive research
   - Saves all individual sub-agent research files
   
   Mode configuration:
   ```yaml
   execution_mode: "multi_agent"
   method_directory: "research/orchestrator/methods/multi-agent/"
   orchestrator_role: "spawn_and_coordinate_sub_agents"
   file_saving: "individual_files_plus_synthesis"
   ```

2. **Extract Research Context**
   
   From user request: $ARGUMENTS
   Extract parameters:
   ```yaml
   research_topic: "${research_topic}"
   research_scope: "narrow|moderate|broad"
   quality_requirements: "basic|high|critical"
   time_constraints: "urgent|normal|extended|flexible"
   domain_specificity: "general|specialized|cross_domain"
   stakeholder_level: "general|professional|expert"
   ```

3. **Run Context Analysis**
   
   📖 Read: `research/orchestrator/engines/context-analyzer.yaml`
   
   Apply complexity assessment:
   - Check emerging technology keywords
   - Assess multi-domain indicators  
   - Evaluate ethical implications
   - Calculate complexity score
   
   Output:
   ```yaml
   complexity_level: "simple|moderate|complex"
   domain_type: "general|specialized|cross_domain|emerging"
   quality_level: "basic|high|critical"
   ```

4. **Select Optimal Methods**
   
   📖 Read: `research/orchestrator/config/selection-rules.yaml`
   📖 Read: `research/orchestrator/config/method-registry.yaml`
   
   Method selection process:
   - Primary method from complexity mapping
   - Enhancement methods from quality requirements
   - Validate compatibility matrix
   - Route to appropriate mode directory
   
   Output:
   ```yaml
   selected_methods: ["method1", "method2"]
   execution_pattern: "sequential|parallel|hybrid"
   method_files: "research/orchestrator/methods/{mode}/{method}.md"
   estimated_duration: "time estimate"
   ```

5. **Execute Multi-Agent Research Orchestration**
   
   **Claude Code Multi-Agent Execution:**
   📖 Read: `research/orchestrator/engines/sub-agent-spawner.yaml`
   📖 Read method files from: `research/orchestrator/methods/multi-agent/`
   
   Execution process:
   - Load multi-agent method specifications
   - Spawn specialized sub-agents using Task tool
   - Coordinate parallel sub-agent execution
   - Each sub-agent saves research to reports/ folder with inline citations
   - Collect and validate all sub-agent outputs
   - Synthesize results into comprehensive analysis
   - Save simplified session info to .meta/ folder
   
   File outputs:
   Research Reports (reports/ folder):
   - Individual sub-agent files: reports/perspective-X-[description].md
   - Comprehensive synthesis: reports/comprehensive-analysis.md
   
   Session Info (.meta/ folder - hidden):
   - Research log: .meta/research-log.md
   - Source tracking: .meta/sources.md  
   - Session metadata: .meta/session-info.yaml
   
   Citation format: (Source Name, Year [https://full-url-here])

6. **Multi-Agent Orchestrator Summary Output**

   ```
   🔀 Multi-Agent Research Orchestrator Analysis
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Execution Mode: multi_agent
   Agent Type: Claude Code
   
   Context Analysis:
   ├── Complexity: ${complexity_level} (${confidence}% confidence)
   ├── Domain: ${domain_type} requiring ${expertise_level} expertise
   └── Quality Target: ${quality_level}
   
   Selected Methods:
   ├── Primary: ${primary_methods}
   ├── Enhancement: ${enhancement_methods}
   ├── Method Directory: research/orchestrator/methods/multi-agent/
   └── Execution Pattern: parallel sub-agent spawning
   
   Sub-Agent Coordination:
   ├── Sub-Agents Spawned: ${sub_agent_count}
   ├── Individual Files Saved: ${individual_file_count}
   ├── Synthesis Completed: comprehensive-analysis.md
   └── Metadata Saved: Complete research documentation
   
   Quality Checkpoints:
   ${quality_checkpoints}
   
   Estimated Duration: ${estimated_duration}
   ```

## File Access Patterns for Hybrid System:

**Core Engine Files:**
- Hybrid Controller: `research/orchestrator/engines/hybrid-orchestrator-controller.yaml`
- Sub-Agent Spawner: `research/orchestrator/engines/sub-agent-spawner.yaml`
- Context Analyzer: `research/orchestrator/engines/context-analyzer.yaml`
- Agent Capability Detector: `research/orchestrator/engines/agent-capability-detector.yaml`

**Configuration Files:**
- Method Registry: `research/orchestrator/config/method-registry.yaml`
- Selection Rules: `research/orchestrator/config/selection-rules.yaml`

**Method Files (Mode-Specific):**
- Multi-Agent Methods: `research/orchestrator/methods/multi-agent/[method_name].md`
- Single-Agent Methods: `research/orchestrator/methods/single-agent/[method_name].md`
- Existing Methods (Fallback): `research/orchestrator/methods/existing/[method_name].md`
- Advanced Methods: `research/orchestrator/methods/advanced/[method_name].md`
- Methods Index: `research/orchestrator/methods/methods-index.yaml`

**Templates:**
- Research Log: `research/templates/research-log-template.md`
- Sources: `research/templates/sources-template.md`
- Session Info: `research/templates/session-info-template.yaml`

**Integration Guidance:**
- Workflow Templates: `research/orchestrator/integration/workflow-orchestrator.yaml`
- Claude Instructions: `research/orchestrator/integration/claude-orchestrator-integration.yaml`

## Usage Examples:

**Claude Code Multi-Agent Research:**
```
User: "Research AI impact on healthcare"
→ Mode Detection: Claude Code → Multi-agent mode
→ Orchestrator Analysis: moderate complexity, cross-domain, high quality
→ Selected Methods: multi_perspective_approach (multi-agent version)
→ Execution: Spawn 4 specialized sub-agents in parallel
  ├── Quantitative Analysis Agent
  ├── Qualitative Insights Agent  
  ├── Industry Practice Agent
  └── Future Trends Agent
→ Result: Synthesized comprehensive analysis from all perspectives
```

**Other Agent Single-Agent Research:**
```
User: "Research AI impact on healthcare"  
→ Mode Detection: Other Agent → Single-agent mode
→ Orchestrator Analysis: moderate complexity, cross-domain, high quality
→ Selected Methods: multi_perspective_approach (single-agent version)
→ Execution: Sequential perspective analysis within single agent
  ├── Quantitative Analysis Perspective
  ├── Qualitative Insights Perspective
  ├── Industry Practice Perspective
  └── Future Trends Perspective
→ Result: Integrated analysis with perspective synthesis
```

**Complex Multi-Agent Research:**
```
User: "Analyze ethical implications of AGI on global economics"
→ Mode Detection: Claude Code → Multi-agent mode
→ Orchestrator Analysis: complex, cross-domain, critical quality
→ Selected Methods: complex_research (multi-agent) + constitutional_ai
→ Execution: Spawn specialized module agents for parallel research
→ Quality: Cross-agent validation and constitutional AI enhancement
```

## Interactive Options:

[1] Use hybrid orchestrator for current research request (auto-detects mode)
[2] Force multi-agent mode (if Task tool available)
[3] Force single-agent mode (compatibility mode)
[4] View method capabilities and selection rationale
[5] Customize method selection for specific needs
[6] Apply adaptive orchestration with mid-execution optimization
[7] Generate research quality assessment and improvement recommendations

---

**AI Instructions for Claude Code Multi-Agent System:**

**Multi-Agent Research Execution:**
1. Always use multi-agent mode with Task tool
2. Spawn specialized sub-agents for parallel research
3. Each sub-agent saves to reports/ folder with inline citations
4. Create simplified session tracking in .meta/ folder
5. Synthesize all sub-agent work into comprehensive analysis
6. Include full URLs in citation format: (Source, Year [https://full-url])

**File Structure Requirements:**
1. All research reports in reports/ folder (clean, visible)
2. All session info in .meta/ folder (hidden metadata)
3. Inline citations with complete URLs in all reports
4. Use provided templates for .meta/ files
5. Maintain clean separation between research and metadata

**Quality Standards:**
1. Every claim must have inline citation with full URL
2. All sub-agent files must be saved and preserved
3. Comprehensive synthesis must integrate all perspectives
4. Session tracking must be simple and minimal
5. Research quality over administrative complexity