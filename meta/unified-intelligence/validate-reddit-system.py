#!/usr/bin/env python3
"""
Reddit Dynamic Discovery System Validation
Validates the system setup and configuration
"""

import json
import sys
from pathlib import Path
from datetime import datetime

def validate_system():
    """Validate Reddit Dynamic Discovery System setup"""
    print("🔍 Validating Reddit Dynamic Discovery System")
    print("=" * 50)
    
    validation_results = {
        "config_files": False,
        "storage_directories": False,
        "priority_topics": False,
        "import_capability": False,
        "rate_limiting": False
    }
    
    # 1. Check configuration files
    try:
        config_file = Path("reddit-dynamic-discovery-config.json")
        if config_file.exists():
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            required_keys = ["priority_subreddits", "search_queries", "quality_thresholds", "storage_path"]
            if all(key in config for key in required_keys):
                print("✅ Configuration file valid")
                print(f"   • {len(config['priority_subreddits'])} priority subreddits configured")
                print(f"   • {len(config['search_queries'])} search queries defined")
                validation_results["config_files"] = True
            else:
                print("❌ Configuration file missing required keys")
        else:
            print("❌ Configuration file not found")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
    
    # 2. Check storage directories
    try:
        if config_file.exists():
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            storage_path = Path(config["storage_path"])
            storage_path.mkdir(parents=True, exist_ok=True)
            
            # Test write permissions
            test_file = storage_path / "test_write.json"
            with open(test_file, 'w') as f:
                json.dump({"test": True}, f)
            test_file.unlink()  # Clean up
            
            print("✅ Storage directories accessible")
            print(f"   • Storage path: {storage_path}")
            validation_results["storage_directories"] = True
        else:
            print("❌ Cannot validate storage - config missing")
    except Exception as e:
        print(f"❌ Storage directory error: {e}")
    
    # 3. Check priority topics
    try:
        topics_file = Path("priority-topics.json")
        if topics_file.exists():
            with open(topics_file, 'r') as f:
                topics = json.load(f)
            
            priority_topics = topics.get("priority_topics", {})
            if priority_topics:
                print("✅ Priority topics configured")
                print(f"   • {len(priority_topics)} priority topics loaded")
                for topic, config in list(priority_topics.items())[:3]:
                    weight = config.get("weight", 0)
                    keywords = len(config.get("keywords", []))
                    print(f"   • {topic}: weight {weight}, {keywords} keywords")
                validation_results["priority_topics"] = True
            else:
                print("❌ No priority topics found in configuration")
        else:
            print("⚠️  Priority topics file not found (will use defaults)")
            validation_results["priority_topics"] = True  # Optional file
    except Exception as e:
        print(f"❌ Priority topics error: {e}")
    
    # 4. Check import capability
    try:
        sys.path.insert(0, str(Path.cwd()))
        
        # Test basic imports
        import requests
        import feedparser
        print("✅ Required packages available")
        print("   • requests: ✓")
        print("   • feedparser: ✓")
        
        # Test optional PRAW
        try:
            import praw
            print("   • praw: ✓ (Reddit API capable)")
        except ImportError:
            print("   • praw: ❌ (RSS-only mode)")
        
        validation_results["import_capability"] = True
    except ImportError as e:
        print(f"❌ Missing required packages: {e}")
        print("   Run: pip install requests feedparser praw")
    except Exception as e:
        print(f"❌ Import test error: {e}")
    
    # 5. Check rate limiting configuration
    try:
        if config_file.exists():
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            rate_limits = config.get("rate_limits", {})
            if rate_limits and "requests_per_minute" in rate_limits:
                rpm = rate_limits["requests_per_minute"]
                print("✅ Rate limiting configured")
                print(f"   • {rpm} requests per minute limit")
                if rpm <= 60:  # Conservative Reddit API usage
                    print("   • Conservative rate limiting ✓")
                    validation_results["rate_limiting"] = True
                else:
                    print("   • ⚠️  Rate limit may be too aggressive")
                    validation_results["rate_limiting"] = True
            else:
                print("❌ Rate limiting not configured")
    except Exception as e:
        print(f"❌ Rate limiting check error: {e}")
    
    # Summary
    print("\n📊 Validation Summary")
    print("-" * 30)
    
    passed = sum(validation_results.values())
    total = len(validation_results)
    
    for check, result in validation_results.items():
        status = "✅" if result else "❌"
        print(f"{status} {check.replace('_', ' ').title()}")
    
    print(f"\n🎯 Overall: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 System validation successful!")
        print("Ready to run reddit-dynamic-discovery.py")
        return True
    else:
        print(f"\n⚠️  {total - passed} issues found. Please resolve before running the system.")
        return False

def show_quick_start():
    """Show quick start instructions"""
    print("\n🚀 Quick Start Guide")
    print("-" * 20)
    print("1. Install dependencies (if missing):")
    print("   pip install requests feedparser praw")
    print("")
    print("2. Run the discovery system:")
    print("   python reddit-dynamic-discovery.py")
    print("")
    print("3. For Reddit API access (optional):")
    print("   • Create app at https://www.reddit.com/prefs/apps")
    print("   • Copy .env.template to .env")
    print("   • Add REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET")
    print("")
    print("4. Monitor results:")
    print("   • Logs: reddit-dynamic-discovery.log")
    print("   • Storage: knowledge-vault/.../reddit-intelligence/")
    print("")
    print("5. Integration with digest:")
    print("   python reddit-digest-integration.py")

def main():
    """Main validation function"""
    success = validate_system()
    show_quick_start()
    
    if success:
        print("\n✨ The Reddit Dynamic Discovery System is ready to discover")
        print("   high-quality discussions about your priority topics!")
        return 0
    else:
        print("\n🔧 Please resolve validation issues before proceeding.")
        return 1

if __name__ == "__main__":
    sys.exit(main())