/**
 * AI-Powered Optimization Workflow Example
 * 
 * This example demonstrates how AI can automatically analyze and optimize
 * React applications for performance, accessibility, and code quality.
 */

import React, { useState, useEffect, useCallback } from 'react';
import { 
  Zap, 
  TrendingUp, 
  Code, 
  Eye, 
  Shield, 
  BarChart3,
  Target,
  Cpu,
  HardDrive,
  Wifi,
  AlertTriangle,
  CheckCircle,
  Clock,
  Lightbulb
} from 'lucide-react';

// Optimization interfaces
export interface OptimizationMetric {
  id: string;
  name: string;
  current: number;
  target: number;
  unit: string;
  status: 'excellent' | 'good' | 'needs_improvement' | 'poor';
  trend: 'improving' | 'stable' | 'degrading';
}

export interface OptimizationSuggestion {
  id: string;
  category: 'performance' | 'accessibility' | 'security' | 'code_quality' | 'bundle';
  priority: 'critical' | 'high' | 'medium' | 'low';
  title: string;
  description: string;
  impact: string;
  effort: 'low' | 'medium' | 'high';
  automatable: boolean;
  implementation: string;
  codeExample?: string;
  estimatedImprovement: string;
}

export interface OptimizationReport {
  timestamp: string;
  overallScore: number;
  metrics: OptimizationMetric[];
  suggestions: OptimizationSuggestion[];
  appliedOptimizations: string[];
  nextSteps: string[];
}

export interface AIOptimizationWorkflowProps {
  /** Component to analyze */
  targetComponent?: string;
  /** Enable real-time analysis */
  realTimeAnalysis?: boolean;
  /** Auto-apply safe optimizations */
  autoApply?: boolean;
  /** Custom CSS classes */
  className?: string;
}

/**
 * AI Optimization Workflow Component
 * 
 * Demonstrates how AI can automatically:
 * 1. Analyze application performance and code quality
 * 2. Identify optimization opportunities
 * 3. Generate specific improvement suggestions
 * 4. Apply safe optimizations automatically
 * 5. Monitor improvement results
 */
export const AIOptimizationWorkflow: React.FC<AIOptimizationWorkflowProps> = ({
  targetComponent = 'SearchableProductList',
  realTimeAnalysis = true,
  autoApply = false,
  className = '',
}) => {
  // State management
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [report, setReport] = useState<OptimizationReport | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [appliedOptimizations, setAppliedOptimizations] = useState<string[]>([]);

  // Mock data for demonstration
  const mockMetrics: OptimizationMetric[] = [
    {
      id: 'lcp',
      name: 'Largest Contentful Paint',
      current: 2.8,
      target: 2.5,
      unit: 's',
      status: 'needs_improvement',
      trend: 'stable',
    },
    {
      id: 'fid',
      name: 'First Input Delay',
      current: 95,
      target: 100,
      unit: 'ms',
      status: 'good',
      trend: 'improving',
    },
    {
      id: 'cls',
      name: 'Cumulative Layout Shift',
      current: 0.08,
      target: 0.1,
      unit: '',
      status: 'excellent',
      trend: 'stable',
    },
    {
      id: 'bundle_size',
      name: 'Bundle Size',
      current: 687,
      target: 500,
      unit: 'KB',
      status: 'needs_improvement',
      trend: 'degrading',
    },
    {
      id: 'accessibility_score',
      name: 'Accessibility Score',
      current: 94,
      target: 100,
      unit: '%',
      status: 'good',
      trend: 'improving',
    },
    {
      id: 'code_coverage',
      name: 'Test Coverage',
      current: 87,
      target: 90,
      unit: '%',
      status: 'good',
      trend: 'stable',
    },
  ];

  const mockSuggestions: OptimizationSuggestion[] = [
    {
      id: 'image_optimization',
      category: 'performance',
      priority: 'high',
      title: 'Optimize Image Loading',
      description: 'Images are not optimized and lack modern formats',
      impact: 'Reduces LCP by ~400ms and bundle size by ~150KB',
      effort: 'medium',
      automatable: true,
      implementation: 'Convert to WebP, add responsive images, implement lazy loading',
      estimatedImprovement: '15% faster loading',
      codeExample: `
// Before
<img src="/large-image.jpg" alt="Product" />

// After (AI-optimized)
<img 
  src="/large-image.webp"
  srcSet="/large-image-480.webp 480w, /large-image-800.webp 800w"
  sizes="(max-width: 768px) 480px, 800px"
  loading="lazy"
  alt="Product"
/>`,
    },
    {
      id: 'code_splitting',
      category: 'performance',
      priority: 'high',
      title: 'Implement Route-Based Code Splitting',
      description: 'Bundle contains unused code that increases initial load time',
      impact: 'Reduces initial bundle by ~200KB',
      effort: 'low',
      automatable: true,
      implementation: 'Split routes with React.lazy() and dynamic imports',
      estimatedImprovement: '25% faster initial load',
      codeExample: `
// AI-generated code splitting
const LazyProductList = React.lazy(() => 
  import('./components/SearchableProductList')
);

// Route setup
<Suspense fallback={<LoadingSpinner />}>
  <Routes>
    <Route path="/products" element={<LazyProductList />} />
  </Routes>
</Suspense>`,
    },
    {
      id: 'memo_optimization',
      category: 'performance',
      priority: 'medium',
      title: 'Add React Memoization',
      description: 'Components re-render unnecessarily due to missing memoization',
      impact: 'Reduces re-renders by ~40%',
      effort: 'low',
      automatable: true,
      implementation: 'Add React.memo, useMemo, and useCallback optimizations',
      estimatedImprovement: '30% fewer re-renders',
      codeExample: `
// AI-optimized component
const ProductCard = React.memo(({ product, onSelect }) => {
  const handleClick = useCallback(() => {
    onSelect(product.id);
  }, [product.id, onSelect]);

  const formattedPrice = useMemo(() => 
    new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD'
    }).format(product.price)
  , [product.price]);

  return (
    <div onClick={handleClick}>
      {/* Component content */}
      <span>{formattedPrice}</span>
    </div>
  );
});`,
    },
    {
      id: 'accessibility_improvements',
      category: 'accessibility',
      priority: 'medium',
      title: 'Enhance Keyboard Navigation',
      description: 'Some interactive elements lack proper keyboard support',
      impact: 'Improves accessibility score to 98%',
      effort: 'low',
      automatable: true,
      implementation: 'Add proper ARIA attributes and keyboard event handlers',
      estimatedImprovement: '4% accessibility improvement',
      codeExample: `
// AI-enhanced accessibility
<div
  role="button"
  tabIndex={0}
  aria-label="Select product"
  onKeyDown={(e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      handleProductSelect();
    }
  }}
>
  {/* Content */}
</div>`,
    },
    {
      id: 'error_boundaries',
      category: 'code_quality',
      priority: 'medium',
      title: 'Add Error Boundaries',
      description: 'Components lack error boundaries for graceful failure handling',
      impact: 'Improves application stability and user experience',
      effort: 'low',
      automatable: true,
      implementation: 'Add error boundaries around key components',
      estimatedImprovement: 'Better error handling',
      codeExample: `
// AI-generated error boundary
class ProductListErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-fallback">
          <h3>Something went wrong loading products</h3>
          <button onClick={() => window.location.reload()}>
            Retry
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}`,
    },
  ];

  // Run optimization analysis
  const runAnalysis = useCallback(async () => {
    setIsAnalyzing(true);
    
    // Simulate AI analysis
    await new Promise(resolve => setTimeout(resolve, 3000));
    
    const newReport: OptimizationReport = {
      timestamp: new Date().toISOString(),
      overallScore: 78,
      metrics: mockMetrics,
      suggestions: mockSuggestions,
      appliedOptimizations,
      nextSteps: [
        'Implement high-priority performance optimizations',
        'Set up automated performance monitoring',
        'Create performance budgets for CI/CD',
        'Schedule regular optimization reviews',
      ],
    };
    
    setReport(newReport);
    setIsAnalyzing(false);
  }, [appliedOptimizations]);

  // Apply optimization
  const applyOptimization = useCallback(async (suggestion: OptimizationSuggestion) => {
    if (!suggestion.automatable) {
      alert('This optimization requires manual implementation');
      return;
    }

    // Simulate applying optimization
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    setAppliedOptimizations(prev => [...prev, suggestion.id]);
    
    // Update metrics to reflect improvement
    if (report) {
      const updatedMetrics = report.metrics.map(metric => {
        if (suggestion.id === 'image_optimization' && metric.id === 'lcp') {
          return { ...metric, current: metric.current - 0.4, status: 'good' as const };
        }
        if (suggestion.id === 'code_splitting' && metric.id === 'bundle_size') {
          return { ...metric, current: metric.current - 200, status: 'good' as const };
        }
        return metric;
      });

      setReport(prev => prev ? {
        ...prev,
        metrics: updatedMetrics,
        overallScore: prev.overallScore + 5,
      } : null);
    }
  }, [report]);

  // Auto-run analysis on mount
  useEffect(() => {
    if (realTimeAnalysis) {
      runAnalysis();
    }
  }, [realTimeAnalysis, runAnalysis]);

  // Filter suggestions by category
  const filteredSuggestions = report?.suggestions.filter(s => 
    selectedCategory === 'all' || s.category === selectedCategory
  ) || [];

  return (
    <div className={`bg-white rounded-lg shadow-lg p-6 ${className}`}>
      {/* Header */}
      <div className="border-b border-gray-200 pb-4 mb-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Zap className="h-8 w-8 text-yellow-500" />
            <div>
              <h2 className="text-2xl font-bold text-gray-900">AI Optimization Workflow</h2>
              <p className="text-gray-600">Target: {targetComponent}</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <button
              onClick={runAnalysis}
              disabled={isAnalyzing}
              className="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400 text-white px-4 py-2 rounded-lg font-medium transition-colors flex items-center space-x-2"
            >
              {isAnalyzing ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  <span>Analyzing...</span>
                </>
              ) : (
                <>
                  <BarChart3 className="h-4 w-4" />
                  <span>Run Analysis</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Overall Score */}
        {report && (
          <div className="mt-4 flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <span className="text-sm font-medium text-gray-700">Overall Score:</span>
              <div className={`text-2xl font-bold ${
                report.overallScore >= 90 ? 'text-green-600' :
                report.overallScore >= 70 ? 'text-yellow-600' :
                'text-red-600'
              }`}>
                {report.overallScore}/100
              </div>
            </div>
            <div className="text-sm text-gray-500">
              Last updated: {new Date(report.timestamp).toLocaleTimeString()}
            </div>
          </div>
        )}
      </div>

      {/* Content */}
      {report ? (
        <div className="space-y-6">
          {/* Metrics Grid */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Performance Metrics</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {report.metrics.map(metric => (
                <MetricCard key={metric.id} metric={metric} />
              ))}
            </div>
          </div>

          {/* Optimization Suggestions */}
          <div>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">AI Optimization Suggestions</h3>
              
              {/* Category Filter */}
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="px-3 py-2 border border-gray-300 rounded-md text-sm"
              >
                <option value="all">All Categories</option>
                <option value="performance">Performance</option>
                <option value="accessibility">Accessibility</option>
                <option value="security">Security</option>
                <option value="code_quality">Code Quality</option>
                <option value="bundle">Bundle</option>
              </select>
            </div>

            <div className="space-y-4">
              {filteredSuggestions.map(suggestion => (
                <SuggestionCard
                  key={suggestion.id}
                  suggestion={suggestion}
                  onApply={() => applyOptimization(suggestion)}
                  isApplied={appliedOptimizations.includes(suggestion.id)}
                />
              ))}
            </div>
          </div>

          {/* Applied Optimizations */}
          {appliedOptimizations.length > 0 && (
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Applied Optimizations</h3>
              <div className="space-y-2">
                {appliedOptimizations.map(optId => {
                  const suggestion = mockSuggestions.find(s => s.id === optId);
                  return suggestion ? (
                    <div key={optId} className="flex items-center space-x-2 text-sm text-green-700 bg-green-50 p-2 rounded">
                      <CheckCircle className="h-4 w-4" />
                      <span>{suggestion.title}</span>
                      <span className="text-green-600">({suggestion.estimatedImprovement})</span>
                    </div>
                  ) : null;
                })}
              </div>
            </div>
          )}

          {/* Next Steps */}
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Recommended Next Steps</h3>
            <ul className="space-y-2">
              {report.nextSteps.map((step, index) => (
                <li key={index} className="flex items-start space-x-2">
                  <Target className="h-5 w-5 text-blue-500 mt-0.5" />
                  <span className="text-gray-700">{step}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      ) : (
        <div className="text-center py-12">
          <BarChart3 className="h-16 w-16 text-gray-400 mx-auto mb-4" />
          <p className="text-gray-600 mb-4">No analysis data available</p>
          <button
            onClick={runAnalysis}
            className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-lg font-medium"
          >
            Start AI Analysis
          </button>
        </div>
      )}

      {/* Workflow Information */}
      <div className="mt-8 p-4 bg-yellow-50 rounded-lg">
        <h3 className="text-lg font-semibold text-yellow-900 mb-3">
          <Lightbulb className="h-5 w-5 inline mr-2" />
          How AI Optimization Works
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-yellow-800">
          <div>
            <h4 className="font-semibold mb-2">Analysis Phase:</h4>
            <ul className="space-y-1">
              <li>• Bundle size and composition analysis</li>
              <li>• Performance metrics measurement</li>
              <li>• Code quality assessment</li>
              <li>• Accessibility compliance check</li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold mb-2">Optimization Phase:</h4>
            <ul className="space-y-1">
              <li>• AI-generated improvement suggestions</li>
              <li>• Priority-based recommendation ranking</li>
              <li>• Automated safe optimizations</li>
              <li>• Impact measurement and tracking</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

/**
 * Metric Card Component
 */
interface MetricCardProps {
  metric: OptimizationMetric;
}

const MetricCard: React.FC<MetricCardProps> = ({ metric }) => {
  const getStatusColor = (status: string) => {
    switch (status) {
      case 'excellent': return 'text-green-600 bg-green-50 border-green-200';
      case 'good': return 'text-blue-600 bg-blue-50 border-blue-200';
      case 'needs_improvement': return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      case 'poor': return 'text-red-600 bg-red-50 border-red-200';
      default: return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case 'improving': return <TrendingUp className="h-4 w-4 text-green-500" />;
      case 'degrading': return <AlertTriangle className="h-4 w-4 text-red-500" />;
      default: return <Clock className="h-4 w-4 text-gray-500" />;
    }
  };

  return (
    <div className={`p-4 rounded-lg border ${getStatusColor(metric.status)}`}>
      <div className="flex items-center justify-between mb-2">
        <h4 className="font-medium">{metric.name}</h4>
        {getTrendIcon(metric.trend)}
      </div>
      
      <div className="space-y-1">
        <div className="flex justify-between items-end">
          <span className="text-2xl font-bold">
            {metric.current}{metric.unit}
          </span>
          <span className="text-sm opacity-75">
            Target: {metric.target}{metric.unit}
          </span>
        </div>
        
        <div className="w-full bg-white bg-opacity-50 rounded-full h-2">
          <div
            className="bg-current h-2 rounded-full transition-all duration-300"
            style={{
              width: `${Math.min((metric.current / metric.target) * 100, 100)}%`
            }}
          />
        </div>
      </div>
    </div>
  );
};

/**
 * Suggestion Card Component
 */
interface SuggestionCardProps {
  suggestion: OptimizationSuggestion;
  onApply: () => void;
  isApplied: boolean;
}

const SuggestionCard: React.FC<SuggestionCardProps> = ({ suggestion, onApply, isApplied }) => {
  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'critical': return 'bg-red-100 text-red-800';
      case 'high': return 'bg-orange-100 text-orange-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'low': return 'bg-blue-100 text-blue-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'performance': return <Zap className="h-4 w-4" />;
      case 'accessibility': return <Eye className="h-4 w-4" />;
      case 'security': return <Shield className="h-4 w-4" />;
      case 'code_quality': return <Code className="h-4 w-4" />;
      case 'bundle': return <HardDrive className="h-4 w-4" />;
      default: return <Target className="h-4 w-4" />;
    }
  };

  return (
    <div className={`p-4 rounded-lg border ${isApplied ? 'border-green-200 bg-green-50' : 'border-gray-200'}`}>
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center space-x-2 mb-2">
            {getCategoryIcon(suggestion.category)}
            <h4 className="font-semibold text-gray-900">{suggestion.title}</h4>
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(suggestion.priority)}`}>
              {suggestion.priority}
            </span>
            {suggestion.automatable && (
              <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs font-medium">
                Auto-fixable
              </span>
            )}
          </div>
          
          <p className="text-gray-600 text-sm mb-2">{suggestion.description}</p>
          
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="font-medium text-gray-700">Impact:</span>
              <p className="text-gray-600">{suggestion.impact}</p>
            </div>
            <div>
              <span className="font-medium text-gray-700">Effort:</span>
              <span className={`ml-1 px-2 py-1 rounded text-xs ${
                suggestion.effort === 'low' ? 'bg-green-100 text-green-800' :
                suggestion.effort === 'medium' ? 'bg-yellow-100 text-yellow-800' :
                'bg-red-100 text-red-800'
              }`}>
                {suggestion.effort}
              </span>
            </div>
          </div>
          
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
        
        <div className="ml-4">
          {isApplied ? (
            <div className="flex items-center space-x-1 text-green-600">
              <CheckCircle className="h-5 w-5" />
              <span className="text-sm font-medium">Applied</span>
            </div>
          ) : (
            <button
              onClick={onApply}
              disabled={!suggestion.automatable}
              className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                suggestion.automatable
                  ? 'bg-blue-500 hover:bg-blue-600 text-white'
                  : 'bg-gray-300 text-gray-500 cursor-not-allowed'
              }`}
            >
              {suggestion.automatable ? 'Apply' : 'Manual'}
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default AIOptimizationWorkflow;