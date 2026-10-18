# Target repository layout

```text
AGENTS.md                 # map, one screen; or CLAUDE.md for Claude Code
ARCHITECTURE.md           # layers, dependency direction, where things live
docs/
├── design-docs/          # one file per significant decision, dated
├── exec-plans/
│   ├── active/           # plans for work in flight, updated as it progresses
│   ├── completed/        # moved here when done; the design history
│   └── tech-debt-tracker.md
├── generated/            # machine-generated references (API schemas, DB schema dumps)
├── product-specs/        # what the product should do, acceptance criteria
├── references/           # external docs pulled in-repo so the agent can read them
├── DESIGN.md             # visual / UX principles
├── FRONTEND.md           # frontend conventions
├── PLANS.md              # how exec plans are written and reviewed
├── PRODUCT_SENSE.md      # who the users are, what matters to them
├── QUALITY_SCORE.md      # per-area quality rating, updated by a recurring task
├── RELIABILITY.md        # SLOs, failure modes, what must never break
└── SECURITY.md           # threat model, rules that are non-negotiable
```

## Rules for the map (`AGENTS.md` / `CLAUDE.md`)

- One screen. If it is longer than ~60 lines, it has stopped being a map.
- Each line that names a doc says when to read it: "Read `docs/RELIABILITY.md` before touching
  anything under `src/payments/`."
- Commands the agent needs on every task (run, test, lint, start app, query logs) belong here,
  because they are needed every time. Explanations of *why* belong in the linked docs.
- Keep both `AGENTS.md` and `CLAUDE.md` only if the tools actually differ; otherwise make one a
  one-line pointer to the other.

## Exec plans

A plan file is the agent's working memory across sessions. It holds the goal, the steps, what is
done, what was learned, and what is blocked. Move it from `active/` to `completed/` when the work
ships. Template: `assets/docs/exec-plans/TEMPLATE.md`.

## Generated references

Anything an agent would otherwise have to rediscover by grepping (DB schema, API routes, env vars)
gets generated into `docs/generated/` by a script that CI runs. Stale generated docs are worse than
none, so make CI fail if the output drifts from what is committed.

## Validating the docs

Add a lint step that checks:
- every relative link in `AGENTS.md`, `ARCHITECTURE.md` and `docs/**` resolves;
- every file in `docs/exec-plans/active/` was modified in the last N days (else it is stale or done);
- `AGENTS.md` stays under the length limit.

`scripts/harness_audit.py --strict` exits non-zero on these, so it can run in CI as-is.
