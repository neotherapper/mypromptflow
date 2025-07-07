/**
 * AI-Assisted Test-Driven Development (TDD) Workflow Example
 * 
 * This example demonstrates how to use AI tools for test-driven development
 * in React applications, showcasing the complete TDD cycle with AI assistance.
 */

import React, { useState, useCallback } from 'react';
import { Calculator, Plus, Minus, X, Divide, RotateCcw } from 'lucide-react';

// Step 1: Define requirements and interfaces (AI-assisted)
export interface CalculatorState {
  display: string;
  previousValue: number | null;
  operation: string | null;
  waitingForOperand: boolean;
}

export interface CalculatorProps {
  /** Initial value to display */
  initialValue?: string;
  /** Callback when calculation is performed */
  onCalculation?: (result: number, operation: string) => void;
  /** Enable scientific mode */
  scientificMode?: boolean;
  /** Custom CSS classes */
  className?: string;
}

/**
 * AI-Generated Calculator Component using TDD Approach
 * 
 * Development Process:
 * 1. Write failing tests (AI-assisted test generation)
 * 2. Implement minimal code to pass tests
 * 3. Refactor with AI optimization suggestions
 * 4. Repeat cycle
 * 
 * AI Tools Used:
 * - Cursor AI: Component generation and refactoring
 * - GitHub Copilot: Test completion and edge case suggestions
 * - Claude Code: Architecture review and optimization
 */
export const TDDCalculator: React.FC<CalculatorProps> = ({
  initialValue = '0',
  onCalculation,
  scientificMode = false,
  className = '',
}) => {
  // Step 2: Initialize state (driven by test requirements)
  const [state, setState] = useState<CalculatorState>({
    display: initialValue,
    previousValue: null,
    operation: null,
    waitingForOperand: false,
  });

  // Step 3: Implement core functionality (test-driven)
  const inputNumber = useCallback((num: string) => {
    if (state.waitingForOperand) {
      setState(prev => ({
        ...prev,
        display: num,
        waitingForOperand: false,
      }));
    } else {
      setState(prev => ({
        ...prev,
        display: prev.display === '0' ? num : prev.display + num,
      }));
    }
  }, [state.waitingForOperand]);

  const inputDecimal = useCallback(() => {
    if (state.waitingForOperand) {
      setState(prev => ({
        ...prev,
        display: '0.',
        waitingForOperand: false,
      }));
    } else if (state.display.indexOf('.') === -1) {
      setState(prev => ({
        ...prev,
        display: prev.display + '.',
      }));
    }
  }, [state.waitingForOperand, state.display]);

  const clear = useCallback(() => {
    setState({
      display: '0',
      previousValue: null,
      operation: null,
      waitingForOperand: false,
    });
  }, []);

  const performOperation = useCallback((nextOperation: string) => {
    const inputValue = parseFloat(state.display);

    if (state.previousValue === null) {
      setState(prev => ({
        ...prev,
        previousValue: inputValue,
        waitingForOperand: true,
        operation: nextOperation,
      }));
    } else if (state.operation) {
      const currentValue = state.previousValue || 0;
      let result: number;

      // AI-suggested comprehensive operation handling
      switch (state.operation) {
        case '+':
          result = currentValue + inputValue;
          break;
        case '-':
          result = currentValue - inputValue;
          break;
        case '*':
          result = currentValue * inputValue;
          break;
        case '/':
          if (inputValue === 0) {
            // AI-suggested error handling
            alert('Cannot divide by zero');
            return;
          }
          result = currentValue / inputValue;
          break;
        default:
          return;
      }

      // AI-suggested result formatting
      const formattedResult = Number(result.toFixed(10)).toString();

      setState({
        display: formattedResult,
        previousValue: result,
        operation: nextOperation,
        waitingForOperand: true,
      });

      // Callback for external handling
      if (onCalculation) {
        onCalculation(result, state.operation);
      }
    }
  }, [state, onCalculation]);

  const calculate = useCallback(() => {
    performOperation('=');
  }, [performOperation]);

  // Step 4: AI-suggested accessibility and UX improvements
  const handleKeyPress = useCallback((event: React.KeyboardEvent) => {
    const { key } = event;

    if (/[0-9]/.test(key)) {
      inputNumber(key);
    } else if (key === '.') {
      inputDecimal();
    } else if (key === '+') {
      performOperation('+');
    } else if (key === '-') {
      performOperation('-');
    } else if (key === '*') {
      performOperation('*');
    } else if (key === '/') {
      event.preventDefault();
      performOperation('/');
    } else if (key === 'Enter' || key === '=') {
      calculate();
    } else if (key === 'Escape' || key === 'c' || key === 'C') {
      clear();
    }
  }, [inputNumber, inputDecimal, performOperation, calculate, clear]);

  // Step 5: Render component with AI-optimized structure
  return (
    <div 
      className={`bg-white rounded-lg shadow-lg p-6 max-w-sm mx-auto ${className}`}
      onKeyDown={handleKeyPress}
      tabIndex={0}
      role="application"
      aria-label="Calculator"
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <Calculator className="h-6 w-6 text-blue-500" />
          <h2 className="text-xl font-semibold text-gray-900">
            TDD Calculator
          </h2>
        </div>
        {scientificMode && (
          <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">
            Scientific
          </span>
        )}
      </div>

      {/* Display */}
      <div className="bg-gray-100 rounded-lg p-4 mb-4">
        <div 
          className="text-right text-2xl font-mono text-gray-900 min-h-[2rem] flex items-center justify-end"
          aria-live="polite"
          aria-label={`Calculator display showing ${state.display}`}
        >
          {state.display}
        </div>
        {state.operation && state.previousValue !== null && (
          <div className="text-right text-sm text-gray-500 mt-1">
            {state.previousValue} {state.operation}
          </div>
        )}
      </div>

      {/* Controls */}
      <div className="grid grid-cols-4 gap-2">
        {/* Clear button */}
        <button
          onClick={clear}
          className="col-span-2 flex items-center justify-center space-x-1 bg-red-500 hover:bg-red-600 text-white font-semibold py-3 rounded-lg transition-colors"
          aria-label="Clear calculator"
        >
          <RotateCcw className="h-4 w-4" />
          <span>Clear</span>
        </button>
        
        {/* Operation buttons */}
        <OperationButton
          operation="/"
          onClick={() => performOperation('/')}
          icon={<Divide className="h-4 w-4" />}
          label="Divide"
        />
        <OperationButton
          operation="*"
          onClick={() => performOperation('*')}
          icon={<X className="h-4 w-4" />}
          label="Multiply"
        />

        {/* Number row 1 */}
        <NumberButton number="7" onClick={() => inputNumber('7')} />
        <NumberButton number="8" onClick={() => inputNumber('8')} />
        <NumberButton number="9" onClick={() => inputNumber('9')} />
        <OperationButton
          operation="-"
          onClick={() => performOperation('-')}
          icon={<Minus className="h-4 w-4" />}
          label="Subtract"
        />

        {/* Number row 2 */}
        <NumberButton number="4" onClick={() => inputNumber('4')} />
        <NumberButton number="5" onClick={() => inputNumber('5')} />
        <NumberButton number="6" onClick={() => inputNumber('6')} />
        <OperationButton
          operation="+"
          onClick={() => performOperation('+')}
          icon={<Plus className="h-4 w-4" />}
          label="Add"
        />

        {/* Number row 3 */}
        <NumberButton number="1" onClick={() => inputNumber('1')} />
        <NumberButton number="2" onClick={() => inputNumber('2')} />
        <NumberButton number="3" onClick={() => inputNumber('3')} />
        
        {/* Equals button */}
        <button
          onClick={calculate}
          className="row-span-2 bg-blue-500 hover:bg-blue-600 text-white font-semibold rounded-lg transition-colors"
          aria-label="Calculate result"
        >
          =
        </button>

        {/* Bottom row */}
        <NumberButton number="0" onClick={() => inputNumber('0')} className="col-span-2" />
        <button
          onClick={inputDecimal}
          className="bg-gray-200 hover:bg-gray-300 text-gray-900 font-semibold py-3 rounded-lg transition-colors"
          aria-label="Decimal point"
        >
          .
        </button>
      </div>

      {/* TDD Workflow Information */}
      <div className="mt-6 p-4 bg-blue-50 rounded-lg">
        <h3 className="text-sm font-semibold text-blue-900 mb-2">TDD Workflow Used:</h3>
        <ol className="text-xs text-blue-800 space-y-1">
          <li>1. ✅ Write failing tests for each function</li>
          <li>2. ✅ Implement minimal code to pass tests</li>
          <li>3. ✅ Refactor with AI optimization</li>
          <li>4. ✅ Add accessibility features</li>
          <li>5. ✅ Performance optimization</li>
        </ol>
      </div>

      {/* AI Tools Usage */}
      <div className="mt-4 p-4 bg-green-50 rounded-lg">
        <h3 className="text-sm font-semibold text-green-900 mb-2">AI Tools Integration:</h3>
        <ul className="text-xs text-green-800 space-y-1">
          <li>• Cursor AI: Component structure generation</li>
          <li>• Copilot: Test completion & edge cases</li>
          <li>• Claude Code: Architecture review</li>
        </ul>
      </div>
    </div>
  );
};

/**
 * Number Button Component (AI-generated)
 */
interface NumberButtonProps {
  number: string;
  onClick: () => void;
  className?: string;
}

const NumberButton: React.FC<NumberButtonProps> = ({ number, onClick, className = '' }) => (
  <button
    onClick={onClick}
    className={`bg-gray-200 hover:bg-gray-300 text-gray-900 font-semibold py-3 rounded-lg transition-colors ${className}`}
    aria-label={`Number ${number}`}
  >
    {number}
  </button>
);

/**
 * Operation Button Component (AI-generated)
 */
interface OperationButtonProps {
  operation: string;
  onClick: () => void;
  icon?: React.ReactNode;
  label: string;
}

const OperationButton: React.FC<OperationButtonProps> = ({ operation, onClick, icon, label }) => (
  <button
    onClick={onClick}
    className="bg-orange-500 hover:bg-orange-600 text-white font-semibold py-3 rounded-lg transition-colors flex items-center justify-center"
    aria-label={label}
  >
    {icon || operation}
  </button>
);

export default TDDCalculator;