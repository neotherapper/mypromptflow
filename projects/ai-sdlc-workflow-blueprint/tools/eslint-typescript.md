# ESLint + TypeScript - Code Quality & Type Safety (2024/2025 Standards)

## Overview

ESLint with TypeScript integration provides comprehensive code quality enforcement and type safety for the maritime insurance application. This guide covers the latest ESLint 9.x with flat configuration and TypeScript ESLint v8.x for 2024/2025 best practices. This combination ensures consistent code style, catches potential bugs early, and maintains high code quality standards across the development team.

## 🆕 What's New in 2024/2025

### Modern Flat Configuration
- **ESLint 9.x**: New flat config system (`eslint.config.js`) replaces legacy `.eslintrc.js`
- **Better Performance**: Faster loading and execution with flat config
- **Simplified Syntax**: More intuitive configuration structure

### TypeScript ESLint v8.x
- **New Rule Sets**: `strict`, `stylistic`, `strictTypeChecked`, `stylisticTypeChecked`
- **Better Type Checking**: Enhanced integration with TypeScript compiler
- **Performance Improvements**: Faster linting with optimized type checking

### Modern Import Plugin
- **Import-X**: Modern replacement for `eslint-plugin-import` with better performance
- **ESM Support**: Enhanced ES module support and tree-shaking optimization

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

### Modern ESLint Flat Configuration (2024/2025)

```javascript
// eslint.config.js - Modern flat configuration format
import js from '@eslint/js';
import typescript from '@typescript-eslint/eslint-plugin';
import typescriptParser from '@typescript-eslint/parser';
import react from 'eslint-plugin-react';
import reactHooks from 'eslint-plugin-react-hooks';
import jsxA11y from 'eslint-plugin-jsx-a11y';
import importX from 'eslint-plugin-import-x';
import prettier from 'eslint-config-prettier';

export default [
  // Base JavaScript configuration
  js.configs.recommended,
  
  // Global configuration for all files
  {
    languageOptions: {
      ecmaVersion: 'latest',
      sourceType: 'module',
      globals: {
        browser: true,
        node: true,
        es2024: true,
      },
    },
  },
  
  // TypeScript configuration
  {
    files: ['**/*.{ts,tsx}'],
    languageOptions: {
      parser: typescriptParser,
      parserOptions: {
        ecmaFeatures: { jsx: true },
        project: './tsconfig.json',
        tsconfigRootDir: import.meta.dirname,
      },
    },
    plugins: {
      '@typescript-eslint': typescript,
      'react': react,
      'react-hooks': reactHooks,
      'jsx-a11y': jsxA11y,
      'import-x': importX,
    },
    
    // TypeScript ESLint v8.x rule sets
    rules: {
      // New TypeScript ESLint v8 strict rules
      ...typescript.configs.strict.rules,
      ...typescript.configs.stylistic.rules,
      
      // Type-checked rules (enhanced in v8)
      '@typescript-eslint/no-unused-vars': ['error', { 
        argsIgnorePattern: '^_',
        varsIgnorePattern: '^_',
        ignoreRestSiblings: true,
      }],
      '@typescript-eslint/no-explicit-any': 'warn',
      '@typescript-eslint/explicit-function-return-type': ['warn', {
        allowExpressions: true,
        allowTypedFunctionExpressions: true,
      }],
      '@typescript-eslint/no-unsafe-assignment': 'error',
      '@typescript-eslint/no-unsafe-member-access': 'error',
      '@typescript-eslint/no-unsafe-call': 'error',
      '@typescript-eslint/no-unsafe-return': 'error',
      '@typescript-eslint/prefer-nullish-coalescing': 'error',
      '@typescript-eslint/prefer-optional-chain': 'error',
      '@typescript-eslint/no-floating-promises': 'error',
      '@typescript-eslint/no-misused-promises': 'error',
      
      // New v8 rules for better type safety
      '@typescript-eslint/no-unnecessary-condition': 'warn',
      '@typescript-eslint/prefer-string-starts-ends-with': 'error',
      '@typescript-eslint/prefer-includes': 'error',
      '@typescript-eslint/switch-exhaustiveness-check': 'error',
      '@typescript-eslint/consistent-type-imports': ['error', {
        prefer: 'type-imports',
        disallowTypeAnnotations: false,
      }],
      
      // React rules with React 19 compatibility
      'react/react-in-jsx-scope': 'off',
      'react/prop-types': 'off',
      'react/jsx-uses-react': 'off',
      'react/jsx-uses-vars': 'error',
      'react/jsx-key': ['error', {
        checkFragmentShorthand: true,
        checkKeyMustBeforeSpread: true,
      }],
      'react/jsx-no-duplicate-props': 'error',
      'react/jsx-no-undef': 'error',
      'react/jsx-pascal-case': 'error',
      'react/no-deprecated': 'error',
      'react/no-direct-mutation-state': 'error',
      'react/no-unused-state': 'error',
      'react/prefer-stateless-function': 'warn',
      
      // React Hooks rules (updated for React 19)
      'react-hooks/rules-of-hooks': 'error',
      'react-hooks/exhaustive-deps': 'warn',
      
      // Accessibility rules (enhanced)
      'jsx-a11y/alt-text': 'error',
      'jsx-a11y/anchor-has-content': 'error',
      'jsx-a11y/aria-props': 'error',
      'jsx-a11y/aria-proptypes': 'error',
      'jsx-a11y/aria-unsupported-elements': 'error',
      'jsx-a11y/click-events-have-key-events': 'error',
      'jsx-a11y/heading-has-content': 'error',
      'jsx-a11y/label-has-associated-control': 'error',
      'jsx-a11y/no-redundant-roles': 'error',
      
      // Import-X rules (modern replacement for eslint-plugin-import)
      'import-x/order': ['error', {
        groups: [
          'builtin',
          'external',
          'internal',
          'parent',
          'sibling',
          'index',
          'type',
        ],
        'newlines-between': 'always',
        alphabetize: {
          order: 'asc',
          caseInsensitive: true,
        },
        pathGroups: [
          {
            pattern: '@/**',
            group: 'internal',
            position: 'before',
          },
        ],
        pathGroupsExcludedImportTypes: ['type'],
      }],
      'import-x/no-duplicates': ['error', { 'prefer-inline': true }],
      'import-x/no-unresolved': 'error',
      'import-x/no-cycle': 'error',
      'import-x/consistent-type-specifier-style': ['error', 'prefer-inline'],
      
      // General code quality rules (ESLint 9.x)
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
      'import-x/resolver': {
        typescript: {
          alwaysTryTypes: true,
          project: './tsconfig.json',
        },
        node: true,
      },
    },
  },
  
  // Test files configuration
  {
    files: ['**/*.{test,spec}.{ts,tsx}'],
    languageOptions: {
      globals: {
        jest: true,
        vi: true, // Vitest globals
      },
    },
    rules: {
      '@typescript-eslint/no-unsafe-assignment': 'off',
      '@typescript-eslint/no-unsafe-member-access': 'off',
      '@typescript-eslint/no-unsafe-call': 'off',
      '@typescript-eslint/no-explicit-any': 'off',
    },
  },
  
  // Storybook files configuration
  {
    files: ['**/*.stories.{ts,tsx}'],
    rules: {
      'import-x/no-anonymous-default-export': 'off',
      '@typescript-eslint/no-unsafe-assignment': 'off',
    },
  },
  
  // Prettier integration (must be last)
  prettier,
];
```

### Legacy Configuration (For Reference)

<details>
<summary>Click to see legacy .eslintrc.js format</summary>

```javascript
// .eslintrc.js - Legacy format (deprecated in ESLint 9.x)
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
    'plugin:import/recommended', // Note: now replaced by import-x
    'plugin:import/typescript',
    'prettier',
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaFeatures: { jsx: true },
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
    'import', // Now: import-x
  ],
  // ... rest of legacy configuration
};
```

</details>

### Enhanced TypeScript Configuration (2024/2025)

```json
// tsconfig.json - Enhanced for modern TypeScript and ESLint integration
{
  "compilerOptions": {
    "target": "ES2023", // Updated for 2024/2025
    "lib": ["DOM", "DOM.Iterable", "ES2023", "WebWorker"],
    "allowJs": true,
    "skipLibCheck": true,
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noFallthroughCasesInSwitch": true,
    "module": "ESNext",
    "moduleResolution": "Bundler", // Updated module resolution
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
    
    // Enhanced strict type checking options (TypeScript 5.4+)
    "noImplicitAny": true,
    "noImplicitReturns": true,
    "noImplicitThis": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitOverride": true,
    "noPropertyAccessFromIndexSignature": true,
    "noUncheckedIndexedAccess": true,
    
    // New TypeScript 5.4+ options for better linting integration
    "verbatimModuleSyntax": true, // Better ESM/CJS detection
    "allowImportingTsExtensions": false,
    "allowArbitraryExtensions": false,
    
    // Enhanced performance options
    "assumeChangesOnlyAffectDirectDependencies": true,
    "disableSourceOfProjectReferenceRedirect": true,
    
    // Additional modern checks
    "noEmitOnError": true,
    "useDefineForClassFields": true,
    "experimentalDecorators": true,
    "emitDecoratorMetadata": true,
    
    // Enhanced for ESLint TypeScript v8 integration
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  },
  "include": [
    "src/**/*",
    "src/**/*.json",
    "vite.config.ts",
    "vitest.config.ts",
    "eslint.config.js" // Include modern config file
  ],
  "exclude": [
    "node_modules",
    "dist",
    "build",
    "coverage",
    "**/*.test.*",
    "**/*.spec.*"
  ],
  "ts-node": {
    "esm": true,
    "experimentalSpecifierResolution": "node"
  }
}
```

### TypeScript Configuration for Strict Type Checking

For maximum type safety with TypeScript ESLint v8, consider this enhanced configuration:

```json
// tsconfig.strict.json - For maximum type safety
{
  "extends": "./tsconfig.json",
  "compilerOptions": {
    // Even stricter options for TypeScript ESLint v8 integration
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noPropertyAccessFromIndexSignature": true,
    
    // New strict options (TypeScript 5.4+)
    "allowUnusedLabels": false,
    "allowUnreachableCode": false,
    "noImplicitOverride": true,
    
    // Enhanced module resolution
    "moduleResolution": "Bundler",
    "allowImportingTsExtensions": false,
    "verbatimModuleSyntax": true
  },
  "include": ["src/**/*"],
  "exclude": ["**/*.test.*", "**/*.spec.*", "**/*.stories.*"]
}
```

## Maritime Insurance Type Definitions (Modern 2024/2025 Patterns)

### Core Domain Types with Enhanced Type Safety

```typescript
// src/types/maritime-insurance.ts - Modern TypeScript patterns
import type { z } from 'zod'; // Using Zod for runtime validation

// Branded types with enhanced validation (TypeScript 5.4+ patterns)
export type VesselId = string & { readonly __brand: 'VesselId' };
export type FleetId = string & { readonly __brand: 'FleetId' };
export type QuoteId = string & { readonly __brand: 'QuoteId' };
export type IMONumber = string & { readonly __brand: 'IMONumber' };
export type Money = number & { readonly __brand: 'Money' };
export type CountryCode = string & { readonly __brand: 'CountryCode' };

// Enhanced string literal types (using satisfies operator for type checking)
export const VESSEL_TYPES = [
  'cargo',
  'tanker', 
  'container',
  'bulk',
  'passenger',
  'offshore'
] as const satisfies readonly string[];

export const FLEET_TYPES = [
  'cargo',
  'tanker',
  'container', 
  'mixed',
  'specialized'
] as const satisfies readonly string[];

export const COVERAGE_TYPES = [
  'hull',
  'cargo',
  'liability',
  'war',
  'piracy',
  'environmental'
] as const satisfies readonly string[];

export const RISK_LEVELS = [
  'low',
  'medium', 
  'high',
  'extreme'
] as const satisfies readonly string[];

export const CLASSIFICATION_SOCIETIES = [
  'ABS',
  'DNV',
  'LR', 
  'BV',
  'CCS',
  'NK',
  'RINA'
] as const satisfies readonly string[];

// Modern type definitions using const assertions
export type VesselType = typeof VESSEL_TYPES[number];
export type FleetType = typeof FLEET_TYPES[number];
export type CoverageType = typeof COVERAGE_TYPES[number];
export type RiskLevel = typeof RISK_LEVELS[number];
export type ClassificationSociety = typeof CLASSIFICATION_SOCIETIES[number];

// Enhanced interfaces with stricter typing
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
  readonly certificates: readonly VesselCertificate[];
  readonly lastInspection: Date;
  readonly nextInspectionDue: Date;
  readonly operationalStatus: 'active' | 'maintenance' | 'decommissioned';
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
  readonly createdAt: Date;
  readonly updatedAt: Date;
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
  readonly calculatedAt: Date;
  readonly brokerCommission: Money;
}

export interface BrokerResponse {
  readonly broker: BrokerInfo;
  readonly quote: Quote;
  readonly responseTime: number;
  readonly confidence: number;
  readonly additionalNotes?: string;
  readonly timestamp: Date;
  readonly validityPeriod: number; // in days
}

// Enhanced type guards using TypeScript 5.4+ patterns
export function isVessel(obj: unknown): obj is Vessel {
  if (typeof obj !== 'object' || obj === null) return false;
  
  const vessel = obj as Record<string, unknown>;
  
  return (
    typeof vessel.id === 'string' &&
    typeof vessel.name === 'string' &&
    typeof vessel.type === 'string' &&
    VESSEL_TYPES.includes(vessel.type as VesselType) &&
    typeof vessel.tonnage === 'number' &&
    typeof vessel.value === 'number' &&
    typeof vessel.flag === 'string' &&
    typeof vessel.yearBuilt === 'number' &&
    typeof vessel.imo === 'string' &&
    typeof vessel.classification === 'string' &&
    CLASSIFICATION_SOCIETIES.includes(vessel.classification as ClassificationSociety) &&
    Array.isArray(vessel.certificates) &&
    vessel.lastInspection instanceof Date &&
    vessel.nextInspectionDue instanceof Date &&
    typeof vessel.operationalStatus === 'string'
  );
}

export function isFleet(obj: unknown): obj is Fleet {
  if (typeof obj !== 'object' || obj === null) return false;
  
  const fleet = obj as Record<string, unknown>;
  
  return (
    typeof fleet.id === 'string' &&
    typeof fleet.name === 'string' &&
    typeof fleet.type === 'string' &&
    FLEET_TYPES.includes(fleet.type as FleetType) &&
    Array.isArray(fleet.vessels) &&
    fleet.vessels.every(isVessel) &&
    typeof fleet.totalValue === 'number' &&
    fleet.createdAt instanceof Date &&
    fleet.updatedAt instanceof Date
  );
}

// Enhanced factory functions with strict validation
export function createVesselId(id: string): VesselId {
  if (!/^vessel-[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}$/i.test(id)) {
    throw new Error(`Invalid vessel ID format: ${id}. Expected format: vessel-{uuid}`);
  }
  return id as VesselId;
}

export function createFleetId(id: string): FleetId {
  if (!/^fleet-[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}$/i.test(id)) {
    throw new Error(`Invalid fleet ID format: ${id}. Expected format: fleet-{uuid}`);
  }
  return id as FleetId;
}

export function createQuoteId(id: string): QuoteId {
  if (!/^quote-[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}$/i.test(id)) {
    throw new Error(`Invalid quote ID format: ${id}. Expected format: quote-{uuid}`);
  }
  return id as QuoteId;
}

export function createMoney(amount: number): Money {
  if (amount < 0) {
    throw new Error('Money amount cannot be negative');
  }
  if (!Number.isFinite(amount)) {
    throw new Error('Money amount must be a finite number');
  }
  // Round to 2 decimal places for currency precision
  return Math.round(amount * 100) / 100 as Money;
}

export function createIMONumber(imo: string): IMONumber {
  if (!/^\d{7}$/.test(imo)) {
    throw new Error(`Invalid IMO number format: ${imo}. Expected 7 digits`);
  }
  return imo as IMONumber;
}

export function createCountryCode(code: string): CountryCode {
  if (!/^[A-Z]{2}$/.test(code)) {
    throw new Error(`Invalid country code format: ${code}. Expected 2 uppercase letters`);
  }
  return code as CountryCode;
}

// Enhanced utility types using template literals (TypeScript 5.4+)
export type VesselIdPattern = `vessel-${string}`;
export type FleetIdPattern = `fleet-${string}`;
export type QuoteIdPattern = `quote-${string}`;

// Conditional types for enhanced type safety
export type VesselByType<T extends VesselType> = T extends 'tanker' 
  ? Vessel & { readonly cargoCapacity: number; readonly hazmatCertified: boolean }
  : T extends 'passenger'
  ? Vessel & { readonly passengerCapacity: number; readonly safetyRating: number }
  : Vessel;

// Modern Result type pattern for error handling
export type Result<T, E = Error> = 
  | { readonly success: true; readonly data: T }
  | { readonly success: false; readonly error: E };

// Utility functions for Result type
export function success<T>(data: T): Result<T> {
  return { success: true, data };
}

export function failure<E = Error>(error: E): Result<never, E> {
  return { success: false, error };
}

// Enhanced validation using discriminated unions
export interface ValidationSuccess<T> {
  readonly type: 'success';
  readonly data: T;
  readonly validatedAt: Date;
}

export interface ValidationError {
  readonly type: 'error';
  readonly errors: readonly string[];
  readonly field?: string;
}

export type ValidationResult<T> = ValidationSuccess<T> | ValidationError;
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

### Required Dependencies (2024/2025 Latest Versions)

```json
// package.json - Updated for ESLint 9.x and TypeScript ESLint v8.x
{
  "devDependencies": {
    // Core ESLint 9.x with flat config support
    "eslint": "^9.15.0",
    "@eslint/js": "^9.15.0",
    
    // TypeScript ESLint v8.x with enhanced rules
    "@typescript-eslint/eslint-plugin": "^8.15.0",
    "@typescript-eslint/parser": "^8.15.0",
    
    // Modern import plugin (replaces eslint-plugin-import)
    "eslint-plugin-import-x": "^4.4.2",
    
    // React plugins with React 19 support
    "eslint-plugin-react": "^7.37.2",
    "eslint-plugin-react-hooks": "^5.0.0",
    "eslint-plugin-jsx-a11y": "^6.10.2",
    
    // Testing plugins (updated for modern testing frameworks)
    "eslint-plugin-jest": "^28.8.3",
    "eslint-plugin-jest-dom": "^5.4.0",
    "eslint-plugin-testing-library": "^6.4.0",
    "eslint-plugin-vitest": "^0.5.4", // For Vitest support
    
    // TypeScript and related tooling
    "typescript": "^5.7.2",
    "typescript-eslint": "^8.15.0", // New umbrella package
    
    // Code formatting and Git hooks
    "prettier": "^3.3.3",
    "eslint-config-prettier": "^9.1.0",
    "husky": "^9.1.6",
    "lint-staged": "^15.2.10",
    
    // Additional utilities for enhanced development
    "@types/node": "^22.9.3",
    "tsx": "^4.19.2" // For running TypeScript files directly
  },
  "engines": {
    "node": ">=18.0.0",
    "npm": ">=9.0.0"
  }
}
```

### Flat Config Compatible Versions

For projects using the modern flat configuration, ensure these minimum versions:

```json
{
  "devDependencies": {
    // ESLint 9.x is required for full flat config support
    "eslint": ">=9.0.0",
    "@eslint/js": ">=9.0.0",
    
    // TypeScript ESLint v8.x for new rule sets
    "@typescript-eslint/eslint-plugin": ">=8.0.0",
    "@typescript-eslint/parser": ">=8.0.0",
    
    // Import-X for modern import linting
    "eslint-plugin-import-x": ">=4.0.0",
    
    // React plugins with flat config support  
    "eslint-plugin-react": ">=7.35.0",
    "eslint-plugin-react-hooks": ">=5.0.0",
    
    // TypeScript 5.4+ for latest language features
    "typescript": ">=5.4.0"
  }
}
```

### Migration from Legacy Dependencies

If migrating from older versions, here's the mapping:

| Legacy Package | Modern Replacement | Notes |
|---|---|---|
| `eslint@8.x` | `eslint@9.x` | Flat config support |
| `@typescript-eslint/*@6.x` | `@typescript-eslint/*@8.x` | New rule sets |
| `eslint-plugin-import` | `eslint-plugin-import-x` | Better performance |
| `react-hooks@4.x` | `react-hooks@5.x` | React 19 support |
| N/A | `typescript-eslint@8.x` | New umbrella package |
| N/A | `eslint-plugin-vitest` | Vitest testing support |

### npm Scripts (Updated for ESLint 9.x Flat Config)

```json
{
  "scripts": {
    // ESLint 9.x scripts (no --ext flag needed with flat config)
    "lint": "eslint .",
    "lint:fix": "eslint . --fix",
    "lint:ci": "eslint . --format json --output-file eslint-report.json",
    
    // TypeScript checking
    "type-check": "tsc --noEmit",
    "type-check:watch": "tsc --noEmit --watch",
    "type-check:strict": "tsc --noEmit --project tsconfig.strict.json",
    
    // Code formatting
    "format": "prettier --write \"**/*.{ts,tsx,js,jsx,json,css,scss,md}\"",
    "format:check": "prettier --check \"**/*.{ts,tsx,js,jsx,json,css,scss,md}\"",
    
    // Combined quality checks
    "quality": "npm run lint && npm run type-check && npm run format:check",
    "quality:fix": "npm run lint:fix && npm run format",
    "quality:strict": "npm run lint && npm run type-check:strict && npm run format:check",
    
    // Advanced linting with specific rules
    "lint:performance": "eslint . --rule '@typescript-eslint/prefer-string-starts-ends-with: error' --rule '@typescript-eslint/prefer-includes: error'",
    "lint:security": "eslint . --rule 'no-eval: error' --rule 'no-implied-eval: error' --rule 'no-new-func: error'",
    
    // Git hooks setup
    "prepare": "husky install",
    
    // Development utilities
    "lint:debug": "eslint . --debug",
    "lint:print-config": "eslint --print-config src/index.ts",
    
    // Migration utilities
    "migrate:eslint": "npx @eslint/migrate-config .eslintrc.js"
  }
}
```

### Modern Lint-Staged Configuration

```json
// package.json - Updated for ESLint 9.x
{
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --fix",
      "tsc --noEmit --skipLibCheck",
      "prettier --write"
    ],
    "*.{js,jsx}": [
      "eslint --fix", 
      "prettier --write"
    ],
    "*.{json,css,scss,md}": [
      "prettier --write"
    ]
  }
}
```

### Husky Git Hooks (Updated)

```bash
# .husky/pre-commit
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Run lint-staged with ESLint 9.x
npx lint-staged

# Run TypeScript check
npm run type-check

# Optional: Run security-focused linting
npm run lint:security
```

```bash
# .husky/pre-push
#!/usr/bin/env sh
. "$(dirname -- "$0")/_/husky.sh"

# Full quality check before push
npm run quality:strict
```

## 🚀 Migration Guide: Legacy to Modern ESLint (2024/2025)

### Step 1: Prepare for Migration

Before migrating, ensure you have:
- Node.js 18+ installed
- Git repository backed up
- Current configuration documented

### Step 2: Update Dependencies

```bash
# Remove old dependencies
npm uninstall eslint @typescript-eslint/eslint-plugin @typescript-eslint/parser eslint-plugin-import

# Install modern dependencies
npm install -D eslint@^9.15.0 @eslint/js@^9.15.0
npm install -D @typescript-eslint/eslint-plugin@^8.15.0 @typescript-eslint/parser@^8.15.0
npm install -D eslint-plugin-import-x@^4.4.2
npm install -D eslint-plugin-react@^7.37.2 eslint-plugin-react-hooks@^5.0.0
npm install -D typescript@^5.7.2 typescript-eslint@^8.15.0
```

### Step 3: Convert Configuration

Use the official migration tool:

```bash
# Automatically convert .eslintrc.js to eslint.config.js
npx @eslint/migrate-config .eslintrc.js
```

Or manually create `eslint.config.js`:

```javascript
// eslint.config.js - Converted from legacy format
import js from '@eslint/js';
import typescript from '@typescript-eslint/eslint-plugin';
import typescriptParser from '@typescript-eslint/parser';

export default [
  js.configs.recommended,
  {
    files: ['**/*.{ts,tsx}'],
    languageOptions: {
      parser: typescriptParser,
      parserOptions: {
        project: './tsconfig.json',
      },
    },
    plugins: {
      '@typescript-eslint': typescript,
    },
    rules: {
      // Migrate your existing rules here
      ...typescript.configs.strict.rules,
    },
  },
];
```

### Step 4: Update Scripts

Replace in `package.json`:

```json
{
  "scripts": {
    // Old: "lint": "eslint . --ext .ts,.tsx"
    "lint": "eslint .",
    
    // Old: No migration script
    "migrate:eslint": "npx @eslint/migrate-config .eslintrc.js"
  }
}
```

### Step 5: Update Import Statements

Replace import plugin usage:

```javascript
// Old: eslint-plugin-import
import/order: 'error'

// New: eslint-plugin-import-x  
'import-x/order': 'error'
```

### Step 6: Test Migration

```bash
# Test the new configuration
npm run lint

# Check for any migration issues
npm run lint:debug

# Verify TypeScript integration
npm run type-check
```

### Step 7: Clean Up

```bash
# Remove old configuration file
rm .eslintrc.js

# Update .gitignore if needed
echo "eslint-report.json" >> .gitignore
```

### Common Migration Issues and Solutions

#### Issue 1: Import Plugin Rules Not Working

```javascript
// Problem: Old import rules don't work
'import/order': 'error'

// Solution: Update to import-x
'import-x/order': 'error'
```

#### Issue 2: TypeScript Rules Throwing Errors

```javascript
// Problem: Old TypeScript rules syntax
'@typescript-eslint/recommended-requiring-type-checking'

// Solution: Use new rule sets
...typescript.configs.strictTypeChecked.rules
```

#### Issue 3: React Rules Not Applied

```javascript
// Problem: React rules not working in flat config
extends: ['plugin:react/recommended']

// Solution: Import and apply manually
import react from 'eslint-plugin-react';

export default [{
  plugins: { react },
  rules: {
    ...react.configs.recommended.rules,
  },
}];
```

### Migration Checklist

- [ ] Dependencies updated to ESLint 9.x and TypeScript ESLint v8.x
- [ ] `.eslintrc.js` converted to `eslint.config.js`
- [ ] Import plugin replaced with import-x
- [ ] TypeScript rules updated to v8 syntax
- [ ] React rules configured for flat config
- [ ] npm scripts updated (removed `--ext` flags)
- [ ] Git hooks updated
- [ ] Configuration tested and working
- [ ] Team documentation updated

### Performance Benefits After Migration

- **Faster Loading**: Flat config loads 20-30% faster than legacy config
- **Better Type Checking**: TypeScript ESLint v8 provides enhanced type analysis
- **Improved Import Handling**: Import-X plugin offers better performance and tree-shaking
- **Modern Rule Sets**: Access to latest ESLint rules and TypeScript patterns

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

## Summary: ESLint + TypeScript 2024/2025 Modern Stack

**Modern Configuration**: ✅ ESLint 9.x with flat config (`eslint.config.js`)  
**Enhanced Type Safety**: ✅ TypeScript ESLint v8.x with strict/stylistic rule sets  
**Performance Optimized**: ✅ Import-X plugin for better tree-shaking and performance  
**React 19 Ready**: ✅ Latest React plugin with modern hooks support  
**Zero External Cost**: ✅ All tools are open source  
**Migration Support**: ✅ Complete migration guide and automated tools included  
**Modern TypeScript**: ✅ TypeScript 5.7+ with latest language features  
**AI Integration**: ✅ GitHub Copilot compatible with enhanced code suggestions  

### Key Advantages Over Legacy Setup

| Feature | Legacy ESLint 8.x | Modern ESLint 9.x |
|---------|-------------------|-------------------|
| Configuration Format | `.eslintrc.js` (complex) | `eslint.config.js` (flat, intuitive) |
| TypeScript Rules | v6.x (limited) | v8.x (strict, stylistic, type-checked) |
| Import Handling | `eslint-plugin-import` | `eslint-plugin-import-x` (faster) |
| React Support | Basic rules | React 19 compatible with hooks 5.x |
| Performance | Slower startup | 20-30% faster loading |
| Type Checking | Basic integration | Enhanced TypeScript 5.7+ integration |
| Rule Categories | Mixed organization | Clear strict/stylistic separation |

### Implementation Readiness

- **Documentation**: Complete with modern examples and patterns
- **Migration Path**: Step-by-step guide with automated tools
- **Team Training**: Examples cover maritime insurance domain types
- **CI/CD Integration**: Updated GitHub Actions workflows included
- **Development Workflow**: Modern git hooks and lint-staged configuration

This modernized ESLint + TypeScript setup provides the foundation for high-quality, type-safe code development using 2024/2025 industry best practices.