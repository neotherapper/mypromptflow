# TypeScript Frontend Development Context - For AI Agent Frontend Developers

## Current TypeScript Version Context

**TypeScript 5.7.2** (Latest as of 2025-07-25)
- **New Features**: `satisfies` operator, const assertions, template literal types, conditional types
- **Frontend Improvements**: Better React integration, improved inference, enhanced JSX support
- **Breaking Changes**: Stricter null assessment, improved type narrowing, better error messages

## Essential TypeScript Patterns for Frontend

### 1. Component Type Definitions

```typescript
// React component props with TypeScript
import { ReactNode, HTMLAttributes, forwardRef, ForwardedRef } from 'react';

// Basic component props interface
interface ButtonProps extends HTMLAttributes<HTMLButtonElement> {
  variant: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  leftIcon?: ReactNode;
  rightIcon?: ReactNode;
  children: ReactNode;
}

// Implementation with forwardRef for ref forwarding
const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  (
    { 
      variant, 
      size = 'md', 
      isLoading = false, 
      leftIcon, 
      rightIcon, 
      children, 
      className = '', 
      disabled,
      ...props 
    },
    ref: ForwardedRef<HTMLButtonElement>
  ) => {
    const baseClasses = 'inline-flex items-center justify-center rounded-md font-medium transition-colors';
    const variantClasses = {
      primary: 'bg-blue-600 text-white hover:bg-blue-700 disabled:bg-blue-400',
      secondary: 'bg-gray-600 text-white hover:bg-gray-700 disabled:bg-gray-400',
      outline: 'border border-gray-300 text-gray-700 hover:bg-gray-50 disabled:text-gray-400',
      ghost: 'text-gray-700 hover:bg-gray-100 disabled:text-gray-400'
    };
    const sizeClasses = {
      sm: 'px-3 py-1.5 text-sm',
      md: 'px-4 py-2 text-base',
      lg: 'px-6 py-3 text-lg'
    };

    return (
      <button
        ref={ref}
        className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${className}`}
        disabled={disabled || isLoading}
        {...props}
      >
        {isLoading && (
          <svg 
            className="animate-spin -ml-1 mr-2 h-4 w-4" 
            fill="none" 
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
        )}
        {leftIcon && !isLoading && <span className="mr-2">{leftIcon}</span>}
        {children}
        {rightIcon && <span className="ml-2">{rightIcon}</span>}
      </button>
    );
  }
);

Button.displayName = 'Button';

// Usage example with type safety
function App() {
  return (
    <div>
      <Button variant="primary" size="lg" onClick={() => console.log('clicked')}>
        Primary Button
      </Button>
      
      <Button
        variant="outline"
        isLoading={true}
        leftIcon={<span>📧</span>}
        disabled // TypeScript ensures this works with HTMLButtonElement
      >
        Send Email
      </Button>
    </div>
  );
}
```

### 2. Form Handling with TypeScript

```typescript
import { useState, useCallback, FormEvent, ChangeEvent } from 'react';

// Form data types
interface ContactFormData {
  name: string;
  email: string;
  message: string;
  newsletter: boolean;
  category: 'support' | 'sales' | 'feedback';
}

// Validation error types
type ValidationErrors<T> = {
  [K in keyof T]?: string;
};

// Form validation functions
const validateEmail = (email: string): string | undefined => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!email) return 'Email is required';
  if (!emailRegex.test(email)) return 'Please enter a valid email address';
  return undefined;
};

const validateRequired = (value: string, fieldName: string): string | undefined => {
  if (!value.trim()) return `${fieldName} is required`;
  return undefined;
};

// Custom hook for form handling
function useForm<T extends Record<string, any>>(
  initialValues: T,
  validationRules: Partial<Record<keyof T, (value: any) => string | undefined>>
) {
  const [values, setValues] = useState<T>(initialValues);
  const [errors, setErrors] = useState<ValidationErrors<T>>({});
  const [touched, setTouched] = useState<Partial<Record<keyof T, boolean>>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = useCallback(<K extends keyof T>(
    field: K,
    value: T[K]
  ) => {
    setValues(prev => ({ ...prev, [field]: value }));
    
    // Clear error when user starts typing
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: undefined }));
    }
  }, [errors]);

  const handleBlur = useCallback(<K extends keyof T>(field: K) => {
    setTouched(prev => ({ ...prev, [field]: true }));
    
    // Validate field on blur if there's a validation rule
    const validator = validationRules[field];
    if (validator) {
      const error = validator(values[field]);
      setErrors(prev => ({ ...prev, [field]: error }));
    }
  }, [values, validationRules]);

  const validateForm = useCallback((): boolean => {
    const newErrors: ValidationErrors<T> = {};
    let hasErrors = false;

    // Run all validation rules
    Object.entries(validationRules).forEach(([field, validator]) => {
      if (validator) {
        const error = validator(values[field as keyof T]);
        if (error) {
          newErrors[field as keyof T] = error;
          hasErrors = true;
        }
      }
    });

    setErrors(newErrors);
    return !hasErrors;
  }, [values, validationRules]);

  const handleSubmit = useCallback(async (
    onSubmit: (values: T) => Promise<void> | void
  ) => {
    setIsSubmitting(true);
    
    // Mark all fields as touched
    const allFieldsTouched = Object.keys(values).reduce(
      (acc, key) => ({ ...acc, [key]: true }),
      {} as Record<keyof T, boolean>
    );
    setTouched(allFieldsTouched);

    // Validate form
    if (!validateForm()) {
      setIsSubmitting(false);
      return;
    }

    try {
      await onSubmit(values);
    } finally {
      setIsSubmitting(false);
    }
  }, [values, validateForm]);

  const reset = useCallback(() => {
    setValues(initialValues);
    setErrors({});
    setTouched({});
    setIsSubmitting(false);
  }, [initialValues]);

  return {
    values,
    errors,
    touched,
    isSubmitting,
    handleChange,
    handleBlur,
    handleSubmit,
    reset,
    validate
  };
}

// Contact form component
function ContactForm() {
  const {
    values,
    errors,
    touched,
    isSubmitting,
    handleChange,
    handleBlur,
    handleSubmit,
    reset
  } = useForm<ContactFormData>(
    {
      name: '',
      email: '',
      message: '',
      newsletter: false,
      category: 'support'
    },
    {
      name: (value) => validateRequired(value, 'Name'),
      email: validateEmail,
      message: (value) => validateRequired(value, 'Message')
    }
  );

  const onSubmit = async (formData: ContactFormData) => {
    try {
      const response = await fetch('/api/contact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error('Failed to submit form');
      }

      alert('Message sent successfully!');
      reset();
    } catch (error) {
      alert('Failed to send message. Please try again.');
      console.error('Form submission error:', error);
    }
  };

  const handleFormSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    handleSubmit(onSubmit);
  };

  return (
    <form onSubmit={handleFormSubmit} className="max-w-md mx-auto space-y-4">
      <div>
        <label htmlFor="name" className="block text-sm font-medium text-gray-700">
          Name
        </label>
        <input
          id="name"
          type="text"
          value={values.name}
          onChange={(e: ChangeEvent<HTMLInputElement>) => 
            handleChange('name', e.target.value)
          }
          onBlur={() => handleBlur('name')}
          className={`mt-1 block w-full rounded-md border px-3 py-2 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.name && touched.name 
              ? 'border-red-500 focus:border-red-500' 
              : 'border-gray-300 focus:border-blue-500'
          }`}
        />
        {errors.name && touched.name && (
          <p className="mt-1 text-sm text-red-600" role="alert">
            {errors.name}
          </p>
        )}
      </div>

      <div>
        <label htmlFor="email" className="block text-sm font-medium text-gray-700">
          Email
        </label>
        <input
          id="email"
          type="email"
          value={values.email}
          onChange={(e: ChangeEvent<HTMLInputElement>) => 
            handleChange('email', e.target.value)
          }
          onBlur={() => handleBlur('email')}
          className={`mt-1 block w-full rounded-md border px-3 py-2 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.email && touched.email 
              ? 'border-red-500 focus:border-red-500' 
              : 'border-gray-300 focus:border-blue-500'
          }`}
        />
        {errors.email && touched.email && (
          <p className="mt-1 text-sm text-red-600" role="alert">
            {errors.email}
          </p>
        )}
      </div>

      <div>
        <label htmlFor="category" className="block text-sm font-medium text-gray-700">
          Category
        </label>
        <select
          id="category"
          value={values.category}
          onChange={(e: ChangeEvent<HTMLSelectElement>) => 
            handleChange('category', e.target.value as ContactFormData['category'])
          }
          className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="support">Support</option>
          <option value="sales">Sales</option>
          <option value="feedback">Feedback</option>
        </select>
      </div>

      <div>
        <label htmlFor="message" className="block text-sm font-medium text-gray-700">
          Message
        </label>
        <textarea
          id="message"
          rows={4}
          value={values.message}
          onChange={(e: ChangeEvent<HTMLTextAreaElement>) => 
            handleChange('message', e.target.value)
          }
          onBlur={() => handleBlur('message')}
          className={`mt-1 block w-full rounded-md border px-3 py-2 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 ${
            errors.message && touched.message 
              ? 'border-red-500 focus:border-red-500' 
              : 'border-gray-300 focus:border-blue-500'
          }`}
        />
        {errors.message && touched.message && (
          <p className="mt-1 text-sm text-red-600" role="alert">
            {errors.message}
          </p>
        )}
      </div>

      <div className="flex items-center">
        <input
          id="newsletter"
          type="checkbox"
          checked={values.newsletter}
          onChange={(e: ChangeEvent<HTMLInputElement>) => 
            handleChange('newsletter', e.target.checked)
          }
          className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-2 focus:ring-blue-500"
        />
        <label htmlFor="newsletter" className="ml-2 block text-sm text-gray-700">
          Subscribe to newsletter
        </label>
      </div>

      <Button
        type="submit"
        variant="primary"
        isLoading={isSubmitting}
        className="w-full"
        disabled={isSubmitting}
      >
        {isSubmitting ? 'Sending...' : 'Send Message'}
      </Button>
    </form>
  );
}
```

### 3. API Integration with TypeScript

```typescript
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

// User-related types
interface User {
  id: string;
  name: string;
  email: string;
  avatar?: string;
  createdAt: string;
  updatedAt: string;
}

interface CreateUserRequest {
  name: string;
  email: string;
}

interface UpdateUserRequest {
  name?: string;
  email?: string;
  avatar?: string;
}

// Generic API client with TypeScript
class ApiClient {
  private baseURL: string;
  
  constructor(baseURL: string) {
    this.baseURL = baseURL;
  }
  
  private async request<T>(
    endpoint: string, 
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const url = `${this.baseURL}${endpoint}`;
    
    const defaultHeaders: HeadersInit = {
      'Content-Type': 'application/json',
    };
    
    // Add auth token if available
    const token = localStorage.getItem('authToken');
    if (token) {
      defaultHeaders.Authorization = `Bearer ${token}`;
    }
    
    const config: RequestInit = {
      ...options,
      headers: {
        ...defaultHeaders,
        ...options.headers,
      },
    };
    
    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        const errorData: ApiError = await response.json();
        throw new Error(`API Error: ${errorData.message || response.statusText}`);
      }
      
      return await response.json();
    } catch (error) {
      if (error instanceof Error) {
        throw error;
      }
      throw new Error('Network error occurred');
    }
  }
  
  // Generic CRUD methods
  public async get<T>(endpoint: string): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { method: 'GET' });
  }
  
  public async post<TRequest, TResponse>(
    endpoint: string, 
    data: TRequest
  ): Promise<ApiResponse<TResponse>> {
    return this.request<TResponse>(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
  
  public async put<TRequest, TResponse>(
    endpoint: string, 
    data: TRequest
  ): Promise<ApiResponse<TResponse>> {
    return this.request<TResponse>(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }
  
  public async delete<T>(endpoint: string): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { method: 'DELETE' });
  }
}

// User service with typed methods
class UserService {
  constructor(private apiClient: ApiClient) {}
  
  public async getUsers(): Promise<User[]> {
    const response = await this.apiClient.get<User[]>('/users');
    return response.data;
  }
  
  public async getUserById(id: string): Promise<User> {
    const response = await this.apiClient.get<User>(`/users/${id}`);
    return response.data;
  }
  
  public async createUser(userData: CreateUserRequest): Promise<User> {
    const response = await this.apiClient.post<CreateUserRequest, User>(
      '/users', 
      userData
    );
    return response.data;
  }
  
  public async updateUser(id: string, userData: UpdateUserRequest): Promise<User> {
    const response = await this.apiClient.put<UpdateUserRequest, User>(
      `/users/${id}`, 
      userData
    );
    return response.data;
  }
  
  public async deleteUser(id: string): Promise<void> {
    await this.apiClient.delete(`/users/${id}`);
  }
}

// React hook for API data fetching
function useApiData<T>(
  fetcher: () => Promise<T>,
  dependencies: any[] = []
) {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const result = await fetcher();
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  }, dependencies); // eslint-disable-line react-hooks/exhaustive-deps
  
  useEffect(() => {
    fetchData();
  }, [fetchData]);
  
  return { data, loading, error, refetch: fetchData };
}

// Usage in a component
function UserList() {
  const apiClient = new ApiClient('/api');
  const userService = new UserService(apiClient);
  
  const { data: users, loading, error, refetch } = useApiData(
    () => userService.getUsers()
  );
  
  const handleDeleteUser = async (userId: string) => {
    try {
      await userService.deleteUser(userId);
      refetch(); // Refresh the list
    } catch (error) {
      alert('Failed to delete user');
      console.error('Delete error:', error);
    }
  };
  
  if (loading) {
    return (
      <div className="flex justify-center items-center h-32">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="text-red-600 text-center p-4">
        <p>Error: {error}</p>
        <Button variant="outline" onClick={refetch} className="mt-2">
          Try Again
        </Button>
      </div>
    );
  }
  
  return (
    <div className="grid gap-4">
      {users?.map(user => (
        <div key={user.id} className="border rounded-lg p-4 flex justify-between items-center">
          <div>
            <h3 className="font-medium">{user.name}</h3>
            <p className="text-gray-600">{user.email}</p>
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={() => handleDeleteUser(user.id)}
          >
            Delete
          </Button>
        </div>
      ))}
    </div>
  );
}
```

### 4. State Management with TypeScript

```typescript
// Redux Toolkit with TypeScript
import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';

// State types
interface UserState {
  users: User[];
  currentUser: User | null;
  loading: boolean;
  error: string | null;
}

// Initial state
const initialState: UserState = {
  users: [],
  currentUser: null,
  loading: false,
  error: null,
};

// Async thunks with TypeScript
export const fetchUsers = createAsyncThunk<
  User[], // Return type
  void, // Argument type
  { rejectValue: string } // ThunkAPI type
>('users/fetchUsers', async (_, { rejectWithValue }) => {
  try {
    const apiClient = new ApiClient('/api');
    const userService = new UserService(apiClient);
    return await userService.getUsers();
  } catch (error) {
    return rejectWithValue(
      error instanceof Error ? error.message : 'Failed to fetch users'
    );
  }
});

export const createUser = createAsyncThunk<
  User,
  CreateUserRequest,
  { rejectValue: string }
>('users/createUser', async (userData, { rejectWithValue }) => {
  try {
    const apiClient = new ApiClient('/api');
    const userService = new UserService(apiClient);
    return await userService.createUser(userData);
  } catch (error) {
    return rejectWithValue(
      error instanceof Error ? error.message : 'Failed to create user'
    );
  }
});

// Slice with TypeScript
const userSlice = createSlice({
  name: 'users',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    setCurrentUser: (state, action: PayloadAction<User | null>) => {
      state.currentUser = action.payload;
    },
    updateUserLocally: (state, action: PayloadAction<{ id: string; updates: Partial<User> }>) => {
      const { id, updates } = action.payload;
      const userIndex = state.users.findIndex(user => user.id === id);
      if (userIndex !== -1) {
        state.users[userIndex] = { ...state.users[userIndex], ...updates };
      }
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch users
      .addCase(fetchUsers.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchUsers.fulfilled, (state, action: PayloadAction<User[]>) => {
        state.loading = false;
        state.users = action.payload;
      })
      .addCase(fetchUsers.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload || 'Failed to fetch users';
      })
      // Create user
      .addCase(createUser.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(createUser.fulfilled, (state, action: PayloadAction<User>) => {
        state.loading = false;
        state.users.push(action.payload);
      })
      .addCase(createUser.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload || 'Failed to create user';
      });
  },
});

export const { clearError, setCurrentUser, updateUserLocally } = userSlice.actions;
export default userSlice.reducer;

// Store configuration with TypeScript
import { configureStore } from '@reduxjs/toolkit';
import { useDispatch, useSelector, TypedUseSelectorHook } from 'react-redux';

export const store = configureStore({
  reducer: {
    users: userSlice.reducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

// Typed hooks
export const useAppDispatch = () => useDispatch<AppDispatch>();
export const useAppSelector: TypedUseSelectorHook<RootState> = useSelector;

// Component using typed Redux
function UserManagement() {
  const dispatch = useAppDispatch();
  const { users, loading, error } = useAppSelector((state) => state.users);
  
  useEffect(() => {
    dispatch(fetchUsers());
  }, [dispatch]);
  
  const handleCreateUser = async (userData: CreateUserRequest) => {
    const result = await dispatch(createUser(userData));
    if (createUser.fulfilled.match(result)) {
      alert('User created successfully!');
    } else {
      alert(`Failed to create user: ${result.payload}`);
    }
  };
  
  const handleClearError = () => {
    dispatch(clearError());
  };
  
  return (
    <div>
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          <p>{error}</p>
          <Button variant="outline" size="sm" onClick={handleClearError}>
            Dismiss
          </Button>
        </div>
      )}
      
      {loading && <p>Loading users...</p>}
      
      <div className="grid gap-4">
        {users.map(user => (
          <div key={user.id} className="border rounded p-4">
            <h3 className="font-medium">{user.name}</h3>
            <p className="text-gray-600">{user.email}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
```

### 5. Custom Hooks with TypeScript

```typescript
// Local storage hook with TypeScript
function useLocalStorage<T>(
  key: string,
  initialValue: T
): [T, (value: T | ((val: T) => T)) => void] {
  // Get value from localStorage or use initial value
  const [storedValue, setStoredValue] = useState<T>(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(`Error reading localStorage key "${key}":`, error);
      return initialValue;
    }
  });

  // Return a wrapped version of useState's setter function that persists the new value to localStorage
  const setValue = useCallback((value: T | ((val: T) => T)) => {
    try {
      // Allow value to be a function so we have the same API as useState
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error(`Error setting localStorage key "${key}":`, error);
    }
  }, [key, storedValue]);

  return [storedValue, setValue];
}

// Debounced value hook
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);

  return debouncedValue;
}

// Online status hook
function useOnlineStatus(): boolean {
  const [isOnline, setIsOnline] = useState<boolean>(
    typeof navigator !== 'undefined' ? navigator.onLine : true
  );

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  return isOnline;
}

// Previous value hook
function usePrevious<T>(value: T): T | undefined {
  const ref = useRef<T>();
  useEffect(() => {
    ref.current = value;
  });
  return ref.current;
}

// Window size hook
interface WindowSize {
  width: number | undefined;
  height: number | undefined;
}

function useWindowSize(): WindowSize {
  const [windowSize, setWindowSize] = useState<WindowSize>({
    width: undefined,
    height: undefined,
  });

  useEffect(() => {
    function handleResize() {
      setWindowSize({
        width: window.innerWidth,
        height: window.innerHeight,
      });
    }

    window.addEventListener('resize', handleResize);
    handleResize(); // Call handler right away so state gets updated with initial window size

    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return windowSize;
}

// Usage examples in components
function ExampleComponent() {
  // Local storage for user preferences
  const [theme, setTheme] = useLocalStorage<'light' | 'dark'>('theme', 'light');
  
  // Search functionality with debounce
  const [searchTerm, setSearchTerm] = useState('');
  const debouncedSearchTerm = useDebounce(searchTerm, 300);
  
  // Online status
  const isOnline = useOnlineStatus();
  
  // Previous value for comparison
  const previousSearchTerm = usePrevious(debouncedSearchTerm);
  
  // Window size for responsive behavior
  const { width } = useWindowSize();
  const isMobile = width !== undefined && width < 768;
  
  // Effect that runs when debounced search term changes
  useEffect(() => {
    if (debouncedSearchTerm !== previousSearchTerm && debouncedSearchTerm) {
      // Perform search
      console.log('Searching for:', debouncedSearchTerm);
    }
  }, [debouncedSearchTerm, previousSearchTerm]);
  
  return (
    <div className={`app ${theme}`}>
      {!isOnline && (
        <div className="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded mb-4">
          You are currently offline
        </div>
      )}
      
      <div className="flex justify-between items-center mb-4">
        <input
          type="text"
          placeholder="Search..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="px-3 py-2 border rounded-md"
        />
        
        <Button
          variant={theme === 'light' ? 'primary' : 'secondary'}
          onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
        >
          Toggle Theme
        </Button>
      </div>
      
      <p className="text-sm text-gray-600">
        Screen size: {isMobile ? 'Mobile' : 'Desktop'} ({width}px)
      </p>
      
      {debouncedSearchTerm && (
        <p className="text-sm text-gray-600">
          Searching for: "{debouncedSearchTerm}"
        </p>
      )}
    </div>
  );
}
```

### 6. Testing Components with TypeScript

```typescript
// Test utilities with TypeScript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { vi, describe, it, expect, beforeEach } from 'vitest';
import type { ReactElement } from 'react';

// Mock types
interface MockApiClient {
  get: ReturnType<typeof vi.fn>;
  post: ReturnType<typeof vi.fn>;
  put: ReturnType<typeof vi.fn>;
  delete: ReturnType<typeof vi.fn>;
}

// Test helper function
function renderWithProviders(ui: ReactElement, options = {}) {
  // Add providers like Redux, Router, Theme, etc.
  return render(ui, options);
}

// Component tests
describe('ContactForm', () => {
  let mockOnSubmit: ReturnType<typeof vi.fn>;
  
  beforeEach(() => {
    mockOnSubmit = vi.fn();
  });
  
  it('renders all form fields with TypeScript type validation', () => {
    renderWithProviders(<ContactForm />);
    
    expect(screen.getByLabelText(/name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/message/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/category/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/newsletter/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /send message/i })).toBeInTheDocument();
  });
  
  it('validates required fields', async () => {
    const user = userEvent.setup();
    renderWithProviders(<ContactForm />);
    
    const submitButton = screen.getByRole('button', { name: /send message/i });
    await user.click(submitButton);
    
    expect(screen.getByText(/name is required/i)).toBeInTheDocument();
    expect(screen.getByText(/email is required/i)).toBeInTheDocument();
    expect(screen.getByText(/message is required/i)).toBeInTheDocument();
  });
  
  it('validates email format', async () => {
    const user = userEvent.setup();
    renderWithProviders(<ContactForm />);
    
    const emailInput = screen.getByLabelText(/email/i);
    await user.type(emailInput, 'invalid-email');
    await user.tab(); // Trigger blur event
    
    expect(screen.getByText(/please enter a valid email address/i)).toBeInTheDocument();
  });
  
  it('submits form with valid data', async () => {
    const user = userEvent.setup();
    global.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ success: true }),
    });
    
    renderWithProviders(<ContactForm />);
    
    // Fill out form
    await user.type(screen.getByLabelText(/name/i), 'John Doe');
    await user.type(screen.getByLabelText(/email/i), 'john@example.com');
    await user.type(screen.getByLabelText(/message/i), 'Hello, this is a test message.');
    await user.selectOptions(screen.getByLabelText(/category/i), 'feedback');
    await user.click(screen.getByLabelText(/newsletter/i));
    
    // Submit form
    await user.click(screen.getByRole('button', { name: /send message/i }));
    
    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith('/api/contact', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: 'John Doe',
          email: 'john@example.com',
          message: 'Hello, this is a test message.',
          category: 'feedback',
          newsletter: true,
        }),
      });
    });
  });
  
  it('handles form submission errors', async () => {
    const user = userEvent.setup();
    global.fetch = vi.fn().mockRejectedValue(new Error('Network error'));
    
    // Mock alert
    global.alert = vi.fn();
    
    renderWithProviders(<ContactForm />);
    
    // Fill out form with valid data
    await user.type(screen.getByLabelText(/name/i), 'John Doe');
    await user.type(screen.getByLabelText(/email/i), 'john@example.com');
    await user.type(screen.getByLabelText(/message/i), 'Test message');
    
    // Submit form
    await user.click(screen.getByRole('button', { name: /send message/i }));
    
    await waitFor(() => {
      expect(global.alert).toHaveBeenCalledWith('Failed to send message. Please try again.');
    });
  });
});

// Hook testing
describe('useForm', () => {
  interface TestFormData {
    name: string;
    email: string;
  }
  
  const mockValidation = {
    name: (value: string) => value ? undefined : 'Name is required',
    email: (value: string) => value.includes('@') ? undefined : 'Invalid email',
  };
  
  it('initializes with default values', () => {
    const initialValues: TestFormData = { name: '', email: '' };
    const { result } = renderHook(() => 
      useForm(initialValues, mockValidation)
    );
    
    expect(result.current.values).toEqual(initialValues);
    expect(result.current.errors).toEqual({});
    expect(result.current.touched).toEqual({});
    expect(result.current.isSubmitting).toBe(false);
  });
  
  it('updates values when handleChange is called', () => {
    const initialValues: TestFormData = { name: '', email: '' };
    const { result } = renderHook(() => 
      useForm(initialValues, mockValidation)
    );
    
    act(() => {
      result.current.handleChange('name', 'John Doe');
    });
    
    expect(result.current.values.name).toBe('John Doe');
  });
  
  it('validates fields on blur', () => {
    const initialValues: TestFormData = { name: '', email: '' };
    const { result } = renderHook(() => 
      useForm(initialValues, mockValidation)
    );
    
    act(() => {
      result.current.handleBlur('name');
    });
    
    expect(result.current.errors.name).toBe('Name is required');
    expect(result.current.touched.name).toBe(true);
  });
  
  it('validates entire form on submit', async () => {
    const initialValues: TestFormData = { name: '', email: '' };
    const mockSubmit = vi.fn();
    
    const { result } = renderHook(() => 
      useForm(initialValues, mockValidation)
    );
    
    await act(async () => {
      await result.current.handleSubmit(mockSubmit);
    });
    
    expect(result.current.errors.name).toBe('Name is required');
    expect(result.current.errors.email).toBe('Invalid email');
    expect(mockSubmit).not.toHaveBeenCalled();
  });
});

// API service testing
describe('UserService', () => {
  let userService: UserService;
  let mockApiClient: MockApiClient;
  
  beforeEach(() => {
    mockApiClient = {
      get: vi.fn(),
      post: vi.fn(),
      put: vi.fn(),
      delete: vi.fn(),
    };
    
    userService = new UserService(mockApiClient as unknown as ApiClient);
  });
  
  it('fetches users successfully', async () => {
    const mockUsers: User[] = [
      {
        id: '1',
        name: 'John Doe',
        email: 'john@example.com',
        createdAt: '2023-01-01T00:00:00Z',
        updatedAt: '2023-01-01T00:00:00Z',
      },
    ];
    
    mockApiClient.get.mockResolvedValue({
      data: mockUsers,
      message: 'Success',
      success: true,
    });
    
    const result = await userService.getUsers();
    
    expect(mockApiClient.get).toHaveBeenCalledWith('/users');
    expect(result).toEqual(mockUsers);
  });
  
  it('creates user successfully', async () => {
    const newUserData: CreateUserRequest = {
      name: 'Jane Doe',
      email: 'jane@example.com',
    };
    
    const createdUser: User = {
      id: '2',
      ...newUserData,
      createdAt: '2023-01-01T00:00:00Z',
      updatedAt: '2023-01-01T00:00:00Z',
    };
    
    mockApiClient.post.mockResolvedValue({
      data: createdUser,
      message: 'User created',
      success: true,
    });
    
    const result = await userService.createUser(newUserData);
    
    expect(mockApiClient.post).toHaveBeenCalledWith('/users', newUserData);
    expect(result).toEqual(createdUser);
  });
});
```

## Best Practices for Frontend TypeScript

### 1. Component Development Guidelines

- **Props Interface Design**: Always define explicit interfaces for component props
- **Generic Components**: Use generics for reusable components with varying data types
- **Ref Forwarding**: Use `forwardRef` for components that need to expose DOM references
- **Event Handlers**: Type event handlers with specific event types
- **Default Props**: Use default parameters instead of `defaultProps` for better TypeScript support

### 2. Type Safety Guidelines

- **Strict Configuration**: Enable all strict TypeScript compiler options
- **No Any Types**: Avoid `any` type; use `unknown` or specific types instead
- **Type Guards**: Implement type guards for runtime type checking
- **Branded Types**: Use branded types for values that need additional type safety
- **Utility Types**: Leverage TypeScript utility types (`Pick`, `Omit`, `Partial`, etc.)

### 3. Performance Considerations

- **Bundle Size**: Monitor TypeScript's impact on bundle size
- **Compilation Speed**: Optimize TypeScript configuration for faster builds
- **Runtime Overhead**: Minimize runtime type checking; prefer compile-time checks
- **Tree Shaking**: Use ES modules and proper imports for tree shaking
- **Code Splitting**: Implement lazy loading with proper TypeScript types

## Context Usage Guidelines

**For AI Agents in Frontend Developer Role:**
1. Focus on practical implementation patterns and component development
2. Include specific TypeScript configurations and real-world examples
3. Consider accessibility and user experience in all implementations
4. Think about form handling, API integration, and state management
5. Use current TypeScript 5.7+ features and patterns

**Don't Include:**
- High-level architectural decisions (use architect context)
- Backend-specific TypeScript patterns (use backend-dev context)
- Advanced build configuration (use build/deployment contexts)
- Complex type theory (use advanced TypeScript contexts)

This context should guide day-to-day TypeScript development tasks in frontend applications.