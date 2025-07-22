#!/usr/bin/env python3
"""
Knowledge-Vault Batch Migration Script
AI INSTRUCTIONS: This script performs automated batch migration of knowledge-vault items to Notion

Purpose: Production-ready batch migration with comprehensive error handling and validation
Target: 30 VanguardAI test items for validation, scalable to 400+ full migration
"""

import os
import sys
import json
import yaml
import logging
import argparse
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import requests
from dataclasses import dataclass
from enum import Enum

# Configuration and Constants
NOTION_API_VERSION = "2022-06-28"
NOTION_BASE_URL = "https://api.notion.com/v1"
DEFAULT_BATCH_SIZE = 25
MAX_RETRIES = 3
RATE_LIMIT_DELAY = 0.5  # 500ms between requests to respect Notion's 3 requests/second limit

class MigrationStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"

@dataclass
class MigrationItem:
    """Represents a single item to be migrated"""
    source_file: Path
    database_type: str
    item_data: Dict[str, Any]
    notion_database_id: str
    migration_status: MigrationStatus = MigrationStatus.PENDING
    error_message: Optional[str] = None
    notion_page_id: Optional[str] = None
    retry_count: int = 0

@dataclass
class MigrationResult:
    """Results of a migration batch"""
    total_items: int
    completed: int
    failed: int
    skipped: int
    errors: List[str]
    duration_seconds: float
    performance_metrics: Dict[str, Any]

class NotionAPIClient:
    """Notion API client with rate limiting and error handling"""
    
    def __init__(self, auth_token: str, timeout: int = 30):
        self.auth_token = auth_token
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {auth_token}',
            'Content-Type': 'application/json',
            'Notion-Version': NOTION_API_VERSION
        })
        self.last_request_time = 0
        
    def _rate_limit(self):
        """Implement rate limiting to respect Notion's 3 requests/second limit"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < RATE_LIMIT_DELAY:
            time.sleep(RATE_LIMIT_DELAY - time_since_last)
        self.last_request_time = time.time()
    
    def create_page(self, database_id: str, properties: Dict[str, Any]) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Create a page in a Notion database
        Returns: (success, page_id, error_message)
        """
        self._rate_limit()
        
        payload = {
            "parent": {"database_id": database_id},
            "properties": properties
        }
        
        try:
            response = self.session.post(
                f"{NOTION_BASE_URL}/pages",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return True, result.get('id'), None
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                return False, None, error_msg
                
        except requests.exceptions.RequestException as e:
            return False, None, f"Request error: {str(e)}"
    
    def get_database_schema(self, database_id: str) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """Get database schema for validation"""
        self._rate_limit()
        
        try:
            response = self.session.get(
                f"{NOTION_BASE_URL}/databases/{database_id}",
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return True, response.json(), None
            else:
                error_msg = f"HTTP {response.status_code}: {response.text}"
                return False, None, error_msg
                
        except requests.exceptions.RequestException as e:
            return False, None, f"Request error: {str(e)}"

class DataTransformer:
    """Transform YAML data to Notion-compatible format"""
    
    def __init__(self, mappings_config: Dict[str, Any]):
        self.mappings_config = mappings_config
        self.database_schemas = mappings_config.get('notion_database_schemas', {})
        self.transformation_rules = mappings_config.get('transformation_rules', {})
        
    def transform_item(self, item_data: Dict[str, Any], database_type: str) -> Tuple[bool, Optional[Dict], Optional[str]]:
        """
        Transform a knowledge-vault item to Notion format
        Returns: (success, notion_properties, error_message)
        """
        try:
            if database_type not in self.transformation_rules:
                return False, None, f"No transformation rules found for database type: {database_type}"
            
            rules = self.transformation_rules[database_type]
            field_transformations = rules.get('field_transformations', {})
            notion_properties = {}
            
            for field_name, transformation in field_transformations.items():
                source_field = transformation.get('source_field')
                transformation_type = transformation.get('transformation_type')
                
                # Extract source value
                source_value = self._extract_source_value(item_data, source_field)
                
                # Apply transformation
                if source_value is not None:
                    notion_value = self._apply_transformation(source_value, transformation)
                    if notion_value is not None:
                        notion_properties[field_name] = notion_value
                elif transformation.get('validation') == 'required':
                    return False, None, f"Required field missing: {source_field}"
            
            return True, notion_properties, None
            
        except Exception as e:
            return False, None, f"Transformation error: {str(e)}"
    
    def _extract_source_value(self, data: Dict[str, Any], source_field: str) -> Any:
        """Extract value from nested dictionary using dot notation"""
        if not source_field:
            return None
            
        keys = source_field.split('.')
        value = data
        
        try:
            for key in keys:
                if isinstance(value, dict):
                    value = value.get(key)
                else:
                    return None
            return value
        except:
            return None
    
    def _apply_transformation(self, value: Any, transformation: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Apply specific transformation based on type"""
        transformation_type = transformation.get('transformation_type')
        
        if transformation_type == 'direct_copy':
            return self._transform_title(value, transformation)
        elif transformation_type == 'rich_text_conversion':
            return self._transform_rich_text(value, transformation)
        elif transformation_type == 'category_mapping':
            return self._transform_select(value, transformation)
        elif transformation_type == 'array_to_multi_select':
            return self._transform_multi_select(value, transformation)
        elif transformation_type == 'url_validation':
            return self._transform_url(value, transformation)
        elif transformation_type == 'date_conversion':
            return self._transform_date(value, transformation)
        elif transformation_type == 'boolean_conversion':
            return self._transform_checkbox(value, transformation)
        else:
            # Default to rich text for unknown types
            return self._transform_rich_text(value, transformation)
    
    def _transform_title(self, value: Any, transformation: Dict[str, Any]) -> Dict[str, Any]:
        """Transform to Notion title format"""
        max_length = transformation.get('max_length', 2000)
        text = str(value)[:max_length]
        return {
            "title": [{"text": {"content": text}}]
        }
    
    def _transform_rich_text(self, value: Any, transformation: Dict[str, Any]) -> Dict[str, Any]:
        """Transform to Notion rich text format"""
        max_length = transformation.get('max_length', 2000)
        text = str(value)[:max_length]
        return {
            "rich_text": [{"text": {"content": text}}]
        }
    
    def _transform_select(self, value: Any, transformation: Dict[str, Any]) -> Dict[str, Any]:
        """Transform to Notion select format"""
        return {
            "select": {"name": str(value)}
        }
    
    def _transform_multi_select(self, value: Any, transformation: Dict[str, Any]) -> Dict[str, Any]:
        """Transform to Notion multi-select format"""
        if isinstance(value, list):
            options = [{"name": str(item)} for item in value]
        else:
            options = [{"name": str(value)}]
        return {
            "multi_select": options
        }
    
    def _transform_url(self, value: Any, transformation: Dict[str, Any]) -> Dict[str, Any]:
        """Transform to Notion URL format"""
        url = str(value)
        if not url.startswith(('http://', 'https://')):
            protocol = transformation.get('add_protocol', 'https')
            url = f"{protocol}://{url}"
        return {
            "url": url
        }
    
    def _transform_date(self, value: Any, transformation: Dict[str, Any]) -> Dict[str, Any]:
        """Transform to Notion date format"""
        # For simplicity, assume ISO date format
        return {
            "date": {"start": str(value)}
        }
    
    def _transform_checkbox(self, value: Any, transformation: Dict[str, Any]) -> Dict[str, Any]:
        """Transform to Notion checkbox format"""
        return {
            "checkbox": bool(value)
        }

class BatchMigrationManager:
    """Main migration management class"""
    
    def __init__(self, 
                 source_dir: Path, 
                 notion_client: NotionAPIClient,
                 transformer: DataTransformer,
                 batch_size: int = DEFAULT_BATCH_SIZE):
        self.source_dir = source_dir
        self.notion_client = notion_client
        self.transformer = transformer
        self.batch_size = batch_size
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        """Setup logging configuration"""
        logger = logging.getLogger('batch_migration')
        logger.setLevel(logging.INFO)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create file handler
        log_file = Path("operations/logs/batch_migration.log")
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        
        return logger
    
    def discover_migration_items(self, database_mappings: Dict[str, str]) -> List[MigrationItem]:
        """Discover all YAML files to migrate"""
        migration_items = []
        
        for database_type, database_id in database_mappings.items():
            # Look for YAML files in database-specific directories
            pattern = f"databases/{database_type}/*.yaml"
            yaml_files = list(self.source_dir.glob(pattern))
            
            for yaml_file in yaml_files:
                try:
                    with open(yaml_file, 'r', encoding='utf-8') as f:
                        item_data = yaml.safe_load(f)
                    
                    migration_item = MigrationItem(
                        source_file=yaml_file,
                        database_type=database_type,
                        item_data=item_data,
                        notion_database_id=database_id
                    )
                    migration_items.append(migration_item)
                    
                except Exception as e:
                    self.logger.error(f"Failed to load {yaml_file}: {str(e)}")
        
        return migration_items
    
    def migrate_batch(self, items: List[MigrationItem]) -> MigrationResult:
        """Migrate a batch of items"""
        start_time = time.time()
        completed = 0
        failed = 0
        skipped = 0
        errors = []
        
        self.logger.info(f"Starting migration of {len(items)} items")
        
        for i, item in enumerate(items, 1):
            self.logger.info(f"Processing item {i}/{len(items)}: {item.source_file.name}")
            
            # Transform item
            success, properties, error = self.transformer.transform_item(
                item.item_data, item.database_type
            )
            
            if not success:
                item.migration_status = MigrationStatus.FAILED
                item.error_message = error
                errors.append(f"{item.source_file.name}: {error}")
                failed += 1
                continue
            
            # Create Notion page
            success, page_id, error = self.notion_client.create_page(
                item.notion_database_id, properties
            )
            
            if success:
                item.migration_status = MigrationStatus.COMPLETED
                item.notion_page_id = page_id
                completed += 1
                self.logger.info(f"Successfully migrated {item.source_file.name}")
            else:
                item.migration_status = MigrationStatus.FAILED
                item.error_message = error
                errors.append(f"{item.source_file.name}: {error}")
                failed += 1
                self.logger.error(f"Failed to migrate {item.source_file.name}: {error}")
        
        duration = time.time() - start_time
        
        result = MigrationResult(
            total_items=len(items),
            completed=completed,
            failed=failed,
            skipped=skipped,
            errors=errors,
            duration_seconds=duration,
            performance_metrics={
                'items_per_second': len(items) / duration if duration > 0 else 0,
                'success_rate': completed / len(items) if len(items) > 0 else 0
            }
        )
        
        self.logger.info(f"Migration batch completed: {completed} successful, {failed} failed")
        return result
    
    def generate_migration_report(self, results: List[MigrationResult], output_file: Path):
        """Generate comprehensive migration report"""
        report = {
            'migration_summary': {
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'total_batches': len(results),
                'total_items': sum(r.total_items for r in results),
                'total_completed': sum(r.completed for r in results),
                'total_failed': sum(r.failed for r in results),
                'total_skipped': sum(r.skipped for r in results),
                'overall_success_rate': sum(r.completed for r in results) / sum(r.total_items for r in results) if results else 0,
                'total_duration_seconds': sum(r.duration_seconds for r in results)
            },
            'batch_results': [],
            'all_errors': []
        }
        
        for i, result in enumerate(results, 1):
            report['batch_results'].append({
                'batch_number': i,
                'total_items': result.total_items,
                'completed': result.completed,
                'failed': result.failed,
                'skipped': result.skipped,
                'duration_seconds': result.duration_seconds,
                'success_rate': result.performance_metrics['success_rate'],
                'items_per_second': result.performance_metrics['items_per_second']
            })
            report['all_errors'].extend(result.errors)
        
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Migration report generated: {output_file}")

def load_config(config_file: Path) -> Dict[str, Any]:
    """Load configuration from YAML file"""
    with open(config_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Batch migrate knowledge-vault items to Notion')
    parser.add_argument('--source-dir', type=Path, required=True,
                        help='Source directory containing knowledge-vault YAML files')
    parser.add_argument('--notion-token', type=str,
                        help='Notion integration token (or set NOTION_TOKEN env var)')
    parser.add_argument('--database-mappings', type=Path, required=True,
                        help='JSON file mapping database types to Notion database IDs')
    parser.add_argument('--mappings-config', type=Path, required=True,
                        help='YAML file containing property mappings configuration')
    parser.add_argument('--batch-size', type=int, default=DEFAULT_BATCH_SIZE,
                        help='Number of items to process per batch')
    parser.add_argument('--output-report', type=Path,
                        default='operations/logs/migration_report.json',
                        help='Output file for migration report')
    parser.add_argument('--dry-run', action='store_true',
                        help='Perform validation only, do not create Notion pages')
    
    args = parser.parse_args()
    
    # Get Notion token
    notion_token = args.notion_token or os.environ.get('NOTION_TOKEN')
    if not notion_token:
        print("ERROR: Notion token is required. Use --notion-token or set NOTION_TOKEN environment variable.")
        sys.exit(1)
    
    try:
        # Load configurations
        with open(args.database_mappings, 'r') as f:
            database_mappings = json.load(f)
        
        mappings_config = load_config(args.mappings_config)
        
        # Initialize components
        notion_client = NotionAPIClient(notion_token)
        transformer = DataTransformer(mappings_config)
        migration_manager = BatchMigrationManager(
            args.source_dir, notion_client, transformer, args.batch_size
        )
        
        # Discover migration items
        migration_items = migration_manager.discover_migration_items(database_mappings)
        
        if not migration_items:
            print("No migration items found.")
            sys.exit(0)
        
        print(f"Found {len(migration_items)} items to migrate")
        
        if args.dry_run:
            print("DRY RUN: Validating transformations only")
            for item in migration_items:
                success, properties, error = transformer.transform_item(
                    item.item_data, item.database_type
                )
                if success:
                    print(f"✓ {item.source_file.name}: Valid transformation")
                else:
                    print(f"✗ {item.source_file.name}: {error}")
            sys.exit(0)
        
        # Process items in batches
        results = []
        for i in range(0, len(migration_items), args.batch_size):
            batch = migration_items[i:i + args.batch_size]
            result = migration_manager.migrate_batch(batch)
            results.append(result)
        
        # Generate report
        migration_manager.generate_migration_report(results, args.output_report)
        
        # Print summary
        total_items = sum(r.total_items for r in results)
        total_completed = sum(r.completed for r in results)
        total_failed = sum(r.failed for r in results)
        
        print(f"\nMigration completed:")
        print(f"  Total items: {total_items}")
        print(f"  Successful: {total_completed}")
        print(f"  Failed: {total_failed}")
        print(f"  Success rate: {total_completed/total_items*100:.1f}%")
        print(f"  Report: {args.output_report}")
        
        if total_failed > 0:
            sys.exit(1)
            
    except Exception as e:
        print(f"ERROR: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()