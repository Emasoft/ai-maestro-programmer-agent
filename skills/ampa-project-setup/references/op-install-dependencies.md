---
name: op-install-dependencies
description: Install project dependencies using the initialized package manager.
parent-skill: ampa-project-setup
operation-number: 3
---

# Operation: Install Dependencies


## Contents

- [When to Use](#when-to-use)
- [Prerequisites](#prerequisites)
- [Procedure](#procedure)
  - [Python: uv Dependencies](#python-uv-dependencies)
  - [JavaScript/TypeScript: bun or pnpm Dependencies](#javascripttypescript-bun-or-pnpm-dependencies)
  - [Rust: cargo Dependencies](#rust-cargo-dependencies)
  - [Go: go mod Dependencies](#go-go-mod-dependencies)
  - [.NET: dotnet Dependencies](#net-dotnet-dependencies)
  - [C/C++: Manual or Package Manager](#cc-manual-or-package-manager)
  - [Swift: swift package Dependencies](#swift-swift-package-dependencies)
- [Checklist](#checklist)
- [Examples](#examples)
  - [Example 1: Python uv Install](#example-1-python-uv-install)
  - [Example 2: TypeScript bun Install](#example-2-typescript-bun-install)
  - [Example 3: Rust cargo Build](#example-3-rust-cargo-build)
- [Error Handling](#error-handling)
  - [Network Errors](#network-errors)
  - [Version Conflicts](#version-conflicts)
  - [Missing System Dependencies](#missing-system-dependencies)
  - [Disk Space Issues](#disk-space-issues)
  - [Authentication Required](#authentication-required)

This operation installs all project dependencies using the package manager that was initialized in the previous operation.

## When to Use

Use this operation when:
- Package manager has been initialized but dependencies not installed
- Dependencies need to be refreshed after configuration changes
- New dependencies have been added to the project
- Lock file needs to be regenerated

Do NOT use when:
- Dependencies are already installed and up to date
- Working in an offline environment without cached packages
- The project has no dependencies defined

## Prerequisites

Before executing this operation:
1. Package manager has been initialized (see op-initialize-package-manager.md)
2. Dependency file exists (pyproject.toml, package.json, Cargo.toml, etc.)
3. Network access is available for downloading packages

## Procedure

### Python: uv Dependencies

**Step 1: Read dependency file**

Check pyproject.toml for dependencies:
```bash
# View dependencies section
grep -A 20 "\[project\]" pyproject.toml | grep -A 10 "dependencies"
```

Or check requirements.txt if present:
```bash
cat requirements.txt
```

**Step 2: Install dependencies**

With pyproject.toml:
```bash
# Ensure venv is activated
source .venv/bin/activate

# Sync all dependencies
uv sync

# Or install specific package
uv add <package-name>
```

With requirements.txt:
```bash
uv pip install -r requirements.txt
```

**Step 3: Install dev dependencies**
```bash
# Sync including dev dependencies
uv sync --dev

# Or add dev dependency
uv add --dev <package-name>
```

**Step 4: Verify installation**
```bash
uv pip list
```

### JavaScript/TypeScript: bun or pnpm Dependencies

**Step 1: Read package.json**
```bash
# View dependencies
cat package.json | grep -A 20 '"dependencies"'
cat package.json | grep -A 20 '"devDependencies"'
```

**Step 2: Install with bun**
```bash
# Install all dependencies
bun install

# Install specific package
bun add <package-name>

# Install dev dependency
bun add -d <package-name>
```

**Step 2 (alternative): Install with pnpm**
```bash
# Install all dependencies
pnpm install

# Install specific package
pnpm add <package-name>

# Install dev dependency
pnpm add -D <package-name>
```

**Step 3: Verify installation**
```bash
# List installed packages
bun pm ls
# or
pnpm list
```

### Rust: cargo Dependencies

**Step 1: Read Cargo.toml**
```bash
# View dependencies
grep -A 20 "\[dependencies\]" Cargo.toml
```

**Step 2: Install dependencies**
```bash
# Fetch and compile dependencies
cargo build

# Or just fetch without compiling
cargo fetch
```

**Step 3: Add new dependency**
```bash
cargo add <crate-name>
```

**Step 4: Verify installation**
```bash
cargo tree
```

### Go: go mod Dependencies

**Step 1: Read go.mod**
```bash
cat go.mod
```

**Step 2: Install dependencies**
```bash
# Download all dependencies
go mod download

# Tidy up (add missing, remove unused)
go mod tidy
```

**Step 3: Add new dependency**
```bash
go get <module-path>
```

**Step 4: Verify installation**
```bash
go list -m all
```

### .NET: dotnet Dependencies

**Step 1: Read project file**
```bash
# Find and read .csproj file
cat *.csproj | grep -A 5 "PackageReference"
```

**Step 2: Install dependencies**
```bash
dotnet restore
```

**Step 3: Add new dependency**
```bash
dotnet add package <package-name>
```

**Step 4: Verify installation**
```bash
dotnet list package
```

### C/C++: Manual or Package Manager

C/C++ projects typically use system packages or vendored dependencies.

**Step 1: Check for package managers**
```bash
# Check for vcpkg
vcpkg --version

# Check for conan
conan --version
```

**Step 2: Install system dependencies (Linux/macOS)**
```bash
# Linux (apt)
sudo apt install <package>

# macOS (brew)
brew install <package>
```

**Step 3: Build to verify**
```bash
# CMake
cd build && cmake .. && make

# Make
make
```

### Swift: swift package Dependencies

**Step 1: Read Package.swift**
```bash
cat Package.swift | grep -A 10 "dependencies"
```

**Step 2: Resolve dependencies**
```bash
swift package resolve
```

**Step 3: Add new dependency**

Edit Package.swift to add dependency, then:
```bash
swift package update
```

**Step 4: Verify installation**
```bash
swift package show-dependencies
```

## Checklist

- [ ] Dependency file located and read
- [ ] All required dependencies identified
- [ ] Install command executed successfully
- [ ] Dev dependencies installed (if needed)
- [ ] Lock file updated with installed versions
- [ ] Installation verified with list command
- [ ] No version conflicts or missing packages

## Examples

### Example 1: Python uv Install

```bash
# Activate venv
source .venv/bin/activate

# Install all dependencies
uv sync
# Output:
# Resolved 15 packages in 1.2s
# Installed 15 packages in 0.8s

# Verify
uv pip list
# Output:
# Package    Version
# ---------- -------
# requests   2.31.0
# pytest     8.0.0
# ...
```

### Example 2: TypeScript bun Install

```bash
# Install dependencies
bun install
# Output:
# bun install v1.x.x
# Resolving dependencies...
# Installed 142 packages in 2.3s

# Verify
ls node_modules
# Output: .bin  @types  react  typescript  ...
```

### Example 3: Rust cargo Build

```bash
# Build (installs and compiles deps)
cargo build
# Output:
# Compiling serde v1.0.0
# Compiling tokio v1.0.0
# ...
# Finished dev [unoptimized + debuginfo] target(s)

# Verify
cargo tree --depth 1
# Output:
# my-project v0.1.0
# ├── serde v1.0.0
# └── tokio v1.0.0
```

## Error Handling

### Network Errors

**Symptom**: Package download fails with connection errors.

**Action**:
1. Check internet connectivity
2. Check if package registry is accessible
3. Check for proxy settings if behind corporate firewall
4. Try again after network is restored

### Version Conflicts

**Symptom**: Package manager reports conflicting version requirements.

**Action**:
1. Read the conflict message carefully
2. Identify which packages have conflicting requirements
3. Try updating the conflicting packages to compatible versions
4. If necessary, pin specific versions in the dependency file

### Missing System Dependencies

**Symptom**: Build fails due to missing system libraries (common in C/C++ or native extensions).

**Action**:
1. Read the error message to identify missing library
2. Install the system package (apt, brew, etc.)
3. Retry the installation

### Disk Space Issues

**Symptom**: Installation fails due to insufficient disk space.

**Action**:
1. Check available disk space: `df -h`
2. Clean package caches:
   - Python: `uv cache clean`
   - bun: `bun pm cache rm`
   - cargo: `cargo clean`
3. Free up disk space and retry

### Authentication Required

**Symptom**: Private package requires authentication.

**Action**:
1. Set up authentication for the package registry
2. Configure credentials in the appropriate config file
3. For npm/bun: `.npmrc`
4. For pip/uv: `~/.netrc` or keyring
