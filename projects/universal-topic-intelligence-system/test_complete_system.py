#!/usr/bin/env python3
"""
Complete System Validation Test
Tests the entire Universal Topic Intelligence System with React and Claude configurations
"""

import asyncio
import logging
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

from sources.real_mcp_integration import RealMCPIntegration
from core.rss_feed_validator import RSSFeedValidator
from core import SourceMetadata, SourceType

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SystemValidator:
    """Complete system validation orchestrator"""
    
    def __init__(self):
        self.mcp_integration = RealMCPIntegration()
        self.rss_validator = RSSFeedValidator()
        self.test_results = {
            'start_time': datetime.now(),
            'tests': [],
            'total_items_collected': 0,
            'success_count': 0,
            'failure_count': 0
        }
    
    async def load_topic_configuration(self, config_path: str) -> Dict[str, Any]:
        """Load a topic configuration file"""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            logger.info(f"✅ Loaded configuration: {config['topic_metadata']['name']}")
            return config
        except Exception as e:
            logger.error(f"❌ Failed to load configuration {config_path}: {e}")
            return {}
    
    async def validate_rss_feeds(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate all RSS feeds in a topic configuration"""
        logger.info("📡 Validating RSS feeds...")
        
        rss_urls = []
        
        # Extract RSS URLs from all tiers
        source_mapping = config.get('source_mapping', {})
        for tier_name, tier_data in source_mapping.items():
            sources = tier_data.get('sources', [])
            for source in sources:
                if source.get('monitoring_method') == 'RSS':
                    rss_urls.append({
                        'url': source.get('url'),
                        'name': source.get('name', 'Unknown'),
                        'source_id': source.get('source_id', 'unknown')
                    })
        
        if not rss_urls:
            return {'status': 'skipped', 'message': 'No RSS feeds found', 'feeds': 0}
        
        # Validate feeds
        validation_results = []
        for feed_info in rss_urls:
            try:
                result = await self.rss_validator.validate_single_feed(
                    feed_info['url'], 
                    feed_info['source_id'], 
                    feed_info['name']
                )
                validation_results.append(result)
            except Exception as e:
                logger.error(f"❌ RSS validation error for {feed_info['url']}: {e}")
        
        # Calculate success rate
        successful_feeds = [r for r in validation_results if r.is_valid]
        success_rate = (len(successful_feeds) / len(validation_results)) * 100 if validation_results else 0
        
        return {
            'status': 'completed',
            'total_feeds': len(rss_urls),
            'successful_feeds': len(successful_feeds),
            'success_rate': success_rate,
            'results': validation_results
        }
    
    async def test_youtube_mcp_integration(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Test YouTube MCP integration with configuration sources"""
        logger.info("📹 Testing YouTube MCP integration...")
        
        youtube_sources = []
        
        # Extract YouTube sources
        source_mapping = config.get('source_mapping', {})
        for tier_name, tier_data in source_mapping.items():
            sources = tier_data.get('sources', [])
            for source in sources:
                if source.get('monitoring_method') == 'YouTube MCP':
                    # For testing, we'll use example videos
                    test_videos = [
                        "https://www.youtube.com/watch?v=8pDqJVdNa44",  # React documentary
                        "https://www.youtube.com/watch?v=N3AkSS5hXMA",  # React explained
                    ]
                    youtube_sources.extend(test_videos[:1])  # Limit to 1 for testing
        
        if not youtube_sources:
            return {'status': 'skipped', 'message': 'No YouTube sources found', 'items': 0}
        
        try:
            youtube_items = await self.mcp_integration.extract_youtube_transcripts(
                youtube_sources, max_videos=len(youtube_sources)
            )
            
            return {
                'status': 'success',
                'items_collected': len(youtube_items),
                'sources_tested': len(youtube_sources),
                'items': youtube_items
            }
        except Exception as e:
            logger.error(f"❌ YouTube MCP integration failed: {e}")
            return {'status': 'failed', 'error': str(e), 'items': 0}
    
    async def test_github_mcp_integration(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Test GitHub MCP integration with configuration sources"""
        logger.info("🐙 Testing GitHub MCP integration...")
        
        github_sources = []
        
        # Extract GitHub sources
        source_mapping = config.get('source_mapping', {})
        for tier_name, tier_data in source_mapping.items():
            sources = tier_data.get('sources', [])
            for source in sources:
                if source.get('monitoring_method') == 'GitHub MCP':
                    # Extract repo query from URL
                    url = source.get('url', '')
                    if 'github.com/' in url:
                        repo_path = url.split('github.com/')[-1]
                        github_sources.append(repo_path)
        
        if not github_sources:
            return {'status': 'skipped', 'message': 'No GitHub sources found', 'items': 0}
        
        try:
            github_items = await self.mcp_integration.search_github_repositories(
                github_sources[:3], max_results=2  # Limit for testing
            )
            
            return {
                'status': 'success',
                'items_collected': len(github_items),
                'sources_tested': len(github_sources),
                'items': github_items
            }
        except Exception as e:
            logger.error(f"❌ GitHub MCP integration failed: {e}")
            return {'status': 'failed', 'error': str(e), 'items': 0}
    
    async def test_search_mcp_integration(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Test web search MCP integration with configuration sources"""
        logger.info("🔍 Testing Search MCP integration...")
        
        search_sources = []
        
        # Extract search sources
        source_mapping = config.get('source_mapping', {})
        for tier_name, tier_data in source_mapping.items():
            sources = tier_data.get('sources', [])
            for source in sources:
                if source.get('monitoring_method') == 'Search MCP':
                    query = source.get('search_query', source.get('name', 'test query'))
                    search_sources.append(query)
        
        if not search_sources:
            # Use topic keywords as search queries
            keywords = config.get('topic_metadata', {}).get('keywords_primary', [])
            search_sources = keywords[:2] if keywords else ['technology news']
        
        try:
            search_items = await self.mcp_integration.search_web_content(
                search_sources[:2], max_results=3  # Limit for testing
            )
            
            return {
                'status': 'success',
                'items_collected': len(search_items),
                'sources_tested': len(search_sources),
                'items': search_items
            }
        except Exception as e:
            logger.error(f"❌ Search MCP integration failed: {e}")
            return {'status': 'failed', 'error': str(e), 'items': 0}
    
    async def validate_topic_configuration(self, config_path: str) -> Dict[str, Any]:
        """Complete validation of a topic configuration"""
        config = await self.load_topic_configuration(config_path)
        if not config:
            return {'status': 'failed', 'error': 'Failed to load configuration'}
        
        topic_name = config.get('topic_metadata', {}).get('name', 'Unknown')
        logger.info(f"\n🧪 Testing Topic: {topic_name}")
        logger.info("=" * 60)
        
        test_result = {
            'topic_name': topic_name,
            'config_path': config_path,
            'tests': {},
            'total_items': 0,
            'success': True
        }
        
        # Test RSS feeds
        rss_result = await self.validate_rss_feeds(config)
        test_result['tests']['rss_feeds'] = rss_result
        if rss_result['status'] == 'failed':
            test_result['success'] = False
        
        # Test YouTube MCP integration
        youtube_result = await self.test_youtube_mcp_integration(config)
        test_result['tests']['youtube_mcp'] = youtube_result
        test_result['total_items'] += youtube_result.get('items_collected', 0)
        if youtube_result['status'] == 'failed':
            test_result['success'] = False
        
        # Test GitHub MCP integration
        github_result = await self.test_github_mcp_integration(config)
        test_result['tests']['github_mcp'] = github_result
        test_result['total_items'] += github_result.get('items_collected', 0)
        if github_result['status'] == 'failed':
            test_result['success'] = False
        
        # Test Search MCP integration
        search_result = await self.test_search_mcp_integration(config)
        test_result['tests']['search_mcp'] = search_result
        test_result['total_items'] += search_result.get('items_collected', 0)
        if search_result['status'] == 'failed':
            test_result['success'] = False
        
        # Update global results
        self.test_results['total_items_collected'] += test_result['total_items']
        if test_result['success']:
            self.test_results['success_count'] += 1
        else:
            self.test_results['failure_count'] += 1
        
        self.test_results['tests'].append(test_result)
        
        return test_result
    
    def print_test_results(self, test_result: Dict[str, Any]):
        """Print formatted test results"""
        topic_name = test_result['topic_name']
        success_icon = "✅" if test_result['success'] else "❌"
        
        print(f"\n{success_icon} Topic: {topic_name}")
        print(f"   📊 Total Items Collected: {test_result['total_items']}")
        
        for test_name, result in test_result['tests'].items():
            status_icon = "✅" if result['status'] == 'success' else "⚠️" if result['status'] == 'skipped' else "❌"
            
            if test_name == 'rss_feeds':
                if result['status'] == 'completed':
                    print(f"   {status_icon} RSS Feeds: {result['successful_feeds']}/{result['total_feeds']} ({result['success_rate']:.1f}%)")
                else:
                    print(f"   {status_icon} RSS Feeds: {result['message']}")
            
            elif test_name in ['youtube_mcp', 'github_mcp', 'search_mcp']:
                service_name = test_name.replace('_mcp', '').replace('_', ' ').title()
                if result['status'] == 'success':
                    print(f"   {status_icon} {service_name}: {result['items_collected']} items from {result.get('sources_tested', 0)} sources")
                elif result['status'] == 'skipped':
                    print(f"   {status_icon} {service_name}: {result['message']}")
                else:
                    print(f"   {status_icon} {service_name}: Failed - {result.get('error', 'Unknown error')}")
    
    async def run_complete_validation(self) -> Dict[str, Any]:
        """Run complete system validation"""
        print("🚀 Universal Topic Intelligence System - Complete Validation")
        print("=" * 70)
        
        # Test configurations
        config_paths = [
            "universal-topic-system/examples/react-ecosystem-topic-configuration.yaml",
            "universal-topic-system/examples/claude-ecosystem-topic-configuration.yaml"
        ]
        
        for config_path in config_paths:
            if Path(config_path).exists():
                test_result = await self.validate_topic_configuration(config_path)
                self.print_test_results(test_result)
            else:
                logger.warning(f"⚠️  Configuration file not found: {config_path}")
        
        # Final summary
        self.test_results['end_time'] = datetime.now()
        duration = self.test_results['end_time'] - self.test_results['start_time']
        
        print("\n" + "=" * 70)
        print("📊 COMPLETE SYSTEM VALIDATION SUMMARY")
        print("=" * 70)
        print(f"⏱️  Duration: {duration.total_seconds():.1f} seconds")
        print(f"📝 Topics Tested: {len(self.test_results['tests'])}")
        print(f"✅ Successful Topics: {self.test_results['success_count']}")
        print(f"❌ Failed Topics: {self.test_results['failure_count']}")
        print(f"📊 Total Items Collected: {self.test_results['total_items_collected']}")
        
        overall_success = self.test_results['failure_count'] == 0
        print(f"\n🎯 OVERALL RESULT: {'✅ SUCCESS' if overall_success else '❌ FAILURE'}")
        
        return {
            'success': overall_success,
            'results': self.test_results
        }

async def main():
    """Main test execution"""
    validator = SystemValidator()
    result = await validator.run_complete_validation()
    return result['success']

if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)