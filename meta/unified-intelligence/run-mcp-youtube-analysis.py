#!/usr/bin/env python3
"""
Run MCP YouTube Analysis
Practical script for running YouTube content analysis with MCP transcript integration in Claude Code
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

# Add current directory to path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

from mcp_youtube_processor import MCPYouTubeProcessor

def get_video_from_mcp_transcript(video_url: str, transcript: str, title: str = "", channel: str = "") -> Optional[Dict[str, Any]]:
    """Process a video using MCP-provided transcript"""
    processor = MCPYouTubeProcessor()
    
    # Override the transcript method to use provided transcript
    def use_provided_transcript(url: str, lang: str = "en") -> Optional[str]:
        return transcript if url == video_url else None
    
    processor.get_transcript_via_mcp = use_provided_transcript
    
    # Process the video
    result = processor.process_video(video_url, title, channel)
    
    if result:
        # Save to knowledge vault
        processor.save_analysis_result(result)
        
        # Return serializable result
        return {
            'video_id': result.video_id,
            'video_url': result.video_url,
            'title': result.title,
            'channel': result.channel,
            'programming_concepts': result.programming_concepts,
            'priority_topics': result.priority_topics,
            'topic_scores': result.topic_scores,
            'unified_score': result.unified_score,
            'content_summary': result.content_summary,
            'insights': result.insights,
            'processing_timestamp': result.processing_timestamp,
            'transcript_length': len(transcript),
            'analysis_quality': 'high' if result.unified_score > 0.7 else 'medium' if result.unified_score > 0.4 else 'low'
        }
    
    return None

def process_video_with_mcp_call(video_url: str, title: str = "", channel: str = "") -> Optional[Dict[str, Any]]:
    """
    Process video using actual MCP transcript call
    This function is designed to be called from Claude Code with MCP integration
    """
    try:
        # This would be called by Claude Code with actual MCP transcript
        # For standalone usage, we return instructions
        print(f"🎯 To process this video in Claude Code:")
        print(f"   1. Use mcp__MCP_DOCKER__get_transcript with URL: {video_url}")
        print(f"   2. Pass the transcript to get_video_from_mcp_transcript()")
        print(f"   3. The analysis will be automatically saved to knowledge vault")
        
        return {
            'status': 'ready_for_mcp',
            'video_url': video_url,
            'title': title,
            'channel': channel,
            'instructions': 'Call MCP transcript tool and pass result to get_video_from_mcp_transcript()'
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'video_url': video_url
        }

def batch_process_missing_videos() -> List[Dict[str, Any]]:
    """Find and prepare batch processing for videos missing unified analysis"""
    processor = MCPYouTubeProcessor()
    
    # Find videos that need reprocessing
    missing_videos = processor.find_missing_unified_analysis()
    
    if not missing_videos:
        print("✅ All videos already have unified analysis!")
        return []
    
    print(f"🔍 Found {len(missing_videos)} videos needing MCP transcript analysis:")
    
    batch_instructions = []
    
    for i, video_info in enumerate(missing_videos[:10], 1):  # Limit to 10 for practical processing
        print(f"\n📹 Video {i}: {video_info['title']}")
        print(f"   Channel: {video_info['channel']}")
        print(f"   URL: {video_info['video_url']}")
        print(f"   Reason: {video_info['reason']}")
        
        # Prepare batch instruction
        batch_instructions.append({
            'video_url': video_info['video_url'],
            'title': video_info['title'],
            'channel': video_info['channel'],
            'current_file': video_info['file_path'],
            'mcp_instruction': f"get_transcript('{video_info['video_url']}')"
        })
    
    return batch_instructions

def generate_mcp_processing_script(video_urls: List[str], titles: List[str] = None, channels: List[str] = None) -> str:
    """Generate a script for MCP processing in Claude Code"""
    titles = titles or [""] * len(video_urls)
    channels = channels or [""] * len(video_urls)
    
    script_lines = [
        "# MCP YouTube Processing Script",
        "# Run this in Claude Code with MCP integration",
        "",
        "import sys",
        "from pathlib import Path",
        "sys.path.append(str(Path(__file__).parent))",
        "from run_mcp_youtube_analysis import get_video_from_mcp_transcript",
        "",
        "# Process videos with MCP transcripts",
        "results = []",
        ""
    ]
    
    for i, (url, title, channel) in enumerate(zip(video_urls, titles, channels)):
        script_lines.extend([
            f"# Video {i+1}: {title or 'Untitled'}",
            f"transcript_{i+1} = mcp__MCP_DOCKER__get_transcript('{url}')",
            f"if transcript_{i+1}:",
            f"    result_{i+1} = get_video_from_mcp_transcript(",
            f"        '{url}',",
            f"        transcript_{i+1},",
            f"        '{title}',",
            f"        '{channel}'",
            f"    )",
            f"    if result_{i+1}:",
            f"        results.append(result_{i+1})",
            f"        print(f'✅ Processed: {title} (Score: {{result_{i+1}[\"unified_score\"]:.3f}})')",
            f"    else:",
            f"        print(f'❌ Failed to process: {title}')",
            f"else:",
            f"    print(f'❌ No transcript for: {title}')",
            ""
        ])
    
    script_lines.extend([
        "# Summary",
        "print(f'\\n📊 Processed {len(results)} videos')",
        "if results:",
        "    avg_score = sum(r['unified_score'] for r in results) / len(results)",
        "    print(f'📈 Average score: {avg_score:.3f}')",
        "    high_value = [r for r in results if r['unified_score'] > 0.8]",
        "    print(f'🌟 High-value videos: {len(high_value)}')",
        "",
        "# Results are automatically saved to knowledge vault"
    ])
    
    return "\n".join(script_lines)

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="MCP YouTube Content Analysis")
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Process single video
    process_parser = subparsers.add_parser('process', help='Process single video')
    process_parser.add_argument('url', help='YouTube video URL')
    process_parser.add_argument('--title', help='Video title', default="")
    process_parser.add_argument('--channel', help='Channel name', default="")
    
    # Find missing videos
    missing_parser = subparsers.add_parser('find-missing', help='Find videos missing unified analysis')
    
    # Generate processing script
    script_parser = subparsers.add_parser('generate-script', help='Generate MCP processing script')
    script_parser.add_argument('urls', nargs='+', help='Video URLs to process')
    script_parser.add_argument('--output', help='Output script file', default='mcp_processing_script.py')
    
    # Demo mode
    demo_parser = subparsers.add_parser('demo', help='Run demo with sample data')
    
    args = parser.parse_args()
    
    if args.command == 'process':
        print(f"🎯 Processing video: {args.url}")
        result = process_video_with_mcp_call(args.url, args.title, args.channel)
        print(json.dumps(result, indent=2))
        
    elif args.command == 'find-missing':
        print("🔍 Finding videos missing unified analysis...")
        batch_instructions = batch_process_missing_videos()
        
        if batch_instructions:
            print(f"\n📝 To process these videos in Claude Code:")
            print("   1. Copy the URLs below")
            print("   2. Use mcp__MCP_DOCKER__get_transcript for each URL")
            print("   3. Call get_video_from_mcp_transcript() with the results")
            
            print(f"\n🔗 Video URLs for MCP processing:")
            for instruction in batch_instructions:
                print(f"   {instruction['video_url']}")
    
    elif args.command == 'generate-script':
        print(f"📝 Generating MCP processing script for {len(args.urls)} videos...")
        script_content = generate_mcp_processing_script(args.urls)
        
        with open(args.output, 'w') as f:
            f.write(script_content)
        
        print(f"✅ Script saved to: {args.output}")
        print(f"   Run this script in Claude Code with MCP integration")
    
    elif args.command == 'demo':
        print("🚀 Running MCP YouTube Analysis Demo...")
        # Import and run demo
        from mcp_youtube_integration_demo import MCPYouTubeIntegrationDemo
        demo = MCPYouTubeIntegrationDemo()
        demo.run_demo()
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()