#!/usr/bin/env python3
"""
Consistency Validator
AI Knowledge Lifecycle Orchestrator - PR Validation Enhancement

Validates project consistency including dependency patterns, architecture consistency,
coding standards, and documentation consistency. Ensures PR changes align with
existing project patterns and conventions.
"""

import re
import json
import logging
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path


@dataclass
class ConsistencyViolation:
    """Consistency violation data structure"""
    violation_id: str
    violation_type: str
    severity: str  # 'critical', 'high', 'medium', 'low'
    category: str  # 'dependency', 'architecture', 'coding_standards', 'documentation'
    file_path: str
    line_number: Optional[int]
    description: str
    expected_pattern: str
    actual_pattern: str
    recommendation: str
    confidence: float
    impact_scope: str  # 'file', 'module', 'project'


@dataclass
class ConsistencyMetrics:
    """Consistency metrics data structure"""
    overall_consistency_score: float
    dependency_consistency_score: float
    architecture_consistency_score: float
    coding_standards_score: float
    documentation_consistency_score: float
    total_violations: int
    violations_by_severity: Dict[str, int]
    compliance_percentage: float


@dataclass
class ConsistencyValidationResult:
    """Complete consistency validation result"""
    pr_id: str
    consistency_score: float
    validation_passed: bool
    violations: List[ConsistencyViolation]
    consistency_metrics: ConsistencyMetrics
    dependency_analysis: Dict[str, Any]
    architecture_analysis: Dict[str, Any]
    coding_standards_analysis: Dict[str, Any]
    documentation_analysis: Dict[str, Any]
    recommendations: List[Dict[str, Any]]
    processing_time: float


class ConsistencyValidator:
    """Validates project consistency and coding standards"""
    
    def __init__(self, knowledge_vault, config: Dict[str, Any]):
        """Initialize the consistency validator"""
        self.knowledge_vault = knowledge_vault
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Load consistency rules and patterns
        self.consistency_patterns = self._load_consistency_patterns()
        self.coding_standards = self._load_coding_standards()
        self.architecture_patterns = self._load_architecture_patterns()
        
        self.logger.info("Consistency Validator initialized")
    
    def _load_consistency_patterns(self) -> Dict[str, Any]:
        """Load consistency validation patterns"""
        return {
            'dependency_patterns': {
                'import_style_consistency': {
                    'javascript': {
                        'patterns': [
                            {
                                'name': 'es6_imports',
                                'pattern': r'import\s+.*\s+from\s+["\'][^"\']+["\']',
                                'preferred': True,
                                'description': 'ES6 import statements'
                            },
                            {
                                'name': 'require_statements',
                                'pattern': r'const\s+.*=\s+require\(["\'][^"\']+["\']\)',
                                'preferred': False,
                                'description': 'CommonJS require statements'
                            }
                        ]
                    },
                    'python': {
                        'patterns': [
                            {
                                'name': 'absolute_imports',
                                'pattern': r'from\s+\w+(?:\.\w+)*\s+import',
                                'preferred': True,
                                'description': 'Absolute import statements'
                            },
                            {
                                'name': 'relative_imports',
                                'pattern': r'from\s+\.+\w*\s+import',
                                'preferred': False,
                                'description': 'Relative import statements'
                            }
                        ]
                    }
                },
                'dependency_organization': {
                    'grouping_rules': [
                        {
                            'name': 'standard_library_first',
                            'description': 'Standard library imports should come first',
                            'pattern': r'^(import|from)\s+(os|sys|json|re|datetime|pathlib)',
                            'order': 1
                        },
                        {
                            'name': 'third_party_second',
                            'description': 'Third-party imports should come second',
                            'pattern': r'^(import|from)\s+(react|express|numpy|pandas|requests)',
                            'order': 2
                        },
                        {
                            'name': 'local_imports_last',
                            'description': 'Local imports should come last',
                            'pattern': r'^(import|from)\s+\.',
                            'order': 3
                        }
                    ]
                }
            },
            'naming_conventions': {
                'javascript': {
                    'variables': {
                        'pattern': r'^[a-z][a-zA-Z0-9]*$',
                        'style': 'camelCase',
                        'description': 'Variables should use camelCase'
                    },
                    'functions': {
                        'pattern': r'^[a-z][a-zA-Z0-9]*$',
                        'style': 'camelCase',
                        'description': 'Functions should use camelCase'
                    },
                    'constants': {
                        'pattern': r'^[A-Z][A-Z0-9_]*$',
                        'style': 'UPPER_SNAKE_CASE',
                        'description': 'Constants should use UPPER_SNAKE_CASE'
                    },
                    'classes': {
                        'pattern': r'^[A-Z][a-zA-Z0-9]*$',
                        'style': 'PascalCase',
                        'description': 'Classes should use PascalCase'
                    }
                },
                'python': {
                    'variables': {
                        'pattern': r'^[a-z][a-z0-9_]*$',
                        'style': 'snake_case',
                        'description': 'Variables should use snake_case'
                    },
                    'functions': {
                        'pattern': r'^[a-z][a-z0-9_]*$',
                        'style': 'snake_case',
                        'description': 'Functions should use snake_case'
                    },
                    'constants': {
                        'pattern': r'^[A-Z][A-Z0-9_]*$',
                        'style': 'UPPER_SNAKE_CASE',
                        'description': 'Constants should use UPPER_SNAKE_CASE'
                    },
                    'classes': {
                        'pattern': r'^[A-Z][a-zA-Z0-9]*$',
                        'style': 'PascalCase',
                        'description': 'Classes should use PascalCase'
                    }
                }
            },
            'file_organization': {
                'directory_structure': {
                    'frontend': {
                        'expected_dirs': ['src', 'components', 'hooks', 'utils', 'types'],
                        'file_patterns': {
                            'components': r'.*\.(?:jsx?|tsx?)$',
                            'hooks': r'use[A-Z].*\.(?:js|ts)$',
                            'utils': r'.*\.(?:js|ts)$',
                            'types': r'.*\.d\.ts$'
                        }
                    },
                    'backend': {
                        'expected_dirs': ['src', 'models', 'routes', 'middleware', 'utils'],
                        'file_patterns': {
                            'models': r'.*\.py$',
                            'routes': r'.*\.py$',
                            'middleware': r'.*\.py$',
                            'utils': r'.*\.py$'
                        }
                    }
                }
            }
        }
    
    def _load_coding_standards(self) -> Dict[str, Any]:
        """Load coding standards and style guidelines"""
        return {
            'javascript': {
                'formatting': {
                    'semicolons': {
                        'required': True,
                        'pattern': r';$',
                        'description': 'Statements should end with semicolons'
                    },
                    'quotes': {
                        'style': 'single',
                        'pattern': r"'[^']*'",
                        'description': 'Use single quotes for strings'
                    },
                    'indentation': {
                        'style': 'spaces',
                        'size': 2,
                        'pattern': r'^  ',
                        'description': 'Use 2 spaces for indentation'
                    }
                },
                'best_practices': {
                    'strict_equality': {
                        'pattern': r'===|!==',
                        'avoid_pattern': r'==|!=',
                        'description': 'Use strict equality operators'
                    },
                    'const_declarations': {
                        'pattern': r'const\s+\w+',
                        'prefer_over': r'var\s+\w+',
                        'description': 'Prefer const over var'
                    }
                }
            },
            'typescript': {
                'type_annotations': {
                    'function_returns': {
                        'pattern': r'function\s+\w+\([^)]*\):\s*\w+',
                        'description': 'Functions should have return type annotations'
                    },
                    'interface_definitions': {
                        'pattern': r'interface\s+\w+\s*{',
                        'description': 'Use interfaces for object types'
                    }
                },
                'strict_settings': {
                    'no_any': {
                        'avoid_pattern': r':\s*any\b',
                        'description': 'Avoid using any type'
                    },
                    'null_checks': {
                        'pattern': r'\?\.|??|!\.`,
                        'description': 'Use optional chaining and nullish coalescing'
                    }
                }
            },
            'python': {
                'pep8_compliance': {
                    'line_length': {
                        'max_length': 88,
                        'description': 'Lines should not exceed 88 characters'
                    },
                    'imports': {
                        'pattern': r'^(import|from)',
                        'description': 'Imports should be at top of file'
                    }
                },
                'docstrings': {
                    'functions': {
                        'pattern': r'def\s+\w+\([^)]*\):\s*"""',
                        'description': 'Functions should have docstrings'
                    },
                    'classes': {
                        'pattern': r'class\s+\w+.*:\s*"""',
                        'description': 'Classes should have docstrings'
                    }
                }
            }
        }
    
    def _load_architecture_patterns(self) -> Dict[str, Any]:
        """Load architecture consistency patterns"""
        return {
            'component_structure': {
                'react': {
                    'functional_components': {
                        'pattern': r'const\s+\w+\s*=\s*\([^)]*\)\s*=>\s*{',
                        'description': 'Prefer functional components over class components'
                    },
                    'hooks_usage': {
                        'patterns': [
                            r'useState\(',
                            r'useEffect\(',
                            r'useContext\(',
                            r'use\w+\('
                        ],
                        'description': 'Use React hooks for state management'
                    },
                    'prop_types': {
                        'typescript_pattern': r'interface\s+\w+Props',
                        'description': 'Define TypeScript interfaces for props'
                    }
                }
            },
            'module_structure': {
                'separation_of_concerns': {
                    'patterns': [
                        {
                            'name': 'business_logic_separation',
                            'description': 'Business logic should be separated from UI',
                            'check': 'hooks_for_logic'
                        },
                        {
                            'name': 'api_layer_separation',
                            'description': 'API calls should be in dedicated modules',
                            'check': 'api_modules'
                        }
                    ]
                }
            },
            'dependency_injection': {
                'python': {
                    'patterns': [
                        {
                            'name': 'constructor_injection',
                            'pattern': r'def\s+__init__\(self,.*\w+:\s*\w+',
                            'description': 'Use constructor injection for dependencies'
                        }
                    ]
                }
            }
        }
    
    def validate_consistency(self, pr_request, context_analysis) -> ConsistencyValidationResult:
        """
        Validate project consistency across multiple dimensions
        
        Args:
            pr_request: PRValidationRequest object
            context_analysis: PRContextAnalysis from context analyzer
            
        Returns:
            ConsistencyValidationResult: Complete consistency validation
        """
        start_time = datetime.now()
        self.logger.info(f"Starting consistency validation for PR #{pr_request.pr_id}")
        
        violations = []
        
        # Phase 1: Dependency Consistency Analysis
        dependency_analysis = self._analyze_dependency_consistency(context_analysis)
        violations.extend(dependency_analysis['violations'])
        
        # Phase 2: Architecture Consistency Analysis
        architecture_analysis = self._analyze_architecture_consistency(context_analysis)
        violations.extend(architecture_analysis['violations'])
        
        # Phase 3: Coding Standards Analysis
        coding_standards_analysis = self._analyze_coding_standards(context_analysis)
        violations.extend(coding_standards_analysis['violations'])
        
        # Phase 4: Documentation Consistency Analysis
        documentation_analysis = self._analyze_documentation_consistency(context_analysis)
        violations.extend(documentation_analysis['violations'])
        
        # Calculate consistency metrics
        consistency_metrics = self._calculate_consistency_metrics(
            violations,
            dependency_analysis,
            architecture_analysis,
            coding_standards_analysis,
            documentation_analysis
        )
        
        # Determine overall validation result
        consistency_score = consistency_metrics.overall_consistency_score
        min_score = self.config.get('quality_thresholds', {}).get('consistency_score', {}).get('minimum', 70)
        validation_passed = consistency_score >= min_score
        
        # Generate recommendations
        recommendations = self._generate_consistency_recommendations(
            violations,
            dependency_analysis,
            architecture_analysis,
            coding_standards_analysis,
            documentation_analysis
        )
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        result = ConsistencyValidationResult(
            pr_id=pr_request.pr_id,
            consistency_score=consistency_score,
            validation_passed=validation_passed,
            violations=violations,
            consistency_metrics=consistency_metrics,
            dependency_analysis=dependency_analysis,
            architecture_analysis=architecture_analysis,
            coding_standards_analysis=coding_standards_analysis,
            documentation_analysis=documentation_analysis,
            recommendations=recommendations,
            processing_time=processing_time
        )
        
        self.logger.info(
            f"Consistency validation completed for PR #{pr_request.pr_id}: "
            f"Score: {consistency_score:.1f}, Violations: {len(violations)}, "
            f"Passed: {validation_passed}"
        )
        
        return result
    
    def _analyze_dependency_consistency(self, context_analysis) -> Dict[str, Any]:
        """Analyze dependency usage consistency"""
        violations = []
        analysis_summary = {
            'total_files_analyzed': len(context_analysis.file_analyses),
            'import_styles_found': {},
            'dependency_patterns': {},
            'inconsistencies_detected': 0
        }
        
        # Track import styles across files
        import_styles = {}
        
        for file_analysis in context_analysis.file_analyses:
            file_path = file_analysis.filename
            file_type = file_analysis.file_type
            
            # Get existing project dependencies for comparison
            existing_deps = self._get_existing_project_dependencies(file_analysis.technologies_detected)
            
            # Analyze import statements
            import_analysis = self._analyze_import_statements(file_analysis, file_type)
            
            # Check for consistency with existing patterns
            for style, count in import_analysis['styles'].items():
                if file_type not in import_styles:
                    import_styles[file_type] = {}
                if style not in import_styles[file_type]:
                    import_styles[file_type][style] = 0
                import_styles[file_type][style] += count
            
            # Check for dependency consistency violations
            dep_violations = self._check_dependency_violations(file_analysis, existing_deps)
            violations.extend(dep_violations)
            
            # Check import organization
            org_violations = self._check_import_organization(file_analysis, file_type)
            violations.extend(org_violations)
        
        # Analyze overall consistency
        for file_type, styles in import_styles.items():
            if len(styles) > 1:
                # Multiple import styles detected
                dominant_style = max(styles, key=styles.get)
                for style, count in styles.items():
                    if style != dominant_style and count > 0:
                        analysis_summary['inconsistencies_detected'] += 1
        
        analysis_summary['import_styles_found'] = import_styles
        
        # Calculate dependency consistency score
        total_possible_violations = len(context_analysis.file_analyses) * 3  # Rough estimate
        dependency_score = max(0, 100 - (len(violations) / max(total_possible_violations, 1)) * 100)
        
        return {
            'violations': violations,
            'summary': analysis_summary,
            'dependency_consistency_score': dependency_score
        }
    
    def _analyze_architecture_consistency(self, context_analysis) -> Dict[str, Any]:
        """Analyze architectural pattern consistency"""
        violations = []
        analysis_summary = {
            'component_patterns': {},
            'module_structure': {},
            'architecture_violations': 0
        }
        
        # Detect primary technology stack
        primary_technologies = self._identify_primary_technologies(context_analysis.detected_technologies)
        
        for file_analysis in context_analysis.file_analyses:
            file_content = self._get_file_content(file_analysis.filename, context_analysis)
            
            # Check React component patterns
            if any(tech.name.lower() == 'react' for tech in file_analysis.technologies_detected):
                react_violations = self._check_react_patterns(file_analysis, file_content)
                violations.extend(react_violations)
            
            # Check Python architecture patterns
            if file_analysis.file_type == 'python':
                python_violations = self._check_python_architecture(file_analysis, file_content)
                violations.extend(python_violations)
            
            # Check module structure consistency
            structure_violations = self._check_module_structure(file_analysis, primary_technologies)
            violations.extend(structure_violations)
        
        analysis_summary['architecture_violations'] = len(violations)
        
        # Calculate architecture consistency score
        architecture_score = max(0, 100 - len(violations) * 5)
        
        return {
            'violations': violations,
            'summary': analysis_summary,
            'architecture_consistency_score': architecture_score
        }
    
    def _analyze_coding_standards(self, context_analysis) -> Dict[str, Any]:
        """Analyze coding standards compliance"""
        violations = []
        analysis_summary = {
            'standards_checked': {},
            'violations_by_type': {},
            'compliance_percentage': 0
        }
        
        total_checks = 0
        passed_checks = 0
        
        for file_analysis in context_analysis.file_analyses:
            file_content = self._get_file_content(file_analysis.filename, context_analysis)
            file_type = self._get_language_from_file_type(file_analysis.file_type)
            
            if file_type not in self.coding_standards:
                continue
            
            standards = self.coding_standards[file_type]
            
            # Check formatting standards
            if 'formatting' in standards:
                format_violations = self._check_formatting_standards(
                    file_analysis, file_content, standards['formatting']
                )
                violations.extend(format_violations)
                total_checks += len(standards['formatting'])
                passed_checks += len(standards['formatting']) - len(format_violations)
            
            # Check best practices
            if 'best_practices' in standards:
                practice_violations = self._check_best_practices(
                    file_analysis, file_content, standards['best_practices']
                )
                violations.extend(practice_violations)
                total_checks += len(standards['best_practices'])
                passed_checks += len(standards['best_practices']) - len(practice_violations)
            
            # Check specific language standards
            if file_type == 'typescript' and 'type_annotations' in standards:
                type_violations = self._check_type_annotations(
                    file_analysis, file_content, standards['type_annotations']
                )
                violations.extend(type_violations)
            
            if file_type == 'python' and 'pep8_compliance' in standards:
                pep8_violations = self._check_pep8_compliance(
                    file_analysis, file_content, standards['pep8_compliance']
                )
                violations.extend(pep8_violations)
        
        # Calculate compliance percentage
        if total_checks > 0:
            analysis_summary['compliance_percentage'] = (passed_checks / total_checks) * 100
        
        # Group violations by type
        for violation in violations:
            vtype = violation.violation_type
            if vtype not in analysis_summary['violations_by_type']:
                analysis_summary['violations_by_type'][vtype] = 0
            analysis_summary['violations_by_type'][vtype] += 1
        
        # Calculate coding standards score
        coding_standards_score = analysis_summary['compliance_percentage']
        
        return {
            'violations': violations,
            'summary': analysis_summary,
            'coding_standards_score': coding_standards_score
        }
    
    def _analyze_documentation_consistency(self, context_analysis) -> Dict[str, Any]:
        """Analyze documentation consistency"""
        violations = []
        analysis_summary = {
            'documentation_files': 0,
            'missing_documentation': [],
            'documentation_quality': {}
        }
        
        # Check for documentation files
        doc_files = [f for f in context_analysis.file_analyses if f.file_type in ['markdown', 'documentation']]
        analysis_summary['documentation_files'] = len(doc_files)
        
        # Check for missing documentation
        code_files = [f for f in context_analysis.file_analyses if f.file_type in ['javascript', 'typescript', 'python']]
        
        for file_analysis in code_files:
            file_content = self._get_file_content(file_analysis.filename, context_analysis)
            
            # Check for missing function documentation
            if file_analysis.file_type == 'python':
                doc_violations = self._check_python_documentation(file_analysis, file_content)
                violations.extend(doc_violations)
            
            # Check for missing TypeScript documentation
            if file_analysis.file_type in ['typescript', 'typescript_react']:
                ts_doc_violations = self._check_typescript_documentation(file_analysis, file_content)
                violations.extend(ts_doc_violations)
        
        # Check README consistency
        readme_violations = self._check_readme_consistency(context_analysis)
        violations.extend(readme_violations)
        
        # Calculate documentation score
        total_expected_docs = len(code_files) * 2  # Rough estimate
        documentation_score = max(0, 100 - (len(violations) / max(total_expected_docs, 1)) * 100)
        
        return {
            'violations': violations,
            'summary': analysis_summary,
            'documentation_consistency_score': documentation_score
        }
    
    def _calculate_consistency_metrics(self, violations: List[ConsistencyViolation], 
                                     dependency_analysis: Dict[str, Any],
                                     architecture_analysis: Dict[str, Any],
                                     coding_standards_analysis: Dict[str, Any],
                                     documentation_analysis: Dict[str, Any]) -> ConsistencyMetrics:
        """Calculate comprehensive consistency metrics"""
        
        # Extract individual scores
        dep_score = dependency_analysis.get('dependency_consistency_score', 100)
        arch_score = architecture_analysis.get('architecture_consistency_score', 100)
        coding_score = coding_standards_analysis.get('coding_standards_score', 100)
        doc_score = documentation_analysis.get('documentation_consistency_score', 100)
        
        # Calculate weighted overall score
        weights = {
            'dependency': 0.25,
            'architecture': 0.25,
            'coding_standards': 0.25,
            'documentation': 0.25
        }
        
        overall_score = (
            dep_score * weights['dependency'] +
            arch_score * weights['architecture'] +
            coding_score * weights['coding_standards'] +
            doc_score * weights['documentation']
        )
        
        # Count violations by severity
        violations_by_severity = {
            'critical': len([v for v in violations if v.severity == 'critical']),
            'high': len([v for v in violations if v.severity == 'high']),
            'medium': len([v for v in violations if v.severity == 'medium']),
            'low': len([v for v in violations if v.severity == 'low'])
        }
        
        # Calculate compliance percentage
        total_checks = len(violations) + 100  # Assume 100 passed checks
        compliance_percentage = (100 / total_checks) * 100 if total_checks > 0 else 100
        
        return ConsistencyMetrics(
            overall_consistency_score=overall_score,
            dependency_consistency_score=dep_score,
            architecture_consistency_score=arch_score,
            coding_standards_score=coding_score,
            documentation_consistency_score=doc_score,
            total_violations=len(violations),
            violations_by_severity=violations_by_severity,
            compliance_percentage=compliance_percentage
        )
    
    def _generate_consistency_recommendations(self, violations: List[ConsistencyViolation],
                                            dependency_analysis: Dict[str, Any],
                                            architecture_analysis: Dict[str, Any],
                                            coding_standards_analysis: Dict[str, Any],
                                            documentation_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate actionable consistency recommendations"""
        recommendations = []
        
        # Group violations by category
        violations_by_category = {}
        for violation in violations:
            if violation.category not in violations_by_category:
                violations_by_category[violation.category] = []
            violations_by_category[violation.category].append(violation)
        
        # Generate category-specific recommendations
        for category, category_violations in violations_by_category.items():
            if category == 'dependency':
                recommendations.append({
                    'type': 'consistency_improvement',
                    'priority': 'medium',
                    'category': 'dependency_consistency',
                    'message': f'Standardize import statements and dependency patterns ({len(category_violations)} inconsistencies)',
                    'action': 'review_and_standardize_imports',
                    'affected_files': list(set(v.file_path for v in category_violations))
                })
            
            elif category == 'architecture':
                recommendations.append({
                    'type': 'architecture_improvement',
                    'priority': 'high',
                    'category': 'architecture_consistency',
                    'message': f'Align with established architectural patterns ({len(category_violations)} violations)',
                    'action': 'refactor_to_match_architecture',
                    'affected_files': list(set(v.file_path for v in category_violations))
                })
            
            elif category == 'coding_standards':
                recommendations.append({
                    'type': 'coding_standards_improvement',
                    'priority': 'low',
                    'category': 'code_quality',
                    'message': f'Apply consistent coding standards ({len(category_violations)} violations)',
                    'action': 'apply_code_formatting_and_standards',
                    'affected_files': list(set(v.file_path for v in category_violations))
                })
            
            elif category == 'documentation':
                recommendations.append({
                    'type': 'documentation_improvement',
                    'priority': 'medium',
                    'category': 'documentation_consistency',
                    'message': f'Add missing documentation and improve consistency ({len(category_violations)} issues)',
                    'action': 'add_missing_documentation',
                    'affected_files': list(set(v.file_path for v in category_violations))
                })
        
        # Add general recommendations based on scores
        if dependency_analysis.get('dependency_consistency_score', 100) < 80:
            recommendations.append({
                'type': 'process_improvement',
                'priority': 'medium',
                'category': 'development_process',
                'message': 'Consider implementing automated import organization and dependency management',
                'action': 'setup_automated_import_organization'
            })
        
        if coding_standards_analysis.get('coding_standards_score', 100) < 70:
            recommendations.append({
                'type': 'tooling_improvement',
                'priority': 'high',
                'category': 'development_tooling',
                'message': 'Setup automated code formatting and linting to maintain consistency',
                'action': 'configure_automated_code_formatting'
            })
        
        return recommendations
    
    # Helper methods for specific consistency checks
    
    def _get_existing_project_dependencies(self, technologies_detected) -> Dict[str, Any]:
        """Get existing project dependencies from knowledge vault"""
        try:
            existing_deps = {}
            for tech in technologies_detected:
                deps = self.knowledge_vault.get_dependencies_by_technology(tech.name)
                existing_deps[tech.name] = deps
            return existing_deps
        except Exception as e:
            self.logger.warning(f"Failed to get existing dependencies: {str(e)}")
            return {}
    
    def _analyze_import_statements(self, file_analysis, file_type: str) -> Dict[str, Any]:
        """Analyze import statement patterns in a file"""
        import_styles = {}
        
        for import_stmt in file_analysis.import_statements:
            # Determine import style
            if 'import' in import_stmt and 'from' in import_stmt:
                style = 'es6_named_import'
            elif import_stmt.startswith('import'):
                style = 'es6_default_import'
            elif 'require(' in import_stmt:
                style = 'commonjs_require'
            elif import_stmt.startswith('from') and 'import' in import_stmt:
                style = 'python_from_import'
            else:
                style = 'unknown'
            
            if style not in import_styles:
                import_styles[style] = 0
            import_styles[style] += 1
        
        return {
            'styles': import_styles,
            'total_imports': len(file_analysis.import_statements)
        }
    
    def _check_dependency_violations(self, file_analysis, existing_deps: Dict[str, Any]) -> List[ConsistencyViolation]:
        """Check for dependency-related consistency violations"""
        violations = []
        
        # This would implement specific dependency consistency checks
        # For now, return empty list as placeholder
        
        return violations
    
    def _check_import_organization(self, file_analysis, file_type: str) -> List[ConsistencyViolation]:
        """Check import organization consistency"""
        violations = []
        
        # This would implement import organization checks
        # For now, return empty list as placeholder
        
        return violations
    
    def _identify_primary_technologies(self, detected_technologies) -> List[str]:
        """Identify primary technologies in the project"""
        # Sort by confidence and return top technologies
        sorted_techs = sorted(detected_technologies, key=lambda x: x.confidence, reverse=True)
        return [tech.name for tech in sorted_techs[:5]]
    
    def _check_react_patterns(self, file_analysis, file_content: str) -> List[ConsistencyViolation]:
        """Check React-specific patterns"""
        violations = []
        
        # Check for functional vs class components
        has_class_components = bool(re.search(r'class\s+\w+\s+extends\s+React\.Component', file_content))
        has_functional_components = bool(re.search(r'const\s+\w+\s*=\s*\([^)]*\)\s*=>', file_content))
        
        if has_class_components and has_functional_components:
            violations.append(ConsistencyViolation(
                violation_id=self._generate_violation_id(file_analysis.filename, 'mixed_component_types'),
                violation_type='mixed_component_types',
                severity='medium',
                category='architecture',
                file_path=file_analysis.filename,
                line_number=None,
                description='Mix of functional and class components detected',
                expected_pattern='Consistent component pattern (prefer functional components)',
                actual_pattern='Mixed functional and class components',
                recommendation='Convert class components to functional components with hooks',
                confidence=0.8,
                impact_scope='file'
            ))
        
        return violations
    
    def _check_python_architecture(self, file_analysis, file_content: str) -> List[ConsistencyViolation]:
        """Check Python-specific architectural patterns"""
        violations = []
        
        # This would implement Python architecture checks
        # For now, return empty list as placeholder
        
        return violations
    
    def _check_module_structure(self, file_analysis, primary_technologies: List[str]) -> List[ConsistencyViolation]:
        """Check module structure consistency"""
        violations = []
        
        # This would implement module structure checks
        # For now, return empty list as placeholder
        
        return violations
    
    def _get_language_from_file_type(self, file_type: str) -> str:
        """Map file type to programming language"""
        mapping = {
            'javascript': 'javascript',
            'typescript': 'typescript',
            'typescript_react': 'typescript',
            'react_component': 'javascript',
            'python': 'python'
        }
        return mapping.get(file_type, 'unknown')
    
    def _check_formatting_standards(self, file_analysis, file_content: str, formatting_standards: Dict[str, Any]) -> List[ConsistencyViolation]:
        """Check formatting standards"""
        violations = []
        
        # This would implement formatting checks
        # For now, return empty list as placeholder
        
        return violations
    
    def _check_best_practices(self, file_analysis, file_content: str, best_practices: Dict[str, Any]) -> List[ConsistencyViolation]:
        """Check best practices compliance"""
        violations = []
        
        # This would implement best practices checks
        # For now, return empty list as placeholder
        
        return violations
    
    def _check_type_annotations(self, file_analysis, file_content: str, type_standards: Dict[str, Any]) -> List[ConsistencyViolation]:
        """Check TypeScript type annotation consistency"""
        violations = []
        
        # This would implement TypeScript-specific checks
        # For now, return empty list as placeholder
        
        return violations
    
    def _check_pep8_compliance(self, file_analysis, file_content: str, pep8_standards: Dict[str, Any]) -> List[ConsistencyViolation]:
        """Check PEP 8 compliance"""
        violations = []
        
        # This would implement PEP 8 checks
        # For now, return empty list as placeholder
        
        return violations
    
    def _check_python_documentation(self, file_analysis, file_content: str) -> List[ConsistencyViolation]:
        """Check Python documentation consistency"""
        violations = []
        
        # This would implement Python documentation checks
        # For now, return empty list as placeholder
        
        return violations
    
    def _check_typescript_documentation(self, file_analysis, file_content: str) -> List[ConsistencyViolation]:
        """Check TypeScript documentation consistency"""
        violations = []
        
        # This would implement TypeScript documentation checks
        # For now, return empty list as placeholder
        
        return violations
    
    def _check_readme_consistency(self, context_analysis) -> List[ConsistencyViolation]:
        """Check README file consistency"""
        violations = []
        
        # This would implement README consistency checks
        # For now, return empty list as placeholder
        
        return violations
    
    def _get_file_content(self, filename: str, context_analysis) -> str:
        """Get file content for analysis (placeholder implementation)"""
        # In a real implementation, this would get the actual file content
        return f"// Content of {filename}\n// Consistency analysis placeholder"
    
    def _generate_violation_id(self, file_path: str, violation_type: str) -> str:
        """Generate unique violation ID"""
        import hashlib
        data = f"{file_path}:{violation_type}:{datetime.now().isoformat()}"
        return hashlib.md5(data.encode()).hexdigest()[:12]
    
    def validate_configuration(self) -> Dict[str, Any]:
        """Validate validator configuration"""
        return {
            'status': 'healthy',
            'consistency_patterns_loaded': len(self.consistency_patterns),
            'coding_standards_loaded': len(self.coding_standards),
            'architecture_patterns_loaded': len(self.architecture_patterns),
            'knowledge_vault_available': self.knowledge_vault is not None
        }