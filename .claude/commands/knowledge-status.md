Check the knowledge base status and route to appropriate workflow.

Read `ai/context/knowledge-status-cache.yaml` to determine the current state:

- If `cache_summary.total_documents == 0`: Route to Bootstrap Workflow
- Otherwise: Present Status Menu with 9 options

## Bootstrap Workflow (Empty Knowledge Base)
```
🚀 Welcome to AI Knowledge Base Bootstrap!
Your knowledge base is empty. Starting personalized setup...
```

**Bootstrap Workflow Navigation:**
- Follow workflow in `@ai/workflows/bootstrap/CLAUDE.md`
- Use questionnaire from `@ai/workflows/bootstrap/questionnaire.yaml`
- Apply response logic from `@ai/workflows/bootstrap/response-logic.yaml`
- Guide user through personalized document creation roadmap

## Status Workflow (Existing Documents)
```
📊 AI Knowledge Base Status

Choose an option:
1. Overall Status - Completion percentage and tier status
2. Completed Documents - List existing documents with status
3. Missing Documents - Defined but not yet created
4. Ready to Create - Documents whose dependencies are satisfied
5. Blocked Documents - Documents waiting for dependencies
6. Next Priority - What should be created next
7. Dependency Chains - How documents relate to each other
8. Tier Analysis - Status by tier (strategic, product, technical)
9. Suggested Actions - What you should do next

Enter choice (1-9): 
```

**Status Workflow Navigation:**
- Follow workflow in `@ai/workflows/status/CLAUDE.md`
- Use templates from `@ai/workflows/status/templates/`
- Generate report based on user's selection