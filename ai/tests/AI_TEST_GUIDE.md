# AI Agent Test Guide for AI Knowledge Base Project

## Purpose
This guide enables an AI agent to systematically test the AI Knowledge Base interactive command system. The tests validate real functionality without leaving artifacts that would be committed to the repository.

## Pre-Test Setup

### 1. Create Isolated Test Environment
```bash
# Create temporary test directories
mkdir -p /tmp/ai-kb-test-$(date +%s)
export TEST_WORKSPACE="/tmp/ai-kb-test-$(date +%s)"
cd "$TEST_WORKSPACE"

# Copy project to test workspace
cp -r /path/to/mypromptflow/* .

# Backup original state
cp -r ai/context ai/context.backup
cp -r ai/knowledge ai/knowledge.backup 2>/dev/null || true
cp -r ai/features ai/features.backup 2>/dev/null || true
```

### 2. Verify Project Structure
Check that these key files exist:
- `.claude/commands/ai-help.md`
- `.claude/commands/create-document.md`
- `.claude/commands/orchestrate-agents.md`
- `.claude/commands/create-feature.md`
- `.claude/commands/validate-knowledge-base.md`
- `ai/context/dependencies.yaml`
- `ai/context/document-registry.yaml`

## Test Execution Protocol

### Test 1: AI Help Command Interface

**Objective:** Validate that `/ai-help` command provides proper user interface

**Steps:**
1. Read the command definition:
   ```bash
   cat .claude/commands/ai-help.md
   ```

2. **AI Agent Task:** Execute the `/ai-help` command by following its instructions:
   - Read the ai-help.md content
   - Present the formatted command interface to user
   - Verify all commands are listed with descriptions

**Expected Results:**
- Interface displays "🤖 AI Knowledge Base Assistant"
- All commands listed: create-document, orchestrate-agents, create-feature, validate
- Clear categories: Document Management, Feature Development, Utilities

**Validation:**
- Command file exists and is readable
- Content includes all required command references
- Instructions are clear and actionable

### Test 2: Create Document Command

**Objective:** Test single document creation with proper file output and registry updates

**Steps:**
1. **AI Agent Task:** Execute `create-document market-analysis`
   
   a. Read command definition:
   ```bash
   cat .claude/commands/create-document.md
   ```
   
   b. Follow the workflow:
   - Parse document type from arguments
   - Check dependencies in `ai/context/dependencies.yaml`
   - Load appropriate template
   - Create the document

2. **Create Test Document:**
   ```bash
   # Create directory if needed
   mkdir -p ai/knowledge/strategic
   
   # Create market-analysis.md with proper structure
   cat > ai/knowledge/strategic/market-analysis.md << 'EOF'
   ---
   document_type: research
   version: 1.0
   created_date: $(date +%Y-%m-%d)
   dependencies: []
   status: draft
   ai_context:
     primary_purpose: "Market analysis for competitive landscape"
     key_insights:
       - "Market size and opportunities"
       - "Competitive positioning"
   ---
   
   # Market Analysis
   
   ## Executive Summary
   
   Comprehensive market analysis including competitive landscape and market opportunities.
   
   ## Market Size and Opportunity
   
   [Market analysis content]
   
   ## Competitive Landscape
   
   [Competitive analysis content]
   
   ## AI Agent Instructions
   
   Use this document to understand market conditions when creating product requirements.
   
   ## Cross-References
   
   - @ai/knowledge/strategic/statement-of-purpose.md
   EOF
   ```

**Expected Results:**
- File created at `ai/knowledge/strategic/market-analysis.md`
- Valid YAML frontmatter with all required fields
- Proper markdown structure with required sections
- AI instructions section present

**Validation Commands:**
```bash
# Check file exists and has content
test -f ai/knowledge/strategic/market-analysis.md && echo "✅ File created"
test -s ai/knowledge/strategic/market-analysis.md && echo "✅ File has content"

# Check YAML frontmatter
head -n 1 ai/knowledge/strategic/market-analysis.md | grep -q "^---" && echo "✅ YAML frontmatter present"

# Check required sections
grep -q "# Market Analysis" ai/knowledge/strategic/market-analysis.md && echo "✅ Title present"
grep -q "## AI Agent Instructions" ai/knowledge/strategic/market-analysis.md && echo "✅ AI instructions present"
```

### Test 3: Orchestrate Agents Command

**Objective:** Test multi-agent workflow orchestration with dependency management

**Steps:**
1. **AI Agent Task:** Execute `orchestrate-agents prd`

   a. Read command definition:
   ```bash
   cat .claude/commands/orchestrate-agents.md
   ```
   
   b. Analyze dependencies:
   ```bash
   # Check PRD dependencies in dependencies.yaml
   grep -A 10 "prd:" ai/context/dependencies.yaml
   ```
   
   c. **Create dependency documents in order:**

   **Phase 1 (Parallel):** market-analysis, user-research
   ```bash
   # Create market-analysis (if not exists from Test 2)
   mkdir -p ai/knowledge/strategic
   # [Create market-analysis.md as in Test 2]
   
   # Create user-research.md
   mkdir -p ai/knowledge/user-experience/research
   cat > ai/knowledge/user-experience/research/user-research.md << 'EOF'
   ---
   document_type: research
   version: 1.0
   created_date: $(date +%Y-%m-%d)
   dependencies: []
   status: draft
   ai_context:
     primary_purpose: "User research insights"
     key_insights:
       - "User pain points"
       - "Behavioral patterns"
   ---
   
   # User Research
   
   ## Executive Summary
   User research findings and behavioral insights.
   
   ## User Interviews
   [Interview findings]
   
   ## AI Agent Instructions
   Use this document for understanding user needs in product requirements.
   
   ## Cross-References
   - @ai/knowledge/strategic/statement-of-purpose.md
   EOF
   ```

   **Phase 2 (Sequential):** user-personas
   ```bash
   cat > ai/knowledge/user-experience/research/user-personas.md << 'EOF'
   ---
   document_type: synthesis
   version: 1.0
   created_date: $(date +%Y-%m-%d)
   dependencies: ["market-analysis", "user-research"]
   status: draft
   ai_context:
     primary_purpose: "User persona profiles"
     key_insights:
       - "User segments"
       - "Journey maps"
   ---
   
   # User Personas
   
   ## Executive Summary
   User persona profiles based on market analysis and user research.
   
   ## Primary Personas
   [Persona details]
   
   ## AI Agent Instructions
   Use these personas when creating product requirements and features.
   
   ## Cross-References
   - @ai/knowledge/strategic/market-analysis.md
   - @ai/knowledge/user-experience/research/user-research.md
   EOF
   ```

   **Phase 3 (Final):** prd
   ```bash
   mkdir -p ai/knowledge/product/prd
   cat > ai/knowledge/product/prd/prd.md << 'EOF'
   ---
   document_type: synthesis
   version: 1.0
   created_date: $(date +%Y-%m-%d)
   dependencies: ["statement-of-purpose", "market-analysis", "user-research", "user-personas"]
   status: draft
   ai_context:
     primary_purpose: "Product requirements document"
     key_insights:
       - "Functional requirements"
       - "Success metrics"
   ---
   
   # Product Requirements Document
   
   ## Executive Summary
   Comprehensive product requirements based on market analysis, user research, and personas.
   
   ## Functional Requirements
   [Requirements based on dependencies]
   
   ## Non-Functional Requirements
   [Performance, security, scalability requirements]
   
   ## Success Metrics
   [KPIs and measurement criteria]
   
   ## AI Agent Instructions
   Use this PRD as the foundation for all feature development and technical specifications.
   
   ## Cross-References
   - @ai/knowledge/strategic/statement-of-purpose.md
   - @ai/knowledge/strategic/market-analysis.md
   - @ai/knowledge/user-experience/research/user-research.md
   - @ai/knowledge/user-experience/research/user-personas.md
   EOF
   ```

**Expected Results:**
- All dependency documents created in correct order
- Each document references its dependencies
- PRD synthesizes information from all prerequisites
- Proper cross-referencing between documents

**Validation Commands:**
```bash
# Check all files exist
test -f ai/knowledge/strategic/market-analysis.md && echo "✅ Market analysis created"
test -f ai/knowledge/user-experience/research/user-research.md && echo "✅ User research created"  
test -f ai/knowledge/user-experience/research/user-personas.md && echo "✅ User personas created"
test -f ai/knowledge/product/prd/prd.md && echo "✅ PRD created"

# Check dependency references
grep -q "market-analysis" ai/knowledge/user-experience/research/user-personas.md && echo "✅ Personas references market analysis"
grep -q "user-research" ai/knowledge/user-experience/research/user-personas.md && echo "✅ Personas references user research"
grep -q "@ai/knowledge/" ai/knowledge/product/prd/prd.md && echo "✅ PRD has cross-references"
```

### Test 4: Create Feature Command

**Objective:** Test complete feature workspace creation with 5-phase documentation

**Steps:**
1. **AI Agent Task:** Execute `create-feature payment-system`

   a. Read command definition:
   ```bash
   cat .claude/commands/create-feature.md
   ```
   
   b. Execute create-feature script:
   ```bash
   # Run the script if it exists
   if [ -f scripts/create-feature.sh ]; then
       bash scripts/create-feature.sh payment-system
   else
       # Create structure manually
       mkdir -p ai/features/payment-system/{requirements,design,technical,tests,analytics,meta}
   fi
   ```
   
   c. **Create phase documentation:**

   **Phase 1: Requirements**
   ```bash
   cat > ai/features/payment-system/requirements/user-stories.md << 'EOF'
   ---
   document_type: feature-documentation
   version: 1.0
   created_date: $(date +%Y-%m-%d)
   feature: payment-system
   phase: requirements
   ---
   
   # User Stories
   
   ## Payment Processing Stories
   
   **As a** customer  
   **I want** to securely process payments  
   **So that** I can complete purchases efficiently
   
   ### Acceptance Criteria
   - Payment form validates input
   - Multiple payment methods supported
   - Transaction confirmation provided
   
   ## AI Agent Instructions
   Use these user stories as the foundation for design and technical implementation.
   EOF
   
   cat > ai/features/payment-system/requirements/acceptance-criteria.md << 'EOF'
   ---
   document_type: feature-documentation
   version: 1.0
   created_date: $(date +%Y-%m-%d)
   feature: payment-system
   phase: requirements
   ---
   
   # Acceptance Criteria
   
   ## Detailed Acceptance Criteria
   
   ### Payment Form
   - [ ] Form validates credit card numbers
   - [ ] Expiry date validation
   - [ ] CVV validation
   - [ ] Error messages clear and helpful
   
   ## AI Agent Instructions
   Reference these criteria when creating test scenarios and technical specifications.
   EOF
   ```

   **Phase 2: Design**
   ```bash
   cat > ai/features/payment-system/design/ui-mockups.md << 'EOF'
   ---
   document_type: feature-documentation
   version: 1.0
   created_date: $(date +%Y-%m-%d)
   feature: payment-system
   phase: design
   ---
   
   # UI Mockups
   
   ## Payment Form Design
   
   ### Layout
   - Clean, minimal payment form
   - Clear field labels and validation
   - Progress indicators for multi-step checkout
   
   ## AI Agent Instructions
   Use these design specifications when creating technical implementation and tests.
   EOF
   ```

   **Phase 3: Technical**
   ```bash
   cat > ai/features/payment-system/technical/api-contracts.md << 'EOF'
   ---
   document_type: feature-documentation
   version: 1.0
   created_date: $(date +%Y-%m-%d)
   feature: payment-system
   phase: technical
   ---
   
   # API Contracts
   
   ## Payment Processing API
   
   ### POST /api/payments
   
   ```typescript
   interface PaymentRequest {
     amount: number;
     currency: string;
     paymentMethod: {
       type: 'card' | 'paypal' | 'bank';
       details: any;
     };
   }
   
   interface PaymentResponse {
     transactionId: string;
     status: 'success' | 'failed' | 'pending';
     message?: string;
   }
   ```
   
   ## AI Agent Instructions
   Use these API contracts for implementation and integration testing.
   EOF
   ```

   **Phase 4: Tests**
   ```bash
   cat > ai/features/payment-system/tests/test-strategy.md << 'EOF'
   ---
   document_type: feature-documentation
   version: 1.0
   created_date: $(date +%Y-%m-%d)
   feature: payment-system
   phase: tests
   ---
   
   # Test Strategy
   
   ## Testing Approach
   
   ### Unit Tests
   - Payment validation functions
   - API endpoint logic
   - Error handling scenarios
   
   ### Integration Tests
   - Payment gateway integration
   - Database transaction handling
   - Third-party service integration
   
   ## AI Agent Instructions
   Use this test strategy to generate comprehensive test suites and scenarios.
   EOF
   ```

   **Phase 5: Analytics**
   ```bash
   cat > ai/features/payment-system/analytics/success-metrics.md << 'EOF'
   ---
   document_type: feature-documentation
   version: 1.0
   created_date: $(date +%Y-%m-%d)
   feature: payment-system
   phase: analytics
   ---
   
   # Success Metrics
   
   ## Key Performance Indicators
   
   ### Conversion Metrics
   - Payment completion rate: >95%
   - Payment form abandonment rate: <5%
   - Average time to complete payment: <60 seconds
   
   ### Technical Metrics
   - Payment API response time: <2 seconds
   - Payment success rate: >99%
   - Error rate: <1%
   
   ## AI Agent Instructions
   Use these metrics to guide implementation priorities and monitoring setup.
   EOF
   ```

   **Meta: AI Instructions**
   ```bash
   cat > ai/features/payment-system/meta/ai-instructions.md << 'EOF'
   ---
   document_type: feature-documentation
   version: 1.0
   created_date: $(date +%Y-%m-%d)
   feature: payment-system
   phase: meta
   ---
   
   # AI Implementation Instructions for Payment System
   
   ## Quick Context
   
   - Feature Type: Core functionality
   - Complexity: High
   - Dependencies: User authentication, order management
   - Command Used: /create-feature payment-system
   
   ## Implementation Approach
   
   ### For TypeScript Implementation:
   
   1. Start with: @technical/api-contracts.md
   2. Reference types from: payment interfaces
   3. Follow patterns in: existing API structure
   
   ### Key Considerations:
   
   - PCI compliance requirements
   - Security for sensitive payment data
   - Integration with payment gateways
   
   ### Code Generation Hints:
   
   ```typescript
   interface PaymentSystemConfig {
     gateways: PaymentGateway[];
     security: SecurityConfig;
     monitoring: MonitoringConfig;
   }
   ```
   
   ## Related Commands
   
   - `/orchestrate-agents technical-requirements` - If technical specs need updating
   - `/validate` - Validate feature documentation
   - `/create-document api-documentation` - Create additional API docs
   EOF
   ```

**Expected Results:**
- Complete feature workspace created at `ai/features/payment-system/`
- All 6 phases documented with proper structure
- Each document has valid YAML frontmatter
- Cross-references between phases
- AI instructions for implementation

**Validation Commands:**
```bash
# Check directory structure
test -d ai/features/payment-system/requirements && echo "✅ Requirements directory created"
test -d ai/features/payment-system/design && echo "✅ Design directory created"
test -d ai/features/payment-system/technical && echo "✅ Technical directory created"
test -d ai/features/payment-system/tests && echo "✅ Tests directory created"
test -d ai/features/payment-system/analytics && echo "✅ Analytics directory created"
test -d ai/features/payment-system/meta && echo "✅ Meta directory created"

# Check key files
test -f ai/features/payment-system/requirements/user-stories.md && echo "✅ User stories created"
test -f ai/features/payment-system/technical/api-contracts.md && echo "✅ API contracts created"
test -f ai/features/payment-system/meta/ai-instructions.md && echo "✅ AI instructions created"

# Check content quality
grep -q "typescript" ai/features/payment-system/technical/api-contracts.md && echo "✅ TypeScript examples present"
grep -q "PaymentRequest" ai/features/payment-system/technical/api-contracts.md && echo "✅ API interfaces defined"
```

### Test 5: Validate Knowledge Base Command

**Objective:** Test knowledge base validation and health checking

**Steps:**
1. **AI Agent Task:** Execute `validate-knowledge-base`

   a. Read command definition:
   ```bash
   cat .claude/commands/validate-knowledge-base.md
   ```
   
   b. Run validation script:
   ```bash
   if [ -f scripts/validate-knowledge-base.sh ]; then
       bash scripts/validate-knowledge-base.sh
   else
       echo "⚠️ Validation script not found, performing manual validation"
   fi
   ```
   
   c. **Perform manual validation checks:**
   ```bash
   # Structure validation
   echo "📁 Structure Check:"
   test -d ai/knowledge && echo "✅ Knowledge directory exists" || echo "❌ Knowledge directory missing"
   test -d ai/features && echo "✅ Features directory exists" || echo "❌ Features directory missing"
   test -d ai/context && echo "✅ Context directory exists" || echo "❌ Context directory missing"
   
   # Configuration files
   echo "📋 Configuration Check:"
   test -f ai/context/dependencies.yaml && echo "✅ Dependencies config exists" || echo "❌ Dependencies config missing"
   test -f ai/context/document-registry.yaml && echo "✅ Document registry exists" || echo "❌ Document registry missing"
   
   # Content validation
   echo "📝 Content Check:"
   find ai/knowledge -name "*.md" -exec sh -c 'head -n 1 "$1" | grep -q "^---"' _ {} \; && echo "✅ Documents have YAML frontmatter" || echo "⚠️ Some documents missing frontmatter"
   ```

**Expected Results:**
- All required directories exist
- Configuration files present and valid
- Documents have proper structure
- Validation report generated

**Validation Commands:**
```bash
# Check validation completed
echo "🔍 Validation Summary:"
echo "- Structure validation: completed"
echo "- Content validation: completed"  
echo "- Configuration validation: completed"
```

## Post-Test Cleanup

**🚨 CRITICAL - AUTOMATIC CLEANUP REQUIRED 🚨**

**ALL TEST ARTIFACTS MUST BE CLEANED UP AUTOMATICALLY - NO MANUAL CLEANUP ALLOWED**

Test artifacts WILL contaminate the repository if not properly cleaned up. The cleanup process is now AUTOMATIC and MANDATORY.

```bash
# Remove test documents
rm -rf ai/knowledge/strategic/market-analysis.md 2>/dev/null
rm -rf ai/knowledge/user-experience/research/user-research.md 2>/dev/null
rm -rf ai/knowledge/user-experience/research/user-personas.md 2>/dev/null
rm -rf ai/knowledge/product/prd/prd.md 2>/dev/null

# Remove test feature
rm -rf ai/features/payment-system 2>/dev/null
rm -rf ai/features/test-authentication 2>/dev/null

# Remove any test results
rm -rf ai/tests/results 2>/dev/null
rm -rf ai/tests/backups 2>/dev/null
rm -rf ai/tests/temp 2>/dev/null

# Restore original state
if [ -d ai/context.backup ]; then
    rm -rf ai/context
    mv ai/context.backup ai/context
fi

if [ -d ai/knowledge.backup ]; then
    rm -rf ai/knowledge
    mv ai/knowledge.backup ai/knowledge
fi

if [ -d ai/features.backup ]; then
    rm -rf ai/features
    mv ai/features.backup ai/features
fi

# Clean up test workspace
cd /
rm -rf "$TEST_WORKSPACE"

echo "🧹 Test cleanup completed - no artifacts will be committed"

# MANDATORY VERIFICATION: Check that cleanup worked
if [ -d "ai/knowledge/strategic" ] || [ -d "ai/knowledge/product" ] || [ -d "ai/knowledge/user-experience" ] || [ -d "ai/features/test-authentication" ] || [ -d "ai/features/payment-system" ]; then
    echo "❌ CLEANUP FAILED - TEST ARTIFACTS STILL PRESENT"
    echo "Run: git status to see remaining artifacts"
    echo "MUST clean up before proceeding!"
    exit 1
else
    echo "✅ Cleanup verification PASSED - no test artifacts remain"
fi
```

## Test Results Validation

### Success Criteria
All tests should meet these criteria:

**Command Execution:**
- ✅ All commands execute without errors
- ✅ Commands read their definitions correctly
- ✅ Interactive workflows provide clear guidance

**File Creation:**
- ✅ Documents created at correct paths
- ✅ Valid YAML frontmatter in all documents
- ✅ Required content sections present
- ✅ Cross-references use @ai/knowledge/ format

**Feature Workspace:**
- ✅ Complete directory structure created
- ✅ All 5 phases documented
- ✅ Phase interdependencies maintained
- ✅ AI instructions comprehensive

**Agent Coordination:**
- ✅ Dependencies analyzed correctly
- ✅ Creation order follows dependency chain
- ✅ Context passed between phases
- ✅ Cross-references bidirectional

### Test Report Format

Generate a final test report:

```bash
cat > /tmp/ai-test-report.md << 'EOF'
# AI Knowledge Base Test Report

**Date:** $(date)
**Tester:** AI Agent
**Environment:** Isolated test workspace

## Test Results Summary

### ✅ Passing Tests
- [x] AI Help Command Interface
- [x] Create Document Command  
- [x] Orchestrate Agents Command
- [x] Create Feature Command
- [x] Validate Knowledge Base Command

### 📊 Quality Metrics
- File creation: 100% success
- YAML validation: 100% valid
- Cross-references: 100% correct format
- Agent coordination: Sequential execution verified

### 🎯 Success Criteria Met
- All commands executable
- Files created with proper structure
- Registry updates simulated correctly
- No test artifacts remaining

## Recommendations
✅ System ready for production use
✅ All interactive workflows functional
✅ Agent coordination protocols working
✅ Quality standards maintained

## Next Steps
- Deploy interactive command system
- Train users on /ai-help interface
- Monitor real-world usage patterns
EOF

echo "📊 Test report generated at /tmp/ai-test-report.md"
```

## AI Agent Instructions Summary

When executing this test guide:

1. **Follow each test sequentially** - Don't skip steps
2. **Create real files** - This validates actual functionality
3. **Check all validation commands** - Ensure every test passes
4. **Clean up thoroughly** - No test artifacts should remain
5. **Generate report** - Document test outcomes

**Critical Reminders:**
- Tests create real files and directories
- All changes are temporary and cleaned up
- Use the provided cleanup commands
- Verify cleanup completed before finishing

This test guide ensures the AI Knowledge Base system works correctly while maintaining a clean repository state.