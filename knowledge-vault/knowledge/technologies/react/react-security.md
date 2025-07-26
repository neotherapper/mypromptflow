# React Security Context - For AI Agent Security Specialists

## Current React Security Landscape (2025-07-25)

**React Security Stack**
- **React Security Tools**: ESLint Security Plugin, React Security Scanner, OWASP ZAP React Extensions
- **Authentication Libraries**: Auth0 React SDK, Firebase Auth, NextAuth.js, React-OIDC-Context
- **Security Testing**: React Testing Library Security, Enzyme Security Testing, Jest Security Matchers
- **Static Analysis**: SonarQube React Rules, CodeQL React Queries, Semgrep React Rules

## React-Specific Security Vulnerabilities

### 1. Cross-Site Scripting (XSS) in React

```yaml
# React XSS vulnerability patterns
react_xss_vulnerabilities:
  dangerously_set_inner_html:
    vulnerability: "Direct HTML injection bypass React's XSS protection"
    example: |
      // VULNERABLE
      <div dangerouslySetInnerHTML={{__html: userInput}} />
    mitigation: |
      // SECURE - Use DOMPurify for sanitization
      import DOMPurify from 'dompurify';
      <div dangerouslySetInnerHTML={{
        __html: DOMPurify.sanitize(userInput)
      }} />
    
  jsx_injection:
    vulnerability: "Dynamic JSX creation from user input"
    example: |
      // VULNERABLE
      const Component = eval(`() => <div>${userInput}</div>`);
    mitigation: "Never use eval() or Function() with user input for JSX creation"
    
  href_javascript_protocol:
    vulnerability: "javascript: URLs in links and redirects"
    example: |
      // VULNERABLE
      <a href={`javascript:${userScript}`}>Click me</a>
    mitigation: |
      // SECURE - Validate and sanitize URLs
      const isValidUrl = (url) => {
        try {
          const parsed = new URL(url);
          return ['http:', 'https:', 'mailto:'].includes(parsed.protocol);
        } catch {
          return false;
        }
      };
```

### 2. Component Security Patterns

```yaml
# Secure React component patterns
secure_component_patterns:
  input_validation:
    pattern: "Validate all props and user inputs"
    implementation: |
      import PropTypes from 'prop-types';
      import { z } from 'zod';
      
      // Runtime validation with Zod
      const UserProfileSchema = z.object({
        name: z.string().min(1).max(100),
        email: z.string().email(),
        age: z.number().min(0).max(150)
      });
      
      function UserProfile({ user }) {
        const validatedUser = UserProfileSchema.parse(user);
        return <div>{validatedUser.name}</div>;
      }
      
  secure_refs:
    pattern: "Secure ref handling to prevent DOM manipulation"
    implementation: |
      // SECURE - Validate ref operations  
      const inputRef = useRef(null);
      
      const focusInput = useCallback(() => {
        if (inputRef.current && typeof inputRef.current.focus === 'function') {
          inputRef.current.focus();
        }
      }, []);
      
  conditional_rendering_security:
    pattern: "Secure conditional rendering to prevent information disclosure"
    implementation: |
      // SECURE - Explicit boolean conversion
      function SecretComponent({ user, showSecret }) {
        // Prevent truthy object rendering
        return Boolean(showSecret) && user?.isAdmin && (
          <div>Secret information</div>
        );
      }
```

### 3. State Management Security

```yaml
# Secure state management in React
state_security_patterns:
  sensitive_data_storage:
    vulnerability: "Storing sensitive data in component state"
    secure_approach: |
      // Avoid storing sensitive data in state
      const [sensitiveToken, setSensitiveToken] = useState(); // AVOID
      
      // Use secure storage or memory-only variables
      const tokenRef = useRef();
      
      // Or use secure storage libraries
      import { useSecureStorage } from 'react-secure-storage';
      const [data, setData] = useSecureStorage('key', initialValue);
      
  state_exposure_prevention:
    pattern: "Prevent state exposure through dev tools"
    implementation: |
      // Use React DevTools security configurations
      if (process.env.NODE_ENV === 'production') {
        // Disable React DevTools in production
        if (typeof window.__REACT_DEVTOOLS_GLOBAL_HOOK__ === 'object') {
          window.__REACT_DEVTOOLS_GLOBAL_HOOK__.onCommitFiberRoot = null;
          window.__REACT_DEVTOOLS_GLOBAL_HOOK__.onCommitFiberUnmount = null;
        }
      }
      
  immutable_state_updates:
    pattern: "Secure state updates preventing prototype pollution"
    implementation: |
      // SECURE - Use proper immutable updates
      const updateUser = useCallback((updates) => {
        setUser(prev => ({
          ...prev,
          ...Object.fromEntries(
            Object.entries(updates).filter(([key]) => 
              ['name', 'email', 'age'].includes(key)
            )
          )
        }));
      }, []);
```

## Authentication and Authorization Security

### 1. React Authentication Patterns

```yaml
# Secure React authentication implementations
react_auth_patterns:
  token_handling:
    secure_storage: |
      // Use httpOnly cookies for tokens when possible
      import { useCookies } from 'react-cookie';
      
      function useAuthToken() {
        const [cookies, setCookie, removeCookie] = useCookies(['authToken']);
        
        const setToken = (token) => {
          setCookie('authToken', token, {
            httpOnly: true,
            secure: true,
            sameSite: 'strict',
            maxAge: 3600 // 1 hour
          });
        };
        
        return { token: cookies.authToken, setToken, removeToken: () => removeCookie('authToken') };
      }
      
  protected_routes:
    pattern: "Secure route protection with proper loading states"
    implementation: |
      function ProtectedRoute({ children }) {
        const { user, loading, error } = useAuth();
        
        if (loading) return <LoadingSpinner />;
        if (error) return <ErrorComponent error={error} />;
        if (!user) return <Navigate to="/login" replace />;
        
        return children;
      }
      
  permission_based_rendering:
    pattern: "Component-level permission verification"
    implementation: |
      function usePermission(requiredPermission) {
        const { user } = useAuth();
        return user?.permissions?.includes(requiredPermission) ?? false;
      }
      
      function AdminPanel() {
        const canViewAdmin = usePermission('admin.view');
        
        if (!canViewAdmin) {
          return <div>Access Denied</div>;
        }
        
        return <div>Admin content</div>;
      }
```

### 2. OAuth and Social Login Security

```yaml
# Secure OAuth implementation in React
oauth_security:
  csrf_protection:
    pattern: "CSRF protection for OAuth flows"
    implementation: |
      function useOAuthFlow() {
        const [state] = useState(() => crypto.randomUUID());
        
        const initiateLogin = useCallback((provider) => {
          // Store state in sessionStorage for CSRF protection
          sessionStorage.setItem('oauth_state', state);
          
          const authUrl = new URL(`/auth/${provider}`);
          authUrl.searchParams.set('state', state);
          authUrl.searchParams.set('redirect_uri', window.location.origin + '/callback');
          
          window.location.href = authUrl.toString();
        }, [state]);
        
        return { initiateLogin };
      }
      
  callback_validation:
    pattern: "Secure OAuth callback handling"
    implementation: |
      function OAuthCallback() {
        const location = useLocation();
        const navigate = useNavigate();
        
        useEffect(() => {
          const urlParams = new URLSearchParams(location.search);
          const returnedState = urlParams.get('state');
          const storedState = sessionStorage.getItem('oauth_state');
          
          if (!returnedState || returnedState !== storedState) {
            console.error('OAuth state mismatch - possible CSRF attack');
            navigate('/login', { replace: true });
            return;
          }
          
          // Clear stored state
          sessionStorage.removeItem('oauth_state');
          
          // Process OAuth callback securely
          processOAuthCallback(urlParams);
        }, [location, navigate]);
        
        return <div>Processing login...</div>;
      }
```

## React Security Testing

### 1. Component Security Testing

```yaml
# Security testing patterns for React components
component_security_testing:
  xss_testing:
    pattern: "Test components against XSS vulnerabilities"
    implementation: |
      import { render, screen } from '@testing-library/react';
      import userEvent from '@testing-library/user-event';
      
      describe('UserProfile XSS Protection', () => {
        test('should not render script tags from user input', () => {
          const maliciousInput = '<script>alert("XSS")</script>';
          render(<UserProfile name={maliciousInput} />);
          
          // Should not find script element
          expect(document.querySelector('script')).toBeNull();
          
          // Should escape or sanitize the content
          expect(screen.queryByText(maliciousInput)).toBeNull();
        });
        
        test('should sanitize dangerouslySetInnerHTML content', () => {
          const maliciousHTML = '<img src="x" onerror="alert(1)">';
          render(<ContentDisplay html={maliciousHTML} />);
          
          const img = document.querySelector('img');
          expect(img?.getAttribute('onerror')).toBeNull();
        });
      });
      
  authentication_testing:
    pattern: "Test authentication flows and edge cases"
    implementation: |
      describe('Authentication Security', () => {
        test('should redirect unauthenticated users', () => {
          render(
            <MemoryRouter initialEntries={['/protected']}>
              <ProtectedRoute>
                <SecretComponent />
              </ProtectedRoute>
            </MemoryRouter>
          );
          
          expect(screen.queryByText('Secret information')).toBeNull();
        });
        
        test('should not expose sensitive data in DOM', () => {
          const sensitiveData = { token: 'secret123', apiKey: 'key456' };
          render(<UserDashboard user={sensitiveData} />);
          
          // Check that sensitive data is not in DOM
          expect(document.body.innerHTML).not.toContain('secret123');
          expect(document.body.innerHTML).not.toContain('key456');
        });
      });
```

### 2. Security Integration Testing

```yaml
# Integration testing for React security
security_integration_testing:
  api_security_testing:
    pattern: "Test API integration security"
    implementation: |
      import { rest } from 'msw';
      import { setupServer } from 'msw/node';
      
      const server = setupServer(
        rest.get('/api/user', (req, res, ctx) => {
          const authHeader = req.headers.get('Authorization');
          
          if (!authHeader || !authHeader.startsWith('Bearer ')) {
            return res(ctx.status(401), ctx.json({ error: 'Unauthorized' }));
          }
          
          return res(ctx.json({ user: { id: 1, name: 'Test User' } }));
        })
      );
      
      describe('API Security Integration', () => {
        test('should include auth headers in requests', async () => {
          render(<UserProfile userId={1} />);
          
          await waitFor(() => {
            expect(screen.getByText('Test User')).toBeInTheDocument();
          });
        });
        
        test('should handle auth failures gracefully', async () => {
          // Test with invalid token
          render(<UserProfile userId={1} token="invalid" />);
          
          await waitFor(() => {
            expect(screen.getByText('Please log in')).toBeInTheDocument();
          });
        });
      });
```

## React Security Best Practices

### 1. Development Security Guidelines

- **Input Validation**: Always validate and sanitize user inputs at component boundaries
- **XSS Prevention**: Use React's built-in XSS protection; avoid dangerouslySetInnerHTML without sanitization
- **Authentication State**: Implement proper loading states and error handling for auth flows
- **Permission Verification**: Perform authorization verification at both route and component levels
- **Sensitive Data**: Never store sensitive data in component state or localStorage
- **HTTPS Enforcement**: Ensure all authentication and sensitive operations use HTTPS

### 2. Security Testing Guidelines

- **Component Testing**: Test components with malicious inputs and edge cases
- **Integration Testing**: Validate API security and authentication flows
- **E2E Security Testing**: Test complete user journeys including authentication
- **Static Analysis**: Use ESLint security rules and static analysis tools
- **Dependency Scanning**: Regular security audits of React dependencies
- **Runtime Protection**: Implement CSP headers and security monitoring

### 3. Deployment Security

- **Build Security**: Secure CI/CD pipelines and build environments
- **Asset Security**: Implement proper CSP headers and resource integrity verification
- **Environment Variables**: Secure handling of environment variables and secrets
- **Error Handling**: Prevent information disclosure through error messages
- **Monitoring**: Implement security monitoring and incident response

## Context Usage Guidelines

**For AI Agents in Security Specialist Role:**
1. Focus on React-specific security vulnerabilities and mitigation strategies
2. Emphasize secure coding patterns and authentication implementations
3. Validate security testing approaches and integration patterns
4. Consider both client-side and server-side security implications
5. Stay current with React security best practices and emerging threats

**Don't Include:**
- General web security concepts (use general security contexts)
- Backend-specific security patterns (use backend security contexts)  
- Infrastructure security details (use infrastructure security contexts)
- Basic React concepts (use React development contexts)

This context should guide React-specific security analysis, vulnerability assessment, and secure development practices for React applications.