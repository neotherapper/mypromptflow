"""
AI Knowledge Lifecycle Orchestrator - Validation Integration Package

This package provides seamless integration between the AI Knowledge Lifecycle Orchestrator's
update pipeline and the AI Agent Instruction Design Excellence framework for quality-preserving
automated instruction updates.

Key Components:
- FrameworkConnector: Main interface to AI Agent Instruction Design Excellence framework
- QualityMonitor: Real-time quality monitoring and alerting system
- ValidationOrchestrator: Comprehensive validation workflow coordination
- RollbackManager: Quality-based rollback system with automatic recovery

Example Usage:
    from validation_integration import (
        AIInstructionFrameworkConnector,
        QualityMonitor, 
        ValidationOrchestrator,
        RollbackManager
    )
    
    # Initialize components
    framework_connector = AIInstructionFrameworkConnector(framework_config)
    quality_monitor = QualityMonitor(framework_connector, monitor_config)
    rollback_manager = RollbackManager(rollback_config)
    orchestrator = ValidationOrchestrator(
        framework_connector, quality_monitor, rollback_manager, orchestrator_config
    )
    
    # Execute validation workflow
    results = await orchestrator.execute_pre_update_validation(file_paths)
"""

__version__ = "1.0.0"
__author__ = "AI Knowledge Lifecycle Orchestrator"

# Import main classes for easy access
from .framework_connector import (
    AIInstructionFrameworkConnector,
    FrameworkValidationResult,
    ValidationType,
    ValidationIssue,
    ValidationSeverity
)

from .quality_monitor import (
    QualityMonitor,
    QualitySnapshot,
    QualityAlert,
    QualityTrend,
    MonitoringMode
)

from .validation_orchestrator import (
    ValidationOrchestrator,
    ValidationWorkflowResult,
    ValidationPhase,
    ValidationStatus
)

from .rollback_manager import (
    RollbackManager,
    RollbackDecision,
    RollbackExecution,
    RollbackReason,
    RollbackStatus
)

# Package-level configuration
INTEGRATION_CONFIG_PATH = "integration_config.yaml"
DEFAULT_FRAMEWORK_PATH = "/Users/georgiospilitsoglou/Developer/projects/mypromptflow/projects/ai-agent-instruction-design-excellence"
DEFAULT_VALIDATORS_PATH = "/Users/georgiospilitsoglou/Developer/projects/mypromptflow/meta/validation/validators/ai-instruction"

__all__ = [
    # Framework Connector
    "AIInstructionFrameworkConnector",
    "FrameworkValidationResult", 
    "ValidationType",
    "ValidationIssue",
    "ValidationSeverity",
    
    # Quality Monitor
    "QualityMonitor",
    "QualitySnapshot",
    "QualityAlert", 
    "QualityTrend",
    "MonitoringMode",
    
    # Validation Orchestrator
    "ValidationOrchestrator",
    "ValidationWorkflowResult",
    "ValidationPhase",
    "ValidationStatus",
    
    # Rollback Manager
    "RollbackManager",
    "RollbackDecision",
    "RollbackExecution",
    "RollbackReason",
    "RollbackStatus",
    
    # Configuration
    "INTEGRATION_CONFIG_PATH",
    "DEFAULT_FRAMEWORK_PATH",
    "DEFAULT_VALIDATORS_PATH"
]


def get_default_config():
    """Get default configuration for validation integration"""
    return {
        'framework_connector': {
            'framework_base_path': DEFAULT_FRAMEWORK_PATH,
            'validators_path': DEFAULT_VALIDATORS_PATH,
            'quality_threshold': 75.0,
            'validation_timeout': 60,
            'enable_parallel_validation': True
        },
        'quality_monitor': {
            'critical_threshold': 50.0,
            'warning_threshold': 65.0,
            'monitoring_interval': 30,
            'trend_analysis_window': 5,
            'max_quality_decline': 10.0
        },
        'rollback_manager': {
            'quality_decline_threshold': 10.0,
            'critical_issues_threshold': 1,
            'confidence_threshold': 0.7,
            'backup_retention_days': 30
        },
        'validation_orchestrator': {
            'enable_quality_monitoring': True,
            'enable_automatic_rollback': True,
            'quality_preservation_threshold': 5.0,
            'validation_timeout': 120
        }
    }


async def create_integrated_validation_system(config=None):
    """
    Create a complete integrated validation system with all components
    
    Args:
        config: Optional configuration dictionary. Uses defaults if not provided.
        
    Returns:
        Tuple of (framework_connector, quality_monitor, rollback_manager, orchestrator)
    """
    if config is None:
        config = get_default_config()
    
    # Initialize framework connector
    framework_connector = AIInstructionFrameworkConnector(
        config.get('framework_connector', {})
    )
    
    # Initialize quality monitor
    quality_monitor = QualityMonitor(
        framework_connector, 
        config.get('quality_monitor', {})
    )
    
    # Initialize rollback manager
    rollback_manager = RollbackManager(
        config.get('rollback_manager', {})
    )
    
    # Initialize validation orchestrator
    validation_orchestrator = ValidationOrchestrator(
        framework_connector,
        quality_monitor, 
        rollback_manager,
        config.get('validation_orchestrator', {})
    )
    
    return framework_connector, quality_monitor, rollback_manager, validation_orchestrator


def get_integration_info():
    """Get information about the validation integration package"""
    return {
        'package_name': 'validation-integration',
        'version': __version__,
        'description': 'AI Agent Instruction Design Excellence framework integration for quality-preserving updates',
        'components': [
            'AIInstructionFrameworkConnector - Framework validation interface',
            'QualityMonitor - Real-time quality monitoring and alerting',
            'ValidationOrchestrator - Comprehensive validation workflow coordination', 
            'RollbackManager - Quality-based rollback system'
        ],
        'capabilities': [
            'Pre-update quality validation',
            'Post-update quality verification',
            'Real-time quality monitoring',
            'Automatic rollback on quality degradation',
            'Batch validation processing',
            'Quality trend analysis',
            'Framework compliance checking',
            'Comprehensive reporting'
        ],
        'integration_points': [
            'Update pipeline integration',
            'AI Agent Instruction Design Excellence framework',
            'Quality preservation systems',
            'Backup and recovery systems'
        ]
    }