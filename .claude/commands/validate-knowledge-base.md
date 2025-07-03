Run comprehensive validation tests on knowledge base

## Validation Process:

1. **Structure Validation**

   - Check all required directories exist
   - Verify document paths match configuration
   - Ensure no orphaned documents

2. **Dependency Validation**

   - Build complete dependency graph
   - Check for circular dependencies
   - Verify all references resolve

3. **Content Validation**

   - Verify frontmatter in all documents
   - Check required sections present
   - Validate AI instruction sections

4. **Cross-Reference Validation**

   - Ensure all @file_path references valid
   - Check bidirectional links consistency
   - Verify feature ↔ knowledge base links

5. **AI Optimization Check**
   - Score documents for AI readability
   - Check structured data usage
   - Verify TypeScript examples present

## Output format:

🔍 Knowledge Base Validation Report
═══════════════════════════════════
📁 Structure Check: [status]
🔗 Dependency Check: [status]
📝 Content Check: [status]
🤖 AI Optimization: [score]
📊 Summary:
Health Score: [score]/100
Issues Found: [count]
Recommendations: [list]
