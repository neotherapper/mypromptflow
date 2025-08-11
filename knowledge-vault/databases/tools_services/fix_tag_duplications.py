#!/usr/bin/env python3
"""
Fix tag duplications in MCP server profiles.
Removes duplicate tags with different capitalizations and standardizes tag format.
"""

import os
import re
from pathlib import Path

# Define tag standardization rules
TAG_STANDARDIZATION = {
    # Tier tags - use capitalized format
    'tier-1': 'Tier 1',
    'tier-2': 'Tier 2',
    'tier-3': 'Tier 3',
    'tier-4': 'Tier 4',
    'tier 1': 'Tier 1',
    'tier 2': 'Tier 2',
    'tier 3': 'Tier 3',
    'tier 4': 'Tier 4',
    
    # MCP and service tags - use capitalized format
    'mcp-server': 'MCP Server',
    'mcp server': 'MCP Server',
    'api-service': 'API Service',
    'api service': 'API Service',
    'database-service': 'Database Service',
    'database service': 'Database Service',
    'analytics-platform': 'Analytics Platform',
    'analytics platform': 'Analytics Platform',
    'development-platform': 'Development Platform',
    'development platform': 'Development Platform',
    'monitoring-tool': 'Monitoring Tool',
    'monitoring tool': 'Monitoring Tool',
    'security-tool': 'Security Tool',
    'security tool': 'Security Tool',
    'storage-service': 'Storage Service',
    'storage service': 'Storage Service',
    
    # Technology tags - use lowercase
    'E-commerce': 'e-commerce',
    'E-Commerce': 'e-commerce',
    'Fintech': 'fintech',
    'FinTech': 'fintech',
    'AI': 'ai',
    'Ai': 'ai',
    'ML': 'ml',
    'Ml': 'ml',
    
    # Common duplicates
    'Enterprise': 'enterprise',
    'Analytics': 'analytics',
    'Monitoring': 'monitoring',
    'Security': 'security',
    'Database': 'database',
    'Storage': 'storage',
    'Automation': 'automation',
    'Integration': 'integration',
    'Testing': 'testing',
    'Deployment': 'deployment',
    'DevOps': 'devops',
    'Devops': 'devops',
}

def extract_tags(content):
    """Extract tags section from YAML frontmatter."""
    tags_match = re.search(r'^tags:\s*\n((?:- .*\n)+)', content, re.MULTILINE)
    if tags_match:
        tags_text = tags_match.group(1)
        tags = [line.strip('- ').strip() for line in tags_text.strip().split('\n')]
        return tags, tags_match
    return [], None

def standardize_tags(tags):
    """Standardize and deduplicate tags."""
    standardized = []
    seen_normalized = set()
    
    for tag in tags:
        # Apply standardization rules
        standardized_tag = TAG_STANDARDIZATION.get(tag.lower(), tag)
        if standardized_tag == tag and tag.lower() in TAG_STANDARDIZATION:
            standardized_tag = TAG_STANDARDIZATION[tag.lower()]
        
        # Normalize for comparison (lowercase for deduplication check)
        normalized = standardized_tag.lower()
        
        # Only add if not a duplicate
        if normalized not in seen_normalized:
            standardized.append(standardized_tag)
            seen_normalized.add(normalized)
    
    # Sort tags to maintain consistency
    # Keep tier tags first, then MCP Server, then others alphabetically
    def tag_sort_key(tag):
        if tag.startswith('Tier '):
            return (0, tag)
        elif tag == 'MCP Server':
            return (1, tag)
        elif 'Service' in tag or 'Platform' in tag or 'Tool' in tag:
            return (2, tag)
        else:
            return (3, tag.lower())
    
    standardized.sort(key=tag_sort_key)
    return standardized

def fix_file_tags(filepath):
    """Fix tag duplications in a single file."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Extract and process tags
    tags, tags_match = extract_tags(content)
    if not tags:
        return False, "No tags found"
    
    # Standardize and deduplicate
    original_count = len(tags)
    standardized = standardize_tags(tags)
    new_count = len(standardized)
    
    # Check if changes are needed
    if tags == standardized:
        return False, f"No changes needed ({original_count} tags)"
    
    # Rebuild tags section
    new_tags_text = '\n'.join(f'- {tag}' for tag in standardized) + '\n'
    
    # Replace in content
    content = content[:tags_match.start(1)] + new_tags_text + content[tags_match.end(1):]
    
    # Write back
    with open(filepath, 'w') as f:
        f.write(content)
    
    duplicates_removed = original_count - new_count
    return True, f"Fixed: {original_count} tags → {new_count} tags ({duplicates_removed} duplicates removed)"

def main():
    """Process all MCP server profile files."""
    items_dir = Path('/Users/georgiospilitsoglou/Developer/projects/mypromptflow/knowledge-vault/databases/tools_services/items')
    
    if not items_dir.exists():
        print(f"Error: Directory not found: {items_dir}")
        return
    
    # Process all .md files
    md_files = sorted(items_dir.glob('*.md'))
    
    print(f"Processing {len(md_files)} files for tag duplications...")
    print("=" * 60)
    
    fixed_count = 0
    error_count = 0
    unchanged_count = 0
    total_duplicates_removed = 0
    
    for filepath in md_files:
        try:
            changed, message = fix_file_tags(filepath)
            
            if changed:
                fixed_count += 1
                # Extract duplicate count from message
                if 'duplicates removed' in message:
                    dup_count = int(message.split('(')[1].split(' ')[0])
                    total_duplicates_removed += dup_count
                print(f"✓ {filepath.name}: {message}")
            else:
                unchanged_count += 1
                # Only show files with tags (skip those without)
                if "No tags found" not in message:
                    print(f"  {filepath.name}: {message}")
        
        except Exception as e:
            error_count += 1
            print(f"✗ {filepath.name}: Error - {str(e)}")
    
    print("=" * 60)
    print(f"\nSummary:")
    print(f"  Files processed: {len(md_files)}")
    print(f"  Files fixed: {fixed_count}")
    print(f"  Files unchanged: {unchanged_count}")
    print(f"  Files with errors: {error_count}")
    print(f"  Total duplicates removed: {total_duplicates_removed}")
    
    if fixed_count > 0:
        print(f"\n✅ Successfully fixed tag duplications in {fixed_count} files!")
    else:
        print("\n✅ No tag duplications found - all files are clean!")

if __name__ == "__main__":
    main()