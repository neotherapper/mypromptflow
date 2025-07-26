#!/usr/bin/env python3
"""
Framework Connector
AI Knowledge Lifecycle Orchestrator - Integration with AI Agent Instruction Design Excellence Framework

This module provides seamless integration between the update pipeline and the AI Agent Instruction
Design Excellence framework for quality-preserving automated updates.
"""

import asyncio
import logging
import json
import os
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ValidationType(Enum):
    """Types of validation to perform"""
    PRE_UPDATE = "pre_update"
    POST_UPDATE = "post_update" 
    ROLLBACK_VALIDATION = "rollback_validation"
    QUALITY_MONITORING = "quality_monitoring"


class ValidationSeverity(Enum):
    """Validation result severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass 
class ValidationIssue:
    """Individual validation issue"""
    severity: ValidationSeverity
    category: str
    message: str
    line_number: Optional[int]
    suggestion: Optional[str]
    tool_source: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['severity'] = self.severity.value
        return data


@dataclass
class FrameworkValidationResult:
    """Comprehensive validation result from AI Agent Instruction Design Excellence framework"""
    file_path: str
    validation_type: ValidationType
    overall_score: float
    component_scores: Dict[str, float] 
    quality_classification: str
    approval_status: str
    issues: List[ValidationIssue]
    strengths: List[str]
    recommendations: List[str]
    validation_time: float
    framework_version: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['validation_type'] = self.validation_type.value
        data['issues'] = [issue.to_dict() for issue in self.issues]
        return data
    
    def is_passing(self, threshold: float = 75.0) -> bool:
        """Check if validation passes quality threshold"""
        return self.overall_score >= threshold and self.approval_status == "APPROVED"
    
    def has_critical_issues(self) -> bool:
        """Check if validation has critical issues"""
        return any(issue.severity == ValidationSeverity.CRITICAL for issue in self.issues)


class AIInstructionFrameworkConnector:
    """
    Main connector to AI Agent Instruction Design Excellence framework
    Provides validation capabilities for AI instruction files during updates
    """
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the framework connector"""
        self.config = config
        
        # Framework paths
        self.framework_base = Path(config.get('framework_base_path', 
            '/Users/georgiospilitsoglou/Developer/projects/mypromptflow/projects/ai-agent-instruction-design-excellence'))
        self.validators_path = Path(config.get('validators_path',
            '/Users/georgiospilitsoglou/Developer/projects/mypromptflow/meta/validation/validators/ai-instruction'))
        self.automation_tools_path = self.framework_base / 'docs' / 'automation-tools'
        
        # Quality thresholds
        self.quality_threshold = config.get('quality_threshold', 75.0)
        self.critical_threshold = config.get('critical_threshold', 60.0)
        self.rollback_threshold = config.get('rollback_threshold', 50.0)
        
        # Validation configuration
        self.validation_timeout = config.get('validation_timeout', 60)  # seconds
        self.enable_parallel_validation = config.get('enable_parallel_validation', True)
        self.framework_version = config.get('framework_version', '3.0.0')
        
        # Available validators
        self.available_validators = {
            'claude_command_evaluator': self.validators_path / 'claude-command-evaluator.md',
            'command_intent_validator': self.validators_path / 'command-intent-validator.md',
            'ai_agent_instruction_evaluator': self.validators_path / 'ai-agent-instruction-evaluator.md',
            'intent_implementation_validator': self.validators_path / 'intent-implementation-validator.md'
        }
        
        # Available automation tools
        self.available_automation_tools = {
            'vagueness_detector': self.automation_tools_path / 'vagueness-detector.md',
            'dependency_scanner': self.automation_tools_path / 'dependency-scanner.md',
            'checklist_automator': self.automation_tools_path / 'checklist-automator.md',
            'assessment_calculator': self.automation_tools_path / 'assessment-calculator.md',
            'report_generator': self.automation_tools_path / 'report-generator.md'
        }
        
        # Metrics tracking
        self.validation_metrics = {
            'total_validations': 0,
            'passed_validations': 0,
            'failed_validations': 0,
            'rollbacks_triggered': 0,
            'average_validation_time': 0.0,
            'framework_errors': 0
        }
        
        logger.info(f"Framework Connector initialized with {len(self.available_validators)} validators")
    
    async def validate_instruction_file(self, file_path: str, validation_type: ValidationType = ValidationType.PRE_UPDATE, 
                                      original_content: Optional[str] = None) -> FrameworkValidationResult:
        """
        Validate an AI instruction file using the framework
        
        Args:
            file_path: Path to the instruction file
            validation_type: Type of validation to perform
            original_content: Original content for comparison (for POST_UPDATE validation)
            
        Returns:
            Comprehensive validation result
        """
        start_time = asyncio.get_event_loop().time()
        
        try:
            logger.info(f"Validating {file_path} with {validation_type.value}")
            
            # Determine appropriate validators based on file type
            validators_to_use = await self._select_validators(file_path, validation_type)
            
            # Execute validation workflow
            if self.enable_parallel_validation and len(validators_to_use) > 1:
                validation_results = await self._execute_parallel_validation(file_path, validators_to_use)
            else:
                validation_results = await self._execute_sequential_validation(file_path, validators_to_use)
            
            # Integrate automation tools for comprehensive analysis
            automation_results = await self._execute_automation_tools(file_path, validation_type)
            
            # Combine results into comprehensive assessment
            comprehensive_result = await self._synthesize_validation_results(
                file_path, validation_type, validation_results, automation_results, start_time
            )
            
            # Update metrics
            self._update_validation_metrics(comprehensive_result, start_time)
            
            logger.info(f"Validation completed: {comprehensive_result.overall_score:.1f}/100 ({comprehensive_result.quality_classification})")
            return comprehensive_result
            
        except Exception as e:
            logger.error(f"Error validating instruction file {file_path}: {e}")
            self.validation_metrics['framework_errors'] += 1
            
            # Return failure result
            return FrameworkValidationResult(
                file_path=file_path,
                validation_type=validation_type,
                overall_score=0.0,
                component_scores={},
                quality_classification="VALIDATION_ERROR",
                approval_status="FAILED",
                issues=[ValidationIssue(
                    severity=ValidationSeverity.CRITICAL,
                    category="framework_error",
                    message=f"Framework validation failed: {str(e)}",
                    line_number=None,
                    suggestion="Check framework configuration and file accessibility",
                    tool_source="framework_connector"
                )],
                strengths=[],
                recommendations=["Resolve framework integration issues before proceeding"],
                validation_time=asyncio.get_event_loop().time() - start_time,
                framework_version=self.framework_version
            )
    
    async def _select_validators(self, file_path: str, validation_type: ValidationType) -> List[str]:
        """Select appropriate validators based on file type and validation type"""
        path = Path(file_path)
        validators = []
        
        # Determine file type
        if '.claude/commands' in str(path):
            # Command file validation
            validators.extend(['command_intent_validator', 'claude_command_evaluator'])
        elif 'CLAUDE.md' in path.name:
            # CLAUDE.md file validation
            validators.extend(['ai_agent_instruction_evaluator', 'intent_implementation_validator'])
        else:
            # General AI instruction validation
            validators.extend(['ai_agent_instruction_evaluator'])
        
        # Add validation-type specific validators
        if validation_type == ValidationType.POST_UPDATE:
            # Post-update validation focuses on quality preservation
            if 'claude_command_evaluator' not in validators:
                validators.append('claude_command_evaluator')
        elif validation_type == ValidationType.ROLLBACK_VALIDATION:
            # Rollback validation focuses on critical issues
            validators = ['command_intent_validator']  # Fast, focused validation
        
        # Filter to available validators
        available_validators = [v for v in validators if v in self.available_validators]
        
        logger.debug(f"Selected validators for {path.name}: {available_validators}")
        return available_validators
    
    async def _execute_parallel_validation(self, file_path: str, validators: List[str]) -> Dict[str, Any]:
        """Execute multiple validators in parallel"""
        logger.debug(f"Executing {len(validators)} validators in parallel")
        
        # Create validation tasks
        tasks = []
        for validator in validators:
            task = self._execute_single_validator(file_path, validator)
            tasks.append(task)
        
        # Execute all validators concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        validation_results = {}
        for i, result in enumerate(results):
            validator_name = validators[i]
            if isinstance(result, Exception):
                logger.error(f"Validator {validator_name} failed: {result}")
                validation_results[validator_name] = {
                    'error': str(result),
                    'success': False
                }
            else:
                validation_results[validator_name] = result
        
        return validation_results
    
    async def _execute_sequential_validation(self, file_path: str, validators: List[str]) -> Dict[str, Any]:
        """Execute validators sequentially"""
        logger.debug(f"Executing {len(validators)} validators sequentially")
        
        validation_results = {}
        for validator in validators:
            try:
                result = await self._execute_single_validator(file_path, validator)
                validation_results[validator] = result
            except Exception as e:
                logger.error(f"Validator {validator} failed: {e}")
                validation_results[validator] = {
                    'error': str(e),
                    'success': False
                }
        
        return validation_results
    
    async def _execute_single_validator(self, file_path: str, validator_name: str) -> Dict[str, Any]:
        """Execute a single validator on the file"""
        validator_path = self.available_validators.get(validator_name)
        if not validator_path or not validator_path.exists():
            raise FileNotFoundError(f"Validator not found: {validator_name}")
        
        # This would integrate with the actual validator execution
        # For now, simulate validator execution with structured output
        logger.debug(f"Executing validator: {validator_name}")
        
        # Read the file content to analyze
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Simulate validator analysis based on actual validator patterns
        if validator_name == 'claude_command_evaluator':
            return await self._simulate_claude_command_evaluation(content, file_path)
        elif validator_name == 'command_intent_validator':
            return await self._simulate_intent_validation(content, file_path)
        elif validator_name == 'ai_agent_instruction_evaluator':
            return await self._simulate_ai_instruction_evaluation(content, file_path)
        else:
            return await self._simulate_generic_validation(content, file_path, validator_name)
    
    async def _simulate_claude_command_evaluation(self, content: str, file_path: str) -> Dict[str, Any]:
        """Simulate Claude command evaluator based on actual framework"""
        issues = []
        strengths = []
        component_scores = {}
        
        # Check for title/user-facing description
        lines = content.split('\n')
        first_line = lines[0].strip() if lines else ""
        
        if first_line.startswith('#') or '$ARGUMENTS' in first_line:
            strengths.append("Clear user-facing title or direct instruction present")
            component_scores['title_quality'] = 9.0
        else:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.HIGH,
                category="user_interface",
                message="Missing clear user-facing title or direct instruction",
                line_number=1,
                suggestion="Add markdown title (# Title) or direct instruction as first line",
                tool_source="claude_command_evaluator"
            ))
            component_scores['title_quality'] = 4.0
        
        # Check for $ARGUMENTS pattern if command seems parameterized
        if 'ARGUMENTS' in content.upper() or any(param in content.lower() for param in ['parameter', 'argument', 'input']):
            if '$ARGUMENTS' in content:
                strengths.append("Proper $ARGUMENTS pattern usage")
                component_scores['arguments_pattern'] = 6.0
            else:
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.MEDIUM,
                    category="parameter_handling", 
                    message="Command appears parameterized but missing $ARGUMENTS pattern",
                    line_number=None,
                    suggestion="Use $ARGUMENTS pattern for parameterized commands",
                    tool_source="claude_command_evaluator"
                ))
                component_scores['arguments_pattern'] = 2.0
        else:
            component_scores['arguments_pattern'] = 6.0  # N/A for non-parameterized
        
        # Check for actionable steps
        if any(pattern in content for pattern in ['1.', '2.', '3.', '- ', '* ', 'Follow these steps']):
            strengths.append("Actionable steps provided")
            component_scores['actionable_steps'] = 6.0
        else:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.HIGH,
                category="actionability",
                message="Missing clear actionable steps",
                line_number=None,
                suggestion="Add numbered or bulleted steps for AI agent execution",
                tool_source="claude_command_evaluator"
            ))
            component_scores['actionable_steps'] = 2.0
        
        # Check for vague language
        vague_terms = ['effectively', 'efficiently', 'appropriately', 'properly', 'optimally']
        vague_count = sum(content.lower().count(term) for term in vague_terms)
        
        if vague_count > 3:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.MEDIUM,
                category="vagueness",
                message=f"High vagueness detected: {vague_count} vague terms found",
                line_number=None,
                suggestion="Replace vague terms with specific, concrete language",
                tool_source="claude_command_evaluator"
            ))
            component_scores['concrete_specificity'] = max(8.0 - vague_count * 0.5, 3.0)
        else:
            component_scores['concrete_specificity'] = 8.0
        
        # Calculate overall score
        total_possible = 35.0  # Based on framework scoring
        earned_score = sum(component_scores.values())
        overall_score = (earned_score / total_possible) * 100
        
        return {
            'success': True,
            'overall_score': overall_score,
            'component_scores': component_scores,
            'issues': issues,
            'strengths': strengths,
            'quality_classification': self._classify_quality(overall_score),
            'approval_status': "APPROVED" if overall_score >= self.quality_threshold else "NEEDS_IMPROVEMENT"
        }
    
    async def _simulate_intent_validation(self, content: str, file_path: str) -> Dict[str, Any]:
        """Simulate command intent validator"""
        issues = []
        strengths = []
        
        # Analyze first line for intent
        lines = content.split('\n')
        first_line = lines[0].strip() if lines else ""
        
        # Intent classification
        if any(pattern in first_line.lower() for pattern in ['display', 'show', 'present']):
            intent_type = "display_intent"
            strengths.append("Clear display intent detected")
        elif any(pattern in first_line.lower() for pattern in ['execute', 'run', 'perform', 'analyze']):
            intent_type = "execution_intent"  
            strengths.append("Clear execution intent detected")
        else:
            intent_type = "unclear_intent"
            issues.append(ValidationIssue(
                severity=ValidationSeverity.HIGH,
                category="intent_clarity",
                message="Unclear command intent",
                line_number=1,
                suggestion="Start with clear action verb indicating command purpose",
                tool_source="command_intent_validator"
            ))
        
        overall_score = 85.0 if intent_type != "unclear_intent" else 65.0
        
        return {
            'success': True,
            'overall_score': overall_score,
            'component_scores': {'intent_clarity': overall_score / 100 * 25},
            'issues': issues,
            'strengths': strengths,
            'intent_type': intent_type,
            'quality_classification': self._classify_quality(overall_score),
            'approval_status': "APPROVED" if overall_score >= self.quality_threshold else "NEEDS_IMPROVEMENT"
        }
    
    async def _simulate_ai_instruction_evaluation(self, content: str, file_path: str) -> Dict[str, Any]:
        """Simulate AI agent instruction evaluator"""
        issues = []
        strengths = []
        component_scores = {}
        
        # Check for immediate actionability
        action_indicators = ['Execute', 'Apply', 'Create', 'Analyze', 'Follow', 'Use', 'Run']
        if any(indicator in content for indicator in action_indicators):
            strengths.append("Immediate actionability indicators present")
            component_scores['immediate_actionability'] = 22.0
        else:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.HIGH,
                category="actionability",
                message="Limited immediate actionability indicators",
                line_number=None,
                suggestion="Add clear action verbs and executable instructions",
                tool_source="ai_agent_instruction_evaluator"
            ))
            component_scores['immediate_actionability'] = 15.0
        
        # Check for external dependencies
        external_deps = ['http://', 'https://', 'external', 'third-party', 'outside']
        external_count = sum(content.lower().count(dep) for dep in external_deps)
        
        if external_count == 0:
            strengths.append("No external dependencies detected")
            component_scores['self_sufficiency'] = 20.0
        else:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.MEDIUM,
                category="dependencies",
                message=f"External dependencies detected: {external_count}",
                line_number=None,
                suggestion="Replace external references with internal resources",
                tool_source="ai_agent_instruction_evaluator"
            ))
            component_scores['self_sufficiency'] = max(20.0 - external_count * 2, 10.0)
        
        # Design excellence compliance
        component_scores['design_excellence'] = 23.0  # Default good score
        
        # Calculate overall score
        total_possible = 65.0
        earned_score = sum(component_scores.values())
        overall_score = (earned_score / total_possible) * 100
        
        return {
            'success': True,
            'overall_score': overall_score,
            'component_scores': component_scores,
            'issues': issues,
            'strengths': strengths,
            'quality_classification': self._classify_quality(overall_score),
            'approval_status': "APPROVED" if overall_score >= self.quality_threshold else "NEEDS_IMPROVEMENT"
        }
    
    async def _simulate_generic_validation(self, content: str, file_path: str, validator_name: str) -> Dict[str, Any]:
        """Simulate generic validation for any validator"""
        # Basic content analysis
        overall_score = 80.0  # Default score
        
        return {
            'success': True,
            'overall_score': overall_score,
            'component_scores': {'general_quality': overall_score},
            'issues': [],
            'strengths': ["File accessible and readable"],
            'quality_classification': self._classify_quality(overall_score),
            'approval_status': "APPROVED" if overall_score >= self.quality_threshold else "NEEDS_IMPROVEMENT"
        }
    
    async def _execute_automation_tools(self, file_path: str, validation_type: ValidationType) -> Dict[str, Any]:
        """Execute automation tools for comprehensive analysis"""
        if validation_type == ValidationType.ROLLBACK_VALIDATION:
            # Skip automation tools for rollback validation (speed priority)
            return {'automation_skipped': True}
        
        # Simulate automation tools execution
        automation_results = {
            'vagueness_analysis': {
                'density': 8.5,  # Percentage
                'high_severity_count': 2,
                'medium_severity_count': 3,
                'recommendations': ['Replace "effectively" with specific measurement criteria']
            },
            'dependency_analysis': {
                'external_dependencies': 1,
                'self_sufficiency_score': 85,
                'recommendations': ['Convert external URL to internal resource reference']
            }
        }
        
        return automation_results
    
    async def _synthesize_validation_results(self, file_path: str, validation_type: ValidationType, 
                                           validation_results: Dict[str, Any], automation_results: Dict[str, Any], 
                                           start_time: float) -> FrameworkValidationResult:
        """Synthesize all validation results into comprehensive assessment"""
        
        all_issues = []
        all_strengths = []
        all_recommendations = []
        component_scores = {}
        
        # Process validator results
        validator_scores = []
        for validator_name, result in validation_results.items():
            if result.get('success', False):
                validator_scores.append(result.get('overall_score', 0))
                all_issues.extend([
                    issue if isinstance(issue, ValidationIssue) else ValidationIssue(**issue)
                    for issue in result.get('issues', [])
                ])
                all_strengths.extend(result.get('strengths', []))
                
                # Merge component scores
                for component, score in result.get('component_scores', {}).items():
                    component_scores[f"{validator_name}_{component}"] = score
        
        # Process automation results
        if not automation_results.get('automation_skipped', False):
            vagueness = automation_results.get('vagueness_analysis', {})
            if vagueness.get('density', 0) > 10:
                all_issues.append(ValidationIssue(
                    severity=ValidationSeverity.MEDIUM,
                    category="vagueness",
                    message=f"High vagueness density: {vagueness.get('density', 0):.1f}%",
                    line_number=None,
                    suggestion="Reduce vague language using concrete alternatives",
                    tool_source="automation_tools"
                ))
            
            all_recommendations.extend(vagueness.get('recommendations', []))
            all_recommendations.extend(
                automation_results.get('dependency_analysis', {}).get('recommendations', [])
            )
        
        # Calculate overall score
        if validator_scores:
            overall_score = sum(validator_scores) / len(validator_scores)
        else:
            overall_score = 0.0
        
        # Adjust score based on automation analysis
        if not automation_results.get('automation_skipped', False):
            vagueness_penalty = min(automation_results.get('vagueness_analysis', {}).get('density', 0) * 0.5, 10)
            dependency_penalty = max(0, (100 - automation_results.get('dependency_analysis', {}).get('self_sufficiency_score', 100)) * 0.3)
            overall_score = max(0, overall_score - vagueness_penalty - dependency_penalty)
        
        # Determine quality classification and approval
        quality_classification = self._classify_quality(overall_score)
        approval_status = "APPROVED" if overall_score >= self.quality_threshold and not any(
            issue.severity == ValidationSeverity.CRITICAL for issue in all_issues
        ) else "NEEDS_IMPROVEMENT"
        
        validation_time = asyncio.get_event_loop().time() - start_time
        
        return FrameworkValidationResult(
            file_path=file_path,
            validation_type=validation_type,
            overall_score=overall_score,
            component_scores=component_scores,
            quality_classification=quality_classification,
            approval_status=approval_status,
            issues=all_issues,
            strengths=all_strengths,
            recommendations=all_recommendations,
            validation_time=validation_time,
            framework_version=self.framework_version
        )
    
    def _classify_quality(self, score: float) -> str:
        """Classify quality based on score"""
        if score >= 90:
            return "EXCELLENT"
        elif score >= 80:
            return "GOOD"
        elif score >= 70:
            return "ACCEPTABLE"
        elif score >= 60:
            return "NEEDS_IMPROVEMENT"
        else:
            return "UNACCEPTABLE"
    
    def _update_validation_metrics(self, result: FrameworkValidationResult, start_time: float):
        """Update validation metrics"""
        self.validation_metrics['total_validations'] += 1
        
        if result.is_passing(self.quality_threshold):
            self.validation_metrics['passed_validations'] += 1
        else:
            self.validation_metrics['failed_validations'] += 1
        
        # Update average validation time
        total_validations = self.validation_metrics['total_validations']
        current_avg = self.validation_metrics['average_validation_time']
        new_time = result.validation_time
        
        self.validation_metrics['average_validation_time'] = (
            (current_avg * (total_validations - 1) + new_time) / total_validations
        )
    
    async def batch_validate_files(self, file_paths: List[str], 
                                 validation_type: ValidationType = ValidationType.PRE_UPDATE) -> List[FrameworkValidationResult]:
        """Validate multiple files in batch"""
        logger.info(f"Batch validating {len(file_paths)} files")
        
        # Create validation tasks
        tasks = []
        for file_path in file_paths:
            task = self.validate_instruction_file(file_path, validation_type)
            tasks.append(task)
        
        # Execute all validations concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        validation_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Batch validation failed for {file_paths[i]}: {result}")
                # Create error result
                error_result = FrameworkValidationResult(
                    file_path=file_paths[i],
                    validation_type=validation_type,
                    overall_score=0.0,
                    component_scores={},
                    quality_classification="BATCH_ERROR",
                    approval_status="FAILED",
                    issues=[ValidationIssue(
                        severity=ValidationSeverity.CRITICAL,
                        category="batch_error",
                        message=f"Batch validation failed: {str(result)}",
                        line_number=None,
                        suggestion="Check file accessibility and framework configuration",
                        tool_source="framework_connector"
                    )],
                    strengths=[],
                    recommendations=["Resolve batch validation issues"],
                    validation_time=0.0,
                    framework_version=self.framework_version
                )
                validation_results.append(error_result)
            else:
                validation_results.append(result)
        
        return validation_results
    
    async def get_validation_metrics(self) -> Dict[str, Any]:
        """Get validation metrics and statistics"""
        total = self.validation_metrics['total_validations']
        
        return {
            'total_validations': total,
            'passed_validations': self.validation_metrics['passed_validations'],
            'failed_validations': self.validation_metrics['failed_validations'],
            'rollbacks_triggered': self.validation_metrics['rollbacks_triggered'],
            'framework_errors': self.validation_metrics['framework_errors'],
            'success_rate': self.validation_metrics['passed_validations'] / max(total, 1),
            'average_validation_time': self.validation_metrics['average_validation_time'],
            'quality_threshold': self.quality_threshold,
            'framework_version': self.framework_version,
            'available_validators': list(self.available_validators.keys()),
            'available_automation_tools': list(self.available_automation_tools.keys()),
            'timestamp': datetime.utcnow().isoformat()
        }


async def main():
    """Main function for testing"""
    try:
        # Initialize framework connector
        config = {
            'quality_threshold': 75.0,
            'validation_timeout': 60,
            'enable_parallel_validation': True
        }
        
        connector = AIInstructionFrameworkConnector(config)
        
        # Test validation
        test_file = '/Users/georgiospilitsoglou/Developer/projects/mypromptflow/.claude/commands/ai-help.md'
        if Path(test_file).exists():
            result = await connector.validate_instruction_file(test_file, ValidationType.PRE_UPDATE)
            
            print("Framework Connector Test Results:")
            print(f"File: {result.file_path}")
            print(f"Overall Score: {result.overall_score:.1f}/100")
            print(f"Quality: {result.quality_classification}")
            print(f"Status: {result.approval_status}")
            print(f"Issues: {len(result.issues)}")
            print(f"Strengths: {len(result.strengths)}")
            print(f"Validation Time: {result.validation_time:.2f}s")
        
        # Get metrics
        metrics = await connector.get_validation_metrics()
        print("\nValidation Metrics:")
        print(json.dumps(metrics, indent=2))
        
        print("\nFramework Connector test completed successfully!")
        
    except Exception as e:
        print(f"Error testing framework connector: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(asyncio.run(main()))