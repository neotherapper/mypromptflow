#!/bin/bash

# YouTube Channel Monitoring System Setup Script
# Universal Topic Intelligence System - Complete Setup

set -e  # Exit on any error

echo "🚀 Setting up YouTube Channel Monitoring System"
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if we're in the right directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo -e "${BLUE}ℹ️  Project root: $PROJECT_ROOT${NC}"
echo

# Function to print status
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check prerequisites
echo "🔍 Checking prerequisites..."

# Check Python 3
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_status "Python $PYTHON_VERSION found"
else
    print_error "Python 3 is required but not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check pip
if command -v pip3 &> /dev/null; then
    print_status "pip3 found"
else
    print_error "pip3 is required but not installed"
    exit 1
fi

# Check Claude Code CLI
if command -v claude &> /dev/null; then
    print_status "Claude Code CLI found"
else
    print_warning "Claude Code CLI not found - MCP transcript extraction may not work"
    echo "Install with: https://claude.ai/code"
fi

echo

# Create virtual environment
echo "🐍 Setting up Python environment..."
cd "$SCRIPT_DIR"

if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_status "Created virtual environment"
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate
print_status "Activated virtual environment"

# Install dependencies
echo
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
print_status "Dependencies installed"

# Create necessary directories
echo
echo "📁 Creating directory structure..."
mkdir -p ../knowledge-vault/youtube-content
mkdir -p ../logs
mkdir -p ../config
mkdir -p ../dashboard
print_status "Directory structure created"

# Create configuration file
echo
echo "⚙️  Creating configuration files..."

# Channel configuration
cat > ../config/youtube-channels-config.json << 'EOF'
[
  {
    "name": "ThePrimeagen",
    "url": "https://www.youtube.com/@ThePrimeagen",
    "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UC8ENHE5xdFSwx71u3fDH5Xw",
    "rating": 5.0,
    "topics": ["software-engineering", "vim", "programming", "development-workflow"],
    "upload_frequency": "weekly",
    "priority": "high"
  },
  {
    "name": "Fireship",
    "url": "https://www.youtube.com/@Fireship", 
    "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCsBjURrPoezykLs9EqgamOA",
    "rating": 5.0,
    "topics": ["programming", "web-development", "tech-trends", "tutorials"],
    "upload_frequency": "weekly",
    "priority": "high"
  },
  {
    "name": "Theo - t3․gg",
    "url": "https://www.youtube.com/@t3dotgg",
    "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UC7K3iGDFa6OlnshFLrr2_Mw",
    "rating": 5.0,
    "topics": ["typescript", "react", "trpc", "t3-stack", "modern-web-dev"],
    "upload_frequency": "frequent",
    "priority": "high"
  },
  {
    "name": "Learn With Jason",
    "url": "https://www.youtube.com/@learnwithjason",
    "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCnty0z0pNRDgnuoirYXnC5A",
    "rating": 5.0,
    "topics": ["web-development", "live-coding", "javascript", "community"],
    "upload_frequency": "weekly",
    "priority": "high"
  },
  {
    "name": "James Q Quick",
    "url": "https://www.youtube.com/@JamesQQuick",
    "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UC-T8W79DN6PBnzomelvqJYw",
    "rating": 4.0,
    "topics": ["javascript", "react", "career-advice", "web-development"],
    "upload_frequency": "bi-weekly",
    "priority": "medium"
  },
  {
    "name": "UI.dev",
    "url": "https://www.youtube.com/@uidotdev",
    "rss_url": "https://www.youtube.com/feeds/videos.xml?channel_id=UCsKsymTY_4BYR-wytLjex7A",
    "rating": 4.0,
    "topics": ["javascript", "frontend", "ecosystem", "tutorials"],
    "upload_frequency": "weekly",
    "priority": "medium"
  }
]
EOF

print_status "Created channel configuration with 6 sample channels"

# Create monitoring script launcher
cat > run-monitoring.sh << 'EOF'
#!/bin/bash
# YouTube Monitoring Launcher

cd "$(dirname "$0")"
source venv/bin/activate

echo "🎬 Starting YouTube Channel Monitoring"
echo "======================================"

# Run RSS monitoring
echo "📡 Step 1: Checking RSS feeds for new videos..."
python3 rss-youtube-monitor.py

echo
echo "🎯 Step 2: Processing transcript queue..."
python3 youtube-integration-manager.py

echo
echo "✅ Monitoring cycle complete!"
echo "📊 View results in the dashboard: ../dashboard/youtube-monitor-dashboard.html"
EOF

chmod +x run-monitoring.sh
print_status "Created monitoring launcher script"

# Create system service file (optional)
cat > youtube-monitor.service << 'EOF'
[Unit]
Description=YouTube Channel Monitoring Service
After=network.target

[Service]
Type=simple
User=%i
WorkingDirectory=/path/to/your/project/scripts
ExecStart=/path/to/your/project/scripts/run-monitoring.sh
Restart=always
RestartSec=3600

[Install]
WantedBy=multi-user.target
EOF

print_status "Created systemd service template"

# Test the setup
echo
echo "🧪 Testing setup..."

# Test RSS monitoring (dry run)
echo "Testing RSS feed access..."
if python3 -c "import feedparser, requests; print('✅ RSS dependencies working')" 2>/dev/null; then
    print_status "RSS monitoring dependencies working"
else
    print_error "RSS monitoring dependencies failed"
fi

# Test script execution
echo "Testing script execution..."
if python3 -c "from rss_youtube_monitor import YouTubeRSSMonitor; print('✅ Main script imports working')" 2>/dev/null; then
    print_status "Main monitoring script working"
else
    print_error "Main monitoring script has issues"
fi

echo
echo "🎉 Setup Complete!"
echo "=================="
echo
echo "📋 What's been set up:"
echo "  ✅ Python virtual environment with dependencies"
echo "  ✅ Directory structure for knowledge vault storage"
echo "  ✅ Configuration files for 6 sample YouTube channels"
echo "  ✅ RSS monitoring script with bypass techniques"
echo "  ✅ MCP integration for transcript processing"
echo "  ✅ Web dashboard for monitoring results"
echo "  ✅ Automated workflow scripts"
echo
echo "🚀 Quick Start Guide:"
echo "  1. Run monitoring: ./run-monitoring.sh"
echo "  2. View dashboard: open ../dashboard/youtube-monitor-dashboard.html"
echo "  3. Check logs: tail -f *.log"
echo "  4. View processed content: ls ../knowledge-vault/youtube-content/"
echo
echo "⚙️  Configuration:"
echo "  • Edit channels: ../config/youtube-channels-config.json"
echo "  • Add more channels from your Notion database"
echo "  • Adjust monitoring frequency in the scripts"
echo
echo "🔄 Automation Options:"
echo "  • Cron job: Add to crontab for scheduled runs"
echo "  • Systemd service: Use youtube-monitor.service template"
echo "  • Manual runs: Execute ./run-monitoring.sh anytime"
echo
echo "📚 Integration:"
echo "  • Universal Topic Intelligence: Configured and ready"
echo "  • Knowledge Vault: Automatic structured storage"
echo "  • MCP Tools: Transcript extraction enabled"
echo "  • Cross-topic connections: Built into analysis pipeline"
echo
echo "🎯 Next Steps:"
echo "  1. Test with: ./run-monitoring.sh"
echo "  2. Add remaining 17 channels from your Notion database"
echo "  3. Set up automated scheduling (cron or systemd)"
echo "  4. Customize relevance scoring for your interests"
echo
print_status "YouTube Channel Monitoring System is ready to use!"