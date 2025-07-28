# Ephemeral Environments Training

## Overview

This training module focuses on VanguardAI's revolutionary ephemeral environment strategy that delivers $12/month per PR environments with automatic cleanup, enabling isolated testing and stakeholder review for every feature.

**Target Audience**: All development team members  
**Duration**: 3 weeks (12 hours total)  
**Format**: Hands-on labs with real PR workflow simulation

---

## Learning Objectives

By completion, participants will master:

1. **Deploy ephemeral PR environments** automatically via GitHub Actions
2. **Execute E2E testing** on isolated infrastructure per feature
3. **Manage cost-effective workflows** maintaining $12/month per environment
4. **Implement auto-cleanup** systems preventing resource waste
5. **Facilitate stakeholder review** through preview environment access

---

## Week 1: Ephemeral Environment Architecture

### Day 1-2: Understanding Ephemeral Environments

**Learning Goals**: Grasp the revolutionary approach to PR-based infrastructure

**Conceptual Framework**:
```
Traditional Development:
Shared Dev Environment → Conflicts → Manual Testing → $200+/month

VanguardAI Ephemeral:
PR Creation → Isolated Environment → Auto-Testing → Auto-Cleanup → $12/month
```

**Hands-on Lab 1**: Basic Ephemeral Environment Deployment
```python
# Claude Code Max CDK construct creation:
"Build ephemeral environment CDK stack for maritime insurance PR:
- Unique naming: pr-{number}-vanguard-{service}
- App Runner: 0.25 vCPU, 0.5GB RAM, scale-to-zero
- Aurora Serverless v2: 0.5-1 ACU, 5-minute auto-pause
- S3 + CloudFront: Unique subdomain pr-{number}.preview.domain.com
- Resource tags for cleanup identification"
```

**Practical Exercise**:
- Create PR with sample maritime insurance feature
- Observe automatic environment deployment
- Access unique preview URL
- Monitor resource creation and costs

**Role-Specific Focus**:
- **Head of Engineering**: Architecture oversight and cost validation
- **Lead Frontend**: Preview environment testing and validation
- **Lead Backend**: API isolation and database seeding
- **UI/UX Engineer**: Design validation on live environment

### Day 3-5: GitHub Actions Integration

**Learning Goals**: Automate ephemeral environment lifecycle through CI/CD

**Hands-on Lab 2**: Complete PR Pipeline Setup
```yaml
# GitHub Actions workflow with Claude Code Max:
"Create comprehensive PR pipeline for ephemeral environments:

Workflow stages:
1. Change Detection: Identify modified components
2. Build & Package: Create deployable artifacts
3. Deploy Infrastructure: CDK deploy with unique PR identifier
4. Environment Validation: Health checks and connectivity tests
5. E2E Test Execution: Full workflow testing on isolated infrastructure
6. PR Status Update: Comment with environment URLs and test results"
```

**Practical Exercise**:
- Configure GitHub repository secrets and environments
- Set up OIDC authentication for AWS deployment
- Test complete pipeline with sample feature PR
- Validate environment isolation and functionality

**Assessment Criteria**:
- Successfully deploy ephemeral environment ✅
- Achieve deployment time <10 minutes ✅
- Validate resource isolation ✅
- Confirm cost tracking <$12/month ✅

---

## Week 2: Testing and Validation Workflows

### Day 6-8: E2E Testing on Ephemeral Infrastructure

**Learning Goals**: Execute comprehensive testing on isolated environments

**Hands-on Lab 3**: E2E Test Suite Configuration
```typescript
# Playwright configuration with Claude Code Max:
"Configure E2E test suite for maritime insurance ephemeral environments:

Test scenarios:
- User authentication with isolated database
- Quote generation workflow with real calculations
- Fleet management operations
- Claims processing simulation
- Cross-browser compatibility validation

Configuration:
- Dynamic base URL from GitHub Actions environment
- Test data seeding for consistent state
- Parallel test execution for speed
- Screenshot capture on failures
- Results integration with PR comments"
```

**Practical Exercise**:
- Set up Playwright test suite for maritime insurance workflows
- Configure test data seeding strategies
- Execute tests against ephemeral environment
- Generate comprehensive test reports

**Role-Specific Tasks**:
- **Lead Frontend**: UI/UX workflow testing and validation
- **Lead Backend**: API integration and data consistency testing
- **UI/UX Engineer**: User experience validation across devices
- **Head of Engineering**: Test infrastructure optimization

### Day 9-10: Stakeholder Review Process

**Learning Goals**: Enable effective business stakeholder validation

**Hands-on Lab 4**: Stakeholder Review Workflow
```markdown
# Claude Code Max PR template creation:
"Create comprehensive PR template for stakeholder review:

PR Description Template:
- Feature overview with business context
- Preview environment URLs (frontend, API docs)
- Test credentials and sample data
- Known limitations and edge cases
- Acceptance criteria checklist
- Mobile/desktop compatibility notes"
```

**Practical Exercise**:
- Create stakeholder-friendly PR with preview environment
- Generate test data representing realistic maritime scenarios
- Document review process and feedback collection
- Simulate stakeholder acceptance workflow

**Assessment Criteria**:
- Configure effective E2E testing ✅
- Enable stakeholder preview access ✅
- Document review processes ✅
- Achieve testing automation ✅

---

## Week 3: Cost Control and Cleanup Automation

### Day 11-12: Auto-Cleanup Implementation

**Learning Goals**: Implement reliable cleanup automation preventing cost overruns

**Hands-on Lab 5**: Comprehensive Cleanup System
```yaml
# Multi-trigger cleanup with Claude Code Max:
"Create robust cleanup automation for ephemeral environments:

Cleanup Triggers:
1. PR Close/Merge: Immediate cleanup via GitHub webhook
2. Scheduled Cleanup: Daily scan for abandoned environments  
3. Cost Threshold: Automatic cleanup if environment exceeds $15/month
4. Manual Cleanup: On-demand cleanup for emergency situations

Cleanup Process:
- Identify all resources by PR tags
- Force destroy CDK stack with all resources
- Verify CloudFront distribution removal
- Clean up Route 53 records
- Update PR with cleanup status
- Log cleanup actions for audit"
```

**Practical Exercise**:
- Implement all cleanup triggers
- Test cleanup reliability with multiple scenarios
- Validate complete resource removal
- Monitor cleanup success rates

### Day 13-15: Cost Monitoring and Optimization

**Learning Goals**: Maintain strict cost control for ephemeral environments

**Hands-on Lab 6**: Advanced Cost Control
```python
# Cost monitoring with Claude Code Max:
"Implement comprehensive cost monitoring for ephemeral environments:

Monitoring Components:
- Real-time cost tracking per PR environment
- Budget alerts at $10, $15, and $20 thresholds
- Usage pattern analysis for optimization
- Cost anomaly detection and automatic investigation
- Weekly cost reports with optimization recommendations

Optimization Strategies:
- Auto-pause Aurora after 5 minutes of inactivity
- Scale-to-zero App Runner during off-hours
- Aggressive CloudFront caching configuration
- S3 lifecycle policies for temporary assets"
```

**Final Assessment**:
- Achieve cost target: $12/month per environment ✅
- Implement automated cleanup with 99%+ success rate ✅
- Configure comprehensive monitoring ✅
- Document optimization strategies ✅

---

## Advanced Topics

### Multi-Environment Testing Strategy

**Scenario**: Testing features that require integration across multiple services

**Solution Pattern**:
```yaml
# Complex environment setup:
Multi-Service Ephemeral Environment:
  - Frontend: React application with unique branding
  - Backend API: FastAPI with isolated database
  - Third-party Integrations: Sandboxed external API connections
  - Authentication: Isolated auth service with test users
```

### Database Migration Testing

**Challenge**: Testing schema changes safely in ephemeral environments

**VanguardAI Approach**:
```python
# Migration testing strategy:
"Implement database migration testing in ephemeral environments:
- Seed production-like data structures
- Execute forward migrations in isolated database
- Validate rollback procedures
- Test application compatibility with new schema"
```

### Performance Testing Integration

**Advanced Lab**: Load testing on ephemeral infrastructure
```python
# Performance validation:
"Configure performance testing for ephemeral environments:
- Artillery.js load testing integration
- Aurora Serverless scaling validation
- App Runner auto-scaling behavior
- CloudFront cache performance measurement"
```

---

## Success Metrics and KPIs

### Technical Performance
- **Deployment Time**: <10 minutes for complete environment
- **Test Execution**: <15 minutes for full E2E suite
- **Cleanup Success**: >99% automated cleanup completion
- **Cost Control**: <$12/month per active PR environment

### Business Impact
- **Development Velocity**: 40% faster feature review cycles
- **Quality Improvement**: 60% reduction in production bugs
- **Stakeholder Satisfaction**: Faster feedback and validation
- **Cost Savings**: 85% reduction vs traditional development environments

### Team Productivity
- **PR Review Efficiency**: Faster reviews with live environment access
- **Integration Confidence**: Reduced fear of breaking shared environments
- **Feature Isolation**: Parallel development without conflicts
- **Learning Acceleration**: Hands-on experience with AWS serverless

---

## Certification Process

### Practical Demonstration
1. **Create complete ephemeral environment** for a new maritime insurance feature
2. **Execute full testing suite** with comprehensive coverage
3. **Facilitate stakeholder review** with clear documentation
4. **Demonstrate cleanup automation** with cost validation

### Knowledge Assessment
- **Architecture Understanding**: Explain ephemeral environment benefits
- **Cost Analysis**: Calculate and optimize environment costs
- **Troubleshooting**: Resolve deployment and cleanup issues
- **Process Design**: Design efficient review workflows

### Team Integration Skills
- **Collaborative Development**: Work effectively with isolated environments
- **Stakeholder Communication**: Present features clearly for business review
- **Process Improvement**: Identify optimization opportunities
- **Knowledge Transfer**: Train other team members

---

## Troubleshooting Guide

### Common Issues and Solutions

**Environment Deployment Failures**:
```bash
# Diagnostic commands:
aws cloudformation describe-stacks --stack-name preview-pr-123
aws logs describe-log-groups --log-group-name-prefix /aws/apprunner
```

**Cost Overruns**:
```python
# Cost investigation:
"Use Claude Code Max to analyze AWS Cost Explorer:
- Identify highest cost resources in PR environment
- Compare actual vs expected costs
- Generate optimization recommendations"
```

**Cleanup Failures**:
```yaml
# Manual cleanup process:
Emergency Cleanup Steps:
1. Identify stuck resources via AWS Console
2. Force delete CloudFormation stack
3. Manual cleanup of remaining resources
4. Update cleanup automation to prevent recurrence
```

---

## Resources and Next Steps

### Documentation References
- **VanguardAI Implementation Guide**: Complete deployment procedures
- **AWS CDK Best Practices**: Infrastructure patterns and examples
- **GitHub Actions Documentation**: CI/CD workflow optimization

### Advanced Training Paths
- **VanguardAI Git Workflow Training**: Advanced CI/CD patterns
- **AWS Cost Optimization Training**: Advanced cost management
- **Production Deployment Training**: Blue-green deployment mastery

### Community and Support
- **Team Office Hours**: Weekly troubleshooting and Q&A
- **Claude Code Max Integration**: AI-assisted problem solving
- **Best Practices Sharing**: Regular team knowledge sessions

---

**Training Status**: Ready for Team Implementation  
**Prerequisites**: VanguardAI Infrastructure Training completed  
**Next Module**: VanguardAI Git Workflow Training  
**Estimated Time to Mastery**: 3 weeks with daily practice