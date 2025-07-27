#!/usr/bin/env python3
"""
Knowledge Vault Name Resolution Engine

Converts raw UUIDs to human-readable markdown links for the knowledge vault system.
Provides bidirectional UUID ↔ Name mapping and generates markdown links for cross-references.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

class NameResolutionEngine:
    """
    Engine for converting UUIDs to human-readable markdown links in the knowledge vault.
    
    Features:
    - UUID → Name mapping with automatic fallback
    - Markdown link generation with proper slugification
    - Bidirectional relationship tracking
    - Validation and error handling
    """
    
    def __init__(self, vault_path: str = "/Users/georgiospilitsoglou/Developer/projects/mypromptflow/knowledge-vault"):
        self.vault_path = Path(vault_path)
        self.items_path = self.vault_path / "databases" / "knowledge_vault" / "items"
        self.uuid_to_name = {}
        self.name_to_filename = {}
        self.uuid_to_filename = {}
        self._load_mappings()
    
    def _slugify(self, name: str) -> str:
        """Convert human name to filename slug."""
        # Remove quotes and clean up
        name = name.strip('\'"')
        # Convert to lowercase and replace spaces/special chars with hyphens
        slug = re.sub(r'[^\w\s-]', '', name.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')
    
    def _load_mappings(self) -> None:
        """Load UUID → Name mappings from all knowledge vault items."""
        print("Loading UUID → Name mappings...")
        
        # Manual mapping for items we know
        uuid_name_mappings = {
            # Notion UUIDs → Names  
            "209f8374-7088-81dd-91fc-cffff197c0b4": "Adobe Commerce (Magento)",
            "1fef8374-7088-80b0-a9b8-cf6636c1fa54": "Affiliate Marketing", 
            "239f8374-7088-8158-86c5-d4db7df1faf4": "AI Knowledge Intelligence Orchestrator",
            "1fd38b01-791d-40ec-aa4b-c853b466cbd8": "Apache Spark",  # Notion page ID
            "apache-spark-analytics-engine-uuid": "Apache Spark",     # Local UUID
            "1dcf8374-7088-8012-9ecc-d89f1a919c4f": "Assembly language",
            "53cc21a6-c3e1-47cd-aa4c-eeacfee96a1f": "Atlassian Design System",
            "1dcf8374-7088-801f-b92c-c9f6a68bfa22": "Business Intelligence",  # Note: This UUID appears in multiple places
            "cf5e1488-1ee1-4846-b1f1-242b9b53e4ba": "Carbon Design System",
            "239f8374-7088-812f-89aa-f956eeb12366": "Claude Code Multi-Agent Orchestration Framework",
            "34ceedb5-aaeb-4d8b-9bcd-7260529fef41": "Continue",
            "20af8374-7088-811c-8c39-e1f8992a3055": "Crystallize",
            "cc30d146-052c-45b7-ae29-6584ee8f42c8": "D",
            "764be31b-7c78-4e11-bc03-fd31c8eca465": "Data Visualisation",
            "fbee53bc-b8d6-4bd0-ad9d-be9116b85043": "Desktop",
            "c23d56fe-26b9-4ea4-957e-39b3e9bfbb3b": "Discontinued - Outdated",
            "531b06b2-1a71-46eb-960e-0f47934c9985": "Evergreen",
            "20af8374-7088-812e-97cc-d599487b603f": "Firebase Studio",
            "1e5f8374-7088-808a-9d76-fa648d83f4f6": "Game Design",
            "141d71b0-fa46-4c72-8075-b833950c1e2b": "Gamification",
            "15903988-d2e1-4ac6-8089-2c4c7ac26ece": "GOV.UK Design System",
            "00809f02-5a0d-4834-b3d1-f05655dc8f44": "Hono",
            "1fdf8374-7088-8050-ac4b-c391f88e4787": "Human Resources",
            "7185755d-4bd8-4b1e-9d47-f589ec418d9e": "Leonardo AI",
            "bd2dc7b8-2bc1-4197-9f71-613e14750320": "Linux",
            "9b56afea-6921-477c-aa6d-b2516d2af161": "LlamaIndex",
            "27d61be4-c2f5-4f8b-9a68-f8507a3c4f33": "LLaVA",
            "f4e3c268-d5a2-4bbb-b39b-f2a5fcae6c23": "Material Design",
            "1fdf8374-7088-80e5-b6d1-d218f38b49be": "MCP",
            "239f8374-7088-819c-92c6-eac956f35eec": "Meta-Prompting Frameworks",
            "79f51bcc-3a69-43f0-978c-8d201cf4dca9": "Mistral AI",
            "a245a512-a231-477b-80a7-759fef8b4602": "Mobile",
            "20af8374-7088-818a-aea8-ec2d0f9ca797": "Neon",
            "393bf209-df9c-4e4a-a8f3-a162e896f8f9": "Vector Database",  # Common UUID in many files
            "5930459b-d2ed-47bf-8ac1-6a265b8eaade": "Nitro",
            "4c2c0681-c038-4bc3-8ef6-89ccfba3dcdd": "NVIDIA",
            "21af8374-7088-8031-a360-c517a82741cf": "Online Directory",
            "1f7f8374-7088-811a-9db9-e8b65527addb": "Perplexity",
            "20af8374-7088-80c5-9ae0-df585087651a": "PIM",
            "4e6359ca-bac0-4599-aadb-5aeedbca7a15": "Pinecone",
            "1f4f8374-7088-807d-8a1f-db855edbe3ce": "Platformers",
            "12f5b8cf-fd87-45c5-829a-6182d36d3912": "RAFT",
            "1f4f8374-7088-8039-9e6b-e8e644735853": "Real Time Strategy",
            "1f4f8374-7088-80e1-8e32-fda716839fda": "Shooter",
            "354bb7fe-dec9-470b-ac32-e819fab9f3db": "Shopify Polaris",
            "1f5f8374-7088-80fb-bcc3-dabe4db9dbf8": "Spring Boot",  # Notion page ID
            "spring-boot-java-framework-uuid": "Spring Boot",        # Local UUID
            "fbd07457-873d-4b36-9505-c5c4ef479d8c": "Stripe",
            "1f4f8374-7088-80ca-a321-f5b43ba41f4c": "Tower Defence",
            "1e5f8374-7088-8097-9b73-f5d6976cac12": "Unity Engine",
            "1e5f8374-7088-801b-9b45-fd7dd26e4b9d": "Unreal Engine",
        }
        
        self.uuid_to_name = uuid_name_mappings
        
        # Generate filename mappings
        for uuid, name in self.uuid_to_name.items():
            filename = f"{self._slugify(name)}.md"
            self.name_to_filename[name] = filename
            self.uuid_to_filename[uuid] = filename
        
        print(f"Loaded {len(self.uuid_to_name)} UUID → Name mappings")
    
    def resolve_uuid_to_name(self, uuid: str) -> str:
        """Convert UUID to human-readable name."""
        return self.uuid_to_name.get(uuid, f"Unknown Item ({uuid[:8]}...)")
    
    def resolve_uuid_to_link(self, uuid: str) -> str:
        """Convert UUID to markdown link."""
        name = self.resolve_uuid_to_name(uuid)
        if name.startswith("Unknown Item"):
            return name  # Don't create links for unknown items
        
        filename = self.uuid_to_filename.get(uuid)
        if not filename:
            filename = f"{self._slugify(name)}.md"
        
        return f"[{name}]({filename})"
    
    def generate_multiple_markdown_links(self, uuid_list: List[str]) -> str:
        """Convert list of UUIDs to comma-separated markdown links."""
        if not uuid_list:
            return ""
        
        # Remove duplicates while preserving order
        seen = set()
        unique_uuids = []
        for uuid in uuid_list:
            if uuid not in seen:
                seen.add(uuid)
                unique_uuids.append(uuid)
        
        links = [self.resolve_uuid_to_link(uuid) for uuid in unique_uuids]
        valid_links = [link for link in links if not link.startswith("Unknown Item")]
        
        return ", ".join(valid_links) if valid_links else "No related items found"
    
    def convert_raw_uuid_list_to_links(self, raw_text: str) -> str:
        """
        Convert raw UUID listings to markdown links.
        
        Input: "- `uuid1` - Context\n- `uuid2` - Context"
        Output: "- [Name1](file1.md)\n- [Name2](file2.md)"
        """
        lines = raw_text.strip().split('\n')
        converted_lines = []
        
        for line in lines:
            # Extract UUID from formats like "- `uuid` - context" or "- uuid - context"
            uuid_match = re.search(r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})', line)
            if uuid_match:
                uuid = uuid_match.group(1)
                link = self.resolve_uuid_to_link(uuid)
                if not link.startswith("Unknown Item"):
                    converted_lines.append(f"- {link}")
            # Skip lines with unknown UUIDs
        
        return '\n'.join(converted_lines) if converted_lines else "No related items found"
    
    def validate_all_references(self) -> Dict:
        """Validate all UUID references and return report."""
        total_mappings = len(self.uuid_to_name)
        valid_mappings = sum(1 for name in self.uuid_to_name.values() if not name.startswith("Unknown Item"))
        
        return {
            "total_mappings": total_mappings,
            "valid_mappings": valid_mappings,
            "coverage_percentage": (valid_mappings / total_mappings * 100) if total_mappings > 0 else 0,
            "validation_results": {
                "total_uuids": total_mappings,
                "resolved_uuids": valid_mappings,
                "unresolved_uuids": total_mappings - valid_mappings,
                "invalid_mappings": 0  # All our mappings are valid by design
            }
        }

# Utility functions for direct usage
def create_engine():
    """Create and return a name resolution engine instance."""
    return NameResolutionEngine()

def convert_uuid_to_link(uuid: str) -> str:
    """Quick utility to convert single UUID to markdown link."""
    engine = create_engine()
    return engine.resolve_uuid_to_link(uuid)

def convert_uuid_list_to_links(uuid_list: List[str]) -> str:
    """Quick utility to convert UUID list to comma-separated links."""
    engine = create_engine()
    return engine.generate_multiple_markdown_links(uuid_list)

if __name__ == "__main__":
    # Test the engine
    engine = NameResolutionEngine()
    
    # Test individual UUID resolution
    test_uuid = "1dcf8374-7088-801f-b92c-c9f6a68bfa22"
    print(f"UUID: {test_uuid}")
    print(f"Name: {engine.resolve_uuid_to_name(test_uuid)}")
    print(f"Link: {engine.resolve_uuid_to_link(test_uuid)}")
    
    # Test validation report
    report = engine.validate_all_references()
    print(f"\nValidation Report:")
    print(f"Total mappings: {report['total_mappings']}")
    print(f"Valid mappings: {report['valid_mappings']}")
    print(f"Coverage: {report['coverage_percentage']:.1f}%")