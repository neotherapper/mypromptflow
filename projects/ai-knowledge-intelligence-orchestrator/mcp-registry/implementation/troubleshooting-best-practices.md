# MCP Server Troubleshooting and Best Practices Guide

## Overview

This comprehensive troubleshooting and best practices guide provides systematic approaches to diagnose, resolve, and prevent common MCP server integration issues based on analysis of 302 servers. The guide includes diagnostic procedures, resolution strategies, preventive measures, and operational best practices for enterprise deployments.

## 🔧 **Common Integration Issues and Solutions**

### **Authentication and Authorization Problems**

#### **OAuth 2.0 Integration Issues**
```yaml
oauth_troubleshooting:
  invalid_grant_errors:
    symptoms:
      - "invalid_grant" error responses
      - "unauthorized_client" errors
      - Token refresh failures
    
    root_causes:
      - expired_authorization_codes: "Authorization codes typically expire in 10 minutes"
      - incorrect_redirect_uri: "Redirect URI must match exactly (including trailing slashes)"
      - client_credentials_mismatch: "Client ID/secret incorrect or for wrong environment"
      - scope_permissions: "Requested scopes not granted or available"
    
    diagnostic_steps:
      1. "Verify authorization code is used within expiration window"
      2. "Check redirect URI exact match in both request and configuration"
      3. "Validate client credentials against server environment"
      4. "Confirm all requested scopes are available and approved"
    
    resolution_strategies:
      - implement_token_refresh: "Proactive token refresh 15 minutes before expiration"
      - error_handling: "Graceful handling of auth failures with user notification"
      - configuration_validation: "Automated validation of OAuth configuration"
      - logging_enhancement: "Detailed logging for OAuth flow debugging"
  
  token_expiration_issues:
    symptoms:
      - Intermittent authentication failures
      - "token_expired" error responses
      - Successful requests followed by auth failures
    
    resolution_strategies:
      automatic_refresh: |
        ```javascript
        const tokenManager = {
          refreshThreshold: 15 * 60 * 1000, // 15 minutes
          async getValidToken() {
            if (this.isTokenExpiringSoon()) {
              await this.refreshToken();
            }
            return this.currentToken;
          },
          isTokenExpiringSoon() {
            return (this.tokenExpiry - Date.now()) < this.refreshThreshold;
          }
        }
        ```
      
      error_recovery: |
        ```javascript
        const apiCall = async (endpoint, options) => {
          try {
            return await fetch(endpoint, options);
          } catch (error) {
            if (error.status === 401) {
              await tokenManager.refreshToken();
              return await fetch(endpoint, {
                ...options,
                headers: {
                  ...options.headers,
                  'Authorization': `Bearer ${tokenManager.currentToken}`
                }
              });
            }
            throw error;
          }
        }
        ```
```

#### **API Key Management Issues**
```yaml
api_key_troubleshooting:
  invalid_key_errors:
    symptoms:
      - "401 Unauthorized" responses
      - "403 Forbidden" for valid keys
      - "API key not found" errors
    
    diagnostic_checklist:
      - [ ] API key format validation (length, character set)
      - [ ] Environment-specific key usage (dev/staging/prod)
      - [ ] Key expiration date verification
      - [ ] IP whitelist configuration check
      - [ ] Rate limit status validation
    
    common_fixes:
      key_rotation: "Implement 90-day key rotation with overlap period"
      environment_management: "Use environment variables for key storage"
      validation_testing: "Automated API key validation in CI/CD"
      secure_storage: "Use HashiCorp Vault or similar for key storage"
  
  rate_limit_exceeded:
    symptoms:
      - "429 Too Many Requests" responses
      - Temporary API access suspension
      - Degraded performance during peak usage
    
    resolution_strategies:
      client_side_limiting: |
        ```javascript
        const rateLimiter = {
          requests: [],
          maxRequests: 100,
          timeWindow: 60000, // 1 minute
          
          async makeRequest(apiCall) {
            await this.waitIfNecessary();
            this.requests.push(Date.now());
            return apiCall();
          },
          
          async waitIfNecessary() {
            const now = Date.now();
            this.requests = this.requests.filter(time => now - time < this.timeWindow);
            
            if (this.requests.length >= this.maxRequests) {
              const oldestRequest = Math.min(...this.requests);
              const waitTime = this.timeWindow - (now - oldestRequest);
              await new Promise(resolve => setTimeout(resolve, waitTime));
            }
          }
        }
        ```
      
      exponential_backoff: |
        ```javascript
        const retryWithBackoff = async (apiCall, maxRetries = 3) => {
          for (let attempt = 0; attempt < maxRetries; attempt++) {
            try {
              return await apiCall();
            } catch (error) {
              if (error.status === 429 && attempt < maxRetries - 1) {
                const backoffTime = Math.pow(2, attempt) * 1000 + Math.random() * 1000;
                await new Promise(resolve => setTimeout(resolve, backoffTime));
                continue;
              }
              throw error;
            }
          }
        }
        ```
```

### **Network and Connectivity Issues**

#### **Connection Timeout Problems**
```yaml
connection_troubleshooting:
  timeout_diagnosis:
    symptoms:
      - "Connection timeout" errors
      - Intermittent request failures
      - Slow response times during peak hours
    
    diagnostic_steps:
      network_analysis:
        1. "Test network connectivity using ping and traceroute"
        2. "Verify DNS resolution for API endpoints"
        3. "Check for firewall or proxy interference"
        4. "Analyze network latency patterns over time"
      
      server_analysis:
        1. "Check server status pages and incident reports"
        2. "Verify API endpoint availability with curl/wget"
        3. "Test from multiple geographic locations"
        4. "Monitor response time patterns across different endpoints"
    
    resolution_strategies:
      timeout_configuration: |
        ```javascript
        const httpClient = axios.create({
          timeout: 30000, // 30 second timeout
          retry: 3,
          retryDelay: (retryCount) => {
            return Math.pow(2, retryCount) * 1000; // exponential backoff
          },
          retryCondition: (error) => {
            return error.code === 'ECONNRESET' || 
                   error.code === 'ETIMEDOUT' ||
                   (error.response && error.response.status >= 500);
          }
        });
        ```
      
      connection_pooling: |
        ```javascript
        const https = require('https');
        const agent = new https.Agent({
          keepAlive: true,
          keepAliveMsecs: 30000,
          maxSockets: 50,
          maxFreeSockets: 10,
          timeout: 60000
        });
        ```
  
  ssl_certificate_issues:
    symptoms:
      - "SSL certificate verification failed"
      - "Certificate has expired" errors
      - "Hostname verification failed"
    
    diagnostic_commands:
      - certificate_check: "openssl s_client -connect api.server.com:443 -servername api.server.com"
      - expiration_check: "echo | openssl s_client -connect api.server.com:443 | openssl x509 -noout -dates"
      - chain_validation: "openssl s_client -connect api.server.com:443 -verify_return_error"
    
    resolution_approaches:
      certificate_pinning: "Implement certificate pinning for enhanced security"
      monitoring: "Automated certificate expiration monitoring"
      fallback_endpoints: "Configure backup endpoints with valid certificates"
```

### **Data and Response Issues**

#### **Data Validation and Parsing Problems**
```yaml
data_troubleshooting:
  json_parsing_errors:
    symptoms:
      - "Unexpected token" in JSON parsing
      - "Invalid JSON" error messages
      - Partial data extraction from responses
    
    diagnostic_approach:
      response_analysis:
        1. "Log raw API responses for inspection"
        2. "Validate JSON structure with online validators"
        3. "Check for non-printable characters or encoding issues"
        4. "Verify Content-Type headers match response format"
      
      data_validation:
        1. "Implement schema validation for expected response structure"
        2. "Add type checking for critical data fields"
        3. "Validate data ranges and constraints"
        4. "Check for null or undefined values in critical fields"
    
    prevention_strategies:
      robust_parsing: |
        ```javascript
        const safeJSONParse = (jsonString) => {
          try {
            // Remove BOM and clean whitespace
            const cleanedJson = jsonString.replace(/^\uFEFF/, '').trim();
            const parsed = JSON.parse(cleanedJson);
            
            // Validate expected structure
            if (!parsed || typeof parsed !== 'object') {
              throw new Error('Invalid JSON structure');
            }
            
            return parsed;
          } catch (error) {
            console.error('JSON parsing failed:', {
              error: error.message,
              rawData: jsonString.substring(0, 500) + '...'
            });
            throw new Error(`Failed to parse JSON response: ${error.message}`);
          }
        }
        ```
      
      schema_validation: |
        ```javascript
        const Joi = require('joi');
        
        const apiResponseSchema = Joi.object({
          data: Joi.array().required(),
          status: Joi.string().valid('success', 'error').required(),
          timestamp: Joi.date().iso().required(),
          pagination: Joi.object({
            page: Joi.number().integer().min(1),
            limit: Joi.number().integer().min(1).max(1000),
            total: Joi.number().integer().min(0)
          }).optional()
        });
        
        const validateResponse = (response) => {
          const { error, value } = apiResponseSchema.validate(response);
          if (error) {
            throw new Error(`Response validation failed: ${error.message}`);
          }
          return value;
        }
        ```
  
  encoding_charset_issues:
    symptoms:
      - Garbled text or special characters
      - "Invalid character encoding" errors
      - Missing or corrupted non-ASCII characters
    
    resolution_strategies:
      encoding_detection: |
        ```javascript
        const detectEncoding = (buffer) => {
          // Check for BOM
          if (buffer.length >= 3 && 
              buffer[0] === 0xEF && buffer[1] === 0xBB && buffer[2] === 0xBF) {
            return 'utf8';
          }
          
          // Check for common encodings
          try {
            const decoded = buffer.toString('utf8');
            if (decoded.includes('�')) {
              return 'latin1'; // fallback for non-UTF8
            }
            return 'utf8';
          } catch (error) {
            return 'binary';
          }
        }
        ```
      
      content_negotiation: |
        ```javascript
        const requestWithEncoding = {
          headers: {
            'Accept': 'application/json; charset=utf-8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Charset': 'utf-8'
          },
          responseType: 'arraybuffer', // Get raw bytes
          transformResponse: (data) => {
            const buffer = Buffer.from(data);
            const encoding = detectEncoding(buffer);
            return JSON.parse(buffer.toString(encoding));
          }
        }
        ```
```

## 🛠️ **Server-Specific Troubleshooting Guides**

### **High-Priority Server Issues**

#### **Redis (9.18) Troubleshooting**
```yaml
redis_troubleshooting:
  memory_issues:
    out_of_memory_errors:
      symptoms:
        - "OOM command not allowed when used memory > 'maxmemory'"
        - Slow response times
        - Connection refused errors
      
      diagnostic_commands:
        - memory_info: "redis-cli INFO memory"
        - key_analysis: "redis-cli --bigkeys"
        - memory_usage: "redis-cli MEMORY USAGE <keyname>"
      
      resolution_strategies:
        memory_optimization: |
          # redis.conf optimization
          maxmemory 2gb
          maxmemory-policy allkeys-lru
          
          # Enable RDB compression
          rdbcompression yes
          
          # Optimize data structures
          hash-max-ziplist-entries 512
          hash-max-ziplist-value 64
          list-max-ziplist-entries 512
          list-max-ziplist-value 64
        
        monitoring_setup: |
          ```bash
          # Monitor memory usage
          redis-cli INFO memory | grep used_memory_human
          
          # Monitor key expiration
          redis-cli INFO keyspace
          
          # Check memory fragmentation
          redis-cli INFO memory | grep mem_fragmentation_ratio
          ```
  
  connection_issues:
    connection_pool_exhaustion:
      symptoms:
        - "Too many clients" error
        - Connection timeout errors
        - Intermittent connection failures
      
      resolution_approach:
        connection_management: |
          ```javascript
          const Redis = require('ioredis');
          
          const redis = new Redis({
            host: 'localhost',
            port: 6379,
            maxRetriesPerRequest: 3,
            retryDelayOnFailover: 100,
            enableReadyCheck: false,
            lazyConnect: true,
            keepAlive: 30000,
            connectTimeout: 10000,
            commandTimeout: 5000,
            family: 4
          });
          
          // Connection pool management
          const cluster = new Redis.Cluster([
            { host: '127.0.0.1', port: 7000 },
            { host: '127.0.0.1', port: 7001 }
          ], {
            enableOfflineQueue: false,
            maxRetriesPerRequest: 2,
            slotsRefreshTimeout: 10000
          });
          ```
```

#### **PostgreSQL (8.0) Troubleshooting**
```yaml
postgresql_troubleshooting:
  performance_issues:
    slow_queries:
      diagnostic_queries: |
        ```sql
        -- Find slow queries
        SELECT query, mean_time, calls, total_time, mean_time, stddev_time
        FROM pg_stat_statements
        ORDER BY mean_time DESC
        LIMIT 10;
        
        -- Check for unused indexes
        SELECT schemaname, tablename, attname, n_distinct, correlation
        FROM pg_stats
        WHERE tablename = 'your_table'
        ORDER BY n_distinct DESC;
        
        -- Monitor connection activity
        SELECT state, count(*) 
        FROM pg_stat_activity 
        GROUP BY state;
        ```
      
      optimization_strategies:
        query_optimization: |
          -- Use EXPLAIN ANALYZE for query planning
          EXPLAIN (ANALYZE, BUFFERS, VERBOSE) 
          SELECT * FROM users WHERE email = 'user@example.com';
          
          -- Create appropriate indexes
          CREATE INDEX CONCURRENTLY idx_users_email ON users(email);
          
          -- Update table statistics
          ANALYZE users;
        
        configuration_tuning: |
          # postgresql.conf optimizations
          shared_buffers = 256MB        # 25% of RAM
          effective_cache_size = 1GB    # 75% of RAM
          work_mem = 4MB                # Per operation
          maintenance_work_mem = 64MB   # For maintenance operations
          checkpoint_completion_target = 0.9
          wal_buffers = 16MB
          random_page_cost = 1.1        # For SSD storage
  
  connection_issues:
    connection_pool_problems:
      diagnostic_approach:
        monitoring_connections: |
          ```sql
          -- Monitor active connections
          SELECT 
            state,
            count(*) as connection_count,
            max(now() - state_change) as max_duration
          FROM pg_stat_activity 
          WHERE state IS NOT NULL
          GROUP BY state;
          
          -- Check for long-running queries
          SELECT 
            pid,
            user,
            application_name,
            state,
            query_start,
            now() - query_start as duration,
            query
          FROM pg_stat_activity
          WHERE state != 'idle'
          AND now() - query_start > interval '5 minutes'
          ORDER BY query_start;
          ```
      
      resolution_strategies:
        connection_pooling: |
          ```javascript
          const { Pool } = require('pg');
          
          const pool = new Pool({
            user: 'dbuser',
            host: 'database.server.com',
            database: 'mydb',
            password: 'secretpassword',
            port: 5432,
            max: 20, // Maximum number of connections
            min: 2,  // Minimum number of connections
            idle: 10000, // Close connections after 10 seconds of inactivity
            acquire: 60000, // Maximum time to get connection
            evict: 1000 // Check for idle connections every second
          });
          
          // Graceful connection handling
          const queryWithRetry = async (text, params, retries = 3) => {
            for (let attempt = 0; attempt < retries; attempt++) {
              try {
                const client = await pool.connect();
                try {
                  const result = await client.query(text, params);
                  return result;
                } finally {
                  client.release();
                }
              } catch (error) {
                if (attempt === retries - 1) throw error;
                await new Promise(resolve => setTimeout(resolve, 1000 * Math.pow(2, attempt)));
              }
            }
          }
          ```
```

### **API-Based Server Troubleshooting**

#### **Stripe (8.4) Payment Processing Issues**
```yaml
stripe_troubleshooting:
  payment_failures:
    card_declined_errors:
      common_decline_codes:
        - insufficient_funds: "Customer's bank account has insufficient funds"
        - card_declined: "Generic decline by issuing bank"
        - expired_card: "Card has expired"
        - incorrect_cvc: "CVC verification failed"
        - processing_error: "Temporary processing issue"
      
      error_handling_strategy: |
        ```javascript
        const handlePaymentError = (error) => {
          switch (error.decline_code) {
            case 'insufficient_funds':
              return {
                message: 'Your card has insufficient funds. Please use a different payment method.',
                retryable: false,
                userAction: 'change_payment_method'
              };
            
            case 'card_declined':
              return {
                message: 'Your card was declined. Please contact your bank or try another card.',
                retryable: false,
                userAction: 'contact_bank_or_change_card'
              };
            
            case 'processing_error':
              return {
                message: 'A temporary error occurred. Please try again in a moment.',
                retryable: true,
                userAction: 'retry_later'
              };
            
            default:
              return {
                message: 'Payment could not be processed. Please try a different payment method.',
                retryable: false,
                userAction: 'change_payment_method'
              };
          }
        }
        ```
  
  webhook_reliability:
    webhook_verification_issues:
      verification_implementation: |
        ```javascript
        const crypto = require('crypto');
        
        const verifyWebhookSignature = (payload, signature, secret) => {
          const expectedSignature = crypto
            .createHmac('sha256', secret)
            .update(payload, 'utf8')
            .digest('hex');
          
          const providedSignature = signature.split('=')[1];
          
          // Use timing-safe comparison
          return crypto.timingSafeEqual(
            Buffer.from(expectedSignature, 'hex'),
            Buffer.from(providedSignature, 'hex')
          );
        }
        
        // Express middleware for webhook handling
        const handleStripeWebhook = (req, res, next) => {
          const signature = req.headers['stripe-signature'];
          const payload = req.body;
          
          if (!verifyWebhookSignature(payload, signature, process.env.STRIPE_WEBHOOK_SECRET)) {
            return res.status(400).send('Webhook signature verification failed');
          }
          
          // Process webhook event
          const event = JSON.parse(payload);
          processWebhookEvent(event);
          
          res.status(200).send('Webhook received');
        }
        ```
    
    idempotency_handling:
      implementation_strategy: |
        ```javascript
        const processPaymentWithIdempotency = async (paymentData, idempotencyKey) => {
          try {
            const paymentIntent = await stripe.paymentIntents.create({
              amount: paymentData.amount,
              currency: paymentData.currency,
              customer: paymentData.customerId,
              payment_method: paymentData.paymentMethodId,
              confirmation_method: 'manual',
              confirm: true
            }, {
              idempotencyKey: idempotencyKey // Ensures safe retries
            });
            
            return paymentIntent;
          } catch (error) {
            if (error.type === 'idempotency_error') {
              // Retrieve the original request result
              return await stripe.paymentIntents.retrieve(error.payment_intent.id);
            }
            throw error;
          }
        }
        ```
```

## 📋 **Operational Best Practices**

### **Monitoring and Alerting Framework**

#### **Proactive Monitoring Setup**
```yaml
monitoring_best_practices:
  health_check_implementation:
    comprehensive_health_checks: |
      ```javascript
      const healthCheck = {
        async checkMCPServerHealth(serverConfig) {
          const checks = {
            connectivity: await this.testConnectivity(serverConfig),
            authentication: await this.testAuthentication(serverConfig),
            basicOperations: await this.testBasicOperations(serverConfig),
            performance: await this.testResponseTime(serverConfig)
          };
          
          const overallHealth = Object.values(checks).every(check => check.status === 'healthy');
          
          return {
            server: serverConfig.name,
            status: overallHealth ? 'healthy' : 'unhealthy',
            checks: checks,
            timestamp: new Date().toISOString()
          };
        },
        
        async testConnectivity(config) {
          try {
            const response = await fetch(config.healthEndpoint, {
              timeout: 5000
            });
            return {
              status: response.ok ? 'healthy' : 'unhealthy',
              responseTime: response.headers.get('x-response-time'),
              statusCode: response.status
            };
          } catch (error) {
            return {
              status: 'unhealthy',
              error: error.message
            };
          }
        }
      }
      ```
  
  alerting_configuration:
    critical_alerts:
      - authentication_failures: "Alert when >5% of requests fail authentication"
      - response_time_degradation: "Alert when P95 response time >2x baseline"
      - error_rate_increase: "Alert when error rate >2% for 5+ minutes"
      - rate_limit_approaching: "Alert when rate limit utilization >80%"
    
    alert_implementation: |
      ```javascript
      const alertManager = {
        thresholds: {
          errorRate: 0.02, // 2%
          responseTimeP95: 2000, // 2 seconds
          authFailureRate: 0.05 // 5%
        },
        
        async checkMetrics(metrics) {
          const alerts = [];
          
          if (metrics.errorRate > this.thresholds.errorRate) {
            alerts.push({
              severity: 'high',
              message: `Error rate ${(metrics.errorRate * 100).toFixed(2)}% exceeds threshold`,
              server: metrics.serverName
            });
          }
          
          if (metrics.responseTimeP95 > this.thresholds.responseTimeP95) {
            alerts.push({
              severity: 'medium',
              message: `P95 response time ${metrics.responseTimeP95}ms exceeds threshold`,
              server: metrics.serverName
            });
          }
          
          return alerts;
        }
      }
      ```
```

### **Security Best Practices**

#### **Secure Configuration Management**
```yaml
security_best_practices:
  credential_management:
    secure_storage: |
      ```javascript
      const AWS = require('aws-sdk');
      const secretsManager = new AWS.SecretsManager();
      
      class SecureCredentialManager {
        constructor() {
          this.cache = new Map();
          this.cacheTimeout = 5 * 60 * 1000; // 5 minutes
        }
        
        async getCredentials(secretName) {
          const cached = this.cache.get(secretName);
          if (cached && Date.now() - cached.timestamp < this.cacheTimeout) {
            return cached.value;
          }
          
          try {
            const result = await secretsManager.getSecretValue({
              SecretId: secretName
            }).promise();
            
            const credentials = JSON.parse(result.SecretString);
            
            this.cache.set(secretName, {
              value: credentials,
              timestamp: Date.now()
            });
            
            return credentials;
          } catch (error) {
            console.error(`Failed to retrieve secret ${secretName}:`, error);
            throw error;
          }
        }
        
        // Automatic credential rotation
        async rotateCredentials(secretName, rotationFunction) {
          const newCredentials = await rotationFunction();
          
          await secretsManager.putSecretValue({
            SecretId: secretName,
            SecretString: JSON.stringify(newCredentials)
          }).promise();
          
          // Clear cache to force refresh
          this.cache.delete(secretName);
        }
      }
      ```
  
  api_security_hardening:
    request_validation: |
      ```javascript
      const rateLimit = require('express-rate-limit');
      const helmet = require('helmet');
      
      // Security middleware setup
      app.use(helmet());
      
      // Rate limiting
      const limiter = rateLimit({
        windowMs: 15 * 60 * 1000, // 15 minutes
        max: 100, // limit each IP to 100 requests per windowMs
        message: 'Too many requests from this IP',
        standardHeaders: true,
        legacyHeaders: false
      });
      
      app.use('/api/', limiter);
      
      // Request validation middleware
      const validateRequest = (schema) => {
        return (req, res, next) => {
          const { error } = schema.validate(req.body);
          if (error) {
            return res.status(400).json({
              error: 'Request validation failed',
              details: error.details.map(detail => detail.message)
            });
          }
          next();
        };
      };
      ```
```

### **Performance Optimization Best Practices**

#### **Caching Strategy Implementation**
```yaml
caching_best_practices:
  multi_level_caching: |
    ```javascript
    class MultiLevelCache {
      constructor() {
        this.l1Cache = new Map(); // In-memory cache
        this.l2Cache = redis.createClient(); // Redis cache
        this.l3Cache = null; // Database/persistent storage
      }
      
      async get(key) {
        // L1 Cache (fastest)
        if (this.l1Cache.has(key)) {
          const cached = this.l1Cache.get(key);
          if (Date.now() < cached.expiry) {
            return cached.value;
          }
          this.l1Cache.delete(key);
        }
        
        // L2 Cache (Redis)
        try {
          const redisValue = await this.l2Cache.get(key);
          if (redisValue) {
            const parsed = JSON.parse(redisValue);
            // Promote to L1 cache
            this.l1Cache.set(key, {
              value: parsed,
              expiry: Date.now() + (5 * 60 * 1000) // 5 minutes
            });
            return parsed;
          }
        } catch (error) {
          console.warn('Redis cache miss:', error.message);
        }
        
        // L3 Cache (fallback to source)
        return null;
      }
      
      async set(key, value, ttl = 3600) {
        // Set in all cache levels
        this.l1Cache.set(key, {
          value: value,
          expiry: Date.now() + Math.min(ttl * 1000, 5 * 60 * 1000)
        });
        
        try {
          await this.l2Cache.setex(key, ttl, JSON.stringify(value));
        } catch (error) {
          console.warn('Redis cache set failed:', error.message);
        }
      }
    }
    ```
  
  intelligent_prefetching: |
    ```javascript
    class IntelligentPrefetcher {
      constructor(cache, mcpServer) {
        this.cache = cache;
        this.mcpServer = mcpServer;
        this.accessPatterns = new Map();
      }
      
      recordAccess(key) {
        const pattern = this.accessPatterns.get(key) || {
          count: 0,
          lastAccess: Date.now(),
          frequency: 0
        };
        
        pattern.count++;
        pattern.frequency = pattern.count / (Date.now() - pattern.lastAccess);
        pattern.lastAccess = Date.now();
        
        this.accessPatterns.set(key, pattern);
        
        // Trigger prefetching for related data
        this.schedulePrefetch(key);
      }
      
      async schedulePrefetch(key) {
        const relatedKeys = this.getRelatedKeys(key);
        
        for (const relatedKey of relatedKeys) {
          if (!this.cache.has(relatedKey)) {
            // Prefetch in background
            setImmediate(async () => {
              try {
                const data = await this.mcpServer.fetch(relatedKey);
                await this.cache.set(relatedKey, data);
              } catch (error) {
                console.debug('Prefetch failed for', relatedKey, error.message);
              }
            });
          }
        }
      }
    }
    ```
```

## 🎯 **Troubleshooting Decision Tree**

### **Systematic Problem Resolution**

#### **Issue Classification and Response**
```yaml
troubleshooting_decision_tree:
  initial_assessment:
    issue_categorization:
      - connectivity_issues: "Cannot establish connection to MCP server"
      - authentication_issues: "Valid connection but authentication failures"
      - data_issues: "Connected and authenticated but data problems"
      - performance_issues: "Everything works but too slowly"
      - intermittent_issues: "Works sometimes, fails other times"
  
  connectivity_troubleshooting:
    immediate_actions:
      1. "Test basic network connectivity (ping, traceroute)"
      2. "Verify DNS resolution for server endpoints"
      3. "Check firewall and proxy configurations"
      4. "Validate SSL/TLS certificate chain"
      5. "Test from different network locations"
    
    escalation_path:
      - level_1: "Network administrator involvement"
      - level_2: "MCP server vendor support"
      - level_3: "Infrastructure team escalation"
  
  authentication_troubleshooting:
    systematic_approach:
      1. "Verify credentials in appropriate environment"
      2. "Check credential expiration and rotation status"
      3. "Validate API key or token format and permissions"
      4. "Test authentication flow step-by-step"
      5. "Review audit logs for authentication patterns"
    
    resolution_timeline:
      - immediate: "Credential validation and refresh"
      - short_term: "Authentication flow debugging"
      - long_term: "Automated credential management implementation"
```

### **Escalation Procedures**

#### **Support Escalation Matrix**
```yaml
escalation_procedures:
  internal_escalation:
    tier_1_support:
      - scope: "Standard troubleshooting procedures"
      - escalation_criteria: "Issue not resolved within 2 hours"
      - required_documentation: "Problem description, steps taken, error logs"
    
    tier_2_support:
      - scope: "Advanced technical analysis and vendor coordination"
      - escalation_criteria: "Issue not resolved within 8 hours or business critical"
      - required_documentation: "Complete diagnostic data, business impact assessment"
    
    tier_3_support:
      - scope: "Architecture review and strategic resolution planning"
      - escalation_criteria: "Issue requires architectural changes or vendor escalation"
      - required_documentation: "Root cause analysis, proposed solutions, cost-benefit analysis"
  
  vendor_escalation:
    escalation_triggers:
      - server_outage: "MCP server unavailable for >30 minutes during business hours"
      - data_corruption: "Data integrity issues or data loss detected"
      - security_incident: "Suspected security breach or vulnerability"
      - performance_degradation: "Performance below SLA for >2 hours"
    
    required_information:
      - account_details: "Account ID, subscription level, contact information"
      - technical_details: "Error messages, request/response samples, timestamps"
      - business_impact: "Affected users, revenue impact, criticality assessment"
      - troubleshooting_performed: "Steps taken, diagnostic data collected"
```

This comprehensive troubleshooting and best practices guide provides systematic approaches to diagnose, resolve, and prevent common MCP server integration issues, enabling organizations to maintain reliable and high-performing MCP server deployments.