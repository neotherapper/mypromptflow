#!/usr/bin/env python3
"""
Schema Validation Script
AI INSTRUCTIONS: This script validates YAML files against defined schemas with comprehensive error reporting

Purpose: Ensure data integrity before migration to Notion
Target: 100% schema compliance for production-ready migration
"""

import os
import sys
import yaml
import json
import jsonschema
import argparse
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
from datetime import datetime, timezone
import logging

# Schema validation configurations
SCHEMA_DEFINITIONS = {
    "tools_services": {
        "type": "object",
        "required": ["tool_name", "category", "description"],
        "properties": {
            "tool_name": {"type": "string", "minLength": 1, "maxLength": 200},
            "category": {"type": "string", "enum": [
                "AI Development", "Cloud Services", "Development Tools", "Databases",
                "Monitoring", "Communication", "Content Processing", "File Systems",
                "Search & Discovery", "Version Control", "Authentication", "Analytics", "Infrastructure"
            ]},
            "subcategory": {"type": "string", "maxLength": 100},
            "description": {"type": "string", "minLength": 10, "maxLength": 2000},
            "website": {"type": "string", "format": "uri"},
            "documentation": {"type": "string", "format": "uri"},
            "pricing": {
                "type": "object",
                "properties": {
                    "model": {"type": "string", "enum": ["Free", "Freemium", "Subscription", "One-time Purchase", "Enterprise", "Open Source"]},
                    "details": {"type": "string", "maxLength": 500}
                }
            },
            "use_cases": {"type": "array", "items": {"type": "string"}},
            "complexity": {"type": "string", "enum": ["Simple", "Moderate", "Complex", "Expert"]},
            "status": {"type": "string", "enum": ["Not Evaluated", "Under Evaluation", "Approved", "In Use", "Deprecated"]},
            "tags": {"type": "array", "items": {"type": "string"}},
            "metadata": {
                "type": "object", 
                "required": ["created_date", "last_updated"],
                "properties": {
                    "created_date": {"type": "string", "format": "date-time"},
                    "last_updated": {"type": "string", "format": "date-time"},
                    "version": {"type": "string"},
                    "database_type": {"type": "string"},
                    "validation_status": {"type": "string"}
                }
            }
        }
    },
    
    "knowledge_vault": {
        "type": "object",
        "required": ["knowledge_name", "category", "type", "description"],
        "properties": {
            "knowledge_name": {"type": "string", "minLength": 1, "maxLength": 200},
            "category": {"type": "string", "enum": [
                "AI Frameworks", "Development Methodologies", "Research Insights", "Best Practices",
                "Design Patterns", "Business Strategies", "Technical Specifications", "Implementation Guides"
            ]},
            "type": {"type": "string", "enum": [
                "Methodology", "Framework", "Pattern", "Technique", "Research Finding",
                "Best Practice", "Case Study", "Implementation Guide"
            ]},
            "description": {"type": "string", "minLength": 10, "maxLength": 3000},
            "concepts": {"type": "array", "items": {"type": "string"}},
            "maturity": {"type": "string", "enum": ["Concept", "Prototype", "Tested", "Proven", "Industry Standard"]},
            "applicability": {"type": "array", "items": {"type": "string"}},
            "complexity": {"type": "string", "enum": ["Beginner", "Intermediate", "Advanced", "Expert"]},
            "references": {"type": "string", "maxLength": 1000},
            "validation": {
                "type": "object",
                "properties": {
                    "last_date": {"type": "string", "format": "date"},
                    "notes": {"type": "string", "maxLength": 500}
                }
            },
            "metadata": {
                "type": "object",
                "required": ["created_date", "last_updated"],
                "properties": {
                    "created_date": {"type": "string", "format": "date-time"},
                    "last_updated": {"type": "string", "format": "date-time"},
                    "version": {"type": "string"},
                    "database_type": {"type": "string"},
                    "validation_status": {"type": "string"}
                }
            }
        }
    },
    
    "business_ideas": {
        "type": "object",
        "required": ["idea_name", "category", "stage", "description"],
        "properties": {
            "idea_name": {"type": "string", "minLength": 1, "maxLength": 200},
            "category": {"type": "string", "enum": [
                "AI Products", "Enterprise Software", "Developer Tools", "Consulting Services",
                "SaaS Platforms", "Open Source Projects", "Research Initiatives", "Educational Products"
            ]},
            "stage": {"type": "string", "enum": [
                "Concept", "Research", "Planning", "Development", "Testing", "Launch", "Growth", "Mature", "Sunset"
            ]},
            "description": {"type": "string", "minLength": 10, "maxLength": 5000},
            "value_proposition": {"type": "string", "maxLength": 1000},
            "target_market": {"type": "array", "items": {"type": "string"}},
            "priority": {"type": "string", "enum": ["Critical", "High", "Medium", "Low", "Backlog"]},
            "effort": {"type": "string", "enum": ["Days", "Weeks", "Months", "Quarters", "Years"]},
            "feasibility": {
                "type": "object",
                "properties": {
                    "technical": {"type": "string", "enum": ["Proven", "Likely", "Uncertain", "Challenging", "Research Required"]},
                    "market": {"type": "string", "enum": ["Large", "Medium", "Small", "Niche", "Unknown"]}
                }
            },
            "competitive_advantage": {"type": "string", "maxLength": 1000},
            "metadata": {
                "type": "object",
                "required": ["created_date", "last_updated"],
                "properties": {
                    "created_date": {"type": "string", "format": "date-time"},
                    "last_updated": {"type": "string", "format": "date-time"},
                    "version": {"type": "string"},
                    "database_type": {"type": "string"},
                    "validation_status": {"type": "string"}
                }
            }
        }
    },
    
    "learning_resources": {
        "type": "object",
        "required": ["resource_name", "type", "category", "description"],
        "properties": {
            "resource_name": {"type": "string", "minLength": 1, "maxLength": 200},
            "type": {"type": "string", "enum": [
                "Course", "Certification", "Tutorial", "Documentation", "Book", "Article",
                "Video Series", "Workshop", "Conference", "Webinar"
            ]},
            "category": {"type": "string", "enum": [
                "AI Development", "Software Engineering", "Cloud Computing", "Data Science",
                "DevOps", "Project Management", "Business Strategy", "Design", "Security", "Leadership"
            ]},
            "provider": {"type": "string", "maxLength": 100},
            "description": {"type": "string", "minLength": 10, "maxLength": 1000},
            "url": {"type": "string", "format": "uri"},
            "skill_level": {"type": "string", "enum": ["Beginner", "Intermediate", "Advanced", "Expert", "All Levels"]},
            "duration": {"type": "string", "maxLength": 50},
            "cost": {"type": "string", "enum": ["Free", "Freemium", "Paid", "Subscription", "Corporate"]},
            "priority": {"type": "string", "enum": ["Critical", "High", "Medium", "Low", "Future"]},
            "status": {"type": "string", "enum": ["Not Started", "In Progress", "Completed", "Certified", "Expired"]},
            "metadata": {
                "type": "object",
                "required": ["created_date", "last_updated"],
                "properties": {
                    "created_date": {"type": "string", "format": "date-time"},
                    "last_updated": {"type": "string", "format": "date-time"},
                    "version": {"type": "string"},
                    "database_type": {"type": "string"},
                    "validation_status": {"type": "string"}
                }
            }
        }
    },
    
    "platforms_sites": {
        "type": "object",
        "required": ["platform_name", "category", "type", "description", "url"],
        "properties": {
            "platform_name": {"type": "string", "minLength": 1, "maxLength": 200},
            "category": {"type": "string", "enum": [
                "Development Platforms", "Community Forums", "Documentation Sites", "News & Blogs",
                "Learning Platforms", "Resource Libraries", "API Documentation", "Tool Directories",
                "Research Repositories", "Professional Networks"
            ]},
            "type": {"type": "string", "enum": [
                "Code Repository", "Documentation", "Community", "News Site", "Blog", "Forum",
                "Directory", "Library", "Marketplace", "Social Network"
            ]},
            "description": {"type": "string", "minLength": 10, "maxLength": 1000},
            "url": {"type": "string", "format": "uri"},
            "access": {"type": "string", "enum": ["Public", "Free Registration", "Paid Subscription", "Invitation Only", "Enterprise"]},
            "quality": {"type": "string", "enum": ["Excellent", "Good", "Average", "Poor", "Not Rated"]},
            "update_frequency": {"type": "string", "enum": ["Daily", "Weekly", "Monthly", "Quarterly", "Yearly", "Irregular", "Archived"]},
            "audience": {"type": "array", "items": {"type": "string"}},
            "specialization": {"type": "array", "items": {"type": "string"}},
            "metadata": {
                "type": "object",
                "required": ["created_date", "last_updated"],
                "properties": {
                    "created_date": {"type": "string", "format": "date-time"},
                    "last_updated": {"type": "string", "format": "date-time"},
                    "version": {"type": "string"},
                    "database_type": {"type": "string"},
                    "validation_status": {"type": "string"}
                }
            }
        }
    },
    
    "notes_ideas": {
        "type": "object",
        "required": ["note_title", "type", "content"],
        "properties": {
            "note_title": {"type": "string", "minLength": 1, "maxLength": 200},
            "type": {"type": "string", "enum": [
                "Quick Note", "Observation", "Insight", "Idea", "Reminder", "Question",
                "Discovery", "Hypothesis", "Feedback", "Reflection"
            ]},
            "category": {"type": "string", "enum": [
                "Technical", "Business", "Process", "Creative", "Research", "Learning",
                "Problem Solving", "Innovation", "Strategy", "Personal"
            ]},
            "content": {"type": "string", "minLength": 5, "maxLength": 10000},
            "priority": {"type": "string", "enum": ["Urgent", "High", "Medium", "Low", "Reference Only"]},
            "actionable": {"type": "boolean"},
            "status": {"type": "string", "enum": ["New", "Under Review", "In Progress", "Completed", "Parked", "Discarded"]},
            "tags": {"type": "array", "items": {"type": "string"}},
            "context": {"type": "string", "maxLength": 1000},
            "metadata": {
                "type": "object",
                "required": ["created_date", "last_updated"],
                "properties": {
                    "created_date": {"type": "string", "format": "date-time"},
                    "last_updated": {"type": "string", "format": "date-time"},
                    "version": {"type": "string"},
                    "database_type": {"type": "string"},
                    "validation_status": {"type": "string"}
                }
            }
        }
    }
}

class ValidationResult:
    """Container for validation results"""
    
    def __init__(self):
        self.total_files = 0
        self.valid_files = 0
        self.invalid_files = 0
        self.errors = []
        self.warnings = []
        self.file_results = {}
        
    def add_file_result(self, file_path: str, is_valid: bool, errors: List[str] = None, warnings: List[str] = None):
        """Add result for a single file"""
        self.total_files += 1
        
        if is_valid:
            self.valid_files += 1
        else:
            self.invalid_files += 1
            
        self.file_results[file_path] = {
            "valid": is_valid,
            "errors": errors or [],
            "warnings": warnings or []
        }
        
        if errors:
            self.errors.extend([f"{file_path}: {error}" for error in errors])
        if warnings:
            self.warnings.extend([f"{file_path}: {warning}" for warning in warnings])
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate"""
        return self.valid_files / self.total_files if self.total_files > 0 else 0.0
    
    @property 
    def is_valid(self) -> bool:
        """Check if all files are valid"""
        return self.invalid_files == 0

class SchemaValidator:
    """YAML schema validator with comprehensive error reporting"""
    
    def __init__(self, schema_definitions: Dict[str, Any]):
        self.schema_definitions = schema_definitions
        self.logger = self._setup_logger()
        
    def _setup_logger(self) -> logging.Logger:
        """Setup logging configuration"""
        logger = logging.getLogger('schema_validator')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            # File handler 
            log_file = Path("operations/logs/schema_validation.log")
            log_file.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            
            # Formatter
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(formatter)
            file_handler.setFormatter(formatter)
            
            logger.addHandler(console_handler)
            logger.addHandler(file_handler)
            
        return logger
    
    def validate_file(self, file_path: Path, database_type: str) -> Tuple[bool, List[str], List[str]]:
        """
        Validate a single YAML file
        Returns: (is_valid, errors, warnings)
        """
        errors = []
        warnings = []
        
        try:
            # Load YAML file
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
                
            if not data:
                errors.append("File is empty or contains no data")
                return False, errors, warnings
            
            # Get schema for database type
            if database_type not in self.schema_definitions:
                errors.append(f"No schema defined for database type: {database_type}")
                return False, errors, warnings
            
            schema = self.schema_definitions[database_type]
            
            # Validate against schema
            try:
                jsonschema.validate(data, schema)
            except jsonschema.ValidationError as e:
                errors.append(f"Schema validation failed: {e.message}")
                if e.path:
                    errors.append(f"Error path: {' -> '.join(str(p) for p in e.path)}")
                return False, errors, warnings
            except jsonschema.SchemaError as e:
                errors.append(f"Schema definition error: {e.message}")
                return False, errors, warnings
            
            # Additional custom validations
            custom_errors, custom_warnings = self._custom_validations(data, database_type)
            errors.extend(custom_errors)
            warnings.extend(custom_warnings)
            
            return len(errors) == 0, errors, warnings
            
        except yaml.YAMLError as e:
            errors.append(f"YAML parsing error: {str(e)}")
            return False, errors, warnings
        except FileNotFoundError:
            errors.append(f"File not found: {file_path}")
            return False, errors, warnings
        except Exception as e:
            errors.append(f"Unexpected error: {str(e)}")
            return False, errors, warnings
    
    def _custom_validations(self, data: Dict[str, Any], database_type: str) -> Tuple[List[str], List[str]]:
        """Perform custom validations beyond schema"""
        errors = []
        warnings = []
        
        # Check for missing metadata
        metadata = data.get('metadata', {})
        if not metadata:
            warnings.append("Missing metadata section")
        else:
            # Check date formats
            for date_field in ['created_date', 'last_updated']:
                if date_field in metadata:
                    try:
                        datetime.fromisoformat(metadata[date_field].replace('Z', '+00:00'))
                    except ValueError:
                        errors.append(f"Invalid date format in metadata.{date_field}")
        
        # Database-specific validations
        if database_type == "tools_services":
            errors.extend(self._validate_tools_services(data))
        elif database_type == "knowledge_vault":
            errors.extend(self._validate_knowledge_vault(data))
        elif database_type == "business_ideas":
            errors.extend(self._validate_business_ideas(data))
        elif database_type == "learning_resources":
            errors.extend(self._validate_learning_resources(data))
        elif database_type == "platforms_sites":
            errors.extend(self._validate_platforms_sites(data))
        elif database_type == "notes_ideas":
            errors.extend(self._validate_notes_ideas(data))
        
        return errors, warnings
    
    def _validate_tools_services(self, data: Dict[str, Any]) -> List[str]:
        """Custom validations for tools & services"""
        errors = []
        
        # Check URL accessibility (basic format check)
        for url_field in ['website', 'documentation']:
            if url_field in data and data[url_field]:
                url = data[url_field]
                if not (url.startswith('http://') or url.startswith('https://')):
                    errors.append(f"{url_field} must start with http:// or https://")
        
        # Check tag consistency
        if 'tags' in data and data['tags']:
            valid_tags = {
                'high-priority', 'enterprise', 'open-source', 'cloud-native', 'ai-powered',
                'developer-tools', 'production-ready', 'beta', 'experimental'
            }
            for tag in data['tags']:
                if tag not in valid_tags:
                    errors.append(f"Unknown tag: {tag}. Consider using standard tags.")
        
        return errors
    
    def _validate_knowledge_vault(self, data: Dict[str, Any]) -> List[str]:
        """Custom validations for knowledge vault"""
        errors = []
        
        # Check concept consistency
        if 'concepts' in data and data['concepts']:
            valid_concepts = {
                'AI Development', 'Prompt Engineering', 'System Design', 'Quality Assurance',
                'Performance Optimization', 'Security', 'Scalability', 'User Experience',
                'Team Collaboration', 'Process Improvement'
            }
            for concept in data['concepts']:
                if concept not in valid_concepts:
                    errors.append(f"Unknown concept: {concept}. Consider using standard concepts.")
        
        return errors
    
    def _validate_business_ideas(self, data: Dict[str, Any]) -> List[str]:
        """Custom validations for business ideas"""
        errors = []
        
        # Check feasibility consistency
        if 'feasibility' in data:
            feasibility = data['feasibility']
            if isinstance(feasibility, dict):
                technical = feasibility.get('technical')
                market = feasibility.get('market')
                
                # Warn if technical is challenging but market is large
                if technical == "Challenging" and market == "Large":
                    # This is a warning, not an error
                    pass
                    
        return errors
    
    def _validate_learning_resources(self, data: Dict[str, Any]) -> List[str]:
        """Custom validations for learning resources"""
        errors = []
        
        # Check duration format
        if 'duration' in data and data['duration']:
            duration = data['duration']
            # Basic check for common duration patterns
            if not any(unit in duration.lower() for unit in ['hour', 'day', 'week', 'month', 'year']):
                errors.append("Duration should include time units (hours, days, weeks, months, years)")
        
        return errors
    
    def _validate_platforms_sites(self, data: Dict[str, Any]) -> List[str]:
        """Custom validations for platforms & sites"""
        errors = []
        
        # URL is required and must be valid format
        if 'url' in data and data['url']:
            url = data['url']
            if not (url.startswith('http://') or url.startswith('https://')):
                errors.append("URL must start with http:// or https://")
        
        return errors
    
    def _validate_notes_ideas(self, data: Dict[str, Any]) -> List[str]:
        """Custom validations for notes & ideas"""
        errors = []
        
        # Check content length for specific note types
        note_type = data.get('type', '')
        content = data.get('content', '')
        
        if note_type in ['Discovery', 'Insight'] and len(content) < 50:
            errors.append(f"{note_type} notes should have substantial content (minimum 50 characters)")
        
        return errors
    
    def validate_directory(self, source_dir: Path, validation_level: str = "strict") -> ValidationResult:
        """
        Validate all YAML files in a directory structure
        validation_level: "strict", "normal", or "lenient"
        """
        result = ValidationResult()
        
        self.logger.info(f"Starting validation of directory: {source_dir}")
        
        # Find all YAML files organized by database type
        for database_type in self.schema_definitions.keys():
            db_dir = source_dir / "databases" / database_type
            
            if not db_dir.exists():
                self.logger.warning(f"Database directory not found: {db_dir}")
                continue
            
            yaml_files = list(db_dir.glob("*.yaml")) + list(db_dir.glob("*.yml"))
            
            if not yaml_files:
                self.logger.warning(f"No YAML files found in: {db_dir}")
                continue
            
            self.logger.info(f"Validating {len(yaml_files)} files in {database_type}")
            
            for yaml_file in yaml_files:
                is_valid, errors, warnings = self.validate_file(yaml_file, database_type)
                
                # Apply validation level filtering
                if validation_level == "lenient" and warnings and not errors:
                    is_valid = True  # Accept with warnings in lenient mode
                
                result.add_file_result(str(yaml_file), is_valid, errors, warnings)
                
                if is_valid:
                    self.logger.debug(f"✓ {yaml_file.name}")
                else:
                    self.logger.error(f"✗ {yaml_file.name}: {'; '.join(errors)}")
        
        self.logger.info(f"Validation complete: {result.valid_files}/{result.total_files} files valid")
        return result
    
    def generate_validation_report(self, result: ValidationResult, output_file: Path):
        """Generate comprehensive validation report"""
        report = {
            "validation_summary": {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "total_files": result.total_files,
                "valid_files": result.valid_files,
                "invalid_files": result.invalid_files,
                "success_rate": result.success_rate,
                "overall_status": "PASS" if result.is_valid else "FAIL"
            },
            "file_results": result.file_results,
            "error_summary": {
                "total_errors": len(result.errors),
                "total_warnings": len(result.warnings),
                "all_errors": result.errors,
                "all_warnings": result.warnings
            }
        }
        
        # Add error categorization
        error_categories = {}
        for error in result.errors:
            if "Schema validation failed" in error:
                category = "schema_violation"
            elif "YAML parsing error" in error:
                category = "yaml_format"
            elif "File not found" in error:
                category = "file_access"
            elif "Invalid date format" in error:
                category = "date_format"
            elif "URL must start with" in error:
                category = "url_format"
            else:
                category = "other"
                
            error_categories[category] = error_categories.get(category, 0) + 1
            
        report["error_categorization"] = error_categories
        
        # Save report
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        self.logger.info(f"Validation report saved: {output_file}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Validate knowledge-vault YAML files against schemas')
    parser.add_argument('--source-dir', type=Path, required=True,
                        help='Source directory containing YAML files to validate')
    parser.add_argument('--validation-level', choices=['strict', 'normal', 'lenient'], 
                        default='strict', help='Validation strictness level')
    parser.add_argument('--output-report', type=Path,
                        default='operations/logs/validation_report.json',
                        help='Output file for validation report')
    parser.add_argument('--output-format', choices=['json', 'console'], 
                        default='console', help='Output format')
    
    args = parser.parse_args()
    
    try:
        # Initialize validator
        validator = SchemaValidator(SCHEMA_DEFINITIONS)
        
        # Perform validation
        result = validator.validate_directory(args.source_dir, args.validation_level)
        
        # Generate report
        validator.generate_validation_report(result, args.output_report)
        
        # Output results
        if args.output_format == 'console':
            print(f"\n📋 Schema Validation Results")
            print(f"═══════════════════════════")
            print(f"Total files: {result.total_files}")
            print(f"Valid files: {result.valid_files}")
            print(f"Invalid files: {result.invalid_files}")
            print(f"Success rate: {result.success_rate:.1%}")
            print(f"Status: {'✅ PASS' if result.is_valid else '❌ FAIL'}")
            
            if result.errors:
                print(f"\n❌ Errors ({len(result.errors)}):")
                for error in result.errors[:10]:  # Show first 10 errors
                    print(f"  • {error}")
                if len(result.errors) > 10:
                    print(f"  • ... and {len(result.errors) - 10} more errors")
                    
            if result.warnings:
                print(f"\n⚠️  Warnings ({len(result.warnings)}):")
                for warning in result.warnings[:5]:  # Show first 5 warnings
                    print(f"  • {warning}")
                if len(result.warnings) > 5:
                    print(f"  • ... and {len(result.warnings) - 5} more warnings")
            
            print(f"\n📄 Detailed report: {args.output_report}")
        
        # Exit with appropriate code
        if result.is_valid:
            print(f"\n🎯 All files passed validation!")
            sys.exit(0)
        else:
            print(f"\n💥 Validation failed - see errors above")
            sys.exit(1)
            
    except Exception as e:
        print(f"ERROR: {str(e)}")
        sys.exit(2)

if __name__ == '__main__':
    main()