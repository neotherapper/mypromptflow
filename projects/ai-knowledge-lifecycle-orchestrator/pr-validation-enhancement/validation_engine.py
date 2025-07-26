#!/usr/bin/env python3
"""
Technology Validation Engine
AI Knowledge Lifecycle Orchestrator - PR Validation Enhancement

Validates technology usage, versions, and patterns against current best practices
and knowledge base information. Provides recommendations for improvements and
identifies outdated or deprecated patterns.
"""

import re
import logging
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import json


@dataclass
class ValidationIssue:
    """Validation issue data structure"""
    issue_type: str
    severity: str
    technology: str
    file_path: str
    line_number: Optional[int]
    message: str
    recommendation: str
    current_value: Optional[str]
    suggested_value: Optional[str]
    documentation_url: Optional[str]


@dataclass
class TechnologyValidationResult:
    """Technology validation result data structure"""
    technology_name: str
    current_version_detected: Optional[str]
    latest_version_available: Optional[str]
    version_status: str  # 'current', 'outdated', 'deprecated', 'unknown'
    validation_score: float
    issues: List[ValidationIssue]
    recommendations: List[str]
    compatibility_warnings: List[str]


@dataclass
class ValidationEngineResult:
    """Complete validation engine result"""
    overall_score: float
    total_technologies_validated: int
    validation_passed: bool
    critical_issues: List[ValidationIssue]
    technology_results: List[TechnologyValidationResult]
    recommendations: List[Dict[str, Any]]
    validation_summary: Dict[str, Any]
    processing_time: float


class TechnologyValidationEngine:
    """Validates technology usage and provides improvement recommendations"""
    
    def __init__(self, knowledge_vault, config: Dict[str, Any]):
        """Initialize the validation engine"""
        self.knowledge_vault = knowledge_vault
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Load validation rules
        self.validation_rules = self._load_validation_rules()
        self.deprecation_patterns = self._load_deprecation_patterns()
        self.version_policies = self._load_version_policies()
        
        self.logger.info("Technology Validation Engine initialized")
    
    def _load_validation_rules(self) -> Dict[str, Any]:
        """Load technology validation rules"""
        return {
            'version_validation': {
                'max_version_age_months': 12,
                'critical_version_age_months': 24,
                'require_semantic_versioning': True,
                'allow_prerelease': False
            },
            'security_validation': {
                'check_known_vulnerabilities': True,
                'require_security_updates': True,
                'minimum_security_score': 80
            },
            'compatibility_validation': {
                'check_peer_dependencies': True,
                'validate_node_version': True,
                'check_browser_compatibility': True
            },
            'best_practices': {
                'enforce_typescript': True,
                'require_testing_framework': True,
                'validate_build_tools': True,
                'check_linting_setup': True
            }
        }
    
    def _load_deprecation_patterns(self) -> Dict[str, Any]:
        """Load patterns for detecting deprecated usage"""
        return {
            'react': {
                'deprecated_patterns': [
                    {
                        'pattern': r'React\.createClass',
                        'message': 'React.createClass is deprecated, use function components or ES6 classes',
                        'severity': 'high',
                        'replacement': 'function component or React.Component class'
                    },
                    {
                        'pattern': r'componentWillMount|componentWillReceiveProps|componentWillUpdate',
                        'message': 'Deprecated lifecycle methods detected',
                        'severity': 'medium',
                        'replacement': 'useEffect hook or new lifecycle methods'
                    },
                    {
                        'pattern': r'findDOMNode',
                        'message': 'findDOMNode is deprecated',
                        'severity': 'medium',
                        'replacement': 'useRef hook'
                    }
                ],
                'version_specific': {
                    '16.x': ['React.createClass', 'PropTypes from react'],
                    '17.x': ['componentWillMount', 'componentWillReceiveProps'],
                    '18.x': ['ReactDOM.render without createRoot']
                }
            },
            'typescript': {
                'deprecated_patterns': [
                    {
                        'pattern': r'namespace\s+\w+',
                        'message': 'TypeScript namespaces are discouraged, use ES6 modules',
                        'severity': 'low',
                        'replacement': 'ES6 modules (import/export)'
                    },
                    {
                        'pattern': r'module\s+\w+',
                        'message': 'TypeScript modules are deprecated, use ES6 modules',
                        'severity': 'medium',
                        'replacement': 'ES6 modules (import/export)'
                    }
                ]
            },
            'javascript': {
                'deprecated_patterns': [
                    {
                        'pattern': r'var\s+\w+',
                        'message': 'var declarations should be replaced with let/const',
                        'severity': 'low',
                        'replacement': 'let or const'
                    },
                    {
                        'pattern': r'\.substr\(',
                        'message': 'String.substr() is deprecated, use substring() or slice()',
                        'severity': 'low',
                        'replacement': 'substring() or slice()'
                    }
                ]
            },
            'python': {
                'deprecated_patterns': [
                    {
                        'pattern': r'import imp\b',
                        'message': 'imp module is deprecated since Python 3.4, use importlib',
                        'severity': 'medium',
                        'replacement': 'importlib'
                    },
                    {
                        'pattern': r'\.format\(\)',
                        'message': 'Consider using f-strings for better performance and readability',
                        'severity': 'low',
                        'replacement': 'f-string syntax'
                    }
                ]
            }
        }
    
    def _load_version_policies(self) -> Dict[str, Any]:
        """Load version policies for different technologies"""
        return {
            'react': {
                'minimum_supported': '16.8.0',
                'recommended': '18.2.0',
                'latest_stable': '18.2.0',
                'eol_versions': ['15.x', '16.0.x', '16.1.x', '16.2.x']
            },
            'typescript': {
                'minimum_supported': '4.0.0',
                'recommended': '5.0.0',
                'latest_stable': '5.1.6',
                'eol_versions': ['3.x', '2.x']
            },
            'next.js': {
                'minimum_supported': '12.0.0',
                'recommended': '13.4.0',
                'latest_stable': '13.4.19',
                'eol_versions': ['10.x', '11.x']
            },
            'node.js': {
                'minimum_supported': '16.0.0',
                'recommended': '18.17.0',
                'latest_stable': '20.5.0',
                'eol_versions': ['12.x', '14.x']
            }
        }
    
    def validate_technologies(self, pr_request, context_analysis) -> ValidationEngineResult:
        """
        Validate all technologies detected in the PR
        
        Args:
            pr_request: PRValidationRequest object
            context_analysis: PRContextAnalysis from context analyzer
            
        Returns:
            ValidationEngineResult: Complete validation results
        """
        start_time = datetime.now()
        self.logger.info(f"Starting technology validation for PR #{pr_request.pr_id}")
        
        technology_results = []
        all_issues = []
        all_recommendations = []
        
        # Validate each detected technology
        for tech_detection in context_analysis.detected_technologies:
            tech_result = self._validate_single_technology(
                tech_detection, 
                context_analysis,
                pr_request
            )
            technology_results.append(tech_result)
            all_issues.extend(tech_result.issues)
            all_recommendations.extend(tech_result.recommendations)
        
        # Calculate overall score
        if technology_results:
            overall_score = sum(t.validation_score for t in technology_results) / len(technology_results)
        else:
            overall_score = 100.0  # No technologies detected = perfect score
        
        # Identify critical issues
        critical_issues = [issue for issue in all_issues if issue.severity == 'critical']
        
        # Determine if validation passed
        min_score = self.config.get('quality_thresholds', {}).get('technology_currency_score', {}).get('minimum', 60)
        validation_passed = overall_score >= min_score and len(critical_issues) == 0
        
        # Create validation summary
        validation_summary = self._create_validation_summary(
            technology_results, 
            all_issues, 
            context_analysis
        )
        
        # Create structured recommendations
        structured_recommendations = self._create_structured_recommendations(
            all_recommendations, 
            technology_results
        )
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        result = ValidationEngineResult(
            overall_score=overall_score,
            total_technologies_validated=len(technology_results),
            validation_passed=validation_passed,
            critical_issues=critical_issues,
            technology_results=technology_results,
            recommendations=structured_recommendations,
            validation_summary=validation_summary,
            processing_time=processing_time
        )
        
        self.logger.info(
            f"Technology validation completed for PR #{pr_request.pr_id}: "
            f"Score: {overall_score:.1f}, Issues: {len(all_issues)}, "
            f"Critical: {len(critical_issues)}"
        )
        
        return result
    
    def _validate_single_technology(self, tech_detection, context_analysis, pr_request) -> TechnologyValidationResult:
        """Validate a single technology"""
        tech_name = tech_detection.name.lower()
        issues = []
        recommendations = []
        compatibility_warnings = []
        
        # Get knowledge vault information
        vault_info = self._get_technology_info_from_vault(tech_name)
        
        # Validate version
        version_result = self._validate_version(tech_detection, vault_info)
        issues.extend(version_result['issues'])
        recommendations.extend(version_result['recommendations'])
        
        # Check for deprecated patterns
        deprecation_result = self._check_deprecated_patterns(tech_detection, context_analysis)
        issues.extend(deprecation_result['issues'])
        recommendations.extend(deprecation_result['recommendations'])
        
        # Validate security aspects
        security_result = self._validate_security_aspects(tech_detection, vault_info)
        issues.extend(security_result['issues'])
        recommendations.extend(security_result['recommendations'])
        
        # Check compatibility
        compatibility_result = self._check_compatibility(tech_detection, context_analysis)
        compatibility_warnings.extend(compatibility_result['warnings'])
        recommendations.extend(compatibility_result['recommendations'])
        
        # Calculate validation score
        validation_score = self._calculate_technology_score(issues, tech_detection)
        
        # Determine version status
        version_status = self._determine_version_status(tech_detection, vault_info)
        
        return TechnologyValidationResult(
            technology_name=tech_detection.name,
            current_version_detected=tech_detection.version_detected,
            latest_version_available=vault_info.get('current_version') if vault_info else None,
            version_status=version_status,
            validation_score=validation_score,
            issues=issues,
            recommendations=recommendations,
            compatibility_warnings=compatibility_warnings
        )
    
    def _get_technology_info_from_vault(self, tech_name: str) -> Optional[Dict[str, Any]]:
        """Get technology information from knowledge vault"""
        try:
            entries = self.knowledge_vault.query_technologies({'technology_name': tech_name})
            return entries[0] if entries else None
        except Exception as e:
            self.logger.warning(f"Failed to get technology info for {tech_name}: {str(e)}")
            return None
    
    def _validate_version(self, tech_detection, vault_info: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate technology version"""
        issues = []
        recommendations = []
        
        tech_name = tech_detection.name.lower()
        detected_version = tech_detection.version_detected
        
        # Check if we have version information
        if not detected_version:
            if tech_name in self.version_policies:
                issues.append(ValidationIssue(
                    issue_type='version_missing',
                    severity='medium',
                    technology=tech_detection.name,
                    file_path=tech_detection.file_references[0] if tech_detection.file_references else 'unknown',
                    line_number=None,
                    message=f'No version detected for {tech_detection.name}',
                    recommendation=f'Specify version constraint in dependency file',
                    current_value=None,
                    suggested_value=self.version_policies[tech_name].get('recommended'),
                    documentation_url=None
                ))
            return {'issues': issues, 'recommendations': recommendations}
        
        # Check against version policies
        if tech_name in self.version_policies:
            policy = self.version_policies[tech_name]
            
            # Check if version is deprecated/EOL
            if any(detected_version.startswith(eol) for eol in policy.get('eol_versions', [])):
                issues.append(ValidationIssue(
                    issue_type='version_eol',
                    severity='critical',
                    technology=tech_detection.name,
                    file_path=tech_detection.file_references[0] if tech_detection.file_references else 'unknown',
                    line_number=None,
                    message=f'{tech_detection.name} version {detected_version} is end-of-life',
                    recommendation=f'Upgrade to {policy.get("recommended")} or later',
                    current_value=detected_version,
                    suggested_value=policy.get('recommended'),
                    documentation_url=None
                ))
            
            # Check if version is below minimum supported
            elif self._version_compare(detected_version, policy.get('minimum_supported', '0.0.0')) < 0:
                issues.append(ValidationIssue(
                    issue_type='version_too_old',
                    severity='high',
                    technology=tech_detection.name,
                    file_path=tech_detection.file_references[0] if tech_detection.file_references else 'unknown',
                    line_number=None,
                    message=f'{tech_detection.name} version {detected_version} is below minimum supported version',
                    recommendation=f'Upgrade to {policy.get("minimum_supported")} or later',
                    current_value=detected_version,
                    suggested_value=policy.get('minimum_supported'),
                    documentation_url=None
                ))
            
            # Check if version is below recommended
            elif self._version_compare(detected_version, policy.get('recommended', '0.0.0')) < 0:
                recommendations.append(
                    f'Consider upgrading {tech_detection.name} from {detected_version} to {policy.get("recommended")} '
                    f'for latest features and security updates'
                )
        
        # Check against knowledge vault information
        if vault_info:
            vault_version = vault_info.get('current_version')
            if vault_version and detected_version != vault_version:
                if self._version_compare(detected_version, vault_version) < 0:
                    recommendations.append(
                        f'{tech_detection.name} can be updated from {detected_version} to {vault_version}'
                    )
        
        return {'issues': issues, 'recommendations': recommendations}
    
    def _check_deprecated_patterns(self, tech_detection, context_analysis) -> Dict[str, Any]:
        """Check for deprecated patterns in the technology usage"""
        issues = []
        recommendations = []
        
        tech_name = tech_detection.name.lower()
        
        if tech_name not in self.deprecation_patterns:
            return {'issues': issues, 'recommendations': recommendations}
        
        patterns = self.deprecation_patterns[tech_name].get('deprecated_patterns', [])
        
        # Check each file that uses this technology
        for file_analysis in context_analysis.file_analyses:
            if any(t.name.lower() == tech_name for t in file_analysis.technologies_detected):
                # Get file content (would need actual implementation)
                file_content = self._get_file_content(file_analysis.filename, context_analysis)
                
                for pattern_info in patterns:
                    matches = re.finditer(pattern_info['pattern'], file_content, re.IGNORECASE | re.MULTILINE)
                    
                    for match in matches:
                        line_number = file_content[:match.start()].count('\n') + 1
                        
                        issues.append(ValidationIssue(
                            issue_type='deprecated_pattern',
                            severity=pattern_info['severity'],
                            technology=tech_detection.name,
                            file_path=file_analysis.filename,
                            line_number=line_number,
                            message=pattern_info['message'],
                            recommendation=f"Replace with {pattern_info['replacement']}",
                            current_value=match.group(0),
                            suggested_value=pattern_info['replacement'],
                            documentation_url=None
                        ))
        
        return {'issues': issues, 'recommendations': recommendations}
    
    def _validate_security_aspects(self, tech_detection, vault_info: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate security aspects of technology usage"""
        issues = []
        recommendations = []
        
        # Check if technology has known security issues
        if vault_info:
            # Check for recent security changes
            tech_name = tech_detection.name
            try:
                security_changes = self.knowledge_vault.query_change_events({
                    'technology_name': tech_name,
                    'change_type': 'security_update'
                })
                
                if security_changes:
                    recent_security_changes = [
                        c for c in security_changes 
                        if self._is_recent_change(c.get('detected_date'))
                    ]
                    
                    if recent_security_changes:
                        issues.append(ValidationIssue(
                            issue_type='security_update_available',
                            severity='high',
                            technology=tech_detection.name,
                            file_path=tech_detection.file_references[0] if tech_detection.file_references else 'unknown',
                            line_number=None,
                            message=f'Recent security updates available for {tech_detection.name}',
                            recommendation='Review and apply latest security updates',
                            current_value=tech_detection.version_detected,
                            suggested_value='latest',
                            documentation_url=None
                        ))
            
            except Exception as e:
                self.logger.warning(f"Failed to check security changes for {tech_name}: {str(e)}")
        
        return {'issues': issues, 'recommendations': recommendations}
    
    def _check_compatibility(self, tech_detection, context_analysis) -> Dict[str, Any]:
        """Check compatibility with other technologies"""
        warnings = []
        recommendations = []
        
        # Get all detected technologies
        all_technologies = {t.name.lower(): t for t in context_analysis.detected_technologies}
        
        # Check known compatibility issues
        compatibility_rules = {
            'react': {
                'compatible_with': ['typescript', 'next.js', 'webpack'],
                'incompatible_with': [],
                'version_constraints': {
                    'typescript': '>= 4.0.0',
                    'next.js': '>= 12.0.0'
                }
            },
            'typescript': {
                'compatible_with': ['react', 'next.js', 'express'],
                'incompatible_with': [],
                'version_constraints': {
                    'react': '>= 16.8.0'
                }
            }
        }
        
        tech_name = tech_detection.name.lower()
        if tech_name in compatibility_rules:
            rules = compatibility_rules[tech_name]
            
            # Check for incompatible technologies
            for incompatible in rules.get('incompatible_with', []):
                if incompatible in all_technologies:
                    warnings.append(
                        f'{tech_detection.name} may have compatibility issues with {incompatible}'
                    )
            
            # Check version constraints
            for constraint_tech, constraint_version in rules.get('version_constraints', {}).items():
                if constraint_tech in all_technologies:
                    other_tech = all_technologies[constraint_tech]
                    if other_tech.version_detected:
                        # Simple version check (would need proper semver parsing)
                        if constraint_version.startswith('>='):
                            min_version = constraint_version[2:].strip()
                            if self._version_compare(other_tech.version_detected, min_version) < 0:
                                warnings.append(
                                    f'{tech_detection.name} requires {constraint_tech} {constraint_version}, '
                                    f'but {other_tech.version_detected} is detected'
                                )
        
        return {'warnings': warnings, 'recommendations': recommendations}
    
    def _calculate_technology_score(self, issues: List[ValidationIssue], tech_detection) -> float:
        """Calculate validation score for a technology"""
        base_score = 100.0
        
        # Deduct points based on issue severity
        for issue in issues:
            if issue.severity == 'critical':
                base_score -= 25
            elif issue.severity == 'high':
                base_score -= 15
            elif issue.severity == 'medium':
                base_score -= 10
            elif issue.severity == 'low':
                base_score -= 5
        
        # Bonus points for high confidence detection
        if tech_detection.confidence > 0.8:
            base_score += 5
        
        return max(0.0, min(100.0, base_score))
    
    def _determine_version_status(self, tech_detection, vault_info: Optional[Dict[str, Any]]) -> str:
        """Determine the status of the detected version"""
        if not tech_detection.version_detected:
            return 'unknown'
        
        tech_name = tech_detection.name.lower()
        detected_version = tech_detection.version_detected
        
        # Check against version policies
        if tech_name in self.version_policies:
            policy = self.version_policies[tech_name]
            
            # Check if EOL
            if any(detected_version.startswith(eol) for eol in policy.get('eol_versions', [])):
                return 'deprecated'
            
            # Check if current with recommended
            if detected_version == policy.get('recommended'):
                return 'current'
            
            # Check if below minimum
            if self._version_compare(detected_version, policy.get('minimum_supported', '0.0.0')) < 0:
                return 'deprecated'
            
            # Check if below recommended
            if self._version_compare(detected_version, policy.get('recommended', '0.0.0')) < 0:
                return 'outdated'
        
        # Check against knowledge vault
        if vault_info:
            vault_version = vault_info.get('current_version')
            if vault_version:
                if detected_version == vault_version:
                    return 'current'
                elif self._version_compare(detected_version, vault_version) < 0:
                    return 'outdated'
        
        return 'unknown'
    
    def _version_compare(self, version1: str, version2: str) -> int:
        """
        Compare two semantic versions
        Returns: -1 if version1 < version2, 0 if equal, 1 if version1 > version2
        """
        try:
            # Simple version comparison (would need proper semver library in production)
            v1_parts = [int(x) for x in version1.split('.')]
            v2_parts = [int(x) for x in version2.split('.')]
            
            # Pad shorter version with zeros
            max_len = max(len(v1_parts), len(v2_parts))
            v1_parts.extend([0] * (max_len - len(v1_parts)))
            v2_parts.extend([0] * (max_len - len(v2_parts)))
            
            for i in range(max_len):
                if v1_parts[i] < v2_parts[i]:
                    return -1
                elif v1_parts[i] > v2_parts[i]:
                    return 1
            
            return 0
        except (ValueError, AttributeError):
            return 0  # Can't compare, treat as equal
    
    def _get_file_content(self, filename: str, context_analysis) -> str:
        """Get file content for pattern matching (placeholder implementation)"""
        # In a real implementation, this would get the actual file content
        # For now, return a placeholder that allows pattern matching
        return f"// Content of {filename}\n// Pattern matching placeholder"
    
    def _is_recent_change(self, detected_date: Optional[str]) -> bool:
        """Check if a change is recent (within last 30 days)"""
        if not detected_date:
            return False
        
        try:
            change_date = datetime.fromisoformat(detected_date.replace('Z', '+00:00'))
            return (datetime.now() - change_date).days <= 30
        except (ValueError, AttributeError):
            return False
    
    def _create_validation_summary(self, technology_results: List[TechnologyValidationResult], 
                                 issues: List[ValidationIssue], context_analysis) -> Dict[str, Any]:
        """Create validation summary"""
        return {
            'total_technologies': len(technology_results),
            'technologies_with_issues': len([t for t in technology_results if t.issues]),
            'total_issues': len(issues),
            'issues_by_severity': {
                'critical': len([i for i in issues if i.severity == 'critical']),
                'high': len([i for i in issues if i.severity == 'high']),
                'medium': len([i for i in issues if i.severity == 'medium']),
                'low': len([i for i in issues if i.severity == 'low'])
            },
            'version_status_summary': {
                'current': len([t for t in technology_results if t.version_status == 'current']),
                'outdated': len([t for t in technology_results if t.version_status == 'outdated']),
                'deprecated': len([t for t in technology_results if t.version_status == 'deprecated']),
                'unknown': len([t for t in technology_results if t.version_status == 'unknown'])
            },
            'average_score': sum(t.validation_score for t in technology_results) / len(technology_results) if technology_results else 100.0
        }
    
    def _create_structured_recommendations(self, recommendations: List[str], 
                                         technology_results: List[TechnologyValidationResult]) -> List[Dict[str, Any]]:
        """Create structured recommendations"""
        structured = []
        
        # Group recommendations by type
        version_updates = []
        deprecation_fixes = []
        security_updates = []
        general_improvements = []
        
        for tech_result in technology_results:
            for issue in tech_result.issues:
                if issue.issue_type in ['version_eol', 'version_too_old']:
                    version_updates.append({
                        'type': 'version_update',
                        'priority': 'high' if issue.severity in ['critical', 'high'] else 'medium',
                        'technology': issue.technology,
                        'current_version': issue.current_value,
                        'suggested_version': issue.suggested_value,
                        'message': issue.message,
                        'action': issue.recommendation
                    })
                elif issue.issue_type == 'deprecated_pattern':
                    deprecation_fixes.append({
                        'type': 'deprecation_fix',
                        'priority': 'medium',
                        'technology': issue.technology,
                        'file': issue.file_path,
                        'line': issue.line_number,
                        'pattern': issue.current_value,
                        'replacement': issue.suggested_value,
                        'message': issue.message
                    })
                elif issue.issue_type == 'security_update_available':
                    security_updates.append({
                        'type': 'security_update',
                        'priority': 'high',
                        'technology': issue.technology,
                        'message': issue.message,
                        'action': issue.recommendation
                    })
        
        # Add general recommendations
        for rec in recommendations:
            general_improvements.append({
                'type': 'general_improvement',
                'priority': 'low',
                'message': rec,
                'action': 'review_and_consider'
            })
        
        # Combine all recommendations
        structured.extend(version_updates)
        structured.extend(security_updates)
        structured.extend(deprecation_fixes)
        structured.extend(general_improvements[:10])  # Limit general recommendations
        
        return structured
    
    def validate_configuration(self) -> Dict[str, Any]:
        """Validate engine configuration"""
        return {
            'status': 'healthy',
            'validation_rules_loaded': len(self.validation_rules),
            'deprecation_patterns_loaded': len(self.deprecation_patterns),
            'version_policies_loaded': len(self.version_policies),
            'knowledge_vault_available': self.knowledge_vault is not None
        }