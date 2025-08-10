"""
Universal Topic Intelligence System - Core Components
"""

from .universal_source_monitor import (
    UniversalSourceMonitor,
    SourceType,
    ContentPriority,
    SourceMetadata,
    ContentItem,
    MonitoringResult,
    SourceMonitorFactory
)

from .content_prioritizer import (
    UniversalContentPrioritizer,
    PriorityFactors,
    PriorityResult,
    PriorityStrategy,
    DefaultPriorityStrategy,
    NewsPriorityStrategy,
    TechnicalContentStrategy,
    SocialSignalsStrategy
)

__all__ = [
    # Source Monitor
    'UniversalSourceMonitor',
    'SourceType',
    'ContentPriority',
    'SourceMetadata',
    'ContentItem',
    'MonitoringResult',
    'SourceMonitorFactory',
    # Content Prioritizer
    'UniversalContentPrioritizer',
    'PriorityFactors',
    'PriorityResult',
    'PriorityStrategy',
    'DefaultPriorityStrategy',
    'NewsPriorityStrategy',
    'TechnicalContentStrategy',
    'SocialSignalsStrategy'
]