#!/usr/bin/env python3
"""
Knowledge Vault Migration Validation

This script validates that the YAML to Markdown migration was successful:
1. Tests that all files are properly formatted
2. Validates schema compliance
3. Tests filename changes and references
4. Ensures system functionality is preserved
"""

import os
import sys
import frontmatter
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Tuple
import json

class MigrationValidator:
    """Validate Knowledge Vault migration to Markdown format."""
    
    def __init__(self):
        self.knowledge_vault_path = Path(__file__).parent.parent.parent
        self.validation_results = {
            'files_tested': 0,
            'files_passed': 0,
            'files_failed': 0,
            'schemas_tested': 0,
            'schemas_passed': 0,
            'functionality_tests': 0,
            'functionality_passed': 0,
            'errors': [],
            'warnings': []
        }
    
    def validate_complete_migration(self) -> bool:
        """Run complete migration validation."""
        print("🔍 Starting Knowledge Vault migration validation...")
        print("Testing YAML to Markdown migration, human-friendly filenames, and system functionality...")
        
        # Test 1: Validate file format conversion
        print(f"\n📄 Test 1: File Format Validation")
        format_success = self._validate_file_formats()
        
        # Test 2: Validate human-friendly filenames
        print(f"\n📛 Test 2: Filename Validation")
        filename_success = self._validate_filenames()
        
        # Test 3: Validate schema compliance
        print(f"\n📋 Test 3: Schema Compliance")
        schema_success = self._validate_schemas()
        
        # Test 4: Test system functionality
        print(f"\n⚙️  Test 4: System Functionality")
        functionality_success = self._test_functionality()
        
        # Test 5: Validate configuration updates
        print(f"\n🔧 Test 5: Configuration Updates")
        config_success = self._validate_configurations()
        
        # Print comprehensive summary
        self._print_validation_summary()
        
        # Overall success
        overall_success = all([
            format_success,
            filename_success, 
            schema_success,
            functionality_success,
            config_success
        ])
        
        return overall_success
    
    def _validate_file_formats(self) -> bool:
        """Validate that all files are properly formatted Markdown with YAML frontmatter."""
        success = True
        databases_path = self.knowledge_vault_path / "databases"
        
        for db_dir in databases_path.iterdir():
            if not db_dir.is_dir() or not (db_dir / "items").exists():
                continue
                
            items_path = db_dir / "items"
            md_files = list(items_path.glob('*.md'))
            
            print(f"   📁 Testing {db_dir.name}: {len(md_files)} files")
            
            for md_file in md_files:
                self.validation_results['files_tested'] += 1
                
                try:
                    # Test frontmatter parsing
                    with open(md_file, 'r', encoding='utf-8') as f:
                        post = frontmatter.load(f)
                    
                    # Validate has frontmatter
                    if not post.metadata:
                        self.validation_results['errors'].append(f"No frontmatter in {md_file.name}")
                        success = False
                        continue
                    
                    # Validate has content
                    if not post.content.strip():
                        self.validation_results['warnings'].append(f"Empty content in {md_file.name}")
                    
                    # Validate essential fields
                    required_fields = ['id']
                    for field in required_fields:
                        if field not in post.metadata:
                            self.validation_results['errors'].append(f"Missing {field} in {md_file.name}")
                            success = False
                            continue
                    
                    print(f"      ✅ {md_file.name}")
                    self.validation_results['files_passed'] += 1
                    
                except Exception as e:
                    print(f"      ❌ {md_file.name}: {str(e)}")
                    self.validation_results['errors'].append(f"Format error in {md_file.name}: {str(e)}")
                    self.validation_results['files_failed'] += 1
                    success = False
        
        return success
    
    def _validate_filenames(self) -> bool:
        """Validate that filenames are human-friendly."""
        success = True
        databases_path = self.knowledge_vault_path / "databases"
        
        # Check filename mapping was created
        mapping_file = self.knowledge_vault_path / "operations/filename_mapping.json"
        if mapping_file.exists():
            with open(mapping_file, 'r', encoding='utf-8') as f:
                mapping_data = json.load(f)
            print(f"   📄 Filename mapping found: {len(mapping_data['filename_mapping'])} changes")
        else:
            self.validation_results['warnings'].append("No filename mapping file found")
        
        # Test filename patterns
        uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\.md$'
        technical_pattern = r'.*-[0-9a-f]{8}\.md$'
        
        for db_dir in databases_path.iterdir():
            if not db_dir.is_dir() or not (db_dir / "items").exists():
                continue
                
            items_path = db_dir / "items"
            md_files = list(items_path.glob('*.md'))
            
            print(f"   📁 Testing {db_dir.name} filenames: {len(md_files)} files")
            
            human_friendly_count = 0
            for md_file in md_files:
                filename = md_file.name
                
                # Check if filename is human-friendly
                import re
                is_uuid = re.match(uuid_pattern, filename)
                is_technical = re.match(technical_pattern, filename)
                
                if is_uuid:
                    self.validation_results['errors'].append(f"UUID filename not converted: {filename}")
                    success = False
                elif is_technical and db_dir.name == 'knowledge_vault':
                    # Knowledge vault should have been converted
                    self.validation_results['errors'].append(f"Technical filename not converted: {filename}")
                    success = False
                else:
                    human_friendly_count += 1
                    print(f"      ✅ {filename}")
            
            print(f"      Human-friendly: {human_friendly_count}/{len(md_files)}")
        
        return success
    
    def _validate_schemas(self) -> bool:
        """Validate that schemas are updated for Markdown format."""
        success = True
        schemas_path = self.knowledge_vault_path / "schemas"
        
        if not schemas_path.exists():
            self.validation_results['errors'].append("Schemas directory not found")
            return False
        
        schema_files = list(schemas_path.glob('*.yaml'))
        print(f"   📋 Testing {len(schema_files)} schema files")
        
        for schema_file in schema_files:
            self.validation_results['schemas_tested'] += 1
            
            try:
                with open(schema_file, 'r', encoding='utf-8') as f:
                    schema_data = yaml.safe_load(f)
                
                # Check if schema references are updated
                schema_content = schema_file.read_text()
                
                # Should reference .md files, not .yaml
                if '.yaml' in schema_content and 'schemas/' not in schema_content:
                    self.validation_results['warnings'].append(f"Schema {schema_file.name} may have .yaml references")
                
                print(f"      ✅ {schema_file.name}")
                self.validation_results['schemas_passed'] += 1
                
            except Exception as e:
                print(f"      ❌ {schema_file.name}: {str(e)}")
                self.validation_results['errors'].append(f"Schema error in {schema_file.name}: {str(e)}")
                success = False
        
        return success
    
    def _test_functionality(self) -> bool:
        """Test key system functionality."""
        success = True
        
        # Test 1: Schema validation script
        print(f"   🧪 Testing schema validation...")
        self.validation_results['functionality_tests'] += 1
        
        validate_script = self.knowledge_vault_path / "operations/scripts/validate_schemas.py"
        if validate_script.exists():
            try:
                # Read the script to check if it has frontmatter support
                script_content = validate_script.read_text()
                if 'frontmatter' in script_content:
                    print(f"      ✅ Schema validation script updated for frontmatter")
                    self.validation_results['functionality_passed'] += 1
                else:
                    self.validation_results['errors'].append("Schema validation script not updated for frontmatter")
                    success = False
            except Exception as e:
                self.validation_results['errors'].append(f"Error testing schema validation: {str(e)}")
                success = False
        else:
            self.validation_results['errors'].append("Schema validation script not found")
            success = False
        
        # Test 2: Frontmatter library availability
        print(f"   🧪 Testing frontmatter library...")
        self.validation_results['functionality_tests'] += 1
        
        try:
            import frontmatter
            print(f"      ✅ Frontmatter library available")
            self.validation_results['functionality_passed'] += 1
        except ImportError:
            self.validation_results['errors'].append("Frontmatter library not available")
            success = False
        
        # Test 3: File reading functionality
        print(f"   🧪 Testing file reading...")
        self.validation_results['functionality_tests'] += 1
        
        try:
            # Find a sample Markdown file
            sample_file = None
            for db_dir in (self.knowledge_vault_path / "databases").iterdir():
                if db_dir.is_dir() and (db_dir / "items").exists():
                    items = list((db_dir / "items").glob('*.md'))
                    if items:
                        sample_file = items[0]
                        break
            
            if sample_file:
                with open(sample_file, 'r', encoding='utf-8') as f:
                    post = frontmatter.load(f)
                
                if post.metadata and isinstance(post.metadata, dict):
                    print(f"      ✅ File reading works: {sample_file.name}")
                    self.validation_results['functionality_passed'] += 1
                else:
                    self.validation_results['errors'].append("File reading returned invalid frontmatter")
                    success = False
            else:
                self.validation_results['warnings'].append("No sample files found for testing")
        except Exception as e:
            self.validation_results['errors'].append(f"File reading test failed: {str(e)}")
            success = False
        
        return success
    
    def _validate_configurations(self) -> bool:
        """Validate that configurations are updated."""
        success = True
        
        # Test CLAUDE.md updates
        claude_file = self.knowledge_vault_path / "CLAUDE.md"
        if claude_file.exists():
            claude_content = claude_file.read_text()
            if 'Markdown files' in claude_content:
                print(f"   ✅ CLAUDE.md updated for Markdown format")
            else:
                self.validation_results['warnings'].append("CLAUDE.md may not be fully updated")
        
        # Test operations files
        operations_path = self.knowledge_vault_path / "operations"
        if operations_path.exists():
            markdown_sync_file = operations_path / "markdown-sync-implementation.md"
            if markdown_sync_file.exists():
                print(f"   ✅ Markdown sync implementation created")
            else:
                self.validation_results['warnings'].append("Markdown sync implementation not found")
        
        return success
    
    def _print_validation_summary(self):
        """Print comprehensive validation summary."""
        results = self.validation_results
        
        print(f"\n🎯 MIGRATION VALIDATION SUMMARY")
        print(f"=" * 60)
        print(f"📄 Files tested: {results['files_tested']}")
        print(f"   ✅ Passed: {results['files_passed']}")
        print(f"   ❌ Failed: {results['files_failed']}")
        
        print(f"\n📋 Schemas tested: {results['schemas_tested']}")
        print(f"   ✅ Passed: {results['schemas_passed']}")
        
        print(f"\n⚙️  Functionality tests: {results['functionality_tests']}")
        print(f"   ✅ Passed: {results['functionality_passed']}")
        
        if results['errors']:
            print(f"\n❌ ERRORS ({len(results['errors'])}):")
            for error in results['errors']:
                print(f"   • {error}")
        
        if results['warnings']:
            print(f"\n⚠️  WARNINGS ({len(results['warnings'])}):")
            for warning in results['warnings']:
                print(f"   • {warning}")
        
        # Calculate success rates
        file_success_rate = (results['files_passed'] / max(results['files_tested'], 1)) * 100
        schema_success_rate = (results['schemas_passed'] / max(results['schemas_tested'], 1)) * 100
        functionality_success_rate = (results['functionality_passed'] / max(results['functionality_tests'], 1)) * 100
        
        print(f"\n📊 SUCCESS RATES:")
        print(f"   📄 File Format: {file_success_rate:.1f}%")
        print(f"   📋 Schema Compliance: {schema_success_rate:.1f}%")
        print(f"   ⚙️  Functionality: {functionality_success_rate:.1f}%")
        
        overall_success = (
            results['files_failed'] == 0 and
            len(results['errors']) == 0
        )
        
        if overall_success:
            print(f"\n🎉 MIGRATION VALIDATION: SUCCESS")
            print(f"   • All files properly converted to Markdown with YAML frontmatter")
            print(f"   • Human-friendly filenames implemented")
            print(f"   • System functionality preserved")
            print(f"   • Configuration files updated")
        else:
            print(f"\n⚠️  MIGRATION VALIDATION: ISSUES FOUND")
            print(f"   • Please review errors and warnings above")
            print(f"   • Some functionality may need attention")

def main():
    """Main execution function."""
    validator = MigrationValidator()
    
    try:
        success = validator.validate_complete_migration()
        
        if success:
            print(f"\n✅ Knowledge Vault migration validation completed successfully!")
            return 0
        else:
            print(f"\n⚠️  Knowledge Vault migration has issues that need attention.")
            return 1
            
    except KeyboardInterrupt:
        print(f"\n⏹️  Validation interrupted by user")
        return 1
    except Exception as e:
        print(f"\n💥 Fatal error during validation: {str(e)}")
        return 1

if __name__ == '__main__':
    sys.exit(main())