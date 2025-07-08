/**
 * AI Workflow Examples Export
 * 
 * This module exports all AI workflow examples for easy integration
 * and demonstration of AI-assisted development patterns.
 */

export { default as TDDWorkflowExample, TDDCalculator } from './TDDWorkflowExample';
export { default as MultiAgentWorkflowExample, MultiAgentWorkflow } from './MultiAgentWorkflowExample';
export { default as AIOptimizationWorkflowExample, AIOptimizationWorkflow } from './AIOptimizationWorkflowExample';

// Re-export types for external use
export type {
  CalculatorState,
  CalculatorProps,
} from './TDDWorkflowExample';

export type {
  Agent,
  WorkflowStep,
  MultiAgentWorkflowProps,
} from './MultiAgentWorkflowExample';

export type {
  OptimizationMetric,
  OptimizationSuggestion,
  OptimizationReport,
  AIOptimizationWorkflowProps,
} from './AIOptimizationWorkflowExample';

/**
 * Workflow metadata for documentation and examples
 */
export const workflowExamples = {
  tdd: {
    name: 'Test-Driven Development',
    description: 'AI-assisted TDD workflow with automated test generation',
    component: 'TDDWorkflowExample',
    features: [
      'AI-generated test cases',
      'Real-time test feedback',
      'Code coverage optimization',
      'Refactoring suggestions',
    ],
    tools: ['Cursor AI', 'GitHub Copilot', 'Claude Code'],
  },
  multiAgent: {
    name: 'Multi-Agent Development',
    description: 'Coordinated AI agents for comprehensive feature development',
    component: 'MultiAgentWorkflowExample',
    features: [
      'Specialized agent roles',
      'Dependency management',
      'Parallel processing',
      'Quality assurance',
    ],
    tools: ['Multiple AI models', 'Orchestration system', 'Quality gates'],
  },
  optimization: {
    name: 'AI-Powered Optimization',
    description: 'Automated performance and code quality optimization',
    component: 'AIOptimizationWorkflowExample',
    features: [
      'Performance analysis',
      'Automated optimizations',
      'Real-time monitoring',
      'Impact measurement',
    ],
    tools: ['Performance profilers', 'Bundle analyzers', 'AI optimization engine'],
  },
} as const;

export default {
  TDDWorkflowExample,
  MultiAgentWorkflowExample,
  AIOptimizationWorkflowExample,
  workflowExamples,
};