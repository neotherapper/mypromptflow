#!/usr/bin/env python3
"""
RSS Feed Collector for Unified Intelligence System
Collects and processes RSS feeds from YouTube channels and other sources
"""

import json
import os
import requests
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
import time
import logging
from urllib.parse import urlparse
import hashlib

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RSSFeedCollector:
    """Collects and processes RSS feeds for the unified intelligence system"""
    
    def __init__(self, config_path: Optional[Path] = None):
        self.base_path = Path(__file__).parent
        self.config_path = config_path or (self.base_path / "config" / "youtube-rss-channels.json")
        self.data_path = self.base_path / "data" / "rss-feeds"
        self.data_path.mkdir(parents=True, exist_ok=True)
        
        # Load RSS configuration
        self.config = self._load_config()
        self.feed_settings = self.config.get('feed_settings', {})
        
        # Request session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Unified Intelligence System RSS Collector)'
        })
        
        logger.info(f"RSS Feed Collector initialized with {len(self.config.get('channels', []))} channels")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load RSS feed configuration"""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                logger.info(f"Loaded configuration for {config.get('metadata', {}).get('total_channels', 0)} channels")
                return config
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {self.config_path}")
            return {"channels": [], "feed_settings": {}}
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in configuration file: {e}")
            return {"channels": [], "feed_settings": {}}
    
    def collect_all_feeds(self) -> Dict[str, Any]:
        """Collect content from all configured RSS feeds"""
        
        logger.info("🔄 Starting RSS feed collection for all channels")
        start_time = time.time()
        
        results = {
            "collection_metadata": {
                "started_at": datetime.now(timezone.utc).isoformat(),
                "total_channels": len(self.config.get('channels', [])),
                "successful_channels": 0,
                "failed_channels": 0,
                "total_items_collected": 0
            },
            "channel_results": {},
            "errors": []
        }
        
        channels = self.config.get('channels', [])
        
        for channel in channels:
            channel_id = channel.get('id')
            logger.info(f"📡 Processing RSS feed for {channel.get('name', channel_id)}")
            
            try:
                channel_result = self._collect_channel_feed(channel)
                results["channel_results"][channel_id] = channel_result
                
                if channel_result.get('success', False):
                    results["collection_metadata"]["successful_channels"] += 1
                    results["collection_metadata"]["total_items_collected"] += len(
                        channel_result.get('items', [])
                    )
                else:
                    results["collection_metadata"]["failed_channels"] += 1
                    
            except Exception as e:
                error_msg = f"Failed to collect feed for {channel_id}: {str(e)}"
                logger.error(error_msg)
                results["errors"].append(error_msg)
                results["collection_metadata"]["failed_channels"] += 1
        
        # Complete metadata
        duration = time.time() - start_time
        results["collection_metadata"]["completed_at"] = datetime.now(timezone.utc).isoformat()
        results["collection_metadata"]["duration_seconds"] = round(duration, 2)
        
        # Save collection results
        self._save_collection_results(results)
        
        logger.info(f"✅ RSS collection completed in {duration:.2f}s")
        logger.info(f"   📊 {results['collection_metadata']['successful_channels']} successful, "
                   f"{results['collection_metadata']['failed_channels']} failed")
        logger.info(f"   📰 {results['collection_metadata']['total_items_collected']} total items collected")
        
        return results
    
    def _collect_channel_feed(self, channel: Dict[str, Any]) -> Dict[str, Any]:
        """Collect RSS feed for a single channel"""
        
        channel_id = channel.get('id')
        rss_url = channel.get('rss_url')
        
        result = {
            "channel_id": channel_id,
            "channel_name": channel.get('name'),
            "success": False,
            "items": [],
            "error": None,
            "collected_at": datetime.now(timezone.utc).isoformat()
        }
        
        if not rss_url:
            result["error"] = "No RSS URL configured"
            return result
        
        try:
            # Fetch RSS feed with timeout and retries
            timeout = self.feed_settings.get('timeout_seconds', 30)
            retry_attempts = self.feed_settings.get('retry_attempts', 3)
            
            response = None
            last_error = None
            
            for attempt in range(retry_attempts):
                try:
                    response = self.session.get(rss_url, timeout=timeout)
                    response.raise_for_status()
                    break
                except Exception as e:
                    last_error = e
                    if attempt < retry_attempts - 1:
                        logger.warning(f"Attempt {attempt + 1} failed for {channel_id}: {e}")
                        time.sleep(2 ** attempt)  # Exponential backoff
                    
            if response is None:
                result["error"] = f"Failed after {retry_attempts} attempts: {last_error}"
                return result
            
            # Parse RSS XML
            items = self._parse_rss_xml(response.text, channel)
            
            # Filter by age and quality
            filtered_items = self._filter_items(items, channel)
            
            result["items"] = filtered_items
            result["success"] = True
            result["total_items_found"] = len(items)
            result["items_after_filtering"] = len(filtered_items)
            
            # Save channel data
            self._save_channel_data(channel_id, filtered_items)
            
            logger.info(f"   ✅ {channel.get('name')}: {len(filtered_items)} items collected")
            
        except ET.ParseError as e:
            result["error"] = f"XML parsing error: {str(e)}"
            logger.error(f"XML parsing error for {channel_id}: {e}")
        except requests.RequestException as e:
            result["error"] = f"Request error: {str(e)}"
            logger.error(f"Request error for {channel_id}: {e}")
        except Exception as e:
            result["error"] = f"Unexpected error: {str(e)}"
            logger.error(f"Unexpected error for {channel_id}: {e}")
        
        return result
    
    def _parse_rss_xml(self, xml_content: str, channel: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse RSS XML and extract items"""
        
        root = ET.fromstring(xml_content)
        
        # Find all item elements (handle different RSS namespaces)
        items = []
        
        # YouTube RSS feeds use Atom format
        if root.tag.endswith('feed'):
            # Atom feed format
            entries = root.findall('.//{http://www.w3.org/2005/Atom}entry')
            
            for entry in entries:
                item = self._parse_atom_entry(entry, channel)
                if item:
                    items.append(item)
        else:
            # Standard RSS format
            rss_items = root.findall('.//item')
            
            for rss_item in rss_items:
                item = self._parse_rss_item(rss_item, channel)
                if item:
                    items.append(item)
        
        return items
    
    def _parse_atom_entry(self, entry: ET.Element, channel: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Parse an Atom entry (YouTube RSS format)"""
        
        try:
            # Extract basic information
            title_elem = entry.find('.//{http://www.w3.org/2005/Atom}title')
            link_elem = entry.find('.//{http://www.w3.org/2005/Atom}link')
            published_elem = entry.find('.//{http://www.w3.org/2005/Atom}published')
            updated_elem = entry.find('.//{http://www.w3.org/2005/Atom}updated')
            author_elem = entry.find('.//{http://www.w3.org/2005/Atom}author/{http://www.w3.org/2005/Atom}name')
            
            # YouTube-specific elements
            video_id_elem = entry.find('.//{http://www.youtube.com/xml/schemas/2015}videoId')
            channel_id_elem = entry.find('.//{http://www.youtube.com/xml/schemas/2015}channelId')
            
            # Extract description/summary
            summary_elem = entry.find('.//{http://www.w3.org/2005/Atom}summary')
            content_elem = entry.find('.//{http://www.w3.org/2005/Atom}content')
            
            # Build item data
            item = {
                "id": video_id_elem.text if video_id_elem is not None else None,
                "title": title_elem.text if title_elem is not None else "Unknown Title",
                "url": link_elem.get('href') if link_elem is not None else "",
                "published_date": published_elem.text if published_elem is not None else None,
                "updated_date": updated_elem.text if updated_elem is not None else None,
                "author": author_elem.text if author_elem is not None else channel.get('name', 'Unknown'),
                "channel_id": channel_id_elem.text if channel_id_elem is not None else channel.get('channel_id'),
                "channel_name": channel.get('name'),
                "description": (summary_elem.text if summary_elem is not None else 
                              content_elem.text if content_elem is not None else ""),
                "source_channel": channel.get('id'),
                "platform": "youtube",
                "priority_score": channel.get('priority_score', 3.0),
                "quality_rating": channel.get('quality_rating', 4.0),
                "priority_topics": channel.get('priority_topics', []),
                "categories": channel.get('categories', []),
                "collected_at": datetime.now(timezone.utc).isoformat()
            }
            
            # Generate unique hash for deduplication
            content_hash = hashlib.md5(
                f"{item['id']}{item['title']}{item['url']}".encode()
            ).hexdigest()
            item["content_hash"] = content_hash
            
            return item
            
        except Exception as e:
            logger.warning(f"Error parsing Atom entry: {e}")
            return None
    
    def _parse_rss_item(self, item_elem: ET.Element, channel: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Parse a standard RSS item"""
        
        try:
            # Extract basic information
            title_elem = item_elem.find('title')
            link_elem = item_elem.find('link')
            pub_date_elem = item_elem.find('pubDate')
            description_elem = item_elem.find('description')
            guid_elem = item_elem.find('guid')
            
            # Build item data
            item = {
                "id": guid_elem.text if guid_elem is not None else None,
                "title": title_elem.text if title_elem is not None else "Unknown Title",
                "url": link_elem.text if link_elem is not None else "",
                "published_date": pub_date_elem.text if pub_date_elem is not None else None,
                "description": description_elem.text if description_elem is not None else "",
                "channel_name": channel.get('name'),
                "source_channel": channel.get('id'),
                "platform": "rss",
                "priority_score": channel.get('priority_score', 3.0),
                "quality_rating": channel.get('quality_rating', 4.0),
                "priority_topics": channel.get('priority_topics', []),
                "categories": channel.get('categories', []),
                "collected_at": datetime.now(timezone.utc).isoformat()
            }
            
            # Generate unique hash for deduplication
            content_hash = hashlib.md5(
                f"{item['id']}{item['title']}{item['url']}".encode()
            ).hexdigest()
            item["content_hash"] = content_hash
            
            return item
            
        except Exception as e:
            logger.warning(f"Error parsing RSS item: {e}")
            return None
    
    def _filter_items(self, items: List[Dict[str, Any]], channel: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Filter items by age and quality thresholds"""
        
        filtered_items = []
        
        # Get filtering settings
        max_items = self.feed_settings.get('max_items_per_feed', 10)
        age_limit_days = self.feed_settings.get('content_age_limit_days', 7)
        quality_threshold = self.feed_settings.get('quality_threshold', 0.7)
        
        # Calculate age cutoff
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=age_limit_days)
        
        for item in items:
            # Check content age
            if self._is_item_too_old(item, cutoff_date):
                continue
            
            # Check quality threshold (based on channel rating)
            channel_quality = channel.get('quality_rating', 4.0) / 5.0  # Normalize to 0-1
            if channel_quality < quality_threshold:
                continue
            
            # Add content age calculation
            item['content_age_days'] = self._calculate_item_age(item)
            
            filtered_items.append(item)
        
        # Limit number of items per feed
        filtered_items = filtered_items[:max_items]
        
        return filtered_items
    
    def _is_item_too_old(self, item: Dict[str, Any], cutoff_date: datetime) -> bool:
        """Check if item is too old based on published date"""
        
        published_date_str = item.get('published_date')
        if not published_date_str:
            return False  # Keep items without date info
        
        try:
            # Parse published date
            if published_date_str.endswith('Z'):
                published_date = datetime.fromisoformat(published_date_str.replace('Z', '+00:00'))
            elif '+' in published_date_str or 'T' in published_date_str:
                published_date = datetime.fromisoformat(published_date_str)
            else:
                # Handle RFC 2822 format (pubDate)
                from email.utils import parsedate_to_datetime
                published_date = parsedate_to_datetime(published_date_str)
            
            return published_date < cutoff_date
            
        except Exception as e:
            logger.warning(f"Error parsing date '{published_date_str}': {e}")
            return False  # Keep items with unparseable dates
    
    def _calculate_item_age(self, item: Dict[str, Any]) -> float:
        """Calculate item age in days"""
        
        published_date_str = item.get('published_date')
        if not published_date_str:
            return 999.0  # Very old for items without date
        
        try:
            # Parse published date
            if published_date_str.endswith('Z'):
                published_date = datetime.fromisoformat(published_date_str.replace('Z', '+00:00'))
            elif '+' in published_date_str or 'T' in published_date_str:
                published_date = datetime.fromisoformat(published_date_str)
            else:
                # Handle RFC 2822 format
                from email.utils import parsedate_to_datetime
                published_date = parsedate_to_datetime(published_date_str)
            
            # Calculate age in days
            now = datetime.now(timezone.utc)
            age_delta = now - published_date.replace(tzinfo=timezone.utc)
            return max(0.0, age_delta.total_seconds() / (24 * 3600))
            
        except Exception as e:
            logger.warning(f"Error calculating age for date '{published_date_str}': {e}")
            return 999.0
    
    def _save_channel_data(self, channel_id: str, items: List[Dict[str, Any]]) -> None:
        """Save channel data to file"""
        
        if not items:
            return
        
        # Create channel directory
        channel_dir = self.data_path / channel_id
        channel_dir.mkdir(parents=True, exist_ok=True)
        
        # Save with timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f"rss_feed_{timestamp}.json"
        filepath = channel_dir / filename
        
        data = {
            "channel_id": channel_id,
            "collected_at": datetime.now(timezone.utc).isoformat(),
            "item_count": len(items),
            "items": items
        }
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Also save as "latest" for easy access
        latest_filepath = channel_dir / "latest.json"
        with open(latest_filepath, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _save_collection_results(self, results: Dict[str, Any]) -> None:
        """Save collection results summary"""
        
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f"collection_results_{timestamp}.json"
        
        results_dir = self.data_path / "results"
        results_dir.mkdir(parents=True, exist_ok=True)
        
        filepath = results_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Also save as "latest"
        latest_filepath = results_dir / "latest_collection.json"
        with open(latest_filepath, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"Collection results saved to: {filepath}")
    
    def get_recent_items(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get all RSS items collected in the last N hours"""
        
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
        recent_items = []
        
        # Scan all channel directories
        for channel_dir in self.data_path.iterdir():
            if not channel_dir.is_dir() or channel_dir.name == "results":
                continue
            
            latest_file = channel_dir / "latest.json"
            if latest_file.exists():
                try:
                    with open(latest_file, 'r') as f:
                        data = json.load(f)
                    
                    # Check collection time
                    collected_at_str = data.get('collected_at')
                    if collected_at_str:
                        collected_at = datetime.fromisoformat(collected_at_str.replace('Z', '+00:00'))
                        if collected_at >= cutoff_time:
                            recent_items.extend(data.get('items', []))
                            
                except Exception as e:
                    logger.warning(f"Error reading {latest_file}: {e}")
        
        return recent_items
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about RSS feed collections"""
        
        stats = {
            "total_channels": len(self.config.get('channels', [])),
            "active_channels": 0,
            "total_items": 0,
            "last_collection": None,
            "channel_stats": {}
        }
        
        # Check latest collection results
        latest_results_file = self.data_path / "results" / "latest_collection.json"
        if latest_results_file.exists():
            try:
                with open(latest_results_file, 'r') as f:
                    latest_results = json.load(f)
                
                metadata = latest_results.get('collection_metadata', {})
                stats["last_collection"] = metadata.get('completed_at')
                stats["active_channels"] = metadata.get('successful_channels', 0)
                stats["total_items"] = metadata.get('total_items_collected', 0)
                
            except Exception as e:
                logger.warning(f"Error reading latest collection results: {e}")
        
        # Get per-channel stats
        for channel_dir in self.data_path.iterdir():
            if not channel_dir.is_dir() or channel_dir.name == "results":
                continue
            
            channel_id = channel_dir.name
            latest_file = channel_dir / "latest.json"
            
            if latest_file.exists():
                try:
                    with open(latest_file, 'r') as f:
                        data = json.load(f)
                    
                    stats["channel_stats"][channel_id] = {
                        "item_count": data.get('item_count', 0),
                        "last_collection": data.get('collected_at')
                    }
                    
                except Exception as e:
                    logger.warning(f"Error reading {latest_file}: {e}")
        
        return stats

def main():
    """Main function for testing RSS feed collection"""
    
    collector = RSSFeedCollector()
    
    print("🔄 RSS Feed Collector - Testing Mode")
    print("=" * 50)
    
    # Test collection
    results = collector.collect_all_feeds()
    
    # Show summary
    metadata = results.get('collection_metadata', {})
    print(f"\n📊 Collection Summary:")
    print(f"   Total channels: {metadata.get('total_channels', 0)}")
    print(f"   Successful: {metadata.get('successful_channels', 0)}")
    print(f"   Failed: {metadata.get('failed_channels', 0)}")
    print(f"   Total items: {metadata.get('total_items_collected', 0)}")
    print(f"   Duration: {metadata.get('duration_seconds', 0):.2f}s")
    
    # Show sample items
    recent_items = collector.get_recent_items(hours=24)
    if recent_items:
        print(f"\n📰 Sample Recent Items ({len(recent_items)} total):")
        for item in recent_items[:5]:
            age = item.get('content_age_days', 0)
            print(f"   • {item.get('title', 'Unknown')[:50]}... "
                  f"({item.get('channel_name', 'Unknown')}) - {age:.1f}d ago")
    
    # Show stats
    stats = collector.get_collection_stats()
    print(f"\n📈 System Stats:")
    print(f"   Active channels: {stats['active_channels']}/{stats['total_channels']}")
    print(f"   Total items collected: {stats['total_items']}")
    print(f"   Last collection: {stats.get('last_collection', 'Never')}")
    
    print(f"\n✅ RSS Feed Collection Test Complete!")

if __name__ == "__main__":
    main()