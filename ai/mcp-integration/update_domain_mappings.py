#!/usr/bin/env python3
"""
Domain Mapping Update Script
Fixes broken profile paths and expands MCP server coverage using knowledge-vault as source of truth
"""

import os
import yaml
import re
from pathlib import Path
from typing import Dict, List, Any, Optional

# Configuration
PROJECT_ROOT = Path("/Users/georgiospilitsoglou/Developer/projects/mypromptflow")
DOMAIN_MAPPINGS_PATH = PROJECT_ROOT / "ai/mcp-integration/domain-server-mappings.yaml"
KNOWLEDGE_VAULT_ITEMS = PROJECT_ROOT / "knowledge-vault/databases/tools_services/items"
BACKUP_PATH = PROJECT_ROOT / "ai/mcp-integration/domain-server-mappings.yaml.backup"

class DomainMappingUpdater:
    def __init__(self):
        self.current_mappings = None
        self.knowledge_vault_servers = {}
        self.server_name_mappings = {
            # Current mappings -> Knowledge vault file names
            "aws": ["aws-mcp-server.md", "aws-cloud-infrastructure-mcp-server-comprehensive-profile.md"],
            "docker": ["docker-containerization-platform-mcp-server-comprehensive-profile.md"],
            "github": ["github-mcp-server.md", "github-mcp-server-platform.md"],
            "postgresql": ["postgresql-mcp-server-enhanced.md"],
            "redis": ["redis-caching-server-profile.md"],
            "figma": ["figma-mcp-server.md"],
            "google_analytics": ["google-analytics-web-platform-mcp-server.md"],
            "qdrant": ["qdrant-mcp-server-database.md", "qdrant-vector-database-server-profile.md"],
            "slack": ["slack-server-profile.md"],
            "hubspot": ["hubspot-marketing-automation-mcp-server-detailed-profile.md"],
            "fetch": ["fetch-mcp-server.md"],
            "memory": ["memory-mcp-server.md"]
        }
        
    def load_current_mappings(self):
        """Load current domain mappings"""
        with open(DOMAIN_MAPPINGS_PATH, 'r') as f:
            self.current_mappings = yaml.safe_load(f)
        print(f"✅ Loaded current domain mappings with {len(self.current_mappings.get('domain_mappings', {}))} domains")
            
    def scan_knowledge_vault_servers(self):
        """Scan knowledge-vault for all MCP server profiles"""
        print("🔍 Scanning knowledge-vault for MCP server profiles...")
        
        for item_file in KNOWLEDGE_VAULT_ITEMS.glob("*.md"):
            try:
                with open(item_file, 'r') as f:
                    content = f.read()
                    
                # Extract YAML frontmatter
                if content.startswith('---'):
                    yaml_content = content.split('---')[1]
                    metadata = yaml.safe_load(yaml_content)
                    
                    # Check if it's an MCP server
                    if (metadata.get('item_type') == 'mcp_server' or 
                        'MCP Server' in metadata.get('tags', []) or
                        'mcp' in str(item_file).lower()):
                        
                        server_info = {
                            'file_path': f"knowledge-vault/databases/tools_services/items/{item_file.name}",
                            'name': metadata.get('name', item_file.stem),
                            'description': metadata.get('description', ''),
                            'tags': metadata.get('tags', []),
                            'category': metadata.get('category', ''),
                            'quality_score': metadata.get('quality_score', 0),
                            'setup_complexity': metadata.get('setup_complexity', 'unknown'),
                            'status': metadata.get('status', 'unknown'),
                            'priority': metadata.get('priority', ''),
                            'tier': self.estimate_tier(metadata)
                        }
                        
                        self.knowledge_vault_servers[item_file.stem] = server_info
                        
            except Exception as e:
                print(f"⚠️  Error processing {item_file.name}: {e}")
                
        print(f"✅ Found {len(self.knowledge_vault_servers)} MCP servers in knowledge-vault")
        
    def estimate_tier(self, metadata: Dict) -> int:
        """Estimate tier based on metadata"""
        priority = metadata.get('priority', '')
        quality = metadata.get('quality_score', 0)
        complexity = metadata.get('setup_complexity', '').lower()
        
        if '1st_priority' in priority or quality >= 9.0:
            return 1
        elif '2nd_priority' in priority or quality >= 8.0:
            return 2
        elif complexity in ['high', 'complex'] or quality < 7.0:
            return 3
        else:
            return 2  # Default to tier 2
            
    def fix_broken_profile_paths(self):
        """Fix broken profile paths in current mappings"""
        print("🔧 Fixing broken profile paths...")
        
        fixed_count = 0
        for domain_name, domain_config in self.current_mappings.get('domain_mappings', {}).items():
            for server in domain_config.get('primary_servers', []):
                server_id = server.get('server_id')
                
                if server_id in self.server_name_mappings:
                    # Find the best matching file
                    for filename in self.server_name_mappings[server_id]:
                        file_stem = filename.replace('.md', '')
                        if file_stem in self.knowledge_vault_servers:
                            old_path = server.get('profile_path', '')
                            new_path = self.knowledge_vault_servers[file_stem]['file_path']
                            server['profile_path'] = new_path
                            print(f"  📝 {server_id}: {old_path} -> {new_path}")
                            fixed_count += 1
                            break
                            
        print(f"✅ Fixed {fixed_count} broken profile paths")
        
    def add_missing_servers(self):
        """Add missing servers from knowledge-vault to domain mappings"""
        print("➕ Adding missing MCP servers to domain mappings...")
        
        # Define domain categories based on server names and tags
        domain_categories = {
            'ai_platforms': ['claude', 'openai', 'anthropic', 'cohere', 'hugging', 'mistral', 'perplexity'],
            'database_systems': ['postgresql', 'mysql', 'mongodb', 'redis', 'neo4j', 'clickhouse', 'supabase', 'sqlite'],
            'cloud_infrastructure': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'pulumi'],
            'development_tools': ['github', 'gitlab', 'git', 'jenkins', 'circleci'],
            'communication_tools': ['slack', 'discord', 'teams', 'twilio'],
            'business_systems': ['hubspot', 'salesforce', 'stripe', 'shopify', 'quickbooks'],
            'information_retrieval': ['fetch', 'memory', 'wikipedia', 'youtube', 'duckduckgo'],
            'analytics_data_science': ['google_analytics', 'datadog', 'prometheus', 'grafana'],
            'security_systems': ['okta', 'auth0', 'vault'],
            'frontend_development': ['figma', 'storybook', 'vercel', 'netlify']
        }
        
        # Add new domain if it doesn't exist
        if 'ai_platforms' not in self.current_mappings['domain_mappings']:
            self.current_mappings['domain_mappings']['ai_platforms'] = {
                'description': 'AI and machine learning platforms, language models, content generation',
                'keywords': ['ai', 'machine learning', 'llm', 'language model', 'content generation', 'analysis'],
                'primary_servers': []
            }
            
        # Add missing servers to appropriate domains
        added_count = 0
        for file_stem, server_info in self.knowledge_vault_servers.items():
            # Determine which domain this server belongs to
            server_domain = self.categorize_server(file_stem, server_info, domain_categories)
            
            if server_domain and server_domain in self.current_mappings['domain_mappings']:
                # Check if server already exists
                existing_ids = [s.get('server_id') for s in 
                              self.current_mappings['domain_mappings'][server_domain].get('primary_servers', [])]
                
                server_id = self.generate_server_id(file_stem)
                if server_id not in existing_ids:
                    new_server = {
                        'server_id': server_id,
                        'name': server_info['name'],
                        'tier': server_info['tier'],
                        'composite_score': float(server_info['quality_score']) if server_info['quality_score'] else 7.0,
                        'profile_path': server_info['file_path'],
                        'use_cases': self.generate_use_cases(server_info),
                        'integration_priority': self.get_integration_priority(server_info['tier']),
                        'setup_complexity': server_info['setup_complexity'].lower() if server_info['setup_complexity'] != 'unknown' else 'moderate'
                    }
                    
                    self.current_mappings['domain_mappings'][server_domain]['primary_servers'].append(new_server)
                    added_count += 1
                    print(f"  ➕ Added {server_id} to {server_domain}")
                    
        print(f"✅ Added {added_count} new MCP servers to domain mappings")
        
    def categorize_server(self, file_stem: str, server_info: Dict, domain_categories: Dict) -> Optional[str]:
        """Categorize server into appropriate domain"""
        name_lower = file_stem.lower()
        
        for domain, keywords in domain_categories.items():
            for keyword in keywords:
                if keyword in name_lower:
                    return domain
                    
        # Check tags and category
        tags = ' '.join(server_info.get('tags', [])).lower()
        category = server_info.get('category', '').lower()
        
        if 'ai' in tags or 'ai' in category:
            return 'ai_platforms'
        elif 'database' in tags or 'database' in category:
            return 'database_systems' 
        elif 'cloud' in tags or 'infrastructure' in category:
            return 'cloud_infrastructure'
        elif 'development' in tags or 'development' in category:
            return 'development_tools'
            
        return None
        
    def generate_server_id(self, file_stem: str) -> str:
        """Generate server ID from file stem"""
        # Clean up file stem to create server ID
        server_id = file_stem.replace('-mcp-server', '').replace('-server-profile', '')
        server_id = server_id.replace('-comprehensive-profile', '').replace('-detailed-profile', '')
        server_id = server_id.replace('-platform', '').replace('-service', '')
        server_id = re.sub(r'-+', '_', server_id)
        return server_id
        
    def generate_use_cases(self, server_info: Dict) -> List[str]:
        """Generate use cases based on server info"""
        description = server_info.get('description', '')
        name = server_info.get('name', '')
        
        # Extract use cases from description or generate based on name
        if 'github' in name.lower():
            return ["Repository analysis and code context", "Pull request and issue management", "CI/CD integration"]
        elif 'database' in description.lower():
            return ["Database operations and queries", "Schema management", "Data analysis"]
        elif 'ai' in description.lower() or 'ai' in name.lower():
            return ["AI-powered content generation", "Natural language processing", "Intelligent analysis"]
        else:
            return [f"{name} integration and automation", "Data access and management", "Workflow optimization"]
            
    def get_integration_priority(self, tier: int) -> str:
        """Get integration priority based on tier"""
        if tier == 1:
            return "high"
        elif tier == 2:
            return "medium"
        else:
            return "low"
            
    def backup_current_file(self):
        """Create backup of current domain mappings"""
        if DOMAIN_MAPPINGS_PATH.exists():
            with open(DOMAIN_MAPPINGS_PATH, 'r') as src, open(BACKUP_PATH, 'w') as dst:
                dst.write(src.read())
            print(f"✅ Created backup: {BACKUP_PATH}")
            
    def save_updated_mappings(self):
        """Save updated domain mappings"""
        with open(DOMAIN_MAPPINGS_PATH, 'w') as f:
            yaml.dump(self.current_mappings, f, default_flow_style=False, sort_keys=False, indent=2)
        print(f"✅ Saved updated domain mappings to {DOMAIN_MAPPINGS_PATH}")
        
    def run(self):
        """Execute the complete update process"""
        print("🚀 Starting domain mapping update process...")
        
        self.backup_current_file()
        self.load_current_mappings()
        self.scan_knowledge_vault_servers()
        self.fix_broken_profile_paths()
        self.add_missing_servers()
        self.save_updated_mappings()
        
        print("🎉 Domain mapping update completed successfully!")
        print(f"📊 Total servers now mapped: {sum(len(domain.get('primary_servers', [])) for domain in self.current_mappings.get('domain_mappings', {}).values())}")

if __name__ == "__main__":
    updater = DomainMappingUpdater()
    updater.run()