#!/usr/bin/env python3
"""
Trend Analysis and Recommendations System
Advanced analytics for YouTube channel trend detection and strategic recommendations
"""

import json
import time
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
import statistics
from collections import defaultdict

@dataclass
class TrendMetric:
    """Trend analysis metric"""
    metric_name: str
    current_value: float
    previous_value: float
    change_percentage: float
    trend_direction: str  # "increasing", "decreasing", "stable"
    confidence_level: float
    time_period: str

@dataclass
class ContentTrend:
    """Content trend analysis"""
    topic: str
    frequency: int
    growth_rate: float
    engagement_score: float
    quality_score: float
    channels_covering: List[str]
    trend_strength: str  # "strong", "moderate", "weak"
    recommendation: str

@dataclass
class ChannelTrend:
    """Channel performance trend"""
    channel_id: str
    channel_name: str
    performance_trend: str  # "improving", "declining", "stable"
    key_metrics: Dict[str, TrendMetric]
    content_trends: List[ContentTrend]
    strategic_recommendations: List[str]
    priority_level: str  # "high", "medium", "low"

class TrendAnalysisSystem:
    """Advanced trend analysis and recommendations system"""
    
    def __init__(self, base_path: Optional[Path] = None):
        self.base_path = base_path or Path(__file__).parent
        self.data_path = self.base_path / "data"
        self.reports_path = self.base_path / "reports"
        self.trends_path = self.base_path / "trends"
        self.trends_path.mkdir(parents=True, exist_ok=True)
        
        print(f"📈 Trend Analysis System initialized")
        print(f"   📊 Data path: {self.data_path}")
        print(f"   📋 Reports path: {self.reports_path}")
        print(f"   📈 Trends path: {self.trends_path}")
    
    def analyze_historical_trends(self, days_back: int = 30) -> Dict[str, Any]:
        """Analyze historical trends across multiple time periods"""
        
        print(f"📈 Analyzing historical trends (last {days_back} days)...")
        
        # Load historical intelligence reports
        historical_reports = self._load_historical_reports(days_back)
        
        if len(historical_reports) < 2:
            print(f"⚠️  Need at least 2 historical reports for trend analysis")
            return {"status": "insufficient_data", "reports_found": len(historical_reports)}
        
        # Analyze channel performance trends
        channel_trends = self._analyze_channel_performance_trends(historical_reports)
        
        # Analyze content trends
        content_trends = self._analyze_content_trends(historical_reports)
        
        # Analyze system-wide trends
        system_trends = self._analyze_system_trends(historical_reports)
        
        # Generate strategic recommendations
        strategic_recommendations = self._generate_strategic_recommendations(
            channel_trends, content_trends, system_trends
        )
        
        # Create comprehensive trend report
        trend_report = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "analysis_period_days": days_back,
            "reports_analyzed": len(historical_reports),
            "date_range": {
                "start": historical_reports[-1].get("generated_at", ""),
                "end": historical_reports[0].get("generated_at", "")
            },
            "channel_trends": [asdict(trend) for trend in channel_trends],
            "content_trends": [asdict(trend) for trend in content_trends],
            "system_trends": system_trends,
            "strategic_recommendations": strategic_recommendations,
            "trend_summary": self._generate_trend_summary(channel_trends, content_trends, system_trends)
        }
        
        print(f"✅ Trend analysis complete:")
        print(f"   📊 Channel trends: {len(channel_trends)}")
        print(f"   🎯 Content trends: {len(content_trends)}")
        print(f"   💡 Recommendations: {len(strategic_recommendations)}")
        
        return trend_report
    
    def _load_historical_reports(self, days_back: int) -> List[Dict[str, Any]]:
        """Load historical intelligence reports"""
        
        reports = []
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        # Look for intelligence report files
        for report_file in self.reports_path.glob("channel_intelligence_*.json"):
            try:
                # Extract date from filename
                filename = report_file.stem
                if "channel_intelligence_" in filename:
                    date_part = filename.replace("channel_intelligence_", "")
                    file_date = datetime.strptime(date_part, "%Y-%m-%d_%H-%M-%S")
                    
                    if file_date >= cutoff_date:
                        with open(report_file, 'r') as f:
                            report_data = json.load(f)
                            report_data['file_date'] = file_date.isoformat()
                            reports.append(report_data)
                            
            except Exception as e:
                print(f"   ⚠️  Could not load report {report_file}: {e}")
        
        # Sort by date (newest first)
        reports.sort(key=lambda x: x.get('file_date', ''), reverse=True)
        
        print(f"   📚 Loaded {len(reports)} historical reports")
        return reports
    
    def _analyze_channel_performance_trends(self, reports: List[Dict[str, Any]]) -> List[ChannelTrend]:
        """Analyze performance trends for each channel"""
        
        channel_trends = []
        
        if len(reports) < 2:
            return channel_trends
        
        # Get channel data from most recent and oldest reports
        latest_report = reports[0]
        oldest_report = reports[-1]
        
        latest_channels = {ch['channel_id']: ch for ch in latest_report.get('channel_metrics', [])}
        oldest_channels = {ch['channel_id']: ch for ch in oldest_report.get('channel_metrics', [])}
        
        # Analyze trends for channels present in both reports
        for channel_id in set(latest_channels.keys()) & set(oldest_channels.keys()):
            latest_data = latest_channels[channel_id]
            oldest_data = oldest_channels[channel_id]
            
            # Calculate trend metrics
            key_metrics = {}
            
            # Quality score trend
            if latest_data.get('quality_score') and oldest_data.get('quality_score'):
                quality_trend = self._calculate_trend_metric(
                    "quality_score",
                    latest_data['quality_score'],
                    oldest_data['quality_score']
                )
                key_metrics['quality_score'] = quality_trend
            
            # High-value videos trend
            if latest_data.get('high_value_videos') is not None and oldest_data.get('high_value_videos') is not None:
                high_value_trend = self._calculate_trend_metric(
                    "high_value_videos",
                    latest_data['high_value_videos'],
                    oldest_data['high_value_videos']
                )
                key_metrics['high_value_videos'] = high_value_trend
            
            # Content frequency trend
            if latest_data.get('content_frequency') and oldest_data.get('content_frequency'):
                frequency_trend = self._calculate_trend_metric(
                    "content_frequency",
                    latest_data['content_frequency'],
                    oldest_data['content_frequency']
                )
                key_metrics['content_frequency'] = frequency_trend
            
            # Determine overall performance trend
            performance_trend = self._determine_performance_trend(key_metrics)
            
            # Generate strategic recommendations for this channel
            channel_recommendations = self._generate_channel_recommendations(
                latest_data, oldest_data, key_metrics, performance_trend
            )
            
            # Determine priority level
            priority_level = self._calculate_channel_priority(latest_data, key_metrics, performance_trend)
            
            channel_trend = ChannelTrend(
                channel_id=channel_id,
                channel_name=latest_data.get('channel_name', channel_id),
                performance_trend=performance_trend,
                key_metrics=key_metrics,
                content_trends=[],  # Will be populated by content trend analysis
                strategic_recommendations=channel_recommendations,
                priority_level=priority_level
            )
            
            channel_trends.append(channel_trend)
        
        return channel_trends
    
    def _calculate_trend_metric(self, metric_name: str, current: float, previous: float) -> TrendMetric:
        """Calculate trend metric with direction and confidence"""
        
        if previous == 0:
            change_percentage = 100.0 if current > 0 else 0.0
        else:
            change_percentage = ((current - previous) / previous) * 100
        
        # Determine trend direction
        if abs(change_percentage) < 5:
            trend_direction = "stable"
        elif change_percentage > 0:
            trend_direction = "increasing"
        else:
            trend_direction = "decreasing"
        
        # Calculate confidence level (simplified)
        confidence_level = min(abs(change_percentage) / 50, 1.0)
        
        return TrendMetric(
            metric_name=metric_name,
            current_value=current,
            previous_value=previous,
            change_percentage=round(change_percentage, 2),
            trend_direction=trend_direction,
            confidence_level=round(confidence_level, 3),
            time_period="historical_comparison"
        )
    
    def _determine_performance_trend(self, key_metrics: Dict[str, TrendMetric]) -> str:
        """Determine overall performance trend from key metrics"""
        
        if not key_metrics:
            return "stable"
        
        positive_trends = 0
        negative_trends = 0
        
        for metric in key_metrics.values():
            if metric.trend_direction == "increasing":
                positive_trends += 1
            elif metric.trend_direction == "decreasing":
                negative_trends += 1
        
        if positive_trends > negative_trends:
            return "improving"
        elif negative_trends > positive_trends:
            return "declining"
        else:
            return "stable"
    
    def _analyze_content_trends(self, reports: List[Dict[str, Any]]) -> List[ContentTrend]:
        """Analyze content and topic trends across reports"""
        
        content_trends = []
        
        if len(reports) < 2:
            return content_trends
        
        # Collect trending topics from all reports
        topic_evolution = defaultdict(list)
        
        for report in reports:
            trending_analysis = report.get('trending_analysis', {})
            top_topics = trending_analysis.get('top_trending_topics', [])
            
            for topic_data in top_topics:
                topic = topic_data.get('topic', '')
                if topic:
                    topic_evolution[topic].append({
                        'timestamp': report.get('generated_at', ''),
                        'channel_count': topic_data.get('channel_count', 0),
                        'channels': topic_data.get('channels', [])
                    })
        
        # Analyze trends for each topic
        for topic, evolution in topic_evolution.items():
            if len(evolution) < 2:
                continue
            
            # Sort by timestamp
            evolution.sort(key=lambda x: x['timestamp'])
            
            # Calculate growth rate
            latest = evolution[-1]
            earliest = evolution[0]
            
            if earliest['channel_count'] == 0:
                growth_rate = 100.0 if latest['channel_count'] > 0 else 0.0
            else:
                growth_rate = ((latest['channel_count'] - earliest['channel_count']) / earliest['channel_count']) * 100
            
            # Determine trend strength
            if abs(growth_rate) > 50:
                trend_strength = "strong"
            elif abs(growth_rate) > 25:
                trend_strength = "moderate"
            else:
                trend_strength = "weak"
            
            # Generate recommendation
            recommendation = self._generate_topic_recommendation(topic, growth_rate, latest, trend_strength)
            
            content_trend = ContentTrend(
                topic=topic,
                frequency=latest['channel_count'],
                growth_rate=round(growth_rate, 2),
                engagement_score=0.0,  # Would require more detailed data
                quality_score=0.0,    # Would require more detailed data
                channels_covering=latest['channels'],
                trend_strength=trend_strength,
                recommendation=recommendation
            )
            
            content_trends.append(content_trend)
        
        # Sort by growth rate (descending)
        content_trends.sort(key=lambda x: x.growth_rate, reverse=True)
        
        return content_trends
    
    def _analyze_system_trends(self, reports: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze system-wide trends"""
        
        if len(reports) < 2:
            return {}
        
        latest = reports[0].get('aggregate_metrics', {})
        oldest = reports[-1].get('aggregate_metrics', {})
        
        system_trends = {}
        
        # Key system metrics to track
        metrics_to_track = [
            'total_videos_tracked',
            'total_high_value_videos',
            'high_value_percentage',
            'average_quality_score',
            'channels_with_high_value_content'
        ]
        
        for metric in metrics_to_track:
            if metric in latest and metric in oldest:
                trend_metric = self._calculate_trend_metric(
                    metric,
                    latest[metric],
                    oldest[metric]
                )
                system_trends[metric] = asdict(trend_metric)
        
        # Overall system health assessment
        positive_trends = sum(1 for trend in system_trends.values() 
                            if trend['trend_direction'] == 'increasing')
        total_trends = len(system_trends)
        
        if total_trends > 0:
            health_score = positive_trends / total_trends
            if health_score > 0.6:
                system_health = "improving"
            elif health_score < 0.4:
                system_health = "declining"
            else:
                system_health = "stable"
        else:
            system_health = "unknown"
        
        system_trends['overall_health'] = {
            'status': system_health,
            'score': round(health_score if 'health_score' in locals() else 0.5, 3),
            'positive_trends': positive_trends,
            'total_trends': total_trends
        }
        
        return system_trends
    
    def _generate_strategic_recommendations(self, channel_trends: List[ChannelTrend], 
                                         content_trends: List[ContentTrend], 
                                         system_trends: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate strategic recommendations based on trend analysis"""
        
        recommendations = []
        
        # Channel-based recommendations
        improving_channels = [ct for ct in channel_trends if ct.performance_trend == "improving"]
        declining_channels = [ct for ct in channel_trends if ct.performance_trend == "declining"]
        
        if improving_channels:
            recommendations.append({
                "category": "channel_optimization",
                "priority": "medium",
                "title": "Capitalize on Improving Channels",
                "description": f"{len(improving_channels)} channels showing positive performance trends",
                "action_items": [
                    f"Increase monitoring frequency for {', '.join([c.channel_name for c in improving_channels[:3]])}",
                    "Study successful content patterns from improving channels",
                    "Consider lowering quality thresholds for these channels temporarily"
                ],
                "expected_impact": "15-25% increase in high-value content discovery"
            })
        
        if declining_channels:
            recommendations.append({
                "category": "channel_optimization",
                "priority": "high",
                "title": "Address Declining Channel Performance",
                "description": f"{len(declining_channels)} channels showing negative performance trends",
                "action_items": [
                    f"Review content criteria for {', '.join([c.channel_name for c in declining_channels[:3]])}",
                    "Analyze if topic priorities need adjustment",
                    "Consider reducing resource allocation to consistently poor performers"
                ],
                "expected_impact": "10-15% improvement in overall system quality"
            })
        
        # Content trend recommendations
        strong_growing_topics = [ct for ct in content_trends if ct.trend_strength == "strong" and ct.growth_rate > 0]
        if strong_growing_topics:
            recommendations.append({
                "category": "content_strategy",
                "priority": "high",
                "title": "Leverage Growing Content Trends",
                "description": f"Strong growth detected in {len(strong_growing_topics)} topic areas",
                "action_items": [
                    f"Increase priority weighting for trending topics: {', '.join([t.topic for t in strong_growing_topics[:3]])}",
                    "Enable transcript extraction for content in trending areas",
                    "Expand channel monitoring to include more sources for hot topics"
                ],
                "expected_impact": "20-30% improvement in relevant content capture"
            })
        
        # System health recommendations
        system_health = system_trends.get('overall_health', {})
        if system_health.get('status') == 'declining':
            recommendations.append({
                "category": "system_health",
                "priority": "critical",
                "title": "Address System Performance Decline",
                "description": f"Overall system health declining ({system_health.get('score', 0):.1%} positive trends)",
                "action_items": [
                    "Review and update quality scoring algorithms",
                    "Audit channel configurations for accuracy",
                    "Consider expanding data collection sources"
                ],
                "expected_impact": "System-wide performance improvement"
            })
        
        return recommendations
    
    def _generate_channel_recommendations(self, latest_data: Dict[str, Any], 
                                        oldest_data: Dict[str, Any],
                                        key_metrics: Dict[str, TrendMetric],
                                        performance_trend: str) -> List[str]:
        """Generate specific recommendations for a channel"""
        
        recommendations = []
        
        # Quality-based recommendations
        quality_metric = key_metrics.get('quality_score')
        if quality_metric:
            if quality_metric.trend_direction == "decreasing":
                recommendations.append("Review content quality criteria and scoring algorithm")
                recommendations.append("Analyze recent content for topic alignment issues")
            elif quality_metric.trend_direction == "increasing":
                recommendations.append("Consider this channel as a model for other channels")
                recommendations.append("Increase monitoring frequency to capture more content")
        
        # High-value content recommendations
        high_value_metric = key_metrics.get('high_value_videos')
        if high_value_metric:
            if high_value_metric.current_value == 0:
                recommendations.append("Lower quality threshold temporarily to capture more content")
                recommendations.append("Review priority topic alignments")
            elif high_value_metric.trend_direction == "increasing":
                recommendations.append("Enable transcript extraction for high-value videos")
                recommendations.append("Prioritize this channel for real-time monitoring")
        
        # Frequency-based recommendations
        frequency_metric = key_metrics.get('content_frequency')
        if frequency_metric:
            if frequency_metric.current_value > 3.0:
                recommendations.append("Implement automated quality filtering for high-frequency content")
            elif frequency_metric.trend_direction == "decreasing":
                recommendations.append("Monitor for potential channel inactivity")
        
        return recommendations
    
    def _calculate_channel_priority(self, latest_data: Dict[str, Any], 
                                  key_metrics: Dict[str, TrendMetric], 
                                  performance_trend: str) -> str:
        """Calculate priority level for channel attention"""
        
        priority_score = 0
        
        # Performance trend factor
        if performance_trend == "improving":
            priority_score += 2
        elif performance_trend == "declining":
            priority_score += 3  # Declining channels need more attention
        
        # Quality score factor
        quality_score = latest_data.get('quality_score', 0)
        if quality_score > 0.7:
            priority_score += 2
        elif quality_score < 0.3:
            priority_score += 1
        
        # High-value content factor
        high_value_ratio = latest_data.get('high_value_videos', 0) / max(latest_data.get('total_videos', 1), 1)
        if high_value_ratio > 0.1:
            priority_score += 2
        
        # Trend significance factor
        for metric in key_metrics.values():
            if abs(metric.change_percentage) > 25:
                priority_score += 1
        
        if priority_score >= 5:
            return "high"
        elif priority_score >= 3:
            return "medium"
        else:
            return "low"
    
    def _generate_topic_recommendation(self, topic: str, growth_rate: float, 
                                     latest_data: Dict[str, Any], trend_strength: str) -> str:
        """Generate recommendation for a topic trend"""
        
        if growth_rate > 50:
            return f"High growth trend - increase priority weighting and expand monitoring for '{topic}'"
        elif growth_rate > 25:
            return f"Moderate growth trend - monitor '{topic}' more closely and consider transcript extraction"
        elif growth_rate < -25:
            return f"Declining trend - review relevance of '{topic}' and consider reducing priority"
        else:
            return f"Stable trend - maintain current monitoring level for '{topic}'"
    
    def _generate_trend_summary(self, channel_trends: List[ChannelTrend], 
                               content_trends: List[ContentTrend], 
                               system_trends: Dict[str, Any]) -> Dict[str, Any]:
        """Generate executive summary of trends"""
        
        summary = {}
        
        # Channel trend summary
        if channel_trends:
            improving = len([ct for ct in channel_trends if ct.performance_trend == "improving"])
            declining = len([ct for ct in channel_trends if ct.performance_trend == "declining"])
            stable = len([ct for ct in channel_trends if ct.performance_trend == "stable"])
            
            summary["channel_trends"] = {
                "total_channels_analyzed": len(channel_trends),
                "improving_channels": improving,
                "declining_channels": declining,
                "stable_channels": stable,
                "improvement_rate": round(improving / len(channel_trends) * 100, 1) if channel_trends else 0
            }
        
        # Content trend summary
        if content_trends:
            growing_topics = len([ct for ct in content_trends if ct.growth_rate > 0])
            strong_trends = len([ct for ct in content_trends if ct.trend_strength == "strong"])
            
            summary["content_trends"] = {
                "total_topics_tracked": len(content_trends),
                "growing_topics": growing_topics,
                "strong_trends": strong_trends,
                "top_growing_topic": content_trends[0].topic if content_trends else None,
                "average_growth_rate": round(statistics.mean([ct.growth_rate for ct in content_trends]), 2) if content_trends else 0
            }
        
        # System health summary
        system_health = system_trends.get('overall_health', {})
        summary["system_health"] = {
            "status": system_health.get('status', 'unknown'),
            "health_score": system_health.get('score', 0),
            "positive_trends": system_health.get('positive_trends', 0),
            "total_metrics": system_health.get('total_trends', 0)
        }
        
        return summary
    
    def save_trend_report(self, trend_report: Dict[str, Any]) -> str:
        """Save trend analysis report"""
        
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        trend_file = self.trends_path / f"trend_analysis_{timestamp}.json"
        
        with open(trend_file, 'w') as f:
            json.dump(trend_report, f, indent=2)
        
        # Create latest symlink
        latest_trend = self.trends_path / "latest_trend_analysis.json"
        if latest_trend.exists():
            latest_trend.unlink()
        
        try:
            latest_trend.symlink_to(trend_file.name)
        except:
            import shutil
            shutil.copy2(trend_file, latest_trend)
        
        return str(trend_file)

def main():
    """Run trend analysis system"""
    
    print("📈 Trend Analysis & Recommendations System")
    print("=" * 60)
    
    # Initialize trend analysis system
    trend_system = TrendAnalysisSystem()
    
    # Run trend analysis
    trend_report = trend_system.analyze_historical_trends(days_back=30)
    
    if trend_report.get('status') == 'insufficient_data':
        print(f"❌ Insufficient data for trend analysis")
        print(f"   Found {trend_report.get('reports_found', 0)} reports, need at least 2")
        print(f"   Generate more intelligence reports over time to enable trend analysis")
        return False
    
    # Save trend report
    trend_file = trend_system.save_trend_report(trend_report)
    
    print(f"\n✅ Trend Analysis Complete!")
    print(f"📊 Report saved: {trend_file}")
    
    # Display summary
    summary = trend_report.get('trend_summary', {})
    channel_summary = summary.get('channel_trends', {})
    content_summary = summary.get('content_trends', {})
    
    if channel_summary:
        print(f"\n📈 Channel Trends Summary:")
        print(f"   Improving: {channel_summary.get('improving_channels', 0)}")
        print(f"   Declining: {channel_summary.get('declining_channels', 0)}")
        print(f"   Stable: {channel_summary.get('stable_channels', 0)}")
        print(f"   Improvement Rate: {channel_summary.get('improvement_rate', 0):.1f}%")
    
    if content_summary:
        print(f"\n🎯 Content Trends Summary:")
        print(f"   Growing Topics: {content_summary.get('growing_topics', 0)}")
        print(f"   Strong Trends: {content_summary.get('strong_trends', 0)}")
        if content_summary.get('top_growing_topic'):
            print(f"   Top Growing: {content_summary.get('top_growing_topic')}")
    
    recommendations = trend_report.get('strategic_recommendations', [])
    if recommendations:
        print(f"\n💡 Strategic Recommendations: {len(recommendations)}")
        for rec in recommendations[:3]:  # Show top 3
            print(f"   • {rec.get('title', 'Recommendation')} ({rec.get('priority', 'medium')} priority)")
    
    return True

if __name__ == "__main__":
    main()