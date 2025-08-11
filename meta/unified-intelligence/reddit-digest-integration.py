#!/usr/bin/env python3
"""
Reddit Digest Integration
Integrates Reddit Dynamic Discovery with the daily digest system
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

try:
    from reddit_dynamic_discovery import RedditDynamicDiscovery
except ImportError:
    print("Error: Could not import reddit_dynamic_discovery module")
    print("Please ensure reddit-dynamic-discovery.py is in the same directory")
    sys.exit(1)

class RedditDigestIntegration:
    """Integration layer between Reddit discovery and digest system"""
    
    def __init__(self, 
                 storage_base: str = None,
                 digest_output: str = None):
        self.logger = self._setup_logging()
        
        # Default paths
        if not storage_base:
            storage_base = "/Users/georgiospilitsoglou/Developer/projects/mypromptflow/knowledge-vault/databases/knowledge_vault/content-intelligence/reddit-intelligence"
        
        if not digest_output:
            digest_output = "/Users/georgiospilitsoglou/Developer/projects/mypromptflow/meta/unified-intelligence/daily-digest/generated/content"
        
        self.storage_base = Path(storage_base)
        self.digest_output = Path(digest_output)
        
        # Ensure directories exist
        self.storage_base.mkdir(parents=True, exist_ok=True)
        self.digest_output.mkdir(parents=True, exist_ok=True)
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for integration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)
    
    def run_discovery_and_integrate(self) -> Dict[str, Any]:
        """Run Reddit discovery and integrate with digest system"""
        try:
            self.logger.info("Starting Reddit discovery and digest integration")
            
            # Initialize and run discovery
            discovery = RedditDynamicDiscovery()
            result = discovery.run_discovery_cycle()
            
            if not result["success"]:
                return {"success": False, "error": f"Discovery failed: {result['error']}"}
            
            # Process results for digest integration
            integration_result = self._process_discovery_results(result)
            
            return {
                "success": True,
                "discovery_result": result,
                "integration_result": integration_result
            }
            
        except Exception as e:
            self.logger.error(f"Integration failed: {e}")
            return {"success": False, "error": str(e)}
    
    def _process_discovery_results(self, discovery_result: Dict[str, Any]) -> Dict[str, Any]:
        """Process discovery results for digest integration"""
        try:
            posts_discovered = discovery_result.get("posts_discovered", 0)
            batch_directory = discovery_result.get("batch_directory")
            
            if not batch_directory or posts_discovered == 0:
                self.logger.info("No posts to process for digest integration")
                return {"posts_processed": 0}
            
            batch_dir = Path(batch_directory)
            
            # Load digest-ready posts
            digest_file = batch_dir / "digest_ready.json"
            if not digest_file.exists():
                self.logger.warning("No digest-ready posts found")
                return {"posts_processed": 0}
            
            with open(digest_file, 'r') as f:
                digest_data = json.load(f)
            
            # Create digest-compatible output
            digest_output = self._create_digest_output(digest_data)
            
            # Save to digest system location
            timestamp = datetime.now().strftime("%Y-%m-%d")
            output_file = self.digest_output / f"reddit-intelligence-{timestamp}.json"
            
            with open(output_file, 'w') as f:
                json.dump(digest_output, f, indent=2)
            
            self.logger.info(f"Digest integration completed: {len(digest_data['posts'])} posts processed")
            
            return {
                "posts_processed": len(digest_data['posts']),
                "output_file": str(output_file),
                "digest_data": digest_output
            }
            
        except Exception as e:
            self.logger.error(f"Error processing discovery results: {e}")
            return {"error": str(e)}
    
    def _create_digest_output(self, reddit_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create digest-compatible output from Reddit discovery data"""
        posts = reddit_data.get("posts", [])
        
        # Group posts by priority topic
        posts_by_topic = {}
        high_priority_posts = []
        
        for post in posts:
            priority_topics = post.get("priority_topics", [])
            combined_score = post.get("topic_score", 0) + post.get("quality_score", 0)
            
            # High priority posts (score >= 2.5)
            if combined_score >= 2.5:
                high_priority_posts.append(post)
            
            # Group by topic
            for topic in priority_topics:
                if topic not in posts_by_topic:
                    posts_by_topic[topic] = []
                posts_by_topic[topic].append(post)
        
        # Create summary statistics
        total_posts = len(posts)
        avg_score = sum(p.get("score", 0) for p in posts) / max(total_posts, 1)
        avg_comments = sum(p.get("comments", 0) for p in posts) / max(total_posts, 1)
        
        # Top subreddits
        subreddit_counts = {}
        for post in posts:
            subreddit = post.get("subreddit", "unknown")
            subreddit_counts[subreddit] = subreddit_counts.get(subreddit, 0) + 1
        
        top_subreddits = sorted(subreddit_counts.items(), 
                               key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "source": "reddit-dynamic-discovery",
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_posts": total_posts,
                "high_priority_posts": len(high_priority_posts),
                "average_score": round(avg_score, 1),
                "average_comments": round(avg_comments, 1),
                "topics_covered": list(posts_by_topic.keys()),
                "top_subreddits": top_subreddits
            },
            "high_priority_posts": high_priority_posts[:10],  # Top 10
            "posts_by_topic": {
                topic: posts[:5]  # Top 5 per topic
                for topic, posts in posts_by_topic.items()
            },
            "all_posts": posts,
            "metadata": {
                "discovery_timestamp": reddit_data.get("discovery_timestamp"),
                "total_discovered": reddit_data.get("high_quality_posts", 0),
                "processing_timestamp": datetime.now().isoformat()
            }
        }
    
    def get_latest_reddit_intelligence(self, days_back: int = 3) -> Dict[str, Any]:
        """Get latest Reddit intelligence for digest generation"""
        try:
            # Look for recent digest files
            cutoff_date = datetime.now() - timedelta(days=days_back)
            
            recent_files = []
            for file_path in self.digest_output.glob("reddit-intelligence-*.json"):
                try:
                    # Extract date from filename
                    date_str = file_path.stem.split('-')[-3:]  # last 3 parts: YYYY-MM-DD
                    if len(date_str) == 3:
                        file_date = datetime.strptime('-'.join(date_str), "%Y-%m-%d")
                        if file_date >= cutoff_date:
                            recent_files.append((file_date, file_path))
                except:
                    continue
            
            if not recent_files:
                return {"posts": [], "summary": {"total_posts": 0}}
            
            # Get most recent file
            recent_files.sort(key=lambda x: x[0], reverse=True)
            latest_file = recent_files[0][1]
            
            with open(latest_file, 'r') as f:
                return json.load(f)
            
        except Exception as e:
            self.logger.error(f"Error getting latest Reddit intelligence: {e}")
            return {"posts": [], "summary": {"total_posts": 0}}
    
    def create_reddit_summary_for_digest(self, data: Dict[str, Any] = None) -> str:
        """Create a summary of Reddit discoveries for the daily digest"""
        if not data:
            data = self.get_latest_reddit_intelligence()
        
        summary = data.get("summary", {})
        high_priority = data.get("high_priority_posts", [])
        posts_by_topic = data.get("posts_by_topic", {})
        
        if summary.get("total_posts", 0) == 0:
            return "No Reddit intelligence discovered in recent monitoring cycles."
        
        lines = [
            "## 🔍 Reddit Intelligence",
            f"**{summary.get('total_posts', 0)} posts discovered** across priority topics",
            f"Average engagement: {summary.get('average_score', 0)} upvotes, {summary.get('average_comments', 0)} comments",
            ""
        ]
        
        # High priority discoveries
        if high_priority:
            lines.extend([
                "### 🎯 High Priority Discoveries",
                ""
            ])
            
            for post in high_priority[:5]:  # Top 5
                topics = ", ".join(post.get("priority_topics", []))
                combined_score = post.get("topic_score", 0) + post.get("quality_score", 0)
                lines.extend([
                    f"**[{post.get('title', 'Untitled')}]({post.get('url', '#')})**",
                    f"*r/{post.get('subreddit', 'unknown')} • {post.get('score', 0)} pts • {post.get('comments', 0)} comments*",
                    f"Topics: {topics} • Score: {combined_score:.1f}",
                    ""
                ])
        
        # Topic breakdown
        if posts_by_topic:
            lines.extend([
                "### 📊 By Priority Topic",
                ""
            ])
            
            for topic, posts in posts_by_topic.items():
                if posts:
                    lines.append(f"**{topic.title()}** ({len(posts)} posts)")
                    for post in posts[:2]:  # Top 2 per topic
                        lines.append(f"• [{post.get('title', 'Untitled')}]({post.get('url', '#')}) ({post.get('score', 0)} pts)")
                    lines.append("")
        
        # Top subreddits
        top_subreddits = summary.get("top_subreddits", [])
        if top_subreddits:
            lines.extend([
                "### 🏆 Most Active Subreddits",
                ""
            ])
            for subreddit, count in top_subreddits[:3]:
                lines.append(f"• r/{subreddit}: {count} posts")
            lines.append("")
        
        return "\n".join(lines)

def main():
    """Main execution function"""
    integration = RedditDigestIntegration()
    
    print("Reddit Digest Integration")
    print("=" * 40)
    
    # Run discovery and integration
    result = integration.run_discovery_and_integrate()
    
    if result["success"]:
        discovery = result["discovery_result"]
        integration_data = result["integration_result"]
        
        print("✅ Integration completed successfully")
        print(f"📊 Posts discovered: {discovery.get('posts_discovered', 0)}")
        print(f"📝 Posts processed for digest: {integration_data.get('posts_processed', 0)}")
        
        if integration_data.get("output_file"):
            print(f"💾 Digest file: {integration_data['output_file']}")
        
        # Generate sample digest summary
        if integration_data.get("digest_data"):
            print("\n📋 Sample digest summary:")
            summary = integration.create_reddit_summary_for_digest(integration_data["digest_data"])
            print(summary[:500] + "..." if len(summary) > 500 else summary)
    else:
        print(f"❌ Integration failed: {result['error']}")

if __name__ == "__main__":
    main()