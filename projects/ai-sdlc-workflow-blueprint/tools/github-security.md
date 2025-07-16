# GitHub Security Features for Maritime Insurance Applications

## Overview

GitHub provides comprehensive security features to protect code, dependencies, and sensitive data throughout the software development lifecycle. For maritime insurance applications handling sensitive vessel data, policy information, and risk assessments, these security features are essential for maintaining compliance and protecting customer information.

## Key Security Features

### 1. Dependabot
- **Automated dependency updates**: Monitors dependencies for known vulnerabilities
- **Security alerts**: Immediate notifications for vulnerable dependencies
- **Automated pull requests**: Creates PRs to update vulnerable dependencies
- **Version updates**: Keeps dependencies current with configurable update schedules

### 2. Code Scanning with CodeQL
- **Static analysis**: Identifies security vulnerabilities in code
- **Custom queries**: Create maritime-specific security rules
- **Pull request integration**: Blocks merging of vulnerable code
- **Multiple language support**: JavaScript, TypeScript, Python, Java, Go, and more

### 3. Secret Scanning
- **Token detection**: Identifies exposed API keys, passwords, and certificates
- **Partner patterns**: Detects tokens from 100+ service providers
- **Push protection**: Prevents secrets from being committed
- **Custom patterns**: Define maritime-specific secret patterns

### 4. Security Policies
- **SECURITY.md**: Define vulnerability reporting procedures
- **Security advisories**: Private vulnerability discussions and fixes
- **Coordinated disclosure**: Manage vulnerability disclosure timelines

## Configuration Examples

### 1. Dependabot Configuration

Create `.github/dependabot.yml`:

```yaml
version: 2
updates:
  # Enable version updates for npm
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "daily"
      time: "04:00"
    open-pull-requests-limit: 10
    reviewers:
      - "maritime-security-team"
    labels:
      - "dependencies"
      - "security"
    commit-message:
      prefix: "chore"
      prefix-development: "chore"
      include: "scope"
    # Security updates only for production dependencies
    allow:
      - dependency-type: "production"
    
  # Docker base image updates
  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"
    reviewers:
      - "maritime-devops-team"
    
  # Python dependencies for risk calculation services
  - package-ecosystem: "pip"
    directory: "/services/risk-calculator"
    schedule:
      interval: "weekly"
    versioning-strategy: "lockfile-only"
    
  # GitHub Actions
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    commit-message:
      prefix: "ci"
```

### 2. CodeQL Analysis Setup

Create `.github/workflows/codeql-analysis.yml`:

```yaml
name: "CodeQL Security Analysis"

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '30 5 * * 1'  # Weekly scan on Mondays

jobs:
  analyze:
    name: Analyze
    runs-on: ubuntu-latest
    permissions:
      actions: read
      contents: read
      security-events: write

    strategy:
      fail-fast: false
      matrix:
        language: [ 'javascript', 'typescript', 'python' ]

    steps:
    - name: Checkout repository
      uses: actions/checkout@v4

    - name: Initialize CodeQL
      uses: github/codeql-action/init@v3
      with:
        languages: ${{ matrix.language }}
        queries: +security-extended,security-and-quality
        # Custom queries for maritime insurance
        config-file: ./.github/codeql/codeql-config.yml

    - name: Autobuild
      uses: github/codeql-action/autobuild@v3

    - name: Perform CodeQL Analysis
      uses: github/codeql-action/analyze@v3
      with:
        category: "/language:${{matrix.language}}"
```

### 3. Custom CodeQL Configuration

Create `.github/codeql/codeql-config.yml`:

```yaml
name: "Maritime Insurance Security Configuration"

queries:
  - uses: security-extended
  - uses: security-and-quality
  
query-filters:
  - exclude:
      id: js/angular/insecure-url-whitelist
  - exclude:
      id: py/flask-debug

paths-ignore:
  - 'node_modules'
  - 'test'
  - '**/*.test.js'
  - '**/*.spec.ts'

# Custom query suites for maritime data
packs:
  - maritime-insurance/vessel-data-queries
  - maritime-insurance/policy-validation-queries
```

### 4. Custom CodeQL Queries for Maritime Data

Create `.github/codeql/queries/vessel-data-exposure.ql`:

```ql
/**
 * @name Vessel data exposure in logs
 * @description Detects potential vessel identification data in log statements
 * @kind problem
 * @problem.severity warning
 * @security-severity 6.5
 * @tags security
 *       maritime
 *       data-exposure
 */

import javascript
import semmle.javascript.security.dataflow.LogInjectionQuery

from DataFlow::Node source, DataFlow::Node sink
where
  sink instanceof LoggerCall and
  source.asExpr().(PropertyAccess).getPropertyName().regexpMatch(".*(?i)(imo|mmsi|vessel.*id|ship.*number).*") and
  DataFlow::localFlow(source, sink)
select sink, "Potential vessel identification data exposed in logs from $@.", source, "here"
```

### 5. Secret Scanning Configuration

Create `.github/secret_scanning.yml`:

```yaml
# Custom patterns for maritime insurance secrets
paths-ignore:
  - 'docs/**'
  - '*.md'
  - 'test/**'

custom-patterns:
  - name: Maritime API Key
    pattern: 'MAR_API_[A-Z0-9]{32}'
    
  - name: Vessel Tracking Token
    pattern: 'VTS_TOKEN_[a-zA-Z0-9]{40}'
    
  - name: Lloyd's API Credential
    pattern: 'LLOYDS_[A-Z]+_[A-Z0-9]{20,}'
    
  - name: Marine Weather Service Key
    pattern: 'MWS_KEY_[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
```

### 6. Security Policy

Create `SECURITY.md`:

```markdown
# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.x.x   | :white_check_mark: |
| 1.x.x   | :x:                |

## Reporting a Vulnerability

The Maritime Insurance Platform team takes security vulnerabilities seriously. We appreciate your efforts to responsibly disclose your findings.

### Where to Report

**DO NOT** create a public GitHub issue for security vulnerabilities.

Instead, please report security vulnerabilities by emailing:
security@maritime-insurance.example.com

### What to Include

- Type of vulnerability
- Full paths of source file(s) related to the vulnerability
- Location of the affected source code (tag/branch/commit or direct URL)
- Step-by-step instructions to reproduce the issue
- Proof-of-concept or exploit code (if possible)
- Impact assessment

### Response Timeline

- **Initial Response**: Within 48 hours
- **Vulnerability Assessment**: Within 5 business days
- **Resolution Timeline**: Based on severity
  - Critical: 7 days
  - High: 14 days
  - Medium: 30 days
  - Low: 90 days

### Disclosure Policy

- Security advisories will be published after the fix is released
- Credit will be given to reporters (unless anonymity is requested)
- We follow coordinated disclosure practices
```

## Maritime Insurance Security Examples

### 1. Protecting Vessel Data

```yaml
# .github/workflows/vessel-data-security.yml
name: Vessel Data Security Check

on:
  pull_request:
    paths:
      - 'src/services/vessel/**'
      - 'src/api/vessel/**'

jobs:
  data-protection:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check for IMO number exposure
        run: |
          # Check for hardcoded IMO numbers
          if grep -r "IMO[0-9]\{7\}" src/ --exclude-dir=test; then
            echo "::error::Hardcoded IMO numbers detected"
            exit 1
          fi
      
      - name: Verify encryption requirements
        run: |
          # Ensure vessel data models use encryption decorators
          python scripts/check_encryption_decorators.py src/models/vessel/
```

### 2. Policy Data Protection

```javascript
// Custom ESLint rules for policy data (.eslintrc.js)
module.exports = {
  rules: {
    'no-policy-data-in-logs': {
      create(context) {
        return {
          CallExpression(node) {
            if (node.callee.name === 'console' || 
                node.callee.property?.name === 'log') {
              const args = node.arguments;
              args.forEach(arg => {
                if (arg.type === 'Identifier' && 
                    /policy|premium|claim/i.test(arg.name)) {
                  context.report({
                    node,
                    message: 'Avoid logging sensitive policy data'
                  });
                }
              });
            }
          }
        };
      }
    }
  }
};
```

### 3. Risk Assessment Data Security

```python
# scripts/check_encryption_decorators.py
import ast
import sys
from pathlib import Path

class EncryptionChecker(ast.NodeVisitor):
    def __init__(self):
        self.missing_encryption = []
    
    def visit_ClassDef(self, node):
        has_encryption = False
        sensitive_fields = []
        
        for item in node.body:
            if isinstance(item, ast.AnnAssign):
                field_name = item.target.id if hasattr(item.target, 'id') else None
                if field_name and any(term in field_name.lower() 
                                     for term in ['risk', 'score', 'premium', 'claim']):
                    sensitive_fields.append(field_name)
        
        for decorator in node.decorator_list:
            if hasattr(decorator, 'id') and decorator.id == 'encrypted_model':
                has_encryption = True
                break
        
        if sensitive_fields and not has_encryption:
            self.missing_encryption.append({
                'class': node.name,
                'fields': sensitive_fields
            })
        
        self.generic_visit(node)

def check_directory(directory):
    checker = EncryptionChecker()
    
    for py_file in Path(directory).glob('**/*.py'):
        with open(py_file, 'r') as f:
            tree = ast.parse(f.read())
            checker.visit(tree)
    
    if checker.missing_encryption:
        print("Classes missing encryption:")
        for item in checker.missing_encryption:
            print(f"  - {item['class']}: {', '.join(item['fields'])}")
        sys.exit(1)
    else:
        print("All sensitive classes have encryption decorators")

if __name__ == '__main__':
    check_directory(sys.argv[1])
```

## Vulnerability Management

### 1. Creating Security Advisories

```bash
# Using GitHub CLI to create a security advisory
gh api \
  --method POST \
  /repos/maritime-insurance/platform/security-advisories \
  --field summary="SQL Injection in vessel search" \
  --field description="SQL injection vulnerability in vessel search API endpoint" \
  --field severity="high" \
  --field cve_id="CVE-2024-12345" \
  --field vulnerable_versions="<2.1.0" \
  --field patched_versions=">=2.1.0"
```

### 2. Automated Security Updates Workflow

```yaml
# .github/workflows/security-updates.yml
name: Automated Security Updates

on:
  schedule:
    - cron: '0 2 * * *'  # Daily at 2 AM
  workflow_dispatch:

jobs:
  security-updates:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run npm audit
        id: npm_audit
        run: |
          npm audit --json > audit-report.json
          echo "vulnerabilities=$(jq '.metadata.vulnerabilities.total' audit-report.json)" >> $GITHUB_OUTPUT
      
      - name: Fix vulnerabilities
        if: steps.npm_audit.outputs.vulnerabilities > 0
        run: |
          npm audit fix --force
          npm test
      
      - name: Create Pull Request
        if: steps.npm_audit.outputs.vulnerabilities > 0
        uses: peter-evans/create-pull-request@v5
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          commit-message: 'fix(security): automated vulnerability fixes'
          title: 'Security: Automated vulnerability fixes'
          body: |
            ## Automated Security Update
            
            This PR contains automated security fixes from npm audit.
            
            ### Vulnerabilities Fixed
            See audit-report.json for details.
            
            ### Testing
            - [ ] All tests pass
            - [ ] No breaking changes
            - [ ] Security scan clean
          branch: security/automated-fixes
          reviewers: maritime-security-team
```

## Team Security Integration

### 1. Security Team Configuration

```yaml
# .github/CODEOWNERS
# Security team owns all security-related files
/SECURITY.md @maritime-insurance/security-team
/.github/workflows/security-*.yml @maritime-insurance/security-team
/.github/workflows/codeql-*.yml @maritime-insurance/security-team
/.github/dependabot.yml @maritime-insurance/security-team

# Vessel data protection
/src/services/vessel/ @maritime-insurance/security-team @maritime-insurance/vessel-team
/src/models/vessel/ @maritime-insurance/security-team @maritime-insurance/vessel-team

# Policy and claims data
/src/services/policy/ @maritime-insurance/security-team @maritime-insurance/policy-team
/src/services/claims/ @maritime-insurance/security-team @maritime-insurance/claims-team
```

### 2. Security Review Automation

```yaml
# .github/workflows/security-review.yml
name: Security Review Requirements

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  security-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check security impact
        id: security_check
        run: |
          # Check for security-sensitive file changes
          SENSITIVE_FILES=$(git diff --name-only origin/main..HEAD | grep -E "(auth|security|crypto|vessel.*data|policy.*data)" || true)
          
          if [ -n "$SENSITIVE_FILES" ]; then
            echo "requires_security_review=true" >> $GITHUB_OUTPUT
            echo "files=$SENSITIVE_FILES" >> $GITHUB_OUTPUT
          fi
      
      - name: Add security review label
        if: steps.security_check.outputs.requires_security_review == 'true'
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.addLabels({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.issue.number,
              labels: ['security-review-required']
            });
      
      - name: Request security team review
        if: steps.security_check.outputs.requires_security_review == 'true'
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.pulls.requestReviewers({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: context.issue.number,
              team_reviewers: ['security-team']
            });
```

## CI/CD Security Integration

### 1. Secure Build Pipeline

```yaml
# .github/workflows/secure-build.yml
name: Secure Build Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  DOCKER_BUILDKIT: 1

jobs:
  security-scan:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      security-events: write
      
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'
      
      - name: Upload Trivy results to GitHub Security
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: 'trivy-results.sarif'
      
      - name: SAST Scan with Semgrep
        uses: returntocorp/semgrep-action@v1
        with:
          config: >-
            p/security-audit
            p/owasp-top-ten
            p/typescript
            p/javascript
            p/dockerfile
          generateSarif: true
      
      - name: Container scan
        uses: anchore/scan-action@v3
        with:
          image: "maritime-insurance/platform:${{ github.sha }}"
          fail-build: true
          severity-cutoff: high
```

### 2. Supply Chain Security

```yaml
# .github/workflows/supply-chain-security.yml
name: Supply Chain Security

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  dependency-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Dependency Review
        uses: actions/dependency-review-action@v3
        with:
          fail-on-severity: moderate
          deny-licenses: GPL-3.0, AGPL-3.0
          
      - name: Generate SBOM
        uses: anchore/sbom-action@v0
        with:
          artifact-name: sbom.spdx.json
          format: spdx-json
          
      - name: SLSA Provenance
        uses: slsa-framework/slsa-github-generator@v1.9.0
        with:
          subjects: |
            dist/*.js
            dist/*.tar.gz
```

## Best Practices

### 1. Security Configuration Standards

```yaml
# .github/security-standards.yml
security-standards:
  dependencies:
    auto-merge-security-updates: true
    max-severity-for-auto-merge: moderate
    update-frequency: daily
    
  code-scanning:
    languages: [javascript, typescript, python, dockerfile]
    scan-frequency: daily
    block-pr-on-high-severity: true
    
  secrets:
    scan-push-protection: true
    custom-patterns: true
    revoke-exposed-tokens: true
    
  policies:
    require-2fa: true
    signed-commits: recommended
    security-policy-file: required
    vulnerability-disclosure: 90-days
```

### 2. Security Checklist for PRs

```markdown
<!-- .github/pull_request_template.md -->
## Security Checklist

- [ ] No hardcoded secrets or credentials
- [ ] Input validation implemented for all user inputs
- [ ] SQL queries use parameterized statements
- [ ] API endpoints have proper authentication
- [ ] Sensitive data is encrypted at rest
- [ ] No sensitive data in logs
- [ ] Dependencies scanned for vulnerabilities
- [ ] Security tests added/updated

### For Maritime Data Changes:
- [ ] Vessel identifiers (IMO, MMSI) are properly masked
- [ ] Policy data access is role-based
- [ ] Risk calculations are not exposed in client code
- [ ] Geolocation data is access-controlled
```

### 3. Security Training Resources

```yaml
# .github/security-training.yml
security-training:
  onboarding:
    - course: "GitHub Security Features"
      url: "https://lab.github.com/githubtraining/security"
      required: true
      
    - course: "OWASP Top 10"
      url: "https://owasp.org/www-project-top-ten/"
      required: true
      
  maritime-specific:
    - course: "Maritime Cybersecurity"
      topics:
        - "Vessel tracking data protection"
        - "Insurance data compliance"
        - "Port system integrations"
      
  continuous-education:
    - monthly-security-workshop: true
    - security-champion-program: true
    - bug-bounty-participation: encouraged
```

## Pricing and Licensing

### GitHub Security Features Availability

| Feature | Free/Pro/Team | Enterprise | GitHub Advanced Security |
|---------|---------------|------------|-------------------------|
| Dependency graph | ✓ | ✓ | ✓ |
| Dependabot alerts | ✓ | ✓ | ✓ |
| Dependabot updates | ✓ | ✓ | ✓ |
| Secret scanning (public repos) | ✓ | ✓ | ✓ |
| Secret scanning (private repos) | ✗ | ✗ | ✓ |
| Code scanning | ✓ (public) | ✗ | ✓ |
| Security overview | ✗ | ✗ | ✓ |

### Cost Considerations

- **GitHub Advanced Security**: $49/user/month for private repositories
- **Free tier**: Sufficient for public repositories and basic security
- **ROI for Maritime Insurance**: 
  - Prevents data breaches (average cost: $4.88M)
  - Ensures compliance with maritime regulations
  - Reduces security audit costs by 60%

## Compliance and Audit

### 1. Audit Trail Configuration

```yaml
# .github/workflows/security-audit.yml
name: Security Audit Trail

on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly
  workflow_dispatch:

jobs:
  generate-audit-report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Generate Security Report
        run: |
          # Collect security metrics
          echo "# Security Audit Report - $(date)" > security-audit.md
          echo "## Dependency Vulnerabilities" >> security-audit.md
          npm audit --json | jq '.metadata.vulnerabilities' >> security-audit.md
          
          echo "## Code Scanning Results" >> security-audit.md
          gh api /repos/${{ github.repository }}/code-scanning/alerts \
            --jq '.[] | {rule_description, state, created_at}' >> security-audit.md
          
          echo "## Secret Scanning Results" >> security-audit.md
          gh api /repos/${{ github.repository }}/secret-scanning/alerts \
            --jq '.[] | {secret_type, state, created_at}' >> security-audit.md
      
      - name: Upload Audit Report
        uses: actions/upload-artifact@v3
        with:
          name: security-audit-${{ github.run_id }}
          path: security-audit.md
          retention-days: 90
```

### 2. Compliance Reporting

```python
# scripts/generate_compliance_report.py
import json
import datetime
from github import Github

def generate_compliance_report(repo_name, token):
    g = Github(token)
    repo = g.get_repo(repo_name)
    
    report = {
        "report_date": datetime.datetime.now().isoformat(),
        "repository": repo_name,
        "compliance_status": {
            "iso_27001": check_iso_27001_compliance(repo),
            "gdpr": check_gdpr_compliance(repo),
            "maritime_cyber": check_maritime_cyber_compliance(repo)
        },
        "security_metrics": {
            "open_vulnerabilities": count_open_vulnerabilities(repo),
            "mean_time_to_remediate": calculate_mttr(repo),
            "security_coverage": calculate_security_coverage(repo)
        }
    }
    
    return report

def check_maritime_cyber_compliance(repo):
    """Check compliance with IMO Maritime Cyber Risk Management"""
    checks = {
        "access_control": check_branch_protection(repo),
        "incident_response": check_security_policy(repo),
        "network_security": check_dependency_scanning(repo),
        "data_protection": check_secret_scanning(repo)
    }
    
    return {
        "compliant": all(checks.values()),
        "details": checks
    }
```

## Integration Examples

### 1. Slack Security Notifications

```yaml
# .github/workflows/security-notifications.yml
name: Security Notifications

on:
  security_advisory:
    types: [published]
  workflow_run:
    workflows: ["CodeQL Security Analysis"]
    types: [completed]

jobs:
  notify:
    runs-on: ubuntu-latest
    steps:
      - name: Send Slack Notification
        uses: 8398a7/action-slack@v3
        with:
          status: ${{ job.status }}
          text: |
            Security Alert: ${{ github.event_name }}
            Repository: ${{ github.repository }}
            Severity: ${{ github.event.security_advisory.severity }}
          webhook_url: ${{ secrets.SLACK_SECURITY_WEBHOOK }}
```

### 2. JIRA Security Issue Creation

```javascript
// scripts/create-security-issue.js
const { Octokit } = require("@octokit/rest");
const JiraClient = require("jira-connector");

async function createSecurityIssue(vulnerability) {
  const jira = new JiraClient({
    host: process.env.JIRA_HOST,
    basic_auth: {
      email: process.env.JIRA_EMAIL,
      api_token: process.env.JIRA_TOKEN
    }
  });
  
  const issue = {
    fields: {
      project: { key: "MARSEC" },
      summary: `Security: ${vulnerability.rule.description}`,
      description: {
        type: "doc",
        version: 1,
        content: [{
          type: "paragraph",
          content: [{
            type: "text",
            text: `Vulnerability detected in ${vulnerability.location.path}`
          }]
        }]
      },
      issuetype: { name: "Security Vulnerability" },
      priority: mapSeverityToPriority(vulnerability.rule.severity),
      labels: ["security", "automated", "github-scanning"],
      components: [{ name: "Maritime Platform" }]
    }
  };
  
  return await jira.issue.createIssue(issue);
}

function mapSeverityToPriority(severity) {
  const mapping = {
    "critical": { name: "Critical" },
    "high": { name: "High" },
    "medium": { name: "Medium" },
    "low": { name: "Low" }
  };
  return mapping[severity.toLowerCase()] || { name: "Medium" };
}
```

## Conclusion

GitHub's security features provide comprehensive protection for maritime insurance applications, from code to deployment. By implementing these configurations and best practices, teams can ensure their applications meet security requirements while maintaining development velocity. The combination of automated scanning, dependency management, and secret protection creates a robust security posture essential for handling sensitive maritime and insurance data.