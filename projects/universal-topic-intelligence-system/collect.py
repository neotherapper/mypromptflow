#!/usr/bin/env python3
"""
RSS Collection CLI for Universal Topic Intelligence System
Collects RSS feeds from sources.yaml and stores them in SQLite database
"""

import yaml
import sys
import argparse
import logging
from pathlib import Path
from intelligence_system import TopicIntelligence

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_sources_config(config_path="sources.yaml"):
    """Load sources configuration from YAML file"""
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        logger.error(f"Sources configuration file not found: {config_path}")
        return None
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file: {e}")
        return None

def collect_all_sources(config, db_path="intelligence.db"):
    """Collect from all RSS sources in the configuration"""
    if not config or 'sources' not in config:
        logger.error("Invalid configuration: no sources found")
        return False
    
    total_collected = 0
    total_sources = len(config['sources'])
    
    with TopicIntelligence(db_path) as system:
        logger.info(f"Starting collection from {total_sources} sources...")
        
        for tool_name, source_info in config['sources'].items():
            if 'rss_url' not in source_info:
                logger.warning(f"No RSS URL found for {tool_name}, skipping...")
                continue
            
            logger.info(f"Collecting from {tool_name} ({source_info.get('source_name', 'Unknown')})")
            
            try:
                # Collect from this source
                collected = system.collect_from_source(
                    feed_url=source_info['rss_url'],
                    tool_name=tool_name
                )
                
                total_collected += collected
                logger.info(f"✓ {tool_name}: {collected} new articles")
                
            except Exception as e:
                logger.error(f"✗ {tool_name}: Failed to collect - {e}")
    
    logger.info(f"Collection complete: {total_collected} total new articles from {total_sources} sources")
    return True

def collect_specific_tools(tools, config, db_path="intelligence.db"):
    """Collect from specific tools only"""
    if not config or 'sources' not in config:
        logger.error("Invalid configuration: no sources found")
        return False
    
    total_collected = 0
    
    with TopicIntelligence(db_path) as system:
        for tool_name in tools:
            if tool_name not in config['sources']:
                logger.warning(f"Tool '{tool_name}' not found in configuration, skipping...")
                continue
            
            source_info = config['sources'][tool_name]
            if 'rss_url' not in source_info:
                logger.warning(f"No RSS URL found for {tool_name}, skipping...")
                continue
            
            logger.info(f"Collecting from {tool_name} ({source_info.get('source_name', 'Unknown')})")
            
            try:
                collected = system.collect_from_source(
                    feed_url=source_info['rss_url'],
                    tool_name=tool_name
                )
                
                total_collected += collected
                logger.info(f"✓ {tool_name}: {collected} new articles")
                
            except Exception as e:
                logger.error(f"✗ {tool_name}: Failed to collect - {e}")
    
    logger.info(f"Collection complete: {total_collected} total new articles")
    return True

def show_sources(config):
    """Display available sources"""
    if not config or 'sources' not in config:
        logger.error("Invalid configuration: no sources found")
        return
    
    print("\n📰 Available RSS Sources:")
    print("=" * 50)
    
    for tool_name, source_info in config['sources'].items():
        source_name = source_info.get('source_name', 'Unknown')
        keywords = ', '.join(source_info.get('keywords', []))
        
        print(f"\n🔧 {tool_name}")
        print(f"   Source: {source_name}")
        print(f"   URL: {source_info.get('rss_url', 'No URL')}")
        if keywords:
            print(f"   Keywords: {keywords}")

def show_stats(db_path="intelligence.db"):
    """Show database statistics"""
    with TopicIntelligence(db_path) as system:
        stats = system.get_stats()
        
        print("\n📊 Database Statistics:")
        print("=" * 30)
        print(f"Total Articles: {stats['total_articles']}")
        print(f"Recent Articles (7 days): {stats['recent_articles']}")
        
        if stats['date_range']['earliest'] and stats['date_range']['latest']:
            print(f"Date Range: {stats['date_range']['earliest'][:10]} to {stats['date_range']['latest'][:10]}")
        
        print(f"\n📈 Articles by Tool:")
        for tool, count in list(stats['by_tool'].items())[:10]:  # Top 10
            print(f"   {tool}: {count} articles")

def main():
    parser = argparse.ArgumentParser(description="RSS Collection CLI for Topic Intelligence")
    parser.add_argument('--config', '-c', default='sources.yaml', 
                       help='Path to sources configuration file (default: sources.yaml)')
    parser.add_argument('--db', '-d', default='intelligence.db',
                       help='Path to SQLite database file (default: intelligence.db)')
    
    # Action arguments
    parser.add_argument('--collect-all', action='store_true',
                       help='Collect from all RSS sources')
    parser.add_argument('--collect', nargs='+', metavar='TOOL',
                       help='Collect from specific tools (e.g., --collect React TypeScript)')
    parser.add_argument('--list-sources', action='store_true',
                       help='List all available RSS sources')
    parser.add_argument('--stats', action='store_true',
                       help='Show database statistics')
    
    # Logging level
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Minimize output (errors only)')
    
    args = parser.parse_args()
    
    # Configure logging level
    if args.quiet:
        logging.getLogger().setLevel(logging.ERROR)
    elif args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Load configuration
    config = load_sources_config(args.config)
    if not config:
        sys.exit(1)
    
    # Execute actions
    try:
        if args.list_sources:
            show_sources(config)
            
        elif args.stats:
            show_stats(args.db)
            
        elif args.collect_all:
            success = collect_all_sources(config, args.db)
            if not success:
                sys.exit(1)
                
        elif args.collect:
            success = collect_specific_tools(args.collect, config, args.db)
            if not success:
                sys.exit(1)
                
        else:
            # No action specified, show help
            parser.print_help()
            print("\nExamples:")
            print("  python collect.py --collect-all                    # Collect from all sources")
            print("  python collect.py --collect React TypeScript       # Collect from specific tools")
            print("  python collect.py --list-sources                   # Show available sources")
            print("  python collect.py --stats                          # Show database stats")
            
    except KeyboardInterrupt:
        logger.info("\nCollection interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()