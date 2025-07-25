#!/usr/bin/env python3
"""
Knowledge Vault Filename Standardizer

This script converts non-human-friendly filenames (UUIDs, technical IDs) to 
human-readable kebab-case filenames based on the content's name or title field.
"""

import os
import sys
import yaml
import frontmatter
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Tuple
import shutil
import re
import json

class FilenameStandardizer:
    """Convert Knowledge Vault files to human-friendly filenames."""
    
    def __init__(self, backup=True):
        self.backup = backup
        self.knowledge_vault_path = Path(__file__).parent.parent.parent
        self.standardization_stats = {
            'converted': 0,
            'skipped': 0,
            'errors': 0,
            'databases': {},
            'mapping': {}  # Track old_filename -> new_filename
        }
        self.filename_conflicts = {}  # Track conflicts and resolution
    
    def standardize_all_filenames(self):
        """Standardize filenames in all databases."""
        print("🚀 Starting Knowledge Vault filename standardization...")
        print("Converting UUIDs and technical IDs to human-readable names...")
        
        if self.backup:
            self._create_backup()
        
        databases_path = self.knowledge_vault_path / "databases"
        
        for db_dir in databases_path.iterdir():
            if db_dir.is_dir() and (db_dir / "items").exists():
                self._standardize_database(db_dir)
        
        self._save_filename_mapping()
        self._print_summary()
    
    def _create_backup(self):
        """Create backup of entire databases folder."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.knowledge_vault_path / f"backups/filename_backup_{timestamp}"
        
        print(f"📦 Creating backup at: {backup_path}")
        
        # Create backups directory if it doesn't exist
        backup_path.parent.mkdir(exist_ok=True)
        
        # Copy entire databases folder
        shutil.copytree(
            self.knowledge_vault_path / "databases",
            backup_path,
            ignore=shutil.ignore_patterns('*.pyc', '__pycache__', '.DS_Store')
        )
        
        print(f"✅ Backup created successfully")
    
    def _standardize_database(self, db_path: Path):
        """Standardize filenames in a specific database."""
        db_name = db_path.name
        items_path = db_path / "items"
        
        print(f"\n📁 Standardizing database: {db_name}")
        
        if db_name not in self.standardization_stats['databases']:
            self.standardization_stats['databases'][db_name] = {
                'converted': 0,
                'skipped': 0,
                'errors': 0
            }
        
        md_files = list(items_path.glob('*.md'))
        print(f"   Found {len(md_files)} Markdown files")
        
        for md_file in md_files:
            try:
                # Skip if filename is already human-friendly
                if self._is_filename_human_friendly(md_file.name):
                    print(f"   ⏭️  Skipping {md_file.name} (already human-friendly)")
                    self.standardization_stats['skipped'] += 1
                    self.standardization_stats['databases'][db_name]['skipped'] += 1
                    continue
                
                new_filename = self._generate_human_friendly_filename(md_file)
                
                if new_filename and new_filename != md_file.name:
                    new_path = md_file.parent / new_filename
                    
                    # Handle filename conflicts
                    if new_path.exists():
                        new_filename = self._resolve_filename_conflict(new_filename, md_file.parent)
                        new_path = md_file.parent / new_filename
                    
                    # Rename the file
                    md_file.rename(new_path)
                    
                    # Track the mapping
                    self.standardization_stats['mapping'][str(md_file.relative_to(self.knowledge_vault_path))] = str(new_path.relative_to(self.knowledge_vault_path))
                    
                    print(f"   ✅ {md_file.name} → {new_filename}")
                    self.standardization_stats['converted'] += 1
                    self.standardization_stats['databases'][db_name]['converted'] += 1
                else:
                    print(f"   ⏭️  Skipping {md_file.name} (no name/title found)")
                    self.standardization_stats['skipped'] += 1
                    self.standardization_stats['databases'][db_name]['skipped'] += 1
                    
            except Exception as e:
                print(f"   ❌ Error processing {md_file.name}: {str(e)}")
                self.standardization_stats['errors'] += 1
                self.standardization_stats['databases'][db_name]['errors'] += 1
    
    def _is_filename_human_friendly(self, filename: str) -> bool:
        """Check if filename is already human-friendly."""
        # Remove .md extension for checking
        name_without_ext = filename.replace('.md', '')
        
        # Check if it's a UUID pattern
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
        if re.match(uuid_pattern, name_without_ext):
            return False
        
        # Check if it has technical suffix pattern (like -1f5f8374)
        technical_suffix_pattern = r'.*-[0-9a-f]{8}$'
        if re.match(technical_suffix_pattern, name_without_ext):
            return False
        
        # If it contains meaningful words and doesn't match technical patterns, consider it human-friendly
        # Examples of good names: "github-mcp-maritime-intelligence", "spring-boot", "human-resources"
        has_meaningful_words = len(name_without_ext.split('-')) > 1 or len(name_without_ext) > 8
        
        return has_meaningful_words
    
    def _generate_human_friendly_filename(self, md_file: Path) -> str:
        """Generate human-friendly filename from content."""
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
            
            # Try to get name or title from frontmatter
            content_name = None
            
            # Priority order: title, name, description (if short)
            if 'title' in post.metadata:
                content_name = post.metadata['title']
            elif 'name' in post.metadata:
                content_name = post.metadata['name']
            elif 'description' in post.metadata:
                desc = str(post.metadata['description']).strip()
                # Use description if it's short and descriptive
                if desc and len(desc) < 50 and not desc.lower().startswith('null'):
                    content_name = desc
            
            if content_name:
                # Convert to kebab-case
                return self._to_kebab_case(content_name) + '.md'
            
            # If no name/title found, try to extract from content
            content_lines = post.content.strip().split('\n')
            for line in content_lines:
                if line.startswith('# '):
                    header_name = line[2:].strip()
                    if header_name and header_name != 'Knowledge Item':
                        return self._to_kebab_case(header_name) + '.md'
            
            # Last resort: generate name based on database and context
            database_name = md_file.parent.parent.name
            return self._generate_fallback_filename(database_name, post.metadata)
            
        except Exception as e:
            print(f"   ❌ Error reading {md_file.name}: {str(e)}")
            return None
    
    def _generate_fallback_filename(self, database_name: str, metadata: dict) -> str:
        """Generate fallback filename based on database type and available metadata."""
        # Try to use any identifying information
        if 'id' in metadata:
            # Use database name + shortened id for better readability
            short_id = str(metadata['id'])[:8]  # First 8 characters
            return f"{database_name}-item-{short_id}.md"
        
        # Generic fallback
        return f"{database_name}-knowledge-item.md"
    
    def _to_kebab_case(self, text: str) -> str:
        """Convert text to kebab-case filename."""
        # Remove or replace special characters
        text = str(text).strip()
        
        # Replace common separators and spaces with hyphens
        text = re.sub(r'[\/\\\s\|]+', '-', text)
        
        # Remove special characters except hyphens and alphanumeric
        text = re.sub(r'[^\w\-]', '', text)
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove multiple consecutive hyphens
        text = re.sub(r'-+', '-', text)
        
        # Remove leading/trailing hyphens
        text = text.strip('-')
        
        # Limit length to reasonable filename length
        if len(text) > 50:
            text = text[:50].rstrip('-')
        
        # Ensure it's not empty
        if not text:
            text = 'knowledge-item'
        
        return text
    
    def _resolve_filename_conflict(self, filename: str, directory: Path) -> str:
        """Resolve filename conflicts by adding numeric suffix."""
        base_name = filename.replace('.md', '')
        counter = 1
        
        while True:
            new_filename = f"{base_name}-{counter}.md"
            new_path = directory / new_filename
            
            if not new_path.exists():
                # Track the conflict resolution
                if filename not in self.filename_conflicts:
                    self.filename_conflicts[filename] = []
                self.filename_conflicts[filename].append(new_filename)
                
                print(f"   ⚠️  Filename conflict resolved: {filename} → {new_filename}")
                return new_filename
            
            counter += 1
            if counter > 100:  # Safety check
                return f"{base_name}-{datetime.now().strftime('%H%M%S')}.md"
    
    def _save_filename_mapping(self):
        """Save filename mapping to JSON file for reference."""
        mapping_file = self.knowledge_vault_path / "operations/filename_mapping.json"
        
        mapping_data = {
            'timestamp': datetime.now().isoformat(),
            'total_files_converted': self.standardization_stats['converted'],
            'filename_mapping': self.standardization_stats['mapping'],
            'filename_conflicts': self.filename_conflicts
        }
        
        with open(mapping_file, 'w', encoding='utf-8') as f:
            json.dump(mapping_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Filename mapping saved to: {mapping_file}")
    
    def _print_summary(self):
        """Print conversion summary."""
        stats = self.standardization_stats
        
        print(f"\n🎉 Filename standardization completed!")
        print(f"=" * 60)
        print(f"Total files processed: {stats['converted'] + stats['skipped'] + stats['errors']}")
        print(f"✅ Files converted: {stats['converted']}")
        print(f"⏭️  Files skipped: {stats['skipped']}")
        print(f"❌ Errors: {stats['errors']}")
        
        print(f"\nDatabase breakdown:")
        for db_name, db_stats in stats['databases'].items():
            total = db_stats['converted'] + db_stats['skipped'] + db_stats['errors']
            print(f"  📁 {db_name}: {total} files ({db_stats['converted']} converted, {db_stats['skipped']} skipped, {db_stats['errors']} errors)")
        
        if self.filename_conflicts:
            print(f"\n⚠️  Filename conflicts resolved: {len(self.filename_conflicts)}")
            for original, conflicts in self.filename_conflicts.items():
                print(f"     {original} → {', '.join(conflicts)}")
        
        print(f"\n📊 Summary:")
        print(f"   • All files now have human-readable names")
        print(f"   • Filename mapping saved for reference")
        print(f"   • Backup created before changes")
        print(f"   • Ready for system configuration updates")

def main():
    """Main execution function."""
    if len(sys.argv) > 1 and sys.argv[1] == '--no-backup':
        converter = FilenameStandardizer(backup=False)
    else:
        converter = FilenameStandardizer(backup=True)
    
    try:
        converter.standardize_all_filenames()
        print(f"\n🚀 Knowledge Vault filenames are now human-friendly!")
        return 0
    except KeyboardInterrupt:
        print(f"\n⏹️  Standardization interrupted by user")
        return 1
    except Exception as e:
        print(f"\n💥 Fatal error: {str(e)}")
        return 1

if __name__ == '__main__':
    sys.exit(main())