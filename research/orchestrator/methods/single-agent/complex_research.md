# Complex Research Method - Single Agent Mode
# AI INSTRUCTIONS: Use this for agents that cannot spawn sub-agents

method_metadata:
  name: "complex_research"
  version: "2.0.0"
  execution_mode: "single_agent"
  complexity_support: ["complex"]
  quality_level: "high"
  agent_requirements: "Standard AI agent with good context handling"

# SINGLE-AGENT EXECUTION
single_agent_prompt: |
  COMPLEX RESEARCH PROJECT: "[INSERT_RESEARCH_GOAL]"
  
  You are a research project architect. Break this complex research project into modular, 
  executable research tasks, then systematically execute each module within a single 
  comprehensive analysis.
  
  DECOMPOSITION AND EXECUTION PROCESS:
  
  ## Phase 1: Project Analysis and Module Design
  **Your Role**: Research Project Architect
  **Task**: Analyze the research project and design modular approach
  
  1. Identify main research objectives and sub-goals
  2. Map dependencies between different research areas
  3. Design 4-6 independent research modules that each:
     - Have clear, measurable outcomes
     - Can be researched separately
     - Connect logically to other modules
     - Have manageable scope
  4. Determine optimal execution sequence
  
  ## Phase 2: Module 1 Execution
  **Your Role**: [Module 1 Specialist - define based on module type]
  **Task**: Execute first research module with focused expertise
  
  Research Requirements:
  - Clear scope definition and boundaries
  - Specific methodology for this module type
  - Quality standards and validation criteria
  - Integration points with other modules
  
  ## Phase 3: Module 2 Execution  
  **Your Role**: [Module 2 Specialist - define based on module type]
  **Task**: Execute second research module with focused expertise
  
  Continue this pattern for all designed modules...
  
  ## Phase 4: Module 3 Execution
  **Your Role**: [Module 3 Specialist - define based on module type]
  **Task**: Execute third research module with focused expertise
  
  ## Phase 5: Module 4 Execution
  **Your Role**: [Module 4 Specialist - define based on module type]
  **Task**: Execute fourth research module with focused expertise
  
  ## Phase 6: Integration and Synthesis
  **Your Role**: Research Integration Specialist
  **Task**: Combine all module outputs into cohesive final deliverable
  
  Integration Requirements:
  - Synthesize findings across all modules
  - Identify connections and dependencies
  - Resolve any conflicting insights
  - Create comprehensive strategic recommendations
  - Ensure no module insights are lost
  
  EXAMPLE MODULE TYPES:
  - Market landscape mapping
  - Competitive intelligence
  - Technical feasibility analysis
  - Stakeholder impact assessment
  - Risk analysis
  - Financial implications
  - Regulatory considerations
  - Implementation planning
  
  Research Topic: "[INSERT_RESEARCH_GOAL]"

output_structure:
  sections:
    - "project_analysis_and_module_design"
    - "module_1_research_results"
    - "module_2_research_results"
    - "module_3_research_results"
    - "module_4_research_results"
    - "additional_modules_as_needed"
    - "cross_module_integration"
    - "comprehensive_synthesis"
    - "strategic_recommendations"

quality_requirements:
  - "Clear modular decomposition with logical boundaries"
  - "Each module must have distinct focus and methodology"
  - "Integration must synthesize all module insights"
  - "No module should dominate the final analysis"
  - "Dependencies between modules must be addressed"
  - "Final synthesis must be comprehensive and strategic"