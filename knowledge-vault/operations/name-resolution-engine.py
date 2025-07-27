#!/usr/bin/env python3
"""
Name Resolution Engine - UUID to Human-Readable Cross-Reference Converter
Enables dual-layer architecture by converting UUID relationships to meaningful markdown links
Part of the Knowledge Vault system for AI agent operations
"""

import yaml
import re
import logging
from typing import Dict, List, Optional, Tuple, Union
from pathlib import Path
from datetime import datetime
import json

class NameResolutionError(Exception):
    """Custom exception for name resolution issues"""
    pass

class NameResolutionEngine:
    """
    Core engine for converting UUID relationships to human-readable markdown links
    Supports the dual-layer architecture by maintaining separation between AI metadata and human content
    """
    
    def __init__(self, index_path: str = None):
        """
        Initialize the name resolution engine
        
        Args:
            index_path: Path to the name resolution index YAML file
        """
        self.index_path = index_path or "knowledge-vault/operations/name-resolution-index.yaml"
        self.mappings = {}
        self.fallback_strategies = {}
        self.usage_stats = {
            "resolutions_performed": 0,
            "successful_resolutions": 0,
            "fallback_resolutions": 0,
            "failed_resolutions": 0
        }
        
        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Load the name resolution index
        self.load_index()
    
    def load_index(self) -> None:
        """Load the name resolution index from YAML file"""
        try:
            with open(self.index_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
                
            # Consolidate all mappings into a single dictionary
            self.mappings = {}
            for db_key in ['knowledge_vault_mappings', 'training_vault_mappings', 
                          'tools_services_mappings', 'platforms_sites_mappings',
                          'business_ideas_mappings', 'notes_ideas_mappings']:
                if db_key in data:
                    self.mappings.update(data[db_key])
            
            # Load fallback strategies
            self.fallback_strategies = data.get('fallback_strategies', {})
            
            self.logger.info(f"Loaded {len(self.mappings)} name mappings from index")
            
        except FileNotFoundError:
            self.logger.error(f"Name resolution index not found at {self.index_path}")
            raise NameResolutionError(f"Index file not found: {self.index_path}")
        except yaml.YAMLError as e:
            self.logger.error(f"Error parsing index YAML: {e}")
            raise NameResolutionError(f"Invalid YAML in index file: {e}")
    
    def resolve_uuid_to_name(self, uuid: str) -> Dict[str, str]:
        """
        Resolve a single UUID to human-readable information
        
        Args:
            uuid: The UUID to resolve
            
        Returns:
            Dictionary with name, display_name, slug, and other metadata
        """
        self.usage_stats["resolutions_performed"] += 1
        
        if uuid in self.mappings:
            self.usage_stats["successful_resolutions"] += 1
            return self.mappings[uuid]
        
        # Try fallback strategies
        return self._apply_fallback_strategy(uuid)
    
    def resolve_multiple_uuids(self, uuids: List[str]) -> Dict[str, Dict[str, str]]:
        """
        Resolve multiple UUIDs in batch for efficiency
        
        Args:
            uuids: List of UUIDs to resolve
            
        Returns:
            Dictionary mapping UUIDs to their resolved information
        """
        results = {}
        for uuid in uuids:
            results[uuid] = self.resolve_uuid_to_name(uuid)
        return results
    
    def generate_markdown_link(self, uuid: str, context: str = None) -> str:
        """
        Generate a markdown link from UUID
        
        Args:
            uuid: The UUID to convert to a markdown link
            context: Optional context for link formatting
            
        Returns:
            Formatted markdown link
        """
        resolved = self.resolve_uuid_to_name(uuid)
        
        if resolved.get('status') == 'resolved':
            display_name = resolved.get('display_name', resolved.get('name', uuid))
            slug = resolved.get('slug', uuid)
            return f"[{display_name}]({slug}.md)"
        else:
            return resolved.get('fallback_link', f"[Missing Item: {uuid}](missing-{uuid}.md)")
    
    def generate_multiple_markdown_links(self, uuids: List[str], 
                                       separator: str = ", ",
                                       context: str = None) -> str:
        """
        Generate multiple markdown links joined by separator
        
        Args:
            uuids: List of UUIDs to convert
            separator: String to join links with
            context: Optional context for formatting
            
        Returns:
            Comma-separated markdown links
        """
        links = [self.generate_markdown_link(uuid, context) for uuid in uuids]
        return separator.join(links)
    
    def convert_frontmatter_to_markdown_relationships(self, frontmatter: Dict) -> Dict[str, str]:
        """
        Convert UUID relationships from frontmatter to human-readable markdown sections
        
        Args:
            frontmatter: Dictionary containing frontmatter with UUID relationships
            
        Returns:
            Dictionary with markdown-formatted relationship sections
        """
        markdown_sections = {}
        
        if 'relationships' not in frontmatter:
            return markdown_sections
        
        relationships = frontmatter['relationships']
        
        # Define relationship type mappings
        relationship_mappings = {
            'knowledge_vault_relations': 'Related Knowledge',
            'training_vault_relations': 'Learning Resources', 
            'tools_services_relations': 'Tools & Services',
            'platforms_sites_relations': 'Platforms & Sites',
            'business_ideas_relations': 'Business Applications',
            'notes_ideas_relations': 'Notes & Ideas'
        }
        
        for rel_type, uuids in relationships.items():
            if uuids and rel_type in relationship_mappings:
                section_title = relationship_mappings[rel_type]
                if isinstance(uuids, list) and uuids:
                    links = self.generate_multiple_markdown_links(uuids)
                    markdown_sections[section_title] = f"- **{section_title}**: {links}"
        
        return markdown_sections
    
    def apply_template_name_resolution(self, template_content: str, 
                                     frontmatter: Dict) -> str:
        """
        Apply name resolution to template content using frontmatter UUID data
        
        Args:
            template_content: Template content with placeholders
            frontmatter: Frontmatter containing UUID relationships
            
        Returns:
            Template content with resolved names
        """
        # Convert UUID relationships to markdown
        markdown_relationships = self.convert_frontmatter_to_markdown_relationships(frontmatter)
        
        # Replace relationship placeholders in template
        resolved_content = template_content
        
        for section_title, markdown_content in markdown_relationships.items():
            # Replace placeholders like {{#if related_technologies}}
            placeholder_pattern = r'\{\{#if\s+' + section_title.lower().replace(' ', '_') + r'.*?\{\{/if\}\}'
            if re.search(placeholder_pattern, resolved_content, re.DOTALL):
                resolved_content = re.sub(placeholder_pattern, markdown_content, 
                                        resolved_content, flags=re.DOTALL)
        
        return resolved_content
    
    def validate_all_references(self) -> Dict[str, any]:
        """
        Validate integrity of all references in the knowledge vault system
        
        Returns:
            Comprehensive validation report
        """
        validation_report = {
            "timestamp": datetime.now().isoformat(),
            "total_mappings": len(self.mappings),
            "validation_results": {
                "valid_mappings": 0,
                "invalid_mappings": 0,
                "missing_required_fields": [],
                "duplicate_slugs": [],
                "orphaned_references": []
            },
            "recommendations": []
        }
        
        # Validate mapping completeness
        required_fields = ['name', 'slug', 'category']
        slugs_seen = set()
        
        for uuid, mapping in self.mappings.items():
            is_valid = True
            
            # Check required fields
            for field in required_fields:
                if field not in mapping or not mapping[field]:
                    validation_report["validation_results"]["missing_required_fields"].append(
                        {"uuid": uuid, "missing_field": field}
                    )
                    is_valid = False
            
            # Check for duplicate slugs
            slug = mapping.get('slug')
            if slug:
                if slug in slugs_seen:
                    validation_report["validation_results"]["duplicate_slugs"].append(
                        {"uuid": uuid, "duplicate_slug": slug}
                    )
                    is_valid = False
                else:
                    slugs_seen.add(slug)
            
            if is_valid:
                validation_report["validation_results"]["valid_mappings"] += 1
            else:
                validation_report["validation_results"]["invalid_mappings"] += 1
        
        # Generate recommendations
        if validation_report["validation_results"]["missing_required_fields"]:
            validation_report["recommendations"].append(
                "Update mappings with missing required fields"
            )
        
        if validation_report["validation_results"]["duplicate_slugs"]:
            validation_report["recommendations"].append(
                "Resolve duplicate slug conflicts"
            )
        
        return validation_report
    
    def _apply_fallback_strategy(self, uuid: str) -> Dict[str, str]:
        """
        Apply fallback strategy for unresolved UUIDs
        
        Args:
            uuid: The UUID that couldn't be resolved
            
        Returns:
            Fallback resolution information
        """
        self.usage_stats["fallback_resolutions"] += 1
        
        missing_strategy = self.fallback_strategies.get('missing_uuid', {})
        
        # Try to extract meaningful name from UUID
        extracted_name = self._extract_name_from_uuid(uuid)
        
        fallback_result = {
            "status": "fallback",
            "name": extracted_name,
            "display_name": extracted_name,
            "slug": uuid.replace('-uuid', '').replace('_', '-'),
            "category": "unknown",
            "fallback_link": missing_strategy.get('format', '[Missing Item: {{uuid}}]').replace('{{uuid}}', uuid),
            "requires_manual_resolution": True
        }
        
        # Log for manual resolution
        self.logger.warning(f"UUID not found in index: {uuid}, using fallback strategy")
        
        return fallback_result
    
    def _extract_name_from_uuid(self, uuid: str) -> str:
        """
        Extract a human-readable name from UUID structure
        
        Args:
            uuid: The UUID to extract name from
            
        Returns:
            Best-guess human-readable name
        """
        # Remove common UUID suffixes
        cleaned = uuid.replace('-uuid', '').replace('_uuid', '')
        
        # Convert underscores and hyphens to spaces and title case
        name_parts = re.split(r'[-_]', cleaned)
        name = ' '.join(word.capitalize() for word in name_parts if word)
        
        return name or uuid
    
    def get_usage_statistics(self) -> Dict[str, any]:
        """
        Get usage statistics for monitoring and optimization
        
        Returns:
            Usage statistics and performance metrics  
        """
        total_attempts = self.usage_stats["resolutions_performed"]
        if total_attempts > 0:
            success_rate = (self.usage_stats["successful_resolutions"] / total_attempts) * 100
            fallback_rate = (self.usage_stats["fallback_resolutions"] / total_attempts) * 100
        else:
            success_rate = fallback_rate = 0
        
        return {
            **self.usage_stats,
            "success_rate_percentage": round(success_rate, 2),
            "fallback_rate_percentage": round(fallback_rate, 2),
            "total_mappings_available": len(self.mappings)
        }
    
    def update_index_from_notion_data(self, notion_data: Dict) -> Dict[str, any]:
        """
        Update the name resolution index from fresh Notion database data
        
        Args:
            notion_data: Data retrieved from Notion API
            
        Returns:
            Update report with statistics
        """
        update_report = {
            "timestamp": datetime.now().isoformat(),
            "items_processed": 0,
            "new_mappings": 0,
            "updated_mappings": 0,
            "errors": []
        }
        
        # Process Notion data and update mappings
        # This would integrate with the actual Notion MCP integration
        # Implementation depends on specific Notion data structure
        
        self.logger.info("Name resolution index updated from Notion data")
        return update_report


def main():
    """
    Command-line interface for name resolution engine
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="Knowledge Vault Name Resolution Engine")
    parser.add_argument("--resolve", type=str, help="Resolve a single UUID")
    parser.add_argument("--validate", action="store_true", help="Validate all references")
    parser.add_argument("--stats", action="store_true", help="Show usage statistics")
    parser.add_argument("--index-path", type=str, help="Path to name resolution index")
    
    args = parser.parse_args()
    
    try:
        engine = NameResolutionEngine(args.index_path)
        
        if args.resolve:
            result = engine.resolve_uuid_to_name(args.resolve)
            print(json.dumps(result, indent=2))
            
        elif args.validate:
            report = engine.validate_all_references()
            print(json.dumps(report, indent=2))
            
        elif args.stats:
            stats = engine.get_usage_statistics()
            print(json.dumps(stats, indent=2))
            
        else:
            # Interactive mode
            print("Knowledge Vault Name Resolution Engine")
            print("Enter UUIDs to resolve (or 'quit' to exit):")
            
            while True:
                uuid_input = input("> ").strip()
                if uuid_input.lower() in ['quit', 'exit', 'q']:
                    break
                
                if uuid_input:
                    try:
                        result = engine.resolve_uuid_to_name(uuid_input)
                        link = engine.generate_markdown_link(uuid_input)
                        print(f"Resolved: {result.get('name', 'Unknown')}")
                        print(f"Markdown: {link}")
                    except Exception as e:
                        print(f"Error: {e}")
    
    except Exception as e:
        print(f"Error initializing name resolution engine: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())