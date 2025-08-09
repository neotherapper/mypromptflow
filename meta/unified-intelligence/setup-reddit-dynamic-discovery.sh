#!/bin/bash
"""
Reddit Dynamic Discovery System Setup Script
Installs dependencies and configures the system for priority topic monitoring
"""

set -e

echo "🔧 Setting up Reddit Dynamic Discovery System..."

# Check if we're in the right directory
if [ ! -f "reddit-dynamic-discovery.py" ]; then
    echo "❌ Error: reddit-dynamic-discovery.py not found in current directory"
    echo "Please run this script from the meta/unified-intelligence directory"
    exit 1
fi

# Create Python virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install required packages
echo "📚 Installing required packages..."
pip install requests feedparser praw python-dateutil

# Create requirements.txt for future reference
echo "📝 Creating requirements.txt..."
cat > requirements.txt << EOF
requests>=2.31.0
feedparser>=6.0.10
praw>=7.7.1
python-dateutil>=2.8.2
EOF

# Create storage directories
echo "📁 Creating storage directories..."
STORAGE_BASE="/Users/georgiospilitsoglou/Developer/projects/mypromptflow/knowledge-vault/databases/knowledge_vault/content-intelligence/reddit-intelligence"
mkdir -p "$STORAGE_BASE/dynamic-discovery"
mkdir -p "$STORAGE_BASE/by-topic"
mkdir -p "$STORAGE_BASE/summaries"
mkdir -p "$STORAGE_BASE/daily"

# Create .env template for Reddit API credentials
echo "🔐 Creating .env template..."
cat > .env.template << EOF
# Reddit API Credentials (Optional - for enhanced search capabilities)
# Get these from https://www.reddit.com/prefs/apps
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here

# Rate Limiting Configuration
REDDIT_REQUESTS_PER_MINUTE=30
REDDIT_BURST_LIMIT=10
EOF

# Create environment loading script
echo "🌍 Creating environment setup script..."
cat > load_env.py << 'EOF'
#!/usr/bin/env python3
"""Load environment variables from .env file if it exists"""
import os
from pathlib import Path

def load_env():
    env_file = Path('.env')
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key] = value

if __name__ == "__main__":
    load_env()
    print("Environment variables loaded from .env file")
EOF

# Create test script
echo "🧪 Creating test script..."
cat > test_reddit_discovery.py << 'EOF'
#!/usr/bin/env python3
"""Test script for Reddit Dynamic Discovery System"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from reddit_dynamic_discovery import RedditDynamicDiscovery
    print("✅ Successfully imported RedditDynamicDiscovery")
    
    # Test configuration loading
    discovery = RedditDynamicDiscovery()
    print(f"✅ Configuration loaded with {len(discovery.config.priority_subreddits)} priority subreddits")
    print(f"✅ Search queries configured: {len(discovery.config.search_queries)}")
    print(f"✅ Storage path: {discovery.storage_path}")
    
    # Test priority topics loading
    if discovery.priority_topics:
        priority_count = len(discovery.priority_topics.get("priority_topics", {}))
        print(f"✅ Priority topics loaded: {priority_count}")
    else:
        print("⚠️  Priority topics not found - will use default scoring")
    
    # Test Reddit client (will warn if no credentials)
    if discovery.reddit_client:
        print("✅ Reddit API client configured")
    else:
        print("⚠️  Reddit API not configured - RSS-only mode")
    
    print("\n🎉 Reddit Dynamic Discovery System is ready!")
    print("\nTo run the system:")
    print("  python reddit-dynamic-discovery.py")
    print("\nTo set up Reddit API (optional):")
    print("  1. Copy .env.template to .env")
    print("  2. Add your Reddit API credentials")
    print("  3. Restart the system")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Please install required packages: pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Configuration error: {e}")
    sys.exit(1)
EOF

# Make scripts executable
chmod +x setup-reddit-dynamic-discovery.sh
chmod +x load_env.py
chmod +x test_reddit_discovery.py

# Run the test
echo "🧪 Testing configuration..."
python test_reddit_discovery.py

echo ""
echo "✅ Reddit Dynamic Discovery System setup complete!"
echo ""
echo "📋 Setup Summary:"
echo "  • Python virtual environment created"
echo "  • Required packages installed"
echo "  • Storage directories created"
echo "  • Configuration files ready"
echo "  • Environment template created"
echo ""
echo "🚀 Next Steps:"
echo "  1. (Optional) Set up Reddit API credentials:"
echo "     • Copy .env.template to .env"
echo "     • Get credentials from https://www.reddit.com/prefs/apps"
echo "     • Add REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET to .env"
echo ""
echo "  2. Run the discovery system:"
echo "     • source venv/bin/activate"
echo "     • python reddit-dynamic-discovery.py"
echo ""
echo "  3. Monitor results in:"
echo "     • Logs: reddit-dynamic-discovery.log"
echo "     • Storage: knowledge-vault/databases/knowledge_vault/content-intelligence/reddit-intelligence/"
echo ""
echo "🔍 The system will monitor these priority topics:"
echo "  • Claude AI and Anthropic developments"
echo "  • React framework and ecosystem"
echo "  • TypeScript language and tooling"
echo "  • Meta-prompting and prompt engineering"
echo "  • Next.js and full-stack React"
echo ""
echo "💡 System features:"
echo "  • RSS monitoring of priority subreddits"
echo "  • Cross-subreddit search for priority topics"
echo "  • Quality scoring and filtering"
echo "  • Priority topic detection and scoring"
echo "  • JSON output compatible with digest generator"
echo "  • Rate limiting and Reddit API guidelines compliance"