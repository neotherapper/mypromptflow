/**
 * AI-Generated Integration Test Suite for SearchableProductList Component
 * 
 * Integration Testing Focus:
 * - Complete user workflows
 * - Component interaction patterns
 * - State management integration
 * - Real-world usage scenarios
 * - Error boundary integration
 */

import React, { useState } from 'react';
import { render, screen, fireEvent, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { jest } from '@jest/globals';

import SearchableProductList, { Product } from '../SearchableProductList';
import { generateMockProduct, generateMockProducts } from '../../../test/setup';

// Test wrapper component for integration testing
const SearchableProductListWrapper: React.FC<{
  initialProducts?: Product[];
  onSelectionChange?: (product: Product) => void;
}> = ({ initialProducts = generateMockProducts(50), onSelectionChange }) => {
  const [products] = useState(initialProducts);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | undefined>();

  const handleProductSelect = (product: Product) => {
    setSelectedProduct(product);
    onSelectionChange?.(product);
  };

  const simulateError = () => setError('Failed to load products');
  const simulateLoading = () => setLoading(true);
  const clearError = () => setError(undefined);
  const clearLoading = () => setLoading(false);

  return (
    <div>
      <div data-testid="controls">
        <button onClick={simulateError}>Simulate Error</button>
        <button onClick={simulateLoading}>Simulate Loading</button>
        <button onClick={clearError}>Clear Error</button>
        <button onClick={clearLoading}>Clear Loading</button>
      </div>
      
      {selectedProduct && (
        <div data-testid="selected-product">
          <h3>Selected Product: {selectedProduct.name}</h3>
          <p>Price: ${selectedProduct.price}</p>
        </div>
      )}
      
      <SearchableProductList
        products={products}
        onProductSelect={handleProductSelect}
        loading={loading}
        error={error}
      />
    </div>
  );
};

describe('SearchableProductList Integration Tests', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Complete User Workflows', () => {
    test('product discovery workflow', async () => {
      const mockOnSelectionChange = jest.fn();
      render(<SearchableProductListWrapper onSelectionChange={mockOnSelectionChange} />);

      // 1. User starts with browsing all products
      expect(screen.getByText(/50 products found/i)).toBeInTheDocument();

      // 2. User searches for specific product
      const searchInput = screen.getByRole('textbox', { name: /search products/i });
      await userEvent.type(searchInput, 'Product 1');

      await waitFor(() => {
        expect(screen.getByText(/products found/i)).toBeInTheDocument();
      });

      // 3. User applies filters to narrow down results
      await userEvent.click(screen.getByRole('button', { name: /filters/i }));
      
      const categorySelect = screen.getByLabelText(/category/i);
      await userEvent.selectOptions(categorySelect, 'electronics');

      // 4. User sorts results by price
      const sortSelect = screen.getByLabelText(/sort products by/i);
      await userEvent.selectOptions(sortSelect, 'price');

      // 5. User selects a product
      const productCards = screen.getAllByRole('gridcell');
      if (productCards.length > 0) {
        await userEvent.click(productCards[0]);
        
        expect(mockOnSelectionChange).toHaveBeenCalled();
        expect(screen.getByTestId('selected-product')).toBeInTheDocument();
      }
    });

    test('comparison shopping workflow', async () => {
      const products = [
        generateMockProduct({ id: '1', name: 'iPhone 15', price: 999, category: 'electronics', rating: 4.5 }),
        generateMockProduct({ id: '2', name: 'iPhone 14', price: 799, category: 'electronics', rating: 4.3 }),
        generateMockProduct({ id: '3', name: 'Samsung Galaxy', price: 899, category: 'electronics', rating: 4.4 }),
      ];

      render(<SearchableProductListWrapper initialProducts={products} />);

      // 1. User searches for phones
      const searchInput = screen.getByRole('textbox', { name: /search products/i });
      await userEvent.type(searchInput, 'phone');

      // 2. User sorts by price to compare
      const sortSelect = screen.getByLabelText(/sort products by/i);
      await userEvent.selectOptions(sortSelect, 'price');

      await waitFor(() => {
        const productCards = screen.getAllByRole('gridcell');
        expect(productCards).toHaveLength(2); // iPhone 14 and iPhone 15
        
        // Verify price sorting
        const firstProduct = within(productCards[0]).getByText(/\$799/);
        expect(firstProduct).toBeInTheDocument();
      });

      // 3. User sorts by rating
      await userEvent.selectOptions(sortSelect, 'rating');

      await waitFor(() => {
        const productCards = screen.getAllByRole('gridcell');
        // Verify rating sorting (highest first)
        const firstProductRating = within(productCards[0]).getByText(/4\.5/);
        expect(firstProductRating).toBeInTheDocument();
      });
    });

    test('filter refinement workflow', async () => {
      const products = [
        generateMockProduct({ id: '1', name: 'Laptop', price: 1200, category: 'electronics', inStock: true, rating: 4.5 }),
        generateMockProduct({ id: '2', name: 'Tablet', price: 600, category: 'electronics', inStock: false, rating: 4.0 }),
        generateMockProduct({ id: '3', name: 'T-Shirt', price: 25, category: 'clothing', inStock: true, rating: 3.5 }),
        generateMockProduct({ id: '4', name: 'Jeans', price: 80, category: 'clothing', inStock: true, rating: 4.2 }),
      ];

      render(<SearchableProductListWrapper initialProducts={products} />);

      // 1. Start with all products
      expect(screen.getByText(/4 products found/i)).toBeInTheDocument();

      // 2. Filter by category
      await userEvent.click(screen.getByRole('button', { name: /filters/i }));
      const categorySelect = screen.getByLabelText(/category/i);
      await userEvent.selectOptions(categorySelect, 'electronics');

      await waitFor(() => {
        expect(screen.getByText(/2 products found/i)).toBeInTheDocument();
      });

      // 3. Add stock filter
      const stockCheckbox = screen.getByLabelText(/in stock only/i);
      await userEvent.click(stockCheckbox);

      await waitFor(() => {
        expect(screen.getByText(/1 product found/i)).toBeInTheDocument();
        expect(screen.getByText('Laptop')).toBeInTheDocument();
      });

      // 4. Add rating filter
      const ratingSelect = screen.getByLabelText(/minimum rating/i);
      await userEvent.selectOptions(ratingSelect, '4');

      await waitFor(() => {
        expect(screen.getByText(/1 product found/i)).toBeInTheDocument();
        expect(screen.getByText('Laptop')).toBeInTheDocument();
      });

      // 5. Remove filters to see all products again
      await userEvent.selectOptions(categorySelect, 'all');
      await userEvent.click(stockCheckbox); // uncheck
      await userEvent.selectOptions(ratingSelect, '0');

      await waitFor(() => {
        expect(screen.getByText(/4 products found/i)).toBeInTheDocument();
      });
    });

    test('pagination navigation workflow', async () => {
      const manyProducts = generateMockProducts(75);
      render(<SearchableProductListWrapper initialProducts={manyProducts} />);

      // 1. Verify initial state
      expect(screen.getByText(/75 products found/i)).toBeInTheDocument();
      
      const pagination = screen.getByRole('navigation', { name: /pagination/i });
      expect(pagination).toBeInTheDocument();

      // 2. Navigate to second page
      const page2Button = screen.getByRole('button', { name: /go to page 2/i });
      await userEvent.click(page2Button);

      expect(page2Button).toHaveAttribute('aria-current', 'page');

      // 3. Navigate to last page
      const page4Button = screen.getByRole('button', { name: /go to page 4/i });
      await userEvent.click(page4Button);

      expect(page4Button).toHaveAttribute('aria-current', 'page');

      // 4. Search to reduce results and verify pagination updates
      const searchInput = screen.getByRole('textbox', { name: /search products/i });
      await userEvent.type(searchInput, 'Product 1'); // Should match Product 1, 10, 11, etc.

      await waitFor(() => {
        // Pagination should update based on filtered results
        const updatedPagination = screen.queryByRole('navigation', { name: /pagination/i });
        // If results fit on one page, pagination should be hidden
        if (screen.getByText(/products found/i).textContent?.includes('20') === false) {
          expect(updatedPagination).not.toBeInTheDocument();
        }
      });
    });
  });

  describe('View Mode Integration', () => {
    test('switching between grid and list views', async () => {
      render(<SearchableProductListWrapper />);

      const productGrid = screen.getByRole('grid', { name: /product results/i });
      const gridButton = screen.getByRole('button', { name: /grid view/i });
      const listButton = screen.getByRole('button', { name: /list view/i });

      // 1. Initially in grid view
      expect(gridButton).toHaveAttribute('aria-pressed', 'true');
      expect(productGrid).toHaveClass('grid');

      // 2. Switch to list view
      await userEvent.click(listButton);

      expect(listButton).toHaveAttribute('aria-pressed', 'true');
      expect(gridButton).toHaveAttribute('aria-pressed', 'false');
      expect(productGrid).toHaveClass('space-y-4');

      // 3. Verify product cards adapt to list view
      const productCards = screen.getAllByRole('gridcell');
      productCards.forEach(card => {
        // In list view, cards should have different layout
        expect(card).toHaveClass('p-4');
      });

      // 4. Switch back to grid view
      await userEvent.click(gridButton);

      expect(gridButton).toHaveAttribute('aria-pressed', 'true');
      expect(listButton).toHaveAttribute('aria-pressed', 'false');
      expect(productGrid).toHaveClass('grid');
    });

    test('view mode persistence during interactions', async () => {
      render(<SearchableProductListWrapper />);

      const listButton = screen.getByRole('button', { name: /list view/i });
      
      // 1. Switch to list view
      await userEvent.click(listButton);
      expect(listButton).toHaveAttribute('aria-pressed', 'true');

      // 2. Perform search - view mode should persist
      const searchInput = screen.getByRole('textbox', { name: /search products/i });
      await userEvent.type(searchInput, 'Product');

      expect(listButton).toHaveAttribute('aria-pressed', 'true');

      // 3. Apply filters - view mode should persist
      await userEvent.click(screen.getByRole('button', { name: /filters/i }));
      const categorySelect = screen.getByLabelText(/category/i);
      await userEvent.selectOptions(categorySelect, 'electronics');

      expect(listButton).toHaveAttribute('aria-pressed', 'true');

      // 4. Change sorting - view mode should persist
      const sortSelect = screen.getByLabelText(/sort products by/i);
      await userEvent.selectOptions(sortSelect, 'price');

      expect(listButton).toHaveAttribute('aria-pressed', 'true');
    });
  });

  describe('Error Handling Integration', () => {
    test('error state recovery workflow', async () => {
      render(<SearchableProductListWrapper />);

      // 1. Simulate error
      await userEvent.click(screen.getByText('Simulate Error'));

      expect(screen.getByText(/error loading products/i)).toBeInTheDocument();
      expect(screen.getByText(/failed to load products/i)).toBeInTheDocument();

      // 2. Clear error and verify normal operation
      await userEvent.click(screen.getByText('Clear Error'));

      expect(screen.queryByText(/error loading products/i)).not.toBeInTheDocument();
      expect(screen.getByRole('textbox', { name: /search products/i })).toBeInTheDocument();

      // 3. Verify functionality works after error recovery
      const searchInput = screen.getByRole('textbox', { name: /search products/i });
      await userEvent.type(searchInput, 'test');

      expect(searchInput).toHaveValue('test');
    });

    test('loading state workflow', async () => {
      render(<SearchableProductListWrapper />);

      // 1. Simulate loading
      await userEvent.click(screen.getByText('Simulate Loading'));

      expect(screen.getByRole('status', { name: /loading products/i })).toBeInTheDocument();
      expect(screen.queryByRole('grid')).not.toBeInTheDocument();

      // 2. Clear loading state
      await userEvent.click(screen.getByText('Clear Loading'));

      expect(screen.queryByRole('status')).not.toBeInTheDocument();
      expect(screen.getByRole('grid', { name: /product results/i })).toBeInTheDocument();
    });
  });

  describe('Complex Search Scenarios', () => {
    test('multi-criteria search workflow', async () => {
      const products = [
        generateMockProduct({ 
          id: '1', 
          name: 'Gaming Laptop Pro', 
          description: 'High-performance gaming laptop with RTX graphics',
          category: 'electronics',
          price: 1500,
          tags: ['gaming', 'laptop', 'rtx', 'performance'],
          inStock: true,
          rating: 4.8
        }),
        generateMockProduct({ 
          id: '2', 
          name: 'Business Laptop', 
          description: 'Professional laptop for business use',
          category: 'electronics',
          price: 800,
          tags: ['business', 'laptop', 'professional'],
          inStock: true,
          rating: 4.2
        }),
        generateMockProduct({ 
          id: '3', 
          name: 'Gaming Mouse', 
          description: 'RGB gaming mouse with high DPI',
          category: 'electronics',
          price: 80,
          tags: ['gaming', 'mouse', 'rgb'],
          inStock: false,
          rating: 4.5
        }),
      ];

      render(<SearchableProductListWrapper initialProducts={products} />);

      // 1. Search by tag
      const searchInput = screen.getByRole('textbox', { name: /search products/i });
      await userEvent.type(searchInput, 'gaming');

      await waitFor(() => {
        expect(screen.getByText(/2 products found/i)).toBeInTheDocument();
        expect(screen.getByText('Gaming Laptop Pro')).toBeInTheDocument();
        expect(screen.getByText('Gaming Mouse')).toBeInTheDocument();
      });

      // 2. Add stock filter
      await userEvent.click(screen.getByRole('button', { name: /filters/i }));
      const stockCheckbox = screen.getByLabelText(/in stock only/i);
      await userEvent.click(stockCheckbox);

      await waitFor(() => {
        expect(screen.getByText(/1 product found/i)).toBeInTheDocument();
        expect(screen.getByText('Gaming Laptop Pro')).toBeInTheDocument();
        expect(screen.queryByText('Gaming Mouse')).not.toBeInTheDocument();
      });

      // 3. Search by description keyword
      await userEvent.clear(searchInput);
      await userEvent.type(searchInput, 'RTX');

      await waitFor(() => {
        expect(screen.getByText(/1 product found/i)).toBeInTheDocument();
        expect(screen.getByText('Gaming Laptop Pro')).toBeInTheDocument();
      });
    });

    test('relevance scoring integration', async () => {
      const products = [
        generateMockProduct({ 
          id: '1', 
          name: 'iPhone 15 Pro Max', 
          description: 'Latest iPhone model',
          rating: 4.8,
          inStock: true
        }),
        generateMockProduct({ 
          id: '2', 
          name: 'iPhone Case', 
          description: 'Protective case for iPhone',
          rating: 4.0,
          inStock: true
        }),
        generateMockProduct({ 
          id: '3', 
          name: 'Phone Charger', 
          description: 'Universal phone charger for iPhone and Android',
          rating: 3.5,
          inStock: false
        }),
      ];

      render(<SearchableProductListWrapper initialProducts={products} />);

      const searchInput = screen.getByRole('textbox', { name: /search products/i });
      await userEvent.type(searchInput, 'iPhone');

      const sortSelect = screen.getByLabelText(/sort products by/i);
      await userEvent.selectOptions(sortSelect, 'relevance');

      await waitFor(() => {
        const productCards = screen.getAllByRole('gridcell');
        
        // iPhone 15 Pro Max should be first (exact name match + high rating + in stock)
        expect(within(productCards[0]).getByText('iPhone 15 Pro Max')).toBeInTheDocument();
        
        // iPhone Case should be second (name match + good rating + in stock)
        expect(within(productCards[1]).getByText('iPhone Case')).toBeInTheDocument();
        
        // Phone Charger should be last (description match only + out of stock)
        expect(within(productCards[2]).getByText('Phone Charger')).toBeInTheDocument();
      });
    });
  });

  describe('Performance Integration', () => {
    test('large dataset handling', async () => {
      const largeDataset = generateMockProducts(1000);
      render(<SearchableProductListWrapper initialProducts={largeDataset} />);

      // 1. Verify initial render with pagination
      expect(screen.getByText(/1000 products found/i)).toBeInTheDocument();
      expect(screen.getByRole('navigation', { name: /pagination/i })).toBeInTheDocument();

      // 2. Search should work efficiently
      const searchInput = screen.getByRole('textbox', { name: /search products/i });
      await userEvent.type(searchInput, 'Product 1');

      await waitFor(() => {
        // Should find Product 1, 10, 100, 101, etc.
        const resultsText = screen.getByText(/products found/i).textContent;
        expect(resultsText).toMatch(/\d+ products found/);
      });

      // 3. Filtering should work efficiently
      await userEvent.click(screen.getByRole('button', { name: /filters/i }));
      const categorySelect = screen.getByLabelText(/category/i);
      await userEvent.selectOptions(categorySelect, 'electronics');

      await waitFor(() => {
        expect(screen.getByText(/products found/i)).toBeInTheDocument();
      });
    });

    test('rapid user interaction handling', async () => {
      render(<SearchableProductListWrapper />);

      const searchInput = screen.getByRole('textbox', { name: /search products/i });

      // Simulate rapid typing
      const rapidSearches = ['a', 'ab', 'abc', 'abcd', 'abcde'];
      
      for (const search of rapidSearches) {
        await userEvent.clear(searchInput);
        await userEvent.type(searchInput, search);
      }

      // Component should remain stable
      expect(searchInput).toBeInTheDocument();
      expect(searchInput).toHaveValue('abcde');
    });
  });

  describe('Accessibility Integration', () => {
    test('complete keyboard navigation workflow', async () => {
      render(<SearchableProductListWrapper />);

      // Tab through all interactive elements
      await userEvent.tab(); // Search input
      expect(screen.getByRole('textbox')).toHaveFocus();

      await userEvent.tab(); // Filter button
      expect(screen.getByRole('button', { name: /filters/i })).toHaveFocus();

      await userEvent.tab(); // Sort select
      expect(screen.getByLabelText(/sort products by/i)).toHaveFocus();

      await userEvent.tab(); // Grid view button
      expect(screen.getByRole('button', { name: /grid view/i })).toHaveFocus();

      await userEvent.tab(); // List view button
      expect(screen.getByRole('button', { name: /list view/i })).toHaveFocus();

      await userEvent.tab(); // First product
      expect(screen.getAllByRole('gridcell')[0]).toHaveFocus();
    });

    test('screen reader announcements workflow', async () => {
      render(<SearchableProductListWrapper />);

      // Search should update results count
      const searchInput = screen.getByRole('textbox', { name: /search products/i });
      await userEvent.type(searchInput, 'Product 1');

      await waitFor(() => {
        expect(screen.getByText(/products found/i)).toBeInTheDocument();
      });

      // Product selection should be announced
      const productCards = screen.getAllByRole('gridcell');
      if (productCards.length > 0) {
        await userEvent.click(productCards[0]);
        
        const announcement = screen.getByRole('status');
        expect(announcement).toHaveTextContent(/selected/i);
      }
    });
  });
});

// Integration test helpers
export const integrationTestHelpers = {
  performCompleteUserWorkflow: async (searchTerm: string, category: string) => {
    // Helper function for complete user workflow testing
    const searchInput = screen.getByRole('textbox', { name: /search products/i });
    await userEvent.type(searchInput, searchTerm);

    await userEvent.click(screen.getByRole('button', { name: /filters/i }));
    const categorySelect = screen.getByLabelText(/category/i);
    await userEvent.selectOptions(categorySelect, category);

    const productCards = screen.getAllByRole('gridcell');
    if (productCards.length > 0) {
      await userEvent.click(productCards[0]);
    }

    return productCards.length;
  },

  simulateNetworkConditions: async (delay: number = 1000) => {
    // Helper to simulate slow network conditions
    await new Promise(resolve => setTimeout(resolve, delay));
  },

  verifyAccessibilityCompliance: (container: HTMLElement) => {
    // Helper to verify accessibility compliance
    const interactiveElements = container.querySelectorAll('button, input, select, [role="gridcell"]');
    
    interactiveElements.forEach(element => {
      expect(element).toHaveAttribute('tabindex');
    });
  },
};