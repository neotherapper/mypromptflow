#!/bin/bash

echo "🚀 Setting up AI Knowledge Base..."

# Run initialization scripts
bash scripts/init/create_directories.sh
bash scripts/init/create_claude_files.sh
bash scripts/init/create_ai_files.sh

echo "✅ Setup complete! See README.md for next steps."