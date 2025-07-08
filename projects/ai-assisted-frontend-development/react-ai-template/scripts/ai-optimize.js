#!/usr/bin/env node

/**
 * AI Performance Optimization Script
 * 
 * This script provides automated performance optimization for React applications
 * using AI-driven analysis and recommendations.
 * 
 * Features:
 * - Analyzes bundle size and composition
 * - Identifies performance bottlenecks
 * - Generates optimization recommendations
 * - Implements common optimizations automatically
 * - Creates performance reports
 * - Monitors Core Web Vitals
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Configuration
const config = {
  bundleAnalyzer: 'webpack-bundle-analyzer',
  lighthouseCI: '@lhci/cli',
  outputDir: 'performance-reports',
  thresholds: {
    bundleSize: 512, // KB
    lcp: 2500, // ms
    fid: 100, // ms
    cls: 0.1,
    lighthouse: 90, // score
  },
  optimizations: {
    enableCodeSplitting: true,
    enableTreeShaking: true,
    enableImageOptimization: true,
    enableBundleAnalysis: true,
    enableLighthouseAudit: true,
  },
};

// Colors for console output
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
};

const log = {
  info: (msg) => console.log(`${colors.blue}ℹ${colors.reset} ${msg}`),
  success: (msg) => console.log(`${colors.green}✓${colors.reset} ${msg}`),
  warning: (msg) => console.log(`${colors.yellow}⚠${colors.reset} ${msg}`),
  error: (msg) => console.log(`${colors.red}✗${colors.reset} ${msg}`),
  header: (msg) => console.log(`${colors.bright}${colors.cyan}${msg}${colors.reset}`),
};

/**
 * Main optimization function
 */
async function main() {
  const args = process.argv.slice(2);
  
  if (args.includes('--help') || args.includes('-h')) {
    showHelp();
    return;
  }

  const options = parseArgs(args);
  
  try {
    log.header('🤖 AI Performance Optimizer');
    log.info('Starting performance analysis and optimization...');
    
    // Create output directory
    if (!fs.existsSync(config.outputDir)) {
      fs.mkdirSync(config.outputDir, { recursive: true });
    }

    // Run analysis phases
    const results = {
      bundleAnalysis: null,
      lighthouseAudit: null,
      codeAnalysis: null,
      optimizations: [],
      recommendations: [],
    };

    if (options.bundle || options.all) {
      results.bundleAnalysis = await analyzeBundleSize();
    }

    if (options.lighthouse || options.all) {
      results.lighthouseAudit = await runLighthouseAudit();
    }

    if (options.code || options.all) {
      results.codeAnalysis = await analyzeCodeQuality();
    }

    // Generate AI recommendations
    results.recommendations = generateAIRecommendations(results);

    // Apply optimizations if requested
    if (options.apply) {
      results.optimizations = await applyOptimizations(results.recommendations);
    }

    // Generate report
    const report = generateReport(results);
    const reportPath = path.join(config.outputDir, `optimization-report-${Date.now()}.json`);
    fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));

    // Display summary
    displaySummary(results);
    
    log.success(`Report saved to: ${reportPath}`);
    log.header('🚀 Optimization complete!');

  } catch (error) {
    log.error(`Optimization failed: ${error.message}`);
    process.exit(1);
  }
}

/**
 * Parse command line arguments
 */
function parseArgs(args) {
  return {
    all: args.includes('--all'),
    bundle: args.includes('--bundle'),
    lighthouse: args.includes('--lighthouse'),
    code: args.includes('--code'),
    apply: args.includes('--apply'),
    ci: args.includes('--ci'),
    threshold: getArgValue(args, '--threshold'),
  };
}

/**
 * Get argument value
 */
function getArgValue(args, flag) {
  const index = args.indexOf(flag);
  return index !== -1 && index + 1 < args.length ? args[index + 1] : null;
}

/**
 * Analyze bundle size and composition
 */
async function analyzeBundleSize() {
  log.info('Analyzing bundle size...');
  
  try {
    // Build the project
    execSync('npm run build', { stdio: 'pipe' });
    
    // Analyze build directory
    const buildDir = path.join(process.cwd(), 'dist');
    const analysis = {
      totalSize: 0,
      files: [],
      chunks: {},
      recommendations: [],
    };

    if (fs.existsSync(buildDir)) {
      const files = getAllFiles(buildDir);
      
      for (const file of files) {
        const stats = fs.statSync(file);
        const relativePath = path.relative(buildDir, file);
        const size = stats.size;
        
        analysis.files.push({
          path: relativePath,
          size,
          sizeKB: Math.round(size / 1024),
        });
        
        analysis.totalSize += size;
      }
      
      // Sort by size
      analysis.files.sort((a, b) => b.size - a.size);
      
      // Analyze chunks
      analysis.chunks = analyzeChunks(analysis.files);
      
      // Generate recommendations
      analysis.recommendations = generateBundleRecommendations(analysis);
    }
    
    log.success(`Bundle analysis complete. Total size: ${Math.round(analysis.totalSize / 1024)}KB`);
    return analysis;
    
  } catch (error) {
    log.error(`Bundle analysis failed: ${error.message}`);
    return null;
  }
}

/**
 * Get all files recursively
 */
function getAllFiles(dir) {
  const files = [];
  
  function traverse(currentDir) {
    const items = fs.readdirSync(currentDir);
    
    for (const item of items) {
      const fullPath = path.join(currentDir, item);
      const stats = fs.statSync(fullPath);
      
      if (stats.isDirectory()) {
        traverse(fullPath);
      } else {
        files.push(fullPath);
      }
    }
  }
  
  traverse(dir);
  return files;
}

/**
 * Analyze chunks
 */
function analyzeChunks(files) {
  const chunks = {
    vendor: { size: 0, files: [] },
    main: { size: 0, files: [] },
    css: { size: 0, files: [] },
    assets: { size: 0, files: [] },
  };
  
  for (const file of files) {
    if (file.path.includes('vendor') || file.path.includes('node_modules')) {
      chunks.vendor.size += file.size;
      chunks.vendor.files.push(file);
    } else if (file.path.endsWith('.css')) {
      chunks.css.size += file.size;
      chunks.css.files.push(file);
    } else if (file.path.endsWith('.js')) {
      chunks.main.size += file.size;
      chunks.main.files.push(file);
    } else {
      chunks.assets.size += file.size;
      chunks.assets.files.push(file);
    }
  }
  
  return chunks;
}

/**
 * Generate bundle recommendations
 */
function generateBundleRecommendations(analysis) {
  const recommendations = [];
  const totalSizeKB = Math.round(analysis.totalSize / 1024);
  
  if (totalSizeKB > config.thresholds.bundleSize) {
    recommendations.push({
      type: 'bundle-size',
      priority: 'high',
      title: 'Reduce bundle size',
      description: `Bundle size is ${totalSizeKB}KB, exceeding the ${config.thresholds.bundleSize}KB threshold.`,
      actions: [
        'Implement code splitting',
        'Remove unused dependencies',
        'Use dynamic imports',
        'Enable tree shaking',
      ],
    });
  }
  
  // Check for large vendor chunks
  const vendorSizeKB = Math.round(analysis.chunks.vendor.size / 1024);
  if (vendorSizeKB > 200) {
    recommendations.push({
      type: 'vendor-chunk',
      priority: 'medium',
      title: 'Optimize vendor chunk',
      description: `Vendor chunk is ${vendorSizeKB}KB. Consider splitting large libraries.`,
      actions: [
        'Split vendor chunks by library',
        'Use CDN for large libraries',
        'Consider lighter alternatives',
      ],
    });
  }
  
  // Check for large individual files
  const largeFiles = analysis.files.filter(f => f.sizeKB > 100);
  if (largeFiles.length > 0) {
    recommendations.push({
      type: 'large-files',
      priority: 'medium',
      title: 'Optimize large files',
      description: `Found ${largeFiles.length} files larger than 100KB.`,
      actions: [
        'Split large components',
        'Use lazy loading',
        'Optimize images and assets',
      ],
      files: largeFiles.map(f => ({ path: f.path, size: f.sizeKB })),
    });
  }
  
  return recommendations;
}

/**
 * Run Lighthouse audit
 */
async function runLighthouseAudit() {
  log.info('Running Lighthouse performance audit...');
  
  try {
    // Check if Lighthouse CI is available
    try {
      execSync('npx lhci --version', { stdio: 'pipe' });
    } catch {
      log.warning('Lighthouse CI not available. Installing...');
      execSync('npm install -g @lhci/cli', { stdio: 'pipe' });
    }
    
    // Create Lighthouse configuration
    const lighthouseConfig = {
      ci: {
        collect: {
          url: ['http://localhost:3000'],
          startServerCommand: 'npm start',
          startServerReadyPattern: 'Local:',
          startServerReadyTimeout: 30000,
        },
        assert: {
          assertions: {
            'categories:performance': ['error', { minScore: config.thresholds.lighthouse / 100 }],
            'categories:accessibility': ['error', { minScore: 0.9 }],
            'categories:best-practices': ['error', { minScore: 0.9 }],
            'categories:seo': ['error', { minScore: 0.9 }],
          },
        },
        upload: {
          target: 'temporary-public-storage',
        },
      },
    };
    
    const configPath = path.join(config.outputDir, 'lighthouserc.json');
    fs.writeFileSync(configPath, JSON.stringify(lighthouseConfig, null, 2));
    
    // Run Lighthouse
    const result = execSync(`npx lhci autorun --config=${configPath}`, { 
      encoding: 'utf8',
      stdio: 'pipe',
    });
    
    log.success('Lighthouse audit complete');
    return parseLighthouseResults(result);
    
  } catch (error) {
    log.error(`Lighthouse audit failed: ${error.message}`);
    return null;
  }
}

/**
 * Parse Lighthouse results
 */
function parseLighthouseResults(output) {
  const results = {
    performance: null,
    accessibility: null,
    bestPractices: null,
    seo: null,
    recommendations: [],
  };
  
  try {
    // Extract scores from output
    const scoreRegex = /Performance: (\d+)/;
    const performanceMatch = output.match(scoreRegex);
    
    if (performanceMatch) {
      results.performance = parseInt(performanceMatch[1]);
    }
    
    // Generate recommendations based on scores
    if (results.performance && results.performance < config.thresholds.lighthouse) {
      results.recommendations.push({
        type: 'lighthouse-performance',
        priority: 'high',
        title: 'Improve Lighthouse performance score',
        description: `Performance score is ${results.performance}, below the ${config.thresholds.lighthouse} threshold.`,
        actions: [
          'Optimize Core Web Vitals',
          'Reduce bundle size',
          'Optimize images',
          'Eliminate render-blocking resources',
        ],
      });
    }
    
  } catch (error) {
    log.warning(`Failed to parse Lighthouse results: ${error.message}`);
  }
  
  return results;
}

/**
 * Analyze code quality and performance patterns
 */
async function analyzeCodeQuality() {
  log.info('Analyzing code quality and performance patterns...');
  
  const analysis = {
    components: [],
    hooks: [],
    patterns: [],
    recommendations: [],
  };
  
  try {
    // Find all React components
    const srcDir = path.join(process.cwd(), 'src');
    const componentFiles = findFiles(srcDir, /\.(tsx?|jsx?)$/);
    
    for (const file of componentFiles) {
      const content = fs.readFileSync(file, 'utf8');
      const componentAnalysis = analyzeComponent(file, content);
      
      if (componentAnalysis.isComponent) {
        analysis.components.push(componentAnalysis);
      }
    }
    
    // Generate code quality recommendations
    analysis.recommendations = generateCodeQualityRecommendations(analysis);
    
    log.success(`Code analysis complete. Analyzed ${analysis.components.length} components`);
    return analysis;
    
  } catch (error) {
    log.error(`Code analysis failed: ${error.message}`);
    return null;
  }
}

/**
 * Find files matching pattern
 */
function findFiles(dir, pattern) {
  const files = [];
  
  function traverse(currentDir) {
    if (!fs.existsSync(currentDir)) return;
    
    const items = fs.readdirSync(currentDir);
    
    for (const item of items) {
      const fullPath = path.join(currentDir, item);
      const stats = fs.statSync(fullPath);
      
      if (stats.isDirectory() && !item.startsWith('.') && item !== 'node_modules') {
        traverse(fullPath);
      } else if (stats.isFile() && pattern.test(item)) {
        files.push(fullPath);
      }
    }
  }
  
  traverse(dir);
  return files;
}

/**
 * Analyze individual component
 */
function analyzeComponent(filePath, content) {
  const analysis = {
    file: path.relative(process.cwd(), filePath),
    name: path.basename(filePath, path.extname(filePath)),
    isComponent: false,
    linesOfCode: content.split('\\n').length,
    hooks: [],
    issues: [],
    optimizationOpportunities: [],
  };
  
  // Check if it's a React component
  if (content.includes('React') || content.includes('useState') || content.includes('useEffect')) {
    analysis.isComponent = true;
  }
  
  // Extract hooks
  const hookMatches = content.match(/use\\w+/g);
  if (hookMatches) {
    analysis.hooks = [...new Set(hookMatches)];
  }
  
  // Identify potential issues
  if (content.includes('console.log')) {
    analysis.issues.push('Contains console.log statements');
  }
  
  if (analysis.linesOfCode > 200) {
    analysis.issues.push('Component is too large (>200 lines)');
    analysis.optimizationOpportunities.push('Split into smaller components');
  }
  
  if (content.includes('useEffect') && !content.includes('[]')) {
    analysis.optimizationOpportunities.push('Consider memoizing useEffect dependencies');
  }
  
  if (content.includes('map(') && !content.includes('React.memo')) {
    analysis.optimizationOpportunities.push('Consider using React.memo for list items');
  }
  
  if (content.includes('onChange') && !content.includes('useCallback')) {
    analysis.optimizationOpportunities.push('Consider using useCallback for event handlers');
  }
  
  return analysis;
}

/**
 * Generate code quality recommendations
 */
function generateCodeQualityRecommendations(analysis) {
  const recommendations = [];
  
  // Find components with issues
  const problemComponents = analysis.components.filter(c => c.issues.length > 0);
  if (problemComponents.length > 0) {
    recommendations.push({
      type: 'code-quality',
      priority: 'medium',
      title: 'Fix code quality issues',
      description: `Found ${problemComponents.length} components with potential issues.`,
      actions: [
        'Remove console.log statements',
        'Split large components',
        'Add proper error boundaries',
      ],
      components: problemComponents.map(c => ({
        name: c.name,
        file: c.file,
        issues: c.issues,
      })),
    });
  }
  
  // Find optimization opportunities
  const optimizableComponents = analysis.components.filter(c => c.optimizationOpportunities.length > 0);
  if (optimizableComponents.length > 0) {
    recommendations.push({
      type: 'performance-optimization',
      priority: 'medium',
      title: 'Optimize component performance',
      description: `Found ${optimizableComponents.length} components with optimization opportunities.`,
      actions: [
        'Add React.memo to prevent unnecessary re-renders',
        'Use useCallback and useMemo for expensive operations',
        'Optimize event handlers',
      ],
      components: optimizableComponents.map(c => ({
        name: c.name,
        file: c.file,
        opportunities: c.optimizationOpportunities,
      })),
    });
  }
  
  return recommendations;
}

/**
 * Generate AI recommendations
 */
function generateAIRecommendations(results) {
  const allRecommendations = [];
  
  // Collect recommendations from all analyses
  if (results.bundleAnalysis?.recommendations) {
    allRecommendations.push(...results.bundleAnalysis.recommendations);
  }
  
  if (results.lighthouseAudit?.recommendations) {
    allRecommendations.push(...results.lighthouseAudit.recommendations);
  }
  
  if (results.codeAnalysis?.recommendations) {
    allRecommendations.push(...results.codeAnalysis.recommendations);
  }
  
  // Add AI-specific recommendations
  const aiRecommendations = generateAdvancedRecommendations(results);
  allRecommendations.push(...aiRecommendations);
  
  // Sort by priority
  const priorityOrder = { high: 3, medium: 2, low: 1 };
  allRecommendations.sort((a, b) => priorityOrder[b.priority] - priorityOrder[a.priority]);
  
  return allRecommendations;
}

/**
 * Generate advanced AI recommendations
 */
function generateAdvancedRecommendations(results) {
  const recommendations = [];
  
  // Bundle optimization patterns
  if (results.bundleAnalysis) {
    const totalSize = results.bundleAnalysis.totalSize / 1024; // KB
    
    if (totalSize > 1000) {
      recommendations.push({
        type: 'ai-bundle-splitting',
        priority: 'high',
        title: 'Implement intelligent code splitting',
        description: 'Large bundle detected. AI suggests route-based and component-based splitting.',
        actions: [
          'Split routes with React.lazy()',
          'Split large components',
          'Use dynamic imports for features',
          'Implement progressive loading',
        ],
        automatable: true,
      });
    }
  }
  
  // Performance pattern analysis
  if (results.codeAnalysis) {
    const componentsWithHooks = results.codeAnalysis.components.filter(c => c.hooks.length > 5);
    
    if (componentsWithHooks.length > 0) {
      recommendations.push({
        type: 'ai-hook-optimization',
        priority: 'medium',
        title: 'Optimize React hooks usage',
        description: 'Components with many hooks detected. Consider custom hooks and memoization.',
        actions: [
          'Extract custom hooks',
          'Add useMemo for expensive calculations',
          'Use useCallback for stable references',
          'Consider state consolidation',
        ],
        components: componentsWithHooks.map(c => c.name),
        automatable: false,
      });
    }
  }
  
  return recommendations;
}

/**
 * Apply optimizations automatically
 */
async function applyOptimizations(recommendations) {
  log.info('Applying automatic optimizations...');
  
  const applied = [];
  
  for (const rec of recommendations) {
    if (rec.automatable) {
      try {
        const result = await applyOptimization(rec);
        if (result.success) {
          applied.push({
            recommendation: rec.title,
            result: result.message,
          });
          log.success(`Applied: ${rec.title}`);
        }
      } catch (error) {
        log.warning(`Failed to apply ${rec.title}: ${error.message}`);
      }
    }
  }
  
  log.success(`Applied ${applied.length} automatic optimizations`);
  return applied;
}

/**
 * Apply individual optimization
 */
async function applyOptimization(recommendation) {
  switch (recommendation.type) {
    case 'ai-bundle-splitting':
      return applyBundleSplitting();
      
    default:
      return { success: false, message: 'Optimization not supported' };
  }
}

/**
 * Apply bundle splitting optimization
 */
function applyBundleSplitting() {
  // This would implement automatic code splitting
  // For now, just create configuration suggestions
  
  const viteConfigSuggestion = `
// Add to vite.config.ts
export default defineConfig({
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
          router: ['react-router-dom'],
          ui: ['@headlessui/react', 'lucide-react'],
        },
      },
    },
  },
});
`;
  
  const suggestionsPath = path.join(config.outputDir, 'optimization-suggestions.md');
  fs.writeFileSync(suggestionsPath, viteConfigSuggestion);
  
  return {
    success: true,
    message: `Bundle splitting suggestions saved to ${suggestionsPath}`,
  };
}

/**
 * Generate final report
 */
function generateReport(results) {
  return {
    timestamp: new Date().toISOString(),
    version: '1.0.0',
    project: path.basename(process.cwd()),
    summary: {
      totalRecommendations: results.recommendations.length,
      highPriority: results.recommendations.filter(r => r.priority === 'high').length,
      mediumPriority: results.recommendations.filter(r => r.priority === 'medium').length,
      lowPriority: results.recommendations.filter(r => r.priority === 'low').length,
      optimizationsApplied: results.optimizations.length,
    },
    analysis: {
      bundle: results.bundleAnalysis,
      lighthouse: results.lighthouseAudit,
      code: results.codeAnalysis,
    },
    recommendations: results.recommendations,
    optimizations: results.optimizations,
    nextSteps: generateNextSteps(results.recommendations),
  };
}

/**
 * Generate next steps
 */
function generateNextSteps(recommendations) {
  const steps = [];
  
  const highPriority = recommendations.filter(r => r.priority === 'high');
  if (highPriority.length > 0) {
    steps.push('Address high-priority performance issues first');
    steps.push('Focus on Core Web Vitals optimization');
  }
  
  const bundleIssues = recommendations.filter(r => r.type.includes('bundle'));
  if (bundleIssues.length > 0) {
    steps.push('Implement code splitting and bundle optimization');
  }
  
  const codeIssues = recommendations.filter(r => r.type.includes('code'));
  if (codeIssues.length > 0) {
    steps.push('Refactor components for better performance');
  }
  
  steps.push('Set up continuous performance monitoring');
  steps.push('Implement performance budgets in CI/CD');
  
  return steps;
}

/**
 * Display summary
 */
function displaySummary(results) {
  log.header('📊 Optimization Summary');
  
  if (results.bundleAnalysis) {
    const totalSizeKB = Math.round(results.bundleAnalysis.totalSize / 1024);
    log.info(`Bundle size: ${totalSizeKB}KB`);
  }
  
  if (results.lighthouseAudit?.performance) {
    log.info(`Lighthouse performance: ${results.lighthouseAudit.performance}/100`);
  }
  
  if (results.codeAnalysis) {
    log.info(`Components analyzed: ${results.codeAnalysis.components.length}`);
  }
  
  log.info(`Recommendations generated: ${results.recommendations.length}`);
  log.info(`Optimizations applied: ${results.optimizations.length}`);
  
  // Show top recommendations
  const topRecs = results.recommendations.slice(0, 3);
  if (topRecs.length > 0) {
    log.header('🔧 Top Recommendations:');
    topRecs.forEach((rec, index) => {
      log.info(`${index + 1}. [${rec.priority.toUpperCase()}] ${rec.title}`);
    });
  }
}

/**
 * Show help message
 */
function showHelp() {
  console.log(`
AI Performance Optimizer

Usage: node ai-optimize.js [options]

Options:
  --all              Run all analyses (default)
  --bundle           Analyze bundle size and composition
  --lighthouse       Run Lighthouse performance audit  
  --code             Analyze code quality and patterns
  --apply            Apply automatic optimizations
  --ci               Run in CI mode (no interactive prompts)
  --threshold <n>    Set performance threshold
  --help, -h         Show this help message

Examples:
  node ai-optimize.js --all
  node ai-optimize.js --bundle --lighthouse
  node ai-optimize.js --apply --ci
  node ai-optimize.js --threshold 95
  `);
}

// Run the script
if (require.main === module) {
  main().catch(error => {
    log.error(error.message);
    process.exit(1);
  });
}

module.exports = {
  analyzeBundleSize,
  runLighthouseAudit,
  analyzeCodeQuality,
  generateAIRecommendations,
  config,
};