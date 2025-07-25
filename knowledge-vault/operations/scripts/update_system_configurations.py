#!/usr/bin/env python3
"""
Knowledge Vault System Configuration Updater

This script updates system configurations to reflect the migration from YAML to Markdown:
1. Updates file extension references from .yaml to .md
2. Updates any hardcoded filename references
3. Ensures all scripts work with the new Markdown format
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Tuple
import shutil
import json

class SystemConfigUpdater:
    """Update system configurations for YAML to Markdown migration."""
    
    def __init__(self, backup=True):
        self.backup = backup
        self.knowledge_vault_path = Path(__file__).parent.parent.parent
        self.update_stats = {
            'files_updated': 0,
            'extensions_changed': 0,
            'patterns_updated': 0,
            'errors': 0,
            'updated_files': []
        }
        
        # Load filename mapping from previous conversion
        self.filename_mapping = self._load_filename_mapping()
    
    def update_all_configurations(self):
        """Update all system configurations."""
        print("🔧 Starting Knowledge Vault system configuration updates...")
        print("Updating file extensions and references for Markdown migration...")
        
        if self.backup:
            self._create_backup()
        
        # Update Python scripts
        self._update_python_scripts()
        
        # Update configuration files
        self._update_config_files()
        
        # Update documentation
        self._update_documentation_files()
        
        self._print_summary()
    
    def _load_filename_mapping(self) -> Dict[str, str]:
        """Load filename mapping from previous conversion."""
        mapping_file = self.knowledge_vault_path / "operations/filename_mapping.json"
        
        if mapping_file.exists():
            with open(mapping_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('filename_mapping', {})
        
        return {}
    
    def _create_backup(self):
        """Create backup of configuration files."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.knowledge_vault_path / f"backups/config_backup_{timestamp}"
        
        print(f"📦 Creating backup at: {backup_path}")
        
        # Create backups directory if it doesn't exist
        backup_path.mkdir(parents=True, exist_ok=True)
        
        # Backup key directories
        for dir_name in ['operations', 'core', 'schemas', 'shared']:
            source_dir = self.knowledge_vault_path / dir_name
            if source_dir.exists():
                shutil.copytree(
                    source_dir,
                    backup_path / dir_name,
                    ignore=shutil.ignore_patterns('*.pyc', '__pycache__', '.DS_Store', 'venv')
                )
        
        print(f"✅ Configuration backup created successfully")
    
    def _update_python_scripts(self):
        """Update Python scripts to handle Markdown format."""
        print(f"\n🐍 Updating Python scripts...")
        
        scripts_path = self.knowledge_vault_path / "operations/scripts"
        py_files = list(scripts_path.glob('*.py'))
        
        for py_file in py_files:
            try:
                updated = self._update_python_file(py_file)
                if updated:
                    self.update_stats['files_updated'] += 1
                    self.update_stats['updated_files'].append(str(py_file.relative_to(self.knowledge_vault_path)))
                    print(f"   ✅ Updated: {py_file.name}")
                else:
                    print(f"   ⏭️  No changes needed: {py_file.name}")
            except Exception as e:
                print(f"   ❌ Error updating {py_file.name}: {str(e)}")
                self.update_stats['errors'] += 1
    
    def _update_python_file(self, file_path: Path) -> bool:
        """Update a single Python file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Update glob patterns for Markdown files to include Markdown
        patterns_to_update = [
            # Update glob patterns
            (r"\.glob\('?\*\.yaml'?\)", r".glob('*.md')"),
            (r"\.glob\('?\*\.yml'?\)", r".glob('*.md')"),
            (r"glob\('?\*\.yaml'?\)", r"glob('*.md')"),
            (r"glob\('?\*\.yml'?\)", r"glob('*.md')"),
            
            # Update file extension checks
            (r"\.endswith\('?\.yaml'?\)", r".endswith('.md')"),
            (r"\.endswith\('?\.yml'?\)", r".endswith('.md')"),
            (r"file_path\.suffix\.lower\(\) == '?\.yaml'?", r"file_path.suffix.lower() == '.md'"),
            (r"file_path\.suffix\.lower\(\) == '?\.yml'?", r"file_path.suffix.lower() == '.md'"),
            
            # Update comments and documentation strings
            (r"Markdown files", r"Markdown files"),
            (r"Markdown files", r"Markdown files"),
            (r"\.Markdown files", r".md files"),
        ]
        
        changes_made = 0
        for pattern, replacement in patterns_to_update:
            new_content, count = re.subn(pattern, replacement, content, flags=re.IGNORECASE)
            if count > 0:
                content = new_content
                changes_made += count
                self.update_stats['patterns_updated'] += count
        
        # Special handling for validate_schemas.py - ensure it handles both YAML and MD
        if file_path.name == 'validate_schemas.py' and 'glob(\'*.md\')' in content:
            # Make sure it handles both formats during transition
            content = content.replace(
                "list(directory_path.glob('*.md'))",
                "list(directory_path.glob('*.md')) + list(directory_path.glob('*.md')) + list(directory_path.glob('*.md'))"
            )
            changes_made += 1
        
        # Update any specific filename references using the mapping
        for old_path, new_path in self.filename_mapping.items():
            old_filename = Path(old_path).name
            new_filename = Path(new_path).name
            
            if old_filename in content:
                content = content.replace(old_filename, new_filename)
                changes_made += 1
        
        if changes_made > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    
    def _update_config_files(self):
        """Update configuration Markdown files."""
        print(f"\n⚙️  Updating configuration files...")
        
        # Update files in various directories
        config_dirs = ['core', 'schemas', 'shared']
        
        for dir_name in config_dirs:
            dir_path = self.knowledge_vault_path / dir_name
            if dir_path.exists():
                yaml_files = list(dir_path.glob('*.md')) + list(dir_path.glob('*.md'))
                
                for yaml_file in yaml_files:
                    try:
                        updated = self._update_config_file(yaml_file)
                        if updated:
                            self.update_stats['files_updated'] += 1
                            self.update_stats['updated_files'].append(str(yaml_file.relative_to(self.knowledge_vault_path)))
                            print(f"   ✅ Updated: {dir_name}/{yaml_file.name}")
                        else:
                            print(f"   ⏭️  No changes needed: {dir_name}/{yaml_file.name}")
                    except Exception as e:
                        print(f"   ❌ Error updating {yaml_file.name}: {str(e)}")
                        self.update_stats['errors'] += 1
    
    def _update_config_file(self, file_path: Path) -> bool:
        """Update a single configuration file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Update file extension references
        patterns_to_update = [
            (r'\.yaml\b', r'.md'),
            (r'\.yml\b', r'.md'),
            (r'Markdown files', r'Markdown files'),
            (r'Markdown files', r'Markdown files'),
        ]
        
        changes_made = 0
        for pattern, replacement in patterns_to_update:
            new_content, count = re.subn(pattern, replacement, content, flags=re.IGNORECASE)
            if count > 0:
                content = new_content
                changes_made += count
                self.update_stats['extensions_changed'] += count
        
        # Update any specific filename references
        for old_path, new_path in self.filename_mapping.items():
            old_filename = Path(old_path).name
            new_filename = Path(new_path).name
            
            if old_filename in content:
                content = content.replace(old_filename, new_filename)
                changes_made += 1
        
        if changes_made > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    
    def _update_documentation_files(self):
        """Update documentation files."""
        print(f"\n📚 Updating documentation files...")
        
        # Update README files and other documentation
        doc_files = []
        
        # Find documentation files
        for pattern in ['**/*.md', '**/*.rst', '**/*.txt']:
            doc_files.extend(self.knowledge_vault_path.glob(pattern))
        
        # Exclude items directories and backup directories
        doc_files = [f for f in doc_files if 'items' not in f.parts and 'backup' not in f.parts and 'venv' not in f.parts]
        
        for doc_file in doc_files:
            try:
                updated = self._update_documentation_file(doc_file)
                if updated:
                    self.update_stats['files_updated'] += 1
                    self.update_stats['updated_files'].append(str(doc_file.relative_to(self.knowledge_vault_path)))
                    print(f"   ✅ Updated: {doc_file.relative_to(self.knowledge_vault_path)}")
            except Exception as e:
                print(f"   ❌ Error updating {doc_file.name}: {str(e)}")
                self.update_stats['errors'] += 1
    
    def _update_documentation_file(self, file_path: Path) -> bool:
        """Update a single documentation file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Update references to file formats
        patterns_to_update = [
            (r'YAML format', r'Markdown format with YAML frontmatter'),
            (r'\.Markdown files', r'.md files'),
            (r'\.yml files', r'.md files'),
            (r'Individual items \(Markdown files\)', r'Individual items (Markdown files)'),
        ]
        
        changes_made = 0
        for pattern, replacement in patterns_to_update:
            new_content, count = re.subn(pattern, replacement, content, flags=re.IGNORECASE)
            if count > 0:
                content = new_content
                changes_made += count
        
        # Update any specific filename references
        for old_path, new_path in self.filename_mapping.items():
            old_filename = Path(old_path).name
            new_filename = Path(new_path).name
            
            if old_filename in content:
                content = content.replace(old_filename, new_filename)
                changes_made += 1
        
        if changes_made > 0:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
    
    def _print_summary(self):
        """Print update summary."""
        stats = self.update_stats
        
        print(f"\n🎉 System configuration update completed!")
        print(f"=" * 60)
        print(f"Files updated: {stats['files_updated']}")
        print(f"Extension references changed: {stats['extensions_changed']}")
        print(f"Pattern updates made: {stats['patterns_updated']}")
        print(f"Errors encountered: {stats['errors']}")
        
        if stats['updated_files']:
            print(f"\nUpdated files:")
            for file_path in stats['updated_files']:
                print(f"  ✅ {file_path}")
        
        print(f"\n📊 Summary:")
        print(f"   • All file extension references updated (.yaml → .md)")
        print(f"   • Filename references updated with new human-friendly names")
        print(f"   • Documentation updated to reflect Markdown format")
        print(f"   • System ready for Markdown-based operations")

def main():
    """Main execution function."""
    if len(sys.argv) > 1 and sys.argv[1] == '--no-backup':
        updater = SystemConfigUpdater(backup=False)
    else:
        updater = SystemConfigUpdater(backup=True)
    
    try:
        updater.update_all_configurations()
        print(f"\n🚀 Knowledge Vault system configurations updated successfully!")
        return 0
    except KeyboardInterrupt:
        print(f"\n⏹️  Update interrupted by user")
        return 1
    except Exception as e:
        print(f"\n💥 Fatal error: {str(e)}")
        return 1

if __name__ == '__main__':
    sys.exit(main())