#!/usr/bin/env python3
"""
PR Knowledge Connector
AI Knowledge Lifecycle Orchestrator - PR Validation Enhancement

Main interface connecting PR validation with the AI Knowledge Lifecycle Orchestrator
system. Provides context-aware validation using current technology knowledge,
dependency mapping, and change tracking.
"""

import os
import sys
import yaml
import json
import logging
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
from datetime import datetime

# Add parent directory to path for knowledge vault integration
sys.path.append(str(Path(__file__).parent.parent))
from knowledge_vault_integration import KnowledgeVaultIntegration

from context_analyzer import PRContextAnalyzer
from validation_engine import TechnologyValidationEngine
from security_assessor import SecurityAssessor
from consistency_validator import ConsistencyValidator


@dataclass
class PRValidationRequest:
    """PR validation request data structure"""
    pr_id: str
    pr_title: str
    pr_description: str
    author: str
    target_branch: str
    source_branch: str
    changed_files: List[Dict[str, Any]]
    diff_content: str
    repository_context: Dict[str, Any]
    validation_config: Dict[str, Any]


@dataclass
class PRValidationResult:
    """PR validation result data structure"""
    pr_id: str
    overall_score: float
    validation_passed: bool
    security_score: float
    consistency_score: float
    technology_currency_score: float
    critical_issues: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]
    detailed_findings: Dict[str, Any]
    processing_time: float
    timestamp: str


class PRKnowledgeConnector:
    """Main interface for PR validation with knowledge system integration"""
    
    def __init__(self, config_path: str = None):
        """Initialize the PR Knowledge Connector"""
        self.config_path = config_path or self._get_default_config_path()
        self.config = self._load_configuration()
        self._setup_logging()
        
        # Initialize knowledge vault integration
        self.knowledge_vault = KnowledgeVaultIntegration(
            base_path=self.config['knowledge_vault']['base_path']
        )
        
        # Initialize validation components
        self.context_analyzer = PRContextAnalyzer(self.knowledge_vault, self.config)
        self.validation_engine = TechnologyValidationEngine(self.knowledge_vault, self.config)
        self.security_assessor = SecurityAssessor(self.knowledge_vault, self.config)
        self.consistency_validator = ConsistencyValidator(self.knowledge_vault, self.config)
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("PR Knowledge Connector initialized successfully")
    
    def _get_default_config_path(self) -> str:
        """Get default configuration file path"""
        return str(Path(__file__).parent / "enhancement_config.yaml")
    
    def _load_configuration(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
            return config
        except Exception as e:
            raise RuntimeError(f"Failed to load configuration from {self.config_path}: {str(e)}")
    
    def _setup_logging(self):
        """Setup logging configuration"""
        log_config = self.config.get('logging', {})
        log_level = getattr(logging, log_config.get('level', 'INFO'))
        
        # Configure logging
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Setup file logging if configured
        if 'file' in log_config.get('output', []):
            file_settings = log_config.get('file_settings', {})
            log_path = Path(file_settings.get('path', 'logs/pr_validation_enhancement.log'))
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            file_handler = logging.FileHandler(log_path)
            file_handler.setLevel(log_level)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(formatter)
            
            root_logger = logging.getLogger()
            root_logger.addHandler(file_handler)
    
    def validate_pr(self, pr_request: PRValidationRequest) -> PRValidationResult:
        """
        Main PR validation entry point
        
        Args:
            pr_request: PR validation request with all necessary data
            
        Returns:
            PRValidationResult: Comprehensive validation results
        """
        start_time = datetime.now()
        self.logger.info(f"Starting PR validation for PR #{pr_request.pr_id}")
        
        try:
            # Phase 1: Context Analysis
            self.logger.info("Phase 1: Analyzing PR context and detecting technologies")
            context_analysis = self.context_analyzer.analyze_pr_context(pr_request)
            
            # Phase 2: Technology Validation
            self.logger.info("Phase 2: Validating technology usage and versions")
            technology_validation = self.validation_engine.validate_technologies(
                pr_request, context_analysis
            )
            
            # Phase 3: Security Assessment
            self.logger.info("Phase 3: Performing security assessment")
            security_assessment = self.security_assessor.assess_pr_security(
                pr_request, context_analysis
            )
            
            # Phase 4: Consistency Validation
            self.logger.info("Phase 4: Validating project consistency")
            consistency_validation = self.consistency_validator.validate_consistency(
                pr_request, context_analysis
            )
            
            # Phase 5: Result Aggregation
            self.logger.info("Phase 5: Aggregating validation results")
            validation_result = self._aggregate_validation_results(
                pr_request,
                context_analysis,
                technology_validation,
                security_assessment,
                consistency_validation,
                start_time
            )
            
            # Log completion
            processing_time = validation_result.processing_time
            self.logger.info(
                f"PR validation completed for PR #{pr_request.pr_id} "
                f"in {processing_time:.2f}s - Overall Score: {validation_result.overall_score:.1f}"
            )
            
            return validation_result
            
        except Exception as e:
            self.logger.error(f"PR validation failed for PR #{pr_request.pr_id}: {str(e)}")
            return self._create_error_result(pr_request, str(e), start_time)
    
    def _aggregate_validation_results(
        self,
        pr_request: PRValidationRequest,
        context_analysis: Dict[str, Any],
        technology_validation: Dict[str, Any],
        security_assessment: Dict[str, Any],
        consistency_validation: Dict[str, Any],
        start_time: datetime
    ) -> PRValidationResult:
        """Aggregate all validation results into final result"""
        
        # Calculate individual scores
        tech_score = technology_validation.get('overall_score', 0.0)
        security_score = security_assessment.get('security_score', 0.0)
        consistency_score = consistency_validation.get('consistency_score', 0.0)
        
        # Calculate weighted overall score
        weights = self.config.get('scoring_weights', {
            'technology': 0.3,
            'security': 0.4,
            'consistency': 0.3
        })
        
        overall_score = (
            tech_score * weights.get('technology', 0.3) +
            security_score * weights.get('security', 0.4) +
            consistency_score * weights.get('consistency', 0.3)
        )
        
        # Determine if validation passed
        min_threshold = self.config.get('quality_thresholds', {}).get('overall_score', {}).get('minimum', 75)
        validation_passed = overall_score >= min_threshold
        
        # Collect critical issues
        critical_issues = []
        critical_issues.extend(technology_validation.get('critical_issues', []))
        critical_issues.extend(security_assessment.get('critical_issues', []))
        critical_issues.extend(consistency_validation.get('critical_issues', []))
        
        # Collect recommendations
        recommendations = []
        recommendations.extend(technology_validation.get('recommendations', []))
        recommendations.extend(security_assessment.get('recommendations', []))
        recommendations.extend(consistency_validation.get('recommendations', []))
        
        # Create detailed findings
        detailed_findings = {
            'context_analysis': context_analysis,
            'technology_validation': technology_validation,
            'security_assessment': security_assessment,
            'consistency_validation': consistency_validation,
            'processing_metadata': {
                'components_executed': 4,
                'validation_config': pr_request.validation_config,
                'knowledge_vault_queries': self._get_knowledge_queries_count()
            }
        }
        
        # Calculate processing time
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return PRValidationResult(
            pr_id=pr_request.pr_id,
            overall_score=overall_score,
            validation_passed=validation_passed,
            security_score=security_score,
            consistency_score=consistency_score,
            technology_currency_score=tech_score,
            critical_issues=critical_issues,
            recommendations=recommendations,
            detailed_findings=detailed_findings,
            processing_time=processing_time,
            timestamp=datetime.now().isoformat()
        )
    
    def _create_error_result(
        self, 
        pr_request: PRValidationRequest, 
        error_message: str, 
        start_time: datetime
    ) -> PRValidationResult:
        """Create error result for failed validation"""
        processing_time = (datetime.now() - start_time).total_seconds()
        
        return PRValidationResult(
            pr_id=pr_request.pr_id,
            overall_score=0.0,
            validation_passed=False,
            security_score=0.0,
            consistency_score=0.0,
            technology_currency_score=0.0,
            critical_issues=[{
                'type': 'validation_error',
                'severity': 'critical',
                'message': f"PR validation failed: {error_message}",
                'component': 'pr_knowledge_connector',
                'timestamp': datetime.now().isoformat()
            }],
            recommendations=[{
                'type': 'error_resolution',
                'priority': 'high',
                'message': 'Review validation configuration and ensure all dependencies are available',
                'action': 'troubleshoot_validation_setup'
            }],
            detailed_findings={
                'error': error_message,
                'processing_metadata': {
                    'validation_failed': True,
                    'error_timestamp': datetime.now().isoformat()
                }
            },
            processing_time=processing_time,
            timestamp=datetime.now().isoformat()
        )
    
    def _get_knowledge_queries_count(self) -> int:
        """Get count of knowledge vault queries made during validation"""
        # This would be implemented with proper query tracking
        # For now, return estimated count
        return 10
    
    def get_validation_summary(self, pr_id: str) -> Dict[str, Any]:
        """Get summary of validation for a specific PR"""
        # This would retrieve cached validation results
        # For now, return basic structure
        return {
            'pr_id': pr_id,
            'status': 'not_implemented',
            'message': 'Validation summary retrieval not yet implemented'
        }
    
    def get_technology_context(self, technologies: List[str]) -> Dict[str, Any]:
        """Get current technology context for specified technologies"""
        context = {}
        
        for tech_name in technologies:
            # Get technology tracking info
            tech_entries = self.knowledge_vault.query_technologies({'technology_name': tech_name})
            
            # Get dependencies
            dependencies = self.knowledge_vault.get_dependencies_by_technology(tech_name)
            
            # Get recent changes
            changes = self.knowledge_vault.query_change_events({'technology_name': tech_name})
            
            context[tech_name] = {
                'tracking_entries': len(tech_entries),
                'current_version': tech_entries[0].get('current_version') if tech_entries else 'unknown',
                'monitoring_priority': tech_entries[0].get('monitoring_priority') if tech_entries else 'unknown',
                'affected_files': len(dependencies),
                'recent_changes': len(changes),
                'has_critical_updates': any(
                    change.get('change_classification') == 'critical' 
                    for change in changes
                )
            }
        
        return context
    
    def validate_configuration(self) -> Dict[str, Any]:
        """Validate the current configuration and dependencies"""
        validation_results = {
            'configuration_valid': True,
            'issues': [],
            'warnings': [],
            'component_status': {}
        }
        
        try:
            # Check knowledge vault integration
            health = self.knowledge_vault.get_system_health_summary()
            validation_results['component_status']['knowledge_vault'] = {
                'status': 'healthy',
                'database_counts': health['database_counts']
            }
        except Exception as e:
            validation_results['configuration_valid'] = False
            validation_results['issues'].append(f"Knowledge Vault integration failed: {str(e)}")
            validation_results['component_status']['knowledge_vault'] = {
                'status': 'error',
                'error': str(e)
            }
        
        # Check validation components
        components = [
            ('context_analyzer', self.context_analyzer),
            ('validation_engine', self.validation_engine),
            ('security_assessor', self.security_assessor),
            ('consistency_validator', self.consistency_validator)
        ]
        
        for name, component in components:
            try:
                # Basic component health check
                if hasattr(component, 'validate_configuration'):
                    component_status = component.validate_configuration()
                    validation_results['component_status'][name] = component_status
                else:
                    validation_results['component_status'][name] = {'status': 'available'}
            except Exception as e:
                validation_results['configuration_valid'] = False
                validation_results['issues'].append(f"{name} component failed: {str(e)}")
                validation_results['component_status'][name] = {
                    'status': 'error',
                    'error': str(e)
                }
        
        return validation_results


def create_sample_pr_request() -> PRValidationRequest:
    """Create a sample PR request for testing"""
    return PRValidationRequest(
        pr_id="123",
        pr_title="Update React components and add TypeScript support",
        pr_description="This PR updates several React components to use modern patterns and adds TypeScript support for better type safety.",
        author="developer@example.com",
        target_branch="main",
        source_branch="feature/react-typescript-update",
        changed_files=[
            {
                'filename': 'src/components/UserProfile.tsx',
                'status': 'modified',
                'additions': 45,
                'deletions': 23,
                'changes': 68
            },
            {
                'filename': 'src/hooks/useAuth.ts',
                'status': 'added',
                'additions': 67,
                'deletions': 0,
                'changes': 67
            },
            {
                'filename': 'package.json',
                'status': 'modified',
                'additions': 3,
                'deletions': 1,
                'changes': 4
            }
        ],
        diff_content="Sample diff content would be here...",
        repository_context={
            'name': 'example-react-app',
            'language': 'TypeScript',
            'framework': 'React',
            'package_manager': 'npm'
        },
        validation_config={
            'strict_mode': False,
            'security_scan': True,
            'performance_check': True
        }
    )


def main():
    """Main function for testing"""
    try:
        # Initialize connector
        connector = PRKnowledgeConnector()
        
        print("PR Knowledge Connector - Testing Interface")
        print("=" * 50)
        
        # Validate configuration
        print("Validating configuration...")
        config_validation = connector.validate_configuration()
        print(f"Configuration valid: {config_validation['configuration_valid']}")
        
        if not config_validation['configuration_valid']:
            print("Configuration issues found:")
            for issue in config_validation['issues']:
                print(f"  - {issue}")
            return 1
        
        # Test with sample PR request
        print("\nTesting with sample PR request...")
        sample_request = create_sample_pr_request()
        
        # Perform validation
        result = connector.validate_pr(sample_request)
        
        # Display results
        print(f"\nValidation Results for PR #{result.pr_id}:")
        print(f"Overall Score: {result.overall_score:.1f}")
        print(f"Validation Passed: {result.validation_passed}")
        print(f"Security Score: {result.security_score:.1f}")
        print(f"Consistency Score: {result.consistency_score:.1f}")
        print(f"Technology Currency Score: {result.technology_currency_score:.1f}")
        print(f"Processing Time: {result.processing_time:.2f}s")
        print(f"Critical Issues: {len(result.critical_issues)}")
        print(f"Recommendations: {len(result.recommendations)}")
        
        # Test technology context
        print("\nTesting technology context lookup...")
        tech_context = connector.get_technology_context(['React', 'TypeScript'])
        print(f"Technology context retrieved for {len(tech_context)} technologies")
        
        print("\nPR Knowledge Connector test completed successfully!")
        return 0
        
    except Exception as e:
        print(f"Test failed: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())