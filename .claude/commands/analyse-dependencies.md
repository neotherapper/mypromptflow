Analyze the dependency graph for document: $ARGUMENTS

1. Read @ai/context/dependencies.yaml
2. Check which dependencies exist in @ai/knowledge/
3. Create a visual representation:
   - ✅ Existing documents
   - ❌ Missing documents
   - 🔄 Documents with outdated dependencies
4. Suggest creation order based on dependency graph
5. Estimate effort for completing missing documents

Output format:

Dependency Analysis for: {document}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Required Dependencies:
├── ✅ statement-of-purpose.md (exists)
├── ❌ market-analysis.md (missing)
└── ❌ user-research.md (missing)

Suggested Creation Order:

1. market-analysis.md (parallel with user-research)
2. user-research.md (parallel with market-analysis)
3. {target-document} (after all dependencies)

Interactive Options:
[1] Create all missing documents
[2] Create specific document
[3] View existing document
[4] Update dependency configuration
