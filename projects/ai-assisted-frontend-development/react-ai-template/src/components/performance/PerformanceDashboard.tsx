/**
 * AI-Powered Performance Dashboard Component
 * 
 * Real-time performance monitoring dashboard with AI insights and recommendations.
 * Displays Core Web Vitals, component performance, and optimization suggestions.
 */

import React, { useState, useEffect } from 'react';
import { 
  Activity, 
  Zap, 
  TrendingUp, 
  TrendingDown, 
  AlertTriangle, 
  CheckCircle,
  BarChart3,
  Clock,
  Download,
  RefreshCw,
  Lightbulb
} from 'lucide-react';
import { clsx } from 'clsx';

import usePerformanceMonitoring, { 
  useMemoryTracking, 
  useAPIPerformance,
  useBundleMonitoring 
} from '../../hooks/usePerformanceMonitoring';
import { PERFORMANCE_THRESHOLDS } from '../../utils/performance';

// Component props
export interface PerformanceDashboardProps {
  /** Show detailed metrics */
  showDetails?: boolean;
  /** Enable real-time updates */
  realTimeUpdates?: boolean;
  /** Show AI suggestions */
  showSuggestions?: boolean;
  /** Compact view */
  compact?: boolean;
  /** Custom CSS classes */
  className?: string;
}

/**
 * Performance Dashboard Component
 */
export const PerformanceDashboard: React.FC<PerformanceDashboardProps> = ({
  showDetails = true,
  realTimeUpdates = true,
  showSuggestions = true,
  compact = false,
  className
}) => {
  const [selectedTab, setSelectedTab] = useState<'overview' | 'vitals' | 'components' | 'suggestions'>('overview');
  const [autoRefresh, setAutoRefresh] = useState(realTimeUpdates);

  // Performance monitoring
  const { 
    metrics, 
    report, 
    grade, 
    suggestions, 
    isLoading, 
    refresh, 
    exportData 
  } = usePerformanceMonitoring({
    componentName: 'PerformanceDashboard',
    enableSuggestions: showSuggestions,
  });

  const memoryUsage = useMemoryTracking();
  const { requests, getRequestStats } = useAPIPerformance();
  const bundleStats = useBundleMonitoring();

  // Auto-refresh effect
  useEffect(() => {
    if (!autoRefresh) return;

    const interval = setInterval(() => {
      refresh();
    }, 5000); // Refresh every 5 seconds

    return () => clearInterval(interval);
  }, [autoRefresh, refresh]);

  // Handle export
  const handleExport = () => {
    const data = exportData();
    const blob = new Blob([data], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `performance-report-${new Date().toISOString().split('T')[0]}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  if (isLoading && !metrics) {
    return (
      <div className={clsx('flex items-center justify-center p-8', className)}>
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
        <span className="ml-2 text-gray-600">Loading performance data...</span>
      </div>
    );
  }

  return (
    <div className={clsx('bg-white rounded-lg shadow-lg', className)}>
      {/* Header */}
      <div className="border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Activity className="h-6 w-6 text-blue-500" />
            <h2 className="text-xl font-semibold text-gray-900">
              Performance Dashboard
            </h2>
            {grade && (
              <span className={clsx('px-2 py-1 rounded-full text-sm font-medium', {
                'bg-green-100 text-green-800': grade === 'A',
                'bg-blue-100 text-blue-800': grade === 'B',
                'bg-yellow-100 text-yellow-800': grade === 'C',
                'bg-orange-100 text-orange-800': grade === 'D',
                'bg-red-100 text-red-800': grade === 'F',
              })}>
                Grade {grade}
              </span>
            )}
          </div>
          
          <div className="flex items-center space-x-2">
            <button
              onClick={() => setAutoRefresh(!autoRefresh)}
              className={clsx('p-2 rounded-md transition-colors', {
                'bg-blue-100 text-blue-600': autoRefresh,
                'bg-gray-100 text-gray-600': !autoRefresh,
              })}
              title={autoRefresh ? 'Disable auto-refresh' : 'Enable auto-refresh'}
            >
              <RefreshCw className={clsx('h-4 w-4', { 'animate-spin': autoRefresh })} />
            </button>
            
            <button
              onClick={refresh}
              className="p-2 bg-gray-100 text-gray-600 rounded-md hover:bg-gray-200 transition-colors"
              title="Refresh data"
            >
              <RefreshCw className="h-4 w-4" />
            </button>
            
            <button
              onClick={handleExport}
              className="p-2 bg-gray-100 text-gray-600 rounded-md hover:bg-gray-200 transition-colors"
              title="Export data"
            >
              <Download className="h-4 w-4" />
            </button>
          </div>
        </div>

        {/* Tab Navigation */}
        {!compact && (
          <div className="mt-4">
            <nav className="flex space-x-4">
              {[
                { key: 'overview', label: 'Overview', icon: BarChart3 },
                { key: 'vitals', label: 'Core Web Vitals', icon: Zap },
                { key: 'components', label: 'Components', icon: Activity },
                { key: 'suggestions', label: 'AI Suggestions', icon: Lightbulb },
              ].map(tab => (
                <button
                  key={tab.key}
                  onClick={() => setSelectedTab(tab.key as any)}
                  className={clsx('flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-colors', {
                    'bg-blue-100 text-blue-700': selectedTab === tab.key,
                    'text-gray-500 hover:text-gray-700': selectedTab !== tab.key,
                  })}
                >
                  <tab.icon className="h-4 w-4" />
                  <span>{tab.label}</span>
                </button>
              ))}
            </nav>
          </div>
        )}
      </div>

      {/* Content */}
      <div className="p-6">
        {(compact || selectedTab === 'overview') && (
          <OverviewTab 
            metrics={metrics} 
            report={report} 
            memoryUsage={memoryUsage}
            bundleStats={bundleStats}
            compact={compact}
          />
        )}
        
        {!compact && selectedTab === 'vitals' && (
          <CoreWebVitalsTab metrics={metrics} />
        )}
        
        {!compact && selectedTab === 'components' && (
          <ComponentsTab requests={requests} getRequestStats={getRequestStats} />
        )}
        
        {!compact && selectedTab === 'suggestions' && showSuggestions && (
          <SuggestionsTab suggestions={suggestions} />
        )}
      </div>
    </div>
  );
};

/**
 * Overview Tab Component
 */
interface OverviewTabProps {
  metrics: any;
  report: any;
  memoryUsage: any;
  bundleStats: any;
  compact: boolean;
}

const OverviewTab: React.FC<OverviewTabProps> = ({ 
  metrics, 
  report, 
  memoryUsage, 
  bundleStats,
  compact 
}) => (
  <div className="space-y-6">
    {/* Key Metrics */}
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      <MetricCard
        title="LCP"
        value={metrics?.lcp}
        unit="ms"
        threshold={PERFORMANCE_THRESHOLDS.LCP}
        compact={compact}
      />
      <MetricCard
        title="FID"
        value={metrics?.fid}
        unit="ms"
        threshold={PERFORMANCE_THRESHOLDS.FID}
        compact={compact}
      />
      <MetricCard
        title="CLS"
        value={metrics?.cls}
        unit=""
        threshold={PERFORMANCE_THRESHOLDS.CLS}
        decimals={3}
        compact={compact}
      />
      <MetricCard
        title="TTFB"
        value={metrics?.ttfb}
        unit="ms"
        threshold={PERFORMANCE_THRESHOLDS.TTFB}
        compact={compact}
      />
    </div>

    {/* Performance Score */}
    {report && !compact && (
      <div className="bg-gray-50 rounded-lg p-4">
        <h3 className="text-lg font-medium text-gray-900 mb-4">Performance Scores</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <ScoreCard title="Overall" score={report.scores.overall} />
          <ScoreCard title="Core Web Vitals" score={report.scores.coreWebVitals} />
          <ScoreCard title="Loading" score={report.scores.loading} />
          <ScoreCard title="Interactivity" score={report.scores.interactivity} />
        </div>
      </div>
    )}

    {/* Resource Usage */}
    {(memoryUsage || bundleStats) && !compact && (
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {memoryUsage && (
          <div className="bg-gray-50 rounded-lg p-4">
            <h3 className="text-lg font-medium text-gray-900 mb-2">Memory Usage</h3>
            <div className="flex items-center justify-between">
              <span className="text-2xl font-bold text-gray-900">
                {memoryUsage.used.toFixed(1)} MB
              </span>
              <span className="text-sm text-gray-600">
                {memoryUsage.percentage.toFixed(1)}% of {memoryUsage.total.toFixed(1)} MB
              </span>
            </div>
            <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                style={{ width: `${Math.min(memoryUsage.percentage, 100)}%` }}
              />
            </div>
          </div>
        )}

        {bundleStats && (
          <div className="bg-gray-50 rounded-lg p-4">
            <h3 className="text-lg font-medium text-gray-900 mb-2">Bundle Stats</h3>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Size:</span>
                <span className="text-sm font-medium">{(bundleStats.size / 1024).toFixed(1)} KB</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Gzipped:</span>
                <span className="text-sm font-medium">{(bundleStats.gzipSize / 1024).toFixed(1)} KB</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-gray-600">Load Time:</span>
                <span className="text-sm font-medium">{bundleStats.loadTime.toFixed(0)} ms</span>
              </div>
            </div>
          </div>
        )}
      </div>
    )}
  </div>
);

/**
 * Core Web Vitals Tab Component
 */
const CoreWebVitalsTab: React.FC<{ metrics: any }> = ({ metrics }) => (
  <div className="space-y-6">
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <VitalCard
        title="Largest Contentful Paint (LCP)"
        description="Measures loading performance. Good LCP is 2.5s or less."
        value={metrics?.lcp}
        threshold={PERFORMANCE_THRESHOLDS.LCP}
        unit="ms"
      />
      <VitalCard
        title="First Input Delay (FID)"
        description="Measures interactivity. Good FID is 100ms or less."
        value={metrics?.fid}
        threshold={PERFORMANCE_THRESHOLDS.FID}
        unit="ms"
      />
      <VitalCard
        title="Cumulative Layout Shift (CLS)"
        description="Measures visual stability. Good CLS is 0.1 or less."
        value={metrics?.cls}
        threshold={PERFORMANCE_THRESHOLDS.CLS}
        unit=""
        decimals={3}
      />
      <VitalCard
        title="Time to First Byte (TTFB)"
        description="Measures server response time. Good TTFB is 800ms or less."
        value={metrics?.ttfb}
        threshold={PERFORMANCE_THRESHOLDS.TTFB}
        unit="ms"
      />
    </div>
  </div>
);

/**
 * Components Tab Component
 */
const ComponentsTab: React.FC<{ requests: any[]; getRequestStats: any }> = ({ 
  requests, 
  getRequestStats 
}) => {
  const stats = getRequestStats();
  
  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="text-lg font-medium text-gray-900">API Requests</h3>
          <p className="text-2xl font-bold text-blue-600">{stats.total}</p>
        </div>
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="text-lg font-medium text-gray-900">Average Response</h3>
          <p className="text-2xl font-bold text-blue-600">{stats.average.toFixed(0)}ms</p>
        </div>
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="text-lg font-medium text-gray-900">Slowest Request</h3>
          <p className="text-2xl font-bold text-blue-600">{stats.max.toFixed(0)}ms</p>
        </div>
      </div>

      {requests.length > 0 && (
        <div className="bg-gray-50 rounded-lg p-4">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Recent API Requests</h3>
          <div className="space-y-2">
            {requests.slice(-10).map(([endpoint, data], index) => (
              <div key={index} className="flex items-center justify-between py-2 border-b border-gray-200 last:border-0">
                <span className="text-sm font-medium text-gray-900 truncate">{endpoint}</span>
                <div className="flex items-center space-x-2">
                  <span className="text-sm text-gray-600">{data.duration.toFixed(0)}ms</span>
                  {data.status === 'success' ? (
                    <CheckCircle className="h-4 w-4 text-green-500" />
                  ) : (
                    <AlertTriangle className="h-4 w-4 text-red-500" />
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

/**
 * Suggestions Tab Component
 */
const SuggestionsTab: React.FC<{ suggestions: any[] }> = ({ suggestions }) => (
  <div className="space-y-4">
    {suggestions.length === 0 ? (
      <div className="text-center py-8">
        <Lightbulb className="h-12 w-12 text-gray-400 mx-auto mb-4" />
        <p className="text-gray-600">No optimization suggestions at this time.</p>
        <p className="text-sm text-gray-500 mt-2">Your application is performing well!</p>
      </div>
    ) : (
      suggestions.map((suggestion, index) => (
        <SuggestionCard key={index} suggestion={suggestion} />
      ))
    )}
  </div>
);

/**
 * Metric Card Component
 */
interface MetricCardProps {
  title: string;
  value?: number;
  unit: string;
  threshold: { good: number; poor: number };
  decimals?: number;
  compact?: boolean;
}

const MetricCard: React.FC<MetricCardProps> = ({ 
  title, 
  value, 
  unit, 
  threshold, 
  decimals = 0,
  compact = false 
}) => {
  const getStatus = () => {
    if (value === undefined) return 'unknown';
    if (value <= threshold.good) return 'good';
    if (value >= threshold.poor) return 'poor';
    return 'needs-improvement';
  };

  const status = getStatus();

  return (
    <div className="bg-gray-50 rounded-lg p-4">
      <div className="flex items-center justify-between">
        <h3 className={clsx('font-medium text-gray-900', {
          'text-sm': compact,
          'text-lg': !compact,
        })}>
          {title}
        </h3>
        {status === 'good' && <CheckCircle className="h-5 w-5 text-green-500" />}
        {status === 'needs-improvement' && <AlertTriangle className="h-5 w-5 text-yellow-500" />}
        {status === 'poor' && <AlertTriangle className="h-5 w-5 text-red-500" />}
      </div>
      <p className={clsx('font-bold', {
        'text-lg': compact,
        'text-2xl': !compact,
        'text-green-600': status === 'good',
        'text-yellow-600': status === 'needs-improvement',
        'text-red-600': status === 'poor',
        'text-gray-400': status === 'unknown',
      })}>
        {value !== undefined ? `${value.toFixed(decimals)}${unit}` : 'N/A'}
      </p>
      {!compact && (
        <p className="text-xs text-gray-500 mt-1">
          Target: ≤{threshold.good}{unit}
        </p>
      )}
    </div>
  );
};

/**
 * Score Card Component
 */
const ScoreCard: React.FC<{ title: string; score: number }> = ({ title, score }) => (
  <div className="text-center">
    <p className="text-sm text-gray-600">{title}</p>
    <p className={clsx('text-2xl font-bold', {
      'text-green-600': score >= 90,
      'text-blue-600': score >= 80 && score < 90,
      'text-yellow-600': score >= 70 && score < 80,
      'text-orange-600': score >= 60 && score < 70,
      'text-red-600': score < 60,
    })}>
      {score.toFixed(0)}
    </p>
  </div>
);

/**
 * Vital Card Component
 */
const VitalCard: React.FC<{
  title: string;
  description: string;
  value?: number;
  threshold: { good: number; poor: number };
  unit: string;
  decimals?: number;
}> = ({ title, description, value, threshold, unit, decimals = 0 }) => {
  const getStatus = () => {
    if (value === undefined) return 'unknown';
    if (value <= threshold.good) return 'good';
    if (value >= threshold.poor) return 'poor';
    return 'needs-improvement';
  };

  const status = getStatus();

  return (
    <div className="bg-gray-50 rounded-lg p-6">
      <div className="flex items-start justify-between">
        <div>
          <h3 className="text-lg font-medium text-gray-900">{title}</h3>
          <p className="text-sm text-gray-600 mt-1">{description}</p>
        </div>
        {status === 'good' && <CheckCircle className="h-6 w-6 text-green-500" />}
        {status === 'needs-improvement' && <AlertTriangle className="h-6 w-6 text-yellow-500" />}
        {status === 'poor' && <AlertTriangle className="h-6 w-6 text-red-500" />}
      </div>
      
      <div className="mt-4">
        <p className={clsx('text-3xl font-bold', {
          'text-green-600': status === 'good',
          'text-yellow-600': status === 'needs-improvement',
          'text-red-600': status === 'poor',
          'text-gray-400': status === 'unknown',
        })}>
          {value !== undefined ? `${value.toFixed(decimals)}${unit}` : 'N/A'}
        </p>
        <p className="text-sm text-gray-500 mt-1">
          Good: ≤{threshold.good}{unit} | Poor: ≥{threshold.poor}{unit}
        </p>
      </div>
    </div>
  );
};

/**
 * Suggestion Card Component
 */
const SuggestionCard: React.FC<{ suggestion: any }> = ({ suggestion }) => (
  <div className="bg-gray-50 rounded-lg p-4 border-l-4 border-l-blue-500">
    <div className="flex items-start justify-between">
      <div className="flex-1">
        <div className="flex items-center space-x-2">
          <h3 className="text-lg font-medium text-gray-900">{suggestion.title}</h3>
          <span className={clsx('px-2 py-1 rounded-full text-xs font-medium', {
            'bg-red-100 text-red-800': suggestion.priority === 'high',
            'bg-yellow-100 text-yellow-800': suggestion.priority === 'medium',
            'bg-blue-100 text-blue-800': suggestion.priority === 'low',
          })}>
            {suggestion.priority} priority
          </span>
        </div>
        <p className="text-sm text-gray-600 mt-1">{suggestion.description}</p>
        <p className="text-sm text-gray-700 mt-2">{suggestion.implementation}</p>
        
        {suggestion.codeExample && (
          <details className="mt-3">
            <summary className="text-sm font-medium text-blue-600 cursor-pointer">
              View code example
            </summary>
            <pre className="mt-2 p-3 bg-gray-900 text-gray-100 rounded-md text-xs overflow-x-auto">
              <code>{suggestion.codeExample}</code>
            </pre>
          </details>
        )}
      </div>
      
      <div className="ml-4 text-right">
        <p className="text-sm text-gray-600">Impact: {suggestion.impact}</p>
        <p className="text-sm text-gray-600">Effort: {suggestion.effort}</p>
      </div>
    </div>
  </div>
);

export default PerformanceDashboard;