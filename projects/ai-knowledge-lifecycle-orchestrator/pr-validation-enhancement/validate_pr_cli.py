#!/usr/bin/env python3
"""
PR Validation CLI Tool
AI Knowledge Lifecycle Orchestrator - PR Validation Enhancement

Command-line interface for testing and integrating PR validation capabilities.
Provides easy access to validation functionality for development and CI/CD integration.
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, Optional

# Handle imports gracefully for testing without dependencies
try:
    from pr_knowledge_connector import PRKnowledgeConnector, PRValidationRequest, create_sample_pr_request
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    DEPENDENCIES_AVAILABLE = False
    IMPORT_ERROR = str(e)
    # Create placeholder classes for type hints when dependencies aren't available
    class PRValidationRequest:
        pass


def create_cli_parser() -> argparse.ArgumentParser:
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description="AI-Powered PR Validation Enhancement System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test with sample PR
  python validate_pr_cli.py --test

  # Validate specific PR
  python validate_pr_cli.py --pr-id 123 --title "Update components" --files "src/App.tsx,src/utils.ts"

  # Configuration validation
  python validate_pr_cli.py --validate-config

  # Output JSON results
  python validate_pr_cli.py --test --json --output results.json
        """
    )
    
    # Main operation modes
    parser.add_argument('--test', action='store_true',
                       help='Run validation with sample PR data')
    parser.add_argument('--validate-config', action='store_true',
                       help='Validate system configuration')
    
    # PR-specific arguments
    parser.add_argument('--pr-id', type=str,
                       help='PR ID to validate')
    parser.add_argument('--title', type=str,
                       help='PR title')
    parser.add_argument('--description', type=str, default="",
                       help='PR description')
    parser.add_argument('--author', type=str, default="developer@example.com",
                       help='PR author email')
    parser.add_argument('--target-branch', type=str, default="main",
                       help='Target branch')
    parser.add_argument('--source-branch', type=str, default="feature/update",
                       help='Source branch')
    parser.add_argument('--files', type=str,
                       help='Comma-separated list of changed files')
    parser.add_argument('--repository', type=str, default="example-repo",
                       help='Repository name')
    
    # Configuration options
    parser.add_argument('--config', type=str,
                       help='Path to configuration file')
    parser.add_argument('--strict', action='store_true',
                       help='Enable strict validation mode')
    parser.add_argument('--security-scan', action='store_true', default=True,
                       help='Enable security scanning')
    
    # Output options
    parser.add_argument('--json', action='store_true',
                       help='Output results in JSON format')
    parser.add_argument('--output', type=str,
                       help='Output file path')
    parser.add_argument('--verbose', action='store_true',
                       help='Enable verbose output')
    parser.add_argument('--quiet', action='store_true',
                       help='Minimize output')
    
    # Development options
    parser.add_argument('--debug', action='store_true',
                       help='Enable debug mode')
    parser.add_argument('--dry-run', action='store_true',
                       help='Validate configuration without running validation')
    
    return parser


def validate_dependencies() -> bool:
    """Validate that required dependencies are available"""
    if not DEPENDENCIES_AVAILABLE:
        print(f"❌ Dependencies not available: {IMPORT_ERROR}")
        print("\nTo install dependencies:")
        print("  pip install -r requirements.txt")
        print("\nOr install manually:")
        print("  pip install pyyaml")
        return False
    return True


def create_pr_request_from_args(args) -> Optional[PRValidationRequest]:
    """Create PR validation request from command line arguments"""
    if not args.pr_id:
        print("❌ PR ID is required (use --pr-id)")
        return None
    
    # Parse changed files
    changed_files = []
    if args.files:
        for filename in args.files.split(','):
            filename = filename.strip()
            changed_files.append({
                'filename': filename,
                'status': 'modified',
                'additions': 10,  # Default values
                'deletions': 5,
                'changes': 15
            })
    
    # Create validation request
    return PRValidationRequest(
        pr_id=args.pr_id,
        pr_title=args.title or f"PR #{args.pr_id}",
        pr_description=args.description,
        author=args.author,
        target_branch=args.target_branch,
        source_branch=args.source_branch,
        changed_files=changed_files,
        diff_content=f"Sample diff content for PR {args.pr_id}",
        repository_context={
            'name': args.repository,
            'language': 'TypeScript',
            'framework': 'React'
        },
        validation_config={
            'strict_mode': args.strict,
            'security_scan': args.security_scan,
            'debug_mode': args.debug
        }
    )


def format_validation_results(result, format_json: bool = False, verbose: bool = False) -> str:
    """Format validation results for output"""
    if format_json:
        # Convert result to JSON-serializable format
        result_dict = {
            'pr_id': result.pr_id,
            'overall_score': result.overall_score,
            'validation_passed': result.validation_passed,
            'security_score': result.security_score,
            'consistency_score': result.consistency_score,
            'technology_currency_score': result.technology_currency_score,
            'processing_time': result.processing_time,
            'timestamp': result.timestamp,
            'critical_issues_count': len(result.critical_issues),
            'recommendations_count': len(result.recommendations)
        }
        
        if verbose:
            result_dict['critical_issues'] = result.critical_issues
            result_dict['recommendations'] = result.recommendations
            result_dict['detailed_findings'] = result.detailed_findings
        
        return json.dumps(result_dict, indent=2)
    
    else:
        # Human-readable format
        output = []
        output.append(f"PR Validation Results for PR #{result.pr_id}")
        output.append("=" * 50)
        output.append(f"Overall Score:           {result.overall_score:.1f}/100")
        output.append(f"Validation Passed:       {'✅ Yes' if result.validation_passed else '❌ No'}")
        output.append(f"Security Score:          {result.security_score:.1f}/100")
        output.append(f"Consistency Score:       {result.consistency_score:.1f}/100")
        output.append(f"Technology Currency:     {result.technology_currency_score:.1f}/100")
        output.append(f"Processing Time:         {result.processing_time:.2f}s")
        output.append("")
        
        # Critical Issues
        if result.critical_issues:
            output.append(f"🚨 Critical Issues ({len(result.critical_issues)}):")
            for i, issue in enumerate(result.critical_issues[:5]):  # Show first 5
                output.append(f"  {i+1}. {issue.get('message', 'Unknown issue')}")
            if len(result.critical_issues) > 5:
                output.append(f"  ... and {len(result.critical_issues) - 5} more")
            output.append("")
        
        # Recommendations
        if result.recommendations:
            output.append(f"💡 Recommendations ({len(result.recommendations)}):")
            for i, rec in enumerate(result.recommendations[:5]):  # Show first 5
                output.append(f"  {i+1}. {rec.get('message', 'Unknown recommendation')}")
            if len(result.recommendations) > 5:
                output.append(f"  ... and {len(result.recommendations) - 5} more")
            output.append("")
        
        # Verbose details
        if verbose and result.detailed_findings:
            output.append("📊 Detailed Analysis:")
            context = result.detailed_findings.get('context_analysis', {})
            if context:
                output.append(f"  Technologies Detected: {len(context.get('detected_technologies', []))}")
                output.append(f"  Files Analyzed: {context.get('total_files_changed', 0)}")
            
            tech_validation = result.detailed_findings.get('technology_validation', {})
            if tech_validation:
                output.append(f"  Technology Issues: {len(tech_validation.get('critical_issues', []))}")
            
            security = result.detailed_findings.get('security_assessment', {})
            if security:
                output.append(f"  Security Findings: {len(security.get('findings', []))}")
        
        return "\n".join(output)


def run_test_validation(args) -> int:
    """Run validation with sample data"""
    if not validate_dependencies():
        return 1
    
    try:
        # Initialize connector
        if not args.quiet:
            print("🔧 Initializing PR Knowledge Connector...")
        
        config_path = args.config if args.config else None
        connector = PRKnowledgeConnector(config_path)
        
        # Create sample request
        if not args.quiet:
            print("📝 Creating sample PR request...")
        
        sample_request = create_sample_pr_request()
        
        # Perform validation
        if not args.quiet:
            print("🔍 Performing PR validation...")
        
        result = connector.validate_pr(sample_request)
        
        # Format and output results
        formatted_output = format_validation_results(result, args.json, args.verbose)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(formatted_output)
            if not args.quiet:
                print(f"💾 Results saved to {args.output}")
        else:
            print(formatted_output)
        
        return 0 if result.validation_passed else 1
        
    except Exception as e:
        print(f"❌ Test validation failed: {str(e)}")
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1


def run_custom_validation(args) -> int:
    """Run validation with custom PR data"""
    if not validate_dependencies():
        return 1
    
    try:
        # Create PR request from arguments
        pr_request = create_pr_request_from_args(args)
        if not pr_request:
            return 1
        
        # Initialize connector
        if not args.quiet:
            print(f"🔧 Initializing PR Knowledge Connector for PR #{pr_request.pr_id}...")
        
        config_path = args.config if args.config else None
        connector = PRKnowledgeConnector(config_path)
        
        # Perform validation
        if not args.quiet:
            print("🔍 Performing PR validation...")
        
        result = connector.validate_pr(pr_request)
        
        # Format and output results
        formatted_output = format_validation_results(result, args.json, args.verbose)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(formatted_output)
            if not args.quiet:
                print(f"💾 Results saved to {args.output}")
        else:
            print(formatted_output)
        
        return 0 if result.validation_passed else 1
        
    except Exception as e:
        print(f"❌ Custom validation failed: {str(e)}")
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1


def run_config_validation(args) -> int:
    """Validate system configuration"""
    if not validate_dependencies():
        return 1
    
    try:
        if not args.quiet:
            print("🔧 Validating system configuration...")
        
        config_path = args.config if args.config else None
        connector = PRKnowledgeConnector(config_path)
        
        # Validate configuration
        config_validation = connector.validate_configuration()
        
        # Format results
        if args.json:
            output = json.dumps(config_validation, indent=2)
        else:
            output = []
            output.append("Configuration Validation Results")
            output.append("=" * 40)
            output.append(f"Configuration Valid: {'✅ Yes' if config_validation['configuration_valid'] else '❌ No'}")
            
            if config_validation['issues']:
                output.append(f"\n🚨 Issues Found ({len(config_validation['issues'])}):")
                for issue in config_validation['issues']:
                    output.append(f"  - {issue}")
            
            if config_validation['warnings']:
                output.append(f"\n⚠️  Warnings ({len(config_validation['warnings'])}):")
                for warning in config_validation['warnings']:
                    output.append(f"  - {warning}")
            
            output.append(f"\n📊 Component Status:")
            for component, status in config_validation['component_status'].items():
                status_icon = "✅" if status.get('status') == 'healthy' else "❌"
                output.append(f"  {status_icon} {component}: {status.get('status', 'unknown')}")
                if status.get('error'):
                    output.append(f"      Error: {status['error']}")
            
            output = "\n".join(output)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            if not args.quiet:
                print(f"💾 Configuration validation saved to {args.output}")
        else:
            print(output)
        
        return 0 if config_validation['configuration_valid'] else 1
        
    except Exception as e:
        print(f"❌ Configuration validation failed: {str(e)}")
        if args.debug:
            import traceback
            traceback.print_exc()
        return 1


def main() -> int:
    """Main CLI entry point"""
    parser = create_cli_parser()
    args = parser.parse_args()
    
    # Handle no arguments
    if len(sys.argv) == 1:
        parser.print_help()
        return 0
    
    # Set up debug mode
    if args.debug:
        import logging
        logging.basicConfig(level=logging.DEBUG)
    
    # Route to appropriate operation
    if args.test:
        return run_test_validation(args)
    elif args.validate_config:
        return run_config_validation(args)
    elif args.pr_id:
        return run_custom_validation(args)
    else:
        print("❌ No operation specified. Use --test, --validate-config, or --pr-id")
        parser.print_help()
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"💥 Unexpected error: {str(e)}")
        sys.exit(1)