# Performance Testing Context - For AI Agent Performance Specialists

## Current Performance Testing Context

**Modern Performance Testing Stack** (2025-07-25)
- **Load Testing**: Artillery.js, k6, JMeter, Gatling
- **Browser Performance**: Lighthouse CI, WebPageTest, Playwright Performance
- **Monitoring**: New Relic, DataDog, Grafana, Prometheus
- **Profiling**: Chrome DevTools, Node.js Inspector, memory profilers

## Performance Testing Architecture

### 1. Performance Testing Pyramid

```typescript
// Performance testing strategy framework
interface PerformanceTestingPyramid {
  // Unit Performance Tests (60%) (Source: Performance testing pyramid adapted from Google Testing Blog)
  unitPerformanceTests: {
    scope: 'Individual functions, algorithms, data structures';
    characteristics: 'Fast execution, isolated, repeatable';
    tools: 'Benchmark.js, Vitest bench, Jest performance';
    metrics: 'Execution time, memory usage, CPU cycles';
    thresholds: 'Function execution <1ms, memory growth <1MB (Source: V8 JavaScript engine performance guidelines)';
    automation: 'Run with every commit in CI/CD';
  };

  // Integration Performance Tests (30%) (Source: Performance testing pyramid adapted from Google Testing Blog)
  integrationPerformanceTests: {
    scope: 'API endpoints, database queries, service interactions';
    characteristics: 'Realistic dependencies, controlled load';
    tools: 'Artillery, k6, Supertest with timing';
    metrics: 'Response times, throughput, resource utilization';
    thresholds: 'API responses <200ms p95, DB queries <100ms (Source: HTTP response time standards and database performance best practices)';
    automation: 'Run on feature branches and staging';
  };

  // End-to-End Performance Tests (10%) (Source: Performance testing pyramid adapted from Google Testing Blog)
  e2ePerformanceTests: {
    scope: 'Complete user workflows, full system load';
    characteristics: 'Production-like environment, real user patterns';
    tools: 'Lighthouse CI, WebPageTest, k6 with browser';
    metrics: 'Core Web Vitals, user journey times, system capacity';
    thresholds: 'LCP <2.5s, FID <100ms, CLS <0.1 (Source: Google Core Web Vitals thresholds)';
    automation: 'Run before production deployments';
  };
}

// Performance test execution strategy
const performanceTestStrategy = {
  // Continuous performance testing
  continuousPerformance: {
    commitLevel: 'Unit performance tests only',
    pullRequestLevel: 'Unit + critical integration tests',
    stagingLevel: 'Full performance test suite',
    productionLevel: 'Synthetic monitoring + alerting'
  },

  // Performance budgets
  performanceBudgets: {
    frontend: {
      bundleSize: '500KB gzipped',
      loadTime: '3s on 3G',
      interactiveTime: '5s on 3G',
      coreWebVitals: 'LCP <2.5s, FID <100ms, CLS <0.1 (Source: Google Core Web Vitals)'
    },
    backend: {
      apiResponse: 'p95 <200ms, p99 <500ms (Source: HTTP API performance standards)',
      databaseQueries: 'p95 <100ms, p99 <300ms (Source: Database performance best practices)',
      throughput: '1000 RPS sustained (Measured using: Load testing tools with sustained load patterns)',
      errorRate: '<0.1% under normal load (Source: SRE error budget best practices)'
    },
    infrastructure: {
      cpuUtilization: '<70% under normal load',
      memoryUtilization: '<80% under normal load',
      diskIO: '<80% of capacity',
      networkLatency: '<50ms between services'
    }
  }
};
```

### 2. Load Testing Implementation

```typescript
// k6 load testing examples
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate, Trend, Counter } from 'k6/metrics';

// Custom metrics
const errorRate = new Rate('error_rate');
const responseTime = new Trend('response_time');
const requestCount = new Counter('request_count');

// Load testing configuration
export const options = {
  stages: [
    // Ramp-up: gradually increase load
    { duration: '5m', target: 10 },   // Ramp-up to 10 VUs over 5 minutes
    { duration: '10m', target: 50 },  // Ramp-up to 50 VUs over 10 minutes
    { duration: '15m', target: 100 }, // Ramp-up to 100 VUs over 15 minutes
    
    // Sustained load
    { duration: '30m', target: 100 }, // Stay at 100 VUs for 30 minutes
    
    // Peak load testing
    { duration: '5m', target: 200 },  // Spike to 200 VUs
    { duration: '10m', target: 200 }, // Sustain peak load
    
    // Ramp-down
    { duration: '10m', target: 0 },   // Ramp-down to 0 VUs
  ],
  
  thresholds: {
    // Response time thresholds
    'http_req_duration': ['p(95)<200', 'p(99)<500'],
    
    // Error rate thresholds
    'error_rate': ['rate<0.01'], // Error rate should be less than 1%
    
    // Custom metric thresholds
    'response_time': ['p(95)<300'],
    
    // Checks should pass 99% of the time
    'checks': ['rate>0.99'],
  },
};

// Test data and configuration
const config = {
  baseUrl: __ENV.BASE_URL || 'https://api.example.com',
  apiKey: __ENV.API_KEY || 'test-api-key',
};

// Realistic test data
const testData = {
  users: [
    { email: 'user1@example.com', name: 'Test User 1' },
    { email: 'user2@example.com', name: 'Test User 2' },
    { email: 'user3@example.com', name: 'Test User 3' },
  ],
  
  products: [
    { id: 'prod-1', name: 'Product 1', price: 99.99 },
    { id: 'prod-2', name: 'Product 2', price: 149.99 },
    { id: 'prod-3', name: 'Product 3', price: 199.99 },
  ]
};

// Authentication helper
function authenticate() {
  const authResponse = http.post(`${config.baseUrl}/auth/login`, {
    email: 'test@example.com',
    password: 'test-password'
  }, {
    headers: { 'Content-Type': 'application/json' }
  });
  
  check(authResponse, {
    'authentication successful': (r) => r.status === 200,
    'token received': (r) => r.json('token') !== undefined,
  });
  
  return authResponse.json('token');
}

// Main test function
export default function() {
  // Authenticate user
  const token = authenticate();
  
  if (!token) {
    errorRate.add(1);
    return;
  }
  
  const headers = {
    'Authorization': `Bearer ${token}`,
    'Content-Type': 'application/json',
  };
  
  // Test scenario 1: Browse products
  const startTime = Date.now();
  
  const productsResponse = http.get(`${config.baseUrl}/products`, { headers });
  
  const responseTimeMs = Date.now() - startTime;
  responseTime.add(responseTimeMs);
  requestCount.add(1);
  
  const success = check(productsResponse, {
    'products endpoint responds': (r) => r.status === 200,
    'products data is valid': (r) => r.json('products').length > 0,
    'response time acceptable': (r) => r.timings.duration < 500,
  });
  
  errorRate.add(!success);
  
  if (!success) return;
  
  // Test scenario 2: Create order (write operation)
  const randomUser = testData.users[Math.floor(Math.random() * testData.users.length)];
  const randomProduct = testData.products[Math.floor(Math.random() * testData.products.length)];
  
  const orderData = {
    userId: randomUser.email,
    items: [
      {
        productId: randomProduct.id,
        quantity: Math.floor(Math.random() * 3) + 1,
        price: randomProduct.price
      }
    ]
  };
  
  const orderResponse = http.post(`${config.baseUrl}/orders`, JSON.stringify(orderData), { headers });
  
  const orderSuccess = check(orderResponse, {
    'order creation successful': (r) => r.status === 201,
    'order has valid ID': (r) => r.json('orderId') !== undefined,
    'order total calculated': (r) => r.json('total') > 0,
  });
  
  errorRate.add(!orderSuccess);
  requestCount.add(1);
  
  // Test scenario 3: Retrieve order details
  if (orderSuccess) {
    const orderId = orderResponse.json('orderId');
    
    const orderDetailsResponse = http.get(`${config.baseUrl}/orders/${orderId}`, { headers });
    
    const detailsSuccess = check(orderDetailsResponse, {
      'order details retrieved': (r) => r.status === 200,
      'order details match': (r) => r.json('id') === orderId,
    });
    
    errorRate.add(!detailsSuccess);
    requestCount.add(1);
  }
  
  // Realistic user behavior: think time between requests
  sleep(Math.random() * 2 + 1); // Sleep 1-3 seconds
}

// Setup and teardown
export function setup() {
  console.log('Starting load test...');
  console.log(`Base URL: ${config.baseUrl}`);
  console.log('Test configuration:', options);
  
  // Verify API is accessible
  const healthCheck = http.get(`${config.baseUrl}/health`);
  if (healthCheck.status !== 200) {
    throw new Error('API health assessment failed');
  }
  
  return { startTime: Date.now() };
}

export function teardown(data) {
  const duration = (Date.now() - data.startTime) / 1000;
  console.log(`Load test completed in ${duration} seconds`);
}
```

### 3. Frontend Performance Testing

```typescript
// Lighthouse CI configuration and custom performance tests
// lighthouse.config.js
module.exports = {
  ci: {
    collect: {
      startServerCommand: 'npm run start:test',
      startServerReadyPattern: 'ready on',
      startServerReadyTimeout: 30000,
      url: [
        'http://localhost:3000',
        'http://localhost:3000/products',
        'http://localhost:3000/checkout',
        'http://localhost:3000/profile'
      ],
      numberOfRuns: 3,
      settings: {
        chromeFlags: '--no-sandbox --headless',
        preset: 'desktop', // or 'perf' for performance-focused audits
        onlyCategories: ['performance'],
        skipAudits: ['screenshot-thumbnails', 'final-screenshot'],
      }
    },
    assert: {
      assertions: {
        'categories:performance': ['error', { minScore: 0.9 }],
        'first-contentful-paint': ['error', { maxNumericValue: 2000 }],
        'largest-contentful-paint': ['error', { maxNumericValue: 2500 }],
        'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
        'total-blocking-time': ['error', { maxNumericValue: 300 }],
        'speed-index': ['error', { maxNumericValue: 3000 }],
        'interactive': ['error', { maxNumericValue: 3000 }],
      }
    },
    upload: {
      target: 'temporary-public-storage',
    }
  }
};

// Custom Playwright performance testing
import { test, expect } from '@playwright/test';
import { injectSpeedInsights } from 'vercel/speed-insights';

interface PerformanceMetrics {
  loadTime: number;
  domContentLoaded: number;
  firstPaint: number;
  firstContentfulPaint: number;
  largestContentfulPaint: number;
  firstInputDelay: number;
  cumulativeLayoutShift: number;
  totalBlockingTime: number;
  timeToInteractive: number;
}

async function measurePerformanceMetrics(page): Promise<PerformanceMetrics> {
  // Inject performance measurement script
  await page.addInitScript(() => {
    window.performanceMetrics = {
      loadTime: 0,
      domContentLoaded: 0,
      firstPaint: 0,
      firstContentfulPaint: 0,
      largestContentfulPaint: 0,
      firstInputDelay: 0,
      cumulativeLayoutShift: 0,
      totalBlockingTime: 0,
      timeToInteractive: 0,
    };

    // Measure basic timing metrics
    window.addEventListener('load', () => {
      const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
      window.performanceMetrics.loadTime = navigation.loadEventEnd - navigation.loadEventStart;
      window.performanceMetrics.domContentLoaded = navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart;
    });

    // Measure paint metrics
    const paintObserver = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if (entry.name === 'first-paint') {
          window.performanceMetrics.firstPaint = entry.startTime;
        } else if (entry.name === 'first-contentful-paint') {
          window.performanceMetrics.firstContentfulPaint = entry.startTime;
        }
      }
    });
    paintObserver.observe({ entryTypes: ['paint'] });

    // Measure Largest Contentful Paint
    const lcpObserver = new PerformanceObserver((list) => {
      const entries = list.getEntries();
      if (entries.length > 0) {
        window.performanceMetrics.largestContentfulPaint = entries[entries.length - 1].startTime;
      }
    });
    lcpObserver.observe({ entryTypes: ['largest-contentful-paint'] });

    // Measure First Input Delay
    const fidObserver = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        window.performanceMetrics.firstInputDelay = entry.processingStart - entry.startTime;
      }
    });
    fidObserver.observe({ entryTypes: ['first-input'] });

    // Measure Cumulative Layout Shift
    let cumulativeLayoutShift = 0;
    const clsObserver = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if (!entry.hadRecentInput) {
          cumulativeLayoutShift += entry.value;
        }
      }
      window.performanceMetrics.cumulativeLayoutShift = cumulativeLayoutShift;
    });
    clsObserver.observe({ entryTypes: ['layout-shift'] });

    // Measure Total Blocking Time
    let totalBlockingTime = 0;
    const tbtObserver = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if (entry.duration > 50) {
          totalBlockingTime += entry.duration - 50;
        }
      }
      window.performanceMetrics.totalBlockingTime = totalBlockingTime;
    });
    tbtObserver.observe({ entryTypes: ['longtask'] });
  });

  return page.evaluate(() => window.performanceMetrics);
}

test.describe('Frontend Performance Tests', () => {
  test('homepage performance meets thresholds', async ({ page }) => {
    // Navigate to homepage
    await page.goto('/');
    
    // Wait for page to be fully loaded
    await page.waitForLoadState('networkidle');
    
    // Measure performance metrics
    const metrics = await measurePerformanceMetrics(page);
    
    // Assert performance thresholds
    expect(metrics.firstContentfulPaint).toBeLessThan(2000); // 2 seconds
    expect(metrics.largestContentfulPaint).toBeLessThan(2500); // 2.5 seconds
    expect(metrics.cumulativeLayoutShift).toBeLessThan(0.1); // 0.1 CLS score
    expect(metrics.firstInputDelay).toBeLessThan(100); // 100ms
    expect(metrics.totalBlockingTime).toBeLessThan(300); // 300ms
    
    console.log('Performance Metrics:', metrics);
  });

  test('product listing page performance', async ({ page }) => {
    await page.goto('/products');
    await page.waitForLoadState('networkidle');
    
    // Measure time to render product list
    const startTime = Date.now();
    await page.waitForSelector('[data-testid="product-list"]');
    const renderTime = Date.now() - startTime;
    
    expect(renderTime).toBeLessThan(1000); // Products should render within 1 second
    
    // Test scroll performance
    const scrollStartTime = Date.now();
    await page.evaluate(() => {
      window.scrollTo(0, document.body.scrollHeight);
    });
    await page.waitForTimeout(100); // Allow for any lazy loading
    const scrollTime = Date.now() - scrollStartTime;
    
    expect(scrollTime).toBeLessThan(500); // Scrolling should be smooth
    
    const metrics = await measurePerformanceMetrics(page);
    expect(metrics.cumulativeLayoutShift).toBeLessThan(0.1);
  });

  test('form interaction performance', async ({ page }) => {
    await page.goto('/contact');
    await page.waitForLoadState('networkidle');
    
    // Measure form interaction responsiveness
    const formInteractions = [
      { selector: '#name', value: 'John Doe' },
      { selector: '#email', value: 'john@example.com' },
      { selector: '#message', value: 'This is a test message for performance testing.' }
    ];
    
    for (const interaction of formInteractions) {
      const startTime = Date.now();
      await page.fill(interaction.selector, interaction.value);
      const fillTime = Date.now() - startTime;
      
      expect(fillTime).toBeLessThan(100); // Form inputs should respond within 100ms
    }
    
    // Measure form submission performance
    const submitStartTime = Date.now();
    await page.click('button[type="submit"]');
    await page.waitForSelector('.success-message', { timeout: 5000 });
    const submitTime = Date.now() - submitStartTime;
    
    expect(submitTime).toBeLessThan(3000); // Form submission should complete within 3 seconds
  });

  test('bundle size and resource loading', async ({ page }) => {
    // Intercept network requests to measure resource sizes
    const resources: Array<{ url: string; size: number; type: string }> = [];
    
    page.on('response', async (response) => {
      const url = response.url();
      const headers = response.headers();
      const contentLength = headers['content-length'];
      
      if (contentLength && (url.includes('.js') || url.includes('.css'))) {
        resources.push({
          url,
          size: parseInt(contentLength),
          type: url.includes('.js') ? 'javascript' : 'css'
        });
      }
    });
    
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    // Calculate total bundle sizes
    const jsSize = resources
      .filter(r => r.type === 'javascript')
      .reduce((total, r) => total + r.size, 0);
    
    const cssSize = resources
      .filter(r => r.type === 'css')
      .reduce((total, r) => total + r.size, 0);
    
    // Assert bundle size thresholds (in bytes)
    expect(jsSize).toBeLessThan(500 * 1024); // 500KB JavaScript
    expect(cssSize).toBeLessThan(100 * 1024); // 100KB CSS
    
    console.log(`JavaScript bundle size: ${(jsSize / 1024).toFixed(2)}KB`);
    console.log(`CSS bundle size: ${(cssSize / 1024).toFixed(2)}KB`);
  });
});

// Memory leak detection
test.describe('Memory Performance Tests', () => {
  test('no memory leaks in SPA navigation', async ({ page }) => {
    await page.goto('/');
    
    // Get initial memory usage
    const initialMemory = await page.evaluate(() => {
      return (performance as any).memory?.usedJSHeapSize || 0;
    });
    
    // Navigate through multiple pages
    const pages = ['/products', '/about', '/contact', '/profile', '/'];
    
    for (let i = 0; i < 5; i++) { // Repeat navigation cycle 5 times
      for (const pagePath of pages) {
        await page.goto(pagePath);
        await page.waitForLoadState('networkidle');
        
        // Force garbage collection if available
        await page.evaluate(() => {
          if ((window as any).gc) {
            (window as any).gc();
          }
        });
      }
    }
    
    // Get final memory usage
    const finalMemory = await page.evaluate(() => {
      return (performance as any).memory?.usedJSHeapSize || 0;
    });
    
    const memoryIncrease = finalMemory - initialMemory;
    const memoryIncreasePercentage = (memoryIncrease / initialMemory) * 100;
    
    // Memory increase should be less than 50% of initial memory
    expect(memoryIncreasePercentage).toBeLessThan(50);
    
    console.log(`Initial memory: ${(initialMemory / 1024 / 1024).toFixed(2)}MB`);
    console.log(`Final memory: ${(finalMemory / 1024 / 1024).toFixed(2)}MB`);
    console.log(`Memory increase: ${memoryIncreasePercentage.toFixed(2)}%`);
  });
});
```

### 4. Database Performance Testing

```typescript
// Database performance testing with realistic scenarios
import { Pool } from 'pg';
import { performance } from 'perf_hooks';

interface DatabasePerformanceMetrics {
  operationType: string;
  executionTime: number;
  rowsAffected: number;
  memoryUsage: number;
  cpuUsage: number;
}

class DatabasePerformanceTester {
  private pool: Pool;
  private metrics: DatabasePerformanceMetrics[] = [];

  constructor(connectionConfig: any) {
    this.pool = new Pool({
      ...connectionConfig,
      max: 20, // Maximum number of connections
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 2000,
    });
  }

  async measureQuery<T>(
    operationType: string,
    query: string,
    params: any[] = []
  ): Promise<{ result: T[]; metrics: DatabasePerformanceMetrics }> {
    const startTime = performance.now();
    const startMemory = process.memoryUsage().heapUsed;
    const startCpu = process.cpuUsage();

    try {
      const result = await this.pool.query(query, params);
      
      const endTime = performance.now();
      const endMemory = process.memoryUsage().heapUsed;
      const endCpu = process.cpuUsage(startCpu);

      const metrics: DatabasePerformanceMetrics = {
        operationType,
        executionTime: endTime - startTime,
        rowsAffected: result.rowCount || 0,
        memoryUsage: endMemory - startMemory,
        cpuUsage: endCpu.user + endCpu.system
      };

      this.metrics.push(metrics);
      return { result: result.rows, metrics };

    } catch (error) {
      const endTime = performance.now();
      const metrics: DatabasePerformanceMetrics = {
        operationType: `${operationType}_ERROR`,
        executionTime: endTime - startTime,
        rowsAffected: 0,
        memoryUsage: 0,
        cpuUsage: 0
      };

      this.metrics.push(metrics);
      throw error;
    }
  }

  async runPerformanceTests(): Promise<void> {
    console.log('Starting database performance tests...');

    // Test 1: Simple SELECT performance
    await this.testSimpleSelects();

    // Test 2: Complex JOIN performance
    await this.testComplexJoins();

    // Test 3: INSERT performance
    await this.testInsertPerformance();

    // Test 4: UPDATE performance
    await this.testUpdatePerformance();

    // Test 5: Index performance
    await this.testIndexPerformance();

    // Test 6: Concurrent operations
    await this.testConcurrentOperations();

    // Generate performance report
    this.generatePerformanceReport();
  }

  private async testSimpleSelects(): Promise<void> {
    console.log('Testing simple SELECT queries...');

    // Test small result set
    const { metrics: smallResultMetrics } = await this.measureQuery(
      'SELECT_SMALL',
      'SELECT * FROM users WHERE status = $1 LIMIT 10',
      ['active']
    );

    expect(smallResultMetrics.executionTime).toBeLessThan(50); // < 50ms

    // Test medium result set
    const { metrics: mediumResultMetrics } = await this.measureQuery(
      'SELECT_MEDIUM',
      'SELECT * FROM orders WHERE created_at >= $1 LIMIT 1000',
      [new Date(Date.now() - 30 * 24 * 60 * 60 * 1000)] // Last 30 days
    );

    expect(mediumResultMetrics.executionTime).toBeLessThan(200); // < 200ms

    // Test large result set
    const { metrics: largeResultMetrics } = await this.measureQuery(
      'SELECT_LARGE',
      'SELECT id, created_at FROM audit_logs WHERE created_at >= $1',
      [new Date(Date.now() - 7 * 24 * 60 * 60 * 1000)] // Last 7 days
    );

    expect(largeResultMetrics.executionTime).toBeLessThan(1000); // < 1s
  }

  private async testComplexJoins(): Promise<void> {
    console.log('Testing complex JOIN queries...');

    const complexQuery = `
      SELECT 
        u.id,
        u.name,
        u.email,
        COUNT(o.id) as order_count,
        SUM(o.total) as total_spent,
        AVG(p.amount) as avg_payment
      FROM users u
      LEFT JOIN orders o ON u.id = o.user_id
      LEFT JOIN payments p ON o.id = p.order_id
      WHERE u.created_at >= $1
      GROUP BY u.id, u.name, u.email
      HAVING COUNT(o.id) > 0
      ORDER BY total_spent DESC
      LIMIT 100
    `;

    const { metrics } = await this.measureQuery(
      'COMPLEX_JOIN',
      complexQuery,
      [new Date(Date.now() - 90 * 24 * 60 * 60 * 1000)] // Last 90 days
    );

    expect(metrics.executionTime).toBeLessThan(500); // < 500ms
  }

  private async testInsertPerformance(): Promise<void> {
    console.log('Testing INSERT performance...');

    // Single insert
    const singleInsertStart = performance.now();
    await this.measureQuery(
      'INSERT_SINGLE',
      'INSERT INTO test_records (name, data, created_at) VALUES ($1, $2, NOW())',
      ['test_record', JSON.stringify({ test: true })]
    );

    // Batch insert
    const batchInsertQuery = `
      INSERT INTO test_records (name, data, created_at)
      SELECT 
        'batch_record_' || generate_series,
        '{"batch": true, "index": ' || generate_series || '}',
        NOW()
      FROM generate_series(1, 1000)
    `;

    const { metrics: batchMetrics } = await this.measureQuery(
      'INSERT_BATCH',
      batchInsertQuery
    );

    expect(batchMetrics.executionTime).toBeLessThan(1000); // < 1s for 1000 records
    expect(batchMetrics.rowsAffected).toBe(1000);
  }

  private async testUpdatePerformance(): Promise<void> {
    console.log('Testing UPDATE performance...');

    // Single record update
    const { metrics: singleUpdateMetrics } = await this.measureQuery(
      'UPDATE_SINGLE',
      'UPDATE users SET last_login = NOW() WHERE id = $1',
      ['user-123']
    );

    expect(singleUpdateMetrics.executionTime).toBeLessThan(50); // < 50ms

    // Bulk update
    const { metrics: bulkUpdateMetrics } = await this.measureQuery(
      'UPDATE_BULK',
      'UPDATE products SET updated_at = NOW() WHERE category = $1',
      ['electronics']
    );

    expect(bulkUpdateMetrics.executionTime).toBeLessThan(500); // < 500ms
  }

  private async testIndexPerformance(): Promise<void> {
    console.log('Testing index performance...');

    // Query with index
    const { metrics: indexedMetrics } = await this.measureQuery(
      'SELECT_INDEXED',
      'SELECT * FROM orders WHERE user_id = $1', // Assuming user_id is indexed
      ['user-123']
    );

    // Query without index (full table scan)
    const { metrics: fullScanMetrics } = await this.measureQuery(
      'SELECT_FULL_SCAN',
      'SELECT * FROM orders WHERE notes LIKE $1', // Assuming notes is not indexed
      ['%urgent%']
    );

    // Indexed query should be significantly faster
    expect(indexedMetrics.executionTime).toBeLessThan(100);
    
    // Log the difference for analysis
    console.log(`Indexed query: ${indexedMetrics.executionTime}ms`);
    console.log(`Full scan query: ${fullScanMetrics.executionTime}ms`);
  }

  private async testConcurrentOperations(): Promise<void> {
    console.log('Testing concurrent operations...');

    const concurrentQueries = Array.from({ length: 20 }, (_, i) =>
      this.measureQuery(
        'CONCURRENT_SELECT',
        'SELECT COUNT(*) FROM orders WHERE user_id = $1',
        [`user-${i % 10}`] // Rotate through 10 different users
      )
    );

    const startTime = performance.now();
    const results = await Promise.all(concurrentQueries);
    const totalTime = performance.now() - startTime;

    // All concurrent queries should complete within 2 seconds
    expect(totalTime).toBeLessThan(2000); // < 2s for 20 concurrent queries

    // Individual queries should still be fast
    results.forEach(({ metrics }) => {
      expect(metrics.executionTime).toBeLessThan(200);
    });

    console.log(`20 concurrent queries completed in ${totalTime}ms`);
  }

  private generatePerformanceReport(): void {
    console.log('\n=== Database Performance Report ===');

    const operationGroups = this.metrics.reduce((groups, metric) => {
      if (!groups[metric.operationType]) {
        groups[metric.operationType] = [];
      }
      groups[metric.operationType].push(metric);
      return groups;
    }, {} as Record<string, DatabasePerformanceMetrics[]>);

    Object.entries(operationGroups).forEach(([operation, metrics]) => {
      const avgTime = metrics.reduce((sum, m) => sum + m.executionTime, 0) / metrics.length;
      const maxTime = Math.max(...metrics.map(m => m.executionTime));
      const minTime = Math.min(...metrics.map(m => m.executionTime));
      const totalRows = metrics.reduce((sum, m) => sum + m.rowsAffected, 0);

      console.log(`\n${operation}:`);
      console.log(`  Count: ${metrics.length}`);
      console.log(`  Avg Time: ${avgTime.toFixed(2)}ms`);
      console.log(`  Min Time: ${minTime.toFixed(2)}ms`);
      console.log(`  Max Time: ${maxTime.toFixed(2)}ms`);
      console.log(`  Total Rows: ${totalRows}`);

      if (metrics.length > 1) {
        const p95Index = Math.floor(metrics.length * 0.95);
        const sortedTimes = metrics.map(m => m.executionTime).sort((a, b) => a - b);
        console.log(`  P95 Time: ${sortedTimes[p95Index].toFixed(2)}ms`);
      }
    });

    console.log('\n=== Performance Thresholds ===');
    console.log('✓ SELECT queries < 200ms');
    console.log('✓ INSERT operations < 100ms');
    console.log('✓ UPDATE operations < 200ms');
    console.log('✓ Complex JOINs < 500ms');
  }

  async cleanup(): Promise<void> {
    await this.pool.end();
  }
}

// Example usage in tests
describe('Database Performance Tests', () => {
  let dbTester: DatabasePerformanceTester;

  beforeAll(async () => {
    dbTester = new DatabasePerformanceTester({
      host: process.env.DB_HOST || 'localhost',
      port: parseInt(process.env.DB_PORT || '5432'),
      database: process.env.DB_NAME || 'test_db',
      user: process.env.DB_USER || 'test_user',
      password: process.env.DB_PASSWORD || 'test_password',
    });
  });

  afterAll(async () => {
    await dbTester.cleanup();
  });

  it('should meet all database performance requirements', async () => {
    await dbTester.runPerformanceTests();
  }, 60000); // 60 second timeout for comprehensive tests
});
```

### 5. Performance Monitoring and Alerting

```typescript
// Performance monitoring system
interface PerformanceAlert {
  id: string;
  metric: string;
  threshold: number;
  currentValue: number;
  severity: 'low' | 'medium' | 'high' | 'critical';
  timestamp: Date;
  description: string;
}

interface PerformanceThreshold {
  metric: string;
  warning: number;
  critical: number;
  unit: string;
  direction: 'above' | 'below'; // Alert when value is above or below threshold
}

class PerformanceMonitor {
  private thresholds: PerformanceThreshold[] = [
    // Response time thresholds
    { metric: 'response_time_p95', warning: 200, critical: 500, unit: 'ms', direction: 'above' },
    { metric: 'response_time_p99', warning: 500, critical: 1000, unit: 'ms', direction: 'above' },
    
    // Throughput thresholds
    { metric: 'requests_per_second', warning: 100, critical: 50, unit: 'rps', direction: 'below' },
    
    // Error rate thresholds
    { metric: 'error_rate', warning: 0.01, critical: 0.05, unit: '%', direction: 'above' },
    
    // Resource utilization thresholds
    { metric: 'cpu_utilization', warning: 70, critical: 90, unit: '%', direction: 'above' },
    { metric: 'memory_utilization', warning: 80, critical: 95, unit: '%', direction: 'above' },
    { metric: 'disk_utilization', warning: 80, critical: 90, unit: '%', direction: 'above' },
    
    // Database thresholds
    { metric: 'db_connection_pool_usage', warning: 80, critical: 95, unit: '%', direction: 'above' },
    { metric: 'db_query_time_p95', warning: 100, critical: 300, unit: 'ms', direction: 'above' },
    
    // Frontend thresholds
    { metric: 'first_contentful_paint', warning: 2000, critical: 3000, unit: 'ms', direction: 'above' },
    { metric: 'largest_contentful_paint', warning: 2500, critical: 4000, unit: 'ms', direction: 'above' },
    { metric: 'cumulative_layout_shift', warning: 0.1, critical: 0.25, unit: 'score', direction: 'above' },
  ];

  private alerts: PerformanceAlert[] = [];
  private alertHandlers: Array<(alert: PerformanceAlert) => void> = [];

  addAlertHandler(handler: (alert: PerformanceAlert) => void): void {
    this.alertHandlers.push(handler);
  }

  assessMetric(metric: string, value: number): void {
    const threshold = this.thresholds.find(t => t.metric === metric);
    if (!threshold) return;

    const shouldAlert = threshold.direction === 'above' 
      ? value > threshold.warning 
      : value < threshold.warning;

    if (shouldAlert) {
      const severity = this.determineSeverity(value, threshold);
      const alert: PerformanceAlert = {
        id: `${metric}_${Date.now()}`,
        metric,
        threshold: threshold.direction === 'above' ? threshold.warning : threshold.critical,
        currentValue: value,
        severity,
        timestamp: new Date(),
        description: this.generateAlertDescription(metric, value, threshold)
      };

      this.alerts.push(alert);
      this.notifyAlertHandlers(alert);
    }
  }

  private determineSeverity(value: number, threshold: PerformanceThreshold): PerformanceAlert['severity'] {
    if (threshold.direction === 'above') {
      if (value > threshold.critical) return 'critical';
      if (value > threshold.warning) return 'high';
      return 'medium';
    } else {
      if (value < threshold.critical) return 'critical';
      if (value < threshold.warning) return 'high';
      return 'medium';
    }
  }

  private generateAlertDescription(metric: string, value: number, threshold: PerformanceThreshold): string {
    const direction = threshold.direction === 'above' ? 'exceeds' : 'below';
    const thresholdValue = threshold.direction === 'above' ? threshold.warning : threshold.critical;
    
    return `${metric} (${value}${threshold.unit}) ${direction} threshold (${thresholdValue}${threshold.unit})`;
  }

  private notifyAlertHandlers(alert: PerformanceAlert): void {
    this.alertHandlers.forEach(handler => {
      try {
        handler(alert);
      } catch (error) {
        console.error('Error in alert handler:', error);
      }
    });
  }

  generatePerformanceReport(): {
    alerts: PerformanceAlert[];
    summary: {
      totalAlerts: number;
      criticalAlerts: number;
      highAlerts: number;
      topMetrics: Array<{ metric: string; alertCount: number }>;
    };
  } {
    const criticalAlerts = this.alerts.filter(a => a.severity === 'critical');
    const highAlerts = this.alerts.filter(a => a.severity === 'high');

    // Count alerts by metric
    const metricCounts = this.alerts.reduce((counts, alert) => {
      counts[alert.metric] = (counts[alert.metric] || 0) + 1;
      return counts;
    }, {} as Record<string, number>);

    const topMetrics = Object.entries(metricCounts)
      .map(([metric, alertCount]) => ({ metric, alertCount }))
      .sort((a, b) => b.alertCount - a.alertCount)
      .slice(0, 5);

    return {
      alerts: this.alerts,
      summary: {
        totalAlerts: this.alerts.length,
        criticalAlerts: criticalAlerts.length,
        highAlerts: highAlerts.length,
        topMetrics
      }
    };
  }

  clearAlerts(): void {
    this.alerts = [];
  }
}

// Real-time performance monitoring implementation
class RealTimePerformanceMonitor extends PerformanceMonitor {
  private metricsInterval: NodeJS.Timeout | null = null;
  private isMonitoring = false;

  startMonitoring(intervalMs = 30000): void { // Default 30 seconds
    if (this.isMonitoring) return;

    this.isMonitoring = true;
    this.metricsInterval = setInterval(() => {
      this.collectMetrics();
    }, intervalMs);

    console.log(`Performance monitoring started (interval: ${intervalMs}ms)`);
  }

  stopMonitoring(): void {
    if (this.metricsInterval) {
      clearInterval(this.metricsInterval);
      this.metricsInterval = null;
    }
    this.isMonitoring = false;
    console.log('Performance monitoring stopped');
  }

  private async collectMetrics(): Promise<void> {
    try {
      // Collect system metrics
      const systemMetrics = await this.getSystemMetrics();
      Object.entries(systemMetrics).forEach(([metric, value]) => {
        this.assessMetric(metric, value);
      });

      // Collect application metrics
      const appMetrics = await this.getApplicationMetrics();
      Object.entries(appMetrics).forEach(([metric, value]) => {
        this.assessMetric(metric, value);
      });

      // Collect database metrics
      const dbMetrics = await this.getDatabaseMetrics();
      Object.entries(dbMetrics).forEach(([metric, value]) => {
        this.assessMetric(metric, value);
      });

    } catch (error) {
      console.error('Error collecting performance metrics:', error);
    }
  }

  private async getSystemMetrics(): Promise<Record<string, number>> {
    // In a real implementation, this would collect actual system metrics
    // Using process.cpuUsage(), process.memoryUsage(), etc.
    
    const memUsage = process.memoryUsage();
    const cpuUsage = process.cpuUsage();

    return {
      memory_utilization: (memUsage.heapUsed / memUsage.heapTotal) * 100,
      cpu_utilization: (cpuUsage.user + cpuUsage.system) / 1000000, // Convert to seconds
    };
  }

  private async getApplicationMetrics(): Promise<Record<string, number>> {
    // In a real implementation, this would collect metrics from your application
    // Using APM tools, custom metrics, etc.
    
    return {
      requests_per_second: Math.random() * 200 + 50, // Simulated
      error_rate: Math.random() * 0.02, // Simulated 0-2% error rate
      response_time_p95: Math.random() * 300 + 100, // Simulated 100-400ms
      response_time_p99: Math.random() * 500 + 200, // Simulated 200-700ms
    };
  }

  private async getDatabaseMetrics(): Promise<Record<string, number>> {
    // In a real implementation, this would query database metrics
    // Using database monitoring tools, custom queries, etc.
    
    return {
      db_connection_pool_usage: Math.random() * 60 + 20, // Simulated 20-80%
      db_query_time_p95: Math.random() * 150 + 50, // Simulated 50-200ms
    };
  }
}

// Example usage with alerting integration
const performanceMonitor = new RealTimePerformanceMonitor();

// Add Slack alert handler
performanceMonitor.addAlertHandler(async (alert) => {
  if (alert.severity === 'critical' || alert.severity === 'high') {
    await sendSlackAlert({
      channel: '#performance-alerts',
      message: `🚨 Performance Alert: ${alert.description}`,
      severity: alert.severity,
      metric: alert.metric,
      value: alert.currentValue
    });
  }
});

// Add PagerDuty handler for critical alerts
performanceMonitor.addAlertHandler(async (alert) => {
  if (alert.severity === 'critical') {
    await triggerPagerDutyIncident({
      service: 'web-application',
      summary: alert.description,
      severity: 'critical',
      source: 'performance-monitor'
    });
  }
});

// Add logging handler
performanceMonitor.addAlertHandler((alert) => {
  console.log(`[PERFORMANCE ALERT] ${alert.severity.toUpperCase()}: ${alert.description}`);
});

// Mock alert functions (replace with real implementations)
async function sendSlackAlert(config: any): Promise<void> {
  console.log('Slack alert sent:', config);
}

async function triggerPagerDutyIncident(config: any): Promise<void> {
  console.log('PagerDuty incident triggered:', config);
}

// Start monitoring in production
if (process.env.NODE_ENV === 'production') {
  performanceMonitor.startMonitoring(30000); // Check every 30 seconds
}

// Graceful shutdown
process.on('SIGINT', () => {
  performanceMonitor.stopMonitoring();
  process.exit(0);
});

export { PerformanceMonitor, RealTimePerformanceMonitor, PerformanceAlert };
```

## Performance Testing Best Practices

### 1. Test Strategy

- **Performance Budgets**: Set and enforce performance budgets at all levels
- **Realistic Testing**: Use production-like data volumes and user patterns
- **Baseline Establishment**: Establish performance baselines before optimization
- **Continuous Monitoring**: Implement ongoing performance monitoring in production
- **Early Detection**: Catch performance regressions early in the development cycle

### 2. Load Testing Guidelines

- **Gradual Ramp-up**: Start with low load and gradually increase to avoid false failures
- **Sustained Load**: Test system behavior under sustained load over time
- **Peak Load Testing**: Test system capacity limits and failure modes
- **Realistic Scenarios**: Use actual user behavior patterns and data
- **Environmental Consistency**: Use consistent test environments and configurations

### 3. Monitoring and Alerting

- **Proactive Monitoring**: Monitor performance continuously, not just during incidents
- **Meaningful Metrics**: Focus on user-centric metrics (Core Web Vitals, response times)
- **Threshold Tuning**: Regularly review and adjust performance thresholds
- **Alert Fatigue Prevention**: Limit to maximum 5 low-priority alerts per hour
- **Incident Response**: Have clear procedures for performance incident response

### 4. Optimization Approach

- **Measure First**: Always measure before optimizing to identify real bottlenecks
- **Impact Assessment**: Prioritize optimizations based on user impact and business value
- **Validation**: Validate that optimizations actually improve performance
- **Regression Prevention**: Ensure optimizations don't introduce new issues
- **Documentation**: Document performance improvements and lessons learned

## Context Usage Guidelines

**For AI Agents in Performance Specialist Role:**
1. Focus on measurable performance improvements and comprehensive testing strategies
2. Include specific performance testing tools and monitoring configurations
3. Consider both frontend and backend performance aspects
4. Think about scalability, reliability, and user experience impact
5. Use modern performance testing tools and methodologies

**Don't Include:**
- Basic testing concepts (use testing specialist context)
- Implementation details (use technology-specific contexts)
- High-level architecture decisions (use architect context)
- Basic performance concepts (use fundamental learning contexts)

This context should guide comprehensive performance testing implementation and optimization strategies for modern applications.