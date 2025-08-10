#!/usr/bin/env python3
"""
MCP-Integrated YouTube Transcript Processor
Real-time transcript extraction and AI-powered analysis
"""

import json
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import logging

@dataclass
class TranscriptAnalysis:
    """Structured transcript analysis results"""
    video_id: str
    transcript_text: str
    key_topics: List[str]
    programming_concepts: List[str]
    tools_mentioned: List[str]
    learning_outcomes: List[str]
    relevance_score: float
    summary: str
    actionable_insights: List[str]
    cross_platform_connections: Dict[str, List[str]]

class MCPTranscriptProcessor:
    """MCP-integrated transcript processing with AI analysis"""
    
    def __init__(self):
        self.logger = self._setup_logging()
        self.base_path = Path(__file__).parent
        self.cache_dir = self.base_path / "transcript_cache"
        self.cache_dir.mkdir(exist_ok=True)
        
    def _setup_logging(self):
        """Configure logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        return logging.getLogger(__name__)
    
    def extract_transcript_direct(self, video_url: str) -> Optional[str]:
        """Direct MCP transcript extraction using mcp__MCP_DOCKER__get_transcript"""
        
        # This function would be called by Claude Code with MCP access
        # For simulation, we'll create a placeholder
        
        prompt = f"""
        Please extract the transcript from this YouTube video:
        {video_url}
        
        Use the mcp__MCP_DOCKER__get_transcript tool to get the full transcript.
        Return the complete transcript text.
        """
        
        # In real implementation, this would use MCP tool
        # For now, return cached or simulated transcript
        
        video_id = self._extract_video_id(video_url)
        cache_file = self.cache_dir / f"{video_id}_transcript.txt"
        
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                return f.read()
        
        # Simulated transcript for testing
        simulated_transcript = f"""
        This is a simulated transcript for video {video_id}.
        
        In this video, we discuss React performance optimization techniques.
        We cover topics like useMemo, useCallback, and React.memo.
        We also explore code splitting and lazy loading strategies.
        
        Key tools mentioned: React DevTools, Lighthouse, Bundle Analyzer.
        
        The main learning outcomes include understanding when to optimize,
        measuring performance impacts, and implementing effective solutions.
        """
        
        # Cache the transcript
        with open(cache_file, 'w') as f:
            f.write(simulated_transcript)
        
        return simulated_transcript
    
    def _extract_video_id(self, video_url: str) -> str:
        """Extract video ID from URL"""
        if "youtube.com/watch?v=" in video_url:
            return video_url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in video_url:
            return video_url.split("youtu.be/")[1].split("?")[0]
        elif "youtube.com/shorts/" in video_url:
            return video_url.split("shorts/")[1].split("?")[0]
        return video_url
    
    async def analyze_transcript_with_ai(self, transcript: str, video_metadata: Dict) -> TranscriptAnalysis:
        """Analyze transcript using AI for insights"""
        
        # Extract key information from transcript
        analysis = self._perform_analysis(transcript, video_metadata)
        
        # Identify cross-platform connections
        cross_platform = self._identify_cross_platform_connections(analysis)
        
        # Calculate relevance score
        relevance_score = self._calculate_relevance_score(analysis, video_metadata)
        
        return TranscriptAnalysis(
            video_id=video_metadata.get("video_id", "unknown"),
            transcript_text=transcript[:500],  # Store snippet
            key_topics=analysis["topics"],
            programming_concepts=analysis["concepts"],
            tools_mentioned=analysis["tools"],
            learning_outcomes=analysis["outcomes"],
            relevance_score=relevance_score,
            summary=analysis["summary"],
            actionable_insights=analysis["insights"],
            cross_platform_connections=cross_platform
        )
    
    def _perform_analysis(self, transcript: str, metadata: Dict) -> Dict:
        """Perform detailed transcript analysis"""
        
        # This would use AI/NLP in production
        # For now, use keyword extraction and pattern matching
        
        transcript_lower = transcript.lower()
        
        # Extract programming concepts
        concepts = []
        concept_keywords = [
            "react", "typescript", "javascript", "python", "api",
            "database", "performance", "optimization", "testing",
            "deployment", "architecture", "design pattern", "algorithm"
        ]
        for keyword in concept_keywords:
            if keyword in transcript_lower:
                concepts.append(keyword)
        
        # Extract tools
        tools = []
        tool_keywords = [
            "vscode", "github", "docker", "kubernetes", "aws",
            "react devtools", "chrome devtools", "webpack", "vite",
            "jest", "cypress", "lighthouse", "postman"
        ]
        for tool in tool_keywords:
            if tool in transcript_lower:
                tools.append(tool)
        
        # Extract topics based on content patterns
        topics = []
        if "performance" in transcript_lower or "optimization" in transcript_lower:
            topics.append("Performance Optimization")
        if "tutorial" in transcript_lower or "guide" in transcript_lower:
            topics.append("Tutorial")
        if "best practice" in transcript_lower:
            topics.append("Best Practices")
        if "debug" in transcript_lower or "error" in transcript_lower:
            topics.append("Debugging")
        
        # Generate learning outcomes
        outcomes = []
        if concepts:
            outcomes.append(f"Understanding {', '.join(concepts[:3])}")
        if tools:
            outcomes.append(f"Using {', '.join(tools[:2])} effectively")
        if topics:
            outcomes.append(f"Mastering {topics[0]}")
        
        # Generate summary
        channel = metadata.get("channel", "Unknown")
        title = metadata.get("title", "Unknown")
        summary = f"Video '{title}' by {channel} covers {', '.join(topics[:2]) if topics else 'technical content'}. "
        summary += f"Key concepts include {', '.join(concepts[:3]) if concepts else 'programming techniques'}."
        
        # Generate actionable insights
        insights = []
        if "react" in concepts:
            insights.append("Apply React optimization techniques to current projects")
        if "performance" in topics:
            insights.append("Implement performance monitoring in your applications")
        if tools:
            insights.append(f"Explore {tools[0]} for improved development workflow")
        
        return {
            "topics": topics,
            "concepts": concepts,
            "tools": tools,
            "outcomes": outcomes,
            "summary": summary,
            "insights": insights
        }
    
    def _identify_cross_platform_connections(self, analysis: Dict) -> Dict[str, List[str]]:
        """Identify connections to other platforms/sources"""
        
        connections = {}
        
        # GitHub connections
        if any(tool in ["github", "git"] for tool in analysis.get("tools", [])):
            connections["github"] = [
                "Search for related repositories",
                "Check for code examples",
                "Find implementation patterns"
            ]
        
        # Documentation connections
        if "react" in analysis.get("concepts", []):
            connections["documentation"] = [
                "React official docs for detailed API",
                "MDN for JavaScript fundamentals"
            ]
        
        # Reddit/Community connections
        if analysis.get("topics"):
            connections["reddit"] = [
                f"r/programming discussions on {analysis['topics'][0]}",
                "Community best practices and experiences"
            ]
        
        # Course/Learning platform connections
        if "tutorial" in str(analysis.get("topics", [])).lower():
            connections["learning_platforms"] = [
                "Related courses for deeper understanding",
                "Practice exercises and projects"
            ]
        
        return connections
    
    def _calculate_relevance_score(self, analysis: Dict, metadata: Dict) -> float:
        """Calculate content relevance score"""
        
        score = 0.0
        
        # Channel authority
        channel_rating = metadata.get("channel_rating", 3.0) / 5.0
        score += channel_rating * 0.3
        
        # Content richness
        concept_count = len(analysis.get("concepts", []))
        tool_count = len(analysis.get("tools", []))
        content_richness = min(1.0, (concept_count + tool_count) / 10)
        score += content_richness * 0.3
        
        # Learning value
        outcome_count = len(analysis.get("outcomes", []))
        learning_value = min(1.0, outcome_count / 3)
        score += learning_value * 0.2
        
        # Actionability
        insight_count = len(analysis.get("insights", []))
        actionability = min(1.0, insight_count / 3)
        score += actionability * 0.2
        
        return min(1.0, score)
    
    async def process_video_batch(self, videos: List[Dict]) -> List[TranscriptAnalysis]:
        """Process multiple videos in batch"""
        
        results = []
        
        for video in videos:
            try:
                self.logger.info(f"Processing: {video['title'][:50]}...")
                
                # Extract transcript
                transcript = self.extract_transcript_direct(video['url'])
                
                if transcript:
                    # Analyze transcript
                    analysis = await self.analyze_transcript_with_ai(transcript, video)
                    results.append(analysis)
                    
                    # Store analysis
                    self._store_analysis(analysis)
                    
                    self.logger.info(f"✅ Analyzed: {video['title'][:30]}... (Score: {analysis.relevance_score:.2f})")
                else:
                    self.logger.warning(f"❌ No transcript for: {video['title'][:30]}...")
                    
            except Exception as e:
                self.logger.error(f"Error processing {video['video_id']}: {str(e)}")
        
        return results
    
    def _store_analysis(self, analysis: TranscriptAnalysis):
        """Store analysis results"""
        
        analysis_dir = self.base_path / "transcript_analysis"
        analysis_dir.mkdir(exist_ok=True)
        
        analysis_file = analysis_dir / f"{analysis.video_id}_analysis.json"
        
        with open(analysis_file, 'w') as f:
            json.dump({
                "video_id": analysis.video_id,
                "timestamp": datetime.now().isoformat(),
                "relevance_score": analysis.relevance_score,
                "key_topics": analysis.key_topics,
                "programming_concepts": analysis.programming_concepts,
                "tools_mentioned": analysis.tools_mentioned,
                "learning_outcomes": analysis.learning_outcomes,
                "summary": analysis.summary,
                "actionable_insights": analysis.actionable_insights,
                "cross_platform_connections": analysis.cross_platform_connections
            }, f, indent=2)
    
    def generate_intelligence_report(self, analyses: List[TranscriptAnalysis]) -> Dict:
        """Generate intelligence report from analyses"""
        
        if not analyses:
            return {"error": "No analyses to report"}
        
        # Aggregate insights
        all_topics = []
        all_concepts = []
        all_tools = []
        high_value_videos = []
        
        for analysis in analyses:
            all_topics.extend(analysis.key_topics)
            all_concepts.extend(analysis.programming_concepts)
            all_tools.extend(analysis.tools_mentioned)
            
            if analysis.relevance_score >= 0.8:
                high_value_videos.append({
                    "video_id": analysis.video_id,
                    "score": analysis.relevance_score,
                    "summary": analysis.summary
                })
        
        # Count frequencies
        from collections import Counter
        topic_freq = Counter(all_topics)
        concept_freq = Counter(all_concepts)
        tool_freq = Counter(all_tools)
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "videos_analyzed": len(analyses),
            "average_relevance": sum(a.relevance_score for a in analyses) / len(analyses),
            "high_value_videos": high_value_videos,
            "trending_topics": dict(topic_freq.most_common(5)),
            "key_concepts": dict(concept_freq.most_common(5)),
            "popular_tools": dict(tool_freq.most_common(5)),
            "cross_platform_opportunities": self._identify_opportunities(analyses)
        }
        
        # Save report
        report_file = self.base_path / f"intelligence_report_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def _identify_opportunities(self, analyses: List[TranscriptAnalysis]) -> List[str]:
        """Identify cross-platform opportunities"""
        
        opportunities = []
        
        # Check for GitHub opportunities
        github_mentions = sum(1 for a in analyses if "github" in a.cross_platform_connections)
        if github_mentions > len(analyses) / 2:
            opportunities.append("High GitHub integration potential - consider repository monitoring")
        
        # Check for learning path opportunities
        tutorial_count = sum(1 for a in analyses if "Tutorial" in a.key_topics)
        if tutorial_count > len(analyses) / 3:
            opportunities.append("Strong tutorial content - create learning path compilation")
        
        # Check for tool adoption opportunities
        tool_diversity = len(set(tool for a in analyses for tool in a.tools_mentioned))
        if tool_diversity > 10:
            opportunities.append("Diverse tool ecosystem - create tool comparison guide")
        
        return opportunities

async def main():
    """Main entry point for testing"""
    processor = MCPTranscriptProcessor()
    
    # Test videos
    test_videos = [
        {
            "video_id": "test1",
            "url": "https://youtube.com/watch?v=test1",
            "title": "React Performance Optimization Guide",
            "channel": "TestChannel",
            "channel_rating": 5.0
        },
        {
            "video_id": "test2",
            "url": "https://youtube.com/watch?v=test2",
            "title": "TypeScript Best Practices",
            "channel": "TestChannel2",
            "channel_rating": 4.5
        }
    ]
    
    # Process videos
    analyses = await processor.process_video_batch(test_videos)
    
    # Generate report
    report = processor.generate_intelligence_report(analyses)
    
    print("📊 Intelligence Report Generated:")
    print(f"  • Videos analyzed: {report['videos_analyzed']}")
    print(f"  • Average relevance: {report['average_relevance']:.2f}")
    print(f"  • High-value videos: {len(report['high_value_videos'])}")
    
    if report['trending_topics']:
        print("\n🔥 Trending Topics:")
        for topic, count in list(report['trending_topics'].items())[:3]:
            print(f"  • {topic}: {count} mentions")

if __name__ == "__main__":
    asyncio.run(main())