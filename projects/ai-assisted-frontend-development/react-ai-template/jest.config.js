/**
 * AI-Optimized Jest Configuration for React Development
 * 
 * This configuration is specifically designed for AI-assisted React development
 * with comprehensive testing capabilities including:
 * - Unit tests with React Testing Library
 * - Integration tests
 * - Accessibility tests with jest-axe
 * - Performance tests
 * - Visual regression tests
 */

module.exports = {
  // Test environment
  testEnvironment: 'jsdom',
  
  // TypeScript support
  preset: 'ts-jest/presets/default-esm',
  extensionsToTreatAsEsm: ['.ts', '.tsx'],
  
  // Module resolution
  moduleNameMapping: {
    // Path aliases
    '^@/(.*)$': '<rootDir>/src/$1',
    '^@components/(.*)$': '<rootDir>/src/components/$1',
    '^@hooks/(.*)$': '<rootDir>/src/hooks/$1',
    '^@utils/(.*)$': '<rootDir>/src/utils/$1',
    '^@stores/(.*)$': '<rootDir>/src/stores/$1',
    '^@styles/(.*)$': '<rootDir>/src/styles/$1',
    '^@test/(.*)$': '<rootDir>/src/test/$1',
    '^@types/(.*)$': '<rootDir>/src/types/$1',
    
    // CSS modules and assets
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
    '\\.(jpg|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2|mp4|webm|wav|mp3|m4a|aac|oga)$': 
      '<rootDir>/src/test/__mocks__/fileMock.js',
  },
  
  // Setup files
  setupFilesAfterEnv: [
    '<rootDir>/src/test/setup.ts'
  ],
  
  // Test file patterns
  testMatch: [
    '<rootDir>/src/**/__tests__/**/*.{ts,tsx}',
    '<rootDir>/src/**/*.(test|spec).{ts,tsx}',
  ],
  
  // Files to collect coverage from
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/test/**/*',
    '!src/**/*.stories.{ts,tsx}',
    '!src/index.tsx',
    '!src/reportWebVitals.ts',
    '!src/setupTests.ts',
  ],
  
  // Coverage thresholds for AI-generated code quality
  coverageThreshold: {
    global: {
      branches: 85,
      functions: 85,
      lines: 85,
      statements: 85,
    },
    // Specific thresholds for critical components
    './src/components/examples/': {
      branches: 90,
      functions: 90,
      lines: 90,
      statements: 90,
    },
  },
  
  // Coverage reporters
  coverageReporters: [
    'text',
    'text-summary',
    'html',
    'lcov',
    'json-summary',
  ],
  
  // Coverage directory
  coverageDirectory: '<rootDir>/coverage',
  
  // Transform configuration
  transform: {
    '^.+\\.(ts|tsx)$': ['ts-jest', {
      useESM: true,
      tsconfig: {
        jsx: 'react-jsx',
      },
    }],
  },
  
  // Module file extensions
  moduleFileExtensions: [
    'ts',
    'tsx',
    'js',
    'jsx',
    'json',
  ],
  
  // Test timeout for performance tests
  testTimeout: 10000,
  
  // Globals for AI testing utilities
  globals: {
    'ts-jest': {
      useESM: true,
      tsconfig: {
        jsx: 'react-jsx',
      },
    },
    __DEV__: true,
    __PROD__: false,
    __AI_TOOLS_ENABLED__: true,
  },
  
  // Projects for different test types
  projects: [
    {
      displayName: 'unit',
      testMatch: [
        '<rootDir>/src/**/__tests__/**/*.test.{ts,tsx}',
        '<rootDir>/src/**/*.test.{ts,tsx}',
      ],
      testPathIgnorePatterns: [
        'integration.test',
        'accessibility.test',
        'performance.test',
        'e2e.test',
      ],
    },
    {
      displayName: 'integration',
      testMatch: [
        '<rootDir>/src/**/*.integration.test.{ts,tsx}',
      ],
      setupFilesAfterEnv: [
        '<rootDir>/src/test/setup.ts',
        '<rootDir>/src/test/integration-setup.ts',
      ],
    },
    {
      displayName: 'accessibility',
      testMatch: [
        '<rootDir>/src/**/*.accessibility.test.{ts,tsx}',
      ],
      setupFilesAfterEnv: [
        '<rootDir>/src/test/setup.ts',
        '<rootDir>/src/test/accessibility-setup.ts',
      ],
    },
    {
      displayName: 'performance',
      testMatch: [
        '<rootDir>/src/**/*.performance.test.{ts,tsx}',
      ],
      setupFilesAfterEnv: [
        '<rootDir>/src/test/setup.ts',
        '<rootDir>/src/test/performance-setup.ts',
      ],
      testTimeout: 30000, // Longer timeout for performance tests
    },
  ],
  
  // Watch mode configuration
  watchPlugins: [
    'jest-watch-typeahead/filename',
    'jest-watch-typeahead/testname',
  ],
  
  // Cache configuration
  cacheDirectory: '<rootDir>/node_modules/.cache/jest',
  
  // Clear mocks between tests
  clearMocks: true,
  
  // Restore mocks after each test
  restoreMocks: true,
  
  // Verbose output for AI development
  verbose: true,
  
  // Error handling
  errorOnDeprecated: true,
  
  // Test results processor for AI analytics
  testResultsProcessor: '<rootDir>/scripts/test-results-processor.js',
  
  // Custom reporters for AI integration
  reporters: [
    'default',
    [
      'jest-html-reporters',
      {
        publicPath: './coverage/html-report',
        filename: 'report.html',
        expand: true,
        hideIcon: false,
        pageTitle: 'AI React Template Test Report',
      },
    ],
    [
      'jest-junit',
      {
        outputDirectory: './coverage',
        outputName: 'junit.xml',
        ancestorSeparator: ' › ',
        uniqueOutputName: 'false',
        suiteNameTemplate: '{filepath}',
        classNameTemplate: '{classname}',
        titleTemplate: '{title}',
      },
    ],
  ],
  
  // Notify configuration for development
  notify: true,
  notifyMode: 'failure-change',
  
  // Snapshot configuration
  snapshotSerializers: [
    'jest-serializer-html',
  ],
  
  // Maximum worker configuration for AI development
  maxWorkers: '50%',
  
  // Collect coverage for untested files
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/test/**/*',
    '!src/**/*.stories.{ts,tsx}',
    '!src/index.tsx',
    '!src/reportWebVitals.ts',
  ],
  
  // Force exit after tests complete
  forceExit: false,
  
  // Detect open handles for debugging
  detectOpenHandles: true,
  
  // Custom test environment options
  testEnvironmentOptions: {
    url: 'http://localhost:3000',
  },
};

// AI-specific test configuration for different environments
const environments = {
  development: {
    collectCoverage: false,
    verbose: true,
    notify: true,
  },
  ci: {
    collectCoverage: true,
    verbose: false,
    notify: false,
    maxWorkers: 2,
    ci: true,
  },
  production: {
    collectCoverage: true,
    verbose: false,
    notify: false,
    bail: true,
  },
};

// Apply environment-specific configuration
const env = process.env.NODE_ENV || 'development';
if (environments[env]) {
  Object.assign(module.exports, environments[env]);
}

// AI testing performance optimizations
if (process.env.AI_PERFORMANCE_MODE === 'true') {
  module.exports.maxWorkers = 1;
  module.exports.testTimeout = 60000;
  module.exports.setupFilesAfterEnv.push('<rootDir>/src/test/ai-performance-setup.ts');
}

// Visual regression testing configuration
if (process.env.VISUAL_REGRESSION === 'true') {
  module.exports.setupFilesAfterEnv.push('<rootDir>/src/test/visual-regression-setup.ts');
  module.exports.testMatch.push('<rootDir>/src/**/*.visual.test.{ts,tsx}');
}

// AI accessibility testing configuration
if (process.env.AI_ACCESSIBILITY_MODE === 'true') {
  module.exports.setupFilesAfterEnv.push('<rootDir>/src/test/ai-accessibility-setup.ts');
  module.exports.coverageThreshold.global.branches = 95;
  module.exports.coverageThreshold.global.functions = 95;
  module.exports.coverageThreshold.global.lines = 95;
  module.exports.coverageThreshold.global.statements = 95;
}