#!/usr/bin/env python3
"""
Integration Test Suite
AI Knowledge Lifecycle Orchestrator - Validation Integration Testing

This script tests the complete integration between the update pipeline and
the AI Agent Instruction Design Excellence framework.
"""

import asyncio
import logging
import json
import tempfile
import os
from pathlib import Path
import sys

# Add the parent directory to the path to import modules
sys.path.append(str(Path(__file__).parent))

try:
    from .framework_connector import AIInstructionFrameworkConnector, ValidationType
    from .quality_monitor import QualityMonitor, MonitoringMode
    from .rollback_manager import RollbackManager
    from .validation_orchestrator import ValidationOrchestrator
except ImportError:
    from framework_connector import AIInstructionFrameworkConnector, ValidationType
    from quality_monitor import QualityMonitor, MonitoringMode
    from rollback_manager import RollbackManager
    from validation_orchestrator import ValidationOrchestrator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class IntegrationTestSuite:
    """Comprehensive integration test suite"""
    
    def __init__(self):
        self.test_results = {}
        self.components = {}
    
    async def run_all_tests(self):
        """Run all integration tests"""
        logger.info("Starting AI Agent Instruction Design Excellence integration tests")
        
        # Test 1: Component initialization
        await self.test_component_initialization()
        
        # Test 2: Framework connector validation
        await self.test_framework_connector()
        
        # Test 3: Quality monitoring
        await self.test_quality_monitoring()
        
        # Test 4: Rollback management
        await self.test_rollback_management()
        
        # Test 5: Validation orchestration
        await self.test_validation_orchestration()
        
        # Test 6: End-to-end workflow
        await self.test_end_to_end_workflow()
        
        # Generate test report
        self.generate_test_report()
    
    async def test_component_initialization(self):
        """Test component initialization and configuration"""
        logger.info("Testing component initialization...")
        
        try:
            # Initialize framework connector
            framework_config = {
                'quality_threshold': 75.0,
                'validation_timeout': 60,
                'enable_parallel_validation': True
            }
            
            self.components['framework_connector'] = AIInstructionFrameworkConnector(framework_config)
            
            # Initialize quality monitor  
            monitor_config = {
                'critical_threshold': 50.0,
                'warning_threshold': 65.0,
                'monitoring_interval': 10
            }
            
            self.components['quality_monitor'] = QualityMonitor(
                self.components['framework_connector'], monitor_config
            )
            
            # Initialize rollback manager
            rollback_config = {
                'quality_decline_threshold': 10.0,
                'critical_issues_threshold': 1,
                'backup_directory': '/tmp/test_integration_backups'
            }
            
            self.components['rollback_manager'] = RollbackManager(rollback_config)
            
            # Initialize validation orchestrator
            orchestrator_config = {
                'enable_quality_monitoring': True,
                'enable_automatic_rollback': True,
                'quality_preservation_threshold': 5.0
            }
            
            self.components['validation_orchestrator'] = ValidationOrchestrator(
                self.components['framework_connector'],
                self.components['quality_monitor'],
                self.components['rollback_manager'],
                orchestrator_config
            )
            
            self.test_results['component_initialization'] = {
                'status': 'PASSED',
                'components_initialized': len(self.components),
                'framework_connector': 'initialized',
                'quality_monitor': 'initialized',
                'rollback_manager': 'initialized',
                'validation_orchestrator': 'initialized'
            }
            
            logger.info("✓ Component initialization test passed")
            
        except Exception as e:
            self.test_results['component_initialization'] = {
                'status': 'FAILED',
                'error': str(e)
            }
            logger.error(f"✗ Component initialization test failed: {e}")
    
    async def test_framework_connector(self):
        """Test framework connector functionality"""
        logger.info("Testing framework connector...")
        
        try:
            framework_connector = self.components['framework_connector']
            
            # Test file validation
            test_file = '/Users/georgiospilitsoglou/Developer/projects/mypromptflow/.claude/commands/ai-help.md'
            
            if Path(test_file).exists():
                # Test pre-update validation
                result = await framework_connector.validate_instruction_file(
                    test_file, ValidationType.PRE_UPDATE
                )
                
                # Test batch validation
                batch_results = await framework_connector.batch_validate_files(
                    [test_file], ValidationType.PRE_UPDATE
                )
                
                # Get metrics
                metrics = await framework_connector.get_validation_metrics()
                
                self.test_results['framework_connector'] = {
                    'status': 'PASSED',
                    'validation_result': {
                        'file_path': result.file_path,
                        'overall_score': result.overall_score,
                        'quality_classification': result.quality_classification,
                        'issues_count': len(result.issues),
                        'validation_time': result.validation_time
                    },
                    'batch_validation': {
                        'files_validated': len(batch_results),
                        'successful_validations': len([r for r in batch_results if r.approval_status == 'APPROVED'])
                    },
                    'metrics': {
                        'total_validations': metrics['total_validations'],
                        'success_rate': metrics['success_rate'],
                        'available_validators': len(metrics['available_validators'])
                    }
                }
                
                logger.info("✓ Framework connector test passed")
            else:
                self.test_results['framework_connector'] = {
                    'status': 'SKIPPED',
                    'reason': 'Test file not found'
                }
                logger.warning("⚠ Framework connector test skipped - test file not found")
                
        except Exception as e:
            self.test_results['framework_connector'] = {
                'status': 'FAILED',
                'error': str(e)
            }
            logger.error(f"✗ Framework connector test failed: {e}")
    
    async def test_quality_monitoring(self):
        """Test quality monitoring functionality"""
        logger.info("Testing quality monitoring...")
        
        try:
            quality_monitor = self.components['quality_monitor']
            
            # Test monitoring setup
            test_file = '/Users/georgiospilitsoglou/Developer/projects/mypromptflow/.claude/commands/ai-help.md'
            
            if Path(test_file).exists():
                # Test alert callback
                captured_alerts = []
                
                async def test_alert_callback(alert):
                    captured_alerts.append(alert)
                
                quality_monitor.add_alert_callback(test_alert_callback)
                
                # Test on-demand monitoring
                await quality_monitor.start_monitoring([test_file], MonitoringMode.ON_DEMAND)
                
                # Get quality report
                report = await quality_monitor.get_quality_report(test_file)
                
                # Get dashboard
                dashboard = await quality_monitor.get_quality_dashboard()
                
                # Test quality impact validation
                with open(test_file, 'r') as f:
                    content = f.read()
                
                quality_impact = await quality_monitor.validate_update_quality_impact(
                    test_file, content, content  # Same content for test
                )
                
                self.test_results['quality_monitoring'] = {
                    'status': 'PASSED',
                    'monitoring_started': True,
                    'alerts_captured': len(captured_alerts),
                    'quality_report': {
                        'file_path': report.get('file_path'),
                        'current_quality': report.get('current_quality', {}),
                        'alerts': len(report.get('alerts', []))
                    },
                    'dashboard': {
                        'total_files': dashboard['summary']['total_files'],
                        'average_quality': dashboard['summary']['average_quality']
                    },
                    'quality_impact': {
                        'recommendation': quality_impact.get('recommendation'),
                        'quality_change': quality_impact.get('quality_change', 0)
                    }
                }
                
                # Stop monitoring
                await quality_monitor.stop_monitoring([test_file])
                
                logger.info("✓ Quality monitoring test passed")
            else:
                self.test_results['quality_monitoring'] = {
                    'status': 'SKIPPED',
                    'reason': 'Test file not found'
                }
                logger.warning("⚠ Quality monitoring test skipped - test file not found")
                
        except Exception as e:
            self.test_results['quality_monitoring'] = {
                'status': 'FAILED',
                'error': str(e)
            }
            logger.error(f"✗ Quality monitoring test failed: {e}")
    
    async def test_rollback_management(self):
        """Test rollback management functionality"""
        logger.info("Testing rollback management...")
        
        try:
            rollback_manager = self.components['rollback_manager']
            
            # Create test scenario
            test_file = '/tmp/test_rollback_file.md'
            test_content = "# Test File\n\nThis is a test instruction file."
            
            # Create test file
            with open(test_file, 'w') as f:
                f.write(test_content)
            
            # Create backup directory and backup
            backup_dir = Path('/tmp/test_integration_backups')
            backup_dir.mkdir(exist_ok=True)
            
            backup_file = backup_dir / 'test_rollback_file.md_20250725_120000.backup'
            with open(backup_file, 'w') as f:
                f.write(test_content)
            
            # Simulate framework result
            class MockFrameworkResult:
                def __init__(self):
                    self.overall_score = 45.0  # Low score
                    self.approval_status = "NEEDS_IMPROVEMENT"
                    self.issues = [MockIssue()]
            
            class MockIssue:
                def __init__(self):
                    self.severity = MockSeverity()
            
            class MockSeverity:
                def __init__(self):
                    self.value = 'critical'
            
            framework_result = MockFrameworkResult()
            quality_impact = {
                'quality_change': -12.0,  # Significant decline
                'impact_analysis': {
                    'significant_decline': True
                }
            }
            
            # Test rollback assessment
            decision = await rollback_manager.assess_rollback_need(
                test_file, framework_result, quality_impact, []
            )
            
            # Test rollback execution if recommended
            rollback_result = None
            if decision.should_rollback:
                rollback_result = await rollback_manager.execute_rollback(decision)
            
            # Get metrics
            metrics = await rollback_manager.get_rollback_metrics()
            
            self.test_results['rollback_management'] = {
                'status': 'PASSED',
                'rollback_decision': {
                    'should_rollback': decision.should_rollback,
                    'reason': decision.reason.value,
                    'confidence': decision.confidence,
                    'backup_available': decision.backup_available
                },
                'rollback_execution': rollback_result,
                'metrics': {
                    'total_decisions': metrics['total_decisions'],
                    'rollbacks_recommended': metrics['rollbacks_recommended'],
                    'success_rate': metrics['success_rate']
                }
            }
            
            # Cleanup
            if os.path.exists(test_file):
                os.unlink(test_file)
            if backup_file.exists():
                backup_file.unlink()
            
            logger.info("✓ Rollback management test passed")
            
        except Exception as e:
            self.test_results['rollback_management'] = {
                'status': 'FAILED',
                'error': str(e)
            }
            logger.error(f"✗ Rollback management test failed: {e}")
    
    async def test_validation_orchestration(self):
        """Test validation orchestration functionality"""
        logger.info("Testing validation orchestration...")
        
        try:
            orchestrator = self.components['validation_orchestrator']
            
            test_file = '/Users/georgiospilitsoglou/Developer/projects/mypromptflow/.claude/commands/ai-help.md'
            
            if Path(test_file).exists():
                # Test pre-update validation
                pre_results = await orchestrator.execute_pre_update_validation([test_file])
                
                # Test batch readiness validation
                readiness = await orchestrator.validate_batch_update_readiness([test_file])
                
                # Get orchestration status
                status = await orchestrator.get_orchestration_status()
                
                self.test_results['validation_orchestration'] = {
                    'status': 'PASSED',
                    'pre_update_validation': {
                        'files_validated': len(pre_results),
                        'approved_files': len([r for r in pre_results if r.overall_status.value == 'approved']),
                        'workflow_duration': pre_results[0].workflow_duration if pre_results else 0
                    },
                    'batch_readiness': {
                        'readiness_score': readiness['readiness_score'],
                        'recommendation': readiness['batch_recommendation'],
                        'approved_files': readiness['file_analysis']['approved_files']
                    },
                    'orchestration_status': {
                        'active_workflows': status['active_workflows'],
                        'metrics': status['metrics']
                    }
                }
                
                logger.info("✓ Validation orchestration test passed")
            else:
                self.test_results['validation_orchestration'] = {
                    'status': 'SKIPPED',
                    'reason': 'Test file not found'
                }
                logger.warning("⚠ Validation orchestration test skipped - test file not found")
                
        except Exception as e:
            self.test_results['validation_orchestration'] = {
                'status': 'FAILED',
                'error': str(e)
            }
            logger.error(f"✗ Validation orchestration test failed: {e}")
    
    async def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow"""
        logger.info("Testing end-to-end workflow...")
        
        try:
            # Create temporary test file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
                f.write("""# Test Command

Execute test workflow for: $ARGUMENTS

Follow these steps:
1. Validate input parameters
2. Execute test operations  
3. Generate test results
4. Report completion status

This command tests the validation integration system.
""")
                test_file_path = f.name
            
            try:
                # Step 1: Pre-update validation
                orchestrator = self.components['validation_orchestrator']
                pre_results = await orchestrator.execute_pre_update_validation([test_file_path])
                
                # Step 2: Simulate file update (modify content)
                original_content = ""
                with open(test_file_path, 'r') as f:
                    original_content = f.read()
                
                updated_content = original_content + "\n\n## Additional Notes\nUpdated content for testing."
                with open(test_file_path, 'w') as f:
                    f.write(updated_content)
                
                # Step 3: Post-update validation
                post_results = await orchestrator.execute_post_update_validation(
                    [test_file_path], 
                    {test_file_path: original_content}
                )
                
                # Step 4: Quality monitoring
                quality_monitor = self.components['quality_monitor']
                quality_impact = await quality_monitor.validate_update_quality_impact(
                    test_file_path, original_content, updated_content
                )
                
                self.test_results['end_to_end_workflow'] = {
                    'status': 'PASSED',
                    'pre_update': {
                        'files_processed': len(pre_results),
                        'validation_status': pre_results[0].overall_status.value if pre_results else 'unknown'
                    },
                    'post_update': {
                        'files_processed': len(post_results),
                        'validation_status': post_results[0].overall_status.value if post_results else 'unknown',
                        'rollback_required': any(r.overall_status.value == 'rollback_required' for r in post_results)
                    },
                    'quality_impact': {
                        'recommendation': quality_impact.get('recommendation'),
                        'quality_change': quality_impact.get('quality_change', 0),
                        'quality_preserved': quality_impact.get('impact_analysis', {}).get('quality_preserved', False)
                    },
                    'workflow_complete': True
                }
                
                logger.info("✓ End-to-end workflow test passed")
                
            finally:
                # Cleanup temporary file
                if os.path.exists(test_file_path):
                    os.unlink(test_file_path)
                    
        except Exception as e:
            self.test_results['end_to_end_workflow'] = {
                'status': 'FAILED',
                'error': str(e)
            }
            logger.error(f"✗ End-to-end workflow test failed: {e}")
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        logger.info("Generating integration test report...")
        
        # Calculate summary statistics
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results.values() if r.get('status') == 'PASSED'])
        failed_tests = len([r for r in self.test_results.values() if r.get('status') == 'FAILED'])
        skipped_tests = len([r for r in self.test_results.values() if r.get('status') == 'SKIPPED'])
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        report = {
            'integration_test_summary': {
                'test_suite': 'AI Agent Instruction Design Excellence Integration',
                'total_tests': total_tests,
                'passed_tests': passed_tests,
                'failed_tests': failed_tests,
                'skipped_tests': skipped_tests,
                'success_rate': f"{success_rate:.1f}%",
                'overall_status': 'PASSED' if failed_tests == 0 else 'FAILED'
            },
            'test_results': self.test_results,
            'integration_status': {
                'framework_connector': 'OPERATIONAL' if self.components.get('framework_connector') else 'FAILED',
                'quality_monitor': 'OPERATIONAL' if self.components.get('quality_monitor') else 'FAILED',
                'rollback_manager': 'OPERATIONAL' if self.components.get('rollback_manager') else 'FAILED',
                'validation_orchestrator': 'OPERATIONAL' if self.components.get('validation_orchestrator') else 'FAILED'
            },
            'recommendations': self._generate_recommendations()
        }
        
        print("\n" + "="*80)
        print("AI AGENT INSTRUCTION DESIGN EXCELLENCE INTEGRATION TEST REPORT")
        print("="*80)
        print(json.dumps(report, indent=2, default=str))
        print("="*80)
        
        return report
    
    def _generate_recommendations(self):
        """Generate recommendations based on test results"""
        recommendations = []
        
        # Check for failed tests
        failed_tests = [name for name, result in self.test_results.items() if result.get('status') == 'FAILED']
        if failed_tests:
            recommendations.append(f"Address failures in: {', '.join(failed_tests)}")
        
        # Check for skipped tests
        skipped_tests = [name for name, result in self.test_results.items() if result.get('status') == 'SKIPPED']
        if skipped_tests:
            recommendations.append(f"Review skipped tests: {', '.join(skipped_tests)} - ensure test files are available")
        
        # Quality-specific recommendations
        if 'framework_connector' in self.test_results:
            fc_result = self.test_results['framework_connector']
            if fc_result.get('status') == 'PASSED':
                validation_result = fc_result.get('validation_result', {})
                if validation_result.get('overall_score', 0) < 75:
                    recommendations.append("Consider improving test file quality for better framework validation scores")
        
        # Add general recommendations
        if not recommendations:
            recommendations.extend([
                "Integration system is operational and ready for production use",
                "Monitor quality preservation during actual update operations",
                "Regularly review validation thresholds and adjust as needed",
                "Consider implementing additional automated tests for edge cases"
            ])
        
        return recommendations


async def main():
    """Main test execution function"""
    test_suite = IntegrationTestSuite()
    await test_suite.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())