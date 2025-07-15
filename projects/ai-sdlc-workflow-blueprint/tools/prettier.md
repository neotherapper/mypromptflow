# Prettier - Code Formatting & Style Consistency

## Overview

Prettier is an opinionated code formatter that enforces consistent code style across the maritime insurance application. It automatically formats code according to predefined rules, eliminating style debates and ensuring a uniform codebase across all team members.

## Key Benefits

### Consistent Code Style
- **Automatic formatting** eliminates manual code styling
- **Team consistency** ensures all code follows the same formatting rules
- **Reduced cognitive load** by removing formatting decisions
- **Faster code reviews** by focusing on logic rather than style

### Developer Experience
- **Editor integration** with real-time formatting
- **Pre-commit hooks** to ensure consistent formatting
- **CI/CD integration** to validate formatting in pull requests
- **Minimal configuration** with sensible defaults

## Configuration

### Prettier Configuration

```json
// .prettierrc.json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2,
  "useTabs": false,
  "bracketSpacing": true,
  "bracketSameLine": false,
  "arrowParens": "avoid",
  "endOfLine": "lf",
  "quoteProps": "as-needed",
  "jsxSingleQuote": true,
  "proseWrap": "preserve",
  "htmlWhitespaceSensitivity": "css",
  "embeddedLanguageFormatting": "auto",
  "insertPragma": false,
  "requirePragma": false,
  "plugins": ["prettier-plugin-tailwindcss", "prettier-plugin-organize-imports"],
  "overrides": [
    {
      "files": "*.md",
      "options": {
        "printWidth": 80,
        "proseWrap": "always"
      }
    },
    {
      "files": "*.json",
      "options": {
        "printWidth": 200,
        "tabWidth": 2
      }
    },
    {
      "files": "*.yml",
      "options": {
        "tabWidth": 2,
        "singleQuote": false
      }
    },
    {
      "files": "*.tsx",
      "options": {
        "jsxSingleQuote": true,
        "bracketSameLine": false
      }
    }
  ]
}
```

### Prettier Ignore Configuration

```bash
# .prettierignore
# Build directories
build/
dist/
coverage/
node_modules/

# Generated files
*.generated.ts
*.generated.tsx
*.d.ts
!src/**/*.d.ts

# Config files that shouldn't be formatted
.env*
*.min.js
*.min.css

# Documentation that requires specific formatting
CHANGELOG.md
LICENSE

# Storybook build
storybook-static/

# Testing
__snapshots__/
test-results/
playwright-report/

# Package files
package-lock.json
yarn.lock
pnpm-lock.yaml

# IDE files
.vscode/
.idea/

# Maritime insurance specific
# Keep certain data files unformatted
src/data/vessel-types.json
src/data/country-codes.json
src/data/classification-societies.json
```

## Integration with Development Tools

### ESLint Integration

```json
// .eslintrc.js (relevant parts)
{
  "extends": [
    "eslint:recommended",
    "@typescript-eslint/recommended",
    "plugin:react/recommended",
    "prettier" // Must be last to override other formatting rules
  ],
  "plugins": ["prettier"],
  "rules": {
    "prettier/prettier": "error"
  }
}
```

### Package.json Scripts

```json
{
  "scripts": {
    "format": "prettier --write \"src/**/*.{ts,tsx,js,jsx,json,md}\"",
    "format:check": "prettier --check \"src/**/*.{ts,tsx,js,jsx,json,md}\"",
    "lint": "eslint src --ext .ts,.tsx --fix",
    "lint:check": "eslint src --ext .ts,.tsx",
    "code-quality": "npm run format && npm run lint",
    "code-quality:check": "npm run format:check && npm run lint:check"
  }
}
```

## Maritime Insurance Code Examples

*Note: The maritime insurance examples below are illustrative and demonstrate how Prettier formats real-world TypeScript code in a domain-specific application.*

### Before and After Formatting

#### Component Example - Before

```typescript
// Before Prettier formatting
import React,{useState,useEffect} from 'react';
import{Fleet,Vessel,VesselType}from '../types/maritime-insurance';
import{useFleetData}from '../hooks/useFleetData';

interface FleetManagementProps{
fleets:Fleet[];
onFleetCreate:(fleet:Omit<Fleet,'id'>)=>void;
onFleetUpdate:(id:string,fleet:Partial<Fleet>)=>void;
onFleetDelete:(id:string)=>void;
}

export const FleetManagement:React.FC<FleetManagementProps>=({fleets,onFleetCreate,onFleetUpdate,onFleetDelete})=>{
const[selectedFleet,setSelectedFleet]=useState<Fleet|null>(null);
const[isLoading,setIsLoading]=useState(false);
const{updateFleet,deleteFleet}=useFleetData();

const handleFleetSelect=(fleet:Fleet)=>{
setSelectedFleet(fleet);
};

const handleVesselAdd=async(vessel:Omit<Vessel,'id'>)=>{
if(!selectedFleet)return;
setIsLoading(true);
try{
const updatedFleet={...selectedFleet,vessels:[...selectedFleet.vessels,{...vessel,id:`vessel-${Date.now()}`}]};
await updateFleet(selectedFleet.id,updatedFleet);
onFleetUpdate(selectedFleet.id,updatedFleet);
}catch(error){
console.error('Failed to add vessel:',error);
}finally{
setIsLoading(false);
}
};

return(<div className="fleet-management">
<h2>Fleet Management</h2>
{fleets.map(fleet=>(
<div key={fleet.id}className="fleet-card"onClick={()=>handleFleetSelect(fleet)}>
<h3>{fleet.name}</h3>
<p>Type: {fleet.type}</p>
<p>Vessels: {fleet.vessels.length}</p>
<p>Total Value: ${fleet.totalValue.toLocaleString()}</p>
</div>
))}
</div>);
};
```

#### Component Example - After

```typescript
// After Prettier formatting
import React, { useState, useEffect } from 'react';

import { Fleet, Vessel, VesselType } from '../types/maritime-insurance';
import { useFleetData } from '../hooks/useFleetData';

interface FleetManagementProps {
  fleets: Fleet[];
  onFleetCreate: (fleet: Omit<Fleet, 'id'>) => void;
  onFleetUpdate: (id: string, fleet: Partial<Fleet>) => void;
  onFleetDelete: (id: string) => void;
}

export const FleetManagement: React.FC<FleetManagementProps> = ({
  fleets,
  onFleetCreate,
  onFleetUpdate,
  onFleetDelete,
}) => {
  const [selectedFleet, setSelectedFleet] = useState<Fleet | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const { updateFleet, deleteFleet } = useFleetData();

  const handleFleetSelect = (fleet: Fleet) => {
    setSelectedFleet(fleet);
  };

  const handleVesselAdd = async (vessel: Omit<Vessel, 'id'>) => {
    if (!selectedFleet) return;
    
    setIsLoading(true);
    try {
      const updatedFleet = {
        ...selectedFleet,
        vessels: [
          ...selectedFleet.vessels,
          { ...vessel, id: `vessel-${Date.now()}` },
        ],
      };
      
      await updateFleet(selectedFleet.id, updatedFleet);
      onFleetUpdate(selectedFleet.id, updatedFleet);
    } catch (error) {
      console.error('Failed to add vessel:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className='fleet-management'>
      <h2>Fleet Management</h2>
      {fleets.map(fleet => (
        <div
          key={fleet.id}
          className='fleet-card'
          onClick={() => handleFleetSelect(fleet)}
        >
          <h3>{fleet.name}</h3>
          <p>Type: {fleet.type}</p>
          <p>Vessels: {fleet.vessels.length}</p>
          <p>Total Value: ${fleet.totalValue.toLocaleString()}</p>
        </div>
      ))}
    </div>
  );
};
```

### Service Layer Example

```typescript
// Maritime Insurance Service - Formatted
import { Fleet, Vessel, Quote, QuoteRequest } from '../types/maritime-insurance';
import { APIClient } from '../utils/api-client';
import { logger } from '../utils/logger';

export class MaritimeInsuranceService {
  private readonly apiClient: APIClient;

  constructor(apiClient: APIClient) {
    this.apiClient = apiClient;
  }

  async generateQuote(request: QuoteRequest): Promise<Quote> {
    logger.info('Generating quote for fleet', {
      fleetId: request.fleetId,
      coverageTypes: request.coverageTypes,
      routes: request.routes.map(r => r.name),
    });

    try {
      const response = await this.apiClient.post<Quote>('/quotes/generate', {
        fleetId: request.fleetId,
        coverageTypes: request.coverageTypes,
        routes: request.routes,
        effectiveDate: request.effectiveDate,
        duration: request.duration,
      });

      return response.data;
    } catch (error) {
      logger.error('Failed to generate quote', {
        error: error.message,
        fleetId: request.fleetId,
      });
      throw error;
    }
  }

  async getFleetRiskAssessment(fleetId: string): Promise<RiskAssessment> {
    const fleet = await this.apiClient.get<Fleet>(`/fleets/${fleetId}`);
    
    const riskFactors = await Promise.all([
      this.assessRouteRisk(fleet.data.operationalRoutes),
      this.assessVesselRisk(fleet.data.vessels),
      this.assessOperationalRisk(fleet.data),
    ]);

    return {
      fleetId,
      overallRisk: this.calculateOverallRisk(riskFactors),
      riskFactors,
      recommendations: this.generateRiskRecommendations(riskFactors),
    };
  }

  private async assessRouteRisk(routes: Route[]): Promise<RiskFactor> {
    const highRiskRoutes = routes.filter(route => 
      route.riskLevel === 'high' || route.pirateRisk > 0.3
    );

    return {
      category: 'route',
      level: highRiskRoutes.length > 0 ? 'high' : 'medium',
      description: `${highRiskRoutes.length} high-risk routes identified`,
      impact: highRiskRoutes.length * 0.15,
      mitigation: [
        'Consider alternative routing',
        'Increase security measures',
        'Adjust sailing schedules',
      ],
    };
  }

  private calculateOverallRisk(riskFactors: RiskFactor[]): RiskLevel {
    const averageImpact = riskFactors.reduce((sum, factor) => sum + factor.impact, 0) / riskFactors.length;
    
    if (averageImpact > 0.7) return 'high';
    if (averageImpact > 0.4) return 'medium';
    return 'low';
  }
}
```

## AI-Assisted Code Formatting

### Using AI Tools with Prettier

While Prettier handles automatic code formatting, AI tools can help with code formatting in several ways:

#### 1. Configuration Optimization
AI assistants can help analyze your codebase and suggest optimal Prettier configurations based on:
- Team preferences and existing code patterns
- Industry best practices
- Framework-specific conventions
- Performance considerations

#### 2. Custom Rule Development
When you need formatting beyond Prettier's capabilities, AI can help:
- Write custom ESLint rules for domain-specific patterns
- Create code transformation scripts
- Generate formatting migration scripts
- Develop team-specific style guides

#### 3. Code Review Assistance
AI tools can complement Prettier by:
- Explaining why certain formatting is preferred
- Suggesting structural improvements beyond formatting
- Identifying patterns that could benefit from refactoring
- Helping maintain consistent naming conventions

### Practical AI Integration Examples

#### Configuration Analysis
```typescript
// Example: Using AI to analyze and suggest Prettier config improvements
// This is a conceptual example - actual implementation would use your preferred AI tool

async function analyzeFormattingPatterns(projectPath: string): Promise<ConfigSuggestions> {
  // Analyze existing code patterns
  const codePatterns = await scanCodebase(projectPath);
  
  // Generate configuration suggestions based on patterns
  const suggestions = {
    printWidth: determinOptimalLineWidth(codePatterns),
    tabWidth: mostCommonIndentation(codePatterns),
    trailingComma: shouldUseTrailingCommas(codePatterns),
    // ... other configuration options
  };
  
  return suggestions;
}
```

#### Style Guide Documentation
```typescript
// Example: Generating style guide documentation from Prettier config
export function generateStyleGuide(prettierConfig: PrettierConfig): string {
  const guide = `
# Code Style Guide

This project uses Prettier for automatic code formatting with the following rules:

## Line Width
- Maximum line width: ${prettierConfig.printWidth} characters
- This helps maintain readability on standard displays

## Indentation
- Tab width: ${prettierConfig.tabWidth} spaces
- Using spaces for consistent rendering across editors

## Quotes
- ${prettierConfig.singleQuote ? 'Single quotes' : 'Double quotes'} for strings
- ${prettierConfig.jsxSingleQuote ? 'Single quotes' : 'Double quotes'} in JSX

## Trailing Commas
- ${prettierConfig.trailingComma === 'all' ? 'Always use trailing commas' : 
     prettierConfig.trailingComma === 'es5' ? 'Use trailing commas where valid in ES5' : 
     'No trailing commas'}

## Semicolons
- ${prettierConfig.semi ? 'Always use semicolons' : 'Omit semicolons where possible'}
  `;
  
  return guide;
}
```

### Real AI Tools for Code Formatting Support

#### 1. GitHub Copilot
- **Format suggestions**: Provides formatting suggestions while coding
- **Pattern detection**: Learns from your codebase formatting patterns
- **Configuration help**: Assists in writing Prettier configurations

#### 2. Codeium
- **Free AI assistant**: Helps with code formatting and style consistency
- **Multi-language support**: Works across different file types
- **Format explanations**: Explains formatting choices and best practices

#### 3. Tabnine
- **Code completion**: Suggests properly formatted code completions
- **Team learning**: Learns from team's formatting preferences
- **Local processing**: Can run locally for privacy

#### 4. AI-Powered Linters
- **ESLint with AI**: Some ESLint plugins use AI for pattern detection
- **Custom rule generation**: AI can help create custom linting rules
- **Format migration**: AI assists in migrating between formatting standards

### Practical Prettier Plugins

#### Real Prettier Plugins You Can Use
```json
{
  "devDependencies": {
    "@prettier/plugin-php": "^0.22.0",
    "@prettier/plugin-pug": "^3.0.0",
    "@prettier/plugin-ruby": "^4.0.0",
    "@prettier/plugin-xml": "^3.0.0",
    "prettier": "^3.0.0",
    "prettier-plugin-go-template": "^0.0.15",
    "prettier-plugin-java": "^2.0.0",
    "prettier-plugin-organize-imports": "^3.0.0",
    "prettier-plugin-packagejson": "^2.0.0",
    "prettier-plugin-properties": "^0.3.0",
    "prettier-plugin-sh": "^0.14.0",
    "prettier-plugin-sql": "^0.18.0",
    "prettier-plugin-tailwindcss": "^0.6.0",
    "prettier-plugin-toml": "^2.0.0"
  }
}
```

## Editor Integration

### VS Code Configuration

```json
// .vscode/settings.json
{
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "editor.formatOnPaste": true,
  "editor.formatOnType": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true,
    "source.organizeImports": true
  },
  "prettier.requireConfig": true,
  "prettier.useEditorConfig": false,
  "typescript.preferences.importModuleSpecifier": "relative",
  "typescript.suggest.autoImports": true,
  "typescript.updateImportsOnFileMove.enabled": "always",
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescriptreact]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[json]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[markdown]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.wordWrap": "on"
  }
}
```

### Git Hooks Integration

```bash
#!/bin/sh
# .husky/pre-commit
. "$(dirname "$0")/_/husky.sh"

# Run Prettier on staged files
npx lint-staged

# Run type checking
npm run type-check

# Run tests on staged files
npm run test:staged
```

```json
// package.json - lint-staged configuration
{
  "lint-staged": {
    "*.{ts,tsx,js,jsx}": [
      "prettier --write",
      "eslint --fix",
      "git add"
    ],
    "*.{json,md,yml,yaml}": [
      "prettier --write",
      "git add"
    ]
  }
}
```

## Team Workflow Integration

### Development Team Usage

#### Head of Engineering
- **Code style enforcement**: Ensure consistent formatting across all team members
- **CI/CD integration**: Monitor formatting compliance in deployment pipeline
- **Team standards**: Set and maintain formatting standards for the project

#### Lead Frontend Developer
- **Component formatting**: Ensure React components follow consistent formatting
- **Style guide maintenance**: Maintain and update Prettier configuration
- **Code review efficiency**: Focus on logic rather than formatting in reviews

#### Lead Backend Developer
- **API formatting**: Ensure service layer code follows consistent patterns
- **Type definition formatting**: Maintain clean and readable type definitions
- **Error handling formatting**: Ensure consistent error handling patterns

#### UI/UX Engineer
- **Style consistency**: Ensure styling code follows consistent patterns
- **Component documentation**: Maintain well-formatted component examples
- **Design system formatting**: Keep design system code properly formatted

## Best Practices

### Configuration Management
- **Team consensus**: Agree on formatting rules as a team
- **Minimal configuration**: Use Prettier defaults where possible
- **Consistent enforcement**: Apply formatting rules consistently
- **Documentation**: Document any custom formatting decisions

### Editor Setup
- **Format on save**: Enable automatic formatting in editors
- **Pre-commit hooks**: Prevent unformatted code from being committed
- **Team alignment**: Ensure all team members use the same configuration
- **Tool updates**: Keep Prettier and plugins updated

### Code Quality
- **Readability first**: Prioritize code readability over personal preferences
- **Consistent patterns**: Use consistent formatting patterns throughout
- **Team efficiency**: Reduce time spent on formatting discussions
- **Focus on logic**: Spend code review time on business logic

## Performance and Optimization

### Formatting Performance

```typescript
// src/scripts/format-performance.ts
import { performance } from 'perf_hooks';
import prettier from 'prettier';

export async function measureFormattingPerformance(): Promise<void> {
  const files = await glob('src/**/*.{ts,tsx}');
  const config = await prettier.resolveConfig('.');
  
  const startTime = performance.now();
  
  for (const file of files) {
    const content = await fs.readFile(file, 'utf-8');
    const formatted = prettier.format(content, {
      ...config,
      filepath: file,
    });
    
    if (content !== formatted) {
      await fs.writeFile(file, formatted);
    }
  }
  
  const endTime = performance.now();
  const duration = endTime - startTime;
  
  console.log(`Formatted ${files.length} files in ${duration.toFixed(2)}ms`);
  console.log(`Average: ${(duration / files.length).toFixed(2)}ms per file`);
}
```

### Incremental Formatting

```typescript
// src/scripts/incremental-format.ts
import { execSync } from 'child_process';

export function formatChangedFiles(): void {
  // Get list of changed files
  const changedFiles = execSync('git diff --name-only --cached')
    .toString()
    .split('\n')
    .filter(file => file.match(/\.(ts|tsx|js|jsx)$/));
  
  if (changedFiles.length === 0) {
    console.log('No files to format');
    return;
  }
  
  // Format only changed files
  const fileList = changedFiles.join(' ');
  execSync(`npx prettier --write ${fileList}`);
  execSync(`git add ${fileList}`);
  
  console.log(`Formatted ${changedFiles.length} changed files`);
}
```

## Common Issues and Solutions

### Formatting Conflicts

#### ESLint vs Prettier Conflicts
```javascript
// Problem: ESLint and Prettier have conflicting rules
// Solution: Use eslint-config-prettier to disable conflicting ESLint rules

module.exports = {
  extends: [
    'eslint:recommended',
    'plugin:@typescript-eslint/recommended',
    'plugin:react/recommended',
    'prettier' // Must be last - disables ESLint rules that conflict with Prettier
  ],
  rules: {
    // Avoid these formatting rules - let Prettier handle them
    // 'indent': ['error', 2], // Don't use this
    // 'quotes': ['error', 'single'], // Don't use this
    // 'semi': ['error', 'always'], // Don't use this
    
    // Use these logic/quality rules instead
    'no-unused-vars': 'error',
    'no-console': 'warn',
    'prefer-const': 'error'
  }
};
```

#### Editor Integration Issues
```json
// VS Code settings.json - Common fixes
{
  // Fix: Prettier not running on save
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  
  // Fix: Wrong formatter being used
  "[javascript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  "[typescript]": {
    "editor.defaultFormatter": "esbenp.prettier-vscode"
  },
  
  // Fix: Prettier ignoring configuration
  "prettier.requireConfig": true,
  
  // Fix: Format on save timeout issues
  "editor.formatOnSaveTimeout": 5000
}
```

### Performance Optimization

#### Large Codebase Formatting
```bash
# Format only changed files in git
prettier --write $(git diff --name-only --diff-filter=ACM | grep -E '\.(js|jsx|ts|tsx)$')

# Format files in chunks to avoid memory issues
find src -name "*.ts" -o -name "*.tsx" | xargs -n 50 prettier --write

# Use cache for faster formatting
prettier --write --cache --cache-location .prettierCache "src/**/*.{js,jsx,ts,tsx}"
```

#### Pre-commit Performance
```json
// .lintstagedrc.json - Optimize pre-commit performance
{
  "*.{js,jsx,ts,tsx}": [
    "prettier --write --cache",
    "eslint --fix --cache"
  ],
  "*.{json,md,yml}": [
    "prettier --write"
  ]
}
```

## CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/code-formatting.yml
name: Code Formatting

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  format-check:
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
        
      - name: Check code formatting
        run: pnpm run format:check
        
      - name: Comment on PR if formatting needed
        if: failure()
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '❌ Code formatting check failed. Please run `npm run format` to fix formatting issues.'
            })
```

### Auto-formatting Action

```yaml
# .github/workflows/auto-format.yml
name: Auto Format

on:
  push:
    branches: [develop]

jobs:
  auto-format:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          
      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'pnpm'
          
      - name: Install dependencies
        run: pnpm install --frozen-lockfile
        
      - name: Format code
        run: pnpm run format
        
      - name: Commit changes
        uses: stefanzweifel/git-auto-commit-action@v5
        with:
          commit_message: 'style: auto-format code with Prettier'
          file_pattern: '*.ts *.tsx *.js *.jsx *.json *.md'
```

## Prettier Tips and Tricks

### Advanced Configuration

#### File-Specific Formatting
```javascript
// .prettierrc.js - Dynamic configuration
module.exports = {
  // Base configuration
  semi: true,
  singleQuote: true,
  tabWidth: 2,
  
  // Override for specific file patterns
  overrides: [
    {
      files: ['*.json', '*.jsonc'],
      options: {
        tabWidth: 2,
        printWidth: 200,
        trailingComma: 'none'
      }
    },
    {
      files: ['*.yml', '*.yaml'],
      options: {
        tabWidth: 2,
        singleQuote: false
      }
    },
    {
      files: ['**/*.test.ts', '**/*.spec.ts'],
      options: {
        printWidth: 120 // Allow longer lines in tests
      }
    },
    {
      files: ['*.md'],
      options: {
        proseWrap: 'always',
        printWidth: 80
      }
    }
  ]
};
```

#### Ignore Formatting Selectively
```typescript
// Ignore next line
// prettier-ignore
const matrix = [
  [1, 0, 0, 0],
  [0, 1, 0, 0],
  [0, 0, 1, 0],
  [0, 0, 0, 1]
];

// Ignore block
// prettier-ignore-start
const complexQuery = `
  SELECT    u.id,
            u.name,
            COUNT(o.id) as order_count
  FROM      users u
  LEFT JOIN orders o ON u.id = o.user_id
  GROUP BY  u.id, u.name
`;
// prettier-ignore-end

// HTML/JSX ignore
<div>
  {/* prettier-ignore */}
  <span>Preserve   this   spacing</span>
</div>
```

### Integration Best Practices

#### Gradual Adoption
```bash
# Format new/changed files only
git diff --name-only --diff-filter=ACM | xargs prettier --write

# Format specific directories progressively
prettier --write "src/components/**/*.{js,jsx}"
prettier --write "src/utils/**/*.{ts,tsx}"
prettier --write "src/services/**/*.ts"

# Check formatting without changing files
prettier --check "src/**/*.{js,jsx,ts,tsx}"
```

#### Team Onboarding Script
```json
// package.json
{
  "scripts": {
    "format": "prettier --write .",
    "format:check": "prettier --check .",
    "format:staged": "lint-staged",
    "setup:prettier": "npm run format && git add -A && git commit -m 'chore: initial prettier formatting'",
    "format:diff": "prettier --write $(git diff --name-only HEAD)",
    "format:branch": "prettier --write $(git diff --name-only $(git merge-base HEAD main))"
  }
}
```

### Troubleshooting Guide

#### Common Problems and Solutions

1. **Prettier not working in VS Code**
   - Install Prettier extension: `ext install esbenp.prettier-vscode`
   - Check workspace settings override user settings
   - Verify `.prettierrc` is in project root
   - Check output panel for Prettier errors

2. **Different formatting between developers**
   - Ensure everyone has same Prettier version
   - Commit `.prettierrc` to repository
   - Use exact version in package.json: `"prettier": "3.0.0"`
   - Run `npm ci` instead of `npm install`

3. **CI/CD formatting failures**
   - Match local and CI Prettier versions
   - Use `--check` in CI, not `--write`
   - Cache node_modules in CI
   - Consider using Docker for consistency

4. **Performance issues**
   - Use `--cache` flag
   - Limit file patterns
   - Exclude large generated files
   - Format in parallel when possible

---

**Monthly Cost**: $0 (Open Source)  
**Code Consistency**: ✅ Automatic formatting enforcement  
**Team Efficiency**: ✅ Reduced formatting discussions  
**CI/CD Integration**: ✅ Automated formatting validation