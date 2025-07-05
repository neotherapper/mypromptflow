# Claude Command: Orchestrate Research

Use intelligent meta-prompt orchestrator for research requests: $ARGUMENTS

## Research Orchestration Workflow:

1. **Extract Research Context**
   
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

2. **Run Context Analysis**
   
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

3. **Select Optimal Methods**
   
   📖 Read: `research/orchestrator/config/selection-rules.yaml`
   📖 Read: `research/orchestrator/config/method-registry.yaml`
   
   Method selection process:
   - Primary method from complexity mapping
   - Enhancement methods from quality requirements
   - Validate compatibility matrix
   - Determine execution pattern
   
   Output:
   ```yaml
   selected_methods: ["method1", "method2"]
   execution_pattern: "sequential|parallel|hybrid"
   estimated_duration: "time estimate"
   ```

4. **Execute Methods with Orchestrator Guidance**
   
   📖 Read method files from:
   - `research/orchestrator/methods/existing/` (11 existing methods)
   - `research/orchestrator/methods/advanced/` (4 advanced methods)
   
   Apply methods in sequence:
   - Follow execution pattern
   - Apply quality checkpoints
   - Use enhancement methods
   
   Quality validation:
   - constitutional_ai for ethical validation
   - self_consistency for critical accuracy
   - iterative_refinement for improvement

5. **Orchestrator Summary Output**

   ```
   🧠 Research Orchestrator Analysis
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Context Analysis:
   ├── Complexity: ${complexity_level} (${confidence}% confidence)
   ├── Domain: ${domain_type} requiring ${expertise_level} expertise
   └── Quality Target: ${quality_level}
   
   Selected Methods:
   ├── Primary: ${primary_methods}
   ├── Enhancement: ${enhancement_methods}
   └── Pattern: ${execution_pattern}
   
   Execution Plan:
   ${execution_sequence}
   
   Quality Checkpoints:
   ${quality_checkpoints}
   
   Estimated Duration: ${estimated_duration}
   ```

## File Access Patterns for Claude:

**Configuration Files:**
- Context Analyzer: `research/orchestrator/engines/context-analyzer.yaml`
- Method Registry: `research/orchestrator/config/method-registry.yaml`
- Selection Rules: `research/orchestrator/config/selection-rules.yaml`

**Method Files:**
- Existing Methods: `research/orchestrator/methods/existing/[method_name].md`
- Advanced Methods: `research/orchestrator/methods/advanced/[method_name].md`
- Methods Index: `research/orchestrator/methods/methods-index.yaml`

**Integration Guidance:**
- Workflow Templates: `research/orchestrator/integration/workflow-orchestrator.yaml`
- Claude Instructions: `research/orchestrator/integration/claude-orchestrator-integration.yaml`

## Usage Examples:

**Simple Research Request:**
```
User: "Research remote work productivity impact"
→ Orchestrator Analysis: moderate complexity, business domain, high quality
→ Selected Methods: domain_adaptive + constitutional_ai
→ Execution: sequential pattern with quality validation
```

**Complex Research Request:**
```
User: "Analyze ethical implications of AGI on global economics"
→ Orchestrator Analysis: complex, cross-domain, critical quality
→ Selected Methods: multi_perspective_approach + tree_of_thoughts + constitutional_ai + self_consistency
→ Execution: hybrid pattern with extensive validation
```

## Interactive Options:

[1] Use orchestrator for current research request
[2] View method capabilities and selection rationale
[3] Customize method selection for specific needs
[4] Apply adaptive orchestration with mid-execution optimization
[5] Generate research quality assessment and improvement recommendations

---

**AI Instructions for Claude:**
1. Always use this orchestrator workflow for research requests
2. Read configuration files to understand method selection logic
3. Apply selected methods from appropriate directories
4. Follow execution patterns and quality checkpoints
5. Provide orchestrator analysis summary to user
6. Document method effectiveness for future optimization