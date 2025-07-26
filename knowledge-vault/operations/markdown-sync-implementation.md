# Knowledge Vault Notion Sync - Markdown Implementation

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
    lines = content.split('\n')
    
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
    
    return '\n'.join(markdown_lines).strip()

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
