# Anti-Fiction and Cognitive Contamination Prevention

Apply comprehensive safeguards to prevent academic contamination and fabricated claims in AI agent operations.

## Problem: Academic Contamination Risk

Academic knowledge mixed with AI agent instructions causes cognitive contamination leading to:
- **Fiction Generation**: Making up statistics instead of using actual data  
- **Academic Creep**: Adding research-style validation where none exists
- **Performance Metric Fabrication**: Creating credible-sounding but false statistics
- **Instruction Pollution**: Mixing research findings with actionable commands

**Root Cause**: AI agents become contaminated when processing academic content alongside operational instructions.

## Enhanced Anti-Fiction Safeguards

### Safeguard 1: Real-Time Fact Validation
**BEFORE ANY NUMERICAL CLAIM**:
- [ ] Source identified and verifiable (file path + line number)
- [ ] Actual measurement vs. estimation clearly labeled  
- [ ] Evidence trail documented with timestamps
- [ ] Anti-fiction protocol checkpoint passed

### Safeguard 2: Mandatory Evidence Citation
**EVERY CLAIM MUST INCLUDE**:
- **Verified Data**: `Source: file_path:line_number` OR
- **Estimation**: `Estimated based on [specific methodology]` OR  
- **Analysis**: `Opinion based on [criteria] - not measured` OR
- **Unknown**: `No source available - cannot verify`

### Safeguard 3: Academic Content Quarantine
**WHEN ANALYZING ACADEMIC CONTENT**:
- [ ] Process in analysis mode separate from execution mode
- [ ] Document academic claims as "Source Claims" not "Verified Data"
- [ ] Use distinct formatting for academic vs. factual content
- [ ] Apply cognitive firewall between analysis and operational reporting

### Safeguard 4: Contamination Detection
**DETECT ACADEMIC CONTAMINATION PATTERNS**:
- Using research-style language in operational reports
- Adding percentage claims without source verification
- Generating "effectiveness" or "success rate" statistics
- Including academic justification in actionable instructions

### Safeguard 5: Knowledge-Vault Access Control
**STRICT ACCESS RESTRICTIONS**:
- **Normal Operations**: AI agents MUST NOT access `knowledge-vault/` files
- **Research Tasks**: Only when explicitly instructed by humans
- **Academic Content**: Process separately from operational instructions
- **Cross-References**: Only reference actionable instruction files

## Cognitive Contamination Prevention Protocols

### Protocol 1: Content Type Identification
**BEFORE PROCESSING ANY FILE**:
1. Identify content type: Academic/Research vs. Actionable Instructions
2. Apply appropriate processing mode: Analysis vs. Execution  
3. Maintain cognitive separation between modes
4. Prevent academic style from influencing operational reporting

### Protocol 2: Evidence-Based Reporting
**FOR ALL CLAIMS AND STATISTICS**:
1. Verify source: Actual data vs. estimation vs. opinion
2. Label uncertainty: High/Medium/Low confidence with reasoning
3. Provide evidence trail: File paths, line numbers, timestamps
4. Avoid fabrication: "Unknown" is acceptable, fiction is not

### Protocol 3: Academic Style Prevention
**OPERATIONAL REPORTING STANDARDS**:
1. Use direct, actionable language only
2. Avoid academic phrases: "research shows", "studies indicate" 
3. Focus on configuration parameters and thresholds
4. Eliminate research justification from instructions

## Knowledge-Vault Restrictions

**AI agents are RESTRICTED from accessing `knowledge-vault/` during normal operations.**

**Knowledge-Vault Contains**:
- Research findings and academic validation
- Performance metrics and effectiveness statistics
- Success stories and implementation reports  
- Academic justification and research validation

**Access Policy**:
- **Forbidden**: Normal operational tasks
- **Permitted**: When explicitly instructed by humans for research/reporting
- **Purpose**: Prevent cognitive contamination during instruction execution

## Enforcement and Validation

### Anti-Fiction Validation Checklist
**Before completing any task involving claims or statistics**:
- [ ] All numerical claims verified with sources
- [ ] No fabricated performance metrics included
- [ ] Academic content processed separately from instructions
- [ ] Knowledge-vault access restrictions followed
- [ ] Evidence trail documented for all claims

### Contamination Recovery Protocol
**If academic contamination detected**:
1. **Stop Processing**: Halt current task immediately
2. **Identify Source**: Locate contaminating academic content
3. **Quarantine Content**: Separate academic from operational content
4. **Restart Task**: Begin again with clean, actionable instructions only
5. **Document Incident**: Record contamination source for prevention

**ENFORCEMENT**: Violations of anti-fiction safeguards trigger immediate task invalidation and protocol restart.