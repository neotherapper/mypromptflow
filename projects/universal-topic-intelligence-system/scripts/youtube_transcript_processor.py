#!/usr/bin/env python3
"""
YouTube Transcript Processor
Processes YouTube video transcripts for insights and educational content analysis
"""

import re
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ProcessedInsights:
    """Container for processed transcript insights"""
    summary: str
    key_points: List[str]
    programming_concepts: List[str]
    tools_mentioned: List[str]
    learning_outcomes: List[str]
    relevance_score: float
    content_type: str
    difficulty_level: str
    estimated_duration: str


class YouTubeTranscriptProcessor:
    """Process YouTube transcripts for educational content analysis"""
    
    def __init__(self):
        # Programming-related keywords for relevance scoring
        self.programming_keywords = {
            'languages': ['python', 'javascript', 'typescript', 'java', 'c++', 'rust', 'go', 'swift', 
                         'kotlin', 'php', 'ruby', 'scala', 'haskell', 'clojure', 'elixir'],
            'frameworks': ['react', 'vue', 'angular', 'django', 'flask', 'spring', 'rails', 'express',
                          'next.js', 'nuxt', 'gatsby', 'svelte', 'solid', 'astro'],
            'tools': ['git', 'docker', 'kubernetes', 'jenkins', 'github', 'gitlab', 'aws', 'azure',
                     'gcp', 'terraform', 'ansible', 'vim', 'vscode', 'intellij'],
            'concepts': ['algorithm', 'data structure', 'design pattern', 'architecture', 'testing',
                        'debugging', 'optimization', 'refactoring', 'deployment', 'ci/cd', 'api', 'database']
        }
        
        # Educational content patterns
        self.educational_patterns = [
            r'tutorial', r'how to', r'guide', r'learn', r'teach', r'explain', r'understand',
            r'beginner', r'advanced', r'course', r'lesson', r'example', r'demonstration'
        ]
        
        # Content type classifiers
        self.content_types = {
            'tutorial': ['tutorial', 'how to', 'step by step', 'guide', 'walkthrough'],
            'review': ['review', 'comparison', 'vs', 'versus', 'opinion', 'thoughts on'],
            'discussion': ['discussion', 'talk', 'interview', 'conversation', 'debate'],
            'live-coding': ['live coding', 'coding session', 'build', 'create', 'develop'],
            'news': ['news', 'update', 'announcement', 'release', 'new version']
        }

    def process_transcript(self, transcript: str, metadata: Dict) -> ProcessedInsights:
        """Process a transcript and extract educational insights"""
        
        # Clean and normalize transcript
        cleaned_transcript = self._clean_transcript(transcript)
        
        # Extract key information
        summary = self._generate_summary(cleaned_transcript)
        key_points = self._extract_key_points(cleaned_transcript)
        programming_concepts = self._identify_programming_concepts(cleaned_transcript)
        tools_mentioned = self._extract_tools_mentioned(cleaned_transcript)
        learning_outcomes = self._extract_learning_outcomes(cleaned_transcript)
        
        # Calculate relevance score
        relevance_score = self._calculate_relevance_score(cleaned_transcript, metadata)
        
        # Classify content type
        content_type = self._classify_content_type(cleaned_transcript, metadata)
        
        # Determine difficulty level
        difficulty_level = self._assess_difficulty_level(cleaned_transcript, programming_concepts)
        
        # Estimate duration for learning
        estimated_duration = self._estimate_learning_duration(cleaned_transcript, content_type)
        
        return ProcessedInsights(
            summary=summary,
            key_points=key_points,
            programming_concepts=programming_concepts,
            tools_mentioned=tools_mentioned,
            learning_outcomes=learning_outcomes,
            relevance_score=relevance_score,
            content_type=content_type,
            difficulty_level=difficulty_level,
            estimated_duration=estimated_duration
        )

    def _clean_transcript(self, transcript: str) -> str:
        """Clean and normalize transcript text"""
        # Remove timestamp markers
        cleaned = re.sub(r'\d{1,2}:\d{2}:\d{2}', '', transcript)
        
        # Remove speaker labels
        cleaned = re.sub(r'^[A-Za-z]+:', '', cleaned, flags=re.MULTILINE)
        
        # Remove excessive whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned)
        
        # Remove common filler words and sounds
        fillers = ['um', 'uh', 'ah', 'like', 'you know', 'so', 'basically', 'actually']
        for filler in fillers:
            cleaned = re.sub(rf'\b{filler}\b', '', cleaned, flags=re.IGNORECASE)
        
        return cleaned.strip()

    def _generate_summary(self, transcript: str) -> str:
        """Generate a concise summary of the transcript"""
        # Simple extractive summarization - take first meaningful sentences
        sentences = re.split(r'[.!?]+', transcript)
        meaningful_sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
        
        # Take up to 3 sentences for summary
        summary_sentences = meaningful_sentences[:3]
        return '. '.join(summary_sentences) + '.' if summary_sentences else "No meaningful content found."

    def _extract_key_points(self, transcript: str) -> List[str]:
        """Extract key points from the transcript"""
        key_points = []
        
        # Look for enumerated points
        enumeration_patterns = [
            r'first[ly]?[,:]?\s+(.{20,100}?)[\.\n]',
            r'second[ly]?[,:]?\s+(.{20,100}?)[\.\n]',
            r'third[ly]?[,:]?\s+(.{20,100}?)[\.\n]',
            r'number \d+[,:]?\s+(.{20,100}?)[\.\n]',
            r'\d+[.\)]\s+(.{20,100}?)[\.\n]'
        ]
        
        for pattern in enumeration_patterns:
            matches = re.findall(pattern, transcript, re.IGNORECASE)
            key_points.extend([match.strip() for match in matches])
        
        # Look for emphatic statements
        emphatic_patterns = [
            r'important[ly]?[,:]?\s+(.{20,100}?)[\.\n]',
            r'key point[,:]?\s+(.{20,100}?)[\.\n]',
            r'remember[,:]?\s+(.{20,100}?)[\.\n]',
            r'crucial[ly]?[,:]?\s+(.{20,100}?)[\.\n]'
        ]
        
        for pattern in emphatic_patterns:
            matches = re.findall(pattern, transcript, re.IGNORECASE)
            key_points.extend([match.strip() for match in matches])
        
        return key_points[:5]  # Limit to top 5 key points

    def _identify_programming_concepts(self, transcript: str) -> List[str]:
        """Identify programming concepts mentioned in the transcript"""
        concepts_found = []
        transcript_lower = transcript.lower()
        
        for category, keywords in self.programming_keywords.items():
            for keyword in keywords:
                if keyword in transcript_lower:
                    concepts_found.append(keyword)
        
        return list(set(concepts_found))  # Remove duplicates

    def _extract_tools_mentioned(self, transcript: str) -> List[str]:
        """Extract development tools and technologies mentioned"""
        tools_found = []
        transcript_lower = transcript.lower()
        
        # Use the tools from programming_keywords
        for tool in self.programming_keywords['tools']:
            if tool in transcript_lower:
                tools_found.append(tool)
        
        # Additional tool patterns
        tool_patterns = [
            r'using\s+(\w+)',
            r'with\s+(\w+)\s+(?:framework|library|tool)',
            r'(\w+)\s+(?:framework|library|tool)',
        ]
        
        for pattern in tool_patterns:
            matches = re.findall(pattern, transcript, re.IGNORECASE)
            tools_found.extend(matches)
        
        return list(set(tools_found))[:10]  # Limit to top 10 tools

    def _extract_learning_outcomes(self, transcript: str) -> List[str]:
        """Extract potential learning outcomes from the content"""
        outcomes = []
        
        # Look for outcome-indicating phrases
        outcome_patterns = [
            r'you(?:\'ll| will) learn\s+(.{20,100}?)[\.\n]',
            r'this (?:will|teaches?)\s+(.{20,100}?)[\.\n]',
            r'by the end[,:]?\s+(.{20,100}?)[\.\n]',
            r'after (?:watching|this)[,:]?\s+(.{20,100}?)[\.\n]'
        ]
        
        for pattern in outcome_patterns:
            matches = re.findall(pattern, transcript, re.IGNORECASE)
            outcomes.extend([match.strip() for match in matches])
        
        return outcomes[:3]  # Limit to top 3 learning outcomes

    def _calculate_relevance_score(self, transcript: str, metadata: Dict) -> float:
        """Calculate relevance score for programming/development content"""
        score = 0.0
        transcript_lower = transcript.lower()
        total_words = len(transcript.split())
        
        # Programming keyword density
        programming_word_count = 0
        for category, keywords in self.programming_keywords.items():
            for keyword in keywords:
                programming_word_count += transcript_lower.count(keyword)
        
        # Base score from programming keyword density
        if total_words > 0:
            keyword_density = programming_word_count / total_words
            score += min(keyword_density * 10, 0.4)  # Max 0.4 from keywords
        
        # Educational content indicators
        educational_matches = 0
        for pattern in self.educational_patterns:
            educational_matches += len(re.findall(pattern, transcript_lower))
        
        score += min(educational_matches * 0.05, 0.3)  # Max 0.3 from educational content
        
        # Channel reputation (from metadata)
        channel_rating = metadata.get('rating', 3.0)
        score += (channel_rating / 5.0) * 0.2  # Max 0.2 from channel rating
        
        # Length appropriateness (not too short, not too long)
        if 300 <= total_words <= 3000:  # Ideal length range
            score += 0.1
        
        return min(score, 1.0)  # Cap at 1.0

    def _classify_content_type(self, transcript: str, metadata: Dict) -> str:
        """Classify the type of educational content"""
        transcript_lower = transcript.lower()
        title_lower = metadata.get('title', '').lower()
        
        # Check each content type
        for content_type, indicators in self.content_types.items():
            for indicator in indicators:
                if indicator in transcript_lower or indicator in title_lower:
                    return content_type
        
        return 'general'  # Default classification

    def _assess_difficulty_level(self, transcript: str, concepts: List[str]) -> str:
        """Assess the difficulty level of the content"""
        # Simple heuristic based on concept complexity and language used
        advanced_indicators = ['advanced', 'complex', 'sophisticated', 'enterprise', 'production', 'scalable']
        beginner_indicators = ['beginner', 'basic', 'simple', 'intro', 'getting started', 'first time']
        
        transcript_lower = transcript.lower()
        
        advanced_count = sum(1 for indicator in advanced_indicators if indicator in transcript_lower)
        beginner_count = sum(1 for indicator in beginner_indicators if indicator in transcript_lower)
        
        # Factor in number of programming concepts
        concept_complexity = len(concepts)
        
        if beginner_count > advanced_count and concept_complexity < 5:
            return 'beginner'
        elif advanced_count > beginner_count or concept_complexity > 10:
            return 'advanced'
        else:
            return 'intermediate'

    def _estimate_learning_duration(self, transcript: str, content_type: str) -> str:
        """Estimate time needed to learn/implement the content"""
        word_count = len(transcript.split())
        
        # Base time estimates by content type
        base_times = {
            'tutorial': 30,  # minutes
            'review': 15,
            'discussion': 20,
            'live-coding': 60,
            'news': 10,
            'general': 20
        }
        
        base_time = base_times.get(content_type, 20)
        
        # Adjust based on content length
        if word_count > 2000:
            base_time *= 1.5
        elif word_count < 500:
            base_time *= 0.7
        
        if base_time < 15:
            return "< 15 minutes"
        elif base_time < 30:
            return "15-30 minutes"
        elif base_time < 60:
            return "30-60 minutes"
        else:
            return "1+ hours"


def process_transcript_file(transcript_path: str, metadata_path: str) -> Dict:
    """Process a transcript file and return insights"""
    try:
        # Load transcript
        with open(transcript_path, 'r', encoding='utf-8') as f:
            transcript_content = f.read()
        
        # Load metadata
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        # Process transcript
        processor = YouTubeTranscriptProcessor()
        insights = processor.process_transcript(transcript_content, metadata)
        
        # Convert to dictionary for JSON serialization
        return {
            'summary': insights.summary,
            'key_points': insights.key_points,
            'programming_concepts': insights.programming_concepts,
            'tools_mentioned': insights.tools_mentioned,
            'learning_outcomes': insights.learning_outcomes,
            'relevance_score': insights.relevance_score,
            'content_type': insights.content_type,
            'difficulty_level': insights.difficulty_level,
            'estimated_duration': insights.estimated_duration,
            'processed_at': datetime.now().isoformat()
        }
        
    except Exception as e:
        return {
            'error': str(e),
            'processed_at': datetime.now().isoformat()
        }


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 3:
        print("Usage: python youtube_transcript_processor.py <transcript_file> <metadata_file>")
        sys.exit(1)
    
    transcript_file = sys.argv[1]
    metadata_file = sys.argv[2]
    
    result = process_transcript_file(transcript_file, metadata_file)
    print(json.dumps(result, indent=2))