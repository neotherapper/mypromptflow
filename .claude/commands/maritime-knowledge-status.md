Check status and completeness of maritime insurance knowledge base: $ARGUMENTS

## Maritime Knowledge Status Check:

1. **Knowledge Base Health Assessment**
   
   Check completeness across all maritime knowledge areas:
   
   - **Risk Assessment Knowledge**: War risk, voyage risk, static vessel risk models
   - **Regulatory Knowledge**: Sanctions, KYC, compliance frameworks
   - **Operational Knowledge**: Quote generation, customer onboarding, vessel management
   - **Business Knowledge**: Competitive analysis, pricing, market positioning

2. **Validation Status Analysis**
   
   Review validation progress:
   - Count pending validation questions in `validation-interactions/pending-questions.yaml`
   - Assess approved knowledge in `validated/` directories
   - Check rejected knowledge and reasons
   - Identify knowledge gaps requiring additional research

3. **OneDrive File Coverage**
   
   Assess source file processing:
   - Files processed vs. total files available
   - Categories covered: MVP scope, premium examples, project documents, UI/UX
   - Identify unprocessed files requiring attention
   - Check for new files added since last extraction

4. **Knowledge Quality Metrics**
   
   Evaluate knowledge base quality:
   - Confidence scores for validated knowledge
   - Source tracking completeness
   - Cross-reference consistency
   - AI agent usability scoring

5. **Integration Readiness**
   
   Check readiness for @ai/ system integration:
   - Validated knowledge formatted for AI consumption
   - Maritime agent specialization completeness
   - Command integration status
   - Cross-reference links to general business knowledge

## Status Report Format:

```
🚢 Maritime Knowledge Base Status Report
═════════════════════════════════════════
📊 Overall Health Score: [score]/100

📁 Knowledge Coverage:
├── Risk Assessment: [%] complete
│   ├── War Risk Models: [status]
│   ├── Voyage Risk Assessment: [status]
│   └── Static Vessel Risk: [status]
├── Regulatory Compliance: [%] complete
│   ├── Sanction Procedures: [status]
│   ├── KYC Requirements: [status]
│   └── Compliance Framework: [status]
├── Operational Processes: [%] complete
│   ├── Quote Generation: [status]
│   ├── Customer Onboarding: [status]
│   └── Vessel Management: [status]
└── Business Intelligence: [%] complete
    ├── Competitive Analysis: [status]
    ├── Pricing Strategies: [status]
    └── Market Positioning: [status]

✅ Validation Status:
├── Pending Questions: [count]
├── Approved Knowledge: [count]
├── Rejected Items: [count]
└── Knowledge Gaps: [count]

📋 OneDrive Processing:
├── Files Processed: [count]/[total]
├── Categories Covered: [count]/[total]
├── Unprocessed Files: [list]
└── New Files Detected: [count]

🎯 Quality Metrics:
├── Average Confidence Score: [score]%
├── Source Tracking: [%] complete
├── Cross-References: [count] validated
└── AI Readiness: [%] complete

⚠️ Issues Found:
├── Knowledge Conflicts: [count]
├── Outdated Information: [count]
├── Missing Critical Areas: [list]
└── Validation Bottlenecks: [count]

📈 Recommendations:
├── Priority validations needed: [list]
├── Additional research required: [list]
├── Integration blockers: [list]
└── Next steps: [list]
```

## Advanced Analysis Options:

**Detailed Category Analysis**: `--category [risk|regulatory|operational|business]`
- Deep dive into specific knowledge area
- Show detailed validation status
- Identify specific gaps and conflicts

**File Processing Analysis**: `--files`
- Show detailed OneDrive file processing status
- Identify specific unprocessed files
- Check for new or updated files

**Integration Readiness**: `--integration`
- Check @ai/ system integration status
- Validate maritime agent readiness
- Test command functionality

**Quality Assessment**: `--quality`
- Detailed quality metrics
- Confidence score distributions
- Source tracking completeness

## Automated Actions:

Based on status check, automatically:
- Flag critical knowledge gaps for immediate attention
- Identify high-priority validation questions
- Update task-list.md with next steps
- Generate recommendations for completion

## Integration Points:

- Reads from all `projects/maritime-insurance-knowledge-system/` directories
- Checks @ai/ system integration status
- Updates knowledge status cache
- Integrates with existing validation and quality frameworks