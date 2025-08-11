#!/usr/bin/env python3
"""
Test language filtering in RSS monitor
"""

import asyncio
import logging
from sources.rss_monitor import RSSSourceMonitor
from core import SourceMetadata, SourceType

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def test_language_filtering():
    """Test RSS monitor with language filtering"""
    
    # Create source metadata for dev.to (which has multi-language content)
    metadata = SourceMetadata(
        source_id="dev_to_test",
        source_name="Dev.to Test",
        source_type=SourceType.RSS,
        source_url="https://dev.to/feed/tag/typescript",  # TypeScript feed from dev.to
        authority_score=0.8,
        update_frequency="daily",
        topics=["typescript"]
    )
    
    # Create RSS monitor with language filtering enabled
    config = {
        "timeout": 15,
        "max_items": 10,
        "enable_language_filtering": True,
        "target_languages": ["en"],
        "min_language_confidence": 0.7
    }
    
    monitor = RSSSourceMonitor(metadata, config)
    
    print("🔍 Testing RSS monitor with language filtering...")
    print(f"📡 Source: {metadata.source_name}")
    print(f"🌐 URL: {metadata.source_url}")
    print(f"🔧 Language filtering: {config['enable_language_filtering']}")
    print(f"📝 Target languages: {config['target_languages']}")
    print()
    
    # Run monitoring
    result = await monitor.monitor()
    
    print(f"✅ Monitoring completed!")
    print(f"📊 Items found: {result.items_found}")
    print(f"🆕 New English items: {len(result.new_items)}")
    print(f"❌ Errors: {len(result.errors)}")
    print()
    
    # Show sample items
    if result.new_items:
        print("📰 Sample filtered items (English only):")
        for i, item in enumerate(result.new_items[:3]):
            print(f"  {i+1}. {item.title[:80]}...")
            lang_info = item.metadata.get('detected_language', 'unknown')
            confidence = item.metadata.get('language_confidence', 0)
            print(f"     Language: {lang_info} (confidence: {confidence:.2f})")
            print()
    
    if result.errors:
        print("⚠️  Errors encountered:")
        for error in result.errors[:3]:
            print(f"  - {error}")
    
    return result

async def main():
    """Main test function"""
    result = await test_language_filtering()
    
    # Summary
    print("=" * 60)
    print("🎯 LANGUAGE FILTERING TEST SUMMARY")
    print("=" * 60)
    print(f"Total items processed: {result.items_found}")
    print(f"English items retained: {len(result.new_items)}")
    
    if result.items_found > 0:
        retention_rate = (len(result.new_items) / result.items_found) * 100
        print(f"Retention rate: {retention_rate:.1f}%")
    
    print(f"Success: {'✅ YES' if result.success else '❌ NO'}")

if __name__ == "__main__":
    asyncio.run(main())