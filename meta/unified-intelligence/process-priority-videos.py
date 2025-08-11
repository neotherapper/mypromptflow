#!/usr/bin/env python3
"""
Priority Video Processing Script
Process high-value YouTube videos using MCP transcript integration
"""

import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

# Add unified intelligence directory to path
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

# Import MCP YouTube processor
from mcp_youtube_processor import MCPYouTubeProcessor, VideoAnalysisResult

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PriorityVideoProcessor:
    """Process priority videos with MCP transcript integration"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.processor = MCPYouTubeProcessor()
        self.knowledge_vault_path = self._get_knowledge_vault_path()
        
        # Priority videos to process
        self.priority_videos = [
            {
                'url': 'https://www.youtube.com/watch?v=KmYoJmZs3sY',
                'title': 'Introduction to TypeScript with React - Complete Tutorial',
                'channel': 'Tech Tutorial',
                'priority': 'high',
                'expected_topics': ['react', 'typescript'],
                'transcript': None  # Will be set via MCP
            }
        ]
    
    def _get_knowledge_vault_path(self) -> Path:
        """Get knowledge vault path for priority content"""
        vault_path = self.base_path.parent.parent / "knowledge-vault" / "databases" / "knowledge_vault" / "content-intelligence" / "priority-youtube"
        vault_path.mkdir(parents=True, exist_ok=True)
        return vault_path
    
    def set_transcript_for_video(self, video_url: str, transcript: str):
        """Set transcript for a specific video (called from MCP context)"""
        for video in self.priority_videos:
            if video['url'] == video_url:
                video['transcript'] = transcript
                logger.info(f"Transcript set for video: {video_url}")
                return True
        return False
    
    def process_video_with_transcript(self, video_data: Dict[str, Any]) -> Optional[VideoAnalysisResult]:
        """Process a single video with its transcript"""
        try:
            if not video_data.get('transcript'):
                logger.warning(f"No transcript available for {video_data['url']}")
                return None
            
            # Create a modified version of the processor that uses our transcript
            result = self._analyze_video_with_real_transcript(video_data)
            
            if result:
                self._save_priority_result(result)
                logger.info(f"Successfully processed: {video_data['title']}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing video {video_data['url']}: {str(e)}")
            return None
    
    def _analyze_video_with_real_transcript(self, video_data: Dict[str, Any]) -> Optional[VideoAnalysisResult]:
        """Analyze video using real transcript data"""
        transcript = video_data['transcript']
        title = video_data['title']
        channel = video_data['channel']
        video_url = video_data['url']
        
        # Extract video ID
        video_id = self.processor.extract_video_id(video_url)
        if not video_id:
            logger.error(f"Could not extract video ID from: {video_url}")
            return None
        
        # Extract programming concepts from real transcript
        concepts = self.processor.extract_programming_concepts(transcript)
        
        # Analyze for priority topics using real transcript
        priority_topics, topic_scores = self.processor.analyze_content_for_priority_topics(title, transcript)
        
        # Generate content summary from real transcript
        content_summary = self.processor.generate_content_summary(title, transcript, concepts)
        
        # Calculate unified intelligence score
        unified_score = self.processor.calculate_unified_intelligence_score(
            title, transcript, concepts, priority_topics, topic_scores
        )
        
        # Generate enhanced insights for priority content
        insights = self._generate_enhanced_insights(transcript, concepts, priority_topics, video_data)
        
        return VideoAnalysisResult(
            video_id=video_id,
            video_url=video_url,
            title=title,
            channel=channel,
            transcript_text=transcript,
            programming_concepts=concepts,
            priority_topics=priority_topics,
            topic_scores=topic_scores,
            unified_score=unified_score,
            content_summary=content_summary,
            insights=insights,
            processing_timestamp=datetime.now(timezone.utc).isoformat()
        )
    
    def _generate_enhanced_insights(self, transcript: str, concepts: List[str], 
                                  priority_topics: List[str], video_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate enhanced insights for priority content"""
        transcript_lower = transcript.lower()
        
        # Enhanced analysis for priority videos
        insights = {
            'priority_video': True,
            'expected_topics_covered': self._check_expected_topics(priority_topics, video_data.get('expected_topics', [])),
            'concept_count': len(concepts),
            'transcript_length': len(transcript),
            'topic_diversity': len(priority_topics),
            'technical_depth': len([c for c in concepts if c in ['architecture', 'optimization', 'performance', 'implementation']]),
            'content_quality_indicators': {
                'has_code_examples': any(indicator in transcript_lower for indicator in ['example', 'code', 'import', 'function', 'const', 'let']),
                'has_explanations': any(indicator in transcript_lower for indicator in ['explain', 'understand', 'how to', 'what is', 'why']),
                'has_best_practices': any(indicator in transcript_lower for indicator in ['best practice', 'should', 'recommended', 'convention']),
                'has_troubleshooting': any(indicator in transcript_lower for indicator in ['error', 'fix', 'debug', 'issue', 'problem']),
                'has_step_by_step': any(indicator in transcript_lower for indicator in ['step', 'first', 'next', 'then', 'finally']),
                'has_practical_demo': any(indicator in transcript_lower for indicator in ['demo', 'build', 'create', 'implement', 'tutorial'])
            },
            'topic_score_breakdown': {},
            'top_concepts': concepts[:10],
            'learning_value_indicators': {
                'beginner_friendly': any(indicator in transcript_lower for indicator in ['basic', 'beginner', 'introduction', 'getting started', 'from scratch']),
                'advanced_concepts': any(indicator in transcript_lower for indicator in ['advanced', 'complex', 'architecture', 'optimization', 'performance']),
                'comprehensive_coverage': len(concepts) > 15,
                'practical_focus': any(indicator in transcript_lower for indicator in ['build', 'create', 'implement', 'project', 'application'])
            },
            'transcript_analysis': {
                'word_count': len(transcript.split()),
                'unique_technical_terms': len(set(concepts)),
                'code_discussion_density': transcript_lower.count('code') + transcript_lower.count('function') + transcript_lower.count('component'),
                'explanation_quality': transcript_lower.count('because') + transcript_lower.count('reason') + transcript_lower.count('explain')
            }
        }
        
        return insights
    
    def _check_expected_topics(self, found_topics: List[str], expected_topics: List[str]) -> Dict[str, Any]:
        """Check if expected topics were covered"""
        covered = [topic for topic in expected_topics if topic in found_topics]
        missing = [topic for topic in expected_topics if topic not in found_topics]
        
        return {
            'expected': expected_topics,
            'found': found_topics,
            'covered': covered,
            'missing': missing,
            'coverage_percentage': len(covered) / len(expected_topics) * 100 if expected_topics else 100
        }
    
    def _save_priority_result(self, result: VideoAnalysisResult) -> Path:
        """Save priority video analysis result"""
        # Create directory structure: priority/date/
        process_date = datetime.now().strftime('%Y-%m-%d')
        save_dir = self.knowledge_vault_path / process_date
        save_dir.mkdir(parents=True, exist_ok=True)
        
        # Save main result file with enhanced structure
        result_file = save_dir / f"{result.video_id}_priority_unified_intelligence.json"
        
        # Convert to enhanced saveable format
        result_dict = {
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
            'processed_with': 'priority-video-processor',
            'framework_version': '1.0.0',
            'content_type': 'priority_youtube_video',
            'transcript_available': bool(result.transcript_text),
            'quality_score': self._calculate_quality_score(result),
            'error': result.error
        }
        
        with open(result_file, 'w') as f:
            json.dump(result_dict, f, indent=2)
        
        # Save transcript with enhanced metadata
        if result.transcript_text:
            transcript_file = save_dir / f"{result.video_id}_priority_transcript.txt"
            with open(transcript_file, 'w') as f:
                f.write(f"# PRIORITY VIDEO ANALYSIS\n")
                f.write(f"# Title: {result.title}\n")
                f.write(f"# Channel: {result.channel}\n")
                f.write(f"# Video URL: {result.video_url}\n")
                f.write(f"# Processing Date: {result.processing_timestamp}\n")
                f.write(f"# Unified Score: {result.unified_score:.3f}\n")
                f.write(f"# Priority Topics: {', '.join(result.priority_topics)}\n")
                f.write(f"# Programming Concepts: {len(result.programming_concepts)}\n")
                f.write(f"# Quality Score: {self._calculate_quality_score(result):.3f}\n")
                f.write(f"\n{'='*80}\n")
                f.write(f"TRANSCRIPT\n")
                f.write(f"{'='*80}\n\n")
                f.write(result.transcript_text)
        
        logger.info(f"Saved priority analysis result: {result_file}")
        return result_file
    
    def _calculate_quality_score(self, result: VideoAnalysisResult) -> float:
        """Calculate enhanced quality score for priority videos"""
        base_score = result.unified_score
        
        # Quality bonuses
        quality_indicators = result.insights.get('content_quality_indicators', {})
        learning_indicators = result.insights.get('learning_value_indicators', {})
        
        quality_bonus = 0.0
        quality_bonus += 0.1 if quality_indicators.get('has_code_examples') else 0
        quality_bonus += 0.1 if quality_indicators.get('has_practical_demo') else 0
        quality_bonus += 0.08 if quality_indicators.get('has_step_by_step') else 0
        quality_bonus += 0.05 if quality_indicators.get('has_best_practices') else 0
        quality_bonus += 0.07 if learning_indicators.get('practical_focus') else 0
        quality_bonus += 0.05 if learning_indicators.get('comprehensive_coverage') else 0
        
        # Topic coverage bonus
        expected_coverage = result.insights.get('expected_topics_covered', {})
        coverage_percentage = expected_coverage.get('coverage_percentage', 0) / 100
        quality_bonus += coverage_percentage * 0.15
        
        final_score = min(base_score + quality_bonus, 1.0)
        return final_score
    
    def process_all_priority_videos(self) -> List[VideoAnalysisResult]:
        """Process all priority videos"""
        results = []
        
        for video_data in self.priority_videos:
            if video_data.get('transcript'):
                result = self.process_video_with_transcript(video_data)
                if result:
                    results.append(result)
            else:
                logger.warning(f"Skipping video without transcript: {video_data['url']}")
        
        return results
    
    def generate_priority_report(self, results: List[VideoAnalysisResult]) -> Dict[str, Any]:
        """Generate comprehensive report for priority videos"""
        if not results:
            return {"error": "No priority results to report"}
        
        # Calculate enhanced statistics
        avg_score = sum(r.unified_score for r in results) / len(results)
        avg_quality = sum(self._calculate_quality_score(r) for r in results) / len(results)
        
        # Topic analysis
        all_topics = []
        all_concepts = []
        for result in results:
            all_topics.extend(result.priority_topics)
            all_concepts.extend(result.programming_concepts)
        
        topic_frequency = {}
        for topic in all_topics:
            topic_frequency[topic] = topic_frequency.get(topic, 0) + 1
        
        concept_frequency = {}
        for concept in all_concepts:
            concept_frequency[concept] = concept_frequency.get(concept, 0) + 1
        
        # Generate enhanced report
        report = {
            'priority_processing_summary': {
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'total_priority_videos': len(results),
                'average_unified_score': round(avg_score, 3),
                'average_quality_score': round(avg_quality, 3),
                'high_value_videos': len([r for r in results if r.unified_score > 0.8]),
                'exceptional_quality_videos': len([r for r in results if self._calculate_quality_score(r) > 0.9]),
                'processor_version': 'priority-1.0.0'
            },
            'priority_videos_analyzed': [
                {
                    'title': r.title,
                    'channel': r.channel,
                    'video_url': r.video_url,
                    'unified_score': r.unified_score,
                    'quality_score': self._calculate_quality_score(r),
                    'priority_topics': r.priority_topics,
                    'concept_count': len(r.programming_concepts),
                    'learning_indicators': r.insights.get('learning_value_indicators', {}),
                    'expected_coverage': r.insights.get('expected_topics_covered', {}).get('coverage_percentage', 0)
                }
                for r in sorted(results, key=lambda x: self._calculate_quality_score(x), reverse=True)
            ],
            'topic_analysis': {
                'priority_topics_discovered': sorted(topic_frequency.items(), key=lambda x: x[1], reverse=True),
                'unique_topics': len(topic_frequency),
                'topic_distribution': topic_frequency
            },
            'concept_analysis': {
                'top_programming_concepts': sorted(concept_frequency.items(), key=lambda x: x[1], reverse=True)[:20],
                'unique_concepts_discovered': len(concept_frequency),
                'concept_categories': self._categorize_priority_concepts(list(concept_frequency.keys()))
            },
            'content_quality_metrics': {
                'videos_with_code_examples': len([r for r in results if r.insights.get('content_quality_indicators', {}).get('has_code_examples')]),
                'videos_with_practical_demos': len([r for r in results if r.insights.get('content_quality_indicators', {}).get('has_practical_demo')]),
                'comprehensive_tutorials': len([r for r in results if r.insights.get('learning_value_indicators', {}).get('comprehensive_coverage')]),
                'beginner_friendly_content': len([r for r in results if r.insights.get('learning_value_indicators', {}).get('beginner_friendly')])
            }
        }
        
        # Save enhanced report
        report_file = self.knowledge_vault_path / f"priority_processing_report_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Priority processing report saved: {report_file}")
        return report
    
    def _categorize_priority_concepts(self, concepts: List[str]) -> Dict[str, List[str]]:
        """Categorize concepts for priority content"""
        categories = {
            'react_ecosystem': [],
            'typescript_features': [],
            'development_tools': [],
            'best_practices': [],
            'advanced_concepts': [],
            'other': []
        }
        
        for concept in concepts:
            concept_lower = concept.lower()
            categorized = False
            
            # React ecosystem
            if any(keyword in concept_lower for keyword in ['react', 'jsx', 'component', 'hook', 'state', 'props']):
                categories['react_ecosystem'].append(concept)
                categorized = True
            # TypeScript features
            elif any(keyword in concept_lower for keyword in ['typescript', 'type', 'interface', 'generic', 'enum']):
                categories['typescript_features'].append(concept)
                categorized = True
            # Development tools
            elif any(keyword in concept_lower for keyword in ['vite', 'webpack', 'npm', 'yarn', 'eslint', 'prettier']):
                categories['development_tools'].append(concept)
                categorized = True
            # Best practices
            elif any(keyword in concept_lower for keyword in ['convention', 'pattern', 'practice', 'standard']):
                categories['best_practices'].append(concept)
                categorized = True
            # Advanced concepts
            elif any(keyword in concept_lower for keyword in ['optimization', 'performance', 'architecture', 'scalability']):
                categories['advanced_concepts'].append(concept)
                categorized = True
            
            if not categorized:
                categories['other'].append(concept)
        
        # Remove empty categories
        return {k: v for k, v in categories.items() if v}

def main():
    """Main function for priority video processing"""
    processor = PriorityVideoProcessor()
    
    print("🎯 Priority Video Processor")
    print("=" * 50)
    print(f"Processing {len(processor.priority_videos)} priority videos...")
    
    # Note: In actual MCP context, transcripts would be set via the MCP system
    # For demonstration, we show how the system would work
    
    print("\n📋 Priority Videos to Process:")
    for i, video in enumerate(processor.priority_videos, 1):
        print(f"   {i}. {video['title']}")
        print(f"      URL: {video['url']}")
        print(f"      Expected Topics: {', '.join(video['expected_topics'])}")
        print(f"      Priority: {video['priority']}")
        print()
    
    print("ℹ️  Note: This script requires MCP transcript integration to function fully.")
    print("   In Claude Code context, transcripts would be automatically provided.")
    print("   Run via Claude Code's MCP system for full functionality.")

if __name__ == "__main__":
    main()