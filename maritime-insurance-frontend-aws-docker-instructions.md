# Maritime Insurance Frontend - Complete Build Instructions

Build a complete maritime insurance B2C platform frontend using React 19, TanStack ecosystem, AWS deployment with Docker Compose, and PostgreSQL database integration.

## Project Scope & Business Context

**Platform Type**: B2C maritime insurance platform with controlled authentication
**Target Users**: Ship brokers, ship owners, cargo owners (office-based professionals)
**Core Features**: Quote generator, vessel management, policy dashboard, controlled registration/authentication
**Business Model**: Maritime insurance with complex vessel data, route planning, and coverage types

**Key Business Requirements**:

- Multi-step quote generator with vessel selection and route planning
- Type-safe API integration with FastAPI backend
- Responsive design for office and mobile usage
- Performance optimization for maritime connectivity (ships/ports)
- Role-based access control for different user types
- Document upload capabilities for insurance documents

## Technology Stack Architecture

### Frontend Stack

- **Framework**: React 19 with concurrent features and automatic batching
- **Build Tool**: Vite with hot module replacement and optimized bundling
- **Package Manager**: pnpm for efficient dependency management
- **Language**: TypeScript in strict mode with full type inference
- **Router**: TanStack Router for type-safe routing with search parameters
- **State Management**: TanStack Query for server state, TanStack Form for forms
- **API Client**: Orval for auto-generated TypeScript hooks from OpenAPI specs
- **Styling**: Tailwind CSS for utility-first responsive design
- **Testing**: Vitest + React Testing Library + Playwright for E2E

### Infrastructure Stack

- **Cloud Platform**: AWS with ECS/Fargate deployment
- **Containerization**: Docker Compose for local and production orchestration
- **Database**: PostgreSQL with Docker containers and proper migrations
- **Frontend Hosting**: AWS CloudFront + S3 or ECS web service
- **CI/CD**: GitHub Actions with AWS deployment automation
- **Environment Management**: AWS Systems Manager Parameter Store

## Complete Project Setup

### Step 1: Initial Project Scaffolding

```bash
# Initialize with Vite + React + TypeScript
pnpm create vite . --template react-ts

# Install core dependencies
pnpm install

# Install TanStack ecosystem
pnpm add @tanstack/react-query @tanstack/react-router @tanstack/react-form
pnpm add @tanstack/router-plugin @tanstack/zod-form-adapter
pnpm add @tanstack/react-query-devtools @tanstack/router-devtools

# Install API and validation
pnpm add orval axios zod

# Install styling and UI
pnpm add tailwindcss postcss autoprefixer

# Install testing dependencies
pnpm add -D vitest @testing-library/react @testing-library/jest-dom
pnpm add -D playwright @playwright/test

# Install development tools
pnpm add -D eslint prettier eslint-plugin-react-hooks
pnpm add -D @types/node concurrently rimraf

# Enforce pnpm usage
pnpm add -D only-allow

# Initialize Tailwind CSS
npx tailwindcss init -p
```

### Step 2: Project Structure Setup

Create the following directory structure:

```
maritime-insurance-frontend/
├── docker-compose.yml              # Docker orchestration
├── Dockerfile                      # Frontend container
├── vite.config.ts                  # Vite configuration
├── orval.config.js                 # API generation config
├── tailwind.config.js              # Tailwind configuration
├── src/
│   ├── main.tsx                    # App entry point
│   ├── App.tsx                     # Root component
│   ├── router.tsx                  # Route definitions
│   ├── api/                        # Generated API clients
│   │   ├── generated/              # Orval generated files
│   │   └── maritime-client.ts      # Custom API client
│   ├── components/                 # Reusable components
│   │   ├── ui/                     # Base UI components
│   │   ├── forms/                  # Form components
│   │   └── maritime/               # Business components
│   ├── pages/                      # Page components
│   │   ├── auth/                   # Authentication pages
│   │   ├── dashboard/              # Dashboard pages
│   │   ├── quotes/                 # Quote generator pages
│   │   └── policies/               # Policy management
│   ├── hooks/                      # Custom React hooks
│   ├── utils/                      # Utility functions
│   ├── types/                      # TypeScript type definitions
│   └── styles/                     # Global styles
├── tests/                          # Test files
│   ├── unit/                       # Unit tests
│   ├── integration/                # Integration tests
│   └── e2e/                        # End-to-end tests
└── docs/                           # Documentation
```

### Step 3: Package.json Configuration

```json
{
  "name": "maritime-insurance-frontend",
  "version": "1.0.0",
  "type": "module",
  "engines": {
    "node": ">=18.0.0",
    "pnpm": ">=8.0.0"
  },
  "scripts": {
    "preinstall": "npx only-allow pnpm",

    "// === API Generation ===": "",
    "api:generate": "orval --config orval.config.js",
    "api:watch": "orval --config orval.config.js --watch",

    "// === Development ===": "",
    "predev": "pnpm api:generate",
    "dev": "vite --host 0.0.0.0 --port 5173",
    "dev:api": "concurrently \"pnpm api:watch\" \"pnpm dev\"",
    "dev:docker": "docker compose up --build",

    "// === Type Safety ===": "",
    "type-check": "tsc --noEmit",
    "type-check:watch": "tsc --noEmit --watch",

    "// === Building ===": "",
    "prebuild": "pnpm api:generate && pnpm type-check",
    "build": "vite build",
    "build:docker": "docker build -t maritime-frontend .",
    "build:analyze": "vite build --mode analyze",

    "// === Testing ===": "",
    "test": "vitest",
    "test:ui": "vitest --ui",
    "test:coverage": "vitest --coverage",
    "test:e2e": "playwright test",
    "test:e2e:ui": "playwright test --ui",

    "// === Quality ===": "",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "lint:fix": "eslint . --ext ts,tsx --fix",
    "format": "prettier --write .",
    "format:check": "prettier --check .",

    "// === Docker ===": "",
    "docker:up": "docker compose up -d",
    "docker:down": "docker compose down",
    "docker:logs": "docker compose logs -f",
    "docker:reset": "docker compose down -v && docker compose up --build",

    "// === Deployment ===": "",
    "deploy:staging": "pnpm build && aws s3 sync dist/ s3://maritime-staging --delete",
    "deploy:production": "pnpm build && aws s3 sync dist/ s3://maritime-production --delete",

    "// === Maintenance ===": "",
    "clean": "rimraf dist node_modules/.vite",
    "reset": "pnpm clean && pnpm install",
    "update:deps": "pnpm update --interactive --latest"
  }
}
```

## Docker Configuration

### Docker Compose Setup

Create `docker-compose.yml`:

```yaml
version: "3.8"

services:
  # PostgreSQL Database
  postgres:
    image: postgres:15-alpine
    container_name: maritime-postgres
    environment:
      POSTGRES_DB: maritime_insurance
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./database/init:/docker-entrypoint-initdb.d
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 30s
      timeout: 10s
      retries: 3

  # FastAPI Backend (when running locally)
  api:
    build:
      context: ../maritime-insurance-backend
      dockerfile: Dockerfile
    container_name: maritime-api
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/maritime_insurance
      ENVIRONMENT: development
    ports:
      - "8000:8000"
    depends_on:
      postgres:
        condition: service_healthy
    volumes:
      - ../maritime-insurance-backend:/app
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Frontend Development Server
  frontend:
    build:
      context: .
      dockerfile: Dockerfile.dev
    container_name: maritime-frontend
    environment:
      VITE_API_URL: http://api:8000
      VITE_APP_ENV: development
    ports:
      - "5173:5173"
    depends_on:
      api:
        condition: service_healthy
    volumes:
      - .:/app
      - /app/node_modules
    command: pnpm dev

volumes:
  postgres_data:
```

### Frontend Dockerfile

Create `Dockerfile` for production:

```dockerfile
# Multi-stage build for production
FROM node:20-alpine AS base
RUN corepack enable
RUN corepack prepare pnpm@latest --activate

# Dependencies stage
FROM base AS dependencies
WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

# Build stage
FROM base AS builder
WORKDIR /app
COPY . .
COPY --from=dependencies /app/node_modules ./node_modules
RUN pnpm build

# Production stage
FROM nginx:alpine AS production
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

Create `Dockerfile.dev` for development:

```dockerfile
FROM node:20-alpine
RUN corepack enable
RUN corepack prepare pnpm@latest --activate

WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN pnpm install

COPY . .
EXPOSE 5173
CMD ["pnpm", "dev", "--host", "0.0.0.0"]
```

## Vite Configuration

Create `vite.config.ts`:

```typescript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { tanstackRouter } from "@tanstack/router-plugin/vite";
import path from "path";

export default defineConfig({
  plugins: [
    // TanStack Router plugin must come before React plugin
    tanstackRouter({
      target: "react",
      autoCodeSplitting: true,
    }),
    react(),
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
      "@/components": path.resolve(__dirname, "./src/components"),
      "@/hooks": path.resolve(__dirname, "./src/hooks"),
      "@/utils": path.resolve(__dirname, "./src/utils"),
      "@/types": path.resolve(__dirname, "./src/types"),
      "@/api": path.resolve(__dirname, "./src/api"),
    },
  },
  server: {
    host: "0.0.0.0",
    port: 5173,
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
  build: {
    outDir: "dist",
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ["react", "react-dom"],
          tanstack: ["@tanstack/react-query", "@tanstack/react-router"],
          utils: ["axios", "zod"],
        },
      },
    },
  },
  define: {
    __APP_VERSION__: JSON.stringify(process.env.npm_package_version),
  },
});
```

## API Client Configuration

### Orval Configuration

Create `orval.config.js`:

```javascript
export default {
  maritimeInsurance: {
    input: {
      target: "http://localhost:8000/openapi.json",
      validation: false, // Skip validation for development speed
    },
    output: {
      target: "src/api/generated",
      client: "react-query",
      mode: "tags-split", // Organize by OpenAPI tags
      mock: true, // Generate mock data for testing
      prettier: true,
      override: {
        mutator: {
          path: "./src/api/maritime-client.ts",
          name: "maritimeApiInstance",
        },
        query: {
          useQuery: true,
          useInfinite: true,
          useInfiniteQueryParam: "page",
          options: {
            staleTime: 300000, // 5 minutes for maritime data
            retry: (failureCount, error) => {
              // Aggressive retry for ship connectivity issues
              if (failureCount < 10) return true;
              return false;
            },
            refetchOnWindowFocus: true,
          },
        },
        header: [
          "// Maritime Insurance API Client",
          "// Auto-generated by Orval - DO NOT EDIT",
          "",
          "/* eslint-disable */",
          "// @ts-nocheck",
          "",
        ],
      },
    },
    hooks: {
      afterAllFilesWrite: ["prettier --write src/api/generated"],
    },
  },
};
```

### Custom API Client

Create `src/api/maritime-client.ts`:

```typescript
import axios, { AxiosRequestConfig, AxiosResponse } from "axios";

// Create axios instance with maritime-specific configuration
export const maritimeApiInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
  timeout: 30000, // 30 seconds for slow ship connections
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor for authentication
maritimeApiInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("maritime_auth_token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
maritimeApiInstance.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("maritime_auth_token");
      window.location.href = "/auth/login";
    }
    return Promise.reject(error);
  }
);

// Export the custom instance for Orval
export default maritimeApiInstance;

// Types for maritime-specific errors
export interface MaritimeApiError {
  message: string;
  code: string;
  details?: Record<string, any>;
}

// Utility function for handling API errors
export const handleApiError = (error: any): MaritimeApiError => {
  if (error.response?.data) {
    return error.response.data;
  }
  return {
    message: error.message || "An unexpected error occurred",
    code: "UNKNOWN_ERROR",
  };
};
```

## React Application Setup

### Main Application Entry

Create `src/main.tsx`:

```typescript
import React from "react";
import ReactDOM from "react-dom/client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { RouterProvider, createRouter } from "@tanstack/react-router";
import { routeTree } from "./routeTree.gen";
import "./styles/index.css";

// Create query client with maritime-optimized settings
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes for maritime data
      retry: (failureCount, error: any) => {
        // Aggressive retry for ship connectivity issues
        if (failureCount < 10) return true;
        if (error?.response?.status === 401) return false;
        return false;
      },
      refetchOnWindowFocus: true,
    },
    mutations: {
      retry: 3,
      onError: (error) => {
        console.error("API Mutation Error:", error);
      },
    },
  },
});

// Create router instance
const router = createRouter({
  routeTree,
  context: {
    queryClient,
  },
});

// Register router for TypeScript
declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router;
  }
}

// Render application
ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  </React.StrictMode>
);
```

### Root Route Configuration

Create `src/router.tsx`:

```typescript
import {
  createRootRoute,
  createRoute,
  createRouter,
  Outlet,
} from "@tanstack/react-router";
import { TanStackRouterDevtools } from "@tanstack/router-devtools";
import { QueryClient } from "@tanstack/react-query";
import App from "./App";
import { LoginPage } from "./pages/auth/LoginPage";
import { DashboardPage } from "./pages/dashboard/DashboardPage";
import { QuoteGeneratorPage } from "./pages/quotes/QuoteGeneratorPage";
import { PoliciesPage } from "./pages/policies/PoliciesPage";

// Root route with app layout
export const rootRoute = createRootRoute({
  component: () => (
    <>
      <App />
      <TanStackRouterDevtools />
    </>
  ),
});

// Authentication routes
const authRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/auth",
  component: () => <Outlet />,
});

const loginRoute = createRoute({
  getParentRoute: () => authRoute,
  path: "/login",
  component: LoginPage,
});

// Protected routes
const dashboardRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/dashboard",
  component: DashboardPage,
  beforeLoad: async ({ context }) => {
    // Check authentication
    const token = localStorage.getItem("maritime_auth_token");
    if (!token) {
      throw new Error("Not authenticated");
    }
  },
});

// Quote generator with type-safe search params
const quotesRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/quotes",
  component: () => <Outlet />,
});

const quoteGeneratorRoute = createRoute({
  getParentRoute: () => quotesRoute,
  path: "/new",
  validateSearch: (search: Record<string, unknown>) => ({
    step: (search.step as number) || 1,
    vesselId: (search.vesselId as string) || "",
    coverageType:
      (search.coverageType as "hull" | "cargo" | "liability") || "hull",
  }),
  component: QuoteGeneratorPage,
});

// Policies management
const policiesRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/policies",
  validateSearch: (search: Record<string, unknown>) => ({
    status: (search.status as "active" | "expired" | "all") || "all",
    vesselType: (search.vesselType as string) || "",
    page: Number(search.page) || 1,
    sortBy: (search.sortBy as "date" | "premium" | "vessel") || "date",
    sortOrder: (search.sortOrder as "asc" | "desc") || "desc",
  }),
  component: PoliciesPage,
});

// Create route tree
export const routeTree = rootRoute.addChildren([
  authRoute.addChildren([loginRoute]),
  dashboardRoute,
  quotesRoute.addChildren([quoteGeneratorRoute]),
  policiesRoute,
]);

// Router configuration
export const router = createRouter({
  routeTree,
  context: {
    queryClient: undefined as unknown as QueryClient,
  },
});
```

### Root App Component

Create `src/App.tsx`:

```typescript
import { Outlet, useRouter } from "@tanstack/react-router";
import { useEffect } from "react";
import { Navigation } from "./components/maritime/Navigation";
import { ErrorBoundary } from "./components/ui/ErrorBoundary";
import { LoadingSpinner } from "./components/ui/LoadingSpinner";

export default function App() {
  const router = useRouter();

  // Initialize app
  useEffect(() => {
    // Check authentication status
    const token = localStorage.getItem("maritime_auth_token");
    if (!token && window.location.pathname !== "/auth/login") {
      router.navigate({ to: "/auth/login" });
    }
  }, [router]);

  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-maritime-gray-50">
        <Navigation />
        <main className="container mx-auto px-4 py-8">
          <React.Suspense
            fallback={
              <div className="flex items-center justify-center h-64">
                <LoadingSpinner size="lg" />
              </div>
            }
          >
            <Outlet />
          </React.Suspense>
        </main>
      </div>
    </ErrorBoundary>
  );
}
```

## Core Components Implementation

### Navigation Component

Create `src/components/maritime/Navigation.tsx`:

```typescript
import { Link, useRouter, useRouterState } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import {
  HomeIcon,
  DocumentTextIcon,
  CurrencyDollarIcon,
  UserIcon,
  ArrowRightOnRectangleIcon,
} from "@heroicons/react/24/outline";
import { useCurrentUser } from "@/hooks/useAuth";

export function Navigation() {
  const router = useRouter();
  const routerState = useRouterState();
  const { data: user, isLoading } = useCurrentUser();

  const handleLogout = () => {
    localStorage.removeItem("maritime_auth_token");
    router.navigate({ to: "/auth/login" });
  };

  const navigationItems = [
    {
      name: "Dashboard",
      href: "/dashboard",
      icon: HomeIcon,
    },
    {
      name: "Generate Quote",
      href: "/quotes/new",
      icon: CurrencyDollarIcon,
    },
    {
      name: "Policies",
      href: "/policies",
      icon: DocumentTextIcon,
    },
  ];

  if (isLoading) {
    return (
      <nav className="bg-maritime-blue-900 text-white px-4 py-3">
        <div className="flex items-center justify-between">
          <div className="h-8 w-48 bg-maritime-blue-800 rounded animate-pulse" />
          <div className="h-8 w-32 bg-maritime-blue-800 rounded animate-pulse" />
        </div>
      </nav>
    );
  }

  return (
    <nav className="bg-maritime-blue-900 text-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo and main navigation */}
          <div className="flex items-center space-x-8">
            <Link
              to="/dashboard"
              className="text-xl font-bold text-white hover:text-maritime-blue-200 transition-colors"
            >
              Maritime Insurance
            </Link>

            <div className="hidden md:flex space-x-4">
              {navigationItems.map((item) => {
                const isActive = routerState.location.pathname.startsWith(
                  item.href
                );
                return (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={`flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      isActive
                        ? "bg-maritime-blue-800 text-white"
                        : "text-maritime-blue-200 hover:bg-maritime-blue-800 hover:text-white"
                    }`}
                  >
                    <item.icon className="h-5 w-5" />
                    <span>{item.name}</span>
                  </Link>
                );
              })}
            </div>
          </div>

          {/* User menu */}
          <div className="flex items-center space-x-4">
            {user && (
              <div className="flex items-center space-x-3">
                <div className="flex items-center space-x-2">
                  <UserIcon className="h-5 w-5 text-maritime-blue-200" />
                  <span className="text-sm font-medium">{user.name}</span>
                  <span className="text-xs text-maritime-blue-300">
                    ({user.role})
                  </span>
                </div>
                <button
                  onClick={handleLogout}
                  className="flex items-center space-x-1 px-3 py-2 rounded-md text-sm font-medium text-maritime-blue-200 hover:bg-maritime-blue-800 hover:text-white transition-colors"
                >
                  <ArrowRightOnRectangleIcon className="h-4 w-4" />
                  <span>Logout</span>
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
```

### Quote Generator Page

Create `src/pages/quotes/QuoteGeneratorPage.tsx`:

```typescript
import { useState } from "react";
import { useForm } from "@tanstack/react-form";
import { zodValidator } from "@tanstack/zod-form-adapter";
import { useNavigate, useSearch } from "@tanstack/react-router";
import { z } from "zod";
import { VesselSelector } from "@/components/maritime/VesselSelector";
import { CoverageTypeSelector } from "@/components/maritime/CoverageTypeSelector";
import { RouteSelector } from "@/components/maritime/RouteSelector";
import { QuoteSummary } from "@/components/maritime/QuoteSummary";
import { useCreateQuote } from "@/api/generated/quotes";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { Button } from "@/components/ui/Button";

// Validation schema
const quoteFormSchema = z.object({
  vesselId: z.string().min(1, "Vessel selection is required"),
  coverageType: z.enum(["hull", "cargo", "liability"], {
    required_error: "Coverage type is required",
  }),
  coverageAmount: z
    .number()
    .min(1000, "Coverage amount must be at least $1,000"),
  voyageRoute: z.object({
    departure: z.string().min(1, "Departure port is required"),
    destination: z.string().min(1, "Destination port is required"),
    waypoints: z.array(z.string()).optional(),
    estimatedDuration: z.number().min(1, "Estimated duration is required"),
  }),
  cargoDetails: z
    .object({
      type: z.string().optional(),
      value: z.number().optional(),
      description: z.string().optional(),
    })
    .optional(),
});

type QuoteFormData = z.infer<typeof quoteFormSchema>;

export function QuoteGeneratorPage() {
  const navigate = useNavigate();
  const search = useSearch({ from: "/quotes/new" });
  const { mutate: createQuote, isPending } = useCreateQuote();

  // Multi-step form state
  const [currentStep, setCurrentStep] = useState(search.step || 1);
  const totalSteps = 4;

  // Form configuration
  const form = useForm({
    defaultValues: {
      vesselId: search.vesselId || "",
      coverageType: search.coverageType || "hull",
      coverageAmount: 0,
      voyageRoute: {
        departure: "",
        destination: "",
        waypoints: [],
        estimatedDuration: 0,
      },
      cargoDetails: {
        type: "",
        value: 0,
        description: "",
      },
    } as QuoteFormData,
    validatorAdapter: zodValidator,
    validators: {
      onChange: quoteFormSchema,
    },
    onSubmit: async ({ value }) => {
      try {
        const quote = await createQuote({ data: value });
        navigate({
          to: "/quotes/$quoteId",
          params: { quoteId: quote.id },
        });
      } catch (error) {
        console.error("Quote creation failed:", error);
      }
    },
  });

  // Step navigation
  const handleNextStep = () => {
    const nextStep = Math.min(currentStep + 1, totalSteps);
    setCurrentStep(nextStep);
    navigate({
      to: "/quotes/new",
      search: (prev) => ({ ...prev, step: nextStep }),
      replace: true,
    });
  };

  const handlePreviousStep = () => {
    const prevStep = Math.max(currentStep - 1, 1);
    setCurrentStep(prevStep);
    navigate({
      to: "/quotes/new",
      search: (prev) => ({ ...prev, step: prevStep }),
      replace: true,
    });
  };

  // Step validation
  const isStepValid = (step: number): boolean => {
    const values = form.state.values;
    switch (step) {
      case 1:
        return !!values.vesselId;
      case 2:
        return !!values.coverageType && values.coverageAmount > 0;
      case 3:
        return (
          !!values.voyageRoute.departure && !!values.voyageRoute.destination
        );
      case 4:
        return true; // Summary step
      default:
        return false;
    }
  };

  const renderStepContent = () => {
    switch (currentStep) {
      case 1:
        return (
          <form.Field name="vesselId">
            {(field) => (
              <VesselSelector
                value={field.state.value}
                onChange={field.handleChange}
                error={field.state.meta.errors?.[0]}
              />
            )}
          </form.Field>
        );

      case 2:
        return (
          <div className="space-y-6">
            <form.Field name="coverageType">
              {(field) => (
                <CoverageTypeSelector
                  value={field.state.value}
                  onChange={field.handleChange}
                  error={field.state.meta.errors?.[0]}
                />
              )}
            </form.Field>

            <form.Field name="coverageAmount">
              {(field) => (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Coverage Amount (USD)
                  </label>
                  <input
                    type="number"
                    value={field.state.value}
                    onChange={(e) => field.handleChange(Number(e.target.value))}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-maritime-blue-500"
                    placeholder="Enter coverage amount"
                  />
                  {field.state.meta.errors?.[0] && (
                    <p className="text-red-600 text-sm mt-1">
                      {field.state.meta.errors[0]}
                    </p>
                  )}
                </div>
              )}
            </form.Field>
          </div>
        );

      case 3:
        return (
          <form.Field name="voyageRoute">
            {(field) => (
              <RouteSelector
                value={field.state.value}
                onChange={field.handleChange}
                error={field.state.meta.errors?.[0]}
              />
            )}
          </form.Field>
        );

      case 4:
        return (
          <QuoteSummary
            formData={form.state.values}
            onSubmit={form.handleSubmit}
            isLoading={isPending}
          />
        );

      default:
        return null;
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      {/* Progress indicator */}
      <div className="mb-8">
        <div className="flex items-center justify-between">
          {Array.from({ length: totalSteps }, (_, i) => i + 1).map((step) => (
            <div
              key={step}
              className={`flex items-center ${
                step < totalSteps ? "flex-1" : ""
              }`}
            >
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
                  step <= currentStep
                    ? "bg-maritime-blue-600 text-white"
                    : "bg-gray-200 text-gray-600"
                }`}
              >
                {step}
              </div>
              {step < totalSteps && (
                <div
                  className={`flex-1 h-1 mx-4 ${
                    step < currentStep ? "bg-maritime-blue-600" : "bg-gray-200"
                  }`}
                />
              )}
            </div>
          ))}
        </div>

        <div className="mt-4">
          <h1 className="text-2xl font-bold text-gray-900">
            Generate Insurance Quote
          </h1>
          <p className="text-gray-600">
            Step {currentStep} of {totalSteps}: {getStepTitle(currentStep)}
          </p>
        </div>
      </div>

      {/* Step content */}
      <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
        {renderStepContent()}
      </div>

      {/* Navigation buttons */}
      <div className="flex justify-between">
        <Button
          variant="outline"
          onClick={handlePreviousStep}
          disabled={currentStep === 1}
        >
          Previous
        </Button>

        <div className="flex space-x-4">
          {currentStep < totalSteps ? (
            <Button
              onClick={handleNextStep}
              disabled={!isStepValid(currentStep)}
            >
              Next
            </Button>
          ) : (
            <Button
              onClick={() => form.handleSubmit()}
              disabled={!isStepValid(currentStep) || isPending}
            >
              {isPending ? (
                <>
                  <LoadingSpinner size="sm" className="mr-2" />
                  Generating Quote...
                </>
              ) : (
                "Generate Quote"
              )}
            </Button>
          )}
        </div>
      </div>
    </div>
  );
}

function getStepTitle(step: number): string {
  switch (step) {
    case 1:
      return "Select Vessel";
    case 2:
      return "Choose Coverage";
    case 3:
      return "Define Route";
    case 4:
      return "Review & Submit";
    default:
      return "";
  }
}
```

## Tailwind CSS Configuration

Update `tailwind.config.js`:

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        maritime: {
          blue: {
            50: "#eff6ff",
            100: "#dbeafe",
            200: "#bfdbfe",
            300: "#93c5fd",
            400: "#60a5fa",
            500: "#3b82f6",
            600: "#1e40af",
            700: "#1e3a8a",
            800: "#1e3a8a",
            900: "#1a365d",
          },
          gray: {
            50: "#f8fafc",
            100: "#f1f5f9",
            200: "#e2e8f0",
            300: "#cbd5e1",
            400: "#94a3b8",
            500: "#64748b",
            600: "#475569",
            700: "#334155",
            800: "#1e293b",
            900: "#0f172a",
          },
          green: {
            50: "#f0fdf4",
            100: "#dcfce7",
            200: "#bbf7d0",
            300: "#86efac",
            400: "#4ade80",
            500: "#22c55e",
            600: "#16a34a",
            700: "#15803d",
            800: "#166534",
            900: "#14532d",
          },
          red: {
            50: "#fef2f2",
            100: "#fee2e2",
            200: "#fecaca",
            300: "#fca5a5",
            400: "#f87171",
            500: "#ef4444",
            600: "#dc2626",
            700: "#b91c1c",
            800: "#991b1b",
            900: "#7f1d1d",
          },
        },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
      spacing: {
        18: "4.5rem",
        88: "22rem",
      },
      boxShadow: {
        maritime:
          "0 4px 6px -1px rgba(30, 58, 138, 0.1), 0 2px 4px -1px rgba(30, 58, 138, 0.06)",
      },
    },
  },
  plugins: [require("@tailwindcss/forms"), require("@tailwindcss/typography")],
};
```

## Testing Configuration

### Vitest Configuration

Create `vitest.config.ts`:

```typescript
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: ["./src/tests/setup.ts"],
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html"],
      exclude: [
        "node_modules/",
        "src/tests/",
        "src/api/generated/",
        "**/*.d.ts",
      ],
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
```

Create `src/tests/setup.ts`:

```typescript
import "@testing-library/jest-dom";
import { expect, afterEach } from "vitest";
import { cleanup } from "@testing-library/react";
import * as matchers from "@testing-library/jest-dom/matchers";

// Extend Vitest's expect with jest-dom matchers
expect.extend(matchers);

// Clean up after each test case
afterEach(() => {
  cleanup();
});

// Mock IntersectionObserver
global.IntersectionObserver = class IntersectionObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  unobserve() {}
};

// Mock ResizeObserver
global.ResizeObserver = class ResizeObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  unobserve() {}
};
```

### Playwright Configuration

Create `playwright.config.ts`:

```typescript
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: "html",
  use: {
    baseURL: "http://localhost:5173",
    trace: "on-first-retry",
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
    {
      name: "firefox",
      use: { ...devices["Desktop Firefox"] },
    },
    {
      name: "webkit",
      use: { ...devices["Desktop Safari"] },
    },
    {
      name: "Mobile Chrome",
      use: { ...devices["Pixel 5"] },
    },
  ],
  webServer: {
    command: "pnpm dev",
    url: "http://localhost:5173",
    reuseExistingServer: !process.env.CI,
  },
});
```

## AWS Deployment Configuration

### GitHub Actions Workflow

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy Maritime Insurance Frontend

on:
  push:
    branches: [main, staging]
  pull_request:
    branches: [main]

env:
  AWS_REGION: us-east-1
  ECR_REPOSITORY: maritime-frontend
  ECS_SERVICE: maritime-frontend-service
  ECS_CLUSTER: maritime-cluster

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "pnpm"

      - name: Install pnpm
        uses: pnpm/action-setup@v2
        with:
          version: 8

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Type check
        run: pnpm type-check

      - name: Run tests
        run: pnpm test:coverage

      - name: Run E2E tests
        run: pnpm test:e2e

      - name: Upload coverage reports
        uses: codecov/codecov-action@v3

  build-and-deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' || github.ref == 'refs/heads/staging'

    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}

      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v2

      - name: Build, tag, and push image to Amazon ECR
        id: build-image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
          echo "image=$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG" >> $GITHUB_OUTPUT

      - name: Fill in the new image ID in the Amazon ECS task definition
        id: task-def
        uses: aws-actions/amazon-ecs-render-task-definition@v1
        with:
          task-definition: .aws/task-definition.json
          container-name: maritime-frontend
          image: ${{ steps.build-image.outputs.image }}

      - name: Deploy Amazon ECS task definition
        uses: aws-actions/amazon-ecs-deploy-task-definition@v1
        with:
          task-definition: ${{ steps.task-def.outputs.task-definition }}
          service: ${{ env.ECS_SERVICE }}
          cluster: ${{ env.ECS_CLUSTER }}
          wait-for-service-stability: true
```

### ECS Task Definition

Create `.aws/task-definition.json`:

```json
{
  "family": "maritime-frontend",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "executionRoleArn": "arn:aws:iam::ACCOUNT:role/ecsTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::ACCOUNT:role/ecsTaskRole",
  "containerDefinitions": [
    {
      "name": "maritime-frontend",
      "image": "ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/maritime-frontend:latest",
      "portMappings": [
        {
          "containerPort": 80,
          "protocol": "tcp"
        }
      ],
      "essential": true,
      "environment": [
        {
          "name": "NODE_ENV",
          "value": "production"
        }
      ],
      "secrets": [
        {
          "name": "VITE_API_URL",
          "valueFrom": "arn:aws:ssm:us-east-1:ACCOUNT:parameter/maritime/api-url"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/maritime-frontend",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost/ || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3,
        "startPeriod": 60
      }
    }
  ]
}
```

## Environment Configuration

### Environment Variables

Create `.env.example`:

```bash
# API Configuration
VITE_API_URL=http://localhost:8000
VITE_APP_ENV=development

# Feature Flags
VITE_ENABLE_DEVTOOLS=true
VITE_ENABLE_MOCK_DATA=false

# AWS Configuration (for production)
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key

# Database Configuration (for Docker Compose)
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/maritime_insurance
```

### TypeScript Configuration

Update `tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@/components/*": ["./src/components/*"],
      "@/hooks/*": ["./src/hooks/*"],
      "@/utils/*": ["./src/utils/*"],
      "@/types/*": ["./src/types/*"],
      "@/api/*": ["./src/api/*"]
    }
  },
  "include": ["src", "tests"],
  "references": [{ "path": "./tsconfig.node.json" }]
}
```

## Quality Assurance & Validation

### Code Quality Standards

- **TypeScript**: Strict mode enabled with zero `any` types allowed
- **ESLint**: React hooks rules, TypeScript recommended rules
- **Prettier**: Consistent code formatting with maritime-specific rules
- **Bundle Size**: Target <500KB gzipped for initial load
- **Performance**: Core Web Vitals compliance (LCP <2.5s, FID <100ms, CLS <0.1)
- **Accessibility**: WCAG 2.1 AA compliance for insurance industry standards

### Testing Requirements

- **Unit Tests**: 90%+ coverage for business logic components
- **Integration Tests**: API integration and form validation testing
- **E2E Tests**: Critical user flows (login, quote generation, policy management)
- **Performance Tests**: Lighthouse CI integration with performance budgets

### Security Considerations

- **Authentication**: JWT token management with secure storage
- **API Security**: Request/response validation, rate limiting awareness
- **Data Protection**: Insurance data encryption in transit and at rest
- **Environment Security**: Secure environment variable management

## Deployment Workflow

### Local Development

```bash
# Start full development environment
pnpm docker:up

# Start development server only
pnpm dev

# Generate API client from updated OpenAPI spec
pnpm api:generate

# Run tests
pnpm test
pnpm test:e2e
```

### Production Deployment

```bash
# Build for production
pnpm build

# Deploy to AWS staging
git push origin staging

# Deploy to AWS production
git push origin main
```

## Success Criteria

### Technical Milestones

1. **Project Setup**: All dependencies installed, Docker environment running
2. **API Integration**: Orval generating TypeScript clients successfully
3. **Core Pages**: Login, dashboard, quote generator, policies pages implemented
4. **Navigation**: Type-safe routing with TanStack Router working
5. **Forms**: Multi-step quote generator with validation functioning
6. **Testing**: Unit, integration, and E2E tests passing
7. **Deployment**: Docker containers building and deploying to AWS

### Business Validation

1. **Quote Generation**: Complete multi-step quote workflow functional
2. **User Authentication**: Secure login/logout with role-based access
3. **Vessel Management**: Vessel selection and details integration
4. **Policy Dashboard**: Policy listing with filtering and search
5. **Mobile Responsiveness**: All features work on mobile devices
6. **Performance**: Fast loading times suitable for maritime connectivity

This comprehensive instruction document provides everything needed for an AI agent to build the complete maritime insurance frontend application with your decided technology stack and AWS + Docker + PostgreSQL infrastructure.
