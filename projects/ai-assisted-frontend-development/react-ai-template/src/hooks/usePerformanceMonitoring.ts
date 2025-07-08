/**
 * AI-Powered Performance Monitoring React Hook
 * 
 * This hook provides seamless integration of performance monitoring
 * into React components with AI-driven insights and optimization suggestions.
 */

import { useState, useEffect, useCallback, useRef } from 'react';
import { 
  PerformanceReport, 
  PerformanceMetrics,
  AISuggestion,
  measureRenderTime,
  subscribeToPerformanceReports,
  getPerformanceSummary,
  initializePerformanceMonitoring
} from '../utils/performance';

// Hook options interface
export interface UsePerformanceMonitoringOptions {
  /** Component name for tracking */
  componentName?: string;
  /** Enable automatic render time tracking */
  trackRenderTime?: boolean;
  /** Enable memory usage tracking */
  trackMemory?: boolean;
  /** Enable real-time suggestions */
  enableSuggestions?: boolean;
  /** Threshold for render time warnings (ms) */
  renderTimeThreshold?: number;
  /** Auto-initialize monitoring */
  autoInitialize?: boolean;
}

// Hook return interface
export interface UsePerformanceMonitoringReturn {
  /** Current performance metrics */
  metrics: PerformanceMetrics | null;
  /** Latest performance report */
  report: PerformanceReport | null;
  /** Performance grade (A-F) */
  grade: string;
  /** AI-generated suggestions */
  suggestions: AISuggestion[];
  /** Loading state */
  isLoading: boolean;
  /** Measure render time of a function */
  measureRender: <T>(fn: () => T) => { result: T; duration: number };
  /** Track async operation performance */
  trackAsync: <T>(operation: () => Promise<T>) => Promise<{ result: T; duration: number }>;
  /** Get performance summary */
  getSummary: () => { metrics: PerformanceMetrics; report: PerformanceReport };
  /** Force refresh performance data */
  refresh: () => void;
  /** Export performance data */
  exportData: () => string;
}

/**
 * Hook for AI-powered performance monitoring
 */
export function usePerformanceMonitoring(
  options: UsePerformanceMonitoringOptions = {}
): UsePerformanceMonitoringReturn {
  const {
    componentName = 'Component',
    trackRenderTime = true,
    trackMemory = true,
    enableSuggestions = true,
    renderTimeThreshold = 100,
    autoInitialize = true,
  } = options;

  // State
  const [metrics, setMetrics] = useState<PerformanceMetrics | null>(null);
  const [report, setReport] = useState<PerformanceReport | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  
  // Refs
  const renderCount = useRef(0);
  const componentMountTime = useRef<number>(Date.now());
  const lastRenderTime = useRef<number>(0);

  // Initialize monitoring
  useEffect(() => {
    if (autoInitialize) {
      initializePerformanceMonitoring({
        enableMemoryTracking: trackMemory,
        enableAI: enableSuggestions,
      });
    }
  }, [autoInitialize, trackMemory, enableSuggestions]);

  // Subscribe to performance reports
  useEffect(() => {
    const unsubscribe = subscribeToPerformanceReports((newReport) => {
      setReport(newReport);
      setMetrics(newReport.metrics);
      setIsLoading(false);
    });

    return unsubscribe;
  }, []);

  // Track component render time
  useEffect(() => {
    if (!trackRenderTime) return;

    const renderEndTime = performance.now();
    const renderDuration = renderEndTime - lastRenderTime.current;
    
    if (renderCount.current > 0 && renderDuration > 0) {
      console.log(`⚡ ${componentName} render #${renderCount.current}: ${renderDuration.toFixed(2)}ms`);
      
      if (renderDuration > renderTimeThreshold) {
        console.warn(`⚠️ Slow render detected for ${componentName}: ${renderDuration.toFixed(2)}ms`);
      }
    }
    
    renderCount.current++;
    lastRenderTime.current = performance.now();
  });

  // Measure render time of a function
  const measureRender = useCallback(<T>(fn: () => T): { result: T; duration: number } => {
    return measureRenderTime(componentName, fn);
  }, [componentName]);

  // Track async operation performance
  const trackAsync = useCallback(async <T>(
    operation: () => Promise<T>
  ): Promise<{ result: T; duration: number }> => {
    const startTime = performance.now();
    
    try {
      const result = await operation();
      const duration = performance.now() - startTime;
      
      console.log(`🌐 ${componentName} async operation: ${duration.toFixed(2)}ms`);
      
      return { result, duration };
    } catch (error) {
      const duration = performance.now() - startTime;
      console.error(`❌ ${componentName} async error: ${duration.toFixed(2)}ms`, error);
      throw error;
    }
  }, [componentName]);

  // Get performance summary
  const getSummary = useCallback(() => {
    return getPerformanceSummary();
  }, []);

  // Force refresh performance data
  const refresh = useCallback(() => {
    setIsLoading(true);
    const summary = getSummary();
    setMetrics(summary.metrics);
    setReport(summary.report);
    setIsLoading(false);
  }, [getSummary]);

  // Export performance data
  const exportData = useCallback(() => {
    const summary = getSummary();
    return JSON.stringify({
      component: componentName,
      mountTime: componentMountTime.current,
      renderCount: renderCount.current,
      ...summary,
    }, null, 2);
  }, [componentName, getSummary]);

  return {
    metrics,
    report,
    grade: report?.grade || 'N/A',
    suggestions: report?.suggestions || [],
    isLoading,
    measureRender,
    trackAsync,
    getSummary,
    refresh,
    exportData,
  };
}

/**
 * Hook for tracking specific performance metrics
 */
export function usePerformanceMetric(metricName: string) {
  const [value, setValue] = useState<number | null>(null);
  const [history, setHistory] = useState<number[]>([]);

  const track = useCallback((newValue: number) => {
    setValue(newValue);
    setHistory(prev => [...prev.slice(-9), newValue]); // Keep last 10 values
    
    console.log(`📊 ${metricName}: ${newValue}`);
  }, [metricName]);

  const getAverage = useCallback(() => {
    if (history.length === 0) return 0;
    return history.reduce((sum, val) => sum + val, 0) / history.length;
  }, [history]);

  const getTrend = useCallback(() => {
    if (history.length < 2) return 'stable';
    
    const recent = history.slice(-3);
    const earlier = history.slice(-6, -3);
    
    if (recent.length === 0 || earlier.length === 0) return 'stable';
    
    const recentAvg = recent.reduce((sum, val) => sum + val, 0) / recent.length;
    const earlierAvg = earlier.reduce((sum, val) => sum + val, 0) / earlier.length;
    
    const change = ((recentAvg - earlierAvg) / earlierAvg) * 100;
    
    if (change > 10) return 'degrading';
    if (change < -10) return 'improving';
    return 'stable';
  }, [history]);

  return {
    value,
    history,
    track,
    getAverage,
    getTrend,
  };
}

/**
 * Hook for API performance tracking
 */
export function useAPIPerformance() {
  const [requests, setRequests] = useState<Map<string, {
    duration: number;
    timestamp: number;
    status: 'success' | 'error';
  }>>(new Map());

  const trackRequest = useCallback(async <T>(
    endpoint: string,
    requestFn: () => Promise<T>
  ): Promise<T> => {
    const startTime = performance.now();
    
    try {
      const result = await requestFn();
      const duration = performance.now() - startTime;
      
      setRequests(prev => new Map(prev.set(endpoint, {
        duration,
        timestamp: Date.now(),
        status: 'success',
      })));
      
      console.log(`🌐 API ${endpoint}: ${duration.toFixed(2)}ms`);
      
      return result;
    } catch (error) {
      const duration = performance.now() - startTime;
      
      setRequests(prev => new Map(prev.set(endpoint, {
        duration,
        timestamp: Date.now(),
        status: 'error',
      })));
      
      console.error(`❌ API ${endpoint} error: ${duration.toFixed(2)}ms`, error);
      throw error;
    }
  }, []);

  const getRequestStats = useCallback((endpoint?: string) => {
    const relevantRequests = endpoint 
      ? [requests.get(endpoint)].filter(Boolean)
      : Array.from(requests.values());
    
    if (relevantRequests.length === 0) {
      return { average: 0, min: 0, max: 0, total: 0 };
    }
    
    const durations = relevantRequests.map(req => req!.duration);
    
    return {
      average: durations.reduce((sum, d) => sum + d, 0) / durations.length,
      min: Math.min(...durations),
      max: Math.max(...durations),
      total: relevantRequests.length,
    };
  }, [requests]);

  return {
    requests: Array.from(requests.entries()),
    trackRequest,
    getRequestStats,
  };
}

/**
 * Hook for memory usage tracking
 */
export function useMemoryTracking() {
  const [memoryUsage, setMemoryUsage] = useState<{
    used: number;
    total: number;
    percentage: number;
  } | null>(null);

  useEffect(() => {
    if (!('memory' in performance)) {
      console.warn('Memory API not supported');
      return;
    }

    const updateMemory = () => {
      const memory = (performance as any).memory;
      
      const used = memory.usedJSHeapSize / (1024 * 1024); // MB
      const total = memory.totalJSHeapSize / (1024 * 1024); // MB
      const percentage = (used / total) * 100;
      
      setMemoryUsage({ used, total, percentage });
    };

    // Update immediately
    updateMemory();
    
    // Update every 5 seconds
    const interval = setInterval(updateMemory, 5000);
    
    return () => clearInterval(interval);
  }, []);

  return memoryUsage;
}

/**
 * Hook for bundle size monitoring
 */
export function useBundleMonitoring() {
  const [bundleStats, setBundleStats] = useState<{
    size: number;
    gzipSize: number;
    loadTime: number;
  } | null>(null);

  useEffect(() => {
    // Get initial bundle stats from navigation timing
    const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
    
    if (navigation) {
      setBundleStats({
        size: navigation.transferSize || 0,
        gzipSize: navigation.encodedBodySize || 0,
        loadTime: navigation.loadEventEnd - navigation.loadEventStart,
      });
    }
  }, []);

  return bundleStats;
}

export default usePerformanceMonitoring;