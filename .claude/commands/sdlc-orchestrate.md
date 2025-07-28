# /sdlc-orchestrate Command

**AI Agent Instruction**: SDLC-aware agent orchestration for 6-stage maritime insurance platform development workflow with specialized subagent coordination.

## Usage
```bash
/sdlc-orchestrate [stage] [deliverable]
/sdlc-orchestrate workflow [feature-name]
/sdlc-orchestrate cross-stage [transition]
```

Examples:
```bash
/sdlc-orchestrate requirements "user authentication system"
/sdlc-orchestrate workflow "policy calculation engine"
/sdlc-orchestrate cross-stage "design-to-planning"
```

## Command Description

**Target AI Agent**: Claude Code with Task, Read, Edit, and coordination tools  
**Execution Type**: SDLC-aware multi-agent workflow coordination  
**Resource Efficiency**: Stage-specific subagent activation with cross-stage dependency management  
**Dependencies**: Leverages orchestrate-agents.md foundation with SDLC specialization  
**Revolutionary Feature**: 6-stage SDLC workflow orchestration with maritime insurance domain expertise

This instruction extends the agent orchestration capabilities from orchestrate-agents.md with comprehensive SDLC stage coordination, specialized subagent management, and maritime insurance platform development optimization.

## SDLC Orchestration Framework

When this command is executed, perform the following SDLC-aware orchestration:

### Stage 1: SDLC Context Analysis and Planning

**AI Agent Instructions**: Execute SDLC-aware planning building on orchestrate-agents.md foundation:

**Step 1.1: SDLC Stage Detection and Validation**
```yaml
stage_analysis:
  stage_identification:
    stage_1_requirements:
      deliverables: ["user stories", "acceptance criteria", "business requirements", "feasibility analysis"]
      prerequisites: ["stakeholder alignment", "business context"]
      
    stage_2_design:
      deliverables: ["UI/UX designs", "system architecture", "technical specifications", "integration plans"] 
      prerequisites: ["validated requirements", "technical constraints"]
      
    stage_3_planning:
      deliverables: ["sprint plans", "capacity allocation", "task assignments", "resource planning"]
      prerequisites: ["design approval", "architecture validation"]
      
    stage_4_implementation:
      deliverables: ["feature code", "API implementations", "database changes", "integration code"]
      prerequisites: ["development planning", "environment setup"]
      
    stage_5_testing:
      deliverables: ["test suites", "quality reports", "performance validation", "security testing"]
      prerequisites: ["feature completion", "test environment setup"]
      
    stage_6_deployment:
      deliverables: ["production deployment", "monitoring setup", "rollback procedures", "performance baselines"]
      prerequisites: ["quality certification", "deployment approval"]
```

**Step 1.2: Enhanced Dependency Analysis**
Execute foundation dependency analysis from orchestrate-agents.md with SDLC enhancements:
- Analyze SDLC stage dependencies and prerequisites
- Check for cross-stage integration requirements
- Identify required specialized subagents
- Map deliverable dependencies to SDLC workflow

**Step 1.3: SDLC Subagent Registry Discovery**
```bash
# Use Read tool to discover available SDLC subagents
find .claude/agents/ -name "*.md" -type f
```

Expected SDLC subagents:
- `requirements-analyst.md` (Stage 1)
- `ui-ux-specialist.md` (Stage 2)
- `system-architect.md` (Stage 2)  
- `capacity-planner.md` (Stage 3)
- `implementation-lead.md` (Stage 4)
- `qa-specialist.md` (Stage 5)
- `deployment-coordinator.md` (Stage 6)

**Step 1.4: SDLC Orchestration Plan Generation**
```
🚀 SDLC Orchestration Plan for: [deliverable]
═══════════════════════════════════════════════════

📊 SDLC Stage Analysis:
  🎯 Primary Stage: [stage_name] ([stage_number])
  🔄 Cross-Stage Dependencies: [dependency_count] ([affected_stages])
  📋 Required Prerequisites: [prerequisites_list]

🤖 Specialized Subagent Activation:
  ├── Primary: [primary_subagent] ([expertise_area])
  ├── Supporting: [supporting_subagents] ([coordination_needed])
  └── Cross-Stage: [cross_stage_subagents] ([integration_points])

⏳ Execution Timeline:
  [Phase-by-phase execution plan with estimated timelines]
```

### Stage 2: SDLC-Aware Agent Spawning and Coordination

**AI Agent Instructions**: Enhanced agent spawning with SDLC specialization:

**Step 2.1: Primary SDLC Subagent Activation**
Based on stage analysis, activate primary specialized subagent:

```yaml
stage_specific_spawning:
  stage_1_requirements:
    primary_agent: "requirements-analyst"
    spawning_parameters:
      description: "Business requirements analysis and JIRA integration"
      prompt: "You are a Requirements Analyst specialist from .claude/agents/requirements-analyst.md. Analyze the request: [deliverable]. Apply comprehensive requirements analysis including business context extraction, user story generation, feasibility assessment, and automated JIRA Epic/Story creation. Focus on maritime insurance domain expertise and integration with WorkOS, JIRA, and Sentry. Generate structured requirements document with business validation."
      context: "Maritime insurance platform, 4-person team, React/FastAPI stack"
      expected_tokens: 200
      
  stage_2_design:
    primary_agents: ["ui-ux-specialist", "system-architect"]
    parallel_execution: true
    coordination_required: true
    spawning_parameters:
      ui_ux_specialist:
        description: "UI/UX design and Figma integration"
        prompt: "You are a UI/UX Specialist from .claude/agents/ui-ux-specialist.md. Create comprehensive design for: [deliverable]. Apply user-centered design methodology including persona analysis, user journey mapping, Figma design system integration, and React component specifications. Focus on maritime insurance UI patterns and accessibility compliance. Generate high-fidelity designs with developer handoff specifications."
        context: "Maritime insurance platform, design system compliance, React components"
        expected_tokens: 180
      
      system_architect:
        description: "Technical architecture and AWS infrastructure"
        prompt: "You are a System Architect from .claude/agents/system-architect.md. Design technical architecture for: [deliverable]. Apply comprehensive architecture framework including React frontend, FastAPI backend, PostgreSQL database, and AWS infrastructure. Focus on scalability, security, and WorkOS/JIRA/Sentry integration. Generate system architecture document with infrastructure specifications."
        context: "AWS cloud architecture, maritime insurance platform, security compliance"
        expected_tokens: 220
        
  # [Continue for all 6 stages...]
```

**Step 2.2: Supporting Agent Coordination**
Execute foundation orchestration workflow from orchestrate-agents.md:
- Create specialized agent prompts with SDLC context
- Include relevant shared instruction libraries
- Set SDLC-specific quality criteria
- Establish cross-stage coordination protocols

**Step 2.3: Cross-Stage Integration Setup**
```yaml
cross_stage_coordination:
  integration_points:
    - Stage 1→2: Requirements to design handoff validation
    - Stage 2→3: Design to planning capacity assessment  
    - Stage 3→4: Planning to implementation coordination
    - Stage 4→5: Implementation to testing validation
    - Stage 5→6: Testing to deployment certification
    
  coordination_mechanisms:
    - Shared context propagation between stages
    - Quality gate validation at stage transitions
    - Cross-stage dependency tracking and resolution
    - Stakeholder communication and approval workflows
```

### Stage 3: Enhanced Coordination and Quality Management

**AI Agent Instructions**: Advanced coordination with SDLC quality gates:

**Step 3.1: Foundation Coordination Execution**
Execute complete Phase 3 from orchestrate-agents.md:
- Monitor agent progress with SDLC context
- Share outputs between dependent agents
- Handle conflicts with stage-specific resolution
- Validate outputs against SDLC requirements

**Step 3.2: SDLC Quality Gate Integration**
Apply stage-specific quality gates during coordination:
```yaml
quality_gate_validation:
  stage_transition_gates:
    requirements_to_design:
      criteria: ["Stakeholder approval ≥95%", "Feasibility validated", "JIRA structure complete"]
      validation: "Requirements completeness and business alignment"
      
    design_to_planning:
      criteria: ["Design system compliance ≥95%", "Architecture approved", "Technical feasibility confirmed"]
      validation: "Design quality and implementation readiness"
      
    planning_to_implementation:
      criteria: ["Sprint plan complete", "Capacity validated", "Team alignment confirmed"]
      validation: "Development readiness and resource allocation"
      
    implementation_to_testing:
      criteria: ["Feature complete", "Code review approved", "Integration tested"]
      validation: "Implementation quality and testing readiness"
      
    testing_to_deployment:
      criteria: ["Test coverage ≥85%", "Quality metrics passed", "Security validated"]
      validation: "Production readiness and deployment approval"
```

**Step 3.3: Maritime Insurance Domain Integration**
Apply domain-specific coordination patterns:
- Insurance regulatory compliance validation
- Maritime business process alignment
- ActuariaI calculation accuracy verification
- Lloyd's of London standards compliance

### Stage 4: SDLC-Enhanced Synthesis and Delivery

**AI Agent Instructions**: Enhanced synthesis with SDLC deliverable creation:

**Step 4.1: Foundation Synthesis Execution**  
Execute complete Phase 4 from orchestrate-agents.md:
- Collect all agent outputs with SDLC context
- Create final deliverable using stage dependencies
- Update knowledge base registry with SDLC tracking
- Generate comprehensive summary report

**Step 4.2: SDLC Stage Deliverable Creation**
Create stage-specific deliverables based on orchestration results:
```yaml
deliverable_generation:
  stage_1_deliverables:
    - "requirements-specification.md": Comprehensive business requirements
    - "user-stories.yaml": JIRA-ready Epic and Story structure  
    - "feasibility-assessment.md": Technical and business feasibility analysis
    - "stakeholder-communication.md": Approval and validation documentation
    
  stage_2_deliverables:
    - "ui-ux-designs/": Figma designs and component specifications
    - "system-architecture.md": Technical architecture documentation
    - "integration-specifications.md": API contracts and service integration
    - "design-handoff-package/": Developer-ready design assets
    
  stage_3_deliverables:
    - "sprint-plan.yaml": JIRA sprint configuration and task assignments
    - "capacity-allocation.md": Team resource planning and skill assignments
    - "development-timeline.md": Implementation schedule and milestones
    - "risk-mitigation.md": Risk assessment and contingency planning
    
  # [Continue for stages 4-6...]
```

**Step 4.3: Cross-Stage Integration Documentation**
Document stage transitions and dependencies:
- Stage completion certification
- Next stage readiness assessment  
- Handoff documentation and context
- Quality gate validation results

**Step 4.4: Enhanced Summary Reporting**
```
🚀 SDLC ORCHESTRATION RESULTS
════════════════════════════════════════════════

📊 STAGE EXECUTION SUMMARY:
  🎯 Primary Stage: [stage_name] - [COMPLETED/IN_PROGRESS/BLOCKED]
  🤖 Subagent Coordination: [activated_count] specialists - [success_rate]%
  📋 Deliverables Created: [deliverable_count] ([deliverable_list])
  🎖️ Quality Gates: [passed_count]/[total_count] PASSED

🔄 CROSS-STAGE INTEGRATION:
  ✅ Stage Prerequisites: [met_count]/[total_count] validated
  🔗 Dependency Resolution: [resolved_count] dependencies handled
  📊 Integration Points: [integration_summary]

🎯 MARITIME INSURANCE DOMAIN:
  ⚖️ Regulatory Compliance: [compliance_status]
  🏛️ Lloyd's Standards: [standards_compliance]  
  💼 Business Process Alignment: [alignment_score]%

📋 DELIVERABLES SUMMARY:
  [Comprehensive list of created deliverables with quality metrics]

🚀 NEXT STEPS:
  [Stage-specific recommendations and next actions]
  [Quality gate requirements for stage transition]
  [Cross-stage coordination requirements]

✅ SDLC orchestration complete - Stage: [stage] - Quality: [overall_score]% - Ready for: [next_stage]
```

## SDLC Orchestration Patterns

### Workflow Orchestration Modes

**Single Stage Mode**: `/sdlc-orchestrate requirements "user authentication"`
- Focus on single SDLC stage deliverable creation
- Activate stage-specific primary subagent
- Apply stage-appropriate quality gates
- Generate stage deliverables with next-stage preparation

**Full Workflow Mode**: `/sdlc-orchestrate workflow "policy calculation engine"`  
- Orchestrate complete 6-stage SDLC workflow
- Coordinate sequential stage progression
- Manage cross-stage dependencies and handoffs
- Generate comprehensive feature development lifecycle

**Cross-Stage Transition Mode**: `/sdlc-orchestrate cross-stage "design-to-planning"`
- Focus on stage transition validation and coordination
- Ensure quality gate compliance for stage progression
- Validate prerequisites and deliverable completeness  
- Prepare handoff documentation and context

### Advanced Orchestration Capabilities

**Maritime Insurance Specialization**:
- Domain-specific workflow optimization for insurance processes
- Regulatory compliance integration throughout SDLC stages
- Actuarial accuracy validation for calculation components
- Lloyd's of London standards compliance verification

**Quality Gate Automation**:
- Automated quality criteria validation at stage transitions
- Stage-specific success metrics and KPI tracking
- Cross-stage dependency validation and resolution
- Stakeholder approval workflow automation

**Resource Optimization**:
- Intelligent subagent activation based on deliverable requirements
- Parallel execution coordination for design stage (UI/UX + Architecture)
- Context propagation optimization across stage transitions
- Maritime insurance expertise integration throughout workflow

## Execution Instructions

When user runs `/sdlc-orchestrate requirements "user authentication system"`:

1. **SDLC Context Analysis**: Identify stage 1 requirements workflow
2. **Dependency Analysis**: Execute foundation analysis with SDLC enhancements  
3. **Requirements Analyst Activation**: Spawn requirements-analyst subagent with maritime insurance context
4. **Quality Gate Application**: Apply stage 1 quality criteria and validation
5. **Deliverable Generation**: Create requirements specification, user stories, and feasibility assessment
6. **Stage Transition Preparation**: Prepare handoff to design stage with validated requirements
7. **Comprehensive Reporting**: Document orchestration results and next-stage readiness

## Implementation Notes

This command extends the **orchestrate-agents.md foundation** with comprehensive SDLC specialization:

### SDLC Enhancements
- **6-Stage Workflow Integration**: Complete SDLC stage coordination with specialized subagents
- **Quality Gate Automation**: Stage-specific quality criteria and validation automation
- **Cross-Stage Dependency Management**: Comprehensive stage transition and handoff coordination
- **Maritime Insurance Domain Focus**: Industry-specific workflow optimization and compliance

### Foundation Preservation
- **Agent Coordination Patterns**: Maintains core orchestration workflow from orchestrate-agents.md
- **Dependency Analysis**: Preserves comprehensive dependency analysis and planning
- **Quality Validation**: Extends quality criteria with SDLC-specific requirements
- **Result Synthesis**: Enhances synthesis with stage-specific deliverable creation

### Advanced Capabilities
- **Parallel Agent Coordination**: Design stage coordination of UI/UX specialist and system architect
- **Context Propagation**: Intelligent context sharing across stage transitions
- **Resource Optimization**: Stage-appropriate subagent activation and coordination
- **Stakeholder Integration**: JIRA automation and WorkOS integration throughout SDLC stages

This SDLC-enhanced command enables comprehensive maritime insurance platform development through specialized agent orchestration, quality gate automation, and cross-stage workflow coordination.