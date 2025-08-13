#!/usr/bin/env python3
"""
Universal Topic Monitor - Dynamic topic monitoring using YAML configurations
Replaces hardcoded topic monitoring with configurable, universal approach
"""

import yaml
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional
from .rss_monitor import RSSSourceMonitor
from core import SourceMetadata, SourceType


class UniversalTopicMonitor:
    """
    Universal topic monitor that can load and monitor any topic configuration
    from YAML files, enabling true universal topic intelligence
    """
    
    def __init__(self, config_directory: str = "universal-topic-system/examples"):
        self.config_directory = Path(config_directory)
        self.active_topics: Dict[str, Dict] = {}
        self.monitors: Dict[str, Dict[str, RSSSourceMonitor]] = {}
        
        # Load all available topic configurations
        self._load_topic_configurations()
    
    def _load_topic_configurations(self):
        """Load all topic configuration files from the config directory"""
        if not self.config_directory.exists():
            raise ValueError(f"Configuration directory not found: {self.config_directory}")
        
        config_files = list(self.config_directory.glob("*-topic-configuration.yaml"))
        print(f"Found {len(config_files)} topic configuration files")
        
        for config_file in config_files:
            try:
                topic_config = self._load_yaml_config(config_file)
                topic_slug = topic_config['topic_metadata']['slug']
                
                # Validate required fields
                self._validate_topic_config(topic_config)
                
                self.active_topics[topic_slug] = topic_config
                self._initialize_topic_monitors(topic_slug, topic_config)
                
                print(f"✅ Loaded topic: {topic_config['topic_metadata']['name']} ({topic_slug})")
                
            except Exception as e:
                print(f"❌ Error loading {config_file.name}: {e}")
    
    def _load_yaml_config(self, config_file: Path) -> Dict:
        """Load and parse YAML configuration file"""
        with open(config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _validate_topic_config(self, config: Dict):
        """Validate that topic configuration has required fields"""
        required_fields = ['topic_metadata', 'source_mapping', 'content_analysis']
        for field in required_fields:
            if field not in config:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate topic metadata
        metadata = config['topic_metadata']
        required_metadata = ['name', 'slug', 'description']
        for field in required_metadata:
            if field not in metadata:
                raise ValueError(f"Missing required metadata field: {field}")
    
    def _initialize_topic_monitors(self, topic_slug: str, topic_config: Dict):
        """Initialize RSS monitors for all sources in a topic configuration"""
        self.monitors[topic_slug] = {}
        source_mapping = topic_config['source_mapping']
        
        # Process all tiers of sources
        for tier_name, tier_config in source_mapping.items():
            if 'sources' not in tier_config or not tier_config['sources']:
                continue
                
            for source in tier_config['sources']:
                if not self._is_rss_compatible(source):
                    continue
                    
                source_id = self._generate_source_id(source, topic_slug)
                
                # Create metadata from configuration
                metadata = SourceMetadata(
                    source_id=source_id,
                    source_name=self._extract_source_name(source),
                    source_type=SourceType.RSS,
                    source_url=source['url'],
                    authority_score=source.get('authority_score', 0.5),
                    update_frequency=source.get('update_frequency', 'daily'),
                    topics=self._extract_topics(source, topic_config)
                )
                
                # Initialize monitor
                monitor = RSSSourceMonitor(
                    metadata,
                    config={
                        "timeout": 15,
                        "max_items": 20
                    }
                )
                
                self.monitors[topic_slug][source_id] = monitor
    
    def _is_rss_compatible(self, source: Dict) -> bool:
        """Check if source is compatible with RSS monitoring"""
        monitoring_method = source.get('monitoring_method', 'RSS')
        return any(method in monitoring_method for method in ['RSS', 'Fetch'])
    
    def _generate_source_id(self, source: Dict, topic_slug: str) -> str:
        """Generate unique source ID"""
        if 'source_id' in source:
            return f"{topic_slug}_{source['source_id']}"
        
        # Generate from URL
        from urllib.parse import urlparse
        parsed = urlparse(source['url'])
        domain = parsed.netloc.replace('www.', '').replace('.', '_')
        return f"{topic_slug}_{domain}"
    
    def _extract_source_name(self, source: Dict) -> str:
        """Extract or generate source name"""
        if 'name' in source:
            return source['name']
        if 'source_name' in source:
            return source['source_name']
        
        # Generate from URL
        from urllib.parse import urlparse
        parsed = urlparse(source['url'])
        return parsed.netloc.replace('www.', '').title()
    
    def _extract_topics(self, source: Dict, topic_config: Dict) -> List[str]:
        """Extract topics from source and topic configuration"""
        topics = []
        
        # Add primary topic
        topics.append(topic_config['topic_metadata']['slug'])
        
        # Add source-specific topics if available
        if 'topics' in source:
            topics.extend(source['topics'])
        
        # Add primary keywords as topics
        primary_keywords = topic_config['topic_metadata'].get('keywords_primary', [])
        topics.extend(primary_keywords)
        
        return list(set(topics))  # Remove duplicates
    
    async def monitor_topic(self, topic_slug: str) -> Dict[str, Any]:
        """Monitor all sources for a specific topic"""
        if topic_slug not in self.monitors:
            raise ValueError(f"Topic not found: {topic_slug}")
        
        topic_monitors = self.monitors[topic_slug]
        results = {}
        
        print(f"🔍 Monitoring {len(topic_monitors)} sources for topic: {topic_slug}")
        
        for source_id, monitor in topic_monitors.items():
            try:
                result = await monitor.monitor()
                # Convert MonitoringResult to dict for compatibility
                result_dict = {
                    "success": result.success,
                    "items_found": len(result.new_items) if result.success else 0,
                    "source_name": getattr(result, 'source_name', 'Unknown'),
                    "monitoring_duration": getattr(result, 'monitoring_duration', 0),
                    "errors": result.errors if not result.success else []
                }
                results[source_id] = result_dict
                print(f"✅ {source_id}: {result_dict['items_found']} items")
            except Exception as e:
                print(f"❌ Error monitoring {source_id}: {e}")
                results[source_id] = {"error": str(e), "items_found": 0}
        
        return {
            "topic": topic_slug,
            "sources_monitored": len(topic_monitors),
            "results": results,
            "total_items": sum(
                r.get('items_found', 0) if isinstance(r, dict) else 0 
                for r in results.values()
            )
        }
    
    async def monitor_all_topics(self) -> Dict[str, Any]:
        """Monitor all active topics"""
        all_results = {}
        
        for topic_slug in self.active_topics.keys():
            print(f"\n📊 Starting monitoring for topic: {topic_slug}")
            topic_result = await self.monitor_topic(topic_slug)
            all_results[topic_slug] = topic_result
        
        return all_results
    
    def get_topic_info(self, topic_slug: str) -> Optional[Dict]:
        """Get information about a specific topic"""
        return self.active_topics.get(topic_slug)
    
    def list_available_topics(self) -> List[Dict[str, Any]]:
        """List all available topics with basic information"""
        topics = []
        for slug, config in self.active_topics.items():
            metadata = config['topic_metadata']
            topics.append({
                'slug': slug,
                'name': metadata['name'],
                'description': metadata['description'],
                'priority_level': metadata.get('priority_level', 'medium'),
                'status': metadata.get('status', 'active'),
                'source_count': self._count_topic_sources(slug)
            })
        return topics
    
    def _count_topic_sources(self, topic_slug: str) -> int:
        """Count total sources for a topic"""
        if topic_slug not in self.monitors:
            return 0
        return len(self.monitors[topic_slug])
    
    def get_topic_sources(self, topic_slug: str) -> List[Dict]:
        """Get all sources for a specific topic"""
        if topic_slug not in self.active_topics:
            return []
        
        sources = []
        source_mapping = self.active_topics[topic_slug]['source_mapping']
        
        for tier_name, tier_config in source_mapping.items():
            if 'sources' not in tier_config:
                continue
            
            for source in tier_config['sources']:
                source_info = source.copy()
                source_info['tier'] = tier_name
                source_info['topic'] = topic_slug
                sources.append(source_info)
        
        return sources
    
    async def monitor_by_keywords(self, keywords: List[str]) -> Dict[str, Any]:
        """Monitor topics that contain specific keywords"""
        matching_topics = []
        
        for slug, config in self.active_topics.items():
            topic_keywords = (
                config['topic_metadata'].get('keywords_primary', []) +
                config['topic_metadata'].get('keywords_secondary', [])
            )
            
            # Check if any keyword matches
            if any(keyword.lower() in [k.lower() for k in topic_keywords] 
                   for keyword in keywords):
                matching_topics.append(slug)
        
        results = {}
        for topic_slug in matching_topics:
            results[topic_slug] = await self.monitor_topic(topic_slug)
        
        return results
    
    def add_topic_configuration(self, config_file_path: str):
        """Add a new topic configuration from file"""
        config_file = Path(config_file_path)
        if not config_file.exists():
            raise ValueError(f"Configuration file not found: {config_file_path}")
        
        topic_config = self._load_yaml_config(config_file)
        self._validate_topic_config(topic_config)
        
        topic_slug = topic_config['topic_metadata']['slug']
        self.active_topics[topic_slug] = topic_config
        self._initialize_topic_monitors(topic_slug, topic_config)
        
        return topic_slug
    
    def get_monitoring_stats(self) -> Dict[str, Any]:
        """Get overall monitoring statistics"""
        total_topics = len(self.active_topics)
        total_sources = sum(len(monitors) for monitors in self.monitors.values())
        
        active_topics = [
            slug for slug, config in self.active_topics.items()
            if config['topic_metadata'].get('status', 'active') == 'active'
        ]
        
        return {
            'total_topics': total_topics,
            'active_topics': len(active_topics),
            'total_sources': total_sources,
            'topics': active_topics,
            'average_sources_per_topic': total_sources / max(total_topics, 1)
        }


# Convenience function for backward compatibility
async def monitor_claude_topics():
    """Monitor AI/ML topics (includes Claude, React, etc.)"""
    monitor = UniversalTopicMonitor()
    
    # Look for AI/ML topic configuration
    ai_topics = [topic for topic in monitor.list_available_topics() 
                 if any(keyword in topic['slug'] for keyword in ['ai-ml', 'claude', 'ai'])]
    
    if ai_topics:
        return await monitor.monitor_topic(ai_topics[0]['slug'])
    else:
        print("❌ No AI/ML topic configuration found")
        return {}


if __name__ == "__main__":
    async def main():
        monitor = UniversalTopicMonitor()
        
        print("📋 Available Topics:")
        for topic in monitor.list_available_topics():
            print(f"  - {topic['name']} ({topic['slug']}): {topic['source_count']} sources")
        
        print(f"\n📊 Monitoring Statistics:")
        stats = monitor.get_monitoring_stats()
        print(f"  - Total Topics: {stats['total_topics']}")
        print(f"  - Active Topics: {stats['active_topics']}")
        print(f"  - Total Sources: {stats['total_sources']}")
        
        # Monitor first available topic as example
        if stats['active_topics'] > 0:
            first_topic = stats['topics'][0]
            print(f"\n🔍 Example: Monitoring '{first_topic}'...")
            result = await monitor.monitor_topic(first_topic)
            print(f"✅ Found {result['total_items']} items across {result['sources_monitored']} sources")
    
    asyncio.run(main())