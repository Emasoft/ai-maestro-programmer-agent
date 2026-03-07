---
name: op-detect-project-language
description: Identify the programming language of a project from files and configuration.
parent-skill: ampa-project-setup
workflow-step: "Step 1"
---

# Operation: Detect Project Language

> **Token rule**: Write all command output to a report file. Return only a 2-3 line summary + file path to the caller.


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Step 1: Check for Configuration Files](#step-1-check-for-configuration-files)
  - [Step 2: Examine File Extensions](#step-2-examine-file-extensions)
  - [Step 3: Check for TypeScript vs JavaScript](#step-3-check-for-typescript-vs-javascript)
  - [Step 4: Handle Multi-Language Projects](#step-4-handle-multi-language-projects)
  - [Step 5: Confirm Detection](#step-5-confirm-detection)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example 1: Python Project Detection](#example-1-python-project-detection)
  - [Example 2: TypeScript Project Detection](#example-2-typescript-project-detection)
  - [Example 3: Multi-Language Project](#example-3-multi-language-project)
- [Error Handling](#error-handling)
  - [No Configuration Files Found](#no-configuration-files-found)
  - [Conflicting Indicators](#conflicting-indicators)
  - [Empty Project](#empty-project)

This operation identifies the primary programming language of a project by examining files, directory structure, and configuration files.

## When to Use

Use this operation when:
- Starting work on an unfamiliar project
- The project language is not explicitly stated
- You need to determine which toolchain to initialize
- Working with a project that may use multiple languages

Do NOT use when:
- The language is already known and confirmed
- The user has explicitly stated the project language

## Prerequisites

Before executing this operation:
1. Have read access to the project directory
2. Be able to list files and read file contents
3. Have the project root directory path

## Procedure

### Step 1: Check for Configuration Files

Look for language-specific configuration files at the project root. These are definitive indicators:

| File | Language |
|------|----------|
| `pyproject.toml`, `setup.py`, `requirements.txt` | Python |
| `package.json` | JavaScript/TypeScript |
| `Cargo.toml` | Rust |
| `go.mod` | Go |
| `*.csproj`, `*.sln` | .NET (C#/F#/VB) |
| `CMakeLists.txt`, `Makefile` | C/C++ |
| `*.xcodeproj`, `*.xcworkspace` | Swift/Objective-C |
| `Package.swift` | Swift |
| `Gemfile` | Ruby |
| `pom.xml`, `build.gradle` | Java |

**Command to check**:
```bash
ls -la | grep -E "(pyproject|package\.json|Cargo\.toml|go\.mod|\.csproj|CMakeLists|\.xcodeproj|Package\.swift)"
```

### Step 2: Examine File Extensions

If no configuration files are found, scan for source file extensions:

```bash
find . -type f -name "*.py" -o -name "*.js" -o -name "*.ts" -o -name "*.rs" -o -name "*.go" -o -name "*.cs" -o -name "*.cpp" -o -name "*.swift" -o -name "*.m" 2>/dev/null | head -20
```

Map extensions to languages:
| Extension | Language |
|-----------|----------|
| `.py` | Python |
| `.js`, `.mjs`, `.cjs` | JavaScript |
| `.ts`, `.tsx` | TypeScript |
| `.rs` | Rust |
| `.go` | Go |
| `.cs` | C# (.NET) |
| `.cpp`, `.cc`, `.cxx`, `.h`, `.hpp` | C++ |
| `.c` | C |
| `.swift` | Swift |
| `.m`, `.mm` | Objective-C |

### Step 3: Check for TypeScript vs JavaScript

If `package.json` exists, determine if TypeScript is used:

```bash
# Check for tsconfig.json
test -f tsconfig.json && echo "TypeScript"

# Check for TypeScript in devDependencies
grep -q "typescript" package.json && echo "TypeScript"
```

### Step 4: Handle Multi-Language Projects

Some projects use multiple languages. Identify the primary language by:
1. Check which language has the entry point (main function, index file)
2. Check which language has the most source files
3. Check the `package.json` or equivalent for the main field

```bash
# Count files per language
echo "Python: $(find . -name '*.py' | wc -l)"
echo "JavaScript: $(find . -name '*.js' | wc -l)"
echo "TypeScript: $(find . -name '*.ts' | wc -l)"
echo "Rust: $(find . -name '*.rs' | wc -l)"
echo "Go: $(find . -name '*.go' | wc -l)"
```

### Step 5: Confirm Detection

After detection, confirm by checking for a working entry point:

| Language | Entry Point Check |
|----------|-------------------|
| Python | `python -c "import <main_module>"` or check for `__main__.py` |
| JavaScript | Check `main` field in `package.json` |
| TypeScript | Check `main` field in `package.json` or `tsconfig.json` outDir |
| Rust | Check `src/main.rs` or `src/lib.rs` |
| Go | Check for `func main()` in `.go` files |

## Checklist

- [ ] Configuration files examined at project root
- [ ] Source file extensions scanned and counted
- [ ] TypeScript vs JavaScript distinction made (if applicable)
- [ ] Multi-language project assessment completed (if applicable)
- [ ] Primary language confirmed with entry point check
- [ ] Detection result recorded for next operations

## Examples

### Example 1: Python Project Detection

```
Project structure:
myproject/
  pyproject.toml
  src/
    mymodule/
      __init__.py
      main.py
  tests/
    test_main.py

Detection result: Python
Indicator: pyproject.toml at root
Confirmation: src/mymodule/__init__.py exists
```

### Example 2: TypeScript Project Detection

```
Project structure:
webapp/
  package.json
  tsconfig.json
  src/
    index.ts
    components/
      App.tsx

Detection result: TypeScript
Indicators: package.json + tsconfig.json
Confirmation: .ts and .tsx files present
```

### Example 3: Multi-Language Project

```
Project structure:
fullstack/
  backend/
    pyproject.toml
    src/
      api.py
  frontend/
    package.json
    tsconfig.json
    src/
      App.tsx

Detection result: Multi-language (Python backend, TypeScript frontend)
Primary: Depends on task context
Action: Setup both toolchains, primary based on current work area
```

## Error Handling

### No Configuration Files Found

**Symptom**: Project root contains no recognizable configuration files.

**Action**:
1. Check if you are in the correct directory
2. Check for source files to infer language
3. Ask the user to confirm the project language

### Conflicting Indicators

**Symptom**: Multiple configuration files for different languages exist.

**Action**:
1. Identify which is the primary project vs dependencies
2. Check for monorepo structure (multiple projects in subdirectories)
3. Ask the user which language to prioritize

### Empty Project

**Symptom**: No source files or configuration files found.

**Action**:
1. Confirm the project directory is correct
2. Ask the user what language they want to use
3. Proceed to initialize a new project from scratch
