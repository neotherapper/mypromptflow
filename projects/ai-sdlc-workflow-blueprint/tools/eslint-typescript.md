# ESLint + TypeScript - Code Quality & Type Safety

## Overview

ESLint with TypeScript integration provides comprehensive code quality enforcement and type safety for the maritime insurance application. This combination ensures consistent code style, catches potential bugs early, and maintains high code quality standards across the development team.

## Key Benefits

### Code Quality Enforcement
- **Consistent code style** across all team members
- **Early bug detection** through static analysis
- **Best practices enforcement** for React and TypeScript
- **Automated code quality checks** in CI/CD pipeline

### Type Safety
- **Static type checking** to prevent runtime errors
- **Interface validation** for API responses and component props
- **Strict type enforcement** for maritime insurance domain models
- **IDE integration** for real-time feedback

## Configuration

### ESLint Configuration

```javascript
// .eslintrc.js
module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  extends: [
    'eslint:recommended',
    '@typescript-eslint/recommended',
    '@typescript-eslint/recommended-requiring-type-checking',
    'plugin:react/recommended',
    'plugin:react-hooks/recommended',
    'plugin:jsx-a11y/recommended',
    'plugin:import/recommended',
    'plugin:import/typescript',
    'prettier', // Must be last to override other configs
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaFeatures: {
      jsx: true,
    },
    ecmaVersion: 'latest',
    sourceType: 'module',
    project: './tsconfig.json',
    tsconfigRootDir: __dirname,
  },
  plugins: [
    'react',
    'react-hooks',
    '@typescript-eslint',
    'jsx-a11y',
    'import',
  ],
  rules: {
    // TypeScript-specific rules
    '@typescript-eslint/no-unused-vars': 'error',
    '@typescript-eslint/no-explicit-any': 'warn',
    '@typescript-eslint/explicit-function-return-type': 'warn',
    '@typescript-eslint/no-unsafe-assignment': 'error',
    '@typescript-eslint/no-unsafe-member-access': 'error',
    '@typescript-eslint/no-unsafe-call': 'error',
    '@typescript-eslint/no-unsafe-return': 'error',
    '@typescript-eslint/prefer-nullish-coalescing': 'error',
    '@typescript-eslint/prefer-optional-chain': 'error',
    '@typescript-eslint/no-floating-promises': 'error',
    '@typescript-eslint/no-misused-promises': 'error',
    
    // React-specific rules
    'react/react-in-jsx-scope': 'off', // Not needed in React 17+
    'react/prop-types': 'off', // Using TypeScript for prop validation
    'react/jsx-uses-react': 'off',
    'react/jsx-uses-vars': 'error',
    'react/jsx-key': 'error',
    'react/jsx-no-duplicate-props': 'error',
    'react/jsx-no-undef': 'error',
    'react/jsx-pascal-case': 'error',
    'react/no-deprecated': 'error',
    'react/no-direct-mutation-state': 'error',
    'react/no-unused-state': 'error',
    'react/prefer-stateless-function': 'warn',
    
    // React Hooks rules
    'react-hooks/rules-of-hooks': 'error',
    'react-hooks/exhaustive-deps': 'warn',
    
    // Accessibility rules
    'jsx-a11y/alt-text': 'error',
    'jsx-a11y/anchor-has-content': 'error',
    'jsx-a11y/aria-props': 'error',
    'jsx-a11y/aria-proptypes': 'error',
    'jsx-a11y/aria-unsupported-elements': 'error',
    'jsx-a11y/click-events-have-key-events': 'error',
    'jsx-a11y/heading-has-content': 'error',
    'jsx-a11y/label-has-associated-control': 'error',
    'jsx-a11y/no-redundant-roles': 'error',
    
    // Import rules
    'import/order': [
      'error',
      {
        groups: [
          'builtin',
          'external',
          'internal',
          'parent',
          'sibling',
          'index',
        ],
        'newlines-between': 'always',
        alphabetize: {
          order: 'asc',
          caseInsensitive: true,
        },
      },
    ],
    'import/no-duplicates': 'error',
    'import/no-unresolved': 'error',
    'import/no-cycle': 'error',
    
    // General code quality rules
    'no-console': process.env.NODE_ENV === 'production' ? 'error' : 'warn',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'warn',
    'no-alert': 'error',
    'no-eval': 'error',
    'no-implied-eval': 'error',
    'no-new-func': 'error',
    'no-script-url': 'error',
    'no-sequences': 'error',
    'no-throw-literal': 'error',
    'no-useless-concat': 'error',
    'no-void': 'error',
    'prefer-const': 'error',
    'prefer-template': 'error',
    'eqeqeq': ['error', 'always'],
    'curly': ['error', 'all'],
  },
  settings: {
    react: {
      version: 'detect',
    },
    'import/resolver': {
      typescript: {
        alwaysTryTypes: true,
        project: './tsconfig.json',
      },
    },
  },
  overrides: [
    {
      files: ['*.test.ts', '*.test.tsx', '*.spec.ts', '*.spec.tsx'],
      env: {
        jest: true,
      },
      extends: [
        'plugin:testing-library/react',
        'plugin:jest-dom/recommended',
      ],
      rules: {
        '@typescript-eslint/no-unsafe-assignment': 'off',
        '@typescript-eslint/no-unsafe-member-access': 'off',
        '@typescript-eslint/no-unsafe-call': 'off',
        'testing-library/no-render-in-setup': 'error',
        'testing-library/no-wait-for-empty-callback': 'error',
        'testing-library/prefer-screen-queries': 'error',
        'testing-library/render-result-naming-convention': 'error',
      },
    },
    {
      files: ['*.stories.ts', '*.stories.tsx'],
      rules: {
        'import/no-anonymous-default-export': 'off',
        '@typescript-eslint/no-unsafe-assignment': 'off',
      },
    },
  ],
};
```

### TypeScript Configuration

```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["DOM", "DOM.Iterable", "ES2022"],
    "allowJs": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noFallthroughCasesInSwitch": true,
    "module": "ESNext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "incremental": true,
    "baseUrl": "./src",
    "paths": {
      "@/*": ["*"],
      "@/components/*": ["components/*"],
      "@/services/*": ["services/*"],
      "@/types/*": ["types/*"],
      "@/utils/*": ["utils/*"],
      "@/hooks/*": ["hooks/*"],
      "@/contexts/*": ["contexts/*"],
      "@/test/*": ["test/*"]
    },
    
    // Strict type checking options
    "noImplicitAny": true,
    "noImplicitReturns": true,
    "noImplicitThis": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true,
    "noUncheckedIndexedAccess": true,
    
    // Additional checks
    "noEmitOnError": true,
    "useDefineForClassFields": true,
    "experimentalDecorators": true,
    "emitDecoratorMetadata": true
  },
  "include": [
    "src/**/*",
    "src/**/*.json",
    "vite.config.ts",
    "vitest.config.ts"
  ],
  "exclude": [
    "node_modules",
    "dist",
    "build",
    "coverage"
  ],
  "ts-node": {
    "esm": true
  }
}
```

## Maritime Insurance Type Definitions

### Core Domain Types

```typescript
// src/types/maritime-insurance.ts
export interface Vessel {
  readonly id: VesselId;
  readonly name: string;
  readonly type: VesselType;
  readonly tonnage: number;
  readonly value: Money;
  readonly flag: CountryCode;
  readonly yearBuilt: number;
  readonly imo: IMONumber;
  readonly classification: ClassificationSociety;
  readonly certificates: VesselCertificate[];
}

export interface Fleet {
  readonly id: FleetId;
  readonly name: string;
  readonly type: FleetType;
  readonly vessels: readonly Vessel[];
  readonly owner: FleetOwner;
  readonly operationalRoutes: readonly Route[];
  readonly totalValue: Money;
  readonly riskProfile: RiskProfile;
}

export interface Quote {
  readonly id: QuoteId;
  readonly fleetId: FleetId;
  readonly premium: Money;
  readonly coverage: Money;
  readonly deductible: Money;
  readonly validUntil: Date;
  readonly coverageTypes: readonly CoverageType[];
  readonly exclusions: readonly Exclusion[];
  readonly conditions: readonly PolicyCondition[];
  readonly riskFactors: readonly RiskFactor[];
}

export interface BrokerResponse {
  readonly broker: BrokerInfo;
  readonly quote: Quote;
  readonly responseTime: number;
  readonly confidence: number;
  readonly additionalNotes?: string;
}

// Type guards for runtime validation
export function isVessel(obj: unknown): obj is Vessel {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    'id' in obj &&
    'name' in obj &&
    'type' in obj &&
    'tonnage' in obj &&
    'value' in obj &&
    'flag' in obj &&
    'yearBuilt' in obj
  );
}

export function isFleet(obj: unknown): obj is Fleet {
  return (
    typeof obj === 'object' &&
    obj !== null &&
    'id' in obj &&
    'name' in obj &&
    'type' in obj &&
    'vessels' in obj &&
    Array.isArray((obj as Fleet).vessels) &&
    (obj as Fleet).vessels.every(isVessel)
  );
}

// Branded types for type safety
export type VesselId = string & { readonly __brand: 'VesselId' };
export type FleetId = string & { readonly __brand: 'FleetId' };
export type QuoteId = string & { readonly __brand: 'QuoteId' };
export type IMONumber = string & { readonly __brand: 'IMONumber' };
export type Money = number & { readonly __brand: 'Money' };
export type CountryCode = string & { readonly __brand: 'CountryCode' };

// Factory functions for branded types
export function createVesselId(id: string): VesselId {
  if (!/^vessel-\d+$/.test(id)) {
    throw new Error(`Invalid vessel ID format: ${id}`);
  }
  return id as VesselId;
}

export function createFleetId(id: string): FleetId {
  if (!/^fleet-\d+$/.test(id)) {
    throw new Error(`Invalid fleet ID format: ${id}`);
  }
  return id as FleetId;
}

export function createMoney(amount: number): Money {
  if (amount < 0) {
    throw new Error('Money amount cannot be negative');
  }
  return amount as Money;
}

// Utility types
export type VesselType = 'cargo' | 'tanker' | 'container' | 'bulk' | 'passenger';
export type FleetType = 'cargo' | 'tanker' | 'container' | 'mixed';
export type CoverageType = 'hull' | 'cargo' | 'liability' | 'war' | 'piracy';
export type RiskLevel = 'low' | 'medium' | 'high' | 'extreme';
export type ClassificationSociety = 'ABS' | 'DNV' | 'LR' | 'BV' | 'CCS' | 'NK' | 'RINA';
```

### API Response Types

```typescript
// src/types/api.ts
export interface ApiResponse<T> {
  readonly data: T;
  readonly status: 'success' | 'error';
  readonly message?: string;
  readonly timestamp: string;
}

export interface PaginatedResponse<T> {
  readonly data: readonly T[];
  readonly pagination: {
    readonly page: number;
    readonly limit: number;
    readonly total: number;
    readonly totalPages: number;
  };
}

export interface ErrorResponse {
  readonly error: {
    readonly code: string;
    readonly message: string;
    readonly details?: Record<string, unknown>;
  };
  readonly status: 'error';
  readonly timestamp: string;
}

// API endpoint types
export interface FleetEndpoints {
  readonly getFleets: () => Promise<ApiResponse<readonly Fleet[]>>;
  readonly getFleet: (id: FleetId) => Promise<ApiResponse<Fleet>>;
  readonly createFleet: (fleet: Omit<Fleet, 'id'>) => Promise<ApiResponse<Fleet>>;
  readonly updateFleet: (id: FleetId, fleet: Partial<Fleet>) => Promise<ApiResponse<Fleet>>;
  readonly deleteFleet: (id: FleetId) => Promise<ApiResponse<void>>;
}

export interface QuoteEndpoints {
  readonly generateQuote: (request: QuoteRequest) => Promise<ApiResponse<Quote>>;
  readonly getQuote: (id: QuoteId) => Promise<ApiResponse<Quote>>;
  readonly compareQuotes: (ids: readonly QuoteId[]) => Promise<ApiResponse<QuoteComparison>>;
}
```

## Code Quality Tools Integration

### SonarLint Integration

```json
// .vscode/settings.json
{
  "sonarlint.rules": {
    "typescript:S6571": {
      "level": "on"
    },
    "typescript:S6572": {
      "level": "on"
    },
    "typescript:S6606": {
      "level": "on"
    }
  },
  "sonarlint.connectedMode.connections.sonarcloud": {
    "organizationKey": "your-org",
    "token": "your-token"
  }
}
```

### DeepSource Configuration

```yaml
# .deepsource.toml
version = 1

[[analyzers]]
name = "javascript"
enabled = true

  [analyzers.meta]
  plugins = ["react"]
  dialect = "typescript"

[[analyzers]]
name = "test-coverage"
enabled = true
```

### Code Quality Utilities

```typescript
// src/utils/code-quality.ts
export function assertNever(value: never): never {
  throw new Error(`Unexpected value: ${JSON.stringify(value)}`);
}

export function exhaustiveCheck<T extends Record<string, unknown>>(
  value: T,
  cases: Record<keyof T, unknown>
): void {
  const missingCases = Object.keys(value).filter(key => !(key in cases));
  if (missingCases.length > 0) {
    throw new Error(`Missing cases for: ${missingCases.join(', ')}`);
  }
}

// Type-safe error handling
export class MaritimeInsuranceError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly context?: Record<string, unknown>
  ) {
    super(message);
    this.name = 'MaritimeInsuranceError';
  }
}

export class FleetValidationError extends MaritimeInsuranceError {
  constructor(message: string, public readonly fleetId: FleetId) {
    super(message, 'FLEET_VALIDATION_ERROR', { fleetId });
  }
}

export class QuoteGenerationError extends MaritimeInsuranceError {
  constructor(message: string, public readonly quoteRequest: QuoteRequest) {
    super(message, 'QUOTE_GENERATION_ERROR', { quoteRequest });
  }
}
```

## AI-Assisted Code Quality Tools

### GitHub Copilot Integration

```json
// .vscode/settings.json
{
  "github.copilot.enable": {
    "*": true,
    "yaml": true,
    "plaintext": false,
    "markdown": true,
    "scminput": false
  },
  "github.copilot.advanced": {
    "inlineSuggest.enable": true,
    "length": "medium"
  }
}
```

### CodeClimate Configuration

```yaml
# .codeclimate.yml
version: "2"
checks:
  argument-count:
    config:
      threshold: 4
  complex-logic:
    config:
      threshold: 4
  file-lines:
    config:
      threshold: 250
  method-complexity:
    config:
      threshold: 5
  method-count:
    config:
      threshold: 20
  method-lines:
    config:
      threshold: 25
  nested-control-flow:
    config:
      threshold: 4
  return-statements:
    config:
      threshold: 4

plugins:
  eslint:
    enabled: true
    channel: "eslint-8"
    config:
      config: ".eslintrc.js"
  nodesecurity:
    enabled: true
  fixme:
    enabled: true

exclude_patterns:
  - "config/"
  - "db/"
  - "dist/"
  - "features/"
  - "**/node_modules/"
  - "script/"
  - "**/vendor/"
  - "**/*.d.ts"
  - "**/*.test.ts"
  - "**/*.spec.ts"
```

### Automated Code Quality Scripts

```typescript
// scripts/code-quality-check.ts
import { ESLint } from 'eslint';
import * as fs from 'fs/promises';
import * as path from 'path';

interface QualityReport {
  file: string;
  errors: number;
  warnings: number;
  fixableErrors: number;
  fixableWarnings: number;
}

export async function runCodeQualityAnalysis(): Promise<void> {
  const eslint = new ESLint({
    configFile: '.eslintrc.js',
    fix: false, // Don't auto-fix during analysis
  });
  
  // Get all TypeScript files
  const results = await eslint.lintFiles(['src/**/*.ts', 'src/**/*.tsx']);
  
  const reports: QualityReport[] = [];
  let totalErrors = 0;
  let totalWarnings = 0;
  
  for (const result of results) {
    if (result.errorCount > 0 || result.warningCount > 0) {
      reports.push({
        file: result.filePath,
        errors: result.errorCount,
        warnings: result.warningCount,
        fixableErrors: result.fixableErrorCount,
        fixableWarnings: result.fixableWarningCount,
      });
      
      totalErrors += result.errorCount;
      totalWarnings += result.warningCount;
    }
  }
  
  // Generate report
  const report = {
    timestamp: new Date().toISOString(),
    summary: {
      totalFiles: results.length,
      filesWithIssues: reports.length,
      totalErrors,
      totalWarnings,
    },
    files: reports,
  };
  
  // Save report
  await fs.writeFile(
    path.join(process.cwd(), 'code-quality-report.json'),
    JSON.stringify(report, null, 2)
  );
  
  // Format and display results
  const formatter = await eslint.loadFormatter('stylish');
  const resultText = formatter.format(results);
  console.log(resultText);
  
  // Exit with error if issues found
  if (totalErrors > 0) {
    process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  runCodeQualityAnalysis().catch(console.error);
}
```

## Additional Code Quality Tools

### Prettier Integration

```javascript
// .prettierrc.js
module.exports = {
  semi: true,
  trailingComma: 'es5',
  singleQuote: true,
  printWidth: 80,
  tabWidth: 2,
  useTabs: false,
  arrowParens: 'avoid',
  endOfLine: 'lf',
};
```

### Husky Pre-commit Hooks

```json
// package.json
{
  "scripts": {
    "lint": "eslint src --ext .ts,.tsx",
    "lint:fix": "eslint src --ext .ts,.tsx --fix",
    "type-check": "tsc --noEmit",
    "format": "prettier --write \"src/**/*.{ts,tsx,js,jsx,json,css,md}\"",
    "prepare": "husky install"
  },
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ],
    "*.{js,jsx,json,css,md}": [
      "prettier --write"
    ]
  }
}
```

```bash
# .husky/pre-commit
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

npx lint-staged
npm run type-check
```

### TypeScript Strict Mode Benefits

```typescript
// Example of strict mode catching errors
// Without strict mode, this would compile:
function processVessel(vessel: Vessel | null) {
  // Error: Object is possibly 'null'
  console.log(vessel.name); // ❌ Caught by strict mode
  
  // Correct approach:
  if (vessel) {
    console.log(vessel.name); // ✅ Type-safe
  }
}

// No implicit any
function calculatePremium(data) { // ❌ Error: Parameter 'data' implicitly has an 'any' type
  return data.value * 0.02;
}

// Correct approach:
function calculatePremium(data: { value: number }): number { // ✅
  return data.value * 0.02;
}
```

## Team Integration

### Development Team Usage

#### Head of Engineering
- **Code quality standards**: Set and enforce team-wide quality standards
- **CI/CD integration**: Ensure quality checks run in deployment pipeline
- **Performance monitoring**: Track code quality metrics and improvements

#### Lead Frontend Developer
- **React/TypeScript best practices**: Implement and maintain frontend quality standards
- **Component type safety**: Ensure components have proper TypeScript definitions
- **UI/UX code quality**: Maintain consistent styling and interaction patterns

#### Lead Backend Developer
- **API type safety**: Ensure API responses match TypeScript definitions
- **Data validation**: Implement proper input validation and error handling
- **Service layer quality**: Maintain clean service architecture

#### UI/UX Engineer
- **Accessibility compliance**: Ensure code meets accessibility standards
- **Design system consistency**: Maintain consistent styling and components
- **Visual code quality**: Ensure UI components are properly typed and documented

## Package Configuration

### Required Dependencies

```json
// package.json
{
  "devDependencies": {
    "@typescript-eslint/eslint-plugin": "^6.19.0",
    "@typescript-eslint/parser": "^6.19.0",
    "eslint": "^8.56.0",
    "eslint-config-prettier": "^9.1.0",
    "eslint-import-resolver-typescript": "^3.6.1",
    "eslint-plugin-import": "^2.29.1",
    "eslint-plugin-jest": "^27.6.3",
    "eslint-plugin-jest-dom": "^5.1.0",
    "eslint-plugin-jsx-a11y": "^6.8.0",
    "eslint-plugin-react": "^7.33.2",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-testing-library": "^6.2.0",
    "husky": "^8.0.3",
    "lint-staged": "^15.2.0",
    "prettier": "^3.2.4",
    "typescript": "^5.3.3"
  }
}
```

### npm Scripts

```json
{
  "scripts": {
    "lint": "eslint . --ext .ts,.tsx,.js,.jsx",
    "lint:fix": "eslint . --ext .ts,.tsx,.js,.jsx --fix",
    "lint:ci": "eslint . --ext .ts,.tsx,.js,.jsx --format json --output-file eslint-report.json",
    "type-check": "tsc --noEmit",
    "type-check:watch": "tsc --noEmit --watch",
    "format": "prettier --write \"**/*.{ts,tsx,js,jsx,json,css,scss,md}\"",
    "format:check": "prettier --check \"**/*.{ts,tsx,js,jsx,json,css,scss,md}\"",
    "quality": "npm run lint && npm run type-check && npm run format:check",
    "quality:fix": "npm run lint:fix && npm run format",
    "prepare": "husky install"
  }
}
```

## Best Practices

### TypeScript Usage
- **Strict type checking**: Use strict mode for maximum type safety
- **Branded types**: Use branded types for domain-specific values
- **Type guards**: Implement runtime type validation
- **Avoid any**: Use specific types instead of any

### Code Organization
- **Consistent imports**: Use absolute imports with path mapping
- **Proper file structure**: Organize files by feature and type
- **Clear naming**: Use descriptive names for variables and functions
- **Documentation**: Add JSDoc comments for complex functions

### Error Handling
- **Custom error types**: Create domain-specific error classes
- **Proper error propagation**: Handle errors at appropriate levels
- **Type-safe error handling**: Use Result types for error handling
- **Logging**: Implement structured logging for debugging

## CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/code-quality.yml
name: Code Quality

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'
          
      - name: Install dependencies
        run: pnpm install --frozen-lockfile
        
      - name: Run ESLint
        run: pnpm run lint
        
      - name: Run TypeScript check
        run: pnpm run type-check
        
      - name: Upload ESLint report
        uses: actions/upload-artifact@v4
        if: failure()
        with:
          name: eslint-report
          path: eslint-report.html
```

---

**Monthly Cost**: $0 (ESLint/TypeScript are open source)  
**Type Safety**: ✅ Strict TypeScript configuration  
**Code Quality**: ✅ Comprehensive ESLint rules  
**AI Assistance**: ✅ GitHub Copilot for code suggestions  
**Static Analysis**: ✅ SonarLint, DeepSource, CodeClimate integration