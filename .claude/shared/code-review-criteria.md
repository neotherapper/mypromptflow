# Code Review Criteria - Shared Instructions

**Purpose**: Comprehensive code review standards for consistent quality assessment across AI agents and subagents.

**Usage**: Referenced by:
- `validate-pr` command for automated PR code review
- `code-reviewer` subagent for dedicated code analysis
- SDLC Stage 4 (Implementation) validation
- SDLC Stage 5 (Testing & Quality Assurance) checks

## Universal Code Quality Framework

### 1. Code Structure & Organization

**File Organization Standards**:
```yaml
structure_validation:
  directory_structure:
    - Proper separation of concerns (components, services, utils)
    - Consistent naming conventions (camelCase, kebab-case, PascalCase)
    - Logical grouping of related functionality
  
  file_naming:
    - Descriptive, purposeful file names
    - Consistent extension usage (.ts, .tsx, .py)
    - Proper component/class naming conventions
  
  import_organization:
    - External dependencies first
    - Internal imports grouped logically
    - Unused imports removal
    - Consistent import path patterns
```

**Code Organization Patterns**:
```yaml
organization_checks:
  function_size:
    - Functions ≤ 50 lines (warning at 30+ lines)
    - Single responsibility principle adherence
    - Clear function naming and purpose
  
  class_design:
    - Classes with focused responsibilities
    - Proper encapsulation and access modifiers
    - Clear inheritance hierarchies
  
  module_cohesion:
    - Related functionality grouped together
    - Minimal coupling between modules
    - Clear module boundaries and interfaces
```

### 2. Language-Specific Quality Standards

#### TypeScript/JavaScript Code Review
```yaml
typescript_standards:
  type_safety:
    - Avoid 'any' type usage (flag all instances)
    - Proper interface/type definitions
    - Generic type usage where appropriate
    - Null/undefined handling with proper checks
  
  modern_patterns:
    - Use of ES6+ features appropriately
    - Arrow functions vs function declarations
    - Destructuring for object/array access
    - Async/await over Promise chains
  
  react_specific:
    - Proper hook usage and dependencies
    - Component composition over inheritance
    - Props interface definitions
    - Proper state management patterns
  
  performance_considerations:
    - Unnecessary re-renders prevention
    - Proper memoization usage
    - Bundle size impact awareness
    - Lazy loading for heavy components
```

#### Python Code Review
```yaml
python_standards:
  pep8_compliance:
    - Line length ≤ 88 characters (Black formatter standard)
    - Proper indentation (4 spaces)
    - Function and variable naming (snake_case)
    - Class naming (PascalCase)
  
  pythonic_patterns:
    - List comprehensions over explicit loops where appropriate
    - Context managers for resource handling
    - Proper exception handling
    - Use of built-in functions and libraries
  
  fastapi_specific:
    - Proper dependency injection patterns
    - Request/response model definitions
    - Error handling and status codes
    - API documentation completeness
  
  async_patterns:
    - Proper async/await usage
    - Database connection handling
    - Concurrent operation patterns
    - Resource cleanup in async contexts
```

### 3. Code Quality Metrics

**Complexity Analysis**:
```yaml
complexity_metrics:
  cyclomatic_complexity:
    - Functions with complexity > 10 flagged for review
    - Nested conditional statements minimization
    - Early return patterns for reduced complexity
  
  cognitive_load:
    - Clear variable and function naming
    - Minimal nested logic structures
    - Consistent code patterns throughout
    - Self-documenting code practices
  
  maintainability:
    - DRY principle adherence (Don't Repeat Yourself)
    - SOLID principles application
    - Clear separation of concerns
    - Testable code structure
```

**Performance Considerations**:
```yaml
performance_checks:
  algorithmic_efficiency:
    - O(n²) algorithms flagged for optimization
    - Unnecessary loops or iterations
    - Database query optimization opportunities
    - Memory usage patterns
  
  resource_management:
    - Proper cleanup of resources
    - Memory leak prevention
    - Efficient data structure usage
    - Caching strategy implementation
```

### 4. Testing & Documentation Requirements

**Test Coverage Standards**:
```yaml
testing_requirements:
  coverage_expectations:
    - Unit tests for all business logic functions
    - Integration tests for API endpoints
    - Component tests for React components
    - Error case testing coverage
  
  test_quality:
    - Clear test naming and organization
    - Proper test isolation (no dependencies)
    - Comprehensive edge case coverage
    - Performance test considerations
  
  testing_patterns:
    - AAA pattern (Arrange, Act, Assert)
    - Proper mocking and stubbing
    - Test data management
    - Async testing patterns
```

**Documentation Standards**:
```yaml
documentation_requirements:
  code_comments:
    - Complex logic explanation
    - API endpoint documentation
    - Function parameter descriptions
    - Known limitations or trade-offs
  
  api_documentation:
    - OpenAPI/Swagger completeness
    - Request/response examples
    - Error response documentation
    - Authentication requirements
  
  readme_requirements:
    - Setup and installation instructions
    - Environment configuration
    - Usage examples
    - Contributing guidelines
```

### 5. Project-Specific Standards

#### VanguardAI Maritime Insurance Context
```yaml
maritime_specific_standards:
  domain_logic:
    - Insurance calculation accuracy
    - Regulatory compliance patterns
    - Risk assessment implementations
    - Policy management workflows
  
  data_handling:
    - PII protection patterns
    - Financial data security
    - Audit trail implementation
    - GDPR compliance checks
  
  integration_patterns:
    - WorkOS authentication integration
    - JIRA workflow automation
    - Sentry error tracking setup
    - Maritime data validation
```

### 6. Security Integration

**Security-First Code Review** (Reference: security-validation-core.md):
```yaml
security_integration:
  mandatory_checks:
    - Input validation implementation
    - Authentication/authorization patterns
    - Secure data handling practices
    - Error handling without information disclosure
  
  security_patterns:
    - OWASP Top 10 compliance
    - Secure coding practices
    - Dependency vulnerability assessment
    - Security header implementation
```

## Code Review Scoring System

### Quality Score Calculation (0-100 scale)
```yaml
scoring_framework:
  base_score: 100
  
  deductions:
    critical_issues: -20    # Security vulnerabilities, breaking changes
    major_issues: -10       # Performance problems, poor architecture
    minor_issues: -5        # Style violations, minor improvements
    suggestions: -1         # Optimization opportunities
  
  bonus_points:
    comprehensive_tests: +10
    excellent_documentation: +5
    performance_optimizations: +5
    innovative_solutions: +5
```

### Approval Thresholds
```yaml
approval_criteria:
  auto_approve: ≥90       # Excellent code quality
  approve_with_comments: 75-89  # Good quality with minor improvements
  request_changes: 60-74  # Moderate issues requiring attention
  reject: <60            # Significant issues requiring major revision
```

## Review Report Generation

### Standard Code Review Report Format
```yaml
review_report_template:
  summary:
    overall_score: "[0-100]"
    files_reviewed: "[count]"
    approval_status: "[APPROVE|REVIEW|REJECT]"
    review_time: "[minutes]"
  
  quality_breakdown:
    structure_score: "[0-100]"
    type_safety_score: "[0-100]"
    performance_score: "[0-100]"
    testing_score: "[0-100]"
    documentation_score: "[0-100]"
  
  findings:
    critical_issues: []
    major_improvements: []
    minor_suggestions: []
    positive_patterns: []
  
  recommendations:
    immediate_actions: []
    long_term_improvements: []
    learning_opportunities: []
```

## Implementation Patterns

### Integration with validate-pr Command
```yaml
command_integration:
  execution_context:
    - Automated PR analysis
    - Multi-file review coordination
    - Integration with security validation
    - Performance impact assessment
  
  reporting_integration:
    - Combined security + quality scores
    - Consolidated improvement recommendations
    - Actionable next steps
```

### Subagent Specialization
```yaml
subagent_integration:
  code_reviewer_focus:
    - Deep code quality analysis
    - Architecture pattern validation
    - Refactoring recommendations
    - Technical debt identification
  
  enhanced_capabilities:
    - Multi-file dependency analysis
    - Cross-component impact assessment
    - Technical documentation generation
    - Code improvement roadmap creation
```

## Quality Assurance

**Framework Compliance**: Follows AI Agent Instruction Design Excellence:
- **Concrete Standards**: Specific quality criteria and measurable metrics
- **Language-Specific**: Tailored patterns for TypeScript/Python
- **Project-Aware**: Maritime insurance domain considerations
- **Integration-Ready**: Compatible with existing validation frameworks

**Continuous Improvement**:
- Regular standards updates based on team feedback
- Integration with emerging best practices
- Tool-specific optimization (ESLint, Black, MyPy)
- Performance benchmark tracking

This code review criteria framework ensures consistent, high-quality code assessment across all development stages and AI-assisted workflows.