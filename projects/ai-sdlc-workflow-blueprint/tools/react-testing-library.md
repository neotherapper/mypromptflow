# React Testing Library - User-Centric Component Testing

## Overview

React Testing Library is a testing utility that focuses on testing components from the user's perspective. It encourages testing practices that closely resemble how users interact with the application, making tests more maintainable and providing better confidence in the application's behavior.

## Key Benefits

### User-Centric Testing
- **Test user interactions** rather than implementation details
- **Accessibility-first approach** ensuring components work for all users
- **Behavioral testing** that focuses on what users can see and do
- **Better test maintainability** with tests that survive refactoring

### Developer Experience Benefits
- **Confidence in refactoring** with tests that survive implementation changes
- **Quick feedback loops** with fast test execution
- **Clear debugging** with descriptive test failures
- **Living documentation** through readable test scenarios

## Configuration

### Basic Setup with Vitest

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    globals: true,
  },
});
```

### Test Setup Configuration

```typescript
// src/test/setup.ts
import '@testing-library/jest-dom';
import { expect, afterEach } from 'vitest';
import { cleanup } from '@testing-library/react';
import * as matchers from '@testing-library/jest-dom/matchers';

// Extend Vitest's expect with jest-dom matchers
expect.extend(matchers);

// Clean up after each test
afterEach(() => {
  cleanup();
});

// Mock maritime insurance API
global.fetch = vi.fn();

// Mock Sentry for testing
vi.mock('@sentry/react', () => ({
  captureException: vi.fn(),
  addBreadcrumb: vi.fn(),
  setContext: vi.fn(),
}));
```

## Maritime Insurance Component Testing

### Fleet Management Component Tests

```typescript
// components/FleetManagement/__tests__/FleetManagement.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { FleetManagement } from '../FleetManagement';
import { mockFleetData } from '../../test/fixtures/fleet-fixtures';

describe('FleetManagement', () => {
  const user = userEvent.setup();

  beforeEach(() => {
    // Mock API responses
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => mockFleetData,
    });
  });

  describe('Fleet Creation', () => {
    it('allows user to create a new fleet', async () => {
      render(<FleetManagement />);
      
      // Click "Add Fleet" button
      await user.click(screen.getByRole('button', { name: /add fleet/i }));
      
      // Fill in fleet details
      await user.type(
        screen.getByLabelText(/fleet name/i),
        'Mediterranean Cargo Fleet'
      );
      
      await user.type(
        screen.getByLabelText(/fleet size/i),
        '25'
      );
      
      await user.selectOptions(
        screen.getByLabelText(/fleet type/i),
        'cargo'
      );
      
      // Submit form
      await user.click(screen.getByRole('button', { name: /create fleet/i }));
      
      // Verify fleet was created
      await waitFor(() => {
        expect(screen.getByText('Mediterranean Cargo Fleet')).toBeInTheDocument();
      });
      
      // Verify API was called correctly
      expect(global.fetch).toHaveBeenCalledWith('/api/fleets', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: 'Mediterranean Cargo Fleet',
          size: 25,
          type: 'cargo',
        }),
      });
    });

    it('shows validation errors for invalid fleet data', async () => {
      render(<FleetManagement />);
      
      await user.click(screen.getByRole('button', { name: /add fleet/i }));
      
      // Try to submit without required fields
      await user.click(screen.getByRole('button', { name: /create fleet/i }));
      
      // Verify validation errors
      expect(screen.getByText(/fleet name is required/i)).toBeInTheDocument();
      expect(screen.getByText(/fleet size must be greater than 0/i)).toBeInTheDocument();
      expect(screen.getByText(/fleet type is required/i)).toBeInTheDocument();
    });
  });

  describe('Vessel Management', () => {
    it('allows adding vessels to an existing fleet', async () => {
      render(<FleetManagement />);
      
      // Select existing fleet
      await user.click(screen.getByRole('button', { name: /manage vessels/i }));
      
      // Add vessel
      await user.click(screen.getByRole('button', { name: /add vessel/i }));
      
      // Fill vessel details
      await user.type(
        screen.getByLabelText(/vessel name/i),
        'MV Poseidon'
      );
      
      await user.type(
        screen.getByLabelText(/vessel tonnage/i),
        '50000'
      );
      
      await user.type(
        screen.getByLabelText(/vessel value/i),
        '2000000'
      );
      
      await user.selectOptions(
        screen.getByLabelText(/vessel flag/i),
        'GR'
      );
      
      // Submit vessel
      await user.click(screen.getByRole('button', { name: /add vessel/i }));
      
      // Verify vessel was added
      await waitFor(() => {
        expect(screen.getByText('MV Poseidon')).toBeInTheDocument();
        expect(screen.getByText('50,000 DWT')).toBeInTheDocument();
        expect(screen.getByText('$2,000,000')).toBeInTheDocument();
      });
    });
  });

  describe('Error Handling', () => {
    it('handles API errors gracefully', async () => {
      // Mock API error
      global.fetch = vi.fn().mockRejectedValue(new Error('API Error'));
      
      render(<FleetManagement />);
      
      await user.click(screen.getByRole('button', { name: /add fleet/i }));
      
      // Fill form and submit
      await user.type(screen.getByLabelText(/fleet name/i), 'Test Fleet');
      await user.click(screen.getByRole('button', { name: /create fleet/i }));
      
      // Verify error message
      await waitFor(() => {
        expect(screen.getByText(/failed to create fleet/i)).toBeInTheDocument();
      });
    });
  });
});
```

### Quote Generation Component Tests

```typescript
// components/QuoteGenerator/__tests__/QuoteGenerator.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QuoteGenerator } from '../QuoteGenerator';
import { mockQuoteRequest, mockQuoteResponse } from '../../test/fixtures/quote-fixtures';

describe('QuoteGenerator', () => {
  const user = userEvent.setup();

  beforeEach(() => {
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => mockQuoteResponse,
    });
  });

  describe('Quote Request Flow', () => {
    it('generates quote for fleet with multiple vessels', async () => {
      render(<QuoteGenerator />);
      
      // Select fleet
      await user.selectOptions(
        screen.getByLabelText(/select fleet/i),
        'mediterranean-cargo-fleet'
      );
      
      // Verify fleet details loaded
      await waitFor(() => {
        expect(screen.getByText('25 vessels')).toBeInTheDocument();
        expect(screen.getByText('Total Value: $50,000,000')).toBeInTheDocument();
      });
      
      // Select route
      await user.selectOptions(
        screen.getByLabelText(/primary route/i),
        'mediterranean-sea'
      );
      
      // Set coverage options
      await user.click(screen.getByLabelText(/hull coverage/i));
      await user.click(screen.getByLabelText(/cargo coverage/i));
      await user.click(screen.getByLabelText(/liability coverage/i));
      
      // Generate quote
      await user.click(screen.getByRole('button', { name: /generate quote/i }));
      
      // Verify quote results
      await waitFor(() => {
        expect(screen.getByText(/quote generated successfully/i)).toBeInTheDocument();
        expect(screen.getByText('Premium: $125,000')).toBeInTheDocument();
        expect(screen.getByText('Coverage: $50,000,000')).toBeInTheDocument();
        expect(screen.getByText('Deductible: $25,000')).toBeInTheDocument();
      });
    });

    it('handles high-risk route surcharges', async () => {
      render(<QuoteGenerator />);
      
      // Select fleet and high-risk route
      await user.selectOptions(screen.getByLabelText(/select fleet/i), 'tanker-fleet');
      await user.selectOptions(screen.getByLabelText(/primary route/i), 'horn-of-africa');
      
      // Check high-risk warning
      await user.click(screen.getByRole('button', { name: /generate quote/i }));
      
      await waitFor(() => {
        expect(screen.getByText(/high-risk route surcharge applied/i)).toBeInTheDocument();
        expect(screen.getByText(/additional security measures required/i)).toBeInTheDocument();
      });
    });
  });

  describe('Validation', () => {
    it('validates required fields before quote generation', async () => {
      render(<QuoteGenerator />);
      
      // Try to generate quote without required fields
      await user.click(screen.getByRole('button', { name: /generate quote/i }));
      
      // Verify validation messages
      expect(screen.getByText(/fleet selection is required/i)).toBeInTheDocument();
      expect(screen.getByText(/route selection is required/i)).toBeInTheDocument();
      expect(screen.getByText(/at least one coverage type must be selected/i)).toBeInTheDocument();
    });
  });
});
```

### Broker Competition Component Tests

```typescript
// components/BrokerCompetition/__tests__/BrokerCompetition.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { BrokerCompetition } from '../BrokerCompetition';
import { mockBrokerResponses } from '../../test/fixtures/broker-fixtures';

describe('BrokerCompetition', () => {
  const user = userEvent.setup();

  beforeEach(() => {
    // Mock WebSocket for real-time broker responses
    global.WebSocket = vi.fn().mockImplementation(() => ({
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      send: vi.fn(),
      close: vi.fn(),
    }));
  });

  describe('Competition Flow', () => {
    it('displays real-time broker responses', async () => {
      const mockWebSocket = {
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
        send: vi.fn(),
        close: vi.fn(),
      };
      
      global.WebSocket = vi.fn().mockImplementation(() => mockWebSocket);
      
      render(<BrokerCompetition />);
      
      // Start competition
      await user.click(screen.getByRole('button', { name: /start competition/i }));
      
      // Simulate broker responses
      const messageHandler = mockWebSocket.addEventListener.mock.calls
        .find(([event]) => event === 'message')[1];
      
      // Simulate first broker response
      messageHandler({
        data: JSON.stringify({
          broker: 'Lloyds',
          quote: { premium: 125000, coverage: 50000000, deductible: 25000 }
        })
      });
      
      // Verify broker response displayed
      await waitFor(() => {
        expect(screen.getByText('Lloyds')).toBeInTheDocument();
        expect(screen.getByText('$125,000')).toBeInTheDocument();
      });
    });

    it('allows comparison of multiple broker quotes', async () => {
      render(<BrokerCompetition />);
      
      // Mock multiple broker responses
      const brokerData = mockBrokerResponses;
      
      // Simulate receiving all broker responses
      brokerData.forEach(broker => {
        fireEvent(window, new CustomEvent('brokerResponse', {
          detail: broker
        }));
      });
      
      // Verify all brokers displayed
      await waitFor(() => {
        expect(screen.getByText('Lloyds')).toBeInTheDocument();
        expect(screen.getByText('AIG')).toBeInTheDocument();
        expect(screen.getByText('Zurich')).toBeInTheDocument();
      });
      
      // Test quote comparison
      await user.click(screen.getByRole('button', { name: /compare quotes/i }));
      
      // Verify comparison table
      expect(screen.getByText(/quote comparison/i)).toBeInTheDocument();
      expect(screen.getByText(/best value/i)).toBeInTheDocument();
    });
  });
});
```

## AI-Assisted Test Development

### Using AI Coding Assistants

Modern AI coding assistants can help generate React Testing Library tests. Here are practical approaches:

#### GitHub Copilot
```typescript
// Type a comment describing the test, and Copilot will suggest implementation
// Example: Write test for fleet creation with invalid data

// Copilot will suggest test structure based on your component patterns
describe('FleetManagement', () => {
  // Start typing test descriptions and let Copilot complete them
  it('should validate fleet size is positive number', async () => {
    // Copilot learns from your existing test patterns
  });
});
```

#### Cursor AI / Codeium
```typescript
// Use inline prompts to generate specific test scenarios
// Example prompt: "Generate a test that verifies broker competition real-time updates"

// These tools can analyze your component and suggest comprehensive tests
// based on the component's props, state, and user interactions
```

#### Claude / ChatGPT (Copy-Paste Workflow)
```typescript
// 1. Copy your component code
// 2. Ask: "Generate React Testing Library tests for this maritime insurance component"
// 3. Specify requirements:
//    - Test user interactions
//    - Include error scenarios
//    - Use maritime insurance context
//    - Follow RTL best practices

// Example request:
/*
Please generate React Testing Library tests for a FleetManagement component that:
- Allows users to create fleets with name, size, and type
- Validates required fields
- Handles API errors gracefully
- Shows loading states during API calls
*/
```

### Test Generation Best Practices

```typescript
// test/fixtures/maritime-fixtures.ts
// Create reusable test data that AI assistants can reference

export const mockFleetData = {
  id: 'fleet-001',
  name: 'Mediterranean Cargo Fleet',
  vessels: [
    {
      id: 'vessel-001',
      name: 'MV Poseidon',
      type: 'cargo',
      tonnage: 50000,
      value: 2000000,
      flag: 'GR'
    }
  ],
  totalValue: 50000000,
  activePolicies: 3
};

// AI assistants can use these fixtures to generate consistent test data
```

### Automated Test Execution

```typescript
// package.json scripts for test automation
{
  "scripts": {
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage",
    "test:watch": "vitest --watch",
    "test:ci": "vitest --run --coverage --reporter=junit",
    "test:a11y": "vitest --run --grep accessibility"
  }
}
```

### CI/CD Integration

```yaml
# .github/workflows/test.yml
name: Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm ci
      
      - name: Run tests
        run: npm run test:ci
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage/coverage-final.json
      
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-results
          path: test-results.xml
```

## Custom Testing Utilities

```typescript
// test/utils/maritime-test-utils.tsx
import { render, RenderOptions } from '@testing-library/react';
import { ReactElement } from 'react';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MaritimeInsuranceProvider } from '../../contexts/MaritimeInsuranceContext';

// Create custom render function with providers
const AllTheProviders = ({ children }: { children: React.ReactNode }) => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  });

  return (
    <BrowserRouter>
      <QueryClientProvider client={queryClient}>
        <MaritimeInsuranceProvider>
          {children}
        </MaritimeInsuranceProvider>
      </QueryClientProvider>
    </BrowserRouter>
  );
};

const customRender = (
  ui: ReactElement,
  options?: Omit<RenderOptions, 'wrapper'>
) => render(ui, { wrapper: AllTheProviders, ...options });

// Maritime insurance specific test utilities
export const createMockFleet = (overrides = {}) => ({
  id: 'fleet-1',
  name: 'Mediterranean Cargo Fleet',
  type: 'cargo',
  size: 25,
  totalValue: 50000000,
  vessels: [
    {
      id: 'vessel-1',
      name: 'MV Poseidon',
      type: 'cargo',
      tonnage: 50000,
      value: 2000000,
      flag: 'GR',
      yearBuilt: 2020,
    },
  ],
  ...overrides,
});

export const createMockQuote = (overrides = {}) => ({
  id: 'quote-1',
  premium: 125000,
  coverage: 50000000,
  deductible: 25000,
  validUntil: new Date('2024-12-31'),
  coverageTypes: ['hull', 'cargo', 'liability'],
  ...overrides,
});

export const waitForLoadingToFinish = () => 
  waitFor(() => {
    expect(screen.queryByText(/loading/i)).not.toBeInTheDocument();
  });

export * from '@testing-library/react';
export { customRender as render };
```

## Advanced Testing Patterns

### Visual Regression Testing

```typescript
// test/visual-regression/fleet-components.test.tsx
import { render } from '../utils/maritime-test-utils';
import { FleetCard } from '../../components/FleetCard';

describe('Visual Regression Tests', () => {
  it('fleet card matches visual snapshot', () => {
    const { container } = render(
      <FleetCard 
        fleet={{
          name: 'Mediterranean Cargo Fleet',
          vessels: 25,
          totalValue: 50000000,
          status: 'active'
        }}
      />
    );
    
    // Using Vitest's snapshot feature
    expect(container.firstChild).toMatchSnapshot();
  });
});
```

### Component State Testing

```typescript
// Testing complex state interactions
describe('Fleet State Management', () => {
  it('maintains state across vessel additions', async () => {
    const { rerender } = render(<FleetManagement />);
    const user = userEvent.setup();
    
    // Add first vessel
    await user.click(screen.getByRole('button', { name: /add vessel/i }));
    await user.type(screen.getByLabelText(/vessel name/i), 'MV Atlas');
    await user.click(screen.getByRole('button', { name: /save/i }));
    
    // Verify vessel count
    expect(screen.getByText('1 vessel')).toBeInTheDocument();
    
    // Add second vessel
    await user.click(screen.getByRole('button', { name: /add vessel/i }));
    await user.type(screen.getByLabelText(/vessel name/i), 'MV Titan');
    await user.click(screen.getByRole('button', { name: /save/i }));
    
    // Verify both vessels are present
    expect(screen.getByText('2 vessels')).toBeInTheDocument();
    expect(screen.getByText('MV Atlas')).toBeInTheDocument();
    expect(screen.getByText('MV Titan')).toBeInTheDocument();
  });
});
```

### Integration Testing

```typescript
// integration-tests/fleet-to-quote.test.tsx
import { render, screen, fireEvent, waitFor } from '../test/utils/maritime-test-utils';
import userEvent from '@testing-library/user-event';
import { FleetToQuoteFlow } from '../components/FleetToQuoteFlow';

describe('Fleet to Quote Integration', () => {
  const user = userEvent.setup();

  it('completes full flow from fleet creation to quote generation', async () => {
    render(<FleetToQuoteFlow />);
    
    // Step 1: Create fleet
    await user.click(screen.getByRole('button', { name: /create fleet/i }));
    await user.type(screen.getByLabelText(/fleet name/i), 'Test Fleet');
    await user.click(screen.getByRole('button', { name: /save fleet/i }));
    
    // Step 2: Add vessels
    await user.click(screen.getByRole('button', { name: /add vessel/i }));
    await user.type(screen.getByLabelText(/vessel name/i), 'MV Test');
    await user.type(screen.getByLabelText(/vessel value/i), '1000000');
    await user.click(screen.getByRole('button', { name: /add vessel/i }));
    
    // Step 3: Generate quote
    await user.click(screen.getByRole('button', { name: /generate quote/i }));
    await user.selectOptions(screen.getByLabelText(/route/i), 'safe-route');
    await user.click(screen.getByRole('button', { name: /get quote/i }));
    
    // Verify quote generated
    await waitFor(() => {
      expect(screen.getByText(/quote generated/i)).toBeInTheDocument();
      expect(screen.getByText(/premium/i)).toBeInTheDocument();
    });
  });
});
```

### Accessibility Testing

```typescript
// accessibility-tests/accessibility.test.tsx
import { render } from '../test/utils/maritime-test-utils';
import { axe, toHaveNoViolations } from 'jest-axe';
import { FleetManagement } from '../components/FleetManagement';

expect.extend(toHaveNoViolations);

describe('Accessibility Tests', () => {
  it('has no accessibility violations', async () => {
    const { container } = render(<FleetManagement />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('supports keyboard navigation', async () => {
    render(<FleetManagement />);
    
    // Test keyboard navigation
    const addButton = screen.getByRole('button', { name: /add fleet/i });
    addButton.focus();
    expect(addButton).toHaveFocus();
    
    // Tab through form elements
    await user.keyboard('{Tab}');
    expect(screen.getByLabelText(/fleet name/i)).toHaveFocus();
  });
});
```

## Team Integration

### Development Team Usage

#### Head of Engineering
- **Test strategy oversight**: Monitor test coverage and quality metrics
- **CI/CD integration**: Ensure tests run in deployment pipeline
- **Performance monitoring**: Track test execution time and reliability

#### Lead Frontend Developer
- **Component testing**: Write and maintain component tests
- **User interaction testing**: Test complex user workflows
- **Integration testing**: Ensure components work together properly

#### Lead Backend Developer
- **API integration testing**: Test frontend-backend communication
- **Data validation testing**: Ensure proper data handling
- **Error handling testing**: Test error scenarios and recovery

#### UI/UX Engineer
- **Accessibility testing**: Ensure components are accessible
- **Visual testing**: Test component appearance and behavior
- **User experience testing**: Validate user workflow functionality

## Best Practices

### Writing Effective Tests
- **Test user behavior** not implementation details
- **Use semantic queries** (getByRole, getByLabelText, getByText)
- **Include accessibility testing** with every component
- **Mock external dependencies** appropriately

### Test Organization
- **Group related tests** with describe blocks
- **Use descriptive test names** that explain the expected behavior
- **Keep tests focused** on single behaviors or features
- **Maintain test fixtures** for reusable test data

### Maintenance
- **Update tests with code changes** to avoid false positives
- **Regular test review** to ensure tests remain valuable
- **Monitor test coverage** to identify untested areas
- **Refactor tests** when they become hard to maintain

---

## Real-World Testing Tips

### Common Testing Scenarios

#### Testing Loading States
```typescript
it('shows loading spinner while fetching fleet data', async () => {
  render(<FleetManagement />);
  
  // Loading state should appear immediately
  expect(screen.getByRole('progressbar')).toBeInTheDocument();
  
  // Wait for loading to complete
  await waitFor(() => {
    expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
  });
});
```

#### Testing Form Validation
```typescript
it('prevents form submission with invalid data', async () => {
  render(<QuoteGenerator />);
  const user = userEvent.setup();
  
  // Submit without filling required fields
  await user.click(screen.getByRole('button', { name: /generate quote/i }));
  
  // Check for validation messages
  expect(screen.getByText(/fleet selection is required/i)).toBeInTheDocument();
  
  // Ensure form was not submitted
  expect(global.fetch).not.toHaveBeenCalled();
});
```

#### Testing Error Recovery
```typescript
it('allows retry after API failure', async () => {
  // First attempt fails
  global.fetch = vi.fn().mockRejectedValueOnce(new Error('Network error'));
  
  render(<FleetManagement />);
  const user = userEvent.setup();
  
  await user.click(screen.getByRole('button', { name: /load fleets/i }));
  
  // Error message appears
  await waitFor(() => {
    expect(screen.getByText(/failed to load fleets/i)).toBeInTheDocument();
  });
  
  // Mock successful retry
  global.fetch = vi.fn().mockResolvedValueOnce({
    ok: true,
    json: async () => mockFleetData
  });
  
  // Click retry
  await user.click(screen.getByRole('button', { name: /retry/i }));
  
  // Data loads successfully
  await waitFor(() => {
    expect(screen.getByText('Mediterranean Cargo Fleet')).toBeInTheDocument();
  });
});
```

---

**Monthly Cost**: $0 (Open Source)  
**AI Assistance**: ✅ Compatible with GitHub Copilot, Cursor, Codeium, and LLM chat interfaces  
**Coverage**: ✅ Component, integration, and accessibility testing  
**Maritime Insurance**: ✅ Domain-specific testing patterns and fixtures