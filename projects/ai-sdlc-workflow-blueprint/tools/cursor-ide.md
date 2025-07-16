# Cursor IDE - AI-Powered Development Environment

## Overview

Cursor is an AI-first code editor built on top of VS Code that integrates AI capabilities directly into the development workflow. It provides AI-powered code generation, editing, and understanding features that can significantly enhance developer productivity. The maritime insurance application team can leverage Cursor's AI features to accelerate development while maintaining code quality.

## Key Benefits

### AI-First Development
- **Built-in AI chat** for code generation and questions
- **Inline AI editing** with Cmd+K (Mac) or Ctrl+K (Windows/Linux)
- **Natural language to code** conversion for rapid prototyping
- **AI-powered code completion** with context awareness

### Enhanced Productivity
- **Code explanations** for understanding complex logic
- **Multi-file editing** with codebase-wide context
- **Smart code suggestions** based on your codebase patterns
- **Terminal integration** for AI-assisted command line operations

## Installation and Setup

### Basic Installation

```bash
# Download Cursor IDE from the official website
# Visit https://cursor.sh and download for your platform

# macOS
# 1. Download Cursor.dmg from https://cursor.sh
# 2. Open the DMG file and drag Cursor to Applications folder
# 3. Launch Cursor from Applications

# Windows
# 1. Download Cursor installer from https://cursor.sh
# 2. Run the installer and follow the prompts
# 3. Launch Cursor from Start Menu

# Linux
# 1. Download the appropriate package (.deb, .rpm, or .AppImage) from https://cursor.sh
# 2. Install using your package manager or run the AppImage
# Example for Debian/Ubuntu:
# sudo dpkg -i cursor-*.deb
```

### Initial Configuration

Cursor uses VS Code settings with additional AI-specific configurations. Key settings to configure:

1. **Model Selection**: 
   - Open Settings (Cmd+, on Mac, Ctrl+, on Windows/Linux)
   - Navigate to Cursor Settings
   - Select your preferred AI model (GPT-4, Claude 3.5 Sonnet, etc.)

2. **Privacy Settings**:
   - Choose whether to enable codebase indexing
   - Configure which files should be excluded from AI context
   - Set up API key if using your own OpenAI/Anthropic account

3. **Editor Settings** (standard VS Code settings):
```json
// settings.json
{
  "editor.fontSize": 14,
  "editor.fontFamily": "Fira Code, monospace",
  "editor.fontLigatures": true,
  "editor.formatOnSave": true,
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  "typescript.preferences.importModuleSpecifier": "relative",
  "typescript.suggest.autoImports": true,
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 1000,
  "workbench.colorTheme": "One Dark Pro",
  "workbench.iconTheme": "material-icon-theme",
  "terminal.integrated.defaultProfile.osx": "zsh",
  "terminal.integrated.fontSize": 12,
  "extensions.autoUpdate": true,
  "security.workspace.trust.untrustedFiles": "open"
}
```

## Maritime Insurance Development Features

### AI-Powered Code Generation

#### Using Cursor for Component Generation

To generate code in Cursor:
1. Press Cmd+K (Mac) or Ctrl+K (Windows/Linux) to open inline edit
2. Type your request in natural language
3. Review and accept the generated code

Example - Fleet Management Component:

```typescript
// Using Cursor's inline edit (Cmd+K):
// "Create a React component for managing maritime insurance fleets with TypeScript"
// Cursor generates:

import React, { useState, useEffect } from 'react';
import { Fleet, Vessel, VesselType } from '@/types/maritime-insurance';
import { useFleetData } from '@/hooks/useFleetData';
import { Button } from '@/components/ui/Button';
import { Card } from '@/components/ui/Card';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';

interface FleetManagementProps {
  onFleetCreate: (fleet: Omit<Fleet, 'id'>) => void;
  onFleetUpdate: (id: string, fleet: Partial<Fleet>) => void;
  onFleetDelete: (id: string) => void;
}

/**
 * FleetManagement component for maritime insurance application
 * Handles fleet creation, editing, and vessel management
 */
export const FleetManagement: React.FC<FleetManagementProps> = ({
  onFleetCreate,
  onFleetUpdate,
  onFleetDelete,
}) => {
  const [fleets, setFleets] = useState<Fleet[]>([]);
  const [selectedFleet, setSelectedFleet] = useState<Fleet | null>(null);
  const [isAddingFleet, setIsAddingFleet] = useState(false);
  const [newFleet, setNewFleet] = useState<Partial<Fleet>>({
    name: '',
    type: 'cargo',
    vessels: [],
  });

  const { loadFleets, createFleet, updateFleet, deleteFleet } = useFleetData();

  useEffect(() => {
    loadFleets().then(setFleets);
  }, [loadFleets]);

  const handleFleetCreate = async () => {
    if (newFleet.name && newFleet.type) {
      const fleet = await createFleet(newFleet as Omit<Fleet, 'id'>);
      setFleets(prev => [...prev, fleet]);
      onFleetCreate(fleet);
      setNewFleet({ name: '', type: 'cargo', vessels: [] });
      setIsAddingFleet(false);
    }
  };

  const handleVesselAdd = (vessel: Omit<Vessel, 'id'>) => {
    if (selectedFleet) {
      const updatedFleet = {
        ...selectedFleet,
        vessels: [...selectedFleet.vessels, { ...vessel, id: generateVesselId() }],
      };
      setSelectedFleet(updatedFleet);
      onFleetUpdate(selectedFleet.id, updatedFleet);
    }
  };

  return (
    <div className="fleet-management">
      <div className="fleet-header">
        <h2>Fleet Management</h2>
        <Button onClick={() => setIsAddingFleet(true)}>Add New Fleet</Button>
      </div>

      {isAddingFleet && (
        <Card className="add-fleet-form">
          <h3>Create New Fleet</h3>
          <Input
            placeholder="Fleet Name"
            value={newFleet.name || ''}
            onChange={(e) => setNewFleet({ ...newFleet, name: e.target.value })}
          />
          <Select
            value={newFleet.type}
            onChange={(value) => setNewFleet({ ...newFleet, type: value as VesselType })}
          >
            <option value="cargo">Cargo</option>
            <option value="tanker">Tanker</option>
            <option value="container">Container</option>
            <option value="bulk">Bulk</option>
          </Select>
          <div className="form-actions">
            <Button onClick={handleFleetCreate}>Create Fleet</Button>
            <Button variant="secondary" onClick={() => setIsAddingFleet(false)}>
              Cancel
            </Button>
          </div>
        </Card>
      )}

      <div className="fleet-list">
        {fleets.map(fleet => (
          <FleetCard
            key={fleet.id}
            fleet={fleet}
            onSelect={() => setSelectedFleet(fleet)}
            onDelete={() => onFleetDelete(fleet.id)}
            isSelected={selectedFleet?.id === fleet.id}
          />
        ))}
      </div>

      {selectedFleet && (
        <VesselManagement
          fleet={selectedFleet}
          onVesselAdd={handleVesselAdd}
          onVesselUpdate={(vesselId, updates) => {
            // Handle vessel updates
          }}
        />
      )}
    </div>
  );
};

function generateVesselId(): string {
  return `vessel-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}
```

### AI-Powered Code Explanation

To get code explanations in Cursor:
1. Select the code you want explained
2. Open the AI chat panel (Cmd+L on Mac, Ctrl+L on Windows/Linux)
3. Ask for an explanation

```typescript
// Select the function and ask in Cursor chat: "Explain this risk calculation"
// Cursor provides explanation:

/**
 * AI Explanation:
 * This function calculates the overall risk score for a maritime insurance quote
 * based on multiple risk factors including vessel characteristics, route dangers,
 * and operational patterns.
 * 
 * Risk Factors:
 * - Vessel age and condition (older vessels = higher risk)
 * - Route piracy and weather risks (dangerous routes = higher premiums)
 * - Cargo type and value (hazardous cargo = additional coverage needed)
 * - Operational history (claims history affects future premiums)
 * 
 * The function returns a normalized risk score between 0-1 where:
 * - 0.0-0.3: Low risk (favorable rates)
 * - 0.3-0.7: Medium risk (standard rates)
 * - 0.7-1.0: High risk (premium rates, additional conditions)
 */
function calculateRiskScore(
  vessel: Vessel,
  route: Route,
  cargo: CargoDetails,
  history: OperationalHistory
): number {
  // AI explains each calculation step...
}
```

### AI-Assisted Debugging

Using Cursor for debugging:
1. When you encounter an error, select the problematic code
2. Use Cmd+K (inline edit) or open chat with Cmd+L
3. Describe the error or paste the error message

```typescript
// Example: Select error code and use Cursor chat
// "I'm getting a TypeError: Cannot read property 'pirateRisk' of undefined"
// Cursor analyzes and suggests:

/*
AI Analysis:
The error occurs because the route risk calculation is trying to access 
`route.pirateRisk` but the API response structure has changed.

Issue: Property 'pirateRisk' doesn't exist on type 'Route'
New structure: route.risks.piracy.level

Fix suggestions:
1. Update the risk calculation to use the new API structure
2. Add proper error handling for missing risk data
3. Implement type guards to prevent runtime errors
*/

// Before (causing error):
const pirateRisk = route.pirateRisk || 0;

// After (AI suggested fix):
const pirateRisk = route.risks?.piracy?.level || 0;

// AI also suggests adding type safety:
function getPirateRisk(route: Route): number {
  if (!route.risks || !route.risks.piracy) {
    console.warn(`Missing piracy risk data for route ${route.name}`);
    return 0;
  }
  return route.risks.piracy.level;
}
```

## Team Collaboration Features

### Using Cursor Rules for Project Context

Cursor allows you to define project-specific rules that guide AI behavior. Create a `.cursorrules` file in your project root:

```markdown
# .cursorrules
You are working on a maritime insurance application. Key context:

## Domain Knowledge
- Primary entities: Fleet, Vessel, Quote, Policy, Broker
- Key processes: quote generation, risk assessment, broker competition
- Regulations to consider: IMO, SOLAS, MARPOL

## Code Standards
- Use TypeScript with strict type checking
- Follow the existing project structure and naming conventions
- Implement comprehensive error handling
- Write unit tests for all business logic

## Architecture
- Frontend: React with TypeScript
- Backend: FastAPI (Python) or Express (Node.js)
- Database: PostgreSQL with proper indexing
- Follow microservices patterns where appropriate

## Best Practices
- Use meaningful variable names from the maritime insurance domain
- Add JSDoc comments for complex business logic
- Ensure all API endpoints have proper validation
- Consider performance for large fleet datasets
```

### Team-Specific AI Workflows

#### Head of Engineering Workflow

Using Cursor for architecture and code reviews:
- Review pull requests with AI assistance
- Generate architecture documentation
- Analyze code for patterns and anti-patterns

```typescript
// In Cursor chat: "Generate an architecture review checklist for our maritime insurance quote service"
// Cursor generates relevant checklist based on codebase context:

interface ArchitectureReviewChecklist {
  performance: {
    quoteGeneration: 'Response time < 2 seconds';
    brokerCompetition: 'Handle 10+ concurrent broker requests';
    fleetLoading: 'Support 1000+ vessels per fleet';
  };
  security: {
    dataEncryption: 'All sensitive data encrypted at rest and in transit';
    authentication: 'Multi-factor authentication for all users';
    authorization: 'Role-based access control implemented';
  };
  scalability: {
    horizontalScaling: 'Stateless services for horizontal scaling';
    databaseOptimization: 'Query optimization for large datasets';
    caching: 'Redis caching for frequently accessed data';
  };
  compliance: {
    dataProtection: 'GDPR compliance for customer data';
    auditTrail: 'Complete audit trail for all transactions';
    regulatoryReporting: 'Support for regulatory reporting requirements';
  };
}
```

#### Frontend Lead Workflow

Using Cursor for React development:
- Generate components with Cmd+K inline editing
- Get suggestions for responsive design patterns
- Refactor components for better performance

```typescript
// Using Cmd+K: "Create a responsive broker competition display component"
// Cursor generates component structure with best practices:

const BrokerCompetitionDisplay: React.FC = () => {
  // Cursor will generate a complete component based on:
  // - Your existing component patterns
  // - Project styling conventions
  // - TypeScript interfaces already defined
  // - Accessibility requirements
};
```

#### Backend Lead Workflow

Using Cursor for API development:
- Generate API endpoints with proper validation
- Create database models and migrations
- Implement business logic with error handling

```typescript
// In Cursor chat: "Create a FastAPI endpoint for vessel risk assessment"
// Cursor generates based on your existing patterns:

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import asyncio
from datetime import datetime

class RiskAssessmentService:
    """
    AI-generated maritime insurance risk assessment service
    Handles vessel risk, route risk, and operational risk calculations
    """
    
    async def calculate_comprehensive_risk(
        self, 
        vessel: VesselModel, 
        route: RouteModel,
        cargo: CargoModel
    ) -> RiskAssessmentResult:
        # AI generates complete risk calculation logic
        pass
```

#### UI/UX Engineer Workflow

Using Cursor for accessible UI development:
- Generate accessible components with ARIA attributes
- Get suggestions for keyboard navigation
- Create responsive layouts with CSS-in-JS

```typescript
// Using Cmd+K: "Add accessibility features to this form component"
// Cursor enhances existing components with:
// - Proper ARIA labels
// - Keyboard navigation
// - Focus management
// - Error announcements for screen readers
```

## Advanced Cursor Features

### Code Refactoring

To refactor code in Cursor:
1. Select the code to refactor
2. Press Cmd+K (Mac) or Ctrl+K (Windows/Linux)
3. Describe the refactoring you want

```typescript
// Select component and use Cmd+K: "Refactor to use React Query"
// Cursor suggests refactoring:

// Before: Manual state management
const [fleets, setFleets] = useState<Fleet[]>([]);
const [loading, setLoading] = useState(true);
const [error, setError] = useState<string | null>(null);

// After: AI-suggested React Query implementation
const {
  data: fleets,
  isLoading,
  error,
  refetch,
} = useQuery({
  queryKey: ['fleets'],
  queryFn: () => fleetService.getAllFleets(),
  staleTime: 5 * 60 * 1000, // 5 minutes
  cacheTime: 10 * 60 * 1000, // 10 minutes
});
```

### Test Generation

Using Cursor to generate tests:
1. Select the function or component to test
2. Use Cmd+K: "Generate unit tests for this function"
3. Cursor creates tests based on your testing framework

```typescript
// Select a function and use Cmd+K: "Write Jest tests for this quote calculation"
// Cursor generates:

describe('QuoteGenerationService', () => {
  // AI generates complete test suite with:
  // - Unit tests for all methods
  // - Integration tests with external services
  // - Edge cases and error scenarios
  // - Maritime insurance specific test data
  // - Performance benchmarks
  // - Security vulnerability tests
});
```

### Documentation Generation

Using Cursor for documentation:
1. Select code that needs documentation
2. Use Cmd+K: "Add JSDoc comments" or "Generate API documentation"
3. Cursor adds appropriate documentation

```typescript
// Select an API endpoint and use Cmd+K: "Add OpenAPI documentation"
// Cursor generates:

/**
 * @swagger
 * /api/fleets:
 *   get:
 *     summary: Get all fleets
 *     description: Retrieve all maritime insurance fleets with optional filtering
 *     parameters:
 *       - name: type
 *         in: query
 *         schema:
 *           type: string
 *           enum: [cargo, tanker, container, bulk]
 *         description: Filter by vessel type
 *     responses:
 *       200:
 *         description: List of fleets
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 $ref: '#/components/schemas/Fleet'
 */
```

## Performance Optimization

### Using Cursor for Performance Analysis

To analyze performance issues:
1. Select the component or function
2. Ask in chat: "Analyze this for performance issues"
3. Cursor identifies potential bottlenecks

```typescript
// In Cursor chat with selected code: "Find performance bottlenecks"
// Cursor identifies:

/*
Performance Analysis:
1. Unnecessary re-renders: FleetCard components re-render on every fleet list update
2. Inefficient filtering: Array.filter() called on every render
3. Missing memoization: Expensive calculations not memoized
4. Large bundle size: Importing entire lodash library

Optimization suggestions:
*/

// Before: Performance issues
const filteredFleets = fleets.filter(fleet => 
  fleet.type === selectedType && 
  fleet.vessels.length > minVessels
);

// After: AI-optimized version
const filteredFleets = useMemo(() => 
  fleets.filter(fleet => 
    fleet.type === selectedType && 
    fleet.vessels.length > minVessels
  ), [fleets, selectedType, minVessels]
);
```

### Codebase-Wide Analysis

Cursor can analyze your entire codebase:
1. Open chat with Cmd+L
2. Ask questions about your codebase structure
3. Get suggestions for improvements

```typescript
// In Cursor chat: "What are the largest dependencies in our bundle?"
// Cursor analyzes package.json and imports:

/*
Bundle Analysis Results:
- Total bundle size: 2.3MB (Target: <1MB)
- Largest dependencies: 
  - lodash: 500KB (Use lodash-es with tree shaking)
  - date-fns: 300KB (Use date-fns with selective imports)
  - chart.js: 250KB (Consider lighter alternative)

Optimization Plan:
1. Implement code splitting by route
2. Use dynamic imports for heavy components
3. Optimize image assets with WebP format
4. Enable gzip compression
*/
```

## Development Workflow Integration

### Using Cursor with Git

Cursor includes Git integration similar to VS Code:
- View file changes in the source control panel
- Stage and commit changes
- Use AI to generate commit messages

```bash
# When committing in Cursor:
# 1. Stage your changes in the Source Control panel
# 2. Click the AI icon next to the commit message box
# 3. Cursor generates a commit message based on your changes
# Example generated messages:
# "feat(fleet-management): add vessel filtering and sorting capabilities"
# "fix(quote-generation): resolve race condition in broker competition"
# "refactor(risk-calculation): improve performance with memoization"
```

### Terminal Integration

Cursor's terminal supports AI assistance:
- Ask for command suggestions
- Debug error messages
- Get explanations for command outputs

```bash
# In Cursor terminal, you can ask:
# "How do I run tests for a specific file?"
# "What does this error mean?"
# "Generate a curl command to test my API endpoint"
```

## Team Training and Onboarding

### Getting Started with Cursor

For new team members:

1. **Install Cursor** from https://cursor.sh
2. **Import VS Code settings** if migrating from VS Code
3. **Configure AI preferences** in Settings
4. **Create .cursorrules** file for project context

### Key Shortcuts to Learn

- **Cmd+K / Ctrl+K**: Inline code generation and editing
- **Cmd+L / Ctrl+L**: Open AI chat for questions
- **Cmd+Shift+L / Ctrl+Shift+L**: Add file to chat context
- **Tab**: Accept AI suggestions

### Effective Cursor Usage Tips

1. **Be specific in prompts**: Instead of "fix this", say "add error handling for network failures"
2. **Use codebase context**: Cursor understands your project structure
3. **Iterate on generations**: You can refine AI outputs with follow-up requests
4. **Review AI code**: Always review generated code for business logic accuracy

### Example Learning Path

```markdown
## Week 1: Basic Cursor Features
- Practice inline editing with Cmd+K
- Use chat for code explanations
- Generate simple components

## Week 2: Advanced Features
- Multi-file edits and refactoring
- Test generation
- Documentation creation

## Week 3: Team Workflows
- Collaborate using shared .cursorrules
- Code review with AI assistance
- Performance optimization
```

## Best Practices

### AI Usage Guidelines
- **Provide context**: Include relevant files in chat for better suggestions
- **Review generated code**: Always verify AI-generated code meets requirements
- **Use .cursorrules**: Define project-specific rules for consistent AI behavior
- **Iterate on prompts**: Refine your requests for better results

### Team Collaboration
- **Share .cursorrules**: Keep project rules in version control
- **Document AI patterns**: Share effective prompts and techniques
- **Code review**: Use AI to help review PRs but maintain human oversight
- **Consistent style**: Configure Cursor to follow team coding standards

### Security Considerations
- **API keys**: Use your own API keys for sensitive projects
- **Privacy mode**: Disable codebase indexing for proprietary code
- **Review permissions**: Understand what code Cursor can access
- **Compliance**: Ensure AI usage meets your organization's policies

## Pricing and Plans

### Cursor Pricing (as of 2024)

**Free Plan**:
- Limited AI requests (approximately 50/month)
- GPT-3.5 model access
- Basic features

**Pro Plan** ($20/month):
- 500 fast requests with GPT-4
- Unlimited slow requests
- Claude 3.5 Sonnet access
- Advanced features and priority support

**Business Plan** (Contact for pricing):
- Team management features
- Enhanced security options
- Custom model selection
- Priority support

### Cost-Benefit Analysis for Maritime Insurance Team

**Benefits**:
- Faster feature development (estimated 30-50% productivity gain)
- Reduced debugging time with AI assistance
- Better code consistency across team
- Improved onboarding for new developers

**ROI Calculation**:
- 4 developers × $20/month = $80/month
- Time saved: ~40 hours/month across team
- Value of time saved far exceeds tool cost

---

**Monthly Cost**: Free (limited) / $20 per developer (Pro)  
**AI Models**: GPT-4, Claude 3.5 Sonnet, GPT-3.5  
**VS Code Compatible**: ✅ Built on VS Code, supports extensions  
**Team Features**: ✅ Shared rules and project context