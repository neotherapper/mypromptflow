# TypeScript Testing Context - For AI Agent Testing Specialists

## Overview

This context provides comprehensive testing guidance for AI agents working in testing specialist roles on TypeScript applications. Focus on testing strategies, type-safe testing patterns, advanced testing techniques, and quality assurance methodologies rather than basic implementation details.

## Current TypeScript Version Context

**TypeScript 5.7.2** (Latest as of 2025-07-25)
- **Testing Improvements**: Better type inference in tests, improved mock typing, enhanced assertion types
- **New Features**: Template literal types for test descriptions, improved generic constraints
- **Tool Integration**: Better Jest/Vitest integration, enhanced debugging support

## Testing Architecture and Strategy

### 1. Testing Pyramid for TypeScript Applications

```typescript
// Comprehensive testing strategy matrix
interface TypeScriptTestingStrategy {
  // Unit Tests (70% of test suite)
  unitTests: {
    scope: 'Individual functions, classes, and modules';
    tools: 'Jest, Vitest, Node Test Runner';
    coverage: '90%+ for business logic and utilities';
    characteristics: 'Fast, isolated, deterministic';
    focus: 'Pure functions, algorithms, data transformations';
  };

  // Integration Tests (20% of test suite)
  integrationTests: {
    scope: 'Component interactions, API contracts, database operations';
    tools: 'Supertest, Testing Library, MSW';
    coverage: 'Critical data flows and system boundaries';
    characteristics: 'Realistic dependencies, controlled environment';
    focus: 'Service interactions, data persistence, external APIs';
  };

  // End-to-End Tests (10% of test suite)
  e2eTests: {
    scope: 'Complete user workflows and system behavior';
    tools: 'Playwright, Cypress, Puppeteer';
    coverage: 'Core business processes and user journeys';
    characteristics: 'Full system, real browser, slow but comprehensive';
    focus: 'User scenarios, cross-browser compatibility, performance';
  };
}

// Test organization structure
interface TestOrganization {
  structure: {
    // Mirror source structure
    'src/': 'Source code';
    'tests/unit/': 'Unit tests mirroring src/ structure';
    'tests/integration/': 'Integration tests grouped by feature';
    'tests/e2e/': 'End-to-end tests grouped by user journey';
    'tests/fixtures/': 'Test data and mock fixtures';
    'tests/helpers/': 'Test utilities and custom matchers';
    'tests/setup/': 'Test environment configuration';
  };

  namingConventions: {
    unitTests: '*.test.ts for units, *.spec.ts for specifications';
    integrationTests: '*.integration.test.ts';
    e2eTests: '*.e2e.test.ts';
    mocks: '*.mock.ts or __mocks__/ directory';
    fixtures: '*.fixture.ts or fixtures/ directory';
  };

  testCategories: {
    smoke: 'Basic functionality verification';
    regression: 'Previous bug prevention';
    performance: 'Speed and resource usage validation';
    security: 'Vulnerability and access control testing';
    accessibility: 'A11y compliance and screen reader testing';
  };
}
```

### 2. Type-Safe Testing Configuration

```typescript
// Jest configuration optimized for TypeScript
// jest.config.ts
import type { Config } from 'jest';

const config: Config = {
  // TypeScript support
  preset: 'ts-jest',
  testEnvironment: 'node',
  
  // Module resolution
  moduleNameMapping: {
    '^@/(.*)$': '<rootDir>/src/$1',
    '^@components/(.*)$': '<rootDir>/src/components/$1',
    '^@utils/(.*)$': '<rootDir>/src/utils/$1',
    '^@types/(.*)$': '<rootDir>/src/types/$1',
  },
  
  // Test file patterns
  testMatch: [
    '<rootDir>/tests/**/*.test.ts',
    '<rootDir>/tests/**/*.spec.ts',
    '<rootDir>/src/**/__tests__/**/*.ts',
  ],
  
  // Coverage configuration
  coverageDirectory: 'coverage',
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/*.test.{ts,tsx}',
    '!src/**/*.spec.{ts,tsx}',
    '!src/**/__tests__/**',
    '!src/**/index.ts', // Barrel exports
  ],
  
  // Coverage thresholds
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 85,
      lines: 85,
      statements: 85,
    },
    // Per-directory thresholds
    './src/utils/': {
      branches: 90,
      functions: 95,
      lines: 95,
      statements: 95,
    },
    './src/services/': {
      branches: 85,
      functions: 90,
      lines: 90,
      statements: 90,
    },
  },
  
  // Setup files
  setupFilesAfterEnv: [
    '<rootDir>/tests/setup/jest.setup.ts'
  ],
  
  // Performance optimization
  maxWorkers: '50%',
  cache: true,
  cacheDirectory: '.jest-cache',
  
  // Error handling
  bail: false,
  verbose: true,
  errorOnDeprecated: true,
  
  // TypeScript-specific settings
  globals: {
    'ts-jest': {
      useESM: true,
      isolatedModules: true,
      tsconfig: {
        target: 'es2020',
        module: 'esnext',
        moduleResolution: 'node',
        allowSyntheticDefaultImports: true,
        esModuleInterop: true,
      },
    },
  },
  
  // Reporters
  reporters: [
    'default',
    ['jest-junit', {
      outputDirectory: 'coverage',
      outputName: 'junit.xml',
    }],
    ['jest-html-reporters', {
      publicPath: 'coverage',
      filename: 'report.html',
    }],
  ],
};

export default config;

// Vitest configuration alternative
// vitest.config.ts
import { defineConfig } from 'vitest/config';
import { resolve } from 'path';

export default defineConfig({
  test: {
    environment: 'node',
    globals: true,
    setupFiles: ['./tests/setup/vitest.setup.ts'],
    
    // Coverage with c8
    coverage: {
      provider: 'c8',
      reporter: ['text', 'html', 'lcov'],
      exclude: [
        'node_modules/',
        'tests/',
        '**/*.d.ts',
        '**/*.test.{ts,tsx}',
        '**/*.spec.{ts,tsx}',
      ],
      thresholds: {
        global: {
          branches: 80,
          functions: 85,
          lines: 85,
          statements: 85,
        },
      },
    },
    
    // Performance
    pool: 'threads',
    poolOptions: {
      threads: {
        maxThreads: 4,
        minThreads: 1,
      },
    },
  },
  
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
      '@components': resolve(__dirname, 'src/components'),
      '@utils': resolve(__dirname, 'src/utils'),
      '@types': resolve(__dirname, 'src/types'),
    },
  },
});
```

### 3. Advanced Type-Safe Testing Patterns

```typescript
// Type-safe test factories and builders
interface TestUser {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user' | 'guest';
  permissions: string[];
  createdAt: Date;
  updatedAt: Date;
}

// Builder pattern for test data
class TestUserBuilder {
  private user: Partial<TestUser> = {};
  
  static create(): TestUserBuilder {
    return new TestUserBuilder();
  }
  
  withId(id: string): this {
    this.user.id = id;
    return this;
  }
  
  withName(name: string): this {
    this.user.name = name;
    return this;
  }
  
  withEmail(email: string): this {
    this.user.email = email;
    return this;
  }
  
  withRole(role: TestUser['role']): this {
    this.user.role = role;
    return this;
  }
  
  withPermissions(permissions: string[]): this {
    this.user.permissions = permissions;
    return this;
  }
  
  asAdmin(): this {
    return this.withRole('admin')
      .withPermissions(['read', 'write', 'delete', 'admin']);
  }
  
  asRegularUser(): this {
    return this.withRole('user')
      .withPermissions(['read', 'write']);
  }
  
  asGuest(): this {
    return this.withRole('guest')
      .withPermissions(['read']);
  }
  
  build(): TestUser {
    const defaults: TestUser = {
      id: crypto.randomUUID(),
      name: 'Test User',
      email: 'test@example.com',
      role: 'user',
      permissions: ['read'],
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    
    return { ...defaults, ...this.user };
  }
  
  buildPartial(): Partial<TestUser> {
    return { ...this.user };
  }
}

// Factory functions with type safety
class TestDataFactory {
  private static sequence = 0;
  
  static createUser(overrides: Partial<TestUser> = {}): TestUser {
    const id = ++this.sequence;
    const defaults: TestUser = {
      id: `user-${id}`,
      name: `Test User ${id}`,
      email: `test${id}@example.com`,
      role: 'user',
      permissions: ['read'],
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    
    return { ...defaults, ...overrides };
  }
  
  static createUsers(count: number, template: Partial<TestUser> = {}): TestUser[] {
    return Array.from({ length: count }, () => this.createUser(template));
  }
  
  static createUserList<T extends Partial<TestUser>>(
    configs: T[]
  ): Array<TestUser & T> {
    return configs.map(config => ({ ...this.createUser(), ...config }));
  }
  
  // Type-safe fixture loading
  static async loadFixture<T>(
    fixtureName: string,
    validator: (data: unknown) => data is T
  ): Promise<T> {
    const fs = await import('fs/promises');
    const path = await import('path');
    
    const fixturePath = path.resolve(__dirname, '../fixtures', `${fixtureName}.json`);
    const rawData = await fs.readFile(fixturePath, 'utf-8');
    const data = JSON.parse(rawData);
    
    if (!validator(data)) {
      throw new Error(`Invalid fixture data for ${fixtureName}`);
    }
    
    return data;
  }
}

// Usage examples
describe('TestDataFactory', () => {
  it('creates users with type safety', () => {
    const admin = TestUserBuilder.create()
      .withName('Admin User')
      .withEmail('admin@example.com')
      .asAdmin()
      .build();
    
    expect(admin.role).toBe('admin');
    expect(admin.permissions).toContain('admin');
    
    const regularUser = TestDataFactory.createUser({
      name: 'John Doe',
      role: 'user'
    });
    
    expect(regularUser.name).toBe('John Doe');
    expect(regularUser.role).toBe('user');
  });
  
  it('creates user lists with templates', () => {
    const adminUsers = TestDataFactory.createUsers(3, { role: 'admin' });
    
    expect(adminUsers).toHaveLength(3);
    adminUsers.forEach(user => {
      expect(user.role).toBe('admin');
    });
  });
});
```

### 4. Mock and Stub Architecture

```typescript
// Type-safe mocking system
type MockedFunction<T extends (...args: any[]) => any> = jest.MockedFunction<T>;

interface MockRepository<T> {
  findById: MockedFunction<(id: string) => Promise<T | null>>;
  findAll: MockedFunction<() => Promise<T[]>>;
  create: MockedFunction<(data: Partial<T>) => Promise<T>>;
  update: MockedFunction<(id: string, data: Partial<T>) => Promise<T>>;
  delete: MockedFunction<(id: string) => Promise<void>>;
}

// Generic mock factory
class MockFactory {
  static createRepository<T>(
    entityType: new () => T,
    defaultEntities: T[] = []
  ): MockRepository<T> {
    let entities = [...defaultEntities];
    
    return {
      findById: jest.fn().mockImplementation(async (id: string) => {
        return entities.find((entity: any) => entity.id === id) || null;
      }),
      
      findAll: jest.fn().mockImplementation(async () => {
        return [...entities];
      }),
      
      create: jest.fn().mockImplementation(async (data: Partial<T>) => {
        const entity = {
          id: crypto.randomUUID(),
          createdAt: new Date(),
          updatedAt: new Date(),
          ...data,
        } as T;
        
        entities.push(entity);
        return entity;
      }),
      
      update: jest.fn().mockImplementation(async (id: string, data: Partial<T>) => {
        const index = entities.findIndex((entity: any) => entity.id === id);
        if (index === -1) {
          throw new Error(`Entity with id ${id} not found`);
        }
        
        entities[index] = {
          ...entities[index],
          ...data,
          updatedAt: new Date(),
        };
        
        return entities[index];
      }),
      
      delete: jest.fn().mockImplementation(async (id: string) => {
        const index = entities.findIndex((entity: any) => entity.id === id);
        if (index === -1) {
          throw new Error(`Entity with id ${id} not found`);
        }
        
        entities.splice(index, 1);
      }),
    };
  }
  
  // HTTP client mocking
  static createHttpClient(): {
    get: MockedFunction<(url: string, config?: any) => Promise<any>>;
    post: MockedFunction<(url: string, data?: any, config?: any) => Promise<any>>;
    put: MockedFunction<(url: string, data?: any, config?: any) => Promise<any>>;
    delete: MockedFunction<(url: string, config?: any) => Promise<any>>;
  } {
    return {
      get: jest.fn(),
      post: jest.fn(),
      put: jest.fn(),
      delete: jest.fn(),
    };
  }
  
  // Event emitter mocking
  static createEventEmitter<TEvents extends Record<string, any[]>>(): {
    on: MockedFunction<<K extends keyof TEvents>(event: K, listener: (...args: TEvents[K]) => void) => void>;
    emit: MockedFunction<<K extends keyof TEvents>(event: K, ...args: TEvents[K]) => void>;
    off: MockedFunction<<K extends keyof TEvents>(event: K, listener: (...args: TEvents[K]) => void) => void>;
  } {
    const listeners = new Map<keyof TEvents, Array<(...args: any[]) => void>>();
    
    return {
      on: jest.fn().mockImplementation(<K extends keyof TEvents>(
        event: K,
        listener: (...args: TEvents[K]) => void
      ) => {
        if (!listeners.has(event)) {
          listeners.set(event, []);
        }
        listeners.get(event)!.push(listener);
      }),
      
      emit: jest.fn().mockImplementation(<K extends keyof TEvents>(
        event: K,
        ...args: TEvents[K]
      ) => {
        const eventListeners = listeners.get(event) || [];
        eventListeners.forEach(listener => listener(...args));
      }),
      
      off: jest.fn().mockImplementation(<K extends keyof TEvents>(
        event: K,
        listener: (...args: TEvents[K]) => void
      ) => {
        const eventListeners = listeners.get(event) || [];
        const index = eventListeners.indexOf(listener);
        if (index > -1) {
          eventListeners.splice(index, 1);
        }
      }),
    };
  }
}

// Advanced mocking with MSW (Mock Service Worker)
import { rest } from 'msw';
import { setupServer } from 'msw/node';

// API response types
interface ApiResponse<T> {
  data: T;
  message: string;
  success: boolean;
}

interface ApiError {
  error: string;
  message: string;
  statusCode: number;
}

// MSW handlers with type safety
const createUserHandlers = () => [
  rest.get('/api/users', (req, res, ctx) => {
    const users = TestDataFactory.createUsers(10);
    return res(
      ctx.status(200),
      ctx.json<ApiResponse<TestUser[]>>({
        data: users,
        message: 'Users retrieved successfully',
        success: true,
      })
    );
  }),
  
  rest.get('/api/users/:id', (req, res, ctx) => {
    const { id } = req.params;
    const user = TestDataFactory.createUser({ id: id as string });
    
    return res(
      ctx.status(200),
      ctx.json<ApiResponse<TestUser>>({
        data: user,
        message: 'User retrieved successfully',
        success: true,
      })
    );
  }),
  
  rest.post('/api/users', async (req, res, ctx) => {
    const userData = await req.json<Partial<TestUser>>();
    const user = TestDataFactory.createUser(userData);
    
    return res(
      ctx.status(201),
      ctx.json<ApiResponse<TestUser>>({
        data: user,
        message: 'User created successfully',
        success: true,
      })
    );
  }),
  
  rest.put('/api/users/:id', async (req, res, ctx) => {
    const { id } = req.params;
    const updateData = await req.json<Partial<TestUser>>();
    const user = TestDataFactory.createUser({ id: id as string, ...updateData });
    
    return res(
      ctx.status(200),
      ctx.json<ApiResponse<TestUser>>({
        data: user,
        message: 'User updated successfully',
        success: true,
      })
    );
  }),
  
  rest.delete('/api/users/:id', (req, res, ctx) => {
    return res(
      ctx.status(204),
      ctx.json<ApiResponse<null>>({
        data: null,
        message: 'User deleted successfully',
        success: true,
      })
    );
  }),
];

// Error scenario handlers
const createErrorHandlers = () => [
  rest.get('/api/users/error', (req, res, ctx) => {
    return res(
      ctx.status(500),
      ctx.json<ApiError>({
        error: 'INTERNAL_SERVER_ERROR',
        message: 'Something went wrong',
        statusCode: 500,
      })
    );
  }),
  
  rest.get('/api/users/not-found', (req, res, ctx) => {
    return res(
      ctx.status(404),
      ctx.json<ApiError>({
        error: 'NOT_FOUND',
        message: 'User not found',
        statusCode: 404,
      })
    );
  }),
];

// Test server setup
export const testServer = setupServer(
  ...createUserHandlers(),
  ...createErrorHandlers()
);

// Test setup with MSW
// tests/setup/jest.setup.ts
import { testServer } from './msw-handlers';

beforeAll(() => {
  testServer.listen({
    onUnhandledRequest: 'error',
  });
});

afterEach(() => {
  testServer.resetHandlers();
});

afterAll(() => {
  testServer.close();
});
```

### 5. Property-Based Testing

```typescript
// Property-based testing with fast-check
import fc from 'fast-check';

// Custom arbitraries for domain types
const userArbitrary = fc.record({
  id: fc.uuid(),
  name: fc.string({ minLength: 1, maxLength: 100 }),
  email: fc.emailAddress(),
  role: fc.constantFrom('admin', 'user', 'guest' as const),
  permissions: fc.array(fc.string(), { minLength: 1, maxLength: 10 }),
  createdAt: fc.date(),
  updatedAt: fc.date(),
});

const validEmailArbitrary = fc.string({ minLength: 1, maxLength: 64 })
  .map(local => `${local.replace(/[^a-zA-Z0-9]/g, '')}@example.com`)
  .filter(email => email.length > 5);

// Property-based test examples
describe('User validation properties', () => {
  it('should always validate correctly formed users', () => {
    fc.assert(
      fc.property(userArbitrary, (user) => {
        const result = validateUser(user);
        expect(result.isValid).toBe(true);
        expect(result.errors).toHaveLength(0);
      })
    );
  });
  
  it('should reject users with invalid emails', () => {
    const invalidEmailArbitrary = fc.string()
      .filter(str => !str.includes('@') || str.length < 3);
    
    fc.assert(
      fc.property(
        fc.record({
          ...userArbitrary.getValue(),
          email: invalidEmailArbitrary,
        }),
        (user) => {
          const result = validateUser(user);
          expect(result.isValid).toBe(false);
          expect(result.errors).toContain('Invalid email format');
        }
      )
    );
  });
  
  it('should maintain user count after add/remove operations', () => {
    fc.assert(
      fc.property(
        fc.array(userArbitrary, { minLength: 0, maxLength: 100 }),
        userArbitrary,
        (initialUsers, newUser) => {
          const userManager = new UserManager(initialUsers);
          const initialCount = userManager.count();
          
          userManager.addUser(newUser);
          expect(userManager.count()).toBe(initialCount + 1);
          
          userManager.removeUser(newUser.id);
          expect(userManager.count()).toBe(initialCount);
        }
      )
    );
  });
  
  it('should preserve user data through serialization round-trip', () => {
    fc.assert(
      fc.property(userArbitrary, (originalUser) => {
        const serialized = JSON.stringify(originalUser);
        const deserialized = JSON.parse(serialized);
        
        // Compare all properties except dates (which become strings)
        expect(deserialized.id).toBe(originalUser.id);
        expect(deserialized.name).toBe(originalUser.name);
        expect(deserialized.email).toBe(originalUser.email);
        expect(deserialized.role).toBe(originalUser.role);
        expect(deserialized.permissions).toEqual(originalUser.permissions);
      })
    );
  });
});

// Model-based testing for complex stateful systems
interface UserManagerModel {
  users: Map<string, TestUser>;
}

class UserManagerCommands {
  static addUser(): fc.Arbitrary<{
    toString: () => string;
    check: (model: UserManagerModel) => boolean;
    run: (model: UserManagerModel, real: UserManager) => Promise<void>;
  }> {
    return fc.record({
      user: userArbitrary,
    }).map(({ user }) => ({
      toString: () => `addUser(${user.id})`,
      check: (model: UserManagerModel) => !model.users.has(user.id),
      run: async (model: UserManagerModel, real: UserManager) => {
        await real.addUser(user);
        model.users.set(user.id, user);
      },
    }));
  }
  
  static removeUser(): fc.Arbitrary<{
    toString: () => string;
    check: (model: UserManagerModel) => boolean;
    run: (model: UserManagerModel, real: UserManager) => Promise<void>;
  }> {
    return fc.string().map(userId => ({
      toString: () => `removeUser(${userId})`,
      check: (model: UserManagerModel) => model.users.has(userId),
      run: async (model: UserManagerModel, real: UserManager) => {
        await real.removeUser(userId);
        model.users.delete(userId);
      },
    }));
  }
  
  static getUser(): fc.Arbitrary<{
    toString: () => string;
    check: (model: UserManagerModel) => boolean;
    run: (model: UserManagerModel, real: UserManager) => Promise<void>;
  }> {
    return fc.string().map(userId => ({
      toString: () => `getUser(${userId})`,
      check: () => true,
      run: async (model: UserManagerModel, real: UserManager) => {
        const realUser = await real.getUser(userId);
        const modelUser = model.users.get(userId);
        
        if (modelUser) {
          expect(realUser).toEqual(modelUser);
        } else {
          expect(realUser).toBeNull();
        }
      },
    }));
  }
}

describe('UserManager model-based testing', () => {
  it('should maintain consistency between model and implementation', async () => {
    await fc.assert(
      fc.asyncProperty(
        fc.array(
          fc.oneof(
            UserManagerCommands.addUser(),
            UserManagerCommands.removeUser(),
            UserManagerCommands.getUser()
          ),
          { minLength: 1, maxLength: 50 }
        ),
        async (commands) => {
          const model: UserManagerModel = { users: new Map() };
          const real = new UserManager();
          
          for (const command of commands) {
            if (command.check(model)) {
              await command.run(model, real);
              
              // Verify model and real are consistent
              expect(real.count()).toBe(model.users.size);
            }
          }
        }
      ),
      { numRuns: 100 }
    );
  });
});
```

### 6. Performance Testing

```typescript
// Performance testing framework
interface PerformanceMetrics {
  executionTime: number;
  memoryUsage: number;
  cpuUsage: number;
  operationsPerSecond: number;
}

interface PerformanceBenchmark {
  name: string;
  warmupRuns: number;
  measurementRuns: number;
  timeoutMs: number;
  memoryThreshold: number; // MB
  opsPerSecondThreshold: number;
}

class PerformanceTester {
  private static async measureMemory(): Promise<number> {
    if ('memory' in performance) {
      return (performance as any).memory.usedJSHeapSize / 1024 / 1024; // MB
    }
    return 0;
  }
  
  private static async measureCpuUsage(): Promise<number> {
    // Simplified CPU measurement - in real scenarios, use Node.js process metrics
    const start = process.cpuUsage();
    await new Promise(resolve => setTimeout(resolve, 100));
    const end = process.cpuUsage(start);
    return (end.user + end.system) / 1000; // Convert to milliseconds
  }
  
  static async benchmark<T>(
    name: string,
    operation: () => Promise<T> | T,
    config: Partial<PerformanceBenchmark> = {}
  ): Promise<PerformanceMetrics> {
    const benchmark: PerformanceBenchmark = {
      name,
      warmupRuns: 10,
      measurementRuns: 100,
      timeoutMs: 30000,
      memoryThreshold: 100, // 100MB
      opsPerSecondThreshold: 1000,
      ...config,
    };
    
    // Warmup runs
    for (let i = 0; i < benchmark.warmupRuns; i++) {
      await operation();
    }
    
    // Measurement runs
    const startMemory = await this.measureMemory();
    const startTime = performance.now();
    const startCpu = await this.measureCpuUsage();
    
    for (let i = 0; i < benchmark.measurementRuns; i++) {
      await operation();
    }
    
    const endTime = performance.now();
    const endMemory = await this.measureMemory();
    const endCpu = await this.measureCpuUsage();
    
    const executionTime = endTime - startTime;
    const memoryUsage = endMemory - startMemory;
    const cpuUsage = endCpu - startCpu;
    const operationsPerSecond = (benchmark.measurementRuns / executionTime) * 1000;
    
    return {
      executionTime,
      memoryUsage,
      cpuUsage,
      operationsPerSecond,
    };
  }
  
  static async benchmarkComparison<T>(
    operations: Array<{
      name: string;
      operation: () => Promise<T> | T;
    }>,
    config: Partial<PerformanceBenchmark> = {}
  ): Promise<Array<{ name: string; metrics: PerformanceMetrics }>> {
    const results = [];
    
    for (const { name, operation } of operations) {
      const metrics = await this.benchmark(name, operation, config);
      results.push({ name, metrics });
    }
    
    return results;
  }
  
  static analyzeResults(
    results: Array<{ name: string; metrics: PerformanceMetrics }>,
    baseline?: string
  ): {
    fastest: string;
    slowest: string;
    comparisons: Array<{
      name: string;
      relativePerformance: number; // Multiplier relative to fastest
      memoryEfficiency: number; // MB per operation
    }>;
  } {
    const fastestOps = Math.max(...results.map(r => r.metrics.operationsPerSecond));
    const baselineResult = baseline 
      ? results.find(r => r.name === baseline)
      : results.find(r => r.metrics.operationsPerSecond === fastestOps);
    
    const fastest = results.find(r => r.metrics.operationsPerSecond === fastestOps)!.name;
    const slowest = results.reduce((prev, current) => 
      prev.metrics.operationsPerSecond < current.metrics.operationsPerSecond ? prev : current
    ).name;
    
    const comparisons = results.map(result => ({
      name: result.name,
      relativePerformance: baselineResult 
        ? result.metrics.operationsPerSecond / baselineResult.metrics.operationsPerSecond
        : result.metrics.operationsPerSecond / fastestOps,
      memoryEfficiency: result.metrics.memoryUsage / result.metrics.operationsPerSecond,
    }));
    
    return { fastest, slowest, comparisons };
  }
}

// Performance test examples
describe('Performance benchmarks', () => {
  it('should compare array processing methods', async () => {
    const testData = Array.from({ length: 10000 }, (_, i) => i);
    
    const results = await PerformanceTester.benchmarkComparison([
      {
        name: 'for-loop',
        operation: () => {
          const result = [];
          for (let i = 0; i < testData.length; i++) {
            result.push(testData[i] * 2);
          }
          return result;
        },
      },
      {
        name: 'map',
        operation: () => testData.map(x => x * 2),
      },
      {
        name: 'forEach',
        operation: () => {
          const result: number[] = [];
          testData.forEach(x => result.push(x * 2));
          return result;
        },
      },
    ], {
      measurementRuns: 1000,
    });
    
    const analysis = PerformanceTester.analyzeResults(results);
    
    console.log(`Fastest: ${analysis.fastest}`);
    console.log(`Slowest: ${analysis.slowest}`);
    
    // Assertions based on expected performance characteristics
    expect(analysis.fastest).toBe('for-loop'); // Usually fastest for simple operations
    
    // Ensure all methods complete within reasonable time
    results.forEach(result => {
      expect(result.metrics.operationsPerSecond).toBeGreaterThan(100);
      expect(result.metrics.memoryUsage).toBeLessThan(50); // MB
    });
  });
  
  it('should validate async operation performance', async () => {
    const asyncOperation = async (delay: number) => {
      await new Promise(resolve => setTimeout(resolve, delay));
      return Math.random();
    };
    
    const metrics = await PerformanceTester.benchmark(
      'async-operation',
      () => asyncOperation(1),
      {
        measurementRuns: 50,
        warmupRuns: 5,
      }
    );
    
    // Verify performance meets expectations
    expect(metrics.operationsPerSecond).toBeGreaterThan(10); // At least 10 ops/sec
    expect(metrics.executionTime).toBeLessThan(10000); // Less than 10 seconds total
    expect(metrics.memoryUsage).toBeLessThan(10); // Less than 10MB memory growth
  });
});

// Load testing utilities
class LoadTester {
  static async simulateLoad<T>(
    operation: () => Promise<T>,
    config: {
      concurrentUsers: number;
      durationMs: number;
      rampUpMs: number;
    }
  ): Promise<{
    totalOperations: number;
    successfulOperations: number;
    failedOperations: number;
    averageResponseTime: number;
    maxResponseTime: number;
    minResponseTime: number;
    operationsPerSecond: number;
  }> {
    const { concurrentUsers, durationMs, rampUpMs } = config;
    const results: Array<{ success: boolean; responseTime: number }> = [];
    const startTime = Date.now();
    
    // Create concurrent users with ramp-up
    const userPromises = Array.from({ length: concurrentUsers }, async (_, userIndex) => {
      // Stagger user start times during ramp-up period
      const userStartDelay = (rampUpMs / concurrentUsers) * userIndex;
      await new Promise(resolve => setTimeout(resolve, userStartDelay));
      
      const userStartTime = Date.now();
      
      while (Date.now() - startTime < durationMs) {
        const operationStart = performance.now();
        
        try {
          await operation();
          const responseTime = performance.now() - operationStart;
          results.push({ success: true, responseTime });
        } catch (error) {
          const responseTime = performance.now() - operationStart;
          results.push({ success: false, responseTime });
        }
        
        // Small delay between operations to prevent overwhelming
        await new Promise(resolve => setTimeout(resolve, 10));
      }
    });
    
    await Promise.all(userPromises);
    
    const successfulResults = results.filter(r => r.success);
    const responseTimes = results.map(r => r.responseTime);
    
    return {
      totalOperations: results.length,
      successfulOperations: successfulResults.length,
      failedOperations: results.length - successfulResults.length,
      averageResponseTime: responseTimes.reduce((a, b) => a + b, 0) / responseTimes.length,
      maxResponseTime: Math.max(...responseTimes),
      minResponseTime: Math.min(...responseTimes),
      operationsPerSecond: results.length / (durationMs / 1000),
    };
  }
}

// Load test example
describe('Load testing', () => {
  it('should handle concurrent user load', async () => {
    const mockApiCall = async () => {
      // Simulate API response time
      await new Promise(resolve => setTimeout(resolve, Math.random() * 100));
      
      // Simulate occasional failures
      if (Math.random() < 0.05) { // 5% failure rate
        throw new Error('Simulated API error');
      }
      
      return { data: 'success' };
    };
    
    const results = await LoadTester.simulateLoad(mockApiCall, {
      concurrentUsers: 10,
      durationMs: 5000, // 5 seconds
      rampUpMs: 1000,   // 1 second ramp-up
    });
    
    // Verify system can handle the load
    expect(results.successfulOperations).toBeGreaterThan(0);
    expect(results.failedOperations / results.totalOperations).toBeLessThan(0.1); // <10% failure rate
    expect(results.averageResponseTime).toBeLessThan(200); // <200ms average response
    expect(results.operationsPerSecond).toBeGreaterThan(1); // At least 1 op/sec
    
    console.log('Load test results:', results);
  });
});
```

### 7. Test Automation and CI Integration

```typescript
// Test runner orchestration
interface TestSuite {
  name: string;
  pattern: string;
  timeout: number;
  parallel: boolean;
  coverage: boolean;
  environment: 'node' | 'jsdom' | 'happy-dom';
}

interface TestRunResult {
  suite: string;
  passed: number;
  failed: number;
  skipped: number;
  duration: number;
  coverage: {
    lines: number;
    functions: number;
    branches: number;
    statements: number;
  };
}

class TestOrchestrator {
  private suites: TestSuite[] = [
    {
      name: 'unit',
      pattern: 'tests/unit/**/*.test.ts',
      timeout: 10000,
      parallel: true,
      coverage: true,
      environment: 'node',
    },
    {
      name: 'integration',
      pattern: 'tests/integration/**/*.test.ts',
      timeout: 30000,
      parallel: false,
      coverage: true,
      environment: 'node',
    },
    {
      name: 'e2e',
      pattern: 'tests/e2e/**/*.test.ts',
      timeout: 60000,
      parallel: false,
      coverage: false,
      environment: 'node',
    },
  ];
  
  async runSuite(suiteName: string): Promise<TestRunResult> {
    const suite = this.suites.find(s => s.name === suiteName);
    if (!suite) {
      throw new Error(`Test suite '${suiteName}' not found`);
    }
    
    const startTime = Date.now();
    
    // Configure test runner based on suite settings
    const config = {
      testMatch: [suite.pattern],
      testTimeout: suite.timeout,
      maxConcurrency: suite.parallel ? 4 : 1,
      collectCoverage: suite.coverage,
      testEnvironment: suite.environment,
    };
    
    try {
      // This would integrate with your actual test runner
      const result = await this.executeTests(config);
      
      return {
        suite: suiteName,
        passed: result.numPassedTests,
        failed: result.numFailedTests,
        skipped: result.numPendingTests,
        duration: Date.now() - startTime,
        coverage: result.coverageMap ? {
          lines: result.coverageMap.getCoverageSummary().lines.pct,
          functions: result.coverageMap.getCoverageSummary().functions.pct,
          branches: result.coverageMap.getCoverageSummary().branches.pct,
          statements: result.coverageMap.getCoverageSummary().statements.pct,
        } : { lines: 0, functions: 0, branches: 0, statements: 0 },
      };
    } catch (error) {
      throw new Error(`Test suite '${suiteName}' failed: ${error.message}`);
    }
  }
  
  async runAll(): Promise<TestRunResult[]> {
    const results: TestRunResult[] = [];
    
    for (const suite of this.suites) {
      const result = await this.runSuite(suite.name);
      results.push(result);
      
      // Stop on first failure for CI environments
      if (result.failed > 0 && process.env.CI) {
        throw new Error(`Test suite '${suite.name}' failed with ${result.failed} failures`);
      }
    }
    
    return results;
  }
  
  private async executeTests(config: any): Promise<any> {
    // Placeholder for actual test runner integration
    // This would call Jest, Vitest, or other test runner APIs
    return {
      numPassedTests: 42,
      numFailedTests: 0,
      numPendingTests: 1,
      coverageMap: null,
    };
  }
  
  generateReport(results: TestRunResult[]): string {
    const totalPassed = results.reduce((sum, r) => sum + r.passed, 0);
    const totalFailed = results.reduce((sum, r) => sum + r.failed, 0);
    const totalSkipped = results.reduce((sum, r) => sum + r.skipped, 0);
    const totalDuration = results.reduce((sum, r) => sum + r.duration, 0);
    
    const overallCoverage = results
      .filter(r => r.coverage.lines > 0)
      .reduce((acc, r) => ({
        lines: acc.lines + r.coverage.lines,
        functions: acc.functions + r.coverage.functions,
        branches: acc.branches + r.coverage.branches,
        statements: acc.statements + r.coverage.statements,
      }), { lines: 0, functions: 0, branches: 0, statements: 0 });
    
    const avgCoverage = {
      lines: overallCoverage.lines / results.length,
      functions: overallCoverage.functions / results.length,
      branches: overallCoverage.branches / results.length,
      statements: overallCoverage.statements / results.length,
    };
    
    return `
Test Results Summary
===================
Total Tests: ${totalPassed + totalFailed + totalSkipped}
Passed: ${totalPassed}
Failed: ${totalFailed}
Skipped: ${totalSkipped}
Duration: ${totalDuration}ms

Coverage Summary
================
Lines: ${avgCoverage.lines.toFixed(2)}%
Functions: ${avgCoverage.functions.toFixed(2)}%
Branches: ${avgCoverage.branches.toFixed(2)}%
Statements: ${avgCoverage.statements.toFixed(2)}%

Suite Details
=============
${results.map(r => `
${r.suite}: ${r.passed} passed, ${r.failed} failed, ${r.skipped} skipped (${r.duration}ms)
Coverage: ${r.coverage.lines.toFixed(1)}% lines, ${r.coverage.functions.toFixed(1)}% functions
`).join('')}
    `;
  }
}

// CI/CD integration script
// scripts/run-tests.ts
async function main() {
  const orchestrator = new TestOrchestrator();
  
  try {
    console.log('Starting test execution...');
    const results = await orchestrator.runAll();
    
    const report = orchestrator.generateReport(results);
    console.log(report);
    
    // Write results for CI artifacts
    const fs = await import('fs/promises');
    await fs.writeFile('test-results.json', JSON.stringify(results, null, 2));
    await fs.writeFile('test-report.txt', report);
    
    // Check if all tests passed
    const hasFailures = results.some(r => r.failed > 0);
    if (hasFailures) {
      console.error('Some tests failed');
      process.exit(1);
    }
    
    // Check coverage thresholds
    const lowCoverage = results.some(r => 
      r.coverage.lines < 80 || 
      r.coverage.functions < 85 || 
      r.coverage.branches < 80 || 
      r.coverage.statements < 85
    );
    
    if (lowCoverage) {
      console.error('Coverage thresholds not met');
      process.exit(1);
    }
    
    console.log('All tests passed with adequate coverage!');
    
  } catch (error) {
    console.error('Test execution failed:', error.message);
    process.exit(1);
  }
}

if (require.main === module) {
  main().catch(console.error);
}
```

## Best Practices for TypeScript Testing Specialists

### 1. Test Organization

- **Mirror Source Structure**: Keep test files alongside or mirroring source structure
- **Descriptive Test Names**: Use behavior-driven test descriptions
- **Group Related Tests**: Use `describe` blocks to organize related test cases
- **Test Categories**: Separate unit, integration, and e2e tests clearly
- **Fixture Management**: Centralize test data and fixtures

### 2. Type Safety in Tests

- **Type Test Data**: Use interfaces and types for all test data
- **Mock Type Safety**: Ensure mocks maintain type compatibility
- **Generic Test Utilities**: Create reusable, type-safe test helpers
- **Assertion Types**: Use TypeScript's assertion functions where appropriate
- **Avoid Any**: Never use `any` in test code; prefer proper typing

### 3. Performance and Reliability

- **Isolated Tests**: Ensure tests don't depend on each other
- **Deterministic Results**: Avoid flaky tests with proper async handling
- **Performance Budgets**: Set and monitor test execution performance
- **Resource Cleanup**: Properly clean up resources in teardown
- **Parallel Execution**: Design tests to run safely in parallel

### 4. Coverage and Quality

- **Meaningful Coverage**: Focus on behavior coverage, not just line coverage
- **Edge Case Testing**: Test boundary conditions and error scenarios
- **Property-Based Testing**: Use property-based tests for complex logic
- **Mutation Testing**: Consider mutation testing for critical code paths
- **Code Quality Gates**: Enforce quality thresholds in CI/CD

## Context Usage Guidelines

**For AI Agents in Testing Specialist Role:**
1. Focus on comprehensive testing strategies and advanced testing patterns
2. Include specific testing configurations and frameworks
3. Consider test reliability, maintainability, and performance
4. Think about CI/CD integration and automation
5. Use TypeScript 5.7+ testing features and type safety patterns

**Don't Include:**
- Basic testing syntax (use frontend-dev context)
- Implementation details (use implementation contexts)
- High-level project architecture (use architect context)
- Basic TypeScript concepts (use fundamental learning contexts)

This context should guide comprehensive testing implementation and testing strategy decisions for TypeScript applications.