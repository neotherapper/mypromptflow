/**
 * AI-Generated Performance Test Suite for SearchableProductList Component
 * 
 * Performance Testing Focus:
 * - Render performance with large datasets
 * - Search debouncing efficiency
 * - Memory usage optimization
 * - Bundle size impact
 * - Core Web Vitals metrics
 */

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { jest } from '@jest/globals';

import SearchableProductList from '../SearchableProductList';
import { 
  generateMockProducts, 
  measurePerformance,
  PERFORMANCE_THRESHOLDS,
  detectMemoryLeaks,
  stressTestComponent
} from '../../../test/setup';

// Mock performance.mark and performance.measure
const mockPerformanceMark = jest.fn();
const mockPerformanceMeasure = jest.fn();
Object.defineProperty(window, 'performance', {
  value: {
    ...window.performance,
    mark: mockPerformanceMark,
    measure: mockPerformanceMeasure,
    now: jest.fn(() => Date.now()),
  },
});

describe('SearchableProductList Performance Tests', () => {
  const defaultProps = {
    products: generateMockProducts(100),
    onProductSelect: jest.fn(),
    loading: false,
    error: undefined,
  };

  beforeEach(() => {
    jest.clearAllMocks();
    mockPerformanceMark.mockClear();
    mockPerformanceMeasure.mockClear();
  });

  describe('Render Performance', () => {
    test('initial render performance with 100 products', () => {
      const { duration } = measurePerformance(() => {
        render(<SearchableProductList {...defaultProps} />);
      });

      expect(duration).toBeLessThan(PERFORMANCE_THRESHOLDS.RENDER_TIME);
    });

    test('initial render performance with 1000 products', () => {
      const largeDataset = generateMockProducts(1000);
      const props = { ...defaultProps, products: largeDataset };

      const { duration } = measurePerformance(() => {
        render(<SearchableProductList {...props} />);
      });

      // Allow more time for larger datasets
      expect(duration).toBeLessThan(PERFORMANCE_THRESHOLDS.RENDER_TIME * 3);
    });

    test('initial render performance with 10000 products', () => {
      const veryLargeDataset = generateMockProducts(10000);
      const props = { ...defaultProps, products: veryLargeDataset };

      const { duration } = measurePerformance(() => {
        render(<SearchableProductList {...props} />);
      });

      // Even with very large datasets, should complete within reasonable time
      expect(duration).toBeLessThan(PERFORMANCE_THRESHOLDS.RENDER_TIME * 10);
    });

    test('re-render performance when products change', async () => {
      const { rerender } = render(<SearchableProductList {...defaultProps} />);

      const newProducts = generateMockProducts(150);
      const { duration } = measurePerformance(() => {
        rerender(<SearchableProductList {...defaultProps} products={newProducts} />);
      });

      expect(duration).toBeLessThan(PERFORMANCE_THRESHOLDS.RENDER_TIME);
    });
  });

  describe('Search Performance', () => {
    test('search filtering performance with large dataset', async () => {
      const largeDataset = generateMockProducts(5000);
      render(<SearchableProductList {...defaultProps} products={largeDataset} />);

      const searchInput = screen.getByRole('textbox', { name: /search products/i });

      const { duration } = measurePerformance(() => {
        fireEvent.change(searchInput, { target: { value: 'test' } });
      });

      expect(duration).toBeLessThan(PERFORMANCE_THRESHOLDS.SEARCH_DEBOUNCE);
    });

    test('debounced search performance', async () => {
      jest.useFakeTimers();

      const largeDataset = generateMockProducts(1000);
      render(<SearchableProductList {...defaultProps} products={largeDataset} />);

      const searchInput = screen.getByRole('textbox', { name: /search products/i });

      // Simulate rapid typing
      const startTime = performance.now();
      
      await userEvent.type(searchInput, 'q');
      jest.advanceTimersByTime(50);
      await userEvent.type(searchInput, 'u');
      jest.advanceTimersByTime(50);
      await userEvent.type(searchInput, 'e');
      jest.advanceTimersByTime(50);
      await userEvent.type(searchInput, 'r');
      jest.advanceTimersByTime(50);
      await userEvent.type(searchInput, 'y');
      
      // Complete debounce
      jest.advanceTimersByTime(300);
      
      const endTime = performance.now();
      const totalTime = endTime - startTime;

      expect(totalTime).toBeLessThan(PERFORMANCE_THRESHOLDS.SEARCH_DEBOUNCE * 2);

      jest.useRealTimers();
    });

    test('search result rendering performance', async () => {
      const products = generateMockProducts(1000);
      render(<SearchableProductList {...defaultProps} products={products} />);

      const searchInput = screen.getByRole('textbox', { name: /search products/i });

      const { duration } = measurePerformance(async () => {
        await userEvent.type(searchInput, 'Product 1');
        await waitFor(() => {
          expect(screen.getByText('Product 1')).toBeInTheDocument();
        });
      });

      expect(duration).toBeLessThan(PERFORMANCE_THRESHOLDS.RENDER_TIME * 2);
    });
  });

  describe('Filtering Performance', () => {
    test('category filtering performance', async () => {
      const products = generateMockProducts(2000);
      render(<SearchableProductList {...defaultProps} products={products} />);

      // Open filters
      await userEvent.click(screen.getByRole('button', { name: /filters/i }));

      const categorySelect = screen.getByLabelText(/category/i);

      const { duration } = measurePerformance(async () => {
        await userEvent.selectOptions(categorySelect, 'electronics');
      });

      expect(duration).toBeLessThan(PERFORMANCE_THRESHOLDS.RENDER_TIME);
    });

    test('multiple filter combination performance', async () => {
      const products = generateMockProducts(3000);
      render(<SearchableProductList {...defaultProps} products={products} />);

      // Open filters
      await userEvent.click(screen.getByRole('button', { name: /filters/i }));

      const { duration } = measurePerformance(async () => {
        // Apply multiple filters
        await userEvent.selectOptions(screen.getByLabelText(/category/i), 'electronics');
        await userEvent.click(screen.getByLabelText(/in stock only/i));
        await userEvent.selectOptions(screen.getByLabelText(/minimum rating/i), '3');
      });

      expect(duration).toBeLessThan(PERFORMANCE_THRESHOLDS.RENDER_TIME * 2);
    });
  });

  describe('Sorting Performance', () => {
    test('sorting performance with large dataset', async () => {
      const products = generateMockProducts(5000);
      render(<SearchableProductList {...defaultProps} products={products} />);

      const sortSelect = screen.getByLabelText(/sort products by/i);

      const { duration } = measurePerformance(async () => {
        await userEvent.selectOptions(sortSelect, 'name');
      });

      expect(duration).toBeLessThan(PERFORMANCE_THRESHOLDS.RENDER_TIME * 2);
    });

    test('relevance sorting performance', async () => {
      const products = generateMockProducts(1000);
      render(<SearchableProductList {...defaultProps} products={products} />);

      const searchInput = screen.getByRole('textbox', { name: /search products/i });
      const sortSelect = screen.getByLabelText(/sort products by/i);

      const { duration } = measurePerformance(async () => {
        await userEvent.type(searchInput, 'test');
        await userEvent.selectOptions(sortSelect, 'relevance');
      });

      expect(duration).toBeLessThan(PERFORMANCE_THRESHOLDS.RENDER_TIME * 3);
    });
  });

  describe('View Mode Performance', () => {
    test('switching from grid to list view performance', async () => {
      const products = generateMockProducts(1000);
      render(<SearchableProductList {...defaultProps} products={products} />);

      const listButton = screen.getByRole('button', { name: /list view/i });

      const { duration } = measurePerformance(async () => {
        await userEvent.click(listButton);
      });

      expect(duration).toBeLessThan(PERFORMANCE_THRESHOLDS.RENDER_TIME);
    });

    test('switching from list to grid view performance', async () => {
      const products = generateMockProducts(1000);
      render(<SearchableProductList {...defaultProps} products={products} />);

      // Switch to list view first
      await userEvent.click(screen.getByRole('button', { name: /list view/i }));

      const gridButton = screen.getByRole('button', { name: /grid view/i });

      const { duration } = measurePerformance(async () => {
        await userEvent.click(gridButton);
      });

      expect(duration).toBeLessThan(PERFORMANCE_THRESHOLDS.RENDER_TIME);
    });
  });

  describe('Pagination Performance', () => {
    test('pagination rendering performance', () => {
      const products = generateMockProducts(1000);
      
      const { duration } = measurePerformance(() => {
        render(<SearchableProductList {...defaultProps} products={products} itemsPerPage={20} />);
      });

      expect(duration).toBeLessThan(PERFORMANCE_THRESHOLDS.RENDER_TIME * 2);
    });

    test('page navigation performance', async () => {
      const products = generateMockProducts(500);
      render(<SearchableProductList {...defaultProps} products={products} itemsPerPage={25} />);

      const secondPageButton = screen.getByRole('button', { name: /go to page 2/i });

      const { duration } = measurePerformance(async () => {
        await userEvent.click(secondPageButton);
      });

      expect(duration).toBeLessThan(PERFORMANCE_THRESHOLDS.RENDER_TIME);
    });
  });

  describe('Memory Performance', () => {
    test('memory usage with large dataset', async () => {
      const memoryTracker = detectMemoryLeaks();
      
      const products = generateMockProducts(10000);
      const { unmount } = render(<SearchableProductList {...defaultProps} products={products} />);

      // Simulate user interactions
      const searchInput = screen.getByRole('textbox');
      await userEvent.type(searchInput, 'test search query');
      
      // Apply filters
      await userEvent.click(screen.getByRole('button', { name: /filters/i }));
      await userEvent.selectOptions(screen.getByLabelText(/category/i), 'electronics');

      // Clean up
      unmount();
      
      const memoryDiff = memoryTracker.check();
      expect(memoryDiff).toBeLessThan(10 * 1024 * 1024); // Less than 10MB
    });

    test('memory cleanup after component unmount', () => {
      const memoryTracker = detectMemoryLeaks();
      
      const { unmount } = render(<SearchableProductList {...defaultProps} />);
      
      // Trigger multiple re-renders
      for (let i = 0; i < 10; i++) {
        fireEvent.change(screen.getByRole('textbox'), { target: { value: `query${i}` } });
      }
      
      unmount();
      
      const memoryDiff = memoryTracker.check();
      expect(memoryDiff).toBeLessThan(5 * 1024 * 1024); // Less than 5MB
    });
  });

  describe('Stress Testing', () => {
    test('component stability under rapid interactions', async () => {
      const products = generateMockProducts(1000);
      render(<SearchableProductList {...defaultProps} products={products} />);

      const searchInput = screen.getByRole('textbox');
      const filterButton = screen.getByRole('button', { name: /filters/i });
      const sortSelect = screen.getByLabelText(/sort products by/i);

      // Perform rapid interactions
      for (let i = 0; i < 50; i++) {
        await userEvent.type(searchInput, `query${i}`);
        await userEvent.clear(searchInput);
        
        if (i % 10 === 0) {
          await userEvent.click(filterButton);
          await userEvent.selectOptions(sortSelect, i % 2 === 0 ? 'name' : 'price');
        }
      }

      // Component should still be functional
      expect(screen.getByRole('textbox')).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /filters/i })).toBeInTheDocument();
    });

    test('performance consistency across multiple renders', async () => {
      const products = generateMockProducts(500);
      const results = [];

      for (let i = 0; i < 10; i++) {
        const { duration } = measurePerformance(() => {
          const { unmount } = render(<SearchableProductList {...defaultProps} products={products} />);
          unmount();
        });
        results.push(duration);
      }

      const averageTime = results.reduce((sum, time) => sum + time, 0) / results.length;
      const maxTime = Math.max(...results);
      const minTime = Math.min(...results);

      expect(averageTime).toBeLessThan(PERFORMANCE_THRESHOLDS.RENDER_TIME * 2);
      expect(maxTime - minTime).toBeLessThan(PERFORMANCE_THRESHOLDS.RENDER_TIME); // Consistent performance
    });

    test('load testing with extreme dataset size', async () => {
      const extremeDataset = generateMockProducts(50000);
      
      const performanceResults = await stressTestComponent(
        () => {
          const { unmount } = render(<SearchableProductList {...defaultProps} products={extremeDataset} />);
          unmount();
        },
        3
      );

      expect(performanceResults.average).toBeLessThan(PERFORMANCE_THRESHOLDS.RENDER_TIME * 10);
      expect(performanceResults.max).toBeLessThan(PERFORMANCE_THRESHOLDS.RENDER_TIME * 20);
    });
  });

  describe('Real-world Performance Scenarios', () => {
    test('e-commerce search performance simulation', async () => {
      const products = generateMockProducts(5000);
      render(<SearchableProductList {...defaultProps} products={products} />);

      // Simulate real user search behavior
      const searchInput = screen.getByRole('textbox');
      
      const searchQueries = [
        'i', 'ip', 'iph', 'ipho', 'iphon', 'iphone', 'iphone 1', 'iphone 15'
      ];

      for (const query of searchQueries) {
        const { duration } = measurePerformance(async () => {
          await userEvent.clear(searchInput);
          await userEvent.type(searchInput, query);
        });

        expect(duration).toBeLessThan(PERFORMANCE_THRESHOLDS.SEARCH_DEBOUNCE);
      }
    });

    test('filter refinement performance simulation', async () => {
      const products = generateMockProducts(3000);
      render(<SearchableProductList {...defaultProps} products={products} />);

      // Open filters
      await userEvent.click(screen.getByRole('button', { name: /filters/i }));

      // Simulate user refining filters
      const filterActions = [
        () => userEvent.selectOptions(screen.getByLabelText(/category/i), 'electronics'),
        () => userEvent.click(screen.getByLabelText(/in stock only/i)),
        () => userEvent.selectOptions(screen.getByLabelText(/minimum rating/i), '4'),
        () => userEvent.selectOptions(screen.getByLabelText(/category/i), 'clothing'),
        () => userEvent.selectOptions(screen.getByLabelText(/minimum rating/i), '3'),
      ];

      for (const action of filterActions) {
        const { duration } = measurePerformance(async () => {
          await action();
        });

        expect(duration).toBeLessThan(PERFORMANCE_THRESHOLDS.RENDER_TIME * 2);
      }
    });
  });
});

// Export performance benchmarks for CI/CD integration
export const performanceBenchmarks = {
  renderTime: PERFORMANCE_THRESHOLDS.RENDER_TIME,
  searchDebounce: PERFORMANCE_THRESHOLDS.SEARCH_DEBOUNCE,
  animationDuration: PERFORMANCE_THRESHOLDS.ANIMATION_DURATION,
  bundleSize: PERFORMANCE_THRESHOLDS.BUNDLE_SIZE,
};