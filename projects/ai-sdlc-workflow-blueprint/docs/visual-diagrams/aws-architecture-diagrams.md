# AWS Architecture Visual Diagrams

## Overview

This document provides visual diagrams for all proposed AWS architecture options to help understand the infrastructure layouts, data flows, and component relationships for each deployment strategy.

---

## Option 1: Simple AWS Setup Architecture

### High-Level Architecture Diagram

```mermaid
graph TB
    subgraph "GitHub Integration"
        GH[GitHub Repository]
        GA[GitHub Actions]
    end
    
    subgraph "AWS Cloud"
        subgraph "Frontend (Static)"
            S3[S3 Bucket<br/>Static Website]
            CF[CloudFront CDN<br/>Global Distribution]
        end
        
        subgraph "Backend (Containers)"
            ALB[Application Load Balancer]
            ECS[ECS Fargate Service<br/>FastAPI Container]
            ECR[ECR Container Registry]
        end
        
        subgraph "Database"
            RDS[(RDS PostgreSQL<br/>Single Instance)]
        end
        
        subgraph "Monitoring"
            CW[CloudWatch<br/>Logs & Metrics]
            XR[X-Ray Tracing]
        end
    end
    
    subgraph "Users"
        U1[Global Users]
        U2[API Clients]
    end
    
    %% Data Flow
    GH -->|Code Push| GA
    GA -->|Build & Deploy| S3
    GA -->|Build & Push| ECR
    GA -->|Deploy| ECS
    
    U1 -->|HTTPS Requests| CF
    CF -->|Cache Miss| S3
    
    U2 -->|API Requests| ALB
    ALB -->|Load Balance| ECS
    ECS -->|Database Queries| RDS
    
    ECS -->|Logs & Metrics| CW
    ECS -->|Tracing| XR
    
    style S3 fill:#e1f5fe
    style CF fill:#e8f5e8
    style ECS fill:#fff3e0
    style RDS fill:#fce4ec
```

### Cost Breakdown Visualization

```mermaid
pie title Monthly Cost Distribution - Simple AWS Setup ($388)
    "ECS Fargate" : 160
    "RDS PostgreSQL" : 144
    "ALB" : 18
    "S3 + CloudFront" : 20
    "CloudWatch" : 10
    "Data Transfer" : 20
    "GitHub" : 16
```

### Deployment Flow Diagram

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant GH as GitHub
    participant GA as GitHub Actions
    participant ECR as ECR Registry
    participant ECS as ECS Fargate
    participant S3 as S3 Bucket
    participant CF as CloudFront
    
    Dev->>GH: Push Code
    GH->>GA: Trigger Workflow
    
    par Frontend Deployment
        GA->>GA: Build React App
        GA->>S3: Upload Static Files
        GA->>CF: Invalidate Cache
    and Backend Deployment
        GA->>GA: Build Docker Image
        GA->>ECR: Push Container
        GA->>ECS: Update Service
        ECS->>ECS: Rolling Update
    end
```

---

## Option 2: Multi-Environment Setup Architecture

### Multi-Environment Overview

```mermaid
graph TB
    subgraph "GitHub"
        GH[GitHub Repository]
        GA[GitHub Actions]
        CDP[CDK Pipelines]
    end
    
    subgraph "Development Environment"
        subgraph "Dev Frontend"
            S3D[S3 Dev Bucket]
            CFD[CloudFront Dev]
        end
        subgraph "Dev Backend"
            ALBD[ALB Dev]
            ECSD[ECS Dev]
        end
        subgraph "Dev Database"
            RDSD[(RDS Dev<br/>t3.medium)]
        end
    end
    
    subgraph "Staging Environment"
        subgraph "Staging Frontend"
            S3S[S3 Staging Bucket]
            CFS[CloudFront Staging]
        end
        subgraph "Staging Backend"
            ALBS[ALB Staging]
            ECSS[ECS Staging]
        end
        subgraph "Staging Database"
            RDSS[(RDS Staging<br/>r5.large)]
        end
    end
    
    subgraph "Production Environment"
        subgraph "Prod Frontend"
            S3P[S3 Prod Bucket]
            CFP[CloudFront Prod]
        end
        subgraph "Prod Backend"
            ALBP[ALB Prod]
            ECSP[ECS Prod Multi-AZ]
        end
        subgraph "Prod Database"
            RDSP[(RDS Prod<br/>Multi-AZ + Replicas)]
        end
    end
    
    subgraph "Shared Services"
        R53[Route 53 DNS]
        ACM[Certificate Manager]
        CW[CloudWatch]
    end
    
    %% Deployment Flow
    GH -->|Commit| GA
    GA -->|Deploy| CDP
    CDP -->|Environment 1| S3D
    CDP -->|Environment 2| S3S
    CDP -->|Environment 3| S3P
    
    %% DNS Routing
    R53 -->|dev.app.com| CFD
    R53 -->|staging.app.com| CFS
    R53 -->|app.com| CFP
    
    style S3D fill:#e3f2fd
    style S3S fill:#f3e5f5
    style S3P fill:#e8f5e8
```

### Environment Promotion Pipeline

```mermaid
graph LR
    subgraph "Source Control"
        FB[Feature Branch]
        DB[Develop Branch]
        MB[Main Branch]
    end
    
    subgraph "Environments"
        DE[Development<br/>Auto Deploy]
        SE[Staging<br/>Manual Approval]
        PE[Production<br/>Manual Approval]
    end
    
    subgraph "Quality Gates"
        UT[Unit Tests]
        IT[Integration Tests]
        UAT[User Acceptance<br/>Testing]
        SM[Smoke Tests]
    end
    
    FB -->|Merge| DB
    DB -->|Trigger| DE
    DE -->|Pass| UT
    UT -->|Success| SE
    SE -->|Pass| IT
    IT -->|Approval| UAT
    UAT -->|Success| MB
    MB -->|Deploy| PE
    PE -->|Verify| SM
    
    style DE fill:#e3f2fd
    style SE fill:#f3e5f5
    style PE fill:#e8f5e8
```

---

## Option 3: Full Ephemeral Environments Architecture

### Dynamic Environment Creation

```mermaid
graph TB
    subgraph "GitHub Events"
        PR[Pull Request Created]
        PC[Pull Request Closed]
    end
    
    subgraph "Orchestration Layer"
        GW[GitHub Webhooks]
        L1[Lambda Function<br/>Environment Creator]
        L2[Lambda Function<br/>Environment Destroyer]
        DDB[(DynamoDB<br/>Environment Registry)]
    end
    
    subgraph "Dynamic AWS Resources"
        subgraph "Environment 1 (PR-123)"
            S3E1[S3 Bucket<br/>pr-123-frontend]
            CFE1[CloudFront<br/>pr-123.dev.app.com]
            ECSE1[ECS Service<br/>pr-123-backend]
            RDSE1[(RDS Instance<br/>pr-123-db)]
        end
        
        subgraph "Environment 2 (PR-456)"
            S3E2[S3 Bucket<br/>pr-456-frontend]
            CFE2[CloudFront<br/>pr-456.dev.app.com]
            ECSE2[ECS Service<br/>pr-456-backend]
            RDSE2[(RDS Instance<br/>pr-456-db)]
        end
        
        subgraph "Environment N (PR-789)"
            S3EN[S3 Bucket<br/>pr-789-frontend]
            CFEN[CloudFront<br/>pr-789.dev.app.com]
            ECSEN[ECS Service<br/>pr-789-backend]
            RDSEN[(RDS Instance<br/>pr-789-db)]
        end
    end
    
    subgraph "Cost Management"
        LC[Lambda Cost Monitor]
        CWA[CloudWatch Alarms]
        SC[Scheduled Cleanup]
    end
    
    %% Creation Flow
    PR -->|Webhook| GW
    GW -->|Trigger| L1
    L1 -->|Create| S3E1
    L1 -->|Create| CFE1
    L1 -->|Create| ECSE1
    L1 -->|Create| RDSE1
    L1 -->|Register| DDB
    
    %% Destruction Flow
    PC -->|Webhook| GW
    GW -->|Trigger| L2
    L2 -->|Destroy| S3E2
    L2 -->|Update| DDB
    
    %% Cost Management
    LC -->|Monitor| CWA
    SC -->|Cleanup| L2
    
    style L1 fill:#fff3e0
    style L2 fill:#ffebee
    style DDB fill:#e8f5e8
```

### Ephemeral Environment Lifecycle

```mermaid
stateDiagram-v2
    [*] --> PullRequestCreated
    PullRequestCreated --> Provisioning
    Provisioning --> ResourceCreation
    ResourceCreation --> DeploymentInProgress
    DeploymentInProgress --> EnvironmentReady
    EnvironmentReady --> InUse
    
    InUse --> UpdateTriggered : New commits
    UpdateTriggered --> DeploymentInProgress
    
    InUse --> IdleMonitoring : No activity
    IdleMonitoring --> ScheduledCleanup : 24h idle
    IdleMonitoring --> InUse : Activity detected
    
    InUse --> PullRequestClosed : PR merged/closed
    ScheduledCleanup --> ResourceDestruction
    PullRequestClosed --> ResourceDestruction
    ResourceDestruction --> [*]
    
    note right of ResourceCreation
        - S3 bucket creation
        - CloudFront distribution
        - ECS service deployment
        - RDS instance provisioning
    end note
    
    note right of ScheduledCleanup
        - Cost threshold monitoring
        - Idle time tracking
        - Automated cleanup triggers
    end note
```

---

## Option 4: Hybrid Architecture

### Multi-Platform Integration

```mermaid
graph TB
    subgraph "Production Tier (AWS)"
        subgraph "Production"
            S3P[S3 Production]
            CFP[CloudFront Production]
            ECSP[ECS Production]
            RDSP[(RDS Production)]
        end
        
        subgraph "Staging (AWS)"
            S3S[S3 Staging]
            CFS[CloudFront Staging]
            ECSS[ECS Staging]
            RDSS[(RDS Staging)]
        end
    end
    
    subgraph "Development Tier (Alternative Platforms)"
        subgraph "Vercel (Frontend)"
            VF[Vercel Frontend<br/>Preview Deployments]
        end
        
        subgraph "Railway (Backend)"
            RB[Railway Backend<br/>Ephemeral Services]
        end
        
        subgraph "PlanetScale (Database)"
            PS[(PlanetScale<br/>Database Branching)]
        end
    end
    
    subgraph "GitHub Integration"
        GH[GitHub Repository]
        GA[GitHub Actions]
    end
    
    subgraph "Monitoring & Management"
        UM[Unified Monitoring]
        DS[Data Sync Services]
    end
    
    %% Production Flow
    GH -->|Production Deploy| S3P
    GH -->|Production Deploy| ECSP
    
    %% Development Flow
    GH -->|Feature Branch| VF
    GH -->|Feature Branch| RB
    GH -->|Feature Branch| PS
    
    %% Data Synchronization
    RDSP -->|Periodic Sync| DS
    DS -->|Sanitized Data| PS
    
    %% Monitoring Integration
    S3P -->|Metrics| UM
    ECSP -->|Metrics| UM
    VF -->|Metrics| UM
    RB -->|Metrics| UM
    
    style S3P fill:#e8f5e8
    style VF fill:#e3f2fd
    style RB fill:#fff3e0
    style PS fill:#f3e5f5
```

### Cost Optimization Comparison

```mermaid
graph LR
    subgraph "Full AWS Approach"
        FA[Full AWS<br/>$950/month]
        FAD[3 Environments<br/>All AWS Services]
    end
    
    subgraph "Hybrid Approach"
        HA[Hybrid<br/>$800/month]
        HAP[Production + Staging: AWS<br/>$650/month]
        HAD[Development: Alternatives<br/>$150/month]
    end
    
    subgraph "Savings Analysis"
        SA[15-20% Cost Reduction<br/>Maintained Enterprise Features<br/>for Production]
    end
    
    FA -->|vs| HA
    HA -->|Results in| SA
    FAD -.->|Replaced by| HAD
    HAP -.->|Maintained| SA
    
    style HA fill:#e8f5e8
    style SA fill:#fff3e0
```

---

## Data Flow Diagrams

### Frontend Request Flow (S3 + CloudFront)

```mermaid
sequenceDiagram
    participant U as User
    participant CF as CloudFront Edge
    participant S3 as S3 Bucket
    participant API as FastAPI Backend
    participant DB as PostgreSQL
    
    U->>CF: Request index.html
    CF->>CF: Check Edge Cache
    
    alt Cache Hit
        CF->>U: Return Cached Content
    else Cache Miss
        CF->>S3: Fetch Content
        S3->>CF: Return Content
        CF->>CF: Cache Content
        CF->>U: Return Content
    end
    
    Note over U,CF: Static Assets Delivered
    
    U->>API: API Request
    API->>DB: Database Query
    DB->>API: Query Results
    API->>U: JSON Response
    
    Note over U,API: Dynamic Data Flow
```

### Backend Auto-Scaling Flow

```mermaid
graph TB
    subgraph "Traffic Pattern"
        T1[Low Traffic<br/>2 Tasks]
        T2[Medium Traffic<br/>4 Tasks]
        T3[High Traffic<br/>8 Tasks]
    end
    
    subgraph "ECS Auto Scaling"
        CW[CloudWatch Metrics<br/>CPU > 70%]
        ASG[Auto Scaling Policy<br/>Scale Out]
        ECS[ECS Service<br/>Task Definition]
        ALB[Application Load Balancer<br/>Health Checks]
    end
    
    subgraph "Database Scaling"
        RDS[(RDS PostgreSQL<br/>Connection Pooling)]
        RR[(Read Replicas<br/>Read Traffic)]
    end
    
    T1 -->|Increase| T2
    T2 -->|Spike| T3
    T3 -->|Metrics| CW
    CW -->|Trigger| ASG
    ASG -->|Scale| ECS
    ECS -->|Register| ALB
    ALB -->|Health Check| ECS
    
    ECS -->|Read/Write| RDS
    ECS -->|Read Only| RR
    
    style T3 fill:#ffebee
    style ASG fill:#e8f5e8
    style RR fill:#e3f2fd
```

---

## Security Architecture

### Network Security Diagram

```mermaid
graph TB
    subgraph "Internet Gateway"
        IGW[Internet Gateway]
    end
    
    subgraph "VPC (10.0.0.0/16)"
        subgraph "Public Subnets"
            ALB[Application Load Balancer<br/>10.0.1.0/24]
            NAT[NAT Gateway<br/>10.0.2.0/24]
        end
        
        subgraph "Private Subnets"
            ECS1[ECS Task 1<br/>10.0.10.0/24]
            ECS2[ECS Task 2<br/>10.0.11.0/24]
        end
        
        subgraph "Database Subnets"
            RDS1[(RDS Primary<br/>10.0.20.0/24)]
            RDS2[(RDS Standby<br/>10.0.21.0/24)]
        end
    end
    
    subgraph "Security Groups"
        SGALB[ALB Security Group<br/>80, 443 from Internet]
        SGECS[ECS Security Group<br/>8000 from ALB only]
        SGRDS[RDS Security Group<br/>5432 from ECS only]
    end
    
    subgraph "External Services"
        CF[CloudFront<br/>Global Edge]
        S3[S3 Bucket<br/>Private]
    end
    
    %% Network Flow
    IGW -->|HTTPS| ALB
    ALB -->|HTTP| ECS1
    ALB -->|HTTP| ECS2
    ECS1 -->|TCP 5432| RDS1
    ECS2 -->|TCP 5432| RDS1
    RDS1 -.->|Replication| RDS2
    
    %% Internet Access
    ECS1 -->|HTTPS| NAT
    ECS2 -->|HTTPS| NAT
    NAT -->|Internet| IGW
    
    %% CDN Flow
    CF -->|Origin Access| S3
    
    %% Security Group Associations
    ALB -.->|Protected by| SGALB
    ECS1 -.->|Protected by| SGECS
    ECS2 -.->|Protected by| SGECS
    RDS1 -.->|Protected by| SGRDS
    RDS2 -.->|Protected by| SGRDS
    
    style SGALB fill:#ffebee
    style SGECS fill:#fff3e0
    style SGRDS fill:#e8f5e8
```

---

## Monitoring and Observability

### Comprehensive Monitoring Stack

```mermaid
graph TB
    subgraph "Application Layer"
        FE[React Frontend<br/>S3 + CloudFront]
        BE[FastAPI Backend<br/>ECS Fargate]
        DB[(PostgreSQL<br/>RDS)]
    end
    
    subgraph "Monitoring Services"
        CW[CloudWatch<br/>Metrics & Logs]
        XR[X-Ray<br/>Distributed Tracing]
        CWI[CloudWatch Insights<br/>Log Analysis]
        CWD[CloudWatch Dashboard<br/>Visualization]
    end
    
    subgraph "Alerting"
        SNS[SNS Topics<br/>Notifications]
        SES[SES Email<br/>Alerts]
        SLACK[Slack Integration<br/>Team Notifications]
    end
    
    subgraph "External Monitoring"
        UH[UptimeRobot<br/>Endpoint Monitoring]
        GT[GTmetrix<br/>Performance Monitoring]
    end
    
    %% Data Collection
    FE -->|Access Logs| CW
    FE -->|Performance Metrics| CWI
    BE -->|Application Logs| CW
    BE -->|Trace Data| XR
    DB -->|Performance Metrics| CW
    
    %% Analysis & Visualization
    CW -->|Aggregate| CWD
    XR -->|Trace Analysis| CWD
    CWI -->|Log Insights| CWD
    
    %% Alerting Flow
    CW -->|Threshold Breach| SNS
    SNS -->|Email| SES
    SNS -->|Webhook| SLACK
    
    %% External Monitoring
    UH -->|Uptime Checks| SNS
    GT -->|Performance Reports| SNS
    
    style CW fill:#e3f2fd
    style XR fill:#f3e5f5
    style SNS fill:#fff3e0
```

### Key Metrics Dashboard Layout

```mermaid
graph TB
    subgraph "CloudWatch Dashboard"
        subgraph "Infrastructure Metrics"
            CPU[ECS CPU Utilization<br/>Target: <70%]
            MEM[ECS Memory Utilization<br/>Target: <80%]
            ALB_RC[ALB Request Count<br/>Trend Analysis]
            ALB_RT[ALB Response Time<br/>Target: <200ms]
        end
        
        subgraph "Application Metrics"
            API_RPS[API Requests/Second<br/>Throughput Monitoring]
            API_ERR[API Error Rate<br/>Target: <1%]
            DB_CONN[Database Connections<br/>Connection Pool Usage]
            DB_RT[Database Response Time<br/>Query Performance]
        end
        
        subgraph "Frontend Metrics"
            CF_HR[CloudFront Hit Ratio<br/>Target: >90%]
            CF_BW[Bandwidth Usage<br/>Cost Monitoring]
            PAGE_LOAD[Page Load Time<br/>User Experience]
            JS_ERR[JavaScript Errors<br/>Frontend Health]
        end
        
        subgraph "Business Metrics"
            USER_COUNT[Active Users<br/>Engagement Tracking]
            FEATURE_USAGE[Feature Usage<br/>Product Analytics]
            CONVERSION[Conversion Rate<br/>Business KPIs]
        end
    end
    
    style CPU fill:#ffebee
    style API_ERR fill:#ffebee
    style CF_HR fill:#e8f5e8
    style USER_COUNT fill:#e3f2fd
```

---

## Disaster Recovery Architecture

### Multi-Region Disaster Recovery

```mermaid
graph TB
    subgraph "Primary Region (us-east-1)"
        subgraph "Production Environment"
            S3P[S3 Primary<br/>Cross-Region Replication]
            CFP[CloudFront<br/>Global Distribution]
            ECSP[ECS Primary<br/>Multi-AZ]
            RDSP[(RDS Primary<br/>Multi-AZ)]
        end
    end
    
    subgraph "Disaster Recovery Region (us-west-2)"
        subgraph "DR Environment"
            S3DR[S3 DR<br/>Replica Bucket]
            ECSDR[ECS DR<br/>Standby Capacity]
            RDSDR[(RDS DR<br/>Cross-Region Replica)]
        end
    end
    
    subgraph "DNS Failover"
        R53[Route 53<br/>Health Checks]
        R53P[Primary Endpoint<br/>us-east-1]
        R53DR[DR Endpoint<br/>us-west-2]
    end
    
    subgraph "Monitoring & Automation"
        CWA[CloudWatch Alarms<br/>Health Monitoring]
        LF[Lambda Function<br/>Failover Automation]
        SNS[SNS Notifications<br/>Alert Team]
    end
    
    %% Normal Operation
    S3P -.->|Replication| S3DR
    RDSP -.->|Read Replica| RDSDR
    
    %% DNS Routing
    R53 -->|Health Check Pass| R53P
    R53P -->|Route Traffic| CFP
    
    %% Failover Process
    CWA -->|Health Check Fail| LF
    LF -->|Promote| RDSDR
    LF -->|Activate| ECSDR
    LF -->|Update DNS| R53
    R53 -->|Failover| R53DR
    R53DR -->|Route Traffic| S3DR
    
    %% Notifications
    LF -->|Alert| SNS
    
    style RDSP fill:#e8f5e8
    style RDSDR fill:#ffebee
    style LF fill:#fff3e0
```

---

## Summary

These visual diagrams provide comprehensive views of each AWS architecture option, highlighting:

1. **Option 1**: Simple, cost-effective setup ideal for starting
2. **Option 2**: Professional multi-environment approach for scaling teams
3. **Option 3**: Advanced ephemeral environments for maximum development velocity
4. **Option 4**: Hybrid approach balancing cost and functionality

Each diagram shows the key components, data flows, cost structures, and operational considerations to help make informed architectural decisions based on your specific requirements and constraints.