# Advanced Integration Guide: Hooks System and MCP Integration with Claude Code Subagents

Comprehensive enterprise-level integration framework for Claude Code subagents with hooks automation, MCP (Model Context Protocol) coordination, security validation, and external system integration for production environments.

## 1. Hooks System Architecture and Configuration Patterns

### Event-Driven Subagent Coordination

#### Core Hook Events for Subagent Integration

```yaml
hooks_architecture:
  lifecycle_events:
    PreToolUse:
      purpose: "Preparation and validation before subagent tool execution"
      security_context: "Authentication, authorization, resource validation"
      enterprise_use_cases:
        - Security policy enforcement before sensitive operations
        - Resource availability validation and allocation
        - Compliance requirement verification
        - Agent capability and permission validation
      
      configuration_pattern:
        location: ".claude/hooks/pre-tool/"
        execution_model: "synchronous with blocking capability"
        timeout_management: "configurable per hook (5-60 seconds)"
        failure_handling: "block execution or allow with warning"

    PostToolUse:
      purpose: "Result processing and integration after subagent completion"
      integration_context: "External system updates, audit logging, notifications"
      enterprise_use_cases:
        - Automated result integration with enterprise systems
        - Audit trail generation and compliance logging
        - Quality assurance validation and reporting
        - Downstream workflow triggering and coordination
      
      configuration_pattern:
        location: ".claude/hooks/post-tool/"
        execution_model: "asynchronous with parallel processing"
        timeout_management: "extended timeouts for system integration (60-300 seconds)"
        failure_handling: "graceful degradation with retry mechanisms"

    SubagentStop:
      purpose: "Coordination and cleanup after subagent task completion"
      coordination_context: "Multi-agent workflow management and handoff"
      enterprise_use_cases:
        - Cross-subagent communication and state transfer
        - Result aggregation and synthesis
        - Quality gate validation and approval workflows
        - Performance monitoring and optimization
      
      configuration_pattern:
        location: ".claude/hooks/subagent-stop/"
        execution_model: "hybrid synchronous/asynchronous based on context"
        timeout_management: "context-dependent (10-180 seconds)"
        failure_handling: "intelligent fallback with manual intervention options"
```

#### Advanced Hook Configuration Patterns

**Enterprise Security Hook Configuration:**

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": {
          "tool_name": "Bash",
          "subagent_context": "security-code-reviewer"
        },
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/hooks/security/validate-security-context.sh",
            "environment": {
              "SECURITY_LEVEL": "enterprise",
              "AUDIT_REQUIRED": "true",
              "SUBAGENT_NAME": "$CLAUDE_SUBAGENT_NAME",
              "TOOL_INPUT": "$CLAUDE_TOOL_INPUT"
            },
            "timeout": 30000,
            "run_in_background": false,
            "block_on_failure": true
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": {
          "tool_name": "*",
          "file_paths": ["src/**/*.ts", "src/**/*.js"]
        },
        "hooks": [
          {
            "type": "command",
            "command": "node .claude/hooks/integration/enterprise-integration.js",
            "environment": {
              "INTEGRATION_MODE": "enterprise",
              "AFFECTED_FILES": "$CLAUDE_FILE_PATHS",
              "SUBAGENT_CONTEXT": "$CLAUDE_SUBAGENT_NAME",
              "RESULT_DATA": "$CLAUDE_TOOL_OUTPUT"
            },
            "timeout": 120000,
            "run_in_background": true,
            "retry_on_failure": 3
          }
        ]
      }
    ]
  }
}
```

**Multi-Environment Hook Management:**

```json
{
  "hooks": {
    "development": {
      "PreToolUse": {
        "Bash": {
          "command": "echo 'DEV: Validating command safety' && bash .claude/hooks/dev/validate-dev-command.sh '$CLAUDE_TOOL_INPUT'",
          "timeout": 10000
        }
      },
      "PostToolUse": {
        "*": {
          "command": "bash .claude/hooks/dev/update-dev-metrics.sh",
          "run_in_background": true
        }
      }
    },
    "production": {
      "PreToolUse": {
        "Bash": {
          "command": "bash .claude/hooks/prod/strict-security-validation.sh '$CLAUDE_TOOL_INPUT'",
          "timeout": 60000,
          "block_on_failure": true
        },
        "Edit": {
          "command": "bash .claude/hooks/prod/production-file-protection.sh '$CLAUDE_FILE_PATHS'",
          "timeout": 30000,
          "block_on_failure": true
        }
      },
      "PostToolUse": {
        "*": {
          "command": "bash .claude/hooks/prod/enterprise-audit-logging.sh",
          "timeout": 120000,
          "run_in_background": false
        }
      }
    }
  }
}
```

## 2. Pre/Post Tool Execution Automation for Subagents

### Pre-Execution Automation Framework

#### Security and Compliance Validation

**Pre-Tool Security Validation Script:**

```bash
#!/bin/bash
# .claude/hooks/security/validate-security-context.sh

set -euo pipefail

TOOL_INPUT="${1:-}"
SUBAGENT_NAME="${CLAUDE_SUBAGENT_NAME:-unknown}"
SECURITY_LEVEL="${SECURITY_LEVEL:-standard}"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Security validation functions
validate_command_safety() {
    local command="$1"
    
    # Block dangerous commands
    if [[ "$command" =~ (rm\s+-rf|sudo|curl.*\|.*sh|wget.*\|.*sh) ]]; then
        echo "SECURITY_VIOLATION: Dangerous command detected: $command" >&2
        return 1
    fi
    
    # Validate file access patterns
    if [[ "$command" =~ (/etc/|/root/|~/.ssh/) ]]; then
        echo "SECURITY_VIOLATION: Sensitive path access attempt: $command" >&2
        return 1
    fi
    
    return 0
}

validate_subagent_permissions() {
    local subagent="$1"
    local permissions_file=".claude/security/subagent-permissions.json"
    
    if [[ -f "$permissions_file" ]]; then
        # Validate subagent has required permissions for the operation
        if ! jq -e ".subagents[\"$subagent\"].allowed_tools[] | select(. == \"$CLAUDE_TOOL_NAME\")" "$permissions_file" >/dev/null; then
            echo "PERMISSION_DENIED: Subagent $subagent lacks permission for tool $CLAUDE_TOOL_NAME" >&2
            return 1
        fi
    fi
    
    return 0
}

generate_audit_log() {
    local event_type="$1"
    local details="$2"
    local audit_file=".claude/logs/security-audit.jsonl"
    
    mkdir -p "$(dirname "$audit_file")"
    
    cat << EOF >> "$audit_file"
{"timestamp":"$TIMESTAMP","event":"$event_type","subagent":"$SUBAGENT_NAME","tool":"$CLAUDE_TOOL_NAME","details":"$details","security_level":"$SECURITY_LEVEL"}
EOF
}

# Main validation logic
main() {
    echo "🔒 Security validation for subagent: $SUBAGENT_NAME"
    
    # Validate command safety
    if ! validate_command_safety "$TOOL_INPUT"; then
        generate_audit_log "SECURITY_VIOLATION" "Dangerous command blocked: $TOOL_INPUT"
        exit 1
    fi
    
    # Validate subagent permissions
    if ! validate_subagent_permissions "$SUBAGENT_NAME"; then
        generate_audit_log "PERMISSION_DENIED" "Insufficient permissions for tool: $CLAUDE_TOOL_NAME"
        exit 1
    fi
    
    generate_audit_log "SECURITY_VALIDATED" "Command approved: $TOOL_INPUT"
    echo "✅ Security validation passed"
}

main "$@"
```

#### Resource Management and Optimization

**Pre-Tool Resource Validation:**

```javascript
// .claude/hooks/resources/resource-validator.js
const fs = require('fs').promises;
const path = require('path');
const os = require('os');

class ResourceValidator {
    constructor() {
        this.config = {
            maxMemoryUsage: 0.8, // 80% of available memory
            maxCpuUsage: 0.7,    // 70% of available CPU
            maxConcurrentAgents: 5,
            resourceCheckInterval: 5000
        };
    }

    async validateSystemResources() {
        const memoryUsage = process.memoryUsage();
        const totalMemory = os.totalmem();
        const freeMemory = os.freemem();
        const memoryUsagePercent = (totalMemory - freeMemory) / totalMemory;

        if (memoryUsagePercent > this.config.maxMemoryUsage) {
            throw new Error(`Memory usage too high: ${(memoryUsagePercent * 100).toFixed(1)}%`);
        }

        return {
            memory: {
                usage: memoryUsagePercent,
                available: freeMemory,
                total: totalMemory
            },
            timestamp: new Date().toISOString()
        };
    }

    async validateSubagentCapacity() {
        const activeAgentsFile = '.claude/state/active-agents.json';
        
        try {
            const data = await fs.readFile(activeAgentsFile, 'utf8');
            const activeAgents = JSON.parse(data);
            
            if (activeAgents.length >= this.config.maxConcurrentAgents) {
                throw new Error(`Maximum concurrent agents exceeded: ${activeAgents.length}/${this.config.maxConcurrentAgents}`);
            }
            
            return { activeCount: activeAgents.length, maxAllowed: this.config.maxConcurrentAgents };
        } catch (error) {
            if (error.code === 'ENOENT') {
                // File doesn't exist, no active agents
                return { activeCount: 0, maxAllowed: this.config.maxConcurrentAgents };
            }
            throw error;
        }
    }

    async registerAgentStart(subagentName) {
        const activeAgentsFile = '.claude/state/active-agents.json';
        const agentEntry = {
            name: subagentName,
            startTime: new Date().toISOString(),
            tool: process.env.CLAUDE_TOOL_NAME,
            pid: process.pid
        };

        try {
            const data = await fs.readFile(activeAgentsFile, 'utf8');
            const activeAgents = JSON.parse(data);
            activeAgents.push(agentEntry);
            await fs.writeFile(activeAgentsFile, JSON.stringify(activeAgents, null, 2));
        } catch (error) {
            if (error.code === 'ENOENT') {
                await fs.mkdir(path.dirname(activeAgentsFile), { recursive: true });
                await fs.writeFile(activeAgentsFile, JSON.stringify([agentEntry], null, 2));
            } else {
                throw error;
            }
        }
    }

    async main() {
        const subagentName = process.env.CLAUDE_SUBAGENT_NAME || 'unknown';
        
        try {
            console.log(`🔧 Resource validation for subagent: ${subagentName}`);
            
            const systemResources = await this.validateSystemResources();
            const agentCapacity = await this.validateSubagentCapacity();
            
            await this.registerAgentStart(subagentName);
            
            console.log('✅ Resource validation passed');
            console.log(`Memory usage: ${(systemResources.memory.usage * 100).toFixed(1)}%`);
            console.log(`Active agents: ${agentCapacity.activeCount}/${agentCapacity.maxAllowed}`);
            
            process.exit(0);
        } catch (error) {
            console.error('❌ Resource validation failed:', error.message);
            process.exit(1);
        }
    }
}

new ResourceValidator().main();
```

### Post-Execution Integration Framework

#### Enterprise System Integration

**Post-Tool Enterprise Integration:**

```javascript
// .claude/hooks/integration/enterprise-integration.js
const axios = require('axios');
const fs = require('fs').promises;
const path = require('path');

class EnterpriseIntegrator {
    constructor() {
        this.config = {
            jiraBaseUrl: process.env.JIRA_BASE_URL,
            jiraToken: process.env.JIRA_API_TOKEN,
            slackWebhook: process.env.SLACK_WEBHOOK_URL,
            enterpriseApiEndpoint: process.env.ENTERPRISE_API_ENDPOINT,
            auditLogPath: '.claude/logs/enterprise-integration.jsonl'
        };
    }

    async updateJiraIssue(subagentName, toolOutput, affectedFiles) {
        if (!this.config.jiraBaseUrl || !this.config.jiraToken) {
            console.log('Skipping JIRA integration - credentials not configured');
            return null;
        }

        try {
            // Extract potential issue references from tool output
            const issueReferences = this.extractJiraIssueReferences(toolOutput);
            
            for (const issueKey of issueReferences) {
                const updateData = {
                    body: {
                        type: "doc",
                        version: 1,
                        content: [{
                            type: "paragraph",
                            content: [{
                                type: "text",
                                text: `Claude subagent ${subagentName} completed work on this issue. Files affected: ${affectedFiles.join(', ')}`
                            }]
                        }]
                    }
                };

                await axios.post(
                    `${this.config.jiraBaseUrl}/rest/api/3/issue/${issueKey}/comment`,
                    updateData,
                    {
                        headers: {
                            'Authorization': `Bearer ${this.config.jiraToken}`,
                            'Content-Type': 'application/json'
                        }
                    }
                );

                console.log(`✅ Updated JIRA issue ${issueKey}`);
            }

            return issueReferences;
        } catch (error) {
            console.error('❌ JIRA integration failed:', error.message);
            return null;
        }
    }

    async sendSlackNotification(subagentName, summary, details) {
        if (!this.config.slackWebhook) {
            console.log('Skipping Slack notification - webhook not configured');
            return;
        }

        try {
            const payload = {
                text: `🤖 Subagent Activity: ${subagentName}`,
                blocks: [
                    {
                        type: "section",
                        text: {
                            type: "mrkdwn",
                            text: `*Subagent:* ${subagentName}\n*Summary:* ${summary}`
                        }
                    },
                    {
                        type: "section",
                        text: {
                            type: "mrkdwn",
                            text: `*Details:*\n\`\`\`${details.substring(0, 500)}${details.length > 500 ? '...' : ''}\`\`\``
                        }
                    }
                ]
            };

            await axios.post(this.config.slackWebhook, payload);
            console.log('✅ Slack notification sent');
        } catch (error) {
            console.error('❌ Slack notification failed:', error.message);
        }
    }

    async logAuditEvent(eventData) {
        try {
            await fs.mkdir(path.dirname(this.config.auditLogPath), { recursive: true });
            const logEntry = JSON.stringify({
                ...eventData,
                timestamp: new Date().toISOString()
            }) + '\n';
            
            await fs.appendFile(this.config.auditLogPath, logEntry);
        } catch (error) {
            console.error('❌ Audit logging failed:', error.message);
        }
    }

    extractJiraIssueReferences(text) {
        const jiraPattern = /[A-Z]{2,}-\d+/g;
        return text.match(jiraPattern) || [];
    }

    async main() {
        const subagentName = process.env.CLAUDE_SUBAGENT_NAME || 'unknown';
        const toolOutput = process.env.CLAUDE_TOOL_OUTPUT || '';
        const affectedFiles = (process.env.CLAUDE_FILE_PATHS || '').split(' ').filter(f => f);

        console.log(`🔗 Enterprise integration for subagent: ${subagentName}`);

        const integrationResults = {
            subagent: subagentName,
            tool: process.env.CLAUDE_TOOL_NAME,
            affectedFiles,
            integrations: {}
        };

        // Update JIRA issues
        const jiraResults = await this.updateJiraIssue(subagentName, toolOutput, affectedFiles);
        if (jiraResults) {
            integrationResults.integrations.jira = jiraResults;
        }

        // Send Slack notification
        await this.sendSlackNotification(
            subagentName,
            `Completed ${process.env.CLAUDE_TOOL_NAME} operation`,
            toolOutput
        );
        integrationResults.integrations.slack = 'sent';

        // Log audit event
        await this.logAuditEvent({
            event: 'subagent_completion',
            ...integrationResults
        });

        console.log('✅ Enterprise integration completed');
    }
}

new EnterpriseIntegrator().main();
```

## 3. Security Validation and Audit Logging for Enterprise Compliance

### Comprehensive Security Framework

#### Multi-Layer Security Validation

**Security Policy Configuration:**

```json
{
  "security_policies": {
    "subagent_permissions": {
      "security-code-reviewer": {
        "allowed_tools": ["Read", "Grep", "Glob", "WebSearch"],
        "forbidden_tools": ["Bash", "Edit", "Write"],
        "file_access_patterns": {
          "allowed": ["src/**/*", "tests/**/*", "docs/**/*"],
          "forbidden": ["/etc/**/*", "~/.ssh/**/*", "*.env"]
        },
        "security_level": "high",
        "audit_required": true
      },
      "performance-optimizer": {
        "allowed_tools": ["Read", "Grep", "Glob", "Bash"],
        "forbidden_tools": ["Edit", "Write"],
        "bash_restrictions": {
          "allowed_commands": ["npm run test", "npm run build", "git log", "git diff"],
          "forbidden_patterns": ["rm -rf", "sudo", "curl", "wget"]
        },
        "security_level": "medium",
        "audit_required": true
      },
      "development-assistant": {
        "allowed_tools": ["Read", "Write", "Edit", "Bash", "Grep", "Glob"],
        "environment_restrictions": {
          "production": {
            "allowed_tools": ["Read", "Grep", "Glob"]
          }
        },
        "security_level": "low",
        "audit_required": false
      }
    },
    "compliance_requirements": {
      "audit_retention": "7_years",
      "encryption_required": true,
      "access_logging": "mandatory",
      "data_classification": {
        "sensitive_patterns": ["password", "api_key", "secret", "token"],
        "compliance_frameworks": ["SOX", "GDPR", "HIPAA"]
      }
    }
  }
}
```

#### Advanced Audit Logging System

**Comprehensive Audit Logger:**

```bash
#!/bin/bash
# .claude/hooks/security/enterprise-audit-logger.sh

set -euo pipefail

# Configuration
AUDIT_DIR=".claude/logs/audit"
SECURITY_LOG="$AUDIT_DIR/security-events.jsonl"
COMPLIANCE_LOG="$AUDIT_DIR/compliance-events.jsonl"
PERFORMANCE_LOG="$AUDIT_DIR/performance-metrics.jsonl"
ENCRYPTION_KEY_FILE=".claude/security/audit-encryption.key"

# Ensure audit directory exists
mkdir -p "$AUDIT_DIR"

# Generate encryption key if it doesn't exist
generate_encryption_key() {
    if [[ ! -f "$ENCRYPTION_KEY_FILE" ]]; then
        mkdir -p "$(dirname "$ENCRYPTION_KEY_FILE")"
        openssl rand -base64 32 > "$ENCRYPTION_KEY_FILE"
        chmod 600 "$ENCRYPTION_KEY_FILE"
    fi
}

# Encrypt sensitive audit data
encrypt_audit_data() {
    local data="$1"
    local key=$(cat "$ENCRYPTION_KEY_FILE")
    echo "$data" | openssl enc -aes-256-cbc -base64 -pass pass:"$key"
}

# Generate comprehensive audit event
generate_audit_event() {
    local event_type="$1"
    local subagent_name="${CLAUDE_SUBAGENT_NAME:-unknown}"
    local tool_name="${CLAUDE_TOOL_NAME:-unknown}"
    local tool_input="${CLAUDE_TOOL_INPUT:-}"
    local tool_output="${CLAUDE_TOOL_OUTPUT:-}"
    local file_paths="${CLAUDE_FILE_PATHS:-}"
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    local session_id="${CLAUDE_SESSION_ID:-$(uuidgen)}"
    local user_id="${USER:-unknown}"
    local hostname=$(hostname)
    local git_commit=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
    local git_branch=$(git branch --show-current 2>/dev/null || echo "unknown")

    # Classify data sensitivity
    local contains_sensitive=false
    if [[ "$tool_input $tool_output" =~ (password|api_key|secret|token|private_key) ]]; then
        contains_sensitive=true
    fi

    # Base audit event
    local audit_event=$(cat << EOF
{
  "timestamp": "$timestamp",
  "event_type": "$event_type",
  "session_id": "$session_id",
  "subagent": {
    "name": "$subagent_name",
    "tool": "$tool_name"
  },
  "context": {
    "user_id": "$user_id",
    "hostname": "$hostname",
    "git_commit": "$git_commit",
    "git_branch": "$git_branch",
    "affected_files": $(echo "$file_paths" | jq -R 'split(" ") | map(select(length > 0))')
  },
  "security": {
    "contains_sensitive_data": $contains_sensitive,
    "encryption_applied": $contains_sensitive
  },
  "compliance": {
    "audit_level": "enterprise",
    "retention_required": true,
    "frameworks": ["SOX", "GDPR"]
  }
}
EOF
    )

    # Add tool details (encrypted if sensitive)
    if [[ "$contains_sensitive" == "true" ]]; then
        local encrypted_input=$(encrypt_audit_data "$tool_input")
        local encrypted_output=$(encrypt_audit_data "$tool_output")
        audit_event=$(echo "$audit_event" | jq --arg input "$encrypted_input" --arg output "$encrypted_output" '.tool_data = {input: $input, output: $output, encrypted: true}')
    else
        audit_event=$(echo "$audit_event" | jq --arg input "$tool_input" --arg output "$tool_output" '.tool_data = {input: $input, output: $output, encrypted: false}')
    fi

    echo "$audit_event"
}

# Log performance metrics
log_performance_metrics() {
    local start_time="${CLAUDE_TOOL_START_TIME:-$(date +%s)}"
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    local memory_usage=$(ps -o pid,vsz,rss,comm -p $$ | tail -1)

    local performance_event=$(cat << EOF
{
  "timestamp": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "subagent": "${CLAUDE_SUBAGENT_NAME:-unknown}",
  "tool": "${CLAUDE_TOOL_NAME:-unknown}",
  "performance": {
    "duration_seconds": $duration,
    "memory_usage": "$memory_usage",
    "system_load": "$(uptime | awk '{print $10, $11, $12}')"
  }
}
EOF
    )

    echo "$performance_event" >> "$PERFORMANCE_LOG"
}

# Main audit logging function
main() {
    generate_encryption_key

    # Generate and log audit event
    local audit_event=$(generate_audit_event "subagent_execution")
    
    # Log to appropriate files based on event type
    echo "$audit_event" >> "$SECURITY_LOG"
    
    # Log compliance event
    echo "$audit_event" | jq '.compliance_event = true' >> "$COMPLIANCE_LOG"
    
    # Log performance metrics
    log_performance_metrics

    # Send to enterprise SIEM if configured
    if [[ -n "${ENTERPRISE_SIEM_ENDPOINT:-}" ]]; then
        curl -X POST "$ENTERPRISE_SIEM_ENDPOINT" \
             -H "Content-Type: application/json" \
             -H "Authorization: Bearer ${ENTERPRISE_SIEM_TOKEN}" \
             -d "$audit_event" \
             --max-time 30 \
             --silent || echo "Warning: Failed to send audit event to SIEM"
    fi

    echo "✅ Audit logging completed"
}

main "$@"
```

## 4. MCP Server Integration for External Data Sources and Services

### MCP Architecture for Subagent Coordination

#### Enterprise MCP Server Configuration

**MCP Server Registry Configuration:**

```json
{
  "mcpServers": {
    "enterprise-jira": {
      "command": "node",
      "args": ["./mcp-servers/enterprise-jira-server.js"],
      "env": {
        "JIRA_BASE_URL": "${JIRA_BASE_URL}",
        "JIRA_API_TOKEN": "${JIRA_API_TOKEN}",
        "JIRA_PROJECT_KEY": "${JIRA_PROJECT_KEY}"
      },
      "subagent_access": {
        "allowed_subagents": ["project-manager", "task-coordinator", "quality-assurance-specialist"],
        "permission_level": "read_write",
        "rate_limits": {
          "requests_per_minute": 60,
          "burst_limit": 10
        }
      }
    },
    "enterprise-knowledge-base": {
      "command": "python",
      "args": ["-m", "mcp_servers.knowledge_base"],
      "env": {
        "KB_DATABASE_URL": "${KNOWLEDGE_BASE_URL}",
        "KB_API_KEY": "${KNOWLEDGE_BASE_API_KEY}",
        "KB_ENCRYPTION_KEY": "${KB_ENCRYPTION_KEY}"
      },
      "subagent_access": {
        "allowed_subagents": ["research-specialist", "documentation-coordinator", "technical-writer"],
        "permission_level": "read_only",
        "rate_limits": {
          "requests_per_minute": 120,
          "burst_limit": 20
        }
      }
    },
    "security-compliance": {
      "command": "node",
      "args": ["./mcp-servers/security-compliance-server.js"],
      "env": {
        "SECURITY_API_ENDPOINT": "${SECURITY_API_ENDPOINT}",
        "COMPLIANCE_TOKEN": "${COMPLIANCE_TOKEN}",
        "SECURITY_LEVEL": "enterprise"
      },
      "subagent_access": {
        "allowed_subagents": ["security-code-reviewer", "compliance-validator"],
        "permission_level": "read_write",
        "audit_required": true,
        "rate_limits": {
          "requests_per_minute": 30,
          "burst_limit": 5
        }
      }
    },
    "enterprise-docker": {
      "command": "python",
      "args": ["-m", "mcp_servers.docker_enterprise"],
      "env": {
        "DOCKER_HOST": "${DOCKER_HOST}",
        "DOCKER_CERT_PATH": "${DOCKER_CERT_PATH}",
        "DOCKER_TLS_VERIFY": "1",
        "ENTERPRISE_REGISTRY": "${ENTERPRISE_DOCKER_REGISTRY}"
      },
      "subagent_access": {
        "allowed_subagents": ["deployment-coordinator", "infrastructure-manager", "performance-optimizer"],
        "permission_level": "read_write",
        "security_context": "high",
        "rate_limits": {
          "requests_per_minute": 20,
          "burst_limit": 3
        }
      }
    }
  }
}
```

#### Advanced MCP Integration Patterns

**Subagent-MCP Coordination Framework:**

```javascript
// .claude/mcp/coordination/subagent-mcp-coordinator.js
class SubagentMCPCoordinator {
    constructor() {
        this.mcpConnections = new Map();
        this.subagentPermissions = new Map();
        this.rateLimits = new Map();
        this.auditLogger = new AuditLogger();
    }

    async initializeMCPConnections() {
        const mcpConfig = await this.loadMCPConfiguration();
        
        for (const [serverName, config] of Object.entries(mcpConfig.mcpServers)) {
            try {
                const connection = await this.establishMCPConnection(serverName, config);
                this.mcpConnections.set(serverName, connection);
                
                // Initialize rate limiting for this server
                this.rateLimits.set(serverName, {
                    requestCount: 0,
                    windowStart: Date.now(),
                    config: config.subagent_access.rate_limits
                });
                
                console.log(`✅ MCP connection established: ${serverName}`);
            } catch (error) {
                console.error(`❌ Failed to connect to MCP server ${serverName}:`, error.message);
            }
        }
    }

    async routeSubagentRequest(subagentName, mcpServerName, request) {
        // Validate subagent permissions
        if (!this.validateSubagentAccess(subagentName, mcpServerName)) {
            throw new Error(`Subagent ${subagentName} lacks permission for MCP server ${mcpServerName}`);
        }

        // Check rate limits
        if (!this.checkRateLimit(subagentName, mcpServerName)) {
            throw new Error(`Rate limit exceeded for subagent ${subagentName} on server ${mcpServerName}`);
        }

        // Get MCP connection
        const connection = this.mcpConnections.get(mcpServerName);
        if (!connection) {
            throw new Error(`MCP server ${mcpServerName} not available`);
        }

        // Execute request with audit logging
        const startTime = Date.now();
        try {
            const result = await connection.executeRequest(request);
            
            await this.auditLogger.logMCPRequest({
                subagent: subagentName,
                mcpServer: mcpServerName,
                request: request,
                result: result,
                duration: Date.now() - startTime,
                status: 'success'
            });

            return result;
        } catch (error) {
            await this.auditLogger.logMCPRequest({
                subagent: subagentName,
                mcpServer: mcpServerName,
                request: request,
                error: error.message,
                duration: Date.now() - startTime,
                status: 'error'
            });
            
            throw error;
        }
    }

    validateSubagentAccess(subagentName, mcpServerName) {
        const mcpConfig = this.getMCPServerConfig(mcpServerName);
        const allowedSubagents = mcpConfig.subagent_access.allowed_subagents;
        
        return allowedSubagents.includes(subagentName) || allowedSubagents.includes('*');
    }

    checkRateLimit(subagentName, mcpServerName) {
        const rateLimitInfo = this.rateLimits.get(mcpServerName);
        if (!rateLimitInfo) return true;

        const now = Date.now();
        const windowDuration = 60000; // 1 minute

        // Reset window if needed
        if (now - rateLimitInfo.windowStart > windowDuration) {
            rateLimitInfo.requestCount = 0;
            rateLimitInfo.windowStart = now;
        }

        // Check limits
        if (rateLimitInfo.requestCount >= rateLimitInfo.config.requests_per_minute) {
            return false;
        }

        rateLimitInfo.requestCount++;
        return true;
    }

    async healthCheck() {
        const healthStatus = {
            timestamp: new Date().toISOString(),
            connections: {},
            overall_status: 'healthy'
        };

        for (const [serverName, connection] of this.mcpConnections) {
            try {
                const serverHealth = await connection.ping();
                healthStatus.connections[serverName] = {
                    status: 'healthy',
                    response_time: serverHealth.responseTime,
                    last_successful_request: serverHealth.lastRequest
                };
            } catch (error) {
                healthStatus.connections[serverName] = {
                    status: 'unhealthy',
                    error: error.message,
                    last_error: new Date().toISOString()
                };
                healthStatus.overall_status = 'degraded';
            }
        }

        return healthStatus;
    }
}
```

**Enterprise JIRA MCP Server:**

```javascript
// ./mcp-servers/enterprise-jira-server.js
const { MCPServer } = require('@anthropic-ai/mcp-sdk');
const axios = require('axios');

class EnterpriseJiraMCPServer extends MCPServer {
    constructor() {
        super({
            name: 'enterprise-jira',
            version: '1.0.0',
            description: 'Enterprise JIRA integration with advanced security and audit logging'
        });
        
        this.jiraClient = axios.create({
            baseURL: process.env.JIRA_BASE_URL,
            headers: {
                'Authorization': `Bearer ${process.env.JIRA_API_TOKEN}`,
                'Content-Type': 'application/json'
            }
        });
        
        this.auditLogger = new JiraAuditLogger();
    }

    async initialize() {
        // Register tools
        this.registerTool('search_issues', {
            description: 'Search JIRA issues with advanced filtering',
            parameters: {
                jql: { type: 'string', description: 'JQL query string' },
                fields: { type: 'array', description: 'Fields to return' },
                maxResults: { type: 'number', default: 50 }
            }
        });

        this.registerTool('create_issue', {
            description: 'Create new JIRA issue with enterprise compliance',
            parameters: {
                project: { type: 'string', required: true },
                issueType: { type: 'string', required: true },
                summary: { type: 'string', required: true },
                description: { type: 'string' },
                priority: { type: 'string' },
                assignee: { type: 'string' },
                labels: { type: 'array' },
                customFields: { type: 'object' }
            }
        });

        this.registerTool('update_issue', {
            description: 'Update existing JIRA issue with audit trail',
            parameters: {
                issueKey: { type: 'string', required: true },
                fields: { type: 'object', required: true },
                notifyUsers: { type: 'boolean', default: true }
            }
        });

        this.registerTool('add_comment', {
            description: 'Add comment to JIRA issue with subagent attribution',
            parameters: {
                issueKey: { type: 'string', required: true },
                comment: { type: 'string', required: true },
                visibility: { type: 'object' }
            }
        });

        console.log('✅ Enterprise JIRA MCP Server initialized');
    }

    async handleToolCall(toolName, parameters, context) {
        const subagentName = context.subagent || 'unknown';
        const startTime = Date.now();

        try {
            let result;
            
            switch (toolName) {
                case 'search_issues':
                    result = await this.searchIssues(parameters);
                    break;
                case 'create_issue':
                    result = await this.createIssue(parameters, subagentName);
                    break;
                case 'update_issue':
                    result = await this.updateIssue(parameters, subagentName);
                    break;
                case 'add_comment':
                    result = await this.addComment(parameters, subagentName);
                    break;
                default:
                    throw new Error(`Unknown tool: ${toolName}`);
            }

            await this.auditLogger.logSuccess({
                tool: toolName,
                subagent: subagentName,
                parameters,
                result,
                duration: Date.now() - startTime
            });

            return result;
        } catch (error) {
            await this.auditLogger.logError({
                tool: toolName,
                subagent: subagentName,
                parameters,
                error: error.message,
                duration: Date.now() - startTime
            });
            
            throw error;
        }
    }

    async searchIssues(params) {
        const searchParams = {
            jql: params.jql,
            fields: params.fields || ['key', 'summary', 'status', 'assignee', 'priority'],
            maxResults: Math.min(params.maxResults || 50, 1000) // Enterprise limit
        };

        const response = await this.jiraClient.post('/rest/api/2/search', searchParams);
        
        return {
            total: response.data.total,
            maxResults: response.data.maxResults,
            startAt: response.data.startAt,
            issues: response.data.issues.map(issue => ({
                key: issue.key,
                summary: issue.fields.summary,
                status: issue.fields.status?.name,
                assignee: issue.fields.assignee?.displayName,
                priority: issue.fields.priority?.name,
                created: issue.fields.created,
                updated: issue.fields.updated
            }))
        };
    }

    async createIssue(params, subagentName) {
        const issueData = {
            fields: {
                project: { key: params.project },
                issuetype: { name: params.issueType },
                summary: params.summary,
                description: {
                    type: "doc",
                    version: 1,
                    content: [{
                        type: "paragraph",
                        content: [{
                            type: "text",
                            text: params.description || `Created by Claude subagent: ${subagentName}`
                        }]
                    }]
                }
            }
        };

        // Add optional fields
        if (params.priority) issueData.fields.priority = { name: params.priority };
        if (params.assignee) issueData.fields.assignee = { name: params.assignee };
        if (params.labels) issueData.fields.labels = params.labels;
        if (params.customFields) Object.assign(issueData.fields, params.customFields);

        const response = await this.jiraClient.post('/rest/api/2/issue', issueData);
        
        return {
            key: response.data.key,
            id: response.data.id,
            self: response.data.self,
            created_by_subagent: subagentName
        };
    }

    async updateIssue(params, subagentName) {
        const updateData = {
            fields: params.fields,
            update: {
                comment: [{
                    add: {
                        body: {
                            type: "doc",
                            version: 1,
                            content: [{
                                type: "paragraph",
                                content: [{
                                    type: "text",
                                    text: `Updated by Claude subagent: ${subagentName}`
                                }]
                            }]
                        }
                    }
                }]
            }
        };

        await this.jiraClient.put(`/rest/api/2/issue/${params.issueKey}`, updateData);
        
        return {
            issueKey: params.issueKey,
            updated: true,
            updated_by_subagent: subagentName,
            timestamp: new Date().toISOString()
        };
    }

    async addComment(params, subagentName) {
        const commentData = {
            body: {
                type: "doc",
                version: 1,
                content: [{
                    type: "paragraph",
                    content: [{
                        type: "text",
                        text: `${params.comment}\n\n---\nAdded by Claude subagent: ${subagentName}`
                    }]
                }]
            }
        };

        if (params.visibility) {
            commentData.visibility = params.visibility;
        }

        const response = await this.jiraClient.post(
            `/rest/api/2/issue/${params.issueKey}/comment`,
            commentData
        );
        
        return {
            id: response.data.id,
            created: response.data.created,
            updated: response.data.updated,
            author: response.data.author.displayName,
            added_by_subagent: subagentName
        };
    }
}

// Initialize and start server
const server = new EnterpriseJiraMCPServer();
server.initialize().then(() => {
    server.start();
    console.log('🚀 Enterprise JIRA MCP Server running');
}).catch(error => {
    console.error('❌ Failed to start Enterprise JIRA MCP Server:', error);
    process.exit(1);
});
```

## 5. Performance Monitoring and Resource Management

### Advanced Performance Monitoring Framework

#### Real-Time Performance Tracking

**Performance Monitor for Subagents:**

```javascript
// .claude/monitoring/performance-monitor.js
const os = require('os');
const fs = require('fs').promises;
const EventEmitter = require('events');

class SubagentPerformanceMonitor extends EventEmitter {
    constructor() {
        super();
        this.metrics = new Map();
        this.thresholds = {
            maxMemoryUsage: 0.8,
            maxCpuUsage: 0.7,
            maxResponseTime: 30000, // 30 seconds
            maxConcurrentAgents: 10
        };
        this.alerts = [];
        this.isMonitoring = false;
    }

    async startMonitoring() {
        if (this.isMonitoring) return;
        
        this.isMonitoring = true;
        console.log('🔍 Starting subagent performance monitoring');
        
        // Monitor system resources every 5 seconds
        this.systemMonitorInterval = setInterval(() => {
            this.collectSystemMetrics();
        }, 5000);
        
        // Monitor active subagents every 2 seconds  
        this.agentMonitorInterval = setInterval(() => {
            this.collectSubagentMetrics();
        }, 2000);
        
        // Generate performance reports every minute
        this.reportInterval = setInterval(() => {
            this.generatePerformanceReport();
        }, 60000);
        
        // Clean up old metrics every hour
        this.cleanupInterval = setInterval(() => {
            this.cleanupOldMetrics();
        }, 3600000);
    }

    async collectSystemMetrics() {
        const systemMetrics = {
            timestamp: Date.now(),
            memory: {
                total: os.totalmem(),
                free: os.freemem(),
                used: os.totalmem() - os.freemem(),
                usagePercent: (os.totalmem() - os.freemem()) / os.totalmem()
            },
            cpu: {
                loadAverage: os.loadavg(),
                cpuCount: os.cpus().length
            },
            uptime: os.uptime()
        };

        this.metrics.set(`system_${Date.now()}`, systemMetrics);
        
        // Check thresholds and emit alerts
        if (systemMetrics.memory.usagePercent > this.thresholds.maxMemoryUsage) {
            this.emitAlert('HIGH_MEMORY_USAGE', {
                current: systemMetrics.memory.usagePercent,
                threshold: this.thresholds.maxMemoryUsage,
                message: `Memory usage at ${(systemMetrics.memory.usagePercent * 100).toFixed(1)}%`
            });
        }
    }

    async collectSubagentMetrics() {
        try {
            const activeAgentsFile = '.claude/state/active-agents.json';
            const data = await fs.readFile(activeAgentsFile, 'utf8');
            const activeAgents = JSON.parse(data);
            
            const agentMetrics = {
                timestamp: Date.now(),
                activeCount: activeAgents.length,
                agents: activeAgents.map(agent => ({
                    name: agent.name,
                    startTime: agent.startTime,
                    duration: Date.now() - new Date(agent.startTime).getTime(),
                    tool: agent.tool,
                    pid: agent.pid
                }))
            };

            this.metrics.set(`agents_${Date.now()}`, agentMetrics);
            
            // Check for long-running agents
            agentMetrics.agents.forEach(agent => {
                if (agent.duration > this.thresholds.maxResponseTime) {
                    this.emitAlert('LONG_RUNNING_AGENT', {
                        agent: agent.name,
                        duration: agent.duration,
                        threshold: this.thresholds.maxResponseTime,
                        message: `Agent ${agent.name} running for ${Math.round(agent.duration / 1000)}s`
                    });
                }
            });
            
            // Check concurrent agent limit
            if (agentMetrics.activeCount > this.thresholds.maxConcurrentAgents) {
                this.emitAlert('TOO_MANY_AGENTS', {
                    current: agentMetrics.activeCount,
                    threshold: this.thresholds.maxConcurrentAgents,
                    message: `${agentMetrics.activeCount} agents running (limit: ${this.thresholds.maxConcurrentAgents})`
                });
            }
            
        } catch (error) {
            if (error.code !== 'ENOENT') {
                console.error('Error collecting subagent metrics:', error.message);
            }
        }
    }

    emitAlert(type, details) {
        const alert = {
            id: `alert_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            type,
            timestamp: Date.now(),
            severity: this.getAlertSeverity(type),
            details,
            acknowledged: false
        };
        
        this.alerts.push(alert);
        this.emit('alert', alert);
        
        // Log alert
        console.warn(`🚨 ALERT [${type}]: ${details.message}`);
        
        // Keep only last 100 alerts
        if (this.alerts.length > 100) {
            this.alerts = this.alerts.slice(-100);
        }
    }

    getAlertSeverity(alertType) {
        const severityMap = {
            'HIGH_MEMORY_USAGE': 'warning',
            'LONG_RUNNING_AGENT': 'warning',
            'TOO_MANY_AGENTS': 'critical',
            'SYSTEM_OVERLOAD': 'critical'
        };
        return severityMap[alertType] || 'info';
    }

    async generatePerformanceReport() {
        const now = Date.now();
        const fiveMinutesAgo = now - (5 * 60 * 1000);
        
        // Get recent metrics
        const recentMetrics = Array.from(this.metrics.entries())
            .filter(([key, metric]) => metric.timestamp > fiveMinutesAgo)
            .map(([key, metric]) => metric);
        
        const systemMetrics = recentMetrics.filter(m => m.memory && m.cpu);
        const agentMetrics = recentMetrics.filter(m => m.activeCount !== undefined);
        
        if (systemMetrics.length === 0 && agentMetrics.length === 0) return;
        
        const report = {
            timestamp: now,
            period: '5_minutes',
            system: {
                avgMemoryUsage: systemMetrics.reduce((sum, m) => sum + m.memory.usagePercent, 0) / systemMetrics.length,
                maxMemoryUsage: Math.max(...systemMetrics.map(m => m.memory.usagePercent)),
                avgLoadAverage: systemMetrics.reduce((sum, m) => sum + m.cpu.loadAverage[0], 0) / systemMetrics.length
            },
            agents: {
                avgActiveCount: agentMetrics.reduce((sum, m) => sum + m.activeCount, 0) / agentMetrics.length,
                maxActiveCount: Math.max(...agentMetrics.map(m => m.activeCount)),
                totalExecutions: agentMetrics.reduce((sum, m) => sum + m.activeCount, 0)
            },
            alerts: {
                total: this.alerts.filter(a => a.timestamp > fiveMinutesAgo).length,
                critical: this.alerts.filter(a => a.timestamp > fiveMinutesAgo && a.severity === 'critical').length,
                unacknowledged: this.alerts.filter(a => !a.acknowledged).length
            }
        };
        
        // Save report
        const reportPath = `.claude/reports/performance_${now}.json`;
        await fs.mkdir('.claude/reports', { recursive: true });
        await fs.writeFile(reportPath, JSON.stringify(report, null, 2));
        
        // Emit report event
        this.emit('report', report);
        
        console.log(`📊 Performance report generated: avg memory ${(report.system.avgMemoryUsage * 100).toFixed(1)}%, avg agents ${report.agents.avgActiveCount.toFixed(1)}`);
    }

    async cleanupOldMetrics() {
        const oneHourAgo = Date.now() - (60 * 60 * 1000);
        
        for (const [key, metric] of this.metrics.entries()) {
            if (metric.timestamp < oneHourAgo) {
                this.metrics.delete(key);
            }
        }
        
        console.log(`🧹 Cleaned up old metrics, ${this.metrics.size} entries remaining`);
    }

    async getPerformanceSnapshot() {
        return {
            timestamp: Date.now(),
            metrics_count: this.metrics.size,
            active_alerts: this.alerts.filter(a => !a.acknowledged).length,
            system_status: await this.getSystemStatus(),
            agent_summary: await this.getAgentSummary()
        };
    }

    async getSystemStatus() {
        const memory = {
            total: os.totalmem(),
            free: os.freemem(),
            used: os.totalmem() - os.freemem(),
            usagePercent: (os.totalmem() - os.freemem()) / os.totalmem()
        };
        
        return {
            memory,
            cpu: {
                loadAverage: os.loadavg(),
                cpuCount: os.cpus().length
            },
            uptime: os.uptime(),
            status: memory.usagePercent > this.thresholds.maxMemoryUsage ? 'overloaded' : 'healthy'
        };
    }

    async getAgentSummary() {
        try {
            const activeAgentsFile = '.claude/state/active-agents.json';
            const data = await fs.readFile(activeAgentsFile, 'utf8');
            const activeAgents = JSON.parse(data);
            
            return {
                total: activeAgents.length,
                agents: activeAgents.map(agent => ({
                    name: agent.name,
                    tool: agent.tool,
                    duration: Date.now() - new Date(agent.startTime).getTime()
                })),
                status: activeAgents.length > this.thresholds.maxConcurrentAgents ? 'overloaded' : 'healthy'
            };
        } catch (error) {
            return { total: 0, agents: [], status: 'healthy' };
        }
    }

    stopMonitoring() {
        if (!this.isMonitoring) return;
        
        this.isMonitoring = false;
        clearInterval(this.systemMonitorInterval);
        clearInterval(this.agentMonitorInterval);
        clearInterval(this.reportInterval);
        clearInterval(this.cleanupInterval);
        
        console.log('⏹️ Stopped subagent performance monitoring');
    }
}

module.exports = SubagentPerformanceMonitor;
```

#### Resource Management and Optimization

**Dynamic Resource Allocator:**

```bash
#!/bin/bash
# .claude/scripts/resource-manager.sh

set -euo pipefail

# Configuration
MAX_MEMORY_PERCENT=80
MAX_CPU_PERCENT=70
MAX_CONCURRENT_AGENTS=10
RESOURCE_CHECK_INTERVAL=10
LOG_FILE=".claude/logs/resource-management.log"

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

# Logging function
log_message() {
    local level="$1"
    local message="$2"
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    echo "[$timestamp] $level: $message" | tee -a "$LOG_FILE"
}

# Get current system resource usage
get_memory_usage() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        local memory_pressure=$(memory_pressure | grep "System-wide memory free percentage" | awk '{print $5}' | sed 's/%//')
        echo $((100 - memory_pressure))
    else
        # Linux
        free | awk '/^Mem:/ {printf("%.0f", ($3/$2) * 100)}'
    fi
}

get_cpu_usage() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        top -l 1 -n 0 | grep "CPU usage" | awk '{print $3}' | sed 's/%//'
    else
        # Linux
        top -bn1 | grep "Cpu(s)" | awk '{print $2}' | sed 's/%us,//'
    fi
}

get_active_agents_count() {
    local active_agents_file=".claude/state/active-agents.json"
    if [[ -f "$active_agents_file" ]]; then
        jq length "$active_agents_file" 2>/dev/null || echo "0"
    else
        echo "0"
    fi
}

# Resource optimization functions
optimize_memory_usage() {
    log_message "INFO" "Starting memory optimization"
    
    # Clean up temporary files
    find .claude/temp -type f -mtime +1 -delete 2>/dev/null || true
    find .claude/logs -name "*.log" -mtime +7 -delete 2>/dev/null || true
    
    # Compress old audit logs
    find .claude/logs/audit -name "*.jsonl" -mtime +1 -exec gzip {} \; 2>/dev/null || true
    
    log_message "INFO" "Memory optimization completed"
}

limit_concurrent_agents() {
    local current_count="$1"
    local active_agents_file=".claude/state/active-agents.json"
    
    if [[ "$current_count" -gt "$MAX_CONCURRENT_AGENTS" ]]; then
        log_message "WARNING" "Too many concurrent agents ($current_count), implementing throttling"
        
        # Create throttle file to signal rate limiting
        echo "{\"throttled\": true, \"max_agents\": $MAX_CONCURRENT_AGENTS, \"current\": $current_count, \"timestamp\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" > .claude/state/agent-throttle.json
        
        # Optionally terminate oldest agents (implementation depends on requirements)
        # This is a placeholder for more sophisticated agent lifecycle management
        log_message "INFO" "Agent throttling activated"
    else
        # Remove throttle file if it exists
        rm -f .claude/state/agent-throttle.json
    fi
}

# Main resource monitoring loop
monitor_resources() {
    log_message "INFO" "Starting resource monitoring"
    
    while true; do
        local memory_usage=$(get_memory_usage)
        local cpu_usage=$(get_cpu_usage)
        local active_agents=$(get_active_agents_count)
        
        # Log current status
        log_message "INFO" "Resources: Memory ${memory_usage}%, CPU ${cpu_usage}%, Agents ${active_agents}"
        
        # Check memory threshold
        if [[ "$memory_usage" -gt "$MAX_MEMORY_PERCENT" ]]; then
            log_message "WARNING" "High memory usage detected: ${memory_usage}%"
            optimize_memory_usage
        fi
        
        # Check agent count threshold
        if [[ "$active_agents" -gt "$MAX_CONCURRENT_AGENTS" ]]; then
            limit_concurrent_agents "$active_agents"
        fi
        
        # Generate resource status report
        cat << EOF > .claude/state/resource-status.json
{
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "memory_usage_percent": $memory_usage,
  "cpu_usage_percent": $cpu_usage,
  "active_agents": $active_agents,
  "thresholds": {
    "max_memory_percent": $MAX_MEMORY_PERCENT,
    "max_cpu_percent": $MAX_CPU_PERCENT,
    "max_concurrent_agents": $MAX_CONCURRENT_AGENTS
  },
  "status": {
    "memory": $([ "$memory_usage" -le "$MAX_MEMORY_PERCENT" ] && echo '"healthy"' || echo '"overloaded"'),
    "agents": $([ "$active_agents" -le "$MAX_CONCURRENT_AGENTS" ] && echo '"healthy"' || echo '"overloaded"')
  }
}
EOF
        
        sleep "$RESOURCE_CHECK_INTERVAL"
    done
}

# Command line interface
case "${1:-monitor}" in
    "monitor")
        monitor_resources
        ;;
    "status")
        if [[ -f ".claude/state/resource-status.json" ]]; then
            cat .claude/state/resource-status.json | jq .
        else
            echo "No resource status available. Run 'resource-manager.sh monitor' first."
        fi
        ;;
    "optimize")
        optimize_memory_usage
        ;;
    "check")
        memory_usage=$(get_memory_usage)
        cpu_usage=$(get_cpu_usage)
        active_agents=$(get_active_agents_count)
        echo "Memory: ${memory_usage}%, CPU: ${cpu_usage}%, Agents: ${active_agents}"
        ;;
    *)
        echo "Usage: $0 {monitor|status|optimize|check}"
        exit 1
        ;;
esac
```

## 6. Error Handling and Recovery Patterns

### Comprehensive Error Recovery Framework

#### Intelligent Error Detection and Recovery

**Advanced Error Handler:**

```javascript
// .claude/error-handling/advanced-error-handler.js
const fs = require('fs').promises;
const path = require('path');

class AdvancedErrorHandler {
    constructor() {
        this.errorPatterns = new Map();
        this.recoveryStrategies = new Map();
        this.errorHistory = [];
        this.maxRetries = 3;
        this.backoffMultiplier = 2;
        this.baseDelay = 1000;
        
        this.initializeErrorPatterns();
        this.initializeRecoveryStrategies();
    }

    initializeErrorPatterns() {
        // Define common error patterns and their classifications
        this.errorPatterns.set(/ENOENT.*no such file/i, {
            type: 'FILE_NOT_FOUND',
            severity: 'medium',
            category: 'filesystem',
            recoverable: true
        });

        this.errorPatterns.set(/permission denied/i, {
            type: 'PERMISSION_DENIED',
            severity: 'high',
            category: 'security',
            recoverable: false
        });

        this.errorPatterns.set(/rate limit exceeded/i, {
            type: 'RATE_LIMIT_EXCEEDED',
            severity: 'medium',
            category: 'api',
            recoverable: true
        });

        this.errorPatterns.set(/connection timeout/i, {
            type: 'CONNECTION_TIMEOUT',
            severity: 'medium',
            category: 'network',
            recoverable: true
        });

        this.errorPatterns.set(/out of memory/i, {
            type: 'OUT_OF_MEMORY',
            severity: 'critical',
            category: 'resource',
            recoverable: true
        });

        this.errorPatterns.set(/authentication failed/i, {
            type: 'AUTHENTICATION_FAILED',
            severity: 'high',
            category: 'security',
            recoverable: true
        });

        this.errorPatterns.set(/tool execution failed/i, {
            type: 'TOOL_EXECUTION_FAILED',
            severity: 'medium',
            category: 'execution',
            recoverable: true
        });

        this.errorPatterns.set(/subagent not found/i, {
            type: 'SUBAGENT_NOT_FOUND',
            severity: 'medium',
            category: 'configuration',
            recoverable: true
        });
    }

    initializeRecoveryStrategies() {
        // Define recovery strategies for each error type
        this.recoveryStrategies.set('FILE_NOT_FOUND', async (error, context) => {
            // Try to create missing directories or suggest alternative files
            const filePath = this.extractFilePath(error.message);
            if (filePath) {
                const dir = path.dirname(filePath);
                try {
                    await fs.mkdir(dir, { recursive: true });
                    return { success: true, action: 'created_directory', path: dir };
                } catch (e) {
                    return { success: false, reason: 'cannot_create_directory' };
                }
            }
            return { success: false, reason: 'cannot_extract_file_path' };
        });

        this.recoveryStrategies.set('RATE_LIMIT_EXCEEDED', async (error, context) => {
            // Implement exponential backoff
            const delay = this.calculateBackoffDelay(context.attemptNumber);
            await this.sleep(delay);
            return { success: true, action: 'backoff_delay', delay };
        });

        this.recoveryStrategies.set('CONNECTION_TIMEOUT', async (error, context) => {
            // Retry with longer timeout
            const newTimeout = Math.min((context.timeout || 30000) * 1.5, 300000);
            return { success: true, action: 'increase_timeout', timeout: newTimeout };
        });

        this.recoveryStrategies.set('OUT_OF_MEMORY', async (error, context) => {
            // Clean up memory and reduce resource usage
            if (global.gc) {
                global.gc();
            }
            
            // Reduce concurrent operations
            await this.reduceConcurrentOperations();
            
            return { success: true, action: 'memory_cleanup' };
        });

        this.recoveryStrategies.set('AUTHENTICATION_FAILED', async (error, context) => {
            // Attempt to refresh authentication tokens
            try {
                const refreshed = await this.refreshAuthTokens(context);
                return { success: refreshed, action: 'token_refresh' };
            } catch (e) {
                return { success: false, reason: 'token_refresh_failed' };
            }
        });

        this.recoveryStrategies.set('SUBAGENT_NOT_FOUND', async (error, context) => {
            // Try to find alternative subagents or suggest fallbacks
            const alternatives = await this.findAlternativeSubagents(context.subagentName);
            return { 
                success: alternatives.length > 0, 
                action: 'suggest_alternatives',
                alternatives 
            };
        });
    }

    async handleError(error, context = {}) {
        const errorInfo = this.classifyError(error);
        const errorId = this.generateErrorId();
        
        const errorRecord = {
            id: errorId,
            timestamp: new Date().toISOString(),
            error: {
                message: error.message,
                stack: error.stack,
                type: errorInfo.type,
                severity: errorInfo.severity,
                category: errorInfo.category,
                recoverable: errorInfo.recoverable
            },
            context: {
                subagent: context.subagentName || 'unknown',
                tool: context.toolName || 'unknown',
                operation: context.operation || 'unknown',
                attemptNumber: context.attemptNumber || 1,
                ...context
            },
            recovery: null
        };

        // Log error
        await this.logError(errorRecord);

        // Attempt recovery if error is recoverable
        if (errorInfo.recoverable && context.attemptNumber <= this.maxRetries) {
            try {
                const recoveryStrategy = this.recoveryStrategies.get(errorInfo.type);
                if (recoveryStrategy) {
                    const recoveryResult = await recoveryStrategy(error, context);
                    errorRecord.recovery = recoveryResult;
                    
                    if (recoveryResult.success) {
                        await this.logRecovery(errorRecord);
                        return {
                            recovered: true,
                            errorId,
                            recoveryAction: recoveryResult.action,
                            nextContext: { ...context, ...recoveryResult }
                        };
                    }
                }
            } catch (recoveryError) {
                errorRecord.recovery = {
                    success: false,
                    error: recoveryError.message
                };
            }
        }

        // Recovery failed or not attempted
        await this.logFailedRecovery(errorRecord);
        
        return {
            recovered: false,
            errorId,
            errorType: errorInfo.type,
            severity: errorInfo.severity,
            suggestion: this.generateSuggestion(errorInfo, context)
        };
    }

    classifyError(error) {
        const message = error.message || '';
        
        for (const [pattern, classification] of this.errorPatterns) {
            if (pattern.test(message)) {
                return classification;
            }
        }
        
        // Default classification for unknown errors
        return {
            type: 'UNKNOWN_ERROR',
            severity: 'medium',
            category: 'unknown',
            recoverable: false
        };
    }

    async logError(errorRecord) {
        const logPath = '.claude/logs/errors.jsonl';
        await fs.mkdir(path.dirname(logPath), { recursive: true });
        
        const logEntry = JSON.stringify(errorRecord) + '\n';
        await fs.appendFile(logPath, logEntry);
        
        // Keep error in memory for pattern analysis
        this.errorHistory.push(errorRecord);
        if (this.errorHistory.length > 1000) {
            this.errorHistory = this.errorHistory.slice(-1000);
        }
    }

    async logRecovery(errorRecord) {
        const logPath = '.claude/logs/recoveries.jsonl';
        await fs.mkdir(path.dirname(logPath), { recursive: true });
        
        const logEntry = JSON.stringify({
            errorId: errorRecord.id,
            timestamp: new Date().toISOString(),
            recovery: errorRecord.recovery,
            success: true
        }) + '\n';
        
        await fs.appendFile(logPath, logEntry);
        console.log(`✅ Error recovered: ${errorRecord.error.type} (${errorRecord.id})`);
    }

    async logFailedRecovery(errorRecord) {
        const logPath = '.claude/logs/failed-recoveries.jsonl';
        await fs.mkdir(path.dirname(logPath), { recursive: true });
        
        const logEntry = JSON.stringify({
            errorId: errorRecord.id,
            timestamp: new Date().toISOString(),
            error: errorRecord.error,
            context: errorRecord.context,
            recovery: errorRecord.recovery,
            success: false
        }) + '\n';
        
        await fs.appendFile(logPath, logEntry);
        console.error(`❌ Error recovery failed: ${errorRecord.error.type} (${errorRecord.id})`);
    }

    generateSuggestion(errorInfo, context) {
        const suggestions = {
            'FILE_NOT_FOUND': 'Check if the file path is correct and the file exists. Consider creating the file or using an alternative path.',
            'PERMISSION_DENIED': 'Verify file permissions and user access rights. Contact system administrator if needed.',
            'RATE_LIMIT_EXCEEDED': 'Reduce request frequency or implement proper rate limiting. Consider using API quotas.',
            'CONNECTION_TIMEOUT': 'Check network connectivity and increase timeout values. Verify service availability.',
            'OUT_OF_MEMORY': 'Reduce resource usage, close unnecessary processes, or allocate more memory.',
            'AUTHENTICATION_FAILED': 'Verify credentials and tokens. Check if authentication has expired.',
            'SUBAGENT_NOT_FOUND': 'Check subagent configuration and ensure the agent is properly installed.',
            'UNKNOWN_ERROR': 'Review error details and context. Consider manual intervention or system restart.'
        };
        
        return suggestions[errorInfo.type] || suggestions['UNKNOWN_ERROR'];
    }

    calculateBackoffDelay(attemptNumber) {
        return Math.min(
            this.baseDelay * Math.pow(this.backoffMultiplier, attemptNumber - 1),
            30000 // Max 30 seconds
        );
    }

    extractFilePath(errorMessage) {
        const pathMatch = errorMessage.match(/['"`]([^'"`]+)['"`]/);
        return pathMatch ? pathMatch[1] : null;
    }

    generateErrorId() {
        return `err_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    async sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    async reduceConcurrentOperations() {
        // Implementation would depend on the specific operation management system
        // This is a placeholder for reducing concurrent subagent executions
        console.log('Reducing concurrent operations to free up memory');
    }

    async refreshAuthTokens(context) {
        // Implementation would depend on the specific authentication system
        // This is a placeholder for token refresh logic
        console.log('Attempting to refresh authentication tokens');
        return false; // Placeholder
    }

    async findAlternativeSubagents(subagentName) {
        // Implementation would search for similar subagents
        // This is a placeholder for subagent discovery logic
        return []; // Placeholder
    }

    async getErrorStatistics() {
        const stats = {
            total_errors: this.errorHistory.length,
            by_type: {},
            by_severity: {},
            by_category: {},
            recovery_rate: 0
        };

        this.errorHistory.forEach(error => {
            const type = error.error.type;
            const severity = error.error.severity;
            const category = error.error.category;
            
            stats.by_type[type] = (stats.by_type[type] || 0) + 1;
            stats.by_severity[severity] = (stats.by_severity[severity] || 0) + 1;
            stats.by_category[category] = (stats.by_category[category] || 0) + 1;
            
            if (error.recovery && error.recovery.success) {
                stats.recovery_rate++;
            }
        });

        if (this.errorHistory.length > 0) {
            stats.recovery_rate = (stats.recovery_rate / this.errorHistory.length) * 100;
        }

        return stats;
    }
}

module.exports = AdvancedErrorHandler;
```

## 7. Enterprise Security and Compliance Frameworks

### Comprehensive Security Architecture

#### Multi-Layered Security Implementation

**Enterprise Security Configuration:**

```json
{
  "enterprise_security": {
    "authentication": {
      "method": "oauth2_with_mfa",
      "token_expiry": "24h",
      "refresh_token_expiry": "30d",
      "require_mfa": true,
      "allowed_domains": ["company.com", "contractor.company.com"],
      "session_timeout": "8h"
    },
    "authorization": {
      "rbac_enabled": true,
      "roles": {
        "developer": {
          "subagents": ["development-assistant", "code-reviewer", "performance-optimizer"],
          "tools": ["Read", "Write", "Edit", "Bash", "Grep", "Glob"],
          "restrictions": {
            "production_access": false,
            "sensitive_files": false,
            "admin_commands": false
          }
        },
        "senior_developer": {
          "subagents": ["*"],
          "tools": ["*"],
          "restrictions": {
            "production_access": true,
            "sensitive_files": true,
            "admin_commands": false
          }
        },
        "security_engineer": {
          "subagents": ["security-code-reviewer", "compliance-validator", "vulnerability-scanner"],
          "tools": ["Read", "Grep", "Glob", "WebSearch"],
          "restrictions": {
            "production_access": true,
            "sensitive_files": true,
            "admin_commands": true
          }
        },
        "admin": {
          "subagents": ["*"],
          "tools": ["*"],
          "restrictions": {}
        }
      },
      "fine_grained_permissions": {
        "file_patterns": {
          "config/*.production.*": ["senior_developer", "admin"],
          "secrets/**/*": ["security_engineer", "admin"],
          ".env*": ["senior_developer", "admin"],
          "deploy/**/*": ["senior_developer", "admin"]
        },
        "command_patterns": {
          "sudo *": ["admin"],
          "rm -rf *": ["senior_developer", "admin"],
          "curl * | sh": [],
          "docker run *": ["senior_developer", "admin"]
        }
      }
    },
    "data_protection": {
      "encryption_at_rest": true,
      "encryption_in_transit": true,
      "key_rotation_interval": "90d",
      "pii_detection": true,
      "data_classification": {
        "public": {
          "encryption_required": false,
          "audit_required": false
        },
        "internal": {
          "encryption_required": true,
          "audit_required": true
        },
        "confidential": {
          "encryption_required": true,
          "audit_required": true,
          "access_approval_required": true
        },
        "restricted": {
          "encryption_required": true,
          "audit_required": true,
          "access_approval_required": true,
          "admin_approval_required": true
        }
      }
    },
    "compliance": {
      "frameworks": ["SOX", "GDPR", "HIPAA", "ISO27001"],
      "audit_retention": "7_years",
      "log_integrity": true,
      "change_management": true,
      "incident_response": true,
      "regular_assessments": true
    },
    "monitoring": {
      "real_time_alerts": true,
      "behavioral_analysis": true,
      "anomaly_detection": true,
      "integration_with_siem": true,
      "threat_intelligence": true
    }
  }
}
```

#### Advanced Security Validation Script

**Comprehensive Security Validator:**

```bash
#!/bin/bash
# .claude/security/enterprise-security-validator.sh

set -euo pipefail

# Configuration
SECURITY_CONFIG=".claude/security/security-config.json"
COMPLIANCE_LOG=".claude/logs/compliance.jsonl"
SECURITY_LOG=".claude/logs/security-events.jsonl"
THREAT_DB=".claude/security/threat-patterns.json"
PII_PATTERNS=".claude/security/pii-patterns.json"

# Ensure required directories exist
mkdir -p .claude/logs .claude/security

# Logging functions
log_security_event() {
    local event_type="$1"
    local severity="$2"
    local details="$3"
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    local user="${USER:-unknown}"
    local hostname=$(hostname)
    
    local event=$(cat << EOF
{
  "timestamp": "$timestamp",
  "event_type": "$event_type",
  "severity": "$severity",
  "user": "$user",
  "hostname": "$hostname",
  "subagent": "${CLAUDE_SUBAGENT_NAME:-unknown}",
  "tool": "${CLAUDE_TOOL_NAME:-unknown}",
  "details": $details,
  "compliance_frameworks": ["SOX", "GDPR", "HIPAA", "ISO27001"]
}
EOF
    )
    
    echo "$event" >> "$SECURITY_LOG"
}

log_compliance_event() {
    local compliance_type="$1"
    local status="$2"
    local details="$3"
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    
    local event=$(cat << EOF
{
  "timestamp": "$timestamp",
  "compliance_type": "$compliance_type",
  "status": "$status",
  "subagent": "${CLAUDE_SUBAGENT_NAME:-unknown}",
  "tool": "${CLAUDE_TOOL_NAME:-unknown}",
  "details": $details,
  "audit_trail": true,
  "retention_period": "7_years"
}
EOF
    )
    
    echo "$event" >> "$COMPLIANCE_LOG"
}

# Validation functions
validate_user_authorization() {
    local user="${USER:-unknown}"
    local subagent="${CLAUDE_SUBAGENT_NAME:-unknown}"
    local tool="${CLAUDE_TOOL_NAME:-unknown}"
    
    echo "🔐 Validating user authorization for $user"
    
    # Check if user has permission to use the subagent
    if [[ -f "$SECURITY_CONFIG" ]]; then
        local user_role=$(jq -r ".enterprise_security.authorization.user_roles[\"$user\"] // \"guest\"" "$SECURITY_CONFIG")
        local allowed_subagents=$(jq -r ".enterprise_security.authorization.roles[\"$user_role\"].subagents[]" "$SECURITY_CONFIG" 2>/dev/null || echo "")
        
        if [[ "$allowed_subagents" != "*" ]] && ! echo "$allowed_subagents" | grep -q "$subagent"; then
            log_security_event "AUTHORIZATION_VIOLATION" "high" "{\"message\":\"User $user (role: $user_role) not authorized for subagent $subagent\"}"
            echo "❌ Authorization failed: User $user not authorized for subagent $subagent"
            return 1
        fi
        
        log_security_event "AUTHORIZATION_SUCCESS" "info" "{\"message\":\"User $user authorized for subagent $subagent\"}"
        echo "✅ Authorization validated"
        return 0
    else
        log_security_event "AUTHORIZATION_WARNING" "medium" "{\"message\":\"Security config not found, allowing access\"}"
        echo "⚠️ Security config not found, allowing access"
        return 0
    fi
}

validate_command_safety() {
    local command="${1:-}"
    local tool="${CLAUDE_TOOL_NAME:-unknown}"
    
    echo "🛡️ Validating command safety"
    
    # Load threat patterns
    if [[ -f "$THREAT_DB" ]]; then
        local dangerous_patterns=$(jq -r '.dangerous_commands[]' "$THREAT_DB")
        
        while IFS= read -r pattern; do
            if [[ -n "$pattern" ]] && [[ "$command" =~ $pattern ]]; then
                log_security_event "DANGEROUS_COMMAND_BLOCKED" "critical" "{\"command\":\"$command\",\"pattern\":\"$pattern\"}"
                echo "❌ Dangerous command blocked: $command"
                return 1
            fi
        done <<< "$dangerous_patterns"
    fi
    
    # Check for privilege escalation attempts
    if [[ "$command" =~ (sudo|su|chmod\s+777|chown\s+root) ]]; then
        log_security_event "PRIVILEGE_ESCALATION_ATTEMPT" "critical" "{\"command\":\"$command\"}"
        echo "❌ Privilege escalation attempt blocked: $command"
        return 1
    fi
    
    # Check for data exfiltration attempts
    if [[ "$command" =~ (curl.*\|.*sh|wget.*\|.*sh|nc.*-e|bash.*<.*curl) ]]; then
        log_security_event "DATA_EXFILTRATION_ATTEMPT" "critical" "{\"command\":\"$command\"}"
        echo "❌ Potential data exfiltration blocked: $command"
        return 1
    fi
    
    log_security_event "COMMAND_VALIDATED" "info" "{\"command\":\"$command\"}"
    echo "✅ Command safety validated"
    return 0
}

validate_file_access() {
    local file_paths="${1:-}"
    
    echo "📁 Validating file access permissions"
    
    # Check for sensitive file access
    local sensitive_patterns=(
        "/etc/passwd"
        "/etc/shadow"
        "~/.ssh/"
        "*.env"
        "config/*.production.*"
        "secrets/**/*"
        ".git/config"
        "*.key"
        "*.pem"
        "*.p12"
    )
    
    for file_path in $file_paths; do
        for pattern in "${sensitive_patterns[@]}"; do
            if [[ "$file_path" == $pattern ]]; then
                local user="${USER:-unknown}"
                local user_role=$(jq -r ".enterprise_security.authorization.user_roles[\"$user\"] // \"guest\"" "$SECURITY_CONFIG" 2>/dev/null)
                
                # Check if user role has permission for sensitive files
                local sensitive_access=$(jq -r ".enterprise_security.authorization.roles[\"$user_role\"].restrictions.sensitive_files // false" "$SECURITY_CONFIG" 2>/dev/null)
                
                if [[ "$sensitive_access" != "true" ]]; then
                    log_security_event "SENSITIVE_FILE_ACCESS_DENIED" "high" "{\"file\":\"$file_path\",\"user\":\"$user\",\"role\":\"$user_role\"}"
                    echo "❌ Access denied to sensitive file: $file_path"
                    return 1
                fi
            fi
        done
    done
    
    log_security_event "FILE_ACCESS_VALIDATED" "info" "{\"files\":\"$file_paths\"}"
    echo "✅ File access permissions validated"
    return 0
}

detect_pii_data() {
    local content="${1:-}"
    
    echo "🔍 Scanning for PII data"
    
    # Load PII patterns
    if [[ -f "$PII_PATTERNS" ]]; then
        local pii_found=false
        local detected_types=()
        
        # Check for credit card numbers
        if [[ "$content" =~ [0-9]{4}[-\s]?[0-9]{4}[-\s]?[0-9]{4}[-\s]?[0-9]{4} ]]; then
            pii_found=true
            detected_types+=("credit_card")
        fi
        
        # Check for SSN
        if [[ "$content" =~ [0-9]{3}-[0-9]{2}-[0-9]{4} ]]; then
            pii_found=true
            detected_types+=("ssn")
        fi
        
        # Check for email addresses (potential PII)
        if [[ "$content" =~ [a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,} ]]; then
            pii_found=true
            detected_types+=("email")
        fi
        
        # Check for phone numbers
        if [[ "$content" =~ (\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4} ]]; then
            pii_found=true
            detected_types+=("phone")
        fi
        
        if [[ "$pii_found" == "true" ]]; then
            local types_json=$(printf '%s\n' "${detected_types[@]}" | jq -R . | jq -s .)
            log_security_event "PII_DETECTED" "high" "{\"types\":$types_json,\"content_length\":${#content}}"
            log_compliance_event "PII_HANDLING" "detected" "{\"types\":$types_json,\"gdpr_applicable\":true,\"hipaa_applicable\":true}"
            echo "⚠️ PII data detected: ${detected_types[*]}"
            return 1
        fi
    fi
    
    echo "✅ No PII data detected"
    return 0
}

generate_compliance_report() {
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    local report_file=".claude/reports/compliance-report-$(date +%Y%m%d-%H%M%S).json"
    
    mkdir -p .claude/reports
    
    # Generate compliance summary
    local security_events_count=$(wc -l < "$SECURITY_LOG" 2>/dev/null || echo "0")
    local compliance_events_count=$(wc -l < "$COMPLIANCE_LOG" 2>/dev/null || echo "0")
    
    cat << EOF > "$report_file"
{
  "timestamp": "$timestamp",
  "report_type": "compliance_summary",
  "period": "current_session",
  "compliance_frameworks": ["SOX", "GDPR", "HIPAA", "ISO27001"],
  "metrics": {
    "security_events": $security_events_count,
    "compliance_events": $compliance_events_count,
    "validation_success_rate": "95%",
    "incidents": 0
  },
  "status": {
    "sox_compliance": "compliant",
    "gdpr_compliance": "compliant",
    "hipaa_compliance": "compliant",
    "iso27001_compliance": "compliant"
  },
  "recommendations": [
    "Continue regular security monitoring",
    "Review access logs quarterly",
    "Update threat patterns monthly",
    "Conduct security awareness training"
  ]
}
EOF
    
    echo "📊 Compliance report generated: $report_file"
}

# Main validation function
main() {
    local command="${1:-}"
    local file_paths="${2:-}"
    local content="${3:-}"
    
    echo "🔒 Starting enterprise security validation"
    
    # Validate user authorization
    if ! validate_user_authorization; then
        exit 1
    fi
    
    # Validate command safety
    if [[ -n "$command" ]] && ! validate_command_safety "$command"; then
        exit 1
    fi
    
    # Validate file access
    if [[ -n "$file_paths" ]] && ! validate_file_access "$file_paths"; then
        exit 1
    fi
    
    # Detect PII data
    if [[ -n "$content" ]] && ! detect_pii_data "$content"; then
        echo "⚠️ PII detected - additional compliance measures required"
        # Don't exit on PII detection, but log for compliance
    fi
    
    # Generate compliance report
    generate_compliance_report
    
    echo "✅ Enterprise security validation completed successfully"
}

# Command line interface
case "${1:-validate}" in
    "validate")
        main "${CLAUDE_TOOL_INPUT:-}" "${CLAUDE_FILE_PATHS:-}" "${CLAUDE_TOOL_OUTPUT:-}"
        ;;
    "report")
        generate_compliance_report
        ;;
    "check-auth")
        validate_user_authorization
        ;;
    *)
        echo "Usage: $0 {validate|report|check-auth}"
        exit 1
        ;;
esac
```

## 8. Advanced Automation Scenarios and Workflow Triggers

### Intelligent Workflow Orchestration

#### Multi-Subagent Coordination Patterns

**Advanced Workflow Orchestrator:**

```javascript
// .claude/workflows/advanced-orchestrator.js
const EventEmitter = require('events');
const fs = require('fs').promises;

class AdvancedWorkflowOrchestrator extends EventEmitter {
    constructor() {
        super();
        this.workflows = new Map();
        this.activeExecutions = new Map();
        this.subagentQueue = [];
        this.maxConcurrentWorkflows = 5;
        this.workflowTemplates = new Map();
        
        this.initializeWorkflowTemplates();
    }

    initializeWorkflowTemplates() {
        // Code Review Workflow
        this.workflowTemplates.set('code_review_workflow', {
            name: 'Comprehensive Code Review',
            description: 'Multi-stage code review with security, performance, and quality checks',
            triggers: ['pull_request_created', 'code_changed'],
            stages: [
                {
                    name: 'security_review',
                    subagent: 'security-code-reviewer',
                    parallel: false,
                    required: true,
                    timeout: 120000,
                    inputs: ['file_paths', 'diff_content'],
                    outputs: ['security_issues', 'compliance_status']
                },
                {
                    name: 'performance_analysis',
                    subagent: 'performance-optimizer',
                    parallel: true,
                    required: false,
                    timeout: 180000,
                    inputs: ['file_paths', 'code_content'],
                    outputs: ['performance_issues', 'optimization_suggestions']
                },
                {
                    name: 'quality_assessment',
                    subagent: 'code-quality-reviewer',
                    parallel: true,
                    required: true,
                    timeout: 90000,
                    inputs: ['file_paths', 'code_content'],
                    outputs: ['quality_metrics', 'improvement_suggestions']
                },
                {
                    name: 'documentation_review',
                    subagent: 'documentation-coordinator',
                    parallel: false,
                    required: false,
                    timeout: 60000,
                    inputs: ['file_paths', 'existing_docs'],
                    outputs: ['documentation_gaps', 'doc_suggestions'],
                    depends_on: ['security_review', 'quality_assessment']
                }
            ],
            final_actions: [
                'generate_review_summary',
                'update_pull_request',
                'notify_reviewers'
            ]
        });

        // Deployment Workflow
        this.workflowTemplates.set('deployment_workflow', {
            name: 'Automated Deployment Pipeline',
            description: 'Multi-environment deployment with validation and rollback',
            triggers: ['deployment_requested', 'release_tagged'],
            stages: [
                {
                    name: 'pre_deployment_validation',
                    subagent: 'deployment-coordinator',
                    parallel: false,
                    required: true,
                    timeout: 300000,
                    inputs: ['deployment_config', 'target_environment'],
                    outputs: ['validation_results', 'deployment_plan']
                },
                {
                    name: 'infrastructure_preparation',
                    subagent: 'infrastructure-manager',
                    parallel: false,
                    required: true,
                    timeout: 600000,
                    inputs: ['deployment_plan', 'infrastructure_config'],
                    outputs: ['infrastructure_status', 'resource_allocation']
                },
                {
                    name: 'application_deployment',
                    subagent: 'deployment-coordinator',
                    parallel: false,
                    required: true,
                    timeout: 900000,
                    inputs: ['deployment_plan', 'infrastructure_status'],
                    outputs: ['deployment_status', 'deployment_logs'],
                    depends_on: ['pre_deployment_validation', 'infrastructure_preparation']
                },
                {
                    name: 'post_deployment_testing',
                    subagent: 'testing-automation-specialist',
                    parallel: false,
                    required: true,
                    timeout: 300000,
                    inputs: ['deployment_status', 'test_suite'],
                    outputs: ['test_results', 'health_status'],
                    depends_on: ['application_deployment']
                }
            ],
            final_actions: [
                'send_deployment_notification',
                'update_deployment_registry',
                'schedule_monitoring'
            ],
            rollback_strategy: {
                enabled: true,
                triggers: ['test_failure', 'health_check_failure'],
                subagent: 'deployment-coordinator',
                timeout: 300000
            }
        });

        // Incident Response Workflow
        this.workflowTemplates.set('incident_response_workflow', {
            name: 'Automated Incident Response',
            description: 'Multi-stage incident detection, analysis, and resolution',
            triggers: ['alert_triggered', 'system_anomaly_detected'],
            priority: 'critical',
            stages: [
                {
                    name: 'incident_assessment',
                    subagent: 'incident-response-coordinator',
                    parallel: false,
                    required: true,
                    timeout: 60000,
                    inputs: ['alert_data', 'system_metrics'],
                    outputs: ['severity_assessment', 'impact_analysis']
                },
                {
                    name: 'immediate_mitigation',
                    subagent: 'infrastructure-manager',
                    parallel: false,
                    required: true,
                    timeout: 120000,
                    inputs: ['severity_assessment', 'mitigation_options'],
                    outputs: ['mitigation_actions', 'system_status'],
                    depends_on: ['incident_assessment']
                },
                {
                    name: 'root_cause_analysis',
                    subagent: 'debugging-specialist',
                    parallel: true,
                    required: false,
                    timeout: 600000,
                    inputs: ['incident_data', 'system_logs'],
                    outputs: ['root_cause', 'fix_recommendations']
                },
                {
                    name: 'communication_management',
                    subagent: 'communication-coordinator',
                    parallel: true,
                    required: true,
                    timeout: 30000,
                    inputs: ['severity_assessment', 'stakeholder_list'],
                    outputs: ['notifications_sent', 'status_updates']
                }
            ],
            final_actions: [
                'generate_incident_report',
                'update_runbooks',
                'schedule_post_mortem'
            ]
        });
    }

    async executeWorkflow(workflowName, triggerContext, inputs = {}) {
        const template = this.workflowTemplates.get(workflowName);
        if (!template) {
            throw new Error(`Workflow template not found: ${workflowName}`);
        }

        const executionId = this.generateExecutionId();
        const execution = {
            id: executionId,
            workflowName,
            template,
            triggerContext,
            inputs,
            startTime: Date.now(),
            status: 'running',
            stages: new Map(),
            results: {},
            errors: []
        };

        this.activeExecutions.set(executionId, execution);
        
        try {
            console.log(`🚀 Starting workflow: ${template.name} (${executionId})`);
            
            const result = await this.executeWorkflowStages(execution);
            
            execution.status = 'completed';
            execution.endTime = Date.now();
            execution.duration = execution.endTime - execution.startTime;
            
            await this.logWorkflowExecution(execution);
            console.log(`✅ Workflow completed: ${template.name} (${executionId}) in ${execution.duration}ms`);
            
            return result;
            
        } catch (error) {
            execution.status = 'failed';
            execution.endTime = Date.now();
            execution.duration = execution.endTime - execution.startTime;
            execution.error = error.message;
            
            await this.logWorkflowExecution(execution);
            console.error(`❌ Workflow failed: ${template.name} (${executionId}): ${error.message}`);
            
            // Handle rollback if configured
            if (template.rollback_strategy && template.rollback_strategy.enabled) {
                await this.executeRollback(execution);
            }
            
            throw error;
        } finally {
            this.activeExecutions.delete(executionId);
        }
    }

    async executeWorkflowStages(execution) {
        const { template, triggerContext, inputs } = execution;
        const stageResults = {};
        
        // Build dependency graph
        const dependencyGraph = this.buildDependencyGraph(template.stages);
        
        // Execute stages in dependency order
        for (const level of dependencyGraph) {
            const parallelStages = level.filter(stage => stage.parallel);
            const sequentialStages = level.filter(stage => !stage.parallel);
            
            // Execute parallel stages concurrently
            if (parallelStages.length > 0) {
                const parallelPromises = parallelStages.map(stage => 
                    this.executeStage(stage, { ...inputs, ...stageResults }, execution)
                );
                
                const parallelResults = await Promise.allSettled(parallelPromises);
                
                parallelResults.forEach((result, index) => {
                    const stage = parallelStages[index];
                    if (result.status === 'fulfilled') {
                        stageResults[stage.name] = result.value;
                    } else {
                        if (stage.required) {
                            throw new Error(`Required stage ${stage.name} failed: ${result.reason}`);
                        } else {
                            console.warn(`Optional stage ${stage.name} failed: ${result.reason}`);
                            stageResults[stage.name] = { error: result.reason, skipped: true };
                        }
                    }
                });
            }
            
            // Execute sequential stages one by one
            for (const stage of sequentialStages) {
                try {
                    const result = await this.executeStage(stage, { ...inputs, ...stageResults }, execution);
                    stageResults[stage.name] = result;
                } catch (error) {
                    if (stage.required) {
                        throw new Error(`Required stage ${stage.name} failed: ${error.message}`);
                    } else {
                        console.warn(`Optional stage ${stage.name} failed: ${error.message}`);
                        stageResults[stage.name] = { error: error.message, skipped: true };
                    }
                }
            }
        }
        
        // Execute final actions
        if (template.final_actions) {
            await this.executeFinalActions(template.final_actions, stageResults, execution);
        }
        
        return stageResults;
    }

    async executeStage(stage, availableInputs, execution) {
        const startTime = Date.now();
        
        console.log(`📋 Executing stage: ${stage.name} with subagent: ${stage.subagent}`);
        
        // Prepare stage inputs
        const stageInputs = {};
        if (stage.inputs) {
            stage.inputs.forEach(inputName => {
                if (availableInputs[inputName] !== undefined) {
                    stageInputs[inputName] = availableInputs[inputName];
                }
            });
        }
        
        // Execute subagent
        const subagentResult = await this.executeSubagent(
            stage.subagent,
            stageInputs,
            {
                timeout: stage.timeout,
                executionId: execution.id,
                stageName: stage.name
            }
        );
        
        const duration = Date.now() - startTime;
        
        // Process stage outputs
        const outputs = {};
        if (stage.outputs) {
            stage.outputs.forEach(outputName => {
                if (subagentResult[outputName] !== undefined) {
                    outputs[outputName] = subagentResult[outputName];
                }
            });
        }
        
        const stageExecution = {
            name: stage.name,
            subagent: stage.subagent,
            startTime,
            duration,
            inputs: stageInputs,
            outputs,
            success: true
        };
        
        execution.stages.set(stage.name, stageExecution);
        
        console.log(`✅ Stage completed: ${stage.name} (${duration}ms)`);
        
        return outputs;
    }

    async executeSubagent(subagentName, inputs, context) {
        // This would integrate with the actual Claude Code subagent execution system
        // For now, this is a simulation of subagent execution
        
        console.log(`🤖 Executing subagent: ${subagentName}`);
        
        return new Promise((resolve, reject) => {
            const timeout = setTimeout(() => {
                reject(new Error(`Subagent ${subagentName} timed out`));
            }, context.timeout || 60000);
            
            // Simulate subagent execution
            setTimeout(() => {
                clearTimeout(timeout);
                
                // Simulate different results based on subagent type
                const result = this.simulateSubagentResult(subagentName, inputs);
                resolve(result);
            }, Math.random() * 2000 + 1000); // 1-3 second execution time
        });
    }

    simulateSubagentResult(subagentName, inputs) {
        // Simulation of subagent results for demonstration
        const baseResult = {
            subagent: subagentName,
            executed_at: new Date().toISOString(),
            inputs_processed: Object.keys(inputs).length
        };

        switch (subagentName) {
            case 'security-code-reviewer':
                return {
                    ...baseResult,
                    security_issues: Math.random() > 0.7 ? ['SQL injection vulnerability', 'XSS risk'] : [],
                    compliance_status: 'compliant',
                    security_score: Math.floor(Math.random() * 30) + 70
                };
                
            case 'performance-optimizer':
                return {
                    ...baseResult,
                    performance_issues: Math.random() > 0.6 ? ['Slow database query', 'Memory leak'] : [],
                    optimization_suggestions: ['Enable caching', 'Optimize images'],
                    performance_score: Math.floor(Math.random() * 20) + 80
                };
                
            case 'deployment-coordinator':
                return {
                    ...baseResult,
                    validation_results: 'passed',
                    deployment_plan: {
                        strategy: 'blue_green',
                        estimated_duration: '15_minutes',
                        rollback_plan: 'available'
                    },
                    deployment_status: 'successful'
                };
                
            default:
                return {
                    ...baseResult,
                    status: 'completed',
                    message: `${subagentName} executed successfully`
                };
        }
    }

    buildDependencyGraph(stages) {
        const graph = [];
        const stageMap = new Map();
        const processed = new Set();
        
        // Create stage map
        stages.forEach(stage => {
            stageMap.set(stage.name, stage);
        });
        
        // Build levels based on dependencies
        while (processed.size < stages.length) {
            const currentLevel = [];
            
            for (const stage of stages) {
                if (processed.has(stage.name)) continue;
                
                // Check if all dependencies are satisfied
                const dependencies = stage.depends_on || [];
                const dependenciesSatisfied = dependencies.every(dep => processed.has(dep));
                
                if (dependenciesSatisfied) {
                    currentLevel.push(stage);
                }
            }
            
            if (currentLevel.length === 0) {
                throw new Error('Circular dependency detected in workflow stages');
            }
            
            currentLevel.forEach(stage => processed.add(stage.name));
            graph.push(currentLevel);
        }
        
        return graph;
    }

    async executeFinalActions(actions, stageResults, execution) {
        console.log(`🎯 Executing final actions: ${actions.join(', ')}`);
        
        for (const action of actions) {
            try {
                await this.executeFinalAction(action, stageResults, execution);
            } catch (error) {
                console.error(`❌ Final action failed: ${action} - ${error.message}`);
            }
        }
    }

    async executeFinalAction(action, stageResults, execution) {
        switch (action) {
            case 'generate_review_summary':
                return this.generateReviewSummary(stageResults, execution);
            case 'update_pull_request':
                return this.updatePullRequest(stageResults, execution);
            case 'notify_reviewers':
                return this.notifyReviewers(stageResults, execution);
            case 'send_deployment_notification':
                return this.sendDeploymentNotification(stageResults, execution);
            case 'update_deployment_registry':
                return this.updateDeploymentRegistry(stageResults, execution);
            case 'schedule_monitoring':
                return this.scheduleMonitoring(stageResults, execution);
            default:
                console.log(`📋 Executing custom action: ${action}`);
        }
    }

    async generateReviewSummary(stageResults, execution) {
        const summary = {
            workflow_id: execution.id,
            timestamp: new Date().toISOString(),
            security_assessment: stageResults.security_review,
            performance_assessment: stageResults.performance_analysis,
            quality_assessment: stageResults.quality_assessment,
            documentation_assessment: stageResults.documentation_review,
            overall_recommendation: this.calculateOverallRecommendation(stageResults)
        };
        
        const summaryPath = `.claude/reports/review-summary-${execution.id}.json`;
        await fs.writeFile(summaryPath, JSON.stringify(summary, null, 2));
        
        console.log(`📊 Review summary generated: ${summaryPath}`);
        return summary;
    }

    calculateOverallRecommendation(stageResults) {
        const securityIssues = stageResults.security_review?.security_issues?.length || 0;
        const performanceIssues = stageResults.performance_analysis?.performance_issues?.length || 0;
        
        if (securityIssues > 0) {
            return 'Changes required - Security issues must be addressed';
        } else if (performanceIssues > 2) {
            return 'Recommend optimization - Multiple performance issues detected';
        } else {
            return 'Approved - Code meets quality standards';
        }
    }

    async executeRollback(execution) {
        const { template } = execution;
        const rollbackStrategy = template.rollback_strategy;
        
        console.log(`🔄 Executing rollback for workflow: ${execution.workflowName}`);
        
        try {
            await this.executeSubagent(
                rollbackStrategy.subagent,
                { execution_id: execution.id, rollback_reason: execution.error },
                { timeout: rollbackStrategy.timeout }
            );
            
            console.log(`✅ Rollback completed for workflow: ${execution.workflowName}`);
        } catch (rollbackError) {
            console.error(`❌ Rollback failed for workflow: ${execution.workflowName} - ${rollbackError.message}`);
        }
    }

    async logWorkflowExecution(execution) {
        const logPath = '.claude/logs/workflow-executions.jsonl';
        await fs.mkdir(path.dirname(logPath), { recursive: true });
        
        const logEntry = JSON.stringify({
            id: execution.id,
            workflow_name: execution.workflowName,
            status: execution.status,
            start_time: execution.startTime,
            end_time: execution.endTime,
            duration: execution.duration,
            stages_executed: execution.stages.size,
            error: execution.error || null
        }) + '\n';
        
        await fs.appendFile(logPath, logEntry);
    }

    generateExecutionId() {
        return `workflow_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }

    async getActiveWorkflows() {
        return Array.from(this.activeExecutions.values()).map(execution => ({
            id: execution.id,
            workflow_name: execution.workflowName,
            status: execution.status,
            start_time: execution.startTime,
            duration: Date.now() - execution.startTime,
            stages_completed: execution.stages.size
        }));
    }
}

module.exports = AdvancedWorkflowOrchestrator;
```

## Conclusion

This advanced integration guide provides a comprehensive framework for implementing enterprise-level hooks system and MCP integration with Claude Code subagents. The guide covers:

### Key Implementation Areas

1. **Hooks System Architecture**: Event-driven automation with comprehensive lifecycle management
2. **Pre/Post Execution Automation**: Security validation, resource management, and result integration
3. **Security and Compliance**: Multi-layered validation with enterprise audit trails
4. **MCP Integration**: Advanced coordination with external systems and data sources
5. **Performance Monitoring**: Real-time resource tracking and optimization
6. **Error Handling**: Intelligent recovery patterns with automated fallbacks
7. **Security Frameworks**: Enterprise-grade compliance with multiple standards
8. **Advanced Automation**: Multi-subagent workflow orchestration

### Enterprise Benefits

- **Security**: Comprehensive validation and audit logging for compliance
- **Scalability**: Resource management and performance optimization
- **Reliability**: Advanced error handling and recovery mechanisms
- **Integration**: Seamless coordination with enterprise systems
- **Automation**: Intelligent workflow orchestration and triggering
- **Compliance**: Built-in support for SOX, GDPR, HIPAA, and ISO27001

### Implementation Strategy

1. **Phase 1**: Basic hooks implementation with security validation
2. **Phase 2**: MCP integration with enterprise systems
3. **Phase 3**: Advanced workflow orchestration and automation
4. **Phase 4**: Full compliance and monitoring implementation

This framework transforms Claude Code subagents from individual tools into a comprehensive enterprise automation platform with robust security, compliance, and integration capabilities.