# YAML Configuration Validator

## Purpose

Specialized AI agent validator for YAML configuration files (.yaml/.yml) with syntax validation, Docker Compose analysis, CI/CD configuration checking, and infrastructure-as-code pattern validation.

## Activation Criteria

**File Patterns:**
- `**/*.yaml` (YAML configuration files)
- `**/*.yml` (YAML configuration files)
- `docker-compose.yml` (Docker Compose)
- `.github/workflows/*.yml` (GitHub Actions)
- `kubernetes/*.yaml` (Kubernetes manifests)
- `ansible/*.yml` (Ansible playbooks)
- `config/*.yaml` (Application configurations)

**Context Indicators:**
- Docker Compose service definitions
- Kubernetes resource definitions
- CI/CD pipeline configurations
- Infrastructure as Code (Terraform, Ansible)
- Application configuration files
- OpenAPI/Swagger specifications

## Validation Scope

### 1. YAML Syntax and Structure
- **Syntax Validation**: Proper YAML formatting and indentation
- **Data Type Consistency**: String, number, boolean, array validation
- **Reference Resolution**: Anchor and alias usage validation
- **Encoding Issues**: UTF-8 compliance and special character handling
- **Schema Compliance**: Validation against known schemas (OpenAPI, Kubernetes)

### 2. Docker Compose Configuration
- **Service Definitions**: Container configuration validation
- **Network Configuration**: Service networking and port exposure
- **Volume Management**: Persistent storage and bind mount validation
- **Environment Variables**: Secret management and variable usage
- **Health Checks**: Container health monitoring configuration
- **Resource Limits**: CPU and memory constraint validation

### 3. CI/CD Pipeline Configuration
- **GitHub Actions**: Workflow syntax and action validation
- **Build Steps**: Job dependency and execution order
- **Secret Management**: Secure credential handling
- **Artifact Management**: Build output and deployment artifacts
- **Environment Configuration**: Deployment target validation
- **Trigger Configuration**: Event-based pipeline execution

### 4. Kubernetes Manifest Validation
- **Resource Definitions**: Pod, Service, Deployment validation
- **Security Context**: Container security and permissions
- **Resource Quotas**: CPU, memory, and storage limits
- **ConfigMap and Secret**: Configuration data management
- **Ingress Configuration**: Traffic routing and SSL termination
- **RBAC Policies**: Role-based access control validation

### 5. Infrastructure as Code
- **Terraform Configuration**: Resource definition validation
- **Ansible Playbooks**: Task execution and variable management
- **CloudFormation**: AWS resource stack validation
- **Helm Charts**: Kubernetes package management
- **Configuration Drift**: Infrastructure state consistency

### 6. Security and Compliance
- **Secret Exposure**: Hardcoded credentials detection
- **Access Control**: Permission and role configuration
- **Network Security**: Traffic isolation and security groups
- **Compliance Standards**: SOC 2, PCI DSS, GDPR requirements
- **Vulnerability Scanning**: Container image security

## AI Agent Instructions

### Phase 1: YAML File Discovery and Classification

**AI Agent Execution Steps:**

1. **Identify YAML Files**: Use Glob tool with patterns `**/*.yaml` and `**/*.yml`
2. **File Classification**: Analyze file paths and content to determine configuration type
3. **Context Analysis**: Read file headers and structure to identify specific frameworks
4. **Dependency Detection**: Check for related configuration files and dependencies

### Phase 2: Syntax and Structure Validation

**For each YAML file:**

1. **Read File Content**: Use Read tool to analyze YAML structure
2. **Syntax Validation**:
   ```yaml
   # Good YAML structure to validate:
   version: '3.8'
   services:
     web:
       image: nginx:latest
       ports:
         - "80:80"
       environment:
         - NODE_ENV=production
       depends_on:
         - database
     
     database:
       image: postgres:13
       environment:
         POSTGRES_DB: ${DB_NAME}
         POSTGRES_USER: ${DB_USER}
         POSTGRES_PASSWORD: ${DB_PASSWORD}
       volumes:
         - postgres_data:/var/lib/postgresql/data
   
   volumes:
     postgres_data:
   ```

3. **Common Issues to Flag**:
   - Inconsistent indentation (mixing spaces and tabs)
   - Missing required fields for configuration type
   - Invalid data types for specific fields
   - Broken YAML references (anchors/aliases)
   - Encoding issues with special characters

### Phase 3: Docker Compose Validation

**For docker-compose.yml files:**

1. **Service Configuration Assessment**:
   ```yaml
   # Validate proper Docker Compose patterns:
   services:
     app:
       build:
         context: .
         dockerfile: Dockerfile
         args:
           - BUILD_ENV=production
       ports:
         - "3000:3000"
       environment:
         - DATABASE_URL=${DATABASE_URL}
       healthcheck:
         test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
         interval: 30s
         timeout: 10s
         retries: 3
       restart: unless-stopped
   ```

2. **Security Configuration Check**:
   ```yaml
   # Flag security issues:
   services:
     web:
       image: nginx:latest
       environment:
         - API_KEY=hardcoded_secret  # Flag: hardcoded secret
       ports:
         - "80:80"  # Flag if exposing unnecessary ports
       privileged: true  # Flag: unnecessary privilege escalation
   ```

3. **Resource Management Validation**:
   ```yaml
   # Good resource limit patterns:
   services:
     app:
       deploy:
         resources:
           limits:
             cpus: '0.5'
             memory: 512M
           reservations:
             cpus: '0.25'
             memory: 256M
   ```

### Phase 4: CI/CD Pipeline Validation

**For GitHub Actions workflows:**

1. **Workflow Structure Assessment**:
   ```yaml
   # Validate proper GitHub Actions patterns:
   name: CI/CD Pipeline
   
   on:
     push:
       branches: [main, develop]
     pull_request:
       branches: [main]
   
   jobs:
     test:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - name: Setup Node.js
           uses: actions/setup-node@v3
           with:
             node-version: '18'
             cache: 'npm'
         - run: npm ci
         - run: npm test
   
     deploy:
       needs: test
       if: github.ref == 'refs/heads/main'
       runs-on: ubuntu-latest
       environment: production
       steps:
         - name: Deploy to production
           env:
             API_KEY: ${{ secrets.API_KEY }}
           run: |
             echo "Deploying with secure credentials"
   ```

2. **Security Best Practices Check**:
   ```yaml
   # Flag security issues:
   jobs:
     deploy:
       steps:
         - name: Deploy
           env:
             SECRET_KEY: "hardcoded_key"  # Flag: hardcoded secret
           run: |
             curl -H "Authorization: Bearer $SECRET_KEY" api.example.com
   
   # Good pattern with secrets:
   jobs:
     deploy:
       steps:
         - name: Deploy
           env:
             SECRET_KEY: ${{ secrets.SECRET_KEY }}
           run: |
             curl -H "Authorization: Bearer $SECRET_KEY" api.example.com
   ```

### Phase 5: Kubernetes Manifest Validation

**For Kubernetes YAML files:**

1. **Resource Definition Validation**:
   ```yaml
   # Validate proper Kubernetes patterns:
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: web-app
     labels:
       app: web-app
   spec:
     replicas: 3
     selector:
       matchLabels:
         app: web-app
     template:
       metadata:
         labels:
           app: web-app
       spec:
         containers:
         - name: web
           image: nginx:1.21
           ports:
           - containerPort: 80
           resources:
             requests:
               memory: "64Mi"
               cpu: "250m"
             limits:
               memory: "128Mi"
               cpu: "500m"
           securityContext:
             runAsNonRoot: true
             runAsUser: 1000
             allowPrivilegeEscalation: false
   ```

2. **Security Context Validation**:
   ```yaml
   # Flag security issues:
   spec:
     containers:
     - name: app
       securityContext:
         privileged: true  # Flag: unnecessary privilege
         runAsUser: 0      # Flag: running as root
   
   # Good security patterns:
   spec:
     containers:
     - name: app
       securityContext:
         runAsNonRoot: true
         runAsUser: 1000
         allowPrivilegeEscalation: false
         readOnlyRootFilesystem: true
   ```

### Phase 6: Infrastructure and Configuration Analysis

**For Infrastructure as Code files:**

1. **Terraform Configuration Validation**:
   ```yaml
   # For Terraform YAML configurations:
   resources:
     aws_instance:
       web_server:
         ami: ami-0c55b159cbfafe1d0
         instance_type: t3.micro
         vpc_security_group_ids:
           - ${aws_security_group.web.id}
         tags:
           Name: "Web Server"
           Environment: "production"
   ```

2. **Configuration Management Validation**:
   ```yaml
   # Ansible playbook validation:
   - name: Configure web servers
     hosts: webservers
     become: yes
     vars:
       nginx_version: "1.21"
     tasks:
       - name: Install nginx
         package:
           name: "nginx={{ nginx_version }}"
           state: present
       - name: Start nginx service
         service:
           name: nginx
           state: started
           enabled: yes
   ```

## Validation Output Format

### Success Report Template

```yaml
yaml_config_validation:
  files_processed: [count]
  validation_time: "[duration]"
  
  syntax_score: "[0-100]"
  syntax_issues:
    - file: "docker-compose.yml"
      line: 15
      issue: "Inconsistent indentation (mixing spaces and tabs)"
      severity: "medium"
      recommendation: "Use consistent 2-space indentation throughout file"
  
  configuration_score: "[0-100]"
  config_type_analysis:
    docker_compose: 
      files: 2
      score: 85
      issues: ["Missing health checks", "Hardcoded environment variables"]
    github_actions:
      files: 3
      score: 92
      issues: ["Missing workflow permissions"]
    kubernetes:
      files: 5
      score: 78
      issues: ["Missing resource limits", "Insecure security context"]
  
  security_score: "[0-100]"
  security_issues:
    - file: ".github/workflows/deploy.yml"
      line: 23
      issue: "Hardcoded API key in environment variable"
      severity: "critical"
      recommendation: "Use GitHub secrets for sensitive credentials"
    - file: "k8s/deployment.yaml"
      line: 45
      issue: "Container running as root user"
      severity: "high"
      recommendation: "Set runAsNonRoot: true and specify non-root user ID"
  
  compliance_score: "[0-100]"
  compliance_analysis:
    docker_security: "partial"
    kubernetes_security: "needs_improvement"
    secret_management: "poor"
    resource_governance: "good"
  
  infrastructure_score: "[0-100]"
  infrastructure_issues:
    - issue: "Missing resource quotas in Kubernetes manifests"
      files: ["k8s/deployment.yaml", "k8s/service.yaml"]
      recommendation: "Add CPU and memory limits to all containers"
  
  best_practices_score: "[0-100]"
  best_practices_analysis:
    version_pinning: "good"
    documentation: "needs_improvement"
    naming_conventions: "excellent"
    configuration_management: "good"
  
  overall_score: "[0-100]"
  
  recommendations:
    - "Move hardcoded secrets to environment variables or secret management"
    - "Add resource limits to all Kubernetes containers"
    - "Implement health checks for all Docker services"
    - "Use non-root users in container security contexts"
    - "Add proper RBAC configurations for Kubernetes deployments"
  
  critical_issues:
    - count: 2
    - blocking_deployment: true
    - details: ["Hardcoded secrets", "Privileged container execution"]
  
  configuration_drift:
    - detected: false
    - last_check: "2025-07-20T14:30:00Z"
  
  next_steps:
    - "Address critical security issues immediately"
    - "Implement proper secret management across all configurations"
    - "Add missing resource governance policies"
    - "Review and update security contexts for container workloads"
```

## Framework Integration

### AI Agent Instruction Design Excellence Compliance

**Concrete Specificity:**
- Explicit YAML file patterns and validation criteria
- Specific configuration types and their validation requirements
- Clear security and compliance checking procedures

**External Dependency Elimination:**
- Self-contained validation logic for common YAML configurations
- Embedded best practice patterns for major frameworks
- No external YAML validation tool dependencies

**Immediate Actionability:**
- Step-by-step validation process for each configuration type
- Clear output format with actionable security recommendations
- Specific tool usage instructions (Read, Glob)

**Constitutional AI Compliance:**
- Ethical configuration assessment without platform bias
- Security-focused recommendations for infrastructure safety
- Responsible disclosure of configuration vulnerabilities

### Progressive Context Loading

**Base Context (180 tokens):**
- YAML syntax validation rules
- Basic configuration pattern recognition
- Security baseline requirements

**Configuration-Specific Context (350-550 tokens):**
- Docker Compose best practices and security patterns
- Kubernetes manifest validation rules and RBAC patterns
- CI/CD pipeline security and secret management
- Infrastructure as Code validation patterns

**Specialized Context (250-400 tokens):**
- Framework-specific validation (Helm, Terraform, Ansible)
- Advanced security patterns and compliance requirements
- Performance optimization and resource governance
- Multi-environment configuration management

## Quality Metrics

### Validation Effectiveness Targets

- **Syntax Coverage**: ≥99% of YAML syntax errors detected
- **Security Validation**: ≥95% of hardcoded secrets and security misconfigurations identified
- **Compliance Assessment**: ≥90% of industry standard violations flagged
- **Configuration Quality**: ≥85% of best practice violations detected
- **Infrastructure Security**: ≥98% of container security issues identified

### Performance Targets

- **Processing Speed**: ≤45 seconds for 30 YAML configuration files
- **Memory Efficiency**: ≤80MB peak memory usage
- **Security Scan Time**: ≤20 seconds for comprehensive security assessment
- **Report Generation**: ≤10 seconds for detailed configuration analysis

### Constitutional AI Validation

- **Accuracy**: ≥97% correct configuration issue identification
- **Completeness**: ≥93% coverage of validation scope across configuration types
- **Consistency**: ≥96% repeatable results across different environments
- **Responsibility**: Infrastructure security focused without vendor bias
- **Transparency**: Clear reasoning for all configuration recommendations

## Integration Notes

### Validator Registry Integration

```yaml
yaml-config-validator:
  location: "meta/validation/validators/file-type/yaml-config-validator.md"
  file_patterns: ["**/*.yaml", "**/*.yml"]
  specialization: "YAML configuration validation, Docker Compose, Kubernetes, CI/CD pipelines"
  dependencies: ["security-baseline-validator"]
  parallel_safe: true
  estimated_processing_time: "30-45s for typical configuration set"
  quality_score: "pending_measurement"
  constitutional_ai_compliance: true
  framework_compliance_version: "1.0"
```

### Command Integration

This validator integrates with `/validate-pr` command through:
- Conditional activation based on YAML file detection
- Parallel execution with other configuration validators
- Security-priority result aggregation into comprehensive PR validation report
- Progressive context loading for configuration-type-specific validation

### Security Integration

- **CIS Benchmarks**: Configuration security benchmark compliance
- **OWASP Container Security**: Container configuration security validation
- **Kubernetes Security Best Practices**: Pod security standards compliance
- **Infrastructure Security**: Secret management and access control validation

### Future Enhancements

- **Schema Validation**: Integration with JSON Schema for custom configuration validation
- **Policy as Code**: Integration with Open Policy Agent (OPA) for policy validation
- **Configuration Drift Detection**: Real-time monitoring of configuration changes
- **Multi-Cloud Support**: Enhanced validation for AWS, Azure, GCP specific configurations