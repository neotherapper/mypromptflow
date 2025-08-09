#!/usr/bin/env python3
"""
Test script for performance and UX improvements
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from content_digest_generator import ContentDigestGenerator

def test_performance():
    """Test optimized content digest generator"""
    
    print("🧪 Testing Performance Optimized Content Digest Generator")
    print("=" * 60)
    
    generator = ContentDigestGenerator()
    
    # Force regeneration to test performance
    result = generator.generate_content_digest("today", force_regenerate=True)
    
    if result['status'] == 'generated':
        generation_time = result.get('generation_time', 0)
        print(f"\n✅ Performance Test Complete!")
        print(f"   📊 Generation Time: {generation_time:.2f}s")
        
        if generation_time < 15:
            print(f"   🚀 Performance: EXCELLENT (target: <15s)")
        elif generation_time < 30:
            print(f"   ⚠️ Performance: ACCEPTABLE (target: <15s)")
        else:
            print(f"   ❌ Performance: NEEDS IMPROVEMENT (target: <15s)")
            
        print(f"   📄 Output: {result['file_path']}")
    else:
        print(f"❌ Test failed: {result}")

if __name__ == "__main__":
    test_performance()