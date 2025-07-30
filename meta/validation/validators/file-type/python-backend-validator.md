# Python Backend Validator

## Purpose

Specialized AI agent validator for Python backend files (.py) with API security validation, PEP compliance checking, architecture pattern validation, and performance optimization assessment.

**Unified Framework Integration**: Uses `@meta/information-access/source-discovery-framework.yaml` for consistent source discovery and backend-specific mappings, eliminating duplicate validation logic.

## Activation Criteria

**Unified Framework Integration**:
- **Technology Mappings**: `technology_mappings.python`
- **Category Mappings**: `category_mappings.backend` + `category_mappings.database`
- **Source Discovery**: Leverages unified framework source selection algorithm

**File Patterns:**
- `**/*.py` (Python modules)
- `api/**/*.py` (API endpoints)
- `backend/**/*.py` (Backend services)
- `src/**/*.py` (Source modules)
- `app/**/*.py` (Application code)
- `services/**/*.py` (Service layer)

**Context Indicators:**
- FastAPI, Django, Flask dependencies in requirements.txt/pyproject.toml
- API route definitions (`@app.route`, `@router.get`)
- Database ORM imports (SQLAlchemy, Django ORM, Tortoise)
- Authentication middleware (JWT, OAuth implementations)
- Async/await patterns for API handling

**Information Sources** (from unified framework):
- **Primary**: `technology_mappings.python.sources.primary`
- **Supplementary**: `technology_mappings.python.sources.supplementary`
- **Backend Patterns**: `category_mappings.backend.sources`
- **Database Integration**: `category_mappings.database.sources`

## Validation Scope

### 1. API Security and Authentication
- **Input Validation**: Proper request validation and sanitization
- **Authentication Patterns**: JWT, OAuth, API key implementations
- **Authorization Logic**: Role-based access control (RBAC) validation
- **SQL Injection Prevention**: ORM usage and parameterized queries
- **Rate Limiting**: API throttling and abuse prevention
- **CORS Configuration**: Cross-origin request security

### 2. PEP Compliance and Code Quality
- **PEP 8**: Style guide compliance (imports, naming, formatting)
- **PEP 484**: Type hints and annotations
- **PEP 257**: Docstring conventions
- **Import Organization**: Proper import grouping and ordering
- **Naming Conventions**: Function, class, and variable naming

### 3. Architecture and Design Patterns
- **Dependency Injection**: Service layer organization
- **Repository Pattern**: Data access layer abstraction
- **Factory Pattern**: Object creation and configuration
- **Singleton Usage**: Appropriate singleton implementations
- **Error Handling**: Exception hierarchy and error propagation

### 4. Database and ORM Patterns
- **Query Optimization**: Efficient database queries
- **Migration Patterns**: Database schema management
- **Connection Pooling**: Database connection efficiency
- **Transaction Management**: ACID compliance and rollback handling
- **Data Validation**: Model validation and constraints

### 5. Performance and Scalability
- **Async/Await Usage**: Proper asynchronous programming
- **Caching Strategies**: Redis, Memcached implementations
- **Background Tasks**: Celery, asyncio task management
- **Memory Management**: Memory leaks and optimization
- **API Response Times**: Performance bottleneck identification

### 6. Testing and Quality Assurance
- **Test Coverage**: Unit and integration test presence
- **Test Patterns**: pytest fixtures and mocking
- **API Testing**: FastAPI TestClient, Django test cases
- **Mock Usage**: Proper external dependency mocking
- **Test Data Management**: Factory patterns for test data

## AI Agent Instructions

### Phase 1: Python Environment Analysis

**AI Agent Execution Steps:**

1. **Identify Python Files**: Use Glob tool with pattern `**/*.py`
2. **Framework Detection**: Read requirements.txt, pyproject.toml, setup.py
3. **Project Structure Assessment**: Analyze directory structure for architecture patterns
4. **Configuration Analysis**: Check settings.py, config files, environment variables

### Phase 2: Security Validation

**For each .py file containing API endpoints:**

1. **Read File Content**: Use Read tool to analyze Python code
2. **Input Validation Assessment**:
   ```python
   # Good patterns to validate for:
   from pydantic import BaseModel, Field, validator
   
   class UserCreateRequest(BaseModel):
       email: str = Field(..., regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')
       password: str = Field(..., min_length=8, max_length=128)
       
       @validator('password')
       def validate_password_strength(cls, v):
           if not re.search(r'[A-Z]', v):
               raise ValueError('Password must contain uppercase letter')
           return v
   ```

3. **Authentication Pattern Validation**:
   ```python
   # Check for proper JWT handling:
   from fastapi import Depends, HTTPException, status
   from fastapi.security import HTTPBearer
   
   security = HTTPBearer()
   
   async def get_current_user(token: str = Depends(security)):
       try:
           payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
           user_id = payload.get("sub")
           if user_id is None:
               raise HTTPException(status_code=401, detail="Invalid token")
           return await get_user_by_id(user_id)
       except jwt.PyJWTError:
           raise HTTPException(status_code=401, detail="Invalid token")
   ```

4. **Common Security Issues to Flag**:
   - SQL string concatenation instead of parameterized queries
   - Missing input validation on API endpoints
   - Hardcoded secrets or API keys
   - Insecure random number generation
   - Missing HTTPS enforcement
   - Inadequate error message information disclosure

### Phase 3: Code Quality and PEP Compliance

**PEP Compliance Assessment:**

1. **PEP 8 Style Validation**:
   ```python
   # Flag style violations:
   def badFunctionName(userName, userAge):  # Flag: snake_case required
       pass
   
   # Good patterns:
   def calculate_user_score(user_name: str, user_age: int) -> float:
       """Calculate user score based on name and age."""
       pass
   ```

2. **Type Hints Validation** (PEP 484):
   ```python
   # Good type hint patterns:
   from typing import List, Dict, Optional, Union
   
   def process_users(users: List[Dict[str, Union[str, int]]]) -> Optional[List[str]]:
       """Process list of user dictionaries."""
       pass
   
   # Flag missing type hints:
   def process_data(data):  # Flag: missing type hints
       return data
   ```

3. **Import Organization** (PEP 8):
   ```python
   # Good import organization:
   import os
   import sys
   from datetime import datetime
   
   import requests
   from fastapi import FastAPI
   
   from .models import User
   from .services import UserService
   ```

### Phase 4: Architecture Pattern Validation

**Design Pattern Assessment:**

1. **Repository Pattern Validation**:
   ```python
   # Check for proper repository pattern:
   from abc import ABC, abstractmethod
   
   class UserRepository(ABC):
       @abstractmethod
       async def get_user_by_id(self, user_id: int) -> Optional[User]:
           pass
       
       @abstractmethod
       async def create_user(self, user_data: UserCreateRequest) -> User:
           pass
   
   class SQLUserRepository(UserRepository):
       async def get_user_by_id(self, user_id: int) -> Optional[User]:
           # Implementation
           pass
   ```

2. **Dependency Injection Validation**:
   ```python
   # Check for proper DI patterns:
   from fastapi import Depends
   
   def get_user_service() -> UserService:
       return UserService(get_user_repository())
   
   @router.post("/users")
   async def create_user(
       user_data: UserCreateRequest,
       user_service: UserService = Depends(get_user_service)
   ):
       return await user_service.create_user(user_data)
   ```

### Phase 5: Database and Performance Analysis

**Database Pattern Validation:**

1. **ORM Usage Assessment**:
   ```python
   # Good SQLAlchemy patterns:
   from sqlalchemy.orm import Session
   from sqlalchemy import select
   
   async def get_users_with_posts(session: Session, limit: int = 10):
       result = await session.execute(
           select(User)
           .options(selectinload(User.posts))
           .limit(limit)
       )
       return result.scalars().all()
   ```

2. **Query Optimization Check**:
   ```python
   # Flag N+1 query problems:
   users = await session.execute(select(User).limit(10))
   for user in users:
       posts = await session.execute(  # Flag: N+1 query
           select(Post).where(Post.user_id == user.id)
       )
   
   # Good pattern with eager loading:
   users = await session.execute(
       select(User).options(selectinload(User.posts)).limit(10)
   )
   ```

**Performance Pattern Analysis:**

1. **Async/Await Validation**:
   ```python
   # Check for proper async patterns:
   import asyncio
   
   async def fetch_user_data(user_id: int) -> UserData:
       user_task = fetch_user(user_id)
       posts_task = fetch_user_posts(user_id)
       
       user, posts = await asyncio.gather(user_task, posts_task)
       return UserData(user=user, posts=posts)
   ```

### Phase 6: Testing and Quality Assessment

**Test Coverage Analysis:**

1. **Test Presence Validation**:
   ```python
   # Check for proper test patterns:
   import pytest
   from fastapi.testclient import TestClient
   
   @pytest.fixture
   def test_client():
       return TestClient(app)
   
   @pytest.fixture
   def sample_user():
       return UserFactory.create()
   
   def test_create_user_success(test_client, sample_user):
       response = test_client.post("/users", json=sample_user.dict())
       assert response.status_code == 201
       assert response.json()["email"] == sample_user.email
   ```

2. **Mock Usage Assessment**:
   ```python
   # Check for proper mocking:
   from unittest.mock import AsyncMock, patch
   
   @patch('app.services.user_service.send_email')
   async def test_user_registration_sends_email(mock_send_email):
       mock_send_email.return_value = AsyncMock()
       # Test implementation
   ```

## Validation Output Format

### Success Report Template

```yaml
python_backend_validation:
  files_processed: [count]
  validation_time: "[duration]"
  
  security_score: "[0-100]"
  security_issues:
    - file: "api/auth.py"
      line: 45
      issue: "Hardcoded JWT secret key"
      severity: "critical"
      recommendation: "Use environment variable for JWT_SECRET_KEY"
    - file: "api/users.py"
      line: 23
      issue: "Missing input validation on user creation endpoint"
      severity: "high"
      recommendation: "Add Pydantic model validation for request body"
  
  code_quality_score: "[0-100]"
  pep_compliance:
    pep8_score: "[0-100]"
    type_hints_coverage: "[0-100]"
    docstring_coverage: "[0-100]"
    import_organization: "good"
  
  architecture_score: "[0-100]"
  design_patterns:
    repository_pattern: "implemented"
    dependency_injection: "partial"
    error_handling: "needs_improvement"
    separation_of_concerns: "good"
  
  database_score: "[0-100]"
  database_issues:
    - issue: "Potential N+1 query in user/posts endpoint"
      file: "api/users.py"
      line: 67
      recommendation: "Use eager loading with selectinload"
  
  performance_score: "[0-100]"
  performance_analysis:
    async_usage: "appropriate"
    caching_implementation: "missing"
    memory_efficiency: "good"
    response_time_optimization: "needs_review"
  
  testing_score: "[0-100]"
  test_coverage:
    unit_tests: "65%"
    integration_tests: "40%"
    api_tests: "80%"
    test_quality: "good"
  
  overall_score: "[0-100]"
  
  recommendations:
    - "Move JWT secret to environment variables"
    - "Add comprehensive input validation using Pydantic"
    - "Implement caching layer for frequently accessed data"
    - "Add missing unit tests for service layer"
    - "Optimize database queries to prevent N+1 problems"
  
  critical_issues:
    - count: 1
    - blocking_deployment: true
    - details: ["Hardcoded secrets present"]
  
  compliance_checks:
    owasp_api_security: "partial"
    pci_dss_requirements: "not_applicable"
    gdpr_compliance: "review_required"
  
  next_steps:
    - "Address critical security issues immediately"
    - "Implement missing test coverage"
    - "Review database query optimization opportunities"
    - "Add comprehensive API documentation"
```

## Framework Integration

### AI Agent Instruction Design Excellence Compliance

**Concrete Specificity:**
- Explicit Python file patterns and validation criteria
- Specific security patterns and anti-patterns
- Clear architecture and performance requirements

**External Dependency Elimination:**
- Self-contained validation logic for common frameworks
- Embedded security and performance check patterns
- No external linting tool dependencies

**Immediate Actionability:**
- Step-by-step validation process for each file type
- Clear output format with actionable recommendations
- Specific tool usage instructions (Read, Glob)

**Constitutional AI Compliance:**
- Ethical security assessment without bias
- Constructive code quality recommendations
- Responsible disclosure of security vulnerabilities

### Progressive Context Loading

**Base Context (200 tokens):**
- File pattern recognition
- Basic Python validation criteria
- Security assessment framework

**Framework-Specific Context (400-600 tokens):**
- FastAPI patterns and validation
- Django ORM and security patterns
- Flask application structure validation
- SQLAlchemy query optimization

**Specialized Context (300-500 tokens):**
- Advanced security patterns (OAuth, JWT)
- Performance optimization techniques
- Testing framework integration
- Database optimization patterns

## Quality Metrics

### Validation Effectiveness Targets

- **Security Coverage**: ≥99% of OWASP Top 10 vulnerabilities detected
- **PEP Compliance**: ≥95% of style and convention violations identified
- **Architecture Assessment**: ≥90% of design pattern violations flagged
- **Performance Analysis**: ≥85% of optimization opportunities identified
- **Testing Coverage**: ≥90% of missing test scenarios flagged

### Performance Targets

- **Processing Speed**: ≤90 seconds for 100 Python files
- **Memory Efficiency**: ≤150MB peak memory usage
- **Security Scan Time**: ≤30 seconds for vulnerability assessment
- **Report Generation**: ≤20 seconds for comprehensive output

### Constitutional AI Validation

- **Accuracy**: ≥98% correct security issue identification
- **Completeness**: ≥95% coverage of validation scope
- **Consistency**: ≥97% repeatable results across runs
- **Responsibility**: Security-focused recommendations without false alarms
- **Transparency**: Clear reasoning for all flagged issues and recommendations

## Integration Notes

### Validator Registry Integration

```yaml
python-backend-validator:
  location: "meta/validation/validators/file-type/python-backend-validator.md"
  file_patterns: ["**/*.py"]
  specialization: "Backend Python security, PEP compliance, and architecture validation"
  dependencies: ["security-baseline-validator"]
  parallel_safe: true
  estimated_processing_time: "60-90s for typical backend codebase"
  quality_score: "pending_measurement"
  constitutional_ai_compliance: true
  framework_compliance_version: "1.0"
```

### Command Integration

This validator integrates with `/validate-pr` command through:
- Conditional activation based on Python file detection
- Parallel execution with other file-type validators
- Security-priority result aggregation into comprehensive PR validation report
- Progressive context loading for framework-specific validation

### Security Integration

- **OWASP API Security Top 10**: Comprehensive coverage of API security risks
- **SANS Top 25**: Software vulnerability pattern detection
- **CVE Database Integration**: Known vulnerability pattern matching
- **Security Baseline Validation**: Integration with security-baseline-validator

### Future Enhancements

- **Advanced Static Analysis**: Integration with bandit, semgrep for deeper security analysis
- **Performance Profiling**: Integration with memory profilers and performance monitoring
- **Framework Evolution**: Enhanced patterns for newer Python frameworks (Starlette, Litestar)
- **ML-Based Vulnerability Detection**: Machine learning enhanced security pattern recognition