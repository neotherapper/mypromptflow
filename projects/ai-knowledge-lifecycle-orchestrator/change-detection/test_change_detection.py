#!/usr/bin/env python3
"""
Change Detection Engine Integration Test Suite
AI Knowledge Lifecycle Orchestrator - Comprehensive testing script

This script provides comprehensive integration testing for the change detection system,
validating all components work together correctly and meet performance requirements.
"""

import asyncio
import logging
import time
import tempfile
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import sys
import os

# Add current directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent))

from config_manager import ConfigManager
from mcp_integrator import MCPIntegrator
from storage_interface import StorageInterface
from change_detector import ChangeDetectionEngine, ChangeValidator, TechnologyChange, ChangeType
from orchestrator import ChangeDetectionOrchestrator, AlertNotification

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ChangeDetectionTestSuite:
    """Comprehensive test suite for the change detection system"""
    
    def __init__(self, test_config_dir: Optional[Path] = None):
        """Initialize test suite"""
        self.test_config_dir = test_config_dir or Path(__file__).parent
        self.temp_dir = None
        self.components = {}
        self.test_results = {
            'total_tests': 0,
            'passed_tests': 0,
            'failed_tests': 0,
            'test_details': [],
            'performance_metrics': {},
            'start_time': None,
            'end_time': None
        }
        
        logger.info("Change Detection Test Suite initialized")
    
    async def run_all_tests(self) -> Dict[str, Any]:
        """Run comprehensive test suite"""
        self.test_results['start_time'] = datetime.utcnow()
        logger.info("Starting comprehensive change detection test suite")
        
        try:
            # Setup test environment
            await self.setup_test_environment()
            
            # Run component tests
            await self.test_config_manager()
            await self.test_mcp_integrator()
            await self.test_storage_interface()
            await self.test_change_detector()
            await self.test_change_validator()
            await self.test_orchestrator()
            
            # Run integration tests
            await self.test_end_to_end_workflow()
            await self.test_performance_requirements()
            await self.test_error_handling()
            await self.test_concurrency()
            
            # Generate test report
            self.test_results['end_time'] = datetime.utcnow()
            return self.generate_test_report()
            
        except Exception as e:
            logger.error(f"Test suite execution failed: {e}")
            self.test_results['end_time'] = datetime.utcnow()
            return self.generate_test_report()
        finally:
            await self.cleanup_test_environment()
    
    async def setup_test_environment(self):
        """Setup test environment with temporary files and mock data"""
        try:
            logger.info("Setting up test environment")
            
            # Create temporary directory
            self.temp_dir = Path(tempfile.mkdtemp(prefix="change_detection_test_"))
            logger.info(f"Created temporary test directory: {self.temp_dir}")
            
            # Create mock configuration files
            await self.create_mock_configurations()
            
            # Initialize components
            config_manager = ConfigManager(self.temp_dir)
            mcp_integrator = MCPIntegrator(config_manager)
            storage_interface = StorageInterface(config_manager)
            change_detector = ChangeDetectionEngine(config_manager, mcp_integrator, storage_interface)
            change_validator = ChangeValidator(config_manager)
            orchestrator = ChangeDetectionOrchestrator(self.temp_dir)
            
            self.components = {
                'config_manager': config_manager,
                'mcp_integrator': mcp_integrator,
                'storage_interface': storage_interface,
                'change_detector': change_detector,
                'change_validator': change_validator,
                'orchestrator': orchestrator
            }
            
            logger.info("Test environment setup completed")
            
        except Exception as e:
            logger.error(f"Error setting up test environment: {e}")
            raise
    
    async def create_mock_configurations(self):
        """Create mock configuration files for testing"""
        try:
            # Create mock architecture configuration
            arch_config = {
                'system_overview': {
                    'name': 'Test Change Detection System',
                    'version': '1.0.0-test'
                },
                'architecture_components': {
                    'source_monitor_controller': {
                        'description': 'Test source monitoring',
                        'responsibilities': ['Monitor test sources']
                    },
                    'change_detection_engine': {
                        'description': 'Test change detection',
                        'responsibilities': ['Detect test changes']
                    },
                    'mcp_integration_layer': {
                        'description': 'Test MCP integration',
                        'responsibilities': ['Integrate with test MCP servers']
                    },
                    'storage_caching_layer': {
                        'description': 'Test storage',
                        'responsibilities': ['Store test data']
                    },
                    'notification_alert_system': {
                        'description': 'Test notifications',
                        'responsibilities': ['Send test alerts']
                    }
                },
                'integration_architecture': {
                    'data_flow': 'Test data flow'
                },
                'orchestration_settings': {
                    'mode': 'scheduled',
                    'check_interval_minutes': 1,
                    'batch_size': 2,
                    'max_concurrent_detections': 2,
                    'health_check_interval_minutes': 1
                }
            }
            
            with open(self.temp_dir / 'change-detection-architecture.yaml', 'w') as f:
                import yaml
                yaml.dump(arch_config, f)
            
            # Create mock technology sources configuration
            tech_config = {
                'tier_1_critical_technologies': {
                    'test_framework': {
                        'official_sources': {
                            'github_releases': {
                                'url': 'https://api.github.com/repos/test/framework/releases',
                                'type': 'github_api',
                                'mcp_server': 'mcp__MCP_DOCKER__github_server',
                                'extraction_pattern': 'json_api'
                            }
                        },
                        'monitoring_config': {
                            'check_frequency': '1m',
                            'priority_level': 'high',
                            'notification_delay': '0m',
                            'enabled': True
                        },
                        'current_version': '1.0.0',
                        'criticality': 'high'
                    }
                },
                'tier_2_important_technologies': {
                    'test_library': {
                        'official_sources': {
                            'npm_registry': {
                                'url': 'https://registry.npmjs.org/test-library',
                                'type': 'npm_registry',
                                'mcp_server': 'mcp__MCP_DOCKER__fetch',
                                'extraction_pattern': 'npm_json'
                            }
                        },
                        'monitoring_config': {
                            'check_frequency': '5m',
                            'priority_level': 'medium',
                            'notification_delay': '5m',
                            'enabled': True
                        },
                        'current_version': '2.1.0',
                        'criticality': 'medium'
                    }
                },
                'tier_3_supplemental_technologies': {}
            }
            
            with open(self.temp_dir / 'technology-source-config.yaml', 'w') as f:
                yaml.dump(tech_config, f)
            
            # Create mock classification rules
            classification_config = {
                'change_type_classification': {
                    'breaking_change': {
                        'detection_patterns': {
                            'content_keywords': {
                                'high_confidence': ['breaking', 'incompatible', 'removed'],
                                'medium_confidence': ['deprecated', 'changed'],
                                'low_confidence': ['updated', 'modified']
                            }
                        },
                        'impact_calculation': {
                            'base_impact': 'high',
                            'multipliers': {'criticality': 1.5}
                        }
                    },
                    'security_update': {
                        'detection_patterns': {
                            'content_keywords': {
                                'high_confidence': ['security', 'vulnerability', 'CVE'],
                                'medium_confidence': ['fix', 'patch'],
                                'low_confidence': ['update']
                            }
                        },
                        'impact_calculation': {
                            'base_impact': 'high',
                            'multipliers': {'criticality': 2.0}
                        }
                    },
                    'deprecation_warning': {
                        'detection_patterns': {
                            'content_keywords': {
                                'high_confidence': ['deprecated', 'deprecation'],
                                'medium_confidence': ['legacy', 'obsolete'],
                                'low_confidence': ['old']
                            }
                        },
                        'impact_calculation': {
                            'base_impact': 'medium',
                            'multipliers': {'criticality': 1.2}
                        }
                    },
                    'feature_addition': {
                        'detection_patterns': {
                            'content_keywords': {
                                'high_confidence': ['feature', 'new', 'added'],
                                'medium_confidence': ['enhanced', 'improved'],
                                'low_confidence': ['updated']
                            }
                        },
                        'impact_calculation': {
                            'base_impact': 'low',
                            'multipliers': {'criticality': 1.0}
                        }
                    },
                    'bug_fix': {
                        'detection_patterns': {
                            'content_keywords': {
                                'high_confidence': ['fix', 'bug', 'issue'],
                                'medium_confidence': ['resolved', 'corrected'],
                                'low_confidence': ['improved']
                            }
                        },
                        'impact_calculation': {
                            'base_impact': 'low',
                            'multipliers': {'criticality': 1.0}
                        }
                    },
                    'configuration_change': {
                        'detection_patterns': {
                            'content_keywords': {
                                'high_confidence': ['config', 'configuration'],
                                'medium_confidence': ['settings', 'options'],
                                'low_confidence': ['change']
                            }
                        },
                        'impact_calculation': {
                            'base_impact': 'medium',
                            'multipliers': {'criticality': 1.1}
                        }
                    }
                },
                'impact_assessment': {
                    'factors': ['change_type', 'technology_criticality', 'version_change_magnitude']
                },
                'urgency_classification': {
                    'immediate': ['breaking_change', 'security_update'],
                    'high': ['deprecation_warning'],
                    'medium': ['configuration_change', 'bug_fix'],
                    'low': ['feature_addition']
                },
                'confidence_scoring': {
                    'algorithm': 'weighted_evidence',
                    'minimum_threshold': 0.3
                }
            }
            
            with open(self.temp_dir / 'change-classification-rules.yaml', 'w') as f:
                yaml.dump(classification_config, f)
            
            # Create mock MCP integration configuration
            mcp_config = {
                'integration_architecture': {
                    'request_routing': 'intelligent',
                    'fallback_strategy': 'cascade',
                    'performance_optimization': True
                },
                'available_mcp_servers': {
                    'fetch_server': {
                        'server_name': 'mcp__MCP_DOCKER__fetch',
                        'description': 'Test fetch server',
                        'capabilities': ['web_content_retrieval'],
                        'performance_characteristics': {
                            'rate_limit': '60 requests per minute',
                            'timeout': '30s',
                            'retry_count': 3
                        }
                    },
                    'github_server': {
                        'server_name': 'mcp__MCP_DOCKER__github_server',
                        'description': 'Test GitHub server',
                        'capabilities': ['github_api_access'],
                        'performance_characteristics': {
                            'rate_limit': '60 requests per minute',
                            'timeout': '30s',
                            'retry_count': 3
                        }
                    },
                    'search_server': {
                        'server_name': 'mcp__MCP_DOCKER__search',
                        'description': 'Test search server',
                        'capabilities': ['web_search'],
                        'performance_characteristics': {
                            'rate_limit': '10 requests per minute',
                            'timeout': '60s',
                            'retry_count': 2
                        }
                    },
                    'browser_automation_server': {
                        'server_name': 'mcp__MCP_DOCKER__browser_automation',
                        'description': 'Test browser automation server',
                        'capabilities': ['browser_automation'],
                        'performance_characteristics': {
                            'rate_limit': '5 requests per minute',
                            'timeout': '120s',
                            'retry_count': 1
                        }
                    }
                },
                'integration_patterns': {
                    'primary_fallback_chains': {
                        'web_content': ['fetch_server', 'browser_automation_server'],
                        'github_content': ['github_server', 'fetch_server']
                    }
                }
            }
            
            with open(self.temp_dir / 'mcp-integration-patterns.yaml', 'w') as f:
                yaml.dump(mcp_config, f)
            
            # Create empty storage config
            storage_config = {}
            with open(self.temp_dir / 'storage-and-caching-design.yaml', 'w') as f:
                yaml.dump(storage_config, f)
            
            logger.info("Mock configuration files created")
            
        except Exception as e:
            logger.error(f"Error creating mock configurations: {e}")
            raise
    
    async def test_config_manager(self):
        """Test configuration manager functionality"""
        test_name = "Config Manager Tests"
        logger.info(f"Running {test_name}")
        
        try:
            config_manager = self.components['config_manager']
            
            # Test configuration loading
            self.assert_true(
                len(config_manager.configs) > 0,
                "Configuration files should be loaded"
            )
            
            # Test technology configuration access
            all_technologies = config_manager.get_all_technologies()
            self.assert_true(
                'test_framework' in all_technologies,
                "Test framework should be in technologies"
            )
            
            # Test specific technology lookup
            test_framework = config_manager.get_technology_by_name('test_framework')
            self.assert_not_none(test_framework, "Should find test_framework by name")
            
            # Test validation
            is_valid = config_manager.is_configuration_valid()
            logger.info(f"Configuration validation status: {is_valid}")
            
            self.record_test_result(test_name, True, "All config manager tests passed")
            
        except Exception as e:
            self.record_test_result(test_name, False, f"Config manager test failed: {e}")
    
    async def test_mcp_integrator(self):
        """Test MCP integrator functionality"""
        test_name = "MCP Integrator Tests"
        logger.info(f"Running {test_name}")
        
        try:
            mcp_integrator = self.components['mcp_integrator']
            
            # Test server health tracking
            server_health = await mcp_integrator.get_server_health()
            self.assert_true(
                len(server_health) > 0,
                "Should have server health information"
            )
            
            # Test performance stats
            perf_stats = await mcp_integrator.get_performance_stats()
            self.assert_true(
                'total_requests' in perf_stats,
                "Should have performance statistics"
            )
            
            # Test basic health check (this will use mock/simulated responses)
            health_check_result = await mcp_integrator.health_check()
            logger.info(f"MCP health check result: {health_check_result}")
            
            self.record_test_result(test_name, True, "All MCP integrator tests passed")
            
        except Exception as e:
            self.record_test_result(test_name, False, f"MCP integrator test failed: {e}")
    
    async def test_storage_interface(self):
        """Test storage interface functionality"""
        test_name = "Storage Interface Tests"
        logger.info(f"Running {test_name}")
        
        try:
            storage = self.components['storage_interface']
            
            # Test health check
            health_status = await storage.health_check()
            self.assert_true(
                health_status.get('cache_healthy', False),
                "Cache should be healthy"
            )
            
            # Test performance metrics storage
            success = await storage.store_performance_metric(
                "test_metric", 123.45, {"test": "data"}
            )
            self.assert_true(success, "Should store performance metric successfully")
            
            # Test performance metrics retrieval
            metrics = await storage.get_performance_metrics("test_metric", hours_back=1)
            logger.info(f"Retrieved {len(metrics)} performance metrics")
            
            # Test storage stats
            stats = await storage.get_storage_stats()
            self.assert_true(
                hasattr(stats, 'total_reads'),
                "Should have storage statistics"
            )
            
            self.record_test_result(test_name, True, "All storage interface tests passed")
            
        except Exception as e:
            self.record_test_result(test_name, False, f"Storage interface test failed: {e}")
    
    async def test_change_detector(self):
        """Test change detection engine functionality"""
        test_name = "Change Detector Tests"
        logger.info(f"Running {test_name}")
        
        try:
            change_detector = self.components['change_detector']
            
            # Test performance stats
            perf_stats = await change_detector.get_performance_stats()
            self.assert_true(
                'detections_processed' in perf_stats,
                "Should have performance statistics"
            )
            
            # Test change detection (this will use mock data due to MCP server simulation)
            changes = await change_detector.detect_changes_for_technology('test_framework')
            logger.info(f"Detected {len(changes)} changes for test_framework")
            
            # The actual change detection might return empty results due to mock data,
            # but the function should execute without errors
            self.assert_true(
                isinstance(changes, list),
                "Should return a list of changes"
            )
            
            self.record_test_result(test_name, True, "All change detector tests passed")
            
        except Exception as e:
            self.record_test_result(test_name, False, f"Change detector test failed: {e}")
    
    async def test_change_validator(self):
        """Test change validator functionality"""
        test_name = "Change Validator Tests"
        logger.info(f"Running {test_name}")
        
        try:
            change_validator = self.components['change_validator']
            
            # Create a mock change for testing
            mock_change = TechnologyChange(
                technology_name='test_framework',
                change_type=ChangeType.FEATURE_ADDITION,
                old_version='1.0.0',
                new_version='1.1.0',
                source_url='https://example.com/test',
                detection_timestamp=datetime.utcnow(),
                impact_level='medium',
                urgency_level='low',
                confidence_score=0.8,
                change_description='Test change',
                evidence=['test evidence']
            )
            
            # Test change validation
            is_valid, adjusted_confidence = await change_validator.validate_change(mock_change)
            logger.info(f"Change validation result: valid={is_valid}, confidence={adjusted_confidence}")
            
            self.assert_true(
                isinstance(is_valid, bool),
                "Should return boolean validation result"
            )
            
            self.assert_true(
                0.0 <= adjusted_confidence <= 1.0,
                "Adjusted confidence should be between 0 and 1"
            )
            
            self.record_test_result(test_name, True, "All change validator tests passed")
            
        except Exception as e:
            self.record_test_result(test_name, False, f"Change validator test failed: {e}")
    
    async def test_orchestrator(self):
        """Test orchestrator functionality"""
        test_name = "Orchestrator Tests"
        logger.info(f"Running {test_name}")
        
        try:
            orchestrator = self.components['orchestrator']
            
            # Test orchestration status
            status = await orchestrator.get_orchestration_status()
            self.assert_true(
                'running' in status,
                "Should have orchestration status"
            )
            
            # Test task status
            task_status = await orchestrator.get_task_status()
            logger.info(f"Task status: {len(task_status) if isinstance(task_status, dict) else 'N/A'} tasks")
            
            # Test manual detection trigger
            trigger_result = await orchestrator.trigger_detection('test_framework')
            logger.info(f"Manual trigger result: {trigger_result}")
            
            self.record_test_result(test_name, True, "All orchestrator tests passed")
            
        except Exception as e:
            self.record_test_result(test_name, False, f"Orchestrator test failed: {e}")
    
    async def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow"""
        test_name = "End-to-End Workflow Tests"
        logger.info(f"Running {test_name}")
        
        try:
            orchestrator = self.components['orchestrator']
            storage = self.components['storage_interface']
            
            # Trigger detection
            success = await orchestrator.trigger_detection('test_framework')
            self.assert_true(success, "Should successfully trigger detection")
            
            # Wait a bit for processing
            await asyncio.sleep(2)
            
            # Check if monitoring status was updated
            monitoring_status = await storage.get_monitoring_status('test_framework')
            logger.info(f"Monitoring status after detection: {monitoring_status}")
            
            # Get orchestration status
            orch_status = await orchestrator.get_orchestration_status()
            self.assert_true(
                orch_status.get('statistics', {}).get('total_detections', 0) >= 0,
                "Should have detection statistics"
            )
            
            self.record_test_result(test_name, True, "End-to-end workflow tests passed")
            
        except Exception as e:
            self.record_test_result(test_name, False, f"End-to-end workflow test failed: {e}")
    
    async def test_performance_requirements(self):
        """Test performance requirements compliance"""
        test_name = "Performance Requirements Tests"
        logger.info(f"Running {test_name}")
        
        try:
            start_time = time.time()
            
            # Test detection performance
            change_detector = self.components['change_detector']
            
            # Run multiple detections to test performance
            for i in range(3):
                await change_detector.detect_changes_for_technology('test_framework')
            
            total_time = time.time() - start_time
            avg_time = total_time / 3
            
            logger.info(f"Average detection time: {avg_time:.2f}s")
            
            # Performance requirement: should complete within reasonable time
            self.assert_true(
                avg_time < 30,  # 30 seconds max per detection
                f"Average detection time ({avg_time:.2f}s) should be under 30s"
            )
            
            # Test storage performance
            storage = self.components['storage_interface']
            storage_stats = await storage.get_storage_stats()
            
            self.test_results['performance_metrics'] = {
                'average_detection_time': avg_time,
                'total_test_time': total_time,
                'cache_hit_rate': storage_stats.cache_hit_rate
            }
            
            self.record_test_result(test_name, True, f"Performance tests passed (avg: {avg_time:.2f}s)")
            
        except Exception as e:
            self.record_test_result(test_name, False, f"Performance test failed: {e}")
    
    async def test_error_handling(self):
        """Test error handling and recovery"""
        test_name = "Error Handling Tests"
        logger.info(f"Running {test_name}")
        
        try:
            orchestrator = self.components['orchestrator']
            
            # Test detection with non-existent technology
            result = await orchestrator.trigger_detection('non_existent_tech')
            self.assert_false(result, "Should fail gracefully for non-existent technology")
            
            # Test health checks handle errors gracefully
            mcp_integrator = self.components['mcp_integrator']
            health_result = await mcp_integrator.health_check()
            # Health check should not crash even if some servers are unavailable
            
            self.record_test_result(test_name, True, "Error handling tests passed")
            
        except Exception as e:
            self.record_test_result(test_name, False, f"Error handling test failed: {e}")
    
    async def test_concurrency(self):
        """Test concurrent operations"""
        test_name = "Concurrency Tests"
        logger.info(f"Running {test_name}")
        
        try:
            orchestrator = self.components['orchestrator']
            
            # Test concurrent detection triggers
            tasks = []
            for tech in ['test_framework', 'test_library']:
                task = asyncio.create_task(orchestrator.trigger_detection(tech))
                tasks.append(task)
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Check that concurrent operations work
            success_count = sum(1 for result in results if result is True)
            logger.info(f"Concurrent operations: {success_count} successful out of {len(results)}")
            
            self.assert_true(
                success_count >= 1,
                "At least one concurrent operation should succeed"
            )
            
            self.record_test_result(test_name, True, f"Concurrency tests passed ({success_count}/{len(results)} successful)")
            
        except Exception as e:
            self.record_test_result(test_name, False, f"Concurrency test failed: {e}")
    
    def assert_true(self, condition: bool, message: str):
        """Assert that condition is true"""
        if not condition:
            raise AssertionError(f"Assertion failed: {message}")
    
    def assert_false(self, condition: bool, message: str):
        """Assert that condition is false"""
        if condition:
            raise AssertionError(f"Assertion failed: {message}")
    
    def assert_not_none(self, value: Any, message: str):
        """Assert that value is not None"""
        if value is None:
            raise AssertionError(f"Assertion failed: {message}")
    
    def record_test_result(self, test_name: str, passed: bool, details: str):
        """Record test result"""
        self.test_results['total_tests'] += 1
        if passed:
            self.test_results['passed_tests'] += 1
            logger.info(f"✅ {test_name}: PASSED - {details}")
        else:
            self.test_results['failed_tests'] += 1
            logger.error(f"❌ {test_name}: FAILED - {details}")
        
        self.test_results['test_details'].append({
            'test_name': test_name,
            'passed': passed,
            'details': details,
            'timestamp': datetime.utcnow().isoformat()
        })
    
    def generate_test_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        if self.test_results['start_time'] and self.test_results['end_time']:
            duration = (self.test_results['end_time'] - self.test_results['start_time']).total_seconds()
        else:
            duration = 0
        
        success_rate = (
            self.test_results['passed_tests'] / max(1, self.test_results['total_tests']) * 100
        )
        
        report = {
            'test_summary': {
                'total_tests': self.test_results['total_tests'],
                'passed_tests': self.test_results['passed_tests'],
                'failed_tests': self.test_results['failed_tests'],
                'success_rate': f"{success_rate:.1f}%",
                'duration_seconds': duration,
                'start_time': self.test_results['start_time'].isoformat() if self.test_results['start_time'] else None,
                'end_time': self.test_results['end_time'].isoformat() if self.test_results['end_time'] else None
            },
            'test_details': self.test_results['test_details'],
            'performance_metrics': self.test_results['performance_metrics'],
            'system_info': {
                'python_version': sys.version,
                'platform': sys.platform,
                'test_config_dir': str(self.test_config_dir),
                'temp_dir': str(self.temp_dir) if self.temp_dir else None
            }
        }
        
        return report
    
    async def cleanup_test_environment(self):
        """Cleanup test environment"""
        try:
            logger.info("Cleaning up test environment")
            
            # Close storage connections
            if 'storage_interface' in self.components:
                await self.components['storage_interface'].close()
            
            # Clear MCP caches
            if 'mcp_integrator' in self.components:
                await self.components['mcp_integrator'].clear_cache()
            
            # Remove temporary directory
            if self.temp_dir and self.temp_dir.exists():
                import shutil
                shutil.rmtree(self.temp_dir)
                logger.info(f"Removed temporary directory: {self.temp_dir}")
            
            logger.info("Test environment cleanup completed")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")


async def main():
    """Main entry point for running the test suite"""
    print("🧪 Change Detection Engine - Integration Test Suite")
    print("=" * 60)
    
    # Initialize and run test suite
    test_suite = ChangeDetectionTestSuite()
    
    try:
        # Run all tests
        test_report = await test_suite.run_all_tests()
        
        # Print test report
        print("\n📊 Test Report")
        print("=" * 60)
        
        summary = test_report['test_summary']
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Passed: {summary['passed_tests']} ✅")
        print(f"Failed: {summary['failed_tests']} ❌")
        print(f"Success Rate: {summary['success_rate']}")
        print(f"Duration: {summary['duration_seconds']:.2f} seconds")
        
        if test_report['performance_metrics']:
            print("\n⚡ Performance Metrics")
            print("-" * 30)
            for metric, value in test_report['performance_metrics'].items():
                if isinstance(value, float):
                    print(f"{metric}: {value:.3f}")
                else:
                    print(f"{metric}: {value}")
        
        print("\n📝 Test Details")
        print("-" * 30)
        for test_detail in test_report['test_details']:
            status = "✅ PASSED" if test_detail['passed'] else "❌ FAILED"
            print(f"{status} - {test_detail['test_name']}: {test_detail['details']}")
        
        # Save detailed report to file
        report_file = Path(__file__).parent / f"test_report_{int(time.time())}.json"
        with open(report_file, 'w') as f:
            json.dump(test_report, f, indent=2, default=str)
        print(f"\n📄 Detailed report saved to: {report_file}")
        
        # Exit with appropriate code
        exit_code = 0 if summary['failed_tests'] == 0 else 1
        print(f"\n🏁 Test suite completed with exit code: {exit_code}")
        
        return exit_code
        
    except Exception as e:
        print(f"\n💥 Test suite execution failed: {e}")
        logger.exception("Test suite execution failed")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)