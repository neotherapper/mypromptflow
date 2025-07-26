#!/usr/bin/env python3
"""
Test Role-Aware Knowledge Management System
Validates the implementation of role-specific context loading and agent self-discovery patterns.
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Optional, Set

class RoleAwareSystemTester:
    """Test harness for role-aware knowledge management system."""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.knowledge_vault_path = self.base_path / "knowledge-vault" / "knowledge" / "technologies"
        self.test_results = {
            "technology_coverage": {},
            "role_coverage": {},
            "context_loading": {},
            "agent_discovery": {},
            "system_integration": {}
        }
    
    def test_technology_coverage(self) -> Dict[str, bool]:
        """Test that all required technologies have role-specific contexts."""
        print("🔍 Testing Technology Coverage...")
        
        required_technologies = ["react", "typescript", "testing"]
        required_roles = ["architect", "frontend-dev", "performance"]
        
        coverage_results = {}
        
        for tech in required_technologies:
            tech_path = self.knowledge_vault_path / tech
            if not tech_path.exists():
                coverage_results[f"{tech}_directory"] = False
                print(f"❌ Missing technology directory: {tech}")
                continue
            
            coverage_results[f"{tech}_directory"] = True
            print(f"✅ Technology directory exists: {tech}")
            
            # Check role-specific files
            for role in required_roles:
                file_path = tech_path / f"{tech}-{role}.md"
                if file_path.exists():
                    coverage_results[f"{tech}_{role}"] = True
                    print(f"✅ Context file exists: {tech}-{role}.md")
                    
                    # Validate file content
                    with open(file_path, 'r') as f:
                        content = f.read()
                        if len(content) > 500:  # Minimum viable content
                            coverage_results[f"{tech}_{role}_content"] = True
                            print(f"✅ Context file has substantial content: {tech}-{role}.md")
                        else:
                            coverage_results[f"{tech}_{role}_content"] = False
                            print(f"❌ Context file has insufficient content: {tech}-{role}.md")
                else:
                    coverage_results[f"{tech}_{role}"] = False
                    print(f"❌ Missing context file: {tech}-{role}.md")
        
        # Check for additional specialized roles
        specialized_roles = ["accessibility", "security", "testing"]
        for tech in required_technologies:
            tech_path = self.knowledge_vault_path / tech
            if tech_path.exists():
                for role in specialized_roles:
                    file_path = tech_path / f"{tech}-{role}.md"
                    if file_path.exists():
                        coverage_results[f"{tech}_{role}_specialized"] = True
                        print(f"✅ Specialized context exists: {tech}-{role}.md")
        
        self.test_results["technology_coverage"] = coverage_results
        return coverage_results
    
    def test_role_coverage(self) -> Dict[str, bool]:
        """Test that all agent roles have appropriate context access."""
        print("\n👥 Testing Role Coverage...")
        
        role_definitions = {
            "architect": ["High-level design", "Architecture patterns", "System design"],
            "frontend-dev": ["Implementation patterns", "Component development", "User interface"],
            "performance": ["Optimization", "Profiling", "Bundle analysis"],
            "security": ["Vulnerability assessment", "Security testing", "Compliance"]
        }
        
        role_results = {}
        
        for role, expected_content in role_definitions.items():
            print(f"\n🔍 Testing {role} role contexts...")
            role_contexts = []
            
            # Find all contexts for this role across technologies
            for tech_dir in self.knowledge_vault_path.iterdir():
                if tech_dir.is_dir():
                    for context_file in tech_dir.glob(f"*-{role}.md"):
                        role_contexts.append(context_file)
                        print(f"✅ Found {role} context: {context_file.name}")
            
            if len(role_contexts) >= 2:  # Should have contexts for multiple technologies
                role_results[f"{role}_coverage"] = True
                print(f"✅ {role} role has adequate context coverage ({len(role_contexts)} contexts)")
                
                # Validate content themes
                content_validation = self.validate_role_content(role_contexts, expected_content)
                role_results[f"{role}_content_themes"] = content_validation
                
            else:
                role_results[f"{role}_coverage"] = False
                print(f"❌ {role} role has insufficient context coverage ({len(role_contexts)} contexts)")
        
        self.test_results["role_coverage"] = role_results
        return role_results
    
    def validate_role_content(self, context_files: List[Path], expected_themes: List[str]) -> bool:
        """Validate that role contexts contain expected thematic content."""
        combined_content = ""
        
        for file_path in context_files:
            try:
                with open(file_path, 'r') as f:
                    combined_content += f.read().lower()
            except Exception as e:
                print(f"⚠️  Error reading {file_path}: {e}")
                return False
        
        theme_matches = 0
        for theme in expected_themes:
            theme_keywords = theme.lower().split()
            if any(keyword in combined_content for keyword in theme_keywords):
                theme_matches += 1
                print(f"✅ Found theme content: {theme}")
            else:
                print(f"❌ Missing theme content: {theme}")
        
        return theme_matches >= len(expected_themes) * 0.7  # 70% theme coverage required
    
    def test_context_loading_patterns(self) -> Dict[str, bool]:
        """Test REQUEST_CONTEXT() patterns and agent self-discovery."""
        print("\n🔄 Testing Context Loading Patterns...")
        
        test_scenarios = [
            {
                "name": "Single Role Loading",
                "pattern": "REQUEST_CONTEXT(react-frontend-dev)",
                "expected_files": ["react/react-frontend-dev.md"]
            },
            {
                "name": "Multi-Role Loading", 
                "pattern": "REQUEST_CONTEXT(react-architect, typescript-architect)",
                "expected_files": ["react/react-architect.md", "typescript/typescript-architect.md"]
            },
            {
                "name": "Performance Specialist Loading",
                "pattern": "REQUEST_CONTEXT(react-performance, typescript-performance, testing-performance)",
                "expected_files": ["react/react-performance.md", "typescript/typescript-performance.md", "testing/testing-performance.md"]
            },
            {
                "name": "Security Analysis Loading",
                "pattern": "REQUEST_CONTEXT(testing-security)",
                "expected_files": ["testing/testing-security.md"]
            }
        ]
        
        loading_results = {}
        
        for scenario in test_scenarios:
            print(f"\n🧪 Testing scenario: {scenario['name']}")
            print(f"   Pattern: {scenario['pattern']}")
            
            scenario_success = True
            for expected_file in scenario['expected_files']:
                file_path = self.knowledge_vault_path / expected_file
                if file_path.exists():
                    print(f"✅ Context available: {expected_file}")
                else:
                    print(f"❌ Context missing: {expected_file}")
                    scenario_success = False
            
            loading_results[scenario['name']] = scenario_success
        
        self.test_results["context_loading"] = loading_results
        return loading_results
    
    def test_agent_discovery_integration(self) -> Dict[str, bool]:
        """Test integration with agent self-discovery instructions."""
        print("\n🤖 Testing Agent Discovery Integration...")
        
        discovery_instructions_path = self.base_path / "meta" / "docs" / "agent-self-discovery-instructions.md"
        integration_results = {}
        
        if discovery_instructions_path.exists():
            integration_results["instructions_exist"] = True
            print("✅ Agent self-discovery instructions exist")
            
            with open(discovery_instructions_path, 'r') as f:
                content = f.read()
                
                # Check for key integration elements
                key_elements = [
                    "REQUEST_CONTEXT()",
                    "role-aware knowledge management",
                    "Claude Code Max",
                    "react-architect",
                    "typescript-frontend-dev", 
                    "testing-security",
                    "knowledge-vault/knowledge/technologies"
                ]
                
                for element in key_elements:
                    if element in content:
                        integration_results[f"contains_{element.replace('()', '').replace('/', '_')}"] = True
                        print(f"✅ Instructions contain: {element}")
                    else:
                        integration_results[f"contains_{element.replace('()', '').replace('/', '_')}"] = False
                        print(f"❌ Instructions missing: {element}")
        else:
            integration_results["instructions_exist"] = False
            print("❌ Agent self-discovery instructions missing")
        
        self.test_results["agent_discovery"] = integration_results
        return integration_results
    
    def test_system_integration(self) -> Dict[str, bool]:
        """Test integration with PR validation system and other components."""
        print("\n🔗 Testing System Integration...")
        
        integration_results = {}
        
        # Test PR validation system integration
        pr_validation_path = self.base_path / "projects" / "ai-pr-validation-system" / "CLAUDE.md"
        if pr_validation_path.exists():
            integration_results["pr_validation_exists"] = True
            print("✅ PR validation system exists")
            
            with open(pr_validation_path, 'r') as f:
                content = f.read()
                
                integration_checks = [
                    "role-aware",
                    "REQUEST_CONTEXT",
                    "knowledge-vault/knowledge/technologies",
                    "Claude Code Max",
                    "comprehensive context loading"
                ]
                
                for check in integration_checks:
                    if check in content:
                        integration_results[f"pr_validation_{check.replace(' ', '_').replace('/', '_')}"] = True
                        print(f"✅ PR validation includes: {check}")
                    else:
                        integration_results[f"pr_validation_{check.replace(' ', '_').replace('/', '_')}"] = False
                        print(f"❌ PR validation missing: {check}")
        else:
            integration_results["pr_validation_exists"] = False
            print("❌ PR validation system not found")
        
        # Test AI Knowledge Lifecycle Orchestrator integration
        orchestrator_path = self.base_path / "projects" / "ai-knowledge-lifecycle-orchestrator" / "CLAUDE.md"
        if orchestrator_path.exists():
            integration_results["orchestrator_exists"] = True
            print("✅ Knowledge lifecycle orchestrator exists")
            
            with open(orchestrator_path, 'r') as f:
                content = f.read()
                
                if "role-aware knowledge management" in content:
                    integration_results["orchestrator_role_aware"] = True
                    print("✅ Orchestrator includes role-aware management")
                else:
                    integration_results["orchestrator_role_aware"] = False
                    print("❌ Orchestrator missing role-aware management")
        else:
            integration_results["orchestrator_exists"] = False
            print("❌ Knowledge lifecycle orchestrator not found")
        
        self.test_results["system_integration"] = integration_results
        return integration_results
    
    def generate_test_report(self) -> Dict[str, any]:
        """Generate comprehensive test report."""
        print("\n📊 Generating Test Report...")
        
        # Calculate success rates for each test category
        report = {
            "test_summary": {},
            "detailed_results": self.test_results,
            "recommendations": []
        }
        
        for category, results in self.test_results.items():
            if results:
                total_tests = len(results)
                passed_tests = sum(1 for result in results.values() if result is True)
                success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
                
                report["test_summary"][category] = {
                    "total_tests": total_tests,
                    "passed_tests": passed_tests,
                    "success_rate": f"{success_rate:.1f}%"
                }
                
                print(f"📈 {category}: {passed_tests}/{total_tests} tests passed ({success_rate:.1f}%)")
            else:
                report["test_summary"][category] = {
                    "total_tests": 0,
                    "passed_tests": 0,
                    "success_rate": "0.0%"
                }
                print(f"📈 {category}: No tests executed")
        
        # Generate recommendations
        recommendations = []
        
        # Technology coverage recommendations
        tech_results = self.test_results.get("technology_coverage", {})
        missing_contexts = [key for key, value in tech_results.items() if not value and "content" not in key]
        if missing_contexts:
            recommendations.append(f"Create missing context files: {', '.join(missing_contexts)}")
        
        # Role coverage recommendations
        role_results = self.test_results.get("role_coverage", {})
        insufficient_roles = [key.replace("_coverage", "") for key, value in role_results.items() if not value and key.endswith("_coverage")]
        if insufficient_roles:
            recommendations.append(f"Expand context coverage for roles: {', '.join(insufficient_roles)}")
        
        # Integration recommendations
        integration_results = self.test_results.get("system_integration", {})
        missing_integrations = [key for key, value in integration_results.items() if not value]
        if missing_integrations:
            recommendations.append(f"Improve system integrations: {', '.join(missing_integrations)}")
        
        report["recommendations"] = recommendations
        
        if recommendations:
            print("\n💡 Recommendations:")
            for i, rec in enumerate(recommendations, 1):
                print(f"   {i}. {rec}")
        else:
            print("\n🎉 All tests passed! No recommendations needed.")
        
        return report
    
    def run_all_tests(self) -> Dict[str, any]:
        """Run all test suites and generate comprehensive report."""
        print("🚀 Starting Role-Aware Knowledge Management System Tests")
        print("=" * 70)
        
        # Run all test suites
        self.test_technology_coverage()
        self.test_role_coverage()
        self.test_context_loading_patterns()
        self.test_agent_discovery_integration()
        self.test_system_integration()
        
        # Generate and return comprehensive report
        report = self.generate_test_report()
        
        print("\n" + "=" * 70)
        print("🏁 Role-Aware Knowledge Management System Tests Complete")
        
        return report

def main():
    """Main test execution function."""
    # Use current working directory as base path
    base_path = "/Users/georgiospilitsoglou/Developer/projects/mypromptflow"
    
    # Initialize and run tester
    tester = RoleAwareSystemTester(base_path)
    report = tester.run_all_tests()
    
    # Save detailed report
    import json
    report_path = Path(base_path) / "role_aware_system_test_report.json"
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📋 Detailed test report saved to: {report_path}")
    
    # Calculate overall success rate
    total_tests = sum(data["total_tests"] for data in report["test_summary"].values())
    total_passed = sum(data["passed_tests"] for data in report["test_summary"].values())
    overall_success = (total_passed / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"\n🎯 Overall System Success Rate: {total_passed}/{total_tests} ({overall_success:.1f}%)")
    
    if overall_success >= 90:
        print("🟢 EXCELLENT: System ready for production use")
    elif overall_success >= 75:
        print("🟡 GOOD: System functional with minor improvements needed")
    elif overall_success >= 50:
        print("🟠 FAIR: System needs significant improvements")
    else:
        print("🔴 POOR: System requires major fixes before use")
    
    return report

if __name__ == "__main__":
    main()