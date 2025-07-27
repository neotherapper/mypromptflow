#!/usr/bin/env python3
"""
Name Resolution System Demonstration
Shows how UUID relationships in frontmatter convert to human-readable markdown links
Demonstrates the dual-layer architecture in action
"""

import yaml
import json
from name_resolution_engine import NameResolutionEngine

def demonstrate_name_resolution():
    """Demonstrate the complete name resolution workflow"""
    
    print("=== Knowledge Vault Name Resolution System Demo ===\n")
    
    # Initialize the name resolution engine
    try:
        engine = NameResolutionEngine()
        print("✅ Name Resolution Engine initialized successfully")
        print(f"📊 Loaded {len(engine.mappings)} UUID mappings\n")
    except Exception as e:
        print(f"❌ Error initializing engine: {e}")
        return
    
    # Example 1: Single UUID Resolution
    print("📝 Example 1: Single UUID Resolution")
    print("-" * 40)
    
    test_uuid = "neon-database-postgres-uuid"
    resolved = engine.resolve_uuid_to_name(test_uuid)
    markdown_link = engine.generate_markdown_link(test_uuid)
    
    print(f"UUID: {test_uuid}")
    print(f"Resolved Name: {resolved.get('name', 'Unknown')}")
    print(f"Display Name: {resolved.get('display_name', 'Unknown')}")
    print(f"Category: {resolved.get('category', 'Unknown')}")
    print(f"Markdown Link: {markdown_link}")
    print()
    
    # Example 2: Multiple UUID Resolution (Relationship Lists)
    print("📝 Example 2: Multiple UUID Relationship Resolution")
    print("-" * 50)
    
    relationship_uuids = [
        "react-framework-uuid",
        "performance-optimization-uuid", 
        "serverless-architecture-uuid"
    ]
    
    print("UUID List:")
    for uuid in relationship_uuids:
        print(f"  - {uuid}")
    
    markdown_links = engine.generate_multiple_markdown_links(relationship_uuids)
    print(f"\nMarkdown Links: {markdown_links}")
    print()
    
    # Example 3: Complete Frontmatter to Markdown Conversion
    print("📝 Example 3: Frontmatter to Markdown Conversion")
    print("-" * 48)
    
    # Sample frontmatter from one of our knowledge vault items
    sample_frontmatter = {
        "uuid": "neon-database-postgres-uuid",
        "name": "Neon",
        "relationships": {
            "knowledge_vault_relations": ["postgresql-uuid", "serverless-architecture-uuid"],
            "training_vault_relations": ["database-course-uuid"],
            "tools_services_relations": ["vercel-uuid", "netlify-uuid"],
            "business_ideas_relations": ["saas-development-uuid"]
        }
    }
    
    print("Sample Frontmatter Relationships:")
    print(json.dumps(sample_frontmatter["relationships"], indent=2))
    
    markdown_relationships = engine.convert_frontmatter_to_markdown_relationships(sample_frontmatter)
    
    print("\nConverted to Human-Readable Markdown:")
    for section_title, markdown_content in markdown_relationships.items():
        print(f"  {markdown_content}")
    print()
    
    # Example 4: Fallback Strategy Demonstration
    print("📝 Example 4: Fallback Strategy for Missing UUIDs")
    print("-" * 48)
    
    missing_uuid = "unknown-technology-uuid"
    fallback_resolved = engine.resolve_uuid_to_name(missing_uuid)
    fallback_link = engine.generate_markdown_link(missing_uuid)
    
    print(f"Missing UUID: {missing_uuid}")
    print(f"Fallback Name: {fallback_resolved.get('name', 'Unknown')}")
    print(f"Fallback Link: {fallback_link}")
    print(f"Status: {fallback_resolved.get('status', 'Unknown')}")
    print()
    
    # Example 5: Dual-Layer Architecture in Action
    print("📝 Example 5: Dual-Layer Architecture Demonstration")
    print("-" * 50)
    
    print("🔧 LAYER 1 (AI Agent Frontmatter - Hidden from Human):")
    print("---")
    print("relationships:")
    print("  knowledge_vault_relations: ['postgresql-uuid', 'serverless-architecture-uuid']")
    print("  tools_services_relations: ['vercel-uuid', 'netlify-uuid']")
    print("---")
    print()
    
    print("👁️ LAYER 2 (Human-Readable Markdown Content):")
    print("## 🔗 Related Technologies")
    print()
    
    tech_uuids = ["postgresql-uuid", "serverless-architecture-uuid"]
    tech_links = engine.generate_multiple_markdown_links(tech_uuids)
    print(f"### Foundation Technologies")
    print(f"- **Database Systems**: {tech_links}")
    print()
    
    tool_uuids = ["vercel-uuid", "netlify-uuid"]
    tool_links = engine.generate_multiple_markdown_links(tool_uuids)
    print(f"### Deployment Platforms")
    print(f"- **Hosting Services**: {tool_links}")
    print()
    
    # Example 6: System Validation and Health Check
    print("📝 Example 6: System Validation Report")
    print("-" * 38)
    
    validation_report = engine.validate_all_references()
    
    print(f"Total Mappings: {validation_report['total_mappings']}")
    print(f"Valid Mappings: {validation_report['validation_results']['valid_mappings']}")
    print(f"Invalid Mappings: {validation_report['validation_results']['invalid_mappings']}")
    
    if validation_report['validation_results']['missing_required_fields']:
        print(f"Missing Fields: {len(validation_report['validation_results']['missing_required_fields'])}")
    
    if validation_report['validation_results']['duplicate_slugs']:
        print(f"Duplicate Slugs: {len(validation_report['validation_results']['duplicate_slugs'])}")
    
    print()
    
    # Example 7: Usage Statistics
    print("📝 Example 7: Usage Statistics")
    print("-" * 30)
    
    stats = engine.get_usage_statistics()
    print(f"Resolutions Performed: {stats['resolutions_performed']}")  
    print(f"Successful Resolutions: {stats['successful_resolutions']}")
    print(f"Fallback Resolutions: {stats['fallback_resolutions']}")
    print(f"Success Rate: {stats['success_rate_percentage']}%")
    print()
    
    # Summary
    print("🎉 Name Resolution System Demo Complete!")
    print("=" * 50)
    print("✅ UUID to human-readable name conversion working")
    print("✅ Dual-layer architecture separation maintained")
    print("✅ Fallback strategies handle missing mappings")
    print("✅ Batch processing for relationship lists")
    print("✅ System validation and health monitoring")
    print("\nThe system successfully converts UUID relationships in AI frontmatter")
    print("to meaningful, human-readable cross-references in markdown content! 🚀")


def demonstrate_template_integration():
    """Show how name resolution integrates with knowledge vault templates"""
    
    print("\n=== Template Integration Demonstration ===\n")
    
    engine = NameResolutionEngine()
    
    # Sample template content with relationship placeholders
    template_content = """
# {{TECHNOLOGY_NAME}}

> {{TECHNOLOGY_DESCRIPTION}}

## 🔗 Related Technologies

{{#if foundation_technologies}}
### Foundation Technologies
{{#each foundation_technologies}}
- [{{name}}]({{slug}}.md) - {{context}}
{{/each}}
{{else}}
- **Database Systems**: {{related_database_links}}
- **Architecture Patterns**: {{related_architecture_links}}
{{/if}}

## 🛠️ Development Tools

{{#if development_tools}}
{{#each development_tools}}
- [{{name}}]({{slug}}.md) - {{description}}
{{/each}}
{{else}}
- **Deployment Platforms**: {{deployment_platform_links}}
{{/if}}
"""

    # Sample frontmatter data
    frontmatter_data = {
        "name": "Neon",
        "relationships": {
            "knowledge_vault_relations": ["postgresql-uuid", "serverless-architecture-uuid"],
            "tools_services_relations": ["vercel-uuid", "netlify-uuid"]
        }
    }
    
    print("📋 Original Template Content:")
    print(template_content[:200] + "..." if len(template_content) > 200 else template_content)
    print()
    
    print("🔄 Applying Name Resolution...")
    
    # Generate resolved relationships
    database_links = engine.generate_markdown_link("postgresql-uuid")
    architecture_links = engine.generate_markdown_link("serverless-architecture-uuid") 
    deployment_links = engine.generate_multiple_markdown_links(["vercel-uuid", "netlify-uuid"])
    
    # Replace placeholders with resolved content
    resolved_template = template_content.replace(
        "{{related_database_links}}", database_links
    ).replace(
        "{{related_architecture_links}}", architecture_links
    ).replace(
        "{{deployment_platform_links}}", deployment_links
    ).replace(
        "{{TECHNOLOGY_NAME}}", "Neon"
    ).replace(
        "{{TECHNOLOGY_DESCRIPTION}}", "Serverless Postgres database platform"
    )
    
    print("✅ Resolved Template Content:")
    print(resolved_template)


if __name__ == "__main__":
    demonstrate_name_resolution()
    demonstrate_template_integration()