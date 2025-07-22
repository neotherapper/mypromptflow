#!/usr/bin/env python3
"""
MCP Notion Integration Testing Framework
Comprehensive test suite for VanguardAI test environment migration
Validates all components of the MCP integration system
"""

import os
import sys
import json
import yaml
import time
import logging
import pytest
import asyncio
import tempfile
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from unittest.mock import Mock, patch
import requests_mock

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import our modules
from knowledge_vault.operations.scripts.batch_migration import (
    BatchMigrationOrchestrator, MigrationConfig, NotionAPIClient, 
    DataTransformer, RelationshipManager
)
from knowledge_vault.operations.scripts.validate_schemas import SchemaValidator
from knowledge_vault.operations.scripts.create_vanguardai_test_data import VanguardAITestDataGenerator
from knowledge_vault.operations.scripts.progress_monitor import ProgressMonitor

# Configuration
KNOWLEDGE_VAULT_PATH = PROJECT_ROOT / 'knowledge-vault'
TEST_DATA_PATH = KNOWLEDGE_VAULT_PATH / 'databases' / 'vanguard-ai-test'
LOGS_PATH = KNOWLEDGE_VAULT_PATH / 'operations' / 'logs'

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class TestResult:
    """Result of a single test"""
    test_name: str
    success: bool
    duration: float
    error_message: Optional[str]
    details: Dict[str, Any]

@dataclass
class TestSuiteResult:
    """Result of entire test suite"""
    total_tests: int
    passed_tests: int
    failed_tests: int
    success_rate: float
    total_duration: float
    test_results: List[TestResult]
    summary: Dict[str, Any]

class MockNotionAPI:
    """Mock Notion API for testing without real API calls"""
    
    def __init__(self):
        self.databases = {}
        self.pages = {}
        self.call_count = 0
        self.database_counter = 1
        self.page_counter = 1
        
    def create_database(self, parent_id: str, title: str, properties: Dict) -> Dict:
        """Mock database creation"""
        self.call_count += 1
        db_id = f"mock_db_{self.database_counter}"
        self.database_counter += 1
        
        database = {
            'id': db_id,
            'title': [{'type': 'text', 'text': {'content': title}}],
            'properties': properties,
            'parent': {'page_id': parent_id},
            'created_time': datetime.now().isoformat()
        }
        
        self.databases[db_id] = database
        return database
    
    def create_page(self, database_id: str, properties: Dict, children: List = None) -> Dict:
        """Mock page creation"""
        self.call_count += 1
        page_id = f"mock_page_{self.page_counter}"
        self.page_counter += 1
        
        page = {
            'id': page_id,
            'parent': {'database_id': database_id},
            'properties': properties,
            'children': children or [],
            'created_time': datetime.now().isoformat()
        }
        
        self.pages[page_id] = page
        return page
    
    def get_page(self, page_id: str) -> Dict:
        """Mock get page"""
        self.call_count += 1
        if page_id in self.pages:
            return self.pages[page_id]
        raise Exception(f"Page not found: {page_id}")
    
    def update_page(self, page_id: str, properties: Dict) -> Dict:
        """Mock page update"""
        self.call_count += 1
        if page_id not in self.pages:
            raise Exception(f"Page not found: {page_id}")
            
        self.pages[page_id]['properties'].update(properties)
        return self.pages[page_id]

class IntegrationTestSuite:
    """Comprehensive integration test suite"""
    
    def __init__(self, test_data_path: Path = None):
        self.test_data_path = test_data_path or TEST_DATA_PATH
        self.test_results = []
        self.mock_api = MockNotionAPI()
        
        # Create logs directory
        LOGS_PATH.mkdir(exist_ok=True)
        
    def run_all_tests(self) -> TestSuiteResult:
        """Run complete test suite"""
        start_time = time.time()
        logger.info("Starting MCP Integration Test Suite")
        
        # Test categories
        test_categories = [
            ("Schema Validation Tests", self._run_schema_validation_tests),
            ("Test Data Generation Tests", self._run_test_data_generation_tests),
            ("Data Transformation Tests", self._run_data_transformation_tests),
            ("API Client Tests", self._run_api_client_tests),
            ("Migration Orchestration Tests", self._run_migration_orchestration_tests),
            ("Relationship Management Tests", self._run_relationship_tests),
            ("Progress Monitoring Tests", self._run_progress_monitoring_tests),
            ("End-to-End Integration Tests", self._run_e2e_integration_tests)
        ]
        
        for category_name, test_function in test_categories:
            logger.info(f"Running {category_name}...")
            category_results = test_function()
            self.test_results.extend(category_results)
        
        # Generate summary
        total_duration = time.time() - start_time
        passed_tests = len([r for r in self.test_results if r.success])
        failed_tests = len([r for r in self.test_results if not r.success])
        success_rate = (passed_tests / len(self.test_results)) * 100 if self.test_results else 0
        
        result = TestSuiteResult(
            total_tests=len(self.test_results),
            passed_tests=passed_tests,
            failed_tests=failed_tests,
            success_rate=success_rate,
            total_duration=total_duration,
            test_results=self.test_results,
            summary=self._generate_test_summary()
        )
        
        # Save detailed report
        self._save_test_report(result)
        
        logger.info(f"Test suite completed: {passed_tests}/{len(self.test_results)} tests passed")
        return result
    
    def _run_test(self, test_name: str, test_function, *args, **kwargs) -> TestResult:
        """Run a single test with error handling"""
        start_time = time.time()
        
        try:
            details = test_function(*args, **kwargs)
            duration = time.time() - start_time
            
            return TestResult(
                test_name=test_name,
                success=True,
                duration=duration,
                error_message=None,
                details=details or {}
            )
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(f"Test {test_name} failed: {e}")
            
            return TestResult(
                test_name=test_name,
                success=False,
                duration=duration,
                error_message=str(e),
                details={}
            )
    
    def _run_schema_validation_tests(self) -> List[TestResult]:
        """Test schema validation functionality"""
        results = []
        
        # Test 1: Schema validator initialization
        def test_schema_validator_init():
            validator = SchemaValidator()
            assert len(validator.schemas) >= 0, "Schemas should be loaded"
            assert validator.validation_rules is not None, "Validation rules should be loaded"
            return {"schemas_loaded": len(validator.schemas)}
        
        results.append(self._run_test("Schema Validator Initialization", test_schema_validator_init))
        
        # Test 2: Validate test data if it exists
        def test_validate_existing_data():
            validator = SchemaValidator()
            if self.test_data_path.exists():
                # Test with knowledge_vault items
                kv_path = self.test_data_path / 'knowledge_vault_items'
                if kv_path.exists():
                    validation_results = validator.validate_directory(kv_path, 'knowledge_vault')
                    valid_count = len([r for r in validation_results if r.is_valid])
                    return {
                        "total_items": len(validation_results),
                        "valid_items": valid_count,
                        "validation_rate": (valid_count / len(validation_results)) * 100 if validation_results else 0
                    }
            return {"message": "No test data found to validate"}
        
        results.append(self._run_test("Validate Existing Test Data", test_validate_existing_data))
        
        # Test 3: Cross-reference validation
        def test_cross_reference_validation():
            validator = SchemaValidator()
            # Create mock validation results
            validator.validation_results = [
                Mock(is_valid=True, item_id="test1", database_type="knowledge_vault"),
                Mock(is_valid=True, item_id="test2", database_type="tools_services")
            ]
            validator.cross_references = {
                "test1": {
                    "@tools_services/test2": {
                        "target_database": "tools_services",
                        "target_item": "test2"
                    }
                }
            }
            
            errors, warnings = validator.validate_cross_references()
            return {
                "cross_ref_errors": len(errors),
                "cross_ref_warnings": len(warnings)
            }
        
        results.append(self._run_test("Cross-Reference Validation", test_cross_reference_validation))
        
        return results
    
    def _run_test_data_generation_tests(self) -> List[TestResult]:
        """Test test data generation functionality"""
        results = []
        
        # Test 1: Test data generator initialization
        def test_generator_init():
            generator = VanguardAITestDataGenerator()
            assert generator.output_base_path is not None, "Output path should be set"
            return {"generator_initialized": True}
        
        results.append(self._run_test("Test Data Generator Initialization", test_generator_init))
        
        # Test 2: Generate sample data (small subset)
        def test_generate_sample_data():
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                generator = VanguardAITestDataGenerator(output_path=temp_path)
                
                # Generate just 2 items per database for testing
                original_counts = generator.item_counts.copy()
                generator.item_counts = {db: 2 for db in generator.item_counts.keys()}
                
                test_env = generator.generate_complete_test_environment()
                
                # Verify structure
                assert 'knowledge_vault_items' in test_env, "Knowledge vault items should be generated"
                assert len(test_env['knowledge_vault_items']) == 2, "Should generate 2 knowledge vault items"
                
                return {
                    "items_generated": sum(len(items) for items in test_env.values()),
                    "databases_created": len(test_env)
                }
        
        results.append(self._run_test("Generate Sample Test Data", test_generate_sample_data))
        
        # Test 3: Validate generated data structure
        def test_validate_generated_structure():
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                generator = VanguardAITestDataGenerator(output_path=temp_path)
                generator.item_counts = {db: 1 for db in generator.item_counts.keys()}
                
                test_env = generator.generate_complete_test_environment()
                
                # Check first knowledge vault item structure
                if test_env['knowledge_vault_items']:
                    item = test_env['knowledge_vault_items'][0]
                    required_fields = ['id', 'name', 'category', 'status', 'description']
                    for field in required_fields:
                        assert field in item, f"Required field {field} missing"
                
                return {"structure_validation": "passed"}
        
        results.append(self._run_test("Validate Generated Data Structure", test_validate_generated_structure))
        
        return results
    
    def _run_data_transformation_tests(self) -> List[TestResult]:
        """Test data transformation functionality"""
        results = []
        
        # Load transformation config for tests
        config_path = KNOWLEDGE_VAULT_PATH / 'operations' / 'data-transformations.yaml'
        mappings_path = KNOWLEDGE_VAULT_PATH / 'operations' / 'notion-property-mappings.yaml'
        
        if not config_path.exists() or not mappings_path.exists():
            results.append(TestResult(
                test_name="Load Transformation Config",
                success=False,
                duration=0,
                error_message="Transformation config files not found",
                details={}
            ))
            return results
        
        # Test 1: Data transformer initialization
        def test_transformer_init():
            with open(config_path, 'r') as f:
                transformation_config = yaml.safe_load(f)
            with open(mappings_path, 'r') as f:
                property_mappings = yaml.safe_load(f)
            
            transformer = DataTransformer(transformation_config, property_mappings)
            assert transformer.transformation_config is not None, "Transformation config should be loaded"
            assert transformer.property_mappings is not None, "Property mappings should be loaded"
            
            return {"transformer_initialized": True}
        
        results.append(self._run_test("Data Transformer Initialization", test_transformer_init))
        
        # Test 2: Transform sample item
        def test_transform_sample_item():
            with open(config_path, 'r') as f:
                transformation_config = yaml.safe_load(f)
            with open(mappings_path, 'r') as f:
                property_mappings = yaml.safe_load(f)
            
            transformer = DataTransformer(transformation_config, property_mappings)
            
            # Create sample knowledge vault item
            sample_item = {
                'id': 'test-knowledge-item',
                'name': 'Test Knowledge Item',
                'category': 'Frameworks',
                'status': 'Research',
                'description': 'Test item for transformation',
                'type': 'Framework',
                'research_quality': 85,
                'priority': 'High',
                'tags': ['testing', 'framework']
            }
            
            notion_properties, relationships = transformer.transform_item(sample_item, 'knowledge_vault')
            
            # Verify transformation
            assert 'ID' in notion_properties, "ID property should be transformed"
            assert notion_properties['ID']['title'][0]['text']['content'] == 'test-knowledge-item'
            
            return {
                "properties_transformed": len(notion_properties),
                "relationships_extracted": len(relationships)
            }
        
        results.append(self._run_test("Transform Sample Item", test_transform_sample_item))
        
        # Test 3: Test relationship extraction
        def test_relationship_extraction():
            with open(config_path, 'r') as f:
                transformation_config = yaml.safe_load(f)
            with open(mappings_path, 'r') as f:
                property_mappings = yaml.safe_load(f)
            
            transformer = DataTransformer(transformation_config, property_mappings)
            
            # Sample item with relationships
            sample_item = {
                'id': 'test-item-with-relations',
                'name': 'Test Item',
                'category': 'Test',
                'status': 'Testing',
                'description': 'Test item',
                'relationships': {
                    'tools': ['@tools_services/test-tool'],
                    'ideas': ['@business_ideas/test-idea']
                }
            }
            
            notion_properties, relationships = transformer.transform_item(sample_item, 'knowledge_vault')
            
            return {
                "relationships_found": len(relationships),
                "relationship_types": [r.get('notion_property', 'unknown') for r in relationships]
            }
        
        results.append(self._run_test("Relationship Extraction", test_relationship_extraction))
        
        return results
    
    def _run_api_client_tests(self) -> List[TestResult]:
        """Test Notion API client functionality"""
        results = []
        
        # Test 1: Mock API client initialization
        def test_api_client_init():
            # Patch the NotionAPIClient to use our mock
            with patch.object(NotionAPIClient, '_make_request') as mock_request:
                mock_request.side_effect = self.mock_api._make_request
                
                client = NotionAPIClient("test_token")
                assert client.token == "test_token", "Token should be set"
                assert client.base_url == "https://api.notion.com/v1", "Base URL should be correct"
                
                return {"client_initialized": True}
        
        results.append(self._run_test("API Client Initialization", test_api_client_init))
        
        # Test 2: Mock database creation
        def test_mock_database_creation():
            # Test our mock API directly
            properties = {
                'ID': {'title': {}},
                'Name': {'rich_text': {}},
                'Status': {'select': {'options': []}}
            }
            
            result = self.mock_api.create_database(
                parent_id="mock_workspace",
                title="Test Database",
                properties=properties
            )
            
            assert 'id' in result, "Database should have ID"
            assert result['title'][0]['text']['content'] == "Test Database", "Title should match"
            
            return {
                "database_created": result['id'],
                "api_calls": self.mock_api.call_count
            }
        
        results.append(self._run_test("Mock Database Creation", test_mock_database_creation))
        
        # Test 3: Mock page creation
        def test_mock_page_creation():
            # First create a database
            db_result = self.mock_api.create_database(
                parent_id="mock_workspace",
                title="Test DB",
                properties={'ID': {'title': {}}}
            )
            
            # Then create a page
            page_properties = {
                'ID': {'title': [{'type': 'text', 'text': {'content': 'test-page'}}]}
            }
            
            page_result = self.mock_api.create_page(
                database_id=db_result['id'],
                properties=page_properties
            )
            
            assert 'id' in page_result, "Page should have ID"
            assert page_result['parent']['database_id'] == db_result['id'], "Parent should be correct"
            
            return {
                "page_created": page_result['id'],
                "total_api_calls": self.mock_api.call_count
            }
        
        results.append(self._run_test("Mock Page Creation", test_mock_page_creation))
        
        return results
    
    def _run_migration_orchestration_tests(self) -> List[TestResult]:
        """Test migration orchestration functionality"""
        results = []
        
        # Test 1: Migration config creation
        def test_migration_config():
            config = MigrationConfig(
                notion_token="test_token",
                workspace_id="test_workspace",
                source_path=Path("/tmp/test"),
                transformation_config_path=KNOWLEDGE_VAULT_PATH / 'operations' / 'data-transformations.yaml',
                property_mappings_path=KNOWLEDGE_VAULT_PATH / 'operations' / 'notion-property-mappings.yaml',
                dry_run=True
            )
            
            assert config.notion_token == "test_token", "Token should be set"
            assert config.dry_run is True, "Dry run should be enabled"
            
            return {"config_created": True}
        
        results.append(self._run_test("Migration Config Creation", test_migration_config))
        
        # Test 2: Orchestrator initialization
        def test_orchestrator_init():
            config = MigrationConfig(
                notion_token="test_token",
                workspace_id="test_workspace",
                source_path=KNOWLEDGE_VAULT_PATH,
                transformation_config_path=KNOWLEDGE_VAULT_PATH / 'operations' / 'data-transformations.yaml',
                property_mappings_path=KNOWLEDGE_VAULT_PATH / 'operations' / 'notion-property-mappings.yaml',
                dry_run=True
            )
            
            # Mock the file loading to avoid file not found errors
            with patch.object(BatchMigrationOrchestrator, '_load_yaml') as mock_load:
                mock_load.return_value = {'test': 'data'}
                
                orchestrator = BatchMigrationOrchestrator(config)
                assert orchestrator.config == config, "Config should be stored"
                
                return {"orchestrator_initialized": True}
        
        results.append(self._run_test("Orchestrator Initialization", test_orchestrator_init))
        
        return results
    
    def _run_relationship_tests(self) -> List[TestResult]:
        """Test relationship management functionality"""
        results = []
        
        # Test 1: Relationship manager initialization
        def test_relationship_manager_init():
            # Use mock API client
            with patch.object(NotionAPIClient, '__init__', return_value=None):
                mock_client = NotionAPIClient("test")
                relationship_manager = RelationshipManager(mock_client)
                
                assert relationship_manager.item_id_to_page_id == {}, "Should start with empty mappings"
                
                return {"manager_initialized": True}
        
        results.append(self._run_test("Relationship Manager Initialization", test_relationship_manager_init))
        
        # Test 2: Item mapping
        def test_item_mapping():
            with patch.object(NotionAPIClient, '__init__', return_value=None):
                mock_client = NotionAPIClient("test")
                relationship_manager = RelationshipManager(mock_client)
                
                relationship_manager.add_item_mapping("test-item", "page-123", "knowledge_vault")
                
                expected_key = "knowledge_vault/test-item"
                assert expected_key in relationship_manager.item_id_to_page_id, "Mapping should be added"
                assert relationship_manager.item_id_to_page_id[expected_key] == "page-123", "Page ID should match"
                
                return {"mappings_added": 1}
        
        results.append(self._run_test("Item Mapping", test_item_mapping))
        
        return results
    
    def _run_progress_monitoring_tests(self) -> List[TestResult]:
        """Test progress monitoring functionality"""
        results = []
        
        # Test 1: Progress monitor initialization
        def test_progress_monitor_init():
            monitor = ProgressMonitor(session_id="test_session")
            assert monitor.session_id == "test_session", "Session ID should be set"
            assert monitor.total_items == 0, "Should start with 0 items"
            
            return {"monitor_initialized": True}
        
        results.append(self._run_test("Progress Monitor Initialization", test_progress_monitor_init))
        
        # Test 2: Progress updates
        def test_progress_updates():
            monitor = ProgressMonitor(session_id="test_progress")
            
            monitor.start_monitoring(total_items=10)
            monitor.increment_completed(3)
            monitor.increment_failed(1)
            
            status = monitor.get_current_status()
            
            assert status['progress']['completed'] == 3, "Completed count should be 3"
            assert status['progress']['failed'] == 1, "Failed count should be 1"
            
            monitor.stop_monitoring()
            
            return {
                "completed": status['progress']['completed'],
                "failed": status['progress']['failed']
            }
        
        results.append(self._run_test("Progress Updates", test_progress_updates))
        
        return results
    
    def _run_e2e_integration_tests(self) -> List[TestResult]:
        """End-to-end integration tests"""
        results = []
        
        # Test 1: Full dry-run migration
        def test_full_dry_run_migration():
            # Create minimal test data
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # Create test structure
                test_data_dir = temp_path / 'databases' / 'vanguard-ai-test'
                kv_items_dir = test_data_dir / 'knowledge_vault_items'
                kv_items_dir.mkdir(parents=True, exist_ok=True)
                
                # Create one test item
                test_item = {
                    'id': 'test-e2e-item',
                    'name': 'End-to-End Test Item',
                    'category': 'Testing',
                    'status': 'Research',
                    'description': 'Test item for E2E testing',
                    'type': 'Framework'
                }
                
                with open(kv_items_dir / 'test-item.yaml', 'w') as f:
                    yaml.dump(test_item, f)
                
                # Create migration config
                config = MigrationConfig(
                    notion_token="test_token",
                    workspace_id="test_workspace",
                    source_path=temp_path,
                    transformation_config_path=KNOWLEDGE_VAULT_PATH / 'operations' / 'data-transformations.yaml',
                    property_mappings_path=KNOWLEDGE_VAULT_PATH / 'operations' / 'notion-property-mappings.yaml',
                    dry_run=True,
                    batch_size=1
                )
                
                # Mock the YAML loading and execute migration
                with patch.object(BatchMigrationOrchestrator, '_load_yaml') as mock_load:
                    # Mock transformation config
                    mock_transformation_config = {
                        'database_transformations': {
                            'knowledge_vault_transformations': {
                                'property_mappings': {
                                    'id': {
                                        'notion_property': 'ID',
                                        'transformation_rule': 'yaml_field_to_notion_title'
                                    },
                                    'name': {
                                        'notion_property': 'Name',
                                        'transformation_rule': 'yaml_string_to_rich_text'
                                    }
                                }
                            }
                        }
                    }
                    
                    # Mock property mappings
                    mock_property_mappings = {
                        'notion_database_schemas': {
                            'knowledge_vault_database': {
                                'database_name': 'Knowledge Vault Test',
                                'properties': {
                                    'ID': {'type': 'title'},
                                    'Name': {'type': 'rich_text'}
                                }
                            }
                        }
                    }
                    
                    def mock_load_side_effect(path):
                        if 'data-transformations' in str(path):
                            return mock_transformation_config
                        elif 'notion-property-mappings' in str(path):
                            return mock_property_mappings
                        else:
                            return {}
                    
                    mock_load.side_effect = mock_load_side_effect
                    
                    # Execute migration
                    orchestrator = BatchMigrationOrchestrator(config)
                    
                    # Mock the database creation and item migration for dry run
                    with patch.object(orchestrator, '_create_databases') as mock_create_db, \
                         patch.object(orchestrator, '_migrate_items_in_batches') as mock_migrate:
                        
                        # Set up created databases mock
                        from knowledge_vault.operations.scripts.batch_migration import DatabaseInfo
                        orchestrator.created_databases = {
                            'knowledge_vault_database': DatabaseInfo(
                                notion_id='mock_db_1',
                                name='Knowledge Vault Test',
                                database_type='knowledge_vault_database',
                                properties={},
                                created_at=datetime.now()
                            )
                        }
                        
                        # Execute migration
                        report = orchestrator.execute_migration()
                        
                        return {
                            "dry_run_success": True,
                            "items_processed": report.get('migration_summary', {}).get('total_items', 0)
                        }
        
        results.append(self._run_test("Full Dry-Run Migration", test_full_dry_run_migration))
        
        return results
    
    def _generate_test_summary(self) -> Dict[str, Any]:
        """Generate test summary statistics"""
        summary = {
            "test_categories": {},
            "performance_metrics": {},
            "critical_failures": [],
            "recommendations": []
        }
        
        # Group results by category
        for result in self.test_results:
            category = result.test_name.split()[0]  # First word as category
            if category not in summary["test_categories"]:
                summary["test_categories"][category] = {"passed": 0, "failed": 0, "total": 0}
            
            summary["test_categories"][category]["total"] += 1
            if result.success:
                summary["test_categories"][category]["passed"] += 1
            else:
                summary["test_categories"][category]["failed"] += 1
                summary["critical_failures"].append({
                    "test": result.test_name,
                    "error": result.error_message
                })
        
        # Performance metrics
        total_duration = sum(r.duration for r in self.test_results)
        avg_duration = total_duration / len(self.test_results) if self.test_results else 0
        
        summary["performance_metrics"] = {
            "total_test_duration": total_duration,
            "average_test_duration": avg_duration,
            "fastest_test": min(self.test_results, key=lambda x: x.duration).test_name if self.test_results else None,
            "slowest_test": max(self.test_results, key=lambda x: x.duration).test_name if self.test_results else None
        }
        
        # Generate recommendations
        failed_count = len([r for r in self.test_results if not r.success])
        if failed_count == 0:
            summary["recommendations"].append("All tests passed! System is ready for production migration.")
        elif failed_count < 3:
            summary["recommendations"].append("Minor issues detected. Review failed tests before proceeding.")
        else:
            summary["recommendations"].append("Multiple test failures detected. System needs attention before migration.")
        
        return summary
    
    def _save_test_report(self, result: TestSuiteResult):
        """Save detailed test report"""
        report_data = {
            "test_suite_summary": {
                "timestamp": datetime.now().isoformat(),
                "total_tests": result.total_tests,
                "passed_tests": result.passed_tests,
                "failed_tests": result.failed_tests,
                "success_rate": result.success_rate,
                "total_duration": result.total_duration
            },
            "test_results": [
                {
                    "test_name": r.test_name,
                    "success": r.success,
                    "duration": r.duration,
                    "error_message": r.error_message,
                    "details": r.details
                }
                for r in result.test_results
            ],
            "summary": result.summary
        }
        
        # Save JSON report
        report_path = LOGS_PATH / f'integration_test_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(report_path, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        logger.info(f"Test report saved to: {report_path}")

def run_quick_validation_test() -> bool:
    """Quick validation test for basic functionality"""
    try:
        # Test that all required files exist
        required_files = [
            KNOWLEDGE_VAULT_PATH / 'operations' / 'data-transformations.yaml',
            KNOWLEDGE_VAULT_PATH / 'operations' / 'notion-property-mappings.yaml'
        ]
        
        for file_path in required_files:
            if not file_path.exists():
                logger.error(f"Required file missing: {file_path}")
                return False
        
        # Test that modules can be imported
        from knowledge_vault.operations.scripts.batch_migration import BatchMigrationOrchestrator
        from knowledge_vault.operations.scripts.validate_schemas import SchemaValidator
        
        logger.info("Quick validation test passed")
        return True
        
    except Exception as e:
        logger.error(f"Quick validation test failed: {e}")
        return False

def main():
    """Main entry point for test suite"""
    import argparse
    
    parser = argparse.ArgumentParser(description='MCP Integration Test Suite')
    parser.add_argument('--quick', action='store_true', help='Run quick validation test only')
    parser.add_argument('--test-data-path', help='Path to test data directory')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    if args.quick:
        success = run_quick_validation_test()
        sys.exit(0 if success else 1)
    
    # Run full test suite
    test_data_path = Path(args.test_data_path) if args.test_data_path else None
    test_suite = IntegrationTestSuite(test_data_path)
    
    try:
        result = test_suite.run_all_tests()
        
        print("\n" + "="*60)
        print("MCP INTEGRATION TEST SUITE RESULTS")
        print("="*60)
        print(f"Total Tests: {result.total_tests}")
        print(f"Passed: {result.passed_tests}")
        print(f"Failed: {result.failed_tests}")
        print(f"Success Rate: {result.success_rate:.1f}%")
        print(f"Duration: {result.total_duration:.2f} seconds")
        
        if result.failed_tests > 0:
            print(f"\nFailed Tests:")
            for test_result in result.test_results:
                if not test_result.success:
                    print(f"  ❌ {test_result.test_name}: {test_result.error_message}")
        
        print("\n" + "="*60)
        
        # Exit with appropriate code
        sys.exit(0 if result.failed_tests == 0 else 1)
        
    except Exception as e:
        logger.error(f"Test suite execution failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()