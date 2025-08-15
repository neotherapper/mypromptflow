"""
Universal Topic Intelligence System - 4-Level Agent Hierarchy

Level 1: Queen Agent - Universal orchestrator
Level 2: Architect Agents - Strategy specialists  
Level 3: Specialist Agents - Content processors
Level 4: Worker Agents - Task executors
"""

from .queen_agent import QueenAgent, ResourcePriority, TopicStatus
from .architect_agents import (
    ArchitectAgent,
    OfficialSourceArchitect,
    CommunityIntelligenceArchitect,
    AggregatorIntelligenceArchitect,
    ArchitectCoordinator,
    MonitoringStrategy
)
from .specialist_agents import (
    SpecialistAgent,
    TechnicalContentSpecialist,
    MarketImpactSpecialist,
    SentimentTrendSpecialist,
    QualityValidationSpecialist,
    SpecialistCoordinator,
    ContentAnalysis
)
from .worker_agents import (
    WorkerAgent,
    FetchWorker,
    GitHubWorker,
    YouTubeWorker,
    SocialMediaWorker,
    WorkerPool,
    WorkerTask,
    WorkerResult
)

__all__ = [
    # Queen
    'QueenAgent',
    'ResourcePriority',
    'TopicStatus',
    # Architects
    'ArchitectAgent',
    'OfficialSourceArchitect',
    'CommunityIntelligenceArchitect',
    'AggregatorIntelligenceArchitect',
    'ArchitectCoordinator',
    'MonitoringStrategy',
    # Specialists
    'SpecialistAgent',
    'TechnicalContentSpecialist',
    'MarketImpactSpecialist',
    'SentimentTrendSpecialist',
    'QualityValidationSpecialist',
    'SpecialistCoordinator',
    'ContentAnalysis',
    # Workers
    'WorkerAgent',
    'FetchWorker',
    'GitHubWorker',
    'YouTubeWorker',
    'SocialMediaWorker',
    'WorkerPool',
    'WorkerTask',
    'WorkerResult'
]