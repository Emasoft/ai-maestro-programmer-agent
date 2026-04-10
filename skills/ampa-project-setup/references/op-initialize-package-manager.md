---
name: op-initialize-package-manager
description: Initialize the package manager for the project
parent-skill: ampa-project-setup
---

# Initialize Package Manager

## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
- [Examples](#examples)
- [Error Handling](#error-handling)

> **Token rule**: Write all command output to a report file. Return only a 2-3
> line summary + file path to the caller.

This operation sets up the package manager for the project based on the detected
programming language.

## When to Use

Use this operation when:

- Starting work on a project without a package manager configured
- The project has a configuration file but no lock file
- Creating a new project from scratch
- The package manager needs to be re-initialized after corruption

Do NOT use when:

- Package manager is already initialized (lock file exists)
- Working in a read-only environment
- The project explicitly forbids package manager changes

## Prerequisites

Before executing this operation:

1. Project language has been detected (see op-detect-project-language.md)
2. The package manager executable is installed on the system
3. You have write access to the project directory

## Procedure

### Python: uv Initialization

uv is the preferred Python package manager for this workflow.

**Step 1: Check if uv is installed**

```bash
uv --version
```

If not installed, install uv:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Step 2: Initialize Python project**

For a new project:

```bash
# Create virtual environment with Python 3.12
uv venv --python 3.12

# Activate the virtual environment
source .venv/bin/activate
# Windows: .venv\Scripts\activate.bat (cmd) or .venv\Scripts\Activate.ps1 (PowerShell)

# Initialize as uv-managed project
uv init --python 3.12
```

For an existing project with pyproject.toml:

```bash
# Create virtual environment
uv venv --python 3.12

# Activate
source .venv/bin/activate
# Windows: .venv\Scripts\activate.bat (cmd) or .venv\Scripts\Activate.ps1 (PowerShell)

# Sync dependencies
uv sync
```

**Step 3: Verify initialization**

```bash
# Check virtual environment exists
test -d .venv && echo "Virtual environment created"

# Check uv.lock exists (after sync)
test -f uv.lock && echo "Lock file created"
```

### JavaScript/TypeScript: bun or pnpm Initialization

bun is preferred. Fall back to pnpm if bun is unavailable.

**Step 1: Check if bun is installed**

```bash
bun --version
```

If not installed, check for pnpm:

```bash
pnpm --version
```

**Step 2: Initialize with bun**

For a new project:

```bash
bun init
```

For an existing project with package.json:

```bash
bun install
```

**Step 3: Initialize with pnpm (fallback)**

For a new project:

```bash
pnpm init
```

For an existing project:

```bash
pnpm install
```

**Step 4: Verify initialization**

```bash
# For bun
test -f bun.lockb && echo "Bun lock file created"

# For pnpm
test -f pnpm-lock.yaml && echo "pnpm lock file created"
```

### Rust: cargo Initialization

**Step 1: Check if cargo is installed**

```bash
cargo --version
```

**Step 2: Initialize Rust project**

For a new project:

```bash
cargo init
```

For an existing project with Cargo.toml:

```bash
cargo fetch
```

**Step 3: Verify initialization**

```bash
test -f Cargo.lock && echo "Cargo lock file created"
```

### Go: go mod Initialization

**Step 1: Check if go is installed**

```bash
go version
```

**Step 2: Initialize Go module**

For a new project:

```bash
go mod init <module-name>
```

For an existing project with go.mod:

```bash
go mod download
```

**Step 3: Verify initialization**

```bash
test -f go.sum && echo "Go sum file created"
```

### .NET: dotnet Initialization

**Step 1: Check if dotnet is installed**

```bash
dotnet --version
```

**Step 2: Initialize .NET project**

For a new project:

```bash
dotnet new console  # or webapi, classlib, etc.
```

For an existing project:

```bash
dotnet restore
```

**Step 3: Verify initialization**

```bash
test -d obj && echo ".NET obj directory created"
```

### C/C++: cmake or make Initialization

**Step 1: Check build system**

```bash
# Check for CMake
cmake --version

# Check for make
make --version
```

**Step 2: Initialize build directory**

For CMake projects:

```bash
mkdir -p build
cd build
cmake ..
```

For Makefile projects:

```bash
# No initialization needed, just verify Makefile exists
test -f Makefile && echo "Makefile found"
```

### Swift: swift or xcodebuild Initialization

**Step 1: Check Swift toolchain**

```bash
swift --version
```

**Step 2: Initialize Swift project**

For Swift Package Manager projects:

```bash
swift package init --type executable  # or library
```

For existing projects:

```bash
swift package resolve
```

**Step 3: Verify initialization**

```bash
test -f Package.resolved && echo "Swift package resolved"
```

## Checklist

- [ ] Package manager executable verified as installed
- [ ] Project directory verified as writable
- [ ] Package manager initialization command executed
- [ ] Lock file or equivalent created and verified
- [ ] Virtual environment activated (Python only)
- [ ] Initialization success confirmed

## Examples

### Example 1: Python Project with uv

```bash
# Navigate to project
cd /path/to/python-project

# Check uv
uv --version
# Output: uv 0.5.x

# Create venv
uv venv --python 3.12
# Output: Creating virtual environment at: .venv

# Activate
source .venv/bin/activate
# Windows: .venv\Scripts\activate.bat (cmd) or .venv\Scripts\Activate.ps1 (PowerShell)

# Initialize
uv init --python 3.12
# Output: Initialized project `python-project`

# Verify
ls -la .venv uv.lock pyproject.toml
```

### Example 2: TypeScript Project with bun

```bash
# Navigate to project
cd /path/to/ts-project

# Check bun
bun --version
# Output: 1.x.x

# Install dependencies
bun install
# Output: Packages installed

# Verify
ls bun.lockb node_modules
```

### Example 3: Rust Project with cargo

```bash
# Navigate to project
cd /path/to/rust-project

# Fetch dependencies
cargo fetch
# Output: Downloading crates ...

# Verify
test -f Cargo.lock && echo "OK"
```

## Error Handling

### Package Manager Not Installed

**Symptom**: Command returns "command not found" or similar.

**Action**:

1. Install the package manager using the installation commands provided above
2. Verify PATH includes the package manager location
3. Restart the shell if needed

### Permission Denied

**Symptom**: Cannot create files or directories in the project.

**Action**:

1. Check file permissions: `ls -la`
2. Check if running in a read-only filesystem
3. Request write access or work in a different directory

### Lock File Conflicts

**Symptom**: Package manager refuses to create lock file due to existing
conflicts.

**Action**:

1. Back up existing lock file
2. Delete the conflicting lock file
3. Re-run initialization
4. If issues persist, check for version conflicts in configuration

### Virtual Environment Activation Fails (Python)

**Symptom**: `source .venv/bin/activate` fails or has no effect.

**Action**:

1. Verify .venv directory exists: `ls -la .venv`
2. Check the shell type (bash, zsh, fish) and use appropriate activation script
3. Recreate the virtual environment if corrupted
