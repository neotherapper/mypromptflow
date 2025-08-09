#!/usr/bin/env python3
"""
Orchestrator Integration Validation Script
Validates all components of the Automated Discovery Orchestrator system
"""

import os
import sys
import json
import subprocess
import importlib.util
from pathlib import Path
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OrchestrationValidation:
    """Comprehensive validation of orchestrator integration"""
    
    def __init__(self, base_path: Path = None):
        self.base_path = base_path or Path(__file__).parent
        self.validation_results = []
        self.errors = []
        self.warnings = []
    
    def validate_file_exists(self, file_path: Path, description: str) -> bool:
        """Validate that a required file exists"""
        exists = file_path.exists()
        result = {
            "test": f"File exists: {description}",
            "file": str(file_path),
            "passed": exists,
            "message": "File found" if exists else f"File not found: {file_path}"
        }
        self.validation_results.append(result)
        
        if not exists:
            self.errors.append(f"Missing file: {file_path}")
        
        return exists
    
    def validate_python_syntax(self, file_path: Path, description: str) -> bool:
        """Validate Python file syntax"""
        if not file_path.exists():
            return False
        
        try:
            with open(file_path, 'r') as f:
                compile(f.read(), str(file_path), 'exec')
            
            result = {
                "test": f"Python syntax: {description}",
                "file": str(file_path),
                "passed": True,
                "message": "Syntax valid"
            }
            self.validation_results.append(result)
            return True
            
        except SyntaxError as e:
            result = {
                "test": f"Python syntax: {description}",
                "file": str(file_path),
                "passed": False,
                "message": f"Syntax error: {e}"
            }
            self.validation_results.append(result)
            self.errors.append(f"Syntax error in {file_path}: {e}")
            return False
    
    def validate_json_config(self, file_path: Path, description: str) -> bool:
        """Validate JSON configuration file"""
        if not file_path.exists():
            self.warnings.append(f"Configuration file not found: {file_path}")
            return False
        
        try:
            with open(file_path, 'r') as f:
                json.load(f)
            
            result = {
                "test": f"JSON config: {description}",
                "file": str(file_path),
                "passed": True,
                "message": "Valid JSON"
            }
            self.validation_results.append(result)
            return True
            
        except json.JSONDecodeError as e:
            result = {
                "test": f"JSON config: {description}",
                "file": str(file_path),
                "passed": False,
                "message": f"Invalid JSON: {e}"
            }
            self.validation_results.append(result)
            self.errors.append(f"Invalid JSON in {file_path}: {e}")
            return False
    
    def validate_python_import(self, file_path: Path, description: str) -> bool:
        """Validate that Python file can be imported"""
        if not file_path.exists():
            return False
        
        try:
            spec = importlib.util.spec_from_file_location("test_module", file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            result = {
                "test": f"Python import: {description}",
                "file": str(file_path),
                "passed": True,
                "message": "Import successful"
            }
            self.validation_results.append(result)
            return True
            
        except Exception as e:
            result = {
                "test": f"Python import: {description}",
                "file": str(file_path),
                "passed": False,
                "message": f"Import failed: {e}"
            }
            self.validation_results.append(result)
            self.errors.append(f"Import failed for {file_path}: {e}")
            return False
    
    def validate_dependencies(self) -> bool:
        """Validate required Python dependencies"""
        required_packages = [
            'schedule', 'psutil', 'requests', 'feedparser', 'praw'
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                __import__(package)
                result = {
                    "test": f"Dependency: {package}",
                    "file": "N/A",
                    "passed": True,
                    "message": "Package available"
                }
                self.validation_results.append(result)
            except ImportError:
                missing_packages.append(package)
                result = {
                    "test": f"Dependency: {package}",
                    "file": "N/A", 
                    "passed": False,
                    "message": "Package not found"
                }
                self.validation_results.append(result)
        
        if missing_packages:
            self.errors.append(f"Missing packages: {', '.join(missing_packages)}")
            return False
        
        return True
    
    def validate_orchestrator_components(self) -> bool:
        """Validate all orchestrator components"""
        logger.info("🔍 Validating orchestrator components...")
        
        components = [
            # Core orchestrator
            (self.base_path / "automated-discovery-orchestrator.py", "Main Orchestrator"),
            (self.base_path / "setup-orchestrator.py", "Setup Manager"),
            (self.base_path / "orchestrator-dashboard.py", "Dashboard"),
            
            # Discovery systems
            (self.base_path / "youtube-dynamic-search.py", "YouTube Search"),
            (self.base_path / "reddit-dynamic-discovery.py", "Reddit Discovery"),
            (self.base_path / "mcp-youtube-processor.py", "MCP YouTube Processor"),
            (self.base_path / "daily-digest" / "intelligence-digest-generator.py", "Digest Generator"),
            
            # Supporting systems
            (self.base_path / "topic-scoring-engine.py", "Topic Scoring Engine"),
        ]
        
        all_valid = True
        
        for file_path, description in components:
            # Check file exists
            exists = self.validate_file_exists(file_path, description)
            if not exists:
                all_valid = False
                continue
            
            # Check syntax
            syntax_valid = self.validate_python_syntax(file_path, description)
            if not syntax_valid:
                all_valid = False
        
        return all_valid
    
    def validate_configuration_files(self) -> bool:
        """Validate configuration files"""
        logger.info("⚙️ Validating configuration files...")
        
        configs = [
            (self.base_path / "orchestrator-config.json", "Main Orchestrator Config"),
            (self.base_path / "priority-topics.json", "Priority Topics Config"),
            (self.base_path / "reddit-dynamic-discovery-config.json", "Reddit Config"),
        ]
        
        all_valid = True
        
        for config_path, description in configs:
            if not self.validate_json_config(config_path, description):
                # Only mark as error if it's a critical config
                if "orchestrator-config" in str(config_path):
                    all_valid = False
        
        return all_valid
    
    def validate_directory_structure(self) -> bool:
        """Validate required directory structure"""
        logger.info("📁 Validating directory structure...")
        
        required_dirs = [
            "daily-digest",
            "platforms",
            "platforms/youtube",
            "platforms/reddit", 
            "automation"
        ]
        
        all_valid = True
        
        for dir_name in required_dirs:
            dir_path = self.base_path / dir_name
            exists = dir_path.exists() and dir_path.is_dir()
            
            result = {
                "test": f"Directory exists: {dir_name}",
                "file": str(dir_path),
                "passed": exists,
                "message": "Directory found" if exists else f"Directory missing: {dir_path}"
            }
            self.validation_results.append(result)
            
            if not exists:
                self.warnings.append(f"Missing directory: {dir_path}")
                # Don't fail validation for missing directories, they can be created
        
        return all_valid
    
    def validate_integration_points(self) -> bool:
        """Validate integration between systems"""
        logger.info("🔗 Validating system integration points...")
        
        # Check if orchestrator can find discovery systems
        try:
            from automated_discovery_orchestrator import AutomatedDiscoveryOrchestrator
            orchestrator = AutomatedDiscoveryOrchestrator()
            
            # Check if tasks are initialized
            has_tasks = len(orchestrator.tasks) > 0
            
            result = {
                "test": "Orchestrator task initialization",
                "file": "automated-discovery-orchestrator.py",
                "passed": has_tasks,
                "message": f"Found {len(orchestrator.tasks)} tasks" if has_tasks else "No tasks initialized"
            }
            self.validation_results.append(result)
            
            if not has_tasks:
                self.errors.append("Orchestrator failed to initialize tasks")
                return False
            
            # Validate task configuration
            required_tasks = ["youtube_search", "reddit_discovery", "mcp_youtube_processing", "content_digest"]
            missing_tasks = []
            
            for task_id in required_tasks:
                if task_id not in orchestrator.tasks:
                    missing_tasks.append(task_id)
            
            if missing_tasks:
                result = {
                    "test": "Required tasks present",
                    "file": "automated-discovery-orchestrator.py",
                    "passed": False,
                    "message": f"Missing tasks: {', '.join(missing_tasks)}"
                }
                self.validation_results.append(result)
                self.errors.append(f"Missing required tasks: {', '.join(missing_tasks)}")
                return False
            else:
                result = {
                    "test": "Required tasks present",
                    "file": "automated-discovery-orchestrator.py", 
                    "passed": True,
                    "message": "All required tasks found"
                }
                self.validation_results.append(result)
            
            return True
            
        except Exception as e:
            result = {
                "test": "Orchestrator initialization",
                "file": "automated-discovery-orchestrator.py",
                "passed": False,
                "message": f"Failed to initialize: {e}"
            }
            self.validation_results.append(result)
            self.errors.append(f"Orchestrator initialization failed: {e}")
            return False
    
    def run_system_test(self) -> bool:
        """Run a basic system test"""
        logger.info("🧪 Running system test...")
        
        try:
            # Test orchestrator status command
            result = subprocess.run([
                sys.executable, 
                str(self.base_path / "automated-discovery-orchestrator.py"),
                "--mode", "status"
            ], capture_output=True, text=True, timeout=30, cwd=self.base_path)
            
            success = result.returncode == 0
            
            test_result = {
                "test": "System status test",
                "file": "automated-discovery-orchestrator.py",
                "passed": success,
                "message": "Status command successful" if success else f"Status command failed: {result.stderr}"
            }
            self.validation_results.append(test_result)
            
            if not success:
                self.errors.append(f"System test failed: {result.stderr}")
            
            return success
            
        except subprocess.TimeoutExpired:
            result = {
                "test": "System status test",
                "file": "automated-discovery-orchestrator.py",
                "passed": False,
                "message": "Test timed out"
            }
            self.validation_results.append(result)
            self.errors.append("System test timed out")
            return False
        except Exception as e:
            result = {
                "test": "System status test", 
                "file": "automated-discovery-orchestrator.py",
                "passed": False,
                "message": f"Test failed: {e}"
            }
            self.validation_results.append(result)
            self.errors.append(f"System test failed: {e}")
            return False
    
    def run_full_validation(self) -> bool:
        """Run complete validation suite"""
        logger.info("🚀 Starting comprehensive validation...")
        
        validation_steps = [
            ("Dependencies", self.validate_dependencies),
            ("Directory Structure", self.validate_directory_structure),
            ("Configuration Files", self.validate_configuration_files),
            ("Orchestrator Components", self.validate_orchestrator_components),
            ("Integration Points", self.validate_integration_points),
            ("System Test", self.run_system_test)
        ]
        
        failed_steps = []
        
        for step_name, step_function in validation_steps:
            logger.info(f"📍 Validating: {step_name}")
            
            try:
                if not step_function():
                    failed_steps.append(step_name)
                    logger.error(f"❌ {step_name} validation failed")
                else:
                    logger.info(f"✅ {step_name} validation passed")
            except Exception as e:
                logger.error(f"💥 {step_name} validation crashed: {e}")
                failed_steps.append(step_name)
        
        # Generate summary
        total_tests = len(self.validation_results)
        passed_tests = sum(1 for r in self.validation_results if r["passed"])
        failed_tests = total_tests - passed_tests
        
        logger.info(f"\n📊 Validation Summary:")
        logger.info(f"Total Tests: {total_tests}")
        logger.info(f"Passed: {passed_tests}")
        logger.info(f"Failed: {failed_tests}")
        logger.info(f"Errors: {len(self.errors)}")
        logger.info(f"Warnings: {len(self.warnings)}")
        
        if failed_steps:
            logger.error(f"\n❌ Failed validation steps:")
            for step in failed_steps:
                logger.error(f"  • {step}")
        
        if self.errors:
            logger.error(f"\n🚨 Critical Errors:")
            for error in self.errors:
                logger.error(f"  • {error}")
        
        if self.warnings:
            logger.warning(f"\n⚠️ Warnings:")
            for warning in self.warnings:
                logger.warning(f"  • {warning}")
        
        # Save detailed results
        self.save_validation_report()
        
        success = len(failed_steps) == 0 and len(self.errors) == 0
        
        if success:
            logger.info("\n🎉 All validations passed! System is ready for deployment.")
        else:
            logger.error("\n💥 Validation failed. Please address the errors above.")
        
        return success
    
    def save_validation_report(self):
        """Save detailed validation report"""
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total_tests": len(self.validation_results),
                "passed_tests": sum(1 for r in self.validation_results if r["passed"]),
                "failed_tests": sum(1 for r in self.validation_results if not r["passed"]),
                "errors": len(self.errors),
                "warnings": len(self.warnings)
            },
            "test_results": self.validation_results,
            "errors": self.errors,
            "warnings": self.warnings
        }
        
        report_file = self.base_path / "validation-report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"📄 Detailed validation report saved to: {report_file}")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate Orchestrator Integration")
    parser.add_argument("--base-path", type=Path, help="Base path for validation")
    parser.add_argument("--quick", action="store_true", help="Run quick validation only")
    
    args = parser.parse_args()
    
    validator = OrchestrationValidation(base_path=args.base_path)
    
    if args.quick:
        # Quick validation - just check files and syntax
        success = (validator.validate_dependencies() and 
                  validator.validate_orchestrator_components() and
                  validator.validate_configuration_files())
    else:
        # Full validation
        success = validator.run_full_validation()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()