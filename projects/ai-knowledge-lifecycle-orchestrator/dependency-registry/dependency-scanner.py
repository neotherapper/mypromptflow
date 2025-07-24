#!/usr/bin/env python3
"""
AI Knowledge Lifecycle Orchestrator - Dependency Scanner

This script scans AI instruction files to automatically detect technology dependencies,
building a comprehensive registry for automated knowledge lifecycle management.

Usage:
    python dependency-scanner.py [--config CONFIG_FILE] [--output OUTPUT_FILE] [--debug]
"""

import os
import re
import yaml
import json
import hashlib
import logging
import argparse
import concurrent.futures
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from glob import glob
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dependency-registry/scanner.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class TechnologyReference:
    """Represents a detected technology reference in a file."""
    name: str
    category: str
    confidence: float
    version_constraint: Optional[str] = None
    current_version: Optional[str] = None
    criticality: str = "medium"
    usage_context: List[str] = None
    references: List[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.usage_context is None:
            self.usage_context = []
        if self.references is None:
            self.references = []

@dataclass
class FileAnalysis:
    """Represents the complete analysis of an AI instruction file."""
    file_path: str
    file_type: str
    file_hash: str
    last_modified: str
    last_scanned: str
    scan_confidence: float
    technologies: List[TechnologyReference]
    
class DependencyScanner:
    """Main scanner class for detecting technology dependencies in AI files."""
    
    def __init__(self, config_path: str = "dependency-registry/scanner-config.yaml"):
        """Initialize the scanner with configuration."""
        self.config = self._load_config(config_path)
        self.setup_logging()
        self.technology_patterns = self._compile_patterns()
        self.scanned_files = {}
        self.stats = {
            'files_scanned': 0,
            'technologies_detected': 0,
            'high_confidence_detections': 0,
            'processing_time': 0
        }
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load scanner configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {config_path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"Error parsing configuration: {e}")
            raise
            
    def setup_logging(self):
        """Configure logging based on configuration settings."""
        log_level = getattr(logging, self.config['scanner_configuration']['output_configuration']['log_level'])
        logger.setLevel(log_level)
        
    def _compile_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Compile regex patterns for technology detection."""
        patterns = {}
        detection_config = self.config['scanner_configuration']['technology_detection']['detection_patterns']
        
        for tech_name, tech_config in detection_config.items():
            compiled_patterns = []
            for pattern in tech_config['patterns']:
                try:
                    compiled_patterns.append(re.compile(pattern, re.IGNORECASE | re.MULTILINE))
                except re.error as e:
                    logger.warning(f"Invalid regex pattern for {tech_name}: {pattern} - {e}")
                    continue
                    
            patterns[tech_name] = {
                'patterns': compiled_patterns,
                'context_keywords': tech_config.get('context_keywords', []),
                'minimum_confidence': tech_config.get('minimum_confidence', 0.7)
            }
            
        return patterns
        
    def discover_files(self) -> List[str]:
        """Discover AI instruction files to scan based on configuration."""
        discovered_files = []
        file_discovery = self.config['scanner_configuration']['file_discovery']
        
        for base_dir in file_discovery['base_directories']:
            for pattern in file_discovery['include_patterns']:
                full_pattern = os.path.join(base_dir, pattern)
                files = glob(full_pattern, recursive=True)
                discovered_files.extend(files)
                
        # Filter out excluded patterns
        filtered_files = []
        for file_path in discovered_files:
            exclude = False
            for exclude_pattern in file_discovery['exclude_patterns']:
                # Convert glob patterns to directory/file checks
                if exclude_pattern.endswith('/**'):
                    # Directory exclusion pattern like **/node_modules/**
                    dir_name = exclude_pattern.replace('**/', '').replace('/**', '')
                    if f'/{dir_name}/' in file_path or file_path.endswith(f'/{dir_name}'):
                        exclude = True
                        break
                elif exclude_pattern.startswith('**/') and '*' in exclude_pattern[3:]:
                    # File extension pattern like **/*.log
                    ext = exclude_pattern.replace('**/', '').replace('*', '')
                    if file_path.endswith(ext):
                        exclude = True
                        break
                else:
                    # Simple substring check for other patterns
                    pattern_core = exclude_pattern.replace('**/', '').replace('/**', '').replace('*', '')
                    if pattern_core and pattern_core in file_path:
                        exclude = True
                        break
            if not exclude:
                filtered_files.append(file_path)
                
        # Filter by file size
        size_filtered_files = []
        max_size = file_discovery['file_size_limits']['maximum_file_size_mb'] * 1024 * 1024
        min_size = file_discovery['file_size_limits']['minimum_file_size_bytes']
        
        for file_path in filtered_files:
            try:
                if os.path.exists(file_path):
                    file_size = os.path.getsize(file_path)
                    if min_size <= file_size <= max_size:
                        size_filtered_files.append(file_path)
            except OSError:
                logger.warning(f"Could not access file: {file_path}")
                continue
                
        logger.info(f"Discovered {len(size_filtered_files)} files to scan")
        return size_filtered_files
        
    def get_file_hash(self, file_path: str) -> str:
        """Calculate SHA-256 hash of file content."""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception as e:
            logger.error(f"Error calculating hash for {file_path}: {e}")
            return ""
            
    def classify_file_type(self, file_path: str) -> str:
        """Classify the type of AI instruction file."""
        path_lower = file_path.lower()
        
        if path_lower.endswith('claude.md'):
            return "claude_md"
        elif '/.claude/commands/' in path_lower:
            return "command_file"
        elif '/knowledge-vault/knowledge/' in path_lower:
            return "tool_documentation"
        elif '/tools/' in path_lower:
            return "tool_documentation"
        elif '/docs/' in path_lower:
            return "project_documentation"
        elif path_lower.endswith('readme.md'):
            return "project_documentation"
        else:
            return "instruction"
            
    def read_file_content(self, file_path: str) -> Tuple[str, datetime]:
        """Read file content and get modification time."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            mod_time = datetime.fromtimestamp(os.path.getmtime(file_path), tz=timezone.utc)
            return content, mod_time
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return "", datetime.now(timezone.utc)
            
    def detect_version(self, text: str, tech_name: str) -> Optional[str]:
        """Detect version information for a technology in text."""
        version_patterns = self.config['scanner_configuration']['technology_detection']['version_patterns']
        
        # Look for semantic version pattern near technology name
        tech_pattern = re.compile(rf"\b{re.escape(tech_name)}\b.*?{version_patterns['semantic_version']}", re.IGNORECASE)
        match = tech_pattern.search(text)
        if match:
            return match.group(1) + '.' + match.group(2) + '.' + match.group(3)
            
        # Look for major version pattern
        major_pattern = re.compile(rf"\b{re.escape(tech_name)}\b.*?{version_patterns['major_version']}", re.IGNORECASE)
        match = major_pattern.search(text)
        if match:
            return match.group(1) or match.group(2)
            
        # Look for range version pattern
        range_pattern = re.compile(rf"\b{re.escape(tech_name)}\b.*?{version_patterns['range_version']}", re.IGNORECASE)
        match = range_pattern.search(text)
        if match:
            return match.group(1)
            
        return None
        
    def analyze_context(self, text: str, line_num: int, tech_name: str) -> Tuple[List[str], float]:
        """Analyze context around a technology reference for usage patterns and confidence."""
        lines = text.split('\n')
        context_window = self.config['scanner_configuration']['technology_detection']['context_analysis']['context_window_lines']
        
        # Get context lines
        start_line = max(0, line_num - context_window)
        end_line = min(len(lines), line_num + context_window + 1)
        context_text = ' '.join(lines[start_line:end_line]).lower()
        
        # Detect usage context
        usage_context = []
        context_patterns = {
            'installation': ['install', 'setup', 'npm install', 'yarn add', 'pip install'],
            'configuration': ['config', 'configure', 'settings', 'options', '.config.'],
            'code_examples': ['```', 'example', 'code', 'snippet'],
            'best_practices': ['best practice', 'recommended', 'should', 'avoid'],
            'troubleshooting': ['error', 'issue', 'problem', 'debug', 'fix'],
            'integration': ['integrate', 'connect', 'plugin', 'extension'],
            'testing': ['test', 'spec', 'jest', 'unit', 'integration'],
            'deployment': ['deploy', 'build', 'production', 'docker', 'ci/cd']
        }
        
        for context_type, keywords in context_patterns.items():
            if any(keyword in context_text for keyword in keywords):
                usage_context.append(context_type)
                
        # Calculate confidence boost
        confidence_boost = 0.0
        tech_config = self.technology_patterns.get(tech_name, {})
        context_keywords = tech_config.get('context_keywords', [])
        
        for keyword in context_keywords:
            if keyword.lower() in context_text:
                confidence_boost += self.config['scanner_configuration']['technology_detection']['confidence_calculation']['context_keyword_bonus']
                
        # Additional confidence boosts
        if '```' in context_text:  # Code block
            confidence_boost += self.config['scanner_configuration']['technology_detection']['context_analysis']['code_block_boost'] - 1.0
            
        if any(marker in context_text for marker in ['#', '##', '###']):  # Heading
            confidence_boost += self.config['scanner_configuration']['technology_detection']['context_analysis']['title_boost'] - 1.0
            
        return usage_context, confidence_boost
        
    def detect_technologies(self, content: str, file_path: str) -> List[TechnologyReference]:
        """Detect technology dependencies in file content."""
        detected_technologies = []
        lines = content.split('\n')
        
        for tech_name, tech_config in self.technology_patterns.items():
            references = []
            total_confidence = 0.0
            pattern_matches = 0
            
            # Check each pattern for this technology
            for pattern in tech_config['patterns']:
                for match in pattern.finditer(content):
                    pattern_matches += 1
                    line_num = content[:match.start()].count('\n')
                    context_line = lines[line_num] if line_num < len(lines) else ""
                    
                    # Analyze context around the match
                    usage_context, confidence_boost = self.analyze_context(content, line_num, tech_name)
                    
                    # Calculate confidence for this reference
                    base_confidence = self.config['scanner_configuration']['technology_detection']['confidence_calculation']['base_confidence']
                    reference_confidence = base_confidence + confidence_boost
                    
                    # Detect version if present
                    version = self.detect_version(context_line, tech_name)
                    if version:
                        reference_confidence += self.config['scanner_configuration']['technology_detection']['confidence_calculation']['version_reference_bonus']
                        
                    references.append({
                        'line_number': line_num + 1,
                        'context': context_line.strip()[:200],  # Limit context length
                        'reference_type': 'explicit_mention',
                        'confidence': min(1.0, reference_confidence)
                    })
                    
                    total_confidence += reference_confidence
                    
            # Create technology reference if we found matches above minimum confidence
            if pattern_matches > 0:
                # Calculate overall confidence
                avg_confidence = total_confidence / pattern_matches
                
                # Apply multiple pattern bonus
                if pattern_matches > 1:
                    multiple_bonus = min(0.3, pattern_matches * self.config['scanner_configuration']['technology_detection']['confidence_calculation']['multiple_pattern_bonus'])
                    avg_confidence += multiple_bonus
                    
                # Ensure confidence is within bounds
                avg_confidence = min(1.0, max(0.0, avg_confidence))
                
                # Only include if above minimum threshold
                if avg_confidence >= tech_config['minimum_confidence']:
                    # Get technology category and criticality from standardized definitions
                    tech_definitions = self.config.get('technology_definitions', {}).get('standardized_technologies', {})
                    tech_def = tech_definitions.get(tech_name, {})
                    
                    # Determine usage context from all references
                    all_usage_contexts = set()
                    for ref in references:
                        usage_context, _ = self.analyze_context(content, ref['line_number'] - 1, tech_name)
                        all_usage_contexts.update(usage_context)
                        
                    tech_ref = TechnologyReference(
                        name=tech_name,
                        category=tech_def.get('category', 'unknown'),
                        confidence=avg_confidence,
                        version_constraint=None,  # Will be populated by version detection
                        current_version=tech_def.get('current_stable'),
                        criticality=tech_def.get('criticality_default', 'medium'),
                        usage_context=list(all_usage_contexts),
                        references=references
                    )
                    
                    detected_technologies.append(tech_ref)
                    
        logger.debug(f"Detected {len(detected_technologies)} technologies in {file_path}")
        return detected_technologies
        
    def analyze_file(self, file_path: str) -> Optional[FileAnalysis]:
        """Analyze a single AI instruction file for technology dependencies."""
        try:
            start_time = time.time()
            
            # Read file content and metadata
            content, mod_time = self.read_file_content(file_path)
            if not content:
                return None
                
            file_hash = self.get_file_hash(file_path)
            file_type = self.classify_file_type(file_path)
            
            # Detect technologies
            technologies = self.detect_technologies(content, file_path)
            
            # Calculate overall scan confidence
            if technologies:
                scan_confidence = sum(tech.confidence for tech in technologies) / len(technologies)
            else:
                scan_confidence = 1.0  # High confidence in finding no technologies
                
            analysis = FileAnalysis(
                file_path=file_path,
                file_type=file_type,
                file_hash=file_hash,
                last_modified=mod_time.isoformat(),
                last_scanned=datetime.now(timezone.utc).isoformat(),
                scan_confidence=scan_confidence,
                technologies=technologies
            )
            
            # Update statistics
            processing_time = time.time() - start_time
            self.stats['files_scanned'] += 1
            self.stats['technologies_detected'] += len(technologies)
            self.stats['high_confidence_detections'] += sum(1 for tech in technologies if tech.confidence >= 0.9)
            self.stats['processing_time'] += processing_time
            
            if self.stats['files_scanned'] % 10 == 0:
                logger.info(f"Processed {self.stats['files_scanned']} files, found {self.stats['technologies_detected']} technologies")
                
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing file {file_path}: {e}")
            return None
            
    def scan_files(self, file_paths: List[str]) -> Dict[str, FileAnalysis]:
        """Scan multiple files for technology dependencies using concurrent processing."""
        results = {}
        max_workers = self.config['scanner_configuration']['performance_settings']['max_concurrent_files']
        
        logger.info(f"Starting scan of {len(file_paths)} files with {max_workers} workers")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all files for processing
            future_to_file = {executor.submit(self.analyze_file, file_path): file_path 
                             for file_path in file_paths}
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    analysis = future.result()
                    if analysis:
                        results[file_path] = analysis
                except Exception as e:
                    logger.error(f"Error processing {file_path}: {e}")
                    
        logger.info(f"Scan completed. Analyzed {len(results)} files successfully")
        return results
        
    def generate_registry(self, analyses: Dict[str, FileAnalysis]) -> Dict[str, Any]:
        """Generate the complete dependency registry from file analyses."""
        registry = {
            'version': '1.0.0',
            'generated': datetime.now(timezone.utc).isoformat(),
            'statistics': {
                'total_files_scanned': len(analyses),
                'total_technologies_detected': sum(len(analysis.technologies) for analysis in analyses.values()),
                'high_confidence_detections': sum(
                    sum(1 for tech in analysis.technologies if tech.confidence >= 0.9)
                    for analysis in analyses.values()
                ),
                'average_technologies_per_file': self.stats['technologies_detected'] / max(1, self.stats['files_scanned']),
                'processing_time_seconds': self.stats['processing_time'],
                'files_per_second': len(analyses) / max(1, self.stats['processing_time'])
            },
            'files': {}
        }
        
        # Convert analyses to registry format
        for file_path, analysis in analyses.items():
            registry['files'][file_path] = {
                'file_path': analysis.file_path,
                'file_type': analysis.file_type,
                'file_hash': analysis.file_hash,
                'last_modified': analysis.last_modified,
                'last_scanned': analysis.last_scanned,
                'scan_confidence': analysis.scan_confidence,
                'technologies': [asdict(tech) for tech in analysis.technologies],
                'dependency_relationships': {
                    'depends_on': [],
                    'depended_on_by': []
                },
                'update_tracking': {
                    'needs_update': False,
                    'update_priority': 'none',
                    'pending_updates': [],
                    'last_updated': None,
                    'update_history': []
                }
            }
            
        return registry
        
    def save_registry(self, registry: Dict[str, Any], output_path: str):
        """Save the dependency registry to a YAML file."""
        try:
            # Create backup if file exists
            if os.path.exists(output_path):
                backup_path = f"{output_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                os.rename(output_path, backup_path)
                logger.info(f"Created backup: {backup_path}")
                
            # Save registry
            with open(output_path, 'w') as f:
                yaml.dump(registry, f, default_flow_style=False, sort_keys=False, indent=2)
                
            logger.info(f"Registry saved to: {output_path}")
            
        except Exception as e:
            logger.error(f"Error saving registry: {e}")
            raise
            
    def run_scan(self, output_path: str = "dependency-registry/registry.yaml"):
        """Execute the complete dependency scanning process."""
        logger.info("Starting AI Knowledge Lifecycle Orchestrator dependency scan")
        
        start_time = time.time()
        
        try:
            # Discover files to scan
            file_paths = self.discover_files()
            if not file_paths:
                logger.warning("No files found to scan")
                return
                
            # Scan all files
            analyses = self.scan_files(file_paths)
            
            # Generate registry
            registry = self.generate_registry(analyses)
            
            # Save registry
            self.save_registry(registry, output_path)
            
            # Print summary
            total_time = time.time() - start_time
            logger.info("="*60)
            logger.info("DEPENDENCY SCAN SUMMARY")
            logger.info("="*60)
            logger.info(f"Files scanned: {registry['statistics']['total_files_scanned']}")
            logger.info(f"Technologies detected: {registry['statistics']['total_technologies_detected']}")
            logger.info(f"High confidence detections: {registry['statistics']['high_confidence_detections']}")
            logger.info(f"Average technologies per file: {registry['statistics']['average_technologies_per_file']:.2f}")
            logger.info(f"Total processing time: {total_time:.2f} seconds")
            logger.info(f"Processing rate: {registry['statistics']['files_per_second']:.2f} files/second")
            logger.info("="*60)
            
        except Exception as e:
            logger.error(f"Scan failed: {e}")
            raise

def main():
    """Main entry point for the dependency scanner."""
    parser = argparse.ArgumentParser(description="AI Knowledge Lifecycle Orchestrator Dependency Scanner")
    parser.add_argument('--config', default='dependency-registry/scanner-config.yaml',
                       help='Path to configuration file')
    parser.add_argument('--output', default='dependency-registry/registry.yaml',
                       help='Path to output registry file')
    parser.add_argument('--debug', action='store_true',
                       help='Enable debug logging')
    
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        
    try:
        scanner = DependencyScanner(args.config)
        scanner.run_scan(args.output)
        logger.info("Dependency scan completed successfully")
        
    except KeyboardInterrupt:
        logger.info("Scan interrupted by user")
    except Exception as e:
        logger.error(f"Scan failed: {e}")
        return 1
        
    return 0

if __name__ == "__main__":
    exit(main())