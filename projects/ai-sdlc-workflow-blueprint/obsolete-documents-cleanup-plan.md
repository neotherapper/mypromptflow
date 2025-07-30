# Obsolete Documents Cleanup Plan

## Executive Summary

Following the decision to fully embrace VanguardAI implementation, this document identifies all obsolete, superseded, or misaligned documents that require deletion, major revision, or archival within the AI-SDLC workflow blueprint.

**Impact**: 23 documents flagged for deletion, 31 documents requiring major updates, 35 documents needing minor alignment updates.

---

## 🗑️ DOCUMENTS FOR DELETION (23 files)

### Superseded Infrastructure Tools
These tools are no longer part of the VanguardAI stack and should be completely removed:

| File Path | Reason for Deletion | Replacement |
|-----------|-------------------|-------------|
| `tools/railway.md` | Replaced by App Runner | VanguardAI App Runner implementation |
| `tools/vercel.md` | Replaced by S3+CloudFront | VanguardAI S3+CloudFront optimization |
| `tools/neon.md` | Replaced by Aurora Serverless v2 | VanguardAI Aurora Serverless v2 |
| `tools/gitpod.md` | Conflicts with VanguardAI local dev | Local development with serverless focus |

### Obsolete Implementation Guides
These guides describe approaches that conflict with VanguardAI methodology:

| File Path | Reason for Deletion | Replacement |
|-----------|-------------------|-------------|
| `docs/implementation-guide/complete-implementation-guide.md` | Generic SDLC approach | `vanguardai-complete-implementation-guide.md` |
| `docs/implementation-guide/master-infrastructure-decision.md` | Replaced by VanguardAI decisions | Updated infrastructure decision documents |
| `docs/implementation-guide/phase-1-setup-guide.md` | Traditional AWS setup | VanguardAI 3-phase implementation plan |
| `docs/implementation-guide/phase-2-onboarding-guide.md` | Generic onboarding | VanguardAI-specific team training |
| `docs/implementation-guide/phase-3-workflow-guide.md` | Traditional workflow | VanguardAI ephemeral environment workflow |
| `docs/implementation-guide/phase-4-optimization-guide.md` | Generic optimization | VanguardAI cost optimization strategies |

### Superseded Visual Diagrams
These diagrams show architectures that are no longer relevant:

| File Path | Reason for Deletion | Replacement |
|-----------|-------------------|-------------|
| `docs/visual-diagrams/complete-workflow-diagram.md` | Generic workflow | `vanguardai-complete-workflow-diagram.md` |
| `docs/visual-diagrams/tool-integration-diagram.md` | Traditional tools | VanguardAI serverless architecture |
| `docs/visual-diagrams/data-flow-diagram.md` | Generic data patterns | VanguardAI serverless data flow |

### Obsolete Training Materials
These training materials focus on tools no longer in the stack:

| File Path | Reason for Deletion | Replacement |
|-----------|-------------------|-------------|
| `docs/training-materials/infrastructure-training.md` | Generic AWS training | VanguardAI serverless stack training |
| `docs/workflow-examples/stage-4-implementation-workflow.md` | Traditional deployment | VanguardAI ephemeral environment deployment |
| `docs/workflow-examples/stage-5-testing-workflow.md` | Standard testing | E2E testing on preview environments |
| `docs/workflow-examples/stage-6-deployment-workflow.md` | Traditional deployment | Blue-green deployment process |

### Outdated Options Analysis
These options are superseded by VanguardAI analysis:

| File Path | Reason for Deletion | Replacement |
|-----------|-------------------|-------------|
| `options/infrastructure-options.md` | Superseded by VanguardAI | Archive for historical reference |
| `options/development-environment-options.md` | Needs VanguardAI alignment | VanguardAI-specific development setup |
| `options/repository-architecture-options.md` | Traditional approaches | VanguardAI CDK and GitHub integration |

---

## 🔄 DOCUMENTS REQUIRING MAJOR UPDATES (31 files)

### Infrastructure & Architecture
| File Path | Required Update | Priority |
|-----------|----------------|----------|
| `decisions/infrastructure-decision.md` | ✅ **COMPLETED** - Already updated for VanguardAI | - |
| `options/aws-architecture-options.md` | Add VanguardAI ephemeral environment options | High |
| `options/docker-vs-s3-frontend-analysis.md` | Enhance with VanguardAI S3+CloudFront optimizations | Medium |

### Implementation Guides
| File Path | Required Update | Priority |
|-----------|----------------|----------|
| `docs/implementation-guide/engineering-practices-guide.md` | Add VanguardAI CI/CD practices and ephemeral environments | High |
| `docs/implementation-guide/testing-framework-implementation.md` | Align with VanguardAI testing on ephemeral environments | High |
| `docs/implementation-guide/implementation-setup-guide.md` | Replace with VanguardAI 3-phase setup process | High |
| `docs/implementation-guide/stage-1-requirements-guide.md` | Update for VanguardAI-specific requirements | Medium |

### Cost & ROI Analysis
| File Path | Required Update | Priority |
|-----------|----------------|----------|
| `docs/cost-benefit-analysis/roi-analysis.md` | Update with VanguardAI cost model ($12/PR environment) | High |
| `docs/cost-benefit-analysis/roi-dashboard.md` | Update with serverless cost tracking metrics | Medium |

### Visual Diagrams
| File Path | Required Update | Priority |
|-----------|----------------|----------|
| `docs/visual-diagrams/ai-enhancement-points-diagram.md` | Show VanguardAI AI integration points | Medium |
| `docs/visual-diagrams/cost-benefit-flow-diagram.md` | Update with VanguardAI cost optimization flow | Medium |
| `docs/visual-diagrams/decision-tree-diagram.md` | Update decision paths for VanguardAI stack | Medium |
| `docs/visual-diagrams/quality-gates-diagram.md` | Show ephemeral environment quality gates | Medium |
| `docs/visual-diagrams/team-collaboration-diagram.md` | Update for VanguardAI workflow collaboration | Medium |

### Training Materials
| File Path | Required Update | Priority |
|-----------|----------------|----------|
| `docs/training-materials/git-workflow-training.md` | Add ephemeral environment workflows | High |
| `docs/training-materials/testing-framework-training.md` | Update for E2E testing on ephemeral environments | High |
| `docs/training-materials/code-quality-training.md` | Align with VanguardAI development practices | Medium |
| `docs/training-materials/role-specific-training-guide.md` | Update for VanguardAI stack responsibilities | Medium |

### Setup Procedures
| File Path | Required Update | Priority |
|-----------|----------------|----------|
| `docs/setup-procedures/tool-procurement-guide.md` | Update for VanguardAI stack procurement | High |
| `docs/setup-procedures/team-onboarding-guide.md` | VanguardAI-specific onboarding procedures | High |

### Team Resources
| File Path | Required Update | Priority |
|-----------|----------------|----------|
| `team-resources/software-licenses.md` | Update costs for VanguardAI stack | Medium |
| `team-resources/productivity-tools.md` | Align tools with VanguardAI development | Medium |

### Tool Documentation
| File Path | Required Update | Priority |
|-----------|----------------|----------|
| `tools/github-actions.md` | Update for VanguardAI CI/CD workflows | High |
| `tools/github.md` | Add OIDC authentication setup for AWS | Medium |
| `tools/claude-code-max.md` | Add VanguardAI integration examples | Low |
| `tools/cursor-ide.md` | Update for AWS CDK development | Low |

---

## ⚪ DOCUMENTS NEEDING MINOR UPDATES (35 files)

### Team & Process Documents (No major changes needed)
| File Path | Required Update | Priority |
|-----------|----------------|----------|
| `decisions/team-structure-decision.md` | Minor updates to reflect VanguardAI deployment practices | Low |
| `decisions/sdlc-stages-decision.md` | Minor updates for ephemeral environment integration | Low |
| `decisions/tool-selection-decision.md` | Validate tool selection aligns with VanguardAI | Low |

### Workflow Examples (Minor alignment needed)
| File Path | Required Update | Priority |
|-----------|----------------|----------|
| `docs/workflow-examples/marine-quote-generator-workflow.md` | Update infrastructure references | Low |
| `docs/workflow-examples/stage-1-requirements-workflow.md` | Minor VanguardAI alignment | Low |
| `docs/workflow-examples/stage-2-design-workflow.md` | Update for preview environment design validation | Low |
| `docs/workflow-examples/stage-3-planning-workflow.md` | Minor ephemeral environment planning updates | Low |

### Remaining Tool Documentation (Minor updates)
| File Path | Required Update | Priority |
|-----------|----------------|----------|
| All remaining `tools/*.md` files | Minor updates for consistency with VanguardAI stack | Low |

---

## 📦 ARCHIVAL RECOMMENDATIONS

### Documents to Archive (Keep for Historical Reference)
| File Path | Archival Reason | Archive Location |
|-----------|----------------|------------------|
| `options/infrastructure-options.md` | Historical decision context | `archive/pre-vanguardai/` |
| `docs/implementation-guide/complete-implementation-guide.md` | Original SDLC approach | `archive/pre-vanguardai/` |
| `docs/visual-diagrams/complete-workflow-diagram.md` | Original workflow design | `archive/pre-vanguardai/` |

---

## 🚀 IMPLEMENTATION PLAN

### Phase 1: Critical Deletions (Week 1)
**Priority: HIGH - Remove conflicting guidance**

1. **Delete Obsolete Tool Documentation**
   ```bash
   rm tools/railway.md tools/vercel.md tools/neon.md tools/gitpod.md
   ```

2. **Delete Superseded Implementation Guides**
   ```bash
   rm docs/implementation-guide/complete-implementation-guide.md
   rm docs/implementation-guide/master-infrastructure-decision.md
   rm docs/implementation-guide/phase-*-guide.md
   ```

3. **Delete Obsolete Visual Diagrams**
   ```bash
   rm docs/visual-diagrams/complete-workflow-diagram.md
   rm docs/visual-diagrams/tool-integration-diagram.md
   rm docs/visual-diagrams/data-flow-diagram.md
   ```

### Phase 2: Major Updates (Weeks 1-2)
**Priority: HIGH - Align critical documentation**

1. **Update Infrastructure Documentation**
   - `options/aws-architecture-options.md` - Add VanguardAI options
   - `docs/cost-benefit-analysis/roi-analysis.md` - VanguardAI cost model

2. **Update Training Materials**
   - `docs/training-materials/infrastructure-training.md` - Rewrite for VanguardAI
   - `docs/training-materials/git-workflow-training.md` - Add ephemeral workflows

3. **Update Implementation Guides**
   - `docs/implementation-guide/engineering-practices-guide.md` - VanguardAI practices
   - `docs/implementation-guide/testing-framework-implementation.md` - Ephemeral testing

### Phase 3: Minor Alignments (Week 3)
**Priority: MEDIUM - Consistency and completeness**

1. **Update Tool Documentation**
   - `tools/github-actions.md` - VanguardAI workflows
   - `tools/github.md` - OIDC setup

2. **Update Workflow Examples**
   - Minor updates to all `docs/workflow-examples/*.md` files

3. **Update Team Resources**
   - `team-resources/software-licenses.md` - Cost updates
   - `team-resources/productivity-tools.md` - Tool alignment

### Phase 4: Final Cleanup (Week 4)
**Priority: LOW - Polish and archival**

1. **Archive Historical Documents**
   - Create `archive/pre-vanguardai/` directory
   - Move superseded documents with metadata

2. **Final Consistency Check**
   - Verify all references point to correct documents
   - Update any remaining cross-references
   - Validate all links are functional

---

## 🔍 VALIDATION CHECKLIST

### Content Consistency Validation
- [ ] All cost figures updated to VanguardAI model
- [ ] All infrastructure references point to App Runner + Aurora Serverless v2
- [ ] All deployment processes show ephemeral environment workflow
- [ ] All training materials aligned with VanguardAI stack

### Technical Accuracy Validation
- [ ] CDK construct examples use VanguardAI patterns
- [ ] GitHub Actions workflows match VanguardAI implementation
- [ ] Cost calculations verified against VanguardAI data
- [ ] Security practices align with VanguardAI recommendations

### Documentation Completeness Validation
- [ ] All VanguardAI capabilities documented
- [ ] Implementation timeline updated to 8-week plan
- [ ] Team training updated for serverless technologies
- [ ] Risk mitigation updated for new architecture

### Link and Reference Validation
- [ ] All internal links functional after cleanup
- [ ] Cross-references updated to new document names
- [ ] Tool documentation references consistent
- [ ] Archive references properly maintained

---

## 📊 IMPACT ASSESSMENT

### Cleanup Benefits
- **Reduced Confusion**: Remove conflicting guidance between traditional and VanguardAI approaches
- **Improved Onboarding**: Clear, consistent documentation aligned with actual implementation
- **Maintenance Efficiency**: Fewer documents to maintain, all aligned with chosen architecture
- **Cost Accuracy**: Updated cost models reflect actual VanguardAI economics

### Risk Mitigation
- **Archive Strategy**: Historical documents preserved for reference
- **Phased Approach**: Critical updates first, polish last
- **Validation Process**: Comprehensive checks ensure no broken references
- **Team Communication**: Clear announcement of changes to avoid confusion

### Expected Outcomes
- **23 fewer obsolete documents** cluttering the project
- **31 major updates** ensuring alignment with VanguardAI
- **35 minor updates** for consistency and accuracy
- **100% documentation alignment** with chosen implementation path

---

## 📋 EXECUTION CHECKLIST

### Pre-Cleanup Preparation
- [ ] Create backup of current documentation state
- [ ] Set up `archive/pre-vanguardai/` directory structure
- [ ] Notify team of upcoming documentation changes
- [ ] Identify any dependencies on documents marked for deletion

### Cleanup Execution
- [ ] Execute Phase 1: Critical deletions
- [ ] Execute Phase 2: Major updates
- [ ] Execute Phase 3: Minor alignments
- [ ] Execute Phase 4: Final cleanup and archival

### Post-Cleanup Validation
- [ ] Run link checker on all remaining documents
- [ ] Verify cost calculations in updated documents
- [ ] Test implementation procedures with team members
- [ ] Update project navigation and CLAUDE.md references

### Success Criteria
- [ ] Zero broken internal links
- [ ] All cost figures reflect VanguardAI model
- [ ] All implementation guides use VanguardAI architecture
- [ ] Team can follow documentation without confusion
- [ ] Historical documents preserved in archive

---

**Cleanup Plan Status**: Ready for Execution  
**Estimated Effort**: 4 weeks with parallel execution  
**Risk Level**: Low - comprehensive backup and archival strategy  
**Expected Outcome**: 100% VanguardAI-aligned documentation ready for team implementation