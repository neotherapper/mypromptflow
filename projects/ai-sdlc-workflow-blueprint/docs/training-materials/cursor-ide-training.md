# Cursor IDE Training Guide for Maritime Insurance Development

## Course Overview

This comprehensive training guide provides hands-on instruction for using Cursor IDE in maritime insurance software development. The course progresses from basic setup to advanced AI-assisted development techniques, with practical exercises throughout.

### Target Audience
- Software developers new to AI-assisted coding
- Maritime insurance domain specialists transitioning to development
- Teams adopting Cursor IDE for insurance projects
- Technical leads evaluating AI development tools

### Prerequisites
- Basic programming knowledge (any language)
- Familiarity with version control (Git)
- Understanding of maritime insurance concepts (helpful but not required)

### Learning Outcomes
By completing this training, participants will be able to:
- Install and configure Cursor IDE for maritime insurance development
- Utilize AI assistance for code generation and problem-solving
- Develop insurance-specific components efficiently
- Implement best practices for AI-assisted development
- Troubleshoot common issues and optimize performance

---

## Module 1: Getting Started with Cursor IDE

### Learning Objectives
- Install and configure Cursor IDE
- Navigate the interface effectively
- Understand pricing models and feature sets
- Set up a maritime insurance project

### 1.1 Installation and Setup

#### System Requirements
- **Operating Systems**: macOS 10.15+, Windows 10+, Linux (Ubuntu 20.04+)
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 2GB free space
- **Internet**: Required for AI features

#### Installation Steps

1. **Download Cursor IDE**
   ```bash
   # Visit https://cursor.sh
   # Download appropriate version for your OS
   # macOS: Cursor-darwin-x64.dmg or Cursor-darwin-arm64.dmg
   # Windows: Cursor-win32-x64.exe
   # Linux: Cursor-linux-x64.AppImage
   ```

2. **Initial Setup**
   - Launch Cursor IDE
   - Sign in with GitHub or email
   - Choose workspace location
   - Configure initial preferences

3. **License Activation**
   - Free tier: Automatic activation
   - Pro tier: Enter license key from account dashboard

#### Exercise 1.1: Basic Installation
**Task**: Install Cursor IDE and create your first project
1. Download and install Cursor IDE
2. Create a new folder: `maritime-insurance-app`
3. Open the folder in Cursor
4. Create a file: `README.md`
5. Save and verify installation

**Success Criteria**: 
- Cursor IDE launches without errors
- Project folder opens correctly
- File creation and saving works

### 1.2 Interface Basics and Navigation

#### Key Interface Elements

1. **Activity Bar** (Left side)
   - Explorer: File navigation
   - Search: Find across files
   - Source Control: Git integration
   - Run and Debug: Execution tools
   - Extensions: Add-on management

2. **Editor Area** (Center)
   - Code editing pane
   - Tab management
   - Split view capabilities
   - Minimap navigation

3. **Side Bar** (Contextual)
   - File explorer tree
   - Search results
   - Git changes
   - Debug console

4. **Panel** (Bottom)
   - Terminal
   - Problems
   - Output
   - Debug Console

#### Essential Keyboard Shortcuts

| Action | macOS | Windows/Linux |
|--------|-------|---------------|
| AI Chat | Cmd+L | Ctrl+L |
| AI Edit | Cmd+K | Ctrl+K |
| Command Palette | Cmd+Shift+P | Ctrl+Shift+P |
| Quick Open | Cmd+P | Ctrl+P |
| Toggle Terminal | Cmd+` | Ctrl+` |
| Find in Files | Cmd+Shift+F | Ctrl+Shift+F |

#### Exercise 1.2: Interface Navigation
**Task**: Navigate Cursor IDE efficiently
1. Open Command Palette and search for "theme"
2. Change to a different color theme
3. Split the editor into two panes
4. Open integrated terminal
5. Use Quick Open to find files

**Success Criteria**:
- Successfully change theme
- Work with split editors
- Navigate using keyboard shortcuts

### 1.3 Understanding Pricing Tiers

#### Free Tier Features
- **Basic AI assistance**: Limited requests per month
- **Code completion**: Standard suggestions
- **Single file context**: AI understands current file
- **Community support**: Forums and documentation

#### Pro Tier ($20/month)
- **Unlimited AI requests**: No monthly limits
- **Advanced models**: GPT-4 and Claude access
- **Multi-file context**: Project-wide understanding
- **Priority support**: Direct assistance
- **Team features**: Collaboration tools
- **Custom instructions**: Personalized AI behavior

#### Choosing the Right Tier

**Free Tier Suitable For**:
- Individual learning
- Small personal projects
- Evaluation purposes
- Occasional AI assistance

**Pro Tier Recommended For**:
- Professional development
- Team projects
- Complex applications
- Daily AI-assisted coding

#### Exercise 1.3: Feature Exploration
**Task**: Explore tier differences
1. Check current tier in settings
2. Review AI request limits
3. Test code completion features
4. Document observed limitations

**Success Criteria**:
- Understand current tier capabilities
- Identify upgrade benefits
- Make informed tier decision

---

## Module 2: Core Features and Capabilities

### Learning Objectives
- Master AI-assisted coding commands
- Utilize code completion effectively
- Leverage multi-file context understanding
- Apply AI debugging assistance

### 2.1 AI-Assisted Coding with Cmd+K and Cmd+L

#### Cmd+K (AI Edit Mode)

**Purpose**: Direct code generation and modification

**Usage Pattern**:
1. Select code or position cursor
2. Press Cmd+K (macOS) or Ctrl+K (Windows/Linux)
3. Type instruction in natural language
4. Review and accept changes

**Example: Maritime Insurance Policy Class**
```python
# Position cursor here and press Cmd+K
# Type: "Create a maritime insurance policy class with vessel details, coverage types, and premium calculation"

# Generated code:
class MaritimeInsurancePolicy:
    def __init__(self, policy_number, vessel_details, coverage_types):
        self.policy_number = policy_number
        self.vessel_details = vessel_details
        self.coverage_types = coverage_types
        self.premium = 0
        
    def calculate_premium(self):
        base_rate = 0.005  # 0.5% of vessel value
        risk_factors = self._assess_risk_factors()
        self.premium = self.vessel_details['value'] * base_rate * risk_factors
        return self.premium
```

#### Cmd+L (AI Chat Mode)

**Purpose**: Conversational assistance and explanations

**Usage Pattern**:
1. Press Cmd+L (macOS) or Ctrl+L (Windows/Linux)
2. Ask questions or request guidance
3. Copy code suggestions to editor
4. Continue conversation for clarification

**Example Chat Interactions**:
```
User: How do I implement hull and machinery coverage calculations?

AI: Hull and machinery coverage typically includes:
1. Physical damage to vessel
2. Machinery breakdown
3. Collision liability

Here's an implementation:
[Code example provided by AI]
```

#### Exercise 2.1: AI Command Mastery
**Task**: Build a vessel risk assessment module
1. Use Cmd+K to generate a `VesselRiskAssessment` class
2. Add methods for age, type, and route risk factors
3. Use Cmd+L to understand maritime risk categories
4. Implement comprehensive risk scoring

**Success Criteria**:
- Generate working class structure
- Implement at least 5 risk factors
- Understand maritime risk concepts
- Code passes basic tests

### 2.2 Code Completion and Suggestions

#### Inline Suggestions

**Activation**: Start typing and pause briefly

**Best Practices**:
1. Write descriptive function names
2. Add comments before complex logic
3. Use consistent naming conventions
4. Provide context through variable names

**Maritime Example**:
```javascript
// Calculate war risk premium for vessels in high-risk zones
function calculateWarRiskPremium(vessel, route) {
    // Cursor will suggest implementation based on function name and comment
    const highRiskZones = ['Gulf of Aden', 'Strait of Malacca', 'Gulf of Guinea'];
    // Continue typing and watch suggestions
}
```

#### Smart Completions

**Features**:
- Context-aware suggestions
- Import statement generation
- Method signature completion
- Documentation generation

#### Exercise 2.2: Completion Optimization
**Task**: Develop a cargo insurance calculator
1. Create function with descriptive name
2. Add detailed comment about requirements
3. Let Cursor suggest implementation
4. Refine with additional context

**Success Criteria**:
- Accurate suggestions received
- Minimal manual corrections needed
- Efficient development flow

### 2.3 Multi-File Context Understanding

#### Project-Wide Intelligence

**Setup for Best Results**:
1. Organize related files in logical folders
2. Use consistent naming conventions
3. Maintain clear file relationships
4. Document inter-file dependencies

**Folder Structure Example**:
```
maritime-insurance-system/
├── models/
│   ├── policy.js
│   ├── vessel.js
│   └── coverage.js
├── services/
│   ├── underwriting.js
│   ├── claims.js
│   └── risk-assessment.js
├── utils/
│   └── calculations.js
└── tests/
    └── underwriting.test.js
```

#### Context Utilization

**Techniques**:
1. Reference other files in comments
2. Import related modules
3. Use consistent patterns across files
4. Maintain type definitions

**Example**:
```typescript
// In services/underwriting.js
import { Vessel } from '../models/vessel';
import { calculateBasePremium } from '../utils/calculations';

// Cursor understands relationships and suggests appropriate methods
export class UnderwritingService {
    assessVessel(vessel: Vessel) {
        // AI knows vessel structure from import
    }
}
```

#### Exercise 2.3: Multi-File Project
**Task**: Create interconnected insurance modules
1. Create models for Policy, Vessel, and Claim
2. Build services that use multiple models
3. Implement calculations referencing all components
4. Verify cross-file suggestions work

**Success Criteria**:
- Clean file organization
- Proper imports and exports
- AI suggests based on other files
- Coherent system architecture

### 2.4 Debugging Assistance

#### AI-Powered Debugging

**Capabilities**:
1. Error explanation
2. Fix suggestions
3. Stack trace analysis
4. Logic error detection

**Debugging Workflow**:
```javascript
// Example: Debugging premium calculation error
function calculatePremium(policy) {
    // Error: Cannot read property 'value' of undefined
    const basePremium = policy.vessel.value * 0.02;
    
    // Select error, press Cmd+L
    // Ask: "Why am I getting undefined error and how to fix?"
    // AI explains the issue and suggests defensive coding
}
```

#### Common Maritime Insurance Bugs

1. **Null vessel details**
   ```javascript
   // AI suggestion for defensive coding
   const vesselValue = policy?.vessel?.value || 0;
   ```

2. **Invalid coverage combinations**
   ```javascript
   // AI helps validate coverage rules
   if (hasHullCoverage && !hasLiability) {
       throw new Error('Liability coverage required with hull coverage');
   }
   ```

#### Exercise 2.4: Debug and Fix
**Task**: Fix a buggy claims processing module
1. Create a claims processor with intentional bugs
2. Use AI chat to understand errors
3. Apply suggested fixes
4. Add error handling

**Success Criteria**:
- Identify all bugs using AI
- Apply appropriate fixes
- Add comprehensive error handling
- Code runs without errors

---

## Module 3: Maritime Insurance Development

### Learning Objectives
- Structure insurance-specific projects
- Generate domain-specific components
- Implement insurance workflows
- Integrate testing frameworks

### 3.1 Setting Up Project Structure

#### Maritime Insurance Architecture

**Recommended Structure**:
```
maritime-insurance-platform/
├── src/
│   ├── core/
│   │   ├── entities/
│   │   │   ├── Policy.ts
│   │   │   ├── Vessel.ts
│   │   │   ├── Cargo.ts
│   │   │   └── Claim.ts
│   │   ├── value-objects/
│   │   │   ├── Premium.ts
│   │   │   ├── Coverage.ts
│   │   │   └── Deductible.ts
│   │   └── interfaces/
│   │       └── Repository.ts
│   ├── application/
│   │   ├── use-cases/
│   │   │   ├── CreatePolicy.ts
│   │   │   ├── CalculatePremium.ts
│   │   │   └── ProcessClaim.ts
│   │   └── services/
│   │       ├── UnderwritingService.ts
│   │       └── RiskAssessmentService.ts
│   ├── infrastructure/
│   │   ├── persistence/
│   │   ├── external/
│   │   └── config/
│   └── presentation/
│       ├── api/
│       └── web/
├── tests/
├── docs/
└── package.json
```

#### Initial Setup Commands

```bash
# Create project structure using Cursor
# Position in terminal and use Cmd+K with:
# "Create a complete folder structure for maritime insurance platform with domain-driven design"

# Initialize project
npm init -y
npm install typescript @types/node jest @types/jest

# Configure TypeScript
npx tsc --init
```

#### Exercise 3.1: Project Foundation
**Task**: Set up a maritime insurance API project
1. Create recommended folder structure
2. Initialize npm and TypeScript
3. Configure testing framework
4. Create base entity classes

**Success Criteria**:
- Complete project structure
- All configurations working
- Base classes created
- Tests can run

### 3.2 Domain-Specific Code Generation

#### Insurance Entity Generation

**Policy Entity Example**:
```typescript
// Use Cmd+K: "Generate a comprehensive maritime insurance policy entity with all standard fields, methods for premium calculation, and coverage validation"

export class MaritimePolicy {
    private id: string;
    private policyNumber: string;
    private insuredVessel: Vessel;
    private coverageTypes: Coverage[];
    private effectiveDate: Date;
    private expiryDate: Date;
    private premium: Premium;
    private deductibles: Map<string, Deductible>;
    
    constructor(params: PolicyParams) {
        this.validatePolicy(params);
        Object.assign(this, params);
    }
    
    calculatePremium(): Premium {
        const basePremium = this.calculateBasePremium();
        const adjustments = this.applyRiskAdjustments();
        return new Premium(basePremium * adjustments);
    }
    
    private validatePolicy(params: PolicyParams): void {
        if (!params.insuredVessel) {
            throw new Error('Vessel information required');
        }
        // Additional validations
    }
}
```

#### Coverage Types Implementation

```typescript
// Use Cmd+L: "What are the standard maritime insurance coverage types I should implement?"
// Then Cmd+K to generate each type

export enum CoverageType {
    HULL_AND_MACHINERY = 'HULL_AND_MACHINERY',
    PROTECTION_AND_INDEMNITY = 'P&I',
    CARGO = 'CARGO',
    WAR_RISKS = 'WAR_RISKS',
    FREIGHT = 'FREIGHT',
    LOSS_OF_HIRE = 'LOSS_OF_HIRE'
}

export class Coverage {
    constructor(
        private type: CoverageType,
        private limit: number,
        private deductible: number,
        private conditions: string[]
    ) {}
    
    isValid(): boolean {
        return this.limit > this.deductible && this.conditions.length > 0;
    }
}
```

#### Exercise 3.2: Domain Model Creation
**Task**: Build complete vessel assessment system
1. Generate Vessel entity with maritime-specific fields
2. Create VesselType enum with all vessel categories
3. Implement risk scoring based on vessel characteristics
4. Add voyage route risk factors

**Success Criteria**:
- Comprehensive vessel model
- All vessel types covered
- Risk scoring implemented
- Route risks calculated

### 3.3 Component Development Workflows

#### Workflow Pattern: Feature Development

**Step 1: Define Requirements**
```typescript
// In a new file: features/war-risk-premium.md
// Use Cmd+K: "Create a detailed specification for war risk premium calculation feature"
```

**Step 2: Generate Tests First**
```typescript
// In tests/war-risk-premium.test.ts
// Use Cmd+K: "Generate comprehensive tests for war risk premium calculation including edge cases"

describe('War Risk Premium Calculation', () => {
    it('should calculate higher premium for high-risk zones', () => {
        const voyage = new Voyage('Singapore', 'Rotterdam', ['Strait of Malacca']);
        const premium = calculateWarRiskPremium(voyage, vesselValue);
        expect(premium).toBeGreaterThan(baselinePremium);
    });
});
```

**Step 3: Implement Feature**
```typescript
// Use test-driven development with AI assistance
// Cmd+K helps generate implementation that passes tests
```

#### Component Integration Workflow

**API Endpoint Creation**:
```typescript
// In api/policies.ts
// Cmd+K: "Create Express router for maritime policy CRUD operations with validation"

import { Router } from 'express';
import { PolicyService } from '../services/PolicyService';

export const policyRouter = Router();

policyRouter.post('/policies', validatePolicy, async (req, res) => {
    try {
        const policy = await PolicyService.create(req.body);
        res.status(201).json(policy);
    } catch (error) {
        res.status(400).json({ error: error.message });
    }
});
```

#### Exercise 3.3: Feature Implementation
**Task**: Implement claims processing workflow
1. Define claim submission requirements
2. Generate test cases for claims
3. Build claim validation service
4. Create API endpoints
5. Integrate with policy system

**Success Criteria**:
- Tests cover all scenarios
- Validation is comprehensive
- API properly documented
- Integration tested

### 3.4 Testing Integration

#### Test Strategy for Insurance Systems

**Test Categories**:
1. Unit tests for calculations
2. Integration tests for workflows
3. Contract tests for external services
4. E2E tests for critical paths

#### Unit Test Example

```javascript
// tests/premium-calculation.test.js
// Cmd+K: "Generate unit tests for maritime insurance premium calculation with multiple scenarios"

describe('Premium Calculation', () => {
    describe('Base Premium', () => {
        it('should calculate 2% for standard cargo vessels', () => {
            const vessel = new Vessel({ 
                type: 'CARGO', 
                value: 1000000,
                age: 5 
            });
            const premium = calculateBasePremium(vessel);
            expect(premium).toBe(20000);
        });
    });
    
    describe('Risk Adjustments', () => {
        it('should increase premium 50% for vessels over 20 years', () => {
            const vessel = new Vessel({ 
                type: 'CARGO', 
                value: 1000000,
                age: 25 
            });
            const premium = calculateAdjustedPremium(vessel);
            expect(premium).toBe(30000);
        });
    });
});
```

#### Integration Test Pattern

```javascript
// tests/integration/policy-creation.test.js
describe('Policy Creation Workflow', () => {
    it('should create policy with all validations', async () => {
        const policyData = {
            vessel: validVessel,
            coverage: ['HULL', 'P&I'],
            period: 12
        };
        
        const policy = await PolicyService.create(policyData);
        
        expect(policy).toHaveProperty('policyNumber');
        expect(policy.premium).toBeGreaterThan(0);
        expect(policy.status).toBe('ACTIVE');
    });
});
```

#### Exercise 3.4: Comprehensive Testing
**Task**: Build test suite for underwriting module
1. Create unit tests for risk calculations
2. Add integration tests for policy creation
3. Implement validation error tests
4. Generate test data fixtures

**Success Criteria**:
- 80%+ code coverage
- All edge cases tested
- Tests are maintainable
- Fixtures are realistic

---

## Module 4: Advanced Techniques

### Learning Objectives
- Configure .cursorrules for team standards
- Create custom prompts and workflows
- Integrate with external tools
- Optimize AI performance

### 4.1 .cursorrules File Configuration

#### Purpose and Benefits

**.cursorrules** defines project-specific AI behavior:
- Coding standards enforcement
- Domain terminology understanding
- Pattern consistency
- Security guidelines

#### Maritime Insurance .cursorrules Example

```yaml
# .cursorrules
project_context:
  domain: "Maritime Insurance"
  type: "Full-stack application"
  stack:
    - "Node.js with TypeScript"
    - "PostgreSQL for persistence"
    - "Redis for caching"
    - "Docker for containerization"

coding_standards:
  language_version: "TypeScript 5.0+"
  style_guide: "ESLint with Airbnb config"
  naming_conventions:
    files: "kebab-case"
    classes: "PascalCase"
    functions: "camelCase"
    constants: "UPPER_SNAKE_CASE"

domain_terminology:
  vessel_types:
    - "Bulk Carrier"
    - "Container Ship"
    - "Tanker"
    - "General Cargo"
    - "Passenger Vessel"
  
  coverage_types:
    - "Hull and Machinery (H&M)"
    - "Protection and Indemnity (P&I)"
    - "Freight, Demurrage and Defence (FD&D)"
    - "War Risks"
    - "Loss of Hire"

patterns:
  error_handling: "Use Result<T, E> pattern for operations that can fail"
  validation: "Validate at domain boundaries using value objects"
  testing: "Follow Arrange-Act-Assert pattern"

security:
  - "Never log sensitive policy holder information"
  - "Encrypt PII at rest and in transit"
  - "Use parameterized queries for all database operations"
  - "Implement rate limiting on all public endpoints"

ai_behavior:
  - "Always suggest type-safe implementations"
  - "Include error handling in all code suggestions"
  - "Prefer composition over inheritance"
  - "Generate comprehensive JSDoc comments"
  - "Follow maritime insurance industry standards"
```

#### Team Collaboration Rules

```yaml
# Additional team-specific rules
team_conventions:
  pr_requirements:
    - "All code must have tests"
    - "Update documentation for API changes"
    - "Run security scan before merge"
  
  code_review:
    focus_areas:
      - "Business logic accuracy"
      - "Performance implications"
      - "Security vulnerabilities"
      - "Test coverage"

  documentation:
    required_for:
      - "Public APIs"
      - "Complex algorithms"
      - "Integration points"
      - "Configuration options"
```

#### Exercise 4.1: Custom Rules Creation
**Task**: Create comprehensive .cursorrules file
1. Define project-specific standards
2. Add maritime insurance terminology
3. Include security requirements
4. Configure AI suggestions

**Success Criteria**:
- Rules enforce standards
- AI respects configuration
- Team consistency improved
- Domain accuracy enhanced

### 4.2 Custom Prompts and Workflows

#### Prompt Engineering for Insurance Domain

**Effective Prompt Structure**:
1. Context setting
2. Specific requirements
3. Constraints and boundaries
4. Expected output format

**Example: Complex Premium Calculation**
```
# Prompt for Cmd+K:
Generate a maritime insurance premium calculation system that:
- Handles multiple vessel types (cargo, tanker, passenger)
- Considers voyage routes and seasonal factors
- Applies war risk zones surcharge
- Includes fleet discounts for multiple vessels
- Returns detailed breakdown of all factors
- Follows clean architecture principles
- Includes comprehensive error handling
```

#### Workflow Automation

**Custom Snippet Creation**:
```json
// .vscode/maritime-snippets.code-snippets
{
  "Maritime Policy Factory": {
    "prefix": "mpolicy",
    "body": [
      "export class ${1:PolicyType}PolicyFactory {",
      "  static create(params: ${1:PolicyType}PolicyParams): Policy {",
      "    const validator = new ${1:PolicyType}Validator();",
      "    validator.validate(params);",
      "    ",
      "    return new Policy({",
      "      ...params,",
      "      type: PolicyType.${1:POLICY_TYPE},",
      "      premium: this.calculatePremium(params),",
      "      terms: this.generateTerms(params)",
      "    });",
      "  }",
      "}"
    ],
    "description": "Create a maritime policy factory"
  }
}
```

#### Multi-Step Workflows

**Workflow: New Coverage Type Implementation**
```markdown
## Workflow: Add New Coverage Type

1. **Update Domain Model** (Cmd+K)
   - Add to CoverageType enum
   - Create specific coverage class

2. **Generate Validation Rules** (Cmd+K)
   - Create validator class
   - Add business rules

3. **Update Premium Calculator** (Cmd+L for guidance, then Cmd+K)
   - Add coverage-specific calculations
   - Update risk factors

4. **Create Tests** (Cmd+K)
   - Unit tests for calculations
   - Integration tests for workflows

5. **Update API** (Cmd+K)
   - Add endpoints
   - Update documentation
```

#### Exercise 4.2: Workflow Optimization
**Task**: Create automated workflow for claim processing
1. Design multi-step claim workflow
2. Create prompts for each step
3. Build reusable snippets
4. Document the process

**Success Criteria**:
- Workflow reduces development time
- Prompts generate accurate code
- Process is repeatable
- Documentation is clear

### 4.3 Integration with Other Tools

#### Git Integration

**Commit Message Generation**:
```bash
# After staging changes, use Cmd+K in commit message field:
# "Generate conventional commit message for these changes"

# Result:
feat(underwriting): add vessel age risk factor calculation

- Implement age-based premium adjustments
- Add depreciation factors for vessels >15 years
- Include special survey requirements
- Update risk assessment algorithm

BREAKING CHANGE: Premium calculation API now requires vessel age
```

#### Database Integration

**Schema Generation from Models**:
```typescript
// Select your domain model, then Cmd+K:
// "Generate PostgreSQL schema for this model with proper constraints"

-- Generated SQL:
CREATE TABLE vessels (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    imo_number VARCHAR(7) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL CHECK (type IN ('CARGO', 'TANKER', 'PASSENGER')),
    built_year INTEGER NOT NULL CHECK (built_year > 1900),
    gross_tonnage DECIMAL(10,2) NOT NULL CHECK (gross_tonnage > 0),
    insured_value DECIMAL(15,2) NOT NULL CHECK (insured_value > 0),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_vessels_type ON vessels(type);
CREATE INDEX idx_vessels_built_year ON vessels(built_year);
```

#### API Documentation Tools

**OpenAPI Spec Generation**:
```yaml
# Use Cmd+K on your route handlers:
# "Generate OpenAPI specification for this endpoint"

paths:
  /api/policies:
    post:
      summary: Create new maritime insurance policy
      tags:
        - Policies
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PolicyCreateRequest'
      responses:
        201:
          description: Policy created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Policy'
```

#### Exercise 4.3: Tool Chain Integration
**Task**: Integrate Cursor with your development stack
1. Set up Git hooks for commit standards
2. Generate database migrations from models
3. Create API documentation
4. Configure CI/CD integration

**Success Criteria**:
- Smooth tool integration
- Automated workflows
- Consistent outputs
- Reduced manual work

### 4.4 Performance Optimization

#### AI Response Optimization

**Techniques for Faster Responses**:

1. **Specific Context**
   ```typescript
   // Instead of: "Create a function to calculate premium"
   // Use: "Create a TypeScript function that calculates maritime cargo insurance premium based on value, route, and season"
   ```

2. **Provide Examples**
   ```typescript
   // Include example in prompt:
   // "Similar to this pattern but for passenger vessels:
   // function calculateCargoPremium(value: number, route: Route): Premium { ... }"
   ```

3. **Chunk Large Tasks**
   ```typescript
   // Break down complex requests:
   // Step 1: "Create the base risk assessment interface"
   // Step 2: "Implement cargo-specific risk factors"
   // Step 3: "Add passenger vessel risk factors"
   ```

#### Code Generation Performance

**Best Practices**:

1. **Clear File Organization**
   - Keep related code together
   - Use consistent patterns
   - Maintain clear imports

2. **Explicit Type Information**
   ```typescript
   // Provide type hints for better suggestions
   interface VesselRiskFactors {
     age: number;        // 0-1, where 1 is highest risk
     type: number;       // 0-1 based on vessel category
     route: number;      // 0-1 based on danger zones
     season: number;     // 0-1 based on weather patterns
   }
   ```

3. **Context Windows**
   - Keep relevant code visible
   - Close unrelated files
   - Use folding for large files

#### Memory and Cache Management

**Optimization Strategies**:

1. **Project Structure**
   ```
   # Organize for AI efficiency:
   src/
     core/          # Domain models (keep loaded)
     features/      # Feature modules (load as needed)
     shared/        # Utilities (selective loading)
   ```

2. **Working Sets**
   - Define focused working sets
   - Close unnecessary files
   - Use workspace management

#### Exercise 4.4: Performance Tuning
**Task**: Optimize a slow code generation workflow
1. Analyze current generation times
2. Reorganize code for better context
3. Create optimized prompts
4. Measure improvement

**Success Criteria**:
- 50% faster generation
- More accurate suggestions
- Better context utilization
- Improved workflow

---

## Module 5: Best Practices

### Learning Objectives
- Implement security best practices
- Maintain code quality standards
- Enable effective team collaboration
- Troubleshoot common issues

### 5.1 Security and Privacy Considerations

#### Data Privacy in AI-Assisted Development

**Critical Principles**:

1. **Never Include Sensitive Data in Prompts**
   ```typescript
   // BAD: Including real data
   // "Create a function to process policy for John Doe, SSN: 123-45-6789"
   
   // GOOD: Using placeholders
   // "Create a function to process policy with placeholder data"
   ```

2. **Sanitize Before Sharing**
   ```typescript
   // Create sanitization utility
   export function sanitizeForAI(data: any): any {
     const sensitiveFields = ['ssn', 'email', 'phone', 'address'];
     return sanitiveFields.reduce((acc, field) => {
       if (acc[field]) acc[field] = '[REDACTED]';
       return acc;
     }, { ...data });
   }
   ```

3. **Local Processing Options**
   - Use offline mode when possible
   - Configure local model options
   - Implement data masking

#### Secure Coding Practices

**Security-First Development**:

```typescript
// Use Cmd+L: "Review this code for security vulnerabilities"

// Example: Secure policy lookup
export class PolicyService {
  async findPolicy(userId: string, policyId: string): Promise<Policy> {
    // AI will suggest security improvements:
    // 1. Parameter validation
    if (!isValidUUID(userId) || !isValidUUID(policyId)) {
      throw new ValidationError('Invalid ID format');
    }
    
    // 2. Access control
    const hasAccess = await this.checkUserAccess(userId, policyId);
    if (!hasAccess) {
      throw new ForbiddenError('Access denied');
    }
    
    // 3. SQL injection prevention
    const query = `
      SELECT * FROM policies 
      WHERE id = $1 AND (user_id = $2 OR agent_id = $2)
    `;
    
    return this.db.query(query, [policyId, userId]);
  }
}
```

#### Compliance Considerations

**Maritime Insurance Regulations**:

```yaml
# Add to .cursorrules
compliance:
  regulations:
    - "GDPR for EU operations"
    - "Maritime Labour Convention (MLC)"
    - "International Maritime Organization (IMO) guidelines"
  
  requirements:
    - "Audit trail for all policy changes"
    - "Data retention according to jurisdiction"
    - "Encryption for sensitive data"
    - "Access control with role-based permissions"
```

#### Exercise 5.1: Security Audit
**Task**: Perform security review of existing code
1. Use AI to identify vulnerabilities
2. Implement suggested fixes
3. Add security tests
4. Document security measures

**Success Criteria**:
- No critical vulnerabilities
- Security tests pass
- Documentation complete
- Compliance verified

### 5.2 Code Quality Maintenance

#### Automated Quality Checks

**ESLint Configuration for Maritime Projects**:
```javascript
// .eslintrc.js
module.exports = {
  extends: ['airbnb-base', 'plugin:@typescript-eslint/recommended'],
  rules: {
    // Enforce maritime insurance conventions
    'naming-convention': [
      'error',
      {
        selector: 'class',
        format: ['PascalCase'],
        suffix: ['Service', 'Repository', 'Entity', 'Factory']
      }
    ],
    'max-complexity': ['error', 10],
    'max-depth': ['error', 3],
    'max-lines-per-function': ['error', 50]
  }
};
```

#### Code Review with AI Assistance

**Review Checklist Prompt**:
```
# Use Cmd+L with selected code:
Review this maritime insurance code for:
1. Business logic correctness
2. Error handling completeness
3. Performance implications
4. Security vulnerabilities
5. Test coverage gaps
6. Documentation needs
```

#### Refactoring Patterns

**AI-Assisted Refactoring**:
```typescript
// Select legacy code and Cmd+K:
// "Refactor this to use modern TypeScript patterns with proper error handling"

// Before:
function calculatePremium(policy) {
  var premium = policy.value * 0.02;
  if (policy.vesselAge > 20) premium = premium * 1.5;
  return premium;
}

// After AI refactoring:
export class PremiumCalculator {
  private readonly BASE_RATE = 0.02;
  private readonly AGE_MULTIPLIER = 1.5;
  private readonly AGE_THRESHOLD = 20;

  calculate(policy: Policy): Result<Premium, PremiumCalculationError> {
    try {
      this.validatePolicy(policy);
      const basePremium = this.calculateBase(policy);
      const adjustedPremium = this.applyAgeAdjustment(basePremium, policy);
      return Result.ok(new Premium(adjustedPremium));
    } catch (error) {
      return Result.err(new PremiumCalculationError(error.message));
    }
  }
}
```

#### Exercise 5.2: Quality Improvement
**Task**: Refactor legacy insurance module
1. Run AI-assisted code review
2. Identify improvement areas
3. Refactor using modern patterns
4. Add comprehensive tests

**Success Criteria**:
- Code passes all linters
- Complexity reduced
- Test coverage >90%
- Performance improved

### 5.3 Team Collaboration

#### Shared Configuration Management

**Team Settings Repository**:
```
team-config/
├── .cursorrules           # Shared AI behavior
├── .eslintrc.js          # Code style
├── .prettierrc           # Formatting
├── snippets/             # Team snippets
├── templates/            # Code templates
└── workflows/            # Automation scripts
```

#### Knowledge Sharing

**Documentation Generation**:
```typescript
// Use Cmd+K: "Generate comprehensive documentation for this module"

/**
 * Maritime Insurance Underwriting Service
 * 
 * Handles the complete underwriting workflow for maritime insurance policies.
 * Implements IMO guidelines and industry best practices.
 * 
 * @example
 * ```typescript
 * const underwriter = new UnderwritingService(riskAssessor, pricingEngine);
 * const result = await underwriter.evaluateApplication(application);
 * if (result.isApproved) {
 *   const policy = await underwriter.issuePolicy(result);
 * }
 * ```
 * 
 * @see {@link https://imo.org/guidelines} IMO Guidelines
 * @since 2.0.0
 */
export class UnderwritingService {
  // Implementation
}
```

#### Pair Programming with AI

**Effective Patterns**:

1. **Driver-Navigator with AI**
   - Human drives implementation
   - AI provides suggestions and reviews
   - Regular role switching

2. **Code Review Sessions**
   ```typescript
   // Team member writes code
   // Use Cmd+L: "Act as a senior developer and review this code for maritime insurance best practices"
   ```

3. **Knowledge Transfer**
   ```typescript
   // Junior dev uses Cmd+L: "Explain how this maritime risk calculation works in simple terms"
   ```

#### Exercise 5.3: Team Workflow
**Task**: Establish team collaboration process
1. Create shared configuration
2. Document team conventions
3. Set up review workflows
4. Practice pair programming

**Success Criteria**:
- Consistent code style
- Efficient review process
- Knowledge shared effectively
- Team productivity increased

### 5.4 Troubleshooting Common Issues

#### AI Suggestion Issues

**Problem: Incorrect Domain Suggestions**
```typescript
// Solution: Provide more context
// Instead of: "Calculate premium"
// Use: "Calculate maritime hull insurance premium for cargo vessel using London market rates"
```

**Problem: Outdated Patterns**
```typescript
// Solution: Specify modern requirements
// Add to prompt: "Use TypeScript 5.0 features, async/await, and functional programming patterns"
```

#### Performance Issues

**Problem: Slow Code Generation**

Solutions:
1. Close unnecessary files
2. Simplify project structure
3. Use specific prompts
4. Clear cache if needed

**Problem: Memory Usage**

Solutions:
1. Limit open files
2. Use focused workspaces
3. Restart Cursor periodically
4. Disable unused extensions

#### Integration Problems

**Problem: Git Conflicts with AI Changes**

```bash
# Best practice: Review before committing
git diff                  # Review AI changes
git add -p               # Selective staging
git commit -m "feat: implement risk assessment with AI assistance"
```

**Problem: Test Failures After AI Generation**

```typescript
// Solution: Use TDD approach
// 1. Write test first
// 2. Use Cmd+K: "Implement code to make this test pass"
// 3. Verify and refine
```

#### Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| "Context limit exceeded" | Too much code selected | Select smaller sections |
| "Unable to understand request" | Vague prompt | Add specific requirements |
| "Timeout generating response" | Complex request | Break into smaller tasks |
| "Conflicting suggestions" | Inconsistent context | Clear context, restart |

#### Exercise 5.4: Troubleshooting Practice
**Task**: Resolve common Cursor issues
1. Create scenarios with known issues
2. Practice troubleshooting steps
3. Document solutions
4. Create team playbook

**Success Criteria**:
- Issues resolved quickly
- Solutions documented
- Team can self-serve
- Productivity maintained

---

## Assessment and Certification

### Competency Assessment Framework

#### Skill Levels

1. **Beginner**: Can use basic features
2. **Intermediate**: Develops efficiently with AI
3. **Advanced**: Optimizes team workflows
4. **Expert**: Trains others and creates standards

### Practical Assessment Tasks

#### Task 1: Basic Proficiency (Beginner)
**Objective**: Demonstrate basic Cursor IDE usage

**Requirements**:
1. Set up new maritime insurance project
2. Generate basic policy model
3. Use AI to fix simple bugs
4. Create unit tests

**Time Limit**: 2 hours

**Evaluation Criteria**:
- [ ] Project structure correct
- [ ] AI commands used effectively
- [ ] Code runs without errors
- [ ] Tests pass

#### Task 2: Feature Development (Intermediate)
**Objective**: Build complete insurance feature

**Requirements**:
1. Implement claims processing workflow
2. Create comprehensive tests
3. Document with AI assistance
4. Handle edge cases

**Time Limit**: 4 hours

**Evaluation Criteria**:
- [ ] Feature fully functional
- [ ] 80%+ test coverage
- [ ] Documentation complete
- [ ] Error handling robust

#### Task 3: System Design (Advanced)
**Objective**: Design and implement complex system

**Requirements**:
1. Design multi-tenant insurance platform
2. Implement with clean architecture
3. Create deployment configuration
4. Performance optimization

**Time Limit**: 8 hours

**Evaluation Criteria**:
- [ ] Architecture sound
- [ ] Code quality high
- [ ] Performance acceptable
- [ ] Deployment ready

#### Task 4: Team Leadership (Expert)
**Objective**: Lead team implementation

**Requirements**:
1. Create team standards
2. Design workflow automation
3. Implement review process
4. Train team members

**Time Limit**: Project-based

**Evaluation Criteria**:
- [ ] Standards documented
- [ ] Automation effective
- [ ] Team productivity increased
- [ ] Knowledge transferred

### Certification Path

#### Cursor IDE Certified Developer - Maritime Insurance

**Requirements**:
1. Complete all training modules
2. Pass practical assessments
3. Submit portfolio project
4. Peer review participation

**Portfolio Project Requirements**:
- Complete maritime insurance system
- Uses advanced Cursor features
- Demonstrates best practices
- Includes documentation

**Certification Benefits**:
- Industry recognition
- Team leadership eligibility
- Advanced training access
- Community privileges

### Continuous Learning

#### Stay Updated

1. **Monthly Cursor Updates**
   - Review changelog
   - Test new features
   - Update workflows

2. **Maritime Insurance Trends**
   - Regulatory changes
   - Technology advances
   - Industry practices

3. **Community Engagement**
   - Share experiences
   - Learn from others
   - Contribute improvements

#### Advanced Resources

1. **Cursor Documentation**: https://cursor.sh/docs
2. **Maritime Insurance Resources**: Industry specifications
3. **AI Development Best Practices**: Current research
4. **Community Forums**: Problem solving and tips

### Course Completion

Congratulations on completing the Cursor IDE Training for Maritime Insurance Development! 

**Next Steps**:
1. Apply learning to real projects
2. Share knowledge with team
3. Continue practicing advanced features
4. Pursue certification

**Remember**: AI-assisted development is a tool that amplifies your capabilities. The combination of domain expertise and AI assistance creates exceptional results.

---

## Appendices

### Appendix A: Quick Reference Card

**Essential Shortcuts**:
- `Cmd+K` / `Ctrl+K`: AI Edit
- `Cmd+L` / `Ctrl+L`: AI Chat
- `Cmd+P` / `Ctrl+P`: Quick Open
- `Cmd+Shift+P` / `Ctrl+Shift+P`: Command Palette

**Best Practices Checklist**:
- [ ] Never include sensitive data
- [ ] Provide specific context
- [ ] Use consistent patterns
- [ ] Review AI suggestions
- [ ] Test generated code
- [ ] Document complex logic

### Appendix B: Troubleshooting Guide

**Common Issues Quick Fixes**:
1. Restart Cursor
2. Clear cache
3. Update to latest version
4. Check internet connection
5. Review error logs

### Appendix C: Resources and Links

- **Cursor Homepage**: https://cursor.sh
- **Support**: support@cursor.sh
- **Community**: Discord and forums
- **Updates**: Blog and changelog

---

*This training guide is a living document. Please submit feedback and suggestions for improvements to enhance the learning experience for future participants.*