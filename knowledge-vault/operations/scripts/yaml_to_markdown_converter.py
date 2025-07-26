#!/usr/bin/env python3
"""
Knowledge Vault YAML to Markdown Converter

This script converts YAML knowledge vault files to Markdown with YAML frontmatter,
preserving all metadata while adding human-readable content.
"""

import os
import sys
import yaml
import frontmatter
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
import shutil
import re

class YAMLToMarkdownConverter:
    """Convert YAML knowledge vault files to Markdown with YAML frontmatter."""
    
    def __init__(self, backup=True):
        self.backup = backup
        self.knowledge_vault_path = Path(__file__).parent.parent.parent
        self.conversion_stats = {
            'converted': 0,
            'skipped': 0,
            'errors': 0,
            'databases': {}
        }
    
    def convert_all_databases(self):
        """Convert all Markdown files in all databases to Markdown format."""
        print("🚀 Starting Knowledge Vault YAML to Markdown conversion...")
        
        if self.backup:
            self._create_backup()
        
        databases_path = self.knowledge_vault_path / "databases"
        
        for db_dir in databases_path.iterdir():
            if db_dir.is_dir() and (db_dir / "items").exists():
                self._convert_database(db_dir)
        
        self._print_summary()
    
    def _create_backup(self):
        """Create backup of entire databases folder."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.knowledge_vault_path / f"backups/yaml_backup_{timestamp}"
        backup_path.mkdir(parents=True, exist_ok=True)
        
        databases_path = self.knowledge_vault_path / "databases"
        shutil.copytree(databases_path, backup_path / "databases")
        
        print(f"📦 Created backup at: {backup_path}")
    
    def _convert_database(self, db_path: Path):
        """Convert all Markdown files in a single database."""
        db_name = db_path.name
        items_path = db_path / "items"
        
        print(f"\n📁 Converting database: {db_name}")
        
        db_stats = {'converted': 0, 'skipped': 0, 'errors': 0}
        
        for yaml_file in items_path.glob("*.md"):
            # Skip hidden files (starting with .)
            if yaml_file.name.startswith('.'):
                print(f"   ⏭️  Skipping hidden file: {yaml_file.name}")
                db_stats['skipped'] += 1
                continue
                
            try:
                if self._convert_yaml_file(yaml_file):
                    db_stats['converted'] += 1
                else:
                    db_stats['skipped'] += 1
            except Exception as e:
                print(f"❌ Error converting {yaml_file.name}: {str(e)}")
                db_stats['errors'] += 1
        
        self.conversion_stats['databases'][db_name] = db_stats
        self.conversion_stats['converted'] += db_stats['converted']
        self.conversion_stats['skipped'] += db_stats['skipped']
        self.conversion_stats['errors'] += db_stats['errors']
        
        print(f"   ✅ Converted: {db_stats['converted']}")
        print(f"   ⏭️  Skipped: {db_stats['skipped']}")
        print(f"   ❌ Errors: {db_stats['errors']}")
    
    def _convert_yaml_file(self, yaml_file: Path) -> bool:
        """Convert a single Markdown file to Markdown."""
        md_file = yaml_file.with_suffix('.md')
        
        # Skip if already converted
        if md_file.exists():
            print(f"   ⏭️  Already exists: {md_file.name}")
            return False
        
        try:
            # Read Markdown file
            with open(yaml_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse YAML content
            data = self._parse_yaml_content(content)
            
            # Generate frontmatter and content
            frontmatter_data, markdown_content = self._generate_markdown_structure(data)
            
            # Create frontmatter post
            post = frontmatter.Post(markdown_content, **frontmatter_data)
            
            # Write Markdown file
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(frontmatter.dumps(post))
            
            print(f"   ✅ Converted: {yaml_file.name} → {md_file.name}")
            
            # Remove original Markdown file
            yaml_file.unlink()
            
            return True
            
        except Exception as e:
            print(f"   ❌ Failed to convert {yaml_file.name}: {str(e)}")
            raise
    
    def _parse_yaml_content(self, content: str) -> Dict[str, Any]:
        """Parse YAML content, handling comments and mixed formats."""
        # Remove comment lines but preserve structure
        lines = content.split('\n')
        yaml_lines = []
        
        for line in lines:
            # Skip pure comment lines
            if line.strip().startswith('#') and ':' not in line:
                continue
            # Remove inline comments but keep the data
            if '#' in line and ':' in line:
                line = line.split('#')[0].rstrip()
            yaml_lines.append(line)
        
        yaml_content = '\n'.join(yaml_lines)
        
        # Parse YAML
        try:
            return yaml.safe_load(yaml_content) or {}
        except yaml.YAMLError as e:
            # Fallback: try to parse as a simple key-value structure
            print(f"   ⚠️  YAML parsing issue, attempting simple parse: {str(e)}")
            return self._simple_yaml_parse(yaml_content)
    
    def _simple_yaml_parse(self, content: str) -> Dict[str, Any]:
        """Simple fallback YAML parser for problematic files."""
        data = {}
        current_section = None
        
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            if ':' in line and not line.startswith(' '):
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip().strip('"\'')
                
                if value:
                    # Try to parse as number or boolean
                    if value.lower() in ['true', 'false']:
                        data[key] = value.lower() == 'true'
                    elif value.isdigit():
                        data[key] = int(value)
                    elif value == 'null':
                        data[key] = None
                    else:
                        data[key] = value
                else:
                    current_section = key
                    data[key] = {}
            elif current_section and line.startswith('-'):
                # Handle lists
                if current_section not in data:
                    data[current_section] = []
                item = line[1:].strip().strip('"\'')
                data[current_section].append(item)
        
        return data
    
    def _generate_markdown_structure(self, data: Dict[str, Any]) -> tuple:
        """Generate frontmatter and markdown content from YAML data."""
        
        # Core fields for frontmatter
        frontmatter_data = {}
        
        # Essential fields
        essential_fields = [
            'id', 'name', 'title', 'description', 'status', 'priority', 'tags',
            'uuid', 'created_date', 'last_modified', 'source_database'
        ]
        
        for field in essential_fields:
            if field in data:
                frontmatter_data[field] = data[field]
        
        # Relationship fields
        relationship_fields = [
            'knowledge_vault_relations', 'training_vault_relations', 'tools_services_relations',
            'platforms_sites_relations', 'business_ideas_relations', 'notes_ideas_relations',
            'projects_relations', 'habits_routines_relations', 'media_vault_relations',
            'startups_relations', 'pillars_relations', 'maritime_intelligence_relations'
        ]
        
        for field in relationship_fields:
            if field in data and data[field]:
                frontmatter_data[field] = data[field]
        
        # Additional metadata
        metadata_fields = [
            'url', 'notion_url', 'public_url', 'date',
            'maritime_domain', 'business_impact', 'stakeholders', 'regulatory_frameworks',
            'risk_categories', 'generic_tool_reference'
        ]
        
        for field in metadata_fields:
            if field in data and data[field] is not None:
                frontmatter_data[field] = data[field]
        
        # Handle nested metadata
        if 'metadata' in data and isinstance(data['metadata'], dict):
            frontmatter_data['metadata'] = data['metadata']
        
        # Generate markdown content
        markdown_content = self._generate_markdown_content(data, frontmatter_data)
        
        return frontmatter_data, markdown_content
    
    def _generate_markdown_content(self, data: Dict[str, Any], frontmatter_data: Dict[str, Any]) -> str:
        """Generate human-readable markdown content."""
        
        title = data.get('name') or data.get('title') or 'Knowledge Item'
        
        content_parts = [f"# {title}"]
        
        # Description/Overview section
        description = data.get('description')
        if description:
            content_parts.extend([
                "",
                "## Overview",
                "",
                description
            ])
        
        # URL/Links section
        url = data.get('url')
        notion_url = data.get('notion_url')
        public_url = data.get('public_url')
        
        if url or notion_url or public_url:
            content_parts.extend(["", "## Links", ""])
            if url:
                content_parts.append(f"- **Official**: [{url}]({url})")
            if notion_url:
                content_parts.append(f"- **Notion**: [View in Notion]({notion_url})")
            if public_url:
                content_parts.append(f"- **Public**: [Public View]({public_url})")
        
        # Maritime-specific content (for maritime intelligence)
        if 'use_cases' in data and data['use_cases']:
            content_parts.extend([
                "",
                "## Use Cases",
                "",
                data['use_cases']
            ])
        
        if 'implementation_examples' in data and data['implementation_examples']:
            content_parts.extend([
                "",
                "## Implementation Examples",
                "",
                data['implementation_examples']
            ])
        
        if 'regulatory_considerations' in data and data['regulatory_considerations']:
            content_parts.extend([
                "",
                "## Regulatory Considerations",
                "",
                data['regulatory_considerations']
            ])
        
        if 'implementation_notes' in data and data['implementation_notes']:
            content_parts.extend([
                "",
                "## Implementation Notes",
                "",
                data['implementation_notes']
            ])
        
        if 'success_metrics' in data and data['success_metrics']:
            content_parts.extend([
                "",
                "## Success Metrics",
                "",
                data['success_metrics']
            ])
        
        # Status and Classification
        status = data.get('status')
        priority = data.get('priority')
        tags = data.get('tags', [])
        
        if status or priority or tags:
            content_parts.extend(["", "## Classification", ""])
            if status:
                content_parts.append(f"- **Status**: {status}")
            if priority:
                content_parts.append(f"- **Priority**: {priority}")
            if tags:
                tag_list = ', '.join(f"`{tag}`" for tag in tags)
                content_parts.append(f"- **Tags**: {tag_list}")
        
        # Relationships section
        relationships = self._format_relationships(data)
        if relationships:
            content_parts.extend([
                "",
                "## Related Items",
                "",
                relationships
            ])
        
        # Note: Metadata is now available in YAML frontmatter, no need for duplicate section
        
        return '\n'.join(content_parts)
    
    def _format_relationships(self, data: Dict[str, Any]) -> str:
        """Format relationship data into readable markdown."""
        relationships = []
        
        relationship_fields = {
            'knowledge_vault_relations': 'Knowledge Vault',
            'training_vault_relations': 'Training Vault',
            'tools_services_relations': 'Tools & Services',
            'platforms_sites_relations': 'Platforms & Sites',
            'business_ideas_relations': 'Business Ideas',
            'notes_ideas_relations': 'Notes & Ideas',
            'maritime_intelligence_relations': 'Maritime Intelligence'
        }
        
        for field, label in relationship_fields.items():
            if field in data and data[field]:
                relations = data[field]
                if isinstance(relations, list) and relations:
                    relationships.append(f"### {label}")
                    for relation in relations:
                        if isinstance(relation, dict) and 'id' in relation:
                            context = relation.get('context', '')
                            relationships.append(f"- `{relation['id']}` - {context}")
                        elif isinstance(relation, str):
                            relationships.append(f"- `{relation}`")
                    relationships.append("")
        
        # Handle generic tool reference
        if 'generic_tool_reference' in data and data['generic_tool_reference']:
            relationships.append("### Generic Reference")
            relationships.append(f"- {data['generic_tool_reference']}")
            relationships.append("")
        
        return '\n'.join(relationships)
    
    def _print_summary(self):
        """Print conversion summary."""
        print("\n" + "="*50)
        print("📊 CONVERSION SUMMARY")
        print("="*50)
        print(f"✅ Total Converted: {self.conversion_stats['converted']}")
        print(f"⏭️  Total Skipped: {self.conversion_stats['skipped']}")
        print(f"❌ Total Errors: {self.conversion_stats['errors']}")
        
        print("\n📁 Database Breakdown:")
        for db_name, stats in self.conversion_stats['databases'].items():
            print(f"   {db_name}:")
            print(f"      ✅ Converted: {stats['converted']}")
            print(f"      ⏭️  Skipped: {stats['skipped']}")
            print(f"      ❌ Errors: {stats['errors']}")
        
        print("\n🎉 Knowledge Vault conversion completed!")
        if self.backup:
            print("💾 Original files have been backed up")
        print("📖 Files are now human-readable Markdown with YAML frontmatter")


def main():
    """Main execution function."""
    print("Knowledge Vault YAML to Markdown Converter")
    print("==========================================")
    
    # Confirm with user
    response = input("\n⚠️  This will convert all Markdown files to Markdown. Continue? (y/N): ")
    if response.lower() != 'y':
        print("❌ Conversion cancelled.")
        sys.exit(0)
    
    # Create backup by default
    backup = input("\n💾 Create backup of original files? (Y/n): ")
    create_backup = backup.lower() != 'n'
    
    # Run conversion
    converter = YAMLToMarkdownConverter(backup=create_backup)
    converter.convert_all_databases()


if __name__ == "__main__":
    main()