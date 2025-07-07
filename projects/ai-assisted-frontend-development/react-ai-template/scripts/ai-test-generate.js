#!/usr/bin/env node

/**
 * AI Test Generation Script
 * 
 * This script uses AI assistance to automatically generate comprehensive test suites
 * for React components based on their implementation and requirements.
 * 
 * Features:
 * - Analyzes component structure and props
 * - Generates unit tests, integration tests, and accessibility tests
 * - Creates performance benchmarks
 * - Generates test data and mocks
 * - Validates test coverage requirements
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Configuration
const config = {
  testFramework: 'jest',
  testingLibrary: '@testing-library/react',
  coverageThreshold: 90,
  testTypes: ['unit', 'integration', 'accessibility', 'performance'],
  outputDir: 'src/components/**/__tests__',
  templateDir: 'scripts/templates/tests',
};

// Colors for console output
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
};

const log = {
  info: (msg) => console.log(`${colors.blue}ℹ${colors.reset} ${msg}`),
  success: (msg) => console.log(`${colors.green}✓${colors.reset} ${msg}`),
  warning: (msg) => console.log(`${colors.yellow}⚠${colors.reset} ${msg}`),
  error: (msg) => console.log(`${colors.red}✗${colors.reset} ${msg}`),
  header: (msg) => console.log(`${colors.bright}${colors.cyan}${msg}${colors.reset}`),
};

/**
 * Analyzes a React component file to extract metadata for test generation
 */
function analyzeComponent(componentPath) {
  log.info(`Analyzing component: ${componentPath}`);
  
  if (!fs.existsSync(componentPath)) {
    throw new Error(`Component file not found: ${componentPath}`);
  }

  const content = fs.readFileSync(componentPath, 'utf8');
  
  // Extract component information using regex patterns
  const componentName = extractComponentName(content);
  const props = extractProps(content);
  const hooks = extractHooks(content);
  const imports = extractImports(content);
  const exports = extractExports(content);
  
  return {
    name: componentName,
    path: componentPath,
    props,
    hooks,
    imports,
    exports,
    hasTypeScript: componentPath.endsWith('.tsx'),
    complexity: calculateComplexity(content),
  };
}

/**
 * Extracts component name from file content
 */
function extractComponentName(content) {
  const patterns = [
    /export\s+(?:const|function)\s+(\w+)/,
    /(?:const|function)\s+(\w+).*=.*React\.FC/,
    /(?:const|function)\s+(\w+).*=.*forwardRef/,
  ];
  
  for (const pattern of patterns) {
    const match = content.match(pattern);
    if (match) return match[1];
  }
  
  return 'UnknownComponent';
}

/**
 * Extracts props interface from TypeScript component
 */
function extractProps(content) {
  const interfacePattern = /interface\s+(\w+Props)\s*\{([^}]+)\}/g;
  const props = [];
  
  let match;
  while ((match = interfacePattern.exec(content)) !== null) {
    const propsContent = match[2];
    const propLines = propsContent.split('\n')
      .map(line => line.trim())
      .filter(line => line && !line.startsWith('//') && !line.startsWith('*'));
    
    for (const line of propLines) {
      const propMatch = line.match(/(\w+)(\?)?\s*:\s*([^;]+)/);
      if (propMatch) {
        props.push({
          name: propMatch[1],
          optional: Boolean(propMatch[2]),
          type: propMatch[3].trim(),
        });
      }
    }
  }
  
  return props;
}

/**
 * Extracts React hooks usage
 */
function extractHooks(content) {
  const hookPatterns = [
    /useState/g,
    /useEffect/g,
    /useCallback/g,
    /useMemo/g,
    /useRef/g,
    /useContext/g,
    /useReducer/g,
    /use\w+/g, // Custom hooks
  ];
  
  const hooks = new Set();
  
  for (const pattern of hookPatterns) {
    const matches = content.match(pattern);
    if (matches) {
      matches.forEach(hook => hooks.add(hook));
    }
  }
  
  return Array.from(hooks);
}

/**
 * Extracts import statements
 */
function extractImports(content) {
  const importPattern = /import\s+(?:\{([^}]+)\}|\*\s+as\s+(\w+)|(\w+))\s+from\s+['"]([^'"]+)['"]/g;
  const imports = [];
  
  let match;
  while ((match = importPattern.exec(content)) !== null) {
    imports.push({
      named: match[1] ? match[1].split(',').map(s => s.trim()) : [],
      namespace: match[2],
      default: match[3],
      from: match[4],
    });
  }
  
  return imports;
}

/**
 * Extracts export statements
 */
function extractExports(content) {
  const exportPattern = /export\s+(?:\{([^}]+)\}|(?:default\s+)?(?:const|function|class)\s+(\w+))/g;
  const exports = [];
  
  let match;
  while ((match = exportPattern.exec(content)) !== null) {
    if (match[1]) {
      exports.push(...match[1].split(',').map(s => s.trim()));
    } else if (match[2]) {
      exports.push(match[2]);
    }
  }
  
  return exports;
}

/**
 * Calculates component complexity based on various factors
 */
function calculateComplexity(content) {
  const factors = {
    linesOfCode: content.split('\\n').length,
    conditionalStatements: (content.match(/if\\s*\\(|\\?\\s*:|&&|\\|\\|/g) || []).length,
    loops: (content.match(/for\\s*\\(|while\\s*\\(|map\\s*\\(|forEach\\s*\\(/g) || []).length,
    functions: (content.match(/function\\s+\\w+|\\w+\\s*=\\s*\\([^)]*\\)\\s*=>/g) || []).length,
    hooks: (content.match(/use\\w+/g) || []).length,
  };
  
  const score = 
    factors.linesOfCode * 0.1 +
    factors.conditionalStatements * 2 +
    factors.loops * 3 +
    factors.functions * 1.5 +
    factors.hooks * 2;
  
  if (score < 20) return 'low';
  if (score < 50) return 'medium';
  if (score < 100) return 'high';
  return 'very-high';
}

/**
 * Generates test template based on component analysis
 */
function generateTestTemplate(analysis, testType) {
  const templates = {
    unit: generateUnitTestTemplate,
    integration: generateIntegrationTestTemplate,
    accessibility: generateAccessibilityTestTemplate,
    performance: generatePerformanceTestTemplate,
  };
  
  if (!templates[testType]) {
    throw new Error(`Unknown test type: ${testType}`);
  }
  
  return templates[testType](analysis);
}

/**
 * Generates unit test template
 */
function generateUnitTestTemplate(analysis) {
  return `/**
 * AI-Generated Unit Test Suite for ${analysis.name}
 * Generated: ${new Date().toISOString()}
 * 
 * Test Coverage:
 * - Rendering tests
 * - Props validation
 * - Event handling
 * - State management
 * - Edge cases
 */

import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { jest } from '@jest/globals';

import ${analysis.name} from '../${analysis.name}';

describe('${analysis.name}', () => {
  const defaultProps = {
    ${analysis.props.filter(p => !p.optional).map(p => 
      `${p.name}: ${generateMockValue(p.type)},`
    ).join('\\n    ')}
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('Rendering', () => {
    test('renders without crashing', () => {
      render(<${analysis.name} {...defaultProps} />);
    });

    ${analysis.props.map(prop => `
    test('renders with ${prop.name} prop', () => {
      const testValue = ${generateMockValue(prop.type)};
      render(<${analysis.name} {...defaultProps} ${prop.name}={testValue} />);
      // Add specific assertions for ${prop.name}
    });`).join('')}
  });

  describe('Props Validation', () => {
    ${analysis.props.filter(p => p.optional).map(prop => `
    test('handles missing optional prop: ${prop.name}', () => {
      const { ${prop.name}, ...requiredProps } = defaultProps;
      render(<${analysis.name} {...requiredProps} />);
      // Component should render without ${prop.name}
    });`).join('')}

    ${analysis.props.filter(p => p.type.includes('function')).map(prop => `
    test('calls ${prop.name} when appropriate', async () => {
      const mock${prop.name} = jest.fn();
      render(<${analysis.name} {...defaultProps} ${prop.name}={mock${prop.name}} />);
      
      // Trigger event that should call ${prop.name}
      // Add specific trigger logic here
      
      expect(mock${prop.name}).toHaveBeenCalled();
    });`).join('')}
  });

  ${analysis.hooks.includes('useState') ? `
  describe('State Management', () => {
    test('manages internal state correctly', async () => {
      render(<${analysis.name} {...defaultProps} />);
      
      // Test state changes
      // Add specific state testing logic here
    });
  });` : ''}

  ${analysis.hooks.includes('useEffect') ? `
  describe('Side Effects', () => {
    test('handles effects correctly', () => {
      render(<${analysis.name} {...defaultProps} />);
      
      // Test side effects
      // Add specific effect testing logic here
    });
  });` : ''}

  describe('Edge Cases', () => {
    test('handles empty data', () => {
      render(<${analysis.name} {...defaultProps} />);
      // Test with empty/null data
    });

    test('handles error conditions', () => {
      // Test error scenarios
    });
  });
});`;
}

/**
 * Generates integration test template
 */
function generateIntegrationTestTemplate(analysis) {
  return `/**
 * AI-Generated Integration Test Suite for ${analysis.name}
 * Generated: ${new Date().toISOString()}
 */

import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

import ${analysis.name} from '../${analysis.name}';

describe('${analysis.name} Integration Tests', () => {
  describe('User Workflows', () => {
    test('complete user interaction workflow', async () => {
      render(<${analysis.name} {...defaultProps} />);
      
      // Test complete user workflow
      // Add specific workflow testing logic here
    });
  });

  describe('Component Interactions', () => {
    test('interacts correctly with parent components', () => {
      // Test parent-child interactions
    });
  });
});`;
}

/**
 * Generates accessibility test template
 */
function generateAccessibilityTestTemplate(analysis) {
  return `/**
 * AI-Generated Accessibility Test Suite for ${analysis.name}
 * Generated: ${new Date().toISOString()}
 */

import React from 'react';
import { render, screen } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';
import userEvent from '@testing-library/user-event';

import ${analysis.name} from '../${analysis.name}';

expect.extend(toHaveNoViolations);

describe('${analysis.name} Accessibility Tests', () => {
  test('passes accessibility audit', async () => {
    const { container } = render(<${analysis.name} {...defaultProps} />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  test('supports keyboard navigation', async () => {
    render(<${analysis.name} {...defaultProps} />);
    
    // Test keyboard navigation
    await userEvent.tab();
    // Add specific keyboard testing logic
  });

  test('provides screen reader support', () => {
    render(<${analysis.name} {...defaultProps} />);
    
    // Test ARIA attributes and labels
    // Add specific screen reader testing logic
  });
});`;
}

/**
 * Generates performance test template
 */
function generatePerformanceTestTemplate(analysis) {
  return `/**
 * AI-Generated Performance Test Suite for ${analysis.name}
 * Generated: ${new Date().toISOString()}
 */

import React from 'react';
import { render } from '@testing-library/react';

import ${analysis.name} from '../${analysis.name}';
import { measurePerformance, PERFORMANCE_THRESHOLDS } from '../../../test/setup';

describe('${analysis.name} Performance Tests', () => {
  test('renders within performance threshold', () => {
    const { duration } = measurePerformance(() => {
      render(<${analysis.name} {...defaultProps} />);
    });
    
    expect(duration).toBeLessThan(PERFORMANCE_THRESHOLDS.RENDER_TIME);
  });

  ${analysis.complexity === 'high' || analysis.complexity === 'very-high' ? `
  test('handles large datasets efficiently', () => {
    // Test with large data sets
    const largeProps = {
      ...defaultProps,
      // Add large dataset props
    };
    
    const { duration } = measurePerformance(() => {
      render(<${analysis.name} {...largeProps} />);
    });
    
    expect(duration).toBeLessThan(PERFORMANCE_THRESHOLDS.RENDER_TIME * 2);
  });` : ''}
});`;
}

/**
 * Generates mock values based on TypeScript types
 */
function generateMockValue(type) {
  const typeMap = {
    'string': "'test'",
    'number': '42',
    'boolean': 'true',
    'Array': '[]',
    'object': '{}',
    'function': 'jest.fn()',
    'Date': 'new Date()',
    'undefined': 'undefined',
    'null': 'null',
  };

  // Handle complex types
  if (type.includes('[]')) {
    return '[]';
  }
  if (type.includes('Function') || type.includes('=>')) {
    return 'jest.fn()';
  }
  if (type.includes('|')) {
    const types = type.split('|');
    return generateMockValue(types[0].trim());
  }

  return typeMap[type] || "''";
}

/**
 * Writes test files to the file system
 */
function writeTestFiles(analysis, testSuites) {
  const testDir = path.join(path.dirname(analysis.path), '__tests__');
  
  if (!fs.existsSync(testDir)) {
    fs.mkdirSync(testDir, { recursive: true });
  }

  for (const [testType, content] of Object.entries(testSuites)) {
    const filename = `${analysis.name}.${testType}.test.${analysis.hasTypeScript ? 'tsx' : 'jsx'}`;
    const filepath = path.join(testDir, filename);
    
    fs.writeFileSync(filepath, content, 'utf8');
    log.success(`Generated ${testType} tests: ${filepath}`);
  }
}

/**
 * Runs test coverage analysis
 */
function analyzeCoverage() {
  try {
    log.info('Running test coverage analysis...');
    
    const result = execSync('npm run test:coverage', { 
      encoding: 'utf8',
      stdio: 'pipe'
    });
    
    // Parse coverage results
    const coveragePattern = /All files\\s+\\|\\s+([\\d.]+)/;
    const match = result.match(coveragePattern);
    
    if (match) {
      const coverage = parseFloat(match[1]);
      if (coverage >= config.coverageThreshold) {
        log.success(`Coverage: ${coverage}% (meets ${config.coverageThreshold}% threshold)`);
      } else {
        log.warning(`Coverage: ${coverage}% (below ${config.coverageThreshold}% threshold)`);
      }
      return coverage;
    }
  } catch (error) {
    log.error(`Coverage analysis failed: ${error.message}`);
  }
  
  return 0;
}

/**
 * Main execution function
 */
async function main() {
  const args = process.argv.slice(2);
  
  if (args.includes('--help') || args.includes('-h')) {
    console.log(`
AI Test Generator

Usage: node ai-test-generate.js [options] <component-path>

Options:
  --types <types>     Test types to generate (comma-separated)
                      Available: ${config.testTypes.join(', ')}
                      Default: all types
  --coverage         Run coverage analysis after generation
  --overwrite        Overwrite existing test files
  --help, -h         Show this help message

Examples:
  node ai-test-generate.js src/components/Button.tsx
  node ai-test-generate.js --types unit,accessibility src/components/Button.tsx
  node ai-test-generate.js --coverage src/components/Button.tsx
    `);
    return;
  }

  const componentPath = args.find(arg => !arg.startsWith('--'));
  
  if (!componentPath) {
    log.error('Component path is required');
    process.exit(1);
  }

  const typesArg = args.find(arg => arg.startsWith('--types='))?.split('=')[1];
  const testTypes = typesArg ? typesArg.split(',') : config.testTypes;
  const runCoverage = args.includes('--coverage');
  const overwrite = args.includes('--overwrite');

  try {
    log.header('🤖 AI Test Generator');
    log.info(`Generating tests for: ${componentPath}`);
    
    // Analyze component
    const analysis = analyzeComponent(componentPath);
    log.success(`Analyzed ${analysis.name} (complexity: ${analysis.complexity})`);
    
    // Check if test files already exist
    const testDir = path.join(path.dirname(analysis.path), '__tests__');
    if (fs.existsSync(testDir) && !overwrite) {
      const existingTests = fs.readdirSync(testDir)
        .filter(file => file.includes(analysis.name));
      
      if (existingTests.length > 0) {
        log.warning('Test files already exist. Use --overwrite to replace them.');
        log.info(`Existing tests: ${existingTests.join(', ')}`);
        return;
      }
    }
    
    // Generate test suites
    const testSuites = {};
    for (const testType of testTypes) {
      log.info(`Generating ${testType} tests...`);
      testSuites[testType] = generateTestTemplate(analysis, testType);
    }
    
    // Write test files
    writeTestFiles(analysis, testSuites);
    
    log.success(`Generated ${Object.keys(testSuites).length} test suites`);
    
    // Run coverage analysis if requested
    if (runCoverage) {
      const coverage = analyzeCoverage();
      
      if (coverage < config.coverageThreshold) {
        log.warning('Consider adding more test cases to improve coverage');
      }
    }
    
    log.header('✨ Test generation complete!');
    
  } catch (error) {
    log.error(`Test generation failed: ${error.message}`);
    process.exit(1);
  }
}

// Run the script
if (require.main === module) {
  main().catch(error => {
    log.error(error.message);
    process.exit(1);
  });
}

module.exports = {
  analyzeComponent,
  generateTestTemplate,
  config,
};