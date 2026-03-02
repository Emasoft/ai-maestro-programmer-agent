---
name: op-configure-linting
description: Configure linting tools for code quality checks.
parent-skill: ampa-project-setup
operation-number: 4
---

# Operation: Configure Linting


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Python: ruff and mypy Configuration](#python-ruff-and-mypy-configuration)
  - [JavaScript/TypeScript: eslint Configuration](#javascripttypescript-eslint-configuration)
  - [Rust: clippy Configuration](#rust-clippy-configuration)
  - [Go: golint and staticcheck Configuration](#go-golint-and-staticcheck-configuration)
  - [.NET: Built-in Analyzers](#net-built-in-analyzers)
  - [C/C++: clang-tidy Configuration](#cc-clang-tidy-configuration)
  - [Swift: swiftlint Configuration](#swift-swiftlint-configuration)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example 1: Python ruff + mypy Setup](#example-1-python-ruff-mypy-setup)
  - [Example 2: TypeScript eslint Setup](#example-2-typescript-eslint-setup)
  - [Example 3: Rust clippy Setup](#example-3-rust-clippy-setup)
- [Error Handling](#error-handling)
  - [Linter Not Found](#linter-not-found)
  - [Configuration Syntax Error](#configuration-syntax-error)
  - [Too Many Errors on Existing Code](#too-many-errors-on-existing-code)
  - [Type Checking Fails](#type-checking-fails)

This operation sets up linting tools appropriate for the project language to ensure code quality and consistency.

## When to Use

Use this operation when:
- Setting up a new project that needs linting
- Existing project lacks linting configuration
- Updating linting rules to match team standards
- Adding type checking to a project

Do NOT use when:
- Linting is already configured and working
- The project explicitly avoids linting tools
- Working in a read-only environment

## Prerequisites

Before executing this operation:
1. Dependencies have been installed (see op-install-dependencies.md)
2. You have write access to create configuration files
3. The package manager can install additional dev dependencies

## Procedure

### Python: ruff and mypy Configuration

**Step 1: Install linting tools**
```bash
source .venv/bin/activate
uv add --dev ruff mypy
```

**Step 2: Create ruff configuration**

Add to `pyproject.toml`:
```toml
[tool.ruff]
line-length = 88
target-version = "py312"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "UP",  # pyupgrade
]
ignore = []

[tool.ruff.lint.isort]
known-first-party = ["your_package_name"]
```

**Step 3: Create mypy configuration**

Add to `pyproject.toml`:
```toml
[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

**Step 4: Verify linting works**
```bash
# Run ruff
uv run ruff check .

# Run ruff format check
uv run ruff format --check .

# Run mypy
uv run mypy src/
```

### JavaScript/TypeScript: eslint Configuration

**Step 1: Install eslint**

With bun:
```bash
bun add -d eslint @eslint/js typescript-eslint
```

With pnpm:
```bash
pnpm add -D eslint @eslint/js typescript-eslint
```

**Step 2: Create eslint.config.js**

For TypeScript projects:
```javascript
import eslint from '@eslint/js';
import tseslint from 'typescript-eslint';

export default tseslint.config(
  eslint.configs.recommended,
  ...tseslint.configs.recommended,
  {
    rules: {
      '@typescript-eslint/no-unused-vars': 'error',
      '@typescript-eslint/no-explicit-any': 'warn',
    },
  },
);
```

For JavaScript projects:
```javascript
import eslint from '@eslint/js';

export default [
  eslint.configs.recommended,
  {
    rules: {
      'no-unused-vars': 'error',
      'no-console': 'warn',
    },
  },
];
```

**Step 3: Verify eslint works**
```bash
# With bun
bun run eslint .

# With pnpm
pnpm eslint .
```

### Rust: clippy Configuration

**Step 1: Clippy is included with Rust**

No installation needed. Clippy comes with rustup.

**Step 2: Configure clippy**

Add to `Cargo.toml`:
```toml
[lints.clippy]
pedantic = "warn"
nursery = "warn"
```

Or create `clippy.toml`:
```toml
cognitive-complexity-threshold = 25
```

**Step 3: Verify clippy works**
```bash
cargo clippy
```

### Go: golint and staticcheck Configuration

**Step 1: Install linters**
```bash
go install golang.org/x/lint/golint@latest
go install honnef.co/go/tools/cmd/staticcheck@latest
```

**Step 2: Configure staticcheck**

Create `.staticcheck.conf`:
```
checks = ["all", "-ST1000"]
```

**Step 3: Verify linting works**
```bash
golint ./...
staticcheck ./...
```

### .NET: Built-in Analyzers

**Step 1: Enable analyzers in project file**

Add to `.csproj`:
```xml
<PropertyGroup>
  <EnableNETAnalyzers>true</EnableNETAnalyzers>
  <AnalysisLevel>latest</AnalysisLevel>
  <TreatWarningsAsErrors>true</TreatWarningsAsErrors>
</PropertyGroup>
```

**Step 2: Verify analysis works**
```bash
dotnet build
```

### C/C++: clang-tidy Configuration

**Step 1: Check clang-tidy is installed**
```bash
clang-tidy --version
```

**Step 2: Create .clang-tidy**
```yaml
Checks: >
  -*,
  clang-analyzer-*,
  bugprone-*,
  modernize-*,
  performance-*,
  readability-*
WarningsAsErrors: ''
HeaderFilterRegex: '.*'
```

**Step 3: Verify clang-tidy works**
```bash
clang-tidy src/*.cpp
```

### Swift: swiftlint Configuration

**Step 1: Install swiftlint**
```bash
brew install swiftlint
```

**Step 2: Create .swiftlint.yml**
```yaml
disabled_rules:
  - trailing_whitespace
opt_in_rules:
  - empty_count
  - closure_spacing
line_length: 120
```

**Step 3: Verify swiftlint works**
```bash
swiftlint
```

## Checklist

- [ ] Linting tool installed as dev dependency
- [ ] Configuration file created with appropriate rules
- [ ] Type checking configured (if applicable)
- [ ] Linting command tested and working
- [ ] No blocking errors on existing code (or errors documented)
- [ ] Format checking configured (if applicable)

## Examples

### Example 1: Python ruff + mypy Setup

```bash
# Install
uv add --dev ruff mypy
# Output: Added ruff, mypy to dev dependencies

# Test ruff
uv run ruff check src/
# Output: All checks passed!

# Test mypy
uv run mypy src/
# Output: Success: no issues found

# Format check
uv run ruff format --check src/
# Output: 3 files would be reformatted

# Fix formatting
uv run ruff format src/
# Output: 3 files reformatted
```

### Example 2: TypeScript eslint Setup

```bash
# Install
bun add -d eslint @eslint/js typescript-eslint

# Create config (eslint.config.js as shown above)

# Test
bun run eslint src/
# Output:
# /src/index.ts
#   5:1  error  'unused' is defined but never used
#
# 1 problem (1 error, 0 warnings)
```

### Example 3: Rust clippy Setup

```bash
# No install needed

# Run clippy
cargo clippy
# Output:
# warning: unnecessary `return` statement
#   --> src/main.rs:10:5
#    |
# 10 |     return result;
#    |     ^^^^^^^^^^^^^^ help: remove `return`
#
# warning: 1 warning generated
```

## Error Handling

### Linter Not Found

**Symptom**: Command not found when running linter.

**Action**:
1. Verify the linter is installed: check dev dependencies
2. For Go/Rust tools, ensure they are in PATH
3. Reinstall the linter package

### Configuration Syntax Error

**Symptom**: Linter fails to parse configuration file.

**Action**:
1. Validate the configuration file syntax
2. Check for typos in rule names
3. Ensure the config format matches the linter version

### Too Many Errors on Existing Code

**Symptom**: Linter reports hundreds of errors on existing codebase.

**Action**:
1. Start with fewer/less strict rules
2. Use ignore comments for legacy code
3. Fix errors incrementally
4. Consider using baseline files to ignore existing issues

### Type Checking Fails

**Symptom**: mypy or TypeScript compiler reports many type errors.

**Action**:
1. Start with lenient settings and gradually increase strictness
2. Add type annotations incrementally
3. Use `# type: ignore` or `// @ts-ignore` for complex legacy code
4. Configure which directories to check
