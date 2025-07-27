# Frontend Testing Context - For AI Agent Frontend Developers

## Current Frontend Testing Context

**Modern Frontend Testing Stack** (2025-07-25)
- **Component Testing**: React Testing Library, Vue Test Utils, Svelte Testing Library
- **End-to-End Testing**: Playwright 1.40+, Cypress 13.x with component testing
- **Visual Testing**: Chromatic, Percy, Storybook visual regression
- **Performance Testing**: Lighthouse CI, WebPageTest, Core Web Vitals monitoring

## Essential Frontend Testing Patterns

### 1. Component Testing Fundamentals

```typescript
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { vi } from 'vitest';

// Component under test
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  onClick?: () => void;
  children: React.ReactNode;
}

const Button: React.FC<ButtonProps> = ({ 
  variant, 
  size = 'md', 
  disabled = false, 
  loading = false, 
  onClick, 
  children 
}) => {
  const baseClasses = 'rounded font-medium transition-colors';
  const variantClasses = {
    primary: 'bg-blue-600 text-white hover:bg-blue-700',
    secondary: 'bg-gray-200 text-gray-900 hover:bg-gray-300',
    danger: 'bg-red-600 text-white hover:bg-red-700'
  };
  const sizeClasses = {
    sm: 'px-3 py-1 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg'
  };

  return (
    <button
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]}`}
      disabled={disabled || loading}
      onClick={onClick}
      aria-label={loading ? 'Loading...' : undefined}
    >
      {loading ? (
        <>
          <span className="animate-spin inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full mr-2" />
          Loading...
        </>
      ) : (
        children
      )}
    </button>
  );
};

// Comprehensive component tests
describe('Button Component', () => {
  it('renders with correct text and variant styles', () => {
    render(<Button variant="primary">Click me</Button>);
    
    const button = screen.getByRole('button', { name: /click me/i });
    expect(button).toBeInTheDocument();
    expect(button).toHaveClass('bg-blue-600', 'text-white');
  });

  it('handles different sizes according to design specifications', () => {
    const { rerender } = render(<Button variant="primary" size="sm">Small</Button>);
    expect(screen.getByRole('button')).toHaveClass('px-3', 'py-1', 'text-sm');

    rerender(<Button variant="primary" size="lg">Large</Button>);
    expect(screen.getByRole('button')).toHaveClass('px-6', 'py-3', 'text-lg');
  });

  it('calls onClick handler when clicked', async () => {
    const user = userEvent.setup();
    const handleClick = vi.fn();
    
    render(<Button variant="primary" onClick={handleClick}>Click me</Button>);
    
    await user.click(screen.getByRole('button'));
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('does not call onClick when disabled', async () => {
    const user = userEvent.setup();
    const handleClick = vi.fn();
    
    render(<Button variant="primary" disabled onClick={handleClick}>Disabled</Button>);
    
    const button = screen.getByRole('button');
    expect(button).toBeDisabled();
    
    await user.click(button);
    expect(handleClick).not.toHaveBeenCalled();
  });

  it('shows loading state with appropriate visual indicators', () => {
    render(<Button variant="primary" loading>Loading</Button>);
    
    const button = screen.getByRole('button', { name: /loading/i });
    expect(button).toBeDisabled();
    expect(button).toHaveTextContent('Loading...');
    expect(button.querySelector('.animate-spin')).toBeInTheDocument();
  });

  it('supports keyboard navigation', async () => {
    const user = userEvent.setup();
    const handleClick = vi.fn();
    
    render(<Button variant="primary" onClick={handleClick}>Press me</Button>);
    
    const button = screen.getByRole('button');
    button.focus();
    
    await user.keyboard('{Enter}');
    expect(handleClick).toHaveBeenCalledTimes(1);
    
    await user.keyboard(' ');
    expect(handleClick).toHaveBeenCalledTimes(2);
  });

  it('meets accessibility requirements', () => {
    render(<Button variant="danger">Delete</Button>);
    
    const button = screen.getByRole('button', { name: /delete/i });
    expect(button).toBeInTheDocument();
    expect(button).toHaveAttribute('type', 'button');
  });
});
```

### 2. Form Testing Patterns

```typescript
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { vi } from 'vitest';

// Form component under test
interface ContactFormData {
  name: string;
  email: string;
  message: string;
  newsletter: boolean;
}

interface ContactFormProps {
  onSubmit: (data: ContactFormData) => Promise<void>;
  initialData?: Partial<ContactFormData>;
}

const ContactForm: React.FC<ContactFormProps> = ({ onSubmit, initialData = {} }) => {
  const [formData, setFormData] = useState<ContactFormData>({
    name: initialData.name || '',
    email: initialData.email || '',
    message: initialData.message || '',
    newsletter: initialData.newsletter || false,
  });
  const [errors, setErrors] = useState<Partial<ContactFormData>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);

  const validateForm = (): boolean => {
    const newErrors: Partial<ContactFormData> = {};
    
    if (!formData.name.trim()) newErrors.name = 'Name is required';
    if (!formData.email.trim()) newErrors.email = 'Email is required';
    else if (!/\S+@\S+\.\S+/.test(formData.email)) newErrors.email = 'Email is invalid';
    if (!formData.message.trim()) newErrors.message = 'Message is required';
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) return;
    
    setIsSubmitting(true);
    try {
      await onSubmit(formData);
    } catch (error) {
      console.error('Form submission failed:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} noValidate>
      <div className="mb-4">
        <label htmlFor="name" className="block text-sm font-medium mb-1">
          Name *
        </label>
        <input
          id="name"
          type="text"
          value={formData.name}
          onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
          className={`w-full px-3 py-2 border rounded-md ${
            errors.name ? 'border-red-500' : 'border-gray-300'
          }`}
          aria-invalid={!!errors.name}
          aria-describedby={errors.name ? 'name-error' : undefined}
        />
        {errors.name && (
          <p id="name-error" className="text-red-500 text-sm mt-1" role="alert">
            {errors.name}
          </p>
        )}
      </div>

      <div className="mb-4">
        <label htmlFor="email" className="block text-sm font-medium mb-1">
          Email *
        </label>
        <input
          id="email"
          type="email"
          value={formData.email}
          onChange={(e) => setFormData(prev => ({ ...prev, email: e.target.value }))}
          className={`w-full px-3 py-2 border rounded-md ${
            errors.email ? 'border-red-500' : 'border-gray-300'
          }`}
          aria-invalid={!!errors.email}
          aria-describedby={errors.email ? 'email-error' : undefined}
        />
        {errors.email && (
          <p id="email-error" className="text-red-500 text-sm mt-1" role="alert">
            {errors.email}
          </p>
        )}
      </div>

      <div className="mb-4">
        <label htmlFor="message" className="block text-sm font-medium mb-1">
          Message *
        </label>
        <textarea
          id="message"
          rows={4}
          value={formData.message}
          onChange={(e) => setFormData(prev => ({ ...prev, message: e.target.value }))}
          className={`w-full px-3 py-2 border rounded-md ${
            errors.message ? 'border-red-500' : 'border-gray-300'
          }`}
          aria-invalid={!!errors.message}
          aria-describedby={errors.message ? 'message-error' : undefined}
        />
        {errors.message && (
          <p id="message-error" className="text-red-500 text-sm mt-1" role="alert">
            {errors.message}
          </p>
        )}
      </div>

      <div className="mb-6">
        <label className="flex items-center">
          <input
            type="checkbox"
            checked={formData.newsletter}
            onChange={(e) => setFormData(prev => ({ ...prev, newsletter: e.target.checked }))}
            className="mr-2"
          />
          <span className="text-sm">Subscribe to newsletter</span>
        </label>
      </div>

      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50"
      >
        {isSubmitting ? 'Sending...' : 'Send Message'}
      </button>
    </form>
  );
};

// Comprehensive form tests
describe('ContactForm', () => {
  const mockOnSubmit = vi.fn();

  beforeEach(() => {
    mockOnSubmit.mockClear();
  });

  it('renders all form fields with proper labels and validation', () => {
    render(<ContactForm onSubmit={mockOnSubmit} />);
    
    expect(screen.getByLabelText(/name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/message/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/newsletter/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /send message/i })).toBeInTheDocument();
  });

  it('populates form with initial data', () => {
    const initialData = {
      name: 'John Doe',
      email: 'john@example.com',
      newsletter: true,
    };
    
    render(<ContactForm onSubmit={mockOnSubmit} initialData={initialData} />);
    
    expect(screen.getByDisplayValue('John Doe')).toBeInTheDocument();
    expect(screen.getByDisplayValue('john@example.com')).toBeInTheDocument();
    expect(screen.getByRole('checkbox')).toBeChecked();
  });

  it('validates required fields on submit', async () => {
    const user = userEvent.setup();
    render(<ContactForm onSubmit={mockOnSubmit} />);
    
    await user.click(screen.getByRole('button', { name: /send message/i }));
    
    expect(screen.getByText('Name is required')).toBeInTheDocument();
    expect(screen.getByText('Email is required')).toBeInTheDocument();
    expect(screen.getByText('Message is required')).toBeInTheDocument();
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  it('validates email format', async () => {
    const user = userEvent.setup();
    render(<ContactForm onSubmit={mockOnSubmit} />);
    
    await user.type(screen.getByLabelText(/name/i), 'John Doe');
    await user.type(screen.getByLabelText(/email/i), 'invalid-email');
    await user.type(screen.getByLabelText(/message/i), 'Test message');
    await user.click(screen.getByRole('button', { name: /send message/i }));
    
    expect(screen.getByText('Email is invalid')).toBeInTheDocument();
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  it('submits form with valid data', async () => {
    const user = userEvent.setup();
    mockOnSubmit.mockResolvedValue(undefined);
    
    render(<ContactForm onSubmit={mockOnSubmit} />);
    
    await user.type(screen.getByLabelText(/name/i), 'John Doe');
    await user.type(screen.getByLabelText(/email/i), 'john@example.com');
    await user.type(screen.getByLabelText(/message/i), 'Test message');
    await user.click(screen.getByLabelText(/newsletter/i));
    await user.click(screen.getByRole('button', { name: /send message/i }));
    
    await waitFor(() => {
      expect(mockOnSubmit).toHaveBeenCalledWith({
        name: 'John Doe',
        email: 'john@example.com',
        message: 'Test message',
        newsletter: true,
      });
    });
  });

  it('shows loading state during submission', async () => {
    const user = userEvent.setup();
    let resolveSubmit: () => void;
    const submitPromise = new Promise<void>(resolve => { resolveSubmit = resolve; });
    mockOnSubmit.mockReturnValue(submitPromise);
    
    render(<ContactForm onSubmit={mockOnSubmit} />);
    
    await user.type(screen.getByLabelText(/name/i), 'John Doe');
    await user.type(screen.getByLabelText(/email/i), 'john@example.com');
    await user.type(screen.getByLabelText(/message/i), 'Test message');
    await user.click(screen.getByRole('button', { name: /send message/i }));
    
    expect(screen.getByRole('button', { name: /sending/i })).toBeDisabled();
    
    resolveSubmit();
    await waitFor(() => {
      expect(screen.getByRole('button', { name: /send message/i })).not.toBeDisabled();
    });
  });

  it('clears errors when user starts typing', async () => {
    const user = userEvent.setup();
    render(<ContactForm onSubmit={mockOnSubmit} />);
    
    // Submit to show errors
    await user.click(screen.getByRole('button', { name: /send message/i }));
    expect(screen.getByText('Name is required')).toBeInTheDocument();
    
    // Start typing to clear error
    await user.type(screen.getByLabelText(/name/i), 'J');
    expect(screen.queryByText('Name is required')).not.toBeInTheDocument();
  });

  it('handles form submission errors gracefully', async () => {
    const user = userEvent.setup();
    const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
    mockOnSubmit.mockRejectedValue(new Error('Network error'));
    
    render(<ContactForm onSubmit={mockOnSubmit} />);
    
    await user.type(screen.getByLabelText(/name/i), 'John Doe');
    await user.type(screen.getByLabelText(/email/i), 'john@example.com');
    await user.type(screen.getByLabelText(/message/i), 'Test message');
    await user.click(screen.getByRole('button', { name: /send message/i }));
    
    await waitFor(() => {
      expect(consoleErrorSpy).toHaveBeenCalledWith('Form submission failed:', expect.any(Error));
      expect(screen.getByRole('button', { name: /send message/i })).not.toBeDisabled();
    });
    
    consoleErrorSpy.mockRestore();
  });
});
```

### 3. Interactive Component Testing

```typescript
// Complex interactive component testing
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';

// Modal component with complex interactions
interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
  size?: 'sm' | 'md' | 'lg';
  closeOnBackdrop?: boolean;
  closeOnEscape?: boolean;
}

const Modal: React.FC<ModalProps> = ({
  isOpen,
  onClose,
  title,
  children,
  size = 'md',
  closeOnBackdrop = true,
  closeOnEscape = true,
}) => {
  const modalRef = useRef<HTMLDivElement>(null);
  const previousFocus = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (isOpen) {
      previousFocus.current = document.activeElement as HTMLElement;
      modalRef.current?.focus();
    } else {
      previousFocus.current?.focus();
    }
  }, [isOpen]);

  useEffect(() => {
    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && closeOnEscape) {
        onClose();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      document.body.style.overflow = 'hidden';
    }

    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, closeOnEscape, onClose]);

  const handleBackdropClick = (event: React.MouseEvent) => {
    if (event.target === event.currentTarget && closeOnBackdrop) {
      onClose();
    }
  };

  if (!isOpen) return null;

  const sizeClasses = {
    sm: 'max-w-sm',
    md: 'max-w-md',
    lg: 'max-w-lg',
  };

  return createPortal(
    <div
      className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50"
      onClick={handleBackdropClick}
      data-testid="modal-backdrop"
    >
      <div
        ref={modalRef}
        className={`bg-white rounded-lg shadow-lg ${sizeClasses[size]} w-full mx-4`}
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        tabIndex={-1}
      >
        <div className="flex items-center justify-between p-4 border-b">
          <h2 id="modal-title" className="text-lg font-semibold">
            {title}
          </h2>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600"
            aria-label="Close modal"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div className="p-4">
          {children}
        </div>
      </div>
    </div>,
    document.body
  );
};

// Comprehensive modal tests
describe('Modal Component', () => {
  const mockOnClose = vi.fn();

  beforeEach(() => {
    mockOnClose.mockClear();
    // Clean up any existing modals
    document.body.innerHTML = '';
  });

  afterEach(() => {
    // Restore body overflow
    document.body.style.overflow = 'unset';
  });

  it('renders modal when open', () => {
    render(
      <Modal isOpen={true} onClose={mockOnClose} title="Test Modal">
        <p>Modal content</p>
      </Modal>
    );

    expect(screen.getByRole('dialog')).toBeInTheDocument();
    expect(screen.getByText('Test Modal')).toBeInTheDocument();
    expect(screen.getByText('Modal content')).toBeInTheDocument();
  });

  it('does not render when closed', () => {
    render(
      <Modal isOpen={false} onClose={mockOnClose} title="Test Modal">
        <p>Modal content</p>
      </Modal>
    );

    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  });

  it('closes when close button is clicked', async () => {
    const user = userEvent.setup();
    render(
      <Modal isOpen={true} onClose={mockOnClose} title="Test Modal">
        <p>Modal content</p>
      </Modal>
    );

    await user.click(screen.getByLabelText('Close modal'));
    expect(mockOnClose).toHaveBeenCalledTimes(1);
  });

  it('closes when backdrop is clicked', async () => {
    const user = userEvent.setup();
    render(
      <Modal isOpen={true} onClose={mockOnClose} title="Test Modal">
        <p>Modal content</p>
      </Modal>
    );

    await user.click(screen.getByTestId('modal-backdrop'));
    expect(mockOnClose).toHaveBeenCalledTimes(1);
  });

  it('does not close when backdrop clicked if closeOnBackdrop is false', async () => {
    const user = userEvent.setup();
    render(
      <Modal isOpen={true} onClose={mockOnClose} title="Test Modal" closeOnBackdrop={false}>
        <p>Modal content</p>
      </Modal>
    );

    await user.click(screen.getByTestId('modal-backdrop'));
    expect(mockOnClose).not.toHaveBeenCalled();
  });

  it('closes when Escape key is pressed', async () => {
    const user = userEvent.setup();
    render(
      <Modal isOpen={true} onClose={mockOnClose} title="Test Modal">
        <p>Modal content</p>
      </Modal>
    );

    await user.keyboard('{Escape}');
    expect(mockOnClose).toHaveBeenCalledTimes(1);
  });

  it('does not close when Escape pressed if closeOnEscape is false', async () => {
    const user = userEvent.setup();
    render(
      <Modal isOpen={true} onClose={mockOnClose} title="Test Modal" closeOnEscape={false}>
        <p>Modal content</p>
      </Modal>
    );

    await user.keyboard('{Escape}');
    expect(mockOnClose).not.toHaveBeenCalled();
  });

  it('traps focus within modal', async () => {
    const user = userEvent.setup();
    render(
      <div>
        <button>Outside button</button>
        <Modal isOpen={true} onClose={mockOnClose} title="Test Modal">
          <button>Inside button 1</button>
          <button>Inside button 2</button>
        </Modal>
      </div>
    );

    const modal = screen.getByRole('dialog');
    const closeButton = screen.getByLabelText('Close modal');
    const insideButton1 = screen.getByText('Inside button 1');
    const insideButton2 = screen.getByText('Inside button 2');

    // Modal should receive initial focus
    expect(modal).toHaveFocus();

    // Tab through modal elements
    await user.tab();
    expect(closeButton).toHaveFocus();

    await user.tab();
    expect(insideButton1).toHaveFocus();

    await user.tab();
    expect(insideButton2).toHaveFocus();

    // Tab should cycle back to close button
    await user.tab();
    expect(closeButton).toHaveFocus();
  });

  it('prevents body scroll when open', () => {
    const { rerender } = render(
      <Modal isOpen={false} onClose={mockOnClose} title="Test Modal">
        <p>Modal content</p>
      </Modal>
    );

    expect(document.body.style.overflow).toBe('');

    rerender(
      <Modal isOpen={true} onClose={mockOnClose} title="Test Modal">
        <p>Modal content</p>
      </Modal>
    );

    expect(document.body.style.overflow).toBe('hidden');
  });

  it('restores body scroll when closed', () => {
    const { rerender } = render(
      <Modal isOpen={true} onClose={mockOnClose} title="Test Modal">
        <p>Modal content</p>
      </Modal>
    );

    expect(document.body.style.overflow).toBe('hidden');

    rerender(
      <Modal isOpen={false} onClose={mockOnClose} title="Test Modal">
        <p>Modal content</p>
      </Modal>
    );

    expect(document.body.style.overflow).toBe('unset');
  });

  it('applies correct size classes', () => {
    const { rerender } = render(
      <Modal isOpen={true} onClose={mockOnClose} title="Small Modal" size="sm">
        <p>Content</p>
      </Modal>
    );

    expect(screen.getByRole('dialog')).toHaveClass('max-w-sm');

    rerender(
      <Modal isOpen={true} onClose={mockOnClose} title="Large Modal" size="lg">
        <p>Content</p>
      </Modal>
    );

    expect(screen.getByRole('dialog')).toHaveClass('max-w-lg');
  });

  it('has proper accessibility attributes', () => {
    render(
      <Modal isOpen={true} onClose={mockOnClose} title="Accessible Modal">
        <p>Modal content</p>
      </Modal>
    );

    const modal = screen.getByRole('dialog');
    expect(modal).toHaveAttribute('aria-modal', 'true');
    expect(modal).toHaveAttribute('aria-labelledby', 'modal-title');
    expect(screen.getByText('Accessible Modal')).toHaveAttribute('id', 'modal-title');
  });
});
```

### 4. Async Component Testing

```typescript
// Testing components with async operations
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { vi } from 'vitest';

// Mock API service
const mockApiService = {
  getUsers: vi.fn(),
  createUser: vi.fn(),
  updateUser: vi.fn(),
  deleteUser: vi.fn(),
};

// User list component with CRUD operations
interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user';
}

interface UserListProps {
  apiService: typeof mockApiService;
}

const UserList: React.FC<UserListProps> = ({ apiService }) => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editingUser, setEditingUser] = useState<User | null>(null);

  useEffect(() => {
    loadUsers();
  }, []);

  const loadUsers = async () => {
    try {
      setLoading(true);
      setError(null);
      const fetchedUsers = await apiService.getUsers();
      setUsers(fetchedUsers);
    } catch (err) {
      setError('Failed to load users');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteUser = async (userId: string) => {
    if (!confirm('Are you sure you want to delete this user?')) return;

    try {
      await apiService.deleteUser(userId);
      setUsers(prev => prev.filter(user => user.id !== userId));
    } catch (err) {
      setError('Failed to delete user');
    }
  };

  const handleUpdateUser = async (updatedUser: User) => {
    try {
      const result = await apiService.updateUser(updatedUser.id, updatedUser);
      setUsers(prev => prev.map(user => user.id === result.id ? result : user));
      setEditingUser(null);
    } catch (err) {
      setError('Failed to update user');
    }
  };

  if (loading) {
    return (
      <div role="status" aria-label="Loading users">
        <div className="animate-spin w-8 h-8 border-4 border-blue-500 border-t-transparent rounded-full" />
        <span className="sr-only">Loading users...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div role="alert" className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
        <p>{error}</p>
        <button
          onClick={loadUsers}
          className="mt-2 bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">Users</h2>
      
      {users.length === 0 ? (
        <p className="text-gray-500">No users found.</p>
      ) : (
        <div className="space-y-4">
          {users.map(user => (
            <div key={user.id} className="border rounded-lg p-4 flex justify-between items-center">
              {editingUser?.id === user.id ? (
                <UserEditForm
                  user={editingUser}
                  onSave={handleUpdateUser}
                  onCancel={() => setEditingUser(null)}
                />
              ) : (
                <>
                  <div>
                    <h3 className="font-medium">{user.name}</h3>
                    <p className="text-gray-600">{user.email}</p>
                    <span className="text-sm bg-gray-100 px-2 py-1 rounded">{user.role}</span>
                  </div>
                  <div className="space-x-2">
                    <button
                      onClick={() => setEditingUser(user)}
                      className="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleDeleteUser(user.id)}
                      className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600"
                    >
                      Delete
                    </button>
                  </div>
                </>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

// Edit form component
interface UserEditFormProps {
  user: User;
  onSave: (user: User) => void;
  onCancel: () => void;
}

const UserEditForm: React.FC<UserEditFormProps> = ({ user, onSave, onCancel }) => {
  const [formData, setFormData] = useState(user);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSave(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="flex-1 space-y-2">
      <input
        type="text"
        value={formData.name}
        onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
        className="w-full px-3 py-2 border rounded"
        placeholder="Name"
        required
      />
      <input
        type="email"
        value={formData.email}
        onChange={(e) => setFormData(prev => ({ ...prev, email: e.target.value }))}
        className="w-full px-3 py-2 border rounded"
        placeholder="Email"
        required
      />
      <select
        value={formData.role}
        onChange={(e) => setFormData(prev => ({ ...prev, role: e.target.value as 'admin' | 'user' }))}
        className="w-full px-3 py-2 border rounded"
      >
        <option value="user">User</option>
        <option value="admin">Admin</option>
      </select>
      <div className="flex space-x-2">
        <button
          type="submit"
          className="bg-green-500 text-white px-3 py-1 rounded hover:bg-green-600"
        >
          Save
        </button>
        <button
          type="button"
          onClick={onCancel}
          className="bg-gray-500 text-white px-3 py-1 rounded hover:bg-gray-600"
        >
          Cancel
        </button>
      </div>
    </form>
  );
};

// Comprehensive async component tests
describe('UserList Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    // Mock window.confirm
    Object.defineProperty(window, 'confirm', {
      writable: true,
      value: vi.fn(),
    });
  });

  it('displays loading state initially', () => {
    mockApiService.getUsers.mockReturnValue(new Promise(() => {})); // Never resolves
    
    render(<UserList apiService={mockApiService} />);
    
    expect(screen.getByRole('status', { name: /loading users/i })).toBeInTheDocument();
    expect(screen.getByText('Loading users...')).toBeInTheDocument();
  });

  it('displays users after successful load', async () => {
    const mockUsers: User[] = [
      { id: '1', name: 'John Doe', email: 'john@example.com', role: 'admin' },
      { id: '2', name: 'Jane Smith', email: 'jane@example.com', role: 'user' },
    ];
    
    mockApiService.getUsers.mockResolvedValue(mockUsers);
    
    render(<UserList apiService={mockApiService} />);
    
    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument();
    });
    
    expect(screen.getByText('john@example.com')).toBeInTheDocument();
    expect(screen.getByText('Jane Smith')).toBeInTheDocument();
    expect(screen.getByText('jane@example.com')).toBeInTheDocument();
    expect(screen.getAllByText('admin')).toHaveLength(1);
    expect(screen.getAllByText('user')).toHaveLength(1);
  });

  it('displays error message when load fails', async () => {
    mockApiService.getUsers.mockRejectedValue(new Error('Network error'));
    
    render(<UserList apiService={mockApiService} />);
    
    await waitFor(() => {
      expect(screen.getByRole('alert')).toBeInTheDocument();
    });
    
    expect(screen.getByText('Failed to load users')).toBeInTheDocument();
    expect(screen.getByText('Retry')).toBeInTheDocument();
  });

  it('retries loading when retry button is clicked', async () => {
    const user = userEvent.setup();
    
    // First call fails
    mockApiService.getUsers.mockRejectedValueOnce(new Error('Network error'));
    // Second call succeeds
    mockApiService.getUsers.mockResolvedValue([]);
    
    render(<UserList apiService={mockApiService} />);
    
    await waitFor(() => {
      expect(screen.getByText('Failed to load users')).toBeInTheDocument();
    });
    
    await user.click(screen.getByText('Retry'));
    
    await waitFor(() => {
      expect(screen.getByText('No users found.')).toBeInTheDocument();
    });
    
    expect(mockApiService.getUsers).toHaveBeenCalledTimes(2);
  });

  it('displays empty state when no users exist', async () => {
    mockApiService.getUsers.mockResolvedValue([]);
    
    render(<UserList apiService={mockApiService} />);
    
    await waitFor(() => {
      expect(screen.getByText('No users found.')).toBeInTheDocument();
    });
  });

  it('deletes user when delete button is clicked and confirmed', async () => {
    const user = userEvent.setup();
    const mockUsers: User[] = [
      { id: '1', name: 'John Doe', email: 'john@example.com', role: 'admin' },
    ];
    
    mockApiService.getUsers.mockResolvedValue(mockUsers);
    mockApiService.deleteUser.mockResolvedValue(undefined);
    (window.confirm as jest.Mock).mockReturnValue(true);
    
    render(<UserList apiService={mockApiService} />);
    
    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument();
    });
    
    await user.click(screen.getByText('Delete'));
    
    expect(window.confirm).toHaveBeenCalledWith('Are you sure you want to delete this user?');
    
    await waitFor(() => {
      expect(screen.queryByText('John Doe')).not.toBeInTheDocument();
    });
    
    expect(mockApiService.deleteUser).toHaveBeenCalledWith('1');
  });

  it('does not delete user when delete is not confirmed', async () => {
    const user = userEvent.setup();
    const mockUsers: User[] = [
      { id: '1', name: 'John Doe', email: 'john@example.com', role: 'admin' },
    ];
    
    mockApiService.getUsers.mockResolvedValue(mockUsers);
    (window.confirm as jest.Mock).mockReturnValue(false);
    
    render(<UserList apiService={mockApiService} />);
    
    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument();
    });
    
    await user.click(screen.getByText('Delete'));
    
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(mockApiService.deleteUser).not.toHaveBeenCalled();
  });

  it('edits user when edit button is clicked', async () => {
    const user = userEvent.setup();
    const mockUsers: User[] = [
      { id: '1', name: 'John Doe', email: 'john@example.com', role: 'user' },
    ];
    
    mockApiService.getUsers.mockResolvedValue(mockUsers);
    mockApiService.updateUser.mockResolvedValue({
      id: '1',
      name: 'John Updated',
      email: 'john.updated@example.com',
      role: 'admin',
    });
    
    render(<UserList apiService={mockApiService} />);
    
    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument();
    });
    
    await user.click(screen.getByText('Edit'));
    
    // Form should appear
    expect(screen.getByDisplayValue('John Doe')).toBeInTheDocument();
    expect(screen.getByDisplayValue('john@example.com')).toBeInTheDocument();
    
    // Update form values
    await user.clear(screen.getByDisplayValue('John Doe'));
    await user.type(screen.getByDisplayValue(''), 'John Updated');
    
    await user.clear(screen.getByDisplayValue('john@example.com'));
    await user.type(screen.getByDisplayValue(''), 'john.updated@example.com');
    
    await user.selectOptions(screen.getByDisplayValue('user'), 'admin');
    
    // Save changes
    await user.click(screen.getByText('Save'));
    
    await waitFor(() => {
      expect(screen.getByText('John Updated')).toBeInTheDocument();
    });
    
    expect(screen.getByText('john.updated@example.com')).toBeInTheDocument();
    expect(mockApiService.updateUser).toHaveBeenCalledWith('1', {
      id: '1',
      name: 'John Updated',
      email: 'john.updated@example.com',
      role: 'admin',
    });
  });

  it('cancels edit when cancel button is clicked', async () => {
    const user = userEvent.setup();
    const mockUsers: User[] = [
      { id: '1', name: 'John Doe', email: 'john@example.com', role: 'user' },
    ];
    
    mockApiService.getUsers.mockResolvedValue(mockUsers);
    
    render(<UserList apiService={mockApiService} />);
    
    await waitFor(() => {
      expect(screen.getByText('John Doe')).toBeInTheDocument();
    });
    
    await user.click(screen.getByText('Edit'));
    
    // Form should appear
    expect(screen.getByDisplayValue('John Doe')).toBeInTheDocument();
    
    await user.click(screen.getByText('Cancel'));
    
    // Form should disappear, original data should be shown
    expect(screen.queryByDisplayValue('John Doe')).not.toBeInTheDocument();
    expect(screen.getByText('John Doe')).toBeInTheDocument();
    expect(mockApiService.updateUser).not.toHaveBeenCalled();
  });
});
```

### 5. Visual and Accessibility Testing

```typescript
// Visual regression and accessibility testing
import { render, screen } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';

// Extend Jest matchers
expect.extend(toHaveNoViolations);

// Component for visual testing
interface CardProps {
  title: string;
  description: string;
  imageUrl?: string;
  tags?: string[];
  actions?: React.ReactNode;
  variant?: 'default' | 'highlighted' | 'muted';
}

const Card: React.FC<CardProps> = ({
  title,
  description,
  imageUrl,
  tags = [],
  actions,
  variant = 'default'
}) => {
  const variantClasses = {
    default: 'bg-white border-gray-200',
    highlighted: 'bg-blue-50 border-blue-200',
    muted: 'bg-gray-50 border-gray-300'
  };

  return (
    <article className={`border rounded-lg p-6 shadow-sm ${variantClasses[variant]}`}>
      {imageUrl && (
        <img
          src={imageUrl}
          alt={`Image for ${title}`}
          className="w-full h-48 object-cover rounded-md mb-4"
        />
      )}
      
      <header className="mb-3">
        <h3 className="text-xl font-semibold text-gray-900">{title}</h3>
      </header>
      
      <p className="text-gray-600 mb-4">{description}</p>
      
      {tags.length > 0 && (
        <div className="flex flex-wrap gap-2 mb-4">
          {tags.map((tag, index) => (
            <span
              key={index}
              className="bg-gray-100 text-gray-700 px-2 py-1 rounded-md text-sm"
            >
              {tag}
            </span>
          ))}
        </div>
      )}
      
      {actions && (
        <footer className="flex gap-2 pt-4 border-t border-gray-200">
          {actions}
        </footer>
      )}
    </article>
  );
};

// Visual testing with Storybook integration
describe('Card Visual Tests', () => {
  const defaultProps = {
    title: 'Sample Card Title',
    description: 'This is a sample card description that provides context about the card content.',
    tags: ['React', 'TypeScript', 'Testing'],
    actions: (
      <>
        <button className="bg-blue-500 text-white px-4 py-2 rounded">Action 1</button>
        <button className="bg-gray-500 text-white px-4 py-2 rounded">Action 2</button>
      </>
    )
  };

  it('renders default variant with expected styles', () => {
    const { container } = render(<Card {...defaultProps} />);
    
    // Visual snapshot test
    expect(container.firstChild).toMatchSnapshot('card-default');
    
    // Verify visual elements are present
    expect(screen.getByRole('article')).toHaveClass('bg-white', 'border-gray-200');
    expect(screen.getByText('Sample Card Title')).toBeInTheDocument();
    expect(screen.getByText(/sample card description/i)).toBeInTheDocument();
  });

  it('renders highlighted variant with blue background', () => {
    const { container } = render(<Card {...defaultProps} variant="highlighted" />);
    
    expect(container.firstChild).toMatchSnapshot('card-highlighted');
    expect(screen.getByRole('article')).toHaveClass('bg-blue-50', 'border-blue-200');
  });

  it('renders muted variant with reduced opacity', () => {
    const { container } = render(<Card {...defaultProps} variant="muted" />);
    
    expect(container.firstChild).toMatchSnapshot('card-muted');
    expect(screen.getByRole('article')).toHaveClass('bg-gray-50', 'border-gray-300');
  });

  it('renders with image using proper aspect ratio', () => {
    const { container } = render(
      <Card {...defaultProps} imageUrl="https://example.com/image.jpg" />
    );
    
    expect(container.firstChild).toMatchSnapshot('card-with-image');
    
    const image = screen.getByRole('img');
    expect(image).toHaveAttribute('src', 'https://example.com/image.jpg');
    expect(image).toHaveAttribute('alt', 'Image for Sample Card Title');
  });

  it('renders without optional elements', () => {
    const minimalProps = {
      title: 'Minimal Card',
      description: 'Basic card with no extras'
    };
    
    const { container } = render(<Card {...minimalProps} />);
    
    expect(container.firstChild).toMatchSnapshot('card-minimal');
    expect(screen.queryByRole('img')).not.toBeInTheDocument();
    expect(screen.queryByText('React')).not.toBeInTheDocument();
  });
});

// Accessibility testing
describe('Card Accessibility Tests', () => {
  const defaultProps = {
    title: 'Accessible Card Title',
    description: 'This card is designed to be fully accessible to all users.',
    tags: ['Accessibility', 'WCAG', 'Testing'],
    actions: (
      <>
        <button>Primary Action</button>
        <button>Secondary Action</button>
      </>
    )
  };

  it('should not have accessibility violations', async () => {
    const { container } = render(<Card {...defaultProps} />);
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('should have proper semantic structure', () => {
    render(<Card {...defaultProps} />);
    
    // Check semantic HTML elements
    expect(screen.getByRole('article')).toBeInTheDocument();
    expect(screen.getByRole('banner')).toBeInTheDocument(); // header
    expect(screen.getByRole('contentinfo')).toBeInTheDocument(); // footer
    
    // Check heading hierarchy
    const heading = screen.getByRole('heading', { level: 3 });
    expect(heading).toHaveTextContent('Accessible Card Title');
  });

  it('should have accessible image when provided', async () => {
    const { container } = render(
      <Card {...defaultProps} imageUrl="https://example.com/test.jpg" />
    );
    
    const image = screen.getByRole('img');
    expect(image).toHaveAttribute('alt', 'Image for Accessible Card Title');
    
    // Ensure no accessibility violations with image
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('should have accessible buttons', async () => {
    const { container } = render(<Card {...defaultProps} />);
    
    const buttons = screen.getAllByRole('button');
    expect(buttons).toHaveLength(2);
    
    buttons.forEach(button => {
      expect(button).toHaveTextContent(/action/i);
    });
    
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it('should support keyboard navigation', async () => {
    const user = userEvent.setup();
    const mockPrimaryAction = vi.fn();
    const mockSecondaryAction = vi.fn();
    
    render(
      <Card 
        {...defaultProps}
        actions={
          <>
            <button onClick={mockPrimaryAction}>Primary Action</button>
            <button onClick={mockSecondaryAction}>Secondary Action</button>
          </>
        }
      />
    );
    
    const primaryButton = screen.getByText('Primary Action');
    const secondaryButton = screen.getByText('Secondary Action');
    
    // Test keyboard navigation
    await user.tab();
    expect(primaryButton).toHaveFocus();
    
    await user.tab();
    expect(secondaryButton).toHaveFocus();
    
    // Test keyboard activation
    await user.keyboard('{Enter}');
    expect(mockSecondaryAction).toHaveBeenCalledTimes(1);
    
    primaryButton.focus();
    await user.keyboard(' ');
    expect(mockPrimaryAction).toHaveBeenCalledTimes(1);
  });

  it('should have proper color contrast', async () => {
    // This would be tested with tools like axe-core or Lighthouse accessibility audits
    // For demonstration, we'll check that proper CSS classes are applied
    render(<Card {...defaultProps} variant="highlighted" />);
    
    const card = screen.getByRole('article');
    const title = screen.getByRole('heading');
    
    // Verify classes that should provide good contrast
    expect(card).toHaveClass('bg-blue-50');
    expect(title).toHaveClass('text-gray-900');
    
    // In a real scenario, you might use tools like:
    // - axe-core color contrast rules
    // - Custom color contrast testing utilities
    // - Visual regression testing with color analysis
  });

  it('should be screen reader friendly', () => {
    render(<Card {...defaultProps} />);
    
    // Check that content is structured for screen readers
    const article = screen.getByRole('article');
    const heading = screen.getByRole('heading');
    const description = screen.getByText(/designed to be fully accessible/i);
    
    // Verify reading order and structure
    expect(article).toContainElement(heading);
    expect(article).toContainElement(description);
    
    // Tags should be grouped within the same container element
    const tags = screen.getAllByText(/accessibility|wcag|testing/i);
    expect(tags).toHaveLength(3);
  });
});

// Performance testing for rendering
describe('Card Performance Tests', () => {
  const generateLargeProps = (count: number) => ({
    title: `Card with ${count} tags`,
    description: 'Performance test card with 100+ elements',
    tags: Array.from({ length: count }, (_, i) => `Tag ${i + 1}`),
    actions: (
      <>
        {Array.from({ length: 10 }, (_, i) => (
          <button key={i}>Action {i + 1}</button>
        ))}
      </>
    )
  });

  it('should render quickly with 100+ elements', () => {
    const startTime = performance.now();
    
    render(<Card {...generateLargeProps(100)} />);
    
    const renderTime = performance.now() - startTime;
    
    // Should render in less than 100ms even with 100+ elements
    expect(renderTime).toBeLessThan(100);
    
    // Verify all elements are rendered
    expect(screen.getAllByText(/Tag \d+/)).toHaveLength(100);
    expect(screen.getAllByText(/Action \d+/)).toHaveLength(10);
  });

  it('should handle re-renders within 50ms', () => {
    const { rerender } = render(<Card {...generateLargeProps(50)} />);
    
    const startTime = performance.now();
    
    // Re-render with updated props
    rerender(<Card {...generateLargeProps(50)} variant="highlighted" />);
    
    const rerenderTime = performance.now() - startTime;
    
    // Re-render should be even faster
    expect(rerenderTime).toBeLessThan(50);
    
    // Verify variant change was applied
    expect(screen.getByRole('article')).toHaveClass('bg-blue-50');
  });
});
```

## Frontend Testing Best Practices

### 1. Component Testing Guidelines

- **Test User Behavior**: Focus on what users see and do, not implementation details
- **Use Semantic Queries**: Prefer `getByRole`, `getByLabelText` over `getByTestId`
- **Test Accessibility**: Ensure components work with screen readers and keyboard navigation
- **Mock External Dependencies**: Mock APIs, services, and complex child components
- **Test Error States**: Include loading, error, and empty state scenarios

### 2. User Interaction Testing

- **Use User Events**: Prefer `@testing-library/user-event` over `fireEvent`
- **Test Complete Workflows**: Test multi-step user interactions
- **Handle Async Operations**: Use `waitFor` and proper async/await patterns
- **Test Edge Cases**: Include boundary conditions and error scenarios
- **Verify Side Effects**: Ensure interactions produce expected results

### 3. Visual and Accessibility

- **Snapshot Testing**: Use snapshots for visual regression detection
- **Accessibility Audits**: Run automated accessibility tests with axe
- **Color Contrast**: Verify sufficient color contrast ratios
- **Keyboard Navigation**: Test all interactive elements with keyboard
- **Screen Reader Support**: Ensure proper ARIA attributes and semantic HTML

### 4. Performance Considerations

- **Fast Test Execution**: Keep tests under 10ms each when possible
- **Efficient Rendering**: Mock heavy components and external dependencies
- **Memory Management**: Clean up event listeners and subscriptions
- **Parallel Execution**: Design tests to run safely in parallel
- **Resource Optimization**: Use minimal test data and fixtures

## Context Usage Guidelines

**For AI Agents in Frontend Developer Role:**
1. Focus on practical component testing and user interaction validation
2. Include specific testing library configurations and examples
3. Consider accessibility, performance, and user experience in all tests
4. Think about browser compatibility and responsive behavior
5. Use modern frontend testing tools and patterns

**Don't Include:**
- High-level testing architecture decisions (use architect context)
- Backend API testing details (use backend testing contexts)
- Complex test automation infrastructure (use testing specialist context)
- Basic testing theory (use fundamental learning contexts)

This context should guide day-to-day frontend testing implementation and quality assurance for user interfaces.