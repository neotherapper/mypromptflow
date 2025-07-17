Review and approve maritime insurance knowledge through user validation: $ARGUMENTS

## Maritime Knowledge Validation Process:

1. **Load Pending Validation Questions**
   
   - Read from `projects/maritime-insurance-knowledge-system/validation-interactions/pending-questions.yaml`
   - Organize questions by priority and category
   - Load source context and confidence scores
   - Prepare batch validation interface

2. **Present Validation Questions**
   
   For each knowledge area, present structured questions:
   
   **Format Example**:
   ```
   🚢 Maritime Knowledge Validation Session
   ══════════════════════════════════════════
   
   📊 Progress: Question 1 of 25 | Category: Risk Assessment
   
   🔍 Source: /MVP scope/Old premium examples/War/OLYMPIC FIGHTER Quote.xlsx
   📅 File Date: 2024-07-01
   🎯 Confidence: 85%
   
   ❓ Question: Should war risk calculations include vessel tonnage as a primary factor?
   
   📋 Context: Found in premium examples showing tonnage-based calculations
   
   Options:
   [A] Approve as stated
   [B] Approve with modifications
   [C] Reject - outdated/incorrect
   [D] Need more information
   [S] Skip for now
   ```

3. **Process User Responses**
   
   Handle different response types:
   
   - **Approval**: Move knowledge to `validated/` directory with user confirmation
   - **Modification**: Update knowledge based on user corrections
   - **Rejection**: Mark as rejected with reason, don't include in validated knowledge
   - **Information Request**: Flag for additional research or clarification
   - **Skip**: Move to end of queue for later review

4. **Update Knowledge Base**
   
   For approved knowledge:
   - Create structured markdown files in appropriate `validated/` subdirectory
   - Include proper YAML frontmatter with validation metadata
   - Add user approval information and timestamp
   - Create cross-references between related knowledge areas
   - Update audit trail with validation decisions

5. **Generate Validation Report**
   
   Create comprehensive validation summary:
   - Questions processed and approval rate
   - Knowledge areas completed
   - Rejected items with reasons
   - Next steps and remaining validations needed

6. **Update Project Status**
   
   Update project documentation:
   - Mark validation tasks as completed in task-list.md
   - Update progress.md with validation outcomes
   - Create next priority tasks based on validation results
   - Update knowledge status cache

## Interactive Validation Flow:

```
User Input Examples:
- "A" → Approve tonnage factor in risk calculations
- "B: Include tonnage but also add vessel age factor" → Modify and approve
- "C: This is outdated, we now use different model" → Reject with reason
- "D: Need to check current regulation" → Flag for research
- "S" → Skip to next question
```

## Expected Output:

```
🚢 Maritime Knowledge Validation Report
═════════════════════════════════════════
📊 Validation Session Summary:
├── Questions Processed: [count]
├── Knowledge Approved: [count]
├── Items Modified: [count]
├── Items Rejected: [count]
└── Items Skipped: [count]

✅ Approved Knowledge Areas:
├── Risk Assessment: [count] facts validated
├── Regulatory: [count] facts validated
├── Operational: [count] facts validated
└── Business: [count] facts validated

📋 Next Actions:
- [count] questions remaining for validation
- [count] knowledge areas ready for AI agent training
- [count] items need additional research

⏭️ Next Step: Run /maritime-knowledge-status to check completion
```

## Quality Assurance:

- **Consistency Checks**: Validate approved knowledge doesn't contradict existing facts
- **Completeness Review**: Ensure all critical knowledge areas have been addressed
- **Source Tracking**: Maintain complete audit trail of validation decisions
- **Confidence Scoring**: Update confidence levels based on user validation

## Integration Points:

- Updates `projects/maritime-insurance-knowledge-system/knowledge/validated/`
- Creates audit trail in `validation-interactions/validation-audit-log.yaml`
- Integrates with existing validation workflows
- Maintains compatibility with @ai/ system knowledge standards