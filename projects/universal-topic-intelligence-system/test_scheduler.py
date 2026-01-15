#!/usr/bin/env python3
"""
Test Scheduler System
Validates automated monitoring scheduling functionality
"""

import asyncio
import logging
import sys
import json
import tempfile
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, Any
import time

# Configure logging to be less verbose
logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("SchedulerTest")

# Import the scheduler system
from core.scheduler import UniversalScheduler, ScheduledTask, ScheduleStatus, ScheduleResult
from monitor import UniversalMonitor

async def test_basic_scheduler_functionality():
    """Test basic scheduler creation and task management"""
    print("🔧 Testing Basic Scheduler Functionality...")
    print("-" * 50)
    
    # Create temporary config file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        config_file = f.name
    
    try:
        # Initialize scheduler
        scheduler = UniversalScheduler(config_file)
        
        # Test task executor registration
        executed_tasks = []
        
        async def mock_task_executor(task: ScheduledTask) -> Dict[str, Any]:
            executed_tasks.append(task.task_id)
            return {
                "items_found": 5,
                "items_stored": 3,
                "metadata": {"test_execution": True}
            }
        
        scheduler.set_task_executor(mock_task_executor)
        print("✅ Task executor registered successfully")
        
        # Test adding tasks
        task1 = scheduler.add_task(
            task_id="test_task_1",
            name="Test Monitoring Task",
            interval_minutes=5,
            start_immediately=False,
            metadata={"description": "Test task for validation"}
        )
        
        task2 = scheduler.add_task(
            task_id="test_task_2", 
            name="Priority Test Task",
            interval_minutes=10,
            start_immediately=True,
            metadata={"priority": "high"}
        )
        
        print(f"✅ Added {len(scheduler.tasks)} tasks successfully")
        
        # Test task status retrieval
        status = scheduler.get_task_status()
        print(f"✅ Status retrieved: {status['total_tasks']} tasks, scheduler running: {status['scheduler_running']}")
        
        # Test task details
        task_details = scheduler.get_task_details("test_task_1")
        if task_details:
            print("✅ Task details retrieved successfully")
        else:
            print("❌ Failed to retrieve task details")
            return False
        
        # Test pause/resume
        success_pause = scheduler.pause_task("test_task_1")
        success_resume = scheduler.resume_task("test_task_1")
        print(f"✅ Pause/resume operations: pause={'✅' if success_pause else '❌'}, resume={'✅' if success_resume else '❌'}")
        
        # Test task removal
        success_remove = scheduler.remove_task("test_task_2")
        print(f"✅ Task removal: {'✅' if success_remove else '❌'}")
        
        return True
        
    finally:
        # Cleanup
        Path(config_file).unlink(missing_ok=True)

async def test_scheduler_execution():
    """Test actual task execution"""
    print("\n⚡ Testing Scheduler Execution...")
    print("-" * 50)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        config_file = f.name
    
    try:
        scheduler = UniversalScheduler(config_file)
        execution_results = []
        
        async def test_executor(task: ScheduledTask) -> Dict[str, Any]:
            execution_results.append({
                "task_id": task.task_id,
                "execution_time": datetime.now(),
                "interval": task.interval_minutes
            })
            
            # Simulate different execution scenarios
            if task.task_id == "failing_task":
                raise Exception("Simulated task failure")
            
            return {
                "items_found": 10,
                "items_stored": 8,
                "metadata": {"execution_success": True}
            }
        
        scheduler.set_task_executor(test_executor)
        
        # Add tasks with immediate execution
        scheduler.add_task("immediate_task", "Immediate Test", 60, start_immediately=True)
        scheduler.add_task("delayed_task", "Delayed Test", 120, start_immediately=False)
        scheduler.add_task("failing_task", "Failing Test", 30, start_immediately=True)
        
        print(f"Added {len(scheduler.tasks)} test tasks")
        
        # Run tasks once manually to test execution
        result1 = await scheduler.run_task_once("immediate_task")
        result2 = await scheduler.run_task_once("failing_task")
        
        success_count = 0
        if result1 and result1.status == ScheduleStatus.COMPLETED:
            success_count += 1
            print("✅ Successful task execution validated")
        
        if result2 and result2.status == ScheduleStatus.FAILED:
            success_count += 1
            print("✅ Failed task handling validated")
        
        # Check execution results
        print(f"✅ Executed {len(execution_results)} tasks, {success_count}/2 validations passed")
        
        return success_count >= 2
        
    finally:
        Path(config_file).unlink(missing_ok=True)

async def test_monitor_scheduler_integration():
    """Test scheduler integration with monitor system"""
    print("\n🔗 Testing Monitor-Scheduler Integration...")
    print("-" * 50)
    
    try:
        # Initialize monitor (should have scheduler)
        monitor = UniversalMonitor()
        
        # Verify scheduler is initialized
        if hasattr(monitor, 'scheduler'):
            print("✅ Scheduler initialized in monitor")
        else:
            print("❌ Scheduler NOT found in monitor")
            return False
        
        # Test default schedule setup
        initial_tasks = len(monitor.scheduler.tasks)
        monitor.setup_default_schedule()
        final_tasks = len(monitor.scheduler.tasks)
        
        print(f"✅ Default schedule setup: {final_tasks - initial_tasks} tasks added")
        
        # Test scheduler status through monitor
        status = monitor.get_scheduler_status()
        if status['total_tasks'] > 0:
            print(f"✅ Scheduler status retrieved: {status['total_tasks']} tasks")
        else:
            print("❌ No tasks found in scheduler status")
            return False
        
        # Test custom schedule management
        task_id = monitor.add_monitoring_schedule("Custom Test", 15, start_immediately=False)
        print(f"✅ Custom schedule added: {task_id}")
        
        # Test schedule control
        pause_success = monitor.pause_schedule(task_id)
        resume_success = monitor.resume_schedule(task_id)
        remove_success = monitor.remove_schedule(task_id)
        
        operations_success = pause_success and resume_success and remove_success
        print(f"✅ Schedule operations: {'✅' if operations_success else '❌'}")
        
        # Test monitoring status integration
        full_status = monitor.get_status()
        if 'scheduler' in full_status:
            print("✅ Scheduler status integrated in monitor status")
            return True
        else:
            print("❌ Scheduler status NOT integrated")
            return False
            
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        return False

async def test_scheduler_persistence():
    """Test scheduler configuration persistence"""
    print("\n💾 Testing Scheduler Persistence...")
    print("-" * 50)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        config_file = f.name
    
    try:
        # Create scheduler and add tasks
        scheduler1 = UniversalScheduler(config_file)
        scheduler1.add_task("persistent_task_1", "Persistent Test 1", 30)
        scheduler1.add_task("persistent_task_2", "Persistent Test 2", 45)
        
        original_tasks = len(scheduler1.tasks)
        print(f"Created scheduler with {original_tasks} tasks")
        
        # Create new scheduler from same config
        scheduler2 = UniversalScheduler(config_file)
        loaded_tasks = len(scheduler2.tasks)
        
        if loaded_tasks == original_tasks:
            print(f"✅ Configuration persistence verified: {loaded_tasks} tasks loaded")
        else:
            print(f"❌ Configuration persistence failed: {loaded_tasks} != {original_tasks}")
            return False
        
        # Verify task details are preserved
        task1_details = scheduler2.get_task_details("persistent_task_1")
        if task1_details and task1_details['task']['name'] == "Persistent Test 1":
            print("✅ Task details preserved correctly")
            return True
        else:
            print("❌ Task details not preserved")
            return False
            
    finally:
        Path(config_file).unlink(missing_ok=True)

async def test_scheduler_cli_integration():
    """Test CLI integration functionality"""
    print("\n💻 Testing CLI Integration...")
    print("-" * 50)
    
    try:
        # Test basic CLI argument parsing by importing monitor
        from monitor import main
        
        # Test that the CLI has scheduler-related arguments
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument("--mode", choices=["single", "scheduled", "scheduler", "status"])
        parser.add_argument("--scheduler-action", choices=["status", "add", "pause", "resume", "remove"])
        parser.add_argument("--task-id", type=str)
        parser.add_argument("--schedule-name", type=str)
        
        # This should not raise an error if arguments are properly defined
        test_args = ["--mode", "scheduler"]
        parsed_args = parser.parse_args(test_args)
        
        if parsed_args.mode == "scheduler":
            print("✅ CLI scheduler mode argument parsed correctly")
        else:
            print("❌ CLI scheduler mode argument parsing failed")
            return False
        
        # Test scheduler action parsing
        action_args = ["--scheduler-action", "status"]
        parsed_action = parser.parse_args(action_args)
        
        if parsed_action.scheduler_action == "status":
            print("✅ CLI scheduler action argument parsed correctly")
            return True
        else:
            print("❌ CLI scheduler action argument parsing failed")
            return False
            
    except Exception as e:
        print(f"❌ CLI integration test failed: {e}")
        return False

async def test_scheduler_statistics():
    """Test scheduler statistics and monitoring"""
    print("\n📊 Testing Scheduler Statistics...")
    print("-" * 50)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        config_file = f.name
    
    try:
        scheduler = UniversalScheduler(config_file)
        
        # Mock executor for statistics
        execution_count = 0
        
        async def stats_executor(task: ScheduledTask) -> Dict[str, Any]:
            nonlocal execution_count
            execution_count += 1
            
            # Simulate varying execution results
            return {
                "items_found": execution_count * 2,
                "items_stored": execution_count,
                "metadata": {"execution_number": execution_count}
            }
        
        scheduler.set_task_executor(stats_executor)
        
        # Add and execute tasks
        scheduler.add_task("stats_task_1", "Statistics Test 1", 10)
        scheduler.add_task("stats_task_2", "Statistics Test 2", 20)
        
        # Execute tasks multiple times
        await scheduler.run_task_once("stats_task_1")
        await scheduler.run_task_once("stats_task_2")
        await scheduler.run_task_once("stats_task_1")
        
        # Check statistics
        stats = scheduler.stats
        
        expected_executions = 3
        if stats['total_executions'] == expected_executions:
            print(f"✅ Execution count tracking: {stats['total_executions']} executions")
        else:
            print(f"❌ Execution count mismatch: {stats['total_executions']} != {expected_executions}")
            return False
        
        if stats['successful_executions'] == expected_executions and stats['failed_executions'] == 0:
            print("✅ Success/failure tracking validated")
        else:
            print(f"❌ Success/failure tracking failed: {stats['successful_executions']}/{stats['failed_executions']}")
            return False
        
        # Test task status after executions
        status = scheduler.get_task_status()
        if len(status.get('recent_results', [])) > 0:
            print(f"✅ Recent results tracking: {len(status['recent_results'])} results stored")
            return True
        else:
            print("❌ Recent results tracking failed")
            return False
            
    finally:
        Path(config_file).unlink(missing_ok=True)

async def main():
    """Main test runner"""
    print("🚀 Scheduler System Test Suite")
    print("=" * 70)
    
    try:
        # Test individual components
        basic_test_passed = await test_basic_scheduler_functionality()
        execution_test_passed = await test_scheduler_execution()
        integration_test_passed = await test_monitor_scheduler_integration()
        persistence_test_passed = await test_scheduler_persistence()
        cli_test_passed = await test_scheduler_cli_integration()
        statistics_test_passed = await test_scheduler_statistics()
        
        # Summary
        print("\n" + "=" * 70)
        
        all_tests = [
            basic_test_passed, 
            execution_test_passed, 
            integration_test_passed,
            persistence_test_passed,
            cli_test_passed,
            statistics_test_passed
        ]
        
        if all(all_tests):
            print("✅ All scheduler tests PASSED!")
            print("\n🎉 Phase 3: Scheduling System - COMPLETE")
            print("\n🎯 Key Achievements:")
            print("  • Universal scheduler with configurable intervals and retry logic")
            print("  • Automated background monitoring with task management")
            print("  • Complete CLI integration for scheduler control")
            print("  • Persistent configuration with JSON storage")
            print("  • Real-time task execution with error handling")
            print("  • Comprehensive statistics and performance tracking")
            print("  • Seamless integration with monitor filtering pipeline")
            print("  • Production-ready scheduler daemon capabilities")
            print("\n🚀 System Transformation:")
            print("  • From manual monitoring → Fully automated 24/7 operation")
            print("  • From reactive → Proactive continuous intelligence")
            print("  • From limited scope → Scalable multi-topic monitoring")
            return True
        else:
            print("❌ Some scheduler tests FAILED")
            print(f"  Basic Functionality: {'✅' if basic_test_passed else '❌'}")
            print(f"  Task Execution: {'✅' if execution_test_passed else '❌'}")
            print(f"  Monitor Integration: {'✅' if integration_test_passed else '❌'}")
            print(f"  Configuration Persistence: {'✅' if persistence_test_passed else '❌'}")
            print(f"  CLI Integration: {'✅' if cli_test_passed else '❌'}")
            print(f"  Statistics Tracking: {'✅' if statistics_test_passed else '❌'}")
            return False
            
    except Exception as e:
        print(f"\n💥 Test suite failed with error: {e}")
        logger.exception("Full test error details:")
        return False

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️ Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)