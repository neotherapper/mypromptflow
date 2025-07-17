Run comprehensive validation on AI Knowledge Base by examining actual project state

## AI Agent Instructions:

You are performing real validation of the AI Knowledge Base system. Examine the actual project files and provide a comprehensive health report.

## Validation Process:

1. **Structure Validation** (25 points)
   - ✅ Check required directories: `ai/knowledge/strategic/`, `ai/knowledge/product/`, `ai/knowledge/technical/`, `ai/context/`
   - ✅ Verify core files exist: `ai/context/dependencies.yaml`, `ai/context/document-registry.yaml`
   - ✅ Check command files: `.claude/commands/ai-help.md`, validate commands exist
   - ❌ Flag any orphaned documents not referenced in registry

2. **Dependency Validation** (25 points)
   - ✅ Read `ai/context/dependencies.yaml` and check all dependencies exist
   - ❌ Identify circular dependency chains (A→B→A)
   - ✅ Verify all referenced documents are actually created
   - ⚠️ Flag missing dependencies that block document creation

3. **Content Validation** (25 points)
   - ✅ Check each document has proper YAML frontmatter starting with `---`
   - ✅ Verify required sections: "# Title", "## Executive Summary", "## AI Agent Instructions"
   - ✅ Ensure documents have minimum 500 words of content
   - ❌ Flag documents missing AI instruction sections

4. **Cross-Reference Validation** (15 points)
   - ✅ Verify all `@ai/knowledge/` references point to existing files
   - ✅ Check bidirectional linking (if A references B, B should mention A)
   - ❌ Flag broken links and missing cross-references
   - ✅ Validate feature workspace links to knowledge base

5. **AI Optimization Check** (10 points)
   - ✅ Check for structured data (YAML frontmatter, tables, lists)
   - ✅ Verify TypeScript examples present in technical documents
   - ✅ Ensure clear AI agent instructions in each document
   - ✅ Validate consistent terminology and formatting

## Output Format:

Provide this exact format with real validation results:

```
🔍 Knowledge Base Validation Report
═══════════════════════════════════
📁 Structure Check: ✅ PASSED (25/25) | ⚠️ ISSUES (X/25) | ❌ FAILED (X/25)
🔗 Dependency Check: ✅ PASSED (25/25) | ⚠️ ISSUES (X/25) | ❌ FAILED (X/25)  
📝 Content Check: ✅ PASSED (25/25) | ⚠️ ISSUES (X/25) | ❌ FAILED (X/25)
🔀 Cross-Reference Check: ✅ PASSED (15/15) | ⚠️ ISSUES (X/15) | ❌ FAILED (X/15)
🤖 AI Optimization: ✅ PASSED (10/10) | ⚠️ ISSUES (X/10) | ❌ FAILED (X/10)

📊 Overall Health Score: [total]/100

🚨 Critical Issues Found: [count]
⚠️ Minor Issues Found: [count]

📋 Detailed Findings:
Structure Issues:
- [List specific missing directories/files]

Dependency Issues:  
- [List circular dependencies, missing files]

Content Issues:
- [List documents missing frontmatter, sections]

Cross-Reference Issues:
- [List broken links, missing bidirectional references]

🎯 Priority Recommendations:
1. [Most critical fix needed]
2. [Second priority fix]
3. [Third priority fix]

✅ Ready for Production: YES/NO
```

## Validation Scoring:
- **90-100**: Excellent health, production ready
- **80-89**: Good health, minor improvements needed
- **70-79**: Fair health, several issues to address
- **60-69**: Poor health, major improvements required  
- **Below 60**: Critical issues, significant work needed
