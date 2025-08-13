#!/usr/bin/env python3
"""
Fixed Universal Topic Monitor with Database Storage Integration
Properly stores collected content and uses existing infrastructure
"""

import yaml
import asyncio
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

from .rss_monitor import RSSSourceMonitor
from core import SourceMetadata, SourceType, ContentItem
from storage.database import StorageManager
from core.content_prioritizer import UniversalContentPrioritizer as ContentPrioritizer
from core.quality_scorer import TopicQualityScorer

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("UniversalTopicMonitor")


class UniversalTopicMonitorFixed:
    """
    Fixed universal topic monitor with proper database integration
    and use of existing infrastructure
    """
    
    def __init__(self, config_directory: str = "universal-topic-system/examples"):
        self.config_directory = Path(config_directory)
        self.active_topics: Dict[str, Dict] = {}
        self.monitors: Dict[str, Dict[str, RSSSourceMonitor]] = {}
        
        # Initialize storage and prioritization
        self.storage = StorageManager()
        self.prioritizer = ContentPrioritizer()
        self.quality_scorers: Dict[str, TopicQualityScorer] = {}
        
        # Statistics tracking
        self.stats = {
            "items_stored": 0,
            "items_failed": 0,
            "sources_success": 0,
            "sources_failed": 0
        }
        
        # Load all available topic configurations
        self._load_topic_configurations()
    
    def _load_topic_configurations(self):
        """Load all topic configuration files from the config directory"""
        if not self.config_directory.exists():
            logger.warning(f"Configuration directory not found: {self.config_directory}")
            return
        
        config_files = list(self.config_directory.glob("*-topic-configuration.yaml"))
        logger.info(f"Found {len(config_files)} topic configuration files")
        
        for config_file in config_files:
            try:
                topic_config = self._load_yaml_config(config_file)
                topic_slug = topic_config['topic_metadata']['slug']
                
                # Validate required fields
                if self._validate_topic_config(topic_config):
                    self.active_topics[topic_slug] = topic_config
                    self._initialize_topic_monitors(topic_slug, topic_config)
                    self._initialize_quality_scorer(topic_slug, topic_config)
                    
                    logger.info(f"✅ Loaded topic: {topic_config['topic_metadata']['name']} ({topic_slug})")
                
            except Exception as e:
                logger.error(f"❌ Error loading {config_file.name}: {e}")
    
    def _load_yaml_config(self, config_file: Path) -> Dict:
        """Load and parse YAML configuration file"""
        with open(config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def _validate_topic_config(self, config: Dict) -> bool:
        """Validate that topic configuration has required fields"""
        try:
            required_fields = ['topic_metadata', 'source_mapping']
            for field in required_fields:
                if field not in config:
                    logger.warning(f"Missing required field: {field}")
                    return False
            
            # Validate topic metadata
            metadata = config['topic_metadata']
            required_metadata = ['name', 'slug']
            for field in required_metadata:
                if field not in metadata:
                    logger.warning(f"Missing required metadata field: {field}")
                    return False
            
            return True
        except Exception as e:
            logger.error(f"Validation error: {e}")
            return False
    
    def _initialize_quality_scorer(self, topic_slug: str, topic_config: Dict):
        """Initialize quality scorer for the topic"""
        try:
            # Extract boost keywords from config
            boost_keywords = []
            if 'keywords_primary' in topic_config['topic_metadata']:
                boost_keywords.extend(topic_config['topic_metadata']['keywords_primary'])
            
            # Create topic-specific quality scorer with proper config
            quality_config = {
                "thresholds": {
                    "critical": 0.85,
                    "high": 0.70,
                    "medium": 0.50,
                    "low": 0.30
                },
                "boost_keywords": boost_keywords,
                "boost_multipliers": self._extract_boost_multipliers(topic_config)
            }
            
            self.quality_scorers[topic_slug] = TopicQualityScorer(quality_config)
            logger.info(f"Initialized quality scorer for topic: {topic_slug}")
        except Exception as e:
            logger.error(f"Error initializing quality scorer for {topic_slug}: {e}")
    
    def _extract_boost_multipliers(self, topic_config: Dict) -> Dict[str, float]:
        """Extract boost multipliers from topic configuration"""
        multipliers = {}
        
        # Check for quality assessment configuration
        if 'quality_assessment' in topic_config:
            qa_config = topic_config['quality_assessment']
            if 'boost_rules' in qa_config and 'high_value_terms' in qa_config['boost_rules']:
                for term_rule in qa_config['boost_rules']['high_value_terms']:
                    if 'term' in term_rule and 'multiplier' in term_rule:
                        multipliers[term_rule['term']] = term_rule['multiplier']
        
        return multipliers
    
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
                
                # Initialize monitor with better error handling
                monitor = RSSSourceMonitor(
                    metadata,
                    config={
                        "timeout": 30,  # Increased timeout
                        "max_items": 20,
                        "enable_language_filtering": True,
                        "retry_on_failure": True,
                        "max_retries": 2
                    }
                )
                
                self.monitors[topic_slug][source_id] = monitor
    
    def _is_rss_compatible(self, source: Dict) -> bool:
        """Check if source is compatible with RSS monitoring"""
        monitoring_method = source.get('monitoring_method', 'RSS')
        return any(method in monitoring_method for method in ['RSS', 'Fetch', 'rss'])
    
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
        topics.extend([k.lower() for k in primary_keywords[:3]])  # Limit to first 3
        
        return list(set(topics))  # Remove duplicates
    
    async def monitor_topic_with_storage(self, topic_slug: str) -> Dict[str, Any]:
        """
        Monitor all sources for a topic and store results in database
        """
        if topic_slug not in self.monitors:
            logger.error(f"Topic not found: {topic_slug}")
            return {"error": f"Topic not found: {topic_slug}"}
        
        topic_monitors = self.monitors[topic_slug]
        topic_config = self.active_topics[topic_slug]
        quality_scorer = self.quality_scorers.get(topic_slug)
        
        results = {}
        total_items_stored = 0
        total_items_found = 0
        
        logger.info(f"🔍 Monitoring {len(topic_monitors)} sources for topic: {topic_slug}")
        
        for source_id, monitor in topic_monitors.items():
            try:
                # Monitor the source
                result = await monitor.monitor()
                
                items_stored = 0
                if result.success and result.new_items:
                    # Process and store each item
                    for item in result.new_items:
                        try:
                            # Calculate priority score using existing prioritizer
                            priority_result = self.prioritizer.prioritize(
                                item,
                                strategy='default'
                            )
                            priority_score = priority_result.total_score
                            
                            # Apply topic-specific quality scoring if available
                            if quality_scorer:
                                quality_result = quality_scorer.score_content(item)
                                quality_score = quality_result.total_score
                                # Combine scores
                                priority_score = (priority_score * 0.6) + (quality_score * 0.4)
                            
                            # Determine priority level
                            if priority_score >= 0.85:
                                priority_level = "critical"
                            elif priority_score >= 0.70:
                                priority_level = "high"
                            elif priority_score >= 0.50:
                                priority_level = "medium"
                            else:
                                priority_level = "low"
                            
                            # Add topic tag to item
                            if not hasattr(item, 'tags'):
                                item.tags = []
                            item.tags.append(f"topic:{topic_slug}")
                            
                            # Store in database
                            stored = await self.storage.store_content(
                                item=item,
                                priority_score=priority_score,
                                priority_level=priority_level
                            )
                            
                            if stored:
                                items_stored += 1
                                
                        except Exception as e:
                            logger.error(f"Error storing item from {source_id}: {e}")
                    
                    total_items_stored += items_stored
                    total_items_found += len(result.new_items)
                    self.stats["sources_success"] += 1
                    
                    logger.info(f"✅ {source_id}: {len(result.new_items)} found, {items_stored} stored")
                else:
                    self.stats["sources_failed"] += 1
                    logger.warning(f"⚠️ {source_id}: No items or failed")
                
                # Store result info
                results[source_id] = {
                    "success": result.success,
                    "items_found": len(result.new_items) if result.success else 0,
                    "items_stored": items_stored,
                    "errors": result.errors if not result.success else []
                }
                
            except Exception as e:
                logger.error(f"❌ Error monitoring {source_id}: {e}")
                results[source_id] = {
                    "success": False,
                    "error": str(e),
                    "items_found": 0,
                    "items_stored": 0
                }
                self.stats["sources_failed"] += 1
        
        # Update global stats
        self.stats["items_stored"] += total_items_stored
        
        return {
            "topic": topic_slug,
            "topic_name": topic_config['topic_metadata']['name'],
            "sources_monitored": len(topic_monitors),
            "results": results,
            "total_items_found": total_items_found,
            "total_items_stored": total_items_stored,
            "success_rate": (self.stats["sources_success"] / 
                           max(self.stats["sources_success"] + self.stats["sources_failed"], 1)) * 100,
            "timestamp": datetime.now().isoformat()
        }
    
    async def monitor_all_topics_with_storage(self) -> Dict[str, Any]:
        """Monitor all active topics and store results"""
        all_results = {}
        total_stored = 0
        total_found = 0
        
        for topic_slug in self.active_topics.keys():
            logger.info(f"\n📊 Starting monitoring for topic: {topic_slug}")
            topic_result = await self.monitor_topic_with_storage(topic_slug)
            all_results[topic_slug] = topic_result
            total_stored += topic_result.get('total_items_stored', 0)
            total_found += topic_result.get('total_items_found', 0)
        
        return {
            "topics_monitored": len(self.active_topics),
            "total_items_found": total_found,
            "total_items_stored": total_stored,
            "topic_results": all_results,
            "global_stats": self.stats,
            "timestamp": datetime.now().isoformat()
        }
    
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
                'description': metadata.get('description', ''),
                'priority_level': metadata.get('priority_level', 'medium'),
                'status': metadata.get('status', 'active'),
                'source_count': len(self.monitors.get(slug, {})),
                'has_quality_scorer': slug in self.quality_scorers
            })
        return topics
    
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
            'average_sources_per_topic': total_sources / max(total_topics, 1),
            'items_stored': self.stats['items_stored'],
            'success_rate': (self.stats["sources_success"] / 
                           max(self.stats["sources_success"] + self.stats["sources_failed"], 1)) * 100
        }


if __name__ == "__main__":
    async def main():
        monitor = UniversalTopicMonitorFixed()
        
        print("📋 Available Topics:")
        for topic in monitor.list_available_topics():
            print(f"  - {topic['name']} ({topic['slug']}): {topic['source_count']} sources")
            print(f"    Quality Scorer: {'✅' if topic['has_quality_scorer'] else '❌'}")
        
        print(f"\n📊 Monitoring Statistics:")
        stats = monitor.get_monitoring_stats()
        print(f"  - Total Topics: {stats['total_topics']}")
        print(f"  - Active Topics: {stats['active_topics']}")
        print(f"  - Total Sources: {stats['total_sources']}")
        
        # Monitor all topics with storage
        print("\n🔍 Monitoring all topics with database storage...")
        result = await monitor.monitor_all_topics_with_storage()
        print(f"✅ Monitoring complete:")
        print(f"  - Items Found: {result['total_items_found']}")
        print(f"  - Items Stored: {result['total_items_stored']}")
        print(f"  - Success Rate: {result['global_stats']['sources_success']}/{result['global_stats']['sources_success'] + result['global_stats']['sources_failed']} sources")
    
    asyncio.run(main())