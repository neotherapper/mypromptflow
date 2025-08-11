#!/usr/bin/env python3
"""
Channel Intelligence Reports Generator
Comprehensive analytics and insights for YouTube channel performance
"""

import json
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
import statistics

@dataclass
class ChannelMetrics:
    """Channel performance metrics"""
    channel_id: str
    channel_name: str
    total_videos: int
    analyzed_videos: int
    high_value_videos: int
    avg_importance_score: float
    avg_priority_topic_score: float
    total_views: int
    total_likes: int
    total_comments: int
    engagement_rate: float
    content_frequency: float  # videos per week
    quality_score: float  # overall channel quality
    trending_topics: List[str]
    last_updated: str

@dataclass
class ChannelInsight:
    """Channel insight or recommendation"""
    insight_type: str  # "strength", "opportunity", "trend", "recommendation"
    title: str
    description: str
    impact_level: str  # "high", "medium", "low"
    data_points: List[str]
    action_items: List[str]

class ChannelIntelligenceReports:
    """Generate comprehensive channel intelligence reports"""
    
    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = base_path or Path(__file__).parent
        self.data_path = self.base_path / "data"
        self.reports_path = self.base_path / "reports"
        self.reports_path.mkdir(parents=True, exist_ok=True)
        
        # Load channel configuration
        self.config_path = self.base_path / "config" / "youtube-rss-channels.json"
        self.channels_config = self._load_channels_config()
        
        print(f"📊 Channel Intelligence Reports initialized")
        print(f"   📺 Channels configured: {len(self.channels_config)}")
        print(f"   📁 Data path: {self.data_path}")
        print(f"   📋 Reports path: {self.reports_path}")
    
    def _load_channels_config(self) -> List[Dict[str, Any]]:
        """Load channels configuration"""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                return config.get('channels', [])
        except Exception as e:
            print(f"⚠️  Could not load channels config: {e}")
            return []
    
    def analyze_all_channels(self) -> Dict[str, Any]:
        """Generate comprehensive analysis for all channels"""
        
        print(f"🔍 Analyzing all {len(self.channels_config)} channels...")
        
        analysis_start = time.time()
        channel_metrics = []
        
        # Analyze each channel
        for channel_config in self.channels_config:
            channel_id = channel_config.get('id')
            try:
                metrics = self._analyze_single_channel(channel_id, channel_config)
                if metrics:
                    channel_metrics.append(metrics)
                    print(f"   ✅ {metrics.channel_name}: {metrics.total_videos} videos, {metrics.high_value_videos} high-value")
                else:
                    print(f"   ❌ {channel_id}: No data available")
                    
            except Exception as e:
                print(f"   ❌ {channel_id}: Analysis failed - {e}")
        
        analysis_time = time.time() - analysis_start
        
        # Generate aggregate insights
        aggregate_insights = self._generate_aggregate_insights(channel_metrics)
        
        # Generate individual channel insights
        channel_insights = {}
        for metrics in channel_metrics:
            insights = self._generate_channel_insights(metrics)
            channel_insights[metrics.channel_id] = [asdict(insight) for insight in insights]
        
        # Create comprehensive report
        report_data = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "analysis_time_seconds": round(analysis_time, 2),
            "total_channels_configured": len(self.channels_config),
            "channels_analyzed": len(channel_metrics),
            "channels_with_data": len([m for m in channel_metrics if m.total_videos > 0]),
            "aggregate_metrics": self._calculate_aggregate_metrics(channel_metrics),
            "aggregate_insights": [asdict(insight) for insight in aggregate_insights],
            "channel_metrics": [asdict(m) for m in channel_metrics],
            "channel_insights": channel_insights,
            "performance_rankings": self._generate_performance_rankings(channel_metrics),
            "trending_analysis": self._analyze_trending_topics(channel_metrics),
            "recommendations": self._generate_system_recommendations(channel_metrics)
        }
        
        print(f"📊 Analysis complete: {len(channel_metrics)} channels analyzed in {analysis_time:.2f}s")
        
        return report_data
    
    def _analyze_single_channel(self, channel_id: str, channel_config: Dict[str, Any]) -> Optional[ChannelMetrics]:
        """Analyze a single channel's performance"""
        
        channel_path = self.data_path / "channels" / channel_id
        catalog_file = channel_path / "videos_catalog.json"
        
        if not catalog_file.exists():
            return None
        
        try:
            with open(catalog_file, 'r') as f:
                catalog_data = json.load(f)
            
            videos = catalog_data.get('videos', [])
            if not videos:
                return None
            
            # Calculate basic metrics
            total_videos = len(videos)
            high_value_videos = len([v for v in videos if v.get('importance_score', 0) > 0.75])
            
            # Calculate scores
            importance_scores = [v.get('importance_score', 0) for v in videos]
            priority_scores = [v.get('priority_topic_score', 0) for v in videos]
            
            avg_importance = statistics.mean(importance_scores) if importance_scores else 0
            avg_priority = statistics.mean(priority_scores) if priority_scores else 0
            
            # Calculate engagement metrics
            total_views = sum(v.get('view_count', 0) or 0 for v in videos)
            total_likes = sum(v.get('like_count', 0) or 0 for v in videos)
            total_comments = sum(v.get('comment_count', 0) or 0 for v in videos)
            
            engagement_rate = (total_likes + total_comments) / max(total_views, 1) * 100
            
            # Calculate content frequency (videos per week)
            if videos:
                dates = []
                for video in videos:
                    pub_date = video.get('published_at')
                    if pub_date:
                        try:
                            date_obj = datetime.fromisoformat(pub_date.replace('Z', '+00:00'))
                            dates.append(date_obj)
                        except:
                            continue
                
                if len(dates) > 1:
                    dates.sort()
                    time_span = (dates[-1] - dates[0]).total_seconds() / (7 * 24 * 3600)  # weeks
                    content_frequency = len(dates) / max(time_span, 1)
                else:
                    content_frequency = 1.0
            else:
                content_frequency = 0.0
            
            # Calculate quality score (composite metric)
            quality_score = (
                avg_importance * 0.4 +
                (high_value_videos / max(total_videos, 1)) * 0.3 +
                min(engagement_rate / 10, 1.0) * 0.2 +
                min(content_frequency / 2, 1.0) * 0.1
            )
            
            # Extract trending topics
            trending_topics = self._extract_trending_topics(videos)
            
            return ChannelMetrics(
                channel_id=channel_id,
                channel_name=channel_config.get('name', channel_id),
                total_videos=total_videos,
                analyzed_videos=total_videos,
                high_value_videos=high_value_videos,
                avg_importance_score=round(avg_importance, 3),
                avg_priority_topic_score=round(avg_priority, 3),
                total_views=total_views,
                total_likes=total_likes,
                total_comments=total_comments,
                engagement_rate=round(engagement_rate, 3),
                content_frequency=round(content_frequency, 2),
                quality_score=round(quality_score, 3),
                trending_topics=trending_topics,
                last_updated=catalog_data.get('last_updated', '')
            )
            
        except Exception as e:
            print(f"Error analyzing channel {channel_id}: {e}")
            return None
    
    def _extract_trending_topics(self, videos: List[Dict[str, Any]]) -> List[str]:
        """Extract trending topics from video content"""
        
        # Simple keyword extraction from titles and descriptions
        keywords = {}
        tech_terms = [
            'ai', 'artificial intelligence', 'machine learning', 'claude', 'gpt',
            'react', 'javascript', 'typescript', 'python', 'nextjs', 'node',
            'api', 'database', 'docker', 'kubernetes', 'aws', 'cloud',
            'frontend', 'backend', 'fullstack', 'web development', 'mobile',
            'security', 'authentication', 'testing', 'devops', 'ci/cd'
        ]
        
        for video in videos:
            text = f"{video.get('title', '')} {video.get('description', '')}".lower()
            
            for term in tech_terms:
                if term in text:
                    keywords[term] = keywords.get(term, 0) + 1
        
        # Return top trending topics
        sorted_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)
        return [term for term, count in sorted_keywords[:5] if count > 1]
    
    def _calculate_aggregate_metrics(self, channel_metrics: List[ChannelMetrics]) -> Dict[str, Any]:
        """Calculate aggregate metrics across all channels"""
        
        if not channel_metrics:
            return {}
        
        total_videos = sum(m.total_videos for m in channel_metrics)
        total_high_value = sum(m.high_value_videos for m in channel_metrics)
        total_views = sum(m.total_views for m in channel_metrics)
        total_engagement = sum(m.total_likes + m.total_comments for m in channel_metrics)
        
        avg_importance = statistics.mean([m.avg_importance_score for m in channel_metrics])
        avg_quality = statistics.mean([m.quality_score for m in channel_metrics])
        avg_frequency = statistics.mean([m.content_frequency for m in channel_metrics])
        
        return {
            "total_videos_tracked": total_videos,
            "total_high_value_videos": total_high_value,
            "high_value_percentage": round((total_high_value / max(total_videos, 1)) * 100, 2),
            "total_views": total_views,
            "total_engagement": total_engagement,
            "average_importance_score": round(avg_importance, 3),
            "average_quality_score": round(avg_quality, 3),
            "average_content_frequency": round(avg_frequency, 2),
            "channels_with_high_value_content": len([m for m in channel_metrics if m.high_value_videos > 0]),
            "most_active_channel": max(channel_metrics, key=lambda x: x.content_frequency).channel_name if channel_metrics else None,
            "highest_quality_channel": max(channel_metrics, key=lambda x: x.quality_score).channel_name if channel_metrics else None
        }
    
    def _generate_aggregate_insights(self, channel_metrics: List[ChannelMetrics]) -> List[ChannelInsight]:
        """Generate insights across all channels"""
        
        insights = []
        
        if not channel_metrics:
            return insights
        
        # High-value content analysis
        high_value_channels = [m for m in channel_metrics if m.high_value_videos > 0]
        if high_value_channels:
            insight = ChannelInsight(
                insight_type="strength",
                title="High-Value Content Discovery",
                description=f"{len(high_value_channels)} channels producing high-value content",
                impact_level="high",
                data_points=[
                    f"Total high-value videos: {sum(m.high_value_videos for m in high_value_channels)}",
                    f"Top performer: {max(high_value_channels, key=lambda x: x.high_value_videos).channel_name}",
                    f"Average quality score: {statistics.mean([m.quality_score for m in high_value_channels]):.3f}"
                ],
                action_items=[
                    "Focus analysis resources on high-performing channels",
                    "Study content patterns from top performers",
                    "Increase monitoring frequency for quality channels"
                ]
            )
            insights.append(insight)
        
        # Content frequency analysis
        active_channels = [m for m in channel_metrics if m.content_frequency > 1.0]
        if active_channels:
            insight = ChannelInsight(
                insight_type="trend",
                title="High Content Frequency Channels",
                description=f"{len(active_channels)} channels with frequent content updates",
                impact_level="medium",
                data_points=[
                    f"Most active: {max(active_channels, key=lambda x: x.content_frequency).channel_name} ({max(m.content_frequency for m in active_channels):.1f} videos/week)",
                    f"Average frequency: {statistics.mean([m.content_frequency for m in active_channels]):.2f} videos/week"
                ],
                action_items=[
                    "Prioritize frequent publishers for real-time monitoring",
                    "Analyze correlation between frequency and quality"
                ]
            )
            insights.append(insight)
        
        # Engagement analysis
        if any(m.total_views > 0 for m in channel_metrics):
            high_engagement = [m for m in channel_metrics if m.engagement_rate > 5.0]
            if high_engagement:
                insight = ChannelInsight(
                    insight_type="opportunity",
                    title="High Engagement Channels",
                    description=f"{len(high_engagement)} channels with strong audience engagement",
                    impact_level="high",
                    data_points=[
                        f"Top engagement: {max(high_engagement, key=lambda x: x.engagement_rate).channel_name} ({max(m.engagement_rate for m in high_engagement):.2f}%)",
                        f"Total engagement events: {sum(m.total_likes + m.total_comments for m in high_engagement):,}"
                    ],
                    action_items=[
                        "Study engagement patterns for content optimization",
                        "Prioritize high-engagement content for transcript extraction"
                    ]
                )
                insights.append(insight)
        
        return insights
    
    def _generate_channel_insights(self, metrics: ChannelMetrics) -> List[ChannelInsight]:
        """Generate insights for a specific channel"""
        
        insights = []
        
        # Quality assessment
        if metrics.quality_score > 0.7:
            insights.append(ChannelInsight(
                insight_type="strength",
                title="High Quality Content Producer",
                description=f"Consistently produces high-quality content with {metrics.quality_score:.2f} quality score",
                impact_level="high",
                data_points=[
                    f"Quality score: {metrics.quality_score:.3f}",
                    f"High-value videos: {metrics.high_value_videos}/{metrics.total_videos}",
                    f"Average importance: {metrics.avg_importance_score:.3f}"
                ],
                action_items=[
                    "Enable transcript extraction for high-value videos",
                    "Increase monitoring frequency",
                    "Study content patterns for optimization"
                ]
            ))
        elif metrics.quality_score < 0.3:
            insights.append(ChannelInsight(
                insight_type="opportunity",
                title="Content Quality Improvement Needed",
                description=f"Below-average quality score suggests content optimization opportunities",
                impact_level="medium",
                data_points=[
                    f"Quality score: {metrics.quality_score:.3f}",
                    f"High-value content ratio: {(metrics.high_value_videos/max(metrics.total_videos,1)*100):.1f}%"
                ],
                action_items=[
                    "Review content filtering criteria",
                    "Analyze topic alignment with priorities",
                    "Consider reducing monitoring frequency"
                ]
            ))
        
        # Content frequency insights
        if metrics.content_frequency > 2.0:
            insights.append(ChannelInsight(
                insight_type="trend",
                title="High-Frequency Publisher",
                description=f"Very active content creation with {metrics.content_frequency:.1f} videos/week",
                impact_level="medium",
                data_points=[
                    f"Publishing frequency: {metrics.content_frequency:.2f} videos/week",
                    f"Total videos tracked: {metrics.total_videos}"
                ],
                action_items=[
                    "Enable real-time monitoring",
                    "Consider automated quality filtering",
                    "Monitor for content quality vs quantity trade-offs"
                ]
            ))
        
        # Trending topics insights
        if metrics.trending_topics:
            insights.append(ChannelInsight(
                insight_type="trend",
                title="Trending Topics Detected",
                description=f"Channel covers {len(metrics.trending_topics)} trending technical topics",
                impact_level="medium",
                data_points=[f"Trending: {', '.join(metrics.trending_topics[:3])}"],
                action_items=[
                    "Align with priority topic scoring",
                    "Monitor topic evolution over time"
                ]
            ))
        
        return insights
    
    def _generate_performance_rankings(self, channel_metrics: List[ChannelMetrics]) -> Dict[str, Any]:
        """Generate performance rankings"""
        
        if not channel_metrics:
            return {}
        
        # Sort by different criteria
        by_quality = sorted(channel_metrics, key=lambda x: x.quality_score, reverse=True)
        by_high_value = sorted(channel_metrics, key=lambda x: x.high_value_videos, reverse=True)
        by_engagement = sorted(channel_metrics, key=lambda x: x.engagement_rate, reverse=True)
        by_frequency = sorted(channel_metrics, key=lambda x: x.content_frequency, reverse=True)
        
        return {
            "top_quality_channels": [
                {"name": m.channel_name, "score": m.quality_score} 
                for m in by_quality[:5]
            ],
            "top_high_value_channels": [
                {"name": m.channel_name, "high_value_videos": m.high_value_videos, "total_videos": m.total_videos} 
                for m in by_high_value[:5]
            ],
            "top_engagement_channels": [
                {"name": m.channel_name, "engagement_rate": m.engagement_rate} 
                for m in by_engagement[:5] if m.engagement_rate > 0
            ],
            "most_active_channels": [
                {"name": m.channel_name, "frequency": m.content_frequency} 
                for m in by_frequency[:5]
            ]
        }
    
    def _analyze_trending_topics(self, channel_metrics: List[ChannelMetrics]) -> Dict[str, Any]:
        """Analyze trending topics across all channels"""
        
        topic_frequency = {}
        topic_channels = {}
        
        for metrics in channel_metrics:
            for topic in metrics.trending_topics:
                topic_frequency[topic] = topic_frequency.get(topic, 0) + 1
                if topic not in topic_channels:
                    topic_channels[topic] = []
                topic_channels[topic].append(metrics.channel_name)
        
        # Sort by frequency
        sorted_topics = sorted(topic_frequency.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "top_trending_topics": [
                {
                    "topic": topic,
                    "channel_count": count,
                    "channels": topic_channels[topic][:3]  # Top 3 channels
                }
                for topic, count in sorted_topics[:10]
            ],
            "total_unique_topics": len(topic_frequency),
            "average_topics_per_channel": round(sum(len(m.trending_topics) for m in channel_metrics) / len(channel_metrics), 2) if channel_metrics else 0
        }
    
    def _generate_system_recommendations(self, channel_metrics: List[ChannelMetrics]) -> List[Dict[str, Any]]:
        """Generate system-level recommendations"""
        
        recommendations = []
        
        if not channel_metrics:
            return recommendations
        
        # API utilization recommendation
        channels_with_data = len([m for m in channel_metrics if m.total_videos > 0])
        if channels_with_data < len(self.channels_config) * 0.5:
            recommendations.append({
                "priority": "high",
                "category": "data_collection",
                "title": "Improve Channel Data Coverage",
                "description": f"Only {channels_with_data}/{len(self.channels_config)} channels have analyzable data",
                "action_items": [
                    "Configure YouTube API key for comprehensive data collection",
                    "Run full channel analysis on all configured channels",
                    "Fix channel configuration issues causing data gaps"
                ],
                "impact": "Comprehensive intelligence requires data from all configured channels"
            })
        
        # Quality threshold optimization
        high_value_ratio = sum(m.high_value_videos for m in channel_metrics) / max(sum(m.total_videos for m in channel_metrics), 1)
        if high_value_ratio < 0.1:
            recommendations.append({
                "priority": "medium",
                "category": "quality_optimization",
                "title": "Optimize Quality Threshold Settings",
                "description": f"Only {high_value_ratio*100:.1f}% of content meets high-value criteria",
                "action_items": [
                    "Review and adjust importance scoring algorithm",
                    "Lower quality threshold for initial content collection",
                    "Enhance priority topic detection and weighting"
                ],
                "impact": "Better content discovery and utilization of available content"
            })
        
        # Transcript processing recommendation
        channels_with_engagement = [m for m in channel_metrics if m.total_views > 0]
        if channels_with_engagement:
            recommendations.append({
                "priority": "medium",
                "category": "content_analysis",
                "title": "Enable Transcript Processing",
                "description": "High-engagement content available for deeper analysis",
                "action_items": [
                    "Configure MCP transcript extraction tools",
                    "Enable transcript processing for high-value videos",
                    "Implement content analysis for better topic detection"
                ],
                "impact": "Deeper content insights and improved quality scoring"
            })
        
        return recommendations
    
    def generate_html_report(self, report_data: Dict[str, Any]) -> str:
        """Generate beautiful HTML report"""
        
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Channel Intelligence Report - {datetime.now().strftime('%Y-%m-%d')}</title>
    <link rel="stylesheet" href="/static/css/design-system.css">
    <style>
        /* Channel Intelligence Report specific overrides - using same styles as updated template */
        .insight {{
            padding: var(--spacing-lg);
            border-radius: var(--radius-lg);
            margin: var(--spacing-lg) 0;
            border-left: 4px solid var(--primary-gradient);
            background: var(--glass-light);
            backdrop-filter: blur(10px);
        }}
        
        .insight.strength {{
            border-left: 4px solid var(--status-active);
            background: rgba(34, 197, 94, 0.1);
        }}
        
        .insight.opportunity {{
            border-left: 4px solid var(--status-inactive);
            background: rgba(245, 158, 11, 0.1);
        }}
        
        .insight.trend {{
            border-left: 4px solid #8b5cf6;
            background: rgba(139, 92, 246, 0.1);
        }}
        
        .stat-number {{
            font-size: var(--text-4xl);
            font-weight: var(--font-weight-bold);
            background: var(--primary-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin: 0;
        }}
        
        .stat-label {{
            color: var(--text-muted);
            font-size: var(--text-sm);
            margin-top: var(--spacing-xs);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: var(--font-weight-medium);
        }}
    </style>
</head>
<body>
    <div class="animated-bg"></div>
    
    <div class="container">
        <!-- Header -->
        <header class="glass-card text-center mb-xl">
            <h1 class="heading-1">📊 Channel Intelligence Report</h1>
            <p class="text-body mb-lg">Comprehensive YouTube Channel Analysis & Insights</p>
            <p class="text-small text-muted">Generated on <span data-timestamp="{datetime.now().isoformat()}Z" data-format="display">{datetime.now().strftime('%B %d, %Y at %H:%M UTC')}</span></p>
        </header>
        </div>
        
        <div class="stats-grid">"""
        
        # Add aggregate statistics
        agg_metrics = report_data.get('aggregate_metrics', {})
        stats = [
            ("Total Videos", f"{agg_metrics.get('total_videos_tracked', 0):,}"),
            ("High-Value Videos", f"{agg_metrics.get('total_high_value_videos', 0):,}"),
            ("Channels Analyzed", f"{report_data.get('channels_analyzed', 0)}/{report_data.get('total_channels_configured', 0)}"),
            ("Average Quality", f"{agg_metrics.get('average_quality_score', 0):.3f}"),
            ("Total Views", f"{agg_metrics.get('total_views', 0):,}"),
            ("High-Value Rate", f"{agg_metrics.get('high_value_percentage', 0):.1f}%")
        ]
        
        for label, value in stats:
            html_content += f"""
            <div class="stat-card">
                <div class="stat-number">{value}</div>
                <div class="stat-label">{label}</div>
            </div>"""
        
        html_content += """
        </div>
        
        <!-- Key Insights Section -->
        <section class="glass-card mb-xl">
            <h2 class="heading-2 mb-lg">🔍 Key Insights</h2>"""
        
        # Add aggregate insights
        for insight in report_data.get('aggregate_insights', []):
            html_content += f"""
            <div class="insight {insight['insight_type']}">
                <h3>{insight['title']}</h3>
                <p>{insight['description']}</p>
                <ul class="data-points">"""
            for point in insight['data_points']:
                html_content += f"<li>{point}</li>"
            html_content += "</ul></div>"
        
        html_content += """
        </section>
        
        <!-- Performance Rankings Section -->
        <section class="glass-card mb-xl">
            <h2 class="heading-2 mb-lg">🏆 Performance Rankings</h2>"""
        
        # Add performance rankings
        rankings = report_data.get('performance_rankings', {})
        
        ranking_sections = [
            ("top_quality_channels", "📈 Top Quality Channels", "score"),
            ("top_high_value_channels", "⭐ High-Value Content Leaders", "high_value_videos"),
            ("top_engagement_channels", "💬 Top Engagement", "engagement_rate"),
            ("most_active_channels", "🚀 Most Active Publishers", "frequency")
        ]
        
        for key, title, metric in ranking_sections:
            if key in rankings and rankings[key]:
                html_content += f"""
                <h3 class="heading-3 mb-md">{title}</h3>
                <ol class="ranking-list mb-lg">"""
                
                for i, item in enumerate(rankings[key][:5], 1):
                    value = item.get(metric, 0)
                    if isinstance(value, float):
                        value = f"{value:.3f}"
                    html_content += f"""
                    <li class="ranking-item">
                        <div class="flex gap-md">
                            <span class="rank">{i}</span>
                            <span class="text-body font-weight-medium">{item['name']}</span>
                        </div>
                        <span class="text-body font-weight-semibold">{value}</span>
                    </li>"""
                
                html_content += "</ol>"
        
        html_content += """
        </section>
        
        <!-- System Recommendations Section -->
        <section class="glass-card mb-xl">
            <h2 class="heading-2 mb-lg">🎯 System Recommendations</h2>"""
        
        # Add recommendations
        for rec in report_data.get('recommendations', []):
            html_content += f"""
            <div class="recommendation {rec['priority']}">
                <h4>{rec['title']}</h4>
                <p>{rec['description']}</p>
                <p><strong>Impact:</strong> {rec['impact']}</p>
                <p><strong>Action Items:</strong></p>
                <ul>"""
            for action in rec['action_items']:
                html_content += f"<li>{action}</li>"
            html_content += "</ul></div>"
        
        html_content += f"""
        </section>
        
        <div class="text-center mt-xl">
            <p class="text-small text-muted">
                Report generated in {report_data.get('analysis_time_seconds', 0):.2f} seconds | Unified Intelligence System
            </p>
        </div>
    </div>
    
    <script src="/static/js/time-formatter.js"></script>
</body>
</html>"""
        
        return html_content
    
    def generate_reports(self) -> Dict[str, str]:
        """Generate all intelligence reports"""
        
        print(f"📋 Generating Channel Intelligence Reports...")
        
        # Generate comprehensive analysis
        report_data = self.analyze_all_channels()
        
        # Generate reports
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        
        # Save JSON report
        json_file = self.reports_path / f"channel_intelligence_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        # Generate and save HTML report
        html_content = self.generate_html_report(report_data)
        html_file = self.reports_path / f"channel_intelligence_{timestamp}.html"
        with open(html_file, 'w') as f:
            f.write(html_content)
        
        # Create latest symlinks
        latest_json = self.reports_path / "latest_intelligence_report.json"
        latest_html = self.reports_path / "latest_intelligence_report.html"
        
        # Remove existing symlinks and create new ones
        for latest_file, source_file in [(latest_json, json_file), (latest_html, html_file)]:
            if latest_file.exists():
                latest_file.unlink()
            try:
                latest_file.symlink_to(source_file.name)
            except:
                # Fallback: copy file if symlink fails
                import shutil
                shutil.copy2(source_file, latest_file)
        
        print(f"✅ Reports generated successfully:")
        print(f"   📊 JSON Report: {json_file}")
        print(f"   🌐 HTML Report: {html_file}")
        print(f"   🔗 Latest HTML: {latest_html}")
        
        return {
            "json_file": str(json_file),
            "html_file": str(html_file),
            "latest_html": str(latest_html),
            "report_data": report_data
        }

def main():
    """Generate channel intelligence reports"""
    
    print("📊 Channel Intelligence Reports Generator")
    print("=" * 60)
    
    # Initialize reporter
    reporter = ChannelIntelligenceReports()
    
    # Generate reports
    results = reporter.generate_reports()
    
    # Open HTML report in browser
    html_file = results["latest_html"]
    if Path(html_file).exists():
        try:
            import webbrowser
            webbrowser.open(f"file://{Path(html_file).absolute()}")
            print(f"🌐 Report opened in browser: {html_file}")
        except:
            print(f"📄 Report available at: {html_file}")
    
    return results

if __name__ == "__main__":
    main()