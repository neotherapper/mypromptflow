#!/usr/bin/env python3
"""
Compare files between docs/mcp-server-registry and mcp-registry to identify newer files
"""
import os
import re
from pathlib import Path
from datetime import datetime

def get_file_timestamp(filepath):
    """Get file modification timestamp"""
    try:
        return os.path.getmtime(filepath)
    except OSError:
        return 0

def normalize_filename(filename):
    """Normalize filename for comparison (remove -mcp suffix, etc.)"""
    # Remove .md extension
    name = filename.replace('.md', '')
    # Remove -mcp- patterns
    name = re.sub(r'-mcp(-|$)', '-', name)
    # Remove trailing dashes
    name = name.rstrip('-')
    return name

def find_matching_files():
    """Find files that exist in both locations and compare timestamps"""
    docs_dir = Path("/Users/georgiospilitsoglou/Developer/projects/mypromptflow/projects/ai-knowledge-intelligence-orchestrator/docs/mcp-server-registry/mcp-registry/detailed-profiles")
    main_dir = Path("/Users/georgiospilitsoglou/Developer/projects/mypromptflow/projects/ai-knowledge-intelligence-orchestrator/mcp-registry/detailed-profiles")
    
    docs_files = {}
    main_files = {}
    
    # Collect docs files
    for tier_dir in docs_dir.iterdir():
        if tier_dir.is_dir():
            for file in tier_dir.glob("*.md"):
                normalized = normalize_filename(file.name)
                docs_files[normalized] = {
                    'path': file,
                    'timestamp': get_file_timestamp(file),
                    'tier': tier_dir.name
                }
    
    # Collect main registry files
    for tier_dir in main_dir.iterdir():
        if tier_dir.is_dir():
            for file in tier_dir.glob("*.md"):
                normalized = normalize_filename(file.name)
                main_files[normalized] = {
                    'path': file,
                    'timestamp': get_file_timestamp(file),
                    'tier': tier_dir.name
                }
    
    newer_in_docs = []
    only_in_docs = []
    
    # Compare timestamps
    for normalized_name, docs_info in docs_files.items():
        if normalized_name in main_files:
            main_info = main_files[normalized_name]
            if docs_info['timestamp'] > main_info['timestamp']:
                time_diff = docs_info['timestamp'] - main_info['timestamp']
                newer_in_docs.append({
                    'normalized': normalized_name,
                    'docs_file': docs_info['path'],
                    'main_file': main_info['path'],
                    'time_diff_hours': time_diff / 3600,
                    'docs_tier': docs_info['tier'],
                    'main_tier': main_info['tier']
                })
        else:
            only_in_docs.append({
                'normalized': normalized_name,
                'docs_file': docs_info['path'],
                'tier': docs_info['tier']
            })
    
    return newer_in_docs, only_in_docs

def main():
    newer_in_docs, only_in_docs = find_matching_files()
    
    print("=== FILES NEWER IN DOCS DIRECTORY ===")
    for item in newer_in_docs:
        print(f"NEWER: {item['normalized']}")
        print(f"  Docs: {item['docs_file']} ({item['docs_tier']})")
        print(f"  Main: {item['main_file']} ({item['main_tier']})")
        print(f"  Time diff: {item['time_diff_hours']:.1f} hours")
        print()
    
    print("=== FILES ONLY IN DOCS DIRECTORY ===")
    for item in only_in_docs:
        print(f"ONLY_DOCS: {item['normalized']}")
        print(f"  Path: {item['docs_file']} ({item['tier']})")
        print()
    
    print(f"\nSUMMARY:")
    print(f"Files newer in docs: {len(newer_in_docs)}")
    print(f"Files only in docs: {len(only_in_docs)}")

if __name__ == "__main__":
    main()