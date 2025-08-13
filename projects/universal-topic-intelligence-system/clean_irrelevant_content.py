#!/usr/bin/env python3
"""
Clean irrelevant content from the database
Removes items that don't match our relevance criteria
"""

import sqlite3
import json
from pathlib import Path
from core.relevance_filter import RelevanceFilter

def clean_database():
    """Remove irrelevant content from the database"""
    
    print("🧹 Starting database cleanup...")
    print("=" * 60)
    
    # Initialize relevance filter
    filter = RelevanceFilter()
    
    # Connect to database
    conn = sqlite3.connect("topic_intelligence.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Get all content items
    cursor.execute("SELECT * FROM content_items")
    items = cursor.fetchall()
    
    print(f"📊 Found {len(items)} total items in database")
    
    # Track what we're removing
    removed_items = []
    kept_items = []
    
    for row in items:
        item = dict(row)
        
        # Parse topics if they're JSON
        topics = []
        if item.get('topics'):
            try:
                topics = json.loads(item['topics']) if isinstance(item['topics'], str) else item['topics']
            except:
                topics = []
        
        # Check relevance
        is_relevant, score, reason = filter.is_relevant(
            item['title'],
            item.get('content', ''),
            topics
        )
        
        if not is_relevant:
            removed_items.append({
                'id': item['item_id'],
                'title': item['title'],
                'reason': reason
            })
        else:
            kept_items.append({
                'id': item['item_id'],
                'title': item['title'],
                'score': score
            })
    
    print(f"\n🔍 Relevance Analysis:")
    print(f"  ✅ Keeping: {len(kept_items)} items")
    print(f"  ❌ Removing: {len(removed_items)} items")
    
    if removed_items:
        print("\n📋 Items to be removed:")
        print("-" * 60)
        
        # Group by reason
        reasons = {}
        for item in removed_items:
            reason = item['reason'].split(':')[0]
            if reason not in reasons:
                reasons[reason] = []
            reasons[reason].append(item)
        
        for reason, items_list in reasons.items():
            print(f"\n{reason} ({len(items_list)} items):")
            for item in items_list[:5]:  # Show first 5
                print(f"  - {item['title'][:70]}...")
            if len(items_list) > 5:
                print(f"  ... and {len(items_list) - 5} more")
        
        # Ask for confirmation
        print("\n" + "=" * 60)
        response = input("⚠️  Do you want to remove these items? (yes/no): ")
        
        if response.lower() == 'yes':
            # Remove items from database
            item_ids = [item['id'] for item in removed_items]
            placeholders = ','.join(['?' for _ in item_ids])
            cursor.execute(f"DELETE FROM content_items WHERE item_id IN ({placeholders})", item_ids)
            conn.commit()
            
            print(f"\n✅ Successfully removed {len(removed_items)} irrelevant items")
            
            # Show updated statistics
            cursor.execute("SELECT COUNT(*) FROM content_items")
            new_total = cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT priority_level, COUNT(*) 
                FROM content_items 
                GROUP BY priority_level
            """)
            priority_stats = dict(cursor.fetchall())
            
            print(f"\n📊 Updated Database Statistics:")
            print(f"  Total items: {new_total}")
            print(f"  Priority distribution:")
            for level in ['critical', 'high', 'medium', 'low']:
                count = priority_stats.get(level, 0)
                if count > 0:
                    print(f"    {level.upper()}: {count}")
        else:
            print("\n❌ Cleanup cancelled")
    else:
        print("\n✨ No irrelevant items found - database is clean!")
    
    conn.close()
    print("\n" + "=" * 60)
    print("Cleanup complete")


if __name__ == "__main__":
    clean_database()