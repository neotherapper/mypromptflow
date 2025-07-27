---
description: '## Header Classification'
id: 1ee41488-d058-4561-8e20-a0ef69d6e36e
installation_priority: 3
item_type: mcp_server
migration_date: '2025-07-26'
name: Convex Real MCP Server
original_file: mcp-registry/detailed-profiles/tier-2/convex-realtime-platform-server-profile.md
priority: 2nd_priority
source_database: tools_services
status: active
tags:
- Database
- Tier 2
- Storage Service
- MCP Server
- API Service
- Security Tool
- Analytics
- Monitoring
- Cloud Platform
- Development Platform
---

## Header Classification

**Server Name**: Convex Real-Time Platform MCP Server  
**Category**: Real-Time Application Development & Backend-as-a-Service  
**Tier Classification**: Tier 2 (Score: 7.8/10)  
**Official Integration**: Community (Convex Ecosystem)  
**Maintenance Status**: Active Development  
**Enterprise Ready**: Yes  

**Quick Value Proposition**: Full-stack platform for building real-time applications with integrated database, functions, and live queries, providing automatic synchronization, real-time updates, and seamless frontend integration through serverless architecture.

## Technical Specifications

### Core Architecture
**Runtime Environment**: V8 JavaScript/TypeScript with Cloudflare Workers  
**Database Engine**: Custom ACID-compliant database with real-time queries  
**Query Interface**: TypeScript functions with automatic API generation  
**Real-Time Protocol**: WebSocket with optimistic updates and conflict resolution  
**Storage Format**: JSON documents with automatic indexing and optimization  

### Protocol Implementation
**Primary Protocol**: HTTP/2 with WebSocket for real-time updates  
**MCP Integration**: JSON-RPC 2.0 over WebSocket with live query support  
**Authentication**: Built-in auth with OAuth providers and custom authentication  
**Transport Security**: TLS 1.3 with automatic certificate management  
**Rate Limiting**: Function-level throttling with burst capacity management  

### Real-Time Capabilities
**Live Queries**: Automatic data synchronization with reactive updates  
**Optimistic Updates**: Client-side optimism with server-side conflict resolution  
**Collaborative Features**: Real-time collaboration with operational transformation  
**Event Streaming**: Server-sent events with reliable message delivery  
**Conflict Resolution**: Automatic merge strategies with custom conflict handlers  

### Development Features
**Full-Stack TypeScript**: End-to-end type safety with automatic code generation  
**Local Development**: Complete local development environment with hot reloading  
**Automatic Deployment**: Git-based deployment with preview environments  
**Schema Evolution**: Automatic database migrations with backwards compatibility  
**Testing Framework**: Built-in testing tools with snapshot testing support  

## Setup & Configuration

### Prerequisites
**Account Requirements**: Convex account with project creation permissions  
**Development Environment**: Node.js 16+ with TypeScript support  
**Git Integration**: Repository with automated deployment configuration  
**Local Tools**: Convex CLI for development and deployment  

### Installation Methods

#### Method 1: New Project Setup
```bash
# Install Convex CLI MCP Server
npm install -g convex

# Create new Convex project
npx create-convex@latest my-app
cd my-app

# Initialize Convex backend
npx convex dev

# Configure MCP integration
npm install @convex/mcp-server
```

#### Method 2: Existing Project Integration
```bash
# Add Convex to existing project
npm install convex

# Initialize Convex configuration
npx convex init

# Set up authentication and deploy
npx convex auth add
npx convex deploy
```

#### Method 3: Docker Development Environment
```dockerfile
# Dockerfile for Convex development
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
EXPOSE 3000 3001

# Start Convex development server
CMD ["npm", "run", "dev"]
```

### Configuration Parameters
```typescript
// convex.config.ts
import { defineApp } from "convex/server";

const app = defineApp();

app.use(convexMcpServer({
  // MCP server configuration
  facility: 3001,
  cors: {
    origin: ["http://localhost:3000", "https://your-app.com"],
    credentials: true
  },
  
  // Real-time configuration
  realtime: {
    maxConnections: 10000,
    heartbeatInterval: 30000,
    connectionTimeout: 60000
  },
  
  // Function configuration
  functions: {
    timeout: 30000,
    memoryLimit: "256MB",
    retryPolicy: {
      maxRetries: 3,
      backoffMultiplier: 2
    }
  },
  
  // Database configuration
  database: {
    consistencyLevel: "strong",
    indexCreationMode: "automatic",
    queryTimeout: 10000
  }
}));

export default app;
```

## API Interface & Usage

### Tool Categories

#### Database Operations
**Tool Name**: `convex_query`  
**Purpose**: Execute queries with real-time subscription capabilities  
**Parameters**: queryName (string), args (object), subscribe (boolean)  
**Response**: Query results with subscription handle for real-time updates  

**Tool Name**: `convex_mutation`  
**Purpose**: Execute database mutations with optimistic updates  
**Parameters**: mutationName (string), args (object), optimistic (boolean)  
**Response**: Mutation result with conflict resolution information  

#### Real-Time Operations
**Tool Name**: `convex_subscribe`  
**Purpose**: Create real-time subscriptions to data changes  
**Parameters**: queryName (string), args (object), callback (function)  
**Response**: Subscription handle with real-time update stream  

**Tool Name**: `convex_action`  
**Purpose**: Execute server-side actions with external API calls  
**Parameters**: actionName (string), args (object), timeout (number)  
**Response**: Action result with execution metadata  

#### Function Management
**Tool Name**: `convex_deploy_function`  
**Purpose**: Deploy and update server functions  
**Parameters**: functionCode (string), functionName (string), config (object)  
**Response**: Deployment status with version information  

**Tool Name**: `convex_function_logs`  
**Purpose**: Retrieve function execution logs and metrics  
**Parameters**: functionName (string), timeRange (object), level (string)  
**Response**: Log entries with performance metrics  

### Practical Implementation Examples

#### Real-Time Chat Application
```typescript
// Real-time messaging with collaborative features
const chatOperations = {
  sendMessage: async (messageData) => {
    return await convexMcp.execute('convex_mutation', {
      mutationName: 'messages:send',
      args: {
        chatId: messageData.chatId,
        content: messageData.content,
        attachments: messageData.attachments,
        mentions: messageData.mentions
      },
      optimistic: true // Enable optimistic updates
    });
  },

  subscribeToChat: async (chatId, onMessage) => {
    return await convexMcp.execute('convex_subscribe', {
      queryName: 'messages:list',
      args: { chatId, limit: 50 },
      callback: (messages) => {
        onMessage(messages);
      }
    });
  },

  updateTypingStatus: async (chatId, isTyping) => {
    return await convexMcp.execute('convex_action', {
      actionName: 'presence:updateTyping',
      args: { chatId, isTyping, timestamp: Date.now() },
      timeout: 5000
    });
  }
};

// Real-time presence tracking
const presenceOperations = {
  trackUserPresence: async (userId, status) => {
    return await convexMcp.execute('convex_mutation', {
      mutationName: 'presence:updateStatus',
      args: {
        userId,
        status: status, // online, away, offline
        lastSeen: new Date().toISOString(),
        metadata: {
          device: navigator.userAgent,
          location: await getCurrentLocation()
        }
      }
    });
  },

  subscribeToPresence: async (userIds, onPresenceChange) => {
    return await convexMcp.execute('convex_subscribe', {
      queryName: 'presence:getUsersStatus',
      args: { userIds },
      callback: onPresenceChange
    });
  }
};
```

#### Collaborative Document Editing
```typescript
// Real-time collaborative editing with operational transformation
const collaborativeOperations = {
  createDocument: async (documentData) => {
    return await convexMcp.execute('convex_mutation', {
      mutationName: 'documents:create',
      args: {
        title: documentData.title,
        content: documentData.content,
        collaborators: documentData.collaborators,
        permissions: {
          read: documentData.readPermissions,
          write: documentData.writePermissions,
          admin: documentData.adminPermissions
        }
      }
    });
  },

  applyOperation: async (documentId, operation) => {
    return await convexMcp.execute('convex_mutation', {
      mutationName: 'documents:applyOperation',
      args: {
        documentId,
        operation: {
          type: operation.type, // insert, delete, format
          position: operation.position,
          content: operation.content,
          attributes: operation.attributes,
          timestamp: Date.now(),
          authorId: operation.authorId
        }
      },
      optimistic: true
    });
  },

  subscribeToDocument: async (documentId, onDocumentChange) => {
    return await convexMcp.execute('convex_subscribe', {
      queryName: 'documents:getWithOperations',
      args: { documentId },
      callback: (document) => {
        onDocumentChange({
          content: document.content,
          operations: document.recentOperations,
          collaborators: document.activeCollaborators,
          version: document.version
        });
      }
    });
  },

  resolveConflicts: async (documentId, conflicts) => {
    return await convexMcp.execute('convex_action', {
      actionName: 'documents:resolveConflicts',
      args: {
        documentId,
        conflicts: conflicts.map(conflict => ({
          operationA: conflict.operationA,
          operationB: conflict.operationB,
          resolution: conflict.preferredResolution
        }))
      }
    });
  }
};
```

#### Real-Time Analytics Dashboard
```typescript
// Live metrics and analytics with automatic updates
const analyticsOperations = {
  trackEvent: async (eventData) => {
    return await convexMcp.execute('convex_mutation', {
      mutationName: 'analytics:trackEvent',
      args: {
        eventType: eventData.type,
        properties: eventData.properties,
        userId: eventData.userId,
        sessionId: eventData.sessionId,
        timestamp: new Date().toISOString(),
        metadata: {
          userAgent: eventData.userAgent,
          ipAddress: eventData.ipAddress,
          referrer: eventData.referrer
        }
      }
    });
  },

  subscribeToDashboard: async (dashboardConfig, onMetricsUpdate) => {
    return await convexMcp.execute('convex_subscribe', {
      queryName: 'analytics:getDashboardMetrics',
      args: {
        timeRange: dashboardConfig.timeRange,
        metrics: dashboardConfig.metrics,
        groupBy: dashboardConfig.groupBy,
        filters: dashboardConfig.filters
      },
      callback: (metrics) => {
        onMetricsUpdate({
          realTimeMetrics: metrics.realTime,
          aggregatedData: metrics.aggregated,
          trends: metrics.trends,
          lastUpdated: metrics.timestamp
        });
      }
    });
  },

  generateReport: async (reportConfig) => {
    return await convexMcp.execute('convex_action', {
      actionName: 'analytics:generateReport',
      args: {
        reportType: reportConfig.type,
        dateRange: reportConfig.dateRange,
        metrics: reportConfig.metrics,
        format: reportConfig.format, // json, csv, pdf
        deliveryMethod: reportConfig.delivery
      },
      timeout: 30000
    });
  }
};
```

## Integration Patterns

### Real-Time Web Application Integration
**Pattern**: Live Frontend Synchronization  
**Use Case**: Collaborative applications with instant updates  
**Implementation**: React/Vue.js with Convex hooks for real-time data binding  
**Benefits**: Automatic UI updates, optimistic rendering, conflict resolution  

### Microservices Event Architecture
**Pattern**: Event-Driven Service Communication  
**Use Case**: Microservices with real-time event propagation  
**Implementation**: Convex actions as event handlers with external API integration  
**Benefits**: Reliable event delivery, automatic retry, service decoupling  

### Mobile App Backend Integration
**Pattern**: Mobile-First Real-Time Backend  
**Use Case**: Mobile applications with offline-first capabilities  
**Implementation**: React Native/Flutter with optimistic updates and sync  
**Benefits**: Offline support, background sync, real-time collaboration  

### IoT Data Processing Integration
**Pattern**: Real-Time IoT Data Pipeline  
**Use Case**: IoT sensor data with live dashboard updates  
**Implementation**: Webhook ingestion with real-time aggregation and alerts  
**Benefits**: Live monitoring, automatic alerting, scalable data processing  

### Multi-Tenant SaaS Integration
**Pattern**: Tenant-Isolated Real-Time Platform  
**Use Case**: SaaS applications with tenant-specific real-time features  
**Implementation**: Tenant-based data isolation with shared infrastructure  
**Benefits**: Cost efficiency, feature isolation, scalable multi-tenancy  

## Performance & Scalability

### Real-Time Performance
**Update Propagation**: <100ms globally with edge network optimization  
**Query Latency**: <50ms P95 for database queries with automatic indexing  
**Function Execution**: <200ms cold start, <10ms warm execution  
**Concurrent Connections**: 100K+ WebSocket connections per deployment  

### Scaling Characteristics
**Automatic Scaling**: Function-based scaling with usage metrics  
**Global Distribution**: Edge deployment with regional data placement  
**Connection Scaling**: WebSocket connection pooling with load balancing  
**Database Scaling**: Automatic sharding with query optimization  

### Performance Optimization
**Query Optimization**: Automatic index creation with query analysis  
**Caching Strategy**: Multi-level caching with edge distribution  
**Bundle Optimization**: Code splitting with lazy loading  
**Memory Management**: Automatic garbage collection with memory profiling  

### Monitoring & Observability
**Real-Time Metrics**: Live performance dashboards with alerting  
**Function Monitoring**: Execution time, error rates, memory usage  
**Database Analytics**: Query performance, index usage, storage metrics  
**User Experience**: Real-time user journey tracking with performance impact  

## Security & Compliance

### Authentication & Authorization
**Built-in Auth**: OAuth integration with custom provider support  
**Role-Based Access**: Granular permissions with function-level security  
**Session Management**: Secure session handling with automatic refresh  
**API Security**: Request validation with rate limiting and abuse detection  

### Data Protection
**End-to-End Encryption**: Client-to-server encryption with key management  
**Data Isolation**: Tenant-based isolation with secure multi-tenancy  
**PII Protection**: Automatic PII detection with encryption and masking  
**Audit Logging**: Comprehensive activity logging with tamper protection  

### Infrastructure Security
**Network Security**: VPC isolation with private networking options  
**Container Security**: Secure function execution with sandboxing  
**Certificate Management**: Automatic SSL/TLS with certificate rotation  
**Vulnerability Management**: Regular security scanning with update notifications  

### Compliance Features
**Data Residency**: Regional data placement with compliance enforcement  
**GDPR Compliance**: Data subject rights with automated data deletion  
**SOC 2 Ready**: Security controls with audit trail preparation  
**Privacy Controls**: Data processing transparency with consent management  

## Troubleshooting Guide

### Common Issues & Solutions

#### Real-Time Synchronization Problems
**Issue**: Updates not propagating or delayed synchronization  
**Diagnosis**: Check WebSocket connectivity, query subscription status, network latency  
**Solution**: Implement connection retry logic, optimize query parameters, check rate limits  
**Prevention**: Monitor connection health, implement graceful degradation  

#### Function Execution Failures
**Issue**: Function timeouts or execution errors  
**Diagnosis**: Review function logs, check memory usage, analyze execution time  
**Solution**: Optimize function code, increase timeout limits, implement error handling  
**Prevention**: Performance testing, memory profiling, error monitoring  

#### Performance Degradation
**Issue**: Slow query responses or high latency  
**Diagnosis**: Analyze query patterns, check index usage, monitor system resources  
**Solution**: Optimize queries, create appropriate indexes, implement caching  
**Prevention**: Regular performance monitoring, query optimization reviews  

### Debug Commands & Tools
```bash
# Local development debugging
npx convex dev --debug

# Function execution analysis
npx convex logs --function messages:send --tail

# Performance profiling
npx convex dashboard --metrics

# Database query analysis
npx convex query --explain messages:list
```

### Monitoring & Logging
**Application Logs**: Structured logging with correlation IDs  
**Performance Metrics**: Real-time dashboards with historical trends  
**Error Tracking**: Automatic error collection with stack traces  
**User Analytics**: Usage patterns with performance correlation  

## Business Value & ROI Analysis

### Development Acceleration
**Time to Market**: 50-70% faster development with integrated backend  
**Feature Velocity**: Real-time features implemented in days vs weeks  
**Code Maintenance**: 60% reduction in backend infrastructure code  
**Testing Efficiency**: Built-in testing tools reduce QA cycle time  

### Operational Benefits
**Infrastructure Management**: Eliminate server management overhead  
**Scalability Planning**: Automatic scaling eliminates capacity planning  
**Monitoring Overhead**: Built-in observability reduces monitoring setup  
**Security Maintenance**: Managed security features reduce security overhead  

### Cost Structure Analysis
**Development Costs**: Reduced by 40-60% through platform efficiency  
**Infrastructure Costs**: Usage-based pricing with automatic optimization  
**Operational Costs**: 70% reduction in DevOps overhead  
**Time-to-Revenue**: Faster feature delivery accelerates revenue generation  


## Implementation Roadmap

### Phase 1: Foundation Setup (Weeks 1-2)
**Objectives**: Establish Convex environment and basic real-time functionality  
**Key Tasks**: Account setup, project initialization, basic query implementation  
**Deliverables**: Working real-time application with MCP integration  
**Success Criteria**: Sub-100ms update propagation with 99.9% uptime  

### Phase 2: Core Features (Weeks 3-4)
**Objectives**: Implement core application features with real-time capabilities  
**Key Tasks**: Database schema design, function development, authentication  
**Deliverables**: Production-ready core features with real-time updates  
**Success Criteria**: Feature completeness with performance targets met  

### Phase 3: Advanced Features (Weeks 5-6)
**Objectives**: Add collaborative features and advanced real-time capabilities  
**Key Tasks**: Conflict resolution, presence tracking, advanced subscriptions  
**Deliverables**: Full collaborative platform with advanced real-time features  
**Success Criteria**: Collaborative features working with conflict resolution  

### Phase 4: Production Optimization (Weeks 7-8)
**Objectives**: Production hardening and performance optimization  
**Key Tasks**: Security review, performance tuning, monitoring setup  
**Deliverables**: Production-ready deployment with comprehensive monitoring  
**Success Criteria**: Enterprise SLAs met with full observability  

## Competitive Analysis

### Convex vs. Firebase/Firestore
**Advantages**: Better TypeScript integration, superior real-time performance, simpler pricing  
**Trade-offs**: Smaller ecosystem vs Firebase's comprehensive platform  
**Use Case Fit**: Better for TypeScript applications requiring real-time collaboration  

### Convex vs. Supabase
**Advantages**: Better real-time capabilities, integrated functions, simpler deployment  
**Trade-offs**: Less SQL compatibility vs Supabase's PostgreSQL foundation  
**Use Case Fit**: Superior for real-time applications vs traditional database needs  

### Convex vs. AWS Amplify
**Advantages**: Simpler architecture, better real-time performance, unified development experience  
**Trade-offs**: Less AWS service integration vs Amplify's comprehensive AWS ecosystem  
**Use Case Fit**: Better for focused real-time applications vs multi-service architectures  

### Convex vs. PlanetScale
**Advantages**: Real-time capabilities, integrated backend, simpler operations  
**Trade-offs**: Less SQL sophistication vs PlanetScale's advanced MySQL features  
**Use Case Fit**: Better for real-time applications vs complex relational database needs  

## Final Recommendations

### Ideal Use Cases
**Primary Fit**: Real-time collaborative applications, live dashboards, chat applications  
**Strong Fit**: Social platforms, gaming backends, IoT dashboards, team collaboration tools  
**Consider Alternatives**: Simple CRUD applications, complex analytical workloads, existing SQL schemas  

### Implementation Strategy
**Start Simple**: Begin with basic real-time queries and mutations  
**Scale Features**: Add collaborative features and advanced real-time capabilities  
**Optimize Performance**: Monitor metrics and optimize based on usage patterns  
**Expand Gradually**: Add complex workflows and integrations over time  

### Success Factors
**Team Training**: Ensure team understands reactive programming concepts  
**Architecture Planning**: Design for real-time from the beginning  
**Performance Monitoring**: Implement comprehensive monitoring early  
**User Experience**: Focus on smooth real-time user experiences  

**Overall Assessment**: Convex provides exceptional value for teams building real-time applications requiring instant updates and collaborative features. Highly recommended for applications where real-time user experience is a primary requirement with strong development velocity benefits.