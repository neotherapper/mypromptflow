# TypeScript Frontend Validator

## Purpose

Specialized AI agent validator for TypeScript frontend files (.ts/.tsx) with React-specific pattern validation, type safety checking, and component architecture validation.

## Activation Criteria

**File Patterns:**
- `src/**/*.ts` (TypeScript modules)
- `src/**/*.tsx` (React TypeScript components)
- `components/**/*.ts` 
- `components/**/*.tsx`
- `pages/**/*.tsx` (Next.js pages)
- `app/**/*.tsx` (Next.js App Router)

**Context Indicators:**
- React/Vue/Angular dependencies in package.json
- Frontend build tools (Vite, Webpack, Next.js config)
- Component directory structure presence
- UI library imports (MUI, Chakra, Tailwind)

## Validation Scope

### 1. TypeScript Type Safety
- **Type Annotations**: Proper type definitions for props, state, and functions
- **Interface Definitions**: Component prop interfaces and type exports
- **Generic Usage**: Correct generic type parameters for reusable components
- **Type Imports**: Proper type-only imports (`import type`)
- **Union Types**: Appropriate use of union types for component variants

### 2. React Component Architecture
- **Component Structure**: Functional components with proper TypeScript typing
- **Hook Usage**: Correct implementation of useState, useEffect, useCallback, useMemo
- **Custom Hooks**: Proper TypeScript typing for custom hook returns
- **Context Usage**: TypeScript-safe Context API implementation
- **Error Boundaries**: TypeScript error boundary implementations

### 3. Frontend Performance Patterns
- **React.memo**: Appropriate memoization for performance optimization
- **useCallback/useMemo**: Proper dependency arrays and optimization usage
- **Dynamic Imports**: Code splitting with proper TypeScript support
- **Bundle Optimization**: Import patterns for tree shaking

### 4. Accessibility and UI Standards
- **ARIA Attributes**: Proper accessibility attributes with TypeScript
- **Semantic HTML**: Correct HTML element usage in JSX
- **Keyboard Navigation**: Tab index and keyboard event handling
- **Screen Reader Support**: ARIA labels and descriptions

### 5. Security Considerations
- **XSS Prevention**: Proper data sanitization in JSX
- **Input Validation**: Client-side validation with TypeScript types
- **Secure API Calls**: Proper error handling and data validation
- **Content Security**: Safe rendering of dynamic content

## AI Agent Instructions

### Phase 1: File Discovery and Context Analysis

**AI Agent Execution Steps:**

1. **Identify TypeScript Files**: Use Glob tool with patterns `**/*.ts` and `**/*.tsx`
2. **Context Analysis**: Read package.json to identify frontend framework
3. **Project Structure Assessment**: Analyze directory structure for component organization
4. **Configuration Detection**: Check for tsconfig.json, vite.config.ts, next.config.js

### Phase 2: TypeScript Type Safety Validation

**For each .ts/.tsx file:**

1. **Read File Content**: Use Read tool to analyze TypeScript code
2. **Type Annotation Assessment**:
   ```typescript
   // Good examples to validate for:
   interface ButtonProps {
     variant: 'primary' | 'secondary' | 'danger';
     size?: 'sm' | 'md' | 'lg';
     onClick: (event: MouseEvent<HTMLButtonElement>) => void;
     children: ReactNode;
   }
   
   const Button: FC<ButtonProps> = ({ variant, size = 'md', onClick, children }) => {
     // Component implementation
   };
   ```

3. **Common Issues to Flag**:
   - Missing prop interfaces
   - `any` type usage without justification
   - Untyped event handlers
   - Missing return type annotations for complex functions
   - Implicit any in useState or useReducer

### Phase 3: React Component Architecture Validation

**Component Structure Assessment:**

1. **Hook Usage Validation**:
   ```typescript
   // Validate proper hook typing:
   const [state, setState] = useState<UserData | null>(null);
   const [loading, setLoading] = useState<boolean>(false);
   
   const handleSubmit = useCallback((data: FormData) => {
     // Proper callback typing
   }, [dependencies]);
   ```

2. **Custom Hook Analysis**:
   ```typescript
   // Check for proper custom hook patterns:
   interface UseApiResult<T> {
     data: T | null;
     loading: boolean;
     error: string | null;
   }
   
   function useApi<T>(url: string): UseApiResult<T> {
     // Hook implementation
   }
   ```

3. **Context Usage Verification**:
   ```typescript
   // Validate TypeScript Context patterns:
   interface ThemeContextType {
     theme: 'light' | 'dark';
     toggleTheme: () => void;
   }
   
   const ThemeContext = createContext<ThemeContextType | undefined>(undefined);
   ```

### Phase 4: Performance and Best Practices

**Performance Pattern Analysis:**

1. **Memoization Validation**:
   - Check React.memo usage for expensive components
   - Validate useCallback dependencies are correctly specified
   - Ensure useMemo is used appropriately for expensive calculations

2. **Import Optimization**:
   ```typescript
   // Validate efficient import patterns:
   import { Button } from '@/components/ui/Button'; // Good
   import * as Icons from 'lucide-react'; // Flag for review
   
   // Check for proper type-only imports:
   import type { User } from '@/types/User';
   ```

### Phase 5: Security and Accessibility Validation

**Security Assessment:**

1. **XSS Prevention**:
   ```typescript
   // Flag dangerous patterns:
   <div dangerouslySetInnerHTML={{ __html: userInput }} /> // Flag
   
   // Validate safe patterns:
   <div>{sanitizedContent}</div> // Good
   ```

2. **Input Validation**:
   ```typescript
   // Check for proper form validation:
   const handleSubmit = (data: FormData) => {
     if (!data.email || !isValidEmail(data.email)) {
       // Proper validation
     }
   };
   ```

**Accessibility Check:**

1. **ARIA Attributes**:
   ```typescript
   // Validate accessibility patterns:
   <button
     aria-label="Close dialog"
     aria-expanded={isOpen}
     onClick={handleClose}
   >
     <X aria-hidden="true" />
   </button>
   ```

## Validation Output Format

### Success Report Template

```yaml
typescript_frontend_validation:
  files_processed: [count]
  validation_time: "[duration]"
  
  type_safety_score: "[0-100]"
  type_safety_issues:
    - file: "src/components/Button.tsx"
      line: 15
      issue: "Missing prop interface for ButtonProps"
      severity: "medium"
      recommendation: "Define proper TypeScript interface for component props"
  
  component_architecture_score: "[0-100]"
  react_patterns_validated:
    - proper_hook_usage: true
    - custom_hooks_typed: true
    - context_implementation: true
  
  performance_score: "[0-100]"
  performance_optimizations:
    - memo_usage: "appropriate"
    - callback_optimization: "needs_review"
    - import_efficiency: "good"
  
  security_score: "[0-100]"
  security_issues: []
  
  accessibility_score: "[0-100]"
  accessibility_compliance:
    - aria_usage: "good"
    - semantic_html: "excellent"
    - keyboard_navigation: "needs_improvement"
  
  overall_score: "[0-100]"
  
  recommendations:
    - "Add TypeScript interfaces for all component props"
    - "Implement proper useCallback dependencies in UserForm component"
    - "Add ARIA labels for icon-only buttons"
    - "Consider React.memo for expensive list components"
  
  critical_issues:
    - count: 0
    - blocking_deployment: false
  
  next_steps:
    - "Review type safety recommendations"
    - "Implement suggested performance optimizations"
    - "Address accessibility improvements"
```

## Framework Integration

### AI Agent Instruction Design Excellence Compliance

**Concrete Specificity:**
- Explicit file patterns and validation criteria
- Specific TypeScript patterns to validate
- Clear React architecture requirements

**External Dependency Elimination:**
- Self-contained validation logic
- Embedded best practice examples
- No external TypeScript checker dependencies

**Immediate Actionability:**
- Step-by-step validation process
- Clear output format requirements
- Specific tool usage instructions (Read, Glob)

**Constitutional AI Compliance:**
- Ethical code quality assessment
- No biased framework preferences
- Constructive improvement recommendations

### Progressive Context Loading

**Base Context (150 tokens):**
- File pattern recognition
- Basic TypeScript validation criteria
- React component identification

**Conditional Context (300-450 tokens):**
- Framework-specific patterns (Next.js, Vite, CRA)
- UI library integrations (MUI, Chakra, Tailwind)
- Advanced TypeScript patterns (generics, utility types)

**Specialized Context (200-350 tokens):**
- Performance optimization patterns
- Accessibility validation rules
- Security best practices

## Quality Metrics

### Validation Effectiveness Targets

- **Type Safety Coverage**: ≥95% of TypeScript issues detected
- **React Pattern Recognition**: ≥90% of anti-patterns identified
- **Performance Assessment**: ≥85% of optimization opportunities flagged
- **Security Validation**: ≥99% of XSS vulnerabilities detected
- **Accessibility Compliance**: ≥90% of WCAG issues identified

### Performance Targets

- **Processing Speed**: ≤60 seconds for 50 TypeScript files
- **Memory Efficiency**: ≤100MB peak memory usage
- **Context Loading**: ≤30 seconds for framework detection
- **Report Generation**: ≤15 seconds for comprehensive output

### Constitutional AI Validation

- **Accuracy**: ≥95% correct issue identification
- **Completeness**: ≥90% coverage of validation scope
- **Consistency**: ≥95% repeatable results across runs
- **Responsibility**: Constructive recommendations only
- **Transparency**: Clear reasoning for all flagged issues

## Integration Notes

### Validator Registry Integration

```yaml
typescript-frontend-validator:
  location: "meta/validation/validators/file-type/typescript-frontend-validator.md"
  file_patterns: ["**/*.ts", "**/*.tsx"]
  specialization: "Frontend TypeScript and React component validation"
  dependencies: []
  parallel_safe: true
  estimated_processing_time: "45-60s for typical frontend codebase"
  quality_score: "pending_measurement"
  constitutional_ai_compliance: true
  framework_compliance_version: "1.0"
```

### Command Integration

This validator integrates with `/validate-pr` command through:
- Conditional activation based on TypeScript file detection
- Parallel execution with other file-type validators
- Result aggregation into comprehensive PR validation report
- Progressive context loading for efficiency optimization

### Future Enhancements

- **Framework-Specific Validation**: Enhanced patterns for Vue 3 Composition API, Angular Standalone Components
- **Advanced Type Analysis**: Complex generic type validation, conditional types assessment
- **Performance Profiling**: Integration with Lighthouse CI for performance impact analysis
- **Design System Integration**: Validation against design token usage and component library compliance