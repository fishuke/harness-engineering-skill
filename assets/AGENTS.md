# AGENTS.md

This file is a map. Keep it under 60 lines. Details live in the linked docs.

## Every task
- Run: `make dev` (isolated instance; prints URL)
- Test: `make test` · Lint: `make lint` · Logs: `scripts/logs.sh '<query>'`
- Before opening a PR: tests green, lint green, evidence of the change attached (screenshot or log excerpt).

## Read before you touch
- `ARCHITECTURE.md` for layers, dependency direction and where new code goes.
- `docs/PLANS.md` before starting multi-step work; create a plan in `docs/exec-plans/active/`.
- `docs/RELIABILITY.md` before changing anything on a critical path.
- `docs/SECURITY.md` before touching auth, secrets or user data.
- `docs/FRONTEND.md` and `docs/DESIGN.md` for UI work.
- `docs/PRODUCT_SENSE.md` when the request is ambiguous about what the user wants.

## When you are stuck
Ask what tool, doc or rule is missing, then add it. Do not retry blindly.
Record debt you notice in `docs/exec-plans/tech-debt-tracker.md`.

## Escalate to a human when
- A change touches data migration, billing, auth or deletes user data.
- Acceptance criteria are unclear after reading the product spec.
- A test is flaky and you cannot make it deterministic in one attempt.
