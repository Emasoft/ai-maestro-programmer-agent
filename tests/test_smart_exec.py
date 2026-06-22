#!/usr/bin/env python3
"""Hermetic unit tests for scripts/smart_exec.py — pure argv-builder assertions (no subprocess).

smart_exec.py is 583 LOC of deterministic argv builders + selection logic. These
table-driven tests assert the FIXED behaviour of TRDD-e4e12416 (the H1 fail-fast
fix is covered by `test_main_unknown_tool_clean_error`) plus the full
correctness matrix the AMPA audit flagged as untested:

- resolve_tool: known -> ToolSpec, unknown -> ValueError (the typosquat guard).
- bunx/npx/pnpm-dlx/yarn-dlx/npm-exec argv: cmd==pkg vs cmd!=pkg shaping.
- uvx argv: pkg==cmd vs pkg!=cmd, plus the latest=False toggle.
- deno_npm argv: @latest toggle + the minimal permission flags.
- build_argv_for_executor: ecosystem gating (python !-> node executors, etc.).
- choose_best: direct-path-wins, PRIORITY order, RuntimeError when nothing applies.
- powershell_module_argv: the injection guard (SECURITY) + ps_quote escaping.
- main: a leading '--' in tool_args is stripped exactly once.

Only `have()`/`which()` (the executor-DETECTION seam) is monkeypatched — never the
unit under test. No network, no subprocess, no real executors required.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

# smart_exec.py lives in scripts/ which is not a package; add it to sys.path so
# the module can be imported directly (mirrors how the builders are pure funcs).
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import smart_exec  # noqa: E402


@pytest.fixture
def all_executors_present(monkeypatch: pytest.MonkeyPatch) -> None:
    """Force every `have(x)` to True so builders pick their primary executor base."""
    monkeypatch.setattr(smart_exec, "have", lambda _cmd: True)
    monkeypatch.setattr(smart_exec, "which", lambda cmd: f"/usr/bin/{cmd}")


# ----------------------------------------------------------------------------
# resolve_tool — known -> ToolSpec, unknown -> ValueError (typosquat guard)
# ----------------------------------------------------------------------------


@pytest.mark.parametrize("name", ["ruff", "eslint", "deno-fmt", "PSScriptAnalyzer"])
def test_resolve_tool_known_returns_spec(name: str) -> None:
    """resolve_tool returns the matching ToolSpec for every tool listed in TOOL_DB."""
    spec = smart_exec.resolve_tool(name)
    assert isinstance(spec, smart_exec.ToolSpec)
    assert spec.name == name


@pytest.mark.parametrize("name", ["notatool", "ruf", "esLint", "rm -rf"])
def test_resolve_tool_unknown_raises_valueerror(name: str) -> None:
    """resolve_tool raises ValueError for any tool absent from TOOL_DB (fail-fast typosquat guard)."""
    with pytest.raises(ValueError, match="Unknown tool"):
        smart_exec.resolve_tool(name)


# ----------------------------------------------------------------------------
# Node argv builders — cmd==pkg vs cmd!=pkg shaping (the documented core)
# ----------------------------------------------------------------------------


def test_bunx_argv_cmd_equals_pkg(all_executors_present: None) -> None:
    """bunx_argv with cmd==pkg runs the package directly: [bunx, pkg, *args]."""
    assert smart_exec.bunx_argv("eslint", "eslint", ["."]) == ["bunx", "eslint", "."]


def test_bunx_argv_cmd_differs_uses_dash_p(all_executors_present: None) -> None:
    """bunx_argv with cmd!=pkg uses -p (the @stoplight/spectral -> spectral case)."""
    assert smart_exec.bunx_argv("@stoplight/spectral", "spectral", ["lint"]) == [
        "bunx", "-p", "@stoplight/spectral", "spectral", "lint",
    ]


def test_pnpm_dlx_argv_branches() -> None:
    """pnpm_dlx_argv appends cmd explicitly only when cmd!=pkg."""
    assert smart_exec.pnpm_dlx_argv("eslint", "eslint", ["."]) == ["pnpm", "dlx", "eslint", "."]
    assert smart_exec.pnpm_dlx_argv("npm-package-json-lint", "npmPkgJsonLint", ["."]) == [
        "pnpm", "dlx", "npm-package-json-lint", "npmPkgJsonLint", ".",
    ]


def test_yarn_dlx_argv_branches() -> None:
    """yarn_dlx_argv uses -p for the cmd!=pkg case."""
    assert smart_exec.yarn_dlx_argv("eslint", "eslint", []) == ["yarn", "dlx", "eslint"]
    assert smart_exec.yarn_dlx_argv("@stoplight/spectral", "spectral", []) == [
        "yarn", "dlx", "-p", "@stoplight/spectral", "spectral",
    ]


def test_npx_argv_branches() -> None:
    """npx_argv always passes --yes and uses -p for cmd!=pkg."""
    assert smart_exec.npx_argv("prettier", "prettier", ["--check", "."]) == [
        "npx", "--yes", "prettier", "--check", ".",
    ]
    assert smart_exec.npx_argv("@stoplight/spectral", "spectral", []) == [
        "npx", "--yes", "-p", "@stoplight/spectral", "spectral",
    ]


def test_npm_exec_argv_uses_package_flag() -> None:
    """npm_exec_argv always uses the `npm exec --yes --package=<pkg> -- <cmd>` form."""
    assert smart_exec.npm_exec_argv("@stoplight/spectral", "spectral", ["lint"]) == [
        "npm", "exec", "--yes", "--package=@stoplight/spectral", "--", "spectral", "lint",
    ]


# ----------------------------------------------------------------------------
# uvx argv — pkg==cmd vs pkg!=cmd, plus the latest toggle
# ----------------------------------------------------------------------------


def test_uvx_argv_pkg_equals_cmd_latest(all_executors_present: None) -> None:
    """uvx_argv with pkg==cmd and latest=True appends @latest."""
    assert smart_exec.uvx_argv("ruff", "ruff", ["check", "."], latest=True) == [
        "uvx", "ruff@latest", "check", ".",
    ]


def test_uvx_argv_pkg_equals_cmd_no_latest(all_executors_present: None) -> None:
    """uvx_argv with latest=False drops the @latest suffix."""
    assert smart_exec.uvx_argv("ruff", "ruff", ["check"], latest=False) == ["uvx", "ruff", "check"]


def test_uvx_argv_pkg_differs_uses_from(all_executors_present: None) -> None:
    """uvx_argv with pkg!=cmd uses `uvx --from <pkg> <cmd>`."""
    assert smart_exec.uvx_argv("typescript", "tsc", ["--noEmit"]) == [
        "uvx", "--from", "typescript", "tsc", "--noEmit",
    ]


def test_uvx_argv_falls_back_to_uv_tool_run(monkeypatch: pytest.MonkeyPatch) -> None:
    """uvx_argv falls back to `uv tool run` when uvx is absent but uv is present."""
    monkeypatch.setattr(smart_exec, "have", lambda cmd: cmd == "uv")
    assert smart_exec.uvx_argv("ruff", "ruff", ["check"], latest=True) == [
        "uv", "tool", "run", "ruff@latest", "check",
    ]


def test_uvx_argv_raises_when_neither_present(monkeypatch: pytest.MonkeyPatch) -> None:
    """uvx_argv raises RuntimeError when neither uvx nor uv is available (fail-fast)."""
    monkeypatch.setattr(smart_exec, "have", lambda _cmd: False)
    with pytest.raises(RuntimeError, match="uvx/uv not available"):
        smart_exec.uvx_argv("ruff", "ruff", [])


# ----------------------------------------------------------------------------
# deno_npm argv — @latest toggle + minimal permission flags
# ----------------------------------------------------------------------------


def test_deno_npm_argv_latest_and_permissions() -> None:
    """deno_npm_argv with latest=True targets npm:<pkg>@latest with the minimal permission flags."""
    argv = smart_exec.deno_npm_argv("eslint", "eslint", ["."], latest=True)
    assert argv[:2] == ["deno", "run"]
    assert "npm:eslint@latest" in argv
    for perm in ("--allow-read=.", "--allow-write=.", "--allow-env", "--allow-net", "--no-prompt"):
        assert perm in argv
    assert argv[-3:] == ["--", "eslint", "."]


def test_deno_npm_argv_no_latest_drops_suffix() -> None:
    """deno_npm_argv with latest=False targets npm:<pkg> (no @latest)."""
    argv = smart_exec.deno_npm_argv("eslint", "eslint", [], latest=False)
    assert "npm:eslint" in argv
    assert "npm:eslint@latest" not in argv


# ----------------------------------------------------------------------------
# build_argv_for_executor — ecosystem gating
# ----------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("tool", "executor"),
    [
        ("ruff", "bunx"),   # python tool, node executor -> None
        ("ruff", "npm"),    # python tool, node executor -> None
        ("ruff", "deno"),   # python tool, deno npm path requires node/native -> None
        ("eslint", "uvx"),  # node tool, python executor -> None
        ("eslint", "pipx"),  # node tool, python executor -> None
    ],
)
def test_build_argv_ecosystem_gating_returns_none(
    tool: str, executor: str, all_executors_present: None
) -> None:
    """build_argv_for_executor returns None when the executor's ecosystem does not match the spec's."""
    spec = smart_exec.resolve_tool(tool)
    assert smart_exec.build_argv_for_executor(executor, spec, []) is None


def test_build_argv_native_accepts_node_executor_and_docker(all_executors_present: None) -> None:
    """A native-ecosystem tool accepts node executors (bunx) and its docker fallback."""
    spec = smart_exec.resolve_tool("hadolint")  # ecosystem=native, has docker fallback
    assert spec.ecosystem == "native"
    bunx = smart_exec.build_argv_for_executor("bunx", spec, ["Dockerfile"])
    assert bunx is not None and bunx[0] == "bunx"
    docker = smart_exec.build_argv_for_executor("docker", spec, ["Dockerfile"])
    assert docker is not None and docker[0] == "docker"


# ----------------------------------------------------------------------------
# choose_best — direct-path-wins, priority order, RuntimeError fallthrough
# ----------------------------------------------------------------------------


def test_choose_best_direct_path_wins(monkeypatch: pytest.MonkeyPatch) -> None:
    """choose_best returns the direct command when the tool is already on PATH (avoids downloads)."""
    monkeypatch.setattr(smart_exec, "have", lambda cmd: cmd == "ruff")
    spec = smart_exec.resolve_tool("ruff")
    argv, chosen = smart_exec.choose_best(spec, ["check", "."], smart_exec.detect_executors())
    assert chosen == "direct"
    assert argv == ["ruff", "check", "."]


def test_choose_best_honors_priority_order(monkeypatch: pytest.MonkeyPatch) -> None:
    """When the tool is not directly present, choose_best follows PRIORITY (uvx before uv/pipx for python)."""
    # ruff not directly present; uvx IS — PRIORITY["python"] == [uvx, uv, pipx].
    monkeypatch.setattr(smart_exec, "have", lambda cmd: cmd == "uvx")
    spec = smart_exec.resolve_tool("ruff")
    argv, chosen = smart_exec.choose_best(spec, [], {"docker": False})
    assert chosen == "uvx"
    assert argv[0] == "uvx"


def test_choose_best_raises_when_nothing_applies(monkeypatch: pytest.MonkeyPatch) -> None:
    """choose_best raises RuntimeError when no executor can run the tool (fail-fast, no silent skip)."""
    monkeypatch.setattr(smart_exec, "have", lambda _cmd: False)
    spec = smart_exec.resolve_tool("ruff")
    with pytest.raises(RuntimeError, match="No suitable executor"):
        smart_exec.choose_best(spec, [], {"docker": False})


# ----------------------------------------------------------------------------
# powershell_module_argv — injection guard (SECURITY) + ps_quote escaping
# ----------------------------------------------------------------------------


def test_ps_quote_escapes_single_quotes() -> None:
    """ps_quote wraps in single quotes and doubles any embedded single quote (' -> '')."""
    assert smart_exec.ps_quote("a'b") == "'a''b'"
    assert smart_exec.ps_quote("plain") == "'plain'"


def test_powershell_module_argv_accepts_clean_names(monkeypatch: pytest.MonkeyPatch) -> None:
    """powershell_module_argv builds a pwsh -Command invocation for valid module/cmdlet names."""
    monkeypatch.setattr(smart_exec, "have", lambda cmd: cmd == "pwsh")
    argv = smart_exec.powershell_module_argv("PSScriptAnalyzer", "Invoke-ScriptAnalyzer", ["-Path", "."])
    assert argv[0] == "pwsh"
    assert argv[1:3] == ["-NoProfile", "-Command"]
    assert "Save-Module" in argv[3]


@pytest.mark.parametrize(
    ("module", "cmdlet"),
    [
        ("PSScriptAnalyzer; rm -rf /", "Invoke-ScriptAnalyzer"),  # metachars in module
        ("Bad$(whoami)", "Invoke-ScriptAnalyzer"),
        ("PSScriptAnalyzer", "Invoke-ScriptAnalyzer; calc"),      # metachars in cmdlet
        ("PSScriptAnalyzer", "no-leading-cap"),                   # cmdlet must start uppercase
        ("PSScriptAnalyzer", "MissingDash"),                      # cmdlet must be Verb-Noun
    ],
)
def test_powershell_module_argv_rejects_injection(module: str, cmdlet: str) -> None:
    """powershell_module_argv raises ValueError for any module/cmdlet name carrying shell metacharacters (injection guard)."""
    with pytest.raises(ValueError, match="Invalid PowerShell"):
        smart_exec.powershell_module_argv(module, cmdlet, [])


# ----------------------------------------------------------------------------
# main — a leading '--' in tool_args is stripped exactly once
# ----------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("argv_in", "expected_tail"),
    [
        # A leading '--' end-of-options marker is consumed (by argparse REMAINDER
        # and/or smart_exec's own strip) and never leaks into the final argv...
        (["which", "--json", "ruff", "--", "check", "."], ["check", "."]),
        (["which", "--json", "ruff", "check", "."], ["check", "."]),
        # ...while a genuine tool flag like --check is preserved verbatim.
        (["which", "--json", "ruff", "--", "--check"], ["--check"]),
        (["which", "--json", "ruff", "--check"], ["--check"]),
    ],
)
def test_main_strips_leading_double_dash_once(
    argv_in: list[str],
    expected_tail: list[str],
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """main consumes a single leading '--' end-of-options marker and never leaks it into argv, but keeps real tool flags."""
    monkeypatch.setattr(smart_exec, "have", lambda cmd: cmd == "ruff")
    rc = smart_exec.main(argv_in)
    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    # Direct path (ruff is "present") => argv == [cmd, *tool_args]; assert no bare
    # '--' marker survived as the first tool arg, and the real args are intact.
    assert payload["argv"] == ["ruff", *expected_tail]
    assert payload["argv"][1] != "--"


def test_main_unknown_tool_clean_error(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """main on an unknown tool prints a clean `Error: Unknown tool ...` to stderr and returns 1 — NO traceback (H1)."""
    monkeypatch.setattr(smart_exec, "have", lambda _cmd: True)
    rc = smart_exec.main(["which", "notatool"])
    assert rc == 1
    captured = capsys.readouterr()
    assert captured.err.startswith("Error: Unknown tool 'notatool'")
    assert "Traceback" not in captured.err
