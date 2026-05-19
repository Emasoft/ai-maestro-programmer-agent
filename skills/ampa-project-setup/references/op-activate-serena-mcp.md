---
name: op-activate-serena-mcp
description: Activate SERENA MCP for code navigation
parent-skill: ampa-project-setup
---

# Activate SERENA MCP

## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
- [Examples](#examples)
- [Error Handling](#error-handling)

> **Token rule**: Write all command output to a report file. Return only a 2-3
> line summary + file path to the caller.

This operation activates the SERENA MCP (Model Context Protocol) server to
enable advanced code navigation and semantic analysis capabilities.

## When to Use

Use this operation when:

- Starting work on a project that benefits from code navigation
- You need to search for symbols, functions, or classes
- You need to understand code relationships and dependencies
- The project is large enough that manual navigation is inefficient

Do NOT use when:

- SERENA is already activated and responding
- The project is trivially small (a few files)
- SERENA MCP is not available in the environment

## Prerequisites

Before executing this operation:

1. Project setup is complete (language detected, dependencies installed)
2. SERENA MCP server is available and configured
3. The project contains source code that SERENA can index

## Procedure

### Step 1: Verify SERENA Availability

Check if SERENA MCP tools are available:

The following SERENA tools should be accessible (names use the canonical
plugin-prefixed form; if SERENA is installed as a non-plugin MCP server the
prefix is `mcp__<server-name>__` instead of `mcp__plugin_serena_serena__`):

- `mcp__plugin_serena_serena__find_symbol` - Find symbol definitions
- `mcp__plugin_serena_serena__find_referencing_symbols` - Find symbol references
- `mcp__plugin_serena_serena__get_symbols_overview` - Get file/folder symbol overview
- `mcp__plugin_serena_serena__search_for_pattern` - Search code patterns

### Step 2: Activate SERENA for the Project

SERENA operates on a per-project basis. Activate it by opening the project:

```text
Use the SERENA activate_project tool with the project root path
(mcp__plugin_serena_serena__activate_project when SERENA is installed
as the canonical `serena` plugin).
```

The project root is typically the directory containing:

- `pyproject.toml` (Python)
- `package.json` (JavaScript/TypeScript)
- `Cargo.toml` (Rust)
- `go.mod` (Go)
- The main source directory

### Step 3: Verify SERENA Connection

Test SERENA by performing a simple search:

1. Search for a known symbol in the project:

```text
Use mcp__plugin_serena_serena__find_symbol with a known function or class name
```

2. Get the symbol overview of a known file:

```text
Use mcp__plugin_serena_serena__get_symbols_overview with a known source file path
```

### Step 4: Index the Project (if needed)

For large projects, SERENA may need to build an index:

1. SERENA typically indexes automatically on first use
2. For large codebases, this may take several seconds
3. Subsequent queries will be faster after indexing

### Step 5: Verify Tool Availability

Confirm all SERENA tools are responding:

| Tool                       | Purpose            | Test Query                       |
| -------------------------- | ------------------ | -------------------------------- |
| `find_symbol`              | Locate definitions | Search for `main` or entry point |
| `find_referencing_symbols` | Find usages        | Search for a common function     |
| `get_symbols_overview`     | Show file outline  | Query a known source file        |
| `search_for_pattern`       | Pattern search     | Search for a unique string       |

## SERENA Tool Reference

### find_symbol

Finds where a symbol (function, class, variable) is defined.

**Use when**: You know a symbol name and need to find its definition.

**Example**: Find where `process_data` function is defined.

### find_referencing_symbols

Finds all locations where a symbol is used.

**Use when**: You need to understand how a function/class is used throughout the
codebase.

**Example**: Find all calls to `validate_input` function.

### get_symbols_overview

Returns the top-level symbols (functions, classes, methods) of a file or folder.

**Use when**: You need an overview of what a file contains without reading the
whole file.

**Example**: Get the symbol overview of `src/main.py` to see available functions.

### search_for_pattern

Searches for code patterns using regex or literal strings.

**Use when**: You need to find specific code patterns or text.

**Example**: Search for all TODO comments or specific error messages.

## Checklist

- [ ] SERENA MCP tools verified as available
- [ ] Project opened/activated in SERENA
- [ ] Test symbol search completed successfully
- [ ] Test file structure query completed successfully
- [ ] Index built for large projects (if applicable)
- [ ] All required SERENA tools responding

## Examples

### Example 1: Activating SERENA for Python Project

```text
1. Activate project:
   mcp__plugin_serena_serena__activate_project project="/path/to/python-project"

2. Verify with symbol search:
   mcp__plugin_serena_serena__find_symbol name_path="main"
   Result: Found in src/main.py at line 15

3. Get symbol overview:
   mcp__plugin_serena_serena__get_symbols_overview relative_path="src/main.py"
   Result:
   - function: main (line 15)
   - function: setup (line 5)
   - class: Application (line 25)
```

### Example 2: Activating SERENA for TypeScript Project

```text
1. Activate project:
   mcp__plugin_serena_serena__activate_project project="/path/to/ts-project"

2. Verify with symbol search:
   mcp__plugin_serena_serena__find_symbol name_path="App"
   Result: Found in src/App.tsx at line 10

3. Find referencing symbols:
   mcp__plugin_serena_serena__find_referencing_symbols name_path="handleClick" relative_path="src/components/Button.tsx"
   Result:
   - src/components/Form.tsx:42 (usage)
   - src/App.tsx:28 (usage)
```

### Example 3: Large Project Indexing

```text
1. Activate large project:
   mcp__plugin_serena_serena__activate_project project="/path/to/large-project"
   Note: Initial indexing may take 5-10 seconds

2. First search (may be slow):
   mcp__plugin_serena_serena__search_for_pattern substring_pattern="TODO"
   Result: 47 matches found (indexing complete)

3. Subsequent searches (fast):
   mcp__plugin_serena_serena__search_for_pattern substring_pattern="FIXME"
   Result: 12 matches found (instant)
```

## Error Handling

### SERENA Not Available

**Symptom**: SERENA MCP tools are not recognized or unavailable.

**Action**:

1. Check if SERENA MCP is configured in the environment
2. Verify MCP server is running
3. Check Claude Code settings for MCP configuration
4. Contact system administrator if SERENA should be available

### Project Open Failed

**Symptom**: SERENA fails to open the project with an error.

**Action**:

1. Verify the project path is correct and accessible
2. Check that the project contains recognized source files
3. Ensure there are no permission issues on the project directory
4. Try with a subdirectory if the root directory is too large

### Symbol Not Found

**Symptom**: SERENA returns no results for a known symbol.

**Action**:

1. Verify the symbol name spelling and case
2. Check that the file containing the symbol is in the indexed directories
3. Try a broader search pattern
4. Verify the symbol is actually defined (not just imported)

### Slow Response Times

**Symptom**: SERENA queries take a long time to complete.

**Action**:

1. Wait for initial indexing to complete
2. For very large projects, allow more time for first queries
3. Use more specific search patterns to reduce result set
4. Check system resources (CPU, memory, disk I/O)

### Connection Lost

**Symptom**: SERENA stops responding mid-session.

**Action**:

1. Check if MCP server process is still running
2. Try reopening the project
3. Restart Claude Code if necessary
4. Check for error messages in MCP logs
