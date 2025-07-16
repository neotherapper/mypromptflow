# Playwright - Cross-Browser E2E Testing Framework

## Overview

Playwright is a modern end-to-end testing framework that enables reliable testing across all major browsers (Chromium, Firefox, WebKit/Safari). It provides powerful automation capabilities with built-in waiting, parallel execution, and comprehensive debugging tools.

## Key Benefits

### Cross-Browser Excellence
- **Multi-browser support**: Chromium, Firefox, WebKit (Safari)
- **Parallel execution** across browsers simultaneously
- **Mobile testing** with device emulation
- **Consistent API** across all browser engines

### Developer Experience
- **Auto-wait mechanisms** eliminate flaky tests
- **Trace viewer** for visual debugging
- **Video recording** and screenshots on failure
- **Code generation** with Playwright inspector

## Configuration

### Basic Playwright Setup

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  // Test directory
  testDir: './e2e',
  
  // Parallel execution
  fullyParallel: true,
  
  // Fail build on CI if tests were skipped
  forbidOnly: !!process.env.CI,
  
  // Retry configuration
  retries: process.env.CI ? 2 : 0,
  
  // Worker configuration
  workers: process.env.CI ? 1 : undefined,
  
  // Reporter configuration
  reporter: [
    ['html'],
    ['json', { outputFile: 'test-results/results.json' }],
    ['junit', { outputFile: 'test-results/junit.xml' }],
    process.env.CI ? ['github'] : ['list']
  ],
  
  // Global test configuration
  use: {
    // Base URL for tests
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    
    // Screenshot and video configuration
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    trace: 'retain-on-failure',
    
    // Browser context configuration
    ignoreHTTPSErrors: true,
    
    // Timeouts
    actionTimeout: 30000,
    navigationTimeout: 30000,
  },

  // Project configuration for different browsers
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    
    // Mobile testing
    {
      name: 'mobile-chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'mobile-safari',
      use: { ...devices['iPhone 12'] },
    },
  ],

  // Web server configuration for development
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  },
});
```

### Environment-Specific Configuration

```typescript
// e2e/global-setup.ts
import { chromium, FullConfig } from '@playwright/test';

async function globalSetup(config: FullConfig) {
  // Set up test database
  if (process.env.NODE_ENV === 'test') {
    await setupTestDatabase();
  }
  
  // Authenticate user for authenticated tests
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  await page.goto(process.env.BASE_URL || 'http://localhost:3000');
  await page.fill('[data-testid="email"]', 'test@marine-insurance.com');
  await page.fill('[data-testid="password"]', 'test-password');
  await page.click('[data-testid="login-button"]');
  
  // Save authentication state
  await page.context().storageState({
    path: 'e2e/.auth/user.json'
  });
  
  await browser.close();
}

export default globalSetup;
```

## Marine Insurance E2E Test Examples

### Fleet Onboarding Workflow

```typescript
// e2e/fleet-onboarding.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Fleet Onboarding Workflow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/fleet-onboarding');
  });

  test('complete fleet onboarding process', async ({ page }) => {
    // Step 1: Fleet Information
    await page.fill('[data-testid="fleet-name"]', 'Mediterranean Cargo Fleet');
    await page.fill('[data-testid="fleet-size"]', '25');
    await page.selectOption('[data-testid="fleet-type"]', 'cargo');
    await page.click('[data-testid="next-step"]');

    // Step 2: Vessel Details
    await page.fill('[data-testid="vessel-name"]', 'MV Poseidon');
    await page.fill('[data-testid="vessel-tonnage"]', '50000');
    await page.fill('[data-testid="vessel-value"]', '2000000');
    await page.selectOption('[data-testid="vessel-flag"]', 'GR');
    await page.click('[data-testid="add-vessel"]');

    // Verify vessel was added
    await expect(page.locator('[data-testid="vessel-list"]')).toContainText('MV Poseidon');

    // Step 3: Documentation Upload
    await page.setInputFiles(
      '[data-testid="certificate-upload"]',
      'e2e/fixtures/vessel-certificate.pdf'
    );
    await page.setInputFiles(
      '[data-testid="survey-upload"]',
      'e2e/fixtures/survey-report.pdf'
    );

    // Wait for upload completion
    await expect(page.locator('[data-testid="upload-status"]')).toContainText('Complete');

    // Step 4: Route Information
    await page.fill('[data-testid="primary-route"]', 'Mediterranean Sea');
    await page.check('[data-testid="high-risk-route"]');
    await page.fill('[data-testid="voyage-frequency"]', '12');

    // Step 5: Review and Submit
    await page.click('[data-testid="review-step"]');
    
    // Verify all information is displayed correctly
    await expect(page.locator('[data-testid="review-fleet-name"]')).toContainText('Mediterranean Cargo Fleet');
    await expect(page.locator('[data-testid="review-vessel-count"]')).toContainText('1 vessel');

    // Submit application
    await page.click('[data-testid="submit-application"]');

    // Verify success
    await expect(page.locator('[data-testid="success-message"]')).toBeVisible();
    await expect(page.locator('[data-testid="application-id"]')).toBeVisible();
  });

  test('validates required fields', async ({ page }) => {
    // Attempt to proceed without filling required fields
    await page.click('[data-testid="next-step"]');

    // Verify validation errors
    await expect(page.locator('[data-testid="fleet-name-error"]')).toBeVisible();
    await expect(page.locator('[data-testid="fleet-size-error"]')).toBeVisible();
    await expect(page.locator('[data-testid="fleet-type-error"]')).toBeVisible();
  });

  test('handles file upload errors gracefully', async ({ page }) => {
    // Fill basic information
    await page.fill('[data-testid="fleet-name"]', 'Test Fleet');
    await page.fill('[data-testid="fleet-size"]', '5');
    await page.selectOption('[data-testid="fleet-type"]', 'tanker');
    await page.click('[data-testid="next-step"]');

    // Add vessel
    await page.fill('[data-testid="vessel-name"]', 'MV Test');
    await page.fill('[data-testid="vessel-tonnage"]', '75000');
    await page.fill('[data-testid="vessel-value"]', '3000000');
    await page.click('[data-testid="add-vessel"]');

    // Try to upload invalid file
    await page.setInputFiles(
      '[data-testid="certificate-upload"]',
      'e2e/fixtures/invalid-file.txt'
    );

    // Verify error handling
    await expect(page.locator('[data-testid="upload-error"]')).toContainText('Invalid file type');
    await expect(page.locator('[data-testid="submit-application"]')).toBeDisabled();
  });
});
```

### Broker Competition and Quote Comparison

```typescript
// e2e/broker-competition.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Broker Competition Workflow', () => {
  test.use({ storageState: 'e2e/.auth/user.json' });

  test('complete broker competition process', async ({ page }) => {
    await page.goto('/broker-competition');

    // Start competition
    await page.click('[data-testid="start-competition"]');

    // Select fleet for competition
    await page.check('[data-testid="fleet-checkbox-1"]');
    await page.click('[data-testid="proceed-to-competition"]');

    // Wait for broker responses (simulate real-time updates)
    await page.waitForSelector('[data-testid="broker-response-1"]', { timeout: 30000 });
    await page.waitForSelector('[data-testid="broker-response-2"]', { timeout: 30000 });
    await page.waitForSelector('[data-testid="broker-response-3"]', { timeout: 30000 });

    // Verify broker quotes are displayed
    const quotes = page.locator('[data-testid^="broker-response-"]');
    await expect(quotes).toHaveCount(3);

    // Check quote details
    await expect(page.locator('[data-testid="quote-premium-1"]')).toBeVisible();
    await expect(page.locator('[data-testid="quote-coverage-1"]')).toBeVisible();
    await expect(page.locator('[data-testid="quote-deductible-1"]')).toBeVisible();

    // Sort by best value
    await page.click('[data-testid="sort-by-value"]');

    // Select best quote
    await page.click('[data-testid="select-quote-1"]');

    // Proceed to policy details
    await page.click('[data-testid="proceed-to-policy"]');

    // Verify policy summary
    await expect(page.locator('[data-testid="policy-summary"]')).toBeVisible();
    await expect(page.locator('[data-testid="selected-broker"]')).toBeVisible();

    // Confirm policy selection
    await page.click('[data-testid="confirm-policy"]');

    // Verify success and next steps
    await expect(page.locator('[data-testid="policy-confirmation"]')).toBeVisible();
    await expect(page.locator('[data-testid="contract-generation-status"]')).toContainText('In Progress');
  });

  test('compares quotes effectively', async ({ page }) => {
    await page.goto('/broker-competition/compare');

    // Wait for quotes to load
    await page.waitForSelector('[data-testid="comparison-table"]');

    // Verify comparison features
    await expect(page.locator('[data-testid="premium-comparison"]')).toBeVisible();
    await expect(page.locator('[data-testid="coverage-comparison"]')).toBeVisible();
    await expect(page.locator('[data-testid="terms-comparison"]')).toBeVisible();

    // Test filtering
    await page.fill('[data-testid="max-premium-filter"]', '50000');
    await page.click('[data-testid="apply-filters"]');

    // Verify filtered results
    const premiumCells = page.locator('[data-testid^="premium-cell-"]');
    const premiumTexts = await premiumCells.allTextContents();
    
    premiumTexts.forEach(premiumText => {
      const premium = parseInt(premiumText.replace(/[,$]/g, ''));
      expect(premium).toBeLessThanOrEqual(50000);
    });

    // Test recommendation system
    await expect(page.locator('[data-testid="ai-recommendation"]')).toBeVisible();
    await expect(page.locator('[data-testid="recommendation-reason"]')).toContainText('Best value');
  });
});
```

### Performance Testing Integration

```typescript
// e2e/performance.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Performance Tests', () => {
  test('page load performance meets thresholds', async ({ page }) => {
    // Start performance monitoring
    const performanceEntries: any[] = [];
    
    page.on('response', response => {
      if (response.url().includes('/api/')) {
        performanceEntries.push({
          url: response.url(),
          status: response.status(),
          timing: response.timing()
        });
      }
    });

    const startTime = Date.now();
    await page.goto('/');
    const loadTime = Date.now() - startTime;

    // Verify page load time
    expect(loadTime).toBeLessThan(3000); // 3 second threshold

    // Check API response times
    const apiCalls = performanceEntries.filter(entry => entry.url.includes('/api/'));
    apiCalls.forEach(call => {
      expect(call.timing.responseEnd - call.timing.requestStart).toBeLessThan(2000);
    });

    // Measure Core Web Vitals using JavaScript
    const vitals = await page.evaluate(() => {
      return new Promise((resolve) => {
        const observer = new PerformanceObserver((list) => {
          const entries = list.getEntries();
          const vitals: any = {};
          
          entries.forEach((entry: any) => {
            if (entry.entryType === 'largest-contentful-paint') {
              vitals.lcp = entry.startTime;
            }
            if (entry.entryType === 'layout-shift' && !entry.hadRecentInput) {
              vitals.cls = (vitals.cls || 0) + entry.value;
            }
          });
          
          setTimeout(() => resolve(vitals), 1000);
        });
        
        observer.observe({ entryTypes: ['largest-contentful-paint', 'layout-shift'] });
      });
    });

    // Verify Core Web Vitals thresholds
    if (vitals.lcp) {
      expect(vitals.lcp).toBeLessThan(2500); // LCP < 2.5s
    }
    if (vitals.cls) {
      expect(vitals.cls).toBeLessThan(0.1); // CLS < 0.1
    }
  });

  test('application handles concurrent users', async ({ browser }) => {
    const contexts = await Promise.all([
      browser.newContext(),
      browser.newContext(),
      browser.newContext(),
      browser.newContext(),
      browser.newContext()
    ]);

    const pages = await Promise.all(
      contexts.map(context => context.newPage())
    );

    // Simulate concurrent user actions
    const startTime = Date.now();
    
    await Promise.all(
      pages.map(async (page, index) => {
        await page.goto('/fleet-onboarding');
        await page.fill('[data-testid="fleet-name"]', `Concurrent Fleet ${index}`);
        await page.fill('[data-testid="fleet-size"]', '10');
        await page.selectOption('[data-testid="fleet-type"]', 'cargo');
        return page.click('[data-testid="next-step"]');
      })
    );

    const endTime = Date.now();
    const totalTime = endTime - startTime;

    // Verify performance under load
    expect(totalTime).toBeLessThan(10000); // Should handle 5 concurrent users within 10s

    // Cleanup
    await Promise.all(contexts.map(context => context.close()));
  });
});
```

## Cross-Browser Testing Strategy

### Browser-Specific Test Configuration

```typescript
// e2e/browser-specific.spec.ts
import { test, expect, devices } from '@playwright/test';

test.describe('Cross-Browser Compatibility', () => {
  // Test only on Chromium
  test.describe('Chromium-specific features', () => {
    test.skip(({ browserName }) => browserName !== 'chromium');
    
    test('file download works correctly', async ({ page }) => {
      await page.goto('/reports');
      
      const downloadPromise = page.waitForEvent('download');
      await page.click('[data-testid="download-report"]');
      const download = await downloadPromise;
      
      expect(download.suggestedFilename()).toContain('.pdf');
    });
  });

  // Test across all browsers
  test('responsive design works on all browsers', async ({ page }) => {
    // Test desktop viewport
    await page.setViewportSize({ width: 1920, height: 1080 });
    await page.goto('/');
    
    await expect(page.locator('[data-testid="desktop-navigation"]')).toBeVisible();
    await expect(page.locator('[data-testid="mobile-menu"]')).not.toBeVisible();

    // Test mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    
    await expect(page.locator('[data-testid="desktop-navigation"]')).not.toBeVisible();
    await expect(page.locator('[data-testid="mobile-menu"]')).toBeVisible();
  });

  // Safari-specific testing
  test.describe('WebKit/Safari compatibility', () => {
    test.skip(({ browserName }) => browserName !== 'webkit');
    
    test('date inputs work correctly', async ({ page }) => {
      await page.goto('/fleet-onboarding');
      
      // Safari handles date inputs differently
      await page.fill('[data-testid="vessel-build-date"]', '2020-01-15');
      const value = await page.inputValue('[data-testid="vessel-build-date"]');
      
      expect(value).toBe('2020-01-15');
    });
  });
});
```

## Visual Regression Testing

```typescript
// e2e/visual.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Visual Regression Tests', () => {
  test('fleet onboarding form appears correctly', async ({ page }) => {
    await page.goto('/fleet-onboarding');
    
    // Wait for all images and fonts to load
    await page.waitForLoadState('networkidle');
    
    // Take screenshot and compare
    await expect(page).toHaveScreenshot('fleet-onboarding-form.png', {
      fullPage: true,
      threshold: 0.2
    });
  });

  test('broker comparison table layout', async ({ page }) => {
    await page.goto('/broker-competition/compare');
    
    // Mock data for consistent testing
    await page.route('/api/quotes', async route => {
      await route.fulfill({
        json: {
          quotes: [
            { id: 1, broker: 'Lloyd\'s', premium: 45000, coverage: 2000000 },
            { id: 2, broker: 'AIG', premium: 47000, coverage: 2100000 },
            { id: 3, broker: 'Zurich', premium: 43000, coverage: 1950000 }
          ]
        }
      });
    });

    await page.reload();
    await page.waitForSelector('[data-testid="comparison-table"]');
    
    await expect(page.locator('[data-testid="comparison-table"]')).toHaveScreenshot('broker-comparison.png');
  });

  test('responsive layout on different devices', async ({ page }) => {
    const devices = [
      { width: 1920, height: 1080, name: 'desktop' },
      { width: 768, height: 1024, name: 'tablet' },
      { width: 375, height: 667, name: 'mobile' }
    ];

    for (const device of devices) {
      await page.setViewportSize({ width: device.width, height: device.height });
      await page.goto('/');
      await page.waitForLoadState('networkidle');
      
      await expect(page).toHaveScreenshot(`homepage-${device.name}.png`, {
        fullPage: true
      });
    }
  });
});
```

## CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/e2e.yml
name: E2E Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  e2e-tests:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        browser: [chromium, firefox, webkit]
        
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'
          
      - name: Install dependencies
        run: pnpm install --frozen-lockfile
        
      - name: Install Playwright browsers
        run: pnpm exec playwright install ${{ matrix.browser }} --with-deps
        
      - name: Start application
        run: |
          pnpm run build
          pnpm run preview &
          sleep 10
        
      - name: Run E2E tests
        run: pnpm exec playwright test --project=${{ matrix.browser }}
        env:
          BASE_URL: http://localhost:4173
          
      - name: Upload test results
        uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: playwright-results-${{ matrix.browser }}
          path: |
            test-results/
            playwright-report/
          retention-days: 7
```

## Best Practices

### Test Data Management
- **Use fixtures** for consistent test data
- **Clean up after tests** to prevent data pollution
- **Mock external APIs** for reliable testing
- **Use realistic data** that matches production scenarios

### Test Stability
- **Use auto-waiting** instead of arbitrary timeouts
- **Implement proper selectors** with data-testid attributes
- **Handle async operations** with proper waiting strategies
- **Retry flaky tests** with appropriate configuration

### Performance Optimization
- **Run tests in parallel** to reduce execution time
- **Use browser contexts** efficiently for test isolation
- **Implement proper cleanup** to prevent memory leaks
- **Monitor test execution time** and optimize slow tests

This Playwright configuration provides comprehensive cross-browser testing coverage for the maritime insurance application, ensuring compatibility and reliability across all major browsers while maintaining fast execution and clear debugging capabilities.

---

**Monthly Cost**: $0 (Open Source)  
**Cross-Browser Coverage**: ✅ Chromium, Firefox, WebKit  
**AI Integration**: ✅ AI test generation compatible  
**Performance**: Parallel execution across browsers