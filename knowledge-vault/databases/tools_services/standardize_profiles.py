#!/usr/bin/env python3
"""
Comprehensive MCP Server Profile Standardization Script
Applies blueprint standards to all profiles systematically
"""

import os
import re
from pathlib import Path

# Configuration
PROFILES_DIR = Path("/Users/georgiospilitsoglou/Developer/projects/mypromptflow/knowledge-vault/databases/tools_services/items")
BLUEPRINT_HEADERS = [
    "## 📋 Basic Information",
    "## Quality & Scoring Metrics", 
    "## Technical Specifications",
    "## Setup & Configuration",
    "## Integration Capabilities",
    "## Business Impact"
]

# Forbidden industry-specific terms
FORBIDDEN_TERMS = [
    "maritime", "vessel", "P&I Club", "IMO", "flag state",
    "insurance company", "marine insurance", "hull insurance",
    "cargo insurance", "liability insurance", "shipping",
    "port authority", "nautical", "seafaring", "naval"
]

# Generic replacements
TERM_REPLACEMENTS = {
    "maritime insurance": "business operations",
    "maritime": "business",
    "vessel": "asset",
    "vessels": "assets",
    "shipping": "logistics",
    "marine": "operational",
    "insurance": "risk management",
    "P&I Club": "industry association",
    "IMO": "regulatory body",
    "flag state": "jurisdiction",
    "port": "facility",
    "cargo": "inventory",
    "hull": "infrastructure"
}

def fix_executive_summary_headers(content):
    """Replace Executive Summary with Basic Information"""
    # Multiple patterns to catch variations
    patterns = [
        (r'## Executive Summary\n', '## 📋 Basic Information\n'),
        (r'## 🎯 Executive Summary\n', '## 📋 Basic Information\n'),
        (r'### Executive Summary\n', '## 📋 Basic Information\n'),
        (r'# Executive Summary\n', '## 📋 Basic Information\n'),
    ]
    
    for pattern, replacement in patterns:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    return content

def remove_industry_references(content):
    """Remove all industry-specific references"""
    # Case-insensitive replacement
    for forbidden, replacement in TERM_REPLACEMENTS.items():
        # Whole word matching to avoid breaking URLs or code
        pattern = r'\b' + re.escape(forbidden) + r'\b'
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    
    return content

def ensure_blueprint_structure(content):
    """Ensure all required blueprint sections exist"""
    lines = content.split('\n')
    
    # Check which sections exist
    existing_sections = set()
    for line in lines:
        for header in BLUEPRINT_HEADERS:
            if header in line:
                existing_sections.add(header)
    
    # If missing critical sections, add them
    if "## 📋 Basic Information" not in existing_sections:
        # Find where to insert (after frontmatter)
        insert_idx = 0
        in_frontmatter = False
        for i, line in enumerate(lines):
            if line.strip() == '---':
                if not in_frontmatter:
                    in_frontmatter = True
                else:
                    insert_idx = i + 1
                    break
        
        if insert_idx > 0 and insert_idx < len(lines):
            lines.insert(insert_idx, "\n## 📋 Basic Information\n")
    
    return '\n'.join(lines)

def add_quality_scoring_section(content):
    """Add quality scoring section if missing"""
    if "## Quality & Scoring Metrics" not in content:
        # Add after Basic Information
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if "## 📋 Basic Information" in line:
                # Find the next section or end of basic info
                j = i + 1
                while j < len(lines) and not lines[j].startswith('##'):
                    j += 1
                
                scoring_section = """
## Quality & Scoring Metrics

### Business-Aligned Scoring Analysis

**Business Domain Relevance**: [Score]/10
**Technical Development Value**: [Score]/10  
**Production Readiness**: [Score]/10
**Setup Complexity**: [Score]/10
**Maintenance Status**: [Score]/10
**Documentation Quality**: [Score]/10

**Composite Score: [Score]/10** - Tier [X] Implementation Priority
"""
                lines.insert(j, scoring_section)
                break
        
        content = '\n'.join(lines)
    
    return content

def add_docker_first_setup(content):
    """Ensure Docker is the first installation method"""
    if "## Setup & Configuration" in content and "Docker MCP Toolkit" not in content:
        # Add Docker-first installation methods
        docker_section = """
### Installation Methods

#### Method 1: Docker MCP Toolkit (Recommended)
```bash
# Pull and run the MCP server
docker pull mcp/[server-name]:latest
docker run -d --name [server-name]-mcp \\
  -e API_KEY=${API_KEY} \\
  -p 3000:3000 \\
  mcp/[server-name]:latest
```

#### Method 2: Docker Compose Deployment
```yaml
version: '3.8'
services:
  [server-name]:
    image: mcp/[server-name]:latest
    environment:
      - API_KEY=${API_KEY}
    ports:
      - "3000:3000"
    restart: unless-stopped
```
"""
        # Insert after Setup & Configuration header
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if "## Setup & Configuration" in line:
                j = i + 1
                # Skip to ### Installation Methods or insert new
                while j < len(lines) and not lines[j].startswith('###'):
                    j += 1
                
                if j < len(lines) and "Installation Methods" in lines[j]:
                    # Replace existing
                    k = j + 1
                    while k < len(lines) and not lines[k].startswith('##'):
                        k += 1
                    lines[j:k] = docker_section.split('\n')
                else:
                    lines.insert(j, docker_section)
                break
        
        content = '\n'.join(lines)
    
    return content

def process_file(filepath):
    """Process a single MCP server profile file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply all fixes
        content = fix_executive_summary_headers(content)
        content = remove_industry_references(content)
        content = ensure_blueprint_structure(content)
        content = add_quality_scoring_section(content)
        content = add_docker_first_setup(content)
        
        # Only write if changed
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        
        return False
        
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    """Main processing function"""
    print("Starting comprehensive MCP server profile standardization...")
    
    # Get all .md files
    md_files = list(PROFILES_DIR.glob("*.md"))
    total_files = len(md_files)
    
    print(f"Found {total_files} profile files to process")
    
    # Process statistics
    stats = {
        'executive_summary_fixed': 0,
        'industry_terms_removed': 0,
        'structure_fixed': 0,
        'files_updated': 0,
        'errors': 0
    }
    
    # Process each file
    for i, filepath in enumerate(md_files, 1):
        if i % 10 == 0:
            print(f"Processing file {i}/{total_files}...")
        
        # Check what needs fixing
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        needs_update = False
        
        if "Executive Summary" in content:
            stats['executive_summary_fixed'] += 1
            needs_update = True
        
        if any(term in content.lower() for term in FORBIDDEN_TERMS):
            stats['industry_terms_removed'] += 1
            needs_update = True
        
        if "## 📋 Basic Information" not in content:
            stats['structure_fixed'] += 1
            needs_update = True
        
        # Process the file
        if needs_update:
            if process_file(filepath):
                stats['files_updated'] += 1
            else:
                stats['errors'] += 1
    
    # Print summary
    print("\n" + "="*50)
    print("STANDARDIZATION COMPLETE")
    print("="*50)
    print(f"Total files processed: {total_files}")
    print(f"Files updated: {stats['files_updated']}")
    print(f"Executive Summary headers fixed: {stats['executive_summary_fixed']}")
    print(f"Industry references removed: {stats['industry_terms_removed']}")
    print(f"Structure issues fixed: {stats['structure_fixed']}")
    print(f"Errors encountered: {stats['errors']}")
    
    return stats

if __name__ == "__main__":
    stats = main()