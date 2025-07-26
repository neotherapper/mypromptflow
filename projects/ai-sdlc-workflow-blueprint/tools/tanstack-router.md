# TanStack Router - Type-Safe React Router for Modern Applications

## Overview

TanStack Router is a fully type-safe React router with built-in caching, 1st-class search-param APIs, and unmatched developer experience. It provides zero-configuration TypeScript integration with React 19, perfect alignment with TanStack Query, and advanced features specifically designed for complex maritime insurance applications requiring robust navigation and state management.

## Key Benefits

### 1. **100% Type-Safe Routing**
- Full TypeScript inference for routes, params, and search parameters
- Compile-time validation of navigation and links
- Auto-completion for all route paths and parameters
- Zero runtime errors from invalid routes

### 2. **First-Class Search Parameter Support**
- Type-safe search parameter handling with validation
- Automatic serialization/deserialization of complex objects
- Perfect for maritime insurance filters (vessel type, coverage, dates)
- Seamless integration with form state management

### 3. **Built-in Route-Level Data Loading**
- Integrated with TanStack Query for optimal caching
- Parallel data fetching with route preloading
- Automatic error boundaries and loading states
- Perfect for maritime insurance data requirements

### 4. **React 19 Optimized**
- Leverages React 19 concurrent features
- Automatic code splitting with Suspense integration
- Enhanced performance with new React capabilities
- Future-proof architecture design

## Configuration Examples

### Basic TanStack Router Setup

```typescript
// src/router.tsx
import { createRouter, createRoute, createRootRoute } from '@tanstack/react-router';
import { QueryClient } from '@tanstack/react-query';

// Root route configuration
const rootRoute = createRootRoute({
  component: () => (
    <div>
      <nav>
        <Link to="/dashboard">Dashboard</Link>
        <Link to="/policies">Policies</Link>
        <Link to="/quotes">Quotes</Link>
      </nav>
      <hr />
      <Outlet />
    </div>
  ),
});

// Dashboard route
const dashboardRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/dashboard',
  component: DashboardComponent,
});

// Policies route with type-safe parameters
const policiesRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/policies',
  validateSearch: (search: Record<string, unknown>) => ({
    status: (search.status as string) || 'all',
    vesselType: (search.vesselType as string) || '',
    page: Number(search.page) || 1,
  }),
  component: PoliciesComponent,
});

// Create router tree
const routeTree = rootRoute.addChildren([
  dashboardRoute,
  policiesRoute,
]);

// Export typed router
export const router = createRouter({ 
  routeTree,
  defaultPreload: 'intent', // Preload on hover/focus
});

// Infer router type for use throughout app
declare module '@tanstack/react-router' {
  interface Register {
    router: typeof router;
  }
}
```

### Advanced Maritime Insurance Configuration

```typescript
// src/routes/maritime-routes.tsx
import { createRoute, createRootRoute, redirect } from '@tanstack/react-router';
import { queryOptions } from '@tanstack/react-query';
import { useGetPolicies, useGetVessels } from '../api/generated/maritime-api';

// Root route with authentication check
const rootRoute = createRootRoute({
  beforeLoad: ({ context, location }) => {
    // Type-safe authentication check
    if (!context.auth.isAuthenticated) {
      throw redirect({
        to: '/login',
        search: {
          redirect: location.href,
        },
      });
    }
  },
  component: RootComponent,
});

// Policy detail route with data loading
const policyRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/policies/$policyId',
  parseParams: (params) => ({
    policyId: params.policyId!,
  }),
  validateSearch: (search: Record<string, unknown>) => ({
    tab: (search.tab as 'details' | 'documents' | 'claims') || 'details',
    edit: Boolean(search.edit),
  }),
  // Integrate with TanStack Query for data loading
  loader: ({ params, context: { queryClient } }) => {
    const policyQuery = queryOptions({
      queryKey: ['policy', params.policyId],
      queryFn: () => getPolicyById(params.policyId),
      staleTime: 5 * 60 * 1000, // 5 minutes for maritime data
    });
    
    // Preload policy data
    return queryClient.ensureQueryData(policyQuery);
  },
  component: PolicyDetailComponent,
  errorComponent: PolicyErrorComponent,
  pendingComponent: PolicyLoadingComponent,
});

// Quote generation with complex search parameters
const quoteRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/quotes/new',
  validateSearch: (search: Record<string, unknown>) => {
    const schema = z.object({
      vesselId: z.string().optional(),
      coverageType: z.enum(['hull', 'cargo', 'liability']).optional(),
      startDate: z.string().datetime().optional(),
      endDate: z.string().datetime().optional(),
      // Complex maritime insurance parameters
      vesselValue: z.coerce.number().positive().optional(),
      routeRegions: z.array(z.string()).optional(),
      cargoTypes: z.array(z.string()).optional(),
    });
    
    return schema.parse(search);
  },
  component: QuoteGeneratorComponent,
});

// Vessel management with infinite scrolling
const vesselsRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/vessels',
  validateSearch: (search: Record<string, unknown>) => ({
    filter: (search.filter as string) || '',
    vesselType: search.vesselType as string | undefined,
    flag: search.flag as string | undefined,
    sortBy: (search.sortBy as 'name' | 'type' | 'flag' | 'lastUpdate') || 'name',
    sortOrder: (search.sortOrder as 'asc' | 'desc') || 'asc',
  }),
  loader: ({ search, context: { queryClient } }) => {
    // Preload vessel data based on search parameters
    const vesselsQuery = queryOptions({
      queryKey: ['vessels', search],
      queryFn: () => getVessels(search),
      staleTime: 10 * 60 * 1000, // 10 minutes for vessel data
    });
    
    return queryClient.ensureQueryData(vesselsQuery);
  },
  component: VesselsListComponent,
});
```

## Maritime Insurance Application Examples

### 1. Policy Management Dashboard

```typescript
// src/components/PolicyDashboard.tsx
import { useNavigate, useSearch } from '@tanstack/react-router';
import { useGetPolicies } from '../api/generated/maritime-api';

const PolicyDashboard: React.FC = () => {
  const navigate = useNavigate();
  
  // Type-safe search parameter access
  const { status, vesselType, page } = useSearch({
    from: '/policies',
  });

  // Integrated data loading with TanStack Query
  const { data: policies, isLoading } = useGetPolicies({
    status: status !== 'all' ? status : undefined,
    vesselType: vesselType || undefined,
    page,
    limit: 20,
  });

  const handleFilterChange = (newFilters: {
    status?: string;
    vesselType?: string;
    page?: number;
  }) => {
    // Type-safe navigation with search parameters
    navigate({
      to: '/policies',
      search: (prev) => ({
        ...prev,
        ...newFilters,
      }),
      replace: true, // Don't add to history for filters
    });
  };

  const handlePolicySelect = (policyId: string) => {
    // Type-safe navigation to policy details
    navigate({
      to: '/policies/$policyId',
      params: { policyId },
      search: { tab: 'details' },
    });
  };

  if (isLoading) return <PolicyLoadingSkeleton />;

  return (
    <div className="policy-dashboard">
      <div className="filters">
        <select 
          value={status} 
          onChange={(e) => handleFilterChange({ status: e.target.value, page: 1 })}
        >
          <option value="all">All Statuses</option>
          <option value="active">Active</option>
          <option value="expired">Expired</option>
          <option value="pending">Pending</option>
        </select>
        
        <select 
          value={vesselType} 
          onChange={(e) => handleFilterChange({ vesselType: e.target.value, page: 1 })}
        >
          <option value="">All Vessel Types</option>
          <option value="cargo">Cargo Ship</option>
          <option value="tanker">Tanker</option>
          <option value="container">Container Ship</option>
        </select>
      </div>

      <div className="policy-list">
        {policies?.map(policy => (
          <PolicyCard 
            key={policy.id}
            policy={policy}
            onClick={() => handlePolicySelect(policy.id)}
          />
        ))}
      </div>

      <Pagination
        currentPage={page}
        totalPages={Math.ceil((policies?.total || 0) / 20)}
        onPageChange={(newPage) => handleFilterChange({ page: newPage })}
      />
    </div>
  );
};
```

### 2. Quote Generation Wizard with Form Integration

```typescript
// src/components/QuoteWizard.tsx
import { useForm } from '@tanstack/react-form';
import { useNavigate, useSearch } from '@tanstack/react-router';
import { zodValidator } from '@tanstack/zod-form-adapter';
import { z } from 'zod';

// Maritime insurance quote schema
const quoteSchema = z.object({
  vesselId: z.string().min(1, 'Vessel selection required'),
  coverageType: z.enum(['hull', 'cargo', 'liability']),
  coverageAmount: z.number().positive('Coverage amount must be positive'),
  startDate: z.date(),
  endDate: z.date(),
  voyageRoute: z.object({
    departure: z.string().min(1, 'Departure port required'),
    destination: z.string().min(1, 'Destination port required'),
    waypoints: z.array(z.string()).optional(),
  }),
  cargoDetails: z.object({
    type: z.string().optional(),
    value: z.number().positive().optional(),
    hazardous: z.boolean().default(false),
  }).optional(),
});

const QuoteWizard: React.FC = () => {
  const navigate = useNavigate();
  
  // Get initial values from URL search parameters
  const searchParams = useSearch({
    from: '/quotes/new',
  });

  // Integrated form with TanStack Form
  const form = useForm({
    defaultValues: {
      vesselId: searchParams.vesselId || '',
      coverageType: searchParams.coverageType || 'hull',
      coverageAmount: 0,
      startDate: searchParams.startDate ? new Date(searchParams.startDate) : new Date(),
      endDate: searchParams.endDate ? new Date(searchParams.endDate) : new Date(),
      voyageRoute: {
        departure: '',
        destination: '',
        waypoints: [],
      },
      cargoDetails: {
        type: '',
        value: 0,
        hazardous: false,
      },
    },
    validatorAdapter: zodValidator,
    validators: {
      onChange: quoteSchema,
    },
    onSubmit: async ({ value }) => {
      try {
        // Generate quote using Orval-generated hook
        const quote = await createQuote({ data: value });
        
        // Navigate to quote results with type safety
        navigate({
          to: '/quotes/$quoteId',
          params: { quoteId: quote.id },
          search: { generated: true },
        });
      } catch (error) {
        console.error('Quote generation failed:', error);
      }
    },
  });

  // Update URL when form values change (debounced)
  const updateSearchParams = useMemo(
    () => debounce((values: any) => {
      navigate({
        to: '/quotes/new',
        search: {
          vesselId: values.vesselId || undefined,
          coverageType: values.coverageType,
          startDate: values.startDate?.toISOString(),
          endDate: values.endDate?.toISOString(),
        },
        replace: true,
      });
    }, 500),
    [navigate]
  );

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        e.stopPropagation();
        form.handleSubmit();
      }}
      className="quote-wizard"
    >
      <div className="wizard-steps">
        {/* Step 1: Vessel Selection */}
        <div className="step">
          <h3>Select Vessel</h3>
          <form.Field
            name="vesselId"
            children={(field) => (
              <div>
                <VesselSelector
                  value={field.state.value}
                  onChange={(vesselId) => {
                    field.handleChange(vesselId);
                    updateSearchParams(form.state.values);
                  }}
                />
                {field.state.meta.errors && (
                  <span className="error">{field.state.meta.errors[0]}</span>
                )}
              </div>
            )}
          />
        </div>

        {/* Step 2: Coverage Details */}
        <div className="step">
          <h3>Coverage Details</h3>
          <form.Field
            name="coverageType"
            children={(field) => (
              <div>
                <label>Coverage Type</label>
                <select
                  value={field.state.value}
                  onChange={(e) => {
                    field.handleChange(e.target.value as any);
                    updateSearchParams(form.state.values);
                  }}
                >
                  <option value="hull">Hull Insurance</option>
                  <option value="cargo">Cargo Insurance</option>
                  <option value="liability">Liability Insurance</option>
                </select>
              </div>
            )}
          />
        </div>

        {/* Step 3: Voyage Route */}
        <div className="step">
          <h3>Voyage Route</h3>
          <form.Field
            name="voyageRoute.departure"
            children={(field) => (
              <div>
                <label>Departure Port</label>
                <PortSelector
                  value={field.state.value}
                  onChange={field.handleChange}
                />
              </div>
            )}
          />
          
          <form.Field
            name="voyageRoute.destination"
            children={(field) => (
              <div>
                <label>Destination Port</label>
                <PortSelector
                  value={field.state.value}
                  onChange={field.handleChange}
                />
              </div>
            )}
          />
        </div>
      </div>

      <div className="wizard-actions">
        <button type="submit" disabled={!form.state.isValid}>
          Generate Quote
        </button>
      </div>
    </form>
  );
};
```

### 3. Route-Level Data Loading with Error Boundaries

```typescript
// src/routes/policy-detail.tsx
import { createRoute } from '@tanstack/react-router';
import { queryOptions } from '@tanstack/react-query';

const policyDetailRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/policies/$policyId',
  parseParams: (params) => ({
    policyId: params.policyId!,
  }),
  validateSearch: (search: Record<string, unknown>) => ({
    tab: (search.tab as 'details' | 'documents' | 'claims' | 'history') || 'details',
    edit: Boolean(search.edit),
    documentId: search.documentId as string | undefined,
  }),
  // Pre-load all necessary data
  loader: async ({ params, search, context: { queryClient } }) => {
    const policyQuery = queryOptions({
      queryKey: ['policy', params.policyId],
      queryFn: () => getPolicyById(params.policyId),
      staleTime: 5 * 60 * 1000,
    });

    const documentsQuery = queryOptions({
      queryKey: ['policy-documents', params.policyId],
      queryFn: () => getPolicyDocuments(params.policyId),
      staleTime: 10 * 60 * 1000,
    });

    const claimsQuery = queryOptions({
      queryKey: ['policy-claims', params.policyId],
      queryFn: () => getPolicyClaims(params.policyId),
      staleTime: 5 * 60 * 1000,
    });

    // Load data in parallel
    const [policy, documents, claims] = await Promise.all([
      queryClient.ensureQueryData(policyQuery),
      queryClient.ensureQueryData(documentsQuery),
      queryClient.ensureQueryData(claimsQuery),
    ]);

    // Validate policy access permissions
    if (!policy || !hasAccessToPolicy(policy, context.auth.user)) {
      throw new Error('Access denied to this policy');
    }

    return { policy, documents, claims };
  },
  component: PolicyDetailComponent,
  errorComponent: ({ error }) => (
    <div className="error-boundary">
      <h2>Policy Loading Error</h2>
      <p>{error.message}</p>
      <button onClick={() => window.location.reload()}>
        Retry
      </button>
    </div>
  ),
  pendingComponent: () => (
    <div className="loading-state">
      <PolicyDetailSkeleton />
    </div>
  ),
});

// Policy detail component with tab navigation
const PolicyDetailComponent: React.FC = () => {
  const { policyId } = useParams({ from: '/policies/$policyId' });
  const { tab, edit, documentId } = useSearch({ from: '/policies/$policyId' });
  const navigate = useNavigate();

  // Data is pre-loaded by route loader
  const { data: policy } = useGetPolicyById(policyId);
  const { data: documents } = useGetPolicyDocuments(policyId);
  const { data: claims } = useGetPolicyClaims(policyId);

  const handleTabChange = (newTab: 'details' | 'documents' | 'claims' | 'history') => {
    navigate({
      to: '/policies/$policyId',
      params: { policyId },
      search: (prev) => ({
        ...prev,
        tab: newTab,
        // Clear document selection when changing tabs
        documentId: newTab === 'documents' ? prev.documentId : undefined,
      }),
    });
  };

  const handleDocumentSelect = (docId: string) => {
    navigate({
      search: (prev) => ({ ...prev, documentId: docId }),
    });
  };

  return (
    <div className="policy-detail">
      <PolicyHeader policy={policy} />
      
      <nav className="tab-navigation">
        <button 
          className={tab === 'details' ? 'active' : ''}
          onClick={() => handleTabChange('details')}
        >
          Policy Details
        </button>
        <button 
          className={tab === 'documents' ? 'active' : ''}
          onClick={() => handleTabChange('documents')}
        >
          Documents ({documents?.length || 0})
        </button>
        <button 
          className={tab === 'claims' ? 'active' : ''}
          onClick={() => handleTabChange('claims')}
        >
          Claims ({claims?.length || 0})
        </button>
        <button 
          className={tab === 'history' ? 'active' : ''}
          onClick={() => handleTabChange('history')}
        >
          History
        </button>
      </nav>

      <div className="tab-content">
        {tab === 'details' && (
          <PolicyDetailsTab 
            policy={policy} 
            editMode={edit}
            onEditToggle={(enabled) => 
              navigate({ search: (prev) => ({ ...prev, edit: enabled }) })
            }
          />
        )}
        
        {tab === 'documents' && (
          <PolicyDocumentsTab 
            documents={documents}
            selectedDocumentId={documentId}
            onDocumentSelect={handleDocumentSelect}
          />
        )}
        
        {tab === 'claims' && (
          <PolicyClaimsTab claims={claims} />
        )}
        
        {tab === 'history' && (
          <PolicyHistoryTab policyId={policyId} />
        )}
      </div>
    </div>
  );
};
```

## Performance Optimizations

### Bundle Size Analysis

```bash
# TanStack Router bundle impact analysis
# Maritime insurance app with 50+ routes

Base Router Bundle:
├── Core router: ~35KB (gzipped: ~12KB)
├── Route definitions: ~15KB (gzipped: ~5KB)
├── Type definitions: ~5KB (gzipped: ~1KB)
└── Total impact: ~55KB (gzipped: ~18KB)

Comparison with alternatives:
├── React Router v6: ~45KB (gzipped: ~15KB) - no type safety
├── Next.js App Router: ~80KB+ (gzipped: ~25KB+) - full framework
├── Reach Router: ~30KB (gzipped: ~10KB) - deprecated
└── TanStack Router: ~55KB (gzipped: ~18KB) - full type safety
```

### Code Splitting and Lazy Loading

```typescript
// src/routes/lazy-routes.tsx
import { createRoute, lazyRouteComponent } from '@tanstack/react-router';

// Lazy load heavy components
const policyAnalyticsRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/analytics',
  component: lazyRouteComponent(() => 
    import('../components/PolicyAnalytics').then(d => ({
      default: d.PolicyAnalyticsComponent,
    }))
  ),
});

// Preload on route hover for instant navigation
const quotesRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/quotes',
  // Preload component and data on hover/focus
  preload: 'intent',
  component: lazyRouteComponent(() => 
    import('../components/QuotesList')
  ),
});

// Critical route - always loaded
const dashboardRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/dashboard',
  preload: false, // Always bundled
  component: DashboardComponent,
});
```

### Route-Level Caching Strategies

```typescript
// src/router-config.tsx
import { createRouter } from '@tanstack/react-router';

export const router = createRouter({
  routeTree,
  defaultPreload: 'intent', // Preload on hover
  defaultPreloadStaleTime: 10000, // 10 seconds
  defaultPreloadDelay: 100, // 100ms delay
  // Maritime-specific optimizations
  defaultStaleTime: 5 * 60 * 1000, // 5 minutes for maritime data
  context: {
    queryClient,
    auth: authManager,
  },
  // Route-level error recovery
  defaultErrorComponent: ({ error, retry, reset }) => (
    <div className="route-error">
      <h2>Navigation Error</h2>
      <p>{error.message}</p>
      <div>
        <button onClick={retry}>Retry</button>
        <button onClick={reset}>Reset</button>
        <button onClick={() => window.location.href = '/dashboard'}>
          Go to Dashboard
        </button>
      </div>
    </div>
  ),
});
```

## Security and Authentication Integration

### Route-Level Authentication

```typescript
// src/auth/route-guards.tsx
import { createRoute, redirect } from '@tanstack/react-router';

// Authentication context
interface AuthContext {
  isAuthenticated: boolean;
  user: User | null;
  permissions: string[];
  hasPermission: (permission: string) => boolean;
}

// Protected route higher-order function
const createProtectedRoute = (
  routeConfig: any,
  requiredPermissions: string[] = []
) => {
  return createRoute({
    ...routeConfig,
    beforeLoad: ({ context, location }) => {
      const { isAuthenticated, hasPermission } = context.auth as AuthContext;
      
      // Check authentication
      if (!isAuthenticated) {
        throw redirect({
          to: '/login',
          search: {
            redirect: location.href,
          },
        });
      }
      
      // Check permissions
      const hasRequiredPermissions = requiredPermissions.every(
        permission => hasPermission(permission)
      );
      
      if (!hasRequiredPermissions) {
        throw redirect({
          to: '/unauthorized',
          search: {
            required: requiredPermissions.join(','),
          },
        });
      }
    },
  });
};

// Usage examples
const adminRoute = createProtectedRoute({
  getParentRoute: () => rootRoute,
  path: '/admin',
  component: AdminDashboard,
}, ['admin.access']);

const policyManagementRoute = createProtectedRoute({
  getParentRoute: () => rootRoute,
  path: '/policies/manage',
  component: PolicyManagement,
}, ['policies.write', 'policies.delete']);
```

### Role-Based Route Access

```typescript
// src/routes/role-based-routes.tsx
import { createRoute } from '@tanstack/react-router';

const brokerRoutes = createRoute({
  getParentRoute: () => rootRoute,
  path: '/broker',
  beforeLoad: ({ context }) => {
    const { user } = context.auth;
    if (user?.role !== 'broker') {
      throw redirect({ to: '/dashboard' });
    }
  },
  component: BrokerDashboard,
});

const underwriterRoutes = createRoute({
  getParentRoute: () => rootRoute,
  path: '/underwriter',
  beforeLoad: ({ context }) => {
    const { user } = context.auth;
    if (!['underwriter', 'senior_underwriter'].includes(user?.role)) {
      throw redirect({ to: '/dashboard' });
    }
  },
  component: UnderwriterDashboard,
});

const claimsRoutes = createRoute({
  getParentRoute: () => rootRoute,
  path: '/claims',
  beforeLoad: ({ context }) => {
    const { hasPermission } = context.auth;
    if (!hasPermission('claims.access')) {
      throw redirect({ to: '/unauthorized' });
    }
  },
  component: ClaimsDashboard,
});
```

## Integration with TanStack Ecosystem

### TanStack Query Integration

```typescript
// src/routes/data-integrated-routes.tsx
import { queryOptions } from '@tanstack/react-query';
import { createRoute } from '@tanstack/react-router';

const vesselsRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/vessels',
  validateSearch: (search: Record<string, unknown>) => ({
    page: Number(search.page) || 1,
    limit: Number(search.limit) || 20,
    search: (search.search as string) || '',
    flag: search.flag as string | undefined,
  }),
  // Seamless TanStack Query integration
  loader: ({ search, context: { queryClient } }) => {
    const vesselsQuery = queryOptions({
      queryKey: ['vessels', search],
      queryFn: () => getVessels(search),
      staleTime: 10 * 60 * 1000, // 10 minutes
    });
    
    // Prefetch next page for better UX
    const nextPageQuery = queryOptions({
      queryKey: ['vessels', { ...search, page: search.page + 1 }],
      queryFn: () => getVessels({ ...search, page: search.page + 1 }),
      staleTime: 10 * 60 * 1000,
    });
    
    // Load current page, prefetch next
    return Promise.all([
      queryClient.ensureQueryData(vesselsQuery),
      queryClient.prefetchQuery(nextPageQuery),
    ]);
  },
  component: VesselsListComponent,
});
```

### TanStack Form Integration

```typescript
// src/components/PolicyForm.tsx
import { useForm } from '@tanstack/react-form';
import { useNavigate, useParams } from '@tanstack/react-router';
import { zodValidator } from '@tanstack/zod-form-adapter';

const PolicyEditForm: React.FC = () => {
  const { policyId } = useParams({ from: '/policies/$policyId' });
  const navigate = useNavigate();
  
  // Get existing policy data
  const { data: existingPolicy } = useGetPolicyById(policyId);
  
  const form = useForm({
    defaultValues: existingPolicy || {
      vesselId: '',
      coverageType: 'hull',
      premium: 0,
      startDate: new Date(),
      endDate: new Date(),
    },
    validatorAdapter: zodValidator,
    validators: {
      onChange: policySchema,
    },
    onSubmit: async ({ value }) => {
      try {
        await updatePolicy({ policyId, data: value });
        
        // Navigate back to policy detail with success message
        navigate({
          to: '/policies/$policyId',
          params: { policyId },
          search: { 
            tab: 'details',
            updated: true,
          },
        });
      } catch (error) {
        console.error('Policy update failed:', error);
      }
    },
  });

  // Auto-save draft to URL search parameters
  const saveDraftToUrl = useMemo(
    () => debounce((values: any) => {
      navigate({
        search: (prev) => ({
          ...prev,
          draft: JSON.stringify(values),
        }),
        replace: true,
      });
    }, 1000),
    [navigate]
  );

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        form.handleSubmit();
      }}
    >
      {/* Form fields with real-time URL sync */}
      <form.Field
        name="premium"
        children={(field) => (
          <div>
            <label>Premium Amount</label>
            <input
              type="number"
              value={field.state.value}
              onChange={(e) => {
                const value = Number(e.target.value);
                field.handleChange(value);
                saveDraftToUrl(form.state.values);
              }}
            />
            {field.state.meta.errors && (
              <span className="error">{field.state.meta.errors[0]}</span>
            )}
          </div>
        )}
      />
      
      <div className="form-actions">
        <button type="submit" disabled={!form.state.isValid}>
          Update Policy
        </button>
        <button 
          type="button" 
          onClick={() => navigate({ 
            to: '/policies/$policyId', 
            params: { policyId } 
          })}
        >
          Cancel
        </button>
      </div>
    </form>
  );
};
```

## CI/CD and Development Integration

### Development Workflow

```json
{
  "scripts": {
    "// Router Development": "",
    "dev": "vite dev",
    "dev:routes": "tanstack-router dev",
    "build:routes": "tanstack-router build",
    
    "// Type Generation": "",
    "routes:generate": "tanstack-router generate",
    "routes:watch": "tanstack-router generate --watch",
    
    "// Testing": "",
    "test:routes": "vitest run routes",
    "test:navigation": "playwright test navigation",
    
    "// Production": "",
    "build": "tanstack-router build && vite build",
    "preview": "vite preview"
  }
}
```

### TypeScript Configuration

```json
{
  "compilerOptions": {
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true
  },
  "include": [
    "src/**/*",
    "src/routeTree.gen.ts" // Generated route tree
  ]
}
```

### Route Testing Examples

```typescript
// src/__tests__/routes.test.tsx
import { render, screen } from '@testing-library/react';
import { createMemoryHistory } from '@tanstack/react-router';
import { router } from '../router';

describe('Maritime Routes', () => {
  test('policy detail route loads correctly', async () => {
    const history = createMemoryHistory({
      initialEntries: ['/policies/policy-123?tab=details'],
    });
    
    const TestRouter = () => <router.Router history={history} />;
    
    render(<TestRouter />);
    
    // Wait for route to load
    await screen.findByText('Policy Details');
    
    // Verify correct data loading
    expect(screen.getByTestId('policy-id')).toHaveTextContent('policy-123');
    expect(screen.getByTestId('active-tab')).toHaveTextContent('details');
  });
  
  test('search parameter validation works', () => {
    const result = policiesRoute.options.validateSearch({
      status: 'active',
      page: '2',
      invalidParam: 'ignored',
    });
    
    expect(result).toEqual({
      status: 'active',
      vesselType: '',
      page: 2,
    });
  });
});
```

## Best Practices

### Route Organization

```typescript
// src/routes/index.ts - Route organization pattern
import { createRoute } from '@tanstack/react-router';

// Organize routes by domain
export const authRoutes = [
  loginRoute,
  logoutRoute,
  registerRoute,
];

export const policyRoutes = [
  policiesListRoute,
  policyDetailRoute,
  policyCreateRoute,
  policyEditRoute,
];

export const quoteRoutes = [
  quotesListRoute,
  quoteGeneratorRoute,
  quoteDetailRoute,
];

export const adminRoutes = [
  adminDashboardRoute,
  userManagementRoute,
  systemSettingsRoute,
];

// Combine all routes
export const allRoutes = [
  ...authRoutes,
  ...policyRoutes,
  ...quoteRoutes,
  ...adminRoutes,
];
```

### URL Design Patterns

```typescript
// Maritime insurance URL patterns
const urlPatterns = {
  // RESTful resource patterns
  policies: '/policies',
  policyDetail: '/policies/$policyId',
  policyEdit: '/policies/$policyId/edit',
  
  // Nested resources
  policyDocuments: '/policies/$policyId/documents',
  policyDocument: '/policies/$policyId/documents/$documentId',
  
  // Action-based patterns
  quoteGenerator: '/quotes/new',
  claimSubmission: '/claims/submit',
  
  // Search and filtering
  vesselSearch: '/vessels?search=...&flag=...&type=...',
  policySearch: '/policies?status=...&coverage=...&page=...',
  
  // User-specific resources
  myPolicies: '/my/policies',
  myQuotes: '/my/quotes',
  myProfile: '/my/profile',
};
```

### Error Handling Strategies

```typescript
// src/routes/error-handling.tsx
import { createRoute, ErrorComponent } from '@tanstack/react-router';

// Global error component
const GlobalErrorFallback: ErrorComponent = ({ error, reset, retry }) => {
  const navigate = useNavigate();
  
  // Log error for monitoring
  useEffect(() => {
    console.error('Route Error:', error);
    // Send to error tracking service
    errorTracker.captureException(error);
  }, [error]);

  return (
    <div className="error-boundary">
      <h2>Something went wrong</h2>
      <details>
        <summary>Error details</summary>
        <pre>{error.message}</pre>
      </details>
      
      <div className="error-actions">
        <button onClick={retry}>Try Again</button>
        <button onClick={reset}>Reset</button>
        <button onClick={() => navigate({ to: '/dashboard' })}>
          Go to Dashboard
        </button>
      </div>
    </div>
  );
};

// Route-specific error handling
const policyRoute = createRoute({
  // ... route config
  errorComponent: ({ error }) => {
    if (error.message.includes('not found')) {
      return (
        <div className="policy-not-found">
          <h2>Policy Not Found</h2>
          <p>The requested policy could not be found.</p>
          <Link to="/policies">Back to Policies</Link>
        </div>
      );
    }
    
    if (error.message.includes('access denied')) {
      return (
        <div className="access-denied">
          <h2>Access Denied</h2>
          <p>You don't have permission to view this policy.</p>
          <Link to="/dashboard">Back to Dashboard</Link>
        </div>
      );
    }
    
    // Fallback to global error handler
    return <GlobalErrorFallback error={error} />;
  },
});
```

## Pricing and Licensing

- **License**: MIT (Open Source)
- **Cost**: Free
- **Enterprise Support**: Community-driven with excellent documentation
- **Maintenance**: Active development by Tanner Linsley and team

## Migration Guide

### From React Router v6

```typescript
// Before: React Router v6
import { BrowserRouter, Routes, Route, useParams, useSearchParams } from 'react-router-dom';

const App = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/policies/:policyId" element={<PolicyDetail />} />
    </Routes>
  </BrowserRouter>
);

const PolicyDetail = () => {
  const { policyId } = useParams<{ policyId: string }>();
  const [searchParams] = useSearchParams();
  const tab = searchParams.get('tab') || 'details';
  
  // No type safety, manual parameter handling
  return <div>Policy {policyId}, Tab: {tab}</div>;
};

// After: TanStack Router
const policyRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/policies/$policyId',
  parseParams: (params) => ({ policyId: params.policyId! }),
  validateSearch: (search: Record<string, unknown>) => ({
    tab: (search.tab as 'details' | 'documents') || 'details',
  }),
  component: PolicyDetail,
});

const PolicyDetail = () => {
  // Full type safety
  const { policyId } = useParams({ from: '/policies/$policyId' });
  const { tab } = useSearch({ from: '/policies/$policyId' });
  
  return <div>Policy {policyId}, Tab: {tab}</div>;
};
```

### From Next.js App Router

```typescript
// Before: Next.js App Router (file-based)
// app/policies/[policyId]/page.tsx
interface Props {
  params: { policyId: string };
  searchParams: { tab?: string };
}

export default function PolicyPage({ params, searchParams }: Props) {
  const { policyId } = params;
  const tab = searchParams.tab || 'details';
  
  return <div>Policy {policyId}, Tab: {tab}</div>;
}

// After: TanStack Router (code-based with better type safety)
const policyRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/policies/$policyId',
  parseParams: (params) => ({ policyId: params.policyId! }),
  validateSearch: (search: Record<string, unknown>) => ({
    tab: (search.tab as PolicyTab) || 'details',
  }),
  component: PolicyDetail,
});
```

## Troubleshooting

### Common Issues

```bash
# Route tree generation issues
pnpm tanstack-router generate

# TypeScript errors with routes
# Check that all routes are properly typed and exported

# Search parameter validation errors
# Ensure validateSearch returns the correct type

# Data loading issues
# Verify loader functions and TanStack Query integration
```

### Performance Optimization

```typescript
// Route-level performance optimizations
const optimizedRoute = createRoute({
  // Preload strategy
  preload: 'intent', // Load on hover/focus
  
  // Cache configuration
  loaderMaxAge: 5 * 60 * 1000, // 5 minutes
  
  // Component optimization
  component: React.memo(OptimizedComponent),
  
  // Code splitting
  component: lazyRouteComponent(() => import('./HeavyComponent')),
});
```

## Conclusion

TanStack Router provides unmatched type safety and developer experience for maritime insurance applications. Its seamless integration with TanStack Query, built-in search parameter handling, and route-level data loading make it the perfect choice for complex React applications requiring robust navigation, form integration, and state management.

The combination of compile-time safety, runtime performance, and excellent developer tools creates a superior foundation for maritime insurance platforms that need to handle complex user workflows, data relationships, and business logic with complete confidence.