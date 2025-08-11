#!/usr/bin/env python3
"""
Database Migration Script
Adds language detection fields and updates existing content
"""

import sqlite3
import logging
from typing import List, Dict, Any
from pathlib import Path
import json
import sys
import os

# Add project root to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from core.language_filter import LanguageFilter


class DatabaseMigrator:
    """Handle database schema migrations and data updates"""
    
    def __init__(self, db_path: str = "topic_intelligence.db"):
        self.db_path = db_path
        self.logger = logging.getLogger("DatabaseMigrator")
        self.language_filter = LanguageFilter()
    
    def add_language_fields(self):
        """Add language detection fields to content_items table"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Check if language fields already exist
            cursor.execute("PRAGMA table_info(content_items)")
            columns = [col[1] for col in cursor.fetchall()]
            
            fields_to_add = []
            if 'detected_language' not in columns:
                fields_to_add.append("ALTER TABLE content_items ADD COLUMN detected_language TEXT DEFAULT 'unknown'")
            if 'language_confidence' not in columns:
                fields_to_add.append("ALTER TABLE content_items ADD COLUMN language_confidence REAL DEFAULT 0.0")
            if 'is_english' not in columns:
                fields_to_add.append("ALTER TABLE content_items ADD COLUMN is_english INTEGER DEFAULT 0")
            
            # Add new fields
            for field_sql in fields_to_add:
                cursor.execute(field_sql)
                self.logger.info(f"Added field: {field_sql}")
            
            conn.commit()
            
            if fields_to_add:
                self.logger.info(f"Successfully added {len(fields_to_add)} language fields to database")
            else:
                self.logger.info("Language fields already exist in database")
            
        except Exception as e:
            self.logger.error(f"Error adding language fields: {str(e)}")
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def update_existing_content_languages(self, batch_size: int = 50):
        """Update language detection for existing content"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Get all content that needs language detection
            cursor.execute("""
                SELECT item_id, title, content, url 
                FROM content_items 
                WHERE detected_language = 'unknown' OR detected_language IS NULL
                ORDER BY collected_date DESC
            """)
            
            items_to_update = cursor.fetchall()
            total_items = len(items_to_update)
            
            if total_items == 0:
                self.logger.info("No content items need language detection")
                return
            
            self.logger.info(f"Updating language detection for {total_items} items")
            
            updated_count = 0
            
            # Process in batches
            for i in range(0, total_items, batch_size):
                batch = items_to_update[i:i + batch_size]
                
                for item_id, title, content, url in batch:
                    try:
                        # Detect language
                        description = content or ""
                        should_include, lang_result = self.language_filter.should_include_content(title, description)
                        
                        # Update database
                        cursor.execute("""
                            UPDATE content_items 
                            SET detected_language = ?, 
                                language_confidence = ?, 
                                is_english = ?
                            WHERE item_id = ?
                        """, (
                            lang_result.language,
                            lang_result.confidence,
                            1 if lang_result.is_english else 0,
                            item_id
                        ))
                        
                        updated_count += 1
                        
                        if updated_count % 10 == 0:
                            self.logger.info(f"Updated {updated_count}/{total_items} items")
                    
                    except Exception as e:
                        self.logger.error(f"Error processing item {item_id}: {str(e)}")
                        continue
                
                # Commit batch
                conn.commit()
            
            self.logger.info(f"Successfully updated language detection for {updated_count} items")
            
        except Exception as e:
            self.logger.error(f"Error updating content languages: {str(e)}")
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def get_language_statistics(self) -> Dict[str, Any]:
        """Get statistics about content languages"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Language distribution
            cursor.execute("""
                SELECT detected_language, COUNT(*) as count, is_english
                FROM content_items 
                WHERE detected_language IS NOT NULL AND detected_language != 'unknown'
                GROUP BY detected_language, is_english
                ORDER BY count DESC
            """)
            
            language_stats = []
            total_items = 0
            english_items = 0
            
            for lang, count, is_eng in cursor.fetchall():
                language_stats.append({
                    'language': lang,
                    'count': count,
                    'is_english': bool(is_eng)
                })
                total_items += count
                if is_eng:
                    english_items += count
            
            # Confidence distribution
            cursor.execute("""
                SELECT 
                    AVG(language_confidence) as avg_confidence,
                    MIN(language_confidence) as min_confidence,
                    MAX(language_confidence) as max_confidence,
                    COUNT(CASE WHEN language_confidence >= 0.7 THEN 1 END) as high_confidence_count
                FROM content_items 
                WHERE language_confidence > 0
            """)
            
            conf_stats = cursor.fetchone()
            
            return {
                'total_items': total_items,
                'english_items': english_items,
                'non_english_items': total_items - english_items,
                'english_percentage': (english_items / total_items * 100) if total_items > 0 else 0,
                'language_distribution': language_stats,
                'confidence_stats': {
                    'average': conf_stats[0] or 0,
                    'minimum': conf_stats[1] or 0,
                    'maximum': conf_stats[2] or 0,
                    'high_confidence_count': conf_stats[3] or 0
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error getting language statistics: {str(e)}")
            return {}
        finally:
            conn.close()
    
    def clean_non_english_content(self, dry_run: bool = True) -> Dict[str, int]:
        """Remove non-English content from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Find non-English content
            cursor.execute("""
                SELECT item_id, title, detected_language, language_confidence
                FROM content_items 
                WHERE is_english = 0 AND detected_language != 'unknown'
                ORDER BY detected_language, language_confidence DESC
            """)
            
            non_english_items = cursor.fetchall()
            
            if dry_run:
                self.logger.info(f"DRY RUN: Would remove {len(non_english_items)} non-English items")
                for item_id, title, lang, conf in non_english_items[:10]:  # Show first 10
                    self.logger.info(f"  - [{lang}] {title[:50]}... (confidence: {conf:.2f})")
                if len(non_english_items) > 10:
                    self.logger.info(f"  ... and {len(non_english_items) - 10} more items")
            else:
                # Actually remove items
                if non_english_items:
                    item_ids = [item[0] for item in non_english_items]
                    placeholders = ','.join(['?'] * len(item_ids))
                    cursor.execute(f"DELETE FROM content_items WHERE item_id IN ({placeholders})", item_ids)
                    conn.commit()
                    self.logger.info(f"Removed {len(non_english_items)} non-English items")
            
            return {
                'total_found': len(non_english_items),
                'removed': 0 if dry_run else len(non_english_items),
                'dry_run': dry_run
            }
            
        except Exception as e:
            self.logger.error(f"Error cleaning non-English content: {str(e)}")
            if not dry_run:
                conn.rollback()
            raise
        finally:
            conn.close()
    
    def run_full_migration(self):
        """Run complete migration process"""
        self.logger.info("Starting database migration for language support")
        
        # Step 1: Add language fields
        self.add_language_fields()
        
        # Step 2: Update existing content
        self.update_existing_content_languages()
        
        # Step 3: Show statistics
        stats = self.get_language_statistics()
        self.logger.info(f"Migration complete. Statistics:")
        self.logger.info(f"  Total items: {stats.get('total_items', 0)}")
        self.logger.info(f"  English items: {stats.get('english_items', 0)} ({stats.get('english_percentage', 0):.1f}%)")
        self.logger.info(f"  Non-English items: {stats.get('non_english_items', 0)}")
        
        # Show language distribution
        lang_dist = stats.get('language_distribution', [])
        self.logger.info("  Language distribution:")
        for lang_info in lang_dist:
            self.logger.info(f"    {lang_info['language']}: {lang_info['count']} items")


def main():
    """Main migration script"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Database Migration for Language Support')
    parser.add_argument('--db', default='topic_intelligence.db', help='Database path')
    parser.add_argument('--add-fields', action='store_true', help='Add language fields only')
    parser.add_argument('--update-content', action='store_true', help='Update existing content only')
    parser.add_argument('--stats', action='store_true', help='Show language statistics only')
    parser.add_argument('--clean', action='store_true', help='Remove non-English content')
    parser.add_argument('--dry-run', action='store_true', help='Dry run mode (show what would be done)')
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    migrator = DatabaseMigrator(args.db)
    
    if args.add_fields:
        migrator.add_language_fields()
    elif args.update_content:
        migrator.update_existing_content_languages()
    elif args.stats:
        stats = migrator.get_language_statistics()
        print(json.dumps(stats, indent=2))
    elif args.clean:
        result = migrator.clean_non_english_content(dry_run=args.dry_run)
        print(f"Clean result: {result}")
    else:
        # Run full migration
        migrator.run_full_migration()


if __name__ == "__main__":
    main()