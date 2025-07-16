AI-Enhanced SDLC Workflow Assistant for maritime insurance development team.

Help users navigate role-specific setup, onboarding, and training based on their team persona.

Present team persona selection menu:

```
🤖 AI-Enhanced SDLC Workflow Assistant

Select your team role:
1. Head of Engineering - Infrastructure & team coordination
2. Lead Frontend Developer - React/TypeScript development & UI  
3. Lead Backend Developer - FastAPI development & database architecture
4. UI/UX Engineer - Design system & user experience optimization

Which role describes you? (Enter 1-4)
```

After user selects their role, show role-specific dashboard with:
- Current status and hardware info
- High priority tasks for their role
- Team resources and dependencies
- Next steps and training schedule

Based on the selected role, load the appropriate todo file and display:

1. **Head of Engineering**: Load `@projects/ai-sdlc-workflow-blueprint/todos/head-of-engineering.md`
2. **Lead Frontend Developer**: Load `@projects/ai-sdlc-workflow-blueprint/todos/lead-frontend-developer.md`
3. **Lead Backend Developer**: Load `@projects/ai-sdlc-workflow-blueprint/todos/lead-backend-developer.md`
4. **UI/UX Engineer**: Load `@projects/ai-sdlc-workflow-blueprint/todos/ui-ux-engineer.md`

Show role-specific dashboard with:
- Current status and hardware info
- High priority tasks for the week
- Team resources and tools
- Progress tracking and next steps

Provide options for:
- [A] View detailed task list
- [B] Check team resources  
- [C] View training schedule
- [D] Show dependency map