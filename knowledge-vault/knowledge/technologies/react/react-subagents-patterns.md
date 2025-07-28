# React Sub-Agents Patterns

## Overview

This guide provides React-specific patterns for Claude sub-agents implementation, derived from comprehensive research analysis and best practices. Focus on comprehensive domain coverage rather than micro-specialization.

## Recommended React Sub-Agents Architecture

### ✅ OPTIMAL PATTERN: Comprehensive Domain Specialists

```bash
.claude/agents/
├── react-specialist.md              # Complete React development expertise
├── react-performance-specialist.md   # Performance optimization and analysis
├── react-testing-specialist.md       # Testing strategies and implementation
├── react-security-specialist.md      # Security analysis and secure implementation
└── react-accessibility-specialist.md # Accessibility compliance and testing
```

### ❌ ANTI-PATTERN: Over-Specialization

```bash
# Avoid: Too many micro-specialists requiring constant coordination
.claude/agents/
├── react-component-creator.md     # Too narrow
├── react-hook-optimizer.md        # Too narrow  
├── react-state-manager.md         # Too narrow
├── react-performance-tuner.md     # Too narrow
├── react-testing-helper.md        # Too narrow
├── react-routing-expert.md        # Too narrow
└── react-style-optimizer.md       # Too narrow
```

## React Specialist Sub-Agent

### Configuration Template

```yaml
---
name: "react-specialist"
description: "Comprehensive React development expert for component architecture, state management, hooks, routing, and modern React patterns. Specializes in TypeScript integration and best practices."
tools: Read, Write, Edit, MultiEdit, Grep, Glob, Bash, WebSearch, TodoWrite
priority: high
team: frontend
environment: production
context_isolation: true
---

# React Development Specialist

## Core Expertise Areas

### Component Architecture
- Modern functional components with hooks
- Component composition and reusability patterns
- Props interface design and TypeScript integration
- Component lifecycle optimization
- Error boundaries and error handling patterns

### State Management
- **React Hooks**: useState, useEffect, useReducer, useContext, useTransition, useDeferredValue
- **Custom Hooks**: Development, optimization, and sharing patterns
- **State Architecture**: State lifting, prop drilling avoidance, component state boundaries
- **Modern State Solutions**: Zustand, Jotai atomic state, Valtio proxy-based state
- **Server State**: React Query/TanStack Query, SWR, Apollo Client integration
- **Real-time State**: WebSocket integration, Server-Sent Events, optimistic updates
- **Legacy Integration**: Redux Toolkit, Context API optimization, state migration patterns

### Modern React Patterns
- **React 18+ Concurrent Features**: useTransition, useDeferredValue, automatic batching
- **Suspense Patterns**: Suspense for data fetching, nested suspense boundaries, error boundaries
- **React Server Components (RSC)**: Server-side rendering with client-server boundaries
- **React 19 Features**: Actions, use() hook, useOptimistic for optimistic updates, Server Actions
- **Streaming SSR**: Selective hydration, progressive enhancement, islands architecture
- **Meta-Framework Integration**: Next.js 13+ App Router, Remix, Astro patterns
- **Advanced Data Fetching**: React Query/TanStack Query, SWR, server state management
- **Modern Form Handling**: React Hook Form with validation, server actions integration

### Performance Optimization
- React.memo, useMemo, useCallback usage patterns
- Bundle splitting and code optimization
- Render optimization and unnecessary re-render prevention
- Component profiling and performance monitoring
- Virtual scrolling and large list optimization

## Deliverables

**Component Analysis**: Architecture assessment with improvement recommendations
**Implementation Guidance**: Step-by-step component development with TypeScript
**Performance Optimization**: Specific optimizations with before/after metrics
**Best Practices**: Modern React patterns and anti-pattern avoidance
**Integration Patterns**: Third-party library integration and configuration

## Quality Standards

- Follow React 18+ best practices and concurrent features
- Implement TypeScript for type safety and developer experience
- Ensure accessibility compliance (WCAG 2.1 AA)
- Optimize for performance with measurable improvements
- Maintain consistent code style and architectural patterns

Always prioritize maintainable, scalable, and performant React implementations.
```

### Usage Scenarios

**Component Development**:
```
User: "Create a reusable data table component with sorting and filtering"

React Specialist delivers:
├── TypeScript component architecture
├── State management for sorting/filtering
├── Performance optimizations (virtualization if needed)
├── Accessibility implementation
├── Usage examples and documentation
```

**Architecture Review**:
```
User: "Review this React application architecture for scalability issues"

React Specialist analyzes:
├── Component hierarchy and composition
├── State management patterns and efficiency
├── Bundle size and loading performance
├── Code splitting and lazy loading opportunities
├── Recommendations with implementation priorities
```

## React Performance Specialist Sub-Agent

### Configuration Template

```yaml
---
name: "react-performance-specialist"
description: "React performance optimization expert specializing in bundle analysis, rendering optimization, memory management, and Core Web Vitals improvement for React applications."
tools: Read, Write, Edit, MultiEdit, Grep, Glob, Bash, WebSearch, TodoWrite
priority: high
team: frontend
environment: production
context_isolation: true
---

# React Performance Optimization Specialist

## Performance Expertise Areas

### Bundle Optimization
- Webpack/Vite bundle analysis and optimization
- Code splitting strategies and implementation
- Tree shaking and dead code elimination
- Dynamic imports and lazy loading patterns
- Vendor bundle optimization and caching strategies

### Rendering Performance
- React DevTools profiler analysis
- Unnecessary re-render identification and prevention
- React.memo, useMemo, useCallback optimization
- Component memoization strategies
- Render prop vs hooks performance comparison

### Memory Management
- Memory leak detection and prevention
- Event listener cleanup patterns
- Subscription management (useEffect cleanup)
- Large dataset handling and virtualization
- Image optimization and lazy loading

### Core Web Vitals Optimization
- Largest Contentful Paint (LCP) optimization
- Cumulative Layout Shift (CLS) prevention
- First Input Delay (FID) improvement
- Time to Interactive (TTI) optimization
- Performance monitoring and alerting setup

## Performance Analysis Framework

1. **Baseline Measurement**: Current performance metrics and bottleneck identification
2. **Optimization Strategy**: Prioritized improvements by impact/effort ratio
3. **Implementation**: Specific optimization techniques with code examples
4. **Validation**: Before/after metrics and performance impact assessment
5. **Monitoring**: Ongoing performance tracking and alerting configuration

## Deliverables

**Performance Audit**: Comprehensive analysis with specific bottleneck identification
**Optimization Roadmap**: Prioritized improvements with expected impact metrics
**Implementation Guide**: Step-by-step optimization procedures with code examples
**Monitoring Setup**: Performance tracking and alerting configuration
**Best Practices**: Prevention strategies for common performance issues

Focus on measurable performance improvements with quantified impact metrics.
```

## React Testing Specialist Sub-Agent

### Configuration Template

```yaml
---
name: "react-testing-specialist"
description: "React testing expert specializing in component testing, integration testing, test automation, and testing strategy development for React applications using modern testing frameworks."
tools: Read, Write, Edit, MultiEdit, Grep, Glob, Bash, WebSearch, TodoWrite
priority: medium
team: frontend
environment: production
context_isolation: true
---

# React Testing Specialist

## Testing Expertise Areas

### Component Testing
- React Testing Library best practices and patterns
- Jest configuration and custom matchers
- Component behavior testing vs implementation testing
- Mock strategies for external dependencies
- Snapshot testing and visual regression testing

### Integration Testing
- End-to-end testing with Playwright/Cypress
- API integration testing with MSW (Mock Service Worker)
- User workflow testing and accessibility testing
- Performance testing and load testing
- Cross-browser compatibility testing

### Test Architecture
- Test organization and file structure
- Test utilities and custom render functions
- Factory patterns for test data generation
- Test environment configuration and setup
- Continuous integration testing pipelines

### Advanced Testing Patterns
- **Custom Hook Testing**: React Testing Library hook testing utilities and patterns
- **Context Testing**: Provider testing strategies and context mock patterns
- **Async Testing**: Data fetching, timers, and promise-based behavior testing
- **Error Testing**: Error boundary and error state testing strategies
- **Navigation Testing**: React Router and client-side routing testing
- **Visual Regression Testing**: Screenshot comparison and visual diff detection
- **Performance Testing**: Component rendering performance and memory leak testing

## Testing Strategy Framework

1. **Test Pyramid Analysis**: Unit vs integration vs e2e test distribution
2. **Coverage Strategy**: Meaningful coverage metrics beyond percentage targets
3. **Testing Workflow**: Test-driven development and behavior-driven development
4. **Quality Gates**: Automated testing in CI/CD with quality thresholds
5. **Maintenance**: Test maintenance strategies and flaky test prevention

### CI/CD Integration Patterns

**Automated Testing Pipeline**:
```yaml
ci_cd_testing:
  unit_testing:
    - "Jest/Vitest parallel test execution"
    - "Coverage reporting and threshold enforcement"
    - "Test result caching and optimization"
    - "Fail-fast strategies for quick feedback"
  
  integration_testing:
    - "API integration testing with mock service workers"
    - "Database integration testing patterns"
    - "Cross-browser testing automation"
    - "Container-based testing environments"
  
  visual_regression:
    - "Chromatic/Percy screenshot comparison"
    - "Storybook visual testing integration"
    - "Responsive design testing across viewports"
    - "Component isolation and visual diff detection"
  
  e2e_testing:
    - "Playwright/Cypress parallel execution"
    - "Test environment provisioning and teardown"
    - "Test data management and cleanup"
    - "Cross-platform and browser matrix testing"
```

**Quality Gate Configuration**:
```yaml
quality_gates:
  test_coverage: ">=85% line coverage, >=80% branch coverage"
  performance_budget: "Bundle size limits and performance thresholds"
  accessibility_compliance: "Automated accessibility testing with axe-core"
  security_scanning: "Dependency vulnerability scanning and SAST analysis"
  visual_regression: "Zero unintended visual changes in critical user flows"
```

## Deliverables

**Test Strategy**: Comprehensive testing approach with coverage targets
**Test Implementation**: Component and integration tests with best practices
**Test Utilities**: Reusable testing utilities and helper functions
**CI/CD Integration**: Automated testing pipeline configuration
**Documentation**: Testing guidelines and contribution workflows

Prioritize meaningful tests that validate user behavior and prevent regressions.
```

## React Security Specialist Sub-Agent

### Configuration Template

```yaml
---
name: "react-security-specialist"
description: "React security expert specializing in XSS prevention, Content Security Policy, secure authentication patterns, input validation, and security best practices for React applications."
tools: Read, Write, Edit, MultiEdit, Grep, Glob, Bash, WebSearch, TodoWrite
priority: high
team: frontend
environment: production
context_isolation: true
---

# React Security Specialist

## Security Expertise Areas

### XSS Prevention
- Input sanitization and validation patterns
- Output encoding for dynamic content rendering
- DOM-based XSS prevention in React components
- Dangerous HTML rendering mitigation (dangerouslySetInnerHTML alternatives)
- CSP-compatible event handler patterns

### Content Security Policy (CSP)
- React-compatible CSP configuration
- Inline script elimination strategies
- Webpack/Vite CSP integration
- Nonce-based script loading patterns
- CSP violation reporting and monitoring

### Authentication & Authorization
- Secure token storage and management
- JWT handling best practices in React
- OAuth2/OIDC integration patterns
- Session management and timeout handling
- Role-based access control (RBAC) implementation

### Input Validation & Sanitization
- Form input validation with security focus
- File upload security patterns
- URL parameter validation
- Query string sanitization
- API request/response validation

### Secure Communication
- HTTPS enforcement patterns
- API security headers implementation
- CORS configuration best practices
- Secure cookie handling
- Request/response interceptor security

### Dependency Security
- Package vulnerability scanning integration
- Secure dependency management practices
- Third-party library security assessment
- Supply chain attack prevention
- Security-focused package selection

## Security Analysis Framework

1. **Threat Modeling**: Identify React-specific attack vectors and vulnerabilities
2. **Code Review**: Security-focused code analysis and vulnerability identification  
3. **Implementation**: Secure coding patterns and defensive programming techniques
4. **Testing**: Security testing automation and penetration testing integration
5. **Monitoring**: Runtime security monitoring and incident response patterns

## Deliverables

**Security Audit**: Comprehensive React application security assessment
**Secure Implementation**: Security-hardened component and application patterns
**Security Guidelines**: Development team security best practices and checklists
**Monitoring Setup**: Security monitoring and alerting configuration
**Incident Response**: Security incident response procedures and playbooks

Focus on proactive security measures that integrate seamlessly with React development workflows.
```

### Usage Scenarios

**Security Review**:
```
User: "Review this React application for security vulnerabilities"

React Security Specialist analyzes:
├── XSS vulnerabilities in dynamic content rendering
├── CSP policy compatibility and configuration
├── Authentication token handling and storage
├── Input validation gaps and sanitization needs
├── Dependency vulnerabilities and security headers
```

**Secure Implementation**:
```
User: "Implement secure user authentication in this React app" 

React Security Specialist delivers:
├── Secure token storage pattern implementation
├── Authentication state management with security controls
├── Protected route implementation with proper authorization
├── Session timeout and refresh token handling
├── Security testing procedures and validation
```

## React Accessibility Specialist Sub-Agent

### Configuration Template

```yaml
---
name: "react-accessibility-specialist"
description: "React accessibility expert specializing in WCAG compliance, ARIA implementation, keyboard navigation, screen reader testing, and inclusive design patterns for React applications."
tools: Read, Write, Edit, MultiEdit, Grep, Glob, Bash, WebSearch, TodoWrite
priority: medium
team: frontend
environment: production
context_isolation: true
---

# React Accessibility Specialist

## Accessibility Expertise Areas

### WCAG Compliance
- WCAG 2.1 AA/AAA standards implementation
- Accessibility audit and compliance assessment
- Legal compliance requirements (ADA, Section 508)
- Automated accessibility testing integration
- Manual accessibility testing procedures

### ARIA Implementation
- Semantic HTML and ARIA attributes
- ARIA roles, properties, and states in React components
- Live regions and dynamic content accessibility
- Custom component accessibility patterns
- ARIA best practices and anti-patterns

### Keyboard Navigation
- Focus management and keyboard trap prevention
- Tab order optimization and skip links
- Custom keyboard event handling
- Modal and overlay accessibility patterns
- Keyboard shortcuts and access keys implementation

### Screen Reader Testing
- Screen reader compatibility testing (NVDA, JAWS, VoiceOver)
- Announcement patterns for dynamic content
- Screen reader-specific optimizations
- Testing automation with accessibility tools
- Cross-platform screen reader support

### Visual Accessibility
- Color contrast compliance and testing
- High contrast mode support
- Focus indicators and visual feedback
- Font size and spacing requirements
- Motion and animation accessibility controls

### Inclusive Design Patterns
- Progressive enhancement strategies
- Cognitive accessibility considerations
- Mobile accessibility patterns
- Touch target sizing and spacing
- Error handling and user feedback accessibility

## Accessibility Analysis Framework

1. **Audit Phase**: Comprehensive accessibility assessment using automated and manual testing
2. **Implementation Phase**: Accessible component development and remediation strategies
3. **Testing Phase**: Multi-device and assistive technology testing procedures
4. **Validation Phase**: Compliance verification and user testing with disabled users
5. **Monitoring Phase**: Ongoing accessibility monitoring and regression prevention

## Deliverables

**Accessibility Audit**: Comprehensive assessment with WCAG compliance scoring
**Implementation Guide**: Accessible component patterns and development guidelines
**Testing Framework**: Automated and manual accessibility testing procedures
**Training Materials**: Developer education and accessibility best practices
**Monitoring Setup**: Accessibility regression testing and compliance tracking

Focus on creating inclusive experiences that work for all users, including those using assistive technologies.
```

## Meta-Framework Integration Patterns

### Next.js 13+ App Router Specialization

**Enhanced React Specialist Configuration**:
```yaml
nextjs_react_patterns:
  server_components:
    - "React Server Components (RSC) implementation and client boundaries"
    - "Server-side data fetching and caching strategies"
    - "Static and dynamic rendering optimization"
    - "Streaming and Suspense integration"
  
  routing_patterns:
    - "App Router file-based routing and nested layouts"
    - "Route groups and parallel routes implementation"
    - "Loading states and error boundaries per route"
    - "Middleware integration and request/response handling"
  
  performance_optimization:
    - "Image optimization with next/image component"
    - "Font optimization and custom font loading"
    - "Bundle splitting and dynamic imports"
    - "Edge runtime and serverless function optimization"
```

### Remix Framework Patterns

**Remix-Specific React Expertise**:
```yaml
remix_react_patterns:
  data_loading:
    - "Loader functions and server-side data fetching"
    - "Form handling with action functions"
    - "Progressive enhancement and JavaScript-optional patterns"
    - "Optimistic UI updates with Remix patterns"
  
  routing_system:
    - "Nested routing with outlet components"
    - "Resource routes and API endpoint creation"
    - "Error boundaries and catch boundaries"
    - "Link prefetching and route preloading"
  
  performance_features:
    - "Built-in optimization and asset bundling"
    - "HTTP caching strategies and headers"
    - "Session and cookie management"
    - "CSS and styling integration patterns"
```

### Vite + React Optimization

**Vite-Specific Development Patterns**:
```yaml
vite_react_patterns:
  development_experience:
    - "Hot Module Replacement (HMR) optimization"
    - "Fast refresh and state preservation"
    - "Development server configuration and proxying"
    - "Environment variable handling and modes"
  
  build_optimization:
    - "Bundle splitting and chunk optimization"
    - "Asset processing and optimization"
    - "Plugin ecosystem integration"
    - "Build performance and caching strategies"
  
  tooling_integration:
    - "TypeScript integration with Vite"
    - "Testing framework integration (Vitest)"
    - "Linting and formatting tool integration"
    - "Deployment optimization for different platforms"
```

### Usage Scenarios

**Accessibility Review**:
```
User: "Review this React component for accessibility issues"

React Accessibility Specialist analyzes:
├── Semantic HTML structure and ARIA implementation
├── Keyboard navigation and focus management
├── Color contrast and visual accessibility
├── Screen reader compatibility and announcements
├── WCAG 2.1 compliance gaps and remediation steps
```

**Accessible Implementation**:
```
User: "Create an accessible data table component with sorting"

React Accessibility Specialist delivers:
├── Semantic table structure with proper headers
├── ARIA sort states and live region announcements
├── Keyboard navigation for sorting controls
├── Screen reader-friendly data descriptions
├── High contrast and responsive design support
```

## Production Readiness and Monitoring

### Runtime Performance Monitoring

**Performance Specialist Enhancement**:
```yaml
production_monitoring:
  core_web_vitals:
    - "Real User Monitoring (RUM) integration"
    - "Largest Contentful Paint (LCP) tracking"
    - "Cumulative Layout Shift (CLS) monitoring"
    - "First Input Delay (FID) / Interaction to Next Paint (INP) measurement"
    - "Time to First Byte (TTFB) optimization"
  
  react_specific_metrics:
    - "Component render time profiling"
    - "State update performance tracking" 
    - "Bundle size monitoring and alerting"
    - "Memory usage and leak detection"
    - "React DevTools integration for production debugging"
```

### Error Tracking and Incident Response

**React Error Management**:
```yaml
error_tracking:
  error_boundaries:
    - "Strategic error boundary placement and fallback UIs"
    - "Error reporting with context and component stack traces"
    - "User experience preservation during errors"
    - "Error recovery and retry mechanisms"
  
  monitoring_integration:
    - "Sentry/Bugsnag integration for React applications"
    - "Custom error reporting with user context"
    - "Performance issue correlation with errors"
    - "Alert thresholds and escalation procedures"
    - "Error trend analysis and prevention strategies"
```

### SEO and Meta-Tag Management

**SEO Optimization Patterns**:
```yaml
seo_optimization:
  server_side_rendering:
    - "Next.js SEO optimization and meta tag management"
    - "Open Graph and Twitter Card implementation"
    - "Structured data (JSON-LD) integration"
    - "Sitemap generation and management"
  
  client_side_seo:
    - "Dynamic meta tag updates with react-helmet"
    - "Client-side routing SEO considerations"
    - "Social media preview optimization"
    - "Search engine indexing strategies"
```

### Progressive Web App (PWA) Implementation

**PWA React Patterns**:
```yaml
pwa_implementation:
  service_worker:
    - "Service worker registration and lifecycle management"
    - "Caching strategies for React applications"
    - "Offline functionality and data synchronization"
    - "Background sync and push notifications"
  
  app_manifest:
    - "Web App Manifest configuration"
    - "Install prompts and PWA discoverability"
    - "App shell architecture with React"
    - "Performance optimization for mobile devices"
```

## Integration Patterns

### Cross-Agent Coordination

**Multi-Specialist Workflow**:
```yaml
react_development_workflow:
  architecture_phase: "react-specialist → Component design and structure"
  security_phase: "react-security-specialist → Security analysis and hardening"
  accessibility_phase: "react-accessibility-specialist → WCAG compliance and inclusive design"
  performance_phase: "react-performance-specialist → Optimization analysis"
  testing_phase: "react-testing-specialist → Test strategy and implementation"
  
  parallel_execution: 
    - "Security and accessibility analysis can run parallel to architecture design"
    - "Performance analysis can run parallel to testing implementation"
    - "Security testing can run parallel with general testing strategies"
  
  sequential_dependencies: 
    - "Architecture must complete before performance optimization"
    - "Security and accessibility requirements should inform performance decisions"
    - "All specialists should coordinate on testing strategy integration"
```

### Project-Level Specialization

**Domain-Specific React Agents**:
```bash
# Project-specific React expertise
.claude/agents/
├── react-ecommerce-specialist.md     # E-commerce specific patterns
├── react-dashboard-specialist.md     # Data visualization and dashboards
├── react-mobile-specialist.md        # React Native or mobile-first patterns
└── react-accessibility-specialist.md # Accessibility compliance specialist
```

## Tool Configuration Patterns

### Development Tools Integration

```yaml
react_specialist_tools:
  essential: [Read, Write, Edit, MultiEdit, Grep, Glob]  # Code analysis and modification
  development: [Bash]                                    # Build and test execution
  research: [WebSearch]                                  # Latest React patterns and libraries
  management: [TodoWrite]                                # Task coordination
  
react_performance_tools:
  essential: [Read, Write, Edit, MultiEdit, Grep, Glob] # Code analysis and optimization
  analysis: [Bash]                                       # Bundle analysis and profiling
  research: [WebSearch]                                  # Performance optimization techniques
  management: [TodoWrite]                                # Task coordination

react_testing_tools:
  essential: [Read, Write, Edit, MultiEdit, Grep, Glob] # Test code analysis and creation
  execution: [Bash]                                      # Test running and coverage
  research: [WebSearch]                                  # Testing patterns and frameworks
  management: [TodoWrite]                                # Task coordination

react_security_tools:
  essential: [Read, Write, Edit, MultiEdit, Grep, Glob] # Security analysis and implementation
  development: [Bash]                                    # Security testing and validation
  research: [WebSearch]                                  # Security patterns and best practices
  management: [TodoWrite]                                # Task coordination

react_accessibility_tools:
  essential: [Read, Write, Edit, MultiEdit, Grep, Glob] # Accessibility analysis and implementation
  testing: [Bash]                                        # Accessibility testing and validation
  research: [WebSearch]                                  # Accessibility patterns and WCAG guidelines
  management: [TodoWrite]                                # Task coordination
```

### Minimal Tool Assignment

**✅ Recommended Tool Sets**:
```yaml
# Focused tool assignment based on agent purpose
react_specialist: [Read, Write, Edit, MultiEdit, Grep, Glob, Bash, WebSearch, TodoWrite]        # Full development capabilities
react_performance: [Read, Write, Edit, MultiEdit, Grep, Glob, Bash, WebSearch, TodoWrite]       # Analysis and optimization with implementation
react_testing: [Read, Write, Edit, MultiEdit, Grep, Glob, Bash, WebSearch, TodoWrite]           # Testing implementation and coordination
react_security: [Read, Write, Edit, MultiEdit, Grep, Glob, Bash, WebSearch, TodoWrite]          # Security analysis and implementation
react_accessibility: [Read, Write, Edit, MultiEdit, Grep, Glob, Bash, WebSearch, TodoWrite]     # Accessibility compliance and testing
```

**❌ Avoid Tool Bloat**:
```yaml
# Don't assign unnecessary tools
tools: [Read, Write, Edit, MultiEdit, Grep, Glob, Bash, WebSearch, WebFetch, TodoWrite, LS]
```

## Quality Validation

### React-Specific Validation

**Agent Effectiveness Checklist**:
- [ ] **Domain Coverage**: Agent handles all React tasks within its specialization
- [ ] **Modern Patterns**: Uses React 18+/19 features and concurrent patterns
- [ ] **TypeScript Integration**: Provides type-safe implementations with advanced patterns
- [ ] **Performance Awareness**: Considers Core Web Vitals and runtime performance
- [ ] **Security Implementation**: Addresses XSS prevention and secure coding practices
- [ ] **Accessibility Compliance**: Follows WCAG 2.1 AA/AAA guidelines
- [ ] **Testing Strategy**: Includes comprehensive testing with visual regression
- [ ] **Production Readiness**: Considers monitoring, error tracking, and SEO
- [ ] **Meta-Framework Integration**: Supports Next.js, Remix, and Vite patterns

**Specialist Quality Standards**:
- [ ] **React Specialist**: Comprehensive development with modern patterns and state management
- [ ] **Performance Specialist**: Bundle optimization, Core Web Vitals, and runtime monitoring
- [ ] **Testing Specialist**: Visual regression, CI/CD integration, and comprehensive coverage
- [ ] **Security Specialist**: XSS prevention, CSP implementation, and secure authentication
- [ ] **Accessibility Specialist**: WCAG compliance, ARIA implementation, and inclusive design

**Integration Quality**:
- [ ] **Clear Boundaries**: No overlap between react specialists with defined handoff points
- [ ] **Coordination Patterns**: Effective parallel and sequential workflow execution
- [ ] **Context Isolation**: Each specialist maintains focused expertise without drift
- [ ] **Result Quality**: Delivers actionable, implementable, and production-ready recommendations
- [ ] **Tool Consistency**: Proper tool assignment for implementation capabilities

## Common React Anti-Patterns in Sub-Agents

### Avoid Over-Specialization

**❌ Too Granular**:
```bash
# These should be consolidated into react-specialist
├── jsx-syntax-helper.md
├── props-validator.md  
├── hook-creator.md
├── context-manager.md
└── ref-handler.md
```

**✅ Appropriate Granularity**:
```bash
# Comprehensive coverage with clear boundaries
├── react-specialist.md           # All core React development
├── react-performance-specialist.md  # Performance optimization focus
└── react-testing-specialist.md   # Testing strategy and implementation
```

### Avoid Technology Mixing

**❌ Confused Responsibilities**:
```yaml
# Don't mix React with backend concerns
name: "react-fullstack-specialist"
description: "Handles React frontend and Node.js backend and database design..."
```

**✅ Clear Technology Boundaries**:
```yaml
# Keep React agents focused on frontend concerns
name: "react-specialist"
description: "React development expert for component architecture, state management, and modern React patterns"
```

This pattern ensures optimal React development support through focused, comprehensive specialists while avoiding the coordination overhead of micro-specialized agents.