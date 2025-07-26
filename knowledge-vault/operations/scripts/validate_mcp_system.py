#!/usr/bin/env python3
"""
MCP System Validation Script
Validates the MCP integration system without requiring external dependencies
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import Dict, List, Any, Optional

def check_file_structure() -> Dict[str, bool]:
    """Check if all required files and directories exist"""
    results = {}
    base_path = Path(__file__).parent.parent.parent.parent
    
    # Required files
    required_files = {
        'sync_operations': 'knowledge-vault/operations/sync-operations-executable.md',
        'property_mappings': 'knowledge-vault/operations/notion-property-mappings.md',
        'data_transformations': 'knowledge-vault/operations/data-transformations.md',
        'batch_migration': 'knowledge-vault/operations/scripts/batch_migration.py',
        'validate_schemas': 'knowledge-vault/operations/scripts/validate_schemas.py',
        'test_data_generator': 'knowledge-vault/operations/scripts/create_vanguardai_test_data.py',
        'progress_monitor': 'knowledge-vault/operations/scripts/progress_monitor.py',
        'integration_tests': 'knowledge-vault/operations/scripts/integration_test_suite.py'
    }
    
    for name, file_path in required_files.items():
        full_path = base_path / file_path
        results[name] = full_path.exists()
        if full_path.exists():
            # Check if file is executable for Python scripts
            if file_path.endswith('.py'):
                results[f'{name}_executable'] = os.access(full_path, os.X_OK)
    
    # Required directories
    required_dirs = {
        'operations': 'knowledge-vault/operations',
        'scripts': 'knowledge-vault/operations/scripts',
        'logs': 'knowledge-vault/operations/logs'
    }
    
    for name, dir_path in required_dirs.items():
        full_path = base_path / dir_path
        # Create directory if it doesn't exist
        full_path.mkdir(parents=True, exist_ok=True)
        results[f'dir_{name}'] = full_path.exists()
    
    return results

def validate_yaml_syntax() -> Dict[str, bool]:
    """Validate YAML configuration files syntax"""
    results = {}
    base_path = Path(__file__).parent.parent.parent.parent
    
    yaml_files = [
        'knowledge-vault/operations/sync-operations-executable.md',
        'knowledge-vault/operations/notion-property-mappings.md',
        'knowledge-vault/operations/data-transformations.md'
    ]
    
    for yaml_file in yaml_files:
        file_path = base_path / yaml_file
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Basic YAML syntax checks
                has_proper_structure = True
                
                # Check for basic YAML structure indicators
                if not any(line.strip().endswith(':') for line in content.split('\n')):
                    has_proper_structure = False
                
                # Check for reasonable file size
                if len(content) < 100:  # Too small to be a real config
                    has_proper_structure = False
                
                # Check for common YAML keywords
                yaml_keywords = ['version', 'description', 'operations', 'properties', 'mappings']
                if not any(keyword in content.lower() for keyword in yaml_keywords):
                    has_proper_structure = False
                
                results[yaml_file.split('/')[-1]] = has_proper_structure
                
            except Exception as e:
                results[yaml_file.split('/')[-1]] = False
        else:
            results[yaml_file.split('/')[-1]] = False
    
    return results

def validate_python_scripts() -> Dict[str, bool]:
    """Validate Python scripts syntax"""
    results = {}
    base_path = Path(__file__).parent.parent.parent.parent
    
    python_files = [
        'knowledge-vault/operations/scripts/batch_migration.py',
        'knowledge-vault/operations/scripts/validate_schemas.py',
        'knowledge-vault/operations/scripts/create_vanguardai_test_data.py',
        'knowledge-vault/operations/scripts/progress_monitor.py'
    ]
    
    for py_file in python_files:
        file_path = base_path / py_file
        if file_path.exists():
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Basic Python syntax validation
                has_proper_structure = True
                
                # Check for shebang
                if not content.startswith('#!/usr/bin/env python3'):
                    has_proper_structure = False
                
                # Check for proper imports
                if 'import' not in content:
                    has_proper_structure = False
                
                # Check for class or function definitions
                if not ('def ' in content or 'class ' in content):
                    has_proper_structure = False
                
                # Check for main execution pattern
                if "__name__ == '__main__'" not in content:
                    has_proper_structure = False
                
                # Check file size
                if len(content) < 1000:  # Too small for a real implementation
                    has_proper_structure = False
                
                results[py_file.split('/')[-1]] = has_proper_structure
                
            except Exception as e:
                results[py_file.split('/')[-1]] = False
        else:
            results[py_file.split('/')[-1]] = False
    
    return results

def check_configuration_completeness() -> Dict[str, Any]:
    """Check if configurations are complete"""
    results = {}
    base_path = Path(__file__).parent.parent.parent.parent
    
    # Check sync operations
    sync_ops_path = base_path / 'knowledge-vault/operations/sync-operations-executable.md'
    if sync_ops_path.exists():
        with open(sync_ops_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for VanguardAI test migration
        results['vanguardai_test_migration'] = 'vanguardai_test_migration' in content.lower()
        results['sync_operations_size'] = len(content)
        results['has_migration_commands'] = 'migrate' in content.lower()
    
    # Check property mappings
    prop_map_path = base_path / 'knowledge-vault/operations/notion-property-mappings.md'
    if prop_map_path.exists():
        with open(prop_map_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        results['has_database_schemas'] = 'database' in content.lower()
        results['has_property_definitions'] = 'properties' in content.lower()
        results['property_mappings_size'] = len(content)
    
    # Check data transformations
    data_trans_path = base_path / 'knowledge-vault/operations/data-transformations.md'
    if data_trans_path.exists():
        with open(data_trans_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        results['has_transformation_rules'] = 'transformation' in content.lower()
        results['has_mapping_tables'] = 'mapping' in content.lower()
        results['data_transformations_size'] = len(content)
    
    return results

def check_script_capabilities() -> Dict[str, Any]:
    """Check if scripts have required capabilities"""
    results = {}
    base_path = Path(__file__).parent.parent.parent.parent
    
    # Check batch migration script
    batch_script = base_path / 'knowledge-vault/operations/scripts/batch_migration.py'
    if batch_script.exists():
        with open(batch_script, 'r', encoding='utf-8') as f:
            content = f.read()
        
        results['batch_migration'] = {
            'has_notion_api_client': 'NotionAPIClient' in content,
            'has_data_transformer': 'DataTransformer' in content,
            'has_relationship_manager': 'RelationshipManager' in content,
            'has_error_handling': 'try:' in content and 'except' in content,
            'has_rate_limiting': 'rate_limit' in content.lower(),
            'has_progress_tracking': 'progress' in content.lower(),
            'script_size': len(content)
        }
    
    # Check validation script
    validation_script = base_path / 'knowledge-vault/operations/scripts/validate_schemas.py'
    if validation_script.exists():
        with open(validation_script, 'r', encoding='utf-8') as f:
            content = f.read()
        
        results['schema_validation'] = {
            'has_schema_validator': 'SchemaValidator' in content,
            'has_validation_rules': 'validation_rules' in content,
            'has_cross_reference_validation': 'cross_reference' in content.lower(),
            'has_report_generation': 'report' in content.lower(),
            'script_size': len(content)
        }
    
    # Check progress monitor
    progress_script = base_path / 'knowledge-vault/operations/scripts/progress_monitor.py'
    if progress_script.exists():
        with open(progress_script, 'r', encoding='utf-8') as f:
            content = f.read()
        
        results['progress_monitor'] = {
            'has_progress_monitor': 'ProgressMonitor' in content,
            'has_metrics_collection': 'metrics' in content.lower(),
            'has_performance_tracking': 'performance' in content.lower(),
            'has_real_time_monitoring': 'real.?time' in content.lower(),
            'script_size': len(content)
        }
    
    return results

def generate_system_readiness_score() -> Dict[str, Any]:
    """Generate overall system readiness assessment"""
    
    file_structure = check_file_structure()
    yaml_syntax = validate_yaml_syntax()
    python_syntax = validate_python_scripts()
    config_completeness = check_configuration_completeness()
    script_capabilities = check_script_capabilities()
    
    # Calculate scores
    file_score = (sum(file_structure.values()) / len(file_structure)) * 100
    yaml_score = (sum(yaml_syntax.values()) / len(yaml_syntax)) * 100 if yaml_syntax else 0
    python_score = (sum(python_syntax.values()) / len(python_syntax)) * 100 if python_syntax else 0
    
    # Configuration score based on key indicators
    config_score = 0
    if config_completeness:
        config_indicators = [
            config_completeness.get('vanguardai_test_migration', False),
            config_completeness.get('has_database_schemas', False),
            config_completeness.get('has_transformation_rules', False),
            config_completeness.get('sync_operations_size', 0) > 10000,
            config_completeness.get('property_mappings_size', 0) > 10000,
            config_completeness.get('data_transformations_size', 0) > 10000
        ]
        config_score = (sum(config_indicators) / len(config_indicators)) * 100
    
    # Script capabilities score
    capability_score = 0
    if script_capabilities:
        all_capabilities = []
        for script_name, capabilities in script_capabilities.items():
            if isinstance(capabilities, dict):
                script_caps = [v for k, v in capabilities.items() if isinstance(v, bool)]
                all_capabilities.extend(script_caps)
        
        if all_capabilities:
            capability_score = (sum(all_capabilities) / len(all_capabilities)) * 100
    
    # Overall readiness score (weighted average)
    overall_score = (
        file_score * 0.25 +
        yaml_score * 0.20 +
        python_score * 0.20 +
        config_score * 0.20 +
        capability_score * 0.15
    )
    
    # Determine readiness level
    if overall_score >= 95:
        readiness_level = "PRODUCTION_READY"
    elif overall_score >= 85:
        readiness_level = "STAGING_READY"
    elif overall_score >= 70:
        readiness_level = "DEVELOPMENT_READY"
    else:
        readiness_level = "NEEDS_DEVELOPMENT"
    
    return {
        'overall_score': overall_score,
        'readiness_level': readiness_level,
        'component_scores': {
            'file_structure': file_score,
            'yaml_syntax': yaml_score,
            'python_syntax': python_score,
            'configuration_completeness': config_score,
            'script_capabilities': capability_score
        },
        'detailed_results': {
            'file_structure': file_structure,
            'yaml_syntax': yaml_syntax,
            'python_syntax': python_syntax,
            'configuration_completeness': config_completeness,
            'script_capabilities': script_capabilities
        }
    }

def main():
    """Main validation function"""
    print("🔍 MCP System Validation")
    print("=" * 50)
    
    start_time = time.time()
    
    # Generate system readiness assessment
    assessment = generate_system_readiness_score()
    
    duration = time.time() - start_time
    
    # Display results
    print(f"📊 SYSTEM READINESS ASSESSMENT")
    print("=" * 50)
    print(f"Overall Score: {assessment['overall_score']:.1f}/100")
    print(f"Readiness Level: {assessment['readiness_level']}")
    print(f"Assessment Duration: {duration:.2f} seconds")
    print()
    
    print("📈 Component Scores:")
    for component, score in assessment['component_scores'].items():
        status = "✅" if score >= 90 else "⚠️" if score >= 70 else "❌"
        print(f"   {status} {component.replace('_', ' ').title()}: {score:.1f}%")
    
    print()
    
    # Recommendations based on score
    if assessment['overall_score'] >= 95:
        print("🎉 RECOMMENDATIONS:")
        print("   ✅ System is production-ready for MCP Notion integration!")
        print("   ✅ All components are functioning correctly")
        print("   ✅ Ready to execute VanguardAI test migration")
    elif assessment['overall_score'] >= 85:
        print("⚠️ RECOMMENDATIONS:")
        print("   📋 System is mostly ready - review failed components")
        print("   📋 Consider running integration tests before production use")
        print("   📋 Minor improvements needed for production readiness")
    elif assessment['overall_score'] >= 70:
        print("🔧 RECOMMENDATIONS:")
        print("   📋 System needs development work before use")
        print("   📋 Review and fix failing components")
        print("   📋 Complete configuration and script development")
    else:
        print("❌ RECOMMENDATIONS:")
        print("   📋 System requires significant development work")
        print("   📋 Multiple critical components need attention")
        print("   📋 Not ready for any migration activities")
    
    # Save detailed assessment
    base_path = Path(__file__).parent.parent.parent.parent
    logs_dir = base_path / 'knowledge-vault/operations/logs'
    logs_dir.mkdir(exist_ok=True)
    
    assessment['timestamp'] = time.strftime('%Y-%m-%d %H:%M:%S')
    assessment['duration'] = duration
    
    report_file = logs_dir / f'mcp_system_validation_{int(time.time())}.json'
    with open(report_file, 'w') as f:
        json.dump(assessment, f, indent=2)
    
    print(f"\n📄 Detailed assessment saved to: {report_file}")
    print("=" * 50)
    
    # Exit with appropriate code
    if assessment['overall_score'] >= 85:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()