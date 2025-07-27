#!/usr/bin/env python3
"""
Batch Knowledge Vault Item Transformer

Transforms remaining Notion-migrated items to dual-layer architecture format.
Uses name resolution engine to convert raw UUIDs to human-readable links.
"""

import os
import re
from pathlib import Path
from name_resolution_engine import NameResolutionEngine

class BatchTransformer:
    """
    Transforms knowledge vault items from basic Notion format to dual-layer architecture.
    """
    
    def __init__(self, vault_path: str = "/Users/georgiospilitsoglou/Developer/projects/mypromptflow/knowledge-vault"):
        self.vault_path = Path(vault_path)
        self.items_path = self.vault_path / "databases" / "knowledge_vault" / "items"
        self.engine = NameResolutionEngine(vault_path)
        
    def identify_items_needing_transformation(self) -> list:
        """Identify items that still need dual-layer transformation."""
        items_needing_work = []
        
        for item_file in self.items_path.glob("*.md"):
            content = item_file.read_text()
            # Check if already transformed (has dual-layer format)
            if 'uuid: "' in content and '# Technical metadata for AI agents' in content:
                continue  # Already transformed
            
            # Check if has raw UUID lists that need conversion
            if re.search(r'^- `[a-f0-9-]{36}` -', content, re.MULTILINE):
                items_needing_work.append(item_file.name)
                
        return items_needing_work
    
    def convert_uuid_lists_in_content(self, content: str) -> str:
        """Convert raw UUID lists to human-readable markdown links."""
        lines = content.split('\n')
        converted_lines = []
        in_related_items = False
        
        for line in lines:
            # Detect if we're in a Related Items section
            if line.startswith('## Related Items') or line.startswith('### Knowledge Vault') or line.startswith('### Platforms'):
                in_related_items = True
                converted_lines.append(line)
                continue
            
            # If we hit another section, we're out of related items
            if line.startswith('##') and in_related_items and 'Related' not in line:
                in_related_items = False
            
            # Convert UUID lines if in related items section
            if in_related_items and re.match(r'^- `([a-f0-9-]{36})` -', line):
                uuid_match = re.search(r'([a-f0-9-]{36})', line)
                if uuid_match:
                    uuid = uuid_match.group(1)
                    link = self.engine.resolve_uuid_to_link(uuid)
                    if not link.startswith("Unknown Item"):
                        converted_lines.append(f"- {link}")
                    # Skip lines with unknown UUIDs
                continue
            
            converted_lines.append(line)
        
        return '\n'.join(converted_lines)
    
    def demonstrate_conversion(self, filename: str):
        """Demonstrate the conversion process for a single file."""
        file_path = self.items_path / filename
        if not file_path.exists():
            print(f"File {filename} not found")
            return
        
        content = file_path.read_text()
        print(f"\n=== Processing {filename} ===")
        
        # Show before state
        uuid_lines = [line for line in content.split('\n') if re.match(r'^- `[a-f0-9-]{36}` -', line)]
        if uuid_lines:
            print(f"Found {len(uuid_lines)} raw UUID lines:")
            for line in uuid_lines[:3]:  # Show first 3
                print(f"  BEFORE: {line}")
        
        # Convert
        converted_content = self.convert_uuid_lists_in_content(content)
        
        # Show after state
        converted_lines = converted_content.split('\n')
        new_link_lines = [line for line in converted_lines if re.match(r'^- \[.*\]\(.*\.md\)', line)]
        if new_link_lines:
            print(f"Converted to {len(new_link_lines)} human-readable links:")
            for line in new_link_lines[:3]:
                print(f"  AFTER:  {line}")
        
        return converted_content

if __name__ == "__main__":
    transformer = BatchTransformer()
    
    # Identify items needing work
    items_needed = transformer.identify_items_needing_transformation()
    print(f"Found {len(items_needed)} items needing UUID conversion:")
    
    for item in items_needed[:10]:  # Show first 10
        print(f"  - {item}")
    
    # Demonstrate conversion on one file
    if items_needed:
        sample_file = items_needed[0]
        print(f"\n=== Demonstrating conversion on {sample_file} ===")
        transformer.demonstrate_conversion(sample_file)