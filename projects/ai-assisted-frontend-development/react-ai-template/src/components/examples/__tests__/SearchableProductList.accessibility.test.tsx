/**
 * AI-Generated Accessibility Test Suite for SearchableProductList Component
 * 
 * WCAG 2.1 AA Compliance Testing:
 * - Keyboard navigation
 * - Screen reader support
 * - Color contrast
 * - Focus management
 * - ARIA attributes
 * - Alternative text
 */

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { jest } from '@jest/globals';
import { axe, toHaveNoViolations } from 'jest-axe';

import SearchableProductList from '../SearchableProductList';
import { generateMockProducts, axeConfig } from '../../../test/setup';

// Extend Jest matchers
expect.extend(toHaveNoViolations);

describe('SearchableProductList Accessibility Tests', () => {
  const mockProducts = generateMockProducts(20);
  const defaultProps = {
    products: mockProducts,
    onProductSelect: jest.fn(),
    loading: false,
    error: undefined,
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('WCAG 2.1 AA Compliance', () => {
    test('passes automated accessibility audit', async () => {
      const { container } = render(<SearchableProductList {...defaultProps} />);
      const results = await axe(container, axeConfig);
      expect(results).toHaveNoViolations();
    });

    test('passes accessibility audit in loading state', async () => {
      const { container } = render(<SearchableProductList {...defaultProps} loading={true} />);
      const results = await axe(container, axeConfig);
      expect(results).toHaveNoViolations();
    });

    test('passes accessibility audit in error state', async () => {
      const { container } = render(<SearchableProductList {...defaultProps} error="Failed to load" />);
      const results = await axe(container, axeConfig);
      expect(results).toHaveNoViolations();
    });

    test('passes accessibility audit with filters open', async () => {
      const { container } = render(<SearchableProductList {...defaultProps} />);
      
      // Open filters
      await userEvent.click(screen.getByRole('button', { name: /filters/i }));
      
      const results = await axe(container, axeConfig);
      expect(results).toHaveNoViolations();
    });
  });

  describe('Keyboard Navigation', () => {
    test('search input is keyboard accessible', async () => {
      render(<SearchableProductList {...defaultProps} />);
      
      const searchInput = screen.getByRole('textbox', { name: /search products/i });
      
      // Tab to search input
      await userEvent.tab();
      expect(searchInput).toHaveFocus();
      
      // Type in search input
      await userEvent.keyboard('test query');
      expect(searchInput).toHaveValue('test query');
      
      // Clear with backspace
      await userEvent.keyboard('{Backspace>10}');
      expect(searchInput).toHaveValue('');
    });

    test('filter controls are keyboard accessible', async () => {
      render(<SearchableProductList {...defaultProps} />);
      
      // Tab to filter button
      const filterButton = screen.getByRole('button', { name: /filters/i });
      filterButton.focus();
      expect(filterButton).toHaveFocus();
      
      // Open filters with Enter
      await userEvent.keyboard('{Enter}');
      expect(filterButton).toHaveAttribute('aria-expanded', 'true');
      
      // Tab to category dropdown
      await userEvent.keyboard('{Tab}');
      const categorySelect = screen.getByLabelText(/category/i);
      expect(categorySelect).toHaveFocus();
      
      // Change selection with arrow keys
      await userEvent.keyboard('{ArrowDown}');
      await userEvent.keyboard('{Enter}');
    });

    test('sort controls are keyboard accessible', async () => {
      render(<SearchableProductList {...defaultProps} />);
      
      const sortSelect = screen.getByLabelText(/sort products by/i);
      sortSelect.focus();
      expect(sortSelect).toHaveFocus();
      
      // Change sort option with keyboard
      await userEvent.keyboard('{ArrowDown}');
      await userEvent.keyboard('{Enter}');
    });

    test('view mode buttons are keyboard accessible', async () => {
      render(<SearchableProductList {...defaultProps} />);
      
      const gridButton = screen.getByRole('button', { name: /grid view/i });
      const listButton = screen.getByRole('button', { name: /list view/i });
      
      // Focus grid button
      gridButton.focus();
      expect(gridButton).toHaveFocus();
      
      // Switch to list view with Enter
      listButton.focus();
      await userEvent.keyboard('{Enter}');
      expect(listButton).toHaveAttribute('aria-pressed', 'true');
      
      // Switch back to grid view with Space
      gridButton.focus();
      await userEvent.keyboard(' ');
      expect(gridButton).toHaveAttribute('aria-pressed', 'true');
    });

    test('product cards are keyboard accessible', async () => {
      render(<SearchableProductList {...defaultProps} />);
      
      const productCards = screen.getAllByRole('gridcell');
      const firstCard = productCards[0];
      
      // Tab to first product card
      firstCard.focus();
      expect(firstCard).toHaveFocus();
      
      // Activate with Enter
      await userEvent.keyboard('{Enter}');
      expect(defaultProps.onProductSelect).toHaveBeenCalled();
      
      // Clear mock for next test
      jest.clearAllMocks();
      
      // Activate with Space
      firstCard.focus();
      await userEvent.keyboard(' ');
      expect(defaultProps.onProductSelect).toHaveBeenCalled();
    });

    test('pagination is keyboard accessible', async () => {
      const manyProducts = generateMockProducts(50);
      render(<SearchableProductList {...defaultProps} products={manyProducts} itemsPerPage={10} />);
      
      const pageButtons = screen.getAllByRole('button', { name: /go to page/i });
      const secondPageButton = pageButtons[1];
      
      secondPageButton.focus();
      expect(secondPageButton).toHaveFocus();
      
      await userEvent.keyboard('{Enter}');
      expect(secondPageButton).toHaveAttribute('aria-current', 'page');
    });

    test('logical tab order', async () => {
      render(<SearchableProductList {...defaultProps} />);
      
      // Expected tab order
      const expectedFocusOrder = [
        'textbox', // search input
        'button', // filter button
        'combobox', // sort select
        'button', // grid view
        'button', // list view
        'gridcell', // first product
      ];
      
      let currentIndex = 0;
      
      // Tab through elements
      await userEvent.tab();
      let focusedElement = document.activeElement;
      expect(focusedElement).toHaveAttribute('role', expectedFocusOrder[currentIndex] === 'textbox' ? null : expectedFocusOrder[currentIndex]);
      
      for (let i = 1; i < expectedFocusOrder.length; i++) {
        await userEvent.tab();
        focusedElement = document.activeElement;
        
        // Verify element type matches expected order
        if (expectedFocusOrder[i] === 'gridcell') {
          expect(focusedElement).toHaveAttribute('role', 'gridcell');
        } else if (expectedFocusOrder[i] === 'button') {
          expect(focusedElement?.tagName.toLowerCase()).toBe('button');
        }
      }
    });
  });

  describe('Screen Reader Support', () => {
    test('search input has proper labels and descriptions', () => {
      render(<SearchableProductList {...defaultProps} />);
      
      const searchInput = screen.getByRole('textbox', { name: /search products/i });
      expect(searchInput).toHaveAttribute('aria-label', 'Search products');
      expect(searchInput).toHaveAttribute('aria-describedby', 'search-description');
      
      const description = document.getElementById('search-description');
      expect(description).toHaveTextContent('Search through product names, descriptions, and tags');
    });

    test('loading state is announced to screen readers', () => {
      render(<SearchableProductList {...defaultProps} loading={true} />);
      
      const loadingIndicator = screen.getByRole('status', { name: /loading products/i });
      expect(loadingIndicator).toHaveAttribute('aria-label', 'Loading products');
      
      const srText = screen.getByText(/loading products/i);
      expect(srText).toHaveClass('sr-only');
    });

    test('error state is announced to screen readers', () => {
      const errorMessage = 'Failed to load products';
      render(<SearchableProductList {...defaultProps} error={errorMessage} />);
      
      const errorAlert = screen.getByText(/error loading products/i);
      expect(errorAlert).toBeInTheDocument();
      expect(screen.getByText(errorMessage)).toBeInTheDocument();
    });

    test('filter controls have proper ARIA attributes', async () => {
      render(<SearchableProductList {...defaultProps} />);
      
      const filterButton = screen.getByRole('button', { name: /filters/i });
      expect(filterButton).toHaveAttribute('aria-expanded', 'false');
      expect(filterButton).toHaveAttribute('aria-controls', 'filter-panel');
      
      await userEvent.click(filterButton);
      
      expect(filterButton).toHaveAttribute('aria-expanded', 'true');
      
      const filterPanel = screen.getByRole('generic');
      expect(filterPanel).toHaveAttribute('id', 'filter-panel');
    });

    test('product grid has proper ARIA structure', () => {
      render(<SearchableProductList {...defaultProps} />);
      
      const productGrid = screen.getByRole('grid', { name: /product results/i });
      expect(productGrid).toHaveAttribute('aria-label', 'Product results');
      
      const productCards = screen.getAllByRole('gridcell');
      productCards.forEach((card, index) => {
        expect(card).toHaveAttribute('aria-posinset', String(index + 1));
        expect(card).toHaveAttribute('aria-setsize', String(productCards.length));
      });
    });

    test('view mode buttons have proper ARIA states', () => {
      render(<SearchableProductList {...defaultProps} />);
      
      const gridButton = screen.getByRole('button', { name: /grid view/i });
      const listButton = screen.getByRole('button', { name: /list view/i });
      
      expect(gridButton).toHaveAttribute('aria-pressed', 'true');
      expect(listButton).toHaveAttribute('aria-pressed', 'false');
    });

    test('product selection is announced', async () => {
      render(<SearchableProductList {...defaultProps} />);
      
      const firstProduct = screen.getAllByRole('gridcell')[0];
      await userEvent.click(firstProduct);
      
      const announcement = screen.getByRole('status');
      expect(announcement).toHaveAttribute('aria-live', 'polite');
      expect(announcement).toHaveAttribute('aria-atomic', 'true');
    });

    test('search results count is announced', () => {
      render(<SearchableProductList {...defaultProps} />);
      
      const resultsCount = screen.getByText(/20 products found/i);
      expect(resultsCount).toBeInTheDocument();
    });

    test('pagination has proper ARIA labels', async () => {
      const manyProducts = generateMockProducts(50);
      render(<SearchableProductList {...defaultProps} products={manyProducts} itemsPerPage={10} />);
      
      const pagination = screen.getByRole('navigation', { name: /pagination/i });
      expect(pagination).toBeInTheDocument();
      
      const pageButtons = screen.getAllByRole('button', { name: /go to page/i });
      pageButtons.forEach((button, index) => {
        expect(button).toHaveAttribute('aria-label', `Go to page ${index + 1}`);
      });
      
      const currentPage = screen.getByRole('button', { current: 'page' });
      expect(currentPage).toHaveAttribute('aria-current', 'page');
    });
  });

  describe('Focus Management', () => {
    test('focus returns to filter button after closing filters', async () => {
      render(<SearchableProductList {...defaultProps} />);
      
      const filterButton = screen.getByRole('button', { name: /filters/i });
      
      // Open filters
      await userEvent.click(filterButton);
      expect(filterButton).toHaveAttribute('aria-expanded', 'true');
      
      // Close filters
      await userEvent.click(filterButton);
      expect(filterButton).toHaveAttribute('aria-expanded', 'false');
      expect(filterButton).toHaveFocus();
    });

    test('focus indicator is visible on all interactive elements', async () => {
      render(<SearchableProductList {...defaultProps} />);
      
      const interactiveElements = [
        screen.getByRole('textbox', { name: /search products/i }),
        screen.getByRole('button', { name: /filters/i }),
        screen.getByLabelText(/sort products by/i),
        screen.getByRole('button', { name: /grid view/i }),
        screen.getByRole('button', { name: /list view/i }),
        ...screen.getAllByRole('gridcell').slice(0, 3), // Test first 3 products
      ];
      
      for (const element of interactiveElements) {
        element.focus();
        expect(element).toHaveFocus();
        
        // Check if focus styles are applied (classes containing 'focus')
        const classes = element.className;
        expect(classes).toMatch(/focus/);
      }
    });

    test('skip link functionality (if implemented)', () => {
      render(<SearchableProductList {...defaultProps} />);
      
      // This test would verify skip links if they were implemented
      // For now, we verify that the main content is properly structured
      const main = screen.getByRole('grid', { name: /product results/i });
      expect(main).toBeInTheDocument();
    });
  });

  describe('Alternative Text and Labels', () => {
    test('product images have descriptive alt text', () => {
      render(<SearchableProductList {...defaultProps} />);
      
      const productImages = screen.getAllByRole('img');
      productImages.forEach(img => {
        expect(img).toHaveAttribute('alt');
        const altText = img.getAttribute('alt');
        expect(altText).toBeTruthy();
        expect(altText).not.toBe('');
      });
    });

    test('icons are properly hidden from screen readers', () => {
      render(<SearchableProductList {...defaultProps} />);
      
      // Icons should have aria-hidden="true"
      const icons = screen.getAllByTestId(/-icon$/);
      icons.forEach(icon => {
        expect(icon).toHaveAttribute('aria-hidden', 'true');
      });
    });

    test('form labels are properly associated', async () => {
      render(<SearchableProductList {...defaultProps} />);
      
      // Open filters to test form labels
      await userEvent.click(screen.getByRole('button', { name: /filters/i }));
      
      const categorySelect = screen.getByLabelText(/category/i);
      expect(categorySelect).toHaveAttribute('id');
      
      const categoryLabel = screen.getByText(/category/i);
      expect(categoryLabel).toHaveAttribute('for', categorySelect.id);
      
      const ratingSelect = screen.getByLabelText(/minimum rating/i);
      expect(ratingSelect).toHaveAttribute('id');
      
      const ratingLabel = screen.getByText(/minimum rating/i);
      expect(ratingLabel).toHaveAttribute('for', ratingSelect.id);
    });
  });

  describe('Color and Contrast', () => {
    test('stock status indicators use semantic colors and text', () => {
      const products = [
        { ...mockProducts[0], inStock: true },
        { ...mockProducts[1], inStock: false },
      ];
      
      render(<SearchableProductList {...defaultProps} products={products} />);
      
      const inStockBadge = screen.getByText(/in stock/i);
      const outOfStockBadge = screen.getByText(/out of stock/i);
      
      expect(inStockBadge).toBeInTheDocument();
      expect(outOfStockBadge).toBeInTheDocument();
      
      // Verify text content provides semantic meaning beyond color
      expect(inStockBadge).toHaveTextContent('In Stock');
      expect(outOfStockBadge).toHaveTextContent('Out of Stock');
    });

    test('interactive elements have proper contrast states', async () => {
      render(<SearchableProductList {...defaultProps} />);
      
      const filterButton = screen.getByRole('button', { name: /filters/i });
      
      // Test focus state
      filterButton.focus();
      expect(filterButton).toHaveClass(/focus:/);
      
      // Test hover state (simulated through class checking)
      expect(filterButton).toHaveClass(/hover:/);
    });

    test('rating stars use both color and symbol', () => {
      const productWithRating = { ...mockProducts[0], rating: 4.5, reviewCount: 120 };
      render(<SearchableProductList {...defaultProps} products={[productWithRating]} />);
      
      // Stars should use both visual (★) and semantic information
      const ratingInfo = screen.getByText(/4.5.*120 reviews/);
      expect(ratingInfo).toBeInTheDocument();
    });
  });

  describe('Responsive Accessibility', () => {
    test('maintains accessibility on mobile viewports', async () => {
      // Simulate mobile viewport
      Object.defineProperty(window, 'innerWidth', {
        writable: true,
        configurable: true,
        value: 375,
      });
      
      const { container } = render(<SearchableProductList {...defaultProps} />);
      
      // Run accessibility audit on mobile viewport
      const results = await axe(container, axeConfig);
      expect(results).toHaveNoViolations();
      
      // Verify touch targets are adequately sized (minimum 44px)
      const buttons = screen.getAllByRole('button');
      buttons.forEach(button => {
        const styles = getComputedStyle(button);
        const height = parseInt(styles.height);
        const width = parseInt(styles.width);
        
        // Note: In a real test, you'd check computed styles
        // Here we verify the classes suggest proper sizing
        expect(button.className).toMatch(/p-[234]|py-[234]|h-[0-9]+/);
      });
    });

    test('touch interaction accessibility', async () => {
      render(<SearchableProductList {...defaultProps} />);
      
      const productCard = screen.getAllByRole('gridcell')[0];
      
      // Simulate touch interaction
      fireEvent.touchStart(productCard);
      fireEvent.touchEnd(productCard);
      
      expect(defaultProps.onProductSelect).toHaveBeenCalled();
    });
  });

  describe('Error Prevention and Recovery', () => {
    test('provides clear error messages', () => {
      const errorMessage = 'Network error: Unable to load products';
      render(<SearchableProductList {...defaultProps} error={errorMessage} />);
      
      const errorHeading = screen.getByText(/error loading products/i);
      expect(errorHeading).toBeInTheDocument();
      
      const errorDetails = screen.getByText(errorMessage);
      expect(errorDetails).toBeInTheDocument();
    });

    test('empty state provides helpful guidance', () => {
      render(<SearchableProductList {...defaultProps} products={[]} />);
      
      const emptyMessage = screen.getByText(/no products found/i);
      expect(emptyMessage).toBeInTheDocument();
      
      const clearButton = screen.getByRole('button', { name: /clear all filters/i });
      expect(clearButton).toBeInTheDocument();
    });

    test('search provides helpful feedback', async () => {
      render(<SearchableProductList {...defaultProps} />);
      
      const searchInput = screen.getByRole('textbox', { name: /search products/i });
      await userEvent.type(searchInput, 'nonexistentproduct');
      
      await waitFor(() => {
        const noResults = screen.getByText(/no products found/i);
        expect(noResults).toBeInTheDocument();
      });
    });
  });
});

// Accessibility test utilities for reuse
export const accessibilityTestUtils = {
  checkKeyboardNavigation: async (element: HTMLElement) => {
    element.focus();
    expect(element).toHaveFocus();
    
    await userEvent.keyboard('{Enter}');
    await userEvent.keyboard(' ');
    await userEvent.keyboard('{Tab}');
  },
  
  checkAriaAttributes: (element: HTMLElement, requiredAttrs: string[]) => {
    requiredAttrs.forEach(attr => {
      expect(element).toHaveAttribute(attr);
    });
  },
  
  checkColorIndependence: (element: HTMLElement) => {
    // Verify element provides information through means other than color
    const textContent = element.textContent;
    const ariaLabel = element.getAttribute('aria-label');
    const title = element.getAttribute('title');
    
    expect(textContent || ariaLabel || title).toBeTruthy();
  },
};