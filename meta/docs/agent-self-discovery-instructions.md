# Agent Self-Discovery Instructions - Claude Code Max Integration

## Overview

This document provides comprehensive instructions for AI agents to discover and load role-specific knowledge contexts without token constraints. The system leverages Claude Code Max capabilities with the role-aware knowledge management architecture implemented in the knowledge vault.

## Core Principles

### 1. Agent Role Self-Assessment

**Before requesting context, agents should:**
1. **Analyze the task requirements** to understand what role perspective is needed
2. **Identify the technologies involved** in the specific task or file analysis
3. **Determine the appropriate specialist role** based on task complexity and scope
4. **Choose the most relevant knowledge contexts** for comprehensive task completion

### 2. REQUEST_CONTEXT() Pattern

**Standard Syntax:**
```
REQUEST_CONTEXT(technology-role)
REQUEST_CONTEXT(technology1-role1, technology2-role2, technology3-role3)
```

**Available Role-Technology Combinations:**
- `react-architect` - High-level React architecture and design patterns
- `react-frontend-dev` - React implementation patterns, hooks, components
- `react-performance` - React optimization, profiling, bundle analysis
- `react-accessibility` - React accessibility standards and WCAG compliance
- `typescript-architect` - TypeScript type system design and project architecture
- `typescript-frontend-dev` - TypeScript implementation patterns and development
- `typescript-performance` - TypeScript compilation and runtime optimization
- `typescript-testing` - TypeScript testing patterns and type safety validation
- `testing-architect` - Testing strategy, architecture, and quality frameworks
- `testing-frontend-dev` - Frontend testing patterns and component validation
- `testing-performance` - Performance testing and benchmarking strategies
- `testing-security` - Security testing, vulnerability scanning, OWASP compliance

## Role-Based Context Loading Strategies

### 1. Architect Role Context Loading

**When to Use Architect Role:**
- Designing system architecture or component hierarchies
- Making technology selection decisions
- Planning scalable solutions or refactoring approaches
- Reviewing high-level design patterns and best practices

**Context Loading Pattern:**
```
As an architect agent, I need to understand the high-level design patterns and architectural decisions for this React TypeScript application.

REQUEST_CONTEXT(react-architect, typescript-architect)

This provides me with:
- React component architecture patterns and state management strategies
- TypeScript type system design and project structure guidance
- Scalability considerations and performance architecture patterns
```

### 2. Frontend Developer Role Context Loading

**When to Use Frontend Developer Role:**
- Implementing specific components or features
- Reviewing code implementation details
- Working with hooks, state management, or UI patterns
- Analyzing specific development patterns and techniques

**Context Loading Pattern:**
```
As a frontend developer agent, I need to review this React component implementation for best practices and potential improvements.

REQUEST_CONTEXT(react-frontend-dev, typescript-frontend-dev)

This provides me with:
- Latest React 19 patterns, hooks usage, and component implementation
- TypeScript implementation patterns for frontend development
- Form handling, event management, and state management techniques
```

### 3. Performance Specialist Role Context Loading

**When to Use Performance Specialist Role:**
- Analyzing bundle sizes, runtime performance, or optimization opportunities
- Reviewing memory usage, loading performance, or rendering efficiency
- Implementing performance monitoring or optimization strategies
- Conducting performance audits or benchmarking

**Context Loading Pattern:**
```
As a performance specialist agent, I need to analyze this application for performance bottlenecks and optimization opportunities.

REQUEST_CONTEXT(react-performance, typescript-performance, testing-performance)

This provides me with:
- React DevTools Profiler usage and rendering optimization techniques
- TypeScript compilation performance and runtime optimization strategies
- Performance testing methodologies and benchmarking frameworks
```

### 4. Security Specialist Role Context Loading

**When to Use Security Specialist Role:**
- Conducting security audits or vulnerability assessments
- Reviewing authentication, authorization, or data protection implementations
- Analyzing for OWASP Top 10 vulnerabilities or security best practices
- Implementing security testing or compliance validation

**Context Loading Pattern:**
```
As a security specialist agent, I need to conduct a comprehensive security review of this application.

REQUEST_CONTEXT(testing-security)

This provides me with:
- OWASP Top 10 testing frameworks and vulnerability detection techniques
- Security testing automation tools and methodologies
- API security testing patterns and authentication validation
- Container and infrastructure security testing approaches
```

## Multi-Role Context Loading for Complex Tasks

### 1. Full-Stack Application Review

**Scenario:** Reviewing a complete React TypeScript application with performance and security considerations

**Multi-Role Context Loading:**
```
This task requires comprehensive analysis across multiple specialist perspectives.

REQUEST_CONTEXT(react-architect, typescript-architect, react-performance, typescript-performance, testing-security)

This comprehensive context provides:
- Architectural design patterns and scalability considerations
- Implementation best practices and development patterns
- Performance optimization strategies and monitoring techniques
- Security validation frameworks and vulnerability assessment
```

### 2. Component Implementation with Testing

**Scenario:** Implementing a new React component with comprehensive testing coverage

**Multi-Role Context Loading:**
```
This implementation task requires both development and testing expertise.

REQUEST_CONTEXT(react-frontend-dev, typescript-frontend-dev, testing-frontend-dev)

This provides:
- React component implementation patterns and hooks usage
- TypeScript implementation patterns for type-safe components
- Frontend testing strategies including component, integration, and accessibility testing
```

### 3. Performance Optimization Project

**Scenario:** Optimizing a React TypeScript application for production performance

**Multi-Role Context Loading:**
```
This optimization project requires performance expertise across multiple technologies.

REQUEST_CONTEXT(react-performance, typescript-performance, testing-performance)

This provides:
- React-specific optimization techniques and profiling strategies
- TypeScript compilation optimization and runtime performance improvements
- Performance testing methodologies and continuous monitoring approaches
```

## Context Discovery Decision Tree

### Step 1: Task Analysis
```
1. What is the primary goal of this task?
   - Architecture/Design → Consider architect roles
   - Implementation/Development → Consider frontend-dev roles
   - Optimization/Performance → Consider performance roles
   - Security/Compliance → Consider security roles

2. What technologies are involved?
   - React → Include react-* contexts
   - TypeScript → Include typescript-* contexts
   - Testing → Include testing-* contexts

3. What level of expertise is required?
   - High-level strategic → architect roles
   - Implementation details → frontend-dev roles
   - Specialized analysis → performance/security roles
```

### Step 2: Role Selection Matrix
```
Task Type | Primary Role | Supporting Roles | Context Pattern
---------|-------------|------------------|----------------
New Feature Implementation | frontend-dev | architect, testing | react-frontend-dev, typescript-frontend-dev, testing-frontend-dev
Architecture Review | architect | performance, security | react-architect, typescript-architect, testing-security
Performance Audit | performance | architect | react-performance, typescript-performance, testing-performance
Security Assessment | security | architect | testing-security, react-architect, typescript-architect
Code Review | frontend-dev | performance, security | react-frontend-dev, typescript-frontend-dev, testing-security
```

### Step 3: Context Loading Implementation
```
1. Identify the most specific role needed for the primary task
2. Add supporting roles that provide complementary expertise
3. Use REQUEST_CONTEXT() with comma-separated role-technology combinations
4. Verify context loading provides comprehensive coverage for task requirements
```

## Advanced Context Loading Patterns

### 1. Adaptive Context Loading

**Pattern:** Load contexts based on file analysis and complexity detection

```
After analyzing the PR files, I've identified:
- 15 React components with complex state management → react-architect, react-frontend-dev
- TypeScript files with advanced generic patterns → typescript-architect
- Performance-critical rendering logic → react-performance
- Authentication and security concerns → testing-security

REQUEST_CONTEXT(react-architect, react-frontend-dev, typescript-architect, react-performance, testing-security)
```

### 2. Progressive Context Discovery

**Pattern:** Start with core context and expand based on findings

```
Initial analysis suggests this is a React TypeScript component implementation task.

REQUEST_CONTEXT(react-frontend-dev, typescript-frontend-dev)

After reviewing the components, I've identified performance optimization opportunities and security considerations.

REQUEST_CONTEXT(react-performance, testing-security)
```

### 3. Context Validation and Refinement

**Pattern:** Validate context relevance and adjust as needed

```
The loaded contexts provide comprehensive coverage for:
✅ React component implementation patterns (react-frontend-dev)
✅ TypeScript type safety and implementation (typescript-frontend-dev)
✅ Performance optimization strategies (react-performance)
✅ Security validation frameworks (testing-security)

All contexts are relevant and provide complementary expertise for this task.
```

## Quality Assurance for Context Loading

### 1. Context Relevance Validation

**Before using loaded context:**
- Verify the context directly applies to the current task
- Confirm the role perspective matches the required expertise level
- Ensure the technology coverage aligns with the files being analyzed

### 2. Coverage Completeness Assessment

**Ensure comprehensive coverage:**
- Are all technologies in the task covered by appropriate contexts?
- Are all required expertise levels (architecture, implementation, optimization, security) represented?
- Are there any gaps in knowledge that require additional context loading?

### 3. Context Currency Verification

**Validate knowledge currency:**
- Confirm contexts provide current best practices and patterns
- Verify compatibility with latest technology versions
- Ensure security contexts include latest threat models and compliance requirements

## Integration with Existing Systems

### 1. PR Validation System Integration

The agent self-discovery system integrates seamlessly with the AI PR Validation System:

```yaml
# PR Validation Agent Spawning with Self-Discovery
react_frontend_validation:
  agent_role: "frontend-dev"
  context_loading: "REQUEST_CONTEXT(react-frontend-dev, typescript-frontend-dev)"
  self_discovery: "Analyze PR files to determine additional context needs"
  adaptive_loading: "Load performance/security contexts based on code complexity"
```

### 2. Knowledge Vault Synchronization

The system automatically synchronizes with knowledge vault updates:

- **Automatic Context Updates**: When knowledge vault contexts are updated, agents automatically access the latest versions
- **New Context Discovery**: As new role-specific contexts are added, agents can discover and utilize them
- **Context Deprecation**: Obsolete contexts are automatically excluded from discovery patterns

### 3. Multi-Agent Coordination

When multiple agents work on the same task:

```
Agent 1 (Architect): REQUEST_CONTEXT(react-architect, typescript-architect)
Agent 2 (Frontend Dev): REQUEST_CONTEXT(react-frontend-dev, typescript-frontend-dev)  
Agent 3 (Security): REQUEST_CONTEXT(testing-security)

Coordinated analysis provides comprehensive multi-perspective validation.
```

## Best Practices for AI Agents

### 1. Proactive Context Discovery

**Always analyze before requesting:**
```
1. Read and understand the complete task requirements
2. Identify all technologies and complexity levels involved
3. Determine the most appropriate specialist role perspective
4. Request comprehensive context coverage using REQUEST_CONTEXT()
5. Validate context relevance and completeness before proceeding
```

### 2. Context Utilization Optimization

**Maximize context value:**
- Reference specific patterns and techniques from loaded contexts
- Apply role-specific expertise to provide specialist-level analysis
- Cross-reference multiple contexts for comprehensive solutions
- Maintain consistency with established patterns and best practices

### 3. Continuous Context Validation

**Throughout task execution:**
- Verify recommendations align with loaded context patterns
- Cross-check solutions against multiple specialist perspectives
- Ensure output quality matches the expertise level of loaded contexts
- Provide role-specific insights that demonstrate context utilization

## Error Handling and Fallback Strategies

### 1. Context Loading Failures

**If REQUEST_CONTEXT() fails:**
1. **Fallback to general knowledge** while noting the limitation
2. **Request alternative context combinations** that might be available
3. **Document context limitations** in the response to the user
4. **Suggest manual context specification** if automated discovery fails

### 2. Insufficient Context Coverage

**If loaded contexts don't fully cover task requirements:**
1. **Identify specific knowledge gaps** in the analysis
2. **Request additional relevant contexts** using refined REQUEST_CONTEXT() calls
3. **Combine multiple role perspectives** to achieve comprehensive coverage
4. **Acknowledge limitations** where context gaps cannot be filled

### 3. Context Conflict Resolution

**If contexts provide conflicting guidance:**
1. **Prioritize most specific and current context** for the primary task
2. **Note alternative approaches** from different role perspectives
3. **Provide balanced analysis** considering multiple specialist viewpoints
4. **Recommend consultation** with human experts for critical decisions

## Continuous Improvement

### 1. Context Effectiveness Monitoring

**Track context utilization effectiveness:**
- Monitor which context combinations provide the most valuable insights
- Identify patterns in successful multi-role context loading
- Measure task completion quality with different context strategies
- Refine context discovery patterns based on outcomes

### 2. Knowledge Vault Feedback Integration

**Contribute to knowledge vault improvement:**
- Identify gaps in existing role-specific contexts
- Suggest enhancements based on practical application experience
- Report outdated patterns or best practices that need updating
- Contribute insights from multi-role analysis perspectives

### 3. Agent Learning and Adaptation

**Improve self-discovery capabilities:**
- Learn from successful context loading patterns
- Adapt discovery strategies based on task outcomes
- Refine role selection criteria based on effectiveness
- Enhance multi-role coordination patterns

## Conclusion

The agent self-discovery system represents a revolutionary approach to AI agent knowledge management, eliminating token constraints while providing comprehensive, role-specific expertise. By following these instructions, AI agents can intelligently discover and utilize the most relevant knowledge contexts for any task, ensuring specialist-level analysis and recommendations across architecture, implementation, performance, and security domains.

This system enables AI agents to operate at expert level across multiple specialized roles while maintaining the flexibility to adapt their knowledge loading based on specific task requirements and complexity levels.