/**
 * Multi-Agent AI Development Workflow Example
 * 
 * This example demonstrates coordinated AI agents working together to build
 * a complex feature, with each agent handling different aspects of development.
 */

import React, { useState, useEffect, useCallback } from 'react';
import { 
  Users, 
  Bot, 
  Code, 
  TestTube, 
  Zap, 
  Eye, 
  FileText, 
  CheckCircle, 
  AlertCircle,
  Clock,
  GitBranch
} from 'lucide-react';

// Multi-Agent Workflow Interfaces
export interface Agent {
  id: string;
  name: string;
  role: 'architect' | 'developer' | 'tester' | 'reviewer' | 'performance' | 'accessibility' | 'documentation';
  status: 'idle' | 'working' | 'completed' | 'error';
  currentTask?: string;
  completedTasks: string[];
  icon: React.ComponentType;
}

export interface WorkflowStep {
  id: string;
  name: string;
  agent: string;
  dependencies: string[];
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  output?: any;
  duration?: number;
}

export interface MultiAgentWorkflowProps {
  /** Feature to develop */
  featureName: string;
  /** Requirements specification */
  requirements: string[];
  /** Enable real-time updates */
  realTime?: boolean;
  /** Custom CSS classes */
  className?: string;
}

/**
 * Multi-Agent Development Workflow Component
 * 
 * Demonstrates how different AI agents collaborate to build features:
 * 1. Architect Agent: System design and component planning
 * 2. Developer Agent: Code generation and implementation
 * 3. Tester Agent: Test generation and validation
 * 4. Performance Agent: Optimization and benchmarking
 * 5. Accessibility Agent: A11y compliance and testing
 * 6. Documentation Agent: Documentation generation
 * 7. Reviewer Agent: Code review and quality assurance
 */
export const MultiAgentWorkflow: React.FC<MultiAgentWorkflowProps> = ({
  featureName,
  requirements,
  realTime = true,
  className = '',
}) => {
  // Workflow state
  const [agents, setAgents] = useState<Agent[]>([
    {
      id: 'architect',
      name: 'Architecture Agent',
      role: 'architect',
      status: 'idle',
      completedTasks: [],
      icon: GitBranch,
    },
    {
      id: 'developer',
      name: 'Development Agent',
      role: 'developer',
      status: 'idle',
      completedTasks: [],
      icon: Code,
    },
    {
      id: 'tester',
      name: 'Testing Agent',
      role: 'tester',
      status: 'idle',
      completedTasks: [],
      icon: TestTube,
    },
    {
      id: 'performance',
      name: 'Performance Agent',
      role: 'performance',
      status: 'idle',
      completedTasks: [],
      icon: Zap,
    },
    {
      id: 'accessibility',
      name: 'Accessibility Agent',
      role: 'accessibility',
      status: 'idle',
      completedTasks: [],
      icon: Eye,
    },
    {
      id: 'documentation',
      name: 'Documentation Agent',
      role: 'documentation',
      status: 'idle',
      completedTasks: [],
      icon: FileText,
    },
    {
      id: 'reviewer',
      name: 'Review Agent',
      role: 'reviewer',
      status: 'idle',
      completedTasks: [],
      icon: CheckCircle,
    },
  ]);

  const [workflowSteps, setWorkflowSteps] = useState<WorkflowStep[]>([
    {
      id: 'system_design',
      name: 'System Design & Architecture',
      agent: 'architect',
      dependencies: [],
      status: 'pending',
    },
    {
      id: 'component_generation',
      name: 'Component Implementation',
      agent: 'developer',
      dependencies: ['system_design'],
      status: 'pending',
    },
    {
      id: 'test_generation',
      name: 'Test Suite Generation',
      agent: 'tester',
      dependencies: ['component_generation'],
      status: 'pending',
    },
    {
      id: 'performance_optimization',
      name: 'Performance Optimization',
      agent: 'performance',
      dependencies: ['component_generation'],
      status: 'pending',
    },
    {
      id: 'accessibility_validation',
      name: 'Accessibility Compliance',
      agent: 'accessibility',
      dependencies: ['component_generation'],
      status: 'pending',
    },
    {
      id: 'documentation_generation',
      name: 'Documentation Creation',
      agent: 'documentation',
      dependencies: ['component_generation'],
      status: 'pending',
    },
    {
      id: 'code_review',
      name: 'Code Review & Quality Assurance',
      agent: 'reviewer',
      dependencies: ['test_generation', 'performance_optimization', 'accessibility_validation'],
      status: 'pending',
    },
  ]);

  const [isRunning, setIsRunning] = useState(false);
  const [currentStep, setCurrentStep] = useState<string | null>(null);
  const [progress, setProgress] = useState(0);

  // Simulate agent workflow execution
  const executeWorkflow = useCallback(async () => {
    setIsRunning(true);
    setProgress(0);

    const steps = [...workflowSteps];
    
    for (let i = 0; i < steps.length; i++) {
      const step = steps[i];
      
      // Check if dependencies are completed
      const dependenciesCompleted = step.dependencies.every(depId =>
        steps.find(s => s.id === depId)?.status === 'completed'
      );

      if (!dependenciesCompleted) {
        continue;
      }

      // Start step
      setCurrentStep(step.id);
      setWorkflowSteps(prev => prev.map(s => 
        s.id === step.id ? { ...s, status: 'in_progress' } : s
      ));

      // Update agent status
      setAgents(prev => prev.map(agent => 
        agent.id === step.agent 
          ? { ...agent, status: 'working', currentTask: step.name }
          : agent
      ));

      // Simulate work duration
      const duration = Math.random() * 3000 + 2000; // 2-5 seconds
      await new Promise(resolve => setTimeout(resolve, duration));

      // Complete step
      const output = await simulateAgentWork(step);
      
      setWorkflowSteps(prev => prev.map(s => 
        s.id === step.id 
          ? { ...s, status: 'completed', output, duration }
          : s
      ));

      // Update agent status
      setAgents(prev => prev.map(agent => 
        agent.id === step.agent 
          ? { 
              ...agent, 
              status: 'completed', 
              currentTask: undefined,
              completedTasks: [...agent.completedTasks, step.name]
            }
          : agent
      ));

      setProgress((i + 1) / steps.length * 100);
    }

    setIsRunning(false);
    setCurrentStep(null);
  }, [workflowSteps]);

  // Simulate agent work with realistic outputs
  const simulateAgentWork = async (step: WorkflowStep) => {
    switch (step.agent) {
      case 'architect':
        return {
          components: ['UserProfile', 'UserSettings', 'UserAvatar'],
          interfaces: ['User', 'UserSettings', 'UserActions'],
          architecture: 'Component-based with hooks and context',
        };
      
      case 'developer':
        return {
          files: ['UserProfile.tsx', 'useUserProfile.ts', 'UserProfile.styles.ts'],
          linesOfCode: 247,
          complexityScore: 'Medium',
        };
      
      case 'tester':
        return {
          testFiles: ['UserProfile.test.tsx', 'useUserProfile.test.ts'],
          testCases: 23,
          coverage: '94%',
        };
      
      case 'performance':
        return {
          renderTime: '12ms',
          bundleSize: '23KB',
          optimizations: ['React.memo', 'useMemo', 'code splitting'],
        };
      
      case 'accessibility':
        return {
          wcagCompliance: 'AA',
          issues: 0,
          score: 100,
          features: ['keyboard navigation', 'screen reader support', 'high contrast'],
        };
      
      case 'documentation':
        return {
          files: ['UserProfile.md', 'API.md', 'Examples.md'],
          sections: ['Usage', 'Props', 'Examples', 'Accessibility'],
        };
      
      case 'reviewer':
        return {
          issuesFound: 2,
          suggestions: ['Add error boundary', 'Optimize re-renders'],
          approvalStatus: 'Approved with minor suggestions',
        };
      
      default:
        return {};
    }
  };

  // Reset workflow
  const resetWorkflow = useCallback(() => {
    setAgents(prev => prev.map(agent => ({
      ...agent,
      status: 'idle',
      currentTask: undefined,
      completedTasks: [],
    })));
    
    setWorkflowSteps(prev => prev.map(step => ({
      ...step,
      status: 'pending',
      output: undefined,
      duration: undefined,
    })));
    
    setProgress(0);
    setCurrentStep(null);
    setIsRunning(false);
  }, []);

  return (
    <div className={`bg-white rounded-lg shadow-lg p-6 ${className}`}>
      {/* Header */}
      <div className="border-b border-gray-200 pb-4 mb-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Users className="h-8 w-8 text-blue-500" />
            <div>
              <h2 className="text-2xl font-bold text-gray-900">Multi-Agent Workflow</h2>
              <p className="text-gray-600">Feature: {featureName}</p>
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            <button
              onClick={executeWorkflow}
              disabled={isRunning}
              className="bg-blue-500 hover:bg-blue-600 disabled:bg-gray-400 text-white px-4 py-2 rounded-lg font-medium transition-colors"
            >
              {isRunning ? 'Running...' : 'Start Workflow'}
            </button>
            
            <button
              onClick={resetWorkflow}
              disabled={isRunning}
              className="bg-gray-500 hover:bg-gray-600 disabled:bg-gray-400 text-white px-4 py-2 rounded-lg font-medium transition-colors"
            >
              Reset
            </button>
          </div>
        </div>

        {/* Progress Bar */}
        {isRunning && (
          <div className="mt-4">
            <div className="flex items-center justify-between text-sm text-gray-600 mb-2">
              <span>Progress</span>
              <span>{Math.round(progress)}%</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>
        )}
      </div>

      {/* Requirements */}
      <div className="mb-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-3">Requirements</h3>
        <ul className="space-y-2">
          {requirements.map((req, index) => (
            <li key={index} className="flex items-start space-x-2">
              <CheckCircle className="h-5 w-5 text-green-500 mt-0.5" />
              <span className="text-gray-700">{req}</span>
            </li>
          ))}
        </ul>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Agents Panel */}
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-4">AI Agents</h3>
          <div className="space-y-3">
            {agents.map(agent => (
              <AgentCard
                key={agent.id}
                agent={agent}
                isActive={currentStep ? workflowSteps.find(s => s.id === currentStep)?.agent === agent.id : false}
              />
            ))}
          </div>
        </div>

        {/* Workflow Steps */}
        <div>
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Workflow Steps</h3>
          <div className="space-y-3">
            {workflowSteps.map((step, index) => (
              <WorkflowStepCard
                key={step.id}
                step={step}
                stepNumber={index + 1}
                isActive={currentStep === step.id}
              />
            ))}
          </div>
        </div>
      </div>

      {/* Workflow Explanation */}
      <div className="mt-8 p-4 bg-blue-50 rounded-lg">
        <h3 className="text-lg font-semibold text-blue-900 mb-3">How Multi-Agent Workflow Works</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-blue-800">
          <div>
            <h4 className="font-semibold mb-2">Agent Coordination:</h4>
            <ul className="space-y-1">
              <li>• Each agent has specialized capabilities</li>
              <li>• Dependencies ensure proper execution order</li>
              <li>• Agents communicate through shared context</li>
              <li>• Real-time status updates and progress tracking</li>
            </ul>
          </div>
          <div>
            <h4 className="font-semibold mb-2">Quality Assurance:</h4>
            <ul className="space-y-1">
              <li>• Automated testing at each stage</li>
              <li>• Performance optimization built-in</li>
              <li>• Accessibility validation included</li>
              <li>• Comprehensive documentation generated</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

/**
 * Agent Card Component
 */
interface AgentCardProps {
  agent: Agent;
  isActive: boolean;
}

const AgentCard: React.FC<AgentCardProps> = ({ agent, isActive }) => {
  const Icon = agent.icon;
  
  return (
    <div className={`p-4 rounded-lg border transition-all duration-200 ${
      isActive 
        ? 'border-blue-500 bg-blue-50 shadow-md' 
        : 'border-gray-200 bg-gray-50'
    }`}>
      <div className="flex items-center space-x-3">
        <div className={`p-2 rounded-full ${
          agent.status === 'working' ? 'bg-blue-500 text-white' :
          agent.status === 'completed' ? 'bg-green-500 text-white' :
          agent.status === 'error' ? 'bg-red-500 text-white' :
          'bg-gray-300 text-gray-600'
        }`}>
          <Icon className="h-4 w-4" />
        </div>
        
        <div className="flex-1">
          <h4 className="font-medium text-gray-900">{agent.name}</h4>
          <div className="flex items-center space-x-2 mt-1">
            <StatusIndicator status={agent.status} />
            {agent.currentTask && (
              <span className="text-xs text-gray-600">{agent.currentTask}</span>
            )}
          </div>
        </div>
      </div>
      
      {agent.completedTasks.length > 0 && (
        <div className="mt-3 pt-3 border-t border-gray-200">
          <p className="text-xs font-medium text-gray-700 mb-1">Completed Tasks:</p>
          <ul className="text-xs text-gray-600 space-y-1">
            {agent.completedTasks.map((task, index) => (
              <li key={index} className="flex items-center space-x-1">
                <CheckCircle className="h-3 w-3 text-green-500" />
                <span>{task}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

/**
 * Workflow Step Card Component
 */
interface WorkflowStepCardProps {
  step: WorkflowStep;
  stepNumber: number;
  isActive: boolean;
}

const WorkflowStepCard: React.FC<WorkflowStepCardProps> = ({ step, stepNumber, isActive }) => (
  <div className={`p-4 rounded-lg border transition-all duration-200 ${
    isActive ? 'border-blue-500 bg-blue-50' : 'border-gray-200'
  }`}>
    <div className="flex items-start space-x-3">
      <div className={`w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${
        step.status === 'completed' ? 'bg-green-500 text-white' :
        step.status === 'in_progress' ? 'bg-blue-500 text-white' :
        step.status === 'failed' ? 'bg-red-500 text-white' :
        'bg-gray-300 text-gray-600'
      }`}>
        {stepNumber}
      </div>
      
      <div className="flex-1">
        <h4 className="font-medium text-gray-900">{step.name}</h4>
        <div className="flex items-center space-x-2 mt-1">
          <StatusIndicator status={step.status} />
          {step.duration && (
            <span className="text-xs text-gray-500">
              <Clock className="h-3 w-3 inline mr-1" />
              {(step.duration / 1000).toFixed(1)}s
            </span>
          )}
        </div>
        
        {step.dependencies.length > 0 && (
          <p className="text-xs text-gray-500 mt-1">
            Depends on: {step.dependencies.join(', ')}
          </p>
        )}
        
        {step.output && step.status === 'completed' && (
          <div className="mt-2 p-2 bg-green-50 rounded text-xs">
            <p className="font-medium text-green-800">Output:</p>
            <pre className="text-green-700 mt-1">
              {JSON.stringify(step.output, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  </div>
);

/**
 * Status Indicator Component
 */
interface StatusIndicatorProps {
  status: string;
}

const StatusIndicator: React.FC<StatusIndicatorProps> = ({ status }) => {
  const statusConfig = {
    idle: { color: 'text-gray-500', label: 'Idle' },
    pending: { color: 'text-gray-500', label: 'Pending' },
    working: { color: 'text-blue-500', label: 'Working' },
    in_progress: { color: 'text-blue-500', label: 'In Progress' },
    completed: { color: 'text-green-500', label: 'Completed' },
    failed: { color: 'text-red-500', label: 'Failed' },
    error: { color: 'text-red-500', label: 'Error' },
  };

  const config = statusConfig[status as keyof typeof statusConfig] || statusConfig.idle;

  return (
    <span className={`text-xs font-medium ${config.color}`}>
      {config.label}
    </span>
  );
};

export default MultiAgentWorkflow;