#!/usr/bin/env python3
"""
Configuration Manager
AI Knowledge Lifecycle Orchestrator - Configuration loading and validation

This module manages all configuration files for the change detection system,
providing a centralized interface for accessing and validating configurations.
"""

import yaml
import logging
import os
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from datetime import datetime
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ConfigValidationResult:
    """Result of configuration validation"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    
    def add_error(self, error: str):
        """Add validation error"""
        self.errors.append(error)
        self.is_valid = False
    
    def add_warning(self, warning: str):
        """Add validation warning"""
        self.warnings.append(warning)


class ConfigManager:
    """
    Centralized configuration management for the change detection system.
    Loads, validates, and provides access to all configuration files.
    """
    
    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize configuration manager
        
        Args:
            config_dir: Directory containing configuration files
        """
        self.config_dir = config_dir or Path(__file__).parent
        self.configs = {}
        self.validation_results = {}
        
        # Configuration file mappings
        self.config_files = {
            'architecture': 'change-detection-architecture.yaml',
            'technology_sources': 'technology-source-config.yaml',
            'classification_rules': 'change-classification-rules.yaml',
            'mcp_integration': 'mcp-integration-patterns.yaml',
            'storage_caching': 'storage-and-caching-design.yaml'
        }
        
        # Load all configurations
        self._load_all_configurations()
        
        logger.info(f"Configuration Manager initialized with {len(self.configs)} config files")
    
    def _load_all_configurations(self):
        """Load all configuration files"""
        for config_name, filename in self.config_files.items():
            try:
                config_path = self.config_dir / filename
                if config_path.exists():
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config_data = yaml.safe_load(f)
                        self.configs[config_name] = config_data
                        logger.info(f"Loaded configuration: {config_name}")
                else:
                    logger.warning(f"Configuration file not found: {config_path}")
                    self.configs[config_name] = {}
            except Exception as e:
                logger.error(f"Error loading configuration {config_name}: {e}")
                self.configs[config_name] = {}
        
        # Validate all configurations
        self._validate_all_configurations()
    
    def _validate_all_configurations(self):
        """Validate all loaded configurations"""
        self.validation_results = {}
        
        for config_name in self.config_files.keys():
            self.validation_results[config_name] = self._validate_configuration(config_name)
        
        # Report validation results
        self._report_validation_results()
    
    def _validate_configuration(self, config_name: str) -> ConfigValidationResult:
        """Validate a specific configuration"""
        result = ConfigValidationResult(is_valid=True, errors=[], warnings=[])
        config_data = self.configs.get(config_name, {})
        
        if not config_data:
            result.add_error(f"Configuration {config_name} is empty or failed to load")
            return result
        
        # Validate based on configuration type
        if config_name == 'architecture':
            self._validate_architecture_config(config_data, result)
        elif config_name == 'technology_sources':
            self._validate_technology_sources_config(config_data, result)
        elif config_name == 'classification_rules':
            self._validate_classification_rules_config(config_data, result)
        elif config_name == 'mcp_integration':
            self._validate_mcp_integration_config(config_data, result)
        elif config_name == 'storage_caching':
            self._validate_storage_caching_config(config_data, result)
        
        return result
    
    def _validate_architecture_config(self, config: Dict[str, Any], result: ConfigValidationResult):
        """Validate architecture configuration"""
        required_sections = ['system_overview', 'architecture_components', 'integration_architecture']
        
        for section in required_sections:
            if section not in config:
                result.add_error(f"Missing required section: {section}")
        
        # Validate component structure
        if 'architecture_components' in config:
            components = config['architecture_components']
            required_components = [
                'source_monitor_controller',
                'change_detection_engine',
                'mcp_integration_layer',
                'storage_caching_layer',
                'notification_alert_system'
            ]
            
            for component in required_components:
                if component not in components:
                    result.add_error(f"Missing required component: {component}")
                else:
                    # Validate component structure
                    comp_config = components[component]
                    if 'description' not in comp_config:
                        result.add_warning(f"Component {component} missing description")
                    if 'responsibilities' not in comp_config:
                        result.add_warning(f"Component {component} missing responsibilities")
    
    def _validate_technology_sources_config(self, config: Dict[str, Any], result: ConfigValidationResult):
        """Validate technology sources configuration"""
        required_tiers = ['tier_1_critical_technologies', 'tier_2_important_technologies', 'tier_3_supplemental_technologies']
        
        for tier in required_tiers:
            if tier not in config:
                result.add_error(f"Missing required tier: {tier}")
                continue
            
            # Validate technologies in tier
            tier_config = config[tier]
            for tech_name, tech_config in tier_config.items():
                self._validate_technology_config(tech_name, tech_config, result)
        
        # Validate extraction patterns
        if 'extraction_patterns' not in config:
            result.add_warning("Missing extraction patterns section")
    
    def _validate_technology_config(self, tech_name: str, tech_config: Dict[str, Any], result: ConfigValidationResult):
        """Validate individual technology configuration"""
        required_fields = ['official_sources', 'monitoring_config', 'current_version', 'criticality']
        
        for field in required_fields:
            if field not in tech_config:
                result.add_error(f"Technology {tech_name} missing required field: {field}")
        
        # Validate official sources
        if 'official_sources' in tech_config:
            sources = tech_config['official_sources']
            for source_name, source_config in sources.items():
                required_source_fields = ['url', 'type', 'mcp_server', 'extraction_pattern']
                for field in required_source_fields:
                    if field not in source_config:
                        result.add_error(f"Technology {tech_name}, source {source_name} missing field: {field}")
        
        # Validate monitoring config
        if 'monitoring_config' in tech_config:
            monitoring = tech_config['monitoring_config']
            required_monitoring_fields = ['check_frequency', 'priority_level', 'notification_delay']
            for field in required_monitoring_fields:
                if field not in monitoring:
                    result.add_warning(f"Technology {tech_name} monitoring config missing field: {field}")
    
    def _validate_classification_rules_config(self, config: Dict[str, Any], result: ConfigValidationResult):
        """Validate classification rules configuration"""
        required_sections = ['change_type_classification', 'impact_assessment', 'urgency_classification', 'confidence_scoring']
        
        for section in required_sections:
            if section not in config:
                result.add_error(f"Missing required section: {section}")
        
        # Validate change type classifications
        if 'change_type_classification' in config:
            change_types = config['change_type_classification']
            expected_change_types = [
                'breaking_change', 'security_update', 'deprecation_warning',
                'feature_addition', 'bug_fix', 'configuration_change'
            ]
            
            for change_type in expected_change_types:
                if change_type not in change_types:
                    result.add_warning(f"Missing change type classification: {change_type}")
                else:
                    # Validate change type structure
                    ct_config = change_types[change_type]
                    if 'detection_patterns' not in ct_config:
                        result.add_error(f"Change type {change_type} missing detection_patterns")
                    if 'impact_calculation' not in ct_config:
                        result.add_warning(f"Change type {change_type} missing impact_calculation")
    
    def _validate_mcp_integration_config(self, config: Dict[str, Any], result: ConfigValidationResult):
        """Validate MCP integration configuration"""
        required_sections = ['integration_architecture', 'available_mcp_servers', 'integration_patterns']
        
        for section in required_sections:
            if section not in config:
                result.add_error(f"Missing required section: {section}")
        
        # Validate MCP servers
        if 'available_mcp_servers' in config:
            servers = config['available_mcp_servers']
            expected_servers = ['fetch_server', 'github_server', 'search_server', 'browser_automation_server']
            
            for server in expected_servers:
                if server not in servers:
                    result.add_warning(f"Missing MCP server configuration: {server}")
                else:
                    # Validate server structure
                    server_config = servers[server]
                    required_server_fields = ['server_name', 'description', 'capabilities']
                    for field in required_server_fields:
                        if field not in server_config:
                            result.add_error(f"MCP server {server} missing field: {field}")
    
    def _validate_storage_caching_config(self, config: Dict[str, Any], result: ConfigValidationResult):
        """Validate storage and caching configuration"""
        # This would be implemented when storage-and-caching-design.yaml is available
        if not config:
            result.add_warning("Storage and caching configuration is empty")
    
    def _report_validation_results(self):
        """Report configuration validation results"""
        total_errors = sum(len(result.errors) for result in self.validation_results.values())
        total_warnings = sum(len(result.warnings) for result in self.validation_results.values())
        
        if total_errors > 0:
            logger.error(f"Configuration validation found {total_errors} errors and {total_warnings} warnings")
            for config_name, result in self.validation_results.items():
                if result.errors:
                    logger.error(f"Errors in {config_name}: {', '.join(result.errors)}")
                if result.warnings:
                    logger.warning(f"Warnings in {config_name}: {', '.join(result.warnings)}")
        elif total_warnings > 0:
            logger.warning(f"Configuration validation found {total_warnings} warnings")
            for config_name, result in self.validation_results.items():
                if result.warnings:
                    logger.warning(f"Warnings in {config_name}: {', '.join(result.warnings)}")
        else:
            logger.info("All configurations validated successfully")
    
    def get_architecture_config(self) -> Dict[str, Any]:
        """Get architecture configuration"""
        return self.configs.get('architecture', {})
    
    def get_technology_config(self) -> Dict[str, Any]:
        """Get technology sources configuration"""
        return self.configs.get('technology_sources', {})
    
    def get_classification_rules(self) -> Dict[str, Any]:
        """Get change classification rules"""
        return self.configs.get('classification_rules', {})
    
    def get_mcp_integration_config(self) -> Dict[str, Any]:
        """Get MCP integration configuration"""
        return self.configs.get('mcp_integration', {})
    
    def get_storage_config(self) -> Dict[str, Any]:
        """Get storage and caching configuration"""
        return self.configs.get('storage_caching', {})
    
    def get_all_technologies(self) -> Dict[str, Dict[str, Any]]:
        """Get all configured technologies from all tiers"""
        tech_config = self.get_technology_config()
        all_technologies = {}
        
        # Combine all tiers
        for tier_name in ['tier_1_critical_technologies', 'tier_2_important_technologies', 'tier_3_supplemental_technologies']:
            tier_data = tech_config.get(tier_name, {})
            for tech_name, tech_config in tier_data.items():
                # Add tier information to technology config
                tech_config_copy = tech_config.copy()
                tech_config_copy['tier'] = tier_name
                all_technologies[tech_name] = tech_config_copy
        
        return all_technologies
    
    def get_technology_by_name(self, technology_name: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific technology"""
        all_technologies = self.get_all_technologies()
        return all_technologies.get(technology_name)
    
    def get_critical_technologies(self) -> List[str]:
        """Get list of critical technology names"""
        tech_config = self.get_technology_config()
        tier_1 = tech_config.get('tier_1_critical_technologies', {})
        return list(tier_1.keys())
    
    def get_technologies_by_criticality(self, criticality: str) -> List[str]:
        """Get technologies by criticality level"""
        all_technologies = self.get_all_technologies()
        return [
            name for name, config in all_technologies.items()
            if config.get('criticality') == criticality
        ]
    
    def get_mcp_server_config(self, server_name: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific MCP server"""
        mcp_config = self.get_mcp_integration_config()
        servers = mcp_config.get('available_mcp_servers', {})
        
        # Try direct lookup first
        if server_name in servers:
            return servers[server_name]
        
        # Try lookup by server_name field
        for server_key, server_config in servers.items():
            if server_config.get('server_name') == server_name:
                return server_config
        
        return None
    
    def get_change_type_rules(self, change_type: str) -> Optional[Dict[str, Any]]:
        """Get classification rules for a specific change type"""
        classification_rules = self.get_classification_rules()
        change_types = classification_rules.get('change_type_classification', {})
        return change_types.get(change_type)
    
    def get_extraction_pattern(self, pattern_name: str) -> Optional[Dict[str, Any]]:
        """Get extraction pattern configuration"""
        tech_config = self.get_technology_config()
        extraction_patterns = tech_config.get('extraction_patterns', {})
        return extraction_patterns.get(pattern_name)
    
    def is_configuration_valid(self, config_name: str = None) -> bool:
        """Check if configuration(s) are valid"""
        if config_name:
            result = self.validation_results.get(config_name)
            return result.is_valid if result else False
        
        # Check all configurations
        return all(result.is_valid for result in self.validation_results.values())
    
    def get_validation_errors(self, config_name: str = None) -> List[str]:
        """Get validation errors for configuration(s)"""
        if config_name:
            result = self.validation_results.get(config_name)
            return result.errors if result else []
        
        # Get all errors
        all_errors = []
        for config_name, result in self.validation_results.items():
            for error in result.errors:
                all_errors.append(f"{config_name}: {error}")
        return all_errors
    
    def get_validation_warnings(self, config_name: str = None) -> List[str]:
        """Get validation warnings for configuration(s)"""
        if config_name:
            result = self.validation_results.get(config_name)
            return result.warnings if result else []
        
        # Get all warnings
        all_warnings = []
        for config_name, result in self.validation_results.items():
            for warning in result.warnings:
                all_warnings.append(f"{config_name}: {warning}")
        return all_warnings
    
    def reload_configuration(self, config_name: str = None):
        """Reload specific configuration or all configurations"""
        if config_name:
            if config_name in self.config_files:
                filename = self.config_files[config_name]
                config_path = self.config_dir / filename
                
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        config_data = yaml.safe_load(f)
                        self.configs[config_name] = config_data
                        self.validation_results[config_name] = self._validate_configuration(config_name)
                        logger.info(f"Reloaded configuration: {config_name}")
                except Exception as e:
                    logger.error(f"Error reloading configuration {config_name}: {e}")
            else:
                logger.error(f"Unknown configuration name: {config_name}")
        else:
            # Reload all configurations
            self._load_all_configurations()
    
    def get_configuration_summary(self) -> Dict[str, Any]:
        """Get summary of all configurations"""
        summary = {
            'config_files': len(self.config_files),
            'loaded_configs': len(self.configs),
            'validation_status': {},
            'technology_count': 0,
            'mcp_server_count': 0,
            'change_type_count': 0
        }
        
        # Validation status
        for config_name, result in self.validation_results.items():
            summary['validation_status'][config_name] = {
                'valid': result.is_valid,
                'errors': len(result.errors),
                'warnings': len(result.warnings)
            }
        
        # Count technologies
        all_technologies = self.get_all_technologies()
        summary['technology_count'] = len(all_technologies)
        
        # Count MCP servers
        mcp_config = self.get_mcp_integration_config()
        servers = mcp_config.get('available_mcp_servers', {})
        summary['mcp_server_count'] = len(servers)
        
        # Count change types
        classification_rules = self.get_classification_rules()
        change_types = classification_rules.get('change_type_classification', {})
        summary['change_type_count'] = len(change_types)
        
        return summary
    
    def export_configuration(self, config_name: str, output_path: Path):
        """Export configuration to file"""
        if config_name not in self.configs:
            raise ValueError(f"Configuration {config_name} not found")
        
        config_data = self.configs[config_name]
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.dump(config_data, f, default_flow_style=False, indent=2)
            logger.info(f"Exported configuration {config_name} to {output_path}")
        except Exception as e:
            logger.error(f"Error exporting configuration {config_name}: {e}")
            raise
    
    def import_configuration(self, config_name: str, input_path: Path):
        """Import configuration from file"""
        if config_name not in self.config_files:
            raise ValueError(f"Unknown configuration name: {config_name}")
        
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
                self.configs[config_name] = config_data
                self.validation_results[config_name] = self._validate_configuration(config_name)
                logger.info(f"Imported configuration {config_name} from {input_path}")
        except Exception as e:
            logger.error(f"Error importing configuration {config_name}: {e}")
            raise
    
    def get_environment_config(self, environment: str = "production") -> Dict[str, Any]:
        """Get environment-specific configuration overrides"""
        # This would load environment-specific overrides
        # For now, return basic environment settings
        
        env_configs = {
            "development": {
                "logging_level": "DEBUG",
                "cache_ttl": 60,  # Shorter cache for development
                "request_timeout": 60,  # Longer timeout for debugging
                "retry_count": 2,  # Fewer retries for faster feedback
                "health_check_interval": 300  # 5 minutes
            },
            "staging": {
                "logging_level": "INFO",
                "cache_ttl": 300,  # 5 minutes
                "request_timeout": 30,
                "retry_count": 3,
                "health_check_interval": 180  # 3 minutes
            },
            "production": {
                "logging_level": "WARNING",
                "cache_ttl": 600,  # 10 minutes
                "request_timeout": 30,
                "retry_count": 3,
                "health_check_interval": 120  # 2 minutes
            }
        }
        
        return env_configs.get(environment, env_configs["production"])
    
    def __str__(self) -> str:
        """String representation of configuration manager"""
        summary = self.get_configuration_summary()
        return (f"ConfigManager("
                f"configs={summary['loaded_configs']}, "
                f"technologies={summary['technology_count']}, "
                f"servers={summary['mcp_server_count']}, "
                f"valid={all(status['valid'] for status in summary['validation_status'].values())})")
    
    def __repr__(self) -> str:
        """Detailed representation of configuration manager"""
        return self.__str__()