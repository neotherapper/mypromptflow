/**
 * AI Test Results Processor
 * 
 * Processes Jest test results and generates AI-friendly analytics and reports
 * for continuous improvement of test quality and component reliability.
 */

const fs = require('fs');
const path = require('path');

/**
 * Process test results and generate analytics
 */
function processTestResults(results) {
  const analytics = {
    timestamp: new Date().toISOString(),
    summary: generateSummary(results),
    performance: analyzePerformance(results),
    coverage: analyzeCoverage(results),
    accessibility: analyzeAccessibility(results),
    aiInsights: generateAIInsights(results),
    recommendations: generateRecommendations(results),
  };
  
  // Write analytics to file
  const outputPath = path.join(process.cwd(), 'coverage', 'ai-analytics.json');
  fs.writeFileSync(outputPath, JSON.stringify(analytics, null, 2));
  
  // Generate human-readable report
  generateHumanReport(analytics);
  
  // Return original results for Jest
  return results;
}

/**
 * Generate test summary
 */
function generateSummary(results) {
  return {
    totalTests: results.numTotalTests,
    passedTests: results.numPassedTests,
    failedTests: results.numFailedTests,
    pendingTests: results.numPendingTests,
    testSuites: results.numTotalTestSuites,
    passedTestSuites: results.numPassedTestSuites,
    failedTestSuites: results.numFailedTestSuites,
    runtime: results.testResults.reduce((total, suite) => total + suite.perfStats.runtime, 0),
    success: results.success,
  };
}

/**
 * Analyze performance metrics
 */
function analyzePerformance(results) {
  const performanceTests = results.testResults.filter(suite => 
    suite.testFilePath.includes('performance.test')
  );
  
  const runtimes = results.testResults.map(suite => suite.perfStats.runtime);
  
  return {
    averageRuntime: runtimes.reduce((sum, time) => sum + time, 0) / runtimes.length,
    slowestSuite: Math.max(...runtimes),
    fastestSuite: Math.min(...runtimes),
    performanceTestsCount: performanceTests.length,
    performanceTestsResults: performanceTests.map(suite => ({
      file: path.basename(suite.testFilePath),
      runtime: suite.perfStats.runtime,
      passed: suite.numPassingTests,
      failed: suite.numFailingTests,
    })),
  };
}

/**
 * Analyze coverage data
 */
function analyzeCoverage(results) {
  const coverageSummary = results.coverageMap?.getCoverageSummary?.();
  
  if (!coverageSummary) {
    return { available: false };
  }
  
  return {
    available: true,
    lines: {
      total: coverageSummary.lines.total,
      covered: coverageSummary.lines.covered,
      percentage: coverageSummary.lines.pct,
    },
    functions: {
      total: coverageSummary.functions.total,
      covered: coverageSummary.functions.covered,
      percentage: coverageSummary.functions.pct,
    },
    branches: {
      total: coverageSummary.branches.total,
      covered: coverageSummary.branches.covered,
      percentage: coverageSummary.branches.pct,
    },
    statements: {
      total: coverageSummary.statements.total,
      covered: coverageSummary.statements.covered,
      percentage: coverageSummary.statements.pct,
    },
  };
}

/**
 * Analyze accessibility test results
 */
function analyzeAccessibility(results) {
  const accessibilityTests = results.testResults.filter(suite => 
    suite.testFilePath.includes('accessibility.test')
  );
  
  const accessibilityIssues = [];
  
  accessibilityTests.forEach(suite => {
    suite.testResults.forEach(test => {
      if (test.status === 'failed' && test.failureMessages) {
        test.failureMessages.forEach(message => {
          if (message.includes('accessibility') || message.includes('axe')) {
            accessibilityIssues.push({
              suite: path.basename(suite.testFilePath),
              test: test.title,
              message: message,
            });
          }
        });
      }
    });
  });
  
  return {
    testsCount: accessibilityTests.length,
    issuesFound: accessibilityIssues.length,
    issues: accessibilityIssues,
    compliance: accessibilityIssues.length === 0 ? 'WCAG 2.1 AA' : 'Issues found',
  };
}

/**
 * Generate AI insights based on test results
 */
function generateAIInsights(results) {
  const insights = [];
  
  // Analyze test patterns
  const testTypes = {
    unit: 0,
    integration: 0,
    accessibility: 0,
    performance: 0,
  };
  
  results.testResults.forEach(suite => {
    const fileName = path.basename(suite.testFilePath);
    if (fileName.includes('integration')) testTypes.integration++;
    else if (fileName.includes('accessibility')) testTypes.accessibility++;
    else if (fileName.includes('performance')) testTypes.performance++;
    else testTypes.unit++;
  });
  
  // Generate insights based on test distribution
  const totalTests = Object.values(testTypes).reduce((sum, count) => sum + count, 0);
  
  if (testTypes.unit / totalTests < 0.6) {
    insights.push({
      type: 'warning',
      category: 'test-distribution',
      message: 'Consider adding more unit tests. Unit tests should comprise 60-70% of test suite.',
      impact: 'medium',
    });
  }
  
  if (testTypes.accessibility === 0) {
    insights.push({
      type: 'error',
      category: 'accessibility',
      message: 'No accessibility tests found. Add accessibility tests for WCAG compliance.',
      impact: 'high',
    });
  }
  
  if (testTypes.performance === 0) {
    insights.push({
      type: 'warning',
      category: 'performance',
      message: 'No performance tests found. Consider adding performance benchmarks.',
      impact: 'medium',
    });
  }
  
  // Analyze failure patterns
  const failedTests = results.testResults.filter(suite => suite.numFailingTests > 0);
  if (failedTests.length > 0) {
    const commonFailures = analyzeCommonFailures(failedTests);
    insights.push(...commonFailures);
  }
  
  return insights;
}

/**
 * Analyze common failure patterns
 */
function analyzeCommonFailures(failedTests) {
  const insights = [];
  const failurePatterns = {};
  
  failedTests.forEach(suite => {
    suite.testResults.forEach(test => {
      if (test.status === 'failed' && test.failureMessages) {
        test.failureMessages.forEach(message => {
          // Extract common error patterns
          if (message.includes('timeout')) {
            failurePatterns.timeout = (failurePatterns.timeout || 0) + 1;
          }
          if (message.includes('accessibility')) {
            failurePatterns.accessibility = (failurePatterns.accessibility || 0) + 1;
          }
          if (message.includes('performance')) {
            failurePatterns.performance = (failurePatterns.performance || 0) + 1;
          }
          if (message.includes('async')) {
            failurePatterns.async = (failurePatterns.async || 0) + 1;
          }
        });
      }
    });
  });
  
  Object.entries(failurePatterns).forEach(([pattern, count]) => {
    if (count > 1) {
      insights.push({
        type: 'error',
        category: 'failure-pattern',
        message: `Multiple ${pattern} failures detected (${count} occurrences). Review ${pattern} handling.`,
        impact: 'high',
      });
    }
  });
  
  return insights;
}

/**
 * Generate recommendations based on analysis
 */
function generateRecommendations(results) {
  const recommendations = [];
  
  // Coverage recommendations
  const coverage = analyzeCoverage(results);
  if (coverage.available) {
    if (coverage.lines.percentage < 80) {
      recommendations.push({
        priority: 'high',
        category: 'coverage',
        action: 'Increase line coverage',
        description: `Current line coverage is ${coverage.lines.percentage}%. Target: 85%+`,
        effort: 'medium',
      });
    }
    
    if (coverage.branches.percentage < 75) {
      recommendations.push({
        priority: 'high',
        category: 'coverage',
        action: 'Improve branch coverage',
        description: `Current branch coverage is ${coverage.branches.percentage}%. Add edge case tests.`,
        effort: 'high',
      });
    }
  }
  
  // Performance recommendations
  const performance = analyzePerformance(results);
  if (performance.averageRuntime > 5000) {
    recommendations.push({
      priority: 'medium',
      category: 'performance',
      action: 'Optimize test performance',
      description: `Average test runtime is ${performance.averageRuntime}ms. Consider mocking heavy operations.`,
      effort: 'medium',
    });
  }
  
  // Test quality recommendations
  const summary = generateSummary(results);
  if (summary.failedTests > 0) {
    recommendations.push({
      priority: 'high',
      category: 'reliability',
      action: 'Fix failing tests',
      description: `${summary.failedTests} tests are failing. Address failures before deployment.`,
      effort: 'high',
    });
  }
  
  return recommendations;
}

/**
 * Generate human-readable report
 */
function generateHumanReport(analytics) {
  const report = `
# AI Test Analytics Report
Generated: ${analytics.timestamp}

## Summary
- Total Tests: ${analytics.summary.totalTests}
- Passed: ${analytics.summary.passedTests}
- Failed: ${analytics.summary.failedTests}
- Success Rate: ${((analytics.summary.passedTests / analytics.summary.totalTests) * 100).toFixed(1)}%
- Runtime: ${analytics.summary.runtime}ms

## Coverage
${analytics.coverage.available ? `
- Lines: ${analytics.coverage.lines.percentage}% (${analytics.coverage.lines.covered}/${analytics.coverage.lines.total})
- Functions: ${analytics.coverage.functions.percentage}% (${analytics.coverage.functions.covered}/${analytics.coverage.functions.total})
- Branches: ${analytics.coverage.branches.percentage}% (${analytics.coverage.branches.covered}/${analytics.coverage.branches.total})
- Statements: ${analytics.coverage.statements.percentage}% (${analytics.coverage.statements.covered}/${analytics.coverage.statements.total})
` : 'Coverage data not available'}

## Performance
- Average Runtime: ${analytics.performance.averageRuntime.toFixed(2)}ms
- Slowest Suite: ${analytics.performance.slowestSuite}ms
- Performance Tests: ${analytics.performance.performanceTestsCount}

## Accessibility
- Tests: ${analytics.accessibility.testsCount}
- Issues: ${analytics.accessibility.issuesFound}
- Compliance: ${analytics.accessibility.compliance}

## AI Insights
${analytics.aiInsights.map(insight => 
  `- [${insight.type.toUpperCase()}] ${insight.message} (Impact: ${insight.impact})`
).join('\\n')}

## Recommendations
${analytics.recommendations.map(rec => 
  `- [${rec.priority.toUpperCase()}] ${rec.action}: ${rec.description} (Effort: ${rec.effort})`
).join('\\n')}
`;

  const reportPath = path.join(process.cwd(), 'coverage', 'ai-report.md');
  fs.writeFileSync(reportPath, report);
  
  console.log('\\n🤖 AI Test Analytics Report generated:');
  console.log(`   📊 Analytics: coverage/ai-analytics.json`);
  console.log(`   📝 Report: coverage/ai-report.md`);
}

module.exports = processTestResults;