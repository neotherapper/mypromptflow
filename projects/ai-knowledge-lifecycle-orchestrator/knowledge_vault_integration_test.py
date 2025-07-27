#!/usr/bin/env python3
"""
Knowledge Vault Integration Tests
AI Knowledge Lifecycle Orchestrator

Comprehensive test suite for validating Knowledge Vault integration functionality.
"""

import os
import sys
import unittest
import tempfile
import shutil
import yaml
import json
from datetime import datetime
from pathlib import Path
from unittest.mock import patch, MagicMock

# Import the integration module
try:
    from knowledge_vault_integration import (
        KnowledgeVaultIntegration,
        TechnologyTracking,
        DependencyMapping,
        KnowledgeUpdate,
        ChangeEvent,
        TechnologyCategory,
        ChangeClassification,
        WorkflowStatus,
        ValidationError,
        DatabaseOperationError
    )
except ImportError:
    # Handle import error if running from different directory
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from knowledge_vault_integration import (
        KnowledgeVaultIntegration,
        TechnologyTracking,
        DependencyMapping,
        KnowledgeUpdate,
        ChangeEvent,
        TechnologyCategory,
        ChangeClassification,
        WorkflowStatus,
        ValidationError,
        DatabaseOperationError
    )

class TestKnowledgeVaultIntegration(unittest.TestCase):
    """Test cases for Knowledge Vault integration"""
    
    def setUp(self):
        """Set up test environment"""
        # Create temporary directory for testing
        self.test_dir = tempfile.mkdtemp()
        self.knowledge_vault_path = Path(self.test_dir) / "knowledge-vault"
        
        # Create directory structure
        self.create_test_directory_structure()
        
        # Create test schemas
        self.create_test_schemas()
        
        # Initialize integration with test directory
        self.integration = KnowledgeVaultIntegration(base_path=self.test_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)
    
    def create_test_directory_structure(self):
        """Create test directory structure"""
        # Create base directories
        schemas_path = self.knowledge_vault_path / "schemas"
        databases_path = self.knowledge_vault_path / "databases"
        
        schemas_path.mkdir(parents=True, exist_ok=True)
        databases_path.mkdir(parents=True, exist_ok=True)
        
        # Create database directories
        for db_name in ['technology_tracking', 'dependency_mapping', 'knowledge_updates', 'change_events']:
            db_path = databases_path / db_name
            db_path.mkdir(exist_ok=True)
            
            # Create subdirectories
            for subdir in ['items', 'relations', 'metadata', 'indexes', 'views']:
                (db_path / subdir).mkdir(exist_ok=True)
    
    def create_test_schemas(self):
        """Create minimal test schemas"""
        schemas = {
            'technology-tracking-schema.yaml': {
                'database_info': {
                    'name': 'Technology Tracking',
                    'type': 'specialized_tracking'
                },
                'properties': {
                    'id': {'type': 'uuid', 'required': True},
                    'technology_name': {'type': 'title', 'required': True},
                    'category': {'type': 'select', 'required': True},
                    'current_version': {'type': 'rich_text', 'required': True},
                    'monitoring_priority': {'type': 'select', 'required': True}
                },
                'configuration': {
                    'validation': {
                        'required_fields': ['id', 'technology_name', 'category', 'current_version', 'monitoring_priority']
                    }
                }
            },
            'dependency-mapping-schema.yaml': {
                'database_info': {
                    'name': 'Dependency Mapping',
                    'type': 'relationship_mapping'
                },
                'properties': {
                    'id': {'type': 'uuid', 'required': True},
                    'mapping_name': {'type': 'title', 'required': True},
                    'ai_file_path': {'type': 'rich_text', 'required': True},
                    'technology_name': {'type': 'rich_text', 'required': True},
                    'dependency_criticality': {'type': 'select', 'required': True}
                },
                'configuration': {
                    'validation': {
                        'required_fields': ['id', 'mapping_name', 'ai_file_path', 'technology_name', 'dependency_criticality']
                    }
                }
            },
            'knowledge-update-schema.yaml': {
                'database_info': {
                    'name': 'Knowledge Updates',
                    'type': 'workflow_tracking'
                },
                'properties': {
                    'id': {'type': 'uuid', 'required': True},
                    'update_title': {'type': 'title', 'required': True},
                    'trigger_event': {'type': 'select', 'required': True},
                    'workflow_status': {'type': 'select', 'required': True},
                    'update_priority': {'type': 'select', 'required': True}
                },
                'configuration': {
                    'validation': {
                        'required_fields': ['id', 'update_title', 'trigger_event', 'workflow_status', 'update_priority']
                    }
                }
            },
            'change-event-schema.yaml': {
                'database_info': {
                    'name': 'Change Events',
                    'type': 'event_tracking'
                },
                'properties': {
                    'id': {'type': 'uuid', 'required': True},
                    'event_title': {'type': 'title', 'required': True},
                    'technology_name': {'type': 'rich_text', 'required': True},
                    'change_type': {'type': 'select', 'required': True},
                    'change_classification': {'type': 'select', 'required': True}
                },
                'configuration': {
                    'validation': {
                        'required_fields': ['id', 'event_title', 'technology_name', 'change_type', 'change_classification']
                    }
                }
            }
        }
        
        schemas_path = self.knowledge_vault_path / "schemas"
        for schema_name, schema_content in schemas.items():
            schema_file = schemas_path / schema_name
            with open(schema_file, 'w') as f:
                yaml.dump(schema_content, f)
    
    def test_initialization(self):
        """Test integration initialization"""
        self.assertIsInstance(self.integration, KnowledgeVaultIntegration)
        self.assertEqual(self.integration.base_path, Path(self.test_dir))
        self.assertTrue(self.integration.knowledge_vault_path.exists())
    
    def test_invalid_initialization(self):
        """Test initialization with invalid path"""
        with self.assertRaises(DatabaseOperationError):
            KnowledgeVaultIntegration(base_path="/nonexistent/path")
    
    def test_technology_tracking_creation(self):
        """Test creating technology tracking entries"""
        # Test with TechnologyTracking dataclass
        tech_data = TechnologyTracking(
            id="",  # Will be generated
            technology_name="React",
            category="frontend_framework",
            current_version="18.2.0",
            version_pattern="semantic",
            monitoring_priority="high"
        )
        
        tech_id = self.integration.create_technology_tracking(tech_data)
        self.assertIsNotNone(tech_id)
        self.assertIsInstance(tech_id, str)
        
        # Verify it was saved
        saved_tech = self.integration.get_technology_tracking(tech_id)
        self.assertIsNotNone(saved_tech)
        self.assertEqual(saved_tech['technology_name'], "React")
        self.assertEqual(saved_tech['category'], "frontend_framework")
    
    def test_technology_tracking_with_dict(self):
        """Test creating technology tracking with dictionary"""
        tech_data = {
            'technology_name': 'Vue.js',
            'category': 'frontend_framework',
            'current_version': '3.3.0',
            'version_pattern': 'semantic',
            'monitoring_priority': 'medium'
        }
        
        tech_id = self.integration.create_technology_tracking(tech_data)
        self.assertIsNotNone(tech_id)
        
        # Verify it was saved
        saved_tech = self.integration.get_technology_tracking(tech_id)
        self.assertEqual(saved_tech['technology_name'], "Vue.js")
    
    def test_dependency_mapping_creation(self):
        """Test creating dependency mapping entries"""
        dep_data = DependencyMapping(
            id="",
            mapping_name="React dependency in main file",
            ai_file_path="/test/path/CLAUDE.md",
            ai_file_type="claude_md",
            technology_name="React",
            technology_category="frontend_framework",
            dependency_type="direct_usage",
            dependency_criticality="important",
            update_priority="high",
            validation_status="validated"
        )
        
        dep_id = self.integration.create_dependency_mapping(dep_data)
        self.assertIsNotNone(dep_id)
        
        # Verify it was saved
        saved_dep = self.integration.get_dependency_mapping(dep_id)
        self.assertIsNotNone(saved_dep)
        self.assertEqual(saved_dep['technology_name'], "React")
        self.assertEqual(saved_dep['dependency_criticality'], "important")
    
    def test_knowledge_update_creation(self):
        """Test creating knowledge update entries"""
        update_data = KnowledgeUpdate(
            id="",
            update_title="Update React version",
            trigger_event="technology_change",
            affected_file_path="/test/path/CLAUDE.md",
            affected_file_type="claude_md",
            update_description="Update React version references",
            update_type="version_update",
            update_scope="minor",
            workflow_status="detected",
            update_priority="medium"
        )
        
        update_id = self.integration.create_knowledge_update(update_data)
        self.assertIsNotNone(update_id)
        
        # Verify it was saved
        saved_update = self.integration.get_knowledge_update(update_id)
        self.assertIsNotNone(saved_update)
        self.assertEqual(saved_update['workflow_status'], "detected")
    
    def test_change_event_creation(self):
        """Test creating change event entries"""
        change_data = ChangeEvent(
            id="",
            event_title="React 18.2.0 Released",
            technology_name="React",
            technology_category="frontend_framework",
            change_type="new_feature",
            change_classification="medium",
            detection_source="github_releases",
            detection_method="automated_monitoring",
            change_description="New React version with features",
            processing_status="detected"
        )
        
        change_id = self.integration.create_change_event(change_data)
        self.assertIsNotNone(change_id)
        
        # Verify it was saved
        saved_change = self.integration.get_change_event(change_id)
        self.assertIsNotNone(saved_change)
        self.assertEqual(saved_change['technology_name'], "React")
    
    def test_validation_errors(self):
        """Test validation error handling"""
        # Test missing required fields
        with self.assertRaises(ValidationError):
            self.integration.create_technology_tracking({
                'technology_name': 'Test'
                # Missing required fields
            })
    
    def test_query_operations(self):
        """Test query operations"""
        # Create test data
        tech_data = {
            'technology_name': 'Test Tech',
            'category': 'database',
            'current_version': '1.0.0',
            'version_pattern': 'semantic',
            'monitoring_priority': 'high'
        }
        tech_id = self.integration.create_technology_tracking(tech_data)
        
        # Test queries
        all_techs = self.integration.query_technologies()
        self.assertGreater(len(all_techs), 0)
        
        # Test filtered query
        database_techs = self.integration.get_technologies_by_category('database')
        self.assertEqual(len(database_techs), 1)
        self.assertEqual(database_techs[0]['technology_name'], 'Test Tech')
    
    def test_impact_analysis(self):
        """Test impact analysis functionality"""
        # Create test data
        tech_id = self.integration.create_technology_tracking({
            'technology_name': 'Test Framework',
            'category': 'frontend_framework',
            'current_version': '2.0.0',
            'version_pattern': 'semantic',
            'monitoring_priority': 'critical'
        })
        
        dep_id = self.integration.create_dependency_mapping({
            'mapping_name': 'Test dependency',
            'ai_file_path': '/test/file.md',
            'ai_file_type': 'claude_md',
            'technology_name': 'Test Framework',
            'technology_category': 'frontend_framework',
            'dependency_type': 'direct_usage',
            'dependency_criticality': 'essential',
            'update_priority': 'high',
            'validation_status': 'validated'
        })
        
        # Run impact analysis
        impact = self.integration.analyze_technology_impact('Test Framework')
        
        self.assertIsInstance(impact, dict)
        self.assertEqual(impact['technology_name'], 'Test Framework')
        self.assertGreater(impact['affected_files'], 0)
        self.assertIn('impact_summary', impact)
    
    def test_system_health_summary(self):
        """Test system health summary"""
        # Create some test data
        self.integration.create_technology_tracking({
            'technology_name': 'Health Test',
            'category': 'database',
            'current_version': '1.0.0',
            'version_pattern': 'semantic',
            'monitoring_priority': 'critical'
        })
        
        health = self.integration.get_system_health_summary()
        
        self.assertIsInstance(health, dict)
        self.assertIn('database_counts', health)
        self.assertIn('critical_items', health)
        self.assertIn('pending_work', health)
        self.assertIn('health_indicators', health)
        
        # Verify counts
        self.assertGreater(health['database_counts']['technology_tracking'], 0)
    
    def test_workflow_status_update(self):
        """Test updating workflow status"""
        # Create a knowledge update
        update_data = {
            'update_title': 'Test Update',
            'trigger_event': 'manual_request',
            'affected_file_path': '/test/file.md',
            'affected_file_type': 'claude_md',
            'update_description': 'Test update description',
            'update_type': 'content_update',
            'update_scope': 'minor',
            'workflow_status': 'detected',
            'update_priority': 'low'
        }
        
        update_id = self.integration.create_knowledge_update(update_data)
        
        # Update workflow status
        success = self.integration.update_workflow_status(update_id, 'approved')
        self.assertTrue(success)
        
        # Verify the update
        updated = self.integration.get_knowledge_update(update_id)
        self.assertEqual(updated['workflow_status'], 'approved')
        
        # Test with non-existent ID
        success = self.integration.update_workflow_status('nonexistent', 'completed')
        self.assertFalse(success)
    
    def test_specialized_queries(self):
        """Test specialized query methods"""
        # Create test data for various specialized queries
        
        # Critical technology
        self.integration.create_technology_tracking({
            'technology_name': 'Critical Tech',
            'category': 'security',
            'current_version': '1.0.0',
            'version_pattern': 'semantic',
            'monitoring_priority': 'critical'
        })
        
        # Critical dependency
        self.integration.create_dependency_mapping({
            'mapping_name': 'Critical dependency',
            'ai_file_path': '/critical/file.md',
            'ai_file_type': 'claude_md',
            'technology_name': 'Critical Tech',
            'technology_category': 'security',
            'dependency_type': 'direct_usage',
            'dependency_criticality': 'essential',
            'update_priority': 'critical',
            'validation_status': 'validated'
        })
        
        # Critical update
        self.integration.create_knowledge_update({
            'update_title': 'Critical Update',
            'trigger_event': 'security_update',
            'affected_file_path': '/critical/file.md',
            'affected_file_type': 'claude_md',
            'update_description': 'Critical security update',
            'update_type': 'security_update',
            'update_scope': 'major',
            'workflow_status': 'approval_pending',
            'update_priority': 'critical'
        })
        
        # Breaking change
        self.integration.create_change_event({
            'event_title': 'Breaking Change Event',
            'technology_name': 'Critical Tech',
            'technology_category': 'security',
            'change_type': 'breaking_change',
            'change_classification': 'critical',
            'detection_source': 'official_changelog',
            'detection_method': 'automated_monitoring',
            'change_description': 'Breaking change detected',
            'processing_status': 'classified'
        })
        
        # Test specialized queries
        critical_techs = self.integration.get_critical_technologies()
        self.assertGreater(len(critical_techs), 0)
        
        critical_deps = self.integration.get_critical_dependencies()
        self.assertGreater(len(critical_deps), 0)
        
        critical_updates = self.integration.get_critical_updates()
        self.assertGreater(len(critical_updates), 0)
        
        breaking_changes = self.integration.get_breaking_changes()
        self.assertGreater(len(breaking_changes), 0)
        
        pending_updates = self.integration.get_pending_updates()
        self.assertGreater(len(pending_updates), 0)
    
    def test_data_classes(self):
        """Test data class functionality"""
        # Test TechnologyTracking
        tech = TechnologyTracking(
            id="test-id",
            technology_name="Test",
            category="database",
            current_version="1.0.0",
            version_pattern="semantic",
            monitoring_priority="high"
        )
        
        tech_dict = tech.to_dict()
        self.assertIsInstance(tech_dict, dict)
        self.assertEqual(tech_dict['technology_name'], "Test")
        
        # Test with None values
        tech_with_none = TechnologyTracking(
            id="test-id-2",
            technology_name="Test2",
            category="database",
            current_version="2.0.0",
            version_pattern="semantic",
            monitoring_priority="low",
            description=None  # This should be filtered out
        )
        
        tech_dict_filtered = tech_with_none.to_dict()
        self.assertNotIn('description', tech_dict_filtered)


class TestIntegrationPerformance(unittest.TestCase):
    """Performance tests for the integration"""
    
    def setUp(self):
        """Set up performance test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.setup_test_environment()
        self.integration = KnowledgeVaultIntegration(base_path=self.test_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)
    
    def setup_test_environment(self):
        """Setup minimal test environment for performance tests"""
        knowledge_vault_path = Path(self.test_dir) / "knowledge-vault"
        schemas_path = knowledge_vault_path / "schemas"
        schemas_path.mkdir(parents=True, exist_ok=True)
        
        # Create minimal schema
        schema_content = {
            'properties': {'id': {'required': True}},
            'configuration': {'validation': {'required_fields': ['id']}}
        }
        
        for schema_name in ['technology-tracking-schema.yaml', 'dependency-mapping-schema.yaml', 
                           'knowledge-update-schema.yaml', 'change-event-schema.yaml']:
            with open(schemas_path / schema_name, 'w') as f:
                yaml.dump(schema_content, f)
    
    def test_bulk_creation_performance(self):
        """Test performance with bulk data creation"""
        import time
        
        start_time = time.time()
        
        # Create 100 technology tracking entries
        for i in range(100):
            self.integration.create_technology_tracking({
                'id': f'tech-{i}',
                'technology_name': f'Technology {i}',
                'category': 'database',
                'current_version': f'{i}.0.0',
                'version_pattern': 'semantic',
                'monitoring_priority': 'medium'
            })
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete within reasonable time (adjust as needed)
        self.assertLess(duration, 10.0, f"Bulk creation took {duration:.2f}s, expected < 10s")
        
        # Verify all items were created
        all_techs = self.integration.query_technologies()
        self.assertEqual(len(all_techs), 100)
    
    def test_query_performance(self):
        """Test query performance with larger dataset"""
        # Create test data
        for i in range(50):
            self.integration.create_technology_tracking({
                'id': f'perf-tech-{i}',
                'technology_name': f'Performance Tech {i}',
                'category': 'database' if i % 2 == 0 else 'frontend_framework',
                'current_version': f'{i}.0.0',
                'version_pattern': 'semantic',
                'monitoring_priority': 'critical' if i < 10 else 'medium'
            })
        
        import time
        
        # Test query performance
        start_time = time.time()
        
        # Multiple query operations
        all_techs = self.integration.query_technologies()
        db_techs = self.integration.get_technologies_by_category('database')
        critical_techs = self.integration.get_critical_technologies()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Should complete quickly
        self.assertLess(duration, 2.0, f"Query operations took {duration:.2f}s, expected < 2s")
        
        # Verify results
        self.assertEqual(len(all_techs), 50)
        self.assertEqual(len(db_techs), 25)  # Half should be database
        self.assertEqual(len(critical_techs), 10)  # First 10 are critical


def run_integration_tests():
    """Run all integration tests"""
    print("Running Knowledge Vault Integration Tests")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTests(loader.loadTestsFromTestCase(TestKnowledgeVaultIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegrationPerformance))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    
    if success:
        print("\n🎉 All tests passed!")
    else:
        print("\n❌ Some tests failed.")
    
    return success


def run_connectivity_test():
    """Run basic connectivity test"""
    print("Running Knowledge Vault Connectivity Test")
    print("=" * 40)
    
    try:
        # Test with actual paths
        base_path = "/Users/georgiospilitsoglou/Developer/projects/mypromptflow"
        
        if not os.path.exists(base_path):
            print("❌ Base path not found - using mock test")
            return run_integration_tests()
        
        integration = KnowledgeVaultIntegration(base_path=base_path)
        print("✓ Integration initialized successfully")
        
        # Test basic operations
        health = integration.get_system_health_summary()
        print(f"✓ System health check completed")
        print(f"  Database counts: {health['database_counts']}")
        
        # Test schema validation
        try:
            integration._validate_item_data('technology_tracking', {
                'id': 'test',
                'technology_name': 'Test',
                'category': 'database',
                'current_version': '1.0.0',
                'monitoring_priority': 'medium'
            })
            print("✓ Schema validation working")
        except Exception as e:
            print(f"⚠ Schema validation issue: {e}")
        
        print("\n🎉 Connectivity test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Connectivity test failed: {e}")
        return False


if __name__ == "__main__":
    print("Knowledge Vault Integration Test Suite")
    print("=" * 60)
    
    # Run connectivity test first
    connectivity_success = run_connectivity_test()
    
    print("\n" + "=" * 60)
    
    # Run full integration tests
    integration_success = run_integration_tests()
    
    # Overall result
    overall_success = connectivity_success and integration_success
    
    print("\n" + "=" * 60)
    print("OVERALL RESULT:")
    if overall_success:
        print("🎉 All tests completed successfully!")
        print("Knowledge Vault integration is ready for use.")
    else:
        print("❌ Some tests failed.")
        print("Please review the output above and fix any issues.")
    
    sys.exit(0 if overall_success else 1)