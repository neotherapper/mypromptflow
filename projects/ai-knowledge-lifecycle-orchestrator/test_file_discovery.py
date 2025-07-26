#!/usr/bin/env python3
"""
Test script to debug file discovery logic
"""

import os
import yaml
from glob import glob

def test_file_discovery():
    # Load configuration
    with open('dependency-registry/scanner-config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    
    file_discovery = config['scanner_configuration']['file_discovery']
    
    print(f"Base directories: {file_discovery['base_directories']}")
    print(f"Include patterns: {file_discovery['include_patterns']}")
    print(f"Exclude patterns: {file_discovery['exclude_patterns']}")
    print()
    
    discovered_files = []
    for base_dir in file_discovery['base_directories']:
        print(f"Scanning base directory: {base_dir}")
        print(f"Base directory exists: {os.path.exists(base_dir)}")
        print(f"Base directory is directory: {os.path.isdir(base_dir)}")
        
        for pattern in file_discovery['include_patterns']:
            full_pattern = os.path.join(base_dir, pattern)
            print(f"  Testing pattern: {full_pattern}")
            files = glob(full_pattern, recursive=True)
            print(f"  Found {len(files)} files")
            for f in files[:3]:  # Show first 3 files
                print(f"    {f}")
            discovered_files.extend(files)
            print()
    
    print(f"Total discovered files before filtering: {len(discovered_files)}")
    
    # Test exclude filtering
    filtered_files = []
    for file_path in discovered_files[:5]:  # Test first 5 files only for debugging
        exclude = False
        for exclude_pattern in file_discovery['exclude_patterns']:
            # Convert glob pattern to simple substring check
            # Remove ** wildcards and check if pattern core is in path
            pattern_core = exclude_pattern.replace('**/', '').replace('/**', '').replace('*', '')
            print(f"Testing file: {file_path}")
            print(f"  Against pattern: {exclude_pattern} -> core: '{pattern_core}'")
            print(f"  Contains '{pattern_core}': {pattern_core and pattern_core in file_path}")
            if pattern_core and pattern_core in file_path:
                exclude = True
                print(f"  EXCLUDED: {file_path} (matches pattern: {exclude_pattern})")
                break
        if not exclude:
            filtered_files.append(file_path)
            print(f"  INCLUDED: {file_path}")
        print()
    
    print(f"Files after exclude filtering (first 5 tested): {len(filtered_files)}")
    return  # Exit early for debugging
    
    print(f"Files after exclude filtering: {len(filtered_files)}")
    
    # Test size filtering
    max_size = file_discovery['file_size_limits']['maximum_file_size_mb'] * 1024 * 1024
    min_size = file_discovery['file_size_limits']['minimum_file_size_bytes']
    
    size_filtered_files = []
    for file_path in filtered_files:
        try:
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                if min_size <= file_size <= max_size:
                    size_filtered_files.append(file_path)
                else:
                    print(f"Size filtered: {file_path} (size: {file_size})")
        except OSError:
            print(f"Could not access file: {file_path}")
    
    print(f"Final files after size filtering: {len(size_filtered_files)}")
    for f in size_filtered_files[:5]:
        print(f"  {f}")

if __name__ == "__main__":
    test_file_discovery()