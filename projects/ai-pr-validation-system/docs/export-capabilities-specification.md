# Export Capabilities Specification

## Overview

This specification defines comprehensive export capabilities for the AI PR validation system, enabling flexible output formats (JSON, HTML, Markdown) for different integration scenarios and consumption patterns.

**Foundation**: Built on proven validation framework achieving advanced validation framework with role-aware knowledge management system.

---

## 🎯 Export Format Overview

### Supported Export Formats
```yaml
export_formats:
  json:
    purpose: "API integration, data processing, programmatic consumption"
    structure: "Structured data with full validation results"
    use_cases: ["CI/CD integration", "Dashboard APIs", "Data analytics", "Webhook payloads"]
    
  html:
    purpose: "Web display, interactive dashboards, email reports"
    structure: "Styled HTML with interactive elements and visualizations"
    use_cases: ["Web dashboards", "Email notifications", "Archive storage", "Management reports"]
    
  markdown:
    purpose: "Documentation, GitHub integration, human-readable reports"
    structure: "Formatted markdown with tables and visual indicators"
    use_cases: ["GitHub PR comments", "Documentation", "Team communications", "Archive documentation"]
    
  pdf:
    purpose: "Executive reports, audit documentation, formal presentations"
    structure: "Professional formatted document with charts and visualizations"
    use_cases: ["Executive reporting", "Compliance documentation", "Client presentations", "Audit trails"]
```

---

## 📊 JSON Export Specification

### Complete JSON Schema
```typescript
interface PRValidationReportJSON {
  metadata: ReportMetadata;
  executiveSummary: ExecutiveSummary;
  intentImplementationAnalysis: IntentImplementationAnalysis;
  multiRoleAnalysis: MultiRoleAnalysis;
  fileTypeAnalysis: FileTypeAnalysis;
  actionableRecommendations: ActionableRecommendations;
  validationMetrics: ValidationMetrics;
  finalRecommendation: FinalRecommendation;
}

interface ReportMetadata {
  reportId: string;
  prNumber: number;
  prTitle: string;
  prAuthor: string;
  repositoryName: string;
  generatedAt: Date;
  validationSystemVersion: string;
  processingTimeSeconds: number;
  aiAgentsUsed: string[];
}

interface ExecutiveSummary {
  overallRiskLevel: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  intentAlignmentScore: number; // 0-100
  validationStatus: 'APPROVED' | 'CONDITIONAL' | 'NEEDS_WORK' | 'CRITICAL';
  filesChanged: number;
  technologiesDetected: string[];
  issueBreakdown: {
    critical: number;
    important: number;
    minor: number;
    passed: number;
  };
}

interface IntentImplementationAnalysis {
  semanticAlignmentScore: number; // 0-100
  approvalThreshold: number; // 85
  status: 'APPROVED' | 'CONDITIONAL' | 'NEEDS_WORK' | 'CRITICAL';
  dimensionBreakdown: {
    statedPurposeMatch: DimensionScore;
    scopeConsistency: DimensionScore;
    implementationCompleteness: DimensionScore;
    undisclosedChanges: DimensionScore;
  };
  criticalIntentIssues: IntentIssue[];
}

interface DimensionScore {
  score: number; // 0-100
  status: 'EXCELLENT' | 'GOOD' | 'FAIR' | 'POOR' | 'CRITICAL';
  details: string;
  weight: number; // percentage weight in overall score
}

interface MultiRoleAnalysis {
  roleExpertiseMatrix: {
    [dimension: string]: {
      [role: string]: RoleAnalysisResult;
    };
  };
  roleSpecificVerdicts: {
    architect: RoleVerdict;
    frontendDev: RoleVerdict;
    performance: RoleVerdict;
    security: RoleVerdict;
  };
  crossRoleMetrics: {
    consensusRate: number;
    coordinationEfficiency: number;
    averageConfidence: number;
  };
}

interface RoleAnalysisResult {
  focusLevel: 'HIGH' | 'MEDIUM' | 'LOW';
  score: number; // 0-10
  confidence: number; // 0-100
  keyFindings: string[];
  recommendations: string[];
}

interface RoleVerdict {
  verdict: string;
  confidence: number;
  summary: string;
  keyFindings: Finding[];
  recommendations: Recommendation[];
  processingTime: number;
}

interface FileTypeAnalysis {
  technologyBreakdown: TechnologyAnalysis[];
  detectionAccuracy: number;
  contextLoadingMetrics: {
    [technology: string]: {
      agentRole: string;
      contextSource: string;
      knowledgeLines: number;
      loadingTime: number;
    };
  };
}

interface TechnologyAnalysis {
  technology: string;
  fileCount: number;
  filesAnalyzed: string[];
  primaryAgentRole: string;
  contextSources: string[];
  validationResults: {
    qualityScore: number;
    securityScore: number;
    performanceScore: number;
    issuesCount: number;
  };
  keyFindings: Finding[];
}

interface ActionableRecommendations {
  priorityMatrix: PriorityRecommendation[];
  criticalActions: CriticalAction[];
  highPriorityActions: HighPriorityAction[];
  mediumPriorityImprovements: MediumPriorityImprovement[];
  lowPriorityEnhancements: LowPriorityEnhancement[];
  businessImpactAssessment: BusinessImpactAssessment;
}

interface PriorityRecommendation {
  priority: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW' | 'ENHANCEMENT';
  issue: string;
  expertRole: string;
  effortEstimate: string;
  businessImpact: string;
  recommendation: string;
  timelineDeadline?: Date;
}

interface ValidationMetrics {
  systemPerformance: SystemPerformanceMetrics;
  agentPerformance: AgentPerformanceMetrics;
  qualityAssurance: QualityAssuranceMetrics;
  constitutionalCompliance: ConstitutionalComplianceMetrics;
}

interface SystemPerformanceMetrics {
  totalProcessingTime: number;
  averageAgentResponseTime: number;
  filePatternRecognitionAccuracy: number;
  intentValidationAccuracy: number;
  overallSystemEffectiveness: number;
}

interface AgentPerformanceMetrics {
  [agentRole: string]: {
    effectivenessScore: number;
    processingTime: number;
    issuesFound: number;
    falsePositiveRate: number;
    knowledgeUtilization: number;
  };
}

interface FinalRecommendation {
  overallAssessment: string;
  finalVerdict: 'APPROVED' | 'CONDITIONAL_APPROVAL' | 'NEEDS_WORK' | 'SECURITY_REVIEW_REQUIRED' | 'MAJOR_REVISION_REQUIRED';
  weightedOverallScore: number;
  decisionMatrix: DecisionCriterion[];
  nextSteps: NextStep[];
  escalationRequired: boolean;
  approvalConditions?: string[];
}
```

### JSON Export Example
```json
{
  "metadata": {
    "reportId": "pr-validation-20250726-142035",
    "prNumber": 1234,
    "prTitle": "feat: Add user authentication with JWT tokens to dashboard",
    "prAuthor": "developer123",
    "repositoryName": "mycompany/webapp",
    "generatedAt": "2025-07-26T14:20:35.000Z",
    "validationSystemVersion": "2.0.0",
    "processingTimeSeconds": 127,
    "aiAgentsUsed": ["architect", "frontend-dev", "performance", "security"]
  },
  "executiveSummary": {
    "overallRiskLevel": "MEDIUM",
    "intentAlignmentScore": 78,
    "validationStatus": "CONDITIONAL",
    "filesChanged": 8,
    "technologiesDetected": ["typescript", "react", "nodejs"],
    "issueBreakdown": {
      "critical": 1,
      "important": 3,
      "minor": 2,
      "passed": 12
    }
  },
  "intentImplementationAnalysis": {
    "semanticAlignmentScore": 78,
    "approvalThreshold": 85,
    "status": "CONDITIONAL",
    "dimensionBreakdown": {
      "statedPurposeMatch": {
        "score": 85,
        "status": "GOOD",
        "details": "Authentication system implemented as described",
        "weight": 30
      },
      "scopeConsistency": {
        "score": 72,
        "status": "FAIR",
        "details": "Minor scope expansion with dashboard updates",
        "weight": 25
      },
      "implementationCompleteness": {
        "score": 80,
        "status": "GOOD",
        "details": "Core functionality complete, missing error handling",
        "weight": 25
      },
      "undisclosedChanges": {
        "score": 75,
        "status": "FAIR",
        "details": "Some configuration changes not mentioned in description",
        "weight": 20
      }
    },
    "criticalIntentIssues": []
  }
}
```

---

## 🌐 HTML Export Specification

### HTML Template Structure
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PR Validation Report #{{PR_NUMBER}} - {{PR_TITLE}}</title>
    <style>
        /* Enhanced CSS for professional report presentation */
        .report-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }
        
        .executive-summary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 12px;
            margin-bottom: 30px;
        }
        
        .metric-card {
            background: white;
            border: 1px solid #e1e5e9;
            border-radius: 8px;
            padding: 20px;
            margin: 15px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .risk-critical { border-left: 5px solid #dc3545; }
        .risk-high { border-left: 5px solid #fd7e14; }
        .risk-medium { border-left: 5px solid #ffc107; }
        .risk-low { border-left: 5px solid #28a745; }
        
        .role-matrix {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .progress-bar {
            width: 100%;
            height: 20px;
            background-color: #e9ecef;
            border-radius: 10px;
            overflow: hidden;
            margin: 10px 0;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #28a745 0%, #20c997 50%, #17a2b8 100%);
            transition: width 0.3s ease;
        }
        
        .recommendation-priority {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
            text-transform: uppercase;
        }
        
        .priority-critical { background: #dc3545; color: white; }
        .priority-high { background: #fd7e14; color: white; }
        .priority-medium { background: #ffc107; color: black; }
        .priority-low { background: #28a745; color: white; }
        
        .interactive-chart {
            height: 300px;
            margin: 20px 0;
        }
        
        @media (max-width: 768px) {
            .role-matrix {
                grid-template-columns: 1fr;
            }
        }
        
        @media print {
            .report-container {
                max-width: none;
                padding: 0;
            }
            
            .interactive-chart {
                height: 200px;
            }
        }
    </style>
    
    <!-- Chart.js for interactive visualizations -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <div class="report-container">
        <!-- Executive Summary Section -->
        <div class="executive-summary">
            <h1>🎯 PR Validation Report</h1>
            <div class="summary-grid">
                <div class="summary-item">
                    <h3>{{PR_TITLE}}</h3>
                    <p>PR #{{PR_NUMBER}} by {{PR_AUTHOR}}</p>
                    <p>Generated: {{TIMESTAMP}}</p>
                </div>
                <div class="summary-item">
                    <div class="metric-large">
                        <span class="metric-value">{{INTENT_SCORE}}/100</span>
                        <span class="metric-label">Intent Alignment</span>
                    </div>
                </div>
                <div class="summary-item">
                    <div class="risk-indicator risk-{{RISK_LEVEL_CLASS}}">
                        {{RISK_LEVEL}}
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Intent Implementation Analysis -->
        <div class="metric-card">
            <h2>🔍 Intent vs Implementation Analysis</h2>
            
            <div class="intent-score">
                <h3>Semantic Alignment Score: {{INTENT_SCORE}}/100</h3>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {{INTENT_SCORE}}%"></div>
                </div>
                <p class="threshold-info">Threshold: ≥85 for approval | Status: <strong>{{INTENT_STATUS}}</strong></p>
            </div>
            
            <div class="intent-breakdown">
                <h4>Detailed Breakdown</h4>
                <table class="intent-table">
                    <thead>
                        <tr>
                            <th>Aspect</th>
                            <th>Score</th>
                            <th>Status</th>
                            <th>Details</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Stated Purpose Match</td>
                            <td>{{PURPOSE_SCORE}}/100</td>
                            <td><span class="status-{{PURPOSE_STATUS_CLASS}}">{{PURPOSE_STATUS}}</span></td>
                            <td>{{PURPOSE_DETAILS}}</td>
                        </tr>
                        <!-- Additional intent breakdown rows -->
                    </tbody>
                </table>
            </div>
        </div>
        
        <!-- Multi-Role Analysis Matrix -->
        <div class="metric-card">
            <h2>👥 Multi-Role Expert Analysis</h2>
            
            <div class="role-matrix">
                <div class="role-card architect-card">
                    <h3>🏗️ Architect</h3>
                    <div class="role-verdict">{{ARCH_VERDICT}}</div>
                    <div class="role-confidence">Confidence: {{ARCH_CONFIDENCE}}%</div>
                    <div class="role-summary">{{ARCH_SUMMARY}}</div>
                </div>
                
                <div class="role-card frontend-card">
                    <h3>🎨 Frontend Developer</h3>
                    <div class="role-verdict">{{FRONTEND_VERDICT}}</div>
                    <div class="role-confidence">Confidence: {{FRONTEND_CONFIDENCE}}%</div>
                    <div class="role-summary">{{FRONTEND_SUMMARY}}</div>
                </div>
                
                <div class="role-card performance-card">
                    <h3>⚡ Performance Specialist</h3>
                    <div class="role-verdict">{{PERF_VERDICT}}</div>
                    <div class="role-confidence">Confidence: {{PERF_CONFIDENCE}}%</div>
                    <div class="role-summary">{{PERF_SUMMARY}}</div>
                </div>
                
                <div class="role-card security-card">
                    <h3>🔒 Security Specialist</h3>
                    <div class="role-verdict">{{SEC_VERDICT}}</div>
                    <div class="role-confidence">Confidence: {{SEC_CONFIDENCE}}%</div>
                    <div class="role-summary">{{SEC_SUMMARY}}</div>
                </div>
            </div>
            
            <!-- Interactive Analysis Matrix Chart -->
            <div class="interactive-chart">
                <canvas id="roleAnalysisChart"></canvas>
            </div>
        </div>
        
        <!-- Actionable Recommendations -->
        <div class="metric-card">
            <h2>🎯 Actionable Recommendations</h2>
            
            <div class="recommendations-list">
                {{#each PRIORITY_ISSUES}}
                <div class="recommendation-item priority-{{priority_class}}">
                    <div class="recommendation-header">
                        <span class="recommendation-priority priority-{{priority_class}}">{{priority}}</span>
                        <h4>{{issue}}</h4>
                    </div>
                    <div class="recommendation-details">
                        <p><strong>Expert:</strong> {{expert_role}}</p>
                        <p><strong>Effort:</strong> {{effort_estimate}}</p>
                        <p><strong>Impact:</strong> {{business_impact}}</p>
                        <p><strong>Recommendation:</strong> {{recommendation}}</p>
                    </div>
                </div>
                {{/each}}
            </div>
        </div>
        
        <!-- Validation Metrics Dashboard -->
        <div class="metric-card">
            <h2>📊 Validation Metrics</h2>
            
            <div class="metrics-grid">
                <div class="metric-item">
                    <h4>Processing Time</h4>
                    <div class="metric-value">{{TOTAL_TIME}}s</div>
                </div>
                <div class="metric-item">
                    <h4>System Effectiveness</h4>
                    <div class="metric-value">{{SYSTEM_EFFECTIVENESS}}%</div>
                </div>
                <div class="metric-item">
                    <h4>Constitutional Compliance</h4>
                    <div class="metric-value">{{CONSTITUTIONAL_COMPLIANCE}}%</div>
                </div>
            </div>
            
            <!-- Interactive Performance Chart -->
            <div class="interactive-chart">
                <canvas id="performanceChart"></canvas>
            </div>
        </div>
        
        <!-- Final Recommendation -->
        <div class="metric-card final-recommendation">
            <h2>📋 Final Recommendation</h2>
            <div class="final-verdict {{FINAL_VERDICT_CLASS}}">
                <h3>{{FINAL_VERDICT}}</h3>
            </div>
            <div class="final-summary">
                {{FINAL_SUMMARY}}
            </div>
            <div class="next-steps">
                <h4>Next Steps:</h4>
                <ol>
                    {{#each NEXT_STEPS}}
                    <li><strong>{{step_title}}:</strong> {{step_description}}</li>
                    {{/each}}
                </ol>
            </div>
        </div>
    </div>
    
    <script>
        // Interactive Chart Configurations
        document.addEventListener('DOMContentLoaded', function() {
            // Role Analysis Chart
            const roleCtx = document.getElementById('roleAnalysisChart').getContext('2d');
            new Chart(roleCtx, {
                type: 'radar',
                data: {
                    labels: ['Component Architecture', 'User Experience', 'Performance', 'Security', 'Maintainability', 'Testing'],
                    datasets: [
                        {
                            label: 'Architect',
                            data: [{{ARCH_SCORES}}],
                            borderColor: 'rgb(75, 192, 192)',
                            backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        },
                        {
                            label: 'Frontend Dev',
                            data: [{{FRONTEND_SCORES}}],
                            borderColor: 'rgb(255, 99, 132)',
                            backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        },
                        {
                            label: 'Performance',
                            data: [{{PERF_SCORES}}],
                            borderColor: 'rgb(255, 205, 86)',
                            backgroundColor: 'rgba(255, 205, 86, 0.2)',
                        },
                        {
                            label: 'Security',
                            data: [{{SEC_SCORES}}],
                            borderColor: 'rgb(201, 203, 207)',
                            backgroundColor: 'rgba(201, 203, 207, 0.2)',
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        r: {
                            beginAtZero: true,
                            max: 10
                        }
                    }
                }
            });
            
            // Performance Metrics Chart
            const perfCtx = document.getElementById('performanceChart').getContext('2d');
            new Chart(perfCtx, {
                type: 'bar',
                data: {
                    labels: ['Architect', 'Frontend Dev', 'Performance', 'Security'],
                    datasets: [
                        {
                            label: 'Effectiveness Score (%)',
                            data: [{{AGENT_EFFECTIVENESS_SCORES}}],
                            backgroundColor: 'rgba(54, 162, 235, 0.5)',
                            borderColor: 'rgba(54, 162, 235, 1)',
                            borderWidth: 1
                        },
                        {
                            label: 'Processing Time (s)',
                            data: [{{AGENT_PROCESSING_TIMES}}],
                            backgroundColor: 'rgba(255, 99, 132, 0.5)',
                            borderColor: 'rgba(255, 99, 132, 1)',
                            borderWidth: 1,
                            yAxisID: 'y1'
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            type: 'linear',
                            display: true,
                            position: 'left',
                        },
                        y1: {
                            type: 'linear',
                            display: true,
                            position: 'right',
                            grid: {
                                drawOnChartArea: false,
                            },
                        }
                    }
                }
            });
        });
    </script>
</body>
</html>
```

---

## 📝 Markdown Export Specification

### Enhanced Markdown Template
```markdown
# PR Validation Report

**PR**: {{PR_TITLE}}  
**Number**: [#{{PR_NUMBER}}]({{PR_URL}})  
**Author**: [@{{PR_AUTHOR}}]({{AUTHOR_URL}})  
**Generated**: {{TIMESTAMP}}  
**System Version**: v{{VERSION}}

---

## 🎯 Executive Summary

### Quick Status Overview
| Metric | Value | Status |
|--------|-------|--------|
| **Overall Risk** | {{RISK_LEVEL}} {{RISK_EMOJI}} | {{RISK_STATUS}} |
| **Intent Alignment** | {{INTENT_SCORE}}/100 | {{INTENT_STATUS}} |
| **Files Changed** | {{FILES_COUNT}} files | {{FILES_STATUS}} |
| **Technologies** | {{TECH_LIST}} | {{TECH_STATUS}} |

### Issue Breakdown
- 🔴 **Critical**: {{CRITICAL_COUNT}} issues
- 🟡 **Important**: {{IMPORTANT_COUNT}} issues  
- 🟢 **Minor**: {{MINOR_COUNT}} issues
- ✅ **Passed**: {{PASSED_COUNT}} validations

---

## 🔍 Intent vs Implementation Analysis

### Semantic Alignment Assessment
```
Intent Alignment Score: {{INTENT_SCORE}}/100

{{PROGRESS_BAR_ASCII}}

Threshold: ≥85 for approval
Status: {{INTENT_STATUS}}
```

### Detailed Breakdown

| Aspect | Score | Status | Weight | Details |
|--------|-------|--------|--------|---------|
| **Stated Purpose Match** | {{PURPOSE_SCORE}}/100 | {{PURPOSE_STATUS}} | 30% | {{PURPOSE_DETAILS}} |
| **Scope Consistency** | {{SCOPE_SCORE}}/100 | {{SCOPE_STATUS}} | 25% | {{SCOPE_DETAILS}} |
| **Implementation Completeness** | {{COMPLETENESS_SCORE}}/100 | {{COMPLETENESS_STATUS}} | 25% | {{COMPLETENESS_DETAILS}} |
| **Undisclosed Changes** | {{UNDISCLOSED_SCORE}}/100 | {{UNDISCLOSED_STATUS}} | 20% | {{UNDISCLOSED_DETAILS}} |

{{#if INTENT_ISSUES}}
### 🚨 Critical Intent Issues
{{#each INTENT_ISSUES}}
- **{{severity}}**: {{description}}
  - **Impact**: {{impact}}
  - **Recommendation**: {{recommendation}}
{{/each}}
{{else}}
✅ **No critical intent alignment issues detected**
{{/if}}

---

## 👥 Multi-Role Expert Analysis

### 📊 Role Expertise Matrix

| Analysis Dimension | 🏗️ Architect | 🎨 Frontend | ⚡ Performance | 🔒 Security | Overall |
|-------------------|---------------|-------------|----------------|-------------|---------|
| **Component Architecture** | 🔥 {{ARCH_COMPONENT}} | ⚡ {{FRONTEND_COMPONENT}} | 💭 {{PERF_COMPONENT}} | 💭 {{SEC_COMPONENT}} | **{{COMPONENT_OVERALL}}/10** |
| **User Experience** | 💭 {{ARCH_UX}} | 🔥 {{FRONTEND_UX}} | ⚡ {{PERF_UX}} | 💭 {{SEC_UX}} | **{{UX_OVERALL}}/10** |
| **Performance** | ⚡ {{ARCH_PERF}} | ⚡ {{FRONTEND_PERF}} | 🔥 {{PERF_PERF}} | 💭 {{SEC_PERF}} | **{{PERF_OVERALL}}/10** |
| **Security** | 💭 {{ARCH_SEC}} | 💭 {{FRONTEND_SEC}} | 💭 {{PERF_SEC}} | 🔥 {{SEC_SEC}} | **{{SEC_OVERALL}}/10** |
| **Maintainability** | 🔥 {{ARCH_MAINT}} | 🔥 {{FRONTEND_MAINT}} | ⚡ {{PERF_MAINT}} | ⚡ {{SEC_MAINT}} | **{{MAINT_OVERALL}}/10** |

**Legend**: 🔥 High Focus | ⚡ Medium Focus | 💭 Low Focus

### Role-Specific Verdicts

#### 🏗️ Architecture Review
**Verdict**: {{ARCH_VERDICT}} | **Confidence**: {{ARCH_CONFIDENCE}}%

{{ARCH_SUMMARY}}

<details>
<summary><strong>Architectural Concerns</strong></summary>

{{#each ARCH_CONCERNS}}
- **{{severity}}**: {{concern}}
  - **Impact**: {{impact}}
  - **Solution**: {{solution}}
{{/each}}
</details>

#### 🎨 Frontend Development Review
**Verdict**: {{FRONTEND_VERDICT}} | **Confidence**: {{FRONTEND_CONFIDENCE}}%

{{FRONTEND_SUMMARY}}

<details>
<summary><strong>UX Assessment</strong></summary>

{{#each FRONTEND_UX_ISSUES}}
- **{{severity}}**: {{issue}}
  - **User Impact**: {{user_impact}}
  - **Fix**: {{fix}}
{{/each}}
</details>

#### ⚡ Performance Review
**Verdict**: {{PERF_VERDICT}} | **Confidence**: {{PERF_CONFIDENCE}}%

{{PERF_SUMMARY}}

<details>
<summary><strong>Performance Impact</strong></summary>

{{#each PERF_IMPACTS}}
- **{{metric}}**: {{before}} → {{after}} ({{change}})
  - **Significance**: {{significance}}
  - **Optimization**: {{optimization}}
{{/each}}
</details>

#### 🔒 Security Review
**Verdict**: {{SEC_VERDICT}} | **Confidence**: {{SEC_CONFIDENCE}}%

{{SEC_SUMMARY}}

<details>
<summary><strong>Security Risks</strong></summary>

{{#each SEC_RISKS}}
- **{{severity}}**: {{vulnerability}}
  - **CVSS Score**: {{cvss_score}}
  - **Mitigation**: {{mitigation}}
{{/each}}
</details>

---

## 📁 Technology-Specific Analysis

{{#each TECHNOLOGIES}}
### {{tech_name}} Analysis
**Files**: {{file_count}} files | **Agent**: {{agent_role}} | **Context**: {{context_source}}

**Validation Results**:
- Quality: {{quality_score}}/100
- Security: {{security_score}}/100
- Performance: {{performance_score}}/100

**Key Findings**:
{{#each findings}}
- **{{severity}}**: {{finding}}
{{/each}}

<details>
<summary><strong>Files Analyzed</strong></summary>

{{#each files}}
- [`{{file_path}}`]({{file_url}}) ({{change_type}}, {{lines_changed}} lines)
{{/each}}
</details>

{{/each}}

---

## 🎯 Actionable Recommendations

### Priority Issue Matrix

| Priority | Issue | Expert | Effort | Impact | Recommendation |
|----------|-------|--------|--------|--------|----------------|
{{#each PRIORITY_ISSUES}}
| {{priority_badge}} | {{issue}} | {{expert_role}} | {{effort_estimate}} | {{business_impact}} | {{recommendation}} |
{{/each}}

### 🔴 Critical Actions Required

{{#each CRITICAL_ACTIONS}}
#### {{action_title}}
**Why Critical**: {{justification}}

**Steps**:
{{#each steps}}
{{@index}}. {{this}}
{{/each}}

**Timeline**: {{timeline}} | **Owner**: {{recommended_owner}}

---
{{/each}}

### 🟡 Important Improvements

{{#each IMPORTANT_IMPROVEMENTS}}
#### {{improvement_title}}
**Benefit**: {{benefit}} | **Effort**: {{effort}} | **Timeline**: {{timeline}}

---
{{/each}}

### 🟢 Minor Enhancements

{{#each MINOR_ENHANCEMENTS}}
- **{{enhancement}}**: {{description}} ({{effort}})
{{/each}}

---

## 📊 Validation Metrics

### System Performance
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| **Processing Time** | {{TOTAL_TIME}}s | <300s | {{TIME_STATUS}} |
| **System Effectiveness** | {{SYSTEM_EFFECTIVENESS}}% | >90% | {{EFFECTIVENESS_STATUS}} |
| **Pattern Recognition** | {{PATTERN_ACCURACY}}% | >95% | {{PATTERN_STATUS}} |

### Agent Performance
| Agent | Effectiveness | Response Time | Issues Found | False Positives |
|-------|---------------|---------------|---------------|-----------------|
| Architect | {{ARCH_EFFECTIVENESS}}% | {{ARCH_TIME}}s | {{ARCH_ISSUES}} | {{ARCH_FP}}% |
| Frontend | {{FRONTEND_EFFECTIVENESS}}% | {{FRONTEND_TIME}}s | {{FRONTEND_ISSUES}} | {{FRONTEND_FP}}% |
| Performance | {{PERF_EFFECTIVENESS}}% | {{PERF_TIME}}s | {{PERF_ISSUES}} | {{PERF_FP}}% |
| Security | {{SEC_EFFECTIVENESS}}% | {{SEC_TIME}}s | {{SEC_ISSUES}} | {{SEC_FP}}% |

---

## 📋 Final Recommendation

### Overall Assessment
**{{FINAL_VERDICT}}**

{{FINAL_SUMMARY}}

### Decision Matrix
| Criteria | Status | Weight | Score |
|----------|--------|--------|-------|
| Intent Alignment | {{INTENT_STATUS}} | 30% | {{INTENT_WEIGHTED}} |
| Security | {{SECURITY_STATUS}} | 25% | {{SECURITY_WEIGHTED}} |
| Code Quality | {{QUALITY_STATUS}} | 20% | {{QUALITY_WEIGHTED}} |
| Performance | {{PERF_STATUS}} | 15% | {{PERF_WEIGHTED}} |
| UX Impact | {{UX_STATUS}} | 10% | {{UX_WEIGHTED}} |

**Weighted Score**: {{WEIGHTED_TOTAL}}/100

### Next Steps
{{#each NEXT_STEPS}}
{{@index}}. **{{step_title}}**: {{step_description}}
{{/each}}

---

<sub>**Report Generated by AI PR Validation System v{{VERSION}}**</sub>  
<sub>Revolutionary Intent-Implementation Validator | Role-Aware Knowledge Management</sub>  
<sub>Framework Effectiveness: {{FRAMEWORK_EFFECTIVENESS}}% | Constitutional AI Compliance: {{CONSTITUTIONAL_COMPLIANCE}}%</sub>
```

---

## 🔧 Export Implementation Framework

### Export Service Interface
```typescript
interface ExportService {
  exportToJSON(reportData: PRValidationReportData): string;
  exportToHTML(reportData: PRValidationReportData, options?: HTMLExportOptions): string;
  exportToMarkdown(reportData: PRValidationReportData, options?: MarkdownExportOptions): string;
  exportToPDF(reportData: PRValidationReportData, options?: PDFExportOptions): Buffer;
}

interface ExportOptions {
  includeRawData: boolean;
  compressOutput: boolean;
  customTemplate?: string;
  theme?: 'light' | 'dark' | 'corporate';
}

interface HTMLExportOptions extends ExportOptions {
  includeInteractiveCharts: boolean;
  embedAssets: boolean;
  responsiveDesign: boolean;
}

interface MarkdownExportOptions extends ExportOptions {
  includeCollapsibleSections: boolean;
  generateTableOfContents: boolean;
  linkToFiles: boolean;
}

interface PDFExportOptions extends ExportOptions {
  pageSize: 'A4' | 'Letter' | 'Legal';
  orientation: 'portrait' | 'landscape';
  includeCharts: boolean;
  headerFooter: boolean;
}
```

### Template Engine Integration
```typescript
class ReportExporter {
  private templateEngine: TemplateEngine;
  private chartGenerator: ChartGenerator;
  
  constructor() {
    this.templateEngine = new HandlebarsTemplateEngine();
    this.chartGenerator = new ChartJSGenerator();
  }
  
  async exportReport(
    reportData: PRValidationReportData,
    format: 'json' | 'html' | 'markdown' | 'pdf',
    options: ExportOptions = {}
  ): Promise<ExportResult> {
    
    // Prepare template data
    const templateData = this.prepareTemplateData(reportData);
    
    // Generate format-specific output
    switch (format) {
      case 'json':
        return this.generateJSON(templateData, options);
      case 'html':
        return this.generateHTML(templateData, options as HTMLExportOptions);
      case 'markdown':
        return this.generateMarkdown(templateData, options as MarkdownExportOptions);
      case 'pdf':
        return this.generatePDF(templateData, options as PDFExportOptions);
      default:
        throw new Error(`Unsupported export format: ${format}`);
    }
  }
  
  private prepareTemplateData(reportData: PRValidationReportData): TemplateData {
    return {
      ...reportData,
      // Add computed fields
      PROGRESS_BAR_ASCII: this.generateProgressBar(reportData.intentScore),
      RISK_EMOJI: this.getRiskEmoji(reportData.riskLevel),
      FORMATTED_TIMESTAMP: this.formatTimestamp(reportData.timestamp),
      // Add charts data for HTML export
      CHART_DATA: this.chartGenerator.prepareChartData(reportData)
    };
  }
}
```

This comprehensive export capabilities specification enables flexible output generation for the AI PR validation system, supporting various integration scenarios and consumption patterns while maintaining the proven validation quality and effectiveness.