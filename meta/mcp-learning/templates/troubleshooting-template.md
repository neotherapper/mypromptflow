# [MCP Server Name] Troubleshooting Guide

## Quick Problem Identification

### 1. Error Category Classification
**Step 1:** Identify the error type by checking the error message:

- **Authentication Errors:** Contains "auth", "token", "permission", "unauthorized"
- **Parameter Errors:** Contains "parameter", "required", "invalid", "missing"
- **API Errors:** Contains "rate limit", "unavailable", "not found", "timeout"
- **Network Errors:** Contains "connection", "network", "DNS", "SSL"

### 2. Immediate Checks
Before deep troubleshooting, verify:
- [ ] **Recent Changes:** Did I modify parameters since last success?
- [ ] **Authentication Status:** Are credentials still valid?
- [ ] **Service Status:** Is the external service operational?
- [ ] **Rate Limits:** Did I exceed usage quotas?

## Systematic Diagnosis

### Authentication Issues
**Symptoms:** 401, 403, "unauthorized", "invalid token"

**Diagnosis Steps:**
1. **Check credentials existence:**
   ```bash
   # Verify environment variables or config files
   echo $[AUTH_VAR_NAME]
   ```

2. **Validate credential format:**
   - API keys: Usually alphanumeric strings
   - Tokens: Often JWT format or bearer tokens
   - Basic auth: Username:password base64 encoded

3. **Test credential freshness:**
   - Check expiration dates
   - Verify against service directly if possible

**Resolution:**
- [ ] Refresh expired credentials
- [ ] Update environment variables
- [ ] Verify correct credential type for service

### Parameter Issues  
**Symptoms:** "parameter", "required field", "invalid format"

**Diagnosis Steps:**
1. **Check required parameters:**
   - Compare against usage guide requirements
   - Verify all mandatory fields present

2. **Validate parameter formats:**
   - JSON structure for objects
   - String formats (dates, IDs, etc.)
   - Data types (string vs number vs boolean)

3. **Test parameter values:**
   - Check for typos in IDs or names
   - Verify enum values are valid
   - Ensure numerical ranges are appropriate

**Resolution:**
- [ ] Add missing required parameters
- [ ] Fix format issues (JSON structure, data types)
- [ ] Validate parameter values against service requirements

### API Issues
**Symptoms:** 429 (rate limit), 503 (unavailable), timeouts

**Diagnosis Steps:**
1. **Check service status:**
   - Verify external service health
   - Look for maintenance windows
   - Check service status pages

2. **Analyze usage patterns:**
   - Review recent request frequency
   - Check for rate limit headers in responses
   - Verify quota consumption

3. **Test connectivity:**
   - Simple ping or health check
   - Verify DNS resolution
   - Check network path

**Resolution:**
- [ ] Implement backoff/retry strategy for rate limits
- [ ] Wait for service restoration
- [ ] Switch to alternative endpoints if available

## Step-by-Step Resolution Process

### Phase 1: Quick Fixes (2 minutes)
1. **Retry with exact same parameters** (transient issue check)
2. **Check for typos** in parameters
3. **Verify credentials** are present and formatted correctly
4. **Review error message** for specific guidance

### Phase 2: Parameter Validation (5 minutes)
1. **Cross-reference usage guide** for parameter requirements
2. **Validate JSON structure** if using complex objects
3. **Check data types** match expectations
4. **Verify required fields** are all present

### Phase 3: Deep Diagnosis (10 minutes)
1. **Check service documentation** for API changes
2. **Review error logs** for similar past issues
3. **Test minimal case** with simplest possible parameters
4. **Compare with known working examples**

### Phase 4: Pattern Analysis (15 minutes)
1. **Search common error patterns** in `@meta/mcp-learning/patterns/`
2. **Review recent error log entries** for this server
3. **Check for authentication/token refresh needs**
4. **Analyze parameter validation patterns**

## Common Resolution Strategies

### Strategy 1: Parameter Simplification
**When:** Complex parameters failing
**Approach:**
1. Start with minimal required parameters only
2. Add optional parameters one at a time
3. Test after each addition
4. Identify problematic parameter

### Strategy 2: Authentication Refresh
**When:** Auth-related errors
**Approach:**
1. Verify current credentials
2. Refresh tokens if applicable
3. Test with fresh authentication
4. Update stored credentials

### Strategy 3: API Version Check
**When:** Sudden failures after working
**Approach:**
1. Check for API deprecations
2. Review service changelog
3. Update parameter formats if needed
4. Adjust endpoints if required

### Strategy 4: Gradual Rollback
**When:** Recent changes broke functionality
**Approach:**
1. Identify last working configuration
2. Compare current vs working parameters
3. Revert problematic changes
4. Test incremental modifications

## Prevention Strategies

### Before Every MCP Tool Use:
- [ ] **Check usage guide** for current best practices
- [ ] **Validate parameters** against known working patterns
- [ ] **Verify authentication** status and freshness
- [ ] **Review recent error log** for new patterns

### After Successful Operations:
- [ ] **Document working parameters** in usage guide
- [ ] **Note any parameter variations** that work
- [ ] **Update success patterns** for future reference
- [ ] **Record authentication requirements** used

## Escalation Path

### Level 1: Self-Resolution (15 minutes)
- Follow this troubleshooting guide
- Check error logs and usage guides
- Try common resolution strategies

### Level 2: Pattern Analysis (30 minutes)
- Deep dive into error patterns
- Cross-reference with similar servers
- Analyze parameter validation rules
- Research service documentation

### Level 3: Documentation Update (45 minutes)
- Update error log with detailed findings
- Enhance usage guide with new patterns
- Create prevention strategies
- Share learning with system

### Level 4: System Learning (60 minutes)
- Analyze across all MCP servers for patterns
- Update common error patterns
- Enhance parameter validation
- Improve troubleshooting procedures

## Success Metrics

**Resolution Time:** Target < 15 minutes for known patterns
**Prevention Rate:** Reduce repeat errors by 90%
**Pattern Recognition:** Identify root cause within 5 minutes
**Knowledge Transfer:** Update guides within 10 minutes of resolution

## Template Usage Notes

1. **Copy this template** for each MCP server
2. **Customize sections** based on server-specific patterns
3. **Update regularly** based on new error patterns
4. **Cross-reference** with error logs and usage guides
5. **Maintain** success metrics for continuous improvement