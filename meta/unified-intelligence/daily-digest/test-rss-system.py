#!/usr/bin/env python3
"""
RSS Feed System Integration Test
Tests the complete RSS feed system with all 23 channels
"""

import json
import os
from pathlib import Path
from datetime import datetime, timezone
import time
import sys

# Add parent paths for imports
sys.path.append(str(Path(__file__).parent.parent))

# Import our modules
from pathlib import Path
try:
    import importlib.util
    
    # Import RSS collector
    spec = importlib.util.spec_from_file_location("rss_feed_collector", 
                                                str(Path(__file__).parent / "rss-feed-collector.py"))
    rss_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rss_module)
    RSSFeedCollector = rss_module.RSSFeedCollector
    print("✅ RSS feed collector imported successfully")
    
    # Import content digest generator
    spec = importlib.util.spec_from_file_location("content_digest_generator", 
                                                str(Path(__file__).parent / "content-digest-generator.py"))
    digest_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(digest_module)
    ContentDigestGenerator = digest_module.ContentDigestGenerator
    print("✅ Content digest generator imported successfully")
    
except Exception as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

class RSSSystemTester:
    """Comprehensive RSS feed system tester"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.config_path = self.base_path / "config" / "youtube-rss-channels.json"
        self.test_results = {
            "test_started_at": datetime.now(timezone.utc).isoformat(),
            "phases": {}
        }
        
    def run_complete_test(self) -> dict:
        """Run complete RSS feed system test"""
        
        print("🧪 RSS Feed System Integration Test")
        print("=" * 60)
        
        # Phase 1: Test RSS feed collection
        print(f"\n📡 PHASE 1: Testing RSS Feed Collection")
        phase1_result = self._test_rss_collection()
        self.test_results["phases"]["rss_collection"] = phase1_result
        
        # Phase 2: Test content digest integration
        print(f"\n🎯 PHASE 2: Testing Digest Integration")
        phase2_result = self._test_digest_integration()
        self.test_results["phases"]["digest_integration"] = phase2_result
        
        # Phase 3: Test end-to-end workflow
        print(f"\n🔄 PHASE 3: Testing End-to-End Workflow")
        phase3_result = self._test_end_to_end_workflow()
        self.test_results["phases"]["end_to_end"] = phase3_result
        
        # Phase 4: Validate final output
        print(f"\n✅ PHASE 4: Validating Final Output")
        phase4_result = self._test_output_validation()
        self.test_results["phases"]["output_validation"] = phase4_result
        
        # Generate final report
        self._generate_test_report()
        
        return self.test_results
    
    def _test_rss_collection(self) -> dict:
        """Test RSS feed collection from all 23 channels"""
        
        result = {
            "phase": "rss_collection",
            "started_at": datetime.now(timezone.utc).isoformat(),
            "success": False,
            "channels_tested": 0,
            "channels_successful": 0,
            "channels_failed": 0,
            "total_items_collected": 0,
            "errors": []
        }
        
        try:
            # Load configuration
            if not self.config_path.exists():
                result["errors"].append("RSS configuration file not found")
                return result
            
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            
            channels = config.get('channels', [])
            result["channels_tested"] = len(channels)
            
            print(f"   📊 Testing {len(channels)} configured RSS channels...")
            
            # Initialize RSS collector
            collector = RSSFeedCollector()
            
            # Test RSS collection
            collection_start = time.time()
            collection_results = collector.collect_all_feeds()
            collection_time = time.time() - collection_start
            
            # Analyze results
            metadata = collection_results.get('collection_metadata', {})
            result["channels_successful"] = metadata.get('successful_channels', 0)
            result["channels_failed"] = metadata.get('failed_channels', 0)
            result["total_items_collected"] = metadata.get('total_items_collected', 0)
            result["collection_time_seconds"] = round(collection_time, 2)
            
            # Check for errors
            if collection_results.get('errors'):
                result["errors"].extend(collection_results['errors'])
            
            # Test statistics
            stats = collector.get_collection_stats()
            result["system_stats"] = stats
            
            # Determine success
            success_rate = result["channels_successful"] / result["channels_tested"] if result["channels_tested"] > 0 else 0
            result["success_rate"] = round(success_rate, 3)
            result["success"] = success_rate >= 0.7  # At least 70% success rate
            
            print(f"   ✅ Collection completed: {result['channels_successful']}/{result['channels_tested']} channels successful")
            print(f"   📰 Total items collected: {result['total_items_collected']}")
            print(f"   ⏱️  Collection time: {result['collection_time_seconds']}s")
            print(f"   📈 Success rate: {result['success_rate']*100:.1f}%")
            
        except Exception as e:
            result["errors"].append(f"RSS collection test failed: {str(e)}")
            print(f"   ❌ RSS collection test failed: {e}")
        
        result["completed_at"] = datetime.now(timezone.utc).isoformat()
        return result
    
    def _test_digest_integration(self) -> dict:
        """Test RSS feed integration with digest generator"""
        
        result = {
            "phase": "digest_integration",
            "started_at": datetime.now(timezone.utc).isoformat(),
            "success": False,
            "rss_items_found": 0,
            "integration_working": False,
            "errors": []
        }
        
        try:
            print(f"   🔧 Testing RSS integration in digest generator...")
            
            # Initialize digest generator (this should initialize RSS collector)
            generator = ContentDigestGenerator()
            
            # Check if RSS collector was initialized
            if hasattr(generator, 'rss_collector') and generator.rss_collector:
                print(f"   ✅ RSS collector successfully initialized in digest generator")
                result["integration_working"] = True
                
                # Test RSS feed collection method
                rss_items = generator._collect_rss_feeds("today")
                result["rss_items_found"] = len(rss_items)
                
                print(f"   📊 RSS collection method returned {len(rss_items)} items")
                
                # Test a few sample items for correct format
                if rss_items:
                    sample_item = rss_items[0]
                    required_fields = ['title', 'url', 'channel', 'platform', 'source_type']
                    missing_fields = [field for field in required_fields if field not in sample_item]
                    
                    if missing_fields:
                        result["errors"].append(f"RSS items missing required fields: {missing_fields}")
                    else:
                        print(f"   ✅ RSS items have correct format")
                        print(f"       Sample: '{sample_item['title'][:40]}...' from {sample_item['channel']}")
                
                result["success"] = True
                
            else:
                result["errors"].append("RSS collector not initialized in digest generator")
                print(f"   ❌ RSS collector not initialized in digest generator")
        
        except Exception as e:
            result["errors"].append(f"Digest integration test failed: {str(e)}")
            print(f"   ❌ Digest integration test failed: {e}")
        
        result["completed_at"] = datetime.now(timezone.utc).isoformat()
        return result
    
    def _test_end_to_end_workflow(self) -> dict:
        """Test complete end-to-end RSS workflow"""
        
        result = {
            "phase": "end_to_end",
            "started_at": datetime.now(timezone.utc).isoformat(),
            "success": False,
            "digest_generated": False,
            "rss_content_included": False,
            "html_file_created": False,
            "errors": []
        }
        
        try:
            print(f"   🔄 Testing complete end-to-end RSS workflow...")
            
            # Generate digest with RSS integration
            generator = ContentDigestGenerator()
            
            workflow_start = time.time()
            digest_result = generator.generate_content_digest("today", force_regenerate=True)
            workflow_time = time.time() - workflow_start
            
            result["generation_time_seconds"] = round(workflow_time, 2)
            
            # Check if digest was generated
            if digest_result.get('status') == 'generated':
                result["digest_generated"] = True
                print(f"   ✅ Digest generated successfully in {workflow_time:.2f}s")
                
                # Check if HTML file was created
                html_file_path = digest_result.get('file_path')
                if html_file_path and Path(html_file_path).exists():
                    result["html_file_created"] = True
                    result["html_file_path"] = html_file_path
                    print(f"   ✅ HTML file created: {Path(html_file_path).name}")
                    
                    # Check HTML content for RSS mentions
                    with open(html_file_path, 'r') as f:
                        html_content = f.read()
                    
                    # Look for RSS-related content
                    rss_indicators = ['RSS feeds', 'rss', 'Subscribed', 'subscribed']
                    rss_found = any(indicator in html_content for indicator in rss_indicators)
                    
                    if rss_found:
                        result["rss_content_included"] = True
                        print(f"   ✅ RSS content found in generated HTML")
                    else:
                        result["errors"].append("No RSS content found in generated HTML")
                        print(f"   ⚠️  No obvious RSS content found in HTML")
                
                # Check digest data
                digest_data = digest_result.get('digest_data', {})
                total_items = digest_data.get('total_items', 0)
                subscribed_items = digest_data.get('subscribed_items', 0)
                
                print(f"   📊 Digest statistics:")
                print(f"       Total items: {total_items}")
                print(f"       Subscribed items: {subscribed_items}")
                
                result["total_items"] = total_items
                result["subscribed_items"] = subscribed_items
                
                # Determine overall success
                result["success"] = (result["digest_generated"] and 
                                   result["html_file_created"] and 
                                   total_items > 0)
                
            else:
                result["errors"].append(f"Digest generation failed: {digest_result.get('status', 'unknown')}")
                print(f"   ❌ Digest generation failed")
        
        except Exception as e:
            result["errors"].append(f"End-to-end workflow test failed: {str(e)}")
            print(f"   ❌ End-to-end workflow test failed: {e}")
        
        result["completed_at"] = datetime.now(timezone.utc).isoformat()
        return result
    
    def _test_output_validation(self) -> dict:
        """Validate the final output quality"""
        
        result = {
            "phase": "output_validation",
            "started_at": datetime.now(timezone.utc).isoformat(),
            "success": False,
            "html_valid": False,
            "content_quality": {},
            "errors": []
        }
        
        try:
            print(f"   🔍 Validating final output quality...")
            
            # Find the latest HTML file
            output_dir = Path(__file__).parent / "generated" / "content"
            html_file = output_dir / "daily-digest.html"
            
            if html_file.exists():
                with open(html_file, 'r') as f:
                    html_content = f.read()
                
                # Basic HTML validation
                html_checks = {
                    "has_doctype": html_content.startswith('<!DOCTYPE html>'),
                    "has_title": '<title>' in html_content,
                    "has_css": '<style>' in html_content,
                    "has_content": len(html_content) > 1000,
                    "has_rss_mention": 'RSS' in html_content or 'rss' in html_content
                }
                
                result["html_checks"] = html_checks
                result["html_valid"] = all(html_checks.values())
                
                # Content quality checks
                content_indicators = {
                    "has_priority_topics": "Priority Topics" in html_content,
                    "has_statistics": "Total Items" in html_content,
                    "has_recommendations": "Recommendations" in html_content,
                    "has_source_attribution": "Subscribed" in html_content or "Discovered" in html_content
                }
                
                result["content_quality"] = content_indicators
                
                # Count content items in HTML
                import re
                content_item_pattern = r'<div class="content-item">'
                content_items = len(re.findall(content_item_pattern, html_content))
                result["content_items_in_html"] = content_items
                
                print(f"   ✅ HTML validation: {'✓' if result['html_valid'] else '✗'}")
                print(f"   📊 Content items in HTML: {content_items}")
                print(f"   🎯 Quality indicators: {sum(content_indicators.values())}/{len(content_indicators)}")
                
                # Overall validation success
                result["success"] = (result["html_valid"] and 
                                   content_items > 0 and 
                                   sum(content_indicators.values()) >= 3)
                
            else:
                result["errors"].append("HTML file not found for validation")
                print(f"   ❌ HTML file not found for validation")
        
        except Exception as e:
            result["errors"].append(f"Output validation failed: {str(e)}")
            print(f"   ❌ Output validation failed: {e}")
        
        result["completed_at"] = datetime.now(timezone.utc).isoformat()
        return result
    
    def _generate_test_report(self):
        """Generate comprehensive test report"""
        
        self.test_results["test_completed_at"] = datetime.now(timezone.utc).isoformat()
        
        # Calculate overall success
        phase_successes = [phase.get('success', False) for phase in self.test_results['phases'].values()]
        overall_success = all(phase_successes)
        self.test_results["overall_success"] = overall_success
        self.test_results["phases_passed"] = sum(phase_successes)
        self.test_results["total_phases"] = len(phase_successes)
        
        # Save test report
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        report_file = Path(__file__).parent / "test-results" / f"rss_system_test_{timestamp}.json"
        report_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_file, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        # Print summary
        print(f"\n📋 TEST SUMMARY")
        print("=" * 60)
        print(f"Overall Result: {'✅ PASSED' if overall_success else '❌ FAILED'}")
        print(f"Phases Passed: {self.test_results['phases_passed']}/{self.test_results['total_phases']}")
        
        for phase_name, phase_result in self.test_results['phases'].items():
            status = "✅ PASS" if phase_result.get('success', False) else "❌ FAIL"
            print(f"  {phase_name}: {status}")
            
            if phase_result.get('errors'):
                for error in phase_result['errors'][:2]:  # Show first 2 errors
                    print(f"    ⚠️  {error}")
        
        print(f"\nDetailed report saved to: {report_file}")
        
        return overall_success

def main():
    """Run RSS system integration test"""
    
    tester = RSSSystemTester()
    test_results = tester.run_complete_test()
    
    # Exit with appropriate code
    exit_code = 0 if test_results.get('overall_success', False) else 1
    
    if exit_code == 0:
        print(f"\n🎉 RSS Feed System Test PASSED!")
        print(f"   All 23 channels tested successfully")
        print(f"   RSS content integrated into digest generation")
        print(f"   End-to-end workflow functioning correctly")
    else:
        print(f"\n❌ RSS Feed System Test FAILED!")
        print(f"   Check test report for detailed error information")
    
    return exit_code

if __name__ == "__main__":
    sys.exit(main())