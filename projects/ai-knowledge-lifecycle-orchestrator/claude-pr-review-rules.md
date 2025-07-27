# Claude.md PR Review Rules with Current Technology Context

## AI Agent Instructions for Technology-Aware PR Reviews

Apply comprehensive PR review procedures using current technology knowledge from the AI Knowledge Lifecycle Orchestrator system to ensure all code reviews maintain currency with latest technology versions and best practices.

## Current Technology Context Integration

### Knowledge Source Priority
```yaml
technology_knowledge_sources:
  primary: "AI Knowledge Lifecycle Orchestrator dependency registry"
  secondary: "Knowledge Vault technology tracking schemas"
  fallback: "Official technology documentation and changelogs"
  validation: "AI Agent Instruction Design Excellence framework compliance"
```

### Technology Version Standards (Updated 2025-07-25)
```yaml
current_technology_versions:
  frontend_frameworks:
    React: "19.0.0"      # Latest stable with concurrent features
    Next.js: "15.0.0"    # App Router stable, Server Components production-ready
    Vue.js: "3.5.0"      # Composition API standard
    Angular: "18.0.0"    # Standalone components, signals integration

  backend_frameworks:
    Node.js: "22.6.0"    # Latest LTS with performance improvements
    Express: "4.19.0"    # Security updates and ES6+ support
    Fastify: "4.28.0"    # High-performance alternative
    NestJS: "10.3.0"     # Enterprise framework with TypeScript

  development_tools:
    TypeScript: "5.5.0"  # Latest stable with improved inference
    ESLint: "9.8.0"      # Flat config standard
    Prettier: "3.3.0"    # Stable formatting with new options
    Vite: "5.3.0"        # Build tool standard for modern apps

  testing_frameworks:
    Jest: "29.7.0"       # Stable with ES modules support
    Vitest: "2.0.0"      # Vite-native testing framework
    Testing Library: "16.0.0"  # React/Vue/Angular testing utilities
    Playwright: "1.45.0" # Cross-browser E2E testing

  styling_frameworks:
    Tailwind CSS: "3.4.0"     # Utility-first CSS with container queries
    Styled Components: "6.1.0" # CSS-in-JS for React
    Emotion: "11.11.0"        # Performance-focused CSS-in-JS

  deployment_platforms:
    Vercel: "Latest"     # Edge Functions, middleware support
    Railway: "Latest"    # Full-stack deployments
    Cloudflare Pages: "Latest"  # Static + Functions
    Docker: "27.1.0"     # Containerization standard
```

## PR Review Protocol

### Phase 1: Technology Currency Validation (≤60 seconds)

#### Technology Detection and Version Checking
```yaml
technology_detection_process:
  step_1_identify_technologies:
    action: "Scan PR files for technology imports, package.json dependencies, configuration files"
    patterns:
      - "import statements and require() calls"
      - "package.json dependencies and devDependencies"
      - "framework-specific configuration files (next.config.js, vite.config.ts, etc.)"
      - "Docker files and deployment configurations"
    
  step_2_version_validation:
    action: "Compare detected technology versions against current standards"
    validation_rules:
      - "Flag usage of deprecated versions (React 17.x, Node.js 16.x, etc.)"
      - "Identify security vulnerabilities in older versions"
      - "Check for breaking changes in proposed updates"
      - "Validate compatibility between technology combinations"
    
  step_3_dependency_consistency:
    action: "Validate against existing project dependency patterns"
    consistency_checks:
      - "Ensure new dependencies align with project technology stack"
      - "Check for conflicting versions or duplicate functionality"
      - "Validate peer dependency requirements"
      - "Assess impact on bundle size and performance"
```

#### Technology-Specific Review Rules
```yaml
react_review_rules:
  current_version: "19.0.0"
  deprecated_patterns:
    - "Class components without compelling reason (use function components + hooks)"
    - "Legacy lifecycle methods (componentWillMount, componentWillReceiveProps)"
    - "React.createElement instead of JSX syntax"
    - "PropTypes usage (prefer TypeScript interfaces)"
  
  current_best_practices:
    - "Use React.StrictMode for development builds"
    - "Implement Suspense boundaries for data fetching"
    - "Use concurrent features (startTransition, useDeferredValue) for heavy computations"
    - "Apply Server Components for Next.js 15+ applications"
    - "Use React DevTools Profiler for performance optimization"

typescript_review_rules:
  current_version: "5.5.0"
  deprecated_patterns:
    - "any type usage without specific justification"
    - "namespace declarations (use ES6 modules)"
    - "Function overloads without implementation signatures"
    - "as unknown as Type casting (use proper type guards)"
  
  current_best_practices:
    - "Use satisfies operator for type-safe object configurations"
    - "Implement branded types for domain-specific values"
    - "Apply conditional types for complex type transformations"
    - "Use template literal types for string manipulation"
    - "Leverage infer keyword for type extraction"

nextjs_review_rules:
  current_version: "15.0.0"
  deprecated_patterns:
    - "Pages Router for new applications (use App Router)"
    - "getServerSideProps/getStaticProps (use Server Components)"
    - "_app.js and _document.js (use layout.js and template.js)"
    - "next/head (use Metadata API)"
  
  current_best_practices:
    - "Use App Router with layout and template files"
    - "Implement Server Components for data fetching"
    - "Use Metadata API for SEO optimization"
    - "Apply streaming with loading.js and error.js"
    - "Implement edge middleware for authentication and redirects"

testing_review_rules:
  current_frameworks: ["Jest 29.7.0", "Vitest 2.0.0", "Testing Library 16.0.0"]
  deprecated_patterns:
    - "Enzyme testing (migrate to Testing Library)"
    - "Manual DOM manipulation in tests"
    - "Testing implementation details instead of behavior"
    - "Synchronous act() calls (use async act)"
  
  current_best_practices:
    - "Use Testing Library queries (getByRole, getByLabelText)"
    - "Test user interactions with userEvent library"
    - "Implement accessibility testing with jest-axe"
    - "Use MSW (Mock Service Worker) for API mocking"
    - "Apply test-driven development patterns"
```

### Phase 2: Security and Best Practices Assessment (≤90 seconds)

#### Security Pattern Analysis
```yaml
security_assessment:
  current_vulnerabilities_check:
    action: "Validate against known security issues in current technology versions"
    checks:
      - "npm audit for dependency vulnerabilities"
      - "Known CVEs in detected technology versions"
      - "Insecure coding patterns (SQL injection, XSS, CSRF)"
      - "Exposed secrets or credentials in code"
  
  secure_coding_practices:
    authentication: 
      - "Use established libraries (NextAuth.js, Passport.js)"
      - "Implement proper session management"
      - "Apply rate limiting and brute force protection"
      - "Use secure cookie configurations"
    
    data_validation:
      - "Input validation and sanitization"
      - "Output encoding and escaping"
      - "Parameter validation with TypeScript"
      - "Schema validation (Zod, Joi, Yup)"
    
    api_security:
      - "CORS configuration review"
      - "HTTPS enforcement"
      - "API rate limiting implementation"
      - "Proper error handling without information disclosure"
```

#### Performance and Optimization
```yaml
performance_assessment:
  current_optimization_techniques:
    react_performance:
      - "React.memo for expensive component renders"
      - "useMemo and useCallback for expensive computations"
      - "Code splitting with React.lazy and Suspense"
      - "Bundle analysis and tree shaking optimization"
    
    nextjs_performance:
      - "Image optimization with next/image"
      - "Font optimization with next/font"
      - "Dynamic imports for code splitting"
      - "Static generation optimization"
    
    general_performance:
      - "Lazy loading implementation"
      - "Caching strategies (browser, CDN, API)"
      - "Database query optimization"
      - "Asset compression and minification"
```

### Phase 3: Code Quality and Consistency (≤120 seconds)

#### Code Quality Standards
```yaml
code_quality_validation:
  typescript_quality:
    strict_typing:
      - "Enable strict mode in TypeScript configuration"
      - "Proper return type annotations for functions"
      - "Interface definitions for complex objects"
      - "Generic constraints and conditional types"
    
    error_handling:
      - "Proper error boundary implementation"
      - "Result type patterns for error handling"
      - "Async error handling with try-catch"
      - "Type-safe error messages"
  
  react_quality:
    component_design:
      - "Single responsibility principle for components"
      - "Proper prop drilling vs context usage"
      - "Component composition over inheritance"
      - "Custom hooks for stateful logic"
    
    accessibility:
      - "Semantic HTML elements usage"
      - "ARIA attributes for complex interactions"
      - "Keyboard navigation support"
      - "Screen reader compatibility"
```

#### Architecture and Patterns
```yaml
architecture_validation:
  project_structure:
    consistency_checks:
      - "File naming conventions (camelCase, kebab-case, PascalCase)"
      - "Directory structure patterns"
      - "Import path consistency"
      - "Component organization standards"
  
  design_patterns:
    recommended_patterns:
      - "Container/Presentational component pattern"
      - "Custom hooks for business logic"
      - "Provider pattern for state management"
      - "Repository pattern for data access"
    
    anti_patterns:
      - "Massive components with multiple responsibilities"
      - "Prop drilling beyond 2-3 levels"
      - "Direct DOM manipulation in React"
      - "Global state for local component state"
```

## AI Agent Review Execution

### Review Checklist Template
```yaml
pr_review_template:
  technology_currency:
    - [ ] "All technology versions current (React 19+, TypeScript 5.5+, Next.js 15+)"
    - [ ] "No deprecated patterns or legacy code introduced"
    - [ ] "Dependencies consistent with project technology stack"
    - [ ] "Breaking changes properly handled"
  
  security_compliance:
    - [ ] "No security vulnerabilities in dependencies"
    - [ ] "Secure coding practices applied"
    - [ ] "Input validation and output encoding implemented"
    - [ ] "Authentication and authorization properly configured"
  
  code_quality:
    - [ ] "TypeScript strict mode compliance"
    - [ ] "React best practices (hooks, components, performance)"
    - [ ] "Testing coverage for new functionality"
    - [ ] "Accessibility standards met"
  
  performance_optimization:
    - [ ] "Bundle size impact assessed"
    - [ ] "Performance optimizations applied"
    - [ ] "Code splitting implemented where appropriate"
    - [ ] "Caching strategies considered"
  
  architecture_consistency:
    - [ ] "Follows project architectural patterns"
    - [ ] "Component design principles applied"
    - [ ] "File organization and naming consistent"
    - [ ] "Import/export patterns standardized"
```

### Review Comment Templates

#### Technology Update Recommendations
```markdown
## 🔄 Technology Update Recommendation

**Issue**: Using outdated React version (18.x) in new components
**Current Standard**: React 19.0.0 with concurrent features
**Impact**: Missing performance improvements and new capabilities

**Recommendation**:
```typescript
// ❌ Outdated pattern
import { useEffect, useState } from 'react';

// ✅ Current best practice
import { useTransition, useDeferredValue } from 'react';
const [isPending, startTransition] = useTransition();
```

**Action Required**: Update to React 19+ and implement concurrent features for improved UX

**Resources**: 
- [React 19 Migration Guide](https://react.dev/blog/2024/04/25/react-19)
- [Concurrent Features Documentation](https://react.dev/reference/react/useTransition)
```

#### Security Vulnerability Alert
```markdown
## 🔒 Security Vulnerability Detected

**Severity**: High
**Component**: Package dependency with known CVE
**Issue**: Using vulnerable version of [package] that has known security issues

**Current Version**: X.X.X (vulnerable)
**Recommended Version**: Y.Y.Y+ (patched)

**Vulnerability Details**:
- CVE-YYYY-XXXXX: [Brief description]
- Attack Vector: [How it can be exploited]
- Impact: [What damage could occur]

**Required Action**: 
1. Update package to secure version: `npm install package@^Y.Y.Y`
2. Test functionality after update
3. Review code for any breaking changes

**Verification**: Run `npm audit` to confirm resolution
```

#### Code Quality Improvement
```markdown
## 📈 Code Quality Enhancement

**Pattern**: Opportunity for better TypeScript usage and React optimization

**Current Implementation**:
```typescript
// ❌ Can be improved
function Component({ data }: { data: any }) {
  const [state, setState] = useState();
  // ... component logic
}
```

**Recommended Improvement**:
```typescript
// ✅ Type-safe and optimized
interface ComponentProps {
  data: UserData[];
}

const Component = memo<ComponentProps>(({ data }) => {
  const memoizedValue = useMemo(() => {
    return expensiveComputation(data);
  }, [data]);
  
  // ... component logic
});
```

**Benefits**:
- Type safety with proper interfaces
- Performance optimization with memo and useMemo
- Better maintainability and debugging
```

## Integration with AI Knowledge Lifecycle Orchestrator

### Automated Knowledge Updates
```yaml
knowledge_integration:
  dependency_registry_access:
    action: "Query current project technology dependencies"
    source: "projects/ai-knowledge-lifecycle-orchestrator/dependency-registry/registry.yaml"
    usage: "Validate PR changes against existing project patterns"
  
  technology_tracking_access:
    action: "Get current technology versions and change notifications"
    source: "knowledge-vault/databases/technology_tracking/"
    usage: "Ensure PR reviews use most current technology information"
  
  change_detection_integration:
    action: "Reference recent technology changes and their impact"
    source: "knowledge-vault/databases/change_events/"
    usage: "Provide context-aware recommendations based on recent updates"
```

### Review Quality Metrics
```yaml
review_effectiveness:
  technology_currency_score:
    calculation: "percentage_of_current_technologies / total_technologies_used"
    target: ">95% current technology usage"
  
  security_compliance_score:
    calculation: "secure_patterns_applied / total_security_checkpoints"
    target: ">90% security best practices compliance"
  
  code_quality_score:
    calculation: "quality_patterns_followed / total_quality_checkpoints"
    target: ">85% code quality standards met"
  
  performance_optimization_score:
    calculation: "optimizations_applied / optimization_opportunities"
    target: ">80% performance improvements implemented"
```

## AI Agent Operational Procedures

### Pre-Review Setup
1. **Load Current Technology Context**: Access AI Knowledge Lifecycle Orchestrator for latest technology versions
2. **Query Project Dependencies**: Review existing project technology stack and patterns
3. **Check Recent Changes**: Review any recent technology updates that might affect the PR
4. **Initialize Review Checklist**: Prepare technology-specific review criteria

### During Review Execution
1. **Apply Phase-by-Phase Review**: Follow 3-phase review protocol with time constraints
2. **Generate Contextual Comments**: Use current technology knowledge for specific recommendations
3. **Validate Against Standards**: Ensure all recommendations align with current best practices
4. **Document Review Decisions**: Log review rationale for audit and improvement

### Post-Review Actions
1. **Update Review Metrics**: Track review effectiveness and technology currency scores
2. **Submit Actionable Feedback**: Provide clear, implementable recommendations
3. **Schedule Follow-up**: Set expectations for PR author responses and iterations
4. **Learn from Outcomes**: Update review procedures based on PR resolution success

## Quality Assurance and Continuous Improvement

### Review Quality Standards
- **Technology Currency**: All recommendations must reference current stable versions
- **Security Awareness**: All security recommendations must be current and actionable
- **Performance Focus**: All optimization suggestions must be measurable and relevant
- **Accessibility Compliance**: All UI changes must meet current accessibility standards

### Continuous Learning Integration
- **Knowledge Updates**: Automatically incorporate new technology releases and best practices
- **Pattern Recognition**: Learn from successful PR patterns and apply to future reviews
- **Feedback Integration**: Incorporate developer feedback to improve review quality
- **Metric Analysis**: Use review metrics to identify improvement opportunities

This comprehensive PR review system ensures all code reviews maintain currency with the latest technology standards while providing actionable, context-aware feedback that improves code quality, security, and performance.