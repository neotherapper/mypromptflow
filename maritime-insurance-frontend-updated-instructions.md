# Maritime Insurance Frontend - Updated Build Instructions

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
- **Router**: TanStack Router with file-based routing for automatic route discovery
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

Create the following directory structure with file-based routing:

```
maritime-insurance-frontend/
├── docker-compose.yml              # Docker orchestration
├── Dockerfile                      # Frontend container
├── vite.config.ts                  # Vite configuration with TanStack Router plugin
├── orval.config.js                 # API generation config
├── tailwind.config.js              # Tailwind configuration
├── src/
│   ├── main.tsx                    # App entry point
│   ├── App.tsx                     # Root component
│   ├── routeTree.gen.ts            # Auto-generated route tree
│   ├── routes/                     # File-based routing (AUTO-DISCOVERED)
│   │   ├── __root.tsx              # Root route layout
│   │   ├── index.tsx               # Home page (/)
│   │   ├── auth/                   # Authentication routes
│   │   │   ├── login.tsx           # Login page (/auth/login)
│   │   │   └── register.tsx        # Register page (/auth/register)
│   │   ├── dashboard/              # Dashboard routes
│   │   │   ├── index.tsx           # Dashboard home (/dashboard)
│   │   │   └── profile.tsx         # User profile (/dashboard/profile)
│   │   ├── quotes/                 # Quote management routes
│   │   │   ├── index.tsx           # Quotes list (/quotes)
│   │   │   ├── new.tsx             # Quote generator (/quotes/new)
│   │   │   └── $quoteId.tsx        # Quote details (/quotes/$quoteId)
│   │   ├── policies/               # Policy management routes
│   │   │   ├── index.tsx           # Policies list (/policies)
│   │   │   └── $policyId.tsx       # Policy details (/policies/$policyId)
│   │   └── vessels/                # Vessel management routes
│   │       ├── index.tsx           # Vessels list (/vessels)
│   │       ├── new.tsx             # Add vessel (/vessels/new)
│   │       └── $vesselId.tsx       # Vessel details (/vessels/$vesselId)
│   ├── api/                        # Generated API clients
│   │   ├── generated/              # Orval generated files
│   │   └── maritime-client.ts      # Custom API client
│   ├── components/                 # Reusable components
│   │   ├── ui/                     # Base UI components
│   │   ├── forms/                  # Form components
│   │   └── maritime/               # Business components
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

## Vite Configuration with File-Based Routing

Create `vite.config.ts`:

```typescript
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { TanStackRouterVite } from "@tanstack/router-plugin/vite";
import path from "path";

export default defineConfig({
  plugins: [
    // TanStack Router plugin must come before React plugin
    // This enables file-based routing with automatic route discovery
    TanStackRouterVite({
      routesDirectory: "./src/routes",
      generatedRouteTree: "./src/routeTree.gen.ts",
      routeFileIgnorePrefix: "-",
      quoteStyle: "single",
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

## File-Based Routing Implementation

### Root Route

Create `src/routes/__root.tsx`:

```typescript
import { createRootRoute, Outlet } from "@tanstack/react-router";
import { TanStackRouterDevtools } from "@tanstack/router-devtools";
import { QueryClient } from "@tanstack/react-query";
import { Navigation } from "@/components/maritime/Navigation";
import { ErrorBoundary } from "@/components/ui/ErrorBoundary";

// Root route with app layout
export const Route = createRootRoute({
  component: RootComponent,
  context: {
    queryClient: undefined as unknown as QueryClient,
  },
});

function RootComponent() {
  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-maritime-gray-50">
        <Navigation />
        <main className="container mx-auto px-4 py-8">
          <Outlet />
        </main>
      </div>
      <TanStackRouterDevtools />
    </ErrorBoundary>
  );
}
```

### Home Page

Create `src/routes/index.tsx`:

```typescript
import { createFileRoute, redirect } from "@tanstack/react-router";

export const Route = createFileRoute("/")({
  beforeLoad: ({ context }) => {
    // Redirect to dashboard if authenticated, otherwise to login
    const token = localStorage.getItem("maritime_auth_token");
    if (token) {
      throw redirect({ to: "/dashboard" });
    } else {
      throw redirect({ to: "/auth/login" });
    }
  },
});
```

### Authentication Routes

Create `src/routes/auth/login.tsx`:

```typescript
import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useForm } from "@tanstack/react-form";
import { zodValidator } from "@tanstack/zod-form-adapter";
import { z } from "zod";
import { useLogin } from "@/api/generated/auth";
import { Button } from "@/components/ui/Button";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";

const loginSchema = z.object({
  email: z.string().email("Invalid email address"),
  password: z.string().min(8, "Password must be at least 8 characters"),
});

export const Route = createFileRoute("/auth/login")({
  component: LoginPage,
});

function LoginPage() {
  const navigate = useNavigate();
  const { mutate: login, isPending } = useLogin();

  const form = useForm({
    defaultValues: {
      email: "",
      password: "",
    },
    validatorAdapter: zodValidator,
    validators: {
      onChange: loginSchema,
    },
    onSubmit: async ({ value }) => {
      try {
        const response = await login({ data: value });
        localStorage.setItem("maritime_auth_token", response.access_token);
        navigate({ to: "/dashboard" });
      } catch (error) {
        console.error("Login failed:", error);
      }
    },
  });

  return (
    <div className="min-h-screen flex items-center justify-center bg-maritime-gray-50">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Sign in to your account
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Maritime Insurance Platform
          </p>
        </div>
        
        <form
          onSubmit={(e) => {
            e.preventDefault();
            form.handleSubmit();
          }}
          className="mt-8 space-y-6"
        >
          <div className="space-y-4">
            <form.Field name="email">
              {(field) => (
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Email address
                  </label>
                  <input
                    type="email"
                    value={field.state.value}
                    onChange={(e) => field.handleChange(e.target.value)}
                    className="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-maritime-blue-500 focus:border-maritime-blue-500"
                    placeholder="Enter your email"
                  />
                  {field.state.meta.errors?.[0] && (
                    <p className="text-red-600 text-sm mt-1">
                      {field.state.meta.errors[0]}
                    </p>
                  )}
                </div>
              )}
            </form.Field>

            <form.Field name="password">
              {(field) => (
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Password
                  </label>
                  <input
                    type="password"
                    value={field.state.value}
                    onChange={(e) => field.handleChange(e.target.value)}
                    className="mt-1 appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-maritime-blue-500 focus:border-maritime-blue-500"
                    placeholder="Enter your password"
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

          <div>
            <Button
              type="submit"
              disabled={!form.state.isValid || isPending}
              className="group relative w-full flex justify-center"
            >
              {isPending ? (
                <>
                  <LoadingSpinner size="sm" className="mr-2" />
                  Signing in...
                </>
              ) : (
                "Sign in"
              )}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
```

### Dashboard Route

Create `src/routes/dashboard/index.tsx`:

```typescript
import { createFileRoute, redirect } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { getDashboardStats } from "@/api/generated/dashboard";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { DashboardCard } from "@/components/maritime/DashboardCard";

export const Route = createFileRoute("/dashboard/")({
  beforeLoad: ({ context }) => {
    // Check authentication
    const token = localStorage.getItem("maritime_auth_token");
    if (!token) {
      throw redirect({ to: "/auth/login" });
    }
  },
  component: DashboardPage,
});

function DashboardPage() {
  const { data: stats, isLoading, error } = useQuery({
    queryKey: ["dashboard-stats"],
    queryFn: getDashboardStats,
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center text-red-600">
        Error loading dashboard data
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600">Overview of your maritime insurance portfolio</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <DashboardCard
          title="Active Policies"
          value={stats?.activePolicies || 0}
          change={stats?.policyChange || 0}
          icon="DocumentTextIcon"
        />
        <DashboardCard
          title="Total Premium"
          value={`$${stats?.totalPremium?.toLocaleString() || 0}`}
          change={stats?.premiumChange || 0}
          icon="CurrencyDollarIcon"
        />
        <DashboardCard
          title="Vessels Covered"
          value={stats?.vesselsCovered || 0}
          change={stats?.vesselChange || 0}
          icon="TruckIcon"
        />
        <DashboardCard
          title="Claims This Year"
          value={stats?.claimsThisYear || 0}
          change={stats?.claimsChange || 0}
          icon="ExclamationTriangleIcon"
        />
      </div>

      {/* Additional dashboard content */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Recent Quotes
          </h2>
          {/* Quote history component */}
        </div>
        
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Policy Renewals
          </h2>
          {/* Policy renewals component */}
        </div>
      </div>
    </div>
  );
}
```

### Quote Generator Route with Search Params

Create `src/routes/quotes/new.tsx`:

```typescript
import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useState } from "react";
import { useForm } from "@tanstack/react-form";
import { zodValidator } from "@tanstack/zod-form-adapter";
import { z } from "zod";
import { VesselSelector } from "@/components/maritime/VesselSelector";
import { CoverageTypeSelector } from "@/components/maritime/CoverageTypeSelector";
import { RouteSelector } from "@/components/maritime/RouteSelector";
import { QuoteSummary } from "@/components/maritime/QuoteSummary";
import { useCreateQuote } from "@/api/generated/quotes";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { Button } from "@/components/ui/Button";

// Search params validation schema
const quoteSearchSchema = z.object({
  step: z.number().min(1).max(4).catch(1),
  vesselId: z.string().catch(""),
  coverageType: z.enum(["hull", "cargo", "liability"]).catch("hull"),
});

type QuoteSearch = z.infer<typeof quoteSearchSchema>;

// Form validation schema
const quoteFormSchema = z.object({
  vesselId: z.string().min(1, "Vessel selection is required"),
  coverageType: z.enum(["hull", "cargo", "liability"]),
  coverageAmount: z.number().min(1000, "Coverage amount must be at least $1,000"),
  voyageRoute: z.object({
    departure: z.string().min(1, "Departure port is required"),
    destination: z.string().min(1, "Destination port is required"),
    waypoints: z.array(z.string()).optional(),
    estimatedDuration: z.number().min(1, "Estimated duration is required"),
  }),
  cargoDetails: z.object({
    type: z.string().optional(),
    value: z.number().optional(),
    description: z.string().optional(),
  }).optional(),
});

type QuoteFormData = z.infer<typeof quoteFormSchema>;

export const Route = createFileRoute("/quotes/new")({
  validateSearch: quoteSearchSchema,
  component: QuoteGeneratorPage,
});

function QuoteGeneratorPage() {
  const navigate = useNavigate({ from: Route.fullPath });
  const { step, vesselId, coverageType } = Route.useSearch();
  const { mutate: createQuote, isPending } = useCreateQuote();

  // Multi-step form state
  const [currentStep, setCurrentStep] = useState(step);
  const totalSteps = 4;

  // Form configuration
  const form = useForm({
    defaultValues: {
      vesselId: vesselId || "",
      coverageType: coverageType || "hull",
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

  // Step navigation with URL updates
  const handleNextStep = () => {
    const nextStep = Math.min(currentStep + 1, totalSteps);
    setCurrentStep(nextStep);
    navigate({
      search: (prev) => ({ ...prev, step: nextStep }),
      replace: true,
    });
  };

  const handlePreviousStep = () => {
    const prevStep = Math.max(currentStep - 1, 1);
    setCurrentStep(prevStep);
    navigate({
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
        return !!values.voyageRoute.departure && !!values.voyageRoute.destination;
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
              className={`flex items-center ${step < totalSteps ? "flex-1" : ""}`}
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

### Policies Route with Search Params

Create `src/routes/policies/index.tsx`:

```typescript
import { createFileRoute, Link } from "@tanstack/react-router";
import { useQuery } from "@tanstack/react-query";
import { z } from "zod";
import { getPolicies } from "@/api/generated/policies";
import { PolicyCard } from "@/components/maritime/PolicyCard";
import { LoadingSpinner } from "@/components/ui/LoadingSpinner";
import { Button } from "@/components/ui/Button";

// Search params validation
const policiesSearchSchema = z.object({
  status: z.enum(["active", "expired", "pending", "all"]).catch("all"),
  vesselType: z.string().catch(""),
  page: z.number().min(1).catch(1),
  sortBy: z.enum(["date", "premium", "vessel", "status"]).catch("date"),
  sortOrder: z.enum(["asc", "desc"]).catch("desc"),
});

type PoliciesSearch = z.infer<typeof policiesSearchSchema>;

export const Route = createFileRoute("/policies/")({
  validateSearch: policiesSearchSchema,
  component: PoliciesPage,
});

function PoliciesPage() {
  const { status, vesselType, page, sortBy, sortOrder } = Route.useSearch();
  
  const { data: policies, isLoading, error } = useQuery({
    queryKey: ["policies", { status, vesselType, page, sortBy, sortOrder }],
    queryFn: () => getPolicies({
      status: status !== "all" ? status : undefined,
      vesselType: vesselType || undefined,
      page,
      sortBy,
      sortOrder,
    }),
  });

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center text-red-600">
        Error loading policies
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Insurance Policies</h1>
          <p className="text-gray-600">Manage your maritime insurance policies</p>
        </div>
        <Link to="/quotes/new">
          <Button>Get New Quote</Button>
        </Link>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Status
            </label>
            <select
              value={status}
              onChange={(e) => {
                // Update search params
                const newStatus = e.target.value as PoliciesSearch["status"];
                // Navigate with updated search
              }}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-maritime-blue-500"
            >
              <option value="all">All Policies</option>
              <option value="active">Active</option>
              <option value="expired">Expired</option>
              <option value="pending">Pending</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Vessel Type
            </label>
            <input
              type="text"
              value={vesselType}
              placeholder="Filter by vessel type"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-maritime-blue-500"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Sort By
            </label>
            <select
              value={sortBy}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-maritime-blue-500"
            >
              <option value="date">Date</option>
              <option value="premium">Premium</option>
              <option value="vessel">Vessel</option>
              <option value="status">Status</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Order
            </label>
            <select
              value={sortOrder}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-maritime-blue-500"
            >
              <option value="desc">Descending</option>
              <option value="asc">Ascending</option>
            </select>
          </div>
        </div>
      </div>

      {/* Policies Grid */}
      {policies && policies.items.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {policies.items.map((policy) => (
            <PolicyCard key={policy.id} policy={policy} />
          ))}
        </div>
      ) : (
        <div className="text-center py-12">
          <p className="text-gray-500 text-lg">No policies found</p>
          <Link to="/quotes/new" className="mt-4 inline-block">
            <Button>Get Your First Quote</Button>
          </Link>
        </div>
      )}

      {/* Pagination */}
      {policies && policies.totalPages > 1 && (
        <div className="flex justify-center">
          <div className="flex space-x-2">
            {Array.from({ length: policies.totalPages }, (_, i) => i + 1).map((pageNum) => (
              <Button
                key={pageNum}
                variant={pageNum === page ? "primary" : "outline"}
                size="sm"
                onClick={() => {
                  // Navigate to page
                }}
              >
                {pageNum}
              </Button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
```

## Main Application Entry

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

// Create router instance with file-based routes
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
3. **File-Based Routing**: TanStack Router discovering routes automatically
4. **Core Pages**: Login, dashboard, quote generator, policies pages implemented
5. **Navigation**: Type-safe routing with search parameters working
6. **Forms**: Multi-step quote generator with validation functioning
7. **Testing**: Unit, integration, and E2E tests passing
8. **Deployment**: Docker containers building and deploying to AWS

### Business Validation

1. **Quote Generation**: Complete multi-step quote workflow functional
2. **User Authentication**: Secure login/logout with role-based access
3. **Vessel Management**: Vessel selection and details integration
4. **Policy Dashboard**: Policy listing with filtering and search
5. **Mobile Responsiveness**: All features work on mobile devices
6. **Performance**: Fast loading times suitable for maritime connectivity

This updated instruction document provides everything needed for an AI agent to build the complete maritime insurance frontend application with file-based routing and AWS + Docker + PostgreSQL infrastructure.