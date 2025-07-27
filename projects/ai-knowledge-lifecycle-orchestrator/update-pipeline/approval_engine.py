#!/usr/bin/env python3
"""
Approval Engine
AI Knowledge Lifecycle Orchestrator - Approval workflow management

This module provides sophisticated approval workflow management with tiered approval systems
based on change criticality, impact scope, and business rules for automated decision making.
"""

import asyncio
import logging
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Set
from enum import Enum
from dataclasses import dataclass, asdict
import json
import uuid

from ..change_detection.change_detector import TechnologyChange, ChangeType, ImpactLevel, UrgencyLevel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ApprovalStatus(Enum):
    """Approval request status"""
    PENDING = "pending"
    AUTO_APPROVED = "auto_approved"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"
    ESCALATED = "escalated"


class ApprovalTier(Enum):
    """Approval tier levels"""
    AUTOMATIC = "automatic"
    TECHNICAL_LEAD = "technical_lead"
    ENGINEERING_MANAGER = "engineering_manager"
    SENIOR_LEADERSHIP = "senior_leadership"
    EMERGENCY_OVERRIDE = "emergency_override"


@dataclass
class ApprovalRule:
    """Represents an approval rule"""
    rule_id: str
    name: str
    description: str
    conditions: Dict[str, Any]
    action: str  # auto_approve, require_approval, reject
    approval_tier: ApprovalTier
    timeout_hours: int
    priority: int
    
    def matches_change(self, change: TechnologyChange, impact_assessment) -> bool:
        """Check if this rule matches the given change"""
        try:
            # Check change type conditions
            if 'change_types' in self.conditions:
                if change.change_type.value not in self.conditions['change_types']:
                    return False
            
            # Check impact level conditions
            if 'impact_levels' in self.conditions:
                if change.impact_level.value not in self.conditions['impact_levels']:
                    return False
            
            # Check urgency level conditions
            if 'urgency_levels' in self.conditions:
                if change.urgency_level.value not in self.conditions['urgency_levels']:
                    return False
            
            # Check technology-specific conditions
            if 'technologies' in self.conditions:
                if change.technology_name not in self.conditions['technologies']:
                    return False
            
            # Check confidence score threshold
            if 'min_confidence' in self.conditions:
                if change.confidence_score < self.conditions['min_confidence']:
                    return False
            
            # Check affected files count (from impact assessment)
            if impact_assessment and 'max_affected_files' in self.conditions:
                if impact_assessment.affected_files_count > self.conditions['max_affected_files']:
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error matching rule {self.rule_id}: {e}")
            return False


@dataclass
class ApprovalRequest:
    """Represents an approval request"""
    request_id: str
    change: TechnologyChange
    impact_assessment: Any  # ImpactAssessment from impact_analyzer
    status: ApprovalStatus
    approval_tier: ApprovalTier
    requires_approval: bool
    justification: str
    applied_rule: Optional[ApprovalRule]
    created_at: datetime
    updated_at: datetime
    expires_at: Optional[datetime] = None
    approved_by: Optional[str] = None
    rejection_reason: Optional[str] = None
    emergency_override: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        data = asdict(self)
        data['status'] = self.status.value
        data['approval_tier'] = self.approval_tier.value
        data['created_at'] = self.created_at.isoformat()
        data['updated_at'] = self.updated_at.isoformat()
        if self.expires_at:
            data['expires_at'] = self.expires_at.isoformat()
        if self.applied_rule:
            data['applied_rule'] = {
                'rule_id': self.applied_rule.rule_id,
                'name': self.applied_rule.name,
                'action': self.applied_rule.action,
                'approval_tier': self.applied_rule.approval_tier.value
            }
        return data


class ApprovalEngine:
    """
    Sophisticated approval workflow management engine with tiered approval systems
    """
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the approval engine"""
        self.config = config
        self.approval_rules = self._initialize_approval_rules()
        self.active_requests: Dict[str, ApprovalRequest] = {}
        self.request_history: List[ApprovalRequest] = []
        
        # Performance tracking
        self.metrics = {
            'total_requests': 0,
            'auto_approved': 0,
            'manual_approved': 0,
            'rejected': 0,
            'expired': 0,
            'average_processing_time': 0.0,
            'tier_statistics': {tier.value: {'count': 0, 'avg_time': 0.0} for tier in ApprovalTier}
        }
        
        logger.info("Approval Engine initialized successfully")
    
    def _initialize_approval_rules(self) -> List[ApprovalRule]:
        """Initialize approval rules from configuration"""
        rules = []
        
        # Default approval rules if not in config
        default_rules = [
            # Emergency security updates - immediate approval
            {
                'rule_id': 'security_emergency',
                'name': 'Emergency Security Updates',
                'description': 'Auto-approve critical security updates',
                'conditions': {
                    'change_types': ['security_update'],
                    'urgency_levels': ['immediate', 'urgent'],
                    'min_confidence': 0.8
                },
                'action': 'auto_approve',
                'approval_tier': 'automatic',
                'timeout_hours': 1,
                'priority': 1
            },
            
            # Low impact changes - auto approve
            {
                'rule_id': 'low_impact_auto',
                'name': 'Low Impact Auto Approval',
                'description': 'Auto-approve low impact non-breaking changes',
                'conditions': {
                    'impact_levels': ['minimal', 'low'],
                    'change_types': ['bug_fix', 'feature_addition'],
                    'max_affected_files': 5,
                    'min_confidence': 0.7
                },
                'action': 'auto_approve',
                'approval_tier': 'automatic',
                'timeout_hours': 0,
                'priority': 2
            },
            
            # Breaking changes - require senior approval
            {
                'rule_id': 'breaking_changes',
                'name': 'Breaking Changes Approval',
                'description': 'Require senior leadership approval for breaking changes',
                'conditions': {
                    'change_types': ['breaking_change'],
                    'impact_levels': ['high', 'critical']
                },
                'action': 'require_approval',
                'approval_tier': 'senior_leadership',
                'timeout_hours': 48,
                'priority': 3
            },
            
            # Critical technologies - require technical lead approval
            {
                'rule_id': 'critical_tech',
                'name': 'Critical Technology Changes',
                'description': 'Require technical lead approval for critical technologies',
                'conditions': {
                    'technologies': ['React', 'TypeScript', 'Next.js', 'Node.js'],
                    'impact_levels': ['medium', 'high', 'critical']
                },
                'action': 'require_approval',
                'approval_tier': 'technical_lead',
                'timeout_hours': 24,
                'priority': 4
            },
            
            # High impact changes - require engineering manager approval
            {
                'rule_id': 'high_impact',
                'name': 'High Impact Changes',
                'description': 'Require engineering manager approval for high impact changes',
                'conditions': {
                    'impact_levels': ['high'],
                    'max_affected_files': 50
                },
                'action': 'require_approval',
                'approval_tier': 'engineering_manager',
                'timeout_hours': 24,
                'priority': 5
            },
            
            # Default rule - technical lead approval
            {
                'rule_id': 'default_approval',
                'name': 'Default Technical Approval',
                'description': 'Default rule requiring technical lead approval',
                'conditions': {},
                'action': 'require_approval',
                'approval_tier': 'technical_lead',
                'timeout_hours': 24,
                'priority': 10
            }
        ]
        
        # Load rules from config or use defaults
        rule_configs = self.config.get('approval_rules', default_rules)
        
        for rule_config in rule_configs:
            try:
                rule = ApprovalRule(
                    rule_id=rule_config['rule_id'],
                    name=rule_config['name'],
                    description=rule_config['description'],
                    conditions=rule_config['conditions'],
                    action=rule_config['action'],
                    approval_tier=ApprovalTier(rule_config['approval_tier']),
                    timeout_hours=rule_config['timeout_hours'],
                    priority=rule_config['priority']
                )
                rules.append(rule)
                
            except Exception as e:
                logger.error(f"Error loading approval rule {rule_config.get('rule_id', 'unknown')}: {e}")
        
        # Sort rules by priority
        rules.sort(key=lambda r: r.priority)
        
        logger.info(f"Loaded {len(rules)} approval rules")
        return rules
    
    async def process_approval_request(self, change: TechnologyChange, impact_assessment) -> ApprovalRequest:
        """
        Process an approval request for a technology change
        
        Args:
            change: The technology change requiring approval
            impact_assessment: Impact assessment results
            
        Returns:
            ApprovalRequest with decision and status
        """
        start_time = time.time()
        request_id = str(uuid.uuid4())
        
        try:
            logger.info(f"Processing approval request for {change.technology_name} change")
            
            # Find matching approval rule
            matching_rule = self._find_matching_rule(change, impact_assessment)
            
            # Create approval request
            request = ApprovalRequest(
                request_id=request_id,
                change=change,
                impact_assessment=impact_assessment,
                status=ApprovalStatus.PENDING,
                approval_tier=matching_rule.approval_tier,
                requires_approval=matching_rule.action != 'auto_approve',
                justification=self._generate_justification(change, impact_assessment, matching_rule),
                applied_rule=matching_rule,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            # Set expiration if required
            if matching_rule.timeout_hours > 0:
                request.expires_at = datetime.utcnow() + timedelta(hours=matching_rule.timeout_hours)
            
            # Process based on rule action
            if matching_rule.action == 'auto_approve':
                await self._auto_approve_request(request)
            elif matching_rule.action == 'reject':
                await self._reject_request(request, "Automatically rejected by rule")
            else:
                await self._queue_for_manual_approval(request)
            
            # Store request
            self.active_requests[request_id] = request
            
            # Update metrics
            processing_time = time.time() - start_time
            self._update_metrics(request, processing_time)
            
            logger.info(f"Approval request processed: {request.status.value} ({processing_time:.2f}s)")
            return request
            
        except Exception as e:
            logger.error(f"Error processing approval request: {e}")
            # Create error request
            error_request = ApprovalRequest(
                request_id=request_id,
                change=change,
                impact_assessment=impact_assessment,
                status=ApprovalStatus.REJECTED,
                approval_tier=ApprovalTier.AUTOMATIC,
                requires_approval=True,
                justification=f"Error processing request: {str(e)}",
                applied_rule=None,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                rejection_reason=str(e)
            )
            return error_request
    
    def _find_matching_rule(self, change: TechnologyChange, impact_assessment) -> ApprovalRule:
        """Find the first matching approval rule"""
        for rule in self.approval_rules:
            if rule.matches_change(change, impact_assessment):
                logger.info(f"Matched approval rule: {rule.name}")
                return rule
        
        # Should not happen with proper default rule, but fallback
        logger.warning("No matching approval rule found, using default")
        return self.approval_rules[-1]  # Last rule should be default
    
    def _generate_justification(self, change: TechnologyChange, impact_assessment, rule: ApprovalRule) -> str:
        """Generate justification for approval decision"""
        justification_parts = [
            f"Technology: {change.technology_name}",
            f"Change Type: {change.change_type.value}",
            f"Impact Level: {change.impact_level.value}",
            f"Urgency: {change.urgency_level.value}",
            f"Confidence: {change.confidence_score:.2f}",
            f"Applied Rule: {rule.name}"
        ]
        
        if impact_assessment:
            justification_parts.append(f"Affected Files: {impact_assessment.affected_files_count}")
        
        if change.old_version and change.new_version:
            justification_parts.append(f"Version Change: {change.old_version} -> {change.new_version}")
        
        return "; ".join(justification_parts)
    
    async def _auto_approve_request(self, request: ApprovalRequest):
        """Automatically approve a request"""
        request.status = ApprovalStatus.AUTO_APPROVED
        request.approved_by = "system"
        request.updated_at = datetime.utcnow()
        
        logger.info(f"Request {request.request_id} auto-approved")
    
    async def _reject_request(self, request: ApprovalRequest, reason: str):
        """Reject a request"""
        request.status = ApprovalStatus.REJECTED
        request.rejection_reason = reason
        request.updated_at = datetime.utcnow()
        
        logger.info(f"Request {request.request_id} rejected: {reason}")
    
    async def _queue_for_manual_approval(self, request: ApprovalRequest):
        """Queue request for manual approval"""
        request.status = ApprovalStatus.PENDING
        request.updated_at = datetime.utcnow()
        
        # In a real system, this would integrate with notification systems
        # For now, we'll simulate immediate approval based on configuration
        if self._should_simulate_approval(request):
            await self._simulate_manual_approval(request)
        
        logger.info(f"Request {request.request_id} queued for {request.approval_tier.value} approval")
    
    def _should_simulate_approval(self, request: ApprovalRequest) -> bool:
        """Determine if we should simulate manual approval for testing"""
        # Check configuration for simulation settings
        simulate_approvals = self.config.get('simulate_approvals', True)
        
        if not simulate_approvals:
            return False
        
        # Simulate different approval rates based on tier and change characteristics
        if request.approval_tier == ApprovalTier.TECHNICAL_LEAD:
            # Technical leads approve most changes except very high risk
            if (request.change.impact_level in [ImpactLevel.CRITICAL] and 
                request.change.change_type == ChangeType.BREAKING_CHANGE):
                return False  # Would require escalation
            return True
        
        elif request.approval_tier == ApprovalTier.ENGINEERING_MANAGER:
            # Engineering managers are more conservative
            if request.change.confidence_score < 0.8:
                return False
            return True
        
        elif request.approval_tier == ApprovalTier.SENIOR_LEADERSHIP:
            # Senior leadership very selective
            if (request.change.change_type == ChangeType.BREAKING_CHANGE and
                request.impact_assessment and 
                request.impact_assessment.affected_files_count > 20):
                return False
            return True
        
        return True
    
    async def _simulate_manual_approval(self, request: ApprovalRequest):
        """Simulate manual approval process"""
        # Simulate processing delay
        await asyncio.sleep(0.1)  # Small delay for realism
        
        # Approve the request
        request.status = ApprovalStatus.APPROVED
        request.approved_by = f"simulated_{request.approval_tier.value}"
        request.updated_at = datetime.utcnow()
        
        logger.info(f"Request {request.request_id} simulated approval by {request.approved_by}")
    
    async def manual_approve_request(self, request_id: str, approver: str, comments: str = None) -> bool:
        """Manually approve a pending request"""
        if request_id not in self.active_requests:
            logger.warning(f"Request {request_id} not found for approval")
            return False
        
        request = self.active_requests[request_id]
        
        if request.status != ApprovalStatus.PENDING:
            logger.warning(f"Request {request_id} not in pending status: {request.status.value}")
            return False
        
        request.status = ApprovalStatus.APPROVED
        request.approved_by = approver
        request.updated_at = datetime.utcnow()
        
        if comments:
            request.justification += f" | Approval comments: {comments}"
        
        logger.info(f"Request {request_id} manually approved by {approver}")
        return True
    
    async def manual_reject_request(self, request_id: str, rejector: str, reason: str) -> bool:
        """Manually reject a pending request"""
        if request_id not in self.active_requests:
            logger.warning(f"Request {request_id} not found for rejection")
            return False
        
        request = self.active_requests[request_id]
        
        if request.status != ApprovalStatus.PENDING:
            logger.warning(f"Request {request_id} not in pending status: {request.status.value}")
            return False
        
        request.status = ApprovalStatus.REJECTED
        request.rejection_reason = reason
        request.updated_at = datetime.utcnow()
        
        logger.info(f"Request {request_id} manually rejected by {rejector}: {reason}")
        return True
    
    async def emergency_override(self, request_id: str, override_by: str, justification: str) -> bool:
        """Apply emergency override to immediately approve a request"""
        if request_id not in self.active_requests:
            logger.warning(f"Request {request_id} not found for emergency override")
            return False
        
        request = self.active_requests[request_id]
        
        request.status = ApprovalStatus.APPROVED
        request.approved_by = override_by
        request.emergency_override = True
        request.justification += f" | EMERGENCY OVERRIDE: {justification}"
        request.updated_at = datetime.utcnow()
        
        logger.warning(f"Emergency override applied to request {request_id} by {override_by}")
        return True
    
    async def check_expired_requests(self):
        """Check for and handle expired approval requests"""
        current_time = datetime.utcnow()
        expired_requests = []
        
        for request_id, request in self.active_requests.items():
            if (request.status == ApprovalStatus.PENDING and 
                request.expires_at and 
                current_time > request.expires_at):
                expired_requests.append(request_id)
        
        for request_id in expired_requests:
            request = self.active_requests[request_id]
            request.status = ApprovalStatus.EXPIRED
            request.updated_at = current_time
            
            logger.warning(f"Request {request_id} expired")
            
            # Move to history
            self.request_history.append(request)
            del self.active_requests[request_id]
    
    def _update_metrics(self, request: ApprovalRequest, processing_time: float):
        """Update performance metrics"""
        self.metrics['total_requests'] += 1
        
        # Update status counts
        if request.status == ApprovalStatus.AUTO_APPROVED:
            self.metrics['auto_approved'] += 1
        elif request.status == ApprovalStatus.APPROVED:
            self.metrics['manual_approved'] += 1
        elif request.status == ApprovalStatus.REJECTED:
            self.metrics['rejected'] += 1
        elif request.status == ApprovalStatus.EXPIRED:
            self.metrics['expired'] += 1
        
        # Update average processing time
        total_requests = self.metrics['total_requests']
        current_avg = self.metrics['average_processing_time']
        self.metrics['average_processing_time'] = (
            (current_avg * (total_requests - 1) + processing_time) / total_requests
        )
        
        # Update tier statistics
        tier_key = request.approval_tier.value
        tier_stats = self.metrics['tier_statistics'][tier_key]
        tier_stats['count'] += 1
        
        tier_avg = tier_stats['avg_time']
        tier_count = tier_stats['count']
        tier_stats['avg_time'] = (tier_avg * (tier_count - 1) + processing_time) / tier_count
    
    async def get_pending_requests(self) -> List[Dict[str, Any]]:
        """Get all pending approval requests"""
        pending = []
        for request in self.active_requests.values():
            if request.status == ApprovalStatus.PENDING:
                pending.append(request.to_dict())
        return pending
    
    async def get_request_status(self, request_id: str) -> Optional[Dict[str, Any]]:
        """Get status of a specific request"""
        # Check active requests
        if request_id in self.active_requests:
            return self.active_requests[request_id].to_dict()
        
        # Check history
        for request in self.request_history:
            if request.request_id == request_id:
                return request.to_dict()
        
        return None
    
    async def get_approval_metrics(self) -> Dict[str, Any]:
        """Get approval engine metrics"""
        # Calculate approval rates
        total = max(self.metrics['total_requests'], 1)
        
        return {
            'total_requests': self.metrics['total_requests'],
            'approval_rates': {
                'auto_approved': self.metrics['auto_approved'] / total,
                'manual_approved': self.metrics['manual_approved'] / total,
                'rejected': self.metrics['rejected'] / total,
                'expired': self.metrics['expired'] / total
            },
            'average_processing_time': self.metrics['average_processing_time'],
            'tier_statistics': self.metrics['tier_statistics'],
            'active_requests': len(self.active_requests),
            'pending_requests': len([r for r in self.active_requests.values() 
                                   if r.status == ApprovalStatus.PENDING]),
            'timestamp': datetime.utcnow().isoformat()
        }
    
    async def cleanup_completed_requests(self, max_history: int = 1000):
        """Clean up completed requests and maintain history limit"""
        # Move completed active requests to history
        completed_requests = []
        for request_id, request in list(self.active_requests.items()):
            if request.status in [ApprovalStatus.APPROVED, ApprovalStatus.REJECTED, 
                                ApprovalStatus.EXPIRED, ApprovalStatus.AUTO_APPROVED]:
                completed_requests.append(request_id)
        
        for request_id in completed_requests:
            request = self.active_requests[request_id]
            self.request_history.append(request)
            del self.active_requests[request_id]
        
        # Limit history size
        if len(self.request_history) > max_history:
            self.request_history = self.request_history[-max_history//2:]
        
        logger.info(f"Cleaned up {len(completed_requests)} completed requests")


async def main():
    """Main function for testing"""
    try:
        # Test configuration
        config = {
            'simulate_approvals': True,
            'approval_rules': []  # Will use defaults
        }
        
        # Initialize approval engine
        engine = ApprovalEngine(config)
        
        # Get metrics
        metrics = await engine.get_approval_metrics()
        print("Approval Engine Metrics:")
        print(json.dumps(metrics, indent=2))
        
        # Get pending requests
        pending = await engine.get_pending_requests()
        print(f"\nPending requests: {len(pending)}")
        
        print("\nApproval Engine test completed successfully!")
        
    except Exception as e:
        print(f"Error testing approval engine: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(asyncio.run(main()))