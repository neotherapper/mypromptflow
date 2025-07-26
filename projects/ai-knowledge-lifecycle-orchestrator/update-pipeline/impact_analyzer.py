#!/usr/bin/env python3
"""
Impact Analyzer
AI Knowledge Lifecycle Orchestrator - Sophisticated impact analysis system

This module provides comprehensive impact analysis to determine which AI files need updates
when technologies change, including dependency traversal and cascade analysis.
"""

import asyncio
import logging
import time
import re
from datetime import datetime
from typing import Dict, List, Optional, Any, Set, Tuple
from enum import Enum
from dataclasses import dataclass, asdict
from pathlib import Path
import json
import hashlib

from ..change_detection.change_detector import TechnologyChange, ChangeType, ImpactLevel, UrgencyLevel
from ..knowledge_vault_integration import KnowledgeVaultIntegration

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DependencyType(Enum):
    """Types of dependencies between files"""
    DIRECT_REFERENCE = "direct_reference"
    TRANSITIVE_DEPENDENCY = "transitive_dependency"
    PATTERN_USAGE = "pattern_usage"
    VERSION_CONSTRAINT = "version_constraint"
    CONFIGURATION_DEPENDENCY = "configuration_dependency"


class UpdatePriority(Enum):
    """Update priority levels"""
    IMMEDIATE = "immediate"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    DEFERRED = "deferred"


@dataclass
class AffectedFile:
    """Represents a file affected by a technology change"""
    file_path: str
    file_type: str
    dependency_type: DependencyType
    impact_severity: ImpactLevel
    update_priority: UpdatePriority
    confidence_score: float
    affected_sections: List[str]
    suggested_changes: List[str]
    dependencies: List[str]  # Files this depends on
    dependents: List[str]   # Files that depend on this
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['dependency_type'] = self.dependency_type.value
        data['impact_severity'] = self.impact_severity.value
        data['update_priority'] = self.update_priority.value
        return data


@dataclass
class ImpactAssessment:
    """Comprehensive impact assessment results"""
    assessment_id: str
    technology_name: str
    change: TechnologyChange
    affected_files_count: int
    affected_files: List[AffectedFile]
    dependency_graph: Dict[str, List[str]]
    cascade_analysis: Dict[str, Any]
    update_recommendations: List[str]
    risk_assessment: Dict[str, Any]
    estimated_effort: Dict[str, Any]
    quality_impact: Dict[str, Any]
    impact_level: ImpactLevel
    urgency_level: UrgencyLevel
    confidence_score: float
    analysis_timestamp: datetime
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['affected_files'] = [af.to_dict() for af in self.affected_files]
        data['impact_level'] = self.impact_level.value
        data['urgency_level'] = self.urgency_level.value
        data['analysis_timestamp'] = self.analysis_timestamp.isoformat()
        return data


class ImpactAnalyzer:
    """
    Sophisticated impact analysis system that determines which AI files need updates
    when technologies change, including dependency traversal and cascade analysis
    """
    
    def __init__(self, knowledge_vault: KnowledgeVaultIntegration, config: Dict[str, Any]):
        """Initialize the impact analyzer"""
        self.knowledge_vault = knowledge_vault
        self.config = config
        
        # Analysis configuration
        self.analysis_depth = config.get('analysis_depth', 'comprehensive')
        self.dependency_traversal_depth = config.get('dependency_traversal_depth', 3)
        self.confidence_threshold = config.get('confidence_threshold', 0.7)
        self.parallel_analysis = config.get('parallel_analysis', True)
        
        # File type analysis patterns
        self.file_patterns = self._initialize_file_patterns()
        
        # Technology-specific impact rules
        self.impact_rules = self._initialize_impact_rules()
        
        # Performance tracking
        self.metrics = {
            'total_analyses': 0,
            'average_analysis_time': 0.0,
            'average_files_analyzed': 0.0,
            'cache_hit_rate': 0.0,
            'confidence_distribution': {}
        }
        
        # Analysis cache
        self.analysis_cache: Dict[str, ImpactAssessment] = {}
        self.cache_expiry_hours = config.get('cache_expiry_hours', 24)
        
        logger.info("Impact Analyzer initialized successfully")
    
    def _initialize_file_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Initialize file analysis patterns"""
        return {
            'claude_md': {
                'extensions': ['.md'],
                'name_patterns': [r'CLAUDE\.md$', r'claude\.md$'],
                'content_patterns': {
                    'technology_references': [
                        r'(?i)\b(react|typescript|next\.?js|node\.?js|jest|docker)\b',
                        r'version\s*[:\-]\s*["\']?([0-9]+\.[0-9]+\.[0-9]+)',
                        r'@([a-zA-Z0-9\-_]+/[a-zA-Z0-9\-_]+)',
                        r'npm\s+install\s+([a-zA-Z0-9\-_@/]+)'
                    ],
                    'version_constraints': [
                        r'>=?\s*([0-9]+\.[0-9]+\.[0-9]+)',
                        r'\^([0-9]+\.[0-9]+\.[0-9]+)',
                        r'~([0-9]+\.[0-9]+\.[0-9]+)'
                    ]
                },
                'update_patterns': [
                    'installation_commands',
                    'version_references',
                    'configuration_examples',
                    'best_practices'
                ]
            },
            
            'command_file': {
                'extensions': ['.md'],
                'name_patterns': [r'\.claude/commands/.*\.md$'],
                'content_patterns': {
                    'technology_references': [
                        r'(?i)\b(npm|yarn|pnpm)\s+(install|add|run)',
                        r'(?i)\b(docker|kubectl|helm)\s+',
                        r'(?i)package\.json|tsconfig\.json|webpack\.config'
                    ],
                    'script_patterns': [
                        r'```(?:bash|sh)\s*\n(.*?)\n```',
                        r'`([^`]+)`'
                    ]
                },
                'update_patterns': [
                    'command_syntax',
                    'package_names',
                    'cli_options',
                    'configuration_paths'
                ]
            },
            
            'tool_documentation': {
                'extensions': ['.md', '.yaml', '.json'],
                'content_patterns': {
                    'technology_references': [
                        r'(?i)\b(github|gitlab|bitbucket)\b',
                        r'(?i)\b(aws|azure|gcp|heroku)\b',
                        r'(?i)\b(mongodb|postgresql|redis|elasticsearch)\b'
                    ],
                    'api_patterns': [
                        r'https?://[^\s\)]+',
                        r'api\.[^\s/]+',
                        r'v[0-9]+\.[0-9]+'
                    ]
                },
                'update_patterns': [
                    'api_endpoints',
                    'service_versions',
                    'authentication_methods',
                    'feature_availability'
                ]
            },
            
            'configuration': {
                'extensions': ['.json', '.yaml', '.yml', '.toml'],
                'content_patterns': {
                    'dependency_patterns': [
                        r'"([^"]+)":\s*"([^"]+)"',
                        r'version:\s*["\']?([^"\'\s]+)',
                        r'image:\s*([^\s]+)'
                    ]
                },
                'update_patterns': [
                    'dependency_versions',
                    'image_tags',
                    'configuration_values'
                ]
            }
        }
    
    def _initialize_impact_rules(self) -> Dict[str, Dict[str, Any]]:
        """Initialize technology-specific impact rules"""
        return {
            'React': {
                'high_impact_changes': ['breaking_change', 'deprecation_warning'],
                'affected_patterns': [
                    r'(?i)react\s+hooks?',
                    r'(?i)jsx?|tsx?',
                    r'(?i)component|render',
                    r'useEffect|useState|useContext'
                ],
                'version_sensitivity': 'high',
                'cascade_potential': 'high'
            },
            
            'TypeScript': {
                'high_impact_changes': ['breaking_change', 'feature_addition'],
                'affected_patterns': [
                    r'(?i)typescript|tsc',
                    r'\.tsx?$',
                    r'tsconfig\.json',
                    r'type\s+|interface\s+'
                ],
                'version_sensitivity': 'high',
                'cascade_potential': 'medium'
            },
            
            'Next.js': {
                'high_impact_changes': ['breaking_change', 'configuration_change'],
                'affected_patterns': [
                    r'(?i)next\.js|nextjs',
                    r'next\.config\.',
                    r'pages/|app/',
                    r'getServerSideProps|getStaticProps'
                ],
                'version_sensitivity': 'critical',
                'cascade_potential': 'high'
            },
            
            'Node.js': {
                'high_impact_changes': ['breaking_change', 'security_update'],
                'affected_patterns': [
                    r'(?i)node\.js|nodejs',
                    r'package\.json',
                    r'npm|yarn|pnpm',
                    r'require\(|import\s+'
                ],
                'version_sensitivity': 'medium',
                'cascade_potential': 'critical'
            },
            
            'Jest': {
                'high_impact_changes': ['breaking_change', 'configuration_change'],
                'affected_patterns': [
                    r'(?i)jest',
                    r'\.test\.js|\.spec\.js',
                    r'jest\.config\.',
                    r'describe\(|it\(|test\('
                ],
                'version_sensitivity': 'medium',
                'cascade_potential': 'low'
            },
            
            'Docker': {
                'high_impact_changes': ['breaking_change', 'security_update'],
                'affected_patterns': [
                    r'(?i)docker|dockerfile',
                    r'FROM\s+',
                    r'docker-compose',
                    r'container|image'
                ],
                'version_sensitivity': 'high',
                'cascade_potential': 'medium'
            }
        }
    
    async def analyze_change_impact(self, change: TechnologyChange) -> ImpactAssessment:
        """
        Perform comprehensive impact analysis for a technology change
        
        Args:
            change: The technology change to analyze
            
        Returns:
            Comprehensive impact assessment
        """
        start_time = time.time()
        assessment_id = self._generate_assessment_id(change)
        
        try:
            logger.info(f"Starting impact analysis for {change.technology_name}")
            
            # Check cache first
            cached_assessment = self._check_cache(assessment_id, change)
            if cached_assessment:
                logger.info(f"Using cached impact assessment for {change.technology_name}")
                return cached_assessment
            
            # Get all dependencies for this technology
            dependencies = await self._get_technology_dependencies(change.technology_name)
            
            # Analyze affected files
            affected_files = await self._analyze_affected_files(change, dependencies)
            
            # Build dependency graph
            dependency_graph = await self._build_dependency_graph(affected_files)
            
            # Perform cascade analysis
            cascade_analysis = await self._perform_cascade_analysis(change, affected_files, dependency_graph)
            
            # Generate recommendations
            update_recommendations = await self._generate_update_recommendations(change, affected_files)
            
            # Assess risks
            risk_assessment = await self._assess_risks(change, affected_files, cascade_analysis)
            
            # Estimate effort
            estimated_effort = await self._estimate_effort(affected_files, cascade_analysis)
            
            # Assess quality impact
            quality_impact = await self._assess_quality_impact(change, affected_files)
            
            # Calculate overall impact level and urgency
            overall_impact = self._calculate_overall_impact(change, affected_files, cascade_analysis)
            overall_urgency = self._calculate_overall_urgency(change, risk_assessment)
            
            # Calculate confidence score
            confidence_score = self._calculate_confidence_score(change, affected_files, dependencies)
            
            # Create impact assessment
            assessment = ImpactAssessment(
                assessment_id=assessment_id,
                technology_name=change.technology_name,
                change=change,
                affected_files_count=len(affected_files),
                affected_files=affected_files,
                dependency_graph=dependency_graph,
                cascade_analysis=cascade_analysis,
                update_recommendations=update_recommendations,
                risk_assessment=risk_assessment,
                estimated_effort=estimated_effort,
                quality_impact=quality_impact,
                impact_level=overall_impact,
                urgency_level=overall_urgency,
                confidence_score=confidence_score,
                analysis_timestamp=datetime.utcnow()
            )
            
            # Cache the assessment
            self._cache_assessment(assessment_id, assessment)
            
            # Update metrics
            analysis_time = time.time() - start_time
            self._update_metrics(assessment, analysis_time)
            
            logger.info(f"Impact analysis completed: {len(affected_files)} files affected ({analysis_time:.2f}s)")
            return assessment
            
        except Exception as e:
            logger.error(f"Error during impact analysis: {e}")
            # Return minimal assessment on error
            return ImpactAssessment(
                assessment_id=assessment_id,
                technology_name=change.technology_name,
                change=change,
                affected_files_count=0,
                affected_files=[],
                dependency_graph={},
                cascade_analysis={'error': str(e)},
                update_recommendations=[],
                risk_assessment={'error': str(e)},
                estimated_effort={'error': str(e)},
                quality_impact={'error': str(e)},
                impact_level=ImpactLevel.MEDIUM,
                urgency_level=UrgencyLevel.MEDIUM,
                confidence_score=0.0,
                analysis_timestamp=datetime.utcnow()
            )
    
    def _generate_assessment_id(self, change: TechnologyChange) -> str:
        """Generate unique assessment ID"""
        content = f"{change.technology_name}_{change.change_type.value}_{change.detection_timestamp.isoformat()}"
        return hashlib.md5(content.encode()).hexdigest()
    
    def _check_cache(self, assessment_id: str, change: TechnologyChange) -> Optional[ImpactAssessment]:
        """Check if cached assessment exists and is valid"""
        if assessment_id not in self.analysis_cache:
            return None
        
        cached = self.analysis_cache[assessment_id]
        
        # Check if cache is still valid
        hours_since_analysis = (datetime.utcnow() - cached.analysis_timestamp).total_seconds() / 3600
        if hours_since_analysis > self.cache_expiry_hours:
            del self.analysis_cache[assessment_id]
            return None
        
        return cached
    
    def _cache_assessment(self, assessment_id: str, assessment: ImpactAssessment):
        """Cache assessment for future use"""
        self.analysis_cache[assessment_id] = assessment
        
        # Limit cache size
        if len(self.analysis_cache) > 100:
            # Remove oldest entries
            sorted_cache = sorted(
                self.analysis_cache.items(),
                key=lambda x: x[1].analysis_timestamp
            )
            for old_id, _ in sorted_cache[:20]:
                del self.analysis_cache[old_id]
    
    async def _get_technology_dependencies(self, technology_name: str) -> List[Dict[str, Any]]:
        """Get all dependencies for a technology from Knowledge Vault"""
        try:
            dependencies = await asyncio.to_thread(
                self.knowledge_vault.get_dependencies_by_technology,
                technology_name
            )
            return dependencies
        except Exception as e:
            logger.error(f"Error getting dependencies for {technology_name}: {e}")
            return []
    
    async def _analyze_affected_files(self, change: TechnologyChange, dependencies: List[Dict[str, Any]]) -> List[AffectedFile]:
        """Analyze which files are affected by the change"""
        affected_files = []
        
        try:
            # Analyze known dependencies first
            for dep in dependencies:
                affected_file = await self._analyze_dependency_impact(change, dep)
                if affected_file:
                    affected_files.append(affected_file)
            
            # Perform broader file system analysis if configured
            if self.analysis_depth == 'comprehensive':
                additional_files = await self._scan_filesystem_for_impacts(change)
                affected_files.extend(additional_files)
            
            # Remove duplicates
            seen_paths = set()
            unique_files = []
            for af in affected_files:
                if af.file_path not in seen_paths:
                    seen_paths.add(af.file_path)
                    unique_files.append(af)
            
            return unique_files
            
        except Exception as e:
            logger.error(f"Error analyzing affected files: {e}")
            return []
    
    async def _analyze_dependency_impact(self, change: TechnologyChange, dependency: Dict[str, Any]) -> Optional[AffectedFile]:
        """Analyze impact on a specific dependency"""
        try:
            file_path = dependency.get('ai_file_path', '')
            file_type = dependency.get('ai_file_type', 'unknown')
            
            if not file_path:
                return None
            
            # Determine dependency type
            dep_type = DependencyType.DIRECT_REFERENCE
            if dependency.get('dependency_type') == 'transitive':
                dep_type = DependencyType.TRANSITIVE_DEPENDENCY
            
            # Calculate impact severity based on change type and dependency criticality
            impact_severity = self._calculate_file_impact_severity(change, dependency)
            
            # Determine update priority
            update_priority = self._determine_update_priority(change, dependency, impact_severity)
            
            # Analyze file content for affected sections
            affected_sections = await self._analyze_file_content(file_path, change.technology_name)
            
            # Generate suggested changes
            suggested_changes = await self._generate_file_suggestions(file_path, change, affected_sections)
            
            # Calculate confidence score
            confidence_score = self._calculate_file_confidence(change, dependency, affected_sections)
            
            return AffectedFile(
                file_path=file_path,
                file_type=file_type,
                dependency_type=dep_type,
                impact_severity=impact_severity,
                update_priority=update_priority,
                confidence_score=confidence_score,
                affected_sections=affected_sections,
                suggested_changes=suggested_changes,
                dependencies=[],  # Will be populated by dependency graph
                dependents=[]     # Will be populated by dependency graph
            )
            
        except Exception as e:
            logger.error(f"Error analyzing dependency impact: {e}")
            return None
    
    async def _scan_filesystem_for_impacts(self, change: TechnologyChange) -> List[AffectedFile]:
        """Scan filesystem for additional files that might be impacted"""
        additional_files = []
        
        try:
            # Get technology-specific patterns
            tech_rules = self.impact_rules.get(change.technology_name, {})
            patterns = tech_rules.get('affected_patterns', [])
            
            if not patterns:
                return additional_files
            
            # In a real implementation, this would scan the filesystem
            # For now, we'll simulate finding additional files
            base_path = Path("/Users/georgiospilitsoglou/Developer/projects/mypromptflow")
            
            # Simulate finding files (limited for performance)
            simulated_files = [
                "projects/example/CLAUDE.md",
                "ai/commands/example.md",
                "docs/architecture.md"
            ]
            
            for file_path in simulated_files:
                full_path = base_path / file_path
                if full_path.exists():
                    # Analyze content for technology references
                    has_references = await self._file_contains_technology_references(
                        str(full_path), change.technology_name, patterns
                    )
                    
                    if has_references:
                        affected_file = AffectedFile(
                            file_path=str(full_path),
                            file_type=self._determine_file_type(str(full_path)),
                            dependency_type=DependencyType.PATTERN_USAGE,
                            impact_severity=ImpactLevel.LOW,
                            update_priority=UpdatePriority.LOW,
                            confidence_score=0.6,
                            affected_sections=[],
                            suggested_changes=[],
                            dependencies=[],
                            dependents=[]
                        )
                        additional_files.append(affected_file)
            
            return additional_files
            
        except Exception as e:
            logger.error(f"Error scanning filesystem: {e}")
            return []
    
    async def _file_contains_technology_references(self, file_path: str, technology: str, patterns: List[str]) -> bool:
        """Check if file contains references to the technology"""
        try:
            path = Path(file_path)
            if not path.exists():
                return False
            
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Check for technology name
            if technology.lower() in content.lower():
                return True
            
            # Check patterns
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    return True
            
            return False
            
        except Exception as e:
            logger.error(f"Error checking file content: {e}")
            return False
    
    def _determine_file_type(self, file_path: str) -> str:
        """Determine file type based on path and extension"""
        path = Path(file_path)
        
        if 'CLAUDE.md' in path.name:
            return 'claude_md'
        elif '.claude/commands' in str(path):
            return 'command_file'
        elif path.suffix in ['.md']:
            return 'documentation'
        elif path.suffix in ['.json', '.yaml', '.yml']:
            return 'configuration'
        else:
            return 'unknown'
    
    async def _analyze_file_content(self, file_path: str, technology: str) -> List[str]:
        """Analyze file content to identify affected sections"""
        try:
            path = Path(file_path)
            if not path.exists():
                return []
            
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            affected_sections = []
            lines = content.split('\n')
            
            for i, line in enumerate(lines):
                if technology.lower() in line.lower():
                    # Get context around the match
                    start = max(0, i - 2)
                    end = min(len(lines), i + 3)
                    context = '\n'.join(lines[start:end])
                    affected_sections.append(f"Line {i+1}: {context}")
            
            return affected_sections[:10]  # Limit to first 10 matches
            
        except Exception as e:
            logger.error(f"Error analyzing file content: {e}")
            return []
    
    async def _generate_file_suggestions(self, file_path: str, change: TechnologyChange, affected_sections: List[str]) -> List[str]:
        """Generate suggested changes for a file"""
        suggestions = []
        
        try:
            # Generate suggestions based on change type
            if change.change_type == ChangeType.BREAKING_CHANGE:
                suggestions.append("Review and update deprecated API usage")
                suggestions.append("Test compatibility with new version")
                
            elif change.change_type == ChangeType.SECURITY_UPDATE:
                suggestions.append("Update to secure version immediately")
                suggestions.append("Review security implications")
                
            elif change.change_type == ChangeType.FEATURE_ADDITION:
                suggestions.append("Consider adopting new features")
                suggestions.append("Update documentation with new capabilities")
                
            elif change.change_type == ChangeType.BUG_FIX:
                suggestions.append("Update to bug-fixed version")
                suggestions.append("Remove any workarounds")
            
            # Add version-specific suggestions
            if change.old_version and change.new_version:
                suggestions.append(f"Update version references from {change.old_version} to {change.new_version}")
            
            return suggestions
            
        except Exception as e:
            logger.error(f"Error generating suggestions: {e}")
            return []
    
    def _calculate_file_impact_severity(self, change: TechnologyChange, dependency: Dict[str, Any]) -> ImpactLevel:
        """Calculate impact severity for a specific file"""
        base_severity = change.impact_level
        
        # Adjust based on dependency criticality
        criticality = dependency.get('dependency_criticality', 'moderate')
        if criticality == 'essential':
            # Boost severity
            if base_severity == ImpactLevel.LOW:
                return ImpactLevel.MEDIUM
            elif base_severity == ImpactLevel.MEDIUM:
                return ImpactLevel.HIGH
        elif criticality == 'optional':
            # Reduce severity
            if base_severity == ImpactLevel.HIGH:
                return ImpactLevel.MEDIUM
            elif base_severity == ImpactLevel.MEDIUM:
                return ImpactLevel.LOW
        
        return base_severity
    
    def _determine_update_priority(self, change: TechnologyChange, dependency: Dict[str, Any], impact_severity: ImpactLevel) -> UpdatePriority:
        """Determine update priority for a file"""
        # Start with change urgency
        if change.urgency_level == UrgencyLevel.IMMEDIATE:
            return UpdatePriority.IMMEDIATE
        elif change.urgency_level == UrgencyLevel.URGENT:
            return UpdatePriority.HIGH
        
        # Consider impact severity
        if impact_severity == ImpactLevel.CRITICAL:
            return UpdatePriority.IMMEDIATE
        elif impact_severity == ImpactLevel.HIGH:
            return UpdatePriority.HIGH
        elif impact_severity == ImpactLevel.MEDIUM:
            return UpdatePriority.MEDIUM
        else:
            return UpdatePriority.LOW
    
    def _calculate_file_confidence(self, change: TechnologyChange, dependency: Dict[str, Any], affected_sections: List[str]) -> float:
        """Calculate confidence score for file impact assessment"""
        confidence = change.confidence_score
        
        # Boost confidence if we found specific sections
        if affected_sections:
            confidence += 0.1 * min(len(affected_sections), 5)
        
        # Adjust based on dependency validation status
        validation_status = dependency.get('validation_status', 'unknown')
        if validation_status == 'validated':
            confidence += 0.1
        elif validation_status == 'unvalidated':
            confidence -= 0.1
        
        return min(confidence, 1.0)
    
    async def _build_dependency_graph(self, affected_files: List[AffectedFile]) -> Dict[str, List[str]]:
        """Build dependency graph between affected files"""
        graph = {}
        
        try:
            # Initialize graph
            for af in affected_files:
                graph[af.file_path] = []
            
            # In a real implementation, this would analyze cross-references and imports
            # For now, we'll create a simple graph based on file types and patterns
            
            claude_files = [af for af in affected_files if af.file_type == 'claude_md']
            command_files = [af for af in affected_files if af.file_type == 'command_file']
            
            # Claude files typically depend on command files
            for claude_file in claude_files:
                for command_file in command_files:
                    if self._files_likely_related(claude_file.file_path, command_file.file_path):
                        graph[claude_file.file_path].append(command_file.file_path)
                        command_file.dependents.append(claude_file.file_path)
                        claude_file.dependencies.append(command_file.file_path)
            
            return graph
            
        except Exception as e:
            logger.error(f"Error building dependency graph: {e}")
            return {}
    
    def _files_likely_related(self, file1: str, file2: str) -> bool:
        """Determine if two files are likely related"""
        # Simple heuristic based on path similarity
        path1 = Path(file1)
        path2 = Path(file2)
        
        # Same directory
        if path1.parent == path2.parent:
            return True
        
        # Related project directories
        if any(part in str(path1) and part in str(path2) for part in ['ai', 'claude', 'commands']):
            return True
        
        return False
    
    async def _perform_cascade_analysis(self, change: TechnologyChange, affected_files: List[AffectedFile], dependency_graph: Dict[str, List[str]]) -> Dict[str, Any]:
        """Perform cascade analysis to understand ripple effects"""
        try:
            cascade_analysis = {
                'total_cascade_depth': 0,
                'cascade_paths': [],
                'high_risk_cascades': [],
                'cascade_statistics': {
                    'max_depth': 0,
                    'total_paths': 0,
                    'affected_clusters': 0
                }
            }
            
            # Analyze cascade paths
            for file_path in dependency_graph:
                paths = self._find_cascade_paths(file_path, dependency_graph, max_depth=self.dependency_traversal_depth)
                cascade_analysis['cascade_paths'].extend(paths)
                
                # Track max depth
                for path in paths:
                    cascade_analysis['cascade_statistics']['max_depth'] = max(
                        cascade_analysis['cascade_statistics']['max_depth'],
                        len(path)
                    )
            
            # Identify high-risk cascades
            for path in cascade_analysis['cascade_paths']:
                if len(path) > 3:  # Deep cascades are risky
                    cascade_analysis['high_risk_cascades'].append(path)
            
            # Calculate statistics
            cascade_analysis['cascade_statistics']['total_paths'] = len(cascade_analysis['cascade_paths'])
            cascade_analysis['cascade_statistics']['affected_clusters'] = len(
                set(path[0] for path in cascade_analysis['cascade_paths'] if path)
            )
            
            return cascade_analysis
            
        except Exception as e:
            logger.error(f"Error performing cascade analysis: {e}")
            return {'error': str(e)}
    
    def _find_cascade_paths(self, start_file: str, graph: Dict[str, List[str]], max_depth: int, current_path: List[str] = None) -> List[List[str]]:
        """Find all cascade paths from a starting file"""
        if current_path is None:
            current_path = [start_file]
        
        if len(current_path) >= max_depth:
            return [current_path]
        
        paths = []
        dependencies = graph.get(start_file, [])
        
        if not dependencies:
            return [current_path]
        
        for dep in dependencies:
            if dep not in current_path:  # Avoid cycles
                new_path = current_path + [dep]
                sub_paths = self._find_cascade_paths(dep, graph, max_depth, new_path)
                paths.extend(sub_paths)
        
        return paths
    
    async def _generate_update_recommendations(self, change: TechnologyChange, affected_files: List[AffectedFile]) -> List[str]:
        """Generate update recommendations"""
        recommendations = []
        
        try:
            # Priority-based recommendations
            immediate_files = [af for af in affected_files if af.update_priority == UpdatePriority.IMMEDIATE]
            high_priority_files = [af for af in affected_files if af.update_priority == UpdatePriority.HIGH]
            
            if immediate_files:
                recommendations.append(f"IMMEDIATE: Update {len(immediate_files)} critical files first")
                
            if high_priority_files:
                recommendations.append(f"HIGH PRIORITY: Update {len(high_priority_files)} high-priority files within 24 hours")
            
            # Change-type specific recommendations
            if change.change_type == ChangeType.BREAKING_CHANGE:
                recommendations.append("Test all affected functionality thoroughly after updates")
                recommendations.append("Consider creating backup branches before applying changes")
                
            elif change.change_type == ChangeType.SECURITY_UPDATE:
                recommendations.append("Apply security updates immediately across all affected files")
                recommendations.append("Review security implications and audit logs")
            
            # Batch processing recommendations
            if len(affected_files) > 10:
                recommendations.append("Consider batch processing updates in groups of 5-10 files")
                recommendations.append("Implement staged rollout with validation at each stage")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return []
    
    async def _assess_risks(self, change: TechnologyChange, affected_files: List[AffectedFile], cascade_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Assess risks associated with the change"""
        try:
            risk_assessment = {
                'overall_risk_level': 'medium',
                'risk_factors': [],
                'mitigation_strategies': [],
                'risk_score': 0.5
            }
            
            risk_score = 0.0
            risk_factors = []
            
            # Change type risks
            if change.change_type == ChangeType.BREAKING_CHANGE:
                risk_score += 0.3
                risk_factors.append("Breaking changes may cause compatibility issues")
                
            elif change.change_type == ChangeType.SECURITY_UPDATE:
                risk_score += 0.2
                risk_factors.append("Security updates require immediate attention")
            
            # Scale risks
            if len(affected_files) > 50:
                risk_score += 0.2
                risk_factors.append("Large number of affected files increases coordination complexity")
            
            # Cascade risks
            high_risk_cascades = cascade_analysis.get('high_risk_cascades', [])
            if high_risk_cascades:
                risk_score += 0.15
                risk_factors.append(f"Deep dependency cascades detected ({len(high_risk_cascades)} high-risk paths)")
            
            # Confidence risks
            low_confidence_files = [af for af in affected_files if af.confidence_score < 0.6]
            if low_confidence_files:
                risk_score += 0.1
                risk_factors.append(f"Low confidence in impact assessment for {len(low_confidence_files)} files")
            
            # Determine overall risk level
            if risk_score > 0.7:
                risk_level = 'high'
            elif risk_score > 0.4:
                risk_level = 'medium'
            else:
                risk_level = 'low'
            
            # Generate mitigation strategies
            mitigation_strategies = []
            if 'breaking' in ' '.join(risk_factors).lower():
                mitigation_strategies.append("Create comprehensive test suite before applying changes")
                mitigation_strategies.append("Implement gradual rollout with rollback capabilities")
            
            if len(affected_files) > 20:
                mitigation_strategies.append("Use automated validation tools to verify changes")
                mitigation_strategies.append("Implement parallel processing for large batch updates")
            
            risk_assessment.update({
                'overall_risk_level': risk_level,
                'risk_factors': risk_factors,
                'mitigation_strategies': mitigation_strategies,
                'risk_score': min(risk_score, 1.0)
            })
            
            return risk_assessment
            
        except Exception as e:
            logger.error(f"Error assessing risks: {e}")
            return {'error': str(e)}
    
    async def _estimate_effort(self, affected_files: List[AffectedFile], cascade_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate effort required for updates"""
        try:
            effort_estimation = {
                'total_estimated_hours': 0.0,
                'breakdown_by_priority': {},
                'breakdown_by_file_type': {},
                'complexity_factors': []
            }
            
            total_hours = 0.0
            priority_breakdown = {}
            file_type_breakdown = {}
            
            # Base effort per file by type and priority
            effort_matrix = {
                'claude_md': {'immediate': 2.0, 'high': 1.5, 'medium': 1.0, 'low': 0.5},
                'command_file': {'immediate': 1.5, 'high': 1.0, 'medium': 0.8, 'low': 0.3},
                'documentation': {'immediate': 1.0, 'high': 0.8, 'medium': 0.5, 'low': 0.2},
                'configuration': {'immediate': 0.5, 'high': 0.3, 'medium': 0.2, 'low': 0.1}
            }
            
            for af in affected_files:
                file_type = af.file_type
                priority = af.update_priority.value
                
                base_effort = effort_matrix.get(file_type, {}).get(priority, 1.0)
                
                # Adjust for confidence (lower confidence = more effort)
                confidence_multiplier = 2.0 - af.confidence_score
                file_effort = base_effort * confidence_multiplier
                
                total_hours += file_effort
                
                # Track breakdowns
                if priority not in priority_breakdown:
                    priority_breakdown[priority] = 0.0
                priority_breakdown[priority] += file_effort
                
                if file_type not in file_type_breakdown:
                    file_type_breakdown[file_type] = 0.0
                file_type_breakdown[file_type] += file_effort
            
            # Add complexity factors
            complexity_factors = []
            
            # Cascade complexity
            cascade_paths = cascade_analysis.get('cascade_paths', [])
            if len(cascade_paths) > 10:
                cascade_multiplier = 1.2
                total_hours *= cascade_multiplier
                complexity_factors.append(f"Complex dependency cascades (+20% effort)")
            
            # Large batch complexity
            if len(affected_files) > 30:
                batch_multiplier = 1.15
                total_hours *= batch_multiplier
                complexity_factors.append(f"Large batch processing (+15% effort)")
            
            effort_estimation.update({
                'total_estimated_hours': round(total_hours, 1),
                'breakdown_by_priority': priority_breakdown,
                'breakdown_by_file_type': file_type_breakdown,
                'complexity_factors': complexity_factors
            })
            
            return effort_estimation
            
        except Exception as e:
            logger.error(f"Error estimating effort: {e}")
            return {'error': str(e)}
    
    async def _assess_quality_impact(self, change: TechnologyChange, affected_files: List[AffectedFile]) -> Dict[str, Any]:
        """Assess impact on overall system quality"""
        try:
            quality_impact = {
                'overall_quality_change': 'neutral',
                'quality_score_delta': 0.0,
                'positive_impacts': [],
                'negative_impacts': [],
                'quality_recommendations': []
            }
            
            score_delta = 0.0
            positive_impacts = []
            negative_impacts = []
            
            # Analyze change type impact on quality
            if change.change_type == ChangeType.SECURITY_UPDATE:
                score_delta += 0.1
                positive_impacts.append("Security improvements enhance overall system quality")
                
            elif change.change_type == ChangeType.BUG_FIX:
                score_delta += 0.05
                positive_impacts.append("Bug fixes improve system reliability")
                
            elif change.change_type == ChangeType.BREAKING_CHANGE:
                score_delta -= 0.1
                negative_impacts.append("Breaking changes may temporarily reduce system stability")
            
            # Analyze affected files impact
            critical_files = [af for af in affected_files if af.file_type == 'claude_md']
            if len(critical_files) > 10:
                score_delta -= 0.05
                negative_impacts.append("Many critical AI instruction files affected")
            
            # Generate quality recommendations
            recommendations = []
            if score_delta < 0:
                recommendations.append("Implement comprehensive testing before deployment")
                recommendations.append("Consider phased rollout to minimize quality impact")
                
            if len(affected_files) > 20:
                recommendations.append("Use automated quality validation tools")
                recommendations.append("Monitor quality metrics during update process")
            
            # Determine overall quality change
            if score_delta > 0.05:
                overall_change = 'positive'
            elif score_delta < -0.05:
                overall_change = 'negative'
            else:
                overall_change = 'neutral'
            
            quality_impact.update({
                'overall_quality_change': overall_change,
                'quality_score_delta': round(score_delta, 3),
                'positive_impacts': positive_impacts,
                'negative_impacts': negative_impacts,
                'quality_recommendations': recommendations
            })
            
            return quality_impact
            
        except Exception as e:
            logger.error(f"Error assessing quality impact: {e}")
            return {'error': str(e)}
    
    def _calculate_overall_impact(self, change: TechnologyChange, affected_files: List[AffectedFile], cascade_analysis: Dict[str, Any]) -> ImpactLevel:
        """Calculate overall impact level"""
        base_impact = change.impact_level
        
        # Adjust based on affected files count
        if len(affected_files) > 50:
            if base_impact == ImpactLevel.MEDIUM:
                return ImpactLevel.HIGH
            elif base_impact == ImpactLevel.HIGH:
                return ImpactLevel.CRITICAL
        
        # Adjust based on cascade complexity
        high_risk_cascades = cascade_analysis.get('high_risk_cascades', [])
        if len(high_risk_cascades) > 5:
            if base_impact == ImpactLevel.MEDIUM:
                return ImpactLevel.HIGH
        
        return base_impact
    
    def _calculate_overall_urgency(self, change: TechnologyChange, risk_assessment: Dict[str, Any]) -> UrgencyLevel:
        """Calculate overall urgency level"""
        base_urgency = change.urgency_level
        
        # Adjust based on risk level
        risk_level = risk_assessment.get('overall_risk_level', 'medium')
        if risk_level == 'high':
            if base_urgency == UrgencyLevel.MEDIUM:
                return UrgencyLevel.HIGH
            elif base_urgency == UrgencyLevel.HIGH:
                return UrgencyLevel.URGENT
        
        return base_urgency
    
    def _calculate_confidence_score(self, change: TechnologyChange, affected_files: List[AffectedFile], dependencies: List[Dict[str, Any]]) -> float:
        """Calculate overall confidence score for the assessment"""
        base_confidence = change.confidence_score
        
        # Adjust based on file analysis confidence
        if affected_files:
            file_confidences = [af.confidence_score for af in affected_files]
            avg_file_confidence = sum(file_confidences) / len(file_confidences)
            base_confidence = (base_confidence + avg_file_confidence) / 2
        
        # Adjust based on dependency data quality
        validated_deps = len([d for d in dependencies if d.get('validation_status') == 'validated'])
        if dependencies:
            dep_quality_factor = validated_deps / len(dependencies)
            base_confidence *= (0.5 + 0.5 * dep_quality_factor)
        
        return min(base_confidence, 1.0)
    
    def _update_metrics(self, assessment: ImpactAssessment, analysis_time: float):
        """Update performance metrics"""
        self.metrics['total_analyses'] += 1
        
        # Update average analysis time
        total_analyses = self.metrics['total_analyses']
        current_avg = self.metrics['average_analysis_time']
        self.metrics['average_analysis_time'] = (
            (current_avg * (total_analyses - 1) + analysis_time) / total_analyses
        )
        
        # Update average files analyzed
        files_count = assessment.affected_files_count
        current_files_avg = self.metrics['average_files_analyzed']
        self.metrics['average_files_analyzed'] = (
            (current_files_avg * (total_analyses - 1) + files_count) / total_analyses
        )
        
        # Update confidence distribution
        confidence_bucket = f"{int(assessment.confidence_score * 10) * 10}-{int(assessment.confidence_score * 10) * 10 + 9}%"
        if confidence_bucket not in self.metrics['confidence_distribution']:
            self.metrics['confidence_distribution'][confidence_bucket] = 0
        self.metrics['confidence_distribution'][confidence_bucket] += 1
    
    async def get_impact_metrics(self) -> Dict[str, Any]:
        """Get impact analyzer metrics"""
        return {
            'total_analyses': self.metrics['total_analyses'],
            'average_analysis_time': self.metrics['average_analysis_time'],
            'average_files_analyzed': self.metrics['average_files_analyzed'],
            'cache_hit_rate': self.metrics['cache_hit_rate'],
            'confidence_distribution': self.metrics['confidence_distribution'],
            'cache_size': len(self.analysis_cache),
            'timestamp': datetime.utcnow().isoformat()
        }


async def main():
    """Main function for testing"""
    try:
        # Initialize components
        knowledge_vault = KnowledgeVaultIntegration()
        config = {
            'analysis_depth': 'comprehensive',
            'dependency_traversal_depth': 3,
            'confidence_threshold': 0.7,
            'parallel_analysis': True
        }
        
        analyzer = ImpactAnalyzer(knowledge_vault, config)
        
        # Get metrics
        metrics = await analyzer.get_impact_metrics()
        print("Impact Analyzer Metrics:")
        print(json.dumps(metrics, indent=2))
        
        print("\nImpact Analyzer test completed successfully!")
        
    except Exception as e:
        print(f"Error testing impact analyzer: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(asyncio.run(main()))