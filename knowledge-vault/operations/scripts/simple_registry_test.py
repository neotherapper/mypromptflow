#!/usr/bin/env python3
"""
Simple Database ID Registry Test
Tests core functionality without external dependencies
"""

import os
import sys
import json
import time
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class RegistryEntry:
    """Registry entry for mapping Knowledge Vault UUID to Notion page ID"""
    item_uuid: str
    notion_page_id: str
    database_id: str
    database_notion_id: str
    title: str
    last_updated: str
    last_accessed: str
    access_count: int
    sync_status: str
    content_hash: str = ""

class SimpleDatabaseIDRegistry:
    """
    Simplified Database ID Registry for testing
    Uses JSON instead of YAML for compatibility
    """
    
    def __init__(self, registry_path: str = None):
        """Initialize registry"""
        self.registry_path = registry_path or "/tmp/simple_registry_test.json"
        self.registry_data = {}
        self.load_registry()
        
        logger.info(f"Simple Registry initialized: {self.registry_path}")
    
    def load_registry(self):
        """Load registry from JSON file"""
        try:
            if os.path.exists(self.registry_path):
                with open(self.registry_path, 'r') as f:
                    self.registry_data = json.load(f)
            else:
                self.registry_data = self._create_default_registry()
        except Exception as e:
            logger.error(f"Error loading registry: {e}")
            self.registry_data = self._create_default_registry()
    
    def save_registry(self):
        """Save registry to JSON file"""
        try:
            os.makedirs(os.path.dirname(self.registry_path), exist_ok=True)
            with open(self.registry_path, 'w') as f:
                json.dump(self.registry_data, f, indent=2)
            logger.info(f"Registry saved: {self.registry_path}")
        except Exception as e:
            logger.error(f"Error saving registry: {e}")
    
    def add_entry(self, item_uuid: str, notion_page_id: str, database_id: str,
                  database_notion_id: str = "", title: str = "") -> bool:
        """Add registry entry"""
        try:
            registry_key = f"{database_id}_registry"
            
            if registry_key not in self.registry_data:
                self.registry_data[registry_key] = {
                    'database_notion_id': database_notion_id,
                    'items': [],
                    'last_sync': None,
                    'item_count': 0
                }
            
            now = datetime.now().isoformat()
            entry = {
                'item_uuid': item_uuid,
                'notion_page_id': notion_page_id,
                'database_id': database_id,
                'database_notion_id': database_notion_id,
                'title': title,
                'last_updated': now,
                'last_accessed': now,
                'access_count': 1,
                'sync_status': 'synchronized'
            }
            
            # Check if entry exists and update
            items = self.registry_data[registry_key]['items']
            existing_index = None
            for i, item in enumerate(items):
                if item.get('item_uuid') == item_uuid:
                    existing_index = i
                    break
            
            if existing_index is not None:
                items[existing_index] = entry
            else:
                items.append(entry)
            
            self.registry_data[registry_key]['item_count'] = len(items)
            self.registry_data[registry_key]['last_sync'] = now
            
            return True
            
        except Exception as e:
            logger.error(f"Error adding entry {item_uuid}: {e}")
            return False
    
    def get_notion_page_id(self, item_uuid: str, database_id: str) -> Optional[str]:
        """Get Notion page ID for item UUID"""
        start_time = time.time()
        
        try:
            registry_key = f"{database_id}_registry"
            if registry_key not in self.registry_data:
                return None
            
            items = self.registry_data[registry_key].get('items', [])
            for item in items:
                if item.get('item_uuid') == item_uuid:
                    # Update access stats
                    item['last_accessed'] = datetime.now().isoformat()
                    item['access_count'] = item.get('access_count', 0) + 1
                    
                    processing_time = (time.time() - start_time) * 1000
                    logger.debug(f"Registry HIT: {item_uuid} -> {item['notion_page_id']} ({processing_time:.1f}ms)")
                    return item['notion_page_id']
            
            processing_time = (time.time() - start_time) * 1000
            logger.debug(f"Registry MISS: {item_uuid} ({processing_time:.1f}ms)")
            return None
            
        except Exception as e:
            logger.error(f"Error getting page ID for {item_uuid}: {e}")
            return None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get registry statistics"""
        total_entries = 0
        database_breakdown = {}
        
        for key in self.registry_data:
            if key.endswith('_registry'):
                database_name = key.replace('_registry', '')
                items = self.registry_data[key].get('items', [])
                total_entries += len(items)
                
                database_breakdown[database_name] = {
                    'item_count': len(items),
                    'last_sync': self.registry_data[key].get('last_sync')
                }
        
        return {
            'total_entries': total_entries,
            'database_breakdown': database_breakdown,
            'registry_file': self.registry_path
        }
    
    def _create_default_registry(self) -> Dict:
        """Create default registry structure"""
        return {
            'registry_info': {
                'name': 'Simple Database ID Registry',
                'version': '1.0.0',
                'created': datetime.now().isoformat(),
                'description': 'Test registry for Database ID caching'
            }
        }

def run_simple_tests():
    """Run simplified registry tests"""
    logger.info("🧪 Starting Simple Database ID Registry Tests")
    
    # Initialize registry
    test_registry = SimpleDatabaseIDRegistry()
    
    test_results = {
        'tests_run': 0,
        'tests_passed': 0,
        'errors': []
    }
    
    # Test 1: Add entries
    logger.info("📝 Test 1: Adding registry entries")
    test_results['tests_run'] += 1
    
    test_entries = [
        ("test-item-001", "notion-page-001", "knowledge_vault", "db-001", "Test Item 1"),
        ("test-item-002", "notion-page-002", "tools_services", "db-002", "Test Item 2"),
        ("test-item-003", "notion-page-003", "business_ideas", "db-003", "Test Item 3"),
    ]
    
    add_errors = []
    for item_uuid, notion_id, db_id, db_notion_id, title in test_entries:
        success = test_registry.add_entry(item_uuid, notion_id, db_id, db_notion_id, title)
        if not success:
            add_errors.append(f"Failed to add {item_uuid}")
    
    if not add_errors:
        test_results['tests_passed'] += 1
        logger.info("✅ Test 1 PASSED: All entries added successfully")
    else:
        test_results['errors'].extend(add_errors)
        logger.error(f"❌ Test 1 FAILED: {len(add_errors)} errors")
    
    # Test 2: Retrieve entries
    logger.info("🔍 Test 2: Retrieving registry entries")
    test_results['tests_run'] += 1
    
    retrieve_errors = []
    for item_uuid, expected_notion_id, db_id, _, _ in test_entries:
        actual_notion_id = test_registry.get_notion_page_id(item_uuid, db_id)
        if actual_notion_id != expected_notion_id:
            retrieve_errors.append(f"Mismatch for {item_uuid}: expected {expected_notion_id}, got {actual_notion_id}")
    
    if not retrieve_errors:
        test_results['tests_passed'] += 1
        logger.info("✅ Test 2 PASSED: All entries retrieved correctly")
    else:
        test_results['errors'].extend(retrieve_errors)
        logger.error(f"❌ Test 2 FAILED: {len(retrieve_errors)} errors")
    
    # Test 3: Performance test
    logger.info("⚡ Test 3: Performance testing")
    test_results['tests_run'] += 1
    
    # Add more entries for performance testing
    perf_entries = [(f"perf-{i:03d}", f"notion-perf-{i:03d}", "knowledge_vault", "perf-db", f"Perf {i}") 
                    for i in range(100)]
    
    perf_start = time.time()
    for item_uuid, notion_id, db_id, db_notion_id, title in perf_entries:
        test_registry.add_entry(item_uuid, notion_id, db_id, db_notion_id, title)
    perf_add_time = (time.time() - perf_start) * 1000
    
    # Test lookup performance
    lookup_start = time.time()
    lookup_results = []
    for item_uuid, expected_notion_id, db_id, _, _ in perf_entries[:10]:  # Test first 10
        result = test_registry.get_notion_page_id(item_uuid, db_id)
        lookup_results.append(result == expected_notion_id)
    lookup_time = (time.time() - lookup_start) * 1000
    
    avg_lookup_time = lookup_time / len(lookup_results)
    
    perf_success = all(lookup_results) and avg_lookup_time < 10.0  # 10ms threshold
    
    if perf_success:
        test_results['tests_passed'] += 1
        logger.info(f"✅ Test 3 PASSED: Performance OK (avg lookup: {avg_lookup_time:.2f}ms)")
    else:
        test_results['errors'].append(f"Performance issues: avg lookup {avg_lookup_time:.2f}ms")
        logger.error(f"❌ Test 3 FAILED: Performance issues")
    
    # Test 4: Persistence
    logger.info("💾 Test 4: Registry persistence")
    test_results['tests_run'] += 1
    
    # Save registry
    test_registry.save_registry()
    
    # Create new instance and test persistence
    new_registry = SimpleDatabaseIDRegistry(test_registry.registry_path)
    
    persistence_errors = []
    for item_uuid, expected_notion_id, db_id, _, _ in test_entries:
        actual_notion_id = new_registry.get_notion_page_id(item_uuid, db_id)
        if actual_notion_id != expected_notion_id:
            persistence_errors.append(f"Persistence failed for {item_uuid}")
    
    if not persistence_errors:
        test_results['tests_passed'] += 1
        logger.info("✅ Test 4 PASSED: Registry persistence working")
    else:
        test_results['errors'].extend(persistence_errors)
        logger.error(f"❌ Test 4 FAILED: Persistence issues")
    
    # Test 5: Statistics
    logger.info("📊 Test 5: Registry statistics")
    test_results['tests_run'] += 1
    
    stats = test_registry.get_statistics()
    
    expected_entries = len(test_entries) + len(perf_entries)
    actual_entries = stats['total_entries']
    
    if actual_entries >= expected_entries:
        test_results['tests_passed'] += 1
        logger.info(f"✅ Test 5 PASSED: Statistics correct ({actual_entries} entries)")
    else:
        test_results['errors'].append(f"Statistics error: expected ≥{expected_entries}, got {actual_entries}")
        logger.error(f"❌ Test 5 FAILED: Statistics issues")
    
    # Summary
    success_rate = (test_results['tests_passed'] / test_results['tests_run']) * 100
    logger.info(f"\n📋 TEST SUMMARY")
    logger.info(f"Tests Run: {test_results['tests_run']}")
    logger.info(f"Tests Passed: {test_results['tests_passed']}")
    logger.info(f"Success Rate: {success_rate:.1f}%")
    
    if test_results['errors']:
        logger.error(f"Errors encountered:")
        for error in test_results['errors']:
            logger.error(f"  - {error}")
    
    # Performance metrics
    logger.info(f"\n⚡ PERFORMANCE METRICS")
    logger.info(f"Batch Add Time: {perf_add_time:.1f}ms for 100 items")
    logger.info(f"Add Rate: {100 / (perf_add_time / 1000):.1f} items/sec")
    logger.info(f"Average Lookup Time: {avg_lookup_time:.2f}ms")
    logger.info(f"Registry File: {test_registry.registry_path}")
    
    # Display final statistics
    final_stats = test_registry.get_statistics()
    logger.info(f"\n📈 FINAL REGISTRY STATS")
    logger.info(f"Total Entries: {final_stats['total_entries']}")
    for db_name, db_stats in final_stats['database_breakdown'].items():
        logger.info(f"  {db_name}: {db_stats['item_count']} items")
    
    return success_rate == 100.0

def main():
    """Main function"""
    logger.info("Simple Database ID Registry Test Suite")
    logger.info("=" * 50)
    
    try:
        success = run_simple_tests()
        
        if success:
            logger.info("\n🎉 ALL TESTS PASSED - Database ID Registry working correctly!")
            sys.exit(0)
        else:
            logger.error("\n❌ SOME TESTS FAILED - Check errors above")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Test suite failed with exception: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()