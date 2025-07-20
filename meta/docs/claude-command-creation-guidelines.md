# Claude Command Creation Guidelines

**Purpose**: Guide for creating AI agent-optimized Claude commands that eliminate human documentation artifacts
**Audience**: Developers creating `.claude/commands/*.md` files
**Framework**: Based on AI Agent Instruction Design Excellence principles
**Updated**: 2025-07-20 - Enhanced validation integration

## Overview

Claude commands should be **pure AI agent instructions**, not human documentation. They are consumed by Claude AI to execute specific workflows, not by humans reading usage examples.

### Core Principle
> **Claude commands are AI agent instructions, not human documentation.** Every line should serve AI agent execution, not human explanation.

## ✅ Required Patterns

### 1. Direct Instruction Start
**Always start with the actionable instruction, never with titles or explanations.**

```markdown
✅ CORRECT:
Please analyze and fix the GitHub issue: $ARGUMENTS.

❌ INCORRECT:
# /fix-github-issue Command

## Command Description
This command allows users to analyze and fix GitHub issues...
```

### 2. $ARGUMENTS Pattern (For Parameterized Commands)
**Commands that take parameters MUST use the $ARGUMENTS pattern meaningfully.**

```markdown
✅ CORRECT:
Conduct comprehensive research using the intelligent hybrid orchestrator for: $ARGUMENTS

✅ CORRECT:
Analyze and work on the GitHub issue: $ARGUMENTS

❌ INCORRECT:
This command takes a GitHub issue number as a parameter.

❌ INCORRECT:
Usage: /command [issue-number]
```

### 3. Specific, Actionable Steps
**Provide concrete steps with exact commands, not abstract procedures.**

```markdown
✅ CORRECT:
1. Use `gh issue view $ARGUMENTS` to get the issue details
2. Understand the problem described in the issue
3. Search the codebase for relevant files

❌ INCORRECT:
1. Analyze the issue appropriately
2. Research the problem effectively
3. Find relevant information
```

### 4. Self-Sufficient Context
**Include all necessary context or use proper @file_path references.**

```markdown
✅ CORRECT:
Follow the research workflow from @research/orchestrator/integration/claude-orchestrator-integration.yaml

❌ INCORRECT:
Use the standard research workflow (see documentation)
```

## ❌ Prohibited Patterns (Human Documentation Artifacts)

### 1. Usage Sections
**Never include ## Usage sections - they are for humans, not AI agents.**

```markdown
❌ FORBIDDEN:
## Usage
```bash
/validate-pr [pr-number]
```

✅ REPLACE WITH:
Direct instruction using $ARGUMENTS pattern
```

### 2. Command Description Sections  
**Never include ## Command Description sections - they explain what commands do instead of providing instructions.**

```markdown
❌ FORBIDDEN:
## Command Description
This command validates PR files using advanced techniques...

✅ REPLACE WITH:
Start directly with the actionable instruction
```

### 3. Implementation Notes Sections
**Never include ## Implementation Notes sections - they are meta-commentary.**

```markdown
❌ FORBIDDEN:
## Implementation Notes
This command implements the AI Agent Instruction Design Excellence Framework...

✅ REPLACE WITH:
Integrate necessary context directly into instruction steps
```

### 4. Meta-Explanatory Content
**Avoid explaining what the command does - provide direct instructions instead.**

```markdown
❌ FORBIDDEN:
This instruction guides AI agents through PR validation...
This command allows users to...
The purpose of this tool is to...

✅ REPLACE WITH:
Validate PR files using the following steps:
Execute the validation workflow for:
```

### 5. Human-Oriented Language
**Avoid language directed at human users.**

```markdown
❌ FORBIDDEN:
You can use this command to...
Users should first...
For users who want to...

✅ REPLACE WITH:
Execute the following steps:
Begin with:
Perform:
```

## Command Structure Template

### For Parameterized Commands
```markdown
[Direct actionable instruction using $ARGUMENTS]: $ARGUMENTS

[Optional context or workflow steps]

[Numbered steps with specific commands]
1. [Specific action with exact command]
2. [Specific action with exact command]
3. [Specific action with exact command]

[Any necessary validation or completion steps]
```

### For Non-Parameterized Commands
```markdown
[Direct actionable instruction]

[Numbered steps with specific commands]
1. [Specific action with exact command]
2. [Specific action with exact command]
3. [Specific action with exact command]

[Any necessary validation or completion steps]
```

## Examples

### ✅ Excellent Example (fix-github-issue.md)
```markdown
Please analyze and fix the GitHub issue: $ARGUMENTS.

Follow these steps:

# PLAN
1. Use `gh issue view` to get the issue details
2. Understand the problem described in the issue
3. Ask clarifying questions if necessary
4. Understand the prior art for this issue
   - Search the scratchpads for previous thoughts related to the issue
   - Search PRs to see if you can find history on this issue
   - Search the codebase for relevant files

# CREATE
- Create a new branch for the issue
- Solve the issue in small, manageable steps, according to your plan
- Commit your changes after each step by creating a descriptive commit message

# TEST
- Ensure that all tests are passing

# DEPLOY
- Push and create a PR

Remember to use the GitHub CLI (`gh`) for all GitHub-related tasks.
```

**Why this is excellent:**
- ✅ Starts with direct instruction using $ARGUMENTS
- ✅ No Usage, Description, or Implementation Notes sections
- ✅ Specific commands like `gh issue view`
- ✅ Clear workflow with exact steps
- ✅ Self-sufficient context

### ❌ Poor Example (Before Fixes)
```markdown
# /validate-pr Command

## Usage
```bash
/validate-pr [pr-number]
```

## Command Description
This instruction guides AI agents through revolutionary PR validation using GitHub CLI with systematic fallbacks...

## Implementation Notes
This command implements revolutionary PR validation using the AI Agent Instruction Design Excellence Framework...
```

**Why this is poor:**
- ❌ Starts with title instead of instruction
- ❌ Has Usage section (human documentation artifact)
- ❌ Has Command Description section (meta-explanatory)
- ❌ Has Implementation Notes section (meta-commentary)
- ❌ Missing $ARGUMENTS pattern for parameterized command
- ❌ Explains what command does instead of providing instructions

## Validation Checklist

Before creating or updating a Claude command, verify:

### ✅ Required Elements
- [ ] **Direct instruction start** - First line contains actionable instruction
- [ ] **$ARGUMENTS usage** - Parameterized commands use $ARGUMENTS pattern meaningfully
- [ ] **Specific steps** - Contains numbered or structured steps with exact commands
- [ ] **Self-sufficient context** - All necessary context included or properly referenced

### ❌ Prohibited Elements
- [ ] **No Usage sections** - Zero `## Usage` sections detected
- [ ] **No Description sections** - Zero `## Command Description` sections detected  
- [ ] **No Implementation Notes** - Zero `## Implementation Notes` sections detected
- [ ] **No meta-explanatory content** - No "this command does" or "allows users to" language
- [ ] **No human-oriented language** - No "you can", "users should" language

### 🎯 Quality Indicators
- [ ] **Immediate actionability** - AI agent can execute without interpretation
- [ ] **Concrete specificity** - Exact commands, specific procedures, measurable criteria
- [ ] **Vagueness elimination** - No "effectively", "appropriately", "good quality" terms
- [ ] **Error prevention** - Clear validation steps and structured approach

## Testing Your Command

### Automated Validation
Run the enhanced validators to check your command:

```bash
# Apply claude-command-evaluator (enhanced with AI agent focus)
validate_command ".claude/commands/your-command.md"

# Check for human documentation artifacts
detect_vagueness ".claude/commands/your-command.md"

# Apply AI Agent Instruction Design Excellence framework
validate_ai_instruction ".claude/commands/your-command.md"
```

### Manual Validation Questions
Ask yourself:

1. **Can an AI agent execute this without asking clarification?**
2. **Does it start with a direct instruction, not an explanation?**
3. **Are all steps specific with exact commands?**
4. **Does it use $ARGUMENTS if the command takes parameters?**
5. **Is there any content that explains what the command does instead of providing instructions?**

## Score Targets

Aim for these scores with the enhanced validation system:

- **AI Instruction Structure**: 20+/25 (80%+)
- **Immediate Actionability**: 20+/25 (80%+)  
- **Design Excellence Compliance**: 20+/25 (80%+)
- **Anti-Pattern Detection**: 8+/10 (80%+)
- **Overall Score**: 75+/100 (75%+)

## Common Mistakes and Fixes

### Mistake 1: Starting with Title
```markdown
❌ BEFORE:
# /research Command

Research the specified topic using...

✅ AFTER:
Conduct comprehensive research using the intelligent hybrid orchestrator for: $ARGUMENTS
```

### Mistake 2: Including Usage Examples
```markdown
❌ BEFORE:
## Usage
```bash
/validate-pr 123
```

✅ AFTER:
[Remove section entirely, integrate parameters into instruction]
```

### Mistake 3: Meta-Explanatory Content
```markdown
❌ BEFORE:
This command allows users to validate PR files using advanced AI techniques...

✅ AFTER:
Validate PR files using the following steps:
```

### Mistake 4: Missing $ARGUMENTS
```markdown
❌ BEFORE:
Validate the PR specified in the command arguments.

✅ AFTER:
Validate PR files for: $ARGUMENTS
```

### Mistake 5: Vague Instructions
```markdown
❌ BEFORE:
1. Analyze the PR appropriately
2. Check quality effectively
3. Provide good recommendations

✅ AFTER:
1. Use `gh pr view $ARGUMENTS --json title,body,labels` to extract PR metadata
2. Apply pattern matching classification to detect file types
3. Generate specific improvement recommendations with line numbers
```

## Integration with Development Workflow

### Creating New Commands
1. **Plan the workflow** - Define what the AI agent should do step-by-step
2. **Write direct instruction** - Start with actionable instruction using $ARGUMENTS if needed
3. **Add specific steps** - Include exact commands and procedures
4. **Validate with tools** - Run enhanced validators to check compliance
5. **Test with AI agent** - Verify the command works as intended

### Updating Existing Commands
1. **Run validation tools** - Check current command for issues
2. **Remove human artifacts** - Eliminate Usage, Description, Implementation Notes sections
3. **Add $ARGUMENTS if needed** - Ensure parameterized commands use $ARGUMENTS pattern
4. **Enhance specificity** - Replace vague terms with exact specifications
5. **Re-validate** - Confirm improvements with enhanced validators

## Framework Integration

This guide integrates with:

- **Enhanced claude-command-evaluator** - Validates AI agent instruction patterns
- **Enhanced vagueness-detector** - Detects human documentation artifacts  
- **AI Agent Instruction Design Excellence Framework** - Provides comprehensive validation
- **Claude command pattern validator** - Systematic pattern detection and validation

## Success Criteria

A well-created Claude command should:

✅ **Pass all enhanced validators** with scores ≥75/100
✅ **Eliminate human documentation artifacts** (0 detected)
✅ **Use $ARGUMENTS pattern** for parameterized commands (100% compliance)
✅ **Start with direct instruction** (immediate actionability)
✅ **Contain specific, executable steps** (concrete specificity)
✅ **Require no interpretation** (self-sufficient)

Following these guidelines ensures Claude commands serve as effective AI agent instructions rather than human documentation, leading to better execution and fewer interpretation errors.