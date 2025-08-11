"""
Universal Topic Intelligence System - Agent Framework
4-Level hierarchy: Queen → Architect → Specialist → Worker
"""

from .queen_agent import QueenAgent, TopicOrchestrationResult
from .architect_agents import (
    OfficialSourceArchitect,
    CommunityIntelligenceArchitect, 
    TrendDetectionArchitect,
    ArchitectCoordinator
)

__all__ = [
    'QueenAgent',
    'TopicOrchestrationResult',
    'OfficialSourceArchitect',
    'CommunityIntelligenceArchitect',
    'TrendDetectionArchitect',
    'ArchitectCoordinator'
]