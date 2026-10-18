#!/usr/bin/env python3
"""Audit a repository against the harness-engineering checklist.

Usage: harness_audit.py [--strict] [--json] <repo>

Checks the mechanical items (entry point, docs map, enforcement, maintenance hooks)
and prints a gap list. --strict exits 1 if any gap is found, so it can run in CI.
"""
import argparse
import json
import os
import re
import sys

MAX_MAP_LINES = 60
MAX_MAP_BYTES = 4096


def exists_any(root, *paths):
    return [p for p in paths if os.path.exists(os.path.join(root, p))]


def glob_any(root, pattern, dirs=("tests", "test", "spec", "src")):
    rx = re.compile(pattern, re.I)
    for d in dirs:
        base = os.path.join(root, d)
        if not os.path.isdir(base):
            continue
        for dp, _, files in os.walk(base):
            if "node_modules" in dp or "/." in dp:
                continue
            for f in files:
                if rx.search(f):
                    return os.path.relpath(os.path.join(dp, f), root)
    return None


def broken_links(root, rel):
    path = os.path.join(root, rel)
    try:
        text = open(path, encoding="utf-8", errors="replace").read()
    except OSError:
        return []
    out = []
    for m in re.finditer(r"\]\(([^)#\s]+)(?:#[^)]*)?\)|`([A-Za-z0-9_./-]+\.md)`", text):
        target = m.group(1) or m.group(2)
        if re.match(r"^[a-z]+://", target):
            continue
        full = os.path.normpath(os.path.join(os.path.dirname(path), target))
        if not os.path.exists(full):
            out.append(target)
    return sorted(set(out))


def audit(root):
    checks = []

    def add(name, ok, detail=""):
        checks.append({"check": name, "ok": bool(ok), "detail": detail})

    entry = exists_any(root, "AGENTS.md", "CLAUDE.md")
    add("entry point (AGENTS.md or CLAUDE.md) exists", entry, ", ".join(entry))
    if entry:
        p = os.path.join(root, entry[0])
        text = open(p, encoding="utf-8", errors="replace").read()
        lines = text.count("\n") + 1
        size = len(text.encode())
        add(f"entry point is a map (<= {MAX_MAP_LINES} lines, <= {MAX_MAP_BYTES} B)",
            lines <= MAX_MAP_LINES and size <= MAX_MAP_BYTES, f"{entry[0]}: {lines} lines, {size} B")
        add("entry point links to ARCHITECTURE.md", "ARCHITECTURE.md" in text)
        add("entry point links into docs/", "docs/" in text)
        add("entry point mentions escalation to a human",
            re.search(r"escalat|ask a human|ask the user|human review", text, re.I))
        bl = broken_links(root, entry[0])
        add("entry point has no broken links", not bl, ", ".join(bl))

    add("ARCHITECTURE.md exists", exists_any(root, "ARCHITECTURE.md", "docs/ARCHITECTURE.md"))
    if exists_any(root, "ARCHITECTURE.md"):
        bl = broken_links(root, "ARCHITECTURE.md")
        add("ARCHITECTURE.md has no broken links", not bl, ", ".join(bl))

    for d in ["docs/design-docs", "docs/product-specs", "docs/exec-plans/active",
              "docs/exec-plans/completed"]:
        add(f"{d}/ exists", os.path.isdir(os.path.join(root, d)))
    add("docs/exec-plans/tech-debt-tracker.md exists",
        exists_any(root, "docs/exec-plans/tech-debt-tracker.md"))
    add("docs/QUALITY_SCORE.md exists", exists_any(root, "docs/QUALITY_SCORE.md"))
    add("docs/RELIABILITY.md or SECURITY.md exists",
        exists_any(root, "docs/RELIABILITY.md", "docs/SECURITY.md"))

    ci = exists_any(root, ".github/workflows", ".gitlab-ci.yml", ".circleci", "Jenkinsfile",
                    "azure-pipelines.yml", "bitbucket-pipelines.yml")
    add("CI config exists", ci, ", ".join(ci))
    lint = exists_any(root, ".eslintrc", ".eslintrc.js", ".eslintrc.json", ".eslintrc.cjs",
                      "eslint.config.js", "eslint.config.mjs", "eslint.config.ts", "biome.json",
                      "ruff.toml", ".ruff.toml", ".flake8", "setup.cfg", ".pylintrc", ".golangci.yml",
                      ".rubocop.yml", ".editorconfig", "clippy.toml", ".semgrep.yml", "semgrep.yml")
    pyproject = os.path.join(root, "pyproject.toml")
    if os.path.exists(pyproject) and re.search(r"\[tool\.(ruff|flake8|pylint|mypy)", open(pyproject).read()):
        lint.append("pyproject.toml")
    add("linter / formatter config exists", lint, ", ".join(lint))

    arch = exists_any(root, ".importlinter", ".dependency-cruiser.js", ".dependency-cruiser.cjs",
                      ".dependency-cruiser.json")
    found = glob_any(root, r"(arch|boundar|dependenc|layer|structur)")
    add("architecture / boundary enforcement exists", arch or found, ", ".join(arch) or (found or ""))

    sched = False
    wf = os.path.join(root, ".github/workflows")
    if os.path.isdir(wf):
        for f in os.listdir(wf):
            try:
                if "schedule:" in open(os.path.join(wf, f), errors="replace").read():
                    sched = True
            except OSError:
                pass
    add("a scheduled maintenance job exists (cron in CI)", sched)

    return checks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", nargs="?", default=".")
    ap.add_argument("--strict", action="store_true", help="exit 1 on any gap")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    root = os.path.abspath(a.repo)
    if not os.path.isdir(root):
        sys.exit(f"not a directory: {root}")
    checks = audit(root)
    gaps = [c for c in checks if not c["ok"]]
    if a.json:
        print(json.dumps({"repo": root, "checks": checks, "gaps": len(gaps)}, indent=2))
    else:
        print(f"Harness audit: {root}\n")
        for c in checks:
            mark = "ok " if c["ok"] else "GAP"
            print(f"  [{mark}] {c['check']}" + (f"  ({c['detail']})" if c["detail"] else ""))
        print(f"\n{len(checks) - len(gaps)}/{len(checks)} passed, {len(gaps)} gaps")
    if a.strict and gaps:
        sys.exit(1)


if __name__ == "__main__":
    main()
