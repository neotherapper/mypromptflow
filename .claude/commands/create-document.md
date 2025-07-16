Create a single document interactively: $ARGUMENTS

## Interactive Document Creation:

1. **Document Type Selection**

   - Parse $ARGUMENTS for document type
   - Load template from `@ai/prompts/document-templates/`
   - Check dependencies from `@ai/context/dependencies.yaml`

2. **Dependency Check**

   - Verify prerequisites exist in `@ai/knowledge/`
   - Offer to create missing dependencies
   - Load context from existing documents

3. **Interactive Content Generation**

   - Ask clarifying questions
   - Gather specific requirements
   - Reference existing documentation

4. **Document Creation**

   - Generate content with AI assistance
   - Include proper frontmatter
   - Add AI instructions section
   - Create cross-references

5. **Validation & Save**
   - Validate structure and formatting
   - Save to appropriate location in `@ai/knowledge/`
   - Update `@ai/context/document-registry.yaml`
   - Create cross-references
