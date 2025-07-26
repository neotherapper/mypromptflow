#!/usr/bin/env python3
"""
Change Detection Core Engine
AI Knowledge Lifecycle Orchestrator - Production-ready change detection engine

This module implements the core change detection engine that monitors technology
sources and detects meaningful changes requiring propagation to AI instruction files.
"""

import asyncio
import hashlib
import json
import logging
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Set
from enum import Enum
import re
import semver
from pathlib import Path

from .config_manager import ConfigManager
from .mcp_integrator import MCPIntegrator
from .storage_interface import StorageInterface

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChangeType(Enum):
    """Enumeration of change types"""
    BREAKING_CHANGE = "breaking_change"
    SECURITY_UPDATE = "security_update"
    DEPRECATION_WARNING = "deprecation_warning"
    FEATURE_ADDITION = "feature_addition"
    BUG_FIX = "bug_fix"
    CONFIGURATION_CHANGE = "configuration_change"


class ImpactLevel(Enum):
    """Enumeration of impact levels"""
    MINIMAL = "minimal"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class UrgencyLevel(Enum):
    """Enumeration of urgency levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"
    IMMEDIATE = "immediate"


@dataclass
class TechnologyChange:
    """Represents a detected technology change"""
    technology_name: str
    change_type: ChangeType
    old_version: Optional[str]
    new_version: Optional[str]
    source_url: str
    detection_timestamp: datetime
    impact_level: ImpactLevel
    urgency_level: UrgencyLevel
    confidence_score: float
    change_description: str
    evidence: List[str]
    affected_files: List[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['change_type'] = self.change_type.value
        data['impact_level'] = self.impact_level.value
        data['urgency_level'] = self.urgency_level.value
        data['detection_timestamp'] = self.detection_timestamp.isoformat()
        return data


@dataclass
class SourceData:
    """Represents data retrieved from a technology source"""
    url: str
    content: str
    content_hash: str
    retrieved_at: datetime
    source_type: str
    extraction_metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['retrieved_at'] = self.retrieved_at.isoformat()
        return data


class ChangeDetectionEngine:
    """
    Core change detection engine that monitors technology sources and detects
    meaningful changes requiring propagation to AI instruction files.
    """
    
    def __init__(self, config_manager: ConfigManager, mcp_integrator: MCPIntegrator, 
                 storage: StorageInterface):
        """Initialize the change detection engine"""
        self.config = config_manager
        self.mcp = mcp_integrator
        self.storage = storage
        
        # Load configuration
        self.tech_config = self.config.get_technology_config()
        self.classification_rules = self.config.get_classification_rules()
        
        # Initialize detection patterns
        self._compile_detection_patterns()
        
        # Performance tracking
        self.performance_stats = {
            'detections_processed': 0,
            'changes_detected': 0,
            'false_positives': 0,
            'average_processing_time': 0.0
        }
        
        logger.info("Change Detection Engine initialized successfully")
    
    def _compile_detection_patterns(self):
        """Compile regex patterns for efficient change detection"""
        self.patterns = {}
        
        # Version patterns
        self.patterns['semantic_version'] = re.compile(
            r'v?([0-9]+)\.([0-9]+)\.([0-9]+)(?:-([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?(?:\+([0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*))?'
        )
        
        # Change type patterns from classification rules
        change_rules = self.classification_rules['change_type_classification']
        
        for change_type, rules in change_rules.items():
            if 'detection_patterns' in rules:
                patterns = rules['detection_patterns']
                
                # Compile content keyword patterns
                if 'content_keywords' in patterns:
                    combined_keywords = []
                    for confidence_level, keywords in patterns['content_keywords'].items():
                        if isinstance(keywords, dict) and 'weight' in keywords:
                            # Skip weight entries
                            continue
                        if isinstance(keywords, list):
                            combined_keywords.extend(keywords)
                    
                    if combined_keywords:
                        pattern_str = r'\b(?:' + '|'.join(re.escape(kw) for kw in combined_keywords) + r')\b'
                        self.patterns[f'{change_type}_keywords'] = re.compile(pattern_str, re.IGNORECASE)
        
        logger.info(f"Compiled {len(self.patterns)} detection patterns")
    
    async def detect_changes_for_technology(self, technology_name: str) -> List[TechnologyChange]:
        """
        Detect changes for a specific technology by checking all its configured sources
        
        Args:
            technology_name: Name of the technology to check
            
        Returns:
            List of detected changes
        """
        start_time = time.time()
        changes = []
        
        try:
            # Get technology configuration
            tech_config = self._get_technology_config(technology_name)
            if not tech_config:
                logger.warning(f"No configuration found for technology: {technology_name}")
                return changes
            
            logger.info(f"Detecting changes for {technology_name}")
            
            # Check all sources for this technology
            for source_name, source_config in tech_config['official_sources'].items():
                try:
                    source_changes = await self._check_source_for_changes(
                        technology_name, source_name, source_config
                    )
                    changes.extend(source_changes)
                    
                except Exception as e:
                    logger.error(f"Error checking source {source_name} for {technology_name}: {e}")
                    continue
            
            # Update performance stats
            processing_time = time.time() - start_time
            self.performance_stats['detections_processed'] += 1
            self.performance_stats['changes_detected'] += len(changes)
            self.performance_stats['average_processing_time'] = (
                (self.performance_stats['average_processing_time'] * 
                 (self.performance_stats['detections_processed'] - 1) + processing_time) /
                self.performance_stats['detections_processed']
            )
            
            logger.info(f"Detected {len(changes)} changes for {technology_name} in {processing_time:.2f}s")
            return changes
            
        except Exception as e:
            logger.error(f"Error detecting changes for {technology_name}: {e}")
            return changes
    
    async def _check_source_for_changes(self, technology_name: str, source_name: str, 
                                      source_config: Dict[str, Any]) -> List[TechnologyChange]:
        """Check a specific source for changes"""
        changes = []
        
        try:
            # Retrieve current data from source
            source_data = await self._retrieve_source_data(source_config)
            if not source_data:
                return changes
            
            # Get previous data from storage
            previous_data = await self.storage.get_cached_source_data(
                technology_name, source_name
            )
            
            # Compare and detect changes
            if previous_data and previous_data.content_hash != source_data.content_hash:
                detected_changes = await self._analyze_content_changes(
                    technology_name, source_data, previous_data, source_config
                )
                changes.extend(detected_changes)
            
            # Store current data
            await self.storage.store_source_data(technology_name, source_name, source_data)
            
        except Exception as e:
            logger.error(f"Error checking source {source_name}: {e}")
        
        return changes
    
    async def _retrieve_source_data(self, source_config: Dict[str, Any]) -> Optional[SourceData]:
        """Retrieve data from a technology source using MCP servers"""
        try:
            url = source_config['url']
            source_type = source_config['type']
            mcp_server = source_config['mcp_server']
            extraction_pattern = source_config['extraction_pattern']
            
            # Retrieve content using MCP integrator
            content = await self.mcp.fetch_content(url, mcp_server, source_type)
            if not content:
                return None
            
            # Calculate content hash for change detection
            content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
            
            # Extract metadata based on pattern
            metadata = self._extract_metadata(content, extraction_pattern, source_type)
            
            return SourceData(
                url=url,
                content=content,
                content_hash=content_hash,
                retrieved_at=datetime.utcnow(),
                source_type=source_type,
                extraction_metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"Error retrieving source data: {e}")
            return None
    
    def _extract_metadata(self, content: str, extraction_pattern: str, 
                         source_type: str) -> Dict[str, Any]:
        """Extract metadata from source content based on extraction pattern"""
        metadata = {
            'content_length': len(content),
            'extraction_pattern': extraction_pattern,
            'extracted_versions': [],
            'extracted_dates': [],
            'change_indicators': []
        }
        
        try:
            # Extract version information
            version_matches = self.patterns['semantic_version'].findall(content)
            for match in version_matches:
                version = f"{match[0]}.{match[1]}.{match[2]}"
                if match[3]:  # Pre-release
                    version += f"-{match[3]}"
                if match[4]:  # Build metadata  
                    version += f"+{match[4]}"
                metadata['extracted_versions'].append(version)
            
            # Extract dates (various formats)
            date_patterns = [
                r'\b(\d{4}-\d{2}-\d{2})\b',  # YYYY-MM-DD
                r'\b(\d{1,2}/\d{1,2}/\d{4})\b',  # MM/DD/YYYY
                r'\b(\w+ \d{1,2}, \d{4})\b'  # Month DD, YYYY
            ]
            
            for pattern in date_patterns:
                matches = re.findall(pattern, content)
                metadata['extracted_dates'].extend(matches)
            
            # Extract change indicators based on source type
            if source_type == 'github_api':
                # Look for release-specific indicators
                if 'tag_name' in content:
                    metadata['has_releases'] = True
                if 'prerelease' in content:
                    metadata['has_prereleases'] = True
            elif source_type == 'official_blog':
                # Look for blog post indicators
                if any(keyword in content.lower() for keyword in ['release', 'announce', 'update']):
                    metadata['has_announcements'] = True
            
        except Exception as e:
            logger.error(f"Error extracting metadata: {e}")
        
        return metadata
    
    async def _analyze_content_changes(self, technology_name: str, current_data: SourceData,
                                     previous_data: SourceData, source_config: Dict[str, Any]) -> List[TechnologyChange]:
        """Analyze content changes and classify them"""
        changes = []
        
        try:
            # Get change indicators from source config
            change_indicators = source_config.get('change_indicators', [])
            
            # Analyze version changes
            current_versions = set(current_data.extraction_metadata.get('extracted_versions', []))
            previous_versions = set(previous_data.extraction_metadata.get('extracted_versions', []))
            
            new_versions = current_versions - previous_versions
            
            for version in new_versions:
                # Classify the change based on version and content
                change = await self._classify_version_change(
                    technology_name, version, current_data, previous_data, source_config
                )
                if change:
                    changes.append(change)
            
            # Analyze content changes even without version changes
            if not new_versions:
                content_change = await self._classify_content_change(
                    technology_name, current_data, previous_data, source_config
                )
                if content_change:
                    changes.append(content_change)
            
        except Exception as e:
            logger.error(f"Error analyzing content changes: {e}")
        
        return changes
    
    async def _classify_version_change(self, technology_name: str, version: str,
                                     current_data: SourceData, previous_data: SourceData,
                                     source_config: Dict[str, Any]) -> Optional[TechnologyChange]:
        """Classify a version change"""
        try:
            # Get current version for comparison
            tech_config = self._get_technology_config(technology_name)
            current_version = tech_config.get('current_version', '0.0.0')
            
            # Determine change type based on version comparison
            change_type = self._determine_version_change_type(current_version, version)
            
            # Calculate confidence score
            confidence = self._calculate_confidence_score(current_data, source_config)
            
            # Determine impact and urgency
            impact_level = self._calculate_impact_level(technology_name, change_type)
            urgency_level = self._calculate_urgency_level(change_type, impact_level)
            
            # Extract evidence from content
            evidence = self._extract_change_evidence(current_data.content, change_type)
            
            # Create change description
            description = f"{technology_name} version {version} detected"
            if change_type == ChangeType.BREAKING_CHANGE:
                description += " (Breaking Changes)"
            elif change_type == ChangeType.SECURITY_UPDATE:
                description += " (Security Update)"
            
            return TechnologyChange(
                technology_name=technology_name,
                change_type=change_type,
                old_version=current_version,
                new_version=version,
                source_url=current_data.url,
                detection_timestamp=current_data.retrieved_at,
                impact_level=impact_level,
                urgency_level=urgency_level,
                confidence_score=confidence,
                change_description=description,
                evidence=evidence
            )
            
        except Exception as e:
            logger.error(f"Error classifying version change: {e}")
            return None
    
    async def _classify_content_change(self, technology_name: str, current_data: SourceData,
                                     previous_data: SourceData, source_config: Dict[str, Any]) -> Optional[TechnologyChange]:
        """Classify content changes without version changes"""
        try:
            # Check for various change types using compiled patterns
            detected_change_type = None
            max_confidence = 0.0
            evidence = []
            
            for change_type in ChangeType:
                pattern_key = f'{change_type.value}_keywords'
                if pattern_key in self.patterns:
                    matches = self.patterns[pattern_key].findall(current_data.content)
                    if matches:
                        # Calculate confidence based on matches
                        match_confidence = min(len(matches) * 0.2, 1.0)
                        if match_confidence > max_confidence:
                            max_confidence = match_confidence
                            detected_change_type = change_type
                            evidence = matches
            
            if not detected_change_type or max_confidence < 0.3:
                return None
            
            # Calculate overall confidence
            confidence = self._calculate_confidence_score(current_data, source_config) * max_confidence
            
            # Determine impact and urgency
            impact_level = self._calculate_impact_level(technology_name, detected_change_type)
            urgency_level = self._calculate_urgency_level(detected_change_type, impact_level)
            
            # Create description based on detected change type
            description = f"{technology_name} content change detected: {detected_change_type.value.replace('_', ' ')}"
            
            return TechnologyChange(
                technology_name=technology_name,
                change_type=detected_change_type,
                old_version=None,
                new_version=None,
                source_url=current_data.url,
                detection_timestamp=current_data.retrieved_at,
                impact_level=impact_level,
                urgency_level=urgency_level,
                confidence_score=confidence,
                change_description=description,
                evidence=evidence
            )
            
        except Exception as e:
            logger.error(f"Error classifying content change: {e}")
            return None
    
    def _determine_version_change_type(self, old_version: str, new_version: str) -> ChangeType:
        """Determine change type based on version comparison"""
        try:
            # Clean version strings
            old_clean = self._clean_version(old_version)
            new_clean = self._clean_version(new_version)
            
            if old_clean == "0.0.0" or new_clean == "0.0.0":
                return ChangeType.FEATURE_ADDITION
            
            # Compare versions
            old_parts = [int(x) for x in old_clean.split('.')]
            new_parts = [int(x) for x in new_clean.split('.')]
            
            # Pad to same length
            while len(old_parts) < 3:
                old_parts.append(0)
            while len(new_parts) < 3:
                new_parts.append(0)
            
            # Major version change
            if new_parts[0] > old_parts[0]:
                return ChangeType.BREAKING_CHANGE
            
            # Minor version change  
            elif new_parts[1] > old_parts[1]:
                return ChangeType.FEATURE_ADDITION
            
            # Patch version change
            elif new_parts[2] > old_parts[2]:
                return ChangeType.BUG_FIX
            
            return ChangeType.FEATURE_ADDITION
            
        except Exception as e:
            logger.error(f"Error determining version change type: {e}")
            return ChangeType.FEATURE_ADDITION
    
    def _clean_version(self, version: str) -> str:
        """Clean version string for comparison"""
        if not version or version == "latest":
            return "0.0.0"
        
        # Remove 'v' prefix
        version = version.lstrip('v')
        
        # Extract just the version number part
        match = self.patterns['semantic_version'].match(version)
        if match:
            return f"{match.group(1)}.{match.group(2)}.{match.group(3)}"
        
        return "0.0.0"
    
    def _calculate_confidence_score(self, source_data: SourceData, source_config: Dict[str, Any]) -> float:
        """Calculate confidence score for change detection"""
        base_confidence = 0.5
        
        # Source reliability factor
        source_type = source_data.source_type
        if source_type == 'official_blog':
            base_confidence += 0.3
        elif source_type == 'github_api':
            base_confidence += 0.4
        elif source_type == 'npm_registry':
            base_confidence += 0.3
        
        # Content quality factors
        content_length = len(source_data.content)
        if content_length > 1000:  # Substantial content
            base_confidence += 0.1
        
        # Metadata quality
        versions_found = len(source_data.extraction_metadata.get('extracted_versions', []))
        if versions_found > 0:
            base_confidence += 0.1
        
        return min(base_confidence, 1.0)
    
    def _calculate_impact_level(self, technology_name: str, change_type: ChangeType) -> ImpactLevel:
        """Calculate impact level based on technology and change type"""
        # Base impact from change type
        type_impact = {
            ChangeType.BREAKING_CHANGE: ImpactLevel.CRITICAL,
            ChangeType.SECURITY_UPDATE: ImpactLevel.HIGH,
            ChangeType.DEPRECATION_WARNING: ImpactLevel.HIGH,
            ChangeType.FEATURE_ADDITION: ImpactLevel.MEDIUM,
            ChangeType.BUG_FIX: ImpactLevel.LOW,
            ChangeType.CONFIGURATION_CHANGE: ImpactLevel.MEDIUM
        }
        
        base_impact = type_impact.get(change_type, ImpactLevel.LOW)
        
        # Adjust based on technology criticality
        tech_config = self._get_technology_config(technology_name)
        if tech_config:
            criticality = tech_config.get('criticality', 'low')
            if criticality == 'high' and base_impact != ImpactLevel.CRITICAL:
                # Boost impact level for critical technologies
                impact_levels = [ImpactLevel.MINIMAL, ImpactLevel.LOW, ImpactLevel.MEDIUM, 
                               ImpactLevel.HIGH, ImpactLevel.CRITICAL]
                current_index = impact_levels.index(base_impact)
                if current_index < len(impact_levels) - 1:
                    base_impact = impact_levels[current_index + 1]
        
        return base_impact
    
    def _calculate_urgency_level(self, change_type: ChangeType, impact_level: ImpactLevel) -> UrgencyLevel:
        """Calculate urgency level based on change type and impact"""
        # Base urgency from change type
        type_urgency = {
            ChangeType.BREAKING_CHANGE: UrgencyLevel.IMMEDIATE,
            ChangeType.SECURITY_UPDATE: UrgencyLevel.URGENT,
            ChangeType.DEPRECATION_WARNING: UrgencyLevel.HIGH,
            ChangeType.FEATURE_ADDITION: UrgencyLevel.LOW,
            ChangeType.BUG_FIX: UrgencyLevel.MEDIUM,
            ChangeType.CONFIGURATION_CHANGE: UrgencyLevel.MEDIUM
        }
        
        base_urgency = type_urgency.get(change_type, UrgencyLevel.LOW)
        
        # Adjust based on impact level
        if impact_level == ImpactLevel.CRITICAL:
            return UrgencyLevel.IMMEDIATE
        elif impact_level == ImpactLevel.HIGH and base_urgency != UrgencyLevel.IMMEDIATE:
            urgency_levels = [UrgencyLevel.LOW, UrgencyLevel.MEDIUM, UrgencyLevel.HIGH, 
                            UrgencyLevel.URGENT, UrgencyLevel.IMMEDIATE]
            current_index = urgency_levels.index(base_urgency)
            if current_index < len(urgency_levels) - 1:
                base_urgency = urgency_levels[current_index + 1]
        
        return base_urgency
    
    def _extract_change_evidence(self, content: str, change_type: ChangeType) -> List[str]:
        """Extract evidence supporting the detected change"""
        evidence = []
        
        try:
            # Look for change type specific patterns
            pattern_key = f'{change_type.value}_keywords'
            if pattern_key in self.patterns:
                matches = self.patterns[pattern_key].findall(content)
                evidence.extend(matches[:5])  # Limit to 5 pieces of evidence
            
            # Extract version-related evidence
            version_matches = self.patterns['semantic_version'].findall(content)
            for match in version_matches[:3]:  # Limit to 3 versions
                version = f"{match[0]}.{match[1]}.{match[2]}"
                evidence.append(f"Version: {version}")
            
        except Exception as e:
            logger.error(f"Error extracting evidence: {e}")
        
        return evidence
    
    def _get_technology_config(self, technology_name: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific technology"""
        # Check all tiers for the technology
        for tier in ['tier_1_critical_technologies', 'tier_2_important_technologies', 
                     'tier_3_supplemental_technologies']:
            if tier in self.tech_config and technology_name in self.tech_config[tier]:
                return self.tech_config[tier][technology_name]
        
        return None
    
    async def get_performance_stats(self) -> Dict[str, Any]:
        """Get current performance statistics"""
        return self.performance_stats.copy()
    
    async def reset_performance_stats(self):
        """Reset performance statistics"""
        self.performance_stats = {
            'detections_processed': 0,
            'changes_detected': 0,
            'false_positives': 0,
            'average_processing_time': 0.0
        }
        logger.info("Performance statistics reset")


class ChangeValidator:
    """Validates detected changes for accuracy and reduces false positives"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config = config_manager
        self.classification_rules = config_manager.get_classification_rules()
    
    async def validate_change(self, change: TechnologyChange) -> Tuple[bool, float]:
        """
        Validate a detected change and return validation status and adjusted confidence
        
        Args:
            change: The detected change to validate
            
        Returns:
            Tuple of (is_valid, adjusted_confidence)
        """
        try:
            # Apply validation rules
            validation_score = 1.0
            
            # Confidence threshold validation
            min_confidence = self._get_min_confidence_threshold(change.change_type)
            if change.confidence_score < min_confidence:
                return False, change.confidence_score
            
            # Version consistency validation
            if change.old_version and change.new_version:
                if not self._validate_version_progression(change.old_version, change.new_version):
                    validation_score *= 0.5
            
            # Evidence quality validation
            evidence_score = self._validate_evidence_quality(change.evidence, change.change_type)
            validation_score *= evidence_score
            
            # Cross-validation with other sources (if available)
            # This would be implemented with additional MCP server checks
            
            adjusted_confidence = change.confidence_score * validation_score
            is_valid = adjusted_confidence >= min_confidence
            
            return is_valid, adjusted_confidence
            
        except Exception as e:
            logger.error(f"Error validating change: {e}")
            return False, 0.0
    
    def _get_min_confidence_threshold(self, change_type: ChangeType) -> float:
        """Get minimum confidence threshold for change type"""
        thresholds = {
            ChangeType.BREAKING_CHANGE: 0.7,
            ChangeType.SECURITY_UPDATE: 0.8,
            ChangeType.DEPRECATION_WARNING: 0.6,
            ChangeType.FEATURE_ADDITION: 0.5,
            ChangeType.BUG_FIX: 0.4,
            ChangeType.CONFIGURATION_CHANGE: 0.5
        }
        return thresholds.get(change_type, 0.5)
    
    def _validate_version_progression(self, old_version: str, new_version: str) -> bool:
        """Validate that version progression makes sense"""
        try:
            # Clean versions
            old_clean = self._clean_version(old_version)
            new_clean = self._clean_version(new_version)
            
            old_parts = [int(x) for x in old_clean.split('.')]
            new_parts = [int(x) for x in new_clean.split('.')]
            
            # Pad to same length
            while len(old_parts) < 3:
                old_parts.append(0)
            while len(new_parts) < 3:
                new_parts.append(0)
            
            # Check if new version is actually newer
            for i in range(3):
                if new_parts[i] > old_parts[i]:
                    return True
                elif new_parts[i] < old_parts[i]:
                    return False
            
            return False  # Versions are the same
            
        except Exception as e:
            logger.error(f"Error validating version progression: {e}")
            return False
    
    def _clean_version(self, version: str) -> str:
        """Clean version string for comparison"""
        if not version or version == "latest":
            return "0.0.0"
        
        version = version.lstrip('v')
        
        # Simple version extraction
        parts = version.split('.')
        if len(parts) >= 3:
            try:
                # Validate parts are numeric
                int(parts[0])
                int(parts[1])
                int(parts[2])
                return f"{parts[0]}.{parts[1]}.{parts[2]}"
            except ValueError:
                pass
        
        return "0.0.0"
    
    def _validate_evidence_quality(self, evidence: List[str], change_type: ChangeType) -> float:
        """Validate quality of evidence supporting the change"""
        if not evidence:
            return 0.5
        
        # Base score
        score = 0.6
        
        # Evidence quantity bonus
        if len(evidence) >= 3:
            score += 0.2
        elif len(evidence) >= 2:
            score += 0.1
        
        # Evidence quality based on change type
        if change_type == ChangeType.SECURITY_UPDATE:
            security_keywords = ['security', 'vulnerability', 'CVE', 'exploit']
            if any(keyword in ' '.join(evidence).lower() for keyword in security_keywords):
                score += 0.2
        
        elif change_type == ChangeType.BREAKING_CHANGE:
            breaking_keywords = ['breaking', 'incompatible', 'migration']
            if any(keyword in ' '.join(evidence).lower() for keyword in breaking_keywords):
                score += 0.2
        
        return min(score, 1.0)