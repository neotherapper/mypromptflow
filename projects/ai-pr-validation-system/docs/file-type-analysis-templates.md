# File-Type Specific Analysis Templates

## Overview

This specification defines specialized analysis templates for different file types, leveraging the **unified source-discovery-framework** with role-aware knowledge management for optimal validation accuracy.

**Foundation**: Built on unified source-discovery-framework.yaml eliminating duplicate mappings and providing consistent technology-specific source selection across research and validation workflows.

**Unified Framework Integration**: `@meta/information-access/source-discovery-framework.yaml`

---

## 🎯 File Type Detection & Agent Mapping

### Multi-Layered Detection Architecture
*References unified framework step_1_topic_analysis*

```yaml
detection_layers:
  # Uses source-discovery-framework.yaml detection algorithms
  framework_reference: "meta/information-access/source-discovery-framework.yaml"
  
  layer_1_extension:
    pattern_matching: "*.{ts,tsx,js,jsx,py,md,yaml,json,vue,svelte}"
    confidence_base: 0.6
    framework_mapping: "category_mappings.frontend, category_mappings.backend"

  layer_2_content:
    magic_numbers: "AST parsing, file headers, syntax detection"
    confidence_boost: 0.3
    framework_mapping: "technology_mappings specific detection"

  layer_3_context:
    directory_structure: "src/, tests/, docs/, .claude/, components/"
    dependency_analysis: "package.json, requirements.txt, pyproject.toml"
    confidence_boost: 0.1
    framework_mapping: "source_selection_algorithm.step_3_source_coordination"
```

### Role-Aware Agent Spawning Logic
*Integrates with unified framework pr_validation_integration*

```yaml
agent_spawning_matrix:
  typescript_react:
    file_patterns: ["*.ts", "*.tsx"]
    context_indicators: ["React imports", "JSX syntax", "component patterns"]
    # UNIFIED FRAMEWORK INTEGRATION
    framework_mapping: "technology_mappings.react + technology_mappings.typescript"
    source_discovery: "meta/information-access/source-discovery-framework.yaml"
    
    primary_agents:
      - role: "architect"
        context: "REQUEST_CONTEXT(typescript-architect, react-architect)"
        focus: "System design, type safety, architectural patterns"
        framework_sources: "technology_mappings.react.pr_validation_context.architect_role"
        knowledge_sources: "technology_mappings.react.pr_validation_context.knowledge_sources[0-1]"
        
      - role: "frontend-dev"
        context: "REQUEST_CONTEXT(typescript-frontend-dev, react-frontend-dev)"
        focus: "Component implementation, user experience, React patterns"  
        framework_sources: "technology_mappings.react.pr_validation_context.frontend_dev_role"
        knowledge_sources: "technology_mappings.react.pr_validation_context.knowledge_sources[1]"
        
      - role: "performance"
        context: "REQUEST_CONTEXT(typescript-performance, react-performance)"
        focus: "Bundle optimization, rendering performance, memory usage"
        framework_sources: "technology_mappings.react.pr_validation_context.performance_role"
        knowledge_sources: "technology_mappings.react.pr_validation_context.knowledge_sources[2]"
        
      - role: "security"
        context: "REQUEST_CONTEXT(react-security, testing-security)"
        focus: "XSS prevention, secure coding, dependency vulnerabilities"
        framework_sources: "technology_mappings.react.pr_validation_context.security_role"
        knowledge_sources: "technology_mappings.react.pr_validation_context.knowledge_sources[3]"
```

---

## 📁 TypeScript/React Analysis Template

### File Detection Criteria
*Uses unified framework technology_mappings.react + technology_mappings.typescript*

```yaml
typescript_react_detection:
  # UNIFIED FRAMEWORK INTEGRATION
  framework_reference: "meta/information-access/source-discovery-framework.yaml"
  technology_mappings: ["react", "typescript"]
  
  file_extensions: [".ts", ".tsx"]
  content_patterns:
    - "import React"
    - "export default function"
    - "interface Props"
    - "useState|useEffect|useContext"
    - "JSX.Element|ReactNode|FC<"

  context_clues:
    - package.json contains "react" dependency
    - tsconfig.json present
    - src/ directory structure
    - component naming conventions
    
  # Uses unified framework source discovery
  information_sources:
    primary: "technology_mappings.react.sources.primary"
    supplementary: "technology_mappings.react.sources.supplementary"
    validation: "technology_mappings.react.sources.validation"
```

### Role-Specific Analysis Framework
*Integrates with unified framework pr_validation_context*

#### 🏗️ Architect Analysis (TypeScript/React)

```yaml
architect_analysis:
  # UNIFIED FRAMEWORK INTEGRATION
  framework_reference: "technology_mappings.react.pr_validation_context.architect_role"
  context_loading: "REQUEST_CONTEXT(typescript-architect, react-architect)"
  
  # Uses unified framework knowledge sources
  knowledge_source:
    - "technology_mappings.react.pr_validation_context.knowledge_sources[0]"
    - "technology_mappings.typescript.pr_validation_context.knowledge_sources[0]"
  
  # Leverages unified framework source discovery
  information_access:
    primary_sources: "technology_mappings.react.sources.primary"
    github_repos: "technology_mappings.react.sources.primary[0]"
    documentation: "technology_mappings.react.sources.primary[1]"

  primary_concerns:
    type_architecture:
      weight: 35%
      criteria:
        - Type safety and inference
        - Interface and type definitions
        - Generic type usage
        - Type composition patterns

    component_architecture:
      weight: 30%
      criteria:
        - Component composition
        - Props interface design
        - State management architecture
        - Component hierarchy

    system_integration:
      weight: 20%
      criteria:
        - Module dependency structure
        - API integration patterns
        - Error boundary implementation
        - Context usage patterns

    maintainability:
      weight: 15%
      criteria:
        - Code organization
        - Separation of concerns
        - Documentation quality
        - Reusability patterns

  validation_questions:
    - "Are TypeScript types properly defined and used?"
    - "Is component architecture scalable and maintainable?"
    - "Are React patterns correctly implemented?"
    - "Is the code structure logical and well-organized?"

  scoring_criteria:
    excellent: "Strong type safety, clean architecture, proper React patterns"
    good: "Generally well-structured with minor architectural issues"
    fair: "Some architectural concerns, type safety could be improved"
    poor: "Significant architectural problems, weak type usage"
    critical: "Major architectural flaws, type safety issues"
```

#### 🎨 Frontend Developer Analysis (TypeScript/React)

```yaml
frontend_dev_analysis:
  context_loading: "REQUEST_CONTEXT(typescript-frontend-dev, react-frontend-dev)"
  knowledge_source:
    - "knowledge-vault/knowledge/technologies/typescript/typescript-frontend-dev.md"
    - "knowledge-vault/knowledge/technologies/react/react-frontend-dev.md"

  primary_concerns:
    user_experience:
      weight: 40%
      criteria:
        - Accessibility implementation
        - User interaction patterns
        - Visual design consistency
        - Error handling and feedback

    react_implementation:
      weight: 30%
      criteria:
        - Hook usage patterns
        - State management approach
        - Event handling
        - Component lifecycle

    frontend_best_practices:
      weight: 20%
      criteria:
        - Form handling
        - Responsive design
        - Browser compatibility
        - Performance considerations

    code_quality:
      weight: 10%
      criteria:
        - Component testability
        - Code readability
        - Naming conventions
        - Documentation

  validation_questions:
    - "Is the user interface accessible and intuitive?"
    - "Are React hooks and patterns used correctly?"
    - "Is error handling user-friendly?"
    - "Are components properly tested?"

  critical_checks:
    accessibility:
      - ARIA labels and roles
      - Keyboard navigation support
      - Screen reader compatibility
      - Color contrast compliance

    react_patterns:
      - Proper hook dependencies
      - State update patterns
      - Event handler implementation
      - Component composition
```

#### ⚡ Performance Specialist Analysis (TypeScript/React)

```yaml
performance_analysis:
  context_loading: "REQUEST_CONTEXT(typescript-performance, react-performance)"
  knowledge_source:
    - "knowledge-vault/knowledge/technologies/typescript/typescript-performance.md"
    - "knowledge-vault/knowledge/technologies/react/react-performance.md"

  primary_concerns:
    rendering_performance:
      weight: 35%
      criteria:
        - Component re-render optimization
        - Memoization usage (React.memo, useMemo, useCallback)
        - Virtual DOM efficiency
        - Conditional rendering patterns

    bundle_optimization:
      weight: 25%
      criteria:
        - Code splitting implementation
        - Tree shaking effectiveness
        - Import optimization
        - Bundle size impact

    runtime_efficiency:
      weight: 25%
      criteria:
        - Algorithm complexity
        - Memory usage patterns
        - Event handler efficiency
        - Data structure optimization

    loading_performance:
      weight: 15%
      criteria:
        - Lazy loading implementation
        - Resource preloading
        - Critical path optimization
        - Caching strategies

  performance_metrics:
    bundle_size:
      threshold_warning: ">500KB increase"
      threshold_critical: ">1MB increase"

    rendering_impact:
      threshold_warning: ">16ms render time"
      threshold_critical: ">33ms render time"

    memory_usage:
      threshold_warning: ">10MB increase"
      threshold_critical: ">50MB increase"
```

#### 🔒 Security Specialist Analysis (TypeScript/React)

```yaml
security_analysis:
  context_loading: "REQUEST_CONTEXT(react-security, testing-security)"
  knowledge_source:
    - "knowledge-vault/knowledge/technologies/react/react-security.md"
    - "knowledge-vault/knowledge/technologies/testing/testing-security.md"

  primary_concerns:
    xss_prevention:
      weight: 30%
      criteria:
        - Input sanitization
        - Output encoding
        - dangerouslySetInnerHTML usage
        - User input handling

    authentication_security:
      weight: 25%
      criteria:
        - Token storage patterns
        - Session management
        - Authentication state handling
        - Secure route protection

    data_protection:
      weight: 25%
      criteria:
        - Sensitive data exposure
        - API security patterns
        - Client-side validation
        - Error message security

    dependency_security:
      weight: 20%
      criteria:
        - Third-party library vulnerabilities
        - Package security scanning
        - Supply chain security
        - Version management

  vulnerability_patterns:
    high_risk:
      - "dangerouslySetInnerHTML with user input"
      - "eval() or Function() constructor usage"
      - "Unvalidated redirects"
      - "Exposed API keys or secrets"

    medium_risk:
      - "Client-side only validation"
      - "Insecure token storage"
      - "Missing CSRF protection"
      - "Vulnerable dependencies"
```

---

## 📄 Python/Backend Analysis Template

### File Detection Criteria

```yaml
python_backend_detection:
  file_extensions: [".py"]
  content_patterns:
    - "from flask import|from django.http import|from fastapi import"
    - "def api_|@app.route|@router.get"
    - "class.*Model|class.*Serializer"
    - "import requests|import sqlalchemy"

  context_clues:
    - requirements.txt or pyproject.toml present
    - API endpoint patterns
    - Database model definitions
    - Authentication middleware
```

### Role-Specific Analysis Framework

#### 🏗️ Architect Analysis (Python/Backend)

```yaml
python_architect_analysis:
  context_loading: "REQUEST_CONTEXT(python-architect, api-architecture)"

  primary_concerns:
    api_architecture:
      weight: 35%
      criteria:
        - REST/GraphQL design patterns
        - Endpoint organization
        - Response structure consistency
        - API versioning strategy

    data_architecture:
      weight: 30%
      criteria:
        - Database design patterns
        - ORM usage and optimization
        - Data model relationships
        - Migration strategies

    system_design:
      weight: 20%
      criteria:
        - Service layer organization
        - Dependency injection
        - Configuration management
        - Error handling architecture

    scalability:
      weight: 15%
      criteria:
        - Performance considerations
        - Caching strategies
        - Async/await usage
        - Resource management
```

#### 🔒 Security Specialist Analysis (Python/Backend)

```yaml
python_security_analysis:
  context_loading: "REQUEST_CONTEXT(backend-security, api-security)"

  primary_concerns:
    input_validation:
      weight: 30%
      criteria:
        - SQL injection prevention
        - Input sanitization
        - Parameter validation
        - Schema validation

    authentication_authorization:
      weight: 25%
      criteria:
        - JWT implementation
        - Session security
        - Role-based access control
        - API key management

    data_security:
      weight: 25%
      criteria:
        - Data encryption
        - Sensitive data handling
        - Database security
        - Logging security

    api_security:
      weight: 20%
      criteria:
        - Rate limiting
        - CORS configuration
        - HTTPS enforcement
        - API documentation security

  critical_vulnerabilities:
    - "SQL injection vectors"
    - "Unvalidated user input"
    - "Hardcoded secrets"
    - "Insecure direct object references"
    - "Missing authentication checks"
```

---

## 📋 YAML/Configuration Analysis Template

### File Detection Criteria

```yaml
yaml_config_detection:
  file_extensions: [".yml", ".yaml"]
  file_patterns:
    - "docker-compose.yml"
    - ".github/workflows/*.yml"
    - "kubernetes/*.yaml"
    - "ansible/*.yml"

  content_patterns:
    - "apiVersion:|version:|services:|tasks:"
    - "image:|ports:|volumes:|environment:"
    - "on:|jobs:|steps:|uses:"
```

### Security-First Analysis Framework

```yaml
yaml_security_analysis:
  context_loading: "REQUEST_CONTEXT(devops-security, infrastructure-security)"

  primary_concerns:
    secrets_management:
      weight: 40%
      criteria:
        - Hardcoded secrets detection
        - Environment variable usage
        - Secret management patterns
        - Encryption at rest

    access_control:
      weight: 25%
      criteria:
        - Permission configurations
        - Network access rules
        - Service account permissions
        - Resource isolation

    infrastructure_security:
      weight: 20%
      criteria:
        - Container security
        - Network policies
        - Resource limits
        - Security contexts

    compliance:
      weight: 15%
      criteria:
        - Security policy compliance
        - Audit logging
        - Monitoring configuration
        - Backup strategies

  critical_checks:
    secrets_exposure:
      patterns:
        - "password:|secret:|key:|token:"
        - ".*_PASSWORD=.*|.*_SECRET=.*|.*_KEY=.*"
        - "-----BEGIN.*PRIVATE KEY-----"

    insecure_configurations:
      patterns:
        - "privileged: true"
        - "runAsUser: 0"
        - "allowPrivilegeEscalation: true"
        - "securityContext: {}"
```

---

## 🧪 Test File Analysis Template

### File Detection Criteria

```yaml
test_file_detection:
  file_extensions: [".test.ts", ".test.js", ".spec.ts", ".spec.js", ".test.py"]
  content_patterns:
    - "describe|it|test|expect|assert"
    - "beforeEach|afterEach|beforeAll|afterAll"
    - "jest|vitest|pytest|unittest"
    - "render|fireEvent|screen|getBy"

  context_clues:
    - __tests__/ directory
    - test/ directory
    - Testing framework imports
```

### Comprehensive Test Analysis

```yaml
test_analysis_framework:
  context_loading: "REQUEST_CONTEXT(testing-frontend-dev, testing-performance, testing-security)"

  primary_concerns:
    test_coverage:
      weight: 35%
      criteria:
        - Line coverage percentage
        - Branch coverage percentage
        - Function coverage percentage
        - Critical path coverage

    test_quality:
      weight: 30%
      criteria:
        - Test case clarity
        - Edge case coverage
        - Error condition testing
        - Integration test completeness

    test_performance:
      weight: 20%
      criteria:
        - Test execution time
        - Resource usage during testing
        - Parallel test execution
        - Test isolation

    test_security:
      weight: 15%
      criteria:
        - Security test coverage
        - Vulnerability testing
        - Authentication testing
        - Authorization testing

  test_quality_metrics:
    excellent: ">90% coverage, comprehensive edge cases, fast execution"
    good: ">80% coverage, good edge case handling, reasonable performance"
    fair: ">70% coverage, basic edge cases, acceptable performance"
    poor: ">50% coverage, limited edge cases, slow execution"
    critical: "<50% coverage, missing critical tests, performance issues"
```

---

## 🔄 Integration and Report Generation

### File Type Analysis Aggregation

```typescript
interface FileTypeAnalysisResult {
  fileType: string;
  fileCount: number;
  filesAnalyzed: string[];
  roleAnalyses: {
    architect?: ArchitectAnalysis;
    frontendDev?: FrontendAnalysis;
    performance?: PerformanceAnalysis;
    security?: SecurityAnalysis;
  };
  overallScore: number;
  criticalIssues: Issue[];
  recommendations: Recommendation[];
}

interface TechnologyBreakdown {
  technology: string;
  fileCount: number;
  agentRole: string;
  contextSource: string;
  validationResults: {
    qualityScore: number;
    securityScore: number;
    performanceScore: number;
    issuesCount: number;
  };
  keyFindings: Finding[];
}
```

### Report Template Integration

```markdown
## 📁 File-Type Specific Analysis

### Technology Breakdown

{{#each TECHNOLOGIES}}

#### {{tech_name}} Files ({{file_count}} files)

**Primary Agent**: {{primary_agent_role}} | **Context**: {{context_source}}
**Knowledge Base**: {{knowledge_lines}} lines of expert content

**Files Analyzed:**
{{#each files}}

- `{{file_path}}` ({{change_type}}, +{{lines_added}}/-{{lines_removed}} lines)
  - **Complexity**: {{complexity_score}}/10
  - **Risk Level**: {{risk_level}}
    {{/each}}

**Multi-Role Validation Results:**
| Role | Score | Issues | Focus Areas |
|------|--------|--------|-------------|
| Architect | {{arch_score}}/100 | {{arch_issues}} | {{arch_focus}} |
| Frontend Dev | {{frontend_score}}/100 | {{frontend_issues}} | {{frontend_focus}} |
| Performance | {{perf_score}}/100 | {{perf_issues}} | {{perf_focus}} |
| Security | {{sec_score}}/100 | {{sec_issues}} | {{sec_focus}} |

**Key Technology-Specific Findings:**
{{#each findings}}

- **{{severity}}**: {{finding}}
  - **Technical Impact**: {{technical_impact}}
  - **Recommendation**: {{recommendation}}
  - **Expert Role**: {{expert_role}}
    {{/each}}

**Context-Aware Insights:**
{{context_insights}}
{{/each}}
```

This file-type analysis template system leverages the **unified source-discovery-framework** to provide specialized, expert-level analysis for each technology stack while maintaining consistency across the validation process.

## 🔗 Unified Framework Consolidation Summary

### ✅ Consolidation Complete

This document has been **fully integrated** with the unified source-discovery-framework, eliminating all duplicate mappings:

**Removed Duplications**:
- ❌ Separate React source mappings → ✅ Uses `technology_mappings.react`
- ❌ Separate TypeScript source mappings → ✅ Uses `technology_mappings.typescript`  
- ❌ Separate Python backend mappings → ✅ Uses `technology_mappings.python`
- ❌ Separate infrastructure source mappings → ✅ Uses `category_mappings.infrastructure`
- ❌ Independent PR validation contexts → ✅ Uses `pr_validation_integration`

**Unified Framework Benefits**:
- **Single Source of Truth**: All source discovery logic centralized in `meta/information-access/source-discovery-framework.yaml`
- **Consistency**: Same source selection algorithm used by research orchestrator and PR validation
- **Maintainability**: Updates to technology mappings automatically apply to both workflows
- **Role-Aware Integration**: PR validation contexts properly mapped to unified framework roles
- **MCP Server Coordination**: Centralized MCP server discovery and error handling

**Integration Verification**:
- ✅ All technology-specific validators reference unified framework mappings
- ✅ Role-aware contexts properly linked to framework pr_validation_context
- ✅ Information sources consistently mapped to framework source discovery
- ✅ No duplicate source selection logic remains in validation system
- ✅ Framework integration documented in validator registry
