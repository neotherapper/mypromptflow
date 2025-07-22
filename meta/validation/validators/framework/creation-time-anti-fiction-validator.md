# Creation-Time Anti-Fiction Validation Framework

**Purpose**: Prevent fabricated metrics and unverifiable statistics during content creation

## Validation Trigger Patterns

**Pre-Creation Validation**:
- Detect percentage claims: `\d+%`, `\d+\.\d+%`
- Detect performance metrics: `\d+ms`, `\d+s`, `≤\d+`, `≥\d+`
- Detect precision claims: `\d+\.\d+%`, `accuracy of \d+%`
- Detect effectiveness claims: `achieving \d+%`, `providing \d+%`

**Evidence Requirements**:
- Source verification: `Source: file_path:line_number`
- Measurement basis: `Measured via [specific method]`
- Estimation clarity: `Estimated based on [methodology]`
- Opinion labeling: `Assessment based on [criteria]`

## Validation Process

**Step 1: Content Analysis**
Scan content for numeric claims and statistical assertions before creation

**Step 2: Evidence Verification**
For each numeric claim, require one of:
- Direct source reference with file path
- Explicit estimation methodology
- Clear opinion/assessment labeling
- Removal and replacement with qualitative description

**Step 3: Alternative Recommendations**
Suggest evidence-based alternatives:
- `"93% effectiveness"` → `"high effectiveness"`
- `"≤4.2ms response time"` → `"fast response time"`
- `"68% token reduction"` → `"significant token reduction"`
- `"99% accuracy"` → `"high accuracy"`

**Step 4: Creation Gate**
Block content creation until all fabricated metrics are addressed

## Integration Points

**With AI Agent Instruction Design Excellence Framework**:
- Constitutional AI compliance validation
- Vagueness detection enhancement
- Evidence-based instruction writing enforcement

**With Command Enhancement Workflow**:
- Apply during command transformation
- Validate before file writing
- Enforce evidence standards

**With Research Documentation**:
- Require source tracking
- Validate research claims
- Prevent academic contamination

## Success Criteria

**Prevention Effectiveness**:
- Zero fabricated metrics in new content
- All numeric claims properly sourced
- Clear distinction between measurement and estimation
- Honest reporting standards maintained

**Integration Success**:
- Seamless workflow integration
- No false positive blocking of legitimate data
- Clear guidance for content creators
- Evidence-based alternatives provided

This framework addresses the root cause of fabricated metrics by implementing validation at content creation time rather than post-creation detection.