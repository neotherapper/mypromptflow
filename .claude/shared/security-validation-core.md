# Security Validation Core Instructions

**Purpose**: Reusable security validation patterns extracted from validate-pr command for use across multiple AI agents and subagents.

**Usage**: This instruction library can be referenced by:
- `validate-pr` command for PR security validation
- `security-auditor` subagent for dedicated security reviews
- `code-reviewer` subagent for security-focused code review
- Any SDLC stage requiring security validation

## Core Security Validation Framework

### 1. OWASP Top 10 Compliance Checking

**Critical Security Patterns to Validate**:

#### A01: Broken Access Control
```yaml
access_control_checks:
  authentication_bypass: 
    - Check for missing authentication decorators/middleware
    - Validate authorization checks on sensitive endpoints
    - Ensure proper role-based access control (RBAC)
  
  privilege_escalation:
    - Verify user role validation in administrative functions
    - Check for hardcoded admin credentials or bypasses
    - Validate session management and user context isolation
```

#### A02: Cryptographic Failures
```yaml
cryptographic_checks:
  weak_encryption:
    - Flag use of deprecated algorithms (MD5, SHA1, DES)
    - Ensure use of strong encryption (AES-256, RSA-2048+)
    - Validate proper key management and storage
  
  data_exposure:
    - Check for unencrypted sensitive data transmission
    - Validate HTTPS enforcement and secure headers
    - Ensure encrypted storage of passwords and PII
```

#### A03: Injection Vulnerabilities
```yaml
injection_checks:
  sql_injection:
    - Identify raw SQL queries without parameterization
    - Validate use of prepared statements/ORM
    - Check for dynamic query construction
  
  xss_prevention:
    - Validate input sanitization for user-generated content
    - Check for proper output encoding
    - Ensure Content Security Policy (CSP) implementation
  
  command_injection:
    - Flag direct system command execution with user input
    - Validate input sanitization for shell commands
    - Ensure use of safe subprocess execution
```

### 2. Authentication & Authorization Patterns

**WorkOS Integration Security** (Project-Specific):
```yaml
workos_security_checks:
  sso_validation:
    - Verify proper WorkOS SDK integration
    - Check for secure token validation and storage
    - Ensure proper session management
  
  b2b_auth_patterns:
    - Validate organization-based access control
    - Check for proper user context isolation
    - Ensure secure API key management
```

**JIRA Integration Security**:
```yaml
jira_security_checks:
  api_security:
    - Validate secure JIRA API credential storage
    - Check for proper rate limiting implementation
    - Ensure secure webhook validation
  
  data_privacy:
    - Verify PII handling in JIRA ticket creation
    - Check for secure logging practices
    - Ensure proper data retention policies
```

### 3. Input Validation Framework

**Comprehensive Input Validation**:
```yaml
input_validation_patterns:
  sanitization_checks:
    - HTML/JavaScript injection prevention
    - SQL injection prevention through parameterization
    - Command injection prevention through input filtering
  
  validation_rules:
    - Length limits for all string inputs
    - Type validation for numeric inputs
    - Format validation for emails, URLs, dates
    - Whitelist validation for enum/choice fields
  
  error_handling:
    - Secure error messages (no information disclosure)
    - Proper exception handling without stack trace exposure
    - Logging security events without sensitive data
```

### 4. Security Headers & Configuration

**Required Security Headers Validation**:
```yaml
security_headers:
  required_headers:
    - "Content-Security-Policy": Prevent XSS and data injection
    - "X-Frame-Options": Prevent clickjacking attacks
    - "X-Content-Type-Options": Prevent MIME type sniffing
    - "Strict-Transport-Security": Enforce HTTPS connections
    - "Referrer-Policy": Control referrer information leakage
  
  cookie_security:
    - HttpOnly flag for session cookies
    - Secure flag for HTTPS-only cookies
    - SameSite attribute for CSRF protection
```

### 5. Code Security Analysis Patterns

**Static Analysis Patterns**:
```yaml
code_analysis:
  dangerous_functions:
    javascript:
      - "eval()", "innerHTML", "document.write()"
      - "setTimeout()" with string parameters
      - Direct DOM manipulation without sanitization
    
    python:
      - "exec()", "eval()", "pickle.loads()"
      - Raw SQL query construction
      - Unsafe deserialization patterns
    
    typescript:
      - "any" type usage in security-sensitive contexts
      - Unsafe type assertions
      - Direct HTML rendering without sanitization
  
  secure_patterns:
    - Use of parameterized queries/ORM
    - Input validation libraries usage
    - Secure random number generation
    - Proper error handling and logging
```

### 6. Sentry Integration Security

**Error Monitoring Security**:
```yaml
sentry_security_checks:
  data_sanitization:
    - Ensure PII scrubbing in error reports  
    - Validate secure credential handling in logs
    - Check for proper data retention settings
  
  access_control:
    - Verify Sentry project access permissions
    - Check for secure Sentry DSN management
    - Ensure proper team-based access control
```

## Validation Execution Framework

### Security Assessment Scoring

**Scoring Criteria (0-100 scale)**:
```yaml
security_scoring:
  critical_issues: -25  # Each critical security vulnerability
  high_issues: -10      # Each high-severity security issue
  medium_issues: -5     # Each medium-severity security issue
  low_issues: -1        # Each low-severity security issue
  
  bonus_points:
    comprehensive_input_validation: +10
    proper_authentication_implementation: +10
    secure_error_handling: +5
    security_headers_implementation: +5
```

**Approval Thresholds**:
- **APPROVE**: Score ≥ 85 (no critical issues, minimal high-severity issues)
- **REVIEW**: Score 60-84 (moderate issues requiring attention)
- **BLOCK**: Score < 60 (critical security vulnerabilities present)

### Security Report Generation

**Standard Security Report Format**:
```yaml
security_report_template:
  summary:
    overall_score: "[0-100]"
    risk_level: "[LOW|MEDIUM|HIGH|CRITICAL]"
    approval_recommendation: "[APPROVE|REVIEW|BLOCK]"
  
  critical_findings:
    - issue_type: "[SQL Injection|XSS|Authentication Bypass|etc.]"
      severity: "CRITICAL"
      location: "[file:line_number]"
      description: "[Detailed vulnerability description]"
      recommendation: "[Specific fix recommendation]"
  
  security_improvements:
    - category: "[Input Validation|Authentication|etc.]"
      recommendation: "[Specific improvement]"
      priority: "[HIGH|MEDIUM|LOW]"
      effort_estimate: "[hours/days]"
```

## Integration Patterns

### Command Integration
```yaml
# For use in validate-pr command
security_validation_integration:
  trigger_conditions:
    - File types: "*.ts", "*.tsx", "*.py", "*.js", "*.jsx"
    - Security-sensitive paths: "/auth/", "/api/", "/login/"
  
  execution_context:
    - Apply all OWASP Top 10 checks
    - Include project-specific patterns (WorkOS, JIRA, Sentry)
    - Generate security report with scoring
```

### Subagent Integration
```yaml
# For use in security-auditor subagent
subagent_security_integration:
  specialized_focus:
    - Deep security analysis with extended time allocation
    - Comprehensive vulnerability scanning
    - Security architecture review
    - Compliance framework validation
  
  enhanced_capabilities:
    - Multi-file security pattern analysis
    - Cross-component security validation
    - Security documentation generation
```

## Implementation Notes

**Framework Compliance**: This security validation core follows AI Agent Instruction Design Excellence principles:
- **Concrete Instructions**: Specific security patterns and validation criteria
- **Self-Sufficient**: Complete security framework without external dependencies
- **Immediately Actionable**: Clear validation steps and scoring mechanisms
- **Resource Efficient**: Reusable across multiple validation contexts

**Quality Standards**: 
- Evidence-based security patterns from OWASP guidelines
- Project-specific integration for WorkOS, JIRA, and Sentry
- Measurable scoring system for security assessment
- Comprehensive reporting for actionable security improvements

This security validation core enables consistent, high-quality security validation across all SDLC stages and AI agents.