# React Frontend Development Context - For AI Agent Frontend Developers

## Current React Version Context

**React 19.0.0** (Latest as of 2025-07-25)
- **New Hooks**: `use()` for data fetching, `useActionState()` for form actions, `useOptimistic()` for optimistic updates
- **Server Components**: Direct async/await in components, automatic serialization
- **Actions**: Built-in form handling with server actions, automatic pending states
- **Breaking Changes**: Removed deprecated APIs, new StrictMode behavior

## Essential React 19 Patterns

### 1. Modern Data Fetching with use()
```typescript
import { use, Suspense } from 'react';

// Client Component using use() hook
function UserProfile({ userPromise }: { userPromise: Promise<User> }) {
  const user = use(userPromise); // Suspends until promise resolves
  
  return (
    <div className="user-profile">
      <img src={user.avatar} alt={`${user.name} avatar`} />
      <h2>{user.name}</h2>
      <p>{user.email}</p>
    </div>
  );
}

// Usage with Suspense
function UserPage({ userId }: { userId: string }) {
  const userPromise = fetchUser(userId); // Start fetching immediately
  
  return (
    <Suspense fallback={<UserProfileSkeleton />}>
      <UserProfile userPromise={userPromise} />
    </Suspense>
  );
}

// Error boundary integration
function UserProfileWithErrorBoundary({ userPromise }) {
  return (
    <ErrorBoundary fallback={<UserError />}>
      <Suspense fallback={<UserProfileSkeleton />}>
        <UserProfile userPromise={userPromise} />
      </Suspense>
    </ErrorBoundary>
  );
}
```

### 2. Form Handling with Actions
```typescript
import { useActionState, useOptimistic } from 'react';

// Server Action (in separate server file or 'use server' block)
async function updateUserAction(prevState: any, formData: FormData) {
  'use server';
  
  const name = formData.get('name') as string;
  const email = formData.get('email') as string;
  
  try {
    const updatedUser = await updateUser({ name, email });
    return { success: true, user: updatedUser, error: null };
  } catch (error) {
    return { success: false, user: null, error: error.message };
  }
}

// Client Component using Actions
function UserEditForm({ user }: { user: User }) {
  const [state, submitAction, isPending] = useActionState(updateUserAction, {
    success: false,
    user: null,
    error: null
  });
  
  // Optimistic updates for better UX
  const [optimisticUser, addOptimisticUser] = useOptimistic(
    state.user || user,
    (currentUser, updatedFields) => ({ ...currentUser, ...updatedFields })
  );
  
  return (
    <form action={submitAction} className="user-form">
      <div className="form-group">
        <label htmlFor="name">Name</label>
        <input
          id="name"
          name="name"
          type="text"
          defaultValue={optimisticUser.name}
          required
        />
      </div>
      
      <div className="form-group">
        <label htmlFor="email">Email</label>
        <input
          id="email"
          name="email"
          type="email"
          defaultValue={optimisticUser.email}
          required
        />
      </div>
      
      <button 
        type="submit" 
        disabled={isPending}
        className={`submit-btn ${isPending ? 'loading' : ''}`}
      >
        {isPending ? 'Updating...' : 'Update Profile'}
      </button>
      
      {state.error && (
        <div className="error-message" role="alert">
          {state.error}
        </div>
      )}
      
      {state.success && (
        <div className="success-message" role="status">
          Profile updated successfully!
        </div>
      )}
    </form>
  );
}
```

### 3. Optimistic Updates Pattern
```typescript
import { useOptimistic, startTransition } from 'react';

function TodoList({ todos }: { todos: Todo[] }) {
  const [optimisticTodos, addOptimisticTodo] = useOptimistic(
    todos,
    (currentTodos, optimisticTodo) => [
      ...currentTodos,
      { ...optimisticTodo, id: Date.now(), pending: true }
    ]
  );
  
  async function addTodo(formData: FormData) {
    const text = formData.get('text') as string;
    
    // Add optimistic todo immediately
    addOptimisticTodo({ text, completed: false });
    
    // Submit to server
    startTransition(async () => {
      await createTodo(text);
    });
  }
  
  return (
    <div className="todo-list">
      {optimisticTodos.map(todo => (
        <div 
          key={todo.id} 
          className={`todo-item ${todo.pending ? 'pending' : ''}`}
        >
          <input
            type="checkbox"
            checked={todo.completed}
            onChange={() => toggleTodo(todo.id)}
          />
          <span className={todo.completed ? 'completed' : ''}>
            {todo.text}
          </span>
          {todo.pending && <span className="spinner" />}
        </div>
      ))}
      
      <form action={addTodo} className="add-todo-form">
        <input
          name="text"
          type="text"
          placeholder="Add a new todo..."
          required
        />
        <button type="submit">Add Todo</button>
      </form>
    </div>
  );
}
```

## Component Implementation Patterns

### 1. Modern Functional Components
```typescript
import { useState, useCallback, useMemo, useId } from 'react';

interface ProductCardProps {
  product: Product;
  onAddToCart: (productId: string, quantity: number) => void;
  isInCart?: boolean;
  discount?: number;
}

function ProductCard({ 
  product, 
  onAddToCart, 
  isInCart = false, 
  discount = 0 
}: ProductCardProps) {
  const [quantity, setQuantity] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const quantityId = useId(); // Generate unique ID for accessibility
  
  // Memoize expensive calculations
  const discountedPrice = useMemo(() => {
    return discount > 0 ? product.price * (1 - discount / 100) : product.price;
  }, [product.price, discount]);
  
  // Memoize event handlers to prevent unnecessary re-renders
  const handleAddToCart = useCallback(async () => {
    setIsLoading(true);
    try {
      await onAddToCart(product.id, quantity);
    } finally {
      setIsLoading(false);
    }
  }, [product.id, quantity, onAddToCart]);
  
  const handleQuantityChange = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    setQuantity(Math.max(1, parseInt(e.target.value) || 1));
  }, []);
  
  return (
    <article className="product-card" aria-labelledby={`product-${product.id}`}>
      <div className="product-image-container">
        <img
          src={product.image}
          alt={product.name}
          loading="lazy"
          className="product-image"
        />
        {discount > 0 && (
          <span className="discount-badge" aria-label={`${discount}% discount`}>
            -{discount}%
          </span>
        )}
      </div>
      
      <div className="product-info">
        <h3 id={`product-${product.id}`} className="product-name">
          {product.name}
        </h3>
        
        <div className="product-pricing">
          {discount > 0 && (
            <span className="original-price" aria-label="Original price">
              ${product.price.toFixed(2)}
            </span>
          )}
          <span className="current-price" aria-label="Current price">
            ${discountedPrice.toFixed(2)}
          </span>
        </div>
        
        <p className="product-description">{product.description}</p>
        
        <div className="product-actions">
          <div className="quantity-selector">
            <label htmlFor={quantityId} className="quantity-label">
              Quantity:
            </label>
            <input
              id={quantityId}
              type="number"
              min="1"
              value={quantity}
              onChange={handleQuantityChange}
              className="quantity-input"
            />
          </div>
          
          <button
            onClick={handleAddToCart}
            disabled={isLoading || isInCart}
            className={`add-to-cart-btn ${isInCart ? 'in-cart' : ''}`}
            aria-describedby={isInCart ? 'already-in-cart' : undefined}
          >
            {isLoading ? (
              <>
                <span className="spinner" aria-hidden="true" />
                Adding...
              </>
            ) : isInCart ? (
              'In Cart'
            ) : (
              'Add to Cart'
            )}
          </button>
          
          {isInCart && (
            <p id="already-in-cart" className="sr-only">
              This item is already in your cart
            </p>
          )}
        </div>
      </div>
    </article>
  );
}
```

### 2. Custom Hooks for Logic Reuse
```typescript
import { useState, useEffect, useCallback, useRef } from 'react';

// Custom hook for API data fetching with error handling
function useApiData<T>(url: string, options?: RequestInit) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const abortControllerRef = useRef<AbortController>();
  
  const refetch = useCallback(async () => {
    // Cancel previous request
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    
    // Create new abort controller
    abortControllerRef.current = new AbortController();
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(url, {
        ...options,
        signal: abortControllerRef.current.signal
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const result = await response.json();
      setData(result);
    } catch (err) {
      if (err.name !== 'AbortError') {
        setError(err instanceof Error ? err.message : 'An error occurred');
      }
    } finally {
      setLoading(false);
    }
  }, [url, options]);
  
  useEffect(() => {
    refetch();
    
    // Cleanup function to abort ongoing requests
    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
    };
  }, [refetch]);
  
  return { data, loading, error, refetch };
}

// Custom hook for form handling
function useFormData<T extends Record<string, any>>(initialValues: T) {
  const [values, setValues] = useState<T>(initialValues);
  const [errors, setErrors] = useState<Partial<Record<keyof T, string>>>({});
  const [touched, setTouched] = useState<Partial<Record<keyof T, boolean>>>({});
  
  const setValue = useCallback(<K extends keyof T>(key: K, value: T[K]) => {
    setValues(prev => ({ ...prev, [key]: value }));
    // Clear error when user starts typing
    if (errors[key]) {
      setErrors(prev => ({ ...prev, [key]: undefined }));
    }
  }, [errors]);
  
  const setFieldTouched = useCallback(<K extends keyof T>(key: K) => {
    setTouched(prev => ({ ...prev, [key]: true }));
  }, []);
  
  const validate = useCallback((validationRules: Partial<Record<keyof T, (value: any) => string | undefined>>) => {
    const newErrors: Partial<Record<keyof T, string>> = {};
    
    Object.entries(validationRules).forEach(([key, validator]) => {
      const error = validator(values[key as keyof T]);
      if (error) {
        newErrors[key as keyof T] = error;
      }
    });
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  }, [values]);
  
  const reset = useCallback(() => {
    setValues(initialValues);
    setErrors({});
    setTouched({});
  }, [initialValues]);
  
  return {
    values,
    errors,
    touched,
    setValue,
    setFieldTouched,
    validate,
    reset
  };
}

// Usage example
function ContactForm() {
  const { values, errors, touched, setValue, setFieldTouched, validate, reset } = useFormData({
    name: '',
    email: '',
    message: ''
  });
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    const isValid = validate({
      name: (value) => !value ? 'Name is required' : undefined,
      email: (value) => !value ? 'Email is required' : 
             !/\S+@\S+\.\S+/.test(value) ? 'Email is invalid' : undefined,
      message: (value) => !value ? 'Message is required' : undefined
    });
    
    if (isValid) {
      try {
        await submitContactForm(values);
        reset();
        // Show success message
      } catch (error) {
        // Handle submission error
      }
    }
  };
  
  return (
    <form onSubmit={handleSubmit} className="contact-form">
      <div className="form-group">
        <label htmlFor="name">Name</label>
        <input
          id="name"
          type="text"
          value={values.name}
          onChange={(e) => setValue('name', e.target.value)}
          onBlur={() => setFieldTouched('name')}
          className={errors.name && touched.name ? 'error' : ''}
        />
        {errors.name && touched.name && (
          <span className="error-text">{errors.name}</span>
        )}
      </div>
      
      {/* Similar pattern for email and message fields */}
      
      <button type="submit">Send Message</button>
    </form>
  );
}
```

### 3. Performance Optimization Patterns
```typescript
import { memo, useMemo, useCallback, lazy, Suspense } from 'react';

// Memoized component to prevent unnecessary re-renders
const ExpensiveListItem = memo(function ExpensiveListItem({ 
  item, 
  onUpdate, 
  isSelected 
}: {
  item: ListItem;
  onUpdate: (id: string, data: any) => void;
  isSelected: boolean;
}) {
  // Memoize the update handler to prevent parent re-renders
  const handleUpdate = useCallback((data: any) => {
    onUpdate(item.id, data);
  }, [item.id, onUpdate]);
  
  // Expensive calculation that only runs when dependencies change
  const processedData = useMemo(() => {
    return expensiveDataProcessing(item.data);
  }, [item.data]);
  
  return (
    <div className={`list-item ${isSelected ? 'selected' : ''}`}>
      <h3>{item.title}</h3>
      <p>{processedData.summary}</p>
      <button onClick={() => handleUpdate({ viewed: true })}>
        Mark as Viewed
      </button>
    </div>
  );
});

// Lazy loading for code splitting
const LazyModal = lazy(() => import('./Modal'));
const LazyChart = lazy(() => import('./Chart'));

function Dashboard({ items, selectedId, onItemUpdate }) {
  const [showModal, setShowModal] = useState(false);
  const [showChart, setShowChart] = useState(false);
  
  // Memoize filtered items to prevent recalculation
  const filteredItems = useMemo(() => {
    return items.filter(item => item.active);
  }, [items]);
  
  // Memoize callback to prevent child re-renders
  const handleItemUpdate = useCallback((id: string, data: any) => {
    onItemUpdate(id, data);
  }, [onItemUpdate]);
  
  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <button onClick={() => setShowModal(true)}>
          Open Settings
        </button>
        <button onClick={() => setShowChart(true)}>
          View Analytics
        </button>
      </div>
      
      <div className="items-list">
        {filteredItems.map(item => (
          <ExpensiveListItem
            key={item.id}
            item={item}
            onUpdate={handleItemUpdate}
            isSelected={item.id === selectedId}
          />
        ))}
      </div>
      
      {/* Lazy loaded components with suspense */}
      {showModal && (
        <Suspense fallback={<div className="modal-loading">Loading...</div>}>
          <LazyModal onClose={() => setShowModal(false)} />
        </Suspense>
      )}
      
      {showChart && (
        <Suspense fallback={<div className="chart-loading">Loading chart...</div>}>
          <LazyChart data={filteredItems} />
        </Suspense>
      )}
    </div>
  );
}
```

## Event Handling Patterns

### 1. Modern Event Handling
```typescript
import { useState, useRef, useCallback } from 'react';

function InteractiveForm() {
  const [formData, setFormData] = useState({ search: '', category: 'all' });
  const [draggedFiles, setDraggedFiles] = useState<File[]>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  // Debounced input handler
  const handleSearchInput = useCallback(
    debounce((value: string) => {
      setFormData(prev => ({ ...prev, search: value }));
    }, 300),
    []
  );
  
  // File drag and drop handlers
  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);
  
  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    
    const files = Array.from(e.dataTransfer.files);
    setDraggedFiles(files);
  }, []);
  
  // Keyboard navigation handler
  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && (e.metaKey || e.ctrlKey)) {
      // Cmd/Ctrl + Enter to submit
      handleSubmit();
    } else if (e.key === 'Escape') {
      // Escape to clear
      setFormData({ search: '', category: 'all' });
    }
  }, []);
  
  // Form submission with validation
  const handleSubmit = useCallback(async () => {
    try {
      const result = await submitForm({
        ...formData,
        files: draggedFiles
      });
      
      // Handle success
      console.log('Form submitted:', result);
    } catch (error) {
      console.error('Submission failed:', error);
    }
  }, [formData, draggedFiles]);
  
  return (
    <div className="interactive-form" onKeyDown={handleKeyDown}>
      <div className="search-section">
        <input
          type="text"
          placeholder="Search..."
          onChange={(e) => handleSearchInput(e.target.value)}
          className="search-input"
        />
        
        <select
          value={formData.category}
          onChange={(e) => setFormData(prev => ({ 
            ...prev, 
            category: e.target.value 
          }))}
          className="category-select"
        >
          <option value="all">All Categories</option>
          <option value="documents">Documents</option>
          <option value="images">Images</option>
        </select>
      </div>
      
      <div
        className="file-drop-zone"
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
      >
        {draggedFiles.length > 0 ? (
          <div className="dropped-files">
            {draggedFiles.map((file, index) => (
              <div key={index} className="file-item">
                {file.name} ({file.size} bytes)
              </div>
            ))}
          </div>
        ) : (
          <p>Drag files here or click to select</p>
        )}
        
        <input
          ref={fileInputRef}
          type="file"
          multiple
          style={{ display: 'none' }}
          onChange={(e) => {
            const files = Array.from(e.target.files || []);
            setDraggedFiles(files);
          }}
        />
      </div>
      
      <button onClick={handleSubmit} className="submit-button">
        Submit Form
      </button>
    </div>
  );
}

// Utility function for debouncing
function debounce<T extends (...args: any[]) => any>(
  func: T,
  delay: number
): (...args: Parameters<T>) => void {
  let timeoutId: NodeJS.Timeout;
  
  return (...args: Parameters<T>) => {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), delay);
  };
}
```

## State Management Patterns

### 1. Context API Usage
```typescript
import { createContext, useContext, useReducer, ReactNode } from 'react';

// Theme context example
interface ThemeState {
  theme: 'light' | 'dark';
  fontSize: 'small' | 'medium' | 'large';
}

interface ThemeContextType {
  state: ThemeState;
  toggleTheme: () => void;
  setFontSize: (size: ThemeState['fontSize']) => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

// Theme reducer
type ThemeAction = 
  | { type: 'TOGGLE_THEME' }
  | { type: 'SET_FONT_SIZE'; payload: ThemeState['fontSize'] };

function themeReducer(state: ThemeState, action: ThemeAction): ThemeState {
  switch (action.type) {
    case 'TOGGLE_THEME':
      return { ...state, theme: state.theme === 'light' ? 'dark' : 'light' };
    case 'SET_FONT_SIZE':
      return { ...state, fontSize: action.payload };
    default:
      return state;
  }
}

// Theme provider component
function ThemeProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(themeReducer, {
    theme: 'light',
    fontSize: 'medium'
  });
  
  const toggleTheme = useCallback(() => {
    dispatch({ type: 'TOGGLE_THEME' });
  }, []);
  
  const setFontSize = useCallback((size: ThemeState['fontSize']) => {
    dispatch({ type: 'SET_FONT_SIZE', payload: size });
  }, []);
  
  return (
    <ThemeContext.Provider value={{ state, toggleTheme, setFontSize }}>
      <div 
        className={`app-theme theme-${state.theme} font-${state.fontSize}`}
        data-theme={state.theme}
      >
        {children}
      </div>
    </ThemeContext.Provider>
  );
}

// Custom hook for using theme
function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}

// Usage in component
function ThemedButton({ children, ...props }: React.ButtonHTMLAttributes<HTMLButtonElement>) {
  const { state, toggleTheme } = useTheme();
  
  return (
    <button
      {...props}
      className={`themed-button ${props.className || ''}`}
      onClick={toggleTheme}
      style={{
        backgroundColor: state.theme === 'dark' ? '#333' : '#fff',
        color: state.theme === 'dark' ? '#fff' : '#333',
        fontSize: state.fontSize === 'large' ? '18px' : state.fontSize === 'small' ? '14px' : '16px'
      }}
    >
      {children}
    </button>
  );
}
```

## Error Handling for Frontend Developers

### 1. Practical Error Handling
```typescript
import { useState, useCallback } from 'react';

// Error boundary hook
function useErrorHandler() {
  const [error, setError] = useState<Error | null>(null);
  
  const resetError = useCallback(() => {
    setError(null);
  }, []);
  
  const handleError = useCallback((error: Error) => {
    console.error('Application Error:', error);
    setError(error);
    
    // Report to error tracking service
    if (typeof window !== 'undefined' && window.gtag) {
      window.gtag('event', 'exception', {
        description: error.message,
        fatal: false
      });
    }
  }, []);
  
  return { error, resetError, handleError };
}

// Component with error handling
function DataFetchingComponent({ userId }: { userId: string }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const { error, resetError, handleError } = useErrorHandler();
  
  const fetchData = useCallback(async () => {
    setLoading(true);
    resetError();
    
    try {
      const response = await fetch(`/api/users/${userId}`);
      
      if (!response.ok) {
        throw new Error(`Failed to fetch user data: ${response.status}`);
      }
      
      const userData = await response.json();
      setData(userData);
    } catch (err) {
      handleError(err instanceof Error ? err : new Error('Unknown error'));
    } finally {
      setLoading(false);
    }
  }, [userId, resetError, handleError]);
  
  useEffect(() => {
    fetchData();
  }, [fetchData]);
  
  if (error) {
    return (
      <div className="error-container" role="alert">
        <h3>Something went wrong</h3>
        <p>{error.message}</p>
        <button onClick={resetError}>Try Again</button>
      </div>
    );
  }
  
  if (loading) {
    return <div className="loading-spinner" aria-label="Loading user data" />;
  }
  
  return data ? <UserDisplay user={data} /> : null;
}
```

## Testing Implementation Patterns

### 1. Component Testing with React Testing Library
```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { vi } from 'vitest';

// Mock API calls
const mockSubmitForm = vi.fn();

describe('ContactForm', () => {
  beforeEach(() => {
    mockSubmitForm.mockClear();
  });
  
  test('renders form fields with proper labels and ARIA attributes', () => {
    render(<ContactForm onSubmit={mockSubmitForm} />);
    
    expect(screen.getByLabelText(/name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/message/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /send/i })).toBeInTheDocument();
  });
  
  test('validates required fields', async () => {
    const user = userEvent.setup();
    render(<ContactForm onSubmit={mockSubmitForm} />);
    
    // Try to submit empty form
    await user.click(screen.getByRole('button', { name: /send/i }));
    
    expect(screen.getByText(/name is required/i)).toBeInTheDocument();
    expect(screen.getByText(/email is required/i)).toBeInTheDocument();
    expect(mockSubmitForm).not.toHaveBeenCalled();
  });
  
  test('submits form with valid data', async () => {
    const user = userEvent.setup();
    mockSubmitForm.mockResolvedValue({ success: true });
    
    render(<ContactForm onSubmit={mockSubmitForm} />);
    
    // Fill out form
    await user.type(screen.getByLabelText(/name/i), 'John Doe');
    await user.type(screen.getByLabelText(/email/i), 'john@example.com');
    await user.type(screen.getByLabelText(/message/i), 'Test message');
    
    // Submit form
    await user.click(screen.getByRole('button', { name: /send/i }));
    
    await waitFor(() => {
      expect(mockSubmitForm).toHaveBeenCalledWith({
        name: 'John Doe',
        email: 'john@example.com',
        message: 'Test message'
      });
    });
  });
  
  test('handles submission errors gracefully', async () => {
    const user = userEvent.setup();
    mockSubmitForm.mockRejectedValue(new Error('Network error'));
    
    render(<ContactForm onSubmit={mockSubmitForm} />);
    
    // Fill and submit form
    await user.type(screen.getByLabelText(/name/i), 'John Doe');
    await user.type(screen.getByLabelText(/email/i), 'john@example.com');
    await user.type(screen.getByLabelText(/message/i), 'Test message');
    await user.click(screen.getByRole('button', { name: /send/i }));
    
    await waitFor(() => {
      expect(screen.getByText(/network error/i)).toBeInTheDocument();
    });
  });
});
```

## Best Practices for Frontend Developers

### 1. Component Development Guidelines
- Use TypeScript for type safety and better developer experience
- Implement accessibility attributes (ARIA labels, roles, semantic HTML)
- Optimize for performance with memoization and lazy loading
- Handle loading and error states explicitly
- Write comprehensive tests for user interactions

### 2. Code Organization
- Group related functionality in custom hooks
- Keep components focused on single responsibilities
- Use consistent naming conventions
- Implement proper error boundaries
- Document complex logic with comments

### 3. User Experience Considerations
- Provide immediate feedback for user actions
- Implement loading states for async operations
- Use optimistic updates for better perceived performance
- Ensure keyboard accessibility
- Test across different devices and browsers

## Context Usage Guidelines

**For AI Agents in Frontend Developer Role:**
1. Focus on practical component implementation and user interactions
2. Include specific code examples and patterns
3. Consider accessibility and performance in all implementations
4. Think about user experience and edge cases
5. Use current React 19 patterns and APIs

**Don't Include:**
- High-level architectural decisions (use architect context)
- Detailed performance optimization strategies (use performance context)
- Comprehensive testing strategies (use testing context)
- Advanced build and deployment configuration

This context should guide day-to-day React development tasks and component implementation.