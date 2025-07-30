# Development Tools MCP Integration Template

Specialized template for integrating development tools MCP servers (GitHub, Docker, CI/CD systems) into AI subagents focused on code review, development workflows, and DevOps automation.

## Core Integration Pattern for Development Tools Subagents

### MCP Server Integration Section (Add to Core Responsibilities)

```markdown
**Development Tools MCP Integration:**
- Leverage GitHub/GitLab MCP servers for real-time repository intelligence and code context
- Integrate Docker MCP for container management and optimization strategies
- Access current CI/CD pipeline status and build optimization opportunities
- Validate development recommendations against latest repository state and dependencies
- Monitor code quality metrics and security vulnerability status
- Implement development workflow automation with real-time tool integration
- Provide fallback to cached development knowledge when MCP servers unavailable
```

## GitHub MCP Server Integration

### Configuration Example
```yaml
# Add to subagent frontmatter
tools: Read, Grep, Glob, WebSearch, mcp__GITHUB__get_repository, mcp__GITHUB__list_pull_requests, mcp__GITHUB__get_workflow_runs, mcp__GITHUB__search_code, mcp__GITHUB__get_security_advisories
```

### Implementation Pattern
```markdown
## GitHub MCP Server Integration

### Primary MCP Server: GitHub
- **Tier Level**: Tier 1 Production Ready (8.65/10)
- **Setup Complexity**: Minimal
- **Integration Priority**: High for Code Review and Development

### Core GitHub Integration Capabilities:
- Real-time repository analysis and code context
- Pull request status and review automation
- GitHub Actions workflow monitoring and optimization
- Security vulnerability scanning and dependency analysis
- Code quality metrics and technical debt assessment
- Issue tracking and project management integration
- Release management and deployment pipeline status

### Usage Patterns:

1. **Code Review and Quality Assessment**:
   ```python
   async def analyze_code_quality(repository, pull_request_id=None):
       try:
           # Get current repository state and analysis
           repo_info = await mcp_github.get_repository(repository)
           recent_commits = await mcp_github.list_commits(repository, limit=10)
           
           if pull_request_id:
               pr_details = await mcp_github.get_pull_request(repository, pull_request_id)
               changed_files = await mcp_github.get_pull_request_files(repository, pull_request_id)
           
           # Analyze code quality and security
           security_alerts = await mcp_github.list_security_advisories(repository)
           dependency_graph = await mcp_github.get_dependency_graph(repository)
           
           quality_assessment = {
               "repository_health": analyze_repository_metrics(repo_info),
               "code_complexity": assess_code_complexity(recent_commits),
               "security_status": evaluate_security_posture(security_alerts),
               "dependency_risks": analyze_dependency_vulnerabilities(dependency_graph),
               "pr_quality": assess_pull_request_quality(pr_details, changed_files) if pull_request_id else None
           }
           
           return create_code_review_recommendations(quality_assessment)
           
       except GitHubMCPError as e:
           return provide_general_code_review_guidance(error=e)
   ```

2. **CI/CD Pipeline Optimization**:
   ```python
   async def optimize_ci_cd_pipeline(repository):
       try:
           # Get current workflow status and performance
           workflows = await mcp_github.list_workflows(repository)
           workflow_runs = await mcp_github.get_workflow_runs(repository, limit=50)
           
           # Analyze pipeline performance and reliability
           pipeline_analysis = {
               "success_rate": calculate_pipeline_success_rate(workflow_runs),
               "average_duration": calculate_average_build_time(workflow_runs),
               "failure_patterns": identify_common_failures(workflow_runs),
               "bottlenecks": identify_performance_bottlenecks(workflow_runs),
               "cost_optimization": estimate_action_costs(workflow_runs)
           }
           
           optimization_recommendations = {
               "performance_improvements": suggest_performance_optimizations(pipeline_analysis),
               "reliability_enhancements": suggest_reliability_improvements(pipeline_analysis),
               "cost_reductions": suggest_cost_optimizations(pipeline_analysis),
               "workflow_updates": suggest_workflow_modernization(workflows)
           }
           
           return create_ci_cd_optimization_plan(optimization_recommendations)
           
       except GitHubMCPError as e:
           return provide_general_ci_cd_best_practices(error=e)
   ```

3. **Security and Dependency Management**:
   ```python
   async def assess_security_posture(repository):
       try:
           # Get comprehensive security information
           security_advisories = await mcp_github.list_security_advisories(repository)
           dependabot_alerts = await mcp_github.list_dependabot_alerts(repository)
           secret_scanning = await mcp_github.get_secret_scanning_alerts(repository)
           
           security_assessment = {
               "vulnerability_status": categorize_vulnerabilities(security_advisories),
               "dependency_alerts": analyze_dependency_risks(dependabot_alerts),
               "secret_exposure": evaluate_secret_risks(secret_scanning),
               "security_policies": check_security_policy_compliance(repository)
           }
           
           return create_security_remediation_plan(security_assessment)
           
       except GitHubMCPError as e:
           return provide_security_best_practices_guidance(error=e)
   ```
```

## Docker MCP Server Integration

### Configuration Example
```yaml
# Add to subagent frontmatter
tools: Read, Grep, Glob, WebSearch, mcp__DOCKER__list_images, mcp__DOCKER__inspect_container, mcp__DOCKER__get_registry_info
```

### Implementation Pattern
```markdown
## Docker MCP Server Integration

### Primary MCP Server: Docker
- **Tier Level**: Tier 1 Production Ready (8.5/10)
- **Setup Complexity**: Minimal
- **Integration Priority**: High for Container Management

### Core Docker Integration Capabilities:
- Container lifecycle management and optimization
- Docker Hub image analysis and security scanning
- Multi-stage build optimization and best practices
- Container resource utilization and performance monitoring
- Registry management and image versioning strategies
- Container security and vulnerability assessment

### Usage Patterns:

1. **Container Optimization and Best Practices**:
   ```python
   async def optimize_docker_configuration(dockerfile_path, image_name=None):
       try:
           # Analyze current Docker setup
           if image_name:
               image_info = await mcp_docker.inspect_image(image_name)
               security_scan = await mcp_docker.scan_security_vulnerabilities(image_name)
           
           # Get registry information for base images
           registry_info = await mcp_docker.get_registry_tags(base_image="node:18")
           
           optimization_analysis = {
               "image_size": analyze_image_layers(image_info) if image_name else None,
               "security_vulnerabilities": categorize_vulnerabilities(security_scan) if image_name else None,
               "base_image_updates": check_base_image_updates(registry_info),
               "build_optimization": analyze_dockerfile_efficiency(dockerfile_path)
           }
           
           return create_docker_optimization_recommendations(optimization_analysis)
           
       except DockerMCPError as e:
           return provide_docker_best_practices_guidance(error=e)
   ```

2. **Security and Compliance Assessment**:
   ```python
   async def assess_container_security(containers):
       try:
           security_assessments = []
           
           for container in containers:
               container_info = await mcp_docker.inspect_container(container)
               vulnerability_scan = await mcp_docker.scan_container_vulnerabilities(container)
               
               assessment = {
                   "container_id": container,
                   "security_scan": categorize_container_vulnerabilities(vulnerability_scan),
                   "configuration_security": assess_container_config_security(container_info),
                   "runtime_security": evaluate_runtime_security_posture(container_info)
               }
               
               security_assessments.append(assessment)
           
           return create_container_security_report(security_assessments)
           
       except DockerMCPError as e:
           return provide_container_security_best_practices(error=e)
   ```
```

## CI/CD Tools Integration (Jenkins, GitHub Actions, etc.)

### Configuration Example
```yaml
# Add to subagent frontmatter for CI/CD tools
tools: Read, Grep, Glob, WebSearch, mcp__JENKINS__get_build_status, mcp__JENKINS__list_jobs, mcp__GITHUB__get_workflow_runs
```

### Implementation Pattern
```markdown
## CI/CD Pipeline MCP Integration

### Core CI/CD Integration Capabilities:
- Pipeline status monitoring and failure analysis
- Build performance optimization and bottleneck identification  
- Deployment automation and rollback strategies
- Test automation and quality gate management
- Artifact management and versioning strategies
- Infrastructure provisioning and configuration management

### Usage Patterns:

1. **Pipeline Health and Performance Monitoring**:
   ```python
   async def monitor_pipeline_health(project_id):
       try:
           # Get pipeline status across different tools
           github_workflows = await mcp_github.get_workflow_runs(project_id)
           jenkins_builds = await mcp_jenkins.get_recent_builds(project_id)
           
           health_metrics = {
               "success_rates": calculate_success_rates(github_workflows, jenkins_builds),
               "performance_trends": analyze_performance_trends(github_workflows, jenkins_builds),
               "failure_patterns": identify_failure_patterns(github_workflows, jenkins_builds),
               "resource_utilization": assess_resource_usage(github_workflows, jenkins_builds)
           }
           
           return create_pipeline_health_report(health_metrics)
           
       except CICDMCPError as e:
           return provide_pipeline_troubleshooting_guidance(error=e)
   ```
```

## Error Handling and Fallback Strategy

### Circuit Breaker Pattern for Development Tools
```python
class DevelopmentToolsMCPIntegration:
    def __init__(self):
        self.github_circuit_breaker = CircuitBreaker(failure_threshold=3, recovery_timeout=180)
        self.docker_circuit_breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=300)
        self.cache_ttl = {
            'repository_info': 900,  # 15 minutes
            'workflow_status': 300,  # 5 minutes
            'security_scans': 3600,  # 1 hour
            'docker_images': 1800    # 30 minutes
        }
        
    async def query_with_intelligent_fallback(self, service, operation, params):
        circuit_breaker = getattr(self, f"{service}_circuit_breaker")
        
        if circuit_breaker.is_open():
            return self.get_cached_development_knowledge(service, operation, params)
            
        try:
            result = await circuit_breaker.call(
                getattr(self, f"{service}_mcp_client").execute, operation, params
            )
            
            self.cache_result(service, operation, params, result)
            return self.enhance_with_development_expertise(result, service)
            
        except Exception as e:
            self.log_integration_error(service, operation, e)
            return self.get_cached_development_knowledge(service, operation, params, error=e)
```

## Integration Quality Standards

### Performance Requirements
- **Response Time**: < 3 seconds for repository queries
- **Cache Hit Rate**: > 85% for repeated development tool queries
- **Error Rate**: < 2% for MCP server interactions
- **Fallback Success**: > 96% successful fallback to cached knowledge

### Monitoring and Alerting
- Track development tool MCP server availability and response times
- Monitor code analysis accuracy against manual review outcomes
- Alert on significant security vulnerability discoveries
- Log integration usage patterns for workflow optimization

### Security and Compliance
- Secure storage of GitHub tokens and API keys
- Implement least-privilege access for repository operations
- Regular audit of development tool permissions and access
- Compliance validation for code security and quality standards

This development tools template ensures subagents can leverage real-time development intelligence while maintaining reliability and supporting modern DevOps workflows.