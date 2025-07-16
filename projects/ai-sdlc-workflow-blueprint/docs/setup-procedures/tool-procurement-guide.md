# AI Tool Procurement and Setup Guide

## Executive Summary

This guide provides step-by-step instructions for procuring and setting up the AI tool stack for your 4-person development team.

**Total Monthly Investment**: $530
**Setup Time**: 2-3 days
**Prerequisites**: Admin access to company payment methods and tool accounts

---

## Tool Procurement Checklist

### Required Purchases
- [ ] Claude Code Max - $200 subscription (Backend Developer)
- [ ] Figma Professional - 2 seats at $15 each
- [ ] Total new monthly cost: $230

### Already Subscribed
- [x] Claude Code Max - $200 (Lead Frontend Developer)
- [x] Claude Code Max - $100 (Head of Engineering)

### Free Tools to Install
- [ ] Cursor IDE (all team members)
- [ ] Gemini CLI (all team members)

---

## Detailed Procurement Steps

### Step 1: Claude Code Max Subscription (Backend Developer)

**Who**: Head of Engineering or IT Admin
**Time**: 15 minutes
**Cost**: $200/month

#### Purchase Process:
1. Go to https://claude.ai/subscribe
2. Select "Max" plan ($200/month option)
3. Choose monthly billing
4. Enter payment details
5. Assign to Lead Backend Developer

#### Account Setup:
```
Email: backend.developer@company.com
Plan: Max ($100/month)
Billing: Monthly (cancel anytime)
Usage: ~225 messages per 5-hour session
```

#### Verification:
- Log in as backend developer
- Run test prompt: "Hello, confirm my plan status"
- Should see "Claude Max" indicator

### Step 2: Figma Professional Seats

**Who**: Head of Engineering or Design Lead
**Time**: 20 minutes
**Cost**: $30/month (2 seats × $15)

#### Purchase Process:
1. Go to https://www.figma.com/pricing/
2. Select "Professional" plan
3. Choose 2 seats:
   - UI/UX Engineer
   - Lead Frontend Developer
4. Monthly billing recommended
5. Enter company payment details

#### Seat Assignment:
```
Seat 1: uiux.engineer@company.com (Full access)
Seat 2: frontend.developer@company.com (Full access)
Viewer access: backend.developer@company.com (Free)
Viewer access: engineering.head@company.com (Free)
```

#### Initial Setup:
1. Create team workspace
2. Set up project structure:
   ```
   Company Workspace/
   ├── Design System/
   ├── Current Projects/
   │   └── Customer Portal/
   └── Archives/
   ```

### Step 3: Free Tool Installation

#### Cursor IDE Installation (All Team Members)

**Time**: 10 minutes per person
**Cost**: Free

1. Visit https://cursor.sh/
2. Download for your OS:
   - macOS: cursor-0.34.0.dmg
   - Windows: cursor-0.34.0.exe
   - Linux: cursor-0.34.0.AppImage

3. Install and launch
4. Sign in with GitHub account (recommended)
5. Configure settings:
   ```json
   {
     "cursor.aiProvider": "openai-compatible",
     "cursor.general.betaAccess": false,
     "editor.fontSize": 14,
     "terminal.integrated.fontSize": 14
   }
   ```

#### Gemini CLI Installation (All Team Members)

**Time**: 15 minutes per person
**Cost**: Free
**Prerequisite**: Google Cloud account

1. Install Google Cloud SDK:
   ```bash
   # macOS
   brew install google-cloud-sdk

   # Windows (PowerShell)
   (New-Object Net.WebClient).DownloadFile("https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe", "$env:Temp\GoogleCloudSDKInstaller.exe")
   & $env:Temp\GoogleCloudSDKInstaller.exe

   # Linux
   curl https://sdk.cloud.google.com | bash
   ```

2. Authenticate:
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```

3. Install Gemini CLI:
   ```bash
   pip install google-generativeai
   # or
   npm install -g @google/generative-ai
   ```

4. Test installation:
   ```bash
   gemini "Hello, test my installation"
   ```

---

## Tool Configuration

### Claude Code Max MCP Setup

**For JIRA Integration**:

1. Install MCP JIRA Server:
   ```bash
   npm install -g @modelcontextprotocol/server-jira
   ```

2. Configure authentication:
   ```bash
   export JIRA_URL="https://yourcompany.atlassian.net"
   export JIRA_EMAIL="user@company.com"
   export JIRA_API_TOKEN="your-api-token"
   ```

3. Start MCP server:
   ```bash
   mcp-server-jira start
   ```

4. Test in Claude:
   ```
   @jira list my assigned issues
   ```

### Figma Plugin Installation

**Recommended plugins for AI workflow**:

1. **Figma to Code**
   - Converts designs to React components
   - Install from Figma Community

2. **Design Tokens**
   - Exports design system variables
   - Syncs with code

3. **Accessibility Checker**
   - Ensures WCAG compliance
   - Real-time feedback

---

## Team Assignment Matrix

| Team Member | Claude Code Max | Figma | Cursor IDE | Gemini CLI |
|------------|----------------|-------|------------|------------|
| Head of Engineering | $100 (existing) | Viewer (free) | ✓ | ✓ |
| Lead Frontend Dev | $200 (existing) | $15 Full | ✓ | ✓ |
| Lead Backend Dev | $200 (new) | Viewer (free) | ✓ | ✓ |
| UI/UX Engineer | - | $15 Full | ✓ | ✓ |

---

## First Week Rollout Plan

### Day 1: Procurement
- [ ] Morning: Purchase Claude Max for Backend
- [ ] Afternoon: Purchase Figma seats
- [ ] Send welcome emails with credentials

### Day 2: Installation
- [ ] Morning standup: Installation party
- [ ] Each member installs their tools
- [ ] Verify all installations work
- [ ] Configure integrations

### Day 3: Training Kickoff
- [ ] Claude basics workshop (2 hours)
- [ ] Figma collaboration setup (1 hour)
- [ ] Team workflow walkthrough (1 hour)

### Days 4-5: Practice Sprint
- [ ] Run a simple feature through all stages
- [ ] Practice tool handoffs
- [ ] Document learnings
- [ ] Refine workflows

---

## Budget Tracking

### Monthly Costs
```
New Subscriptions:
- Claude Max (Backend): $200
- Figma (2 seats): $30
Subtotal New: $130/month

Existing Subscriptions:
- Claude Max (Frontend): $200
- Claude Max (Head of Eng): $100
Subtotal Existing: $500/month

Total Monthly: $530
Total Annual: $6,360
```

### Cost Optimization Tips
1. **Annual Billing**: Consider annual plans after 3-month trial
2. **Usage Monitoring**: Track Claude message usage weekly
3. **Seat Sharing**: Figma viewers are free - use for read-only access
4. **Tool Consolidation**: This stack replaces need for many other tools

---

## Troubleshooting Common Issues

### Claude Code Max Issues
**Problem**: "Rate limit exceeded"
**Solution**: Check usage dashboard, wait for 5-hour window reset

**Problem**: MCP JIRA connection fails
**Solution**: Verify API token hasn't expired, regenerate if needed

### Figma Issues
**Problem**: Can't access team files
**Solution**: Ensure proper seat assignment, check team settings

**Problem**: Sync conflicts
**Solution**: Use version history, establish clear file ownership

### Cursor IDE Issues
**Problem**: AI suggestions not appearing
**Solution**: Check internet connection, verify free tier limits

---

## Success Validation

After setup, verify:

- [ ] All team members can log into their tools
- [ ] Claude-JIRA integration creates test ticket
- [ ] Figma collaboration works between UI/UX and Frontend
- [ ] Gemini CLI processes a test file
- [ ] Cursor IDE provides code completions

---

## Support Contacts

- **Claude Support**: support@anthropic.com
- **Figma Support**: support@figma.com
- **Internal IT**: [your IT contact]
- **Head of Engineering**: [contact for tool questions]

---

## Next Steps

Once all tools are procured and installed:
1. Schedule team training sessions
2. Create shared prompt library
3. Establish tool usage guidelines
4. Set up monitoring dashboards
5. Plan first AI-enhanced sprint