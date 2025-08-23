---
name: "Slack Team Communication MCP Server"
category: "Communication & Collaboration"
type: "Team Messaging and Collaboration Platform"
tier: "Tier 1"
quality_score: 9.2
maintainer: "Slack Technologies (Official)"
github_url: "https://github.com/slack/slack-mcp-server"
npm_package: "@slack/mcp-server"
description: "Enterprise team communication MCP server providing comprehensive Slack workspace integration with messaging, file sharing, workflow automation, and app integration capabilities for modern distributed teams"
last_updated: "2025-01-22"
status: "Production"
license: "MIT"
supported_platforms:
  - "Slack workspaces (all tiers)"
  - "Slack Enterprise Grid"
  - "Web, desktop, and mobile"
  - "All major operating systems"
programming_languages:
  - "JavaScript/TypeScript"
  - "Python"
  - "Go"
  - "Any language via Web API"
dependencies:
  - "Slack workspace"
  - "Slack app credentials"
  - "OAuth 2.0 setup"
  - "MCP-compatible client"
features:
  core:
    - "Message sending and receiving"
    - "Channel and DM management"
    - "File upload and sharing"
    - "User presence and status"
    - "Thread conversations"
  advanced:
    - "Workflow Builder automation"
    - "Slash commands"
    - "Interactive components (buttons, modals)"
    - "Event subscriptions"
    - "Scheduled messages"
integration_complexity: "Low"
setup_requirements:
  - "Slack workspace admin access"
  - "App creation in Slack API portal"
  - "OAuth scopes configuration"
  - "Event subscriptions setup (optional)"
authentication: "OAuth 2.0, Bot tokens, User tokens"
rate_limits: "Tier-based (1+ per second for most methods)"
pricing_model: "Free tier available, paid plans for advanced features"
communication_capabilities:
  messaging:
    - "Send/receive messages"
    - "Rich text formatting"
    - "Emoji reactions"
    - "Thread replies"
    - "Message editing/deletion"
  channels:
    - "Public/private channels"
    - "Channel creation/archival"
    - "Member management"
    - "Channel topics and descriptions"
    - "Shared channels (cross-workspace)"
  collaboration:
    - "File sharing (up to 1GB)"
    - "Screen sharing"
    - "Huddles (audio/video)"
    - "Canvas documents"
    - "Workflow automation"
use_cases:
  primary:
    - "Team notifications and alerts"
    - "CI/CD pipeline notifications"
    - "Incident management"
    - "Customer support integration"
  secondary:
    - "Project coordination"
    - "Standup automation"
    - "Approval workflows"
    - "Knowledge sharing"
tools_available:
  - name: "send_message"
    description: "Post messages to channels or DMs"
  - name: "read_messages"
    description: "Retrieve message history"
  - name: "manage_channels"
    description: "Create, archive, manage channels"
  - name: "upload_files"
    description: "Share files in conversations"
  - name: "create_workflow"
    description: "Build automated workflows"
performance_metrics:
  message_delivery: "< 100ms average"
  api_response_time: "< 200ms p95"
  uptime: "99.99% SLA"
documentation_quality: "Excellent"
community_adoption: "Very High"
enterprise_readiness: "Very High"
technology_stack_alignment: 9
business_domain_relevance: 9
mcp_ecosystem_integration: 9
production_readiness: 98
maintenance_status: 10
composite_score: 9.2
bot_development:
  - "Bolt framework (JS/Python/Java)"
  - "Socket Mode for firewall-friendly connections"
  - "Events API for real-time updates"
  - "Web API for all operations"
  - "Block Kit for rich UI"
workflow_automation:
  - "Workflow Builder steps"
  - "Trigger on events"
  - "Conditional logic"
  - "External function calls"
  - "Scheduled workflows"
ci_cd_integration:
  - "GitHub Actions integration"
  - "Jenkins notifications"
  - "CircleCI orb"
  - "GitLab webhooks"
  - "Azure DevOps"
monitoring_integration:
  - "PagerDuty alerts"
  - "Datadog notifications"
  - "New Relic incidents"
  - "Sentry error tracking"
  - "Custom webhook support"
enterprise_features:
  - "Enterprise Grid (multiple workspaces)"
  - "SSO and SAML"
  - "Data loss prevention (DLP)"
  - "eDiscovery and compliance"
  - "Custom retention policies"
security_features:
  - "Enterprise key management (EKM)"
  - "Two-factor authentication"
  - "Session management"
  - "IP allowlisting"
  - "Audit logs API"
limitations:
  - "Rate limits on API calls"
  - "Message history limits on free tier"
  - "File storage limits"
  - "Guest access restrictions"
comparison_notes: "Industry-leading team communication platform with extensive integration ecosystem and proven enterprise scalability"
integration_examples:
  - "GitHub PR notifications"
  - "Deployment status updates"
  - "Error alert routing"
  - "Customer feedback collection"
notable_features:
  - "Official Slack development"
  - "Massive app ecosystem (2500+ apps)"
  - "Industry standard for team communication"
  - "Excellent developer experience"
  - "Rich UI components (Block Kit)"
assessment_notes: "Tier 1 rating due to critical team communication role, extensive integration capabilities, proven enterprise adoption, excellent developer tools, and essential for modern DevOps workflows"
related_servers:
  - "GitHub MCP Server"
  - "Jira Project Management MCP Server"
  - "PagerDuty Incident MCP Server"
---

# Slack Team Communication MCP Server

## Overview

The Slack MCP Server enables comprehensive team communication and collaboration through the Model Context Protocol. As the industry standard for team messaging, it provides rich integration capabilities for notifications, workflow automation, and team coordination.

## 💬 Core Capabilities

### Messaging Features
- **Real-time Messaging**: Instant message delivery
- **Rich Formatting**: Markdown, code blocks, attachments
- **Threading**: Organized conversation threads
- **Reactions**: Emoji reactions for quick feedback
- **Search**: Powerful message and file search

### Collaboration Tools
- **Channels**: Organized team conversations
- **Direct Messages**: Private 1:1 or group chats
- **File Sharing**: Documents, images, code snippets
- **Huddles**: Quick audio/video calls
- **Canvas**: Collaborative documents

## 🚀 Quick Start (15 minutes)

### 1. Create Slack App
```bash
# Visit https://api.slack.com/apps
# Click "Create New App"
# Choose "From scratch"
# Name your app and select workspace
```

### 2. Configure OAuth Scopes
```yaml
# Required Bot Token Scopes:
- chat:write         # Send messages
- channels:read      # View channels
- channels:manage    # Create/manage channels
- files:write       # Upload files
- users:read        # Access user info
```

### 3. Install MCP Server
```bash
npm install -g @slack/mcp-server
```

### 4. Configure Connection
```json
{
  "mcpServers": {
    "slack": {
      "command": "slack-mcp",
      "args": [],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-your-bot-token",
        "SLACK_APP_TOKEN": "xapp-your-app-token"
      }
    }
  }
}
```

## 💡 Use Cases

### CI/CD Notifications
```javascript
// Send deployment notification
const slack = require('@slack/web-api');
const client = new slack.WebClient(token);

await client.chat.postMessage({
  channel: '#deployments',
  blocks: [{
    type: 'section',
    text: {
      type: 'mrkdwn',
      text: `✅ *Deployment Successful*\n*App:* my-app\n*Version:* v2.1.0\n*Environment:* production`
    }
  }, {
    type: 'actions',
    elements: [{
      type: 'button',
      text: { type: 'plain_text', text: 'View Deployment' },
      url: 'https://app.example.com'
    }]
  }]
});
```

### Incident Management
```python
# Python incident bot
from slack_sdk import WebClient

slack = WebClient(token=bot_token)

# Create incident channel
response = slack.conversations_create(
    name=f"incident-{incident_id}",
    is_private=False
)

# Post incident details
slack.chat_postMessage(
    channel=response['channel']['id'],
    text=f"🚨 Incident #{incident_id}: {title}",
    blocks=[
        {
            "type": "header",
            "text": {"type": "plain_text", "text": f"Incident #{incident_id}"}
        },
        {
            "type": "section",
            "fields": [
                {"type": "mrkdwn", "text": f"*Severity:* {severity}"},
                {"type": "mrkdwn", "text": f"*Status:* {status}"},
                {"type": "mrkdwn", "text": f"*Assigned:* {assignee}"},
                {"type": "mrkdwn", "text": f"*Started:* {timestamp}"}
            ]
        }
    ]
)
```

### Workflow Automation
```javascript
// Approval workflow
app.action('approve_request', async ({ ack, body, client }) => {
  await ack();
  
  // Update message with approval
  await client.chat.update({
    channel: body.channel.id,
    ts: body.message.ts,
    text: 'Request approved!',
    blocks: [{
      type: 'section',
      text: {
        type: 'mrkdwn',
        text: `✅ *Approved by <@${body.user.id}>*`
      }
    }]
  });
  
  // Trigger downstream action
  await triggerDeployment(body.actions[0].value);
});
```

## 🔧 Advanced Features

### Interactive Components
```javascript
// Modal with form
await client.views.open({
  trigger_id: body.trigger_id,
  view: {
    type: 'modal',
    title: { type: 'plain_text', text: 'Create Issue' },
    blocks: [{
      type: 'input',
      element: {
        type: 'plain_text_input',
        action_id: 'title'
      },
      label: { type: 'plain_text', text: 'Title' }
    }, {
      type: 'input',
      element: {
        type: 'static_select',
        action_id: 'priority',
        options: [
          { text: { type: 'plain_text', text: 'High' }, value: 'high' },
          { text: { type: 'plain_text', text: 'Medium' }, value: 'medium' },
          { text: { type: 'plain_text', text: 'Low' }, value: 'low' }
        ]
      },
      label: { type: 'plain_text', text: 'Priority' }
    }]
  }
});
```

### Scheduled Messages
```python
# Schedule daily standup reminder
import datetime
from slack_sdk import WebClient

slack = WebClient(token=bot_token)

# Schedule for tomorrow at 9 AM
tomorrow_9am = datetime.datetime.now() + datetime.timedelta(days=1)
tomorrow_9am = tomorrow_9am.replace(hour=9, minute=0, second=0)

slack.chat_scheduleMessage(
    channel="#team-standup",
    post_at=tomorrow_9am.timestamp(),
    text="🌅 Good morning! Time for daily standup. What are you working on today?"
)
```

## 📊 Analytics & Monitoring

### Message Analytics
```javascript
// Track message engagement
const analytics = {
  messages_sent: 0,
  reactions_received: 0,
  threads_created: 0,
  
  async trackMessage(result) {
    this.messages_sent++;
    // Store in database for reporting
    await db.saveMetric('slack_message', {
      channel: result.channel,
      timestamp: result.ts,
      user: result.message.user
    });
  }
};
```

### Workspace Activity
```python
# Monitor channel activity
channels = slack.conversations_list()['channels']
for channel in channels:
    history = slack.conversations_history(
        channel=channel['id'],
        limit=100
    )
    print(f"{channel['name']}: {len(history['messages'])} messages")
```

## 🔒 Security Best Practices

### Token Management
```javascript
// Use environment variables
const token = process.env.SLACK_BOT_TOKEN;

// Rotate tokens regularly
// Never commit tokens to Git
// Use OAuth for user actions
```

### Permission Scoping
```yaml
# Minimum required scopes only
bot_scopes:
  - chat:write         # Send messages
  - channels:read      # Read channel info
  # Don't request:
  # - channels:write    # Unless needed
  # - groups:write      # Unless needed
```

## 🏢 Enterprise Features

### Enterprise Grid
```javascript
// Cross-workspace channel sharing
await client.admin.conversations.setTeams({
  channel_id: 'C1234567890',
  team_id: 'T0987654321',
  org_channel: true  // Share across Enterprise Grid
});
```

### Compliance & eDiscovery
```python
# Export messages for compliance
exports = slack.admin.conversations.getConversationExport(
    channel='C1234567890',
    from_ts='1577836800',  # Jan 1, 2020
    to_ts='1609459200'      # Jan 1, 2021
)
```

## 📈 ROI & Business Value

### Productivity Gains
- **30% reduction** in email volume
- **25% faster** decision making
- **50% fewer** meetings needed
- **2x faster** incident resolution

### Integration Benefits
- Centralized notifications
- Reduced context switching
- Improved team visibility
- Automated workflows

## 🔗 Related MCP Servers

**Complementary**:
- GitHub (code notifications)
- Jira (project updates)
- PagerDuty (incident alerts)

**Alternatives**:
- Microsoft Teams
- Discord
- Mattermost (open source)

## 📚 Resources

- [Slack API Documentation](https://api.slack.com)
- [Bolt Framework](https://slack.dev/bolt)
- [Block Kit Builder](https://app.slack.com/block-kit-builder)
- [Slack App Directory](https://slack.com/apps)

---

**Verdict**: Essential for modern team communication with unmatched integration ecosystem. The free tier is generous for small teams, and the platform scales seamlessly to enterprise needs. The API is well-designed and the developer experience is excellent.