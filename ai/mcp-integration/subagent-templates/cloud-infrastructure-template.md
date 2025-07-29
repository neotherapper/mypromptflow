# Cloud Infrastructure MCP Integration Template

Specialized template for integrating cloud infrastructure MCP servers (AWS, Azure, GCP) into AI subagents focused on system architecture, DevOps, and cloud platform management.

## Core Integration Pattern for Cloud Infrastructure Subagents

### MCP Server Integration Section (Add to Core Responsibilities)

```markdown
**Cloud Infrastructure MCP Integration:**
- Leverage AWS/Azure/GCP MCP servers for real-time infrastructure intelligence and optimization
- Query current service availability, pricing, and regional capabilities
- Validate architecture recommendations against current cloud platform constraints
- Monitor resource utilization and provide cost optimization strategies
- Access latest security best practices and compliance requirements
- Implement infrastructure as code validation with current platform capabilities
- Provide fallback to cached cloud knowledge when MCP servers unavailable
```

## AWS MCP Server Integration

### Configuration Example
```yaml
# Add to subagent frontmatter
tools: Read, Grep, Glob, WebSearch, mcp__AWS__describe_instances, mcp__AWS__list_s3_buckets, mcp__AWS__get_cost_and_usage, mcp__AWS__describe_vpcs, mcp__AWS__get_security_groups
```

### Implementation Pattern
```markdown
## AWS MCP Server Integration

### Primary MCP Server: AWS (Amazon Web Services)
- **Tier Level**: Tier 2 Strategic (6.4/10)
- **Setup Complexity**: High
- **Integration Priority**: High for Cloud Architecture

### Core AWS Integration Capabilities:
- Real-time EC2 instance status and capacity planning
- S3 bucket management and cost optimization
- VPC networking configuration and security validation  
- CloudFormation stack status and resource dependencies
- Cost monitoring and budget optimization recommendations
- Security group and IAM policy validation
- Auto-scaling configuration and performance metrics

### Usage Patterns:

1. **Infrastructure Assessment and Planning**:
   ```python
   async def validate_infrastructure_design(architecture_spec):
       try:
           # Get current AWS service limits and availability
           regions = await mcp_aws.describe_regions()
           instance_types = await mcp_aws.describe_instance_types(architecture_spec.region)
           
           # Validate against current capabilities
           validation_result = {
               "region_availability": check_region_support(regions, architecture_spec.region),
               "instance_capacity": validate_instance_requirements(instance_types, architecture_spec.compute),
               "service_limits": await mcp_aws.describe_account_limits(),
               "cost_estimate": await mcp_aws.estimate_costs(architecture_spec)
           }
           
           return create_architecture_recommendations(validation_result)
           
       except AWSMCPError as e:
           # Fallback to cached AWS knowledge
           return validate_with_cached_knowledge(architecture_spec, error=e)
   ```

2. **Cost Optimization and Monitoring**:
   ```python
   async def analyze_cost_optimization(current_infrastructure):
       try:
           # Get real-time cost and usage data
           cost_data = await mcp_aws.get_cost_and_usage(timeframe="30_days")
           utilization = await mcp_aws.get_rightsizing_recommendations()
           
           optimization_opportunities = {
               "underutilized_instances": identify_underutilized_resources(utilization),
               "reserved_instance_opportunities": calculate_ri_savings(cost_data),
               "storage_optimization": analyze_storage_usage(cost_data),
               "network_optimization": analyze_data_transfer_costs(cost_data)
           }
           
           return generate_cost_optimization_plan(optimization_opportunities)
           
       except AWSMCPError as e:
           return provide_general_cost_optimization_guidance(error=e)
   ```

3. **Security and Compliance Validation**:
   ```python
   async def validate_security_configuration(infrastructure_config):
       try:
           # Real-time security posture assessment
           security_groups = await mcp_aws.describe_security_groups()
           iam_policies = await mcp_aws.get_account_authorization_details()
           compliance_status = await mcp_aws.get_compliance_summary()
           
           security_assessment = {
               "network_security": analyze_security_groups(security_groups),
               "access_controls": validate_iam_policies(iam_policies),
               "compliance_gaps": identify_compliance_issues(compliance_status),
               "encryption_status": check_encryption_configuration(infrastructure_config)
           }
           
           return create_security_recommendations(security_assessment)
           
       except AWSMCPError as e:
           return provide_security_best_practices_guidance(error=e)
   ```

### Error Handling and Fallback Strategy:
```python
class AWSMCPIntegration:
    def __init__(self):
        self.circuit_breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=300)
        self.cache_ttl = 1800  # 30 minutes for AWS data
        
    async def query_with_fallback(self, operation, params):
        if self.circuit_breaker.is_open():
            return self.get_cached_aws_knowledge(operation, params)
            
        try:
            result = await self.circuit_breaker.call(
                self.aws_mcp_client.execute, operation, params
            )
            self.cache_result(operation, params, result)
            return self.enhance_with_expertise(result)
            
        except Exception as e:
            self.log_integration_error(operation, e)
            return self.get_cached_aws_knowledge(operation, params, error=e)
```
```

## Azure MCP Server Integration

### Configuration Example
```yaml
# Add to subagent frontmatter  
tools: Read, Grep, Glob, WebSearch, mcp__AZURE__list_resource_groups, mcp__AZURE__get_vm_sizes, mcp__AZURE__monitor_metrics
```

### Implementation Pattern
```markdown
## Azure MCP Server Integration

### Primary MCP Server: Microsoft Azure
- **Tier Level**: Tier 2 Strategic (6.8/10)
- **Setup Complexity**: High
- **Integration Priority**: High for Enterprise Integration

### Core Azure Integration Capabilities:
- Resource group management and organization strategies
- Virtual machine sizing and performance optimization
- Azure Monitor metrics and alerting configuration
- Subscription limits and quota management
- Cost management and billing optimization
- Active Directory integration and security policies

### Usage Patterns:

1. **Resource Management and Optimization**:
   - Query current resource group configurations
   - Validate VM sizing against workload requirements
   - Monitor resource utilization and performance metrics
   - Optimize subscription management and organization

2. **Enterprise Integration Planning**:
   - Assess Active Directory integration capabilities
   - Validate hybrid cloud connectivity options
   - Plan for enterprise security and compliance requirements
   - Optimize for Microsoft ecosystem integration
```

## GCP MCP Server Integration

### Configuration Example  
```yaml
# Add to subagent frontmatter
tools: Read, Grep, Glob, WebSearch, mcp__GCP__list_projects, mcp__GCP__get_compute_instances, mcp__GCP__billing_account_info
```

### Implementation Pattern
```markdown
## GCP MCP Server Integration

### Primary MCP Server: Google Cloud Platform
- **Tier Level**: Tier 2 Strategic (6.6/10)
- **Setup Complexity**: High  
- **Integration Priority**: High for Data/AI Workloads

### Core GCP Integration Capabilities:
- Project management and organization structure
- Compute Engine instance optimization
- BigQuery data warehouse planning
- AI/ML service integration (Vertex AI, AutoML)
- Kubernetes Engine configuration and management
- Cost optimization and billing analysis

### Usage Patterns:

1. **Data Platform Architecture**:
   - Design BigQuery data warehouse solutions
   - Plan AI/ML model deployment strategies
   - Optimize data pipeline architectures
   - Validate data governance and security models

2. **Kubernetes and Container Orchestration**:
   - Plan GKE cluster configurations
   - Optimize container resource allocation
   - Design service mesh architectures
   - Implement monitoring and observability solutions
```

## Multi-Cloud Integration Strategy

### Cross-Platform Recommendations
```markdown
**Multi-Cloud MCP Integration:**
- Leverage multiple cloud MCP servers for hybrid and multi-cloud architectures
- Compare service capabilities and pricing across platforms
- Validate vendor-neutral architecture decisions
- Implement cloud-agnostic monitoring and management strategies
- Plan for data portability and disaster recovery across clouds
- Optimize costs through strategic workload placement
```

### Implementation Example
```python
async def multi_cloud_architecture_analysis(requirements):
    """Analyze requirements across multiple cloud platforms"""
    try:
        # Query all available cloud MCPs
        aws_capabilities = await mcp_aws.get_service_capabilities(requirements)
        azure_capabilities = await mcp_azure.get_service_capabilities(requirements)  
        gcp_capabilities = await mcp_gcp.get_service_capabilities(requirements)
        
        # Compare and recommend optimal platform mix
        recommendation = {
            "primary_cloud": determine_primary_platform(aws_capabilities, azure_capabilities, gcp_capabilities),
            "workload_distribution": optimize_workload_placement(requirements),
            "cost_comparison": calculate_multi_cloud_costs(aws_capabilities, azure_capabilities, gcp_capabilities),
            "risk_assessment": analyze_vendor_dependency_risks()
        }
        
        return create_multi_cloud_strategy(recommendation)
        
    except Exception as e:
        return provide_multi_cloud_best_practices(error=e)
```

## Integration Quality Standards

### Performance Requirements
- **Response Time**: < 5 seconds for infrastructure queries
- **Cache Hit Rate**: > 80% for repeated architectural assessments  
- **Error Rate**: < 3% for MCP server interactions
- **Fallback Success**: > 95% successful fallback to cached knowledge

### Monitoring and Alerting
- Track cloud MCP server availability and response times
- Monitor cost estimation accuracy against actual usage
- Alert on significant pricing or service capability changes
- Log integration usage patterns for optimization

### Security and Compliance
- Encrypt all cloud platform credentials and API keys
- Implement least-privilege access for cloud MCP servers
- Regular audit of cloud platform permissions and access
- Compliance validation for industry-specific requirements

This cloud infrastructure template ensures subagents can leverage real-time cloud platform intelligence while maintaining reliability and performance standards.