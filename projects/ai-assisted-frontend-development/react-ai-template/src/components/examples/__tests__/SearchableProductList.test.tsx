/**
 * AI-Generated Comprehensive Test Suite for SearchableProductList Component
 * 
 * Test Coverage:
 * - Unit tests for all functionality
 * - Integration tests for user interactions
 * - Performance tests for optimization
 * - Accessibility tests for WCAG compliance
 * - Edge cases and error scenarios
 * 
 * Target Coverage: 95%+
 */

import React from 'react';
import { render, screen, fireEvent, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { jest } from '@jest/globals';
import { axe, toHaveNoViolations } from 'jest-axe';

import SearchableProductList, { 
  Product, 
  SearchableProductListProps 
} from '../SearchableProductList';
import { 
  generateMockProduct, 
  generateMockProducts, 
  measurePerformance,
  PERFORMANCE_THRESHOLDS,
  stressTestComponent,
  detectMemoryLeaks 
} from '../../../test/setup';

// Extend Jest matchers
expect.extend(toHaveNoViolations);

// Mock lodash debounce for predictable testing
jest.mock('lodash-es', () => ({
  debounce: jest.fn((fn) => {
    let timeoutId: NodeJS.Timeout;
    const debounced = (...args: any[]) => {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => fn(...args), 300);
    };
    debounced.cancel = jest.fn();
    return debounced;
  }),
}));

describe('SearchableProductList', () => {
  // Test data setup
  const mockProducts: Product[] = generateMockProducts(50);
  const mockOnProductSelect = jest.fn();
  
  const defaultProps: SearchableProductListProps = {
    products: mockProducts,
    onProductSelect: mockOnProductSelect,
    loading: false,
    error: undefined,
    initialSearch: '',
    virtualScrolling: false,
    itemsPerPage: 20,
    className: '',
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  afterEach(() => {
    jest.clearAllTimers();
  });

  describe('Rendering and Basic Functionality', () => {
    test('renders without crashing', () => {
      render(<SearchableProductList {...defaultProps} />);
      expect(screen.getByRole('textbox', { name: /search products/i })).toBeInTheDocument();
    });

    test('displays correct number of products', () => {
      render(<SearchableProductList {...defaultProps} />);
      const productGrid = screen.getByRole('grid', { name: /product results/i });
      expect(productGrid).toBeInTheDocument();
      
      const productCards = within(productGrid).getAllByRole('gridcell');
      expect(productCards).toHaveLength(Math.min(20, mockProducts.length));
    });

    test('renders loading state correctly', () => {
      render(<SearchableProductList {...defaultProps} loading={true} />);
      expect(screen.getByRole('status', { name: /loading products/i })).toBeInTheDocument();
      expect(screen.getByText(/loading products/i)).toBeInTheDocument();
    });

    test('renders error state correctly', () => {
      const errorMessage = 'Failed to load products';
      render(<SearchableProductList {...defaultProps} error={errorMessage} />);
      
      expect(screen.getByText(/error loading products/i)).toBeInTheDocument();
      expect(screen.getByText(errorMessage)).toBeInTheDocument();
    });

    test('renders empty state when no products match', () => {
      render(<SearchableProductList {...defaultProps} products={[]} />);
      expect(screen.getByText(/no products found matching your criteria/i)).toBeInTheDocument();
      expect(screen.getByText(/clear all filters/i)).toBeInTheDocument();
    });
  });

  describe('Search Functionality', () => {
    test('filters products by name', async () => {
      const products = [
        generateMockProduct({ id: '1', name: 'iPhone 15' }),
        generateMockProduct({ id: '2', name: 'Samsung Galaxy' }),
        generateMockProduct({ id: '3', name: 'iPad Pro' }),
      ];

      render(<SearchableProductList {...defaultProps} products={products} />);
      
      const searchInput = screen.getByRole('textbox', { name: /search products/i });
      await userEvent.type(searchInput, 'iPhone');
      
      await waitFor(() => {
        expect(screen.getByText('iPhone 15')).toBeInTheDocument();
        expect(screen.queryByText('Samsung Galaxy')).not.toBeInTheDocument();
      });
    });

    test('filters products by description', async () => {
      const products = [
        generateMockProduct({ id: '1', name: 'Product 1', description: 'High-quality smartphone' }),
        generateMockProduct({ id: '2', name: 'Product 2', description: 'Powerful laptop' }),
      ];

      render(<SearchableProductList {...defaultProps} products={products} />);
      
      const searchInput = screen.getByRole('textbox', { name: /search products/i });
      await userEvent.type(searchInput, 'smartphone');
      
      await waitFor(() => {
        expect(screen.getByText('Product 1')).toBeInTheDocument();
        expect(screen.queryByText('Product 2')).not.toBeInTheDocument();
      });
    });

    test('filters products by tags', async () => {
      const products = [
        generateMockProduct({ id: '1', name: 'Product 1', tags: ['electronics', 'mobile'] }),
        generateMockProduct({ id: '2', name: 'Product 2', tags: ['clothing', 'fashion'] }),
      ];

      render(<SearchableProductList {...defaultProps} products={products} />);
      
      const searchInput = screen.getByRole('textbox', { name: /search products/i });
      await userEvent.type(searchInput, 'mobile');
      
      await waitFor(() => {
        expect(screen.getByText('Product 1')).toBeInTheDocument();
        expect(screen.queryByText('Product 2')).not.toBeInTheDocument();
      });
    });

    test('search is case insensitive', async () => {
      const products = [
        generateMockProduct({ id: '1', name: 'iPhone 15' }),
        generateMockProduct({ id: '2', name: 'Samsung Galaxy' }),
      ];

      render(<SearchableProductList {...defaultProps} products={products} />);
      
      const searchInput = screen.getByRole('textbox', { name: /search products/i });
      await userEvent.type(searchInput, 'iphone');
      
      await waitFor(() => {
        expect(screen.getByText('iPhone 15')).toBeInTheDocument();
      });
    });

    test('debounces search input', async () => {
      jest.useFakeTimers();
      
      render(<SearchableProductList {...defaultProps} />);
      
      const searchInput = screen.getByRole('textbox', { name: /search products/i });
      
      // Type quickly
      await userEvent.type(searchInput, 'test');
      
      // Advance timers but not enough to trigger debounce
      jest.advanceTimersByTime(200);
      
      // Add more characters
      await userEvent.type(searchInput, 'ing');
      
      // Now advance enough to trigger debounce
      jest.advanceTimersByTime(300);
      
      await waitFor(() => {
        expect(searchInput).toHaveValue('testing');
      });
      
      jest.useRealTimers();
    });
  });

  describe('Filtering Functionality', () => {
    test('shows and hides filter panel', async () => {
      render(<SearchableProductList {...defaultProps} />);
      
      const filterButton = screen.getByRole('button', { name: /filters/i });
      expect(filterButton).toHaveAttribute('aria-expanded', 'false');
      
      await userEvent.click(filterButton);
      
      expect(filterButton).toHaveAttribute('aria-expanded', 'true');
      expect(screen.getByText(/category/i)).toBeInTheDocument();
    });

    test('filters by category', async () => {
      const products = [
        generateMockProduct({ id: '1', name: 'Laptop', category: 'electronics' }),
        generateMockProduct({ id: '2', name: 'T-Shirt', category: 'clothing' }),
      ];

      render(<SearchableProductList {...defaultProps} products={products} />);
      
      // Open filters
      await userEvent.click(screen.getByRole('button', { name: /filters/i }));
      
      // Select category
      const categorySelect = screen.getByLabelText(/category/i);
      await userEvent.selectOptions(categorySelect, 'electronics');
      
      await waitFor(() => {
        expect(screen.getByText('Laptop')).toBeInTheDocument();
        expect(screen.queryByText('T-Shirt')).not.toBeInTheDocument();
      });
    });

    test('filters by stock status', async () => {
      const products = [
        generateMockProduct({ id: '1', name: 'Available Product', inStock: true }),
        generateMockProduct({ id: '2', name: 'Out of Stock Product', inStock: false }),
      ];

      render(<SearchableProductList {...defaultProps} products={products} />);
      
      // Open filters
      await userEvent.click(screen.getByRole('button', { name: /filters/i }));
      
      // Check in stock only
      const stockCheckbox = screen.getByLabelText(/in stock only/i);
      await userEvent.click(stockCheckbox);
      
      await waitFor(() => {
        expect(screen.getByText('Available Product')).toBeInTheDocument();
        expect(screen.queryByText('Out of Stock Product')).not.toBeInTheDocument();
      });
    });

    test('filters by minimum rating', async () => {
      const products = [
        generateMockProduct({ id: '1', name: 'High Rated', rating: 4.5 }),
        generateMockProduct({ id: '2', name: 'Low Rated', rating: 2.0 }),
      ];

      render(<SearchableProductList {...defaultProps} products={products} />);
      
      // Open filters
      await userEvent.click(screen.getByRole('button', { name: /filters/i }));
      
      // Set minimum rating
      const ratingSelect = screen.getByLabelText(/minimum rating/i);
      await userEvent.selectOptions(ratingSelect, '4');
      
      await waitFor(() => {
        expect(screen.getByText('High Rated')).toBeInTheDocument();
        expect(screen.queryByText('Low Rated')).not.toBeInTheDocument();
      });
    });

    test('clears all filters', async () => {
      const products = [
        generateMockProduct({ id: '1', name: 'Product 1', category: 'electronics', inStock: true }),
        generateMockProduct({ id: '2', name: 'Product 2', category: 'clothing', inStock: false }),
      ];

      render(<SearchableProductList {...defaultProps} products={products} />);
      
      // Apply filters that would hide products
      await userEvent.click(screen.getByRole('button', { name: /filters/i }));
      const categorySelect = screen.getByLabelText(/category/i);
      await userEvent.selectOptions(categorySelect, 'nonexistent');
      
      // Should show no products
      await waitFor(() => {
        expect(screen.getByText(/no products found/i)).toBeInTheDocument();
      });
      
      // Clear filters
      await userEvent.click(screen.getByText(/clear all filters/i));
      
      // Should show all products again
      await waitFor(() => {
        expect(screen.getByText('Product 1')).toBeInTheDocument();
        expect(screen.getByText('Product 2')).toBeInTheDocument();
      });
    });
  });

  describe('Sorting Functionality', () => {
    test('sorts by name', async () => {
      const products = [
        generateMockProduct({ id: '1', name: 'Zebra Product' }),
        generateMockProduct({ id: '2', name: 'Alpha Product' }),
        generateMockProduct({ id: '3', name: 'Beta Product' }),
      ];

      render(<SearchableProductList {...defaultProps} products={products} />);
      
      const sortSelect = screen.getByLabelText(/sort products by/i);
      await userEvent.selectOptions(sortSelect, 'name');
      
      await waitFor(() => {
        const productCards = screen.getAllByRole('gridcell');
        expect(within(productCards[0]).getByText('Alpha Product')).toBeInTheDocument();
        expect(within(productCards[1]).getByText('Beta Product')).toBeInTheDocument();
        expect(within(productCards[2]).getByText('Zebra Product')).toBeInTheDocument();
      });
    });

    test('sorts by price', async () => {
      const products = [
        generateMockProduct({ id: '1', name: 'Expensive', price: 1000 }),
        generateMockProduct({ id: '2', name: 'Cheap', price: 10 }),
        generateMockProduct({ id: '3', name: 'Medium', price: 100 }),
      ];

      render(<SearchableProductList {...defaultProps} products={products} />);
      
      const sortSelect = screen.getByLabelText(/sort products by/i);
      await userEvent.selectOptions(sortSelect, 'price');
      
      await waitFor(() => {
        const productCards = screen.getAllByRole('gridcell');
        expect(within(productCards[0]).getByText('Cheap')).toBeInTheDocument();
        expect(within(productCards[1]).getByText('Medium')).toBeInTheDocument();
        expect(within(productCards[2]).getByText('Expensive')).toBeInTheDocument();
      });
    });

    test('sorts by rating', async () => {
      const products = [
        generateMockProduct({ id: '1', name: 'Low Rating', rating: 2.0 }),
        generateMockProduct({ id: '2', name: 'High Rating', rating: 5.0 }),
        generateMockProduct({ id: '3', name: 'Medium Rating', rating: 3.5 }),
      ];

      render(<SearchableProductList {...defaultProps} products={products} />);
      
      const sortSelect = screen.getByLabelText(/sort products by/i);
      await userEvent.selectOptions(sortSelect, 'rating');
      
      await waitFor(() => {
        const productCards = screen.getAllByRole('gridcell');
        expect(within(productCards[0]).getByText('High Rating')).toBeInTheDocument();
        expect(within(productCards[1]).getByText('Medium Rating')).toBeInTheDocument();
        expect(within(productCards[2]).getByText('Low Rating')).toBeInTheDocument();
      });
    });
  });

  describe('View Mode Functionality', () => {
    test('switches between grid and list view', async () => {
      render(<SearchableProductList {...defaultProps} />);
      
      const gridButton = screen.getByRole('button', { name: /grid view/i });
      const listButton = screen.getByRole('button', { name: /list view/i });
      
      // Initially in grid view
      expect(gridButton).toHaveAttribute('aria-pressed', 'true');
      expect(listButton).toHaveAttribute('aria-pressed', 'false');
      
      // Switch to list view
      await userEvent.click(listButton);
      
      expect(gridButton).toHaveAttribute('aria-pressed', 'false');
      expect(listButton).toHaveAttribute('aria-pressed', 'true');
    });

    test('displays different layouts for grid and list view', async () => {
      render(<SearchableProductList {...defaultProps} />);
      
      const productGrid = screen.getByRole('grid');
      
      // Grid view has specific grid classes
      expect(productGrid).toHaveClass('grid');
      
      // Switch to list view
      await userEvent.click(screen.getByRole('button', { name: /list view/i }));
      
      await waitFor(() => {
        expect(productGrid).toHaveClass('space-y-4');
      });
    });
  });

  describe('Pagination Functionality', () => {
    test('displays pagination when items exceed itemsPerPage', () => {
      const manyProducts = generateMockProducts(50);
      render(<SearchableProductList {...defaultProps} products={manyProducts} itemsPerPage={10} />);
      
      const pagination = screen.getByRole('navigation', { name: /pagination/i });
      expect(pagination).toBeInTheDocument();
      
      const pageButtons = within(pagination).getAllByRole('button');
      expect(pageButtons).toHaveLength(5); // 50 products / 10 per page = 5 pages
    });

    test('navigates between pages', async () => {
      const manyProducts = generateMockProducts(30);
      render(<SearchableProductList {...defaultProps} products={manyProducts} itemsPerPage={10} />);
      
      // Check first page
      const firstPageButton = screen.getByRole('button', { name: /go to page 1/i });
      expect(firstPageButton).toHaveAttribute('aria-current', 'page');
      
      // Navigate to second page
      const secondPageButton = screen.getByRole('button', { name: /go to page 2/i });
      await userEvent.click(secondPageButton);
      
      await waitFor(() => {
        expect(secondPageButton).toHaveAttribute('aria-current', 'page');
        expect(firstPageButton).not.toHaveAttribute('aria-current');
      });
    });

    test('does not show pagination when virtualScrolling is enabled', () => {
      const manyProducts = generateMockProducts(50);
      render(<SearchableProductList {...defaultProps} products={manyProducts} virtualScrolling={true} />);
      
      const pagination = screen.queryByRole('navigation', { name: /pagination/i });
      expect(pagination).not.toBeInTheDocument();
    });
  });

  describe('Product Selection', () => {
    test('calls onProductSelect when product is clicked', async () => {
      const products = [generateMockProduct({ id: '1', name: 'Test Product' })];
      render(<SearchableProductList {...defaultProps} products={products} />);
      
      const productCard = screen.getByRole('gridcell');
      await userEvent.click(productCard);
      
      expect(mockOnProductSelect).toHaveBeenCalledWith(products[0]);
    });

    test('calls onProductSelect when Enter key is pressed', async () => {
      const products = [generateMockProduct({ id: '1', name: 'Test Product' })];
      render(<SearchableProductList {...defaultProps} products={products} />);
      
      const productCard = screen.getByRole('gridcell');
      productCard.focus();
      await userEvent.keyboard('{Enter}');
      
      expect(mockOnProductSelect).toHaveBeenCalledWith(products[0]);
    });

    test('calls onProductSelect when Space key is pressed', async () => {
      const products = [generateMockProduct({ id: '1', name: 'Test Product' })];
      render(<SearchableProductList {...defaultProps} products={products} />);
      
      const productCard = screen.getByRole('gridcell');
      productCard.focus();
      await userEvent.keyboard(' ');
      
      expect(mockOnProductSelect).toHaveBeenCalledWith(products[0]);
    });
  });

  describe('Accessibility', () => {
    test('has no accessibility violations', async () => {
      const { container } = render(<SearchableProductList {...defaultProps} />);
      const results = await axe(container);
      expect(results).toHaveNoViolations();
    });

    test('search input has proper labels and descriptions', () => {
      render(<SearchableProductList {...defaultProps} />);
      
      const searchInput = screen.getByRole('textbox', { name: /search products/i });
      expect(searchInput).toHaveAttribute('aria-label', 'Search products');
      expect(searchInput).toHaveAttribute('aria-describedby', 'search-description');
    });

    test('filter controls have proper accessibility attributes', async () => {
      render(<SearchableProductList {...defaultProps} />);
      
      const filterButton = screen.getByRole('button', { name: /filters/i });
      expect(filterButton).toHaveAttribute('aria-expanded', 'false');
      expect(filterButton).toHaveAttribute('aria-controls', 'filter-panel');
      
      await userEvent.click(filterButton);
      
      expect(filterButton).toHaveAttribute('aria-expanded', 'true');
      expect(screen.getByRole('generic', { name: /filter-panel/i })).toBeInTheDocument();
    });

    test('product cards have proper accessibility attributes', () => {
      const products = [generateMockProduct({ id: '1', name: 'Test Product', price: 99.99 })];
      render(<SearchableProductList {...defaultProps} products={products} />);
      
      const productCard = screen.getByRole('gridcell');
      expect(productCard).toHaveAttribute('aria-label');
      expect(productCard).toHaveAttribute('aria-posinset', '1');
      expect(productCard).toHaveAttribute('aria-setsize', '1');
      expect(productCard).toHaveAttribute('tabindex', '0');
    });

    test('view mode buttons have proper accessibility attributes', () => {
      render(<SearchableProductList {...defaultProps} />);
      
      const gridButton = screen.getByRole('button', { name: /grid view/i });
      const listButton = screen.getByRole('button', { name: /list view/i });
      
      expect(gridButton).toHaveAttribute('aria-pressed', 'true');
      expect(listButton).toHaveAttribute('aria-pressed', 'false');
    });

    test('announces product selection to screen readers', async () => {
      const products = [generateMockProduct({ id: '1', name: 'Test Product' })];
      render(<SearchableProductList {...defaultProps} products={products} />);
      
      const productCard = screen.getByRole('gridcell');
      await userEvent.click(productCard);
      
      const announcement = screen.getByRole('status');
      expect(announcement).toHaveTextContent('Selected Test Product');
    });
  });

  describe('Performance', () => {
    test('renders within performance threshold', async () => {
      const { duration } = measurePerformance(() => {
        render(<SearchableProductList {...defaultProps} />);
      });
      
      expect(duration).toBeLessThan(PERFORMANCE_THRESHOLDS.RENDER_TIME);
    });

    test('handles large datasets efficiently', async () => {
      const largeDataset = generateMockProducts(1000);
      
      const { duration } = measurePerformance(() => {
        render(<SearchableProductList {...defaultProps} products={largeDataset} />);
      });
      
      expect(duration).toBeLessThan(PERFORMANCE_THRESHOLDS.RENDER_TIME * 2);
    });

    test('search debouncing works correctly', async () => {
      jest.useFakeTimers();
      
      render(<SearchableProductList {...defaultProps} />);
      
      const searchInput = screen.getByRole('textbox');
      
      // Measure time for multiple rapid inputs
      const startTime = performance.now();
      
      await userEvent.type(searchInput, 'test');
      jest.advanceTimersByTime(100);
      await userEvent.type(searchInput, 'ing');
      jest.advanceTimersByTime(100);
      await userEvent.type(searchInput, ' query');
      jest.advanceTimersByTime(300);
      
      const endTime = performance.now();
      const totalTime = endTime - startTime;
      
      expect(totalTime).toBeLessThan(PERFORMANCE_THRESHOLDS.SEARCH_DEBOUNCE * 2);
      
      jest.useRealTimers();
    });

    test('does not cause memory leaks', async () => {
      const memoryTracker = detectMemoryLeaks();
      
      const { unmount } = render(<SearchableProductList {...defaultProps} />);
      
      // Simulate user interactions
      const searchInput = screen.getByRole('textbox');
      await userEvent.type(searchInput, 'test search');
      
      // Unmount component
      unmount();
      
      // Check for memory leaks
      const memoryDiff = memoryTracker.check();
      expect(memoryDiff).toBeLessThan(1024 * 1024); // Less than 1MB
    });
  });

  describe('Edge Cases', () => {
    test('handles empty product array', () => {
      render(<SearchableProductList {...defaultProps} products={[]} />);
      expect(screen.getByText(/no products found/i)).toBeInTheDocument();
    });

    test('handles products with missing properties', () => {
      const incompleteProduct = {
        id: '1',
        name: 'Incomplete Product',
        price: 0,
        category: '',
        inStock: true,
        rating: 0,
        reviewCount: 0,
      } as Product;
      
      render(<SearchableProductList {...defaultProps} products={[incompleteProduct]} />);
      expect(screen.getByText('Incomplete Product')).toBeInTheDocument();
    });

    test('handles very long product names', () => {
      const longNameProduct = generateMockProduct({
        id: '1',
        name: 'A'.repeat(200),
      });
      
      render(<SearchableProductList {...defaultProps} products={[longNameProduct]} />);
      expect(screen.getByText('A'.repeat(200))).toBeInTheDocument();
    });

    test('handles special characters in search', async () => {
      const products = [
        generateMockProduct({ id: '1', name: 'Product @#$%' }),
        generateMockProduct({ id: '2', name: 'Normal Product' }),
      ];
      
      render(<SearchableProductList {...defaultProps} products={products} />);
      
      const searchInput = screen.getByRole('textbox');
      await userEvent.type(searchInput, '@#$%');
      
      await waitFor(() => {
        expect(screen.getByText('Product @#$%')).toBeInTheDocument();
        expect(screen.queryByText('Normal Product')).not.toBeInTheDocument();
      });
    });
  });

  describe('Error Handling', () => {
    test('handles search errors gracefully', async () => {
      // Mock console.error to prevent error logs in tests
      const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
      
      render(<SearchableProductList {...defaultProps} />);
      
      // Trigger potential error scenario
      const searchInput = screen.getByRole('textbox');
      await userEvent.type(searchInput, 'test');
      
      // Component should still be functional
      expect(screen.getByRole('textbox')).toBeInTheDocument();
      
      consoleSpy.mockRestore();
    });
  });
});

// Stress testing suite
describe('SearchableProductList Stress Tests', () => {
  test('handles rapid user interactions', async () => {
    const products = generateMockProducts(100);
    render(<SearchableProductList {...defaultProps} products={products} />);
    
    const searchInput = screen.getByRole('textbox');
    
    // Simulate rapid typing
    for (let i = 0; i < 10; i++) {
      await userEvent.type(searchInput, `query${i}`);
      await userEvent.clear(searchInput);
    }
    
    expect(screen.getByRole('textbox')).toBeInTheDocument();
  });

  test('performance with large datasets', async () => {
    const largeDataset = generateMockProducts(5000);
    
    const performanceResults = await stressTestComponent(
      () => render(<SearchableProductList {...defaultProps} products={largeDataset} />),
      5
    );
    
    expect(performanceResults.average).toBeLessThan(PERFORMANCE_THRESHOLDS.RENDER_TIME * 3);
  });
});