# Continuous maintenance (garbage collection for the codebase)

Entropy compounds in agent-generated code. Fight it with small recurring tasks, not big cleanups.

## Recurring tasks to set up

Each one is a prompt run on a schedule (CI cron, GitHub Action with a Claude or Codex step, or a
Claude Code scheduled routine) that opens a small PR or an issue:

1. **Drift scan**: compare the code against the golden principles and open one focused refactor PR
   per deviation class.
2. **Quality score update**: re-rate each area in `docs/QUALITY_SCORE.md` with evidence (test
   coverage, lint violations, open debt items), commit the change.
3. **Stale docs**: find docs not touched in N days whose referenced code changed; propose fixes.
4. **Dead plans**: exec plans in `active/` with no commits referencing them in N days; ask whether
   to complete or drop.
5. **Low-risk cleanup**: unused exports, dead feature flags, duplicate utilities. Auto-merge when
   tests pass if the risk policy allows it.

## Golden principles (starter set)

Write these in `ARCHITECTURE.md` and back each one with a rule or test:

- Centralise shared utilities; no second copy of a helper.
- Validate data at boundaries; never guess at a shape.
- One way to do config, logging, HTTP, errors.
- Every public interface has a test.
- No file over N lines; split by responsibility.

## Feeding review back

When a reviewer leaves the same comment twice, that comment becomes a lint rule, a doc line or a
test. Track this explicitly: a `docs/exec-plans/tech-debt-tracker.md` entry per recurring comment
until it is encoded.
