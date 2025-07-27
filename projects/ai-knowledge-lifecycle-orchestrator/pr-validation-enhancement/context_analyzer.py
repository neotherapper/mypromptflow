#!/usr/bin/env python3
"""
PR Context Analyzer
AI Knowledge Lifecycle Orchestrator - PR Validation Enhancement

Analyzes PR content to identify technology usage, detect file types, extract
dependencies, and provide context for validation. Integrates with Knowledge Vault
to understand current technology landscape and dependency patterns.
"""

import os
import re
import json
import logging
from typing import Dict, List, Any, Optional, Set, Tuple
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class TechnologyDetection:
    """Technology detection result"""
    name: str
    category: str
    confidence: float
    version_detected: Optional[str]
    detection_method: str
    file_references: List[str]
    usage_context: List[str]


@dataclass
class FileAnalysis:
    """Individual file analysis result"""
    filename: str
    file_type: str
    file_extension: str
    technologies_detected: List[TechnologyDetection]
    import_statements: List[str]
    dependency_references: List[str]
    complexity_indicators: Dict[str, Any]
    security_patterns: List[str]


@dataclass
class PRContextAnalysis:
    """Complete PR context analysis result"""
    pr_id: str
    total_files_changed: int
    file_analyses: List[FileAnalysis]
    detected_technologies: List[TechnologyDetection]
    dependency_changes: List[Dict[str, Any]]
    architecture_impact: Dict[str, Any]
    risk_assessment: Dict[str, Any]
    knowledge_vault_matches: Dict[str, Any]
    analysis_timestamp: str


class PRContextAnalyzer:
    """Analyzes PR context and detects technologies, dependencies, and patterns"""
    
    def __init__(self, knowledge_vault, config: Dict[str, Any]):
        """Initialize the PR context analyzer"""
        self.knowledge_vault = knowledge_vault
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Load technology detection patterns
        self.detection_patterns = self._load_detection_patterns()
        self.file_type_mappings = self._load_file_type_mappings()
        
        self.logger.info("PR Context Analyzer initialized")
    
    def _load_detection_patterns(self) -> Dict[str, Any]:
        """Load technology detection patterns"""
        return {
            'import_patterns': {
                'react': [
                    r'import.*from ["\']react["\']',
                    r'import React',
                    r'from ["\']react["\']'
                ],
                'typescript': [
                    r'import.*\.ts["\']',
                    r'export.*interface',
                    r'type\s+\w+\s*=',
                    r':\s*\w+\[\]',
                    r'as\s+\w+Type'
                ],
                'next.js': [
                    r'import.*from ["\']next/',
                    r'export.*getServerSideProps',
                    r'export.*getStaticProps',
                    r'from ["\']next/router["\']'
                ],
                'express': [
                    r'import.*from ["\']express["\']',
                    r'require\(["\']express["\']',
                    r'app\.get\(',
                    r'app\.post\('
                ],
                'python': [
                    r'import\s+\w+',
                    r'from\s+\w+\s+import',
                    r'def\s+\w+\(',
                    r'class\s+\w+:'
                ]
            },
            'configuration_patterns': {
                'webpack': [
                    r'module\.exports\s*=',
                    r'webpack\.config',
                    r'entry:',
                    r'module:\s*{'
                ],
                'babel': [
                    r'@babel/',
                    r'"presets":\s*\[',
                    r'"plugins":\s*\['
                ],
                'eslint': [
                    r'"rules":\s*{',
                    r'"extends":\s*\[',
                    r'eslint-disable'
                ]
            },
            'dependency_patterns': {
                'package.json': [
                    r'"dependencies":\s*{',
                    r'"devDependencies":\s*{',
                    r'"scripts":\s*{'
                ],
                'requirements.txt': [
                    r'==\d+\.\d+',
                    r'>=\d+\.\d+',
                    r'^[\w-]+==[\d\.]+'
                ],
                'pip': [
                    r'pip install',
                    r'pip freeze',
                    r'requirements\.txt'
                ]
            }
        }
    
    def _load_file_type_mappings(self) -> Dict[str, str]:
        """Load file extension to type mappings"""
        return {
            '.js': 'javascript',
            '.jsx': 'react_component',
            '.ts': 'typescript',
            '.tsx': 'typescript_react',
            '.py': 'python',
            '.md': 'markdown',
            '.json': 'json_config',
            '.yaml': 'yaml_config',
            '.yml': 'yaml_config',
            '.xml': 'xml_config',
            '.css': 'stylesheet',
            '.scss': 'sass_stylesheet',
            '.html': 'html_template',
            '.sql': 'sql_script',
            '.sh': 'shell_script',
            '.dockerfile': 'docker',
            '.gitignore': 'git_config',
            '.env': 'environment_config'
        }
    
    def analyze_pr_context(self, pr_request) -> PRContextAnalysis:
        """
        Analyze complete PR context including technologies, dependencies, and patterns
        
        Args:
            pr_request: PRValidationRequest object
            
        Returns:
            PRContextAnalysis: Complete context analysis
        """
        self.logger.info(f"Starting PR context analysis for PR #{pr_request.pr_id}")
        
        # Analyze individual files
        file_analyses = []
        for file_info in pr_request.changed_files:
            file_analysis = self._analyze_file(file_info, pr_request.diff_content)
            file_analyses.append(file_analysis)
        
        # Aggregate technology detections
        detected_technologies = self._aggregate_technology_detections(file_analyses)
        
        # Analyze dependency changes
        dependency_changes = self._analyze_dependency_changes(file_analyses, pr_request)
        
        # Assess architecture impact
        architecture_impact = self._assess_architecture_impact(file_analyses, detected_technologies)
        
        # Perform risk assessment
        risk_assessment = self._perform_risk_assessment(file_analyses, detected_technologies)
        
        # Match against knowledge vault
        knowledge_vault_matches = self._match_against_knowledge_vault(detected_technologies)
        
        analysis = PRContextAnalysis(
            pr_id=pr_request.pr_id,
            total_files_changed=len(pr_request.changed_files),
            file_analyses=file_analyses,
            detected_technologies=detected_technologies,
            dependency_changes=dependency_changes,
            architecture_impact=architecture_impact,
            risk_assessment=risk_assessment,
            knowledge_vault_matches=knowledge_vault_matches,
            analysis_timestamp=datetime.now().isoformat()
        )
        
        self.logger.info(
            f"PR context analysis completed for PR #{pr_request.pr_id}: "
            f"{len(detected_technologies)} technologies detected, "
            f"{len(dependency_changes)} dependency changes"
        )
        
        return analysis
    
    def _analyze_file(self, file_info: Dict[str, Any], diff_content: str) -> FileAnalysis:
        """Analyze individual file for technologies and patterns"""
        filename = file_info['filename']
        file_path = Path(filename)
        file_extension = file_path.suffix.lower()
        
        # Determine file type
        file_type = self.file_type_mappings.get(file_extension, 'unknown')
        
        # Extract file content from diff (simplified)
        file_content = self._extract_file_content_from_diff(filename, diff_content)
        
        # Detect technologies
        technologies = self._detect_technologies_in_file(file_content, filename)
        
        # Extract import statements
        imports = self._extract_import_statements(file_content, file_type)
        
        # Extract dependency references
        dependencies = self._extract_dependency_references(file_content, file_type)
        
        # Analyze complexity
        complexity = self._analyze_file_complexity(file_content, file_type)
        
        # Detect security patterns
        security_patterns = self._detect_security_patterns(file_content, file_type)
        
        return FileAnalysis(
            filename=filename,
            file_type=file_type,
            file_extension=file_extension,
            technologies_detected=technologies,
            import_statements=imports,
            dependency_references=dependencies,
            complexity_indicators=complexity,
            security_patterns=security_patterns
        )
    
    def _extract_file_content_from_diff(self, filename: str, diff_content: str) -> str:
        """Extract file content from diff (simplified implementation)"""
        # In a real implementation, this would parse the actual diff
        # For now, return a placeholder that can be used for pattern matching
        return f"# Extracted content for {filename}\n{diff_content[:1000]}"
    
    def _detect_technologies_in_file(self, content: str, filename: str) -> List[TechnologyDetection]:
        """Detect technologies used in file content"""
        detections = []
        
        for tech_name, patterns in self.detection_patterns['import_patterns'].items():
            confidence = 0.0
            matching_patterns = []
            
            for pattern in patterns:
                matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
                if matches:
                    confidence += 0.25  # Each matching pattern adds confidence
                    matching_patterns.extend(matches)
            
            if confidence > 0:
                # Cap confidence at 1.0
                confidence = min(confidence, 1.0)
                
                detection = TechnologyDetection(
                    name=tech_name,
                    category=self._get_technology_category(tech_name),
                    confidence=confidence,
                    version_detected=self._extract_version(content, tech_name),
                    detection_method='import_pattern',
                    file_references=[filename],
                    usage_context=matching_patterns[:5]  # Limit context items
                )
                detections.append(detection)
        
        # Also check configuration patterns
        for tech_name, patterns in self.detection_patterns['configuration_patterns'].items():
            confidence = 0.0
            matching_patterns = []
            
            for pattern in patterns:
                matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
                if matches:
                    confidence += 0.3
                    matching_patterns.extend(matches)
            
            if confidence > 0:
                confidence = min(confidence, 1.0)
                
                detection = TechnologyDetection(
                    name=tech_name,
                    category='build_tool',
                    confidence=confidence,
                    version_detected=None,
                    detection_method='configuration_pattern',
                    file_references=[filename],
                    usage_context=matching_patterns[:5]
                )
                detections.append(detection)
        
        return detections
    
    def _get_technology_category(self, tech_name: str) -> str:
        """Get technology category for a given technology name"""
        category_mapping = {
            'react': 'frontend_framework',
            'typescript': 'programming_language',
            'next.js': 'frontend_framework',
            'express': 'backend_framework',
            'python': 'programming_language',
            'webpack': 'build_tool',
            'babel': 'build_tool',
            'eslint': 'dev_tool'
        }
        return category_mapping.get(tech_name.lower(), 'other')
    
    def _extract_version(self, content: str, tech_name: str) -> Optional[str]:
        """Extract version information for a technology"""
        # Look for version patterns
        version_patterns = [
            rf'{tech_name}["\']:\s*["\']([0-9]+\.[0-9]+\.?[0-9]*)["\']',
            rf'@{tech_name}/[^"\']*["\']:\s*["\']([0-9]+\.[0-9]+\.?[0-9]*)["\']',
            rf'{tech_name}@([0-9]+\.[0-9]+\.?[0-9]*)'
        ]
        
        for pattern in version_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def _extract_import_statements(self, content: str, file_type: str) -> List[str]:
        """Extract import statements from file content"""
        imports = []
        
        if file_type in ['javascript', 'typescript', 'react_component', 'typescript_react']:
            # JavaScript/TypeScript imports
            js_import_patterns = [
                r'import\s+.*from\s+["\'][^"\']+["\']',
                r'import\s+["\'][^"\']+["\']',
                r'require\(["\'][^"\']+["\']\)'
            ]
            
            for pattern in js_import_patterns:
                matches = re.findall(pattern, content, re.MULTILINE)
                imports.extend(matches)
        
        elif file_type == 'python':
            # Python imports
            py_import_patterns = [
                r'import\s+[\w\.]+',
                r'from\s+[\w\.]+\s+import\s+.*'
            ]
            
            for pattern in py_import_patterns:
                matches = re.findall(pattern, content, re.MULTILINE)
                imports.extend(matches)
        
        return imports[:20]  # Limit to first 20 imports
    
    def _extract_dependency_references(self, content: str, file_type: str) -> List[str]:
        """Extract dependency references from file content"""
        dependencies = []
        
        # Look for package.json dependencies
        if 'package.json' in content or file_type == 'json_config':
            dep_pattern = r'"([^"]+)":\s*"([^"]+)"'
            matches = re.findall(dep_pattern, content)
            dependencies.extend([f"{name}@{version}" for name, version in matches])
        
        # Look for Python requirements
        elif 'requirements.txt' in content or file_type == 'python':
            req_pattern = r'([a-zA-Z0-9_-]+)==([0-9\.]+)'
            matches = re.findall(req_pattern, content)
            dependencies.extend([f"{name}=={version}" for name, version in matches])
        
        return dependencies[:15]  # Limit dependencies
    
    def _analyze_file_complexity(self, content: str, file_type: str) -> Dict[str, Any]:
        """Analyze file complexity indicators"""
        complexity = {
            'line_count': len(content.splitlines()),
            'character_count': len(content),
            'function_count': 0,
            'class_count': 0,
            'import_count': 0,
            'complexity_score': 0
        }
        
        if file_type in ['javascript', 'typescript', 'react_component', 'typescript_react']:
            # Count functions
            function_patterns = [r'function\s+\w+', r'const\s+\w+\s*=\s*\(.*\)\s*=>', r'\w+\s*:\s*\(.*\)\s*=>']
            for pattern in function_patterns:
                complexity['function_count'] += len(re.findall(pattern, content))
            
            # Count classes
            complexity['class_count'] = len(re.findall(r'class\s+\w+', content))
            
        elif file_type == 'python':
            # Count Python functions and classes
            complexity['function_count'] = len(re.findall(r'def\s+\w+', content))
            complexity['class_count'] = len(re.findall(r'class\s+\w+', content))
        
        # Count imports
        complexity['import_count'] = len(re.findall(r'import\s+', content))
        
        # Calculate complexity score (0-100)
        base_score = min(complexity['line_count'] / 10, 50)  # Lines contribute up to 50
        function_score = min(complexity['function_count'] * 5, 30)  # Functions up to 30
        class_score = min(complexity['class_count'] * 10, 20)  # Classes up to 20
        
        complexity['complexity_score'] = int(base_score + function_score + class_score)
        
        return complexity
    
    def _detect_security_patterns(self, content: str, file_type: str) -> List[str]:
        """Detect potential security patterns in file content"""
        security_patterns = []
        
        # Common security anti-patterns
        security_checks = {
            'hardcoded_secrets': [
                r'password\s*=\s*["\'][^"\']+["\']',
                r'api_key\s*=\s*["\'][^"\']+["\']',
                r'secret\s*=\s*["\'][^"\']+["\']'
            ],
            'sql_injection': [
                r'SELECT\s.*\+.*',
                r'INSERT\s.*\+.*',
                r'UPDATE\s.*\+.*'
            ],
            'xss_vulnerability': [
                r'innerHTML\s*=\s*.*\+',
                r'document\.write\s*\(',
                r'eval\s*\('
            ],
            'insecure_random': [
                r'Math\.random\(\)',
                r'random\.random\(\)'
            ]
        }
        
        for pattern_type, patterns in security_checks.items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    security_patterns.append(pattern_type)
                    break  # Only add each pattern type once
        
        return security_patterns
    
    def _aggregate_technology_detections(self, file_analyses: List[FileAnalysis]) -> List[TechnologyDetection]:
        """Aggregate technology detections across all files"""
        tech_aggregations = {}
        
        for file_analysis in file_analyses:
            for tech in file_analysis.technologies_detected:
                if tech.name in tech_aggregations:
                    # Merge existing detection
                    existing = tech_aggregations[tech.name]
                    existing.confidence = max(existing.confidence, tech.confidence)
                    existing.file_references.extend(tech.file_references)
                    existing.usage_context.extend(tech.usage_context)
                else:
                    tech_aggregations[tech.name] = tech
        
        # Convert back to list and sort by confidence
        aggregated_techs = list(tech_aggregations.values())
        aggregated_techs.sort(key=lambda x: x.confidence, reverse=True)
        
        return aggregated_techs
    
    def _analyze_dependency_changes(self, file_analyses: List[FileAnalysis], pr_request) -> List[Dict[str, Any]]:
        """Analyze dependency changes in the PR"""
        dependency_changes = []
        
        # Look for package.json or requirements.txt changes
        for file_analysis in file_analyses:
            if 'package.json' in file_analysis.filename:
                changes = {
                    'file': file_analysis.filename,
                    'type': 'npm_dependencies',
                    'dependencies_found': len(file_analysis.dependency_references),
                    'change_type': 'modified',  # Would be determined from git diff
                    'impact_assessment': 'medium'
                }
                dependency_changes.append(changes)
            
            elif 'requirements.txt' in file_analysis.filename or file_analysis.filename.endswith('.txt'):
                changes = {
                    'file': file_analysis.filename,
                    'type': 'python_dependencies',
                    'dependencies_found': len(file_analysis.dependency_references),
                    'change_type': 'modified',
                    'impact_assessment': 'medium'
                }
                dependency_changes.append(changes)
        
        return dependency_changes
    
    def _assess_architecture_impact(self, file_analyses: List[FileAnalysis], technologies: List[TechnologyDetection]) -> Dict[str, Any]:
        """Assess architectural impact of the changes"""
        impact = {
            'impact_level': 'low',
            'affected_layers': [],
            'technology_additions': [],
            'architectural_concerns': []
        }
        
        # Determine impact level based on file types and technologies
        frontend_files = sum(1 for f in file_analyses if f.file_type in ['react_component', 'typescript_react'])
        backend_files = sum(1 for f in file_analyses if f.file_type == 'python')
        config_files = sum(1 for f in file_analyses if 'config' in f.file_type)
        
        if frontend_files > 5 or backend_files > 5:
            impact['impact_level'] = 'high'
        elif frontend_files > 2 or backend_files > 2 or config_files > 1:
            impact['impact_level'] = 'medium'
        
        # Identify affected layers
        if frontend_files > 0:
            impact['affected_layers'].append('frontend')
        if backend_files > 0:
            impact['affected_layers'].append('backend')
        if config_files > 0:
            impact['affected_layers'].append('configuration')
        
        # Identify new technologies
        for tech in technologies:
            if tech.confidence > 0.7:  # High confidence detections
                impact['technology_additions'].append({
                    'name': tech.name,
                    'category': tech.category,
                    'confidence': tech.confidence
                })
        
        return impact
    
    def _perform_risk_assessment(self, file_analyses: List[FileAnalysis], technologies: List[TechnologyDetection]) -> Dict[str, Any]:
        """Perform risk assessment for the PR changes"""
        risk = {
            'overall_risk': 'low',
            'security_risk': 'low',
            'compatibility_risk': 'low',
            'performance_risk': 'low',
            'risk_factors': []
        }
        
        # Assess security risk
        security_issues = sum(len(f.security_patterns) for f in file_analyses)
        if security_issues > 3:
            risk['security_risk'] = 'high'
            risk['risk_factors'].append(f"Multiple security patterns detected ({security_issues})")
        elif security_issues > 0:
            risk['security_risk'] = 'medium'
            risk['risk_factors'].append(f"Security patterns detected ({security_issues})")
        
        # Assess complexity risk
        high_complexity_files = sum(1 for f in file_analyses if f.complexity_indicators['complexity_score'] > 70)
        if high_complexity_files > 2:
            risk['performance_risk'] = 'high'
            risk['risk_factors'].append(f"High complexity files ({high_complexity_files})")
        
        # Assess technology risk
        new_technologies = sum(1 for t in technologies if t.confidence > 0.8)
        if new_technologies > 3:
            risk['compatibility_risk'] = 'medium'
            risk['risk_factors'].append(f"Multiple new technologies ({new_technologies})")
        
        # Calculate overall risk
        risk_scores = {
            'low': 1,
            'medium': 2,
            'high': 3
        }
        
        total_risk = (
            risk_scores[risk['security_risk']] +
            risk_scores[risk['compatibility_risk']] +
            risk_scores[risk['performance_risk']]
        ) / 3
        
        if total_risk >= 2.5:
            risk['overall_risk'] = 'high'
        elif total_risk >= 1.5:
            risk['overall_risk'] = 'medium'
        
        return risk
    
    def _match_against_knowledge_vault(self, technologies: List[TechnologyDetection]) -> Dict[str, Any]:
        """Match detected technologies against knowledge vault data"""
        matches = {
            'total_technologies_tracked': 0,
            'tracked_technologies': [],
            'untracked_technologies': [],
            'dependency_matches': [],
            'version_information': {}
        }
        
        try:
            for tech in technologies:
                # Query knowledge vault for this technology
                vault_entries = self.knowledge_vault.query_technologies({'technology_name': tech.name})
                
                if vault_entries:
                    matches['total_technologies_tracked'] += 1
                    matches['tracked_technologies'].append({
                        'name': tech.name,
                        'current_version': vault_entries[0].get('current_version'),
                        'monitoring_priority': vault_entries[0].get('monitoring_priority'),
                        'detected_confidence': tech.confidence
                    })
                    
                    # Store version information
                    matches['version_information'][tech.name] = {
                        'current_version': vault_entries[0].get('current_version'),
                        'detected_version': tech.version_detected,
                        'version_match': tech.version_detected == vault_entries[0].get('current_version') if tech.version_detected else None
                    }
                else:
                    matches['untracked_technologies'].append({
                        'name': tech.name,
                        'category': tech.category,
                        'confidence': tech.confidence
                    })
                
                # Check for dependency matches
                dependencies = self.knowledge_vault.get_dependencies_by_technology(tech.name)
                if dependencies:
                    matches['dependency_matches'].append({
                        'technology': tech.name,
                        'dependency_count': len(dependencies),
                        'critical_dependencies': len([d for d in dependencies if d.get('dependency_criticality') == 'essential'])
                    })
        
        except Exception as e:
            self.logger.error(f"Error matching against knowledge vault: {str(e)}")
            matches['error'] = str(e)
        
        return matches
    
    def validate_configuration(self) -> Dict[str, Any]:
        """Validate analyzer configuration"""
        return {
            'status': 'healthy',
            'detection_patterns_loaded': len(self.detection_patterns),
            'file_type_mappings_loaded': len(self.file_type_mappings),
            'knowledge_vault_available': self.knowledge_vault is not None
        }