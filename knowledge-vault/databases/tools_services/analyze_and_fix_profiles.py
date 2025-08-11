#!/usr/bin/env python3
"""
Analyze MCP server profiles for duplicates and fix npm to pnpm.
"""

import os
import re
from pathlib import Path
from collections import defaultdict

def extract_metadata(filepath):
    """Extract key metadata from a profile using regex."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Extract YAML frontmatter
    yaml_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not yaml_match:
        return None
    
    yaml_content = yaml_match.group(1)
    
    # Parse key fields using regex
    metadata = {}
    
    # Extract repository_url
    repo_match = re.search(r'^repository_url:\s*(.+)$', yaml_content, re.MULTILINE)
    if repo_match:
        metadata['repository_url'] = repo_match.group(1).strip()
    
    # Extract name
    name_match = re.search(r'^name:\s*(.+)$', yaml_content, re.MULTILINE)
    if name_match:
        metadata['name'] = name_match.group(1).strip()
    
    # Extract quality_score
    quality_match = re.search(r'^quality_score:\s*([\d.]+)$', yaml_content, re.MULTILINE)
    if quality_match:
        metadata['quality_score'] = float(quality_match.group(1))
    
    return metadata

def extract_repository_url(metadata):
    """Extract repository URL from metadata."""
    if metadata:
        return metadata.get('repository_url', 'NO_REPO')
    return 'NO_REPO'

def extract_name(metadata):
    """Extract name from metadata."""
    if metadata:
        return metadata.get('name', 'UNKNOWN')
    return 'UNKNOWN'

def find_duplicates():
    """Find duplicate MCP server profiles based on repository URLs."""
    items_dir = Path('/Users/georgiospilitsoglou/Developer/projects/mypromptflow/knowledge-vault/databases/tools_services/items')
    
    # Group files by repository URL
    repo_groups = defaultdict(list)
    name_groups = defaultdict(list)
    
    for filepath in sorted(items_dir.glob('*.md')):
        metadata = extract_metadata(filepath)
        if metadata:
            repo_url = extract_repository_url(metadata)
            name = extract_name(metadata)
            
            repo_groups[repo_url].append({
                'file': filepath.name,
                'name': name,
                'repo': repo_url,
                'quality_score': metadata.get('quality_score', 0)
            })
            
            # Also group by similar names
            base_name = name.lower().replace('mcp server', '').replace('mcp', '').strip()
            if base_name:
                name_groups[base_name].append({
                    'file': filepath.name,
                    'name': name,
                    'repo': repo_url,
                    'quality_score': metadata.get('quality_score', 0)
                })
    
    print("=" * 80)
    print("DUPLICATE ANALYSIS REPORT")
    print("=" * 80)
    
    # Find duplicates by repository
    print("\n## Profiles with Same Repository URL:")
    print("-" * 40)
    duplicate_count = 0
    for repo_url, profiles in repo_groups.items():
        if len(profiles) > 1 and repo_url != 'NO_REPO':
            duplicate_count += 1
            print(f"\nRepository: {repo_url}")
            for p in sorted(profiles, key=lambda x: x['quality_score'], reverse=True):
                print(f"  - {p['file']} (Quality: {p['quality_score']}, Name: {p['name']})")
    
    if duplicate_count == 0:
        print("No duplicates found based on repository URLs")
    
    # Find potential duplicates by name similarity
    print("\n## Potential Duplicates by Name Similarity:")
    print("-" * 40)
    similar_count = 0
    for base_name, profiles in name_groups.items():
        if len(profiles) > 1:
            # Check if they have different repos
            unique_repos = set(p['repo'] for p in profiles if p['repo'] != 'NO_REPO')
            if len(unique_repos) <= 1:  # Same repo or no repo
                similar_count += 1
                print(f"\nSimilar Name Group: '{base_name}'")
                for p in sorted(profiles, key=lambda x: x['quality_score'], reverse=True):
                    print(f"  - {p['file']}")
                    print(f"    Name: {p['name']}")
                    print(f"    Repo: {p['repo']}")
                    print(f"    Quality: {p['quality_score']}")
    
    if similar_count == 0:
        print("No potential duplicates found by name similarity")
    
    # List profiles without repository URLs
    print("\n## Profiles Without Repository URLs:")
    print("-" * 40)
    no_repo_profiles = repo_groups.get('NO_REPO', [])
    if no_repo_profiles:
        print(f"Found {len(no_repo_profiles)} profiles without repository URLs:")
        for p in sorted(no_repo_profiles, key=lambda x: x['name']):
            print(f"  - {p['file']} ({p['name']})")
    
    return repo_groups, name_groups

def replace_npm_with_pnpm(filepath):
    """Replace npm commands with pnpm in a file."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    original_content = content
    
    # Replace various npm patterns with pnpm
    replacements = [
        # Basic npm install commands
        (r'\bnpm install\b', 'pnpm install'),
        (r'\bnpm i\b', 'pnpm i'),
        
        # npm install with flags
        (r'\bnpm install -g\b', 'pnpm install -g'),
        (r'\bnpm install --global\b', 'pnpm install --global'),
        (r'\bnpm install -D\b', 'pnpm install -D'),
        (r'\bnpm install --save-dev\b', 'pnpm install --save-dev'),
        (r'\bnpm install --save\b', 'pnpm install --save'),
        
        # npm run commands
        (r'\bnpm run\b', 'pnpm run'),
        (r'\bnpm start\b', 'pnpm start'),
        (r'\bnpm test\b', 'pnpm test'),
        (r'\bnpm build\b', 'pnpm build'),
        
        # npx commands (pnpm dlx is the equivalent)
        (r'\bnpx\b', 'pnpm dlx'),
        
        # npm init
        (r'\bnpm init\b', 'pnpm init'),
        
        # npm exec
        (r'\bnpm exec\b', 'pnpm exec'),
        
        # npm list
        (r'\bnpm list\b', 'pnpm list'),
        (r'\bnpm ls\b', 'pnpm ls'),
    ]
    
    changes_made = False
    for pattern, replacement in replacements:
        new_content = re.sub(pattern, replacement, content)
        if new_content != content:
            changes_made = True
            content = new_content
    
    if changes_made:
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    return False

def main():
    """Main analysis and fix function."""
    items_dir = Path('/Users/georgiospilitsoglou/Developer/projects/mypromptflow/knowledge-vault/databases/tools_services/items')
    
    # First, analyze duplicates
    print("PHASE 1: ANALYZING DUPLICATES")
    repo_groups, name_groups = find_duplicates()
    
    # Now replace npm with pnpm
    print("\n" + "=" * 80)
    print("PHASE 2: REPLACING NPM WITH PNPM")
    print("=" * 80)
    
    updated_count = 0
    for filepath in sorted(items_dir.glob('*.md')):
        if replace_npm_with_pnpm(filepath):
            updated_count += 1
            print(f"✓ Updated: {filepath.name}")
    
    print(f"\nSummary: Updated {updated_count} files from npm to pnpm")
    
    # Provide recommendations
    print("\n" + "=" * 80)
    print("RECOMMENDATIONS")
    print("=" * 80)
    
    print("\n1. For duplicate profiles with same repository:")
    print("   - Keep the one with highest quality score")
    print("   - Merge any unique information from others")
    print("   - Delete the redundant profiles")
    
    print("\n2. For profiles without repository URLs:")
    print("   - Research and add repository URLs where possible")
    print("   - This helps identify true duplicates")
    
    print("\n3. For similar named profiles:")
    print("   - Verify if they're truly different services")
    print("   - If same service, consolidate into one profile")

if __name__ == "__main__":
    main()