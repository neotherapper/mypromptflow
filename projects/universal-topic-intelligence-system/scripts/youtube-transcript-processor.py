#!/usr/bin/env python3
"""
YouTube Transcript Processing System
Universal Topic Intelligence System - YouTube Content Analysis

This script demonstrates how to process YouTube video transcripts for educational content
extraction and integration with the Universal Topic Intelligence System.
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

@dataclass
class VideoMetadata:
    """Video metadata structure"""
    url: str
    title: str
    channel: str
    duration: Optional[int] = None
    upload_date: Optional[str] = None
    topics: List[str] = None
    rating: float = 0.0

@dataclass
class TranscriptInsights:
    """Structured insights from transcript analysis"""
    summary: str
    key_takeaways: List[str]
    code_examples: List[str]
    tools_mentioned: List[str]
    learning_resources: List[str]
    timestamps: Dict[str, str]
    relevance_score: float

class YouTubeTranscriptProcessor:
    """Process YouTube transcripts for programming education content"""
    
    def __init__(self):
        self.programming_keywords = [
            'javascript', 'python', 'react', 'typescript', 'node.js', 'css', 'html',
            'api', 'database', 'framework', 'library', 'function', 'variable',
            'programming', 'development', 'code', 'software', 'web', 'frontend',
            'backend', 'fullstack', 'tutorial', 'guide', 'learn', 'development'
        ]
        
        self.quality_indicators = [
            'best practice', 'optimization', 'performance', 'security', 'testing',
            'debugging', 'refactoring', 'architecture', 'design pattern'
        ]
    
    def extract_transcript_via_mcp(self, video_url: str) -> str:
        """
        Extract transcript using MCP Docker tool
        Note: This would call the actual MCP tool in real implementation
        """
        # Pseudo-code for MCP integration
        # transcript = mcp__MCP_DOCKER__get_transcript(url=video_url)
        # return transcript
        
        # For demo purposes, return sample structure
        return "Sample transcript would be extracted here using MCP tool"
    
    def clean_transcript(self, raw_transcript: str) -> str:
        """Clean and format transcript text"""
        # Remove music notation [♪♪♪]
        cleaned = re.sub(r'\[♪+\]', '', raw_transcript)
        
        # Remove repeated musical symbols
        cleaned = re.sub(r'♪+', '', cleaned)
        
        # Remove excessive whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        # Remove common intro/outro patterns
        intro_patterns = [
            r"^.*?welcome to.*?let's get started",
            r"^.*?hey everyone.*?today we're",
            r"^.*?what's up.*?in this video"
        ]
        
        for pattern in intro_patterns:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE)
        
        return cleaned.strip()
    
    def calculate_relevance_score(self, transcript: str, channel_rating: float = 4.0) -> float:
        """Calculate content relevance score for programming education"""
        score = 0.0
        words = transcript.lower().split()
        total_words = len(words)
        
        if total_words == 0:
            return 0.0
        
        # Programming keyword density
        programming_matches = sum(1 for word in words if any(keyword in word for keyword in self.programming_keywords))
        programming_density = programming_matches / total_words
        score += programming_density * 0.4
        
        # Quality indicators
        quality_matches = sum(1 for phrase in self.quality_indicators if phrase in transcript.lower())
        quality_density = quality_matches / (total_words / 100)  # per 100 words
        score += min(quality_density * 0.2, 0.2)
        
        # Channel authority multiplier
        channel_multiplier = channel_rating / 5.0  # Normalize to 0-1
        score *= (0.8 + 0.2 * channel_multiplier)
        
        # Educational structure indicators
        educational_patterns = [
            'first', 'second', 'next', 'then', 'finally',
            'step', 'example', 'demonstrate', 'show you'
        ]
        educational_matches = sum(1 for pattern in educational_patterns if pattern in transcript.lower())
        educational_density = educational_matches / (total_words / 100)
        score += min(educational_density * 0.1, 0.1)
        
        return min(score, 1.0)
    
    def extract_code_examples(self, transcript: str) -> List[str]:
        """Extract code examples and snippets mentioned in transcript"""
        code_examples = []
        
        # Look for code-related language patterns
        code_patterns = [
            r'const\s+\w+\s*=',
            r'function\s+\w+\s*\(',
            r'import\s+.*?from',
            r'class\s+\w+\s*{',
            r'def\s+\w+\s*\(',
            r'<\w+.*?>'  # HTML/JSX tags
        ]
        
        for pattern in code_patterns:
            matches = re.findall(pattern, transcript, re.IGNORECASE)
            code_examples.extend(matches)
        
        # Look for explicit code mentions
        code_mention_patterns = [
            r'here\'s the code.*?(?=\.|$)',
            r'the code looks like.*?(?=\.|$)',
            r'you can write.*?(?=\.|$)'
        ]
        
        for pattern in code_mention_patterns:
            matches = re.findall(pattern, transcript, re.IGNORECASE | re.DOTALL)
            code_examples.extend(matches)
        
        return list(set(code_examples))[:10]  # Limit to top 10, remove duplicates
    
    def extract_tools_mentioned(self, transcript: str) -> List[str]:
        """Extract development tools and technologies mentioned"""
        tools_database = [
            'vscode', 'visual studio code', 'webstorm', 'sublime text',
            'git', 'github', 'gitlab', 'bitbucket',
            'npm', 'yarn', 'webpack', 'vite', 'parcel',
            'react', 'vue', 'angular', 'svelte', 'next.js', 'nuxt',
            'node.js', 'express', 'fastapi', 'django', 'flask',
            'mongodb', 'postgresql', 'mysql', 'redis',
            'docker', 'kubernetes', 'aws', 'vercel', 'netlify',
            'typescript', 'javascript', 'python', 'go', 'rust',
            'tailwind', 'bootstrap', 'sass', 'less'
        ]
        
        mentioned_tools = []
        transcript_lower = transcript.lower()
        
        for tool in tools_database:
            if tool in transcript_lower:
                mentioned_tools.append(tool)
        
        return mentioned_tools
    
    def extract_key_takeaways(self, transcript: str) -> List[str]:
        """Extract key learning points and takeaways"""
        takeaway_patterns = [
            r'the key point is.*?(?=\.|$)',
            r'remember that.*?(?=\.|$)',
            r'important to.*?(?=\.|$)',
            r'best practice.*?(?=\.|$)',
            r'pro tip.*?(?=\.|$)',
            r'the main thing.*?(?=\.|$)'
        ]
        
        takeaways = []
        for pattern in takeaway_patterns:
            matches = re.findall(pattern, transcript, re.IGNORECASE | re.DOTALL)
            takeaways.extend(matches)
        
        # Clean and format takeaways
        cleaned_takeaways = []
        for takeaway in takeaways:
            cleaned = re.sub(r'\s+', ' ', takeaway.strip())
            if len(cleaned) > 20 and len(cleaned) < 200:  # Reasonable length
                cleaned_takeaways.append(cleaned)
        
        return cleaned_takeaways[:5]  # Top 5 takeaways
    
    def generate_summary(self, transcript: str, max_length: int = 500) -> str:
        """Generate a concise summary of the video content"""
        # Simple extractive summarization based on sentence importance
        sentences = re.split(r'[.!?]+', transcript)
        
        # Score sentences based on keyword density and position
        scored_sentences = []
        for i, sentence in enumerate(sentences):
            if len(sentence.strip()) < 20:  # Skip very short sentences
                continue
                
            score = 0.0
            words = sentence.lower().split()
            
            # Keyword relevance
            keyword_matches = sum(1 for word in words if any(kw in word for kw in self.programming_keywords))
            score += keyword_matches / len(words) if words else 0
            
            # Position bonus (early sentences often contain key info)
            position_bonus = 1.0 - (i / len(sentences)) * 0.3
            score *= position_bonus
            
            scored_sentences.append((score, sentence.strip()))
        
        # Select top sentences for summary
        scored_sentences.sort(reverse=True, key=lambda x: x[0])
        selected_sentences = [sent for _, sent in scored_sentences[:3]]
        
        summary = '. '.join(selected_sentences)
        
        # Truncate if too long
        if len(summary) > max_length:
            summary = summary[:max_length-3] + '...'
        
        return summary
    
    def extract_timestamps(self, transcript: str) -> Dict[str, str]:
        """Extract important timestamps and their descriptions"""
        # This would require timing information from the original transcript
        # For demo purposes, return sample structure
        return {
            "00:30": "Introduction and setup",
            "05:15": "Main concept explanation", 
            "12:45": "Code example walkthrough",
            "18:20": "Best practices discussion",
            "22:10": "Conclusion and next steps"
        }
    
    def process_video(self, video_metadata: VideoMetadata) -> TranscriptInsights:
        """Process a complete video for insights extraction"""
        
        # Extract transcript (via MCP in real implementation)
        raw_transcript = self.extract_transcript_via_mcp(video_metadata.url)
        
        # Clean the transcript
        cleaned_transcript = self.clean_transcript(raw_transcript)
        
        # Calculate relevance
        relevance_score = self.calculate_relevance_score(cleaned_transcript, video_metadata.rating)
        
        # Skip processing if relevance is too low
        if relevance_score < 0.5:
            return TranscriptInsights(
                summary="Content relevance too low for processing",
                key_takeaways=[],
                code_examples=[],
                tools_mentioned=[],
                learning_resources=[],
                timestamps={},
                relevance_score=relevance_score
            )
        
        # Extract insights
        insights = TranscriptInsights(
            summary=self.generate_summary(cleaned_transcript),
            key_takeaways=self.extract_key_takeaways(cleaned_transcript),
            code_examples=self.extract_code_examples(cleaned_transcript),
            tools_mentioned=self.extract_tools_mentioned(cleaned_transcript),
            learning_resources=[],  # Would extract from transcript analysis
            timestamps=self.extract_timestamps(cleaned_transcript),
            relevance_score=relevance_score
        )
        
        return insights
    
    def save_insights_to_knowledge_vault(self, video_metadata: VideoMetadata, insights: TranscriptInsights, base_path: str = "knowledge-vault/youtube-content/"):
        """Save processed insights to knowledge vault structure"""
        
        # Create file structure
        channel_slug = video_metadata.channel.lower().replace(' ', '_').replace('-', '_')
        date_str = datetime.now().strftime('%Y-%m-%d')
        
        # Generate file paths
        transcript_path = f"{base_path}{channel_slug}/{date_str}/transcript.md"
        insights_path = f"{base_path}{channel_slug}/{date_str}/insights.md"
        metadata_path = f"{base_path}{channel_slug}/{date_str}/metadata.json"
        
        # Prepare content
        transcript_content = f"""# {video_metadata.title}
        
**Channel:** {video_metadata.channel}
**URL:** {video_metadata.url}  
**Date:** {date_str}
**Relevance Score:** {insights.relevance_score:.2f}

## Summary
{insights.summary}

## Key Takeaways
{chr(10).join(f"- {takeaway}" for takeaway in insights.key_takeaways)}

## Tools Mentioned
{chr(10).join(f"- {tool}" for tool in insights.tools_mentioned)}

## Code Examples  
{chr(10).join(f"```{chr(10)}{example}{chr(10)}```" for example in insights.code_examples)}

## Important Timestamps
{chr(10).join(f"- **{time}**: {desc}" for time, desc in insights.timestamps.items())}
"""

        metadata_content = {
            "video_url": video_metadata.url,
            "channel": video_metadata.channel,
            "title": video_metadata.title,
            "processing_date": date_str,
            "relevance_score": insights.relevance_score,
            "topics": video_metadata.topics or [],
            "tools_mentioned": insights.tools_mentioned,
            "quality_indicators": len(insights.key_takeaways)
        }
        
        return {
            "transcript_path": transcript_path,
            "insights_path": insights_path, 
            "metadata_path": metadata_path,
            "transcript_content": transcript_content,
            "metadata_content": metadata_content
        }

# Example usage demonstration
def demo_processing():
    """Demonstrate the YouTube transcript processing system"""
    
    processor = YouTubeTranscriptProcessor()
    
    # Sample video metadata (from your channel list)
    sample_video = VideoMetadata(
        url="https://www.youtube.com/watch?v=example123",
        title="React Best Practices for 2024",
        channel="ThePrimeagen",
        duration=1200,  # 20 minutes
        topics=["react", "javascript", "best-practices"],
        rating=5.0
    )
    
    # Process the video
    insights = processor.process_video(sample_video)
    
    # Save to knowledge vault structure
    vault_files = processor.save_insights_to_knowledge_vault(sample_video, insights)
    
    # Display results
    print("=== YouTube Video Processing Results ===")
    print(f"Video: {sample_video.title}")
    print(f"Channel: {sample_video.channel}")
    print(f"Relevance Score: {insights.relevance_score:.2f}")
    print(f"Key Takeaways: {len(insights.key_takeaways)}")
    print(f"Tools Mentioned: {len(insights.tools_mentioned)}")
    print(f"Code Examples: {len(insights.code_examples)}")
    
    return insights, vault_files

if __name__ == "__main__":
    # Run demonstration
    insights, files = demo_processing()
    
    print("\n=== System Ready for Integration ===")
    print("Next steps:")
    print("1. Integrate with MCP get_transcript tool")
    print("2. Set up knowledge vault file structure")
    print("3. Create automated processing workflow")
    print("4. Connect to Universal Topic Intelligence System")