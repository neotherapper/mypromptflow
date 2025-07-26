# React Accessibility Context - For AI Agent Accessibility Specialists

## Current React Version Accessibility Context

**React 19.0.0** (Latest as of 2025-07-25)
- **Enhanced ARIA Support**: Improved built-in accessibility attributes
- **Server Components A11y**: Accessibility considerations for server-rendered content
- **Form Accessibility**: Better integration with native form accessibility features
- **React DevTools A11y**: Enhanced accessibility debugging tools

## WCAG 2.1 AA Compliance Standards

### 1. Perceivable Content
```typescript
import { useId } from 'react';

// Proper image accessibility
function AccessibleImage({ 
  src, 
  alt, 
  decorative = false,
  longDescription 
}: {
  src: string;
  alt: string;
  decorative?: boolean;
  longDescription?: string;
}) {
  const descriptionId = useId();
  
  return (
    <>
      <img
        src={src}
        alt={decorative ? '' : alt}
        aria-describedby={longDescription ? descriptionId : undefined}
        role={decorative ? 'presentation' : undefined}
      />
      {longDescription && (
        <div id={descriptionId} className="sr-only">
          {longDescription}
        </div>
      )}
    </>
  );
}

// Color contrast and visual indicators
function AccessibleButton({ 
  children, 
  variant = 'primary',
  disabled = false,
  loading = false,
  onClick 
}: {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'danger';
  disabled?: boolean;
  loading?: boolean;
  onClick: () => void;
}) {
  return (
    <button
      className={`btn btn-${variant} ${disabled || loading ? 'disabled' : ''}`}
      disabled={disabled || loading}
      onClick={onClick}
      aria-disabled={disabled || loading}
      aria-busy={loading}
      style={{
        // Ensure minimum 4.5:1 contrast ratio for AA compliance
        backgroundColor: variant === 'primary' ? '#0066cc' : // 4.6:1 contrast
                        variant === 'danger' ? '#d63031' : // 6.4:1 contrast
                        '#6c757d', // 4.5:1 contrast
        border: '2px solid transparent',
        // Focus indicator with 3:1 contrast ratio
        ':focus': {
          outline: '2px solid #0066cc',
          outlineOffset: '2px'
        }
      }}
    >
      {loading && (
        <span 
          className="spinner" 
          aria-hidden="true"
          role="status"
        />
      )}
      <span className={loading ? 'sr-only' : ''}>
        {children}
      </span>
      {loading && (
        <span className="sr-only">Loading, please wait</span>
      )}
    </button>
  );
}

// Text scaling and responsive typography
function AccessibleTypography({ 
  children, 
  level = 1,
  size = 'base'
}: {
  children: React.ReactNode;
  level?: 1 | 2 | 3 | 4 | 5 | 6;
  size?: 'small' | 'base' | 'large';
}) {
  const Tag = `h${level}` as keyof JSX.IntrinsicElements;
  
  return (
    <Tag 
      className={`heading-${level} text-${size}`}
      style={{
        // Scalable units for text size (supports user zoom up to 200%)
        fontSize: size === 'large' ? '1.5rem' : 
                 size === 'small' ? '0.875rem' : '1rem',
        lineHeight: '1.5', // Minimum line height for readability
        // Adequate spacing between lines
        marginBottom: '0.5em'
      }}
    >
      {children}
    </Tag>
  );
}
```

### 2. Operable Interface
```typescript
import { useState, useRef, useEffect, useCallback } from 'react';

// Keyboard navigation for custom components
function AccessibleDropdown({ 
  label, 
  options, 
  value, 
  onChange 
}: {
  label: string;
  options: Array<{ value: string; label: string }>;
  value: string;
  onChange: (value: string) => void;
}) {
  const [isOpen, setIsOpen] = useState(false);
  const [focusedIndex, setFocusedIndex] = useState(-1);
  const buttonRef = useRef<HTMLButtonElement>(null);
  const listRef = useRef<HTMLUListElement>(null);
  const labelId = useId();
  const listboxId = useId();
  
  // Keyboard event handling
  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    switch (e.key) {
      case 'Enter':
      case ' ':
        e.preventDefault();
        if (!isOpen) {
          setIsOpen(true);
          setFocusedIndex(0);
        } else if (focusedIndex >= 0) {
          onChange(options[focusedIndex].value);
          setIsOpen(false);
          buttonRef.current?.focus();
        }
        break;
      
      case 'ArrowDown':
        e.preventDefault();
        if (!isOpen) {
          setIsOpen(true);
          setFocusedIndex(0);
        } else {
          setFocusedIndex(prev => 
            prev < options.length - 1 ? prev + 1 : 0
          );
        }
        break;
      
      case 'ArrowUp':
        e.preventDefault();
        if (!isOpen) {
          setIsOpen(true);
          setFocusedIndex(options.length - 1);
        } else {
          setFocusedIndex(prev => 
            prev > 0 ? prev - 1 : options.length - 1
          );
        }
        break;
      
      case 'Escape':
        e.preventDefault();
        setIsOpen(false);
        setFocusedIndex(-1);
        buttonRef.current?.focus();
        break;
      
      case 'Tab':
        setIsOpen(false);
        setFocusedIndex(-1);
        break;
    }
  }, [isOpen, focusedIndex, options, onChange]);
  
  // Click outside to close
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (listRef.current && !listRef.current.contains(event.target as Node) &&
          buttonRef.current && !buttonRef.current.contains(event.target as Node)) {
        setIsOpen(false);
        setFocusedIndex(-1);
      }
    };
    
    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      return () => document.removeEventListener('mousedown', handleClickOutside);
    }
  }, [isOpen]);
  
  const selectedOption = options.find(opt => opt.value === value);
  
  return (
    <div className="dropdown-container">
      <label id={labelId} className="dropdown-label">
        {label}
      </label>
      
      <button
        ref={buttonRef}
        className={`dropdown-button ${isOpen ? 'open' : ''}`}
        onClick={() => setIsOpen(!isOpen)}
        onKeyDown={handleKeyDown}
        aria-labelledby={labelId}
        aria-haspopup="listbox"
        aria-expanded={isOpen}
        aria-controls={isOpen ? listboxId : undefined}
      >
        {selectedOption?.label || 'Select an option'}
        <span 
          className="dropdown-arrow" 
          aria-hidden="true"
        >
          {isOpen ? '▲' : '▼'}
        </span>
      </button>
      
      {isOpen && (
        <ul
          ref={listRef}
          id={listboxId}
          className="dropdown-list"
          role="listbox"
          aria-labelledby={labelId}
          tabIndex={-1}
        >
          {options.map((option, index) => (
            <li
              key={option.value}
              className={`dropdown-option ${
                index === focusedIndex ? 'focused' : ''
              } ${option.value === value ? 'selected' : ''}`}
              role="option"
              aria-selected={option.value === value}
              onClick={() => {
                onChange(option.value);
                setIsOpen(false);
                buttonRef.current?.focus();
              }}
              onMouseEnter={() => setFocusedIndex(index)}
            >
              {option.label}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

// Focus management for modals and dialogs
function AccessibleModal({ 
  isOpen, 
  onClose, 
  title, 
  children 
}: {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
}) {
  const modalRef = useRef<HTMLDivElement>(null);
  const previousActiveElement = useRef<HTMLElement | null>(null);
  const titleId = useId();
  
  // Focus management
  useEffect(() => {
    if (isOpen) {
      // Store the currently focused element
      previousActiveElement.current = document.activeElement as HTMLElement;
      
      // Focus the modal
      modalRef.current?.focus();
      
      // Trap focus within modal
      const handleKeyDown = (e: KeyboardEvent) => {
        if (e.key === 'Escape') {
          onClose();
        } else if (e.key === 'Tab') {
          const focusableElements = modalRef.current?.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
          );
          
          if (focusableElements && focusableElements.length > 0) {
            const firstElement = focusableElements[0] as HTMLElement;
            const lastElement = focusableElements[focusableElements.length - 1] as HTMLElement;
            
            if (e.shiftKey && document.activeElement === firstElement) {
              e.preventDefault();
              lastElement.focus();
            } else if (!e.shiftKey && document.activeElement === lastElement) {
              e.preventDefault();
              firstElement.focus();
            }
          }
        }
      };
      
      document.addEventListener('keydown', handleKeyDown);
      
      return () => {
        document.removeEventListener('keydown', handleKeyDown);
        // Restore focus to previous element when modal closes
        if (previousActiveElement.current) {
          previousActiveElement.current.focus();
        }
      };
    }
  }, [isOpen, onClose]);
  
  if (!isOpen) return null;
  
  return (
    <div className="modal-overlay" onClick={onClose}>
      <div
        ref={modalRef}
        className="modal-content"
        role="dialog"
        aria-modal="true"
        aria-labelledby={titleId}
        tabIndex={-1}
        onClick={(e) => e.stopPropagation()}
      >
        <div className="modal-header">
          <h2 id={titleId} className="modal-title">
            {title}
          </h2>
          <button
            className="modal-close"
            onClick={onClose}
            aria-label="Close dialog"
          >
            ×
          </button>
        </div>
        
        <div className="modal-body">
          {children}
        </div>
      </div>
    </div>
  );
}
```

### 3. Understandable Content
```typescript
// Form validation with accessible error messages
function AccessibleForm() {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [submitted, setSubmitted] = useState(false);
  
  const emailId = useId();
  const passwordId = useId();
  const confirmPasswordId = useId();
  
  const validateForm = () => {
    const newErrors: Record<string, string> = {};
    
    // Email validation
    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }
    
    // Password validation
    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters long';
    }
    
    // Confirm password validation
    if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
    
    if (validateForm()) {
      // Handle successful submission
      console.log('Form submitted successfully');
    } else {
      // Focus first error field
      const firstErrorField = Object.keys(errors)[0];
      document.getElementById(firstErrorField)?.focus();
    }
  };
  
  return (
    <form onSubmit={handleSubmit} noValidate>
      <h1>Create Account</h1>
      
      {/* Email field */}
      <div className="form-group">
        <label htmlFor={emailId} className="required">
          Email Address
        </label>
        <input
          id={emailId}
          type="email"
          value={formData.email}
          onChange={(e) => setFormData(prev => ({ ...prev, email: e.target.value }))}
          className={errors.email ? 'error' : ''}
          aria-describedby={errors.email ? `${emailId}-error` : `${emailId}-help`}
          aria-invalid={!!errors.email}
          aria-required="true"
        />
        <div id={`${emailId}-help`} className="help-text">
          We'll use this email to send you account notifications
        </div>
        {errors.email && (
          <div 
            id={`${emailId}-error`} 
            className="error-message" 
            role="alert"
            aria-live="polite"
          >
            {errors.email}
          </div>
        )}
      </div>
      
      {/* Password field */}
      <div className="form-group">
        <label htmlFor={passwordId} className="required">
          Password
        </label>
        <input
          id={passwordId}
          type="password"
          value={formData.password}
          onChange={(e) => setFormData(prev => ({ ...prev, password: e.target.value }))}
          className={errors.password ? 'error' : ''}
          aria-describedby={errors.password ? `${passwordId}-error` : `${passwordId}-help`}
          aria-invalid={!!errors.password}
          aria-required="true"
        />
        <div id={`${passwordId}-help`} className="help-text">
          Must be at least 8 characters long
        </div>
        {errors.password && (
          <div 
            id={`${passwordId}-error`} 
            className="error-message" 
            role="alert"
            aria-live="polite"
          >
            {errors.password}
          </div>
        )}
      </div>
      
      {/* Confirm Password field */}
      <div className="form-group">
        <label htmlFor={confirmPasswordId} className="required">
          Confirm Password
        </label>
        <input
          id={confirmPasswordId}
          type="password"
          value={formData.confirmPassword}
          onChange={(e) => setFormData(prev => ({ ...prev, confirmPassword: e.target.value }))}
          className={errors.confirmPassword ? 'error' : ''}
          aria-describedby={errors.confirmPassword ? `${confirmPasswordId}-error` : undefined}
          aria-invalid={!!errors.confirmPassword}
          aria-required="true"
        />
        {errors.confirmPassword && (
          <div 
            id={`${confirmPasswordId}-error`} 
            className="error-message" 
            role="alert"
            aria-live="polite"
          >
            {errors.confirmPassword}
          </div>
        )}
      </div>
      
      <button type="submit" className="submit-button">
        Create Account
      </button>
      
      {submitted && Object.keys(errors).length > 0 && (
        <div className="form-summary-error" role="alert" aria-live="polite">
          Please correct the {Object.keys(errors).length} error(s) above to continue.
        </div>
      )}
    </form>
  );
}

// Progress indicators and status updates
function AccessibleProgressIndicator({ 
  currentStep, 
  totalSteps, 
  stepTitles 
}: {
  currentStep: number;
  totalSteps: number;
  stepTitles: string[];
}) {
  const progressPercentage = ((currentStep - 1) / (totalSteps - 1)) * 100;
  
  return (
    <div className="progress-container">
      <div className="progress-header">
        <h2 id="progress-title">Setup Progress</h2>
        <div 
          aria-live="polite" 
          aria-atomic="true"
        >
          Step {currentStep} of {totalSteps}: {stepTitles[currentStep - 1]}
        </div>
      </div>
      
      <div 
        className="progress-bar"
        role="progressbar"
        aria-labelledby="progress-title"
        aria-valuenow={currentStep}
        aria-valuemin={1}
        aria-valuemax={totalSteps}
        aria-valuetext={`Step ${currentStep} of ${totalSteps}: ${stepTitles[currentStep - 1]}`}
      >
        <div 
          className="progress-fill"
          style={{ width: `${progressPercentage}%` }}
        />
      </div>
      
      <ol className="step-list">
        {stepTitles.map((title, index) => {
          const stepNumber = index + 1;
          const isCompleted = stepNumber < currentStep;
          const isCurrent = stepNumber === currentStep;
          
          return (
            <li 
              key={stepNumber}
              className={`step ${
                isCompleted ? 'completed' : 
                isCurrent ? 'current' : 'pending'
              }`}
              aria-current={isCurrent ? 'step' : undefined}
            >
              <span className="step-number" aria-hidden="true">
                {isCompleted ? '✓' : stepNumber}
              </span>
              <span className="step-title">
                {title}
                <span className="sr-only">
                  {isCompleted ? ' (completed)' : 
                   isCurrent ? ' (current step)' : ' (pending)'}
                </span>
              </span>
            </li>
          );
        })}
      </ol>
    </div>
  );
}
```

### 4. Robust Implementation
```typescript
// Screen reader announcements and live regions
function useScreenReaderAnnouncement() {
  const [announcement, setAnnouncement] = useState('');
  const timeoutRef = useRef<NodeJS.Timeout>();
  
  const announce = useCallback((message: string, priority: 'polite' | 'assertive' = 'polite') => {
    // Clear previous timeout
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current);
    }
    
    // Set the announcement
    setAnnouncement(message);
    
    // Clear the announcement after it's been read
    timeoutRef.current = setTimeout(() => {
      setAnnouncement('');
    }, 1000);
  }, []);
  
  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, []);
  
  const AnnouncementRegion = () => (
    <div
      aria-live="polite"
      aria-atomic="true"
      className="sr-only"
      role="status"
    >
      {announcement}
    </div>
  );
  
  return { announce, AnnouncementRegion };
}

// Accessible data tables
function AccessibleDataTable({ 
  data, 
  columns, 
  caption 
}: {
  data: any[];
  columns: Array<{ key: string; label: string; sortable?: boolean }>;
  caption: string;
}) {
  const [sortConfig, setSortConfig] = useState<{
    key: string;
    direction: 'asc' | 'desc';
  } | null>(null);
  
  const { announce } = useScreenReaderAnnouncement();
  
  const sortedData = useMemo(() => {
    if (!sortConfig) return data;
    
    return [...data].sort((a, b) => {
      const aValue = a[sortConfig.key];
      const bValue = b[sortConfig.key];
      
      if (aValue < bValue) return sortConfig.direction === 'asc' ? -1 : 1;
      if (aValue > bValue) return sortConfig.direction === 'asc' ? 1 : -1;
      return 0;
    });
  }, [data, sortConfig]);
  
  const handleSort = (key: string) => {
    const direction = sortConfig?.key === key && sortConfig.direction === 'asc' 
      ? 'desc' 
      : 'asc';
    
    setSortConfig({ key, direction });
    
    const column = columns.find(col => col.key === key);
    announce(`Table sorted by ${column?.label} in ${direction}ending order`);
  };
  
  return (
    <div className="table-container">
      <table className="accessible-table">
        <caption className="table-caption">
          {caption}
          {sortConfig && (
            <span className="sr-only">
              , sorted by {columns.find(col => col.key === sortConfig.key)?.label} in {sortConfig.direction}ending order
            </span>
          )}
        </caption>
        
        <thead>
          <tr>
            {columns.map((column) => (
              <th
                key={column.key}
                scope="col"
                className={`table-header ${column.sortable ? 'sortable' : ''}`}
                {...(column.sortable && {
                  'aria-sort': sortConfig?.key === column.key 
                    ? sortConfig.direction === 'asc' ? 'ascending' : 'descending'
                    : 'none',
                  onClick: () => handleSort(column.key),
                  onKeyDown: (e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                      e.preventDefault();
                      handleSort(column.key);
                    }
                  },
                  tabIndex: 0,
                  role: 'button'
                })}
              >
                {column.label}
                {column.sortable && (
                  <span className="sort-indicator" aria-hidden="true">
                    {sortConfig?.key === column.key 
                      ? sortConfig.direction === 'asc' ? ' ↑' : ' ↓'
                      : ' ⇅'}
                  </span>
                )}
              </th>
            ))}
          </tr>
        </thead>
        
        <tbody>
          {sortedData.map((row, index) => (
            <tr key={index}>
              {columns.map((column) => (
                <td key={column.key} className="table-cell">
                  {row[column.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

// Accessible skip links and navigation
function AccessibleSkipLinks() {
  return (
    <div className="skip-links">
      <a href="#main-content" className="skip-link">
        Skip to main content
      </a>
      <a href="#navigation" className="skip-link">
        Skip to navigation
      </a>
      <a href="#search" className="skip-link">
        Skip to search
      </a>
    </div>
  );
}

// Landmark regions and page structure
function AccessiblePageLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="page-layout">
      <AccessibleSkipLinks />
      
      <header role="banner">
        <nav role="navigation" aria-label="Main navigation" id="navigation">
          {/* Navigation content */}
        </nav>
      </header>
      
      <main id="main-content" role="main" tabIndex={-1}>
        {children}
      </main>
      
      <aside role="complementary" aria-label="Sidebar">
        {/* Sidebar content */}
      </aside>
      
      <footer role="contentinfo">
        {/* Footer content */}
      </footer>
    </div>
  );
}
```

## Screen Reader Testing and Compatibility

### 1. Screen Reader Testing Utilities
```typescript
// Screen reader testing helpers
function useScreenReaderTesting() {
  const [isScreenReaderMode, setIsScreenReaderMode] = useState(false);
  
  useEffect(() => {
    // Detect if screen reader is likely active
    const assessScreenReader = () => {
      // Assess for common screen reader indicators
      const hasScreenReader = 
        navigator.userAgent.includes('NVDA') ||
        navigator.userAgent.includes('JAWS') ||
        navigator.userAgent.includes('Dragon') ||
        window.speechSynthesis?.getVoices().length > 0;
      
      setIsScreenReaderMode(hasScreenReader);
    };
    
    assessScreenReader();
    
    // Listen for screen reader events
    const handleVoicesChanged = () => assessScreenReader();
    if (window.speechSynthesis) {
      window.speechSynthesis.addEventListener('voiceschanged', handleVoicesChanged);
    }
    
    return () => {
      if (window.speechSynthesis) {
        window.speechSynthesis.removeEventListener('voiceschanged', handleVoicesChanged);
      }
    };
  }, []);
  
  return { isScreenReaderMode };
}

// Screen reader announcements for dynamic content
function DynamicContentAnnouncer({ 
  children,
  announceOnChange = true
}: {
  children: React.ReactNode;
  announceOnChange?: boolean;
}) {
  const [previousContent, setPreviousContent] = useState('');
  const contentRef = useRef<HTMLDivElement>(null);
  
  useEffect(() => {
    if (announceOnChange && contentRef.current) {
      const currentContent = contentRef.current.textContent || '';
      
      if (currentContent !== previousContent && previousContent !== '') {
        // Announce the change to screen readers
        const announcement = document.createElement('div');
        announcement.setAttribute('aria-live', 'polite');
        announcement.setAttribute('aria-atomic', 'true');
        announcement.className = 'sr-only';
        announcement.textContent = `Content updated: ${currentContent}`;
        
        document.body.appendChild(announcement);
        
        setTimeout(() => {
          document.body.removeChild(announcement);
        }, 1000);
      }
      
      setPreviousContent(currentContent);
    }
  }, [children, announceOnChange, previousContent]);
  
  return (
    <div ref={contentRef} aria-live="polite" aria-atomic="true">
      {children}
    </div>
  );
}
```

## Mobile Accessibility

### 1. Touch and Gesture Accessibility
```typescript
// Accessible touch interactions
function TouchAccessibleButton({ 
  children, 
  onPress,
  minTouchTarget = 44 // WCAG AA minimum
}: {
  children: React.ReactNode;
  onPress: () => void;
  minTouchTarget?: number;
}) {
  return (
    <button
      className="touch-accessible-button"
      onClick={onPress}
      style={{
        minWidth: `${minTouchTarget}px`,
        minHeight: `${minTouchTarget}px`,
        padding: '8px 16px',
        // Ensure WCAG 2.1 AA compliant 44px minimum spacing between touch targets
        margin: '4px'
      }}
    >
      {children}
    </button>
  );
}

// Accessible swipe gestures
function useAccessibleSwipe(
  elementRef: React.RefObject<HTMLElement>,
  onSwipe: (direction: 'left' | 'right' | 'up' | 'down') => void
) {
  useEffect(() => {
    const element = elementRef.current;
    if (!element) return;
    
    let startX = 0;
    let startY = 0;
    
    const handleTouchStart = (e: TouchEvent) => {
      startX = e.touches[0].clientX;
      startY = e.touches[0].clientY;
    };
    
    const handleTouchEnd = (e: TouchEvent) => {
      const endX = e.changedTouches[0].clientX;
      const endY = e.changedTouches[0].clientY;
      
      const deltaX = endX - startX;
      const deltaY = endY - startY;
      
      const minSwipeDistance = 50;
      
      if (Math.abs(deltaX) > Math.abs(deltaY)) {
        if (Math.abs(deltaX) > minSwipeDistance) {
          onSwipe(deltaX > 0 ? 'right' : 'left');
        }
      } else {
        if (Math.abs(deltaY) > minSwipeDistance) {
          onSwipe(deltaY > 0 ? 'down' : 'up');
        }
      }
    };
    
    // Also provide keyboard alternatives
    const handleKeyDown = (e: KeyboardEvent) => {
      switch (e.key) {
        case 'ArrowLeft':
          onSwipe('left');
          break;
        case 'ArrowRight':
          onSwipe('right');
          break;
        case 'ArrowUp':
          onSwipe('up');
          break;
        case 'ArrowDown':
          onSwipe('down');
          break;
      }
    };
    
    element.addEventListener('touchstart', handleTouchStart);
    element.addEventListener('touchend', handleTouchEnd);
    element.addEventListener('keydown', handleKeyDown);
    
    return () => {
      element.removeEventListener('touchstart', handleTouchStart);
      element.removeEventListener('touchend', handleTouchEnd);
      element.removeEventListener('keydown', handleKeyDown);
    };
  }, [elementRef, onSwipe]);
}
```

## Accessibility Testing and Validation

### 1. Automated Accessibility Testing
```typescript
// Accessibility testing utilities
function runAccessibilityAudit(element: HTMLElement) {
  const issues: Array<{
    type: 'error' | 'warning';
    rule: string;
    message: string;
    element: HTMLElement;
  }> = [];
  
  // Assess for missing alt text on images
  const images = element.querySelectorAll('img');
  images.forEach(img => {
    if (!img.hasAttribute('alt') && !img.hasAttribute('role')) {
      issues.push({
        type: 'error',
        rule: 'img-alt',
        message: 'Image missing alt attribute',
        element: img
      });
    }
  });
  
  // Assess for form labels
  const inputs = element.querySelectorAll('input, select, textarea');
  inputs.forEach(input => {
    const id = input.getAttribute('id');
    const ariaLabel = input.getAttribute('aria-label');
    const ariaLabelledby = input.getAttribute('aria-labelledby');
    
    if (!ariaLabel && !ariaLabelledby) {
      if (!id || !element.querySelector(`label[for="${id}"]`)) {
        issues.push({
          type: 'error',
          rule: 'label-missing',
          message: 'Form control missing label',
          element: input as HTMLElement
        });
      }
    }
  });
  
  // Assess for heading hierarchy
  const headings = Array.from(element.querySelectorAll('h1, h2, h3, h4, h5, h6'));
  for (let i = 1; i < headings.length; i++) {
    const currentLevel = parseInt(headings[i].tagName.charAt(1));
    const previousLevel = parseInt(headings[i - 1].tagName.charAt(1));
    
    if (currentLevel > previousLevel + 1) {
      issues.push({
        type: 'warning',
        rule: 'heading-hierarchy',
        message: `Heading level skipped from h${previousLevel} to h${currentLevel}`,
        element: headings[i] as HTMLElement
      });
    }
  }
  
  // Assess for color contrast (simplified evaluation)
  const assessColorContrast = (element: Element) => {
    const style = window.getComputedStyle(element);
    const backgroundColor = style.backgroundColor;
    const color = style.color;
    
    // This is a simplified assessment - in real implementation,
    // you'd use a proper color contrast calculation
    if (backgroundColor === 'white' && color === 'lightgray') {
      issues.push({
        type: 'error',
        rule: 'color-contrast',
        message: 'Insufficient color contrast',
        element: element as HTMLElement
      });
    }
  };
  
  element.querySelectorAll('*').forEach(assessColorContrast);
  
  return issues;
}

// React Testing Library accessibility utilities
import { render, screen } from '@testing-library/react';
import { axe, toHaveNoViolations } from 'jest-axe';

expect.extend(toHaveNoViolations);

// Accessibility test helper
export const renderWithA11yAssessment = async (component: React.ReactElement) => {
  const { container } = render(component);
  const results = await axe(container);
  expect(results).toHaveNoViolations();
  return { container };
};

// Custom accessibility matchers
export const accessibilityMatchers = {
  toBeAccessible: async (element: HTMLElement) => {
    const results = await axe(element);
    const pass = results.violations.length === 0;
    
    return {
      pass,
      message: () => 
        pass 
          ? 'Element is accessible'
          : `Accessibility violations found:\n${results.violations
              .map(v => `- ${v.description}`)
              .join('\n')}`
    };
  }
};
```

### 2. Manual Testing Checklist
```typescript
// Accessibility testing checklist component
function AccessibilityTestingChecklist({ 
  componentName 
}: { 
  componentName: string 
}) {
  const [checklist, setChecklist] = useState({
    keyboardNavigation: false,
    screenReaderCompatibility: false,
    colorContrast: false,
    focusManagement: false,
    errorHandling: false,
    mobileAccessibility: false,
    semanticMarkup: false
  });
  
  const handleChecklistUpdate = (item: keyof typeof checklist) => {
    setChecklist(prev => ({ ...prev, [item]: !prev[item] }));
  };
  
  const completionPercentage = Math.round(
    (Object.values(checklist).filter(Boolean).length / Object.keys(checklist).length) * 100
  );
  
  return (
    <div className="accessibility-checklist">
      <h3>Accessibility Testing Checklist for {componentName}</h3>
      <div className="progress-indicator">
        Progress: {completionPercentage}% complete
      </div>
      
      <ul className="checklist-items">
        <li>
          <label>
            <input
              type="checkbox"
              checked={checklist.keyboardNavigation}
              onChange={() => handleChecklistUpdate('keyboardNavigation')}
            />
            Keyboard Navigation: Can navigate through all interactive elements using Tab, Enter, Space, and arrow keys
          </label>
        </li>
        
        <li>
          <label>
            <input
              type="checkbox"
              checked={checklist.screenReaderCompatibility}
              onChange={() => handleChecklistUpdate('screenReaderCompatibility')}
            />
            Screen Reader: All content is announced with appropriate semantic markup and reading order
          </label>
        </li>
        
        <li>
          <label>
            <input
              type="checkbox"
              checked={checklist.colorContrast}
              onChange={() => handleChecklistUpdate('colorContrast')}
            />
            Color Contrast: All text meets WCAG AA contrast ratios (4.5:1 for normal text, 3:1 for large text)
          </label>
        </li>
        
        <li>
          <label>
            <input
              type="checkbox"
              checked={checklist.focusManagement}
              onChange={() => handleChecklistUpdate('focusManagement')}
            />
            Focus Management: Focus is managed according to WCAG 2.1 guidelines for modals, dynamic content, and state changes
          </label>
        </li>
        
        <li>
          <label>
            <input
              type="checkbox"
              checked={checklist.errorHandling}
              onChange={() => handleChecklistUpdate('errorHandling')}
            />
            Error Handling: Errors are announced to screen readers and provide clear instructions
          </label>
        </li>
        
        <li>
          <label>
            <input
              type="checkbox"
              checked={checklist.mobileAccessibility}
              onChange={() => handleChecklistUpdate('mobileAccessibility')}
            />
            Mobile Accessibility: Touch targets are at least 44px, gestures have keyboard alternatives
          </label>
        </li>
        
        <li>
          <label>
            <input
              type="checkbox"
              checked={checklist.semanticMarkup}
              onChange={() => handleChecklistUpdate('semanticMarkup')}
            />
            Semantic Markup: Uses proper HTML elements and ARIA attributes where needed
          </label>
        </li>
      </ul>
      
      {completionPercentage === 100 && (
        <div className="success-message" role="alert">
          ✅ All accessibility assessments complete! Component is ready for production.
        </div>
      )}
    </div>
  );
}
```

## Best Practices for Accessibility Specialists

### 1. Development Workflow Integration
- Run automated accessibility tests in CI/CD pipeline
- Include accessibility acceptance criteria in user stories
- Conduct regular accessibility audits with real users
- Maintain an accessibility component library
- Document accessibility patterns and anti-patterns

### 2. Testing Tools and Resources
- **Automated Testing**: axe-core, WAVE, Lighthouse accessibility audit
- **Screen Readers**: NVDA (Windows), VoiceOver (macOS), TalkBack (Android)
- **Browser Extensions**: axe DevTools, WAVE browser extension
- **Color Contrast**: Colour Contrast Analyser, WebAIM contrast checker
- **Keyboard Testing**: Physical testing with keyboard-only navigation

### 3. Common Accessibility Pitfalls
- Missing or non-descriptive alt text that fails to convey image purpose and context
- Poor keyboard navigation support
- Insufficient color contrast ratios
- Missing form labels or error messages
- Improper heading hierarchy
- Focus management issues in dynamic content
- Lack of screen reader announcements for status changes

## Context Usage Guidelines

**For AI Agents in Accessibility Specialist Role:**
1. Focus on WCAG 2.1 AA compliance and inclusive design principles
2. Include specific ARIA attributes and semantic HTML usage
3. Consider screen reader compatibility and keyboard navigation
4. Think about diverse user needs and assistive technologies
5. Provide testing strategies and validation methods

**Don't Include:**
- Basic component implementation details (use frontend-dev context)
- High-level design decisions (use architect context)
- Performance optimization techniques (use performance context)
- General development practices unrelated to accessibility

This context should guide accessibility implementation, testing, and validation to ensure React applications are usable by everyone, including users with disabilities.