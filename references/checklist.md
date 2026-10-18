# Harness audit checklist

Use this when auditing a repo. `scripts/harness_audit.py` covers the items marked (auto). The rest
need you to read the repo and talk to the user.

## Entry point and docs map
- (auto) Is there an `AGENTS.md` or `CLAUDE.md` at the root?
- (auto) Is it short (under ~60 lines, under ~4 KB)? Long files are manuals, not maps.
- (auto) Does it link to `ARCHITECTURE.md` and to files under `docs/`?
- Does it say *when* to read each linked doc, not just that it exists?
- Are the links valid? (auto: broken relative links are reported)

## System of record
- (auto) `ARCHITECTURE.md` exists and describes layers and dependency direction.
- (auto) `docs/design-docs/`, `docs/product-specs/`, `docs/exec-plans/{active,completed}` exist.
- (auto) `docs/exec-plans/tech-debt-tracker.md` exists.
- Are decisions actually recorded there, or is it an empty scaffold? Scaffold alone is not a harness.
- Is anything important living only in chat, wikis or heads? Pull it in.

## Legibility of the running app
- Can an agent start the app in isolation (per worktree or branch) with one documented command?
- Can it drive the UI or API (browser automation, HTTP client, CLI) and capture evidence?
- Can it read logs, metrics and traces for its own instance?
- Are these commands named in the docs map?

## Mechanical enforcement
- (auto) CI config exists (`.github/workflows`, `.gitlab-ci.yml`, etc.).
- (auto) A linter / formatter config exists.
- (auto) Structural or architecture tests exist (files named like `*arch*`, `*boundar*`, `*dependency*` under tests, or import-linter / dependency-cruiser / ArchUnit config).
- Do lint and test failures explain the fix? Read three failure messages and judge.
- Are data shapes validated at boundaries?

## Feedback loops and maintenance
- Is there a documented PR workflow in which agents respond to review?
- (auto) `docs/QUALITY_SCORE.md` exists.
- Is there a scheduled task (CI cron, GitHub Action, Claude Code routine) that scans for drift and stale docs?
- When review feedback recurs, does it get encoded as a rule?

## Autonomy and risk
- (auto) The entry point or `docs/` mentions escalation / when to ask a human.
- Is merge policy written down and matched to the real cost of a mistake?
