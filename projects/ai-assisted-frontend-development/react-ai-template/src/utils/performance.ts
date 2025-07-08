/**
 * AI-Optimized Core Web Vitals Monitoring and Performance Utilities
 * 
 * This module provides comprehensive performance monitoring capabilities
 * specifically designed for AI-assisted React development with:
 * - Core Web Vitals tracking (LCP, FID, CLS, INP, TTFB)
 * - Real-time performance analytics
 * - AI-powered optimization suggestions
 * - Bundle size monitoring
 * - Memory usage tracking
 * - Component-level performance profiling
 */

import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

// Performance thresholds based on Core Web Vitals guidelines
export const PERFORMANCE_THRESHOLDS = {
  // Core Web Vitals
  LCP: { good: 2500, poor: 4000 }, // Largest Contentful Paint (ms)
  FID: { good: 100, poor: 300 },   // First Input Delay (ms)
  CLS: { good: 0.1, poor: 0.25 },  // Cumulative Layout Shift
  INP: { good: 200, poor: 500 },   // Interaction to Next Paint (ms)
  TTFB: { good: 800, poor: 1800 }, // Time to First Byte (ms)
  
  // Additional metrics
  FCP: { good: 1800, poor: 3000 }, // First Contentful Paint (ms)
  
  // Custom thresholds for AI development
  RENDER_TIME: 100,        // Component render time (ms)
  BUNDLE_SIZE: 512,        // Bundle size warning (KB)
  MEMORY_USAGE: 50,        // Memory usage warning (MB)
  API_RESPONSE: 1000,      // API response time (ms)
} as const;

// Performance metrics interface
export interface PerformanceMetrics {
  lcp?: number;
  fid?: number;
  cls?: number;
  inp?: number;
  ttfb?: number;
  fcp?: number;
  renderTime?: number;
  bundleSize?: number;
  memoryUsage?: number;
  timestamp: number;
  url: string;
  userAgent: string;
}

// Performance report interface
export interface PerformanceReport {
  metrics: PerformanceMetrics;
  scores: PerformanceScores;
  suggestions: AISuggestion[];
  grade: PerformanceGrade;
  improvements: ImprovementArea[];
}

// Performance scores
export interface PerformanceScores {
  overall: number;
  coreWebVitals: number;
  rendering: number;
  loading: number;
  interactivity: number;
}

// AI suggestion interface
export interface AISuggestion {
  category: 'loading' | 'rendering' | 'interactivity' | 'memory' | 'bundle';
  priority: 'high' | 'medium' | 'low';
  title: string;
  description: string;
  impact: string;
  effort: 'low' | 'medium' | 'high';
  implementation: string;
  codeExample?: string;
}

// Performance grade
export type PerformanceGrade = 'A' | 'B' | 'C' | 'D' | 'F';

// Improvement areas
export interface ImprovementArea {
  metric: string;
  current: number;
  target: number;
  improvement: number;
  actions: string[];
}

// Global performance state
let performanceState = {
  metrics: new Map<string, PerformanceMetrics>(),
  isMonitoring: false,
  observers: new Set<(report: PerformanceReport) => void>(),
  config: {
    autoReport: true,
    reportInterval: 30000, // 30 seconds
    enableAI: true,
    enableMemoryTracking: true,
    enableBundleTracking: true,
  },
};

/**
 * Initialize Core Web Vitals monitoring
 */
export function initializePerformanceMonitoring(config?: Partial<typeof performanceState.config>): void {
  if (performanceState.isMonitoring) {
    console.warn('Performance monitoring is already initialized');
    return;
  }

  // Update configuration
  performanceState.config = { ...performanceState.config, ...config };
  performanceState.isMonitoring = true;

  console.log('🚀 Initializing AI-powered performance monitoring...');

  // Initialize Core Web Vitals collection
  getCLS(onCLS);
  getFID(onFID);
  getFCP(onFCP);
  getLCP(onLCP);
  getTTFB(onTTFB);

  // Initialize additional monitoring
  if (performanceState.config.enableMemoryTracking) {
    startMemoryMonitoring();
  }

  if (performanceState.config.enableBundleTracking) {
    trackBundleSize();
  }

  // Start automatic reporting
  if (performanceState.config.autoReport) {
    startAutoReporting();
  }

  console.log('✅ Performance monitoring initialized');
}

/**
 * Core Web Vitals handlers
 */
function onCLS(metric: any): void {
  updateMetric('cls', metric.value);
  console.log(`📊 CLS: ${metric.value.toFixed(4)}`);
}

function onFID(metric: any): void {
  updateMetric('fid', metric.value);
  console.log(`📊 FID: ${metric.value.toFixed(2)}ms`);
}

function onFCP(metric: any): void {
  updateMetric('fcp', metric.value);
  console.log(`📊 FCP: ${metric.value.toFixed(2)}ms`);
}

function onLCP(metric: any): void {
  updateMetric('lcp', metric.value);
  console.log(`📊 LCP: ${metric.value.toFixed(2)}ms`);
}

function onTTFB(metric: any): void {
  updateMetric('ttfb', metric.value);
  console.log(`📊 TTFB: ${metric.value.toFixed(2)}ms`);
}

/**
 * Update performance metric
 */
function updateMetric(metric: keyof PerformanceMetrics, value: number): void {
  const currentMetrics = getCurrentMetrics();
  (currentMetrics as any)[metric] = value;
  
  performanceState.metrics.set(window.location.pathname, currentMetrics);
  
  // Generate report if AI is enabled
  if (performanceState.config.enableAI) {
    const report = generatePerformanceReport(currentMetrics);
    notifyObservers(report);
  }
}

/**
 * Get current performance metrics
 */
function getCurrentMetrics(): PerformanceMetrics {
  const existing = performanceState.metrics.get(window.location.pathname);
  
  return existing || {
    timestamp: Date.now(),
    url: window.location.href,
    userAgent: navigator.userAgent,
  };
}

/**
 * Measure component render time
 */
export function measureRenderTime<T>(
  componentName: string,
  renderFunction: () => T
): { result: T; duration: number } {
  const startTime = performance.now();
  const result = renderFunction();
  const duration = performance.now() - startTime;
  
  console.log(`⚡ ${componentName} render time: ${duration.toFixed(2)}ms`);
  
  // Update metrics
  updateMetric('renderTime', duration);
  
  // Check for performance issues
  if (duration > PERFORMANCE_THRESHOLDS.RENDER_TIME) {
    console.warn(`⚠️ Slow render detected for ${componentName}: ${duration.toFixed(2)}ms`);
    generateRenderOptimizationSuggestions(componentName, duration);
  }
  
  return { result, duration };
}

/**
 * Track API performance
 */
export async function trackAPIPerformance<T>(
  endpoint: string,
  apiCall: () => Promise<T>
): Promise<{ result: T; duration: number; size?: number }> {
  const startTime = performance.now();
  
  try {
    const result = await apiCall();
    const duration = performance.now() - startTime;
    
    console.log(`🌐 API ${endpoint}: ${duration.toFixed(2)}ms`);
    
    // Estimate response size
    const size = new Blob([JSON.stringify(result)]).size;
    
    if (duration > PERFORMANCE_THRESHOLDS.API_RESPONSE) {
      console.warn(`⚠️ Slow API response: ${endpoint} (${duration.toFixed(2)}ms)`);
    }
    
    return { result, duration, size };
  } catch (error) {
    const duration = performance.now() - startTime;
    console.error(`❌ API error ${endpoint}: ${duration.toFixed(2)}ms`, error);
    throw error;
  }
}

/**
 * Start memory monitoring
 */
function startMemoryMonitoring(): void {
  if (!('memory' in performance)) {
    console.warn('Memory monitoring not supported in this browser');
    return;
  }

  const checkMemory = () => {
    const memory = (performance as any).memory;
    const memoryUsage = memory.usedJSHeapSize / (1024 * 1024); // MB
    
    updateMetric('memoryUsage', memoryUsage);
    
    if (memoryUsage > PERFORMANCE_THRESHOLDS.MEMORY_USAGE) {
      console.warn(`⚠️ High memory usage: ${memoryUsage.toFixed(2)}MB`);
    }
  };

  // Check memory every 10 seconds
  setInterval(checkMemory, 10000);
  checkMemory(); // Initial check
}

/**
 * Track bundle size
 */
function trackBundleSize(): void {
  // Estimate bundle size from navigation timing
  const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
  
  if (navigation) {
    const bundleSize = navigation.transferSize ? navigation.transferSize / 1024 : 0; // KB
    updateMetric('bundleSize', bundleSize);
    
    if (bundleSize > PERFORMANCE_THRESHOLDS.BUNDLE_SIZE) {
      console.warn(`⚠️ Large bundle size: ${bundleSize.toFixed(2)}KB`);
    }
  }
}

/**
 * Start automatic reporting
 */
function startAutoReporting(): void {
  setInterval(() => {
    const currentMetrics = getCurrentMetrics();
    const report = generatePerformanceReport(currentMetrics);
    
    console.group('📊 Performance Report');
    console.log('Metrics:', currentMetrics);
    console.log('Grade:', report.grade);
    console.log('Suggestions:', report.suggestions.length);
    console.groupEnd();
  }, performanceState.config.reportInterval);
}

/**
 * Generate comprehensive performance report with AI insights
 */
export function generatePerformanceReport(metrics: PerformanceMetrics): PerformanceReport {
  const scores = calculatePerformanceScores(metrics);
  const suggestions = generateAISuggestions(metrics, scores);
  const grade = calculatePerformanceGrade(scores.overall);
  const improvements = identifyImprovementAreas(metrics);
  
  return {
    metrics,
    scores,
    suggestions,
    grade,
    improvements,
  };
}

/**
 * Calculate performance scores
 */
function calculatePerformanceScores(metrics: PerformanceMetrics): PerformanceScores {
  const lcpScore = metrics.lcp ? scoreMetric(metrics.lcp, PERFORMANCE_THRESHOLDS.LCP) : 100;
  const fidScore = metrics.fid ? scoreMetric(metrics.fid, PERFORMANCE_THRESHOLDS.FID) : 100;
  const clsScore = metrics.cls ? scoreMetric(metrics.cls, PERFORMANCE_THRESHOLDS.CLS) : 100;
  const ttfbScore = metrics.ttfb ? scoreMetric(metrics.ttfb, PERFORMANCE_THRESHOLDS.TTFB) : 100;
  const fcpScore = metrics.fcp ? scoreMetric(metrics.fcp, PERFORMANCE_THRESHOLDS.FCP) : 100;
  
  const coreWebVitals = (lcpScore + fidScore + clsScore) / 3;
  const loading = (lcpScore + fcpScore + ttfbScore) / 3;
  const interactivity = fidScore;
  const rendering = metrics.renderTime ? scoreMetric(metrics.renderTime, { good: 16, poor: 100 }) : 100;
  
  const overall = (coreWebVitals * 0.5) + (loading * 0.2) + (interactivity * 0.2) + (rendering * 0.1);
  
  return {
    overall,
    coreWebVitals,
    rendering,
    loading,
    interactivity,
  };
}

/**
 * Score individual metric
 */
function scoreMetric(value: number, thresholds: { good: number; poor: number }): number {
  if (value <= thresholds.good) return 100;
  if (value >= thresholds.poor) return 0;
  
  // Linear interpolation between good and poor
  const range = thresholds.poor - thresholds.good;
  const position = value - thresholds.good;
  return Math.max(0, 100 - (position / range) * 100);
}

/**
 * Calculate performance grade
 */
function calculatePerformanceGrade(score: number): PerformanceGrade {
  if (score >= 90) return 'A';
  if (score >= 80) return 'B';
  if (score >= 70) return 'C';
  if (score >= 60) return 'D';
  return 'F';
}

/**
 * Generate AI-powered optimization suggestions
 */
function generateAISuggestions(metrics: PerformanceMetrics, scores: PerformanceScores): AISuggestion[] {
  const suggestions: AISuggestion[] = [];
  
  // LCP optimization
  if (metrics.lcp && metrics.lcp > PERFORMANCE_THRESHOLDS.LCP.good) {
    suggestions.push({
      category: 'loading',
      priority: 'high',
      title: 'Optimize Largest Contentful Paint (LCP)',
      description: `LCP is ${metrics.lcp.toFixed(0)}ms, which exceeds the recommended ${PERFORMANCE_THRESHOLDS.LCP.good}ms threshold.`,
      impact: 'Improves user perception of loading speed',
      effort: 'medium',
      implementation: 'Optimize images, preload critical resources, improve server response times',
      codeExample: `
// Preload critical images
<link rel="preload" as="image" href="/hero-image.jpg" />

// Use responsive images
<img 
  src="/hero-small.jpg"
  srcSet="/hero-small.jpg 480w, /hero-large.jpg 1200w"
  sizes="(max-width: 768px) 480px, 1200px"
  loading="eager"
  alt="Hero image"
/>`,
    });
  }
  
  // FID optimization
  if (metrics.fid && metrics.fid > PERFORMANCE_THRESHOLDS.FID.good) {
    suggestions.push({
      category: 'interactivity',
      priority: 'high',
      title: 'Reduce First Input Delay (FID)',
      description: `FID is ${metrics.fid.toFixed(0)}ms, users may experience delayed interactions.`,
      impact: 'Improves responsiveness to user interactions',
      effort: 'medium',
      implementation: 'Break up long tasks, defer non-critical JavaScript, use web workers',
      codeExample: `
// Break up long tasks
const processLargeArray = async (items) => {
  const chunks = chunkArray(items, 100);
  
  for (const chunk of chunks) {
    await new Promise(resolve => {
      processChunk(chunk);
      setTimeout(resolve, 0); // Yield to browser
    });
  }
};`,
    });
  }
  
  // CLS optimization
  if (metrics.cls && metrics.cls > PERFORMANCE_THRESHOLDS.CLS.good) {
    suggestions.push({
      category: 'rendering',
      priority: 'medium',
      title: 'Reduce Cumulative Layout Shift (CLS)',
      description: `CLS is ${metrics.cls.toFixed(3)}, indicating visual instability.`,
      impact: 'Prevents unexpected layout shifts that frustrate users',
      effort: 'low',
      implementation: 'Add size attributes to images, reserve space for dynamic content',
      codeExample: `
// Reserve space for images
<img 
  src="/image.jpg"
  width="400"
  height="300"
  style={{ aspectRatio: '4/3' }}
  alt="Content image"
/>

// Reserve space for dynamic content
<div style={{ minHeight: '200px' }}>
  {loading ? <LoadingSpinner /> : <DynamicContent />}
</div>`,
    });
  }
  
  // Render time optimization
  if (metrics.renderTime && metrics.renderTime > PERFORMANCE_THRESHOLDS.RENDER_TIME) {
    suggestions.push({
      category: 'rendering',
      priority: 'medium',
      title: 'Optimize Component Render Time',
      description: `Component render time is ${metrics.renderTime.toFixed(2)}ms, consider optimization.`,
      impact: 'Improves component responsiveness and user experience',
      effort: 'medium',
      implementation: 'Use React.memo, useMemo, useCallback, and optimize re-renders',
      codeExample: `
// Memoize expensive computations
const ExpensiveComponent = React.memo(({ data }) => {
  const processedData = useMemo(() => 
    expensiveDataProcessing(data), [data]
  );
  
  const handleClick = useCallback((id) => {
    onItemClick(id);
  }, [onItemClick]);
  
  return <div>{/* render with processedData */}</div>;
});`,
    });
  }
  
  // Bundle size optimization
  if (metrics.bundleSize && metrics.bundleSize > PERFORMANCE_THRESHOLDS.BUNDLE_SIZE) {
    suggestions.push({
      category: 'bundle',
      priority: 'medium',
      title: 'Reduce Bundle Size',
      description: `Bundle size is ${metrics.bundleSize.toFixed(0)}KB, consider optimization.`,
      impact: 'Reduces initial loading time and improves cache efficiency',
      effort: 'high',
      implementation: 'Implement code splitting, tree shaking, and dynamic imports',
      codeExample: `
// Dynamic import for code splitting
const LazyComponent = React.lazy(() => 
  import('./LazyComponent')
);

// Use with Suspense
<Suspense fallback={<LoadingSpinner />}>
  <LazyComponent />
</Suspense>`,
    });
  }
  
  // Memory optimization
  if (metrics.memoryUsage && metrics.memoryUsage > PERFORMANCE_THRESHOLDS.MEMORY_USAGE) {
    suggestions.push({
      category: 'memory',
      priority: 'high',
      title: 'Optimize Memory Usage',
      description: `Memory usage is ${metrics.memoryUsage.toFixed(1)}MB, check for memory leaks.`,
      impact: 'Prevents browser slowdown and crashes',
      effort: 'high',
      implementation: 'Clean up event listeners, clear timers, optimize data structures',
      codeExample: `
// Clean up in useEffect
useEffect(() => {
  const timer = setInterval(updateData, 1000);
  const listener = (e) => handleResize(e);
  
  window.addEventListener('resize', listener);
  
  return () => {
    clearInterval(timer);
    window.removeEventListener('resize', listener);
  };
}, []);`,
    });
  }
  
  return suggestions.sort((a, b) => {
    const priorityOrder = { high: 3, medium: 2, low: 1 };
    return priorityOrder[b.priority] - priorityOrder[a.priority];
  });
}

/**
 * Generate render optimization suggestions
 */
function generateRenderOptimizationSuggestions(componentName: string, duration: number): void {
  console.group(`🔧 Optimization suggestions for ${componentName}`);
  console.log(`Render time: ${duration.toFixed(2)}ms (target: <${PERFORMANCE_THRESHOLDS.RENDER_TIME}ms)`);
  console.log('Suggestions:');
  console.log('1. Use React.memo() to prevent unnecessary re-renders');
  console.log('2. Move expensive calculations to useMemo()');
  console.log('3. Optimize props drilling with useCallback()');
  console.log('4. Consider component splitting for complex components');
  console.log('5. Profile with React DevTools Profiler');
  console.groupEnd();
}

/**
 * Identify improvement areas
 */
function identifyImprovementAreas(metrics: PerformanceMetrics): ImprovementArea[] {
  const improvements: ImprovementArea[] = [];
  
  if (metrics.lcp && metrics.lcp > PERFORMANCE_THRESHOLDS.LCP.good) {
    improvements.push({
      metric: 'Largest Contentful Paint',
      current: metrics.lcp,
      target: PERFORMANCE_THRESHOLDS.LCP.good,
      improvement: metrics.lcp - PERFORMANCE_THRESHOLDS.LCP.good,
      actions: [
        'Optimize images and use WebP format',
        'Preload critical resources',
        'Improve server response times',
        'Use a CDN for static assets',
      ],
    });
  }
  
  if (metrics.fid && metrics.fid > PERFORMANCE_THRESHOLDS.FID.good) {
    improvements.push({
      metric: 'First Input Delay',
      current: metrics.fid,
      target: PERFORMANCE_THRESHOLDS.FID.good,
      improvement: metrics.fid - PERFORMANCE_THRESHOLDS.FID.good,
      actions: [
        'Break up long-running tasks',
        'Defer non-critical JavaScript',
        'Use web workers for heavy computations',
        'Optimize third-party scripts',
      ],
    });
  }
  
  if (metrics.cls && metrics.cls > PERFORMANCE_THRESHOLDS.CLS.good) {
    improvements.push({
      metric: 'Cumulative Layout Shift',
      current: metrics.cls,
      target: PERFORMANCE_THRESHOLDS.CLS.good,
      improvement: metrics.cls - PERFORMANCE_THRESHOLDS.CLS.good,
      actions: [
        'Add dimensions to images and videos',
        'Reserve space for ads and embeds',
        'Avoid inserting content above existing content',
        'Use CSS aspect-ratio for responsive media',
      ],
    });
  }
  
  return improvements;
}

/**
 * Subscribe to performance reports
 */
export function subscribeToPerformanceReports(callback: (report: PerformanceReport) => void): () => void {
  performanceState.observers.add(callback);
  
  return () => {
    performanceState.observers.delete(callback);
  };
}

/**
 * Notify observers of performance reports
 */
function notifyObservers(report: PerformanceReport): void {
  performanceState.observers.forEach(callback => {
    try {
      callback(report);
    } catch (error) {
      console.error('Error in performance report observer:', error);
    }
  });
}

/**
 * Get current performance summary
 */
export function getPerformanceSummary(): {
  metrics: PerformanceMetrics;
  report: PerformanceReport;
} {
  const metrics = getCurrentMetrics();
  const report = generatePerformanceReport(metrics);
  
  return { metrics, report };
}

/**
 * Export performance data for analysis
 */
export function exportPerformanceData(): string {
  const allMetrics = Array.from(performanceState.metrics.entries()).map(([path, metrics]) => ({
    path,
    ...metrics,
    report: generatePerformanceReport(metrics),
  }));
  
  return JSON.stringify({
    timestamp: new Date().toISOString(),
    userAgent: navigator.userAgent,
    config: performanceState.config,
    data: allMetrics,
  }, null, 2);
}

/**
 * Reset performance monitoring
 */
export function resetPerformanceMonitoring(): void {
  performanceState.metrics.clear();
  performanceState.observers.clear();
  performanceState.isMonitoring = false;
  
  console.log('🔄 Performance monitoring reset');
}

// Auto-initialize in browser environment
if (typeof window !== 'undefined' && !performanceState.isMonitoring) {
  // Initialize after DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      initializePerformanceMonitoring();
    });
  } else {
    initializePerformanceMonitoring();
  }
}

export default {
  initializePerformanceMonitoring,
  measureRenderTime,
  trackAPIPerformance,
  generatePerformanceReport,
  subscribeToPerformanceReports,
  getPerformanceSummary,
  exportPerformanceData,
  resetPerformanceMonitoring,
  PERFORMANCE_THRESHOLDS,
};