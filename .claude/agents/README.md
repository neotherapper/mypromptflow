# SDLC Subagent System Documentation

**Version**: 1.0.0  
**Last Updated**: 2025-01-28  
**Registry**: [registry.yaml](./registry.yaml)

## Overview

The SDLC Subagent System provides specialized AI agents for comprehensive 6-stage Software Development Life Cycle (SDLC) workflow management, specifically optimized for maritime insurance platform development with React frontend, FastAPI backend, and AWS infrastructure.

## Quick Start

### Basic Usage

**Single Stage Operation:**
```bash
# Use Task tool to activate specific subagent
Task(description="Requirements analysis", prompt="You are a Requirements Analyst from .claude/agents/requirements-analyst.md. Analyze the user authentication system requirements...")
```

**SDLC Workflow Orchestration:**
```bash
# Orchestrate complete stage workflow
/sdlc-orchestrate requirements "user authentication system"
/sdlc-orchestrate workflow "policy calculation engine"
/sdlc-orchestrate cross-stage "design-to-planning"
```

**SDLC-Enhanced PR Validation:**
```bash
# Validate PR with stage-specific quality gates
/sdlc-validate-pr 23
/sdlc-validate-pr 45 implementation
```

## Architecture Overview

### 6-Stage SDLC Framework

```
Stage 1: Business Ideation & Requirements
├── requirements-analyst.md
└── Output: Requirements specification, user stories, JIRA structure

Stage 2: Design & Architecture  
├── ui-ux-specialist.md (parallel)
├── system-architect.md (parallel)
└── Output: UI designs, technical architecture, integration specs

Stage 3: Development Planning
├── capacity-planner.md
└── Output: Sprint plans, capacity allocation, task assignments

Stage 4: Implementation
├── implementation-lead.md  
└── Output: Feature code, quality validation, team coordination

Stage 5: Testing & Quality Assurance
├── qa-specialist.md
└── Output: Test suites, quality reports, performance validation

Stage 6: Deployment & Monitoring
├── deployment-coordinator.md
└── Output: Production deployment, monitoring setup, baselines
```

### Technology Stack Integration

**Frontend**: React + TypeScript with TanStack ecosystem  
**Backend**: FastAPI + Python with Domain-Driven Design  
**Database**: PostgreSQL with SQLAlchemy and Alembic migrations  
**Infrastructure**: AWS with CDK Infrastructure as Code  
**Tools**: WorkOS (auth), JIRA (project management), Sentry (monitoring)

## Subagent Catalog

### Stage 1: Requirements Analyst

**File**: `requirements-analyst.md`  
**Purpose**: Transform business ideas into structured technical specifications  
**Key Features**:
- Natural language requirement extraction
- Automated JIRA Epic/Story creation
- Technical and business feasibility assessment
- Maritime insurance domain expertise

**Usage Example**:
```yaml
Task:
  description: "Business requirements analysis for policy management"
  prompt: "You are a Requirements Analyst from .claude/agents/requirements-analyst.md. Analyze the policy management system requirements. Focus on maritime insurance workflows, regulatory compliance, and JIRA integration. Generate comprehensive requirements specification with user stories and acceptance criteria."
  context: "Maritime insurance platform, 4-person team, React/FastAPI stack"
```

### Stage 2: UI/UX Specialist & System Architect

**UI/UX Specialist** (`ui-ux-specialist.md`):
- User-centered design with maritime insurance patterns
- Figma integration and design system management
- WCAG AA accessibility compliance
- React component specifications

**System Architect** (`system-architect.md`):
- AWS cloud architecture design
- React/FastAPI/PostgreSQL optimization
- Security and compliance framework
- API design and integration patterns

**Parallel Coordination Example**:
```bash
/sdlc-orchestrate design "claims processing interface"
# Activates both UI/UX specialist and system architect in parallel
# Coordinates design and technical architecture development
# Ensures design-architecture alignment and integration
```

### Stage 3: Capacity Planner

**File**: `capacity-planner.md`  
**Purpose**: AI-enhanced sprint planning and resource optimization  
**Key Features**:
- 4-person team capacity modeling
- Skill-based task assignment algorithms
- JIRA automation for sprint creation
- Predictive velocity forecasting

### Stage 4: Implementation Lead

**File**: `implementation-lead.md`  
**Purpose**: Development execution coordination and quality enforcement  
**Key Features**:
- Cross-functional team collaboration
- Code quality gates and review orchestration
- CI/CD pipeline integration
- Technical risk management

### Stage 5: QA Specialist

**File**: `qa-specialist.md`  
**Purpose**: Comprehensive testing and quality validation  
**Key Features**:
- Multi-layer testing strategy (unit/integration/E2E)
- Performance and security testing
- User acceptance testing coordination
- Maritime insurance domain testing

### Stage 6: Deployment Coordinator

**File**: `deployment-coordinator.md`  
**Purpose**: Production deployment and monitoring orchestration  
**Key Features**:
- Zero-downtime deployment strategies
- AWS infrastructure management
- Sentry monitoring integration
- Incident response and rollback procedures

## Integration Patterns

### Cross-Stage Coordination

**Stage Transitions** follow quality gate validation:

```yaml
Requirements → Design:
  Prerequisites: ["Stakeholder approval ≥95%", "Feasibility validated", "JIRA structure complete"]
  Handoff: ["Requirements specification", "User personas", "Technical constraints"]

Design → Planning:  
  Prerequisites: ["Design system compliance ≥95%", "Architecture approved", "Technical feasibility confirmed"]
  Handoff: ["High-fidelity designs", "Architecture documentation", "Implementation complexity assessment"]

Planning → Implementation:
  Prerequisites: ["Sprint plan approved", "Capacity validated", "Team alignment confirmed"]  
  Handoff: ["Sprint plan with assignments", "Capacity allocation", "Development environment setup"]

Implementation → Testing:
  Prerequisites: ["Feature completion verified", "Code quality standards met", "Integration issues resolved"]
  Handoff: ["Feature implementation complete", "Code review approved", "Integration testing passed"]

Testing → Deployment:
  Prerequisites: ["All testing phases passed", "Performance benchmarks met", "Security compliance verified"]
  Handoff: ["Quality certification", "Performance baselines", "Security validation"]
```

### Tool Integration

**WorkOS Integration**:
- SAML/OIDC authentication and authorization
- Organization-based access control
- Multi-factor authentication enforcement
- Role-based permission management

**JIRA Integration**:
- Automated Epic and Story creation
- Sprint planning and task assignment
- Capacity tracking and velocity analysis
- Cross-stage dependency management

**Sentry Integration**:
- Real-time error monitoring and alerting
- Performance monitoring and optimization
- Custom maritime insurance business contexts
- Incident response and resolution tracking

## Usage Patterns

### 1. Individual Subagent Activation

**When to Use**: Specific stage work or focused expertise needed

```yaml
# Direct subagent activation via Task tool
Task:
  description: "UI/UX design for dashboard"
  prompt: "You are a UI/UX Specialist from .claude/agents/ui-ux-specialist.md. Create comprehensive dashboard design for maritime insurance claims management. Apply user-centered design methodology with maritime domain patterns."
  subagent_type: "ui-ux-specialist"
```

### 2. Stage Orchestration

**When to Use**: Complete stage deliverable creation with coordination

```bash
# Stage-specific orchestration
/sdlc-orchestrate requirements "vessel registration system"
/sdlc-orchestrate design "claims processing workflow"  
/sdlc-orchestrate planning "Q1 sprint preparation"
```

### 3. Full Workflow Orchestration

**When to Use**: End-to-end feature development lifecycle

```bash
# Complete 6-stage workflow
/sdlc-orchestrate workflow "policy calculation engine"
# Executes: Requirements → Design → Planning → Implementation → Testing → Deployment
# Manages cross-stage dependencies and quality gates
# Provides comprehensive feature development coordination
```

### 4. Cross-Stage Transition Management

**When to Use**: Stage handoffs and quality gate validation

```bash
# Stage transition validation
/sdlc-orchestrate cross-stage "implementation-to-testing"
# Validates implementation completion
# Prepares testing environment and data
# Ensures quality gate compliance for stage progression
```

## Best Practices

### Subagent Activation Guidelines

**Context Provision**:
- Always provide clear project context (maritime insurance platform)
- Specify technology stack constraints (React/FastAPI/PostgreSQL)
- Include team composition (4-person team with defined roles)
- Reference integration requirements (WorkOS/JIRA/Sentry)

**Quality Standards**:
- Maintain test coverage requirements (≥85% unit, ≥70% integration)
- Apply security validation (zero critical vulnerabilities)
- Ensure performance benchmarks (≤500ms API response, ≤2s frontend load)
- Validate accessibility compliance (WCAG AA standards)

### Cross-Stage Coordination

**Dependency Management**:
- Validate stage prerequisites before progression
- Document handoff deliverables and quality criteria
- Maintain context continuity across stage transitions
- Track cross-stage impact and integration requirements

**Quality Gate Enforcement**:
- Apply stage-specific validation criteria
- Ensure stakeholder approval and sign-off
- Validate technical feasibility and implementation readiness
- Document quality metrics and compliance status

### Maritime Insurance Domain Focus

**Regulatory Compliance**:
- Lloyd's of London standards validation
- IMO regulatory requirement compliance
- Data privacy and GDPR compliance verification
- Maritime insurance regulatory standards adherence

**Business Process Alignment**:
- Policy underwriting and risk assessment workflows
- Claims processing and settlement procedures
- Actuarial calculation accuracy and precision
- Audit logging and compliance reporting

## Advanced Features

### AI-Enhanced Capabilities

**Predictive Analysis**:
- Capacity planning with velocity forecasting
- Risk assessment with historical data analysis
- Performance optimization recommendations
- Quality metrics prediction and trend analysis

**Intelligent Automation**:
- JIRA workflow automation and optimization
- Code review process enhancement
- Test automation and regression detection
- Deployment automation with intelligent rollback

### Performance Optimization

**Resource Efficiency**:
- Conditional subagent activation based on requirements
- Parallel execution for design stage coordination
- Context propagation optimization across transitions
- Maritime insurance expertise integration throughout workflow

**Quality Assurance**:
- Revolutionary intent-implementation validation integration
- Stage-specific quality gate automation
- Cross-stage dependency validation and resolution
- Comprehensive testing strategy with domain expertise

## Troubleshooting

### Common Issues

**Subagent Activation Failures**:
```yaml
Problem: "Subagent not found or activation timeout"
Solution: 
  - Verify subagent file exists in .claude/agents/
  - Check Task tool parameters and context
  - Validate subagent registry configuration
```

**Cross-Stage Coordination Issues**:
```yaml
Problem: "Quality gate failures or dependency conflicts"
Solution:
  - Review stage prerequisites and deliverables
  - Validate cross-stage integration requirements
  - Check stakeholder approval and technical validation
```

**Integration Tool Failures**:
```yaml
Problem: "JIRA/WorkOS/Sentry integration errors"
Solution:
  - Verify MCP server configuration and authentication
  - Check integration pattern implementation
  - Review error logs and connectivity status
```

### Performance Monitoring

**Subagent Performance Metrics**:
- Activation time and response latency
- Quality output metrics and stakeholder satisfaction
- Cross-stage coordination efficiency
- Domain expertise application effectiveness

**System Integration Health**:
- JIRA automation success rates
- WorkOS authentication reliability
- Sentry monitoring coverage and alerting
- AWS infrastructure performance and availability

## Support and Maintenance

### Registry Updates

**Adding New Subagents**:
1. Create subagent file in `.claude/agents/`
2. Update `registry.yaml` with subagent configuration
3. Add integration patterns and usage examples
4. Test cross-stage coordination and quality gates
5. Update documentation and best practices

**Modifying Existing Subagents**:
1. Review impact on cross-stage dependencies
2. Update registry configuration and metrics
3. Validate integration pattern compatibility
4. Test stage transition and quality gate compliance
5. Update usage examples and troubleshooting guides

### Quality Assurance

**Testing Procedures**:
- Individual subagent functionality validation
- Cross-stage coordination and dependency testing
- Integration tool connectivity and automation testing
- Performance benchmark and quality metric validation

**Monitoring and Maintenance**:
- Regular registry validation and configuration review
- Subagent performance monitoring and optimization
- Integration pattern effectiveness analysis
- Domain expertise accuracy and compliance verification

## Conclusion

The SDLC Subagent System provides comprehensive maritime insurance platform development workflow management through specialized AI agents, quality gate automation, and cross-stage coordination. By following the documented patterns and best practices, teams can achieve optimal development efficiency, quality assurance, and regulatory compliance throughout the complete software development lifecycle.

For detailed technical specifications, refer to individual subagent files and the comprehensive registry configuration.