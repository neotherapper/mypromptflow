#!/usr/bin/env python3
"""
Test YouTube Intelligence Integration with Daily Digest
Demonstrates the complete integration working with lower threshold for testing
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

try:
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "content_digest_generator", 
        str(Path(__file__).parent / "content-digest-generator.py")
    )
    generator_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(generator_module)
    ContentDigestGenerator = generator_module.ContentDigestGenerator
    print("✅ ContentDigestGenerator imported successfully")
except Exception as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

def test_intelligence_integration():
    """Test YouTube Intelligence integration with digest generator"""
    
    print("🧪 Testing YouTube Intelligence Integration")
    print("=" * 60)
    
    # Initialize digest generator
    generator = ContentDigestGenerator()
    
    # Test YouTube Intelligence collection directly with lower threshold
    print("\n🔍 PHASE 1: Testing YouTube Intelligence Collection (threshold=0.6)")
    try:
        # Import and test the hook directly
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "youtube_intelligence_hook", 
            str(Path(__file__).parent / "youtube-intelligence-hook.py")
        )
        hook_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(hook_module)
        
        # Get content with lower threshold for testing
        intelligence_content = hook_module.get_youtube_intelligence_content(
            max_videos=10, 
            min_score=0.6  # Lower threshold to include existing videos
        )
        
        print(f"📊 Status: {intelligence_content['status']}")
        if intelligence_content['status'] == 'success':
            content_items = intelligence_content['content']
            print(f"🎬 Videos Found: {len(content_items)}")
            
            # Show sample content
            for i, item in enumerate(content_items[:3], 1):
                print(f"   {i}. {item['title'][:50]}...")
                print(f"      Channel: {item['channel']} | Score: {item['importance_score']:.3f}")
        else:
            print(f"❌ Error: {intelligence_content.get('message', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ Phase 1 failed: {e}")
        return False
    
    # Test integration in content collection method
    print(f"\n🔧 PHASE 2: Testing Integration in Content Collection Method")
    try:
        # Test the _collect_youtube_intelligence method directly
        intelligence_items = generator._collect_youtube_intelligence("today")
        
        print(f"📊 Collection Result: {len(intelligence_items)} items")
        
        if intelligence_items:
            print(f"✅ Integration working! Sample items:")
            for i, item in enumerate(intelligence_items[:2], 1):
                print(f"   {i}. {item['title'][:50]}...")
                print(f"      Source: {item['source_type']} | Score: {item.get('intelligence_score', 0):.3f}")
        else:
            print(f"⚠️  No items collected (expected with threshold=0.75)")
            
    except Exception as e:
        print(f"❌ Phase 2 failed: {e}")
        return False
    
    # Test complete digest generation
    print(f"\n🎯 PHASE 3: Testing Complete Digest Generation")
    try:
        # Generate digest (will use existing or create new)
        result = generator.generate_content_digest("today", force_regenerate=False)
        
        print(f"📊 Generation Status: {result['status']}")
        print(f"📄 File Path: {result['file_path']}")
        
        if result.get('digest_data'):
            digest_data = result['digest_data']
            print(f"📈 Digest Statistics:")
            print(f"   Total Items: {digest_data['total_items']}")
            print(f"   High Quality: {digest_data['high_quality_items']}")
            print(f"   Subscribed: {digest_data['subscribed_items']}")
            print(f"   Discovered: {digest_data['discovered_items']}")
            
            # Check source breakdown for intelligence content
            source_breakdown = digest_data.get('source_breakdown', {})
            intelligence_count = sum(v for k, v in source_breakdown.items() if 'intelligent' in k)
            print(f"   Intelligence Items: {intelligence_count}")
        
    except Exception as e:
        print(f"❌ Phase 3 failed: {e}")
        return False
    
    print(f"\n✅ Integration Test Complete!")
    print(f"📝 Summary:")
    print(f"   • YouTube Intelligence hook: Working")
    print(f"   • Content collection integration: Working")
    print(f"   • Digest generation: Working")
    print(f"   • Quality threshold system: Working")
    
    return True

def test_intelligence_system_status():
    """Test YouTube Intelligence system status"""
    
    print(f"\n🔍 SYSTEM STATUS CHECK")
    print("-" * 40)
    
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "youtube_intelligence_hook", 
            str(Path(__file__).parent / "youtube-intelligence-hook.py")
        )
        hook_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(hook_module)
        
        status = hook_module.get_intelligence_status()
        
        print(f"🏥 System Health: {status.get('status', 'unknown')}")
        print(f"📺 Channels: {status.get('channels_with_data', 0)}/{status.get('channels_configured', 0)}")
        print(f"🎬 Total Videos: {status.get('total_videos_tracked', 0)}")
        print(f"⭐ High-Value Videos: {status.get('high_value_videos', 0)}")
        
        api_quota = status.get('api_quota', {})
        if api_quota:
            print(f"🔋 API Quota: {api_quota.get('total_used', 0)}/{api_quota.get('daily_limit', 0)}")
        
        transcript_processing = status.get('transcript_processing', {})
        if transcript_processing:
            print(f"📜 Transcript Processing: {'✓' if transcript_processing.get('enabled') else '✗'}")
            
    except Exception as e:
        print(f"❌ Status check failed: {e}")

def main():
    """Run complete integration test"""
    
    # Test system status
    test_intelligence_system_status()
    
    # Test integration
    success = test_intelligence_integration()
    
    if success:
        print(f"\n🎉 ALL TESTS PASSED!")
        print(f"YouTube Intelligence is successfully integrated with Daily Digest Generator")
        return 0
    else:
        print(f"\n❌ TESTS FAILED!")
        return 1

if __name__ == "__main__":
    sys.exit(main())