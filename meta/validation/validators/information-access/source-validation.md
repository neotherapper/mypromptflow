# Information Access Source Validation
# Validates source selection, accessibility, and integration with information access framework

## Purpose

Specialized validator for information access framework compliance, source selection validation, and multi-source coordination patterns in research and AI agent workflows.

## Activation Criteria

**Trigger Patterns:**
- Research orchestrator execution with information source discovery
- AI-PR validation using technology-specific source mappings  
- Knowledge vault queries with information-access tags
- MCP server usage for information retrieval
- Multi-source workflow coordination

**File Patterns:**
- `meta/information-access/**/*.yaml` (source mappings and configurations)
- `research/findings/**/.meta/research-sources.md` (research source tracking)
- `knowledge-vault/databases/tools_services/views/*.yaml` (information source views)
- Any files referencing MCP information access patterns

## Validation Scope

### 1. Source Selection Validation

**Framework Compliance:**
- **Topic vs Category Routing**: Verify specific technology mappings override categorical patterns
- **Decision Tree Logic**: Validate source selection follows agent decision framework
- **Confidence Scoring**: Ensure source selection confidence meets minimum thresholds
- **Fallback Procedures**: Confirm backup sources configured for primary source failures

**Technology-Specific Validation:**
- **React Source Mapping**: Validate React detection triggers proper GitHub, Context7, npm sources
- **Database Category Mapping**: Ensure database patterns route to appropriate MCP servers
- **Cross-Reference Accuracy**: Verify all @file_path references are accessible and current

### 2. Source Accessibility Assessment

**MCP Server Integration:**
- **Server Availability**: Validate MCP servers referenced in mappings are accessible
- **Tool Access Patterns**: Verify MCP tool patterns match actual server capabilities
- **Authentication Requirements**: Assess authentication complexity and feasibility
- **Rate Limit Coordination**: Validate rate limit handling strategies

**Knowledge Vault Integration:**
- **View Accessibility**: Confirm knowledge vault views load correctly
- **Tag Filtering**: Validate information-access tags function as designed
- **Cross-Database Queries**: Ensure tools_services database queries work properly
- **Update Coordination**: Verify mappings stay synchronized with knowledge vault updates

### 3. Multi-Source Coordination

**Research Framework Integration:**
- **Orchestrator Step 3.5**: Validate information source discovery integration
- **Sub-Agent Coordination**: Ensure source-aware sub-agent task distribution
- **Source Attribution**: Verify research outputs include proper source tracking
- **Quality Validation**: Confirm multi-source validation enhances research quality

**AI-PR Validation Integration:**
- **Conditional Source Loading**: Validate React/TypeScript files trigger appropriate sources
- **Validation Enhancement**: Ensure typescript-frontend-validator uses React-specific patterns
- **Progressive Context Loading**: Verify source-specific context loads only when needed
- **Result Aggregation**: Confirm multi-source validation results integrate properly

## AI Agent Instructions

### Phase 1: Source Mapping Validation

**For each information access mapping file:**

1. **Load Mapping Configuration**: Use Read tool to analyze source mapping YAML
2. **Validate Structure Compliance**:
   ```yaml
   # Required elements to check:
   metadata:
     version: "present and semantic"
     purpose: "clear and specific"
     integration: "describes system integration"
   
   conditional_selection:
     detection_triggers: "specific and measurable"
     confidence_scoring: "algorithmic and threshold-based"
     source_prioritization: "tiered with fallbacks"
   
   integration_patterns:
     ai_pr_validation_system: "concrete integration points"
     research_framework_integration: "orchestrator coordination"
     knowledge_vault_coordination: "authoritative source alignment"
   ```

3. **Cross-Reference Validation**:
   - Verify all referenced files exist and are accessible
   - Check MCP server names match knowledge vault entries
   - Validate tool access patterns against MCP server capabilities
   - Confirm authentication requirements are realistic

### Phase 2: Source Selection Logic Testing

**Decision Tree Validation:**

1. **Technology Detection Testing**:
   ```typescript
   // Validate React detection logic:
   test_cases: [
     {
       input: "files: ['src/App.tsx', 'package.json with react dependency']",
       expected: "react-sources.yaml activation with confidence >= 0.8"
     },
     {
       input: "files: ['schema.sql', 'migrations/001_create_users.sql']", 
       expected: "database-sources.yaml activation with PostgreSQL routing"
     }
   ]
   ```

2. **Confidence Scoring Verification**:
   - Test confidence calculation algorithms for accuracy
   - Verify minimum confidence thresholds prevent false positives
   - Validate edge cases and boundary conditions
   - Ensure reproducible scoring across similar inputs

3. **Fallback Logic Testing**:
   - Confirm categorical patterns activate when specific technology unclear
   - Validate knowledge vault fallback when no mappings match
   - Test graceful degradation when primary sources unavailable

### Phase 3: Integration Point Validation

**Research Framework Integration:**

1. **Orchestrator Step 3.5 Validation**:
   ```yaml
   # Check integration points:
   step_3_5_discover_information_sources:
     reference_files: "all paths accessible"
     source_discovery_process: "logic complete and actionable"
     output_format: "matches downstream expectations"
     integration_strategy: "coordinates with existing steps"
   ```

2. **Source Tracking Validation**:
   - Verify research-sources.md template includes information access tracking
   - Check source attribution in research outputs
   - Validate MCP server usage logging
   - Confirm topic vs category routing documentation

**AI-PR Validation Integration:**

1. **TypeScript Frontend Validator Enhancement**:
   ```yaml
   # Verify React-specific enhancements:
   react_integration:
     source_mappings: "GitHub repositories for React patterns"
     documentation_access: "Context7 library docs for React"
     knowledge_context: "react-frontend-dev.md integration"
     validation_patterns: "React-specific TypeScript validation"
   ```

2. **Conditional Loading Validation**:
   - Test React file detection triggers appropriate source loading
   - Verify progressive context loading reduces token usage
   - Validate role-aware agent spawning with React specialization
   - Confirm multi-role coordination (frontend-dev, security, performance)

### Phase 4: Quality and Performance Assessment

**Source Quality Metrics:**

1. **Accessibility Validation**:
   - Test MCP server connectivity and response times
   - Verify authentication setup procedures work as documented
   - Check rate limit handling strategies under load
   - Validate fallback procedures activate correctly

2. **Integration Effectiveness**:
   - Measure source selection accuracy for technology detection
   - Assess research quality improvement with multi-source coordination
   - Validate reduction in setup time through information access framework
   - Confirm constitutional AI compliance across all source operations

## Validation Output Format

### Success Report Template

```yaml
information_access_validation:
  validation_time: "[duration]"
  files_processed: [count]
  
  source_mapping_compliance:
    structure_validation: "[0-100]"
    cross_reference_accuracy: "[0-100]"
    integration_completeness: "[0-100]"
    
    mapping_issues:
      - file: "meta/information-access/topic-mappings/react-sources.yaml"
        issue: "Missing fallback source configuration"
        severity: "medium"
        recommendation: "Add fallback_sources section to source_coordination_plan"
  
  source_selection_accuracy:
    technology_detection: "[0-100]"
    confidence_scoring: "[0-100]"
    fallback_logic: "[0-100]"
    
    test_results:
      react_detection:
        - input: "React TypeScript project"
          expected_confidence: 0.85
          actual_confidence: 0.87
          result: "PASS"
      
      database_detection:
        - input: "SQL migration files"
          expected_routing: "postgresql-mcp-server"
          actual_routing: "postgresql-mcp-server"
          result: "PASS"
  
  integration_validation:
    research_framework: "[0-100]"
    ai_pr_validation: "[0-100]"
    knowledge_vault: "[0-100]"
    
    integration_issues:
      - component: "research orchestrator step 3.5"
        issue: "Source discovery output format needs alignment"
        severity: "low"
        recommendation: "Update output_format to match step 4 expectations"
  
  accessibility_assessment:
    mcp_server_connectivity: "[0-100]"
    authentication_feasibility: "[0-100]"
    rate_limit_handling: "[0-100]"
    
    accessibility_issues:
      - source: "context7-mcp-server"
        issue: "Server response time >2 seconds"
        severity: "medium"
        recommendation: "Implement caching or alternative documentation source"
  
  quality_metrics:
    constitutional_ai_compliance: "[0-100]"
    source_attribution_accuracy: "[0-100]"
    fallback_reliability: "[0-100]"
    
  overall_score: "[0-100]"
  
  recommendations:
    - "Enhance React source mapping with additional fallback sources"
    - "Optimize MCP server response times through caching strategies"
    - "Add integration testing for multi-source workflow coordination"
    - "Implement source quality monitoring and alerting"
  
  critical_issues:
    - count: 0
    - blocking_deployment: false
  
  next_steps:
    - "Review source mapping configurations for completeness"
    - "Test information access framework under load conditions"
    - "Validate cross-system integration points"
    - "Monitor source accessibility and performance metrics"
```

## Framework Integration

### AI Agent Instruction Design Excellence Compliance

**Concrete Specificity:**
- Explicit validation criteria for source mappings and integration points
- Specific test cases for technology detection and source selection
- Clear assessment metrics for accessibility and performance

**External Dependency Elimination:**
- Self-contained validation logic without external service dependencies
- Embedded test patterns and expected outcomes
- Independent validation of each integration component

**Immediate Actionability:**
- Step-by-step validation process with clear tool usage
- Actionable recommendations for identified issues
- Specific remediation steps for common problems

**Constitutional AI Compliance:**
- Ethical assessment of source selection fairness
- No biased technology or vendor preferences
- Constructive improvement recommendations only

### Progressive Context Loading

**Base Context (200 tokens):**
- Source mapping structure validation
- Basic integration point checking
- Technology detection patterns

**Conditional Context (300-500 tokens):**
- Specific technology validation (React, database patterns)
- MCP server connectivity testing
- Multi-source coordination assessment

**Specialized Context (250-400 tokens):**
- Research framework integration validation
- AI-PR validation system coordination
- Performance optimization assessment

## Quality Metrics

### Validation Effectiveness Targets

- **Source Mapping Accuracy**: ≥95% correct technology detection and source routing
- **Integration Compliance**: ≥90% successful integration with research and validation frameworks
- **Accessibility Verification**: ≥95% accuracy in source availability assessment
- **Cross-Reference Validation**: 100% verification of file path accessibility
- **Constitutional Compliance**: ≥99% ethical and unbiased source selection

### Performance Targets

- **Validation Speed**: ≤90 seconds for complete information access framework validation
- **Memory Efficiency**: ≤150MB peak memory usage during validation
- **Integration Testing**: ≤120 seconds for multi-system integration verification
- **Source Testing**: ≤60 seconds for MCP server connectivity validation

### Constitutional AI Validation

- **Accuracy**: ≥95% correct identification of information access issues
- **Completeness**: ≥90% coverage of information access framework scope
- **Consistency**: ≥95% repeatable results across validation runs
- **Responsibility**: Constructive recommendations without vendor bias
- **Transparency**: Clear reasoning for all flagged integration issues

## Integration Notes

### Validator Registry Integration

```yaml
information-access-source-validator:
  location: "meta/validation/validators/information-access/source-validation.md"
  file_patterns: 
    - "meta/information-access/**/*.yaml"
    - "research/findings/**/.meta/research-sources.md"
    - "knowledge-vault/databases/tools_services/views/*.yaml"
  specialization: "Information access framework compliance and source validation"
  dependencies: ["knowledge-vault access", "MCP server connectivity"]
  parallel_safe: true
  estimated_processing_time: "60-90s for complete framework validation"
  quality_score: "pending_measurement"
  constitutional_ai_compliance: true
  framework_compliance_version: "1.0"
```

### Command Integration

This validator integrates with both research workflows and PR validation:
- Research orchestrator step 3.5 source discovery validation
- AI-PR validation technology-specific source usage verification
- Knowledge vault integration and cross-reference validation
- MCP server accessibility and performance monitoring

### Future Enhancements

- **Automated Source Monitoring**: Continuous monitoring of MCP server availability and performance
- **Source Quality Scoring**: Dynamic quality assessment based on response times and reliability
- **Integration Testing Automation**: Automated testing of multi-source workflow coordination
- **Source Discovery Optimization**: Machine learning-based source selection improvement