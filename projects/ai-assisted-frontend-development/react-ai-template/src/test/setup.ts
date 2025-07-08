/**
 * Jest Test Setup Configuration
 * AI-generated comprehensive test environment setup
 */

import '@testing-library/jest-dom';
import { configure } from '@testing-library/react';
import { TextEncoder, TextDecoder } from 'util';
import { jest } from '@jest/globals';

// Configure React Testing Library
configure({
  testIdAttribute: 'data-testid',
  asyncUtilTimeout: 5000,
  computedStyleSupportsPseudoElements: true,
});

// Mock Web APIs not available in jsdom
global.TextEncoder = TextEncoder;
global.TextDecoder = TextDecoder;

// Mock ResizeObserver
global.ResizeObserver = jest.fn().mockImplementation(() => ({
  observe: jest.fn(),
  unobserve: jest.fn(),
  disconnect: jest.fn(),
}));

// Mock IntersectionObserver
global.IntersectionObserver = jest.fn().mockImplementation(() => ({
  observe: jest.fn(),
  unobserve: jest.fn(),
  disconnect: jest.fn(),
}));

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(),
    removeListener: jest.fn(),
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});

// Mock window.scrollTo
Object.defineProperty(window, 'scrollTo', {
  writable: true,
  value: jest.fn(),
});

// Mock HTMLElement.scrollIntoView
Object.defineProperty(HTMLElement.prototype, 'scrollIntoView', {
  writable: true,
  value: jest.fn(),
});

// Mock Web Vitals
jest.mock('web-vitals', () => ({
  getCLS: jest.fn(),
  getFID: jest.fn(),
  getFCP: jest.fn(),
  getLCP: jest.fn(),
  getTTFB: jest.fn(),
}));

// Mock framer-motion
jest.mock('framer-motion', () => ({
  motion: {
    div: 'div',
    span: 'span',
    button: 'button',
    img: 'img',
    a: 'a',
    p: 'p',
    h1: 'h1',
    h2: 'h2',
    h3: 'h3',
    ul: 'ul',
    li: 'li',
    nav: 'nav',
    section: 'section',
    article: 'article',
    aside: 'aside',
    header: 'header',
    footer: 'footer',
    main: 'main',
  },
  AnimatePresence: ({ children }: { children: React.ReactNode }) => children,
  useAnimation: () => ({
    start: jest.fn(),
    stop: jest.fn(),
    set: jest.fn(),
  }),
}));

// Mock lucide-react icons
jest.mock('lucide-react', () => ({
  Search: () => <div data-testid="search-icon">Search</div>,
  Filter: () => <div data-testid="filter-icon">Filter</div>,
  Grid: () => <div data-testid="grid-icon">Grid</div>,
  List: () => <div data-testid="list-icon">List</div>,
  ChevronDown: () => <div data-testid="chevron-down-icon">ChevronDown</div>,
  Star: () => <div data-testid="star-icon">Star</div>,
  Heart: () => <div data-testid="heart-icon">Heart</div>,
  ShoppingCart: () => <div data-testid="cart-icon">ShoppingCart</div>,
}));

// Mock React Router
jest.mock('react-router-dom', () => ({
  BrowserRouter: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  Route: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  Routes: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
  Link: ({ children, to }: { children: React.ReactNode; to: string }) => (
    <a href={to}>{children}</a>
  ),
  useNavigate: () => jest.fn(),
  useLocation: () => ({ pathname: '/' }),
  useParams: () => ({}),
}));

// Mock Zustand
jest.mock('zustand', () => ({
  create: jest.fn(() => jest.fn()),
}));

// Mock React Query
jest.mock('@tanstack/react-query', () => ({
  useQuery: jest.fn(),
  useMutation: jest.fn(),
  QueryClient: jest.fn(),
  QueryClientProvider: ({ children }: { children: React.ReactNode }) => <div>{children}</div>,
}));

// Console spy setup for testing
beforeEach(() => {
  jest.clearAllMocks();
});

// Cleanup after each test
afterEach(() => {
  jest.clearAllTimers();
  jest.useRealTimers();
});

// Global test utilities
declare global {
  namespace jest {
    interface Matchers<R> {
      toBeInTheDocument(): R;
      toHaveAccessibleName(name: string): R;
      toHaveAccessibleDescription(description: string): R;
    }
  }
}

// Performance testing utilities
export const measurePerformance = <T>(fn: () => T): { result: T; duration: number } => {
  const start = performance.now();
  const result = fn();
  const duration = performance.now() - start;
  return { result, duration };
};

// Accessibility testing utilities
export const axeConfig = {
  rules: {
    'color-contrast': { enabled: true },
    'keyboard-navigation': { enabled: true },
    'aria-labels': { enabled: true },
    'focus-management': { enabled: true },
  },
};

// Mock data generators
export const generateMockProduct = (overrides: Partial<any> = {}) => ({
  id: `product-${Math.random().toString(36).substr(2, 9)}`,
  name: `Test Product ${Math.floor(Math.random() * 1000)}`,
  description: 'A high-quality test product with excellent features',
  price: Math.floor(Math.random() * 1000) + 10,
  category: 'electronics',
  image: `https://picsum.photos/300/200?random=${Math.random()}`,
  inStock: Math.random() > 0.3,
  rating: Math.floor(Math.random() * 5) + 1,
  reviewCount: Math.floor(Math.random() * 1000),
  tags: ['test', 'quality', 'featured'],
  ...overrides,
});

export const generateMockProducts = (count: number = 10) => {
  return Array.from({ length: count }, (_, index) => 
    generateMockProduct({ 
      id: `product-${index}`,
      name: `Test Product ${index}`,
    })
  );
};

// Test performance thresholds
export const PERFORMANCE_THRESHOLDS = {
  RENDER_TIME: 100, // ms
  SEARCH_DEBOUNCE: 350, // ms
  ANIMATION_DURATION: 300, // ms
  BUNDLE_SIZE: 500, // kb
} as const;

// Accessibility test helpers
export const waitForAccessibleName = async (element: HTMLElement, name: string) => {
  await expect(element).toHaveAccessibleName(name);
};

export const checkKeyboardNavigation = async (element: HTMLElement) => {
  element.focus();
  expect(element).toHaveFocus();
  
  // Test Enter key
  await userEvent.keyboard('{Enter}');
  
  // Test Space key
  await userEvent.keyboard(' ');
  
  // Test Tab navigation
  await userEvent.keyboard('{Tab}');
};

// Visual regression helpers
export const takeScreenshot = async (element: HTMLElement, name: string) => {
  // Mock implementation for visual regression testing
  return Promise.resolve(`screenshot-${name}.png`);
};

// Error boundary test helper
export const ErrorBoundaryWrapper = ({ children }: { children: React.ReactNode }) => {
  return (
    <div role="alert" data-testid="error-boundary">
      {children}
    </div>
  );
};

// Load testing utilities
export const stressTestComponent = async (
  renderFn: () => void,
  iterations: number = 100
) => {
  const results = [];
  
  for (let i = 0; i < iterations; i++) {
    const { duration } = measurePerformance(renderFn);
    results.push(duration);
  }
  
  return {
    average: results.reduce((sum, time) => sum + time, 0) / results.length,
    max: Math.max(...results),
    min: Math.min(...results),
    iterations: results.length,
  };
};

// Memory leak detection
export const detectMemoryLeaks = () => {
  const initialMemory = (performance as any).memory?.usedJSHeapSize || 0;
  
  return {
    check: () => {
      const currentMemory = (performance as any).memory?.usedJSHeapSize || 0;
      const diff = currentMemory - initialMemory;
      
      if (diff > 1024 * 1024) { // 1MB threshold
        console.warn(`Potential memory leak detected: ${diff} bytes`);
      }
      
      return diff;
    }
  };
};

console.log('🧪 Test environment setup complete with AI-generated utilities');