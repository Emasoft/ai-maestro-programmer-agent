---
name: ruff-configuration-patterns
description: Reference patterns for Ruff linter and formatter configuration
parent-skill: ampa-project-setup
---

# Ruff Configuration Patterns

> **Token rule**: Write all command output to a report file. Return only a 2-3 line summary + file path to the caller.

## Contents
- When to configure ruff for a new project
- Standard ruff.toml template for AI Maestro Programmer projects
- What each rule set does and why it is enabled
- What each ignored rule means and why it is ignored
- Per-file ignore patterns and when to use them
- Formatter settings (quote style, indent, line endings)
- How to run ruff check and ruff format
- Customizing ruff for specific project types

---

## When to Configure Ruff for a New Project

Configure ruff when setting up any new Python project. Ruff replaces multiple tools:
- **pycodestyle** (E, W rules) -- style checking
- **Pyflakes** (F rules) -- logical error detection
- **isort** (I rules) -- import sorting
- **flake8-bugbear** (B rules) -- bug-prone pattern detection
- **flake8-comprehensions** (C4 rules) -- comprehension optimization
- **pyupgrade** (UP rules) -- Python version upgrade suggestions

Create a `ruff.toml` file in the project root directory.

---

## Standard ruff.toml Template for AI Maestro Programmer Projects

```toml
# Ruff configuration for AI Maestro Programmer projects

[lint]
# Enable common rule sets
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # Pyflakes
    "I",      # isort
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "UP",     # pyupgrade
]

ignore = [
    "E501",   # line too long (handled by formatter)
    "B008",   # function call in default argument
    "B904",   # raise from err
    "B905",   # zip without strict parameter
    "C401",   # unnecessary generator
    "C416",   # unnecessary list comprehension
    "E402",   # module level import not at top of file
    "F841",   # local variable assigned but never used
    "W293",   # blank line contains whitespace
    "B007",   # loop control variable not used
]

[lint.per-file-ignores]
"__init__.py" = ["F401"]  # unused imports in __init__.py
"tests/*" = ["B011"]      # assert false in tests
"test_*.py" = ["F401"]    # unused imports in test files

[format]
quote-style = "double"
indent-style = "space"
line-ending = "auto"
```

---

## What Each Rule Set Does

| Rule Set | Code | Purpose | Example Catch |
|----------|------|---------|---------------|
| pycodestyle errors | `E` | PEP 8 style violations | Missing whitespace, wrong indentation |
| pycodestyle warnings | `W` | PEP 8 style warnings | Trailing whitespace, blank lines |
| Pyflakes | `F` | Logical errors | Undefined names, unused imports |
| isort | `I` | Import order | Unsorted imports, missing sections |
| flake8-bugbear | `B` | Bug-prone patterns | Mutable default arguments, bare except |
| flake8-comprehensions | `C4` | Comprehension style | Unnecessary list() around generator |
| pyupgrade | `UP` | Version upgrades | Old-style string formatting, type hints |

### pycodestyle errors (E)

These rules enforce PEP 8 style conventions. They catch formatting issues like missing whitespace around operators, incorrect indentation levels, and missing blank lines between functions or classes. Example: `E111` catches indentation that is not a multiple of four spaces.

### pycodestyle warnings (W)

These are less severe PEP 8 style issues. They catch trailing whitespace on lines, deprecated features, and minor formatting inconsistencies. Example: `W291` catches trailing whitespace at the end of a line.

### Pyflakes (F)

Pyflakes detects logical errors without checking style. It finds undefined variable names, imported modules that are never used, redefined unused variables, and other programming mistakes. Example: `F821` catches usage of an undefined name.

### isort (I)

The isort rules enforce a consistent import ordering. Python imports are sorted into sections: standard library, third-party packages, and local imports. Each section is separated by a blank line. Example: `I001` catches unsorted imports within a section.

### flake8-bugbear (B)

Bugbear catches common programming mistakes and design problems that are not syntax errors but lead to bugs. It detects mutable default arguments, bare `except:` clauses, and other dangerous patterns. Example: `B006` catches using a mutable data structure as a default argument value.

### flake8-comprehensions (C4)

These rules suggest simpler comprehension or generator expressions. They catch cases where code uses unnecessary `list()`, `set()`, or `dict()` calls around generators when a comprehension would be clearer and faster. Example: `C400` catches `list(x for x in items)` which should be `[x for x in items]`.

### pyupgrade (UP)

Pyupgrade suggests modern Python syntax. It catches old-style string formatting (`%`-style or `.format()`), outdated type annotations, and other patterns that have been superseded by newer Python features. Example: `UP031` catches `"%s" % name` which should be an f-string.

---

## What Each Ignored Rule Means

| Rule | Name | Why Ignored |
|------|------|-------------|
| `E501` | Line too long | The ruff formatter handles line length automatically. When you run `ruff format`, it wraps lines to the configured length, making this lint check redundant. |
| `B008` | Function call in default argument | Common pattern in FastAPI and Click. For example, `def endpoint(db: Session = Depends(get_db))` uses a function call as a default argument. This is intentional in dependency injection frameworks. |
| `B904` | Raise from err | This rule requires `raise NewException() from original_exception` syntax to preserve exception chains. Ignored because many existing codebases have too many violations to fix at once. |
| `B905` | zip without strict parameter | This rule requires `zip(..., strict=True)` to catch mismatched lengths. Ignored because the `strict` parameter is only available in Python 3.10 and later, and many projects support older Python versions. |
| `C401` | Unnecessary generator | This rule flags `set(x for x in items)` suggesting `{x for x in items}`. Ignored because sometimes the generator form is clearer, especially in complex expressions. |
| `C416` | Unnecessary list comprehension | This rule flags `[x for x in items]` as unnecessary when `list(items)` would work. Ignored because the comprehension form can be clearer when reading code, and sometimes serves as documentation of intent. |
| `E402` | Module-level import not at top of file | Some scripts need to modify `sys.path` or set environment variables before importing modules. For example, a script might need `sys.path.insert(0, "/custom/path")` before importing a local module. |
| `F841` | Local variable assigned but never used | Sometimes a variable is assigned for debugging purposes, or to document the return value of a function call even when only the side effect matters. Ignored to reduce noise during development. |
| `W293` | Blank line contains whitespace | The ruff formatter automatically strips whitespace from blank lines. This check is redundant when the formatter is used. |
| `B007` | Loop control variable not used | This rule flags `for x in range(n)` when `x` is never used in the loop body. The convention is to use `for _ in range(n)` instead. Ignored because many developers use named variables for clarity even when unused. |

---

## Per-File Ignore Patterns

| Pattern | Rule | Reason |
|---------|------|--------|
| `__init__.py` | `F401` (unused imports) | `__init__.py` files re-export symbols to define a package's public API. The imports exist to make symbols available when someone imports the package, not because the `__init__.py` itself uses them. |
| `tests/*` | `B011` (assert false) | Test files use `assert False` to mark test cases that should never reach a certain point. For example, `assert False, "This line should not be reached"` is a valid test pattern. |
| `test_*.py` | `F401` (unused imports) | Test files import fixtures and test helpers that are used by the test framework (like pytest fixtures) but appear unused to static analysis. |

### Adding Custom Per-File Ignores

Add new per-file ignores in the `[lint.per-file-ignores]` section of `ruff.toml`. The key is a file pattern (glob syntax), and the value is a list of rule codes to ignore for files matching that pattern.

```toml
[lint.per-file-ignores]
"__init__.py" = ["F401"]       # unchanged: unused imports in __init__.py
"tests/*" = ["B011"]           # unchanged: assert false in tests
"test_*.py" = ["F401"]         # unchanged: unused imports in test files
"scripts/*" = ["E402"]         # added: scripts may modify sys.path before imports
"migrations/*" = ["E501"]      # added: auto-generated migrations may have long lines
"conftest.py" = ["F401"]       # added: conftest.py defines fixtures used by other files
```

---

## Formatter Settings

| Setting | Value | Meaning |
|---------|-------|---------|
| `quote-style` | `"double"` | Use double quotes for strings. Write `"hello"` not `'hello'`. Ruff formatter automatically converts single quotes to double quotes. |
| `indent-style` | `"space"` | Use spaces for indentation, not tabs. Standard Python convention is 4 spaces per indentation level. |
| `line-ending` | `"auto"` | Detect line endings automatically. Uses LF (`\n`) on Unix/macOS systems and CRLF (`\r\n`) on Windows. This prevents line ending conflicts in cross-platform teams. |

**Note**: Line length is NOT configured in ruff.toml for AI Maestro Programmer projects. The line length is set to 88 characters and must be passed as a command-line flag:

```bash
uv run ruff format --line-length=88 src/ tests/
```

The reason for using command-line flags instead of configuration: the project CLAUDE.md enforces `--line-length=88` and this ensures the setting is always explicit and visible in every command invocation.

---

## How to Run Ruff

### Linting (check for issues)

To check all Python files for lint issues:

```bash
# Check all Python files in src/ and tests/
uv run ruff check src/ tests/
```

To automatically fix issues that ruff can safely fix (like import sorting, unnecessary parentheses):

```bash
# Auto-fix safe issues
uv run ruff check --fix src/ tests/
```

To see what would change without actually changing any files:

```bash
# Show all fixable issues as a diff without modifying files
uv run ruff check --diff src/ tests/
```

### Formatting

To format all Python files with the standard line length of 88 characters:

```bash
# Format with standard line length
uv run ruff format --line-length=88 src/ tests/
```

To check if files are already formatted correctly without changing them:

```bash
# Check formatting without changing files (exits with error if unformatted)
uv run ruff format --check --line-length=88 src/ tests/
```

### Combined Workflow

Run linting first to fix issues, then format. This order matters because some lint fixes may affect formatting:

```bash
# Fix lint issues first, then format
uv run ruff check --fix src/ tests/ && uv run ruff format --line-length=88 src/ tests/
```

### Checking a Single File

To check or format a single file instead of a directory:

```bash
# Lint a single file
uv run ruff check src/mymodule.py

# Format a single file
uv run ruff format --line-length=88 src/mymodule.py
```

---

## Customizing Ruff for Specific Project Types

### FastAPI Projects

FastAPI uses function calls in default arguments extensively for dependency injection. The `B008` rule is already ignored in the standard template, which covers patterns like:

```python
@app.get("/items")
def read_items(db: Session = Depends(get_db), skip: int = Query(0)):
    ...
```

No additional configuration needed for FastAPI projects.

### CLI Tools (Click or Typer)

Click and Typer use function calls in decorator defaults, similar to FastAPI. The `B008` ignore already covers this. No additional configuration needed.

### Data Science Projects

Data science code often uses single-letter variable names from mathematical conventions (like `l` for length, `O` for big-O, `I` for identity matrix). Add `E741` to the ignore list:

```toml
ignore = [
    # ... all existing ignores from the standard template ...
    "E741",   # ambiguous variable name (common in math: l, O, I)
]
```

### Library Projects with Public API

Library projects may need additional `__init__.py` flexibility. The standard template already ignores `F401` in `__init__.py` files. If you also have `__all__` definitions, no additional configuration is needed.

### Strict Configuration

For projects that want maximum strictness, remove the ignore rules you want to enforce. At minimum, always keep `E501` ignored because the formatter handles line length:

```toml
ignore = [
    "E501",   # Keep: formatter handles this
]
```

This enables all other rules that the standard template ignores, requiring:
- Exception chaining with `raise ... from ...`
- `strict=True` on all `zip()` calls
- Set comprehensions instead of `set()` with generators
- `_` prefix for unused loop variables
- All imports at the top of every file
