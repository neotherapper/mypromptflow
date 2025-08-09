#!/usr/bin/env python3
"""
Quick test version of YouTube Dynamic Search with faster rate limiting
"""

import sys
import json
from pathlib import Path

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

# Import after adding to path
try:
    from youtube_dynamic_search import YouTubeDynamicSearcher
except ImportError:
    # If import fails, run the module directly
    import subprocess
    print("Import failed, running module directly...")
    sys.exit(1)

def create_fast_config():
    """Create a fast configuration for testing"""
    config_data = {
        "search_terms": {
            "claude": ["Claude AI tutorial", "Claude Code IDE"],  # Reduced to 2 terms
            "react": ["React TypeScript tutorial", "React 2024 development"]  # Reduced to 2 terms
        },
        "filters": {
            "published_after_days": 30,
            "min_view_count": 50,  # Lower threshold
            "min_duration_seconds": 60,  # Lower threshold
            "max_duration_seconds": 3600,
            "exclude_shorts": True,
            "language": "en"
        },
        "thresholds": {
            "min_relevance_score": 0.4,  # Lower threshold
            "min_engagement_score": 0.3,  # Lower threshold
            "min_unified_score": 0.3,     # Lower threshold
            "max_results_per_term": 5,    # Fewer results
            "max_total_results": 20       # Fewer total results
        },
        "rate_limiting": {
            "requests_per_minute": 60,    # Faster
            "delay_between_requests": 0.5,  # Much faster
            "backoff_multiplier": 1.2,
            "max_retries": 3
        },
        "output_settings": {
            "include_transcript_preview": False,
            "include_thumbnail": True,
            "save_individual_files": True,
            "generate_summary": True
        }
    }
    
    # Save test config
    config_file = Path(__file__).parent / "youtube-search-test-config.json"
    with open(config_file, 'w') as f:
        json.dump(config_data, f, indent=2)
    
    return str(config_file)

def main():
    """Test the YouTube dynamic search with fast config"""
    print("🚀 Testing YouTube Dynamic Search (Fast Config)")
    print("=" * 50)
    
    # Create fast config
    config_path = create_fast_config()
    print(f"📝 Created test config: {config_path}")
    
    # Run searcher with test config
    searcher = YouTubeDynamicSearcher(config_path)
    results = searcher.run_dynamic_search()
    
    print("\n✅ Test completed successfully!")
    print(f"📊 Found {results['search_metadata']['total_videos_found']} videos")
    print(f"⭐ Selected {results['search_metadata']['quality_videos_selected']} quality videos")
    
    # Show sample results
    if results['top_videos']:
        print(f"\n🏆 Sample Results:")
        for i, video in enumerate(results['top_videos'][:3], 1):
            print(f"{i}. {video['title']}")
            print(f"   Channel: {video['channel_name']}")
            print(f"   Score: {video['unified_score']:.3f}")
            print(f"   Topic: {video['priority_topic']}")
            print()

if __name__ == "__main__":
    main()