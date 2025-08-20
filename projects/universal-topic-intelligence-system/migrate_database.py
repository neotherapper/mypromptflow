#!/usr/bin/env python3
"""
Database Migration Script
Migrates existing database to support MCP-specific fields
"""

import logging
from storage.database import StorageManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("DatabaseMigration")

def main():
    """Run database migration"""
    print("🔧 Running Database Migration for MCP Support...")
    print("=" * 50)
    
    # Initialize storage manager (will use existing database)
    storage = StorageManager("topic_intelligence.db")
    
    # Run migration
    print("📊 Migrating database schema...")
    success = storage.migrate_database_schema()
    
    if success:
        print("✅ Database migration completed successfully!")
        
        # Get statistics to verify migration
        stats = storage.get_statistics()
        print(f"\n📈 Database Statistics:")
        print(f"  Total items: {stats.get('total_items', 0)}")
        print(f"  Topics monitored: {stats.get('topics_monitored', 0)}")
        print(f"  Items last 24h: {stats.get('items_last_24h', 0)}")
        
        # Test MCP analytics (should work now)
        try:
            mcp_analytics = storage.get_mcp_analytics()
            print(f"\n🔍 MCP Analytics (Post-Migration):")
            if mcp_analytics.get('content_by_mcp_type'):
                print(f"  MCP content types: {len(mcp_analytics['content_by_mcp_type'])}")
            else:
                print("  No MCP content found (expected for existing data)")
        except Exception as e:
            print(f"  Analytics test: {e}")
        
        print("\n🎉 Migration complete! Monitor system ready to use enhanced database.")
        
    else:
        print("❌ Database migration failed!")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())