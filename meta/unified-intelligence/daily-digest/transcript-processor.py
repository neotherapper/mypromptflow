#!/usr/bin/env python3
"""
Intelligent Transcript Processor for YouTube Intelligence System
Selective transcript extraction based on importance scoring with MCP integration
"""

import json
import os
import sys
import time
import logging
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
import hashlib
import importlib.util

# Add parent directory for imports
parent_dir = Path(__file__).parent.parent
sys.path.append(str(parent_dir))

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class TranscriptTask:
    """Transcript extraction task"""
    video_id: str
    title: str
    channel_name: str
    importance_score: float
    priority_topics: List[str]
    priority: str  # "high", "medium", "low"
    queued_at: str
    attempts: int = 0
    max_attempts: int = 3
    status: str = "pending"  # "pending", "processing", "completed", "failed"
    error: Optional[str] = None
    processed_at: Optional[str] = None
    transcript_length: Optional[int] = None
    analysis_summary: Optional[str] = None

@dataclass
class TranscriptAnalysis:
    """Results of transcript content analysis"""
    video_id: str
    transcript_length: int
    key_concepts: List[str]
    priority_topic_matches: List[str]
    technical_depth_score: float
    educational_value_score: float
    actionable_insights_count: int
    summary: str
    full_analysis: str
    processing_time: float

class MCPTranscriptExtractor:
    """MCP-based transcript extraction system"""
    
    def __init__(self):
        self.available = False
        self.extract_transcript = None
        
        # Try to set up MCP transcript extraction
        self._setup_mcp_extraction()
    
    def _setup_mcp_extraction(self):
        """Set up MCP transcript extraction if available"""
        try:
            # This would normally import the MCP tools
            # For now, we'll create a mock implementation
            self.available = True
            logger.info("✅ MCP transcript extraction available")
        except Exception as e:
            logger.warning(f"MCP transcript extraction not available: {e}")
    
    def extract_transcript(self, video_url: str) -> Optional[str]:
        """Extract transcript using MCP tools"""
        if not self.available:
            return None
        
        try:
            # Mock implementation - in real system this would use MCP tools
            # mcp__MCP_DOCKER__get_transcript(url=video_url)
            
            # For testing, return a mock transcript
            return f"Mock transcript for video: {video_url}"
            
        except Exception as e:
            logger.error(f"Error extracting transcript: {e}")
            return None
    
    def is_available(self) -> bool:
        """Check if MCP transcript extraction is available"""
        return self.available

class TranscriptAnalyzer:
    """Analyze transcript content for insights and relevance"""
    
    def __init__(self, priority_topics: List[str], priority_weights: Dict[str, float]):
        self.priority_topics = priority_topics
        self.priority_weights = priority_weights
    
    def analyze_transcript(self, video_id: str, transcript: str, 
                         title: str, priority_topics: List[str]) -> TranscriptAnalysis:
        """Analyze transcript content for insights"""
        start_time = time.time()
        
        # Basic analysis
        transcript_length = len(transcript)
        words = transcript.lower().split()
        
        # Find key concepts (important technical terms)
        key_concepts = self._extract_key_concepts(transcript)
        
        # Check priority topic matches
        topic_matches = self._find_topic_matches(transcript, priority_topics)
        
        # Calculate scores
        technical_depth = self._calculate_technical_depth(transcript, words)
        educational_value = self._calculate_educational_value(transcript, words)
        actionable_insights = self._count_actionable_insights(transcript)
        
        # Generate summary
        summary = self._generate_summary(transcript, title, key_concepts)
        
        # Generate full analysis
        full_analysis = self._generate_full_analysis(
            transcript, title, key_concepts, topic_matches, 
            technical_depth, educational_value, actionable_insights
        )
        
        processing_time = time.time() - start_time
        
        return TranscriptAnalysis(
            video_id=video_id,
            transcript_length=transcript_length,
            key_concepts=key_concepts,
            priority_topic_matches=topic_matches,
            technical_depth_score=technical_depth,
            educational_value_score=educational_value,
            actionable_insights_count=actionable_insights,
            summary=summary,
            full_analysis=full_analysis,
            processing_time=processing_time
        )
    
    def _extract_key_concepts(self, transcript: str) -> List[str]:
        """Extract key technical concepts from transcript"""
        text = transcript.lower()
        
        # Technical keywords to look for
        technical_terms = [
            'typescript', 'javascript', 'react', 'nextjs', 'node.js',
            'claude', 'api', 'database', 'architecture', 'framework',
            'algorithm', 'optimization', 'performance', 'security',
            'authentication', 'deployment', 'devops', 'testing',
            'frontend', 'backend', 'fullstack', 'ai', 'machine learning'
        ]
        
        concepts = []
        for term in technical_terms:
            if term in text:
                # Count occurrences
                count = text.count(term)
                if count > 2:  # Only include terms mentioned multiple times
                    concepts.append(f"{term} ({count}x)")
        
        return concepts[:10]  # Top 10 concepts
    
    def _find_topic_matches(self, transcript: str, priority_topics: List[str]) -> List[str]:
        """Find matches with priority topics"""
        text = transcript.lower()
        matches = []
        
        for topic in priority_topics:
            if topic.lower() in text:
                matches.append(topic)
        
        return matches
    
    def _calculate_technical_depth(self, transcript: str, words: List[str]) -> float:
        """Calculate technical depth score"""
        technical_indicators = [
            'implementation', 'architecture', 'algorithm', 'optimization',
            'performance', 'scalability', 'design pattern', 'best practice',
            'configuration', 'deployment', 'testing', 'debugging'
        ]
        
        depth_score = 0
        total_words = len(words)
        
        for indicator in technical_indicators:
            if indicator in transcript.lower():
                depth_score += transcript.lower().count(indicator)
        
        # Normalize to 0-1 scale
        return min(depth_score / (total_words / 100), 1.0)
    
    def _calculate_educational_value(self, transcript: str, words: List[str]) -> float:
        """Calculate educational value score"""
        educational_indicators = [
            'how to', 'tutorial', 'guide', 'example', 'demonstration',
            'step by step', 'learn', 'understand', 'explain', 'show you',
            'beginner', 'advanced', 'tip', 'trick', 'mistake', 'avoid'
        ]
        
        edu_score = 0
        for indicator in educational_indicators:
            if indicator in transcript.lower():
                edu_score += transcript.lower().count(indicator)
        
        # Normalize to 0-1 scale
        return min(edu_score / 10, 1.0)
    
    def _count_actionable_insights(self, transcript: str) -> int:
        """Count actionable insights in transcript"""
        actionable_patterns = [
            'you should', 'you can', 'try this', 'use this', 'avoid this',
            'remember to', 'make sure', 'don\'t forget', 'pro tip',
            'here\'s how', 'solution', 'fix', 'improvement'
        ]
        
        count = 0
        text = transcript.lower()
        
        for pattern in actionable_patterns:
            count += text.count(pattern)
        
        return count
    
    def _generate_summary(self, transcript: str, title: str, concepts: List[str]) -> str:
        """Generate a summary of the transcript"""
        # Simple extractive summary
        sentences = transcript.split('. ')
        
        # Take first few sentences and those with key concepts
        summary_sentences = sentences[:2]  # Opening sentences
        
        for sentence in sentences[2:10]:  # Check middle sentences
            if any(concept.split(' (')[0] in sentence.lower() for concept in concepts):
                summary_sentences.append(sentence)
                if len(summary_sentences) >= 4:
                    break
        
        summary = '. '.join(summary_sentences)
        if len(summary) > 500:
            summary = summary[:500] + "..."
        
        return summary
    
    def _generate_full_analysis(self, transcript: str, title: str, concepts: List[str],
                              topic_matches: List[str], technical_depth: float,
                              educational_value: float, actionable_insights: int) -> str:
        """Generate comprehensive analysis"""
        
        analysis = f"""# Transcript Analysis: {title}

## Key Technical Concepts
{', '.join(concepts) if concepts else 'No major technical concepts identified'}

## Priority Topic Matches
{', '.join(topic_matches) if topic_matches else 'No priority topic matches found'}

## Content Quality Scores
- Technical Depth: {technical_depth:.2f}/1.0
- Educational Value: {educational_value:.2f}/1.0
- Actionable Insights: {actionable_insights} identified

## Content Summary
{self._generate_summary(transcript, title, concepts)}

## Recommendations
"""
        
        if technical_depth > 0.7:
            analysis += "- High technical depth - suitable for experienced developers\n"
        elif technical_depth > 0.4:
            analysis += "- Moderate technical depth - good for intermediate learners\n"
        else:
            analysis += "- Basic technical content - suitable for beginners\n"
        
        if educational_value > 0.6:
            analysis += "- Strong educational value - good for learning purposes\n"
        
        if actionable_insights > 5:
            analysis += "- Rich in actionable insights - highly practical content\n"
        
        if topic_matches:
            analysis += f"- Relevant to priority topics: {', '.join(topic_matches)}\n"
        
        return analysis

class TranscriptProcessor:
    """Main transcript processing system with selective extraction"""
    
    def __init__(self, transcript_threshold: float = 0.75, max_concurrent: int = 3):
        self.base_path = Path(__file__).parent
        self.data_path = self.base_path / "data"
        self.queue_path = self.data_path / "processing_queue"
        self.transcript_threshold = transcript_threshold
        self.max_concurrent = max_concurrent
        
        # Initialize components
        self.mcp_extractor = MCPTranscriptExtractor()
        self.analyzer = TranscriptAnalyzer(
            priority_topics=['claude', 'react', 'typescript', 'nextjs'],
            priority_weights={'claude': 2.0, 'react': 1.5, 'typescript': 1.4, 'nextjs': 1.3}
        )
        
        # Create directories
        self.queue_path.mkdir(parents=True, exist_ok=True)
        (self.data_path / "transcripts").mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Transcript Processor initialized with threshold {transcript_threshold}")
        logger.info(f"MCP extraction available: {self.mcp_extractor.is_available()}")
    
    def add_video_to_queue(self, video_metadata: Dict[str, Any]) -> bool:
        """Add a video to the transcript processing queue if it meets criteria"""
        
        importance_score = video_metadata.get('importance_score', 0.0)
        
        # Only queue high-value videos
        if importance_score < self.transcript_threshold:
            return False
        
        video_id = video_metadata['id']
        
        # Check if already processed or queued
        if self._is_already_processed(video_id) or self._is_already_queued(video_id):
            return False
        
        # Determine priority based on score
        if importance_score >= 0.9:
            priority = "high"
        elif importance_score >= 0.8:
            priority = "medium"
        else:
            priority = "low"
        
        task = TranscriptTask(
            video_id=video_id,
            title=video_metadata.get('title', 'Unknown Title'),
            channel_name=video_metadata.get('channel_name', 'Unknown Channel'),
            importance_score=importance_score,
            priority_topics=video_metadata.get('priority_topics', []),
            priority=priority,
            queued_at=datetime.now(timezone.utc).isoformat()
        )
        
        # Save task to queue
        task_file = self.queue_path / f"task_{video_id}.json"
        with open(task_file, 'w') as f:
            json.dump(asdict(task), f, indent=2)
        
        logger.info(f"📋 Added video to transcript queue: {task.title[:50]}... (score: {importance_score:.3f})")
        return True
    
    def _is_already_processed(self, video_id: str) -> bool:
        """Check if transcript already processed"""
        transcript_file = self.data_path / "transcripts" / f"{video_id}.json"
        return transcript_file.exists()
    
    def _is_already_queued(self, video_id: str) -> bool:
        """Check if video already in queue"""
        task_file = self.queue_path / f"task_{video_id}.json"
        return task_file.exists()
    
    def get_queue_status(self) -> Dict[str, Any]:
        """Get processing queue status"""
        queue_files = list(self.queue_path.glob("task_*.json"))
        
        status = {
            "total_queued": len(queue_files),
            "pending": 0,
            "processing": 0,
            "completed": 0,
            "failed": 0,
            "high_priority": 0,
            "medium_priority": 0,
            "low_priority": 0
        }
        
        for task_file in queue_files:
            try:
                with open(task_file, 'r') as f:
                    task_data = json.load(f)
                    
                status[task_data.get('status', 'pending')] += 1
                status[f"{task_data.get('priority', 'low')}_priority"] += 1
                
            except Exception as e:
                logger.error(f"Error reading task file {task_file}: {e}")
        
        return status
    
    def process_transcript_queue(self, max_videos: Optional[int] = None) -> Dict[str, Any]:
        """Process videos in transcript queue"""
        
        if not self.mcp_extractor.is_available():
            logger.warning("MCP transcript extraction not available")
            return {"status": "error", "message": "MCP extraction not available"}
        
        logger.info("🔄 Starting transcript queue processing")
        
        # Get pending tasks sorted by priority and score
        pending_tasks = self._get_pending_tasks()
        
        if max_videos:
            pending_tasks = pending_tasks[:max_videos]
        
        results = {
            "started_at": datetime.now(timezone.utc).isoformat(),
            "total_tasks": len(pending_tasks),
            "processed": 0,
            "successful": 0,
            "failed": 0,
            "processing_time": 0,
            "task_results": []
        }
        
        start_time = time.time()
        
        for task_data in pending_tasks:
            try:
                result = self._process_single_task(task_data)
                results["task_results"].append(result)
                
                if result.get("status") == "success":
                    results["successful"] += 1
                else:
                    results["failed"] += 1
                
                results["processed"] += 1
                
            except Exception as e:
                logger.error(f"Error processing task {task_data.get('video_id')}: {e}")
                results["failed"] += 1
        
        results["processing_time"] = time.time() - start_time
        results["completed_at"] = datetime.now(timezone.utc).isoformat()
        
        logger.info(f"✅ Queue processing complete: {results['successful']}/{results['total_tasks']} successful")
        
        return results
    
    def _get_pending_tasks(self) -> List[Dict[str, Any]]:
        """Get pending tasks sorted by priority"""
        tasks = []
        
        for task_file in self.queue_path.glob("task_*.json"):
            try:
                with open(task_file, 'r') as f:
                    task_data = json.load(f)
                    
                if task_data.get('status') == 'pending':
                    tasks.append(task_data)
                    
            except Exception as e:
                logger.error(f"Error reading task file {task_file}: {e}")
        
        # Sort by priority (high first) and importance score
        priority_order = {"high": 3, "medium": 2, "low": 1}
        tasks.sort(key=lambda x: (
            priority_order.get(x.get('priority', 'low'), 1),
            x.get('importance_score', 0)
        ), reverse=True)
        
        return tasks
    
    def _process_single_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single transcript extraction task"""
        video_id = task_data['video_id']
        title = task_data['title']
        
        logger.info(f"🎬 Processing transcript: {title[:50]}...")
        
        # Update task status
        task_data['status'] = 'processing'
        task_data['processing_started_at'] = datetime.now(timezone.utc).isoformat()
        self._save_task(task_data)
        
        try:
            # Extract transcript
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            transcript = self.mcp_extractor.extract_transcript(video_url)
            
            if not transcript:
                raise Exception("Failed to extract transcript")
            
            # Analyze transcript
            analysis = self.analyzer.analyze_transcript(
                video_id=video_id,
                transcript=transcript,
                title=title,
                priority_topics=task_data.get('priority_topics', [])
            )
            
            # Save results
            transcript_data = {
                "video_id": video_id,
                "title": title,
                "channel_name": task_data.get('channel_name'),
                "importance_score": task_data.get('importance_score'),
                "transcript": transcript,
                "analysis": asdict(analysis),
                "processed_at": datetime.now(timezone.utc).isoformat(),
                "processing_time": analysis.processing_time
            }
            
            transcript_file = self.data_path / "transcripts" / f"{video_id}.json"
            with open(transcript_file, 'w') as f:
                json.dump(transcript_data, f, indent=2)
            
            # Update task status
            task_data['status'] = 'completed'
            task_data['processed_at'] = datetime.now(timezone.utc).isoformat()
            task_data['transcript_length'] = analysis.transcript_length
            task_data['analysis_summary'] = analysis.summary
            self._save_task(task_data)
            
            logger.info(f"✅ Transcript processed successfully: {len(transcript)} chars, {len(analysis.key_concepts)} concepts")
            
            return {
                "video_id": video_id,
                "title": title,
                "status": "success",
                "transcript_length": analysis.transcript_length,
                "key_concepts": len(analysis.key_concepts),
                "processing_time": analysis.processing_time
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to process transcript: {e}")
            
            # Update task with error
            task_data['status'] = 'failed'
            task_data['error'] = str(e)
            task_data['attempts'] += 1
            self._save_task(task_data)
            
            return {
                "video_id": video_id,
                "title": title,
                "status": "failed",
                "error": str(e)
            }
    
    def _save_task(self, task_data: Dict[str, Any]):
        """Save task data to file"""
        video_id = task_data['video_id']
        task_file = self.queue_path / f"task_{video_id}.json"
        
        with open(task_file, 'w') as f:
            json.dump(task_data, f, indent=2)
    
    def get_processed_transcripts(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get list of processed transcripts"""
        transcript_files = list((self.data_path / "transcripts").glob("*.json"))
        transcripts = []
        
        for transcript_file in transcript_files:
            try:
                with open(transcript_file, 'r') as f:
                    data = json.load(f)
                    
                # Include summary info only
                transcripts.append({
                    "video_id": data["video_id"],
                    "title": data["title"],
                    "channel_name": data["channel_name"],
                    "importance_score": data["importance_score"],
                    "transcript_length": len(data["transcript"]),
                    "processed_at": data["processed_at"],
                    "key_concepts": data["analysis"]["key_concepts"],
                    "priority_topic_matches": data["analysis"]["priority_topic_matches"],
                    "technical_depth_score": data["analysis"]["technical_depth_score"],
                    "educational_value_score": data["analysis"]["educational_value_score"]
                })
                
            except Exception as e:
                logger.error(f"Error reading transcript file {transcript_file}: {e}")
        
        # Sort by importance score
        transcripts.sort(key=lambda x: x["importance_score"], reverse=True)
        
        return transcripts[:limit] if limit else transcripts
    
    def cleanup_completed_tasks(self, keep_days: int = 7):
        """Clean up completed tasks older than specified days"""
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=keep_days)
        cleaned = 0
        
        for task_file in self.queue_path.glob("task_*.json"):
            try:
                with open(task_file, 'r') as f:
                    task_data = json.load(f)
                
                if task_data.get('status') in ['completed', 'failed']:
                    processed_at = task_data.get('processed_at')
                    if processed_at:
                        processed_date = datetime.fromisoformat(processed_at.replace('Z', '+00:00'))
                        if processed_date < cutoff_date:
                            task_file.unlink()
                            cleaned += 1
                            
            except Exception as e:
                logger.error(f"Error cleaning task file {task_file}: {e}")
        
        if cleaned > 0:
            logger.info(f"🧹 Cleaned up {cleaned} old completed tasks")
        
        return cleaned

def main():
    """Test the transcript processing system"""
    
    print("🎬 Transcript Processor - Test Mode")
    print("=" * 50)
    
    processor = TranscriptProcessor()
    
    # Show queue status
    status = processor.get_queue_status()
    print(f"📊 Queue Status:")
    print(f"   Total queued: {status['total_queued']}")
    print(f"   Pending: {status['pending']}")
    print(f"   Processing: {status['processing']}")
    print(f"   Completed: {status['completed']}")
    print(f"   Failed: {status['failed']}")
    
    # Test adding a high-value video to queue
    test_video = {
        "id": "test_video_123",
        "title": "Advanced React TypeScript Patterns with Claude AI",
        "channel_name": "Test Channel",
        "importance_score": 0.85,
        "priority_topics": ["react", "typescript", "claude"]
    }
    
    print(f"\n🧪 Testing video queue addition...")
    added = processor.add_video_to_queue(test_video)
    print(f"   Video added to queue: {added}")
    
    # Show updated queue status
    status = processor.get_queue_status()
    print(f"\n📊 Updated Queue Status:")
    print(f"   Total queued: {status['total_queued']}")
    print(f"   High priority: {status['high_priority']}")
    print(f"   Medium priority: {status['medium_priority']}")
    print(f"   Low priority: {status['low_priority']}")
    
    # Show processed transcripts
    processed = processor.get_processed_transcripts(limit=5)
    print(f"\n📚 Processed Transcripts: {len(processed)}")
    for transcript in processed:
        print(f"   • {transcript['title'][:40]}... (score: {transcript['importance_score']:.3f})")
        if transcript.get('key_concepts'):
            print(f"     Concepts: {', '.join(transcript['key_concepts'][:3])}...")
    
    print(f"\n✅ Test completed!")

if __name__ == "__main__":
    main()