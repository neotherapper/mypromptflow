#!/usr/bin/env python3
"""
Knowledge Vault Integration Interface
AI Knowledge Lifecycle Orchestrator

This module provides a Python interface for interacting with Knowledge Vault schemas
and managing technology tracking, dependency mapping, knowledge updates, and change events.
"""

import os
import sys
import yaml
import json
import uuid
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

class DatabaseOperationError(Exception):
    """Custom exception for database operation errors"""
    pass

class TechnologyCategory(Enum):
    """Technology categories for classification"""
    FRONTEND_FRAMEWORK = "frontend_framework"
    BACKEND_FRAMEWORK = "backend_framework"
    DATABASE = "database"
    CI_CD = "ci_cd"
    CLOUD_PLATFORM = "cloud_platform"
    DEV_TOOL = "dev_tool"
    AI_ML = "ai_ml"
    SECURITY = "security"
    INFRASTRUCTURE = "infrastructure"
    OTHER = "other"

class ChangeClassification(Enum):
    """Change impact classifications"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFORMATIONAL = "informational"

class WorkflowStatus(Enum):
    """Update workflow status values"""
    DETECTED = "detected"
    ANALYSIS_PENDING = "analysis_pending"
    IMPACT_ASSESSED = "impact_assessed"
    APPROVAL_PENDING = "approval_pending"
    APPROVED = "approved"
    IN_PROGRESS = "in_progress"
    TESTING = "testing"
    COMPLETED = "completed"
    REJECTED = "rejected"
    POSTPONED = "postponed"

@dataclass
class TechnologyTracking:
    """Technology tracking data structure"""
    id: str
    technology_name: str
    category: str
    current_version: str
    version_pattern: str
    monitoring_priority: str
    description: Optional[str] = None
    release_frequency: Optional[str] = None
    change_volatility: Optional[str] = None
    official_urls: Optional[str] = None
    ecosystem_impact: Optional[str] = None
    first_tracked: Optional[str] = None
    last_updated: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for YAML serialization"""
        return {k: v for k, v in asdict(self).items() if v is not None}

@dataclass
class DependencyMapping:
    """Dependency mapping data structure"""
    id: str
    mapping_name: str
    ai_file_path: str
    ai_file_type: str
    technology_name: str
    technology_category: str
    dependency_type: str
    dependency_criticality: str
    update_priority: str
    validation_status: str
    usage_context: Optional[List[str]] = None
    version_constraint: Optional[str] = None
    breaking_change_impact: Optional[str] = None
    discovered_date: Optional[str] = None
    last_validated: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for YAML serialization"""
        return {k: v for k, v in asdict(self).items() if v is not None}

@dataclass
class KnowledgeUpdate:
    """Knowledge update data structure"""
    id: str
    update_title: str
    trigger_event: str
    affected_file_path: str
    affected_file_type: str
    update_description: str
    update_type: str
    update_scope: str
    workflow_status: str
    update_priority: str
    related_technology: Optional[str] = None
    approval_required: Optional[bool] = None
    implementation_approach: Optional[str] = None
    detected_date: Optional[str] = None
    scheduled_date: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for YAML serialization"""
        return {k: v for k, v in asdict(self).items() if v is not None}

@dataclass
class ChangeEvent:
    """Change event data structure"""
    id: str
    event_title: str
    technology_name: str
    technology_category: str
    change_type: str
    change_classification: str
    detection_source: str
    detection_method: str
    change_description: str
    processing_status: str
    previous_version: Optional[str] = None
    new_version: Optional[str] = None
    risk_level: Optional[str] = None
    source_url: Optional[str] = None
    detected_date: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for YAML serialization"""
        return {k: v for k, v in asdict(self).items() if v is not None}

class KnowledgeVaultIntegration:
    """Main interface for Knowledge Vault integration"""
    
    def __init__(self, base_path: str = None):
        """Initialize the integration interface"""
        self.base_path = Path(base_path or "/Users/georgiospilitsoglou/Developer/projects/mypromptflow")
        self.knowledge_vault_path = self.base_path / "knowledge-vault"
        self.schemas_path = self.knowledge_vault_path / "schemas"
        self.databases_path = self.knowledge_vault_path / "databases"
        
        # Database configurations
        self.databases = {
            'technology_tracking': {
                'schema_file': 'technology-tracking-schema.yaml',
                'database_path': self.databases_path / 'technology_tracking',
                'data_class': TechnologyTracking
            },
            'dependency_mapping': {
                'schema_file': 'dependency-mapping-schema.yaml',
                'database_path': self.databases_path / 'dependency_mapping',
                'data_class': DependencyMapping
            },
            'knowledge_updates': {
                'schema_file': 'knowledge-update-schema.yaml',
                'database_path': self.databases_path / 'knowledge_updates',
                'data_class': KnowledgeUpdate
            },
            'change_events': {
                'schema_file': 'change-event-schema.yaml',
                'database_path': self.databases_path / 'change_events',
                'data_class': ChangeEvent
            }
        }
        
        self._validate_setup()
    
    def _validate_setup(self):
        """Validate that required directories and schemas exist"""
        if not self.knowledge_vault_path.exists():
            raise DatabaseOperationError(f"Knowledge Vault path not found: {self.knowledge_vault_path}")
        
        if not self.schemas_path.exists():
            raise DatabaseOperationError(f"Schemas path not found: {self.schemas_path}")
        
        # Validate schema files exist
        for db_name, config in self.databases.items():
            schema_file = self.schemas_path / config['schema_file']
            if not schema_file.exists():
                raise DatabaseOperationError(f"Schema file not found: {schema_file}")
            
            # Ensure database directory exists
            config['database_path'].mkdir(parents=True, exist_ok=True)
            
            # Ensure subdirectories exist
            for subdir in ['items', 'relations', 'metadata', 'indexes', 'views']:
                (config['database_path'] / subdir).mkdir(exist_ok=True)
    
    def _generate_id(self) -> str:
        """Generate a unique UUID for database items"""
        return str(uuid.uuid4())
    
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        return datetime.now().isoformat()
    
    def _validate_item_data(self, database_name: str, item_data: Dict[str, Any]) -> bool:
        """Validate item data against schema requirements"""
        if database_name not in self.databases:
            raise ValidationError(f"Unknown database: {database_name}")
        
        # Load schema for validation
        schema_file = self.schemas_path / self.databases[database_name]['schema_file']
        with open(schema_file, 'r') as f:
            schema = yaml.safe_load(f)
        
        # Check required fields
        required_fields = schema.get('configuration', {}).get('validation', {}).get('required_fields', [])
        for field in required_fields:
            if field not in item_data or item_data[field] is None:
                raise ValidationError(f"Required field missing: {field}")
        
        return True
    
    def _save_item(self, database_name: str, item_data: Dict[str, Any]) -> str:
        """Save item to database"""
        # Ensure ID and timestamps first
        if 'id' not in item_data or not item_data['id']:
            item_data['id'] = self._generate_id()
        
        # Validate data after ID is set
        self._validate_item_data(database_name, item_data)
        
        # Set timestamps if not present
        current_time = self._get_timestamp()
        if 'created_date' in item_data and not item_data.get('created_date'):
            item_data['created_date'] = current_time
        if 'last_modified' in item_data and not item_data.get('last_modified'):
            item_data['last_modified'] = current_time
        
        # Save to file
        database_path = self.databases[database_name]['database_path']
        items_path = database_path / 'items'
        item_file = items_path / f"{item_data['id']}.yaml"
        
        with open(item_file, 'w') as f:
            yaml.dump(item_data, f, default_flow_style=False, sort_keys=False)
        
        return item_data['id']
    
    def _load_item(self, database_name: str, item_id: str) -> Optional[Dict[str, Any]]:
        """Load item from database"""
        if database_name not in self.databases:
            raise ValidationError(f"Unknown database: {database_name}")
        
        database_path = self.databases[database_name]['database_path']
        items_path = database_path / 'items'
        item_file = items_path / f"{item_id}.yaml"
        
        if not item_file.exists():
            return None
        
        with open(item_file, 'r') as f:
            return yaml.safe_load(f)
    
    def _query_items(self, database_name: str, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Query items from database with optional filters"""
        if database_name not in self.databases:
            raise ValidationError(f"Unknown database: {database_name}")
        
        database_path = self.databases[database_name]['database_path']
        items_path = database_path / 'items'
        
        if not items_path.exists():
            return []
        
        items = []
        for item_file in items_path.glob('*.yaml'):
            with open(item_file, 'r') as f:
                item_data = yaml.safe_load(f)
                
            # Apply filters if provided
            if filters:
                match = True
                for key, value in filters.items():
                    if key not in item_data or item_data[key] != value:
                        match = False
                        break
                if not match:
                    continue
            
            items.append(item_data)
        
        return items
    
    # Technology Tracking Operations
    def create_technology_tracking(self, technology_data: Union[TechnologyTracking, Dict[str, Any]]) -> str:
        """Create a new technology tracking entry"""
        if isinstance(technology_data, TechnologyTracking):
            data = technology_data.to_dict()
        else:
            data = technology_data.copy()
        
        # Set default timestamps
        if not data.get('first_tracked'):
            data['first_tracked'] = self._get_timestamp()
        if not data.get('last_updated'):
            data['last_updated'] = self._get_timestamp()
        
        return self._save_item('technology_tracking', data)
    
    def get_technology_tracking(self, technology_id: str) -> Optional[Dict[str, Any]]:
        """Get technology tracking entry by ID"""
        return self._load_item('technology_tracking', technology_id)
    
    def query_technologies(self, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Query technology tracking entries"""
        return self._query_items('technology_tracking', filters)
    
    def get_technologies_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get all technologies in a specific category"""
        return self.query_technologies({'category': category})
    
    def get_critical_technologies(self) -> List[Dict[str, Any]]:
        """Get technologies with critical monitoring priority"""
        return self.query_technologies({'monitoring_priority': 'critical'})
    
    # Dependency Mapping Operations
    def create_dependency_mapping(self, dependency_data: Union[DependencyMapping, Dict[str, Any]]) -> str:
        """Create a new dependency mapping entry"""
        if isinstance(dependency_data, DependencyMapping):
            data = dependency_data.to_dict()
        else:
            data = dependency_data.copy()
        
        # Set default timestamps
        if not data.get('discovered_date'):
            data['discovered_date'] = self._get_timestamp()
        
        return self._save_item('dependency_mapping', data)
    
    def get_dependency_mapping(self, dependency_id: str) -> Optional[Dict[str, Any]]:
        """Get dependency mapping entry by ID"""
        return self._load_item('dependency_mapping', dependency_id)
    
    def query_dependencies(self, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Query dependency mapping entries"""
        return self._query_items('dependency_mapping', filters)
    
    def get_dependencies_by_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Get all dependencies for a specific file"""
        return self.query_dependencies({'ai_file_path': file_path})
    
    def get_dependencies_by_technology(self, technology_name: str) -> List[Dict[str, Any]]:
        """Get all dependencies for a specific technology"""
        return self.query_dependencies({'technology_name': technology_name})
    
    def get_critical_dependencies(self) -> List[Dict[str, Any]]:
        """Get dependencies with essential or important criticality"""
        critical_deps = self.query_dependencies({'dependency_criticality': 'essential'})
        important_deps = self.query_dependencies({'dependency_criticality': 'important'})
        return critical_deps + important_deps
    
    # Knowledge Update Operations
    def create_knowledge_update(self, update_data: Union[KnowledgeUpdate, Dict[str, Any]]) -> str:
        """Create a new knowledge update entry"""
        if isinstance(update_data, KnowledgeUpdate):
            data = update_data.to_dict()
        else:
            data = update_data.copy()
        
        # Set default timestamps
        if not data.get('detected_date'):
            data['detected_date'] = self._get_timestamp()
        
        return self._save_item('knowledge_updates', data)
    
    def get_knowledge_update(self, update_id: str) -> Optional[Dict[str, Any]]:
        """Get knowledge update entry by ID"""
        return self._load_item('knowledge_updates', update_id)
    
    def query_updates(self, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Query knowledge update entries"""
        return self._query_items('knowledge_updates', filters)
    
    def get_pending_updates(self) -> List[Dict[str, Any]]:
        """Get updates pending approval or implementation"""
        pending_statuses = ['detected', 'analysis_pending', 'impact_assessed', 'approval_pending', 'approved']
        pending_updates = []
        for status in pending_statuses:
            pending_updates.extend(self.query_updates({'workflow_status': status}))
        return pending_updates
    
    def get_critical_updates(self) -> List[Dict[str, Any]]:
        """Get updates with critical priority"""
        return self.query_updates({'update_priority': 'critical'})
    
    def update_workflow_status(self, update_id: str, new_status: str) -> bool:
        """Update the workflow status of a knowledge update"""
        update_data = self.get_knowledge_update(update_id)
        if not update_data:
            return False
        
        update_data['workflow_status'] = new_status
        update_data['last_modified'] = self._get_timestamp()
        
        # Set completion date if completed
        if new_status == 'completed':
            update_data['completed_date'] = self._get_timestamp()
        
        self._save_item('knowledge_updates', update_data)
        return True
    
    # Change Event Operations
    def create_change_event(self, event_data: Union[ChangeEvent, Dict[str, Any]]) -> str:
        """Create a new change event entry"""
        if isinstance(event_data, ChangeEvent):
            data = event_data.to_dict()
        else:
            data = event_data.copy()
        
        # Set default timestamps
        if not data.get('detected_date'):
            data['detected_date'] = self._get_timestamp()
        
        return self._save_item('change_events', data)
    
    def get_change_event(self, event_id: str) -> Optional[Dict[str, Any]]:
        """Get change event entry by ID"""
        return self._load_item('change_events', event_id)
    
    def query_change_events(self, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Query change event entries"""
        return self._query_items('change_events', filters)
    
    def get_critical_changes(self) -> List[Dict[str, Any]]:
        """Get change events with critical classification"""
        return self.query_change_events({'change_classification': 'critical'})
    
    def get_breaking_changes(self) -> List[Dict[str, Any]]:
        """Get breaking change events"""
        return self.query_change_events({'change_type': 'breaking_change'})
    
    def get_recent_changes(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get change events from the last N days"""
        # This would need more sophisticated date filtering in a real implementation
        return self.query_change_events()
    
    # Impact Analysis Operations
    def analyze_technology_impact(self, technology_name: str) -> Dict[str, Any]:
        """Analyze the impact of a technology across the system"""
        # Get technology tracking info
        tech_entries = self.query_technologies({'technology_name': technology_name})
        
        # Get dependencies
        dependencies = self.get_dependencies_by_technology(technology_name)
        
        # Get recent changes
        changes = self.query_change_events({'technology_name': technology_name})
        
        # Get related updates
        updates = self.query_updates({'related_technology': technology_name})
        
        return {
            'technology_name': technology_name,
            'technology_entries': tech_entries,
            'affected_files': len(dependencies),
            'dependencies': dependencies,
            'recent_changes': len(changes),
            'change_events': changes,
            'pending_updates': len([u for u in updates if u.get('workflow_status') not in ['completed', 'rejected']]),
            'knowledge_updates': updates,
            'impact_summary': {
                'total_affected_files': len(dependencies),
                'critical_dependencies': len([d for d in dependencies if d.get('dependency_criticality') == 'essential']),
                'high_impact_changes': len([c for c in changes if c.get('change_classification') in ['critical', 'high']]),
                'pending_critical_updates': len([u for u in updates if u.get('update_priority') == 'critical' and u.get('workflow_status') not in ['completed', 'rejected']])
            }
        }
    
    def get_system_health_summary(self) -> Dict[str, Any]:
        """Get overall system health summary"""
        # Count items in each database
        tech_count = len(self.query_technologies())
        dep_count = len(self.query_dependencies())
        update_count = len(self.query_updates())
        change_count = len(self.query_change_events())
        
        # Get critical items
        critical_tech = len(self.get_critical_technologies())
        critical_deps = len(self.get_critical_dependencies())
        critical_updates = len(self.get_critical_updates())
        critical_changes = len(self.get_critical_changes())
        
        # Get pending items
        pending_updates = len(self.get_pending_updates())
        
        return {
            'database_counts': {
                'technology_tracking': tech_count,
                'dependency_mapping': dep_count,
                'knowledge_updates': update_count,
                'change_events': change_count
            },
            'critical_items': {
                'technologies': critical_tech,
                'dependencies': critical_deps,
                'updates': critical_updates,
                'changes': critical_changes
            },
            'pending_work': {
                'updates_pending': pending_updates
            },
            'health_indicators': {
                'critical_attention_needed': critical_updates > 0 or critical_changes > 0,
                'pending_work_load': 'high' if pending_updates > 10 else 'moderate' if pending_updates > 5 else 'low'
            }
        }
    
    # Relationship Management
    def create_relationship(self, from_database: str, from_id: str, to_database: str, to_id: str) -> bool:
        """Create a relationship between items in different databases"""
        # This would implement the relationship creation logic
        # For now, we'll just return True as a placeholder
        return True
    
    def get_related_items(self, database_name: str, item_id: str) -> Dict[str, List[Dict[str, Any]]]:
        """Get all items related to a specific item"""
        # This would implement relationship traversal
        # For now, we'll return an empty structure
        return {
            'technology_tracking': [],
            'dependency_mapping': [],
            'knowledge_updates': [],
            'change_events': []
        }


# Utility functions
def create_sample_data(integration: KnowledgeVaultIntegration):
    """Create sample data for testing"""
    # Sample technology tracking
    tech_data = TechnologyTracking(
        id="",  # Will be generated
        technology_name="React",
        category="frontend_framework",
        current_version="18.2.0",
        version_pattern="semantic",
        monitoring_priority="high",
        description="JavaScript library for building user interfaces",
        release_frequency="quarterly",
        change_volatility="moderate"
    )
    tech_id = integration.create_technology_tracking(tech_data)
    
    # Sample dependency mapping
    dep_data = DependencyMapping(
        id="",  # Will be generated
        mapping_name="React dependency in main CLAUDE.md",
        ai_file_path="/path/to/CLAUDE.md",
        ai_file_type="claude_md",
        technology_name="React",
        technology_category="frontend_framework",
        dependency_type="direct_usage",
        dependency_criticality="important",
        update_priority="high",
        validation_status="validated"
    )
    dep_id = integration.create_dependency_mapping(dep_data)
    
    # Sample knowledge update
    update_data = KnowledgeUpdate(
        id="",  # Will be generated
        update_title="Update React version references",
        trigger_event="technology_change",
        affected_file_path="/path/to/CLAUDE.md",
        affected_file_type="claude_md",
        update_description="Update React version from 18.1.0 to 18.2.0",
        update_type="version_update",
        update_scope="minor",
        workflow_status="detected",
        update_priority="medium",
        related_technology="React"
    )
    update_id = integration.create_knowledge_update(update_data)
    
    # Sample change event
    change_data = ChangeEvent(
        id="",  # Will be generated
        event_title="React 18.2.0 Released",
        technology_name="React",
        technology_category="frontend_framework",
        change_type="new_feature",
        change_classification="medium",
        detection_source="github_releases",
        detection_method="automated_monitoring",
        change_description="React 18.2.0 includes new features and bug fixes",
        processing_status="detected",
        previous_version="18.1.0",
        new_version="18.2.0"
    )
    change_id = integration.create_change_event(change_data)
    
    return {
        'technology_id': tech_id,
        'dependency_id': dep_id,
        'update_id': update_id,
        'change_id': change_id
    }


def main():
    """Main function for testing"""
    try:
        # Initialize integration
        integration = KnowledgeVaultIntegration()
        
        print("Knowledge Vault Integration Interface")
        print("=" * 40)
        
        # Test basic functionality
        print("Testing basic functionality...")
        
        # Create sample data
        sample_ids = create_sample_data(integration)
        print(f"Created sample data: {sample_ids}")
        
        # Test queries
        print("\nQuerying data...")
        
        technologies = integration.query_technologies()
        print(f"Total technologies tracked: {len(technologies)}")
        
        dependencies = integration.query_dependencies()
        print(f"Total dependencies mapped: {len(dependencies)}")
        
        updates = integration.query_updates()
        print(f"Total knowledge updates: {len(updates)}")
        
        changes = integration.query_change_events()
        print(f"Total change events: {len(changes)}")
        
        # Test impact analysis
        print("\nTesting impact analysis...")
        impact = integration.analyze_technology_impact("React")
        print(f"React impact analysis: {impact['impact_summary']}")
        
        # Test system health
        print("\nSystem health summary:")
        health = integration.get_system_health_summary()
        print(json.dumps(health, indent=2))
        
        print("\nIntegration test completed successfully!")
        
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())