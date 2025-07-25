#!/usr/bin/env python3
"""
Security Assessor
AI Knowledge Lifecycle Orchestrator - PR Validation Enhancement

Performs comprehensive security assessment of PR changes, including vulnerability
scanning, security pattern analysis, and current security recommendations based
on Knowledge Vault data and industry best practices.
"""

import re
import hashlib
import logging
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import json


@dataclass
class SecurityFinding:
    """Security finding data structure"""
    finding_id: str
    finding_type: str
    severity: str  # 'critical', 'high', 'medium', 'low', 'info'
    category: str  # 'vulnerability', 'weak_crypto', 'injection', 'exposure', etc.
    file_path: str
    line_number: Optional[int]
    description: str
    recommendation: str
    cwe_id: Optional[str]
    cvss_score: Optional[float]
    confidence: float
    evidence: Dict[str, Any]
    remediation_effort: str  # 'low', 'medium', 'high'


@dataclass
class SecurityMetrics:
    """Security metrics data structure"""
    total_findings: int
    findings_by_severity: Dict[str, int]
    security_score: float
    risk_level: str
    coverage_percentage: float
    scan_timestamp: str


@dataclass
class SecurityAssessmentResult:
    """Complete security assessment result"""
    pr_id: str
    security_score: float
    risk_level: str
    findings: List[SecurityFinding]
    critical_issues: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]
    security_metrics: SecurityMetrics
    vulnerability_analysis: Dict[str, Any]
    dependency_security: Dict[str, Any]
    compliance_status: Dict[str, Any]
    processing_time: float


class SecurityAssessor:
    """Performs comprehensive security assessment of PR changes"""
    
    def __init__(self, knowledge_vault, config: Dict[str, Any]):
        """Initialize the security assessor"""
        self.knowledge_vault = knowledge_vault
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Load security rules and patterns
        self.security_patterns = self._load_security_patterns()
        self.vulnerability_database = self._load_vulnerability_database()
        self.security_policies = self._load_security_policies()
        
        self.logger.info("Security Assessor initialized")
    
    def _load_security_patterns(self) -> Dict[str, Any]:
        """Load security detection patterns"""
        return {
            'injection_vulnerabilities': {
                'sql_injection': [
                    {
                        'pattern': r'(SELECT|INSERT|UPDATE|DELETE).*\+.*["\']',
                        'description': 'Potential SQL injection via string concatenation',
                        'severity': 'high',
                        'cwe': 'CWE-89',
                        'confidence': 0.8
                    },
                    {
                        'pattern': r'execute\s*\(\s*["\'].*\+.*["\']',
                        'description': 'SQL execution with concatenated user input',
                        'severity': 'critical',
                        'cwe': 'CWE-89',
                        'confidence': 0.9
                    }
                ],
                'command_injection': [
                    {
                        'pattern': r'(exec|system|shell_exec|eval)\s*\(\s*.*\$',
                        'description': 'Potential command injection with user input',
                        'severity': 'critical',
                        'cwe': 'CWE-78',
                        'confidence': 0.8
                    },
                    {
                        'pattern': r'subprocess\.(call|run|Popen).*shell=True',
                        'description': 'Subprocess execution with shell=True is dangerous',
                        'severity': 'high',
                        'cwe': 'CWE-78',
                        'confidence': 0.7
                    }
                ],
                'xss_vulnerabilities': [
                    {
                        'pattern': r'innerHTML\s*=\s*.*\+',
                        'description': 'Potential XSS via innerHTML with concatenation',
                        'severity': 'medium',
                        'cwe': 'CWE-79',
                        'confidence': 0.6
                    },
                    {
                        'pattern': r'document\.write\s*\(\s*.*\+',
                        'description': 'Potential XSS via document.write with user input',
                        'severity': 'medium',
                        'cwe': 'CWE-79',
                        'confidence': 0.7
                    }
                ]
            },
            'cryptographic_issues': {
                'weak_encryption': [
                    {
                        'pattern': r'(MD5|SHA1)\s*\(',
                        'description': 'Weak cryptographic hash function detected',
                        'severity': 'medium',
                        'cwe': 'CWE-327',
                        'confidence': 0.9
                    },
                    {
                        'pattern': r'DES|3DES|RC4',
                        'description': 'Weak encryption algorithm detected',
                        'severity': 'high',
                        'cwe': 'CWE-327',
                        'confidence': 0.9
                    }
                ],
                'insecure_random': [
                    {
                        'pattern': r'Math\.random\(\)',
                        'description': 'Math.random() is not cryptographically secure',
                        'severity': 'low',
                        'cwe': 'CWE-338',
                        'confidence': 0.8
                    },
                    {
                        'pattern': r'random\.random\(\)',
                        'description': 'Python random module is not cryptographically secure',
                        'severity': 'low',
                        'cwe': 'CWE-338',
                        'confidence': 0.8
                    }
                ]
            },
            'data_exposure': {
                'hardcoded_secrets': [
                    {
                        'pattern': r'(password|pwd|pass)\s*=\s*["\'][^"\']{6,}["\']',
                        'description': 'Potential hardcoded password detected',
                        'severity': 'critical',
                        'cwe': 'CWE-798',
                        'confidence': 0.7
                    },
                    {
                        'pattern': r'(api[_-]?key|apikey|secret[_-]?key)\s*=\s*["\'][^"\']{10,}["\']',
                        'description': 'Potential hardcoded API key or secret detected',
                        'severity': 'critical',
                        'cwe': 'CWE-798',
                        'confidence': 0.8
                    },
                    {
                        'pattern': r'(token|jwt|bearer)\s*=\s*["\'][^"\']{20,}["\']',
                        'description': 'Potential hardcoded authentication token detected',
                        'severity': 'high',
                        'cwe': 'CWE-798',
                        'confidence': 0.7
                    }
                ],
                'sensitive_data_logging': [
                    {
                        'pattern': r'(console\.log|print|logger\.debug).*password',
                        'description': 'Potential logging of sensitive data',
                        'severity': 'medium',
                        'cwe': 'CWE-532',
                        'confidence': 0.6
                    }
                ]
            },
            'authentication_authorization': {
                'weak_session_management': [
                    {
                        'pattern': r'session\[.*\]\s*=\s*true',
                        'description': 'Simple session management without proper validation',
                        'severity': 'medium',
                        'cwe': 'CWE-287',
                        'confidence': 0.5
                    }
                ],
                'missing_access_control': [
                    {
                        'pattern': r'@app\.route.*methods=.*POST.*\ndef\s+\w+\([^)]*\):(?!.*@)',
                        'description': 'POST endpoint without authentication decorator',
                        'severity': 'medium',
                        'cwe': 'CWE-284',
                        'confidence': 0.4
                    }
                ]
            },
            'input_validation': {
                'missing_input_validation': [
                    {
                        'pattern': r'request\.(args|form|json)\[.*\](?!.*validate)',
                        'description': 'User input used without validation',
                        'severity': 'medium',
                        'cwe': 'CWE-20',
                        'confidence': 0.5
                    }
                ],
                'path_traversal': [
                    {
                        'pattern': r'open\s*\(\s*.*\+.*request',
                        'description': 'Potential path traversal vulnerability',
                        'severity': 'high',
                        'cwe': 'CWE-22',
                        'confidence': 0.7
                    }
                ]
            }
        }
    
    def _load_vulnerability_database(self) -> Dict[str, Any]:
        """Load known vulnerability database"""
        return {
            'known_vulnerable_packages': {
                'npm': {
                    'lodash': {
                        'vulnerable_versions': ['< 4.17.21'],
                        'cve_ids': ['CVE-2020-8203', 'CVE-2021-23337'],
                        'severity': 'high',
                        'description': 'Prototype pollution vulnerabilities'
                    },
                    'axios': {
                        'vulnerable_versions': ['< 0.21.1'],
                        'cve_ids': ['CVE-2020-28168'],
                        'severity': 'medium',
                        'description': 'SSRF vulnerability'
                    },
                    'minimist': {
                        'vulnerable_versions': ['< 1.2.6'],
                        'cve_ids': ['CVE-2021-44906'],
                        'severity': 'critical',
                        'description': 'Prototype pollution'
                    }
                },
                'pip': {
                    'pillow': {
                        'vulnerable_versions': ['< 8.3.2'],
                        'cve_ids': ['CVE-2021-34552'],
                        'severity': 'high',
                        'description': 'Buffer overflow vulnerability'
                    },
                    'requests': {
                        'vulnerable_versions': ['< 2.20.0'],
                        'cve_ids': ['CVE-2018-18074'],
                        'severity': 'medium',
                        'description': 'Request smuggling vulnerability'
                    }
                }
            },
            'security_advisories': {
                'react': {
                    'advisories': [
                        {
                            'id': 'GHSA-react-xss',
                            'title': 'XSS vulnerability in React SSR',
                            'affected_versions': ['< 16.13.1', '17.0.0 - 17.0.1'],
                            'severity': 'medium',
                            'published': '2021-03-15'
                        }
                    ]
                },
                'typescript': {
                    'advisories': [
                        {
                            'id': 'GHSA-ts-path-traversal',
                            'title': 'Path traversal in TypeScript compiler',
                            'affected_versions': ['< 4.2.4'],
                            'severity': 'low',
                            'published': '2021-04-20'
                        }
                    ]
                }
            }
        }
    
    def _load_security_policies(self) -> Dict[str, Any]:
        """Load security policies and compliance requirements"""
        return {
            'minimum_security_score': 80,
            'critical_findings_allowed': 0,
            'high_findings_threshold': 3,
            'compliance_requirements': {
                'owasp_top_10': True,
                'cwe_coverage': True,
                'secure_coding_standards': True
            },
            'encryption_requirements': {
                'minimum_key_length': 256,
                'approved_algorithms': ['AES', 'RSA', 'ECDSA'],
                'prohibited_algorithms': ['DES', '3DES', 'RC4', 'MD5', 'SHA1']
            },
            'authentication_requirements': {
                'multi_factor_authentication': True,
                'password_complexity': True,
                'session_timeout': 3600  # seconds
            }
        }
    
    def assess_pr_security(self, pr_request, context_analysis) -> SecurityAssessmentResult:
        """
        Perform comprehensive security assessment of PR changes
        
        Args:
            pr_request: PRValidationRequest object
            context_analysis: PRContextAnalysis from context analyzer
            
        Returns:
            SecurityAssessmentResult: Complete security assessment
        """
        start_time = datetime.now()
        self.logger.info(f"Starting security assessment for PR #{pr_request.pr_id}")
        
        findings = []
        
        # Phase 1: Static Security Analysis
        static_findings = self._perform_static_security_analysis(context_analysis)
        findings.extend(static_findings)
        
        # Phase 2: Dependency Security Analysis
        dependency_analysis = self._analyze_dependency_security(context_analysis)
        findings.extend(dependency_analysis['findings'])
        
        # Phase 3: Vulnerability Database Check
        vulnerability_analysis = self._check_vulnerability_database(context_analysis)
        findings.extend(vulnerability_analysis['findings'])
        
        # Phase 4: Security Pattern Analysis
        pattern_findings = self._analyze_security_patterns(context_analysis)
        findings.extend(pattern_findings)
        
        # Phase 5: Compliance Assessment
        compliance_status = self._assess_compliance(findings, context_analysis)
        
        # Calculate security metrics
        security_metrics = self._calculate_security_metrics(findings)
        
        # Identify critical issues
        critical_issues = self._identify_critical_security_issues(findings)
        
        # Generate recommendations
        recommendations = self._generate_security_recommendations(findings, context_analysis)
        
        # Calculate overall security score
        security_score = self._calculate_security_score(findings, context_analysis)
        risk_level = self._determine_risk_level(security_score, findings)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        result = SecurityAssessmentResult(
            pr_id=pr_request.pr_id,
            security_score=security_score,
            risk_level=risk_level,
            findings=findings,
            critical_issues=critical_issues,
            recommendations=recommendations,
            security_metrics=security_metrics,
            vulnerability_analysis=vulnerability_analysis,
            dependency_security=dependency_analysis,
            compliance_status=compliance_status,
            processing_time=processing_time
        )
        
        self.logger.info(
            f"Security assessment completed for PR #{pr_request.pr_id}: "
            f"Score: {security_score:.1f}, Risk: {risk_level}, "
            f"Findings: {len(findings)}, Critical: {len(critical_issues)}"
        )
        
        return result
    
    def _perform_static_security_analysis(self, context_analysis) -> List[SecurityFinding]:
        """Perform static security analysis on code changes"""
        findings = []
        
        for file_analysis in context_analysis.file_analyses:
            file_content = self._get_file_content(file_analysis.filename, context_analysis)
            
            # Analyze each security pattern category
            for category, subcategories in self.security_patterns.items():
                for subcategory, patterns in subcategories.items():
                    for pattern_info in patterns:
                        matches = re.finditer(
                            pattern_info['pattern'], 
                            file_content, 
                            re.IGNORECASE | re.MULTILINE | re.DOTALL
                        )
                        
                        for match in matches:
                            line_number = file_content[:match.start()].count('\n') + 1
                            
                            finding = SecurityFinding(
                                finding_id=self._generate_finding_id(file_analysis.filename, line_number, subcategory),
                                finding_type=subcategory,
                                severity=pattern_info['severity'],
                                category=category,
                                file_path=file_analysis.filename,
                                line_number=line_number,
                                description=pattern_info['description'],
                                recommendation=self._get_recommendation_for_pattern(subcategory),
                                cwe_id=pattern_info.get('cwe'),
                                cvss_score=self._calculate_cvss_score(pattern_info['severity']),
                                confidence=pattern_info['confidence'],
                                evidence={
                                    'matched_text': match.group(0),
                                    'pattern': pattern_info['pattern'],
                                    'context_before': file_content[max(0, match.start()-100):match.start()],
                                    'context_after': file_content[match.end():min(len(file_content), match.end()+100)]
                                },
                                remediation_effort=self._estimate_remediation_effort(pattern_info['severity'])
                            )
                            findings.append(finding)
        
        return findings
    
    def _analyze_dependency_security(self, context_analysis) -> Dict[str, Any]:
        """Analyze security of dependencies"""
        findings = []
        dependency_summary = {
            'total_dependencies': 0,
            'vulnerable_dependencies': 0,
            'critical_vulnerabilities': 0,
            'packages_analyzed': []
        }
        
        for file_analysis in context_analysis.file_analyses:
            for dep_ref in file_analysis.dependency_references:
                dependency_summary['total_dependencies'] += 1
                
                # Parse dependency reference
                dep_info = self._parse_dependency_reference(dep_ref)
                if not dep_info:
                    continue
                
                dependency_summary['packages_analyzed'].append(dep_info)
                
                # Check against vulnerability database
                vulnerabilities = self._check_dependency_vulnerabilities(dep_info)
                
                for vuln in vulnerabilities:
                    if vuln['severity'] == 'critical':
                        dependency_summary['critical_vulnerabilities'] += 1
                    
                    if vuln['severity'] in ['critical', 'high']:
                        dependency_summary['vulnerable_dependencies'] += 1
                    
                    finding = SecurityFinding(
                        finding_id=self._generate_finding_id(file_analysis.filename, None, 'dependency_vulnerability'),
                        finding_type='dependency_vulnerability',
                        severity=vuln['severity'],
                        category='dependency_security',
                        file_path=file_analysis.filename,
                        line_number=None,
                        description=f"Vulnerable dependency: {dep_info['name']}@{dep_info['version']} - {vuln['description']}",
                        recommendation=f"Upgrade to version {vuln.get('fixed_version', 'latest')} or higher",
                        cwe_id=vuln.get('cwe_id'),
                        cvss_score=vuln.get('cvss_score'),
                        confidence=0.9,
                        evidence={
                            'dependency': dep_info,
                            'vulnerability': vuln,
                            'cve_ids': vuln.get('cve_ids', [])
                        },
                        remediation_effort='medium'
                    )
                    findings.append(finding)
        
        return {
            'findings': findings,
            'summary': dependency_summary
        }
    
    def _check_vulnerability_database(self, context_analysis) -> Dict[str, Any]:
        """Check detected technologies against vulnerability database"""
        findings = []
        analysis_summary = {
            'technologies_checked': 0,
            'advisories_found': 0,
            'affected_technologies': []
        }
        
        for tech_detection in context_analysis.detected_technologies:
            analysis_summary['technologies_checked'] += 1
            tech_name = tech_detection.name.lower()
            
            # Check security advisories
            if tech_name in self.vulnerability_database.get('security_advisories', {}):
                advisories = self.vulnerability_database['security_advisories'][tech_name]['advisories']
                
                for advisory in advisories:
                    analysis_summary['advisories_found'] += 1
                    
                    # Check if detected version is affected
                    if self._is_version_affected(tech_detection.version_detected, advisory['affected_versions']):
                        analysis_summary['affected_technologies'].append({
                            'technology': tech_name,
                            'version': tech_detection.version_detected,
                            'advisory': advisory['id']
                        })
                        
                        finding = SecurityFinding(
                            finding_id=self._generate_finding_id('', None, 'security_advisory'),
                            finding_type='security_advisory',
                            severity=advisory['severity'],
                            category='vulnerability_management',
                            file_path=tech_detection.file_references[0] if tech_detection.file_references else 'unknown',
                            line_number=None,
                            description=f"Security advisory for {tech_detection.name}: {advisory['title']}",
                            recommendation=f"Review advisory {advisory['id']} and update if necessary",
                            cwe_id=None,
                            cvss_score=self._calculate_cvss_score(advisory['severity']),
                            confidence=0.8,
                            evidence={
                                'advisory': advisory,
                                'technology': tech_detection.name,
                                'detected_version': tech_detection.version_detected
                            },
                            remediation_effort='medium'
                        )
                        findings.append(finding)
        
        return {
            'findings': findings,
            'summary': analysis_summary
        }
    
    def _analyze_security_patterns(self, context_analysis) -> List[SecurityFinding]:
        """Analyze security-specific patterns beyond basic static analysis"""
        findings = []
        
        # Additional security pattern analysis
        security_checks = {
            'insecure_configurations': {
                'patterns': [
                    {
                        'pattern': r'debug\s*=\s*True',
                        'description': 'Debug mode enabled in production code',
                        'severity': 'medium',
                        'category': 'configuration_security'
                    },
                    {
                        'pattern': r'CORS.*origin.*\*',
                        'description': 'CORS configured to allow all origins',
                        'severity': 'medium',
                        'category': 'configuration_security'
                    }
                ]
            },
            'data_protection': {
                'patterns': [
                    {
                        'pattern': r'(credit[_-]?card|ssn|social[_-]?security)',
                        'description': 'Potential handling of sensitive personal data',
                        'severity': 'low',
                        'category': 'data_protection'
                    }
                ]
            }
        }
        
        for file_analysis in context_analysis.file_analyses:
            file_content = self._get_file_content(file_analysis.filename, context_analysis)
            
            for check_category, check_data in security_checks.items():
                for pattern_info in check_data['patterns']:
                    matches = re.finditer(pattern_info['pattern'], file_content, re.IGNORECASE)
                    
                    for match in matches:
                        line_number = file_content[:match.start()].count('\n') + 1
                        
                        finding = SecurityFinding(
                            finding_id=self._generate_finding_id(file_analysis.filename, line_number, check_category),
                            finding_type=check_category,
                            severity=pattern_info['severity'],
                            category=pattern_info['category'],
                            file_path=file_analysis.filename,
                            line_number=line_number,
                            description=pattern_info['description'],
                            recommendation=self._get_recommendation_for_pattern(check_category),
                            cwe_id=None,
                            cvss_score=self._calculate_cvss_score(pattern_info['severity']),
                            confidence=0.6,
                            evidence={
                                'matched_text': match.group(0),
                                'pattern': pattern_info['pattern']
                            },
                            remediation_effort='low'
                        )
                        findings.append(finding)
        
        return findings
    
    def _assess_compliance(self, findings: List[SecurityFinding], context_analysis) -> Dict[str, Any]:
        """Assess compliance with security standards"""
        compliance_status = {
            'owasp_top_10': {
                'compliant': True,
                'violations': [],
                'coverage': 0.0
            },
            'cwe_coverage': {
                'total_cwe_categories': 0,
                'covered_categories': 0,
                'coverage_percentage': 0.0
            },
            'security_policies': {
                'compliant': True,
                'violations': []
            }
        }
        
        # Check OWASP Top 10 compliance
        owasp_violations = self._check_owasp_compliance(findings)
        compliance_status['owasp_top_10']['violations'] = owasp_violations
        compliance_status['owasp_top_10']['compliant'] = len(owasp_violations) == 0
        
        # Check CWE coverage
        cwe_ids = [f.cwe_id for f in findings if f.cwe_id]
        unique_cwe_ids = set(cwe_ids)
        compliance_status['cwe_coverage']['total_cwe_categories'] = len(unique_cwe_ids)
        compliance_status['cwe_coverage']['covered_categories'] = len(unique_cwe_ids)
        
        # Check security policy compliance
        policy_violations = self._check_policy_compliance(findings)
        compliance_status['security_policies']['violations'] = policy_violations
        compliance_status['security_policies']['compliant'] = len(policy_violations) == 0
        
        return compliance_status
    
    def _calculate_security_metrics(self, findings: List[SecurityFinding]) -> SecurityMetrics:
        """Calculate comprehensive security metrics"""
        findings_by_severity = {
            'critical': len([f for f in findings if f.severity == 'critical']),
            'high': len([f for f in findings if f.severity == 'high']),
            'medium': len([f for f in findings if f.severity == 'medium']),
            'low': len([f for f in findings if f.severity == 'low']),
            'info': len([f for f in findings if f.severity == 'info'])
        }
        
        # Calculate security score
        security_score = self._calculate_security_score(findings, None)
        risk_level = self._determine_risk_level(security_score, findings)
        
        # Calculate coverage (placeholder - would be more sophisticated)
        coverage_percentage = 85.0  # Placeholder value
        
        return SecurityMetrics(
            total_findings=len(findings),
            findings_by_severity=findings_by_severity,
            security_score=security_score,
            risk_level=risk_level,
            coverage_percentage=coverage_percentage,
            scan_timestamp=datetime.now().isoformat()
        )
    
    def _identify_critical_security_issues(self, findings: List[SecurityFinding]) -> List[Dict[str, Any]]:
        """Identify critical security issues requiring immediate attention"""
        critical_issues = []
        
        for finding in findings:
            if finding.severity == 'critical':
                critical_issues.append({
                    'type': 'critical_security_finding',
                    'severity': 'critical',
                    'message': finding.description,
                    'file': finding.file_path,
                    'line': finding.line_number,
                    'recommendation': finding.recommendation,
                    'cwe_id': finding.cwe_id,
                    'cvss_score': finding.cvss_score,
                    'finding_id': finding.finding_id
                })
            elif finding.severity == 'high' and finding.confidence > 0.8:
                critical_issues.append({
                    'type': 'high_confidence_security_issue',
                    'severity': 'high',
                    'message': finding.description,
                    'file': finding.file_path,
                    'line': finding.line_number,
                    'recommendation': finding.recommendation,
                    'confidence': finding.confidence,
                    'finding_id': finding.finding_id
                })
        
        return critical_issues
    
    def _generate_security_recommendations(self, findings: List[SecurityFinding], context_analysis) -> List[Dict[str, Any]]:
        """Generate actionable security recommendations"""
        recommendations = []
        
        # Group findings by category for targeted recommendations
        findings_by_category = {}
        for finding in findings:
            if finding.category not in findings_by_category:
                findings_by_category[finding.category] = []
            findings_by_category[finding.category].append(finding)
        
        # Generate category-specific recommendations
        for category, category_findings in findings_by_category.items():
            if category == 'injection_vulnerabilities':
                recommendations.append({
                    'type': 'security_improvement',
                    'priority': 'high',
                    'category': 'injection_prevention',
                    'message': f'Implement input validation and parameterized queries to prevent injection attacks ({len(category_findings)} issues found)',
                    'action': 'review_and_fix_injection_vulnerabilities',
                    'affected_files': list(set(f.file_path for f in category_findings))
                })
            
            elif category == 'data_exposure':
                recommendations.append({
                    'type': 'security_improvement',
                    'priority': 'critical',
                    'category': 'data_protection',
                    'message': f'Remove hardcoded secrets and implement secure credential management ({len(category_findings)} issues found)',
                    'action': 'implement_secure_credential_management',
                    'affected_files': list(set(f.file_path for f in category_findings))
                })
            
            elif category == 'cryptographic_issues':
                recommendations.append({
                    'type': 'security_improvement',
                    'priority': 'medium',
                    'category': 'cryptography',
                    'message': f'Upgrade to secure cryptographic algorithms and practices ({len(category_findings)} issues found)',
                    'action': 'upgrade_cryptographic_implementations',
                    'affected_files': list(set(f.file_path for f in category_findings))
                })
        
        # Add general recommendations
        if len(findings) > 10:
            recommendations.append({
                'type': 'security_process',
                'priority': 'medium',
                'category': 'security_review',
                'message': f'Consider implementing automated security scanning in CI/CD pipeline ({len(findings)} total findings)',
                'action': 'implement_automated_security_scanning'
            })
        
        # Add dependency-specific recommendations
        dep_findings = [f for f in findings if f.finding_type == 'dependency_vulnerability']
        if dep_findings:
            recommendations.append({
                'type': 'dependency_security',
                'priority': 'high',
                'category': 'dependency_management',
                'message': f'Update vulnerable dependencies and implement dependency scanning ({len(dep_findings)} vulnerable dependencies)',
                'action': 'update_vulnerable_dependencies',
                'affected_dependencies': [f.evidence.get('dependency', {}).get('name') for f in dep_findings]
            })
        
        return recommendations
    
    def _calculate_security_score(self, findings: List[SecurityFinding], context_analysis) -> float:
        """Calculate overall security score"""
        base_score = 100.0
        
        # Deduct points based on findings
        for finding in findings:
            if finding.severity == 'critical':
                base_score -= 25 * finding.confidence
            elif finding.severity == 'high':
                base_score -= 15 * finding.confidence
            elif finding.severity == 'medium':
                base_score -= 8 * finding.confidence
            elif finding.severity == 'low':
                base_score -= 3 * finding.confidence
            elif finding.severity == 'info':
                base_score -= 1 * finding.confidence
        
        return max(0.0, min(100.0, base_score))
    
    def _determine_risk_level(self, security_score: float, findings: List[SecurityFinding]) -> str:
        """Determine overall risk level"""
        critical_findings = len([f for f in findings if f.severity == 'critical'])
        high_findings = len([f for f in findings if f.severity == 'high'])
        
        if critical_findings > 0 or security_score < 50:
            return 'critical'
        elif high_findings > 3 or security_score < 70:
            return 'high'
        elif security_score < 85:
            return 'medium'
        else:
            return 'low'
    
    # Helper methods
    
    def _generate_finding_id(self, file_path: str, line_number: Optional[int], finding_type: str) -> str:
        """Generate unique finding ID"""
        data = f"{file_path}:{line_number}:{finding_type}:{datetime.now().isoformat()}"
        return hashlib.md5(data.encode()).hexdigest()[:12]
    
    def _get_recommendation_for_pattern(self, pattern_type: str) -> str:
        """Get recommendation text for a pattern type"""
        recommendations = {
            'sql_injection': 'Use parameterized queries or prepared statements',
            'command_injection': 'Validate and sanitize all user inputs, avoid shell execution',
            'xss_vulnerabilities': 'Use proper output encoding and validation',
            'hardcoded_secrets': 'Move secrets to secure configuration or environment variables',
            'weak_encryption': 'Use strong encryption algorithms (AES-256, RSA-2048+)',
            'insecure_random': 'Use cryptographically secure random number generators',
            'insecure_configurations': 'Review and secure configuration settings',
            'data_protection': 'Implement proper data handling and privacy controls'
        }
        return recommendations.get(pattern_type, 'Review and follow security best practices')
    
    def _calculate_cvss_score(self, severity: str) -> Optional[float]:
        """Calculate CVSS score based on severity"""
        score_mapping = {
            'critical': 9.5,
            'high': 7.5,
            'medium': 5.0,
            'low': 2.5,
            'info': 0.0
        }
        return score_mapping.get(severity)
    
    def _estimate_remediation_effort(self, severity: str) -> str:
        """Estimate remediation effort based on severity"""
        effort_mapping = {
            'critical': 'high',
            'high': 'medium',
            'medium': 'medium',
            'low': 'low',
            'info': 'low'
        }
        return effort_mapping.get(severity, 'medium')
    
    def _get_file_content(self, filename: str, context_analysis) -> str:
        """Get file content for analysis (placeholder implementation)"""
        # In a real implementation, this would get the actual file content
        return f"// Content of {filename}\n// Security analysis placeholder"
    
    def _parse_dependency_reference(self, dep_ref: str) -> Optional[Dict[str, str]]:
        """Parse dependency reference into name and version"""
        if '@' in dep_ref:
            parts = dep_ref.split('@')
            if len(parts) >= 2:
                return {'name': parts[0], 'version': parts[1]}
        elif '==' in dep_ref:
            parts = dep_ref.split('==')
            if len(parts) == 2:
                return {'name': parts[0], 'version': parts[1]}
        return None
    
    def _check_dependency_vulnerabilities(self, dep_info: Dict[str, str]) -> List[Dict[str, Any]]:
        """Check dependency for known vulnerabilities"""
        vulnerabilities = []
        package_name = dep_info['name']
        version = dep_info['version']
        
        # Check NPM vulnerabilities
        npm_vulns = self.vulnerability_database.get('known_vulnerable_packages', {}).get('npm', {})
        if package_name in npm_vulns:
            vuln_info = npm_vulns[package_name]
            if self._is_version_vulnerable(version, vuln_info['vulnerable_versions']):
                vulnerabilities.append({
                    'package': package_name,
                    'version': version,
                    'description': vuln_info['description'],
                    'severity': vuln_info['severity'],
                    'cve_ids': vuln_info['cve_ids'],
                    'fixed_version': 'latest'  # Simplified
                })
        
        # Check Python vulnerabilities
        pip_vulns = self.vulnerability_database.get('known_vulnerable_packages', {}).get('pip', {})
        if package_name in pip_vulns:
            vuln_info = pip_vulns[package_name]
            if self._is_version_vulnerable(version, vuln_info['vulnerable_versions']):
                vulnerabilities.append({
                    'package': package_name,
                    'version': version,
                    'description': vuln_info['description'],
                    'severity': vuln_info['severity'],
                    'cve_ids': vuln_info['cve_ids'],
                    'fixed_version': 'latest'  # Simplified
                })
        
        return vulnerabilities
    
    def _is_version_affected(self, version: Optional[str], affected_versions: List[str]) -> bool:
        """Check if version is in affected versions list"""
        if not version:
            return False
        # Simplified version checking - would need proper semver implementation
        for affected in affected_versions:
            if version in affected:
                return True
        return False
    
    def _is_version_vulnerable(self, version: str, vulnerable_versions: List[str]) -> bool:
        """Check if version is vulnerable"""
        # Simplified vulnerability checking
        for vuln_range in vulnerable_versions:
            if '<' in vuln_range:
                # Simple less-than check
                return True
        return False
    
    def _check_owasp_compliance(self, findings: List[SecurityFinding]) -> List[str]:
        """Check compliance with OWASP Top 10"""
        violations = []
        
        # Map findings to OWASP categories
        owasp_findings = {
            'A01_Broken_Access_Control': [f for f in findings if f.finding_type in ['missing_access_control']],
            'A02_Cryptographic_Failures': [f for f in findings if f.category == 'cryptographic_issues'],
            'A03_Injection': [f for f in findings if f.category == 'injection_vulnerabilities'],
            'A05_Security_Misconfiguration': [f for f in findings if f.finding_type in ['insecure_configurations']],
            'A07_Identity_Authentication_Failures': [f for f in findings if f.finding_type in ['weak_session_management']],
            'A09_Security_Logging_Monitoring_Failures': [f for f in findings if f.finding_type in ['sensitive_data_logging']]
        }
        
        for owasp_cat, cat_findings in owasp_findings.items():
            if cat_findings:
                violations.append(f"{owasp_cat}: {len(cat_findings)} findings")
        
        return violations
    
    def _check_policy_compliance(self, findings: List[SecurityFinding]) -> List[str]:
        """Check compliance with security policies"""
        violations = []
        
        # Check critical findings threshold
        critical_findings = len([f for f in findings if f.severity == 'critical'])
        if critical_findings > self.security_policies['critical_findings_allowed']:
            violations.append(f"Exceeds critical findings threshold: {critical_findings} > {self.security_policies['critical_findings_allowed']}")
        
        # Check high findings threshold
        high_findings = len([f for f in findings if f.severity == 'high'])
        if high_findings > self.security_policies['high_findings_threshold']:
            violations.append(f"Exceeds high findings threshold: {high_findings} > {self.security_policies['high_findings_threshold']}")
        
        return violations
    
    def validate_configuration(self) -> Dict[str, Any]:
        """Validate assessor configuration"""
        return {
            'status': 'healthy',
            'security_patterns_loaded': len(self.security_patterns),
            'vulnerability_database_loaded': len(self.vulnerability_database),
            'security_policies_loaded': len(self.security_policies),
            'knowledge_vault_available': self.knowledge_vault is not None
        }