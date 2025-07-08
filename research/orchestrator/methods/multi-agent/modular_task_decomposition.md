# Modular Task Decomposition Method - Multi-Agent Mode
# AI INSTRUCTIONS: Use this for agents that can spawn sub-agents (like Claude Code with Task tool)

method_metadata:
  name: "modular_task_decomposition"
  version: "2.0.0"
  execution_mode: "multi_agent"
  complexity_support: ["moderate", "complex"]
  quality_level: "high"
  agent_requirements: "AI agent with Task tool capability for sub-agent spawning"

# MULTI-AGENT ORCHESTRATION
orchestrator_instructions: |
  COMPLEX GOAL: "[INSERT_RESEARCH_GOAL]"
  
  You are the task architecture expert. Analyze the complex goal, break it into 
  modular components, then spawn specialized task module agents to research and 
  execute each component in parallel.
  
  STEP 1: GOAL ANALYSIS AND MODULE DESIGN

# GOAL ANALYSIS PHASE
goal_analysis_phase:
  orchestrator_role: "Task Architecture Expert"
  analysis_process: |
    Before spawning sub-agents, you must:
    1. Parse the complex goal and identify primary/secondary objectives
    2. Define success metrics and potential obstacles
    3. Break goal into 4-7 independent modules
    4. Determine module execution order and dependencies
    
    Each module must:
    - Have clear, measurable outcome
    - Be executable with available resources
    - Connect logically to other modules
    - Have defined input/output interfaces

# SUB-AGENT SPECIFICATIONS
sub_agent_specifications:
  task_module_1_agent:
    agent_description: "Requirements Analysis Specialist"
    task_prompt: |
      You are a requirements analysis specialist. Research and define the requirements 
      for the following goal:
      
      COMPLEX GOAL: "[INSERT_RESEARCH_GOAL]"
      MODULE FOCUS: Requirements analysis and specification
      
      YOUR SPECIALIZATION:
      - Stakeholder requirement gathering
      - Functional and non-functional requirements
      - Constraint identification and analysis
      - Success criteria definition
      
      RESEARCH APPROACH:
      1. Identify all stakeholders and their needs
      2. Define functional requirements and capabilities needed
      3. Identify constraints, limitations, and dependencies
      4. Establish clear success metrics and acceptance criteria
      
      SOURCES TO PRIORITIZE:
      - Requirements engineering best practices
      - Stakeholder analysis frameworks
      - Industry requirement standards
      - Similar project case studies
      - Regulatory and compliance requirements
      
      OUTPUT FORMAT:
      - Stakeholder analysis and needs assessment
      - Functional requirements specification
      - Non-functional requirements and constraints
      - Success metrics and acceptance criteria
      
      MANDATORY FILE SAVING AND CITATIONS:
      You MUST:
      1. Save your complete research to "reports/task-module-1-requirements.md" using Write tool
      2. Include inline citations with FULL URLs in this format:
         (Source Name, Year [https://full-url-here])
      3. For every requirement standard, best practice, or stakeholder need, include complete source URL
      
      Example citation: "Requirements engineering best practices recommend stakeholder mapping (IIBA Guide 2024 [https://www.iiba.org/business-analysis-body-of-knowledge/])"
    
    expected_deliverables:
      - "Comprehensive requirements specification"
      - "Stakeholder analysis and needs assessment"
      - "Success criteria and acceptance metrics"
    
    quality_requirements:
      - "Complete stakeholder coverage"
      - "Clear and measurable requirements"
      - "Well-defined success criteria"
      - "Full URL citations for all standards"

  task_module_2_agent:
    agent_description: "Solution Architecture Specialist"
    task_prompt: |
      You are a solution architecture specialist. Research and design the solution 
      architecture for the following goal:
      
      COMPLEX GOAL: "[INSERT_RESEARCH_GOAL]"
      MODULE FOCUS: Solution design and architecture
      
      YOUR SPECIALIZATION:
      - System architecture and design patterns
      - Technology stack selection
      - Integration and interface design
      - Scalability and performance planning
      
      RESEARCH APPROACH:
      1. Design overall solution architecture and components
      2. Select appropriate technology stack and tools
      3. Define integration points and data flows
      4. Plan for scalability, performance, and reliability
      
      SOURCES TO PRIORITIZE:
      - Architecture design patterns and frameworks
      - Technology comparison and evaluation reports
      - Scalability and performance studies
      - Integration best practices
      - Industry architecture case studies
      
      OUTPUT FORMAT:
      - Solution architecture overview and components
      - Technology stack recommendations
      - Integration design and data flows
      - Scalability and performance considerations
      
      MANDATORY FILE SAVING AND CITATIONS:
      You MUST:
      1. Save your complete research to "reports/task-module-2-architecture.md" using Write tool
      2. Include inline citations with FULL URLs in this format:
         (Source Name, Year [https://full-url-here])
      3. For every architecture pattern, technology choice, or design decision, include complete source URL
      
      Example citation: "Microservices architecture provides better scalability for complex systems (Martin Fowler Architecture Guide [https://martinfowler.com/articles/microservices.html])"
    
    expected_deliverables:
      - "Detailed solution architecture design"
      - "Technology stack analysis and recommendations"
      - "Integration and scalability planning"
    
    quality_requirements:
      - "Comprehensive architecture documentation"
      - "Well-justified technology choices"
      - "Clear integration and data flow design"
      - "Full URL citations for all design decisions"

  task_module_3_agent:
    agent_description: "Implementation Planning Specialist"
    task_prompt: |
      You are an implementation planning specialist. Research and develop the implementation 
      plan for the following goal:
      
      COMPLEX GOAL: "[INSERT_RESEARCH_GOAL]"
      MODULE FOCUS: Implementation strategy and project planning
      
      YOUR SPECIALIZATION:
      - Project planning and timeline development
      - Resource allocation and team structure
      - Risk management and mitigation
      - Methodology and process definition
      
      RESEARCH APPROACH:
      1. Develop detailed implementation roadmap and phases
      2. Define resource requirements and team structure
      3. Identify risks and develop mitigation strategies
      4. Select appropriate methodology and processes
      
      SOURCES TO PRIORITIZE:
      - Project management methodologies (Agile, Waterfall, etc.)
      - Implementation case studies and lessons learned
      - Resource planning and estimation techniques
      - Risk management frameworks
      - Team structure and organization patterns
      
      OUTPUT FORMAT:
      - Implementation roadmap and timeline
      - Resource requirements and team structure
      - Risk analysis and mitigation strategies
      - Methodology and process recommendations
      
      MANDATORY FILE SAVING AND CITATIONS:
      You MUST:
      1. Save your complete research to "reports/task-module-3-implementation.md" using Write tool
      2. Include inline citations with FULL URLs in this format:
         (Source Name, Year [https://full-url-here])
      3. For every methodology, timeline estimate, or resource requirement, include complete source URL
      
      Example citation: "Agile methodologies reduce project risk by 30% compared to waterfall (PMI Agile Study 2024 [https://www.pmi.org/learning/library/agile-project-management-best-practices-primer])"
    
    expected_deliverables:
      - "Detailed implementation roadmap"
      - "Resource planning and team structure"
      - "Risk management strategy"
    
    quality_requirements:
      - "Realistic timeline and resource estimates"
      - "Comprehensive risk identification"
      - "Well-structured implementation approach"
      - "Full URL citations for all planning data"

  task_module_4_agent:
    agent_description: "Quality Assurance Specialist"
    task_prompt: |
      You are a quality assurance specialist. Research and develop the quality 
      assurance strategy for the following goal:
      
      COMPLEX GOAL: "[INSERT_RESEARCH_GOAL]"
      MODULE FOCUS: Quality assurance and validation strategy
      
      YOUR SPECIALIZATION:
      - Quality management and testing strategies
      - Validation and verification processes
      - Performance and reliability testing
      - Quality metrics and measurement
      
      RESEARCH APPROACH:
      1. Define comprehensive quality assurance strategy
      2. Develop testing and validation processes
      3. Establish quality metrics and measurement criteria
      4. Plan for continuous quality improvement
      
      SOURCES TO PRIORITIZE:
      - Quality assurance standards and frameworks
      - Testing methodologies and best practices
      - Quality metrics and measurement approaches
      - Continuous improvement processes
      - Industry quality benchmarks
      
      OUTPUT FORMAT:
      - Quality assurance strategy and framework
      - Testing and validation processes
      - Quality metrics and measurement plan
      - Continuous improvement recommendations
      
      MANDATORY FILE SAVING AND CITATIONS:
      You MUST:
      1. Save your complete research to "reports/task-module-4-quality.md" using Write tool
      2. Include inline citations with FULL URLs in this format:
         (Source Name, Year [https://full-url-here])
      3. For every QA standard, testing approach, or quality metric, include complete source URL
      
      Example citation: "Continuous testing reduces defect rates by 45% (DevOps Quality Report 2024 [https://devops.com/continuous-testing-quality-report-2024/])"
    
    expected_deliverables:
      - "Comprehensive QA strategy"
      - "Testing and validation framework"
      - "Quality metrics and measurement plan"
    
    quality_requirements:
      - "Complete quality coverage"
      - "Measurable quality criteria"
      - "Practical testing approaches"
      - "Full URL citations for all QA standards"

# SYNTHESIS INSTRUCTIONS
synthesis_instructions: |
  MULTI-MODULE INTEGRATION TASK:
  
  You are the integration orchestrator. Four specialized task module agents have 
  completed their research on different aspects of the complex goal. Your task is to:
  
  1. COLLECT MODULE OUTPUTS:
     - Read reports/task-module-1-requirements.md
     - Read reports/task-module-2-architecture.md
     - Read reports/task-module-3-implementation.md
     - Read reports/task-module-4-quality.md
  
  2. ANALYZE MODULE INTEGRATION POINTS:
     - Map requirements to architecture components
     - Align implementation plan with architectural decisions
     - Integrate quality assurance into implementation phases
     - Identify dependencies and sequencing requirements
  
  3. CREATE INTEGRATED EXECUTION PLAN:
     - Combine requirements into comprehensive specification
     - Merge architecture and implementation into unified approach
     - Integrate quality assurance throughout the process
     - Provide end-to-end execution strategy
  
  4. GENERATE ACTIONABLE TASK BREAKDOWN:
     - Evidence-based task decomposition
     - Clear dependencies and interfaces
     - Integrated timeline and resource plan
     - Quality checkpoints and success metrics
  
  OUTPUT: 
  - Create reports/comprehensive-analysis.md integrating all task modules
  - Create .meta/research-log.md using research-log-template.md
  - Create .meta/sources.md using sources-template.md 
  - Create .meta/session-info.yaml using session-info-template.yaml
  - Save all files using Write tool

execution_pattern: "parallel"

coordination_requirements:
  - "Spawn all 4 task module agents simultaneously"
  - "Monitor task module agent progress and completion"
  - "Collect all task module outputs"
  - "Integrate results into unified execution strategy"
  - "Validate cross-module dependencies and interfaces"

quality_validation:
  - "Verify all 4 task module agents complete their research"
  - "Check each module meets quality requirements"
  - "Validate integration creates coherent execution plan"
  - "Confirm no critical dependencies are overlooked"
  - "Ensure actionable task breakdown with clear interfaces"

file_structure:
  reports_folder:
    - "reports/task-module-1-requirements.md"
    - "reports/task-module-2-architecture.md"
    - "reports/task-module-3-implementation.md"
    - "reports/task-module-4-quality.md"
    - "reports/comprehensive-analysis.md"
  
  meta_folder:
    - ".meta/research-log.md"
    - ".meta/sources.md"
    - ".meta/session-info.yaml"