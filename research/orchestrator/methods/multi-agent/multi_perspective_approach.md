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
      
      INTELLIGENT SOURCE COORDINATION:
      Apply unified source discovery framework from meta/information-access/source-discovery-framework.yaml:
      
      PRIMARY SOURCES (Technology-Specific if detected):
      - technology_mappings: "Use React/TypeScript/Python/Database mappings if topic involves specific technologies"
      - category_mappings: "Use frontend/backend/infrastructure mappings for broader domains"
      - mcp_servers: "GitHub repositories, technical documentation, code examples"
      
      QUANTITATIVE FOCUS SOURCES:
      - Academic research papers with statistical analysis
      - Industry reports with quantitative data and benchmarks
      - Government statistics and performance datasets
      - Survey results and polling data with statistical validation
      - Financial and performance metrics from authoritative sources
      
      SOURCE COORDINATION STRATEGY:
      - Apply parallel source access for comprehensive data gathering
      - Use MCP server coordination for technical repositories and documentation
      - Implement fallback to web sources if MCP servers unavailable
      - Cross-validate quantitative claims across multiple authoritative sources
      - Prioritize recent data sources for current trends and metrics
      
      OUTPUT FORMAT:
      - Executive summary with key quantitative findings
      - Statistical analysis with specific metrics
      - Trend analysis with numerical evidence
      - Data-driven conclusions and recommendations
      
      MANDATORY FILE SAVING AND CITATIONS:
      Your research findings will be used as the quantitative perspective in a 
      comprehensive multi-perspective analysis. You MUST:
      
      1. Save your complete research to "reports/perspective-1-quantitative.md" using Write tool
      2. Include inline citations with FULL URLs in this format:
         (Source Name, Year [https://full-url-here])
      3. For every fact, statistic, or claim, include the complete source URL
      
      Example citation: "AI adoption increased 35% in 2024 (McKinsey AI Survey 2024 [https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai-in-2024])"
    
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
      
      INTELLIGENT SOURCE COORDINATION:
      Apply unified source discovery framework for qualitative perspectives:
      
      PRIMARY SOURCES (Technology-Specific if detected):
      - technology_mappings: "User experience insights, community discussions, developer testimonials"
      - category_mappings: "Domain-specific qualitative research and case studies"
      - mcp_servers: "GitHub discussions, documentation narratives, community insights"
      
      QUALITATIVE FOCUS SOURCES:
      - Case studies and narrative accounts with rich contextual detail
      - Interview transcripts, testimonials, and user experience reports
      - Ethnographic research and observational studies
      - Qualitative academic research with thematic analysis
      - Expert opinions, commentary, and thought leadership content
      
      SOURCE COORDINATION STRATEGY:
      - Use sequential access for in-depth contextual analysis
      - Coordinate community sources (forums, discussions) with official documentation
      - Apply adaptive routing to find high-quality narrative sources
      - Cross-validate stakeholder perspectives across multiple qualitative sources
      - Prioritize diverse perspectives and underrepresented voices
      
      OUTPUT FORMAT:
      - Executive summary with key qualitative insights
      - Stakeholder analysis with different perspectives
      - Contextual factors and cultural considerations
      - Thematic analysis with narrative understanding
      - Nuanced conclusions with rich interpretation
      
      MANDATORY FILE SAVING AND CITATIONS:
      Your research findings will be used as the qualitative perspective in a 
      comprehensive multi-perspective analysis. You MUST:
      
      1. Save your complete research to "reports/perspective-2-qualitative.md" using Write tool
      2. Include inline citations with FULL URLs in this format:
         (Source Name, Year [https://full-url-here])
      3. For every quote, case study, or qualitative insight, include the complete source URL
      
      Example citation: "Stakeholders reported implementation challenges (Harvard Business Review Case Study 2024 [https://hbr.org/full-article-url-here])"
    
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
      
      INTELLIGENT SOURCE COORDINATION:
      Apply unified source discovery framework for industry practices:
      
      PRIMARY SOURCES (Technology-Specific if detected):
      - technology_mappings: "Production implementations, enterprise case studies, technical best practices"
      - category_mappings: "Industry-specific practices and domain standards"
      - mcp_servers: "GitHub Enterprise repos, industry documentation, implementation guides"
      
      INDUSTRY PRACTICE FOCUS SOURCES:
      - Industry reports and whitepapers from authoritative organizations
      - Company case studies and implementation guides with measurable outcomes
      - Best practice documentation from recognized industry leaders
      - Practitioner blogs and professional forums with validated experiences
      - Standards and certification documentation from official bodies
      
      SOURCE COORDINATION STRATEGY:
      - Prioritize authoritative industry sources and recognized standards bodies
      - Use MCP coordination for accessing enterprise repositories and documentation
      - Apply adaptive routing to find current implementation examples
      - Cross-validate practices across multiple industry sources
      - Focus on recent implementations and current industry trends
      
      OUTPUT FORMAT:
      - Executive summary with key practice insights
      - Current industry standards and approaches
      - Implementation challenges and solutions
      - Case studies with lessons learned
      - Practical recommendations and best practices
      
      MANDATORY FILE SAVING AND CITATIONS:
      Your research findings will be used as the industry practice perspective in a 
      comprehensive multi-perspective analysis. You MUST:
      
      1. Save your complete research to "reports/perspective-3-industry-practice.md" using Write tool
      2. Include inline citations with FULL URLs in this format:
         (Source Name, Year [https://full-url-here])
      3. For every best practice, case study, or industry standard, include the complete source URL
      
      Example citation: "Companies using agile methodology report 25% faster delivery (State of Agile Report 2024 [https://stateofagile.com/report-2024-full-url])"
    
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
      
      INTELLIGENT SOURCE COORDINATION:
      Apply unified source discovery framework for future trends analysis:
      
      PRIMARY SOURCES (Technology-Specific if detected):
      - technology_mappings: "Emerging tech developments, future roadmaps, innovation patterns"
      - category_mappings: "Strategic industry evolution and emerging domain trends"
      - mcp_servers: "GitHub trending repos, cutting-edge research, innovation showcases"
      
      FUTURE TRENDS FOCUS SOURCES:
      - Technology trend reports and forecasts from reputable research organizations
      - Strategic consulting analyses with future scenario modeling
      - Innovation research, patent analysis, and emerging technology assessments
      - Expert predictions and thought leadership from recognized industry visionaries
      - Venture capital and investment trend reports indicating market directions
      
      SOURCE COORDINATION STRATEGY:
      - Prioritize forward-looking sources with predictive analytics
      - Use parallel access for comprehensive trend coverage across domains
      - Apply adaptive routing to find cutting-edge research and innovation sources
      - Cross-validate trend predictions across multiple authoritative sources
      - Focus on convergent trends and strategic inflection points
      
      OUTPUT FORMAT:
      - Executive summary with key trend insights
      - Emerging developments and innovations
      - Strategic implications and opportunities
      - Risk assessment and potential disruptions
      - Future-oriented strategic recommendations
      
      MANDATORY FILE SAVING AND CITATIONS:
      Your research findings will be used as the future trends perspective in a 
      comprehensive multi-perspective analysis. You MUST:
      
      1. Save your complete research to "reports/perspective-4-future-trends.md" using Write tool
      2. Include inline citations with FULL URLs in this format:
         (Source Name, Year [https://full-url-here])
      3. For every trend prediction, forecast, or strategic insight, include the complete source URL
      
      Example citation: "Experts predict 40% growth in quantum computing by 2030 (Gartner Technology Trends 2024 [https://www.gartner.com/full-report-url-here])"
    
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
     - Read reports/perspective-1-quantitative.md
     - Read reports/perspective-2-qualitative.md
     - Read reports/perspective-3-industry-practice.md
     - Read reports/perspective-4-future-trends.md
  
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
  
  OUTPUT: 
  - Create reports/comprehensive-analysis.md integrating all perspectives
  - Create .meta/research-log.md using research-log-template.md
  - Create .meta/sources.md using sources-template.md 
  - Create .meta/session-info.yaml using session-info-template.yaml
  - Save all files using Write tool

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
  reports_folder:
    - "reports/perspective-1-quantitative.md"
    - "reports/perspective-2-qualitative.md"
    - "reports/perspective-3-industry-practice.md"
    - "reports/perspective-4-future-trends.md"
    - "reports/comprehensive-analysis.md"
  
  meta_folder:
    - ".meta/research-log.md"
    - ".meta/sources.md"
    - ".meta/session-info.yaml"