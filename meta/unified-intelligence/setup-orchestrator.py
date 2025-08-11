#!/usr/bin/env python3
"""
Automated Discovery Orchestrator Setup and Management Script
Handles installation, configuration, and management of the orchestration system
"""

import os
import sys
import json
import subprocess
import shutil
from pathlib import Path
from datetime import datetime
import logging
import argparse

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OrchestratorSetup:
    """Setup and management for the Automated Discovery Orchestrator"""
    
    def __init__(self, base_path: Path = None):
        self.base_path = base_path or Path(__file__).parent
        self.orchestrator_script = self.base_path / "automated-discovery-orchestrator.py"
        self.config_file = self.base_path / "orchestrator-config.json"
        self.requirements_file = self.base_path / "orchestrator-requirements.txt"
        self.systemd_service_file = self.base_path / "orchestrator.service"
        self.cron_file = self.base_path / "orchestrator-cron"
        
    def check_prerequisites(self) -> bool:
        """Check if all prerequisites are met"""
        logger.info("🔍 Checking prerequisites...")
        
        issues = []
        
        # Check Python version
        if sys.version_info < (3, 8):
            issues.append("Python 3.8+ is required")
        
        # Check if main script exists
        if not self.orchestrator_script.exists():
            issues.append(f"Main orchestrator script not found: {self.orchestrator_script}")
        
        # Check if discovery systems exist
        discovery_systems = [
            "youtube-dynamic-search.py",
            "reddit-dynamic-discovery.py", 
            "mcp-youtube-processor.py",
            "daily-digest/intelligence-digest-generator.py"
        ]
        
        for system in discovery_systems:
            system_path = self.base_path / system
            if not system_path.exists():
                issues.append(f"Discovery system not found: {system_path}")
        
        # Check required Python packages
        required_packages = [
            "schedule", "psutil", "requests", "feedparser", "praw"
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                missing_packages.append(package)
        
        if missing_packages:
            issues.append(f"Missing Python packages: {', '.join(missing_packages)}")
        
        if issues:
            logger.error("❌ Prerequisites check failed:")
            for issue in issues:
                logger.error(f"  • {issue}")
            return False
        
        logger.info("✅ All prerequisites met")
        return True
    
    def create_requirements_file(self):
        """Create requirements.txt file for the orchestrator"""
        requirements = [
            "schedule>=1.2.0",
            "psutil>=5.9.0", 
            "requests>=2.28.0",
            "feedparser>=6.0.10",
            "praw>=7.6.0",
            "python-dateutil>=2.8.0",
            "pyyaml>=6.0"
        ]
        
        with open(self.requirements_file, 'w') as f:
            f.write('\n'.join(requirements))
        
        logger.info(f"📝 Created requirements file: {self.requirements_file}")
    
    def install_dependencies(self):
        """Install required Python dependencies"""
        logger.info("📦 Installing dependencies...")
        
        if not self.requirements_file.exists():
            self.create_requirements_file()
        
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(self.requirements_file)
            ], check=True)
            logger.info("✅ Dependencies installed successfully")
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to install dependencies: {e}")
            return False
        
        return True
    
    def create_systemd_service(self):
        """Create systemd service file for continuous operation"""
        service_content = f"""[Unit]
Description=Automated Discovery Orchestrator
After=network.target

[Service]
Type=simple
User={os.getenv('USER', 'root')}
WorkingDirectory={self.base_path}
ExecStart={sys.executable} {self.orchestrator_script} --mode continuous
Restart=always
RestartSec=30
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
"""
        
        with open(self.systemd_service_file, 'w') as f:
            f.write(service_content)
        
        logger.info(f"📄 Created systemd service file: {self.systemd_service_file}")
        logger.info("To install as system service, run:")
        logger.info(f"  sudo cp {self.systemd_service_file} /etc/systemd/system/")
        logger.info("  sudo systemctl daemon-reload")
        logger.info("  sudo systemctl enable orchestrator.service")
        logger.info("  sudo systemctl start orchestrator.service")
    
    def create_cron_job(self):
        """Create cron job for scheduled execution"""
        cron_content = f"""# Automated Discovery Orchestrator - Scheduled Tasks
# Run every 30 minutes during business hours (6 AM - 10 PM)
*/30 6-22 * * * {sys.executable} {self.orchestrator_script} --mode single >> {self.base_path}/orchestrator-cron.log 2>&1

# Run full cycle daily at 6 AM
0 6 * * * {sys.executable} {self.orchestrator_script} --mode single >> {self.base_path}/orchestrator-cron.log 2>&1

# Run weekly tasks on Sunday at 8 AM  
0 8 * * 0 {sys.executable} {self.orchestrator_script} --mode single >> {self.base_path}/orchestrator-cron.log 2>&1

# Health check every hour
0 * * * * {sys.executable} {self.orchestrator_script} --mode single --task system_health >> {self.base_path}/orchestrator-health.log 2>&1
"""
        
        with open(self.cron_file, 'w') as f:
            f.write(cron_content)
        
        logger.info(f"📅 Created cron job file: {self.cron_file}")
        logger.info("To install cron job, run:")
        logger.info(f"  crontab {self.cron_file}")
    
    def setup_directories(self):
        """Create necessary directories for orchestrator operation"""
        directories = [
            "orchestrator-outputs",
            "orchestrator-outputs/daily",
            "orchestrator-outputs/weekly", 
            "orchestrator-outputs/logs",
            "orchestrator-outputs/reports",
            "orchestrator-outputs/backups"
        ]
        
        for directory in directories:
            dir_path = self.base_path / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"📁 Created directory: {dir_path}")
    
    def validate_configuration(self) -> bool:
        """Validate the orchestrator configuration"""
        logger.info("🔧 Validating configuration...")
        
        if not self.config_file.exists():
            logger.warning("⚠️ Configuration file not found, will be created on first run")
            return True
        
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            
            # Validate required sections
            required_sections = [
                "max_concurrent_tasks",
                "resource_limits", 
                "scheduling_intervals",
                "quality_thresholds",
                "retry_policies",
                "monitoring_settings",
                "output_organization"
            ]
            
            missing_sections = []
            for section in required_sections:
                if section not in config:
                    missing_sections.append(section)
            
            if missing_sections:
                logger.error(f"❌ Missing configuration sections: {', '.join(missing_sections)}")
                return False
            
            # Validate paths
            output_path = Path(config["output_organization"]["base_storage_path"])
            if not output_path.is_absolute():
                # Make relative to base path
                output_path = self.base_path / output_path
                config["output_organization"]["base_storage_path"] = str(output_path)
                
                # Save updated config
                with open(self.config_file, 'w') as f:
                    json.dump(config, f, indent=2)
            
            logger.info("✅ Configuration validated successfully")
            return True
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ Invalid JSON in configuration file: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Configuration validation failed: {e}")
            return False
    
    def test_orchestrator(self) -> bool:
        """Test the orchestrator with a dry run"""
        logger.info("🧪 Testing orchestrator...")
        
        try:
            # Run status check
            result = subprocess.run([
                sys.executable, str(self.orchestrator_script), "--mode", "status"
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                logger.info("✅ Orchestrator test passed")
                logger.info("Status output:")
                print(result.stdout)
                return True
            else:
                logger.error(f"❌ Orchestrator test failed: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("❌ Orchestrator test timed out")
            return False
        except Exception as e:
            logger.error(f"❌ Orchestrator test failed: {e}")
            return False
    
    def create_management_scripts(self):
        """Create management scripts for common operations"""
        
        # Start script
        start_script = self.base_path / "start-orchestrator.sh"
        with open(start_script, 'w') as f:
            f.write(f"""#!/bin/bash
# Start Automated Discovery Orchestrator
cd {self.base_path}
{sys.executable} {self.orchestrator_script} --mode continuous
""")
        start_script.chmod(0o755)
        
        # Stop script
        stop_script = self.base_path / "stop-orchestrator.sh"
        with open(stop_script, 'w') as f:
            f.write("""#!/bin/bash
# Stop Automated Discovery Orchestrator
pkill -f "automated-discovery-orchestrator.py"
""")
        stop_script.chmod(0o755)
        
        # Status script
        status_script = self.base_path / "status-orchestrator.sh"
        with open(status_script, 'w') as f:
            f.write(f"""#!/bin/bash
# Get Orchestrator Status
cd {self.base_path}
{sys.executable} {self.orchestrator_script} --mode status
""")
        status_script.chmod(0o755)
        
        logger.info("🔧 Created management scripts:")
        logger.info(f"  • Start: {start_script}")
        logger.info(f"  • Stop: {stop_script}")
        logger.info(f"  • Status: {status_script}")
    
    def setup_logging(self):
        """Setup logging configuration"""
        log_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                }
            },
            "handlers": {
                "file": {
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": str(self.base_path / "orchestrator.log"),
                    "maxBytes": 10485760,  # 10MB
                    "backupCount": 5,
                    "formatter": "standard"
                },
                "console": {
                    "class": "logging.StreamHandler",
                    "formatter": "standard"
                }
            },
            "loggers": {
                "": {
                    "handlers": ["file", "console"],
                    "level": "INFO",
                    "propagate": False
                }
            }
        }
        
        log_config_file = self.base_path / "logging-config.json"
        with open(log_config_file, 'w') as f:
            json.dump(log_config, f, indent=2)
        
        logger.info(f"📋 Created logging configuration: {log_config_file}")
    
    def full_setup(self):
        """Run complete setup process"""
        logger.info("🚀 Starting full orchestrator setup...")
        
        steps = [
            ("Checking prerequisites", self.check_prerequisites),
            ("Creating requirements file", lambda: self.create_requirements_file() or True),
            ("Installing dependencies", self.install_dependencies),
            ("Setting up directories", lambda: self.setup_directories() or True),
            ("Validating configuration", self.validate_configuration),
            ("Setting up logging", lambda: self.setup_logging() or True),
            ("Creating systemd service", lambda: self.create_systemd_service() or True),
            ("Creating cron job", lambda: self.create_cron_job() or True),
            ("Creating management scripts", lambda: self.create_management_scripts() or True),
            ("Testing orchestrator", self.test_orchestrator)
        ]
        
        failed_steps = []
        
        for step_name, step_function in steps:
            logger.info(f"📍 {step_name}...")
            try:
                if not step_function():
                    failed_steps.append(step_name)
                    logger.error(f"❌ {step_name} failed")
                else:
                    logger.info(f"✅ {step_name} completed")
            except Exception as e:
                logger.error(f"💥 {step_name} crashed: {e}")
                failed_steps.append(step_name)
        
        if failed_steps:
            logger.error(f"❌ Setup completed with {len(failed_steps)} failed steps:")
            for step in failed_steps:
                logger.error(f"  • {step}")
            return False
        else:
            logger.info("🎉 Full setup completed successfully!")
            logger.info("")
            logger.info("Next steps:")
            logger.info("1. Review configuration in orchestrator-config.json")
            logger.info("2. Set up API credentials for YouTube/Reddit if needed")
            logger.info("3. Choose deployment method:")
            logger.info("   • Manual: ./start-orchestrator.sh")
            logger.info("   • Cron: crontab orchestrator-cron")
            logger.info("   • Systemd: Follow systemd service instructions above")
            logger.info("4. Monitor with: ./status-orchestrator.sh")
            return True
    
    def uninstall(self):
        """Uninstall orchestrator and clean up"""
        logger.info("🗑️ Uninstalling orchestrator...")
        
        # Stop any running processes
        try:
            subprocess.run(["pkill", "-f", "automated-discovery-orchestrator.py"], 
                         capture_output=True)
        except:
            pass
        
        # Remove created files
        cleanup_files = [
            self.systemd_service_file,
            self.cron_file,
            "start-orchestrator.sh",
            "stop-orchestrator.sh", 
            "status-orchestrator.sh",
            "logging-config.json",
            "orchestrator.log",
            "orchestrator-state.json",
            "orchestrator-metrics.json",
            "orchestrator.lock"
        ]
        
        for file_name in cleanup_files:
            file_path = self.base_path / file_name
            if file_path.exists():
                file_path.unlink()
                logger.info(f"🗑️ Removed {file_path}")
        
        # Remove directories (if empty)
        cleanup_dirs = ["orchestrator-outputs"]
        for dir_name in cleanup_dirs:
            dir_path = self.base_path / dir_name
            if dir_path.exists():
                try:
                    shutil.rmtree(dir_path)
                    logger.info(f"🗑️ Removed directory {dir_path}")
                except:
                    logger.warning(f"⚠️ Could not remove {dir_path} (not empty?)")
        
        logger.info("✅ Uninstall completed")

def main():
    parser = argparse.ArgumentParser(description="Orchestrator Setup and Management")
    parser.add_argument("action", choices=["setup", "test", "uninstall", "install-deps", "validate"],
                       help="Action to perform")
    parser.add_argument("--base-path", type=Path, help="Base path for orchestrator")
    
    args = parser.parse_args()
    
    setup = OrchestratorSetup(base_path=args.base_path)
    
    if args.action == "setup":
        success = setup.full_setup()
        sys.exit(0 if success else 1)
    
    elif args.action == "test":
        success = setup.test_orchestrator()
        sys.exit(0 if success else 1)
    
    elif args.action == "uninstall":
        setup.uninstall()
    
    elif args.action == "install-deps":
        success = setup.install_dependencies()
        sys.exit(0 if success else 1)
    
    elif args.action == "validate":
        success = setup.validate_configuration()
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()