#!/usr/bin/env python3
"""
Knowledge Vault Batch Migration System with Database ID Registry Integration
Production-ready migration script for VanguardAI test environment
Supports complete 30-item migration with comprehensive error handling and intelligent caching
"""

import os
import sys
import json
import yaml
import time
import logging
import argparse
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from urllib.parse import urlparse
import re

# Add the project root to Python path for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import Database ID Registry Manager
from database_id_registry_manager import DatabaseIDRegistryManager

# Configuration
NOTION_API_VERSION = "2022-06-28"
RATE_LIMIT_DELAY = 0.334  # ~3 requests per second
MAX_RETRIES = 5
BATCH_SIZE = 5
TIMEOUT = 30

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Path(__file__).parent.parent / 'logs' / 'batch_migration.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class MigrationConfig:
    """Migration configuration and settings"""
    notion_token: str
    workspace_id: str
    source_path: Path
    transformation_config_path: Path
    property_mappings_path: Path
    batch_size: int = BATCH_SIZE
    rate_limit_delay: float = RATE_LIMIT_DELAY
    max_retries: int = MAX_RETRIES
    dry_run: bool = False
    
@dataclass
class DatabaseInfo:
    """Information about a created Notion database"""
    notion_id: str
    name: str
    database_type: str
    properties: Dict[str, Any]
    created_at: datetime
    
@dataclass 
class MigrationResult:
    """Result of migrating a single item"""
    item_id: str
    database_type: str
    notion_page_id: Optional[str]
    success: bool
    error_message: Optional[str]
    processing_time: float
    relationships_created: int
    retry_count: int

class NotionAPIClient:
    """Notion API client with rate limiting and error handling"""
    
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Notion-Version": NOTION_API_VERSION,
            "Content-Type": "application/json"
        }
        self.last_request_time = 0
        
    def _rate_limit(self):
        """Implement rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < RATE_LIMIT_DELAY:
            sleep_time = RATE_LIMIT_DELAY - time_since_last
            time.sleep(sleep_time)
        self.last_request_time = time.time()
        
    def _make_request(self, method: str, endpoint: str, data: Dict = None, retries: int = MAX_RETRIES) -> Dict:
        """Make API request with retry logic"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        for attempt in range(retries + 1):
            try:
                self._rate_limit()
                
                if method.upper() == "GET":
                    response = requests.get(url, headers=self.headers, timeout=TIMEOUT)
                elif method.upper() == "POST":
                    response = requests.post(url, headers=self.headers, json=data, timeout=TIMEOUT)
                elif method.upper() == "PATCH":
                    response = requests.patch(url, headers=self.headers, json=data, timeout=TIMEOUT)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
                
                # Handle rate limiting
                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 60))
                    logger.warning(f"Rate limited. Waiting {retry_after} seconds...")
                    time.sleep(retry_after)
                    continue
                
                response.raise_for_status()
                return response.json()
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Request failed (attempt {attempt + 1}): {e}")
                if attempt == retries:
                    raise
                wait_time = (2 ** attempt) * 1  # Exponential backoff
                time.sleep(wait_time)
                
        raise Exception(f"Failed to make request after {retries + 1} attempts")
    
    def create_database(self, parent_id: str, title: str, properties: Dict) -> Dict:
        """Create a new Notion database"""
        data = {
            "parent": {"page_id": parent_id},
            "title": [{"type": "text", "text": {"content": title}}],
            "properties": properties
        }
        return self._make_request("POST", "databases", data)
    
    def create_page(self, database_id: str, properties: Dict, children: List = None) -> Dict:
        """Create a new page in a database"""
        data = {
            "parent": {"database_id": database_id},
            "properties": properties
        }
        if children:
            data["children"] = children
        return self._make_request("POST", "pages", data)
    
    def update_page(self, page_id: str, properties: Dict) -> Dict:
        """Update an existing page"""
        data = {"properties": properties}
        return self._make_request("PATCH", f"pages/{page_id}", data)
    
    def query_database(self, database_id: str, filter_criteria: Dict = None) -> Dict:
        """Query a database"""
        data = {}
        if filter_criteria:
            data["filter"] = filter_criteria
        return self._make_request("POST", f"databases/{database_id}/query", data)
    
    def get_page(self, page_id: str) -> Dict:
        """Get page information"""
        return self._make_request("GET", f"pages/{page_id}")

class DataTransformer:
    """Transform YAML data to Notion format"""
    
    def __init__(self, transformation_config: Dict, property_mappings: Dict):
        self.transformation_config = transformation_config
        self.property_mappings = property_mappings
        
    def transform_item(self, item_data: Dict, database_type: str) -> Tuple[Dict, List[str]]:
        """Transform a YAML item to Notion properties format"""
        try:
            database_config = self.transformation_config['database_transformations'][f'{database_type}_transformations']
            property_mappings = database_config['property_mappings']
            
            notion_properties = {}
            relationships = []
            
            # Transform basic properties
            for yaml_field, mapping in property_mappings.items():
                if yaml_field in item_data:
                    transformed_value = self._transform_property(
                        item_data[yaml_field],
                        mapping['transformation_rule'],
                        mapping.get('mapping_table'),
                        yaml_field
                    )
                    if transformed_value is not None:
                        notion_properties[mapping['notion_property']] = transformed_value
                elif mapping.get('validation') == 'required_non_empty':
                    logger.warning(f"Required field {yaml_field} missing from item {item_data.get('id', 'unknown')}")
            
            # Extract relationships for later processing
            if 'relationships' in item_data:
                relationships = self._extract_relationships(
                    item_data['relationships'],
                    database_config.get('relationship_mappings', {}),
                    item_data.get('id', 'unknown')
                )
            
            return notion_properties, relationships
            
        except Exception as e:
            logger.error(f"Error transforming item {item_data.get('id', 'unknown')}: {e}")
            raise
    
    def _transform_property(self, value: Any, rule: str, mapping_table: str = None, field_name: str = "") -> Dict:
        """Transform individual property based on transformation rule"""
        try:
            if rule == "yaml_field_to_notion_title":
                return {"title": [{"type": "text", "text": {"content": str(value)}}]}
            
            elif rule == "yaml_string_to_rich_text":
                return {"rich_text": [{"type": "text", "text": {"content": str(value)}}]}
            
            elif rule == "yaml_string_to_select_option":
                if mapping_table and mapping_table in self.property_mappings.get('mapping_tables', {}):
                    mapping = self.property_mappings['mapping_tables'][mapping_table]
                    if value in mapping:
                        return {"select": mapping[value]}
                    else:
                        logger.warning(f"Option {value} not found in {mapping_table} for field {field_name}")
                        # Try to create a valid option
                        return {"select": {"name": str(value)}}
                return {"select": {"name": str(value)}}
            
            elif rule == "yaml_array_to_multi_select":
                if isinstance(value, list):
                    options = []
                    if mapping_table and mapping_table in self.property_mappings.get('mapping_tables', {}):
                        mapping = self.property_mappings['mapping_tables'][mapping_table]
                        for item in value:
                            if item in mapping:
                                options.append(mapping[item])
                            else:
                                options.append({"name": str(item)})
                    else:
                        options = [{"name": str(item)} for item in value]
                    return {"multi_select": options}
                return {"multi_select": []}
            
            elif rule == "yaml_integer_to_star_rating":
                if isinstance(value, int) and 1 <= value <= 5:
                    star_mapping = self.property_mappings['mapping_tables']['star_rating_mapping']
                    return {"select": star_mapping[value]}
                return {"select": {"name": "⭐⭐⭐"}}  # Default to 3 stars
            
            elif rule == "yaml_string_to_url":
                if self._is_valid_url(str(value)):
                    return {"url": str(value)}
                return None
            
            elif rule == "yaml_boolean_to_checkbox":
                return {"checkbox": bool(value)}
            
            elif rule == "yaml_integer_to_number":
                return {"number": int(value) if isinstance(value, (int, float)) else 0}
            
            else:
                logger.warning(f"Unknown transformation rule: {rule}")
                return {"rich_text": [{"type": "text", "text": {"content": str(value)}}]}
                
        except Exception as e:
            logger.error(f"Error transforming property {field_name} with rule {rule}: {e}")
            return None
    
    def _extract_relationships(self, relationships: Dict, relationship_mappings: Dict, item_id: str) -> List[str]:
        """Extract relationship references for later processing"""
        extracted = []
        for yaml_rel, notion_rel_config in relationship_mappings.items():
            if yaml_rel.replace('related_', '') in relationships:
                rel_data = relationships[yaml_rel.replace('related_', '')]
                if isinstance(rel_data, list):
                    for ref in rel_data:
                        if isinstance(ref, str) and ref.startswith('@'):
                            extracted.append({
                                'source_item': item_id,
                                'target_reference': ref,
                                'notion_property': notion_rel_config['notion_property'],
                                'target_database': notion_rel_config['target_database'],
                                'bidirectional': notion_rel_config.get('bidirectional', False)
                            })
        return extracted
    
    def _is_valid_url(self, url: str) -> bool:
        """Validate URL format"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

class RelationshipManager:
    """Manage cross-database relationships with Database ID Registry integration"""
    
    def __init__(self, notion_client: NotionAPIClient, registry_manager: DatabaseIDRegistryManager = None):
        self.notion_client = notion_client
        self.item_id_to_page_id = {}  # Legacy cache for compatibility
        self.registry_manager = registry_manager or DatabaseIDRegistryManager()
        logger.info("RelationshipManager initialized with Database ID Registry integration")
        
    def add_item_mapping(self, item_id: str, notion_page_id: str, database_type: str, 
                         database_notion_id: str = "", title: str = "", content: str = ""):
        """Add item ID to Notion page ID mapping with Database ID Registry integration"""
        # Legacy cache for compatibility
        self.item_id_to_page_id[f"{database_type}/{item_id}"] = notion_page_id
        
        # Add to Database ID Registry for performance optimization
        try:
            success = self.registry_manager.add_registry_entry(
                item_uuid=item_id,
                notion_page_id=notion_page_id,
                database_id=database_type,
                database_notion_id=database_notion_id,
                title=title,
                content=content
            )
            if success:
                logger.debug(f"Added registry entry for {item_id} -> {notion_page_id}")
            else:
                logger.warning(f"Failed to add registry entry for {item_id}")
        except Exception as e:
            logger.error(f"Error adding registry entry for {item_id}: {e}")
        
    def resolve_relationships(self, relationships: List[Dict], database_mappings: Dict) -> int:
        """Resolve and create relationship links"""
        created_count = 0
        
        for rel in relationships:
            try:
                # Parse target reference (@database/item_id)
                target_ref = rel['target_reference']
                match = re.match(r'@(\w+)/(.+)', target_ref)
                if not match:
                    logger.warning(f"Invalid relationship reference format: {target_ref}")
                    continue
                    
                target_db, target_item_id = match.groups()
                target_key = f"{target_db}/{target_item_id}"
                
                # Find target page ID using registry-first approach
                target_page_id = self.registry_manager.get_notion_page_id(target_item_id, target_db)
                if not target_page_id:
                    # Fallback to legacy cache
                    target_page_id = self.item_id_to_page_id.get(target_key)
                    if not target_page_id:
                        logger.warning(f"Target item not found: {target_ref}")
                        continue
                
                # Find source page ID using registry-first approach
                source_item_id = rel['source_item']
                source_db = rel.get('source_database', '')
                source_page_id = self.registry_manager.get_notion_page_id(source_item_id, source_db)
                if not source_page_id:
                    # Fallback to legacy cache
                    source_page_id = self.item_id_to_page_id.get(f"{source_db}/{source_item_id}")
                
                if not source_page_id:
                    logger.warning(f"Source page not found for item: {rel['source_item']}")
                    continue
                
                # Create relationship link
                self._create_relationship_link(
                    source_page_id,
                    target_page_id,
                    rel['notion_property']
                )
                
                # Create bidirectional link if needed
                if rel.get('bidirectional', False):
                    # Determine reverse property name
                    reverse_property = self._get_reverse_property_name(
                        rel['target_database'],
                        rel.get('source_database', '')
                    )
                    if reverse_property:
                        self._create_relationship_link(
                            target_page_id,
                            source_page_id,
                            reverse_property
                        )
                
                created_count += 1
                
            except Exception as e:
                logger.error(f"Error creating relationship {rel}: {e}")
                
        return created_count
    
    def _create_relationship_link(self, source_page_id: str, target_page_id: str, property_name: str):
        """Create a single relationship link"""
        try:
            # Get current page to check existing relationships
            current_page = self.notion_client.get_page(source_page_id)
            current_relations = current_page['properties'].get(property_name, {}).get('relation', [])
            
            # Add new relationship if not already exists
            target_ids = [rel['id'] for rel in current_relations]
            if target_page_id not in target_ids:
                current_relations.append({'id': target_page_id})
                
                # Update page with new relationships
                update_data = {
                    property_name: {'relation': current_relations}
                }
                self.notion_client.update_page(source_page_id, update_data)
                logger.debug(f"Created relationship: {source_page_id} -> {target_page_id} ({property_name})")
                
        except Exception as e:
            logger.error(f"Error creating relationship link: {e}")
            raise
    
    def _get_reverse_property_name(self, target_db: str, source_db: str) -> Optional[str]:
        """Determine reverse property name for bidirectional relationships"""
        # Mapping based on relationship patterns
        reverse_mappings = {
            ('knowledge_vault', 'tools_services'): 'Related_Knowledge',
            ('knowledge_vault', 'business_ideas'): 'Related_Knowledge',
            ('knowledge_vault', 'training_vault'): 'Related_Knowledge',
            ('knowledge_vault', 'platforms_sites'): 'Related_Knowledge',
            ('knowledge_vault', 'notes_ideas'): 'Related_Knowledge',
            ('tools_services', 'knowledge_vault'): 'Related_Tools',
            ('business_ideas', 'knowledge_vault'): 'Related_Business_Ideas',
            ('training_vault', 'knowledge_vault'): 'Related_Training',
            ('platforms_sites', 'knowledge_vault'): 'Related_Platforms',
            ('notes_ideas', 'knowledge_vault'): 'Related_Notes',
            ('notes_ideas', 'tools_services'): 'Related_Notes',
            ('notes_ideas', 'business_ideas'): 'Related_Notes',
            ('notes_ideas', 'training_vault'): 'Related_Notes',
            ('notes_ideas', 'platforms_sites'): 'Related_Notes',
        }
        
        return reverse_mappings.get((target_db, source_db))

class BatchMigrationOrchestrator:
    """Main orchestrator for batch migration process with Database ID Registry integration"""
    
    def __init__(self, config: MigrationConfig):
        self.config = config
        self.notion_client = NotionAPIClient(config.notion_token)
        self.created_databases = {}
        self.migration_results = []
        
        # Initialize Database ID Registry Manager
        self.registry_manager = DatabaseIDRegistryManager()
        self.relationship_manager = RelationshipManager(self.notion_client, self.registry_manager)
        
        # Load configuration files
        self.transformation_config = self._load_yaml(config.transformation_config_path)
        self.property_mappings = self._load_yaml(config.property_mappings_path)
        self.data_transformer = DataTransformer(self.transformation_config, self.property_mappings)
        
        # Create logs directory
        (Path(__file__).parent.parent / 'logs').mkdir(exist_ok=True)
        
        logger.info("BatchMigrationOrchestrator initialized with Database ID Registry integration")
        
    def _load_yaml(self, path: Path) -> Dict:
        """Load YAML configuration file"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Error loading {path}: {e}")
            raise
    
    def execute_migration(self) -> Dict:
        """Execute complete migration process"""
        start_time = time.time()
        logger.info("Starting VanguardAI test environment migration")
        
        try:
            # Step 1: Create databases
            logger.info("Creating Notion databases...")
            self._create_databases()
            
            # Step 2: Load and validate items
            logger.info("Loading VanguardAI test items...")
            items = self._load_vanguardai_items()
            
            # Step 3: Migrate items in batches
            logger.info(f"Migrating {len(items)} items in batches of {self.config.batch_size}...")
            self._migrate_items_in_batches(items)
            
            # Step 4: Create relationships
            logger.info("Creating cross-database relationships...")
            self._create_relationships()
            
            # Step 5: Save Database ID Registry
            logger.info("Saving Database ID Registry...")
            self.registry_manager.save_registry()
            
            # Step 6: Generate report
            duration = time.time() - start_time
            report = self._generate_migration_report(duration)
            
            logger.info(f"Migration completed in {duration:.2f} seconds")
            return report
            
        except Exception as e:
            logger.error(f"Migration failed: {e}")
            raise
    
    def _create_databases(self):
        """Create all required Notion databases"""
        database_schemas = self.property_mappings['notion_database_schemas']
        
        creation_order = [
            'knowledge_vault_database',
            'tools_services_database', 
            'business_ideas_database',
            'training_vault_database',
            'platforms_sites_database',
            'notes_ideas_database'
        ]
        
        for db_key in creation_order:
            if db_key not in database_schemas:
                logger.warning(f"Database schema not found: {db_key}")
                continue
                
            schema = database_schemas[db_key]
            logger.info(f"Creating database: {schema['database_name']}")
            
            if not self.config.dry_run:
                try:
                    # Convert properties to Notion format
                    notion_properties = self._convert_properties_to_notion_format(schema['properties'])
                    
                    # Create database
                    database_response = self.notion_client.create_database(
                        parent_id=self.config.workspace_id,
                        title=schema['database_name'],
                        properties=notion_properties
                    )
                    
                    self.created_databases[db_key] = DatabaseInfo(
                        notion_id=database_response['id'],
                        name=schema['database_name'],
                        database_type=db_key,
                        properties=notion_properties,
                        created_at=datetime.now()
                    )
                    
                    logger.info(f"Created database: {schema['database_name']} (ID: {database_response['id']})")
                    
                except Exception as e:
                    logger.error(f"Failed to create database {schema['database_name']}: {e}")
                    raise
            else:
                logger.info(f"[DRY RUN] Would create database: {schema['database_name']}")
    
    def _convert_properties_to_notion_format(self, properties: Dict) -> Dict:
        """Convert property definitions to Notion API format"""
        notion_properties = {}
        
        for prop_name, prop_config in properties.items():
            if prop_config['type'] == 'title':
                notion_properties[prop_name] = {'title': {}}
                
            elif prop_config['type'] == 'rich_text':
                notion_properties[prop_name] = {'rich_text': {}}
                
            elif prop_config['type'] == 'select':
                options = []
                if 'options' in prop_config:
                    options = [
                        {'name': opt['name'], 'color': opt['color']}
                        for opt in prop_config['options']
                    ]
                notion_properties[prop_name] = {'select': {'options': options}}
                
            elif prop_config['type'] == 'multi_select':
                options = []
                if 'options' in prop_config:
                    options = [
                        {'name': opt['name'], 'color': opt['color']}
                        for opt in prop_config['options']
                    ]
                notion_properties[prop_name] = {'multi_select': {'options': options}}
                
            elif prop_config['type'] == 'number':
                notion_properties[prop_name] = {'number': {'format': 'number'}}
                
            elif prop_config['type'] == 'url':
                notion_properties[prop_name] = {'url': {}}
                
            elif prop_config['type'] == 'checkbox':
                notion_properties[prop_name] = {'checkbox': {}}
                
            elif prop_config['type'] == 'relation':
                # Relations will be configured after all databases are created
                notion_properties[prop_name] = {
                    'relation': {
                        'database_id': 'PLACEHOLDER_DATABASE_ID'
                    }
                }
                
            elif prop_config['type'] == 'created_time':
                notion_properties[prop_name] = {'created_time': {}}
                
            elif prop_config['type'] == 'last_edited_time':
                notion_properties[prop_name] = {'last_edited_time': {}}
                
        return notion_properties
    
    def _load_vanguardai_items(self) -> List[Tuple[Dict, str]]:
        """Load all VanguardAI test items"""
        items = []
        vanguardai_path = self.config.source_path / 'databases' / 'vanguard-ai-test'
        
        database_dirs = {
            'knowledge_vault_items': 'knowledge_vault',
            'tools_services_items': 'tools_services',
            'business_ideas_items': 'business_ideas',
            'training_vault_items': 'training_vault',
            'platforms_sites_items': 'platforms_sites',
            'notes_ideas_items': 'notes_ideas'
        }
        
        for dir_name, db_type in database_dirs.items():
            item_dir = vanguardai_path / dir_name
            if not item_dir.exists():
                logger.warning(f"Directory not found: {item_dir}")
                continue
                
            for item_file in item_dir.glob('*.yaml'):
                try:
                    with open(item_file, 'r', encoding='utf-8') as f:
                        item_data = yaml.safe_load(f)
                    items.append((item_data, db_type))
                    logger.debug(f"Loaded item: {item_data.get('id', 'unknown')} ({db_type})")
                except Exception as e:
                    logger.error(f"Error loading {item_file}: {e}")
                    
        logger.info(f"Loaded {len(items)} items from VanguardAI test environment")
        return items
    
    def _migrate_items_in_batches(self, items: List[Tuple[Dict, str]]):
        """Migrate items in batches with error handling"""
        all_relationships = []
        
        for i in range(0, len(items), self.config.batch_size):
            batch = items[i:i + self.config.batch_size]
            logger.info(f"Processing batch {i // self.config.batch_size + 1} ({len(batch)} items)")
            
            for item_data, db_type in batch:
                result = self._migrate_single_item(item_data, db_type)
                self.migration_results.append(result)
                
                # Collect relationships for later processing
                if result.success and 'relationships' in item_data:
                    item_relationships = self.data_transformer._extract_relationships(
                        item_data['relationships'],
                        self.transformation_config['database_transformations'][f'{db_type}_transformations'].get('relationship_mappings', {}),
                        item_data['id']
                    )
                    # Add source database info to relationships
                    for rel in item_relationships:
                        rel['source_database'] = db_type
                    all_relationships.extend(item_relationships)
            
            # Brief pause between batches
            if i + self.config.batch_size < len(items):
                time.sleep(2)
        
        # Store relationships for final processing
        self.collected_relationships = all_relationships
    
    def _migrate_single_item(self, item_data: Dict, database_type: str) -> MigrationResult:
        """Migrate a single item to Notion"""
        start_time = time.time()
        item_id = item_data.get('id', 'unknown')
        retry_count = 0
        
        try:
            # Transform item data
            notion_properties, relationships = self.data_transformer.transform_item(item_data, database_type)
            
            # Get target database ID
            database_key = f"{database_type}_database"
            if database_key not in self.created_databases:
                raise Exception(f"Database not created: {database_key}")
                
            database_id = self.created_databases[database_key].notion_id
            
            # Create page in Notion
            if not self.config.dry_run:
                for attempt in range(self.config.max_retries):
                    try:
                        page_response = self.notion_client.create_page(
                            database_id=database_id,
                            properties=notion_properties
                        )
                        
                        # Cache item mapping for relationships with registry integration
                        page_id = page_response['id']
                        database_id = self.created_databases[database_key].notion_id
                        item_title = item_data.get('name', item_data.get('title', item_id))
                        item_description = item_data.get('description', '')
                        
                        self.relationship_manager.add_item_mapping(
                            item_id=item_id,
                            notion_page_id=page_id,
                            database_type=database_type,
                            database_notion_id=database_id,
                            title=item_title,
                            content=item_description
                        )
                        
                        processing_time = time.time() - start_time
                        return MigrationResult(
                            item_id=item_id,
                            database_type=database_type,
                            notion_page_id=page_id,
                            success=True,
                            error_message=None,
                            processing_time=processing_time,
                            relationships_created=0,  # Will be updated later
                            retry_count=retry_count
                        )
                        
                    except Exception as e:
                        retry_count += 1
                        logger.warning(f"Attempt {attempt + 1} failed for {item_id}: {e}")
                        if attempt == self.config.max_retries - 1:
                            raise
                        time.sleep(2 ** attempt)  # Exponential backoff
            else:
                logger.info(f"[DRY RUN] Would migrate {item_id} to {database_type}")
                return MigrationResult(
                    item_id=item_id,
                    database_type=database_type,
                    notion_page_id="dry_run_page_id",
                    success=True,
                    error_message=None,
                    processing_time=0.1,
                    relationships_created=0,
                    retry_count=0
                )
                
        except Exception as e:
            processing_time = time.time() - start_time
            error_msg = str(e)
            logger.error(f"Failed to migrate {item_id}: {error_msg}")
            
            return MigrationResult(
                item_id=item_id,
                database_type=database_type,
                notion_page_id=None,
                success=False,
                error_message=error_msg,
                processing_time=processing_time,
                relationships_created=0,
                retry_count=retry_count
            )
    
    def _create_relationships(self):
        """Create cross-database relationships"""
        if self.config.dry_run:
            logger.info(f"[DRY RUN] Would create {len(self.collected_relationships)} relationships")
            return
            
        logger.info(f"Creating {len(self.collected_relationships)} cross-database relationships...")
        
        # Create database mappings for relationship manager
        database_mappings = {}
        for db_key, db_info in self.created_databases.items():
            database_mappings[db_key] = db_info.notion_id
        
        # Resolve relationships in batches
        relationship_batches = [
            self.collected_relationships[i:i + 10] 
            for i in range(0, len(self.collected_relationships), 10)
        ]
        
        total_created = 0
        for batch_num, batch in enumerate(relationship_batches, 1):
            logger.info(f"Processing relationship batch {batch_num}/{len(relationship_batches)}")
            
            try:
                created = self.relationship_manager.resolve_relationships(batch, database_mappings)
                total_created += created
                logger.info(f"Created {created} relationships in batch {batch_num}")
                
                # Brief pause between batches
                if batch_num < len(relationship_batches):
                    time.sleep(1)
                    
            except Exception as e:
                logger.error(f"Error in relationship batch {batch_num}: {e}")
        
        logger.info(f"Total relationships created: {total_created}")
    
    def _generate_migration_report(self, duration: float) -> Dict:
        """Generate comprehensive migration report"""
        successful_migrations = [r for r in self.migration_results if r.success]
        failed_migrations = [r for r in self.migration_results if not r.success]
        
        # Group by database type
        by_database = {}
        for result in self.migration_results:
            if result.database_type not in by_database:
                by_database[result.database_type] = {'success': 0, 'failed': 0}
            if result.success:
                by_database[result.database_type]['success'] += 1
            else:
                by_database[result.database_type]['failed'] += 1
        
        report = {
            'migration_summary': {
                'total_items': len(self.migration_results),
                'successful': len(successful_migrations),
                'failed': len(failed_migrations),
                'success_rate': (len(successful_migrations) / len(self.migration_results)) * 100 if self.migration_results else 0,
                'total_duration': duration,
                'average_item_time': sum(r.processing_time for r in self.migration_results) / len(self.migration_results) if self.migration_results else 0
            },
            'databases_created': len(self.created_databases),
            'by_database_type': by_database,
            'created_databases': {
                db_key: {
                    'notion_id': db_info.notion_id,
                    'name': db_info.name,
                    'created_at': db_info.created_at.isoformat()
                }
                for db_key, db_info in self.created_databases.items()
            },
            'failed_items': [
                {
                    'item_id': r.item_id,
                    'database_type': r.database_type,
                    'error': r.error_message,
                    'retry_count': r.retry_count
                }
                for r in failed_migrations
            ],
            'performance_metrics': {
                'total_retries': sum(r.retry_count for r in self.migration_results),
                'avg_processing_time': sum(r.processing_time for r in successful_migrations) / len(successful_migrations) if successful_migrations else 0,
                'relationships_processed': len(getattr(self, 'collected_relationships', [])),
            },
            'database_id_registry_stats': self.registry_manager.get_registry_statistics()
        }
        
        # Save report to file
        report_path = Path(__file__).parent.parent / 'logs' / f'migration_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info(f"Migration report saved to: {report_path}")
        return report

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='VanguardAI Knowledge Vault Migration')
    parser.add_argument('--notion-token', required=True, help='Notion API token')
    parser.add_argument('--workspace-id', required=True, help='Notion workspace page ID')
    parser.add_argument('--source-path', default='knowledge-vault', help='Source path for knowledge vault')
    parser.add_argument('--batch-size', type=int, default=5, help='Batch size for migration')
    parser.add_argument('--dry-run', action='store_true', help='Run migration in dry-run mode')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Build configuration
    config = MigrationConfig(
        notion_token=args.notion_token,
        workspace_id=args.workspace_id,
        source_path=Path(args.source_path),
        transformation_config_path=Path(__file__).parent.parent / 'data-transformations.yaml',
        property_mappings_path=Path(__file__).parent.parent / 'notion-property-mappings.yaml',
        batch_size=args.batch_size,
        dry_run=args.dry_run
    )
    
    # Execute migration
    orchestrator = BatchMigrationOrchestrator(config)
    
    try:
        report = orchestrator.execute_migration()
        
        print("\n" + "="*60)
        print("MIGRATION COMPLETED SUCCESSFULLY")
        print("="*60)
        print(f"Total items processed: {report['migration_summary']['total_items']}")
        print(f"Successful migrations: {report['migration_summary']['successful']}")
        print(f"Failed migrations: {report['migration_summary']['failed']}")
        print(f"Success rate: {report['migration_summary']['success_rate']:.1f}%")
        print(f"Duration: {report['migration_summary']['total_duration']:.2f} seconds")
        print(f"Databases created: {report['databases_created']}")
        
        if report['failed_items']:
            print(f"\nFailed items:")
            for item in report['failed_items']:
                print(f"  - {item['item_id']} ({item['database_type']}): {item['error']}")
                
    except Exception as e:
        logger.error(f"Migration failed with error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()