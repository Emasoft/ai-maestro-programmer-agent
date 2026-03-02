---
name: op-activate-serena-mcp
description: Activate SERENA MCP for code navigation and semantic analysis.
parent-skill: ampa-project-setup
operation-number: 6
---

# Operation: Activate SERENA MCP


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Verify SERENA Availability](#step-1-verify-serena-availability)
  - [Step 2: Activate SERENA for the Project](#step-2-activate-serena-for-the-project)
  - [Step 3: Verify SERENA Connection](#step-3-verify-serena-connection)
  - [Step 4: Index the Project (if needed)](#step-4-index-the-project-if-needed)
  - [Step 5: Verify Tool Availability](#step-5-verify-tool-availability)
- [SERENA Tool Reference](#serena-tool-reference)
  - [find_symbol](#find_symbol)
  - [find_references](#find_references)
  - [get_file_structure](#get_file_structure)
  - [search_code](#search_code)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example 1: Activating SERENA for Python Project](#example-1-activating-serena-for-python-project)
  - [Example 2: Activating SERENA for TypeScript Project](#example-2-activating-serena-for-typescript-project)
  - [Example 3: Large Project Indexing](#example-3-large-project-indexing)
- [Error Handling](#error-handling)
  - [SERENA Not Available](#serena-not-available)
  - [Project Open Failed](#project-open-failed)
  - [Symbol Not Found](#symbol-not-found)
  - [Slow Response Times](#slow-response-times)
  - [Connection Lost](#connection-lost)

This operation activates the SERENA MCP (Model Context Protocol) server to enable advanced code navigation and semantic analysis capabilities.

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

The following SERENA tools should be accessible:
- `mcp__serena__find_symbol` - Find symbol definitions
- `mcp__serena__find_references` - Find symbol references
- `mcp__serena__get_file_structure` - Get file structure
- `mcp__serena__search_code` - Search code patterns

### Step 2: Activate SERENA for the Project

SERENA operates on a per-project basis. Activate it by opening the project:

```
Use the SERENA open_project tool with the project root path
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
```
Use mcp__serena__find_symbol with a known function or class name
```

2. Get the structure of a known file:
```
Use mcp__serena__get_file_structure with a known source file path
```

### Step 4: Index the Project (if needed)

For large projects, SERENA may need to build an index:

1. SERENA typically indexes automatically on first use
2. For large codebases, this may take several seconds
3. Subsequent queries will be faster after indexing

### Step 5: Verify Tool Availability

Confirm all SERENA tools are responding:

| Tool | Purpose | Test Query |
|------|---------|------------|
| `find_symbol` | Locate definitions | Search for `main` or entry point |
| `find_references` | Find usages | Search for a common function |
| `get_file_structure` | Show file outline | Query a known source file |
| `search_code` | Pattern search | Search for a unique string |

## SERENA Tool Reference

### find_symbol

Finds where a symbol (function, class, variable) is defined.

**Use when**: You know a symbol name and need to find its definition.

**Example**: Find where `process_data` function is defined.

### find_references

Finds all locations where a symbol is used.

**Use when**: You need to understand how a function/class is used throughout the codebase.

**Example**: Find all calls to `validate_input` function.

### get_file_structure

Returns the structure of a file (functions, classes, methods).

**Use when**: You need an overview of what a file contains without reading the whole file.

**Example**: Get structure of `src/main.py` to see available functions.

### search_code

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

```
1. Open project:
   mcp__serena__open_project path="/path/to/python-project"

2. Verify with symbol search:
   mcp__serena__find_symbol symbol="main"
   Result: Found in src/main.py at line 15

3. Get file structure:
   mcp__serena__get_file_structure path="src/main.py"
   Result:
   - function: main (line 15)
   - function: setup (line 5)
   - class: Application (line 25)
```

### Example 2: Activating SERENA for TypeScript Project

```
1. Open project:
   mcp__serena__open_project path="/path/to/ts-project"

2. Verify with symbol search:
   mcp__serena__find_symbol symbol="App"
   Result: Found in src/App.tsx at line 10

3. Find references:
   mcp__serena__find_references symbol="handleClick"
   Result:
   - src/components/Button.tsx:15 (definition)
   - src/components/Form.tsx:42 (usage)
   - src/App.tsx:28 (usage)
```

### Example 3: Large Project Indexing

```
1. Open large project:
   mcp__serena__open_project path="/path/to/large-project"
   Note: Initial indexing may take 5-10 seconds

2. First search (may be slow):
   mcp__serena__search_code pattern="TODO"
   Result: 47 matches found (indexing complete)

3. Subsequent searches (fast):
   mcp__serena__search_code pattern="FIXME"
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
