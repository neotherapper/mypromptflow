# Maritime Insurance Knowledge System

## Project Context

**Project Type**: Domain-Specific Knowledge System
**Status**: Active Development
**Priority**: High

## Project Summary

This project creates a comprehensive AI-powered knowledge base for maritime insurance, specifically focused on the VanguardAI maritime risk platform. The system processes business documentation from OneDrive, validates knowledge through user interaction, and provides intelligent maritime insurance domain expertise to AI agents.

**Goals**: 
- Extract and structure maritime insurance knowledge from OneDrive source files
- Create user-validated knowledge base with approval workflows
- Build AI agents specialized in maritime insurance domain
- Integrate with existing @ai/ system for comprehensive business intelligence

**Success Criteria**: 
- Complete knowledge extraction from OneDrive files
- User-approved knowledge base with validation audit trail
- Functional maritime insurance AI agents
- Integration with project development workflows

**Approach**: 
- Hybrid approach combining projects/ structure with @ai/ system integration
- Specialized maritime agents for knowledge extraction
- Interactive validation system for user knowledge approval
- Structured markdown/yaml knowledge base

**Constraints**: 
- No code or database files - markdown/yaml only
- All critical knowledge requires user validation
- Must maintain integration with existing @ai/ system
- OneDrive files may contain outdated information requiring verification

## Current Status

**Progress**: Phase 1 - Project structure setup complete

**Active Tasks**: 
- Creating maritime-specific CLAUDE.md with domain context
- Building knowledge validation system
- Creating maritime commands integration

**Blockers**: None currently

## AI Agent Instructions

### Maritime Insurance Domain Context

This project focuses on **maritime insurance and risk assessment**, specifically for the VanguardAI platform. The domain includes:

**Core Business Areas**:
- War risk insurance for maritime vessels
- Voyage-based and static vessel risk calculations
- Sanction compliance and KYC procedures
- Maritime customer onboarding (B2C focus)
- Quote generation and pricing workflows
- Vessel management and data specifications

**Key Terminology**:
- **War Risk**: Insurance coverage for vessels in war zones or high-risk areas
- **Voyage Risk**: Risk assessment based on specific voyage routes and destinations
- **Static Vessel Risk**: Risk calculation for vessels at port or anchor
- **Sanction Screening**: Compliance checks against international sanctions lists
- **KYC**: Know Your Customer procedures for maritime insurance clients
- **PMSC**: Private Maritime Security Company (service provider view)
- **B2C Platform**: Business-to-consumer insurance platform (confirmed by user)

**Business Model**: B2C maritime insurance platform serving individual vessel owners and operators

### How to Work on This Project

1. **Read Context First**: Review project-purpose.md for detailed goals and scope
2. **Check Tasks**: Look at task-list.md for current priorities and status
3. **Review Research**: Check research-integration.md for relevant knowledge and gaps
4. **Update Progress**: Document your work in progress.md
5. **Manage Tasks**: Update task-list.md when completing or adding tasks

### Working Patterns

**Preferred Approach**: 
- Process OneDrive files systematically using specialized maritime agents
- Extract key facts and create structured validation questions
- Always validate critical knowledge with user before marking as approved
- Maintain clear separation between pending and approved knowledge
- Use structured markdown with proper YAML frontmatter

**Quality Standards**: 
- All documents must include maritime-specific metadata
- Source tracking for every piece of knowledge
- Confidence scoring for extracted information
- User approval audit trail for all critical facts
- Clear AI agent instructions for domain usage

**Things to Avoid**: 
- Don't assume knowledge without user validation
- Don't create code or database files
- Don't modify existing @ai/ system structure
- Don't mix pending and approved knowledge
- Don't ignore OneDrive file timestamps and potential outdated info

### Maritime Knowledge Categories

**Risk Assessment Knowledge**:
- War risk calculation models and factors
- Voyage risk assessment methodologies
- Static vessel risk evaluation procedures
- Historical risk data and trends

**Regulatory Knowledge**:
- Sanction compliance procedures
- KYC requirements and workflows
- International maritime regulations
- Compliance documentation standards

**Operational Knowledge**:
- Quote generation workflows
- Customer onboarding procedures
- Vessel management processes
- Premium calculation methodologies

**Business Knowledge**:
- Competitive analysis and positioning
- Market trends and opportunities
- Pricing strategies and models
- Customer segment analysis

### Tools and Resources

**Research Context**: 
- OneDrive source files at `/Users/georgiospilitsoglou/Library/CloudStorage/OneDrive-SharedLibraries-VanguardTech/Vanguard Tech - Risk Platform`
- Existing @ai/ system for cross-referencing
- Research orchestrator for complex domain analysis

**Dependencies**: 
- OneDrive file access for source material
- User interaction for knowledge validation
- @ai/ system integration for enhanced capabilities
- Git worktree for isolated development

**External Resources**: 
- Maritime insurance industry standards
- International sanctions databases
- Vessel registration and classification systems
- Maritime risk assessment frameworks

## Validation System Guidelines

### Knowledge Validation Process

1. **Extraction Phase**: AI agents process OneDrive files and extract key facts
2. **Question Generation**: Create specific validation questions for user approval
3. **User Interaction**: Present questions and collect user responses
4. **Approval Process**: User validates, corrects, or rejects extracted knowledge
5. **Knowledge Storage**: Approved knowledge moves to validated/ directory
6. **Audit Trail**: Complete history of validation decisions

### Validation Question Examples

**Format**: Clear, specific questions with context
- "Based on the OneDrive files, is the VanguardAI platform B2C or B2B?"
- "Should war risk calculations include the vessel tonnage factor as described in the premium examples?"
- "Are the sanction screening procedures in the HH Sanction Questionnaire still current?"

### User Response Processing

**Approval**: "B2C" → Knowledge approved and stored in validated/business/platform-type.md
**Correction**: "B2C but with PMSC partnership model" → Knowledge updated and stored
**Rejection**: "Outdated, now B2B" → Knowledge marked as rejected, new fact stored

## Quick Navigation

- **Project Purpose**: See project-purpose.md for detailed goals
- **Current Tasks**: See task-list.md for work queue
- **Progress Tracking**: See progress.md for accomplishments
- **Research Integration**: See research-integration.md for knowledge context
- **Knowledge Base**: See knowledge/ for maritime domain knowledge
- **Validation System**: See validation-interactions/ for user approval workflows

## Next Steps for AI Agents

1. **Immediate**: Complete project setup and documentation
2. **Phase 2**: Begin OneDrive file processing with maritime agents
3. **Phase 3**: Generate validation questions for user approval
4. **Phase 4**: Build approved knowledge base
5. **Phase 5**: Integrate with @ai/ system commands

## Integration with @ai/ System

### Command Extensions
- Maritime-specific commands in `.claude/commands/`
- Integration with existing orchestration workflows
- Cross-references to @ai/knowledge/ when applicable

### Knowledge Sharing
- Validated maritime knowledge available to general AI agents
- Domain expertise enhances general business knowledge
- Specialized maritime prompts and templates

### Quality Assurance
- Extension of validate-knowledge-base.md for maritime domain
- Maritime-specific validation criteria
- Integration with existing quality standards

Last Updated: 2025-01-17