#!/usr/bin/env python3
"""
Query CLI for Universal Topic Intelligence System
Natural language queries and searches for development tool updates
"""

import sys
import argparse
import logging
from datetime import datetime, timedelta
from intelligence_system import TopicIntelligence

# Configure logging
logging.basicConfig(
    level=logging.WARNING,  # Quiet by default for cleaner output
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def format_results(results, query, result_type="search"):
    """Format and display search results nicely"""
    if not results:
        print(f"❌ No results found for: {query}")
        return
    
    print(f"\n🔍 Results for: {query}")
    print("=" * 60)
    
    for i, result in enumerate(results, 1):
        if result_type == "digest":
            # Digest is already formatted
            print(result)
            return
            
        # Standard result format
        title = result[0]
        tool = result[1]
        url = result[2]
        
        print(f"\n{i}. 📰 {title}")
        print(f"   🔧 Tool: {tool}")
        print(f"   🔗 URL: {url}")
        
        # Show additional fields if available
        if len(result) > 3:
            if result_type == "whats_new" and len(result) > 3:
                days_ago = result[3]
                print(f"   📅 Published: {days_ago} days ago")
            elif len(result) > 4:
                published_date = result[4]
                if published_date:
                    print(f"   📅 Published: {published_date[:10]}")
        
        # Show content preview for full-text search
        if len(result) > 3 and result_type == "search":
            content = result[3]
            if content and len(content) > 100:
                preview = content[:200] + "..."
                print(f"   📝 Preview: {preview}")
    
    print(f"\n📊 Found {len(results)} result{'s' if len(results) != 1 else ''}")

def interactive_mode(db_path="intelligence.db"):
    """Interactive query mode"""
    print("🤖 Welcome to Universal Topic Intelligence!")
    print("=" * 45)
    print("Ask natural language questions about development tools.")
    print("Examples:")
    print("  • What's new in React this week?")
    print("  • Show me TypeScript updates")
    print("  • Security updates across all tools")
    print("  • Give me a daily digest")
    print("\nType 'help' for more commands, or 'quit' to exit.\n")
    
    with TopicIntelligence(db_path) as system:
        while True:
            try:
                query = input("❓ Your question: ").strip()
                
                if not query:
                    continue
                    
                if query.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                    
                if query.lower() in ['help', 'h']:
                    show_help_commands()
                    continue
                    
                if query.lower() in ['stats', 'status']:
                    show_interactive_stats(system)
                    continue
                    
                if query.lower().startswith('digest'):
                    # Extract days if specified
                    parts = query.lower().split()
                    days = 1  # default
                    if len(parts) > 1 and parts[1].isdigit():
                        days = int(parts[1])
                    
                    digest = system.generate_digest(days)
                    format_results([digest], f"Daily digest ({days} days)", "digest")
                    continue
                    
                if query.lower().startswith('security'):
                    # Security updates
                    parts = query.lower().split()
                    days = 90  # default
                    if len(parts) > 2 and parts[2].isdigit():
                        days = int(parts[2])
                    
                    results = system.find_security_updates(days)
                    format_results(results, f"Security updates (last {days} days)", "security")
                    continue
                
                # Regular query
                results = system.query(query)
                
                # Determine result type for formatting
                if "what's new" in query.lower() or "whats new" in query.lower():
                    format_results(results, query, "whats_new")
                else:
                    format_results(results, query, "search")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except EOFError:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def show_help_commands():
    """Show available interactive commands"""
    print("\n📖 Available Commands:")
    print("-" * 25)
    print("🔍 Natural Language Queries:")
    print("  • What's new in [tool] this week/month?")
    print("  • [tool] updates")
    print("  • Search for [keywords]")
    print("  • Latest [tool] features")
    print()
    print("🛠️ Special Commands:")
    print("  • digest [days]     - Generate digest (default: 1 day)")
    print("  • security [days]   - Find security updates (default: 90 days)")
    print("  • stats             - Show database statistics")
    print("  • help              - Show this help")
    print("  • quit              - Exit the program")
    print()

def show_interactive_stats(system):
    """Show statistics in interactive mode"""
    stats = system.get_stats()
    
    print("\n📊 Database Statistics:")
    print("-" * 25)
    print(f"Total Articles: {stats['total_articles']}")
    print(f"Recent Articles (7 days): {stats['recent_articles']}")
    
    if stats['date_range']['earliest'] and stats['date_range']['latest']:
        print(f"Date Range: {stats['date_range']['earliest'][:10]} to {stats['date_range']['latest'][:10]}")
    
    print(f"\n📈 Top Tools by Articles:")
    for tool, count in list(stats['by_tool'].items())[:8]:
        print(f"  {tool}: {count}")

def single_query_mode(query, db_path="intelligence.db", limit=20):
    """Single query mode for command line usage"""
    with TopicIntelligence(db_path) as system:
        # Handle special query types
        if query.lower().startswith('digest'):
            parts = query.split()
            days = 1
            if len(parts) > 1 and parts[1].isdigit():
                days = int(parts[1])
            
            digest = system.generate_digest(days)
            format_results([digest], f"Daily digest ({days} days)", "digest")
            return
            
        if query.lower().startswith('security'):
            parts = query.split()
            days = 90
            if len(parts) > 1 and parts[1].isdigit():
                days = int(parts[1])
            
            results = system.find_security_updates(days)
            format_results(results, f"Security updates (last {days} days)", "security")
            return
        
        # Regular query
        results = system.query(query)
        if limit and len(results) > limit:
            results = results[:limit]
        
        # Determine result type for formatting
        if "what's new" in query.lower() or "whats new" in query.lower():
            format_results(results, query, "whats_new")
        else:
            format_results(results, query, "search")

def main():
    parser = argparse.ArgumentParser(description="Query CLI for Topic Intelligence")
    parser.add_argument('query', nargs='*', 
                       help='Natural language query (if not provided, enters interactive mode)')
    parser.add_argument('--db', '-d', default='intelligence.db',
                       help='Path to SQLite database file (default: intelligence.db)')
    parser.add_argument('--limit', '-l', type=int, default=20,
                       help='Maximum number of results to display (default: 20)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Configure logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.INFO)
    
    # Check if database exists
    import os
    if not os.path.exists(args.db):
        print(f"❌ Database not found: {args.db}")
        print(f"Run 'python collect.py --collect-all' to create the database and collect articles.")
        sys.exit(1)
    
    try:
        if args.query:
            # Single query mode
            query = " ".join(args.query)
            single_query_mode(query, args.db, args.limit)
        else:
            # Interactive mode
            interactive_mode(args.db)
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()