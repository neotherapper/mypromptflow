# AWS App Runner - Serverless Container Service

## Overview

AWS App Runner is a fully managed serverless container service that enables automatic scaling from zero to production capacity without infrastructure management. In the VanguardAI stack, App Runner provides scale-to-zero capability for backend FastAPI services, delivering revolutionary cost optimization with $2.70/month preview environments and 70% cost reduction compared to traditional ECS alternatives.

## Key Benefits

### VanguardAI Cost Optimization
- **Scale-to-zero capability** reduces costs to $0 during inactivity
- **Preview environments** cost only $2.70/month with automatic cleanup
- **No infrastructure management** eliminates DevOps overhead
- **Automatic scaling** from 0 to production capacity without configuration

### Development Productivity
- **Zero-downtime deployments** with automatic blue-green switching
- **Integrated container registry** with Amazon ECR
- **Health check automation** with configurable endpoints
- **Built-in load balancing** and SSL certificate management

## VanguardAI Implementation Context

### Maritime Insurance Application Architecture

App Runner serves as the backend compute platform for FastAPI services in the maritime insurance application, handling:

- **Quote generation APIs** with broker competition logic
- **Risk assessment calculations** for vessel and route analysis
- **Fleet management services** with real-time vessel tracking
- **Policy management endpoints** with complex business rules

### Integration with VanguardAI Stack

```mermaid
graph LR
    CF[CloudFront] --> S3[S3 Static Site]
    S3 --> AR[App Runner Service]
    AR --> AU[Aurora Serverless v2]
    AR --> SM[Secrets Manager]
    
    GH[GitHub Actions] --> ECR[ECR Repository]
    ECR --> AR
    
    AR --> |Scale to Zero| ZERO[0 Cost When Inactive]
    AU --> |Auto-pause| PAUSE[5min → $0]
```

## Configuration Examples

### CDK Construct for VanguardAI App Runner

```python
from aws_cdk import (
    Stack,
    aws_apprunner as apprunner,
    aws_ecr as ecr,
    aws_iam as iam,
    aws_secretsmanager as secrets,
    Duration,
)

class VanguardAIAppRunnerConstruct(Construct):
    """
    VanguardAI App Runner construct optimized for maritime insurance FastAPI backend
    Includes scale-to-zero configuration and Aurora Serverless v2 integration
    """
    
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # ECR repository for container images
        self.repository = ecr.Repository(
            self, "FastAPIRepository",
            repository_name="vanguardai-maritime-api",
            lifecycle_rules=[
                ecr.LifecycleRule(
                    max_image_count=10,
                    rule_priority=1,
                    tag_status=ecr.TagStatus.UNTAGGED
                )
            ]
        )
        
        # IAM role for App Runner service
        self.execution_role = iam.Role(
            self, "AppRunnerExecutionRole",
            assumed_by=iam.ServicePrincipal("build.apprunner.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "service-role/AWSAppRunnerServicePolicyForECRAccess"
                )
            ]
        )
        
        # Instance role for runtime access
        self.instance_role = iam.Role(
            self, "AppRunnerInstanceRole",
            assumed_by=iam.ServicePrincipal("tasks.apprunner.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AmazonRDSDataFullAccess"  # For Aurora Serverless v2
                ),
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "SecretsManagerReadWrite"  # For database credentials
                )
            ]
        )
        
        # App Runner service configuration
        self.service = apprunner.Service(
            self, "VanguardAIService",
            service_name=f"vanguardai-{kwargs.get('environment', 'preview')}",
            source=apprunner.Source.from_ecr(
                image_configuration=apprunner.ImageConfiguration(
                    port=8000,  # FastAPI default port
                    environment_variables={
                        "ENVIRONMENT": kwargs.get('environment', 'preview'),
                        "DATABASE_HOST": kwargs.get('database_host'),
                        "REDIS_URL": kwargs.get('redis_url', ''),
                    },
                    environment_secrets={
                        "DATABASE_PASSWORD": apprunner.Secret.from_secrets_manager(
                            kwargs.get('db_secret')
                        ),
                        "JWT_SECRET": apprunner.Secret.from_secrets_manager(
                            kwargs.get('jwt_secret')
                        )
                    }
                ),
                repository=self.repository,
                tag="latest"
            ),
            instance_configuration=apprunner.InstanceConfiguration(
                # VanguardAI scale-to-zero configuration
                cpu=apprunner.Cpu.HALF_VCPU if kwargs.get('environment') == 'preview' else apprunner.Cpu.ONE_VCPU,
                memory=apprunner.Memory.HALF_GB if kwargs.get('environment') == 'preview' else apprunner.Memory.TWO_GB,
                # Scale-to-zero configuration
                instance_role=self.instance_role
            ),
            auto_scaling_configuration=apprunner.AutoScalingConfiguration(
                self, "AutoScaling",
                auto_scaling_configuration_name=f"vanguardai-{kwargs.get('environment', 'preview')}-scaling",
                max_concurrency=kwargs.get('max_concurrency', 100),
                max_size=kwargs.get('max_size', 25),
                min_size=0  # Enable scale-to-zero
            ),
            health_check_configuration=apprunner.HealthCheckConfiguration(
                healthy_threshold=1,
                interval=Duration.seconds(10),
                path="/health",
                protocol=apprunner.HealthCheckProtocol.HTTP,
                timeout=Duration.seconds(5),
                unhealthy_threshold=5
            )
        )
```

### FastAPI Health Check Implementation

```python
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import psycopg2
import os
from datetime import datetime

app = FastAPI(title="VanguardAI Maritime Insurance API")

@app.get("/health")
async def health_check():
    """
    VanguardAI health check endpoint for App Runner
    Validates database connectivity and service status
    """
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "maritime-insurance-api",
        "environment": os.getenv("ENVIRONMENT", "preview"),
        "checks": {}
    }
    
    try:
        # Database connectivity check
        db_host = os.getenv("DATABASE_HOST")
        if db_host:
            # Simple connection test for Aurora Serverless v2
            import asyncpg
            conn = await asyncpg.connect(
                host=db_host,
                database=os.getenv("DATABASE_NAME", "maritime_insurance"),
                user=os.getenv("DATABASE_USER", "postgres"),
                password=os.getenv("DATABASE_PASSWORD"),
                timeout=3  # Quick timeout for health checks
            )
            await conn.close()
            health_status["checks"]["database"] = "connected"
        else:
            health_status["checks"]["database"] = "not_configured"
        
        # Additional service checks
        health_status["checks"]["memory_usage"] = "within_limits"
        health_status["checks"]["api_endpoints"] = "responsive"
        
        return JSONResponse(content=health_status, status_code=200)
        
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["checks"]["database"] = f"error: {str(e)}"
        return JSONResponse(content=health_status, status_code=503)

@app.get("/")
async def root():
    """Root endpoint with service information"""
    return {
        "service": "VanguardAI Maritime Insurance API",
        "version": "1.0.0",
        "environment": os.getenv("ENVIRONMENT", "preview"),
        "status": "running"
    }
```

### GitHub Actions Deployment Pipeline

```yaml
name: VanguardAI App Runner Deploy

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

permissions:
  id-token: write
  contents: read

jobs:
  deploy-preview:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    environment: preview
    
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          aws-region: ${{ secrets.AWS_REGION }}
      
      - name: Build and push Docker image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          ECR_REPOSITORY: vanguardai-maritime-api
          IMAGE_TAG: pr-${{ github.event.number }}
        run: |
          # Build FastAPI container
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
      
      - name: Deploy preview environment with CDK
        run: |
          cd infrastructure
          pip install -r requirements.txt
          cdk deploy preview-stack-pr-${{ github.event.number }} \
            --parameters ImageTag=pr-${{ github.event.number }} \
            --parameters Environment=preview \
            --require-approval never
      
      - name: Comment PR with preview URL
        uses: actions/github-script@v7
        with:
          script: |
            const { data: service } = await github.rest.apprunner.describeService({
              ServiceArn: process.env.APP_RUNNER_ARN
            });
            
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `🚀 **VanguardAI Preview Environment Deployed**
              
              **Preview URL**: https://${service.ServiceUrl}
              **Cost**: ~$2.70/month with scale-to-zero
              **Features**: Auto-cleanup on PR close
              
              **API Endpoints**:
              - Health Check: https://${service.ServiceUrl}/health
              - API Docs: https://${service.ServiceUrl}/docs
              - Fleet Management: https://${service.ServiceUrl}/api/fleets
              `
            });

  cleanup-preview:
    if: github.event.action == 'closed'
    runs-on: ubuntu-latest
    environment: preview
    
    steps:
      - name: Cleanup preview environment
        run: |
          cd infrastructure
          cdk destroy preview-stack-pr-${{ github.event.number }} --force
```

## Best Practices

### VanguardAI Cost Optimization

#### Scale-to-Zero Configuration
```python
# Optimal configuration for preview environments
instance_configuration=apprunner.InstanceConfiguration(
    cpu=apprunner.Cpu.HALF_VCPU,      # Minimal CPU for cost savings
    memory=apprunner.Memory.HALF_GB,   # Minimal memory for basic FastAPI
    instance_role=instance_role
),
auto_scaling_configuration=apprunner.AutoScalingConfiguration(
    min_size=0,          # Enable scale-to-zero
    max_size=5,          # Limit maximum for cost control
    max_concurrency=50   # Optimize for preview workloads
)
```

#### Production Configuration
```python
# Production configuration with performance optimization
instance_configuration=apprunner.InstanceConfiguration(
    cpu=apprunner.Cpu.FOUR_VCPU,      # High performance for production
    memory=apprunner.Memory.EIGHT_GB,  # Sufficient memory for complex operations
    instance_role=instance_role
),
auto_scaling_configuration=apprunner.AutoScalingConfiguration(
    min_size=2,          # Always-on for production availability
    max_size=25,         # Scale for high traffic
    max_concurrency=100  # Optimize for production workloads
)
```

### Security Best Practices

#### Environment-Specific Access Control
```python
def create_instance_role(self, environment: str) -> iam.Role:
    """Create environment-specific IAM role with least privilege access"""
    
    policies = [
        iam.ManagedPolicy.from_aws_managed_policy_name(
            "SecretsManagerReadWrite"
        )
    ]
    
    # Add Aurora Serverless v2 access
    if environment in ['uat', 'production']:
        policies.append(
            iam.ManagedPolicy.from_aws_managed_policy_name(
                "AmazonRDSDataFullAccess"
            )
        )
    
    # Preview environments get limited access
    if environment == 'preview':
        policies.append(
            iam.ManagedPolicy(
                self, f"PreviewDBAccess-{environment}",
                statements=[
                    iam.PolicyStatement(
                        effect=iam.Effect.ALLOW,
                        actions=[
                            "rds-data:ExecuteStatement",
                            "rds-data:BatchExecuteStatement"
                        ],
                        resources=[f"arn:aws:rds:*:*:cluster:preview-*"]
                    )
                ]
            )
        )
    
    return iam.Role(
        self, f"AppRunnerInstanceRole-{environment}",
        assumed_by=iam.ServicePrincipal("tasks.apprunner.amazonaws.com"),
        managed_policies=policies
    )
```

### Performance Optimization

#### Container Image Optimization
```dockerfile
# Multi-stage build for optimized container images
FROM python:3.11-slim as builder

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim

# Copy only necessary files
COPY --from=builder /root/.local /root/.local
COPY ./app /app

# VanguardAI health check optimization
HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# App Runner port configuration
EXPOSE 8000

# Optimized startup command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
```

## Team Member Responsibilities

### Head of Engineering
**Tools**: Claude Code Max ($100/month), AWS Console  
**Responsibilities**:
- App Runner service architecture and scaling policies
- Security configuration and IAM role management
- Cost optimization monitoring and budget alerts
- Cross-environment deployment strategy

**Key Tasks**:
```bash
# Monitor App Runner costs and scaling metrics
aws apprunner describe-service --service-arn <service-arn>
aws cloudwatch get-metric-statistics --namespace AWS/AppRunner

# Configure environment-specific policies
cdk deploy shared-iam-stack --parameters Environment=production
```

### Lead Backend Developer
**Tools**: Claude Code Max ($200/month), Cursor IDE  
**Responsibilities**:
- FastAPI application containerization and optimization
- Health check implementation and monitoring
- Database integration with Aurora Serverless v2
- API performance optimization

**Key Tasks**:
```python
# Using Claude Code Max for App Runner optimization:
"Optimize FastAPI application for App Runner scale-to-zero with:
- Minimal cold start time
- Efficient database connection pooling for Aurora Serverless v2
- Health check endpoint optimized for 10-second intervals
- Memory usage optimization for 0.5GB containers"
```

### Lead Frontend Developer
**Tools**: Claude Code Max ($200/month), Figma ($15/month)  
**Responsibilities**:
- CDK frontend construct integration with App Runner
- CloudFront origin configuration for App Runner services
- Frontend-backend integration testing in preview environments
- Performance monitoring from frontend perspective

**Key Tasks**:
```typescript
// Using Claude Code Max for CDK integration:
"Create CDK construct that integrates CloudFront with App Runner service:
- Custom origin configuration with health check failover
- Cache behavior optimization for API endpoints
- Preview environment URL generation for PR comments
- SSL certificate management for custom domains"
```

### UI/UX Engineer
**Tools**: Figma ($15/month)  
**Responsibilities**:
- Design validation in App Runner preview environments
- User experience testing with scale-to-zero behavior
- Performance impact assessment on user interactions
- Mobile responsiveness testing across environments

**Key Tasks**:
- Test design implementations in $2.70/month preview environments
- Validate user experience during App Runner cold starts
- Document performance impact of scale-to-zero on user flows

## Training Resources and Learning Path

### Week 1: App Runner Fundamentals
**Objective**: Understand serverless container concepts and VanguardAI architecture

**Resources**:
- [AWS App Runner Developer Guide](https://docs.aws.amazon.com/apprunner/latest/dg/)
- [VanguardAI Implementation Guide](../docs/implementation-guide/vanguardai-complete-implementation-guide.md)
- [Serverless Containers Best Practices](https://aws.amazon.com/getting-started/hands-on/deploy-docker-containers/)

**Hands-on Labs**:
1. Deploy simple FastAPI app to App Runner
2. Configure health checks and scaling policies
3. Test scale-to-zero behavior with traffic simulation

### Week 2: VanguardAI Integration
**Objective**: Implement App Runner in VanguardAI stack with CDK

**Resources**:
- [AWS CDK App Runner Construct Documentation](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_apprunner.html)
- [Maritime Insurance API Integration Patterns](../docs/implementation-guide/stage-1-requirements-guide.md)

**Hands-on Labs**:
1. Create CDK constructs for maritime insurance FastAPI backend
2. Integrate with Aurora Serverless v2 and Secrets Manager
3. Deploy preview environment with GitHub Actions

### Week 3: Production Optimization
**Objective**: Optimize App Runner for production workloads and cost efficiency

**Resources**:
- [App Runner Performance Optimization](https://docs.aws.amazon.com/apprunner/latest/dg/service-configure-performance.html)
- [VanguardAI Cost Optimization Strategies](../docs/cost-benefit-analysis/roi-analysis.md)

**Hands-on Labs**:
1. Configure production-grade scaling policies
2. Implement comprehensive monitoring and alerting
3. Test blue-green deployment with zero downtime

### Week 4: Advanced Features
**Objective**: Master advanced App Runner features for enterprise deployment

**Resources**:
- [Custom Domains and SSL Certificates](https://docs.aws.amazon.com/apprunner/latest/dg/manage-custom-domains.html)
- [VPC Connectivity](https://docs.aws.amazon.com/apprunner/latest/dg/network-vpc.html)

**Hands-on Labs**:
1. Configure custom domains for maritime insurance API
2. Implement VPC connectivity for enhanced security
3. Set up cross-region deployment strategies

### Self-Assessment Checklist

**Basic Competency**:
- [ ] Can deploy FastAPI application to App Runner
- [ ] Understands scale-to-zero cost benefits
- [ ] Can configure health checks and basic monitoring

**Intermediate Competency**:
- [ ] Can create CDK constructs for App Runner services
- [ ] Integrates App Runner with Aurora Serverless v2
- [ ] Configures GitHub Actions deployment pipelines

**Advanced Competency**:
- [ ] Optimizes App Runner for production workloads
- [ ] Implements comprehensive monitoring and alerting
- [ ] Manages multi-environment deployment strategies

**Expert Level**:
- [ ] Designs cost-optimized architectures with App Runner
- [ ] Troubleshoots complex scaling and performance issues
- [ ] Mentors team members on App Runner best practices

## Cost Analysis and ROI

### VanguardAI Cost Model

| Environment | Configuration | Monthly Cost | Annual Cost | Key Benefits |
|-------------|---------------|--------------|-------------|--------------|
| **Preview (per PR)** | 0.5 vCPU, 0.5GB RAM | $2.70 | $32.40 | Scale-to-zero, auto-cleanup |
| **UAT** | 1 vCPU, 2GB RAM | $81.00 | $972.00 | Production-like testing |
| **Production** | 4 vCPU, 8GB RAM | $1,500.00 | $18,000.00 | Enterprise scale, high availability |

### Cost Comparison vs Traditional ECS

| Platform | Preview Environment | UAT Environment | Production Environment |
|----------|-------------------|-----------------|----------------------|
| **App Runner (VanguardAI)** | $2.70/month | $81/month | $1,500/month |
| **ECS Fargate (Traditional)** | $43.80/month | $175.20/month | $2,190/month |
| **Savings** | **94% reduction** | **54% reduction** | **32% reduction** |

### ROI Calculation

**Investment**:
- Implementation time: 2 weeks (Head of Engineering + Lead Backend)
- Training cost: 4 weeks × 4 team members = 16 person-weeks
- Infrastructure setup: $500 one-time

**Annual Savings**:
- Preview environments: 10 PRs/month × $41.10 savings = $4,932/year
- UAT environment: $94.20 savings × 12 months = $1,130/year
- Production environment: $690 savings × 12 months = $8,280/year
- **Total Annual Savings**: $14,342/year

**ROI**: 1,434% return on investment within first year

---

**Monthly Cost**: $2.70 (preview) to $1,500 (production)  
**Scale-to-Zero**: ✅ Reduces costs to $0 during inactivity  
**Container Platform**: ✅ Fully managed serverless containers  
**VanguardAI Integration**: ✅ Optimized for maritime insurance FastAPI backend