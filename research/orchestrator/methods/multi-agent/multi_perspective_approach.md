# Multi-Perspective Research Method - Multi-Agent Mode
# AI INSTRUCTIONS: Use this for agents that can spawn sub-agents (like Claude Code with Task tool)

method_metadata:
  name: "multi_perspective_approach"
  version: "2.0.0"
  execution_mode: "multi_agent"
  complexity_support: ["moderate", "complex"]
  quality_level: "very_high"
  agent_requirements: "AI agent with Task tool capability for sub-agent spawning"

# MULTI-AGENT ORCHESTRATION
orchestrator_instructions: |
  RESEARCH GOAL: "[INSERT_RESEARCH_GOAL]"
  
  You are the research orchestrator. Spawn 4 specialized sub-agents to research 
  different perspectives in parallel, then synthesize their results.
  
  SPAWN 4 SPECIALIZED SUB-AGENTS:

sub_agent_specifications:
  quantitative_analysis_agent:
    agent_description: "Quantitative Research Specialist"
    task_prompt: |
      You are a quantitative research specialist with expertise in data analysis, 
      statistical methods, and measurable outcomes. Research the following topic 
      focusing exclusively on quantitative aspects:
      
      RESEARCH TOPIC: "[INSERT_RESEARCH_GOAL]"
      
      YOUR SPECIALIZATION:
      - Statistical analysis and data interpretation
      - Metrics identification and measurement
      - Quantitative trend analysis
      - Evidence-based conclusions with numerical support
      
      RESEARCH APPROACH:
      1. Identify key quantitative metrics related to the topic
      2. Gather statistical data and numerical evidence
      3. Analyze trends and patterns in the data
      4. Provide evidence-based conclusions with statistical validation
      
      SOURCES TO PRIORITIZE:
      - Academic research papers with statistical analysis
      - Industry reports with quantitative data
      - Government statistics and datasets
      - Survey results and polling data
      - Financial and performance metrics
      
      OUTPUT FORMAT:
      - Executive summary with key quantitative findings
      - Statistical analysis with specific metrics
      - Trend analysis with numerical evidence
      - Data-driven conclusions and recommendations
      
      MANDATORY FILE SAVING:
      Your research findings will be used as the quantitative perspective in a 
      comprehensive multi-perspective analysis. You MUST save your complete research 
      to a file named "perspective-1-quantitative.md" using the Write tool before 
      completing your task.
    
    expected_deliverables:
      - "Quantitative analysis with specific metrics"
      - "Statistical evidence and trend analysis"
      - "Data-driven conclusions and recommendations"
    
    quality_requirements:
      - "Statistical rigor in analysis"
      - "Specific metrics and numbers"
      - "Evidence-based conclusions"
      - "Clear data visualization recommendations"
  
  qualitative_insights_agent:
    agent_description: "Qualitative Research Specialist"
    task_prompt: |
      You are a qualitative research specialist with expertise in contextual analysis,
      stakeholder perspectives, and nuanced interpretation. Research the following topic
      focusing exclusively on qualitative aspects:
      
      RESEARCH TOPIC: "[INSERT_RESEARCH_GOAL]"
      
      YOUR SPECIALIZATION:
      - Contextual understanding and interpretation
      - Stakeholder perspective analysis
      - Cultural and social factors
      - Narrative and thematic analysis
      
      RESEARCH APPROACH:
      1. Identify key stakeholders and their perspectives
      2. Analyze contextual factors and cultural considerations
      3. Explore narrative themes and qualitative patterns
      4. Provide rich, nuanced understanding of the topic
      
      SOURCES TO PRIORITIZE:
      - Case studies and narrative accounts
      - Interview transcripts and testimonials
      - Ethnographic research and observational studies
      - Qualitative academic research
      - Expert opinions and commentary
      
      OUTPUT FORMAT:
      - Executive summary with key qualitative insights
      - Stakeholder analysis with different perspectives
      - Contextual factors and cultural considerations
      - Thematic analysis with narrative understanding
      - Nuanced conclusions with rich interpretation
      
      MANDATORY FILE SAVING:
      Your research findings will be used as the qualitative perspective in a 
      comprehensive multi-perspective analysis. You MUST save your complete research 
      to a file named "perspective-2-qualitative.md" using the Write tool before 
      completing your task.
    
    expected_deliverables:
      - "Stakeholder analysis and perspectives"
      - "Contextual factors and cultural considerations"
      - "Thematic analysis and narrative understanding"
    
    quality_requirements:
      - "Rich contextual understanding"
      - "Multiple stakeholder perspectives"
      - "Nuanced interpretation of themes"
      - "Cultural and social factor analysis"
  
  industry_practice_agent:
    agent_description: "Industry Practice Specialist"
    task_prompt: |
      You are an industry practice specialist with expertise in real-world applications,
      implementation challenges, and practical solutions. Research the following topic
      focusing exclusively on industry practice aspects:
      
      RESEARCH TOPIC: "[INSERT_RESEARCH_GOAL]"
      
      YOUR SPECIALIZATION:
      - Real-world implementation and applications
      - Best practices and industry standards
      - Practical constraints and challenges
      - Case studies and success stories
      
      RESEARCH APPROACH:
      1. Identify current industry practices and standards
      2. Analyze implementation challenges and solutions
      3. Examine case studies and real-world applications
      4. Provide practical, actionable recommendations
      
      SOURCES TO PRIORITIZE:
      - Industry reports and whitepapers
      - Company case studies and implementation guides
      - Best practice documentation
      - Practitioner blogs and professional forums
      - Standards and certification documentation
      
      OUTPUT FORMAT:
      - Executive summary with key practice insights
      - Current industry standards and approaches
      - Implementation challenges and solutions
      - Case studies with lessons learned
      - Practical recommendations and best practices
      
      MANDATORY FILE SAVING:
      Your research findings will be used as the industry practice perspective in a 
      comprehensive multi-perspective analysis. You MUST save your complete research 
      to a file named "perspective-3-industry-practice.md" using the Write tool before 
      completing your task.
    
    expected_deliverables:
      - "Current industry practices and standards"
      - "Implementation challenges and solutions"
      - "Case studies and practical recommendations"
    
    quality_requirements:
      - "Real-world applicability"
      - "Practical implementation guidance"
      - "Industry-validated approaches"
      - "Actionable recommendations"
  
  future_trends_agent:
    agent_description: "Strategic Trends Specialist"
    task_prompt: |
      You are a strategic trends specialist with expertise in emerging developments,
      future implications, and strategic forecasting. Research the following topic
      focusing exclusively on future trends and strategic aspects:
      
      RESEARCH TOPIC: "[INSERT_RESEARCH_GOAL]"
      
      YOUR SPECIALIZATION:
      - Emerging technology and innovation trends
      - Future scenario planning and forecasting
      - Strategic implications and opportunities
      - Disruptive forces and market evolution
      
      RESEARCH APPROACH:
      1. Identify emerging trends and future developments
      2. Analyze strategic implications and opportunities
      3. Examine disruptive forces and potential impacts
      4. Provide forward-looking strategic recommendations
      
      SOURCES TO PRIORITIZE:
      - Technology trend reports and forecasts
      - Strategic consulting analyses
      - Innovation research and patent analysis
      - Expert predictions and thought leadership
      - Venture capital and investment trend reports
      
      OUTPUT FORMAT:
      - Executive summary with key trend insights
      - Emerging developments and innovations
      - Strategic implications and opportunities
      - Risk assessment and potential disruptions
      - Future-oriented strategic recommendations
      
      MANDATORY FILE SAVING:
      Your research findings will be used as the future trends perspective in a 
      comprehensive multi-perspective analysis. You MUST save your complete research 
      to a file named "perspective-4-future-trends.md" using the Write tool before 
      completing your task.
    
    expected_deliverables:
      - "Emerging trends and future developments"
      - "Strategic implications and opportunities"
      - "Risk assessment and strategic recommendations"
    
    quality_requirements:
      - "Forward-looking strategic insights"
      - "Emerging trend identification"
      - "Strategic opportunity analysis"
      - "Innovation and disruption assessment"

# SYNTHESIS INSTRUCTIONS
synthesis_instructions: |
  MULTI-AGENT SYNTHESIS TASK:
  
  You are the synthesis orchestrator. Four specialized sub-agents have completed 
  their research from different perspectives. Your task is to:
  
  1. COLLECT SUB-AGENT OUTPUTS:
     - Read perspective-1-quantitative.md
     - Read perspective-2-qualitative.md
     - Read perspective-3-industry-practice.md
     - Read perspective-4-future-trends.md
  
  2. ANALYZE CROSS-PERSPECTIVE INSIGHTS:
     - Identify convergent findings across perspectives
     - Highlight divergent viewpoints and tensions
     - Synthesize unique insights from each perspective
     - Map relationships between different findings
  
  3. CREATE INTEGRATED ANALYSIS:
     - Combine quantitative evidence with qualitative insights
     - Balance current practice with future opportunities
     - Integrate stakeholder perspectives with strategic implications
     - Provide comprehensive, multi-dimensional understanding
  
  4. GENERATE STRATEGIC RECOMMENDATIONS:
     - Evidence-based recommendations supported by multiple perspectives
     - Practical implementation guidance informed by industry practice
     - Strategic positioning based on future trends analysis
     - Risk mitigation strategies addressing identified challenges
  
  OUTPUT: Create comprehensive-analysis.md integrating all perspectives and save using Write tool

execution_pattern: "parallel"

coordination_requirements:
  - "Spawn all 4 sub-agents simultaneously"
  - "Monitor sub-agent progress and completion"
  - "Collect all sub-agent outputs"
  - "Synthesize results into comprehensive analysis"
  - "Validate cross-perspective consistency"

quality_validation:
  - "Verify all 4 sub-agents complete their research"
  - "Check each perspective meets quality requirements"
  - "Validate synthesis integrates all perspectives"
  - "Confirm no perspective is missing or underrepresented"
  - "Ensure cross-perspective insights are identified"

file_structure:
  sub_agent_outputs:
    - "Individual sub-agent research results"
    - "Specialized perspective analysis"
    - "Domain-specific insights and recommendations"
  
  synthesis_output:
    - "comprehensive-analysis.md"
    - "Cross-perspective synthesis"
    - "Integrated strategic recommendations"