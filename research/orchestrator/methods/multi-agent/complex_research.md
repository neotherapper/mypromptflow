# Complex Research Method - Multi-Agent Mode
# AI INSTRUCTIONS: Use this for agents that can spawn sub-agents (like Claude Code with Task tool)

method_metadata:
  name: "complex_research"
  version: "2.0.0"
  execution_mode: "multi_agent"
  complexity_support: ["complex"]
  quality_level: "high"
  agent_requirements: "AI agent with Task tool capability for sub-agent spawning"

# MULTI-AGENT ORCHESTRATION
orchestrator_instructions: |
  COMPLEX RESEARCH PROJECT: "[INSERT_RESEARCH_GOAL]"
  
  You are the research orchestrator. Analyze the complex research project, design modular 
  approach, then spawn specialized module agents to research each component in parallel.
  
  STEP 1: ANALYZE AND DESIGN MODULES

# PROJECT ANALYSIS AND MODULE DESIGN
project_analysis_phase:
  orchestrator_role: "Research Project Architect"
  analysis_process: |
    Before spawning sub-agents, you must:
    1. Identify main research objectives, sub-goals, and dependencies
    2. Design 4-6 independent research modules
    3. Determine optimal execution sequence for module agents
    4. Define clear interfaces between modules
    
    Each module must:
    - Have clear, measurable outcomes
    - Be researchable by a specialized agent
    - Connect logically to other modules
    - Have manageable scope (2-4 hours of research)

# SUB-AGENT SPECIFICATIONS
sub_agent_specifications:
  module_1_agent:
    agent_description: "Market Landscape Research Specialist"
    task_prompt: |
      You are a market landscape research specialist. Research the market aspects 
      of the following topic:
      
      RESEARCH TOPIC: "[INSERT_RESEARCH_GOAL]"
      MODULE FOCUS: Market landscape mapping and competitive analysis
      
      YOUR SPECIALIZATION:
      - Market size and growth analysis
      - Competitive landscape mapping
      - Industry structure and dynamics
      - Market opportunities and gaps
      
      RESEARCH APPROACH:
      1. Define market boundaries and segments
      2. Identify key players and competitive dynamics
      3. Analyze market size, growth trends, and forecasts
      4. Map market opportunities and white spaces
      
      SOURCES TO PRIORITIZE:
      - Industry analyst reports (Gartner, McKinsey, etc.)
      - Market research firms (IDC, Forrester, etc.)
      - Company financial reports and investor presentations
      - Trade publications and industry news
      - Government market statistics
      
      OUTPUT FORMAT:
      - Executive summary of market landscape
      - Market size and growth analysis
      - Competitive landscape map
      - Market opportunities and recommendations
      
      MANDATORY FILE SAVING AND CITATIONS:
      You MUST:
      1. Save your complete research to "reports/module-1-market-landscape.md" using Write tool
      2. Include inline citations with FULL URLs in this format:
         (Source Name, Year [https://full-url-here])
      3. For every market statistic, forecast, or competitive insight, include complete source URL
      
      Example citation: "The global AI market is projected to reach $1.8 trillion by 2030 (Gartner AI Market Forecast 2024 [https://www.gartner.com/en/newsroom/press-releases/2024-full-url])"
    
    expected_deliverables:
      - "Market size and growth analysis with sources"
      - "Competitive landscape mapping"
      - "Market opportunity identification"
    
    quality_requirements:
      - "Quantitative market data with sources"
      - "Comprehensive competitive analysis"
      - "Actionable market insights"
      - "Full URL citations for all claims"

  module_2_agent:
    agent_description: "Technical Feasibility Research Specialist"
    task_prompt: |
      You are a technical feasibility research specialist. Research the technical 
      aspects of the following topic:
      
      RESEARCH TOPIC: "[INSERT_RESEARCH_GOAL]"
      MODULE FOCUS: Technical feasibility and implementation requirements
      
      YOUR SPECIALIZATION:
      - Technology stack analysis
      - Implementation complexity assessment
      - Technical risk evaluation
      - Infrastructure and resource requirements
      
      RESEARCH APPROACH:
      1. Identify core technical components and requirements
      2. Assess technology readiness and maturity
      3. Evaluate implementation complexity and challenges
      4. Analyze infrastructure and resource needs
      
      SOURCES TO PRIORITIZE:
      - Technical documentation and whitepapers
      - Academic research papers on relevant technologies
      - Open source project documentation
      - Technology vendor specifications
      - Engineering blogs and case studies
      
      OUTPUT FORMAT:
      - Technical architecture overview
      - Technology stack recommendations
      - Implementation complexity assessment
      - Risk analysis and mitigation strategies
      
      MANDATORY FILE SAVING AND CITATIONS:
      You MUST:
      1. Save your complete research to "reports/module-2-technical-feasibility.md" using Write tool
      2. Include inline citations with FULL URLs in this format:
         (Source Name, Year [https://full-url-here])
      3. For every technical specification, benchmark, or implementation detail, include complete source URL
      
      Example citation: "Kubernetes adoption increased 67% in enterprise environments (CNCF Survey 2024 [https://www.cncf.io/reports/cncf-annual-survey-2024/])"
    
    expected_deliverables:
      - "Technical architecture and requirements"
      - "Technology stack analysis"
      - "Implementation risk assessment"
    
    quality_requirements:
      - "Detailed technical analysis"
      - "Realistic feasibility assessment"
      - "Implementation roadmap guidance"
      - "Full URL citations for all technical claims"

  module_3_agent:
    agent_description: "Risk Assessment Research Specialist"
    task_prompt: |
      You are a risk assessment research specialist. Research the risk aspects 
      of the following topic:
      
      RESEARCH TOPIC: "[INSERT_RESEARCH_GOAL]"
      MODULE FOCUS: Risk analysis and mitigation strategies
      
      YOUR SPECIALIZATION:
      - Risk identification and classification
      - Impact and probability assessment
      - Regulatory and compliance risks
      - Financial and operational risks
      
      RESEARCH APPROACH:
      1. Identify potential risks across multiple dimensions
      2. Assess probability and impact of identified risks
      3. Analyze regulatory and compliance requirements
      4. Develop risk mitigation and contingency strategies
      
      SOURCES TO PRIORITIZE:
      - Risk management frameworks and standards
      - Regulatory guidance and compliance documents
      - Industry risk reports and case studies
      - Insurance and actuarial data
      - Legal and regulatory analysis
      
      OUTPUT FORMAT:
      - Comprehensive risk register
      - Risk impact and probability matrix
      - Regulatory compliance requirements
      - Risk mitigation strategies and action plans
      
      MANDATORY FILE SAVING AND CITATIONS:
      You MUST:
      1. Save your complete research to "reports/module-3-risk-assessment.md" using Write tool
      2. Include inline citations with FULL URLs in this format:
         (Source Name, Year [https://full-url-here])
      3. For every risk factor, regulation, or mitigation strategy, include complete source URL
      
      Example citation: "Data breach costs averaged $4.45 million in 2024 (IBM Cost of Data Breach Report 2024 [https://www.ibm.com/reports/data-breach])"
    
    expected_deliverables:
      - "Comprehensive risk identification and assessment"
      - "Regulatory compliance analysis"
      - "Risk mitigation strategies"
    
    quality_requirements:
      - "Systematic risk analysis"
      - "Quantified risk assessments where possible"
      - "Actionable mitigation strategies"
      - "Full URL citations for all risk data"

  module_4_agent:
    agent_description: "Financial Impact Research Specialist"
    task_prompt: |
      You are a financial impact research specialist. Research the financial 
      aspects of the following topic:
      
      RESEARCH TOPIC: "[INSERT_RESEARCH_GOAL]"
      MODULE FOCUS: Financial analysis and economic impact assessment
      
      YOUR SPECIALIZATION:
      - Cost-benefit analysis
      - ROI and financial modeling
      - Funding and investment requirements
      - Economic impact assessment
      
      RESEARCH APPROACH:
      1. Identify all relevant costs and financial implications
      2. Analyze potential benefits and revenue opportunities
      3. Develop ROI models and financial projections
      4. Assess funding requirements and financing options
      
      SOURCES TO PRIORITIZE:
      - Financial analyst reports and models
      - Industry cost benchmarks and studies
      - Investment research and venture capital data
      - Economic impact studies
      - Government financial and economic data
      
      OUTPUT FORMAT:
      - Comprehensive cost analysis
      - Benefit identification and quantification
      - ROI models and financial projections
      - Funding requirements and financing options
      
      MANDATORY FILE SAVING AND CITATIONS:
      You MUST:
      1. Save your complete research to "reports/module-4-financial-impact.md" using Write tool
      2. Include inline citations with FULL URLs in this format:
         (Source Name, Year [https://full-url-here])
      3. For every cost figure, ROI calculation, or financial projection, include complete source URL
      
      Example citation: "AI implementation typically requires 18-24 months to achieve positive ROI (Deloitte AI ROI Study 2024 [https://www2.deloitte.com/insights/us/en/focus/cognitive-technologies/ai-investment-return-study.html])"
    
    expected_deliverables:
      - "Detailed financial analysis and modeling"
      - "ROI projections and break-even analysis"
      - "Funding requirements and options"
    
    quality_requirements:
      - "Realistic financial modeling"
      - "Well-supported cost and benefit estimates"
      - "Clear investment recommendations"
      - "Full URL citations for all financial data"

  module_5_agent:
    agent_description: "Implementation Planning Research Specialist"
    task_prompt: |
      You are an implementation planning research specialist. Research the implementation 
      aspects of the following topic:
      
      RESEARCH TOPIC: "[INSERT_RESEARCH_GOAL]"
      MODULE FOCUS: Implementation strategy and execution planning
      
      YOUR SPECIALIZATION:
      - Implementation methodology and best practices
      - Project planning and timeline development
      - Resource requirements and allocation
      - Success factors and performance metrics
      
      RESEARCH APPROACH:
      1. Research proven implementation methodologies
      2. Identify critical success factors and best practices
      3. Analyze resource requirements and timeline considerations
      4. Develop performance metrics and success criteria
      
      SOURCES TO PRIORITIZE:
      - Implementation case studies and success stories
      - Project management methodologies and frameworks
      - Best practice guides and implementation standards
      - Consultant reports on implementation strategies
      - Academic research on implementation success factors
      
      OUTPUT FORMAT:
      - Implementation methodology recommendations
      - Project timeline and milestone planning
      - Resource requirements and team structure
      - Success metrics and performance indicators
      
      MANDATORY FILE SAVING AND CITATIONS:
      You MUST:
      1. Save your complete research to "reports/module-5-implementation-planning.md" using Write tool
      2. Include inline citations with FULL URLs in this format:
         (Source Name, Year [https://full-url-here])
      3. For every methodology, timeline estimate, or success factor, include complete source URL
      
      Example citation: "Agile implementation approaches show 40% higher success rates (Project Management Institute Study 2024 [https://www.pmi.org/learning/library/agile-implementation-success-factors-study])"
    
    expected_deliverables:
      - "Implementation strategy and methodology"
      - "Project planning and timeline guidance"
      - "Resource requirements and success metrics"
    
    quality_requirements:
      - "Practical implementation guidance"
      - "Realistic timelines and resource estimates"
      - "Measurable success criteria"
      - "Full URL citations for all implementation data"

# SYNTHESIS INSTRUCTIONS
synthesis_instructions: |
  MULTI-MODULE SYNTHESIS TASK:
  
  You are the synthesis orchestrator. Five specialized module agents have completed 
  their research on different aspects of the complex project. Your task is to:
  
  1. COLLECT MODULE OUTPUTS:
     - Read reports/module-1-market-landscape.md
     - Read reports/module-2-technical-feasibility.md
     - Read reports/module-3-risk-assessment.md
     - Read reports/module-4-financial-impact.md
     - Read reports/module-5-implementation-planning.md
  
  2. ANALYZE CROSS-MODULE DEPENDENCIES:
     - Identify how market insights affect technical decisions
     - Map financial constraints to implementation planning
     - Connect risk factors to technical and financial considerations
     - Synthesize timing dependencies across modules
  
  3. CREATE INTEGRATED STRATEGIC ANALYSIS:
     - Combine market opportunity with technical feasibility
     - Balance financial projections with risk assessments
     - Integrate implementation timeline with resource availability
     - Provide comprehensive strategic recommendations
  
  4. GENERATE ACTIONABLE ROADMAP:
     - Evidence-based strategic recommendations
     - Phased implementation approach
     - Risk-adjusted financial projections
     - Success metrics and milestones
  
  OUTPUT: 
  - Create reports/comprehensive-analysis.md integrating all modules
  - Create .meta/research-log.md using research-log-template.md
  - Create .meta/sources.md using sources-template.md 
  - Create .meta/session-info.yaml using session-info-template.yaml
  - Save all files using Write tool

execution_pattern: "parallel"

coordination_requirements:
  - "Spawn all 5 module agents simultaneously"
  - "Monitor module agent progress and completion"
  - "Collect all module outputs"
  - "Synthesize results into comprehensive strategic analysis"
  - "Validate cross-module consistency and integration"

quality_validation:
  - "Verify all 5 module agents complete their research"
  - "Check each module meets quality requirements"
  - "Validate synthesis integrates all module insights"
  - "Confirm no module dependencies are overlooked"
  - "Ensure actionable strategic recommendations"

file_structure:
  reports_folder:
    - "reports/module-1-market-landscape.md"
    - "reports/module-2-technical-feasibility.md"
    - "reports/module-3-risk-assessment.md"
    - "reports/module-4-financial-impact.md"
    - "reports/module-5-implementation-planning.md"
    - "reports/comprehensive-analysis.md"
  
  meta_folder:
    - ".meta/research-log.md"
    - ".meta/sources.md"
    - ".meta/session-info.yaml"