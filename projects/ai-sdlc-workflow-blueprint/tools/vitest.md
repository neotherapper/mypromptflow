# Vitest - Fast Unit Testing Framework

## Overview

Vitest is a blazing fast unit test framework powered by Vite, designed for modern JavaScript/TypeScript applications. It provides Jest-compatible APIs while offering superior performance and developer experience.

## Key Benefits

### Performance Advantages
- **10x faster** test execution compared to Jest
- **Hot Module Replacement (HMR)** for instant test feedback
- **Native TypeScript support** without additional configuration
- **Parallel test execution** by default

### Developer Experience
- **Vite ecosystem integration** for consistent tooling
- **Watch mode** with intelligent test re-running
- **Source map support** for accurate debugging
- **Rich CLI output** with clear error reporting

## Configuration

### Basic Vitest Setup

```javascript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test/setup.ts'],
    css: true,
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
      },
      exclude: [
        'node_modules/',
        'dist/',
        '**/*.test.ts',
        '**/*.spec.ts',
        'src/test/',
        '**/*.stories.tsx'
      ]
    }
  }
});
```

### Test Environment Setup

```typescript
// src/test/setup.ts
import '@testing-library/jest-dom';
import { vi } from 'vitest';

// Mock environment variables
vi.mock('../config/env', () => ({
  API_URL: 'http://localhost:8000',
  SENTRY_DSN: 'test-dsn',
}));

// Global test utilities
global.ResizeObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
}));
```

## AI-Enhanced Testing Patterns

### Claude Code Max Integration

```typescript
// Example: AI-generated test for marine quote calculator
import { describe, it, expect, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MarineQuoteCalculator } from './MarineQuoteCalculator';
import { createMockVessel, createMockCoverage } from '../test/factories';

describe('MarineQuoteCalculator', () => {
  let calculator: MarineQuoteCalculator;

  beforeEach(() => {
    calculator = new MarineQuoteCalculator();
  });

  // AI-generated comprehensive test cases
  describe('Premium Calculation', () => {
    it('calculates accurate premium for cargo vessel', async () => {
      const vessel = createMockVessel({
        type: 'cargo',
        tonnage: 50000,
        value: 2000000,
        route: 'mediterranean',
        yearBuilt: 2015
      });

      const quote = await calculator.calculatePremium(vessel);

      expect(quote.premium).toBeGreaterThan(0);
      expect(quote.premium).toBeLessThan(vessel.value * 0.1); // Max 10% of value
      expect(quote.coverage.hull).toBe(vessel.value);
      expect(quote.coverage.machinery).toBeGreaterThan(0);
      expect(quote.deductible).toBeGreaterThan(0);
    });

    it('applies correct risk factors for vessel age', async () => {
      const newVessel = createMockVessel({ yearBuilt: 2023 });
      const oldVessel = createMockVessel({ yearBuilt: 1990 });

      const newQuote = await calculator.calculatePremium(newVessel);
      const oldQuote = await calculator.calculatePremium(oldVessel);

      expect(oldQuote.premium).toBeGreaterThan(newQuote.premium);
      expect(oldQuote.riskFactor).toBeGreaterThan(newQuote.riskFactor);
    });

    it('handles edge cases for premium calculation', async () => {
      // AI-identified edge cases
      const edgeCases = [
        { tonnage: 0, expectError: true },
        { value: -1000, expectError: true },
        { tonnage: 999999, expectWarning: true },
        { yearBuilt: 1800, expectError: true },
        { yearBuilt: 2030, expectError: true }
      ];

      for (const testCase of edgeCases) {
        const vessel = createMockVessel(testCase);
        
        if (testCase.expectError) {
          await expect(calculator.calculatePremium(vessel))
            .rejects.toThrow();
        } else if (testCase.expectWarning) {
          const quote = await calculator.calculatePremium(vessel);
          expect(quote.warnings).toBeDefined();
          expect(quote.warnings.length).toBeGreaterThan(0);
        }
      }
    });
  });

  describe('Route Risk Assessment', () => {
    it('applies higher premiums for high-risk routes', async () => {
      const safeRoute = createMockVessel({ route: 'north_sea' });
      const riskRoute = createMockVessel({ route: 'gulf_of_aden' });

      const safeQuote = await calculator.calculatePremium(safeRoute);
      const riskQuote = await calculator.calculatePremium(riskRoute);

      expect(riskQuote.premium).toBeGreaterThan(safeQuote.premium);
      expect(riskQuote.routeRiskFactor).toBeGreaterThan(safeQuote.routeRiskFactor);
    });
  });

  describe('Performance', () => {
    it('calculates premium within performance threshold', async () => {
      const vessel = createMockVessel();
      const startTime = performance.now();
      
      await calculator.calculatePremium(vessel);
      
      const endTime = performance.now();
      const duration = endTime - startTime;
      
      expect(duration).toBeLessThan(100); // Should complete within 100ms
    });

    it('handles concurrent calculations efficiently', async () => {
      const vessels = Array(10).fill(null).map(() => createMockVessel());
      const startTime = performance.now();
      
      const quotes = await Promise.all(
        vessels.map(vessel => calculator.calculatePremium(vessel))
      );
      
      const endTime = performance.now();
      const duration = endTime - startTime;
      
      expect(quotes).toHaveLength(10);
      expect(duration).toBeLessThan(500); // All 10 should complete within 500ms
      quotes.forEach(quote => {
        expect(quote.premium).toBeGreaterThan(0);
      });
    });
  });
});
```

### Test Factories for Realistic Data

```typescript
// src/test/factories/vesselFactory.ts
import { faker } from '@faker-js/faker';

export interface MockVessel {
  id: string;
  type: 'cargo' | 'tanker' | 'container' | 'bulk';
  name: string;
  tonnage: number;
  value: number;
  yearBuilt: number;
  route: string;
  owner: string;
  flag: string;
}

export function createMockVessel(overrides: Partial<MockVessel> = {}): MockVessel {
  return {
    id: faker.string.uuid(),
    type: faker.helpers.arrayElement(['cargo', 'tanker', 'container', 'bulk']),
    name: `MV ${faker.company.name()}`,
    tonnage: faker.number.int({ min: 1000, max: 200000 }),
    value: faker.number.int({ min: 500000, max: 50000000 }),
    yearBuilt: faker.number.int({ min: 1980, max: 2024 }),
    route: faker.helpers.arrayElement([
      'mediterranean', 'north_sea', 'atlantic', 'pacific',
      'gulf_of_aden', 'suez_canal', 'panama_canal'
    ]),
    owner: faker.company.name(),
    flag: faker.location.countryCode(),
    ...overrides
  };
}

export function createMockCoverage(overrides: Partial<any> = {}) {
  return {
    hull: faker.number.int({ min: 1000000, max: 10000000 }),
    machinery: faker.number.int({ min: 100000, max: 1000000 }),
    cargo: faker.number.int({ min: 500000, max: 5000000 }),
    liability: faker.number.int({ min: 1000000, max: 50000000 }),
    ...overrides
  };
}
```

## Code Coverage Strategy

### Coverage Configuration

```javascript
// Comprehensive coverage setup
coverage: {
  provider: 'v8',
  reporter: ['text', 'json', 'html', 'lcov'],
  reportsDirectory: './coverage',
  
  // Strict thresholds for maritime insurance app
  thresholds: {
    global: {
      branches: 90,
      functions: 90,
      lines: 90,
      statements: 90
    },
    
    // Critical modules require higher coverage
    './src/services/calculator/': {
      branches: 95,
      functions: 95,
      lines: 95,
      statements: 95
    },
    
    './src/services/compliance/': {
      branches: 95,
      functions: 95,
      lines: 95,
      statements: 95
    }
  },
  
  // Exclude test files and non-critical paths
  exclude: [
    'node_modules/',
    'dist/',
    'coverage/',
    '**/*.test.ts',
    '**/*.spec.ts',
    '**/*.stories.tsx',
    'src/test/',
    'src/**/*.d.ts'
  ],
  
  // Include all TypeScript and JavaScript files
  include: [
    'src/**/*.ts',
    'src/**/*.tsx',
    'src/**/*.js',
    'src/**/*.jsx'
  ]
}
```

### Coverage Reporting Integration

```yaml
# GitHub Actions integration
- name: Run tests with coverage
  run: |
    npm run test:coverage
    npm run coverage:report

- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v3
  with:
    file: ./coverage/lcov.info
    flags: vitest
    name: vitest-coverage
```

## Performance Optimization

### Parallel Test Execution

```javascript
// vitest.config.ts optimization
export default defineConfig({
  test: {
    // Enable parallel execution
    threads: true,
    minThreads: 2,
    maxThreads: 6,
    
    // Optimize file watching
    watchExclude: [
      '**/node_modules/**',
      '**/dist/**',
      '**/coverage/**'
    ],
    
    // Pool configuration for better performance
    pool: 'threads',
    poolOptions: {
      threads: {
        singleThread: false,
        useAtomics: true
      }
    },
    
    // Timeout configuration
    testTimeout: 10000,
    hookTimeout: 10000
  }
});
```

### Test Isolation and Cleanup

```typescript
// Proper test isolation
import { afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';

afterEach(() => {
  // Clean up DOM after each test
  cleanup();
  
  // Reset all mocks
  vi.clearAllMocks();
  
  // Clear local storage
  localStorage.clear();
  sessionStorage.clear();
  
  // Reset fetch mocks
  fetchMock.resetMocks();
});
```

## CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/test.yml
name: Test Suite

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'
          
      - name: Install dependencies
        run: pnpm install --frozen-lockfile
        
      - name: Run type checking
        run: pnpm run type-check
        
      - name: Run linting
        run: pnpm run lint
        
      - name: Run unit tests
        run: pnpm run test:coverage
        
      - name: Upload coverage reports
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage/lcov.info
          
      - name: Comment coverage on PR
        uses: romeovs/lcov-reporter-action@v0.3.1
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          lcov-file: ./coverage/lcov.info
```

## Integration with Other Tools

### React Testing Library Compatibility

```typescript
// Perfect compatibility with React Testing Library
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect } from 'vitest';

// All React Testing Library patterns work seamlessly
describe('QuoteForm Component', () => {
  it('submits form with valid data', async () => {
    render(<QuoteForm onSubmit={mockSubmit} />);
    
    fireEvent.change(screen.getByLabelText(/vessel name/i), {
      target: { value: 'MV Test Vessel' }
    });
    
    fireEvent.click(screen.getByRole('button', { name: /submit/i }));
    
    await waitFor(() => {
      expect(mockSubmit).toHaveBeenCalledWith(
        expect.objectContaining({
          vesselName: 'MV Test Vessel'
        })
      );
    });
  });
});
```

### Storybook Integration

```typescript
// Stories can be tested directly
import type { Meta, StoryObj } from '@storybook/react';
import { expect } from '@storybook/jest';
import { within, userEvent } from '@storybook/testing-library';

const meta: Meta<typeof QuoteForm> = {
  title: 'Forms/QuoteForm',
  component: QuoteForm,
};

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    
    // Vitest-compatible testing within Storybook
    await userEvent.type(canvas.getByLabelText(/vessel name/i), 'Test Vessel');
    await expect(canvas.getByDisplayValue('Test Vessel')).toBeInTheDocument();
  },
};
```

## Best Practices

### Test Organization
- **Group related tests** using nested `describe` blocks
- **Use descriptive test names** that explain the behavior being tested
- **Follow AAA pattern**: Arrange, Act, Assert
- **Test one behavior per test** to improve clarity and debugging

### Mocking Strategy
- **Mock external dependencies** (APIs, databases, file system)
- **Use real implementations** for internal business logic
- **Mock time-dependent code** using `vi.useFakeTimers()`
- **Reset mocks** between tests to prevent cross-test pollution

### Performance Considerations
- **Keep tests fast** - aim for under 10ms per unit test
- **Use parallel execution** for independent test suites
- **Avoid unnecessary setup** in beforeEach hooks
- **Profile slow tests** using Vitest's built-in performance monitoring

This Vitest configuration provides the foundation for fast, reliable, and AI-enhanced testing in the maritime insurance application, supporting the test-driven development approach with comprehensive coverage and excellent developer experience.

---

**Monthly Cost**: $0 (Open Source)  
**AI Integration**: ✅ Claude Code Max compatible  
**Performance**: 10x faster than Jest  
**Coverage**: 90%+ automated coverage tracking