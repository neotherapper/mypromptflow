# React Performance Context - For AI Agent Performance Specialists

## Overview

This context provides performance optimization guidance for AI agents working in performance specialist roles on React applications. Focus on performance analysis, optimization techniques, profiling methods, and performance monitoring patterns.

## Current React Version Performance Context

**React 19.0.0** (Latest as of 2025-07-25)
- **Performance Improvements**: React Compiler for automatic optimizations, improved Server Components, enhanced concurrent features
- **New Profiling APIs**: Enhanced React DevTools Profiler, better performance tracking
- **Bundle Optimizations**: Tree shaking improvements, better dead code elimination
- **Server Components**: Reduced client bundle size, server-side performance gains

## Performance Analysis Techniques

### 1. React DevTools Profiler
```typescript
import { Profiler, ProfilerOnRenderCallback } from 'react';

// Performance measurement wrapper
function PerformanceProfiler({ 
  id, 
  children, 
  onRender 
}: { 
  id: string;
  children: React.ReactNode;
  onRender?: ProfilerOnRenderCallback;
}) {
  const handleRender: ProfilerOnRenderCallback = (
    id,
    phase,
    actualDuration,
    baseDuration,
    startTime,
    commitTime,
    interactions
  ) => {
    // Log performance metrics
    console.log('Performance Metrics:', {
      component: id,
      phase, // 'mount' or 'update'
      actualDuration, // Time spent rendering
      baseDuration, // Estimated time to render entire subtree
      startTime, // When React began rendering
      commitTime, // When React committed the update
      interactions: Array.from(interactions) // Set of interactions
    });
    
    // Send metrics to analytics
    if (actualDuration > 16) { // Flag slow renders (>16ms = 60fps threshold)
      reportPerformanceMetric({
        type: 'slow_render',
        component: id,
        duration: actualDuration,
        phase,
        timestamp: Date.now()
      });
    }
    
    // Call custom onRender callback
    onRender?.(id, phase, actualDuration, baseDuration, startTime, commitTime, interactions);
  };
  
  return (
    <Profiler id={id} onRender={handleRender}>
      {children}
    </Profiler>
  );
}

// Usage example
function App() {
  return (
    <PerformanceProfiler id="App">
      <Header />
      <PerformanceProfiler id="MainContent">
        <MainContent />
      </PerformanceProfiler>
      <Footer />
    </PerformanceProfiler>
  );
}
```

### 2. Custom Performance Hooks
```typescript
import { useEffect, useRef, useState, useCallback } from 'react';

// Hook for measuring component render times
function useRenderTime(componentName: string) {
  const renderStartTime = useRef<number>();
  const [renderMetrics, setRenderMetrics] = useState<{
    lastRenderTime: number;
    averageRenderTime: number;
    renderCount: number;
  }>({
    lastRenderTime: 0,
    averageRenderTime: 0,
    renderCount: 0
  });
  
  // Mark render start
  renderStartTime.current = performance.now();
  
  useEffect(() => {
    const renderEndTime = performance.now();
    const renderTime = renderEndTime - (renderStartTime.current || renderEndTime);
    
    setRenderMetrics(prev => {
      const newCount = prev.renderCount + 1;
      const newAverage = (prev.averageRenderTime * prev.renderCount + renderTime) / newCount;
      
      return {
        lastRenderTime: renderTime,
        averageRenderTime: newAverage,
        renderCount: newCount
      };
    });
    
    // Warn about slow renders
    if (renderTime > 16) {
      console.warn(`Slow render detected in ${componentName}: ${renderTime.toFixed(2)}ms`);
    }
  });
  
  return renderMetrics;
}

// Hook for measuring memory usage
function useMemoryUsage() {
  const [memoryInfo, setMemoryInfo] = useState<{
    usedJSHeapSize: number;
    totalJSHeapSize: number;
    jsHeapSizeLimit: number;
  } | null>(null);
  
  const measureMemory = useCallback(() => {
    if ('memory' in performance) {
      const memory = (performance as any).memory;
      setMemoryInfo({
        usedJSHeapSize: memory.usedJSHeapSize,
        totalJSHeapSize: memory.totalJSHeapSize,
        jsHeapSizeLimit: memory.jsHeapSizeLimit
      });
    }
  }, []);
  
  useEffect(() => {
    measureMemory();
    const interval = setInterval(measureMemory, 5000); // Measure every 5 seconds
    
    return () => clearInterval(interval);
  }, [measureMemory]);
  
  return { memoryInfo, measureMemory };
}

// Usage example
function PerformanceAwareComponent() {
  const renderMetrics = useRenderTime('PerformanceAwareComponent');
  const { memoryInfo } = useMemoryUsage();
  
  return (
    <div className="performance-aware">
      <div className="content">
        {/* Component content */}
      </div>
      
      {process.env.NODE_ENV === 'development' && (
        <div className="performance-debug">
          <p>Last render: {renderMetrics.lastRenderTime.toFixed(2)}ms</p>
          <p>Average render: {renderMetrics.averageRenderTime.toFixed(2)}ms</p>
          <p>Render count: {renderMetrics.renderCount}</p>
          {memoryInfo && (
            <p>Memory: {(memoryInfo.usedJSHeapSize / 1024 / 1024).toFixed(2)}MB</p>
          )}
        </div>
      )}
    </div>
  );
}
```

## React 19 Performance Optimizations

### 1. React Compiler Optimizations
```typescript
// React Compiler automatically optimizes these patterns
// Manual optimizations are less necessary with React 19

// Before React 19 (manual optimization required)
const ManualOptimization = memo(function ExpensiveComponent({ data, onUpdate }) {
  const processedData = useMemo(() => expensiveCalculation(data), [data]);
  const handleUpdate = useCallback((id) => onUpdate(id), [onUpdate]);
  
  return <div>{/* render logic */}</div>;
});

// React 19 with Compiler (automatic optimization)
function AutoOptimizedComponent({ data, onUpdate }) {
  // React Compiler automatically memoizes when beneficial
  const processedData = expensiveCalculation(data);
  const handleUpdate = (id) => onUpdate(id);
  
  return <div>{/* render logic */}</div>;
}

// Compiler directives for fine-tuned control
function ComponentWithDirectives({ items }) {
  // Mark expensive computation for compiler attention
  'use memo'; // Hint to compiler to memoize this component
  
  const expensiveResult = items.map(item => ({
    ...item,
    processed: heavyComputation(item.data)
  }));
  
  return (
    <div>
      {expensiveResult.map(item => (
        <ItemComponent key={item.id} item={item} />
      ))}
    </div>
  );
}
```

### 2. Server Components Performance
```typescript
// Server Component - runs on server, reduces client bundle
async function ProductList({ category }: { category: string }) {
  // This runs on the server - no client-side JavaScript sent
  const products = await fetchProducts(category);
  const processedProducts = products.map(product => ({
    ...product,
    formattedPrice: formatCurrency(product.price)
  }));
  
  return (
    <div className="product-list">
      {processedProducts.map(product => (
        // Server Component can render client components
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  );
}

// Client Component - interactive parts only
'use client';
function ProductCard({ product }: { product: Product }) {
  const [isInCart, setIsInCart] = useState(false);
  
  return (
    <div className="product-card">
      <h3>{product.name}</h3>
      <p>{product.formattedPrice}</p>
      <button
        onClick={() => setIsInCart(!isInCart)}
        className={isInCart ? 'in-cart' : 'add-to-cart'}
      >
        {isInCart ? 'Remove from Cart' : 'Add to Cart'}
      </button>
    </div>
  );
}

// Hybrid approach for optimal performance
async function OptimizedProductPage({ productId }: { productId: string }) {
  // Server-side data fetching and processing
  const [product, reviews, relatedProducts] = await Promise.all([
    fetchProduct(productId),
    fetchReviews(productId),
    fetchRelatedProducts(productId)
  ]);
  
  return (
    <div className="product-page">
      {/* Static content rendered on server */}
      <ProductDetails product={product} />
      <ReviewsList reviews={reviews} />
      
      {/* Interactive components sent to client */}
      <AddToCartButton product={product} />
      <RelatedProductsCarousel products={relatedProducts} />
    </div>
  );
}
```

### 3. Concurrent Features Performance
```typescript
import { startTransition, useDeferredValue, Suspense } from 'react';

// Prioritize urgent updates over non-urgent ones
function SearchInterface() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isPending, setIsPending] = useState(false);
  
  // Defer expensive search results
  const deferredQuery = useDeferredValue(query);
  
  const handleSearch = (newQuery: string) => {
    setQuery(newQuery); // Urgent update - immediate
    
    startTransition(() => {
      setIsPending(true);
      // Non-urgent update - can be interrupted
      performSearch(newQuery).then(results => {
        setResults(results);
        setIsPending(false);
      });
    });
  };
  
  return (
    <div className="search-interface">
      <input
        type="text"
        value={query}
        onChange={(e) => handleSearch(e.target.value)}
        placeholder="Search products..."
      />
      
      <Suspense fallback={<SearchSkeleton />}>
        <SearchResults 
          query={deferredQuery} 
          results={results}
          isPending={isPending}
        />
      </Suspense>
    </div>
  );
}

// Optimistic updates for better perceived performance
function OptimisticTodoList({ todos }: { todos: Todo[] }) {
  const [optimisticTodos, addOptimisticTodo] = useOptimistic(
    todos,
    (currentTodos, optimisticTodo) => [
      ...currentTodos,
      { ...optimisticTodo, id: Date.now(), pending: true }
    ]
  );
  
  const addTodo = async (text: string) => {
    // Immediate UI update
    addOptimisticTodo({ text, completed: false });
    
    // Background server sync
    startTransition(async () => {
      await createTodo(text);
    });
  };
  
  return (
    <div className="todo-list">
      {optimisticTodos.map(todo => (
        <TodoItem 
          key={todo.id} 
          todo={todo}
          className={todo.pending ? 'pending' : ''}
        />
      ))}
    </div>
  );
}
```

## Bundle Size Optimization

### 1. Code Splitting Strategies
```typescript
import { lazy, Suspense } from 'react';

// Route-level code splitting
const HomePage = lazy(() => import('../pages/HomePage'));
const ProductPage = lazy(() => import('../pages/ProductPage'));
const CheckoutPage = lazy(() => import('../pages/CheckoutPage'));

// Component-level code splitting for large components
const DataVisualization = lazy(() => import('../components/DataVisualization'));
const RichTextEditor = lazy(() => import('../components/RichTextEditor'));

// Dynamic imports with error handling
const LazyModal = lazy(() => 
  import('../components/Modal').catch(() => ({
    default: () => <div>Failed to load modal</div>
  }))
);

// Conditional loading based on user permissions
function AdminPanel({ user }: { user: User }) {
  const [showAdvanced, setShowAdvanced] = useState(false);
  
  return (
    <div className="admin-panel">
      <div className="basic-controls">
        {/* Always loaded content */}
      </div>
      
      {user.isAdmin && (
        <button onClick={() => setShowAdvanced(true)}>
          Show Advanced Features
        </button>
      )}
      
      {showAdvanced && (
        <Suspense fallback={<div>Loading advanced features...</div>}>
          <LazyAdminFeatures />
        </Suspense>
      )}
    </div>
  );
}

// Preloading for better UX
function ProductCard({ product }: { product: Product }) {
  const [preloadTriggered, setPreloadTriggered] = useState(false);
  
  const handleMouseEnter = () => {
    if (!preloadTriggered) {
      // Preload the product detail page
      import('../pages/ProductDetailPage');
      setPreloadTriggered(true);
    }
  };
  
  return (
    <div 
      className="product-card"
      onMouseEnter={handleMouseEnter}
    >
      {/* Product card content */}
    </div>
  );
}
```

### 2. Tree Shaking Optimization
```typescript
// Bad: Imports entire library
import _ from 'lodash';
import * as utils from '../utils';

// Good: Import only what you need
import { debounce, throttle } from 'lodash';
import { formatCurrency, validateEmail } from '../utils';

// Optimal: Use tree-shakable alternatives
import debounce from 'lodash/debounce';
import throttle from 'lodash/throttle';

// Custom utilities that are tree-shakable
// utils/index.ts
export { formatCurrency } from './currency';
export { validateEmail } from './validation';
export { debounce } from './timing';

// Component using tree-shakable imports
import { formatCurrency, validateEmail } from '../utils';
import { debounce } from '../utils/timing';

function OptimizedComponent({ price, email }: { price: number; email: string }) {
  const debouncedValidation = useMemo(
    () => debounce(validateEmail, 300),
    []
  );
  
  return (
    <div>
      <span>{formatCurrency(price)}</span>
      <input 
        type="email"
        onChange={(e) => debouncedValidation(e.target.value)}
      />
    </div>
  );
}

// Bundle analyzer configuration
// webpack.config.js or vite.config.js
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;

module.exports = {
  plugins: [
    new BundleAnalyzerPlugin({
      analyzerMode: 'static',
      openAnalyzer: false,
      reportFilename: 'bundle-report.html'
    })
  ]
};
```

## Memory Optimization

### 1. Memory Leak Prevention
```typescript
import { useEffect, useRef, useCallback } from 'react';

// Proper cleanup of subscriptions
function useWebSocketConnection(url: string) {
  const ws = useRef<WebSocket | null>(null);
  const [connectionStatus, setConnectionStatus] = useState<'connecting' | 'connected' | 'disconnected'>('disconnected');
  
  useEffect(() => {
    // Create connection
    ws.current = new WebSocket(url);
    setConnectionStatus('connecting');
    
    const handleOpen = () => setConnectionStatus('connected');
    const handleClose = () => setConnectionStatus('disconnected');
    
    ws.current.addEventListener('open', handleOpen);
    ws.current.addEventListener('close', handleClose);
    
    // Cleanup function
    return () => {
      if (ws.current) {
        ws.current.removeEventListener('open', handleOpen);
        ws.current.removeEventListener('close', handleClose);
        ws.current.close();
        ws.current = null;
      }
    };
  }, [url]);
  
  return { connectionStatus, ws: ws.current };
}

// Memory-efficient event listener management
function useResizeListener(callback: (size: { width: number; height: number }) => void) {
  const callbackRef = useRef(callback);
  
  // Update callback ref without re-running effect
  useEffect(() => {
    callbackRef.current = callback;
  }, [callback]);
  
  useEffect(() => {
    const handleResize = () => {
      callbackRef.current({
        width: window.innerWidth,
        height: window.innerHeight
      });
    };
    
    window.addEventListener('resize', handleResize);
    
    // Initial call
    handleResize();
    
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []); // Empty deps array - effect only runs once
}

// Proper cleanup of intervals and timeouts
function useTimer(callback: () => void, delay: number | null) {
  const savedCallback = useRef(callback);
  
  useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);
  
  useEffect(() => {
    if (delay === null) return;
    
    const timer = setInterval(() => savedCallback.current(), delay);
    
    return () => clearInterval(timer);
  }, [delay]);
}
```

### 2. Efficient Data Structures
```typescript
// Use Map for better performance with large datasets
function useEntityManager<T extends { id: string }>() {
  const [entities] = useState(() => new Map<string, T>());
  
  const addEntity = useCallback((entity: T) => {
    entities.set(entity.id, entity);
  }, [entities]);
  
  const removeEntity = useCallback((id: string) => {
    entities.delete(id);
  }, [entities]);
  
  const getEntity = useCallback((id: string) => {
    return entities.get(id);
  }, [entities]);
  
  const getAllEntities = useCallback(() => {
    return Array.from(entities.values());
  }, [entities]);
  
  return {
    addEntity,
    removeEntity,
    getEntity,
    getAllEntities,
    size: entities.size
  };
}

// Virtual scrolling for large lists
function VirtualizedList({ 
  items, 
  itemHeight, 
  containerHeight 
}: {
  items: any[];
  itemHeight: number;
  containerHeight: number;
}) {
  const [scrollTop, setScrollTop] = useState(0);
  
  const startIndex = Math.floor(scrollTop / itemHeight);
  const endIndex = Math.min(
    startIndex + Math.ceil(containerHeight / itemHeight) + 1,
    items.length
  );
  
  const visibleItems = items.slice(startIndex, endIndex);
  
  return (
    <div 
      className="virtual-list-container"
      style={{ height: containerHeight, overflow: 'auto' }}
      onScroll={(e) => setScrollTop(e.currentTarget.scrollTop)}
    >
      <div style={{ height: items.length * itemHeight, position: 'relative' }}>
        {visibleItems.map((item, index) => (
          <div
            key={startIndex + index}
            style={{
              position: 'absolute',
              top: (startIndex + index) * itemHeight,
              height: itemHeight,
              width: '100%'
            }}
          >
            <ListItem item={item} />
          </div>
        ))}
      </div>
    </div>
  );
}
```

## Performance Monitoring

### 1. Real User Monitoring (RUM)
```typescript
// Core Web Vitals measurement
function measureWebVitals() {
  // Largest Contentful Paint
  new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      console.log('LCP:', entry.startTime);
      // Send to analytics
      gtag('event', 'web_vital', {
        name: 'LCP',
        value: Math.round(entry.startTime),
        event_category: 'performance'
      });
    }
  }).observe({ entryTypes: ['largest-contentful-paint'] });
  
  // First Input Delay
  new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      const fid = entry.processingStart - entry.startTime;
      console.log('FID:', fid);
      gtag('event', 'web_vital', {
        name: 'FID',
        value: Math.round(fid),
        event_category: 'performance'
      });
    }
  }).observe({ entryTypes: ['first-input'] });
  
  // Cumulative Layout Shift
  let cumulativeLayoutShift = 0;
  new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      if (!entry.hadRecentInput) {
        cumulativeLayoutShift += entry.value;
      }
    }
    console.log('CLS:', cumulativeLayoutShift);
    gtag('event', 'web_vital', {
      name: 'CLS',
      value: Math.round(cumulativeLayoutShift * 1000),
      event_category: 'performance'
    });
  }).observe({ entryTypes: ['layout-shift'] });
}

// Component-level performance tracking
function usePerformanceTracking(componentName: string) {
  const mountTime = useRef(performance.now());
  const renderCount = useRef(0);
  
  useEffect(() => {
    renderCount.current += 1;
    
    const renderTime = performance.now() - mountTime.current;
    
    // Track component lifecycle
    gtag('event', 'component_render', {
      component_name: componentName,
      render_count: renderCount.current,
      render_time: Math.round(renderTime),
      event_category: 'performance'
    });
    
    // Warn about excessive renders
    if (renderCount.current > 10) {
      console.warn(`Component ${componentName} has rendered ${renderCount.current} times`);
    }
  });
  
  return {
    renderCount: renderCount.current,
    mountTime: mountTime.current
  };
}
```

### 2. Performance Budget Monitoring
```typescript
// Performance budget configuration
const PERFORMANCE_BUDGETS = {
  // Bundle size budgets (in KB)
  MAIN_BUNDLE_SIZE: 250,
  VENDOR_BUNDLE_SIZE: 500,
  TOTAL_BUNDLE_SIZE: 1000,
  
  // Runtime performance budgets (in ms)
  TIME_TO_INTERACTIVE: 3000,
  FIRST_CONTENTFUL_PAINT: 1500,
  LARGEST_CONTENTFUL_PAINT: 2500,
  
  // Memory budgets (in MB)
  MEMORY_USAGE_LIMIT: 50,
  
  // Network budgets
  MAX_REQUESTS_PER_PAGE: 50,
  MAX_IMAGE_SIZE: 200 // KB
};

// Budget monitoring system
class PerformanceBudgetMonitor {
  private violations: Array<{ metric: string; value: number; budget: number; timestamp: number }> = [];
  
  checkBundleSize(bundleName: string, size: number) {
    const budget = PERFORMANCE_BUDGETS[`${bundleName.toUpperCase()}_BUNDLE_SIZE`];
    if (budget && size > budget) {
      this.reportViolation('bundle_size', size, budget);
    }
  }
  
  checkRuntimeMetric(metric: string, value: number) {
    const budget = PERFORMANCE_BUDGETS[metric.toUpperCase()];
    if (budget && value > budget) {
      this.reportViolation(metric, value, budget);
    }
  }
  
  private reportViolation(metric: string, value: number, budget: number) {
    const violation = {
      metric,
      value,
      budget,
      timestamp: Date.now()
    };
    
    this.violations.push(violation);
    
    console.warn(`Performance budget violation: ${metric}`, violation);
    
    // Send to monitoring service
    gtag('event', 'performance_budget_violation', {
      metric,
      value: Math.round(value),
      budget,
      event_category: 'performance'
    });
  }
  
  getViolations() {
    return this.violations;
  }
  
  clearViolations() {
    this.violations = [];
  }
}

// Usage in application
const performanceMonitor = new PerformanceBudgetMonitor();

// Monitor bundle sizes (in build process)
performanceMonitor.checkBundleSize('main', mainBundleSize);
performanceMonitor.checkBundleSize('vendor', vendorBundleSize);

// Monitor runtime metrics
window.addEventListener('load', () => {
  // Measure and check performance metrics
  const navigationTiming = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
  
  performanceMonitor.checkRuntimeMetric('time_to_interactive', navigationTiming.loadEventEnd);
  performanceMonitor.checkRuntimeMetric('first_contentful_paint', navigationTiming.responseStart);
});
```

## Performance Testing Strategies

### 1. Automated Performance Testing
```typescript
// Performance test utilities
function measureComponentRenderTime(Component: React.ComponentType, props: any) {
  const startTime = performance.now();
  
  const { unmount } = render(<Component {...props} />);
  
  const renderTime = performance.now() - startTime;
  
  unmount();
  
  return renderTime;
}

// Load testing simulation
function simulateHighLoad(Component: React.ComponentType, iterations: number = 100) {
  const renderTimes: number[] = [];
  
  for (let i = 0; i < iterations; i++) {
    const renderTime = measureComponentRenderTime(Component, {
      data: generateMockData(1000) // Large dataset
    });
    renderTimes.push(renderTime);
  }
  
  return {
    averageRenderTime: renderTimes.reduce((a, b) => a + b, 0) / renderTimes.length,
    maxRenderTime: Math.max(...renderTimes),
    minRenderTime: Math.min(...renderTimes),
    renders: renderTimes.length
  };
}

// Memory leak detection
function checkForMemoryLeaks(Component: React.ComponentType) {
  const initialMemory = (performance as any).memory?.usedJSHeapSize || 0;
  
  // Mount and unmount component multiple times
  for (let i = 0; i < 50; i++) {
    const { unmount } = render(<Component />);
    unmount();
  }
  
  // Force garbage collection if available
  if ('gc' in window) {
    (window as any).gc();
  }
  
  const finalMemory = (performance as any).memory?.usedJSHeapSize || 0;
  const memoryIncrease = finalMemory - initialMemory;
  
  return {
    initialMemory,
    finalMemory,
    memoryIncrease,
    potentialLeak: memoryIncrease > 1024 * 1024 // 1MB threshold
  };
}
```

## Best Practices for Performance Specialists

### 1. Performance Optimization Workflow
1. **Measure First**: Always profile before optimizing
2. **Focus on Impact**: Optimize the biggest performance bottlenecks first
3. **Test Changes**: Measure performance impact of optimizations
4. **Monitor Continuously**: Set up ongoing performance monitoring
5. **Document Findings**: Keep track of optimization techniques and results

### 2. Common Performance Pitfalls
- Over-optimizing with useMemo/useCallback when not needed
- Not cleaning up subscriptions and event listeners
- Large bundle sizes from unnecessary dependencies
- Inefficient re-rendering patterns
- Memory leaks from uncleaned references

### 3. Performance Tools and Resources
- React DevTools Profiler for component performance
- Chrome DevTools for Core Web Vitals
- Bundle analyzers for code splitting insights
- Lighthouse for comprehensive audits
- Real User Monitoring for production insights

## Context Usage Guidelines

**For AI Agents in Performance Specialist Role:**
1. Focus on measurable performance improvements and optimization techniques
2. Include specific profiling methods and performance measurement code
3. Consider both runtime performance and bundle size optimization
4. Think about real-world performance impact and user experience
5. Use React 19 performance features and compiler optimizations

**Don't Include:**
- Basic component implementation details (use frontend-dev context)
- High-level architectural decisions (use architect context)
- Comprehensive testing strategies (use testing context)
- General development practices

This context should guide performance analysis, optimization implementation, and performance monitoring setup for React applications.