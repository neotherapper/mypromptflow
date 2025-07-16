# Storybook - Component Development & Documentation

## Overview

Storybook is a powerful open-source tool for developing, testing, and documenting UI components in isolation. It provides a sandbox environment where developers can build and test components independently of the main application, making it ideal for component-driven development and design system management. Storybook supports React, Vue, Angular, and many other frameworks.

## Key Benefits

### Component Development
- **Isolated development** environment for building components independently
- **Interactive playground** for testing component states and variations
- **Visual documentation** that serves as a living style guide
- **Hot reloading** for rapid development and iteration

### Design System Management
- **Component library** documentation and organization
- **Visual regression testing** to catch UI changes
- **Design tokens** integration for consistent styling
- **Accessibility testing** built into the workflow

## Configuration

### Basic Storybook Setup

```typescript
// .storybook/main.ts
import type { StorybookConfig } from '@storybook/react-vite';

const config: StorybookConfig = {
  stories: ['../src/**/*.stories.@(js|jsx|ts|tsx|mdx)'],
  addons: [
    '@storybook/addon-essentials',
    '@storybook/addon-interactions',
    '@storybook/addon-a11y',
    '@storybook/addon-viewport',
    '@storybook/addon-docs',
    '@storybook/addon-controls',
    '@storybook/addon-actions',
  ],
  framework: {
    name: '@storybook/react-vite',
    options: {},
  },
  typescript: {
    check: false,
    reactDocgen: 'react-docgen-typescript',
    reactDocgenTypescriptOptions: {
      shouldExtractLiteralValuesFromEnum: true,
      propFilter: (prop) => (prop.parent ? !/node_modules/.test(prop.parent.fileName) : true),
    },
  },
  docs: {
    autodocs: 'tag',
  },
};

export default config;
```

### Preview Configuration

```typescript
// .storybook/preview.ts
import type { Preview } from '@storybook/react';
import { INITIAL_VIEWPORTS } from '@storybook/addon-viewport';
import '../src/index.css';

const preview: Preview = {
  parameters: {
    actions: { argTypesRegex: '^on[A-Z].*' },
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/,
      },
    },
    viewport: {
      viewports: {
        ...INITIAL_VIEWPORTS,
        maritimeDesktop: {
          name: 'Maritime Desktop',
          styles: {
            width: '1440px',
            height: '900px',
          },
        },
        maritimeTablet: {
          name: 'Maritime Tablet',
          styles: {
            width: '768px',
            height: '1024px',
          },
        },
        maritimeMobile: {
          name: 'Maritime Mobile',
          styles: {
            width: '375px',
            height: '667px',
          },
        },
      },
    },
    backgrounds: {
      default: 'light',
      values: [
        { name: 'light', value: '#ffffff' },
        { name: 'dark', value: '#1a1a1a' },
        { name: 'maritime', value: '#003366' },
      ],
    },
  },
  globalTypes: {
    theme: {
      description: 'Global theme for components',
      defaultValue: 'light',
      toolbar: {
        title: 'Theme',
        icon: 'paintbrush',
        items: ['light', 'dark'],
        dynamicTitle: true,
      },
    },
  },
};

export default preview;
```

## Maritime Insurance Component Stories

### Fleet Management Component Stories

```typescript
// src/components/FleetManagement/FleetManagement.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { FleetManagement } from './FleetManagement';
import { mockFleetData } from '../../test/fixtures/fleet-fixtures';

const meta: Meta<typeof FleetManagement> = {
  title: 'Maritime Insurance/Fleet Management',
  component: FleetManagement,
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component: 'Fleet Management component for maritime insurance applications. Handles fleet creation, vessel management, and fleet overview functionality.',
      },
    },
  },
  argTypes: {
    onFleetCreate: { action: 'fleet-created' },
    onFleetUpdate: { action: 'fleet-updated' },
    onFleetDelete: { action: 'fleet-deleted' },
    onVesselAdd: { action: 'vessel-added' },
    onVesselUpdate: { action: 'vessel-updated' },
    onVesselDelete: { action: 'vessel-deleted' },
  },
  decorators: [
    (Story) => (
      <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
        <Story />
      </div>
    ),
  ],
};

export default meta;
type Story = StoryObj<typeof FleetManagement>;

export const Default: Story = {
  args: {
    fleets: mockFleetData,
    loading: false,
    error: null,
  },
};

export const EmptyState: Story = {
  args: {
    fleets: [],
    loading: false,
    error: null,
  },
  parameters: {
    docs: {
      description: {
        story: 'Empty state shown when no fleets exist.',
      },
    },
  },
};

export const Loading: Story = {
  args: {
    fleets: [],
    loading: true,
    error: null,
  },
};

export const Error: Story = {
  args: {
    fleets: [],
    loading: false,
    error: 'Failed to load fleet data',
  },
};

export const LargeFleet: Story = {
  args: {
    fleets: [
      {
        id: 'large-fleet-1',
        name: 'Global Shipping Fleet',
        type: 'mixed',
        size: 150,
        totalValue: 500000000,
        vessels: Array.from({ length: 150 }, (_, i) => ({
          id: `vessel-${i + 1}`,
          name: `MV Vessel ${i + 1}`,
          type: i % 3 === 0 ? 'cargo' : i % 3 === 1 ? 'tanker' : 'container',
          tonnage: 30000 + (i * 1000),
          value: 2000000 + (i * 100000),
          flag: ['GR', 'US', 'GB', 'DE', 'NL'][i % 5],
          yearBuilt: 2010 + (i % 14),
        })),
        routes: ['Mediterranean Sea', 'North Atlantic', 'Pacific Ocean'],
        riskLevel: 'high',
      },
    ],
    loading: false,
    error: null,
  },
  parameters: {
    docs: {
      description: {
        story: 'Large fleet with 150+ vessels to test performance and pagination.',
      },
    },
  },
};

export const MixedFleetTypes: Story = {
  args: {
    fleets: [
      {
        id: 'cargo-fleet',
        name: 'Mediterranean Cargo Fleet',
        type: 'cargo',
        size: 25,
        totalValue: 50000000,
        vessels: mockFleetData[0].vessels,
        routes: ['Mediterranean Sea'],
        riskLevel: 'medium',
      },
      {
        id: 'tanker-fleet',
        name: 'Oil Tanker Fleet',
        type: 'tanker',
        size: 12,
        totalValue: 120000000,
        vessels: [
          {
            id: 'tanker-1',
            name: 'MT Oceanic',
            type: 'tanker',
            tonnage: 80000,
            value: 10000000,
            flag: 'LR',
            yearBuilt: 2018,
          },
        ],
        routes: ['Horn of Africa', 'Persian Gulf'],
        riskLevel: 'high',
      },
    ],
    loading: false,
    error: null,
  },
};
```

### Quote Generator Component Stories

```typescript
// src/components/QuoteGenerator/QuoteGenerator.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { QuoteGenerator } from './QuoteGenerator';
import { mockFleetData } from '../../test/fixtures/fleet-fixtures';

const meta: Meta<typeof QuoteGenerator> = {
  title: 'Maritime Insurance/Quote Generator',
  component: QuoteGenerator,
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component: 'Quote Generator component for creating maritime insurance quotes based on fleet data and risk assessment.',
      },
    },
  },
  argTypes: {
    onQuoteGenerated: { action: 'quote-generated' },
    onQuoteError: { action: 'quote-error' },
  },
};

export default meta;
type Story = StoryObj<typeof QuoteGenerator>;

export const Default: Story = {
  args: {
    availableFleets: mockFleetData,
    loading: false,
    error: null,
  },
};

export const WithSelectedFleet: Story = {
  args: {
    availableFleets: mockFleetData,
    selectedFleet: mockFleetData[0],
    loading: false,
    error: null,
  },
};

export const GeneratingQuote: Story = {
  args: {
    availableFleets: mockFleetData,
    selectedFleet: mockFleetData[0],
    loading: true,
    error: null,
    quoteInProgress: true,
  },
};

export const QuoteGenerated: Story = {
  args: {
    availableFleets: mockFleetData,
    selectedFleet: mockFleetData[0],
    loading: false,
    error: null,
    generatedQuote: {
      id: 'quote-123',
      premium: 125000,
      coverage: 50000000,
      deductible: 25000,
      validUntil: new Date('2024-12-31'),
      coverageTypes: ['hull', 'cargo', 'liability'],
      riskFactors: [
        { factor: 'Route Risk', impact: 'medium', description: 'Mediterranean route with moderate piracy risk' },
        { factor: 'Vessel Age', impact: 'low', description: 'Modern fleet with average age of 8 years' },
        { factor: 'Cargo Type', impact: 'medium', description: 'General cargo with standard risk profile' },
      ],
    },
  },
};

export const HighRiskFleet: Story = {
  args: {
    availableFleets: [
      {
        id: 'high-risk-fleet',
        name: 'High Risk Tanker Fleet',
        type: 'tanker',
        size: 8,
        totalValue: 80000000,
        vessels: [
          {
            id: 'high-risk-vessel-1',
            name: 'MT Dangerous',
            type: 'tanker',
            tonnage: 100000,
            value: 15000000,
            flag: 'PA',
            yearBuilt: 2005,
          },
        ],
        routes: ['Horn of Africa', 'Strait of Hormuz'],
        riskLevel: 'high',
      },
    ],
    loading: false,
    error: null,
  },
  parameters: {
    docs: {
      description: {
        story: 'High-risk fleet scenario with dangerous routes and older vessels.',
      },
    },
  },
};
```

### Broker Competition Component Stories

```typescript
// src/components/BrokerCompetition/BrokerCompetition.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { BrokerCompetition } from './BrokerCompetition';
import { mockBrokerResponses } from '../../test/fixtures/broker-fixtures';

const meta: Meta<typeof BrokerCompetition> = {
  title: 'Maritime Insurance/Broker Competition',
  component: BrokerCompetition,
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component: 'Broker Competition component for real-time quote comparison from multiple maritime insurance brokers.',
      },
    },
  },
  argTypes: {
    onCompetitionStart: { action: 'competition-started' },
    onQuoteReceived: { action: 'quote-received' },
    onQuoteSelected: { action: 'quote-selected' },
  },
};

export default meta;
type Story = StoryObj<typeof BrokerCompetition>;

export const Initial: Story = {
  args: {
    competitionActive: false,
    brokerResponses: [],
    loading: false,
    error: null,
  },
};

export const CompetitionInProgress: Story = {
  args: {
    competitionActive: true,
    brokerResponses: mockBrokerResponses.slice(0, 2),
    loading: true,
    error: null,
    expectedResponses: 5,
  },
};

export const AllResponsesReceived: Story = {
  args: {
    competitionActive: true,
    brokerResponses: mockBrokerResponses,
    loading: false,
    error: null,
    expectedResponses: 5,
  },
};

export const CompetitionComplete: Story = {
  args: {
    competitionActive: false,
    brokerResponses: mockBrokerResponses,
    loading: false,
    error: null,
    selectedQuote: mockBrokerResponses[0],
  },
};

export const NoResponses: Story = {
  args: {
    competitionActive: false,
    brokerResponses: [],
    loading: false,
    error: 'No broker responses received',
  },
};
```

## AI-Assisted Storybook Development

### AI Tools for Storybook Development

While Storybook itself doesn't have built-in AI features, developers can leverage various AI tools to assist with Storybook development:

#### 1. GitHub Copilot
- **Story generation**: Assists in writing component stories based on existing patterns
- **Props documentation**: Helps generate comprehensive argTypes definitions
- **Test scenarios**: Suggests edge cases and testing scenarios

#### 2. ChatGPT/Claude
- **Component documentation**: Generate detailed component descriptions
- **Story planning**: Help identify important story variations to include
- **Accessibility recommendations**: Suggest accessibility improvements

#### 3. Codeium/Tabnine
- **Auto-completion**: Speed up story writing with intelligent code completion
- **Pattern recognition**: Suggest story patterns based on your codebase

### Example: Using AI Tools for Story Development

```typescript
// Example workflow using AI assistance (conceptual)

// 1. Start with your component
// src/components/FleetManagement/FleetManagement.tsx

// 2. Use AI tools to help generate comprehensive stories:
// - Open your AI assistant (Copilot, Codeium, etc.)
// - Provide context about the component
// - Request story variations based on:
//   * Component props and their types
//   * Common use cases
//   * Error states
//   * Loading states
//   * Edge cases

// 3. Review and customize the generated stories
// 4. Add domain-specific context (maritime insurance)
// 5. Ensure all stories follow your team's conventions
```

### Best Practices for AI-Assisted Development

1. **Always review AI suggestions**: Ensure generated code follows your standards
2. **Add domain context**: Customize examples with real maritime insurance scenarios
3. **Validate accessibility**: Check that AI suggestions meet accessibility standards
4. **Test thoroughly**: Verify all generated stories work correctly
5. **Document manually**: Add human-written documentation for complex behaviors

## Advanced Storybook Features

### Custom Decorators

```typescript
// .storybook/decorators.tsx
import React from 'react';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { MaritimeInsuranceProvider } from '../src/contexts/MaritimeInsuranceContext';

// Maritime Insurance Context Decorator
export const withMaritimeContext = (Story: any) => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
      mutations: { retry: false },
    },
  });

  return (
    <BrowserRouter>
      <QueryClientProvider client={queryClient}>
        <MaritimeInsuranceProvider>
          <Story />
        </MaritimeInsuranceProvider>
      </QueryClientProvider>
    </BrowserRouter>
  );
};

// Responsive Design Decorator
export const withResponsiveLayout = (Story: any) => (
  <div style={{ 
    padding: '20px', 
    maxWidth: '1200px', 
    margin: '0 auto',
    backgroundColor: 'var(--background-color)',
    minHeight: '100vh'
  }}>
    <Story />
  </div>
);

// Dark Mode Decorator
export const withDarkMode = (Story: any, context: any) => {
  const theme = context.globals.theme || 'light';
  
  return (
    <div className={`theme-${theme}`}>
      <Story />
    </div>
  );
};
```

### Custom Addon for Maritime Insurance

```typescript
// .storybook/addons/maritime-addon/index.ts
import { addons, types } from '@storybook/addons';
import { MaritimePanel } from './MaritimePanel';

const ADDON_ID = 'maritime-insurance-addon';
const PANEL_ID = `${ADDON_ID}/panel`;

addons.register(ADDON_ID, () => {
  addons.add(PANEL_ID, {
    type: types.PANEL,
    title: 'Maritime Insurance',
    render: ({ active, key }) => (
      <MaritimePanel active={active} key={key} />
    ),
  });
});
```

### Visual Testing Integration

#### Chromatic (Visual Regression Testing Service)

Chromatic is a cloud-based visual testing service built specifically for Storybook. It captures screenshots of your stories and compares them across commits to catch visual regressions.

**Note**: Chromatic is a paid service with a free tier (5,000 snapshots/month). Pricing scales based on snapshot usage.

```bash
# Installation
npm install --save-dev chromatic
# or
pnpm add -D chromatic
```

```typescript
// package.json - Chromatic integration
{
  "scripts": {
    "chromatic": "chromatic --project-token=<your-project-token>",
    "chromatic:ci": "chromatic --project-token=$CHROMATIC_PROJECT_TOKEN --exit-zero-on-changes"
  },
  "devDependencies": {
    "chromatic": "^11.0.0"
  }
}

// chromatic.config.json - Chromatic configuration
{
  "projectId": "your-project-id",
  "onlyChanged": true,
  "exitZeroOnChanges": true,
  "autoAcceptChanges": "main",
  "skip": ["*.stories.skip.js"],
  "externals": ["public/**"]
}
```

#### Alternative: Storybook Test Runner (Free)

For teams that prefer open-source solutions, Storybook provides a test runner that can perform visual regression testing locally:

```bash
# Installation
npm install --save-dev @storybook/test-runner
```

```typescript
// .storybook/test-runner.ts
import { TestRunnerConfig } from '@storybook/test-runner';

const config: TestRunnerConfig = {
  // Run visual tests on all stories
  async postRender(page, context) {
    // Take a screenshot of the story
    await page.screenshot({ path: `screenshots/${context.id}.png` });
  },
};

export default config;
```

## Design System Integration

### Design Tokens

```typescript
// src/design-system/tokens.ts
export const maritimeDesignTokens = {
  colors: {
    primary: {
      50: '#E6F3FF',
      100: '#B3DAFF',
      500: '#003366',
      900: '#001A33',
    },
    secondary: {
      50: '#F0F8FF',
      500: '#0066CC',
      900: '#004499',
    },
    danger: {
      50: '#FFF5F5',
      500: '#DC2626',
      900: '#991B1B',
    },
    warning: {
      50: '#FFFBEB',
      500: '#F59E0B',
      900: '#92400E',
    },
    success: {
      50: '#F0FDF4',
      500: '#059669',
      900: '#064E3B',
    },
  },
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px',
    xxl: '48px',
  },
  typography: {
    fontFamily: {
      sans: ['Inter', 'system-ui', 'sans-serif'],
      mono: ['Fira Code', 'monospace'],
    },
    fontSize: {
      xs: '12px',
      sm: '14px',
      base: '16px',
      lg: '18px',
      xl: '20px',
      '2xl': '24px',
      '3xl': '32px',
    },
  },
  breakpoints: {
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
  },
};

// Storybook integration
export const storybookTheme = {
  ...maritimeDesignTokens,
  base: 'light',
  brandTitle: 'Maritime Insurance Design System',
  brandUrl: 'https://maritime-insurance-app.com',
  brandImage: '/logo.png',
};
```

## Team Integration

### Development Team Usage

#### Head of Engineering
- **Design system oversight**: Monitor component consistency and standards
- **Documentation review**: Ensure components are properly documented
- **Quality assurance**: Review component stories for completeness

#### Lead Frontend Developer
- **Component development**: Create and maintain component stories
- **Visual testing**: Implement visual regression testing
- **Performance monitoring**: Track component performance metrics

#### Lead Backend Developer
- **API integration stories**: Document API-dependent components
- **Data validation**: Test components with various data scenarios
- **Error handling**: Create error state stories

#### UI/UX Engineer
- **Design system management**: Maintain design tokens and guidelines
- **Accessibility testing**: Ensure components meet accessibility standards
- **Visual design**: Create and maintain visual design documentation

## Best Practices

### Story Organization
- **Consistent naming**: Use clear, descriptive story names
- **Logical grouping**: Group related stories by feature or component type
- **Comprehensive coverage**: Include all component states and variations
- **Documentation**: Add detailed descriptions for complex components

### Component Development
- **Isolated components**: Ensure components work independently
- **Props documentation**: Document all props with proper types
- **Accessibility**: Include accessibility considerations in all stories
- **Responsive design**: Test components across different screen sizes

### Testing Integration
- **Visual regression**: Use Chromatic for visual testing
- **Accessibility testing**: Include a11y addon for accessibility checks
- **Interaction testing**: Test component interactions and user flows
- **Performance testing**: Monitor component performance metrics

## CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/storybook.yml
name: Storybook

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  storybook:
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
        
      - name: Build Storybook
        run: pnpm run storybook:build
        
      - name: Run visual tests
        run: pnpm run chromatic
        env:
          CHROMATIC_PROJECT_TOKEN: ${{ secrets.CHROMATIC_PROJECT_TOKEN }}
          
      - name: Deploy to Storybook
        if: github.ref == 'refs/heads/main'
        run: pnpm run storybook:deploy
```

---

**Monthly Cost**: $0 (Open Source)  
**AI Integration**: ✅ Compatible with AI development assistants (Copilot, Codeium, etc.)  
**Visual Testing**: ✅ Chromatic integration available (separate subscription)  
**Design System**: ✅ Maritime insurance component library  
**Testing Addons**: ✅ Accessibility, interactions, viewport testing included