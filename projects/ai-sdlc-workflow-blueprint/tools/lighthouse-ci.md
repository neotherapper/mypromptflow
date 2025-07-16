# Lighthouse CI - Web Performance Monitoring

## Overview

Lighthouse CI is an open-source tool that automates running Google Lighthouse performance audits for every commit, tracking performance metrics over time and preventing regressions. It provides continuous monitoring of Core Web Vitals, accessibility, best practices, and SEO scores.

### Key Benefits

- **Automated Performance Testing**: Run Lighthouse audits on every commit
- **Historical Tracking**: Monitor performance trends over time
- **Performance Budgets**: Set thresholds and fail builds on regressions
- **Core Web Vitals Monitoring**: Track LCP, FID, CLS metrics
- **Detailed Reports**: Rich HTML reports with actionable insights
- **GitHub Integration**: Comments on PRs with performance impacts
- **Free and Open Source**: No licensing costs
- **Self-Hosted or Cloud**: Flexible deployment options

## Core Features

### 1. Performance Metrics Tracking

```yaml
# lighthouserc.yml
ci:
  collect:
    # Maritime insurance app URLs to audit
    url:
      - http://localhost:3000/
      - http://localhost:3000/policies
      - http://localhost:3000/claims
      - http://localhost:3000/risk-assessment
    numberOfRuns: 3
    settings:
      # Desktop and mobile configurations
      preset: 'desktop'
      throttling:
        cpuSlowdownMultiplier: 1
      screenEmulation:
        disabled: true
  assert:
    # Performance budgets
    preset: 'lighthouse:no-pwa'
    assertions:
      # Core Web Vitals
      largest-contentful-paint:
        - error
        - maxNumericValue: 2500
          aggregationMethod: optimistic
      first-contentful-paint:
        - error
        - maxNumericValue: 1800
          aggregationMethod: optimistic
      cumulative-layout-shift:
        - error
        - maxNumericValue: 0.1
          aggregationMethod: optimistic
      total-blocking-time:
        - error
        - maxNumericValue: 300
          aggregationMethod: optimistic
      # Performance scores
      categories:performance:
        - error
        - minScore: 0.9
      categories:accessibility:
        - error
        - minScore: 0.95
      categories:best-practices:
        - warn
        - minScore: 0.9
      categories:seo:
        - warn
        - minScore: 0.9
  upload:
    target: 'lhci'
    serverBaseUrl: 'https://lighthouse-ci.maritime-insurance.com'
    token: $LHCI_BUILD_TOKEN
```

### 2. GitHub Actions Integration

```yaml
# .github/workflows/lighthouse-ci.yml
name: Lighthouse CI
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          
      - name: Install dependencies
        run: npm ci
        
      - name: Build application
        run: npm run build
        env:
          REACT_APP_API_URL: ${{ secrets.STAGING_API_URL }}
          
      - name: Run Lighthouse CI
        run: |
          npm install -g @lhci/cli@0.12.x
          lhci autorun
        env:
          LHCI_GITHUB_APP_TOKEN: ${{ secrets.LHCI_GITHUB_APP_TOKEN }}
          LHCI_BUILD_TOKEN: ${{ secrets.LHCI_BUILD_TOKEN }}
          
      - name: Upload Lighthouse reports
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: lighthouse-reports
          path: .lighthouseci
```

### 3. Maritime Insurance Performance Budgets

```javascript
// lighthouse-budgets.json
[
  {
    "path": "/*",
    "resourceSizes": [
      {
        "resourceType": "script",
        "budget": 300 // 300KB for JavaScript
      },
      {
        "resourceType": "stylesheet",
        "budget": 100 // 100KB for CSS
      },
      {
        "resourceType": "image",
        "budget": 500 // 500KB for images
      },
      {
        "resourceType": "total",
        "budget": 1500 // 1.5MB total page weight
      }
    ],
    "timings": [
      {
        "metric": "time-to-interactive",
        "budget": 3000 // 3 seconds TTI
      },
      {
        "metric": "first-contentful-paint",
        "budget": 1500 // 1.5 seconds FCP
      }
    ]
  },
  {
    "path": "/risk-assessment/*",
    "resourceSizes": [
      {
        "resourceType": "third-party",
        "budget": 200 // Stricter budget for risk assessment tools
      }
    ]
  }
]
```

### 4. Custom Lighthouse Configuration

```javascript
// lighthouse.config.js
module.exports = {
  extends: 'lighthouse:default',
  settings: {
    // Skip PWA audits for internal tools
    skipAudits: ['maskable-icon', 'apple-touch-icon'],
    // Custom throttling for maritime industry users
    throttling: {
      rttMs: 150, // Typical corporate network RTT
      throughputKbps: 1638.4, // 10 Mbps
      cpuSlowdownMultiplier: 2,
    },
    // Form factor settings
    formFactor: 'desktop',
    screenEmulation: {
      mobile: false,
      width: 1920,
      height: 1080,
      deviceScaleFactor: 1,
    },
  },
  // Custom audits for maritime insurance
  audits: [
    'metrics/maritime-form-responsiveness',
    'metrics/policy-data-load-time',
  ],
  categories: {
    'maritime-performance': {
      title: 'Maritime Insurance Performance',
      description: 'Industry-specific performance metrics',
      auditRefs: [
        {id: 'maritime-form-responsiveness', weight: 2},
        {id: 'policy-data-load-time', weight: 3},
      ],
    },
  },
};
```

## Maritime Insurance Implementation

### 1. Performance Monitoring Dashboard

```javascript
// lighthouse-dashboard.js
const express = require('express');
const { getClient } = require('@lhci/server/src/api/storage/storage-method.js');

const app = express();
const client = getClient({
  storageMethod: 'sql',
  sqlDatabasePath: './lighthouse-ci.db',
});

// Performance trends API
app.get('/api/performance-trends/:projectId', async (req, res) => {
  const { projectId } = req.params;
  const builds = await client.getBuilds(projectId, {
    limit: 30,
    branch: 'main',
  });
  
  const trends = builds.map(build => ({
    date: build.createdAt,
    performance: build.statistics.performance.median,
    lcp: build.statistics['largest-contentful-paint'].median,
    fid: build.statistics['max-potential-fid'].median,
    cls: build.statistics['cumulative-layout-shift'].median,
    ttfb: build.statistics['server-response-time'].median,
  }));
  
  res.json(trends);
});

// Page-specific metrics
app.get('/api/page-metrics/:projectId', async (req, res) => {
  const { projectId } = req.params;
  const { url } = req.query;
  
  const runs = await client.getRuns(projectId, {
    url,
    limit: 10,
  });
  
  const metrics = runs.map(run => ({
    url: run.url,
    performance: run.lhr.categories.performance.score * 100,
    accessibility: run.lhr.categories.accessibility.score * 100,
    bestPractices: run.lhr.categories['best-practices'].score * 100,
    seo: run.lhr.categories.seo.score * 100,
    diagnostics: {
      fcp: run.lhr.audits['first-contentful-paint'].numericValue,
      lcp: run.lhr.audits['largest-contentful-paint'].numericValue,
      cls: run.lhr.audits['cumulative-layout-shift'].numericValue,
      tbt: run.lhr.audits['total-blocking-time'].numericValue,
    },
  }));
  
  res.json(metrics);
});
```

### 2. React Performance Monitoring Component

```jsx
// PerformanceMonitor.jsx
import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';

const PerformanceMonitor = ({ projectId }) => {
  const [trends, setTrends] = useState([]);
  const [selectedMetric, setSelectedMetric] = useState('performance');
  
  useEffect(() => {
    fetchPerformanceTrends();
  }, [projectId]);
  
  const fetchPerformanceTrends = async () => {
    const response = await fetch(`/api/performance-trends/${projectId}`);
    const data = await response.json();
    setTrends(data);
  };
  
  const metrics = {
    performance: { label: 'Performance Score', color: '#0ea5e9' },
    lcp: { label: 'Largest Contentful Paint', color: '#10b981' },
    cls: { label: 'Cumulative Layout Shift', color: '#f59e0b' },
    ttfb: { label: 'Time to First Byte', color: '#8b5cf6' },
  };
  
  return (
    <div className="performance-monitor">
      <h2>Maritime Insurance App Performance Trends</h2>
      
      <div className="metric-selector">
        {Object.entries(metrics).map(([key, config]) => (
          <button
            key={key}
            onClick={() => setSelectedMetric(key)}
            className={selectedMetric === key ? 'active' : ''}
          >
            {config.label}
          </button>
        ))}
      </div>
      
      <LineChart width={800} height={400} data={trends}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis 
          dataKey="date" 
          tickFormatter={(date) => new Date(date).toLocaleDateString()}
        />
        <YAxis />
        <Tooltip />
        <Line 
          type="monotone" 
          dataKey={selectedMetric}
          stroke={metrics[selectedMetric].color}
          strokeWidth={2}
        />
      </LineChart>
      
      <PerformanceAlerts trends={trends} />
    </div>
  );
};

const PerformanceAlerts = ({ trends }) => {
  const getAlerts = () => {
    if (!trends.length) return [];
    
    const latest = trends[trends.length - 1];
    const alerts = [];
    
    if (latest.lcp > 2500) {
      alerts.push({
        level: 'error',
        message: `LCP is ${latest.lcp}ms - exceeds 2.5s threshold`,
        recommendation: 'Optimize largest content element loading',
      });
    }
    
    if (latest.cls > 0.1) {
      alerts.push({
        level: 'warning',
        message: `CLS is ${latest.cls} - layout shifts detected`,
        recommendation: 'Reserve space for dynamic content',
      });
    }
    
    return alerts;
  };
  
  return (
    <div className="performance-alerts">
      {getAlerts().map((alert, index) => (
        <div key={index} className={`alert ${alert.level}`}>
          <strong>{alert.message}</strong>
          <p>{alert.recommendation}</p>
        </div>
      ))}
    </div>
  );
};
```

### 3. Performance Optimization Scripts

```javascript
// performance-analyzer.js
const fs = require('fs');
const path = require('path');

class PerformanceAnalyzer {
  constructor(lhciManifest) {
    this.manifest = JSON.parse(fs.readFileSync(lhciManifest, 'utf8'));
  }
  
  analyzeBundle() {
    const results = [];
    
    this.manifest.forEach(run => {
      const { url, summary } = run;
      const bundles = summary.audits['resource-summary'].details.items;
      
      bundles.forEach(bundle => {
        if (bundle.transferSize > 200000) { // 200KB threshold
          results.push({
            url,
            resource: bundle.label,
            size: bundle.transferSize,
            recommendation: this.getBundleRecommendation(bundle),
          });
        }
      });
    });
    
    return results;
  }
  
  getBundleRecommendation(bundle) {
    if (bundle.label.includes('JavaScript')) {
      return 'Consider code splitting or lazy loading';
    }
    if (bundle.label.includes('Images')) {
      return 'Optimize images with next-gen formats (WebP, AVIF)';
    }
    if (bundle.label.includes('CSS')) {
      return 'Remove unused CSS with PurgeCSS';
    }
    return 'Review resource necessity';
  }
  
  generateOptimizationReport() {
    const bundleIssues = this.analyzeBundle();
    const report = {
      timestamp: new Date().toISOString(),
      totalIssues: bundleIssues.length,
      criticalIssues: bundleIssues.filter(i => i.size > 500000).length,
      recommendations: this.prioritizeRecommendations(bundleIssues),
    };
    
    fs.writeFileSync(
      'performance-optimization-report.json',
      JSON.stringify(report, null, 2)
    );
    
    return report;
  }
  
  prioritizeRecommendations(issues) {
    return issues
      .sort((a, b) => b.size - a.size)
      .slice(0, 5)
      .map(issue => ({
        priority: issue.size > 500000 ? 'high' : 'medium',
        ...issue,
      }));
  }
}
```

## Team Collaboration Features

### 1. Slack Integration

```javascript
// slack-lighthouse-bot.js
const { WebClient } = require('@slack/web-api');
const { getClient } = require('@lhci/server/src/api/storage/storage-method.js');

const slack = new WebClient(process.env.SLACK_TOKEN);
const lhciClient = getClient({
  storageMethod: 'sql',
  sqlDatabasePath: './lighthouse-ci.db',
});

async function notifyPerformanceRegression(build) {
  const previousBuild = await lhciClient.findAncestorBuild(build.id);
  
  if (!previousBuild) return;
  
  const regressions = [];
  const improvements = [];
  
  // Compare performance scores
  Object.keys(build.statistics).forEach(metric => {
    const current = build.statistics[metric].median;
    const previous = previousBuild.statistics[metric].median;
    const diff = current - previous;
    
    if (metric === 'performance-score') {
      if (diff < -5) {
        regressions.push(`Performance score dropped by ${Math.abs(diff)}%`);
      } else if (diff > 5) {
        improvements.push(`Performance score improved by ${diff}%`);
      }
    }
  });
  
  if (regressions.length > 0) {
    await slack.chat.postMessage({
      channel: '#maritime-app-performance',
      blocks: [
        {
          type: 'header',
          text: {
            type: 'plain_text',
            text: '⚠️ Performance Regression Detected',
          },
        },
        {
          type: 'section',
          text: {
            type: 'mrkdwn',
            text: `*Branch:* ${build.branch}\n*Commit:* ${build.hash}`,
          },
        },
        {
          type: 'section',
          text: {
            type: 'mrkdwn',
            text: `*Regressions:*\n${regressions.map(r => `• ${r}`).join('\n')}`,
          },
        },
        {
          type: 'actions',
          elements: [
            {
              type: 'button',
              text: {
                type: 'plain_text',
                text: 'View Report',
              },
              url: `${process.env.LHCI_SERVER_URL}/app/projects/${build.projectId}/builds/${build.id}`,
            },
          ],
        },
      ],
    });
  }
}
```

### 2. Performance Review Dashboard

```html
<!-- performance-review.html -->
<!DOCTYPE html>
<html>
<head>
  <title>Maritime Insurance Performance Review</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
  <div class="dashboard">
    <h1>Weekly Performance Review</h1>
    
    <div class="metrics-grid">
      <div class="metric-card">
        <h3>Performance Score</h3>
        <canvas id="performanceChart"></canvas>
        <div class="metric-details">
          <p>Current: <span id="currentPerf">92</span></p>
          <p>Target: <span id="targetPerf">90</span></p>
          <p>Status: <span class="status-good">✓ Meeting target</span></p>
        </div>
      </div>
      
      <div class="metric-card">
        <h3>Core Web Vitals</h3>
        <canvas id="vitalsChart"></canvas>
        <div class="vital-details">
          <p>LCP: <span class="vital-good">1.8s</span></p>
          <p>FID: <span class="vital-good">45ms</span></p>
          <p>CLS: <span class="vital-needs-improvement">0.08</span></p>
        </div>
      </div>
      
      <div class="metric-card">
        <h3>Page Performance Breakdown</h3>
        <table class="performance-table">
          <thead>
            <tr>
              <th>Page</th>
              <th>Score</th>
              <th>Load Time</th>
              <th>Trend</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>/policies</td>
              <td class="score-good">94</td>
              <td>1.2s</td>
              <td class="trend-up">↑ +3</td>
            </tr>
            <tr>
              <td>/claims</td>
              <td class="score-ok">88</td>
              <td>1.8s</td>
              <td class="trend-stable">→ 0</td>
            </tr>
            <tr>
              <td>/risk-assessment</td>
              <td class="score-poor">78</td>
              <td>2.4s</td>
              <td class="trend-down">↓ -5</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    
    <div class="action-items">
      <h2>Recommended Actions</h2>
      <ul>
        <li>
          <strong>Risk Assessment Page:</strong> Implement lazy loading for charts
          <span class="impact">Expected improvement: +10 points</span>
        </li>
        <li>
          <strong>All Pages:</strong> Enable text compression (gzip)
          <span class="impact">Expected improvement: -200ms load time</span>
        </li>
        <li>
          <strong>Claims Page:</strong> Optimize database queries
          <span class="impact">Expected improvement: -500ms TTFB</span>
        </li>
      </ul>
    </div>
  </div>
  
  <script>
    // Performance trend chart
    const perfCtx = document.getElementById('performanceChart').getContext('2d');
    new Chart(perfCtx, {
      type: 'line',
      data: {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
        datasets: [{
          label: 'Performance Score',
          data: [89, 91, 90, 92, 92],
          borderColor: '#10b981',
          tension: 0.1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: false,
            min: 80,
            max: 100
          }
        }
      }
    });
  </script>
</body>
</html>
```

## CI/CD Integration Examples

### 1. Jenkins Pipeline

```groovy
// Jenkinsfile
pipeline {
  agent any
  
  environment {
    LHCI_BUILD_TOKEN = credentials('lhci-build-token')
  }
  
  stages {
    stage('Build') {
      steps {
        sh 'npm ci'
        sh 'npm run build'
      }
    }
    
    stage('Lighthouse CI') {
      steps {
        sh 'npm install -g @lhci/cli@0.12.x'
        sh 'lhci autorun'
      }
      post {
        always {
          publishHTML([
            allowMissing: false,
            alwaysLinkToLastBuild: true,
            keepAll: true,
            reportDir: '.lighthouseci',
            reportFiles: '*.html',
            reportName: 'Lighthouse Report'
          ])
        }
      }
    }
    
    stage('Performance Gate') {
      steps {
        script {
          def lhciReport = readJSON file: '.lighthouseci/manifest.json'
          def performanceScore = lhciReport[0].summary.performance
          
          if (performanceScore < 0.9) {
            error("Performance score ${performanceScore} is below threshold")
          }
        }
      }
    }
  }
}
```

### 2. GitLab CI Integration

```yaml
# .gitlab-ci.yml
stages:
  - build
  - test
  - performance

variables:
  LHCI_BUILD_TOKEN: $LHCI_BUILD_TOKEN

lighthouse:
  stage: performance
  image: node:18
  before_script:
    - npm ci
    - npm run build
    - npm install -g @lhci/cli@0.12.x
  script:
    - lhci autorun
  artifacts:
    when: always
    paths:
      - .lighthouseci
    reports:
      performance: .lighthouseci/lhr-*.json
  only:
    - merge_requests
    - main
```

## Best Practices

### 1. Performance Budget Management

```javascript
// performance-budget-monitor.js
class PerformanceBudgetMonitor {
  constructor(budgetConfig) {
    this.budgets = budgetConfig;
  }
  
  checkBudgets(lhrData) {
    const violations = [];
    
    // Check resource size budgets
    const resources = lhrData.audits['resource-summary'].details.items;
    resources.forEach(resource => {
      const budget = this.budgets.resourceSizes.find(
        b => b.resourceType === resource.resourceType
      );
      
      if (budget && resource.transferSize > budget.budget * 1024) {
        violations.push({
          type: 'resource-size',
          resource: resource.label,
          actual: resource.transferSize,
          budget: budget.budget * 1024,
          severity: 'error'
        });
      }
    });
    
    // Check timing budgets
    this.budgets.timings.forEach(timing => {
      const audit = lhrData.audits[timing.metric];
      if (audit && audit.numericValue > timing.budget) {
        violations.push({
          type: 'timing',
          metric: timing.metric,
          actual: audit.numericValue,
          budget: timing.budget,
          severity: 'warning'
        });
      }
    });
    
    return violations;
  }
  
  generateReport(violations) {
    if (violations.length === 0) {
      console.log('✅ All performance budgets met!');
      return;
    }
    
    console.log('❌ Performance budget violations:');
    violations.forEach(v => {
      const percentOver = ((v.actual - v.budget) / v.budget * 100).toFixed(1);
      console.log(`  - ${v.type}: ${v.resource || v.metric} is ${percentOver}% over budget`);
    });
  }
}
```

### 2. Custom Metrics for Maritime Insurance

```javascript
// maritime-metrics.js
module.exports = {
  audits: [{
    id: 'maritime-form-responsiveness',
    title: 'Form Input Responsiveness',
    description: 'Measures responsiveness of critical insurance forms',
    requiredArtifacts: ['traces'],
    
    audit: (artifacts) => {
      const trace = artifacts.traces.defaultPass;
      const formInteractions = trace.traceEvents.filter(event => 
        event.name === 'Event' && 
        event.args && 
        event.args.data && 
        event.args.data.type === 'input'
      );
      
      let totalDelay = 0;
      let count = 0;
      
      formInteractions.forEach(interaction => {
        const responseTime = this.calculateResponseTime(interaction, trace);
        if (responseTime > 50) { // 50ms threshold
          totalDelay += responseTime;
          count++;
        }
      });
      
      const score = count === 0 ? 1 : Math.max(0, 1 - (totalDelay / (count * 100)));
      
      return {
        score,
        numericValue: totalDelay / Math.max(1, count),
        displayValue: `Average form response time: ${(totalDelay / Math.max(1, count)).toFixed(0)}ms`,
      };
    }
  }]
};
```

## Pricing

Lighthouse CI is **completely free and open source**. There are no licensing costs, usage limits, or premium tiers. You can:

- Run unlimited audits
- Store unlimited historical data
- Deploy on your own infrastructure
- Modify the source code as needed

### Deployment Options

1. **Self-Hosted Server** (Free)
   - Deploy on your infrastructure
   - Full control over data
   - No external dependencies

2. **GitHub Actions** (Free within limits)
   - 2,000 minutes/month free for private repos
   - Unlimited for public repos

3. **Cloud Infrastructure Costs** (Variable)
   - Only pay for hosting if using cloud services
   - Typical costs: $5-20/month for small teams

## Team Collaboration

### 1. Shared Performance Dashboard

```javascript
// team-dashboard-server.js
const express = require('express');
const app = express();

app.get('/team-metrics', async (req, res) => {
  const teamMetrics = await aggregateTeamMetrics();
  
  res.json({
    overview: {
      averageScore: teamMetrics.avgScore,
      totalBuilds: teamMetrics.buildCount,
      improvementRate: teamMetrics.improvementTrend,
    },
    topIssues: teamMetrics.commonIssues,
    teamGoals: {
      performance: { target: 90, current: teamMetrics.avgScore },
      accessibility: { target: 95, current: teamMetrics.avgAccessibility },
    },
    recentActivity: teamMetrics.recentBuilds.map(build => ({
      developer: build.author,
      branch: build.branch,
      score: build.score,
      timestamp: build.createdAt,
    })),
  });
});
```

### 2. Performance Review Automation

```javascript
// weekly-performance-review.js
const cron = require('node-cron');
const { generateWeeklyReport } = require('./report-generator');

// Run every Monday at 9 AM
cron.schedule('0 9 * * 1', async () => {
  const report = await generateWeeklyReport();
  
  // Send to team channels
  await sendSlackReport(report);
  await sendEmailReport(report);
  
  // Create JIRA tickets for critical issues
  if (report.criticalIssues.length > 0) {
    await createPerformanceTickets(report.criticalIssues);
  }
});
```

## Conclusion

Lighthouse CI provides comprehensive performance monitoring for maritime insurance applications with zero licensing costs. Its automated testing, historical tracking, and team collaboration features ensure consistent performance standards across development cycles. The tool's flexibility allows custom metrics and budgets tailored to insurance industry requirements while maintaining Core Web Vitals compliance.