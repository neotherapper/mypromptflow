# Development Protocols

Apply comprehensive development workflows ensuring consistent Git practices, JIRA integration, and Claude optimization patterns across all development work.

## Git Workflow Protocol (MANDATORY)

### Branch Management
- **NEVER** commit directly to `master` branch (automated prevention: merge conflicts will result)
- **ALWAYS** create feature branch: `git checkout -b feature/[descriptive-name]`
- **Naming Convention**: `feature/task-description-YYYY-MM-DD`
- **Pre-commit Validation**: All commits must pass quality score ≥85%, no external dependencies

### Commit Creation Process
When creating new git commits, follow these steps:

1. **Parallel Information Gathering** (run simultaneously):
   - `git status` - See all untracked files
   - `git diff` - See staged and unstaged changes  
   - `git log --oneline -5` - See recent commit messages for style

2. **Analyze and Draft Commit Message**:
   - Summarize nature of changes (new feature, enhancement, bug fix, refactoring, test, docs)
   - Check for sensitive information that shouldn't be committed
   - Draft concise (1-2 sentences) commit message focusing on "why" rather than "what"
   - Ensure message accurately reflects changes and their purpose

3. **Execute Commit** (run in parallel):
   - Add relevant untracked files to staging area
   - Create commit with message ending with:
     ```
     🤖 Generated with [Claude Code](https://claude.ai/code)
     
     Co-Authored-By: Claude <noreply@anthropic.com>
     ```
   - Run `git status` to verify commit succeeded

4. **Handle Pre-commit Hook Changes**:
   - If commit fails due to pre-commit hook changes, retry ONCE to include automated changes
   - If files were modified by pre-commit hook, amend commit to include them

### Pull Request Creation
When creating pull requests using `gh pr create`:

1. **Parallel State Analysis** (run simultaneously):
   - `git status` - Check untracked files
   - `git diff` - Review staged/unstaged changes
   - Check current branch tracks remote and is up to date
   - `git log [base-branch]...HEAD` - Understand full commit history

2. **Analyze All PR Changes**:
   - Review ALL commits included (not just latest)
   - Ensure comprehensive understanding of changes for PR summary

3. **Create PR** (execute in parallel):
   - Create new branch if needed
   - Push to remote with `-u` flag if needed  
   - Create PR using `gh pr create` with HEREDOC format:
     ```bash
     gh pr create --title "PR title" --body "$(cat <<'EOF'
     ## Summary
     <1-3 bullet points>
     
     ## Test plan
     [Checklist of TODOs for testing]
     
     🤖 Generated with [Claude Code](https://claude.ai/code)
     EOF
     )"
     ```

## JIRA Integration Protocol (MANDATORY)

### Required Tools
Use MCP JIRA server tools for ALL JIRA operations:
- `mcp__MCP_DOCKER__jira_search` - Search with JQL queries
- `mcp__MCP_DOCKER__jira_get_issue` - Get comprehensive issue details
- `mcp__MCP_DOCKER__jira_add_comment` - Add structured comments
- `mcp__MCP_DOCKER__jira_update_issue` - Update status and fields
- `mcp__MCP_DOCKER__jira_transition_issue` - Change issue status

### Comment Format Standards
Use markdown formatting for structured, professional comments:
- **Problem Analysis**: Clear description of issue investigation
- **Solution Approach**: Detailed explanation of resolution strategy  
- **Implementation Details**: Specific changes made or planned
- **Supporting Documentation**: Reference documentation paths
- **Next Steps**: Clear action items with ownership

### Issue Management Workflow
1. **Search Issues**: Use JQL queries like `key = SCRUM-33`
2. **Analyze Issue**: Get comprehensive details with field specifications
3. **Add Progress Comments**: Document investigation and resolution progress
4. **Update Status**: Use appropriate transitions based on issue workflow
5. **Reference Documentation**: Always include supporting file paths in comments

## Efficiency Protocol

### Parallel Tool Execution
Achieve 60-70% time reduction through simultaneous operations:

**Git Operations Example**:
```bash
# Execute simultaneously in single response
git status & git diff & git log --oneline -5
```

**Research Operations Example**:
```bash
# Run concurrently
WebFetch + Read @research/templates/ + Glob **/*research*.md
```

**Validation Operations Example**:  
```bash
# Execute in parallel
Read file1.md + Read file2.md + Grep "pattern" **/*.md
```

### Performance Targets
- **Time Reduction**: 60-70% through parallel processing
- **Accuracy Maintenance**: ≥95% accuracy scores
- **Consistency Scores**: ≥90% consistency across operations
- **Quality Preservation**: No reduction in deliverable quality

## Claude Integration Optimization

### Automatic Context Loading
Execute recursive file discovery protocol:
- **Scan Depth**: 5 levels maximum
- **File Types**: .md/.yaml/.json priority
- **Timeout**: 30s discovery limit
- **Context Prioritization**: Load most relevant content first

### Cross-Reference Utilization  
Implement @file_path patterns:
- **Validation**: 100% accuracy required
- **Resolution Time**: ≤2s per reference
- **Pattern Format**: `@directory/subdirectory/filename.extension`
- **Accessibility**: Verify all references are reachable

### Command System Integration
Access @.claude/commands/ using standardized execution protocol:
- **Available Commands**: ai-help.md, improve-claude.md, validate-pr.md, research.md, create-document.md, create-feature.md
- **Execution Pattern**: Read command definition → Execute step-by-step → Apply $ARGUMENTS pattern
- **Command Validation**: ≤5s validation time, ≤2% error rate
- **Guidelines Reference**: @meta/docs/claude-command-creation-guidelines.md

### Memory Persistence Structure
Utilize three-tier memory hierarchy:
- **Project Context**: Persistent across sessions (CLAUDE.md files)
- **User Context**: Session-based preferences and patterns
- **Dynamic Context**: Task-specific loading with progressive expansion

## Quality Assurance Integration

### Development Quality Gates
Before completing any development task:
- **Code Quality**: ESLint, Prettier, TypeScript validation pass
- **Test Coverage**: Automated tests execute successfully
- **Documentation**: All changes documented with examples
- **Cross-References**: All @file_path patterns validated

### Performance Monitoring
Track development workflow efficiency:
- **Parallel Execution Rate**: Percentage of operations run simultaneously
- **Context Loading Time**: Time to load project context
- **Cross-Reference Resolution**: Time to validate @file_path patterns
- **Command Execution Speed**: Time from command to completion

### Error Recovery Protocols
When development workflow failures occur:
1. **Identify Failure Point**: Git operation, JIRA integration, or Claude context issue
2. **Apply Recovery Strategy**: Retry with alternative approach or escalate to manual intervention
3. **Document Failure**: Record issue and prevention measures
4. **Update Protocols**: Enhance procedures to prevent similar failures

## Integration Points

### Research Framework Integration
- Development tasks can trigger research orchestrator when complex analysis needed
- Research findings inform development decisions and architectural choices
- Research quality validation applies to development documentation

### Task Management Integration
- All development work follows task completion protocol
- Development tasks update project task lists and progress tracking
- Cross-project coordination for development dependencies

### AI Knowledge Base Integration
- Development patterns contribute to knowledge base enhancement
- Successful workflows become reusable templates
- Development metrics inform AI agent instruction improvements

**ENFORCEMENT**: All development work must follow these protocols. Violations result in automatic quality review and protocol re-execution requirements.