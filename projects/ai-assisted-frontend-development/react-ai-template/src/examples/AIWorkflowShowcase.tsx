/**
 * AI Workflow Showcase Component
 * 
 * This component demonstrates all available AI workflow patterns
 * in a comprehensive showcase with interactive examples.
 */

import React, { useState } from 'react';
import { 
  Workflow, 
  Code, 
  Users, 
  Zap, 
  BookOpen, 
  Play, 
  ChevronRight,
  ExternalLink,
  GitBranch,
  TestTube,
  Eye,
  BarChart3
} from 'lucide-react';

import { TDDCalculator } from './ai-workflows/TDDWorkflowExample';
import { MultiAgentWorkflow } from './ai-workflows/MultiAgentWorkflowExample';
import { AIOptimizationWorkflow } from './ai-workflows/AIOptimizationWorkflowExample';
import { workflowExamples } from './ai-workflows';

// Showcase interfaces
export interface WorkflowDemo {
  id: string;
  title: string;
  description: string;
  component: React.ComponentType<any>;
  props: any;
  category: 'development' | 'testing' | 'optimization';
  complexity: 'beginner' | 'intermediate' | 'advanced';
  timeToImplement: string;
  benefits: string[];
  prerequisites: string[];
}

export interface AIWorkflowShowcaseProps {
  /** Show only specific categories */
  categories?: ('development' | 'testing' | 'optimization')[];
  /** Enable interactive mode */
  interactive?: boolean;
  /** Show implementation details */
  showDetails?: boolean;
  /** Custom CSS classes */
  className?: string;
}

/**
 * AI Workflow Showcase Component
 * 
 * Provides a comprehensive demonstration of AI-assisted development workflows
 * with interactive examples and detailed explanations.
 */
export const AIWorkflowShowcase: React.FC<AIWorkflowShowcaseProps> = ({
  categories = ['development', 'testing', 'optimization'],
  interactive = true,
  showDetails = true,
  className = '',
}) => {
  const [selectedWorkflow, setSelectedWorkflow] = useState<string>('tdd');
  const [activeDemo, setActiveDemo] = useState<string | null>(null);

  // Define workflow demos
  const workflowDemos: WorkflowDemo[] = [
    {
      id: 'tdd',
      title: 'Test-Driven Development Workflow',
      description: 'AI-assisted TDD with automated test generation, real-time feedback, and intelligent refactoring suggestions.',
      component: TDDCalculator,
      props: {
        initialValue: '0',
        scientificMode: false,
        onCalculation: (result: number, operation: string) => {
          console.log(`TDD Demo: ${operation} = ${result}`);
        },
      },
      category: 'testing',
      complexity: 'intermediate',
      timeToImplement: '2-4 hours',
      benefits: [
        'Faster test creation with AI assistance',
        'Higher code coverage and quality',
        'Automated refactoring suggestions',
        'Real-time feedback during development',
      ],
      prerequisites: [
        'Understanding of React testing patterns',
        'Familiarity with Jest and React Testing Library',
        'Basic knowledge of TDD principles',
      ],
    },
    {
      id: 'multi-agent',
      title: 'Multi-Agent Development Workflow',
      description: 'Coordinated AI agents working together on different aspects of feature development for comprehensive automation.',
      component: MultiAgentWorkflow,
      props: {
        featureName: 'User Profile Management',
        requirements: [
          'Create user profile component with avatar upload',
          'Implement user settings management',
          'Add profile privacy controls',
          'Include accessibility features',
          'Ensure mobile responsiveness',
        ],
        realTimeUpdates: true,
      },
      category: 'development',
      complexity: 'advanced',
      timeToImplement: '1-2 days',
      benefits: [
        'Parallel development across multiple aspects',
        'Consistent quality across all deliverables',
        'Automated coordination and dependency management',
        'Comprehensive feature development',
      ],
      prerequisites: [
        'Advanced React development skills',
        'Understanding of AI orchestration concepts',
        'Experience with complex project workflows',
      ],
    },
    {
      id: 'ai-optimization',
      title: 'AI-Powered Optimization Workflow',
      description: 'Automated performance analysis, optimization suggestions, and implementation with real-time monitoring.',
      component: AIOptimizationWorkflow,
      props: {
        targetComponent: 'SearchableProductList',
        realTimeAnalysis: true,
        autoApply: false,
      },
      category: 'optimization',
      complexity: 'intermediate',
      timeToImplement: '4-8 hours',
      benefits: [
        'Automated performance bottleneck detection',
        'AI-generated optimization strategies',
        'Real-time performance monitoring',
        'Measurable improvement tracking',
      ],
      prerequisites: [
        'Performance optimization knowledge',
        'Understanding of React performance patterns',
        'Familiarity with Core Web Vitals',
      ],
    },
  ];

  // Filter workflows by category
  const filteredWorkflows = workflowDemos.filter(workflow => 
    categories.includes(workflow.category)
  );

  const selectedDemo = filteredWorkflows.find(w => w.id === selectedWorkflow);

  return (
    <div className={`bg-white rounded-lg shadow-lg ${className}`}>
      {/* Header */}
      <div className="border-b border-gray-200 p-6">
        <div className="flex items-center space-x-3 mb-4">
          <Workflow className="h-8 w-8 text-blue-500" />
          <div>
            <h1 className="text-3xl font-bold text-gray-900">AI Workflow Showcase</h1>
            <p className="text-gray-600">Interactive examples of AI-assisted development workflows</p>
          </div>
        </div>

        {/* Category tabs */}
        <div className="flex space-x-1 bg-gray-100 rounded-lg p-1">
          {['development', 'testing', 'optimization'].map(category => (
            <button
              key={category}
              onClick={() => {
                const firstWorkflow = filteredWorkflows.find(w => w.category === category);
                if (firstWorkflow) setSelectedWorkflow(firstWorkflow.id);
              }}
              className={`flex-1 px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                categories.includes(category as any)
                  ? 'bg-white text-gray-900 shadow-sm'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              {category.charAt(0).toUpperCase() + category.slice(1)}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 divide-x divide-gray-200">
        {/* Workflow List */}
        <div className="p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Workflow Examples</h2>
          <div className="space-y-3">
            {filteredWorkflows.map(workflow => (
              <WorkflowCard
                key={workflow.id}
                workflow={workflow}
                isSelected={selectedWorkflow === workflow.id}
                onClick={() => setSelectedWorkflow(workflow.id)}
              />
            ))}
          </div>

          {/* Quick Start Guide */}
          <div className="mt-8 p-4 bg-blue-50 rounded-lg">
            <h3 className="text-sm font-semibold text-blue-900 mb-2">
              <BookOpen className="h-4 w-4 inline mr-1" />
              Quick Start Guide
            </h3>
            <ol className="text-xs text-blue-800 space-y-1">
              <li>1. Select a workflow from the list</li>
              <li>2. Review the implementation details</li>
              <li>3. Try the interactive demo</li>
              <li>4. Check prerequisites and benefits</li>
              <li>5. Start implementing in your project</li>
            </ol>
          </div>
        </div>

        {/* Workflow Details */}
        <div className="p-6 lg:col-span-2">
          {selectedDemo ? (
            <div className="space-y-6">
              {/* Workflow Header */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <h2 className="text-xl font-bold text-gray-900">{selectedDemo.title}</h2>
                  <div className="flex items-center space-x-2">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      selectedDemo.complexity === 'beginner' ? 'bg-green-100 text-green-800' :
                      selectedDemo.complexity === 'intermediate' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {selectedDemo.complexity}
                    </span>
                    <span className="text-sm text-gray-500">{selectedDemo.timeToImplement}</span>
                  </div>
                </div>
                <p className="text-gray-600">{selectedDemo.description}</p>
              </div>

              {/* Interactive Demo */}
              {interactive && (
                <div>
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold text-gray-900">Interactive Demo</h3>
                    <button
                      onClick={() => setActiveDemo(activeDemo === selectedDemo.id ? null : selectedDemo.id)}
                      className="flex items-center space-x-2 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg font-medium transition-colors"
                    >
                      <Play className="h-4 w-4" />
                      <span>{activeDemo === selectedDemo.id ? 'Hide Demo' : 'Show Demo'}</span>
                    </button>
                  </div>

                  {activeDemo === selectedDemo.id && (
                    <div className="border border-gray-200 rounded-lg p-4 bg-gray-50">
                      <selectedDemo.component {...selectedDemo.props} />
                    </div>
                  )}
                </div>
              )}

              {/* Implementation Details */}
              {showDetails && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* Benefits */}
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-3">Benefits</h3>
                    <ul className="space-y-2">
                      {selectedDemo.benefits.map((benefit, index) => (
                        <li key={index} className="flex items-start space-x-2">
                          <ChevronRight className="h-4 w-4 text-green-500 mt-0.5" />
                          <span className="text-gray-700">{benefit}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Prerequisites */}
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900 mb-3">Prerequisites</h3>
                    <ul className="space-y-2">
                      {selectedDemo.prerequisites.map((prereq, index) => (
                        <li key={index} className="flex items-start space-x-2">
                          <ChevronRight className="h-4 w-4 text-blue-500 mt-0.5" />
                          <span className="text-gray-700">{prereq}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}

              {/* Implementation Guide */}
              <div className="bg-gray-50 rounded-lg p-4">
                <h3 className="text-lg font-semibold text-gray-900 mb-3">Implementation Guide</h3>
                <div className="space-y-4">
                  {selectedDemo.id === 'tdd' && (
                    <TDDImplementationGuide />
                  )}
                  {selectedDemo.id === 'multi-agent' && (
                    <MultiAgentImplementationGuide />
                  )}
                  {selectedDemo.id === 'ai-optimization' && (
                    <OptimizationImplementationGuide />
                  )}
                </div>
              </div>
            </div>
          ) : (
            <div className="text-center py-12">
              <Workflow className="h-16 w-16 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-600">Select a workflow to view details and examples</p>
            </div>
          )}
        </div>
      </div>

      {/* Footer */}
      <div className="border-t border-gray-200 p-6 bg-gray-50">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-sm font-semibold text-gray-900">Ready to implement?</h3>
            <p className="text-sm text-gray-600">Check out our complete implementation guides and templates</p>
          </div>
          <button className="flex items-center space-x-2 bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg font-medium transition-colors">
            <ExternalLink className="h-4 w-4" />
            <span>View Documentation</span>
          </button>
        </div>
      </div>
    </div>
  );
};

/**
 * Workflow Card Component
 */
interface WorkflowCardProps {
  workflow: WorkflowDemo;
  isSelected: boolean;
  onClick: () => void;
}

const WorkflowCard: React.FC<WorkflowCardProps> = ({ workflow, isSelected, onClick }) => {
  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'development': return <Code className="h-4 w-4" />;
      case 'testing': return <TestTube className="h-4 w-4" />;
      case 'optimization': return <Zap className="h-4 w-4" />;
      default: return <Workflow className="h-4 w-4" />;
    }
  };

  return (
    <button
      onClick={onClick}
      className={`w-full text-left p-4 rounded-lg border transition-all duration-200 ${
        isSelected 
          ? 'border-blue-500 bg-blue-50 shadow-md' 
          : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
      }`}
    >
      <div className="flex items-start space-x-3">
        <div className={`p-2 rounded-full ${
          isSelected ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-600'
        }`}>
          {getCategoryIcon(workflow.category)}
        </div>
        
        <div className="flex-1 min-w-0">
          <h3 className="font-medium text-gray-900 mb-1">{workflow.title}</h3>
          <p className="text-sm text-gray-600 line-clamp-2">{workflow.description}</p>
          
          <div className="flex items-center justify-between mt-3">
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${
              workflow.complexity === 'beginner' ? 'bg-green-100 text-green-800' :
              workflow.complexity === 'intermediate' ? 'bg-yellow-100 text-yellow-800' :
              'bg-red-100 text-red-800'
            }`}>
              {workflow.complexity}
            </span>
            <span className="text-xs text-gray-500">{workflow.timeToImplement}</span>
          </div>
        </div>
      </div>
    </button>
  );
};

/**
 * Implementation Guide Components
 */
const TDDImplementationGuide: React.FC = () => (
  <div className="space-y-3">
    <div className="flex items-center space-x-2">
      <TestTube className="h-5 w-5 text-blue-500" />
      <h4 className="font-semibold text-gray-900">TDD Workflow Setup</h4>
    </div>
    <ol className="text-sm text-gray-700 space-y-2 ml-7">
      <li>1. Configure AI tools (Cursor, Copilot, Claude Code) for test generation</li>
      <li>2. Set up Jest and React Testing Library with AI-optimized configuration</li>
      <li>3. Create test templates for AI-assisted generation</li>
      <li>4. Implement the Red-Green-Refactor cycle with AI feedback</li>
      <li>5. Use AI for test case expansion and edge case detection</li>
    </ol>
  </div>
);

const MultiAgentImplementationGuide: React.FC = () => (
  <div className="space-y-3">
    <div className="flex items-center space-x-2">
      <Users className="h-5 w-5 text-blue-500" />
      <h4 className="font-semibold text-gray-900">Multi-Agent Setup</h4>
    </div>
    <ol className="text-sm text-gray-700 space-y-2 ml-7">
      <li>1. Define agent roles and responsibilities</li>
      <li>2. Set up orchestration system with dependency management</li>
      <li>3. Configure AI models for each specialized agent</li>
      <li>4. Implement communication protocols between agents</li>
      <li>5. Create quality gates and validation checkpoints</li>
    </ol>
  </div>
);

const OptimizationImplementationGuide: React.FC = () => (
  <div className="space-y-3">
    <div className="flex items-center space-x-2">
      <BarChart3 className="h-5 w-5 text-blue-500" />
      <h4 className="font-semibold text-gray-900">Optimization Workflow Setup</h4>
    </div>
    <ol className="text-sm text-gray-700 space-y-2 ml-7">
      <li>1. Install performance monitoring and analysis tools</li>
      <li>2. Configure AI optimization engine with project-specific rules</li>
      <li>3. Set up automated performance benchmarking</li>
      <li>4. Implement suggestion ranking and application system</li>
      <li>5. Create feedback loop for continuous improvement</li>
    </ol>
  </div>
);

export default AIWorkflowShowcase;