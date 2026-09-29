#!/usr/bin/env python3
"""The release must carry the tag Claude Code's dependency resolver looks for.

A plugin that depends on this one declares
`{"name": "ai-maestro-programmer-agent", "version": "^1.4.0"}`. Claude Code resolves that
by listing THIS repo's tags, filtering to those starting with
`ai-maestro-programmer-agent--v`, and taking the highest one satisfying the range
(https://code.claude.com/docs/en/plugin-dependencies.md, since CC 2.1.110).

The plain `v{version}` tag does NOT match that filter. Without the `{name}--v{version}`
tag, every constrained dependent fails to install with "no git tag satisfying <range>"
while the repo is visibly full of tags — a silent, total outage for the dependent. That is
what grounded the fleet for a day when `ai-maestro-plugin` had the same gap
(ai-maestro-programmer-agent#26).

These tests pin the four halves that must hold: the tag NAME comes from the MANIFEST (not
the directory name — they can differ), a manifest with no name HARD-FAILS (never a tag
literally named `unknown--v1.2.3`), both refs ride ONE atomic push, and the plain
`v{version}` tag survives (GitHub Releases and the marketplace notify chain read it).

TRDD-UMRQ84S9.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import publish  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
PUBLISH_SRC = (ROOT / "scripts" / "publish.py").read_text(encoding="utf-8")


def _write_manifest(tmp_path: Path, data: dict | None) -> Path:
    """Build a throwaway plugin root; `None` writes no manifest at all."""
    if data is not None:
        pj = tmp_path / ".claude-plugin"
        pj.mkdir(parents=True, exist_ok=True)
        (pj / "plugin.json").write_text(json.dumps(data), encoding="utf-8")
    return tmp_path


def test_tag_name_comes_from_the_manifest_not_the_directory(tmp_path: Path) -> None:
    """The dep tag is built from plugin.json's `name`, never the containing dir's name."""
    # The directory is deliberately named nothing like the plugin: the resolver filters on
    # the MANIFEST name, so a dir-derived tag would be invisible to it.
    root = _write_manifest(tmp_path / "some-checkout-dir", {"name": "my-plugin", "version": "9.9.9"})
    assert publish.dependency_resolution_tag(root, "1.4.5") == "my-plugin--v1.4.5"


def test_missing_name_hard_fails(tmp_path: Path) -> None:
    """No `name` in the manifest => raise. NEVER fall back to a placeholder.

    publish.detect_plugin_info() answers "unknown" for a missing name. Reusing it here
    would push a tag literally called `unknown--v1.4.5`: published, and resolvable by
    nobody. A missing tag is a loud failure; a wrongly-named one is a silent outage.
    """
    root = _write_manifest(tmp_path / "a", {"version": "1.0.0"})  # name absent
    with pytest.raises(ValueError):
        publish.dependency_resolution_tag(root, "1.4.5")


def test_blank_name_hard_fails(tmp_path: Path) -> None:
    """An empty-string name is as unusable as a missing one — same hard failure."""
    root = _write_manifest(tmp_path / "b", {"name": "   ", "version": "1.0.0"})
    with pytest.raises(ValueError):
        publish.dependency_resolution_tag(root, "1.4.5")


def test_missing_manifest_hard_fails(tmp_path: Path) -> None:
    """No manifest at all => raise, rather than inventing a tag."""
    root = _write_manifest(tmp_path / "c", None)
    with pytest.raises(ValueError):
        publish.dependency_resolution_tag(root, "1.4.5")


def test_this_plugins_own_manifest_yields_the_expected_tag() -> None:
    """The real manifest resolves to the tag a future dependent would search for."""
    assert publish.dependency_resolution_tag(ROOT, "1.4.5") == "ai-maestro-programmer-agent--v1.4.5"


def test_push_is_atomic_and_carries_both_refs() -> None:
    """Step 13 pushes HEAD + both tags in ONE --atomic transaction.

    A release that landed with only `v{version}` would be published-but-unresolvable for
    every dependent — the half-published state --atomic exists to prevent. Two sequential
    pushes can produce exactly that if the second one fails.
    """
    assert '"--atomic"' in PUBLISH_SRC, "the release push must be atomic"
    # The single push carries HEAD, the release tag, and the dependency-resolution tag.
    assert '["git", "push", "--atomic", "origin", "HEAD", f"v{new_version}", dep_tag]' in PUBLISH_SRC, (
        "the atomic push must carry HEAD + v{version} + the dependency-resolution tag"
    )


def test_release_tag_still_created() -> None:
    """The plain v{version} tag survives — GitHub Releases + notify chain read it."""
    assert '"git", "tag", "-a", f"v{new_version}"' in PUBLISH_SRC


def test_dependency_tag_is_created_annotated() -> None:
    """The dep tag is annotated too (git tag -a), so it carries the release notes."""
    assert '"git", "tag", "-a", dep_tag' in PUBLISH_SRC


def test_never_calls_claude_plugin_tag() -> None:
    """`claude plugin tag <name>` takes a PATH, not a tag name — it silently creates nothing.

    This is the exact trap that cost the fleet a day (#26). Pin it shut: the pipeline must
    do the tagging with git directly.
    """
    assert '"plugin", "tag"' not in PUBLISH_SRC, (
        "do not call `claude plugin tag` — its positional arg is a path, not a tag name"
    )


def test_embedded_cliff_template_body_has_no_trailing_blank_line() -> None:
    """The embedded default cliff template must not emit a trailing blank run at EOF.

    The pipeline normalizes the regenerated CHANGELOG post-cliff (belt-and-suspenders),
    but a bare `git-cliff -o CHANGELOG.md` outside the pipeline reads the template
    directly — if its body ends in a blank line, MD012 re-imports the defect that CI
    red on the v2.1.0 tag. Parse the '''-string the way Python evaluates it (AST, not
    regex over source — the escapes are the trap) and assert the body template's tail.
    """
    import ast as _ast

    tree = _ast.parse(PUBLISH_SRC)
    default = None
    for node in _ast.walk(tree):
        if isinstance(node, _ast.Assign):
            for target in node.targets:
                if getattr(target, "id", None) == "default":
                    if default is not None:
                        raise AssertionError(
                            "second Assign named 'default' found in publish.py — this test "
                            "would pin whichever the walk hits last; disambiguate it"
                        )
                    default = node.value.value
    assert default is not None, "embedded cliff default template not found in publish.py"
    body = re.search(r'body = """(.*?)"""', default, re.S).group(1)
    assert not body.endswith("\n\n"), (
        "embedded cliff template body ends with a blank line — a bare git-cliff run "
        "regenerates CHANGELOG.md with an MD012 EOF defect"
    )
    # Backslash scoped to the TAIL, not the whole body: legitimate escapes inside
    # the body (escaped quotes, regexes) are fine; the defect class this guards is
    # the backslash-continuation idiom at the tail degrading into a literal `\`.
    assert not body.rstrip("\n").endswith("\\"), (
        "embedded cliff template body tail carries a literal backslash — the "
        "backslash-continuation that removes the trailing newline degraded"
    )
