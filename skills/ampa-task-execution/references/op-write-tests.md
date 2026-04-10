---
name: op-write-tests
description: Write tests for implemented code changes
parent-skill: ampa-task-execution
---

# Write Tests

## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
- [Examples](#examples)
- [Error Handling](#error-handling)

> **Token rule**: Write all command output to a report file. Return only a 2-3
> line summary + file path to the caller.

Create tests that verify the implementation meets acceptance criteria.

## When to Use

Use this operation when:

- Code implementation is complete for a component
- You need to verify behavior matches requirements
- Acceptance criteria require test coverage as proof

## Prerequisites

Before executing this operation:

1. Code implementation must be complete (op-implement-code completed)
2. The code must pass linting and type checking
3. Test framework must be configured (pytest for Python)
4. Test dependencies must be installed

## Procedure

### Step 5.1: Identify Test Scenarios from Requirements

Map each acceptance criterion to test scenarios:

| Criterion                      | Test Scenarios                                 |
| ------------------------------ | ---------------------------------------------- |
| AC-001: Email format validated | Valid email passes, invalid fails, edge cases  |
| AC-002: Error message shown    | Error message text, visibility, dismissibility |
| AC-003: Form submission works  | Submits with valid input, blocks with invalid  |

For each scenario, identify:

- **Input**: What data or state to set up
- **Action**: What operation to perform
- **Expected**: What outcome to verify

### Step 5.2: Write Unit Tests for New Functions

Create test files following project conventions:

```python
"""Tests for email validation functionality."""
import pytest
from src.validators.user import validate_email


class TestValidateEmail:
    """Test cases for validate_email function."""

    def test_valid_email_returns_true(self):
        """Valid email addresses should return True."""
        assert validate_email("user@example.com") is True
        assert validate_email("user.name@example.com") is True
        assert validate_email("user+tag@example.co.uk") is True

    def test_invalid_email_returns_false(self):
        """Invalid email formats should return False."""
        assert validate_email("not-an-email") is False
        assert validate_email("@example.com") is False
        assert validate_email("user@") is False

    def test_empty_string_returns_false(self):
        """Empty string should return False."""
        assert validate_email("") is False

    def test_none_raises_type_error(self):
        """None input should raise TypeError."""
        with pytest.raises(TypeError):
            validate_email(None)
```

Test naming conventions:

| Convention  | Example                              |
| ----------- | ------------------------------------ |
| File name   | `test_<module>.py`                   |
| Class name  | `Test<FunctionOrClass>`              |
| Method name | `test_<condition>_<expected_result>` |

### Step 5.3: Write Integration Tests if Applicable

When testing components that interact with external systems:

```python
"""Integration tests for password reset flow."""
import pytest
from src.services.password_reset import PasswordResetService


class TestPasswordResetIntegration:
    """Integration tests for the password reset service."""

    @pytest.fixture
    def service(self, user_repository, token_repository):
        """Create a service instance with real repositories."""
        return PasswordResetService(user_repository, token_repository)

    @pytest.fixture
    def existing_user(self, user_repository):
        """Create a test user in the database."""
        user = User(email="test@example.com", username="testuser")
        user_repository.save(user)
        return user

    def test_create_token_for_existing_user(self, service, existing_user):
        """Token should be created for existing user."""
        token = service.create_reset_token("test@example.com")

        assert token is not None
        assert len(token) > 20  # Sufficient entropy

    def test_create_token_for_nonexistent_user(self, service):
        """None should be returned for nonexistent user."""
        token = service.create_reset_token("nobody@example.com")

        assert token is None

    def test_token_expires_after_24_hours(self, service, existing_user, token_repository):
        """Token should have 24-hour expiration."""
        token = service.create_reset_token("test@example.com")

        stored_token = token_repository.find_by_token(token)
        assert stored_token.expires_at > datetime.utcnow()
        assert stored_token.expires_at < datetime.utcnow() + timedelta(hours=25)
```

Do NOT use mocks unless absolutely necessary. Real tests with real components
find real bugs.

### Step 5.4: Run Tests and Fix Failures

Execute tests and verify all pass:

```bash
# Run specific test file
uv run pytest tests/unit/test_validators.py -v

# Run tests with coverage
uv run pytest tests/ --cov=src --cov-report=term-missing

# Run only tests matching a pattern
uv run pytest -k "email" -v
```

When a test fails:

1. **Read the failure output carefully**
2. **Determine if test or implementation is wrong**
3. **Fix the appropriate component**
4. **Re-run until all tests pass**

Test result interpretation:

| Result  | Meaning          | Action                      |
| ------- | ---------------- | --------------------------- |
| PASSED  | Test passed      | Continue                    |
| FAILED  | Assertion failed | Fix implementation or test  |
| ERROR   | Exception raised | Fix code error              |
| SKIPPED | Test was skipped | Verify skip reason is valid |

## Checklist

- [ ] All acceptance criteria mapped to test scenarios
- [ ] Unit tests written for all new functions
- [ ] Integration tests written for component interactions
- [ ] All tests have descriptive docstrings
- [ ] Tests follow project naming conventions
- [ ] All tests pass when run individually
- [ ] All tests pass when run together
- [ ] Test coverage meets project requirements
- [ ] No mocks used unless absolutely necessary

## Examples

### Example 1: Unit Test for Validator

Acceptance criterion: "Email format is validated on submit"

```python
"""Tests for email validation."""
import pytest
from src.validators.user import validate_email


class TestValidateEmail:
    """Tests for the validate_email function."""

    @pytest.mark.parametrize("email,expected", [
        ("user@example.com", True),
        ("user.name@example.com", True),
        ("user+tag@sub.example.com", True),
        ("u@ex.co", True),
        ("invalid", False),
        ("@example.com", False),
        ("user@", False),
        ("user@.com", False),
        ("", False),
    ])
    def test_email_validation(self, email, expected):
        """Email validation returns correct result for various inputs."""
        assert validate_email(email) is expected
```

### Example 2: Integration Test for Service

Acceptance criterion: "Reset link expires after 24 hours"

```python
"""Integration tests for token expiration."""
import pytest
from datetime import datetime, timedelta
from freezegun import freeze_time
from src.services.password_reset import PasswordResetService


class TestTokenExpiration:
    """Tests for password reset token expiration."""

    def test_token_valid_within_24_hours(self, service, test_user):
        """Token should be valid within 24-hour window."""
        token = service.create_reset_token(test_user.email)

        # Fast forward 23 hours
        with freeze_time(datetime.utcnow() + timedelta(hours=23)):
            is_valid = service.validate_token(token)

        assert is_valid is True

    def test_token_invalid_after_24_hours(self, service, test_user):
        """Token should be invalid after 24-hour window."""
        token = service.create_reset_token(test_user.email)

        # Fast forward 25 hours
        with freeze_time(datetime.utcnow() + timedelta(hours=25)):
            is_valid = service.validate_token(token)

        assert is_valid is False
```

### Example 3: Test Output Format

Running tests should produce:

```text
$ uv run pytest tests/unit/test_validators.py -v

========================= test session starts ==========================
collected 9 items

tests/unit/test_validators.py::TestValidateEmail::test_email_validation[user@example.com-True] PASSED
tests/unit/test_validators.py::TestValidateEmail::test_email_validation[user.name@example.com-True] PASSED
tests/unit/test_validators.py::TestValidateEmail::test_email_validation[invalid-False] PASSED
tests/unit/test_validators.py::TestValidateEmail::test_email_validation[@example.com-False] PASSED
...

========================= 9 passed in 0.12s ============================
```

## Error Handling

| Error                 | Cause                     | Resolution                                |
| --------------------- | ------------------------- | ----------------------------------------- |
| Test collection error | Syntax error in test file | Fix Python syntax                         |
| Import error          | Module not found          | Check import paths, run from project root |
| Fixture not found     | Missing pytest fixture    | Define fixture or import from conftest    |
| Assertion error       | Test expectation wrong    | Verify expected value is correct          |
| Timeout               | Test runs too long        | Check for infinite loops, add timeout     |

## Related Operations

- [op-implement-code.md](op-implement-code.md) - Previous step
- [op-validate-acceptance-criteria.md](op-validate-acceptance-criteria.md) -
  Next step
