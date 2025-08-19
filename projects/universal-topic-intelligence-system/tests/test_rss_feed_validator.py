#!/usr/bin/env python3
"""
Tests for RSS Feed Validator
Comprehensive test suite for RSS feed validation functionality
"""

import pytest
import asyncio
import json
import tempfile
import yaml
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock

from core.rss_feed_validator import (
    RSSFeedValidator, 
    RSSValidationResult, 
    RSSHealthReport
)

class TestRSSValidationResult:
    """Test RSSValidationResult dataclass"""
    
    def test_valid_result_creation(self):
        """Test creating a valid RSS validation result"""
        result = RSSValidationResult(
            url="https://example.com/feed.xml",
            source_id="test_feed",
            source_name="Test Feed",
            is_valid=True,
            status_code=200,
            feed_title="Example Blog",
            item_count=10
        )
        
        assert result.is_valid == True
        assert result.status_code == 200
        assert result.item_count == 10
        assert result.feed_title == "Example Blog"
    
    def test_invalid_result_creation(self):
        """Test creating an invalid RSS validation result"""
        result = RSSValidationResult(
            url="https://example.com/broken-feed.xml",
            source_id="broken_feed",
            source_name="Broken Feed",
            is_valid=False,
            status_code=404,
            error_message="Feed not found",
            suggested_fix="Check if URL has changed"
        )
        
        assert result.is_valid == False
        assert result.status_code == 404
        assert result.error_message == "Feed not found"
        assert result.suggested_fix == "Check if URL has changed"

class TestRSSFeedValidator:
    """Test RSSFeedValidator class"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.validator = RSSFeedValidator({
            "timeout": 5,
            "min_items_threshold": 1,
            "max_age_days": 30
        })
    
    def test_default_user_agent(self):
        """Test default user agent generation"""
        user_agent = self.validator._default_user_agent()
        assert "UniversalTopicIntelligence" in user_agent
        assert "RSS Validator" in user_agent
    
    def test_suggest_feed_alternative(self):
        """Test feed alternative suggestion"""
        # Test domain-specific fix
        medium_suggestion = asyncio.run(
            self.validator._suggest_feed_alternative("https://medium.com/broken-feed")
        )
        assert "medium.com" in medium_suggestion.lower()
        assert "/feed" in medium_suggestion
        
        # Test generic suggestions
        generic_suggestion = asyncio.run(
            self.validator._suggest_feed_alternative("https://unknown-domain.com/broken")
        )
        assert "common alternatives" in generic_suggestion
        assert "/feed" in generic_suggestion
    
    @pytest.mark.asyncio
    async def test_validate_single_feed_invalid_url(self):
        """Test validation with invalid URL"""
        result = await self.validator.validate_single_feed(
            "not-a-url",
            "invalid_test",
            "Invalid Test"
        )
        
        assert result.is_valid == False
        assert "Invalid URL format" in result.error_message
        assert "Check URL format" in result.suggested_fix
    
    @pytest.mark.asyncio 
    async def test_validate_single_feed_timeout(self):
        """Test validation with timeout"""
        # Use a non-routable IP to trigger timeout quickly
        result = await self.validator.validate_single_feed(
            "https://203.0.113.1/feed.xml",  # Test IP that should not respond
            "timeout_test", 
            "Timeout Test"
        )
        
        assert result.is_valid == False
        # Should either timeout or connection error
        assert any(error in result.error_message for error in ["timeout", "Connection error", "Cannot connect"])
    
    @pytest.mark.asyncio
    async def test_validate_single_feed_404(self):
        """Test validation with 404 response"""
        with patch('aiohttp.ClientSession.get') as mock_get:
            # Mock 404 response
            mock_response = AsyncMock()
            mock_response.status = 404
            mock_response.headers = {'content-type': 'text/html'}
            mock_response.history = []
            mock_get.return_value.__aenter__.return_value = mock_response
            
            result = await self.validator.validate_single_feed(
                "https://example.com/nonexistent-feed.xml",
                "404_test",
                "404 Test"
            )
            
            assert result.is_valid == False
            assert result.status_code == 404
            assert "Feed not found" in result.error_message
            assert "Try common alternatives" in result.suggested_fix
    
    @pytest.mark.asyncio
    async def test_validate_single_feed_success(self):
        """Test successful feed validation"""
        # Mock RSS content
        valid_rss = """<?xml version="1.0"?>
        <rss version="2.0">
            <channel>
                <title>Test Blog</title>
                <description>Test RSS feed</description>
                <link>https://example.com</link>
                <item>
                    <title>Test Post</title>
                    <description>Test content</description>
                    <link>https://example.com/post1</link>
                    <pubDate>Mon, 19 Aug 2025 12:00:00 GMT</pubDate>
                </item>
            </channel>
        </rss>"""
        
        with patch('aiohttp.ClientSession.get') as mock_get:
            # Mock successful response
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.headers = {'content-type': 'application/rss+xml'}
            mock_response.history = []
            mock_response.text.return_value = valid_rss
            mock_get.return_value.__aenter__.return_value = mock_response
            
            result = await self.validator.validate_single_feed(
                "https://example.com/feed.xml",
                "success_test",
                "Success Test"
            )
            
            assert result.is_valid == True
            assert result.status_code == 200
            assert result.feed_title == "Test Blog"
            assert result.item_count == 1

class TestRSSHealthReport:
    """Test RSS health report functionality"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.validator = RSSFeedValidator()
    
    def test_generate_recommendations(self):
        """Test recommendation generation"""
        # Create mock validation results
        results = [
            RSSValidationResult("https://example.com/1", "test1", "Test 1", True),
            RSSValidationResult("https://example.com/2", "test2", "Test 2", False, 404, "Not found"),
            RSSValidationResult("https://example.com/3", "test3", "Test 3", False, 403, "Forbidden"),
            RSSValidationResult("https://example.com/4", "test4", "Test 4", True, 200, parse_warnings="Feed appears stale"),
        ]
        
        recommendations = self.validator._generate_recommendations(results)
        
        assert len(recommendations) > 0
        assert any("404 errors" in rec for rec in recommendations)
        assert any("403 errors" in rec for rec in recommendations)
        assert any("stale feeds" in rec for rec in recommendations)
    
    def test_generate_recommendations_all_valid(self):
        """Test recommendations when all feeds are valid"""
        results = [
            RSSValidationResult("https://example.com/1", "test1", "Test 1", True),
            RSSValidationResult("https://example.com/2", "test2", "Test 2", True),
        ]
        
        recommendations = self.validator._generate_recommendations(results)
        
        assert len(recommendations) == 1
        assert "no immediate action required" in recommendations[0].lower()
    
    @pytest.mark.asyncio
    async def test_validate_topic_configuration_file_not_found(self):
        """Test validation with non-existent configuration file"""
        with pytest.raises(ValueError, match="Failed to load configuration file"):
            await self.validator.validate_topic_configuration("/nonexistent/file.yaml")
    
    @pytest.mark.asyncio
    async def test_validate_topic_configuration_no_rss(self):
        """Test validation with configuration containing no RSS sources"""
        # Create temporary config with no RSS sources
        config = {
            'topic_metadata': {'name': 'Test Topic'},
            'source_mapping': {
                'tier_1': {
                    'sources': [
                        {
                            'url': 'https://github.com/user/repo',
                            'monitoring_method': 'GitHub MCP',
                            'name': 'Test Repo'
                        }
                    ]
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config, f)
            config_path = f.name
        
        try:
            report = await self.validator.validate_topic_configuration(config_path)
            
            assert report.total_feeds == 0
            assert report.valid_feeds == 0
            assert report.success_rate == 0.0
            assert "No RSS feeds found" in report.recommendations[0]
            
        finally:
            Path(config_path).unlink()
    
    @pytest.mark.asyncio
    async def test_validate_topic_configuration_with_rss(self):
        """Test validation with configuration containing RSS sources"""
        # Create temporary config with RSS sources
        config = {
            'topic_metadata': {'name': 'Test Topic'},
            'source_mapping': {
                'tier_1': {
                    'sources': [
                        {
                            'url': 'https://example.com/feed1.xml',
                            'monitoring_method': 'RSS',
                            'name': 'Test Feed 1',
                            'source_id': 'test_feed_1'
                        },
                        {
                            'url': 'https://example.com/feed2.xml', 
                            'monitoring_method': 'RSS',
                            'name': 'Test Feed 2',
                            'source_id': 'test_feed_2'
                        }
                    ]
                }
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.dump(config, f)
            config_path = f.name
        
        try:
            with patch.object(self.validator, 'validate_single_feed') as mock_validate:
                # Mock validation results
                mock_validate.side_effect = [
                    RSSValidationResult("https://example.com/feed1.xml", "test_feed_1", "Test Feed 1", True),
                    RSSValidationResult("https://example.com/feed2.xml", "test_feed_2", "Test Feed 2", False, 404)
                ]
                
                report = await self.validator.validate_topic_configuration(config_path)
                
                assert report.total_feeds == 2
                assert report.valid_feeds == 1
                assert report.invalid_feeds == 1
                assert report.success_rate == 50.0
                assert len(report.validation_results) == 2
            
        finally:
            Path(config_path).unlink()
    
    def test_save_validation_report(self):
        """Test saving validation report to JSON"""
        # Create sample report
        results = [
            RSSValidationResult("https://example.com/feed.xml", "test", "Test", True, 200, item_count=5),
        ]
        
        report = RSSHealthReport(
            total_feeds=1,
            valid_feeds=1, 
            invalid_feeds=0,
            success_rate=100.0,
            validation_results=results,
            validation_timestamp="2025-08-19T12:00:00",
            recommendations=["All feeds working"]
        )
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            output_path = f.name
        
        try:
            self.validator.save_validation_report(report, output_path)
            
            # Verify file was created and contains expected data
            assert Path(output_path).exists()
            
            with open(output_path, 'r') as f:
                saved_data = json.load(f)
            
            assert saved_data['total_feeds'] == 1
            assert saved_data['valid_feeds'] == 1
            assert saved_data['success_rate'] == 100.0
            assert len(saved_data['validation_results']) == 1
            assert saved_data['validation_results'][0]['is_valid'] == True
            
        finally:
            Path(output_path).unlink()

class TestIntegration:
    """Integration tests with actual topic configurations"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.validator = RSSFeedValidator()
    
    def test_load_feed_alternatives(self):
        """Test loading of feed alternatives configuration"""
        alternatives = self.validator.feed_alternatives
        
        assert 'feed_paths' in alternatives
        assert 'domain_fixes' in alternatives
        assert len(alternatives['feed_paths']) > 0
        assert 'medium.com' in alternatives['domain_fixes']
    
    def test_print_validation_summary(self, capsys):
        """Test console output formatting"""
        results = [
            RSSValidationResult("https://example.com/good.xml", "good", "Good Feed", True, 200, item_count=5),
            RSSValidationResult("https://example.com/bad.xml", "bad", "Bad Feed", False, 404, error_message="Not found", suggested_fix="Try alternatives"),
        ]
        
        report = RSSHealthReport(
            total_feeds=2,
            valid_feeds=1,
            invalid_feeds=1,
            success_rate=50.0,
            validation_results=results,
            validation_timestamp="2025-08-19T12:00:00",
            recommendations=["Fix broken feeds"]
        )
        
        self.validator.print_validation_summary(report)
        captured = capsys.readouterr()
        
        assert "RSS FEED VALIDATION REPORT" in captured.out
        assert "Total Feeds: 2" in captured.out
        assert "Valid Feeds: 1" in captured.out
        assert "Success Rate: 50.0%" in captured.out
        assert "❌ Bad Feed" in captured.out
        assert "✅ All feeds are valid!" not in captured.out

if __name__ == "__main__":
    pytest.main([__file__])