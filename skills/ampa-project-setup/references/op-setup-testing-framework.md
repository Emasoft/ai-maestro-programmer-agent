---
name: op-setup-testing-framework
description: Configure the testing framework for the project.
parent-skill: ampa-project-setup
operation-number: 5
---

# Operation: Setup Testing Framework


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Python: pytest Configuration](#python-pytest-configuration)
  - [JavaScript/TypeScript: jest or vitest Configuration](#javascripttypescript-jest-or-vitest-configuration)
  - [Rust: cargo test Configuration](#rust-cargo-test-configuration)
  - [Go: go test Configuration](#go-go-test-configuration)
  - [.NET: dotnet test Configuration](#net-dotnet-test-configuration)
  - [C/C++: gtest Configuration](#cc-gtest-configuration)
  - [Swift: XCTest Configuration](#swift-xctest-configuration)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example 1: Python pytest Setup](#example-1-python-pytest-setup)
  - [Example 2: TypeScript vitest Setup](#example-2-typescript-vitest-setup)
  - [Example 3: Rust cargo test Setup](#example-3-rust-cargo-test-setup)
- [Error Handling](#error-handling)
  - [Tests Not Found](#tests-not-found)
  - [Import Errors in Tests](#import-errors-in-tests)
  - [Tests Hang or Timeout](#tests-hang-or-timeout)
  - [Coverage Not Working](#coverage-not-working)

This operation configures the testing framework appropriate for the project language, enabling test execution and coverage reporting.

## When to Use

Use this operation when:
- Setting up a new project that needs testing
- Existing project lacks testing configuration
- Migrating to a different testing framework
- Adding test coverage reporting

Do NOT use when:
- Testing framework is already configured and working
- Project has no need for automated tests
- Working in a read-only environment

## Prerequisites

Before executing this operation:
1. Package manager has been initialized (see op-initialize-package-manager.md)
2. Dependencies have been installed (see op-install-dependencies.md)
3. You have write access to create configuration files and test directories

## Procedure

### Python: pytest Configuration

**Step 1: Install pytest and plugins**
```bash
source .venv/bin/activate
uv add --dev pytest pytest-cov pytest-asyncio
```

**Step 2: Create pytest configuration**

Add to `pyproject.toml`:
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "-v",
    "--tb=short",
    "--strict-markers",
]
asyncio_mode = "auto"

[tool.coverage.run]
source = ["src"]
branch = true

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "raise NotImplementedError",
]
```

**Step 3: Create tests directory structure**
```bash
mkdir -p tests/unit tests/integration
touch tests/__init__.py
touch tests/unit/__init__.py
touch tests/integration/__init__.py
```

**Step 4: Create sample test**

Create `tests/unit/test_sample.py`:
```python
"""Sample test to verify pytest is working."""

def test_sample_passes():
    """Verify basic test execution works."""
    assert True

def test_addition():
    """Verify simple arithmetic."""
    assert 1 + 1 == 2
```

**Step 5: Verify pytest works**
```bash
uv run pytest tests/ -v
```

### JavaScript/TypeScript: jest or vitest Configuration

**vitest is preferred for modern projects. Use jest for legacy compatibility.**

#### vitest Setup

**Step 1: Install vitest**

With bun:
```bash
bun add -d vitest @vitest/coverage-v8
```

**Step 2: Create vitest configuration**

Create `vitest.config.ts`:
```typescript
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    include: ['tests/**/*.test.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html'],
    },
  },
});
```

**Step 3: Create tests directory**
```bash
mkdir -p tests
```

**Step 4: Create sample test**

Create `tests/sample.test.ts`:
```typescript
import { describe, it, expect } from 'vitest';

describe('Sample', () => {
  it('should pass', () => {
    expect(true).toBe(true);
  });

  it('should add numbers', () => {
    expect(1 + 1).toBe(2);
  });
});
```

**Step 5: Add test script to package.json**
```json
{
  "scripts": {
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage"
  }
}
```

**Step 6: Verify vitest works**
```bash
bun run test
```

#### jest Setup (Alternative)

**Step 1: Install jest**
```bash
bun add -d jest @types/jest ts-jest
```

**Step 2: Create jest.config.js**
```javascript
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  testMatch: ['**/tests/**/*.test.ts'],
  collectCoverageFrom: ['src/**/*.ts'],
};
```

**Step 3: Verify jest works**
```bash
bun run jest
```

### Rust: cargo test Configuration

**Step 1: cargo test is built-in**

No installation needed. Cargo includes a test runner.

**Step 2: Create tests directory**
```bash
mkdir -p tests
```

**Step 3: Create integration test**

Create `tests/integration_test.rs`:
```rust
#[test]
fn sample_test() {
    assert!(true);
}

#[test]
fn addition_test() {
    assert_eq!(1 + 1, 2);
}
```

**Step 4: Add unit tests to modules**

In `src/lib.rs` or any module:
```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_function() {
        assert!(true);
    }
}
```

**Step 5: Verify cargo test works**
```bash
cargo test
```

### Go: go test Configuration

**Step 1: go test is built-in**

No installation needed. Go includes a test runner.

**Step 2: Create test file**

Create `sample_test.go` next to the code file:
```go
package main

import "testing"

func TestSample(t *testing.T) {
    if true != true {
        t.Error("Expected true to be true")
    }
}

func TestAddition(t *testing.T) {
    result := 1 + 1
    if result != 2 {
        t.Errorf("Expected 2, got %d", result)
    }
}
```

**Step 3: Verify go test works**
```bash
go test ./...
```

### .NET: dotnet test Configuration

**Step 1: Add test project**
```bash
dotnet new xunit -o tests
dotnet sln add tests/tests.csproj
dotnet add tests/tests.csproj reference src/MyProject.csproj
```

**Step 2: Create sample test**

Create `tests/SampleTests.cs`:
```csharp
using Xunit;

public class SampleTests
{
    [Fact]
    public void SampleTest()
    {
        Assert.True(true);
    }

    [Fact]
    public void AdditionTest()
    {
        Assert.Equal(2, 1 + 1);
    }
}
```

**Step 3: Verify dotnet test works**
```bash
dotnet test
```

### C/C++: gtest Configuration

**Step 1: Install Google Test**
```bash
# macOS
brew install googletest

# Linux
sudo apt install libgtest-dev
```

**Step 2: Add to CMakeLists.txt**
```cmake
enable_testing()
find_package(GTest REQUIRED)

add_executable(tests tests/sample_test.cpp)
target_link_libraries(tests GTest::gtest GTest::gtest_main)
add_test(NAME SampleTests COMMAND tests)
```

**Step 3: Create test file**

Create `tests/sample_test.cpp`:
```cpp
#include <gtest/gtest.h>

TEST(SampleTest, BasicAssertion) {
    EXPECT_TRUE(true);
}

TEST(SampleTest, Addition) {
    EXPECT_EQ(1 + 1, 2);
}
```

**Step 4: Build and run tests**
```bash
cd build && cmake .. && make && ctest
```

### Swift: XCTest Configuration

**Step 1: Create test target**

For Swift Package Manager projects, tests go in `Tests/` directory.

**Step 2: Create test file**

Create `Tests/MyProjectTests/SampleTests.swift`:
```swift
import XCTest
@testable import MyProject

final class SampleTests: XCTestCase {
    func testSample() {
        XCTAssertTrue(true)
    }

    func testAddition() {
        XCTAssertEqual(1 + 1, 2)
    }
}
```

**Step 3: Verify swift test works**
```bash
swift test
```

## Checklist

- [ ] Testing framework installed as dev dependency
- [ ] Configuration file created with appropriate settings
- [ ] Tests directory structure created
- [ ] Sample test file created and passing
- [ ] Test command verified and working
- [ ] Coverage reporting configured (optional)
- [ ] Test scripts added to package.json or equivalent

## Examples

### Example 1: Python pytest Setup

```bash
# Install
uv add --dev pytest pytest-cov
# Output: Added pytest, pytest-cov to dev dependencies

# Create structure
mkdir -p tests/unit tests/integration

# Run tests
uv run pytest tests/ -v
# Output:
# ======================== test session starts =========================
# collected 2 items
#
# tests/unit/test_sample.py::test_sample_passes PASSED   [50%]
# tests/unit/test_sample.py::test_addition PASSED        [100%]
#
# ========================= 2 passed in 0.02s ==========================
```

### Example 2: TypeScript vitest Setup

```bash
# Install
bun add -d vitest

# Create config (vitest.config.ts as shown above)

# Run tests
bun run test
# Output:
#  DEV  v1.x.x
#
#  ✓ tests/sample.test.ts (2)
#    ✓ Sample (2)
#      ✓ should pass
#      ✓ should add numbers
#
#  Test Files  1 passed (1)
#       Tests  2 passed (2)
```

### Example 3: Rust cargo test Setup

```bash
# Run tests (no install needed)
cargo test
# Output:
# running 2 tests
# test tests::test_function ... ok
# test integration_test::sample_test ... ok
#
# test result: ok. 2 passed; 0 failed
```

## Error Handling

### Tests Not Found

**Symptom**: Test runner reports no tests found.

**Action**:
1. Verify test file naming conventions match configuration
2. Check testpaths or include patterns in configuration
3. Ensure test functions follow naming conventions (test_*, Test*)

### Import Errors in Tests

**Symptom**: Tests fail with import or module not found errors.

**Action**:
1. Ensure the package is installed in editable/development mode
2. Check that `__init__.py` files exist in Python packages
3. Verify tsconfig paths configuration for TypeScript
4. Add the source directory to the test configuration

### Tests Hang or Timeout

**Symptom**: Tests never complete or timeout.

**Action**:
1. Check for infinite loops or blocking calls in test code
2. Add timeout configuration to test runner
3. Use async test mode for async code
4. Check for missing mocks that make real network calls

### Coverage Not Working

**Symptom**: Coverage reports show 0% or fail to generate.

**Action**:
1. Verify coverage tool is installed
2. Check source path configuration in coverage settings
3. Ensure tests actually exercise the source code
4. Check for coverage ignore patterns that may be too broad
