---
name: op-implement-code
description: Implement code changes per task requirements
parent-skill: ampa-task-execution
---

# Implement Code

## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
- [Examples](#examples)
- [Error Handling](#error-handling)

> **Token rule**: Write all command output to a report file. Return only a 2-3 line summary + file path to the caller.

Write code that fulfills the task requirements and acceptance criteria.

## When to Use

Use this operation when:
- Development environment is configured and ready
- Requirements are fully understood
- You are ready to write the actual implementation

## Prerequisites

Before executing this operation:
1. Environment setup must be complete (op-setup-development-environment completed)
2. Acceptance criteria must be documented
3. Target files and components must be identified
4. SERENA MCP must be active for code navigation

## Procedure

### Step 4.1: Analyze Existing Code Structure with SERENA

Before writing any code, understand the existing codebase:

```
# Get overall structure
mcp__serena__get_codebase_structure()

# Find related components
mcp__serena__find_symbol("RelatedClass")

# Get implementation details
mcp__serena__get_symbol_details("RelatedClass")
```

Document patterns to follow:

| Pattern | Example Location | Description |
|---------|------------------|-------------|
| Naming convention | src/services/user_service.py | snake_case for functions |
| Error handling | src/core/exceptions.py | Custom exception classes |
| Logging pattern | src/utils/logger.py | Structured logging |
| Testing pattern | tests/unit/test_user.py | pytest with fixtures |

### Step 4.2: Plan Implementation Approach

Create an implementation plan before writing code:

1. **Identify units of work**: Break the task into small, testable pieces
2. **Order by dependencies**: Implement foundations before dependents
3. **Define interfaces first**: Write function signatures and docstrings
4. **Plan for testability**: Ensure each unit can be tested in isolation

Implementation plan template:

| Order | Component | File | Dependencies | Testable |
|-------|-----------|------|--------------|----------|
| 1 | Data model | src/models/session.py | None | Yes |
| 2 | Service layer | src/services/auth.py | models/session | Yes |
| 3 | API endpoint | src/api/routes.py | services/auth | Yes |

### Step 4.3: Write Code in Small, Testable Increments

Follow this incremental process:

1. **Write one component at a time**
   - Focus on a single function or class
   - Complete it fully before moving on

2. **Use the Read-Edit-Verify cycle**
   ```
   Read: View existing file with Read tool
   Edit: Make changes with Edit tool
   Verify: Run linter/type checker to catch errors
   ```

3. **Run verification after each change**
   ```bash
   # Lint the changed file
   uv run ruff check src/path/to/file.py

   # Type check
   uv run mypy src/path/to/file.py
   ```

4. **Commit logical units**
   - Each component that works independently should be committed
   - Commit message should reference the task ID

Code quality requirements:

| Requirement | Tool | Command |
|-------------|------|---------|
| No lint errors | ruff | `uv run ruff check src/` |
| No type errors | mypy | `uv run mypy src/` |
| Formatting | ruff | `uv run ruff format src/` |

### Step 4.4: Add Documentation and Comments

Every implementation must include:

1. **Docstrings**: For all public functions and classes

   ```python
   def authenticate_user(username: str, password: str) -> User:
       """Authenticate a user and return their profile.

       Args:
           username: The user's login name
           password: The user's password (will be hashed)

       Returns:
           User object if authentication succeeds

       Raises:
           AuthenticationError: If credentials are invalid
           UserNotFoundError: If username doesn't exist
       """
   ```

2. **Inline comments**: Explain the WHY, not the WHAT

   ```python
   # Rate limit to 5 attempts per minute to prevent brute force attacks
   if attempt_count > 5:
       raise RateLimitExceeded()
   ```

3. **Type hints**: For all function parameters and returns

   ```python
   def create_session(user_id: int, expires_in: int = 3600) -> Session:
   ```

## Checklist

- [ ] Existing code patterns analyzed with SERENA
- [ ] Implementation plan created and ordered
- [ ] Each component implemented incrementally
- [ ] Ruff lint check passes on all changed files
- [ ] Mypy type check passes on all changed files
- [ ] All public functions have docstrings
- [ ] All functions have type hints
- [ ] Inline comments explain the WHY
- [ ] Code follows existing project conventions

## Examples

### Example 1: Implementing a Service Function

Task: Add a function to validate email addresses

**Step 1: Analyze existing code**
```
mcp__serena__find_symbol("validate_")
# Found: validate_username in src/validators/user.py
```

**Step 2: Read the existing pattern**
```python
# From src/validators/user.py
def validate_username(username: str) -> bool:
    """Validate username format.

    Args:
        username: The username to validate

    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z][a-zA-Z0-9_]{2,29}$'
    return bool(re.match(pattern, username))
```

**Step 3: Implement following the pattern**
```python
def validate_email(email: str) -> bool:
    """Validate email address format.

    Uses RFC 5322 simplified pattern for common email formats.
    Does not validate deliverability, only format.

    Args:
        email: The email address to validate

    Returns:
        True if format is valid, False otherwise
    """
    # RFC 5322 simplified pattern - covers 99% of real email formats
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))
```

**Step 4: Verify**
```bash
uv run ruff check src/validators/user.py
# All checks passed

uv run mypy src/validators/user.py
# Success: no issues found
```

### Example 2: Creating a New Module

Task: Create a password reset service

**Step 1: Create the file with Edit tool**

File: `src/services/password_reset.py`
```python
"""Password reset service.

Handles password reset token generation, validation, and execution.
"""
import secrets
from datetime import datetime, timedelta
from typing import Optional

from src.models.user import User
from src.models.reset_token import ResetToken
from src.exceptions import TokenExpiredError, TokenInvalidError


class PasswordResetService:
    """Service for managing password reset operations."""

    TOKEN_EXPIRY_HOURS = 24
    TOKEN_LENGTH = 32

    def __init__(self, user_repository, token_repository):
        """Initialize the service with required repositories.

        Args:
            user_repository: Repository for user data access
            token_repository: Repository for reset token storage
        """
        self._users = user_repository
        self._tokens = token_repository

    def create_reset_token(self, email: str) -> Optional[str]:
        """Generate a password reset token for the given email.

        Args:
            email: User's email address

        Returns:
            The reset token if user exists, None otherwise
        """
        user = self._users.find_by_email(email)
        if not user:
            # Return None rather than error to prevent email enumeration
            return None

        token = secrets.token_urlsafe(self.TOKEN_LENGTH)
        expires_at = datetime.utcnow() + timedelta(hours=self.TOKEN_EXPIRY_HOURS)

        reset_token = ResetToken(
            user_id=user.id,
            token=token,
            expires_at=expires_at
        )
        self._tokens.save(reset_token)

        return token
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Ruff errors | Code style violations | Fix violations, do not skip |
| Mypy errors | Type mismatches | Add proper types, do not use Any |
| Import errors | Missing dependencies | Add to pyproject.toml with uv add |
| SERENA not finding symbol | Wrong name or scope | Try alternative names or browse structure |

## Related Operations

- [op-setup-development-environment.md](op-setup-development-environment.md) - Previous step
- [op-write-tests.md](op-write-tests.md) - Next step
- [op-validate-acceptance-criteria.md](op-validate-acceptance-criteria.md) - Verification step
