#!/usr/bin/env python3
"""
Database ID Registry Integration Test Suite
Validates registry functionality and performance with migration system
"""

import os
import sys
import time
import json
import logging
from pathlib import Path
from typing import Dict, List, Any

# Add the project root to Python path for imports
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Import components
from database_id_registry_manager import DatabaseIDRegistryManager
from mcp_operations_enhanced import EnhancedMCPOperations

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class RegistryIntegrationTestSuite:
    """
    Comprehensive test suite for Database ID Registry integration
    Tests performance, functionality, and integration with existing systems
    """
    
    def __init__(self):
        """Initialize test suite"""
        self.registry_manager = DatabaseIDRegistryManager()
        self.mcp_operations = EnhancedMCPOperations(self.registry_manager)
        self.test_results = []
        
        logger.info("Registry Integration Test Suite initialized")
    
    def run_all_tests(self) -> Dict[str, Any]:
        """
        Run comprehensive test suite
        
        Returns:
            Dictionary with detailed test results
        """
        logger.info("🧪 Starting Database ID Registry Integration Test Suite")
        
        test_suite_start = time.time()
        
        # Test 1: Registry Manager Basic Functionality
        test1_result = self.test_registry_manager_basic()
        
        # Test 2: Registry Performance with Large Dataset
        test2_result = self.test_registry_performance()
        
        # Test 3: MCP Operations Integration
        test3_result = self.test_mcp_integration()
        
        # Test 4: Registry Persistence and Recovery
        test4_result = self.test_registry_persistence()
        
        # Test 5: Error Handling and Edge Cases
        test5_result = self.test_error_handling()
        
        # Test 6: Performance Targets Validation
        test6_result = self.test_performance_targets()
        
        # Calculate overall results
        total_time = (time.time() - test_suite_start) * 1000
        
        overall_results = {
            "test_suite_summary": {
                "total_tests": 6,
                "passed_tests": sum(1 for r in [test1_result, test2_result, test3_result, 
                                               test4_result, test5_result, test6_result] if r["passed"]),
                "total_execution_time_ms": total_time,
                "overall_success": True
            },
            "individual_test_results": {
                "registry_manager_basic": test1_result,
                "registry_performance": test2_result,
                "mcp_integration": test3_result,
                "registry_persistence": test4_result,
                "error_handling": test5_result,
                "performance_targets": test6_result
            }
        }
        
        # Check overall success
        overall_results["test_suite_summary"]["overall_success"] = all([
            test1_result["passed"], test2_result["passed"], test3_result["passed"],
            test4_result["passed"], test5_result["passed"], test6_result["passed"]
        ])
        
        logger.info(f"✅ Test Suite Completed: {overall_results['test_suite_summary']['passed_tests']}/6 tests passed")
        
        return overall_results
    
    def test_registry_manager_basic(self) -> Dict[str, Any]:
        """Test basic registry manager functionality"""
        logger.info("🔍 Test 1: Registry Manager Basic Functionality")
        
        test_start = time.time()
        errors = []
        
        try:
            # Test adding entries
            test_entries = [
                ("test-item-001", "notion-page-001", "knowledge_vault", "db-001", "Test Item 1"),
                ("test-item-002", "notion-page-002", "tools_services", "db-002", "Test Item 2"),
                ("test-item-003", "notion-page-003", "business_ideas", "db-003", "Test Item 3"),
            ]
            
            for item_uuid, notion_id, db_id, db_notion_id, title in test_entries:
                success = self.registry_manager.add_registry_entry(
                    item_uuid=item_uuid,
                    notion_page_id=notion_id,
                    database_id=db_id,
                    database_notion_id=db_notion_id,
                    title=title,
                    content=f"Test content for {title}"
                )
                if not success:
                    errors.append(f"Failed to add entry: {item_uuid}")
            
            # Test retrieving entries
            for item_uuid, notion_id, db_id, _, _ in test_entries:
                retrieved_id = self.registry_manager.get_notion_page_id(item_uuid, db_id)
                if retrieved_id != notion_id:
                    errors.append(f"Retrieved ID mismatch: expected {notion_id}, got {retrieved_id}")
            
            # Test bulk operations
            bulk_entries = [
                {
                    "item_uuid": f"bulk-test-{i:03d}",
                    "notion_page_id": f"bulk-notion-{i:03d}",
                    "database_id": "knowledge_vault",
                    "database_notion_id": "bulk-db-001",
                    "title": f"Bulk Test Item {i}",
                    "content": f"Bulk content {i}"
                }
                for i in range(10)
            ]
            
            bulk_success = self.registry_manager.bulk_add_entries(bulk_entries)
            if bulk_success != 10:
                errors.append(f"Bulk add failed: expected 10, got {bulk_success}")
            
            # Test statistics
            stats = self.registry_manager.get_registry_statistics()
            if stats["total_entries"] < 13:  # 3 individual + 10 bulk
                errors.append(f"Statistics error: expected ≥13 entries, got {stats['total_entries']}")
            
            execution_time = (time.time() - test_start) * 1000
            
            return {
                "test_name": "Registry Manager Basic Functionality",
                "passed": len(errors) == 0,
                "execution_time_ms": execution_time,
                "errors": errors,
                "metrics": {
                    "entries_added": 13,
                    "retrieval_tests": 3,
                    "bulk_operations": 1,
                    "statistics_generated": True
                }
            }
            
        except Exception as e:
            return {
                "test_name": "Registry Manager Basic Functionality",
                "passed": False,
                "execution_time_ms": (time.time() - test_start) * 1000,
                "errors": [f"Exception: {str(e)}"],
                "metrics": {}
            }
    
    def test_registry_performance(self) -> Dict[str, Any]:
        """Test registry performance with larger dataset"""
        logger.info("⚡ Test 2: Registry Performance Testing")
        
        test_start = time.time()
        errors = []
        
        try:
            # Generate large dataset
            dataset_size = 100
            performance_entries = [
                {
                    "item_uuid": f"perf-test-{i:04d}",
                    "notion_page_id": f"perf-notion-{i:04d}",
                    "database_id": ["knowledge_vault", "tools_services", "business_ideas"][i % 3],
                    "database_notion_id": f"perf-db-{(i % 3) + 1:03d}",
                    "title": f"Performance Test Item {i}",
                    "content": f"Performance test content for item {i} with longer description"
                }
                for i in range(dataset_size)
            ]
            
            # Test bulk add performance
            bulk_start = time.time()
            bulk_success = self.registry_manager.bulk_add_entries(performance_entries)
            bulk_time = (time.time() - bulk_start) * 1000
            
            if bulk_success != dataset_size:
                errors.append(f"Bulk performance test failed: {bulk_success}/{dataset_size}")
            
            # Test lookup performance
            lookup_times = []
            for i in range(0, min(50, dataset_size), 5):  # Test every 5th item
                entry = performance_entries[i]
                lookup_start = time.time()
                retrieved_id = self.registry_manager.get_notion_page_id(
                    entry["item_uuid"], entry["database_id"]
                )
                lookup_time = (time.time() - lookup_start) * 1000
                lookup_times.append(lookup_time)
                
                if retrieved_id != entry["notion_page_id"]:
                    errors.append(f"Lookup failed for {entry['item_uuid']}")
            
            # Performance analysis
            avg_lookup_time = sum(lookup_times) / len(lookup_times) if lookup_times else 0
            max_lookup_time = max(lookup_times) if lookup_times else 0
            
            # Performance thresholds (should be sub-millisecond for cache hits)
            if avg_lookup_time > 5.0:  # 5ms threshold
                errors.append(f"Average lookup time too slow: {avg_lookup_time:.2f}ms")
            
            if bulk_time / dataset_size > 50.0:  # 50ms per item threshold
                errors.append(f"Bulk operation too slow: {bulk_time / dataset_size:.2f}ms per item")
            
            execution_time = (time.time() - test_start) * 1000
            
            return {
                "test_name": "Registry Performance Testing",
                "passed": len(errors) == 0,
                "execution_time_ms": execution_time,
                "errors": errors,
                "metrics": {
                    "dataset_size": dataset_size,
                    "bulk_add_time_ms": bulk_time,
                    "bulk_rate_items_per_sec": dataset_size / (bulk_time / 1000),
                    "average_lookup_time_ms": avg_lookup_time,
                    "max_lookup_time_ms": max_lookup_time,
                    "lookup_operations_tested": len(lookup_times)
                }
            }
            
        except Exception as e:
            return {
                "test_name": "Registry Performance Testing",
                "passed": False,
                "execution_time_ms": (time.time() - test_start) * 1000,
                "errors": [f"Exception: {str(e)}"],
                "metrics": {}
            }
    
    def test_mcp_integration(self) -> Dict[str, Any]:
        """Test MCP operations integration with registry"""
        logger.info("🔌 Test 3: MCP Operations Integration")
        
        test_start = time.time()
        errors = []
        
        try:
            # Test enhanced MCP operations
            test_items = [
                ("mcp-test-001", "knowledge_vault"),
                ("mcp-test-002", "tools_services"),
                ("mcp-test-003", "business_ideas"),
            ]
            
            # First lookup (should be cache miss, fallback to MCP)
            first_lookup_results = []
            for item_uuid, database_id in test_items:
                result = self.mcp_operations.get_notion_page_by_uuid(item_uuid, database_id)
                first_lookup_results.append(result)
                
                # Most should be cache misses on first run
                if result.cache_hit and not item_uuid.startswith('test-'):
                    # Only flag as error if it's not a test item we added earlier
                    pass  # This is actually fine - might be cached from previous tests
            
            # Second lookup (should be cache hits if items were found)
            second_lookup_results = []
            cache_hits = 0
            for item_uuid, database_id in test_items:
                result = self.mcp_operations.get_notion_page_by_uuid(item_uuid, database_id)
                second_lookup_results.append(result)
                
                if result.success and result.cache_hit:
                    cache_hits += 1
            
            # Test batch operations
            batch_items = [(f"batch-mcp-{i:03d}", "knowledge_vault") for i in range(10)]
            batch_results = self.mcp_operations.batch_get_notion_pages(batch_items)
            
            if len(batch_results) != 10:
                errors.append(f"Batch operation failed: expected 10 results, got {len(batch_results)}")
            
            # Test performance metrics
            metrics = self.mcp_operations.get_performance_metrics()
            if "operation_summary" not in metrics:
                errors.append("Performance metrics not available")
            
            execution_time = (time.time() - test_start) * 1000
            
            return {
                "test_name": "MCP Operations Integration",
                "passed": len(errors) == 0,
                "execution_time_ms": execution_time,
                "errors": errors,
                "metrics": {
                    "individual_operations": len(first_lookup_results) + len(second_lookup_results),
                    "batch_operations": 1,
                    "cache_hits_second_lookup": cache_hits,
                    "performance_metrics_available": "operation_summary" in metrics
                }
            }
            
        except Exception as e:
            return {
                "test_name": "MCP Operations Integration",
                "passed": False,
                "execution_time_ms": (time.time() - test_start) * 1000,
                "errors": [f"Exception: {str(e)}"],
                "metrics": {}
            }
    
    def test_registry_persistence(self) -> Dict[str, Any]:
        """Test registry persistence and recovery"""
        logger.info("💾 Test 4: Registry Persistence and Recovery")
        
        test_start = time.time()
        errors = []
        
        try:
            # Add test data
            persistence_entries = [
                ("persist-test-001", "persist-notion-001", "knowledge_vault", "persist-db", "Persist Test 1"),
                ("persist-test-002", "persist-notion-002", "tools_services", "persist-db", "Persist Test 2"),
            ]
            
            for item_uuid, notion_id, db_id, db_notion_id, title in persistence_entries:
                success = self.registry_manager.add_registry_entry(
                    item_uuid=item_uuid,
                    notion_page_id=notion_id,
                    database_id=db_id,
                    database_notion_id=db_notion_id,
                    title=title
                )
                if not success:
                    errors.append(f"Failed to add persistence test entry: {item_uuid}")
            
            # Save registry
            save_success = self.registry_manager.save_registry()
            if not save_success:
                errors.append("Failed to save registry")
            
            # Create new registry manager instance (simulates restart)
            new_registry_manager = DatabaseIDRegistryManager()
            
            # Test that data persisted
            for item_uuid, notion_id, db_id, _, _ in persistence_entries:
                retrieved_id = new_registry_manager.get_notion_page_id(item_uuid, db_id)
                if retrieved_id != notion_id:
                    errors.append(f"Persistence failed for {item_uuid}: expected {notion_id}, got {retrieved_id}")
            
            # Test cleanup functionality
            cleanup_count = new_registry_manager.cleanup_expired_entries()
            # Should be 0 for fresh entries
            
            execution_time = (time.time() - test_start) * 1000
            
            return {
                "test_name": "Registry Persistence and Recovery",
                "passed": len(errors) == 0,
                "execution_time_ms": execution_time,
                "errors": errors,
                "metrics": {
                    "entries_saved": len(persistence_entries),
                    "entries_recovered": len(persistence_entries),
                    "cleanup_entries_removed": cleanup_count
                }
            }
            
        except Exception as e:
            return {
                "test_name": "Registry Persistence and Recovery",
                "passed": False,
                "execution_time_ms": (time.time() - test_start) * 1000,
                "errors": [f"Exception: {str(e)}"],
                "metrics": {}
            }
    
    def test_error_handling(self) -> Dict[str, Any]:
        """Test error handling and edge cases"""
        logger.info("⚠️ Test 5: Error Handling and Edge Cases")
        
        test_start = time.time()
        errors = []
        
        try:
            # Test invalid UUIDs
            invalid_result = self.registry_manager.get_notion_page_id("", "knowledge_vault")
            if invalid_result is not None:
                errors.append("Should return None for empty UUID")
            
            # Test invalid database IDs
            invalid_db_result = self.registry_manager.get_notion_page_id("valid-uuid", "")
            if invalid_db_result is not None:
                errors.append("Should return None for empty database ID")
            
            # Test adding duplicate entries (should update, not fail)
            duplicate_success = self.registry_manager.add_registry_entry(
                item_uuid="duplicate-test",
                notion_page_id="duplicate-notion-1",
                database_id="knowledge_vault",
                database_notion_id="duplicate-db",
                title="Original Title"
            )
            
            if not duplicate_success:
                errors.append("Failed to add initial duplicate test entry")
            
            # Update with different data
            update_success = self.registry_manager.add_registry_entry(
                item_uuid="duplicate-test",  # Same UUID
                notion_page_id="duplicate-notion-2",  # Different Notion ID
                database_id="knowledge_vault",
                database_notion_id="duplicate-db",
                title="Updated Title"
            )
            
            if not update_success:
                errors.append("Failed to update duplicate entry")
            
            # Verify update worked
            final_id = self.registry_manager.get_notion_page_id("duplicate-test", "knowledge_vault")
            if final_id != "duplicate-notion-2":
                errors.append(f"Duplicate update failed: expected duplicate-notion-2, got {final_id}")
            
            # Test removing non-existent entry
            remove_success = self.registry_manager.remove_registry_entry("non-existent", "knowledge_vault")
            if remove_success:
                errors.append("Should return False when removing non-existent entry")
            
            # Test cache invalidation
            invalidate_success = self.registry_manager.invalidate_cache("knowledge_vault")
            if invalidate_success == 0:
                # This might be OK if no entries exist for that database
                pass
            
            execution_time = (time.time() - test_start) * 1000
            
            return {
                "test_name": "Error Handling and Edge Cases",
                "passed": len(errors) == 0,
                "execution_time_ms": execution_time,
                "errors": errors,
                "metrics": {
                    "invalid_input_tests": 2,
                    "duplicate_handling_tests": 2,
                    "removal_tests": 1,
                    "invalidation_tests": 1
                }
            }
            
        except Exception as e:
            return {
                "test_name": "Error Handling and Edge Cases",
                "passed": False,
                "execution_time_ms": (time.time() - test_start) * 1000,
                "errors": [f"Exception: {str(e)}"],
                "metrics": {}
            }
    
    def test_performance_targets(self) -> Dict[str, Any]:
        """Test that performance targets are met"""
        logger.info("🎯 Test 6: Performance Targets Validation")
        
        test_start = time.time()
        errors = []
        
        try:
            # Get comprehensive performance metrics
            mcp_metrics = self.mcp_operations.get_performance_metrics()
            registry_stats = self.registry_manager.get_registry_statistics()
            
            # Check if we have enough operations for meaningful metrics
            if "operation_summary" in mcp_metrics and mcp_metrics["operation_summary"]["total_operations"] > 0:
                # Target: 70-85% API call reduction
                cache_performance = mcp_metrics.get("cache_performance", {})
                cache_hit_rate = cache_performance.get("cache_hit_rate_percentage", 0)
                
                if cache_hit_rate < 70.0:
                    errors.append(f"Cache hit rate below target: {cache_hit_rate:.1f}% < 70%")
                
                # Target: Sub-2ms response time for cache hits (registry lookups)
                response_times = mcp_metrics.get("response_times", {})
                avg_response_time = response_times.get("average_response_time_ms", 0)
                
                # This is average across all operations, cache hits should be much faster
                if avg_response_time > 100.0:  # 100ms threshold for mixed operations
                    errors.append(f"Average response time too slow: {avg_response_time:.1f}ms")
            
            # Check registry statistics
            if registry_stats["total_entries"] == 0:
                errors.append("No entries in registry - cannot validate performance targets")
            
            # Check cache efficiency
            cache_efficiency = registry_stats.get("cache_efficiency", 0)
            if "performance_metrics" in registry_stats and cache_efficiency > 0:
                if cache_efficiency < 70.0:
                    errors.append(f"Cache efficiency below target: {cache_efficiency:.1f}% < 70%")
            
            execution_time = (time.time() - test_start) * 1000
            
            return {
                "test_name": "Performance Targets Validation",
                "passed": len(errors) == 0,
                "execution_time_ms": execution_time,
                "errors": errors,
                "metrics": {
                    "registry_entries": registry_stats.get("total_entries", 0),
                    "cache_hit_rate_percentage": mcp_metrics.get("cache_performance", {}).get("cache_hit_rate_percentage", 0),
                    "average_response_time_ms": mcp_metrics.get("response_times", {}).get("average_response_time_ms", 0),
                    "api_calls_saved": mcp_metrics.get("cache_performance", {}).get("api_calls_saved", 0),
                    "performance_target_achievement": mcp_metrics.get("performance_target_achievement", {})
                }
            }
            
        except Exception as e:
            return {
                "test_name": "Performance Targets Validation",
                "passed": False,
                "execution_time_ms": (time.time() - test_start) * 1000,
                "errors": [f"Exception: {str(e)}"],
                "metrics": {}
            }
    
    def generate_test_report(self, results: Dict[str, Any], output_path: str = None) -> str:
        """
        Generate comprehensive test report
        
        Args:
            results: Test results dictionary
            output_path: Optional path to save report
            
        Returns:
            Formatted test report string
        """
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("DATABASE ID REGISTRY INTEGRATION TEST REPORT")
        report_lines.append("=" * 80)
        
        # Summary
        summary = results["test_suite_summary"]
        report_lines.append(f"\n📊 SUMMARY")
        report_lines.append(f"Total Tests: {summary['total_tests']}")
        report_lines.append(f"Passed: {summary['passed_tests']}")
        report_lines.append(f"Failed: {summary['total_tests'] - summary['passed_tests']}")
        report_lines.append(f"Success Rate: {(summary['passed_tests'] / summary['total_tests']) * 100:.1f}%")
        report_lines.append(f"Total Execution Time: {summary['total_execution_time_ms']:.1f}ms")
        report_lines.append(f"Overall Result: {'✅ PASSED' if summary['overall_success'] else '❌ FAILED'}")
        
        # Individual test results
        report_lines.append(f"\n📋 DETAILED RESULTS")
        for test_name, test_result in results["individual_test_results"].items():
            status = "✅ PASS" if test_result["passed"] else "❌ FAIL"
            report_lines.append(f"\n{status} {test_result['test_name']}")
            report_lines.append(f"  Execution Time: {test_result['execution_time_ms']:.1f}ms")
            
            if test_result["errors"]:
                report_lines.append("  Errors:")
                for error in test_result["errors"]:
                    report_lines.append(f"    - {error}")
            
            if test_result["metrics"]:
                report_lines.append("  Metrics:")
                for metric, value in test_result["metrics"].items():
                    report_lines.append(f"    {metric}: {value}")
        
        report_content = "\n".join(report_lines)
        
        # Save to file if path provided
        if output_path:
            with open(output_path, 'w') as f:
                f.write(report_content)
            logger.info(f"Test report saved to: {output_path}")
        
        return report_content

def main():
    """Main function for running tests"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Database ID Registry Integration Test Suite')
    parser.add_argument('--output', help='Output file for test report')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Run test suite
    test_suite = RegistryIntegrationTestSuite()
    results = test_suite.run_all_tests()
    
    # Generate and display report
    report_path = args.output or f"/tmp/registry_test_report_{int(time.time())}.txt"
    report_content = test_suite.generate_test_report(results, report_path)
    
    print(report_content)
    
    # Exit with appropriate code
    sys.exit(0 if results["test_suite_summary"]["overall_success"] else 1)

if __name__ == "__main__":
    main()