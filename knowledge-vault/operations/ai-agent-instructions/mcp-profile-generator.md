# AI Agent Instructions: Automated MCP Server Profile Generator

## System Purpose

Generate comprehensive, standardized MCP server profiles using the unified blueprint template system with intelligent knowledge-vault integration, community-driven scoring v4.0.0, and Docker-first deployment approach.

**System Context**:
- **Blueprint Template**: `@knowledge-vault/operations/blueprints/mcp-server-profile-blueprint.yaml` - Master standardization template
- **Scoring Algorithm**: `@projects/universal-topic-intelligence-system/mcp-registry/schemas/business-aligned-scoring-algorithm.yaml` v4.0.0 - Community-driven scoring
- **Knowledge-Vault Schema**: `@knowledge-vault/schemas/tools-services-schema.yaml` - Data structure and tagging system
- **Profile Examples**: `@projects/universal-topic-intelligence-system/docs/mcp-server-registry/mcp-registry/detailed-profiles/` - Quality reference patterns

## Core Instructions

### Phase 1: Blueprint Template Application

#### 1.1 Template Loading and Validation
```yaml
Required Actions:
1. Load blueprint template from @knowledge-vault/operations/blueprints/mcp-server-profile-blueprint.yaml
2. Validate template structure and required sections
3. Confirm placeholder format consistency ({{variable}} pattern)
4. Verify integration points with scoring algorithm v4.0.0
5. Check knowledge-vault cross-reference format requirements
```

#### 1.2 Server Information Collection
```yaml
Data Collection Requirements:
Basic Information:
  - server_name: Official project/repository name
  - server_description: Comprehensive capability overview
  - primary_capability: Core functionality description
  - key_features: 4-6 specific features (bulleted)
  - target_use_cases: Primary application domains
  - business_value_statement: Strategic value articulation

Technical Specifications:
  - server_type: Classification (Database, API, Workflow, etc.)
  - primary_language: Main programming language
  - key_dependencies: Critical runtime dependencies
  - auth_methods: Authentication mechanisms
  - api_capabilities: Structured capability matrix
  - docker_image: Container registry reference
  - default_port: Standard service port

Source Requirements:
  - Use official documentation, README files, and repository information
  - Prioritize current, accurate technical specifications
  - Validate compatibility claims against actual capabilities
  - Cross-reference deployment requirements
```

#### 1.3 Placeholder Substitution Protocol
```yaml
Substitution Rules:
1. Replace ALL {{placeholder}} variables with server-specific values
2. Maintain consistent naming conventions (server_name vs SERVER_NAME)
3. Use exact format specified in template examples
4. Preserve code block formatting and syntax highlighting
5. Ensure all examples are executable and accurate

Quality Validation:
- No remaining {{placeholder}} patterns in final output
- All code examples are syntactically correct
- Docker commands are executable with provided parameters
- Authentication examples match actual server requirements
```

### Phase 2: Community-Driven Scoring Application (v4.0.0)

#### 2.1 Scoring Algorithm Implementation
```yaml
Community-Driven Scoring Dimensions (v4.0.0):

1. Community Adoption (35% weight):
   Scale: 0-10
   Assessment Criteria:
     - GitHub stars, forks, contributor count
     - Production usage testimonials and case studies
     - Community engagement (Discord, forums, tutorials)
     - Enterprise adoption indicators
   Scoring Examples:
     - >10k stars, industry standard: 10
     - Popular SaaS platforms: 9
     - Active community projects: 8
     - Emerging tools with traction: 7
     - Niche specialized tools: 6
     - Experimental/early stage: 4
     - Minimal usage: 2

2. Information Retrieval Relevance (25% weight):
   Scale: 0-10
   Assessment Criteria:
     - Search and discovery capabilities
     - Knowledge management features
     - Database query functionality
     - Content organization and retrieval
   Scoring Examples:
     - Elasticsearch, vector databases: 10
     - Notion, documentation platforms: 9
     - PostgreSQL, graph databases: 9
     - Content management systems: 8
     - Analytics and reporting: 8
     - Entertainment platforms: 3

3. Integration Potential (20% weight):
   Scale: 0-10
   Assessment Criteria:
     - API richness and extensibility
     - Webhook and automation support
     - Plugin ecosystem availability
     - Standard protocol compliance
   Scoring Examples:
     - Zapier, Make (workflow automation): 10
     - GitHub, Slack (rich APIs): 9
     - PostgreSQL (multiple integrations): 8
     - Standard protocol support: 7
     - Limited integration APIs: 5
     - Standalone tools: 2

4. Production Readiness (10% weight):
   Scale: 0-10
   Assessment Criteria:
     - Enterprise deployment capability
     - SLA and uptime guarantees
     - Security compliance standards
     - Commercial support availability
   Scoring Examples:
     - Enterprise managed services: 10
     - Official vendor support: 9
     - Battle-tested platforms: 8
     - Active community maintenance: 7
     - Stable but limited production: 6
     - Experimental/beta: 4

5. Maintenance Status (10% weight):
   Scale: 0-10
   Assessment Criteria:
     - Active development indicators
     - Recent update frequency
     - Security patch responsiveness
     - Community health metrics
   Scoring Examples:
     - Official Anthropic servers: 10
     - Enterprise vendor support: 9
     - Active open source projects: 7
     - Moderate community maintenance: 5
     - Minimal maintenance: 3
     - Abandoned projects: 1
```

#### 2.2 Composite Score Calculation
```yaml
Calculation Formula:
composite_score = 
  (community_adoption * 0.35) +
  (information_retrieval_relevance * 0.25) +
  (integration_potential * 0.20) +
  (production_readiness * 0.10) +
  (maintenance_status * 0.10)

Tier Classification:
- Tier 1: 8.0+ (High Community Adoption)
- Tier 2: 6.5-7.9 (Moderate Adoption)
- Tier 3: 4.5-6.4 (Emerging/Niche)
- Tier 4: 2.5-4.4 (Experimental)
- Tier 5: 0.0-2.4 (Low Value)

Validation Requirements:
- Show calculation breakdown for transparency
- Include rationale for each dimension score
- Cross-reference with similar servers for consistency
- Document edge cases and scoring decisions
```

### Phase 3: Content Quality Assurance

#### 3.1 Industry Neutrality Enforcement
```yaml
Content Sanitization Rules:
Forbidden Terms/References:
  - "maritime insurance", "vessel", "P&I Club", "flag state", "IMO"
  - "cargo", "shipping", "marine", "nautical", "port operations"
  - "Lloyd's", "classification society", "hull & machinery"
  - Industry-specific terminology requiring domain expertise

Required Replacements:
  - Maritime → Business/Enterprise applications
  - Vessel tracking → Asset management
  - Cargo management → Inventory management
  - Port operations → Facility operations
  - Claims processing → Business process management

Generic Business Examples:
  - "Claims processing workflows for business applications"
  - "Asset management and tracking systems"
  - "Compliance monitoring for enterprise applications"
  - "Business process automation and optimization"
  - "Enterprise resource planning integration"
```

#### 3.2 Docker-First Setup Priority
```yaml
Installation Method Priority Order:
1. Method 1: Docker MCP Toolkit (Recommended)
   - Most detailed configuration examples
   - Complete environment variable documentation
   - Production-ready deployment patterns
   - Container orchestration examples

2. Method 2: Docker Compose Deployment
   - Multi-service deployment scenarios
   - Dependency management examples
   - Volume and network configuration
   - Service discovery patterns

3. Method 3: Claude Code Integration
   - Development environment setup
   - NPM/package manager installation
   - Configuration file examples
   - Environment variable management

4. Method 4: Claude Desktop Integration
   - Desktop application configuration
   - JSON configuration examples
   - Plugin installation procedures

5. Method 5: Alternative Installation Methods
   - Package manager fallbacks
   - Source compilation options
   - Platform-specific installers
   - Enterprise deployment tools

Quality Requirements:
- Docker methods must have complete, executable examples
- All environment variables documented with descriptions
- Port mappings clearly specified
- Volume requirements explained
- Security considerations addressed
```

#### 3.3 Section Header Standardization
```yaml
Required Section Structure:
## 📋 Basic Information (NOT Executive Summary)
## Quality & Scoring Metrics
### Business-Aligned Scoring Analysis
### Production Readiness Assessment
### Quality Validation Metrics
## Technical Specifications
### Core Architecture
### System Requirements
### API Capabilities
### Data Models
## Setup & Configuration
### Installation Methods
#### Method 1: Docker MCP Toolkit (Recommended)
#### Method 2: Docker Compose Deployment
#### Method 3: Claude Code Integration
#### Method 4: Claude Desktop Integration
#### Method 5: Alternative Installation Methods
### Authentication Configuration
### Advanced Configuration Options

Consistency Requirements:
- Use EXACT header text as specified
- Maintain emoji usage where indicated
- Follow hierarchical structure precisely
- Ensure all required subsections present
```

### Phase 4: Knowledge-Vault Integration

#### 4.1 Intelligent Tagging System Application
```yaml
Required Tags (All Profiles):
- "mcp-server"
- "tier-{tier_number}" (tier-1, tier-2, tier-3)
- Primary domain category from schema

Automatic Tag Assignment Rules:
Server Type → Tags:
  - PostgreSQL, MongoDB → "database"
  - GitHub, GitLab → "developer-tools", "version-control"
  - Docker, Kubernetes → "containerization", "developer-tools"
  - Slack, Microsoft Teams → "communication", "collaboration"
  - Notion, Confluence → "documentation", "collaboration"
  - Elasticsearch, Algolia → "search", "analytics"
  - Zapier, Make → "automation", "integration"
  - Auth0, Keycloak → "security", "authentication"

Company/Vendor Tags:
- Extract from repository URL or official documentation
- Apply vendor-specific tags (microsoft, google, amazon, etc.)
- Include platform tags (saas, platform, open-source)

Quality Validation:
- Minimum 3 tags per profile (mcp-server + tier + domain)
- Maximum 8 tags per profile (avoid over-tagging)
- Validate tags exist in tools-services-schema.yaml
- Ensure tag consistency across similar servers
```

#### 4.2 Cross-Reference Generation
```yaml
Knowledge-Vault Cross-Reference Format:
- @knowledge_vault/{item_uuid} for direct item references
- Bidirectional relationship creation required
- Cross-reference validation against existing items

Relationship Categories:
Related Servers:
  - Similar functionality servers
  - Complementary technology servers
  - Alternative implementation servers
  - Dependency relationship servers

Related Knowledge Items:
  - Technology research findings
  - Implementation guides
  - Best practice documentation
  - Architecture decision records

Integration Patterns:
- Document common integration scenarios
- Reference deployment patterns
- Link to configuration templates
- Connect to troubleshooting guides

File Structure Requirements:
base_path: "knowledge-vault/databases/tools_services/items/"
naming_convention: "{server_name_lowercase}_mcp_server.yaml"
metadata_format: Complete YAML frontmatter with all schema fields
```

#### 4.3 Database Synchronization
```yaml
YAML Frontmatter Generation:
id: Generate UUID v4 for unique identification
name: Use official server name (matches profile title)
status: Set to "discovered" for new profiles
rating: Calculate based on composite score (8.0+ = 5 stars, 6.5+ = 4 stars, etc.)
maturity_level: Assess based on production readiness score
technology_type: Array of applicable technology classifications
deployment_model: Primary deployment approach (cloud_hosted, self_hosted, etc.)
integration_complexity: Based on setup complexity assessment
vendor: Extract from official documentation
licensing_model: Determine from repository/documentation
tags: Apply intelligent tagging rules
url: Primary documentation or repository URL
description: Comprehensive capability description
key_features: Extract 4-6 primary capabilities
use_cases: Generic business applications
created_date: Current timestamp
last_modified: Current timestamp

Notion Synchronization:
- Generate YAML file compatible with Notion import
- Include all required fields from tools-services-schema.yaml
- Validate against schema constraints
- Prepare for bidirectional sync capability
```

### Phase 5: Batch Processing Capabilities

#### 5.1 Multi-Profile Generation Workflow
```yaml
Batch Processing Protocol:
1. Input Validation:
   - Validate server list format (name, repository URL, tier target)
   - Check for duplicate entries
   - Verify accessibility of source documentation
   - Validate prerequisite data availability

2. Sequential Processing:
   - Process servers in tier priority order (Tier 1 first)
   - Apply consistent scoring methodology
   - Maintain cross-reference consistency
   - Track progress and error states

3. Quality Validation:
   - Cross-validate scoring consistency
   - Check tag assignment patterns
   - Verify Docker-first setup priority
   - Validate industry neutrality compliance

4. Output Organization:
   - Create profiles in correct directory structure
   - Generate knowledge-vault YAML files
   - Update master registry databases
   - Create relationship mappings

Progress Tracking:
- Log successful profile generations
- Track failed attempts with error details
- Maintain processing statistics
- Generate batch completion reports
```

#### 5.2 Error Handling and Recovery
```yaml
Error Categories:
1. Data Collection Failures:
   - Repository inaccessible
   - Documentation incomplete
   - API information unavailable
   - Technical specifications unclear

2. Scoring Calculation Errors:
   - Insufficient community data
   - Ambiguous feature classifications
   - Integration capability unclear
   - Production readiness uncertain

3. Template Application Issues:
   - Placeholder substitution failures
   - Code example generation problems
   - Docker configuration errors
   - Authentication setup complications

Recovery Procedures:
1. Automatic Retry:
   - Retry data collection with alternative sources
   - Apply fallback scoring methodologies
   - Use template defaults where appropriate
   - Generate minimal viable profiles

2. Manual Review Queue:
   - Flag profiles requiring human review
   - Document specific issues encountered
   - Provide partial profile with known gaps
   - Include improvement recommendations

3. Quality Assurance:
   - Validate generated profiles against blueprint
   - Check scoring calculation accuracy
   - Verify code example executability
   - Confirm knowledge-vault integration
```

### Phase 6: Integration and Validation

#### 6.1 Profile Completeness Validation
```yaml
17-Point Quality Checklist:
Content Validation:
[ ] All industry-specific references removed
[ ] Generic business examples used throughout
[ ] Section headers match user preferences exactly
[ ] Key value propositions clearly articulated (4-6 items)
[ ] Business-aligned scoring properly calculated and formatted

Technical Validation:
[ ] Docker-first deployment approach implemented
[ ] All installation methods properly documented
[ ] Code examples are complete and executable
[ ] API capabilities properly structured with TypeScript interfaces
[ ] Authentication methods comprehensively covered

Integration Validation:
[ ] Knowledge-vault tagging system properly applied
[ ] Cross-references use correct @knowledge_vault/uuid format
[ ] File structure follows knowledge-vault conventions
[ ] YAML frontmatter includes all required metadata fields
[ ] Bidirectional relationships properly documented

Final Validation:
[ ] All template placeholders replaced with specific values
[ ] Scoring calculations match community-driven algorithm v4.0.0
[ ] Production readiness assessment is comprehensive
[ ] Setup instructions prioritize Docker deployment methods
[ ] Documentation is complete and implementable
```

#### 6.2 Cross-Reference Accuracy Verification
```yaml
Validation Protocol:
1. Knowledge-Vault References:
   - Verify @knowledge_vault/{uuid} format accuracy
   - Check referenced items exist and are accessible
   - Validate bidirectional relationship integrity
   - Confirm cross-reference semantic accuracy

2. External References:
   - Validate all URLs are accessible and current
   - Check repository references point to correct projects
   - Verify documentation links are functional
   - Confirm Docker image references are valid

3. Internal Consistency:
   - Cross-check scoring rationale with capability descriptions
   - Verify tier classification matches composite score
   - Validate technical specifications consistency
   - Check deployment method priority ordering

4. Schema Compliance:
   - Validate against tools-services-schema.yaml requirements
   - Check all required fields are populated
   - Verify tag assignments are valid schema options
   - Confirm data type compliance for all fields
```

### Phase 7: Advanced Features

#### 7.1 Similarity Analysis and Deduplication
```yaml
Similarity Detection:
1. Server Name Matching:
   - Check for exact name duplicates
   - Identify similar naming patterns
   - Detect abbreviation variations
   - Flag potential duplicate servers

2. Functionality Overlap Analysis:
   - Compare capability descriptions
   - Analyze API feature matrices
   - Check use case similarity
   - Identify redundant functionality

3. Repository Analysis:
   - Check for same repository references
   - Identify forked or mirrored projects
   - Detect wrapper or proxy servers
   - Flag organization duplicates

Deduplication Strategy:
- Merge profiles for identical servers
- Create cross-reference relationships for similar servers
- Prioritize official over community implementations
- Document relationship types between similar servers
```

#### 7.2 Quality Scoring Consistency
```yaml
Consistency Validation Rules:
1. Community Adoption Scoring:
   - GitHub stars >10k consistently score 9-10
   - Popular SaaS platforms score 8-9
   - Active community projects score 6-8
   - Experimental platforms score 3-5

2. Information Retrieval Relevance:
   - Search platforms consistently score 9-10
   - Knowledge management tools score 8-9
   - Database systems score 7-9
   - Entertainment platforms score 2-4

3. Integration Potential:
   - Workflow automation platforms score 9-10
   - API-rich platforms score 8-9
   - Standard protocol support scores 6-8
   - Closed systems score 2-4

4. Cross-Server Validation:
   - Compare similar servers for scoring consistency
   - Flag outlier scores for manual review
   - Maintain scoring rationale documentation
   - Apply calibration adjustments as needed
```

#### 7.3 Automated Quality Improvement
```yaml
Quality Enhancement Features:
1. Content Optimization:
   - Automated grammar and style checking
   - Technical terminology consistency
   - Example code validation and testing
   - Link accessibility verification

2. Structure Optimization:
   - Section completeness checking
   - Header hierarchy validation
   - Content length balancing
   - Information density optimization

3. Integration Enhancement:
   - Automatic relationship discovery
   - Smart tag suggestion based on content
   - Cross-reference validation and repair
   - Knowledge-vault synchronization verification

4. Continuous Improvement:
   - Profile usage analytics integration
   - User feedback incorporation
   - Community contribution integration
   - Version control and change tracking
```

## Execution Protocol

### Standard Profile Generation Process
```yaml
Single Profile Generation:
1. Execute Phase 1: Blueprint Template Application (5-10 minutes)
2. Execute Phase 2: Community-Driven Scoring v4.0.0 (3-5 minutes)
3. Execute Phase 3: Content Quality Assurance (3-5 minutes)
4. Execute Phase 4: Knowledge-Vault Integration (2-3 minutes)
5. Execute Phase 6: Integration and Validation (2-3 minutes)
Total Time: 15-26 minutes per profile

Quality Gates:
- Phase completion validation before proceeding
- Error handling and recovery at each phase
- Rollback capability for failed generations
- Manual review queue for complex cases
```

### Batch Processing Execution
```yaml
Multi-Profile Generation:
1. Input validation and preprocessing (2-5 minutes)
2. Tier-based processing priority (Tier 1 → Tier 2 → Tier 3)
3. Parallel processing where possible (3-5 profiles concurrent)
4. Progress tracking and error logging
5. Batch validation and consistency checking
6. Knowledge-vault database updates
7. Final reporting and statistics

Monitoring Requirements:
- Real-time progress tracking
- Error rate monitoring
- Quality metric reporting
- Resource utilization tracking
- Completion time estimation
```

## Success Metrics and Quality Standards

### Profile Quality Metrics
- **Completeness**: 100% of required sections populated
- **Accuracy**: 95%+ technical specification accuracy
- **Consistency**: 95%+ scoring methodology consistency
- **Industry Neutrality**: 100% maritime reference removal
- **Docker-First Priority**: 100% Docker method prioritization

### Integration Quality Metrics
- **Knowledge-Vault Sync**: 100% successful YAML generation
- **Cross-Reference Accuracy**: 98%+ valid reference links
- **Tag Assignment**: 95%+ appropriate tag selection
- **Schema Compliance**: 100% schema validation passing

### Performance Metrics
- **Generation Time**: 15-26 minutes per profile (single)
- **Batch Processing**: 3-5 profiles concurrent processing
- **Error Rate**: <5% profile generation failures
- **Quality Score**: 90%+ average profile quality rating

## Integration Points and Dependencies

### Required File Access
- `@knowledge-vault/operations/blueprints/mcp-server-profile-blueprint.yaml` - Master template
- `@projects/universal-topic-intelligence-system/mcp-registry/schemas/business-aligned-scoring-algorithm.yaml` - Scoring algorithm v4.0.0
- `@knowledge-vault/schemas/tools-services-schema.yaml` - Data structure and validation
- `@projects/universal-topic-intelligence-system/docs/mcp-server-registry/mcp-registry/detailed-profiles/` - Quality reference examples

### Output Locations
- **Profile Files**: `@projects/universal-topic-intelligence-system/docs/mcp-server-registry/mcp-registry/detailed-profiles/tier-{n}/`
- **Knowledge-Vault Items**: `@knowledge-vault/databases/tools_services/items/`
- **Registry Updates**: Master database files in MCP registry structure
- **Relationship Files**: Cross-reference and relationship mapping files

### External Integration Points
- **Notion Synchronization**: YAML files compatible with Notion database import
- **MCP Registry System**: Integration with existing registry structure
- **Quality Validation**: Integration with existing validation frameworks
- **Version Control**: Git-based change tracking and collaboration support

This comprehensive instruction set enables any AI agent to generate high-quality, consistent MCP server profiles using the unified blueprint template system with full knowledge-vault integration and community-driven scoring methodology.