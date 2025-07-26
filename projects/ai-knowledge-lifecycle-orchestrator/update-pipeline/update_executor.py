#!/usr/bin/env python3
"""
Update Executor
AI Knowledge Lifecycle Orchestrator - Automated update execution with validation

This module provides sophisticated update execution capabilities with rollback functionality,
quality validation, and comprehensive error handling for AI instruction file updates.
"""

import asyncio
import logging
import time
import shutil
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
from dataclasses import dataclass, asdict
from pathlib import Path
import json
import re
import tempfile

from .approval_engine import ApprovalRequest
from .impact_analyzer import ImpactAssessment, AffectedFile
from ..change_detection.change_detector import TechnologyChange, ChangeType
from ..knowledge_vault_integration import KnowledgeVaultIntegration

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UpdateStatus(Enum):
    """Update execution status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"
    SKIPPED = "skipped"


class ValidationResult(Enum):
    """Validation result status"""
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"
    SKIPPED = "skipped"


@dataclass
class BackupInfo:
    """Information about file backup"""
    original_path: str
    backup_path: str
    backup_timestamp: datetime
    file_hash: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['backup_timestamp'] = self.backup_timestamp.isoformat()
        return data


@dataclass
class UpdateResult:
    """Result of an update operation"""
    file_path: str
    file_type: str
    status: UpdateStatus
    changes_made: Optional[str]
    backup_info: Optional[BackupInfo]
    validation_results: Dict[str, Any]
    quality_score: Optional[float]
    execution_time: float
    error_details: Optional[str]
    rollback_available: bool
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['status'] = self.status.value
        if self.backup_info:
            data['backup_info'] = self.backup_info.to_dict()
        return data


class FileUpdateStrategy:
    """Base class for file update strategies"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    async def can_handle(self, file_path: str, file_type: str) -> bool:
        """Check if this strategy can handle the file type"""
        raise NotImplementedError
    
    async def update_file(self, file_path: str, change: TechnologyChange, affected_file: AffectedFile) -> Tuple[bool, str, List[str]]:
        """
        Update the file based on the change
        
        Returns:
            Tuple of (success, changes_description, list_of_changes)
        """
        raise NotImplementedError
    
    async def validate_update(self, file_path: str, original_content: str, updated_content: str) -> Dict[str, Any]:
        """Validate the update quality"""
        raise NotImplementedError


class ClaudeMdUpdateStrategy(FileUpdateStrategy):
    """Update strategy for CLAUDE.md files"""
    
    async def can_handle(self, file_path: str, file_type: str) -> bool:
        """Check if this strategy can handle the file type"""
        return file_type == 'claude_md' or 'CLAUDE.md' in Path(file_path).name
    
    async def update_file(self, file_path: str, change: TechnologyChange, affected_file: AffectedFile) -> Tuple[bool, str, List[str]]:
        """Update CLAUDE.md file with technology changes"""
        try:
            path = Path(file_path)
            if not path.exists():
                return False, f"File not found: {file_path}", []
            
            # Read current content
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            changes_made = []
            
            # Update version references
            if change.old_version and change.new_version:
                # Pattern for version updates
                version_patterns = [
                    rf'\b{re.escape(change.technology_name)}\s*[:\-]\s*["\']?{re.escape(change.old_version)}',
                    rf'{re.escape(change.old_version)}',
                    rf'version\s*[:\-]\s*["\']?{re.escape(change.old_version)}'
                ]
                
                for pattern in version_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        content = re.sub(
                            pattern,
                            lambda m: m.group(0).replace(change.old_version, change.new_version),
                            content,
                            flags=re.IGNORECASE
                        )
                        changes_made.append(f"Updated version reference from {change.old_version} to {change.new_version}")
            
            # Update technology-specific patterns
            if change.technology_name.lower() == 'react':
                content = await self._update_react_patterns(content, change, changes_made)
            elif change.technology_name.lower() == 'typescript':
                content = await self._update_typescript_patterns(content, change, changes_made)
            elif change.technology_name.lower() == 'next.js':
                content = await self._update_nextjs_patterns(content, change, changes_made)
            
            # Add change notification if significant changes
            if change.change_type in [ChangeType.BREAKING_CHANGE, ChangeType.SECURITY_UPDATE]:
                content = await self._add_change_notification(content, change, changes_made)
            
            # Write updated content if changes were made
            if content != original_content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                changes_description = f"Updated {len(changes_made)} patterns in {path.name}"
                return True, changes_description, changes_made
            else:
                return True, "No changes required", []
                
        except Exception as e:
            logger.error(f"Error updating CLAUDE.md file {file_path}: {e}")
            return False, f"Update failed: {str(e)}", []
    
    async def _update_react_patterns(self, content: str, change: TechnologyChange, changes_made: List[str]) -> str:
        """Update React-specific patterns"""
        if change.change_type == ChangeType.BREAKING_CHANGE:
            # Update deprecated hooks patterns
            if 'useEffect' in content and change.new_version and change.new_version.startswith('18'):
                # Add note about React 18 concurrent features
                if 'React 18' not in content:
                    content = content.replace(
                        'useEffect',
                        'useEffect // Note: React 18 introduces concurrent features'
                    )
                    changes_made.append("Added React 18 concurrent features note")
        
        return content
    
    async def _update_typescript_patterns(self, content: str, change: TechnologyChange, changes_made: List[str]) -> str:
        """Update TypeScript-specific patterns"""
        if change.change_type == ChangeType.FEATURE_ADDITION:
            # Update type patterns if new features are mentioned
            if 'satisfies' not in content and change.new_version and float(change.new_version.split('.')[0]) >= 4:
                # Could add satisfies operator examples
                pass
        
        return content
    
    async def _update_nextjs_patterns(self, content: str, change: TechnologyChange, changes_made: List[str]) -> str:
        """Update Next.js-specific patterns"""
        if change.change_type == ChangeType.BREAKING_CHANGE:
            # Update app router patterns
            if 'pages/' in content and change.new_version and change.new_version.startswith('13'):
                content = content.replace(
                    'pages/',
                    'pages/ # Note: Consider migrating to app/ directory in Next.js 13+'
                )
                changes_made.append("Added Next.js 13+ app directory migration note")
        
        return content
    
    async def _add_change_notification(self, content: str, change: TechnologyChange, changes_made: List[str]) -> str:
        """Add change notification to file"""
        notification = f"\n<!-- Updated for {change.technology_name} {change.new_version or 'latest'} - {datetime.utcnow().strftime('%Y-%m-%d')} -->\n"
        
        # Add at the beginning after any frontmatter
        lines = content.split('\n')
        insert_line = 0
        
        # Skip YAML frontmatter if present
        if lines and lines[0].strip() == '---':
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == '---':
                    insert_line = i + 1
                    break
        
        lines.insert(insert_line, notification.strip())
        changes_made.append(f"Added change notification for {change.technology_name}")
        
        return '\n'.join(lines)
    
    async def validate_update(self, file_path: str, original_content: str, updated_content: str) -> Dict[str, Any]:
        """Validate CLAUDE.md update quality"""
        validation = {
            'overall_result': ValidationResult.PASSED.value,
            'checks_performed': [],
            'issues_found': [],
            'quality_score': 1.0,
            'recommendations': []
        }
        
        try:
            # Check content length didn't change dramatically
            original_length = len(original_content)
            updated_length = len(updated_content)
            length_change_ratio = abs(updated_length - original_length) / max(original_length, 1)
            
            validation['checks_performed'].append('content_length_check')
            
            if length_change_ratio > 0.1:  # More than 10% change
                validation['issues_found'].append(f"Significant content length change: {length_change_ratio:.1%}")
                validation['quality_score'] -= 0.1
            
            # Check for broken markdown syntax
            validation['checks_performed'].append('markdown_syntax_check')
            if updated_content.count('```') % 2 != 0:
                validation['issues_found'].append("Unmatched code block markers")
                validation['quality_score'] -= 0.2
            
            # Check for valid cross-references
            validation['checks_performed'].append('cross_reference_check')
            cross_refs = re.findall(r'@([a-zA-Z0-9\-_/\.]+)', updated_content)
            for ref in cross_refs[:5]:  # Check first 5
                ref_path = Path(f"/Users/georgiospilitsoglou/Developer/projects/mypromptflow/{ref}")
                if not ref_path.exists():
                    validation['issues_found'].append(f"Broken cross-reference: @{ref}")
                    validation['quality_score'] -= 0.05
            
            # Determine overall result
            if validation['quality_score'] >= 0.8:
                validation['overall_result'] = ValidationResult.PASSED.value
            elif validation['quality_score'] >= 0.6:
                validation['overall_result'] = ValidationResult.WARNING.value
            else:
                validation['overall_result'] = ValidationResult.FAILED.value
            
            # Generate recommendations
            if validation['issues_found']:
                validation['recommendations'].append("Review and fix identified issues")
                
            if length_change_ratio > 0.05:
                validation['recommendations'].append("Verify all intended changes were applied correctly")
            
        except Exception as e:
            logger.error(f"Error validating update: {e}")
            validation['overall_result'] = ValidationResult.FAILED.value
            validation['issues_found'].append(f"Validation error: {str(e)}")
            validation['quality_score'] = 0.0
        
        return validation


class CommandFileUpdateStrategy(FileUpdateStrategy):
    """Update strategy for command files"""
    
    async def can_handle(self, file_path: str, file_type: str) -> bool:
        """Check if this strategy can handle the file type"""
        return file_type == 'command_file' or '.claude/commands' in file_path
    
    async def update_file(self, file_path: str, change: TechnologyChange, affected_file: AffectedFile) -> Tuple[bool, str, List[str]]:
        """Update command file with technology changes"""
        try:
            path = Path(file_path)
            if not path.exists():
                return False, f"File not found: {file_path}", []
            
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            changes_made = []
            
            # Update command syntax and tool references
            if change.old_version and change.new_version:
                # Update CLI commands with version references
                cli_patterns = [
                    rf'(npm install\s+{re.escape(change.technology_name)}@){re.escape(change.old_version)}',
                    rf'(yarn add\s+{re.escape(change.technology_name)}@){re.escape(change.old_version)}',
                    rf'({re.escape(change.technology_name)}@){re.escape(change.old_version)}'
                ]
                
                for pattern in cli_patterns:
                    if re.search(pattern, content, re.IGNORECASE):
                        content = re.sub(pattern, rf'\g<1>{change.new_version}', content, flags=re.IGNORECASE)
                        changes_made.append(f"Updated CLI version reference to {change.new_version}")
            
            # Update technology-specific command patterns
            if change.technology_name.lower() == 'docker':
                content = await self._update_docker_commands(content, change, changes_made)
            elif change.technology_name.lower() == 'node.js':
                content = await self._update_nodejs_commands(content, change, changes_made)
            
            # Write updated content if changes were made
            if content != original_content:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                changes_description = f"Updated {len(changes_made)} command patterns in {path.name}"
                return True, changes_description, changes_made
            else:
                return True, "No changes required", []
                
        except Exception as e:
            logger.error(f"Error updating command file {file_path}: {e}")
            return False, f"Update failed: {str(e)}", []
    
    async def _update_docker_commands(self, content: str, change: TechnologyChange, changes_made: List[str]) -> str:
        """Update Docker-specific commands"""
        if change.new_version:
            # Update Docker image tags
            content = re.sub(
                r'(FROM\s+[^\s:]+:)([^\s]+)',
                rf'\g<1>{change.new_version}',
                content
            )
            changes_made.append(f"Updated Docker image tag to {change.new_version}")
        
        return content
    
    async def _update_nodejs_commands(self, content: str, change: TechnologyChange, changes_made: List[str]) -> str:
        """Update Node.js-specific commands"""
        if change.new_version:
            # Update Node.js version in commands
            content = re.sub(
                r'(node --version|node -v)',
                rf'# Node.js {change.new_version}',
                content
            )
            changes_made.append(f"Updated Node.js version reference to {change.new_version}")
        
        return content
    
    async def validate_update(self, file_path: str, original_content: str, updated_content: str) -> Dict[str, Any]:
        """Validate command file update quality"""
        validation = {
            'overall_result': ValidationResult.PASSED.value,
            'checks_performed': ['syntax_check', 'command_validity_check'],
            'issues_found': [],
            'quality_score': 1.0,
            'recommendations': []
        }
        
        try:
            # Check for valid command syntax
            code_blocks = re.findall(r'```(?:bash|sh)?\s*\n(.*?)\n```', updated_content, re.DOTALL)
            for block in code_blocks:
                if not block.strip():
                    validation['issues_found'].append("Empty code block found")
                    validation['quality_score'] -= 0.1
            
            # Check for common command issues
            if 'sudo' in updated_content:
                validation['issues_found'].append("Warning: sudo usage found")
                validation['quality_score'] -= 0.05
            
            # Determine overall result
            if validation['quality_score'] >= 0.8:
                validation['overall_result'] = ValidationResult.PASSED.value
            elif validation['quality_score'] >= 0.6:
                validation['overall_result'] = ValidationResult.WARNING.value
            else:
                validation['overall_result'] = ValidationResult.FAILED.value
                
        except Exception as e:
            logger.error(f"Error validating command update: {e}")
            validation['overall_result'] = ValidationResult.FAILED.value
            validation['quality_score'] = 0.0
        
        return validation


class UpdateExecutor:
    """
    Sophisticated update execution engine with rollback capabilities and quality validation
    """
    
    def __init__(self, knowledge_vault: KnowledgeVaultIntegration, config: Dict[str, Any]):
        """Initialize the update executor"""
        self.knowledge_vault = knowledge_vault
        self.config = config
        
        # Execution configuration
        self.batch_size = config.get('batch_size', 10)
        self.validation_enabled = config.get('validation_enabled', True)
        self.rollback_on_failure = config.get('rollback_on_failure', True)
        self.backup_enabled = config.get('backup_enabled', True)
        
        # Initialize update strategies
        self.update_strategies = [
            ClaudeMdUpdateStrategy(config),
            CommandFileUpdateStrategy(config)
        ]
        
        # Backup management
        self.backup_directory = Path(config.get('backup_directory', 
            '/Users/georgiospilitsoglou/Developer/projects/mypromptflow/.backups'))
        self.backup_directory.mkdir(parents=True, exist_ok=True)
        
        # Performance tracking
        self.metrics = {
            'total_updates': 0,
            'successful_updates': 0,
            'failed_updates': 0,
            'rollbacks_performed': 0,
            'average_update_time': 0.0,
            'batch_statistics': {
                'total_batches': 0,
                'successful_batches': 0,
                'average_batch_size': 0.0
            }
        }
        
        logger.info("Update Executor initialized successfully")
    
    async def execute_updates(self, change: TechnologyChange, impact_assessment: ImpactAssessment, 
                            approval_request: ApprovalRequest) -> List[UpdateResult]:
        """
        Execute updates for all affected files
        
        Args:
            change: The technology change
            impact_assessment: Impact analysis results
            approval_request: Approval decision
            
        Returns:
            List of update results
        """
        start_time = time.time()
        
        try:
            logger.info(f"Executing updates for {len(impact_assessment.affected_files)} files")
            
            # Process files in batches
            results = []
            affected_files = impact_assessment.affected_files
            
            for i in range(0, len(affected_files), self.batch_size):
                batch = affected_files[i:i + self.batch_size]
                batch_results = await self._execute_batch(change, batch, f"batch_{i // self.batch_size + 1}")
                results.extend(batch_results)
                
                # Check for failures and determine if we should continue
                batch_failures = [r for r in batch_results if r.status == UpdateStatus.FAILED]
                if batch_failures and len(batch_failures) / len(batch_results) > 0.5:
                    logger.warning(f"High failure rate in batch ({len(batch_failures)}/{len(batch_results)})")
                    if self.rollback_on_failure:
                        await self._rollback_batch_results(batch_results)
                        break
            
            # Update metrics
            execution_time = time.time() - start_time
            self._update_metrics(results, execution_time)
            
            successful_updates = len([r for r in results if r.status == UpdateStatus.SUCCESS])
            logger.info(f"Update execution completed: {successful_updates}/{len(results)} successful ({execution_time:.2f}s)")
            
            return results
            
        except Exception as e:
            logger.error(f"Error executing updates: {e}")
            return []
    
    async def _execute_batch(self, change: TechnologyChange, affected_files: List[AffectedFile], batch_id: str) -> List[UpdateResult]:
        """Execute updates for a batch of files"""
        logger.info(f"Processing {batch_id} with {len(affected_files)} files")
        
        batch_results = []
        
        # Execute updates in parallel within the batch
        tasks = []
        for affected_file in affected_files:
            task = self._execute_single_update(change, affected_file)
            tasks.append(task)
        
        # Wait for all updates in the batch to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                # Handle exception case
                error_result = UpdateResult(
                    file_path=affected_files[i].file_path,
                    file_type=affected_files[i].file_type,
                    status=UpdateStatus.FAILED,
                    changes_made=None,
                    backup_info=None,
                    validation_results={'error': str(result)},
                    quality_score=0.0,
                    execution_time=0.0,
                    error_details=str(result),
                    rollback_available=False
                )
                batch_results.append(error_result)
            else:
                batch_results.append(result)
        
        # Update batch metrics
        self.metrics['batch_statistics']['total_batches'] += 1
        successful_batch_updates = len([r for r in batch_results if r.status == UpdateStatus.SUCCESS])
        
        if successful_batch_updates == len(batch_results):
            self.metrics['batch_statistics']['successful_batches'] += 1
        
        # Update average batch size
        total_batches = self.metrics['batch_statistics']['total_batches']
        current_avg = self.metrics['batch_statistics']['average_batch_size']
        self.metrics['batch_statistics']['average_batch_size'] = (
            (current_avg * (total_batches - 1) + len(affected_files)) / total_batches
        )
        
        return batch_results
    
    async def _execute_single_update(self, change: TechnologyChange, affected_file: AffectedFile) -> UpdateResult:
        """Execute update for a single file"""
        start_time = time.time()
        
        try:
            logger.debug(f"Updating file: {affected_file.file_path}")
            
            # Create backup if enabled
            backup_info = None
            if self.backup_enabled:
                backup_info = await self._create_backup(affected_file.file_path)
            
            # Find appropriate update strategy
            strategy = await self._find_update_strategy(affected_file.file_path, affected_file.file_type)
            if not strategy:
                return UpdateResult(
                    file_path=affected_file.file_path,
                    file_type=affected_file.file_type,
                    status=UpdateStatus.SKIPPED,
                    changes_made="No suitable update strategy found",
                    backup_info=backup_info,
                    validation_results={'skipped': True},
                    quality_score=None,
                    execution_time=time.time() - start_time,
                    error_details=None,
                    rollback_available=backup_info is not None
                )
            
            # Read original content for validation
            original_content = ""
            path = Path(affected_file.file_path)
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    original_content = f.read()
            
            # Execute the update
            success, changes_description, changes_list = await strategy.update_file(
                affected_file.file_path, change, affected_file
            )
            
            if not success:
                return UpdateResult(
                    file_path=affected_file.file_path,
                    file_type=affected_file.file_type,
                    status=UpdateStatus.FAILED,
                    changes_made=None,
                    backup_info=backup_info,
                    validation_results={'error': changes_description},
                    quality_score=0.0,
                    execution_time=time.time() - start_time,
                    error_details=changes_description,
                    rollback_available=backup_info is not None
                )
            
            # Validate the update if enabled
            validation_results = {}
            quality_score = 1.0
            
            if self.validation_enabled:
                updated_content = ""
                if path.exists():
                    with open(path, 'r', encoding='utf-8') as f:
                        updated_content = f.read()
                
                validation_results = await strategy.validate_update(
                    affected_file.file_path, original_content, updated_content
                )
                quality_score = validation_results.get('quality_score', 1.0)
                
                # Check if validation failed critically
                if validation_results.get('overall_result') == ValidationResult.FAILED.value:
                    if self.rollback_on_failure and backup_info:
                        await self._restore_from_backup(backup_info)
                        return UpdateResult(
                            file_path=affected_file.file_path,
                            file_type=affected_file.file_type,
                            status=UpdateStatus.ROLLED_BACK,
                            changes_made=changes_description,
                            backup_info=backup_info,
                            validation_results=validation_results,
                            quality_score=quality_score,
                            execution_time=time.time() - start_time,
                            error_details="Update rolled back due to validation failure",
                            rollback_available=False
                        )
            
            return UpdateResult(
                file_path=affected_file.file_path,
                file_type=affected_file.file_type,
                status=UpdateStatus.SUCCESS,
                changes_made=changes_description,
                backup_info=backup_info,
                validation_results=validation_results,
                quality_score=quality_score,
                execution_time=time.time() - start_time,
                error_details=None,
                rollback_available=backup_info is not None
            )
            
        except Exception as e:
            logger.error(f"Error updating file {affected_file.file_path}: {e}")
            return UpdateResult(
                file_path=affected_file.file_path,
                file_type=affected_file.file_type,
                status=UpdateStatus.FAILED,
                changes_made=None,
                backup_info=None,
                validation_results={'error': str(e)},
                quality_score=0.0,
                execution_time=time.time() - start_time,
                error_details=str(e),
                rollback_available=False
            )
    
    async def _find_update_strategy(self, file_path: str, file_type: str) -> Optional[FileUpdateStrategy]:
        """Find appropriate update strategy for a file"""
        for strategy in self.update_strategies:
            if await strategy.can_handle(file_path, file_type):
                return strategy
        return None
    
    async def _create_backup(self, file_path: str) -> Optional[BackupInfo]:
        """Create backup of a file before updating"""
        try:
            source_path = Path(file_path)
            if not source_path.exists():
                return None
            
            # Generate backup filename with timestamp
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            backup_filename = f"{source_path.name}_{timestamp}.backup"
            backup_path = self.backup_directory / backup_filename
            
            # Create backup
            shutil.copy2(source_path, backup_path)
            
            # Calculate file hash for integrity verification
            with open(source_path, 'rb') as f:
                file_hash = hashlib.sha256(f.read()).hexdigest()
            
            backup_info = BackupInfo(
                original_path=str(source_path),
                backup_path=str(backup_path),
                backup_timestamp=datetime.utcnow(),
                file_hash=file_hash
            )
            
            logger.debug(f"Created backup: {backup_path}")
            return backup_info
            
        except Exception as e:
            logger.error(f"Error creating backup for {file_path}: {e}")
            return None
    
    async def _restore_from_backup(self, backup_info: BackupInfo) -> bool:
        """Restore file from backup"""
        try:
            backup_path = Path(backup_info.backup_path)
            original_path = Path(backup_info.original_path)
            
            if not backup_path.exists():
                logger.error(f"Backup file not found: {backup_path}")
                return False
            
            # Verify backup integrity
            with open(backup_path, 'rb') as f:
                backup_hash = hashlib.sha256(f.read()).hexdigest()
            
            if backup_hash != backup_info.file_hash:
                logger.error(f"Backup integrity check failed for {backup_path}")
                return False
            
            # Restore from backup
            shutil.copy2(backup_path, original_path)
            
            logger.info(f"Restored file from backup: {original_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error restoring from backup: {e}")
            return False
    
    async def _rollback_batch_results(self, batch_results: List[UpdateResult]):
        """Rollback all successful updates in a batch"""
        logger.warning("Rolling back batch due to high failure rate")
        
        for result in batch_results:
            if result.status == UpdateStatus.SUCCESS and result.backup_info:
                success = await self._restore_from_backup(result.backup_info)
                if success:
                    result.status = UpdateStatus.ROLLED_BACK
                    result.error_details = "Rolled back due to batch failure"
                    self.metrics['rollbacks_performed'] += 1
    
    async def rollback_updates(self, update_results: List[UpdateResult]) -> List[UpdateResult]:
        """Rollback a list of updates"""
        logger.info(f"Rolling back {len(update_results)} updates")
        
        rollback_results = []
        
        for result in update_results:
            if result.status == UpdateStatus.SUCCESS and result.backup_info:
                success = await self._restore_from_backup(result.backup_info)
                
                rollback_result = UpdateResult(
                    file_path=result.file_path,
                    file_type=result.file_type,
                    status=UpdateStatus.SUCCESS if success else UpdateStatus.FAILED,
                    changes_made=f"Rollback {'successful' if success else 'failed'}",
                    backup_info=result.backup_info,
                    validation_results={'rollback': success},
                    quality_score=1.0 if success else 0.0,
                    execution_time=0.1,  # Rollback is typically fast
                    error_details=None if success else "Rollback failed",
                    rollback_available=False
                )
                rollback_results.append(rollback_result)
                
                if success:
                    self.metrics['rollbacks_performed'] += 1
            else:
                # Cannot rollback
                rollback_result = UpdateResult(
                    file_path=result.file_path,
                    file_type=result.file_type,
                    status=UpdateStatus.FAILED,
                    changes_made="Cannot rollback - no backup available",
                    backup_info=None,
                    validation_results={'rollback_unavailable': True},
                    quality_score=0.0,
                    execution_time=0.0,
                    error_details="No backup available for rollback",
                    rollback_available=False
                )
                rollback_results.append(rollback_result)
        
        return rollback_results
    
    def _update_metrics(self, results: List[UpdateResult], execution_time: float):
        """Update performance metrics"""
        self.metrics['total_updates'] += len(results)
        
        successful_updates = len([r for r in results if r.status == UpdateStatus.SUCCESS])
        failed_updates = len([r for r in results if r.status == UpdateStatus.FAILED])
        
        self.metrics['successful_updates'] += successful_updates
        self.metrics['failed_updates'] += failed_updates
        
        # Update average execution time
        total_updates = self.metrics['total_updates']
        current_avg = self.metrics['average_update_time']
        
        if total_updates > 0:
            avg_per_file = execution_time / len(results) if results else 0
            self.metrics['average_update_time'] = (
                (current_avg * (total_updates - len(results)) + avg_per_file * len(results)) / total_updates
            )
    
    async def cleanup_old_backups(self, days_to_keep: int = 30):
        """Clean up old backup files"""
        try:
            cutoff_time = datetime.utcnow().timestamp() - (days_to_keep * 24 * 3600)
            
            cleaned_count = 0
            for backup_file in self.backup_directory.glob('*.backup'):
                if backup_file.stat().st_mtime < cutoff_time:
                    backup_file.unlink()
                    cleaned_count += 1
            
            logger.info(f"Cleaned up {cleaned_count} old backup files")
            
        except Exception as e:
            logger.error(f"Error cleaning up backups: {e}")
    
    async def get_update_metrics(self) -> Dict[str, Any]:
        """Get update execution metrics"""
        return {
            'total_updates': self.metrics['total_updates'],
            'successful_updates': self.metrics['successful_updates'],
            'failed_updates': self.metrics['failed_updates'],
            'rollbacks_performed': self.metrics['rollbacks_performed'],
            'success_rate': self.metrics['successful_updates'] / max(self.metrics['total_updates'], 1),
            'average_update_time': self.metrics['average_update_time'],
            'batch_statistics': self.metrics['batch_statistics'],
            'backup_directory': str(self.backup_directory),
            'backup_count': len(list(self.backup_directory.glob('*.backup'))),
            'timestamp': datetime.utcnow().isoformat()
        }


async def main():
    """Main function for testing"""
    try:
        # Initialize components
        knowledge_vault = KnowledgeVaultIntegration()
        config = {
            'batch_size': 5,
            'validation_enabled': True,
            'rollback_on_failure': True,
            'backup_enabled': True
        }
        
        executor = UpdateExecutor(knowledge_vault, config)
        
        # Get metrics
        metrics = await executor.get_update_metrics()
        print("Update Executor Metrics:")
        print(json.dumps(metrics, indent=2))
        
        # Test cleanup
        await executor.cleanup_old_backups()
        
        print("\nUpdate Executor test completed successfully!")
        
    except Exception as e:
        print(f"Error testing update executor: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(asyncio.run(main()))