Extract and process maritime insurance knowledge from OneDrive files: $ARGUMENTS

## Maritime Knowledge Extraction Process:

1. **OneDrive File Analysis**
   
   - Scan OneDrive directory: `/Users/georgiospilitsoglou/Library/CloudStorage/OneDrive-SharedLibraries-VanguardTech/Vanguard Tech - Risk Platform`
   - Categorize files by type: risk assessment, regulatory, operational, business
   - Check file timestamps and identify potentially outdated information
   - Create processing plan with file priorities

2. **Maritime Agent Deployment**
   
   Deploy specialized agents for parallel processing:
   
   - **Maritime Risk Analyst**: Process risk calculation models, war risk factors, voyage risk assessments
   - **Regulatory Compliance Specialist**: Extract sanction procedures, KYC requirements, compliance frameworks
   - **Quote Generation Expert**: Document pricing workflows, premium calculations, quote processes
   - **Vessel Data Specialist**: Structure vessel specifications, data models, management processes
   - **Customer Onboarding Expert**: Map B2C registration flows, onboarding procedures, user workflows

3. **Knowledge Extraction Phase**
   
   For each file category:
   - Extract structured facts and procedures
   - Assign confidence scores to extracted information
   - Track source file and timestamp for each piece of knowledge
   - Identify relationships and dependencies between knowledge areas
   - Flag potential conflicts or outdated information

4. **Validation Question Generation**
   
   Create structured questions for user approval:
   - Generate specific, contextual questions for each extracted fact
   - Include source context and confidence scores
   - Create batch validation workflows for efficient user interaction
   - Prioritize questions by business criticality

5. **Knowledge Organization**
   
   Structure extracted knowledge in:
   - `projects/maritime-insurance-knowledge-system/knowledge/extraction/`
   - Organize by category: risk-assessment/, regulatory/, operational/, business/
   - Create pending validation files with proper YAML frontmatter
   - Generate validation questions in `validation-interactions/pending-questions.yaml`

6. **Progress Reporting**
   
   Update project status:
   - Document files processed and knowledge extracted
   - Report validation questions generated
   - Update task-list.md with completion status
   - Create extraction summary report

## Expected Output:

```
🚢 Maritime Knowledge Extraction Report
═════════════════════════════════════════
📁 OneDrive Files Processed: [count]
🔍 Knowledge Facts Extracted: [count]
❓ Validation Questions Generated: [count]
📊 Categories Processed:
├── Risk Assessment: [count] facts
├── Regulatory: [count] facts  
├── Operational: [count] facts
└── Business: [count] facts

⏭️ Next Step: Run /maritime-validation-review to approve knowledge
```

## Error Handling:

- **File Access Issues**: Report inaccessible files and continue with available ones
- **Conflicting Information**: Flag conflicts for user resolution during validation
- **Outdated Files**: Mark with timestamps and create validation questions about currency
- **Processing Errors**: Log errors and continue with next files, report at end

## Integration Points:

- Updates `projects/maritime-insurance-knowledge-system/knowledge/extraction/`
- Creates validation questions in `validation-interactions/`
- Integrates with existing @ai/ system agents and workflows
- Maintains compatibility with project structure and documentation standards