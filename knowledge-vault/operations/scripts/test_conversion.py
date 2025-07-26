#!/usr/bin/env python3
"""
Test script for YAML to Markdown conversion.
Tests the conversion on a single file to validate the process.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
import frontmatter
import yaml

# Add the scripts directory to the path
sys.path.insert(0, str(Path(__file__).parent))
from yaml_to_markdown_converter import YAMLToMarkdownConverter

def test_conversion():
    """Test the conversion process on a sample file."""
    
    # Create a test YAML file
    test_yaml_content = """# Knowledge Vault Item: Test Item
# Created: 2025-01-24

metadata:
  item_type: knowledge_item
  source: test
  created_date: "2025-01-24T12:00:00.000Z"
  last_modified: "2025-01-24T12:00:00.000Z"

## 📝 Core Information

name: "Test Item"
description: "A test item for conversion validation"
url: "https://example.com"

## 🏷️ Classification & Status

status: "active"
priority: "high"
tags: ["test", "conversion"]

## 🔗 Relationship Management

knowledge_vault_relations:
  - id: "test-uuid-1"
    context: "Related test item"

tools_services_relations: []

## 📊 Metadata & Timestamps

uuid: "test-uuid-main"
created_date: "2025-01-24T12:00:00.000Z"
last_modified: "2025-01-24T12:00:00.000Z"
"""
    
    # Create a temporary directory structure
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create the database structure
        db_path = temp_path / "test_database" / "items"
        db_path.mkdir(parents=True)
        
        # Write test YAML file
        yaml_file = db_path / "test-item.yaml"
        with open(yaml_file, 'w') as f:
            f.write(test_yaml_content)
        
        print("🧪 Testing YAML to Markdown conversion...")
        print(f"📁 Test directory: {temp_path}")
        print(f"📄 Test file: {yaml_file}")
        
        # Create converter instance (no backup for test)
        converter = YAMLToMarkdownConverter(backup=False)
        converter.knowledge_vault_path = temp_path
        
        # Convert the test file
        try:
            success = converter._convert_yaml_file(yaml_file)
            
            if success:
                # Check if markdown file was created
                md_file = yaml_file.with_suffix('.md')
                if md_file.exists():
                    print("✅ Conversion successful!")
                    
                    # Read and display the result
                    with open(md_file, 'r') as f:
                        content = f.read()
                    
                    print("\n📖 Generated Markdown file:")
                    print("-" * 50)
                    print(content)
                    print("-" * 50)
                    
                    # Parse with frontmatter to validate
                    post = frontmatter.load(md_file)
                    print(f"\n🔍 Frontmatter validation:")
                    print(f"   - Metadata fields: {len(post.metadata)}")
                    print(f"   - Content length: {len(post.content)} characters")
                    print(f"   - Has 'name' field: {'name' in post.metadata}")
                    print(f"   - Has relationships: {'knowledge_vault_relations' in post.metadata}")
                    
                    # Check original YAML was removed
                    if not yaml_file.exists():
                        print("✅ Original YAML file was properly removed")
                    else:
                        print("⚠️  Original YAML file still exists")
                    
                    return True
                else:
                    print("❌ Markdown file was not created")
                    return False
            else:
                print("❌ Conversion returned False")
                return False
                
        except Exception as e:
            print(f"❌ Conversion failed with error: {str(e)}")
            return False

def main():
    """Run the test."""
    print("Knowledge Vault Conversion Test")
    print("===============================")
    
    success = test_conversion()
    
    if success:
        print("\n🎉 Test passed! The conversion process works correctly.")
        print("✅ Ready to run full conversion on your Knowledge Vault.")
    else:
        print("\n❌ Test failed! Please check the conversion script.")
        print("🔧 Review the error messages above and fix issues before running full conversion.")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())