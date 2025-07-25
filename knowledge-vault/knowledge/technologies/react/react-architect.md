# React Architecture Context - For AI Agent Architects

## Overview

This context provides architectural guidance for AI agents working in architect roles on React applications. Focus on high-level design decisions, component architecture, state management strategies, and system-wide patterns rather than implementation details.

## Current React Version Context

**React 19.0.0** (Latest as of 2025-07-25)
- **Major Features**: Server Components, Actions, use() hook, React Compiler
- **Breaking Changes**: StrictMode behavior changes, deprecated APIs removal
- **Architecture Impact**: New patterns for server-client boundaries, improved concurrent rendering

## Architectural Patterns

### Component Architecture Patterns

#### 1. Component Composition Hierarchy
```typescript
// Recommended architectural pattern for large applications
const AppArchitecture = {
  pages: "Route-level components handling data fetching and error boundaries",
  layouts: "Shared structure components with consistent navigation and styling",
  containers: "Business logic containers that manage state and side effects",
  presentational: "Pure components focused on rendering and user interaction",
  primitives: "Lowest-level reusable components (buttons, inputs, cards)"
};

// Example architectural structure
src/
├── pages/           // Next.js pages or route components
├── layouts/         // Application layouts and shells
├── containers/      // Smart components with business logic
├── components/      // Presentational components
├── primitives/      // Basic reusable UI elements
└── hooks/          // Custom hooks for shared logic
```

#### 2. Feature-Based Architecture (Recommended for large teams)
```typescript
// Feature-based organization for scalability
src/
├── features/
│   ├── authentication/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── services/
│   │   └── types/
│   ├── dashboard/
│   │   ├── components/
│   │   ├── hooks/
│   │   └── services/
│   └── shared/           // Cross-feature utilities
├── app/                  // App-level configuration
└── shared/              // Global utilities and components
```

### State Management Architecture

#### 1. State Management Strategy Matrix
```typescript
// Choose based on application scope and complexity
const StateManagementMatrix = {
  localState: {
    use: "Component-specific state, forms, UI interactions",
    tools: "useState, useReducer",
    scope: "Single component or small component tree"
  },
  
  sharedState: {
    use: "Cross-component state, user preferences, theme",
    tools: "Context API, Zustand, Valtio",
    scope: "Multiple components, feature-level sharing"
  },
  
  globalState: {
    use: "Application-wide state, authentication, global settings",
    tools: "Redux Toolkit, Zustand, React Query + Context",
    scope: "Entire application"
  },
  
  serverState: {
    use: "Data fetching, caching, synchronization",
    tools: "TanStack Query, SWR, Apollo Client",
    scope: "Server data management"
  }
};
```

#### 2. React 19 State Patterns
```typescript
// New React 19 patterns for architects
import { use, startTransition } from 'react';

// Server Components pattern
async function DataFetchingArchitecture() {
  // Direct async/await in Server Components
  const data = await fetchCriticalData();
  return <ClientComponent data={data} />;
}

// Actions pattern for form handling
function FormArchitecture() {
  async function submitAction(formData: FormData) {
    'use server';
    // Server action handling
    await processFormSubmission(formData);
  }
  
  return <form action={submitAction}>{/* form fields */}</form>;
}

// use() hook for data fetching
function ClientDataPattern({ dataPromise }) {
  const data = use(dataPromise); // Suspends until resolved
  return <DataDisplay data={data} />;
}
```

### Performance Architecture

#### 1. Rendering Optimization Strategy
```typescript
// Architectural decisions for performance
const PerformanceArchitecture = {
  codeSpinning: {
    strategy: "Route-based code splitting with React.lazy",
    implementation: "Dynamic imports for pages and large features",
    tools: "React.lazy, Suspense, Next.js dynamic imports"
  },
  
  componentOptimization: {
    strategy: "Selective re-rendering prevention",
    implementation: "React.memo, useMemo, useCallback for expensive operations",
    architecture: "Pure components at leaf nodes, memoization at boundaries"
  },
  
  concurrentFeatures: {
    strategy: "Leverage React 18+ concurrent features",
    implementation: "startTransition for non-urgent updates, Suspense boundaries",
    architecture: "Progressive enhancement with fallback strategies"
  },
  
  bundleOptimization: {
    strategy: "Tree shaking and dead code elimination",
    implementation: "ES modules, webpack/vite optimization",
    architecture: "Modular imports, avoid default exports for libraries"
  }
};
```

#### 2. Data Flow Architecture
```typescript
// Unidirectional data flow patterns
const DataFlowArchitecture = {
  topDown: {
    pattern: "Props drilling for simple cases",
    use: "2-3 component levels maximum",
    alternative: "Context API for deeper hierarchies"
  },
  
  contextProviders: {
    pattern: "Multiple focused context providers",
    architecture: "Feature-specific contexts, avoid monolithic global context",
    optimization: "Context splitting to prevent unnecessary re-renders"
  },
  
  eventBus: {
    pattern: "Custom event system for cross-tree communication",
    use: "Rare cases where context is insufficient",
    implementation: "Custom hooks with event emitters"
  }
};
```

## Error Handling Architecture

### 1. Error Boundary Strategy
```typescript
// Hierarchical error handling architecture
const ErrorBoundaryArchitecture = {
  applicationLevel: {
    purpose: "Catch critical application errors",
    fallback: "Full application error page with recovery options",
    logging: "Comprehensive error reporting to monitoring services"
  },
  
  featureLevel: {
    purpose: "Isolate feature-specific errors",
    fallback: "Feature-specific error UI with graceful degradation",
    recovery: "Retry mechanisms and alternative flows"
  },
  
  componentLevel: {
    purpose: "Handle component-specific failures",
    fallback: "Minimal fallback UI maintaining core functionality",
    strategy: "Granular error isolation"
  }
};

// React 19 error handling improvements
class ModernErrorBoundary extends Component {
  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }
  
  componentDidCatch(error, errorInfo) {
    // Enhanced error reporting with React 19 features
    this.reportError(error, {
      ...errorInfo,
      userAgent: navigator.userAgent,
      timestamp: new Date().toISOString(),
      reactVersion: '19.0.0'
    });
  }
}
```

### 2. Async Error Handling
```typescript
// Server Components and Actions error patterns
async function ServerComponentErrorHandling() {
  try {
    const data = await fetchData();
    return <SuccessComponent data={data} />;
  } catch (error) {
    // Server-side error handling
    return <ErrorFallback error={error} />;
  }
}

// Actions error handling
async function serverActionWithErrorHandling(formData: FormData) {
  'use server';
  
  try {
    await processData(formData);
    return { success: true };
  } catch (error) {
    return { 
      success: false, 
      error: error.message,
      code: error.code 
    };
  }
}
```

## Security Architecture

### 1. Security-First Design Principles
```typescript
const SecurityArchitecture = {
  xssPreVention: {
    strategy: "React's built-in XSS protection with additional safeguards",
    implementation: "Sanitize dangerouslySetInnerHTML, validate all user inputs",
    architecture: "Content Security Policy headers, input validation layers"
  },
  
  authentication: {
    strategy: "JWT with refresh tokens or session-based auth",
    implementation: "Secure token storage, automatic token refresh",
    architecture: "Auth context with automatic redirects, protected routes"
  },
  
  dataValidation: {
    strategy: "Client and server-side validation",
    implementation: "Schema validation with Zod/Yup, API request validation",
    architecture: "Validation boundaries at component and API levels"
  }
};
```

### 2. Server Components Security
```typescript
// React 19 Server Components security considerations
async function SecureServerComponent({ userId }: { userId: string }) {
  // Server-side authorization check
  const user = await validateUserAccess(userId);
  if (!user) {
    return <UnauthorizedAccess />;
  }
  
  // Safe to fetch sensitive data on server
  const sensitiveData = await fetchUserData(userId);
  
  // Only send necessary data to client
  return <ClientComponent safeData={sanitizeForClient(sensitiveData)} />;
}
```

## Testing Architecture

### 1. Testing Strategy Pyramid
```typescript
const TestingArchitecture = {
  unitTests: {
    focus: "Individual component behavior, hooks, utilities",
    tools: "Jest, React Testing Library, Vitest",
    coverage: "80%+ for utility functions, custom hooks"
  },
  
  integrationTests: {
    focus: "Component interactions, data flow, context behavior",
    tools: "React Testing Library with MSW for API mocking",
    coverage: "Key user flows and feature interactions"
  },
  
  e2eTests: {
    focus: "Complete user journeys, critical business flows",
    tools: "Playwright, Cypress",
    coverage: "Core application paths, authentication flows"
  },
  
  visualTests: {
    focus: "UI consistency, responsive design, component variations",
    tools: "Storybook, Chromatic, Percy",
    coverage: "All component states and breakpoints"
  }
};
```

### 2. Testing Patterns for React 19
```typescript
// Testing Server Components (integration approach)
describe('Server Component Architecture', () => {
  test('renders with server data', async () => {
    // Mock server-side data fetching
    mockServerData(expectedData);
    
    // Test the full server component render
    const { result } = await renderServerComponent(<DataComponent />);
    
    expect(result).toContainData(expectedData);
  });
});

// Testing Actions
describe('Server Actions', () => {
  test('handles form submission', async () => {
    const formData = new FormData();
    formData.append('field', 'value');
    
    const result = await submitAction(formData);
    
    expect(result.success).toBe(true);
  });
});
```

## Deployment and Build Architecture

### 1. Build Optimization
```typescript
const BuildArchitecture = {
  bundling: {
    strategy: "Modern bundling with tree shaking and code splitting",
    tools: "Vite, webpack 5, esbuild",
    optimization: "Dynamic imports, chunk splitting, asset optimization"
  },
  
  serverComponents: {
    strategy: "Server/Client component separation",
    build: "Server bundle for Node.js, client bundle for browser",
    optimization: "Minimal client JavaScript, server-side rendering"
  },
  
  deployment: {
    strategy: "Edge deployment with CDN distribution",
    platforms: "Vercel, Netlify, CloudFlare Pages",
    optimization: "Geographic distribution, automatic scaling"
  }
};
```

### 2. Performance Monitoring Architecture
```typescript
// Built-in performance monitoring
import { startTransition } from 'react';

function PerformanceAwareArchitecture() {
  const handleExpensiveUpdate = () => {
    startTransition(() => {
      // Mark non-urgent updates
      setExpensiveState(newValue);
    });
  };
  
  // React DevTools Profiler integration
  return (
    <Profiler id="FeatureComponent" onRender={logPerformanceMetrics}>
      <FeatureComponent />
    </Profiler>
  );
}
```

## Architecture Decision Framework

### 1. Technology Selection Criteria
```typescript
const ArchitecturalDecisions = {
  stateManagement: {
    simple: "useState, useReducer for local state",
    complex: "Context API for feature-level, external library for global",
    serverState: "TanStack Query, SWR for API data management"
  },
  
  styling: {
    componentLevel: "CSS Modules, styled-components, emotion",
    utilityFirst: "Tailwind CSS with design system constraints",
    hybrid: "Tailwind + CSS Modules for component libraries"
  },
  
  routing: {
    spa: "React Router v6 with data loading",
    ssr: "Next.js App Router with Server Components",
    static: "Next.js with static generation"
  }
};
```

### 2. Scalability Considerations
```typescript
// Architecture patterns for team scalability
const ScalabilityArchitecture = {
  teamStructure: {
    feature: "Feature teams own complete vertical slices",
    platform: "Platform team provides shared infrastructure",
    component: "Design system team maintains component library"
  },
  
  codeSharing: {
    components: "Shared component library with versioning",
    utilities: "Shared utility packages with clear APIs",
    types: "Shared TypeScript definitions and schemas"
  },
  
  deployment: {
    microfrontends: "Module federation for independent deployment",
    monorepo: "Single repository with coordinated releases",
    libraries: "Published component libraries for cross-team usage"
  }
};
```

## Migration and Upgrade Strategies

### 1. React 19 Migration Path
```typescript
const MigrationStrategy = {
  preparation: {
    step1: "Audit current usage of deprecated APIs",
    step2: "Update React DevTools and testing tools",
    step3: "Review third-party library compatibility"
  },
  
  gradualMigration: {
    phase1: "Update React and ReactDOM, run existing tests",
    phase2: "Adopt Server Components in new features",
    phase3: "Migrate forms to use Actions",
    phase4: "Replace legacy patterns with new APIs"
  },
  
  validation: {
    testing: "Comprehensive test suite execution",
    performance: "Bundle size and runtime performance checks",
    compatibility: "Browser and device compatibility validation"
  }
};
```

## Best Practices for Architects

### 1. Decision Documentation
- Document architectural decisions with rationale
- Maintain ADRs (Architecture Decision Records) for major choices
- Regular architecture review sessions with team leads
- Performance budget definitions and monitoring

### 2. Team Guidelines
- Code review focused on architectural consistency
- Component API design standards
- State management patterns enforcement
- Performance optimization guidelines

### 3. Monitoring and Metrics
- Core Web Vitals tracking and budgets
- Error tracking with architectural context
- Bundle size monitoring and alerts
- User experience metrics correlation

## Context Usage Guidelines

**For AI Agents in Architect Role:**
1. Focus on high-level design decisions and system architecture
2. Consider scalability, maintainability, and team productivity
3. Balance performance with development velocity
4. Think in terms of system boundaries and integration points
5. Consider both current React 19 capabilities and future roadmap

**Don't Include:**
- Detailed implementation code (use frontend-dev context)
- Specific performance optimization techniques (use performance context)
- Testing implementation details (use testing context)
- Styling implementation (use design context)

This context should guide architectural thinking and high-level technical decisions for React applications.