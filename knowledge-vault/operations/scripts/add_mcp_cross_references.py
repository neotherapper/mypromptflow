#!/usr/bin/env python3
"""
Add MCP profile cross-references to MCP server files in knowledge-vault.
This script adds the mcp_profile_reference field to all MCP server files
that are missing this cross-reference format.
"""

import os
import re
from pathlib import Path

def extract_server_name_from_filename(filename):
    """Extract clean server name from filename for cross-reference."""
    # Remove file extension
    name = filename.replace('.md', '')
    
    # Remove common suffixes
    suffixes_to_remove = [
        '-mcp-server', '-server-profile', '-comprehensive-profile',
        '-enterprise-profile', '-detailed-profile', '-platform',
        '-service', '-comprehensive', '-enhanced', '-official',
        '-ai-powered', '-real-time', '-enterprise', '-database'
    ]
    
    for suffix in suffixes_to_remove:
        if name.endswith(suffix):
            name = name.replace(suffix, '')
            break
    
    # Clean up remaining parts
    name = re.sub(r'-mcp-.*', '', name)  # Remove anything after -mcp-
    name = re.sub(r'-tier-\d+', '', name)  # Remove tier indicators
    
    # Handle specific cases
    replacements = {
        'github-pr-creator': 'github-pr-creator',
        'github-pr-reviewer': 'github-pr-reviewer', 
        'github-actions': 'github-actions',
        'apache-doris-real-time-data-warehouse': 'apache-doris',
        'bigquery-enterprise-analytics': 'bigquery',
        'clickhouse-high-performance-analytics': 'clickhouse',
        'postgresql-real-time-ai-agent-interactions': 'postgresql',
        'sequelize-database-orm': 'sequelize',
    }
    
    if name in replacements:
        name = replacements[name]
    
    return name

def add_cross_reference_to_file(file_path):
    """Add mcp_profile_reference field to a file if missing."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check if already has cross-reference
        if 'mcp_profile_reference:' in content:
            return False, "Already has cross-reference"
        
        # Extract filename for server name
        filename = os.path.basename(file_path)
        server_name = extract_server_name_from_filename(filename)
        cross_ref = f'mcp_profile_reference: "@mcp_profile/{server_name}"'
        
        # Find the end of the YAML frontmatter
        if content.startswith('---\n'):
            # Find the closing ---
            parts = content.split('---\n', 2)
            if len(parts) >= 3:
                yaml_part = parts[1]
                rest_content = parts[2]
                
                # Add cross-reference before closing ---
                new_yaml = yaml_part.rstrip() + '\n' + cross_ref + '\n'
                new_content = '---\n' + new_yaml + '---\n' + rest_content
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                return True, f"Added @mcp_profile/{server_name}"
            else:
                return False, "Invalid YAML frontmatter format"
        else:
            return False, "No YAML frontmatter found"
            
    except Exception as e:
        return False, f"Error: {str(e)}"

def main():
    """Main execution function."""
    tools_services_dir = Path("knowledge-vault/databases/tools_services/items")
    
    if not tools_services_dir.exists():
        print(f"Directory not found: {tools_services_dir}")
        return
    
    # Find all MCP server files
    mcp_files = list(tools_services_dir.glob("*mcp*.md"))
    
    print(f"Found {len(mcp_files)} MCP server files")
    print("Processing files...")
    
    success_count = 0
    already_has_count = 0
    error_count = 0
    
    for file_path in mcp_files:
        success, message = add_cross_reference_to_file(file_path)
        
        if success:
            success_count += 1
            print(f"✅ {file_path.name}: {message}")
        elif "Already has cross-reference" in message:
            already_has_count += 1
        else:
            error_count += 1
            print(f"❌ {file_path.name}: {message}")
    
    print(f"\nResults:")
    print(f"✅ Successfully added cross-references: {success_count}")
    print(f"ℹ️  Already had cross-references: {already_has_count}")
    print(f"❌ Errors: {error_count}")
    print(f"📊 Total files processed: {len(mcp_files)}")

if __name__ == "__main__":
    main()