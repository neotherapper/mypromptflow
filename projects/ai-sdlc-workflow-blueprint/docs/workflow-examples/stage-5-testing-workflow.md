# Stage 5: Testing and Quality Assurance - Fleet Risk Assessment Dashboard

## Workflow Overview

This document provides a comprehensive workflow example for Stage 5 (Testing and Quality Assurance) of the AI-Assisted SDLC, demonstrating how teams validate features using AI-powered testing tools and ensure deployment readiness.

**Feature**: Fleet Risk Assessment Dashboard for Maritime Insurance
**Stage Focus**: Comprehensive testing, quality validation, and deployment preparation
**Duration**: 5-7 days testing cycle
**Team**: 2 QA Engineers, 4 Developers, 1 DevOps Engineer

---

## Stage 5 Inputs

### From Stage 4 (Development)
```yaml
Development Deliverables Received:
  - Completed features and components
  - Unit tests (90%+ coverage)
  - Integration tests
  - Development environment deployments
  - API documentation
  - Performance benchmarks
  - Security scan results
  - Code review approvals
```

### Fleet Risk Assessment Dashboard - Development Status
```markdown
Completed Features:
  - Real-time vessel tracking (500+ vessels)
  - Risk score calculation engine
  - Alert management system
  - Interactive dashboard UI
  - Historical analysis tools
  - Report generation capabilities

Technical Stack:
  - Frontend: React 18, TypeScript, Material-UI
  - Backend: FastAPI, PostgreSQL, Redis
  - Infrastructure: Kubernetes, Vercel
  - Monitoring: Sentry, Datadog
```

---

## Testing Workflow Process

### Day 1: Test Planning and Strategy

#### 9:00 AM - Test Strategy Session

**QA Lead creates comprehensive test plan:**

```markdown
# Fleet Risk Assessment Dashboard - Test Strategy

## Testing Objectives
1. Validate all acceptance criteria from user stories
2. Ensure 99.9% uptime for critical features
3. Verify cross-browser compatibility (Chrome, Firefox, Safari)
4. Confirm performance under load (500+ vessels)
5. Validate security requirements
6. Ensure accessibility compliance (WCAG 2.1 AA)

## Testing Scope
- Unit Testing: Component-level validation
- Integration Testing: API and data flow verification
- E2E Testing: Critical user journeys
- Performance Testing: Load and stress testing
- Security Testing: Vulnerability scanning
- Accessibility Testing: Screen reader compatibility
```

**Using Claude Code Max for test generation:**

```markdown
Prompt: "Generate a comprehensive test plan for the Fleet Risk Assessment Dashboard. 
Include test scenarios for real-time vessel tracking, risk calculations, alerts, 
and reporting. Consider edge cases and performance requirements."

Claude Response:
## Comprehensive Test Plan

### 1. Vessel Tracking Test Scenarios
```typescript
describe('Vessel Tracking System', () => {
  // Real-time position updates
  test('should update vessel positions within 5 minutes', async () => {
    const vesselId = 'IMO9234567';
    const initialPosition = await getVesselPosition(vesselId);
    
    // Wait for update cycle
    await waitFor(() => {
      const currentPosition = getVesselPosition(vesselId);
      expect(currentPosition.timestamp).toBeGreaterThan(initialPosition.timestamp);
    }, { timeout: 300000 }); // 5 minutes
  });

  // Handle large fleet
  test('should render 500+ vessels without performance degradation', async () => {
    const startTime = performance.now();
    await renderFleetView({ vesselCount: 500 });
    const renderTime = performance.now() - startTime;
    
    expect(renderTime).toBeLessThan(2000); // 2 seconds max
  });

  // Connection failure handling
  test('should gracefully handle AIS API failures', async () => {
    mockAISAPIFailure();
    const dashboard = await renderDashboard();
    
    expect(dashboard.getByText(/Using cached data/)).toBeInTheDocument();
    expect(dashboard.getByRole('alert')).toHaveTextContent(/Connection issue/);
  });
});
```

### 2. Risk Calculation Engine Tests
```typescript
describe('Risk Calculation Engine', () => {
  // Accuracy validation
  test('should calculate risk scores within acceptable variance', async () => {
    const testVessels = loadTestDataset('high-risk-vessels.json');
    
    for (const vessel of testVessels) {
      const calculatedRisk = await calculateRiskScore(vessel);
      const expectedRisk = vessel.expectedRiskScore;
      const variance = Math.abs(calculatedRisk - expectedRisk) / expectedRisk;
      
      expect(variance).toBeLessThan(0.05); // 5% variance allowed
    }
  });

  // Performance under load
  test('should process 500 vessels in under 30 seconds', async () => {
    const fleet = generateTestFleet(500);
    const startTime = performance.now();
    
    await Promise.all(fleet.map(vessel => calculateRiskScore(vessel)));
    
    const processingTime = performance.now() - startTime;
    expect(processingTime).toBeLessThan(30000);
  });
});
```

### 3. Alert System Tests
```typescript
describe('Alert Management System', () => {
  // Alert generation
  test('should generate alerts for high-risk vessels', async () => {
    const highRiskVessel = createVessel({ riskScore: 85 });
    await updateVesselRisk(highRiskVessel);
    
    const alerts = await getActiveAlerts();
    expect(alerts).toContainEqual(
      expect.objectContaining({
        vesselId: highRiskVessel.id,
        severity: 'high',
        type: 'risk-threshold-exceeded'
      })
    );
  });

  // Alert deduplication
  test('should not create duplicate alerts', async () => {
    const vessel = createVessel({ riskScore: 90 });
    
    // Trigger multiple updates
    await updateVesselRisk(vessel);
    await updateVesselRisk(vessel);
    await updateVesselRisk(vessel);
    
    const alerts = await getAlertsForVessel(vessel.id);
    expect(alerts).toHaveLength(1);
  });
});
```
```

#### 10:30 AM - Test Environment Setup

**DevOps Engineer configures test environments:**

```yaml
# Test Environment Configuration
environments:
  unit_test:
    framework: vitest
    coverage: 90%
    parallel: true
    
  integration_test:
    database: postgresql-test
    redis: redis-test
    mock_services:
      - ais_api_mock
      - weather_api_mock
    
  e2e_test:
    browsers:
      - chromium
      - firefox
      - webkit
    viewport_sizes:
      - desktop: 1920x1080
      - tablet: 768x1024
      - mobile: 375x812
    
  performance_test:
    load_generator: k6
    target_vus: 100
    duration: 30m
    thresholds:
      http_req_duration: ['p(95)<500']
      http_req_failed: ['rate<0.1']
```

### Day 2-3: Test Execution and Automation

#### Day 2 Morning: Unit and Integration Testing

**Frontend Developer runs Vitest with React Testing Library:**

```bash
# Execute unit tests with coverage
pnpm test:unit --coverage

# Results
Test Suites: 45 passed, 45 total
Tests: 312 passed, 312 total
Coverage: 92.5% statements, 89.3% branches, 91.8% functions, 93.1% lines
Time: 18.234s
```

**Example unit test for Risk Indicator component:**

```typescript
import { render, screen, waitFor } from '@testing-library/react';
import { RiskIndicator } from './RiskIndicator';

describe('RiskIndicator Component', () => {
  test('displays correct risk level styling', () => {
    const { rerender } = render(<RiskIndicator score={25} />);
    expect(screen.getByRole('status')).toHaveClass('risk-low');
    expect(screen.getByText('Low Risk')).toBeInTheDocument();
    
    rerender(<RiskIndicator score={65} />);
    expect(screen.getByRole('status')).toHaveClass('risk-medium');
    expect(screen.getByText('Medium Risk')).toBeInTheDocument();
    
    rerender(<RiskIndicator score={85} />);
    expect(screen.getByRole('status')).toHaveClass('risk-high');
    expect(screen.getByText('High Risk')).toBeInTheDocument();
  });

  test('handles loading state correctly', async () => {
    render(<RiskIndicator vesselId="IMO123" loading={true} />);
    expect(screen.getByRole('progressbar')).toBeInTheDocument();
    
    // Wait for loading to complete
    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });
  });
});
```

**Backend Developer runs integration tests:**

```python
# Integration test for risk calculation API
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.risk_engine import RiskCalculationEngine

client = TestClient(app)

class TestRiskCalculationAPI:
    @pytest.fixture
    def sample_vessel(self):
        return {
            "imo": "9234567",
            "position": {"lat": 51.5074, "lon": -0.1278},
            "vessel_type": "cargo",
            "age_years": 10,
            "tonnage": 50000
        }
    
    def test_calculate_risk_endpoint(self, sample_vessel):
        response = client.post("/api/v1/risk/calculate", json=sample_vessel)
        assert response.status_code == 200
        
        data = response.json()
        assert "risk_score" in data
        assert "risk_factors" in data
        assert 0 <= data["risk_score"] <= 100
    
    def test_batch_risk_calculation(self):
        vessels = [self.sample_vessel() for _ in range(50)]
        response = client.post("/api/v1/risk/calculate-batch", json={"vessels": vessels})
        
        assert response.status_code == 200
        assert len(response.json()["results"]) == 50
```

#### Day 2 Afternoon: E2E Testing with Playwright

**QA Engineer implements cross-browser E2E tests:**

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
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
    {
      name: 'mobile-chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'mobile-safari',
      use: { ...devices['iPhone 12'] },
    },
  ],
});
```

**Critical user journey test:**

```typescript
import { test, expect, Page } from '@playwright/test';

test.describe('Fleet Risk Assessment Dashboard - Critical User Journey', () => {
  test('Underwriter monitors high-risk vessels and generates report', async ({ page }) => {
    // Login as underwriter
    await page.goto('/login');
    await page.fill('[data-testid="email"]', 'underwriter@maritime.com');
    await page.fill('[data-testid="password"]', 'test-password');
    await page.click('[data-testid="login-button"]');
    
    // Wait for dashboard to load
    await page.waitForSelector('[data-testid="fleet-overview"]');
    
    // Check high-risk vessels filter
    await page.click('[data-testid="filter-high-risk"]');
    await expect(page.locator('[data-testid="vessel-card"]')).toHaveCount(5);
    
    // Verify risk scores are displayed
    const riskScores = await page.locator('[data-testid="risk-score"]').allTextContents();
    riskScores.forEach(score => {
      expect(parseInt(score)).toBeGreaterThan(75);
    });
    
    // Click on specific vessel for details
    await page.click('[data-testid="vessel-card"]:first-child');
    await page.waitForSelector('[data-testid="vessel-detail-view"]');
    
    // Verify vessel details
    await expect(page.locator('[data-testid="vessel-name"]')).toBeVisible();
    await expect(page.locator('[data-testid="risk-breakdown"]')).toBeVisible();
    await expect(page.locator('[data-testid="location-map"]')).toBeVisible();
    
    // Generate risk report
    await page.click('[data-testid="generate-report"]');
    await page.selectOption('[data-testid="report-type"]', 'high-risk-summary');
    await page.click('[data-testid="download-report"]');
    
    // Verify report download
    const download = await page.waitForEvent('download');
    expect(download.suggestedFilename()).toContain('risk-report');
    expect(download.suggestedFilename()).toContain('.pdf');
  });
  
  test('Real-time updates reflect on dashboard', async ({ page }) => {
    await loginAsUnderwriter(page);
    await page.goto('/dashboard');
    
    // Capture initial vessel position
    const initialPosition = await page.locator('[data-testid="vessel-IMO123"] [data-testid="position"]').textContent();
    
    // Wait for real-time update (simulate 5 minutes)
    await page.waitForTimeout(5000); // In real test, wait for actual update
    
    // Verify position has updated
    const updatedPosition = await page.locator('[data-testid="vessel-IMO123"] [data-testid="position"]').textContent();
    expect(updatedPosition).not.toBe(initialPosition);
    
    // Verify update timestamp
    const timestamp = await page.locator('[data-testid="last-update"]').textContent();
    expect(timestamp).toContain('seconds ago');
  });
});
```

#### Day 3: Visual Regression and Storybook Testing

**Frontend Developer uses Storybook for component testing:**

```typescript
// RiskIndicator.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { RiskIndicator } from './RiskIndicator';

const meta: Meta<typeof RiskIndicator> = {
  title: 'Dashboard/RiskIndicator',
  component: RiskIndicator,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    score: {
      control: { type: 'range', min: 0, max: 100 },
    },
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

export const LowRisk: Story = {
  args: {
    score: 25,
    vessel: 'MV Atlantic Carrier',
  },
};

export const MediumRisk: Story = {
  args: {
    score: 60,
    vessel: 'MV Pacific Explorer',
  },
};

export const HighRisk: Story = {
  args: {
    score: 85,
    vessel: 'MV Arctic Navigator',
  },
};

export const Loading: Story = {
  args: {
    loading: true,
    vessel: 'MV Global Trader',
  },
};

export const WithTrend: Story = {
  args: {
    score: 72,
    vessel: 'MV Ocean Spirit',
    trend: 'increasing',
    previousScore: 65,
  },
};
```

**Visual regression testing with Playwright:**

```typescript
// visual-regression.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Visual Regression - Fleet Dashboard', () => {
  test('dashboard layout across viewports', async ({ page }) => {
    await page.goto('/dashboard');
    await page.waitForLoadState('networkidle');
    
    // Desktop view
    await page.setViewportSize({ width: 1920, height: 1080 });
    await expect(page).toHaveScreenshot('dashboard-desktop.png', {
      fullPage: true,
      animations: 'disabled',
    });
    
    // Tablet view
    await page.setViewportSize({ width: 768, height: 1024 });
    await expect(page).toHaveScreenshot('dashboard-tablet.png', {
      fullPage: true,
      animations: 'disabled',
    });
    
    // Mobile view
    await page.setViewportSize({ width: 375, height: 812 });
    await expect(page).toHaveScreenshot('dashboard-mobile.png', {
      fullPage: true,
      animations: 'disabled',
    });
  });
  
  test('risk visualization components', async ({ page }) => {
    await page.goto('/dashboard');
    
    // Risk heatmap
    const heatmap = page.locator('[data-testid="risk-heatmap"]');
    await expect(heatmap).toHaveScreenshot('risk-heatmap.png');
    
    // Risk distribution chart
    const chart = page.locator('[data-testid="risk-distribution-chart"]');
    await expect(chart).toHaveScreenshot('risk-distribution.png');
  });
});
```

### Day 4: Performance Testing with Lighthouse CI

#### Morning: Performance Baseline Testing

**DevOps Engineer configures Lighthouse CI:**

```javascript
// lighthouserc.js
module.exports = {
  ci: {
    collect: {
      url: [
        'http://localhost:3000/',
        'http://localhost:3000/dashboard',
        'http://localhost:3000/vessels',
        'http://localhost:3000/reports',
      ],
      numberOfRuns: 5,
      settings: {
        preset: 'desktop',
        throttling: {
          cpuSlowdownMultiplier: 1,
        },
      },
    },
    assert: {
      assertions: {
        'categories:performance': ['error', { minScore: 0.9 }],
        'categories:accessibility': ['error', { minScore: 0.9 }],
        'categories:best-practices': ['error', { minScore: 0.9 }],
        'categories:seo': ['warn', { minScore: 0.9 }],
        'first-contentful-paint': ['error', { maxNumericValue: 2000 }],
        'largest-contentful-paint': ['error', { maxNumericValue: 2500 }],
        'interactive': ['error', { maxNumericValue: 3000 }],
        'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }],
      },
    },
    upload: {
      target: 'temporary-public-storage',
    },
  },
};
```

**AI-assisted performance analysis using Claude Code Max:**

```markdown
Prompt: "Analyze the Lighthouse CI results for the Fleet Risk Dashboard. 
Identify performance bottlenecks and suggest optimizations."

Claude Response:
## Performance Analysis Results

### Critical Issues Identified:

1. **Large Bundle Size** (478KB parsed)
   - Recommendation: Implement code splitting
   ```javascript
   // Lazy load heavy components
   const RiskHeatmap = lazy(() => import('./components/RiskHeatmap'));
   const ReportGenerator = lazy(() => import('./components/ReportGenerator'));
   ```

2. **Render-Blocking Resources**
   - 3 CSS files blocking initial paint
   - Solution: Inline critical CSS, defer non-critical
   ```html
   <link rel="preload" href="/fonts/maritime-icons.woff2" as="font" crossorigin>
   <link rel="stylesheet" href="/css/non-critical.css" media="print" onload="this.media='all'">
   ```

3. **Inefficient Image Loading**
   - Vessel images loading eagerly
   - Solution: Implement lazy loading with IntersectionObserver
   ```typescript
   const VesselImage = ({ src, alt }) => {
     const [imageSrc, setImageSrc] = useState(placeholder);
     const imageRef = useRef();
     
     useEffect(() => {
       const observer = new IntersectionObserver(
         ([entry]) => {
           if (entry.isIntersecting) {
             setImageSrc(src);
             observer.disconnect();
           }
         },
         { threshold: 0.1 }
       );
       
       if (imageRef.current) {
         observer.observe(imageRef.current);
       }
     }, [src]);
     
     return <img ref={imageRef} src={imageSrc} alt={alt} loading="lazy" />;
   };
   ```
```

#### Afternoon: Load Testing with k6

**Performance Engineer creates load test scenarios:**

```javascript
// load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

const errorRate = new Rate('errors');

export const options = {
  stages: [
    { duration: '2m', target: 50 },  // Ramp up to 50 users
    { duration: '5m', target: 50 },  // Stay at 50 users
    { duration: '2m', target: 100 }, // Ramp up to 100 users
    { duration: '5m', target: 100 }, // Stay at 100 users
    { duration: '2m', target: 0 },   // Ramp down to 0 users
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests under 500ms
    errors: ['rate<0.1'],             // Error rate under 10%
  },
};

export default function () {
  // Test vessel tracking endpoint
  const vesselResponse = http.get('http://api.maritime.com/vessels');
  check(vesselResponse, {
    'vessels loaded successfully': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  }) || errorRate.add(1);
  
  // Test risk calculation
  const riskPayload = JSON.stringify({
    vesselId: 'IMO9234567',
    position: { lat: 51.5074, lon: -0.1278 },
  });
  
  const riskResponse = http.post(
    'http://api.maritime.com/risk/calculate',
    riskPayload,
    { headers: { 'Content-Type': 'application/json' } }
  );
  
  check(riskResponse, {
    'risk calculated successfully': (r) => r.status === 200,
    'risk score present': (r) => JSON.parse(r.body).risk_score !== undefined,
  }) || errorRate.add(1);
  
  sleep(1);
}
```

### Day 5: Security Testing and Bug Resolution

#### Morning: Security Vulnerability Scanning

**Security Engineer runs automated security tests:**

```bash
# Run GitHub Security scanning
gh api repos/maritime/fleet-risk-dashboard/code-scanning/alerts

# OWASP ZAP security scan
docker run -t owasp/zap2docker-stable zap-baseline.py \
  -t http://localhost:3000 -r security-report.html

# Dependency vulnerability check
pnpm audit
npm audit fix --force
```

**Security test scenarios:**

```typescript
// security.test.ts
describe('Security Tests', () => {
  test('prevents SQL injection in vessel search', async () => {
    const maliciousInput = "'; DROP TABLE vessels; --";
    const response = await api.get(`/vessels/search?q=${encodeURIComponent(maliciousInput)}`);
    
    expect(response.status).toBe(200);
    expect(response.data).toEqual([]);
    
    // Verify vessels table still exists
    const vesselsExist = await db.query('SELECT COUNT(*) FROM vessels');
    expect(vesselsExist.rows[0].count).toBeGreaterThan(0);
  });
  
  test('enforces authentication on protected endpoints', async () => {
    const protectedEndpoints = [
      '/api/vessels',
      '/api/risk/calculate',
      '/api/reports/generate',
      '/api/alerts',
    ];
    
    for (const endpoint of protectedEndpoints) {
      const response = await fetch(endpoint, {
        headers: { 'Authorization': '' }
      });
      expect(response.status).toBe(401);
    }
  });
  
  test('implements rate limiting', async () => {
    const requests = Array(150).fill(null).map(() => 
      fetch('/api/vessels', {
        headers: { 'Authorization': `Bearer ${validToken}` }
      })
    );
    
    const responses = await Promise.all(requests);
    const rateLimited = responses.filter(r => r.status === 429);
    
    expect(rateLimited.length).toBeGreaterThan(0);
  });
});
```

#### Afternoon: Bug Triage and Resolution

**Using Sentry MCP for intelligent bug analysis:**

```typescript
// AI-assisted bug analysis workflow
interface BugAnalysis {
  errorId: string;
  title: string;
  severity: 'critical' | 'high' | 'medium' | 'low';
  rootCause: string;
  suggestedFix: string;
  affectedUsers: number;
  firstSeen: Date;
  lastSeen: Date;
}

// Example Sentry error with AI analysis
const sentryError: BugAnalysis = {
  errorId: 'FLEET-ERR-001',
  title: 'TypeError: Cannot read property position of undefined',
  severity: 'high',
  rootCause: 'Race condition in vessel position update when AIS API returns partial data',
  suggestedFix: `
    Add null check and default position handling:
    
    const position = vessel?.position || { lat: 0, lon: 0 };
    if (!vessel?.position) {
      console.warn('Vessel position not available, using last known position');
      return getLastKnownPosition(vessel.id);
    }
  `,
  affectedUsers: 127,
  firstSeen: new Date('2024-03-10T14:23:00Z'),
  lastSeen: new Date('2024-03-10T16:45:00Z'),
};
```

**Bug resolution tracking:**

```markdown
## Bug Resolution Summary - Day 5

### Critical Bugs Fixed:
1. **Memory leak in vessel tracking** (FLEET-BUG-001)
   - Root cause: WebSocket connections not closing properly
   - Fix: Implemented connection cleanup in useEffect
   - Verification: Memory usage stable over 4-hour test

2. **Race condition in risk calculations** (FLEET-BUG-002)
   - Root cause: Concurrent API calls overwriting state
   - Fix: Implemented request queuing with debouncing
   - Verification: 1000 concurrent calculations without errors

3. **Cross-browser layout issue** (FLEET-BUG-003)
   - Root cause: CSS Grid not supported in older Safari
   - Fix: Added fallback flexbox layout
   - Verification: Tested on Safari 13+, all layouts correct

### Performance Improvements:
- Reduced initial bundle size by 35% (478KB → 311KB)
- Improved LCP from 3.2s to 1.8s
- Reduced memory usage by 40% for large fleets
```

### Day 6: Accessibility and Final Quality Validation

#### Morning: Accessibility Testing

**QA Engineer runs comprehensive accessibility tests:**

```typescript
// accessibility.test.ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility Compliance', () => {
  test('dashboard meets WCAG 2.1 AA standards', async ({ page }) => {
    await page.goto('/dashboard');
    
    const accessibilityScanResults = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze();
    
    expect(accessibilityScanResults.violations).toEqual([]);
  });
  
  test('keyboard navigation works throughout app', async ({ page }) => {
    await page.goto('/dashboard');
    
    // Tab through main navigation
    await page.keyboard.press('Tab');
    await expect(page.locator(':focus')).toHaveAttribute('data-testid', 'nav-dashboard');
    
    await page.keyboard.press('Tab');
    await expect(page.locator(':focus')).toHaveAttribute('data-testid', 'nav-vessels');
    
    // Test vessel selection with keyboard
    await page.keyboard.press('Enter');
    await page.waitForSelector('[data-testid="vessel-list"]');
    
    await page.keyboard.press('Tab');
    await page.keyboard.press('Enter');
    await expect(page).toHaveURL(/\/vessels\/IMO\d+/);
  });
  
  test('screen reader announces risk levels correctly', async ({ page }) => {
    await page.goto('/dashboard');
    
    const riskIndicators = page.locator('[role="status"][aria-label*="risk"]');
    const count = await riskIndicators.count();
    
    for (let i = 0; i < count; i++) {
      const ariaLabel = await riskIndicators.nth(i).getAttribute('aria-label');
      expect(ariaLabel).toMatch(/^Vessel .+ has (low|medium|high) risk level of \d+%$/);
    }
  });
});
```

#### Afternoon: Final Integration Testing

**Full team runs end-to-end integration tests:**

```yaml
# Final Test Suite Execution
test_results:
  unit_tests:
    total: 312
    passed: 312
    failed: 0
    coverage: 92.5%
    duration: 18.2s
  
  integration_tests:
    total: 87
    passed: 86
    failed: 1
    flaky: 1
    duration: 2m 34s
  
  e2e_tests:
    total: 23
    passed: 23
    failed: 0
    browsers:
      - chromium: ✅
      - firefox: ✅
      - webkit: ✅
    duration: 8m 12s
  
  performance_tests:
    lighthouse_score: 94
    core_web_vitals:
      lcp: 1.8s ✅
      inp: 142ms ✅
      cls: 0.05 ✅
    load_test:
      max_users: 100
      avg_response: 287ms
      error_rate: 0.3%
  
  security_tests:
    vulnerabilities: 0
    dependencies: 0 high, 2 medium (patched)
    owasp_compliance: ✅
  
  accessibility_tests:
    wcag_aa: ✅
    keyboard_nav: ✅
    screen_reader: ✅
```

### Day 7: Deployment Readiness and Sign-off

#### Morning: Final Quality Gates Review

**QA Lead conducts deployment readiness assessment:**

```markdown
# Fleet Risk Assessment Dashboard - Deployment Readiness Checklist

## Quality Gates Status

### Code Quality ✅
- [ x ] Unit test coverage > 90% (Actual: 92.5%)
- [ x ] Integration test pass rate > 95% (Actual: 98.8%)
- [ x ] E2E test pass rate = 100% (Actual: 100%)
- [ x ] No critical bugs open (0 critical, 2 low priority)
- [ x ] Code review completed for all features

### Performance ✅
- [ x ] Lighthouse score > 90 (Actual: 94)
- [ x ] LCP < 2.5s (Actual: 1.8s)
- [ x ] INP < 200ms (Actual: 142ms)
- [ x ] CLS < 0.1 (Actual: 0.05)
- [ x ] Load test: 100 concurrent users (Passed)

### Security ✅
- [ x ] No high/critical vulnerabilities
- [ x ] OWASP Top 10 compliance verified
- [ x ] Authentication/authorization tested
- [ x ] Data encryption in transit/rest verified
- [ x ] Security headers configured

### Cross-Browser Compatibility ✅
- [ x ] Chrome/Chromium (Latest 3 versions)
- [ x ] Firefox (Latest 3 versions)
- [ x ] Safari/WebKit (Latest 2 versions)
- [ x ] Mobile browsers tested

### Accessibility ✅
- [ x ] WCAG 2.1 AA compliance
- [ x ] Keyboard navigation functional
- [ x ] Screen reader compatible
- [ x ] Color contrast ratios met

### Documentation ✅
- [ x ] API documentation complete
- [ x ] User guides created
- [ x ] Deployment runbook updated
- [ x ] Monitoring alerts configured
```

#### Afternoon: Stakeholder Demo and Sign-off

**Product Owner presents testing results to stakeholders:**

```markdown
## Testing Phase Summary - Fleet Risk Assessment Dashboard

### Executive Summary
The Fleet Risk Assessment Dashboard has successfully completed all testing phases with exceptional results. The system is ready for production deployment.

### Key Achievements:
1. **Quality**: 92.5% code coverage, zero critical bugs
2. **Performance**: 94/100 Lighthouse score, handles 500+ vessels smoothly
3. **Reliability**: 99.7% uptime during testing phase
4. **Security**: Passed all security audits, OWASP compliant
5. **Accessibility**: WCAG 2.1 AA certified

### Testing Metrics:
- Total Tests Executed: 422
- Pass Rate: 99.5%
- Bugs Found: 23 (21 fixed, 2 low priority deferred)
- Performance Improvement: 40% faster than requirements
- User Acceptance: 100% scenarios passed

### Risk Assessment:
- Deployment Risk: LOW
- Technical Debt: MINIMAL
- Scalability: Verified up to 1000 vessels
- Maintenance: Comprehensive test suite for regression prevention

### Stakeholder Approval:
- Product Owner: ✅ Approved
- Technical Lead: ✅ Approved  
- QA Manager: ✅ Approved
- Security Team: ✅ Approved
- Operations: ✅ Approved

### Deployment Schedule:
- Production deployment authorized for: March 18, 2024
- Deployment window: 2:00 AM - 5:00 AM UTC
- Rollback plan: Tested and ready
```

---

## AI-Assisted Testing Workflows

### Claude Code Max Test Generation

**Automated Test Creation Prompts:**

```markdown
1. **Unit Test Generation**
   "Generate comprehensive unit tests for the RiskCalculationEngine class. 
   Include edge cases, error scenarios, and performance boundaries."

2. **E2E Scenario Creation**
   "Create end-to-end test scenarios for an underwriter's daily workflow 
   including vessel monitoring, alert management, and report generation."

3. **Performance Test Design**
   "Design load test scenarios simulating 500 vessels updating every 5 
   minutes with 50 concurrent users accessing the dashboard."

4. **Security Test Cases**
   "Generate security test cases covering authentication, authorization, 
   input validation, and API security for maritime insurance platform."

5. **Accessibility Testing**
   "Create accessibility test suite ensuring WCAG 2.1 AA compliance for 
   users with visual, motor, and cognitive disabilities."
```

### Sentry MCP Integration for Bug Analysis

**AI-Powered Error Resolution:**

```typescript
// Sentry MCP Configuration
const sentryMCPConfig = {
  project: 'fleet-risk-dashboard',
  ai_features: {
    seer: true,              // Automated root cause analysis
    suggested_fixes: true,    // AI-generated fix suggestions
    similar_issues: true,     // Find related bugs
    impact_analysis: true,    // User impact assessment
  },
  automation: {
    auto_assign: true,       // Assign to relevant developer
    priority_scoring: true,   // AI-based priority
    alert_grouping: true,    // Smart alert consolidation
  },
};

// Example AI-generated bug fix
const aiFix = {
  issue: "TypeError in vessel position update",
  root_cause: "Async state update race condition",
  suggested_solution: `
    // Use callback form of setState to ensure latest state
    setVessels(prevVessels => 
      prevVessels.map(vessel => 
        vessel.id === updatedVessel.id 
          ? { ...vessel, ...updatedVessel }
          : vessel
      )
    );
  `,
  confidence: 0.92,
  similar_fixes: 3,
};
```

### Lighthouse MCP Performance Optimization

**AI-Driven Performance Improvements:**

```javascript
// Lighthouse MCP Analysis
const performanceAnalysis = {
  current_metrics: {
    lcp: 3.2,
    inp: 245,
    cls: 0.12,
    overall_score: 76
  },
  ai_recommendations: [
    {
      issue: "Large Contentful Paint delay",
      impact: "+18 points",
      solution: "Preload hero image and critical fonts",
      implementation: `
        <link rel="preload" as="image" href="/hero-dashboard.webp">
        <link rel="preload" as="font" href="/fonts/main.woff2" crossorigin>
      `
    },
    {
      issue: "JavaScript execution blocking",
      impact: "+12 points",
      solution: "Defer non-critical scripts",
      implementation: `
        // Move analytics and monitoring to post-load
        if ('requestIdleCallback' in window) {
          requestIdleCallback(() => loadAnalytics());
        }
      `
    }
  ]
};
```

---

## Quality Gates and Deliverables

### Testing Phase Deliverables

1. **Test Documentation**
   - Comprehensive test plan (100% complete)
   - Test case repository (422 test cases)
   - Test execution reports (7 days of testing)
   - Bug tracking reports (23 bugs logged)

2. **Quality Metrics**
   - Code coverage report: 92.5%
   - Performance benchmark results
   - Security audit report
   - Accessibility compliance certificate

3. **Deployment Artifacts**
   - Tested build artifacts (v1.0.0-rc.1)
   - Configuration files validated
   - Database migration scripts tested
   - Rollback procedures verified

4. **Sign-off Documentation**
   - Stakeholder approval matrix
   - Risk assessment document
   - Deployment readiness checklist
   - Go-live communication plan

### Success Criteria Achievement

| Criteria | Target | Actual | Status |
|----------|--------|--------|--------|
| Test Coverage | 90%+ | 92.5% | ✅ Exceeded |
| Performance (Lighthouse) | 90+ | 94 | ✅ Exceeded |
| Bug Fix Rate | 95%+ | 91.3% | ⚠️ Met (2 deferred) |
| Security Vulnerabilities | 0 Critical | 0 | ✅ Met |
| Cross-Browser Support | 100% | 100% | ✅ Met |
| Accessibility (WCAG AA) | Required | Passed | ✅ Met |
| Load Test (100 users) | <500ms p95 | 287ms | ✅ Exceeded |

### Deployment Readiness Score: 98/100

**Recommendation**: APPROVED FOR PRODUCTION DEPLOYMENT

---

## Continuous Improvement Recommendations

### Post-Deployment Monitoring
1. Set up Sentry alerts for production errors
2. Configure Lighthouse CI for continuous performance monitoring
3. Implement real user monitoring (RUM)
4. Schedule weekly security scans

### Test Suite Optimization
1. Parallelize E2E tests for faster execution
2. Implement visual regression testing baseline
3. Add chaos engineering tests for resilience
4. Create synthetic monitoring for critical paths

### Team Knowledge Sharing
1. Document test patterns and best practices
2. Create test writing guidelines
3. Conduct testing retrospective
4. Share AI-assisted testing workflows

**Testing Phase Duration**: 7 days
**Total Tests Executed**: 422
**Overall Quality Score**: 98/100
**Status**: READY FOR PRODUCTION