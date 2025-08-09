#!/usr/bin/env python3
"""
Comprehensive YouTube Processing Report Generator
Analyzes all processed priority YouTube videos and generates detailed reports
"""

import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime, timezone

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_comprehensive_report():
    """Generate comprehensive report for all processed YouTube videos"""
    
    # Path to processed videos
    knowledge_vault_path = Path(__file__).parent.parent.parent / "knowledge-vault" / "databases" / "knowledge_vault" / "content-intelligence" / "priority-youtube"
    process_date = datetime.now().strftime('%Y-%m-%d')
    save_dir = knowledge_vault_path / process_date
    
    if not save_dir.exists():
        print(f"❌ No processed videos found in {save_dir}")
        return
    
    # Find all processed intelligence files
    processed_videos = []
    intelligence_files = list(save_dir.glob("*_unified_intelligence.json"))
    
    print(f"🔍 Found {len(intelligence_files)} processed videos")
    
    for file in intelligence_files:
        try:
            with open(file, 'r') as f:
                data = json.load(f)
                processed_videos.append(data)
        except Exception as e:
            logger.warning(f"Could not load {file}: {e}")
    
    if not processed_videos:
        print("❌ No valid processed video data found")
        return
    
    # Sort videos by quality score
    processed_videos.sort(key=lambda x: x.get('quality_score', 0), reverse=True)
    
    # Generate comprehensive analysis
    report = {
        'processing_summary': {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'total_videos_processed': len(processed_videos),
            'processing_date': process_date,
            'average_unified_score': round(sum(v.get('unified_score', 0) for v in processed_videos) / len(processed_videos), 3),
            'average_quality_score': round(sum(v.get('quality_score', 0) for v in processed_videos) / len(processed_videos), 3),
            'high_quality_videos': len([v for v in processed_videos if v.get('quality_score', 0) > 0.9]),
            'exceptional_videos': len([v for v in processed_videos if v.get('quality_score', 0) >= 1.0]),
            'processor_framework_version': 'unified-intelligence-1.2.0'
        },
        'videos_analyzed': [],
        'topic_analysis': {
            'priority_topics_discovered': {},
            'unique_topics': set(),
            'topic_distribution': {},
            'cross_video_topics': {}
        },
        'concept_analysis': {
            'top_programming_concepts': {},
            'unique_concepts_discovered': set(),
            'concept_frequency_across_videos': {}
        },
        'content_quality_metrics': {
            'videos_with_code_examples': 0,
            'videos_with_practical_demos': 0,
            'comprehensive_tutorials': 0,
            'beginner_friendly_content': 0,
            'industry_relevant_content': 0,
            'project_based_tutorials': 0,
            'comparison_analyses': 0
        },
        'platform_insights': {
            'channels_analyzed': set(),
            'content_types': {},
            'estimated_total_duration': '0 hours',
            'total_transcript_length': 0
        }
    }
    
    # Analyze each video
    total_duration_minutes = 0
    for video in processed_videos:
        # Basic video info
        video_summary = {
            'title': video.get('title', 'Unknown'),
            'channel': video.get('channel', 'Unknown'),
            'video_url': video.get('video_url', ''),
            'video_id': video.get('video_id', ''),
            'unified_score': video.get('unified_score', 0),
            'quality_score': video.get('quality_score', 0),
            'priority_topics': video.get('priority_topics', []),
            'concept_count': len(video.get('programming_concepts', [])),
            'transcript_length': video.get('insights', {}).get('transcript_length', 0),
            'tutorial_type': video.get('tutorial_type', 'standard'),
            'comprehensive_rating': video.get('comprehensive_rating', 'medium'),
            'processing_timestamp': video.get('processing_timestamp', ''),
            'high_value_indicators': video.get('high_value_indicators', {})
        }
        
        # Extract duration if available
        duration = video.get('estimated_duration', '')
        if 'h' in duration:
            try:
                hours = float(duration.split('h')[0].strip())
                total_duration_minutes += hours * 60
                if 'm' in duration:
                    minutes = float(duration.split('h')[1].split('m')[0].strip())
                    total_duration_minutes += minutes
            except:
                pass
        elif 'm' in duration:
            try:
                minutes = float(duration.split('m')[0].strip())
                total_duration_minutes += minutes
            except:
                pass
        
        report['videos_analyzed'].append(video_summary)
        
        # Topic analysis
        for topic in video.get('priority_topics', []):
            report['topic_analysis']['unique_topics'].add(topic)
            if topic not in report['topic_analysis']['priority_topics_discovered']:
                report['topic_analysis']['priority_topics_discovered'][topic] = []
            report['topic_analysis']['priority_topics_discovered'][topic].append({
                'video_id': video.get('video_id', ''),
                'title': video.get('title', ''),
                'score': video.get('topic_scores', {}).get(topic, 0)
            })
            
            # Topic distribution
            report['topic_analysis']['topic_distribution'][topic] = report['topic_analysis']['topic_distribution'].get(topic, 0) + 1
        
        # Concept analysis
        for concept in video.get('programming_concepts', []):
            report['concept_analysis']['unique_concepts_discovered'].add(concept)
            report['concept_analysis']['concept_frequency_across_videos'][concept] = report['concept_analysis']['concept_frequency_across_videos'].get(concept, 0) + 1
        
        # Quality metrics
        content_quality = video.get('insights', {}).get('content_quality_indicators', {})
        learning_value = video.get('insights', {}).get('learning_value_indicators', {})
        
        if content_quality.get('has_code_examples'):
            report['content_quality_metrics']['videos_with_code_examples'] += 1
        if content_quality.get('has_practical_demo'):
            report['content_quality_metrics']['videos_with_practical_demos'] += 1
        if learning_value.get('comprehensive_coverage'):
            report['content_quality_metrics']['comprehensive_tutorials'] += 1
        if learning_value.get('beginner_friendly'):
            report['content_quality_metrics']['beginner_friendly_content'] += 1
        if learning_value.get('industry_relevant'):
            report['content_quality_metrics']['industry_relevant_content'] += 1
        if content_quality.get('has_project_based'):
            report['content_quality_metrics']['project_based_tutorials'] += 1
        if content_quality.get('has_comparison_analysis'):
            report['content_quality_metrics']['comparison_analyses'] += 1
        
        # Platform insights
        report['platform_insights']['channels_analyzed'].add(video.get('channel', 'Unknown'))
        content_type = video.get('tutorial_type', 'standard')
        report['platform_insights']['content_types'][content_type] = report['platform_insights']['content_types'].get(content_type, 0) + 1
        report['platform_insights']['total_transcript_length'] += video.get('insights', {}).get('transcript_length', 0)
    
    # Convert sets to lists for JSON serialization
    report['topic_analysis']['unique_topics'] = sorted(list(report['topic_analysis']['unique_topics']))
    report['concept_analysis']['unique_concepts_discovered'] = sorted(list(report['concept_analysis']['unique_concepts_discovered']))
    report['platform_insights']['channels_analyzed'] = sorted(list(report['platform_insights']['channels_analyzed']))
    
    # Calculate duration
    hours = int(total_duration_minutes // 60)
    minutes = int(total_duration_minutes % 60)
    report['platform_insights']['estimated_total_duration'] = f"{hours}h {minutes}m"
    
    # Sort concepts by frequency
    sorted_concepts = sorted(report['concept_analysis']['concept_frequency_across_videos'].items(), 
                           key=lambda x: x[1], reverse=True)[:20]
    report['concept_analysis']['top_programming_concepts'] = dict(sorted_concepts)
    
    # Cross-video topic analysis
    for topic, videos in report['topic_analysis']['priority_topics_discovered'].items():
        if len(videos) > 1:
            report['topic_analysis']['cross_video_topics'][topic] = {
                'video_count': len(videos),
                'average_score': round(sum(v['score'] for v in videos) / len(videos), 3),
                'videos': [{'id': v['video_id'], 'title': v['title'][:50] + '...' if len(v['title']) > 50 else v['title']} for v in videos]
            }
    
    # Save comprehensive report
    report_file = save_dir / f"comprehensive_processing_report_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    # Generate summary report
    summary_file = save_dir / f"processing_summary_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.md"
    with open(summary_file, 'w') as f:
        f.write(f"# YouTube Video Processing Report\\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n")
        
        f.write(f"## Processing Summary\\n\\n")
        f.write(f"- **Total Videos Processed:** {report['processing_summary']['total_videos_processed']}\\n")
        f.write(f"- **Average Unified Score:** {report['processing_summary']['average_unified_score']}\\n")
        f.write(f"- **Average Quality Score:** {report['processing_summary']['average_quality_score']}\\n")
        f.write(f"- **High Quality Videos (>0.9):** {report['processing_summary']['high_quality_videos']}\\n")
        f.write(f"- **Perfect Quality Videos (1.0):** {report['processing_summary']['exceptional_videos']}\\n")
        f.write(f"- **Estimated Total Duration:** {report['platform_insights']['estimated_total_duration']}\\n")
        f.write(f"- **Total Transcript Length:** {report['platform_insights']['total_transcript_length']:,} characters\\n\\n")
        
        f.write(f"## Videos Processed\\n\\n")
        for i, video in enumerate(report['videos_analyzed'], 1):
            f.write(f"### {i}. {video['title']}\\n")
            f.write(f"- **Channel:** {video['channel']}\\n")
            f.write(f"- **Quality Score:** {video['quality_score']:.3f}\\n")
            f.write(f"- **Priority Topics:** {', '.join(video['priority_topics'])}\\n")
            f.write(f"- **Programming Concepts:** {video['concept_count']}\\n")
            f.write(f"- **Type:** {video['tutorial_type'].replace('_', ' ').title()}\\n")
            f.write(f"- **URL:** {video['video_url']}\\n\\n")
        
        f.write(f"## Topic Analysis\\n\\n")
        f.write(f"- **Unique Topics Discovered:** {len(report['topic_analysis']['unique_topics'])}\\n")
        f.write(f"- **Topics:** {', '.join(report['topic_analysis']['unique_topics'])}\\n\\n")
        
        if report['topic_analysis']['cross_video_topics']:
            f.write(f"### Cross-Video Topics\\n\\n")
            for topic, data in report['topic_analysis']['cross_video_topics'].items():
                f.write(f"- **{topic}:** {data['video_count']} videos (avg score: {data['average_score']})\\n")
        
        f.write(f"\\n## Programming Concepts\\n\\n")
        f.write(f"- **Unique Concepts:** {len(report['concept_analysis']['unique_concepts_discovered'])}\\n")
        f.write(f"- **Top Concepts:**\\n")
        for concept, count in list(report['concept_analysis']['top_programming_concepts'].items())[:10]:
            f.write(f"  - {concept}: {count} videos\\n")
        
        f.write(f"\\n## Content Quality Metrics\\n\\n")
        metrics = report['content_quality_metrics']
        f.write(f"- **Videos with Code Examples:** {metrics['videos_with_code_examples']}\\n")
        f.write(f"- **Videos with Practical Demos:** {metrics['videos_with_practical_demos']}\\n")
        f.write(f"- **Comprehensive Tutorials:** {metrics['comprehensive_tutorials']}\\n")
        f.write(f"- **Beginner-Friendly Content:** {metrics['beginner_friendly_content']}\\n")
        f.write(f"- **Industry-Relevant Content:** {metrics['industry_relevant_content']}\\n")
        f.write(f"- **Project-Based Tutorials:** {metrics['project_based_tutorials']}\\n")
        f.write(f"- **Comparison Analyses:** {metrics['comparison_analyses']}\\n")
        
        f.write(f"\\n## Platform Insights\\n\\n")
        f.write(f"- **Channels Analyzed:** {len(report['platform_insights']['channels_analyzed'])}\\n")
        for channel in report['platform_insights']['channels_analyzed']:
            f.write(f"  - {channel}\\n")
        
        f.write(f"\\n- **Content Types:**\\n")
        for content_type, count in report['platform_insights']['content_types'].items():
            f.write(f"  - {content_type.replace('_', ' ').title()}: {count}\\n")
    
    # Display results
    print("📊 Comprehensive YouTube Processing Report Generated!")
    print("=" * 80)
    print(f"📈 Processing Summary:")
    print(f"   Total Videos Processed: {report['processing_summary']['total_videos_processed']}")
    print(f"   Average Unified Score: {report['processing_summary']['average_unified_score']}")
    print(f"   Average Quality Score: {report['processing_summary']['average_quality_score']}")
    print(f"   High Quality Videos (>0.9): {report['processing_summary']['high_quality_videos']}")
    print(f"   Perfect Quality Videos (1.0): {report['processing_summary']['exceptional_videos']}")
    print(f"   Estimated Total Duration: {report['platform_insights']['estimated_total_duration']}")
    print()
    
    print("🎯 Topic Analysis:")
    print(f"   Unique Topics: {len(report['topic_analysis']['unique_topics'])}")
    print(f"   Topics: {', '.join(report['topic_analysis']['unique_topics'])}")
    print()
    
    print("💻 Programming Concepts:")
    print(f"   Unique Concepts: {len(report['concept_analysis']['unique_concepts_discovered'])}")
    print(f"   Top 5 Concepts:")
    for concept, count in list(report['concept_analysis']['top_programming_concepts'].items())[:5]:
        print(f"     - {concept}: {count} videos")
    print()
    
    print("📺 Platform Insights:")
    print(f"   Channels Analyzed: {len(report['platform_insights']['channels_analyzed'])}")
    print(f"   Content Types: {len(report['platform_insights']['content_types'])}")
    print(f"   Total Transcript Length: {report['platform_insights']['total_transcript_length']:,} characters")
    print()
    
    print("✅ Quality Metrics:")
    metrics = report['content_quality_metrics']
    print(f"   Videos with Code Examples: {metrics['videos_with_code_examples']}")
    print(f"   Videos with Practical Demos: {metrics['videos_with_practical_demos']}")
    print(f"   Comprehensive Tutorials: {metrics['comprehensive_tutorials']}")
    print(f"   Project-Based Tutorials: {metrics['project_based_tutorials']}")
    print()
    
    print("🏆 Report Files Generated:")
    print(f"   Comprehensive Report: {report_file.name}")
    print(f"   Summary Report: {summary_file.name}")
    print(f"   Saved to: {save_dir}")
    print()
    print("✅ All processed videos are ready for daily digest inclusion!")

if __name__ == "__main__":
    generate_comprehensive_report()