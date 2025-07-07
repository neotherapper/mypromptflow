---
title: "AI-Assisted Frontend Development Code Examples & Templates"
type: "code-examples"
framework: "frontend-development"
technology: "typescript"
examples: ["react", "nextjs", "vue", "angular", "testing", "performance"]
status: "active"
version: "1.0.0"
last_updated: "2025-01-07"
---

# AI-Assisted Frontend Development Code Examples & Templates

## AI Agent Instructions

This guide provides comprehensive code examples and templates for AI-assisted frontend development. Use these patterns as starting points for AI-generated code and workflow implementation.

## React/Next.js Examples

### 1. AI-Generated Component with Full TypeScript Support

```typescript
// AI-generated searchable product list component
import React, { useState, useMemo, useCallback } from 'react';
import { debounce } from 'lodash';

interface Product {
  id: number;
  name: string;
  category: string;
  price: number;
  description: string;
  image: string;
  inStock: boolean;
}

interface SearchableProductListProps {
  products: Product[];
  onProductSelect: (product: Product) => void;
  loading?: boolean;
  error?: string;
}

export const SearchableProductList: React.FC<SearchableProductListProps> = ({
  products,
  onProductSelect,
  loading = false,
  error
}) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [sortBy, setSortBy] = useState<'name' | 'price'>('name');

  // AI-optimized filtering and sorting
  const filteredAndSortedProducts = useMemo(() => {
    let filtered = products.filter(product => {
      const matchesSearch = product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           product.description.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesCategory = selectedCategory === 'all' || product.category === selectedCategory;
      return matchesSearch && matchesCategory;
    });

    filtered.sort((a, b) => {
      if (sortBy === 'price') {
        return a.price - b.price;
      }
      return a.name.localeCompare(b.name);
    });

    return filtered;
  }, [products, searchTerm, selectedCategory, sortBy]);

  // AI-generated debounced search
  const debouncedSearch = useCallback(
    debounce((term: string) => {
      setSearchTerm(term);
    }, 300),
    []
  );

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    debouncedSearch(e.target.value);
  };

  const categories = useMemo(() => {
    const cats = Array.from(new Set(products.map(p => p.category)));
    return ['all', ...cats];
  }, [products]);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-md p-4">
        <h3 className="text-red-800 font-medium">Error loading products</h3>
        <p className="text-red-600">{error}</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Search and filter controls */}
      <div className="flex flex-col sm:flex-row gap-4">
        <div className="flex-1">
          <label htmlFor="search" className="sr-only">Search products</label>
          <input
            id="search"
            type="text"
            placeholder="Search products..."
            onChange={handleSearchChange}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            aria-label="Search products"
          />
        </div>
        
        <select
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
          className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          aria-label="Filter by category"
        >
          {categories.map(category => (
            <option key={category} value={category}>
              {category === 'all' ? 'All Categories' : category}
            </option>
          ))}
        </select>

        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value as 'name' | 'price')}
          className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
          aria-label="Sort by"
        >
          <option value="name">Sort by Name</option>
          <option value="price">Sort by Price</option>
        </select>
      </div>

      {/* Results count */}
      <div className="text-sm text-gray-600">
        {filteredAndSortedProducts.length} product{filteredAndSortedProducts.length !== 1 ? 's' : ''} found
      </div>

      {/* Product grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredAndSortedProducts.map(product => (
          <div
            key={product.id}
            className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow cursor-pointer"
            onClick={() => onProductSelect(product)}
            role="button"
            tabIndex={0}
            onKeyDown={(e) => {
              if (e.key === 'Enter' || e.key === ' ') {
                onProductSelect(product);
              }
            }}
            aria-label={`Select ${product.name}`}
          >
            <img
              src={product.image}
              alt={product.name}
              className="w-full h-48 object-cover"
              loading="lazy"
            />
            <div className="p-4">
              <h3 className="font-semibold text-lg text-gray-900">{product.name}</h3>
              <p className="text-gray-600 text-sm mt-1">{product.description}</p>
              <div className="flex justify-between items-center mt-4">
                <span className="text-xl font-bold text-blue-600">${product.price}</span>
                <span className={`px-2 py-1 rounded-full text-xs ${
                  product.inStock 
                    ? 'bg-green-100 text-green-800' 
                    : 'bg-red-100 text-red-800'
                }`}>
                  {product.inStock ? 'In Stock' : 'Out of Stock'}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {filteredAndSortedProducts.length === 0 && (
        <div className="text-center py-8">
          <p className="text-gray-500">No products found matching your criteria.</p>
        </div>
      )}
    </div>
  );
};
```

### 2. AI-Generated Custom Hook Template

```typescript
// AI-generated data fetching hook with error handling
import { useState, useEffect, useCallback } from 'react';

interface UseApiState<T> {
  data: T | null;
  loading: boolean;
  error: string | null;
}

interface UseApiOptions {
  immediate?: boolean;
  retries?: number;
  retryDelay?: number;
}

export function useApi<T>(
  url: string,
  options: UseApiOptions = {}
): UseApiState<T> & { refetch: () => Promise<void>; reset: () => void } {
  const { immediate = true, retries = 3, retryDelay = 1000 } = options;
  
  const [state, setState] = useState<UseApiState<T>>({
    data: null,
    loading: false,
    error: null
  });

  const fetchData = useCallback(async (attemptCount = 0): Promise<void> => {
    setState(prev => ({ ...prev, loading: true, error: null }));

    try {
      const response = await fetch(url);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setState({ data, loading: false, error: null });
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'An error occurred';
      
      if (attemptCount < retries) {
        setTimeout(() => {
          fetchData(attemptCount + 1);
        }, retryDelay);
      } else {
        setState(prev => ({
          ...prev,
          loading: false,
          error: errorMessage
        }));
      }
    }
  }, [url, retries, retryDelay]);

  const reset = useCallback(() => {
    setState({ data: null, loading: false, error: null });
  }, []);

  useEffect(() => {
    if (immediate) {
      fetchData();
    }
  }, [fetchData, immediate]);

  return {
    ...state,
    refetch: fetchData,
    reset
  };
}
```

### 3. AI-Generated Form Validation Hook

```typescript
// AI-generated form validation with TypeScript
import { useState, useCallback } from 'react';

type ValidationRule<T> = {
  validator: (value: T) => boolean;
  message: string;
};

type ValidationSchema<T> = {
  [K in keyof T]: ValidationRule<T[K]>[];
};

type ValidationErrors<T> = {
  [K in keyof T]?: string;
};

export function useFormValidation<T extends Record<string, any>>(
  initialValues: T,
  validationSchema: ValidationSchema<T>
) {
  const [values, setValues] = useState<T>(initialValues);
  const [errors, setErrors] = useState<ValidationErrors<T>>({});
  const [touched, setTouched] = useState<Record<keyof T, boolean>>({} as Record<keyof T, boolean>);

  const validateField = useCallback((name: keyof T, value: T[keyof T]): string | null => {
    const fieldRules = validationSchema[name];
    if (!fieldRules) return null;

    for (const rule of fieldRules) {
      if (!rule.validator(value)) {
        return rule.message;
      }
    }
    return null;
  }, [validationSchema]);

  const validateForm = useCallback((): boolean => {
    const newErrors: ValidationErrors<T> = {};
    let isValid = true;

    Object.keys(values).forEach(key => {
      const fieldKey = key as keyof T;
      const error = validateField(fieldKey, values[fieldKey]);
      if (error) {
        newErrors[fieldKey] = error;
        isValid = false;
      }
    });

    setErrors(newErrors);
    return isValid;
  }, [values, validateField]);

  const setValue = useCallback((name: keyof T, value: T[keyof T]) => {
    setValues(prev => ({ ...prev, [name]: value }));
    
    // Validate field if it's been touched
    if (touched[name]) {
      const error = validateField(name, value);
      setErrors(prev => ({ ...prev, [name]: error || undefined }));
    }
  }, [validateField, touched]);

  const setTouched = useCallback((name: keyof T) => {
    setTouched(prev => ({ ...prev, [name]: true }));
    
    // Validate field when touched
    const error = validateField(name, values[name]);
    setErrors(prev => ({ ...prev, [name]: error || undefined }));
  }, [validateField, values]);

  const resetForm = useCallback(() => {
    setValues(initialValues);
    setErrors({});
    setTouched({} as Record<keyof T, boolean>);
  }, [initialValues]);

  return {
    values,
    errors,
    touched,
    setValue,
    setTouched,
    validateForm,
    resetForm,
    isValid: Object.keys(errors).length === 0
  };
}

// Example usage
const loginFormSchema: ValidationSchema<{ email: string; password: string }> = {
  email: [
    { validator: (value) => value.length > 0, message: 'Email is required' },
    { validator: (value) => /\S+@\S+\.\S+/.test(value), message: 'Email is invalid' }
  ],
  password: [
    { validator: (value) => value.length > 0, message: 'Password is required' },
    { validator: (value) => value.length >= 8, message: 'Password must be at least 8 characters' }
  ]
};
```

## Vue.js Examples

### 4. AI-Generated Vue Composition API Component

```vue
<!-- AI-generated Vue component with TypeScript -->
<template>
  <div class="user-profile">
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Loading user profile...</p>
    </div>
    
    <div v-else-if="error" class="error">
      <h3>Error loading profile</h3>
      <p>{{ error }}</p>
      <button @click="refetch">Retry</button>
    </div>
    
    <div v-else-if="user" class="profile-content">
      <div class="profile-header">
        <img :src="user.avatar" :alt="`${user.name} avatar`" class="avatar" />
        <div class="user-info">
          <h1>{{ user.name }}</h1>
          <p class="email">{{ user.email }}</p>
          <p class="role">{{ user.role }}</p>
        </div>
      </div>
      
      <div class="profile-tabs">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          @click="activeTab = tab.id"
          :class="{ active: activeTab === tab.id }"
          class="tab-button"
        >
          {{ tab.label }}
        </button>
      </div>
      
      <div class="tab-content">
        <component :is="activeTabComponent" :user="user" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useApi } from '../composables/useApi';
import ProfileDetails from './ProfileDetails.vue';
import UserSettings from './UserSettings.vue';
import ActivityHistory from './ActivityHistory.vue';

interface User {
  id: number;
  name: string;
  email: string;
  role: string;
  avatar: string;
  createdAt: string;
  lastLogin: string;
}

interface Tab {
  id: string;
  label: string;
  component: string;
}

const props = defineProps<{
  userId: number;
}>();

// AI-generated reactive state
const activeTab = ref('details');
const tabs: Tab[] = [
  { id: 'details', label: 'Details', component: 'ProfileDetails' },
  { id: 'settings', label: 'Settings', component: 'UserSettings' },
  { id: 'activity', label: 'Activity', component: 'ActivityHistory' }
];

// AI-generated API integration
const { data: user, loading, error, refetch } = useApi<User>(
  () => `/api/users/${props.userId}`,
  { immediate: true }
);

// AI-generated computed properties
const activeTabComponent = computed(() => {
  const componentMap: Record<string, any> = {
    'details': ProfileDetails,
    'settings': UserSettings,
    'activity': ActivityHistory
  };
  return componentMap[activeTab.value];
});

onMounted(() => {
  // AI-generated lifecycle hook
  console.log('UserProfile component mounted');
});
</script>

<style scoped>
.user-profile {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #3498db;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error {
  background-color: #fee;
  border: 1px solid #fcc;
  padding: 20px;
  border-radius: 8px;
  text-align: center;
}

.profile-header {
  display: flex;
  align-items: center;
  margin-bottom: 30px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  margin-right: 20px;
}

.user-info h1 {
  margin: 0 0 8px 0;
  font-size: 24px;
}

.email {
  color: #666;
  margin: 4px 0;
}

.role {
  color: #007bff;
  font-weight: 500;
}

.profile-tabs {
  display: flex;
  border-bottom: 1px solid #ddd;
  margin-bottom: 20px;
}

.tab-button {
  padding: 12px 24px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  color: #666;
  border-bottom: 2px solid transparent;
  transition: all 0.3s ease;
}

.tab-button:hover {
  color: #007bff;
}

.tab-button.active {
  color: #007bff;
  border-bottom-color: #007bff;
}

.tab-content {
  min-height: 200px;
}
</style>
```

## Testing Templates

### 5. AI-Generated Testing Suite

```typescript
// AI-generated comprehensive test suite
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { SearchableProductList } from './SearchableProductList';

const mockProducts = [
  {
    id: 1,
    name: 'MacBook Pro',
    category: 'electronics',
    price: 2499,
    description: 'Apple MacBook Pro 16-inch',
    image: '/macbook.jpg',
    inStock: true
  },
  {
    id: 2,
    name: 'iPhone 15',
    category: 'electronics',
    price: 999,
    description: 'Apple iPhone 15 Pro',
    image: '/iphone.jpg',
    inStock: false
  },
  {
    id: 3,
    name: 'Gaming Chair',
    category: 'furniture',
    price: 299,
    description: 'Ergonomic gaming chair',
    image: '/chair.jpg',
    inStock: true
  }
];

describe('SearchableProductList', () => {
  const mockOnProductSelect = jest.fn();

  beforeEach(() => {
    mockOnProductSelect.mockClear();
  });

  it('renders all products initially', () => {
    render(
      <SearchableProductList 
        products={mockProducts} 
        onProductSelect={mockOnProductSelect} 
      />
    );

    expect(screen.getByText('MacBook Pro')).toBeInTheDocument();
    expect(screen.getByText('iPhone 15')).toBeInTheDocument();
    expect(screen.getByText('Gaming Chair')).toBeInTheDocument();
  });

  it('filters products by search term', async () => {
    const user = userEvent.setup();
    
    render(
      <SearchableProductList 
        products={mockProducts} 
        onProductSelect={mockOnProductSelect} 
      />
    );

    const searchInput = screen.getByPlaceholderText('Search products...');
    await user.type(searchInput, 'macbook');

    await waitFor(() => {
      expect(screen.getByText('MacBook Pro')).toBeInTheDocument();
      expect(screen.queryByText('iPhone 15')).not.toBeInTheDocument();
      expect(screen.queryByText('Gaming Chair')).not.toBeInTheDocument();
    });
  });

  it('filters products by category', async () => {
    const user = userEvent.setup();
    
    render(
      <SearchableProductList 
        products={mockProducts} 
        onProductSelect={mockOnProductSelect} 
      />
    );

    const categorySelect = screen.getByLabelText('Filter by category');
    await user.selectOptions(categorySelect, 'furniture');

    expect(screen.getByText('Gaming Chair')).toBeInTheDocument();
    expect(screen.queryByText('MacBook Pro')).not.toBeInTheDocument();
    expect(screen.queryByText('iPhone 15')).not.toBeInTheDocument();
  });

  it('sorts products by price', async () => {
    const user = userEvent.setup();
    
    render(
      <SearchableProductList 
        products={mockProducts} 
        onProductSelect={mockOnProductSelect} 
      />
    );

    const sortSelect = screen.getByLabelText('Sort by');
    await user.selectOptions(sortSelect, 'price');

    const productNames = screen.getAllByRole('button').map(button => 
      button.textContent?.includes('$') ? button.textContent : null
    ).filter(Boolean);

    // Gaming Chair ($299) should come before iPhone 15 ($999)
    expect(productNames[0]).toContain('Gaming Chair');
  });

  it('handles product selection', async () => {
    const user = userEvent.setup();
    
    render(
      <SearchableProductList 
        products={mockProducts} 
        onProductSelect={mockOnProductSelect} 
      />
    );

    const macbookCard = screen.getByLabelText('Select MacBook Pro');
    await user.click(macbookCard);

    expect(mockOnProductSelect).toHaveBeenCalledWith(mockProducts[0]);
  });

  it('handles keyboard navigation', async () => {
    const user = userEvent.setup();
    
    render(
      <SearchableProductList 
        products={mockProducts} 
        onProductSelect={mockOnProductSelect} 
      />
    );

    const macbookCard = screen.getByLabelText('Select MacBook Pro');
    macbookCard.focus();
    await user.keyboard('{Enter}');

    expect(mockOnProductSelect).toHaveBeenCalledWith(mockProducts[0]);
  });

  it('shows loading state', () => {
    render(
      <SearchableProductList 
        products={[]} 
        onProductSelect={mockOnProductSelect} 
        loading={true}
      />
    );

    expect(screen.getByRole('progressbar')).toBeInTheDocument();
  });

  it('shows error state', () => {
    render(
      <SearchableProductList 
        products={[]} 
        onProductSelect={mockOnProductSelect} 
        error="Failed to load products"
      />
    );

    expect(screen.getByText('Error loading products')).toBeInTheDocument();
    expect(screen.getByText('Failed to load products')).toBeInTheDocument();
  });

  it('shows empty state when no products match filters', async () => {
    const user = userEvent.setup();
    
    render(
      <SearchableProductList 
        products={mockProducts} 
        onProductSelect={mockOnProductSelect} 
      />
    );

    const searchInput = screen.getByPlaceholderText('Search products...');
    await user.type(searchInput, 'nonexistent');

    await waitFor(() => {
      expect(screen.getByText('No products found matching your criteria.')).toBeInTheDocument();
    });
  });
});
```

## Performance Templates

### 6. AI-Generated Performance Monitoring

```typescript
// AI-generated performance monitoring utility
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

interface PerformanceMetrics {
  cls: number;
  fid: number;
  fcp: number;
  lcp: number;
  ttfb: number;
  timestamp: number;
}

class PerformanceMonitor {
  private metrics: Partial<PerformanceMetrics> = {};
  private observers: PerformanceObserver[] = [];

  constructor(private onMetricsUpdate?: (metrics: PerformanceMetrics) => void) {
    this.initializeWebVitals();
    this.initializeCustomMetrics();
  }

  private initializeWebVitals(): void {
    getCLS(this.handleMetric('cls'));
    getFID(this.handleMetric('fid'));
    getFCP(this.handleMetric('fcp'));
    getLCP(this.handleMetric('lcp'));
    getTTFB(this.handleMetric('ttfb'));
  }

  private handleMetric(name: keyof PerformanceMetrics) {
    return (metric: any) => {
      this.metrics[name] = metric.value;
      this.metrics.timestamp = Date.now();
      
      if (this.onMetricsUpdate && this.isComplete()) {
        this.onMetricsUpdate(this.metrics as PerformanceMetrics);
      }
    };
  }

  private initializeCustomMetrics(): void {
    // Monitor long tasks
    if ('PerformanceObserver' in window) {
      const longTaskObserver = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          if (entry.duration > 50) {
            console.warn(`Long task detected: ${entry.duration}ms`);
          }
        }
      });
      
      longTaskObserver.observe({ type: 'longtask', buffered: true });
      this.observers.push(longTaskObserver);
    }

    // Monitor memory usage
    this.monitorMemoryUsage();
  }

  private monitorMemoryUsage(): void {
    if ('memory' in performance) {
      const memoryInfo = (performance as any).memory;
      
      setInterval(() => {
        const memoryUsage = {
          usedJSHeapSize: memoryInfo.usedJSHeapSize,
          totalJSHeapSize: memoryInfo.totalJSHeapSize,
          jsHeapSizeLimit: memoryInfo.jsHeapSizeLimit
        };
        
        // Alert if memory usage is high
        const usagePercent = (memoryUsage.usedJSHeapSize / memoryUsage.jsHeapSizeLimit) * 100;
        if (usagePercent > 80) {
          console.warn(`High memory usage: ${usagePercent.toFixed(2)}%`);
        }
      }, 30000); // Check every 30 seconds
    }
  }

  private isComplete(): boolean {
    return !!(this.metrics.cls && this.metrics.fid && this.metrics.fcp && 
              this.metrics.lcp && this.metrics.ttfb);
  }

  public getMetrics(): Partial<PerformanceMetrics> {
    return { ...this.metrics };
  }

  public destroy(): void {
    this.observers.forEach(observer => observer.disconnect());
    this.observers = [];
  }
}

// Usage example
export const performanceMonitor = new PerformanceMonitor((metrics) => {
  console.log('Performance metrics:', metrics);
  
  // Send to analytics service
  if (window.gtag) {
    window.gtag('event', 'web_vitals', {
      'custom_parameter': metrics.lcp,
      'custom_parameter_2': metrics.cls
    });
  }
});
```

## Cross-References

- @ai/knowledge/components/react-optimization-patterns
- @ai/knowledge/testing/comprehensive-test-strategies
- @ai/knowledge/performance/web-vitals-monitoring
- @research/findings/ai-frontend-development/

## Usage Guidelines

### For AI Agents
- Use these templates as starting points for code generation
- Adapt TypeScript interfaces to match project requirements
- Ensure accessibility compliance in all generated components
- Follow performance best practices in component implementation

### For Developers
- Copy and customize templates for your specific use cases
- Validate AI-generated code against your project standards
- Test thoroughly before deploying AI-generated components
- Monitor performance impact of AI-generated code