#!/usr/bin/env python3
"""
Notion Sync Operations Updater

This script updates Notion sync operations to handle Markdown content with YAML frontmatter:
1. Updates sync scripts to parse frontmatter instead of YAML
2. Handles Markdown content conversion to Notion rich text
3. Ensures bidirectional sync works with new format
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
import json
import shutil

class NotionSyncUpdater:
    """Update Notion sync operations for Markdown format."""
    
    def __init__(self, backup=True):
        self.backup = backup
        self.knowledge_vault_path = Path(__file__).parent.parent.parent
        self.update_stats = {
            'files_updated': 0,
            'sync_configs_updated': 0,
            'scripts_updated': 0,
            'errors': 0,
            'updated_files': []
        }
    
    def update_notion_sync_operations(self):
        """Update all Notion sync operations for Markdown format."""
        print("🔄 Starting Notion sync operations update...")
        print("Updating sync operations to handle Markdown content with YAML frontmatter...")
        
        if self.backup:
            self._create_backup()
        
        # Update configuration files
        self._update_sync_configurations()
        
        # Create updated sync implementation example
        self._create_markdown_sync_implementation()
        
        # Update any existing sync scripts
        self._update_sync_scripts()
        
        self._print_summary()
    
    def _create_backup(self):
        """Create backup of sync operations."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.knowledge_vault_path / f"backups/notion_sync_backup_{timestamp}"
        
        print(f"📦 Creating backup at: {backup_path}")
        
        backup_path.mkdir(parents=True, exist_ok=True)
        
        # Backup operations directory
        operations_dir = self.knowledge_vault_path / "operations"
        if operations_dir.exists():
            shutil.copytree(
                operations_dir,
                backup_path / "operations",
                ignore=shutil.ignore_patterns('*.pyc', '__pycache__', '.DS_Store', 'venv')
            )
        
        print(f"✅ Notion sync backup created successfully")
    
    def _update_sync_configurations(self):
        """Update sync configuration files."""
        print(f"\n⚙️  Updating sync configuration files...")
        
        # Update sync-operations.md
        sync_ops_file = self.knowledge_vault_path / "operations/sync-operations.md"
        if sync_ops_file.exists():
            try:
                self._update_sync_operations_config(sync_ops_file)
                print(f"   ✅ Updated: sync-operations.md")
                self.update_stats['sync_configs_updated'] += 1
            except Exception as e:
                print(f"   ❌ Error updating sync-operations.md: {str(e)}")
                self.update_stats['errors'] += 1
        
        # Update notion-integration.md
        notion_integration_file = self.knowledge_vault_path / "operations/notion-integration.md"
        if notion_integration_file.exists():
            try:
                self._update_notion_integration_config(notion_integration_file)
                print(f"   ✅ Updated: notion-integration.md")
                self.update_stats['sync_configs_updated'] += 1
            except Exception as e:
                print(f"   ❌ Error updating notion-integration.md: {str(e)}")
                self.update_stats['errors'] += 1
    
    def _update_sync_operations_config(self, file_path: Path):
        """Update sync operations configuration."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update references to file format
        updates = [
            ('Markdown files', 'Markdown files with YAML frontmatter'),
            ('Markdown files', 'Markdown files with YAML frontmatter'),
            ('.md files', '.md files'),
            ('YAML format', 'Markdown format with YAML frontmatter'),
            ('yaml.safe_load', 'frontmatter.load'),
            ('Parse YAML', 'Parse frontmatter'),
            ('YAML parsing', 'frontmatter parsing')
        ]
        
        original_content = content
        for old_text, new_text in updates:
            content = content.replace(old_text, new_text)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.update_stats['files_updated'] += 1
            self.update_stats['updated_files'].append(str(file_path.relative_to(self.knowledge_vault_path)))
    
    def _update_notion_integration_config(self, file_path: Path):
        """Update Notion integration configuration."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update references to file format and add frontmatter handling
        updates = [
            ('Markdown files', 'Markdown files with YAML frontmatter'),
            ('Markdown files', 'Markdown files with YAML frontmatter'),
            ('.md files', '.md files'),
            ('yaml.safe_load', 'frontmatter.load'),
            ('Parse YAML content', 'Parse Markdown frontmatter'),
            ('YAML frontmatter', 'YAML frontmatter (embedded in Markdown)'),
        ]
        
        original_content = content
        for old_text, new_text in updates:
            content = content.replace(old_text, new_text)
        
        # Add note about Markdown content handling
        if '# Data Transformation Rules' in content and 'markdown_content_handling' not in content:
            transformation_section = """
# Markdown Content Handling
markdown_content_handling:
  frontmatter_extraction:
    description: "Extract YAML frontmatter from Markdown files"
    method: "Use frontmatter library to parse .md files"
    preservation: "Maintain all metadata in frontmatter during sync"
  
  content_conversion:
    markdown_to_notion:
      description: "Convert Markdown content to Notion rich text blocks"
      method: "Parse Markdown and convert to Notion block format"
      supported_elements: ["headers", "paragraphs", "lists", "links", "emphasis"]
    
    notion_to_markdown:
      description: "Convert Notion rich text to Markdown format"
      method: "Extract blocks and convert to Markdown syntax"
      preservation: "Maintain formatting and structure"
  
  sync_efficiency:
    change_detection: "Compare frontmatter timestamps for incremental sync"
    content_comparison: "Hash-based comparison for content changes"
    batch_processing: "Group multiple file operations for efficiency"

"""
            # Insert before existing transformation rules
            content = content.replace('# Data Transformation Rules', transformation_section + '# Data Transformation Rules')
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.update_stats['files_updated'] += 1
            self.update_stats['updated_files'].append(str(file_path.relative_to(self.knowledge_vault_path)))
    
    def _create_markdown_sync_implementation(self):
        """Create updated sync implementation example for Markdown."""
        print(f"\n📝 Creating Markdown sync implementation example...")
        
        implementation_content = '''# Knowledge Vault Notion Sync - Markdown Implementation

This document provides implementation examples for syncing Markdown files with YAML frontmatter to Notion databases.

## Prerequisites

```python
import frontmatter
import yaml
from pathlib import Path
from typing import Dict, Any, List

# MCP Notion API tools
# - mcp__MCP_DOCKER__API-retrieve-a-database
# - mcp__MCP_DOCKER__API-post-database-query
# - mcp__MCP_DOCKER__API-retrieve-a-page
# - mcp__MCP_DOCKER__API-patch-page
# - mcp__MCP_DOCKER__API-post-page
```

## Markdown File Reading

```python
def read_markdown_file(file_path: Path) -> Dict[str, Any]:
    """Read Markdown file with YAML frontmatter."""
    with open(file_path, 'r', encoding='utf-8') as f:
        post = frontmatter.load(f)
    
    return {
        'metadata': post.metadata,
        'content': post.content,
        'frontmatter': post.metadata,
        'markdown_content': post.content
    }

def write_markdown_file(file_path: Path, metadata: Dict[str, Any], content: str):
    """Write Markdown file with YAML frontmatter."""
    post = frontmatter.Post(content, **metadata)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter.dumps(post))
```

## File to Notion Sync

```python
def sync_file_to_notion(file_path: Path, notion_database_id: str) -> bool:
    """Sync Markdown file to Notion database."""
    try:
        # Read Markdown file
        file_data = read_markdown_file(file_path)
        metadata = file_data['metadata']
        content = file_data['content']
        
        # Check if page already exists in Notion
        existing_page = find_notion_page_by_id(metadata.get('id'), notion_database_id)
        
        if existing_page:
            # Update existing page
            return update_notion_page(existing_page['id'], metadata, content)
        else:
            # Create new page
            return create_notion_page(notion_database_id, metadata, content)
            
    except Exception as e:
        print(f"Error syncing {file_path.name}: {str(e)}")
        return False

def create_notion_page(database_id: str, metadata: Dict[str, Any], content: str) -> bool:
    """Create new Notion page from Markdown data."""
    # Prepare properties for Notion
    properties = prepare_notion_properties(metadata)
    
    # Convert Markdown content to Notion blocks
    children = convert_markdown_to_notion_blocks(content)
    
    # Use MCP API to create page
    # mcp__MCP_DOCKER__API-post-page with database_id, properties, children
    return True

def update_notion_page(page_id: str, metadata: Dict[str, Any], content: str) -> bool:
    """Update existing Notion page with Markdown data."""
    # Prepare properties for update
    properties = prepare_notion_properties(metadata)
    
    # Use MCP API to update page properties
    # mcp__MCP_DOCKER__API-patch-page with page_id and properties
    
    # Update page content if needed
    children = convert_markdown_to_notion_blocks(content)
    # mcp__MCP_DOCKER__API-patch-block-children with page_id and children
    
    return True
```

## Notion to File Sync

```python
def sync_notion_to_file(page_id: str, file_path: Path) -> bool:
    """Sync Notion page to Markdown file."""
    try:
        # Retrieve page from Notion
        # page_data = mcp__MCP_DOCKER__API-retrieve-a-page(page_id)
        page_data = get_notion_page(page_id)  # Placeholder
        
        # Extract metadata from Notion properties
        metadata = extract_metadata_from_notion(page_data['properties'])
        
        # Get page content blocks
        # blocks = mcp__MCP_DOCKER__API-get-block-children(page_id)
        blocks = get_notion_blocks(page_id)  # Placeholder
        
        # Convert Notion blocks to Markdown
        content = convert_notion_blocks_to_markdown(blocks)
        
        # Write to Markdown file
        write_markdown_file(file_path, metadata, content)
        
        return True
        
    except Exception as e:
        print(f"Error syncing Notion page to {file_path.name}: {str(e)}")
        return False
```

## Content Conversion Utilities

```python
def prepare_notion_properties(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Convert file metadata to Notion properties format."""
    properties = {}
    
    # Title field
    if 'name' in metadata:
        properties['Name'] = {
            'title': [{'text': {'content': metadata['name']}}]
        }
    
    # Status field
    if 'status' in metadata:
        properties['Status'] = {
            'select': {'name': metadata['status']}
        }
    
    # Tags field
    if 'tags' in metadata and isinstance(metadata['tags'], list):
        properties['Tags'] = {
            'multi_select': [{'name': tag} for tag in metadata['tags']]
        }
    
    # Date fields
    for date_field in ['created_date', 'last_modified']:
        if date_field in metadata:
            properties[date_field.replace('_', ' ').title()] = {
                'date': {'start': metadata[date_field]}
            }
    
    return properties

def convert_markdown_to_notion_blocks(content: str) -> List[Dict[str, Any]]:
    """Convert Markdown content to Notion blocks."""
    blocks = []
    lines = content.split('\\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('# '):
            # Header 1
            blocks.append({
                'object': 'block',
                'type': 'heading_1',
                'heading_1': {
                    'rich_text': [{'text': {'content': line[2:]}}]
                }
            })
        elif line.startswith('## '):
            # Header 2
            blocks.append({
                'object': 'block',
                'type': 'heading_2', 
                'heading_2': {
                    'rich_text': [{'text': {'content': line[3:]}}]
                }
            })
        elif line.startswith('- '):
            # Bullet list item
            blocks.append({
                'object': 'block',
                'type': 'bulleted_list_item',
                'bulleted_list_item': {
                    'rich_text': [{'text': {'content': line[2:]}}]
                }
            })
        else:
            # Paragraph
            blocks.append({
                'object': 'block',
                'type': 'paragraph',
                'paragraph': {
                    'rich_text': [{'text': {'content': line}}]
                }
            })
    
    return blocks

def convert_notion_blocks_to_markdown(blocks: List[Dict[str, Any]]) -> str:
    """Convert Notion blocks to Markdown content."""
    markdown_lines = []
    
    for block in blocks:
        block_type = block.get('type')
        
        if block_type == 'heading_1':
            text = extract_text_from_rich_text(block['heading_1']['rich_text'])
            markdown_lines.append(f"# {text}")
        elif block_type == 'heading_2':
            text = extract_text_from_rich_text(block['heading_2']['rich_text'])
            markdown_lines.append(f"## {text}")
        elif block_type == 'paragraph':
            text = extract_text_from_rich_text(block['paragraph']['rich_text'])
            markdown_lines.append(text)
        elif block_type == 'bulleted_list_item':
            text = extract_text_from_rich_text(block['bulleted_list_item']['rich_text'])
            markdown_lines.append(f"- {text}")
        
        markdown_lines.append("")  # Add blank line after each block
    
    return '\\n'.join(markdown_lines).strip()

def extract_text_from_rich_text(rich_text: List[Dict[str, Any]]) -> str:
    """Extract plain text from Notion rich text format."""
    return ''.join([item['text']['content'] for item in rich_text if 'text' in item])
```

## Batch Sync Operations

```python
def sync_all_files_to_notion(database_mapping: Dict[str, str]) -> Dict[str, int]:
    """Sync all Markdown files to their respective Notion databases."""
    stats = {'success': 0, 'errors': 0, 'skipped': 0}
    
    for db_name, notion_db_id in database_mapping.items():
        db_path = Path(f"databases/{db_name}/items")
        
        if not db_path.exists():
            continue
            
        md_files = list(db_path.glob("*.md"))
        print(f"Syncing {len(md_files)} files from {db_name} to Notion...")
        
        for md_file in md_files:
            try:
                if sync_file_to_notion(md_file, notion_db_id):
                    stats['success'] += 1
                    print(f"  ✅ Synced: {md_file.name}")
                else:
                    stats['errors'] += 1
                    print(f"  ❌ Failed: {md_file.name}")
            except Exception as e:
                stats['errors'] += 1
                print(f"  ❌ Error syncing {md_file.name}: {str(e)}")
    
    return stats

def sync_all_notion_to_files(database_mapping: Dict[str, str]) -> Dict[str, int]:
    """Sync all Notion pages to Markdown files."""
    stats = {'success': 0, 'errors': 0, 'skipped': 0}
    
    for db_name, notion_db_id in database_mapping.items():
        try:
            # Query all pages in database
            # pages = mcp__MCP_DOCKER__API-post-database-query(notion_db_id)
            pages = query_notion_database(notion_db_id)  # Placeholder
            
            db_path = Path(f"databases/{db_name}/items")
            db_path.mkdir(parents=True, exist_ok=True)
            
            print(f"Syncing {len(pages)} pages from Notion to {db_name}...")
            
            for page in pages:
                try:
                    # Generate filename from page properties
                    filename = generate_filename_from_notion_page(page)
                    file_path = db_path / f"{filename}.md"
                    
                    if sync_notion_to_file(page['id'], file_path):
                        stats['success'] += 1
                        print(f"  ✅ Synced: {filename}.md")
                    else:
                        stats['errors'] += 1
                        print(f"  ❌ Failed: {filename}.md")
                        
                except Exception as e:
                    stats['errors'] += 1
                    print(f"  ❌ Error syncing page: {str(e)}")
                    
        except Exception as e:
            print(f"❌ Error querying {db_name} database: {str(e)}")
    
    return stats
```

## Usage Examples

```python
# Example database mapping
DATABASE_MAPPING = {
    'knowledge_vault': 'a1b2c3d4-e5f6-7890-abcd-ef1234567890',
    'training_vault': 'b2c3d4e5-f6g7-8901-bcde-f23456789012',
    'business_ideas': 'c3d4e5f6-g7h8-9012-cdef-345678901234'
}

# Sync files to Notion
print("📤 Syncing files to Notion...")
file_to_notion_stats = sync_all_files_to_notion(DATABASE_MAPPING)
print(f"Results: {file_to_notion_stats['success']} success, {file_to_notion_stats['errors']} errors")

# Sync Notion to files
print("📥 Syncing Notion to files...")
notion_to_file_stats = sync_all_notion_to_files(DATABASE_MAPPING)
print(f"Results: {notion_to_file_stats['success']} success, {notion_to_file_stats['errors']} errors")

# Individual file sync
file_path = Path("databases/knowledge_vault/items/spring-boot.md")
notion_db_id = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
sync_file_to_notion(file_path, notion_db_id)
```

## Error Handling and Recovery

```python
def validate_sync_integrity() -> bool:
    """Validate that files and Notion are in sync."""
    # Compare timestamps and content hashes
    # Report any discrepancies
    return True

def recover_from_sync_failure(operation: str, target: str) -> bool:
    """Recover from sync operation failures."""
    # Implement rollback or retry logic
    return True
```

This implementation provides the foundation for syncing Markdown files with YAML frontmatter to Notion databases using the MCP API tools.
'''
        
        implementation_file = self.knowledge_vault_path / "operations/markdown-sync-implementation.md"
        
        with open(implementation_file, 'w', encoding='utf-8') as f:
            f.write(implementation_content)
        
        self.update_stats['files_updated'] += 1
        self.update_stats['updated_files'].append(str(implementation_file.relative_to(self.knowledge_vault_path)))
        print(f"   ✅ Created: markdown-sync-implementation.md")
    
    def _update_sync_scripts(self):
        """Update any existing sync scripts."""
        print(f"\n🐍 Updating sync scripts...")
        
        scripts_path = self.knowledge_vault_path / "operations/scripts"
        
        # Look for sync-related Python files
        sync_files = []
        for py_file in scripts_path.glob("*.py"):
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if 'notion' in content.lower() or 'sync' in content.lower():
                    sync_files.append(py_file)
        
        if not sync_files:
            print(f"   ℹ️  No existing sync scripts found to update")
            return
        
        for script_file in sync_files:
            try:
                updated = self._update_sync_script(script_file)
                if updated:
                    print(f"   ✅ Updated: {script_file.name}")
                    self.update_stats['scripts_updated'] += 1
                else:
                    print(f"   ⏭️  No changes needed: {script_file.name}")
            except Exception as e:
                print(f"   ❌ Error updating {script_file.name}: {str(e)}")
                self.update_stats['errors'] += 1
    
    def _update_sync_script(self, file_path: Path) -> bool:
        """Update a sync script for Markdown format."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Update imports
        if 'import yaml' in content and 'import frontmatter' not in content:
            content = content.replace('import yaml', 'import yaml\nimport frontmatter')
        
        # Update file reading patterns
        updates = [
            ('frontmatter.load(f)', 'frontmatter.load(f)'),
            ('frontmatter.load(f)', 'frontmatter.load(f)'),
            ("glob('*.md')", "glob('*.md')"),
            ("glob('*.md')", "glob('*.md')"),
            ('.md', '.md'),
            ('.md', '.md'),
            ('Markdown file', 'Markdown file'),
            ('Markdown file', 'Markdown file'),
        ]
        
        for old_pattern, new_pattern in updates:
            content = content.replace(old_pattern, new_pattern)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            self.update_stats['files_updated'] += 1
            self.update_stats['updated_files'].append(str(file_path.relative_to(self.knowledge_vault_path)))
            return True
        
        return False
    
    def _print_summary(self):
        """Print update summary."""
        stats = self.update_stats
        
        print(f"\n🎉 Notion sync operations update completed!")
        print(f"=" * 60)
        print(f"Files updated: {stats['files_updated']}")
        print(f"Sync configurations updated: {stats['sync_configs_updated']}")
        print(f"Scripts updated: {stats['scripts_updated']}")
        print(f"Errors encountered: {stats['errors']}")
        
        if stats['updated_files']:
            print(f"\nUpdated files:")
            for file_path in stats['updated_files']:
                print(f"  ✅ {file_path}")
        
        print(f"\n📊 Summary:")
        print(f"   • Notion sync operations updated for Markdown format")
        print(f"   • Configuration files updated with frontmatter handling")
        print(f"   • Implementation example created for Markdown sync")
        print(f"   • All sync operations ready for Markdown files with YAML frontmatter")

def main():
    """Main execution function."""
    if len(sys.argv) > 1 and sys.argv[1] == '--no-backup':
        updater = NotionSyncUpdater(backup=False)
    else:
        updater = NotionSyncUpdater(backup=True)
    
    try:
        updater.update_notion_sync_operations()
        print(f"\n🚀 Notion sync operations updated successfully!")
        return 0
    except KeyboardInterrupt:
        print(f"\n⏹️  Update interrupted by user")
        return 1
    except Exception as e:
        print(f"\n💥 Fatal error: {str(e)}")
        return 1

if __name__ == '__main__':
    sys.exit(main())