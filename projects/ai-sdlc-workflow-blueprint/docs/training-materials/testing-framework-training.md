# Testing Framework Training Guide

## Overview

This comprehensive training guide provides hands-on instruction for implementing a modern testing framework in maritime insurance applications. Our testing strategy emphasizes Test-Driven Development (TDD), achieving 90%+ code coverage, and leveraging AI assistance for test generation and maintenance.

**Training Duration**: 3-day intensive program + 2 weeks practical application  
**Target Audience**: Frontend and Backend Developers  
**Prerequisites**: JavaScript/TypeScript knowledge, React basics, Node.js experience  

---

## Module 1: Testing Framework Overview (Day 1 Morning)

### Learning Objectives

By the end of this module, participants will:
- Understand the complete testing stack and tool selection rationale
- Master the testing pyramid concept for maritime insurance applications
- Configure all testing tools for optimal performance
- Implement AI-assisted test generation workflows

### 1.1 Testing Stack Architecture

#### Core Testing Tools

| Tool | Purpose | Why This Choice |
|------|---------|-----------------|
| **Vitest** | Unit testing | 10x faster than Jest, native TypeScript support |
| **React Testing Library** | Component testing | Tests user behavior, not implementation |
| **Storybook** | UI documentation | Component isolation and visual testing |
| **Playwright** | E2E testing | Cross-browser support (Chrome, Firefox, Safari) |

#### Supporting Tools

- **Coverage**: Vitest Coverage (V8 provider)
- **Performance**: Lighthouse CI
- **Error Tracking**: Sentry with AI analysis
- **Code Quality**: ESLint + Prettier + TypeScript

### 1.2 Testing Pyramid for Maritime Insurance

```
         /\
        /  \  E2E Tests (10%)
       /    \ - Critical user journeys
      /      \ - Cross-browser validation
     /________\
    /          \ Integration Tests (30%)
   /            \ - API endpoint testing
  /              \ - Database interactions
 /________________\
/                  \ Unit Tests (60%)
/                    \ - Business logic
/______________________\ - Component behavior
```

### 1.3 Environment Setup

#### Hands-On Exercise 1: Initial Configuration

```bash
# Create a new maritime insurance project
mkdir marine-insurance-app
cd marine-insurance-app
pnpm init
pnpm add -D vitest @vitest/ui @vitest/coverage-v8
pnpm add -D @testing-library/react @testing-library/jest-dom
pnpm add -D @playwright/test
pnpm add -D @storybook/react @storybook/addon-essentials
```

#### Configure Vitest

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test/setup.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      thresholds: {
        global: {
          branches: 90,
          functions: 90,
          lines: 90,
          statements: 90
        }
      }
    }
  }
});
```

### 1.4 AI-Assisted Test Generation Setup

#### Configure Claude Code Max Integration

1. Install Claude Code Max extension in your IDE
2. Create test generation templates:

```typescript
// test-templates/unit-test.template.ts
export const unitTestTemplate = `
Generate comprehensive unit tests for the following code:
- Test all public methods
- Include edge cases and error scenarios
- Use React Testing Library for components
- Include performance benchmarks for critical functions
- Add maritime insurance domain-specific test cases
`;
```

### Assessment Checkpoint 1

**Practical Task**: Set up a testing environment for a maritime insurance quote calculator
- Configure all testing tools
- Create a basic test structure
- Run initial test suite successfully

**Success Criteria**:
- [ ] All tools installed and configured
- [ ] Test runner executes successfully
- [ ] Coverage reporter generates output
- [ ] AI test generation template created

---

## Module 2: Core Testing Concepts (Day 1 Afternoon)

### Learning Objectives

- Master Test-Driven Development (TDD) methodology
- Understand coverage metrics and quality gates
- Implement continuous integration testing workflows
- Apply testing best practices to maritime insurance domain

### 2.1 Test-Driven Development (TDD)

#### The TDD Cycle

```
1. Write a failing test (Red)
2. Write minimal code to pass (Green)
3. Refactor with confidence (Refactor)
```

#### Hands-On Exercise 2: TDD for Premium Calculator

**Step 1: Write the test first**

```typescript
// src/services/premiumCalculator.test.ts
import { describe, it, expect } from 'vitest';
import { PremiumCalculator } from './premiumCalculator';

describe('PremiumCalculator', () => {
  it('calculates base premium for cargo vessel', () => {
    const calculator = new PremiumCalculator();
    const vessel = {
      type: 'cargo',
      value: 1000000,
      tonnage: 50000,
      age: 5
    };
    
    const premium = calculator.calculateBasePremium(vessel);
    
    expect(premium).toBe(15000); // 1.5% of value for cargo vessels
  });
});
```

**Step 2: Implement minimal code**

```typescript
// src/services/premiumCalculator.ts
export class PremiumCalculator {
  calculateBasePremium(vessel: any): number {
    const baseRate = vessel.type === 'cargo' ? 0.015 : 0.02;
    return vessel.value * baseRate;
  }
}
```

**Step 3: Refactor and add more tests**

```typescript
describe('PremiumCalculator', () => {
  let calculator: PremiumCalculator;

  beforeEach(() => {
    calculator = new PremiumCalculator();
  });

  describe('Base Premium Calculation', () => {
    it.each([
      { type: 'cargo', value: 1000000, expected: 15000 },
      { type: 'tanker', value: 2000000, expected: 40000 },
      { type: 'container', value: 1500000, expected: 22500 },
    ])('calculates premium for $type vessel', ({ type, value, expected }) => {
      const vessel = { type, value, tonnage: 50000, age: 5 };
      expect(calculator.calculateBasePremium(vessel)).toBe(expected);
    });
  });

  describe('Age Adjustments', () => {
    it('applies age penalty for vessels over 15 years', () => {
      const oldVessel = { type: 'cargo', value: 1000000, age: 20 };
      const newVessel = { type: 'cargo', value: 1000000, age: 5 };
      
      const oldPremium = calculator.calculateAdjustedPremium(oldVessel);
      const newPremium = calculator.calculateAdjustedPremium(newVessel);
      
      expect(oldPremium).toBeGreaterThan(newPremium);
      expect(oldPremium).toBe(newPremium * 1.25); // 25% age penalty
    });
  });
});
```

### 2.2 Coverage Targets and Quality Gates

#### Understanding Coverage Metrics

- **Line Coverage**: Percentage of code lines executed
- **Branch Coverage**: Percentage of decision branches tested
- **Function Coverage**: Percentage of functions called
- **Statement Coverage**: Percentage of statements executed

#### Implementing Quality Gates

```yaml
# .github/workflows/quality-gates.yml
name: Quality Gates
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: pnpm install
      - run: pnpm test:coverage
      
      - name: Check Coverage Thresholds
        run: |
          coverage_report=$(cat coverage/coverage-summary.json)
          lines=$(echo $coverage_report | jq '.total.lines.pct')
          if (( $(echo "$lines < 90" | bc -l) )); then
            echo "Coverage below 90%: $lines%"
            exit 1
          fi
```

### 2.3 CI/CD Integration Best Practices

#### Hands-On Exercise 3: Complete CI Pipeline

```yaml
# .github/workflows/ci.yml
name: CI Pipeline
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          
      - name: Install dependencies
        run: pnpm install --frozen-lockfile
        
      - name: Run unit tests
        run: pnpm test:unit
        
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  e2e-tests:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        browser: [chromium, firefox, webkit]
    steps:
      - uses: actions/checkout@v4
      - name: Install Playwright
        run: pnpm exec playwright install ${{ matrix.browser }}
        
      - name: Run E2E tests
        run: pnpm test:e2e --project=${{ matrix.browser }}
```

### Assessment Checkpoint 2

**Practical Task**: Implement TDD for a fleet risk assessment feature
- Write tests for risk calculation logic
- Achieve 90%+ coverage
- Set up CI pipeline with quality gates

**Success Criteria**:
- [ ] All tests written before implementation
- [ ] Coverage meets 90% threshold
- [ ] CI pipeline runs on every commit
- [ ] Quality gates enforce standards

---

## Module 3: Maritime Insurance Testing Patterns (Day 2 Morning)

### Learning Objectives

- Apply domain-specific testing patterns for maritime insurance
- Test complex business rules and calculations
- Validate compliance and regulatory requirements
- Handle maritime-specific edge cases

### 3.1 Domain-Specific Test Patterns

#### Fleet Management Testing

```typescript
// src/features/fleet/fleetManagement.test.ts
import { describe, it, expect, beforeEach } from 'vitest';
import { FleetManager } from './fleetManager';
import { createMockVessel, createMockFleet } from '../test/factories';

describe('Fleet Management', () => {
  let fleetManager: FleetManager;

  beforeEach(() => {
    fleetManager = new FleetManager();
  });

  describe('Fleet Composition Rules', () => {
    it('enforces maximum fleet size limits', () => {
      const fleet = createMockFleet({ size: 100 });
      const newVessel = createMockVessel();
      
      expect(() => {
        fleetManager.addVessel(fleet, newVessel);
      }).toThrow('Fleet size limit exceeded');
    });

    it('validates vessel compatibility within fleet', () => {
      const fleet = createMockFleet({ type: 'tanker' });
      const cargoVessel = createMockVessel({ type: 'cargo' });
      
      const result = fleetManager.validateVesselCompatibility(fleet, cargoVessel);
      
      expect(result.compatible).toBe(false);
      expect(result.reason).toContain('vessel type mismatch');
    });

    it('calculates fleet-wide risk profile', () => {
      const fleet = createMockFleet({
        vessels: [
          createMockVessel({ age: 5, value: 1000000 }),
          createMockVessel({ age: 15, value: 2000000 }),
          createMockVessel({ age: 25, value: 500000 })
        ]
      });
      
      const riskProfile = fleetManager.calculateFleetRisk(fleet);
      
      expect(riskProfile.averageAge).toBe(15);
      expect(riskProfile.riskScore).toBeGreaterThan(5);
      expect(riskProfile.category).toBe('medium-high');
    });
  });
});
```

#### Quote Generation Testing

```typescript
// src/features/quotes/quoteGeneration.test.ts
describe('Quote Generation', () => {
  describe('Multi-Vessel Quote Calculation', () => {
    it('applies bulk discount for large fleets', () => {
      const smallFleet = createMockFleet({ size: 5 });
      const largeFleet = createMockFleet({ size: 50 });
      
      const smallQuote = quoteGenerator.generateFleetQuote(smallFleet);
      const largeQuote = quoteGenerator.generateFleetQuote(largeFleet);
      
      const smallPerVessel = smallQuote.totalPremium / smallFleet.size;
      const largePerVessel = largeQuote.totalPremium / largeFleet.size;
      
      expect(largePerVessel).toBeLessThan(smallPerVessel * 0.85); // 15% bulk discount
    });

    it('handles voyage-specific coverage', () => {
      const vessel = createMockVessel({
        routes: ['Mediterranean', 'Red Sea', 'Persian Gulf']
      });
      
      const quote = quoteGenerator.generateVoyageQuote(vessel, {
        departure: 'Piraeus',
        destination: 'Dubai',
        cargo: { type: 'electronics', value: 5000000 }
      });
      
      expect(quote.coverage).toMatchObject({
        hull: expect.any(Number),
        cargo: 5000000,
        warRisk: expect.any(Number), // Required for Persian Gulf
        piracy: expect.any(Number)    // Required for Red Sea
      });
    });
  });
});
```

### 3.2 Risk Assessment Validation

#### Hands-On Exercise 4: Comprehensive Risk Testing

```typescript
// src/services/riskAssessment.test.ts
import { describe, it, expect } from 'vitest';
import { RiskAssessmentService } from './riskAssessment';
import { mockWeatherAPI, mockPirateActivityAPI } from '../test/mocks';

describe('Risk Assessment Service', () => {
  let service: RiskAssessmentService;

  beforeEach(() => {
    service = new RiskAssessmentService({
      weatherAPI: mockWeatherAPI,
      pirateAPI: mockPirateActivityAPI
    });
  });

  describe('Route Risk Calculation', () => {
    it('identifies high-risk maritime zones', async () => {
      const route = {
        waypoints: [
          { lat: 12.5, lon: 43.5 }, // Gulf of Aden
          { lat: 13.0, lon: 44.0 },
          { lat: 13.5, lon: 45.0 }
        ]
      };
      
      const assessment = await service.assessRouteRisk(route);
      
      expect(assessment.riskLevel).toBe('high');
      expect(assessment.factors).toContain('piracy-zone');
      expect(assessment.recommendations).toContain('armed-guards');
    });

    it('adjusts for seasonal weather patterns', async () => {
      mockWeatherAPI.setConditions({
        season: 'monsoon',
        waveHeight: 6,
        windSpeed: 45
      });
      
      const assessment = await service.assessVoyageRisk({
        route: 'Indian Ocean',
        date: new Date('2024-07-15')
      });
      
      expect(assessment.weatherRisk).toBe('severe');
      expect(assessment.premiumAdjustment).toBe(1.5);
    });
  });

  describe('Compliance Validation', () => {
    it('verifies IMO compliance requirements', () => {
      const vessel = createMockVessel({
        imoNumber: '1234567',
        certifications: ['ISM', 'ISPS', 'MLC']
      });
      
      const compliance = service.validateCompliance(vessel);
      
      expect(compliance.isCompliant).toBe(true);
      expect(compliance.missingCertifications).toHaveLength(0);
    });

    it('flags vessels with expired certifications', () => {
      const vessel = createMockVessel({
        certifications: [
          { type: 'ISM', expiry: new Date('2023-01-01') },
          { type: 'ISPS', expiry: new Date('2025-01-01') }
        ]
      });
      
      const compliance = service.validateCompliance(vessel);
      
      expect(compliance.isCompliant).toBe(false);
      expect(compliance.expiredCertifications).toContain('ISM');
    });
  });
});
```

### 3.3 Test Data Management for Maritime Domain

#### Creating Realistic Test Fixtures

```typescript
// src/test/fixtures/maritime-data.ts
export const maritimeTestData = {
  vessels: {
    cargoShip: {
      type: 'cargo',
      name: 'MV Mediterranean Star',
      imoNumber: '9876543',
      flag: 'GR',
      yearBuilt: 2018,
      tonnage: 75000,
      value: 25000000,
      specifications: {
        length: 299,
        beam: 48,
        draft: 14.5,
        enginePower: 18000
      }
    },
    tanker: {
      type: 'tanker',
      name: 'MT Aegean Spirit',
      imoNumber: '8765432',
      flag: 'MT',
      yearBuilt: 2015,
      tonnage: 150000,
      value: 45000000,
      cargoType: 'crude-oil',
      doubleHull: true
    }
  },
  
  routes: {
    mediterranean: {
      name: 'Mediterranean Trade Route',
      waypoints: ['Piraeus', 'Malta', 'Gibraltar', 'Marseille'],
      distance: 2800,
      transitTime: 7,
      riskZones: []
    },
    suezCanal: {
      name: 'Asia-Europe via Suez',
      waypoints: ['Singapore', 'Colombo', 'Suez', 'Port Said', 'Rotterdam'],
      distance: 8500,
      transitTime: 21,
      riskZones: ['Red Sea', 'Gulf of Aden']
    }
  },
  
  incidents: {
    collision: {
      type: 'collision',
      date: new Date('2023-06-15'),
      location: { lat: 36.8, lon: 23.5 },
      severity: 'major',
      estimatedLoss: 2500000
    },
    piracy: {
      type: 'piracy-attempt',
      date: new Date('2023-08-20'),
      location: { lat: 12.1, lon: 43.2 },
      severity: 'minor',
      outcome: 'repelled'
    }
  }
};
```

### Assessment Checkpoint 3

**Practical Task**: Create comprehensive tests for a voyage planning feature
- Test route risk assessment
- Validate compliance checks
- Handle weather-based adjustments
- Test fleet coordination rules

**Success Criteria**:
- [ ] Tests cover all business rules
- [ ] Maritime-specific edge cases handled
- [ ] Test data represents real scenarios
- [ ] Compliance validation implemented

---

## Module 4: Advanced Testing Techniques (Day 2 Afternoon)

### Learning Objectives

- Implement performance testing strategies
- Set up security testing patterns
- Configure cross-browser testing
- Master visual regression testing

### 4.1 Performance Testing with Lighthouse CI

#### Setting Up Performance Budgets

```javascript
// lighthouse.config.js
module.exports = {
  ci: {
    collect: {
      numberOfRuns: 3,
      startServerCommand: 'npm run preview',
      url: [
        'http://localhost:4173/',
        'http://localhost:4173/fleet-dashboard',
        'http://localhost:4173/quote-calculator'
      ]
    },
    assert: {
      assertions: {
        'categories:performance': ['error', { minScore: 0.9 }],
        'categories:accessibility': ['error', { minScore: 0.95 }],
        'first-contentful-paint': ['error', { maxNumericValue: 2000 }],
        'interactive': ['error', { maxNumericValue: 5000 }],
        'max-potential-fid': ['error', { maxNumericValue: 100 }],
        'cumulative-layout-shift': ['error', { maxNumericValue: 0.1 }]
      }
    },
    upload: {
      target: 'temporary-public-storage'
    }
  }
};
```

#### Hands-On Exercise 5: Performance Testing Implementation

```typescript
// src/features/dashboard/dashboard.perf.test.ts
import { test, expect } from '@playwright/test';
import { measurePerformance } from '../test/utils/performance';

test.describe('Dashboard Performance', () => {
  test('loads fleet overview within performance budget', async ({ page }) => {
    const metrics = await measurePerformance(page, async () => {
      await page.goto('/fleet-dashboard');
      await page.waitForSelector('[data-testid="fleet-overview"]');
    });
    
    expect(metrics.fcp).toBeLessThan(2000); // First Contentful Paint < 2s
    expect(metrics.lcp).toBeLessThan(2500); // Largest Contentful Paint < 2.5s
    expect(metrics.fid).toBeLessThan(100);  // First Input Delay < 100ms
    expect(metrics.cls).toBeLessThan(0.1);  // Cumulative Layout Shift < 0.1
  });

  test('handles large fleet data efficiently', async ({ page }) => {
    // Mock large dataset
    await page.route('/api/fleet/vessels', route => {
      const vessels = Array(1000).fill(null).map((_, i) => ({
        id: i,
        name: `Vessel ${i}`,
        type: 'cargo',
        status: 'active'
      }));
      
      route.fulfill({ json: { vessels } });
    });
    
    const startTime = Date.now();
    await page.goto('/fleet-dashboard');
    await page.waitForSelector('[data-testid="vessel-count"]');
    const loadTime = Date.now() - startTime;
    
    expect(loadTime).toBeLessThan(3000);
    
    // Test virtualization is working
    const visibleVessels = await page.locator('[data-testid^="vessel-row-"]').count();
    expect(visibleVessels).toBeLessThan(100); // Should virtualize, not render all 1000
  });
});
```

### 4.2 Security Testing Patterns

#### Implementing Security Test Suite

```typescript
// src/security/security.test.ts
import { describe, it, expect } from 'vitest';
import { SecurityValidator } from './securityValidator';

describe('Security Validation', () => {
  const validator = new SecurityValidator();

  describe('Input Sanitization', () => {
    it('prevents SQL injection in vessel search', () => {
      const maliciousInput = "'; DROP TABLE vessels; --";
      const sanitized = validator.sanitizeSearchInput(maliciousInput);
      
      expect(sanitized).not.toContain('DROP');
      expect(sanitized).not.toContain(';');
      expect(sanitized).toBe('DROP TABLE vessels');
    });

    it('prevents XSS in vessel names', () => {
      const xssAttempt = '<script>alert("XSS")</script>MV Legitimate';
      const sanitized = validator.sanitizeVesselName(xssAttempt);
      
      expect(sanitized).not.toContain('<script>');
      expect(sanitized).toBe('MV Legitimate');
    });
  });

  describe('Authentication Security', () => {
    it('enforces strong password requirements', () => {
      const weakPasswords = ['password', '12345678', 'maritime'];
      const strongPassword = 'M@r1t1m3Ins2024!';
      
      weakPasswords.forEach(pwd => {
        expect(validator.isPasswordStrong(pwd)).toBe(false);
      });
      
      expect(validator.isPasswordStrong(strongPassword)).toBe(true);
    });

    it('implements rate limiting for login attempts', async () => {
      const attempter = new LoginAttemptTracker();
      const ip = '192.168.1.100';
      
      // Simulate failed attempts
      for (let i = 0; i < 5; i++) {
        await attempter.recordFailedAttempt(ip);
      }
      
      expect(attempter.isBlocked(ip)).toBe(true);
      expect(attempter.getBlockDuration(ip)).toBe(900); // 15 minutes
    });
  });

  describe('Data Encryption', () => {
    it('encrypts sensitive vessel data', () => {
      const sensitiveData = {
        vesselId: '12345',
        ownerSSN: '123-45-6789',
        bankAccount: 'GR1234567890'
      };
      
      const encrypted = validator.encryptSensitiveData(sensitiveData);
      
      expect(encrypted).not.toContain('123-45-6789');
      expect(encrypted).not.toContain('GR1234567890');
      expect(validator.decryptData(encrypted)).toEqual(sensitiveData);
    });
  });
});
```

### 4.3 Cross-Browser Testing Strategy

#### Hands-On Exercise 6: Browser Compatibility Testing

```typescript
// e2e/cross-browser.spec.ts
import { test, expect, devices } from '@playwright/test';

test.describe('Cross-Browser Compatibility', () => {
  const browsers = ['chromium', 'firefox', 'webkit'];
  
  browsers.forEach(browserName => {
    test.describe(`${browserName} compatibility`, () => {
      test('quote calculator works across browsers', async ({ page }) => {
        await page.goto('/quote-calculator');
        
        // Fill form
        await page.fill('[data-testid="vessel-value"]', '1000000');
        await page.selectOption('[data-testid="vessel-type"]', 'cargo');
        await page.fill('[data-testid="vessel-age"]', '5');
        
        // Calculate quote
        await page.click('[data-testid="calculate-quote"]');
        
        // Verify results
        await expect(page.locator('[data-testid="quote-result"]')).toBeVisible();
        await expect(page.locator('[data-testid="premium-amount"]')).toContainText('$');
      });

      test('responsive design adapts correctly', async ({ page }) => {
        const viewports = [
          { width: 1920, height: 1080, name: 'desktop' },
          { width: 768, height: 1024, name: 'tablet' },
          { width: 375, height: 667, name: 'mobile' }
        ];
        
        for (const viewport of viewports) {
          await page.setViewportSize({ 
            width: viewport.width, 
            height: viewport.height 
          });
          
          await page.goto('/');
          
          if (viewport.name === 'mobile') {
            await expect(page.locator('[data-testid="mobile-menu"]')).toBeVisible();
            await expect(page.locator('[data-testid="desktop-nav"]')).not.toBeVisible();
          } else {
            await expect(page.locator('[data-testid="desktop-nav"]')).toBeVisible();
            await expect(page.locator('[data-testid="mobile-menu"]')).not.toBeVisible();
          }
        }
      });
    });
  });

  test('Safari-specific date handling', async ({ page, browserName }) => {
    test.skip(browserName !== 'webkit', 'Safari-specific test');
    
    await page.goto('/vessel-registration');
    
    // Safari handles date inputs differently
    await page.fill('[data-testid="build-date"]', '2020-01-15');
    
    const value = await page.inputValue('[data-testid="build-date"]');
    expect(value).toBe('2020-01-15');
  });
});
```

### 4.4 Visual Regression Testing

#### Setting Up Visual Testing

```typescript
// e2e/visual-regression.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Visual Regression Tests', () => {
  test.beforeEach(async ({ page }) => {
    // Set consistent viewport for screenshots
    await page.setViewportSize({ width: 1280, height: 720 });
    
    // Disable animations for consistent screenshots
    await page.addStyleTag({
      content: `
        *, *::before, *::after {
          animation-duration: 0s !important;
          animation-delay: 0s !important;
          transition-duration: 0s !important;
          transition-delay: 0s !important;
        }
      `
    });
  });

  test('fleet dashboard visual consistency', async ({ page }) => {
    await page.goto('/fleet-dashboard');
    await page.waitForLoadState('networkidle');
    
    // Take full page screenshot
    await expect(page).toHaveScreenshot('fleet-dashboard-full.png', {
      fullPage: true,
      threshold: 0.2
    });
    
    // Component-level screenshots
    await expect(page.locator('[data-testid="fleet-statistics"]'))
      .toHaveScreenshot('fleet-statistics.png');
    
    await expect(page.locator('[data-testid="vessel-map"]'))
      .toHaveScreenshot('vessel-map.png');
  });

  test('quote form visual states', async ({ page }) => {
    await page.goto('/quote-calculator');
    
    // Default state
    await expect(page.locator('[data-testid="quote-form"]'))
      .toHaveScreenshot('quote-form-default.png');
    
    // Error state
    await page.click('[data-testid="calculate-quote"]');
    await expect(page.locator('[data-testid="quote-form"]'))
      .toHaveScreenshot('quote-form-errors.png');
    
    // Success state
    await page.fill('[data-testid="vessel-value"]', '1000000');
    await page.selectOption('[data-testid="vessel-type"]', 'cargo');
    await page.click('[data-testid="calculate-quote"]');
    
    await expect(page.locator('[data-testid="quote-result"]'))
      .toHaveScreenshot('quote-result.png');
  });
});
```

### Assessment Checkpoint 4

**Practical Task**: Implement comprehensive testing for a claims submission feature
- Performance testing for file uploads
- Security validation for sensitive data
- Cross-browser form compatibility
- Visual regression for UI states

**Success Criteria**:
- [ ] Performance meets defined budgets
- [ ] Security tests prevent common vulnerabilities
- [ ] Works across all target browsers
- [ ] Visual tests catch UI regressions

---

## Module 5: Best Practices and Maintenance (Day 3)

### Learning Objectives

- Organize tests for scalability and maintenance
- Implement effective mocking strategies
- Handle asynchronous testing patterns
- Establish team testing standards

### 5.1 Test Organization and Structure

#### Recommended Project Structure

```
src/
├── components/
│   ├── VesselCard/
│   │   ├── VesselCard.tsx
│   │   ├── VesselCard.test.tsx
│   │   ├── VesselCard.stories.tsx
│   │   └── VesselCard.module.css
│   └── QuoteForm/
│       ├── QuoteForm.tsx
│       ├── QuoteForm.test.tsx
│       └── QuoteForm.stories.tsx
├── services/
│   ├── premiumCalculator/
│   │   ├── premiumCalculator.ts
│   │   ├── premiumCalculator.test.ts
│   │   └── premiumCalculator.perf.test.ts
│   └── riskAssessment/
│       ├── riskAssessment.ts
│       └── riskAssessment.test.ts
├── test/
│   ├── fixtures/
│   ├── factories/
│   ├── mocks/
│   ├── utils/
│   └── setup.ts
└── e2e/
    ├── workflows/
    ├── visual/
    └── performance/
```

#### Test Naming Conventions

```typescript
// Good test names that describe behavior
describe('PremiumCalculator', () => {
  describe('when calculating premiums for cargo vessels', () => {
    it('should apply base rate of 1.5% for standard cargo', () => {});
    it('should increase rate by 25% for hazardous cargo', () => {});
    it('should apply bulk discount for fleets over 20 vessels', () => {});
  });
});

// Avoid implementation-focused names
// Bad: it('should call calculateBaseRate method')
// Good: it('should calculate correct base premium for vessel value')
```

### 5.2 Mock Data and Fixtures

#### Creating Reusable Test Factories

```typescript
// src/test/factories/vesselFactory.ts
import { faker } from '@faker-js/faker';

export class VesselFactory {
  static create(overrides: Partial<Vessel> = {}): Vessel {
    return {
      id: faker.string.uuid(),
      name: `MV ${faker.company.name()}`,
      imoNumber: this.generateIMO(),
      type: faker.helpers.arrayElement(['cargo', 'tanker', 'container', 'bulk']),
      flag: faker.location.countryCode(),
      yearBuilt: faker.date.past({ years: 30 }).getFullYear(),
      tonnage: faker.number.int({ min: 5000, max: 200000 }),
      value: faker.number.int({ min: 500000, max: 50000000 }),
      specifications: this.generateSpecs(),
      certifications: this.generateCertifications(),
      ...overrides
    };
  }

  static createFleet(size: number = 10): Vessel[] {
    return Array(size).fill(null).map(() => this.create());
  }

  private static generateIMO(): string {
    const number = faker.number.int({ min: 1000000, max: 9999999 });
    return `IMO${number}`;
  }

  private static generateSpecs(): VesselSpecs {
    return {
      length: faker.number.int({ min: 100, max: 400 }),
      beam: faker.number.int({ min: 15, max: 60 }),
      draft: faker.number.float({ min: 5, max: 20, precision: 0.1 }),
      enginePower: faker.number.int({ min: 5000, max: 50000 })
    };
  }

  private static generateCertifications(): Certification[] {
    const certTypes = ['ISM', 'ISPS', 'MLC', 'MARPOL'];
    return certTypes.map(type => ({
      type,
      issueDate: faker.date.past({ years: 2 }),
      expiryDate: faker.date.future({ years: 3 }),
      issuingAuthority: faker.company.name()
    }));
  }
}
```

#### Hands-On Exercise 7: Advanced Mocking Patterns

```typescript
// src/test/mocks/externalServices.ts
import { vi } from 'vitest';

export const createWeatherAPIMock = () => {
  const mock = {
    getRouteWeather: vi.fn(),
    getPortConditions: vi.fn(),
    getSeasonalForecast: vi.fn()
  };

  // Default implementations
  mock.getRouteWeather.mockResolvedValue({
    conditions: 'moderate',
    waveHeight: 2.5,
    windSpeed: 15,
    visibility: 10
  });

  mock.getPortConditions.mockResolvedValue({
    operational: true,
    restrictions: []
  });

  return mock;
};

export const createPirateActivityAPIMock = () => {
  const mock = {
    checkRoute: vi.fn(),
    getIncidentHistory: vi.fn(),
    getRiskZones: vi.fn()
  };

  mock.checkRoute.mockImplementation(async (route) => {
    const highRiskZones = ['Gulf of Aden', 'Strait of Malacca'];
    const isHighRisk = highRiskZones.some(zone => 
      route.toLowerCase().includes(zone.toLowerCase())
    );

    return {
      riskLevel: isHighRisk ? 'high' : 'low',
      recentIncidents: isHighRisk ? 3 : 0,
      recommendedMeasures: isHighRisk ? ['armed-guards', 'convoy'] : []
    };
  });

  return mock;
};
```

### 5.3 Error Handling Testing

#### Comprehensive Error Scenario Testing

```typescript
// src/services/quoteService.test.ts
describe('Quote Service Error Handling', () => {
  describe('Network Failures', () => {
    it('retries failed API calls with exponential backoff', async () => {
      const mockAPI = vi.fn()
        .mockRejectedValueOnce(new Error('Network error'))
        .mockRejectedValueOnce(new Error('Network error'))
        .mockResolvedValueOnce({ premium: 50000 });

      const service = new QuoteService({ api: mockAPI });
      const quote = await service.generateQuote(mockVessel);

      expect(mockAPI).toHaveBeenCalledTimes(3);
      expect(quote.premium).toBe(50000);
    });

    it('falls back to cached rates after max retries', async () => {
      const mockAPI = vi.fn().mockRejectedValue(new Error('Network error'));
      const mockCache = { getLastKnownRates: vi.fn().mockResolvedValue({ base: 0.015 }) };

      const service = new QuoteService({ api: mockAPI, cache: mockCache });
      const quote = await service.generateQuote(mockVessel);

      expect(mockAPI).toHaveBeenCalledTimes(3); // Max retries
      expect(mockCache.getLastKnownRates).toHaveBeenCalled();
      expect(quote.warning).toContain('cached rates');
    });
  });

  describe('Data Validation Errors', () => {
    it('provides helpful error messages for invalid vessel data', () => {
      const invalidVessels = [
        { vessel: { tonnage: -1000 }, error: 'Tonnage must be positive' },
        { vessel: { yearBuilt: 2030 }, error: 'Year built cannot be in the future' },
        { vessel: { value: 0 }, error: 'Vessel value must be greater than zero' }
      ];

      invalidVessels.forEach(({ vessel, error }) => {
        expect(() => service.validateVessel(vessel)).toThrow(error);
      });
    });
  });

  describe('Business Rule Violations', () => {
    it('rejects quotes for vessels over age limit', async () => {
      const oldVessel = createMockVessel({ yearBuilt: 1970 });
      
      await expect(service.generateQuote(oldVessel))
        .rejects.toThrow('Vessel exceeds maximum insurable age');
    });

    it('requires additional approval for high-value vessels', async () => {
      const expensiveVessel = createMockVessel({ value: 100000000 });
      
      const quote = await service.generateQuote(expensiveVessel);
      
      expect(quote.status).toBe('pending-approval');
      expect(quote.approvalRequired).toBe(true);
      expect(quote.approvalReason).toContain('high value');
    });
  });
});
```

### 5.4 Maintenance and Refactoring

#### Test Maintenance Best Practices

```typescript
// src/test/utils/testHelpers.ts
export class TestHelper {
  // Centralize common test operations
  static async loginAs(page: Page, role: 'admin' | 'broker' | 'customer') {
    const credentials = {
      admin: { email: 'admin@marine.com', password: 'AdminPass123!' },
      broker: { email: 'broker@marine.com', password: 'BrokerPass123!' },
      customer: { email: 'customer@marine.com', password: 'CustomerPass123!' }
    };

    await page.goto('/login');
    await page.fill('[data-testid="email"]', credentials[role].email);
    await page.fill('[data-testid="password"]', credentials[role].password);
    await page.click('[data-testid="login-button"]');
    await page.waitForURL('/dashboard');
  }

  // Reusable assertions
  static async expectQuoteInRange(quote: Quote, min: number, max: number) {
    expect(quote.premium).toBeGreaterThanOrEqual(min);
    expect(quote.premium).toBeLessThanOrEqual(max);
    expect(quote.breakdown).toBeDefined();
    expect(quote.validity).toBeGreaterThan(Date.now());
  }

  // Common data setup
  static async setupTestFleet(size: number = 5): Promise<Fleet> {
    const vessels = VesselFactory.createFleet(size);
    const fleet = await FleetService.create({
      name: `Test Fleet ${Date.now()}`,
      vessels
    });
    
    return fleet;
  }
}
```

#### Refactoring Tests for Better Maintainability

```typescript
// Before: Duplicated test logic
test('calculates premium for cargo vessel', async () => {
  const vessel = { type: 'cargo', value: 1000000, tonnage: 50000 };
  const calculator = new PremiumCalculator();
  const premium = calculator.calculate(vessel);
  expect(premium).toBe(15000);
});

test('calculates premium for tanker vessel', async () => {
  const vessel = { type: 'tanker', value: 2000000, tonnage: 100000 };
  const calculator = new PremiumCalculator();
  const premium = calculator.calculate(vessel);
  expect(premium).toBe(40000);
});

// After: Parameterized tests
describe('Premium Calculation', () => {
  const testCases = [
    { type: 'cargo', value: 1000000, tonnage: 50000, expected: 15000 },
    { type: 'tanker', value: 2000000, tonnage: 100000, expected: 40000 },
    { type: 'container', value: 1500000, tonnage: 75000, expected: 22500 }
  ];

  test.each(testCases)(
    'calculates premium for $type vessel',
    ({ type, value, tonnage, expected }) => {
      const vessel = { type, value, tonnage };
      const premium = calculator.calculate(vessel);
      expect(premium).toBe(expected);
    }
  );
});
```

### Assessment Checkpoint 5

**Practical Task**: Refactor and optimize an existing test suite
- Identify and eliminate test duplication
- Implement shared test utilities
- Improve test performance
- Add missing error scenarios

**Success Criteria**:
- [ ] Test execution time reduced by 30%
- [ ] No duplicated test logic
- [ ] All error paths covered
- [ ] Tests remain readable and maintainable

---

## Final Project: Comprehensive Testing Implementation

### Project Overview

Implement a complete testing suite for a maritime insurance claims processing system including:

1. **Unit Tests**: Business logic for claim validation and processing
2. **Integration Tests**: API endpoints and database operations
3. **E2E Tests**: Complete claim submission workflow
4. **Performance Tests**: Handle 100 concurrent claim submissions
5. **Visual Tests**: Claim form and status dashboard

### Requirements

```typescript
// Features to test:
interface ClaimSystem {
  // Claim submission with multiple document uploads
  submitClaim(claim: ClaimData, documents: Document[]): Promise<ClaimId>;
  
  // Real-time claim status tracking
  trackClaim(claimId: ClaimId): Observable<ClaimStatus>;
  
  // Automated claim validation
  validateClaim(claim: ClaimData): ValidationResult;
  
  // Risk assessment for claim approval
  assessClaimRisk(claim: ClaimData): RiskAssessment;
  
  // Multi-party approval workflow
  processApprovals(claimId: ClaimId, approvals: Approval[]): Promise<void>;
}
```

### Evaluation Criteria

1. **Coverage**: Achieve 95%+ code coverage
2. **Performance**: All operations complete within defined SLAs
3. **Cross-browser**: Works on Chrome, Firefox, Safari
4. **Security**: Prevents common vulnerabilities
5. **Maintainability**: Well-organized, documented tests

---

## Competency Assessment

### Technical Skills Assessment

**Level 1: Foundation**
- [ ] Can write basic unit tests
- [ ] Understands coverage metrics
- [ ] Can run test suites
- [ ] Basic debugging skills

**Level 2: Proficient**
- [ ] Implements TDD methodology
- [ ] Writes comprehensive test suites
- [ ] Uses mocking effectively
- [ ] Handles async testing

**Level 3: Advanced**
- [ ] Designs test architectures
- [ ] Implements performance testing
- [ ] Creates reusable test utilities
- [ ] Mentors others in testing

**Level 4: Expert**
- [ ] Drives testing strategy
- [ ] Optimizes test performance
- [ ] Implements advanced patterns
- [ ] Innovates testing approaches

### Practical Assessment Tasks

1. **Bug Hunt Challenge**: Given a buggy component, write tests to identify all issues
2. **Performance Optimization**: Improve slow test suite performance by 50%
3. **Coverage Gap Analysis**: Achieve 95% coverage on legacy code
4. **Cross-browser Debug**: Fix browser-specific test failures

---

## Resources and References

### Documentation
- [Vitest Documentation](https://vitest.dev/)
- [React Testing Library](https://testing-library.com/react)
- [Playwright Documentation](https://playwright.dev/)
- [Storybook Documentation](https://storybook.js.org/)

### Maritime Insurance Testing Resources
- IMO Compliance Testing Guidelines
- Marine Insurance Act Testing Requirements
- P&I Club System Testing Standards

### Continuous Learning
- Weekly testing technique workshops
- Monthly tool updates and new features
- Quarterly testing strategy reviews
- Annual testing conference participation

---

## Conclusion

This comprehensive training program equips developers with the skills needed to implement and maintain a robust testing framework for maritime insurance applications. By combining modern testing tools with domain-specific knowledge and AI assistance, teams can achieve exceptional code quality while maintaining rapid development velocity.

Remember: Testing is not about finding bugs—it's about building confidence in your code and ensuring your maritime insurance systems protect both your customers and your business.