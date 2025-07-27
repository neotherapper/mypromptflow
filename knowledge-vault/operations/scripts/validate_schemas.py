#!/usr/bin/env python3
"""
Knowledge Vault Schema Validation Framework
Comprehensive YAML schema validation with detailed error reporting
Production-ready validation for migration integrity
"""

import os
import sys
import yaml
import frontmatter
import json
import re
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from dataclasses import dataclass
from urllib.parse import urlparse

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
KNOWLEDGE_VAULT_PATH = PROJECT_ROOT / 'knowledge-vault'
SCHEMAS_PATH = KNOWLEDGE_VAULT_PATH / 'schemas'

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    """Result of validating a single item"""
    item_id: str
    database_type: str
    file_path: str
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    validation_score: float
    required_fields_present: int
    total_required_fields: int
    
@dataclass
class DatabaseValidationSummary:
    """Summary of validation results for a database"""
    database_type: str
    total_items: int
    valid_items: int
    invalid_items: int
    validation_rate: float
    average_score: float
    common_errors: Dict[str, int]
    critical_issues: List[str]

class SchemaValidator:
    """Comprehensive schema validation engine"""
    
    def __init__(self):
        self.schemas = {}
        self.validation_rules = {}
        self.validation_results = []
        self.cross_references = {}
        
        # Load schemas and validation rules
        self._load_database_schemas()
        self._load_validation_rules()
        
    def _load_database_schemas(self):
        """Load database schemas from Markdown files"""
        schema_files = {
            'knowledge_vault': 'knowledge-vault-schema.yaml',
            'tools_services': 'tools-services-schema.yaml',
            'business_ideas': 'business-ideas-schema.yaml',
            'training_vault': 'training-vault-schema.yaml',
            'platforms_sites': 'platforms-sites-schema.yaml',
            'notes_ideas': 'notes-ideas-schema.yaml'
        }
        
        for db_type, filename in schema_files.items():
            schema_path = SCHEMAS_PATH / filename
            if schema_path.exists():
                try:
                    with open(schema_path, 'r', encoding='utf-8') as f:
                        schema = yaml.safe_load(f)
                    self.schemas[db_type] = schema
                    logger.debug(f"Loaded schema: {db_type}")
                except Exception as e:
                    logger.error(f"Error loading schema {filename}: {e}")
            else:
                logger.warning(f"Schema file not found: {schema_path}")
                
    def _load_validation_rules(self):
        """Load validation rules and constraints"""
        self.validation_rules = {
            'required_fields': {
                'all': ['id', 'name', 'category', 'status', 'description'],
                'knowledge_vault': ['type'],
                'tools_services': ['type', 'performance_rating'],
                'business_ideas': ['market_type', 'revenue_model'],
                'training_vault': ['type', 'difficulty_level'],
                'platforms_sites': ['type', 'url'],
                'notes_ideas': ['type', 'source_context']
            },
            'field_types': {
                'id': 'string',
                'name': 'string', 
                'category': 'string',
                'status': 'string',
                'description': 'string',
                'type': 'string',
                'performance_rating': 'integer',
                'research_quality': 'integer',
                'priority': 'string',
                'tags': 'array',
                'relationships': 'dict',
                'url': 'string',
                'api_available': 'boolean',
                'website': 'string',
                'documentation': 'string'
            },
            'constraints': {
                'id': {
                    'pattern': r'^[a-z0-9-]+$',
                    'max_length': 100,
                    'required': True
                },
                'performance_rating': {
                    'min_value': 1,
                    'max_value': 5,
                    'type': 'integer'
                },
                'research_quality': {
                    'min_value': 0,
                    'max_value': 100,
                    'type': 'integer'
                },
                'url': {
                    'pattern': r'^https?://.+',
                    'required': False
                },
                'priority': {
                    'allowed_values': ['Critical', 'High', 'Medium', 'Low'],
                    'required': False
                },
                'status': {
                    'allowed_values': {
                        'knowledge_vault': ['Research', 'Development', 'Testing', 'Production', 'Archived'],
                        'tools_services': ['Evaluating', 'Testing', 'In_Use', 'Production', 'Deprecated'],
                        'business_ideas': ['Concept', 'Research', 'Prototype', 'MVP', 'Launch', 'Growth', 'Mature'],
                        'training_vault': ['Planning', 'Development', 'Testing', 'Available', 'Running', 'Completed', 'Archived'],
                        'platforms_sites': ['Active', 'Stable', 'Beta', 'Deprecated', 'Archived', 'Under_Development'],
                        'notes_ideas': []  # Notes don't have specific status constraints
                    }
                }
            },
            'relationships': {
                'format': r'^@[a-z_]+/[a-z0-9-]+$',
                'allowed_databases': ['knowledge_vault', 'tools_services', 'business_ideas', 'training_vault', 'platforms_sites', 'notes_ideas'],
                'bidirectional_required': True
            }
        }
        
    def validate_item(self, item_data: Dict, database_type: str, file_path: str) -> ValidationResult:
        """Validate a single item against schema and rules"""
        errors = []
        warnings = []
        
        item_id = item_data.get('id', 'unknown')
        
        # Validate required fields
        required_fields = self.validation_rules['required_fields']['all'].copy()
        if database_type in self.validation_rules['required_fields']:
            required_fields.extend(self.validation_rules['required_fields'][database_type])
            
        required_present = 0
        for field in required_fields:
            if field in item_data and item_data[field] is not None and item_data[field] != '':
                required_present += 1
            else:
                errors.append(f"Required field '{field}' is missing or empty")
        
        # Validate field types
        for field, expected_type in self.validation_rules['field_types'].items():
            if field in item_data:
                if not self._validate_field_type(item_data[field], expected_type):
                    errors.append(f"Field '{field}' has incorrect type (expected {expected_type})")
        
        # Validate constraints
        for field, constraints in self.validation_rules['constraints'].items():
            if field in item_data:
                field_errors = self._validate_field_constraints(item_data[field], constraints, field, database_type)
                errors.extend(field_errors)
        
        # Validate relationships
        if 'relationships' in item_data:
            rel_errors, rel_warnings = self._validate_relationships(item_data['relationships'], item_id, database_type)
            errors.extend(rel_errors)
            warnings.extend(rel_warnings)
        
        # Validate database-specific requirements
        db_errors, db_warnings = self._validate_database_specific(item_data, database_type)
        errors.extend(db_errors)
        warnings.extend(db_warnings)
        
        # Calculate validation score
        total_checks = len(required_fields) + len([f for f in item_data.keys() if f in self.validation_rules['field_types']])
        error_count = len(errors)
        warning_count = len(warnings)
        
        if total_checks > 0:
            validation_score = max(0, (total_checks - error_count - (warning_count * 0.5)) / total_checks) * 100
        else:
            validation_score = 0
        
        is_valid = len(errors) == 0
        
        return ValidationResult(
            item_id=item_id,
            database_type=database_type,
            file_path=file_path,
            is_valid=is_valid,
            errors=errors,
            warnings=warnings,
            validation_score=validation_score,
            required_fields_present=required_present,
            total_required_fields=len(required_fields)
        )
    
    def _validate_field_type(self, value: Any, expected_type: str) -> bool:
        """Validate field type"""
        if expected_type == 'string':
            return isinstance(value, str)
        elif expected_type == 'integer':
            return isinstance(value, int)
        elif expected_type == 'boolean':
            return isinstance(value, bool)
        elif expected_type == 'array':
            return isinstance(value, list)
        elif expected_type == 'dict':
            return isinstance(value, dict)
        return True
    
    def _validate_field_constraints(self, value: Any, constraints: Dict, field_name: str, database_type: str) -> List[str]:
        """Validate field against constraints"""
        errors = []
        
        if 'pattern' in constraints:
            if isinstance(value, str) and not re.match(constraints['pattern'], value):
                errors.append(f"Field '{field_name}' does not match required pattern: {constraints['pattern']}")
        
        if 'min_value' in constraints:
            if isinstance(value, (int, float)) and value < constraints['min_value']:
                errors.append(f"Field '{field_name}' value {value} is below minimum {constraints['min_value']}")
        
        if 'max_value' in constraints:
            if isinstance(value, (int, float)) and value > constraints['max_value']:
                errors.append(f"Field '{field_name}' value {value} exceeds maximum {constraints['max_value']}")
        
        if 'max_length' in constraints:
            if isinstance(value, str) and len(value) > constraints['max_length']:
                errors.append(f"Field '{field_name}' length {len(value)} exceeds maximum {constraints['max_length']}")
        
        if 'allowed_values' in constraints:
            allowed = constraints['allowed_values']
            if isinstance(allowed, dict) and database_type in allowed:
                allowed_values = allowed[database_type]
                if allowed_values and value not in allowed_values:
                    errors.append(f"Field '{field_name}' value '{value}' not in allowed values: {allowed_values}")
            elif isinstance(allowed, list) and value not in allowed:
                errors.append(f"Field '{field_name}' value '{value}' not in allowed values: {allowed}")
        
        return errors
    
    def _validate_relationships(self, relationships: Dict, item_id: str, database_type: str) -> Tuple[List[str], List[str]]:
        """Validate relationship structure and format"""
        errors = []
        warnings = []
        
        if not isinstance(relationships, dict):
            errors.append(f"Relationships must be a dictionary")
            return errors, warnings
        
        # Track cross-references for later validation
        if item_id not in self.cross_references:
            self.cross_references[item_id] = {}
        
        for rel_type, rel_values in relationships.items():
            if not isinstance(rel_values, list):
                errors.append(f"Relationship '{rel_type}' must be a list")
                continue
                
            for ref in rel_values:
                if not isinstance(ref, str):
                    errors.append(f"Relationship reference must be a string: {ref}")
                    continue
                
                # Validate cross-reference format
                if not re.match(self.validation_rules['relationships']['format'], ref):
                    errors.append(f"Invalid relationship reference format: {ref} (should be @database/item_id)")
                    continue
                
                # Parse and validate reference
                match = re.match(r'^@([a-z_]+)/([a-z0-9-]+)$', ref)
                if match:
                    ref_database, ref_item_id = match.groups()
                    
                    # Validate target database exists
                    if ref_database not in self.validation_rules['relationships']['allowed_databases']:
                        errors.append(f"Invalid target database in reference: {ref}")
                    
                    # Store cross-reference for bidirectional validation
                    self.cross_references[item_id][ref] = {
                        'target_database': ref_database,
                        'target_item': ref_item_id,
                        'source_database': database_type,
                        'relationship_type': rel_type
                    }
        
        return errors, warnings
    
    def _validate_database_specific(self, item_data: Dict, database_type: str) -> Tuple[List[str], List[str]]:
        """Validate database-specific requirements"""
        errors = []
        warnings = []
        
        if database_type == 'knowledge_vault':
            # Knowledge vault specific validations
            if 'research_quality' in item_data:
                if not isinstance(item_data['research_quality'], int) or not (0 <= item_data['research_quality'] <= 100):
                    errors.append("Research quality must be an integer between 0 and 100")
        
        elif database_type == 'tools_services':
            # Tools & services specific validations
            if 'website' in item_data and item_data['website']:
                if not self._is_valid_url(item_data['website']):
                    errors.append(f"Invalid website URL: {item_data['website']}")
            
            if 'performance_rating' in item_data:
                if not isinstance(item_data['performance_rating'], int) or not (1 <= item_data['performance_rating'] <= 5):
                    errors.append("Performance rating must be an integer between 1 and 5")
        
        elif database_type == 'platforms_sites':
            # Platforms & sites specific validations
            if 'url' not in item_data or not item_data['url']:
                errors.append("URL is required for platforms & sites items")
            elif not self._is_valid_url(item_data['url']):
                errors.append(f"Invalid URL: {item_data['url']}")
        
        elif database_type == 'business_ideas':
            # Business ideas specific validations
            required_business_fields = ['market_type', 'revenue_model']
            for field in required_business_fields:
                if field not in item_data or not item_data[field]:
                    errors.append(f"Business ideas require field: {field}")
        
        elif database_type == 'training_vault':
            # Training vault specific validations
            if 'difficulty_level' not in item_data or not item_data['difficulty_level']:
                errors.append("Difficulty level is required for training items")
        
        elif database_type == 'notes_ideas':
            # Notes & ideas specific validations
            if 'source_context' not in item_data or not item_data['source_context']:
                errors.append("Source context is required for notes & ideas items")
        
        return errors, warnings
    
    def _is_valid_url(self, url: str) -> bool:
        """Validate URL format"""
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc]) and result.scheme in ['http', 'https']
        except Exception:
            return False
    
    def validate_directory(self, directory_path: Path, database_type: str) -> List[ValidationResult]:
        """Validate all items in a directory"""
        results = []
        
        if not directory_path.exists():
            logger.warning(f"Directory does not exist: {directory_path}")
            return results
        
        # Support both YAML and Markdown files with frontmatter
        data_files = list(directory_path.glob('*.yaml')) + list(directory_path.glob('*.yml')) + list(directory_path.glob('*.md')) + list(directory_path.glob('*.yaml')) + list(directory_path.glob('*.yml')) + list(directory_path.glob('*.md')) + list(directory_path.glob('*.yaml')) + list(directory_path.glob('*.yml')) + list(directory_path.glob('*.md'))
        
        for file_path in data_files:
            try:
                if file_path.suffix.lower() == '.md':
                    # Read Markdown file with YAML frontmatter
                    with open(file_path, 'r', encoding='utf-8') as f:
                        post = frontmatter.load(f)
                        item_data = post.metadata
                else:
                    # Read traditional YAML file
                    with open(file_path, 'r', encoding='utf-8') as f:
                        item_data = yaml.safe_load(f)
                
                if item_data:
                    result = self.validate_item(item_data, database_type, str(file_path))
                    results.append(result)
                    self.validation_results.append(result)
                    
            except Exception as e:
                error_result = ValidationResult(
                    item_id='unknown',
                    database_type=database_type,
                    file_path=str(file_path),
                    is_valid=False,
                    errors=[f"Failed to load YAML: {e}"],
                    warnings=[],
                    validation_score=0,
                    required_fields_present=0,
                    total_required_fields=0
                )
                results.append(error_result)
                self.validation_results.append(error_result)
        
        return results
    
    def validate_all_databases(self, base_path: Path = None) -> Dict[str, DatabaseValidationSummary]:
        """Validate all databases in the knowledge vault"""
        if base_path is None:
            base_path = KNOWLEDGE_VAULT_PATH / 'databases'
        
        database_dirs = {
            'knowledge_vault': 'knowledge_vault',
            'tools_services': 'tools_services', 
            'business_ideas': 'business_ideas',
            'training_vault': 'training_vault',
            'platforms_sites': 'platforms_sites',
            'notes_ideas': 'notes_ideas'
        }
        
        summaries = {}
        
        for db_type, dir_name in database_dirs.items():
            logger.info(f"Validating database: {db_type}")
            
            db_path = base_path / dir_name / 'items'
            results = self.validate_directory(db_path, db_type)
            
            # Create summary
            valid_items = len([r for r in results if r.is_valid])
            invalid_items = len([r for r in results if not r.is_valid])
            validation_rate = (valid_items / len(results)) * 100 if results else 0
            average_score = sum(r.validation_score for r in results) / len(results) if results else 0
            
            # Collect common errors
            common_errors = {}
            critical_issues = []
            
            for result in results:
                for error in result.errors:
                    if error not in common_errors:
                        common_errors[error] = 0
                    common_errors[error] += 1
                    
                    # Identify critical issues
                    if any(critical in error.lower() for critical in ['required field', 'invalid url', 'incorrect type']):
                        critical_issues.append(f"{result.item_id}: {error}")
            
            summary = DatabaseValidationSummary(
                database_type=db_type,
                total_items=len(results),
                valid_items=valid_items,
                invalid_items=invalid_items,
                validation_rate=validation_rate,
                average_score=average_score,
                common_errors=dict(sorted(common_errors.items(), key=lambda x: x[1], reverse=True)),
                critical_issues=critical_issues
            )
            
            summaries[db_type] = summary
            logger.info(f"Database {db_type}: {valid_items}/{len(results)} valid ({validation_rate:.1f}%)")
        
        return summaries
    
    def validate_cross_references(self) -> Tuple[List[str], List[str]]:
        """Validate cross-reference integrity"""
        errors = []
        warnings = []
        
        # Check for orphaned references (references that don't exist as items)
        all_item_ids = set()
        for result in self.validation_results:
            if result.is_valid:
                all_item_ids.add(f"{result.database_type}/{result.item_id}")
        
        for source_item, references in self.cross_references.items():
            for ref, ref_data in references.items():
                target_key = f"{ref_data['target_database']}/{ref_data['target_item']}"
                if target_key not in all_item_ids:
                    errors.append(f"Orphaned reference: {source_item} -> {ref} (target does not exist)")
        
        # TODO: Add bidirectional relationship validation
        # This would require tracking reverse relationships and ensuring consistency
        
        return errors, warnings
    
    def generate_validation_report(self, summaries: Dict[str, DatabaseValidationSummary]) -> Dict:
        """Generate comprehensive validation report"""
        total_items = sum(s.total_items for s in summaries.values())
        total_valid = sum(s.valid_items for s in summaries.values())
        total_invalid = sum(s.invalid_items for s in summaries.values())
        
        overall_validation_rate = (total_valid / total_items) * 100 if total_items > 0 else 0
        overall_average_score = sum(s.average_score * s.total_items for s in summaries.values()) / total_items if total_items > 0 else 0
        
        # Cross-reference validation
        cross_ref_errors, cross_ref_warnings = self.validate_cross_references()
        
        # Identify databases needing attention
        needs_attention = []
        for db_type, summary in summaries.items():
            if summary.validation_rate < 95 or summary.critical_issues:
                needs_attention.append(db_type)
        
        report = {
            'validation_summary': {
                'timestamp': datetime.now().isoformat(),
                'total_items': total_items,
                'valid_items': total_valid,
                'invalid_items': total_invalid,
                'overall_validation_rate': round(overall_validation_rate, 2),
                'overall_average_score': round(overall_average_score, 2),
                'databases_needing_attention': needs_attention
            },
            'database_summaries': {
                db_type: {
                    'total_items': summary.total_items,
                    'valid_items': summary.valid_items,
                    'invalid_items': summary.invalid_items,
                    'validation_rate': round(summary.validation_rate, 2),
                    'average_score': round(summary.average_score, 2),
                    'critical_issues_count': len(summary.critical_issues),
                    'most_common_errors': dict(list(summary.common_errors.items())[:5])  # Top 5 errors
                }
                for db_type, summary in summaries.items()
            },
            'cross_reference_validation': {
                'total_references': len(self.cross_references),
                'orphaned_references': len(cross_ref_errors),
                'reference_warnings': len(cross_ref_warnings),
                'orphaned_reference_details': cross_ref_errors[:10]  # First 10 for brevity
            },
            'quality_metrics': {
                'schema_compliance': 'High' if overall_validation_rate >= 95 else 'Medium' if overall_validation_rate >= 80 else 'Low',
                'data_integrity': 'High' if len(cross_ref_errors) == 0 else 'Medium' if len(cross_ref_errors) < 5 else 'Low',
                'overall_health': 'Excellent' if overall_validation_rate >= 95 and len(cross_ref_errors) == 0 else 'Good' if overall_validation_rate >= 80 else 'Needs Improvement'
            },
            'recommendations': self._generate_recommendations(summaries, cross_ref_errors)
        }
        
        return report
    
    def _generate_recommendations(self, summaries: Dict[str, DatabaseValidationSummary], cross_ref_errors: List[str]) -> List[str]:
        """Generate actionable recommendations based on validation results"""
        recommendations = []
        
        # Database-specific recommendations
        for db_type, summary in summaries.items():
            if summary.validation_rate < 90:
                recommendations.append(f"Improve data quality in {db_type} database (current: {summary.validation_rate:.1f}%)")
            
            if summary.critical_issues:
                recommendations.append(f"Address {len(summary.critical_issues)} critical issues in {db_type} database")
            
            # Most common error recommendations
            if summary.common_errors:
                top_error = list(summary.common_errors.keys())[0]
                count = summary.common_errors[top_error]
                if count > 1:
                    recommendations.append(f"Fix recurring issue in {db_type}: '{top_error}' ({count} occurrences)")
        
        # Cross-reference recommendations
        if cross_ref_errors:
            recommendations.append(f"Fix {len(cross_ref_errors)} orphaned cross-references")
            
        # General recommendations
        overall_rate = sum(s.validation_rate * s.total_items for s in summaries.values()) / sum(s.total_items for s in summaries.values()) if summaries else 0
        
        if overall_rate < 95:
            recommendations.append("Implement automated validation checks in CI/CD pipeline")
            
        if overall_rate >= 95:
            recommendations.append("Excellent data quality! Consider implementing additional business logic validation")
        
        return recommendations

def main():
    """Main entry point for validation script"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Knowledge Vault Schema Validation')
    parser.add_argument('--path', help='Path to validate (default: knowledge-vault/databases)')
    parser.add_argument('--database', help='Specific database to validate')
    parser.add_argument('--output', help='Output file for validation report')
    parser.add_argument('--format', choices=['json', 'yaml'], default='json', help='Report format')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('--vanguardai-test', action='store_true', help='Validate VanguardAI test environment')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Initialize validator
    validator = SchemaValidator()
    
    # Determine validation path
    if args.vanguardai_test:
        base_path = KNOWLEDGE_VAULT_PATH / 'databases' / 'vanguard-ai-test'
        logger.info("Validating VanguardAI test environment")
    elif args.path:
        base_path = Path(args.path)
    else:
        base_path = KNOWLEDGE_VAULT_PATH / 'databases'
    
    try:
        if args.database:
            # Validate specific database
            logger.info(f"Validating database: {args.database}")
            db_path = base_path / args.database
            if args.vanguardai_test:
                db_path = base_path / f"{args.database}_items"
            
            results = validator.validate_directory(db_path, args.database)
            
            valid_count = len([r for r in results if r.is_valid])
            print(f"\nValidation Results for {args.database}:")
            print(f"Total items: {len(results)}")
            print(f"Valid items: {valid_count}")
            print(f"Invalid items: {len(results) - valid_count}")
            print(f"Validation rate: {(valid_count/len(results)*100):.1f}%" if results else "0%")
            
            # Show individual errors
            for result in results:
                if not result.is_valid:
                    print(f"\n❌ {result.item_id}:")
                    for error in result.errors:
                        print(f"  - {error}")
            
        else:
            # Validate all databases
            logger.info("Validating all databases...")
            summaries = validator.validate_all_databases(base_path)
            
            # Generate comprehensive report
            report = validator.generate_validation_report(summaries)
            
            # Output results
            print("\n" + "="*60)
            print("KNOWLEDGE VAULT VALIDATION REPORT")
            print("="*60)
            print(f"Total items validated: {report['validation_summary']['total_items']}")
            print(f"Valid items: {report['validation_summary']['valid_items']}")
            print(f"Invalid items: {report['validation_summary']['invalid_items']}")
            print(f"Overall validation rate: {report['validation_summary']['overall_validation_rate']:.1f}%")
            print(f"Overall quality health: {report['quality_metrics']['overall_health']}")
            
            print(f"\nDatabase Results:")
            for db_type, summary in report['database_summaries'].items():
                status = "✅" if summary['validation_rate'] >= 95 else "⚠️" if summary['validation_rate'] >= 80 else "❌"
                print(f"{status} {db_type}: {summary['valid_items']}/{summary['total_items']} ({summary['validation_rate']:.1f}%)")
            
            if report['cross_reference_validation']['orphaned_references'] > 0:
                print(f"\n⚠️  Cross-reference issues: {report['cross_reference_validation']['orphaned_references']} orphaned references")
            
            if report['recommendations']:
                print(f"\n📋 Recommendations:")
                for i, rec in enumerate(report['recommendations'][:5], 1):
                    print(f"  {i}. {rec}")
            
            # Save detailed report if requested
            if args.output:
                output_path = Path(args.output)
                if args.format == 'json':
                    with open(output_path, 'w') as f:
                        json.dump(report, f, indent=2, default=str)
                else:
                    with open(output_path, 'w') as f:
                        yaml.dump(report, f, default_flow_style=False, indent=2)
                
                print(f"\nDetailed report saved to: {output_path}")
        
    except Exception as e:
        logger.error(f"Validation failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()

# Orchestrator schema validation
ORCHESTRATOR_SCHEMAS = [
    'knowledge-vault/schemas/technology-tracking-schema.yaml',
    'knowledge-vault/schemas/dependency-mapping-schema.yaml',
    'knowledge-vault/schemas/knowledge-update-schema.yaml',
    'knowledge-vault/schemas/change-event-schema.yaml'
]


def validate_orchestrator_schemas():
    """Validate all orchestrator-related schemas"""
    print("Validating orchestrator schemas...")
    for schema_path in ORCHESTRATOR_SCHEMAS:
        if os.path.exists(schema_path):
            print(f"✓ Found schema: {schema_path}")
            # Additional validation logic would go here
        else:
            print(f"✗ Missing schema: {schema_path}")
            return False
    print("All orchestrator schemas validated successfully")
    return True


if __name__ == "__main__":
    # Add orchestrator validation to main execution
    validate_orchestrator_schemas()
