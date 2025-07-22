#!/usr/bin/env python3
"""
MCP Integration Test Runner
Quick test execution and validation for MCP Notion integration system
"""

import os
import sys
import time
import logging
from pathlib import Path
from typing import Dict, List, Any

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_system_requirements() -> Dict[str, bool]:
    """Check if all system requirements are met"""
    requirements = {}
    
    # Check Python version
    requirements['python_version'] = sys.version_info >= (3, 8)
    
    # Check required files exist
    required_files = [
        'knowledge-vault/operations/sync-operations-executable.yaml',
        'knowledge-vault/operations/notion-property-mappings.yaml',
        'knowledge-vault/operations/data-transformations.yaml',
        'knowledge-vault/operations/scripts/batch_migration.py',
        'knowledge-vault/operations/scripts/validate_schemas.py',
        'knowledge-vault/operations/scripts/create_vanguardai_test_data.py',
        'knowledge-vault/operations/scripts/progress_monitor.py',
        'knowledge-vault/operations/scripts/integration_test_suite.py'
    ]
    
    for file_path in required_files:
        full_path = PROJECT_ROOT / file_path
        requirements[f'file_{file_path.split("/")[-1]}'] = full_path.exists()
    
    # Check required directories
    required_dirs = [
        'knowledge-vault',
        'knowledge-vault/operations',
        'knowledge-vault/operations/scripts',
        'knowledge-vault/operations/logs'
    ]
    
    for dir_path in required_dirs:
        full_path = PROJECT_ROOT / dir_path
        full_path.mkdir(exist_ok=True)  # Create if missing
        requirements[f'dir_{dir_path.split("/")[-1]}'] = full_path.exists()
    
    # Check Python packages
    try:
        import yaml
        requirements['yaml_package'] = True
    except ImportError:
        requirements['yaml_package'] = False
    
    try:
        import requests
        requirements['requests_package'] = True
    except ImportError:
        requirements['requests_package'] = False
    
    return requirements

def run_quick_validation() -> bool:
    """Run quick validation tests"""
    logger.info("Running quick validation tests...")
    
    try:
        # Test 1: Import all modules
        logger.info("Testing module imports...")
        
        from knowledge_vault.operations.scripts.batch_migration import BatchMigrationOrchestrator
        from knowledge_vault.operations.scripts.validate_schemas import SchemaValidator
        from knowledge_vault.operations.scripts.create_vanguardai_test_data import VanguardAITestDataGenerator
        from knowledge_vault.operations.scripts.progress_monitor import ProgressMonitor
        
        logger.info("✅ All modules imported successfully")
        
        # Test 2: Configuration file validation
        logger.info("Testing configuration files...")
        
        config_files = [
            PROJECT_ROOT / 'knowledge-vault/operations/notion-property-mappings.yaml',
            PROJECT_ROOT / 'knowledge-vault/operations/data-transformations.yaml'
        ]
        
        import yaml
        for config_file in config_files:
            if config_file.exists():
                with open(config_file, 'r') as f:
                    yaml.safe_load(f)
                logger.info(f"✅ {config_file.name} is valid YAML")
            else:
                logger.warning(f"⚠️  {config_file.name} not found")
        
        # Test 3: Basic class instantiation
        logger.info("Testing class instantiation...")
        
        # Test progress monitor
        monitor = ProgressMonitor(session_id="test_validation")
        logger.info("✅ ProgressMonitor instantiated")
        
        # Test schema validator
        validator = SchemaValidator()
        logger.info("✅ SchemaValidator instantiated")
        
        # Test data generator
        generator = VanguardAITestDataGenerator()
        logger.info("✅ VanguardAITestDataGenerator instantiated")
        
        logger.info("🎉 Quick validation completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Quick validation failed: {e}")
        return False

def run_component_tests() -> Dict[str, bool]:
    """Run individual component tests"""
    logger.info("Running component tests...")
    
    results = {}
    
    # Test 1: Schema Validation Component
    try:
        logger.info("Testing schema validation component...")
        from knowledge_vault.operations.scripts.validate_schemas import SchemaValidator
        
        validator = SchemaValidator()
        
        # Test validation rules loading
        assert validator.validation_rules is not None
        assert 'required_fields' in validator.validation_rules
        
        logger.info("✅ Schema validation component working")
        results['schema_validation'] = True
        
    except Exception as e:
        logger.error(f"❌ Schema validation component failed: {e}")
        results['schema_validation'] = False
    
    # Test 2: Data Transformation Component
    try:
        logger.info("Testing data transformation component...")
        
        # Mock transformation config
        transformation_config = {
            'database_transformations': {
                'knowledge_vault_transformations': {
                    'property_mappings': {
                        'id': {
                            'notion_property': 'ID',
                            'transformation_rule': 'yaml_field_to_notion_title'
                        }
                    }
                }
            }
        }
        
        property_mappings = {
            'mapping_tables': {
                'star_rating_mapping': {
                    1: {'name': '⭐'},
                    2: {'name': '⭐⭐'},
                    3: {'name': '⭐⭐⭐'},
                    4: {'name': '⭐⭐⭐⭐'},
                    5: {'name': '⭐⭐⭐⭐⭐'}
                }
            }
        }
        
        from knowledge_vault.operations.scripts.batch_migration import DataTransformer
        transformer = DataTransformer(transformation_config, property_mappings)
        
        # Test transformation
        sample_item = {'id': 'test-item', 'name': 'Test Item'}
        notion_props, relationships = transformer.transform_item(sample_item, 'knowledge_vault')
        
        logger.info("✅ Data transformation component working")
        results['data_transformation'] = True
        
    except Exception as e:
        logger.error(f"❌ Data transformation component failed: {e}")
        results['data_transformation'] = False
    
    # Test 3: Progress Monitoring Component
    try:
        logger.info("Testing progress monitoring component...")
        from knowledge_vault.operations.scripts.progress_monitor import ProgressMonitor
        
        monitor = ProgressMonitor(session_id="component_test")
        monitor.start_monitoring(total_items=10)
        
        # Test progress updates
        monitor.increment_completed(3)
        monitor.increment_failed(1)
        
        status = monitor.get_current_status()
        assert status['progress']['completed'] == 3
        assert status['progress']['failed'] == 1
        
        monitor.stop_monitoring()
        
        logger.info("✅ Progress monitoring component working")
        results['progress_monitoring'] = True
        
    except Exception as e:
        logger.error(f"❌ Progress monitoring component failed: {e}")
        results['progress_monitoring'] = False
    
    # Test 4: Test Data Generation Component
    try:
        logger.info("Testing test data generation component...")
        from knowledge_vault.operations.scripts.create_vanguardai_test_data import VanguardAITestDataGenerator
        
        import tempfile
        with tempfile.TemporaryDirectory() as temp_dir:
            generator = VanguardAITestDataGenerator(output_path=Path(temp_dir))
            
            # Generate minimal test data
            generator.item_counts = {db: 1 for db in generator.item_counts.keys()}
            test_env = generator.generate_complete_test_environment()
            
            assert len(test_env) > 0
            assert 'knowledge_vault_items' in test_env
            
        logger.info("✅ Test data generation component working")
        results['test_data_generation'] = True
        
    except Exception as e:
        logger.error(f"❌ Test data generation component failed: {e}")
        results['test_data_generation'] = False
    
    return results

def run_integration_test() -> bool:
    """Run a simple integration test"""
    logger.info("Running integration test...")
    
    try:
        import tempfile
        from unittest.mock import patch, Mock
        
        # Create temporary test environment
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create test data structure
            test_data_dir = temp_path / 'databases' / 'vanguard-ai-test'
            kv_items_dir = test_data_dir / 'knowledge_vault_items'
            kv_items_dir.mkdir(parents=True, exist_ok=True)
            
            # Create test item
            import yaml
            test_item = {
                'id': 'integration-test-item',
                'name': 'Integration Test Item',
                'category': 'Testing',
                'status': 'Research',
                'description': 'Test item for integration testing',
                'type': 'Framework'
            }
            
            with open(kv_items_dir / 'test-item.yaml', 'w') as f:
                yaml.dump(test_item, f)
            
            # Test migration configuration
            from knowledge_vault.operations.scripts.batch_migration import MigrationConfig
            
            config = MigrationConfig(
                notion_token="test_token",
                workspace_id="test_workspace",
                source_path=temp_path,
                transformation_config_path=PROJECT_ROOT / 'knowledge-vault/operations/data-transformations.yaml',
                property_mappings_path=PROJECT_ROOT / 'knowledge-vault/operations/notion-property-mappings.yaml',
                dry_run=True
            )
            
            logger.info("✅ Integration test configuration created")
            
            # Mock the orchestrator execution
            from knowledge_vault.operations.scripts.batch_migration import BatchMigrationOrchestrator
            
            with patch.object(BatchMigrationOrchestrator, '_load_yaml') as mock_load:
                mock_load.return_value = {'test': 'data'}
                
                orchestrator = BatchMigrationOrchestrator(config)
                logger.info("✅ Migration orchestrator created successfully")
        
        logger.info("🎉 Integration test completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Integration test failed: {e}")
        return False

def generate_test_report(requirements: Dict[str, bool], component_results: Dict[str, bool], 
                        quick_validation: bool, integration_test: bool) -> Dict[str, Any]:
    """Generate comprehensive test report"""
    
    total_checks = len(requirements) + len(component_results) + 2  # +2 for quick_validation and integration_test
    passed_checks = sum(requirements.values()) + sum(component_results.values()) + \
                   (1 if quick_validation else 0) + (1 if integration_test else 0)
    
    report = {
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'summary': {
            'total_checks': total_checks,
            'passed_checks': passed_checks,
            'failed_checks': total_checks - passed_checks,
            'success_rate': (passed_checks / total_checks) * 100,
            'overall_status': 'PASS' if passed_checks == total_checks else 'FAIL'
        },
        'system_requirements': requirements,
        'component_tests': component_results,
        'validation_tests': {
            'quick_validation': quick_validation,
            'integration_test': integration_test
        },
        'recommendations': []
    }
    
    # Generate recommendations
    if report['summary']['success_rate'] == 100:
        report['recommendations'].append("✅ All tests passed! MCP integration system is ready for use.")
    elif report['summary']['success_rate'] >= 90:
        report['recommendations'].append("⚠️ Most tests passed. Review failed items before proceeding.")
    else:
        report['recommendations'].append("❌ Multiple test failures. System needs attention before use.")
    
    # Specific recommendations
    if not requirements.get('python_version', True):
        report['recommendations'].append("📋 Upgrade Python to version 3.8 or higher")
    
    if not requirements.get('yaml_package', True):
        report['recommendations'].append("📋 Install PyYAML: pip install PyYAML")
    
    if not requirements.get('requests_package', True):
        report['recommendations'].append("📋 Install requests: pip install requests")
    
    failed_components = [k for k, v in component_results.items() if not v]
    if failed_components:
        report['recommendations'].append(f"📋 Fix component issues: {', '.join(failed_components)}")
    
    return report

def main():
    """Main test runner"""
    print("🚀 MCP Integration Test Runner")
    print("=" * 50)
    
    start_time = time.time()
    
    # Step 1: Check system requirements
    print("1. Checking system requirements...")
    requirements = check_system_requirements()
    
    req_passed = sum(requirements.values())
    req_total = len(requirements)
    print(f"   Requirements: {req_passed}/{req_total} passed")
    
    # Step 2: Run quick validation
    print("\n2. Running quick validation...")
    quick_validation = run_quick_validation()
    
    # Step 3: Run component tests
    print("\n3. Running component tests...")
    component_results = run_component_tests()
    
    comp_passed = sum(component_results.values())
    comp_total = len(component_results)
    print(f"   Components: {comp_passed}/{comp_total} passed")
    
    # Step 4: Run integration test
    print("\n4. Running integration test...")
    integration_test = run_integration_test()
    
    # Step 5: Generate report
    print("\n5. Generating test report...")
    report = generate_test_report(requirements, component_results, quick_validation, integration_test)
    
    # Display results
    duration = time.time() - start_time
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    print(f"Overall Status: {report['summary']['overall_status']}")
    print(f"Success Rate: {report['summary']['success_rate']:.1f}%")
    print(f"Total Checks: {report['summary']['total_checks']}")
    print(f"Passed: {report['summary']['passed_checks']}")
    print(f"Failed: {report['summary']['failed_checks']}")
    print(f"Duration: {duration:.2f} seconds")
    
    if report['recommendations']:
        print(f"\n📋 RECOMMENDATIONS:")
        for rec in report['recommendations']:
            print(f"   {rec}")
    
    # Save detailed report
    logs_dir = PROJECT_ROOT / 'knowledge-vault/operations/logs'
    logs_dir.mkdir(exist_ok=True)
    
    import json
    report_file = logs_dir / f'integration_test_summary_{int(time.time())}.json'
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Detailed report saved to: {report_file}")
    print("=" * 50)
    
    # Exit with appropriate code
    sys.exit(0 if report['summary']['overall_status'] == 'PASS' else 1)

if __name__ == '__main__':
    main()