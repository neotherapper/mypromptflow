#!/usr/bin/env python3
"""
RSS Feed Validator
Comprehensive tool for validating RSS feed URLs and health status
"""

import asyncio
import aiohttp
import feedparser
import yaml
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from urllib.parse import urlparse
import logging
from dataclasses import dataclass
from pathlib import Path
import json
import time

@dataclass
class RSSValidationResult:
    """Result of RSS feed validation"""
    url: str
    source_id: str
    source_name: str
    is_valid: bool
    status_code: Optional[int] = None
    error_message: Optional[str] = None
    feed_title: Optional[str] = None
    last_updated: Optional[str] = None
    item_count: int = 0
    parse_warnings: Optional[str] = None
    suggested_fix: Optional[str] = None
    response_time_ms: float = 0.0
    content_type: Optional[str] = None
    redirect_url: Optional[str] = None

@dataclass
class RSSHealthReport:
    """Complete health report for RSS feeds"""
    total_feeds: int
    valid_feeds: int
    invalid_feeds: int
    success_rate: float
    validation_results: List[RSSValidationResult]
    validation_timestamp: str
    recommendations: List[str]

class RSSFeedValidator:
    """
    Comprehensive RSS feed validator for universal topic monitoring
    """
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize RSS feed validator"""
        self.config = config or {}
        
        # Validation settings
        self.timeout = self.config.get("timeout", 15)
        self.max_redirects = self.config.get("max_redirects", 3)
        self.user_agent = self.config.get("user_agent", self._default_user_agent())
        self.min_items_threshold = self.config.get("min_items_threshold", 1)
        self.max_age_days = self.config.get("max_age_days", 30)
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        # Known feed alternatives and fixes
        self.feed_alternatives = self._load_feed_alternatives()
        
    def _default_user_agent(self) -> str:
        """Default user agent for RSS requests"""
        return "UniversalTopicIntelligence/2.0 RSS Validator (+https://github.com/yourusername/universal-topic-intelligence)"
    
    def _load_feed_alternatives(self) -> Dict[str, List[str]]:
        """Load known feed alternatives and common fixes"""
        return {
            # Common feed path alternatives
            "feed_paths": [
                "/feed",
                "/feeds",
                "/rss",
                "/rss.xml",
                "/feed.xml", 
                "/atom.xml",
                "/blog/feed",
                "/blog/rss",
                "/news/rss",
                "/articles/feed"
            ],
            
            # Domain-specific known alternatives
            "domain_fixes": {
                "medium.com": ["/feed"],
                "substack.com": ["/feed"],
                "wordpress.com": ["/feed"],
                "blogspot.com": ["/feeds/posts/default"],
                "github.io": ["/feed.xml", "/atom.xml"]
            }
        }
    
    async def validate_single_feed(self, url: str, source_id: str, source_name: str) -> RSSValidationResult:
        """
        Validate a single RSS feed URL
        
        Args:
            url: RSS feed URL to validate
            source_id: Unique identifier for the source
            source_name: Human-readable source name
            
        Returns:
            RSSValidationResult with validation details
        """
        start_time = time.time()
        
        try:
            result = RSSValidationResult(
                url=url,
                source_id=source_id,
                source_name=source_name,
                is_valid=False
            )
            
            # Basic URL validation
            parsed_url = urlparse(url)
            if not parsed_url.scheme or not parsed_url.netloc:
                result.error_message = "Invalid URL format"
                result.suggested_fix = "Check URL format and protocol (http/https)"
                return result
            
            # HTTP request with proper headers
            headers = {
                'User-Agent': self.user_agent,
                'Accept': 'application/rss+xml, application/atom+xml, application/xml, text/xml, */*',
                'Accept-Encoding': 'gzip, deflate',
                'Cache-Control': 'no-cache'
            }
            
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.get(
                        url,
                        headers=headers,
                        timeout=aiohttp.ClientTimeout(total=self.timeout),
                        allow_redirects=True,
                        max_redirects=self.max_redirects
                    ) as response:
                        
                        result.status_code = response.status
                        result.content_type = response.headers.get('content-type', '')
                        result.response_time_ms = (time.time() - start_time) * 1000
                        
                        # Check for redirects
                        if len(response.history) > 0:
                            result.redirect_url = str(response.url)
                        
                        # Handle non-200 status codes
                        if response.status == 404:
                            result.error_message = "Feed not found (404)"
                            result.suggested_fix = await self._suggest_feed_alternative(url)
                            return result
                        elif response.status == 403:
                            result.error_message = "Access forbidden (403) - may require different user agent"
                            result.suggested_fix = "Try different user agent or check if authentication required"
                            return result
                        elif response.status >= 400:
                            result.error_message = f"HTTP error {response.status}"
                            result.suggested_fix = "Check if feed URL has changed or service is down"
                            return result
                        
                        # Read content
                        content = await response.text()
                        
                        # Parse RSS/Atom feed
                        feed = feedparser.parse(content)
                        
                        # Check for parse errors
                        if feed.bozo and hasattr(feed, 'bozo_exception'):
                            result.parse_warnings = str(feed.bozo_exception)
                            self.logger.warning(f"Parse warning for {source_name}: {result.parse_warnings}")
                        
                        # Validate feed structure
                        if not hasattr(feed, 'feed') or not feed.entries:
                            result.error_message = "No valid feed structure or entries found"
                            result.suggested_fix = "Check if URL returns valid RSS/Atom XML"
                            return result
                        
                        # Extract feed information
                        result.feed_title = getattr(feed.feed, 'title', 'Unknown')
                        result.item_count = len(feed.entries)
                        
                        # Check last update
                        if feed.entries:
                            latest_entry = feed.entries[0]
                            if hasattr(latest_entry, 'published_parsed') and latest_entry.published_parsed:
                                from time import mktime
                                latest_date = datetime.fromtimestamp(mktime(latest_entry.published_parsed))
                                result.last_updated = latest_date.isoformat()
                                
                                # Check if feed is stale
                                age_days = (datetime.now() - latest_date).days
                                if age_days > self.max_age_days:
                                    result.parse_warnings = f"Feed appears stale (last update {age_days} days ago)"
                        
                        # Validation passed
                        if result.item_count >= self.min_items_threshold:
                            result.is_valid = True
                        else:
                            result.error_message = f"Feed has too few items ({result.item_count} < {self.min_items_threshold})"
                        
                        return result
                        
                except asyncio.TimeoutError:
                    result.error_message = f"Request timeout ({self.timeout}s)"
                    result.suggested_fix = "Feed server may be slow or unresponsive"
                    return result
                    
                except aiohttp.ClientError as e:
                    result.error_message = f"Connection error: {str(e)}"
                    result.suggested_fix = "Check network connectivity and DNS resolution"
                    return result
                    
        except Exception as e:
            result.error_message = f"Unexpected error: {str(e)}"
            result.suggested_fix = "Manual inspection required"
            return result
    
    async def _suggest_feed_alternative(self, original_url: str) -> str:
        """
        Suggest alternative feed URLs based on domain and common patterns
        
        Args:
            original_url: Original failing URL
            
        Returns:
            Suggested alternative URL or generic advice
        """
        parsed = urlparse(original_url)
        domain = parsed.netloc
        
        # Check domain-specific fixes
        for known_domain, alternatives in self.feed_alternatives["domain_fixes"].items():
            if known_domain in domain:
                alt_url = f"{parsed.scheme}://{domain}{alternatives[0]}"
                return f"Try domain-specific alternative: {alt_url}"
        
        # Suggest common feed paths
        common_paths = self.feed_alternatives["feed_paths"][:3]  # Top 3 alternatives
        suggestions = [f"{parsed.scheme}://{domain}{path}" for path in common_paths]
        
        return f"Try common alternatives: {', '.join(suggestions)}"
    
    async def validate_topic_configuration(self, config_path: str) -> RSSHealthReport:
        """
        Validate all RSS feeds in a topic configuration file
        
        Args:
            config_path: Path to YAML topic configuration file
            
        Returns:
            RSSHealthReport with complete validation results
        """
        self.logger.info(f"Validating RSS feeds in topic configuration: {config_path}")
        
        # Load configuration
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
        except Exception as e:
            raise ValueError(f"Failed to load configuration file: {e}")
        
        # Extract RSS sources
        rss_sources = []
        source_mapping = config.get('source_mapping', {})
        
        for tier_name, tier_config in source_mapping.items():
            sources = tier_config.get('sources', [])
            for source in sources:
                if source.get('monitoring_method') == 'RSS' and 'url' in source:
                    rss_sources.append({
                        'url': source['url'],
                        'source_id': source.get('source_id', source['url']),
                        'name': source.get('name', f"Source from {tier_name}")
                    })
        
        if not rss_sources:
            self.logger.warning("No RSS sources found in configuration")
            return RSSHealthReport(
                total_feeds=0,
                valid_feeds=0,
                invalid_feeds=0,
                success_rate=0.0,
                validation_results=[],
                validation_timestamp=datetime.now().isoformat(),
                recommendations=["No RSS feeds found in configuration"]
            )
        
        # Validate all RSS sources
        validation_tasks = [
            self.validate_single_feed(source['url'], source['source_id'], source['name'])
            for source in rss_sources
        ]
        
        self.logger.info(f"Validating {len(rss_sources)} RSS feeds...")
        results = await asyncio.gather(*validation_tasks)
        
        # Calculate statistics
        total_feeds = len(results)
        valid_feeds = sum(1 for r in results if r.is_valid)
        invalid_feeds = total_feeds - valid_feeds
        success_rate = (valid_feeds / total_feeds) * 100 if total_feeds > 0 else 0
        
        # Generate recommendations
        recommendations = self._generate_recommendations(results)
        
        self.logger.info(f"Validation complete: {valid_feeds}/{total_feeds} feeds valid ({success_rate:.1f}%)")
        
        return RSSHealthReport(
            total_feeds=total_feeds,
            valid_feeds=valid_feeds,
            invalid_feeds=invalid_feeds,
            success_rate=success_rate,
            validation_results=results,
            validation_timestamp=datetime.now().isoformat(),
            recommendations=recommendations
        )
    
    def _generate_recommendations(self, results: List[RSSValidationResult]) -> List[str]:
        """
        Generate actionable recommendations based on validation results
        
        Args:
            results: List of validation results
            
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        # Count common issues
        status_404_count = sum(1 for r in results if r.status_code == 404)
        status_403_count = sum(1 for r in results if r.status_code == 403)
        timeout_count = sum(1 for r in results if "timeout" in (r.error_message or "").lower())
        parse_error_count = sum(1 for r in results if r.parse_warnings)
        stale_feeds = sum(1 for r in results if r.parse_warnings and "stale" in r.parse_warnings)
        
        # Generate specific recommendations
        if status_404_count > 0:
            recommendations.append(f"Found {status_404_count} feeds with 404 errors - check suggested alternatives")
        
        if status_403_count > 0:
            recommendations.append(f"Found {status_403_count} feeds with 403 errors - may need authentication or different user agent")
        
        if timeout_count > 0:
            recommendations.append(f"Found {timeout_count} feeds with timeout issues - consider increasing timeout or removing slow feeds")
        
        if parse_error_count > 0:
            recommendations.append(f"Found {parse_error_count} feeds with parse warnings - check XML validity")
        
        if stale_feeds > 0:
            recommendations.append(f"Found {stale_feeds} stale feeds - consider removing inactive sources")
        
        # General recommendations
        invalid_count = sum(1 for r in results if not r.is_valid)
        if invalid_count > len(results) * 0.3:  # More than 30% invalid
            recommendations.append("High failure rate detected - consider comprehensive feed URL review")
        
        if not recommendations:
            recommendations.append("All feeds validated successfully - no immediate action required")
        
        return recommendations
    
    def save_validation_report(self, report: RSSHealthReport, output_path: str):
        """
        Save validation report to JSON file
        
        Args:
            report: RSS health report to save
            output_path: Path to save the report
        """
        # Convert dataclass to dict for JSON serialization
        report_dict = {
            'total_feeds': report.total_feeds,
            'valid_feeds': report.valid_feeds,
            'invalid_feeds': report.invalid_feeds,
            'success_rate': report.success_rate,
            'validation_timestamp': report.validation_timestamp,
            'recommendations': report.recommendations,
            'validation_results': [
                {
                    'url': r.url,
                    'source_id': r.source_id,
                    'source_name': r.source_name,
                    'is_valid': r.is_valid,
                    'status_code': r.status_code,
                    'error_message': r.error_message,
                    'feed_title': r.feed_title,
                    'last_updated': r.last_updated,
                    'item_count': r.item_count,
                    'parse_warnings': r.parse_warnings,
                    'suggested_fix': r.suggested_fix,
                    'response_time_ms': r.response_time_ms,
                    'content_type': r.content_type,
                    'redirect_url': r.redirect_url
                }
                for r in report.validation_results
            ]
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report_dict, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Validation report saved to: {output_path}")
    
    def print_validation_summary(self, report: RSSHealthReport):
        """
        Print formatted validation summary to console
        
        Args:
            report: RSS health report to display
        """
        print("\n" + "="*80)
        print("RSS FEED VALIDATION REPORT")
        print("="*80)
        print(f"Validation Time: {report.validation_timestamp}")
        print(f"Total Feeds: {report.total_feeds}")
        print(f"Valid Feeds: {report.valid_feeds}")
        print(f"Invalid Feeds: {report.invalid_feeds}")
        print(f"Success Rate: {report.success_rate:.1f}%")
        
        print("\n" + "-"*80)
        print("FAILED FEEDS:")
        print("-"*80)
        
        failed_feeds = [r for r in report.validation_results if not r.is_valid]
        
        if not failed_feeds:
            print("✅ All feeds are valid!")
        else:
            for result in failed_feeds:
                print(f"\n❌ {result.source_name}")
                print(f"   URL: {result.url}")
                print(f"   Error: {result.error_message}")
                if result.suggested_fix:
                    print(f"   Suggested Fix: {result.suggested_fix}")
                if result.status_code:
                    print(f"   Status Code: {result.status_code}")
        
        print("\n" + "-"*80)
        print("RECOMMENDATIONS:")
        print("-"*80)
        for i, rec in enumerate(report.recommendations, 1):
            print(f"{i}. {rec}")
        
        print("\n" + "="*80)


async def main():
    """
    CLI interface for RSS feed validation
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Validate RSS feeds in topic configurations')
    parser.add_argument('config_path', help='Path to topic configuration YAML file')
    parser.add_argument('--output', '-o', help='Path to save validation report (JSON)')
    parser.add_argument('--timeout', '-t', type=int, default=15, help='Request timeout in seconds')
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress console output')
    
    args = parser.parse_args()
    
    # Initialize validator
    config = {
        'timeout': args.timeout,
    }
    validator = RSSFeedValidator(config)
    
    # Run validation
    try:
        report = await validator.validate_topic_configuration(args.config_path)
        
        # Print summary if not quiet
        if not args.quiet:
            validator.print_validation_summary(report)
        
        # Save report if output path specified
        if args.output:
            validator.save_validation_report(report, args.output)
            
        # Exit with appropriate code
        exit_code = 0 if report.success_rate >= 80 else 1
        exit(exit_code)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    import sys
    asyncio.run(main())