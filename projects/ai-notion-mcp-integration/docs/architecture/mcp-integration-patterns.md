# MCP Integration Patterns and Implementation Guide

## JSON-RPC 2.0 Implementation Details

### Protocol Stack Architecture
```yaml
protocol_implementation:
  transport_layer:
    primary: "streamable_http"
    fallback: "server_sent_events"
    endpoint: "http://127.0.0.1:3845/sse"
    connection_management: "persistent_with_reconnect"
    
  message_format:
    protocol: "json_rpc_2.0"
    encoding: "utf-8"
    compression: "gzip_optional"
    max_message_size: "10MB"
    
  session_management:
    stateful: true
    session_timeout: "30m"
    keepalive_interval: "5m"
    auto_reconnect: true
```

### MCP Server Configuration Patterns
```typescript
// MCP Server Configuration
interface MCPServerConfig {
  name: "notion-integration";
  version: "1.0.0";
  transport: {
    type: "streamable_http";
    port: 3845;
    host: "127.0.0.1";
    cors: {
      origin: ["vscode://", "cursor://", "claude://"];
      credentials: true;
    };
  };
  capabilities: {
    resources: true;
    tools: true;
    prompts: true;
    logging: true;
  };
  authentication: {
    type: "oauth2";
    provider: "notion";
    required_scopes: ["read", "write"];
  };
}
```

### Tool Implementation Patterns
```typescript
// Database Query Tool
export const queryDatabaseTool: Tool = {
  name: "query_database",
  description: "Query Notion database with filters and sorting",
  inputSchema: {
    type: "object",
    properties: {
      database_id: {
        type: "string",
        description: "Database identifier"
      },
      filter: {
        type: "object",
        description: "Query filter conditions"
      },
      sort: {
        type: "array",
        description: "Sort specifications"
      },
      limit: {
        type: "number",
        default: 100,
        maximum: 1000
      }
    },
    required: ["database_id"]
  }
};

// Implementation with error handling
async function handleQueryDatabase(params: QueryDatabaseParams): Promise<ToolResult> {
  try {
    const startTime = Date.now();
    
    const response = await notionClient.databases.query({
      database_id: params.database_id,
      filter: params.filter,
      sorts: params.sort,
      page_size: Math.min(params.limit || 100, 1000)
    });
    
    const processingTime = Date.now() - startTime;
    
    // Performance validation
    if (processingTime > 500) {
      console.warn(`Query exceeded 500ms target: ${processingTime}ms`);
    }
    
    return {
      content: [{
        type: "text",
        text: formatDatabaseResults(response)
      }],
      metadata: {
        processing_time_ms: processingTime,
        result_count: response.results.length,
        has_more: response.has_more
      }
    };
  } catch (error) {
    return {
      content: [{
        type: "text", 
        text: `Error querying database: ${error.message}`
      }],
      isError: true
    };
  }
}
```

## Performance Optimization Strategies

### Connection Management Optimization
```typescript
// Connection Pool Management
class MCPConnectionManager {
  private connections: Map<string, WebSocket> = new Map();
  private reconnectAttempts: Map<string, number> = new Map();
  private maxReconnectAttempts = 5;
  private reconnectDelay = 1000; // Start with 1s delay
  
  async getConnection(clientId: string): Promise<WebSocket> {
    if (this.connections.has(clientId)) {
      const conn = this.connections.get(clientId)!;
      if (conn.readyState === WebSocket.OPEN) {
        return conn;
      }
    }
    
    return this.createConnection(clientId);
  }
  
  private async createConnection(clientId: string): Promise<WebSocket> {
    const ws = new WebSocket('ws://127.0.0.1:3845/ws');
    
    ws.on('open', () => {
      this.connections.set(clientId, ws);
      this.reconnectAttempts.delete(clientId);
      console.log(`MCP connection established for ${clientId}`);
    });
    
    ws.on('close', () => {
      this.handleReconnection(clientId);
    });
    
    ws.on('error', (error) => {
      console.error(`MCP connection error for ${clientId}:`, error);
      this.handleReconnection(clientId);
    });
    
    return ws;
  }
  
  private async handleReconnection(clientId: string): Promise<void> {
    const attempts = this.reconnectAttempts.get(clientId) || 0;
    
    if (attempts < this.maxReconnectAttempts) {
      this.reconnectAttempts.set(clientId, attempts + 1);
      const delay = this.reconnectDelay * Math.pow(2, attempts); // Exponential backoff
      
      setTimeout(() => {
        this.createConnection(clientId);
      }, delay);
    }
  }
}
```

### Batch Request Optimization
```typescript
// Batch Request Handler
interface BatchRequest {
  id: string;
  method: string;
  params: any;
  timestamp: number;
}

class BatchRequestProcessor {
  private batchQueue: BatchRequest[] = [];
  private batchSize = 10;
  private batchTimeout = 100; // 100ms batching window
  private processingTimeout: NodeJS.Timeout | null = null;
  
  async addRequest(request: BatchRequest): Promise<any> {
    return new Promise((resolve, reject) => {
      this.batchQueue.push({
        ...request,
        resolve,
        reject
      } as any);
      
      this.scheduleBatchProcessing();
    });
  }
  
  private scheduleBatchProcessing(): void {
    if (this.processingTimeout) {
      clearTimeout(this.processingTimeout);
    }
    
    if (this.batchQueue.length >= this.batchSize) {
      this.processBatch();
    } else {
      this.processingTimeout = setTimeout(() => {
        this.processBatch();
      }, this.batchTimeout);
    }
  }
  
  private async processBatch(): Promise<void> {
    if (this.batchQueue.length === 0) return;
    
    const batch = this.batchQueue.splice(0, this.batchSize);
    const batchRequest = {
      jsonrpc: "2.0",
      method: "batch",
      params: batch.map(req => ({
        id: req.id,
        method: req.method,
        params: req.params
      })),
      id: `batch_${Date.now()}`
    };
    
    try {
      const startTime = Date.now();
      const response = await this.sendBatchRequest(batchRequest);
      const processingTime = Date.now() - startTime;
      
      // Performance monitoring
      if (processingTime > 500) {
        console.warn(`Batch processing exceeded 500ms: ${processingTime}ms`);
      }
      
      this.handleBatchResponse(batch, response);
    } catch (error) {
      batch.forEach(req => req.reject(error));
    }
  }
}
```

### Caching Strategy Implementation
```typescript
// Multi-Tier Caching System
interface CacheEntry<T> {
  data: T;
  timestamp: number;
  ttl: number;
  accessCount: number;
}

class MultiTierCache {
  private memoryCache = new Map<string, CacheEntry<any>>();
  private memoryCacheSize = 256 * 1024 * 1024; // 256MB
  private diskCacheDir = './cache/notion-mcp';
  
  async get<T>(key: string): Promise<T | null> {
    // Check memory cache first
    const memoryEntry = this.memoryCache.get(key);
    if (memoryEntry && this.isValid(memoryEntry)) {
      memoryEntry.accessCount++;
      return memoryEntry.data;
    }
    
    // Check disk cache
    const diskEntry = await this.getDiskCacheEntry<T>(key);
    if (diskEntry && this.isValid(diskEntry)) {
      // Promote to memory cache
      this.memoryCache.set(key, diskEntry);
      this.evictIfNeeded();
      return diskEntry.data;
    }
    
    return null;
  }
  
  async set<T>(key: string, data: T, ttl: number = 300000): Promise<void> {
    const entry: CacheEntry<T> = {
      data,
      timestamp: Date.now(),
      ttl,
      accessCount: 1
    };
    
    // Store in memory cache
    this.memoryCache.set(key, entry);
    this.evictIfNeeded();
    
    // Store in disk cache for persistence
    await this.setDiskCacheEntry(key, entry);
  }
  
  private isValid<T>(entry: CacheEntry<T>): boolean {
    return Date.now() - entry.timestamp < entry.ttl;
  }
  
  private evictIfNeeded(): void {
    const currentSize = this.estimateMemoryUsage();
    if (currentSize > this.memoryCacheSize) {
      // LRU eviction - remove least recently used items
      const sortedEntries = Array.from(this.memoryCache.entries())
        .sort(([, a], [, b]) => a.accessCount - b.accessCount);
      
      const toRemove = Math.ceil(sortedEntries.length * 0.2); // Remove 20%
      for (let i = 0; i < toRemove; i++) {
        this.memoryCache.delete(sortedEntries[i][0]);
      }
    }
  }
}
```

## Error Handling and Recovery Patterns

### Comprehensive Error Handling
```typescript
// Error Classification and Handling
enum MCPErrorType {
  CONNECTION_ERROR = "connection_error",
  TIMEOUT_ERROR = "timeout_error", 
  RATE_LIMIT_ERROR = "rate_limit_error",
  VALIDATION_ERROR = "validation_error",
  NOTION_API_ERROR = "notion_api_error",
  INTERNAL_ERROR = "internal_error"
}

class MCPErrorHandler {
  private retryAttempts = new Map<string, number>();
  private maxRetries = 3;
  private baseDelay = 1000;
  
  async handleError(error: Error, context: string): Promise<any> {
    const errorType = this.classifyError(error);
    const shouldRetry = this.shouldRetry(errorType, context);
    
    if (shouldRetry) {
      const attempts = this.retryAttempts.get(context) || 0;
      if (attempts < this.maxRetries) {
        this.retryAttempts.set(context, attempts + 1);
        const delay = this.calculateDelay(attempts);
        
        await this.sleep(delay);
        return this.retry(context);
      }
    }
    
    // Reset retry counter
    this.retryAttempts.delete(context);
    
    // Return appropriate error response
    return this.formatErrorResponse(errorType, error, context);
  }
  
  private classifyError(error: Error): MCPErrorType {
    if (error.message.includes('connect')) {
      return MCPErrorType.CONNECTION_ERROR;
    }
    if (error.message.includes('timeout')) {
      return MCPErrorType.TIMEOUT_ERROR;
    }
    if (error.message.includes('rate limit')) {
      return MCPErrorType.RATE_LIMIT_ERROR;
    }
    if (error.message.includes('validation')) {
      return MCPErrorType.VALIDATION_ERROR;
    }
    if (error.message.includes('notion')) {
      return MCPErrorType.NOTION_API_ERROR;
    }
    return MCPErrorType.INTERNAL_ERROR;
  }
  
  private shouldRetry(errorType: MCPErrorType, context: string): boolean {
    const nonRetryableErrors = [
      MCPErrorType.VALIDATION_ERROR,
      MCPErrorType.INTERNAL_ERROR
    ];
    
    return !nonRetryableErrors.includes(errorType);
  }
  
  private calculateDelay(attempt: number): number {
    // Exponential backoff with jitter
    const exponentialDelay = this.baseDelay * Math.pow(2, attempt);
    const jitter = Math.random() * 0.3 * exponentialDelay;
    return exponentialDelay + jitter;
  }
}
```

### Circuit Breaker Pattern
```typescript
// Circuit Breaker Implementation for MCP Services
class CircuitBreaker {
  private failures = 0;
  private successCount = 0;
  private lastFailureTime = 0;
  private state: 'CLOSED' | 'OPEN' | 'HALF_OPEN' = 'CLOSED';
  
  constructor(
    private failureThreshold = 5,
    private recoveryTimeout = 30000, // 30 seconds
    private monitoringWindow = 60000 // 1 minute
  ) {}
  
  async execute<T>(operation: () => Promise<T>): Promise<T> {
    if (this.state === 'OPEN') {
      if (Date.now() - this.lastFailureTime > this.recoveryTimeout) {
        this.state = 'HALF_OPEN';
      } else {
        throw new Error('Circuit breaker is OPEN');
      }
    }
    
    try {
      const result = await operation();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }
  
  private onSuccess(): void {
    this.failures = 0;
    this.successCount++;
    
    if (this.state === 'HALF_OPEN') {
      this.state = 'CLOSED';
    }
  }
  
  private onFailure(): void {
    this.failures++;
    this.lastFailureTime = Date.now();
    
    if (this.failures >= this.failureThreshold) {
      this.state = 'OPEN';
    }
  }
  
  getState(): string {
    return this.state;
  }
  
  getMetrics(): object {
    return {
      state: this.state,
      failures: this.failures,
      successCount: this.successCount,
      lastFailureTime: this.lastFailureTime
    };
  }
}
```

## Monitoring and Observability

### Performance Monitoring Implementation
```typescript
// Performance Metrics Collection
class MCPPerformanceMonitor {
  private metrics = new Map<string, number[]>();
  private metricTypes = ['response_time', 'memory_usage', 'cpu_usage', 'error_rate'];
  
  recordMetric(type: string, value: number): void {
    if (!this.metrics.has(type)) {
      this.metrics.set(type, []);
    }
    
    const values = this.metrics.get(type)!;
    values.push(value);
    
    // Keep only last 1000 measurements
    if (values.length > 1000) {
      values.shift();
    }
    
    this.checkAlerts(type, value);
  }
  
  getMetrics(type: string): { avg: number; p95: number; p99: number } {
    const values = this.metrics.get(type) || [];
    if (values.length === 0) return { avg: 0, p95: 0, p99: 0 };
    
    const sorted = [...values].sort((a, b) => a - b);
    const avg = values.reduce((a, b) => a + b, 0) / values.length;
    const p95 = sorted[Math.floor(sorted.length * 0.95)];
    const p99 = sorted[Math.floor(sorted.length * 0.99)];
    
    return { avg, p95, p99 };
  }
  
  private checkAlerts(type: string, value: number): void {
    const thresholds = {
      response_time: 500, // 500ms
      memory_usage: 512 * 1024 * 1024, // 512MB
      cpu_usage: 70, // 70%
      error_rate: 5 // 5%
    };
    
    if (thresholds[type] && value > thresholds[type]) {
      console.warn(`Alert: ${type} exceeded threshold: ${value} > ${thresholds[type]}`);
      this.triggerAlert(type, value, thresholds[type]);
    }
  }
  
  private triggerAlert(type: string, value: number, threshold: number): void {
    // Implementation for alerting system
    // Could integrate with monitoring platforms like DataDog, New Relic, etc.
  }
}
```

### Health Check Implementation
```typescript
// Comprehensive Health Check System
interface HealthCheckResult {
  status: 'healthy' | 'degraded' | 'unhealthy';
  checks: {
    mcp_server: boolean;
    notion_api: boolean;
    file_system: boolean;
    cache_system: boolean;
  };
  metrics: {
    response_time: number;
    memory_usage: number;
    active_connections: number;
  };
  timestamp: number;
}

class HealthChecker {
  async performHealthCheck(): Promise<HealthCheckResult> {
    const startTime = Date.now();
    
    const checks = {
      mcp_server: await this.checkMCPServer(),
      notion_api: await this.checkNotionAPI(),
      file_system: await this.checkFileSystem(),
      cache_system: await this.checkCacheSystem()
    };
    
    const responseTime = Date.now() - startTime;
    const status = this.determineOverallStatus(checks);
    
    return {
      status,
      checks,
      metrics: {
        response_time: responseTime,
        memory_usage: process.memoryUsage().heapUsed,
        active_connections: this.getActiveConnections()
      },
      timestamp: Date.now()
    };
  }
  
  private async checkMCPServer(): Promise<boolean> {
    try {
      // Perform a simple ping to MCP server
      const response = await fetch('http://127.0.0.1:3845/health');
      return response.ok;
    } catch {
      return false;
    }
  }
  
  private async checkNotionAPI(): Promise<boolean> {
    try {
      // Simple API call to verify connection
      await notionClient.users.me();
      return true;
    } catch {
      return false;
    }
  }
  
  private async checkFileSystem(): Promise<boolean> {
    try {
      // Check if knowledge vault is accessible
      await fs.access('./knowledge-vault', fs.constants.R_OK | fs.constants.W_OK);
      return true;
    } catch {
      return false;
    }
  }
  
  private async checkCacheSystem(): Promise<boolean> {
    try {
      // Test cache read/write
      await cache.set('health_check', 'test');
      const result = await cache.get('health_check');
      return result === 'test';
    } catch {
      return false;
    }
  }
  
  private determineOverallStatus(checks: any): 'healthy' | 'degraded' | 'unhealthy' {
    const failedChecks = Object.values(checks).filter(check => !check).length;
    
    if (failedChecks === 0) return 'healthy';
    if (failedChecks <= 1) return 'degraded';
    return 'unhealthy';
  }
}
```

## Security Implementation

### Authentication and Authorization
```typescript
// OAuth2 Implementation for Notion Integration
class NotionOAuthManager {
  private clientId: string;
  private clientSecret: string;
  private redirectUri: string;
  private tokenStorage: TokenStorage;
  
  constructor(config: OAuthConfig) {
    this.clientId = config.clientId;
    this.clientSecret = config.clientSecret;
    this.redirectUri = config.redirectUri;
    this.tokenStorage = new SecureTokenStorage(config.encryptionKey);
  }
  
  async initializeAuth(): Promise<string> {
    const state = this.generateSecureState();
    const authUrl = `https://api.notion.com/v1/oauth/authorize?` +
      `client_id=${this.clientId}&` +
      `response_type=code&` +
      `redirect_uri=${encodeURIComponent(this.redirectUri)}&` +
      `state=${state}`;
    
    return authUrl;
  }
  
  async handleCallback(code: string, state: string): Promise<void> {
    if (!this.validateState(state)) {
      throw new Error('Invalid state parameter');
    }
    
    const tokenResponse = await this.exchangeCodeForToken(code);
    await this.tokenStorage.store(tokenResponse);
  }
  
  private async exchangeCodeForToken(code: string): Promise<TokenResponse> {
    const response = await fetch('https://api.notion.com/v1/oauth/token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Basic ${Buffer.from(`${this.clientId}:${this.clientSecret}`).toString('base64')}`
      },
      body: JSON.stringify({
        grant_type: 'authorization_code',
        code,
        redirect_uri: this.redirectUri
      })
    });
    
    if (!response.ok) {
      throw new Error(`Token exchange failed: ${response.statusText}`);
    }
    
    return response.json();
  }
  
  async getValidToken(): Promise<string> {
    const token = await this.tokenStorage.retrieve();
    
    if (this.isTokenExpired(token)) {
      const refreshedToken = await this.refreshToken(token.refresh_token);
      await this.tokenStorage.store(refreshedToken);
      return refreshedToken.access_token;
    }
    
    return token.access_token;
  }
}
```

### Request Validation and Sanitization
```typescript
// Input Validation and Sanitization
import { z } from 'zod';

const DatabaseQuerySchema = z.object({
  database_id: z.string().min(1).max(100),
  filter: z.object({}).optional(),
  sort: z.array(z.object({
    property: z.string(),
    direction: z.enum(['ascending', 'descending'])
  })).optional(),
  limit: z.number().min(1).max(1000).optional()
});

class InputValidator {
  static validateDatabaseQuery(input: any): DatabaseQueryParams {
    try {
      return DatabaseQuerySchema.parse(input);
    } catch (error) {
      throw new ValidationError(`Invalid database query parameters: ${error.message}`);
    }
  }
  
  static sanitizeString(input: string): string {
    // Remove potentially dangerous characters
    return input
      .replace(/[<>]/g, '') // Remove HTML brackets
      .replace(/javascript:/gi, '') // Remove javascript protocols
      .replace(/data:/gi, '') // Remove data protocols
      .trim()
      .substring(0, 1000); // Limit length
  }
  
  static validateFileSystemPath(path: string): boolean {
    // Prevent directory traversal attacks
    const normalizedPath = path.replace(/\\/g, '/');
    const forbiddenPatterns = [
      '../',
      '..\\',
      '/..',
      '\\..',
      '/etc/',
      '/proc/',
      'C:\\Windows',
      'C:\\Program Files'
    ];
    
    return !forbiddenPatterns.some(pattern => 
      normalizedPath.toLowerCase().includes(pattern.toLowerCase())
    );
  }
}
```

This comprehensive MCP integration patterns guide provides the technical foundation for implementing JSON-RPC 2.0 communications, performance optimization strategies, and security measures essential for the AI Notion MCP Integration project.