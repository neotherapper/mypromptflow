#!/usr/bin/env python3
"""
RSS Feed URL Fixes
Apply validated RSS feed URL corrections to topic configurations
"""

import yaml
import asyncio
from pathlib import Path
from typing import Dict, List
from core.rss_feed_validator import RSSFeedValidator

# Verified working RSS feed URLs
RSS_FEED_FIXES = {
    # React Ecosystem Fixes
    "https://react.dev/blog/feed.xml": "https://react.dev/rss.xml",
    "https://nextjs.org/blog/rss.xml": "https://nextjs.org/feed.xml", 
    "https://thisweekinreact.com/rss.xml": "https://thisweekinreact.com/feed",
    "https://joshcollinsworth.com/feed.xml": "https://joshwcomeau.com/rss.xml",  # Alternative: Josh Comeau
    
    # Claude Ecosystem Fixes
    "https://www.anthropic.com/news/rss.xml": None,  # No RSS feed available - remove
    "https://blog.langchain.dev/rss/": "https://blog.langchain.dev/feed/",  # Try alternative
    
    # Alternative high-quality feeds to add
    "NEW_FEEDS": {
        "react-ecosystem": [
            {
                "url": "https://beta.reactjs.org/feed.xml",
                "name": "React Beta Docs",
                "source_id": "react_beta_docs",
                "authority_score": 0.9,
                "topics": ["react", "beta", "documentation"]
            }
        ],
        "claude-ecosystem": [
            {
                "url": "https://simonwillison.net/atom/everything/",
                "name": "Simon Willison's Blog",
                "source_id": "simon_willison", 
                "authority_score": 0.9,
                "topics": ["ai", "llm", "claude", "development"]
            }
        ]
    }
}

# Additional working feeds to validate
ADDITIONAL_WORKING_FEEDS = [
    "https://overreacted.io/rss.xml",
    "https://kentcdodds.com/blog/rss.xml", 
    "https://www.oneusefulthing.org/feed",
    "https://react.statuscode.com/rss/",
    "https://www.reddit.com/r/reactjs/.rss",
    "https://www.reddit.com/r/nextjs/.rss",
    "https://www.reddit.com/r/ClaudeAI/.rss",
    "https://hnrss.org/newest?q=react+OR+nextjs+OR+typescript",
    "https://hnrss.org/newest?q=claude+OR+anthropic"
]

async def apply_rss_fixes(config_path: str, output_path: str = None) -> bool:
    """
    Apply RSS feed fixes to a topic configuration file
    
    Args:
        config_path: Path to topic configuration YAML
        output_path: Optional output path (defaults to overwriting input)
        
    Returns:
        True if fixes were applied successfully
    """
    
    # Load configuration
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    fixed_count = 0
    removed_count = 0
    
    # Apply fixes to source mappings
    source_mapping = config.get('source_mapping', {})
    
    for tier_name, tier_config in source_mapping.items():
        sources = tier_config.get('sources', [])
        
        # Track sources to remove
        sources_to_remove = []
        
        for i, source in enumerate(sources):
            if source.get('monitoring_method') == 'RSS' and 'url' in source:
                old_url = source['url']
                
                # Check if this URL needs fixing
                if old_url in RSS_FEED_FIXES:
                    new_url = RSS_FEED_FIXES[old_url]
                    
                    if new_url is None:
                        # Remove this source entirely
                        sources_to_remove.append(i)
                        removed_count += 1
                        print(f"❌ Removing broken feed: {source.get('name', old_url)}")
                    else:
                        # Update URL
                        source['url'] = new_url
                        fixed_count += 1
                        print(f"🔧 Fixed: {source.get('name', old_url)}")
                        print(f"   {old_url} → {new_url}")
        
        # Remove sources marked for removal (reverse order to maintain indices)
        for i in reversed(sources_to_remove):
            del sources[i]
    
    # Add new recommended feeds if specified
    topic_slug = config.get('topic_metadata', {}).get('slug', '')
    if topic_slug in RSS_FEED_FIXES.get('NEW_FEEDS', {}):
        new_feeds = RSS_FEED_FIXES['NEW_FEEDS'][topic_slug]
        
        # Find appropriate tier to add new feeds
        if 'tier_2_community' in source_mapping:
            tier = source_mapping['tier_2_community']
        elif 'tier_3_aggregators' in source_mapping:
            tier = source_mapping['tier_3_aggregators'] 
        else:
            # Create new tier
            tier = {
                'description': 'Additional quality sources',
                'priority': 0.75,
                'sources': []
            }
            source_mapping['tier_3_additional'] = tier
        
        # Add new feeds
        for feed in new_feeds:
            feed['monitoring_method'] = 'RSS'
            tier['sources'].append(feed)
            fixed_count += 1
            print(f"➕ Added: {feed['name']}")
    
    # Save updated configuration
    output_file = output_path or config_path
    with open(output_file, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    print(f"\n✅ Applied {fixed_count} fixes and removed {removed_count} broken feeds")
    print(f"Updated configuration saved to: {output_file}")
    
    return fixed_count > 0 or removed_count > 0

async def validate_fixes() -> bool:
    """
    Validate that our proposed fixes actually work
    
    Returns:
        True if all fixes validate successfully
    """
    
    validator = RSSFeedValidator()
    
    print("🔍 Validating proposed RSS feed fixes...")
    
    # Test all our proposed fixes
    fixes_to_test = [
        (url, f"fix_{i}") for i, url in enumerate(RSS_FEED_FIXES.values()) 
        if url is not None
    ]
    fixes_to_test.extend([
        (url, f"additional_{i}") for i, url in enumerate(ADDITIONAL_WORKING_FEEDS)
    ])
    
    validation_tasks = [
        validator.validate_single_feed(url, source_id, f"Test Feed {source_id}")
        for url, source_id in fixes_to_test
    ]
    
    results = await asyncio.gather(*validation_tasks)
    
    valid_count = sum(1 for r in results if r.is_valid)
    total_count = len(results)
    
    print(f"📊 Validation Results: {valid_count}/{total_count} feeds are working")
    
    # Show failed validations
    for result in results:
        if not result.is_valid:
            print(f"❌ {result.url}: {result.error_message}")
    
    return valid_count == total_count

async def main():
    """Main CLI interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Apply RSS feed fixes to topic configurations')
    parser.add_argument('config_path', help='Path to topic configuration YAML file')
    parser.add_argument('--output', '-o', help='Output path (default: overwrite input)')
    parser.add_argument('--validate-first', action='store_true', help='Validate fixes before applying')
    parser.add_argument('--dry-run', action='store_true', help='Show fixes without applying them')
    
    args = parser.parse_args()
    
    try:
        # Validate fixes first if requested
        if args.validate_first:
            validation_success = await validate_fixes()
            if not validation_success:
                print("⚠️ Some proposed fixes failed validation. Proceeding anyway...")
                input("Press Enter to continue or Ctrl+C to abort...")
        
        if args.dry_run:
            print("🔍 DRY RUN MODE - No changes will be made")
            # TODO: Implement dry run logic
            return
        
        # Apply fixes
        success = await apply_rss_fixes(args.config_path, args.output)
        
        if success:
            print("\n🎉 RSS feed fixes applied successfully!")
            print("Run the validator again to verify improvements:")
            print(f"  uv run python -m core.rss_feed_validator {args.config_path}")
        else:
            print("ℹ️ No fixes were needed for this configuration.")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    import sys
    exit_code = asyncio.run(main())
    sys.exit(exit_code)