# pnpm - Fast, Disk Space Efficient Package Manager

## Overview

pnpm is a fast, disk space efficient package manager for JavaScript that uses a unique approach to storing dependencies. Unlike npm and yarn, pnpm creates a single content-addressable store for all packages and uses hard links to reference them in projects, significantly reducing disk space usage and installation time.

## Key Benefits

### 1. **Disk Space Efficiency**
- Single storage location for all package versions
- Hard links instead of copies save 50-70% disk space
- Ideal for monorepos and microservices architectures

### 2. **Faster Installations**
- Parallel installation of dependencies
- 2-3x faster than npm for clean installs
- Efficient caching mechanism

### 3. **Strict Dependency Resolution**
- Non-flat node_modules structure
- Prevents phantom dependencies
- Better security through isolation

### 4. **Monorepo Support**
- Built-in workspace support
- Shared dependencies across packages
- Efficient linking of local packages

## Configuration Examples

### Basic pnpm Configuration

```yaml
# .npmrc
# Store location for all packages
store-dir=~/.pnpm-store

# Strict dependency resolution
shamefully-hoist=false
hoist-pattern[]=''

# Network concurrency
network-concurrency=16

# Lifecycle scripts
enable-pre-post-scripts=true

# Registry configuration
registry=https://registry.npmjs.org/
@maritime-insurance:registry=https://npm.maritimeinsurance.com/
```

### Workspace Configuration

```yaml
# pnpm-workspace.yaml
packages:
  # Core packages
  - 'packages/*'
  # Microservices
  - 'services/*'
  # Shared libraries
  - 'libs/*'
  # Documentation
  - 'docs'
```

## Maritime Insurance Application Examples

### 1. Monorepo Structure

```bash
maritime-insurance-platform/
├── pnpm-workspace.yaml
├── package.json
├── packages/
│   ├── risk-assessment/
│   │   ├── package.json
│   │   └── src/
│   ├── vessel-tracking/
│   │   ├── package.json
│   │   └── src/
│   └── claims-processing/
│       ├── package.json
│       └── src/
├── services/
│   ├── api-gateway/
│   ├── notification-service/
│   └── reporting-service/
└── libs/
    ├── shared-types/
    ├── maritime-utils/
    └── insurance-calculations/
```

### 2. Root Package Configuration

```json
{
  "name": "maritime-insurance-platform",
  "version": "1.0.0",
  "private": true,
  "engines": {
    "node": ">=18.0.0",
    "pnpm": ">=8.0.0"
  },
  "scripts": {
    "preinstall": "npx only-allow pnpm",
    "build": "pnpm -r build",
    "test": "pnpm -r test",
    "lint": "pnpm -r lint",
    "dev": "pnpm -r --parallel dev",
    "deploy:staging": "pnpm -r --filter './services/*' deploy:staging",
    "risk:dev": "pnpm --filter @maritime/risk-assessment dev",
    "vessel:dev": "pnpm --filter @maritime/vessel-tracking dev"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "typescript": "^5.0.0",
    "eslint": "^8.0.0",
    "prettier": "^3.0.0"
  }
}
```

### 3. Service Package Example

```json
{
  "name": "@maritime/risk-assessment",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "@maritime/shared-types": "workspace:*",
    "@maritime/insurance-calculations": "workspace:*",
    "express": "^4.18.0",
    "mongoose": "^7.0.0",
    "axios": "^1.4.0"
  },
  "devDependencies": {
    "@types/express": "^4.17.0",
    "vitest": "^0.34.0"
  },
  "scripts": {
    "build": "tsc",
    "dev": "tsx watch src/index.ts",
    "test": "vitest",
    "test:coverage": "vitest --coverage"
  }
}
```

## Performance Comparisons

### Installation Speed (Real-world Monorepo)

```bash
# Maritime Insurance Platform - 1,200 dependencies
# Clean install (no cache)
pnpm install: 45s
yarn install: 110s
npm install: 135s

# With cache
pnpm install: 12s
yarn install: 28s
npm install: 35s
```

### Disk Space Usage

```bash
# 10 projects sharing similar dependencies
pnpm: 1.2GB (shared store)
yarn: 8.5GB
npm: 9.1GB

# Space savings: ~87%
```

## Security Features

### 1. Dependency Isolation

```yaml
# .npmrc - Security configuration
# Prevent phantom dependencies
shamefully-hoist=false

# Audit on install
audit-level=moderate

# Strict SSL
strict-ssl=true

# Package verification
package-lock=true
```

### 2. Security Scripts

```json
{
  "scripts": {
    "audit": "pnpm audit --audit-level=moderate",
    "audit:fix": "pnpm audit --fix",
    "audit:production": "pnpm audit --prod",
    "licenses": "pnpm licenses list",
    "outdated": "pnpm outdated -r",
    "update:interactive": "pnpm update -i -r"
  }
}
```

### 3. Dependency Overrides

```json
{
  "pnpm": {
    "overrides": {
      "lodash@<4.17.21": "4.17.21",
      "axios@<1.6.0": "1.6.0",
      "minimist@<1.2.6": "1.2.6"
    },
    "peerDependencyRules": {
      "ignoreMissing": ["@types/react"],
      "allowedVersions": {
        "react": "17 || 18"
      }
    }
  }
}
```

## CI/CD Integration

### 1. GitHub Actions

```yaml
name: Maritime Insurance CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node-version: [18.x, 20.x]
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Install pnpm
      uses: pnpm/action-setup@v2
      with:
        version: 8
    
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'pnpm'
    
    - name: Install dependencies
      run: pnpm install --frozen-lockfile
    
    - name: Run tests
      run: pnpm test:coverage
    
    - name: Build packages
      run: pnpm build
    
    - name: Run security audit
      run: pnpm audit --audit-level=high

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v4
    
    - name: Install pnpm
      uses: pnpm/action-setup@v2
      with:
        version: 8
    
    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: 20.x
        cache: 'pnpm'
    
    - name: Install production dependencies
      run: pnpm install --frozen-lockfile --prod
    
    - name: Deploy services
      run: |
        pnpm --filter './services/*' deploy:production
```

### 2. Docker Integration

```dockerfile
# Dockerfile for pnpm monorepo
FROM node:20-alpine AS base
RUN corepack enable
RUN corepack prepare pnpm@latest --activate

FROM base AS dependencies
WORKDIR /app
COPY pnpm-lock.yaml pnpm-workspace.yaml package.json ./
COPY packages/*/package.json ./packages/
COPY services/*/package.json ./services/
COPY libs/*/package.json ./libs/
RUN pnpm install --frozen-lockfile

FROM base AS build
WORKDIR /app
COPY . .
COPY --from=dependencies /app/node_modules ./node_modules
COPY --from=dependencies /app/packages/*/node_modules ./packages/*/
COPY --from=dependencies /app/services/*/node_modules ./services/*/
RUN pnpm build

FROM base AS runtime
WORKDIR /app
ENV NODE_ENV=production
COPY --from=build /app/dist ./dist
COPY --from=build /app/node_modules ./node_modules
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

## Team Collaboration Features

### 1. Shared Scripts

```json
{
  "scripts": {
    "// Team Development": "",
    "dev:all": "pnpm -r --parallel --stream dev",
    "dev:services": "pnpm -r --parallel --filter './services/*' dev",
    "dev:risk": "pnpm --filter @maritime/risk-assessment dev",
    
    "// Testing": "",
    "test:changed": "pnpm -r --filter ...[origin/main] test",
    "test:affected": "pnpm -r --filter ...{packages/**} test",
    
    "// Deployment": "",
    "deploy:service": "pnpm --filter $SERVICE_NAME deploy",
    "version:packages": "pnpm changeset version",
    "release": "pnpm changeset publish"
  }
}
```

### 2. Development Workflow

```bash
# Clone and setup
git clone https://github.com/maritime-insurance/platform
cd platform
pnpm install

# Work on specific package
pnpm --filter @maritime/risk-assessment dev

# Run tests for changed packages
pnpm test:changed

# Update dependencies interactively
pnpm update -i -r --latest

# Check for security issues
pnpm audit

# Clean install for production
pnpm install --frozen-lockfile --prod
```

## Best Practices

### 1. Lock File Management

```yaml
# .gitattributes
pnpm-lock.yaml merge=ours
```

```json
{
  "scripts": {
    "preinstall": "npx only-allow pnpm",
    "postinstall": "pnpm audit",
    "prepare": "husky install"
  }
}
```

### 2. Performance Optimization

```yaml
# .npmrc - Performance settings
# Parallel network requests
network-concurrency=32

# Faster installs
prefer-offline=true
cache-dir=.pnpm-cache

# Reduce install size
node-linker=hoisted
dedupe-peer-dependents=true
```

### 3. Monorepo Commands

```bash
# Filter commands
pnpm --filter @maritime/risk-assessment add axios
pnpm --filter './packages/*' update
pnpm --filter ...@maritime/vessel-tracking test

# Recursive commands
pnpm -r build --filter {./services}
pnpm -r --parallel start
pnpm -r exec -- rm -rf dist

# Workspace protocol
pnpm add @maritime/shared-types --workspace
```

## Pricing and Licensing

- **License**: MIT (Open Source)
- **Cost**: Free
- **Enterprise Support**: Community-driven
- **Private Registry**: Self-hosted options available

## Migration Guide

### From npm/yarn to pnpm

```bash
# 1. Install pnpm
npm install -g pnpm

# 2. Import existing lock file
pnpm import  # Reads package-lock.json or yarn.lock

# 3. Install dependencies
pnpm install

# 4. Update scripts
# Replace 'npm run' with 'pnpm'
# Replace 'yarn' with 'pnpm'

# 5. Configure CI/CD
# Update build pipelines to use pnpm
```

## Troubleshooting

### Common Issues

```bash
# Clear pnpm cache
pnpm store prune

# Verify store integrity
pnpm store status

# Fix peer dependency issues
pnpm install --fix-lockfile

# Debug installation
pnpm install --reporter=append-only
```

## Integration with Development Tools

### VS Code Settings

```json
{
  "npm.packageManager": "pnpm",
  "eslint.packageManager": "pnpm",
  "prettier.packageManager": "pnpm",
  "typescript.tsdk": "node_modules/typescript/lib"
}
```

### Pre-commit Hooks

```json
{
  "husky": {
    "hooks": {
      "pre-commit": "pnpm lint-staged",
      "pre-push": "pnpm test:changed"
    }
  },
  "lint-staged": {
    "*.{js,ts,tsx}": [
      "pnpm eslint --fix",
      "pnpm prettier --write"
    ]
  }
}
```

## Conclusion

pnpm provides significant advantages for maritime insurance applications through its efficient dependency management, excellent monorepo support, and superior performance characteristics. Its strict dependency resolution and security features make it particularly suitable for enterprise applications handling sensitive insurance data.